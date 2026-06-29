# ecap-workspace — commits 2026-06-28

共 5 个 commits

---

## fix(claw-interface): dedupe WeChat QR accounts (#2634)

- **SHA**: `c0080406ea352c13f4fd4a37c50cea926c801007`
- **作者**: sharplee-srp
- **日期**: 2026-06-28T11:09:59Z
- **PR**: #2634

### 完整 Commit Message

```
fix(claw-interface): dedupe WeChat QR accounts (#2634)

## Summary

- Reuse an existing WeChat account when QR confirmation returns a
`userId` already present in the bot's WeChat account files.
- Move the reused account's binding to the requested agent instead of
creating another account alias for the same real WeChat identity.
- Clean up stale duplicate WeChat account aliases from the account
index, credential files, channel config, and agent bindings.

## Testing

- `cd services/claw-interface && .venv/bin/pytest
tests/unit/test_openclaw_settings_routes.py::TestWeixinPollEndpoint -q`
- `cd services/claw-interface && .venv/bin/pytest
tests/unit/test_openclaw_settings_routes.py -q`
- `bash scripts/verify-py.sh --ruff-only`
- `cd services/claw-interface && .venv/bin/pyright --pythonpath
.venv/bin/python app/routes/openclaw_settings/weixin.py
app/routes/openclaw_settings/weixin_helpers.py
app/routes/openclaw_settings/helpers.py
tests/unit/test_openclaw_settings_routes.py`

Note: `bash scripts/verify-py.sh` was also attempted. Ruff and
import-linter passed, but the script-level pyright invocation did not
pick up the local venv and reported broad missing imports such as
`fastapi`, `pytest`, and `favie_common`. The changed files pass pyright
when run with the explicit venv python path above.
```

### PR Body

## Summary

- Reuse an existing WeChat account when QR confirmation returns a `userId` already present in the bot's WeChat account files.
- Move the reused account's binding to the requested agent instead of creating another account alias for the same real WeChat identity.
- Clean up stale duplicate WeChat account aliases from the account index, credential files, channel config, and agent bindings.

## Testing

- `cd services/claw-interface && .venv/bin/pytest tests/unit/test_openclaw_settings_routes.py::TestWeixinPollEndpoint -q`
- `cd services/claw-interface && .venv/bin/pytest tests/unit/test_openclaw_settings_routes.py -q`
- `bash scripts/verify-py.sh --ruff-only`
- `cd services/claw-interface && .venv/bin/pyright --pythonpath .venv/bin/python app/routes/openclaw_settings/weixin.py app/routes/openclaw_settings/weixin_helpers.py app/routes/openclaw_settings/helpers.py tests/unit/test_openclaw_settings_routes.py`

Note: `bash scripts/verify-py.sh` was also attempted. Ruff and import-linter passed, but the script-level pyright invocation did not pick up the local venv and reported broad missing imports such as `fastapi`, `pytest`, and `favie_common`. The changed files pass pyright when run with the explicit venv python path above.


---

## fix(openclaw-settings): bind WeChat agents before activation (#2613)

- **SHA**: `66377dc070912c6933b40d1f19cc44756701e6b0`
- **作者**: sharplee-srp
- **日期**: 2026-06-28T05:55:01Z
- **PR**: #2613

### 完整 Commit Message

```
fix(openclaw-settings): bind WeChat agents before activation (#2613)

## Summary

- Write or clear the WeChat channel agent binding before calling
FastClaw channel activation.
- Make explicit WeChat custom-agent binding failures fail setup instead
of returning success with a warning.
- Restore the previous WeChat binding during setup compensation when a
later activation or reload step fails.
- Add focused WeChat regression tests for custom-agent ordering,
main-agent binding cleanup, binding failure, and
restore-after-activation failure.

Scope is intentionally limited to the WeChat plugin. Mattermost and MS
Teams rollout cleanup are left out per follow-up direction.

Stacked on #2611.

## Tests

- PATH="$PWD/services/claw-interface/.venv/bin:$PATH"
PYTHONPATH="$PWD/services/claw-interface/.venv/lib/python3.12/site-packages"
bash scripts/verify-py.sh
- services/claw-interface/.venv/bin/pytest
tests/unit/test_openclaw_settings_routes.py -k 'WeixinPollEndpoint or
WeixinSetupScenarios or weixin_trigger_index_reload' -q
```

