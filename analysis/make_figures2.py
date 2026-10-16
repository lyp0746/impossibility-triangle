# -*- coding: utf-8 -*-
"""make_figures2.py — 《选择的代价》第二批插图（正文各章配图）。

统一 house style（与 make_figures.py 一致）：蓝 C / 绿 A / 金 T、微软雅黑标题。
输出到 assets/svg/。所有图形确定性生成、可复现。
"""
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "assets", "svg")

BLUE, GREEN, GOLD, RED, GREY, INK = "#3a6ea5", "#009E73", "#b8862f", "#c94f4f", "#666", "#1a1a1a"
FONT = "'Microsoft YaHei','SimHei',Arial,sans-serif"


def wrap(w, h, body, bg="#ffffff"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>'
            f'<style>text{{font-family:{FONT};fill:{INK};}}</style>'
            f'<defs><marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="3" '
            f'orient="auto"><path d="M0,0 L8,3 L0,6 z" fill="{GREY}"/></marker></defs>'
            f'{body}</svg>')


def T(x, y, s, size=16, color=INK, anchor="start", weight="normal"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{s}</text>')


def box(x, y, w, h, label, sub="", color=BLUE, fill="#ffffff", fs=18):
    b = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" '
         f'stroke="{color}" stroke-width="2"/>'
         f'{T(x + w/2, y + h/2 - (6 if sub else -6), label, fs, color, "middle", "600")}')
    if sub:
        b += T(x + w/2, y + h/2 + 20, sub, 13, GREY, "middle")
    return b


