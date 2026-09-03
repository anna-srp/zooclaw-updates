---
title: "修复：企业版「无限额度」成员的用量页永远显示 0"
type: "Bug Fix"
priority: "中"
date: "2026-09-02"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：企业版「无限额度」成员的用量页永远显示 0

## 核心宣传点

企业版里配置为 Unlimited（无限额度）LLM 配额的成员，不管实际花了多少，用量页始终显示 0。

根因不在我们的统计聚合，而在 LiteLLM：它只有在成员被加入「带预算字段的团队」时才会创建对应的成员计量记录。绑定到没有配额的企业团队的成员从来不会有这条记录，之后 LiteLLM 用更新语句去累加消费时匹配到 0 条文档，于是每一次增量都被静默丢弃——不报错、不打日志，就是永远的 0。结果最可能花得最多的无限额度成员，恰恰是完全没有被计量的那批人。

修复方式是在所有会绑定企业成员的入口之后补一次计量记录的确保动作：接受邀请/加入组织、个人版升企业版、暂停成员恢复、已有账号的企业交接、首次计费密钥初始化、套餐或模型权限重绑、团队组织创建，共七条路径。记录缺失时创建一条无限额度、只带周期窗口的记录；已存在则只重钉周期边界，保留成员原有配额和已累计的消费。这个调用是尽力而为且有 10 秒超时的，不会因为它失败而阻塞绑定本身。修复后成员从加入时刻起的用量都会被正常计量。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `4d9eedb4fa608252bc222490c3d4e488101f774c`
- PR: #3516
- 作者: sharplee-srp
- 日期: 2026-09-02T13:50:26Z

### Commit Message

