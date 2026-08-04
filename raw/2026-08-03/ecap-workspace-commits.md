# SerendipityOneInc/ecap-workspace commits — 2026-08-03

## docs(packs): stop claiming a failed register wrote nothing (#3212)

- **SHA**: `12c1ec1b59ee6c019dca71e1bbc4dc0a9710b367`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-03T13:09:15Z

### Commit Message

```
docs(packs): stop claiming a failed register wrote nothing (#3212)

Two accuracy fixes from review of #3206. No behavior change.

**The log line overstated what a failure means.**
`_register_snapshot_atomically` logged `nothing was registered` on any
`DependencyNotReadyError`. But an Engine that committed and then lost
the response looks identical from this side, and in that case the
registry *does* hold the versions. The retry converges — same content,
same `content_hash`, same versions returned, snapshot row lands then —
so there is no inconsistency to fix. What was wrong is sending whoever
reads that log looking for an empty registry that may not be empty. It
now says the outcome is unknown and that no snapshot was persisted,
which is the part this side actually knows.

**The spec repeated that claim** and separately **got the request-count
arithmetic wrong**: the old path was one `:preflight` plus one upsert
per skill — `N+1`, not `2N+1`. That number was mine and it reached the
design doc unchecked.

123 passed on the two affected suites; ruff, format and ci-lint
01/02/04/05/06/07/08 clean.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01JksoXqdHArutJFifUtrKS6
```

### PR Body

```
Two accuracy fixes from review of #3206. No behavior change.

**The log line overstated what a failure means.** `_register_snapshot_atomically` logged `nothing was registered` on any `DependencyNotReadyError`. But an Engine that committed and then lost the response looks identical from this side, and in that case the registry *does* hold the versions. The retry converges — same content, same `content_hash`, same versions returned, snapshot row lands then — so there is no inconsistency to fix. What was wrong is sending whoever reads that log looking for an empty registry that may not be empty. It now says the outcome is unknown and that no snapshot was persisted, which is the part this side actually knows.

**The spec repeated that claim** and separately **got the request-count arithmetic wrong**: the old path was one `:preflight` plus one upsert per skill — `N+1`, not `2N+1`. That number was mine and it reached the design doc unchecked.

123 passed on the two affected suites; ruff, format and ci-lint 01/02/04/05/06/07/08 clean.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01JksoXqdHArutJFifUtrKS6
```

---

## feat(enterprise): add member AI credit quotas (#3205)

- **SHA**: `d055c5854fb981381092e8ea10e32c91e06d065e`
- **作者**: kaka-srp
- **日期**: 2026-08-03T12:54:30Z

### Commit Message

```
feat(enterprise): add member AI credit quotas (#3205)

## Linear


https://linear.app/srpone/issue/ECA-1353/add-enterprise-member-llm-credit-quotas

## Summary

- Add enterprise member AI credit quotas with Unlimited and fixed-credit
configurations in the Users page, while keeping the existing Computer
quota column visible.
- Derive each member quota window from the organization purchase period
and pass the exact period-end timestamp to LiteLLM through Billing
Gateway.
- Surface quota update failures on the affected member row with a
prominent Retry action, including failures before a quota projection is
available.
- Re-pin only existing finite quotas during billing-period rollover
without rewriting their configured limit. The best-effort operation uses
concurrency 5 and a 30-second total deadline covering both projection
read and mutation fanout.
- Map a pending LiteLLM reset boundary to a stable row-level conflict so
administrators can retry after the reset completes.
- Accept LiteLLM's approximately 60-second cache propagation delay and
at-most-one-admitted-request overshoot; no synchronizer, cache
invalidation, or per-request Billing Gateway lookup is added.
- Update the MVP design with the final period-boundary, readback,
failure, and deployment contracts.

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] Enterprise Admin TypeScript and ESLint
- [x] Enterprise Admin Vitest: 48 files / 319 tests passed; final
UserTable regression: 10 tests passed
- [x] Claw Interface focused quota, route, client, and fulfillment
tests: 142 passed
- [x] Claw Interface ruff, format, pyright, and import-contract checks
- [x] True local-to-staging E2E: period `2026-07-12` to `2026-08-12`
propagated exactly
- [x] True quota enforcement: configured 3 credits, real model traffic
reached 429, then restored to Unlimited
- [x] Failure UX: stopped local Billing Gateway, observed member-row
error and successful Retry after restart

## Deployment

Deploy [Billing Gateway PR
#65](https://github.com/SerendipityOneInc/billing-gateway/pull/65)
first, then this PR.
```

### PR Body

```
## Linear

https://linear.app/srpone/issue/ECA-1353/add-enterprise-member-llm-credit-quotas

## Summary

- Add enterprise member AI credit quotas with Unlimited and fixed-credit configurations in the Users page, while keeping the existing Computer quota column visible.
- Derive each member quota window from the organization purchase period and pass the exact period-end timestamp to LiteLLM through Billing Gateway.
- Surface quota update failures on the affected member row with a prominent Retry action, including failures before a quota projection is available.
- Re-pin only existing finite quotas during billing-period rollover without rewriting their configured limit. The best-effort operation uses concurrency 5 and a 30-second total deadline covering both projection read and mutation fanout.
- Map a pending LiteLLM reset boundary to a stable row-level conflict so administrators can retry after the reset completes.
- Accept LiteLLM's approximately 60-second cache propagation delay and at-most-one-admitted-request overshoot; no synchronizer, cache invalidation, or per-request Billing Gateway lookup is added.
- Update the MVP design with the final period-boundary, readback, failure, and deployment contracts.

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] Enterprise Admin TypeScript and ESLint
- [x] Enterprise Admin Vitest: 48 files / 319 tests passed; final UserTable regression: 10 tests passed
- [x] Claw Interface focused quota, route, client, and fulfillment tests: 142 passed
- [x] Claw Interface ruff, format, pyright, and import-contract checks
- [x] True local-to-staging E2E: period `2026-07-12` to `2026-08-12` propagated exactly
- [x] True quota enforcement: configured 3 credits, real model traffic reached 429, then restored to Unlimited
- [x] Failure UX: stopped local Billing Gateway, observed member-row error and successful Retry after restart

## Deployment

Deploy [Billing Gateway PR #65](https://github.com/SerendipityOneInc/billing-gateway/pull/65) first, then this PR.

```

---

## feat(packs): register pack skills atomically and drop the preflight layer (#3206)

- **SHA**: `3a5cc013c3c106fc04462979aacb1c127f607e3a`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-03T12:15:40Z

### Commit Message

```
feat(packs): register pack skills atomically and drop the preflight layer (#3206)

## What

Switch the V2 pack-skill projection to zooclaw-engine#609's atomic batch
route
`POST /admin/v1/skills/pack/{pack_id}:register`, and delete the entire
preflight
layer added in #3197.

## Why the preflight is deleted, not simplified

The preflight had exactly one premise: **the registration was not
atomic**, so
the whole set had to be validated before any of it was written durably.

`:register` removes that premise. It runs `preparePackSkillSnapshot` —
literally
the same function `:preflight` used, same name / frontmatter /
file-manifest /
content-hash / prompt-version normalization — and then writes every
skill inside
one PostgreSQL transaction. A failure on the Nth skill leaves no row for
the
first N-1.

So a preceding preflight now adds **zero** guarantee: it re-runs the
identical
validator, reaches the identical verdict, and its only measurable effect
is
sending a second copy of the whole inline base64 body. That is the exact
doubling of the whole-request size ceiling tracked in #3199. Keeping it
would be
paying twice for one answer.

## Why V1 is not switched

`_project_archive` is shared between V1 (`asset is None`) and V2.
`:register`,
like `:preflight` before it, only exists on newer Engines. Making V1
depend on it
would mean an Engine lagging the rollout breaks legacy Pack projections
too —
far past what enabling V2 publishing should touch, and the same
reasoning that
makes the build-readiness gate V2-only.

V1 keeps its per-skill `admin_upsert_pack_skill_version` loop, its
`except: continue` tolerance, and its "incomplete → log at error, skip
the
snapshot row, return normally" behavior, byte for byte.

The path is chosen by an explicit `atomic=` argument at the
`_project_archive`
call site (mirroring `preflight=asset is not None` from #3197), never
inferred
from `source_sha256 is None` inside the projection.

## What this closes in #3204

- **Closed — the write-time half, on V2.** A batch that fails partway no
longer
leaves registry residue, so the "partial write is tolerated, the install
path
rebuilds it" branch is gone from V2: a failure now writes nothing and
raises a
  retryable error instead of continuing to publish an Environment.
- **Still open — V1.** V1 keeps that branch, so #3204's description
continues to
  hold for the legacy path.

## Effect on #3199

Requests per V2 projection drop from **2N+1** (1 preflight + N upserts,
each
carrying its own body) to **1**. The known limitation itself is *not*
fixed: one
inline JSON body for the whole snapshot still has a whole-request size
ceiling
the per-skill path never had, and that single-request ceiling is
unchanged.

## Failure classification: unchanged

Every failure stays retryable (`DependencyNotReadyError` on
`run_guarded_engine_projection`'s 1s/5s/15s ladder). The reasoning never
depended
on the call being validate-only: the Engine still overloads
`invalid_request`
between its route layer and the snapshot validator's duplicate-name
check
(zooclaw-engine#607), and a proxy in front of it can still answer
400/413 with no
Engine envelope. A 200 whose body does not parse is wrapped the same
way, so it
cannot escape the ladder as an `ExternalServiceError`.

## Response coverage check — kept, for a different reason

`pack_id` plus the returned skill names must match what was submitted.
This is
**not** the removed preflight parity check moved over: the persisted
snapshot row
is *derived* from this response, so a truncated or partially-deployed
answer
taken at face value would persist a snapshot pinning fewer skills than
the Pack
actually has — and the install path trusts that snapshot instead of
rebuilding
from the archive. Same reason every field on `EnginePackSkillRegistered`
is
required: a lenient default would not fail loudly, it would silently pin
`skill_id=""` / `version=0`.

## Changes

- `app/schema/engine.py` — `EnginePackSkillRegistered` /
`EnginePackSkillsRegistered`
(all fields required); `EnginePackSkillPreflightSkill` /
`EnginePackSkillsPreflight` removed.
- `app/services/engine_client/_skills.py` —
`admin_register_pack_skills`;
`admin_preflight_pack_skills` removed; `_raise_for_preflight_status`
generalized
  to `_raise_for_pack_snapshot_status` with identical behavior.
- `app/services/pack_store/pack_skill_projection.py` —
`preflight_pack_skills` removed;
`register_pack_skills` split into an atomic (V2) and a per-skill (V1)
path.
- `app/services/pack_store/pack_environment_service.py` — `preflight=` →
`atomic=`.
-
`docs/superpowers/specs/2026-08-02-engine-runtime-asset-publishing-design.md`.

## Verification

- `ruff check` + `ruff format --check` clean; `pyright app/ tests/` 0
errors;
  `lint-imports` 8 contracts kept.
- ci-lint 01/02/04/05/06/07/08 pass (03 is a known local false red — the
local
ruff version scores `chat.py` below the allowlist on clean `main` too).
- `pytest tests/unit` — 2339 passed.
- Every new test was anti-vacuity checked by reverting the corresponding
implementation change and confirming it goes red (8 mutations: atomic
flag
ignored, coverage check removed, V1 forced onto the atomic route,
unparsable-200
no longer wrapped, wrong route path, `sourceLabel` dropped, schema
fields
  defaulted, HTTP status check removed).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01JksoXqdHArutJFifUtrKS6

Co-authored-by: Claude Opus 5 <noreply@anthropic.com>
```

### PR Body

