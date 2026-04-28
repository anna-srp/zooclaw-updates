---
title: "功能上新弹窗升级：新增 PPTX Master 展示"
type: "产品基础功能更新"
priority: "中"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# 功能上新弹窗升级：新增 PPTX Master 展示

## 核心宣传点
打开 ZooClaw 时弹出的「新功能上新」弹窗升级为多页轮播，现在可以同时介绍多个新功能，新增了 PPTX Master 的展示页。

## 原始内容
**Commit**: feat(chat): 功能上新弹窗支持多 slide 轮播，新增 PPTX Master 上新 (#1315)  
**PR Body**:  
把现有的 Seedance 上新弹窗从单一功能展示，改成支持任意数量功能上新的通用轮播弹窗。新增 PPTX Master 作为第二张 slide。核心重构：SeedanceLaunchModal → FeatureLaunchModal，内容改成 data-driven 的 SLIDES 数组，后续加第3/4个功能上新只要往数组里加一条。新增多媒体类型支持（视频+图片），轮播导航（Next/Previous/Got it），indicator dots 居中对齐。新增 storage key ECAP:feature-launch-seen。
