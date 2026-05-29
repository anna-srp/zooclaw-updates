---
title: "PPT Master Agent 升级至 2.0.8，生成画质提升至 1080p"
type: "Agent 上架/更新"
priority: "高"
date: "2026-05-28"
status: "待审核"
channels: ""
---

# PPT Master Agent 升级至 2.0.8，生成画质提升至 1080p

## 核心宣传点

PPT Master 生成的演示文稿分辨率从 720p 提升至 1080p（1920×1080），输出质量显著提升，画面更清晰锐利。

## 原始内容

feat(pptx-master): upgrade to 2.0.8 — 1080p canvas + sidebar-only wireframe (#152)

Canvas upgrade 1280x720 -> 1920x1080 across all pipelines: new bundled marp theme-1080p.css with mandatory --theme-set workflow; output-html coordinate system / template_mirror / thumbnail clone+scale / fidelity page dimensions all updated to 1080p. Wireframe simplified to sidebar-only (patch_wireframe.py v0.6.17 -> v0.6.18).

PR Summary: Upgrades the PPT Master pack (pptx-master/) from the deployed 2.0.7 to 2.0.8. Canvas upgrade 1280×720 → 1920×1080 (16:9) across all pipelines: Marp new bundled theme-1080p.css; SKILL.md documents the mandatory --theme-set artifacts/theme-1080p.css render workflow.
