# 交接档 · 产品工程 Skill（2026-09-23 · 入口索引式）

> 用途：任一会话冷启动的**入口索引**——只给指针与队列，不复制正文（防双权威/双份漂移）。
> 开工必读仍是 `memory/agent-log.md` 状态段（一屏）；本档=现状一句话 + 必读清单 + 队列 + 未决 + 回滚基线 + 操作 SOP。

## 一、现状一句话

第四包 `shisan-xinuo-product` 已双仓在线、三副本同步（本体：82 行 SKILL.md + 8 references + 4 scripts；源库 `D:\Agent工作流启动包\shisan-xinuo-workflow\skill\shisan-xinuo-product\`）。本轮完成两件大事：**①产品对象上游修正**（跑道步骤 0=产品对象六问；边界 PE≠PI；判定表 J 域四条+0b）**②高风险闭环试验实跑**（无头子代理 ×6，模型 GLM-5.3-Flash）——**正向十环成立**，核心命题「缺失可检出」**未获实证**（判据停在态级；候选 12/13 已在册）。

## 二、必读清单（按序）

1. `memory/agent-log.md` 状态段（现役队列=13 项）
2. `docs/direction.md` §〇（问题定义）/ §十一·§十二（两轮修正记录）
3. `docs/product-architecture.md`（母架构与定位边界）/ `docs/three-definitions.md`（产品/工程/产品工程 加固定义）
4. `docs/closed-loop-report.md`（试验判决全文：十环证据 + 反向注入 + 两类判据缺口 + 下一步规格草案）
5. `docs/closed-loop-experiment-protocol.md`（协议：十环定义 + 反向注入方法）
6. 本体与副本核对：`diff -rq <源库 product 包> C:/Users/zxc66/.zcode/skills/shisan-xinuo-product`（应零输出）

## 三、遗留队列（按证据排序；与状态段同源）

1. `statechart-gate` 补**引用完整性**（候选 13，一行级；验收用例=试验变体 C「删态留悬空入边，现 C1-C5 全绿」）
2. **recovery 行 ↔ 转换双向对账**门禁（候选 12；验收=变体 A；规格草案=`closed-loop-report.md` §⑥.2）
3. 强变异 B + 报告证据标准（命令原文 + diff 留档）**进协议**
4. **Q1-Q8 八条待用户裁决**（试验仓 `DEFINITION.md` §6：客户端权限非安全边界/500 阈值/主功能判定…）
5. A/B 四指标口径冻结（defect_escape/rework/coverage/cost；需先定义「什么算遗漏状态」）
6. 双会话实验扩样本 N=1→N≥3｜触发词新会话实测｜spec-trace 清单自动提取器
7. Gitee 同步｜源库发行流程（RELEASE-CHECKLIST）｜两组工具箱浏览器人工走查｜G 档 §6 抖音关键帧
8. `.agents/decision-ledger.md` 漂移处置待裁（含财务项目裁决 11 行，源库无 —— 移回项目账本 or 认作样例）

## 四、待用户裁决（阻塞项）

- 上表 4（Q1-Q8 八条）
- 上表 8（副本漂移处置）
- 本体 `version`（0.1.0）是否随本轮修正升版（家族发行流程另裁）

## 五、回滚基线

| 仓 | 基线 | 备注 |
|---|---|---|
| 设计部（本仓） | `cfb0599`（+本轮交接提交） | 权威设计档 + agent-log |
| 源库 | `aeba388` | **本地 commit，未 push**（发行走 RELEASE-CHECKLIST） |
| 试验仓 | `D:/产品工程闭环实验/` HEAD `bbcea84` | 独立仓，不 push；只读参考 |
| 三副本 | `.zcode` 与源库一致；`.agents` 仅 `decision-ledger.md` 已知漂移 | 全目录 `diff -rq` 为唯一判据 |

## 六、操作 SOP（本会话新增约束）

- **多会话并发**：本仓 `agent-log.md` 可能被他会话写入（已实测两次：04:29 并发写导致 Edit 报 modified）→ **编辑前必重读实文**（#294），且**合并而非覆盖**（教训区用追加）。
- **本体改动 SOP**：改源库 → `cp` 到两安装副本（`.zcode` + `.agents`）→ `diff -rq` 全目录核验 → 源库本地 commit（**不 push**）。
- **试验/对照类工作的记录纪律**：报告必须内联**命令原文 + 退出码 + 变异 diff**（否则「可重跑工件」在报告内不成立——本轮独立复核抓到的最大缺口）。
- **门禁声明纪律**：任何门禁必须写清「检的是**存在性**还是**完整性**」；「缺失可检出」只有拿到**反向注入证据**才算成立。
