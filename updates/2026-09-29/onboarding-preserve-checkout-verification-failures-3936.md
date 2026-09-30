---
title: "修复：从 Stripe 返回后校验失败不再整页报错，套餐和「继续结账」保留在原处可重试"
type: "Bug Fix"
priority: "高"
date: "2026-09-29"
status: "待审核"
channels: ""
---

# 修复：从 Stripe 返回后校验失败不再整页报错，套餐和「继续结账」保留在原处可重试

## 核心宣传点

新用户打开 Stripe 付款再回到 ZooWork 时，后台那次准入校验一旦失败，整个引导流程会被卸载、结账界面被一整页错误提示取代，用户既看不到自己选的套餐，也找不到继续付款的入口。现在对于已知未付费的用户，套餐卡片和「继续结账」动作会保持挂载，校验重试直接显示在套餐里；受保护的工作区内容在拿到新的服务端凭证之前仍然保持拦截，不会因为界面留着就放人进去。引导流程和工作区门禁现在共用同一套错误展示判定，缓存的、UID 匹配的账号身份只能用来保住结账界面的呈现，不能授予工作区访问权、也不能跳过完成引导时的那次校验。首次校验还没有结果、以及此前已准入的用户被明确拒绝这两种情况，仍然保留原来的阻断式恢复流程。轮询频率、支付凭证判定和后端行为都没有变化。

## 分级

- 内部：P0
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Problem and behavior

After a new user opens Stripe and returns to ZooWork, a failed background admission request currently unmounts onboarding and replaces the checkout screen with a full-page error. Keep the known-unpaid user's plan and Continue checkout action mounted, show verification retry in the plan, and leave protected workspace content blocked until fresh server evidence permits admission.

The provider and workspace gate now share the same error-display decision. Cached, UID-matched account identity may preserve checkout presentation, but cannot grant workspace access or skip the existing completion-time verification. Initial unresolved verification and explicit rejection of previously admitted users retain blocking recovery. Polling frequency, payment evidence and backend behavior are unchanged.

## Validation

- Four regression cases fail against the previous implementation; 361 relevant unit/integration tests pass after the fix.
- TypeScript, changed-file ESLint, frontend governance guards and full pre-commit ESLint pass.
- Two local Chromium checkout cases pass with actual Provider/Modal/query logic and mocked HTTP: open HTTPS checkout popup, return after account or order 503s, keep checkout usable, retry without extra orders or premature completion, then admit after confirmed order evidence. Screenshots inspected.
- All 13 existing admission/loading browser cases also pass, including desktop/mobile entry, initial errors/recovery, anonymous/unpaid protection and paid users.
- Real Stripe payment and the original production request failure were not reproduced.

## #3901 polling audit

Only one 3-second loop was introduced, owned by OnboardingProvider via useOnboardingAdmission. Other consumers share its UID-scoped query without enabling their own interval. It reads account/me, then personal orders when needed; active team admins can additionally read team orders and enterprise credits evidence. It begins whenever a protected-page user resolves unpaid, even before Stripe is opened. Focus/mount, checkout-open and completion checks are event-triggered; the 15-second transient-error recovery was added later by #3916. These reads do not create orders or confirm Stripe sessions.

## Review follow-up

Codex and Claude both approve. Claude's non-blocking account-error observation does not introduce a new checkout-skip restriction: previously account.isError forced audience=null, which already prevented skipping checkout. The new explicit !account.isError preserves that condition while cached identity now allows known-unpaid checkout to remain usable. Both account observers use accountSessionKeys.me(uid), rather than independent account caches. No expansion to paid-user error policy is needed for this fix.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `cd905d00775939b723098c5d29e61d14f6eee017`
- PR: #3936
- 作者：ericma-srp
- 日期：2026-09-29T14:54:32Z

### Commit Message

```
fix(onboarding): preserve checkout during verification failures (#3936)

## Problem and behavior

After a new user opens Stripe and returns to ZooWork, a failed
background admission request currently unmounts onboarding and replaces
the checkout screen with a full-page error. Keep the known-unpaid user's
plan and Continue checkout action mounted, show verification retry in
the plan, and leave protected workspace content blocked until fresh
server evidence permits admission.

The provider and workspace gate now share the same error-display
decision. Cached, UID-matched account identity may preserve checkout
presentation, but cannot grant workspace access or skip the existing
completion-time verification. Initial unresolved verification and
explicit rejection of previously admitted users retain blocking
recovery. Polling frequency, payment evidence and backend behavior are
unchanged.

## Validation

- Four regression cases fail against the previous implementation; 361
relevant unit/integration tests pass after the fix.
- TypeScript, changed-file ESLint, frontend governance guards and full
pre-commit ESLint pass.
- Two local Chromium checkout cases pass with actual
Provider/Modal/query logic and mocked HTTP: open HTTPS checkout popup,
return after account or order 503s, keep checkout usable, retry without
extra orders or premature completion, then admit after confirmed order
evidence. Screenshots inspected.
- All 13 existing admission/loading browser cases also pass, including
desktop/mobile entry, initial errors/recovery, anonymous/unpaid
protection and paid users.
- Real Stripe payment and the original production request failure were
not reproduced.

## #3901 polling audit

Only one 3-second loop was introduced, owned by OnboardingProvider via
useOnboardingAdmission. Other consumers share its UID-scoped query
without enabling their own interval. It reads account/me, then personal
orders when needed; active team admins can additionally read team orders
and enterprise credits evidence. It begins whenever a protected-page
user resolves unpaid, even before Stripe is opened. Focus/mount,
checkout-open and completion checks are event-triggered; the 15-second
transient-error recovery was added later by #3916. These reads do not
create orders or confirm Stripe sessions.

## Review follow-up

Codex and Claude both approve. Claude's non-blocking account-error
observation does not introduce a new checkout-skip restriction:
previously account.isError forced audience=null, which already prevented
skipping checkout. The new explicit !account.isError preserves that
condition while cached identity now allows known-unpaid checkout to
remain usable. Both account observers use accountSessionKeys.me(uid),
rather than independent account caches. No expansion to paid-user error
policy is needed for this fix.
```

来源：SerendipityOneInc/ecap-workspace @ cd905d00，PR #3936，作者 ericma-srp。