```
## What

Switch the V2 pack-skill projection to zooclaw-engine#609's atomic batch route
`POST /admin/v1/skills/pack/{pack_id}:register`, and delete the entire preflight
layer added in #3197.

## Why the preflight is deleted, not simplified

The preflight had exactly one premise: **the registration was not atomic**, so
the whole set had to be validated before any of it was written durably.

`:register` removes that premise. It runs `preparePackSkillSnapshot` — literally
the same function `:preflight` used, same name / frontmatter / file-manifest /
content-hash / prompt-version normalization — and then writes every skill inside
one PostgreSQL transaction. A failure on the Nth skill leaves no row for the
first N-1.

So a preceding preflight now adds **zero** guarantee: it re-runs the identical
validator, reaches the identical verdict, and its only measurable effect is
sending a second copy of the whole inline base64 body. That is the exact
doubling of the whole-request size ceiling tracked in #3199. Keeping it would be
paying twice for one answer.

## Why V1 is not switched

`_project_archive` is shared between V1 (`asset is None`) and V2. `:register`,
like `:preflight` before it, only exists on newer Engines. Making V1 depend on it
would mean an Engine lagging the rollout breaks legacy Pack projections too —
far past what enabling V2 publishing should touch, and the same reasoning that
makes the build-readiness gate V2-only.

V1 keeps its per-skill `admin_upsert_pack_skill_version` loop, its
`except: continue` tolerance, and its "incomplete → log at error, skip the
snapshot row, return normally" behavior, byte for byte.

The path is chosen by an explicit `atomic=` argument at the `_project_archive`
call site (mirroring `preflight=asset is not None` from #3197), never inferred
from `source_sha256 is None` inside the projection.

## What this closes in #3204

- **Closed — the write-time half, on V2.** A batch that fails partway no longer
  leaves registry residue, so the "partial write is tolerated, the install path
  rebuilds it" branch is gone from V2: a failure now writes nothing and raises a
  retryable error instead of continuing to publish an Environment.
- **Still open — V1.** V1 keeps that branch, so #3204's description continues to
  hold for the legacy path.

## Effect on #3199

Requests per V2 projection drop from **2N+1** (1 preflight + N upserts, each
carrying its own body) to **1**. The known limitation itself is *not* fixed: one
inline JSON body for the whole snapshot still has a whole-request size ceiling
the per-skill path never had, and that single-request ceiling is unchanged.

## Failure classification: unchanged

Every failure stays retryable (`DependencyNotReadyError` on
`run_guarded_engine_projection`'s 1s/5s/15s ladder). The reasoning never depended
on the call being validate-only: the Engine still overloads `invalid_request`
between its route layer and the snapshot validator's duplicate-name check
(zooclaw-engine#607), and a proxy in front of it can still answer 400/413 with no
Engine envelope. A 200 whose body does not parse is wrapped the same way, so it
cannot escape the ladder as an `ExternalServiceError`.

## Response coverage check — kept, for a different reason

`pack_id` plus the returned skill names must match what was submitted. This is
**not** the removed preflight parity check moved over: the persisted snapshot row
is *derived* from this response, so a truncated or partially-deployed answer
taken at face value would persist a snapshot pinning fewer skills than the Pack
actually has — and the install path trusts that snapshot instead of rebuilding
from the archive. Same reason every field on `EnginePackSkillRegistered` is
required: a lenient default would not fail loudly, it would silently pin
`skill_id=""` / `version=0`.

## Changes

- `app/schema/engine.py` — `EnginePackSkillRegistered` / `EnginePackSkillsRegistered`
  (all fields required); `EnginePackSkillPreflightSkill` / `EnginePackSkillsPreflight` removed.
- `app/services/engine_client/_skills.py` — `admin_register_pack_skills`;
  `admin_preflight_pack_skills` removed; `_raise_for_preflight_status` generalized
  to `_raise_for_pack_snapshot_status` with identical behavior.
- `app/services/pack_store/pack_skill_projection.py` — `preflight_pack_skills` removed;
  `register_pack_skills` split into an atomic (V2) and a per-skill (V1) path.
- `app/services/pack_store/pack_environment_service.py` — `preflight=` → `atomic=`.
- `docs/superpowers/specs/2026-08-02-engine-runtime-asset-publishing-design.md`.

## Verification

- `ruff check` + `ruff format --check` clean; `pyright app/ tests/` 0 errors;
  `lint-imports` 8 contracts kept.
- ci-lint 01/02/04/05/06/07/08 pass (03 is a known local false red — the local
  ruff version scores `chat.py` below the allowlist on clean `main` too).
- `pytest tests/unit` — 2339 passed.
- Every new test was anti-vacuity checked by reverting the corresponding
  implementation change and confirming it goes red (8 mutations: atomic flag
  ignored, coverage check removed, V1 forced onto the atomic route, unparsable-200
  no longer wrapped, wrong route path, `sourceLabel` dropped, schema fields
  defaulted, HTTP status check removed).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01JksoXqdHArutJFifUtrKS6

```

---

## feat(web): chat transcript and layout UX improvements (#3101)

- **SHA**: `98a6b5626fa3d7bcc037886eb9cea4ffb21953f3`
- **作者**: david-srp
- **日期**: 2026-08-03T12:08:00Z

### Commit Message

```
feat(web): chat transcript and layout UX improvements (#3101)

## 背景

聊天消息流与布局优化，并补齐旧 engine workspace 的前端头像解析。此前 #3100 已先行合入 P0 bugfix
子集；本分支现已合并最新 main，PR 只保留尚未合入的 transcript/layout 改动与本次头像修正。

## 改动

| 范围 | 说明 |
|---|---|
| 宽度统一 | session 路由与主 chat 使用一致的消息列宽 |
| 历史加载 | prepend 时保持滚动锚点，靠近顶部自动加载，按钮仍作兜底 |
| 流式指示 | 使用共享 `LoadingDots` 替代 ASCII 轮转 |
| 空状态 | 空会话展示头像、名称、问候语与最多 4 个 quick commands |
| 头像解析 | 新增共享 workspace presentation resolver；engine workspace 用
`pack_id` 查 pack avatar/animal，computer workspace 仍用 `agent_id`；主
chat、session thread、sidebar、composer 共用 |

## 测试

- [x] 头像修正红绿 TDD：旧实现无法用 `pack_id` 找到 engine avatar
- [x] 头像与四个入口相关测试：145 passed
- [x] merge 冲突相关测试：131 passed
- [x] `bash scripts/verify-web.sh ...`：governance
guards、tsc、vitest、eslint 全通过
- [x] pre-push：PR size 1577 / 3000，guards、tsc、eslint 全通过

## 部署注意

纯前端。#3099 已删除后端头像读时回填；旧 workspace 的头像展示由本 PR 的前端 pack metadata fallback
负责。

---------

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

```
## 背景

聊天消息流与布局优化，并补齐旧 engine workspace 的前端头像解析。此前 #3100 已先行合入 P0 bugfix 子集；本分支现已合并最新 main，PR 只保留尚未合入的 transcript/layout 改动与本次头像修正。

## 改动

| 范围 | 说明 |
|---|---|
| 宽度统一 | session 路由与主 chat 使用一致的消息列宽 |
| 历史加载 | prepend 时保持滚动锚点，靠近顶部自动加载，按钮仍作兜底 |
| 流式指示 | 使用共享 `LoadingDots` 替代 ASCII 轮转 |
| 空状态 | 空会话展示头像、名称、问候语与最多 4 个 quick commands |
| 头像解析 | 新增共享 workspace presentation resolver；engine workspace 用 `pack_id` 查 pack avatar/animal，computer workspace 仍用 `agent_id`；主 chat、session thread、sidebar、composer 共用 |

## 测试

- [x] 头像修正红绿 TDD：旧实现无法用 `pack_id` 找到 engine avatar
- [x] 头像与四个入口相关测试：145 passed
- [x] merge 冲突相关测试：131 passed
- [x] `bash scripts/verify-web.sh ...`：governance guards、tsc、vitest、eslint 全通过
- [x] pre-push：PR size 1577 / 3000，guards、tsc、eslint 全通过

## 部署注意

纯前端。#3099 已删除后端头像读时回填；旧 workspace 的头像展示由本 PR 的前端 pack metadata fallback 负责。

