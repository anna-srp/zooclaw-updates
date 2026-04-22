---
title: "性能优化：聊天背景图 880KB→31KB，首屏更快"
type: "体验优化"
priority: "低"
date: "2026-04-22"
status: "待审核"
channels: ""
---

# 性能优化：聊天背景图 880KB→31KB，首屏更快

## 核心宣传点

聊天页背景图从 880KB JPEG 压缩为 31KB WebP，首屏加载速度显著提升（LCP 优化）。

## 原始内容

fix(web): replace 880KB JPEG bg-pattern with 31KB WebP to fix LCP (#1135)

LCP fix: panda-claw chat background pattern was a 1638×914 external JPEG (417KB light / 467KB dark) loaded on every /chat page visit. Replaced with optimized 31KB WebP, improving Largest Contentful Paint by ~93%.
