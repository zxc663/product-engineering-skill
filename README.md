# product-engineering-skill · 产品工程 Skill（设计部）

> 十三希诺工作流家族第四包 `shisan-xinuo-product` 的**设计源**（设计部）：联通层结构设计、八份调研蒸馏、可判定门禁。
> 包本体随家族主仓发行：[shisan-xinuo-workflow](https://github.com/zxc663/shisan-xinuo-workflow)（`skill/shisan-xinuo-product/`）。

## 这是什么

市面上的设计类 Skill 几乎全部挤在**手法层**——教模型「怎么写才好看好交互」（样式、组件、动效、文案）。本项目的定位是那片之外的**结构层**——一个尚未形成成熟统一范式的工程层（不证明无人做，只补生态缺的「统一、可执行、可验证的桥接层」）：

> **设计 Skill 只设计怎么做，我们定义各功能的流程状态怎么来。**

每次会话的模型都是一个失忆的、只做局部最优的工人；产品是需要对全局负责、持续兑现承诺的有机体。本 Skill 把工匠的三样东西——**地图（项目里已有什么）、厂规（这个项目什么是好的）、验收机（交付是不是真的）**——外置成工人每次上岗必领的工具。

**唯一目的**：真实用户使用产品时的体验。3 万与 30 万的功能清单可以完全相同，差价全在旅程完整性——本 Skill 把这个差价变成可判定、可生产的清单。

**定位边界（2026-09-23 裁决）**：本仓库=设计部；包本体=**产品工程**（Product Contracts 规范层的**第一垂直域**）——层级门（先定位在回答哪一层）+ 上游「产品对象定义」+ 中游「交互工程」已落地，母架构其余域**未实现**；**产品工程≠产品创新**（创新属产品决策侧，不是工程的必要任务）。详见 [docs/product-architecture.md](docs/product-architecture.md)。

**先读这张纸**：[docs/one-page-definition.md](docs/one-page-definition.md)——一页说完「是什么 / 不是什么 / 哪里还不牢」（人话版规范；术语消歧也在里面）。

## 核心构件

| 构件 | 一句话 | 出处挂靠 |
|---|---|---|
| 功能天生六问 | 输入什么/何时发生/成功落哪/防失败-恢复-出路/能否反悔/下次换环境还认吗 | Norman 行动七阶段+两个鸿沟 |
| 联通层 | 功能语义↔交互逻辑的**可判定契约**（双向可追溯+机器可验） | Garrett 五层（范围↔结构接口） |
| statechart 载体 | 态+转换矩阵的源=机器可读 JSON（无死端/全可达/错误态有恢复=「出路」的严格表述） | Harel 1987 / XState |
| 双底双顶+第四底 | 不难用/不难看/无障碍（底线·法律）+更好用/更好看（上限·劝导） | Nielsen/ISO 9241-11/WCAG POUR |
| 反借口表 | 借口→驳斥成对，危险词触发自检；一切规则二值化 | taste-skill 教训 |
| 裁决账本 | 记「为何这么定」，跨会话复利——劝导会衰减，法律不会 | 本项目原创（同类空白） |
| 效力衰减链 | 在场不触发→计划不引用→压缩失真→仪式化→产出照旧：五级衰减与对策 | 见 docs/direction.md §七 |
| 产品对象六问 | 上游先于六问：为什么存在/职责句/能力清单/主次（恰好一个主功能）/能力完整性（八组闭环）/可运营性（谁能管）——缺答=停 | 用户定稿 2026-09-23（四偏移纠正，direction §十二） |
| 层级栈 L0-L10 + 层级门 | 先定位「在回答哪一层的问题」→检上游→才允许下沉；**实现层完整性≠产品工程完整性** | 用户定稿 2026-09-23（direction §十三） |
| 契约 schema | Interaction/Gate/Evidence 三件；硬层机器可验、软层可追溯（禁全链 JSON 化） | 用户裁决 2026-09-23 |
| 风险自适应四档 | 档0 不启动 / 档1 轻量 / 档2 六问+trace / 档3 +recovery+evidence+regression | 同上（判定表 §风险档位；2026-09-23 由 L0-L3 改名防与层栈混淆） |

## 仓库结构

```
docs/one-page-definition.md ← **一页纸：这个 Skill 是什么**（人话版规范，冷启动先读）
docs/direction.md          ← 方向档（问题定义/衰减链/品味与时序/联通层/强制边界/修正记录）——权威设计档
docs/product-architecture.md ← 母架构与定位边界（Product Contracts 七域；已落地=Interaction）
docs/three-definitions.md  ← 三定义调研（产品/工程/产品工程 加固定义 + 缺失逻辑可检出表述）
docs/layer-judgement-matrix.md ← 层×判据矩阵（11 层各自有哪些判据/人工裁决域/空白）
docs/reverse-injection/EVIDENCE.md ← 「缺失可检出」反向注入实证（可重跑：verify.py）
参考Skill/A~H              ← 八份调研蒸馏（设计品味系/工作流极简系/工具文档系/外部同类/桌面项目/成熟方法论/高密度界面/结构层蓝海）
skill/…（在家族主仓）       ← 第四包本体：SKILL.md+references 九件+scripts 四门禁
memory/agent-log.md        ← 工作流水（诚实留档：含每轮 GATE 与教训）
```

## 门禁用法（第四包 scripts）

```bash
# 组件归因检查（自研必须带归因标记 registry:）
python registry-gate.py --path <组件目录> --selftest

# statechart 结构检查（出路的严格表述）
python statechart-gate.py --file statechart.json --selftest
```

两门禁均内置 `--selftest` 两态自测（拦截态+放行态）。

## 与家族的关系

`shisan-xinuo-workflow` 核心包已埋**条件式挂接钩子**（skill-usage §8）：本包在场→三缝合点自动生效（计划检索位/GATE 门禁真值/收尾账本写回）；不在场→跳过+GATE exempt 声明。分合都可用。

## 设计纪律（本仓库自己的规矩）

- 隐私红线：真实账单/密钥绝不入仓。
- 诚实红线：未实现/未验证显式标注；出处带信心级（原文读过/转述可靠/待验），接受抽验。
- 强制清单宁缺毋滥：新增强制须过「可机器判定+决策点拦截+成本检验」三判据。

## License

MIT（与家族主仓一致）
