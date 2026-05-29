---
title: "修复切换对话时 Canvas 画布版本号未重置的问题"
type: "Bug Fix"
priority: "低"
date: "2026-05-28"
status: "待审核"
channels: ""
---

# 修复切换对话时 Canvas 画布版本号未重置的问题

## 核心宣传点

在 Canvas 模式下切换到不同对话后，自动保存功能现在能正确重置状态，避免因版本号混乱导致的画布数据异常。

## 原始内容

fix(canvas): reset versionRef on session change too (#2051)

Symmetric reset fix for the useCanvasPersistence hook. The bug: clearCanvas (same-session "start over") explicitly calls resetVersion() to zero the autosave version counter. The session-change reset effect did not. So on session A (versionRef = N) → session B with no saved canvas, reset effect fires → clears nodes/edges + onReset(), but does not call resetVersion(), causing autosave version counter mismatch.
