---
title: "修复：Agent 激活/重新激活流程更加稳定"
type: "Bug Fix"
priority: "中"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# 修复：Agent 激活/重新激活流程更加稳定

## 核心宣传点

修复了 Agent 首次启动和重新激活时行为不一致的问题，确保每次启动都能正确完成初始化流程。

## 原始内容

**Commit**: `63fa7ffc0d604d1087ae831779bb9695522b329b`
**仓库**: ecap-workspace
**作者**: nolan-srp
**时间**: 2026-04-28T07:17:58Z

### 完整 Commit Message

```
fix(claw-interface): normalize openclaw agent activation (#1433)

## Summary
- send `Hi` for both newly hired and re-hired OpenClaw agents so
onboarding runs consistently
- allow custom agent archive downloads in pod runtime to follow HTTP
redirects for signed object storage URLs
- add focused unit coverage for the activation message and
redirect-enabled download script behavior
```

### PR #1433 完整描述

## Summary
- send `Hi` for both newly hired and re-hired OpenClaw agents so onboarding runs consistently
- allow custom agent archive downloads in pod runtime to follow HTTP redirects for signed object storage URLs
- add focused unit coverage for the activation message and redirect-enabled download script behavior