```
feat(claw-interface): track Business member LLM usage from join time (#3516)

## Linear

_None — this came out of a production billing investigation, not a
tracked issue._

## Problem

Business members on an **Unlimited** LLM quota show `0` usage on the
Usage page no matter how much they actually spend.

Root cause is in LiteLLM, not in our aggregation: LiteLLM only creates a
`LiteLLM_TeamMembership` row when a member is *added to a team with
budget fields*. A member bound to a Business team without a quota never
gets that row. LiteLLM then increments member spend with an
`update_many` against the missing row, which matches zero documents and
**silently drops every increment** — no error, no log, just a permanent
`0`.

So the members most likely to spend the most (Unlimited) are exactly the
ones that are never metered.

## What this PR does

**1. Ensure the tracking row at every Business bind point.**

New `app/services/org/member_usage_tracking.py` wraps billing-gateway's
`ensure_tracking` mode: create an unlimited, window-only row when
missing; otherwise repin the period boundary while preserving the
member's quota and accumulated spend. It is called right after the key
bind in all seven paths:

- accept invite / join org
- personal to business upgrade
- suspended member resume
- existing-account enterprise handoff
- first billing-key bootstrap
- plan / model-access rebind
- team org creation

The call is **best-effort and time-boxed (10s)**: the bind has already
succeeded by the time it runs, so a failure or a `reset_pending` result
logs and continues rather than rolling anything back. `suspended`
members are included on purpose — suspend only moves the key to a
personal fallback team, so the Business membership row and its
accumulated spend survive and must stay pinned.

**2. Omitted-vs-null quota semantics on `POST
/orgs/{org_id}/users/{uid}/llm-quota`.**

An omitted `quota_credits` now means *repin only* (preserve the quota,
re-align the window); an explicit `null` means *clear the quota to
Unlimited*. `ge=1` is unchanged, so a `0` quota still cannot reach
billing-gateway.

**3. Unknown usage is explicit end to end.**

`tracking_status` is passed through from billing-gateway; when the
gateway omits it, `not_initialized` is derived from a missing
`budget_reset_at`, otherwise `tracked`. `used_credits` stays a non-null
number on the wire for backward compatibility, but enterprise-admin now
treats `tracking_status == "not_initialized"` as authoritative: it
displays `Unknown`, excludes the row from member totals/share and
usage-based filters, exports an unknown value in CSV, and offers an
Untracked filter. The Users table no longer renders `0 / quota` for an
untracked member.

The row Retry action sends `{}` to the existing quota endpoint, so an
admin can initialize/repin tracking without changing the member's quota.
`_to_public` also no longer requires a quota to report `reset_pending`,
so an Unlimited member's drifted window remains visible and retryable.

**4. Rollover hook now repins Unlimited members.**

After a credit reset LiteLLM recomputes the member budget from its own
clock and normalizes it to a *calendar-month* boundary. The rollover
hook previously skipped every member without a positive quota, so
Unlimited members drifted onto LiteLLM's month boundary and got reset
mid credit period — undercounting again. They are now aligned through
the same quota-preserving ensure call. Expired boundaries are still left
alone (LiteLLM's reset job has to zero the row before its boundary can
move). Concurrency stays 5; the deadline scales with member count
(`min(300, max(30, 2n))` s) and truncation is logged with a count.
Members who left the org are excluded. The ensure client falls back to
the legacy repin body on a 422 from an older gateway, so this hook keeps
working for limited members regardless of deploy order. The first
enterprise-package grant also runs the sweep so founding members get a
row as soon as a credit period exists.

Eligibility repository failures fail closed: if the org or membership
list cannot be read, no member is aligned. A confirmed absence of a
local org mapping retains the previous align-all fallback. Failed ensure
calls are not counted as settled, so any later timeout reports the true
number of unresolved members.

**5. Controlled backfill and production completion gate.**

`services/claw-interface/scripts/backfill_member_usage_tracking.py`
walks every `org_type=team` org and ensures a row for its `active` and
`suspended` members. `--dry-run` is the default, `--write` applies, and
`--verify` performs a fresh read-only completion check. The JSON reports
failed org/member counts plus remaining `members_not_initialized` and
`members_repin_needed`; verify exits non-zero while failures or fixable
rows remain.

The script reads first and only writes where the row is missing or
drifted, so it never clears a quota, never resets a spend counter, and
re-running a converged org is a no-op. Orgs with no current credit
period are counted as skipped rather than failing the walk.

The production procedure and gate are committed in
`docs/production-validation/2026-09-01-member-usage-tracking-rollout.md`.

## Rollout order

**The billing-gateway PR must deploy FIRST.**

- SerendipityOneInc/billing-gateway#69
(`feat/member-usage-tracking-ensure`).
- Then deploy claw-interface and enterprise-admin from this PR.
- Run the reviewed dry-run, one write, and final `--verify` from the
production runbook.
- Production completion requires `converged=true`, zero org/member
failures, `members_not_initialized=0`, and `members_repin_needed=0`.

The contract changes are backward compatible: an older billing-gateway
returns **422** on the unknown `ensure_tracking` field, and the
best-effort wrapper tolerates that (logs and continues, bind is
unaffected). So merging this first is safe but inert — no tracking rows
get created until billing-gateway ships.

## Test plan

- [x] Backend PR-related unit tests: **256 passed**; backfill targeted
suite: **16 passed**.
- [x] Changed backend files: Ruff check + format passed; Pyright has 0
errors; import-linter keeps all 8 contracts.
- [x] enterprise-admin targeted tests: **69 passed**; full suite under
CI's UTC timezone: **426 passed**; ESLint and `tsc --noEmit` pass.
- [x] Fresh isolated A102 E2E against the production LiteLLM image
(`ghcr.io/berriai/litellm-database@sha256:8075b0…`) with real
Postgres/Mongo/Redis, billing-gateway#69, and this branch: **7 scenarios
/ 84 assertions passed**.
- [x] E2E completion gate: `--verify` exits 0 with `converged=true`,
zero failures, `members_not_initialized=0`, and
`members_repin_needed=0`.
- [x] Real-browser enterprise-admin check: before backfill, the legacy
row shows `Unknown`, share `—`, and `Tracking not initialized`; after
backfill and one metered request it shows `6 credits / 16.7%` and no
tracking warning.

`verify-local --changed` still surfaces an unrelated repository-wide
Ruff baseline (72 lint findings and 20 format drifts outside this PR).
The changed files and all scoped checks above pass; unrelated files were
intentionally left untouched.

## Size override justification

The PR is **3287 changed lines** against the repository's 3000-line
budget. The 287-line overage comes from the reviewer-requested
unknown-state and rollover-failure coverage, backfill verification
tests, and the production rollout runbook. Splitting those from the
implementation would separate the safety gate and tests from the code
they validate, so `size-override` is applied for this review round.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01DN37xKgDJNupV4VSFYdjWY

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

```
## Linear

_None — this came out of a production billing investigation, not a tracked issue._

## Problem

Business members on an **Unlimited** LLM quota show `0` usage on the Usage page no matter how much they actually spend.

Root cause is in LiteLLM, not in our aggregation: LiteLLM only creates a `LiteLLM_TeamMembership` row when a member is *added to a team with budget fields*. A member bound to a Business team without a quota never gets that row. LiteLLM then increments member spend with an `update_many` against the missing row, which matches zero documents and **silently drops every increment** — no error, no log, just a permanent `0`.

So the members most likely to spend the most (Unlimited) are exactly the ones that are never metered.

## What this PR does

**1. Ensure the tracking row at every Business bind point.**

New `app/services/org/member_usage_tracking.py` wraps billing-gateway's `ensure_tracking` mode: create an unlimited, window-only row when missing; otherwise repin the period boundary while preserving the member's quota and accumulated spend. It is called right after the key bind in all seven paths:

- accept invite / join org
- personal to business upgrade
- suspended member resume
- existing-account enterprise handoff
- first billing-key bootstrap
- plan / model-access rebind
- team org creation

The call is **best-effort and time-boxed (10s)**: the bind has already succeeded by the time it runs, so a failure or a `reset_pending` result logs and continues rather than rolling anything back. `suspended` members are included on purpose — suspend only moves the key to a personal fallback team, so the Business membership row and its accumulated spend survive and must stay pinned.

**2. Omitted-vs-null quota semantics on `POST /orgs/{org_id}/users/{uid}/llm-quota`.**

