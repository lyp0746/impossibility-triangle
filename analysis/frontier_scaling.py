# -*- coding: utf-8 -*-
"""frontier_scaling.py — 说明性模型 T 的前沿如何随系统规模 n 变化。

模型与 triangle_frontier.py 相同：
  r_i ∈ {0,1,2}，预算 Σ r_i ≤ K（精确描述贵一倍）；
  C = #{r_i=2}/n，A = 1 − 边界数/(n−1)，T = 相邻双覆盖数/(n−1)。

n 较小时用精确枚举（triangle_frontier.py）；本脚本用**局部搜索 + 多权重**
在较大 n 上估计 Pareto 前沿与坐标和上界，检验"三角是不是有限规模效应"。

结论（可复算）：在固定预算比 α=K/n 下，坐标和上界随 n 增大而上升，
趋近 α+1；**模型 T 的"三选二"是有限规模 + 紧预算现象**，
真正的取舍需要正的交互惩罚 ψ（见附录 A.7）。这支持第 2 章的记帐不等式。
"""
import json
import os
import random

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT = os.path.join(HERE, "analysis", "results", "frontier_scaling.json")
SVG = os.path.join(HERE, "assets", "svg", "fig04-frontier-scaling.svg")


def metrics(r):
    n = len(r)
    C = sum(1 for x in r if x == 2) / n
    A = 1.0 - sum(1 for i in range(n - 1) if r[i] != r[i + 1]) / (n - 1)
    T = sum(1 for i in range(n - 1) if r[i] >= 1 and r[i + 1] >= 1) / (n - 1)
    return C, A, T


def hill_climb(n, K, w, rng, restarts=12):
    best = None
    best_val = -1e18
    for _ in range(restarts):
        r = [rng.choice((0, 1, 2)) for _ in range(n)]
        while sum(r) > K:
            r[rng.randrange(n)] = 0
        val = w[0] * metrics(r)[0] + w[1] * metrics(r)[1] + w[2] * metrics(r)[2]
        improved = True
        while improved:
            improved = False
            for i in rng.sample(range(n), n):
                for v in (0, 1, 2):
                    if v == r[i]:
                        continue
                    old = r[i]
                    r[i] = v
                    if sum(r) > K:
                        r[i] = old
                        continue
                    nv = w[0] * metrics(r)[0] + w[1] * metrics(r)[1] + w[2] * metrics(r)[2]
                    if nv > val + 1e-12:
                        val = nv
                        improved = True
                    else:
                        r[i] = old
        if val > best_val:
            best_val = val
            best = r[:]
    return best


def pareto(points):
    pts = sorted(set(points), reverse=True)
    front = []
    for p in pts:
        if not any(q[0] >= p[0] and q[1] >= p[1] and q[2] >= p[2] and q != p for q in front):
            front.append(p)
    return front


def run(n, alpha, seed=0):
    rng = random.Random(seed)
    K = int(round(alpha * n))
    pts = []
    # 覆盖各种权重方向，收集 Pareto 点
    weights = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1),
               (1, 1, 1), (2, 1, 1), (1, 2, 1), (1, 1, 2), (3, 1, 2), (2, 1, 3)]
    for w in weights:
        r = hill_climb(n, K, w, rng)
        pts.append(metrics(r))
    front = pareto(pts)
    # 解析构造下界：全部 ≥1（花费 n），把 (K−n) 个改成 2 并聚成一块
    e = max(0, K - n)
    e = min(e, n)
    Cc = e / n
    Ac = 1.0 - (1.0 / (n - 1) if 0 < e < n else 0.0)
    Tc = 1.0 if K >= n else 0.0
    return {
        "n": n, "K": K, "alpha": alpha,
        "max_sum_found": max(sum(p) for p in pts),
        "max_sum_constructive": Cc + Ac + Tc,
        "frontier": [list(p) for p in front],
    }


def build_svg(rows):
    W, H = 1000, 640
    b = [f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    b.append('<text x="40" y="46" font-size="25" font-weight="700">'
             '图 2.2　前沿如何随规模变化（说明性模型 T）</text>')
    b.append('<text x="40" y="76" font-size="15" fill="#666">'
             '固定预算比 α = K/n，横轴为 n，纵轴为可达到的坐标和上界 C+A+T</text>')
    # 坐标轴
    x0, x1, y0, y1 = 90, 940, 560, 110
    b.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="#333" stroke-width="1.4"/>')
    b.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="#333" stroke-width="1.4"/>')
    for val in (2.0, 2.5, 3.0):
        yy = y0 - (val - 1.5) / 1.6 * (y0 - y1)
        b.append(f'<line x1="{x0}" y1="{yy:.0f}" x2="{x1}" y2="{yy:.0f}" stroke="#eee"/>')
        b.append(f'<text x="{x0-8}" y="{yy+5:.0f}" text-anchor="end" font-size="13" fill="#666">{val:g}</text>')
    ns = [r["n"] for r in rows]
    nmin, nmax = min(ns), max(ns)

    def X(n):
        return x0 + (n - nmin) / max(1, nmax - nmin) * (x1 - x0)

    def Y(v):
        return y0 - (v - 1.5) / 1.6 * (y0 - y1)

    for alpha, col in [(1.5, "#3a6ea5"), (1.8, "#009E73")]:
        sub = [r for r in rows if abs(r["alpha"] - alpha) < 1e-9]
        if not sub:
            continue
        pts = " ".join(f"{X(r['n']):.1f},{Y(r['max_sum_found']):.1f}" for r in sorted(sub, key=lambda z: z["n"]))
        b.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.4"/>')
        for r in sub:
            b.append(f'<circle cx="{X(r["n"]):.1f}" cy="{Y(r["max_sum_found"]):.1f}" r="4" fill="{col}"/>')
        b.append(f'<text x="{X(sub[-1]["n"])-6:.0f}" y="{Y(sub[-1]["max_sum_found"])-12:.0f}" '
                 f'text-anchor="end" font-size="15" fill="{col}">α={alpha}</text>')
    b.append(f'<text x="{(x0+x1)//2}" y="{y0+46}" text-anchor="middle" font-size="15" fill="#333">系统规模 n（对数刻度近似）</text>')
    b.append(f'<text x="20" y="{(y0+y1)//2}" font-size="15" fill="#333" transform="rotate(-90 20 {(y0+y1)//2})" text-anchor="middle">坐标和上界</text>')
    b.append('<text x="40" y="612" font-size="13" fill="#888">'
             '结论：固定预算比下，坐标和上界随 n 增大而上升；模型 T 的三选二是有限规模 + 紧预算现象。'
             '复现：python analysis/frontier_scaling.py</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">'
            '<style>text{font-family:"Microsoft YaHei","SimHei",Arial,sans-serif;}</style>'
            + "\n".join(b) + "</svg>")


def main():
    rows = []
    for alpha in (1.5, 1.8):
        for n in (12, 20, 30, 50, 100, 200):
            rows.append(run(n, alpha, seed=n + int(alpha * 100)))
    os.makedirs(os.path.dirname(RESULT), exist_ok=True)
    with open(RESULT, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    with open(SVG, "w", encoding="utf-8") as f:
        f.write(build_svg(rows))
    for r in rows:
        print(f"n={r['n']:>3} a={r['alpha']} max_sum={r['max_sum_found']:.3f} "
              f"constru={r['max_sum_constructive']:.3f}")
    print("wrote", RESULT)
    print("wrote", SVG)


if __name__ == "__main__":
    main()
