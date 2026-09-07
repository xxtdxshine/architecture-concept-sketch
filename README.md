# Architecture Concept Sketch · 建筑概念手绘

把建筑照片或效果图转译为自由、抽象的大师式概念手稿，分别生成钢笔稿和炭笔稿，并择优与完整原图拼成 3:4 竖版。

Turn architectural photographs or renderings into expressive, abstract concept sketches in fountain pen and charcoal, then pair the stronger sketch with the intact source image in a 3:4 portrait composition.

## 中文简介

本 skill 先分析体量、构成动作、虚实与场地关系，再以开放轮廓、试探复线和有依据的形变表达构想。照片提供构成起点，不要求逐边描摹或完全复现最终建筑。

- **钢笔稿**：自由长线、回折与疏密变化，参考用户认可的概念稿与盖里手绘的表达方法。
- **炭笔稿**：宽厚侧锋、干燥颗粒、浓黑与留白交替，参考本地隈研吾命名图片的视觉笔触。
- 每稿均为一幅主稿与两幅不同用途的构成小图；每张只使用一种画材。
- 拼合图为 1800 × 2400 PNG，上方原图完整等比例缩放、通栏无边框，下方米白手稿直接衔接。
- 每次仅交付三张图片：成图.png、钢笔稿.png、炭笔稿.png。

### 使用

将本目录放入个人 skills 目录，保留 references 和 scripts 的相对结构。在支持该 skill 的 Codex 环境中提供图片并输入：

> 使用 $architecture-concept-sketch 处理这张建筑照片。

运行环境需要内置图像生成工具、Python 3 和 Pillow。图像生成负责草图；程序负责拼版及原图像素验证。脚本本身不会生成手绘。

## English overview

The skill identifies massing, compositional movements, solids and voids, and site relationships before developing exploratory sketches. The photograph is a conceptual starting point rather than a silhouette to trace.

- **Fountain pen:** open contours, searching restrokes, long gestures, and varied line density.
- **Charcoal:** broad dry side strokes, visible grain, and decisive dark bands separated by clean paper.
- Each medium produces one main sketch and two smaller studies with distinct analytical purposes.
- The final composition is a 1800 × 2400 PNG. The source image is proportionally resized without cropping or retouching, fills the top edge to edge, and meets the ivory sketch panel directly.
- Exactly three images are delivered: one composite, one standalone pen panel, and one standalone charcoal panel.

### Usage

Place this folder in your personal skills directory, retaining its internal structure. In a compatible Codex environment, attach an architectural image and ask:

> Use $architecture-concept-sketch to create concept sketches from this architectural image.

Requires the built-in image generation tool, Python 3, and Pillow. Image generation creates the sketches; the Python script handles composition and verifies preservation of the resized photograph.

## Files · 文件

- SKILL.md — workflow and delivery rules / 工作流程与交付规则
- references/ — style guidance, reference images, and source notes / 风格、参考图与来源说明
- scripts/compose.py — composition and verification / 拼版与验证
- scripts/test_compose.py — composition regression checks / 拼版回归检查

## Reference notes · 参考说明

Reference filenames reflect the supplied labels, not authenticated authorship or medium identification. Generated examples are AI-created style benchmarks, not original works by the named architects. See references/sources.md and references/reference-catalog.md for provenance notes. Third-party reference images retain their respective rights; no ownership or blanket license is claimed for them.

参考图文件名不代表对作者、项目或原画材的鉴定；生成样例是 AI 风格标尺，不是大师原作。来源信息见 references/sources.md 与 references/reference-catalog.md。第三方图片的权利归原权利人所有，本仓库不主张其所有权或统一授权。
