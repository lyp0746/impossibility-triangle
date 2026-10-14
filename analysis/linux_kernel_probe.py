# -*- coding: utf-8 -*-
"""linux_kernel_probe.py — 大型模块化开源项目的实证探针（附录 W.6）。

两次执行：
  (1) torvalds/linux  —— commit 模式（该仓库 GitHub PR 被禁用）；
  (2) nodejs/node     —— pull 模式（PR 可用，merge latency 更接近审阅时延）。

假设：跨多个子系统（top-level 目录）的改动，比单子系统改动更慢被接受。

统计：Spearman r + p（scipy）、Mann–Whitney U、Cliff's delta、bootstrap 中位数差 CI。

必须随结果报告的方法学局限（见附录 W.6 自检）：
  · commit 模式的 author→committer gap 混淆了"评审延迟 / 排队延迟 / 维护者树合并"；
  · 样本极度不均衡（跨子系统改动极稀有）；
  · 单一/双案例无随机对照，因果推论有限。

用法：
  python analysis/linux_kernel_probe.py --n 200
"""
import argparse
import json
import os
import statistics as st
import subprocess
import time
from datetime import datetime

import numpy as np
import requests
from scipy import stats

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT = os.path.join(HERE, "analysis", "results", "linux_kernel_probe.json")
SVG = os.path.join(HERE, "assets", "svg", "fig35-linux-probe.svg")


