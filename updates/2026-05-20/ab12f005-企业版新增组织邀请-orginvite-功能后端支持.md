---
title: "企业版新增组织邀请（OrgInvite）功能后端支持"
type: "新功能上线"
priority: "中"
date: "2026-05-20"
status: "待审核"
channels: ""
repo: "ecap-workspace"
sha: "ab12f00588f30f1c171a0fdf5134654edbfe7e1a"
pr: 1771
---
# 企业版新增组织邀请（OrgInvite）功能后端支持

## 核心宣传点

企业版现在支持通过邀请码加入组织，管理员可邀请新成员加入企业账户。

## 原始内容

### Commit Message

```
feat(enterprise): OrgInvite schema, repo, and membership service (#1771)

## Summary

Implements spec §3.3 (org membership lifecycle: invite / join / suspend
/ resume / remove / list) on a dedicated `ecap-org-invite-codes`
collection that is intentionally independent of the legacy
`ecap-invite-codes` referral system. Org invites are 1-shot, expire in
30 days, are scoped to one email, and never propagate (no child-slots
chain).

- **`OrgInvite` Pydantic schema** — required `org_id`, `invite_role`,
`computer_quota`, `invited_email`; `used_by`/`used_at` track redemption;
no `max_bindings` since 1-shot is implicit.
- **`org_invite_repo`** — typed repo + atomic `claim_redemption` /
`release_redemption` CAS (via `mongo.update` wrapper) + bulk
`create_many` (best-effort `insert_many(ordered=False)`) + 4 indexes:
  - unique `code`
  - `(org_id, used_by)` compound — list pending + history
- partial unique `(invited_email, org_id)` where `used_by IS NULL AND
is_active == True` — prevents duplicate open invites
  - `expires_at` — for cleanup cron
- **`membership_service`** — `invite_user`, `join_org`, `suspend`,
`resume`, `remove`, `list_users`. `join_org`'s personal→team path
atomically suspends the personal `AccountOrg` before inserting the team
row (satisfies `unique_uid_active` partial index from PR #1748).
Compensation paths restore the personal row if claim or insert fails.
- **DuplicateKeyError disambiguation** — uses `details["keyPattern"]`
(structured, version-stable across pymongo) to distinguish "duplicate
pending email" from "duplicate code"; falls back to string match if
`details` is absent.

The legacy `ecap-invite-codes` system (referral chain, child slots,
multi-binding) is completely untouched — no imports of
`app.services.invite_code` or `app.database.invite_code_repo` anywhere
in the new code path. Legacy can be retired in a future PR without
affecting org membership.

**Email-binding** (verifying joiner's account email matches
`invite.invited_email`) is intentionally deferred to the route layer
(S1-15) — same pattern as `create_org`'s single-active-membership check
living at the route. Service stays a pure primitive; internal callers
(V2 register, migration, admin override) aren't forced around the
policy.

## Diff vs main

10 files, +2152/-16:

```
+ app/schema/org_invite.py                          (NEW)
+ app/database/org_invite_repo.py                   (NEW)
+ app/services/org/membership_service.py            (NEW)
+ tests/unit/test_org_invite_schema.py              (NEW)
+ tests/unit/test_org_invite_repo.py                (NEW)
+ tests/unit/test_membership_service.py             (NEW)
M app/database/collections.py                       (+1 — ORG_INVITE_COLLECTION const)
M app/lifetime.py                                   (+2 — ensure_indexes wiring)
M pyproject.toml                                    (+3 — C1/C4/C4b contracts)
M docs/superpowers/specs/2026-05-19-enterprise-phase1-backend.md  (§1.6 + new §1.6.1 OrgInvite section)
```

## Test plan

- [x] 56 unit tests for the new modules (org_invite schema/repo +
membership_service) — 100% line coverage on each
- [x] Full unit suite green locally (3399 passed)
- [x] ruff + format + pyright + lint-imports + 8 import-linter contracts
kept
- [x] Spot-checked legacy `ecap-invite-codes` tests still pass — they
were not touched
- [x] Spot-checked `lint-imports` confirms zero imports from
`app.services.invite_code` / `app.database.invite_code_repo` in the new
code
- [x] Independent code-review pass: 0 critical, 0 high, 4 medium (M2 fix
landed in `8c6524c2`), 4 low/observations

## Follow-ups (not in this PR)

- **S1-15 routes** — `POST /orgs/{org_id}/invite`, `POST
/users/join-org`, lifecycle endpoints. Email-binding enforcement lives
here.
- **`quota_total` semantics** — currently approximated as
`default_computer_quota * member_count` with a TODO; needs a real
org-cap field when billing-tier integration lands.
- **Compensation double-failure** — if both `account_org.create` AND
personal-restore fail, only an ERROR log signals it. A future hardening
pass should write an operational record.
- **Retire legacy `ecap-invite-codes`** — independent PR once warm-pool,
trial-credits, and Stripe webhook integrations are migrated off it.
```

