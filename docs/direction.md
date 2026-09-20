# 定向定稿 · 产品工程 Skill v0.1 方向

> 2026-09-21。依据：参考Skill/ 三份蒸馏（A 设计品味系 7/B 工作流极简系 10/C 工具文档系 34）+ 上位调研档（财务项目 docs/design-specs/product-engineering-skill-research.md）。
> 本文=Skill 本体动工前的方向权威；本体落成后本文退位为设计档。

## 〇、我们究竟解决什么问题（问题定义，先于一切机制）

**一句话**：每次会话的模型，都是一个失忆的、只做局部最优的工人，交付完就走；而产品是一个需要有人对全局负责、对承诺持续兑现的有机体。本 Skill 把工匠的三样东西——**地图（项目里已有什么）、厂规（这个项目什么是好的）、验收机（交付是不是真的）**——外置成工人每次上岗必领的工具，让局部优化器每走一步都恰好是全局最优的一步。

**根因=成本结构镜像颠倒**。模型的成本结构（写新代码便宜/复用贵/验证更贵/用户信任=0）与产品的成本结构（写新代码最贵/复用最便宜/验证是唯一真实/用户信任=一切）逐项相反。模型在自己结构里理性的选择，在产品结构里全是毒药。工作流 Skill 已修正「验证」一项（GATE 强制）；本 Skill 修正剩下两项：**让「复用」和「用户视角」从模型的免费品变成必须支付的硬成本。**

**产品=承诺的集合**。按钮是承诺（点了会发生什么）、输入框是承诺（这里该填什么）、错误信息是承诺（你有出路）。四个症状在这个镜头下统一：假理想功能=不兑现的承诺；反人类交互=违背直觉的承诺（JSON 甩脸=把实现细节当对用户的承诺）；组件库闲置=与过去承诺冲突的新承诺（产品精神分裂）；共识不用=对行业承诺的无知。模型的致命点：它只生产承诺的表皮——**兑现发生在交互时，而它只在场于生成时**。本 Skill 的一切工件，本质都是把「兑现义务」从交互时（模型已离场）前移到生成时（模型在场的唯一时刻）。

**反面校验（由此推导的不该做）**：①不写更多抽象原则（原则对失忆工人是噪音）；②不追求「模型拥有审美」（工人永远是新的，给他厂规，审美单源=用户投进账本的票）；③厂规不写一千条（准入测试+上限防废话化）；④每件工件必过检验：「下个会话的失忆工人在哪个动作前、以多少成本、被什么机制强制使用它？」——答不上来的工件，删。

## 一、四问题域 → 机制映射（问题定义的三件工具展开）

| 问题域 | 症状（用户原话） | 解药机制 | 上游出处 | 归属工具 |
|---|---|---|---|---|
| ① 成熟共识不用 | 「成熟共识怎么做？」模型凭感觉不自查共识 | **出处化规则+检索前置**：每条判定带业界出处；共识以可检索清单（CSV/表）分发，动手前必查 | ux-feature-design 权威依据表、ui-ux-pro-max 119 准则 CSV、cms-skill-collection 共识清单、flows 调研矩阵 | 厂规 |
| ② 上游组件库闲置 | 「有上游组件库却没被开发利用」另造轮子 | **组件注册表+查找顺序+闲置归因**：复用五问/懒人阶梯为查表顺序；自研必须写归因；P2 出处链门禁拦截发明视觉 | anti-ui-slop「extend not invent」、flows 复用五问、ponytail 七级阶梯、impeccable extract/document、shisan 能力检索「无归因=违规绕行」 | 地图 |
| ③ 反人类交互 | 「写了反人类的交互设计」甩 JSON/无出路/假快 | **判定表+真渲染取证**：一票否决反面模式（错误无出路/JSON 甩脸/点了没反应/转圈到底）；交互判断必须落到截图+DOM 证据，不接受口头 | ux-feature-design 七条一票否决+user-voices、emil 判定表、frontend-design 文案纪律、web-gui-tester 执行通道 | 厂规+验收机 |
| ④ 假理想功能 | 「看起来正常但缺失实际逻辑链」按钮没接事件/死代码/空 catch | **逻辑链检查+运行验证门禁**：inert interactions 固定检查项；「未经运行验证不得声称已实现」；GATE caps/ev 双字段；六态覆盖检查 | anti-ui-slop inert interactions、ux-feature-design「点了没反应」专项、impeccable detector+bounded verify、shisan GATE | 验收机 |

## 二、反借口表 v1（Skill 内独立成节；借口→驳斥成对，配危险词触发器）

