# ecap-workspace Commits — 2026-05-16

共 6 条 commits

---

## [1] Use public warm-pool account service routes (#1718)

- **SHA**: `d33c02a4e817303450539945a3577dcb0fe1f2ea`
- **作者**: tim-srp
- **日期**: 2026-05-16T17:45:15Z
- **PR**: #1718

### 完整 Commit Message

```
Use public warm-pool account service routes (#1718)

## Summary\n- switch warm-pool account service calls from to \n- align
claw-interface with the new user-interface service routes\n\n##
Testing\n-

services/claw-interface/tests/unit/test_warm_pool.py::test_warm_pool_cron_requires_key
-------------------------------- live log setup
--------------------------------
[INIT] Using gem_account collection (auto-routed to gem-sensitive
database)
[LITELLM_SDK] Configured with:
  API Base: 
  API Key: Not set
-------------------------------- live log call
---------------------------------
Handled HTTP request /cron/warm-pool-provision
PASSED [ 9%]

services/claw-interface/tests/unit/test_warm_pool.py::test_warm_pool_cron_accepts_key
-------------------------------- live log call
---------------------------------
Handled HTTP request /cron/warm-pool-provision
PASSED [ 18%]

services/claw-interface/tests/unit/test_warm_pool.py::test_warm_pool_status_endpoint
-------------------------------- live log call
---------------------------------
Handled HTTP request /admin/warm-pool/status
PASSED [ 27%]

services/claw-interface/tests/unit/test_warm_pool.py::test_account_service_calls_use_admin_secret_and_payloads
PASSED [ 36%]

services/claw-interface/tests/unit/test_warm_pool.py::test_warm_pool_repo_query_shapes_and_indexes
-------------------------------- live log call
---------------------------------
[STARTUP] Ensured warm-pool indexes
PASSED [ 45%]

services/claw-interface/tests/unit/test_warm_pool.py::test_cleanup_paths_process_expired_and_failed_entries
PASSED [ 54%]

services/claw-interface/tests/unit/test_warm_pool.py::test_provision_warm_pool_creates_entry_with_absolute_expiry
PASSED [ 63%]

services/claw-interface/tests/unit/test_warm_pool.py::test_provision_one_entry_advances_all_stages_and_marks_ready
PASSED [ 72%]

services/claw-interface/tests/unit/test_warm_pool.py::test_maybe_finalize_claims_ready_entry
PASSED [ 81%]

services/claw-interface/tests/unit/test_warm_pool.py::test_maybe_finalize_retries_claimed_unfinished_entry
PASSED [ 90%]

services/claw-interface/tests/unit/test_warm_pool.py::test_finalize_registration_reuses_pre_increment_open_exempt_decision
PASSED [100%]

============================== 11 passed in 3.34s
==============================
```

### PR Body

## Summary\n- switch warm-pool account service calls from  to \n- align claw-interface with the new user-interface service routes\n\n## Testing\n- 
services/claw-interface/tests/unit/test_warm_pool.py::test_warm_pool_cron_requires_key 
-------------------------------- live log setup --------------------------------
[INIT] Using gem_account collection (auto-routed to gem-sensitive database)
[LITELLM_SDK] Configured with:
  API Base: 
  API Key: Not set
-------------------------------- live log call ---------------------------------
Handled HTTP request /cron/warm-pool-provision
PASSED                                                                   [  9%]
services/claw-interface/tests/unit/test_warm_pool.py::test_warm_pool_cron_accepts_key 
-------------------------------- live log call ---------------------------------
Handled HTTP request /cron/warm-pool-provision
PASSED                                                                   [ 18%]
services/claw-interface/tests/unit/test_warm_pool.py::test_warm_pool_status_endpoint 
-------------------------------- live log call ---------------------------------
Handled HTTP request /admin/warm-pool/status
PASSED                                                                   [ 27%]
services/claw-interface/tests/unit/test_warm_pool.py::test_account_service_calls_use_admin_secret_and_payloads PASSED [ 36%]
services/claw-interface/tests/unit/test_warm_pool.py::test_warm_pool_repo_query_shapes_and_indexes 
-------------------------------- live log call ---------------------------------
[STARTUP] Ensured warm-pool indexes
PASSED                                                                   [ 45%]
services/claw-interface/tests/unit/test_warm_pool.py::test_cleanup_paths_process_expired_and_failed_entries PASSED [ 54%]
services/claw-interface/tests/unit/test_warm_pool.py::test_provision_warm_pool_creates_entry_with_absolute_expiry PASSED [ 63%]
services/claw-interface/tests/unit/test_warm_pool.py::test_provision_one_entry_advances_all_stages_and_marks_ready PASSED [ 72%]
services/claw-interface/tests/unit/test_warm_pool.py::test_maybe_finalize_claims_ready_entry PASSED [ 81%]
services/claw-interface/tests/unit/test_warm_pool.py::test_maybe_finalize_retries_claimed_unfinished_entry PASSED [ 90%]
services/claw-interface/tests/unit/test_warm_pool.py::test_finalize_registration_reuses_pre_increment_open_exempt_decision PASSED [100%]

