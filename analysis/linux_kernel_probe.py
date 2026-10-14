# -*- coding: utf-8 -*-
"""linux_kernel_probe.py — Linux 内核的实证探针（附录 W.3 / X.4.1 的第一次执行）。

背景事实（本身就是一项发现）：
  torvalds/linux 的 GitHub **Pull Requests 被禁用**（返回 404）——内核走邮件列表，
  不走过 GitHub PR。因此本探针改用 **commit 历史**。

假设（来自第 10 章 / 附录 W.3）：
  在内核这类"模块化 A+T"系统中，跨多个子系统（top-level 目录）的改动，
  比单子系统改动**更慢被接受**（C 型架构缺口）。

操作化（GitHub API，无需克隆 6.4 GB 仓库）：
  · 取 torvalds/linux 的**非合并提交**（parents == 1，即实际补丁）；
  · 每个提交：改动的 top-level 目录数（跨子系统程度）；
  · 时延代理：committer.date − author.date（补丁从撰写到落地的时间）；
  · 检验：目录数越多，时延是否越长（Spearman + 分桶中位数）。

必须随结果一起报告的局限：
  · 时延代理受"维护者即作者"影响（自提交时 gap≈0）；
  · commit 端点的 files 对大改动截断（最多 300 文件）；
  · 时延受审阅人作息、补丁大小、合并窗口等多因素影响，不能单独归因于"架构缺口"。

用法：python analysis/linux_kernel_probe.py --n 200
"""
import argparse
import json
import os
import statistics as st
import subprocess
import time
from datetime import datetime

import requests

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT = os.path.join(HERE, "analysis", "results", "linux_kernel_probe.json")
SVG = os.path.join(HERE, "assets", "svg", "fig35-linux-probe.svg")
REPO = "torvalds/linux"


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


def run(n):
    h = {"Authorization": f"token {token()}",
         "Accept": "application/vnd.github+json", "User-Agent": "linux-probe"}
    base = f"https://api.github.com/repos/{REPO}"
    # 记录 PR 禁用这一事实
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
                continue  # 只要非合并提交（实际补丁）
            sha = c["sha"]
            d = requests.get(f"{base}/commits/{sha}", headers=h, timeout=60)
            if d.status_code != 200:
                continue
            files = d.json().get("files", [])
            dirs = top_dirs(files)
            a = parse(c["commit"]["author"]["date"])
            m = parse(c["commit"]["committer"]["date"])
            rows.append({"sha": sha[:8], "dirs": len(dirs),
                         "changed_files": c.get("files", len(files)),
                         "latency_h": round(max(0.0, (m - a) / 3600.0), 3),
                         "same_author_committer":
                             c["commit"]["author"]["date"] == c["commit"]["committer"]["date"]})
            time.sleep(0.02)
            if len(rows) >= n:
                break
        page += 1
    return pr_status, rows


def spearman(xs, ys):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(xs), rank(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else 0.0


def analyse(rows):
    dirs = [r["dirs"] for r in rows]
    lat = [r["latency_h"] for r in rows]
    buckets = {"1": [], "2": [], "3-4": [], "5+": []}
    for r in rows:
        d = r["dirs"]
        k = "1" if d <= 1 else "2" if d == 2 else "3-4" if d <= 4 else "5+"
        buckets[k].append(r["latency_h"])
    frm = [r for r in rows if not r["same_author_committer"]]
    return {
        "n": len(rows),
        "n_author_ne_committer": len(frm),
        "spearman_dirs_latency_all": round(spearman(dirs, lat), 4),
        "spearman_dirs_latency_reviewed": (
            round(spearman([r["dirs"] for r in frm], [r["latency_h"] for r in frm]), 4)
            if len(frm) > 5 else None),
        "median_latency_by_dirs": {k: (round(st.median(v), 2) if v else None)
                                    for k, v in buckets.items()},
        "count_by_dirs": {k: len(v) for k, v in buckets.items()},
        "median_dirs": st.median(dirs),
        "max_dirs": max(dirs),
        "share_cross_subsystem": round(sum(1 for d in dirs if d >= 2) / len(dirs), 3),
    }


def build_svg(res, pr_status):
    W, H = 1000, 540
    b = [f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         '<style>text{font-family:"Microsoft YaHei","SimHei",Arial,sans-serif;}</style>',
         '<text x="40" y="46" font-size="24" font-weight="700">'
         '图 W.1　Linux 内核实证探针：跨子系统改动是否更慢落地</text>',
         f'<text x="40" y="76" font-size="15" fill="#666">'
         f'n={res["n"]} 个非合并提交；Spearman(dirs,latency) 全体={res["spearman_dirs_latency_all"]}，'
         f'仅审阅子集={res["spearman_dirs_latency_reviewed"]}</text>']
    mx = max([v for v in res["median_latency_by_dirs"].values() if v] or [1])
    x = 100
    for k in ["1", "2", "3-4", "5+"]:
        v = res["median_latency_by_dirs"].get(k)
        cnt = res["count_by_dirs"].get(k, 0)
        h = 0 if not v else int(v / mx * 320)
        col = ["#3a6ea5", "#009E73", "#b8862f", "#c94f4f"][["1", "2", "3-4", "5+"].index(k)]
        b.append(f'<rect x="{x}" y="{440-h}" width="140" height="{h}" rx="6" fill="{col}" opacity="0.5"/>')
        b.append(f'<text x="{x+70}" y="{440-h-10}" text-anchor="middle" font-size="15" fill="{col}">'
                 f'{v if v is not None else "—"} h</text>')
        b.append(f'<text x="{x+70}" y="470" text-anchor="middle" font-size="15">{k} 个目录</text>')
        b.append(f'<text x="{x+70}" y="492" text-anchor="middle" font-size="13" fill="#888">n={cnt}</text>')
        x += 210
    b.append(f'<text x="40" y="525" font-size="13" fill="#888">'
             f'数据：GitHub API 实时抓取（torvalds/linux；其 GitHub PR 被禁用，状态码 {pr_status}）'
             f'。局限：PR/邮件列表偏差、files 截断、自提交 gap≈0。</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">'
            + "\n".join(b) + "</svg>")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=200)
    args = ap.parse_args()
    pr_status, rows = run(args.n)
    res = analyse(rows)
    res["github_pull_requests_disabled"] = (pr_status == 404)
    res["pull_request_endpoint_status"] = pr_status
    os.makedirs(os.path.dirname(RESULT), exist_ok=True)
    with open(RESULT, "w", encoding="utf-8") as f:
        json.dump({"summary": res, "rows": rows}, f, ensure_ascii=False, indent=2)
    with open(SVG, "w", encoding="utf-8") as f:
        f.write(build_svg(res, pr_status))
    print(json.dumps(res, ensure_ascii=False, indent=2))
    print("wrote", RESULT)
    print("wrote", SVG)


if __name__ == "__main__":
    main()
