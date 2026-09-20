# Agent 工作日志（一档制）

> 权威承载 = 本文件｜开工必读状态段

## 一、状态段

STATE: task=产品工程 Skill 立项——骨架+全量本机 Skill 蒸馏+定向+外部同类项目调研（已齐） | level=L2-F | route=四问题域三件工具（地图=注册表/厂规=判定表/验收机=门禁）+裁决写回闭环；同类对照确认四增量域无人覆盖 | confirm=无需 | gates_passed=—（本体未动工） | last_errpath=WebFetch github.com 本机 TLS 证书拦截→改 mcp web_reader 服务端抓取（成功）
- 当前阶段：**调研全部完成（2026-09-21）**，待用户点名开工第一迭代切片（SKILL.md 骨架→anti-excuses.md→registry-gate→三重检验验收）
- 任务级别：L2-F
- 本机环境：Windows+ZCode；WebFetch 对 github.com 证书验证失败（本机 TLS 拦截），外部仓库深读走 mcp web_reader
- 最近更新：2026-09-21 02:50
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
