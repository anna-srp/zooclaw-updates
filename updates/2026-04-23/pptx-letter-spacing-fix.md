---
title: "PPTX 预览修复：文字间距现在正确渲染"
type: "Bug Fix"
priority: "低"
date: "2026-04-23"
status: "待审核"
channels: "Discord+changelog"
---
# PPTX 预览修复：文字间距现在正确渲染

## 核心宣传点
修复了 PPTX 幻灯片预览中文字间距（letter-spacing）不正确的问题，含自定义字符间距的幻灯片现在显示正常。

## 原始内容
fix(web): render OOXML run-level spc (letter-spacing) in PPTX preview (#1204)

PptxRenderer parsed paragraph-level spacing but ignored run-level `spc` (letter-spacing), causing text to display with incorrect character spacing.
