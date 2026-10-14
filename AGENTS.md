# AGENTS.md — 本仓库工作约定与工具链（记忆）

> pi 会把本文件作为目录级上下文/记忆自动加载。改动后新会话生效。

## 工具链（本机实测，2026-10）

- **Git**：`D:\Git\cmd\git.exe`（不在 WSL 的 PATH 里，请用绝对路径 `/mnt/d/Git/cmd/git.exe`）
  - remote：`https://github.com/lyp0746/impossibility-triangle.git`，默认分支 `main`
  - 凭据已缓存，可直接 `push`；脚本里加 `GIT_TERMINAL_PROMPT=0` 防卡住
- **Python（构建/分析）**：`/mnt/d/0_Code/Iris Series/.venv/Scripts/python.exe`
  - 已装：numpy scipy pandas matplotlib bs4 lxml pypdf requests（**无** weasyprint / markdown）
  - `.env.build` 的 `PYTHON` 已指向该解释器；路径含空格，务必加引号
  - 注意：WSL 的 `export VAR=...` **不会**传入 Windows Python（interop）；需要 token 时在
    Python 里自己调 `git credential fill`
- **PDF 生成**：`build_book.py --pdf` 调**无头 Chrome**
  （`C:\Program Files\Google\Chrome\Application\chrome.exe`）打印，**不是** weasyprint

## 常用命令

```bash
PY="/mnt/d/0_Code/Iris Series/.venv/Scripts/python.exe"
GIT="/mnt/d/Git/cmd/git.exe"

"$PY" analysis/triangle_frontier.py   # 说明性模型 T 的精确枚举（附录 A / 图 0.1）
"$PY" analysis/frontier_scaling.py     # 前沿随规模变化（附录 A.10 / 图 2.2）
"$PY" analysis/make_figures.py        # 正文插图 fig01/02/03
"$PY" analysis/make_figures2.py       # 第二批正文配图（25 幅）
"$PY" analysis/make_cover.py          # 生成 assets/svg/cover.svg
"$PY" analysis/audit.py               # 校对 → 刷新 校对清单.md
"$PY" analysis/preregistration_checkup.py  # 校验 append-only 登记账本
bash scripts/build.sh                 # audit→印刷PDF→电子阅读PDF→EPUB→Markdown
bash scripts/validate.sh              # 校对 + EPUB 结构校验
bash scripts/release.sh               # 组装 release/
"$PY" scripts/set_repo_meta.py        # 设置 GitHub 双语描述与 topics
"$PY" scripts/create_github_release_single.py --date 2026-10-15
```

## 仓库约定

- **`source/*.html` 是唯一权威正文来源**；`output/`、`release/` 是派生产物（见 `.gitignore`）。
- 图表：脚本输出 `assets/svg/*.svg`；正文用相对路径 `assets/svg/...` 引用。
- 改正文后顺序：`analysis/make_figures.py`（如改图）→ `analysis/audit.py`
  （应无“引用但未定义的表/图”、无“无效章节引用”）→ `bash scripts/build.sh`。
- 结论标注：证据等级 **A/B/C** 与概念等级 **甲/乙/丙** 双重标注；全书数字必须带等级。
  C 级（稀疏/构造/思辨）仅作方向判断，绝不伪装成 A 级。
- **单一 release**：本仓库只保留**一个** release（tag `edition-<日期>`），一次承载全部产物
  （PDF/EPUB/HTML/Markdown/封面/说明）。**不要**再创建 per-artifact 的 release/tag；
  更新用 `--refresh` 覆盖同名资产。
- **可证伪登记簿**（`source/appendix_e_preregistration.html` 与 `docs/preregistration/`）为
  **append-only**：只追加，绝不改写旧行。
- **正文与元数据不含版本号**；日期使用真实完成日期（`source/book.json` 单一来源）。
- 发布包只放读者面文件；不得含 xlsx/csv/json/py 等原始数据与脚本（`release.sh` 有守门检查）。

## 写作风格（重要）

见 skill `academic-book-pipeline` 的 `references/voice.md`。要点：

- **张力，不宿命**：约束是交易的条件，不是判决。禁止把“必然／不可避免／无法消除／注定／死路”
  当作结论；但“给定某个选择，这笔账必然到来”属于交易句，可用。
- **分级在装置，不在每句**：证据/概念等级放表格与附录；正文一句一个精确限定即可。
- **反例进正文**；**地图只定性**；**负面结果**照实写出。
- 每个硬约束章必须带反向力量：这条限制**使什么成为可能**。
- 结构由论证决定：本书为 症状 → 三角 → 诊断 → 课题 → 设计。

## 本书特有

