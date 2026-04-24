---
title: "PPTX 预览修复：OOXML 表格现在正常渲染"
type: "Bug Fix"
priority: "中"
date: "2026-04-22"
status: "待审核"
channels: "Discord+changelog"
---

# PPTX 预览修复：OOXML 表格现在正常渲染

## 核心宣传点

修复含真实表格数据的 PPTX 幻灯片预览空白问题，现在所有 OOXML 表格都能正确显示。

## 原始内容

feat(web): render pptx OOXML tables (graphicFrame > a:tbl) (#1149)

Slides with real OOXML tables (<p:graphicFrame> containing <a:tbl>) previously rendered a blank region where the table should be. Now correctly parses and renders all OOXML table types in the PPTX viewer.
