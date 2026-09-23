# 工作流 Skill 漏洞账本（2026-09-24 战役立）

> 范围：shisan-xinuo-workflow 家族（核心/flows/roles/product）+ 其运行时依赖（平台 CLI/hooks/注入链）。用户指令「同步检查工作流Skill的漏洞」的产出物。
> 处置纪律：**确凿漏洞**（死引用/自相矛盾/脚本坏/事实性失效）→ 修复（源库+安装根双同步，改前备份）；设计层争议 → 只记账待裁决。每条带证据 file:line。

## 发现清单

| # | 严重度 | 症状 | 证据 | 处置 | 状态 |
|---|---|---|---|---|---|
| F1 | 高（无人值守入口失效） | ZCode CLI 无法独立启动：缺 built-in provider 配置，报「无法定位 CLI ZCode Built-in Provider Config」两路路径均不存在；手工补造需从应用存储取密钥材料=红线禁止 | 实测 2026-09-24 01:47：`node zcode.cjs --version`→0.16.9 OK；无参启动→报错退出（NR1/evidence 前终端截图）；`resources/glm/provider/` 目录不存在；env 名 `ZCODE_BUILTIN_PROVIDER_BUNDLED_CONFIG_FILE`/`ZCODE_BUILTIN_PROVIDER_CONFIG_FILE`（zcode.cjs 内 grep 实证） | 平台侧缺陷（非 Skill 本体）；影响=CLI 场景（CI/无人值守/真会话自动化）全部走 GUI；Skill 文档若引用 CLI 工作流须标注「当前平台版本不可用」 | 🟡 记账（平台问题，Skill 侧防御性标注待排） |

## 系统体检（2026-09-24 01:55 实测）

| 项 | 结果 | 证据 |
|---|---|---|
| ① product 包回指实存性 | ✅ 全实存（references 9 件+scripts 5 件；跨包 skill-usage.md 在核心包实存） | ls 实测；注意首轮 for+[ -f ] 输出全 MISSING 为沙箱假象（规律=仅末项 OK），已用 ls 直取真值排除——**本机 shell 验证一律 ls 目录取地面真值，禁信复合循环 test 输出** |
| ② 五门禁 selftest | ✅ 5/5 PASS（01:52） | product-object/registry/spec-trace/statechart/usage-probe `--selftest` rc=0 |
| ③ product 源库 vs 安装根 | ✅ 仅 decision-ledger.md 1 件漂移（与 HANDOVER 队列⑩一致，无意外漂移） | diff -rq 实测 |
| ④ 核心包回指实存性 | ✅ references 9 件全实存（details.md 132KB 等） | ls 实测（for+[ -f ] 假象同①排除） |
| ⑤ 核心包 5 脚本可跑性 | ✅ 5/5 `--help` rc=0 | agent_log_rotate/detail_lookup/gate_audit/risk_scan/syncer |
| ⑥ ZCode CLI 独立启动 | ❌ 见 F1 | 实测报错 |

> 阶段结论（01:55）：家族本体无死引用、脚本全可跑、双副本仅 1 件已登记漂移——**纪律层健康；真正缺口在「真实会话证据链」（NR1 进行中）与平台工具链（F1）**。

