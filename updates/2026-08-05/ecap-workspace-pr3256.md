---
title: "修复会话页「停止」按钮点击无效"
type: "Bug Fix"
priority: "中"
date: "2026-08-05"
status: "待审核"
channels: ""
---

# 修复会话页「停止」按钮点击无效

## 核心宣传点

新版会话页的「停止」按钮真正生效，重复点击也不会刷屏出现多余的控制消息。

## 原始内容

- 仓库：`SerendipityOneInc/ecap-workspace`
- Commit：`95ff913000b24275338e4417aa123d4906729a4c`
- 作者：kaka-srp
- 日期：2026-08-05T09:46:27Z
- PR：#3256

### Commit Message

```
fix(chat): stop v2 session thread generation (#3256)

## Summary

- wire the v2 session-thread Stop button to a tagged Mattermost `/stop`
reply
- hide only button-generated control posts from the ECAP transcript
while keeping manually typed `/stop` messages visible
- latch a successful stop request for the current generation so repeated
UI or runtime abort calls do not create duplicate posts; failed sends
remain retryable

## Root cause

The v2 session-thread page passed a no-op abort handler to the shared
chat runtime and input. Unlike the direct-chat page, it therefore never
emitted the `/stop` command consumed by the channel control path.

## Performance

- the hidden-post check stays inside the existing memoized single-pass
post filter
- stop deduplication is an in-memory ref with no timer, polling, or
additional read request
- ACS authorization uses the already loaded managed-v2 session tuple and
adds no Mattermost or database call

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] related Vitest suite — 4 files and 80 tests passed
- [x] TypeScript and ESLint checks
- [x] `git diff --check`

## Companion change

- https://github.com/SerendipityOneInc/agent-channel-service/pull/60
```

### PR Body

## Summary

- wire the v2 session-thread Stop button to a tagged Mattermost `/stop` reply
- hide only button-generated control posts from the ECAP transcript while keeping manually typed `/stop` messages visible
- latch a successful stop request for the current generation so repeated UI or runtime abort calls do not create duplicate posts; failed sends remain retryable

## Root cause

The v2 session-thread page passed a no-op abort handler to the shared chat runtime and input. Unlike the direct-chat page, it therefore never emitted the `/stop` command consumed by the channel control path.

## Performance

- the hidden-post check stays inside the existing memoized single-pass post filter
- stop deduplication is an in-memory ref with no timer, polling, or additional read request
- ACS authorization uses the already loaded managed-v2 session tuple and adds no Mattermost or database call

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] related Vitest suite — 4 files and 80 tests passed
- [x] TypeScript and ESLint checks
- [x] `git diff --check`

## Companion change

- https://github.com/SerendipityOneInc/agent-channel-service/pull/60

