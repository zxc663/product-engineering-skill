# 定向定稿 · 产品工程 Skill v0.1 方向

> 2026-09-21。依据：参考Skill/ 三份蒸馏（A 设计品味系 7/B 工作流极简系 10/C 工具文档系 34）+ 上位调研档（财务项目 docs/design-specs/product-engineering-skill-research.md）。
> 本文=Skill 本体动工前的方向权威；本体落成后本文退位为设计档。

## 一、四问题域 → 机制映射（Skill 存在的理由）

| 问题域 | 症状（用户原话） | 解药机制 | 上游出处 |
|---|---|---|---|
| ① 成熟共识不用 | 「成熟共识怎么做？」模型凭感觉不自查共识 | **出处化规则+检索前置**：每条判定带业界出处；共识以可检索清单（CSV/表）分发，动手前必查 | ux-feature-design 权威依据表、ui-ux-pro-max 119 准则 CSV、cms-skill-collection 共识清单、flows 调研矩阵 |
| ② 上游组件库闲置 | 「有上游组件库却没被开发利用」另造轮子 | **组件注册表+查找顺序+闲置归因**：复用五问/懒人阶梯为查表顺序；自研必须写归因；P2 出处链门禁拦截发明视觉 | anti-ui-slop「extend not invent」、flows 复用五问、ponytail 七级阶梯、impeccable extract/document、shisan 能力检索「无归因=违规绕行」 |
| ③ 反人类交互 | 「写了反人类的交互设计」甩 JSON/无出路/假快 | **判定表+真渲染取证**：一票否决反面模式（错误无出路/JSON 甩脸/点了没反应/转圈到底）；交互判断必须落到截图+DOM 证据，不接受口头 | ux-feature-design 七条一票否决+user-voices、emil 判定表、frontend-design 文案纪律、web-gui-tester 执行通道 |
| ④ 假理想功能 | 「看起来正常但缺失实际逻辑链」按钮没接事件/死代码/空 catch | **逻辑链检查+运行验证门禁**：inert interactions 固定检查项；「未经运行验证不得声称已实现」；GATE caps/ev 双字段；六态覆盖检查 | anti-ui-slop inert interactions、ux-feature-design「点了没反应」专项、impeccable detector+bounded verify、shisan GATE |

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

## 五、与既有技能的编排（不重造）

前置调度沿用财务项目 AGENTS.md Skill 前置条模式：前端任务先 ux-feature-design/impeccable（六态/打磨），极简判断先 ponytail，灵感检索 ui-ux-pro-max，落地前 critic；本 Skill 负责**注册表/账本/门禁/裁决写回**这四个无人覆盖的增量域，并在收尾把新裁决回写进 decision-ledger。
