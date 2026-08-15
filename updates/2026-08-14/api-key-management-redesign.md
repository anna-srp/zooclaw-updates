---
title: "API 密钥管理页重做：创建、一次性查看、轮换、吊销一站搞定"
type: "产品基础功能更新"
priority: "中"
date: "2026-08-14"
status: "待审核"
channels: ""
---

## 核心宣传点

设置里的 API 密钥页面全新改版，创建、仅显示一次的安全查看、轮换和吊销都有清晰的引导弹窗，加载/空/异常状态一目了然。

## 原始内容

feat(settings): redesign API key management (#3371)

## Linear

N/A

## Summary

- Redesign **Claw Settings → API Keys** as a ZooClaw Design System
security ledger with distinct loading, empty, populated, and error
states.
- Keep a single **Create API Key** action in the correct location and
add consistent create, one-time reveal, rotate, and revoke dialogs.
- Keep plaintext secrets only in controller memory, add local mock
service-token coverage, and refine shared dialog/control behavior needed
for safe state handoffs.

## Test plan

- [x] Web app governance guards, TypeScript, and scoped ESLint via
`scripts/verify-web.sh --no-test`
- [x] Web app focused Vitest: 4 files / 49 tests
- [x] ZooClaw Design System focused Vitest: 4 files / 36 tests
- [x] ZooClaw Design System TypeScript and ESLint
- [x] Changed-surface verification via `scripts/verify-changed.sh`
- [x] Diff whitespace check and PR size guard (1,539 / 3,000 effective
lines)

## Security notes

- The complete API key is held only in local controller state for the
reveal dialog and is cleared when the dialog closes.
- The complete key is not written to React Query cache, URL state,
browser storage, or logs.
- A successful create/rotate response that omits its one-time secret is
presented as a terminal partial-success state, preventing accidental
duplicate creation or rotation retries.
- Dialog handoff visibility is latched through predecessor exit
animations, preventing a fast-close flash of the completed Create/Rotate
dialog.

---
### PR Body

## Linear

N/A

## Summary

- Redesign **Claw Settings → API Keys** as a ZooClaw Design System security ledger with distinct loading, empty, populated, and error states.
- Keep a single **Create API Key** action in the correct location and add consistent create, one-time reveal, rotate, and revoke dialogs.
- Keep plaintext secrets only in controller memory, add local mock service-token coverage, and refine shared dialog/control behavior needed for safe state handoffs.

## Test plan

- [x] Web app governance guards, TypeScript, and scoped ESLint via `scripts/verify-web.sh --no-test`
- [x] Web app focused Vitest: 4 files / 49 tests
- [x] ZooClaw Design System focused Vitest: 4 files / 36 tests
- [x] ZooClaw Design System TypeScript and ESLint
- [x] Changed-surface verification via `scripts/verify-changed.sh`
- [x] Diff whitespace check and PR size guard (1,539 / 3,000 effective lines)

## Security notes

- The complete API key is held only in local controller state for the reveal dialog and is cleared when the dialog closes.
- The complete key is not written to React Query cache, URL state, browser storage, or logs.
- A successful create/rotate response that omits its one-time secret is presented as a terminal partial-success state, preventing accidental duplicate creation or rotation retries.
- Dialog handoff visibility is latched through predecessor exit animations, preventing a fast-close flash of the completed Create/Rotate dialog.

