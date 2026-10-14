# -*- coding: utf-8 -*-
"""make_figures.py — 《选择的代价》正文插图（系列统一配色与字体）。

输出：assets/svg/fig01-triangle.svg, fig02-layers.svg, fig03-growth-cycle.svg
（fig00-triangle-frontier.svg 由 analysis/triangle_frontier.py 生成。）
"""
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "assets", "svg")

BLUE, RED, GOLD, GREEN, GREY = "#3a6ea5", "#c94f4f", "#b8862f", "#009E73", "#666"
INK = "#1a1a1a"
FONT = "'Microsoft YaHei','SimHei',Arial,sans-serif"
SERIF = "'Times New Roman',Georgia,serif"


def wrap(w, h, body, bg="#ffffff"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>'
            f'<style>text{{font-family:{FONT};fill:{INK};}}'
            f'.s{{font-family:{SERIF};}}</style>'
            f'{body}</svg>')


def box(x, y, w, h, label, sub="", color=BLUE, fc="#ffffff", fs=22):
    body = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" '
            f'fill="{fc}" stroke="{color}" stroke-width="2"/>'
            f'<text x="{x + w/2}" y="{y + h/2 - (8 if sub else -8)}" text-anchor="middle" '
            f'font-size="{fs}" font-weight="600" fill="{color}">{label}</text>')
    if sub:
        body += (f'<text x="{x + w/2}" y="{y + h/2 + 20}" text-anchor="middle" '
                 f'font-size="15" fill="{GREY}">{sub}</text>')
    return body


def fig_triangle():
    W, H = 1000, 620
    Cx, Cy, Ax, Ay, Tx, Ty = 500, 90, 130, 540, 870, 540
    b = []
    b.append('<text x="40" y="46" font-size="24" font-weight="700">图 2.1　不可能三角：三个顶点与三个缺口</text>')
    for (x1, y1), (x2, y2) in [((Cx, Cy), (Ax, Ay)), ((Ax, Ay), (Tx, Ty)), ((Tx, Ty), (Cx, Cy))]:
        b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#c9c9c9" stroke-width="2"/>')
    b.append(box(Cx - 90, Cy - 62, 180, 70, "C 完备", "局部说得清", BLUE, "#eef3f8", 20))
    b.append(box(Ax - 20, Ay - 8, 180, 70, "A 可组合", "拼得回去", GREEN, "#eefaf4", 20))
    b.append(box(Tx - 160, Ty - 8, 180, 70, "T 传递", "跨得过去", GOLD, "#fbf6ec", 20))
    # 顶点对面缺口标注
    b.append(f'<text x="500" y="360" text-anchor="middle" font-size="17" fill="{BLUE}">'
             '选 C+T ⇒ 让出 A：能力不能相加（子模性）</text>')
    b.append(f'<text x="230" y="470" text-anchor="middle" font-size="17" fill="{GREEN}">'
             '选 C+A ⇒ 让出 T：1/3 缺口</text>')
    b.append(f'<text x="770" y="470" text-anchor="middle" font-size="17" fill="{GOLD}">'
             '选 A+T ⇒ 让出 C：τ 发散</text>')
    b.append('<text x="40" y="596" font-size="14" fill="#888">组织坐标图，不是可行域的精确形状。三本书分别位于三个顶点。</text>')
    return wrap(W, H, "\n".join(b))


def fig_layers():
    W, H = 1000, 520
    b = []
    b.append('<text x="40" y="46" font-size="24" font-weight="700">图 3.1　三层结构与各自的证伪方式</text>')
    layers = [
        (80, "硬核层 A", "信息子模性 · 离散曲率恒等式 · 模型 T", GREEN, "反例 / 复算失败"),
        (210, "诊断框架层 B", "三角命题 · 四战场诊断 · 三阶段模式", BLUE, "领域反例"),
        (340, "可选工具层 C", "诊断手册 · 制度模板 · 降级清单", GOLD, "不好用（不承载真值）"),
    ]
    for y, name, sub, col, how in layers:
        b.append(box(70, y, 560, 100, name, sub, col))
        b.append(f'<text x="650" y="{y+42}" font-size="15" fill="{GREY}">证伪方式：</text>')
        b.append(f'<text x="650" y="{y+70}" font-size="16" fill="{INK}">{how}</text>')
    for y0, y1 in [(180, 210), (310, 340)]:
        b.append(f'<line x1="350" y1="{y0}" x2="350" y2="{y1}" stroke="{RED}" stroke-width="2.4"/>')
    b.append(f'<text x="70" y="490" font-size="15" fill="{GREY}">三层之间只有单向依赖：读者可只接受其中一层。</text>')
    return wrap(W, H, "\n".join(b))


def fig_growth():
    W, H = 1000, 640
    b = []
    b.append('<text x="40" y="46" font-size="24" font-weight="700">图 11.1　三阶段成长与危机：连续换顶点</text>')
    stages = [
        ("范式建立", "C + T", BLUE, "难教学、依赖个人"),
        ("教学化", "A + T", GREEN, "丢失精妙与边界"),
        ("工程化", "C + A", GOLD, "失去“为什么”"),
    ]
    x = 70
    for i, (name, sel, col, cost) in enumerate(stages):
        b.append(box(x, 150, 250, 110, name, sel, col, "#ffffff", 22))
        b.append(f'<text x="{x+125}" y="300" text-anchor="middle" font-size="15" fill="{GREY}">代价：{cost}</text>')
        if i < 2:
            b.append(f'<line x1="{x+255}" y1="205" x2="{x+320}" y2="205" stroke="{RED}" '
                     'stroke-width="3" marker-end="url(#ar)"/>')
        x += 330
    # 危机回路
    b.append(f'<path d="M 900 205 C 960 205 960 470 500 470 C 250 470 195 470 195 300" '
             f'fill="none" stroke="{RED}" stroke-width="2.6" stroke-dasharray="8,6" marker-end="url(#ar)"/>')
    b.append(f'<text x="560" y="456" text-anchor="middle" font-size="17" fill="{RED}" font-weight="600">'
             '危机：旧三边碎裂 → 重返 C+T</text>')
    b.append('<text x="40" y="540" font-size="15" fill="#888">'
             '箭头表示“被让出的顶点的转移”，不是水平提高。此模式是组织方式，不是历史定律。</text>')
    b.append(f'<defs><marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="3" '
             f'orient="auto"><path d="M0,0 L8,3 L0,6 z" fill="{RED}"/></marker></defs>')
    return wrap(W, H, "\n".join(b))


def main():
    figs = {
        "fig01-triangle.svg": fig_triangle(),
        "fig02-layers.svg": fig_layers(),
        "fig03-growth-cycle.svg": fig_growth(),
    }
    os.makedirs(OUT, exist_ok=True)
    for name, svg in figs.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(svg)
        print("wrote", name)


if __name__ == "__main__":
    main()
