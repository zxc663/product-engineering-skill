# D 组调研 · 同类相似项目（外部竞品/同类品）

> 研读日期 2026-09-21。目的：校验产品工程 Skill 的差异化是否成立，吸收同类已验证的做法。

## 1. Nutlope/hallmark（Together AI）——最直接同类

**定位**：给 Claude Code/Cursor/Codex 的反 AI-slop 设计技能——「refuses to look AI-generated」。
**机制**：
- **四动词产品化**：默认 build（选宏观结构+套规则集+交稿前跑 slop test）/ `hallmark audit <target>`（对既有代码按反模式打分，出 punch list 不改码）/ `hallmark redesign`（抛结构保内容与品牌重建）/ `hallmark study <截图|URL>`（提取心仪设计 DNA：宏观结构/字体配对/色彩锚，拒像素克隆，可产出 portable `design.md` 交接给其他 AI 工具）。
- **20 预置主题 + 57 道 slop-test gates + pre-emit self-critique**（交付前自我批评一轮）；「refuses the on-distribution defaults every LLM was trained into」（拒绝训练分布里的默认审美）。
- Custom 分支：brief 带无主题可配的创意意图时从零设计，同一 57 门禁，协议在 `custom-theme.md`。
- 结构：SKILL.md + references/ + docs/recipes.md（实例）+ docs/study-examples.md；安装 `npx skills add nutlope/hallmark`；每页 CSS 注释盖 macrostructure 戳。
**对照我们**：强=视觉 slop 防护、主题分发、**audit/study 动词化命令**（audit=对既有代码打分出清单，正是 registry-gate 的产品化形态；study=从人类欣赏的设计提取 DNA 再落地，是「审美单源=人类投票」的工程化）；**缺**=项目既有组件注册表、跨会话裁决账本、假理想功能/逻辑链检查、中文与工作流对接。

## 2. vercel-labs/web-interface-guidelines（862★）

**定位**：Web 界面构建准则的活文档（100+ 条，七类：Interactions/Animations/Layout/Content/Forms/Performance/Design + Vercel-specific 品牌分节）；配套 `web-design-guidelines` skill——**扫描 UI 代码产出 file:line findings**（违反条目定位到行）；另发 AGENTS.md 供项目集成使 agent 生成时即遵守。
**与本项目判定表直接互补的条目**（此前清单没有的）：
- 「No dead ends. Every screen offers a next step or recovery path.」——空态跳转按钮缺陷的业界原文表述
- 「All states designed. Empty, sparse, dense, & error states.」——六态的近亲表述
- 「Error messages guide the exit」+ 反例正例对照（"Invalid API key"→"…Generate a new key in your account settings."）——错误出路的标准范式
- 「Loading buttons 保留原标签」「spinner 150-300ms 延迟+300-500ms 最短可见防闪烁」「Confirm destructive actions / Undo 安全窗」「URL as state / deep-link everything」「Never `transition: all`」「tabular-nums」「不单靠颜色传状态（冗余状态线索）」「Links are links（导航禁用 button/div）」「Don't pre-disable submit（允许提交空表单暴露校验反馈）」
- **结构验证**：Vercel-specific 单独分节把「品牌选择」与「通用准则」隔离——与 taste-skill em-dash 教训同构，**验证我们判定表「业界共识/本 Skill 风格」两栏分离的设计**。
**对照我们**：强=静态指南密度与条目文风（粗体原则+一句做法）、file:line findings 输出、AGENTS.md 集成；**缺**=项目绑定（注册表/账本）、假功能检查、跨会话机制。

## 3. 分发与目录生态
awesome-claude-skills 三大目录（BehiSecc / travisvn ≈8.8k★ / ComposioHQ）+ rohitg00/awesome-claude-code-toolkit（135 agents/35+ skills）=同类技能的发现渠道与素材矿；skillselion/skillhub 等第三方目录已收录 vercel 的 web-design-guidelines。

## 4. 差异化校验结论（四增量全部仍然成立，且得到强化）

| 我们的增量 | 同类现状 | 结论 |
|---|---|---|
| 组件注册表+出处链 | anti-ui-slop 只有一句「extend them」原则；shadcn registry 是通用分发非项目绑定 | 成立，且 registry-gate 可借 hallmark `audit` 命令形态产品化 |
| 跨会话裁决账本（写回协议） | 全场空白（hallmark/vercel 均无状态） | 成立，最独特 |
| 假理想功能/逻辑链门禁 | 仅 anti-ui-slop 一句 inert interactions Finish 检查，无系统化 | 成立，先发优势明显 |
| 与工作流纪律对接（GATE/复述/能力检索） | 无人做 agent 纪律与设计品味的合流 | 成立 |
| 新增借鉴 | hallmark 四动词（audit/study 特别值得）、vercel file:line findings 输出与 AGENTS.md 集成、vercel 条目文风与 20+ 条互补判定、No dead ends 等表述 | 并入判定表与命令设计 |

## 5. 对方向档的修订（增补进 direction.md 的三点）
1. 判定表新增「业界共识」来源：vercel-labs/web-interface-guidelines（100+ 条，七类）——与 ux-feature-design/ui-ux-pro-max 并列为出处源。
2. 命令形态借鉴 hallmark：门禁不只是脚本，做成 `audit`（出 punch list）/`study`（从人类指定设计提取 DNA 进注册表）两类动词。
3. 交付物可携带「portable design.md」交接形态（hallmark study 同款）——跨工具/跨会话交接的现成范式。
