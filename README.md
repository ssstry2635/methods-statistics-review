# 研究方法与统计审查

本项目面向对照、独立样本单位、样本流和结果报告复核。校验工具接受已经转录且明确适用范围的输入，能复算样本流和百分比，并检查数值区间、p 值范围与分析单位。原文定位按来源 ID 和行区间核对，报告保留参与计算的数值及其派生结果。

## 适用场景

使用实际稿件和问题清单开展可定位的审查或文献阅读核对。研究判断由使用者或加载本 Skill 的 Agent 完成。Python 标准库工具负责来源哈希、原文短引核对及声明过的计算规则，无需网络和密钥。

## 快速运行

需要 Python 3.10 或更新版本。从仓库根目录执行以下命令。

```bash
python scripts/verify.py examples/input.json --root examples --out output/report.json
```

示例显示 100 入组减去 5 个互斥排除应为 95，与报告的 94 有差异。1/13 报告成 7.7% 符合精度。对重复读数的模型处理未知，因此推断仍待检查。 所附材料均为虚构样例，用于证明接口和程序行为。

## 输入与输出

`sources` 给出 `id`、`path`，可选原文件路径和预期 SHA-256。`checks` 的每条记录需要 `id`、`kind`、`scope`、`anchors` 与 `applicable`。`sample_flow` 需要入组、互斥排除和分析数量。`percentage` 需要分子、分母、报告值与小数位数。`p_range`、`interval_order` 和 `unit_independence` 的输入见脚本。材料不足可填 `applicable: false` 和 `reason`。

原文锚点含 `source_id`、从 1 开始且包含端点的 `start`、`end`，以及区间内的 `quote`。文本文件可来自对 PDF 的带页码转录。可记录 `original_path` 和 `original_sha256`，让报告能回到实际原件。输入源根目录通过 `--root` 声明。若文件不可读、引文不存在或请求字段非法，工具将返回非零退出码和错误报告。

## Agent 使用方式

让 Agent 加载 [SKILL.md](SKILL.md)，提供研究问题、材料路径、检查范围和预期输出。保留原文页码或图表定位，将核心数值或声明整理成可执行输入，读回校验报告，再完成科学判断。对每个检查项给出证据、适用范围、具体行动以及仍需核实的事项。

## 项目结构与验证

- `SKILL.md` 说明阅读、组织证据与交付流程。
- `scripts/verify.py` 执行本项目特有的检查。
- `scripts/evidence.py` 处理 UTF-8 原文、路径、行区间和来源哈希。
- `examples/` 保存独立复跑的虚构材料。
- `tests/` 覆盖关键计算、证据和边界行为。

运行 `python -B -m unittest discover -s tests -v` 复核。更新逻辑或评分规则时同步修订说明和样例。形式或数值检查通过后仍应以原文、研究设计与实际评分口径为准。
