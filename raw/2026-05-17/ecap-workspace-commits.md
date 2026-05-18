# ecap-workspace — 2026-05-17 commits

## [1] 230d261d

- **Author**: felix-srp
- **Date**: 2026-05-17T07:59:22Z
- **PR**: #1714

### Commit Message

```
fix(claw-interface): install-endpoint platform follow-ups #2 + #3 + #4 (#1714)

## Summary

Three platform-side fixes for the `install/async` flow, tracking
[recommendations #2, #3, #4 in the 2026-05-15 install-endpoint platform
follow-ups](https://github.com/SerendipityOneInc/ecap-agent-pack/pull/127).
The PR went through 10 review iterations (manual + CI auto-review + CI
codex-review + user design feedback); the contract is meaningfully
tighter than the design doc requested.

**One conceptual shift worth flagging up-front**: install used to be
implicitly *atomic* (success = everything worked; failure = clean
rollback). After this PR, the contract is **partial commit-forward**:
- Mongo state is always **rolled back** on deploy failure (catalog
reflects what's actually deployable; never lies about installed state).
- Runtime cleanup is **skipped on upgrade failure** so the prior
workspace (or a partial post-rm-rf state recoverable from
`.upgrade-backups/<version>/`) survives. Fresh installs still clean up
since there's no prior state to preserve.
- Post-deploy activation failures **don't trigger any rollback** (deploy
is the commit point; activation is best-effort).
- User-data files overwritten during upgrade are **backed up** to
`.upgrade-backups/<old-version>/` before the overwrite; packager files
are overwritten without backup (recoverable from prior archive).

### #3 — Upgrade-in-place for custom-agent re-install

- Re-installing an already-installed **custom** or **import** agent
replaces the existing `custom_agents` entry instead of raising `409
Conflict` from `_resolve_install_payload`. Matching entry swapped in a
single-pass loop with a `replaced` flag; fallback append covers the
anomalous migration state where the id is in `selected_agent_ids` but
not in `custom_agents`.
- `_resolve_install_payload` returns `is_upgrade` as a 6th tuple element
so `_install_custom_agent_impl` doesn't recompute the membership
predicate (single source of truth).
- The upgrading `agent_id` is removed from `old_ids` when calling
`deploy_selected_agents` so phase-3 sees it as `added` and re-deploys
the archive. The mattermost provisioner is idempotent on `agent_id` —
chat history is preserved.
- **Upgrade preserves user data** via the deploy script's
`preserve_user_data=True` branch + backup-on-overwrite (see below).
User's `data/`, `memory/`, `media/`, `artifacts/shares/` files survive
across upgrades.

### #4 — Post-commit activation failure must not roll back the install

- Hoisted `_ensure_agent_mattermost_ready_and_activate` out of the main
commit/rollback try-block. Once `_deploy_selected_agents` writes the new
bot config to FastClaw DB, the pod's reconciler will (eventually)
materialize the agent regardless of any later step.
- Activation failures are logged via `stage_tracker` + `logger.warning`
and the operation completes successfully. One `except Exception` block
handles both `HTTPException`/`ServiceError` and generic exceptions
(`getattr(e, \"detail\", e)` falls back to the exception when `detail`
is absent).
- The same fix applies to **`hire_agent`** (which goes through
`_install_custom_agent_impl`): a post-deploy MM-bot-entry race no longer
rolls back the hire. `test_hire_rollback_when_mm_not_provisioned` was
encoding the bug — renamed to
`test_hire_treats_post_commit_activation_failure_as_non_fatal`.

### Upgrade-failure recovery semantics

- The deploy script does `rm -rf $WORKSPACE_REAL_DIR` mid-run when
`preserve_user_data=False`. Once that runs, the prior version's runtime
is not reliably recoverable.
- **For `is_custom_upgrade=True` deploy failures**: roll back mongo to
the prior version's metadata (catalog stays consistent with what's
actually deployable); SKIP `_cleanup_custom_agent_runtime` (the prior
workspace, or a partial post-rm-rf state recoverable from
`.upgrade-backups/<version>/`, is the only viable recovery point).
- **For fresh installs (`is_custom_upgrade=False`)**: unchanged — roll
back mongo + cleanup runtime, because there's no prior state to corrupt.
- The backup tree (see below) is what makes the late-fail case
acceptable.

