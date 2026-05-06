# DPR模块灵感来源论文列表

本文档按与本课题 `DPR` 模块的相关程度，对参考论文进行重新划分。这里的判断标准不是“是否属于超分辨率论文”本身，而是这些论文是否能够直接支撑当前 `DPR` 的核心设计，即：

- 动态语义组织
- token 分组与归属
- 候选集合构造
- 路由元信息向后续模块传递

## 一、DPR主谱系来源论文

这部分论文与本课题 `DPR` 的设计链条最直接相关，可作为核心灵感来源。

### 1. SPIN

- 论文名：`Lightweight Image Super-Resolution with Superpixel Token Interaction`
- 年份：`2023`
- 出处：`ICCV 2023`
- 链接：https://openaccess.thecvf.com/content/ICCV2023/html/Zhang_Lightweight_Image_Super-Resolution_with_Superpixel_Token_Interaction_ICCV_2023_paper.html
- 核心机制：
  - 使用 `superpixels` 聚类局部相似像素，形成可解释的局部区域；
  - 使用 `intra-superpixel attention` 做组内信息交互；
  - 使用 `superpixel cross-attention` 做组间信息传播。
- 对 DPR 的启发：
  - 提供了“先按内容相似性分组，再进行交互”的基础范式；
  - 可直接对应 `DPR` 中的内容组织与候选区域构造思想。

### 2. ATD-SR

- 论文名：`Transcending the Limit of Local Window: Advanced Super-Resolution Transformer with Adaptive Token Dictionary`
- 年份：`2024`
- 出处：`CVPR 2024`
- 链接：https://arxiv.org/html/2401.08209v2/
- 核心机制：
  - 引入 `Adaptive Token Dictionary` 作为外部先验；
  - 使用 `Token Dictionary Cross-Attention (TDCA)` 增强输入特征；
  - 使用 `Adaptive Category-based Attention` 将图像 token 按类别分组，再做注意力建模。
- 对 DPR 的启发：
  - 强化了“动态先验 + 类别分组 + 自适应交互”的思想；
  - 对 `DPR` 中 token 的动态归属与路由组织具有直接参考价值。

### 3. CATANet

- 论文名：`CATANet: Efficient Content-Aware Token Aggregation for Lightweight Image Super-Resolution`
- 年份：`2025`
- 出处：`CVPR 2025`
- 链接：https://openaccess.thecvf.com/content/CVPR2025/html/Liu_CATANet_Efficient_Content-Aware_Token_Aggregation_for_Lightweight_Image_Super-Resolution_CVPR_2025_paper.html
- 核心机制：
  - 使用 `Content-Aware Token Aggregation (CATA)` 聚合长程内容相似 token；
  - 使用组内自注意力与组间交叉注意力建模远距离相似区域之间的关系。
- 对 DPR 的启发：
  - 是本课题最直接的过渡参考论文；
  - 已证明“内容感知 token 组织”有助于提高跨区域相似信息利用效率；
  - 本课题在其基础上进一步从“内容聚合”推进到“语义动态路由”。

## 二、DPR机制增强参照论文

这部分论文不是 `CATANet` 的严格直系谱系，但对 `DPR` 的部分关键机制有较强支撑作用。

### 4. HSNet

- 论文名：`HSNet: Heterogeneous Subgraph Network for Single Image Super-resolution`
- 年份：`2025`
- 出处：`arXiv 2025`
- 链接：https://arxiv.org/html/2510.06564v1
- 核心机制：
  - 使用 `Constructive Subgraph Set Block` 构造多种异构子图；
  - 使用 `Subgraph Aggregation Block` 融合多子图表示。
- 对 DPR 的启发：
  - 与 `DPR` 中“将 token 组织为候选交互集合”的思想非常接近；
  - 可作为“异构候选集合构建 / 图式分组建模”的重要参考。

### 5. MambaIRv2

- 论文名：`MambaIRv2: Attentive State Space Restoration`
- 年份：`2025`
- 出处：`CVPR 2025`
- 链接：https://openaccess.thecvf.com/content/CVPR2025/html/Guo_MambaIRv2_Attentive_State_Space_Restoration_CVPR_2025_paper.html
- 核心机制：
  - 提出 `attentive state-space equation`；
  - 引入 `semantic-guided neighboring mechanism`，促进远距离但内容相似像素之间的交互。
- 对 DPR 的启发：
  - 与 `DPR` 中“组织 distant but similar tokens”目标高度一致；
  - 可作为“语义引导邻域构造”方向的重要参考。

## 三、DPR辅助参照论文

这部分论文不能直接作为 `DPR` 的主来源，但可用于支撑动态先验、层级组织、结构先验或多范围依赖建模等相关设计。

### 6. PromptSR

- 论文名：`PromptSR: Cascade Prompting for Lightweight Image Super-Resolution`
- 年份：`2025`
- 出处：`arXiv 2025`
- 链接：https://arxiv.org/html/2507.04118v1/
- 核心机制：
  - 使用 `Global Anchor Prompting Layer (GAPL)` 构造全局锚点提示；
  - 使用两个 `Local Prompting Layers (LPLs)` 做局部细化；
  - 结合 `category-based self-attention` 与窗口注意力，完成由全局到局部的级联引导。
- 参考价值：
  - 更适合作为“全局先验引导局部交互”的辅助参考；
  - 不能直接替代 `DPR` 的候选集合构造逻辑。

### 7. UCIP

