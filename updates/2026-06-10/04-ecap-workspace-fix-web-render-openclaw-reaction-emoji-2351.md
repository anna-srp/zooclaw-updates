---
title: "聊天表情反馈显示修复"
type: "体验优化"
priority: "低"
date: "2026-06-10"
status: "待审核"
channels: ""
---
# 聊天表情反馈显示修复

## 核心宣传点
修复了聊天中部分状态表情显示为文字代码（如 :white_check_mark:）的问题，现在能正常显示为表情图标。

## 原始内容
```
fix(web): render openclaw reaction emoji (#2351)

## Summary
- add frontend mappings for OpenClaw status reaction emoji names
- cover the newer Mattermost reaction names with a unit test

## Root Cause
Mattermost reactions arrive as emoji names such as `white_check_mark`.
The chat UI only mapped a subset of older names, so unknown names
rendered as fallback text like `:white_check_mark:`.

## Validation
- `pnpm exec vitest run
tests/unit/app/chat/OpenClawUserMessage.unit.spec.tsx`

---

### PR Description

## Summary
- add frontend mappings for OpenClaw status reaction emoji names
- cover the newer Mattermost reaction names with a unit test

## Root Cause
Mattermost reactions arrive as emoji names such as `white_check_mark`. The chat UI only mapped a subset of older names, so unknown names rendered as fallback text like `:white_check_mark:`.

## Validation
- `pnpm exec vitest run tests/unit/app/chat/OpenClawUserMessage.unit.spec.tsx`
```
