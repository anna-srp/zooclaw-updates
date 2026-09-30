---
title: "修复：用兑换码、人工调整或试用拿到 Pro 的用户不再被要求再走一次 Stripe 付款"
type: "Bug Fix"
priority: "高"
date: "2026-09-29"
status: "待审核"
channels: ""
---

# 修复：用兑换码、人工调整或试用拿到 Pro 的用户不再被要求再走一次 Stripe 付款

## 核心宣传点

上一版引导门禁收紧之后，那些不是通过刷卡付费、而是通过订阅码、人工调整或服务端确认的试用拿到 Pro 权限的用户，会被重新推进 Stripe 结账流程——明明已经有权限，却被要求再付一次钱。现在只要服务端判定权益有效且未过期（状态为 active 或 trial），不管来源是订阅码、人工调整、试用还是付费，一律跳过 Stripe；Starter 和 Ultra 等受支持的档位沿用同一条规则。一个服务端判定为 Pro、但没有绑卡、没有兑换码、没有付费周期也没有订单的账号，现在可以正常走完引导、刷新页面并打开受保护的工作区页面；保存「引导已完成」之前还会再取一次权限做确认。已过期或不完整的授权不会仅因为套餐名写着 Pro 就被放行。

## 分级

- 内部：P0
- 外部：A
- toB 相关：否
- 发布状态：已随正式 release 上线

## PR 说明

## Problem and behavior
After #3901, effective Pro users granted access without a payment provider could be forced into Stripe onboarding. Every effective, unexpired Pro entitlement (server status `active` or `trial`) now skips Stripe, regardless of its source: subscription code, manual adjustment, server-confirmed trial or payment. The same shared rule preserves the supported Starter/Ultra tiers.

A server-resolved Pro account with no card, code, paid cycles or orders can finish onboarding, refresh and open protected workspace routes. Access is fetched again before onboarding completion is saved. An expired or incomplete grant is not accepted merely because its plan says Pro.

## Implementation
- Share the active/trial status + supported plan + future finite expiry predicate between onboarding admission and card-binding/send prompts. Do not enumerate source types or require a code/source id.
- Reuse `/account/me`'s current-access projection for admission and billing initialization; use `billing_summary.current_access` for credits checks. Team/legacy credits responses without a summary use their existing resolved status/plan/expiry fields. A present summary takes precedence over flat fields.
- All admitted personal/team users skip the Stripe plan step, without catalog, order or popup creation. Preserve the existing paid-history, invited-member and legacy enterprise admission paths.
- Keep payment-provider identity unchanged; no personal entitlement is injected into team billing responses.

## Validation
- Four admission/modal regression tests fail on the previous code for valid Pro accounts without a subscription code or provider.
- 409 targeted unit/integration tests across 22 files passed, including manual Pro, code/card parity, zero credits, billing initialization, invalid status/expiry, summary precedence and expiry immediately before completion.
- TypeScript, ESLint and frontend governance guards passed.
- Chromium: all 6 personal scenarios passed (code, card, manual grant, valid Pro trial, expired code, expired trial). Verified completion retry, refresh and direct `/home`, `/identity`, `/agents`; zero catalog/order/popup for admitted users.
- Three additional trial admission/modal regressions failed before the status update and pass afterward, including expiry during completion.
- CI settled on `4b4179155`: 23 checks passed, 16 skipped, no failures. Full frontend tests, production build, lint/typecheck, CodeQL and review gates passed.
- Claude and Codex re-reviews both APPROVE, with no new inline findings. Claude explicitly confirms both Tim comments (providerless grants and effective Pro trials) are addressed. Its optional suggestion to share expiry logic with the legacy enterprise branch is left unchanged: this is a pre-existing duplication, not a defect or necessary part of this fix.
- Local API fixtures only: no live grant/redemption, production payment, deployment or merge.

## Review resolution
Tim's P1 and subsequent P2 are addressed: valid Pro trials are explicitly included under the user's all-effective-Pro rule. A trial status alone, free plan, missing/invalid expiry or expired trial remains insufficient. Completion re-verification covers a trial expiring mid-flow. Access continues to be based on the effective server-resolved entitlement.