An omitted `quota_credits` now means *repin only* (preserve the quota, re-align the window); an explicit `null` means *clear the quota to Unlimited*. `ge=1` is unchanged, so a `0` quota still cannot reach billing-gateway.

**3. Unknown usage is explicit end to end.**

`tracking_status` is passed through from billing-gateway; when the gateway omits it, `not_initialized` is derived from a missing `budget_reset_at`, otherwise `tracked`. `used_credits` stays a non-null number on the wire for backward compatibility, but enterprise-admin now treats `tracking_status == "not_initialized"` as authoritative: it displays `Unknown`, excludes the row from member totals/share and usage-based filters, exports an unknown value in CSV, and offers an Untracked filter. The Users table no longer renders `0 / quota` for an untracked member.

The row Retry action sends `{}` to the existing quota endpoint, so an admin can initialize/repin tracking without changing the member's quota. `_to_public` also no longer requires a quota to report `reset_pending`, so an Unlimited member's drifted window remains visible and retryable.

**4. Rollover hook now repins Unlimited members.**

After a credit reset LiteLLM recomputes the member budget from its own clock and normalizes it to a *calendar-month* boundary. The rollover hook previously skipped every member without a positive quota, so Unlimited members drifted onto LiteLLM's month boundary and got reset mid credit period — undercounting again. They are now aligned through the same quota-preserving ensure call. Expired boundaries are still left alone (LiteLLM's reset job has to zero the row before its boundary can move). Concurrency stays 5; the deadline scales with member count (`min(300, max(30, 2n))` s) and truncation is logged with a count. Members who left the org are excluded. The ensure client falls back to the legacy repin body on a 422 from an older gateway, so this hook keeps working for limited members regardless of deploy order. The first enterprise-package grant also runs the sweep so founding members get a row as soon as a credit period exists.

Eligibility repository failures fail closed: if the org or membership list cannot be read, no member is aligned. A confirmed absence of a local org mapping retains the previous align-all fallback. Failed ensure calls are not counted as settled, so any later timeout reports the true number of unresolved members.

**5. Controlled backfill and production completion gate.**

`services/claw-interface/scripts/backfill_member_usage_tracking.py` walks every `org_type=team` org and ensures a row for its `active` and `suspended` members. `--dry-run` is the default, `--write` applies, and `--verify` performs a fresh read-only completion check. The JSON reports failed org/member counts plus remaining `members_not_initialized` and `members_repin_needed`; verify exits non-zero while failures or fixable rows remain.

The script reads first and only writes where the row is missing or drifted, so it never clears a quota, never resets a spend counter, and re-running a converged org is a no-op. Orgs with no current credit period are counted as skipped rather than failing the walk.

The production procedure and gate are committed in `docs/production-validation/2026-09-01-member-usage-tracking-rollout.md`.

## Rollout order

**The billing-gateway PR must deploy FIRST.**

- SerendipityOneInc/billing-gateway#69 (`feat/member-usage-tracking-ensure`).
- Then deploy claw-interface and enterprise-admin from this PR.
- Run the reviewed dry-run, one write, and final `--verify` from the production runbook.
- Production completion requires `converged=true`, zero org/member failures, `members_not_initialized=0`, and `members_repin_needed=0`.

The contract changes are backward compatible: an older billing-gateway returns **422** on the unknown `ensure_tracking` field, and the best-effort wrapper tolerates that (logs and continues, bind is unaffected). So merging this first is safe but inert — no tracking rows get created until billing-gateway ships.

## Test plan

- [x] Backend PR-related unit tests: **256 passed**; backfill targeted suite: **16 passed**.
- [x] Changed backend files: Ruff check + format passed; Pyright has 0 errors; import-linter keeps all 8 contracts.
- [x] enterprise-admin targeted tests: **69 passed**; full suite under CI's UTC timezone: **426 passed**; ESLint and `tsc --noEmit` pass.
- [x] Fresh isolated A102 E2E against the production LiteLLM image (`ghcr.io/berriai/litellm-database@sha256:8075b0…`) with real Postgres/Mongo/Redis, billing-gateway#69, and this branch: **7 scenarios / 84 assertions passed**.
- [x] E2E completion gate: `--verify` exits 0 with `converged=true`, zero failures, `members_not_initialized=0`, and `members_repin_needed=0`.
- [x] Real-browser enterprise-admin check: before backfill, the legacy row shows `Unknown`, share `—`, and `Tracking not initialized`; after backfill and one metered request it shows `6 credits / 16.7%` and no tracking warning.

`verify-local --changed` still surfaces an unrelated repository-wide Ruff baseline (72 lint findings and 20 format drifts outside this PR). The changed files and all scoped checks above pass; unrelated files were intentionally left untouched.

## Size override justification

The PR is **3287 changed lines** against the repository's 3000-line budget. The 287-line overage comes from the reviewer-requested unknown-state and rollover-failure coverage, backfill verification tests, and the production rollout runbook. Splitting those from the implementation would separate the safety gate and tests from the code they validate, so `size-override` is applied for this review round.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01DN37xKgDJNupV4VSFYdjWY

```