### PR Description

## Summary

Implements spec §3.3 (org membership lifecycle: invite / join / suspend / resume / remove / list) on a dedicated `ecap-org-invite-codes` collection that is intentionally independent of the legacy `ecap-invite-codes` referral system. Org invites are 1-shot, expire in 30 days, are scoped to one email, and never propagate (no child-slots chain).

- **`OrgInvite` Pydantic schema** — required `org_id`, `invite_role`, `computer_quota`, `invited_email`; `used_by`/`used_at` track redemption; no `max_bindings` since 1-shot is implicit.
- **`org_invite_repo`** — typed repo + atomic `claim_redemption` / `release_redemption` CAS (via `mongo.update` wrapper) + bulk `create_many` (best-effort `insert_many(ordered=False)`) + 4 indexes:
  - unique `code`
  - `(org_id, used_by)` compound — list pending + history
  - partial unique `(invited_email, org_id)` where `used_by IS NULL AND is_active == True` — prevents duplicate open invites
  - `expires_at` — for cleanup cron
- **`membership_service`** — `invite_user`, `join_org`, `suspend`, `resume`, `remove`, `list_users`. `join_org`'s personal→team path atomically suspends the personal `AccountOrg` before inserting the team row (satisfies `unique_uid_active` partial index from PR #1748). Compensation paths restore the personal row if claim or insert fails.
- **DuplicateKeyError disambiguation** — uses `details["keyPattern"]` (structured, version-stable across pymongo) to distinguish "duplicate pending email" from "duplicate code"; falls back to string match if `details` is absent.

The legacy `ecap-invite-codes` system (referral chain, child slots, multi-binding) is completely untouched — no imports of `app.services.invite_code` or `app.database.invite_code_repo` anywhere in the new code path. Legacy can be retired in a future PR without affecting org membership.

**Email-binding** (verifying joiner's account email matches `invite.invited_email`) is intentionally deferred to the route layer (S1-15) — same pattern as `create_org`'s single-active-membership check living at the route. Service stays a pure primitive; internal callers (V2 register, migration, admin override) aren't forced around the policy.

## Diff vs main

10 files, +2152/-16:

```
+ app/schema/org_invite.py                          (NEW)
+ app/database/org_invite_repo.py                   (NEW)
+ app/services/org/membership_service.py            (NEW)
+ tests/unit/test_org_invite_schema.py              (NEW)
+ tests/unit/test_org_invite_repo.py                (NEW)
+ tests/unit/test_membership_service.py             (NEW)
M app/database/collections.py                       (+1 — ORG_INVITE_COLLECTION const)
M app/lifetime.py                                   (+2 — ensure_indexes wiring)
M pyproject.toml                                    (+3 — C1/C4/C4b contracts)
M docs/superpowers/specs/2026-05-19-enterprise-phase1-backend.md  (§1.6 + new §1.6.1 OrgInvite section)
```

## Test plan

- [x] 56 unit tests for the new modules (org_invite schema/repo + membership_service) — 100% line coverage on each
- [x] Full unit suite green locally (3399 passed)
- [x] ruff + format + pyright + lint-imports + 8 import-linter contracts kept
- [x] Spot-checked legacy `ecap-invite-codes` tests still pass — they were not touched
- [x] Spot-checked `lint-imports` confirms zero imports from `app.services.invite_code` / `app.database.invite_code_repo` in the new code
- [x] Independent code-review pass: 0 critical, 0 high, 4 medium (M2 fix landed in `8c6524c2`), 4 low/observations

## Follow-ups (not in this PR)

- **S1-15 routes** — `POST /orgs/{org_id}/invite`, `POST /users/join-org`, lifecycle endpoints. Email-binding enforcement lives here.
- **`quota_total` semantics** — currently approximated as `default_computer_quota * member_count` with a TODO; needs a real org-cap field when billing-tier integration lands.
- **Compensation double-failure** — if both `account_org.create` AND personal-restore fail, only an ERROR log signals it. A future hardening pass should write an operational record.
- **Retire legacy `ecap-invite-codes`** — independent PR once warm-pool, trial-credits, and Stripe webhook integrations are migrated off it.
