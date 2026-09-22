---
title: "fix(models): guide users without access to billing (#3839)"
type: "Bug Fix"
priority: "高"
date: "2026-09-21"
status: "待审核"
channels: ""
---

# 没有模型访问权限时，给出可点的开通入口而不是报错

## 核心宣传点

以前账号既没有有效订阅、也没有积分时，模型列表接口会直接抛 500，用户看到的是一个原始服务端错误，完全不知道下一步该干什么。现在这种「确认无权限」的情况会返回 402 和明确的错误码，前端识别后不再做无意义的重试和错误上报，而是展示「解锁模型 / 查看方案」入口，点击在新标签打开账号计费页，不再弹结账弹窗。关键是原来的输入框不会被卸载：New Task、Agent Builder 和会话里已经输入的内容、待上传文件和模型选择都保留，回到标签页时只刷新模型目录、不会自动帮你发送。另外做了个重要的安全边界——如果计费网关本身查不通，返回的是可重试的 502，而不是当成「有权限」或者「该买了」，避免把服务异常误判成用户没付费。

## 分级

- 内部：P0
- 外部：A
- 发布状态：已合并待发版

## PR 说明

## Problem

The model catalog returns an unhandled 500 when Billing Gateway reports `no_active_subscription`. Users with confirmed missing access see a raw server error rather than a useful Billing link.

## Behavior

- Return HTTP 402 with `{code: "billing.subscription_or_credits_required", detail: ...}` only when neither effective subscription/grant/team access nor available credits exists. Frontend branches on the code, suppresses expected-error retries/reporting, and gates submission and model replacement prompts.
- Both “Unlock models” and “Explore options” open the canonical `/identity?tab=account-billing` page in a new tab, with no checkout modal. Keeping the original composer mounted preserves input, pending files, and model selection in New Task, Agent Builder, and chat. Returning to the tab refreshes the catalog without auto-submitting.
- Keep shared credit authorization behavior unchanged. Extract only the existing customer-ID resolution for reuse; model synchronization and runtime recovery still use the gateway credit check, without any wallet fallback.
- Handle billing exceptions in a catalog-only adapter. The exact `400/no_active_subscription` response permits reading the wallet only to establish an empty/nonpositive balance. Positive settled wallet balance is not authorization: if the gateway cannot confirm availability, return retryable `billing.balance_unavailable` (502), not full model access or purchase guidance. Actual gateway-confirmed positive available credits retain existing full model access.
- Invalid balances return `billing.invalid_balance` (502). Model catalog dependency errors retain `models.catalog_unavailable` (503).

## Validation

- Backend: 86 targeted tests passed, including shared authorization isolation, confirmed available versus settled balance, malformed wallet/check payloads, subscription/team states, and the 402 route contract.
- Frontend: 186 targeted tests passed, including English/Chinese new-tab destinations through the canonical locale-free app route, submission gating, return-to-tab access refresh, New Task composer, and Agent Builder dialogs.
- Backend static checks passed: ruff, format, pyright, import contracts.
- Frontend TypeScript passed; ESLint formatting correction applied and verified.

## Deployment and limits

Requires both claw-interface and web deployment. Deploy web before or alongside the backend for the new guidance. No live billing/configuration data changed.

Gateway-independent top-up spending is not implemented here: the current gateway still requires an active subscription for its authoritative credit check. Settled wallet balance alone cannot safely establish spendability. This change preserves that boundary and reports uncertainty as a retryable error.

## Review adjudication

Fixed the malformed-wallet-response finding with shape validation and regression tests. The follow-up review identified a broader authorization effect from placing fallback in the shared helper; moved diagnostics to the catalog-only adapter and pinned the original shared behavior. Fixed navigation-related draft loss by opening Billing in a new tab rather than unmounting draft-owning surfaces.

PAST_DUE remains effective under the current-access resolver. MANUAL_REVIEW remains unresolved and is not presented as a confirmed need to purchase again. Tests retain both cases.