```

---

## fix(agent-builder): restore v1 pack test preview (#3207)

- **SHA**: `4cc91bf5b6128f3a40896c3be6cafc45febded72`
- **作者**: kaka-srp
- **日期**: 2026-08-03T12:03:07Z

### Commit Message

```
fix(agent-builder): restore v1 pack test preview (#3207)

## Summary

- restore channel-scoped preview behavior for `computer_v1` Agent
Builder Pack Test sessions
- restore v1 terminal-turn detection and Builder feedback from
`turn_status`
- ignore late v1 terminal statuses that belong to a turn before a reset
boundary
- keep `engine_v2` previews isolated by `root_post_id`
- add regression coverage for v1 null-root, plain-response feedback, and
the v2 missing-root guard

## Root cause

The Agent Builder v2 rollout made the shared preview chat require
`root_post_id` for every runtime. A v1 Pack Test preview is scoped by
its Mattermost DM channel and intentionally returns a null root, so the
composer stayed disabled even though the bot connection was healthy.

The same shared component also derived reviewable turns only from v2
`assistant_segment` metadata. Normal v1 replies terminate through
`turn_status` and do not carry that metadata, preventing automatic and
manual feedback from reaching Builder after chat connectivity was
restored.

## Validation

- `bash scripts/verify-changed.sh`
- `bash scripts/verify-local.sh --web-static
'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderTestChat.tsx'
web/app/tests/unit/app/agent-builder-test-chat.unit.spec.tsx`
- 23 targeted Vitest cases passed, including a real v1 terminal status
with a plain assistant reply and a late status after `/new`

## Risk

Frontend-only runtime branching. v1 restores its pre-v2 channel and
terminal-status behavior; v2 root-scoped and terminal-segment behavior
is unchanged.
```

### PR Body

```
## Summary

- restore channel-scoped preview behavior for `computer_v1` Agent Builder Pack Test sessions
- restore v1 terminal-turn detection and Builder feedback from `turn_status`
- ignore late v1 terminal statuses that belong to a turn before a reset boundary
- keep `engine_v2` previews isolated by `root_post_id`
- add regression coverage for v1 null-root, plain-response feedback, and the v2 missing-root guard

## Root cause

The Agent Builder v2 rollout made the shared preview chat require `root_post_id` for every runtime. A v1 Pack Test preview is scoped by its Mattermost DM channel and intentionally returns a null root, so the composer stayed disabled even though the bot connection was healthy.

The same shared component also derived reviewable turns only from v2 `assistant_segment` metadata. Normal v1 replies terminate through `turn_status` and do not carry that metadata, preventing automatic and manual feedback from reaching Builder after chat connectivity was restored.

## Validation

- `bash scripts/verify-changed.sh`
- `bash scripts/verify-local.sh --web-static 'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderTestChat.tsx' web/app/tests/unit/app/agent-builder-test-chat.unit.spec.tsx`
- 23 targeted Vitest cases passed, including a real v1 terminal status with a plain assistant reply and a late status after `/new`

## Risk

Frontend-only runtime branching. v1 restores its pre-v2 channel and terminal-status behavior; v2 root-scoped and terminal-segment behavior is unchanged.

```

---

## feat(packs): preflight pack skills before any registry write (#3197)

- **SHA**: `e89207828418374af62a4269cdb619fc39639a79`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-03T09:46:45Z

### Commit Message

```
feat(packs): preflight pack skills before any registry write (#3197)

## Why

`_project_archive` registered Pack-local Skills one at a time through
`admin_upsert_pack_skill_version`, and every one of those calls is
durable
(PostgreSQL row + blob + version-ready refresh). Validation happened
*inside* that
loop, so an archive whose Nth skill was malformed left skills 1..N-1
permanently
registered against the Pack. Nothing cleans that up: the failing archive
never gets
far enough to overwrite the partial snapshot, so the Pack keeps a
half-written skill
set until someone notices.

## What changed

Paired with **zooclaw-engine#603**, which adds
`POST /admin/v1/skills/pack/{pack_id}:preflight`. That route runs the
*identical*
name / frontmatter / file-manifest / content-hash / prompt-version
normalization as
the real upsert, but behind a service function that structurally has no
`RegistryDeps` — it cannot write PostgreSQL, R2, or registry rows. It
accepts inline
files only (rejects `upload_id`) and requires the existing admin service
token.

- `EngineClient.admin_preflight_pack_skills` — posts the whole inline
snapshot
  (base64 file content) and parses the returned immutable metadata.
- `app/services/pack_store/pack_skill_preflight.py` — the small service
call, with
  the failure-classification contract documented where it is enforced.
- `_project_archive` calls it immediately **before**
`_register_pack_skills`, so the
projection writes the whole snapshot or none of it. A zero-skill Pack
skips the
  call entirely.
- Spec
`docs/superpowers/specs/2026-08-02-engine-runtime-asset-publishing-design.md`
gains a "validate the skill snapshot before any registry write" section
naming
  zooclaw-engine#603.

Out of scope, untouched: `pack_environment_publish.py` and the
idempotency-key /
readiness logic owned by #3193.

## Error semantics (the load-bearing part)

| Outcome | Mapped to | Behaviour |
| --- | --- | --- |
| Engine rejects the snapshot — **400 / 413 carrying the Engine's
`{"error": {...}}` envelope** (`invalid_name`, `invalid_frontmatter`,
`invalid_files`, `unsupported_upload`, `payload_too_large`) |
`DomainValidationError` (`pack.skill_preflight_rejected`) | Permanent
verdict about these bytes. `context` carries the Engine's own message,
which names the offending skill and file (`skill 'writing' (SKILL.md):
description is required`), plus `org_id`, `submission_id`, and every
skill name. `run_guarded_engine_projection` logs it at **error** level
once and stops — it does not burn the retry budget on an outcome that
cannot change. |
| Preflight unreachable — transport failure, **5xx**, missing
`ZOOCLAW_ENGINE_ADMIN_TOKEN`, any other 4xx (**404** from an Engine
without #603, **401/403/429**), an **envelope-less 400/413** (an ingress
/ reverse proxy / service mesh verdict about the *request*, not the
skills), or a response that does not cover the submitted snapshot |
`DependencyNotReadyError` (`agent.runtime_unavailable`) | Says nothing
about the archive, so it stays on the bounded retry path. "Skills are
fine, Engine was busy / not deployed yet" never becomes a permanent
failure; an exhausted budget leaves the existing retryable
`pack_environment_not_ready` state that the admin rebuild endpoint
recovers. |

Both outcomes skip the registry writes, so an unreachable preflight
**defers** the
projection rather than half-registering it. Nothing is swallowed inside
the preflight
itself — the existing guard owns the swallow-into-logs policy.

## Review follow-ups (second commit)

Three findings from review, all confirmed against the code before
fixing:

1. **Only the Engine may condemn a Pack.** `_raise_for_preflight_status`
used to
decide "this snapshot is invalid" from the status code alone. Anything
between
claw-interface and the Engine — ingress, a reverse proxy, a service mesh
—
answers 400/413 without the Engine's `{"error": {...}}` envelope, so a
proxy's
request-body cap was being reported as "this Pack's skills are invalid"
and
permanently failing a valid archive. A rejection now additionally
requires the
Engine's envelope; envelope-less 4xx falls through to the retryable
path. The
   sibling `_raise_for_skill_status` already enforced this (`code in
_ZIP_VALIDATION_CODES`); the preflight path had dropped the
precondition. An
**enveloped** 413 stays permanent — retrying the same bytes cannot
succeed.
2. **A pass must cover what was submitted.** The response was never
checked
against the submission, so a truncated or partially-deployed Engine
answer
would have let the per-skill registration proceed for skills the
preflight
never validated — reintroducing exactly the partial registration this PR
exists to prevent. `project_pack_skills` now requires a matching
`pack_id`
and an identical skill-name multiset, and raises
`DependencyNotReadyError`
otherwise (an incomplete answer is not a verdict, so it stays
retryable).
The contract test that had frozen "submit 2, get 1 back" as acceptable
is
   split: the client keeps parsing leniently (documented as a transport
   boundary), and the parity refusal is asserted at the service layer.
3. **Equal diagnostics on the retryable path.** The explicit 5xx branch
reached
`_raise_for_status`, which raises the same `DependencyNotReadyError` /
   `agent.runtime_unavailable` — so this was a context difference, not a
behaviour change — but with no `pack_id` or `engine_error_type`. That
branch
is gone; every non-verdict status now shares one raise and one context.

## Why `pack_environment_service.py` got split

Rebasing onto #3193 would have put this file at **501 lines** — over the
500-line
CI guard. #3193 (+3) and this branch (+3) touch different regions, so
Git merges
them cleanly and only CI on `main` would have caught it. This is the
third PR in a
row to land in the 498–500 window, so the fix is a split rather than
another
shaved line.

The pack-skill step is the cohesive block that left: the preflight and
the durable
per-skill registration are only correct *together* — the preflight is
what makes
one-at-a-time registration safe to start. They now live in
`pack_skill_projection.py` behind a single `project_pack_skills` call,
so no caller
can register without validating first. `pack_environment_service.py`
drops to
**439 lines**. (`pack_skill_preflight.py`, added earlier in this same
PR, is the
file that was renamed — no history churn.)

## Known limitation filed

Batching the whole snapshot into one inline JSON body adds a
**whole-request** size
ceiling the per-skill path never had (Engine route 72 MB vs. 50 MB per
skill, and
base64 inflates bytes ~4/3). A large Pack of individually valid skills
can fail
preflight purely on combined payload size. Tracked in **#3199**, with
anchor
comments in `_skills.py` and `pack_skill_projection.py`. Not fixed here.

## Validation

- `pytest tests/unit/test_pack_environment_service.py
tests/unit/test_engine_client_skills.py` — 114 passed
- Full `pytest tests/unit` on the rebased tree — 7409 passed (1
unrelated local-sandbox failure: `test_ci_lint_deptry` needs a writable
`requirements.txt`)
- `ruff check` + `ruff format --check` — clean; `pyright app/ tests/` —
0 errors; `lint-imports` — 8 contracts kept
- `scripts/ci-lint/` 01/03/05/06/07/08 — pass
(`pack_environment_service.py` now **439**/500)
- Anti-vacuity: reverting each fix individually turns its own tests red
— envelope check → the 3 envelope-less-4xx cases fail with
`DomainValidationError`; parity check → both new service-layer tests
fail with `DID NOT RAISE`; unified 5xx raise →
`test_..._treats_engine_5xx_as_retryable` fails with `KeyError:
'pack_id'`.

New coverage: preflight accepted → both skills registered as before;
preflight
rejected → zero `admin_upsert_pack_skill_version` calls, zero snapshot
write, no
Environment create, error log with the Engine's per-skill reason;
rejection context
names the offending skill; unreachable preflight → full retry budget
consumed with
nothing registered; recovery on a later attempt registers normally;
client-side
tests for the request shape, the admin-token precondition, and each
status class. Added in the follow-up: envelope-less 400/413 stays
retryable; a preflight response missing a submitted skill or naming
another Pack writes nothing and stays retryable; 5xx carries `pack_id`;
the client's lenient parsing is asserted separately from the
service-layer parity refusal.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01JksoXqdHArutJFifUtrKS6

---------

Co-authored-by: Claude Opus 5 <noreply@anthropic.com>
```

### PR Body

```
## Why

`_project_archive` registered Pack-local Skills one at a time through
`admin_upsert_pack_skill_version`, and every one of those calls is durable
(PostgreSQL row + blob + version-ready refresh). Validation happened *inside* that
loop, so an archive whose Nth skill was malformed left skills 1..N-1 permanently
registered against the Pack. Nothing cleans that up: the failing archive never gets
far enough to overwrite the partial snapshot, so the Pack keeps a half-written skill
set until someone notices.

## What changed

Paired with **zooclaw-engine#603**, which adds
`POST /admin/v1/skills/pack/{pack_id}:preflight`. That route runs the *identical*
name / frontmatter / file-manifest / content-hash / prompt-version normalization as
the real upsert, but behind a service function that structurally has no
`RegistryDeps` — it cannot write PostgreSQL, R2, or registry rows. It accepts inline
files only (rejects `upload_id`) and requires the existing admin service token.

- `EngineClient.admin_preflight_pack_skills` — posts the whole inline snapshot
  (base64 file content) and parses the returned immutable metadata.
- `app/services/pack_store/pack_skill_preflight.py` — the small service call, with
  the failure-classification contract documented where it is enforced.
- `_project_archive` calls it immediately **before** `_register_pack_skills`, so the
  projection writes the whole snapshot or none of it. A zero-skill Pack skips the
  call entirely.
- Spec `docs/superpowers/specs/2026-08-02-engine-runtime-asset-publishing-design.md`
  gains a "validate the skill snapshot before any registry write" section naming
  zooclaw-engine#603.

Out of scope, untouched: `pack_environment_publish.py` and the idempotency-key /
readiness logic owned by #3193.

## Error semantics (the load-bearing part)

| Outcome | Mapped to | Behaviour |
| --- | --- | --- |
| Engine rejects the snapshot — **400 / 413 carrying the Engine's `{"error": {...}}` envelope** (`invalid_name`, `invalid_frontmatter`, `invalid_files`, `unsupported_upload`, `payload_too_large`) | `DomainValidationError` (`pack.skill_preflight_rejected`) | Permanent verdict about these bytes. `context` carries the Engine's own message, which names the offending skill and file (`skill 'writing' (SKILL.md): description is required`), plus `org_id`, `submission_id`, and every skill name. `run_guarded_engine_projection` logs it at **error** level once and stops — it does not burn the retry budget on an outcome that cannot change. |
| Preflight unreachable — transport failure, **5xx**, missing `ZOOCLAW_ENGINE_ADMIN_TOKEN`, any other 4xx (**404** from an Engine without #603, **401/403/429**), an **envelope-less 400/413** (an ingress / reverse proxy / service mesh verdict about the *request*, not the skills), or a response that does not cover the submitted snapshot | `DependencyNotReadyError` (`agent.runtime_unavailable`) | Says nothing about the archive, so it stays on the bounded retry path. "Skills are fine, Engine was busy / not deployed yet" never becomes a permanent failure; an exhausted budget leaves the existing retryable `pack_environment_not_ready` state that the admin rebuild endpoint recovers. |

Both outcomes skip the registry writes, so an unreachable preflight **defers** the
projection rather than half-registering it. Nothing is swallowed inside the preflight
itself — the existing guard owns the swallow-into-logs policy.

## Review follow-ups (second commit)

Three findings from review, all confirmed against the code before fixing:

1. **Only the Engine may condemn a Pack.** `_raise_for_preflight_status` used to
   decide "this snapshot is invalid" from the status code alone. Anything between
   claw-interface and the Engine — ingress, a reverse proxy, a service mesh —
   answers 400/413 without the Engine's `{"error": {...}}` envelope, so a proxy's
   request-body cap was being reported as "this Pack's skills are invalid" and
   permanently failing a valid archive. A rejection now additionally requires the
   Engine's envelope; envelope-less 4xx falls through to the retryable path. The
   sibling `_raise_for_skill_status` already enforced this (`code in
   _ZIP_VALIDATION_CODES`); the preflight path had dropped the precondition. An
   **enveloped** 413 stays permanent — retrying the same bytes cannot succeed.
2. **A pass must cover what was submitted.** The response was never checked
   against the submission, so a truncated or partially-deployed Engine answer
   would have let the per-skill registration proceed for skills the preflight
   never validated — reintroducing exactly the partial registration this PR
   exists to prevent. `project_pack_skills` now requires a matching `pack_id`
   and an identical skill-name multiset, and raises `DependencyNotReadyError`
   otherwise (an incomplete answer is not a verdict, so it stays retryable).
   The contract test that had frozen "submit 2, get 1 back" as acceptable is
   split: the client keeps parsing leniently (documented as a transport
   boundary), and the parity refusal is asserted at the service layer.
3. **Equal diagnostics on the retryable path.** The explicit 5xx branch reached
   `_raise_for_status`, which raises the same `DependencyNotReadyError` /
   `agent.runtime_unavailable` — so this was a context difference, not a
   behaviour change — but with no `pack_id` or `engine_error_type`. That branch
   is gone; every non-verdict status now shares one raise and one context.

## Why `pack_environment_service.py` got split

Rebasing onto #3193 would have put this file at **501 lines** — over the 500-line
CI guard. #3193 (+3) and this branch (+3) touch different regions, so Git merges
them cleanly and only CI on `main` would have caught it. This is the third PR in a
row to land in the 498–500 window, so the fix is a split rather than another
shaved line.

The pack-skill step is the cohesive block that left: the preflight and the durable
per-skill registration are only correct *together* — the preflight is what makes
one-at-a-time registration safe to start. They now live in
`pack_skill_projection.py` behind a single `project_pack_skills` call, so no caller
can register without validating first. `pack_environment_service.py` drops to
**439 lines**. (`pack_skill_preflight.py`, added earlier in this same PR, is the
file that was renamed — no history churn.)

## Known limitation filed

Batching the whole snapshot into one inline JSON body adds a **whole-request** size
ceiling the per-skill path never had (Engine route 72 MB vs. 50 MB per skill, and
base64 inflates bytes ~4/3). A large Pack of individually valid skills can fail
preflight purely on combined payload size. Tracked in **#3199**, with anchor
comments in `_skills.py` and `pack_skill_projection.py`. Not fixed here.

## Validation

- `pytest tests/unit/test_pack_environment_service.py tests/unit/test_engine_client_skills.py` — 114 passed
- Full `pytest tests/unit` on the rebased tree — 7409 passed (1 unrelated local-sandbox failure: `test_ci_lint_deptry` needs a writable `requirements.txt`)
- `ruff check` + `ruff format --check` — clean; `pyright app/ tests/` — 0 errors; `lint-imports` — 8 contracts kept
- `scripts/ci-lint/` 01/03/05/06/07/08 — pass (`pack_environment_service.py` now **439**/500)
- Anti-vacuity: reverting each fix individually turns its own tests red — envelope check → the 3 envelope-less-4xx cases fail with `DomainValidationError`; parity check → both new service-layer tests fail with `DID NOT RAISE`; unified 5xx raise → `test_..._treats_engine_5xx_as_retryable` fails with `KeyError: 'pack_id'`.

New coverage: preflight accepted → both skills registered as before; preflight
rejected → zero `admin_upsert_pack_skill_version` calls, zero snapshot write, no
Environment create, error log with the Engine's per-skill reason; rejection context
names the offending skill; unreachable preflight → full retry budget consumed with
nothing registered; recovery on a later attempt registers normally; client-side
tests for the request shape, the admin-token precondition, and each status class. Added in the follow-up: envelope-less 400/413 stays retryable; a preflight response missing a submitted skill or naming another Pack writes nothing and stays retryable; 5xx carries `pack_id`; the client's lenient parsing is asserted separately from the service-layer parity refusal.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01JksoXqdHArutJFifUtrKS6

```

---

## feat(whatsapp): run oura ring bridge on v2 engine agents (#3196)

- **SHA**: `d07d3cee633efb8cce56c34b7c009be4327301b4`
- **作者**: bill-srp
- **日期**: 2026-08-03T09:02:35Z

### Commit Message

```
feat(whatsapp): run oura ring bridge on v2 engine agents (#3196)

## Summary

Cut the WhatsApp bridge flow over from computer-runtime `oura_ring`
agents to **v2 engine agents** — no computer is created anywhere in the
WhatsApp path anymore.

Spec:
`docs/superpowers/specs/2026-08-03-whatsapp-engine-agent-design.md` ·
Plan: `docs/superpowers/plans/2026-08-03-whatsapp-engine-agent.md`

### claw-interface

- `POST /whatsapp/users/bind` accepts optional `user_access_token`; when
present and the engine workspace needs install/repair,
`install_engine_agent` is kicked as a tracked background task
(`agent.operation_in_progress` / `agent.already_installed` swallowed).
- `_resolve_routable_user` resolves via `pack_repo` (official
`oura_ring`) + `engine_agent_workspace_repo.get_by_pack`: routable ⇔
workspace `active` + complete Mattermost runtime + account MM token;
`installing` never double-installs; missing/`install_failed` marks
repair.
- Lookup (`GET /whatsapp/users/{wa_id}`) is now **read-only** — repair
is driven by the bridge.
- Outbound resolution (agent reply → WhatsApp) uses engine workspaces,
same fail-closed bot-author checks; new
`engine_agent_workspace_repo.get_active_by_mattermost_dm_channel` for
the uid-less fallback.
- All computer-path code deleted
(`_primary_or_bootstrap_primary_computer`, ready-polling loop, bootstrap
statuses).

### whatsapp-business-service

- `bindWhatsAppUser` forwards `user_access_token` (from user-interface's
`/admin/user/whatsapp-account` get-or-create, which the bridge already
calls).
- Non-routable lookups (`not_bound` or `bound_not_routable`) with
Account Service config re-run the idempotent auto-bind sequence — this
is the engine repair path. Without config, behavior is unchanged (notice
only).

### CI (riding along intentionally)

- `auto-review.yaml`: Claude review pinned to
`us.anthropic.claude-sonnet-5` (was reusable default
`us.anthropic.claude-sonnet-4-6`); Codex review pinned to
`gpt-5.6-terra`. Note: the first terra attempt 404'd on the Azure
endpoint (run 30789441913, no deployment at the time) — re-pinned on
request; this PR's review run is the live test. (Replaces closed #3195.)

## Test plan

- [x] claw-interface: full pytest — 7,406 unit passed, 260 BDD passed
(local Mongo); `verify-py.sh` green (ruff, ruff-format, pyright,
import-linter 8/8 contracts)
- [x] Rewritten `whatsapp_service.py` at 98.7% line coverage; whole-app
coverage gate re-checked in CI (local run under-reads due to env-skipped
suites)
- [x] whatsapp-business-service: `pnpm test` 68 passed, `pnpm
typecheck`, `pnpm build`
- [x] TDD per plan task (red→green verified in Codex session log)
- [ ] This PR's auto-review run confirms `us.anthropic.claude-sonnet-5`
(Bedrock) and `gpt-5.6-terra` (Azure) resolve
- [ ] Staging smoke after deploy: first message from unbound number →
"workspace is being prepared"; follow-up message routes into the engine
agent's Mattermost DM; agent reply returns to WhatsApp

## Rollout

Deploy claw-interface before whatsapp-business-service (bind schema
tolerates either order — the token field is ignored by an older backend,
so degradation is a skipped install, not an error). Environment
prerequisites before enabling: `AGENTS_V2_ENABLED` +
`AGENT_CHANNEL_SERVICE_URL/TOKEN` on claw-interface, and a current
engine runtime asset for the official `oura_ring` pack.
```

### PR Body

```
## Summary

Cut the WhatsApp bridge flow over from computer-runtime `oura_ring` agents to **v2 engine agents** — no computer is created anywhere in the WhatsApp path anymore.

Spec: `docs/superpowers/specs/2026-08-03-whatsapp-engine-agent-design.md` · Plan: `docs/superpowers/plans/2026-08-03-whatsapp-engine-agent.md`

### claw-interface

- `POST /whatsapp/users/bind` accepts optional `user_access_token`; when present and the engine workspace needs install/repair, `install_engine_agent` is kicked as a tracked background task (`agent.operation_in_progress` / `agent.already_installed` swallowed).
- `_resolve_routable_user` resolves via `pack_repo` (official `oura_ring`) + `engine_agent_workspace_repo.get_by_pack`: routable ⇔ workspace `active` + complete Mattermost runtime + account MM token; `installing` never double-installs; missing/`install_failed` marks repair.
- Lookup (`GET /whatsapp/users/{wa_id}`) is now **read-only** — repair is driven by the bridge.
- Outbound resolution (agent reply → WhatsApp) uses engine workspaces, same fail-closed bot-author checks; new `engine_agent_workspace_repo.get_active_by_mattermost_dm_channel` for the uid-less fallback.
- All computer-path code deleted (`_primary_or_bootstrap_primary_computer`, ready-polling loop, bootstrap statuses).

### whatsapp-business-service

- `bindWhatsAppUser` forwards `user_access_token` (from user-interface's `/admin/user/whatsapp-account` get-or-create, which the bridge already calls).
- Non-routable lookups (`not_bound` or `bound_not_routable`) with Account Service config re-run the idempotent auto-bind sequence — this is the engine repair path. Without config, behavior is unchanged (notice only).

### CI (riding along intentionally)

- `auto-review.yaml`: Claude review pinned to `us.anthropic.claude-sonnet-5` (was reusable default `us.anthropic.claude-sonnet-4-6`); Codex review pinned to `gpt-5.6-terra`. Note: the first terra attempt 404'd on the Azure endpoint (run 30789441913, no deployment at the time) — re-pinned on request; this PR's review run is the live test. (Replaces closed #3195.)

## Test plan

- [x] claw-interface: full pytest — 7,406 unit passed, 260 BDD passed (local Mongo); `verify-py.sh` green (ruff, ruff-format, pyright, import-linter 8/8 contracts)
- [x] Rewritten `whatsapp_service.py` at 98.7% line coverage; whole-app coverage gate re-checked in CI (local run under-reads due to env-skipped suites)
- [x] whatsapp-business-service: `pnpm test` 68 passed, `pnpm typecheck`, `pnpm build`
- [x] TDD per plan task (red→green verified in Codex session log)
- [ ] This PR's auto-review run confirms `us.anthropic.claude-sonnet-5` (Bedrock) and `gpt-5.6-terra` (Azure) resolve
- [ ] Staging smoke after deploy: first message from unbound number → "workspace is being prepared"; follow-up message routes into the engine agent's Mattermost DM; agent reply returns to WhatsApp

## Rollout

Deploy claw-interface before whatsapp-business-service (bind schema tolerates either order — the token field is ignored by an older backend, so degradation is a skipped install, not an error). Environment prerequisites before enabling: `AGENTS_V2_ENABLED` + `AGENT_CHANNEL_SERVICE_URL/TOKEN` on claw-interface, and a current engine runtime asset for the official `oura_ring` pack.

```

---

## docs: sync-docs weekly sweep (2026-08-03) (#3202)

- **SHA**: `ed02035a1e993840ff6c6903d8bc9ce5383f44b2`
- **作者**: srp-claude-assistant[bot]
- **日期**: 2026-08-03T08:22:15Z

### Commit Message

```
docs: sync-docs weekly sweep (2026-08-03) (#3202)

## Tier 1 — Deterministic fixes

- [x] **version → `services/claw-interface/AGENTS.md`**: Removed the
incorrect `(Python 3.11+ alias)` annotation from the `datetime.UTC`
guidance. The service requires Python ≥ 3.12 (per `pyproject.toml`), and
writing "3.11+ alias" implied the service supports 3.11. Fix: strip the
version qualifier — the statement that `datetime.UTC` is preferred over
`datetime.timezone.utc` remains accurate for any supported version.

## Tier 2 — Semantic fixes (with evidence)

- [x] **`ACCOUNT_SERVICE_URL` missing from `architecture.md` +
`architecture.zh-CN.md` env var table**
- **Evidence**: `.env.example` gained `ACCOUNT_SERVICE_URL` in the
`c1bdc6c..HEAD` window;
`services/claw-interface/app/auth/token_verifier.py:55` reads
`SETTINGS.ACCOUNT_SERVICE_URL or SETTINGS.NEXT_PUBLIC_ACCOUNT_URL` at
runtime; `services/claw-interface/app/settings.py:258` documents its
purpose (in-cluster user-interface URL). The env var table in Section E
existed for all other `user-interface` variables but was missing this
one.
- **Fix**: added one row to the env var table in both bilingual docs,
describing it as the optional in-cluster JWT verify URL that falls back
to `NEXT_PUBLIC_ACCOUNT_URL`.

**Docs changed**: `services/claw-interface/AGENTS.md`,
`architecture.md`, `architecture.zh-CN.md`
**Window reviewed**: `c1bdc6c1e7c7eb324c7083919e77a5f048878f8e..HEAD`
(approx last 90 days)

## Tier 3 — Suggestions (not applied)

- The Council feature (`services/claw-interface/app/routes/council.py`,
`app/services/council/`) is a new backend surface introduced in this
window. It is a product feature, not an onboarding-critical architecture
change, so it does not need documentation in the 7 target docs. If it
evolves into a standalone deployment or changes the overall topology,
`architecture.md` Section C would be the right place to add it.
- `ENGINE_PACK_RUNTIME_ASSETS_ENABLED` /
`ENGINE_PACK_RUNTIME_ASSETS_PACK_IDS` are new env vars for pack runtime
assets. They are feature-flag levers for internal rollout, not topology
env vars — out of scope for the architecture env var table (which tracks
service → service wiring). No update needed.

Co-authored-by: claude[bot] <41898282+claude[bot]@users.noreply.github.com>
Co-authored-by: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### PR Body

```
## Tier 1 — Deterministic fixes

- [x] **version → `services/claw-interface/AGENTS.md`**: Removed the incorrect `(Python 3.11+ alias)` annotation from the `datetime.UTC` guidance. The service requires Python ≥ 3.12 (per `pyproject.toml`), and writing "3.11+ alias" implied the service supports 3.11. Fix: strip the version qualifier — the statement that `datetime.UTC` is preferred over `datetime.timezone.utc` remains accurate for any supported version.

## Tier 2 — Semantic fixes (with evidence)

- [x] **`ACCOUNT_SERVICE_URL` missing from `architecture.md` + `architecture.zh-CN.md` env var table**
  - **Evidence**: `.env.example` gained `ACCOUNT_SERVICE_URL` in the `c1bdc6c..HEAD` window; `services/claw-interface/app/auth/token_verifier.py:55` reads `SETTINGS.ACCOUNT_SERVICE_URL or SETTINGS.NEXT_PUBLIC_ACCOUNT_URL` at runtime; `services/claw-interface/app/settings.py:258` documents its purpose (in-cluster user-interface URL). The env var table in Section E existed for all other `user-interface` variables but was missing this one.
  - **Fix**: added one row to the env var table in both bilingual docs, describing it as the optional in-cluster JWT verify URL that falls back to `NEXT_PUBLIC_ACCOUNT_URL`.

**Docs changed**: `services/claw-interface/AGENTS.md`, `architecture.md`, `architecture.zh-CN.md`
**Window reviewed**: `c1bdc6c1e7c7eb324c7083919e77a5f048878f8e..HEAD` (approx last 90 days)

## Tier 3 — Suggestions (not applied)

- The Council feature (`services/claw-interface/app/routes/council.py`, `app/services/council/`) is a new backend surface introduced in this window. It is a product feature, not an onboarding-critical architecture change, so it does not need documentation in the 7 target docs. If it evolves into a standalone deployment or changes the overall topology, `architecture.md` Section C would be the right place to add it.
- `ENGINE_PACK_RUNTIME_ASSETS_ENABLED` / `ENGINE_PACK_RUNTIME_ASSETS_PACK_IDS` are new env vars for pack runtime assets. They are feature-flag levers for internal rollout, not topology env vars — out of scope for the architecture env var table (which tracks service → service wiring). No update needed.

```

---

## fix(landing): force light mode across marketing UI (#3200)

- **SHA**: `b12770f0a67d31c6ebc5f6939e5bfa6465d1004b`
- **作者**: lynn Zhuang
- **日期**: 2026-08-03T08:19:46Z

### Commit Message

```
fix(landing): force light mode across marketing UI (#3200)

## Summary
- Force the complete public marketing route group (landing, features,
pricing, about/legal, and shared packs) to use light mode at both
pre-hydration bootstrap and React runtime.
- Preserve the user's saved theme preference so authenticated app routes
continue to honor dark mode.
- Add route-matrix unit coverage plus Playwright coverage for the
category-button hover state and the portaled template dialog.

## Root cause
The shared marketing wrapper pinned branded light tokens, but the
document could still retain the global `dark` class. The design-system
outline button's later `dark:hover` rule therefore overrode the landing
hover color, while Radix portal content rendered outside the
token-scoped wrapper. Enforcing the theme at the root provider across
every route rendered by `(marketing)` resolves both cases.

## Test plan
- [x] `bash scripts/verify-web.sh` on all changed frontend files (123
related unit tests, TypeScript, ESLint, and governance guards)
- [x] `bash scripts/verify-changed.sh`
- [x] Local Playwright landing theme scenario with a saved dark
preference, including category hover and template dialog assertions
```

### PR Body

```
## Summary
- Force the complete public marketing route group (landing, features, pricing, about/legal, and shared packs) to use light mode at both pre-hydration bootstrap and React runtime.
- Preserve the user's saved theme preference so authenticated app routes continue to honor dark mode.
- Add route-matrix unit coverage plus Playwright coverage for the category-button hover state and the portaled template dialog.

## Root cause
The shared marketing wrapper pinned branded light tokens, but the document could still retain the global `dark` class. The design-system outline button's later `dark:hover` rule therefore overrode the landing hover color, while Radix portal content rendered outside the token-scoped wrapper. Enforcing the theme at the root provider across every route rendered by `(marketing)` resolves both cases.

## Test plan
- [x] `bash scripts/verify-web.sh` on all changed frontend files (123 related unit tests, TypeScript, ESLint, and governance guards)
- [x] `bash scripts/verify-changed.sh`
- [x] Local Playwright landing theme scenario with a saved dark preference, including category hover and template dialog assertions

```

---

## fix(landing): complete localized starter copy (#3201)

- **SHA**: `a813d96f8024d73ab484ad62dd1e55b7db3579bd`
- **作者**: shana-srp
- **日期**: 2026-08-03T08:18:59Z

### Commit Message

```
fix(landing): complete localized starter copy (#3201)

## Summary

- align the landing-page hero, category labels, and footer copy with the
latest English source across all supported locales
- localize all starter prompt titles and prompt bodies instead of
forcing non-English locales to fall back to English
- localize slide-template names, metadata, descriptions, tags, and
best-use copy for every supported language
- restore the wide landing template-preview layout and add regression
coverage

## Root cause

The landing dictionaries only overrode a subset of the latest English
copy, while `getStarterPromptTranslation` explicitly forced every locale
except English and Chinese back to English. Template metadata supported
only English and Chinese. Separately, the shared dialog's responsive
`sm:max-w-lg` default overrode the landing preview's intended wide
layout.

## Test plan

- [x] ESLint for all changed locale, catalog, copy, and test files
- [x] locale/catalog unit tests: 10 passed
- [x] chat-ui starter component tests: 14 passed
- [x] prompt-key completeness audit: 0 missing keys for zh, ja, ko, fr,
de, it, es, ar, and pt
- [x] local preview routes returned HTTP 200

## Notes

- Full `tsc` remains blocked by a pre-existing `AgentPickerProps.open`
error on current `main`, unrelated to this PR.
- Template preview images contain baked-in source-language text and are
intentionally not dynamically translated.

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Body

```
## Summary

- align the landing-page hero, category labels, and footer copy with the latest English source across all supported locales
- localize all starter prompt titles and prompt bodies instead of forcing non-English locales to fall back to English
- localize slide-template names, metadata, descriptions, tags, and best-use copy for every supported language
- restore the wide landing template-preview layout and add regression coverage

## Root cause

The landing dictionaries only overrode a subset of the latest English copy, while `getStarterPromptTranslation` explicitly forced every locale except English and Chinese back to English. Template metadata supported only English and Chinese. Separately, the shared dialog's responsive `sm:max-w-lg` default overrode the landing preview's intended wide layout.

## Test plan

- [x] ESLint for all changed locale, catalog, copy, and test files
- [x] locale/catalog unit tests: 10 passed
- [x] chat-ui starter component tests: 14 passed
- [x] prompt-key completeness audit: 0 missing keys for zh, ja, ko, fr, de, it, es, ar, and pt
- [x] local preview routes returned HTTP 200

## Notes

- Full `tsc` remains blocked by a pre-existing `AgentPickerProps.open` error on current `main`, unrelated to this PR.
- Template preview images contain baked-in source-language text and are intentionally not dynamically translated.

```

---

## fix(agent-builder): separate workspace access from project state (#3194)

- **SHA**: `e5595b19cde7b893c028a57563aa656a4a8c5a6f`
- **作者**: kaka-srp
- **日期**: 2026-08-03T07:35:55Z

### Commit Message

```
fix(agent-builder): separate workspace access from project state (#3194)

## Summary
- keep persisted Agent Builder project lifecycle and workspace-health
state unchanged when workspace access is waiting or fails
- contain v1 with an independent browser-lock access state and a waiting
banner, without adding new v1 backend infrastructure
- gate v1 chat, Package/Test, and live model changes on active workspace
access
- return structured v2 lease-holder metadata, preserve same-project
multi-page acquisition, and classify waiting only from
`agent_builder.workspace_in_use`
- retry recoverable v2 renewal failures after lease expiry, prevent late
activation from restoring a lost lease, and distinguish live, expired,
recovery, and unknown holders
- keep Builder update/reinstall available as a control-plane recovery
action when workspace health is failed

Linear:
[ECA-1351](https://linear.app/srpone/issue/ECA-1351/separate-agent-builder-workspace-access-state)

## Root cause
The v1 Web Lock and v2 Mongo lease adapters converted temporary access
failures into copied `AgentBuilderProject` objects with
`builder_workspace_status = failed`. The UI therefore rendered a setup
failure even though the persisted project and workspace were healthy.
The v2 client also treated every HTTP 409 as workspace contention, so it
could not distinguish another project, a same-project operation, or an
unrelated conflict.

## Review fixes
- disable the v1 live model selector while another page holds the
workspace lock
- reacquire after retryable renewal errors outlive the v2 lease, without
retrying unrelated business conflicts
- ignore activation results from a lease cycle that has already been
invalidated
- filter expired page holders and avoid mislabeling unknown or
same-project page races
- classify expired running operations as recovery-required instead of
still active
- prioritize workspace-access waiting/error notices in the Test pane
while persisted workspace health remains ready
- preserve validation feedback while workspace access is only
initializing

## Test plan
- [x] targeted review-fix frontend suites: 87 passed, plus 9
status-notice tests after the final review fixes
- [x] targeted backend lease service tests: 14 passed
- [x] selected frontend guards, TypeScript, unit tests, and ESLint via
`scripts/verify-web.sh`
- [x] backend ruff, formatting, pyright, and import contracts via
`scripts/verify-py.sh`
- [x] changed-surface verification via `scripts/verify-changed.sh`
- [x] pre-commit and pre-push hooks
```

### PR Body

```
## Summary
- keep persisted Agent Builder project lifecycle and workspace-health state unchanged when workspace access is waiting or fails
- contain v1 with an independent browser-lock access state and a waiting banner, without adding new v1 backend infrastructure
- gate v1 chat, Package/Test, and live model changes on active workspace access
- return structured v2 lease-holder metadata, preserve same-project multi-page acquisition, and classify waiting only from `agent_builder.workspace_in_use`
- retry recoverable v2 renewal failures after lease expiry, prevent late activation from restoring a lost lease, and distinguish live, expired, recovery, and unknown holders
- keep Builder update/reinstall available as a control-plane recovery action when workspace health is failed

Linear: [ECA-1351](https://linear.app/srpone/issue/ECA-1351/separate-agent-builder-workspace-access-state)

## Root cause
The v1 Web Lock and v2 Mongo lease adapters converted temporary access failures into copied `AgentBuilderProject` objects with `builder_workspace_status = failed`. The UI therefore rendered a setup failure even though the persisted project and workspace were healthy. The v2 client also treated every HTTP 409 as workspace contention, so it could not distinguish another project, a same-project operation, or an unrelated conflict.

## Review fixes
- disable the v1 live model selector while another page holds the workspace lock
- reacquire after retryable renewal errors outlive the v2 lease, without retrying unrelated business conflicts
- ignore activation results from a lease cycle that has already been invalidated
- filter expired page holders and avoid mislabeling unknown or same-project page races
- classify expired running operations as recovery-required instead of still active
- prioritize workspace-access waiting/error notices in the Test pane while persisted workspace health remains ready
- preserve validation feedback while workspace access is only initializing

## Test plan
- [x] targeted review-fix frontend suites: 87 passed, plus 9 status-notice tests after the final review fixes
- [x] targeted backend lease service tests: 14 passed
- [x] selected frontend guards, TypeScript, unit tests, and ESLint via `scripts/verify-web.sh`
- [x] backend ruff, formatting, pyright, and import contracts via `scripts/verify-py.sh`
- [x] changed-surface verification via `scripts/verify-changed.sh`
- [x] pre-commit and pre-push hooks

```

---

## feat(skills): add CI registry-publish API for global skills (#3198)

- **SHA**: `e8475f3a2a1294bace48db8b78ab469e64b5b48c`
- **作者**: bill-srp
- **日期**: 2026-08-03T07:08:49Z

### Commit Message

```
feat(skills): add CI registry-publish API for global skills (#3198)

## Linear
<!-- 无对应 Linear issue；此 API 为 ecap-skills 发布流水线迁移的前置（spec/plan 见下） -->

## Summary
- Add `POST /skills/registry-publish`: a CI-only, token-gated endpoint
so the ecap-skills GitHub Actions workflow can publish global skills
into the v2 engine registry, replacing the current raw `aws s3 sync` to
the JuiceFS S3 gateway.
- Auth mirrors the agent-pack CI pattern: `X-Skills-Publish-Token`
header checked with `secrets.compare_digest` against the existing
`AGENT_STUDIO_PACK_UPDATE_TOKEN` (spec decision: same shared CI
credential, no new secret wiring).
- claw-interface stays a thin proxy: new engine-client method
`admin_upsert_global_skill_version` calls `PUT
/admin/v1/skills/global/{name}/versions` (multipart zip + optional
`sourceLabel`); the engine creates the skill row if missing, enforces
URL-name ↔ `SKILL.md` frontmatter match, and dedups versions by
`content_hash`, so CI retries and unchanged republishes are no-ops.
- New `global_publish_service` wraps the call in the existing
`await_engine_skill_call` error translation:
`invalid_frontmatter`/`invalid_name`/`invalid_zip` → 400 with the
engine's actionable message, `payload_too_large` → 413, everything else
masked.
- Design spec:
`docs/superpowers/specs/2026-08-03-skills-registry-publish-api-design.md`;
implementation plan:
`docs/superpowers/plans/2026-08-03-skills-registry-publish-api.md`.
- Out of scope (tracked in the spec): the ecap-skills workflow PR
(separate repo, after this deploys), removal/deprecation of delisted
skills, any frontend work.

## Test plan
- [x] Engine client: 4 new tests (multipart PUT shape + admin token
routing, `sourceLabel` omission, missing-admin-token guard before
request, typed zip-validation error) —
`tests/unit/test_engine_client_skills.py`
- [x] Service: forwarding, validation-error translation, unknown-error
masking — `tests/unit/test_global_publish_service.py`
- [x] Route: unconfigured-token 500, wrong/missing token 401, happy path
+ `source_label` default, size-cap rejection before service call;
route-shape/auth-matrix test updated to 7 routes with the CI route
explicitly excluded from user auth —
`tests/unit/test_skills_manager_routes.py`
- [x] `bash scripts/verify-py.sh` green (ruff, ruff format, pyright,
import-linter 8/8 contracts)
- [x] 86 tests passing across the seven skills-adjacent unit suites,
post-rebase onto latest main
```

### PR Body

```
## Linear
<!-- 无对应 Linear issue；此 API 为 ecap-skills 发布流水线迁移的前置（spec/plan 见下） -->

## Summary
- Add `POST /skills/registry-publish`: a CI-only, token-gated endpoint so the ecap-skills GitHub Actions workflow can publish global skills into the v2 engine registry, replacing the current raw `aws s3 sync` to the JuiceFS S3 gateway.
- Auth mirrors the agent-pack CI pattern: `X-Skills-Publish-Token` header checked with `secrets.compare_digest` against the existing `AGENT_STUDIO_PACK_UPDATE_TOKEN` (spec decision: same shared CI credential, no new secret wiring).
- claw-interface stays a thin proxy: new engine-client method `admin_upsert_global_skill_version` calls `PUT /admin/v1/skills/global/{name}/versions` (multipart zip + optional `sourceLabel`); the engine creates the skill row if missing, enforces URL-name ↔ `SKILL.md` frontmatter match, and dedups versions by `content_hash`, so CI retries and unchanged republishes are no-ops.
- New `global_publish_service` wraps the call in the existing `await_engine_skill_call` error translation: `invalid_frontmatter`/`invalid_name`/`invalid_zip` → 400 with the engine's actionable message, `payload_too_large` → 413, everything else masked.
- Design spec: `docs/superpowers/specs/2026-08-03-skills-registry-publish-api-design.md`; implementation plan: `docs/superpowers/plans/2026-08-03-skills-registry-publish-api.md`.
- Out of scope (tracked in the spec): the ecap-skills workflow PR (separate repo, after this deploys), removal/deprecation of delisted skills, any frontend work.

## Test plan
- [x] Engine client: 4 new tests (multipart PUT shape + admin token routing, `sourceLabel` omission, missing-admin-token guard before request, typed zip-validation error) — `tests/unit/test_engine_client_skills.py`
- [x] Service: forwarding, validation-error translation, unknown-error masking — `tests/unit/test_global_publish_service.py`
- [x] Route: unconfigured-token 500, wrong/missing token 401, happy path + `source_label` default, size-cap rejection before service call; route-shape/auth-matrix test updated to 7 routes with the CI route explicitly excluded from user auth — `tests/unit/test_skills_manager_routes.py`
- [x] `bash scripts/verify-py.sh` green (ruff, ruff format, pyright, import-linter 8/8 contracts)
- [x] 86 tests passing across the seven skills-adjacent unit suites, post-rebase onto latest main

```

---

## fix(claw-interface): confirm Environment builds before recording provenance (#3193)

- **SHA**: `87bd466731cd128b9d18167ac92334b878225fcd`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-03T07:06:55Z

### Commit Message

```
fix(claw-interface): confirm Environment builds before recording provenance (#3193)

## What staging showed

The `amazon-analyst` canary on staging looked healthy and was
permanently
uninstallable. Its submission carried `engine_environment_version = 3`
and an
`environment_source_sha256` matching the registered asset — the exact
shape
every recovery path reads as "projection complete". Environment `v3`,
`v4`, and
`v5` were all `status = failed`, `failure_stage = verifying`. Every
install
returned 409 `agent.environment_not_ready`, and #3188's same-SHA replay
heal
skipped the Pack because provenance was present. Re-projecting by hand
hit
Engine's `409 {"error":{"type":"idempotency_conflict"}}` until I
appended a
`:probe<ts>` suffix to the key.

(The builds failed because the staging root template is missing the
artifact-upload from zooclaw-engine#586, so verify fails on its first
check.
That is a separate operational fix on the Engine side and is not part of
this
PR — it is only how these two defects got exposed. Either one would have
turned
any single bad build into a permanently broken Pack.)

## P0-1: provenance recorded without confirming the build

`create_environment` / `create_environment_version` return as soon as
the
immutable version row exists; the E2B image build runs asynchronously
afterwards. `_create_or_version_environment` recorded
`engine_environment_version` + `environment_source_sha256` straight off
that
response, so a version that later failed was written as if it were
usable.

The projection now polls `get_environment_version` for that exact
version
before recording anything:

- `ready` → record provenance, return `True` (unchanged behavior)
- `failed` → record **nothing**, raise `DependencyNotReadyError`
  `agent.pack_environment_build_failed` with `environment_id`,
  `environment_version`, `failure_stage`, `failure_message` in context.
`run_guarded_engine_projection` logs it at error level; the caller's
request
  still succeeds, as before.
- Bounded: 5s interval, 10min total budget (observed builds settle in
16–40s).
  Timeout is treated exactly like `failed`.
- A read failure says nothing about the build, so transport/upstream
errors
  keep polling until the budget is spent; an explicit `failed` returns
  immediately.

Leaving no provenance behind is the point: the next CI re-run now trips
#3188's missing-provenance check and re-projects, instead of being told
the
projection is already complete.

## P0-2: immutable idempotency key blocked every re-projection

The key was `{submission_id}:{asset.sha256}` (or just `submission_id`
for V1).
Both parts are immutable, and Engine replays the first response for a
repeated
key — so after a failed build, admin `environment/rebuild`, the #3188
replay
heal, and future zooclaw-engine#604 reconciliation all replayed the
failed
version rather than producing a new one.

The key now carries a per-attempt suffix. **Invariant, documented on
`build_idempotency_key`:**

- stable across every Engine call *within* one publish attempt —
computed once
  per attempt and threaded through the upload declaration, the upload
finalize, and the version create (`build_environment_config` takes the
same
  value, so the declare/finalize path stays consistent);
- different for every *new* attempt, so a re-projection actually
rebuilds.

A useful side effect: the bounded in-process retry now retries a flaky
build
under a fresh key instead of re-reading the same failed version.

## Structure

The build wait, the key builder, and the provenance write moved to a new
`app/services/pack_store/pack_environment_publish.py`.
`pack_environment_service.py` was 495 of its 500 permitted lines, so the
polling logic could not live there; it is now 492.

## Verification

- `tests/unit/test_pack_environment_service.py`: 56 passed (45
pre-existing,
11 new). New coverage: `ready` records provenance for the exact created
version; `failed` records nothing and raises the new code with its
context;
non-terminal statuses poll on; an unreadable status keeps polling; both
the
build-never-settles and status-unreadable paths are bounded; the key is
  stable across declare/finalize/create inside one attempt and different
across attempts; a failed engine build exhausts retries with 5 distinct
keys
  and no provenance write.
- Full `tests/unit`: 7403 passed. The 2 failures in
`test_ci_lint_deptry.py`
are environmental — this fresh worktree has no local `.venv`, so
`deptry` is
  not on PATH; the same tests pass in a worktree that has one.
- `ruff check` + `ruff format --check` clean on `app` and `tests`.
- `pyright`: 0 errors on all three changed Python files.
- `scripts/ci-lint/01-file-length.sh` with `GITHUB_BASE_REF=main`: no
new
  violations.

## Relationship to other work

- **#3188** (same-SHA replay heal) is what this unblocks. Its
missing-provenance check was correct; it was being fed a false positive.
With P0-1, a failed build leaves no provenance, so the next release
re-run
  heals it; with P0-2, that heal can actually produce a new build.
- **zooclaw-engine#604** (durable autonomous reconciliation) inherits
both
properties — it will see failed builds as un-projected and will be able
to
  re-publish.
- **zooclaw-engine#586** (staging root template artifact-upload) is the
operational fix for why the canary's builds failed at `verifying`.
Separate
  line of work, not in this PR.

## Spec


`docs/superpowers/specs/2026-08-02-engine-runtime-asset-publishing-design.md`
described the old "complete at create" semantics. Step 6 of the flow now
points at the wait, a new "Projection completes at `ready`, not at
create"
section states both rules and the key invariant, and the Testing section
covers them.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01JksoXqdHArutJFifUtrKS6
```

### PR Body

```
## What staging showed

The `amazon-analyst` canary on staging looked healthy and was permanently
uninstallable. Its submission carried `engine_environment_version = 3` and an
`environment_source_sha256` matching the registered asset — the exact shape
every recovery path reads as "projection complete". Environment `v3`, `v4`, and
`v5` were all `status = failed`, `failure_stage = verifying`. Every install
returned 409 `agent.environment_not_ready`, and #3188's same-SHA replay heal
skipped the Pack because provenance was present. Re-projecting by hand hit
Engine's `409 {"error":{"type":"idempotency_conflict"}}` until I appended a
`:probe<ts>` suffix to the key.

(The builds failed because the staging root template is missing the
artifact-upload from zooclaw-engine#586, so verify fails on its first check.
That is a separate operational fix on the Engine side and is not part of this
PR — it is only how these two defects got exposed. Either one would have turned
any single bad build into a permanently broken Pack.)

## P0-1: provenance recorded without confirming the build

`create_environment` / `create_environment_version` return as soon as the
immutable version row exists; the E2B image build runs asynchronously
afterwards. `_create_or_version_environment` recorded
`engine_environment_version` + `environment_source_sha256` straight off that
response, so a version that later failed was written as if it were usable.

The projection now polls `get_environment_version` for that exact version
before recording anything:

- `ready` → record provenance, return `True` (unchanged behavior)
- `failed` → record **nothing**, raise `DependencyNotReadyError`
  `agent.pack_environment_build_failed` with `environment_id`,
  `environment_version`, `failure_stage`, `failure_message` in context.
  `run_guarded_engine_projection` logs it at error level; the caller's request
  still succeeds, as before.
- Bounded: 5s interval, 10min total budget (observed builds settle in 16–40s).
  Timeout is treated exactly like `failed`.
- A read failure says nothing about the build, so transport/upstream errors
  keep polling until the budget is spent; an explicit `failed` returns
  immediately.

Leaving no provenance behind is the point: the next CI re-run now trips
#3188's missing-provenance check and re-projects, instead of being told the
projection is already complete.

## P0-2: immutable idempotency key blocked every re-projection

The key was `{submission_id}:{asset.sha256}` (or just `submission_id` for V1).
Both parts are immutable, and Engine replays the first response for a repeated
key — so after a failed build, admin `environment/rebuild`, the #3188 replay
heal, and future zooclaw-engine#604 reconciliation all replayed the failed
version rather than producing a new one.

The key now carries a per-attempt suffix. **Invariant, documented on
`build_idempotency_key`:**

- stable across every Engine call *within* one publish attempt — computed once
  per attempt and threaded through the upload declaration, the upload
  finalize, and the version create (`build_environment_config` takes the same
  value, so the declare/finalize path stays consistent);
- different for every *new* attempt, so a re-projection actually rebuilds.

A useful side effect: the bounded in-process retry now retries a flaky build
under a fresh key instead of re-reading the same failed version.

## Structure

The build wait, the key builder, and the provenance write moved to a new
`app/services/pack_store/pack_environment_publish.py`.
`pack_environment_service.py` was 495 of its 500 permitted lines, so the
polling logic could not live there; it is now 492.

## Verification

- `tests/unit/test_pack_environment_service.py`: 56 passed (45 pre-existing,
  11 new). New coverage: `ready` records provenance for the exact created
  version; `failed` records nothing and raises the new code with its context;
  non-terminal statuses poll on; an unreadable status keeps polling; both the
  build-never-settles and status-unreadable paths are bounded; the key is
  stable across declare/finalize/create inside one attempt and different
  across attempts; a failed engine build exhausts retries with 5 distinct keys
  and no provenance write.
- Full `tests/unit`: 7403 passed. The 2 failures in `test_ci_lint_deptry.py`
  are environmental — this fresh worktree has no local `.venv`, so `deptry` is
  not on PATH; the same tests pass in a worktree that has one.
- `ruff check` + `ruff format --check` clean on `app` and `tests`.
- `pyright`: 0 errors on all three changed Python files.
- `scripts/ci-lint/01-file-length.sh` with `GITHUB_BASE_REF=main`: no new
  violations.

## Relationship to other work

- **#3188** (same-SHA replay heal) is what this unblocks. Its
  missing-provenance check was correct; it was being fed a false positive.
  With P0-1, a failed build leaves no provenance, so the next release re-run
  heals it; with P0-2, that heal can actually produce a new build.
- **zooclaw-engine#604** (durable autonomous reconciliation) inherits both
  properties — it will see failed builds as un-projected and will be able to
  re-publish.
- **zooclaw-engine#586** (staging root template artifact-upload) is the
  operational fix for why the canary's builds failed at `verifying`. Separate
  line of work, not in this PR.

## Spec

`docs/superpowers/specs/2026-08-02-engine-runtime-asset-publishing-design.md`
described the old "complete at create" semantics. Step 6 of the flow now
points at the wait, a new "Projection completes at `ready`, not at create"
section states both rules and the key invariant, and the Testing section
covers them.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01JksoXqdHArutJFifUtrKS6

```

---

## feat(web): redesign knowledge base workspace (#3176)

- **SHA**: `644a5a36f98ea458c185f02a6a6a08eb8af6db5d`
- **作者**: shana-srp
- **日期**: 2026-08-03T05:58:21Z

### Commit Message

```
feat(web): redesign knowledge base workspace (#3176)

## Linear

N/A

## Summary

- Redesign the knowledge-base overview around library cards, including
owned, shared, and unfiled states.
- Add fixed-size library dialogs for documents and access management,
collaborator invitation, stable pagination, and responsive upload/file
states.
- Add localized copy, custom knowledge-base icons, mock scenarios,
focused unit coverage, and a design specification.
- Preserve the existing backend data contracts and mutation flow.

## Merge queue repair

- Merged current `main` after merge-group run 30781003384 exposed
contract drift from #3181.
- Updated artifact selection tests for the new `messageUrl` contract and
removed the unused `getAgentArtifact` export that failed the knip hard
gate.
- Applied `size-override` because the PR event still uses base SHA
`a7ab6615`, so the size job counts later `main` changes (11,513 lines)
as PR changes even though they are already on `main`.

## Test plan

- [x] Knowledge-base focused Vitest suite: 59 tests passed.
- [x] Artifact merge-failure Vitest suite: 8 tests passed.
- [x] `lint:ci` passed, including the knip hard gate.
- [x] Repository `verify-web.sh` passed (governance guards, TypeScript,
focused Vitest, ESLint).

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Body

```
## Linear

N/A

## Summary

- Redesign the knowledge-base overview around library cards, including owned, shared, and unfiled states.
- Add fixed-size library dialogs for documents and access management, collaborator invitation, stable pagination, and responsive upload/file states.
- Add localized copy, custom knowledge-base icons, mock scenarios, focused unit coverage, and a design specification.
- Preserve the existing backend data contracts and mutation flow.

## Merge queue repair

- Merged current `main` after merge-group run 30781003384 exposed contract drift from #3181.
- Updated artifact selection tests for the new `messageUrl` contract and removed the unused `getAgentArtifact` export that failed the knip hard gate.
- Applied `size-override` because the PR event still uses base SHA `a7ab6615`, so the size job counts later `main` changes (11,513 lines) as PR changes even though they are already on `main`.

## Test plan

- [x] Knowledge-base focused Vitest suite: 59 tests passed.
- [x] Artifact merge-failure Vitest suite: 8 tests passed.
- [x] `lint:ci` passed, including the knip hard gate.
- [x] Repository `verify-web.sh` passed (governance guards, TypeScript, focused Vitest, ESLint).

```

---

## feat(channels): redesign IM channel setup experience (#3091)

- **SHA**: `b9fb66003a8bbca31eb083edfdb663c58134868f`
- **作者**: shana-srp
- **日期**: 2026-08-03T05:51:17Z

### Commit Message

```
feat(channels): redesign IM channel setup experience (#3091)

## Linear

N/A

## Summary
- 将 IM 频道平台选择重构为统一的平台卡片网格，并补齐各平台品牌图标与中英文文案。
- 统一 Telegram、DingTalk、Discord、Slack、Feishu、WeCom、Weixin
等设置弹窗的视觉、固定头部与连接方式切换交互。
- 优化 Agent 选择和引导连接流程，同时保留现有频道连接数据结构、提交参数与后端逻辑。
- 增加频道卡片与设置向导单元测试，并记录本次复杂 UI 重构设计说明。

## Test plan
- [x] Git pre-commit frontend lint
- [x] Git pre-push changed-surface verification (governance guards,
TypeScript, ESLint)
- [x] Channel-related unit tests (129 passed during implementation)
- [ ] Full local Vitest suite (current shell is Node 20; workspace
requires Node 24)

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Body

```
## Linear

N/A

## Summary
- 将 IM 频道平台选择重构为统一的平台卡片网格，并补齐各平台品牌图标与中英文文案。
- 统一 Telegram、DingTalk、Discord、Slack、Feishu、WeCom、Weixin 等设置弹窗的视觉、固定头部与连接方式切换交互。
- 优化 Agent 选择和引导连接流程，同时保留现有频道连接数据结构、提交参数与后端逻辑。
- 增加频道卡片与设置向导单元测试，并记录本次复杂 UI 重构设计说明。

## Test plan
- [x] Git pre-commit frontend lint
- [x] Git pre-push changed-surface verification (governance guards, TypeScript, ESLint)
- [x] Channel-related unit tests (129 passed during implementation)
- [ ] Full local Vitest suite (current shell is Node 20; workspace requires Node 24)

```

---

## refactor(chat): 优化会话标题与重命名交互 (#3192)

- **SHA**: `6fcca6bc65adddf6f3c33ef02226257572e95f7c`
- **作者**: lynn Zhuang
- **日期**: 2026-08-03T04:05:40Z

### Commit Message

```
refactor(chat): 优化会话标题与重命名交互 (#3192)

## 背景

当前聊天会话页顶部展示的是 Agent 名称，真正的 Session
名称位于独立的第二标题栏中，信息层级重复，重命名入口也与侧边栏体验不一致。本次调整属于现有聊天会话头部的交互与信息架构优化，不新增业务能力。

## 调整内容

- 顶部保留 Agent 头像，将 Agent 名称替换为当前 Session 名称，并移除重复的第二标题栏。
- Session 名称可直接在顶部重命名；编辑态、蓝色文本选中效果和圆角与侧边栏 Session rename 保持一致。
- 支持 Enter 保存、失焦保存、Escape 取消，并在保存后同步更新侧边栏 Session 列表缓存。
- 旧版 Session History 页面继续显示“头像 + Session History”，标题保持只读，不提供 rename。
- 优化窄屏布局和无障碍语义：标题在展示与编辑状态下均保留一级标题结构；手机端仅压缩健康连接状态，异常状态文字始终可见。

## 主干兼容修正

- 对齐 artifacts V2 测试夹具中的已发布文件地址契约。
- 移除当前完整 Web 门禁发现的未使用 `getAgentArtifact` 导出。

## 验证

- [x] `bash scripts/verify-changed.sh`
- [x] `pnpm lint:ci`
- [x] Session header 相关定向测试：8 个文件、179 个测试
- [x] 标题语义与连接状态回归测试：2 个文件、63 个测试
- [x] Asset Library 与 Legacy Workspace Browser 测试：2 个文件、4 个测试
- [x] 本地 Mock 页面验证 Enter/失焦保存、Escape 取消、侧边栏标题同步及只读 Session History
- [x] 390px、720px 和桌面宽度响应式验证，Files/Settings 保持可用，长标题正常截断
- [x] CI 41/41 通过，Codex 与 Claude 自动评审通过

## Linear

无
```

### PR Body

```
## 背景

当前聊天会话页顶部展示的是 Agent 名称，真正的 Session 名称位于独立的第二标题栏中，信息层级重复，重命名入口也与侧边栏体验不一致。本次调整属于现有聊天会话头部的交互与信息架构优化，不新增业务能力。

## 调整内容

- 顶部保留 Agent 头像，将 Agent 名称替换为当前 Session 名称，并移除重复的第二标题栏。
- Session 名称可直接在顶部重命名；编辑态、蓝色文本选中效果和圆角与侧边栏 Session rename 保持一致。
- 支持 Enter 保存、失焦保存、Escape 取消，并在保存后同步更新侧边栏 Session 列表缓存。
- 旧版 Session History 页面继续显示“头像 + Session History”，标题保持只读，不提供 rename。
- 优化窄屏布局和无障碍语义：标题在展示与编辑状态下均保留一级标题结构；手机端仅压缩健康连接状态，异常状态文字始终可见。

## 主干兼容修正

- 对齐 artifacts V2 测试夹具中的已发布文件地址契约。
- 移除当前完整 Web 门禁发现的未使用 `getAgentArtifact` 导出。

## 验证

- [x] `bash scripts/verify-changed.sh`
- [x] `pnpm lint:ci`
- [x] Session header 相关定向测试：8 个文件、179 个测试
- [x] 标题语义与连接状态回归测试：2 个文件、63 个测试
- [x] Asset Library 与 Legacy Workspace Browser 测试：2 个文件、4 个测试
- [x] 本地 Mock 页面验证 Enter/失焦保存、Escape 取消、侧边栏标题同步及只读 Session History
- [x] 390px、720px 和桌面宽度响应式验证，Files/Settings 保持可用，长标题正常截断
- [x] CI 41/41 通过，Codex 与 Claude 自动评审通过

## Linear

无

```

---

## feat(r2-worker): accept a service upload token for CI publishing (#3190)

- **SHA**: `88e82aa4c0f8d06ead81e791ca6bbf2a0f2fe755`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-03T02:28:53Z

### Commit Message

```
feat(r2-worker): accept a service upload token for CI publishing (#3190)

## Motivation

The `ecap-agent-pack` release workflow runs in GitHub Actions and has no
stable user identity, so it cannot call `POST /upload` on the R2 access
worker: that endpoint only accepted a user bearer token, validated
against claw-interface `GET /account/me`. This blocks CI from publishing
V2 engine pack archives. (Review finding #1, P0.)

## What changed

- `POST /upload` now accepts a static service token, mirroring the
existing `COPY_SERVICE_TOKEN` precedent on `POST /copy`:
- If `UPLOAD_SERVICE_TOKEN` is configured and the request's bearer token
matches it (same constant-time comparison helper as `/copy`), the
request is treated as a service-to-service call and the upload org is
pinned to `zooclaw`, so all service-uploaded keys are constrained to the
`zooclaw/` namespace.
- Any other token falls through to the existing user-token path
(`/account/me`), unchanged. When `UPLOAD_SERVICE_TOKEN` is unset,
behavior is identical to before — the Agent Studio user upload flow is
untouched.
- `Env` gains the optional `UPLOAD_SERVICE_TOKEN` field; `wrangler.toml`
header comment now lists it among workflow-managed secrets.
- `deploy-r2-access-worker.yml` validates and uploads
`UPLOAD_SERVICE_TOKEN` exactly like `COPY_SERVICE_TOKEN` (secrets
validation step + wrangler-action `secrets:` upload).
- New tests in `src/__tests__/upload-service-token.test.ts`:
service-token hit uploads under `zooclaw/` without calling
`/account/me`; mismatched token falls back to the user path (success and
401 cases); missing bearer still 401s; unset `UPLOAD_SERVICE_TOKEN`
keeps the user path unchanged.

## Ops required before/at next deploy

The deploy workflow now fails validation if the secret is missing, so
before the next staging/production deploy:

1. Set the `UPLOAD_SERVICE_TOKEN` secret in both `staging` and
`production` GitHub Environments of **ecap-workspace** (distinct values
per environment recommended, same as `COPY_SERVICE_TOKEN`).
2. Configure the same values as `R2_AGENT_PACKS_UPLOAD_TOKEN` in the
corresponding two GitHub Environments of **ecap-agent-pack**, so its
release workflow can authenticate uploads.

## Verification

In `services/r2-access-worker`:

- `vitest run`: 3 files, 39 tests, all passing (includes the 5 new
service-token tests).
- `tsc --noEmit`: clean.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01JksoXqdHArutJFifUtrKS6
```

### PR Body

```
## Motivation

The `ecap-agent-pack` release workflow runs in GitHub Actions and has no stable user identity, so it cannot call `POST /upload` on the R2 access worker: that endpoint only accepted a user bearer token, validated against claw-interface `GET /account/me`. This blocks CI from publishing V2 engine pack archives. (Review finding #1, P0.)

## What changed

- `POST /upload` now accepts a static service token, mirroring the existing `COPY_SERVICE_TOKEN` precedent on `POST /copy`:
  - If `UPLOAD_SERVICE_TOKEN` is configured and the request's bearer token matches it (same constant-time comparison helper as `/copy`), the request is treated as a service-to-service call and the upload org is pinned to `zooclaw`, so all service-uploaded keys are constrained to the `zooclaw/` namespace.
  - Any other token falls through to the existing user-token path (`/account/me`), unchanged. When `UPLOAD_SERVICE_TOKEN` is unset, behavior is identical to before — the Agent Studio user upload flow is untouched.
- `Env` gains the optional `UPLOAD_SERVICE_TOKEN` field; `wrangler.toml` header comment now lists it among workflow-managed secrets.
- `deploy-r2-access-worker.yml` validates and uploads `UPLOAD_SERVICE_TOKEN` exactly like `COPY_SERVICE_TOKEN` (secrets validation step + wrangler-action `secrets:` upload).
- New tests in `src/__tests__/upload-service-token.test.ts`: service-token hit uploads under `zooclaw/` without calling `/account/me`; mismatched token falls back to the user path (success and 401 cases); missing bearer still 401s; unset `UPLOAD_SERVICE_TOKEN` keeps the user path unchanged.

## Ops required before/at next deploy

The deploy workflow now fails validation if the secret is missing, so before the next staging/production deploy:

1. Set the `UPLOAD_SERVICE_TOKEN` secret in both `staging` and `production` GitHub Environments of **ecap-workspace** (distinct values per environment recommended, same as `COPY_SERVICE_TOKEN`).
2. Configure the same values as `R2_AGENT_PACKS_UPLOAD_TOKEN` in the corresponding two GitHub Environments of **ecap-agent-pack**, so its release workflow can authenticate uploads.

## Verification

In `services/r2-access-worker`:

- `vitest run`: 3 files, 39 tests, all passing (includes the 5 new service-token tests).
- `tsc --noEmit`: clean.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01JksoXqdHArutJFifUtrKS6

```

---

## feat(packs): reject stale publisher runs on runtime-asset registration (#3189)

- **SHA**: `9146bf07448a52d39095f450920348b8fd2835c0`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-03T02:01:40Z

### Commit Message

```
feat(packs): reject stale publisher runs on runtime-asset registration (#3189)

## Problem: last-writer-wins TOCTOU on runtime-asset registration

`POST /agent-packs/runtime-assets` records whatever SHA the latest
request carries. When two ecap-agent-pack release runs overlap (e.g. two
pushes in quick succession), the *older* run's registration can arrive
after the newer one and roll the recorded Engine SHA back to the older
archive. The run-number yield check on the CI side is only an
optimization — it cannot close the window between its check and the
registration call, so correctness has to live on the server.

## Fix: monotonic publisher fence, enforced at write time

The request gains an optional `publisher_run_number` (GitHub Actions
`GITHUB_RUN_NUMBER`, monotonic per workflow). The server persists it on
`runtime_assets.engine` and enforces the ordering **in the Mongo write
filter (compare-and-set)** — a preflight read still rejects known-stale
runs early, but the authority is the fenced write, because the archive
copy sits between the preflight read and the write:

- **request < recorded** → `409` with code
`pack_runtime_asset.stale_publisher`. This fires on **both** the
fresh-write path and the identical-SHA replay path — an old run
replaying "its own" SHA after a newer run swapped it is exactly the
rollback vector.
- **request == recorded** → allowed. A manual re-run of the same
workflow run replays the same number and is a legitimate idempotent
replay.
- **either side missing** → comparison skipped entirely.

Concretely:

- `set_engine_runtime_asset` adds a `None`-or-`$lte` fence on
`runtime_assets.engine.publisher_run_number` to the update filter
whenever the incoming asset carries a number. A zero modified-count is
re-read to distinguish losing the CAS to a newer run (`stale_publisher`,
the run gives up) from a displaced/rejected row (`submission_changed`,
CI retries).
- An identical-SHA replay from a **newer** run advances the stored
watermark via a fenced update pinned to the confirmed SHA (strict `$lt`,
so concurrent equal replays converge as no-ops). Leaving the older
watermark in place would let an intermediate run — newer than the
watermark, older than the replay — later pass the fence and overwrite
the confirmed asset. A lost advance is re-read and classified: newer
watermark → `stale_publisher`; swapped SHA → `submission_changed`; equal
number on the same SHA → benign, the replay succeeds.

Both points were raised as P0s by Codex review on the initial revision
and are fixed in `11a1207`.

## Backward compatibility

- A request without the field behaves byte-for-byte as today: the fence
is skipped and the repo update dict is unchanged, so a previously
recorded number is left untouched rather than cleared.
- Pre-existing engine assets have no stored number; the first numbered
registration stamps it.

## Rollout ordering

The field is *sent by CI and enforced by the server*, so the safe
direction is server first: this PR can merge and deploy before the
ecap-agent-pack companion PR that adds `publisher_run_number` to the
release workflow's request. Until CI sends it, every request omits the
field and behavior is unchanged. (The reverse order is also tolerated
only because FastAPI/pydantic ignores unknown body fields by default —
but that is incidental; the intended order is server first.)

## Docs


`docs/superpowers/specs/2026-08-02-engine-runtime-asset-publishing-design.md`
now records the server-side ordering fence and demotes the
ecap-agent-pack concurrency group to an optimization — the correctness
boundary lives on the server.

## Testing

- `tests/unit/test_runtime_asset_registration_service.py`: stale run
rejected on write path and on identical-SHA replay path; equal-number
replay allowed without a write; higher-number replay advances the
watermark (args asserted); first numbered replay stamps pre-fence data;
lost advance classified as stale / swapped-SHA conflict / benign equal
replay; lost fenced write re-read as stale; run number persisted on
registration; both no-number directions (old data / old CI) skip the
comparison. All pre-existing cases pass unchanged without the field
(regression for the compat claim).
- `tests/unit/test_pack_submission_repo.py`: fenced update filter
(`None`-or-`$lte`) asserted when the number is set, pre-field query
shape when unset; `advance_engine_runtime_asset_publisher_run` filter
pinned to SHA with strict `$lt`.
- 42 passed; ruff check/format clean; pyright clean; file-length lint
clean.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01JksoXqdHArutJFifUtrKS6
```

### PR Body

```
## Problem: last-writer-wins TOCTOU on runtime-asset registration

`POST /agent-packs/runtime-assets` records whatever SHA the latest request carries. When two ecap-agent-pack release runs overlap (e.g. two pushes in quick succession), the *older* run's registration can arrive after the newer one and roll the recorded Engine SHA back to the older archive. The run-number yield check on the CI side is only an optimization — it cannot close the window between its check and the registration call, so correctness has to live on the server.

## Fix: monotonic publisher fence, enforced at write time

The request gains an optional `publisher_run_number` (GitHub Actions `GITHUB_RUN_NUMBER`, monotonic per workflow). The server persists it on `runtime_assets.engine` and enforces the ordering **in the Mongo write filter (compare-and-set)** — a preflight read still rejects known-stale runs early, but the authority is the fenced write, because the archive copy sits between the preflight read and the write:

- **request < recorded** → `409` with code `pack_runtime_asset.stale_publisher`. This fires on **both** the fresh-write path and the identical-SHA replay path — an old run replaying "its own" SHA after a newer run swapped it is exactly the rollback vector.
- **request == recorded** → allowed. A manual re-run of the same workflow run replays the same number and is a legitimate idempotent replay.
- **either side missing** → comparison skipped entirely.

Concretely:

- `set_engine_runtime_asset` adds a `None`-or-`$lte` fence on `runtime_assets.engine.publisher_run_number` to the update filter whenever the incoming asset carries a number. A zero modified-count is re-read to distinguish losing the CAS to a newer run (`stale_publisher`, the run gives up) from a displaced/rejected row (`submission_changed`, CI retries).
- An identical-SHA replay from a **newer** run advances the stored watermark via a fenced update pinned to the confirmed SHA (strict `$lt`, so concurrent equal replays converge as no-ops). Leaving the older watermark in place would let an intermediate run — newer than the watermark, older than the replay — later pass the fence and overwrite the confirmed asset. A lost advance is re-read and classified: newer watermark → `stale_publisher`; swapped SHA → `submission_changed`; equal number on the same SHA → benign, the replay succeeds.

Both points were raised as P0s by Codex review on the initial revision and are fixed in `11a1207`.

## Backward compatibility

- A request without the field behaves byte-for-byte as today: the fence is skipped and the repo update dict is unchanged, so a previously recorded number is left untouched rather than cleared.
- Pre-existing engine assets have no stored number; the first numbered registration stamps it.

## Rollout ordering

The field is *sent by CI and enforced by the server*, so the safe direction is server first: this PR can merge and deploy before the ecap-agent-pack companion PR that adds `publisher_run_number` to the release workflow's request. Until CI sends it, every request omits the field and behavior is unchanged. (The reverse order is also tolerated only because FastAPI/pydantic ignores unknown body fields by default — but that is incidental; the intended order is server first.)

## Docs

`docs/superpowers/specs/2026-08-02-engine-runtime-asset-publishing-design.md` now records the server-side ordering fence and demotes the ecap-agent-pack concurrency group to an optimization — the correctness boundary lives on the server.

## Testing

- `tests/unit/test_runtime_asset_registration_service.py`: stale run rejected on write path and on identical-SHA replay path; equal-number replay allowed without a write; higher-number replay advances the watermark (args asserted); first numbered replay stamps pre-fence data; lost advance classified as stale / swapped-SHA conflict / benign equal replay; lost fenced write re-read as stale; run number persisted on registration; both no-number directions (old data / old CI) skip the comparison. All pre-existing cases pass unchanged without the field (regression for the compat claim).
- `tests/unit/test_pack_submission_repo.py`: fenced update filter (`None`-or-`$lte`) asserted when the number is set, pre-field query shape when unset; `advance_engine_runtime_asset_publisher_run` filter pinned to SHA with strict `$lt`.
- 42 passed; ruff check/format clean; pyright clean; file-length lint clean.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01JksoXqdHArutJFifUtrKS6


```

---
