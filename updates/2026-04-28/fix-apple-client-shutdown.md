---
title: "修复：iOS/Mac 客户端连接关闭时资源正确释放"
type: "Bug Fix"
priority: "低"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# 修复：iOS/Mac 客户端连接关闭时资源正确释放

## 核心宣传点

修复了平台关闭时 Apple 客户端连接未正常释放的问题，提升系统稳定性。

## 原始内容

**Commit**: `0a916b37e1dc2edae8319a06ef7e930a1a226cac`
**仓库**: ecap-workspace
**作者**: nolan-srp
**时间**: 2026-04-28T11:40:46Z

### 完整 Commit Message

```
fix(claw-interface): close Apple clients on shutdown (#1445)

## Summary
- close AppleService API clients during application shutdown so
underlying aiohttp sessions are released
- add AppleService close helpers that handle SDK close methods and
session fallbacks
- cover the shutdown path and client cleanup behavior with focused unit
coverage
```

### PR #1445 完整描述

## Summary
- close AppleService API clients during application shutdown so underlying aiohttp sessions are released
- add AppleService close helpers that handle SDK close methods and session fallbacks
- cover the shutdown path and client cleanup behavior with focused unit coverage

