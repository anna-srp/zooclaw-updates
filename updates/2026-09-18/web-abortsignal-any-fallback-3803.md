---
title: "fix(web): support browsers without AbortSignal.any (#3803)"
type: "Bug Fix"
priority: "中"
date: "2026-09-18"
status: "待审核"
channels: ""
---

# 修复：老版本浏览器（不支持 AbortSignal.any）也能正常拉取模型列表

## 核心宣传点

部分浏览器没有 AbortSignal.any()，导致带取消信号的请求直接报错，模型列表等共用接口拉不出来。现在后端请求、Claw 请求和流式请求包装器共用一个轻量兜底实现，浏览器原生支持时仍优先用原生，不引入依赖也不打全局 polyfill。调用方的取消和超时行为保持不变，普通请求结束后会清理监听，流式读取过程中也仍然能取消。

## 分级

- 内部：P2
- 外部：C
- 发布状态：已合并待发版

## PR 说明

## Summary
- Keep model-list and other shared API requests working when a browser lacks `AbortSignal.any()`.
- Add a small shared fallback used by the backend, Claw, and streaming request wrappers. Native support remains preferred; no dependencies or global polyfills are added.
- Preserve caller cancellation and timeouts, clean up fallback listeners after ordinary requests, and retain cancellation while streaming a response body.

## Root cause
Requests with a caller-provided cancellation signal previously invoked `AbortSignal.any()` unconditionally. Removing that API reproduces a TypeError before `/api/claw/models` reaches fetch.

This is a defensive compatibility fix. The reported WeChat incident is not conclusively attributed to this API: available production model requests returned 200, and no matching Sentry TypeError has been confirmed.

## Test plan
- [x] Regression first: all three request wrappers failed with `AbortSignal.any` removed before the fix.
- [x] Native and fallback cancellation, timeout, pre-aborted signals, first abort reason, listener cleanup, model loading, and cancellation after stream headers.
- [x] Targeted frontend verification: TypeScript, lint, governance guards, and related unit tests.

## Validation and review outcome
- Local verification passed: 286 tests across 16 files, TypeScript, lint, and governance checks. CI completed successfully; CodeQL and both automated reviewers passed.
- Reviewed the streaming-listener note and left the code unchanged: conversation creation and direct artifact downloads supply no caller signal; `useResolvedUrl` passes React Query's per-fetch signal. No current caller reuses a long-lived signal across streams. Wrapping response bodies solely for this hypothetical case would broaden this small compatibility fix; cancellation after response headers remains covered by tests.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `89b24b5a909a2223b64bb4c4c0f05937c46073d3`
- PR: #3803
- 作者：tim-srp
- 日期：2026-09-18T12:05:57Z

### Commit Message

```
fix(web): support browsers without AbortSignal.any (#3803)

## Summary
- Keep model-list and other shared API requests working when a browser
lacks `AbortSignal.any()`.
- Add a small shared fallback used by the backend, Claw, and streaming
request wrappers. Native support remains preferred; no dependencies or
global polyfills are added.
- Preserve caller cancellation and timeouts, clean up fallback listeners
after ordinary requests, and retain cancellation while streaming a
response body.

## Root cause
Requests with a caller-provided cancellation signal previously invoked
`AbortSignal.any()` unconditionally. Removing that API reproduces a
TypeError before `/api/claw/models` reaches fetch.

This is a defensive compatibility fix. The reported WeChat incident is
not conclusively attributed to this API: available production model
requests returned 200, and no matching Sentry TypeError has been
confirmed.

## Test plan
- [x] Regression first: all three request wrappers failed with
`AbortSignal.any` removed before the fix.
- [x] Native and fallback cancellation, timeout, pre-aborted signals,
first abort reason, listener cleanup, model loading, and cancellation
after stream headers.
- [x] Targeted frontend verification: TypeScript, lint, governance
guards, and related unit tests.

## Validation and review outcome
- Local verification passed: 286 tests across 16 files, TypeScript,
lint, and governance checks. CI completed successfully; CodeQL and both
automated reviewers passed.
- Reviewed the streaming-listener note and left the code unchanged:
conversation creation and direct artifact downloads supply no caller
signal; `useResolvedUrl` passes React Query's per-fetch signal. No
current caller reuses a long-lived signal across streams. Wrapping
response bodies solely for this hypothetical case would broaden this
small compatibility fix; cancellation after response headers remains
covered by tests.
```

## 备注

发布状态：已合并待发版（尚未包含在任何 ecap-*-release tag 中，最新正式 release 为 ecap-v0.19.16-release）。

来源：SerendipityOneInc/ecap-workspace @ 89b24b5a，PR #3803，作者 tim-srp。
