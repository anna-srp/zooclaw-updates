# ecap-workspace — 2026-05-28
共 64 条 commits

---
## [147a4de] test(web): tighten three test exclusions (#2068)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T14:46:34Z
- **PR**: #2068

### Commit Message
```
test(web): tighten three test exclusions (#2068)

## Summary

Audit found three "exclusive conditions" in `web/app` tests worth fixing
(independent of coverage bar). Plan:
`~/.claude/plans/web-app-gleaming-eclipse.md`.

- **`firebase.unit.spec.ts:173-178`** — "should return error when not in
browser" was vacuous:
- File ran under default `jsdom` env, so `typeof window === 'undefined'`
never held — the SSR guard was never exercised
- Assertion was just `result.success === false`, which the surrounding
try/catch also produces on any throw
- **Fix**: add `// @vitest-environment node` directive (rest of file's
tests use explicit `vi.stubGlobal('window', ...)` so they keep working)
+ strengthen assertion to check `error === 'Not in browser
environment'`. Verified falsifiable: deleting the SSR guard makes this
test fail with `expected 'window is not defined' to be 'Not in browser
environment'`.

- **`agents-manager-publish.unit.spec.tsx:272-275`** — dead `if (typeof
window !== 'undefined')` guard inside a mock body. jsdom always defines
`window`; the branch never goes false. Looks copy-pasted from production
SSR-safe code. Removed.

- **`MiniChatClient.tsx`** — was tagged as "Pure-UI Client.tsx" in
`coverage.exclude`, but actually contains URL decoding + `:subagent:`
split + last-12 fallback chain. Moved out of exclude and added
`tests/unit/app/mini-chat/MiniChatClient.unit.spec.tsx` covering:
missing/empty sessionKey → empty state, `:subagent:` segment → first-12
label, no `:subagent:` → last-12 label, URL-encoded → decoded correctly,
empty subagent segment → falls back to last-12 of full key.

Coverage thresholds re-ratcheted per the `floor(observed - 1.5%)` rule
baked into `vitest.config.mts`:
- statements 80 → 81 (observed 82.82%)
- branches 73 → 73 (observed 75.24%, no change)
- functions 79 → 80 (observed 82.13%)
- lines 82 → 83 (observed 84.92%)

Out of scope (audit confirmed but not handled in this PR):
`PublicPricingClient.tsx` (700 LoC, possible logic extraction),
`cron-client.unit.spec.tsx:837 it.todo` (open issue to link),
SideMenu/AppLayout/ClientLayout auth/responsive logic (would need hook
extraction first).

## Test plan
- [x] `pnpm test:unit` — 411 files / 6232 tests (1 todo) all pass after
changes
- [x] `pnpm test:unit --coverage` — all four thresholds satisfied at new
baseline
- [x] Falsifiability check: temporarily removing
`lib/firebase.ts:154-156` SSR guard makes the strengthened firebase test
fail (confirmed locally, then restored)
- [x] `pnpm lint` — clean
- [x] `npx tsc --noEmit` — clean
- [x] Branch rebased on latest `origin/main`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Audit found three "exclusive conditions" in `web/app` tests worth fixing (independent of coverage bar). Plan: `~/.claude/plans/web-app-gleaming-eclipse.md`.

- **`firebase.unit.spec.ts:173-178`** — "should return error when not in browser" was vacuous:
  - File ran under default `jsdom` env, so `typeof window === 'undefined'` never held — the SSR guard was never exercised
  - Assertion was just `result.success === false`, which the surrounding try/catch also produces on any throw
  - **Fix**: add `// @vitest-environment node` directive (rest of file's tests use explicit `vi.stubGlobal('window', ...)` so they keep working) + strengthen assertion to check `error === 'Not in browser environment'`. Verified falsifiable: deleting the SSR guard makes this test fail with `expected 'window is not defined' to be 'Not in browser environment'`.

- **`agents-manager-publish.unit.spec.tsx:272-275`** — dead `if (typeof window !== 'undefined')` guard inside a mock body. jsdom always defines `window`; the branch never goes false. Looks copy-pasted from production SSR-safe code. Removed.

- **`MiniChatClient.tsx`** — was tagged as "Pure-UI Client.tsx" in `coverage.exclude`, but actually contains URL decoding + `:subagent:` split + last-12 fallback chain. Moved out of exclude and added `tests/unit/app/mini-chat/MiniChatClient.unit.spec.tsx` covering: missing/empty sessionKey → empty state, `:subagent:` segment → first-12 label, no `:subagent:` → last-12 label, URL-encoded → decoded correctly, empty subagent segment → falls back to last-12 of full key.

Coverage thresholds re-ratcheted per the `floor(observed - 1.5%)` rule baked into `vitest.config.mts`:
- statements 80 → 81 (observed 82.82%)
- branches 73 → 73 (observed 75.24%, no change)
- functions 79 → 80 (observed 82.13%)
- lines 82 → 83 (observed 84.92%)

Out of scope (audit confirmed but not handled in this PR): `PublicPricingClient.tsx` (700 LoC, possible logic extraction), `cron-client.unit.spec.tsx:837 it.todo` (open issue to link), SideMenu/AppLayout/ClientLayout auth/responsive logic (would need hook extraction first).

## Test plan
- [x] `pnpm test:unit` — 411 files / 6232 tests (1 todo) all pass after changes
- [x] `pnpm test:unit --coverage` — all four thresholds satisfied at new baseline
- [x] Falsifiability check: temporarily removing `lib/firebase.ts:154-156` SSR guard makes the strengthened firebase test fail (confirmed locally, then restored)
- [x] `pnpm lint` — clean
- [x] `npx tsc --noEmit` — clean
- [x] Branch rebased on latest `origin/main`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [79f9a9f] chore(skills): add --before/--limit/--concurrency to bulk-archive-shipped-docs (#2067)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T14:37:23Z
- **PR**: #2067

### Commit Message
```
chore(skills): add --before/--limit/--concurrency to bulk-archive-shipped-docs (#2067)

## Summary

Adds three explicit args to the `bulk-archive-shipped-docs` skill so the
sweep can be scoped without hand-editing the skill body.

- `--limit N` — analyze at most N docs (taken from the head of the
alphabetically-sorted list = earliest dates first).
- `--concurrency N` — Step 2 analysis batch size (default `8`, hard cap
`16`). Step 5 stays sequential because multiple SHIPPED docs often share
an inbound-link target (a master spec) — concurrent edits would race.
- `--before YYYY-MM-DD` — keep only docs whose filename date prefix is
strictly before this date. The rationale (also in-skill): the newest
plans are likely still in-flight and not worth analyzing for archival,
so `--before` lets a sweep skip them cheaply.

Date matching uses the leading `YYYY-MM-DD-` segment of the basename —
lexicographic compare equals date compare, no mtime confusion when files
get fresh timestamps from `git checkout`. Docs without that prefix are
**kept** by default (no date to compare); the skill instructs the run
echo to surface that explicitly.

## Validation

End-to-end validated by PR #2065 — that sweep ran with `--before
2026-04-01 --limit 20 --concurrency 8`, narrowed 95 candidates to 7,
archived 5 SHIPPED/DESIGN_ONLY_VERIFIED docs, correctly skipped one
NOT_SHIPPED and one PARTIAL.

## Test plan

- [ ] Read the new "Args" section in
`.claude/skills/bulk-archive-shipped-docs/SKILL.md` — does the table +
rationale read cleanly?
- [ ] Confirm Step 1's filter wording matches the table
(keep-strictly-before semantics + "no-date-prefix kept" caveat)
- [ ] Confirm Step 2 heading now reads "batches of `--concurrency`,
default 8"

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Adds three explicit args to the `bulk-archive-shipped-docs` skill so the sweep can be scoped without hand-editing the skill body.

- `--limit N` — analyze at most N docs (taken from the head of the alphabetically-sorted list = earliest dates first).
- `--concurrency N` — Step 2 analysis batch size (default `8`, hard cap `16`). Step 5 stays sequential because multiple SHIPPED docs often share an inbound-link target (a master spec) — concurrent edits would race.
- `--before YYYY-MM-DD` — keep only docs whose filename date prefix is strictly before this date. The rationale (also in-skill): the newest plans are likely still in-flight and not worth analyzing for archival, so `--before` lets a sweep skip them cheaply.

Date matching uses the leading `YYYY-MM-DD-` segment of the basename — lexicographic compare equals date compare, no mtime confusion when files get fresh timestamps from `git checkout`. Docs without that prefix are **kept** by default (no date to compare); the skill instructs the run echo to surface that explicitly.

## Validation

End-to-end validated by PR #2065 — that sweep ran with `--before 2026-04-01 --limit 20 --concurrency 8`, narrowed 95 candidates to 7, archived 5 SHIPPED/DESIGN_ONLY_VERIFIED docs, correctly skipped one NOT_SHIPPED and one PARTIAL.

## Test plan

- [ ] Read the new "Args" section in `.claude/skills/bulk-archive-shipped-docs/SKILL.md` — does the table + rationale read cleanly?
- [ ] Confirm Step 1's filter wording matches the table (keep-strictly-before semantics + "no-date-prefix kept" caveat)
- [ ] Confirm Step 2 heading now reads "batches of `--concurrency`, default 8"

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [c601d79] chore(docs): bulk archive 5 shipped docs (sweep before 2026-04-01) (#2065)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T14:32:42Z
- **PR**: #2065

### Commit Message
```
chore(docs): bulk archive 5 shipped docs (sweep before 2026-04-01) (#2065)

## Summary

Auto-generated archive sweep via `/bulk-archive-shipped-docs --before
2026-04-01 --limit 20 --concurrency 8`.

- **Scanned**: 7 docs (filename date prefix < 2026-04-01, under
`docs/plans/`, `docs/superpowers/plans/`, `docs/superpowers/specs/`)
- **Archived**: 5
- **Skipped**: 2

## Per-doc verdict checklist

Each row is a human spot-check surface — the analysis subagents are not
infallible. Look at the JSON `notes` referenced below if any row feels
off.

| # | Source | → Target | Verdict | Signals | Notes |
|---|---|---|---|---|---|
| 1 | `docs/plans/2026-03-03-gen-claw-implementation.md` |
`docs/archive/specs/2026-03-03-gen-claw-implementation.md` | SHIPPED |
6/8 | Historical implementation log of 2 completed phases. Some named
artifacts (`useOpenClawChat`, `GenClawMessageList`) have since been
consolidated into `useChatMessaging`/`ChatBody` — doc records what
shipped, subsequent refactors out of scope. |
| 2 | `docs/plans/2026-03-06-openclaw-app-admin-design.md` |
`docs/archive/specs/2026-03-06-openclaw-app-admin-design.md` | SHIPPED |
8/8 | Admin UI shipped as `/admin` tab (BotsTab + `useOpenClawAdmin`)
rather than standalone `/admin-openclaw` route — functional surface
(Apps table, View Bots modal, start/stop/restart/delete, recreate flow)
all present. Backend `routes/openclaw_admin.py` with prefix
`/openclaw/admin` and `openclaw_app` MongoDB field confirmed. |
| 3 |
`docs/superpowers/plans/2026-03-30-onboarding-status-resolution.md` |
`docs/archive/plans/2026-03-30-onboarding-status-resolution-plan.md`
*(renamed: appended `-plan`)* | SHIPPED | 11/11 | Shipped in PR #663
(2026-04-14). Paths shifted: `resolveOnboardingStatus.ts` →
`web/app/src/lib/onboarding/resolve-status.ts`; `OnboardingProvider.tsx`
→ `components/providers/`. All key symbols + unit tests confirmed. |
| 4 |
`docs/superpowers/specs/2026-03-13-artifacts-v2-link-preview-design.md`
| `docs/archive/specs/2026-03-13-artifacts-v2-link-preview-design.md` |
DESIGN_ONLY_VERIFIED | 11/11 | Pure design doc. Backend deletions
(`artifact.py`, `artifacts.py`, `artifact_storage.py`) confirmed gone.
Frontend `PreviewFile`, `PREVIEWABLE_EXTS`, `useFilePreview` hook +
renderers all present. Code evolved beyond spec
(DocxRenderer/ExcelRenderer/MermaidRenderer added) — same architecture,
richer implementation. |
| 5 |
`docs/superpowers/specs/2026-03-30-onboarding-status-resolution-design.md`
| `docs/archive/specs/2026-03-30-onboarding-status-resolution-design.md`
| DESIGN_ONLY_VERIFIED | 9/9 | Companion design to #3. All architectural
elements verified in code: `resolveOnboardingStatus`,
`BackendOnboardingStatus`, `onboarding-backend-status` event,
`ScopedBackendOnboardingStatus`, account-scoped storage, 15s timeout +
retry, unit tests. |

## Skipped (kept in active dirs)

| Source | Verdict | Reason |
|---|---|---|
| `docs/plans/2026-03-03-gen-claw-design.md` | NOT_SHIPPED |
Architecture drifted significantly: page renamed `[locale]/gen-claw/` →
`[locale]/chat/`; `GenClawMessageList.tsx` and `useOpenClawChat.ts`
absent; bot naming differs (doc: `ecap-{uid[:8]}-{timestamp}`, code:
`ecap-web-{uid}`); `connect.challenge`/`webchat-ui` handshake constants
absent. Likely earlier design that engineering later superseded with a
redesigned `/chat` experience. |
| `docs/superpowers/plans/2026-03-11-tasks-page.md` | PARTIAL | Feature
shipped (PR shipping commit 8139af6a3, 2026-03-11) then partially
reverted in PR #114 / commit fac08ad70 (2026-03-18). Backend schema +
endpoint + BFF route + `?subagent=` handling all remain, but the
headline `/tasks` page and SideNav Tasks nav item were removed. Classic
"shipped then reverted" failure mode — abstaining per skill guidance. |

## Link rewrites performed

- **Outgoing (in moved doc)**:
`2026-03-30-onboarding-status-resolution-plan.md` (formerly
`.../plans/...-resolution.md`): updated companion design doc path from
`docs/superpowers/specs/...` to `docs/archive/specs/...` (cross-batch —
both docs in this sweep).
- **Inbound (live doc)**:
`docs/superpowers/specs/2026-05-14-eca-675-skip-onboarding-design.md`
line 4: relative link to onboarding design rewritten from
`./2026-03-30-onboarding-status-resolution-design.md` to
`../../archive/specs/2026-03-30-onboarding-status-resolution-design.md`.

## Test plan

- [ ] Spot-check rows #1 and #2 (the only `docs/plans/` →
`docs/archive/specs/` moves — confirm bucket judgment is right; both are
design/implementation docs without `- [ ]` execution checklists)
- [ ] Verify renamed file #3 (`...-resolution.md` →
`...-resolution-plan.md`) — the `-plan` suffix is added because it had
execution checkboxes
- [ ] Confirm skipped row 2 (`tasks-page.md`) really should stay:
feature did ship, but `/tasks` page was reverted; if you'd prefer it
move to `docs/archive/plans/` anyway as a historical record, say so
- [ ] Spot-check the inbound link rewrite in
`2026-05-14-eca-675-skip-onboarding-design.md` line 4 still resolves
correctly when previewing
- [ ] **Do not auto-merge** — false-positive archive of an in-progress
doc is the worst-case failure; the checklist is the human catch.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Auto-generated archive sweep via `/bulk-archive-shipped-docs --before 2026-04-01 --limit 20 --concurrency 8`.

- **Scanned**: 7 docs (filename date prefix < 2026-04-01, under `docs/plans/`, `docs/superpowers/plans/`, `docs/superpowers/specs/`)
- **Archived**: 5
- **Skipped**: 2

## Per-doc verdict checklist

Each row is a human spot-check surface — the analysis subagents are not infallible. Look at the JSON `notes` referenced below if any row feels off.

| # | Source | → Target | Verdict | Signals | Notes |
|---|---|---|---|---|---|
| 1 | `docs/plans/2026-03-03-gen-claw-implementation.md` | `docs/archive/specs/2026-03-03-gen-claw-implementation.md` | SHIPPED | 6/8 | Historical implementation log of 2 completed phases. Some named artifacts (`useOpenClawChat`, `GenClawMessageList`) have since been consolidated into `useChatMessaging`/`ChatBody` — doc records what shipped, subsequent refactors out of scope. |
| 2 | `docs/plans/2026-03-06-openclaw-app-admin-design.md` | `docs/archive/specs/2026-03-06-openclaw-app-admin-design.md` | SHIPPED | 8/8 | Admin UI shipped as `/admin` tab (BotsTab + `useOpenClawAdmin`) rather than standalone `/admin-openclaw` route — functional surface (Apps table, View Bots modal, start/stop/restart/delete, recreate flow) all present. Backend `routes/openclaw_admin.py` with prefix `/openclaw/admin` and `openclaw_app` MongoDB field confirmed. |
| 3 | `docs/superpowers/plans/2026-03-30-onboarding-status-resolution.md` | `docs/archive/plans/2026-03-30-onboarding-status-resolution-plan.md` *(renamed: appended `-plan`)* | SHIPPED | 11/11 | Shipped in PR #663 (2026-04-14). Paths shifted: `resolveOnboardingStatus.ts` → `web/app/src/lib/onboarding/resolve-status.ts`; `OnboardingProvider.tsx` → `components/providers/`. All key symbols + unit tests confirmed. |
| 4 | `docs/superpowers/specs/2026-03-13-artifacts-v2-link-preview-design.md` | `docs/archive/specs/2026-03-13-artifacts-v2-link-preview-design.md` | DESIGN_ONLY_VERIFIED | 11/11 | Pure design doc. Backend deletions (`artifact.py`, `artifacts.py`, `artifact_storage.py`) confirmed gone. Frontend `PreviewFile`, `PREVIEWABLE_EXTS`, `useFilePreview` hook + renderers all present. Code evolved beyond spec (DocxRenderer/ExcelRenderer/MermaidRenderer added) — same architecture, richer implementation. |
| 5 | `docs/superpowers/specs/2026-03-30-onboarding-status-resolution-design.md` | `docs/archive/specs/2026-03-30-onboarding-status-resolution-design.md` | DESIGN_ONLY_VERIFIED | 9/9 | Companion design to #3. All architectural elements verified in code: `resolveOnboardingStatus`, `BackendOnboardingStatus`, `onboarding-backend-status` event, `ScopedBackendOnboardingStatus`, account-scoped storage, 15s timeout + retry, unit tests. |

## Skipped (kept in active dirs)

| Source | Verdict | Reason |
|---|---|---|
| `docs/plans/2026-03-03-gen-claw-design.md` | NOT_SHIPPED | Architecture drifted significantly: page renamed `[locale]/gen-claw/` → `[locale]/chat/`; `GenClawMessageList.tsx` and `useOpenClawChat.ts` absent; bot naming differs (doc: `ecap-{uid[:8]}-{timestamp}`, code: `ecap-web-{uid}`); `connect.challenge`/`webchat-ui` handshake constants absent. Likely earlier design that engineering later superseded with a redesigned `/chat` experience. |
| `docs/superpowers/plans/2026-03-11-tasks-page.md` | PARTIAL | Feature shipped (PR shipping commit 8139af6a3, 2026-03-11) then partially reverted in PR #114 / commit fac08ad70 (2026-03-18). Backend schema + endpoint + BFF route + `?subagent=` handling all remain, but the headline `/tasks` page and SideNav Tasks nav item were removed. Classic "shipped then reverted" failure mode — abstaining per skill guidance. |

## Link rewrites performed

- **Outgoing (in moved doc)**: `2026-03-30-onboarding-status-resolution-plan.md` (formerly `.../plans/...-resolution.md`): updated companion design doc path from `docs/superpowers/specs/...` to `docs/archive/specs/...` (cross-batch — both docs in this sweep).
- **Inbound (live doc)**: `docs/superpowers/specs/2026-05-14-eca-675-skip-onboarding-design.md` line 4: relative link to onboarding design rewritten from `./2026-03-30-onboarding-status-resolution-design.md` to `../../archive/specs/2026-03-30-onboarding-status-resolution-design.md`.

## Test plan

- [ ] Spot-check rows #1 and #2 (the only `docs/plans/` → `docs/archive/specs/` moves — confirm bucket judgment is right; both are design/implementation docs without `- [ ]` execution checklists)
- [ ] Verify renamed file #3 (`...-resolution.md` → `...-resolution-plan.md`) — the `-plan` suffix is added because it had execution checkboxes
- [ ] Confirm skipped row 2 (`tasks-page.md`) really should stay: feature did ship, but `/tasks` page was reverted; if you'd prefer it move to `docs/archive/plans/` anyway as a historical record, say so
- [ ] Spot-check the inbound link rewrite in `2026-05-14-eca-675-skip-onboarding-design.md` line 4 still resolves correctly when previewing
- [ ] **Do not auto-merge** — false-positive archive of an in-progress doc is the worst-case failure; the checklist is the human catch.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [4d508eb] refactor(web): migrate cronHelpers storage to uid-keyed RQ + persister (#2000 Bucket-4 A7) (#2063)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T14:31:17Z
- **PR**: #2063

### Commit Message
```
refactor(web): migrate cronHelpers storage to uid-keyed RQ + persister (#2000 Bucket-4 A7) (#2063)

## Summary

Contributes to https://linear.app/srpone/issue/ECA-2000 — does **not**
close
[#2000](https://github.com/SerendipityOneInc/ecap-workspace/issues/2000)
(A6 is being worked in parallel).

A7 closes out the last of the three Bucket-4 storage migrations by
retiring `cronHelpers.{load,save,remove}CachedJobs` + the
`STORAGE_KEYS.CRON_JOBS_CACHE` key in favor of uid-keyed React Query +
persistQueryClient. Follows the A5 (#2054) and B3 (#2053) templates
merged on 2026-05-28.

### Migration diff

| Area | Pre-A7 | Post-A7 |
|---|---|---|
| Storage owner | `localStorage['claw-cron-jobs-cache']` (single global
key) | RQ cache @ `cronKeys.jobs(uid)`, persisted via
`CRON_JOBS_QUERY_KEY_PREFIX` |
| queryKey | `cronKeys.jobs(authToken)` | `cronKeys.jobs(uid)` |
| Write triggers | `saveCachedJobs(liveJobs)` inside queryFn (violated
R1) | RQ owns it via the queryFn return value |
| Historical merge | `mergeJobsWithCache(live, loadCachedJobs())`
reading `localStorage` | Inline in `useCronJobs` queryFn reading
`queryClient.getQueryData(cronKeys.jobs(uid))` |
| Delete-from-history | `removeCachedJob(jobId)` → `localStorage` |
`queryClient.setQueryData(cronKeys.jobs(uid), prev => prev.filter(…))` |
| Bot recreate cleanup |
`localStorage.removeItem(STORAGE_KEYS.CRON_JOBS_CACHE)` |
`getQueryClient().invalidateQueries({ queryKey:
cronKeys.jobs(resolvedUid) })` (matches A5 pattern) |
| Persister allowlist | n/a | `PERSIST_ALLOWLIST_PREFIXES` 6 → 7 (adds
`CRON_JOBS_QUERY_KEY_PREFIX`) |

### Caller switches

- `CronClient.tsx` — replaced inline `useQuery` with `useCronJobs(uid, {
wsFallback, enabled: wsReady })`; replaced two `removeCachedJob(jobId)`
callsites with `setQueryData` + `refetchJobs`
- `useOpenClawInit.ts` — removed
`localStorage.removeItem(STORAGE_KEYS.CRON_JOBS_CACHE)`, added
`getQueryClient().invalidateQueries({ queryKey:
cronKeys.jobs(resolvedUid) })` next to the existing A5 agents
invalidation
- `lib/auth/types.ts` — removed `STORAGE_KEYS.CRON_JOBS_CACHE`

### Hook design notes

- W2-hooks-pure enforced — `useCronJobs.ts` lives under
`src/hooks/queries/cron/` and cannot import `CronJob` /
`mergeJobsWithCache` from `src/app/[locale]/schedule/cronHelpers.ts`.
The merge logic is inlined with a structural `JobLike` type;
`CronClient` casts back to `CronJob[]` at the boundary
- WS fallback closure is supplied by the caller (matches Bucket-3
pattern) so the hook stays free of the `OpenClaw` context dependency
- No module-level `_inflight` Map needed — RQ's own per-queryKey dedup
covers per-uid isolation (queryKey carries the uid), so the A5 round-5
`_inflightByUid` template is N/A here (no imperative-caller throttle
layer exists for cron jobs)

### Test plan

- [x] **Retired**:
`tests/unit/app/schedule/cronHelpers-storage.unit.spec.ts` (Phase-0
#2049) — boundary contract applies to deleted code; same pattern as
Bucket-1 PR #1990 and Bucket-3 PR-D
- [x] **Retired**: `localStorage cache helpers` + `mergeJobsWithCache`
describes in `tests/unit/app/schedule/cron-helpers.unit.spec.ts` —
replaced by the new hook spec
- [x] **New**: `tests/unit/hooks/queries/cron/useCronJobs.unit.spec.tsx`
— 8 cases covering disabled / fetch / RQ dedup / per-uid isolation /
error / WS fallback / queryKey shape / merge-historical
- [x] **Extended**: `tests/unit/lib/query/persist-client.unit.spec.ts` —
`shouldDehydrateQuery` for `cronKeys.jobs(uid)`,
`PERSIST_ALLOWLIST_PREFIXES` length 6 → 7 +
`containEqual(CRON_JOBS_QUERY_KEY_PREFIX)`
- [x] **Extended**: `tests/unit/hooks/useOpenClawInit.unit.spec.ts` —
new test asserts `cronKeys.jobs('user1')` invalidation on `recreate()`
with the captured `resolvedUid` (mirrors A5 falsifiability anchor)
- [x] `npx tsc --noEmit` clean
- [x] `./node_modules/.bin/vitest run` — 6220 passed | 1 todo (was 6189
on main; +6 from new hook spec, +1 from new useOpenClawInit case, -8
from retired storage spec / -22 from inlined merge/localStorage cleanup
nets out)
- [x] `pnpm lint` + `pnpm lint:ci` clean (W2-hooks-pure passes with the
inlined helper)
- [x] `bash web/scripts/check-cache-governance-disables-shrink-only.sh`
— `main: 3, HEAD: 3` (no new disables)

### Out of scope

- Does NOT touch `useUserAgents` (A5 done in #2054)
- Does NOT touch `useCustomAgentPublishes` (A6 in flight, parallel
branch)
- Does NOT touch the publish draft store (B3 done in #2053)
- Does NOT touch the `cronHelpers` scheduling algorithm
(`parseCronField` / `getJobFireTimesForDay` / `getDayFireSplit` /
`formFromJob` / `jobFromForm` / calendar utils all unchanged)
- Does NOT enable cross-tab broadcast — tracked in #1997, same
disposition as Bucket-1/2/3 + A5

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Contributes to https://linear.app/srpone/issue/ECA-2000 — does **not** close [#2000](https://github.com/SerendipityOneInc/ecap-workspace/issues/2000) (A6 is being worked in parallel).

A7 closes out the last of the three Bucket-4 storage migrations by retiring `cronHelpers.{load,save,remove}CachedJobs` + the `STORAGE_KEYS.CRON_JOBS_CACHE` key in favor of uid-keyed React Query + persistQueryClient. Follows the A5 (#2054) and B3 (#2053) templates merged on 2026-05-28.

### Migration diff

| Area | Pre-A7 | Post-A7 |
|---|---|---|
| Storage owner | `localStorage['claw-cron-jobs-cache']` (single global key) | RQ cache @ `cronKeys.jobs(uid)`, persisted via `CRON_JOBS_QUERY_KEY_PREFIX` |
| queryKey | `cronKeys.jobs(authToken)` | `cronKeys.jobs(uid)` |
| Write triggers | `saveCachedJobs(liveJobs)` inside queryFn (violated R1) | RQ owns it via the queryFn return value |
| Historical merge | `mergeJobsWithCache(live, loadCachedJobs())` reading `localStorage` | Inline in `useCronJobs` queryFn reading `queryClient.getQueryData(cronKeys.jobs(uid))` |
| Delete-from-history | `removeCachedJob(jobId)` → `localStorage` | `queryClient.setQueryData(cronKeys.jobs(uid), prev => prev.filter(…))` |
| Bot recreate cleanup | `localStorage.removeItem(STORAGE_KEYS.CRON_JOBS_CACHE)` | `getQueryClient().invalidateQueries({ queryKey: cronKeys.jobs(resolvedUid) })` (matches A5 pattern) |
| Persister allowlist | n/a | `PERSIST_ALLOWLIST_PREFIXES` 6 → 7 (adds `CRON_JOBS_QUERY_KEY_PREFIX`) |

### Caller switches

- `CronClient.tsx` — replaced inline `useQuery` with `useCronJobs(uid, { wsFallback, enabled: wsReady })`; replaced two `removeCachedJob(jobId)` callsites with `setQueryData` + `refetchJobs`
- `useOpenClawInit.ts` — removed `localStorage.removeItem(STORAGE_KEYS.CRON_JOBS_CACHE)`, added `getQueryClient().invalidateQueries({ queryKey: cronKeys.jobs(resolvedUid) })` next to the existing A5 agents invalidation
- `lib/auth/types.ts` — removed `STORAGE_KEYS.CRON_JOBS_CACHE`

### Hook design notes

- W2-hooks-pure enforced — `useCronJobs.ts` lives under `src/hooks/queries/cron/` and cannot import `CronJob` / `mergeJobsWithCache` from `src/app/[locale]/schedule/cronHelpers.ts`. The merge logic is inlined with a structural `JobLike` type; `CronClient` casts back to `CronJob[]` at the boundary
- WS fallback closure is supplied by the caller (matches Bucket-3 pattern) so the hook stays free of the `OpenClaw` context dependency
- No module-level `_inflight` Map needed — RQ's own per-queryKey dedup covers per-uid isolation (queryKey carries the uid), so the A5 round-5 `_inflightByUid` template is N/A here (no imperative-caller throttle layer exists for cron jobs)

### Test plan

- [x] **Retired**: `tests/unit/app/schedule/cronHelpers-storage.unit.spec.ts` (Phase-0 #2049) — boundary contract applies to deleted code; same pattern as Bucket-1 PR #1990 and Bucket-3 PR-D
- [x] **Retired**: `localStorage cache helpers` + `mergeJobsWithCache` describes in `tests/unit/app/schedule/cron-helpers.unit.spec.ts` — replaced by the new hook spec
- [x] **New**: `tests/unit/hooks/queries/cron/useCronJobs.unit.spec.tsx` — 8 cases covering disabled / fetch / RQ dedup / per-uid isolation / error / WS fallback / queryKey shape / merge-historical
- [x] **Extended**: `tests/unit/lib/query/persist-client.unit.spec.ts` — `shouldDehydrateQuery` for `cronKeys.jobs(uid)`, `PERSIST_ALLOWLIST_PREFIXES` length 6 → 7 + `containEqual(CRON_JOBS_QUERY_KEY_PREFIX)`
- [x] **Extended**: `tests/unit/hooks/useOpenClawInit.unit.spec.ts` — new test asserts `cronKeys.jobs('user1')` invalidation on `recreate()` with the captured `resolvedUid` (mirrors A5 falsifiability anchor)
- [x] `npx tsc --noEmit` clean
- [x] `./node_modules/.bin/vitest run` — 6220 passed | 1 todo (was 6189 on main; +6 from new hook spec, +1 from new useOpenClawInit case, -8 from retired storage spec / -22 from inlined merge/localStorage cleanup nets out)
- [x] `pnpm lint` + `pnpm lint:ci` clean (W2-hooks-pure passes with the inlined helper)
- [x] `bash web/scripts/check-cache-governance-disables-shrink-only.sh` — `main: 3, HEAD: 3` (no new disables)

### Out of scope

- Does NOT touch `useUserAgents` (A5 done in #2054)
- Does NOT touch `useCustomAgentPublishes` (A6 in flight, parallel branch)
- Does NOT touch the publish draft store (B3 done in #2053)
- Does NOT touch the `cronHelpers` scheduling algorithm (`parseCronField` / `getJobFireTimesForDay` / `getDayFireSplit` / `formFromJob` / `jobFromForm` / calendar utils all unchanged)
- Does NOT enable cross-tab broadcast — tracked in #1997, same disposition as Bucket-1/2/3 + A5

---
## [8b550a0] chore(skills): trim both archive-docs skills (~68% shorter, same behavior) (#2064)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T14:19:00Z
- **PR**: #2064

### Commit Message
```
chore(skills): trim both archive-docs skills (~68% shorter, same behavior) (#2064)

## Summary

Both `archive-shipped-doc` and `bulk-archive-shipped-docs` accumulated
bloat through 5+ Codex review iterations on their original PRs (#2058 +
#2061). Each finding got fixed with 5-10 lines of explanation rather
than 1-2 lines of rule. Result was 666 total lines for what's
fundamentally simple work.

Slimmed down with **no behavioral change** — all the load-bearing rules
Codex iterated us to are preserved.

## Line count

| File | Before | After | Δ |
|---|---|---|---|
| `archive-shipped-doc/SKILL.md` | 289 | 95 | -67% |
| `archive-shipped-doc/references/classification-rules.md` | 122 | 33 |
-73% |
| `bulk-archive-shipped-docs/SKILL.md` | 255 | 83 | -67% |
| **Total** | **666** | **211** | **-68%** |

Description blocks roughly halved too (archive ~70 words, bulk ~60
words).

## What got cut

- Long "why this exists" preambles → frontmatter description carries it
- "Staging checklist" section that duplicated workflow steps
- "When you might be wrong" philosophical preamble → condensed to one
trailing block on real failure modes
- "Don't-do list" duplicating what workflow already says
- Verbose worked examples → most folded into condensed bullets
- Full JSON schema spelled twice → kept only the fenced example
- Long "two-phase design" rationale in bulk → one line "why parent does
execution (races + cross-batch awareness)"
- "Future cron driver" expanded section → 2 lines

## What was preserved

Every Codex finding from the original 5 review rounds:

- `web/` → `web/app/` is substitute not prepend
- `gh` failure = inconclusive, never negative
- Spec subtypes `-design`/`-rfd`/`-review` with "preserve if source has
them"
- Bare `docs/...` is NOT repo-root-absolute in Markdown — must recompute
relative
- Basename grep collides across 7+ plan/spec pairs in this repo — verify
hits resolve to source
- `git add` after `Edit` (Git doesn't auto-stage post-`git mv` edits)
- Frozen-snapshot rule for refs inside `docs/archive/`
- "When in doubt, abstain" as the bias
- Batch plan validation BEFORE any execution (collision / exists /
vanished)
- Subagents run Steps 1-6 (analysis + planning, including `target`
computation), not 1-4

## Test plan

- [ ] Re-read each SKILL.md end-to-end and confirm a new contributor
could follow the workflow without missing anything load-bearing
- [ ] Mental dry-run of the previous "vulture plan" test case (PR #2058
demo) against the slim version — verdict should still be PARTIAL with
the same signals reported

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Body
## Summary

Both `archive-shipped-doc` and `bulk-archive-shipped-docs` accumulated bloat through 5+ Codex review iterations on their original PRs (#2058 + #2061). Each finding got fixed with 5-10 lines of explanation rather than 1-2 lines of rule. Result was 666 total lines for what's fundamentally simple work.

Slimmed down with **no behavioral change** — all the load-bearing rules Codex iterated us to are preserved.

## Line count

| File | Before | After | Δ |
|---|---|---|---|
| `archive-shipped-doc/SKILL.md` | 289 | 95 | -67% |
| `archive-shipped-doc/references/classification-rules.md` | 122 | 33 | -73% |
| `bulk-archive-shipped-docs/SKILL.md` | 255 | 83 | -67% |
| **Total** | **666** | **211** | **-68%** |

Description blocks roughly halved too (archive ~70 words, bulk ~60 words).

## What got cut

- Long "why this exists" preambles → frontmatter description carries it
- "Staging checklist" section that duplicated workflow steps
- "When you might be wrong" philosophical preamble → condensed to one trailing block on real failure modes
- "Don't-do list" duplicating what workflow already says
- Verbose worked examples → most folded into condensed bullets
- Full JSON schema spelled twice → kept only the fenced example
- Long "two-phase design" rationale in bulk → one line "why parent does execution (races + cross-batch awareness)"
- "Future cron driver" expanded section → 2 lines

## What was preserved

Every Codex finding from the original 5 review rounds:

- `web/` → `web/app/` is substitute not prepend
- `gh` failure = inconclusive, never negative
- Spec subtypes `-design`/`-rfd`/`-review` with "preserve if source has them"
- Bare `docs/...` is NOT repo-root-absolute in Markdown — must recompute relative
- Basename grep collides across 7+ plan/spec pairs in this repo — verify hits resolve to source
- `git add` after `Edit` (Git doesn't auto-stage post-`git mv` edits)
- Frozen-snapshot rule for refs inside `docs/archive/`
- "When in doubt, abstain" as the bias
- Batch plan validation BEFORE any execution (collision / exists / vanished)
- Subagents run Steps 1-6 (analysis + planning, including `target` computation), not 1-4

## Test plan

- [ ] Re-read each SKILL.md end-to-end and confirm a new contributor could follow the workflow without missing anything load-bearing
- [ ] Mental dry-run of the previous "vulture plan" test case (PR #2058 demo) against the slim version — verdict should still be PARTIAL with the same signals reported

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [551d6f6] refactor(web): migrate useCustomAgentPublishes server-data to uid-keyed RQ + persister (#2000 Bucket-4 A6) (#2062)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T14:13:30Z
- **PR**: #2062

### Commit Message
```
refactor(web): migrate useCustomAgentPublishes server-data to uid-keyed RQ + persister (#2000 Bucket-4 A6) (#2062)

## Summary

Bucket-4 **A6 main PR** for #2000 — flips the `agentCatalogPrivate`
query family from token-keyed to uid-keyed so the
`useCustomAgentPublishes` remote half can ride the persister allowlist
(`PERSIST_ALLOWLIST_PREFIXES`) without exposing the plaintext
`access_token` in sessionStorage.

B3 (#2053) already split off the draft half into
`lib/custom-agent-publish-draft-store.ts`; this PR finishes the A6
server-data half. The hook keeps `authToken !== null` as the `enabled`
gate (so the network is still gated by login state) but the cache
identity is now the uid. Same pattern as Bucket-2/3 + A5 — uid is bound
1:1 to the account, never a secret.

**Contributes to** #2000 (Bucket-4). **Does not close** it — A7
(cronHelpers) is being done in a parallel PR.

## Migration diff

| | Before | After |
|---|---|---|
| `agentCatalogPrivate` factory arg | `authToken: string \| null` |
`uid: string \| null` |
| Key shape | `[v1, openclaw, agent-catalog, private, <token>]` | `[v1,
openclaw, agent-catalog, private, <uid>]` |
| `useCustomAgentPublishes` queryKey |
`openclawKeys.agentCatalogPrivate(authToken)` |
`openclawKeys.agentCatalogPrivate(uid)` |
| `enabled` gate | `authToken !== null` (unchanged) | `authToken !==
null` (unchanged) |
| Persister allowlist | _not allowlisted_ |
`AGENT_CATALOG_PRIVATE_QUERY_KEY_PREFIX` in `PERSIST_ALLOWLIST_PREFIXES`
|
| `PERSIST_ALLOWLIST_PREFIXES` length | 6 | 7 |
| Per-prefix TTL | n/a | none (default 24h `maxAge`, same as A5 /
identity) |

## Caller switch list

`useCustomAgentPublishes` reads the queryKey once into a `const queryKey
= openclawKeys.agentCatalogPrivate(uid)` and reuses it through every
code path. **No standalone call site outside the hook needed migration**
— `grep`ed `openclawKeys.agentCatalogPrivate(`,
`queryClient.invalidateQueries({ queryKey:
openclawKeys.agentCatalogPrivate(...) })`,
`queryClient.setQueryData(openclawKeys.agentCatalogPrivate(...), ...)`
across `web/app/src/` + `web/app/tests/`:

- `web/app/src/hooks/useCustomAgentPublishes.ts` — 1 const + 2 type refs
in helper sigs (all flow from the const, updated in-place).

No `useQuery` / `setQueryData` / `invalidateQueries` consumer elsewhere
references this key, so the migration is contained to the hook + its
sibling key factory + the persister allowlist + the two specs.

## Test plan

- [x] `tests/unit/lib/query/persist-client.unit.spec.ts`: existing
"still token-keyed" assertion flipped to a `true` uid-keyed dehydration
check (`returns true for Bucket-4 A6 uid-keyed agentCatalogPrivate
queries`) with two distinct uids pinned; prefix list length assertion
6→7 + `containEqual(AGENT_CATALOG_PRIVATE_QUERY_KEY_PREFIX)`.
- [x] `tests/unit/hooks/useCustomAgentPublishes.unit.spec.ts`:
- Existing cross-account isolation test (`keeps remote catalogs isolated
across uids (cross-account)`) renamed and re-commented to describe uid
scoping; **still passes unchanged** because the fixtures already use
distinct uids per account.
- **New regression** `uid-scoped queryKey survives a token rotation
(same-uid cache reuse, Bucket-4 A6)` — pins the UX win the uid route
delivers: same-uid token rotation reuses the cache. Falsifiability
anchor (in the test): revert `agentCatalogPrivate` to take `authToken`
and this test flips red.
- Existing `does not route a same-id local draft to remote DELETE after
an account switch` + `mutation completing after a bucket switch updates
only the original account cache` comments updated to reflect uid-keyed
isolation.
- [x] `npx tsc --noEmit` clean
- [x] Full vitest run: **6226 tests pass** (above the 6189 baseline from
A5)
- [x] `pnpm lint` clean
- [x] `pnpm lint:ci` clean (dep-cruiser + knip)
- [x] `bash web/scripts/check-cache-governance-disables-shrink-only.sh`
— main 3, HEAD 3 (R2/R3 shrink-only **persists at 3**)

## Explicitly out of scope

- **B3 draft store** (`lib/custom-agent-publish-draft-store.ts` +
`useCustomAgentPublishDrafts`) — already shipped in #2053, untouched
here.
- **cronHelpers (A7)** — running in a **parallel PR**; the only shared
touch-point is `PERSIST_ALLOWLIST_PREFIXES` (this PR appends
`AGENT_CATALOG_PRIVATE_QUERY_KEY_PREFIX`, A7 will append
`CRON_JOBS_QUERY_KEY_PREFIX` — append-only, conflict-free).
- **useUserAgents (A5)** — shipped in #2054.
- **Cross-tab broadcast** — deferred to #1997
(`@tanstack/query-broadcast-client-experimental` evaluation), same as
A5.

## Related

- Umbrella: #1868
- Bucket-4: #2000 (this PR is A6 main, **not** closing)
- Predecessors: #1990 (B-1) / #1998 (B-2) / #1999 (B-3) / #2049
(Phase-0) / #2053 (B3 draft store) / #2054 (A5 useUserAgents)
- Parallel: A7 cronHelpers (separate branch)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Bucket-4 **A6 main PR** for #2000 — flips the `agentCatalogPrivate` query family from token-keyed to uid-keyed so the `useCustomAgentPublishes` remote half can ride the persister allowlist (`PERSIST_ALLOWLIST_PREFIXES`) without exposing the plaintext `access_token` in sessionStorage.

B3 (#2053) already split off the draft half into `lib/custom-agent-publish-draft-store.ts`; this PR finishes the A6 server-data half. The hook keeps `authToken !== null` as the `enabled` gate (so the network is still gated by login state) but the cache identity is now the uid. Same pattern as Bucket-2/3 + A5 — uid is bound 1:1 to the account, never a secret.

**Contributes to** #2000 (Bucket-4). **Does not close** it — A7 (cronHelpers) is being done in a parallel PR.

## Migration diff

| | Before | After |
|---|---|---|
| `agentCatalogPrivate` factory arg | `authToken: string \| null` | `uid: string \| null` |
| Key shape | `[v1, openclaw, agent-catalog, private, <token>]` | `[v1, openclaw, agent-catalog, private, <uid>]` |
| `useCustomAgentPublishes` queryKey | `openclawKeys.agentCatalogPrivate(authToken)` | `openclawKeys.agentCatalogPrivate(uid)` |
| `enabled` gate | `authToken !== null` (unchanged) | `authToken !== null` (unchanged) |
| Persister allowlist | _not allowlisted_ | `AGENT_CATALOG_PRIVATE_QUERY_KEY_PREFIX` in `PERSIST_ALLOWLIST_PREFIXES` |
| `PERSIST_ALLOWLIST_PREFIXES` length | 6 | 7 |
| Per-prefix TTL | n/a | none (default 24h `maxAge`, same as A5 / identity) |

## Caller switch list

`useCustomAgentPublishes` reads the queryKey once into a `const queryKey = openclawKeys.agentCatalogPrivate(uid)` and reuses it through every code path. **No standalone call site outside the hook needed migration** — `grep`ed `openclawKeys.agentCatalogPrivate(`, `queryClient.invalidateQueries({ queryKey: openclawKeys.agentCatalogPrivate(...) })`, `queryClient.setQueryData(openclawKeys.agentCatalogPrivate(...), ...)` across `web/app/src/` + `web/app/tests/`:

- `web/app/src/hooks/useCustomAgentPublishes.ts` — 1 const + 2 type refs in helper sigs (all flow from the const, updated in-place).

No `useQuery` / `setQueryData` / `invalidateQueries` consumer elsewhere references this key, so the migration is contained to the hook + its sibling key factory + the persister allowlist + the two specs.

## Test plan

- [x] `tests/unit/lib/query/persist-client.unit.spec.ts`: existing "still token-keyed" assertion flipped to a `true` uid-keyed dehydration check (`returns true for Bucket-4 A6 uid-keyed agentCatalogPrivate queries`) with two distinct uids pinned; prefix list length assertion 6→7 + `containEqual(AGENT_CATALOG_PRIVATE_QUERY_KEY_PREFIX)`.
- [x] `tests/unit/hooks/useCustomAgentPublishes.unit.spec.ts`:
  - Existing cross-account isolation test (`keeps remote catalogs isolated across uids (cross-account)`) renamed and re-commented to describe uid scoping; **still passes unchanged** because the fixtures already use distinct uids per account.
  - **New regression** `uid-scoped queryKey survives a token rotation (same-uid cache reuse, Bucket-4 A6)` — pins the UX win the uid route delivers: same-uid token rotation reuses the cache. Falsifiability anchor (in the test): revert `agentCatalogPrivate` to take `authToken` and this test flips red.
  - Existing `does not route a same-id local draft to remote DELETE after an account switch` + `mutation completing after a bucket switch updates only the original account cache` comments updated to reflect uid-keyed isolation.
- [x] `npx tsc --noEmit` clean
- [x] Full vitest run: **6226 tests pass** (above the 6189 baseline from A5)
- [x] `pnpm lint` clean
- [x] `pnpm lint:ci` clean (dep-cruiser + knip)
- [x] `bash web/scripts/check-cache-governance-disables-shrink-only.sh` — main 3, HEAD 3 (R2/R3 shrink-only **persists at 3**)

## Explicitly out of scope

- **B3 draft store** (`lib/custom-agent-publish-draft-store.ts` + `useCustomAgentPublishDrafts`) — already shipped in #2053, untouched here.
- **cronHelpers (A7)** — running in a **parallel PR**; the only shared touch-point is `PERSIST_ALLOWLIST_PREFIXES` (this PR appends `AGENT_CATALOG_PRIVATE_QUERY_KEY_PREFIX`, A7 will append `CRON_JOBS_QUERY_KEY_PREFIX` — append-only, conflict-free).
- **useUserAgents (A5)** — shipped in #2054.
- **Cross-tab broadcast** — deferred to #1997 (`@tanstack/query-broadcast-client-experimental` evaluation), same as A5.

## Related

- Umbrella: #1868
- Bucket-4: #2000 (this PR is A6 main, **not** closing)
- Predecessors: #1990 (B-1) / #1998 (B-2) / #1999 (B-3) / #2049 (Phase-0) / #2053 (B3 draft store) / #2054 (A5 useUserAgents)
- Parallel: A7 cronHelpers (separate branch)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [917397a] chore(skills): add bulk-archive-shipped-docs (parallel scanner + bundler) (#2061)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T14:01:56Z
- **PR**: #2061

### Commit Message
```
chore(skills): add bulk-archive-shipped-docs (parallel scanner + bundler) (#2061)

## Summary

Companion to `archive-shipped-doc` (PR #2058). That skill verifies +
archives **one doc per invocation**. With ~98 active docs in this repo,
running it manually 98 times is impractical.
**`bulk-archive-shipped-docs`** is the wrapper:

1. Enumerate every `.md` under `docs/plans/`, `docs/superpowers/plans/`,
`docs/superpowers/specs/`
2. Dispatch parallel subagents (batched 8-10 at a time) that call
`archive-shipped-doc` in **analysis-only mode** (Steps 1-4 → JSON
verdict, no file changes)
3. Parent collects all verdicts, then **sequentially executes** `git mv`
+ Step 7.5 outgoing-link rewrite + Step 8 inbound-link rewrite, with
full batch knowledge
4. Single commit + branch + push + auto-generated PR with per-doc
verdict checklist for human spot-check

## Why "parallel analysis + sequential execute" instead of full parallel

Three concrete reasons documented in SKILL.md:

1. **Inbound-link race** — 5 SHIPPED docs often share an inbound-link
target (e.g., a master spec). 5 subagents concurrently `Edit`ing that
one file would race.
2. **Cross-batch link awareness** — if X (archived) links to Y (also
archived in same batch), X's link should point at Y's NEW location. Only
the parent — after collecting all verdicts — has the full batch plan.
Subagents can't know.
3. **Git index lock pressure** — 100 subagents simultaneously running
`git mv` would serialize on `.git/index.lock` anyway. Same wall time,
added race risk.

Per the data this PR was written against: 98 active docs total (4 + 19 +
75), with **7 plan/spec same-basename pairs** that would be archived
together when their work ships — exactly the cross-batch case point #2
covers.

## Structure

```
.claude/skills/bulk-archive-shipped-docs/
└── SKILL.md   (243 lines — workflow + decisions + cron driver sketch)
```

No `references/` because all per-doc judgment lives in the inner skill
(`archive-shipped-doc/references/classification-rules.md`).

## Worst-case failure mode

False-positive archive of an in-progress doc — buries it in
`docs/archive/` where future contributors won't find it. Mitigations:

1. The inner skill's "abstain when in doubt" rule (PARTIAL / NOT_SHIPPED
skip) propagates per-doc.
2. The bulk PR's per-doc verdict checklist + skipped list is the human
catch — reviewer sees signals_passed/signals_checked for each archived
doc.
3. PR does NOT auto-merge — explicit human review required.

## Future cron driver (out of scope here)

The skill's `## Future cron driver` section sketches the wrapper: `cd
repo; git checkout main && git pull; invoke this skill; capture stdout`.
The skill exits cleanly on "nothing to archive" (no commit, no PR), so
cron noise stays low. Building that driver is a separate PR.

## Test plan

- [ ] Skill auto-discovered by Claude Code (confirmed locally — appears
in available skills list as `bulk-archive-shipped-docs`)
- [ ] Dry-run on the current 98 docs (analysis-only — produces verdict
report, no file changes) to verify the parallel dispatch + JSON parsing
works
- [ ] Real run on a small subset to verify end-to-end: enumerate →
parallel analyze → sequential execute → auto-PR
- [ ] Empty result case (artificially mark all as PARTIAL) — verify
graceful "nothing to archive" exit

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Body
## Summary

Companion to `archive-shipped-doc` (PR #2058). That skill verifies + archives **one doc per invocation**. With ~98 active docs in this repo, running it manually 98 times is impractical. **`bulk-archive-shipped-docs`** is the wrapper:

1. Enumerate every `.md` under `docs/plans/`, `docs/superpowers/plans/`, `docs/superpowers/specs/`
2. Dispatch parallel subagents (batched 8-10 at a time) that call `archive-shipped-doc` in **analysis-only mode** (Steps 1-4 → JSON verdict, no file changes)
3. Parent collects all verdicts, then **sequentially executes** `git mv` + Step 7.5 outgoing-link rewrite + Step 8 inbound-link rewrite, with full batch knowledge
4. Single commit + branch + push + auto-generated PR with per-doc verdict checklist for human spot-check

## Why "parallel analysis + sequential execute" instead of full parallel

Three concrete reasons documented in SKILL.md:

1. **Inbound-link race** — 5 SHIPPED docs often share an inbound-link target (e.g., a master spec). 5 subagents concurrently `Edit`ing that one file would race.
2. **Cross-batch link awareness** — if X (archived) links to Y (also archived in same batch), X's link should point at Y's NEW location. Only the parent — after collecting all verdicts — has the full batch plan. Subagents can't know.
3. **Git index lock pressure** — 100 subagents simultaneously running `git mv` would serialize on `.git/index.lock` anyway. Same wall time, added race risk.

Per the data this PR was written against: 98 active docs total (4 + 19 + 75), with **7 plan/spec same-basename pairs** that would be archived together when their work ships — exactly the cross-batch case point #2 covers.

## Structure

```
.claude/skills/bulk-archive-shipped-docs/
└── SKILL.md   (243 lines — workflow + decisions + cron driver sketch)
```

No `references/` because all per-doc judgment lives in the inner skill (`archive-shipped-doc/references/classification-rules.md`).

## Worst-case failure mode

False-positive archive of an in-progress doc — buries it in `docs/archive/` where future contributors won't find it. Mitigations:

1. The inner skill's "abstain when in doubt" rule (PARTIAL / NOT_SHIPPED skip) propagates per-doc.
2. The bulk PR's per-doc verdict checklist + skipped list is the human catch — reviewer sees signals_passed/signals_checked for each archived doc.
3. PR does NOT auto-merge — explicit human review required.

## Future cron driver (out of scope here)

The skill's `## Future cron driver` section sketches the wrapper: `cd repo; git checkout main && git pull; invoke this skill; capture stdout`. The skill exits cleanly on "nothing to archive" (no commit, no PR), so cron noise stays low. Building that driver is a separate PR.

## Test plan

- [ ] Skill auto-discovered by Claude Code (confirmed locally — appears in available skills list as `bulk-archive-shipped-docs`)
- [ ] Dry-run on the current 98 docs (analysis-only — produces verdict report, no file changes) to verify the parallel dispatch + JSON parsing works
- [ ] Real run on a small subset to verify end-to-end: enumerate → parallel analyze → sequential execute → auto-PR
- [ ] Empty result case (artificially mark all as PARTIAL) — verify graceful "nothing to archive" exit

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [68d6411] refactor(web): migrate useUserAgents to uid-keyed RQ + persister (#2000 Bucket-4 A5) (#2054)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T13:37:22Z
- **PR**: #2054

### Commit Message
```
refactor(web): migrate useUserAgents to uid-keyed RQ + persister (#2000 Bucket-4 A5) (#2054)

## Summary

Contributes to #2000 (Bucket-4 A5 — **not closed** by this PR; A6, A7,
B3 still pending).

Replaces the hand-maintained `localStorage[ecap:agents:cache]` mirror +
`ecap:agents:cache:owner` token sentinel + `_latestFetchByOwner`
seq-stamp guard + `ecap:agents:updated` window-event fanout with a
**uid-keyed** React Query bucket persisted via
`AGENTS_QUERY_KEY_PREFIX`. Same model as Bucket-2/3 (clawIdentity /
runtime-skills) — per-uid isolation comes from the queryKey itself, not
a hand-rolled owner check. Safe to persist without #1309 (uid, not auth
token).

## Migration diff

| Pre-#2000 | Post-#2000 (A5) |
|---|---|
| queryKey `openclawKeys.agents(authToken)` | `openclawKeys.agents(uid)`
(`AGENTS_QUERY_KEY_PREFIX` exported from `lib/query/keys.ts`) |
| `localStorage.setItem(AGENTS_CACHE, ...)` write | deleted — persister
owns sessionStorage via `PERSIST_ALLOWLIST_PREFIXES` |
| `localStorage.setItem(AGENTS_CACHE_OWNER_KEY, token)` sentinel |
deleted — uid-in-queryKey provides isolation |
| `_latestFetchByOwner` seq-stamp dedup | deleted — RQ provides per-key
dedup |
| `window.dispatchEvent(new Event('ecap:agents:updated'))` producers (×
2) | deleted — replaced by
`getQueryClient().setQueryData(openclawKeys.agents(uid), ...)` inside
`fetchUserAgents` |
| `window.addEventListener('ecap:agents:updated', ...)` in
`MattermostProvider` | `getQueryClient().getQueryCache().subscribe(...)`
filtered to `'success'` updates under `AGENTS_QUERY_KEY_PREFIX` |
| `window.addEventListener('ecap:agents:updated', ...)` + `storage`
listener in `useUserAgents` | deleted — RQ observers + persister
hydration replace both |
| `initialData: readAgentsCacheForCurrentSession(...)` reading
localStorage | deleted — persister `syncRestoreCache` seeds the bucket
pre-render |

## Caller switches

- `useDeepLinkHireFlow` warm-cache: `refreshUserAgentsCache()` now
writes the RQ bucket directly on resolve, so the imperative call
propagates to every mounted observer with no extra `prefetchQuery`
wrapper (caller-stable API preserved).
- `useOpenClawInit.recreate`: deleted `window.dispatchEvent(...)` + R3
inline disable; replaced by `getQueryClient().invalidateQueries({
queryKey: openclawKeys.agents(uid) })`. The legacy
`localStorage.removeItem(AGENTS_CACHE)` +
`removeItem(AGENTS_PENDING_SYNC)` calls stay one cycle to drain residue
from older deploys.
- `useAgentInstallToggle` / `OpenClawAssistantMessage` /
`useAgentActions` / `useLandingContextFlow` / `CompanionSelectStep` /
`useOpenClawVisibilityRecovery`: all `refreshUserAgentsCache()` callers
unchanged — the function's external signature is preserved; only its
internal carrier changed from window-event to `setQueryData`.

## Persister entry

`AGENTS_QUERY_KEY_PREFIX = [QUERY_VERSION, 'openclaw', 'agents']` added
to `PERSIST_ALLOWLIST_PREFIXES` (length 5 → 6). No per-prefix TTL —
agents data rides the default 24h `maxAge`, same as the identity family.
`persist-client.unit.spec.ts` updated to assert containEqual +
`shouldDehydrateQuery(makeQuery(openclawKeys.agents('uid-1')))` returns
`true` (was `false` under the old token-keyed allowlist).

## R3 shrink-only

`bash web/scripts/check-cache-governance-disables-shrink-only.sh`
reports **main: 5, HEAD: 3** ✅. The two deleted inline
`eslint-disable-next-line no-restricted-syntax` comments are:
- `web/app/src/hooks/useUserAgents.ts` — `fetchAndPersistAgents` event
dispatch
- `web/app/src/hooks/useOpenClawInit.ts` — `recreate` event dispatch

## Test plan

- [x] `npx tsc --noEmit` clean
- [x] `vitest run` — 6185 pass / 1 todo (no regressions vs main;
`useUserAgents.unit.spec.ts` rewritten to seed via
`queryClient.setQueryData` instead of localStorage owner-token;
`MattermostContext.unit.spec.tsx` listener cleanup test rewritten as RQ
subscription cleanup with positive flip)
- [x] `pnpm lint` + `pnpm lint:ci` clean
- [x] `check-cache-governance-disables-shrink-only.sh` passes (5 → 3)
- [ ] Manual staging smoke (post-merge): agents list survives hard
refresh in sessionStorage `ecap:rq-cache`; DevTools confirms no
plaintext access_token in persisted payload (uid only).

## Explicit non-goals

- Does **not** touch `useCustomAgentPublishes` / `agent-catalog-private`
(B3 / A6 scope).
- Does **not** touch `cronHelpers` storage (A7 scope).
- Does **not** touch `session-cache.ts` (already deleted in #2046).
- Does **not** touch the #1309 mm-blob path.
- Does **not** close #2000.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Codex round-1 follow-up (commit `17ebebaae`)

Two findings from the initial Codex review, both addressed in the latest
push:

### Finding 1 (HIGH risk) — cross-tab regression: deferred to #1997

Pre-#2000 `useUserAgents` mirrored agents into
`localStorage[AGENTS_CACHE]`, which gave cross-tab sync for free via the
browser's `storage` event. The persister uses `sessionStorage`
(tab-local by design, shared across Bucket-1/2/3 / #1990 / #1998 /
#1999), so another tab's hire/fire is no longer propagated until the
current tab's next refetch.

**Decision: defer to #1997**
(`@tanstack/query-broadcast-client-experimental` evaluation). Adding a
per-family `localStorage` mirror just for agents would contradict the
global persister selection and complicate every future query family's
choice. `#1997` is the correct architectural fix.

Documented inline in `useUserAgents` so future readers (and the
publish-confirm flow that reads `installedIds` to decide install vs
uninstall) see the trade-off + the recommended workaround (explicit
`refetch()` at decision time).

### Finding 2 (HIGH risk) — `currentUid` vs `resolvedUid` mismatch:
fixed

`useOpenClawInit.ts:478` was invalidating
`openclawKeys.agents(getUserInfo().uid)`, but the recreate mutation
above ran against the hook's captured `resolvedUid`. Re-init / account
transition could leave the WRONG agents bucket warm.

- Fixed: invalidate uses `resolvedUid` (same source-of-truth as the
mutation).
- Dropped the now-unused `getUserInfo` import.
- New regression test in `tests/unit/hooks/useOpenClawInit.unit.spec.ts`
exercises the divergence scenario (mock returns `'user-from-auth'`
mid-flight; hook still uses `'user1'`).
- Falsifiability anchor verified locally: reverting to
`getUserInfo().uid` makes the new test red.

## Test plan

- [x] `pnpm lint` clean
- [x] `npx tsc --noEmit` clean
- [x] `pnpm lint:ci` clean
- [x] `./node_modules/.bin/vitest run` — 407 files / 6186 tests / 1 todo
- [x] `bash web/scripts/check-cache-governance-disables-shrink-only.sh`
— main 5, HEAD 3 ✅

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Contributes to #2000 (Bucket-4 A5 — **not closed** by this PR; A6, A7, B3 still pending).

Replaces the hand-maintained `localStorage[ecap:agents:cache]` mirror + `ecap:agents:cache:owner` token sentinel + `_latestFetchByOwner` seq-stamp guard + `ecap:agents:updated` window-event fanout with a **uid-keyed** React Query bucket persisted via `AGENTS_QUERY_KEY_PREFIX`. Same model as Bucket-2/3 (clawIdentity / runtime-skills) — per-uid isolation comes from the queryKey itself, not a hand-rolled owner check. Safe to persist without #1309 (uid, not auth token).

## Migration diff

| Pre-#2000 | Post-#2000 (A5) |
|---|---|
| queryKey `openclawKeys.agents(authToken)` | `openclawKeys.agents(uid)` (`AGENTS_QUERY_KEY_PREFIX` exported from `lib/query/keys.ts`) |
| `localStorage.setItem(AGENTS_CACHE, ...)` write | deleted — persister owns sessionStorage via `PERSIST_ALLOWLIST_PREFIXES` |
| `localStorage.setItem(AGENTS_CACHE_OWNER_KEY, token)` sentinel | deleted — uid-in-queryKey provides isolation |
| `_latestFetchByOwner` seq-stamp dedup | deleted — RQ provides per-key dedup |
| `window.dispatchEvent(new Event('ecap:agents:updated'))` producers (× 2) | deleted — replaced by `getQueryClient().setQueryData(openclawKeys.agents(uid), ...)` inside `fetchUserAgents` |
| `window.addEventListener('ecap:agents:updated', ...)` in `MattermostProvider` | `getQueryClient().getQueryCache().subscribe(...)` filtered to `'success'` updates under `AGENTS_QUERY_KEY_PREFIX` |
| `window.addEventListener('ecap:agents:updated', ...)` + `storage` listener in `useUserAgents` | deleted — RQ observers + persister hydration replace both |
| `initialData: readAgentsCacheForCurrentSession(...)` reading localStorage | deleted — persister `syncRestoreCache` seeds the bucket pre-render |

## Caller switches

- `useDeepLinkHireFlow` warm-cache: `refreshUserAgentsCache()` now writes the RQ bucket directly on resolve, so the imperative call propagates to every mounted observer with no extra `prefetchQuery` wrapper (caller-stable API preserved).
- `useOpenClawInit.recreate`: deleted `window.dispatchEvent(...)` + R3 inline disable; replaced by `getQueryClient().invalidateQueries({ queryKey: openclawKeys.agents(uid) })`. The legacy `localStorage.removeItem(AGENTS_CACHE)` + `removeItem(AGENTS_PENDING_SYNC)` calls stay one cycle to drain residue from older deploys.
- `useAgentInstallToggle` / `OpenClawAssistantMessage` / `useAgentActions` / `useLandingContextFlow` / `CompanionSelectStep` / `useOpenClawVisibilityRecovery`: all `refreshUserAgentsCache()` callers unchanged — the function's external signature is preserved; only its internal carrier changed from window-event to `setQueryData`.

## Persister entry

`AGENTS_QUERY_KEY_PREFIX = [QUERY_VERSION, 'openclaw', 'agents']` added to `PERSIST_ALLOWLIST_PREFIXES` (length 5 → 6). No per-prefix TTL — agents data rides the default 24h `maxAge`, same as the identity family. `persist-client.unit.spec.ts` updated to assert containEqual + `shouldDehydrateQuery(makeQuery(openclawKeys.agents('uid-1')))` returns `true` (was `false` under the old token-keyed allowlist).

## R3 shrink-only

`bash web/scripts/check-cache-governance-disables-shrink-only.sh` reports **main: 5, HEAD: 3** ✅. The two deleted inline `eslint-disable-next-line no-restricted-syntax` comments are:
- `web/app/src/hooks/useUserAgents.ts` — `fetchAndPersistAgents` event dispatch
- `web/app/src/hooks/useOpenClawInit.ts` — `recreate` event dispatch

## Test plan

- [x] `npx tsc --noEmit` clean
- [x] `vitest run` — 6185 pass / 1 todo (no regressions vs main; `useUserAgents.unit.spec.ts` rewritten to seed via `queryClient.setQueryData` instead of localStorage owner-token; `MattermostContext.unit.spec.tsx` listener cleanup test rewritten as RQ subscription cleanup with positive flip)
- [x] `pnpm lint` + `pnpm lint:ci` clean
- [x] `check-cache-governance-disables-shrink-only.sh` passes (5 → 3)
- [ ] Manual staging smoke (post-merge): agents list survives hard refresh in sessionStorage `ecap:rq-cache`; DevTools confirms no plaintext access_token in persisted payload (uid only).

## Explicit non-goals

- Does **not** touch `useCustomAgentPublishes` / `agent-catalog-private` (B3 / A6 scope).
- Does **not** touch `cronHelpers` storage (A7 scope).
- Does **not** touch `session-cache.ts` (already deleted in #2046).
- Does **not** touch the #1309 mm-blob path.
- Does **not** close #2000.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Codex round-1 follow-up (commit `17ebebaae`)

Two findings from the initial Codex review, both addressed in the latest push:

### Finding 1 (HIGH risk) — cross-tab regression: deferred to #1997

Pre-#2000 `useUserAgents` mirrored agents into `localStorage[AGENTS_CACHE]`, which gave cross-tab sync for free via the browser's `storage` event. The persister uses `sessionStorage` (tab-local by design, shared across Bucket-1/2/3 / #1990 / #1998 / #1999), so another tab's hire/fire is no longer propagated until the current tab's next refetch.

**Decision: defer to #1997** (`@tanstack/query-broadcast-client-experimental` evaluation). Adding a per-family `localStorage` mirror just for agents would contradict the global persister selection and complicate every future query family's choice. `#1997` is the correct architectural fix.

Documented inline in `useUserAgents` so future readers (and the publish-confirm flow that reads `installedIds` to decide install vs uninstall) see the trade-off + the recommended workaround (explicit `refetch()` at decision time).

### Finding 2 (HIGH risk) — `currentUid` vs `resolvedUid` mismatch: fixed

`useOpenClawInit.ts:478` was invalidating `openclawKeys.agents(getUserInfo().uid)`, but the recreate mutation above ran against the hook's captured `resolvedUid`. Re-init / account transition could leave the WRONG agents bucket warm.

- Fixed: invalidate uses `resolvedUid` (same source-of-truth as the mutation).
- Dropped the now-unused `getUserInfo` import.
- New regression test in `tests/unit/hooks/useOpenClawInit.unit.spec.ts` exercises the divergence scenario (mock returns `'user-from-auth'` mid-flight; hook still uses `'user1'`).
- Falsifiability anchor verified locally: reverting to `getUserInfo().uid` makes the new test red.

## Test plan

- [x] `pnpm lint` clean
- [x] `npx tsc --noEmit` clean
- [x] `pnpm lint:ci` clean
- [x] `./node_modules/.bin/vitest run` — 407 files / 6186 tests / 1 todo
- [x] `bash web/scripts/check-cache-governance-disables-shrink-only.sh` — main 5, HEAD 3 ✅



---
## [b7d4e33] chore(skills): add archive-shipped-doc skill (repo-local) (#2058)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T13:32:58Z
- **PR**: #2058

### Commit Message
```
chore(skills): add archive-shipped-doc skill (repo-local) (#2058)

## Summary

Repo-local Claude Code skill that codifies the doc-archive workflow
hand-applied to ~40 docs in the May 2026 archive audit (PRs #2052 /
#2055).

**What it does**: Takes one doc path under `docs/plans/`,
`docs/superpowers/plans/`, or `docs/superpowers/specs/`. Verifies the
described work has shipped by checking referenced files / symbols /
endpoints / PRs against current code. If verified shipped, runs `git mv`
to the correct `docs/archive/{plans,specs,prds}/` bucket — with filename
suffix normalized to match content type. Updates inbound links in
**live** docs; leaves links inside `docs/archive/` alone
(frozen-snapshot rule).

**Stages the move, never commits.** Leaves `git status` showing the
rename + inbound edits for human (or automation) review.

## Why now

- Active dirs accumulate cruft: shipped docs sit next to in-progress
docs and new contributors can't tell what's current intent
- The manual workflow is judgment-heavy but mechanical when bucket rules
+ verification approach are codified — that's exactly what the skill
carries
- **Future use case**: a scheduled wrapper will iterate over all active
docs, invoke this skill on each, bundle SHIPPED verdicts into one
auto-generated PR. The skill's structured JSON output block is designed
for that wrapper to parse — see "Future cron wrapper" in the planning
doc

## Structure

```
.claude/skills/archive-shipped-doc/
├── SKILL.md                     # workflow + decision rules (~230 lines)
└── references/
    └── classification-rules.md   # the 3 bucket definitions with examples (~120 lines)
```

Sibling to the existing `.claude/skills/diff-stats/` — same repo-local
pattern.

## Skill design highlights

- **One doc per invocation** by design; batch is the wrapper's job
- **Verdicts**: `SHIPPED` / `PARTIAL` / `NOT_SHIPPED` /
`DESIGN_ONLY_VERIFIED`
- **Trust content over filename**: e.g., a `*-plan.md` whose content is
a design doc → rename to `*-design.md` when archiving
- **`web/X` → `web/app/X` rewrite check**: explicitly handled because
this monorepo restructure broke ~30 doc references during the audit
- **Structured JSON output block** at the end of every report for
downstream automation
- **Conservative**: when in doubt, abstain (return PARTIAL /
NOT_SHIPPED). False positives bury work-in-progress docs in archive
where future contributors won't find them — worse than leaving an extra
doc in the active dir.

## Test plan

- [ ] Verify skill is auto-discovered by Claude Code (it appears in the
available-skills list — confirmed locally during this session)
- [ ] Spot-test on 2-3 known SHIPPED docs from `docs/superpowers/plans/`
(e.g., `2026-05-13-backend-vulture-dead-code.md` — vulture is per
`services/claw-interface/CLAUDE.md` shipped)
- [ ] Spot-test on a known NOT_SHIPPED spec (one with `Status: Design —
pending implementation`) — confirm abstains
- [ ] Spot-test on a doc already under `docs/archive/` — confirm errors
out
- [ ] Confirm `git status` shows staged renames + inbound edits, no
commit
- [ ] Confirm `git log --follow` on moved file preserves history (would
fail if `cp+rm` was used)
- [ ] Confirm fenced JSON block at end of report parses with `jq`

Eval iteration via `/skill-creator` is a suggested follow-up — the plan
file lists candidate evals at
`~/.claude/plans/skill-docs-plans-distributed-wave.md`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Repo-local Claude Code skill that codifies the doc-archive workflow hand-applied to ~40 docs in the May 2026 archive audit (PRs #2052 / #2055).

**What it does**: Takes one doc path under `docs/plans/`, `docs/superpowers/plans/`, or `docs/superpowers/specs/`. Verifies the described work has shipped by checking referenced files / symbols / endpoints / PRs against current code. If verified shipped, runs `git mv` to the correct `docs/archive/{plans,specs,prds}/` bucket — with filename suffix normalized to match content type. Updates inbound links in **live** docs; leaves links inside `docs/archive/` alone (frozen-snapshot rule).

**Stages the move, never commits.** Leaves `git status` showing the rename + inbound edits for human (or automation) review.

## Why now

- Active dirs accumulate cruft: shipped docs sit next to in-progress docs and new contributors can't tell what's current intent
- The manual workflow is judgment-heavy but mechanical when bucket rules + verification approach are codified — that's exactly what the skill carries
- **Future use case**: a scheduled wrapper will iterate over all active docs, invoke this skill on each, bundle SHIPPED verdicts into one auto-generated PR. The skill's structured JSON output block is designed for that wrapper to parse — see "Future cron wrapper" in the planning doc

## Structure

```
.claude/skills/archive-shipped-doc/
├── SKILL.md                     # workflow + decision rules (~230 lines)
└── references/
    └── classification-rules.md   # the 3 bucket definitions with examples (~120 lines)
```

Sibling to the existing `.claude/skills/diff-stats/` — same repo-local pattern.

## Skill design highlights

- **One doc per invocation** by design; batch is the wrapper's job
- **Verdicts**: `SHIPPED` / `PARTIAL` / `NOT_SHIPPED` / `DESIGN_ONLY_VERIFIED`
- **Trust content over filename**: e.g., a `*-plan.md` whose content is a design doc → rename to `*-design.md` when archiving
- **`web/X` → `web/app/X` rewrite check**: explicitly handled because this monorepo restructure broke ~30 doc references during the audit
- **Structured JSON output block** at the end of every report for downstream automation
- **Conservative**: when in doubt, abstain (return PARTIAL / NOT_SHIPPED). False positives bury work-in-progress docs in archive where future contributors won't find them — worse than leaving an extra doc in the active dir.

## Test plan

- [ ] Verify skill is auto-discovered by Claude Code (it appears in the available-skills list — confirmed locally during this session)
- [ ] Spot-test on 2-3 known SHIPPED docs from `docs/superpowers/plans/` (e.g., `2026-05-13-backend-vulture-dead-code.md` — vulture is per `services/claw-interface/CLAUDE.md` shipped)
- [ ] Spot-test on a known NOT_SHIPPED spec (one with `Status: Design — pending implementation`) — confirm abstains
- [ ] Spot-test on a doc already under `docs/archive/` — confirm errors out
- [ ] Confirm `git status` shows staged renames + inbound edits, no commit
- [ ] Confirm `git log --follow` on moved file preserves history (would fail if `cp+rm` was used)
- [ ] Confirm fenced JSON block at end of report parses with `jq`

Eval iteration via `/skill-creator` is a suggested follow-up — the plan file lists candidate evals at `~/.claude/plans/skill-docs-plans-distributed-wave.md`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [b3251ef] fix(arch-review): strip spurious shell escapes from jq filters (#2059)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T13:22:03Z
- **PR**: #2059

### Commit Message
```
fix(arch-review): strip spurious shell escapes from jq filters (#2059)

## Summary

Hotfix for #2031. Dry-run on web (run
[26576402541](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/26576402541))
hit a jq syntax error in the "Mark resolved findings on source issues"
step:

```
jq: error: syntax error, unexpected INVALID_CHARACTER (Unix shell quoting issues?)
to_entries[] | "\(.key)|\(.value | join(\",\"))"
```

## Root cause

Two jq filters in `claude-arch-review.yaml` escape `"` inside
**single-shell-quoted** arguments — `\",\"` and `\", \"`. Single quotes
already protect the `"` from shell interpretation, so jq receives `\"`
as **backslash + quote in expression context** (inside the `\(...)`
interpolation), which is invalid jq syntax. jq exits 3.

The "Reconcile against baseline" step has the same broken filter but
inline in an `echo`, so `set -e` doesn't propagate the non-zero exit
through `$()` in string interpolation — it failed silently to stderr
while the step itself reported success. The "Mark resolved findings"
step captures the value of the substitution and propagates the failure.

## Fix

Drop the backslash before each `"` in the inner `join(...)` arg. Inside
jq's `\(...)` interpolation, `","` is a plain string literal — no shell
or jq escaping needed because the surrounding shell single quotes
already protect it.

| Before | After |
|---|---|
| `'to_entries[] \| "\(.key)\|\(.value \| join(\",\"))"'` |
`'to_entries[] \| "\(.key)\|\(.value \| join(","))"'` |
| `'to_entries[] \| " #\(.key): \(.value \| join(\", \"))"'` |
`'to_entries[] \| " #\(.key): \(.value \| join(", "))"'` |

## Verification

Local reproduction + fix:
```bash
$ echo '{"368":["F13","F14"]}' > /tmp/r.json

$ jq -r 'to_entries[] | "\(.key)|\(.value | join(\",\"))"' /tmp/r.json
jq: error: syntax error, unexpected INVALID_CHARACTER

$ jq -r 'to_entries[] | "\(.key)|\(.value | join(","))"' /tmp/r.json
368|F13,F14
```

## Test plan

- [x] Local jq reproduction confirms fix
- [ ] CI green (actionlint should catch any new YAML escaping issues)
- [ ] After merge: re-run `workflow_dispatch` with `dry_run=true` on web
to confirm the full decision-table path completes end-to-end

## Why pytest didn't catch this

The Python helpers (PR #2019, 64 unit tests) are tested in isolation.
This bug is in the bash plumbing between them — jq filters that route
reconcile.py output into mark_resolved.py input. End-to-end exercise of
the workflow YAML wasn't covered by unit tests; the dry-run mode (PR
#2031) was added for exactly this kind of gap, and worked as intended
this run.

Refs #2031, #368.
```

### PR Body
## Summary

Hotfix for #2031. Dry-run on web (run [26576402541](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/26576402541)) hit a jq syntax error in the "Mark resolved findings on source issues" step:

```
jq: error: syntax error, unexpected INVALID_CHARACTER (Unix shell quoting issues?)
to_entries[] | "\(.key)|\(.value | join(\",\"))"
```

## Root cause

Two jq filters in `claude-arch-review.yaml` escape `"` inside **single-shell-quoted** arguments — `\",\"` and `\", \"`. Single quotes already protect the `"` from shell interpretation, so jq receives `\"` as **backslash + quote in expression context** (inside the `\(...)` interpolation), which is invalid jq syntax. jq exits 3.

The "Reconcile against baseline" step has the same broken filter but inline in an `echo`, so `set -e` doesn't propagate the non-zero exit through `$()` in string interpolation — it failed silently to stderr while the step itself reported success. The "Mark resolved findings" step captures the value of the substitution and propagates the failure.

## Fix

Drop the backslash before each `"` in the inner `join(...)` arg. Inside jq's `\(...)` interpolation, `","` is a plain string literal — no shell or jq escaping needed because the surrounding shell single quotes already protect it.

| Before | After |
|---|---|
| `'to_entries[] \| "\(.key)\|\(.value \| join(\",\"))"'` | `'to_entries[] \| "\(.key)\|\(.value \| join(","))"'` |
| `'to_entries[] \| "    #\(.key): \(.value \| join(\", \"))"'` | `'to_entries[] \| "    #\(.key): \(.value \| join(", "))"'` |

## Verification

Local reproduction + fix:
```bash
$ echo '{"368":["F13","F14"]}' > /tmp/r.json

$ jq -r 'to_entries[] | "\(.key)|\(.value | join(\",\"))"' /tmp/r.json
jq: error: syntax error, unexpected INVALID_CHARACTER

$ jq -r 'to_entries[] | "\(.key)|\(.value | join(","))"' /tmp/r.json
368|F13,F14
```

## Test plan

- [x] Local jq reproduction confirms fix
- [ ] CI green (actionlint should catch any new YAML escaping issues)
- [ ] After merge: re-run `workflow_dispatch` with `dry_run=true` on web to confirm the full decision-table path completes end-to-end

## Why pytest didn't catch this

The Python helpers (PR #2019, 64 unit tests) are tested in isolation. This bug is in the bash plumbing between them — jq filters that route reconcile.py output into mark_resolved.py input. End-to-end exercise of the workflow YAML wasn't covered by unit tests; the dry-run mode (PR #2031) was added for exactly this kind of gap, and worked as intended this run.

Refs #2031, #368.

---
## [6cd7418] feat(web): render all configured Specialist quick commands (#2050)
- **作者**: vincent-srp
- **日期**: 2026-05-28T13:04:47Z
- **PR**: #2050

### Commit Message
```
feat(web): render all configured Specialist quick commands (#2050)

## Linear

https://linear.app/srpone/issue/ECA-711/zooclaw-web-agent-new-chat-%E4%BD%93%E9%AA%8C%E5%AE%8C%E5%96%84%E5%8F%AF%E9%85%8D%E7%BD%AE%E5%BF%AB%E6%8D%B7%E6%8C%87%E4%BB%A4%E5%8C%BA-specialist-%E5%BC%80%E5%9C%BA%E9%80%89%E9%A1%B9

## Summary
- 跟进已合并的 #2021（main Assistant 快捷指令重做）：移除 `MAX_QUICK_COMMAND_COUNT` 与
`configuredCommands.slice(0, 4)`，Specialist 后端配置的 `quick_commands`
**不再被静默截断到 4 个**，全部渲染。
- dropdown 宽度改为自适应
`max-w-[min(42rem,var(--radix-dropdown-menu-content-available-width))]`：桌面端
cap 在 42rem，让多个 chip 换成**紧凑多行块**而非拉满整屏；窄屏自动收缩到视口宽度。
- ds `DropdownMenuContent` 自带 `max-h` + `overflow-y-auto`，命令很多时纵向滚动兜底。

## Test plan
- [x] 单测：`ChatQuickActions.unit.spec.tsx` —— 配置 5 条命令时第 5 条也渲染（不再截断），13
passed
- [ ] 手测：某 Specialist 配多条 `quick_commands` 时，Quick start 下拉的多行布局与宽度观感

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Linear
https://linear.app/srpone/issue/ECA-711/zooclaw-web-agent-new-chat-%E4%BD%93%E9%AA%8C%E5%AE%8C%E5%96%84%E5%8F%AF%E9%85%8D%E7%BD%AE%E5%BF%AB%E6%8D%B7%E6%8C%87%E4%BB%A4%E5%8C%BA-specialist-%E5%BC%80%E5%9C%BA%E9%80%89%E9%A1%B9

## Summary
- 跟进已合并的 #2021（main Assistant 快捷指令重做）：移除 `MAX_QUICK_COMMAND_COUNT` 与 `configuredCommands.slice(0, 4)`，Specialist 后端配置的 `quick_commands` **不再被静默截断到 4 个**，全部渲染。
- dropdown 宽度改为自适应 `max-w-[min(42rem,var(--radix-dropdown-menu-content-available-width))]`：桌面端 cap 在 42rem，让多个 chip 换成**紧凑多行块**而非拉满整屏；窄屏自动收缩到视口宽度。
- ds `DropdownMenuContent` 自带 `max-h` + `overflow-y-auto`，命令很多时纵向滚动兜底。

## Test plan
- [x] 单测：`ChatQuickActions.unit.spec.tsx` —— 配置 5 条命令时第 5 条也渲染（不再截断），13 passed
- [ ] 手测：某 Specialist 配多条 `quick_commands` 时，Quick start 下拉的多行布局与宽度观感

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [78131d9] ci(arch-review): switch to cohort-issues model + Priority/Impact/Effort schema (#2031)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T13:00:40Z
- **PR**: #2031

### Commit Message
```
ci(arch-review): switch to cohort-issues model + Priority/Impact/Effort schema (#2031)

## Summary

PR 3 of 3 for the arch-review cohort-issues rollout. Design spec:
[`docs/superpowers/specs/2026-05-28-arch-review-cohort-issues.md`](docs/superpowers/specs/2026-05-28-arch-review-cohort-issues.md)
(#2015). Helper scripts + tests: #2019.

This PR wires the helper scripts into `claude-arch-review.yaml`,
replaces the inline 200-line Python compose step with structured script
calls, and switches the issue model from **append-only rolling** to
**event-sourced cohorts**.

## Workflow changes

| Step | Before | After |
|---|---|---|
| Snapshot baseline | `gh issue view` newest issue only | `gh issue list
--limit 200` → `compose_baseline.py` aggregates ALL open
`arch-review:<module>` issues |
| Validate schema | — | **NEW**: `validate_schema.py --mode new`
fail-loud before any mutation |
| Compose | 200-line inline Python doing all the merge logic |
`reconcile.py` → `new_findings.md` + `resolutions.json` + `summary.md` |
| Apply (resolve) | full body rewrite of single issue | per-issue
`mark_resolved.py` + auto-close when active=0 |
| Apply (new findings) | merged into the rolling issue |
`compose_new.py` creates a new cohort issue, cross-links other open ones
|
| Minimize stale comments | always ran | **removed** — cohort issues
don't accumulate review comments |

Plus `workflow_dispatch` gains a `dry_run: boolean` input — when true,
every `gh issue edit/create/close` routes to `$GITHUB_STEP_SUMMARY`
instead of executing. Used to dress-rehearse changes against the live
#368/#366/#365 baseline before the first cron fires.

## Decision table (the spec rule the code now enforces)

| `new_findings` | `resolved` | Behaviour |
|---|---|---|
| ∅ | ∅ | Nothing happens. No subscriber noise. |
| ∅ | non-empty | Edit each source issue: strikethrough, close if
active=0. No new issue. |
| non-empty | ∅ | Create one cohort issue with cross-link to open
arch-review issues. |
| non-empty | non-empty | Run the resolve loop first, then build
cross-link list (post-close), then create the cohort issue. |

## Schema change

`Severity` (High/Medium) → `Priority` (P0/P1/P2) + `Impact`
(Broad/Module/Local) + `Effort` (S/M/L). Carried-forward legacy blocks
keep their `Severity` verbatim; new findings must use the new schema and
must not emit `Severity`. Skill prompt (`SKILL.md` + `arch-review.md`)
updated accordingly.

## Migration

Zero one-shot script. `#368`/`#366`/`#365` continue as baseline issues;
their findings drain via the resolve pipeline week-by-week; when each
one's active count hits zero, the workflow auto-closes it. New findings
start landing in new cohort issues from the next cron fire.

## Concurrency

Added `concurrency: arch-review-<workflow>-<ref>` with
`cancel-in-progress: false` so two parallel runs can't race the F-ID
counter.

## Diff stats (excl. generated)

- 3 files changed, +245 / -351 (net -106) — replacing 200 lines of
inline Python with ~120 lines of orchestration shell
- Workflow: 487 → 315 lines

## Test plan

- [x] All 63 pytest tests still pass on the rebase
- [x] `actionlint` (CI gate)
- [ ] CI workflow `arch-review scripts` runs and passes
- [ ] After merge: trigger `workflow_dispatch` with `dry_run=true`
against `arch-review:web` and verify the step summary correctly
describes the no-op vs. resolve/create paths
- [ ] After dry-run looks right: let the cron fire on Monday OR trigger
a real `workflow_dispatch` for one module and confirm new cohort issue
is created + cross-links to #368 etc.

## Out of scope (per spec)

- Auto-assigning cohort issues
- Linking PRs that addressed each finding
- Migrating existing #368/#366/#365 active findings to cohort issues in
one shot
```

### PR Body
## Summary

PR 3 of 3 for the arch-review cohort-issues rollout. Design spec: [`docs/superpowers/specs/2026-05-28-arch-review-cohort-issues.md`](docs/superpowers/specs/2026-05-28-arch-review-cohort-issues.md) (#2015). Helper scripts + tests: #2019.

This PR wires the helper scripts into `claude-arch-review.yaml`, replaces the inline 200-line Python compose step with structured script calls, and switches the issue model from **append-only rolling** to **event-sourced cohorts**.

## Workflow changes

| Step | Before | After |
|---|---|---|
| Snapshot baseline | `gh issue view` newest issue only | `gh issue list --limit 200` → `compose_baseline.py` aggregates ALL open `arch-review:<module>` issues |
| Validate schema | — | **NEW**: `validate_schema.py --mode new` fail-loud before any mutation |
| Compose | 200-line inline Python doing all the merge logic | `reconcile.py` → `new_findings.md` + `resolutions.json` + `summary.md` |
| Apply (resolve) | full body rewrite of single issue | per-issue `mark_resolved.py` + auto-close when active=0 |
| Apply (new findings) | merged into the rolling issue | `compose_new.py` creates a new cohort issue, cross-links other open ones |
| Minimize stale comments | always ran | **removed** — cohort issues don't accumulate review comments |

Plus `workflow_dispatch` gains a `dry_run: boolean` input — when true, every `gh issue edit/create/close` routes to `$GITHUB_STEP_SUMMARY` instead of executing. Used to dress-rehearse changes against the live #368/#366/#365 baseline before the first cron fires.

## Decision table (the spec rule the code now enforces)

| `new_findings` | `resolved` | Behaviour |
|---|---|---|
| ∅ | ∅ | Nothing happens. No subscriber noise. |
| ∅ | non-empty | Edit each source issue: strikethrough, close if active=0. No new issue. |
| non-empty | ∅ | Create one cohort issue with cross-link to open arch-review issues. |
| non-empty | non-empty | Run the resolve loop first, then build cross-link list (post-close), then create the cohort issue. |

## Schema change

`Severity` (High/Medium) → `Priority` (P0/P1/P2) + `Impact` (Broad/Module/Local) + `Effort` (S/M/L). Carried-forward legacy blocks keep their `Severity` verbatim; new findings must use the new schema and must not emit `Severity`. Skill prompt (`SKILL.md` + `arch-review.md`) updated accordingly.

## Migration

Zero one-shot script. `#368`/`#366`/`#365` continue as baseline issues; their findings drain via the resolve pipeline week-by-week; when each one's active count hits zero, the workflow auto-closes it. New findings start landing in new cohort issues from the next cron fire.

## Concurrency

Added `concurrency: arch-review-<workflow>-<ref>` with `cancel-in-progress: false` so two parallel runs can't race the F-ID counter.

## Diff stats (excl. generated)

- 3 files changed, +245 / -351 (net -106) — replacing 200 lines of inline Python with ~120 lines of orchestration shell
- Workflow: 487 → 315 lines

## Test plan

- [x] All 63 pytest tests still pass on the rebase
- [x] `actionlint` (CI gate)
- [ ] CI workflow `arch-review scripts` runs and passes
- [ ] After merge: trigger `workflow_dispatch` with `dry_run=true` against `arch-review:web` and verify the step summary correctly describes the no-op vs. resolve/create paths
- [ ] After dry-run looks right: let the cron fire on Monday OR trigger a real `workflow_dispatch` for one module and confirm new cohort issue is created + cross-links to #368 etc.

## Out of scope (per spec)

- Auto-assigning cohort issues
- Linking PRs that addressed each finding
- Migrating existing #368/#366/#365 active findings to cohort issues in one shot

---
## [b6b0960] refactor(web): decouple custom-agent publish draft into lib/stores (#2000 Bucket-4 B3) (#2053)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T12:46:18Z
- **PR**: #2053

### Commit Message
```
refactor(web): decouple custom-agent publish draft into lib/stores (#2000 Bucket-4 B3) (#2053)

## Summary

将 `useCustomAgentPublishes.ts` 里混在一起的两类数据拆开:

- (1) 后端 catalog mirror (server response) **留在原 hook**，仍 RQ
      `openclawKeys.agentCatalogPrivate(authToken)` (本 PR **不动**
      token-keyed query key — A6 主线 PR 再迁 uid-keyed)
- (2) 用户本地未提交的 pending publishes (client-only draft) **抽到
      独立 Tier D store**:
  - `web/app/src/lib/custom-agent-publish-draft-store.ts` (~278 LOC) —
    pure data，无 react import
  - `web/app/src/lib/useCustomAgentPublishDrafts.ts` (~34 LOC) —
    `'use client'` `useSyncExternalStore` wrapper

模板取自 `lib/agent-description-store.ts` (#2013 留下的 Tier C/D 模板)，
保持 server-bundle safe 的 file split。

## Why now (#2000 Bucket-4 B3)

这是 A6 (`useCustomAgentPublishes` RQ migration to uid-keyed) 的**前置
条件**：RQ 不能持有"还没存在于 server 的 draft"——`invalidateQueries`
flush 会丢。把 draft 留在 Tier D 客户端 store 保住 A6 的 "RQ caches
reflect server state only" invariant。

参 #2000 issue body Scope 表 A6 行 + "B3 解耦" 段。

## What changed

1. **新 store** (`custom-agent-publish-draft-store.ts`) 提供:
- `getCustomAgentPublishDrafts(uid)` / `setCustomAgentPublishDrafts(uid,
drafts)`
- `removeCustomAgentPublishDraft(uid, id)` /
`clearCustomAgentPublishDrafts(uid)`
   - `subscribeCustomAgentPublishDrafts(listener)` — module-local
     `Set<() => void>` (走任务建议的方案 a，规避 R3 `ecap:*:updated`
     selector + shrink-only count 持平)
   - `refreshCustomAgentPublishDraftsFromStorage(uid)` — cross-tab
     `storage` event 入口，drop snapshot + notify
   - `getCustomAgentPublishDraftsStorageKey(uid)` — 完全照搬原
     `${STORAGE_KEYS.CUSTOM_AGENT_PUBLISHES}:${uid||'anonymous'}` shape
   - 写时格式：flat array of `CustomAgentPublishRecord`（Phase-0 #2049
     spec 锁的契约，不动）

2. **hook 改造** (`useCustomAgentPublishes.ts` 350→252 LOC):
   - 删 `subscribeRecords` / `useDraftRecords` / `draftSnapshotCache` /
     `readRecords` / `writeRecords`
   - 删 `STORAGE_EVENT = 'ecap:custom-agent-publishes:updated'` +
     `dispatchEvent`
   - draft 读改 `useCustomAgentPublishDrafts(uid)`
   - mutation 走 `setCustomAgentPublishDrafts` / 不再自写 localStorage
   - cross-tab `storage` event handler 调用
     `refreshCustomAgentPublishDraftsFromStorage(uid)` + 原 invalidate

3. **测试拆分**:
   - 新文件 `tests/unit/lib/custom-agent-publish-draft-store.unit.spec.ts`
     (~308 LOC) — 直接测 store 函数 + ref-equality snapshot cache +
     subscriber Set + `refreshFromStorage`
   - 原 `useCustomAgentPublishes-storage.unit.spec.tsx`
     (Phase-0 #2049) 保留 hook 公共面契约 (storage key /
     anonymous bucket / flat-array on delete)；ref-equality + custom
     event subscription 那条**整体搬**到 store spec
   - 原 `useCustomAgentPublishes.unit.spec.ts` 唯一改写："same-tab
     `CustomEvent` 不 refetch" → "same-tab store mutation 不 refetch"

## 不做的事 (留给 A6 / 不属于本 PR)

- ❌ 不接 RQ uid-keyed (A6 PR)
- ❌ 不动 `PERSIST_ALLOWLIST_PREFIXES`
- ❌ 不动 useUserAgents / cronHelpers
- ❌ 不 close #2000

## Shrink-only

| Rule | main | HEAD |
| ---- | ---- | ---- |
| Cache governance disables (R2 imports + R3 syntax) | **5** | **5** |

R3 没新增任何 inline disable —— store 用 module-local listener Set 替代
window event dispatch。

## Test plan

- [x] `npx tsc --noEmit` clean
- [x] `vitest run` 408/408 files, 6210/6210 tests pass (1 todo
unchanged)
- [x] `pnpm lint` clean
- [x] `pnpm lint:ci` All ci-lint checks passed
- [x] `bash web/scripts/check-cache-governance-disables-shrink-only.sh`
— 5/5 持平
- [ ] Manual staging: publish 流程 draft create/delete 仍 work；
      cross-tab draft 写入仍 surface (A6 主线 PR 再做完整 staging)

Contributes to #2000 (Bucket-4 — uid-keyed RQ migration); B3 decoupling
is the A6 prerequisite. Does NOT close #2000.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

将 `useCustomAgentPublishes.ts` 里混在一起的两类数据拆开:

- (1) 后端 catalog mirror (server response) **留在原 hook**，仍 RQ
      `openclawKeys.agentCatalogPrivate(authToken)` (本 PR **不动**
      token-keyed query key — A6 主线 PR 再迁 uid-keyed)
- (2) 用户本地未提交的 pending publishes (client-only draft) **抽到
      独立 Tier D store**:
  - `web/app/src/lib/custom-agent-publish-draft-store.ts` (~278 LOC) —
    pure data，无 react import
  - `web/app/src/lib/useCustomAgentPublishDrafts.ts` (~34 LOC) —
    `'use client'` `useSyncExternalStore` wrapper

模板取自 `lib/agent-description-store.ts` (#2013 留下的 Tier C/D 模板)，
保持 server-bundle safe 的 file split。

## Why now (#2000 Bucket-4 B3)

这是 A6 (`useCustomAgentPublishes` RQ migration to uid-keyed) 的**前置
条件**：RQ 不能持有"还没存在于 server 的 draft"——`invalidateQueries`
flush 会丢。把 draft 留在 Tier D 客户端 store 保住 A6 的 "RQ caches
reflect server state only" invariant。

参 #2000 issue body Scope 表 A6 行 + "B3 解耦" 段。

## What changed

1. **新 store** (`custom-agent-publish-draft-store.ts`) 提供:
   - `getCustomAgentPublishDrafts(uid)` / `setCustomAgentPublishDrafts(uid, drafts)`
   - `removeCustomAgentPublishDraft(uid, id)` / `clearCustomAgentPublishDrafts(uid)`
   - `subscribeCustomAgentPublishDrafts(listener)` — module-local
     `Set<() => void>` (走任务建议的方案 a，规避 R3 `ecap:*:updated`
     selector + shrink-only count 持平)
   - `refreshCustomAgentPublishDraftsFromStorage(uid)` — cross-tab
     `storage` event 入口，drop snapshot + notify
   - `getCustomAgentPublishDraftsStorageKey(uid)` — 完全照搬原
     `${STORAGE_KEYS.CUSTOM_AGENT_PUBLISHES}:${uid||'anonymous'}` shape
   - 写时格式：flat array of `CustomAgentPublishRecord`（Phase-0 #2049
     spec 锁的契约，不动）

2. **hook 改造** (`useCustomAgentPublishes.ts` 350→252 LOC):
   - 删 `subscribeRecords` / `useDraftRecords` / `draftSnapshotCache` /
     `readRecords` / `writeRecords`
   - 删 `STORAGE_EVENT = 'ecap:custom-agent-publishes:updated'` +
     `dispatchEvent`
   - draft 读改 `useCustomAgentPublishDrafts(uid)`
   - mutation 走 `setCustomAgentPublishDrafts` / 不再自写 localStorage
   - cross-tab `storage` event handler 调用
     `refreshCustomAgentPublishDraftsFromStorage(uid)` + 原 invalidate

3. **测试拆分**:
   - 新文件 `tests/unit/lib/custom-agent-publish-draft-store.unit.spec.ts`
     (~308 LOC) — 直接测 store 函数 + ref-equality snapshot cache +
     subscriber Set + `refreshFromStorage`
   - 原 `useCustomAgentPublishes-storage.unit.spec.tsx`
     (Phase-0 #2049) 保留 hook 公共面契约 (storage key /
     anonymous bucket / flat-array on delete)；ref-equality + custom
     event subscription 那条**整体搬**到 store spec
   - 原 `useCustomAgentPublishes.unit.spec.ts` 唯一改写："same-tab
     `CustomEvent` 不 refetch" → "same-tab store mutation 不 refetch"

## 不做的事 (留给 A6 / 不属于本 PR)

- ❌ 不接 RQ uid-keyed (A6 PR)
- ❌ 不动 `PERSIST_ALLOWLIST_PREFIXES`
- ❌ 不动 useUserAgents / cronHelpers
- ❌ 不 close #2000

## Shrink-only

| Rule | main | HEAD |
| ---- | ---- | ---- |
| Cache governance disables (R2 imports + R3 syntax) | **5** | **5** |

R3 没新增任何 inline disable —— store 用 module-local listener Set 替代
window event dispatch。

## Test plan

- [x] `npx tsc --noEmit` clean
- [x] `vitest run` 408/408 files, 6210/6210 tests pass (1 todo unchanged)
- [x] `pnpm lint` clean
- [x] `pnpm lint:ci` All ci-lint checks passed
- [x] `bash web/scripts/check-cache-governance-disables-shrink-only.sh` — 5/5 持平
- [ ] Manual staging: publish 流程 draft create/delete 仍 work；
      cross-tab draft 写入仍 surface (A6 主线 PR 再做完整 staging)

Contributes to #2000 (Bucket-4 — uid-keyed RQ migration); B3 decoupling
is the A6 prerequisite. Does NOT close #2000.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [1683957] fix(composio): align status response schema (#2057)
- **作者**: tim-srp
- **日期**: 2026-05-28T12:49:08Z
- **PR**: #2057

### Commit Message
```
fix(composio): align status response schema (#2057)

## Summary\n- Align claw-interface Composio status response schema with
ecap-proxy-service enable/disable/delete responses\n- Add deleted as a
valid connector status for disconnect responses\n- Update Composio BFF
proxy tests to cover provider/status/enabled responses\n\n##
Verification\n- python -m pytest
services/claw-interface/tests/unit/test_composio_connectors.py -q\n-
python -m ruff check
services/claw-interface/app/schema/composio_connector.py
services/claw-interface/tests/unit/test_composio_connectors.py
```

### PR Body
## Summary\n- Align claw-interface Composio status response schema with ecap-proxy-service enable/disable/delete responses\n- Add deleted as a valid connector status for disconnect responses\n- Update Composio BFF proxy tests to cover provider/status/enabled responses\n\n## Verification\n- python -m pytest services/claw-interface/tests/unit/test_composio_connectors.py -q\n- python -m ruff check services/claw-interface/app/schema/composio_connector.py services/claw-interface/tests/unit/test_composio_connectors.py

---
## [cf7f0c4] fix(claw-settings): reject malformed Slack tokens (#2026)
- **作者**: sharplee-srp
- **日期**: 2026-05-28T12:35:09Z
- **PR**: #2026

### Commit Message
```
fix(claw-settings): reject malformed Slack tokens (#2026)

## Summary
- Reject Slack channel credentials that include pasted-together tokens
or internal whitespace.
- Trim edge whitespace before writing Slack channel config to FastClaw.
- Add frontend and backend regression coverage for malformed Slack token
submissions.

## Root cause
Slack channel setup previously validated only token prefix and rough
length on the frontend, while the backend forwarded channel config
as-is. A malformed Bot Token containing an internal space could be
persisted, causing Slack auth to fail at runtime even though setup
appeared connected.

## Test plan
- [x] `pnpm --filter @zooclaw/web-app exec vitest run --config
./vitest.config.mts
tests/unit/app/claw-settings/SlackSetupWizard.unit.spec.tsx`
- [x] `uv run --no-project --python 3.12 --with-requirements
requirements.txt --with-requirements requirements-dev.txt pytest
tests/unit/test_openclaw_settings_routes.py -k slack`

Linear: https://linear.app/srpone/issue/ECA-843
```

### PR Body
## Summary
- Reject Slack channel credentials that include pasted-together tokens or internal whitespace.
- Trim edge whitespace before writing Slack channel config to FastClaw.
- Add frontend and backend regression coverage for malformed Slack token submissions.

## Root cause
Slack channel setup previously validated only token prefix and rough length on the frontend, while the backend forwarded channel config as-is. A malformed Bot Token containing an internal space could be persisted, causing Slack auth to fail at runtime even though setup appeared connected.

## Test plan
- [x] `pnpm --filter @zooclaw/web-app exec vitest run --config ./vitest.config.mts tests/unit/app/claw-settings/SlackSetupWizard.unit.spec.tsx`
- [x] `uv run --no-project --python 3.12 --with-requirements requirements.txt --with-requirements requirements-dev.txt pytest tests/unit/test_openclaw_settings_routes.py -k slack`

Linear: https://linear.app/srpone/issue/ECA-843

---
## [348865d] chore(docs): cleanup archive reviews — delete 2 obsolete + rename 1 mislabeled (#2055)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T12:33:50Z
- **PR**: #2055

### Commit Message
```
chore(docs): cleanup archive reviews — delete 2 obsolete + rename 1 mislabeled (#2055)

## Summary

Final pass on the 3 `*-review.md` files that PR #2052 deliberately left
in place ("review-doc bucket policy deferred"). After reading each
end-to-end and comparing against the current code:

**Deleted (2 — actual code reviews whose findings have shipped):**

| File | Lines | Why delete |
|---|---|---|
|
`archive/superpowers/specs/2026-04-03-admin-client-react-best-practices-review.md`
| 86 | 6 React findings on AdminClient → led to
`2026-04-07-admin-react-query-migration-plan.md` (executed). Code-review
docs whose recommendations have been applied are process artifacts; the
actual improvement is in git history. |
| `archive/superpowers/specs/2026-04-03-cronclient-component-review.md`
| 158 | 8 React findings on CronClient → led to
`2026-04-03-cronclient-test-split-plan.md` (executed). Same reasoning. |

Both had one inbound reference each (from the archived plan they
spawned). Per the established principle, archive docs are frozen
snapshots and broken refs from one archive doc to another are acceptable
— same call as the dangling `panda-claw-mockup-lynn-v2.html` ref in PR
#2045.

**Moved + renamed (1 — misnamed as review, actually a design doc):**

| Was | Is now | Why |
|---|---|---|
| `archive/design/payment-subscription-v2-review.md` |
`archive/specs/2026-03-17-payment-subscription-v2-design.md` | 854 lines
of "Payment & Subscription V2 — 综合设计文档" with full system architecture,
subscription state machine, user lifecycle, Stripe Free Trial
integration, module descriptions, test cases. The most architecturally
substantive doc in the entire archive — the `-review` suffix on the
filename was a mislabel. Date taken from inline "日期: 2026-03-17". |

## Conflict note with #2052

PR #2052 is still in merge queue. After both merge, the deferral becomes
moot: 2 reviews deleted, 1 mislabeled design promoted, all three target
dirs (`archive/superpowers/specs/`, `archive/superpowers/`,
`archive/design/`) become empty and disappear from git. No conflicting
file edits between the two PRs.

Empty dirs are not explicitly `rmdir`'d in this PR because main is
currently pre-#2052 and the dirs still contain content #2052 will move
out. Git doesn't track empty dirs so they'll vanish naturally once both
PRs land.

## Result (after this PR + #2052 both merge)

```
docs/archive/
├── plans/    (17 files — execution plans)
├── specs/    (13 files — designs/RFDs, incl. the promoted payment-subscription-v2-design)
├── prds/     (5 files — Product Requirements Docs)
└── *.md      (3 top-level kept per scope: cloudflare-access-legacy, credits-icon-options, style-sync-cui)
```

`archive/superpowers/` and `archive/design/` directories — gone.

## Test plan

- [ ] After both PRs merge: `find docs/archive -type d` shows only
`archive/{plans,specs,prds}` plus the parent.
- [ ] `grep -rn
"admin-client-react-best-practices-review\|cronclient-component-review"`
in live docs (non-archive) returns empty.
- [ ] CI green (doc-only changes).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Final pass on the 3 `*-review.md` files that PR #2052 deliberately left in place ("review-doc bucket policy deferred"). After reading each end-to-end and comparing against the current code:

**Deleted (2 — actual code reviews whose findings have shipped):**

| File | Lines | Why delete |
|---|---|---|
| `archive/superpowers/specs/2026-04-03-admin-client-react-best-practices-review.md` | 86 | 6 React findings on AdminClient → led to `2026-04-07-admin-react-query-migration-plan.md` (executed). Code-review docs whose recommendations have been applied are process artifacts; the actual improvement is in git history. |
| `archive/superpowers/specs/2026-04-03-cronclient-component-review.md` | 158 | 8 React findings on CronClient → led to `2026-04-03-cronclient-test-split-plan.md` (executed). Same reasoning. |

Both had one inbound reference each (from the archived plan they spawned). Per the established principle, archive docs are frozen snapshots and broken refs from one archive doc to another are acceptable — same call as the dangling `panda-claw-mockup-lynn-v2.html` ref in PR #2045.

**Moved + renamed (1 — misnamed as review, actually a design doc):**

| Was | Is now | Why |
|---|---|---|
| `archive/design/payment-subscription-v2-review.md` | `archive/specs/2026-03-17-payment-subscription-v2-design.md` | 854 lines of "Payment & Subscription V2 — 综合设计文档" with full system architecture, subscription state machine, user lifecycle, Stripe Free Trial integration, module descriptions, test cases. The most architecturally substantive doc in the entire archive — the `-review` suffix on the filename was a mislabel. Date taken from inline "日期: 2026-03-17". |

## Conflict note with #2052

PR #2052 is still in merge queue. After both merge, the deferral becomes moot: 2 reviews deleted, 1 mislabeled design promoted, all three target dirs (`archive/superpowers/specs/`, `archive/superpowers/`, `archive/design/`) become empty and disappear from git. No conflicting file edits between the two PRs.

Empty dirs are not explicitly `rmdir`'d in this PR because main is currently pre-#2052 and the dirs still contain content #2052 will move out. Git doesn't track empty dirs so they'll vanish naturally once both PRs land.

## Result (after this PR + #2052 both merge)

```
docs/archive/
├── plans/    (17 files — execution plans)
├── specs/    (13 files — designs/RFDs, incl. the promoted payment-subscription-v2-design)
├── prds/     (5 files — Product Requirements Docs)
└── *.md      (3 top-level kept per scope: cloudflare-access-legacy, credits-icon-options, style-sync-cui)
```

`archive/superpowers/` and `archive/design/` directories — gone.

## Test plan

- [ ] After both PRs merge: `find docs/archive -type d` shows only `archive/{plans,specs,prds}` plus the parent.
- [ ] `grep -rn "admin-client-react-best-practices-review\|cronclient-component-review"` in live docs (non-archive) returns empty.
- [ ] CI green (doc-only changes).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [6b616aa] chore: remove 3 orphan files at repo root (privacy-page.png, terms-page.png, .codex) (#2056)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T12:33:16Z
- **PR**: #2056

### Commit Message
```
chore: remove 3 orphan files at repo root (privacy-page.png, terms-page.png, .codex) (#2056)

## Summary

Three orphan files at the repo root with zero inbound references and no
runtime impact:

| File | Size | Why delete |
|---|---|---|
| `privacy-page.png` | 118 KB | Screenshot dropped at repo root in PR
#197 (2026-03-23). Zero refs in repo (grep across
.md/.ts/.tsx/.py/.html/.css/.json/.yml empty). Not under `web/public/`
so not served. Live `/about/privacy` renders from hardcoded JSX in
`web/app/src/app/about/privacy/page.tsx`, not from any image. |
| `terms-page.png` | 120 KB | Same story, sibling from same PR. |
| `.codex` | 0 bytes | Empty sentinel file from the initial
monorepo-conversion commit `4762f8094 feat: convert to monorepo with
backend service and devcontainer ECA-229`. Never populated; never
referenced. Note: the Codex CLI uses `~/.codex/` (user-global) for
config — the repo-root `.codex` is unrelated despite the name. The grep
hit in `.github/workflows/ios-deploy.yml` is a false positive matching
`.codex-pr-changelog.txt` (a different transient file the workflow
itself creates). |

Same disposition logic as the recent `update_0323.md` / `ZooClaw
onboard.md` cleanups: orphan PM/scratch artifacts from the early 2026-03
phase that nothing uses.

## Test plan

- [ ] `grep -rn "privacy-page\.png\|terms-page\.png\|^\.codex$"` returns
empty.
- [ ] CI green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Three orphan files at the repo root with zero inbound references and no runtime impact:

| File | Size | Why delete |
|---|---|---|
| `privacy-page.png` | 118 KB | Screenshot dropped at repo root in PR #197 (2026-03-23). Zero refs in repo (grep across .md/.ts/.tsx/.py/.html/.css/.json/.yml empty). Not under `web/public/` so not served. Live `/about/privacy` renders from hardcoded JSX in `web/app/src/app/about/privacy/page.tsx`, not from any image. |
| `terms-page.png` | 120 KB | Same story, sibling from same PR. |
| `.codex` | 0 bytes | Empty sentinel file from the initial monorepo-conversion commit `4762f8094 feat: convert to monorepo with backend service and devcontainer ECA-229`. Never populated; never referenced. Note: the Codex CLI uses `~/.codex/` (user-global) for config — the repo-root `.codex` is unrelated despite the name. The grep hit in `.github/workflows/ios-deploy.yml` is a false positive matching `.codex-pr-changelog.txt` (a different transient file the workflow itself creates). |

Same disposition logic as the recent `update_0323.md` / `ZooClaw onboard.md` cleanups: orphan PM/scratch artifacts from the early 2026-03 phase that nothing uses.

## Test plan

- [ ] `grep -rn "privacy-page\.png\|terms-page\.png\|^\.codex$"` returns empty.
- [ ] CI green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [6777cab] fix(public-nav): 官网增加入口跳转到wire Compare ZooClaw link + carry locale/theme to /t… (#1996)
- **作者**: lynn Zhuang
- **日期**: 2026-05-28T12:25:24Z
- **PR**: #1996

### Commit Message
```
fix(public-nav): 官网增加入口跳转到wire Compare ZooClaw link + carry locale/theme to /t… (#1996)

…ips/*

- learnCompare entry had no href; render it as external link to
/tips/compare/
- All 6 /tips/* Learn dropdown items now pass ?lang=&theme= via
buildTipsHref so the sibling zooclaw-tips worker can SSR with the
matching language and color scheme instead of flashing dark-default
before localStorage reconciles
- Add [locale]/not-found.tsx so locale-route 404s inherit the [locale]
layout html/body instead of falling back to the root not-found wrapped
by the passthrough root layout, which triggered "Missing <html> and
<body> tags in the root layout" in local dev

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
…ips/*

- learnCompare entry had no href; render it as external link to /tips/compare/
- All 6 /tips/* Learn dropdown items now pass ?lang=&theme= via buildTipsHref so the sibling zooclaw-tips worker can SSR with the matching language and color scheme instead of flashing dark-default before localStorage reconciles
- Add [locale]/not-found.tsx so locale-route 404s inherit the [locale] layout html/body instead of falling back to the root not-found wrapped by the passthrough root layout, which triggered "Missing <html> and <body> tags in the root layout" in local dev

---
## [bb2ea88] chore(docs): reorganize docs/archive/ by content type (plans / specs / prds) (#2052)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T12:24:24Z
- **PR**: #2052

### Commit Message
```
chore(docs): reorganize docs/archive/ by content type (plans / specs / prds) (#2052)

## Summary

Phase-2 docs audit, archive reorganization. Flatten `docs/archive/` so
each subdirectory holds exactly one content type, with filenames whose
suffix matches that type. Today the sub-buckets do not maintain type
separation (design files sit in plans/, plan files sit in prds/ and
specs/), and an extra `superpowers/` middle layer mirrors the top-level
for no reason.

## Bucket definitions

Anchored on the live `docs/superpowers/{plans,specs}/` taxonomy:

- **`plans/`** — engineering execution plans (Task/Step + `- [ ]`
checkbox format, meant to be replayed by `superpowers:executing-plans`
or a human contributor)
- **`specs/`** — engineering technical docs (design / RFD /
state-machine / API contract — Context + Decisions + Architecture, no
Task/Step structure)
- **`prds/`** — product requirements docs (PM-owned, written in user /
product terms, with acceptance criteria / objectives)

## Result

| Directory | Files | What's there |
|---|---|---|
| `docs/archive/plans/` | 17 | Engineering execution plans (Task/Step
format) |
| `docs/archive/specs/` | 12 | Engineering technical docs (designs /
RFDs / state machines) |
| `docs/archive/prds/` | 5 | Product Requirements Docs (PM-owned) |
| `docs/archive/superpowers/specs/` | 2 | Reserved for the 2
`*-review.md` files (review-doc bucket policy deferred) |
| `docs/archive/design/` | 1 | Holds the 3rd review file
(`payment-subscription-v2-review.md`); same defer reason |
| `docs/archive/` top-level | 3 | Non-bucket misc kept as-is per scope |

## Operations (37 total — see commit message for full file-by-file list)

- 5 renames in place to fix filename-suffix mismatch (incl. ermp
double-file disambiguation: `ermp-plan.md` → `ermp-types-plan.md`,
`ermp-design.md` → `ermp-protocol-plan.md`)
- 6 moves `plans/` → `specs/` (2 with rename — `mattermost-plan` →
`-design`, `ecap-subscription-plan-v2` →
`2026-03-23-subscription-lifecycle-design` with real git creation date
added)
- 1 move `plans/` → `prds/` with `-prd` suffix added
- 2 renames in `prds/` to add `-prd` suffix where files were misnamed
`-plan`
- 6 moves `superpowers/plans/` → `plans/` (flatten middle layer; no
renames)
- 5 moves `superpowers/specs/` → `specs/` (1 rename —
`openclaw-refactor-plan` → `-design` because content is
target-architecture spec, not execution)
- 4 moves `superpowers/specs/` → `plans/` (reclassified
plans-disguised-as-specs; 3 with `-plan` suffix added)
- 1 move `design/` → `specs/`
- 2 deletes: `update_0323.md` (PM scratch, 0 inbound, all 6 listed
changes shipped — see commit) and `comparison-summary.md` (old "ecap vs
dupe" comparison, doesn't fit any bucket, archive-as-noise)
- 4 inbound-link updates in live docs (3 superpowers/specs + 1 test
docstring) for the renamed `stripe-cleanup` / `deptry-rollout` paths

Cross-references **inside archived files** (e.g. a plan referring to its
paired spec) were intentionally NOT updated — archived docs are frozen
snapshots and may legitimately point at where things were when written.
Same principle as the `panda-claw-mockup-lynn-v2.html` ref left dangling
in PR #2045.

## Flags for reviewer

1. **3 review files left in place** (`*-review.md`): 2 in
`archive/superpowers/specs/` + 1 in `archive/design/`. Per separate
decision, review-doc bucket policy is deferred. Both
`archive/superpowers/` and `archive/design/` survive solely to hold
these.
2. **Likely conflicts with #2044 and #2045** (still in queue): both PRs
touch `archive/prds/` and `archive/design/`. After this PR lands, those
will need light rebases. Conflicts are mechanical (renamed targets /
deleted file vs updated file).
3. **`update_0323.md` delete** is safe to merge regardless of #2044 —
#2044's only touch on that file was a relative-link update (to
`archive/prds/2026-03-25-specialists-prd.md`); if #2044 lands first,
this PR's delete supersedes; if this PR lands first, the link update
becomes moot.

## Test plan

- [ ] `grep -rn
"archive/superpowers/plans\|archive/design/2026-03-21\|update_0323\|comparison-summary"`
returns no results in live (non-archive) docs.
- [ ] `tree docs/archive/` confirms 3 buckets + the 2 surviving
review-related dirs.
- [ ] CI green (doc-only changes + 1 test docstring text change).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Phase-2 docs audit, archive reorganization. Flatten `docs/archive/` so each subdirectory holds exactly one content type, with filenames whose suffix matches that type. Today the sub-buckets do not maintain type separation (design files sit in plans/, plan files sit in prds/ and specs/), and an extra `superpowers/` middle layer mirrors the top-level for no reason.

## Bucket definitions

Anchored on the live `docs/superpowers/{plans,specs}/` taxonomy:

- **`plans/`** — engineering execution plans (Task/Step + `- [ ]` checkbox format, meant to be replayed by `superpowers:executing-plans` or a human contributor)
- **`specs/`** — engineering technical docs (design / RFD / state-machine / API contract — Context + Decisions + Architecture, no Task/Step structure)
- **`prds/`** — product requirements docs (PM-owned, written in user / product terms, with acceptance criteria / objectives)

## Result

| Directory | Files | What's there |
|---|---|---|
| `docs/archive/plans/` | 17 | Engineering execution plans (Task/Step format) |
| `docs/archive/specs/` | 12 | Engineering technical docs (designs / RFDs / state machines) |
| `docs/archive/prds/` | 5 | Product Requirements Docs (PM-owned) |
| `docs/archive/superpowers/specs/` | 2 | Reserved for the 2 `*-review.md` files (review-doc bucket policy deferred) |
| `docs/archive/design/` | 1 | Holds the 3rd review file (`payment-subscription-v2-review.md`); same defer reason |
| `docs/archive/` top-level | 3 | Non-bucket misc kept as-is per scope |

## Operations (37 total — see commit message for full file-by-file list)

- 5 renames in place to fix filename-suffix mismatch (incl. ermp double-file disambiguation: `ermp-plan.md` → `ermp-types-plan.md`, `ermp-design.md` → `ermp-protocol-plan.md`)
- 6 moves `plans/` → `specs/` (2 with rename — `mattermost-plan` → `-design`, `ecap-subscription-plan-v2` → `2026-03-23-subscription-lifecycle-design` with real git creation date added)
- 1 move `plans/` → `prds/` with `-prd` suffix added
- 2 renames in `prds/` to add `-prd` suffix where files were misnamed `-plan`
- 6 moves `superpowers/plans/` → `plans/` (flatten middle layer; no renames)
- 5 moves `superpowers/specs/` → `specs/` (1 rename — `openclaw-refactor-plan` → `-design` because content is target-architecture spec, not execution)
- 4 moves `superpowers/specs/` → `plans/` (reclassified plans-disguised-as-specs; 3 with `-plan` suffix added)
- 1 move `design/` → `specs/`
- 2 deletes: `update_0323.md` (PM scratch, 0 inbound, all 6 listed changes shipped — see commit) and `comparison-summary.md` (old "ecap vs dupe" comparison, doesn't fit any bucket, archive-as-noise)
- 4 inbound-link updates in live docs (3 superpowers/specs + 1 test docstring) for the renamed `stripe-cleanup` / `deptry-rollout` paths

Cross-references **inside archived files** (e.g. a plan referring to its paired spec) were intentionally NOT updated — archived docs are frozen snapshots and may legitimately point at where things were when written. Same principle as the `panda-claw-mockup-lynn-v2.html` ref left dangling in PR #2045.

## Flags for reviewer

1. **3 review files left in place** (`*-review.md`): 2 in `archive/superpowers/specs/` + 1 in `archive/design/`. Per separate decision, review-doc bucket policy is deferred. Both `archive/superpowers/` and `archive/design/` survive solely to hold these.
2. **Likely conflicts with #2044 and #2045** (still in queue): both PRs touch `archive/prds/` and `archive/design/`. After this PR lands, those will need light rebases. Conflicts are mechanical (renamed targets / deleted file vs updated file).
3. **`update_0323.md` delete** is safe to merge regardless of #2044 — #2044's only touch on that file was a relative-link update (to `archive/prds/2026-03-25-specialists-prd.md`); if #2044 lands first, this PR's delete supersedes; if this PR lands first, the link update becomes moot.

## Test plan

- [ ] `grep -rn "archive/superpowers/plans\|archive/design/2026-03-21\|update_0323\|comparison-summary"` returns no results in live (non-archive) docs.
- [ ] `tree docs/archive/` confirms 3 buckets + the 2 surviving review-related dirs.
- [ ] CI green (doc-only changes + 1 test docstring text change).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [8da8046] docs: bucket B refresh — 5 docs realigned with current code (audit phase-2) (#2047)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T12:16:13Z
- **PR**: #2047

### Commit Message
```
docs: bucket B refresh — 5 docs realigned with current code (audit phase-2) (#2047)

## Summary

Phase-2 docs audit, bucket B — realign five long-form reference docs
with current code after the `web/app/` nested-workspace restructure and
other architecture moves they had missed. Each commit on this PR handles
one file independently so review can chunk by doc.

All five docs had real unique value (threshold tables / state machines /
API contracts / CI workflow internals) not captured elsewhere —
refresh-not-delete was the right call.

| # | File | Δ | What changed |
|---|---|---|---|
| 1 | `docs/asset-size-guide.md` | +18/-18 | 8-place path drift to
`web/.husky/`/`web/scripts/`/`web/app/public/`; previously missing
`web/enterprise-admin/public/` scan prefix; corrected `cd <repo-root>` →
`cd <repo-root>/web` for `pnpm install` per `web/CLAUDE.md`.
Review-driven follow-up: scoped the "两层防线" claim so the opener and §防线-1
reflect that local pre-commit only fires on `web/app/public/` + iOS
assets (CI still covers all three paths). |
| 2 | `docs/ci-review-and-merge-queue.md` | +29/-13 | PRs #1774 + #1775
consolidated `claude-review.yaml` + `codex-review.yaml` into single
`auto-review.yaml` umbrella, pushed logic into `srp-actions` reusables.
Doc still referenced the deleted files. Updated §1 diagram, §2.1
reviewer table (with `AUTO_REVIEW_*_ENABLED` opt-out vars + per-reviewer
`cc:*` / `gpt:*` label prefixes + `claude_md_paths`), §4.3 (gate
reusable handles merge_group passthrough), §6 troubleshooting row, §7
file index |
| 3 | `docs/backend-api-spec.md` | +24/-20 | All 8 consumer paths
`src/...` → `web/app/src/...`; removed stale
`dashboard/DashboardClient.tsx` reference; rewrote §5 — `POST
/api/subscription/cancel` does not exist as a unified BFF route, the
cancel surface is provider-split (`/api/stripe/cancel-subscription` +
`/api/antom/cancel-subscription`). Review-driven follow-up: corrected
§5's backend mapping — each BFF endpoint proxies to its
**provider-specific** backend route (`/stripe/cancel-subscription` and
`/antom/cancel-subscription`), NOT to a single unified
`/subscription/cancel` endpoint; restored `{ uid }` in the documented
request body (BFF requires it; backend re-resolves authoritative uid
from JWT). |
| 4 | `docs/subscription-status-mapping.md` | +19/-19 | All 12 frontend
file refs `web/src/...` → `web/app/src/...`. Business content (state
machine, \`past_due\` enum, exhaustive field-combination table,
\`getUserDisplayStatus\` logic, \`cancelAtPeriodEnd\` cascade,
per-component copy tables) sanity-checked against current code and
remains accurate |
| 5 | `docs/e2e/README.md` | +6/-6 | All \`web/tests/e2e/...\` →
\`web/app/tests/e2e/...\`; \`web/playwright.config.ts\` →
\`web/app/playwright.config.ts\`; \`cd web && pnpm exec playwright
test\` → \`cd web/app && ...\` (playwright.config.ts lives in
\`web/app/\`, not \`web/\`) |

## Verification

For each doc: grep-verified all referenced file paths exist at their
corrected location; verified all referenced workflows / endpoints /
functions / enums still match the source of truth.

Same audit pass that produced phase-1 deletions (#2017, #2035, #2036,
#2038, #2041, #2042, #2044, #2045) and the design/PRD archive moves.
Bucket B (keep + refresh) is the counterpart to bucket A (delete).

Note: closes prior split PR #2048 (ci-review-and-merge-queue refresh
consolidated here).

## Review-driven fixes

Codex review flagged two factual issues in the first round; both
verified against current code and addressed in commits `00a7e578`
(`asset-size-guide`) and `825b8706` (`backend-api-spec`):

- **`asset-size-guide.md` opener overstated local pre-commit coverage**
— `web/.husky/pre-commit:14` only greps for `web/app/public/|ios/...`,
so `web/enterprise-admin/public/` is CI-only (1 layer), not "两层". Split
the coverage statement in both the opener and §防线-1 so readers see the
asymmetry inline.
- **`backend-api-spec.md` §5 mis-mapped the BFF cancel surface to a
unified backend route** — actual code
(`web/app/src/app/api/{stripe,antom}/cancel-subscription/route.ts`)
proxies to `POST /stripe/cancel-subscription` and `POST
/antom/cancel-subscription` respectively, not to `POST
/subscription/cancel`; both BFF routes also require `{ uid }` in the
request body. Replaced the unified-backend claim with the real BFF →
backend mapping table and corrected the request-body schema, while
keeping a note that the unrelated `/subscription/cancel` backend route
exists at `subscription.py:108` so future readers don't reproduce the
same confusion.

## Test plan

- [ ] Re-read each doc and confirm commands / paths a reader would
follow actually resolve today.
- [ ] CI green (doc-only changes).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Phase-2 docs audit, bucket B — realign five long-form reference docs with current code after the `web/app/` nested-workspace restructure and other architecture moves they had missed. Each commit on this PR handles one file independently so review can chunk by doc.

All five docs had real unique value (threshold tables / state machines / API contracts / CI workflow internals) not captured elsewhere — refresh-not-delete was the right call.

| # | File | Δ | What changed |
|---|---|---|---|
| 1 | `docs/asset-size-guide.md` | +18/-18 | 8-place path drift to `web/.husky/`/`web/scripts/`/`web/app/public/`; previously missing `web/enterprise-admin/public/` scan prefix; corrected `cd <repo-root>` → `cd <repo-root>/web` for `pnpm install` per `web/CLAUDE.md`. Review-driven follow-up: scoped the "两层防线" claim so the opener and §防线-1 reflect that local pre-commit only fires on `web/app/public/` + iOS assets (CI still covers all three paths). |
| 2 | `docs/ci-review-and-merge-queue.md` | +29/-13 | PRs #1774 + #1775 consolidated `claude-review.yaml` + `codex-review.yaml` into single `auto-review.yaml` umbrella, pushed logic into `srp-actions` reusables. Doc still referenced the deleted files. Updated §1 diagram, §2.1 reviewer table (with `AUTO_REVIEW_*_ENABLED` opt-out vars + per-reviewer `cc:*` / `gpt:*` label prefixes + `claude_md_paths`), §4.3 (gate reusable handles merge_group passthrough), §6 troubleshooting row, §7 file index |
| 3 | `docs/backend-api-spec.md` | +24/-20 | All 8 consumer paths `src/...` → `web/app/src/...`; removed stale `dashboard/DashboardClient.tsx` reference; rewrote §5 — `POST /api/subscription/cancel` does not exist as a unified BFF route, the cancel surface is provider-split (`/api/stripe/cancel-subscription` + `/api/antom/cancel-subscription`). Review-driven follow-up: corrected §5's backend mapping — each BFF endpoint proxies to its **provider-specific** backend route (`/stripe/cancel-subscription` and `/antom/cancel-subscription`), NOT to a single unified `/subscription/cancel` endpoint; restored `{ uid }` in the documented request body (BFF requires it; backend re-resolves authoritative uid from JWT). |
| 4 | `docs/subscription-status-mapping.md` | +19/-19 | All 12 frontend file refs `web/src/...` → `web/app/src/...`. Business content (state machine, \`past_due\` enum, exhaustive field-combination table, \`getUserDisplayStatus\` logic, \`cancelAtPeriodEnd\` cascade, per-component copy tables) sanity-checked against current code and remains accurate |
| 5 | `docs/e2e/README.md` | +6/-6 | All \`web/tests/e2e/...\` → \`web/app/tests/e2e/...\`; \`web/playwright.config.ts\` → \`web/app/playwright.config.ts\`; \`cd web && pnpm exec playwright test\` → \`cd web/app && ...\` (playwright.config.ts lives in \`web/app/\`, not \`web/\`) |

## Verification

For each doc: grep-verified all referenced file paths exist at their corrected location; verified all referenced workflows / endpoints / functions / enums still match the source of truth.

Same audit pass that produced phase-1 deletions (#2017, #2035, #2036, #2038, #2041, #2042, #2044, #2045) and the design/PRD archive moves. Bucket B (keep + refresh) is the counterpart to bucket A (delete).

Note: closes prior split PR #2048 (ci-review-and-merge-queue refresh consolidated here).

## Review-driven fixes

Codex review flagged two factual issues in the first round; both verified against current code and addressed in commits `00a7e578` (`asset-size-guide`) and `825b8706` (`backend-api-spec`):

- **`asset-size-guide.md` opener overstated local pre-commit coverage** — `web/.husky/pre-commit:14` only greps for `web/app/public/|ios/...`, so `web/enterprise-admin/public/` is CI-only (1 layer), not "两层". Split the coverage statement in both the opener and §防线-1 so readers see the asymmetry inline.
- **`backend-api-spec.md` §5 mis-mapped the BFF cancel surface to a unified backend route** — actual code (`web/app/src/app/api/{stripe,antom}/cancel-subscription/route.ts`) proxies to `POST /stripe/cancel-subscription` and `POST /antom/cancel-subscription` respectively, not to `POST /subscription/cancel`; both BFF routes also require `{ uid }` in the request body. Replaced the unified-backend claim with the real BFF → backend mapping table and corrected the request-body schema, while keeping a note that the unrelated `/subscription/cancel` backend route exists at `subscription.py:108` so future readers don't reproduce the same confusion.

## Test plan

- [ ] Re-read each doc and confirm commands / paths a reader would follow actually resolve today.
- [ ] CI green (doc-only changes).

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
## [654f581] test(web): characterize useCustomAgentPublishes + cronHelpers storage (#2000 Phase-0) (#2049)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T11:55:13Z
- **PR**: #2049

### Commit Message
```
test(web): characterize useCustomAgentPublishes + cronHelpers storage (#2000 Phase-0) (#2049)

## Summary

Phase-0 characterization tests for **#2000 Bucket-4** (migrate
token-keyed agent / cron caches to uid-keyed RQ). **Zero production
changes** — only pins the A6 + A7 storage boundary contracts so the
upcoming A5/A6/A7/B3 main-line PRs catch silent regressions on the parts
the existing suites do not cover.

Decision: A5 has 400+ LOC of spec already; the seq-stamp gap will be
addressed in the A5 main-line PR itself. This Phase-0 PR is A6 + A7
only.

## Scope

| File | LOC (raw / non-comment) | What it pins |
|---|---|---|
|
`web/app/tests/unit/hooks/useCustomAgentPublishes-storage.unit.spec.tsx`
| 198 / 95 | Storage key composed from
`STORAGE_KEYS.CUSTOM_AGENT_PUBLISHES`; `uid || 'anonymous'` fallback
bucket; delete-path write is a flat JSON array (not envelope);
`draftSnapshotCache` ref-equality contract |
| `web/app/tests/unit/app/schedule/cronHelpers-storage.unit.spec.ts` |
195 / 100 | `saveCachedJobs` writes under
`STORAGE_KEYS.CRON_JOBS_CACHE`; payload is a flat JSON array of CronJob;
merge precedence `live overrides existing`; `removeCachedJob` preserves
array shape on empty; `setItem`-throws swallowed by `saveCachedJobs` and
`removeCachedJob` (sibling spec only covered `loadCachedJobs` corrupt
JSON path) |

Each expected key is sourced from the production `STORAGE_KEYS` constant
rather than duplicated as a string literal (so a producer-side rename
red-flags the assertion). Each assertion is falsifiable against the
production module — deleting the named line in
`src/hooks/useCustomAgentPublishes.ts` or
`src/app/[locale]/schedule/cronHelpers.ts` flips the assertion red.

Test count: **+10** (4 new + 6 new). Total `web/app` vitest now 6187
passed (was 6177) | 1 todo.

## What this PR does NOT do

- No production code changes (zero touches to `src/`).
- No new RQ hooks — those land in A5/A6/A7 main-line PRs.
- No changes to `PERSIST_ALLOWLIST_PREFIXES`.
- No changes to `useUserAgents.ts` (A5 territory).
- No changes to `ecap:agents:updated` paths (A5 main-line will delete
those).
- No cronHelpers algorithm refactor.

## Bugs discovered

None during this characterization pass.

## Test plan

- [x] `npx tsc --noEmit` — clean
- [x] `vitest run` — 407 files, 6187 passed | 1 todo (zero regressions
vs. baseline 6177)
- [x] `pnpm lint` — clean
- [x] `cd app && pnpm lint:ci` (dep-cruise + knip) — clean
- [x] `bash web/scripts/check-cache-governance-disables-shrink-only.sh`
— main 5, HEAD 5 (no increase)

## Reference

- Umbrella: #2000 (Bucket-4 — agent / cron caches → uid-keyed RQ)
- Upstream landed: #1990 (Bucket-1), #1998 (Bucket-2), #1999 (Bucket-3),
#2025 (R1/R2/R3 ESLint), #2043 (per-prefix TTL), #2046 (session-cache
deletion)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Phase-0 characterization tests for **#2000 Bucket-4** (migrate token-keyed agent / cron caches to uid-keyed RQ). **Zero production changes** — only pins the A6 + A7 storage boundary contracts so the upcoming A5/A6/A7/B3 main-line PRs catch silent regressions on the parts the existing suites do not cover.

Decision: A5 has 400+ LOC of spec already; the seq-stamp gap will be addressed in the A5 main-line PR itself. This Phase-0 PR is A6 + A7 only.

## Scope

| File | LOC (raw / non-comment) | What it pins |
|---|---|---|
| `web/app/tests/unit/hooks/useCustomAgentPublishes-storage.unit.spec.tsx` | 198 / 95 | Storage key composed from `STORAGE_KEYS.CUSTOM_AGENT_PUBLISHES`; `uid || 'anonymous'` fallback bucket; delete-path write is a flat JSON array (not envelope); `draftSnapshotCache` ref-equality contract |
| `web/app/tests/unit/app/schedule/cronHelpers-storage.unit.spec.ts` | 195 / 100 | `saveCachedJobs` writes under `STORAGE_KEYS.CRON_JOBS_CACHE`; payload is a flat JSON array of CronJob; merge precedence `live overrides existing`; `removeCachedJob` preserves array shape on empty; `setItem`-throws swallowed by `saveCachedJobs` and `removeCachedJob` (sibling spec only covered `loadCachedJobs` corrupt JSON path) |

Each expected key is sourced from the production `STORAGE_KEYS` constant rather than duplicated as a string literal (so a producer-side rename red-flags the assertion). Each assertion is falsifiable against the production module — deleting the named line in `src/hooks/useCustomAgentPublishes.ts` or `src/app/[locale]/schedule/cronHelpers.ts` flips the assertion red.

Test count: **+10** (4 new + 6 new). Total `web/app` vitest now 6187 passed (was 6177) | 1 todo.

## What this PR does NOT do

- No production code changes (zero touches to `src/`).
- No new RQ hooks — those land in A5/A6/A7 main-line PRs.
- No changes to `PERSIST_ALLOWLIST_PREFIXES`.
- No changes to `useUserAgents.ts` (A5 territory).
- No changes to `ecap:agents:updated` paths (A5 main-line will delete those).
- No cronHelpers algorithm refactor.

## Bugs discovered

None during this characterization pass.

## Test plan

- [x] `npx tsc --noEmit` — clean
- [x] `vitest run` — 407 files, 6187 passed | 1 todo (zero regressions vs. baseline 6177)
- [x] `pnpm lint` — clean
- [x] `cd app && pnpm lint:ci` (dep-cruise + knip) — clean
- [x] `bash web/scripts/check-cache-governance-disables-shrink-only.sh` — main 5, HEAD 5 (no increase)

## Reference

- Umbrella: #2000 (Bucket-4 — agent / cron caches → uid-keyed RQ)
- Upstream landed: #1990 (Bucket-1), #1998 (Bucket-2), #1999 (Bucket-3), #2025 (R1/R2/R3 ESLint), #2043 (per-prefix TTL), #2046 (session-cache deletion)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [afe597e] fix(canvas): reset versionRef on session change too (#2051)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T11:52:35Z
- **PR**: #2051

### Commit Message
```
fix(canvas): reset versionRef on session change too (#2051)

## Summary

Symmetric reset fix for the `useCanvasPersistence` hook (caught by
Claude review on the closed #2029, but the bug also exists on current
main — the out-of-order load guard that landed via a different PR didn't
touch the version-counter path).

### The bug

`clearCanvas` (same-session "start over") explicitly calls
`resetVersion()` to zero the autosave version counter. The
session-change reset effect did not. So on session A (`versionRef = N`)
→ session B with no saved canvas:

1. Reset effect fires → clears nodes/edges + `onReset()`, but **does
not** call `resetVersion()`
2. Load effect fires → `loadCanvasState(B)` returns `success: false`, so
the success branch with `setVersion()` never runs
3. `versionRef.current` stays at `N`
4. The first autosave to session B sends `version: N+1` instead of `1` →
the backend rejects with a version mismatch (or silently accepts a
phantom history)

### The fix

Add `resetVersion()` to the reset effect body and `resetVersion` to its
dep array, symmetric with the `clearCanvas` path. When session B DOES
have a saved canvas, the load-effect's `setVersion(data.version)` fires
right after and overwrites the just-zeroed version with the correct
loaded value — so the fix is harmless in that case.

### Regression test

`session change resets versionRef even when the new session has no saved
canvas` — pinned with an explicit
`expect(setVersion).not.toHaveBeenCalled()` so the test isn't
tautological (if both setVersion and resetVersion zeroed the ref, the
omission wouldn't bite either way).

Existing test `clearCanvas empties nodes/edges, calls resetVersion and
onReset` needed `mocks.resetVersion.mockClear()` added — the reset
effect now also fires resetVersion on mount (sessionId undefined →
'sess-1'), so the post-clearCanvas count would be 2 without the clear.
Inline comment explains.

## Test plan

- [x] `pnpm vitest run
tests/unit/canvas-hooks/useCanvasPersistence.unit.spec.ts` — 13/13 pass
(was 12; +1 regression test, 1 existing test amended)
- [x] `pnpm tsc --noEmit` clean
- [x] `pnpm lint` clean (pre-commit verified)
- [ ] CI green

## Context

Originally addressed on #2029 (closed before this commit was reviewed).
This is the same fix on a fresh branch off current main, since main's
`useCanvasPersistence.ts` (which got the out-of-order load guard via a
different PR) still has the resetVersion-on-session-change omission.

Refs #368 F13.
```

### PR Body
## Summary

Symmetric reset fix for the `useCanvasPersistence` hook (caught by Claude review on the closed #2029, but the bug also exists on current main — the out-of-order load guard that landed via a different PR didn't touch the version-counter path).

### The bug

`clearCanvas` (same-session "start over") explicitly calls `resetVersion()` to zero the autosave version counter. The session-change reset effect did not. So on session A (`versionRef = N`) → session B with no saved canvas:

1. Reset effect fires → clears nodes/edges + `onReset()`, but **does not** call `resetVersion()`
2. Load effect fires → `loadCanvasState(B)` returns `success: false`, so the success branch with `setVersion()` never runs
3. `versionRef.current` stays at `N`
4. The first autosave to session B sends `version: N+1` instead of `1` → the backend rejects with a version mismatch (or silently accepts a phantom history)

### The fix

Add `resetVersion()` to the reset effect body and `resetVersion` to its dep array, symmetric with the `clearCanvas` path. When session B DOES have a saved canvas, the load-effect's `setVersion(data.version)` fires right after and overwrites the just-zeroed version with the correct loaded value — so the fix is harmless in that case.

### Regression test

`session change resets versionRef even when the new session has no saved canvas` — pinned with an explicit `expect(setVersion).not.toHaveBeenCalled()` so the test isn't tautological (if both setVersion and resetVersion zeroed the ref, the omission wouldn't bite either way).

Existing test `clearCanvas empties nodes/edges, calls resetVersion and onReset` needed `mocks.resetVersion.mockClear()` added — the reset effect now also fires resetVersion on mount (sessionId undefined → 'sess-1'), so the post-clearCanvas count would be 2 without the clear. Inline comment explains.

## Test plan

- [x] `pnpm vitest run tests/unit/canvas-hooks/useCanvasPersistence.unit.spec.ts` — 13/13 pass (was 12; +1 regression test, 1 existing test amended)
- [x] `pnpm tsc --noEmit` clean
- [x] `pnpm lint` clean (pre-commit verified)
- [ ] CI green

## Context

Originally addressed on #2029 (closed before this commit was reviewed). This is the same fix on a fresh branch off current main, since main's `useCanvasPersistence.ts` (which got the out-of-order load guard via a different PR) still has the resetVersion-on-session-change omission.

Refs #368 F13.

---
## [06ccff3] chore(docs): archive Google Workspace design doc, delete 7 HTML mockups (docs/design/) (#2045)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T10:35:42Z
- **PR**: #2045

### Commit Message
```
chore(docs): archive Google Workspace design doc, delete 7 HTML mockups (docs/design/) (#2045)

## Summary

`docs/design/` had one architecture markdown plus seven static HTML
mockups left over from the PandaClaw rebrand exploration.

### Archived (1)

- `google-workspace-pod-injection.md` →
`docs/archive/design/2026-03-21-google-workspace-pod-injection-design.md`.
The gog-CLI-into-Pod injection architecture it describes **is still in
production** (`services/claw-interface/app/connectors/google.py` + 16+
`feat/fix(connectors): gog ...` commits). But the doc has drifted from
runtime in three ways:
  1. Calls the product "PandaClaw" (pre-Zooclaw branding).
2. Specifies a `POST /internal/bots/{bot_id}/connectors/google` endpoint
that was never shipped — actual paths are `/connectors/google/callback`
(claw-interface + `services/oauth-worker/` Cloudflare Worker) and
`/api/composio-connectors/google-mail/*` (BFF wrapper).
3. Misses the Nango attempt + revert (PR #1294 → #1441) that restored
gog as the current production approach.

Archived to preserve the design rationale (why Pod filesystem injection
beats runtime API call); current implementation is the runtime source of
truth. Dated to real git first commit 2026-03-21 (PR #138).

### Deleted (7)

`index-v2.html`, `panda-claw-mobile-v2.html`,
`panda-claw-mobile-v3.html`, `panda-claw-mockup-lynn-v2.html`,
`panda-claw-mockup-lynn-v3.html`, `pricing-v2.html`,
`sidebar-scroll-fix-preview.html` — static HTML mockups from the
PandaClaw rebrand exploration. Visual artifacts belong in Figma, not in
docs/. Same disposition as the previously deleted `openclaw-flow.html` /
`architecture.html` in PR #2041.

### Acceptable broken-link note

`docs/archive/plans/2026-03-12-panda-claw-ui-overhaul-{design,plan}.md`
reference `panda-claw-mockup-lynn-v2.html` as a "Reference Mockup".
These two files are themselves archived snapshots — historical records
of the plan at that point in time. Like a published paper referencing a
now-offline URL, broken references in archived docs are acceptable; the
file is recoverable via git history if ever needed.

Empty `docs/design/` directory removed.

## Test plan

- [ ] `grep -rn "docs/design"` returns only the two acceptable archive
references noted above.
- [ ] CI green (doc-only changes).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

`docs/design/` had one architecture markdown plus seven static HTML mockups left over from the PandaClaw rebrand exploration.

### Archived (1)

- `google-workspace-pod-injection.md` → `docs/archive/design/2026-03-21-google-workspace-pod-injection-design.md`. The gog-CLI-into-Pod injection architecture it describes **is still in production** (`services/claw-interface/app/connectors/google.py` + 16+ `feat/fix(connectors): gog ...` commits). But the doc has drifted from runtime in three ways:
  1. Calls the product "PandaClaw" (pre-Zooclaw branding).
  2. Specifies a `POST /internal/bots/{bot_id}/connectors/google` endpoint that was never shipped — actual paths are `/connectors/google/callback` (claw-interface + `services/oauth-worker/` Cloudflare Worker) and `/api/composio-connectors/google-mail/*` (BFF wrapper).
  3. Misses the Nango attempt + revert (PR #1294 → #1441) that restored gog as the current production approach.

  Archived to preserve the design rationale (why Pod filesystem injection beats runtime API call); current implementation is the runtime source of truth. Dated to real git first commit 2026-03-21 (PR #138).

### Deleted (7)

`index-v2.html`, `panda-claw-mobile-v2.html`, `panda-claw-mobile-v3.html`, `panda-claw-mockup-lynn-v2.html`, `panda-claw-mockup-lynn-v3.html`, `pricing-v2.html`, `sidebar-scroll-fix-preview.html` — static HTML mockups from the PandaClaw rebrand exploration. Visual artifacts belong in Figma, not in docs/. Same disposition as the previously deleted `openclaw-flow.html` / `architecture.html` in PR #2041.

### Acceptable broken-link note

`docs/archive/plans/2026-03-12-panda-claw-ui-overhaul-{design,plan}.md` reference `panda-claw-mockup-lynn-v2.html` as a "Reference Mockup". These two files are themselves archived snapshots — historical records of the plan at that point in time. Like a published paper referencing a now-offline URL, broken references in archived docs are acceptable; the file is recoverable via git history if ever needed.

Empty `docs/design/` directory removed.

## Test plan

- [ ] `grep -rn "docs/design"` returns only the two acceptable archive references noted above.
- [ ] CI green (doc-only changes).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [629bc86] refactor(web): delete orphaned session-cache.ts (#1999 Bucket-3 PR-D) (#2046)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T10:30:43Z
- **PR**: #2046

### Commit Message
```
refactor(web): delete orphaned session-cache.ts (#1999 Bucket-3 PR-D) (#2046)

## Summary

PR-B (#2039) and PR-C (#2037) both migrated their consumers off the
hand-maintained sessionStorage TTL wrapper in
\`lib/storage/session-cache.ts\` onto React Query +
\`PersistQueryClientProvider\`. With those landed, the helper module has
**zero remaining production callers** — confirmed by:

\`\`\`
$ grep -rn "from '@/lib/storage/session-cache'" web/app/src/
(no matches)
\`\`\`

This PR-D capstone deletes both the source module and its Phase-0
characterization spec.

## Changes

- **Deleted**: \`web/app/src/lib/storage/session-cache.ts\` (-103 LOC)
- **Deleted**:
\`web/app/tests/unit/lib/storage/session-cache.unit.spec.ts\` (-159 LOC)

The Phase-0 characterization tests retire with the module they were
locking — same shape as #1990 retiring
\`agent-catalog-cache.unit.spec.ts\` once that helper was gone.

## Test plan

- [x] \`pnpm lint\` clean
- [x] \`npx tsc --noEmit\` clean
- [x] \`./node_modules/.bin/vitest run\` — 405 files / 6176 tests / 1
todo (was 406 / 6193; one Phase-0 spec deleted as expected, the rest
carry on)
- [x] \`pnpm lint:ci\` clean (knip + dep-cruise)

## Closes

Closes #1999 — wraps up the Bucket-3 4-PR series:
- Phase-0 (#2032) — characterization tests
- PR-B (#2039) — \`skills-store.ts\` → RQ
- PR-C (#2037) — \`community-client.ts\` → RQ
- PR-D (this) — delete \`session-cache.ts\`
- Codex follow-up (#2043) — tighten runtime-skills persist TTL to 5min

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Body
## Summary

PR-B (#2039) and PR-C (#2037) both migrated their consumers off the hand-maintained sessionStorage TTL wrapper in \`lib/storage/session-cache.ts\` onto React Query + \`PersistQueryClientProvider\`. With those landed, the helper module has **zero remaining production callers** — confirmed by:

\`\`\`
$ grep -rn "from '@/lib/storage/session-cache'" web/app/src/
(no matches)
\`\`\`

This PR-D capstone deletes both the source module and its Phase-0 characterization spec.

## Changes

- **Deleted**: \`web/app/src/lib/storage/session-cache.ts\` (-103 LOC)
- **Deleted**: \`web/app/tests/unit/lib/storage/session-cache.unit.spec.ts\` (-159 LOC)

The Phase-0 characterization tests retire with the module they were locking — same shape as #1990 retiring \`agent-catalog-cache.unit.spec.ts\` once that helper was gone.

## Test plan

- [x] \`pnpm lint\` clean
- [x] \`npx tsc --noEmit\` clean
- [x] \`./node_modules/.bin/vitest run\` — 405 files / 6176 tests / 1 todo (was 406 / 6193; one Phase-0 spec deleted as expected, the rest carry on)
- [x] \`pnpm lint:ci\` clean (knip + dep-cruise)

## Closes

Closes #1999 — wraps up the Bucket-3 4-PR series:
- Phase-0 (#2032) — characterization tests
- PR-B (#2039) — \`skills-store.ts\` → RQ
- PR-C (#2037) — \`community-client.ts\` → RQ
- PR-D (this) — delete \`session-cache.ts\`
- Codex follow-up (#2043) — tighten runtime-skills persist TTL to 5min

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [9841b18] fix(web): neutral avatar placeholder for user messages in share replay (#1995)
- **作者**: rayrain-srp
- **日期**: 2026-05-28T10:28:24Z
- **PR**: #1995

### Commit Message
```
fix(web): neutral avatar placeholder for user messages in share replay (#1995)

## Summary
- Share replay 复用了 live chat 的 `OpenClawUserMessage`，其中 `UserAvatar()`
直接读 `auth.currentUser?.photoURL` + localStorage 用户信息——live chat 下 viewer
== sender 刚好成立，share replay 下穿帮：登录态 viewer 看到的是**自己的**头像，未登录 viewer 看到的是
'U' 字母（碰巧像默认占位）。
- 通过 `useIsReplayReadOnly()` 检测 replay 模式，replay 下渲染 Heroicons
`UserIcon` 中性占位，不再读 viewer 身份。Live chat 路径完全不变。

## Root cause

[`web/app/src/app/[locale]/chat/components/OpenClawUserMessage.tsx`](web/app/src/app/[locale]/chat/components/OpenClawUserMessage.tsx)
中 `UserAvatar` 组件无 props，无差别从全局 Firebase auth + localStorage
取头像/邮箱首字母。Share replay 路径
([`web/app/src/app/share/[shareId]/ReplayPlayer.tsx`](web/app/src/app/share/[shareId]/ReplayPlayer.tsx))
复用 `OpenClawThread` → `OpenClawUserMessage`，于是 viewer 身份被错套到原始分享者头像位。

**配套缺口（不在本 PR 范围）**：后端 `ReplayMessage` schema
([`services/claw-interface/app/schema/chat_replay.py`](services/claw-interface/app/schema/chat_replay.py))
只有 `role: Literal["user", "assistant"]`，没有 user 侧的 `user_id` /
`avatar_url` 字段——bot 侧对称的 `ReplayBot.avatar_url` 是有的。完整修复（捕获
`creator_avatar_url` 进 snapshot、像 `botAvatar` 一样透传）跟踪在 ECA-849 Option
B，待后续 spec。

Linear:
https://linear.app/srpone/issue/ECA-849/share-replay-链路登录态下用户头像渲染为-viewer-自己的而非分享者

## Test plan
- [x] 新增单测 `UserAvatar shows neutral placeholder in replay mode and
ignores viewer identity`：mock `useIsReplayReadOnly` 返 true + viewer
email 设为 `viewer@example.com`，断言 'V' 首字母不出现、svg 占位渲染
- [x] 已有 11 个 `OpenClawUserMessage` 单测在 mock 默认 `useIsReplayReadOnly =
false` 下继续通过（live chat 路径无回归）
- [ ] 手测：用 `https://zooclaw.ai/share/cr_GPmzKJGjgqE7C-q38IH1Sw`
在登录态/未登录态/分享者本人三种状态打开，确认 replay 模式下 user-role 消息的头像统一显示中性占位、不跟随 viewer
切换；live chat 仍显示 viewer 自己的 photoURL

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary
- Share replay 复用了 live chat 的 `OpenClawUserMessage`，其中 `UserAvatar()` 直接读 `auth.currentUser?.photoURL` + localStorage 用户信息——live chat 下 viewer == sender 刚好成立，share replay 下穿帮：登录态 viewer 看到的是**自己的**头像，未登录 viewer 看到的是 'U' 字母（碰巧像默认占位）。
- 通过 `useIsReplayReadOnly()` 检测 replay 模式，replay 下渲染 Heroicons `UserIcon` 中性占位，不再读 viewer 身份。Live chat 路径完全不变。

## Root cause
[`web/app/src/app/[locale]/chat/components/OpenClawUserMessage.tsx`](web/app/src/app/[locale]/chat/components/OpenClawUserMessage.tsx) 中 `UserAvatar` 组件无 props，无差别从全局 Firebase auth + localStorage 取头像/邮箱首字母。Share replay 路径 ([`web/app/src/app/share/[shareId]/ReplayPlayer.tsx`](web/app/src/app/share/[shareId]/ReplayPlayer.tsx)) 复用 `OpenClawThread` → `OpenClawUserMessage`，于是 viewer 身份被错套到原始分享者头像位。

**配套缺口（不在本 PR 范围）**：后端 `ReplayMessage` schema ([`services/claw-interface/app/schema/chat_replay.py`](services/claw-interface/app/schema/chat_replay.py)) 只有 `role: Literal["user", "assistant"]`，没有 user 侧的 `user_id` / `avatar_url` 字段——bot 侧对称的 `ReplayBot.avatar_url` 是有的。完整修复（捕获 `creator_avatar_url` 进 snapshot、像 `botAvatar` 一样透传）跟踪在 ECA-849 Option B，待后续 spec。

Linear: https://linear.app/srpone/issue/ECA-849/share-replay-链路登录态下用户头像渲染为-viewer-自己的而非分享者

## Test plan
- [x] 新增单测 `UserAvatar shows neutral placeholder in replay mode and ignores viewer identity`：mock `useIsReplayReadOnly` 返 true + viewer email 设为 `viewer@example.com`，断言 'V' 首字母不出现、svg 占位渲染
- [x] 已有 11 个 `OpenClawUserMessage` 单测在 mock 默认 `useIsReplayReadOnly = false` 下继续通过（live chat 路径无回归）
- [ ] 手测：用 `https://zooclaw.ai/share/cr_GPmzKJGjgqE7C-q38IH1Sw` 在登录态/未登录态/分享者本人三种状态打开，确认 replay 模式下 user-role 消息的头像统一显示中性占位、不跟随 viewer 切换；live chat 仍显示 viewer 自己的 photoURL

---
## [de1cb42] fix(web): tighten runtime-skills persist TTL to 5min (Codex #2039 follow-up) (#2043)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T10:22:12Z
- **PR**: #2043

### Commit Message
```
fix(web): tighten runtime-skills persist TTL to 5min (Codex #2039 follow-up) (#2043)

## Summary

Follow-up to **#2039** (Bucket-3 PR-B, merged) — addresses Codex round-1
review's `NEED_HUMAN_REVIEW` finding that moving runtime-skills onto the
persister silently extended the cache-expiry contract from the pre-#1999
5-minute TTL to the global 24h \`maxAge\`. Without this fix, a cold open
after a long absence would paint stale install badges briefly before
\`refetchOnMount: 'always'\` lands.

Restores the original 5-min TTL contract on top of RQ + persister via a
per-prefix max-age cap enforced **bidirectionally** (save-side +
hydrate-side).

## Changes

### `lib/query/persist-client.ts`
- New `PER_PREFIX_MAX_AGE_MS` map (file-local) seeded with
`RUNTIME_SKILLS_QUERY_KEY_PREFIX → 5 * 60 * 1000`.
- `shouldDehydrateQuery` refuses to dehydrate any entry whose
`dataUpdatedAt` is already past its family's per-prefix cap → a tab
idled past 5min before close persists nothing for that bucket.
- New exported `evictPerPrefixStaleEntries(client)` walks the cache and
`removeQueries` for entries past their cap → a tab that persisted while
fresh then reopens hours later drops the bucket on hydrate.
- `syncRestoreCache` invokes the scrub after hydrate.

### `components/ClientLayout.tsx`
- `PersistQueryClientProvider.onSuccess` calls
`evictPerPrefixStaleEntries(queryClient)` so the provider's effect-based
hydrate is symmetric with the imperative sync prefill.

### `hooks/queries/skills/useRuntimeSkills.ts`
- Docstring rewritten to call out the two-tier guard (`staleTime` +
per-prefix max-age) on the reading path — the design contract lives next
to the code, not just the PR body.

### Tests (+6 cases, +106 LOC)
- `shouldDehydrateQuery`: stale runtime-skills rejected (>5min), fresh
preserved (<5min), other allowed families unaffected at 1h.
- `evictPerPrefixStaleEntries`: stale runtime evicted, fresh preserved,
other allowed families untouched even when backdated 1h.
- `syncRestoreCache`: stale runtime payload (>5min) gone from client
after restore.

## Test plan

- [x] `pnpm lint` clean
- [x] `npx tsc --noEmit` clean
- [x] `./node_modules/.bin/vitest run
tests/unit/lib/query/persist-client.unit.spec.ts` — 39 passed (was 33,
+6 new)
- [x] `pnpm lint:ci` clean (knip would flag if I left dead exports; only
`evictPerPrefixStaleEntries` is module-public)

## UX semantics

| Scenario | Pre-RQ | PR #2039 (before this) | This PR |
|---|---|---|---|
| Same-tab nav within 5min | cache hit, no fetch | cache hit, no fetch |
cache hit, no fetch |
| Reopen tab after 2h | spinner → fetch | flash of stale data → fetch |
spinner → fetch (matches pre-RQ) |
| Same-tab mutation | cache invalidated | RQ invalidated | RQ
invalidated (unchanged) |

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Body
## Summary

Follow-up to **#2039** (Bucket-3 PR-B, merged) — addresses Codex round-1 review's `NEED_HUMAN_REVIEW` finding that moving runtime-skills onto the persister silently extended the cache-expiry contract from the pre-#1999 5-minute TTL to the global 24h \`maxAge\`. Without this fix, a cold open after a long absence would paint stale install badges briefly before \`refetchOnMount: 'always'\` lands.

Restores the original 5-min TTL contract on top of RQ + persister via a per-prefix max-age cap enforced **bidirectionally** (save-side + hydrate-side).

## Changes

### `lib/query/persist-client.ts`
- New `PER_PREFIX_MAX_AGE_MS` map (file-local) seeded with `RUNTIME_SKILLS_QUERY_KEY_PREFIX → 5 * 60 * 1000`.
- `shouldDehydrateQuery` refuses to dehydrate any entry whose `dataUpdatedAt` is already past its family's per-prefix cap → a tab idled past 5min before close persists nothing for that bucket.
- New exported `evictPerPrefixStaleEntries(client)` walks the cache and `removeQueries` for entries past their cap → a tab that persisted while fresh then reopens hours later drops the bucket on hydrate.
- `syncRestoreCache` invokes the scrub after hydrate.

### `components/ClientLayout.tsx`
- `PersistQueryClientProvider.onSuccess` calls `evictPerPrefixStaleEntries(queryClient)` so the provider's effect-based hydrate is symmetric with the imperative sync prefill.

### `hooks/queries/skills/useRuntimeSkills.ts`
- Docstring rewritten to call out the two-tier guard (`staleTime` + per-prefix max-age) on the reading path — the design contract lives next to the code, not just the PR body.

### Tests (+6 cases, +106 LOC)
- `shouldDehydrateQuery`: stale runtime-skills rejected (>5min), fresh preserved (<5min), other allowed families unaffected at 1h.
- `evictPerPrefixStaleEntries`: stale runtime evicted, fresh preserved, other allowed families untouched even when backdated 1h.
- `syncRestoreCache`: stale runtime payload (>5min) gone from client after restore.

## Test plan

- [x] `pnpm lint` clean
- [x] `npx tsc --noEmit` clean
- [x] `./node_modules/.bin/vitest run tests/unit/lib/query/persist-client.unit.spec.ts` — 39 passed (was 33, +6 new)
- [x] `pnpm lint:ci` clean (knip would flag if I left dead exports; only `evictPerPrefixStaleEntries` is module-public)

## UX semantics

| Scenario | Pre-RQ | PR #2039 (before this) | This PR |
|---|---|---|---|
| Same-tab nav within 5min | cache hit, no fetch | cache hit, no fetch | cache hit, no fetch |
| Reopen tab after 2h | spinner → fetch | flash of stale data → fetch | spinner → fetch (matches pre-RQ) |
| Same-tab mutation | cache invalidated | RQ invalidated | RQ invalidated (unchanged) |

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [2c71696] chore(docs): remove 5 stale docs/ root files (audit bucket A) (#2041)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T10:20:10Z
- **PR**: #2041

### Commit Message
```
chore(docs): remove 5 stale docs/ root files (audit bucket A) (#2041)

## Summary

Phase-2 docs audit, bucket A — five files with zero inbound references
AND no unique surviving value AND a modern equivalent already
maintained.

| File | Lines | Why it goes | Modern equivalent |
|---|---|---|---|
| `docs/code-review-2026-02.md` | 226 | One-off 2026-02-24 review of
pre-restructure `apps/ecap`; never iterated | `web/CLAUDE.md` (22KB,
actively maintained) |
| `docs/web-code-review-2026-03-10.md` | 278 | One-off 2026-03-10
review; PR #25 finding already resolved per its own text, others not
followed up here | `web/CLAUDE.md` + per-PR review trail |
| `docs/local-dev-guide.md` | 179 | Devcontainer paths predate the
`web/app/` restructure | root `CLAUDE.md` DevContainer section +
`web/CLAUDE.md` |
| `docs/openclaw-flow.html` | 444 | Standalone flow diagram; visual
artifacts belong in Figma | n/a (deprecated artifact) |
| `docs/architecture.html` | — | Standalone HTML diagram | root
`architecture.md` (Mermaid topology, current) |

Inbound references for all five verified empty via:

```
grep -rn "code-review-2026-02\|web-code-review-2026-03-10\|local-dev-guide\|openclaw-flow\.html\|architecture\.html" \
  --include='*.md' --include='*.ts' --include='*.tsx' --include='*.html' \
  --include='*.yml' --include='*.yaml' --include='*.mjs' --include='*.sh' \
  --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=.worktrees .
```

Returns 0 hits across the repo.

Same disposition as the prior phase-1 cleanups:
- #2035 `docs/development/` removed
- #2036 `docs/features/` removed
- #2038 `docs/architecture/` + `docs/setup/quick-start.md` removed

## Out of scope for this PR (bucket B / C — being tracked separately)

- `docs/asset-size-guide.md` — has unique value (threshold table,
two-tier defense, backup path); needs a light path-fix only
(`.husky/scripts/` → `web/.husky/`/`web/scripts/`). Will land in a
follow-up.
- `docs/cron-triggers.md` — intentional stub from #2017; **not** to be
removed (historical relative links from `docs/superpowers/plans/`
resolve through it).
- Bucket C items (`canvas-design.md`, `setup/stripe.md`, Firebase docs,
legal texts, PRDs, `design/google-workspace-pod-injection.md`) — owner
judgment required, separate PRs.

## Test plan

- [ ] `grep -rn "<each filename stem>"` returns empty.
- [ ] CI green (doc-only deletions; no link checker should fire).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Phase-2 docs audit, bucket A — five files with zero inbound references AND no unique surviving value AND a modern equivalent already maintained.

| File | Lines | Why it goes | Modern equivalent |
|---|---|---|---|
| `docs/code-review-2026-02.md` | 226 | One-off 2026-02-24 review of pre-restructure `apps/ecap`; never iterated | `web/CLAUDE.md` (22KB, actively maintained) |
| `docs/web-code-review-2026-03-10.md` | 278 | One-off 2026-03-10 review; PR #25 finding already resolved per its own text, others not followed up here | `web/CLAUDE.md` + per-PR review trail |
| `docs/local-dev-guide.md` | 179 | Devcontainer paths predate the `web/app/` restructure | root `CLAUDE.md` DevContainer section + `web/CLAUDE.md` |
| `docs/openclaw-flow.html` | 444 | Standalone flow diagram; visual artifacts belong in Figma | n/a (deprecated artifact) |
| `docs/architecture.html` | — | Standalone HTML diagram | root `architecture.md` (Mermaid topology, current) |

Inbound references for all five verified empty via:

```
grep -rn "code-review-2026-02\|web-code-review-2026-03-10\|local-dev-guide\|openclaw-flow\.html\|architecture\.html" \
  --include='*.md' --include='*.ts' --include='*.tsx' --include='*.html' \
  --include='*.yml' --include='*.yaml' --include='*.mjs' --include='*.sh' \
  --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=.worktrees .
```

Returns 0 hits across the repo.

Same disposition as the prior phase-1 cleanups:
- #2035 `docs/development/` removed
- #2036 `docs/features/` removed
- #2038 `docs/architecture/` + `docs/setup/quick-start.md` removed

## Out of scope for this PR (bucket B / C — being tracked separately)

- `docs/asset-size-guide.md` — has unique value (threshold table, two-tier defense, backup path); needs a light path-fix only (`.husky/scripts/` → `web/.husky/`/`web/scripts/`). Will land in a follow-up.
- `docs/cron-triggers.md` — intentional stub from #2017; **not** to be removed (historical relative links from `docs/superpowers/plans/` resolve through it).
- Bucket C items (`canvas-design.md`, `setup/stripe.md`, Firebase docs, legal texts, PRDs, `design/google-workspace-pod-injection.md`) — owner judgment required, separate PRs.

## Test plan

- [ ] `grep -rn "<each filename stem>"` returns empty.
- [ ] CI green (doc-only deletions; no link checker should fire).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [20a63de] chore(docs): archive 2 PRDs + delete leaked personal scratch (docs/prds/) (#2044)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T10:19:22Z
- **PR**: #2044

### Commit Message
```
chore(docs): archive 2 PRDs + delete leaked personal scratch (docs/prds/) (#2044)

## Summary

Three actions on `docs/prds/`:

1. **Delete `addtask.md`** — 5-line personal scratch list, accidentally
committed. Two tasks reference
`/Users/vincent/Code/claude-src-analysis/buddy-analysis-report.md` (a
contributor's local machine path); the rest discuss "Zoo Buddy"
mechanics that have **zero matching code** in this repo (`grep buddy` in
`web/app/src` returns 0 hits). Not a PRD, no archival value.

2. **Archive `specialists.md` →
`docs/archive/prds/2026-03-25-specialists-prd.md`** — 14-animal
specialist persona PRD from PR #244 (2026-03-25). The concept is live
(`web/app/src/app/landing/components/LandingSpecialists.tsx`), but the
doc hasn't been kept in sync with the current `SPECIALISTS` data passed
into that component. Archived to preserve original design intent; live
code is the runtime source of truth.

3. **Archive `ZooClaw onboard.md` →
`docs/archive/prds/2026-03-23-zooclaw-onboard-prd.md`** — early
onboarding PRD from PR #197 (2026-03-23). All described elements (sprite
guide / invite code / paywall / scenario carousel / channel selection)
are implemented (`OnboardingContext`, `INVITE_CODE` storage key, paywall
flow, LandingSpecialists), but the doc self-contradicts on the number of
animals (says 8 then 12, while `specialists.md` lists 14) — it's a stale
early design draft, not a current spec. Archived for design history.

Both archived files renamed to follow the existing
`YYYY-MM-DD-{name}-{type}.md` convention used in `docs/archive/prds/`
(e.g. `2026-03-26-credits-billing-refinement-plan.md`). Dates are real
git creation dates from `git log --follow` (not mtime, which resets on
copy). The `ZooClaw onboard.md` filename also had a space → tidied to
kebab-case.

Updated one relative link in `docs/archive/prds/update_0323.md` to point
at the new archived path. Empty `docs/prds/` directory removed.

## Test plan

- [ ] `grep -rn "docs/prds"` returns empty (sole inbound ref was already
updated).
- [ ] `grep -rn "ZooClaw onboard\.md\|prds/specialists"` returns empty.
- [ ] CI green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Three actions on `docs/prds/`:

1. **Delete `addtask.md`** — 5-line personal scratch list, accidentally committed. Two tasks reference `/Users/vincent/Code/claude-src-analysis/buddy-analysis-report.md` (a contributor's local machine path); the rest discuss "Zoo Buddy" mechanics that have **zero matching code** in this repo (`grep buddy` in `web/app/src` returns 0 hits). Not a PRD, no archival value.

2. **Archive `specialists.md` → `docs/archive/prds/2026-03-25-specialists-prd.md`** — 14-animal specialist persona PRD from PR #244 (2026-03-25). The concept is live (`web/app/src/app/landing/components/LandingSpecialists.tsx`), but the doc hasn't been kept in sync with the current `SPECIALISTS` data passed into that component. Archived to preserve original design intent; live code is the runtime source of truth.

3. **Archive `ZooClaw onboard.md` → `docs/archive/prds/2026-03-23-zooclaw-onboard-prd.md`** — early onboarding PRD from PR #197 (2026-03-23). All described elements (sprite guide / invite code / paywall / scenario carousel / channel selection) are implemented (`OnboardingContext`, `INVITE_CODE` storage key, paywall flow, LandingSpecialists), but the doc self-contradicts on the number of animals (says 8 then 12, while `specialists.md` lists 14) — it's a stale early design draft, not a current spec. Archived for design history.

Both archived files renamed to follow the existing `YYYY-MM-DD-{name}-{type}.md` convention used in `docs/archive/prds/` (e.g. `2026-03-26-credits-billing-refinement-plan.md`). Dates are real git creation dates from `git log --follow` (not mtime, which resets on copy). The `ZooClaw onboard.md` filename also had a space → tidied to kebab-case.

Updated one relative link in `docs/archive/prds/update_0323.md` to point at the new archived path. Empty `docs/prds/` directory removed.

## Test plan

- [ ] `grep -rn "docs/prds"` returns empty (sole inbound ref was already updated).
- [ ] `grep -rn "ZooClaw onboard\.md\|prds/specialists"` returns empty.
- [ ] CI green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [1841076] fix(billing): match existing partial index specs (#2033)
- **作者**: kaka-srp
- **日期**: 2026-05-28T10:18:48Z
- **PR**: #2033

### Commit Message
```
fix(billing): match existing partial index specs (#2033)

## Summary
- Keep the Mongo-supported `$gt: ""` optional string partial filters
from #2012.
- Restore `$exists: true` on Billing v2 optional unique indexes so Mongo
index specs are explicit and stable.
- Add a guarded manual index path that rebuilds only known equivalent
old Billing v2 string partial indexes (`$ne`, no-`$exists`, or exact
current form), then recreates them with the current spec.
- Remove Billing v2 profile/payment/subscription index creation from
normal app startup; these indexes must be prepared before rollout with
`python -m scripts.ensure_billing_v2_indexes`.
- Keep startup enforcement as validation only: startup checks those
Billing v2 indexes already exist with the expected specs and fails fast
with the manual command if they are missing or drifted.
- Add `services/claw-interface/docs/billing-v2-index-rollout.md` as the
runbook for the manual pre-deploy step.
- Update tests to lock the exact profile/payment/subscription partial
filter expressions, cover the guarded rebuild path, cover
validation-only behavior, and assert startup does not create those
manual Billing v2 indexes.

## Why
Staging still fails after #2012 because Mongo sees the requested profile
index as different from the existing same-name index:

```text
Requested: partialFilterExpression: { customer_id: { $type: "string", $gt: "" } }
Existing:  partialFilterExpression: { customer_id: { $exists: true, $type: "string", $gt: "" } }
codeName: IndexKeySpecsConflict
```

`$exists + $type + $gt` is accepted by staging Mongo and avoids the
original unsupported `$ne`/`$not` predicate while making the stored spec
explicit. The rebuild fallback is now a controlled pre-deploy operation
rather than a multi-replica startup side effect; startup only verifies
the manual step was completed.

## Manual rollout step
Before deploying this service change to an environment, run:

```bash
cd services/claw-interface
python -m scripts.ensure_billing_v2_indexes
```

This may drop/recreate equivalent legacy unique indexes, so it should be
run as a deliberate pre-rollout operation with billing writes controlled
as needed. If this step is missed, app startup will fail with a message
pointing to this command instead of booting without the required
indexes. See `services/claw-interface/docs/billing-v2-index-rollout.md`.

## Test Plan
- `/home/node/.venvs/claw-interface/bin/ruff format --check
app/lifetime.py app/database/billing_index_utils.py
app/database/billing_profile_repo.py app/database/payment_order_repo.py
app/database/subscription_agreement_repo.py
scripts/ensure_billing_v2_indexes.py tests/unit/test_lifetime.py
tests/unit/test_billing_v2_repos.py`
- `/home/node/.venvs/claw-interface/bin/ruff check app/lifetime.py
app/database/billing_index_utils.py app/database/billing_profile_repo.py
app/database/payment_order_repo.py
app/database/subscription_agreement_repo.py
scripts/ensure_billing_v2_indexes.py tests/unit/test_lifetime.py
tests/unit/test_billing_v2_repos.py`
- `/home/node/.venvs/claw-interface/bin/pyright app/lifetime.py
app/database/billing_index_utils.py app/database/billing_profile_repo.py
app/database/payment_order_repo.py
app/database/subscription_agreement_repo.py
scripts/ensure_billing_v2_indexes.py tests/unit/test_lifetime.py
tests/unit/test_billing_v2_repos.py`
- `/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_billing_v2_repos.py tests/unit/test_lifetime.py -q`
- `/home/node/.venvs/claw-interface/bin/python -m
scripts.ensure_billing_v2_indexes --help`
```

### PR Body
## Summary
- Keep the Mongo-supported `$gt: ""` optional string partial filters from #2012.
- Restore `$exists: true` on Billing v2 optional unique indexes so Mongo index specs are explicit and stable.
- Add a guarded manual index path that rebuilds only known equivalent old Billing v2 string partial indexes (`$ne`, no-`$exists`, or exact current form), then recreates them with the current spec.
- Remove Billing v2 profile/payment/subscription index creation from normal app startup; these indexes must be prepared before rollout with `python -m scripts.ensure_billing_v2_indexes`.
- Keep startup enforcement as validation only: startup checks those Billing v2 indexes already exist with the expected specs and fails fast with the manual command if they are missing or drifted.
- Add `services/claw-interface/docs/billing-v2-index-rollout.md` as the runbook for the manual pre-deploy step.
- Update tests to lock the exact profile/payment/subscription partial filter expressions, cover the guarded rebuild path, cover validation-only behavior, and assert startup does not create those manual Billing v2 indexes.

## Why
Staging still fails after #2012 because Mongo sees the requested profile index as different from the existing same-name index:

```text
Requested: partialFilterExpression: { customer_id: { $type: "string", $gt: "" } }
Existing:  partialFilterExpression: { customer_id: { $exists: true, $type: "string", $gt: "" } }
codeName: IndexKeySpecsConflict
```

`$exists + $type + $gt` is accepted by staging Mongo and avoids the original unsupported `$ne`/`$not` predicate while making the stored spec explicit. The rebuild fallback is now a controlled pre-deploy operation rather than a multi-replica startup side effect; startup only verifies the manual step was completed.

## Manual rollout step
Before deploying this service change to an environment, run:

```bash
cd services/claw-interface
python -m scripts.ensure_billing_v2_indexes
```

This may drop/recreate equivalent legacy unique indexes, so it should be run as a deliberate pre-rollout operation with billing writes controlled as needed. If this step is missed, app startup will fail with a message pointing to this command instead of booting without the required indexes. See `services/claw-interface/docs/billing-v2-index-rollout.md`.

## Test Plan
- `/home/node/.venvs/claw-interface/bin/ruff format --check app/lifetime.py app/database/billing_index_utils.py app/database/billing_profile_repo.py app/database/payment_order_repo.py app/database/subscription_agreement_repo.py scripts/ensure_billing_v2_indexes.py tests/unit/test_lifetime.py tests/unit/test_billing_v2_repos.py`
- `/home/node/.venvs/claw-interface/bin/ruff check app/lifetime.py app/database/billing_index_utils.py app/database/billing_profile_repo.py app/database/payment_order_repo.py app/database/subscription_agreement_repo.py scripts/ensure_billing_v2_indexes.py tests/unit/test_lifetime.py tests/unit/test_billing_v2_repos.py`
- `/home/node/.venvs/claw-interface/bin/pyright app/lifetime.py app/database/billing_index_utils.py app/database/billing_profile_repo.py app/database/payment_order_repo.py app/database/subscription_agreement_repo.py scripts/ensure_billing_v2_indexes.py tests/unit/test_lifetime.py tests/unit/test_billing_v2_repos.py`
- `/home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_billing_v2_repos.py tests/unit/test_lifetime.py -q`
- `/home/node/.venvs/claw-interface/bin/python -m scripts.ensure_billing_v2_indexes --help`

---
## [9f7f142] chore(docs): remove unused docs/legals/ markdown (site has its own canonical) (#2042)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T10:14:39Z
- **PR**: #2042

### Commit Message
```
chore(docs): remove unused docs/legals/ markdown (site has its own canonical) (#2042)

## Summary

`docs/legals/260325/{privacy,terms}.md` were never wired into the
runtime — no `fs.readFileSync`, no `import`, no build step reads them
(verified via grep across `web/app/src/**`). The Privacy / Terms text
users actually see is hardcoded as JSX in four places:

- `web/app/src/app/about/privacy/page.tsx` (canonical, locale-free)
- `web/app/src/app/about/terms/page.tsx` (canonical, locale-free)
- `web/app/src/app/[locale]/about/privacy/PrivacyClient.tsx`
(locale-mirror deep-link fallback)
- `web/app/src/app/[locale]/about/terms/TermsClient.tsx` (locale-mirror
deep-link fallback)

The locale-free path is the canonical — `[locale]/terms/page.tsx`
explicitly documents this and redirects to `/about/terms`;
`middleware.ts` skips locale handling for `/about/{privacy,terms}`;
`_seo.ts` `legalPaths` only lists the locale-free path.

The two markdown files were a parallel copy that had **already drifted**
from the served pages — e.g. `privacy.md` says "product version of
**OpenClaw**" while the page says "product version of **Claw**". Keeping
the markdown as an unmaintained reference is worse than removing it:
anyone editing it might assume changes ship to users, but nothing does.

Deleted rather than archived: not load-bearing, not synced, and the live
drift made the markdown actively misleading. Git history preserves them
if the `YYMMDD/` folder pattern is ever reintroduced as a real
source-of-truth scheme (build-time MD → JSX codegen, sync check, etc.).

Empty `docs/legals/260325/` and `docs/legals/` directories also removed.

## Out of scope (flagged separately, not blocking this PR)

The served pages contain a possible typo worth a product / legal review:

```
served:   "ZooClaw, the online cloud service product version of Claw"
markdown: "ZooClaw, the online cloud service product version of OpenClaw"
```

This is what users actually see at `/about/privacy`. The JSX is the
runtime source of truth either way; this PR does not touch it.

## Test plan

- [ ] `grep -rn "legals/260325\|docs/legals"` returns empty in
non-archive code.
- [ ] `/about/privacy` and `/about/terms` continue to render the same
content (no runtime change — only `docs/` files removed).
- [ ] CI green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

`docs/legals/260325/{privacy,terms}.md` were never wired into the runtime — no `fs.readFileSync`, no `import`, no build step reads them (verified via grep across `web/app/src/**`). The Privacy / Terms text users actually see is hardcoded as JSX in four places:

- `web/app/src/app/about/privacy/page.tsx` (canonical, locale-free)
- `web/app/src/app/about/terms/page.tsx` (canonical, locale-free)
- `web/app/src/app/[locale]/about/privacy/PrivacyClient.tsx` (locale-mirror deep-link fallback)
- `web/app/src/app/[locale]/about/terms/TermsClient.tsx` (locale-mirror deep-link fallback)

The locale-free path is the canonical — `[locale]/terms/page.tsx` explicitly documents this and redirects to `/about/terms`; `middleware.ts` skips locale handling for `/about/{privacy,terms}`; `_seo.ts` `legalPaths` only lists the locale-free path.

The two markdown files were a parallel copy that had **already drifted** from the served pages — e.g. `privacy.md` says "product version of **OpenClaw**" while the page says "product version of **Claw**". Keeping the markdown as an unmaintained reference is worse than removing it: anyone editing it might assume changes ship to users, but nothing does.

Deleted rather than archived: not load-bearing, not synced, and the live drift made the markdown actively misleading. Git history preserves them if the `YYMMDD/` folder pattern is ever reintroduced as a real source-of-truth scheme (build-time MD → JSX codegen, sync check, etc.).

Empty `docs/legals/260325/` and `docs/legals/` directories also removed.

## Out of scope (flagged separately, not blocking this PR)

The served pages contain a possible typo worth a product / legal review:

```
served:   "ZooClaw, the online cloud service product version of Claw"
markdown: "ZooClaw, the online cloud service product version of OpenClaw"
```

This is what users actually see at `/about/privacy`. The JSX is the runtime source of truth either way; this PR does not touch it.

## Test plan

- [ ] `grep -rn "legals/260325\|docs/legals"` returns empty in non-archive code.
- [ ] `/about/privacy` and `/about/terms` continue to render the same content (no runtime change — only `docs/` files removed).
- [ ] CI green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [12185d9] refactor(web): migrate skills-store runtime-skills to RQ + persister (#1999 Bucket-3 PR-B) (#2039)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T10:11:23Z
- **PR**: #2039

### Commit Message
```
refactor(web): migrate skills-store runtime-skills to RQ + persister (#1999 Bucket-3 PR-B) (#2039)

## Summary

Replaces the manual `sessionStorage['skills-store:runtime:v3:…']` TTL
wrapper that `lib/api/skills-store.ts` maintained pre-#1999 with a
`useRuntimeSkills(uid)` hook backed by React Query +
`PersistQueryClientProvider`.

Parallel sibling: PR-C (#2037 — `community-client` migration).
`session-cache.ts` deletion deferred to PR-D once both land.

Contributes to #1999 — does **not** close it (PR-C + PR-D remain).

## Production changes

| File | Change |
|---|---|
| `src/hooks/queries/skills/keys.ts` (new) | `skillsKeys.runtime(uid)`
factory |
| `src/hooks/queries/skills/useRuntimeSkills.ts` (new) | `useQuery`
wrapper |
| `src/lib/query/keys.ts` | new `RUNTIME_SKILLS_QUERY_KEY_PREFIX` const
|
| `src/lib/query/persist-client.ts` | append prefix to
`PERSIST_ALLOWLIST_PREFIXES` (3rd entry) |
| `src/lib/api/skills-store.ts` | drop `session-cache` import + cache
helpers; now pure fetch wrappers |
| `SkillsSearchClient.tsx` / `SkillDetailClient.tsx` | switch inline
`useQuery` + `readCachedRuntimeSkills` seed → `useRuntimeSkills(uid)` |

## Test changes

- **New**:
`tests/unit/hooks/queries/skills/useRuntimeSkills.unit.spec.tsx` — 6
cases (disabled / fetch / dedup / uid isolation / error / queryKey
shape).
- **Slimmed**: Phase-0 `skills-store.unit.spec.ts` — characterization
for deleted helpers retired alongside the helpers (mirrors how #1990
retired `agent-catalog-cache` characterization).
- **Updated**: 3 consumer specs (skills-store-install-toast /
SkillDetailClient / SkillsSearchClient) — `readCachedRuntimeSkills`
mocks dropped; cache seeds rewritten to
`testQueryClient.setQueryData(skillsKeys.runtime(uid), …)`.
- **Updated**: `persist-client.unit.spec.ts` —
`PERSIST_ALLOWLIST_PREFIXES` length 2→3 + new `containEqual` assertion.

## Governance

- R2 inline-disable count: **7 → 6** (skills-store.ts disable removed).
- shrink-only `check-cache-governance-disables-shrink-only.sh` passes
locally.
- `session-cache.ts` not touched (PR-D).

## Test plan

- [x] `pnpm lint` clean
- [x] `npx tsc --noEmit` clean
- [x] `./node_modules/.bin/vitest run` — 404 files / 6159 tests / 1
todo, all green
- [x] `pnpm lint:ci` clean (dep-cruise + knip)
- [x] `bash web/scripts/check-cache-governance-disables-shrink-only.sh`
— main 7, HEAD 6 ✅

## Not in scope

- `community-client.ts` migration → PR-C (#2037)
- `session-cache.ts` deletion → PR-D
- R3 `ecap:*:updated` events → #2000 Bucket-4

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Body
## Summary

Replaces the manual `sessionStorage['skills-store:runtime:v3:…']` TTL wrapper that `lib/api/skills-store.ts` maintained pre-#1999 with a `useRuntimeSkills(uid)` hook backed by React Query + `PersistQueryClientProvider`.

Parallel sibling: PR-C (#2037 — `community-client` migration). `session-cache.ts` deletion deferred to PR-D once both land.

Contributes to #1999 — does **not** close it (PR-C + PR-D remain).

## Production changes

| File | Change |
|---|---|
| `src/hooks/queries/skills/keys.ts` (new) | `skillsKeys.runtime(uid)` factory |
| `src/hooks/queries/skills/useRuntimeSkills.ts` (new) | `useQuery` wrapper |
| `src/lib/query/keys.ts` | new `RUNTIME_SKILLS_QUERY_KEY_PREFIX` const |
| `src/lib/query/persist-client.ts` | append prefix to `PERSIST_ALLOWLIST_PREFIXES` (3rd entry) |
| `src/lib/api/skills-store.ts` | drop `session-cache` import + cache helpers; now pure fetch wrappers |
| `SkillsSearchClient.tsx` / `SkillDetailClient.tsx` | switch inline `useQuery` + `readCachedRuntimeSkills` seed → `useRuntimeSkills(uid)` |

## Test changes

- **New**: `tests/unit/hooks/queries/skills/useRuntimeSkills.unit.spec.tsx` — 6 cases (disabled / fetch / dedup / uid isolation / error / queryKey shape).
- **Slimmed**: Phase-0 `skills-store.unit.spec.ts` — characterization for deleted helpers retired alongside the helpers (mirrors how #1990 retired `agent-catalog-cache` characterization).
- **Updated**: 3 consumer specs (skills-store-install-toast / SkillDetailClient / SkillsSearchClient) — `readCachedRuntimeSkills` mocks dropped; cache seeds rewritten to `testQueryClient.setQueryData(skillsKeys.runtime(uid), …)`.
- **Updated**: `persist-client.unit.spec.ts` — `PERSIST_ALLOWLIST_PREFIXES` length 2→3 + new `containEqual` assertion.

## Governance

- R2 inline-disable count: **7 → 6** (skills-store.ts disable removed).
- shrink-only `check-cache-governance-disables-shrink-only.sh` passes locally.
- `session-cache.ts` not touched (PR-D).

## Test plan

- [x] `pnpm lint` clean
- [x] `npx tsc --noEmit` clean
- [x] `./node_modules/.bin/vitest run` — 404 files / 6159 tests / 1 todo, all green
- [x] `pnpm lint:ci` clean (dep-cruise + knip)
- [x] `bash web/scripts/check-cache-governance-disables-shrink-only.sh` — main 7, HEAD 6 ✅

## Not in scope

- `community-client.ts` migration → PR-C (#2037)
- `session-cache.ts` deletion → PR-D
- R3 `ecap:*:updated` events → #2000 Bucket-4

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [b783fbd] chore(web): narrow useCanvasState lint override after F13 split (#2040)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T10:03:57Z
- **PR**: #2040

### Commit Message
```
chore(web): narrow useCanvasState lint override after F13 split (#2040)

## Summary

Follow-up to F13 god-hook split (issue #368, landed via #2022 / #2027 /
#2034).

\`useCanvasState.ts\` is now **424 raw lines** (was 788, -46%),
comfortably under the default \`max-lines: 600\` ceiling. Dropping the
\`max-lines: 'off'\` exemption.

The composition function is still **317 lines** (17 over the default
\`max-lines-per-function: 300\`) — irreducible without sacrificing the
composition shape: 14 \`useCallback\` wrappers + 4 sub-hook calls + the
22-field return that \`CanvasClient\` destructures. Per memory
\`feedback_lint_line_limits_800\` ("先尽量拆;只有抽完所有合理子组件仍超才 per-file
override"), the per-function exemption stays, narrowed and re-commented
to point at the F13 spec.

## Test plan

- [x] \`pnpm --filter @zooclaw/web-app lint\` clean
- [ ] CI green

Refs #368 F13.

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Follow-up to F13 god-hook split (issue #368, landed via #2022 / #2027 / #2034).

\`useCanvasState.ts\` is now **424 raw lines** (was 788, -46%), comfortably under the default \`max-lines: 600\` ceiling. Dropping the \`max-lines: 'off'\` exemption.

The composition function is still **317 lines** (17 over the default \`max-lines-per-function: 300\`) — irreducible without sacrificing the composition shape: 14 \`useCallback\` wrappers + 4 sub-hook calls + the 22-field return that \`CanvasClient\` destructures. Per memory \`feedback_lint_line_limits_800\` ("先尽量拆;只有抽完所有合理子组件仍超才 per-file override"), the per-function exemption stays, narrowed and re-commented to point at the F13 spec.

## Test plan

- [x] \`pnpm --filter @zooclaw/web-app lint\` clean
- [ ] CI green

Refs #368 F13.

---
## [55eae53] chore(docs): remove stale docs/architecture/ + docs/setup/quick-start.md (#2038)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T09:51:05Z
- **PR**: #2038

### Commit Message
```
chore(docs): remove stale docs/architecture/ + docs/setup/quick-start.md (#2038)

## Summary

Removes four time-frozen Jan-2025-era documents that all predate the
`web/app/` nested-workspace restructure and have drifted significantly
from current code:

- `docs/architecture/api-proxy.md` (487 lines) — all `src/lib/api/*`
paths broken; misses half the live middleware rules
(`/api/antom/webhook`, `/api/chat-replays/<share>/` GET prefix, token
≥32 char enforcement, X-User-UID stripping, backend admin-permission
roundtrip); proxy.ts implementation has moved on (CLAW_INTERFACE_URL
priority, `getCFAccessHeaders()`, Authorization forwarding, 10-min
timeout) — none reflected; misses the canonical two-client guidance in
`web/app/CLAUDE.md:138` (backend.ts BFF vs client.ts direct).
- `docs/architecture/backend-integration.md` (315 lines) — paths broken;
STORAGE_KEYS list incomplete (missing BRAND_THEME, AGENTS_CACHE,
MM_TOKEN, MM_SERVER_URL, BILLING_MOCK*, INVITE_CODE); API-call sections
duplicate api-proxy.md; superseded by `web/app/CLAUDE.md` "Client cache
& storage" section (R1/R2/R3 + Tier C/D table with lint enforcement).
- `docs/architecture/design-system.md` (215 lines) — paths broken;
treats `src/components/ui/` as the main path, but current convention in
`web/app/CLAUDE.md` is `src/components/ds/*` (shadcn-first); update log
ends with three `Later:` placeholders (explicit "maintainer gave up"
signal); numeric token reference duplicates `globals.css`.
- `docs/setup/quick-start.md` (203 lines) — paths broken; env-var
guidance uses `BACKEND_URL` (proxy.ts now prefers `CLAW_INTERFACE_URL`);
only inbound references were to the two architecture docs being deleted
here; modern equivalents = root CLAUDE.md (DevContainer) + web/CLAUDE.md
(workspace) + web/app/CLAUDE.md (22KB).

Verified against the live source (`web/app/src/lib/api/backend.ts`,
`proxy.ts`, `middleware.ts`, `lib/auth/types.ts`) and the actively
maintained replacements (`architecture.md` for cross-service topology,
`web/app/CLAUDE.md` for frontend conventions — last edited today).

`docs/architecture/` empty after deletion; directory removed.
`docs/setup/` keeps `cloudflare-access.md`, `phone-login.md`,
`stripe.md` (not in scope this round).

Same disposition as the prior `docs/development/` (#2035) and
`docs/features/` (#2036) cleanups.

## Test plan

- [ ] `grep -rn "docs/architecture\|docs/setup/quick-start"
--exclude-dir={node_modules,.next,.worktrees}` returns empty.
- [ ] CI green (doc-only deletions, no link checker should fire).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Removes four time-frozen Jan-2025-era documents that all predate the `web/app/` nested-workspace restructure and have drifted significantly from current code:

- `docs/architecture/api-proxy.md` (487 lines) — all `src/lib/api/*` paths broken; misses half the live middleware rules (`/api/antom/webhook`, `/api/chat-replays/<share>/` GET prefix, token ≥32 char enforcement, X-User-UID stripping, backend admin-permission roundtrip); proxy.ts implementation has moved on (CLAW_INTERFACE_URL priority, `getCFAccessHeaders()`, Authorization forwarding, 10-min timeout) — none reflected; misses the canonical two-client guidance in `web/app/CLAUDE.md:138` (backend.ts BFF vs client.ts direct).
- `docs/architecture/backend-integration.md` (315 lines) — paths broken; STORAGE_KEYS list incomplete (missing BRAND_THEME, AGENTS_CACHE, MM_TOKEN, MM_SERVER_URL, BILLING_MOCK*, INVITE_CODE); API-call sections duplicate api-proxy.md; superseded by `web/app/CLAUDE.md` "Client cache & storage" section (R1/R2/R3 + Tier C/D table with lint enforcement).
- `docs/architecture/design-system.md` (215 lines) — paths broken; treats `src/components/ui/` as the main path, but current convention in `web/app/CLAUDE.md` is `src/components/ds/*` (shadcn-first); update log ends with three `Later:` placeholders (explicit "maintainer gave up" signal); numeric token reference duplicates `globals.css`.
- `docs/setup/quick-start.md` (203 lines) — paths broken; env-var guidance uses `BACKEND_URL` (proxy.ts now prefers `CLAW_INTERFACE_URL`); only inbound references were to the two architecture docs being deleted here; modern equivalents = root CLAUDE.md (DevContainer) + web/CLAUDE.md (workspace) + web/app/CLAUDE.md (22KB).

Verified against the live source (`web/app/src/lib/api/backend.ts`, `proxy.ts`, `middleware.ts`, `lib/auth/types.ts`) and the actively maintained replacements (`architecture.md` for cross-service topology, `web/app/CLAUDE.md` for frontend conventions — last edited today).

`docs/architecture/` empty after deletion; directory removed. `docs/setup/` keeps `cloudflare-access.md`, `phone-login.md`, `stripe.md` (not in scope this round).

Same disposition as the prior `docs/development/` (#2035) and `docs/features/` (#2036) cleanups.

## Test plan

- [ ] `grep -rn "docs/architecture\|docs/setup/quick-start" --exclude-dir={node_modules,.next,.worktrees}` returns empty.
- [ ] CI green (doc-only deletions, no link checker should fire).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [308fd7f] refactor(web): migrate community-client to RQ + persister (#1999 Bucket-3 PR-C) (#2037)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T09:49:06Z
- **PR**: #2037

### Commit Message
```
refactor(web): migrate community-client to RQ + persister (#1999 Bucket-3 PR-C) (#2037)

## Summary

Bucket-3 PR-C (#1999) — replaces the hand-maintained
`sessionStorage[skills-store:community:*]` TTL wrap layer in
`lib/skills/community-client.ts` with the React Query persister
(provisioned by Bucket-1 / PR #1990).

`listCommunitySkills` / `getCommunitySkillDetail` are now pure fetchers
consumed as RQ `queryFn`s; cross-mount survival is owned by
`COMMUNITY_SKILLS_{LIST,DETAIL}_QUERY_KEY_PREFIX` entries in
`PERSIST_ALLOWLIST_PREFIXES`.

Contributing to #1999 — **does not close the umbrella**; PR-B
(`skills-store.ts` runtime cache) and PR-D (`session-cache.ts`
deletion + final unwiring) are tracked separately.

## Migration diff

| Surface | Before | After |
|---|---|---|
| `lib/skills/community-client.ts` |
`writeSessionCache(buildCommunityListCacheKey(...), payload)` after each
fetch | pure fetch — no storage write |
| `lib/skills/community-client.ts` | exports `readCachedCommunitySkills`
/ `readCachedCommunitySkillDetail` | both accessors deleted (persister
owns hydration) |
| `lib/skills/community-client.ts` | imports `readSessionCache` /
`writeSessionCache` via R2 disable | imports removed; R2 TODO comment
deleted |
| `lib/query/keys.ts` | — | adds
`COMMUNITY_SKILLS_LIST_QUERY_KEY_PREFIX` +
`COMMUNITY_SKILLS_DETAIL_QUERY_KEY_PREFIX` |
| `lib/query/persist-client.ts` | `PERSIST_ALLOWLIST_PREFIXES` has 2
Bucket-2 entries | adds 2 community-skills prefixes (total 4) |
| `SkillsSearchClient.tsx` | `readCachedCommunitySkills` →
`useInfiniteQuery.initialData` | seed dropped; persister rehydrates
synchronously via `syncRestoreCache` |
| `SkillDetailClient.tsx` | `readCachedCommunitySkillDetail` →
`useQuery.initialData` | seed dropped; same rationale |

## Caller switches (2 prod files)

- `web/app/src/app/[locale]/skills/search/SkillsSearchClient.tsx` — list
path
-
`web/app/src/app/[locale]/skills/[category]/[slug]/SkillDetailClient.tsx`
— detail path

(`web/app/src/lib/skills/runtime-skills.ts` re-exports the
`CommunitySkillDetail` type only — unaffected.)

## Hook wrapper decision

Issue text suggested `useCommunitySkillsList` /
`useCommunitySkillDetail`
hooks, but both consumers were already RQ-native:
`SkillsSearchClient` uses `useInfiniteQuery` (pagination +
`fetchNextPage`
+ `isError` clamping) and `SkillDetailClient` uses a plain `useQuery`.
Wrapping each in a single-caller hook would either lose the rich
infinite
API or add an indirection for one caller. Kept the inline RQ calls and
let the persister do the work, following the AGENTS.md R2 guidance
("persister + `syncRestoreCache` for cross-mount hydration") and the
`feedback_use_stable_callback` precedent against premature wrapper
extraction.

## R2 governance

| | main | HEAD |
|---|---|---|
| `eslint-disable-next-line no-restricted-(imports\|syntax) --
TODO(#...)` count | 7 | 6 |

Net diff = -1 (the `community-client.ts` disable). Concurrent PR-B
(another agent) deletes the `skills-store.ts` disable; the eventual
stable target after both merge is 5. `session-cache.ts` module body
intentionally left in place — its deletion is PR-D's scope.

## Tests

- **Modified `tests/unit/lib/communityClient.unit.spec.ts`** —
  removed 4 `readCached*` cases (functions deleted) and the
  `characterization: cache key + TTL` describe block (sessionStorage
  writes removed). Added 2 falsifiable invariants under
  `PR-C migration invariant: no sessionStorage writes` asserting
  `sessionStorageStore === {}` after each fetcher succeeds.
- **Modified `tests/unit/lib/query/persist-client.unit.spec.ts`** —
  added: (a) `shouldDehydrateQuery` returns true for community list /
  detail keys; (b) `shouldDehydrateQuery` still returns false for
  `skillsKeys.runtime(uid)` (Bucket-3 PR-B territory); (c) the prefix
  allowlist length goes from 2 → 4 and contains both new prefixes;
  (d) the list prefix and detail prefix do not cross-match on either
  side (falsifiability anchor against a future "simplify" PR that
  collapses them to a shared `[v1, skills, community]` segment).
- **Modified caller specs** (`SkillsSearchClient.unit.spec.tsx`,
`SkillDetailClient.unit.spec.tsx`,
`skills-store-install-toast.unit.spec.tsx`)
  — removed `readCached*` from hoisted mocks; rewired the
  `cached community → renders synchronously` / `fetch rejects → keeps
  cached detail` tests to seed the test `QueryClient` directly via
  `queryClient.setQueryData(skillsKeys.community*, ...)`, matching the
  shape `syncRestoreCache` would hydrate from the persister.

## Test plan

- [x] `npx tsc --noEmit` clean
- [x] `vitest run` — 403 files / 6160 tests pass
- [x] `pnpm lint` pass
- [x] `pnpm lint:ci` pass
- [x] `bash web/scripts/check-cache-governance-disables-shrink-only.sh`
— main 7, HEAD 6, shrink-only ✅
- [ ] Manual staging: skills search + detail still render cached data on
      hard refresh (persister-driven), then background-refetch on mount

## Out of scope (deferred to follow-up PRs)

- **`skills-store.ts` runtime cache → RQ** — Bucket-3 PR-B (concurrent
agent)
- **`session-cache.ts` module deletion** — Bucket-3 PR-D (after PR-B +
this PR merge; last consumer goes away)
- **Bucket-4 `OPENCLAW_*` event dispatchers** — issue #2000

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Bucket-3 PR-C (#1999) — replaces the hand-maintained
`sessionStorage[skills-store:community:*]` TTL wrap layer in
`lib/skills/community-client.ts` with the React Query persister
(provisioned by Bucket-1 / PR #1990).

`listCommunitySkills` / `getCommunitySkillDetail` are now pure fetchers
consumed as RQ `queryFn`s; cross-mount survival is owned by
`COMMUNITY_SKILLS_{LIST,DETAIL}_QUERY_KEY_PREFIX` entries in
`PERSIST_ALLOWLIST_PREFIXES`.

Contributing to #1999 — **does not close the umbrella**; PR-B
(`skills-store.ts` runtime cache) and PR-D (`session-cache.ts`
deletion + final unwiring) are tracked separately.

## Migration diff

| Surface | Before | After |
|---|---|---|
| `lib/skills/community-client.ts` | `writeSessionCache(buildCommunityListCacheKey(...), payload)` after each fetch | pure fetch — no storage write |
| `lib/skills/community-client.ts` | exports `readCachedCommunitySkills` / `readCachedCommunitySkillDetail` | both accessors deleted (persister owns hydration) |
| `lib/skills/community-client.ts` | imports `readSessionCache` / `writeSessionCache` via R2 disable | imports removed; R2 TODO comment deleted |
| `lib/query/keys.ts` | — | adds `COMMUNITY_SKILLS_LIST_QUERY_KEY_PREFIX` + `COMMUNITY_SKILLS_DETAIL_QUERY_KEY_PREFIX` |
| `lib/query/persist-client.ts` | `PERSIST_ALLOWLIST_PREFIXES` has 2 Bucket-2 entries | adds 2 community-skills prefixes (total 4) |
| `SkillsSearchClient.tsx` | `readCachedCommunitySkills` → `useInfiniteQuery.initialData` | seed dropped; persister rehydrates synchronously via `syncRestoreCache` |
| `SkillDetailClient.tsx` | `readCachedCommunitySkillDetail` → `useQuery.initialData` | seed dropped; same rationale |

## Caller switches (2 prod files)

- `web/app/src/app/[locale]/skills/search/SkillsSearchClient.tsx` — list path
- `web/app/src/app/[locale]/skills/[category]/[slug]/SkillDetailClient.tsx` — detail path

(`web/app/src/lib/skills/runtime-skills.ts` re-exports the
`CommunitySkillDetail` type only — unaffected.)

## Hook wrapper decision

Issue text suggested `useCommunitySkillsList` / `useCommunitySkillDetail`
hooks, but both consumers were already RQ-native:
`SkillsSearchClient` uses `useInfiniteQuery` (pagination + `fetchNextPage`
+ `isError` clamping) and `SkillDetailClient` uses a plain `useQuery`.
Wrapping each in a single-caller hook would either lose the rich infinite
API or add an indirection for one caller. Kept the inline RQ calls and
let the persister do the work, following the AGENTS.md R2 guidance
("persister + `syncRestoreCache` for cross-mount hydration") and the
`feedback_use_stable_callback` precedent against premature wrapper
extraction.

## R2 governance

| | main | HEAD |
|---|---|---|
| `eslint-disable-next-line no-restricted-(imports\|syntax) -- TODO(#...)` count | 7 | 6 |

Net diff = -1 (the `community-client.ts` disable). Concurrent PR-B
(another agent) deletes the `skills-store.ts` disable; the eventual
stable target after both merge is 5. `session-cache.ts` module body
intentionally left in place — its deletion is PR-D's scope.

## Tests

- **Modified `tests/unit/lib/communityClient.unit.spec.ts`** —
  removed 4 `readCached*` cases (functions deleted) and the
  `characterization: cache key + TTL` describe block (sessionStorage
  writes removed). Added 2 falsifiable invariants under
  `PR-C migration invariant: no sessionStorage writes` asserting
  `sessionStorageStore === {}` after each fetcher succeeds.
- **Modified `tests/unit/lib/query/persist-client.unit.spec.ts`** —
  added: (a) `shouldDehydrateQuery` returns true for community list /
  detail keys; (b) `shouldDehydrateQuery` still returns false for
  `skillsKeys.runtime(uid)` (Bucket-3 PR-B territory); (c) the prefix
  allowlist length goes from 2 → 4 and contains both new prefixes;
  (d) the list prefix and detail prefix do not cross-match on either
  side (falsifiability anchor against a future "simplify" PR that
  collapses them to a shared `[v1, skills, community]` segment).
- **Modified caller specs** (`SkillsSearchClient.unit.spec.tsx`,
  `SkillDetailClient.unit.spec.tsx`, `skills-store-install-toast.unit.spec.tsx`)
  — removed `readCached*` from hoisted mocks; rewired the
  `cached community → renders synchronously` / `fetch rejects → keeps
  cached detail` tests to seed the test `QueryClient` directly via
  `queryClient.setQueryData(skillsKeys.community*, ...)`, matching the
  shape `syncRestoreCache` would hydrate from the persister.

## Test plan

- [x] `npx tsc --noEmit` clean
- [x] `vitest run` — 403 files / 6160 tests pass
- [x] `pnpm lint` pass
- [x] `pnpm lint:ci` pass
- [x] `bash web/scripts/check-cache-governance-disables-shrink-only.sh` — main 7, HEAD 6, shrink-only ✅
- [ ] Manual staging: skills search + detail still render cached data on
      hard refresh (persister-driven), then background-refetch on mount

## Out of scope (deferred to follow-up PRs)

- **`skills-store.ts` runtime cache → RQ** — Bucket-3 PR-B (concurrent agent)
- **`session-cache.ts` module deletion** — Bucket-3 PR-D (after PR-B + this PR merge; last consumer goes away)
- **Bucket-4 `OPENCLAW_*` event dispatchers** — issue #2000

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [b593229] refactor(web): extract canvasNodeBuilders + finalize #368 F13 (PR-4) (#2034)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T09:43:37Z
- **PR**: #2034

### Commit Message
```
refactor(web): extract canvasNodeBuilders + finalize #368 F13 (PR-4) (#2034)

## Summary

**PR 4/4** — final PR of the F13 god-hook split (issue #368). Extracts
the pure node/edge construction code from \`useCanvasState.ts\` into
**\`canvasNodeBuilders.ts\`** (228 lines, 0 React) and ships the design
spec.

### Builders module

| Function | Caller | Purpose |
|---|---|---|
| \`buildMessageNodes(message, rowY)\` | \`addNodeFromMessage\` | Text +
image + video row layout with sibling-edge chaining and raw-content
fallback |
| \`buildActionImageNodes(message, sourceId, rowY)\` |
\`addNodeFromAction\` | N images all connected from the source node |
| \`buildPlaceholderSplitNodes(message, placeholder, incomingEdges)\` |
\`updatePlaceholderWithResult\` | Multi-media split: position from
placeholder, redirect incoming edges, chain siblings |
| 4 ID generators (\`genTextId\` / \`genImgIdSolo\` / \`genVidIdSolo\` /
\`genResultCardId\`) + \`buildEdge\` | various | Centralized so callers
don't repeat the \`Date.now()\` + random suffix pattern |

### Line counts

| File | Before PR 4 | After PR 4 |
|---|---|---|
| \`useCanvasState.ts\` | 653 | **424** (-229, **-35%**) |
| \`canvasNodeBuilders.ts\` | — | +228 |
| **Cumulative since baseline** | 788 | **-47%** |

### Why 424 vs the 200-line aspirational target

The F13 finding aimed at ≤200 lines. Settled at ~424 — the observed
floor with the F15 D3 decision rule (\"further extraction adds plumbing
without gain\"). What's left:

- 4 sub-hook calls + cross-hook callback wiring (\`useCanvasLayout\` /
\`useCanvasAutoSave\` / \`useCanvasPersistence\` getters / setters)
- Node CRUD (\`addImageNode\` / \`addVideoNode\` / \`addTextNode\` /
\`addEdgesFromSources\` / \`deleteNode\`)
- Placeholder lifecycle (\`addPlaceholderNode\` /
\`updatePlaceholderWithResult\` single-media branch routing + split
delegation / \`updatePlaceholderToError\` / \`removePlaceholderNode\` /
\`convertToLayerEditor\` / \`addImageNodeFromUrl\`)
- \`lastAssistantNodeIdRef\` coordination (D5: stays in main hook)
- The 22-field return shape (D4: surface preservation)

## F13 PR series status

| PR | Result |
|---|---|
| #2016 (PR 0) | Closed/superseded — characterization tests carried by
PR 1's squash; Codex fix carried by PR 2 |
| #2022 (PR 1) | ✅ Merged |
| #2027 (PR 2) | ✅ Merged (race fix included after Codex
\`NEED_HUMAN_REVIEW\`) |
| #2029 (PR 3) | Awaiting merge |
| **This PR (PR 4)** | Ships canvasNodeBuilders + spec doc, F13 closed |

## Design spec


\`docs/superpowers/specs/2026-05-28-issue-368-f13-useCanvasState-refactor.md\`
— full design narrative: D1-D5 decisions, PR walkthrough, bug catches
during refactor (Codex cross-session race; getter-pattern hook
regression), deferred follow-ups.

## Test plan

- [x] PR-0 characterization spec: **49 / 49 unchanged** across all 4
refactor PRs (zero-behavior-change gate)
- [x] New \`canvasNodeBuilders.unit.spec.ts\`: 14 cases (ID-prefix
invariants, geometry math, edge chaining, model-source-of-truth
fallback, placeholder-position propagation, ID uniqueness across single
build)
- [x] \`pnpm --filter @zooclaw/web-app test:unit
tests/unit/canvas-hooks/\` — **182 / 182 green**
- [x] \`pnpm --filter @zooclaw/web-app tsc --noEmit\` clean
- [x] \`pnpm --filter @zooclaw/web-app lint\` clean
- [ ] CI green

Stacked on #2029. Refs #368 F13.

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

**PR 4/4** — final PR of the F13 god-hook split (issue #368). Extracts the pure node/edge construction code from \`useCanvasState.ts\` into **\`canvasNodeBuilders.ts\`** (228 lines, 0 React) and ships the design spec.

### Builders module

| Function | Caller | Purpose |
|---|---|---|
| \`buildMessageNodes(message, rowY)\` | \`addNodeFromMessage\` | Text + image + video row layout with sibling-edge chaining and raw-content fallback |
| \`buildActionImageNodes(message, sourceId, rowY)\` | \`addNodeFromAction\` | N images all connected from the source node |
| \`buildPlaceholderSplitNodes(message, placeholder, incomingEdges)\` | \`updatePlaceholderWithResult\` | Multi-media split: position from placeholder, redirect incoming edges, chain siblings |
| 4 ID generators (\`genTextId\` / \`genImgIdSolo\` / \`genVidIdSolo\` / \`genResultCardId\`) + \`buildEdge\` | various | Centralized so callers don't repeat the \`Date.now()\` + random suffix pattern |

### Line counts

| File | Before PR 4 | After PR 4 |
|---|---|---|
| \`useCanvasState.ts\` | 653 | **424** (-229, **-35%**) |
| \`canvasNodeBuilders.ts\` | — | +228 |
| **Cumulative since baseline** | 788 | **-47%** |

### Why 424 vs the 200-line aspirational target

The F13 finding aimed at ≤200 lines. Settled at ~424 — the observed floor with the F15 D3 decision rule (\"further extraction adds plumbing without gain\"). What's left:

- 4 sub-hook calls + cross-hook callback wiring (\`useCanvasLayout\` / \`useCanvasAutoSave\` / \`useCanvasPersistence\` getters / setters)
- Node CRUD (\`addImageNode\` / \`addVideoNode\` / \`addTextNode\` / \`addEdgesFromSources\` / \`deleteNode\`)
- Placeholder lifecycle (\`addPlaceholderNode\` / \`updatePlaceholderWithResult\` single-media branch routing + split delegation / \`updatePlaceholderToError\` / \`removePlaceholderNode\` / \`convertToLayerEditor\` / \`addImageNodeFromUrl\`)
- \`lastAssistantNodeIdRef\` coordination (D5: stays in main hook)
- The 22-field return shape (D4: surface preservation)

## F13 PR series status

| PR | Result |
|---|---|
| #2016 (PR 0) | Closed/superseded — characterization tests carried by PR 1's squash; Codex fix carried by PR 2 |
| #2022 (PR 1) | ✅ Merged |
| #2027 (PR 2) | ✅ Merged (race fix included after Codex \`NEED_HUMAN_REVIEW\`) |
| #2029 (PR 3) | Awaiting merge |
| **This PR (PR 4)** | Ships canvasNodeBuilders + spec doc, F13 closed |

## Design spec

\`docs/superpowers/specs/2026-05-28-issue-368-f13-useCanvasState-refactor.md\` — full design narrative: D1-D5 decisions, PR walkthrough, bug catches during refactor (Codex cross-session race; getter-pattern hook regression), deferred follow-ups.

## Test plan

- [x] PR-0 characterization spec: **49 / 49 unchanged** across all 4 refactor PRs (zero-behavior-change gate)
- [x] New \`canvasNodeBuilders.unit.spec.ts\`: 14 cases (ID-prefix invariants, geometry math, edge chaining, model-source-of-truth fallback, placeholder-position propagation, ID uniqueness across single build)
- [x] \`pnpm --filter @zooclaw/web-app test:unit tests/unit/canvas-hooks/\` — **182 / 182 green**
- [x] \`pnpm --filter @zooclaw/web-app tsc --noEmit\` clean
- [x] \`pnpm --filter @zooclaw/web-app lint\` clean
- [ ] CI green

Stacked on #2029. Refs #368 F13.

---
## [63c94d6] chore(docs): remove stale docs/features/login-system.md (#2036)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T09:38:51Z
- **PR**: #2036

### Commit Message
```
chore(docs): remove stale docs/features/login-system.md (#2036)

## Summary

- Removes `docs/features/login-system.md` — the sole file in
`docs/features/`, a Jan-2025 placeholder category that never grew.
- Doc had drifted significantly from the code:
- All 6 referenced paths broken (`web/src/lib/auth/*` → actual
`web/app/src/lib/auth/*`, missed during the `web/app/` nested-workspace
restructure).
- Missing ~half the current auth surface (`subscription-storage.ts`,
`ecap-auth.ts`, `login-check.ts`, Mattermost, invite codes, brand-theme
storage, billing-mock backup).
  - Still referred to the project as "Gensmo AI Workspace".
- The code itself is the source of truth and is self-documenting:
`types.ts` defines `STORAGE_KEYS` (the `gensmo:` prefix is a
localStorage compat fact, not stale branding), `manager.ts` has JSDoc'd
login flows on the `AuthManager` singleton, and `tests/unit/lib/auth/`
exercises every public API.
- No file in the repo references `docs/features/` — verified with `grep
-rn "docs/features"` across all sources (zero hits).
- Empty `docs/features/` directory also removed.
- Same disposition as the `docs/development/` cleanup in #2035.

## Follow-up (not in this PR)

`docs/architecture/{api-proxy,backend-integration,design-system}.md` are
in similarly poor shape — all use the pre-`web/app/` paths, mix
architecture with setup/troubleshooting/changelog content, and
`api-proxy.md` ↔ `backend-integration.md` overlap heavily. Worth a
separate cleanup pass. Their only inbound references are
`docs/setup/quick-start.md:148-149` (which is also a Jan-2025 doc and
likely needs review too).

## Test plan

- [ ] `grep -rn "docs/features"` returns empty.
- [ ] CI green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

- Removes `docs/features/login-system.md` — the sole file in `docs/features/`, a Jan-2025 placeholder category that never grew.
- Doc had drifted significantly from the code:
  - All 6 referenced paths broken (`web/src/lib/auth/*` → actual `web/app/src/lib/auth/*`, missed during the `web/app/` nested-workspace restructure).
  - Missing ~half the current auth surface (`subscription-storage.ts`, `ecap-auth.ts`, `login-check.ts`, Mattermost, invite codes, brand-theme storage, billing-mock backup).
  - Still referred to the project as "Gensmo AI Workspace".
- The code itself is the source of truth and is self-documenting: `types.ts` defines `STORAGE_KEYS` (the `gensmo:` prefix is a localStorage compat fact, not stale branding), `manager.ts` has JSDoc'd login flows on the `AuthManager` singleton, and `tests/unit/lib/auth/` exercises every public API.
- No file in the repo references `docs/features/` — verified with `grep -rn "docs/features"` across all sources (zero hits).
- Empty `docs/features/` directory also removed.
- Same disposition as the `docs/development/` cleanup in #2035.

## Follow-up (not in this PR)

`docs/architecture/{api-proxy,backend-integration,design-system}.md` are in similarly poor shape — all use the pre-`web/app/` paths, mix architecture with setup/troubleshooting/changelog content, and `api-proxy.md` ↔ `backend-integration.md` overlap heavily. Worth a separate cleanup pass. Their only inbound references are `docs/setup/quick-start.md:148-149` (which is also a Jan-2025 doc and likely needs review too).

## Test plan

- [ ] `grep -rn "docs/features"` returns empty.
- [ ] CI green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [74f308e] chore(docs): remove stale docs/development/ meta-docs (#2035)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T09:34:22Z
- **PR**: #2035

### Commit Message
```
chore(docs): remove stale docs/development/ meta-docs (#2035)

## Summary

- Removes `docs/development/{CHANGELOG,TODO,AI_DECISIONS}.md` — a
Jan-2025 experimental meta-docs trio that was abandoned (last meaningful
update 2025-01-22), refers to the project under its old "Gensmo AI
Workspace" name, and **self-contradicts** (CHANGELOG marks
Husky/TypeScript-strict as done while TODO lists them as pending).
- No file in the repo references `docs/development/` — verified with
`grep -rn "docs/development"` across all source and docs (zero hits).
- Each file's source-of-truth is already authoritative elsewhere: git
log (changelog), Linear ECA-* issues (TODOs), `docs/superpowers/specs/`
+ PR descriptions (architecture decisions).
- Deleted rather than archived: git history preserves them if anyone
ever needs to look back; keeping them under `docs/` actively misleads
readers (and AI agents) into treating stale snapshots as current state.
- Empty `docs/development/` directory also removed.

## Test plan

- [ ] `grep -rn "docs/development" --exclude-dir=node_modules
--exclude-dir=.next --exclude-dir=.worktrees` returns empty (no broken
inbound links).
- [ ] CI green (no doc-link checker should fire since nothing pointed
here).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

- Removes `docs/development/{CHANGELOG,TODO,AI_DECISIONS}.md` — a Jan-2025 experimental meta-docs trio that was abandoned (last meaningful update 2025-01-22), refers to the project under its old "Gensmo AI Workspace" name, and **self-contradicts** (CHANGELOG marks Husky/TypeScript-strict as done while TODO lists them as pending).
- No file in the repo references `docs/development/` — verified with `grep -rn "docs/development"` across all source and docs (zero hits).
- Each file's source-of-truth is already authoritative elsewhere: git log (changelog), Linear ECA-* issues (TODOs), `docs/superpowers/specs/` + PR descriptions (architecture decisions).
- Deleted rather than archived: git history preserves them if anyone ever needs to look back; keeping them under `docs/` actively misleads readers (and AI agents) into treating stale snapshots as current state.
- Empty `docs/development/` directory also removed.

## Test plan

- [ ] `grep -rn "docs/development" --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=.worktrees` returns empty (no broken inbound links).
- [ ] CI green (no doc-link checker should fire since nothing pointed here).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [86694df] ci(web): add web-build-check (next build compile-only) + README badges split (#2028)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T09:24:55Z
- **PR**: #2028

### Commit Message
```
ci(web): add web-build-check (next build compile-only) + README badges split (#2028)

## Summary

Closes the CI gap that let PR #2013 land a working-tree-broken RSC
import that only surfaced at Deploy ECAP (Staging) on push-to-main (see
hotfix #2023). Two changes bundled:

1. **CI: new `web-build-check` job in `code-quality.yml`** — runs `next
build --experimental-build-mode=compile` on every `web/**` PR.
2. **Docs: README badges layout** — splits the combined Deploy column
(Production + Staging stacked via `<br>`) into two separate columns.

## CI job: measured behaviour

**Measured on workflow_dispatch run
[26565518087](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/26565518087):**

| Aspect | Choice | Measured |
|---|---|---|
| Build mode | `--experimental-build-mode=compile` | **2:00 min
wallclock** (job start 09:08:09 → 09:10:09). Webpack compile itself is
~14s locally; remaining time is checkout + pnpm install + setup-node. |
| PR feedback wallclock impact | Runs in parallel with `web-quality /
test` (2 min) and `web-quality / lint-and-typecheck` (2 min) | **~0** —
`web-build-check` is not the new bottleneck, the parallel slowest is
unchanged at ~2 min. |
| GH Actions cost | `ubuntu-latest-m` (10× multiplier) × 2 min | **+~20
GH-minutes per `web/**` PR push**. ~30 pushes/day → ~18k GH-min/month. |
| Side effects on staging | None | Compile mode skips prerender → no
Firebase / Stripe / R2 API calls. No `wrangler` invocation. No Sentry
release upload (no `SENTRY_AUTH_TOKEN` passed → @sentry/nextjs no-ops
the release, matches existing PR-build behaviour). |
| Production | Untouched | Job uses `.env.staging` only; production
secrets never accessed. |
| What slips through | Prerender-time errors only (e.g. a server
component throwing during static generation) | Accepted: the original
bug class is compile-phase; full prerender would 4-6× PR CI cost.
Revisit if prerender bugs start leaking. |

## Env file generation pattern

Mirrors `deploy.yml` exactly minus deploy-only secrets
(`CLOUDFLARE_API_TOKEN`, etc). Two-step pattern:

1. **Step 1** — quoted-EOF heredoc into `$GITHUB_ENV`. No shell
substitution → any `vars.X` value containing `$(...)` or `$VAR` is
written literally (defends against repo-admin-controlled values being
shell-interpreted).
2. **Step 2** — shell-`${VAR}` heredoc into `.env.staging`, reads from
`env:` block only. No `${{ vars.X }}` interpolation into the heredoc
body.

## Test plan

- [x] **CI dispatch trigger** — `web-build-check` ran clean in 2:00 min
on workflow_dispatch run 26565518087.
- [x] All other `code-quality` sub-jobs (web-quality,
enterprise-admin-quality, claw-interface-quality,
python-duplication-check) stayed green with the new job added to the
aggregator `needs:`.
- [ ] Manual smoke (post-merge, optional): introduce a deliberate RSC
violation in a throwaway branch, push, verify `web-build-check` catches
it. (Not blocking — the trust signal is that compile mode runs webpack's
RSC validator.)

## Why the PR's own paths-filter didn't trigger `web-build-check`

This PR only touches `.github/workflows/` and `README.md`, so the `web`
filter in the `changes` job (which gates `if: needs.changes.outputs.web
== 'true'`) stays false and `web-build-check` is skipped on
`pull_request` events. To validate the job actually runs, I dispatched
it manually via `workflow_dispatch` (which the `if` condition also
accepts). Future workflow-only changes will need the same treatment, or
— separately — the `web` filter could be widened to include
`'.github/workflows/code-quality.yml'`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Body
## Summary

Closes the CI gap that let PR #2013 land a working-tree-broken RSC import that only surfaced at Deploy ECAP (Staging) on push-to-main (see hotfix #2023). Two changes bundled:

1. **CI: new `web-build-check` job in `code-quality.yml`** — runs `next build --experimental-build-mode=compile` on every `web/**` PR.
2. **Docs: README badges layout** — splits the combined Deploy column (Production + Staging stacked via `<br>`) into two separate columns.

## CI job: measured behaviour

**Measured on workflow_dispatch run [26565518087](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/26565518087):**

| Aspect | Choice | Measured |
|---|---|---|
| Build mode | `--experimental-build-mode=compile` | **2:00 min wallclock** (job start 09:08:09 → 09:10:09). Webpack compile itself is ~14s locally; remaining time is checkout + pnpm install + setup-node. |
| PR feedback wallclock impact | Runs in parallel with `web-quality / test` (2 min) and `web-quality / lint-and-typecheck` (2 min) | **~0** — `web-build-check` is not the new bottleneck, the parallel slowest is unchanged at ~2 min. |
| GH Actions cost | `ubuntu-latest-m` (10× multiplier) × 2 min | **+~20 GH-minutes per `web/**` PR push**. ~30 pushes/day → ~18k GH-min/month. |
| Side effects on staging | None | Compile mode skips prerender → no Firebase / Stripe / R2 API calls. No `wrangler` invocation. No Sentry release upload (no `SENTRY_AUTH_TOKEN` passed → @sentry/nextjs no-ops the release, matches existing PR-build behaviour). |
| Production | Untouched | Job uses `.env.staging` only; production secrets never accessed. |
| What slips through | Prerender-time errors only (e.g. a server component throwing during static generation) | Accepted: the original bug class is compile-phase; full prerender would 4-6× PR CI cost. Revisit if prerender bugs start leaking. |

## Env file generation pattern

Mirrors `deploy.yml` exactly minus deploy-only secrets (`CLOUDFLARE_API_TOKEN`, etc). Two-step pattern:

1. **Step 1** — quoted-EOF heredoc into `$GITHUB_ENV`. No shell substitution → any `vars.X` value containing `$(...)` or `$VAR` is written literally (defends against repo-admin-controlled values being shell-interpreted).
2. **Step 2** — shell-`${VAR}` heredoc into `.env.staging`, reads from `env:` block only. No `${{ vars.X }}` interpolation into the heredoc body.

## Test plan

- [x] **CI dispatch trigger** — `web-build-check` ran clean in 2:00 min on workflow_dispatch run 26565518087.
- [x] All other `code-quality` sub-jobs (web-quality, enterprise-admin-quality, claw-interface-quality, python-duplication-check) stayed green with the new job added to the aggregator `needs:`.
- [ ] Manual smoke (post-merge, optional): introduce a deliberate RSC violation in a throwaway branch, push, verify `web-build-check` catches it. (Not blocking — the trust signal is that compile mode runs webpack's RSC validator.)

## Why the PR's own paths-filter didn't trigger `web-build-check`

This PR only touches `.github/workflows/` and `README.md`, so the `web` filter in the `changes` job (which gates `if: needs.changes.outputs.web == 'true'`) stays false and `web-build-check` is skipped on `pull_request` events. To validate the job actually runs, I dispatched it manually via `workflow_dispatch` (which the `if` condition also accepts). Future workflow-only changes will need the same treatment, or — separately — the `web` filter could be widened to include `'.github/workflows/code-quality.yml'`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [4f1dcc0] test(web): characterize skills session-cache + skills-store + community-client (#1999 Phase-0) (#2032)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T09:16:03Z
- **PR**: #2032

### Commit Message
```
test(web): characterize skills session-cache + skills-store + community-client (#1999 Phase-0) (#2032)

## Summary

Phase-0 characterization tests for Bucket-3 (#1999) — extends the
existing 3
session-cache / skills-store / community-client unit specs with **zero
production code change**. Locks current TTL, cache-key format, and
storage-failure-mode behavior so PR-B (skills-store → RQ) and PR-C
(community-client → RQ + delete `session-cache.ts`) have a regression
net.

This PR does **not** close #1999 — it's the prerequisite Phase-0 in the
issue's
Acceptance Criteria. PR-B / PR-C will land separately.

## Scope (zero production change)

| File | Existing | Added | Total |
|---|---:|---:|---:|
| `web/app/tests/unit/lib/storage/session-cache.unit.spec.ts` | 10 | +7
| 17 |
| `web/app/tests/unit/lib/api/skills-store.unit.spec.ts` | 7 | +4 | 11 |
| `web/app/tests/unit/lib/communityClient.unit.spec.ts` | 7 | +5 | 12 |
| **Total** | **24** | **+16** | **40** |

Net diff: +264 / -2 LOC, tests only.

### What the new cases lock

**`session-cache.ts`** — failure-mode + storage-unavailable gaps the
existing
suite did not cover (it had TTL / corrupt / removeByPrefix):
- `writeSessionCache` swallows `QuotaExceededError` from `setItem`
- `readSessionCache` returns `null` when `getItem` itself throws
- `readSessionCache` does not throw when the cleanup `removeItem` also
throws
- Environment without `sessionStorage` (accessor throws): every public
fn no-ops

**`skills-store.ts`** — TTL boundary + literal cache-key + prefix-clear
scope:
- Runtime payload is written under the literal key
  `skills-store:runtime:v3:uid=user-1&eligible=true&verbose=true`
- 5-min TTL boundary: cache hits at 4:59 and expires at 5:01
- `installSkill({ uid: 'user-1' })` only clears entries whose key starts
with
  `…:uid=user-1`, leaving `user-2`'s cache intact

**`community-client.ts`** — list / detail TTL + literal cache-key +
invalid-slug short-circuit:
- List payload written under
  `skills-store:community:list:v1:cursor=page-1&limit=10`
- Detail payload written under
`skills-store:community:detail:v1:valid-skill`
- List 5-min TTL boundary, detail 10-min TTL boundary
- `readCachedCommunitySkillDetail('INVALID SLUG!')` returns `null` and
never
  calls `sessionStorage.getItem`

## What this PR does NOT do (deferred)

- No `useQuery` wrapping — Phase 1 (PR-B for skills-store, PR-C for
  community-client)
- No `session-cache.ts` deletion — PR-C, after all consumers migrate
- No new `PERSIST_ALLOWLIST` / `PERSIST_ALLOWLIST_PREFIXES` entries
- No new `lib/*-cache` imports or `ecap:*:updated` dispatch (R2/R3
shrink-only
  count stays 7=7)

No real bugs were discovered while writing these tests, so no follow-up
issues
were filed.

## Test plan

- [x] `pnpm lint` — pass (web/auth-client/enterprise-admin all clean)
- [x] `npx tsc --noEmit` in `web/app` — exit 0
- [x] `./node_modules/.bin/vitest run` in `web/app` — 402 files, 6155
passed |
      1 todo (16 new cases included, zero regression)
- [x] `pnpm lint:ci` — all ci-lint checks passed (dep-cruise + knip)
- [x] `bash web/scripts/check-cache-governance-disables-shrink-only.sh`
—
      main: 7, HEAD: 7 (unchanged)

## Reference

- #1868 — Bucket roadmap (umbrella)
- #1999 — Bucket-3 issue (this PR is Phase-0 prerequisite, does not
close)
- #1990 — Bucket-1 (persistQueryClient + PERSIST_ALLOWLIST)
- #1998 — Bucket-2 (identity triplet migration)
- #2025 — client cache governance R1/R2/R3 + shrink-only script

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Phase-0 characterization tests for Bucket-3 (#1999) — extends the existing 3
session-cache / skills-store / community-client unit specs with **zero
production code change**. Locks current TTL, cache-key format, and
storage-failure-mode behavior so PR-B (skills-store → RQ) and PR-C
(community-client → RQ + delete `session-cache.ts`) have a regression net.

This PR does **not** close #1999 — it's the prerequisite Phase-0 in the issue's
Acceptance Criteria. PR-B / PR-C will land separately.

## Scope (zero production change)

| File | Existing | Added | Total |
|---|---:|---:|---:|
| `web/app/tests/unit/lib/storage/session-cache.unit.spec.ts` | 10 | +7 | 17 |
| `web/app/tests/unit/lib/api/skills-store.unit.spec.ts` | 7 | +4 | 11 |
| `web/app/tests/unit/lib/communityClient.unit.spec.ts` | 7 | +5 | 12 |
| **Total** | **24** | **+16** | **40** |

Net diff: +264 / -2 LOC, tests only.

### What the new cases lock

**`session-cache.ts`** — failure-mode + storage-unavailable gaps the existing
suite did not cover (it had TTL / corrupt / removeByPrefix):
- `writeSessionCache` swallows `QuotaExceededError` from `setItem`
- `readSessionCache` returns `null` when `getItem` itself throws
- `readSessionCache` does not throw when the cleanup `removeItem` also throws
- Environment without `sessionStorage` (accessor throws): every public fn no-ops

**`skills-store.ts`** — TTL boundary + literal cache-key + prefix-clear scope:
- Runtime payload is written under the literal key
  `skills-store:runtime:v3:uid=user-1&eligible=true&verbose=true`
- 5-min TTL boundary: cache hits at 4:59 and expires at 5:01
- `installSkill({ uid: 'user-1' })` only clears entries whose key starts with
  `…:uid=user-1`, leaving `user-2`'s cache intact

**`community-client.ts`** — list / detail TTL + literal cache-key +
invalid-slug short-circuit:
- List payload written under
  `skills-store:community:list:v1:cursor=page-1&limit=10`
- Detail payload written under `skills-store:community:detail:v1:valid-skill`
- List 5-min TTL boundary, detail 10-min TTL boundary
- `readCachedCommunitySkillDetail('INVALID SLUG!')` returns `null` and never
  calls `sessionStorage.getItem`

## What this PR does NOT do (deferred)

- No `useQuery` wrapping — Phase 1 (PR-B for skills-store, PR-C for
  community-client)
- No `session-cache.ts` deletion — PR-C, after all consumers migrate
- No new `PERSIST_ALLOWLIST` / `PERSIST_ALLOWLIST_PREFIXES` entries
- No new `lib/*-cache` imports or `ecap:*:updated` dispatch (R2/R3 shrink-only
  count stays 7=7)

No real bugs were discovered while writing these tests, so no follow-up issues
were filed.

## Test plan

- [x] `pnpm lint` — pass (web/auth-client/enterprise-admin all clean)
- [x] `npx tsc --noEmit` in `web/app` — exit 0
- [x] `./node_modules/.bin/vitest run` in `web/app` — 402 files, 6155 passed |
      1 todo (16 new cases included, zero regression)
- [x] `pnpm lint:ci` — all ci-lint checks passed (dep-cruise + knip)
- [x] `bash web/scripts/check-cache-governance-disables-shrink-only.sh` —
      main: 7, HEAD: 7 (unchanged)

## Reference

- #1868 — Bucket roadmap (umbrella)
- #1999 — Bucket-3 issue (this PR is Phase-0 prerequisite, does not close)
- #1990 — Bucket-1 (persistQueryClient + PERSIST_ALLOWLIST)
- #1998 — Bucket-2 (identity triplet migration)
- #2025 — client cache governance R1/R2/R3 + shrink-only script

---
## [a73c1f7] refactor(web): remove dead subscription-storage exports (#2001) (#2030)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T09:16:00Z
- **PR**: #2001

### Commit Message
```
refactor(web): remove dead subscription-storage exports (#2001) (#2030)

## Summary

Audit of `web/app/src/lib/auth/subscription-storage.ts` callers per
#2001 found 9 exports with zero production consumers. This PR removes
those dead exports along with the test mocks and self-tests that were
keeping them alive, and documents the module-level decision (keep as
Tier D legitimate storage) in the file header.

Closes #2001.

## Audit result

Module-level decision per the #2001 decision matrix: **partial delete**
— the surviving 5 exports feed real first-paint synchronous reads on hot
paths (SideNav, billing surfaces, `useFreeStatus`) before React Query
has hydrated, plus the `manager.ts` write path on post-login /
post-payment. They land in the spec's Tier D / "per-tab session
continuity" bucket. The dead exports go.

### Removed (9 exports, 0 production callers)

| Export | Why dead |
|---|---|
| `updateSubscriptionInfo` | No callers. `saveSubscriptionInfo` covers
the "write whole record" path; partial updates have no consumer. |
| `clearSubscriptionInfo` | No callers. `clearUserStorage()` wipes the
whole `STORAGE_KEYS` set including `SUBSCRIPTION_INFO`. |
| `hasActiveSubscription` | No callers. The 3 grep hits in
`UserCard.tsx` are a local variable of the same name, not an import.
RQ's `useBillingCredits` exposes `subscriptionStatus`. |
| `getRemainingSubscriptionDays` | No callers.
`computeDaysLeft(trialEndTime / currentPeriodEnd)` covers the live
consumer in `SubscriptionPanel` / `UserMenu` / `SharedPlanCard`. |
| `isSubscriptionExpired` | No callers. `getSubscriptionStatus()`
returns `'expired'` for the same case. |
| `getTeamKey` | No callers. Comment in source already says it "always
returns null" — pre-removed in `useLiteLLMApi` source but the test still
mocked it. |
| `isBillingInitialized` | No callers in source. `useBillingCredits`
reads `subscription_info.billing_initialized` directly. |
| `isInTrial` | No callers. RQ `subscriptionStatus === 'trial'`. |
| `getTrialDaysLeft` | No callers. Same compose:
`computeDaysLeft(trialEndTime)` from `useBillingCredits`. |

### Kept (5 exports, real callers)

| Export | Caller pattern |
|---|---|
| `saveSubscriptionInfo` | `manager.ts::_createAndSyncUser` +
`refreshSubscriptionInfo` (the write path) |
| `getSubscriptionInfo` | `useFreeStatus` (event-driven derive),
`useBillingCredits` (resolve uid + billing_initialized),
`useNavAuthState`, `SubscriptionPanel`, `InvoiceHistory`,
`manager.ts::_doSyncBusinessData` |
| `getSubscriptionStatus` | `CompensationPopup`, `SubscriptionPanel`
(fallback when API status null) |
| `getPlanTier` | `PublicPricingClient`, `SubscriptionPanel` (fallback
when API plan null) |
| `computeDaysLeft` | `SubscriptionPanel`, `SharedPlanCard`,
`CreditsDisplay`, `UserInfoSection`, `UserMenu` — pure helper, lives
here for proximity |

### Stale mocks pruned

- `tests/unit/helpers/mocks.ts::subscriptionStorageDefaults` — drop
`getTeamKey` / `isBillingInitialized` / `clearSubscriptionInfo`
- `tests/unit/hooks/useLiteLLMApi.unit.spec.ts` — drop import +
`mockReturnValue` for `getTeamKey` / `isBillingInitialized` (source no
longer touches them)
- `tests/unit/lib/auth/manager.unit.spec.ts` — drop
`clearSubscriptionInfo` (source uses `clearUserStorage` from
`./storage`)
- `tests/unit/lib/auth/subscription-storage.unit.spec.ts` — drop the 7
dead-export describe blocks; add new coverage for the 3 surviving
fallback helpers (`getSubscriptionStatus`, `getPlanTier`,
`computeDaysLeft`) that previously had none

## Diff size

- Source: 179 → 81 LOC (-98)
- Tests: 230 → 138 LOC (-92), net helper count unchanged (8 → 8 describe
blocks: 2 still cover save/get, 3 new cover the survivors, the rest
gone)
- mocks.ts: -3 lines
- 2 specs: -5 lines total

Net: **256 → 61 LOC (-195)** including 2 specs' inline import/mock
prunes.

## Test plan

- [x] `npx tsc --noEmit` clean
- [x] `pnpm lint` clean (web workspace)
- [x] `pnpm lint:ci` clean (dep-cruiser + knip — knip surfaces no new
unused exports)
- [x] `./node_modules/.bin/vitest run` — 6128 tests pass / 402 files
- [x] `pnpm dup` — 6.02% src duplication (below 7.5% threshold)
- [x] `web/scripts/check-cache-governance-disables-shrink-only.sh` —
R2/R3 disables unchanged (7 → 7, this PR is scoped to
subscription-storage and doesn't touch `lib/*-cache.ts` modules)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---
## [6b9d6f6] feat(web): redesign main Assistant quick commands (#2021)
- **作者**: vincent-srp
- **日期**: 2026-05-28T09:09:27Z
- **PR**: #2021

### Commit Message
```
feat(web): redesign main Assistant quick commands (#2021)

## Linear
[ECA-711: \[ZooClaw Web\] Agent new chat 体验完善:可配置快捷指令区 + Specialist
开场选项](https://linear.app/srpone/issue/ECA-711/zooclaw-web-agent-new-chat-体验完善可配置快捷指令区-specialist-开场选项)

## Summary
- 把 main Assistant 快捷指令从通用 `plan` / `draft` / `summarize` 改为贴合「ZooClaw
导览者」人设的四条：**Impress me** / **Find a specialist** / **Review my team** /
**How ZooClaw works**（依据 `main-agent-workspace` 的
IDENTITY/SOUL：导览者的核心价值是帮用户找 Specialist、管理 Team）
- `impressMe` 为激活/aha 项：基于对用户已有了解（必要时先认识用户，Bootstrap
式——给原则不限定问题数）解决一件有意义但不复杂、最好当场完成的任务，并借此展现导览者独特能力
- 四条仍走「发消息」机制，零结构变更，`MAX_QUICK_COMMAND_COUNT = 4` 正好匹配；不动
Clear/Compress/Tips 与 per-agent 配置路径
- 全 10 语言文案同步 + 新增 locale 完整性守卫测试（防某语言漏键回退英文）；英文 label 用 sentence case
- 修复 quick-action tooltip：用 `text-wrap` 覆盖 ds tooltip 自带的
`text-balance`，消除长 prompt 预览的右侧均匀留白（保留 ds 的 `w-fit`，加 `max-w-xs` 上限）
-
设计/实现文档：`docs/superpowers/specs/2026-05-28-main-assistant-quick-commands-design.md`、`docs/superpowers/plans/2026-05-28-main-assistant-quick-commands.md`

## Test plan
- [x] 单测：`ChatQuickActions.unit.spec.tsx`（四条渲染 + 点击发送对应 prompt）+
`locales/index.unit.spec.ts`（10 语言均含四键、非空）——17 passed
- [ ] 手测：`/chat` 主对话 Quick start 四条 label/顺序、切换 ZH、点击发送、tooltip 观感
- [ ] 8 种非中英文翻译（de/es/fr/it/pt/ja/ko/ar）母语 tone 复核

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Linear
[ECA-711: \[ZooClaw Web\] Agent new chat 体验完善:可配置快捷指令区 + Specialist 开场选项](https://linear.app/srpone/issue/ECA-711/zooclaw-web-agent-new-chat-体验完善可配置快捷指令区-specialist-开场选项)

## Summary
- 把 main Assistant 快捷指令从通用 `plan` / `draft` / `summarize` 改为贴合「ZooClaw 导览者」人设的四条：**Impress me** / **Find a specialist** / **Review my team** / **How ZooClaw works**（依据 `main-agent-workspace` 的 IDENTITY/SOUL：导览者的核心价值是帮用户找 Specialist、管理 Team）
- `impressMe` 为激活/aha 项：基于对用户已有了解（必要时先认识用户，Bootstrap 式——给原则不限定问题数）解决一件有意义但不复杂、最好当场完成的任务，并借此展现导览者独特能力
- 四条仍走「发消息」机制，零结构变更，`MAX_QUICK_COMMAND_COUNT = 4` 正好匹配；不动 Clear/Compress/Tips 与 per-agent 配置路径
- 全 10 语言文案同步 + 新增 locale 完整性守卫测试（防某语言漏键回退英文）；英文 label 用 sentence case
- 修复 quick-action tooltip：用 `text-wrap` 覆盖 ds tooltip 自带的 `text-balance`，消除长 prompt 预览的右侧均匀留白（保留 ds 的 `w-fit`，加 `max-w-xs` 上限）
- 设计/实现文档：`docs/superpowers/specs/2026-05-28-main-assistant-quick-commands-design.md`、`docs/superpowers/plans/2026-05-28-main-assistant-quick-commands.md`

## Test plan
- [x] 单测：`ChatQuickActions.unit.spec.tsx`（四条渲染 + 点击发送对应 prompt）+ `locales/index.unit.spec.ts`（10 语言均含四键、非空）——17 passed
- [ ] 手测：`/chat` 主对话 Quick start 四条 label/顺序、切换 ZH、点击发送、tooltip 观感
- [ ] 8 种非中英文翻译（de/es/fr/it/pt/ja/ko/ar）母语 tone 复核

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [98c76f4] refactor(web): extract useCanvasAutoSave (#368 F13 PR-2) (#2027)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T09:04:54Z
- **PR**: #2027

### Commit Message
```
refactor(web): extract useCanvasAutoSave (#368 F13 PR-2) (#2027)

## Summary

**PR 2/4** of the F13 god-hook split (issue #368). Extracts the
debounced version-controlled autosave from \`useCanvasState.ts\` into
**\`useCanvasAutoSave.ts\`** (83 lines).

This PR carries **two changes** after the rebase onto main:
1. **Spec follow-up from Codex review on PR #2016** (commit
\`409162766\`) — addresses 2 vacuous-assertion findings flagged by Codex
on the now-closed characterization PR. The PR #2016 was superseded when
PR #2022 squash-merged its content to main; that squash predated the
Codex fix, so the fix carries forward here.
2. **The actual PR-2 refactor** (commit \`a28a45032\`) — extracts
\`useCanvasAutoSave\`.

### Hook responsibilities

\`useCanvasAutoSave\` owns:
- \`versionRef\` — optimistic write-version counter
- \`saveTimerRef\` — 2 000 ms debounce handle
- \`scheduleSave\` — cancel + reschedule on every nodes / edges mutation
- Trigger \`useEffect\` (fires when either array changes)

Exposes \`setVersion(v)\` and \`resetVersion()\` so the consuming hook
can restore version on load and zero it on clear without touching the
ref directly. Same getter pattern as \`useCanvasLayout\` (D3 in F15
spec) — accepts \`getNodes\` / \`getEdges\` callbacks, stabilizes via
refs so its outputs keep referential identity across parent re-renders.

### Line counts

| File | Before PR 2 | After PR 2 |
|---|---|---|
| \`useCanvasState.ts\` | 707 | **680** (-27 net; ~50 lines moved out +
boilerplate wiring) |
| \`useCanvasAutoSave.ts\` | — | +83 |

PR 3 (extract \`useCanvasPersistence\` for load / reset / clearCanvas)
will land next.

## Test plan

- [x] PR-0 characterization spec: **49 / 49 unchanged**
(zero-behavior-change gate)
- [x] New \`useCanvasAutoSave.unit.spec.ts\`: 13 cases (debounce timing
/ readonly + null-session + empty-uid suppression / rapid-change
collapse / failed-save version-stay / \`setVersion\` biasing /
\`resetVersion\` zeroing / live-getter snapshot / stable callback
identity)
- [x] \`pnpm --filter @zooclaw/web-app test:unit
tests/unit/canvas-hooks/\` — 153 / 153 green
- [x] \`pnpm --filter @zooclaw/web-app tsc --noEmit\` clean
- [x] \`pnpm --filter @zooclaw/web-app lint\` clean
- [ ] CI green

Refs #368 F13. Supersedes #2016.

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

**PR 2/4** of the F13 god-hook split (issue #368). Extracts the debounced version-controlled autosave from \`useCanvasState.ts\` into **\`useCanvasAutoSave.ts\`** (83 lines).

This PR carries **two changes** after the rebase onto main:
1. **Spec follow-up from Codex review on PR #2016** (commit \`409162766\`) — addresses 2 vacuous-assertion findings flagged by Codex on the now-closed characterization PR. The PR #2016 was superseded when PR #2022 squash-merged its content to main; that squash predated the Codex fix, so the fix carries forward here.
2. **The actual PR-2 refactor** (commit \`a28a45032\`) — extracts \`useCanvasAutoSave\`.

### Hook responsibilities

\`useCanvasAutoSave\` owns:
- \`versionRef\` — optimistic write-version counter
- \`saveTimerRef\` — 2 000 ms debounce handle
- \`scheduleSave\` — cancel + reschedule on every nodes / edges mutation
- Trigger \`useEffect\` (fires when either array changes)

Exposes \`setVersion(v)\` and \`resetVersion()\` so the consuming hook can restore version on load and zero it on clear without touching the ref directly. Same getter pattern as \`useCanvasLayout\` (D3 in F15 spec) — accepts \`getNodes\` / \`getEdges\` callbacks, stabilizes via refs so its outputs keep referential identity across parent re-renders.

### Line counts

| File | Before PR 2 | After PR 2 |
|---|---|---|
| \`useCanvasState.ts\` | 707 | **680** (-27 net; ~50 lines moved out + boilerplate wiring) |
| \`useCanvasAutoSave.ts\` | — | +83 |

PR 3 (extract \`useCanvasPersistence\` for load / reset / clearCanvas) will land next.

## Test plan

- [x] PR-0 characterization spec: **49 / 49 unchanged** (zero-behavior-change gate)
- [x] New \`useCanvasAutoSave.unit.spec.ts\`: 13 cases (debounce timing / readonly + null-session + empty-uid suppression / rapid-change collapse / failed-save version-stay / \`setVersion\` biasing / \`resetVersion\` zeroing / live-getter snapshot / stable callback identity)
- [x] \`pnpm --filter @zooclaw/web-app test:unit tests/unit/canvas-hooks/\` — 153 / 153 green
- [x] \`pnpm --filter @zooclaw/web-app tsc --noEmit\` clean
- [x] \`pnpm --filter @zooclaw/web-app lint\` clean
- [ ] CI green

Refs #368 F13. Supersedes #2016.

---
## [0996697] ci(arch-review): add cohort-issues helper scripts + pytest (#2019)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T08:53:27Z
- **PR**: #2019

### Commit Message
```
ci(arch-review): add cohort-issues helper scripts + pytest (#2019)

## Summary

PR 2 of 3 for the arch-review cohort-issues rollout. Design spec:
[`docs/superpowers/specs/2026-05-28-arch-review-cohort-issues.md`](docs/superpowers/specs/2026-05-28-arch-review-cohort-issues.md)
(merged in #2015).

This PR adds 6 stdlib-only Python scripts under
`.github/scripts/arch-review/` plus pytest tests. **Scripts are not yet
wired into `claude-arch-review.yaml`** — PR 3 will replace the inline
Python compose step with calls to these. Merging this PR has zero
runtime effect on the weekly cron.

## What ships

| File | Purpose |
|---|---|
| `_parse.py` | Shared regex helpers: ARCH_REVIEW markers, finding-block
split, NEXT_ID counter, resolved-bullet round-trip |
| `compose_baseline.py` | Aggregate `gh issue list` JSON →
`prior_body.md` + `fid_to_issue.json` + `next_id.txt` |
| `reconcile.py` | `findings.md` vs baseline → `new_findings.md` +
`resolutions.json` + `summary.md` (lossless on missing F-IDs) |
| `mark_resolved.py` | Move one or more F-ID blocks from FINDINGS to
RESOLVED on a single issue body |
| `count_active.py` | Parse active finding count from issue body (used
by close-when-empty logic) |
| `compose_new.py` | Assemble new cohort issue body w/ NEXT_ID marker +
cross-link list |
| `validate_schema.py` | Enforce new (Priority/Impact/Effort) or legacy
(Severity) schema; lenient mode for baseline parsing |

Plus `.github/workflows/arch-review-scripts-test.yml` — path-filtered
pytest runner on `.github/scripts/arch-review/**`.

## Test coverage

61 unit tests cover:

- All 4 decision-table branches of `reconcile` (no-change / new-only /
resolved-only / mixed)
- Edge cases: contradicted (F-ID in BOTH active and resolved), unknown
resolved F-ID, missing markers
- `mark_resolved` round-trip: bullet output must match
`RESOLVED_BULLET_RE` parser regex (otherwise next run can't read it)
- Manual suffix preservation across resolution
- Duplicate F-ID across two open issues (lower issue number wins)
- NEXT_ID computation with NEXT_ID marker present vs absent (fallback to
max F-ID + 1)
- Schema validation: missing fields, bad values, legacy/new shape
coexistence

Local: `cd .github/scripts/arch-review && pytest tests/ -v` → 61 passed
in 0.18s.

## Diff stats (excl. generated)

- business code: +0 / -3 (.gitignore tweak only)
- test code: +907 / 0 (8 files)
- ci/tooling: +1012 / 0 (scripts + workflow)

Tests are independent, no cross-PR dependency.

## Test plan

- [x] All 61 pytest tests pass locally
- [x] `ruff format --check` clean on all 15 Python files
- [x] `ruff check` clean
- [ ] CI workflow `arch-review scripts` runs and passes on this PR
- [ ] Code review (per `feedback_codex_contract_review` — fixture/script
PRs expect 4-5 contract rounds)

## Next

**PR 3**: `.github/workflows/claude-arch-review.yaml` rewrite — swap
inline 200-line Python for calls to these scripts, update
`.agents/skills/arch-review/SKILL.md` +
`.claude/commands/arch-review.md` for new Priority/Impact/Effort schema,
add `workflow_dispatch dry_run` mode.

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

PR 2 of 3 for the arch-review cohort-issues rollout. Design spec: [`docs/superpowers/specs/2026-05-28-arch-review-cohort-issues.md`](docs/superpowers/specs/2026-05-28-arch-review-cohort-issues.md) (merged in #2015).

This PR adds 6 stdlib-only Python scripts under `.github/scripts/arch-review/` plus pytest tests. **Scripts are not yet wired into `claude-arch-review.yaml`** — PR 3 will replace the inline Python compose step with calls to these. Merging this PR has zero runtime effect on the weekly cron.

## What ships

| File | Purpose |
|---|---|
| `_parse.py` | Shared regex helpers: ARCH_REVIEW markers, finding-block split, NEXT_ID counter, resolved-bullet round-trip |
| `compose_baseline.py` | Aggregate `gh issue list` JSON → `prior_body.md` + `fid_to_issue.json` + `next_id.txt` |
| `reconcile.py` | `findings.md` vs baseline → `new_findings.md` + `resolutions.json` + `summary.md` (lossless on missing F-IDs) |
| `mark_resolved.py` | Move one or more F-ID blocks from FINDINGS to RESOLVED on a single issue body |
| `count_active.py` | Parse active finding count from issue body (used by close-when-empty logic) |
| `compose_new.py` | Assemble new cohort issue body w/ NEXT_ID marker + cross-link list |
| `validate_schema.py` | Enforce new (Priority/Impact/Effort) or legacy (Severity) schema; lenient mode for baseline parsing |

Plus `.github/workflows/arch-review-scripts-test.yml` — path-filtered pytest runner on `.github/scripts/arch-review/**`.

## Test coverage

61 unit tests cover:

- All 4 decision-table branches of `reconcile` (no-change / new-only / resolved-only / mixed)
- Edge cases: contradicted (F-ID in BOTH active and resolved), unknown resolved F-ID, missing markers
- `mark_resolved` round-trip: bullet output must match `RESOLVED_BULLET_RE` parser regex (otherwise next run can't read it)
- Manual suffix preservation across resolution
- Duplicate F-ID across two open issues (lower issue number wins)
- NEXT_ID computation with NEXT_ID marker present vs absent (fallback to max F-ID + 1)
- Schema validation: missing fields, bad values, legacy/new shape coexistence

Local: `cd .github/scripts/arch-review && pytest tests/ -v` → 61 passed in 0.18s.

## Diff stats (excl. generated)

- business code: +0 / -3 (.gitignore tweak only)
- test code: +907 / 0 (8 files)
- ci/tooling: +1012 / 0 (scripts + workflow)

Tests are independent, no cross-PR dependency.

## Test plan

- [x] All 61 pytest tests pass locally
- [x] `ruff format --check` clean on all 15 Python files
- [x] `ruff check` clean
- [ ] CI workflow `arch-review scripts` runs and passes on this PR
- [ ] Code review (per `feedback_codex_contract_review` — fixture/script PRs expect 4-5 contract rounds)

## Next

**PR 3**: `.github/workflows/claude-arch-review.yaml` rewrite — swap inline 200-line Python for calls to these scripts, update `.agents/skills/arch-review/SKILL.md` + `.claude/commands/arch-review.md` for new Priority/Impact/Effort schema, add `workflow_dispatch dry_run` mode.

---
## [7c8b8b9] chore(web): add client cache governance rules (#2002 + #2003) (#2025)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T08:50:21Z
- **PR**: #2025

### Commit Message
```
chore(web): add client cache governance rules (#2002 + #2003) (#2025)

## Summary

Lock in the post-#1868 cache-storage contract with **documentation +
ESLint enforcement** so the manual `sessionStorage` / `lib/*-cache.ts` /
`ecap:*:updated` patterns the `persistQueryClient` migration replaced
cannot regress silently.

Combines two follow-up issues:
- Closes #2002 — `web/app/AGENTS.md` 客户端缓存规范
- Closes #2003 — ESLint R1 / R2 / R3 防回潮规则

## What changes

### 1. `web/app/AGENTS.md` — new "Client cache & storage (post-#1868)"
section
Defines the three hard rules + the Tier C/D legitimate-storage table +
the logout / account-switch invariant. Placed between "Data Fetching"
and "Observability".

### 2. `web/app/eslint.config.mjs` — three new rules
- **R1** (`no-restricted-syntax`): bans `setItem` inside a
`Property[key.name="queryFn"]` — the root cause of the PR #1865 r1
cross-session leak.
- **R2** (`no-restricted-imports`): bans `**/lib/**/*-cache` imports
outside the existing 5 violators.
- **R3** (`no-restricted-syntax`): bans `window.dispatchEvent(new
(CustomEvent|Event)('ecap:*:updated'))` — the deprecated cross-hook
fanout pattern.

All three are mirrored in **Block 1c** so SRC_BLOCK1_IGNORES (raw-fetch
carve-out) can't silently exempt `lib/api/skills-store.ts` /
`lib/skills/community-client.ts`.

### 3. 7 current violators tagged with inline disables
Each `eslint-disable-next-line` carries a `TODO(#1868 | #1999 | #2000 |
#2001)` referencing the migration issue. Distribution:

| Rule | Files | Migration issue |
|---|---|---|
| R2 | `MattermostProvider.tsx`, `UserBusinessDataContext.tsx` | #2001
(Bucket-2 follow-up) |
| R2 | `use-cases.ts` (agent-catalog-cache sync shim) | #1868 |
| R2 | `skills-store.ts`, `community-client.ts` | #1999 (Bucket-3) |
| R3 | `useOpenClawInit.ts`, `useUserAgents.ts` | #2000 (Bucket-4) |

### 4. Shrink-only CI guard
`web/scripts/check-cache-governance-disables-shrink-only.sh` counts the
inline disables and fails CI if HEAD has more than `origin/main` — so a
future PR cannot bypass the rules by stamping on a new disable comment.
Wired into `code-quality.yml` `pre_lint_scripts` alongside the existing
4 shrink-only scripts.

### 5. Spec doc fix
`docs/superpowers/specs/2026-05-27-rq-persist-client-evaluation.md`
previously claimed `PersistQueryClientProvider` subscribes to the
`storage` event for cross-tab sync — corrected (persister writes only,
never reads). Cross-tab tracked in #1997.

## Test plan
- [x] `pnpm lint` clean (root → app + auth-client + enterprise-admin)
- [x] `npx tsc --noEmit` clean
- [x] `./node_modules/.bin/vitest run` — 400 files / 6076 tests / 1
todo, all green
- [x] `pnpm lint:ci` clean (dep-cruise + knip)
- [x] Shrink-only script bootstrap mode verified locally: HEAD=7, main=0
→ "bootstrap PR; skipping" + exit 0. Once this PR merges, subsequent PRs
are checked against count=7.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Body
## Summary

Lock in the post-#1868 cache-storage contract with **documentation + ESLint enforcement** so the manual `sessionStorage` / `lib/*-cache.ts` / `ecap:*:updated` patterns the `persistQueryClient` migration replaced cannot regress silently.

Combines two follow-up issues:
- Closes #2002 — `web/app/AGENTS.md` 客户端缓存规范
- Closes #2003 — ESLint R1 / R2 / R3 防回潮规则

## What changes

### 1. `web/app/AGENTS.md` — new "Client cache & storage (post-#1868)" section
Defines the three hard rules + the Tier C/D legitimate-storage table + the logout / account-switch invariant. Placed between "Data Fetching" and "Observability".

### 2. `web/app/eslint.config.mjs` — three new rules
- **R1** (`no-restricted-syntax`): bans `setItem` inside a `Property[key.name="queryFn"]` — the root cause of the PR #1865 r1 cross-session leak.
- **R2** (`no-restricted-imports`): bans `**/lib/**/*-cache` imports outside the existing 5 violators.
- **R3** (`no-restricted-syntax`): bans `window.dispatchEvent(new (CustomEvent|Event)('ecap:*:updated'))` — the deprecated cross-hook fanout pattern.

All three are mirrored in **Block 1c** so SRC_BLOCK1_IGNORES (raw-fetch carve-out) can't silently exempt `lib/api/skills-store.ts` / `lib/skills/community-client.ts`.

### 3. 7 current violators tagged with inline disables
Each `eslint-disable-next-line` carries a `TODO(#1868 | #1999 | #2000 | #2001)` referencing the migration issue. Distribution:

| Rule | Files | Migration issue |
|---|---|---|
| R2 | `MattermostProvider.tsx`, `UserBusinessDataContext.tsx` | #2001 (Bucket-2 follow-up) |
| R2 | `use-cases.ts` (agent-catalog-cache sync shim) | #1868 |
| R2 | `skills-store.ts`, `community-client.ts` | #1999 (Bucket-3) |
| R3 | `useOpenClawInit.ts`, `useUserAgents.ts` | #2000 (Bucket-4) |

### 4. Shrink-only CI guard
`web/scripts/check-cache-governance-disables-shrink-only.sh` counts the inline disables and fails CI if HEAD has more than `origin/main` — so a future PR cannot bypass the rules by stamping on a new disable comment. Wired into `code-quality.yml` `pre_lint_scripts` alongside the existing 4 shrink-only scripts.

### 5. Spec doc fix
`docs/superpowers/specs/2026-05-27-rq-persist-client-evaluation.md` previously claimed `PersistQueryClientProvider` subscribes to the `storage` event for cross-tab sync — corrected (persister writes only, never reads). Cross-tab tracked in #1997.

## Test plan
- [x] `pnpm lint` clean (root → app + auth-client + enterprise-admin)
- [x] `npx tsc --noEmit` clean
- [x] `./node_modules/.bin/vitest run` — 400 files / 6076 tests / 1 todo, all green
- [x] `pnpm lint:ci` clean (dep-cruise + knip)
- [x] Shrink-only script bootstrap mode verified locally: HEAD=7, main=0 → "bootstrap PR; skipping" + exit 0. Once this PR merges, subsequent PRs are checked against count=7.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [e87b43b] fix(web): split useAgentDescription out to client-only module (#2013 hotfix) (#2023)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T08:49:15Z
- **PR**: #2023

### Commit Message
```
fix(web): split useAgentDescription out to client-only module (#2013 hotfix) (#2023)

## Summary

**Hotfix** — restores Deploy ECAP (Staging) which has been red on every
push to main since 9c77ccef8 ([Deploy ECAP
run](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/26562676284)).

PR #2013 introduced `lib/agent-description-store.ts` with
`useSyncExternalStore` at the top of the file and no `'use client'`
directive. It gets pulled into the server bundle via this import chain:

```
share/[shareId]/page.tsx  (RSC default)
  → chat-replay-api.ts
    → auth-headers.ts
      → auth/storage.ts            (PR #2013 added `import { clearAgentDescriptions }` here)
        → agent-description-store.ts   (PR #2013 new file, uses useSyncExternalStore)
```

`next build` webpack errors out:

> ./src/lib/agent-description-store.ts
> Error: You're importing a component that needs `useSyncExternalStore`.
This React Hook only works in a Client Component.

## Why all PR checks passed on #2013

`lint` / `tsc --noEmit` / `pnpm test:unit` do not enforce App Router RSC
client/server boundaries — only `next build` (production webpack
bundling) does. The CI gap is being tracked separately; this PR is the
hotfix.

## Fix

Split the React surface into a sibling `'use client'` file
`lib/useAgentDescription.ts`. The pure-data API (`getAgentDescription` /
`setAgentDescription` / `clearAgentDescriptions` /
`subscribeAgentDescriptions`) stays in `agent-description-store.ts` with
**no `react` import**, so it remains safe to import from
`auth/storage.ts` on the server side. Only `useChatIdentity.ts` (already
`'use client'`) needs its import path updated.

| File | Change |
|------|--------|
| `web/app/src/lib/agent-description-store.ts` | Remove
`useSyncExternalStore` import + `useAgentDescription` hook. Pure data +
`subscribeAgentDescriptions` remain. |
| `web/app/src/lib/useAgentDescription.ts` | **New** — `'use client'`,
hosts the hook. |
| `web/app/src/app/[locale]/chat/hooks/useChatIdentity.ts` | Switch
import path to `@/lib/useAgentDescription`. |
| `web/app/tests/unit/lib/agent-description-store.unit.spec.ts` | Switch
`useAgentDescription` import to the new file; other API imports
unchanged. |

## Test plan

- [x] `pnpm exec dotenv -e .env.staging -- next build` — `✓ Compiled
successfully` (the RSC error is gone)
- [x] `pnpm test:unit` — 6076/6076 ✓ (1 todo)
- [ ] Post-merge: Deploy ECAP (Staging) goes green
- [ ] Manual on staging: edit agent description in chat-side settings
panel → chat header re-renders without page reload (regression coverage
for the Codex finding on #2013 that motivated `useSyncExternalStore` in
the first place)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

**Hotfix** — restores Deploy ECAP (Staging) which has been red on every push to main since 9c77ccef8 ([Deploy ECAP run](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/26562676284)).

PR #2013 introduced `lib/agent-description-store.ts` with `useSyncExternalStore` at the top of the file and no `'use client'` directive. It gets pulled into the server bundle via this import chain:

```
share/[shareId]/page.tsx  (RSC default)
  → chat-replay-api.ts
    → auth-headers.ts
      → auth/storage.ts            (PR #2013 added `import { clearAgentDescriptions }` here)
        → agent-description-store.ts   (PR #2013 new file, uses useSyncExternalStore)
```

`next build` webpack errors out:

> ./src/lib/agent-description-store.ts
> Error: You're importing a component that needs `useSyncExternalStore`. This React Hook only works in a Client Component.

## Why all PR checks passed on #2013

`lint` / `tsc --noEmit` / `pnpm test:unit` do not enforce App Router RSC client/server boundaries — only `next build` (production webpack bundling) does. The CI gap is being tracked separately; this PR is the hotfix.

## Fix

Split the React surface into a sibling `'use client'` file `lib/useAgentDescription.ts`. The pure-data API (`getAgentDescription` / `setAgentDescription` / `clearAgentDescriptions` / `subscribeAgentDescriptions`) stays in `agent-description-store.ts` with **no `react` import**, so it remains safe to import from `auth/storage.ts` on the server side. Only `useChatIdentity.ts` (already `'use client'`) needs its import path updated.

| File | Change |
|------|--------|
| `web/app/src/lib/agent-description-store.ts` | Remove `useSyncExternalStore` import + `useAgentDescription` hook. Pure data + `subscribeAgentDescriptions` remain. |
| `web/app/src/lib/useAgentDescription.ts` | **New** — `'use client'`, hosts the hook. |
| `web/app/src/app/[locale]/chat/hooks/useChatIdentity.ts` | Switch import path to `@/lib/useAgentDescription`. |
| `web/app/tests/unit/lib/agent-description-store.unit.spec.ts` | Switch `useAgentDescription` import to the new file; other API imports unchanged. |

## Test plan

- [x] `pnpm exec dotenv -e .env.staging -- next build` — `✓ Compiled successfully` (the RSC error is gone)
- [x] `pnpm test:unit` — 6076/6076 ✓ (1 todo)
- [ ] Post-merge: Deploy ECAP (Staging) goes green
- [ ] Manual on staging: edit agent description in chat-side settings panel → chat header re-renders without page reload (regression coverage for the Codex finding on #2013 that motivated `useSyncExternalStore` in the first place)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [23f593d] refactor(web): extract canvasLayoutUtils + useCanvasLayout (#368 F13 PR-1) (#2022)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T08:39:57Z
- **PR**: #2022

### Commit Message
```
refactor(web): extract canvasLayoutUtils + useCanvasLayout (#368 F13 PR-1) (#2022)

## Summary

**PR 1/4** of the F13 god-hook split (issue #368). Extracts the swimlane
layout algorithm from \`useCanvasState.ts\` into:

- **\`canvasLayoutUtils.ts\`** (pure helpers, 59 lines): geometry
constants (\`LEFT_MARGIN\` / \`TOP_MARGIN\` / \`NODE_WIDTH\` /
\`COL_GAP\` / \`ROW_GAP\` / \`NODE_HEIGHT_ESTIMATE\`),
\`hasOverlap(nodes, candidate)\`, \`findChildPosition(nodes, sourceNode,
direction)\`.

- **\`useCanvasLayout.ts\`** (stateful hook, 68 lines): owns
\`nextRowYRef\`; exposes \`recalcNextRowY\` / \`getNextNodePosition\` /
\`resetLayout\` / \`findChildPositionFromNodes\`.

### Getter pattern (D3 from F15 useMattermost spec)

\`useCanvasLayout\` accepts a \`getNodes\` callback, then **stabilizes
it via a ref** so its own outputs keep referential identity across
parent re-renders. This invariant is critical — without it the
consumer's load \`useEffect\` retriggers on every render, doubling
\`loadCanvasState\` calls. Caught by the PR-0 \`loadedRef\`
characterization test on the first attempt; fix is the ref-stabilized
getter.

### Line counts

| File | Before | After |
|---|---|---|
| \`useCanvasState.ts\` | 788 | **707** (-81, -10%) |
| \`canvasLayoutUtils.ts\` | — | +59 |
| \`useCanvasLayout.ts\` | — | +68 |

PR 2/3/4 land the remaining extractions (autosave / persistence) to
reach the ~250 floor.

## Test plan

- [x] PR-0 characterization spec: **49/49 unchanged**
(zero-behavior-change gate)
- [x] New \`canvasLayoutUtils.unit.spec.ts\`: 12 cases (constants +
\`hasOverlap\` + \`findChildPosition\` directions)
- [x] New \`useCanvasLayout.unit.spec.ts\`: 8 cases (start state /
advance / recalc / reset / live-getter / **stable callback identity
invariant**)
- [x] \`pnpm --filter @zooclaw/web-app test:unit
tests/unit/canvas-hooks/\` — 140/140 green
- [x] \`pnpm --filter @zooclaw/web-app tsc --noEmit\` clean
- [x] \`pnpm --filter @zooclaw/web-app lint\` clean
- [ ] CI green

## Notes for reviewer

Stacked on #2016. Merge order: #2016 → this PR. Base will auto-retarget
to \`main\` once #2016 lands; I'll rebase if needed.

Refs #368 F13.

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

**PR 1/4** of the F13 god-hook split (issue #368). Extracts the swimlane layout algorithm from \`useCanvasState.ts\` into:

- **\`canvasLayoutUtils.ts\`** (pure helpers, 59 lines): geometry constants (\`LEFT_MARGIN\` / \`TOP_MARGIN\` / \`NODE_WIDTH\` / \`COL_GAP\` / \`ROW_GAP\` / \`NODE_HEIGHT_ESTIMATE\`), \`hasOverlap(nodes, candidate)\`, \`findChildPosition(nodes, sourceNode, direction)\`.

- **\`useCanvasLayout.ts\`** (stateful hook, 68 lines): owns \`nextRowYRef\`; exposes \`recalcNextRowY\` / \`getNextNodePosition\` / \`resetLayout\` / \`findChildPositionFromNodes\`.

### Getter pattern (D3 from F15 useMattermost spec)

\`useCanvasLayout\` accepts a \`getNodes\` callback, then **stabilizes it via a ref** so its own outputs keep referential identity across parent re-renders. This invariant is critical — without it the consumer's load \`useEffect\` retriggers on every render, doubling \`loadCanvasState\` calls. Caught by the PR-0 \`loadedRef\` characterization test on the first attempt; fix is the ref-stabilized getter.

### Line counts

| File | Before | After |
|---|---|---|
| \`useCanvasState.ts\` | 788 | **707** (-81, -10%) |
| \`canvasLayoutUtils.ts\` | — | +59 |
| \`useCanvasLayout.ts\` | — | +68 |

PR 2/3/4 land the remaining extractions (autosave / persistence) to reach the ~250 floor.

## Test plan

- [x] PR-0 characterization spec: **49/49 unchanged** (zero-behavior-change gate)
- [x] New \`canvasLayoutUtils.unit.spec.ts\`: 12 cases (constants + \`hasOverlap\` + \`findChildPosition\` directions)
- [x] New \`useCanvasLayout.unit.spec.ts\`: 8 cases (start state / advance / recalc / reset / live-getter / **stable callback identity invariant**)
- [x] \`pnpm --filter @zooclaw/web-app test:unit tests/unit/canvas-hooks/\` — 140/140 green
- [x] \`pnpm --filter @zooclaw/web-app tsc --noEmit\` clean
- [x] \`pnpm --filter @zooclaw/web-app lint\` clean
- [ ] CI green

## Notes for reviewer

Stacked on #2016. Merge order: #2016 → this PR. Base will auto-retarget to \`main\` once #2016 lands; I'll rebase if needed.

Refs #368 F13.

---
## [8e589aa] refactor(web): move channel setup wizards under channels/ (#368 F14) (#2024)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T08:38:15Z
- **PR**: #2024

### Commit Message
```
refactor(web): move channel setup wizards under channels/ (#368 F14) (#2024)

## Summary

PR 2 of 2 for
[#368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368)
F14. `git mv` the 6 existing platform setup wizards into the new
`channels/` directory created in PR #2018, so the
`claw-settings/components/` root no longer mixes section components with
wizard implementations.

## Files moved

```
web/app/src/app/[locale]/claw-settings/components/
  {Discord,Slack,Telegram}SetupWizard.tsx        → channels/
  {Feishu,Wecom,Weixin}SetupModal.tsx             → channels/
```

All 6 detected as 100% pure renames (`git diff --summary
--find-renames=50%`).

## Import path updates

- `ChannelsSection.tsx`: 5 imports (Discord/Slack/Feishu/Wecom/Weixin) —
`./XSetupWizard` → `./channels/XSetupWizard`
- `channels/AddChannelModal.tsx`: 1 import (TelegramSetupWizard) —
`../TelegramSetupWizard` → `./TelegramSetupWizard`
- `tests/unit/app/claw-settings/ChannelsSection.unit.spec.tsx`: 5
`vi.mock` paths
- `tests/unit/app/claw-settings/ChannelsSection-extras.unit.spec.tsx`: 6
`vi.mock` paths
- 6 wizard-own `*.unit.spec.tsx`: 1 direct `import` each
- `web/app/eslint.config.mjs`: 2 legacy-override paths (Slack/Telegram
entries that pre-date PR 1's refactor — both still need the existing
complexity exemption since this PR is location-only)

## Verification

- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm test:unit --run claw-settings` — 22 files / 500 tests pass
- [x] `git diff --summary --find-renames=50% origin/main...HEAD | grep
-c '^ rename'` == **6** (all 100%)
- [x] `git diff --shortstat origin/main...HEAD` — **50 lines**
(25+/25-), well under the 2000-line gate. PR contains zero logic change;
the 50 lines are pure import-path tweaks.

## Test plan

- [ ] Staging手测: `/claw-settings` channels 区块所有 wizard 入口 (Telegram
guided / Feishu QR / WeCom QR / Weixin QR / Discord guided / Slack
guided) 都能正常打开,功能不变。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

PR 2 of 2 for [#368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368) F14. `git mv` the 6 existing platform setup wizards into the new `channels/` directory created in PR #2018, so the `claw-settings/components/` root no longer mixes section components with wizard implementations.

## Files moved

```
web/app/src/app/[locale]/claw-settings/components/
  {Discord,Slack,Telegram}SetupWizard.tsx        → channels/
  {Feishu,Wecom,Weixin}SetupModal.tsx             → channels/
```

All 6 detected as 100% pure renames (`git diff --summary --find-renames=50%`).

## Import path updates

- `ChannelsSection.tsx`: 5 imports (Discord/Slack/Feishu/Wecom/Weixin) — `./XSetupWizard` → `./channels/XSetupWizard`
- `channels/AddChannelModal.tsx`: 1 import (TelegramSetupWizard) — `../TelegramSetupWizard` → `./TelegramSetupWizard`
- `tests/unit/app/claw-settings/ChannelsSection.unit.spec.tsx`: 5 `vi.mock` paths
- `tests/unit/app/claw-settings/ChannelsSection-extras.unit.spec.tsx`: 6 `vi.mock` paths
- 6 wizard-own `*.unit.spec.tsx`: 1 direct `import` each
- `web/app/eslint.config.mjs`: 2 legacy-override paths (Slack/Telegram entries that pre-date PR 1's refactor — both still need the existing complexity exemption since this PR is location-only)

## Verification

- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm test:unit --run claw-settings` — 22 files / 500 tests pass
- [x] `git diff --summary --find-renames=50% origin/main...HEAD | grep -c '^ rename'` == **6** (all 100%)
- [x] `git diff --shortstat origin/main...HEAD` — **50 lines** (25+/25-), well under the 2000-line gate. PR contains zero logic change; the 50 lines are pure import-path tweaks.

## Test plan

- [ ] Staging手测: `/claw-settings` channels 区块所有 wizard 入口 (Telegram guided / Feishu QR / WeCom QR / Weixin QR / Discord guided / Slack guided) 都能正常打开,功能不变。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [757a062] refactor(web): split ChannelsSection — extract StatusBadge/ChannelCard/AddChannelModal (#368 F14) (#2018)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T08:28:00Z
- **PR**: #2018

### Commit Message
```
refactor(web): split ChannelsSection — extract StatusBadge/ChannelCard/AddChannelModal (#368 F14) (#2018)

## Summary

Pulls out the three inline sub-components and shared helpers from
`web/app/src/app/[locale]/claw-settings/components/ChannelsSection.tsx`
(1,205 → 261 lines, **-78%**) into a new `channels/` directory. PR 1 of
2.

Issue:
[#368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368)
F14 — "ChannelsSection.tsx 1,172 行,三个子组件内联于同一文件"

## What moved

| New file | Lines | Source |
|---|---|---|
| `channels/StatusBadge.tsx` | 31 | old lines 88-114 |
| `channels/ChannelCard.tsx` | 195 | old lines 118-301 (5 useState + 1
useEffect) |
| `channels/AddChannelModal.tsx` | 672 | old lines 305-958 (10 useState
+ 6 platform branches + colocated
PLATFORMS/DM_POLICIES/GROUP_POLICIES/PLATFORM_FIELDS) |
| `channels/helpers.ts` | 46 | `buildAgentOptions` / `getAgentLabel` /
`normalizeChannelAgentId` / `getChannelAgentId` /
`getAccountIdErrorText` + `ChannelAgentOption` interface |
| `channels/constants.ts` | 16 | `PLATFORM_ICONS` + `isWeixinPlatform` |

## What stayed

- `ChannelsSection.tsx` keeps its public API (`export interface
ChannelsSectionProps` + `export function ChannelsSection`). No caller
changes — `ClawSettingsClient.tsx` import path unchanged.
- Six platform setup wizards (`DiscordSetupWizard.tsx` /
`SlackSetupWizard.tsx` / `TelegramSetupWizard.tsx` /
`FeishuSetupModal.tsx` / `WecomSetupModal.tsx` / `WeixinSetupModal.tsx`)
stay at the current location. PR 2 will `git mv` them under `channels/`
so the directory layout is consistent.

## ESLint legacy override

Moved from `ChannelsSection.tsx` (now passes 600-line / complexity-25 /
function-300-line gates cleanly) to `channels/AddChannelModal.tsx`. The
F14 finding explicitly accepts that AddChannelModal retains its
6-platform-branching complexity since the wizards are already extracted
— quoting issue body: "每个平台 wizard 已独立为组件文件,无需再拆分".

## Tests

**Zero test changes.** The existing 2 spec files
(`ChannelsSection.unit.spec.tsx` 891 lines +
`ChannelsSection-extras.unit.spec.tsx` 280 lines) only import
`ChannelsSection` + `ChannelsSectionProps` and stub the 6 platform
wizards via `vi.mock` of paths that don't move in this PR. All 500
claw-settings unit tests pass unmodified.

Future PR can add isolated unit tests for `AddChannelModal` /
`ChannelCard` / `StatusBadge` — out of scope for this PR; integration
coverage is sufficient.

## Test plan

- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean (legacy override correctly shifted)
- [x] `pnpm test:unit --run claw-settings` — 22 files / 500 tests pass
- [ ] Staging手测:
- [ ] `/claw-settings` channels 区块在 bot running / bot stopped 两种状态下渲染正常
- [ ] "Add Channel" → AddChannelModal 弹出,platform 6 种各试一次(Telegram
guided / Feishu QR / WeCom QR / Weixin QR / Discord guided / Slack
guided)
  - [ ] 现有 channel pairing flow(pair 按钮 → 输入 code → approve / cancel)
  - [ ] Edit mode(点已有 channel "Edit" → 编辑保存)
  - [ ] StatusBadge 在各种 status / dm_policy 下颜色/文案正常

## Out of scope (跟踪)

- PR 2(本系列): `git mv` 6 个 wizard 文件入 `channels/`
- AddChannelModal 10-useState → useReducer(future follow-up,F14 不要求)
- ChannelCard `useEffect` derive-via-effect anti-pattern 治理(future
follow-up)
- ChannelsSection 6 个 platform-setup-opts useState 合并为单一 discriminated
union(future follow-up)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Pulls out the three inline sub-components and shared helpers from
`web/app/src/app/[locale]/claw-settings/components/ChannelsSection.tsx`
(1,205 → 261 lines, **-78%**) into a new `channels/` directory. PR 1 of 2.

Issue: [#368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368) F14 — "ChannelsSection.tsx 1,172 行,三个子组件内联于同一文件"

## What moved

| New file | Lines | Source |
|---|---|---|
| `channels/StatusBadge.tsx` | 31 | old lines 88-114 |
| `channels/ChannelCard.tsx` | 195 | old lines 118-301 (5 useState + 1 useEffect) |
| `channels/AddChannelModal.tsx` | 672 | old lines 305-958 (10 useState + 6 platform branches + colocated PLATFORMS/DM_POLICIES/GROUP_POLICIES/PLATFORM_FIELDS) |
| `channels/helpers.ts` | 46 | `buildAgentOptions` / `getAgentLabel` / `normalizeChannelAgentId` / `getChannelAgentId` / `getAccountIdErrorText` + `ChannelAgentOption` interface |
| `channels/constants.ts` | 16 | `PLATFORM_ICONS` + `isWeixinPlatform` |

## What stayed

- `ChannelsSection.tsx` keeps its public API (`export interface ChannelsSectionProps` + `export function ChannelsSection`). No caller changes — `ClawSettingsClient.tsx` import path unchanged.
- Six platform setup wizards (`DiscordSetupWizard.tsx` / `SlackSetupWizard.tsx` / `TelegramSetupWizard.tsx` / `FeishuSetupModal.tsx` / `WecomSetupModal.tsx` / `WeixinSetupModal.tsx`) stay at the current location. PR 2 will `git mv` them under `channels/` so the directory layout is consistent.

## ESLint legacy override

Moved from `ChannelsSection.tsx` (now passes 600-line / complexity-25 / function-300-line gates cleanly) to `channels/AddChannelModal.tsx`. The F14 finding explicitly accepts that AddChannelModal retains its 6-platform-branching complexity since the wizards are already extracted — quoting issue body: "每个平台 wizard 已独立为组件文件,无需再拆分".

## Tests

**Zero test changes.** The existing 2 spec files (`ChannelsSection.unit.spec.tsx` 891 lines + `ChannelsSection-extras.unit.spec.tsx` 280 lines) only import `ChannelsSection` + `ChannelsSectionProps` and stub the 6 platform wizards via `vi.mock` of paths that don't move in this PR. All 500 claw-settings unit tests pass unmodified.

Future PR can add isolated unit tests for `AddChannelModal` / `ChannelCard` / `StatusBadge` — out of scope for this PR; integration coverage is sufficient.

## Test plan

- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean (legacy override correctly shifted)
- [x] `pnpm test:unit --run claw-settings` — 22 files / 500 tests pass
- [ ] Staging手测:
  - [ ] `/claw-settings` channels 区块在 bot running / bot stopped 两种状态下渲染正常
  - [ ] "Add Channel" → AddChannelModal 弹出,platform 6 种各试一次(Telegram guided / Feishu QR / WeCom QR / Weixin QR / Discord guided / Slack guided)
  - [ ] 现有 channel pairing flow(pair 按钮 → 输入 code → approve / cancel)
  - [ ] Edit mode(点已有 channel "Edit" → 编辑保存)
  - [ ] StatusBadge 在各种 status / dm_policy 下颜色/文案正常

## Out of scope (跟踪)

- PR 2(本系列): `git mv` 6 个 wizard 文件入 `channels/`
- AddChannelModal 10-useState → useReducer(future follow-up,F14 不要求)
- ChannelCard `useEffect` derive-via-effect anti-pattern 治理(future follow-up)
- ChannelsSection 6 个 platform-setup-opts useState 合并为单一 discriminated union(future follow-up)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [25ca2a1] docs: redirect root cron-triggers.md to canonical service doc (#2017)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T08:19:58Z
- **PR**: #2017

### Commit Message
```
docs: redirect root cron-triggers.md to canonical service doc (#2017)

## Summary

- The root `docs/cron-triggers.md` was a stale partial duplicate of
`services/claw-interface/docs/cron-triggers.md` (29 lines vs 157),
missing the Phase 2.5 reconciliation runbook, the run-record query API,
and the production scheduler notes — and at risk of further drift since
nothing in current code/CI enforces the two stay in sync.
- `services/claw-interface/AGENTS.md` already designates the in-service
file as the one to update when cron endpoints change (line 82: "update
`docs/cron-triggers.md` in the same PR" — relative to that AGENTS.md,
this resolves to the service-side file).
- Replaced the root file with a one-paragraph redirect stub. Kept (not
deleted) because several frozen-in-time documents under
`docs/superpowers/plans/` and `docs/superpowers/specs/` link to this
path with relative URLs — deleting would break those historical
references for no benefit.

## Test plan

- [ ] Verify the rendered stub on GitHub shows the link to
`services/claw-interface/docs/cron-triggers.md` and the relative link
resolves.
- [ ] Spot-check one historical link from
`docs/superpowers/plans/2026-05-06-eca-616-bot-leak-reconciliation.md`
still navigates to the stub (no 404).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

- The root `docs/cron-triggers.md` was a stale partial duplicate of `services/claw-interface/docs/cron-triggers.md` (29 lines vs 157), missing the Phase 2.5 reconciliation runbook, the run-record query API, and the production scheduler notes — and at risk of further drift since nothing in current code/CI enforces the two stay in sync.
- `services/claw-interface/AGENTS.md` already designates the in-service file as the one to update when cron endpoints change (line 82: "update `docs/cron-triggers.md` in the same PR" — relative to that AGENTS.md, this resolves to the service-side file).
- Replaced the root file with a one-paragraph redirect stub. Kept (not deleted) because several frozen-in-time documents under `docs/superpowers/plans/` and `docs/superpowers/specs/` link to this path with relative URLs — deleting would break those historical references for no benefit.

## Test plan

- [ ] Verify the rendered stub on GitHub shows the link to `services/claw-interface/docs/cron-triggers.md` and the relative link resolves.
- [ ] Spot-check one historical link from `docs/superpowers/plans/2026-05-06-eca-616-bot-leak-reconciliation.md` still navigates to the stub (no 404).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [d4cf97e] fix(billing): use supported partial index filters (#2012)
- **作者**: tim-srp
- **日期**: 2026-05-28T08:15:15Z
- **PR**: #2012

### Commit Message
```
fix(billing): use supported partial index filters (#2012)

## Summary
- Replace unsupported `$ne` partial index filters on Billing v2 optional
unique indexes with Mongo-supported `$gt: ""` string filters.
- Cover Billing v2 profile, payment order, and subscription agreement
startup indexes.
- Add unit coverage to lock the partial index expressions for the
affected optional unique indexes.

## Why
Staging `claw-interface-deployment` pods were exiting during FastAPI
startup while `billing_profile_repo.ensure_indexes()` created indexes:

```text
pymongo.errors.OperationFailure: Expression not supported in partial index: $not customer_id $eq ""
```

The previous `$ne: ""` filter is compiled by Mongo as `$not ... $eq`,
which is not accepted for partial indexes in this environment. `$type:
"string"` plus `$gt: ""` keeps the same intent for optional unique
indexes: only non-empty string values participate in uniqueness.

The original fix handled `billing_profile_repo`; this follow-up also
fixes the next startup index groups in `payment_order_repo` and
`subscription_agreement_repo`, which used the same unsupported helper.

## Test Plan
- `/home/node/.venvs/claw-interface/bin/ruff check
app/database/payment_order_repo.py
app/database/subscription_agreement_repo.py
tests/unit/test_billing_v2_repos.py`
- `/home/node/.venvs/claw-interface/bin/pyright
app/database/payment_order_repo.py
app/database/subscription_agreement_repo.py
tests/unit/test_billing_v2_repos.py`
- `/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_billing_v2_repos.py -q`

---------

Co-authored-by: kaka-srp <kaka@srp.one>
```

### PR Body
## Summary
- Replace unsupported `$ne` partial index filters on Billing v2 optional unique indexes with Mongo-supported `$gt: ""` string filters.
- Cover Billing v2 profile, payment order, and subscription agreement startup indexes.
- Add unit coverage to lock the partial index expressions for the affected optional unique indexes.

## Why
Staging `claw-interface-deployment` pods were exiting during FastAPI startup while `billing_profile_repo.ensure_indexes()` created indexes:

```text
pymongo.errors.OperationFailure: Expression not supported in partial index: $not customer_id $eq ""
```

The previous `$ne: ""` filter is compiled by Mongo as `$not ... $eq`, which is not accepted for partial indexes in this environment. `$type: "string"` plus `$gt: ""` keeps the same intent for optional unique indexes: only non-empty string values participate in uniqueness.

The original fix handled `billing_profile_repo`; this follow-up also fixes the next startup index groups in `payment_order_repo` and `subscription_agreement_repo`, which used the same unsupported helper.

## Test Plan
- `/home/node/.venvs/claw-interface/bin/ruff check app/database/payment_order_repo.py app/database/subscription_agreement_repo.py tests/unit/test_billing_v2_repos.py`
- `/home/node/.venvs/claw-interface/bin/pyright app/database/payment_order_repo.py app/database/subscription_agreement_repo.py tests/unit/test_billing_v2_repos.py`
- `/home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_billing_v2_repos.py -q`

---
## [b43b60b] docs: add arch-review cohort-issues design spec (#2015)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T08:08:46Z
- **PR**: #2015

### Commit Message
```
docs: add arch-review cohort-issues design spec (#2015)

## Summary

- 把周度 arch-review CI 从「每模块一个永久滚动 issue」改成「每次扫描的新发现 cohort 一个 issue」
- Finding schema 把 `Severity` 替换为 3 维 `Priority` (P0/P1/P2) + `Impact`
(Broad/Module/Local) + `Effort` (S/M/L)
- 仅 spec 文档落地，实现拆为 PR 2 (`.github/scripts/arch-review/` 脚本 + tests) 和 PR
3 (workflow + skill 改造) 串行推进
- 现有 #368/#366/#365 作 baseline issue，旧 finding 自然消化，**无需一次性迁移脚本**
- 4 种 (new × resolved) 组合的决策表见 spec
[算法](docs/superpowers/specs/2026-05-28-arch-review-cohort-issues.md#算法)
章节

Spec 文档：`docs/superpowers/specs/2026-05-28-arch-review-cohort-issues.md`

## Test plan
- [x] 文档与同类 CI spec (`2026-04-16-merge-queue-rollout.md`) 结构对齐
- [ ] Team review spec 方向 + Schema 三维度命名（Priority/Impact/Effort 取值是否合理）
- [ ] Review 后启动 PR 2（脚本 + tests，independent，workflow 暂不接）

## 后续 PR

- **PR 2**：`.github/scripts/arch-review/` 新增 6 个 Python
脚本（compose_baseline / reconcile / mark_resolved / count_active /
compose_new / validate_schema）+ pytest，估算 ~700 行
- **PR 3**：`.github/workflows/claude-arch-review.yaml` 改造 +
`.agents/skills/arch-review/SKILL.md` 与
`.claude/commands/arch-review.md` 更新 schema + 新增 `workflow_dispatch
dry_run` mode，估算 ~400 行

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

- 把周度 arch-review CI 从「每模块一个永久滚动 issue」改成「每次扫描的新发现 cohort 一个 issue」
- Finding schema 把 `Severity` 替换为 3 维 `Priority` (P0/P1/P2) + `Impact` (Broad/Module/Local) + `Effort` (S/M/L)
- 仅 spec 文档落地，实现拆为 PR 2 (`.github/scripts/arch-review/` 脚本 + tests) 和 PR 3 (workflow + skill 改造) 串行推进
- 现有 #368/#366/#365 作 baseline issue，旧 finding 自然消化，**无需一次性迁移脚本**
- 4 种 (new × resolved) 组合的决策表见 spec [算法](docs/superpowers/specs/2026-05-28-arch-review-cohort-issues.md#算法) 章节

Spec 文档：`docs/superpowers/specs/2026-05-28-arch-review-cohort-issues.md`

## Test plan
- [x] 文档与同类 CI spec (`2026-04-16-merge-queue-rollout.md`) 结构对齐
- [ ] Team review spec 方向 + Schema 三维度命名（Priority/Impact/Effort 取值是否合理）
- [ ] Review 后启动 PR 2（脚本 + tests，independent，workflow 暂不接）

## 后续 PR

- **PR 2**：`.github/scripts/arch-review/` 新增 6 个 Python 脚本（compose_baseline / reconcile / mark_resolved / count_active / compose_new / validate_schema）+ pytest，估算 ~700 行
- **PR 3**：`.github/workflows/claude-arch-review.yaml` 改造 + `.agents/skills/arch-review/SKILL.md` 与 `.claude/commands/arch-review.md` 更新 schema + 新增 `workflow_dispatch dry_run` mode，估算 ~400 行

---
## [9c77cce] refactor(web): migrate identity to RQ + persister (#1998 PR-C) (#2013)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T08:05:16Z
- **PR**: #2013

### Commit Message
```
refactor(web): migrate identity to RQ + persister (#1998 PR-C) (#2013)

## Summary

Bucket-2 main migration for
[#1998](https://github.com/SerendipityOneInc/ecap-workspace/issues/1998).
Deletes the legacy \`lib/openclaw-identity-cache.ts\` (155 LOC, 2 custom
events, sync drift root cause for PR #1865/#1867 findings) and migrates
all 5 production call sites to RQ + \`PersistQueryClientProvider\`.
**Net diff: -767 LOC** after counting the new
\`agent-description-store.ts\` (40 LOC) + its spec (110 LOC).

PR-A (#2006 characterization tests) and PR-B (#2008 PERSIST_ALLOWLIST
prefix matcher) both merged.

## Architectural changes

| Before (deleted) | After |
|---|---|
| \`lib/openclaw-identity-cache.ts\` (sessionStorage + localStorage +
custom events) | RQ + \`PersistQueryClientProvider\` (sessionStorage via
persister allowlist) |
| \`OPENCLAW_IDENTITY_UPDATED_EVENT\` +
\`OPENCLAW_AGENT_IDENTITY_UPDATED_EVENT\` window-event fanout |
\`queryClient.setQueryData\` / \`setQueriesData\` direct patch |
| \`useAgentIdentityMapOverlay\` (lastKnownUidRef centralised uid-switch
reset) | RQ queryKey-based uid isolation (per-uid cache buckets) |
| \`useNavIdentity\` cached sessionStorage bootstrap + lastKnownUidRef +
2 listeners | Direct RQ subscription to \`clawIdentity(uid)\` +
\`agentSettingsBatch(uid, …)\` |
| \`useChatIdentity\` direct
\`sessionStorage.getItem(CLAW_IDENTITY_CACHE)\` bootstrap |
\`useClawIdentityQuery\` data (persister rehydrates pre-paint) |
| \`AgentIdentitySection\` \`setCachedAgentIdentity({description,
emit:true})\` | \`setAgentDescription\` (new
\`lib/agent-description-store.ts\`, Tier C/D client-only) |
| \`clearUserStorage\` blanket \`sessionStorage.clear()\` |
\`clearAgentDescriptions()\` + \`getQueryClient().clear()\` +
\`sessionStorage.clear()\` (backstop) |

## What \`identity_description\` does next

Verified during planning: \`identity_description\` is **client-only** —
backend \`AgentSettingsResponse\` has no field for it. The new
\`lib/agent-description-store.ts\` (40 LOC) owns it cleanly:
- localStorage-backed (per-device user preference, Tier C/D per #1868
spec)
- \`getAgentDescription\` / \`setAgentDescription\` /
\`clearAgentDescriptions\` API
- Sentry-reported failures (matches PR #1990 \`syncRestoreCache\`
pattern)

## File breakdown

**New (2 files, +150 LOC):**
- \`lib/agent-description-store.ts\` + its spec

**Deleted (3 files, -417 LOC):**
- \`lib/openclaw-identity-cache.ts\` (production)
- \`hooks/useAgentIdentityMapOverlay.ts\` (production)
- \`tests/unit/lib/openclaw-identity-cache.unit.spec.ts\` (PR-A
characterization retires with source)

**Modified (18 files):** 9 production, 6 specs, 3 cleanup files. Main
hooks:
- \`useNavIdentity\` 199 → 100 LOC (5 useEffects + 2 listeners +
sessionStorage bootstrap gone)
- \`useChatIdentity\` cached identity bootstrap gone
- \`useClawIdentityQuery\` 66 → 45 LOC (sync useEffect dropped)
- \`useAgentSettingsQuery\` saveIdentity now patches batch bucket
directly
- \`useClawSettings\` saveIdentity drops emit;
\`applyIdentityToSettingsCache\` already covers RQ sync
- \`clearUserStorage\` + \`manager.ts _completeLogin\` use
\`getQueryClient().clear()\`

## Test plan

- [x] \`pnpm test:unit\` — **6049/6049 pass** (1 todo)
- [x] \`pnpm lint\` — clean
- [x] \`npx tsc --noEmit\` — clean
- [x] \`pnpm lint:ci\` — dep-cruise W1-lib-pure + knip clean
- [ ] **Manual on staging**: logout → DevTools
\`sessionStorage['ecap:rq-cache']\` clears (identity persister storage
purged via clear()); login → switch uid, new identity shows immediately,
no leak from prior uid; hard refresh → identity visible first paint
(persister rehydrate); edit agent description → persists across hard
refresh (localStorage agent-description-store); edit agent nickname →
persists across hard refresh (RQ persister)

## Notable test changes

- **\`useNavIdentity.unit.spec.ts\` shrank 16 → 9 tests** (473 → 165
LOC). Listener regression tests obsolete; new tests focus on gating +
RQ-data mapping + Sentry reporting.
- **\`useAgentSettings\` cross-account guard** rewrote to spy on
\`setQueriesData\` (verify it's never called when uid changed
mid-flight) rather than filter on \`emit: true\`.
- **\`useAgentSettings\` batch-cache tests** need a custom queryClient
with \`gcTime: Infinity\` — \`createTestQueryClient\` defaults to
\`gcTime: 0\` which evicts the pre-seeded batch before
\`saveIdentity\`'s \`setQueriesData\` can find it.
- **\`AgentIdentitySection\`** mock target swapped from
\`@/lib/openclaw-identity-cache\` to the new
\`@/lib/agent-description-store\`.

## Risk notes

- **uid-change reset removed from useNavIdentity** — RQ's queryKey-based
isolation handles it naturally now (each uid gets its own bucket;
switching uids returns to a different bucket immediately).
\`clearUserStorage\` + \`getQueryClient().clear()\` on logout makes the
leak window even tighter than before.
- **Logout flow timing** — \`getQueryClient().clear()\` happens in
\`clearUserStorage\` (sync); the persister observes via its
useEffect-based save subscription and writes empty state back to
sessionStorage on next observed change. Race conditions possible if
logout is followed immediately by sync render reads, but no such caller
exists in the codebase (verified by grep).

Refs #1998, #1868

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Bucket-2 main migration for [#1998](https://github.com/SerendipityOneInc/ecap-workspace/issues/1998). Deletes the legacy \`lib/openclaw-identity-cache.ts\` (155 LOC, 2 custom events, sync drift root cause for PR #1865/#1867 findings) and migrates all 5 production call sites to RQ + \`PersistQueryClientProvider\`. **Net diff: -767 LOC** after counting the new \`agent-description-store.ts\` (40 LOC) + its spec (110 LOC).

PR-A (#2006 characterization tests) and PR-B (#2008 PERSIST_ALLOWLIST prefix matcher) both merged.

## Architectural changes

| Before (deleted) | After |
|---|---|
| \`lib/openclaw-identity-cache.ts\` (sessionStorage + localStorage + custom events) | RQ + \`PersistQueryClientProvider\` (sessionStorage via persister allowlist) |
| \`OPENCLAW_IDENTITY_UPDATED_EVENT\` + \`OPENCLAW_AGENT_IDENTITY_UPDATED_EVENT\` window-event fanout | \`queryClient.setQueryData\` / \`setQueriesData\` direct patch |
| \`useAgentIdentityMapOverlay\` (lastKnownUidRef centralised uid-switch reset) | RQ queryKey-based uid isolation (per-uid cache buckets) |
| \`useNavIdentity\` cached sessionStorage bootstrap + lastKnownUidRef + 2 listeners | Direct RQ subscription to \`clawIdentity(uid)\` + \`agentSettingsBatch(uid, …)\` |
| \`useChatIdentity\` direct \`sessionStorage.getItem(CLAW_IDENTITY_CACHE)\` bootstrap | \`useClawIdentityQuery\` data (persister rehydrates pre-paint) |
| \`AgentIdentitySection\` \`setCachedAgentIdentity({description, emit:true})\` | \`setAgentDescription\` (new \`lib/agent-description-store.ts\`, Tier C/D client-only) |
| \`clearUserStorage\` blanket \`sessionStorage.clear()\` | \`clearAgentDescriptions()\` + \`getQueryClient().clear()\` + \`sessionStorage.clear()\` (backstop) |

## What \`identity_description\` does next

Verified during planning: \`identity_description\` is **client-only** — backend \`AgentSettingsResponse\` has no field for it. The new \`lib/agent-description-store.ts\` (40 LOC) owns it cleanly:
- localStorage-backed (per-device user preference, Tier C/D per #1868 spec)
- \`getAgentDescription\` / \`setAgentDescription\` / \`clearAgentDescriptions\` API
- Sentry-reported failures (matches PR #1990 \`syncRestoreCache\` pattern)

## File breakdown

**New (2 files, +150 LOC):**
- \`lib/agent-description-store.ts\` + its spec

**Deleted (3 files, -417 LOC):**
- \`lib/openclaw-identity-cache.ts\` (production)
- \`hooks/useAgentIdentityMapOverlay.ts\` (production)
- \`tests/unit/lib/openclaw-identity-cache.unit.spec.ts\` (PR-A characterization retires with source)

**Modified (18 files):** 9 production, 6 specs, 3 cleanup files. Main hooks:
- \`useNavIdentity\` 199 → 100 LOC (5 useEffects + 2 listeners + sessionStorage bootstrap gone)
- \`useChatIdentity\` cached identity bootstrap gone
- \`useClawIdentityQuery\` 66 → 45 LOC (sync useEffect dropped)
- \`useAgentSettingsQuery\` saveIdentity now patches batch bucket directly
- \`useClawSettings\` saveIdentity drops emit; \`applyIdentityToSettingsCache\` already covers RQ sync
- \`clearUserStorage\` + \`manager.ts _completeLogin\` use \`getQueryClient().clear()\`

## Test plan

- [x] \`pnpm test:unit\` — **6049/6049 pass** (1 todo)
- [x] \`pnpm lint\` — clean
- [x] \`npx tsc --noEmit\` — clean
- [x] \`pnpm lint:ci\` — dep-cruise W1-lib-pure + knip clean
- [ ] **Manual on staging**: logout → DevTools \`sessionStorage['ecap:rq-cache']\` clears (identity persister storage purged via clear()); login → switch uid, new identity shows immediately, no leak from prior uid; hard refresh → identity visible first paint (persister rehydrate); edit agent description → persists across hard refresh (localStorage agent-description-store); edit agent nickname → persists across hard refresh (RQ persister)

## Notable test changes

- **\`useNavIdentity.unit.spec.ts\` shrank 16 → 9 tests** (473 → 165 LOC). Listener regression tests obsolete; new tests focus on gating + RQ-data mapping + Sentry reporting.
- **\`useAgentSettings\` cross-account guard** rewrote to spy on \`setQueriesData\` (verify it's never called when uid changed mid-flight) rather than filter on \`emit: true\`.
- **\`useAgentSettings\` batch-cache tests** need a custom queryClient with \`gcTime: Infinity\` — \`createTestQueryClient\` defaults to \`gcTime: 0\` which evicts the pre-seeded batch before \`saveIdentity\`'s \`setQueriesData\` can find it.
- **\`AgentIdentitySection\`** mock target swapped from \`@/lib/openclaw-identity-cache\` to the new \`@/lib/agent-description-store\`.

## Risk notes

- **uid-change reset removed from useNavIdentity** — RQ's queryKey-based isolation handles it naturally now (each uid gets its own bucket; switching uids returns to a different bucket immediately). \`clearUserStorage\` + \`getQueryClient().clear()\` on logout makes the leak window even tighter than before.
- **Logout flow timing** — \`getQueryClient().clear()\` happens in \`clearUserStorage\` (sync); the persister observes via its useEffect-based save subscription and writes empty state back to sessionStorage on next observed change. Race conditions possible if logout is followed immediately by sync render reads, but no such caller exists in the codebase (verified by grep).

Refs #1998, #1868

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [cb3c521] feat(composio): add isolated connector flow (#1933)
- **作者**: tim-srp
- **日期**: 2026-05-28T08:00:25Z
- **PR**: #1933

### Commit Message
```
feat(composio): add isolated connector flow (#1933)

## Linear
https://linear.app/srpone/issue/ECA-819/composio-connectors

## Summary
- add a feature-flagged Settings entry and isolated Composio connector
page
- route Composio connector UI/BFF calls through ecap-proxy-service
- keep claw-interface stateless for Composio connection data and
credentials

## Isolation
- does not modify existing connector, channel, or integration execution
routes
- Composio page is gated by NEXT_PUBLIC_COMPOSIO_CONNECTORS_PAGE_ENABLED
/ COMPOSIO_CONNECTORS_PAGE_ENABLED
- claw-interface only forwards to proxy-service

## Tests
- pytest services/claw-interface/tests/unit/test_composio_connectors.py
-q
- pytest -W ignore:'Please use `import python_multipart`
instead.':PendingDeprecationWarning
services/claw-interface/tests/unit/test_integration_routes.py
services/claw-interface/tests/unit/test_integration_repo.py
services/claw-interface/tests/unit/test_integration_provider.py
services/claw-interface/tests/unit/test_google_connector.py
services/claw-interface/tests/unit/test_connector_status.py -q
- ruff check services/claw-interface/app/routes/composio_connectors.py
services/claw-interface/app/schema/composio_connector.py
services/claw-interface/app/settings.py
services/claw-interface/tests/unit/test_composio_connectors.py
- pyright --pythonpath /Users/shiqi/miniconda3/bin/python
services/claw-interface/app/routes/composio_connectors.py
services/claw-interface/app/schema/composio_connector.py
services/claw-interface/tests/unit/test_composio_connectors.py
- pnpm --dir web/app exec tsc --noEmit --pretty false
- pnpm --dir web/app test:unit
tests/unit/app/claw-settings/ConnectorsSection.unit.spec.tsx --
--runInBand

---------

Co-authored-by: A-Q <a-q@A-QdeMac-mini.local>
```

### PR Body
## Linear
https://linear.app/srpone/issue/ECA-819/composio-connectors

## Summary
- add a feature-flagged Settings entry and isolated Composio connector page
- route Composio connector UI/BFF calls through ecap-proxy-service
- keep claw-interface stateless for Composio connection data and credentials

## Isolation
- does not modify existing connector, channel, or integration execution routes
- Composio page is gated by NEXT_PUBLIC_COMPOSIO_CONNECTORS_PAGE_ENABLED / COMPOSIO_CONNECTORS_PAGE_ENABLED
- claw-interface only forwards to proxy-service

## Tests
- pytest services/claw-interface/tests/unit/test_composio_connectors.py -q
- pytest -W ignore:'Please use `import python_multipart` instead.':PendingDeprecationWarning services/claw-interface/tests/unit/test_integration_routes.py services/claw-interface/tests/unit/test_integration_repo.py services/claw-interface/tests/unit/test_integration_provider.py services/claw-interface/tests/unit/test_google_connector.py services/claw-interface/tests/unit/test_connector_status.py -q
- ruff check services/claw-interface/app/routes/composio_connectors.py services/claw-interface/app/schema/composio_connector.py services/claw-interface/app/settings.py services/claw-interface/tests/unit/test_composio_connectors.py
- pyright --pythonpath /Users/shiqi/miniconda3/bin/python services/claw-interface/app/routes/composio_connectors.py services/claw-interface/app/schema/composio_connector.py services/claw-interface/tests/unit/test_composio_connectors.py
- pnpm --dir web/app exec tsc --noEmit --pretty false
- pnpm --dir web/app test:unit tests/unit/app/claw-settings/ConnectorsSection.unit.spec.tsx -- --runInBand

---
## [d568ae1] docs: add staging deploy badges (#2014)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T07:35:24Z
- **PR**: #2014

### Commit Message
```
docs: add staging deploy badges (#2014)

## Summary
- Add staging deployment badges to the README for Web, Enterprise Admin,
and Claw Interface.
- Publish separate staging deploy badge JSON files from the matching
deploy workflows.
- Keep production deploy badge files independent from staging status.

## Test plan
- [x] git diff --check
- [x] ruby -e 'require "yaml"; ARGV.each { |f| YAML.load_file(f); puts
"#{f}: ok" }' .github/workflows/deploy.yml
.github/workflows/deploy-enterprise-admin.yml
.github/workflows/service-deploy.yml
```

### PR Body
## Summary
- Add staging deployment badges to the README for Web, Enterprise Admin, and Claw Interface.
- Publish separate staging deploy badge JSON files from the matching deploy workflows.
- Keep production deploy badge files independent from staging status.

## Test plan
- [x] git diff --check
- [x] ruby -e 'require "yaml"; ARGV.each { |f| YAML.load_file(f); puts "#{f}: ok" }' .github/workflows/deploy.yml .github/workflows/deploy-enterprise-admin.yml .github/workflows/service-deploy.yml

---
## [c4214d2] refactor(web): hasOverlap → (nodes, rect) options object (#1957) (#2011)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T07:04:26Z
- **PR**: #1957

### Commit Message
```
refactor(web): hasOverlap → (nodes, rect) options object (#1957) (#2011)

## Summary
- 把 \`hasOverlap\` 从 5-positional-param \`(nodes, x, y, w, h)\` 改成几何标准
\`(nodes, { x, y, w?, h? })\` 签名,完成 issue #1957 最后一条 max-params 违例
(issue 自己标 \`可接受 / 边界\`,本 PR full closure 收尾)
- \`w\` / \`h\` 保留 optional 内部默认 \`NODE_WIDTH\` /
\`NODE_HEIGHT_ESTIMATE\` —— 现有 2 个 caller(\`findChildPosition\` 内 right
/ below placement loop)都只关心 x/y,改 \`{ x, y }\` 简洁形式即可,无需在 call site 重复
magic constant
- \`eslint.config.mjs\`:从 legacy complexity exemption block 移除
\`useCanvasState.ts\` + 新增 narrow per-file override 关闭 \`max-lines\` +
\`max-lines-per-function\`(useCanvasState 主函数 578 行 + 文件 641 行均超限,属另外的
refactor 类目),保 \`max-params\` 生效。对照 #1971 pptx-parser / #2007 PlanCard /
#2009 useCanvasChat 同款模板

## Before / After

\`\`\`diff
-function hasOverlap(
-  nodes: Node[],
-  x: number,
-  y: number,
-  w: number = NODE_WIDTH,
-  h: number = NODE_HEIGHT_ESTIMATE,
-): boolean {
-  for (const node of nodes) { ... }
+function hasOverlap(nodes: Node[], candidate: { x: number; y: number;
w?: number; h?: number }): boolean {
+  const { x, y, w = NODE_WIDTH, h = NODE_HEIGHT_ESTIMATE } = candidate
+  for (const node of nodes) { ... }

-if (!hasOverlap(nodes, x, y)) return { x, y }
+if (!hasOverlap(nodes, { x, y })) return { x, y }
\`\`\`

## Test plan
- [x] \`npx eslint src/app/[locale]/canvas/hooks/useCanvasState.ts\` 0
error(移除 exemption + 加 narrow override 后)
- [x] \`npx tsc --noEmit\` 0 error
- [x] \`pnpm test:unit\` canvas 范围 6 spec / 80 test 全绿
- [x] \`grep hasOverlap\` 验证除 useCanvasState.ts 内 2 个 call site 外无其他
caller

## 上下文 — Issue #1957 序列完结
- ✅ #1967 \`getSessionList\`
- ✅ #1969 \`reportLatency\`
- ✅ #1971 \`extractGroupShapes\` + \`mapChildToSlide\`
- ✅ #2005 \`customInputArea\`
- ✅ #2007 \`getCtaConfig\` + \`getBadge\` (BillingState)
- ✅ #2009 \`addPlaceholderNode\` + \`convertToLayerEditor\`
- ➡️ 本 PR \`hasOverlap\` (full closure)

合并后 issue #1957 可关闭。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---
## [6fa41aa] refactor(web): addPlaceholderNode + convertToLayerEditor → options object (#1957) (#2009)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T06:54:38Z
- **PR**: #1957

### Commit Message
```
refactor(web): addPlaceholderNode + convertToLayerEditor → options object (#1957) (#2009)

## Summary
- 把 useCanvasChat interface 声明的两个 5-positional-param 函数改成 \`(identity,
opts)\` 套路,沿用 #1967 \`getSessionList(uid, opts?)\` 模板
- \`addPlaceholderNode(description, opts)\`:opts 全 optional(model /
connectToNodeId / placement / skipLastNodeUpdate)
- \`convertToLayerEditor(nodeId, opts)\`:opts 全 required(layers /
canvasWidth / canvasHeight / onSaveKey 都是同语义簇 layer editor 配置)
- \`eslint.config.mjs\`:从 legacy complexity exemption block 移除
\`useCanvasChat.ts\` + 新增 narrow per-file override 关闭 \`complexity\` +
\`max-lines-per-function\`(useCanvasChat 主函数 455 行 + 2 个 inner
complexity 26/27 是另外的 refactor 类目),保 \`max-params\` 生效。对照 #1971
pptx-parser / #2007 PlanCard 同款模板
- \`useCanvasState.ts\` 仍留 legacy block 不动:\`hasOverlap\` 5-param
未解(issue 标 acceptable,可 defer)+ \`max-lines\` /
\`max-lines-per-function\` 都 hit

## 改动面
- \`useCanvasState.ts\` 2 函数定义改 destructure-with-defaults 模板
- \`useCanvasChat.ts\` interface 2 字段 + 5 个 call site
- \`tests/unit/canvas-hooks/useCanvasChat.unit.spec.ts\` 6 处
\`toHaveBeenCalledWith\` 由 positional 改为 object literal 断言

## Before / After (addPlaceholderNode)

\`\`\`diff
-addPlaceholderNode(description, model, connectToNodeId, placement,
skipLastNodeUpdate)
+addPlaceholderNode(description, { model, connectToNodeId, placement,
skipLastNodeUpdate })

-addPlaceholderNode('Agent working...', 'omni_chat', connectFrom)
+addPlaceholderNode('Agent working...', { model: 'omni_chat',
connectToNodeId: connectFrom })

-addPlaceholderNode(descriptionMap[action], model, sourceNodeId,
'right', true)
+addPlaceholderNode(descriptionMap[action], {
+  model,
+  connectToNodeId: sourceNodeId,
+  placement: 'right',
+  skipLastNodeUpdate: true,
+})
\`\`\`

## Test plan
- [x] \`npx eslint\` 0 error(useCanvasChat.ts 含 narrow override /
useCanvasState.ts 留 legacy block)
- [x] \`npx tsc --noEmit\` 0 error
- [x] \`pnpm test:unit\` canvas 范围 3 spec(useCanvasChat / useCanvasState
/ LayerEditorNode)/ 40 test 全绿
- [x] 2 个 shrink-only 守门脚本(forbid-dom-props / svg-inline)全 pass
- [x] \`grep addPlaceholderNode convertToLayerEditor\` 验证除 canvas hooks
+ spec 外无其他 caller(CanvasClient.tsx 只是 props pass-through)

## 上下文
Issue #1957 序列第 6 个:
- ✅ #1967 \`getSessionList\`
- ✅ #1969 \`reportLatency\`
- ✅ #1971 \`extractGroupShapes\` + \`mapChildToSlide\`
- ✅ #2005 \`customInputArea\`
- 🟡 #2007 \`getCtaConfig\` + \`getBadge\` (in merge queue)
- ➡️ 本 PR \`addPlaceholderNode\` + \`convertToLayerEditor\`
- ⏳ \`hasOverlap\` (issue 标 acceptable,可 defer 或几何重塑收尾)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---
## [8cf2e77] refactor(web): extend PERSIST_ALLOWLIST with prefix matcher (#1998 PR-B) (#2008)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T06:46:16Z
- **PR**: #2008

### Commit Message
```
refactor(web): extend PERSIST_ALLOWLIST with prefix matcher (#1998 PR-B) (#2008)

## Summary

Mechanism-only PR for
[#1998](https://github.com/SerendipityOneInc/ecap-workspace/issues/1998)
Bucket-2. **Production semantics unchanged** —
\`PERSIST_ALLOWLIST_PREFIXES\` is an empty array; the Bucket-2 main PR
(PR-C) adds the first entry (\`CLAW_IDENTITY_QUERY_KEY_PREFIX\`) once
the identity migration is in place.

## Why prefix mode is needed

PR #1990's matcher is exact-equality only (length + every segment ===),
which works for the public catalog's 4-segment key with no scoping. But
identity / settings queries are **uid-parameterized** —
\`clawIdentity('uid-A')\` and \`clawIdentity('uid-B')\` are distinct
full keys, so an exact allowlist would require whitelisting every uid
value individually. A prefix entry covers the whole family in one line:
\`[v1, openclaw, claw-identity]\` allows every uid suffix.

## Changes

| File | Change |
|---|---|
| \`lib/query/keys.ts\` | Add \`CLAW_IDENTITY_QUERY_KEY_PREFIX\` +
\`AGENT_SETTINGS_BATCH_QUERY_KEY_PREFIX\` (Layer 2 source-of-truth,
mirroring the \`AGENT_CATALOG_OFFICIAL_QUERY_KEY\` pattern). |
| \`lib/query/persist-client.ts\` | Add \`PERSIST_ALLOWLIST_PREFIXES\`
(empty), split matcher into \`matchesExact\` + \`matchesPrefix\`
helpers, change \`isAllowedQueryKey\` to \"exact OR prefix\"
composition. \`matchesExact\` + \`matchesPrefix\` exported for unit
tests since the prefix list is module-private. |
| \`tests/unit/lib/query/persist-client.unit.spec.ts\` | +9 tests
(PERSIST_ALLOWLIST_PREFIXES empty assertion + matchesExact 3 cases +
matchesPrefix 5 cases). |

## Strict-prefix semantics

\`matchesPrefix\` requires \`queryKey.length > prefix.length\` (not ≥).
A queryKey equal to the prefix is rejected because a \"family entry\"
with no varying segment is a misuse — exact mode handles that case. The
strict-greater-than guard prevents accidental overlap between the two
matcher modes.

## Test plan

- [x] \`pnpm test:unit\` — 6051/6051 pass (1 todo)
- [x] \`pnpm lint\` — clean
- [x] \`npx tsc --noEmit\` — clean
- [x] \`pnpm lint:ci\` — dep-cruise W1-lib-pure + knip clean (new
exports from lib/query are valid Layer 2 surface)

## Notes for reviewer

- Production behavior is bit-identical to PR #1990:
\`PERSIST_ALLOWLIST_PREFIXES.some(...)\` over an empty array always
returns false, so \`isAllowedQueryKey\` reduces to the original
exact-match path.
- The \`matchesExact\` + \`matchesPrefix\` exports are intentionally
\"test-only\" surface. Alternatives (e.g. a
\`createIsAllowedQueryKey(exactList, prefixList)\` factory) trade larger
refactor for less test-visibility — opted for the simpler shape.
- PR-A characterization (#2006) merged. PR-C (main migration, ~700-1000
LOC) follows this PR.

Refs #1998, #1868

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Mechanism-only PR for [#1998](https://github.com/SerendipityOneInc/ecap-workspace/issues/1998) Bucket-2. **Production semantics unchanged** — \`PERSIST_ALLOWLIST_PREFIXES\` is an empty array; the Bucket-2 main PR (PR-C) adds the first entry (\`CLAW_IDENTITY_QUERY_KEY_PREFIX\`) once the identity migration is in place.

## Why prefix mode is needed

PR #1990's matcher is exact-equality only (length + every segment ===), which works for the public catalog's 4-segment key with no scoping. But identity / settings queries are **uid-parameterized** — \`clawIdentity('uid-A')\` and \`clawIdentity('uid-B')\` are distinct full keys, so an exact allowlist would require whitelisting every uid value individually. A prefix entry covers the whole family in one line: \`[v1, openclaw, claw-identity]\` allows every uid suffix.

## Changes

| File | Change |
|---|---|
| \`lib/query/keys.ts\` | Add \`CLAW_IDENTITY_QUERY_KEY_PREFIX\` + \`AGENT_SETTINGS_BATCH_QUERY_KEY_PREFIX\` (Layer 2 source-of-truth, mirroring the \`AGENT_CATALOG_OFFICIAL_QUERY_KEY\` pattern). |
| \`lib/query/persist-client.ts\` | Add \`PERSIST_ALLOWLIST_PREFIXES\` (empty), split matcher into \`matchesExact\` + \`matchesPrefix\` helpers, change \`isAllowedQueryKey\` to \"exact OR prefix\" composition. \`matchesExact\` + \`matchesPrefix\` exported for unit tests since the prefix list is module-private. |
| \`tests/unit/lib/query/persist-client.unit.spec.ts\` | +9 tests (PERSIST_ALLOWLIST_PREFIXES empty assertion + matchesExact 3 cases + matchesPrefix 5 cases). |

## Strict-prefix semantics

\`matchesPrefix\` requires \`queryKey.length > prefix.length\` (not ≥). A queryKey equal to the prefix is rejected because a \"family entry\" with no varying segment is a misuse — exact mode handles that case. The strict-greater-than guard prevents accidental overlap between the two matcher modes.

## Test plan

- [x] \`pnpm test:unit\` — 6051/6051 pass (1 todo)
- [x] \`pnpm lint\` — clean
- [x] \`npx tsc --noEmit\` — clean
- [x] \`pnpm lint:ci\` — dep-cruise W1-lib-pure + knip clean (new exports from lib/query are valid Layer 2 surface)

## Notes for reviewer

- Production behavior is bit-identical to PR #1990: \`PERSIST_ALLOWLIST_PREFIXES.some(...)\` over an empty array always returns false, so \`isAllowedQueryKey\` reduces to the original exact-match path.
- The \`matchesExact\` + \`matchesPrefix\` exports are intentionally \"test-only\" surface. Alternatives (e.g. a \`createIsAllowedQueryKey(exactList, prefixList)\` factory) trade larger refactor for less test-visibility — opted for the simpler shape.
- PR-A characterization (#2006) merged. PR-C (main migration, ~700-1000 LOC) follows this PR.

Refs #1998, #1868

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [06c25a9] chore(skills): add diff-stats for PR/diff line-count categorization (#1989)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T06:45:11Z
- **PR**: #1989

### Commit Message
```
chore(skills): add diff-stats for PR/diff line-count categorization (#1989)

## Summary

Add a project-local Claude Code skill that **categorizes PR/diff lines
by purpose** — business code / test code / ci-tooling / docs / generated
— so net line counts don't mislead during review.

No verdict, no callouts, no AST analysis. Just the breakdown table.
Reviewer reads it and judges.

## Files

- `.claude/skills/diff-stats/SKILL.md` — trigger keywords + usage
- `.claude/skills/diff-stats/scripts/stats.py` — single-file Python
entrypoint (327 lines)

## Why this scope

Earlier commits on this branch had a much more ambitious "refactor
diagnose" scope: function-length analysis (via lizard), type-escape
regex counting, exported-symbol delta, TODO/FIXME counting,
moved-but-unchanged ratio, and an overall verdict ("Likely
simplification" / "Mixed" / "Likely growth"). After dogfooding it on the
branch's own PR and on 7 historical refactor PRs, the verdict layer
turned out to misfire enough — false-positive TODOs from string
literals, type-escape regex matching legitimate `import x # type:
ignore`, Python `def`/`class` counted as exports — that the reviewer
ends up second-guessing the tool rather than the diff.

This commit rips the verdict and content-analysis layers out (~370 lines
+ the lizard optional dep) and keeps the **one part that's unambiguously
useful**: a per-category line breakdown with rename handling,
generated-file exclusion, and a project-level override
(`.diff-stats.toml`).

Renamed `refactor-diagnose` → `diff-stats`. The old name overpromised.

## Output

```
diff-stats — git diff main...HEAD (merge-base 43ad090a)

  category        +lines  -lines     net  files
  ---------------------------------------------
  business code      120     340    -220      8
  test code          210      30    +180      4
  ci/tooling           5       0      +5      1
  docs                12       3      +9      2
  generated         (excluded)               1

  totals (excl. generated): +347 / -373  (net -26)
  files: +1 added / -3 deleted / 0 renamed / 9 modified
  generated excluded: web/pnpm-lock.yaml
```

## Kept from earlier rounds of fixes

The simplification deletes a lot, but the bug fixes the prior reviews
surfaced (which apply to the categorization core) are kept:

- `_resolve_rename_path` for git's brace notation
- `-M` on both `--name-status` and `--numstat` so rename counts are
correct
- `_match` helper so `**/scripts/**` matches root-level `scripts/`
- override categories in `.diff-stats.toml` win over built-in
classification (incl. reclassifying paths into `business`)
- `detect_main` falls back to `origin/main`, `origin/master`, `HEAD~1`,
empty-tree SHA — no crash in CI / shallow / single-commit /
non-main-branch checkouts
- Diff invocation uses space-separated `git diff A B` so tree-ish bases
work

## Test plan

- [x] Self-test on current branch — reports `+757/-0` to `ci/tooling`,
`+79/-0` to `docs`, no business code (because the script itself lives
under `scripts/`)
- [x] `ba2ef3e8b` (god-hook extract refactor) — business +552/-438 /
test +436/-0
- [x] `42a4b8d0e` (lockfile + small fixes) — `web/pnpm-lock.yaml`
excluded, business +54/-9 reported cleanly
- [x] Synthetic pure-rename of 20-line file — 0/0 with `renamed: 1` (not
20/0 phantom add)
- [x] Single-commit repo on branch `trunk` (no main, no parent) — runs
cleanly against empty-tree base instead of tracebacking

Try it: `python3 .claude/skills/diff-stats/scripts/stats.py --base
<ref>^ --head <ref>`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Add a project-local Claude Code skill that **categorizes PR/diff lines by purpose** — business code / test code / ci-tooling / docs / generated — so net line counts don't mislead during review.

No verdict, no callouts, no AST analysis. Just the breakdown table. Reviewer reads it and judges.

## Files

- `.claude/skills/diff-stats/SKILL.md` — trigger keywords + usage
- `.claude/skills/diff-stats/scripts/stats.py` — single-file Python entrypoint (327 lines)

## Why this scope

Earlier commits on this branch had a much more ambitious "refactor diagnose" scope: function-length analysis (via lizard), type-escape regex counting, exported-symbol delta, TODO/FIXME counting, moved-but-unchanged ratio, and an overall verdict ("Likely simplification" / "Mixed" / "Likely growth"). After dogfooding it on the branch's own PR and on 7 historical refactor PRs, the verdict layer turned out to misfire enough — false-positive TODOs from string literals, type-escape regex matching legitimate `import x  # type: ignore`, Python `def`/`class` counted as exports — that the reviewer ends up second-guessing the tool rather than the diff.

This commit rips the verdict and content-analysis layers out (~370 lines + the lizard optional dep) and keeps the **one part that's unambiguously useful**: a per-category line breakdown with rename handling, generated-file exclusion, and a project-level override (`.diff-stats.toml`).

Renamed `refactor-diagnose` → `diff-stats`. The old name overpromised.

## Output

```
diff-stats — git diff main...HEAD (merge-base 43ad090a)

  category        +lines  -lines     net  files
  ---------------------------------------------
  business code      120     340    -220      8
  test code          210      30    +180      4
  ci/tooling           5       0      +5      1
  docs                12       3      +9      2
  generated         (excluded)               1

  totals (excl. generated): +347 / -373  (net -26)
  files: +1 added / -3 deleted / 0 renamed / 9 modified
  generated excluded: web/pnpm-lock.yaml
```

## Kept from earlier rounds of fixes

The simplification deletes a lot, but the bug fixes the prior reviews surfaced (which apply to the categorization core) are kept:

- `_resolve_rename_path` for git's brace notation
- `-M` on both `--name-status` and `--numstat` so rename counts are correct
- `_match` helper so `**/scripts/**` matches root-level `scripts/`
- override categories in `.diff-stats.toml` win over built-in classification (incl. reclassifying paths into `business`)
- `detect_main` falls back to `origin/main`, `origin/master`, `HEAD~1`, empty-tree SHA — no crash in CI / shallow / single-commit / non-main-branch checkouts
- Diff invocation uses space-separated `git diff A B` so tree-ish bases work

## Test plan

- [x] Self-test on current branch — reports `+757/-0` to `ci/tooling`, `+79/-0` to `docs`, no business code (because the script itself lives under `scripts/`)
- [x] `ba2ef3e8b` (god-hook extract refactor) — business +552/-438 / test +436/-0
- [x] `42a4b8d0e` (lockfile + small fixes) — `web/pnpm-lock.yaml` excluded, business +54/-9 reported cleanly
- [x] Synthetic pure-rename of 20-line file — 0/0 with `renamed: 1` (not 20/0 phantom add)
- [x] Single-commit repo on branch `trunk` (no main, no parent) — runs cleanly against empty-tree base instead of tracebacking

Try it: `python3 .claude/skills/diff-stats/scripts/stats.py --base <ref>^ --head <ref>`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [e843caf] refactor(web): PlanCard getCtaConfig + getBadge → BillingState (#1957) (#2007)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T06:31:28Z
- **PR**: #1957

### Commit Message
```
refactor(web): PlanCard getCtaConfig + getBadge → BillingState (#1957) (#2007)

## Summary
- 把 `PlanCard.tsx` 内的 `getCtaConfig` / `getBadge` 从 6-positional-param
各自改成单 `BillingState` 对象,沿用 #1967 / #1969 / #1971 / #2005 的
options-object 套路
- `BillingState` 是 `PlanCard.tsx` 内部 non-exported interface(7 字段),避开与
`lib/billing/mock-billing-data.ts` 已有的 `MockBillingState`(全量 backend
视图,20+ 字段)重名混淆 —— 名称区分:`BillingState` = UI
决策状态(plan/cycle/userStatus/currentPlan/currentCycle/previousPlan/trialEligible),`MockBillingState`
= mock fixture 全量字段
- 两个函数共享 5 字段,各自第 6 字段不同(getCtaConfig 读 trialEligible / getBadge 读
previousPlan)—— 按 issue 提议合并为单一 type 包含所有 7 字段,caller 一次构造两个共用,函数内部
destructure 各取所需,语义不变
- `eslint.config.mjs`:从 legacy complexity exemption block 移除
`PlanCard.tsx` 一行 + 新增 narrow per-file override 关闭 `complexity`(PlanCard
主体仍 28 > 25,属另外的 refactor 类目),保 `max-params` 生效。对照 #1971 pptx-parser
同款模板

## Before / After

\`\`\`diff
-function getCtaConfig(
-  plan: PlanTier,
-  cycle: BillingCycle,
-  userStatus: UserDisplayStatus,
-  currentPlan: PlanTier | null,
-  currentCycle: BillingCycle | null,
-  trialEligible: boolean,
-): { label, action, variant }
-
-function getBadge(
-  plan: PlanTier,
-  cycle: BillingCycle,
-  userStatus: UserDisplayStatus,
-  currentPlan: PlanTier | null,
-  currentCycle: BillingCycle | null,
-  previousPlan: PlanTier | null | undefined,
-): { label, variant } | null
+interface BillingState {
+  plan: PlanTier
+  cycle: BillingCycle
+  userStatus: UserDisplayStatus
+  currentPlan: PlanTier | null
+  currentCycle: BillingCycle | null
+  previousPlan: PlanTier | null | undefined
+  trialEligible: boolean
+}
+
+function getCtaConfig(state: BillingState): { label, action, variant }
+function getBadge(state: BillingState): { label, variant } | null
\`\`\`

Caller (PlanCard render) 一次构造 state 两个共用:
\`\`\`tsx
const billingState: BillingState = { plan, cycle, userStatus,
currentPlan, currentCycle, previousPlan, trialEligible }
const badge = getBadge(billingState)
const cta = getCtaConfig(billingState)
\`\`\`

## Test plan
- [x] \`npx eslint src/components/billing/PlanCard.tsx\` 0 error(移除
exemption 后)
- [x] \`npx tsc --noEmit\` 0 error
- [x] \`pnpm test:unit\` billing 范围 4 spec(PlanCard / SharedPlanCard /
SubscriptionPanel / SubscriptionPanel-extras)/ 87 test 全绿 —— PlanCard
测试是黑盒 component-level,不直接调内部 helper,refactor 0 impact
- [x] 4 个 shrink-only 守门脚本 全 pass
- [x] \`grep getCtaConfig getBadge\` 验证除 PlanCard.tsx 内部外无其他 caller

## 上下文
Issue #1957 序列第 5 个:
- ✅ #1967 \`getSessionList\`
- ✅ #1969 \`reportLatency\`
- ✅ #1971 \`extractGroupShapes\` + \`mapChildToSlide\`
- ✅ #2005 \`customInputArea\`
- ➡️ 本 PR \`getCtaConfig\` + \`getBadge\`
- ⏳ \`useCanvasState\` 的 \`addPlaceholderNode\` 5-param
- ⏳ \`hasOverlap\` (issue 标 acceptable,可 defer)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---
## [1eb77c7] test(web): Bucket-2 Phase 0 characterization (#1998) (#2006)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T06:21:21Z
- **PR**: #1998

### Commit Message
```
test(web): Bucket-2 Phase 0 characterization (#1998) (#2006)

## Summary

Phase 0 prerequisite for
[#1998](https://github.com/SerendipityOneInc/ecap-workspace/issues/1998)
(Bucket-2 of #1868). **Test-only PR**, zero production code change.
Locks the current behavior of the three layers PR-C will reshape so the
Bucket-2 main PR produces a *behavioral* diff rather than a *code* diff
(per [[feedback_characterize_before_refactor_storage]]).

## Changes

3 spec files, **+214 LOC**:

| File | New tests | Coverage |
|---|---|---|
| \`tests/unit/lib/openclaw-identity-cache.unit.spec.ts\` | +3
(storage-error silent-swallow + integration smoke for emit:true) | error
branches + cross-hook listener boundary |
| \`tests/unit/lib/auth/storage.unit.spec.ts\` | +5 (entire
\`clearUserStorage\` describe block) | sessionStorage.clear /
localStorage selective removeItem / PRESERVE_KEYS / firebase:* skip /
SSR no-op |
| \`tests/unit/lib/auth/manager.unit.spec.ts\` | +3 (entire
\`_completeLogin\` identity cleanup describe block) |
sessionStorage.removeItem(AGENT_IDENTITY_CACHE / CLAW_IDENTITY_CACHE),
localStorage.removeItem(agents/mattermost/agent-description),
Sentry.captureMessage on storage failure |

## Why this is needed before PR-C

\`clearUserStorage\` had **zero test coverage** before this PR.
\`_completeLogin\`'s identity cleanup block (manager.ts:232-247) was
likewise untested. PR-C will:
- swap \`sessionStorage.clear()\` for \`getQueryClient().clear()\`
(precise persister purge)
- delete the per-key \`sessionStorage.removeItem\` calls
(\`clearUserStorage\` will own all session-scoped purges)
- replace \`setCached*({emit: true}) → window.dispatchEvent → listener\`
with \`queryClient.setQueryData\` direct patch

Without Phase 0 lock-in, regressions in any of these would slip through
as silent behavior drift.

## Design discipline

Snapshot **post-fix** behavior (PR #1865/#1867 findings already
resolved). If characterization surfaces a leftover bug it goes to a
separate issue, not this PR — per [[feedback_test_as_bug_hunt]].

## Test plan

- [x] \`pnpm test:unit\` — 6042/6042 pass (1 todo)
- [x] \`pnpm lint\` — clean
- [x] \`npx tsc --noEmit\` — clean
- [x] \`pnpm lint:ci\` — dep-cruise + knip clean
- [x] PR-B (PERSIST_ALLOWLIST 改前缀 matcher, ~100-150 LOC) follows
- [x] PR-C (main migration, ~700-1000 LOC) follows PR-B

## Notes for reviewer

- The 3 new \`openclaw-identity-cache\` tests over-deliver slightly vs
spec estimate (15-25 LOC → 56 LOC) because the integration smoke test is
genuinely useful for locking the listener fanout boundary.
- The \`Sentry.captureMessage\` assertion in the manager test uses
\`.catch(() => undefined)\` because spying on
\`Storage.prototype.removeItem\` also breaks downstream
\`syncBusinessData\` — we only care that the Sentry call fires, not the
login outcome.

Refs #1998, #1868

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---
## [f07e801] refactor(web): customInputArea → props object (#1957) (#2005)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T06:19:50Z
- **PR**: #1957

### Commit Message
```
refactor(web): customInputArea → props object (#1957) (#2005)

## Summary
- 把 `AgentChatClient.customInputArea` render-prop 从 8-positional-param
改为单 props object,并把 prop 名对齐到同文件 `InputArea` 的 `on...`
前缀风格(`setInput`→`onInputChange` / `handleSubmit`→`onSendMessage` /
`messagesCount`→`messagesLength`),沿用 #1967 / #1969 / #1971 的
options-object 套路收口 issue #1957 第 4 条
- `eslint.config.mjs` 从 legacy complexity exemption block 整摘 `types.ts`
一行 —— 该文件全 type 声明无函数实现,移除后 `max-params` 重新生效且不引入新违例,无需 narrow
override(对比 #1971 pptx-parser)
- `grep -rn customInputArea` 验证整 monorepo 仅 4 命中(定义 + 解构 + ternary +
调用),全在 `agent-chat-client/` 内部,零 cross-package caller —— 这条 case 的 "外部
consumer 风险高" 标注属预防性

## Before / After

```diff
-customInputArea?: (
-  input: string,
-  setInput: (value: string) => void,
-  handleSubmit: () => void,
-  isLoading: boolean,
-  sessionId: string | null,
-  isInitializing: boolean,
-  isReadOnly: boolean,
-  messagesCount: number,
-) => React.ReactNode
+customInputArea?: (props: {
+  input: string
+  onInputChange: (value: string) => void
+  onSendMessage: () => void
+  isLoading: boolean
+  sessionId: string | null
+  isInitializing: boolean
+  isReadOnly: boolean
+  messagesLength: number
+}) => React.ReactNode
```

## Test plan
- [x] `pnpm install` 重新拉依赖
- [x] `npx eslint src/components/agent-chat-client/types.ts
src/components/agent-chat-client/index.tsx` 0 error
- [x] `npx tsc --noEmit` 0 error
- [x] `pnpm test:unit` agent-chat-client 范围 10 spec / 66 test 全绿
- [x] 4 个 shrink-only 守门脚本(forbid-dom-props / svg-inline / no-raw-fetch
/ filename-naming)全 pass
- [x] `grep -rn customInputArea` 验证无新增 caller

## 上下文
Issue #1957 跟踪 ESLint `max-params` (默认 4) 违例,F15 anti-pattern audit 期间扫出
7 个 case,本 PR 是序列第 4 个:
- ✅ #1967 `getSessionList`
- ✅ #1969 `reportLatency`
- ✅ #1971 `extractGroupShapes` + `mapChildToSlide`
- ➡️ 本 PR `customInputArea`
- ⏳ `PlanCard` 的 `getCtaConfig` / `getBadge` (BillingState 抽型一并解)
- ⏳ `useCanvasState` 的 `addPlaceholderNode` 5-param
- ⏳ `hasOverlap` (issue 标 acceptable)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---
## [7dd1346] fix(e2e): reduce flakiness in agent hire/fire and chat smoke flows (#1986)
- **作者**: rayhuang198212
- **日期**: 2026-05-28T05:41:46Z
- **PR**: #1986

### Commit Message
```
fix(e2e): reduce flakiness in agent hire/fire and chat smoke flows (#1986)

## Summary
- stabilize the agent hire/fire E2E flow by using per-test pages so each
scenario keeps its own Playwright video
- warm up the OpenClaw chat connection before entering agents manager
and reopen the target agent detail page in each scenario to avoid stale
session state
- add shared popup dismissal helpers for launch, guide tour, and login
modals that can block E2E interactions
- make PandaClaw response completion waits more tolerant of short
streaming pauses
- strengthen the chat smoke prompt so the response length assertion is
less flaky

## Root cause
The E2E suite had a few different sources of flakiness:
- the hire/fire spec reused shared page state across serial scenarios,
which made video capture and session continuity brittle
- several modal overlays could intermittently block clicks and typing
during test execution
- the response-complete heuristic could declare completion during short
mid-stream pauses, causing assertions to run on incomplete assistant
output
- the smoke test prompt sometimes produced responses that were too short
for the assertion budget

## Test plan
- [ ] `pnpm --filter web test:e2e -- agent-hire-fire.spec.ts`
- [ ] `pnpm --filter web test:e2e -- chat-smoke.spec.ts`
```

### PR Body
## Summary
- stabilize the agent hire/fire E2E flow by using per-test pages so each scenario keeps its own Playwright video
- warm up the OpenClaw chat connection before entering agents manager and reopen the target agent detail page in each scenario to avoid stale session state
- add shared popup dismissal helpers for launch, guide tour, and login modals that can block E2E interactions
- make PandaClaw response completion waits more tolerant of short streaming pauses
- strengthen the chat smoke prompt so the response length assertion is less flaky

## Root cause
The E2E suite had a few different sources of flakiness:
- the hire/fire spec reused shared page state across serial scenarios, which made video capture and session continuity brittle
- several modal overlays could intermittently block clicks and typing during test execution
- the response-complete heuristic could declare completion during short mid-stream pauses, causing assertions to run on incomplete assistant output
- the smoke test prompt sometimes produced responses that were too short for the assertion budget

## Test plan
- [ ] `pnpm --filter web test:e2e -- agent-hire-fire.spec.ts`
- [ ] `pnpm --filter web test:e2e -- chat-smoke.spec.ts`

---
## [046f1e8] refactor(web): persistQueryClient prototype for Bucket-1 (#1868) (#1990)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-28T05:39:59Z
- **PR**: #1868

### Commit Message
```
refactor(web): persistQueryClient prototype for Bucket-1 (#1868) (#1990)

## Summary

Phase 1 prototype for
[#1868](https://github.com/SerendipityOneInc/ecap-workspace/issues/1868)
(evaluation #1988 merged). Replaces `lib/agent-catalog-cache.ts` (manual
sessionStorage mirror of the official agent catalog) with
`@tanstack/react-query-persist-client` wired into `sessionStorage` via a
default-deny allowlist.

Currently the allowlist contains exactly one queryKey:
`agentCatalogOfficial()` — public, no token, no uid. This is the safest
Bucket-1 target per the queryKey×token audit in [the evaluation
spec](docs/superpowers/specs/2026-05-27-rq-persist-client-evaluation.md).
Bucket 2/3/4 expansions are tracked in follow-up issues.

## Changes

- **New**: `lib/query/persist-client.ts` — `shouldDehydrateQuery`
allowlist, `getPersistOptions()` returning `{ persister, maxAge: 24h,
buster: QUERY_VERSION, dehydrateOptions }`. SSR-guarded.
- **New**: `lib/query/keys.ts::AGENT_CATALOG_OFFICIAL_QUERY_KEY` —
hoisted from `hooks/queries/openclaw/keys.ts` so the persister allowlist
+ sync lookup shim (both in `lib/`) can reference it without crossing
W1-lib-pure (lib/ may not import from hooks/).
`openclawKeys.agentCatalogOfficial()` returns the same constant.
- **Modified**: `ClientLayout.tsx` swaps `QueryClientProvider` for
`PersistQueryClientProvider`. Falls back to plain provider during SSR
(`persistOptions === null`).
- **Modified**: `lib/query/query-client.ts` adds `getQueryClient()`
module-level singleton. Required so the sync lookup helpers in
`agent-catalog-cache.ts` (consumed from `lib/use-cases.ts` +
`MarkdownContent.tsx`'s lazy-loaded imperative path) read from the same
QueryClient as the Provider.
- **Slimmed**: `lib/agent-catalog-cache.ts` 47 → 33 lines — write side /
`readAgentCatalogCache` deleted; lookup helpers
(`getCatalogAgentDisplayName/Animal/Tagline/AvatarUrl`) now read from RQ
cache via singleton.
- **Slimmed**: `useOfficialAgentCatalog.ts` 78 → 26 lines — drops
`initialData`, custom event listener, cross-tab storage event listener.
Persister handles rehydrate.
- **Modified**: `lib/api/openclaw.ts` drops
`writeAgentCatalogCache(payload.agents)` side-effect — RQ's `queryFn`
return value populates the cache directly.
- **Modified**: `lib/auth/manager.ts` drops
`localStorage.removeItem(AGENTS_CATALOG_CACHE)` on login (catalog is
identity-agnostic public data; per-tab sessionStorage replacement means
no cross-account leak surface).

## Test changes

- **New** `persist-client.unit.spec.ts` (12 tests): allowlist filtering
(token-keyed / uid-keyed / unknown / prefix rejections), config shape,
restore paths (rehydrate / buster mismatch / maxAge expiry / cold start
no-op).
- **Slimmed** `agent-catalog-cache.unit.spec.ts`: 15 → 5 tests. Write
side removed; lookup tests now seed via `setQueryData` on the singleton.
- **Slimmed** `useOfficialAgentCatalog.unit.spec.ts`: 10 → 5 tests.
Listener regression tests (custom event / cross-tab /
removeItem-invalidate) replaced by persister coverage.
- **Slimmed** `openclaw-extras.unit.spec.ts`: drops
`writeAgentCatalogCache` side-effect assertions on the API helper.

## Behavioral diff

- **Same**: hard-refresh first-paint shows the cached catalog (UX
preserved — just rehydrated via RQ persister instead of manual
`readAgentCatalogCache + initialData`).
- **Lost (acceptable)**: cross-tab same-session sync. Previously tab A's
catalog write fired a `storage` event that tab B mirrored via
`setQueryData`. Now tab B's persister sessionStorage is independent; tab
B refreshes its catalog on its own `refetchOnMount: 'always'` + 30s
`staleTime`. Public catalog is low-frequency change so this is a
non-issue.
- **Lost (acceptable)**: on-error preservation of prior cached data.
Previously `initialData` kept the localStorage seed visible if the
refetch errored. Now `items: query.data ?? []` returns `[]` on cold
error — consistent with the rest of the RQ-migrated hooks per
`react-query-migration.md`.

## Test plan

- [x] `pnpm test:unit` — 399 files / 6022 tests green (1 todo)
- [x] `pnpm lint` — clean
- [x] `npx tsc --noEmit` — clean (aligned `@tanstack/react-query` to
5.100.11 to match `query-persist-client-core`)
- [x] `pnpm lint:ci` — dep-cruiser W1-lib-pure + knip dep-health gates
pass
- [ ] **Manual on staging**: hard-refresh chat page → catalog visible
immediately (Network shows fetch still issued but UI not blank);
DevTools → `sessionStorage['ecap:rq-cache']` payload grep clean of
`Bearer ` / token-shaped strings.

## Notes for reviewer

- The module-level singleton in `query-client.ts` is the load-bearing
decision — required because `lib/use-cases.ts` lookup helpers are called
from `.map` callbacks and lazy-loaded `MarkdownContent` paths that have
no React context. Existing consumer tests already mock `@/lib/use-cases`
or `@/lib/agent-catalog-cache`, so the singleton doesn't leak into test
isolation.
- Persister default-deny is enforced by `shouldDehydrateQuery` returning
`true` ONLY when `queryKey.length === allowlist[i].length && every
segment ===`. Prefix match is explicitly tested and rejected (locks
against accidental persistence when Bucket-2 adds longer keys).
- `dependency-cruiser` W1-lib-pure required hoisting the queryKey
constant to `lib/query/keys.ts` — `openclawKeys.agentCatalogOfficial()`
re-exports it so the rest of the codebase doesn't change.
- Do not auto-merge — confirm manual staging verification first.

Refs #1868, #1988

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---
## [87a6a5c] feat(billing): add v2 payment core services (#1994)
- **作者**: kaka-srp
- **日期**: 2026-05-28T03:15:00Z
- **PR**: #1994

### Commit Message
```
feat(billing): add v2 payment core services (#1994)

## Linear

https://linear.app/srpone/issue/ECA-842/billing-v2-subscription-architecture-refactor

## Summary
- add dormant Billing v2 core services for deterministic payment orders,
subscription agreements, entitlement ledger records, and BG grant/revoke
transaction ids
- add repo upsert/provider lookup helpers for payment, subscription, and
entitlement collections
- enforce paid amount/currency validation, provider subscription
ownership, one-current-agreement guard, scheduled downgrade/cancel/apply
behavior, subscription-code redemption guard, trial entitlement paths,
and refund revoke idempotency

## Rollout notes
- This PR does not wire the new core services into Stripe, Antom, Apple,
web routes, cron, or any feature flag. Existing production
payment/subscription paths keep using the legacy implementation.
- Safe to merge as an intermediate-stage PR: it only adds dormant
service/repo helpers plus tests. It will not create, mutate, or read
Billing v2 payment/subscription/entitlement documents unless a later
integration PR explicitly calls these services.
- Apple compatibility is covered at the core layer by treating iOS
originalTransactionId as the provider subscription owner id; web
frontend compatibility is not changed in this PR.

## Test plan
- [x] cd services/claw-interface && ruff check .
- [x] cd services/claw-interface && pyright app tests
- [x] cd services/claw-interface && pytest
tests/unit/test_billing_v2_state.py
tests/unit/test_billing_v2_transitions.py
tests/unit/test_billing_v2_repos.py
tests/unit/test_billing_summary_v2.py
tests/unit/test_billing_v2_payment_orders.py
tests/unit/test_billing_v2_subscription_agreements.py
tests/unit/test_billing_v2_entitlements.py
- [x] cd services/claw-interface && ruff format --check
app/services/billing_v2 app/database/payment_order_repo.py
app/database/subscription_agreement_repo.py
app/database/entitlement_ledger_repo.py
tests/unit/test_billing_v2_repos.py
tests/unit/test_billing_v2_payment_orders.py
tests/unit/test_billing_v2_subscription_agreements.py
tests/unit/test_billing_v2_entitlements.py
```

### PR Body
## Linear
https://linear.app/srpone/issue/ECA-842/billing-v2-subscription-architecture-refactor

## Summary
- add dormant Billing v2 core services for deterministic payment orders, subscription agreements, entitlement ledger records, and BG grant/revoke transaction ids
- add repo upsert/provider lookup helpers for payment, subscription, and entitlement collections
- enforce paid amount/currency validation, provider subscription ownership, one-current-agreement guard, scheduled downgrade/cancel/apply behavior, subscription-code redemption guard, trial entitlement paths, and refund revoke idempotency

## Rollout notes
- This PR does not wire the new core services into Stripe, Antom, Apple, web routes, cron, or any feature flag. Existing production payment/subscription paths keep using the legacy implementation.
- Safe to merge as an intermediate-stage PR: it only adds dormant service/repo helpers plus tests. It will not create, mutate, or read Billing v2 payment/subscription/entitlement documents unless a later integration PR explicitly calls these services.
- Apple compatibility is covered at the core layer by treating iOS originalTransactionId as the provider subscription owner id; web frontend compatibility is not changed in this PR.

## Test plan
- [x] cd services/claw-interface && ruff check .
- [x] cd services/claw-interface && pyright app tests
- [x] cd services/claw-interface && pytest tests/unit/test_billing_v2_state.py tests/unit/test_billing_v2_transitions.py tests/unit/test_billing_v2_repos.py tests/unit/test_billing_summary_v2.py tests/unit/test_billing_v2_payment_orders.py tests/unit/test_billing_v2_subscription_agreements.py tests/unit/test_billing_v2_entitlements.py
- [x] cd services/claw-interface && ruff format --check app/services/billing_v2 app/database/payment_order_repo.py app/database/subscription_agreement_repo.py app/database/entitlement_ledger_repo.py tests/unit/test_billing_v2_repos.py tests/unit/test_billing_v2_payment_orders.py tests/unit/test_billing_v2_subscription_agreements.py tests/unit/test_billing_v2_entitlements.py
