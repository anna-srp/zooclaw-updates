# ecap-workspace — commits 2026-06-09

## chore(dev): add Chrome CDP debug profile launcher (#2318)

- **SHA**: `c7cad481d429d56af36a2dfb2a782f982132d7af`
- **作者**: chris-srp
- **日期**: 2026-06-09T17:34:59Z
- **PR**: #2318
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/c7cad481d429d56af36a2dfb2a782f982132d7af

### 完整 commit message

```
chore(dev): add Chrome CDP debug profile launcher (#2318)

## Summary
- Add `scripts/open-chrome-debug-profile.sh` for launching Chrome with a
dedicated user data dir and local CDP endpoint.
- Document the script in `scripts/README.md`.

## Notes
- The script binds CDP to `127.0.0.1` by default.
- Defaults to staging `/chat`, but URL, profile dir, port, address, and
Chrome binary can be overridden with flags or environment variables.
- The first run prompts the user to sign in with their own staging
account in the opened Chrome profile.

## Validation
- `scripts/open-chrome-debug-profile.sh --help`
- `scripts/open-chrome-debug-profile.sh --unknown-option` exits with
code 2 and usage text
- `shellcheck scripts/open-chrome-debug-profile.sh`
```

### 完整 PR body

## Summary
- Add `scripts/open-chrome-debug-profile.sh` for launching Chrome with a dedicated user data dir and local CDP endpoint.
- Document the script in `scripts/README.md`.

## Notes
- The script binds CDP to `127.0.0.1` by default.
- Defaults to staging `/chat`, but URL, profile dir, port, address, and Chrome binary can be overridden with flags or environment variables.
- The first run prompts the user to sign in with their own staging account in the opened Chrome profile.

## Validation
- `scripts/open-chrome-debug-profile.sh --help`
- `scripts/open-chrome-debug-profile.sh --unknown-option` exits with code 2 and usage text
- `shellcheck scripts/open-chrome-debug-profile.sh`

---

## fix(web): address refactor validation follow-ups (#2317)

- **SHA**: `9a85759eb4f5fc7cd74ea51a894b44ad444cdae1`
- **作者**: chris-srp
- **日期**: 2026-06-09T17:07:48Z
- **PR**: #2317
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/9a85759eb4f5fc7cd74ea51a894b44ad444cdae1

### 完整 commit message

```
fix(web): address refactor validation follow-ups (#2317)

## Summary
- Add visible Add Job entry points for the schedule empty state and All
Jobs header.
- Activate the shared OpenClaw provider on `/assets` so the connection
pill reflects live Claw status instead of staying disconnected while
uploads render.
- Add focused unit coverage and a local validation report for the two
follow-up fixes.

## Root Cause
- `/schedule` already had a create handler, but no visible empty-state
control invoked it.
- `/assets` rendered the shared Claw header while only reading passive
OpenClaw context, so the provider was never activated on the default
uploads view.

## Validation
- `pnpm exec vitest run --config ./vitest.config.mts
tests/unit/app/assets/AssetsClient.unit.spec.tsx
tests/unit/components/ClawPageHeader.unit.spec.ts
tests/unit/app/schedule/cron-client.unit.spec.tsx`
- `pnpm run lint`
- `pnpm exec tsc --noEmit --project app/tsconfig.json`
- `env NODE_OPTIONS="--no-deprecation --no-experimental-webstorage" pnpm
exec vitest run --config ./vitest.config.mts`
- Browser CDP against local `pnpm dev:staging`: `/assets` shows `Claw
Connected`; `/schedule` empty state Add Job opens the New Job form
without submitting a job.

## PR Structure
Stacked on #2316 (`fix/new-chat-session-status`) so this PR only
contains the report follow-up fixes. After #2316 merges, this PR can be
retargeted to `main`.
```

### 完整 PR body

## Summary
- Add visible Add Job entry points for the schedule empty state and All Jobs header.
- Activate the shared OpenClaw provider on `/assets` so the connection pill reflects live Claw status instead of staying disconnected while uploads render.
- Add focused unit coverage and a local validation report for the two follow-up fixes.

## Root Cause
- `/schedule` already had a create handler, but no visible empty-state control invoked it.
- `/assets` rendered the shared Claw header while only reading passive OpenClaw context, so the provider was never activated on the default uploads view.

## Validation
- `pnpm exec vitest run --config ./vitest.config.mts tests/unit/app/assets/AssetsClient.unit.spec.tsx tests/unit/components/ClawPageHeader.unit.spec.ts tests/unit/app/schedule/cron-client.unit.spec.tsx`
- `pnpm run lint`
- `pnpm exec tsc --noEmit --project app/tsconfig.json`
- `env NODE_OPTIONS="--no-deprecation --no-experimental-webstorage" pnpm exec vitest run --config ./vitest.config.mts`
- Browser CDP against local `pnpm dev:staging`: `/assets` shows `Claw Connected`; `/schedule` empty state Add Job opens the New Job form without submitting a job.

## PR Structure
Stacked on #2316 (`fix/new-chat-session-status`) so this PR only contains the report follow-up fixes. After #2316 merges, this PR can be retargeted to `main`.

---

## fix(web): show connected status on session threads (#2316)

- **SHA**: `e20041530533435350bee4bcc6d1ce46be65122b`
- **作者**: chris-srp
- **日期**: 2026-06-09T16:59:43Z
- **PR**: #2316
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/e20041530533435350bee4bcc6d1ce46be65122b

### 完整 commit message

```
fix(web): show connected status on session threads (#2316)

## Summary
- Fix the `/new-chat` session-thread header status so it uses the
route-scoped computer id before the OpenClaw provider snapshot hydrates.
- Pass a small explicit connection status source through
`SessionThreadClient -> ChatHeader -> ClawPageHeader ->
ClawConnectionStatus`.
- Add local staging validation reports for `/chat`, refactor-impact
routes, and the `/new-chat` status fix.

## Root cause
Session-thread routes already know the correct `computerId` from the URL
and can send replies through the Mattermost token, but the shared header
status pill only derived its computer id from `OpenClawContext.oc.bot`.
On session-thread pages that provider snapshot can be missing or late,
so the status pill had no computer id, never polled
`/api/openclaw/computers/:computerId/status`, and fell back to
`Disconnected` even though the thread and send path worked.

## Test plan
- [x] `pnpm exec vitest run --config ./vitest.config.mts
tests/unit/components/ClawPageHeader-extras.unit.spec.tsx
tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx`
- [x] `pnpm run lint`
- [x] `pnpm exec tsc --noEmit --project app/tsconfig.json`
- [x] `env NODE_OPTIONS='--no-deprecation --no-experimental-webstorage'
pnpm exec vitest run --config ./vitest.config.mts`
- [x] Local `pnpm dev:staging` with Chrome CDP: same session-thread
route changed from `Disconnected` to `Claw Connected`; composer visible;
thread not loading/not-found.

Reports:
-
`docs/staging-validation/2026-06-10-chat-route-refactor-staging-report.md`
-
`docs/staging-validation/2026-06-10-web-app-refactor-impact-staging-report.md`
-
`docs/staging-validation/2026-06-10-new-chat-status-fix-local-report.md`
```

### 完整 PR body

## Summary
- Fix the `/new-chat` session-thread header status so it uses the route-scoped computer id before the OpenClaw provider snapshot hydrates.
- Pass a small explicit connection status source through `SessionThreadClient -> ChatHeader -> ClawPageHeader -> ClawConnectionStatus`.
- Add local staging validation reports for `/chat`, refactor-impact routes, and the `/new-chat` status fix.

## Root cause
Session-thread routes already know the correct `computerId` from the URL and can send replies through the Mattermost token, but the shared header status pill only derived its computer id from `OpenClawContext.oc.bot`. On session-thread pages that provider snapshot can be missing or late, so the status pill had no computer id, never polled `/api/openclaw/computers/:computerId/status`, and fell back to `Disconnected` even though the thread and send path worked.

## Test plan
- [x] `pnpm exec vitest run --config ./vitest.config.mts tests/unit/components/ClawPageHeader-extras.unit.spec.tsx tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx`
- [x] `pnpm run lint`
- [x] `pnpm exec tsc --noEmit --project app/tsconfig.json`
- [x] `env NODE_OPTIONS='--no-deprecation --no-experimental-webstorage' pnpm exec vitest run --config ./vitest.config.mts`
- [x] Local `pnpm dev:staging` with Chrome CDP: same session-thread route changed from `Disconnected` to `Claw Connected`; composer visible; thread not loading/not-found.

Reports:
- `docs/staging-validation/2026-06-10-chat-route-refactor-staging-report.md`
- `docs/staging-validation/2026-06-10-web-app-refactor-impact-staging-report.md`
- `docs/staging-validation/2026-06-10-new-chat-status-fix-local-report.md`

---

## chore: add /dev-staging command for local→staging frontend setup (#2313)

- **SHA**: `7a39a67a43739a128c643ecbefa4f6442896d4d1`
- **作者**: chris-srp
- **日期**: 2026-06-09T14:19:11Z
- **PR**: #2313
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/7a39a67a43739a128c643ecbefa4f6442896d4d1

### 完整 commit message

