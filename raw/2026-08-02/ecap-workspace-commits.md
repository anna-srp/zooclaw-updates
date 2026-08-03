# SerendipityOneInc/ecap-workspace commits — 2026-08-02

共 3 个 commit


---

## fix(packs): heal a lost Engine projection on identical-SHA replay (#3188)

- **SHA**: `abc93c01fd7925f4ebbe683db5cfa6ce121efbde`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-02T18:07:04Z
- **PR**: #3188

### 完整 Commit Message

```
fix(packs): heal a lost Engine projection on identical-SHA replay (#3188)

## Problem

The Engine projection scheduled by `POST /agent-packs/runtime-assets` is
best-effort and process-local (#3187). An exhausted 1/5/15s retry budget
or a Workspace restart mid-build loses it; every V2 install then fails
closed on `pack_environment_not_ready`, and nothing drives recovery. The
operator's natural response — re-running the release workflow — was
exactly the path the identical-SHA idempotency short-circuit blocked: it
returned `unchanged` without touching the projection, so the only way
out was the admin rebuild endpoint.

## Fix

- An identical-SHA replay re-checks the recorded Environment provenance
(`environment_source_sha256` + `engine_environment_version`). When the
per-Pack gate is enabled and the provenance is missing or stale, it logs
an **error** and re-schedules the (idempotent) projection before
returning `unchanged`. Replays with complete provenance keep the exact
previous behavior — no copy, no projection.
- The shared projection guard's exhausted-retries log is raised from
warning to error: that state strands the Pack until a replay or an admin
rebuild.

Re-running the release workflow now heals a stuck Pack. Durable
autonomous recovery (persistent marker + lease + minute-level
reconciliation, reference implementation on
`feature/durable-engine-projection-recovery`) remains tracked as
SerendipityOneInc/zooclaw-engine#604.

## Validation

- 71 targeted unit tests pass, including 4 new healing cases: missing
provenance re-schedules, stale provenance re-schedules, disabled gate
does not, and the error log is emitted.
- `ruff check`, `ruff format --check`, pyright, and the file-length lint
pass locally.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01JksoXqdHArutJFifUtrKS6
```

### PR Body

```
## Problem

The Engine projection scheduled by `POST /agent-packs/runtime-assets` is best-effort and process-local (#3187). An exhausted 1/5/15s retry budget or a Workspace restart mid-build loses it; every V2 install then fails closed on `pack_environment_not_ready`, and nothing drives recovery. The operator's natural response — re-running the release workflow — was exactly the path the identical-SHA idempotency short-circuit blocked: it returned `unchanged` without touching the projection, so the only way out was the admin rebuild endpoint.

## Fix

- An identical-SHA replay re-checks the recorded Environment provenance (`environment_source_sha256` + `engine_environment_version`). When the per-Pack gate is enabled and the provenance is missing or stale, it logs an **error** and re-schedules the (idempotent) projection before returning `unchanged`. Replays with complete provenance keep the exact previous behavior — no copy, no projection.
- The shared projection guard's exhausted-retries log is raised from warning to error: that state strands the Pack until a replay or an admin rebuild.

Re-running the release workflow now heals a stuck Pack. Durable autonomous recovery (persistent marker + lease + minute-level reconciliation, reference implementation on `feature/durable-engine-projection-recovery`) remains tracked as SerendipityOneInc/zooclaw-engine#604.

## Validation

- 71 targeted unit tests pass, including 4 new healing cases: missing provenance re-schedules, stale provenance re-schedules, disabled gate does not, and the error log is emitted.
- `ruff check`, `ruff format --check`, pyright, and the file-length lint pass locally.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01JksoXqdHArutJFifUtrKS6

```


---

## feat(packs): register CI-published Engine runtime assets (#3187)

- **SHA**: `8b9b97cb8862e00f247139ac64906c80d6326926`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-02T16:13:29Z
- **PR**: #3187

### 完整 Commit Message

