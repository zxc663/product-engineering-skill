# Agent 工作日志（一档制）

> 权威承载 = 本文件｜开工必读状态段

## 一、状态段

STATE: task=产品工程 Skill 立项——方向档 v0.5：职责再收窄（不定义主题组件）+真强制八项+能力地图+缺口登记五项 | level=L2-F | route=联通层唯一职责（规定功能应怎么来）+强制/劝导分界（八项法律级过成本检验）+capability-map 路由层 | confirm=无需 | gates_passed=—（本体未动工） | last_errpath=WebFetch github.com 本机 TLS 证书拦截→改 mcp web_reader 服务端抓取（成功）
- 当前阶段：**方向定稿 v0.5（2026-09-21）**——四调研（D 档 §1-7）+问题定义+衰减链+品味时序+联通层中心（§九）+强制边界与缺口登记（§十：强制八项/能力地图/新缺口五项/工作流回补四条）；待用户点名开工第一迭代切片
- 任务级别：L2-F
- 本机环境：Windows+ZCode；WebFetch 对 github.com 证书验证失败（本机 TLS 拦截），外部深读走 mcp web_reader；ponytail 本机=单文件 6.7KB（~/.zcode/skills，无 ~/.agents 副本）
- 最近更新：2026-09-21 04:26
- 遗留：Skill 本体未写；门禁脚本未产；工作流 Skill 回补四条待用户择期实施
- 遗留：Skill 本体未写；门禁脚本未产
- 遗留：Skill 本体未写；门禁脚本未产
- 遗留：Skill 本体未写；门禁脚本未产

## 二、教训区

（待积累）

## 三、偏好段

（待积累）

## 四、流水区

### 2026-09-21 01:40｜第一轮：立项骨架+全量研读启动
- 桌面新建「产品工程Skill/」（AGENTS.md+参考Skill/+docs/+gates/+memory/+git init main）
- 要解决四问题域：①成熟共识不用 ②上游组件库闲置 ③反人类交互 ④假理想功能（逻辑链断裂）+反借口表
- 分组研读：A 设计品味系（taste-skill/anti-ui-slop/emil-design-eng/frontend-design/impeccable/ux-feature-design/ui-ux-pro-max）/B 工作流极简系（shisan-xinuo 三册/ponytail×2/grill-me/ask-user/skill-creator/session-knowledge/rule-optimizer）/C 工具文档系快扫（其余+插件官方技能）
- GATE: {level=L2-F, v=立项骨架, cmd=mkdir+git init, exit=0, files=AGENTS.md+参考Skill/+docs/+gates/+memory/, refs=0(未跑 lookup，0 照报), errpath=—, lessons=—, exempt=蒸馏与定向（进行中）, caps=Explore×3 并行, effort=骨架+分组方案, stop_reason=—}

