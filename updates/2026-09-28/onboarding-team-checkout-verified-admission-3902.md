---
title: "修复：受邀加入团队的管理员不再卡在「继续 → 失败 → 重试」死循环，有权益的团队成员直接跳过个人付费"
type: "Bug Fix"
priority: "高"
date: "2026-09-28"
status: "待审核"
channels: ""
---

# 修复：受邀加入团队的管理员不再卡在「继续 → 失败 → 重试」死循环，有权益的团队成员直接跳过个人付费

## 核心宣传点

受邀的团队用户本应走完引导就直接进 Agents，不需要再买个人订阅。但之前一版对所有活跃的团队管理员/成员都跳过结账，另一版又拒绝没付费的管理员完成引导，两者叠在一起，让这批管理员卡在「继续 → 失败 → 重试」的循环里，还找不到任何购买入口。这次统一用同一份准入判定结果：有可验证权益凭证的普通团队成员和管理员会跳过个人套餐、Stripe 商品目录、订单创建和结账弹窗（含旧版企业套餐凭证）；没有合格凭证的团队管理员保留套餐选择和可用的结账流程。只是打开 Stripe 窗口永远不算完成引导，只有确认到准入才算。如果企业凭证在完成之前过期，「重试」会回到能正常购买的路径，而不是反复提交一个已被拒绝的完成请求；保存进度临时失败仍然只是重试、不会莫名要求付费。身份或准入未知/出错时绝不退化成要用户掏钱。

## 分级

- 内部：P0
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Problem and behavior

Invited Team users should finish the introduction and enter `/agents` without personal checkout. Previously #3902 skipped checkout for every active Team admin/member, while #3901 rejected completion for unpaid admins. This left those admins in a Continue → failure → Retry loop with no purchase path.

