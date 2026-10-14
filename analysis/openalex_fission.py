# -*- coding: utf-8 -*-
"""openalex_fission.py — 文献网络的引用层面探针（附录 Y 的 O36 第一次执行）。

假设（第 12 章“学科分裂”的引用层面版本）：
  若学科走向分裂，则论文的**跨领域引用比例**应随时间下降。

操作化（OpenAlex API，公开免费）：
  · 固定若干领域（物理/计算机/神经科学）与年份（1990/2000/2010/2020）；
  · 每个 (领域, 年份) 抽 25 篇论文，取其参考文献（每篇最多 50 条）；
  · 批次查询参考文献的 primary_topic.field，计算与本领域不同的比例；
  · 检验跨领域引用比例随年份的变化。

局限：
  · OpenAlex 的字段归类本身有误差；参考文献覆盖不全（早期论文尤甚）；
  · 各领域参考文献数随时间增长，比例可能受此影响；
  · “跨领域引用”是知识传递的必要非充分代理。

用法：python analysis/openalex_fission.py
"""
import json
import os
import time

import requests

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT = os.path.join(HERE, "analysis", "results", "openalex_fission.json")
SVG = os.path.join(HERE, "assets", "svg", "fig37-openalex-fission.svg")
H = {"User-Agent": "triangle-probe/1.0 (mailto:1610369302@qq.com)"}
FIELDS = {"Physics": 31, "Computer Science": 17, "Neuroscience": 28}
YEARS = [1990, 2000, 2010, 2020]
N_WORKS = 25
CAP_REFS = 50
BATCH = 50


def get(url, **params):
    for _ in range(4):
        try:
            r = requests.get(url, headers=H, timeout=50, params=params)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        time.sleep(2)
    return None


def sample_works(field_id, year):
    d = get("https://api.openalex.org/works",
            filter=f"publication_year:{year},primary_topic.field.id:fields/{field_id}",
            per_page=N_WORKS, select="id,primary_topic,referenced_works")
    if not d:
        return []
    out = []
    for w in d.get("results", []):
        refs = [x for x in (w.get("referenced_works") or [])][:CAP_REFS]
        if refs:
            out.append(refs)
    return out


def field_of(ids):
    """批次取参考文献的领域 id -> {work_id: field_id}"""
    m = {}
    for i in range(0, len(ids), BATCH):
        chunk = ids[i:i + BATCH]
        d = get("https://api.openalex.org/works",
                filter="openalex_id:" + "|".join(x.split("/")[-1] for x in chunk),
                per_page=BATCH, select="id,primary_topic")
        if not d:
            continue
        for w in d.get("results", []):
            f = (w.get("primary_topic") or {}).get("field") or {}
            if "id" in f:
                m[w["id"].split("/")[-1]] = int(f["id"].split("/")[-1])
        time.sleep(0.15)
    return m


def run_field(name, fid):
    rows = {}
    for y in YEARS:
        works = sample_works(fid, y)
        allrefs = [r for w in works for r in w]
        fm = field_of(sorted(set(allrefs)))
        per_work, cross_tot, tot = [], 0, 0
        for w in works:
            known = [fm[r.split("/")[-1]] for r in w if r.split("/")[-1] in fm]
            if not known:
                continue
            cross = sum(1 for f in known if f != fid)
            per_work.append(cross / len(known))
            cross_tot += cross
            tot += len(known)
        rows[str(y)] = {"works": len(per_work),
                        "refs_known": tot,
                        "cross_field_share": round(cross_tot / tot, 3) if tot else None,
                        "mean_per_work": round(sum(per_work) / len(per_work), 3) if per_work else None}
        print(name, y, rows[str(y)])
    return rows


def build_svg(data):
    W, Hh = 1000, 520
    b = [f'<rect width="{W}" height="{Hh}" fill="#ffffff"/>',
         '<style>text{font-family:"Microsoft YaHei","SimHei",Arial,sans-serif;}</style>',
         '<text x="40" y="46" font-size="24" font-weight="700">'
         '图 Y.2　跨领域引用比例随时间的变化（OpenAlex）</text>']
    x0, x1, y0, y1 = 110, 940, 420, 120
    cols = {"Physics": "#3a6ea5", "Computer Science": "#009E73", "Neuroscience": "#b8862f"}
    for name, rows in data.items():
        pts = []
        for y in YEARS:
            v = rows.get(str(y), {}).get("cross_field_share")
            if v is None:
                continue
            X = x0 + (y - min(YEARS)) / (max(YEARS) - min(YEARS)) * (x1 - x0)
            Y = y0 - v * (y0 - y1)
            pts.append(f"{X:.0f},{Y:.0f}")
            b.append(f'<circle cx="{X:.0f}" cy="{Y:.0f}" r="4.5" fill="{cols.get(name,"#333")}"/>')
        if pts:
            b.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{cols.get(name,"#333")}" stroke-width="2.4"/>')
    for i, y in enumerate(YEARS):
        X = x0 + (y - min(YEARS)) / (max(YEARS) - min(YEARS)) * (x1 - x0)
        b.append(f'<text x="{X:.0f}" y="{y0+26}" text-anchor="middle" font-size="14">{y}</text>')
    ly = 120
    for name, col in cols.items():
        b.append(f'<line x1="700" y1="{ly}" x2="740" y2="{ly}" stroke="{col}" stroke-width="2.5"/>')
        b.append(f'<text x="748" y="{ly+5}" font-size="14">{name}</text>')
        ly += 26
    b.append('<text x="40" y="500" font-size="13" fill="#888">'
             '纵轴＝跨领域引用占比。数据：OpenAlex API 实时抓取。局限：字段归类误差、早期引文覆盖不全。</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}">' + "\n".join(b) + "</svg>")


def main():
    data = {}
    for name, fid in FIELDS.items():
        data[name] = run_field(name, fid)
    os.makedirs(os.path.dirname(RESULT), exist_ok=True)
    with open(RESULT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with open(SVG, "w", encoding="utf-8") as f:
        f.write(build_svg(data))
    print("wrote", RESULT)
    print("wrote", SVG)


if __name__ == "__main__":
    main()
