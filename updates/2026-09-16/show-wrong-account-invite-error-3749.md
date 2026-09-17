---
title: "fix(web): show wrong-account invite error (#3749)"
type: "Bug 修复"
priority: "中"
date: "2026-09-16"
status: "待审核"
channels: ""
---

# fix(web): show wrong-account invite error (#3749)

## 核心宣传点

用错误的账号打开组织邀请链接时，会明确提示「请用收到邀请的邮箱登录」，而不是给一个看不懂的报错；同时不会泄露被邀请人的邮箱。

## PR 说明

## Summary

- map the backend `invite_code.email_mismatch` response to the existing `organizationJoin.errors.wrongAccount` copy
- keep the invited email private while telling the user to sign in with the address that received the invitation
- cover the error mapper and the unauthenticated OTP-to-join flow

## Testing

- `bash scripts/verify-web.sh web/app/src/app/[locale]/join/lib/join-state.ts web/app/tests/unit/app/organization-join-flow.unit.spec.tsx web/app/tests/unit/app/organization-join-state.unit.spec.ts`
- TypeScript, 7 related Vitest tests, and ESLint passed

Related to #3727 and follow-up to #3746.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `8c3ae58942d22901be7bd0f80fb2541b622361fc`
- PR: #3749
- 作者：finn-srp
- 日期：2026-09-16T07:13:54Z

### Commit Message

```
fix(web): show wrong-account invite error (#3749)

## Summary

- map the backend `invite_code.email_mismatch` response to the existing
`organizationJoin.errors.wrongAccount` copy
- keep the invited email private while telling the user to sign in with
the address that received the invitation
- cover the error mapper and the unauthenticated OTP-to-join flow

## Testing

- `bash scripts/verify-web.sh
web/app/src/app/[locale]/join/lib/join-state.ts
web/app/tests/unit/app/organization-join-flow.unit.
```