### Backup-on-overwrite for custom-agent upgrades

- When the new archive overwrites a workspace file under `data/`,
`memory/`, `media/`, or `artifacts/shares/` (the user-data convention
paths), the deploy script first copies the existing workspace file to
`$WORKSPACE_REAL_DIR/.upgrade-backups/<old-version>/<rel_path>`. The
user's prior version is always recoverable.
- Files NOT in those paths (code: `agent.py`, `skills/*`,
`artifacts/avatar.png`, etc.) are overwritten without backup — they're
packager-managed and recoverable from the prior archive.
- The backup dir name is the prior version, read from the workspace's
`agent-pack.yaml` (`.upgrade-backups/0.1.2/` reads as \"this is what
0.1.2 looked like\"). Falls back to `unknown-<UTC-ts>` for agents
without an agent-pack.yaml. Version string is sanitized through `tr -cd
'A-Za-z0-9._-'` so a malformed manifest can't escape the backup path.
- `cmp -s "$src_path" "$dst_path"` short-circuits BOTH the backup AND
the copy when source and destination are byte-identical — most files in
a typical upgrade don't change, so this is the dominant savings.

### #2 — Wire `avatar_url` to the pod's artifact host on install

- After `_deploy_selected_agents` unpacks the archive, `avatar.png`
lives at `/workspace/{agent_id}/artifacts/avatar.png` on the pod and is
served by the existing artifact CDN. The platform patches the user's
private catalog row with:
  ```
  https://artifacts.{host}/{bot_id}/{agent_id}/artifacts/avatar.png
  ```
- Host derivation: prefer `APP_FRONTEND_URL` (user-visible host the
browser fetches from); fall back to `APP_PUBLIC_URL` (backend API host)
when frontend isn't configured.
`urlparse(...).hostname.endswith(\"zooclaw.ai\")` — stricter than the
frontend's substring check, by design: a per-install URL written to
mongo can't afford a false positive on hosts like
`myzooclawstaging.example.com`.
- Best-effort: `_write_private_catalog_avatar_url` returns `(ok, err)`
so the caller marks `stage_tracker` accurately (telemetry doesn't lie
when the catalog write fails). Op never fails on this path.
- Skipped for `source=\"official\"`.

### Why bundle #2 + #3 + #4

#3 dissolves the dominant race that fed #4. #2 is the symmetric
write-back complement to #1 (catalog metadata derivation, still
pending). Shipping together makes the agent-studio fix in
[ecap-agent-pack#127](https://github.com/SerendipityOneInc/ecap-agent-pack/pull/127)
testable end-to-end: re-publishes no longer accumulate channels,
transient activate failures no longer phantom-install, the resulting
card shows the avatar, and user state survives upgrades.

## Changes

-
`services/claw-interface/app/services/openclaw/agent_archive_deploy_script.py`
(NEW) — extracted `_build_archive_deploy_script` from `agent_runtime.py`
(which was at the 500-line cap). Adds backup-on-overwrite logic:
`BACKUP_OVERWRITTEN` env var, prior-version detection from
agent-pack.yaml, `UPGRADE_BACKUP_DIR` path, `cmp -s` short-circuit,
user-data path-gated backup case-block.
- `services/claw-interface/app/services/openclaw/agent_runtime.py` —
re-exports `_build_archive_deploy_script` from the new module; gains
`backup_overwritten` kwarg on `deploy_archive_runtime` /
`deploy_agent_archive_source`.
- `services/claw-interface/app/services/openclaw/agent_deploy.py` —
`deploy_selected_agents` gains `archive_preserve_user_data: bool =
False` kwarg, forwarded to `_deploy_workspace_files`.
- `services/claw-interface/app/services/openclaw/agent_deploy_phases.py`
— `_deploy_workspace_files` forwards both `preserve_user_data` and
`backup_overwritten` to `deploy_agent_archive_source` for custom-archive
deploys.
-
`services/claw-interface/app/routes/openclaw_agents/install_support.py`
— `_resolve_install_payload` upgrade branch + `is_upgrade` return.
- `services/claw-interface/app/routes/openclaw_agents/install.py` —
- `_install_custom_agent_impl`: 6-tuple unpack, `is_custom_upgrade`
plumbing, `archive_preserve_user_data=is_custom_upgrade`,
`deploy_old_ids` exclusion.
- Exception handlers: rollback always; cleanup skipped on
`is_custom_upgrade`.
  - Activation hoisted out of rollback scope, single `except Exception`.
- New `_resolve_artifact_avatar_url` (URL host derivation) and
`_write_private_catalog_avatar_url` (best-effort patch_agent wrapper).
- `services/claw-interface/tests/unit/test_openclaw_agents.py` —
  - `mock_mongo` fixture extended to patch `agent_catalog_repo.mongo`.
- 9 new/updated tests covering upgrade path, post-commit activate
non-fatal, avatar URL split-host paths + write failure, upgrade-failure
rollback contract, hire symmetry, stage-timing list, deploy script
content (backup branch + omits-when-flag-off), user-data backup on
upgrade.

## Test plan
- [x] CI \`claw-interface-quality / lint-and-typecheck\` +
\`claw-interface-quality / test\` + \`code-quality\` + \`codex-review\`
+ \`auto-review\` all green.
- [ ] After merge + ecap-agent-pack#127: re-publishing a pack from
agent-studio 1.2.1+ no longer creates duplicate mattermost channels.
- [ ] After merge: intentional activation 500s leave the op in
\`completed\` and the agent visible in the user's catalog.
- [ ] After merge: a freshly installed private pack with
`artifacts/avatar.png` renders the avatar in the catalog UI.
- [ ] After merge: a failed upgrade-in-place attempt leaves mongo at the
prior version metadata + workspace at prior version (or partial new with
backup tree).
- [ ] After merge: a successful upgrade preserves user files in `data/`,
`memory/`, `media/`, `artifacts/shares/` (with backup copies under
`.upgrade-backups/<prior-version>/`).

## Followups (not in this PR)

- **#1** — On `install/async`, derive card metadata from archive
`description.json` and **upsert** by `agentPack_id`. Most of the
user-facing dual-card pain is already addressed by #3 +
ecap-agent-pack#127. Worth picking up if dual-card reports recur
post-merge.
- Mid-deploy (phase-7 channel injection) post-commit failures still
trigger rollback that doesn't reverse the FastClaw DB commit. Reaching
parity with #4 would require either snapshot-restore of the FastClaw bot
config or making phase-7 channel-inject failures non-fatal.
- If a re-installed agent had an avatar previously but the new archive
doesn't, the catalog row keeps the stale URL (404). Acceptable
short-term; tighten with a `test -f` runtime_exec before the patch.
- Single-source-of-truth for the artifact-CDN host: rule encoded in both
`install.py:_resolve_artifact_avatar_url` and
`web/src/app/[locale]/chat/components/workspace-shared.tsx:getArtifactHost`.
A shared `ARTIFACT_HOST` env var would eliminate the drift hazard.
- `.upgrade-backups/<version>/` retention: accrues forever per upgrade.
A cheap retention policy in the shell script (keep last N versions)
would prevent unbounded disk growth.
- Document the partial-commit-forward install-pipeline contract in
`services/claw-interface/CLAUDE.md` so future reviewers reason about
install-pipeline failure modes consistently.

## Commit history
- \`94580b44\` — #3 upgrade-in-place re-install
- \`1ee71533\` — #4 post-commit activation non-fatal
- \`38225616\` — #2 avatar_url write-back (initial)
- \`feb2956f\` — CI fixup (imports, stage list, hire test contract flip)
- \`bcbedb32\` — CI fixup (install_support format + hire test mocks)
- \`b7428260\` — simplify pass (is_custom_upgrade plumbing, collapsed
except, single-pass upgrade loop, urlparse host derivation)
- \`57649baa\` — review iter 1 (stage-tracker telemetry + fallback-host
test)
- \`1899badc\` — review iter 2 (skip cleanup on upgrade failure —
auto-review)
- \`1dc27720\` — review iter 3 (APP_FRONTEND_URL for split-host —
codex-review)
- \`d5d38ce3\` — review iter 4 (commit-forward intent — codex-review)
- \`67ba968e\` — review iter 5 (preserve user data on upgrade —
user-caught)
- \`705973a1\` — review iter 6 (drop artifacts/ from allowlist —
user-caught)
- \`942d8039\` — review iter 7 (backup-on-overwrite — user-directed)
- \`95426c8c\` — review iter 8 (cmp short-circuit + version-keyed backup
dir — user)
- \`8ab556be\` — review iter 9 (roll back mongo on upgrade fail + trim
file — codex-review)
- \`9685491f\` + \`b76bddb1\` — review iter 10 (scope backup to
user-data paths + extract script module + test fix — user)
- \`898f6602\` — final simplify-pass cleanups (comment hygiene)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

Three platform-side fixes for the `install/async` flow, tracking [recommendations #2, #3, #4 in the 2026-05-15 install-endpoint platform follow-ups](https://github.com/SerendipityOneInc/ecap-agent-pack/pull/127). The PR went through 10 review iterations (manual + CI auto-review + CI codex-review + user design feedback); the contract is meaningfully tighter than the design doc requested.

**One conceptual shift worth flagging up-front**: install used to be implicitly *atomic* (success = everything worked; failure = clean rollback). After this PR, the contract is **partial commit-forward**:
- Mongo state is always **rolled back** on deploy failure (catalog reflects what's actually deployable; never lies about installed state).
- Runtime cleanup is **skipped on upgrade failure** so the prior workspace (or a partial post-rm-rf state recoverable from `.upgrade-backups/<version>/`) survives. Fresh installs still clean up since there's no prior state to preserve.
- Post-deploy activation failures **don't trigger any rollback** (deploy is the commit point; activation is best-effort).
- User-data files overwritten during upgrade are **backed up** to `.upgrade-backups/<old-version>/` before the overwrite; packager files are overwritten without backup (recoverable from prior archive).

### #3 — Upgrade-in-place for custom-agent re-install

- Re-installing an already-installed **custom** or **import** agent replaces the existing `custom_agents` entry instead of raising `409 Conflict` from `_resolve_install_payload`. Matching entry swapped in a single-pass loop with a `replaced` flag; fallback append covers the anomalous migration state where the id is in `selected_agent_ids` but not in `custom_agents`.
- `_resolve_install_payload` returns `is_upgrade` as a 6th tuple element so `_install_custom_agent_impl` doesn't recompute the membership predicate (single source of truth).
- The upgrading `agent_id` is removed from `old_ids` when calling `deploy_selected_agents` so phase-3 sees it as `added` and re-deploys the archive. The mattermost provisioner is idempotent on `agent_id` — chat history is preserved.
- **Upgrade preserves user data** via the deploy script's `preserve_user_data=True` branch + backup-on-overwrite (see below). User's `data/`, `memory/`, `media/`, `artifacts/shares/` files survive across upgrades.

### #4 — Post-commit activation failure must not roll back the install

- Hoisted `_ensure_agent_mattermost_ready_and_activate` out of the main commit/rollback try-block. Once `_deploy_selected_agents` writes the new bot config to FastClaw DB, the pod's reconciler will (eventually) materialize the agent regardless of any later step.
- Activation failures are logged via `stage_tracker` + `logger.warning` and the operation completes successfully. One `except Exception` block handles both `HTTPException`/`ServiceError` and generic exceptions (`getattr(e, \"detail\", e)` falls back to the exception when `detail` is absent).
- The same fix applies to **`hire_agent`** (which goes through `_install_custom_agent_impl`): a post-deploy MM-bot-entry race no longer rolls back the hire. `test_hire_rollback_when_mm_not_provisioned` was encoding the bug — renamed to `test_hire_treats_post_commit_activation_failure_as_non_fatal`.

### Upgrade-failure recovery semantics

- The deploy script does `rm -rf $WORKSPACE_REAL_DIR` mid-run when `preserve_user_data=False`. Once that runs, the prior version's runtime is not reliably recoverable.
- **For `is_custom_upgrade=True` deploy failures**: roll back mongo to the prior version's metadata (catalog stays consistent with what's actually deployable); SKIP `_cleanup_custom_agent_runtime` (the prior workspace, or a partial post-rm-rf state recoverable from `.upgrade-backups/<version>/`, is the only viable recovery point).
- **For fresh installs (`is_custom_upgrade=False`)**: unchanged — roll back mongo + cleanup runtime, because there's no prior state to corrupt.
- The backup tree (see below) is what makes the late-fail case acceptable.

### Backup-on-overwrite for custom-agent upgrades

- When the new archive overwrites a workspace file under `data/`, `memory/`, `media/`, or `artifacts/shares/` (the user-data convention paths), the deploy script first copies the existing workspace file to `$WORKSPACE_REAL_DIR/.upgrade-backups/<old-version>/<rel_path>`. The user's prior version is always recoverable.
- Files NOT in those paths (code: `agent.py`, `skills/*`, `artifacts/avatar.png`, etc.) are overwritten without backup — they're packager-managed and recoverable from the prior archive.
- The backup dir name is the prior version, read from the workspace's `agent-pack.yaml` (`.upgrade-backups/0.1.2/` reads as \"this is what 0.1.2 looked like\"). Falls back to `unknown-<UTC-ts>` for agents without an agent-pack.yaml. Version string is sanitized through `tr -cd 'A-Za-z0-9._-'` so a malformed manifest can't escape the backup path.
- `cmp -s "$src_path" "$dst_path"` short-circuits BOTH the backup AND the copy when source and destination are byte-identical — most files in a typical upgrade don't change, so this is the dominant savings.

### #2 — Wire `avatar_url` to the pod's artifact host on install

- After `_deploy_selected_agents` unpacks the archive, `avatar.png` lives at `/workspace/{agent_id}/artifacts/avatar.png` on the pod and is served by the existing artifact CDN. The platform patches the user's private catalog row with:
  ```
  https://artifacts.{host}/{bot_id}/{agent_id}/artifacts/avatar.png
  ```
- Host derivation: prefer `APP_FRONTEND_URL` (user-visible host the browser fetches from); fall back to `APP_PUBLIC_URL` (backend API host) when frontend isn't configured. `urlparse(...).hostname.endswith(\"zooclaw.ai\")` — stricter than the frontend's substring check, by design: a per-install URL written to mongo can't afford a false positive on hosts like `myzooclawstaging.example.com`.
- Best-effort: `_write_private_catalog_avatar_url` returns `(ok, err)` so the caller marks `stage_tracker` accurately (telemetry doesn't lie when the catalog write fails). Op never fails on this path.
- Skipped for `source=\"official\"`.

### Why bundle #2 + #3 + #4

#3 dissolves the dominant race that fed #4. #2 is the symmetric write-back complement to #1 (catalog metadata derivation, still pending). Shipping together makes the agent-studio fix in [ecap-agent-pack#127](https://github.com/SerendipityOneInc/ecap-agent-pack/pull/127) testable end-to-end: re-publishes no longer accumulate channels, transient activate failures no longer phantom-install, the resulting card shows the avatar, and user state survives upgrades.

## Changes

- `services/claw-interface/app/services/openclaw/agent_archive_deploy_script.py` (NEW) — extracted `_build_archive_deploy_script` from `agent_runtime.py` (which was at the 500-line cap). Adds backup-on-overwrite logic: `BACKUP_OVERWRITTEN` env var, prior-version detection from agent-pack.yaml, `UPGRADE_BACKUP_DIR` path, `cmp -s` short-circuit, user-data path-gated backup case-block.
- `services/claw-interface/app/services/openclaw/agent_runtime.py` — re-exports `_build_archive_deploy_script` from the new module; gains `backup_overwritten` kwarg on `deploy_archive_runtime` / `deploy_agent_archive_source`.
- `services/claw-interface/app/services/openclaw/agent_deploy.py` — `deploy_selected_agents` gains `archive_preserve_user_data: bool = False` kwarg, forwarded to `_deploy_workspace_files`.
- `services/claw-interface/app/services/openclaw/agent_deploy_phases.py` — `_deploy_workspace_files` forwards both `preserve_user_data` and `backup_overwritten` to `deploy_agent_archive_source` for custom-archive deploys.
- `services/claw-interface/app/routes/openclaw_agents/install_support.py` — `_resolve_install_payload` upgrade branch + `is_upgrade` return.
- `services/claw-interface/app/routes/openclaw_agents/install.py` —
  - `_install_custom_agent_impl`: 6-tuple unpack, `is_custom_upgrade` plumbing, `archive_preserve_user_data=is_custom_upgrade`, `deploy_old_ids` exclusion.
  - Exception handlers: rollback always; cleanup skipped on `is_custom_upgrade`.
  - Activation hoisted out of rollback scope, single `except Exception`.
  - New `_resolve_artifact_avatar_url` (URL host derivation) and `_write_private_catalog_avatar_url` (best-effort patch_agent wrapper).
- `services/claw-interface/tests/unit/test_openclaw_agents.py` —
  - `mock_mongo` fixture extended to patch `agent_catalog_repo.mongo`.
  - 9 new/updated tests covering upgrade path, post-commit activate non-fatal, avatar URL split-host paths + write failure, upgrade-failure rollback contract, hire symmetry, stage-timing list, deploy script content (backup branch + omits-when-flag-off), user-data backup on upgrade.

## Test plan
- [x] CI \`claw-interface-quality / lint-and-typecheck\` + \`claw-interface-quality / test\` + \`code-quality\` + \`codex-review\` + \`auto-review\` all green.
- [ ] After merge + ecap-agent-pack#127: re-publishing a pack from agent-studio 1.2.1+ no longer creates duplicate mattermost channels.
- [ ] After merge: intentional activation 500s leave the op in \`completed\` and the agent visible in the user's catalog.
- [ ] After merge: a freshly installed private pack with `artifacts/avatar.png` renders the avatar in the catalog UI.
- [ ] After merge: a failed upgrade-in-place attempt leaves mongo at the prior version metadata + workspace at prior version (or partial new with backup tree).
- [ ] After merge: a successful upgrade preserves user files in `data/`, `memory/`, `media/`, `artifacts/shares/` (with backup copies under `.upgrade-backups/<prior-version>/`).

## Followups (not in this PR)

- **#1** — On `install/async`, derive card metadata from archive `description.json` and **upsert** by `agentPack_id`. Most of the user-facing dual-card pain is already addressed by #3 + ecap-agent-pack#127. Worth picking up if dual-card reports recur post-merge.
- Mid-deploy (phase-7 channel injection) post-commit failures still trigger rollback that doesn't reverse the FastClaw DB commit. Reaching parity with #4 would require either snapshot-restore of the FastClaw bot config or making phase-7 channel-inject failures non-fatal.
- If a re-installed agent had an avatar previously but the new archive doesn't, the catalog row keeps the stale URL (404). Acceptable short-term; tighten with a `test -f` runtime_exec before the patch.
- Single-source-of-truth for the artifact-CDN host: rule encoded in both `install.py:_resolve_artifact_avatar_url` and `web/src/app/[locale]/chat/components/workspace-shared.tsx:getArtifactHost`. A shared `ARTIFACT_HOST` env var would eliminate the drift hazard.
- `.upgrade-backups/<version>/` retention: accrues forever per upgrade. A cheap retention policy in the shell script (keep last N versions) would prevent unbounded disk growth.
- Document the partial-commit-forward install-pipeline contract in `services/claw-interface/CLAUDE.md` so future reviewers reason about install-pipeline failure modes consistently.

## Commit history
- \`94580b44\` — #3 upgrade-in-place re-install
- \`1ee71533\` — #4 post-commit activation non-fatal
- \`38225616\` — #2 avatar_url write-back (initial)
- \`feb2956f\` — CI fixup (imports, stage list, hire test contract flip)
- \`bcbedb32\` — CI fixup (install_support format + hire test mocks)
- \`b7428260\` — simplify pass (is_custom_upgrade plumbing, collapsed except, single-pass upgrade loop, urlparse host derivation)
- \`57649baa\` — review iter 1 (stage-tracker telemetry + fallback-host test)
- \`1899badc\` — review iter 2 (skip cleanup on upgrade failure — auto-review)
- \`1dc27720\` — review iter 3 (APP_FRONTEND_URL for split-host — codex-review)
- \`d5d38ce3\` — review iter 4 (commit-forward intent — codex-review)
- \`67ba968e\` — review iter 5 (preserve user data on upgrade — user-caught)
- \`705973a1\` — review iter 6 (drop artifacts/ from allowlist — user-caught)
- \`942d8039\` — review iter 7 (backup-on-overwrite — user-directed)
- \`95426c8c\` — review iter 8 (cmp short-circuit + version-keyed backup dir — user)
- \`8ab556be\` — review iter 9 (roll back mongo on upgrade fail + trim file — codex-review)
- \`9685491f\` + \`b76bddb1\` — review iter 10 (scope backup to user-data paths + extract script module + test fix — user)
- \`898f6602\` — final simplify-pass cleanups (comment hygiene)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

