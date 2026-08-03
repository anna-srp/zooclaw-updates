---
title: slide-master 幻灯片 Agent：品牌配色自动守护可读性
type: Agent 上架/更新
priority: 中
外部: "B"
date: 2026-07-27
status: 待审核
channels: ""
---

## 核心宣传点

slide-master（幻灯片制作 Agent）升级：当你指定自己的品牌主色时，它现在会在保持色相不变的前提下自动微调明度/饱和度，确保文字和图形在页面上始终清晰可读；如果某个品牌色实在无法满足对比度要求，会给出明确的报错和调整提示，而不是默默生成一份看不清的深浅撞色幻灯片。

## 原始内容

**Pack**: slide-master　**版本**: 0.4.1 → 0.4.2

**关键改动文件**:

- `agent-pack.yaml`：版本号 0.4.1 → 0.4.2
- `scripts/deck_tokens.py`：`load_style()` 新增 `clamp_brand: bool = True` 参数。当开启时，用户显式提供的品牌 accent 会经过 W2「保色相包络 + 对比度守护」finalize；显式提供的 `accent2` / `chart_highlight` 保持原样。新增 `BrandContrastError`（当品牌 accent 无法满足 W2 palette-safety 契约时抛出，payload 含 role / failing_check / ratio / archetype / original_hex / clamped_hex / final_attempted_hex / hint）。新增 HSL 工具：`_hsl_to_hex`（HSL→确定性小写 #rrggbb）、`_hue_sep`（最小圆周色相分离度）、`_clamp_once` / `_clamp_into`（保色相地把明度/饱和度夹紧到包络安全的 8-bit 值，含 QUANT_EPS 量化边界处理）。`load_style` 在检测到用户提供了 `accent` 时，按 `provided_color_roles` 调用 `_finalize_brand_accents`。

**用户视角变化**：品牌色现在被"安全地"采纳——保留你想要的色相，但自动保证与背景/文字的对比度达标；无法达标时明确报错而非静默出坏图。属 slide-master Agent 的常规能力迭代。