```
feat(packs): register CI-published Engine runtime assets (#3187)

## What changed

- Adds `POST /agent-packs/runtime-assets`, authenticated by the new
`AGENT_PACK_RUNTIME_ASSET_TOKEN` header setting (same trust pattern as
`AGENT_STUDIO_PACK_UPDATE_TOKEN`). The ecap-agent-pack release workflow
calls it once per published Engine archive.
- Registration attaches `runtime_assets.engine = {asset_id,
archive_name, sha256}` to the submission the Engine resolver already
reads (`pack.latest_submission_id`), behind a `status=approved` write
fence. It creates no submission and synchronizes nothing to the Pack —
`Pack.asset_id`, `pack_version`, listing metadata, and
`latest_submission_id` all stay under V1 ownership.
- The upload worker's `{org}/{display_id}/…` key is normalized into the
Pack-owned `{org}/{pack_id}/{uuid}` shape with the existing
`copy_submission_asset_to_pack` helper, satisfying
`_is_pack_scoped_asset_key` without widening it.
- An identical-SHA replay returns `unchanged` without copying or
re-projecting, so CI re-runs are safe. A same-version SHA swap
re-registers and re-projects (the V2 bug-fix path).
- When `ENGINE_PACK_RUNTIME_ASSETS_ENABLED` covers the Pack,
registration schedules the existing Engine projection
(`run_post_approval`'s engine half, extracted into
`run_engine_projection` so both callers share one retry/error policy). A
projection failure logs and does not fail the request;
`environment/rebuild` remains the recovery path, and installs fail
closed on `pack_environment_not_ready` until the projection lands.

## What deliberately does not change

The Engine resolver, the approval flow, the `PackRuntimeAsset` schema,
and every V1 install path. Design and trade-offs (including the
agent-studio V1-approval displacement caveat) in
`docs/superpowers/specs/2026-08-02-engine-runtime-asset-publishing-design.md`.

## Operator configuration

`AGENT_PACK_RUNTIME_ASSET_TOKEN` must be set in the deployment env and
mirrored as a secret in ecap-agent-pack (companion PR:
SerendipityOneInc/ecap-agent-pack#218, stacked on #214).

## Validation

- 158 targeted unit tests pass: new registration-service suite (10 cases
incl. idempotent replay, SHA swap, lost-write race, gate-off,
V1-isolation regression), submission-repo fence test, refactored
environment-service suite, adjacent pack-store route/review suites.
- `ruff check`, `ruff format --check`, and pyright (venv interpreter)
clean on all changed files.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01JksoXqdHArutJFifUtrKS6
```

### PR Body

```
## What changed

- Adds `POST /agent-packs/runtime-assets`, authenticated by the new `AGENT_PACK_RUNTIME_ASSET_TOKEN` header setting (same trust pattern as `AGENT_STUDIO_PACK_UPDATE_TOKEN`). The ecap-agent-pack release workflow calls it once per published Engine archive.
- Registration attaches `runtime_assets.engine = {asset_id, archive_name, sha256}` to the submission the Engine resolver already reads (`pack.latest_submission_id`), behind a `status=approved` write fence. It creates no submission and synchronizes nothing to the Pack — `Pack.asset_id`, `pack_version`, listing metadata, and `latest_submission_id` all stay under V1 ownership.
- The upload worker's `{org}/{display_id}/…` key is normalized into the Pack-owned `{org}/{pack_id}/{uuid}` shape with the existing `copy_submission_asset_to_pack` helper, satisfying `_is_pack_scoped_asset_key` without widening it.
- An identical-SHA replay returns `unchanged` without copying or re-projecting, so CI re-runs are safe. A same-version SHA swap re-registers and re-projects (the V2 bug-fix path).
- When `ENGINE_PACK_RUNTIME_ASSETS_ENABLED` covers the Pack, registration schedules the existing Engine projection (`run_post_approval`'s engine half, extracted into `run_engine_projection` so both callers share one retry/error policy). A projection failure logs and does not fail the request; `environment/rebuild` remains the recovery path, and installs fail closed on `pack_environment_not_ready` until the projection lands.

## What deliberately does not change

The Engine resolver, the approval flow, the `PackRuntimeAsset` schema, and every V1 install path. Design and trade-offs (including the agent-studio V1-approval displacement caveat) in `docs/superpowers/specs/2026-08-02-engine-runtime-asset-publishing-design.md`.

## Operator configuration

`AGENT_PACK_RUNTIME_ASSET_TOKEN` must be set in the deployment env and mirrored as a secret in ecap-agent-pack (companion PR: SerendipityOneInc/ecap-agent-pack#218, stacked on #214).

## Validation

- 158 targeted unit tests pass: new registration-service suite (10 cases incl. idempotent replay, SHA swap, lost-write race, gate-off, V1-isolation regression), submission-repo fence test, refactored environment-service suite, adjacent pack-store route/review suites.
- `ruff check`, `ruff format --check`, and pyright (venv interpreter) clean on all changed files.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01JksoXqdHArutJFifUtrKS6
```


