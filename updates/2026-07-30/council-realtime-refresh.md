---
title: "Council 调研：运行状态实时刷新"
type: "新功能上线"
priority: "中"
外部: "B"
date: "2026-07-30"
status: "待审核"
channels: ""
---

## 核心宣传点

Council 调研进度现在实时更新——各模型完成情况即时呈现，无需手动刷新即可看到最新调研状态。

## 原始内容

**Commit**: c1d4619d (PR #3160)
**外部评级**: B | **内部**: P2 | **信息类型**: 新功能上线

### Commit Message

```
feat(council): refresh runs from thread activity (#3160)

## Summary

- subscribe to Mattermost activity for the persisted Council run thread
- coalesce websocket activity into the existing status refresh path with
a shared three-second throttle
- keep bounded backoff polling as the safety net, with a higher ceiling
while the socket is connected

## Stack

- Depends on #3158
- Review after #3157 and #3158
- This slice intentionally excludes thread-history synthesis rendering

## Verification

- `bash scripts/verify-web.sh web/app/src/hooks/council
web/app/src/hooks/queries/council web/app/src/hooks/useMattermost.ts
web/app/src/lib/council web/app/src/lib/mattermost/post-status.ts
web/app/tests/unit/hooks/council
web/app/tests/unit/hooks/queries/council web/app/tests/unit/lib/council`
- TypeScript passed
- 270 selected tests passed
- ESLint passed
```

### PR Body

## Summary

- subscribe to Mattermost activity for the persisted Council run thread
- coalesce websocket activity into the existing status refresh path with a shared three-second throttle
- keep bounded backoff polling as the safety net, with a higher ceiling while the socket is connected

## Stack

- Depends on #3158
- Review after #3157 and #3158
- This slice intentionally excludes thread-history synthesis rendering

## Verification

- `bash scripts/verify-web.sh web/app/src/hooks/council web/app/src/hooks/queries/council web/app/src/hooks/useMattermost.ts web/app/src/lib/council web/app/src/lib/mattermost/post-status.ts web/app/tests/unit/hooks/council web/app/tests/unit/hooks/queries/council web/app/tests/unit/lib/council`
- TypeScript passed
- 270 selected tests passed
- ESLint passed