============================== 11 passed in 3.34s ==============================

---

## [2] Move warm-pool cron endpoint out of admin (#1717)

- **SHA**: `5b0b2b9bbfa54572a05f856adb7ef72304c532da`
- **作者**: tim-srp
- **日期**: 2026-05-16T17:22:41Z
- **PR**: #1717

### 完整 Commit Message

```
Move warm-pool cron endpoint out of admin (#1717)

## Summary
- move the warm-pool trigger from `/admin/cron/warm-pool-provision` to
`/cron/warm-pool-provision`
- keep the existing warm-pool service-key auth on the new public route
- leave the rest of the admin cron surface unchanged

## Testing
- `python -m pytest services/claw-interface/tests/unit/test_warm_pool.py
-q -W ignore::PendingDeprecationWarning`

## Notes
- this is split into a dedicated PR so it does not carry the broader
warm-pool branch history
```

### PR Body

## Summary
- move the warm-pool trigger from `/admin/cron/warm-pool-provision` to `/cron/warm-pool-provision`
- keep the existing warm-pool service-key auth on the new public route
- leave the rest of the admin cron surface unchanged

## Testing
- `python -m pytest services/claw-interface/tests/unit/test_warm_pool.py -q -W ignore::PendingDeprecationWarning`

## Notes
- this is split into a dedicated PR so it does not carry the broader warm-pool branch history

---

## [3] Implement warm-pool provisioning in claw-interface (#1715)

- **SHA**: `878e408637e4f0eb1de91c2d188533f0e388847d`
- **作者**: tim-srp
- **日期**: 2026-05-16T15:29:11Z
- **PR**: #1715

### 完整 Commit Message

```
Implement warm-pool provisioning in claw-interface (#1715)

## Summary
- add warm-pool repo, schema, account-service client, and provisioner
- add warm-pool cron/status endpoints and dedicated key-only auth
- finalize claimed warm-pool registrations in /users/create and add
coverage tests

## Testing
- pytest -W ignore::PendingDeprecationWarning
services/claw-interface/tests/unit/test_warm_pool.py
services/claw-interface/tests/unit/test_user_routes_coverage.py -q
- bash services/claw-interface/scripts/ci-lint/01-file-length.sh
- bash services/claw-interface/scripts/ci-lint/02-import-linter.sh
```

### PR Body

## Summary
- add warm-pool repo, schema, account-service client, and provisioner
- add warm-pool cron/status endpoints and dedicated key-only auth
- finalize claimed warm-pool registrations in /users/create and add coverage tests

## Testing
- pytest -W ignore::PendingDeprecationWarning services/claw-interface/tests/unit/test_warm_pool.py services/claw-interface/tests/unit/test_user_routes_coverage.py -q
- bash services/claw-interface/scripts/ci-lint/01-file-length.sh
- bash services/claw-interface/scripts/ci-lint/02-import-linter.sh

---

## [4] refactor(web): Nest pnpm workspace under web/ for multi-app future (#1713)

- **SHA**: `078558dfbd3b84c890adc458f7ea443154347cc8`
- **作者**: bill-srp
- **日期**: 2026-05-16T12:33:44Z
- **PR**: #1713

### 完整 Commit Message