- **三角**：C（完备）／A（可组合）／T（传递）三选二；“被让出的顶点”是诊断的核心动作。
- **形式化**：第 2 章 + 附录 A.7（记账不等式与交互惩罚 ψ 分解）。推论：ψ≡0 时三角不适用。
- **因果强制 vs 经济权衡**（第 2.10 节）：ψ=∞ 为逻辑必然（“不可能”），有限 ψ 为经济权衡（“代价”）。
- **必然性三级**（第 2.10 节定义 2.8b）：L0 框架内 / L1 结构矛盾 / L2 已证；本书 L2 仅两条（子模性、离散曲率恒等式）。
- **冲突迁移**（第 2.10 节命题 2.3）：知识进步把冲突推到另一条边，不移除；图 2.3。
- **T 双源**（第 2.6 节定义 2.6b）：T_内在（选择造成）vs T_外在（教学造成）；三角约束前者。
- **级联反作用**（第 15.9 警告 15.4）：改一层触发 L1→L4 错位。
- **预测参数化**（第 21.8 表 21.6b）：F6-F10 的具体函数形式与反驳条件。
- **迁移边界**（第 2.10.1 警告 2.5c）：代理分化=分形迁移，非逃逸。
- **边的不对称**（第 2.10.2 表 2.3c、附注 2.6，O26）。
- **T_内在可测**（第 12.8.1 定义 12.1）：匹配教学投入下的 T 差。
- **级联条件**（第 15.9 反面检验 15.2）：同质化+长时间；否则分化。
- **验证三分类**（第 21.8 表 21.6c/21.6d）：参数来源 A/B/C；成功/失败/灰区。
- **特征时间多重性**（第 23.5 定义 23.2b）：T_response/T_adaptation/T_evolution/T_transmission。
- **冲突循环**（第 2.10.3 附注 2.7）：循环=约束重分配(L1)，非一步必然(L2)；O27。
- **迁移方向**（第 2.10.4 警告 2.5e）：系统类型/路径依赖/巧合三解。
- **多元性成本**（第 15.9 附注 15.5）：分权=元层 A+T，代价 C。
- **T_内在历史法**（第 12.8.1 替代方案 12.1）：比教学难度下降速率。
- **知识系统三层次**（第 2.2 定义 2.1b）：L_社会/L_认知/L_演化，本书主论 L_社会。
- **K 耦合**（第 2.3 假设检验 A.1）：三分量可能打包增长；O28。
- **演化模式**（第 11.8 表 11.3）：三阶段/双极摆动/顶点驻留/分裂并行；O29。
- **框架自反**（第 23.6 附注 23.1）：本书自身选 C+A、让出 T。
- **哲学基础**（附录 U）：诊断反身性(O30)、集体选择(O31)、系统边界(O32)、失败容限(O33)；框架是一次“区分”，非“从无处观看”。
- **深度失败案例**（附录 W）：四例；框架在“失效形态/方向”上匹配 4/4，在“时点/触发/新配置”上 0/4。
- **框架对标**（附录 V）：与复杂性科学/韧性/制度经济学互补，元层创新、机制薄。
- **计算路线图**（附录 X）：三角诊断套件接口约定（不做一键诊断）。
- **多代理诊断**（第 15.10 节）：代理冲突是级联的根源。
- **强预测**（第 21.8 节表 21.6，F6—F10）：带阈值/拐点、1—5 年可检验。
- **适用范围**（第 23.5 节）：T_char ≤ Δt ≤ 10·T_char；更长尺度只能给方向。
- **数学统一反思**（第 12.8 节）：统一 ≠ 简化；选 C+A 让出 T。
- **尺度错位**（第 15.8 节）：配置向量 Π；改革难是结构问题。
- **预测记录簿**（第 21.8 节，F1—F5）与附录 J 失败记录相对。
- **失败记录**（`source/appendix_j_failed.html`）是正式内容，不得删除。
- **说明性模型 T**（`analysis/triangle_frontier.py`）是 C 级说明，不得被引用为经验事实。
- **定量数据**：关键数字集中于 `data/cases.csv` 与附录 K；时间序列于 `data/cases_timeseries.csv`（近似锚点，用前必须回溯原始来源）；每章新数字必须带 A/B/C（及 B1—B3/C1—C3）等级。
- **新附录**：K 案例数据库、L 研究议题库（O1—O25）、M 系列对应、N 计算/涌现/系统论、O 前沿、P 延伸战场、Q 演化指标。
- **完整案例**：附录 H.4（研究生培养制度五步诊断）；正文第 11.7（机器学习）与 15.7（研究机构更新）。
- **反面检验**：第 5—10 章各有一节“这个诊断会怎样被推翻”；附录 P.6 同理。
- **历史脉络**：第 5—10 章各有“历史脉络”节；第 8.7/9.7.1/10.7 含驱动力表。
- **可操作性评级**：反面检验均带“可操作性评级”。
- **附录 S**：演化视角的三角（新增）；附录 A.12（ψ 测量进展）、A.13（模型 T 代表性局）。
- 三处见证的等级：子模性 A／甲；离散曲率恒等式 A／甲 + 1/3 缺口 B／乙；时间错配
  命题 A／甲 + 诊断 B／乙。

## 版本脉络

见 `versions/CHANGELOG.md`（首版）。
