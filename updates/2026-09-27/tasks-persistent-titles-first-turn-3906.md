---
title: "修复：任务标题改为首轮对话自动生成，不再显示截断的原始 Markdown"
type: "Bug Fix"
priority: "中"
date: "2026-09-27"
status: "待审核"
channels: ""
---

# 修复：任务标题改为首轮对话自动生成，不再显示截断的原始 Markdown

## 核心宣传点

以前从引擎创建的任务从来不会生成标题，侧栏和 Tasks 页面只能拿首条消息的前 80 个字符当标题，Markdown 符号、长链接全都直接露出来。现在首轮对话结束时会在后台（不阻塞）请求一次标题并落库：生成成功后标题保持稳定，手动改过的名字始终优先。只含链接或清洗后为空的首轮消息统一显示「Shared content」，这样切走会话后任务依然能在列表里看到，也不会把链接地址暴露出来；真正的空消息保持未命名。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

Engine tasks created their chat transport without ever invoking title generation, so the sidebar and Tasks page fell back to the first 80 characters of raw message Markdown. This adds a nonblocking, first-turn title request for writable task conversations and persists the result in their existing record. Reads use attachment-aware fallback text; successful generated titles stay stable, and manual names always take precedence. Nonempty first turns that clean down to nothing (including URL-only messages) use `Shared content`, keeping those tasks visible after switching conversations without exposing URL destinations; truly empty messages remain untitled.

The title action resolves the canonical session and original stored thread through the existing ownership boundary. Atomic fallback/attempt checks prevent duplicate generation and protect concurrent renames/archives. Failed generation keeps the readable fallback, with a five-minute retry cooldown on later visits. Naming does not change activity timestamps. The browser refreshes the sidebar, task detail and `/tasks`, and patches the current conversation title without rebinding its transport.

Validation:
- URL-only title/history regression: reproduced the disappearance before the fix; all 79 focused task-title/history tests pass. Coverage includes both history-list paths, saved URL fallback titles, generation success/failure, unlabeled links/attachments, and empty messages. Ruff, formatting, Pyright, and import contracts passed.
- Backend regression checks passed for first-turn extraction, attachment/link normalization, canonical-to-original mapping, concurrent generation, rename/archive races, failure/cooldown, ownership, external/Build exclusion and route scope. Existing session-channel service/repository/schema tests also passed (65 tests).
- Frontend title lifecycle, cache refresh, navigation isolation and legacy workspace tests passed; TypeScript, ESLint, Ruff, Pyright and import contracts passed.
- Playwright with the local mock: sent a first task message and verified the same generated title in the sidebar, chat header and `/tasks`. Mock inference is deterministic; real generation is exercised via service tests with a stubbed existing title provider.

Requires backend and frontend deployment (backend first). Existing tasks receive generated titles when opened; this does not bulk-backfill historical tasks. Credit usage is unchanged. Staging's encrypted Mongo client was unavailable here: the new classic single-collection CAS passes the query guard, but actual encrypted-client validation remains a release gate.

A fallback response gets at most two five-second follow-ups, so a concurrent tab can observe the winning generation. Navigation cancels those checks, and generated/manual titles stop them. Regression tests cover successful completion, exhausted follow-ups and cancellation; no unbounded polling or repeat inference is introduced.



## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `d35f4fd293d9a31a04e02915497fc0fb82224862`
- PR: #3906
- 作者：Nemo Feng
- 日期：2026-09-27T04:16:41Z

### Commit Message

```
fix(tasks): generate persistent titles from the first turn (#3906)

Engine tasks created their chat transport without ever invoking title
generation, so the sidebar and Tasks page fell back to the first 80
characters of raw message Markdown. This adds a nonblocking, first-turn
title request for writable task conversations and persists the result in
their existing record. Reads use attachment-aware fallback text;
successful generated titles stay stable, and manual names always take
precedence. Nonempty first turns that clean down to nothing (including
URL-only messages) use `Shared content`, keeping those tasks visible
after switching conversations without exposing URL destinations; truly
empty messages remain untitled.

The title action resolves the canonical session and original stored
thread through the existing ownership boundary. Atomic fallback/attempt
checks prevent duplicate generation and protect concurrent
renames/archives. Failed generation keeps the readable fallback, with a
five-minute retry cooldown on later visits. Naming does not change
activity timestamps. The browser refreshes the sidebar, task detail and
`/tasks`, and patches the current conversation title without rebinding
its transport.

Validation:
- URL-only title/history regression: reproduced the disappearance before
the fix; all 79 focused task-title/history tests pass. Coverage includes
both history-list paths, saved URL fallback titles, generation
success/failure, unlabeled links/attachments, and empty messages. Ruff,
formatting, Pyright, and import contracts passed.
- Backend regression checks passed for first-turn extraction,
attachment/link normalization, canonical-to-original mapping, concurrent
generation, rename/archive races, failure/cooldown, ownership,
external/Build exclusion and route scope. Existing session-channel
service/repository/schema tests also passed (65 tests).
- Frontend title lifecycle, cache refresh, navigation isolation and
legacy workspace tests passed; TypeScript, ESLint, Ruff, Pyright and
import contracts passed.
- Playwright with the local mock: sent a first task message and verified
the same generated title in the sidebar, chat header and `/tasks`. Mock
inference is deterministic; real generation is exercised via service
tests with a stubbed existing title provider.

Requires backend and frontend deployment (backend first). Existing tasks
receive generated titles when opened; this does not bulk-backfill
historical tasks. Credit usage is unchanged. Staging's encrypted Mongo
client was unavailable here: the new classic single-collection CAS
passes the query guard, but actual encrypted-client validation remains a
release gate.

A fallback response gets at most two five-second follow-ups, so a
concurrent tab can observe the winning generation. Navigation cancels
those checks, and generated/manual titles stop them. Regression tests
cover successful completion, exhausted follow-ups and cancellation; no
unbounded polling or repeat inference is introduced.
```

来源：SerendipityOneInc/ecap-workspace @ d35f4fd2，PR #3906，作者 Nemo Feng。