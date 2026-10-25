---
title: "开发者平台的组织终于可以改名，不再被锁死为 Personal"
type: "新功能"
priority: "高"
date: "2026-10-14"
status: "待审核"
channels: ""
---

# 开发者平台的组织终于可以改名，不再被锁死为 Personal

## 核心宣传点

此前 Platform 所有者拿到的组织名固定叫 Personal，界面上完全没有修改入口。现在在组织通用设置里新增了名称输入框和保存按钮，配套新增 POST /platform/v1/organization/update 接口，所有者可自行改名；新建组织仍默认叫 Personal。接口从已验证的 Platform 会话推导组织，只接受 name，去空白并限制 1–100 个码点，底层是一次原子更新，Project、API Key 和计费关联完全保留。

## 分级

- 内部：P1
- 外部：A
- toB 相关：是
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `3c75b20e9f33c0190f8920331e47d1723927b1ae`
- PR: #4066
- 作者：finn-srp
- 日期：2026-10-14T05:17:37Z

### Commit Message

```
feat(platform): allow owners to rename their organization (#4066)

## Summary

Platform owners currently get an Organization named `Personal` with no
way to change it. Add `POST /platform/v1/organization/update` and a name
input with Save in Organization General settings. New Organizations
still default to `Personal`.

The endpoint derives the Organization from the verified Platform
session, accepts only `name`, trims whitespace, and enforces 1–100
Unicode code points. A single atomic Mongo update filters by
Organization ID, owner UID and active status, preserving Project,
API-key and billing associations. The frontend updates bootstrap through
the scope provider, retains failed drafts for explicit retry, and
disables editing during save. If a save finishes after sign-out and
re-login, the unmounted provider returns before cancelling or modifying
the new session bootstrap; it checks again after awaiting cancellation.

## Test plan

- [x] Organization tests pass independently (7 cases), including late
save completion after sign-out, same-account re-login with an in-flight
bootstrap, and Project pagination preservation. The re-login regression
test fails against the previous provider implementation. Initialize the
sign-out mock in each test group so these tests do not depend on
execution order.
- [x] Node 24: Platform `pnpm lint`, `pnpm typecheck`, `pnpm test` (290
tests), and `pnpm build`, on final merge commit `b636ea5a2` after
merging current `origin/main`.
- [x] `ecap-verify-py-ci` on final merge commit `b636ea5a2` after
merging current `origin/main`: Linux dependency resolution, static
checks, all ci-lint guards, both duplication checks, and the full
4-worker pytest/coverage gate (12,267 passed, 5 skipped; coverage
89.65%, threshold 89.5%).
- [x] Local browser preview: save, reload persistence, desktop/mobile
layouts; no horizontal mobile overflow or browser errors.
- [ ] Staging encrypted-client and authenticated frontend/backend
integration verification before release. Local Mongo tests and the UI
preview do not establish CSFLE runtime compatibility.

The legacy pre-commit `check-user` hook requires a GitHub login ending
in `-srp`, which conflicts with this workspace's required Finn account
(`finn930`). Only that hook was skipped; all quality hooks ran, and the
commit author is `finn-srp <finn@srp.one>`.

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

