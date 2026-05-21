---
title: "顶级套餐用户不再显示升级提示"
type: "Bug Fix"
priority: "低"
date: "2026-05-20"
status: "待审核"
channels: ""
repo: "ecap-workspace"
sha: "c8cfc7cc93c5d6a0ba86367763f75549ebfed40a"
pr: 1729
---
# 顶级套餐用户不再显示升级提示

## 核心宣传点

已购买最高套餐的用户将不再看到不必要的升级提示，界面更简洁。

## 原始内容

### Commit Message

```
fix(web): hide upgrade copy for users at top plan tier (#1729)

## Summary

Ultra-tier users had no upgrade path but still saw "Upgrade" copy in
three places. Root cause: each callsite read `status` only (no `plan`
awareness), and the one place that did check plan hardcoded `'ultra'` as
a string rather than deriving from `PLAN_TIERS`.

- **`UserMenu`** — main CTA in the avatar dropdown now resolves to
`subscription.manage` when an active user is at the top tier, instead of
`subscription.upgrade`.
- **`UpgradePromptModal`** (`active-credits` context) — Ultra users now
see a single `Add Credits` CTA instead of `[Add Credits] [Upgrade
Plan]`; the upgrade button was a dead option for them.
- **`SubscriptionPanel`** header — Ultra-active users see "Manage your
plan" instead of "Upgrade your plan".
- **`isAtTopTier(plan)`** helper added to `billing/constants.ts` so the
rule lives in one place. `SharedPlanCard`'s existing `plan === 'ultra'`
check is migrated to it; adding a future top tier (e.g. `enterprise`) is
now a one-line change to `PLAN_TIERS`.

Non-top-tier users see no behavior change.

## Test plan

- [x] Added unit tests in `tests/unit/billing/constants.unit.spec.ts`
locking `isAtTopTier` behavior (top tier / non-top / null / unknown).
- [x] Added unit test in `tests/unit/components/UserMenu.unit.spec.tsx`
for `active + ultra → subscription.manage`.
- [x] Audited existing tests for regressions — `UserMenu`,
`SubscriptionPanel`, `SubscriptionPanel-extras`, `SharedPlanCard` all
use `plan: 'pro'` / `null` defaults; none assert against the
Ultra-specific copy.
- [ ] Manual: log in locally with `BillingMockSelector → "Active —
Ultra"` → confirm "Manage" in avatar dropdown + "Manage your plan" panel
header; toggle back to "Active — Pro" → confirms "Upgrade" returns.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Ultra-tier users had no upgrade path but still saw "Upgrade" copy in three places. Root cause: each callsite read `status` only (no `plan` awareness), and the one place that did check plan hardcoded `'ultra'` as a string rather than deriving from `PLAN_TIERS`.

- **`UserMenu`** — main CTA in the avatar dropdown now resolves to `subscription.manage` when an active user is at the top tier, instead of `subscription.upgrade`.
- **`UpgradePromptModal`** (`active-credits` context) — Ultra users now see a single `Add Credits` CTA instead of `[Add Credits] [Upgrade Plan]`; the upgrade button was a dead option for them.
- **`SubscriptionPanel`** header — Ultra-active users see "Manage your plan" instead of "Upgrade your plan".
- **`isAtTopTier(plan)`** helper added to `billing/constants.ts` so the rule lives in one place. `SharedPlanCard`'s existing `plan === 'ultra'` check is migrated to it; adding a future top tier (e.g. `enterprise`) is now a one-line change to `PLAN_TIERS`.

Non-top-tier users see no behavior change.

## Test plan

- [x] Added unit tests in `tests/unit/billing/constants.unit.spec.ts` locking `isAtTopTier` behavior (top tier / non-top / null / unknown).
- [x] Added unit test in `tests/unit/components/UserMenu.unit.spec.tsx` for `active + ultra → subscription.manage`.
- [x] Audited existing tests for regressions — `UserMenu`, `SubscriptionPanel`, `SubscriptionPanel-extras`, `SharedPlanCard` all use `plan: 'pro'` / `null` defaults; none assert against the Ultra-specific copy.
- [ ] Manual: log in locally with `BillingMockSelector → "Active — Ultra"` → confirm "Manage" in avatar dropdown + "Manage your plan" panel header; toggle back to "Active — Pro" → confirms "Upgrade" returns.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