### 2026-09-21 02:00｜第一轮（续）：全量研读蒸馏完成+定向定稿
- **A 设计品味系 7 个**（taste-skill/anti-ui-slop/emil-design-eng/frontend-design/impeccable/ux-feature-design/ui-ux-pro-max）：三强机制=①ux-feature-design 出处化规则+一票否决+用户原声验收（四域命中最高）②ui-ux-pro-max CSV 十列判定表 schema+impeccable antipattern registry 多引擎检测器架构③taste-skill 二值化禁令（模型无视 used sparingly）+机械可数门禁。双副本漂移检查：impeccable/ux-feature-design 两副本一致。笔记=参考Skill/A-设计品味系蒸馏.md
- **B 工作流极简系 10 个**：三强=①出口产物门禁链+GATE caps/ev ②复用五问≡懒人阶梯（两套独立演化同构，交叉验证）③反借口表+危险词触发+单行判定输出。skill-creator 形态规范全套收编（pushy description/三层加载<500 行/例子胜过规则/busywork=过度 prescribing）。grill-me 为壳文件仅形态可借。笔记=参考Skill/B-工作流极简系蒸馏.md
- **C 工具文档系 34 条快扫**：高价值 2（cms-skill-collection=注册表与共识素材源；web-gui-tester=③交互门禁取证执行器）、低 5、无关约 28。笔记=参考Skill/C-工具文档系快扫.md
- **定向定稿** docs/direction.md：四问题域→机制映射表+反借口表 v1（9 条，含 taste-skill 对作者本人的教训「模型无视适度，写零容忍」）+Skill 结构定稿（SKILL.md<500 行+references 四件+scripts 三门禁）+防膨胀三闸+冲突裁决（既有组件优先 vs greenfield 反模板 vs brief 原话永远赢）+第一迭代切片四件
- GATE: {level=L2-F, v=全量研读蒸馏+定向定稿, cmd=Explore×3 分组研读(51 Skill 条目) + 蒸馏笔记×3 + direction.md 落盘, exit=全量覆盖(51/51), files=参考Skill/{A,B,C}×3+docs/direction.md, refs=0(未跑 lookup，0 照报), errpath=skill-creator 用户级路径不存在实为插件 cache（重定位）；grill-me 本体缺失如实标注不可蒸馏, lessons=两套独立演化的 Skill 给出同一条复用链=该链是经过市场验证的成熟形态；模型无视「适度」类措辞——品味规则必须零容忍二元化；判定表两栏分离（业界共识 vs 本 Skill 风格）防风格冒充真理, exempt=Skill 本体未写（下一轮第一迭代切片）, caps=Explore×3（内联纪律包：只读+出处+统一蒸馏格式）, effort=51 Skill 全量研读+3 蒸馏笔记+1 定向档, stop_reason=—}

### 2026-09-21 02:20｜第二轮：本质问题想透（用户追问「究竟解决什么」）
- 用户指出上一轮直接给机制清单、跳过问题定义——想透后补进 direction.md 新增「〇、我们究竟解决什么问题」节
- **问题定义**：每次会话的模型=失忆的局部优化工人，产品=需要对全局负责、持续兑现承诺的有机体；根因=模型与产品的成本结构逐项镜像颠倒（写新便宜vs最贵/复用贵vs最便宜/验证贵vs唯一真实/用户信任0vs一切）；产品=承诺的集合，四个症状统一为「承诺的不兑现/反直觉/冲突/无知」；本 Skill 本质=把兑现义务从交互时前移到生成时
- 三件工具定名：地图（注册表）/厂规（判定表）/验收机（门禁）；反面校验四条（不写抽象原则/不追求模型拥有审美/厂规不写千条/工件必过失忆工人-成本-兑现三重检验）
- 第一迭代验收校准：新增三重检验（失忆工人/成本/兑现——门禁必须能对 classifyNotice 式死代码给 exit 1）
- GATE: {level=L2-S, v=问题定义定稿, cmd=思考+direction.md 修订, exit=〇节落档+四节校准, files=docs/direction.md, refs=0(未跑 lookup，0 照报), errpath=上一轮跳过问题定义直接给机制（用户追问纠正）——机制清单不等于问题定义, lessons=先答「病是什么」再开药；检验 Skill 设计的标准=「下个会话的失忆工人在哪个动作前以多少成本被什么机制强制使用它」, exempt=—, caps=—, effort=三层下挖（症状→能力→结构/承诺）+反面校验四条, stop_reason=—}