| # | 借口 | 驳斥 | 上游 |
|---|---|---|---|
| 1 | 「已经实现了/接好了」 | 未经运行验证（真跑+宿主返回），不得声称已连接 | anti-ui-slop:33 |
| 2 | 「没查到相关信息」 | 零结果不得当作有结果；须声明 fallback | ui-ux-pro-max:169 |
| 3 | 「应该有这个库/组件吧」 | 不得假设技术栈与依赖存在——先查 package.json/注册表 | ui-ux-pro-max:71、taste-skill:157 |
| 4 | 「默认这样也可以」 | 选项轴空着=没在做决定；默认必须给出为什么 | impeccable craft-floor:21 |
| 5 | 「加个动画为了好看」 | 「为了好看」对高频操作不成立；先过动画四问（频率→目的→easing→时长） | emil:93 |
| 6 | 「体验应该没问题」 | 以用户在交互点看到什么为准；必须截图+DOM 佐证 | shisan-xinuo-roles frontend.md:11,21 |
| 7 | 「这个很简单/显然/只是小改动」 | 危险词出现即自检：最小改动在错误的地方不是懒，是第二个 bug | shisan:177-188、ponytail:61 |
| 8 | 「为了简化所以没写」 | 为简化辩护的散文比代码长=走私的复杂度，删 | ponytail:70-73 |
| 9 | （对 Skill 作者的教训）「让模型适度/尽量少用」 | 模型无视 used sparingly——一切品味规则写成零容忍二元规则 | taste-skill:701 |

## 三、Skill 结构定稿（对齐 skill-creator 规范）

```
product-engineering/            ← 安装于 .agents/skills/
├── SKILL.md                    ← <500 行：frontmatter + 四问题域路由 + 判定表骨架（首批 10 条）+ 反借口表 v1 + 何时读哪个文件
├── references/
│   ├── judgement-table.md      ← 判定表全集：行 schema=触发场景｜判断｜行动 + Do/Don't 代码双例 + Severity（ui-ux-pro-max 十列 + session-knowledge 三段式融合）
│   ├── decision-ledger.md      ← 决策账本 schema：组件行（名/职责/复用点/淘汰替代+理由）+ 条目准入五问 + 关系枚举（复用/互补/冲突）
│   ├── anti-excuses.md         ← 反借口表全集（v1 九条起步）
│   └── registry.md             ← 组件注册表 schema + 入库流程（impeccable extract/document 模式）
└── scripts/
    ├── registry-gate           ← 门禁①：新组件/类必须先注册（grep 差集，退出码 1）
    ├── inline-style-gate       ← 门禁②：内联样式/硬编码 hex 检查（P4 泛化）
    └── dead-binding-gate       ← 门禁③：假理想功能静态检查（死代码/空 catch/未引用的 computed——classifyNotice 教训）
```

- frontmatter description（pushy，枚举口语触发词）：「丑/难用/反直觉/为什么不用现成的组件/这功能好像没用/假功能/写了没反应」+ 英文等价。
- 判定表两栏分离：**业界共识**（带出处）vs **本 Skill 风格**（标明是选择不是真理）——em-dash 教训。
- 防膨胀三闸：新条目五问准入（rule-optimizer）+账本默认 3 上限 5（session-knowledge）+引用编号不复制正文（roles 防棘轮）。
- 冲突裁决：既有组件/设计系统在→保守复用优先（anti-ui-slop）；greenfield→反模板自批（frontend-design）；用户 brief 原话永远赢过本 Skill（frontend-design:31）。
- 质询环节 `disable-model-invocation: true`（grill-me 形态）。

## 四、第一迭代切片（下一轮动工）

1. SKILL.md 骨架（frontmatter+路由+首批判定表 10 条：四问题域各 2-3 条，全部代码级正反例）。
2. anti-excuses.md：反借口表 9 条成稿。
3. scripts/registry-gate：可运行的 grep 门禁 v1（对一个样例项目实测 exit 0/1 两态）。
4. 验收：按 skill-creator 规范用 2-3 个真实提示词测触发与输出；trace 查 busywork。

**第一迭代验收校准（按问题定义）**：不只测「触发与输出」，每件工件必须同时通过问题定义检验——①失忆工人检验：一个全新会话、只装本 Skill 不装任何历史，能否在正确的动作前拿到它？②成本检验：使用它的成本（一次 grep/一次读 50 行）是否低于不使用（另造一页）？③兑现检验：门禁能否对「classifyNotice 式死代码」给出退出码 1？三者任一不过=该工件返工或删除。

## 五、与既有技能的编排（不重造）

前置调度沿用财务项目 AGENTS.md Skill 前置条模式：前端任务先 ux-feature-design/impeccable（六态/打磨），极简判断先 ponytail，灵感检索 ui-ux-pro-max，落地前 critic；本 Skill 负责**注册表/账本/门禁/裁决写回**这四个无人覆盖的增量域，并在收尾把新裁决回写进 decision-ledger。
