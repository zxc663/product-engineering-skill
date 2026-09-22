# 产品工程母架构与定位边界

> 2026-09-23 立档（用户三条裁决：定位加边界+母架构路线 / 四档风险矩阵 / 三件契约 schema）。
> 依据：docs/three-definitions.md（三定义加固版）+ 用户附呈三方讨论（2026-09，硬层/软层、schema、风险自适应、先跑高风险闭环）。

## 一句话定位

`shisan-xinuo-product` 是一个 **Product Interaction Engineering（交互工程）包**——Product Contracts 规范层的**第一垂直域**，已落地；母架构的其余域**均未实现**。

## 母架构：Product Contracts

```
Product Contracts（规范层）
├── Intent Contract            ← 为什么做（问题/目标/用户/场景/范围）        未实现
├── Scope Contract             ← 做什么/不做什么                          未实现
├── Structure Contract         ← 信息架构/对象模型/功能地图                未实现
├── Interaction Contract       ← 用户怎么完成（六问+态+转换）              ★ 已落地
├── Runtime Contract           ← 真实世界怎么运行（网络/权限/并发/持久）    未实现
├── Implementation Contract    ← 现有工程能力怎么实现（registry/capability） 部分（查询基础设施）
└── Verification Contract      ← 怎么证明兑现（验收/证据/追溯/回归）        支撑件（Gate/Evidence）
```

- **已落地的三件**= Interaction / Gate / Evidence 的字段 schema → `skill/shisan-xinuo-product/references/contract-schema.md`（本体，随家族主仓发行）。
- **硬层/软层分界**：态/转换/权限/恢复/证据=硬层（机器可验，exit 1）；意图/权衡/被否候选=软层（可追溯，落裁决账本）。**禁全链 JSON 化**——讨论已定：为填表而填表=Token 爆炸。
- **迭代次序**（讨论定稿，用户已认）：第二版 Intent/Structure（IA）→ 第三版 Runtime；每一版只在拿到实测证据后落字段。

## 与家族的分工

```
用户需求 → [产品工程] 什么叫做对（判据来源与继承）→ [工作流] 怎么做到/怎么证到 → 代码 → GATE → 实机证据 → 裁决回写
```

- 工作流 = 纪律系统（行为连续性：我们做过什么）；产品工程 = 判断系统（产品连续性：我们为什么这样做）。
- 谁来做（虚拟团队/PM/UX/QA）= 另一层，与规范层**组合不竞争**——前提是本包给出稳定 schema（本轮已给出三件）。

## 叙事修正（2026-09-23）

- 原表述「结构层**蓝海**」→ 现表述「**一个尚未形成成熟统一范式的工程层**：不证明无人做，只补生态缺的『统一、可执行、可验证的桥接层』」。
- 理由（讨论定稿）：蓝海叙事不可证伪且易招质问；「缺一个统一抽象」是可工程验证的命题。受影响处：README、SKILL.md §定位、参考Skill/H 档（**只读不改**，历史研究笔记保留原表述）、direction §九（已加注）。

## 战略目标与最大风险

- **目标**：建立让 AI Agent 能**消费、执行、验证、继承** Product Contracts 的规范层；本包是第一套实现。
- **最大风险**：把自己做成第二个 Workflow（更多表/门禁/checklist）——防法=强制清单宁缺毋滥（README 设计纪律）+ 元规则六问（direction §〇）+ 本轮「未落地域不写字段」。
- **第二风险**：正确但昂贵——防法=四档风险矩阵（默认不全开）+ 硬/软层分界。

## 待办（回指 three-definitions.md §8）

- [x] 高风险特征闭环实验载体已定（新建独立工作区 D:/产品工程闭环实验/）→ 协议档 = docs/closed-loop-experiment-protocol.md（含反向注入检验；实跑下一迭代）
- [ ] A/B 四指标口径冻结（defect_escape / rework / coverage / cost；什么算「遗漏状态」需先定义）
- [ ] 「缺失可检出」判据清单归拢（现状=statechart-gate 候选 + spec-trace 反向 + 九条强制清单）
