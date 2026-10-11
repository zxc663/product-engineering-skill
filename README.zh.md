[English](README.md) | 中文

# product-engineering · 产品工程 Skill

把「做一个 XX 页面 / 工具 / 应用」钉成**可判定契约**——层级门、产品六问、statechart、机器可查的验收门禁——让「演示」与「产品」的差距是被验证的，而不是被假设的。

交付形态 = 一份 [SKILL.md](SKILL.md)（agent 遵循的跑道）+ 九台带自测的门禁脚本。每台检查器自带反向测试——信任它之前，先验证它。

## 为什么

当 agent 说「做完了」，没有任何东西去核验那些真正要紧的主张：

- **演示能跑，产品不行。**错误态、空态、死端、发明出来的端点，只在真实用户撞上时才暴露——那时 agent 已经转身走了。
- **「看起来做完了」不是裁决。**没有机器可判的验收标准，评审就退化成反复读文档然后祈祷。
- **复杂度会走私进代码。**内联样式、死代码、空 catch、伪按钮（绑了 click 的 `div`）都能混过每一次随意的扫视。

本技能把产品工程里反复出现的主张做成**可判定的**，再用脚本去判定。判不了的主张（语义、品味、真实可达性）明说并交给人工——门禁只查**形态**，这正是机器裁决拥有最终发言权的那一层。

## 它查什么

九台脚本、五套编号规则族——**C / T / P / R / A**——每条规则都可追溯到一台门禁断言：

| 脚本 | 一行角色 |
|---|---|
| `statechart-gate` | 每个态都有出路：无死端、全可达、错误态有恢复转换、契约双向对账（C1–C7） |
| `spec-trace-gate` | 三方绑定追溯 页面↔组件↔后端↔证据：孤儿、死逻辑、幽灵端点、文件型证据存在性（T1–T7） |
| `product-object-gate` | 产品对象在档：主功能恰好一个、层级声明+上游引用、可运营性有答案（P1–P4） |
| `l0-l5-gate` | 目标合格线+信息架构底线：可度量北极星、带时间窗 KR、导航三件套、无死端页（L0/L5） |
| `registry-gate` | 新组件必须带归因标记（`registry: … source=…` 或自研理由）；基线模式豁免存量 |
| `frontend-lint-gate` | 组件区禁内联样式 / 硬编码色 / `console.*` / 空 catch；列表页要有空态分支（R1–R5） |
| `a11y-gate` | 可达性静态底线：`img` alt、表单控件与图标按钮可访问名、`html` lang（A1–A4） |
| `spec-trace-extract` | 从代码提取组件/端点清单，喂给 `spec-trace-gate` |
| `usage-probe` | 统计 agent 日志中的技能提及——衰减监控 |

## 安装

```bash
npx skills add zxc663/shisan-xinuo-product-en
```

## 运行

每台门禁独立可跑、自带自测：

```bash
python scripts/statechart-gate.py --file sc.json --contract contract.json
python scripts/frontend-lint-gate.py --path src/components --write-baseline   # 基线豁免存量、只拦新增
python scripts/l0-l5-gate.py --goal goal.json --ia ia.json
python scripts/spec-trace-gate.py --file bindings.json --components comps.txt --backends backends.txt
```

九台全测：`python scripts/<gate>.py --selftest`

检查器**审计自己**：每份 `--selftest` 都带正反两向样本——每个已知绕过形态都有能抓住它的测试。抓不住自己盲区的检查器不出厂。基线模式（`--write-baseline`）让存量项目接入便宜：存量豁免、新增必拦。

## 工作方式

- [SKILL.md](SKILL.md)——八步跑道：层级门 → 六问 → statechart → 风险定档 → 实现 → 验收。
- [references/](references/)——细节层：判定表、层级栈、产品对象、联通层、契约 schema 等，按需加载。
- `scripts/`——上述机器门禁。检测是确定性的静态形态检查：低误报，存量项目可增量接入。

## 诚实边界

- 门禁查的是**形态不是语义**：statechart 过了检不等于它是对的。结构检查与领域评审缺一不可。
- `a11y-gate` / `frontend-lint-gate` 是低误报静态子集——不是 axe-core，不是完整 lint 配置。
- 重构后须重建基线。
- 本仓检查**英文工件**（判定词表为英文）。中文项目请用中文源包 [`shisan-xinuo-product`](https://github.com/zxc663/shisan-xinuo-workflow/tree/main/skill/shisan-xinuo-product)（机制同源，词表为中文）。

## 出处

- **机制权威**：[`shisan-xinuo-product`](https://github.com/zxc663/shisan-xinuo-workflow/tree/main/skill/shisan-xinuo-product)——中文源包（`zxc663/shisan-xinuo-workflow` 仓 `skill/shisan-xinuo-product/`）对机制拥有权威。
- 本仓为 **clean-room 英文发行版**：政策上机制等价、措辞独立成文；两条版本线各自独立（英文 1.x，中文源 0.2.x）。
- 同步策略见 [AGENTS.md](AGENTS.md)：门禁或规则变更时两版同改，或注明分叉。

## 参与

规则只写规则本身 + 至多一句为什么。每台脚本改动必须带 `--selftest` 覆盖，且含反向样本（每个绕过形态都要有能抓住它的测试）。

## License

[MIT](LICENSE)
