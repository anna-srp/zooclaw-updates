---
title: "Mattermost 附件支持直接预览（无需下载）"
type: "产品基础功能更新"
priority: "中"
date: "2026-04-21"
status: "待审核"
channels: "站内弹窗+Discord"
---

# Mattermost 附件支持直接预览（无需下载）

## 核心宣传点

在 Mattermost 消息中收到 PDF、PPTX、Word、Excel 等文件附件时，点击即可在侧边栏内联预览，无需下载到本地。同时大幅修复 PPTX 渲染质量（中文字体、形状、动画等）。

## 原始内容

feat(web): preview Mattermost attachments + pptx rendering fixes (#1125)

- Preview MM attachments inline: clicking a previewable file attachment (pdf / xlsx / docx / pptx / html / md / code / ...) on a Mattermost message now opens the artifact preview side panel
- Bot-sent attachments auto-open like today's in-text artifact URLs
- pptx renderer overhaul: fixes text BiDi, CJK font fallback, shape geometry (custGeom paths, prstGeom presets), border alpha, layout overflow
- Force correct MIME on MM blob URLs
