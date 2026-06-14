# SerendipityOneInc/ecap-workspace — commits 2026-06-13

共 13 条 commits

## chore: default local worktrees away from tmux (#2435)

- **SHA**: `075d78620d536f954b295f85848366048308ea2c`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-13T15:52:38Z
- **PR**: #2435

### 完整 commit message

```
chore: default local worktrees away from tmux (#2435)

## Summary

- Default `scripts/worktree.sh` to skip tmux on local macOS sessions.
- Add `--tmux` to force the old tmux launch behavior when needed.
- Keep Linux, devcontainer, and SSH/server workflows on the existing
tmux default.

## Validation

- `bash -n scripts/worktree.sh`
- `bash scripts/worktree.sh --help`
```

### PR body

## Summary

- Default `scripts/worktree.sh` to skip tmux on local macOS sessions.
- Add `--tmux` to force the old tmux launch behavior when needed.
- Keep Linux, devcontainer, and SSH/server workflows on the existing tmux default.

## Validation

- `bash -n scripts/worktree.sh`
- `bash scripts/worktree.sh --help`


---

## chore(harness): consolidate push verification into husky pre-push (drop duplicate Claude hook) (#2434)

- **SHA**: `4755c8d6f5adb05a7bb2a4066e0ef71fb997d505`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-13T14:55:49Z
- **PR**: #2434

### 完整 commit message

