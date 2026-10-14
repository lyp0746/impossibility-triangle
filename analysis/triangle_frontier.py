# -*- coding: utf-8 -*-
"""triangle_frontier.py — 《选择的代价》说明性模型 T 的精确枚举。

模型（说明性，非定理；C／丙）
------------------------------------------------
* ``n`` 个单元排成一条尺度线；每个单元分配分辨率 ``r_i ∈ {0,1,2}``
  （0＝不描述，1＝粗捆绑，2＝精确）。
* 预算约束 ``Σ r_i ≤ K``（精确描述比粗描述贵一倍）。
* 完备性   C = #{i: r_i = 2} / n          （有多少单元被精确描述）
* 可组合性 A = 1 − #{相邻对 (i,i+1): r_i ≠ r_{i+1}} / (n−1)   （均匀度）
* 传递性   T = #{相邻对 (i,i+1): r_i ≥ 1 且 r_{i+1} ≥ 1} / (n−1)  （连续覆盖）

对全部分配做精确枚举，报告可达域与三种"选两个"的极值。
本脚本只展示三角的结构，不承担任何经验预测。
"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT = os.path.join(HERE, "analysis", "results", "triangle_frontier.json")
SVG = os.path.join(HERE, "assets", "svg", "fig00-triangle-frontier.svg")


def metrics(r):
    n = len(r)
    C = sum(1 for x in r if x == 2) / n
    A = (1.0 - sum(1 for i in range(n - 1) if r[i] != r[i + 1]) / (n - 1)) if n > 1 else 1.0
    T = (sum(1 for i in range(n - 1) if r[i] >= 1 and r[i + 1] >= 1) / (n - 1)) if n > 1 else 0.0
    return C, A, T


def enumerate_points(n, k):
    return [metrics(v) for v in itertools.product((0, 1, 2), repeat=n) if sum(v) <= k]


def pareto3(pts):
    pts = sorted(set(pts), reverse=True)
    front = []
    for p in pts:
        if not any(q[0] >= p[0] and q[1] >= p[1] and q[2] >= p[2] and q != p for q in front):
            front.append(p)
    return front


def max_third(pts, i, j, thresh):
    rest = [k for k in (0, 1, 2) if k not in (i, j)][0]
    cand = [p for p in pts if p[i] >= thresh and p[j] >= thresh]
    if not cand:
        return None
    return max(p[rest] for p in cand)


def analyse(n=12, k=15):
    pts = enumerate_points(n, k)
    return {
        "n": n, "K": k, "num_allocations": len(pts),
        "max_C": max(p[0] for p in pts),
        "max_A": max(p[1] for p in pts),
        "max_T": max(p[2] for p in pts),
        "sum_max": max(sum(p) for p in pts),
        "T_when_C_A_half": max_third(pts, 0, 1, 0.5),
        "C_when_A_T_half": max_third(pts, 1, 2, 0.5),
        "A_when_C_T_half": max_third(pts, 0, 2, 0.5),
        "C_when_A_T_one": max_third(pts, 1, 2, 0.999),
        "pareto_size": len(pareto3(pts)),
    }, pts


def build_svg(res, pts):
    W, H = 1000, 780
    Cx, Cy = 500, 130
    Ax, Ay = 140, 630
    Tx, Ty = 860, 630

    def xy(c, a, t):
        tot = c + a + t
        if tot <= 0:
            return 500, 690
        c, a, t = c / tot, a / tot, t / tot
        return c * Cx + a * Ax + t * Tx, c * Cy + a * Ay + t * Ty

    body = [f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    body.append('<text x="40" y="50" font-size="26" font-weight="700">'
                '图 0.1　三角的可达前沿（说明性模型 T）</text>')
    body.append(f'<text x="40" y="82" font-size="15" fill="#666">'
                f'n={res["n"]}, K={res["K"]}，精确枚举 {res["num_allocations"]} 种分配；'
                '深蓝＝全部可达点，金色＝Pareto 前沿</text>')
    for (x1, y1), (x2, y2) in [((Cx, Cy), (Ax, Ay)), ((Ax, Ay), (Tx, Ty)), ((Tx, Ty), (Cx, Cy))]:
        body.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#bbb" stroke-width="1.5"/>')
    body.append(f'<text x="{Cx}" y="{Cy-18}" text-anchor="middle" font-size="18" fill="#3a6ea5" font-weight="700">C 完备</text>')
    body.append(f'<text x="{Ax-10}" y="{Ay+30}" text-anchor="middle" font-size="18" fill="#009E73" font-weight="700">A 可组合</text>')
    body.append(f'<text x="{Tx+10}" y="{Ty+30}" text-anchor="middle" font-size="18" fill="#c94f4f" font-weight="700">T 传递</text>')
    for c, a, t in pts[:: max(1, len(pts) // 1500)]:
        X, Y = xy(c, a, t)
        body.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="2.0" fill="#3a6ea5" '
                    f'opacity="{0.04 + 0.28 * (c + a + t) / 3:.2f}"/>')
    front = pareto3(pts)
    for c, a, t in front[:: max(1, len(front) // 200)]:
        X, Y = xy(c, a, t)
        body.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="4.0" fill="#b8862f" '
                    'stroke="#7a5a1a" stroke-width="0.8"/>')

    def f(v):
        return "无（不可达）" if v is None else f"{v:.2f}"

    lines = [
        f"max C = {res['max_C']:.2f}，max A = {res['max_A']:.2f}，max T = {res['max_T']:.2f}",
        f"C≥0.5 且 A≥0.5 ⇒ T ≤ {f(res['T_when_C_A_half'])}",
        f"A≥0.5 且 T≥0.5 ⇒ C ≤ {f(res['C_when_A_T_half'])}",
        f"C≥0.5 且 T≥0.5 ⇒ A ≤ {f(res['A_when_C_T_half'])}",
        f"A=1 且 T=1 ⇒ C = {f(res['C_when_A_T_one'])}",
        f"坐标和上界 ≈ {res['sum_max']:.2f}（粗化三角：≤2）",
    ]
    for k, line in enumerate(lines):
        col = "#333" if k in (0, 5) else "#8a6a1a"
        body.append(f'<text x="40" y="{150 + k*30}" font-size="16" fill="{col}">{line}</text>')
    body.append('<text x="40" y="750" font-size="13" fill="#888">'
                '模型为说明性构造，不是对现实系统的测量。复现：python analysis/triangle_frontier.py</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">'
            '<style>text{font-family:"Microsoft YaHei","SimHei",Arial,sans-serif;}</style>'
            + "\n".join(body) + "</svg>")


def main():
    n, k = 12, 15
    for i, a in enumerate(sys.argv):
        if a == "--n" and i + 1 < len(sys.argv):
            n = int(sys.argv[i + 1])
        if a == "--k" and i + 1 < len(sys.argv):
            k = int(sys.argv[i + 1])
    res, pts = analyse(n, k)
    print(f"n={n} K={k} allocations={res['num_allocations']}")
    print("max C,A,T =", round(res["max_C"], 3), round(res["max_A"], 3), round(res["max_T"], 3))
    print("C>=.5 & A>=.5 -> max T =", res["T_when_C_A_half"])
    print("A>=.5 & T>=.5 -> max C =", res["C_when_A_T_half"])
    print("C>=.5 & T>=.5 -> max A =", res["A_when_C_T_half"])
    print("A=1 & T=1 -> C =", res["C_when_A_T_one"])
    print("max sum =", round(res["sum_max"], 3), "pareto =", res["pareto_size"])
    os.makedirs(os.path.dirname(RESULT), exist_ok=True)
    with open(RESULT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=2)
    with open(SVG, "w", encoding="utf-8") as fh:
        fh.write(build_svg(res, pts))
    print("wrote", RESULT)
    print("wrote", SVG)


if __name__ == "__main__":
    main()
