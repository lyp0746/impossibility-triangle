# 选择的代价

### 完备、可组合与可传递的三维权衡——复杂知识系统如何形成、演化与更新

> **The Price of Choice** — The Impossibility Triangle of Completeness, Composability, and Transfer: How Complex Knowledge Systems Form, Evolve, and Renew

李毅芃　著　·　2026　·　CC BY 4.0　·　源码：[github.com/lyp0746/impossibility-triangle](https://github.com/lyp0746/impossibility-triangle)

---

## 这本书在做什么

把作者此前三本书中三处**"无法弥合的矛盾"**诊断为同一个结构性困境：

- 《遗忘的边界》——遗忘与更新 → 让出**可组合性**
- 《区分的演化》——离散完备与连续传递 → 让出**传递性**
- 《错位的时间》——效率与冗余、时间错配 → 让出**完备性**

**一句话：** 任何有限复杂度的知识系统，都不能同时完整地拥有局部完备性（C）、可组合性（A）与跨尺度传递性（T）；至多两个。三角不是宿命，是一张**价目表**；诊断的核心动作，就是指出系统**让出了哪一个顶点**。

## 核心主张（分级）

| 层 | 内容 | 强度 | 位置 |
|---|---|---|---|
| 硬核 | 信息子模性（能力不能线性相加）；离散分离曲率恒等式 | **定理（A／甲）** | 第 5、12 章 |
| 硬核 | 说明性模型 T 的可达前沿（473721 种分配精确枚举） | **模型（A／丙）** | 附录 A |
| 形式化 | 系统四元组、复杂度三分量、可测量坐标 (c,a,t)、记账不等式 | **条件命题（B／乙）** | 第 2 章、附录 A.7 |
| 诊断 | 四个战场的 C-A-T 选择（含定量诊断与历史脉络） | 框架（B／乙） | 第二部分 |
| 诊断 | 三角命题（至多两个顶点满格） | 框架（C／丙） | 第 2 章 |
| 纲领 | 三角之外；第四性质；可行域形状；O1—O25 | 纲领（C／丙） | 第 21、22 章、附录 L |

## 三个可检验的诊断

1. **子模性**：`I(Z; X₁∪X₂) ≤ I(Z;X₁) + I(Z;X₂)`——有限容量下，能力不能相加。
2. **离散—连续缺口**：`κ_info = Var(λ)/2` 在有限图上精确；跨到连续留下因子 `1/3` 的缺口。
3. **时间错配**：`τ = T_min / T_available`；τ 增大时诊断置信区间发散，框架退化为方向。

## 结构：症状 → 三角 → 诊断 → 课题 → 设计

| 部分 | 章 | 内容 |
|---|---|---|
| 先读这一页 | 前件 | 三条可检验的诊断，供怀疑论者先验证 |
| 背景 | 前件 | **从三个复杂系统（记忆/区分结构/社会时间）引入并精确定义 C-A-T** | |
| 第一部分 | 第 1—4 章 | 问题的现身：三处症状、不可能三角、分级纪律、与已有理论对话 |
| 第二部分 | 第 5—10 章 | **现实诊断**：生命、物理、社会、人工四个战场 |
| 第三部分 | 第 11—15 章 | **形成、演化与更新**：三阶段成长、学科分裂、学术体制、范式转变、制度性管理 |
| 第四部分 | 第 16—20 章 | **设计智慧**：分层有效性、制度权衡、优雅降级、书写方式、诊断手册 |
| 第五部分 | 第 21—23 章 | 边界与纲领：证据现状、三角之外、结语 |
| 附录 | A—Y | 形式化、案例总表、文献（含文献地图）、术语、可证伪登记、缺口、工具、模板、对照、失败记录、**案例数据库、研究议题库、系列对应、计算与系统论、三大前沿、延伸战场、演化指标、演化视角、边界案例、根本质疑、**诊断的哲学基础、框架对标、失败案例、计算路线图、**实证探针集** |

## 快速开始

```bash
# 1) 复现说明性模型的精确枚举（n=12, K=15）
python analysis/triangle_frontier.py

# 1c) 软件实证探针（附录 Y.1，需 GitHub token；双仓库对照）
python analysis/linux_kernel_probe.py --n 200

# 1d) arXiv 文献探针（附录 Y.2）
python analysis/arxiv_crossfield.py --per-year 300

# 1e) OpenAlex 引用层面探针（附录 Y.2b，O36）
python analysis/openalex_fission.py

# 1b) 复现前沿随规模变化（n 至 200，图 2.2）
python analysis/frontier_scaling.py

# 2) 生成插图与封面
python analysis/make_figures.py && python analysis/make_cover.py

# 3) 构建全部版本：印刷 PDF / 电子阅读 PDF / EPUB / HTML / Markdown
bash scripts/build.sh

# 4) 质量门禁
bash scripts/validate.sh

# 5) 组装发布包
bash scripts/release.sh
```

依赖：Python（numpy、lxml、pypdf、bs4）、Chrome/Edge（PDF 打印）。

## 目录结构

```
impossibility-triangle/
├── source/              # 唯一权威正文来源（HTML）
│   ├── book.json        # 书名/作者/日期/摘要（单一来源）
│   ├── parts.json       # 部分 → 章 → 节
│   ├── ch01.html … ch23.html
│   ├── front_*.html / back_*.html
│   └── appendix_*.html
├── analysis/            # 数值复现、插图、校对、登记核销
├── assets/{css,svg}/    # 版式与矢量插图
├── docs/                # 方法论、来源、缺口、贡献指南、preregistration/
├── scripts/             # build / validate / release
└── output/, release/    # 派生产物（gitignored）
```

## 可证伪性与失败记录

- **可证伪登记簿**（附录 E 与 `docs/preregistration/`）：每条可反驳命题写明证伪条件与核验日期；账本**只追加、不修改**。
- **失败记录**（附录 J）：作者照实保留两条被自己脚本推翻的强主张（"坐标和上界恒为 2"、"恰好让出一个顶点"）。

## 工程验证

```bash
python analysis/triangle_frontier.py   # 精确枚举 473721 种分配
bash scripts/validate.sh               # 校对 + EPUB 结构校验
```

## 引用

```bibtex
@book{li2026price,
  title     = {选择的代价：完备、可组合与可传递的三维权衡——复杂知识系统如何形成、演化与更新},
  author    = {李毅芃},
  year      = {2026},
  publisher = {GitHub},
  note      = {CC BY 4.0},
  url       = {https://github.com/lyp0746/impossibility-triangle}
}
```

## 许可

- 正文：**CC BY 4.0**
- 代码与脚本：**MIT**

---

# English

## The Price of Choice

### The Impossibility Triangle of Completeness, Composability, and Transfer — How Complex Knowledge Systems Form, Evolve, and Renew

**What this book does.** It diagnoses three "unbridgeable contradictions" from the author's previous three books as one structural predicament. *The Boundary of Forgetting* (forgetting vs. updating) concedes **composability**; *The Evolution of Distinction* (discrete completeness vs. continuous transfer) concedes **transferability**; *The Time Out of Joint* (efficiency vs. redundancy, temporal mismatch) concedes **completeness**.

**Central thesis.** Any knowledge system of bounded complexity cannot fully possess all three at once — local **completeness** (C), **composability** (A), and cross-scale **transferability** (T) — but at most two. The triangle is not fate but a **price list**; the core diagnostic act is to name the *conceded vertex*.

**Three testable diagnostics.**

1. **Submodularity**: `I(Z; X₁∪X₂) ≤ I(Z;X₁) + I(Z;X₂)` — under limited capacity, capabilities do not add linearly.
2. **Discrete–continuous gap**: `κ_info = Var(λ)/2` is exact on finite graphs; passing to the continuum leaves a factor-of-`1/3` gap.
3. **Temporal mismatch**: `τ = T_min / T_available`; as τ grows, the diagnostic's confidence interval diverges and the framework degrades to direction only.

**Structure.** Three testable diagnostics → the triangle → four battlefields (life, physics, society, artifacts) → how knowledge systems form, evolve, and renew → design wisdom (layered validity, institutional trade-offs, graceful degradation, diagnostic playbook). Every strong claim carries an evidence grade (A/B/C) and a falsification condition; the preregistration ledger is append-only and the author's own falsified claims (Appendix J) are kept on record.

**Reproduce.**

```bash
python analysis/triangle_frontier.py   # exact enumeration of the illustrative model
bash scripts/build.sh                   # PDF / EPUB / HTML / Markdown
```

**Cite.** Li Yipeng. *The Price of Choice: The Impossibility Triangle of Completeness, Composability, and Transfer*. 2026. CC BY 4.0.

**License.** Text: CC BY 4.0. Code: MIT.