---

## feat(pack): resolve Engine archives by runtime asset (#3184)

- **SHA**: `38339e6b11e50750dbe28dbf8e518e50af1e5c42`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-02T09:26:43Z
- **PR**: #3184

### 完整 Commit Message

```
feat(pack): resolve Engine archives by runtime asset (#3184)

## Summary

- Add a default-off, per-Pack Engine runtime-assets gate. A selected
Pack resolves only its immutable `runtime_assets.engine` archive; it
never falls back to the V1 `asset_id`.
- Read the selected Engine archive directly from the dedicated Pack R2
bucket, validate its Pack-owned key and SHA-256, and carry that source
digest through persona/skill snapshots, Environment versions, and Agent
provenance.
- Reuse the resolver across Engine install, install retry, update,
post-approval Environment projection, and rebuild. Source transitions
preflight the old skill snapshot and require an exact target Environment
version.
- Retry a transient post-approval Engine projection in-process with a
bounded 1 / 5 / 15-second budget; the existing admin rebuild remains the
recovery path after exhaustion or process restart.
- Preserve V1/OpenClaw behavior behind the default-off gate, including
V1 Environment pinning on install retry. A known V2-only Environment
state fails closed instead of resolving mutable `latest`.
- Add the implementation and staged rollout plan in
`docs/superpowers/specs/2026-08-02-pack-runtime-asset-resolver.md`.

## Scope boundary

This intentionally does **not** add a GitHub Release importer, asset
download/copy pipeline, release journal/replay worker, generic Pack
Store lease/CAS/recovery platform, Markdown rewriting, or a public
R2/r2-access dependency. The release/binding side writes the immutable
V2 reference; Workspace only consumes it.

## PR size

The code/test diff is 3,965 lines (the design spec is excluded from that
calculation), so this draft carries `size-override`. The excess is
source-transition, V1 compatibility, direct-R2 integrity, and
Environment safety coverage—not an additional release/import platform.

## Test plan

- [x] Targeted runtime-assets suite: 362 passed.
- [x] `bash scripts/verify-py.sh` (ruff, formatting, pyright,
import-linter).
- [x] Repository pre-commit suite, including ≤500-line and C901
complexity checks.
- [x] Pre-push changed-surface verification.
```

### PR Body

```
## Summary

- Add a default-off, per-Pack Engine runtime-assets gate. A selected Pack resolves only its immutable `runtime_assets.engine` archive; it never falls back to the V1 `asset_id`.
- Read the selected Engine archive directly from the dedicated Pack R2 bucket, validate its Pack-owned key and SHA-256, and carry that source digest through persona/skill snapshots, Environment versions, and Agent provenance.
- Reuse the resolver across Engine install, install retry, update, post-approval Environment projection, and rebuild. Source transitions preflight the old skill snapshot and require an exact target Environment version.
- Retry a transient post-approval Engine projection in-process with a bounded 1 / 5 / 15-second budget; the existing admin rebuild remains the recovery path after exhaustion or process restart.
- Preserve V1/OpenClaw behavior behind the default-off gate, including V1 Environment pinning on install retry. A known V2-only Environment state fails closed instead of resolving mutable `latest`.
- Add the implementation and staged rollout plan in `docs/superpowers/specs/2026-08-02-pack-runtime-asset-resolver.md`.

## Scope boundary

This intentionally does **not** add a GitHub Release importer, asset download/copy pipeline, release journal/replay worker, generic Pack Store lease/CAS/recovery platform, Markdown rewriting, or a public R2/r2-access dependency. The release/binding side writes the immutable V2 reference; Workspace only consumes it.

## PR size

The code/test diff is 3,965 lines (the design spec is excluded from that calculation), so this draft carries `size-override`. The excess is source-transition, V1 compatibility, direct-R2 integrity, and Environment safety coverage—not an additional release/import platform.

## Test plan

- [x] Targeted runtime-assets suite: 362 passed.
- [x] `bash scripts/verify-py.sh` (ruff, formatting, pyright, import-linter).
- [x] Repository pre-commit suite, including ≤500-line and C901 complexity checks.
- [x] Pre-push changed-surface verification.

```
