---
title: "修复 Artifact 内容更新后仍显示旧版本的问题"
type: "Bug Fix"
priority: "低"
date: "2026-05-21"
status: "待审核"
channels: "Discord, changelog"
---

# 修复 Artifact 内容更新后仍显示旧版本的问题

## 核心宣传点

Agent 生成新版内容后，预览窗口现在会及时刷新显示最新结果，不再卡在旧版本。

## 原始内容

```
fix(web): bust browser cache for artifact iframe when content changes (#1805)

Add cache-busting mechanism to artifact iframe URL so browser refreshes content when the underlying artifact is updated, instead of showing stale cached version.
```
