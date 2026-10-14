# 版本脉络（内部）

> 本文件仅供维护者使用，**不进入发布包**。读者可见的说明见 `docs/RELEASE-NOTES.md`。

## 首版

- **正文**：五部分、二十三章。第一部分（问题的现身：三处症状、不可能三角、分级纪律、与已有理论对话）、第二部分（四个战场：生命、物理、社会、人工）、第三部分（形成、演化与更新）、第四部分（设计智慧）、第五部分（边界与纲领）。
- **前置**：先读这一页、前言、十分钟读懂、阅读合约、术语与分级速查。
- **后置**：结语、附录 A—J。
- **硬核**：信息子模性（引用香农）、离散分离曲率恒等式（引用《区分的演化》第 12.6 节）、说明性模型 T 的精确枚举（新脚本 `analysis/triangle_frontier.py`）。
- **失败记录（附录 J）**：F1（坐标和上界恒为 2）被自己的脚本证伪；F2（恰好让出一个顶点）被削弱。
- **可证伪登记**：`docs/preregistration/registry.json` 登记 P1—P9；`checkups.csv` 为 append-only。
- **工程**：`analysis/triangle_frontier.py`、`make_figures.py`、`make_cover.py`、`audit.py`、`preregistration_checkup.py`。
- **构建**：`scripts/build.sh`、`validate.sh`、`release.sh`；单一 release（tag `edition-<日期>`）。

### 已知局限

- 三角命题为框架（C／丙），未证明。
- 说明性模型 T 只展示结构，不对应任何真实系统的测量。
- 四个战场的诊断依赖领域解释，需领域专家检验。
- 模型 T 的坐标和上界依赖 n、K，非普适常数。
