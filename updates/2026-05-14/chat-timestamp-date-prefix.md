---
title: "聊天消息时间戳新增日期前缀"
type: "产品基础功能更新"
priority: "低"
date: "2026-05-14"
status: "待审核"
channels: ""
---
# 聊天消息时间戳新增日期前缀

## 核心宣传点

非今天的历史消息现在会显示日期（如"5月10日, 09:05"），不再只显示时分，帮你一眼区分今天和历史消息。

## 原始内容

**Commit**: d82918ca5c | feat(web): Show date prefix on chat timestamps not from today (#1633)

**Commit Message**:
```
feat(web): Show date prefix on chat timestamps not from today (#1633)
```

**PR Body**:
## Summary

- `formatMessageTime` now renders `HH:MM` for messages sent today and `MMM D, HH:MM` for messages from any other day, locale-aware via `Intl`.
- Extracted the previously-duplicated helper out of `OpenClawUserMessage` and `OpenClawAssistantMessage` into `web/src/app/[locale]/chat/lib/formatMessageTime.ts`.
- Threaded the app locale (`useLanguage().locale`) into the helper so the rendered date/time respects the user-selected app locale instead of the browser's default. E.g. a user with an English browser who picked Chinese UI now sees `5月10日, 09:05` instead of `May 10, 09:05`.
- Added a focused unit test covering the today / not-today / locale / seconds-vs-ms branches.

## Test plan

- [x] `pnpm lint` clean
- [x] `tsc --noEmit` clean
- [x] `pnpm test:unit` — all 4599 tests pass
