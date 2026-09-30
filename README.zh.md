[English](README.md) | 中文

# product-engineering · 产品工程 Skill

把「做一个 XX 页面 / 工具 / 应用」钉成**可判定契约**——层级门、产品六问、statechart、机器可查的验收门禁——让「演示」与「产品」的差距是被验证的，而不是被假设的。

交付形态 = 一份 [SKILL.md](SKILL.md)（agent 遵循的跑道）+ 九台带自测的门禁脚本（机器可查切片）。

## 它查什么

| 脚本 | 一行角色 |
|---|---|
| `statechart-gate` | 每个态都有出路：无死端、全可达、错误态有恢复转换、契约双向对账（C1–C7） |
| `spec-trace-gate` | 三方绑定追溯 页面↔组件↔后端↔证据：孤儿、死逻辑、幽灵端点（T1–T6） |
| `product-object-gate` | 产品对象在档：主功能恰好一个、层级声明+上游引用、可运营性有答案（P1–P4） |
| `l0-l5-gate` | 目标合格线+信息架构底线：可度量北极星、带时间窗 KR、导航三件套、无死端页（L0/L5） |
| `registry-gate` | 新组件必须带归因标记（`registry: … source=…` 或自研理由）；基线模式豁免存量 |
| `frontend-lint-gate` | 组件区禁内联样式 / 硬编码色 / `console.*` / 空 catch；列表页要有空态分支（R1–R5） |
| `a11y-gate` | 可达性静态底线：`img` alt、表单控件与图标按钮可访问名、`html` lang（A1–A4） |
| `spec-trace-extract` | 从代码提取组件/端点清单，喂给 `spec-trace-gate` |
| `usage-probe` | 统计 agent 日志中的技能提及——衰减监控 |

## 安装

```bash
npx skills add zxc663/product-engineering-skill
```

## 运行

每台门禁独立可跑、自带自测：

```bash
python scripts/statechart-gate.py --file sc.json --contract contract.json
python scripts/frontend-lint-gate.py --path src/components --write-baseline   # 基线豁免存量、只拦新增
python scripts/l0-l5-gate.py --goal goal.json --ia ia.json
```

九台全测：`python scripts/<gate>.py --selftest`

## 工作方式

- [SKILL.md](SKILL.md)——八步跑道：层级门 → 六问 → statechart → 风险定档 → 实现 → 验收。
- [references/](references/)——细节层：判定表、层级栈、产品对象、联通层、契约 schema 等，按需加载。
- `scripts/`——上述机器门禁。检测刻意停在正则级：低误报，存量项目走基线接入。

## 诚实边界

- 门禁查的是**形态不是语义**：statechart 过了检不等于它是对的。结构检查与领域评审缺一不可。
- `a11y-gate` / `frontend-lint-gate` 是低误报静态子集——不是 axe-core，不是完整 lint 配置。
- 基线模式（`--write-baseline`）让存量项目接入便宜（存量豁免、新增必拦）——重构后须重建基线。
- Skill 对 agent 行为是**概率护栏**，不是保证。
- 本仓检查**英文工件**（判定词表为英文）。中文项目请用中文源包 [`shisan-xinuo-product`](https://github.com/zxc663/shisan-xinuo-workflow)（机制同源，词表为中文）。

## 参与

规则只写规则本身 + 至多一句为什么。每台脚本改动必须带 `--selftest` 覆盖，且含反向样本（每个绕过形态都要有能抓住它的测试）。

## License

[MIT](LICENSE)