Original P1: access is based on the effective server-resolved entitlement, not its acquisition source. The personal skip-checkout behavior is explicitly intended by the user. Earlier team-summary feedback is handled using the team's own resolved fields when no summary is returned, preserving the personal/team billing boundary.

Frontend only: no backend, BFF, dependencies or lockfile changes. Based on main `5c3a5d973`, including #3916 (merge `2cdfd5ce9`); its shared account query, retries and initial loading optimizations are preserved.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `9cbeac6b651a24d73e7be2558a53dccf0687019f`
- PR: #3924
- 作者：ericma-srp
- 日期：2026-09-29T09:36:47Z

### Commit Message

```
fix(onboarding): admit all effective Pro entitlements (#3924)

## Problem and behavior
After #3901, effective Pro users granted access without a payment
provider could be forced into Stripe onboarding. Every effective,
unexpired Pro entitlement (server status `active` or `trial`) now skips
Stripe, regardless of its source: subscription code, manual adjustment,
server-confirmed trial or payment. The same shared rule preserves the
supported Starter/Ultra tiers.

A server-resolved Pro account with no card, code, paid cycles or orders
can finish onboarding, refresh and open protected workspace routes.
Access is fetched again before onboarding completion is saved. An
expired or incomplete grant is not accepted merely because its plan says
Pro.

## Implementation
- Share the active/trial status + supported plan + future finite expiry
predicate between onboarding admission and card-binding/send prompts. Do
not enumerate source types or require a code/source id.
- Reuse `/account/me`'s current-access projection for admission and
billing initialization; use `billing_summary.current_access` for credits
checks. Team/legacy credits responses without a summary use their
existing resolved status/plan/expiry fields. A present summary takes
precedence over flat fields.
- All admitted personal/team users skip the Stripe plan step, without
catalog, order or popup creation. Preserve the existing paid-history,
invited-member and legacy enterprise admission paths.
- Keep payment-provider identity unchanged; no personal entitlement is
injected into team billing responses.

## Validation
- Four admission/modal regression tests fail on the previous code for
valid Pro accounts without a subscription code or provider.
- 409 targeted unit/integration tests across 22 files passed, including
manual Pro, code/card parity, zero credits, billing initialization,
invalid status/expiry, summary precedence and expiry immediately before
completion.
- TypeScript, ESLint and frontend governance guards passed.
- Chromium: all 6 personal scenarios passed (code, card, manual grant,
valid Pro trial, expired code, expired trial). Verified completion
retry, refresh and direct `/home`, `/identity`, `/agents`; zero
catalog/order/popup for admitted users.
- Three additional trial admission/modal regressions failed before the
status update and pass afterward, including expiry during completion.
- CI settled on `4b4179155`: 23 checks passed, 16 skipped, no failures.
Full frontend tests, production build, lint/typecheck, CodeQL and review
gates passed.
- Claude and Codex re-reviews both APPROVE, with no new inline findings.
Claude explicitly confirms both Tim comments (providerless grants and
effective Pro trials) are addressed. Its optional suggestion to share
expiry logic with the legacy enterprise branch is left unchanged: this
is a pre-existing duplication, not a defect or necessary part of this
fix.
- Local API fixtures only: no live grant/redemption, production payment,
deployment or merge.

## Review resolution
Tim's P1 and subsequent P2 are addressed: valid Pro trials are
explicitly included under the user's all-effective-Pro rule. A trial
status alone, free plan, missing/invalid expiry or expired trial remains
insufficient. Completion re-verification covers a trial expiring
mid-flow. Access continues to be based on the effective server-resolved
entitlement.

Original P1: access is based on the effective server-resolved
entitlement, not its acquisition source. The personal skip-checkout
behavior is explicitly intended by the user. Earlier team-summary
feedback is handled using the team's own resolved fields when no summary
is returned, preserving the personal/team billing boundary.

Frontend only: no backend, BFF, dependencies or lockfile changes. Based
on main `5c3a5d973`, including #3916 (merge `2cdfd5ce9`); its shared
account query, retries and initial loading optimizations are preserved.
```

来源：SerendipityOneInc/ecap-workspace @ 9cbeac6b，PR #3924，作者 ericma-srp。