### PR Body

## Summary

- Write or clear the WeChat channel agent binding before calling FastClaw channel activation.
- Make explicit WeChat custom-agent binding failures fail setup instead of returning success with a warning.
- Restore the previous WeChat binding during setup compensation when a later activation or reload step fails.
- Add focused WeChat regression tests for custom-agent ordering, main-agent binding cleanup, binding failure, and restore-after-activation failure.

Scope is intentionally limited to the WeChat plugin. Mattermost and MS Teams rollout cleanup are left out per follow-up direction.

Stacked on #2611.

## Tests

- PATH="$PWD/services/claw-interface/.venv/bin:$PATH" PYTHONPATH="$PWD/services/claw-interface/.venv/lib/python3.12/site-packages" bash scripts/verify-py.sh
- services/claw-interface/.venv/bin/pytest tests/unit/test_openclaw_settings_routes.py -k 'WeixinPollEndpoint or WeixinSetupScenarios or weixin_trigger_index_reload' -q


---

## fix(openclaw-settings): reload WeChat channel without rollout (#2610)

- **SHA**: `782f729740f4593ca7c449e49485e8987e8102a1`
- **作者**: sharplee-srp
- **日期**: 2026-06-28T05:26:11Z
- **PR**: #2610

### 完整 Commit Message

```
fix(openclaw-settings): reload WeChat channel without rollout (#2610)

## What

`trigger_index_reload` (WeChat channel setup/remove) no longer rolls out
the bot's Kubernetes Deployment. It now patches the running pod's
`/home/node/.openclaw/openclaw.json` directly via `runtime_exec`, so
OpenClaw's config watcher hot-reloads `openclaw-weixin` in place.

This is **PR 1** of a planned 3-PR rollout-remediation series.

## Why

The old path bumped top-level
`channels.openclaw-weixin.channelConfigUpdatedAt` via
`update_bot_config`. FastClaw treats a `channels` write as
`needsRollout`, so every WeChat setup/remove restarted the bot pod (new
ReplicaSet, dropped sessions). The credential/index writes and the
FastClaw channel API already sync to the running pod without a rollout —
only this reload marker forced one.

## Change

- `weixin_helpers.py::trigger_index_reload`: replace
`update_bot_config({"channels": {...}})` with a `runtime_exec(["node",
"-e", <script>])` that atomically (temp-file + rename) sets
`channels.openclaw-weixin.enabled` + `channelConfigUpdatedAt`,
preserving unknown fields.
- Unit tests asserting the no-rollout call path (`runtime_exec` used,
`update_bot_config` not awaited, the Node script targets `openclaw.json`
at `channels.openclaw-weixin.*`).

## Non-goals (separate follow-up PRs)

- Cross-process mutation lock / compensation for concurrent reloads (PR
2).
- Custom-agent binding order and remaining non-WeChat rollout paths (PR
3).
- No change to FastClaw's generic `channels`/`plugins` rollout guard.

## Validation

Local (claw-interface):
- `ruff check` + `ruff format --check` clean; `pyright` 0 errors on
changed files; `import-linter` 8/8 contracts kept.
- `pytest -k weixin` → 32 passed.

End-to-end against the staging bot (modified backend in the request
path, real WeChat scan):
- **Add** (real QR scan + authorize) → OpenClaw logs `config hot reload
applied (channels.openclaw-weixin.*)`, `openclaw.json` patched in place;
Deployment `generation` unchanged, same pod, `restartCount=0`.
- **Bidirectional message round-trip** through the channel (inbound →
`agent:main` → `text sent OK`).
- **Custom-agent bind** (`soulmate`) → binding written, routing
confirmed (`agent:soulmate:openclaw-weixin:…`), no rollout.
- **Pod restart persistence** → channel record (ConfigMap) + credentials
(JuiceFS PVC) survive, session resumes without re-scan.
- **Remove** → channel-API delete + `runtime_exec` cleanup, no
`update_bot_config`, no rollout.

The only rollout observed during testing came from an unrelated
concurrent actor on the shared staging bot using the old `PUT /bots`
path — i.e. exactly the behavior this PR removes.
```