def token():
    out = subprocess.run([os.environ.get("GIT_BIN", r"D:\Git\cmd\git.exe"),
                          "credential", "fill"],
                         input="protocol=https\nhost=github.com\n\n",
                         capture_output=True, text=True,
                         env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    for line in out.stdout.splitlines():
        if line.startswith("password="):
            return line[len("password="):].strip()
    raise SystemExit("no token")


def parse(dt):
    return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ").timestamp()


def top_dirs(files):
    ds = set()
    for f in files:
        name = f.get("filename", "")
        ds.add(name.split("/", 1)[0] if "/" in name else "(root)")
    return ds


def run_commits(h, repo, n):
    base = f"https://api.github.com/repos/{repo}"
    pr_status = requests.get(f"{base}/pulls", headers=h, timeout=30,
                             params={"per_page": 1}).status_code
    rows, page = [], 1
    while len(rows) < n and page <= 12:
        r = requests.get(f"{base}/commits", headers=h, timeout=60,
                         params={"per_page": 100, "page": page})
        r.raise_for_status()
        cs = r.json()
        if not cs:
            break
        for c in cs:
            if len(c.get("parents", [])) != 1:
                continue
            sha = c["sha"]
            d = requests.get(f"{base}/commits/{sha}", headers=h, timeout=60)
            if d.status_code != 200:
                continue
            dirs = top_dirs(d.json().get("files", []))
            a = parse(c["commit"]["author"]["date"]); m = parse(c["commit"]["committer"]["date"])
            rows.append({"dirs": len(dirs), "latency_h": round(max(0.0, (m - a) / 3600.0), 3)})
            time.sleep(0.02)
            if len(rows) >= n:
                break
        page += 1
    return {"mode": "commits", "pr_status": pr_status, "rows": rows}


def run_pulls(h, repo, n):
    base = f"https://api.github.com/repos/{repo}"
    rows, page = [], 1
    while len(rows) < n and page <= 12:
        r = requests.get(f"{base}/pulls", headers=h, timeout=60,
                         params={"state": "closed", "sort": "updated", "direction": "desc",
                                 "per_page": 100, "page": page})
        r.raise_for_status()
        prs = r.json()
        if not prs:
            break
        for pr in prs:
            if not pr.get("merged_at"):
                continue
            fr = requests.get(f"{base}/pulls/{pr['number']}/files", headers=h, timeout=60,
                              params={"per_page": 100})
            if fr.status_code != 200:
                continue
            dirs = top_dirs(fr.json())
            lat = (parse(pr["merged_at"]) - parse(pr["created_at"])) / 3600.0
            rows.append({"dirs": len(dirs), "latency_h": round(max(0.0, lat), 3)})
            time.sleep(0.03)
            if len(rows) >= n:
                break
        page += 1
    return {"mode": "pulls", "pr_status": 200, "rows": rows}


def stats_block(rows):
    dirs = np.array([r["dirs"] for r in rows], float)
    lat = np.array([r["latency_h"] for r in rows], float)
    single = lat[dirs <= 1]; cross = lat[dirs >= 2]
    sp_r, sp_p = stats.spearmanr(dirs, lat)
    out = {
        "n": len(rows),
        "n_single": int((dirs <= 1).sum()),
        "n_cross": int((dirs >= 2).sum()),
        "share_single": round(float((dirs <= 1).mean()), 3),
        "spearman_r": round(float(sp_r), 4),
        "spearman_p": round(float(sp_p), 4),
        "median_latency_single_h": round(float(np.median(single)), 2) if len(single) else None,
        "median_latency_cross_h": round(float(np.median(cross)), 2) if len(cross) else None,
    }
    if len(cross) >= 3 and len(single) >= 3:
        u, pu = stats.mannwhitneyu(cross, single, alternative="two-sided")
        out["mannwhitney_p"] = round(float(pu), 4)
        # Cliff's delta
        gt = sum((a > b) for a in cross for b in single)
        lt = sum((a < b) for a in cross for b in single)
        out["cliffs_delta"] = round((gt - lt) / (len(cross) * len(single)), 3)
        # bootstrap CI for median difference (cross - single)
        rng = np.random.default_rng(0)
        diffs = []
        for _ in range(2000):
            cs = rng.choice(cross, len(cross), replace=True)
            ss = rng.choice(single, len(single), replace=True)
            diffs.append(np.median(cs) - np.median(ss))
        out["median_diff_ci95"] = [round(float(np.percentile(diffs, 2.5)), 2),
                                   round(float(np.percentile(diffs, 97.5)), 2)]
    return out


def build_svg(blocks):
    W, H = 1000, 560
    b = [f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         '<style>text{font-family:"Microsoft YaHei","SimHei",Arial,sans-serif;}</style>',
         '<text x="40" y="46" font-size="24" font-weight="700">'
         '图 W.1　两个大型项目的实证探针：跨子系统改动是否更慢</text>']
    y = 90
    for name, s in blocks.items():
        b.append(f'<text x="40" y="{y}" font-size="17" font-weight="600">{name}（{s["mode"]}）</text>')
        b.append(f'<text x="40" y="{y+26}" font-size="14" fill="#555">'
                 f'n={s["n"]}（单子系统 {s["n_single"]} / 跨子系统 {s["n_cross"]}）；'
                 f'Spearman r={s["spearman_r"]} (p={s["spearman_p"]})</text>')
        s1 = s["median_latency_single_h"]; c1 = s["median_latency_cross_h"]
        mx = max([v for v in (s1, c1) if v] or [1])
        for i, (lab, v, col) in enumerate([("单子系统", s1, "#3a6ea5"), ("跨子系统", c1, "#c94f4f")]):
            h = 0 if not v else int(v / mx * 90)
            x = 420 + i * 240
            b.append(f'<rect x="{x}" y="{y+40-h}" width="120" height="{h}" rx="6" fill="{col}" opacity="0.5"/>')
            b.append(f'<text x="{x+60}" y="{y+40-h-8}" text-anchor="middle" font-size="14" fill="{col}">'
                     f'{v if v is not None else "—"} h</text>')
            b.append(f'<text x="{x+60}" y="{y+60}" text-anchor="middle" font-size="13">{lab}</text>')
        y += 150
    b.append('<text x="40" y="540" font-size="13" fill="#888">'
             '数据：GitHub API 实时抓取。局限：量度混淆、样本不均衡、无随机对照（见附录 W.6 自检）。</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">'
            + "\n".join(b) + "</svg>")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--repos", nargs="*", default=["torvalds/linux", "nodejs/node"])
    args = ap.parse_args()
    h = {"Authorization": f"token {token()}",
         "Accept": "application/vnd.github+json", "User-Agent": "probe"}
    blocks = {}
    for repo in args.repos:
        mode = "commits" if repo == "torvalds/linux" else "pulls"
        d = run_commits(h, repo, args.n) if mode == "commits" else run_pulls(h, repo, args.n)
        s = stats_block(d["rows"])
        s["mode"] = d["mode"]; s["pr_status"] = d["pr_status"]
        blocks[repo] = s
    out = {"repos": blocks,
           "linux_pr_disabled": blocks.get("torvalds/linux", {}).get("pr_status") == 404}
    os.makedirs(os.path.dirname(RESULT), exist_ok=True)
    with open(RESULT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    with open(SVG, "w", encoding="utf-8") as f:
        f.write(build_svg(blocks))
    print(json.dumps(out, ensure_ascii=False, indent=2))
    print("wrote", RESULT)
    print("wrote", SVG)


if __name__ == "__main__":
    main()
