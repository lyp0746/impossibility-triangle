# -*- coding: utf-8 -*-
"""arxiv_crossfield.py — arXiv 跨领域耦合探针（附录 Y.1 的第一次执行）。

假设（来自第 12 章“学科分裂 = 三角选择的分裂”）：
  若学科在长期走向分裂，则论文的**跨领域耦合**（cross-listing）应随时间下降或停滞；
  即“传递性 T 被让出”在文献层面留下可测痕迹。

操作化（arXiv API，公开免费）：
  · 在若干年份各抽样 N 篇论文；
  · 统计每篇论文的 arXiv 分类数（primary + cross-list）；
  · 指标：cross-list 比例、平均分类数、跨类别对数熵；
  · 检验：随年份是否下降（Spearman + bootstrap 区间）。

局限：
  · arXiv 只覆盖预印本，且领域构成随时间变化（cs 大增）；
  · cross-listing 是“作者自选标签”，不等于真实引用耦合；
  · 需控制领域构成，否则“cs 占比上升”会污染趋势。

用法：python analysis/arxiv_crossfield.py --per-year 300
"""
import argparse
import json
import os
import subprocess
import time
import urllib.parse
import xml.etree.ElementTree as ET

import requests

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT = os.path.join(HERE, "analysis", "results", "arxiv_crossfield.json")
SVG = os.path.join(HERE, "assets", "svg", "fig36-arxiv-crossfield.svg")
NS = {"a": "http://www.w3.org/2005/Atom", "arx": "http://arxiv.org/schemas/atom"}
YEARS = [1995, 2000, 2005, 2010, 2015, 2020, 2023]


def fetch_year(year, want):
    rows, start = [], 0
    q = f"submittedDate:[{year}01010000 TO {year}12312359]"
    url = ("http://export.arxiv.org/api/query?"
           + urllib.parse.urlencode({"search_query": q, "start": 0, "max_results": 100,
                                     "sortBy": "submittedDate", "sortOrder": "ascending"}))
    while len(rows) < want and start <= 2000:
        u = url.replace("start=0", f"start={start}")
        r = requests.get(u, timeout=60, headers={"User-Agent": "triangle-probe/1.0"})
        if r.status_code != 200:
            break
        root = ET.fromstring(r.content)
        entries = root.findall("a:entry", NS)
        if not entries:
            break
        for e in entries:
            cats = [c.get("term") for c in e.findall("a:category", NS)]
            prim = e.find("arx:primary_category", NS)
            if prim is not None and prim.get("term") not in cats:
                cats.append(prim.get("term"))
            rows.append(sorted(set(cats)))
        start += 100
        time.sleep(3)  # arXiv 建议的礼貌间隔
    return rows


def analyse_year(cats_list):
    n = len(cats_list)
    if not n:
        return None
    multi = sum(1 for c in cats_list if len(c) >= 2)
    mean = sum(len(c) for c in cats_list) / n
    return {"n": n, "share_multicat": round(multi / n, 3), "mean_cats": round(mean, 3)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-year", type=int, default=300)
    args = ap.parse_args()
    out = {}
    for y in YEARS:
        rows = fetch_year(y, args.per_year)
        a = analyse_year(rows)
        out[str(y)] = a
        print(y, a)
    os.makedirs(os.path.dirname(RESULT), exist_ok=True)
    with open(RESULT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    # 简单趋势图
    W, H = 1000, 500
    b = [f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         '<style>text{font-family:"Microsoft YaHei","SimHei",Arial,sans-serif;}</style>',
         '<text x="40" y="46" font-size="24" font-weight="700">'
         '图 Y.1　arXiv 跨领域耦合随时间的变化（跨分类论文占比）</text>']
    xs = [y for y in YEARS if out.get(str(y))]
    vals = [out[str(y)]["share_multicat"] for y in xs]
    if xs:
        x0, x1, y0, y1 = 100, 940, 420, 110
        mx = max(vals) or 1
        pts = []
        for y, v in zip(xs, vals):
            X = x0 + (y - min(xs)) / max(1, max(xs) - min(xs)) * (x1 - x0)
            Y = y0 - v / mx * (y0 - y1)
            pts.append(f"{X:.0f},{Y:.0f}")
            b.append(f'<circle cx="{X:.0f}" cy="{Y:.0f}" r="5" fill="#3a6ea5"/>')
            b.append(f'<text x="{X:.0f}" y="{Y-10:.0f}" text-anchor="middle" font-size="13">{v:.2f}</text>')
            b.append(f'<text x="{X:.0f}" y="{y0+24:.0f}" text-anchor="middle" font-size="13">{y}</text>')
        b.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#3a6ea5" stroke-width="2.4"/>')
    b.append('<text x="40" y="470" font-size="13" fill="#888">'
             '数据：arXiv API 实时抓取。局限：领域构成随时间变化、cross-list 为作者自选标签。</text>')
    with open(SVG, "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">' + "\n".join(b) + "</svg>")
    print("wrote", RESULT)
    print("wrote", SVG)


if __name__ == "__main__":
    main()
