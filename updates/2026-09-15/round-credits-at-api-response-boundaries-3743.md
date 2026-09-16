---
title: "fix(billing): round credits at API response boundaries (#3743)"
type: "Bug 修复"
priority: "高"
date: "2026-09-15"
status: "待审核"
channels: ""
---

# fix(billing): round credits at API response boundaries (#3743)

## 核心宣传点

## Problem and behavior
Credits balance and usage APIs expose long decimal tails, so clients show inconsistent precision. Round credit amounts with Decimal ROUND_HALF_UP at the HTTP response boundary (12.5 → 13), after precise aggregation and without changing stored data or internal billing calculations.

## Explicit product decision
The product owner explicitly requires backend rounding for **all client-facing credit amounts**, including task history and usage details, and accepts a one-credit display difference. `/users/credits/usage/details` is intentionally included: returning `"1"` instead of `"1.230001"` is the requested behavior, not loss of an exact-value guarantee that should be restored. Its `attribution: "exact"` describes session ownership, not display precision. The task consumer stores each already-aggregated session total unchanged; it does not sum rounded records. Internal aggregation remains decimal-precise, with no persisted billing changes.

## Changes
- Share CreditsJSONResponse across user credits/balance/usage routes, staff balance lookup, member quota responses, and Council estimates.
- Make rounding best-effort per field: conversion failures (including empty/non-numeric strings and non-finite numeric strings) preserve the original value, while other fields continue rounding. This formatting must not turn an otherwise valid response into HTTP 500.
- Preserve existing string-versus-number types and null semantics; currency amounts, conversion rates, counts, and durations remain precise.
- Remove forced `.00` padding in the web usage record. Clients no longer need separate credit-rounding changes.

## Validation
- 23 response tests passed after adding invalid-value HTTP 200 and fallback regression coverage.
- 110 targeted backend tests passed before the fallback follow-up; includes HTTP response serialization, route registration, half-up ties, nested wallets, exact aggregate preservation, and estimates.
- 8 web usage-record tests and 6 task-credit consumer tests passed; changed-file ESLint passed.
- Backend verify-py.sh passed (ruff, format, pyright, import contracts).
- Full local web typecheck was blocked by reused workspace dependencies: unrelated chat-ui interface mismatches and missing React resolution. CI installs the pinned dependencies and remains the full frontend gate.

## Deployment
Deploy claw-interface for consistent API values across clients. Deploy web/app to remove the usage record's forced decimal padding.


## Verified response-field inventory
The allowlist contains 13 fields, traced to the response producers on the registered routes:
- `services/user/credits_read.py`: `total_credits_balance`, `current_usage_credits`, `available_credits`, `total_available`, `subscription_credits`, `topup_credits`.
- `services/billing.py::_normalize_wallets`: `credits_balance`, `consumed_credits`.
- `services/billing_usage_records.py` and `services/billing_usage_attribution.py`: `credits` in totals, buckets/models, groups, and records.
- `schema/member_quota.py::MemberLlmQuota`: `used_credits`, `quota_credits`.
- `schema/council.py::CouncilEstimate`: `cost_low_credits`, `cost_high_credits`.

`total_available` and `consumed_credits` are emitted response fields; no direct client read was found in this repository. They are retained as existing API outputs, not claimed to be active UI consumers.

Removed unsupported entries: `remaining_credits` (no producer found), `total_credits` (legacy account storage, not these response fields), `granted_credits` and `voided_credits` (outgoing billing-service request parameters, not verified response fields on these routes). A regression test confirms these names remain untouched.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `a09d7320fdf4f7b37604bbe7d384482b913d863a`
- PR: #3743
- 作者：tim-srp
- 日期：2026-09-15T13:15:53Z

### Commit Message

```
fix(billing): round credits at API response boundaries (#3743)

## Problem and behavior
Credits balance and usage APIs expose long decimal tails, so clients
show inconsistent precision. Round credit amounts with Decimal
ROUND_HALF_UP at the HTTP response boundary (12.5 → 13), after precise
aggregation and without changing stored data or internal billing
calculations.

## Explicit product decision
The product owner explicitly requires backend rounding for **all
client-facing credit amounts**, inc
```
