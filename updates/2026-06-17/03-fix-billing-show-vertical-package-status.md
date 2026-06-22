---
title: "侧边栏与用量页正确展示企业垂直套餐订阅状态"
type: "产品基础功能更新"
priority: "中"
date: "2026-06-17"
status: "待审核"
channels: "Discord+changelog"
---
# 侧边栏与用量页正确展示企业垂直套餐订阅状态
## 核心宣传点
购买了企业垂直套餐（Vertical Plan）的用户，现在在侧边栏、用户菜单和用量页都能正确看到「Vertical Plan」订阅状态，团队非所有者成员也能继承正确的套餐展示，不再错误显示为 Pro 或 No Plan。
## 原始内容
fix(billing): show vertical package subscription status (#2501)

## Summary
- Surface enterprise vertical package subscription metadata through
billing summary, user responses, and credits-check responses.
- Show active enterprise package subscriptions as `Vertical Plan` across
sidebar/user menu/usage surfaces.
- Resolve team billing display context from the team owner while keeping
balances on the org billing team, so non-owner members inherit the
package display state.
- Avoid stale localStorage fallback after the billing hook has fetched
fresh null subscription metadata.

Linear:
https://linear.app/srpone/issue/ECA-1022/show-enterprise-package-subscription-status

## Root cause
Vertical package subscriptions are recorded as provider agreements on
the purchasing owner UID while credits are granted to the org
`billing_team_id`. The old UI mostly inferred labels from legacy `plan`
/ `user_type`, and team credits paths did not derive display metadata
from the team owner, so package users could fall back to `Pro` or `No
Plan` depending on which endpoint populated the view.

## Test plan
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_billing_summary_v2.py tests/unit/test_user_credits.py`
- [x] `pnpm exec vitest run
tests/unit/components/credits/CreditsDisplay.unit.spec.tsx
tests/unit/components/sidenav/UserInfoSection.unit.spec.tsx`
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh
web/app/src/components/credits/CreditsDisplay.tsx
web/app/src/components/sidenav/UserInfoSection.tsx
web/app/src/components/sidenav/SideNavUserSection.tsx
web/app/tests/unit/components/credits/CreditsDisplay.unit.spec.tsx
web/app/tests/unit/components/sidenav/UserInfoSection.unit.spec.tsx
web/app/src/components/billing/plan-label.ts
web/app/src/hooks/useBillingCredits.ts web/app/src/lib/api/user.ts
web/app/src/lib/auth/types.ts`
- [x] `bash scripts/verify-changed.sh`

## PR Description
## Summary
- Surface enterprise vertical package subscription metadata through billing summary, user responses, and credits-check responses.
- Show active enterprise package subscriptions as `Vertical Plan` across sidebar/user menu/usage surfaces.
- Resolve team billing display context from the team owner while keeping balances on the org billing team, so non-owner members inherit the package display state.
- Avoid stale localStorage fallback after the billing hook has fetched fresh null subscription metadata.

Linear: https://linear.app/srpone/issue/ECA-1022/show-enterprise-package-subscription-status

## Root cause
Vertical package subscriptions are recorded as provider agreements on the purchasing owner UID while credits are granted to the org `billing_team_id`. The old UI mostly inferred labels from legacy `plan` / `user_type`, and team credits paths did not derive display metadata from the team owner, so package users could fall back to `Pro` or `No Plan` depending on which endpoint populated the view.

## Test plan
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_billing_summary_v2.py tests/unit/test_user_credits.py`
- [x] `pnpm exec vitest run tests/unit/components/credits/CreditsDisplay.unit.spec.tsx tests/unit/components/sidenav/UserInfoSection.unit.spec.tsx`
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh web/app/src/components/credits/CreditsDisplay.tsx web/app/src/components/sidenav/UserInfoSection.tsx web/app/src/components/sidenav/SideNavUserSection.tsx web/app/tests/unit/components/credits/CreditsDisplay.unit.spec.tsx web/app/tests/unit/components/sidenav/UserInfoSection.unit.spec.tsx web/app/src/components/billing/plan-label.ts web/app/src/hooks/useBillingCredits.ts web/app/src/lib/api/user.ts web/app/src/lib/auth/types.ts`
- [x] `bash scripts/verify-changed.sh`