def arrow(x1, y1, x2, y2, color=GREY, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="2" marker-end="url(#ar)"{d}/>')


def title(s, w=1000):
    return T(40, 46, s, 24, INK, "start", "700")


# ---------------------------------------------------------------- 背景
def fig_three_systems():
    W, H = 1000, 560
    b = [title("图 0.2　三个系统 → 一个坐标")]
    data = [("记忆系统", "《遗忘的边界》", "容量级联", BLUE, "保住 C+T", "让出 A"),
            ("区分结构", "《区分的语法》", "1/3 缺口", GREEN, "保住 C+A", "让出 T"),
            ("社会时间", "《错位的时间》", "τ 错配", GOLD, "保住 A+T", "让出 C")]
    for i, (name, book, core, col, keep, miss) in enumerate(data):
        y = 100 + i * 130
        b.append(box(60, y, 250, 90, name, book, col, "#f7f9fc", 20))
        b.append(T(340, y + 52, core, 16, col, "start", "600"))
        b.append(T(500, y + 52, keep, 15, GREY))
        b.append(T(680, y + 52, miss, 15, RED, "start", "600"))
    b.append(arrow(330, 280, 500, 280))
    b.append(box(560, 200, 380, 160, "C-A-T 坐标", "完备 / 可组合 / 传递", INK, "#f4f4f2", 22))
    b.append(T(40, H - 24, "三个系统各自把 A、T、C 逼到极限，账单形状相同。", 13, GREY))
    return wrap(W, H, "\n".join(b))


def fig_cta_definition():
    W, H = 1000, 620
    b = [title("图 0.3　C-A-T 的精确定义")]
    cols = [(BLUE, "C 完备", ["C₁ 描述完备", "C₂ 计算完备", "C₃ 预测完备"]),
            (GREEN, "A 可组合", ["A₁ 线性可组合", "A₂ 关系可组合", "A₃ 代数可组合"]),
            (GOLD, "T 传递", ["T₁ 尺度传递", "T₂ 时间传递", "T₃ 因果传递"])]
    for j, (col, name, tiers) in enumerate(cols):
        x = 80 + j * 300
        b.append(box(x, 100, 240, 70, name, "", col, "#f7f9fc", 22))
        for k, tier in enumerate(tiers):
            b.append(box(x, 200 + k * 80, 240, 60, tier, "", col, "#ffffff", 15))
    # 底部三顶点
    for j, (col, name, _) in enumerate(cols):
        b.append(arrow(200 + j * 300, 450, 200 + j * 300, 470, col))
    b.append(T(500, 530, "记忆 = C+T　|　区分 = C+A　|　社会时间 = A+T", 17, INK, "middle", "600"))
    b.append(T(500, 570, "三者的让出分别是 A、T、C", 14, RED, "middle"))
    return wrap(W, H, "\n".join(b))


def fig_journey():
    W, H = 1000, 300
    b = [title("图 1.1　全书的路：症状 → 三角 → 诊断 → 课题 → 设计")]
    steps = ["症状", "三角", "诊断", "课题", "设计"]
    subs = ["三本书的卡点", "C-A-T 坐标", "四个战场", "形成·演化·更新", "分层与降级"]
    cols = [RED, INK, BLUE, GREEN, GOLD]
    for i, (s, sub, c) in enumerate(zip(steps, subs, cols)):
        x = 60 + i * 185
        b.append(box(x, 110, 150, 90, s, sub, c, "#f7f9fc", 20))
        if i < 4:
            b.append(arrow(x + 150, 155, x + 180, 155, GREY))
    return wrap(W, H, "\n".join(b))


# ---------------------------------------------------------------- 第一部分
def fig_impossibility_family():
    W, H = 1000, 560
    b = [title("图 4.1　不可能定理的家族")]
    items = [("CAP", "一致性/可用性/分区容忍", BLUE),
             ("Arrow", "有序/尊重个体/非独裁", GREEN),
             ("Mundell–Fleming", "固定汇率/资本流动/独立货币", GOLD),
             ("无免费午餐", "对所有问题都不劣的算法不存在", RED),
             ("停机问题", "对任意程序判定终止不可计算", GREY)]
    for i, (name, desc, col) in enumerate(items):
        y = 100 + i * 82
        b.append(box(60, y, 260, 62, name, "", col, "#f7f9fc", 18))
        b.append(T(345, y + 38, desc, 15, INK))
    b.append(box(620, 160, 330, 240, "本书三角", "有限的描述能力在\n完备 / 组合 / 传递间分配", INK, "#f4f4f2", 20))
    b.append(T(40, H - 20, "它们共享同一形状：有限资源在若干理想性质之间的取舍。", 13, GREY))
    return wrap(W, H, "\n".join(b))


def fig_computation():
    W, H = 1000, 400
    b = [title("图 4.2　计算论的三条边界与三角")]
    layers = [("可计算性", "停机问题：某些完备在逻辑上不可达", GREY),
              ("计算不可约性", "预测需与模拟等价的 K_comp（¬C₃ 或 ¬T）", BLUE),
              ("P vs NP", "完备刻画与可组合求解之间的鸿沟", GREEN)]
    for i, (name, desc, col) in enumerate(layers):
        y = 100 + i * 90
        b.append(box(60, y, 300, 70, name, "", col, "#f7f9fc", 19))
        b.append(T(390, y + 44, desc, 15, INK))
    b.append(T(40, H - 20, "它们各自固定一个受限分量：逻辑 / K_comp / 计算复杂度。", 13, GREY))
    return wrap(W, H, "\n".join(b))


# ---------------------------------------------------------------- 第二部分
def _timescale(rows, title_s, unit_note=""):
    W, H = 1000, 120 + len(rows) * 74
    b = [title(title_s)]
    import math
    for i, (name, span, col) in enumerate(rows):
        y = 100 + i * 74
        b.append(box(60, y, 220, 56, name, "", col, "#f7f9fc", 17))
        b.append(f'<rect x="300" y="{y+14}" width="{span}" height="28" rx="6" fill="{col}" opacity="0.35"/>')
        b.append(T(300 + span + 12, y + 36, f"≈ {span}×", 14, GREY))
    if unit_note:
        b.append(T(40, H - 16, unit_note, 13, GREY))
    return wrap(W, H, "\n".join(b))


def fig_memory_cascade():
    rows = [("感觉登记", 20, BLUE), ("工作记忆", 60, BLUE), ("短期巩固", 200, GREEN),
            ("长期巩固", 450, GOLD), ("终身整合", 700, RED)]
    return _timescale(rows, "图 5.1　记忆的容量级联（尺度跨度约 10⁹）",
                      "条形长度示意各尺度的时间跨度；同一组信息论约束支配全部尺度。")


def fig_medical_scales():
    rows = [("急症窗口", 30, RED), ("住院/门诊", 120, BLUE), ("慢病随访", 400, GREEN),
            ("公卫/代际", 700, GOLD)]
    return _timescale(rows, "图 6.1　医疗的四个尺度（分钟 → 十年）",
                      "急性窗口以分钟计，慢病结局以十年计；制度若用同一套指标考核两者，必然在一端失真。")


def fig_climate_clocks():
    W, H = 1000, 520
    b = [title("图 7.1　气候的钟与政治的钟（τ = T_min / T_available）")]
    rows = [("金融/市场", 15, RED), ("政治/选举", 80, BLUE), ("基础设施", 350, GREEN),
            ("生态响应", 650, GOLD)]
    for i, (name, span, col) in enumerate(rows):
        y = 100 + i * 80
        b.append(box(60, y, 200, 60, name, "", col, "#f7f9fc", 18))
        b.append(f'<rect x="290" y="{y+16}" width="{span}" height="28" rx="6" fill="{col}" opacity="0.35"/>')
        b.append(T(290 + span + 12, y + 38, f"≈ {span}×", 14, GREY))
    b.append(T(40, H - 20, "不同尺度的钟无法被同一机制协调——这就是 τ ≫ 1 的构成。", 13, GREY))
    return wrap(W, H, "\n".join(b))


def fig_education_tracks():
    W, H = 1000, 420
    b = [title("图 8.1　教育的三条轨道与三角选择")]
    rows = [("快速轨道", "C + T", BLUE, "小班化、个性化追踪"),
            ("标准轨道", "A + T", GREEN, "标准课程、持续评估"),
            ("探索轨道", "C + A", GOLD, "选课制、灵活进度")]
    for i, (name, sel, col, desc) in enumerate(rows):
        y = 100 + i * 90
        b.append(box(60, y, 200, 70, name, "", col, "#f7f9fc", 20))
        b.append(box(300, y, 160, 70, sel, "", col, "#ffffff", 20))
        b.append(T(500, y + 44, desc, 16, INK))
    b.append(T(40, H - 20, "三条轨道并行：承认无法用单一轨道同时满足三种需求。", 13, GREY))
    return wrap(W, H, "\n".join(b))


def fig_democracy_clocks():
    W, H = 1000, 440
    b = [title("图 9.1　治理的三只钟与错配")]
    rows = [("选举周期", 20, RED), ("政策效果", 180, BLUE), ("代际后果", 700, GOLD)]
    for i, (name, span, col) in enumerate(rows):
        y = 100 + i * 80
        b.append(box(60, y, 200, 60, name, "", col, "#f7f9fc", 18))
        b.append(f'<rect x="290" y="{y+16}" width="{span}" height="28" rx="6" fill="{col}" opacity="0.35"/>')
        b.append(T(290 + span + 12, y + 38, f"≈ {span}×", 14, GREY))
    b.append(T(40, H - 20, "问责期 ≪ 政策收益期 ≪ 代际后果——短期主义的结构来源。", 13, GREY))
    return wrap(W, H, "\n".join(b))


def fig_org_lifecycle():
    W, H = 1000, 420
    b = [title("图 10.1　组织的生命周期：连续换顶点")]
    stages = [("初创", "C + T", BLUE, "让出 A"), ("成长", "A + T", GREEN, "让出 C"),
              ("成熟", "C + A", GOLD, "让出 T"), ("危机/重启", "→ C + T", RED, "换顶点")]
    for i, (name, sel, col, cost) in enumerate(stages):
        x = 60 + i * 230
        b.append(box(x, 110, 190, 90, name, sel, col, "#f7f9fc", 20))
        b.append(T(x + 95, 240, cost, 15, RED, "middle", "600"))
        if i < 3:
            b.append(arrow(x + 190, 155, x + 225, 155, GREY))
    b.append(T(40, H - 20, "每一阶段用顶点换成就；成长 = 换掉被让出的顶点。", 13, GREY))
    return wrap(W, H, "\n".join(b))


# ---------------------------------------------------------------- 第三部分
def fig_discipline_fission():
    W, H = 1000, 560
    b = [title("图 12.1　学科分裂 = 三角选择的分裂")]
    groups = [("物理学", [("粒子物理", "C+T"), ("凝聚态", "A+T"), ("计算物理", "C+A")], BLUE),
              ("生物学", [("分子", "C+T"), ("生态", "A+T"), ("医学", "C+A")], GREEN),
              ("经济学", [("微观", "C+A"), ("宏观", "A+T"), ("计量", "C+T")], GOLD)]
    for gi, (name, subs, col) in enumerate(groups):
        x = 60 + gi * 320
        b.append(box(x, 100, 280, 60, name, "", col, "#f7f9fc", 20))
        for k, (s, sel) in enumerate(subs):
            b.append(box(x, 190 + k * 74, 280, 56, s + "  " + sel, "", col, "#ffffff", 15))
    b.append(T(40, H - 20, "各分支站在不同顶点上；它们之间的“无法统一”是各自选择的账单。", 13, GREY))
    return wrap(W, H, "\n".join(b))


def fig_academic_selection():
    W, H = 1000, 440
    b = [title("图 13.1　学术体制的隐性选择与 C+T 飞地")]
    b.append(box(60, 110, 420, 240, "主流：A + T", "可量化、可比较、可管理", BLUE, "#f7f9fc", 22))
    b.append(T(90, 300, "代价：C（深度积累）与 T（长期因果）被压缩", 14, RED))
    b.append(box(560, 110, 380, 240, "C+T 飞地", "长期资助 / 跨学科中心 / 多元发表", GREEN, "#eefaf4", 22))
    b.append(arrow(480, 230, 560, 230, GOLD))
    b.append(T(40, H - 20, "更新 = 在主流之外保留可问责的另一种选择，而非改造主流。", 13, GREY))
    return wrap(W, H, "\n".join(b))


def fig_paradigm_migration():
    W, H = 1000, 460
    b = [title("图 14.1　范式转变 = 三角的整体迁移")]
    stages = [("旧范式", "C + T", BLUE, "牛顿力学 / 生物医学"),
              ("过渡期", "三边碎裂", RED, "异常积累、教学混乱"),
              ("新范式", "C + T'", GREEN, "相对论 / 循证医学"),
              ("稳定期", "A + T", GOLD, "教科书化、再工程化")]
    for i, (name, sel, col, ex) in enumerate(stages):
        x = 60 + i * 230
        b.append(box(x, 110, 190, 90, name, sel, col, "#f7f9fc", 20))
        b.append(T(x + 95, 235, ex, 13, GREY, "middle"))
        if i < 3:
            b.append(arrow(x + 190, 155, x + 225, 155, GREY))
    b.append(T(40, H - 20, "范式转变是整体重选顶点；缓慢源于三个尺度无法同步。", 13, GREY))
    return wrap(W, H, "\n".join(b))


def fig_update_loop():
    W, H = 1000, 420
    b = [title("图 15.1　最小可行更新协议")]
    steps = ["登记\n当前选择", "划出\nC+T 飞地", "跨顶点\n翻译", "周期\n复检", "写入\n组织记忆"]
    cols = [BLUE, GREEN, GOLD, RED, INK]
    for i, (s, c) in enumerate(zip(steps, cols)):
        x = 50 + i * 190
        b.append(box(x, 130, 150, 100, s.replace("\n", " "), "", c, "#f7f9fc", 16))
        if i < 4:
            b.append(arrow(x + 150, 180, x + 185, 180, GREY))
    b.append(f'<path d="M 850 250 C 900 330 500 360 200 300" fill="none" stroke="{GREY}" '
             f'stroke-width="2" stroke-dasharray="7,6" marker-end="url(#ar)"/>')
    b.append(T(500, 340, "只追加、不修改（append-only）", 14, GREY, "middle"))
    return wrap(W, H, "\n".join(b))


# ---------------------------------------------------------------- 第四部分
def fig_layered_validity():
    W, H = 1000, 460
    b = [title("图 16.1　分层有效性：目标决定选择")]
    rows = [("预测", "C + T", BLUE, "天气预报：约 15 天混沌极限"),
            ("解释", "C + A", GREEN, "临床/数学：跨尺度处断开"),
            ("控制", "A + T", GOLD, "公卫：说不准个案")]
    for i, (goal, sel, col, ex) in enumerate(rows):
        y = 100 + i * 100
        b.append(box(60, y, 180, 76, goal, "", col, "#f7f9fc", 22))
        b.append(box(280, y, 160, 76, sel, "", col, "#ffffff", 20))
        b.append(T(480, y + 46, ex, 15, INK))
    b.append(T(40, H - 20, "同时承诺三者满格的方案，必然在某处食言。", 13, GREY))
    return wrap(W, H, "\n".join(b))


def fig_balance_matrix():
    W, H = 1000, 420
    b = [title("图 17.1　权衡矩阵（可填写）")]
    heads = ["系统部分", "主尺度", "保 C", "保 A", "保 T", "被让出", "失效阈值"]
    xs = [60, 240, 360, 440, 520, 620, 760]
    for x, h in zip(xs, heads):
        b.append(T(x + 40, 120, h, 15, INK, "middle", "700"))
    b.append(f'<line x1="60" y1="135" x2="950" y2="135" stroke="#333" stroke-width="1.4"/>')
    example = ["急诊", "分钟", "✓", "", "✓", "A", "标准化难覆盖个体"]
    for x, v in zip(xs, example):
        b.append(T(x + 40, 176, v, 14, GREY, "middle"))
    b.append(f'<line x1="60" y1="196" x2="950" y2="196" stroke="#ddd"/>')
    b.append(T(60, 480 if H > 480 else 360, "能填完这张表 = 做过一次显式选择；填不完 = 还在回避选择。", 14, GREY))
    return wrap(W, H, "\n".join(b))


def fig_degradation():
    W, H = 1000, 420
    b = [title("图 18.1　优雅降级：预设触发器与顺序")]
    levels = [("正常", "C + T", GREEN), ("降级 1", "A + T", GOLD), ("降级 2", "A", RED)]
    for i, (name, sel, col) in enumerate(levels):
        y = 110 + i * 95
        b.append(box(60, y, 200, 70, name, sel, col, "#f7f9fc", 20))
        if i < 2:
            b.append(arrow(260, y + 35, 330, y + 90, GREY))
            b.append(T(340, y + 70, "触发器 + 最低服务水平", 13, GREY))
    b.append(T(40, H - 20, "失效是被排练过的动作，而不是临场惊慌。", 13, GREY))
    return wrap(W, H, "\n".join(b))


def fig_playbook():
    W, H = 1000, 300
    b = [title("图 20.1　五步诊断手册")]
    steps = ["识别尺度", "定位顶点", "估计阈值", "设计降级", "登记复检"]
    cols = [BLUE, GREEN, GOLD, RED, INK]
    for i, (s, c) in enumerate(zip(steps, cols)):
        x = 60 + i * 185
        b.append(box(x, 120, 150, 80, s, "", c, "#f7f9fc", 16))
        if i < 4:
            b.append(arrow(x + 150, 160, x + 180, 160, GREY))
    return wrap(W, H, "\n".join(b))


# ---------------------------------------------------------------- 第五部分
def fig_evidence_status():
    W, H = 1000, 400
    b = [title("图 21.1　证据状态分层")]
    layers = [("已严格证明（A）", "子模性 · 离散曲率恒等式 · 模型 T", GREEN),
              ("部分严格（B）", "1/3 缺口 · τ 命题 · 四战场诊断", BLUE),
              ("启发式（C）", "三角命题 · 三阶段模式 · 意识读法", GOLD)]
    for i, (name, ex, col) in enumerate(layers):
        y = 100 + i * 90
        b.append(box(60, y, 380, 70, name, "", col, "#f7f9fc", 19))
        b.append(T(470, y + 44, ex, 15, INK))
    return wrap(W, H, "\n".join(b))


def fig_beyond_triangle():
    W, H = 1000, 460
    b = [title("图 22.1　三角之外：27 格空间与三条超越路线")]
    routes = [("路线 A　换坐标", "寻找使取舍成为线性约束的坐标", BLUE),
              ("路线 B　加维度", "是否存在第四个独立性质", GREEN),
              ("路线 C　动态化", "把选择当作演化变量", GOLD)]
    for i, (name, desc, col) in enumerate(routes):
        y = 100 + i * 90
        b.append(box(60, y, 280, 70, name, "", col, "#f7f9fc", 18))
        b.append(T(370, y + 44, desc, 15, INK))
    b.append(box(620, 130, 330, 240, "27 格", "3 档 × 3 性质", INK, "#f4f4f2", 22))
    return wrap(W, H, "\n".join(b))



def fig_ml_timeline():
    W, H = 1000, 520
    b = [title("图 11.2　机器学习的三阶段：带时间坐标")]
    x0, x1 = 120, 940
    def X(year):
        return x0 + (year - 1980) / (2026 - 1980) * (x1 - x0)
    # 时间轴
    b.append(f'<line x1="{x0}" y1="470" x2="{x1}" y2="470" stroke="#333" stroke-width="1.5"/>')
    for yr in (1980, 1990, 2000, 2012, 2020, 2026):
        b.append(f'<line x1="{X(yr):.0f}" y1="464" x2="{X(yr):.0f}" y2="476" stroke="#333"/>')
        b.append(T(X(yr), 498, str(yr), 13, GREY, "middle"))
    rows = [("C+T 范式", 1986, 1995, BLUE, "反向传播"),
            ("A+T 教学", 1995, 2012, GREEN, "基准与课程"),
            ("C+A 工程", 2012, 2024, GOLD, "预训练产业化"),
            ("危机征兆", 2023, 2026, RED, "位置偏差/评估")]
    for i, (name, a, bb, col, note) in enumerate(rows):
        y = 100 + i * 88
        b.append(box(60, y - 24, 0, 0, "")) if False else None
        b.append(f'<rect x="{X(a):.0f}" y="{y}" width="{X(bb)-X(a):.0f}" height="46" rx="8" '
                 f'fill="{col}" opacity="0.30" stroke="{col}"/>')
        b.append(T(60, y + 30, name, 16, col, "start", "600"))
        b.append(T((X(a)+X(bb))/2, y + 30, note, 13, INK, "middle"))
    b.append(T(X(2012), 70, "▲2012 AlexNet", 13, RED, "middle"))
    b.append(T(X(2017), 70, "▲2017 Transformer", 13, RED, "middle"))
    return wrap(W, H, "\n".join(b))


def fig_math_unification():
    W, H = 1000, 560
    b = [title("图 12.2　数学统一的代价：C+A 强，T 被让出")]
    Cx, Cy, Ax, Ay, Tx, Ty = 500, 90, 130, 540, 870, 540
    for (x1, y1), (x2, y2) in [((Cx, Cy), (Ax, Ay)), ((Ax, Ay), (Tx, Ty)), ((Tx, Ty), (Cx, Cy))]:
        b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#c9c9c9" stroke-width="2"/>')
    b.append(box(Cx - 90, Cy - 62, 180, 70, "C 完备", "深层结构精确", BLUE, "#eef3f8", 18))
    b.append(box(Ax - 10, Ay - 8, 180, 70, "A 可组合", "领域间可翻译", GREEN, "#eefaf4", 18))
    b.append(box(Tx - 170, Ty - 8, 180, 70, "T 传递", "几乎无人能懂", RED, "#fdeeee", 18))
    b.append(T(500, 360, "朗兰兹纲领 / 凝聚态数学：选 C+A，让出 T", 18, INK, "middle", "600"))
    b.append(T(500, 400, "统一 ≠ 简化；它牺牲传递性，换取更高层的完备与可组合", 15, GREY, "middle"))
    b.append(T(40, H - 20, "对《区分的语法》的反思：让数学整体变简单，撞上的是同一堵墙。", 13, GREY))
    return wrap(W, H, "\n".join(b))


def fig_conflict_migration():
    W, H = 1000, 600
    b = [title("图 2.3　冲突迁移：知识进步把取舍推到另一条边")]
    Cx, Cy, Ax, Ay, Tx, Ty = 500, 90, 130, 540, 870, 540
    for (x1, y1), (x2, y2) in [((Cx, Cy), (Ax, Ay)), ((Ax, Ay), (Tx, Ty)), ((Tx, Ty), (Cx, Cy))]:
        b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#dcdcdc" stroke-width="2"/>')
    b.append(T(Cx, Cy - 18, "C 完备", 18, BLUE, "middle", "700"))
    b.append(T(Ax, Ay + 26, "A 可组合", 18, GREEN, "middle", "700"))
    b.append(T(Tx, Ty + 26, "T 传递", 18, GOLD, "middle", "700"))
    # 边中点
    ca = ((Cx+Ax)/2, (Cy+Ay)/2); ta = ((Tx+Ax)/2, (Ty+Ay)/2); ct = ((Cx+Tx)/2, (Cy+Ty)/2)
    b.append(f'<circle cx="{ca[0]:.0f}" cy="{ca[1]:.0f}" r="10" fill="{GREEN}" opacity="0.5"/>')
    b.append(T(ca[0]-16, ca[1]-18, "冲突 1：C–A", 15, GREEN, "end", "600"))
    b.append(T(ca[0]-16, ca[1]+6, "个体异质 → 难编码", 13, GREY, "end"))
    b.append(f'<path d="M {ca[0]+20:.0f} {ca[1]:.0f} Q 500 360 {ta[0]:.0f} {ta[1]:.0f}" '
             f'fill="none" stroke="{RED}" stroke-width="2.6" stroke-dasharray="8,6" marker-end="url(#ar)"/>')
    b.append(T(500, 350, "知识进步（如代谢组学）", 15, RED, "middle", "600"))
    b.append(f'<circle cx="{ta[0]:.0f}" cy="{ta[1]:.0f}" r="10" fill="{RED}" opacity="0.5"/>')
    b.append(T(ta[0]+4, ta[1]-18, "冲突 2：A–T", 15, RED, "start", "600"))
    b.append(T(ta[0]+4, ta[1]+6, "个体化知识 → 难复制", 13, GREY, "start"))
    b.append(T(40, H - 20, "结论：知识进步把冲突从一条边推到另一条边，但不把它从系统中移除（除非扩大 K）。", 13, GREY))
    return wrap(W, H, "\n".join(b))


def fig_framework_self():
    W, H = 1000, 560
    b = [title("图 23.2　把三角用到框架自身")]
    Cx, Cy, Ax, Ay, Tx, Ty = 500, 90, 130, 540, 870, 540
    for (x1, y1), (x2, y2) in [((Cx, Cy), (Ax, Ay)), ((Ax, Ay), (Tx, Ty)), ((Tx, Ty), (Cx, Cy))]:
        b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#c9c9c9" stroke-width="2"/>')
    b.append(box(Cx - 110, Cy - 60, 220, 70, "C 覆盖广", "医疗/教育/组织/数学", BLUE, "#eef3f8", 17))
    b.append(box(Ax - 20, Ay - 8, 200, 70, "A 可跨域套用", "模块化诊断", GREEN, "#eefaf4", 17))
    b.append(box(Tx - 180, Ty - 8, 200, 70, "T 实践传递弱", "需工具补偿", RED, "#fdeeee", 17))
    b.append(T(500, 370, "本书选择 C+A：给覆盖与诚实，让出实践传递", 18, INK, "middle", "600"))
    b.append(T(500, 408, "这就是为什么它附带诊断手册、制度模板与案例数据库", 15, GREY, "middle"))
    b.append(T(40, H - 20, "自反一致性：框架对自己用了同一把尺子，没有豁免在外。", 13, GREY))
    return wrap(W, H, "\n".join(b))


def fig_reflexivity():
    W, H = 1000, 480
    b = [title("图 U.1　诊断的反身循环：观察者改变系统")]
    b.append(box(80, 150, 250, 90, "框架 / 观察者", "区分：C-A-T", BLUE, "#eef3f8", 18))
    b.append(box(670, 150, 250, 90, "被诊断系统", "行为与配置", GREEN, "#eefaf4", 18))
    b.append(arrow(330, 175, 670, 175, GOLD))
    b.append(T(500, 165, "诊断（一次区分）", 14, GOLD, "middle", "600"))
    b.append(arrow(670, 215, 330, 215, RED))
    b.append(T(500, 245, "行为改变（诊断即干预）", 14, RED, "middle", "600"))
    b.append(f'<path d="M 205 240 C 205 380 795 380 795 240" fill="none" stroke="{GREY}" '
             'stroke-width="2" stroke-dasharray="7,6" marker-end="url(#ar)"/>')
    b.append(T(500, 360, "新的观察 → 框架更新  M_{t+1} = Update(M_t, E_t)", 15, GREY, "middle"))
    b.append(T(40, H - 20, "Goodhart 定律 · 自我实现预言 · 反身性：诊断不是被动测量。", 13, GREY))
    return wrap(W, H, "\n".join(b))

# ---------------------------------------------------------------- 附录
def fig_psi():
    W, H = 1000, 420
    b = [title("图 A.1　交互惩罚 ψ 的三项分解")]
    rows = [("ψ_desc", "子模性折扣", "第 5 章", BLUE, "证据多"),
            ("ψ_comp", "计算不可约性", "第 4.5 节 / N.1", GREEN, "仅理论"),
            ("ψ_res", "时间错配 τ", "第 7、9 章", GOLD, "证据中")]
    for i, (name, desc, loc, col, ev) in enumerate(rows):
        y = 100 + i * 90
        b.append(box(60, y, 200, 70, name, "", col, "#f7f9fc", 20))
        b.append(T(290, y + 30, desc, 15, INK))
        b.append(T(290, y + 56, loc, 13, GREY))
        b.append(T(850, y + 44, ev, 15, col, "middle", "600"))
    b.append(T(40, H - 20, "三者的测量成熟度不对称：计算论部分基本只有理论。", 13, GREY))
    return wrap(W, H, "\n".join(b))


def fig_emergence():
    W, H = 1000, 400
    b = [title("图 N.1　涌现的三层与三角位置")]
    rows = [("涌现 1　编码涌现", "K_desc 受限；A 与 T 权衡", BLUE),
            ("涌现 2　因果涌现", "T 被让出", GREEN),
            ("涌现 3　价值涌现", "C 让步给 A", GOLD)]
    for i, (name, pos, col) in enumerate(rows):
        y = 100 + i * 90
        b.append(box(60, y, 320, 70, name, "", col, "#f7f9fc", 19))
        b.append(T(430, y + 44, pos, 15, INK))
    return wrap(W, H, "\n".join(b))


def fig_coverage():
    W, H = 1000, 420
    b = [title("图 P.1　核心与延伸战场的覆盖矩阵")]
    heads = ["分量", "核心战场", "延伸战场"]
    xs = [80, 360, 660]
    for x, h in zip(xs, heads):
        b.append(T(x, 116, h, 16, INK, "start", "700"))
    rows = [("K_desc", "记忆（第 5 章）", "AI（O.2）", BLUE),
            ("K_comp", "气候（第 7 章）", "软件（P.4）", GREEN),
            ("K_res", "教育/民主（第 8、9 章）", "法律/公卫（P.1、P.2）", GOLD),
            ("混合", "组织（第 10 章）", "能源（P.3）", RED)]
    for i, (a, bb, c, col) in enumerate(rows):
        y = 150 + i * 66
        b.append(T(xs[0], y, a, 15, col, "start", "600"))
        b.append(T(xs[1], y, bb, 15, INK))
        b.append(T(xs[2], y, c, 15, INK))
    return wrap(W, H, "\n".join(b))


def fig_position_map():
    W, H = 1000, 620
    b = [title("图 23.1　四本书在三角中的位置")]
    Cx, Cy = 500, 110
    Ax, Ay = 140, 540
    Tx, Ty = 860, 540
    for (x1, y1), (x2, y2) in [((Cx, Cy), (Ax, Ay)), ((Ax, Ay), (Tx, Ty)), ((Tx, Ty), (Cx, Cy))]:
        b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#c9c9c9" stroke-width="2"/>')
    books = [("《遗忘的边界》", (500, 300), BLUE), ("《区分的语法》", (360, 400), GREEN),
             ("《错位的时间》", (650, 400), GOLD), ("《选择的代价》", (500, 200), RED)]
    # 顶点标注
    b.append(T(Cx, Cy - 20, "C 完备", 17, BLUE, "middle", "700"))
    b.append(T(Ax - 4, Ay + 28, "A 可组合", 17, GREEN, "middle", "700"))
    b.append(T(Tx + 4, Ty + 28, "T 传递", 17, GOLD, "middle", "700"))
    for name, (x, y), col in books:
        b.append(box(x - 100, y - 22, 200, 46, name, "", col, "#ffffff", 15))
    return wrap(W, H, "\n".join(b))


FIGS = {
    "fig00b-three-systems.svg": fig_three_systems,
    "fig05-cta-definition.svg": fig_cta_definition,
    "fig06-journey.svg": fig_journey,
    "fig07-impossibility-family.svg": fig_impossibility_family,
    "fig08-computation.svg": fig_computation,
    "fig10-memory-cascade.svg": fig_memory_cascade,
    "fig11-medical-scales.svg": fig_medical_scales,
    "fig12-climate-clocks.svg": fig_climate_clocks,
    "fig13-education-tracks.svg": fig_education_tracks,
    "fig14-democracy-clocks.svg": fig_democracy_clocks,
    "fig15-org-lifecycle.svg": fig_org_lifecycle,
    "fig16-discipline-fission.svg": fig_discipline_fission,
    "fig17-academic-selection.svg": fig_academic_selection,
    "fig18-paradigm-migration.svg": fig_paradigm_migration,
    "fig19-update-loop.svg": fig_update_loop,
    "fig20-layered-validity.svg": fig_layered_validity,
    "fig21-balance-matrix.svg": fig_balance_matrix,
    "fig22-degradation.svg": fig_degradation,
    "fig23-playbook.svg": fig_playbook,
    "fig24-evidence-status.svg": fig_evidence_status,
    "fig25-beyond-triangle.svg": fig_beyond_triangle,
    "fig26-psi.svg": fig_psi,
    "fig27-emergence.svg": fig_emergence,
    "fig28-coverage.svg": fig_coverage,
    "fig29-position-map.svg": fig_position_map,
    "fig30-ml-timeline.svg": fig_ml_timeline,
    "fig31-math-unification.svg": fig_math_unification,
    "fig32-conflict-migration.svg": fig_conflict_migration,
    "fig33-framework-self.svg": fig_framework_self,
    "fig34-reflexivity.svg": fig_reflexivity,
}


def main():
    for name, fn in FIGS.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(fn())
        print("wrote", name)
    print(f"共 {len(FIGS)} 幅")


if __name__ == "__main__":
    main()
