# -*- coding: utf-8 -*-
"""make_cover.py — 生成《选择的代价》满版封面 SVG（A4 比例 1000×1414）。

系列统一版式：暗色渐变、顶部金线、同一标题/副标题/作者/英文行的位置与字号；
中心线描母题因书而异——本书为"不可能三角"。
"""
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "assets", "svg", "cover.svg")


def build():
    W, H = 1000, 1414
    ink = "#e8e6df"
    dim = "#9aa0a6"
    layers = []
    # 三角母题：三个顶点 + 内部层次线
    cx, cy = 500, 600
    R = 250
    import math
    verts = {
        "C": (cx + R * math.cos(math.radians(-90)), cy + R * math.sin(math.radians(-90))),
        "A": (cx + R * math.cos(math.radians(150)), cy + R * math.sin(math.radians(150))),
        "T": (cx + R * math.cos(math.radians(30)), cy + R * math.sin(math.radians(30))),
    }
    cols = {"C": "#3a6ea5", "A": "#009E73", "T": "#b8862f"}
    # 同心缩放三角
    for k in range(1, 7):
        s = k / 7
        pts = []
        for key in ("C", "A", "T"):
            x, y = verts[key]
            pts.append(f"{cx + (x-cx)*s:.1f},{cy + (y-cy)*s:.1f}")
        op = 0.10 + 0.06 * k
        layers.append(f'<polygon points="{" ".join(pts)}" fill="none" '
                      f'stroke="#8fa0b5" stroke-width="1" opacity="{min(op,0.35):.2f}"/>')
    # 三顶点
    for key, (x, y) in verts.items():
        layers.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{cols[key]}" opacity="0.9"/>')
    # 三条边（虚线，表示取舍）
    for a, b in (("C", "A"), ("A", "T"), ("T", "C")):
        (x1, y1), (x2, y2) = verts[a], verts[b]
        layers.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                      f'stroke="#c9c9c9" stroke-width="1.6" opacity="0.55" stroke-dasharray="7,6"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#0e1117"/><stop offset="0.55" stop-color="#151a23"/>
<stop offset="1" stop-color="#0b0e14"/>
</linearGradient>
</defs>
<rect x="0" y="0" width="{W}" height="{H}" fill="url(#bg)"/>
<rect x="0" y="0" width="{W}" height="8" fill="#b8862f" opacity="0.85"/>
{chr(10).join(layers)}
<style>
text{{font-family:'Microsoft YaHei','SimHei',Arial,sans-serif;}}
.ttl{{font-size:108px;font-weight:700;letter-spacing:12px;fill:{ink};}}
.sub{{font-size:27px;fill:{dim};letter-spacing:2px;}}
.eng{{font-size:21px;fill:{dim};letter-spacing:1px;}}
.au{{font-size:30px;fill:{ink};letter-spacing:2px;}}
.rule{{stroke:{dim};stroke-width:1;opacity:0.6;}}
.lab{{font-size:24px;font-weight:700;}}
</style>
<text x="80" y="176" class="eng">THE PRICE OF CHOICE</text>
<text x="80" y="300" class="ttl">选择的代价</text>
<line x1="84" y1="344" x2="700" y2="344" class="rule"/>
<text x="84" y="396" class="sub">完备、可组合与可传递的三维权衡</text>
<text x="84" y="440" class="sub">——复杂知识系统如何形成、演化与更新</text>
<text x="{verts['C'][0]-14:.0f}" y="{verts['C'][1]-22:.0f}" class="lab" fill="{cols['C']}" text-anchor="middle">C</text>
<text x="{verts['A'][0]-24:.0f}" y="{verts['A'][1]+34:.0f}" class="lab" fill="{cols['A']}" text-anchor="middle">A</text>
<text x="{verts['T'][0]+24:.0f}" y="{verts['T'][1]+34:.0f}" class="lab" fill="{cols['T']}" text-anchor="middle">T</text>
<text x="80" y="1180" class="au">李毅芃　著</text>
<text x="80" y="1232" class="eng">The Impossibility Triangle: Completeness, Composability, Transfer</text>
<text x="80" y="1274" class="eng">跨学科理论专著 · 2026</text>
</svg>
'''
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", OUT)


if __name__ == "__main__":
    build()