### PR Body

## What

`trigger_index_reload` (WeChat channel setup/remove) no longer rolls out the bot's Kubernetes Deployment. It now patches the running pod's `/home/node/.openclaw/openclaw.json` directly via `runtime_exec`, so OpenClaw's config watcher hot-reloads `openclaw-weixin` in place.

This is **PR 1** of a planned 3-PR rollout-remediation series.

## Why

The old path bumped top-level `channels.openclaw-weixin.channelConfigUpdatedAt` via `update_bot_config`. FastClaw treats a `channels` write as `needsRollout`, so every WeChat setup/remove restarted the bot pod (new ReplicaSet, dropped sessions). The credential/index writes and the FastClaw channel API already sync to the running pod without a rollout — only this reload marker forced one.

## Change

- `weixin_helpers.py::trigger_index_reload`: replace `update_bot_config({"channels": {...}})` with a `runtime_exec(["node", "-e", <script>])` that atomically (temp-file + rename) sets `channels.openclaw-weixin.enabled` + `channelConfigUpdatedAt`, preserving unknown fields.
- Unit tests asserting the no-rollout call path (`runtime_exec` used, `update_bot_config` not awaited, the Node script targets `openclaw.json` at `channels.openclaw-weixin.*`).

## Non-goals (separate follow-up PRs)

- Cross-process mutation lock / compensation for concurrent reloads (PR 2).
- Custom-agent binding order and remaining non-WeChat rollout paths (PR 3).
- No change to FastClaw's generic `channels`/`plugins` rollout guard.

## Validation

Local (claw-interface):
- `ruff check` + `ruff format --check` clean; `pyright` 0 errors on changed files; `import-linter` 8/8 contracts kept.
- `pytest -k weixin` → 32 passed.

End-to-end against the staging bot (modified backend in the request path, real WeChat scan):
- **Add** (real QR scan + authorize) → OpenClaw logs `config hot reload applied (channels.openclaw-weixin.*)`, `openclaw.json` patched in place; Deployment `generation` unchanged, same pod, `restartCount=0`.
- **Bidirectional message round-trip** through the channel (inbound → `agent:main` → `text sent OK`).
- **Custom-agent bind** (`soulmate`) → binding written, routing confirmed (`agent:soulmate:openclaw-weixin:…`), no rollout.
- **Pod restart persistence** → channel record (ConfigMap) + credentials (JuiceFS PVC) survive, session resumes without re-scan.
- **Remove** → channel-API delete + `runtime_exec` cleanup, no `update_bot_config`, no rollout.

The only rollout observed during testing came from an unrelated concurrent actor on the shared staging bot using the old `PUT /bots` path — i.e. exactly the behavior this PR removes.


---

## fix(devcontainer): drop host GITHUB_TOKEN from .env when GitHub rejects it (#2633)

- **SHA**: `68877e33df9de975a4abcf5807cdf373608ce3f5`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-28T02:39:24Z
- **PR**: #2633

### 完整 Commit Message