```
chore(harness): consolidate push verification into husky pre-push (drop duplicate Claude hook) (#2434)

## What & why

Removes the **double-run** in the local verification setup. Verification
was running in two places — husky **pre-commit** (partial) and a
separate Claude **PreToolUse pre-push** hook (full) — so `eslint` /
`ruff` / `pyright` / `import-linter` effectively ran **twice** across
the commit→push cycle. This consolidates the push gate into one
client-side place that covers **both humans and Claude**.

(Background discussion: husky vs Claude hooks, and why a single push
gate is cleaner — git's `pre-push` hands the hook the exact refs on
stdin, so no command-string parsing is needed; and husky covers human
devs too, which a Claude-only hook didn't.)

## Changes

- **`scripts/verify-changed.sh` (new)** — detects the surfaces the
current branch changed (vs `origin/main`) and runs the fast checks:
`verify-web.sh --no-test` (guards + tsc + eslint) for `web/app`,
`verify-py.sh` (ruff + ruff-format + pyright + import-linter) for
`claw-interface`. **Conservative**: degrades to allow (exit 0/3) when
`origin/main` or tooling is missing; exit 1 only on a real failure.
Usable by hand too.
- **`web/.husky/pre-push`** — rewritten to **bash**; reads the push refs
from stdin **once**, keeps the PR-size gate, and adds the verify gate —
but only when pushing **the current branch's tip** (tags/releases and
deletions skip — git gives us the refs, so no command parsing). Bypass:
`SKIP_VERIFY=1` / `SKIP_PR_SIZE_CHECK=1` / `--no-verify` / `HUSKY=0`.
- **`web/.husky/pre-commit`** — bash shebang (consistency); the
frontend-lint step now **degrades** when `web/node_modules` is absent (a
`--no-node` worktree) instead of hard-failing the commit.
- **Deleted** `scripts/hooks/pre-push-verify.sh` and its
`.claude/settings.json` entry. Claude hooks now = SessionStart fetch (no
git equivalent) + screenshot guard.
- These run in worktrees via `scripts/.worktree-setup.sh`'s
`core.hooksPath` wiring.

## Verification (hooks tested directly + dogfooded)

Simulated push refs into the hook: **allows** tag-only / deletion /
no-surface / clean current-branch pushes; **blocks** (exit 1, with
bypass hint) a committed `ruff` violation on the current branch;
`verify-changed.sh` **degrades** (exit 3) on missing tooling.
`shellcheck -S warning` clean on all three scripts. This PR's own push
exercised the new pre-push hook (allowed — no `web/app`/`py` surface).

Found and fixed one bug along the way: `if ! cmd; then rc=$?` reads the
negation's status (0), masking a real failure — switched to capturing
`rc` directly.

## Scope
Touches `.claude/settings.json`, `scripts/**`, `web/.husky/**`,
`AGENTS.md` — no `web/**` app source or `services/**`, so the web/python
quality suites don't run here.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR body

## What & why

Removes the **double-run** in the local verification setup. Verification was running in two places — husky **pre-commit** (partial) and a separate Claude **PreToolUse pre-push** hook (full) — so `eslint` / `ruff` / `pyright` / `import-linter` effectively ran **twice** across the commit→push cycle. This consolidates the push gate into one client-side place that covers **both humans and Claude**.

(Background discussion: husky vs Claude hooks, and why a single push gate is cleaner — git's `pre-push` hands the hook the exact refs on stdin, so no command-string parsing is needed; and husky covers human devs too, which a Claude-only hook didn't.)

## Changes

- **`scripts/verify-changed.sh` (new)** — detects the surfaces the current branch changed (vs `origin/main`) and runs the fast checks: `verify-web.sh --no-test` (guards + tsc + eslint) for `web/app`, `verify-py.sh` (ruff + ruff-format + pyright + import-linter) for `claw-interface`. **Conservative**: degrades to allow (exit 0/3) when `origin/main` or tooling is missing; exit 1 only on a real failure. Usable by hand too.
- **`web/.husky/pre-push`** — rewritten to **bash**; reads the push refs from stdin **once**, keeps the PR-size gate, and adds the verify gate — but only when pushing **the current branch's tip** (tags/releases and deletions skip — git gives us the refs, so no command parsing). Bypass: `SKIP_VERIFY=1` / `SKIP_PR_SIZE_CHECK=1` / `--no-verify` / `HUSKY=0`.
- **`web/.husky/pre-commit`** — bash shebang (consistency); the frontend-lint step now **degrades** when `web/node_modules` is absent (a `--no-node` worktree) instead of hard-failing the commit.
- **Deleted** `scripts/hooks/pre-push-verify.sh` and its `.claude/settings.json` entry. Claude hooks now = SessionStart fetch (no git equivalent) + screenshot guard.
- These run in worktrees via `scripts/.worktree-setup.sh`'s `core.hooksPath` wiring.

## Verification (hooks tested directly + dogfooded)

Simulated push refs into the hook: **allows** tag-only / deletion / no-surface / clean current-branch pushes; **blocks** (exit 1, with bypass hint) a committed `ruff` violation on the current branch; `verify-changed.sh` **degrades** (exit 3) on missing tooling. `shellcheck -S warning` clean on all three scripts. This PR's own push exercised the new pre-push hook (allowed — no `web/app`/`py` surface).

Found and fixed one bug along the way: `if ! cmd; then rc=$?` reads the negation's status (0), masking a real failure — switched to capturing `rc` directly.

## Scope
Touches `.claude/settings.json`, `scripts/**`, `web/.husky/**`, `AGENTS.md` — no `web/**` app source or `services/**`, so the web/python quality suites don't run here.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## docs(verify): correct CF Access topology + add real-staging validation path (#2432)

- **SHA**: `1dbd96fd6c15157ea53846fb9956ddaea8d87251`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-13T14:45:32Z
- **PR**: #2432

### 完整 commit message

```
docs(verify): correct CF Access topology + add real-staging validation path (#2432)

## 背景

排查 `/verify-local` 的 staging 验证路径时，用 Cloudflare API 实读了 Access
策略，发现旧认知错误：
- **staging `claw-interface` 不在 CF Access 后面**（无任何 Access app 覆盖）→ 本地连
staging 验证**从不需要** CF service token。
- **production 的 CF Access 只罩 `/admin`·`/internal` path**，通用 API 不在其后。

据此一并把 Layer 1/2/3 按最新事实更新。敏感细节（IP allowlist / service token id / policy
名 / prod 边缘姿态）**不入库**，统一记录在内部 **Linear INF-366**。

## 改动

**Layer 1 — 纠正（行为修复，不只是措辞）**
- `docs/setup/cloudflare-access.md`：新增"实际拓扑（2026-06 实测）"节，先讲清什么在/不在 CF
Access 后，避免再误导人去申请不需要的 token（脱敏）。
-
`.claude/commands/verify-local.md`、`.claude/commands/dev-staging.md`：删除"staging
需 CF token / `/api/*` 缺 token 全 403"的错误说法；保留已写对的真前置（真实登录态 + Firebase
staging + account 服务 localhost CORS）。

**Layer 2 — 新能力：免 token 连真实 staging**
- 新增 `scripts/dev-staging.sh`（对标 `dev-mock.sh`）：探 staging 后端可达性 → 起
`pnpm dev:staging` → 回显实际端口 → 守 stray `web/app/.env`/`.env.local` 覆盖。
- `/dev-staging` 增"真实登录态"节：`capture-and-reuse`（Playwright storageState）/
手动 OTP / 专用测试账号三策，并把 **account 服务 localhost CORS** 标为第一个要先验的后端依赖。

**Layer 3 — 策略**
- plan 第二批把"给 mock 堆保真度（SSE/可配置状态）"**降级**：能用真 staging 验的盲区优先走真后端，mock
退守离线/确定性/单测 stub 同源。

## 验证
- `bash -n scripts/dev-staging.sh` 通过；shellcheck 仅 SC1091 info（与
`dev-mock.sh` 同款，由 `# shellcheck source=` 处理）。
- 纯 docs/skills/script 改动，不触 `web/**`、`services/**`，不影响应用构建。
- `web/app/.env.staging.local`（gitignored）本地已同步更正，不入库。

## 关联
- Linear **INF-366**（CF Access office-IP bypass + 通用 API/staging 未受保护 +
跨 SaaS secrets/vault 治理；assignee allenz）
- 后续：真 staging 路径的可复现登录态 + localhost CORS 后端依赖，跟踪在 INF-366

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR body

## 背景

排查 `/verify-local` 的 staging 验证路径时，用 Cloudflare API 实读了 Access 策略，发现旧认知错误：
- **staging `claw-interface` 不在 CF Access 后面**（无任何 Access app 覆盖）→ 本地连 staging 验证**从不需要** CF service token。
- **production 的 CF Access 只罩 `/admin`·`/internal` path**，通用 API 不在其后。

据此一并把 Layer 1/2/3 按最新事实更新。敏感细节（IP allowlist / service token id / policy 名 / prod 边缘姿态）**不入库**，统一记录在内部 **Linear INF-366**。

## 改动

**Layer 1 — 纠正（行为修复，不只是措辞）**
- `docs/setup/cloudflare-access.md`：新增"实际拓扑（2026-06 实测）"节，先讲清什么在/不在 CF Access 后，避免再误导人去申请不需要的 token（脱敏）。
- `.claude/commands/verify-local.md`、`.claude/commands/dev-staging.md`：删除"staging 需 CF token / `/api/*` 缺 token 全 403"的错误说法；保留已写对的真前置（真实登录态 + Firebase staging + account 服务 localhost CORS）。

**Layer 2 — 新能力：免 token 连真实 staging**
- 新增 `scripts/dev-staging.sh`（对标 `dev-mock.sh`）：探 staging 后端可达性 → 起 `pnpm dev:staging` → 回显实际端口 → 守 stray `web/app/.env`/`.env.local` 覆盖。
- `/dev-staging` 增"真实登录态"节：`capture-and-reuse`（Playwright storageState）/ 手动 OTP / 专用测试账号三策，并把 **account 服务 localhost CORS** 标为第一个要先验的后端依赖。

**Layer 3 — 策略**
- plan 第二批把"给 mock 堆保真度（SSE/可配置状态）"**降级**：能用真 staging 验的盲区优先走真后端，mock 退守离线/确定性/单测 stub 同源。

## 验证
- `bash -n scripts/dev-staging.sh` 通过；shellcheck 仅 SC1091 info（与 `dev-mock.sh` 同款，由 `# shellcheck source=` 处理）。
- 纯 docs/skills/script 改动，不触 `web/**`、`services/**`，不影响应用构建。
- `web/app/.env.staging.local`（gitignored）本地已同步更正，不入库。

## 关联
- Linear **INF-366**（CF Access office-IP bypass + 通用 API/staging 未受保护 + 跨 SaaS secrets/vault 治理；assignee allenz）
- 后续：真 staging 路径的可复现登录态 + localhost CORS 后端依赖，跟踪在 INF-366

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## chore(harness): add SessionStart fetch + pre-push verify gate hooks (#2431)

- **SHA**: `57bb406f3819265cf6e96cd4daa9769686c6e586`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-13T14:04:23Z
- **PR**: #2431

### 完整 commit message

```
chore(harness): add SessionStart fetch + pre-push verify gate hooks (#2431)

## What & why

Implements the two deferred follow-ups from the harness work (#2424 /
#2425), both wired into `.claude/settings.json` so they run for **every
session — worktrees included** (husky doesn't install in worktrees,
where most work happens).

### 1. SessionStart → `scripts/hooks/session-start-fetch.sh`
**Problem:** ~52/56 sampled sessions opened with the same manual ritual
— `git fetch origin main` + checking how far behind the branch is. Stale
local main is the usual cause of "fails CI but reproduces nowhere" (CI
tests `refs/pull/N/merge` = the PR merged into *current* main).
`worktree.sh` fetches only when it **creates** a worktree, so a
pre-existing worktree resumed days later sits on stale main.

**Fix:** best-effort `git fetch origin main` at session start, reports
if the branch is behind. **Never blocks** — offline / no remote just
prints a note; always exits 0; output is one terse line (it becomes
session context).

### 2. PreToolUse(Bash) → `scripts/hooks/pre-push-verify.sh`
**Problem:** changes pushed without local verification fail CI minutes
later on `tsc` / lint / governance-guard / ruff / pyright — the
recurring "forgot to verify" friction.

**Fix:** before a `git push` of a branch, run the **fast** local CI
checks for the changed surfaces (`verify-web.sh --no-test` = guards +
tsc + eslint; `verify-py.sh` = ruff + ruff-format + pyright +
import-linter) and **block the push** on a real failure.

**Conservative by design — it must never strand you unable to push:**
- Only gates real branch pushes (skips deletes, tag pushes, `git -C
<other>` pushes).
- **Degrades to allow** (with a note) whenever it can't run
authoritatively: `origin/main` missing, `web/node_modules` absent,
backend venv absent.
- **Denies only** on a genuine verify failure (exit 1) with tooling
present; a degraded-skip (exit 3) is allowed.
- **Bypass:** `SKIP_VERIFY=1 git push …` (or `--no-verify`).
- Fast tier only (no vitest/pytest) — heavy suites stay a `--full` / CI
concern.

## Verification (hooks tested directly via simulated tool-call JSON)
- `pre-push-verify.sh`: allows non-push / `SKIP_VERIFY=1` / `--delete` /
no-CI-surface commands (exit 0); **denies** (exit 2 +
`permissionDecision:"deny"` JSON) when a staged `import os` (ruff F401)
makes `verify-py.sh` exit 1.
- `session-start-fetch.sh`: prints one line ("up to date with
origin/main"), exits 0.
- `.claude/settings.json` is valid JSON; `shellcheck -S warning` clean
on both hooks; both are `100755`.

## Scope
Touches only `.claude/settings.json`, `scripts/hooks/**`, and
`AGENTS.md` — no `web/**` or `services/**` source, so the web/python
quality suites don't run on this PR.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR body

## What & why

Implements the two deferred follow-ups from the harness work (#2424 / #2425), both wired into `.claude/settings.json` so they run for **every session — worktrees included** (husky doesn't install in worktrees, where most work happens).

### 1. SessionStart → `scripts/hooks/session-start-fetch.sh`
**Problem:** ~52/56 sampled sessions opened with the same manual ritual — `git fetch origin main` + checking how far behind the branch is. Stale local main is the usual cause of "fails CI but reproduces nowhere" (CI tests `refs/pull/N/merge` = the PR merged into *current* main). `worktree.sh` fetches only when it **creates** a worktree, so a pre-existing worktree resumed days later sits on stale main.

**Fix:** best-effort `git fetch origin main` at session start, reports if the branch is behind. **Never blocks** — offline / no remote just prints a note; always exits 0; output is one terse line (it becomes session context).

### 2. PreToolUse(Bash) → `scripts/hooks/pre-push-verify.sh`
**Problem:** changes pushed without local verification fail CI minutes later on `tsc` / lint / governance-guard / ruff / pyright — the recurring "forgot to verify" friction.

**Fix:** before a `git push` of a branch, run the **fast** local CI checks for the changed surfaces (`verify-web.sh --no-test` = guards + tsc + eslint; `verify-py.sh` = ruff + ruff-format + pyright + import-linter) and **block the push** on a real failure.

**Conservative by design — it must never strand you unable to push:**
- Only gates real branch pushes (skips deletes, tag pushes, `git -C <other>` pushes).
- **Degrades to allow** (with a note) whenever it can't run authoritatively: `origin/main` missing, `web/node_modules` absent, backend venv absent.
- **Denies only** on a genuine verify failure (exit 1) with tooling present; a degraded-skip (exit 3) is allowed.
- **Bypass:** `SKIP_VERIFY=1 git push …` (or `--no-verify`).
- Fast tier only (no vitest/pytest) — heavy suites stay a `--full` / CI concern.

## Verification (hooks tested directly via simulated tool-call JSON)
- `pre-push-verify.sh`: allows non-push / `SKIP_VERIFY=1` / `--delete` / no-CI-surface commands (exit 0); **denies** (exit 2 + `permissionDecision:"deny"` JSON) when a staged `import os` (ruff F401) makes `verify-py.sh` exit 1.
- `session-start-fetch.sh`: prints one line ("up to date with origin/main"), exits 0.
- `.claude/settings.json` is valid JSON; `shellcheck -S warning` clean on both hooks; both are `100755`.

## Scope
Touches only `.claude/settings.json`, `scripts/hooks/**`, and `AGENTS.md` — no `web/**` or `services/**` source, so the web/python quality suites don't run on this PR.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## ci(pr-title-check): drop the feat->Linear-URL requirement (#2430)

- **SHA**: `ecd845afff4c52bfe5c207870845dc47be5b27f0`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-13T13:09:08Z
- **PR**: #2430

### 完整 commit message

```
ci(pr-title-check): drop the feat->Linear-URL requirement (#2430)

## What

Remove the rule in `pr-title-check.yml` that hard-blocks `feat` PRs
unless the
body contains a full Linear issue URL. The **Conventional Commits title
check is
kept unchanged**; only the feat→Linear enforcement is dropped.

## Why

- The hard block rejected legitimate `feat` PRs that have no tracked
Linear
issue, and nudged authors to mislabel real features as `chore` just to
pass CI
  (a title-accuracy loss).
- Linking the Linear issue is still useful for traceability — it stays a
  **recommended convention**, just not a merge gate.

## Changes

- `.github/workflows/pr-title-check.yml`: drop the `if [[ "$TYPE" ==
"feat" ]]`
Linear-URL block and its header comment; rename the step to "Validate
title".
  Also removes the now-unused `BODY` / `REPO` env inputs — a smaller
  workflow-injection surface (only `TITLE` is read now).
- `AGENTS.md` (= `CLAUDE.md` via symlink): the feat→Linear bullet is now
  "recommended, no longer CI-enforced".
- `README.md`: workflow table cell updated.
- `.github/PULL_REQUEST_TEMPLATE/feat.md`: Linear field is recommended,
not
  required; dropped the "CI 会硬拦截" warning.

## Test

- `python3 -c "yaml.safe_load(...)"` parses clean.
- The remaining `run:` block is just the Conventional Commits regex
check
  (verified by inspection); no `feat`-specific path remains.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR body

## What

Remove the rule in `pr-title-check.yml` that hard-blocks `feat` PRs unless the
body contains a full Linear issue URL. The **Conventional Commits title check is
kept unchanged**; only the feat→Linear enforcement is dropped.

## Why

- The hard block rejected legitimate `feat` PRs that have no tracked Linear
  issue, and nudged authors to mislabel real features as `chore` just to pass CI
  (a title-accuracy loss).
- Linking the Linear issue is still useful for traceability — it stays a
  **recommended convention**, just not a merge gate.

## Changes

- `.github/workflows/pr-title-check.yml`: drop the `if [[ "$TYPE" == "feat" ]]`
  Linear-URL block and its header comment; rename the step to "Validate title".
  Also removes the now-unused `BODY` / `REPO` env inputs — a smaller
  workflow-injection surface (only `TITLE` is read now).
- `AGENTS.md` (= `CLAUDE.md` via symlink): the feat→Linear bullet is now
  "recommended, no longer CI-enforced".
- `README.md`: workflow table cell updated.
- `.github/PULL_REQUEST_TEMPLATE/feat.md`: Linear field is recommended, not
  required; dropped the "CI 会硬拦截" warning.

## Test

- `python3 -c "yaml.safe_load(...)"` parses clean.
- The remaining `run:` block is just the Conventional Commits regex check
  (verified by inspection); no `feat`-specific path remains.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## chore(scripts): add --anon and --localhost presets to CDP debug launcher (#2429)

- **SHA**: `4feee46b5f79275e284b16a8742720418fe5d3f8`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-13T13:08:39Z
- **PR**: #2429

### 完整 commit message

```
chore(scripts): add --anon and --localhost presets to CDP debug launcher (#2429)

## What & why

`scripts/open-chrome-debug-profile.sh` only modeled the deployed
staging/production dimension. This adds two **orthogonal** preset
dimensions so
every local validation target is one flag away — each with its own
profile dir
and CDP port, so they coexist and never clobber each other's session:

| preset | URL | profile dir | CDP port |
|--------|-----|-------------|----------|
| `staging` (default) | `ecap.gensmo.nosay.live/chat` |
`~/.cache/ecap-chrome-cdp` | 9222 |
| `staging --anon` | same | `…-anon` | 9322 |
| `production` | `zooclaw.ai/chat` | `…-prod` | 9223 |
| `production --anon` | same | `…-prod-anon` | 9323 |
| `--localhost [PORT]` | `localhost:<PORT\|3000>/chat` | `…-local` |
9422 |
| `--localhost --anon` | same | `…-local-anon` | 9522 |

- **`--anon`** — a never-signed-in profile for the logged-out experience
(login
redirects, public pages). Replaces the manual `--profile-dir … --port …`
dance.
- **`--localhost [PORT]`** — drive a local dev server (`pnpm
dev:staging`, which
serves a local frontend against the **real** staging backend) with the
same
CDP + `lib.mjs` tooling. This is the complement to mock-backend for
things mock
  can't cover — a real Mattermost / bot path. The dev-server port shifts
(`next dev` slides 3000 → 3002 → 3006…), so it is **passed in, not
hardcoded**;
  the CDP debug port stays fixed (9422 / 9522).

## Docs

- `scripts/cdp/README.md`: new **Prerequisites / first run** section
(the profile
is created empty under `~/.cache` and needs a one-time manual sign-in —
nothing
is shared/exportable across machines, so a new dev/machine just signs in
once),
plus a `--localhost` section noting the port-shift gotcha and the
localhost-is-a-
  different-origin login boundary.
- `scripts/README.md`, `/prod-validate`, `/dev-staging` synced to the
new flags.

## Test

- `bash -n` clean, `shellcheck` clean.
- Verified all six `--env`/`--anon`/`--localhost` combinations resolve
the right
  URL / profile dir / CDP port, that flag order is irrelevant, that the
`CHROME_DEBUG_*` env-var forms work, and that the live-Stripe warning is
  correctly suppressed under `--localhost`.
- Behavior with no flags is unchanged (staging on :9222).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR body

## What & why

`scripts/open-chrome-debug-profile.sh` only modeled the deployed
staging/production dimension. This adds two **orthogonal** preset dimensions so
every local validation target is one flag away — each with its own profile dir
and CDP port, so they coexist and never clobber each other's session:

| preset | URL | profile dir | CDP port |
|--------|-----|-------------|----------|
| `staging` (default) | `ecap.gensmo.nosay.live/chat` | `~/.cache/ecap-chrome-cdp` | 9222 |
| `staging --anon` | same | `…-anon` | 9322 |
| `production` | `zooclaw.ai/chat` | `…-prod` | 9223 |
| `production --anon` | same | `…-prod-anon` | 9323 |
| `--localhost [PORT]` | `localhost:<PORT\|3000>/chat` | `…-local` | 9422 |
| `--localhost --anon` | same | `…-local-anon` | 9522 |

- **`--anon`** — a never-signed-in profile for the logged-out experience (login
  redirects, public pages). Replaces the manual `--profile-dir … --port …` dance.
- **`--localhost [PORT]`** — drive a local dev server (`pnpm dev:staging`, which
  serves a local frontend against the **real** staging backend) with the same
  CDP + `lib.mjs` tooling. This is the complement to mock-backend for things mock
  can't cover — a real Mattermost / bot path. The dev-server port shifts
  (`next dev` slides 3000 → 3002 → 3006…), so it is **passed in, not hardcoded**;
  the CDP debug port stays fixed (9422 / 9522).

## Docs

- `scripts/cdp/README.md`: new **Prerequisites / first run** section (the profile
  is created empty under `~/.cache` and needs a one-time manual sign-in — nothing
  is shared/exportable across machines, so a new dev/machine just signs in once),
  plus a `--localhost` section noting the port-shift gotcha and the localhost-is-a-
  different-origin login boundary.
- `scripts/README.md`, `/prod-validate`, `/dev-staging` synced to the new flags.

## Test

- `bash -n` clean, `shellcheck` clean.
- Verified all six `--env`/`--anon`/`--localhost` combinations resolve the right
  URL / profile dir / CDP port, that flag order is irrelevant, that the
  `CHROME_DEBUG_*` env-var forms work, and that the live-Stripe warning is
  correctly suppressed under `--localhost`.
- Behavior with no flags is unchanged (staging on :9222).

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## chore(deps): update openai requirement from <2.39.0,>=2.38.0 to >=2.41.0,<2.42.0 in /services/claw-interface (#2418)

- **SHA**: `604ef347b0b963c0d244aac1e590b6d3447c6e8b`
- **作者**: dependabot[bot]
- **日期**: 2026-06-13T12:57:58Z
- **PR**: #2418

### 完整 commit message

```
chore(deps): update openai requirement from <2.39.0,>=2.38.0 to >=2.41.0,<2.42.0 in /services/claw-interface (#2418)

Updates the requirements on
[openai](https://github.com/openai/openai-python) to permit the latest
version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/openai/openai-python/releases">openai's
releases</a>.</em></p>
<blockquote>
<h2>v2.41.0</h2>
<h2>2.41.0 (2026-06-03)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.40.0...v2.41.0">v2.40.0...v2.41.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> responses.moderation and
chat_completions.moderation (<a
href="https://github.com/openai/openai-python/commit/87e46c25ac9ca8cff407b52ad9fb33e326c059d6">87e46c2</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/openai/openai-python/blob/main/CHANGELOG.md">openai's
changelog</a>.</em></p>
<blockquote>
<h2>2.41.0 (2026-06-03)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.40.0...v2.41.0">v2.40.0...v2.41.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> responses.moderation and
chat_completions.moderation (<a
href="https://github.com/openai/openai-python/commit/87e46c25ac9ca8cff407b52ad9fb33e326c059d6">87e46c2</a>)</li>
</ul>
<h2>2.40.0 (2026-06-01)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.39.0...v2.40.0">v2.39.0...v2.40.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> Add Amazon Bedrock Responses support</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> allow setting bedrock api keys on the client
directly (<a
href="https://github.com/openai/openai-python/commit/4d5bfdec37fa8a2b2a0413724755e586e627e28d">4d5bfde</a>)</li>
</ul>
<h2>2.39.0 (2026-06-01)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.38.0...v2.39.0">v2.38.0...v2.39.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> workload identity in audit logs,
additional_tools item in responses, fix ActionSearch.query to be
optional. (<a
href="https://github.com/openai/openai-python/commit/ab60d7a52c310bb0490ff36b8bdc33b8d4ea725f">ab60d7a</a>)</li>
</ul>
<h2>2.38.0 (2026-05-21)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.37.0...v2.38.0">v2.37.0...v2.38.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> api update (<a
href="https://github.com/openai/openai-python/commit/33d1d013250053886a73d178136e6bd1b09df059">33d1d01</a>)</li>
<li><strong>api:</strong> manual updates (<a
href="https://github.com/openai/openai-python/commit/a21700a2cd510cb9e6c88065ac8e942d4c041aa8">a21700a</a>)</li>
<li><strong>api:</strong> update OpenAPI spec or Stainless config (<a
href="https://github.com/openai/openai-python/commit/00265c5daba4d2481452ad35220f1556dab6bcf6">00265c5</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li><strong>api:</strong> docs updates (<a
href="https://github.com/openai/openai-python/commit/ee101520d49e22c09cf8096f8cbb3848ea58a1f9">ee10152</a>)</li>
<li>check release PR custom code sync (<a
href="https://github.com/openai/openai-python/commit/2638779a5b8fffaa8fdb6eebc1d734f15d2491f8">2638779</a>)</li>
<li>remove release automation trigger (<a
href="https://github.com/openai/openai-python/commit/bd6eea559f2996d914258a65e645981bdce3cad4">bd6eea5</a>)</li>
<li>trigger release automation (<a
href="https://github.com/openai/openai-python/commit/f62d08201eea8e08d4bb3385662f934d4adccb29">f62d082</a>)</li>
</ul>
<h2>2.37.0 (2026-05-13)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.36.0...v2.37.0">v2.36.0...v2.37.0</a></p>
<h3>Features</h3>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/openai/openai-python/commit/2d955a1ac69df0288b8072bbcd25905639e9b2ed"><code>2d955a1</code></a>
Merge pull request <a
href="https://redirect.github.com/openai/openai-python/issues/3359">#3359</a>
from openai/release-please--branches--main--changes-...</li>
<li><a
href="https://github.com/openai/openai-python/commit/519cd027919fa5b73bd8fe237e80c7a01b3e0b2f"><code>519cd02</code></a>
release: 2.41.0</li>
<li><a
href="https://github.com/openai/openai-python/commit/87e46c25ac9ca8cff407b52ad9fb33e326c059d6"><code>87e46c2</code></a>
feat(api): responses.moderation and chat_completions.moderation</li>
<li><a
href="https://github.com/openai/openai-python/commit/a28a3f6aa34f5ac6fcc2fafeb50112f2140c45ae"><code>a28a3f6</code></a>
Merge pull request <a
href="https://redirect.github.com/openai/openai-python/issues/3352">#3352</a>
from openai/release-please--branches--main--changes-...</li>
<li><a
href="https://github.com/openai/openai-python/commit/db6ccafa7b74b72caefbda6fb63bd5c904521770"><code>db6ccaf</code></a>
Update CHANGELOG.md</li>
<li><a
href="https://github.com/openai/openai-python/commit/2264f700dad91e4f570eb7c0a6f10bbd22d34520"><code>2264f70</code></a>
release: 2.40.0</li>
<li><a
href="https://github.com/openai/openai-python/commit/4d5bfdec37fa8a2b2a0413724755e586e627e28d"><code>4d5bfde</code></a>
fix(api): allow setting bedrock api keys on the client directly</li>
<li><a
href="https://github.com/openai/openai-python/commit/ccef1436d9f52b5014597047e450eef543a87540"><code>ccef143</code></a>
Merge pull request <a
href="https://redirect.github.com/openai/openai-python/issues/3326">#3326</a>
from openai/codex/bedrock-responses-review</li>
<li><a
href="https://github.com/openai/openai-python/commit/a50ff0a19084306a09012ff85f730ea2c129eef9"><code>a50ff0a</code></a>
Fix Bedrock with_options overrides</li>
<li><a
href="https://github.com/openai/openai-python/commit/fdf4901e301fa01b368ede0b5b407dca42f07acc"><code>fdf4901</code></a>
codegen metadata</li>
<li>Additional commits viewable in <a
href="https://github.com/openai/openai-python/compare/v2.38.0...v2.41.0">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR body

Updates the requirements on [openai](https://github.com/openai/openai-python) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/openai/openai-python/releases">openai's releases</a>.</em></p>
<blockquote>
<h2>v2.41.0</h2>
<h2>2.41.0 (2026-06-03)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.40.0...v2.41.0">v2.40.0...v2.41.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> responses.moderation and chat_completions.moderation (<a href="https://github.com/openai/openai-python/commit/87e46c25ac9ca8cff407b52ad9fb33e326c059d6">87e46c2</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/openai/openai-python/blob/main/CHANGELOG.md">openai's changelog</a>.</em></p>
<blockquote>
<h2>2.41.0 (2026-06-03)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.40.0...v2.41.0">v2.40.0...v2.41.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> responses.moderation and chat_completions.moderation (<a href="https://github.com/openai/openai-python/commit/87e46c25ac9ca8cff407b52ad9fb33e326c059d6">87e46c2</a>)</li>
</ul>
<h2>2.40.0 (2026-06-01)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.39.0...v2.40.0">v2.39.0...v2.40.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> Add Amazon Bedrock Responses support</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> allow setting bedrock api keys on the client directly (<a href="https://github.com/openai/openai-python/commit/4d5bfdec37fa8a2b2a0413724755e586e627e28d">4d5bfde</a>)</li>
</ul>
<h2>2.39.0 (2026-06-01)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.38.0...v2.39.0">v2.38.0...v2.39.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> workload identity in audit logs, additional_tools item in responses, fix ActionSearch.query to be optional. (<a href="https://github.com/openai/openai-python/commit/ab60d7a52c310bb0490ff36b8bdc33b8d4ea725f">ab60d7a</a>)</li>
</ul>
<h2>2.38.0 (2026-05-21)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.37.0...v2.38.0">v2.37.0...v2.38.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> api update (<a href="https://github.com/openai/openai-python/commit/33d1d013250053886a73d178136e6bd1b09df059">33d1d01</a>)</li>
<li><strong>api:</strong> manual updates (<a href="https://github.com/openai/openai-python/commit/a21700a2cd510cb9e6c88065ac8e942d4c041aa8">a21700a</a>)</li>
<li><strong>api:</strong> update OpenAPI spec or Stainless config (<a href="https://github.com/openai/openai-python/commit/00265c5daba4d2481452ad35220f1556dab6bcf6">00265c5</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li><strong>api:</strong> docs updates (<a href="https://github.com/openai/openai-python/commit/ee101520d49e22c09cf8096f8cbb3848ea58a1f9">ee10152</a>)</li>
<li>check release PR custom code sync (<a href="https://github.com/openai/openai-python/commit/2638779a5b8fffaa8fdb6eebc1d734f15d2491f8">2638779</a>)</li>
<li>remove release automation trigger (<a href="https://github.com/openai/openai-python/commit/bd6eea559f2996d914258a65e645981bdce3cad4">bd6eea5</a>)</li>
<li>trigger release automation (<a href="https://github.com/openai/openai-python/commit/f62d08201eea8e08d4bb3385662f934d4adccb29">f62d082</a>)</li>
</ul>
<h2>2.37.0 (2026-05-13)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.36.0...v2.37.0">v2.36.0...v2.37.0</a></p>
<h3>Features</h3>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/openai/openai-python/commit/2d955a1ac69df0288b8072bbcd25905639e9b2ed"><code>2d955a1</code></a> Merge pull request <a href="https://redirect.github.com/openai/openai-python/issues/3359">#3359</a> from openai/release-please--branches--main--changes-...</li>
<li><a href="https://github.com/openai/openai-python/commit/519cd027919fa5b73bd8fe237e80c7a01b3e0b2f"><code>519cd02</code></a> release: 2.41.0</li>
<li><a href="https://github.com/openai/openai-python/commit/87e46c25ac9ca8cff407b52ad9fb33e326c059d6"><code>87e46c2</code></a> feat(api): responses.moderation and chat_completions.moderation</li>
<li><a href="https://github.com/openai/openai-python/commit/a28a3f6aa34f5ac6fcc2fafeb50112f2140c45ae"><code>a28a3f6</code></a> Merge pull request <a href="https://redirect.github.com/openai/openai-python/issues/3352">#3352</a> from openai/release-please--branches--main--changes-...</li>
<li><a href="https://github.com/openai/openai-python/commit/db6ccafa7b74b72caefbda6fb63bd5c904521770"><code>db6ccaf</code></a> Update CHANGELOG.md</li>
<li><a href="https://github.com/openai/openai-python/commit/2264f700dad91e4f570eb7c0a6f10bbd22d34520"><code>2264f70</code></a> release: 2.40.0</li>
<li><a href="https://github.com/openai/openai-python/commit/4d5bfdec37fa8a2b2a0413724755e586e627e28d"><code>4d5bfde</code></a> fix(api): allow setting bedrock api keys on the client directly</li>
<li><a href="https://github.com/openai/openai-python/commit/ccef1436d9f52b5014597047e450eef543a87540"><code>ccef143</code></a> Merge pull request <a href="https://redirect.github.com/openai/openai-python/issues/3326">#3326</a> from openai/codex/bedrock-responses-review</li>
<li><a href="https://github.com/openai/openai-python/commit/a50ff0a19084306a09012ff85f730ea2c129eef9"><code>a50ff0a</code></a> Fix Bedrock with_options overrides</li>
<li><a href="https://github.com/openai/openai-python/commit/fdf4901e301fa01b368ede0b5b407dca42f07acc"><code>fdf4901</code></a> codegen metadata</li>
<li>Additional commits viewable in <a href="https://github.com/openai/openai-python/compare/v2.38.0...v2.41.0">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---

## chore(deps-dev): update ruff requirement from >=0.15.14 to >=0.15.16 in /services/claw-interface (#2419)

- **SHA**: `e18d3d9a2326e571ba23c8f1a22dd7a79a183445`
- **作者**: dependabot[bot]
- **日期**: 2026-06-13T12:57:43Z
- **PR**: #2419

### 完整 commit message

```
chore(deps-dev): update ruff requirement from >=0.15.14 to >=0.15.16 in /services/claw-interface (#2419)

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to
permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/releases">ruff's
releases</a>.</em></p>
<blockquote>
<h2>0.15.16</h2>
<h2>Release Notes</h2>
<p>Released on 2026-06-04.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>flake8-async</code>] Implement
<code>yield-in-context-manager-in-async-generator</code>
(<code>ASYNC119</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24644">#24644</a>)</li>
<li>[<code>pylint</code>] Narrow diagnostic range and exclude cases
without exception handlers (<code>PLW0717</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25440">#25440</a>)</li>
<li>[<code>ruff</code>] Treat <code>yield</code> before
<code>break</code> from a terminal loop as terminal
(<code>RUF075</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25447">#25447</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>eradicate</code>] Avoid flagging <code>ruff:ignore</code>
comments as code (<code>ERA001</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25537">#25537</a>)</li>
<li>[<code>eradicate</code>] Fix <code>ERA001</code>/<code>RUF100</code>
conflict when <code>noqa</code> is on commented-out code (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25414">#25414</a>)</li>
<li>[<code>pyflakes</code>] Avoid removing the <code>format</code> call
when it would change behavior (<code>F523</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25320">#25320</a>)</li>
<li>[<code>pylint</code>] Avoid syntax errors in invalid character
replacements in f-strings before Python 3.12 (<code>PLE2510</code>,
<code>PLE2512</code>, <code>PLE2513</code>, <code>PLE2514</code>,
<code>PLE2515</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25544">#25544</a>)</li>
<li>[<code>pyupgrade</code>] Avoid converting <code>format</code> calls
with more kinds of side effects (<code>UP032</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25484">#25484</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>flake8-pytest-style</code>] Avoid fixes for ambiguous
<code>argnames</code> and <code>argvalues</code> combinations
(<code>PT006</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24776">#24776</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Drop excess capacity from statement suites during parsing (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25368">#25368</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>[<code>pydocstyle</code>] Improve discoverability of rules enabled
for each convention (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24973">#24973</a>)</li>
<li>[<code>ruff</code>] Restore example code for Python versions before
3.15 (<code>RUF017</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25439">#25439</a>)</li>
<li>Fix typo <code>bin/active</code> → <code>bin/activate</code> in
tutorial (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25473">#25473</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Shrink additional parser AST collections (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25465">#25465</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a
href="https://github.com/Redslayer112"><code>@​Redslayer112</code></a></li>
<li><a
href="https://github.com/koriyoshi2041"><code>@​koriyoshi2041</code></a></li>
<li><a
href="https://github.com/George-Ogden"><code>@​George-Ogden</code></a></li>
<li><a
href="https://github.com/TejasAmle"><code>@​TejasAmle</code></a></li>
<li><a
href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a
href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
<li><a
href="https://github.com/loganrosen"><code>@​loganrosen</code></a></li>
<li><a
href="https://github.com/RafaelJohn9"><code>@​RafaelJohn9</code></a></li>
<li><a
href="https://github.com/adityasingh2400"><code>@​adityasingh2400</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's
changelog</a>.</em></p>
<blockquote>
<h2>0.15.16</h2>
<p>Released on 2026-06-04.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>flake8-async</code>] Implement
<code>yield-in-context-manager-in-async-generator</code>
(<code>ASYNC119</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24644">#24644</a>)</li>
<li>[<code>pylint</code>] Narrow diagnostic range and exclude cases
without exception handlers (<code>PLW0717</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25440">#25440</a>)</li>
<li>[<code>ruff</code>] Treat <code>yield</code> before
<code>break</code> from a terminal loop as terminal
(<code>RUF075</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25447">#25447</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>eradicate</code>] Avoid flagging <code>ruff:ignore</code>
comments as code (<code>ERA001</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25537">#25537</a>)</li>
<li>[<code>eradicate</code>] Fix <code>ERA001</code>/<code>RUF100</code>
conflict when <code>noqa</code> is on commented-out code (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25414">#25414</a>)</li>
<li>[<code>pyflakes</code>] Avoid removing the <code>format</code> call
when it would change behavior (<code>F523</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25320">#25320</a>)</li>
<li>[<code>pylint</code>] Avoid syntax errors in invalid character
replacements in f-strings before Python 3.12 (<code>PLE2510</code>,
<code>PLE2512</code>, <code>PLE2513</code>, <code>PLE2514</code>,
<code>PLE2515</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25544">#25544</a>)</li>
<li>[<code>pyupgrade</code>] Avoid converting <code>format</code> calls
with more kinds of side effects (<code>UP032</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25484">#25484</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>flake8-pytest-style</code>] Avoid fixes for ambiguous
<code>argnames</code> and <code>argvalues</code> combinations
(<code>PT006</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24776">#24776</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Drop excess capacity from statement suites during parsing (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25368">#25368</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>[<code>pydocstyle</code>] Improve discoverability of rules enabled
for each convention (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24973">#24973</a>)</li>
<li>[<code>ruff</code>] Restore example code for Python versions before
3.15 (<code>RUF017</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25439">#25439</a>)</li>
<li>Fix typo <code>bin/active</code> → <code>bin/activate</code> in
tutorial (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25473">#25473</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Shrink additional parser AST collections (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25465">#25465</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a
href="https://github.com/Redslayer112"><code>@​Redslayer112</code></a></li>
<li><a
href="https://github.com/koriyoshi2041"><code>@​koriyoshi2041</code></a></li>
<li><a
href="https://github.com/George-Ogden"><code>@​George-Ogden</code></a></li>
<li><a
href="https://github.com/TejasAmle"><code>@​TejasAmle</code></a></li>
<li><a
href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a
href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
<li><a
href="https://github.com/loganrosen"><code>@​loganrosen</code></a></li>
<li><a
href="https://github.com/RafaelJohn9"><code>@​RafaelJohn9</code></a></li>
<li><a
href="https://github.com/adityasingh2400"><code>@​adityasingh2400</code></a></li>
</ul>
<h2>0.15.15</h2>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/astral-sh/ruff/commit/6c498ab5394edc5622d7f348e12956bf86203716"><code>6c498ab</code></a>
Bump 0.15.16 (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25635">#25635</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/e51e132831c4e1c4a5ac00fca4c9256354ab99bf"><code>e51e132</code></a>
[<code>flake8-async</code>] Implement
<code>yield-in-context-manager-in-async-generator</code> (`AS...</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/7c6dcd9f2611999c449143d241c582dedf287964"><code>7c6dcd9</code></a>
[ty] Add caching for pattern match narrowing (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25613">#25613</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/27058fc071b542bf06395ba89cabed061d313ca6"><code>27058fc</code></a>
[ty] Compact retained definition and expression identities (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25606">#25606</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/bf80d05f007c939799f530c9e775ed9449f5b2eb"><code>bf80d05</code></a>
Fix CODEOWNERS syntax (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25622">#25622</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/10ccd511e94a81d1e836b174f1c553a73ff3f1b3"><code>10ccd51</code></a>
Shrink additional parser AST collections (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25465">#25465</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/0d7135f4d23e7f4d8404daed16b9ef11d14f3fb9"><code>0d7135f</code></a>
[ty] Upgrade Salsa (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25545">#25545</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/49493a3cea83a08fa9aa143695017c816a540f1d"><code>49493a3</code></a>
[ty] Show type alias value on hover (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25381">#25381</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/85207d3b7657a84252f266766cb0d56034dc21cc"><code>85207d3</code></a>
[ty] sys.implementation.version is not sys.version_info (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25608">#25608</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/a8a0614348c1fcf47fc9b666eff61a103914d520"><code>a8a0614</code></a>
[ty] Avoid retaining duplicate function signatures (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25609">#25609</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/astral-sh/ruff/compare/0.15.14...0.15.16">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR body

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's releases</a>.</em></p>
<blockquote>
<h2>0.15.16</h2>
<h2>Release Notes</h2>
<p>Released on 2026-06-04.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>flake8-async</code>] Implement <code>yield-in-context-manager-in-async-generator</code> (<code>ASYNC119</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/24644">#24644</a>)</li>
<li>[<code>pylint</code>] Narrow diagnostic range and exclude cases without exception handlers (<code>PLW0717</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25440">#25440</a>)</li>
<li>[<code>ruff</code>] Treat <code>yield</code> before <code>break</code> from a terminal loop as terminal (<code>RUF075</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25447">#25447</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>eradicate</code>] Avoid flagging <code>ruff:ignore</code> comments as code (<code>ERA001</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25537">#25537</a>)</li>
<li>[<code>eradicate</code>] Fix <code>ERA001</code>/<code>RUF100</code> conflict when <code>noqa</code> is on commented-out code (<a href="https://redirect.github.com/astral-sh/ruff/pull/25414">#25414</a>)</li>
<li>[<code>pyflakes</code>] Avoid removing the <code>format</code> call when it would change behavior (<code>F523</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25320">#25320</a>)</li>
<li>[<code>pylint</code>] Avoid syntax errors in invalid character replacements in f-strings before Python 3.12 (<code>PLE2510</code>, <code>PLE2512</code>, <code>PLE2513</code>, <code>PLE2514</code>, <code>PLE2515</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25544">#25544</a>)</li>
<li>[<code>pyupgrade</code>] Avoid converting <code>format</code> calls with more kinds of side effects (<code>UP032</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25484">#25484</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>flake8-pytest-style</code>] Avoid fixes for ambiguous <code>argnames</code> and <code>argvalues</code> combinations (<code>PT006</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/24776">#24776</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Drop excess capacity from statement suites during parsing (<a href="https://redirect.github.com/astral-sh/ruff/pull/25368">#25368</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>[<code>pydocstyle</code>] Improve discoverability of rules enabled for each convention (<a href="https://redirect.github.com/astral-sh/ruff/pull/24973">#24973</a>)</li>
<li>[<code>ruff</code>] Restore example code for Python versions before 3.15 (<code>RUF017</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25439">#25439</a>)</li>
<li>Fix typo <code>bin/active</code> → <code>bin/activate</code> in tutorial (<a href="https://redirect.github.com/astral-sh/ruff/pull/25473">#25473</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Shrink additional parser AST collections (<a href="https://redirect.github.com/astral-sh/ruff/pull/25465">#25465</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/Redslayer112"><code>@​Redslayer112</code></a></li>
<li><a href="https://github.com/koriyoshi2041"><code>@​koriyoshi2041</code></a></li>
<li><a href="https://github.com/George-Ogden"><code>@​George-Ogden</code></a></li>
<li><a href="https://github.com/TejasAmle"><code>@​TejasAmle</code></a></li>
<li><a href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
<li><a href="https://github.com/loganrosen"><code>@​loganrosen</code></a></li>
<li><a href="https://github.com/RafaelJohn9"><code>@​RafaelJohn9</code></a></li>
<li><a href="https://github.com/adityasingh2400"><code>@​adityasingh2400</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
<blockquote>
<h2>0.15.16</h2>
<p>Released on 2026-06-04.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>flake8-async</code>] Implement <code>yield-in-context-manager-in-async-generator</code> (<code>ASYNC119</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/24644">#24644</a>)</li>
<li>[<code>pylint</code>] Narrow diagnostic range and exclude cases without exception handlers (<code>PLW0717</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25440">#25440</a>)</li>
<li>[<code>ruff</code>] Treat <code>yield</code> before <code>break</code> from a terminal loop as terminal (<code>RUF075</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25447">#25447</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>eradicate</code>] Avoid flagging <code>ruff:ignore</code> comments as code (<code>ERA001</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25537">#25537</a>)</li>
<li>[<code>eradicate</code>] Fix <code>ERA001</code>/<code>RUF100</code> conflict when <code>noqa</code> is on commented-out code (<a href="https://redirect.github.com/astral-sh/ruff/pull/25414">#25414</a>)</li>
<li>[<code>pyflakes</code>] Avoid removing the <code>format</code> call when it would change behavior (<code>F523</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25320">#25320</a>)</li>
<li>[<code>pylint</code>] Avoid syntax errors in invalid character replacements in f-strings before Python 3.12 (<code>PLE2510</code>, <code>PLE2512</code>, <code>PLE2513</code>, <code>PLE2514</code>, <code>PLE2515</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25544">#25544</a>)</li>
<li>[<code>pyupgrade</code>] Avoid converting <code>format</code> calls with more kinds of side effects (<code>UP032</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25484">#25484</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>flake8-pytest-style</code>] Avoid fixes for ambiguous <code>argnames</code> and <code>argvalues</code> combinations (<code>PT006</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/24776">#24776</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Drop excess capacity from statement suites during parsing (<a href="https://redirect.github.com/astral-sh/ruff/pull/25368">#25368</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>[<code>pydocstyle</code>] Improve discoverability of rules enabled for each convention (<a href="https://redirect.github.com/astral-sh/ruff/pull/24973">#24973</a>)</li>
<li>[<code>ruff</code>] Restore example code for Python versions before 3.15 (<code>RUF017</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25439">#25439</a>)</li>
<li>Fix typo <code>bin/active</code> → <code>bin/activate</code> in tutorial (<a href="https://redirect.github.com/astral-sh/ruff/pull/25473">#25473</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Shrink additional parser AST collections (<a href="https://redirect.github.com/astral-sh/ruff/pull/25465">#25465</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/Redslayer112"><code>@​Redslayer112</code></a></li>
<li><a href="https://github.com/koriyoshi2041"><code>@​koriyoshi2041</code></a></li>
<li><a href="https://github.com/George-Ogden"><code>@​George-Ogden</code></a></li>
<li><a href="https://github.com/TejasAmle"><code>@​TejasAmle</code></a></li>
<li><a href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
<li><a href="https://github.com/loganrosen"><code>@​loganrosen</code></a></li>
<li><a href="https://github.com/RafaelJohn9"><code>@​RafaelJohn9</code></a></li>
<li><a href="https://github.com/adityasingh2400"><code>@​adityasingh2400</code></a></li>
</ul>
<h2>0.15.15</h2>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/astral-sh/ruff/commit/6c498ab5394edc5622d7f348e12956bf86203716"><code>6c498ab</code></a> Bump 0.15.16 (<a href="https://redirect.github.com/astral-sh/ruff/issues/25635">#25635</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/e51e132831c4e1c4a5ac00fca4c9256354ab99bf"><code>e51e132</code></a> [<code>flake8-async</code>] Implement <code>yield-in-context-manager-in-async-generator</code> (`AS...</li>
<li><a href="https://github.com/astral-sh/ruff/commit/7c6dcd9f2611999c449143d241c582dedf287964"><code>7c6dcd9</code></a> [ty] Add caching for pattern match narrowing (<a href="https://redirect.github.com/astral-sh/ruff/issues/25613">#25613</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/27058fc071b542bf06395ba89cabed061d313ca6"><code>27058fc</code></a> [ty] Compact retained definition and expression identities (<a href="https://redirect.github.com/astral-sh/ruff/issues/25606">#25606</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/bf80d05f007c939799f530c9e775ed9449f5b2eb"><code>bf80d05</code></a> Fix CODEOWNERS syntax (<a href="https://redirect.github.com/astral-sh/ruff/issues/25622">#25622</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/10ccd511e94a81d1e836b174f1c553a73ff3f1b3"><code>10ccd51</code></a> Shrink additional parser AST collections (<a href="https://redirect.github.com/astral-sh/ruff/issues/25465">#25465</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/0d7135f4d23e7f4d8404daed16b9ef11d14f3fb9"><code>0d7135f</code></a> [ty] Upgrade Salsa (<a href="https://redirect.github.com/astral-sh/ruff/issues/25545">#25545</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/49493a3cea83a08fa9aa143695017c816a540f1d"><code>49493a3</code></a> [ty] Show type alias value on hover (<a href="https://redirect.github.com/astral-sh/ruff/issues/25381">#25381</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/85207d3b7657a84252f266766cb0d56034dc21cc"><code>85207d3</code></a> [ty] sys.implementation.version is not sys.version_info (<a href="https://redirect.github.com/astral-sh/ruff/issues/25608">#25608</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/a8a0614348c1fcf47fc9b666eff61a103914d520"><code>a8a0614</code></a> [ty] Avoid retaining duplicate function signatures (<a href="https://redirect.github.com/astral-sh/ruff/issues/25609">#25609</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.15.14...0.15.16">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---

## chore(harness): add backend verify-py.sh + web governance guards + worktree reap/fetch (#2425)

- **SHA**: `38e0734fb6f76382458ca17a78adebf55cd06d6c`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-13T12:52:01Z
- **PR**: #2425

### 完整 commit message

```
chore(harness): add backend verify-py.sh + web governance guards + worktree reap/fetch (#2425)

## What & why

Repositioned as a **complement to #2424** (the parallel harness work
that landed `verify-web.sh`, mock-backend SSE, CI-wait scripts, the
screenshot hook, and the `/verify-local` `/release` skills). After #2424
+ #2426 merged, I compared this branch against `main` and **dropped
everything that overlapped** (a second web verifier; the "don't run
tests" doc reconciliation #2426 already did), keeping only what #2424
does **not** cover:

### 1. `scripts/verify-py.sh` (new) — the missing backend verifier
There is no Python verifier anywhere on `main`. This is the sibling of
#2424's `verify-web.sh`, built in the same idiom (shared
`scripts/lib/log.sh`, same `--*-only`/`--no-*` flags, same exit codes).
Default = `ruff check` + `ruff format --check` + `pyright app/ tests/` +
`lint-imports`; `--full` adds the full `scripts/ci-lint` guard set,
jscpd duplication, and `pytest` + coverage (`--cov-fail-under=90`, needs
mongo on `127.0.0.1`).

### 2. `scripts/verify-web.sh` — close a false-green gap
#2424's `verify-web.sh` (and its `/verify-local` runbook) describes
itself as mirroring CI's `lint-and-test`, but it omits the 7
`pre_lint_scripts` governance guards CI runs **before** ESLint — so a
change can pass it locally yet fail CI on a shrink-only / governance
guard. Added a guards step (runs first; `--guards-only` / `--no-guards`
to scope), making that claim true.

### 3. `scripts/worktree.sh` — #2424 never touched it
- **create** now `git fetch origin main` + bases new branches on
`origin/main` (no stale-main "fails CI but reproduces nowhere").
- new **`--reap <name>`** — idempotent teardown tolerant of partial
state (kill tmux → remove → prune → branch -D → remote), and refuses
harness-managed `.claude/worktrees/agent-*`.

### 4. Docs (additive on top of #2424/#2426)
Worktree fetch/reap/edit-path guidance; the `verify-py.sh` pointer (root
+ `services/claw-interface` AGENTS.md); and two PR-workflow corrections
not in #2424 — `gh pr create` has no `--disable-auto-merge` flag, and
`git reset --hard` is hard-denied.

## Verification
`verify-py.sh` default green (ruff/format/pyright/import-linter);
`verify-web.sh` full run green (7 guards + tsc + vitest + eslint,
518/518 test files); `worktree.sh --reap` refuses `agent-*` (exit 1) and
is idempotent on a missing name (exit 0); `shellcheck -S warning` clean
on all three scripts. Branch rebuilt on latest `main` (merge), so the PR
diff is exactly the 5-file complement above.

## Also fixed
De-flaked `tests/unit/lint/react-hooks-config.unit.spec.ts` — it
resolved the heavy ESLint flat config inside each `it()` and overran the
10s testTimeout under parallel load. Moved the resolution into a
`beforeAll` (60s hook budget); assertions are now synchronous. Same
contract, deterministic.

## Not included (left to CI, as documented)
`web-build-check` (`next build`), CodeQL, and the enterprise/dashboard
app suites — too slow / not runnable locally.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR body

## What & why

Repositioned as a **complement to #2424** (the parallel harness work that landed `verify-web.sh`, mock-backend SSE, CI-wait scripts, the screenshot hook, and the `/verify-local` `/release` skills). After #2424 + #2426 merged, I compared this branch against `main` and **dropped everything that overlapped** (a second web verifier; the "don't run tests" doc reconciliation #2426 already did), keeping only what #2424 does **not** cover:

### 1. `scripts/verify-py.sh` (new) — the missing backend verifier
There is no Python verifier anywhere on `main`. This is the sibling of #2424's `verify-web.sh`, built in the same idiom (shared `scripts/lib/log.sh`, same `--*-only`/`--no-*` flags, same exit codes). Default = `ruff check` + `ruff format --check` + `pyright app/ tests/` + `lint-imports`; `--full` adds the full `scripts/ci-lint` guard set, jscpd duplication, and `pytest` + coverage (`--cov-fail-under=90`, needs mongo on `127.0.0.1`).

### 2. `scripts/verify-web.sh` — close a false-green gap
#2424's `verify-web.sh` (and its `/verify-local` runbook) describes itself as mirroring CI's `lint-and-test`, but it omits the 7 `pre_lint_scripts` governance guards CI runs **before** ESLint — so a change can pass it locally yet fail CI on a shrink-only / governance guard. Added a guards step (runs first; `--guards-only` / `--no-guards` to scope), making that claim true.

### 3. `scripts/worktree.sh` — #2424 never touched it
- **create** now `git fetch origin main` + bases new branches on `origin/main` (no stale-main "fails CI but reproduces nowhere").
- new **`--reap <name>`** — idempotent teardown tolerant of partial state (kill tmux → remove → prune → branch -D → remote), and refuses harness-managed `.claude/worktrees/agent-*`.

### 4. Docs (additive on top of #2424/#2426)
Worktree fetch/reap/edit-path guidance; the `verify-py.sh` pointer (root + `services/claw-interface` AGENTS.md); and two PR-workflow corrections not in #2424 — `gh pr create` has no `--disable-auto-merge` flag, and `git reset --hard` is hard-denied.

## Verification
`verify-py.sh` default green (ruff/format/pyright/import-linter); `verify-web.sh` full run green (7 guards + tsc + vitest + eslint, 518/518 test files); `worktree.sh --reap` refuses `agent-*` (exit 1) and is idempotent on a missing name (exit 0); `shellcheck -S warning` clean on all three scripts. Branch rebuilt on latest `main` (merge), so the PR diff is exactly the 5-file complement above.

## Also fixed
De-flaked `tests/unit/lint/react-hooks-config.unit.spec.ts` — it resolved the heavy ESLint flat config inside each `it()` and overran the 10s testTimeout under parallel load. Moved the resolution into a `beforeAll` (60s hook budget); assertions are now synchronous. Same contract, deterministic.

## Not included (left to CI, as documented)
`web-build-check` (`next build`), CodeQL, and the enterprise/dashboard app suites — too slow / not runnable locally.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## fix(ci): drop production env gate so sentry-memory-rollup runs daily (#2428)

- **SHA**: `0104a8330d49d5980689aa7854145787a52789e9`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-13T12:19:23Z
- **PR**: #2428

### 完整 commit message

```
fix(ci): drop production env gate so sentry-memory-rollup runs daily (#2428)

## What & why

The **Sentry Memory Rollup** scheduled workflow has never actually run.
Both
existing scheduled runs sat in `waiting` for 10h+ and were cancelled.

Root cause: the `rollup` job declared `environment: production`, and
that
environment has a **required-reviewers** protection rule. Every
scheduled run
paused on manual approval before the job could start, so:

- the job never queried Sentry or produced its `should_notify` /
`message` outputs;
- the `notify` job (`if: needs.rollup.outputs.should_notify == 'true'`)
never fired;
- **neither** the breach alert **nor** the daily "normal" status was
ever posted
  to the Lark dev group.

## Fix

- Remove `environment: production` from the read-only `rollup` job — no
deployment
  approval should gate a daily monitoring task.
- The job only needs two values from that environment:
- `SENTRY_AUTH_TOKEN` — already a **repo-level** secret, so unaffected.
- `SENTRY_DSN` — was **production-env-only**. It is a public client DSN
(the
ingest-endpoint form that's safe to embed client-side), so it has been
promoted to a **repo-level variable**; `vars.SENTRY_DSN` now resolves
without
the environment. The production-env copy is left in place for the deploy
jobs.

The `notify` job is unchanged — it never declared an environment and
already runs
at repo scope.

## Validation

Dispatched on this branch with `dry_run=true` (no Lark post, no
synthetic Sentry
issues) to confirm the approval gate is gone and the job runs to
completion.

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR body

## What & why

The **Sentry Memory Rollup** scheduled workflow has never actually run. Both
existing scheduled runs sat in `waiting` for 10h+ and were cancelled.

Root cause: the `rollup` job declared `environment: production`, and that
environment has a **required-reviewers** protection rule. Every scheduled run
paused on manual approval before the job could start, so:

- the job never queried Sentry or produced its `should_notify` / `message` outputs;
- the `notify` job (`if: needs.rollup.outputs.should_notify == 'true'`) never fired;
- **neither** the breach alert **nor** the daily "normal" status was ever posted
  to the Lark dev group.

## Fix

- Remove `environment: production` from the read-only `rollup` job — no deployment
  approval should gate a daily monitoring task.
- The job only needs two values from that environment:
  - `SENTRY_AUTH_TOKEN` — already a **repo-level** secret, so unaffected.
  - `SENTRY_DSN` — was **production-env-only**. It is a public client DSN (the
    ingest-endpoint form that's safe to embed client-side), so it has been
    promoted to a **repo-level variable**; `vars.SENTRY_DSN` now resolves without
    the environment. The production-env copy is left in place for the deploy jobs.

The `notify` job is unchanged — it never declared an environment and already runs
at repo scope.

## Validation

Dispatched on this branch with `dry_run=true` (no Lark post, no synthetic Sentry
issues) to confirm the approval gate is gone and the job runs to completion.


---

## fix(ci): auto-tag-service watches Code Quality Check, not a nonexistent workflow (#2427)

- **SHA**: `79bf2c7a7ccff3c41b849c482ecd4429e54088fb`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-13T11:55:26Z
- **PR**: #2427

### 完整 commit message

```
fix(ci): auto-tag-service watches Code Quality Check, not a nonexistent workflow (#2427)

## What
`auto-tag-service.yaml`'s beta job had `workflow_run.workflows: ["Python
Code Quality"]`, but **no workflow by that name exists**. The
Python/service checks (ruff/pyright/pytest) run as the
`claw-interface-quality` job *inside* the `Code Quality Check` workflow
(`code-quality.yml`, calling `python-code-quality-v3.yml`). So the
trigger matched nothing and `service-v*-beta` tags were never
auto-created.

**Verified against live data:** `auto-tag-service.yaml` has had zero
`workflow_run`-triggered runs (all its runs are `pull_request`/skipped),
and the existing `service-v0.8.2-beta.1` was created manually
(chris-srp, 2026-06-10), not by the workflow.

**Fix:** repoint the trigger to `Code Quality Check` (same workflow
`auto-tag-frontend.yaml` already watches). YAML validated.

## Related issue found (not fixed here — needs a decision)
Neither `auto-tag-frontend` nor `auto-tag-service` guards on **which
surface changed**:
- Both `workflow_run` beta jobs fire on any `claude/**` `Code Quality
Check` success.
- Both `create-release-tag` jobs fire on any `claude/` PR merge (`merged
&& head.ref startsWith 'claude/'`), with no path filter.

So a `claude/` PR touching only `web/**` would create **both**
`ecap-v*-release` and `service-v*-release` → a spurious backend
**production** deploy (and vice-versa). It's mitigated by the production
approval gate (a human must approve each deploy) and rare in practice
(`claude/**` branches are seldom used), so this PR only fixes the dead
trigger and **documents** the gap in `release.md`. If you want, I can
follow up by adding a `web/**` / `services/claw-interface/**`
changed-paths guard to all four jobs so each tag only fires for its own
surface.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR body

## What
`auto-tag-service.yaml`'s beta job had `workflow_run.workflows: ["Python Code Quality"]`, but **no workflow by that name exists**. The Python/service checks (ruff/pyright/pytest) run as the `claw-interface-quality` job *inside* the `Code Quality Check` workflow (`code-quality.yml`, calling `python-code-quality-v3.yml`). So the trigger matched nothing and `service-v*-beta` tags were never auto-created.

**Verified against live data:** `auto-tag-service.yaml` has had zero `workflow_run`-triggered runs (all its runs are `pull_request`/skipped), and the existing `service-v0.8.2-beta.1` was created manually (chris-srp, 2026-06-10), not by the workflow.

**Fix:** repoint the trigger to `Code Quality Check` (same workflow `auto-tag-frontend.yaml` already watches). YAML validated.

## Related issue found (not fixed here — needs a decision)
Neither `auto-tag-frontend` nor `auto-tag-service` guards on **which surface changed**:
- Both `workflow_run` beta jobs fire on any `claude/**` `Code Quality Check` success.
- Both `create-release-tag` jobs fire on any `claude/` PR merge (`merged && head.ref startsWith 'claude/'`), with no path filter.

So a `claude/` PR touching only `web/**` would create **both** `ecap-v*-release` and `service-v*-release` → a spurious backend **production** deploy (and vice-versa). It's mitigated by the production approval gate (a human must approve each deploy) and rare in practice (`claude/**` branches are seldom used), so this PR only fixes the dead trigger and **documents** the gap in `release.md`. If you want, I can follow up by adding a `web/**` / `services/claw-interface/**` changed-paths guard to all four jobs so each tag only fires for its own surface.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## docs(web): drop the 'don't run tests unless requested' principle (#2426)

- **SHA**: `6cb14a728995b7c25d829c1fa5ac436b6182dd58`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-13T11:35:20Z
- **PR**: #2426

### 完整 commit message

```
docs(web): drop the 'don't run tests unless requested' principle (#2426)

Removes the `web/app/AGENTS.md` Working-Principles line *"Do NOT run
tests, lint, or builds unless explicitly requested"* at the maintainer's
request.

Rationale: the workspace now ships first-class local-verification
tooling (`scripts/verify-web.sh`, the `/verify-local` skill), so the
default-no-verification stance conflicted with encouraging local checks
before push.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR body

Removes the `web/app/AGENTS.md` Working-Principles line *"Do NOT run tests, lint, or builds unless explicitly requested"* at the maintainer's request.

Rationale: the workspace now ships first-class local-verification tooling (`scripts/verify-web.sh`, the `/verify-local` skill), so the default-no-verification stance conflicted with encouraging local checks before push.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## chore(harness): add local-verification scripts, mock SSE, and ecap-specific skills (#2424)

- **SHA**: `174ba0fc93f5de88158b56ff613c6a910414896b`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-13T10:37:15Z
- **PR**: #2424

### 完整 commit message

```
chore(harness): add local-verification scripts, mock SSE, and ecap-specific skills (#2424)

## What & why

Implements the harness-optimization plan distilled from 3 days
(6/10–6/13) of Claude Code sessions on this repo. Plan file:
`docs/superpowers/plans/2026-06-13-claude-harness-optimization.md`.
Tracking:
[ECA-989](https://linear.app/srpone/issue/ECA-989/优化-ecap-workspace-的-claude-code-开发-harness本地验证-ci-等待原语-文档固化).

Targets the four recurring friction classes the session analysis
surfaced: local-verification setup, missing CI-wait primitives, monorepo
cwd/path errors, and knowledge that lived only in personal memory
instead of repo docs.

## Changes

**Scripts (`scripts/`, all shellcheck-clean, help-tested):**
- `verify-web.sh` — runs the web/app suite (`tsc` → `vitest` → `eslint`)
with the correct cwd + runner prefix; clears stale `.next/types`. Scope
to files with args.
- `dev-mock.sh` — one command for `mock-backend.mjs` + `next dev`;
prints the **actual** dev URL (next shifts off `:3000` when taken).
- `watch-pr-checks.sh` — polls PR checks to a real verdict; absorbs `gh
pr checks` pending exit-code 8 and the pending `bucket` shape.
- `prod-version.sh` — reports deployed staging/prod versions from
`/api/version` + tags + recent runs (verified live: prod is
`ecap-v0.8.8-release`).
- `check-control-plane.sh` — probes public surfaces (frontend
`/api/version`, Mattermost ping) to tell "bot silent" from "control
plane down".
- `cdp/lib.mjs` + `cdp/README.md` — reusable CDP verification helpers,
sinking the one-off `/tmp/cdp-*.mjs` pattern.
- `hooks/guard-screenshot-path.sh` — PreToolUse guard enforcing the
`.screenshots/` convention (tested: 4 cases).

**mock-backend (`web/app/scripts/mock-backend.mjs`):**
- Streaming SSE chat: `POST /session/chat` with `streaming:true` returns
`job_started` → partial frames → final → `[DONE]`; added
`/session/chat/subscribe` resume. Unblocks local chat-flow verification
(the gap that forced F16/F19 to stay frozen).
- `MOCK_USER_STATE=onboarding_required` persona (bot not ready, 0
credits, invite gate on, onboarding incomplete) — exercises the new-user
flow that previously couldn't be run locally.
- `/users/credits` now returns the real `UserCreditsInfo` `wallets[]`
shape (was a flat shape with no `wallets`, which the credits UI reads —
a genuine drift). Shape sourced from a shared fixture
`tests/fixtures/backend-shapes.mjs`, guarded by a unit test so
mock↔production can't silently diverge again.

**Skills (`.claude/commands/`):** new `/verify-local`, `/prod-validate`,
`/watch-ci`; full rewrite of `/release` from generic semver boilerplate
to the real three-namespace (`ecap-v*` / `service-v*` / `ios-v*`) +
auto-tag + production approval-gate flow.

**Docs:** `AGENTS.md` (toolchain invariant, gh gotchas incl.
PR-body-via-file, concurrent-session worktree rule,
investigate-before-implement); `architecture.md` (JuiceFS per-botID +
S3-gateway storage section); the plan file.

## Verification done locally
- `verify-web.sh --tsc-only` ✓; full unit suite ✓ (514 files, 7238 tests
pass); lint clean on changed `web/**` files.
- mock booted; SSE frames, `wallets[]`, and onboarding persona all
verified via curl.
- `shellcheck` clean on all new scripts; all `--help` smoke-tested;
`prod-version.sh` / `check-control-plane.sh` verified against live
endpoints (read-only).

## Follow-ups (not in this PR)
- **`.claude/settings.json` could not be edited by the agent**
(auto-mode classifier blocks self-modification of hooks/permissions).
Two manual steps remain: (1) wire the screenshot hook — exact JSON in
`scripts/hooks/README.md`; (2) widen the Bash allowlist via
`/fewer-permission-prompts`.
- Playwright MCP allowed-roots can't be set at repo level (no
`.mcp.json`; MCP comes from a plugin) — the hook is the repo-side lever;
any allowed-roots change is an MCP/plugin-config task.
- `zooclaw-extras` CLAUDE.md is a separate repo — deferred there.
- Open question in the plan: whether to request a CF Access read-only
service token to make staging logged-in validation fully local.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR body

## What & why

Implements the harness-optimization plan distilled from 3 days (6/10–6/13) of Claude Code sessions on this repo. Plan file: `docs/superpowers/plans/2026-06-13-claude-harness-optimization.md`. Tracking: [ECA-989](https://linear.app/srpone/issue/ECA-989/优化-ecap-workspace-的-claude-code-开发-harness本地验证-ci-等待原语-文档固化).

Targets the four recurring friction classes the session analysis surfaced: local-verification setup, missing CI-wait primitives, monorepo cwd/path errors, and knowledge that lived only in personal memory instead of repo docs.

## Changes

**Scripts (`scripts/`, all shellcheck-clean, help-tested):**
- `verify-web.sh` — runs the web/app suite (`tsc` → `vitest` → `eslint`) with the correct cwd + runner prefix; clears stale `.next/types`. Scope to files with args.
- `dev-mock.sh` — one command for `mock-backend.mjs` + `next dev`; prints the **actual** dev URL (next shifts off `:3000` when taken).
- `watch-pr-checks.sh` — polls PR checks to a real verdict; absorbs `gh pr checks` pending exit-code 8 and the pending `bucket` shape.
- `prod-version.sh` — reports deployed staging/prod versions from `/api/version` + tags + recent runs (verified live: prod is `ecap-v0.8.8-release`).
- `check-control-plane.sh` — probes public surfaces (frontend `/api/version`, Mattermost ping) to tell "bot silent" from "control plane down".
- `cdp/lib.mjs` + `cdp/README.md` — reusable CDP verification helpers, sinking the one-off `/tmp/cdp-*.mjs` pattern.
- `hooks/guard-screenshot-path.sh` — PreToolUse guard enforcing the `.screenshots/` convention (tested: 4 cases).

**mock-backend (`web/app/scripts/mock-backend.mjs`):**
- Streaming SSE chat: `POST /session/chat` with `streaming:true` returns `job_started` → partial frames → final → `[DONE]`; added `/session/chat/subscribe` resume. Unblocks local chat-flow verification (the gap that forced F16/F19 to stay frozen).
- `MOCK_USER_STATE=onboarding_required` persona (bot not ready, 0 credits, invite gate on, onboarding incomplete) — exercises the new-user flow that previously couldn't be run locally.
- `/users/credits` now returns the real `UserCreditsInfo` `wallets[]` shape (was a flat shape with no `wallets`, which the credits UI reads — a genuine drift). Shape sourced from a shared fixture `tests/fixtures/backend-shapes.mjs`, guarded by a unit test so mock↔production can't silently diverge again.

**Skills (`.claude/commands/`):** new `/verify-local`, `/prod-validate`, `/watch-ci`; full rewrite of `/release` from generic semver boilerplate to the real three-namespace (`ecap-v*` / `service-v*` / `ios-v*`) + auto-tag + production approval-gate flow.

**Docs:** `AGENTS.md` (toolchain invariant, gh gotchas incl. PR-body-via-file, concurrent-session worktree rule, investigate-before-implement); `architecture.md` (JuiceFS per-botID + S3-gateway storage section); the plan file.

## Verification done locally
- `verify-web.sh --tsc-only` ✓; full unit suite ✓ (514 files, 7238 tests pass); lint clean on changed `web/**` files.
- mock booted; SSE frames, `wallets[]`, and onboarding persona all verified via curl.
- `shellcheck` clean on all new scripts; all `--help` smoke-tested; `prod-version.sh` / `check-control-plane.sh` verified against live endpoints (read-only).

## Follow-ups (not in this PR)
- **`.claude/settings.json` could not be edited by the agent** (auto-mode classifier blocks self-modification of hooks/permissions). Two manual steps remain: (1) wire the screenshot hook — exact JSON in `scripts/hooks/README.md`; (2) widen the Bash allowlist via `/fewer-permission-prompts`.
- Playwright MCP allowed-roots can't be set at repo level (no `.mcp.json`; MCP comes from a plugin) — the hook is the repo-side lever; any allowed-roots change is an MCP/plugin-config task.
- `zooclaw-extras` CLAUDE.md is a separate repo — deferred there.
- Open question in the plan: whether to request a CF Access read-only service token to make staging logged-in validation fully local.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
