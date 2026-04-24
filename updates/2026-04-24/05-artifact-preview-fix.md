---
title: "修复：重新生成同名 Artifact 时预览不刷新"
type: "Bug Fix"
priority: "中"
date: "2026-04-24"
status: "待审核"
channels: ""
---
# 修复：重新生成同名 Artifact 时预览不刷新

## 核心宣传点
修复了一个 bug：让 AI 重新生成同名文件时，预览窗口还显示旧版本内容。现在会实时刷新，看到的就是最新版本。

## 原始内容

fix(web): refresh preview iframe when artifact file identity changes (#1252)

When the model regenerates a same-name artifact, ArtifactPreview's iframe stayed frozen on the cached old HTML. Fix: refresh cacheBuster when file identity changes.
