# 本轮任务包：毕业论文计划清单

日期：2026-11-21。

## 任务范围

依据现有开题报告、方法资料、实验记录和配图，为中文硕士毕业论文生成可执行清单。沿用已有研究问题与 CAPANet 技术路线，并提出章节结构和验收条件。

## 输入资料

- `proposal/开题报告.md`。
- `research/method/` 中的创新点、实现方案、DPR 方案和三大模块说明。
- `research/experiments/实验设计.md`、`实验结果.md`、`全流程.md`。
- `references/notes/` 中的 CATANet、DPR 和两份 Baseline 笔记。
- `assets/figures/效果图清单.md`及已有配图文件清单。
- `CAPANet/basicsr/archs/capanet_arch.py`、训练 YAML 和已有测试代码中的配置覆盖信息。
- 用户已明确的硕士论文类型，以及整理时“保留全部原文件”的约束。

## 文件写入范围

仅新增 `thesis/plan/` 下的项目概览、大纲、计划清单、进度记录和本任务包。

## 使用技能

`research-writing-assistant`、`using-research-writing`、`paper-orchestration`、`brainstorming-research`、`experiment-results-planning`、`verification`。

头脑风暴模块用于检查研究范围与结构信息：已明确的信息从用户请求和开题资料提取；未知格式、期限和正式结构列入计划。本轮不生成正文，不创建章节文件。

## 必须产出

- `project-overview.md`：题目、研究问题、已有材料、当前证据状态和约束。
- `outline.md`：六章建议结构、资料依据和完成条件。
- `毕业论文计划清单.md`：按优先级与依赖关系组织的可勾选任务。
- `progress.md`：阶段判断、两阶段检查、能力使用记录和待验证项。
- 本任务包。

## 验收与拒收条件

- 每项任务具有唯一编号，能勾选，并说明可检查的动作。
- 核心研究内容与开题报告的 DPR / PFSA / LMR 一致。
- 明确已有结果表包含数值；不把本轮未复现的记录标为验证通过。
- 包含来源核验、训练初始化、严格消融结构、指标口径、配图、写作、审阅和答辩准备。
- 截止日期和学校模板不凭空确定。
- 不写模拟性能数字，不新增无来源文献，不声称已完成正文。
- 原有文件不存在删除、覆盖或内容变更。
- 本轮为规划交付，不触发整篇正文生成或多代理分章写作。

## 检查命令

```bash
python3 /tmp/verify_thesis_plan.py
git diff --check
```

该检查核对现有文件哈希、五份规划文件、相对链接、任务编号和章节安排；不用于证明实验结果或学校格式已经通过验收。