Follow-up validation exercises the real billing client methods against malformed HTTP responses, covering JSON decode failures and client-side non-mapping errors. The catalog maps these to `billing.invalid_balance` (502), without changing the shared client. CI-exposed Agent Builder and chat test regressions were fixed by reusing `LocaleLink` inside the billing notice; 148 tests across the affected suites and composer passed locally.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `73a53d8d543d258263aba4ea5409e2ae758b7013`
- PR: #3839
- 作者：tim-srp
- 日期：2026-09-21T09:59:50Z

### Commit Message

```
fix(models): guide users without access to billing (#3839)

## Problem

The model catalog returns an unhandled 500 when Billing Gateway reports
`no_active_subscription`. Users with confirmed missing access see a raw
server error rather than a useful Billing link.

## Behavior

- Return HTTP 402 with `{code:
"billing.subscription_or_credits_required", detail: ...}` only when
neither effective subscription/grant/team access nor available credits
exists. Frontend branches on the code, suppresses expected-error
retries/reporting, and gates submission and model replacement prompts.
- Both “Unlock models” and “Explore options” open the canonical
`/identity?tab=account-billing` page in a new tab, with no checkout
modal. Keeping the original composer mounted preserves input, pending
files, and model selection in New Task, Agent Builder, and chat.
Returning to the tab refreshes the catalog without auto-submitting.
- Keep shared credit authorization behavior unchanged. Extract only the
existing customer-ID resolution for reuse; model synchronization and
runtime recovery still use the gateway credit check, without any wallet
fallback.
- Handle billing exceptions in a catalog-only adapter. The exact
`400/no_active_subscription` response permits reading the wallet only to
establish an empty/nonpositive balance. Positive settled wallet balance
is not authorization: if the gateway cannot confirm availability, return
retryable `billing.balance_unavailable` (502), not full model access or
purchase guidance. Actual gateway-confirmed positive available credits
retain existing full model access.
- Invalid balances return `billing.invalid_balance` (502). Model catalog
dependency errors retain `models.catalog_unavailable` (503).

## Validation

- Backend: 86 targeted tests passed, including shared authorization
isolation, confirmed available versus settled balance, malformed
wallet/check payloads, subscription/team states, and the 402 route
contract.
- Frontend: 186 targeted tests passed, including English/Chinese new-tab
destinations through the canonical locale-free app route, submission
gating, return-to-tab access refresh, New Task composer, and Agent
Builder dialogs.
- Backend static checks passed: ruff, format, pyright, import contracts.
- Frontend TypeScript passed; ESLint formatting correction applied and
verified.

## Deployment and limits

Requires both claw-interface and web deployment. Deploy web before or
alongside the backend for the new guidance. No live
billing/configuration data changed.

Gateway-independent top-up spending is not implemented here: the current
gateway still requires an active subscription for its authoritative
credit check. Settled wallet balance alone cannot safely establish
spendability. This change preserves that boundary and reports
uncertainty as a retryable error.

## Review adjudication

Fixed the malformed-wallet-response finding with shape validation and
regression tests. The follow-up review identified a broader
authorization effect from placing fallback in the shared helper; moved
diagnostics to the catalog-only adapter and pinned the original shared
behavior. Fixed navigation-related draft loss by opening Billing in a
new tab rather than unmounting draft-owning surfaces.

PAST_DUE remains effective under the current-access resolver.
MANUAL_REVIEW remains unresolved and is not presented as a confirmed
need to purchase again. Tests retain both cases.

Follow-up validation exercises the real billing client methods against
malformed HTTP responses, covering JSON decode failures and client-side
non-mapping errors. The catalog maps these to `billing.invalid_balance`
(502), without changing the shared client. CI-exposed Agent Builder and
chat test regressions were fixed by reusing `LocaleLink` inside the
billing notice; 148 tests across the affected suites and composer passed
locally.
```

来源：SerendipityOneInc/ecap-workspace @ 73a53d8d，PR #3839，作者 tim-srp。