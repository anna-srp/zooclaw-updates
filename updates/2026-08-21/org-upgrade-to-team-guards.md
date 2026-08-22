---
title: "个人空间升级为团队时增加拦截校验，避免已购额度作废"
type: "Bug Fix"
priority: "高"
date: "2026-08-21"
status: "待审核"
channels: ""
---

# 个人空间升级为团队时增加拦截校验，避免已购额度作废

## 核心宣传点

把个人空间升级成团队会把计费主体切到团队账户，如果此时你名下还有正在续订的个人订阅，已经付过钱的额度会记在个人账户上、团队用不到，等于白花钱。现在升级前会先检查：账号所有者必须仍是该空间的有效成员、名下不能有还在续订的个人订阅（已在取消流程中的不算），并且升级与企业邀请转移不会同时进行、切换失败会整体回滚。命中任一条都会明确拦下并说明原因，而不是默默把额度弄丢。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `c1f3eae3302a460b5e24cc9546b6c5e714c47945`
- PR: #3410
- 作者: bill-srp
- 日期: 2026-08-21T10:21:40Z

### Commit Message

```
fix(org): harden personal org upgrade-to-team preconditions (#3410)

# What

Backend-only hardening for `POST
/internal/orgs/{org_id}/upgrade-to-team`, closing four gaps a logic
review found by comparing the upgrade against the enterprise invite
handoff (which already solves each of them). Spec:
`docs/superpowers/specs/2026-07-23-org-upgrade-to-team-design.md`,
section "Hardening follow-up (2026-08-14, Bill: backend-only,
hard-block)".

`upgrade_org_to_team` now runs, in order:

1. **Owner-membership guard** — the org owner (`created_by`) must hold
an *active* membership in the org, else 409
`org.upgrade.owner_not_active_member`. Without this, upgrading an
orphaned personal org (owner already handed off to an enterprise) would
rebind the owner's live billing key back to the old personal team.
2. **Personal-subscription hard-block** — new read-only helper
`list_blocking_personal_agreement_providers` (shares the handoff's
`_is_canceling` predicate); any renewable personal agreement → 409
`org.upgrade.personal_subscription_active` with providers in context.
Business mode bills usage to the team customer while personal
fulfillment credits the uid customer, so upgrading with a renewing
personal subscription strands paid credits. Already-canceling agreements
do not block (handoff semantics).
3. **Transition lease** — claims the same `billing_transition` lease the
handoff uses (`org_upgrade:{uuid}`, 300s; 409
`org.join.transition_in_progress` when held; released in `finally`),
making upgrade and an in-flight enterprise handoff mutually exclusive on
the owner's membership row. Owner membership is re-checked under the
lease.
4. **Verified key bind** — the bare `add_user_to_personal_team` call is
replaced with the handoff's `bind_and_verify_key` (bind + canonical
readback assertion), so a partial business-mode flip aborts before the
CAS commit instead of going undetected.

No console changes (Bill's call): the dashboard-console dialog already
renders 409 details generically. The operational sequence is: cancel
owner's personal subscription → upgrade → purchase enterprise plan →
invite members.

# Why

The invite handoff cancels personal subscriptions, leases the
transition, and verifies key readback precisely because flipping billing
to business mode is destructive when interleaved or half-applied. The
upgrade flips the same switch and had none of those guards.

# Test plan

- [x] Unit (`test_org_service.py`, 9 new): inactive/missing owner
membership → 409 before billing; active personal subscription → 409 with
provider context before billing; already-canceling agreement does not
block; lease held → 409; lease released on success and on billing
failure; owner membership re-checked after claim; readback mismatch
aborts before CAS; retry after partial bind failure completes
- [x] Unit (`test_personal_subscription_stop.py`): new helper shares the
handoff canceling predicate
- [x] BDD (`org_lifecycle.feature`, real mongo): upgrade blocked while
the owner has an active personal subscription; existing upgrade
scenarios unchanged
- [x] `bash scripts/verify-py.sh` green (ruff, ruff-format, pyright,
import-linter)
- [x] 170 unit tests across all org/handoff-adjacent suites + 5 BDD
scenarios pass locally after rebasing onto #3407 (which reworked
`personal_subscription_stop.py`; merge verified semantically clean —
`_is_canceling` unchanged)
- Full whole-app coverage gate left to CI (`claw-interface-quality`)
```

### PR Body

# What

Backend-only hardening for `POST /internal/orgs/{org_id}/upgrade-to-team`, closing four gaps a logic review found by comparing the upgrade against the enterprise invite handoff (which already solves each of them). Spec: `docs/superpowers/specs/2026-07-23-org-upgrade-to-team-design.md`, section "Hardening follow-up (2026-08-14, Bill: backend-only, hard-block)".

`upgrade_org_to_team` now runs, in order:

1. **Owner-membership guard** — the org owner (`created_by`) must hold an *active* membership in the org, else 409 `org.upgrade.owner_not_active_member`. Without this, upgrading an orphaned personal org (owner already handed off to an enterprise) would rebind the owner's live billing key back to the old personal team.
2. **Personal-subscription hard-block** — new read-only helper `list_blocking_personal_agreement_providers` (shares the handoff's `_is_canceling` predicate); any renewable personal agreement → 409 `org.upgrade.personal_subscription_active` with providers in context. Business mode bills usage to the team customer while personal fulfillment credits the uid customer, so upgrading with a renewing personal subscription strands paid credits. Already-canceling agreements do not block (handoff semantics).
3. **Transition lease** — claims the same `billing_transition` lease the handoff uses (`org_upgrade:{uuid}`, 300s; 409 `org.join.transition_in_progress` when held; released in `finally`), making upgrade and an in-flight enterprise handoff mutually exclusive on the owner's membership row. Owner membership is re-checked under the lease.
4. **Verified key bind** — the bare `add_user_to_personal_team` call is replaced with the handoff's `bind_and_verify_key` (bind + canonical readback assertion), so a partial business-mode flip aborts before the CAS commit instead of going undetected.

No console changes (Bill's call): the dashboard-console dialog already renders 409 details generically. The operational sequence is: cancel owner's personal subscription → upgrade → purchase enterprise plan → invite members.

# Why

The invite handoff cancels personal subscriptions, leases the transition, and verifies key readback precisely because flipping billing to business mode is destructive when interleaved or half-applied. The upgrade flips the same switch and had none of those guards.

# Test plan

- [x] Unit (`test_org_service.py`, 9 new): inactive/missing owner membership → 409 before billing; active personal subscription → 409 with provider context before billing; already-canceling agreement does not block; lease held → 409; lease released on success and on billing failure; owner membership re-checked after claim; readback mismatch aborts before CAS; retry after partial bind failure completes
- [x] Unit (`test_personal_subscription_stop.py`): new helper shares the handoff canceling predicate
- [x] BDD (`org_lifecycle.feature`, real mongo): upgrade blocked while the owner has an active personal subscription; existing upgrade scenarios unchanged
- [x] `bash scripts/verify-py.sh` green (ruff, ruff-format, pyright, import-linter)
- [x] 170 unit tests across all org/handoff-adjacent suites + 5 BDD scenarios pass locally after rebasing onto #3407 (which reworked `personal_subscription_stop.py`; merge verified semantically clean — `_is_canceling` unchanged)
- Full whole-app coverage gate left to CI (`claw-interface-quality`)

