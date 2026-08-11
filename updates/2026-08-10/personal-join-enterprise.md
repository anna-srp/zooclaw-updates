---
title: "个人账号可直接加入企业组织"
type: "新功能上线"
priority: "高"
date: "2026-08-10"
status: "待审核"
channels: ""
---

# 个人账号可直接加入企业组织

## 核心宣传点

已有个人账号的用户现在可以直接接受企业邀请、成为企业正式成员，无需另开新号；切换时会明确提示个人订阅与资源的停用范围。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `f4b9c441be948559611455390ab4a4cf33d845ea`
- PR: #3323

### Commit Message

```
feat(org): support personal users joining enterprise (#3323)

## Linear

N/A — no Linear issue was supplied.

## Summary

- allow an existing personal account to redeem an enterprise invite and
become a normal active enterprise member without a feature flag or
organization allowlist
- stop personal subscription renewal, then strictly stop personal v2
Computers and Engine Agents and disable user schedules and channel
bindings before switching billing ownership
- rebind the canonical user key to the enterprise Billing Team, verify
its non-secret billing readback, and atomically swap membership with
retry and compensation paths
- reuse the strict v2 cleanup abstraction for subscription-expiry
resource reclamation and add reconciliation, diagnostics, and a
pre-deploy invariant audit
- update enterprise-admin invite UX with explicit shutdown disclosure,
actionable provider/runtime/billing errors, retry support, and
enterprise redirect; iOS remains unchanged and no new collection/table
is introduced

## Cross-repo dependency

- Billing Gateway must be deployed first:
https://github.com/SerendipityOneInc/billing-gateway/pull/66

## Rollout

1. Merge and deploy the Billing Gateway dependency.
2. Run `python -m scripts.audit_existing_personal_enterprise_join_v2`
from `services/claw-interface` and repair any reported invariant
violations.
3. Deploy claw-interface, then enterprise-admin.

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] `pytest -q tests/unit/test_membership_service.py
tests/unit/test_routes_org_users.py
tests/unit/test_personal_enterprise_join.py` — 74 passed
- [x] broader task-related claw-interface regression — 463 passed
- [x] `pnpm lint` in `web/enterprise-admin`
- [x] `pnpm test` in `web/enterprise-admin` — 362 passed after merging
current `main`
- [x] `git diff --check`
```

### PR Body

## Linear

N/A — no Linear issue was supplied.

## Summary

- allow an existing personal account to redeem an enterprise invite and become a normal active enterprise member without a feature flag or organization allowlist
- stop personal subscription renewal, then strictly stop personal v2 Computers and Engine Agents and disable user schedules and channel bindings before switching billing ownership
- rebind the canonical user key to the enterprise Billing Team, verify its non-secret billing readback, and atomically swap membership with retry and compensation paths
- reuse the strict v2 cleanup abstraction for subscription-expiry resource reclamation and add reconciliation, diagnostics, and a pre-deploy invariant audit
- update enterprise-admin invite UX with explicit shutdown disclosure, actionable provider/runtime/billing errors, retry support, and enterprise redirect; iOS remains unchanged and no new collection/table is introduced

## Cross-repo dependency

- Billing Gateway must be deployed first: https://github.com/SerendipityOneInc/billing-gateway/pull/66

## Rollout

1. Merge and deploy the Billing Gateway dependency.
2. Run `python -m scripts.audit_existing_personal_enterprise_join_v2` from `services/claw-interface` and repair any reported invariant violations.
3. Deploy claw-interface, then enterprise-admin.

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] `pytest -q tests/unit/test_membership_service.py tests/unit/test_routes_org_users.py tests/unit/test_personal_enterprise_join.py` — 74 passed
- [x] broader task-related claw-interface regression — 463 passed
- [x] `pnpm lint` in `web/enterprise-admin`
- [x] `pnpm test` in `web/enterprise-admin` — 362 passed after merging current `main`
- [x] `git diff --check`

