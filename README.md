# 硕士毕业论文工作区

本项目用于 CAPANet 轻量级图像超分辨率课题的资料管理、实验和硕士毕业论文撰写。

## 目录结构

```text
catanet_pfa/
├── README.md                     # 项目入口与资料索引
├── .gitignore                    # 编辑器、Python、LaTeX 临时文件规则
├── thesis/                       # 毕业论文正文
│   └── README.md                 # 写作与文件存放约定
├── proposal/                     # 开题材料
│   └── 开题报告.md
├── research/                     # 课题研究与实验资料
│   ├── method/                   # 创新点、模块说明、实现方案
│   └── experiments/              # 实验设计、执行流程、结果记录
├── references/                   # 参考文献与阅读资料
│   ├── papers/                   # 文献原始 PDF
│   ├── extracted/                # 从文献提取的文本
│   └── notes/                    # 阅读笔记、参考论文实验数据
├── assets/
│   └── figures/                  # 开题报告与毕业论文共用配图
│       ├── README.md             # 配图说明
│       ├── 效果图清单.md
│       ├── 效果图生图提示词.md
│       ├── drawio/               # 可编辑图源
│       ├── svg/                  # SVG 矢量图
│       ├── png/                  # PNG 图片
│       └── archive/              # 已有幻灯片提取图片
└── CAPANet/                      # 模型代码与实验配置
    ├── .gitignore                # 数据集、权重、训练输出规则
    ├── basicsr/
    ├── options/
    ├── tests/
    ├── datasets/
    └── pretrained_models/
```

## 资料索引

| 用途 | 文件 |
| --- | --- |
| 毕业论文写作 | [写作目录说明](thesis/README.md) |
| 开题报告 | [开题报告](proposal/开题报告.md) |
| 研究创新点 | [创新点](research/method/创新点.md)、[创新点实现方案](research/method/创新点实现方案.md) |
| 模块设计 | [三大模块详解](research/method/三大模块详解.md)、[DPR 模块独立实现方案](research/method/DPR模块独立实现方案.md) |
| 实验规划与执行 | [实验设计](research/experiments/实验设计.md)、[全流程](research/experiments/全流程.md) |
| 实验结果文档 | [实验结果](research/experiments/实验结果.md) |
| 文献原文与提取文本 | [CATANet PDF](references/papers/CATANet.pdf)、[CATANet 文本](references/extracted/catanet_text.txt)、[PFT 文本](references/extracted/pft_text.txt) |
| 文献阅读与选型 | [CATANet 介绍](references/notes/catanet介绍.md)、[DPR 模块 baseline 论文列表](references/notes/DPR模块baseline论文列表.md) |
| 参考论文实验数据 | [Baseline 实验数据](references/notes/Baseline实验数据.md)、[Baseline 消融实验数据](references/notes/Baseline_Ablation实验数据.md) |
| 配图资料 | [配图目录说明](assets/figures/README.md)、[效果图清单](assets/figures/效果图清单.md)、[效果图生图提示词](assets/figures/效果图生图提示词.md) |
| 训练与测试代码 | [CAPANet 使用说明](CAPANet/README.md) |

两份 Baseline 数据文档汇总的是参考论文中的结果，存放在 `references/notes/`。本课题的实验设计、执行流程与结果文档存放在 `research/experiments/`。

## 文件存放约定

- 毕业论文正文及其 `.tex`、`.bib`、Markdown、Word、最终 PDF 文件放在 `thesis/`；开题材料放在 `proposal/`。
- 新增参考论文 PDF 放在 `references/papers/`，提取文本放在 `references/extracted/`，阅读笔记放在 `references/notes/`。
- 方法设计资料放在 `research/method/`，实验说明、整理后的结果表和实验记录放在 `research/experiments/`。
- 配图源文件和用于正文的导出图片统一放在 `assets/figures/` 对应格式目录。各份文稿通过相对路径引用。
- 在项目根目录执行 `cd CAPANet` 后运行训练与测试命令；数据集和权重路径按实际运行环境填写。

## Git 管理约定

正文、文献、整理后的实验数据、代码、配置和配图均可纳入 Git。Python 缓存、LaTeX 编译中间文件、下载的数据集、模型权重和训练输出由两份 `.gitignore` 忽略。

需要用于论文的实验表格或效果图，应从 `CAPANet/experiments/`、`CAPANet/results/` 或 `CAPANet/output/` 整理到 `research/experiments/` 或 `assets/figures/`，再纳入版本管理。最终 PDF、PNG、SVG、Draw.io、CSV 和 Excel 文件不会按扩展名被全局忽略。

本地 `.trae/` 中的写作技能保留原位置，由根目录规则忽略；其中独立仓库的 Git 元数据不会混入论文仓库。