```
refactor(web): Nest pnpm workspace under web/ for multi-app future (#1713)

## Summary

Restructures the repo so `web/` becomes the pnpm workspace root and the
existing Next.js app is nested at `web/app/`. Repo root reverts to a
polyglot container with **no** Node-adjacent files (`package.json`,
`pnpm-workspace.yaml`, `pnpm-lock.yaml`, `.npmrc`, `.husky/`,
`node_modules/` — all gone from root).

This unblocks scaffolding additional apps (`web/enterprise-admin`,
`web/enterprise-app`) and lazy-extracted shared packages
(`web/packages/*`) on their own hostnames in future PRs, without
bundling those into this PR.

**Design docs:**
- Spec:
[`docs/superpowers/specs/2026-05-15-web-nested-workspace.md`](../blob/feat/web-workspace/docs/superpowers/specs/2026-05-15-web-nested-workspace.md)
- Plan:
[`docs/superpowers/plans/2026-05-15-web-nested-workspace.md`](../blob/feat/web-workspace/docs/superpowers/plans/2026-05-15-web-nested-workspace.md)

## Endstate

```
ecap-workspace/
├── (no Node-adjacent files at root)
├── web/
│   ├── package.json            # workspace root: @zooclaw/web, pnpm.overrides, husky+sharp devdeps
│   ├── pnpm-workspace.yaml     # packages: ['app']
│   ├── pnpm-lock.yaml          # the single lockfile
│   ├── .npmrc                  # public-hoist patterns
│   ├── .husky/{pre-commit,pre-push}
│   ├── scripts/check-asset-size.mjs   # uses sharp via web/node_modules
│   ├── AGENTS.md  CLAUDE.md    # NEW workspace-tier docs
│   └── app/                    # @zooclaw/web-app — the Next.js app (what was web/*)
├── services/                   # Python, unaffected
└── …
```

## Commits (15 migration + 1 unrelated fix + polish — read in order)

| # | SHA | Type | Notes |
|---|-----|------|-------|
| 1 | `c05d74bc` | docs | Relocate impl plan to
`docs/superpowers/plans/` (setup) |
| 2 | `e82f577a` | refactor | Bulk rename `web/*` → `web/app/*` + lift
`.npmrc` to workspace root |
| 3 | `69d4af39` | refactor | Move `.husky/` → `web/.husky/` |
| 4 | `05ba7c30` | refactor | Create `web/pnpm-workspace.yaml` |
| 5 | `b4a66bbd` | refactor | Create `web/package.json` workspace root
(overrides + delegation scripts + sharp devdep) |
| 6 | `b8591662` | refactor | Rename app package → `@zooclaw/web-app`,
drop `packageManager` pin |
| 7 | `7ea52bc2` | **fix** | **⚠️ Unrelated**: Tailwind class order in
`GenClawInput.tsx` — pre-existing nit the now-active hook caught during
commit 8. See "Known caveats" below |
| 8 | `873c8c8a` | refactor | Generate `web/pnpm-lock.yaml` |
| 9 | `1914b0ea` | refactor | Remove root Node files |
| 10 | `c5cf7240` | refactor | Point husky pre-commit at `web/app/`
paths |
| 11 | `5d04f941` | refactor | Move `check-asset-size.mjs` under `web/`,
update devcontainer + worktree-setup |
| 12 | `f83517f4` | ci | Update CI workflows (`code-quality`, `e2e`,
`deploy`, `dependabot-lockfile-refresh`) |
| 13 | `3f3df06a` | ci | Update review/automation workflows
(`claude-review`, `claude-arch-review`, `claude-develop`,
`codex-review`) |
| 14 | `387ba9ff` | ci | `dependabot.yml` comment refs
`web/pnpm-workspace.yaml` |
| 15 | `2505a727` | ci | Delete `deploy-oauth-worker.yml` (oauth-worker
archived; no install path post-migration) |
| 16 | `214e7595` | docs | Add `web/AGENTS.md` (workspace-tier) + update
root sub-project pointer |
| 17 | `07b3954a` | refactor | Add dual-path fallback in 4 shrink-only
scripts (mid-migration CI compat) |
| 18 | `be28a49d` | docs | Fix stale path refs in comments after rename
|

## After pulling this PR

```bash
rm -rf node_modules
cd web && pnpm install
```

This is required because the husky `prepare` script writes
`core.hooksPath=web/.husky/_` into `.git/config`. Without re-running
install, your hooks will silently skip.

## Known caveats

1. **Commit 7 (`7ea52bc2`) is an unrelated `fix(web)` Tailwind
class-order fix.** It's a 1-line change in `GenClawInput.tsx` that
pre-dates this PR but only surfaced because Task 6's `pnpm install`
re-activated the husky hook mid-migration and lint caught it. Including
it here avoided a hook bypass on the lockfile commit. Cleanly separable
if a reviewer wants to cherry-pick it out, but its scope is trivial.
2. **Spec deviation**: `scripts/check-asset-size.mjs` was moved to
`web/scripts/check-asset-size.mjs` and `sharp` was added to
`web/package.json` workspace-root devdeps. The original spec missed this
— without it, Node ESM resolution from the script can't find `sharp`
post-migration (root `node_modules/` is gone). Documented at the top of
the plan.
3. **`web/app/cloudflare-env.d.ts` was NOT regenerated.** Running
`wrangler types` locally produced ~7k lines of unrelated drift
(Cloudflare runtime types have evolved since the file was last
regenerated). Out of scope here; will be handled in a separate
doc/refresh PR.

## Follow-up PR (separate, post-merge)

After this PR merges to main, a small follow-up PR removes the dual-path
fallback in the 4 shrink-only scripts (the `else` branch becomes
unreachable once `origin/main` has the new path). Roughly 10-line diff
across 4 files.

## Verified locally

- ✅ `cd web && pnpm install --frozen-lockfile` (3.1s warm)
- ✅ `pnpm lint` via delegation script
- ✅ `pnpm tsc` (clean — needs `rm -rf web/app/.next` first if you hit
stale `.next/types/route.ts` errors; that's a generic Next.js cache
hazard)
- ✅ `pnpm test:unit` (5496 tests pass)
- ✅ `pnpm exec wrangler types` (reads `web/app/wrangler.jsonc`)
- ✅ Pre-commit hook fires on staged `web/app/public/` and `web/app/`
files
- ✅ Pre-push hook fires on `git push --dry-run`
- ⏭️ `pnpm build` skipped (requires Firebase env not present on macOS
host; CI exercises it)

## Test plan

- [ ] `code-quality / lint-and-test` passes
- [ ] `e2e` passes (Playwright from `web/app/`)
- [ ] `deploy` (staging) succeeds (wrangler `workingDirectory: web/app`)
- [ ] Devcontainer rebuild produces a working dev environment
- [ ] `bash scripts/worktree.sh --node smoke-test` creates a worktree
with deps installed and hooks configured
- [ ] After merge: synthetic Dependabot bump on `web/app/package.json`
triggers `dependabot-lockfile-refresh.yml`
- [ ] After merge: synthetic Dependabot bump on `web/package.json` (root
devdep like `husky`) triggers the same workflow
```

### PR Body

## Summary

Restructures the repo so `web/` becomes the pnpm workspace root and the existing Next.js app is nested at `web/app/`. Repo root reverts to a polyglot container with **no** Node-adjacent files (`package.json`, `pnpm-workspace.yaml`, `pnpm-lock.yaml`, `.npmrc`, `.husky/`, `node_modules/` — all gone from root).

This unblocks scaffolding additional apps (`web/enterprise-admin`, `web/enterprise-app`) and lazy-extracted shared packages (`web/packages/*`) on their own hostnames in future PRs, without bundling those into this PR.

**Design docs:**
- Spec: [`docs/superpowers/specs/2026-05-15-web-nested-workspace.md`](../blob/feat/web-workspace/docs/superpowers/specs/2026-05-15-web-nested-workspace.md)
- Plan: [`docs/superpowers/plans/2026-05-15-web-nested-workspace.md`](../blob/feat/web-workspace/docs/superpowers/plans/2026-05-15-web-nested-workspace.md)

## Endstate

```
ecap-workspace/
├── (no Node-adjacent files at root)
├── web/
│   ├── package.json            # workspace root: @zooclaw/web, pnpm.overrides, husky+sharp devdeps
│   ├── pnpm-workspace.yaml     # packages: ['app']
│   ├── pnpm-lock.yaml          # the single lockfile
│   ├── .npmrc                  # public-hoist patterns
│   ├── .husky/{pre-commit,pre-push}
│   ├── scripts/check-asset-size.mjs   # uses sharp via web/node_modules
│   ├── AGENTS.md  CLAUDE.md    # NEW workspace-tier docs
│   └── app/                    # @zooclaw/web-app — the Next.js app (what was web/*)
├── services/                   # Python, unaffected
└── …
```

## Commits (15 migration + 1 unrelated fix + polish — read in order)

| # | SHA | Type | Notes |
|---|-----|------|-------|
| 1 | `c05d74bc` | docs | Relocate impl plan to `docs/superpowers/plans/` (setup) |
| 2 | `e82f577a` | refactor | Bulk rename `web/*` → `web/app/*` + lift `.npmrc` to workspace root |
| 3 | `69d4af39` | refactor | Move `.husky/` → `web/.husky/` |
| 4 | `05ba7c30` | refactor | Create `web/pnpm-workspace.yaml` |
| 5 | `b4a66bbd` | refactor | Create `web/package.json` workspace root (overrides + delegation scripts + sharp devdep) |
| 6 | `b8591662` | refactor | Rename app package → `@zooclaw/web-app`, drop `packageManager` pin |
| 7 | `7ea52bc2` | **fix** | **⚠️ Unrelated**: Tailwind class order in `GenClawInput.tsx` — pre-existing nit the now-active hook caught during commit 8. See "Known caveats" below |
| 8 | `873c8c8a` | refactor | Generate `web/pnpm-lock.yaml` |
| 9 | `1914b0ea` | refactor | Remove root Node files |
| 10 | `c5cf7240` | refactor | Point husky pre-commit at `web/app/` paths |
| 11 | `5d04f941` | refactor | Move `check-asset-size.mjs` under `web/`, update devcontainer + worktree-setup |
| 12 | `f83517f4` | ci | Update CI workflows (`code-quality`, `e2e`, `deploy`, `dependabot-lockfile-refresh`) |
| 13 | `3f3df06a` | ci | Update review/automation workflows (`claude-review`, `claude-arch-review`, `claude-develop`, `codex-review`) |
| 14 | `387ba9ff` | ci | `dependabot.yml` comment refs `web/pnpm-workspace.yaml` |
| 15 | `2505a727` | ci | Delete `deploy-oauth-worker.yml` (oauth-worker archived; no install path post-migration) |
| 16 | `214e7595` | docs | Add `web/AGENTS.md` (workspace-tier) + update root sub-project pointer |
| 17 | `07b3954a` | refactor | Add dual-path fallback in 4 shrink-only scripts (mid-migration CI compat) |
| 18 | `be28a49d` | docs | Fix stale path refs in comments after rename |

## After pulling this PR

```bash
rm -rf node_modules
cd web && pnpm install
```

This is required because the husky `prepare` script writes `core.hooksPath=web/.husky/_` into `.git/config`. Without re-running install, your hooks will silently skip.

## Known caveats

1. **Commit 7 (`7ea52bc2`) is an unrelated `fix(web)` Tailwind class-order fix.** It's a 1-line change in `GenClawInput.tsx` that pre-dates this PR but only surfaced because Task 6's `pnpm install` re-activated the husky hook mid-migration and lint caught it. Including it here avoided a hook bypass on the lockfile commit. Cleanly separable if a reviewer wants to cherry-pick it out, but its scope is trivial.
2. **Spec deviation**: `scripts/check-asset-size.mjs` was moved to `web/scripts/check-asset-size.mjs` and `sharp` was added to `web/package.json` workspace-root devdeps. The original spec missed this — without it, Node ESM resolution from the script can't find `sharp` post-migration (root `node_modules/` is gone). Documented at the top of the plan.
3. **`web/app/cloudflare-env.d.ts` was NOT regenerated.** Running `wrangler types` locally produced ~7k lines of unrelated drift (Cloudflare runtime types have evolved since the file was last regenerated). Out of scope here; will be handled in a separate doc/refresh PR.

## Follow-up PR (separate, post-merge)

After this PR merges to main, a small follow-up PR removes the dual-path fallback in the 4 shrink-only scripts (the `else` branch becomes unreachable once `origin/main` has the new path). Roughly 10-line diff across 4 files.

## Verified locally

- ✅ `cd web && pnpm install --frozen-lockfile` (3.1s warm)
- ✅ `pnpm lint` via delegation script
- ✅ `pnpm tsc` (clean — needs `rm -rf web/app/.next` first if you hit stale `.next/types/route.ts` errors; that's a generic Next.js cache hazard)
- ✅ `pnpm test:unit` (5496 tests pass)
- ✅ `pnpm exec wrangler types` (reads `web/app/wrangler.jsonc`)
- ✅ Pre-commit hook fires on staged `web/app/public/` and `web/app/` files
- ✅ Pre-push hook fires on `git push --dry-run`
- ⏭️ `pnpm build` skipped (requires Firebase env not present on macOS host; CI exercises it)

## Test plan

- [ ] `code-quality / lint-and-test` passes
- [ ] `e2e` passes (Playwright from `web/app/`)
- [ ] `deploy` (staging) succeeds (wrangler `workingDirectory: web/app`)
- [ ] Devcontainer rebuild produces a working dev environment
- [ ] `bash scripts/worktree.sh --node smoke-test` creates a worktree with deps installed and hooks configured
- [ ] After merge: synthetic Dependabot bump on `web/app/package.json` triggers `dependabot-lockfile-refresh.yml`
- [ ] After merge: synthetic Dependabot bump on `web/package.json` (root devdep like `husky`) triggers the same workflow

---

## [5] refactor(web): destructure ws / mm fields into stable locals (#1526 F partial) (#1698)

- **SHA**: `d3614e43aae90b677098aaa99ddee382b53febce`
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-16T06:00:36Z
- **PR**: #1698

### 完整 Commit Message

```
refactor(web): destructure ws / mm fields into stable locals (#1526 F partial) (#1698)

## Summary

Treats most of the **F bucket** of issue #1526. -10 disables,
\`web/src\` now at **23 / 41**.

The wrapper objects \`ws\` (from \`useOpenClawWs\`) and \`mm\` (from
\`useMattermost\`) get a new reference every render — their individual
fields are state/useCallback at the source, but the wrapper itself
churns. Callers were forced to either:

1. include the whole \`ws\` / \`mm\` in effect deps → over-fires every
render, or
2. suppress \`exhaustive-deps\` to pass property reads like
\`[ws.status, ws.sendRequest]\` → silent suppression

**Why this didn't work without code changes**:
\`eslint-plugin-react-hooks@5.2.0\` (pinned via #1528) demands the whole
wrapper in deps when any \`ws.x\` / \`mm.x\` appears in the body.
Property-path deps aren't accepted as a substitute — verified by
experiment.

**Fix shape**: destructure stable fields into plain locals at the top of
each hook/provider, replace \`ws.x\` / \`mm.x\` in body **and** deps
with the locals. ESLint accepts plain identifiers in deps. The locals
are referentially stable because the underlying useState/useCallback in
the source hook is stable — only the wrapper churn was the problem.

## Files

| File | Disables removed | Notes |
|---|---|---|
| \`useSubagentChat.ts\` | 2 (lines 194, 208) | destructure \`status\` /
\`sendRequest\` |
| \`useOpenClawChat.ts\` | 4 (lines 264, 697, 765, 793) | destructure 8
fields incl. \`chatCacheRef\` |
| \`MattermostProvider.tsx\` | 2 (lines 97, 127) | destructure 4
effect-used fields + drop cargo-cult \`useMemo\` on context value |
| \`OpenClawProvider.tsx\` | 3 (lines 62, 75, 161) | destructure 7 ws
fields; bot effect deps simplified to \`[bot]\` (idempotent sentry
context set) |

### Side-effect: dropped \`useMemo\` around \`MattermostProvider\` value

The pre-existing \`useMemo(() => ({ ...mm, mmBots, refreshBots }),
[mm.connectionState, ...])\` listed 24 field-level deps with an
\`eslint-disable\`. Reading it carefully, the memo was cargo-cult:
\`mm\` is a fresh ref every render, so any memo over \`{ ...mm }\`
rebuilds every render too — the \`useMemo\` was a no-op wearing a
costume. Removed it; replaced with a plain object construction. Behavior
is identical, suppression is gone.

## Deferred (kept disables)

* **\`useMattermostIntegration.ts\`** — destructuring the 11 \`mm\`
fields used in the function pushes the ~290-line
\`useMattermostIntegration\` over the 300-line
\`max-lines-per-function\` ceiling by exactly 1 line. Tried
prettier-ignore single-line destructure; still +1. The right fix is to
decompose this function (or extract a \`useMmStableFields\` helper) —
separate PR. **Keeps 3 F-bucket disables there** + 1 A-bucket disable
that requires useEffectEvent (blocked by plugin version, tracked in
#1539).

* **OpenClawProvider:62 (bot sentry effect)** — switched deps from
\`[bot?.bot_id, bot?.bot_name, bot?.webchat_url]\` to \`[bot]\`. The bot
ref churns whenever \`useOpenClawInit\` re-renders, but
\`setSentryBotContext\` is idempotent for identical content. Net: more
frequent (but harmless) Sentry context sets vs. one suppression removed.

## Test plan
- [x] \`pnpm lint\` passes
- [x] \`npx tsc --noEmit\` passes
- [x] \`pnpm test:unit\` — all 343 spec files / 5444 tests pass
- [ ] CI \`web-quality\` green
- [ ] Manual sanity: agent chat (send/abort), subagent chat panel,
mattermost connection / message send, Sentry bot context still populated

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

Treats most of the **F bucket** of issue #1526. -10 disables, \`web/src\` now at **23 / 41**.

The wrapper objects \`ws\` (from \`useOpenClawWs\`) and \`mm\` (from \`useMattermost\`) get a new reference every render — their individual fields are state/useCallback at the source, but the wrapper itself churns. Callers were forced to either:

1. include the whole \`ws\` / \`mm\` in effect deps → over-fires every render, or
2. suppress \`exhaustive-deps\` to pass property reads like \`[ws.status, ws.sendRequest]\` → silent suppression

**Why this didn't work without code changes**: \`eslint-plugin-react-hooks@5.2.0\` (pinned via #1528) demands the whole wrapper in deps when any \`ws.x\` / \`mm.x\` appears in the body. Property-path deps aren't accepted as a substitute — verified by experiment.

**Fix shape**: destructure stable fields into plain locals at the top of each hook/provider, replace \`ws.x\` / \`mm.x\` in body **and** deps with the locals. ESLint accepts plain identifiers in deps. The locals are referentially stable because the underlying useState/useCallback in the source hook is stable — only the wrapper churn was the problem.

## Files

| File | Disables removed | Notes |
|---|---|---|
| \`useSubagentChat.ts\` | 2 (lines 194, 208) | destructure \`status\` / \`sendRequest\` |
| \`useOpenClawChat.ts\` | 4 (lines 264, 697, 765, 793) | destructure 8 fields incl. \`chatCacheRef\` |
| \`MattermostProvider.tsx\` | 2 (lines 97, 127) | destructure 4 effect-used fields + drop cargo-cult \`useMemo\` on context value |
| \`OpenClawProvider.tsx\` | 3 (lines 62, 75, 161) | destructure 7 ws fields; bot effect deps simplified to \`[bot]\` (idempotent sentry context set) |

### Side-effect: dropped \`useMemo\` around \`MattermostProvider\` value

The pre-existing \`useMemo(() => ({ ...mm, mmBots, refreshBots }), [mm.connectionState, ...])\` listed 24 field-level deps with an \`eslint-disable\`. Reading it carefully, the memo was cargo-cult: \`mm\` is a fresh ref every render, so any memo over \`{ ...mm }\` rebuilds every render too — the \`useMemo\` was a no-op wearing a costume. Removed it; replaced with a plain object construction. Behavior is identical, suppression is gone.

## Deferred (kept disables)

* **\`useMattermostIntegration.ts\`** — destructuring the 11 \`mm\` fields used in the function pushes the ~290-line \`useMattermostIntegration\` over the 300-line \`max-lines-per-function\` ceiling by exactly 1 line. Tried prettier-ignore single-line destructure; still +1. The right fix is to decompose this function (or extract a \`useMmStableFields\` helper) — separate PR. **Keeps 3 F-bucket disables there** + 1 A-bucket disable that requires useEffectEvent (blocked by plugin version, tracked in #1539).

* **OpenClawProvider:62 (bot sentry effect)** — switched deps from \`[bot?.bot_id, bot?.bot_name, bot?.webchat_url]\` to \`[bot]\`. The bot ref churns whenever \`useOpenClawInit\` re-renders, but \`setSentryBotContext\` is idempotent for identical content. Net: more frequent (but harmless) Sentry context sets vs. one suppression removed.

## Test plan
- [x] \`pnpm lint\` passes
- [x] \`npx tsc --noEmit\` passes
- [x] \`pnpm test:unit\` — all 343 spec files / 5444 tests pass
- [ ] CI \`web-quality\` green
- [ ] Manual sanity: agent chat (send/abort), subagent chat panel, mattermost connection / message send, Sentry bot context still populated

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [6] test(web): ratchet vitest coverage thresholds to floor(observed - 1.5%) (Phase 4 done) (#1709)

- **SHA**: `bafe24d54a993ebc6f41af69ddd40351cf2502f7`
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-16T01:48:10Z
- **PR**: #1709

### 完整 Commit Message

```
test(web): ratchet vitest coverage thresholds to floor(observed - 1.5%) (Phase 4 done) (#1709)

## Summary

Phase 4 wrap-up — ratchet vitest coverage thresholds at observed floor.

**Coverage journey (8 PRs over Phase 4)**:
- Start: 76.41% lines (post Phase 3)
- End: 83.94% lines (+7.53pp)
- PRs landed: #1684 (I) / #1687 (J) / #1693 (K) / #1696 (L) / #1699 (M)
/ #1707 (N)

**New thresholds** (per `floor(observed - 1.5%)` ratchet rule):
| Metric | Old | New | Observed |
|--------|-----|-----|----------|
| statements | 77 | **80** | 81.89% |
| branches | 70 | **73** | 74.69% |
| functions | 75 | **79** | 80.60% |
| lines | 79 | **82** | 83.94% |

## Why narrow from 85% goal

Original Phase 4 target was 85% lines. Diminishing returns kicked in
after PR L:
| PR | Delta |
|---|---|
| I | +0.32pp |
| J | +0.29pp |
| K | +0.29pp |
| L | +0.3pp |
| M | +0.23pp |
| N | +0.10pp |

Remaining big uncov are all blocked or low-yield:
- **SubagentChatPanel / MMAttachments / ReplayPlayer** (174 lines
combined): jsdom-incompatible per #1652 — need mock infrastructure or
E2E.
- **useMattermost** (79 uncov / 1033-line existing spec): deep state
machine; extras would be jscpd-dup-heavy.
- **lib/auth/manager** (51 uncov / 835-line existing spec): complex
state machine, marginal coverage per test.

The 82% lines floor leaves ~1.94pp of slack to absorb run-to-run flake —
same buffer profile as Phase 3.

## Test plan
- [x] `pnpm test:unit:coverage` → 5496 pass + 1 todo, thresholds pass
- [x] Verified observed values vs new floors
- [x] Branch off latest `origin/main`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

Phase 4 wrap-up — ratchet vitest coverage thresholds at observed floor.

**Coverage journey (8 PRs over Phase 4)**:
- Start: 76.41% lines (post Phase 3)
- End: 83.94% lines (+7.53pp)
- PRs landed: #1684 (I) / #1687 (J) / #1693 (K) / #1696 (L) / #1699 (M) / #1707 (N)

**New thresholds** (per `floor(observed - 1.5%)` ratchet rule):
| Metric | Old | New | Observed |
|--------|-----|-----|----------|
| statements | 77 | **80** | 81.89% |
| branches | 70 | **73** | 74.69% |
| functions | 75 | **79** | 80.60% |
| lines | 79 | **82** | 83.94% |

## Why narrow from 85% goal

Original Phase 4 target was 85% lines. Diminishing returns kicked in after PR L:
| PR | Delta |
|---|---|
| I | +0.32pp |
| J | +0.29pp |
| K | +0.29pp |
| L | +0.3pp |
| M | +0.23pp |
| N | +0.10pp |

Remaining big uncov are all blocked or low-yield:
- **SubagentChatPanel / MMAttachments / ReplayPlayer** (174 lines combined): jsdom-incompatible per #1652 — need mock infrastructure or E2E.
- **useMattermost** (79 uncov / 1033-line existing spec): deep state machine; extras would be jscpd-dup-heavy.
- **lib/auth/manager** (51 uncov / 835-line existing spec): complex state machine, marginal coverage per test.

The 82% lines floor leaves ~1.94pp of slack to absorb run-to-run flake — same buffer profile as Phase 3.

## Test plan
- [x] `pnpm test:unit:coverage` → 5496 pass + 1 todo, thresholds pass
- [x] Verified observed values vs new floors
- [x] Branch off latest `origin/main`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

