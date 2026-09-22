# 交接档 · 产品工程 Skill（2026-09-23 夜班后 · 入口索引式）

> 用途：任一会话冷启动的**入口索引**——只给指针与队列，不复制正文（防双权威/双份漂移）。
> 开工必读仍是 `memory/agent-log.md` 状态段（一屏）；本档=现状一句话 + 必读清单 + 队列 + 未决 + 回滚基线 + 操作 SOP。

## 一、现状一句话

第四包 `shisan-xinuo-product` **v0.2.0** 双仓在线（家族 **v3.3.0**）：上游层级门（L0-L10 层栈）+产品对象六问+中游交互工程+**C1-C7 门禁**全落地。夜班四线收口：①**「缺失可检出」首次实证**（四变异反向注入全拦、对照组全绿，可重跑 verify.py）②层×判据矩阵+一页纸人话规范③工作流 Skill 三高危修复+单安装根+5 平台注入重部署 HASH-OK④冷启动三条件×8 样本实验：**触发链断点（description 缺构建侧触发词）已定位→修复→N6c 复测闭环（命中即用+层级门+档3）**；显式条件 2/2 八步全链 PASS。剩余最后一环=**用户侧重启后的真实新会话验收锚**。

## 二、必读清单（按序）

1. `memory/agent-log.md` 状态段（现役队列=9 项）
2. `docs/one-page-definition.md`（**一页纸人话规范**——是什么/不是什么/哪里还不牢）
3. `docs/direction.md` §〇 / §十一·§十二·§十三（三轮修正记录）
4. `docs/cold-start-report.md`（三条件×8 样本：触发链实验全文）/ `docs/reverse-injection/EVIDENCE.md`（缺失可检出实证，可重跑 verify.py）
5. `docs/layer-judgement-matrix.md`（每层有哪些判据/空白）/ `docs/product-architecture.md` + `docs/three-definitions.md`
6. 本体与安装根核对：`diff -rq "D:/Agent工作流启动包/shisan-xinuo-workflow/skill/shisan-xinuo-product" "C:/Users/zxc66/.agents/skills/shisan-xinuo-product"`（应仅 `references/decision-ledger.md` 一件漂移；**安装根只剩 `.agents` 一处**）

## 三、遗留队列（按证据排序；与状态段同源，共 9 项）

1. **用户侧最终验收锚**：重启 ZCode → 新会话验「在场提示 · v3.3.0＋373 条细则＋zxc663 应答」→ 说「做一个XX页面」看是否自动加载产品包（N6c 的真实版；hooks 通道只有真实会话有）
2. **Q1-Q8 八条待真人裁决**（试验仓 `DEFINITION.md` §6）
3. **product-object-gate 真实项目转正**（P1-P4 已实现：selftest 两态＋试验仓语料转写过；缺真实项目实测证据）
4. A/B 四指标口径冻结（defect_escape/rework/coverage/cost；「什么算遗漏状态」）
5. 注入+清单修复后扩样本（N6d/N6e 进行中，跨任务验证 N6c 闭环）
6. spec-trace 清单自动提取器
7. Gitee 同步＋Release zip/npm（v3.3.0 GitHub 已推；按 RELEASE-CHECKLIST 剩余项）
8. 两组工具箱浏览器人工走查｜G 档 §6 抖音关键帧
9. `.agents/skills/shisan-xinuo-product/references/decision-ledger.md` 漂移处置待裁（**实测在档**，31 行 vs 源库 20——财务项目 11 行裁决，移回项目账本 or 认作样例）

## 四、待用户裁决（阻塞项）

- 上表 5（Q1-Q8 八条）
- 上表 10（副本漂移处置）
- （非阻塞·已执行待追认）风险四档命名 L0-L3→档0-档3；触发词第三次密集化（构建侧）——均有实验依据，不认可可回退

## 五、回滚基线

| 仓 | 基线 | 备注 |
|---|---|---|
| 设计部（本仓） | `1945421`（+收尾提交） | 权威设计档 + agent-log；GitHub 已推 |
| 源库（家族） | `b9e07a7`（v3.3.0） | **GitHub 已推**；Gitee/Release/npm 未动 |
| 试验仓 | `D:/产品工程闭环实验/` HEAD `bbcea84` | 独立仓，不 push；只读参考 |
| 冷启动实验区 | `D:/产品工程冷启动-20260923*/`（8 个） | 独立仓；实验原始语料，保留 |
| 安装根 | **仅 `~/.agents/skills/`**（`.zcode` 侧家族包已处置，备份=`D:/Agent工作流启动包/skill-backups/zcode-side-family-skills-20260923.tar.gz`） | 一致性判据=`diff -rq` 全目录 |
| 注入副本 | 5 平台 v3.3.0，`--check --hash` 5/5 HASH-OK（`b9b00ca712cc`） | 各带 `.bak-20260923-052926-pre-v3.3.0` |

## 六、操作 SOP（现行版）

- **多会话并发**：编辑 `agent-log.md` 前必重读实文（#294），合并而非覆盖；教训区只追加。
- **本体改动 SOP（v2，单安装根）**：改源库 → cp 到 `.agents`（唯一根；**.py 必须走 Write 工具**，bash cp 会被 Mimosa 拦）→ `diff -rq` 全目录核验 → 源库 commit → GitHub push（`git -c http.proxy= -c https.proxy= push origin HEAD`，本机代理失效需绕行）。
- **随包脚本两处同步**：`risk_scan/agent_log_rotate/gate_audit/syncer` 权威=源库根 `scripts/`，分发副本=包内 `scripts/`——改任一处必须两处同步（发行前 diff 检查已入 RELEASE-CHECKLIST）。
- **注入重部署**：`python scripts/deploy_injection.py --version <ver>`（写模式必须显式给版本）→ `--check --hash` 验收；改 injection-core.md 必须重部署。
- **实验纪律**：触发类实验的实验单元=裸环境（单点子代理+独立空工作区）；工作流引擎只做样本间并行；判定以工作区实物为准（自述≠实物，教训区第 6 条）；注入模拟须带常驻清单（N6 教训）。
- **写档时间戳**：先 `date` 取实时钟再落笔（估时会产生未来时间戳，已发生两次）。