```
chore: add /dev-staging command for local→staging frontend setup (#2313)

## What

Adds `/dev-staging`, a project slash command (sibling to `/telep`) that
sets up the local `web/app` frontend to run against **staging**.

## How

- Pulls the public config from the GitHub `staging` environment
**Variables** (`gh api .../environments/staging/variables`) and writes
`web/app/.env.staging.local`. Pulling the *full* set avoids the
missing-var → prod-fallback trap (e.g. `NEXT_PUBLIC_MATTERMOST_URL`
silently defaulting to `mattermost.zooclaw.ai`).
- On re-run, preserves hand-filled secret values; lists the secrets that
must be supplied manually (CF Access, LiteLLM key, R2 secret).
- Documents known gotchas: `/tips/*` 404 on staging (not a bug — served
by the sibling `zooclaw-tips` worker on the prod zone only),
account-service CORS, the CF Access boundary, and the `NEXT_PUBLIC_*`
restart requirement.

`web/app/.env.staging.local` stays gitignored (`.env*.local`).

## Notes

- Pure tooling: only adds `.claude/commands/dev-staging.md`. No
app/runtime code touched.
- The `dev:staging` / `dev:staging:turbo` scripts it relies on already
landed in `5831b7a2e`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>
```

### 完整 PR body

## What

Adds `/dev-staging`, a project slash command (sibling to `/telep`) that sets up the local `web/app` frontend to run against **staging**.

## How

- Pulls the public config from the GitHub `staging` environment **Variables** (`gh api .../environments/staging/variables`) and writes `web/app/.env.staging.local`. Pulling the *full* set avoids the missing-var → prod-fallback trap (e.g. `NEXT_PUBLIC_MATTERMOST_URL` silently defaulting to `mattermost.zooclaw.ai`).
- On re-run, preserves hand-filled secret values; lists the secrets that must be supplied manually (CF Access, LiteLLM key, R2 secret).
- Documents known gotchas: `/tips/*` 404 on staging (not a bug — served by the sibling `zooclaw-tips` worker on the prod zone only), account-service CORS, the CF Access boundary, and the `NEXT_PUBLIC_*` restart requirement.

`web/app/.env.staging.local` stays gitignored (`.env*.local`).

## Notes

- Pure tooling: only adds `.claude/commands/dev-staging.md`. No app/runtime code touched.
- The `dev:staging` / `dev:staging:turbo` scripts it relies on already landed in `5831b7a2e`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(web): gate email login behind URL parameter (#2308)

- **SHA**: `2b5ff6eeb3febf4aa07f1a0a64fe583a8b9b16f4`
- **作者**: tim-srp
- **日期**: 2026-06-09T14:17:57Z
- **PR**: #2308
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/2b5ff6eeb3febf4aa07f1a0a64fe583a8b9b16f4

### 完整 commit message

```
fix(web): gate email login behind URL parameter (#2308)

## Summary
- Hide the email login option by default in the login modal.
- Show the email login option only when the current URL includes
`email_login=1`.
- Add component coverage for the default-hidden and parameter-enabled
states.

## Test Plan
- [x] `corepack pnpm exec vitest run --config ./vitest.config.mts
tests/unit/components/LoginForm.unit.spec.tsx
tests/unit/components/LoginModal.unit.spec.tsx` from `web/app`
- [x] `corepack pnpm exec eslint src/components/LoginForm.tsx
src/components/LoginModal.tsx
tests/unit/components/LoginForm.unit.spec.tsx
tests/unit/components/LoginModal.unit.spec.tsx --quiet` from `web/app`
```

### 完整 PR body

## Summary
- Hide the email login option by default in the login modal.
- Show the email login option only when the current URL includes `email_login=1`.
- Add component coverage for the default-hidden and parameter-enabled states.

## Test Plan
- [x] `corepack pnpm exec vitest run --config ./vitest.config.mts tests/unit/components/LoginForm.unit.spec.tsx tests/unit/components/LoginModal.unit.spec.tsx` from `web/app`
- [x] `corepack pnpm exec eslint src/components/LoginForm.tsx src/components/LoginModal.tsx tests/unit/components/LoginForm.unit.spec.tsx tests/unit/components/LoginModal.unit.spec.tsx --quiet` from `web/app`

---

## fix(org): persist team wallet ids (#2309)

- **SHA**: `5c91acc3dfc5bf720822c2889ecb312ea5a1da63`
- **作者**: bill-srp
- **日期**: 2026-06-09T13:44:36Z
- **PR**: #2309
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/5c91acc3dfc5bf720822c2889ecb312ea5a1da63

### 完整 commit message

```
fix(org): persist team wallet ids (#2309)

## Summary
- Persist optional org wallet ids on the Org schema.
- During team org creation, subscribe the billing team and create or
reuse subscription/topup wallets.
- Store the wallet ids on the Org without granting initial credits.

## Root cause
Team org creation provisioned billing team state but did not persist the
team wallet ids on the org document. The previous flow also coupled
wallet creation to an initial credits grant.

## Test plan
- [x] source /Users/bill/.venvs/claw-interface/bin/activate && ruff
format --check .
- [x] source /Users/bill/.venvs/claw-interface/bin/activate && ruff
check .
- [x] source /Users/bill/.venvs/claw-interface/bin/activate && pyright
app tests
- [x] source /Users/bill/.venvs/claw-interface/bin/activate && python -m
pytest tests/unit/test_org_service.py tests/unit/test_schema_org.py
tests/unit/test_routes_org.py -q
```

### 完整 PR body

## Summary
- Persist optional org wallet ids on the Org schema.
- During team org creation, subscribe the billing team and create or reuse subscription/topup wallets.
- Store the wallet ids on the Org without granting initial credits.

## Root cause
Team org creation provisioned billing team state but did not persist the team wallet ids on the org document. The previous flow also coupled wallet creation to an initial credits grant.

## Test plan
- [x] source /Users/bill/.venvs/claw-interface/bin/activate && ruff format --check .
- [x] source /Users/bill/.venvs/claw-interface/bin/activate && ruff check .
- [x] source /Users/bill/.venvs/claw-interface/bin/activate && pyright app tests
- [x] source /Users/bill/.venvs/claw-interface/bin/activate && python -m pytest tests/unit/test_org_service.py tests/unit/test_schema_org.py tests/unit/test_routes_org.py -q

---

## feat(desktop-node): node.* command namespace + agent operator pairing self-heal (#2296)

- **SHA**: `4efb44d10b2c10ed6f28bcd5c262291695c3bbc4`
- **作者**: zayne-srp
- **日期**: 2026-06-09T13:42:22Z
- **PR**: #2296
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/4efb44d10b2c10ed6f28bcd5c262291695c3bbc4

### 完整 commit message

```
feat(desktop-node): node.* command namespace + agent operator pairing self-heal (#2296)

Linear: https://linear.app/srpone/issue/ECA-879

Combines two desktop-node changes (previously split as #2287 + #2296)
into one PR per request.

## 1. Namespace desktop node commands under `node.*`
The desktop node's commands used to collide with OpenClaw's built-in
**file-transfer** commands (`dir.list` / `file.*`), which routed them
through the file-transfer plugin's `allowReadPaths` policy. Rename all
desktop node commands to a dedicated `node.*` namespace:

`node.fs.list` / `node.fs.read` / `node.fs.write` / `node.fs.edit` /
`node.fs.glob` / `node.fs.grep` / `node.shell.exec` /
`node.capabilities` (drop `dir.list`).

Now pure custom node commands: gated only by
`gateway.nodes.allowCommands`, never the file-transfer plugin, invoked
by the bot via the generic `node.invoke`. Command names are validated as
`NonEmptyString` (no dot-count limit; OpenClaw itself uses two-dot
commands like `system.run.prepare`). No backward-compat aliases — this
protocol isn't live in production and lands coordinated with the
gateway-side `allowCommands` switch (already updated in gcp-foundation).

## 2. Self-heal the bot agent operator pairing
For the bot to `node.invoke`, its **own agent operator connection** must
carry `operator.write`. That pairing can be lost across a bot pod
restart and sit pending re-approval — and until re-approved every invoke
fails with `missing scope: operator.write`, even though the node is
paired and online (the exact cause of a "worked, then broke" staging
regression).

Extend the desktop-node approve flow to best-effort re-approve the
agent's own operator pairing in-process (same Control-UI `runtime_exec`
path), **strictly scoped** — only a device that is `isRepair` (re-pair
of a previously-trusted device) + operator-only roles +
`operator.*`-only scopes + cli client shape; refuses to act if more than
one candidate matches (never mass-approves); failures surface as
`ok:false`. Node approval is unaffected if the heal step errors.

> Durable fix for #2 still belongs in fastclaw (persist the bot pod's
device-pairing state across restarts). This is the claw-interface safety
net.

## Test plan
- [x] `ruff` + `ruff format` clean, `lint-imports` (8/8 incl. C3) pass.
- [x] Desktop `tsc --noEmit` passes.
- [x] claw-interface unit tests (node approve, agent-operator-repair
parse, best-effort parse) pass.
- [ ] Staging: fresh pairing registers the `node.*` commands; bot
invokes them; confirm whether the operator-pairing heal fires at the
right time (operator pending may only appear once the agent attempts an
invoke — to validate on staging).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>
```

### 完整 PR body

Linear: https://linear.app/srpone/issue/ECA-879

Combines two desktop-node changes (previously split as #2287 + #2296) into one PR per request.

## 1. Namespace desktop node commands under `node.*`
The desktop node's commands used to collide with OpenClaw's built-in **file-transfer** commands (`dir.list` / `file.*`), which routed them through the file-transfer plugin's `allowReadPaths` policy. Rename all desktop node commands to a dedicated `node.*` namespace:

`node.fs.list` / `node.fs.read` / `node.fs.write` / `node.fs.edit` / `node.fs.glob` / `node.fs.grep` / `node.shell.exec` / `node.capabilities` (drop `dir.list`).

Now pure custom node commands: gated only by `gateway.nodes.allowCommands`, never the file-transfer plugin, invoked by the bot via the generic `node.invoke`. Command names are validated as `NonEmptyString` (no dot-count limit; OpenClaw itself uses two-dot commands like `system.run.prepare`). No backward-compat aliases — this protocol isn't live in production and lands coordinated with the gateway-side `allowCommands` switch (already updated in gcp-foundation).

## 2. Self-heal the bot agent operator pairing
For the bot to `node.invoke`, its **own agent operator connection** must carry `operator.write`. That pairing can be lost across a bot pod restart and sit pending re-approval — and until re-approved every invoke fails with `missing scope: operator.write`, even though the node is paired and online (the exact cause of a "worked, then broke" staging regression).

Extend the desktop-node approve flow to best-effort re-approve the agent's own operator pairing in-process (same Control-UI `runtime_exec` path), **strictly scoped** — only a device that is `isRepair` (re-pair of a previously-trusted device) + operator-only roles + `operator.*`-only scopes + cli client shape; refuses to act if more than one candidate matches (never mass-approves); failures surface as `ok:false`. Node approval is unaffected if the heal step errors.

> Durable fix for #2 still belongs in fastclaw (persist the bot pod's device-pairing state across restarts). This is the claw-interface safety net.

## Test plan
- [x] `ruff` + `ruff format` clean, `lint-imports` (8/8 incl. C3) pass.
- [x] Desktop `tsc --noEmit` passes.
- [x] claw-interface unit tests (node approve, agent-operator-repair parse, best-effort parse) pass.
- [ ] Staging: fresh pairing registers the `node.*` commands; bot invokes them; confirm whether the operator-pairing heal fires at the right time (operator pending may only appear once the agent attempts an invoke — to validate on staging).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## chore(web): add dev:staging scripts and enable sentry-cli plugin (#2311)

- **SHA**: `77a2fb6535444b490c919a1c9e11b3dc6e3b89ec`
- **作者**: chris-srp
- **日期**: 2026-06-09T13:25:09Z
- **PR**: #2311
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/77a2fb6535444b490c919a1c9e11b3dc6e3b89ec

### 完整 commit message

```
chore(web): add dev:staging scripts and enable sentry-cli plugin (#2311)

## What

- Add `dev:staging` / `dev:staging:turbo` npm scripts in
`web/app/package.json` that run `next dev` against `.env.staging.local`,
so the local web app can be pointed at the staging backend without
editing `.env.local`.
- Enable the `sentry-cli@claude-plugins-official` Claude Code plugin in
shared `.claude/settings.json`.

## Why

Running the local frontend against staging previously required
hand-editing `.env.local`. A dedicated `.env.staging.local` + script
keeps the two environments cleanly separated.

## Notes

These are tooling/DX changes only — no product code, no runtime behavior
change.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### 完整 PR body

## What

- Add `dev:staging` / `dev:staging:turbo` npm scripts in `web/app/package.json` that run `next dev` against `.env.staging.local`, so the local web app can be pointed at the staging backend without editing `.env.local`.
- Enable the `sentry-cli@claude-plugins-official` Claude Code plugin in shared `.claude/settings.json`.

## Why

Running the local frontend against staging previously required hand-editing `.env.local`. A dedicated `.env.staging.local` + script keeps the two environments cleanly separated.

## Notes

These are tooling/DX changes only — no product code, no runtime behavior change.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(web): prevent onboarding progress sync loop (#2310)

- **SHA**: `c7dc718b4707f37a02b06015c9e132648266c6ed`
- **作者**: chris-srp
- **日期**: 2026-06-09T13:01:56Z
- **PR**: #2310
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/c7dc718b4707f37a02b06015c9e132648266c6ed

### 完整 commit message

```
fix(web): prevent onboarding progress sync loop (#2310)

## Summary
- Prevent hidden onboarding steps from oscillating between resolver
output and local auto-skip state.
- Skip redundant progress state/localStorage writes when resolved
progress is unchanged.
- Add a regression test for the repeated equal-progress sync loop.

## Root cause
`OnboardingProvider` synced `resolution.progress` directly into
`progress` even when the resolver returned a fresh object with the same
visible onboarding state. Hidden-step auto-skip then rewrote
`reminder/channel` completion into `localProgress`, which caused the
resolver to produce another fresh progress object and repeat the state
write until React hit maximum update depth.

## Test plan
- [x] `pnpm --dir web/app exec vitest run
tests/unit/components/providers/OnboardingProvider.unit.spec.tsx
--reporter=dot`
- [x] `pnpm --dir web/app exec eslint
src/components/providers/OnboardingProvider.tsx
tests/unit/components/providers/OnboardingProvider.unit.spec.tsx
--quiet`
- [x] `pnpm --dir web/app exec tsc --noEmit --pretty false`
```

### 完整 PR body

## Summary
- Prevent hidden onboarding steps from oscillating between resolver output and local auto-skip state.
- Skip redundant progress state/localStorage writes when resolved progress is unchanged.
- Add a regression test for the repeated equal-progress sync loop.

## Root cause
`OnboardingProvider` synced `resolution.progress` directly into `progress` even when the resolver returned a fresh object with the same visible onboarding state. Hidden-step auto-skip then rewrote `reminder/channel` completion into `localProgress`, which caused the resolver to produce another fresh progress object and repeat the state write until React hit maximum update depth.

## Test plan
- [x] `pnpm --dir web/app exec vitest run tests/unit/components/providers/OnboardingProvider.unit.spec.tsx --reporter=dot`
- [x] `pnpm --dir web/app exec eslint src/components/providers/OnboardingProvider.tsx tests/unit/components/providers/OnboardingProvider.unit.spec.tsx --quiet`
- [x] `pnpm --dir web/app exec tsc --noEmit --pretty false`

---

## refactor(web): convert LoginCheck to store + bootstrap + modal host, drop LoginCheckProvider (#2305)

- **SHA**: `6c62eb2033c794eee0fded8067812265f4731e3b`
- **作者**: chris-srp
- **日期**: 2026-06-09T12:18:58Z
- **PR**: #2305
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/6c62eb2033c794eee0fded8067812265f4731e3b

### 完整 commit message

```
refactor(web): convert LoginCheck to store + bootstrap + modal host, drop LoginCheckProvider (#2305)

## What

Final "UI-state provider → Zustand" pass — the **most intricate**
(modal-state reducer + 3 router/auth watch-effects + an `onLoginSuccess`
registry + the modal render). Flattens the global tree **6 → 5**
(completes 9 → 5).

- **New `lib/login-check-store.ts`** — vanilla store. The `modalReducer`
(issue #2196, with the 3 pathname subtleties) moves **verbatim**;
`dispatch = setState(s => modalReducer(s, action))`. Holds the
`onLoginSuccess` subscriber Set + the public actions
(`checkLogin`/`showLoginModal`/`hideLoginModal`). `lastSeenRequest`
seeded from `loginModalStore.getState().tick` so the first show-request
is a no-op (matches the provider's lazy `useReducer` seed). React-free
(passes `check-no-react-in-stores`).
- **New `hooks/useLoginCheckBootstrap.ts`** — the 3 watch effects
(pathname → navigated, auth snapshot → auth-changed, show-request tick →
show-requested) + `initLoginCheck`, **effect order preserved**. Called
once in ClientLayout.
- **New `lib/useLoginCheck.ts`** — returns a stable module action
object. The **15 consumers** are unchanged in shape (import path
codemodded to `@/lib/useLoginCheck`).
- **New `components/LoginModalHost.tsx`** — renders `LoginModal` from
`store.open`, in `GlobalOverlays` (LoginCheck is global — public pages
use it too).
- `LoginCheckProvider` deleted; ClientLayout drops the wrapper + calls
the bootstrap.

## Why it's safe

LoginCheck **stays global** (bootstrap in ClientLayout mounts once,
matching the provider's lifetime — no remount concern). The reducer's
subtle invariants (null-pathname hydration, locale-rewrite oscillation,
StrictMode stability, show-request dedup) are preserved verbatim and
still unit-tested directly.

## Tests

- Provider spec → `login-check-store` spec (bootstrap + host harness;
the pure `modalReducer` tests kept, now importing from the store).
- Retargeted **11 stale consumer-spec mocks** from the deleted provider
path to `@/lib/useLoginCheck` — the source codemod left the test mocks
pointing at the old path (same stale-mock-target class Codex flagged on
Feedback; caught here by a full-suite run, not tsc).
- `tsc`, `lint`, `lint:ci` (incl. no-react guard), `dup` green; full
suite passes (1 flaky-under-parallelism file confirmed passing in
isolation).

**Completes the flatten: ClientLayout global providers 9 → 5**
(PersistQueryClient · Language · Theme · BrandTheme · ErrorBoundary).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### 完整 PR body

## What

Final "UI-state provider → Zustand" pass — the **most intricate** (modal-state reducer + 3 router/auth watch-effects + an `onLoginSuccess` registry + the modal render). Flattens the global tree **6 → 5** (completes 9 → 5).

- **New `lib/login-check-store.ts`** — vanilla store. The `modalReducer` (issue #2196, with the 3 pathname subtleties) moves **verbatim**; `dispatch = setState(s => modalReducer(s, action))`. Holds the `onLoginSuccess` subscriber Set + the public actions (`checkLogin`/`showLoginModal`/`hideLoginModal`). `lastSeenRequest` seeded from `loginModalStore.getState().tick` so the first show-request is a no-op (matches the provider's lazy `useReducer` seed). React-free (passes `check-no-react-in-stores`).
- **New `hooks/useLoginCheckBootstrap.ts`** — the 3 watch effects (pathname → navigated, auth snapshot → auth-changed, show-request tick → show-requested) + `initLoginCheck`, **effect order preserved**. Called once in ClientLayout.
- **New `lib/useLoginCheck.ts`** — returns a stable module action object. The **15 consumers** are unchanged in shape (import path codemodded to `@/lib/useLoginCheck`).
- **New `components/LoginModalHost.tsx`** — renders `LoginModal` from `store.open`, in `GlobalOverlays` (LoginCheck is global — public pages use it too).
- `LoginCheckProvider` deleted; ClientLayout drops the wrapper + calls the bootstrap.

## Why it's safe

LoginCheck **stays global** (bootstrap in ClientLayout mounts once, matching the provider's lifetime — no remount concern). The reducer's subtle invariants (null-pathname hydration, locale-rewrite oscillation, StrictMode stability, show-request dedup) are preserved verbatim and still unit-tested directly.

## Tests

- Provider spec → `login-check-store` spec (bootstrap + host harness; the pure `modalReducer` tests kept, now importing from the store).
- Retargeted **11 stale consumer-spec mocks** from the deleted provider path to `@/lib/useLoginCheck` — the source codemod left the test mocks pointing at the old path (same stale-mock-target class Codex flagged on Feedback; caught here by a full-suite run, not tsc).
- `tsc`, `lint`, `lint:ci` (incl. no-react guard), `dup` green; full suite passes (1 flaky-under-parallelism file confirmed passing in isolation).

**Completes the flatten: ClientLayout global providers 9 → 5** (PersistQueryClient · Language · Theme · BrandTheme · ErrorBoundary).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## ci(r2-access-worker): add staging deploy environment (#2307)

- **SHA**: `3d646dbdf6d650031042270f2b5d29eab13174b3`
- **作者**: bill-srp
- **日期**: 2026-06-09T11:35:06Z
- **PR**: #2307
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/3d646dbdf6d650031042270f2b5d29eab13174b3

### 完整 commit message

```
ci(r2-access-worker): add staging deploy environment (#2307)

## Summary
- Add a staging wrangler environment for the R2 access worker.
- Align the deploy workflow with the other deploy workflows: main
deploys staging, release tags deploy production, and manual dispatch can
choose the target environment.

## Root cause
The R2 access worker only had production deployment wiring, so staging
bots could hit a worker configured with the production claw-interface
URL.

## Test plan
- [x] `pnpm --dir services/r2-access-worker test`
- [x] `pnpm --dir services/r2-access-worker exec tsc --noEmit`
- [x] `git diff --check`
```

### 完整 PR body

## Summary
- Add a staging wrangler environment for the R2 access worker.
- Align the deploy workflow with the other deploy workflows: main deploys staging, release tags deploy production, and manual dispatch can choose the target environment.

## Root cause
The R2 access worker only had production deployment wiring, so staging bots could hit a worker configured with the production claw-interface URL.

## Test plan
- [x] `pnpm --dir services/r2-access-worker test`
- [x] `pnpm --dir services/r2-access-worker exec tsc --noEmit`
- [x] `git diff --check`

---

## fix(r2-access-worker): allow zooclaw pack downloads for logged-in users (#2306)

- **SHA**: `586e6cd9b6d3169c249013eb018e1ddffb26e0d9`
- **作者**: bill-srp
- **日期**: 2026-06-09T11:03:34Z
- **PR**: #2306
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/586e6cd9b6d3169c249013eb018e1ddffb26e0d9

### 完整 commit message

```
fix(r2-access-worker): allow zooclaw pack downloads for logged-in users (#2306)

## Summary
- Allow protected R2 reads under the global `zooclaw/` pack namespace
for any valid logged-in account.
- Keep existing org matching behavior for all non-zooclaw object keys.

## Root cause
The R2 access worker derives `org_id` from the first object-key segment
and the default `/account/me` authorization path required it to match
the caller's current org. Official agent pack archives live under
`zooclaw/...`, so normal user tokens were authenticated but rejected by
the org match.

## Test plan
- [x] `pnpm --dir services/r2-access-worker test`
- [x] `pnpm --dir services/r2-access-worker exec tsc --noEmit`
- [x] `git diff --check`
```

### 完整 PR body

## Summary
- Allow protected R2 reads under the global `zooclaw/` pack namespace for any valid logged-in account.
- Keep existing org matching behavior for all non-zooclaw object keys.

## Root cause
The R2 access worker derives `org_id` from the first object-key segment and the default `/account/me` authorization path required it to match the caller's current org. Official agent pack archives live under `zooclaw/...`, so normal user tokens were authenticated but rejected by the org match.

## Test plan
- [x] `pnpm --dir services/r2-access-worker test`
- [x] `pnpm --dir services/r2-access-worker exec tsc --noEmit`
- [x] `git diff --check`

---

## docs: archive shipped provider-tree refactor spec (#2295)

- **SHA**: `d7c448893988c6ae294afeffa944ec90b2eba04f`
- **作者**: chris-srp
- **日期**: 2026-06-09T10:22:01Z
- **PR**: #2295
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/d7c448893988c6ae294afeffa944ec90b2eba04f

### 完整 commit message

```
docs: archive shipped provider-tree refactor spec (#2295)

The provider-tree refactor is complete — all phases merged:

| Phase | PRs |
|---|---|
| 1 memoization | #2237 |
| 2 GlobalOverlays + view extraction | #2275 #2276 #2277 #2278 |
| 3 (marketing)/(app) route groups | #2280 #2283 |
| 4 OpenClaw/Mattermost → (chat) + ClawPageHeader split | #2285 #2289
#2292 |
| 5 drop AppEnvironment + de-provider Auth | #2294 |

Moves `docs/superpowers/specs/2026-06-06-provider-tree-refactor.md` →
`docs/archive/specs/`. No inbound links, no internal relative links to
rewrite.

**Scope-down notes** (documented in PRs, not failures): Phase 4's
`SubscriptionPanel→(billing)` was dropped (app-wide chrome) and Phase 5
was narrowed from "convert 4 contexts to Zustand" to "delete dead
AppEnvironment + de-provider Auth" (Auth already Zustand;
UserBusinessData is RQ; BrandTheme is startup config per the 2026-05-28
migration spec).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### 完整 PR body

The provider-tree refactor is complete — all phases merged:

| Phase | PRs |
|---|---|
| 1 memoization | #2237 |
| 2 GlobalOverlays + view extraction | #2275 #2276 #2277 #2278 |
| 3 (marketing)/(app) route groups | #2280 #2283 |
| 4 OpenClaw/Mattermost → (chat) + ClawPageHeader split | #2285 #2289 #2292 |
| 5 drop AppEnvironment + de-provider Auth | #2294 |

Moves `docs/superpowers/specs/2026-06-06-provider-tree-refactor.md` → `docs/archive/specs/`. No inbound links, no internal relative links to rewrite.

**Scope-down notes** (documented in PRs, not failures): Phase 4's `SubscriptionPanel→(billing)` was dropped (app-wide chrome) and Phase 5 was narrowed from "convert 4 contexts to Zustand" to "delete dead AppEnvironment + de-provider Auth" (Auth already Zustand; UserBusinessData is RQ; BrandTheme is startup config per the 2026-05-28 migration spec).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): stabilize CronClient loadRunsFromAnySource callback identity (#2304)

- **SHA**: `348c9fc416a34782b64af3c0c1bba55a832ba13c`
- **作者**: chris-srp
- **日期**: 2026-06-09T10:21:08Z
- **PR**: #2304
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/348c9fc416a34782b64af3c0c1bba55a832ba13c

### 完整 commit message

```
refactor(web): stabilize CronClient loadRunsFromAnySource callback identity (#2304)

## Summary
- `loadRunsFromAnySource` was the only `useOpenClaw()` consumer that
depended on the **whole** `oc` context object (`useCallback(...,
[oc])`), so the callback identity churned on every passive OpenClaw
state change (ws status, init status, bot, …).
- Switch its WebSocket-fallback call to read `sendRequestRef.current`
(the ref is already kept current each render at the top of the
component) and drop the dependency array to `[]`, mirroring the sibling
`wsFallback` callback right above it.
- Pure identity-stability hygiene — **no behavior change**.

## Context
Follow-up surfaced while auditing the 6 `useOpenClaw()` consumers after
#2302. That audit confirmed none of them form a real `useEffect(...,
[ctx])` + setState update loop; this `[oc]` dependency was the only
remaining whole-object capture, and it's a memoized callback (not an
effect), so it only caused needless callback re-creation, never a render
loop. Cleaning it up removes the last bit of churn and brings the file
fully in line with its own `sendRequestRef` pattern.

## Test plan
- [x] `pnpm --dir web/app exec tsc --noEmit --pretty false`
- [x] `pnpm --dir web/app exec eslint
'src/app/[locale]/(app)/(chat)/schedule/CronClient.tsx' --quiet` (clean;
no new `react-hooks/exhaustive-deps` warning)
- [x] `pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/app/schedule/cron-client.unit.spec.tsx
tests/unit/hooks/queries/cron/useCronJobs.unit.spec.tsx` (69 passed)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### 完整 PR body

## Summary
- `loadRunsFromAnySource` was the only `useOpenClaw()` consumer that depended on the **whole** `oc` context object (`useCallback(..., [oc])`), so the callback identity churned on every passive OpenClaw state change (ws status, init status, bot, …).
- Switch its WebSocket-fallback call to read `sendRequestRef.current` (the ref is already kept current each render at the top of the component) and drop the dependency array to `[]`, mirroring the sibling `wsFallback` callback right above it.
- Pure identity-stability hygiene — **no behavior change**.

## Context
Follow-up surfaced while auditing the 6 `useOpenClaw()` consumers after #2302. That audit confirmed none of them form a real `useEffect(..., [ctx])` + setState update loop; this `[oc]` dependency was the only remaining whole-object capture, and it's a memoized callback (not an effect), so it only caused needless callback re-creation, never a render loop. Cleaning it up removes the last bit of churn and brings the file fully in line with its own `sendRequestRef` pattern.

## Test plan
- [x] `pnpm --dir web/app exec tsc --noEmit --pretty false`
- [x] `pnpm --dir web/app exec eslint 'src/app/[locale]/(app)/(chat)/schedule/CronClient.tsx' --quiet` (clean; no new `react-hooks/exhaustive-deps` warning)
- [x] `pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/app/schedule/cron-client.unit.spec.tsx tests/unit/hooks/queries/cron/useCronJobs.unit.spec.tsx` (69 passed)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): convert Feedback to store + bootstrap hook, drop FeedbackProvider (#2301)

- **SHA**: `8e50ca76a551ab28903aa444ab7f6b92749ce6e2`
- **作者**: chris-srp
- **日期**: 2026-06-09T10:19:31Z
- **PR**: #2301
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/8e50ca76a551ab28903aa444ab7f6b92749ce6e2

### 完整 commit message

```
refactor(web): convert Feedback to store + bootstrap hook, drop FeedbackProvider (#2301)

## What

Third "UI-state provider → Zustand" pass; **first effect-heavy one**
(flattening 7→6). The provider's side-effects move to a bootstrap hook,
its state to a vanilla store.

- **New `lib/feedback-store.ts`** — vanilla store (`{ healthStatus,
isDialogOpen, crashInfo }`) + actions. The `HealthMonitor` instance +
long-task counter are module refs registered by the bootstrap;
`HealthMonitor` is imported **type-only** so the store stays React-free
(passes `check-no-react-in-stores`).
- **New `hooks/useFeedbackBootstrap.ts`** — the 4 effects (HealthMonitor
lifecycle, Sentry identity, window error / long-task observers), called
once in ClientLayout.
- **New `lib/useFeedback.ts`** — `useHealthStatus()` store reader (used
by FeedbackDialog).
- **New `components/feedback/FeedbackHost.tsx`** — the FAB + dialog
portal, reads the store directly.
- **Crash bridge simplified**: `reportCrash` is now a module-level store
action that's always available, so `ErrorBoundary` calls it directly (no
callback/replay queue) and the always-mounted `FeedbackHost` shows the
dialog immediately. Only the monitor's crash *tally* is deferred via a
small queue flushed when the monitor registers — preserving that
behavior for the (extremely early) pre-bootstrap case.

`FeedbackProvider` deleted; `ErrorBoundary` / `GlobalOverlays` /
`FeedbackDialog` imports updated; ClientLayout drops the wrapper + calls
`useFeedbackBootstrap()`.

## Tests

- `FeedbackProvider` spec → `FeedbackHost` spec (integration: bootstrap
harness + host + store). Full surface preserved: monitor lifecycle,
Sentry identity, dialog open/close + acknowledge, reportCrash, the
**#2278 ErrorBoundary-sibling regression**, pre-register crash deferral,
window listeners.
- `tsc`, `lint`, `lint:ci` (incl. no-react guard), `dup` green; unit
suite passes (1 flaky-under-parallelism file confirmed passing in
isolation).

3 of 4. Last: LoginCheck (the most intricate — reducer +
router/auth-watching effects + modal host).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### 完整 PR body

## What

Third "UI-state provider → Zustand" pass; **first effect-heavy one** (flattening 7→6). The provider's side-effects move to a bootstrap hook, its state to a vanilla store.

- **New `lib/feedback-store.ts`** — vanilla store (`{ healthStatus, isDialogOpen, crashInfo }`) + actions. The `HealthMonitor` instance + long-task counter are module refs registered by the bootstrap; `HealthMonitor` is imported **type-only** so the store stays React-free (passes `check-no-react-in-stores`).
- **New `hooks/useFeedbackBootstrap.ts`** — the 4 effects (HealthMonitor lifecycle, Sentry identity, window error / long-task observers), called once in ClientLayout.
- **New `lib/useFeedback.ts`** — `useHealthStatus()` store reader (used by FeedbackDialog).
- **New `components/feedback/FeedbackHost.tsx`** — the FAB + dialog portal, reads the store directly.
- **Crash bridge simplified**: `reportCrash` is now a module-level store action that's always available, so `ErrorBoundary` calls it directly (no callback/replay queue) and the always-mounted `FeedbackHost` shows the dialog immediately. Only the monitor's crash *tally* is deferred via a small queue flushed when the monitor registers — preserving that behavior for the (extremely early) pre-bootstrap case.

`FeedbackProvider` deleted; `ErrorBoundary` / `GlobalOverlays` / `FeedbackDialog` imports updated; ClientLayout drops the wrapper + calls `useFeedbackBootstrap()`.

## Tests

- `FeedbackProvider` spec → `FeedbackHost` spec (integration: bootstrap harness + host + store). Full surface preserved: monitor lifecycle, Sentry identity, dialog open/close + acknowledge, reportCrash, the **#2278 ErrorBoundary-sibling regression**, pre-register crash deferral, window listeners.
- `tsc`, `lint`, `lint:ci` (incl. no-react guard), `dup` green; unit suite passes (1 flaky-under-parallelism file confirmed passing in isolation).

3 of 4. Last: LoginCheck (the most intricate — reducer + router/auth-watching effects + modal host).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(web): stop chat provider update loops (#2302)

- **SHA**: `67ac47b81d6fb6bcddcb5a602cb5fa495cc43d94`
- **作者**: chris-srp
- **日期**: 2026-06-09T10:06:23Z
- **PR**: #2302
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/67ac47b81d6fb6bcddcb5a602cb5fa495cc43d94

### 完整 commit message

```
fix(web): stop chat provider update loops (#2302)

## Summary
- Fix `useOpenClaw()` so passive context state changes do not re-run
chat activation effects.
- Add `FilePreviewProvider` state to session thread chat routes so
shared Mattermost attachment renderers can open artifact previews.
- Add regression coverage for both staging Sentry failures.

## Root cause
The provider-tree refactor moved OpenClaw/Mattermost into the `(chat)`
layout. On `/chat`, `useOpenClaw()` depended on the entire context
object, so normal provider state changes could re-run the activation
effect and contribute to the React maximum update depth failure seen in
staging Sentry.

The session thread route also reused the shared chat renderer but did
not provide `FilePreviewProvider`, so messages with Mattermost
attachments could call `useFilePreview()` outside its provider.

## Test plan
- [x] `pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/contexts/OpenClawContext.unit.spec.tsx
tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx`
- [x] `pnpm --dir web/app exec eslint src/contexts/OpenClawContext.tsx
'src/app/[locale]/(app)/(chat)/chat/[computerId]/[agentId]/[sessionId]/SessionThreadClient.tsx'
tests/unit/contexts/OpenClawContext.unit.spec.tsx
tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx --quiet`\n-
[x] `pnpm --dir web/app exec tsc --noEmit --pretty false`
```

### 完整 PR body

## Summary
- Fix `useOpenClaw()` so passive context state changes do not re-run chat activation effects.
- Add `FilePreviewProvider` state to session thread chat routes so shared Mattermost attachment renderers can open artifact previews.
- Add regression coverage for both staging Sentry failures.

## Root cause
The provider-tree refactor moved OpenClaw/Mattermost into the `(chat)` layout. On `/chat`, `useOpenClaw()` depended on the entire context object, so normal provider state changes could re-run the activation effect and contribute to the React maximum update depth failure seen in staging Sentry.

The session thread route also reused the shared chat renderer but did not provide `FilePreviewProvider`, so messages with Mattermost attachments could call `useFilePreview()` outside its provider.

## Test plan
- [x] `pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/contexts/OpenClawContext.unit.spec.tsx tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx`
- [x] `pnpm --dir web/app exec eslint src/contexts/OpenClawContext.tsx 'src/app/[locale]/(app)/(chat)/chat/[computerId]/[agentId]/[sessionId]/SessionThreadClient.tsx' tests/unit/contexts/OpenClawContext.unit.spec.tsx tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx --quiet`\n- [x] `pnpm --dir web/app exec tsc --noEmit --pretty false`

---

## refactor(web): convert SupportTicket to a Zustand store, drop SupportTicketProvider (#2299)

- **SHA**: `e98b718c4d3e3cb6b66d0fe3af48f77a7fea33ed`
- **作者**: chris-srp
- **日期**: 2026-06-09T09:19:35Z
- **PR**: #2299
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/e98b718c4d3e3cb6b66d0fe3af48f77a7fea33ed

### 完整 commit message

```
refactor(web): convert SupportTicket to a Zustand store, drop SupportTicketProvider (#2299)

## What

Second clean "UI-state provider → Zustand store" pass (same shape as
Toast #2298), flattening the global tree 8→7. SupportTicket holds only
transient open/category state and was already action/state-split in
Phase 2, so this is a net simplification.

- **New `lib/support-ticket-store.ts`** — vanilla store (`{ isOpen,
defaultCategory }` + `openSupportTicket`/`closeSupportTicket`).
React-free (passes `check-no-react-in-stores`).
- **`SupportTicketModal.tsx`** keeps `<SupportTicketHost/>` (now
`useStore(supportTicketStore, …)`) + the modal; `useSupportTicket()`
returns a stable module action object. **Same import path** → the **5
consumers unchanged**. `SupportTicketProvider` + both contexts deleted.
- **ClientLayout** drops `<SupportTicketProvider>`; `SupportTicketHost`
(in `GlobalOverlays`) reads the store directly.

## Tests

- Spec renders `SupportTicketHost` standalone + resets the store between
tests; dropped the obsolete "throws outside provider" test. ClientLayout
spec mock trimmed.
- `tsc`, `lint`, `lint:ci` (incl. no-react guard), `dup` green; unit
suite passes (1 flaky-under-parallelism file confirmed passing in
isolation).

2 of 4. Next: Feedback (store + bootstrap), then LoginCheck.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### 完整 PR body

## What

Second clean "UI-state provider → Zustand store" pass (same shape as Toast #2298), flattening the global tree 8→7. SupportTicket holds only transient open/category state and was already action/state-split in Phase 2, so this is a net simplification.

- **New `lib/support-ticket-store.ts`** — vanilla store (`{ isOpen, defaultCategory }` + `openSupportTicket`/`closeSupportTicket`). React-free (passes `check-no-react-in-stores`).
- **`SupportTicketModal.tsx`** keeps `<SupportTicketHost/>` (now `useStore(supportTicketStore, …)`) + the modal; `useSupportTicket()` returns a stable module action object. **Same import path** → the **5 consumers unchanged**. `SupportTicketProvider` + both contexts deleted.
- **ClientLayout** drops `<SupportTicketProvider>`; `SupportTicketHost` (in `GlobalOverlays`) reads the store directly.

## Tests

- Spec renders `SupportTicketHost` standalone + resets the store between tests; dropped the obsolete "throws outside provider" test. ClientLayout spec mock trimmed.
- `tsc`, `lint`, `lint:ci` (incl. no-react guard), `dup` green; unit suite passes (1 flaky-under-parallelism file confirmed passing in isolation).

2 of 4. Next: Feedback (store + bootstrap), then LoginCheck.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): convert Toast to a Zustand store, drop ToastProvider (#2298)

- **SHA**: `5d6fb222b5d639be93377291f22c3b60387eb073`
- **作者**: chris-srp
- **日期**: 2026-06-09T09:08:38Z
- **PR**: #2298
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/5d6fb222b5d639be93377291f22c3b60387eb073

### 完整 commit message

```
refactor(web): convert Toast to a Zustand store, drop ToastProvider (#2298)

## What

First of the "UI-state provider → Zustand store" passes (flattening the
global tree 9→8 per the agreed cleanup). Toast holds only transient
state and was already action/state-split in Phase 2b, so this is a clean
simplification.

- **New `lib/toast-store.ts`** — vanilla store (`{ toasts }` +
`showToast`/`removeToast`, module-level auto-dismiss timers). React-free
(passes `check-no-react-in-stores`).
- **`ui/Toast.tsx`** keeps `<ToastViewport/>` (now `useStore(toastStore,
…)`) + `useToast()` (returns a stable module action object). **Same
import path** → the **22 `useToast` consumers are unchanged**.
`ToastProvider` + both contexts deleted.
- **ClientLayout** drops `<ToastProvider>`; `ToastViewport` (in
`GlobalOverlays`) reads the store directly — no provider ancestor
needed.

## Tests

- Toast spec renders `ToastViewport` standalone + resets the store
between tests; dropped the now-obsolete "throws outside provider" tests.
ClientLayout spec mock trimmed to `ToastViewport`.
- `tsc`, `lint`, `lint:ci` (incl. no-react-in-stores guard), `dup`
green; unit suite passes.

First of 4 (Toast → SupportTicket → Feedback → LoginCheck); each is an
independent PR.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### 完整 PR body

## What

First of the "UI-state provider → Zustand store" passes (flattening the global tree 9→8 per the agreed cleanup). Toast holds only transient state and was already action/state-split in Phase 2b, so this is a clean simplification.

- **New `lib/toast-store.ts`** — vanilla store (`{ toasts }` + `showToast`/`removeToast`, module-level auto-dismiss timers). React-free (passes `check-no-react-in-stores`).
- **`ui/Toast.tsx`** keeps `<ToastViewport/>` (now `useStore(toastStore, …)`) + `useToast()` (returns a stable module action object). **Same import path** → the **22 `useToast` consumers are unchanged**. `ToastProvider` + both contexts deleted.
- **ClientLayout** drops `<ToastProvider>`; `ToastViewport` (in `GlobalOverlays`) reads the store directly — no provider ancestor needed.

## Tests

- Toast spec renders `ToastViewport` standalone + resets the store between tests; dropped the now-obsolete "throws outside provider" tests. ClientLayout spec mock trimmed to `ToastViewport`.
- `tsc`, `lint`, `lint:ci` (incl. no-react-in-stores guard), `dup` green; unit suite passes.

First of 4 (Toast → SupportTicket → Feedback → LoginCheck); each is an independent PR.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(computers): proxy FastClaw status (#2288)

- **SHA**: `4104f8e42ee2bcd95d8c354ee3f06c709ff8f7fa`
- **作者**: bill-srp
- **日期**: 2026-06-09T09:00:55Z
- **PR**: #2288
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/4104f8e42ee2bcd95d8c354ee3f06c709ff8f7fa

### 完整 commit message

```
feat(computers): proxy FastClaw status (#2288)

## Summary
- add claw-interface computer status proxy backed by FastClaw bot status
- expose Next.js API route and client helper for computer status
- update ClawPageHeader to use FastClaw readiness plus Mattermost
instead of OpenClaw websocket status

## Linear

https://linear.app/srpone/issue/ECA-913/mitigate-openclaw-pod-notready-and-message-latency

## Test plan
- pnpm --dir web run lint
- pnpm --dir web run test:unit
- pnpm --dir web/app exec eslint
'src/app/api/openclaw/computers/[computerId]/status/route.ts'
src/lib/api/openclaw.ts src/components/ClawPageHeader.tsx
tests/unit/components/ClawPageHeader.unit.spec.ts
- pnpm --dir web/app exec vitest run
tests/unit/components/ClawPageHeader.unit.spec.ts
tests/unit/components/ClawPageHeader-extras.unit.spec.tsx
- ruff check .
- PYTHONPATH=. .venv/bin/python -m pytest
tests/unit/test_computer_routes.py tests/unit/test_computer_service.py
-q

## Notes
- pnpm --dir web run tsc currently fails before this change because
web/app/.next/types contains stale generated route references.
- pyright app tests only fails on missing
favie_common.logging/request_context in the local venv.
- full backend pytest coverage is blocked locally by sandboxed Mongo DNS
and missing favie_common request_context modules.
```

### 完整 PR body

## Summary
- add claw-interface computer status proxy backed by FastClaw bot status
- expose Next.js API route and client helper for computer status
- update ClawPageHeader to use FastClaw readiness plus Mattermost instead of OpenClaw websocket status

## Linear
https://linear.app/srpone/issue/ECA-913/mitigate-openclaw-pod-notready-and-message-latency

## Test plan
- pnpm --dir web run lint
- pnpm --dir web run test:unit
- pnpm --dir web/app exec eslint 'src/app/api/openclaw/computers/[computerId]/status/route.ts' src/lib/api/openclaw.ts src/components/ClawPageHeader.tsx tests/unit/components/ClawPageHeader.unit.spec.ts
- pnpm --dir web/app exec vitest run tests/unit/components/ClawPageHeader.unit.spec.ts tests/unit/components/ClawPageHeader-extras.unit.spec.tsx
- ruff check .
- PYTHONPATH=. .venv/bin/python -m pytest tests/unit/test_computer_routes.py tests/unit/test_computer_service.py -q

## Notes
- pnpm --dir web run tsc currently fails before this change because web/app/.next/types contains stale generated route references.
- pyright app tests only fails on missing favie_common.logging/request_context in the local venv.
- full backend pytest coverage is blocked locally by sandboxed Mongo DNS and missing favie_common request_context modules.

---

## refactor(web): drop AppEnvironment + de-provider-ize Auth (provider-tree Phase 5) (#2294)

- **SHA**: `3e63aa92d4e10afba644e2eb79ba90c3980f1ec9`
- **作者**: chris-srp
- **日期**: 2026-06-09T08:41:19Z
- **PR**: #2294
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/3e63aa92d4e10afba644e2eb79ba90c3980f1ec9

### 完整 commit message

```
refactor(web): drop AppEnvironment + de-provider-ize Auth (provider-tree Phase 5) (#2294)

## What

**Final phase** of the provider-tree refactor. Sheds two nodes from
ClientLayout's global provider stack (11→9).

**Scoped down from the spec's "convert 4 contexts to Zustand"** —
investigation showed that framing didn't hold: `Auth` state already
lives in the Zustand `auth-snapshot-store`, `AppEnvironment` is dead,
and `UserBusinessData` (React Query) + `BrandTheme` (startup config) are
explicitly out of Zustand scope per the earlier
`2026-05-28-zustand-store-migration.md`. So this is **targeted
cleanup**, not a migration (confirmed with you).

- **Delete `contexts/AppEnvironmentContext.tsx`** — dead context (zero
consumers). Its only effect (priming `window.isNativeApp`) is preserved
by a one-line `getEnvInfo()` call in ClientLayout's mount effect
(`getEnvInfo` sets it).
- **De-provider-ize Auth**: `AuthProvider` was a pure side-effect runner
(no context; `return <>{children}</>`). Its effect body moves
**verbatim** to a new `hooks/useAuthBootstrap.ts`, called once in
ClientLayout. `AuthProvider` deleted. `useAuth` / `useAuthSnapshot` /
`auth-snapshot-store` / the logout `resetAuthSnapshotForLogout()` are
**unchanged**.
- ClientLayout drops the `<AppEnvironmentProvider>` + `<AuthProvider>`
wrappers.

## Why it's safe

- `AuthProvider` component was imported only by ClientLayout (verified).
No src code reads `window.isNativeApp` directly; the startup write is
preserved defensively.
- Effect-timing note: the bootstrap moves from a deep-child effect to a
ClientLayout (parent) effect — safe, since it only reads localStorage +
installs listeners and doesn't depend on other providers;
`useAuthSnapshot` consumers also self-seed.

## Tests

- `AuthProvider.unit.spec` →
`tests/unit/hooks/useAuthBootstrap.unit.spec.tsx` (renders a hook
harness; same 11 assertions). Deleted AppEnvironment spec. Updated
ClientLayout spec mocks.
- `tsc`, `lint`, `lint:ci`, `dup` green; full `test:unit` (**6971
pass**).

**Completes the provider-tree refactor (Phases 1–5).**
UserBusinessData/BrandTheme intentionally left as-is (RQ /
startup-config; not Zustand candidates).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### 完整 PR body

## What

**Final phase** of the provider-tree refactor. Sheds two nodes from ClientLayout's global provider stack (11→9).

**Scoped down from the spec's "convert 4 contexts to Zustand"** — investigation showed that framing didn't hold: `Auth` state already lives in the Zustand `auth-snapshot-store`, `AppEnvironment` is dead, and `UserBusinessData` (React Query) + `BrandTheme` (startup config) are explicitly out of Zustand scope per the earlier `2026-05-28-zustand-store-migration.md`. So this is **targeted cleanup**, not a migration (confirmed with you).

- **Delete `contexts/AppEnvironmentContext.tsx`** — dead context (zero consumers). Its only effect (priming `window.isNativeApp`) is preserved by a one-line `getEnvInfo()` call in ClientLayout's mount effect (`getEnvInfo` sets it).
- **De-provider-ize Auth**: `AuthProvider` was a pure side-effect runner (no context; `return <>{children}</>`). Its effect body moves **verbatim** to a new `hooks/useAuthBootstrap.ts`, called once in ClientLayout. `AuthProvider` deleted. `useAuth` / `useAuthSnapshot` / `auth-snapshot-store` / the logout `resetAuthSnapshotForLogout()` are **unchanged**.
- ClientLayout drops the `<AppEnvironmentProvider>` + `<AuthProvider>` wrappers.

## Why it's safe

- `AuthProvider` component was imported only by ClientLayout (verified). No src code reads `window.isNativeApp` directly; the startup write is preserved defensively.
- Effect-timing note: the bootstrap moves from a deep-child effect to a ClientLayout (parent) effect — safe, since it only reads localStorage + installs listeners and doesn't depend on other providers; `useAuthSnapshot` consumers also self-seed.

## Tests

- `AuthProvider.unit.spec` → `tests/unit/hooks/useAuthBootstrap.unit.spec.tsx` (renders a hook harness; same 11 assertions). Deleted AppEnvironment spec. Updated ClientLayout spec mocks.
- `tsc`, `lint`, `lint:ci`, `dup` green; full `test:unit` (**6971 pass**).

**Completes the provider-tree refactor (Phases 1–5).** UserBusinessData/BrandTheme intentionally left as-is (RQ / startup-config; not Zustand candidates).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): narrow OpenClaw/Mattermost into (chat) layout (provider-tree Phase 4b) (#2292)

- **SHA**: `6f7fe6df8fd0ab52ea0f43b00d90af8aab2b620c`
- **作者**: chris-srp
- **日期**: 2026-06-09T07:42:44Z
- **PR**: #2292
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/6f7fe6df8fd0ab52ea0f43b00d90af8aab2b620c

### 完整 commit message

```
refactor(web): narrow OpenClaw/Mattermost into (chat) layout (provider-tree Phase 4b) (#2292)

## What

Redo of the closed #2286 — **now safe** after the ClawPageHeader split
(#2289). OpenClaw is consumed only within the `(chat)` cluster (its sole
shared header consumer `ClawConnectionStatus` renders only via
`ClawPageHeader`, which is now only used in `(chat)` pages). Non-chat
app routes stop mounting the WebSocket-heavy providers.

- **New `(app)/(chat)/layout.tsx`** mounts `OpenClaw → Mattermost`.
- **`(app)/layout.tsx`** drops `OpenClaw` + `Mattermost`, keeping
`UserBusinessData → SubscriptionPanel → Onboarding` + `AppLayout` +
`AppOverlays`.

`UserBusinessData` stays at `(app)` (`new-chat` uses it; lazy RQ hook,
no socket; `Mattermost` reads it from the `(app)` parent).
`SubscriptionPanel` stays app-wide (sidebar Upgrade CTA + paywall FAB).

## The audit that the first attempt missed

Full pre-narrowing audit this time confirmed **no non-`(chat)`
consumer** of `useOpenClaw*`/`useMattermost*` (throwing): every real
`ClawPageHeader` importer is in `(chat)`, and the lone `canvas` grep hit
is a comment. The first attempt (#2286) under-counted because it checked
routes that *name* the providers, not *where shared components render* —
`ClawPageHeader` rendered on profile/session-history. #2289 moved those
to the generic `PageHeader`, closing the gap.

## Tests

- New `(chat)`-layout smoke spec; `(app)`-layout spec drops
OpenClaw/Mattermost mocks.
- `tsc`, `lint`, `lint:ci`, `dup` green; full `test:unit` passes (2
flaky-under-parallelism specs confirmed passing in isolation, unrelated
to this change).

**Completes Phase 4.** (SubscriptionPanel→`(billing)` was dropped as
infeasible — it's app-wide chrome.)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### 完整 PR body

## What

Redo of the closed #2286 — **now safe** after the ClawPageHeader split (#2289). OpenClaw is consumed only within the `(chat)` cluster (its sole shared header consumer `ClawConnectionStatus` renders only via `ClawPageHeader`, which is now only used in `(chat)` pages). Non-chat app routes stop mounting the WebSocket-heavy providers.

- **New `(app)/(chat)/layout.tsx`** mounts `OpenClaw → Mattermost`.
- **`(app)/layout.tsx`** drops `OpenClaw` + `Mattermost`, keeping `UserBusinessData → SubscriptionPanel → Onboarding` + `AppLayout` + `AppOverlays`.

`UserBusinessData` stays at `(app)` (`new-chat` uses it; lazy RQ hook, no socket; `Mattermost` reads it from the `(app)` parent). `SubscriptionPanel` stays app-wide (sidebar Upgrade CTA + paywall FAB).

## The audit that the first attempt missed

Full pre-narrowing audit this time confirmed **no non-`(chat)` consumer** of `useOpenClaw*`/`useMattermost*` (throwing): every real `ClawPageHeader` importer is in `(chat)`, and the lone `canvas` grep hit is a comment. The first attempt (#2286) under-counted because it checked routes that *name* the providers, not *where shared components render* — `ClawPageHeader` rendered on profile/session-history. #2289 moved those to the generic `PageHeader`, closing the gap.

## Tests

- New `(chat)`-layout smoke spec; `(app)`-layout spec drops OpenClaw/Mattermost mocks.
- `tsc`, `lint`, `lint:ci`, `dup` green; full `test:unit` passes (2 flaky-under-parallelism specs confirmed passing in isolation, unrelated to this change).

**Completes Phase 4.** (SubscriptionPanel→`(billing)` was dropped as infeasible — it's app-wide chrome.)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## ci: stop web build check creating deployments (#2293)

- **SHA**: `d23d77ddea1f8daee06e783e3efe9b0a6efac70e`
- **作者**: chris-srp
- **日期**: 2026-06-09T07:37:28Z
- **PR**: #2293
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/d23d77ddea1f8daee06e783e3efe9b0a6efac70e

### 完整 commit message

```
ci: stop web build check creating deployments (#2293)

## Summary
- Keep the PR-time web build compile sanity check for App Router/RSC
boundary coverage.
- Remove the staging GitHub environment binding and environment-scoped
vars/secrets injection from that check.
- Keep the required code-quality summary gate wired to web-build-check,
without generating GitHub deployment records.

## Test plan
- [x] ruby -e 'require "yaml";
YAML.load_file(".github/workflows/code-quality.yml"); puts "workflow
yaml ok"'
- [x] git diff --check -- .github/workflows/code-quality.yml
- [x] APP_ENV=staging NODE_ENV=production
NODE_OPTIONS=--max-old-space-size=8192 pnpm --dir web/app exec next
build --experimental-build-mode=compile
- [x] Verified RequireCodeQualityCheck only requires code-quality and
size / size-check.
```

### 完整 PR body

## Summary
- Keep the PR-time web build compile sanity check for App Router/RSC boundary coverage.
- Remove the staging GitHub environment binding and environment-scoped vars/secrets injection from that check.
- Keep the required code-quality summary gate wired to web-build-check, without generating GitHub deployment records.

## Test plan
- [x] ruby -e 'require "yaml"; YAML.load_file(".github/workflows/code-quality.yml"); puts "workflow yaml ok"'
- [x] git diff --check -- .github/workflows/code-quality.yml
- [x] APP_ENV=staging NODE_ENV=production NODE_OPTIONS=--max-old-space-size=8192 pnpm --dir web/app exec next build --experimental-build-mode=compile
- [x] Verified RequireCodeQualityCheck only requires code-quality and size / size-check.

---

## fix(billing): preserve renewal history and retry bg idempotency (#2291)

- **SHA**: `5e4b36b71afda97f3a3cc447a8a413fc2f1c2606`
- **作者**: kaka-srp
- **日期**: 2026-06-09T07:33:02Z
- **PR**: #2291
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/5e4b36b71afda97f3a3cc447a8a413fc2f1c2606

### 完整 commit message

```
fix(billing): preserve renewal history and retry bg idempotency (#2291)

## Summary
- Fix Stripe renewal invoice handling so renewal `invoice.paid` events
create distinct Billing v2 payment orders instead of overwriting the
original checkout order.
- Make invoice download V2-only by reading Billing v2 payment orders
only, with support for provider-created renewal rows addressed by
`payment_order_id`.
- Retry only Billing Gateway's explicit in-progress idempotency `409`
response for `subscribe()` / `topup_wallet()` instead of surfacing
transient webhook 500s.
- Include the PR workflow skill update requested in this branch.

Linear:
https://linear.app/srpone/issue/ECA-928/fix-stripe-renewal-order-history

## Root cause
Stripe renewal invoices can carry the original checkout metadata
`order_id`. The previous `invoice.paid` resolver used that metadata for
renewal invoices too, so the June renewal updated the May checkout
payment order and hid the second payment from the order list / invoice
download flow.

Separately, concurrent webhook fulfillment can send the same BG
`transaction_id` while another worker is still processing it. BG
correctly returns `409 duplicate request still in progress`, but
claw-interface treated that as a terminal HTTP error and returned
webhook 500.

## Test plan
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff format --check .`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff check .`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_billing_client.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_invoice_lookup.py tests/unit/test_stripe_billing_v2.py
tests/unit/test_orders_endpoints.py -q` (156 passed)
- [ ] `cd services/claw-interface && pyright app tests` currently fails
in the local devcontainer because installed `favie-common v0.3.62` lacks
`favie_common.logging` and `favie_common.middleware.request_context`;
this is unrelated to the changed files and is expected to be covered by
CI's pinned environment.
```

### 完整 PR body

## Summary
- Fix Stripe renewal invoice handling so renewal `invoice.paid` events create distinct Billing v2 payment orders instead of overwriting the original checkout order.
- Make invoice download V2-only by reading Billing v2 payment orders only, with support for provider-created renewal rows addressed by `payment_order_id`.
- Retry only Billing Gateway's explicit in-progress idempotency `409` response for `subscribe()` / `topup_wallet()` instead of surfacing transient webhook 500s.
- Include the PR workflow skill update requested in this branch.

Linear: https://linear.app/srpone/issue/ECA-928/fix-stripe-renewal-order-history

## Root cause
Stripe renewal invoices can carry the original checkout metadata `order_id`. The previous `invoice.paid` resolver used that metadata for renewal invoices too, so the June renewal updated the May checkout payment order and hid the second payment from the order list / invoice download flow.

Separately, concurrent webhook fulfillment can send the same BG `transaction_id` while another worker is still processing it. BG correctly returns `409 duplicate request still in progress`, but claw-interface treated that as a terminal HTTP error and returned webhook 500.

## Test plan
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff format --check .`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff check .`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_billing_client.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_invoice_lookup.py tests/unit/test_stripe_billing_v2.py tests/unit/test_orders_endpoints.py -q` (156 passed)
- [ ] `cd services/claw-interface && pyright app tests` currently fails in the local devcontainer because installed `favie-common v0.3.62` lacks `favie_common.logging` and `favie_common.middleware.request_context`; this is unrelated to the changed files and is expected to be covered by CI's pinned environment.

---

## fix(chat): hide legacy new chat sidebar entry (#2290)

- **SHA**: `0701956cdc8ee33bb2128a6abe0e5e6f0b5af7b1`
- **作者**: bill-srp
- **日期**: 2026-06-09T07:13:43Z
- **PR**: #2290
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/0701956cdc8ee33bb2128a6abe0e5e6f0b5af7b1

### 完整 commit message

```
fix(chat): hide legacy new chat sidebar entry (#2290)

## Summary
- hide the sidebar New Chat launcher when the running OpenClaw image
uses the legacy chat version gate
- pass the legacy version flag into bottom nav item derivation
- cover the hidden legacy entry in sidebar nav tests

## Test Plan
- pnpm --dir web/app exec vitest run
tests/unit/components/sidenav/build-bottom-nav-items.unit.spec.ts
tests/unit/components/sidenav/SideNavAgentList.unit.spec.tsx
tests/unit/hooks/useVersionCheck.unit.spec.tsx
tests/unit/lib/openclaw/version-gate.unit.spec.ts
- pnpm exec eslint --quiet
src/components/sidenav/build-bottom-nav-items.ts
src/components/sidenav/SideNav.tsx
tests/unit/components/sidenav/build-bottom-nav-items.unit.spec.ts
- pnpm --dir web/app exec tsc --noEmit

Follow-up to #2282.
```

### 完整 PR body

## Summary
- hide the sidebar New Chat launcher when the running OpenClaw image uses the legacy chat version gate
- pass the legacy version flag into bottom nav item derivation
- cover the hidden legacy entry in sidebar nav tests

## Test Plan
- pnpm --dir web/app exec vitest run tests/unit/components/sidenav/build-bottom-nav-items.unit.spec.ts tests/unit/components/sidenav/SideNavAgentList.unit.spec.tsx tests/unit/hooks/useVersionCheck.unit.spec.tsx tests/unit/lib/openclaw/version-gate.unit.spec.ts
- pnpm exec eslint --quiet src/components/sidenav/build-bottom-nav-items.ts src/components/sidenav/SideNav.tsx tests/unit/components/sidenav/build-bottom-nav-items.unit.spec.ts
- pnpm --dir web/app exec tsc --noEmit

Follow-up to #2282.

---

## refactor(web): split ClawPageHeader into PageHeader + ClawConnectionStatus (#2289)

- **SHA**: `0e9c4599ccbc2a818e891c6a31e3c8d90245c740`
- **作者**: chris-srp
- **日期**: 2026-06-09T07:13:04Z
- **PR**: #2289
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/0e9c4599ccbc2a818e891c6a31e3c8d90245c740

### 完整 commit message

```
refactor(web): split ClawPageHeader into PageHeader + ClawConnectionStatus (#2289)

## What

Unblocks the OpenClaw narrowing that **Codex correctly flagged on
#2286**: `ClawPageHeader` is an OpenClaw-status header (uses the
throwing `useOpenClawPassive`) but renders on **non-chat pages**
(`profile`, `session-history`), so OpenClaw couldn't move into `(chat)`.
This splits the OpenClaw concern out of the generic header chrome.

- **New `PageHeader`** — generic header shell (`h-14` bar + left
children + optional right `actions` + `testId`). No provider hooks;
usable anywhere.
- **New `ClawConnectionStatus`** — the OpenClaw connection pill (status
badge + retry + dropdown + restart modal). The **only** OpenClaw
consumer (`useOpenClawPassive` + `useMattermostOptional`); renders only
inside chat-cluster pages via `ClawPageHeader`.
- **New `AdvancedRecreate` file** — moved out of `ClawPageHeader` (also
imported by 3 chat components) to avoid a `ClawConnectionStatus →
ClawPageHeader` import cycle; the 3 importers updated.
- **`ClawPageHeader`** now composes `PageHeader` +
`ClawConnectionStatus` + chat actions. **External API + the
`genclaw-page-header`/`genclaw-connection-status` testids are
unchanged** — E2E + existing specs still pass.
- **`profile` + `session-history`** switch to the bare `PageHeader` →
they lose the OpenClaw connection pill (correct — they're not chat
pages).

## Outcome

OpenClaw is now consumed only within the `(chat)` cluster, so a
follow-up PR can narrow `OpenClaw`/`Mattermost` into
`(app)/(chat)/layout.tsx` (the reworked #2286) without breaking non-chat
pages.

## Tests

- New `PageHeader` spec; `ClawConnectionStatus`/`AdvancedRecreate`
covered transitively by the existing `ClawPageHeader` specs (which
render the real composition with OpenClaw mocked — 41 pass);
`session-history` spec switched to mock `PageHeader`.
- `tsc`, `lint`, `lint:ci`, `dup`, full `test:unit` (**6974 pass**) —
all green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### 完整 PR body

## What

Unblocks the OpenClaw narrowing that **Codex correctly flagged on #2286**: `ClawPageHeader` is an OpenClaw-status header (uses the throwing `useOpenClawPassive`) but renders on **non-chat pages** (`profile`, `session-history`), so OpenClaw couldn't move into `(chat)`. This splits the OpenClaw concern out of the generic header chrome.

- **New `PageHeader`** — generic header shell (`h-14` bar + left children + optional right `actions` + `testId`). No provider hooks; usable anywhere.
- **New `ClawConnectionStatus`** — the OpenClaw connection pill (status badge + retry + dropdown + restart modal). The **only** OpenClaw consumer (`useOpenClawPassive` + `useMattermostOptional`); renders only inside chat-cluster pages via `ClawPageHeader`.
- **New `AdvancedRecreate` file** — moved out of `ClawPageHeader` (also imported by 3 chat components) to avoid a `ClawConnectionStatus → ClawPageHeader` import cycle; the 3 importers updated.
- **`ClawPageHeader`** now composes `PageHeader` + `ClawConnectionStatus` + chat actions. **External API + the `genclaw-page-header`/`genclaw-connection-status` testids are unchanged** — E2E + existing specs still pass.
- **`profile` + `session-history`** switch to the bare `PageHeader` → they lose the OpenClaw connection pill (correct — they're not chat pages).

## Outcome

OpenClaw is now consumed only within the `(chat)` cluster, so a follow-up PR can narrow `OpenClaw`/`Mattermost` into `(app)/(chat)/layout.tsx` (the reworked #2286) without breaking non-chat pages.

## Tests

- New `PageHeader` spec; `ClawConnectionStatus`/`AdvancedRecreate` covered transitively by the existing `ClawPageHeader` specs (which render the real composition with OpenClaw mocked — 41 pass); `session-history` spec switched to mock `PageHeader`.
- `tsc`, `lint`, `lint:ci`, `dup`, full `test:unit` (**6974 pass**) — all green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

