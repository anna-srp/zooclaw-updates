---
title: "前端素材大小自动管控（pre-commit + CI 双重拦截）"
type: "产品基础功能更新"
priority: "低"
date: "2026-04-19"
status: "待审核"
channels: ""
---

# 前端素材大小自动管控（pre-commit + CI 双重拦截）

## 核心宣传点

新增素材大小自动检查机制：commit 时自动压缩图片，超出阈值的大文件会被 CI 拦截，避免大图拖慢前端加载速度。

## 原始内容

feat(ci): block oversized assets with pre-commit hook and CI gate (#1039)
阈值：PNG/JPG 500KB · WebP 300KB · GIF 1MB · MP4（见文档）
