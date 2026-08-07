---
title: "会话线程中的生成文件自动打开预览"
type: "体验优化"
priority: "中"
date: "2026-08-06"
status: "待审核"
channels: ""
---

## 核心宣传点

在会话线程里生成的 Excel 等可预览文件会自动展开预览，和主聊天页保持一致，不用再手动点开找结果。

## 原始内容

**fix(web): auto-preview session thread attachments (#3289)**

- sha: `eb7f3626065a741b4f66110dcdd6745a05dceb73`
- PR: #3289

```
fix(web): auto-preview session thread attachments (#3289)

## What changed

- reuse the existing artifacts sidebar state in Session Thread
- pass only the current thread's normalized messages into attachment
detection
- automatically open previewable native attachments such as generated
Excel files
- preserve manual preview controls and session-scoped reset behavior
- add a Session Thread regression test for an `.xlsx` attachment

## Root cause

The Session Thread page used a local preview state that only supported
manual file opening. Unlike the main chat page, it was not connected to
the existing attachment auto-preview hook.

## Impact

Generated previewable attachments now open automatically in Session
Thread without scanning unrelated channel messages.

## Validation

- `SessionThreadClient.unit.spec.tsx`: 42 tests passed
- `useArtifactsSidebar.unit.spec.ts`: 20 tests passed
- TypeScript `tsc --noEmit`
- targeted ESLint
- Prettier check
- `git diff --check`
```

**PR Body:**

## What changed

- reuse the existing artifacts sidebar state in Session Thread
- pass only the current thread's normalized messages into attachment detection
- automatically open previewable native attachments such as generated Excel files
- preserve manual preview controls and session-scoped reset behavior
- add a Session Thread regression test for an `.xlsx` attachment

## Root cause

The Session Thread page used a local preview state that only supported manual file opening. Unlike the main chat page, it was not connected to the existing attachment auto-preview hook.

## Impact

Generated previewable attachments now open automatically in Session Thread without scanning unrelated channel messages.

## Validation

- `SessionThreadClient.unit.spec.tsx`: 42 tests passed
- `useArtifactsSidebar.unit.spec.ts`: 20 tests passed
- TypeScript `tsc --noEmit`
- targeted ESLint
- Prettier check
- `git diff --check`