This revision addresses [Tim’s P1 review](https://github.com/SerendipityOneInc/ecap-workspace/pull/3902#issuecomment-5862350592) by using the same `useOnboardingAdmission` result that `OnboardingProvider.completeOnboarding` re-verifies:

- Active ordinary Team members and admins with verified subscription evidence skip the personal plan, Stripe catalog, order creation and Checkout popup. This includes the legacy enterprise-package evidence added by #3901.
- Team admins without qualifying evidence retain the plan and functioning checkout. Opening Stripe alone never completes onboarding; confirmed admission does.
- If enterprise evidence expires before completion, Retry returns to the usable purchase path instead of repeating a rejected completion. A temporary completion-save failure still retries without purchasing.
- Unknown/error identity or admission never falls back to a purchase. Disabled purchase hooks block both catalog fetching and purchase start, including cached catalogs.

## Dependency and scope

#3901 has now been squash-merged into `main` as `fac443103`. This branch incorporates that latest main in `6f2e73940`, resolving the overlapping Modal, checkout hook and integration-test conflicts while preserving the reviewed Team routing fix. The PR diff now contains only the Team-specific frontend changes; there is no longer an outstanding #3901 merge dependency.

Frontend only, using existing account, order-history and credits-check APIs. No backend, invitation redemption, database, dependency or lockfile changes. Existing APIs do not expose an invite-origin flag, so an admin role alone is not treated as proof of admission.

## Validation

- 283 related unit/integration tests across 20 files passed; after extending the payment-confirmation assertion, the 24 directly related tests passed again.
- Actual Provider + Modal + admission query/service + Stripe hooks remain connected in integration tests. Only external APIs, popup boundary and presentation are mocked. Covers unpaid admin checkout followed by confirmed admission, active ordinary member, verified legacy enterprise admin, evidence expiring at completion, and failed-save retry. Eligible Team cases assert zero catalog/order/Checkout/popup calls.
- 4 local Playwright browser tests passed: eligible admin and member complete after a simulated save failure, enter the workspace, and remain completed on reload with zero personal purchase requests; unpaid admin and personal accounts retain the plan. No browser page errors.
- TypeScript, all 7 frontend governance guards, changed-file ESLint and import-boundary checks passed (0 import errors; 684 existing warnings). Pre-push verification and GitHub CI results are checked separately.

Local browser validation uses mock accounts after invitation redemption. Real invitation email, OTP, staging membership/subscription data and real Stripe payment were not exercised. The existing generic network message for inactive/pending membership is an unchanged UX limitation, separate from this admission/checkout correction.

## Validation after syncing main (`6f2e73940`)

Re-ran all 283 related unit/integration tests and all 4 local browser tests against the actual merged main; all passed. The resolved onboarding source and regression tests are identical to the previously approved `6df86117e` implementation. TypeScript passed after stopping the dev server (the first run overlapped Next dev regenerating temporary route types). Full pre-push checks passed. The new GitHub CI round finished with **23 passing / 16 scope-skipped / 0 failures**, including the complete frontend test suite, build, lint/typecheck and CodeQL. Both Codex and Claude approved the current commit, with no blocking findings. GitHub reports **MERGEABLE / CLEAN / APPROVED**; the PR remains open and has not been merged.

Current review notes left unchanged: comment placement is stylistic, and returning to checkout after admission evidence expires is the intended verified-admission behavior. Non-blocking earlier review notes also left unchanged: generic blocked-membership copy is an existing UX limitation; the query key is already centralized in `useOnboardingAdmission`; order-history pagination is inherited from #3901 and optimization is outside this conflict resolution.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `888e6102dc6bacd412b6322dbf982a87d346fe44`
- PR: #3902
- 作者：ericma-srp
- 日期：2026-09-28T06:09:55Z

### Commit Message

```
fix(onboarding): align team checkout with verified admission (#3902)

## Problem and behavior

Invited Team users should finish the introduction and enter `/agents`
without personal checkout. Previously #3902 skipped checkout for every
active Team admin/member, while #3901 rejected completion for unpaid
admins. This left those admins in a Continue → failure → Retry loop with
no purchase path.

This revision addresses [Tim’s P1
review](https://github.com/SerendipityOneInc/ecap-workspace/pull/3902#issuecomment-5862350592)
by using the same `useOnboardingAdmission` result that
`OnboardingProvider.completeOnboarding` re-verifies:

- Active ordinary Team members and admins with verified subscription
evidence skip the personal plan, Stripe catalog, order creation and
Checkout popup. This includes the legacy enterprise-package evidence
added by #3901.
- Team admins without qualifying evidence retain the plan and
functioning checkout. Opening Stripe alone never completes onboarding;
confirmed admission does.
- If enterprise evidence expires before completion, Retry returns to the
usable purchase path instead of repeating a rejected completion. A
temporary completion-save failure still retries without purchasing.
- Unknown/error identity or admission never falls back to a purchase.
Disabled purchase hooks block both catalog fetching and purchase start,
including cached catalogs.

## Dependency and scope

#3901 has now been squash-merged into `main` as `fac443103`. This branch
incorporates that latest main in `6f2e73940`, resolving the overlapping
Modal, checkout hook and integration-test conflicts while preserving the
reviewed Team routing fix. The PR diff now contains only the
Team-specific frontend changes; there is no longer an outstanding #3901
merge dependency.

Frontend only, using existing account, order-history and credits-check
APIs. No backend, invitation redemption, database, dependency or
lockfile changes. Existing APIs do not expose an invite-origin flag, so
an admin role alone is not treated as proof of admission.

## Validation

- 283 related unit/integration tests across 20 files passed; after
extending the payment-confirmation assertion, the 24 directly related
tests passed again.
- Actual Provider + Modal + admission query/service + Stripe hooks
remain connected in integration tests. Only external APIs, popup
boundary and presentation are mocked. Covers unpaid admin checkout
followed by confirmed admission, active ordinary member, verified legacy
enterprise admin, evidence expiring at completion, and failed-save
retry. Eligible Team cases assert zero catalog/order/Checkout/popup
calls.
- 4 local Playwright browser tests passed: eligible admin and member
complete after a simulated save failure, enter the workspace, and remain
completed on reload with zero personal purchase requests; unpaid admin
and personal accounts retain the plan. No browser page errors.
- TypeScript, all 7 frontend governance guards, changed-file ESLint and
import-boundary checks passed (0 import errors; 684 existing warnings).
Pre-push verification and GitHub CI results are checked separately.

Local browser validation uses mock accounts after invitation redemption.
Real invitation email, OTP, staging membership/subscription data and
real Stripe payment were not exercised. The existing generic network
message for inactive/pending membership is an unchanged UX limitation,
separate from this admission/checkout correction.

## Validation after syncing main (`6f2e73940`)

Re-ran all 283 related unit/integration tests and all 4 local browser
tests against the actual merged main; all passed. The resolved
onboarding source and regression tests are identical to the previously
approved `6df86117e` implementation. TypeScript passed after stopping
the dev server (the first run overlapped Next dev regenerating temporary
route types). Full pre-push checks passed. The new GitHub CI round
finished with **23 passing / 16 scope-skipped / 0 failures**, including
the complete frontend test suite, build, lint/typecheck and CodeQL. Both
Codex and Claude approved the current commit, with no blocking findings.
GitHub reports **MERGEABLE / CLEAN / APPROVED**; the PR remains open and
has not been merged.

Current review notes left unchanged: comment placement is stylistic, and
returning to checkout after admission evidence expires is the intended
verified-admission behavior. Non-blocking earlier review notes also left
unchanged: generic blocked-membership copy is an existing UX limitation;
the query key is already centralized in `useOnboardingAdmission`;
order-history pagination is inherited from #3901 and optimization is
outside this conflict resolution.
```

来源：SerendipityOneInc/ecap-workspace @ 888e6102，PR #3902，作者 ericma-srp。