### 2026-09-21 02:50｜第三轮：外部同类项目调研（用户：「这个应有同类相似项目，调研研读」）
- WebSearch+web_reader 深读两最直接同类：**Nutlope/hallmark**（Together AI 反 AI-slop 设计技能：四动词 build/audit/redesign/study+20 主题+57 道 slop-test gates+pre-emit self-critique；本地 taste-skill 实为其衍生）+ **vercel-labs/web-interface-guidelines**（862★：100+ 条七类准则+`web-design-guidelines` skill 产出 file:line findings+AGENTS.md 集成）
- 次要发现：awesome-claude-skills 目录群（BehiSecc/travisvn≈8.8k★/ComposioHQ）+rohitg00 toolkit=分发渠道；shadcn registry+MCP、anti-ui-slop、theme-factory（前轮已录）
- **差异化校验：四增量域全部成立**（注册表+出处链/裁决账本写回/逻辑链门禁/纪律对接——同类均空白或仅一句原则）；vercel「品牌 vs 通用」分节=taste-skill em-dash 教训的独立再发现，两栏分离设计被印证
- 并入三修订进 direction.md §六：vercel 列为判定表「业界共识」出处源（No dead ends/All states designed/错误给出路正反例/Don't pre-disable submit 等互补条目）+hallmark audit/study 动词化命令形态+portable design.md 交接范式
- 落档：参考Skill/D-同类项目调研.md+direction.md §六+依据行更新
- GATE: {level=L2-S, v=外部同类调研, cmd=WebSearch×4+mcp web_reader 深读×2仓库+落档, exit=0, files=参考Skill/D-同类项目调研.md+docs/direction.md, refs=0(未跑 lookup，0 照报), errpath=WebFetch github.com TLS 证书拦截（本机拦截环境）→改 mcp web_reader 服务端抓取成功；WebSearch 429 限流×2→换措辞重试成功, lessons=最直接同类（hallmark 57 门禁）只护视觉 slop 不护逻辑链与项目承诺——本 Skill 的「假理想功能门禁+裁决账本」是真空地带；命令动词化（audit/study）比裸脚本更有产品感, exempt=—, caps=WebSearch+mcp__web_reader__webReader, effort=2 仓库深读+4 组搜索+对照表, stop_reason=—}

