# 下区生成模板

填写全部方括号，先运行 layout 得到比例。一般输入照片和一张最相关参考即可。分别填写钢笔与炭笔两个版本；提示词仅用于内部工作，不作为交付物。

```text
Use case: stylized-concept
Output ONLY an architectural sketch panel, target aspect [width:height]. Do not include the photograph in the output.
Image 1 is the sole content reference: [building]. Image 2 provides only mark-making guidance: [filename and qualities]. Never copy the reference building.
Analysis: [mass hierarchy]. Actions: [1-3 actions]. Preserve anchors: [2-4 anchors]. Omit [surface detail].
Highly abstract exploratory first concept sketch, gestural freedom comparable to the supplied Gehry references, purposeful searching restrokes, economical open contours. Not a traced elevation, realistic drawing, or edge-detection filter. Use the photograph as a starting point for gestures, not a silhouette to reproduce. Preserve the essential compositional tensions while freely stretching, compressing, shifting or omitting local shapes. Do not complete outlines to increase resemblance. Match the approved examples' lively searching movement, sparse-to-dense variation and fragmentary small studies.
EXCLUSIVELY [black fountain pen / charcoal]. [specific mark behavior]. The same medium for every mark in all three studies. No mixed medium, colors, wash, watercolor, marker, or brush ink.
One dominant main sketch, approximately 70% of drawing content, plus TWO subordinate small studies grouped below: mass grouping [content], and [action/void/site relation]. Main view broadly follows source. Small studies simplify visible relationships, never invent hidden plans or construction facts. Exactly three studies; natural asymmetrical spacing, no panel boxes.
Uniform pale ivory #F5F1E8 paper, extremely subtle texture, generous untouched paper. Black and natural gray marks only. No aged stains, vignette, shadows, borders, binding, tools or mockup.
No text, letters, numbers, annotations, signatures, dates, logos or watermarks. [specific avoidance].
```

纠偏最多两轮：太写实则去掉窗格阴影并用动作组织主稿；乱线则重申锚点、减回环；混合画材则重新生成单画材；主次不清则明确一大两小、两小图用途不同；纸底脏则重申平整米白，不强阈值抹除铅笔细线。

使用工具真实参数，模板中的 aspect 不是 API 字段。先看原始手绘，再规范化与拼版，原始图与验证材料留在交付目录外；最终只交付一张拼合图及钢笔、炭笔两张独立稿。



炭笔版填写 specific mark behavior 时采用：
Use the supplied 隈研吾 reference ONLY for charcoal mark-making, not its building. Broad dry side-of-charcoal bands with visible grain, naturally changing width and pressure within a stroke; decisive black masses alternating with clean paper gaps and softer gray bands. Think in masses and voids, with few thin auxiliary marks. Do not trace an ink sketch with thicker lines. Follow the input's angular or curved construction rather than forcing circular stacked forms. No watery wash, uniform gray shading or mixed media.
钢笔版不使用这段；两种画材各自加载对应标尺。