- 论文名：`UCIP: a Universal Framework for Compressed Image Super-Resolution Using Dynamic Prompt`
- 年份：`2024`
- 出处：`ECCV 2024`
- 核心机制：
  - 通过 `dynamic prompt` 适配不同压缩退化条件；
  - 将输入条件转化为动态可调的恢复先验。
- 参考价值：
  - 可作为“动态先验生成”方向的重要参照；
  - 更适合支撑 `DPR` 中的“输入自适应先验”思想，而非路由本体。

### 8. PFRNet

- 论文名：`Lightweight Image Super-Resolution Via Superpixel Prior and Feature Reinforcement`
- 年份：`2025`
- 出处：`Journal of Research in Science and Engineering`
- 链接：https://bryanhousepub.com/index.php/jrse/article/view/2082
- 核心机制：
  - 使用 `superpixel segmentation` 提供结构先验；
  - 结合 `local attention aggregation` 和 `global structure modeling`；
  - 通过多模块完成结构一致的特征增强。
- 参考价值：
  - 与 `SPIN -> CATANet` 的 `superpixel/content grouping` 路线较近；
  - 适合作为较弱的 superpixel-aware 辅助参考。

### 9. HiT-SR

- 论文名：`HiT-SR: Hierarchical Transformer for Efficient Image Super-Resolution`
- 年份：`2024`
- 出处：`ECCV 2024`
- 参考链接：https://www.semanticscholar.org/paper/HiT-SR%3A-Hierarchical-Transformer-for-Efficient-Zhang-Zhang/e422f85a0a0850b9531e3637718fa99b784160e2
- 核心机制：
  - 使用 `expanding hierarchical windows` 进行多尺度信息组织；
  - 建模不同粒度窗口中的空间与通道关系。
- 参考价值：
  - 适合支撑 `DPR -> PFSA -> LMR` 中“先组织再交互”的层级化设计；
  - 但并非显式路由模型。

### 10. MAT

- 论文名：`MAT: Multi-Range Attention Transformer for Efficient Image Super-Resolution`
- 年份：`2025`
- 出处：`2025 IEEE TCSVT / arXiv 2025`
- 链接：https://arxiv.org/html/2411.17214
- 核心机制：
  - 引入 `multi-range attention` 与 `sparse multi-range attention`；
  - 在不同空间范围内建立依赖关系。
- 参考价值：
  - 可作为“多范围依赖组织”方向的补充参考；
  - 更适合支撑 `PFSA` 或后续多范围交互分析，而不是 `DPR` 本体。

## 四、不建议作为DPR直接灵感来源的论文

这部分论文与 `DPR` 的直接关联较弱，更适合放在轻量化背景、部署背景或待核实候选中，而不建议写成 `DPR` 的直接灵感来源。

### 11. ASID

- 论文名：`Efficient Attention-Sharing Information Distillation Transformer for Lightweight Single Image Super-Resolution`
- 年份：`2025`
- 出处：`AAAI 2025`
- 链接：https://arxiv.org/abs/2501.15774
- 原因：
  - 其核心在于高效注意力共享与蒸馏；
  - 更适合支撑“轻量预算下模块设计”的效率背景；
  - 不建议写成 `DPR` 的直接机制来源。

### 12. MambaLiteSR

- 论文名：`MambaLiteSR: Image Super-Resolution with Low-Rank Mamba using Knowledge Distillation`
- 年份：`2025`
- 出处：`arXiv 2025`
- 链接：https://arxiv.org/html/2502.14090
- 原因：
  - 其重点在于 `Low-Rank Mamba`、知识蒸馏与边缘部署效率；
  - 更适合支撑轻量级与部署目标，不适合支撑 `DPR` 的路由设计。

### 13. Tokenized Dynamic Embedding Network

- 论文名：`Lightweight image super-resolution with tokenized dynamic embedding network`
- 年份：`2025`
- 出处：`Knowledge-Based Systems`
- 链接：https://dblp.org/rec/journals/kbs/ZhuLW25.html
- 原因：
  - 当前主要依据标题判断其方向；
  - 公开可获得的信息不足，难以确认其是否能直接支撑 `DPR` 的动态路由或候选集合构造；
  - 现阶段更适合作为待核实候选，而不是直接来源。

## 建议引用顺序

如果写作中需要突出 `DPR` 的来源链条，建议优先按以下顺序组织：

1. `SPIN`
2. `ATD-SR`
3. `CATANet`
4. `HSNet`
5. `MambaIRv2`

其中：

- `SPIN + ATD-SR + CATANet`：构成 `DPR` 的主谱系来源
- `HSNet + MambaIRv2`：构成 `DPR` 的机制增强参照

## 建议用法

- 如果强调 `DPR` 的“内容组织与动态分组”：
  - 优先引用 `SPIN`、`ATD-SR`、`CATANet`
- 如果强调 `DPR` 的“候选集合构造 / 异构关系建模`：
  - 优先引用 `HSNet`
- 如果强调 `DPR` 的“远距离相似 token 组织能力`：
  - 优先引用 `CATANet`、`MambaIRv2`
- 如果强调 `DPR` 的“动态先验生成`：
  - 优先引用 `ATD-SR`、`UCIP`
- 如果强调 `DPR` 的“层级组织或后续协同建模基础`：
  - 优先引用 `HiT-SR`、`MAT`
- 如果强调 `DPR` 的“轻量部署合理性`：
  - 可补充引用 `ASID`、`MambaLiteSR`，但不建议作为核心灵感来源