### 2026-09-21 03:42｜第四轮：用户九问→效力衰减链定稿（direction.md §七）
- 九问（在场没被利用/能力不入计划/压缩失真/被用但只是规范/产出照旧反人类/偷懒怎么达成观念/各态变化/如何补进工作流/揭开什么缺口）逐一归因后收敛为**一条链**：Skill 效力五级衰减——①在场不触发（概率匹配非义务）②计划不引用（规划动作不规划检索）③压缩失真（上下文内终将失真=介质属性）④仪式化合规（读写间无强制函数，「合规靠 hooks 非自觉」实锤）⑤产出照旧（走查 5 缺陷时设计系 Skill 全在场=证据）
- **缺口命名**：现有机制全作用在上下文（劝导生成者），无一作用在交付物（交付时拦截）+结论不复利；劝导会衰减法律不会——Skill=劝导（高带宽/低强制/易衰减），可复跑工件=法律（零带宽/全强制/抗压缩）
- 三附属定稿：偷懒=定价问题非观念问题（给路定价让最便宜的路恰好正确）；态机（greenfield 拦发明/既有拦闲置/会话内拦仪式化/跨会话拦压缩/交付后回写）；工作流缝合三点（计划检索位/GATE cmd 吃门禁真值/收尾账本写回）
- 本体三层与衰减链对齐：判定表治「不知什么是对」/注册表治「不知已有什么」/门禁治「知道也不做」/账本治「做了也白做」
- GATE: {level=L2-S, v=九问缺口定稿, cmd=九问归因+direction.md §七+agent-log+commit, exit=0, files=docs/direction.md+memory/agent-log.md, refs=0(未跑 lookup，0 照报), errpath=Edit agent-log 报 modified（#294 bash heredoc 双通道）→重读实文再改成功, lessons=劝导会衰减法律不会；Skill 与工件是互补介质不是替代品；在场的 Skill 拦不住决策点的先验——只有决策点与交付点之间的机器判定拦得住, exempt=—, caps=—, effort=九问逐环归因+链条命名+对策映射, stop_reason=—}

### 2026-09-21 03:51｜第五轮：工程品味解剖+时序纪律定稿（direction.md §八，PG 原文一手）
- 用户命题「真实交互逻辑应在设计前预设构想，落地时才考虑代码和源库复用」——拉《Taste for Makers》全文（paulgraham.com，web_reader 绕 TLS）逐条对过
- **品味五能力定稿**：①换位提问（炉灶旋钮：问题在错的层面被解决）②识破装饰（「装饰常是说底下没东西的方式」→假功能/内联样式）③丑觉先于美觉（见丑易想象美难→否定性知识=判定表零容忍的理论根据，与 taste-skill 二值化合流）④敢于复用（对>原创）与敢于重画（好设计是重设计，速写=让认错便宜）⑤品味住在作坊不住在个体（佛罗伦萨 vs 米兰→Skill=给失忆工人搭的作坊）
- **时序纪律裁定**：权威序成立（Norman 概念模型/Cooper 目标导向/双钻石+原型即法律实证）；两精确化——①「真实」=态完整（理想路径图=假功能前移到设计层；六态矩阵+承诺清单+失败出路，缺态不得开工）②复用落地执行但代价认知前置（设计读能力索引/落地读组件卡；禁止库的顺手悄悄重写承诺——反人类多是方便累积的）
- 权威序≠瀑布序：设计=宪法/落地=执法/走查=司法审查（证据回写账本反哺下版）
- Skill 后果三条：判定表加「组件驱动设计=一票否决」时序条目+注册表双视图（能力索引/组件卡）+设计档准入六态可数化（设计门禁雏形）
- GATE: {level=L2-S, v=品味解剖+时序纪律定稿, cmd=web_reader 拉 PG 原文+五能力蒸馏+direction §八+agent-log+commit, exit=0, files=docs/direction.md+memory/agent-log.md, refs=0(未跑 lookup，0 照报), errpath=Edit agent-log 再报 modified（#294 heredoc 后未重读）→重读再改成功, lessons=品味可执行部分全是否定性知识（美涌现不可枚举/丑可枚举可判定）；问题在错的层面被解决=无品味的原型症状；反人类设计大多不是决策出来的是方便累积出来的, exempt=联网未多轮（一手文献一轮即定，预算纪律）, caps=mcp__web_reader__webReader, effort=PG 十四条逐条蒸馏为五能力+命题两处严谨化+三条 Skill 后果, stop_reason=—}

### 2026-09-21 04:05｜第六轮：ponytail 上游原仓库深读（用户直供 github.com/DietrichGebert/ponytail）
- 确认=本机 ponytail（单文件 6.7KB）的上游完整产品；本机蒸馏漏掉的四件最值钱：**基准方法论**（同类首个对照实验：真实仓库 12 ticket×n=4 以 git diff 计分——LOC -54%/tokens -22%/cost -20%；裸口号提示 LOC 降但安全掉 95%=白名单条款才是安全来源；single-shot 旧基准 80-94% 被 #126 挑战后公开修正并标注 artifact=诚实测量样本）/**hooks always-on 注入**（UserPromptSubmit+PreToolUse+模式开关=衰减链 1/4 级已验证工程解；20 平台矩阵）/**ponytail: 注释+debt harvest**（裁决账本最小实现样例）/六命令族+check-rule-copies 副本一致性门禁
- 阶梯精确形态补两条：理解问题之后运行（Lazy about solution, never about reading）+「规则不是最少 token，是只写任务需要的且永不砍验证/错误处理/安全/a11y」
- 差异化表修正：账本位非全空白——ponytail-debt 占债务语义（记为何没写），decision-ledger 裁决语义（记为何这么定）仍空白
- 四吸收落档：D 档 §6+direction §四验收升级（agentic 对照）+§八末六条；本机 ponytail-review 为独立 Skill 不在上游命令族内（本机化改动的痕迹，待后考）
- GATE: {level=L2-S, v=ponytail 上游深读, cmd=web_reader 抓仓库全文+本机 ls 对照+D档§6+direction两处+agent-log+commit, exit=0, files=参考Skill/D-同类项目调研.md+docs/direction.md+memory/agent-log.md, refs=0(未跑 lookup，0 照报), errpath=Edit D 档报 not read（#294 压缩后读态丢失）→重读再改成功, lessons=给 Skill 做对照实验是同类首创且可复制（真实 diff 计分+对照组+安全单列）；安全不来自口号来自白名单条款；账本有债务/裁决两种语义；hooks 注入>概率触发, exempt=本机 ponytail-review 与上游关系未深查（B 组已蒸馏其形态，不再重复）, caps=mcp__web_reader__webReader, effort=全文深读+本机副本对照+差异化表修正+四吸收落档, stop_reason=—}

### 2026-09-21 04:09｜第七轮：联通层=中心对象定稿（用户重心校正，direction.md §九）
- 用户校正「不是重复造轮子定义组件怎么写，而是定义产品设计与交互层的真正联通——不难用不难看、更好用更好看的交互逻辑怎么来怎么做」
- 接受依据：§一四问题域中①③④全属联通层仅②注册表在组件域——重心确歪，此校正=聚焦非转向
- **§九 定稿**：中心对象=功能语义↔交互逻辑的可判定契约；**双底双顶**（不难用/不难看=底线法律可门禁；更好用/更好看=上限劝导靠判定表+critic——现有调研素材按四象限整齐归位=定稿旁证）；**来源三合法**（用户心智最强源：惯例=预装交互逻辑，反人类高发机制=迫使用户为你的实现学新交互／功能语义推导／红线约束；非法源：组件库存、模型感觉、酷）；**功能天生六问**（输入什么/何时发生/成功长啥样落哪/失败怎么办出路/能否反悔/下次还认吗→逐问落交互原语=翻译表；六问=提问轴×六态=渲染轴不重复）；**联通工序**（功能句→翻译表→承诺清单+六态矩阵→spec-trace 双向门禁→走查→回写账本；真联通=双向可追溯+机器可验，文档联通=假联通）
- 重心修正落地：注册表降位（落地兑现查询基础设施）；§三增 references/interaction-bridge.md；§四切片 1 改联通层路由+bridge 骨架；触发词改「难用/丑/交互逻辑怎么来」
- 过程自检：Edit direction 误删 §八末两段（old_string 整段替换）→当场发现原样恢复——教训=追加场景禁用「整段替换」式 old_string，锚标题行即可
- GATE: {level=L2-S, v=联通层中心定稿, cmd=校正归因+direction §九+§三/§四联动+agent-log+commit, exit=0, files=docs/direction.md+memory/agent-log.md, refs=0(未跑 lookup，0 照报), errpath=Edit 误删两段（old_string 过宽）→恢复成功并留教训, lessons=中心对象必须是「可判定契约」不是「领域知识」；惯例=预装在用户脑里的交互逻辑（用惯例=零学习成本）；六问是提问轴六态是渲染轴——平行分类法先查轴是否正交再入库, exempt=—, caps=—, effort=校正归因+四象限定稿+六问推导法+工序链, stop_reason=—}

### 2026-09-21 04:16｜第八轮：联通层定向补扫（用户「继续查同类项目」，D 档 §7）
- 四组搜索+spec-kit 深读（web_reader）：**github/spec-kit**（官方 spec-driven：constitution→specify→plan→tasks→implement→converge 三过程+verdict 三态+工件落盘 .specify/+多 agent）——与本 Skill 最同构的业界形态：宪法=厂规形态、converge=正向追溯门禁同类、what/why 先于 how=时序纪律官方版；缺口=通用 spec 无交互域内容、单向收敛无反向发明检测、无品味无账本
- **Figma Code Connect**：design↔code 组件级映射官方工程化（映射文件+属性映射+Figma MCP）——「映射文件」模式被市场验证；层级差异=组件级静态 vs 我们行为级契约，互补
- **设计系统 lint 群**：Atlassian 官方 ESLint plugin/eslint-plugin-panda no-hardcoded-color/案例（401 组件 144 违规全源自粘贴代码）——证明 inline-style-gate=业界共识非首创，差异化校准
- **Nielsen×agent 学术线**：arXiv 2026-05 CUA 重审 10 启发式——真渲染取证路线学术共振；Nielsen 列为判定表出处源（direction §六已补）
- **结论：联通层组合仍无人占**——spec-kit 管通用 spec 不交互域/Code Connect 管组件不管行为/lint 管样式不管逻辑链；无 direction 实质修订
- GATE: {level=L2-S, v=联通层定向补扫, cmd=WebSearch×4+web_reader 深读 spec-kit+D档§7+direction§六增补+commit, exit=0, files=参考Skill/D-同类项目调研.md+docs/direction.md+memory/agent-log.md, refs=0(未跑 lookup，0 照报), errpath=WebFetch github.com TLS 拦截（既往）→web_reader 成功, lessons=门禁②业界已成熟（诚实降级：非首创）；映射文件模式被 Code Connect 市场验证；converge 循环+verdict 三态可借给门禁输出；真联通组合空白依旧, exempt=Code Connect 仅浅读（映射形态已清楚，预算纪律）, caps=WebSearch+mcp__web_reader__webReader, effort=4 组搜索+1 仓库深读+差异化最终校准, stop_reason=—}

### 2026-09-21 04:26｜第九轮：职责再收窄+真强制清单+能力地图+缺口登记（direction.md §十，用户两问定稿）
- 用户校正：主题/组件一概不定义（registry=纯检查者），唯一职责=规定「这个功能应怎么来」；「先检查再二次开发、可复用不完全复制」双重纪律（对模型+对 Skill 本体）；点名缺口=Skill 检索能力地图（工作流×产品工程互补路由层）；ponytail 对工作流有新补充；两问=真强制哪些+未意识到的新缺口
- **强制判据**：可机器判定+决策/交付点拦截+成本检验（执行成本<防止的返工）——八项入选（六问无空格/六态缺态不开工/spec-trace 双向/查表归因/内联样式零容忍/dead-binding/取证存在性/账本写回存在性）；其余全降劝导裁决级（双上限=判定表+critic；三合法=裁决表；阅读义务/反借口=hook 危险词半自动）；防仪式爆炸=强制清单自身过成本检验宁缺毋滥
- **能力地图**：references/capability-map.md，行=动作时点×症状→能力→出口产物；harvest 机制防地图腐化（无人维护的地图=第二个失忆）；工作流计划模板增检索位
- **新缺口五项**：①同层 Skill 冲突无裁决（优先序：底线门禁>流程纪律>品味裁决）②豁免梯度缺（借 ponytail 模式分级，否则 L1 被六问淹没→糊弄温床）③出路活性缺（exit-existence gate 候选：出路指向死页查不出——dead-binding 姊妹件）④触发回归缺（测试集+N 口语命中统计）⑤用户验收面缺（联通行三列表=功能→交互→证据，spec-trace 用户可见形态）
- **工作流回补四条**（ponytail 侧）：hooks 模式开关+subagent 注入正则/debt harvest 形态/agentic 对照基准（治合规不可测）/命令族化——待用户择期实施
- GATE: {level=L2-S, v=强制边界+能力地图+缺口登记定稿, cmd=两问归因+direction §十+§三结构增 capability-map+agent-log+commit, exit=0, files=docs/direction.md+memory/agent-log.md, refs=0(未跑 lookup，0 照报), errpath=—, lessons=强制与劝导的分界线=可机器判定×成本检验；registry 的正确角色是检查者不是定义者；无人维护的地图=第二个失忆（工件需要 harvest 机制）；豁免梯度不是松懈是防糊弄, exempt=—, caps=—, effort=强制筛分八项+缺口挖潜五项+能力地图 schema, stop_reason=—}