```
fix(devcontainer): drop host GITHUB_TOKEN from .env when GitHub rejects it (#2633)

## Problem

`.devcontainer/initializeCommand.sh` resolves a GitHub token on the
**host** (host `$GITHUB_TOKEN` env → `gh auth token`) and writes it into
the gitignored `.devcontainer/.env`, which docker-compose injects into
the container as `$GITHUB_TOKEN`.

If the host's gh login has **expired**, that invalid token still gets
baked in. Inside the container `$GITHUB_TOKEN` takes precedence over
`~/.config/gh/hosts.yml`, so it **shadows the container's own valid,
volume-persisted gh login** — and `postCreate` also bakes it into `git
config url.insteadOf`. Result: `gh auth status` fails and
git/private-package installs break.

This was hit live during a devcontainer rebuild: `uv pip install` of the
private `favie-common` package failed with `could not read Password ...
terminal prompts disabled`, even though the container had a perfectly
valid persisted gh login.

## Fix

After resolving the token, validate it against `api.github.com/user` and
**drop it only on a definitive HTTP 401**, so the container falls back
to its own gh login.

Deliberately conservative — the token is kept on any non-401 result:
- `200` → valid, keep
- timeout / offline / no `curl` (`000`) → can't verify, **keep** (never
punish on inability to check)
- `401` → positively rejected, drop (+ a `⚠️` log line)

## Test

`bash -n` clean. Logic verified by extracting the actual block from the
file and exercising it:
- real garbage token → real API `401` → **dropped** ✓
- mocked `200` → **kept** ✓
- mocked `000` (offline/timeout) → **kept** ✓
- empty token → no-op ✓

No repo secret involved — `.devcontainer/.env` is gitignored and
regenerated each launch.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## Problem

`.devcontainer/initializeCommand.sh` resolves a GitHub token on the **host** (host `$GITHUB_TOKEN` env → `gh auth token`) and writes it into the gitignored `.devcontainer/.env`, which docker-compose injects into the container as `$GITHUB_TOKEN`.

If the host's gh login has **expired**, that invalid token still gets baked in. Inside the container `$GITHUB_TOKEN` takes precedence over `~/.config/gh/hosts.yml`, so it **shadows the container's own valid, volume-persisted gh login** — and `postCreate` also bakes it into `git config url.insteadOf`. Result: `gh auth status` fails and git/private-package installs break.

This was hit live during a devcontainer rebuild: `uv pip install` of the private `favie-common` package failed with `could not read Password ... terminal prompts disabled`, even though the container had a perfectly valid persisted gh login.

## Fix

After resolving the token, validate it against `api.github.com/user` and **drop it only on a definitive HTTP 401**, so the container falls back to its own gh login.

Deliberately conservative — the token is kept on any non-401 result:
- `200` → valid, keep
- timeout / offline / no `curl` (`000`) → can't verify, **keep** (never punish on inability to check)
- `401` → positively rejected, drop (+ a `⚠️` log line)

## Test

`bash -n` clean. Logic verified by extracting the actual block from the file and exercising it:
- real garbage token → real API `401` → **dropped** ✓
- mocked `200` → **kept** ✓
- mocked `000` (offline/timeout) → **kept** ✓
- empty token → no-op ✓

No repo secret involved — `.devcontainer/.env` is gitignored and regenerated each launch.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(devcontainer): state backup/restore tooling + persist ~/.codex volume (#2632)

- **SHA**: `92adf9ccdb504f665ab53723a7b662f4d2082374`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-28T01:38:39Z
- **PR**: #2632

### 完整 Commit Message

```
feat(devcontainer): state backup/restore tooling + persist ~/.codex volume (#2632)

## What & why

Adds a backup/restore workflow for **Claude Code + Codex CLI state**
across a devcontainer **Rebuild Container**, and closes the root-cause
gap behind it.

In the ecap-workspace devcontainer, `~/.claude` is on a persistent named
volume but **`~/.codex` was on the ephemeral container layer** — so
every rebuild wiped Codex sessions, auth, and memory. That's why the
running container has gone un-rebuilt for weeks despite committed config
fixes.

## Changes

**1. Persist `~/.codex` (the fix)** — `.devcontainer/`
- `docker-compose.yml`: new `codex-config` named volume mounted at
`/home/node/.codex` (+ top-level declaration).
- `Dockerfile`: pre-create the node-owned `~/.codex` mountpoint
alongside `~/.claude` / `~/.config`.
- `postCreateCommand.sh`: `chown`/`chmod` `~/.codex` like the other
volumes (it holds `auth.json`, so keep it node-owned and not
group/world-readable).

**2. Backup/restore tooling** — `scripts/dev-state-backup.sh`
- `detect` / `backup` / `restore` / `verify` over `ssh` + `docker exec`
(same transport as the `dev` CLI; connection from the `dev-remote`
profile, or `DEV_SSH_HOST` / `DEV_CONTAINER_PATTERN` env).
- Curated by default (excludes `*.sqlite` runtime DBs — Codex
`logs_*.sqlite` is multi-GB — plus caches/snapshots); `--full` keeps
everything.
- A **quiesce gate** refuses to snapshot while a `claude`/`codex` agent
is mid-write (`--allow-live` to override), and manifest-based
verification runs on both ends (archive integrity, key/secret files,
session counts, find-vs-tar selection diff, post-restore presence +
smoke test).
- Secrets-aware: backup dir is `chmod 700` and the script refuses to
write inside a git repo.

**3. Docs + skill**
- `docs/devcontainer-state-backup.md` — colleague-facing runbook,
including why "absolute paths" matter (Claude path-encodes the workspace
into dir names + transcript `cwd`) and an appendix for restoring into a
*different* path. Same-path round-trip needs no rewriting.
- `.agents/skills/devcontainer-state-backup/` (+ `.claude/skills`
symlink) — agent-facing runbook.

## Why this PR unblocks the rebuild

The rebuild only persists `~/.codex` going forward if `codex-config` is
in the remote checkout's compose file first. Merge this, `git pull` on
the remote, then rebuild + restore.

## Verification

- Script: `bash -n` + shellcheck clean; selection logic unit-tested
against a mock home (curated excludes drop `*.sqlite`/caches; keeps
sessions/memory/auth; `--full` keeps all).
- A real verified backup of the current container is already in hand:
**344 Claude + 14 Codex** transcripts, all key/secret files present,
archive integrity OK, find-vs-tar diff empty.
- `scripts/sync-agent-skills.sh --check` passes; pre-push size +
changed-surface checks pass.

No Linear issue — devcontainer/infra tooling.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What & why

Adds a backup/restore workflow for **Claude Code + Codex CLI state** across a devcontainer **Rebuild Container**, and closes the root-cause gap behind it.

In the ecap-workspace devcontainer, `~/.claude` is on a persistent named volume but **`~/.codex` was on the ephemeral container layer** — so every rebuild wiped Codex sessions, auth, and memory. That's why the running container has gone un-rebuilt for weeks despite committed config fixes.

## Changes

**1. Persist `~/.codex` (the fix)** — `.devcontainer/`
- `docker-compose.yml`: new `codex-config` named volume mounted at `/home/node/.codex` (+ top-level declaration).
- `Dockerfile`: pre-create the node-owned `~/.codex` mountpoint alongside `~/.claude` / `~/.config`.
- `postCreateCommand.sh`: `chown`/`chmod` `~/.codex` like the other volumes (it holds `auth.json`, so keep it node-owned and not group/world-readable).

**2. Backup/restore tooling** — `scripts/dev-state-backup.sh`
- `detect` / `backup` / `restore` / `verify` over `ssh` + `docker exec` (same transport as the `dev` CLI; connection from the `dev-remote` profile, or `DEV_SSH_HOST` / `DEV_CONTAINER_PATTERN` env).
- Curated by default (excludes `*.sqlite` runtime DBs — Codex `logs_*.sqlite` is multi-GB — plus caches/snapshots); `--full` keeps everything.
- A **quiesce gate** refuses to snapshot while a `claude`/`codex` agent is mid-write (`--allow-live` to override), and manifest-based verification runs on both ends (archive integrity, key/secret files, session counts, find-vs-tar selection diff, post-restore presence + smoke test).
- Secrets-aware: backup dir is `chmod 700` and the script refuses to write inside a git repo.

**3. Docs + skill**
- `docs/devcontainer-state-backup.md` — colleague-facing runbook, including why "absolute paths" matter (Claude path-encodes the workspace into dir names + transcript `cwd`) and an appendix for restoring into a *different* path. Same-path round-trip needs no rewriting.
- `.agents/skills/devcontainer-state-backup/` (+ `.claude/skills` symlink) — agent-facing runbook.

## Why this PR unblocks the rebuild

The rebuild only persists `~/.codex` going forward if `codex-config` is in the remote checkout's compose file first. Merge this, `git pull` on the remote, then rebuild + restore.

## Verification

- Script: `bash -n` + shellcheck clean; selection logic unit-tested against a mock home (curated excludes drop `*.sqlite`/caches; keeps sessions/memory/auth; `--full` keeps all).
- A real verified backup of the current container is already in hand: **344 Claude + 14 Codex** transcripts, all key/secret files present, archive integrity OK, find-vs-tar diff empty.
- `scripts/sync-agent-skills.sh --check` passes; pre-push size + changed-surface checks pass.

No Linear issue — devcontainer/infra tooling.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

