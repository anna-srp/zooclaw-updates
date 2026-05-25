# ecap-workspace - 2026-05-24
共 12 条 commits

## [1] fix(web): avoid premature email OTP auth event (#1895)
- **SHA**: `f6c87a4b589539f8d0975ba3737ed87a42aad3c2`
- **作者**: tim-srp
- **日期**: 2026-05-24T16:49:13Z
- **PR**: #1895

### 完整 Commit Message

```
fix(web): avoid premature email OTP auth event (#1895)

## Summary
- Prevent email OTP login from dispatching `auth-state-changed` before
`_completeLogin` finishes.
- Add a regression test that holds `/users/create` pending and asserts
no auth event fires mid-login.

## Why
The email OTP verification screen could briefly remount with an empty
code input while login was still loading because global auth listeners
reacted to token-only user state before `getUserMe` and
business/onboarding sync completed.

## Verification
- `pnpm run test:unit tests/unit/lib/auth/manager.unit.spec.ts`
- `pnpm run test:unit tests/unit/components/LoginForm.unit.spec.tsx
tests/unit/components/LoginCheckProvider.unit.spec.tsx`
- `pnpm exec eslint src/lib/auth/manager.ts
tests/unit/lib/auth/manager.unit.spec.ts --quiet`
- `pnpm run lint`
```

### PR Description

## Summary
- Prevent email OTP login from dispatching `auth-state-changed` before `_completeLogin` finishes.
- Add a regression test that holds `/users/create` pending and asserts no auth event fires mid-login.

## Why
The email OTP verification screen could briefly remount with an empty code input while login was still loading because global auth listeners reacted to token-only user state before `getUserMe` and business/onboarding sync completed.

## Verification
- `pnpm run test:unit tests/unit/lib/auth/manager.unit.spec.ts`
- `pnpm run test:unit tests/unit/components/LoginForm.unit.spec.tsx tests/unit/components/LoginCheckProvider.unit.spec.tsx`
- `pnpm exec eslint src/lib/auth/manager.ts tests/unit/lib/auth/manager.unit.spec.ts --quiet`
- `pnpm run lint`

---

## [2] fix(claw-interface): preprovision warm-pool mattermost (#1894)
- **SHA**: `287158b9c54f304585f33260ec281f0a0f2d3986`
- **作者**: tim-srp
- **日期**: 2026-05-24T15:31:45Z
- **PR**: #1894

### 完整 Commit Message

```
fix(claw-interface): preprovision warm-pool mattermost (#1894)

## Summary\n- Add a warm-pool Mattermost provisioning path that does not
require a pre-claim ecap-account\n- Require Mattermost provisioning
before creating warm-pool OpenClaw bots so ready entries can chat
without claim-time restart\n- Add unit coverage for warm-pool Mattermost
assets and mandatory pre-create channel config\n\n## Verification\n-
ruff check
services/claw-interface/app/services/mattermost_provisioner.py
services/claw-interface/app/services/openclaw/warm_pool_bot_init.py
services/claw-interface/tests/unit/test_mattermost_provisioner.py
services/claw-interface/tests/unit/test_warm_pool_openclaw_assets.py\n-
ruff format --check
services/claw-interface/app/services/mattermost_provisioner.py
services/claw-interface/app/services/openclaw/warm_pool_bot_init.py
services/claw-interface/tests/unit/test_mattermost_provisioner.py
services/claw-interface/tests/unit/test_warm_pool_openclaw_assets.py\n-
pyright app/services/mattermost_provisioner.py
app/services/openclaw/warm_pool_bot_init.py\n- pytest -q -W
ignore::PendingDeprecationWarning
services/claw-interface/tests/unit/test_mattermost_provisioner.py
services/claw-interface/tests/unit/test_openclaw_bot_config.py\n- pytest
-q -W ignore::PendingDeprecationWarning
services/claw-interface/tests/unit/test_warm_pool.py
services/claw-interface/tests/unit/test_warm_pool_materialization.py
services/claw-interface/tests/unit/test_warm_pool_provisioning_assets.py
services/claw-interface/tests/unit/test_warm_pool_openclaw_assets.py\n\n##
Staging\n- Pushed backend staging tag: service-v0.6.84-beta
```

### PR Description

## Summary\n- Add a warm-pool Mattermost provisioning path that does not require a pre-claim ecap-account\n- Require Mattermost provisioning before creating warm-pool OpenClaw bots so ready entries can chat without claim-time restart\n- Add unit coverage for warm-pool Mattermost assets and mandatory pre-create channel config\n\n## Verification\n- ruff check services/claw-interface/app/services/mattermost_provisioner.py services/claw-interface/app/services/openclaw/warm_pool_bot_init.py services/claw-interface/tests/unit/test_mattermost_provisioner.py services/claw-interface/tests/unit/test_warm_pool_openclaw_assets.py\n- ruff format --check services/claw-interface/app/services/mattermost_provisioner.py services/claw-interface/app/services/openclaw/warm_pool_bot_init.py services/claw-interface/tests/unit/test_mattermost_provisioner.py services/claw-interface/tests/unit/test_warm_pool_openclaw_assets.py\n- pyright app/services/mattermost_provisioner.py app/services/openclaw/warm_pool_bot_init.py\n- pytest -q -W ignore::PendingDeprecationWarning services/claw-interface/tests/unit/test_mattermost_provisioner.py services/claw-interface/tests/unit/test_openclaw_bot_config.py\n- pytest -q -W ignore::PendingDeprecationWarning services/claw-interface/tests/unit/test_warm_pool.py services/claw-interface/tests/unit/test_warm_pool_materialization.py services/claw-interface/tests/unit/test_warm_pool_provisioning_assets.py services/claw-interface/tests/unit/test_warm_pool_openclaw_assets.py\n\n## Staging\n- Pushed backend staging tag: service-v0.6.84-beta

---

## [3] fix(onboarding): persist completion state (#1893)
- **SHA**: `24046a354d2448f0d42f92d66d2e0ed94a9a4d39`
- **作者**: tim-srp
- **日期**: 2026-05-24T13:30:48Z
- **PR**: #1893

### 完整 Commit Message

```
fix(onboarding): persist completion state (#1893)

## Summary
- Add explicit onboarding_completed lifecycle state for ecap accounts
and default new accounts to false
- Add authenticated /users/onboarding/complete backend endpoint plus
Next API proxy
- Make frontend onboarding resolver prioritize onboardingCompleted over
bot/credits readiness, with legacy null fallback
- Patch cached backend onboarding status after complete endpoint
succeeds

## Tests
- pnpm --dir web/app run lint
- pnpm --dir web/app exec tsc --noEmit
- pnpm --dir web/app run test:unit --
tests/unit/components/onboarding/resolveOnboardingStatus.unit.spec.ts
tests/unit/lib/api/user.unit.spec.ts
tests/unit/lib/auth/manager.unit.spec.ts
tests/unit/components/providers/OnboardingProvider.unit.spec.tsx
- cd services/claw-interface && ruff check app
tests/unit/test_user_routes_coverage.py && pytest -W
ignore::PendingDeprecationWarning -q
tests/unit/test_user_routes_coverage.py

Note: local manual pyright without the backend venv reports dependency
missing imports; CI/pre-commit standard environment covers pyright.
```

### PR Description

## Summary
- Add explicit onboarding_completed lifecycle state for ecap accounts and default new accounts to false
- Add authenticated /users/onboarding/complete backend endpoint plus Next API proxy
- Make frontend onboarding resolver prioritize onboardingCompleted over bot/credits readiness, with legacy null fallback
- Patch cached backend onboarding status after complete endpoint succeeds

## Tests
- pnpm --dir web/app run lint
- pnpm --dir web/app exec tsc --noEmit
- pnpm --dir web/app run test:unit -- tests/unit/components/onboarding/resolveOnboardingStatus.unit.spec.ts tests/unit/lib/api/user.unit.spec.ts tests/unit/lib/auth/manager.unit.spec.ts tests/unit/components/providers/OnboardingProvider.unit.spec.tsx
- cd services/claw-interface && ruff check app tests/unit/test_user_routes_coverage.py && pytest -W ignore::PendingDeprecationWarning -q tests/unit/test_user_routes_coverage.py

Note: local manual pyright without the backend venv reports dependency missing imports; CI/pre-commit standard environment covers pyright.

---

## [4] refactor(web): extract canvas media utils and pptx parser (#368 F3+F7) (#1884)
- **SHA**: `c03a19d0b3378a45f23bc46a3f0e123cdd0278f9`
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-24T13:05:21Z
- **PR**: #1884

### 完整 Commit Message

```
refactor(web): extract canvas media utils and pptx parser (#368 F3+F7) (#1884)

## Summary

Resolves two findings from web arch-review issue #368:

- **F3** (Duplication): `extractImages` / `extractVideos` / `stripMedia`
were copy-pasted between `useCanvasState.ts` and `useCanvasChat.ts`.
Moved into shared `canvasMediaUtils.ts` (camelCase per
`hooks/**/!(use[A-Z]*).ts` naming rule).
- **F7** (Architecture): `PptxRenderer.tsx` was 1563 lines containing
~1100 lines of inline OOXML parsing before the React component. Split
into `pptx-parser.ts` (1172 lines) + `PptxRenderer.tsx` (398 lines).

## Design notes

- **Parser API surface kept tight**: only `parsePptx`, `EMU_PER_PX`,
`SlideData`, `SlideShape`, `ShapeTransform`, `TextParagraph` are
exported — exactly what the renderer imports. 30+ helpers and 4
supporting types stay module-private (knip flagged a broader export set
as unused).
- **Naming followed lint over finding**: F7 recommended `pptxParser.ts`;
the `check-file/filename-naming-convention` rule for
`src/components/**/!(use[A-Z]*).ts` enforces kebab-case →
`pptx-parser.ts`.
- **Legacy complexity ignore relocated, not added**: `PptxRenderer.tsx`
was on the legacy complexity-overrides list. After split, parser-side
complexity moved with the code; renderer-side `ShapeElement` cc=29
remained. Both files now appear (net +1 entry), but no new lint debt —
existing complexity is attributed to its proper file.
- **F3 helpers modernized to `matchAll`**: replaced `regex.exec()`
while-loop with `Array.from(content.matchAll(...))` — semantically
equivalent, more readable.
- **PR size note**: `git mv` shows as delete+add, doubling the diff line
count for the parser extraction (per known PR-size rename gotcha). The
branch also includes prior unrelated useNavIdentity / SideNav commits
already on origin. May need `size-override` label on CI.

## Test plan

- [x] `npx tsc --noEmit` clean
- [x] `npx eslint` clean on all 5 changed files
- [x] `pnpm lint:deadcode` (knip) clean for new files
- [x] `pnpm test:unit` — 5630 tests pass (no behavior change)
- [x] `bash web/scripts/check-filename-shrink-only.sh` passes
- [ ] CI verification on PR

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Resolves two findings from web arch-review issue #368:

- **F3** (Duplication): `extractImages` / `extractVideos` / `stripMedia` were copy-pasted between `useCanvasState.ts` and `useCanvasChat.ts`. Moved into shared `canvasMediaUtils.ts` (camelCase per `hooks/**/!(use[A-Z]*).ts` naming rule).
- **F7** (Architecture): `PptxRenderer.tsx` was 1563 lines containing ~1100 lines of inline OOXML parsing before the React component. Split into `pptx-parser.ts` (1172 lines) + `PptxRenderer.tsx` (398 lines).

## Design notes

- **Parser API surface kept tight**: only `parsePptx`, `EMU_PER_PX`, `SlideData`, `SlideShape`, `ShapeTransform`, `TextParagraph` are exported — exactly what the renderer imports. 30+ helpers and 4 supporting types stay module-private (knip flagged a broader export set as unused).
- **Naming followed lint over finding**: F7 recommended `pptxParser.ts`; the `check-file/filename-naming-convention` rule for `src/components/**/!(use[A-Z]*).ts` enforces kebab-case → `pptx-parser.ts`.
- **Legacy complexity ignore relocated, not added**: `PptxRenderer.tsx` was on the legacy complexity-overrides list. After split, parser-side complexity moved with the code; renderer-side `ShapeElement` cc=29 remained. Both files now appear (net +1 entry), but no new lint debt — existing complexity is attributed to its proper file.
- **F3 helpers modernized to `matchAll`**: replaced `regex.exec()` while-loop with `Array.from(content.matchAll(...))` — semantically equivalent, more readable.
- **PR size note**: `git mv` shows as delete+add, doubling the diff line count for the parser extraction (per known PR-size rename gotcha). The branch also includes prior unrelated useNavIdentity / SideNav commits already on origin. May need `size-override` label on CI.

## Test plan

- [x] `npx tsc --noEmit` clean
- [x] `npx eslint` clean on all 5 changed files
- [x] `pnpm lint:deadcode` (knip) clean for new files
- [x] `pnpm test:unit` — 5630 tests pass (no behavior change)
- [x] `bash web/scripts/check-filename-shrink-only.sh` passes
- [ ] CI verification on PR

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [5] fix(claw-interface): silence agent pack asset curl progress (#1892)
- **SHA**: `67fa6ffa702edbf53f07f72f9b21489da68027e3`
- **作者**: tim-srp
- **日期**: 2026-05-24T10:37:12Z
- **PR**: #1892

### 完整 Commit Message

```
fix(claw-interface): silence agent pack asset curl progress (#1892)

## Summary
- make GitHub release asset downloads use `curl -fSsL` so curl progress
meters do not pollute runtime deployment errors
- add regression coverage that pack-agent deploy scripts use silent curl
for GitHub release assets

## Testing
- `cd services/claw-interface &&
/Users/a-q/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python
-m pytest tests/unit/test_openclaw_agents.py -q -k 'deploy_agent_pack or
archive_download_script_supports_redirects or archive_deploy_script'` —
3 passed, 126 deselected
- `cd services/claw-interface &&
/Users/a-q/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python
-m pytest tests/unit/test_openclaw_agents.py::TestDeployAgentPack -q` —
6 passed
- `cd services/claw-interface &&
/Users/a-q/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python
-m pytest tests/unit/test_openclaw_agents.py -q` — 129 passed
- `cd services/claw-interface &&
/Users/a-q/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python
-m ruff check app/services/openclaw/agent_archive_deploy_script.py
tests/unit/test_openclaw_agents.py` — passed
- `cd services/claw-interface &&
/Users/a-q/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python
-m ruff format --check
app/services/openclaw/agent_archive_deploy_script.py
tests/unit/test_openclaw_agents.py` — passed
- `cd services/claw-interface &&
/Users/a-q/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python
-m compileall -q app/services/openclaw/agent_archive_deploy_script.py
tests/unit/test_openclaw_agents.py` — passed
- `cd services/claw-interface && LITELLM_PROXY_API_KEY=test-key
/Users/a-q/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python
-m pytest tests/unit -q` — 3618 passed, 2 failed in existing deptry gate
(`tests/unit/test_ci_lint_deptry.py`) because local dependency config
reports pre-existing DEP001 issues such as `bson` imports; no failures
in modified code path

Co-authored-by: A-Q <a-q@A-QdeMac-mini.local>
```

### PR Description

## Summary
- make GitHub release asset downloads use `curl -fSsL` so curl progress meters do not pollute runtime deployment errors
- add regression coverage that pack-agent deploy scripts use silent curl for GitHub release assets

## Testing
- `cd services/claw-interface && /Users/a-q/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python -m pytest tests/unit/test_openclaw_agents.py -q -k 'deploy_agent_pack or archive_download_script_supports_redirects or archive_deploy_script'` — 3 passed, 126 deselected
- `cd services/claw-interface && /Users/a-q/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python -m pytest tests/unit/test_openclaw_agents.py::TestDeployAgentPack -q` — 6 passed
- `cd services/claw-interface && /Users/a-q/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python -m pytest tests/unit/test_openclaw_agents.py -q` — 129 passed
- `cd services/claw-interface && /Users/a-q/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python -m ruff check app/services/openclaw/agent_archive_deploy_script.py tests/unit/test_openclaw_agents.py` — passed
- `cd services/claw-interface && /Users/a-q/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python -m ruff format --check app/services/openclaw/agent_archive_deploy_script.py tests/unit/test_openclaw_agents.py` — passed
- `cd services/claw-interface && /Users/a-q/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python -m compileall -q app/services/openclaw/agent_archive_deploy_script.py tests/unit/test_openclaw_agents.py` — passed
- `cd services/claw-interface && LITELLM_PROXY_API_KEY=test-key /Users/a-q/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python -m pytest tests/unit -q` — 3618 passed, 2 failed in existing deptry gate (`tests/unit/test_ci_lint_deptry.py`) because local dependency config reports pre-existing DEP001 issues such as `bson` imports; no failures in modified code path


---

## [6] fix(web): guard login modal after auth (#1885)
- **SHA**: `d4ca757a336ebff479e506bc75d7a4fbfa8290d6`
- **作者**: tim-srp
- **日期**: 2026-05-24T10:36:39Z
- **PR**: #1885

### 完整 Commit Message

```
fix(web): guard login modal after auth (#1885)

## Summary
- Prevent the global login modal from opening after auth state is
already logged in
- Close any open login modal when `auth-state-changed` reports a
logged-in user
- Add regression coverage for both post-auth modal paths

## Verification
- `pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/components/LoginCheckProvider.unit.spec.tsx`
- `pnpm --dir web/app exec eslint
src/components/providers/LoginCheckProvider.tsx
tests/unit/components/LoginCheckProvider.unit.spec.tsx --quiet`
- `pnpm --dir web run lint`
- `pnpm --dir web/app exec tsc --noEmit`
- `pnpm --dir web run test:unit`

Note: `pnpm --dir web run tsc` currently fails before TypeScript starts
because the workspace script invokes `pnpm ... --if-present exec`, which
this local pnpm 10.26.2 rejects as `Unknown option: if-present`. I ran
the app-level `tsc --noEmit` check directly instead.


## Linear
- ECA-800:
https://linear.app/srpone/issue/ECA-800/bug-手机验证码登录后重复出现验证码输入框并进入-unable-to-connect-页面
```

### PR Description

## Summary
- Prevent the global login modal from opening after auth state is already logged in
- Close any open login modal when `auth-state-changed` reports a logged-in user
- Add regression coverage for both post-auth modal paths

## Verification
- `pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/components/LoginCheckProvider.unit.spec.tsx`
- `pnpm --dir web/app exec eslint src/components/providers/LoginCheckProvider.tsx tests/unit/components/LoginCheckProvider.unit.spec.tsx --quiet`
- `pnpm --dir web run lint`
- `pnpm --dir web/app exec tsc --noEmit`
- `pnpm --dir web run test:unit`

Note: `pnpm --dir web run tsc` currently fails before TypeScript starts because the workspace script invokes `pnpm ... --if-present exec`, which this local pnpm 10.26.2 rejects as `Unknown option: if-present`. I ran the app-level `tsc --noEmit` check directly instead.


## Linear
- ECA-800: https://linear.app/srpone/issue/ECA-800/bug-手机验证码登录后重复出现验证码输入框并进入-unable-to-connect-页面


---

## [7] fix(claw-interface): avoid pre-claim warm-pool accounts (#1886)
- **SHA**: `403b36ce4c837bb2d959000d7f49d17d9f8d0618`
- **作者**: tim-srp
- **日期**: 2026-05-24T07:21:32Z
- **PR**: #1886

### 完整 Commit Message

```
fix(claw-interface): avoid pre-claim warm-pool accounts (#1886)

## Summary
- stop warm-pool provisioning from creating local ecap-account
placeholder docs before claim
- finalize warm-pool registration before normal /users/create upsert and
create the real account from warm-pool assets at claim time
- document Phase 4 no-preclaim-account behavior and add regression
coverage

## Tests
- ruff format --check app tests/unit/test_warm_pool.py
tests/unit/test_warm_pool_provisioning_assets.py
tests/unit/test_warm_pool_materialization.py
- ruff check app tests/unit/test_warm_pool.py
tests/unit/test_warm_pool_provisioning_assets.py
tests/unit/test_warm_pool_materialization.py
- pytest -W ignore::PendingDeprecationWarning
services/claw-interface/tests/unit/test_warm_pool.py
services/claw-interface/tests/unit/test_warm_pool_provisioning_assets.py
services/claw-interface/tests/unit/test_warm_pool_materialization.py -q
- pytest -W ignore::PendingDeprecationWarning
services/claw-interface/tests/unit/test_user_routes_coverage.py
services/claw-interface/tests/unit/test_invite_codes.py -q

## Notes
- local pyright could not run in this shell because the local
environment lacks project deps and uv fails to build the project from
the existing git URL dependency; CI remains the source of truth for
pyright.
```

### PR Description

## Summary
- stop warm-pool provisioning from creating local ecap-account placeholder docs before claim
- finalize warm-pool registration before normal /users/create upsert and create the real account from warm-pool assets at claim time
- document Phase 4 no-preclaim-account behavior and add regression coverage

## Tests
- ruff format --check app tests/unit/test_warm_pool.py tests/unit/test_warm_pool_provisioning_assets.py tests/unit/test_warm_pool_materialization.py
- ruff check app tests/unit/test_warm_pool.py tests/unit/test_warm_pool_provisioning_assets.py tests/unit/test_warm_pool_materialization.py
- pytest -W ignore::PendingDeprecationWarning services/claw-interface/tests/unit/test_warm_pool.py services/claw-interface/tests/unit/test_warm_pool_provisioning_assets.py services/claw-interface/tests/unit/test_warm_pool_materialization.py -q
- pytest -W ignore::PendingDeprecationWarning services/claw-interface/tests/unit/test_user_routes_coverage.py services/claw-interface/tests/unit/test_invite_codes.py -q

## Notes
- local pyright could not run in this shell because the local environment lacks project deps and uv fails to build the project from the existing git URL dependency; CI remains the source of truth for pyright.

---

## [8] feat(enterprise-admin): add action toasts (#1891)
- **SHA**: `42a4b8d0eaba070c06c5a22a59badc098d567732`
- **作者**: bill-srp
- **日期**: 2026-05-24T05:32:05Z
- **PR**: #1891

### 完整 Commit Message

```
feat(enterprise-admin): add action toasts (#1891)

Linear:
https://linear.app/srpone/issue/ECA-763/admin-console-web-phase-1-packs-module

Summary:
- Hide Org Settings from enterprise admin desktop and mobile navigation
for now.
- Add a global Sonner toaster to enterprise admin.
- Show success/error toasts for invite, user actions, pack
review/deprecate, pack creation, version submission, and org-settings
save flows.

Test plan:
- pnpm --dir web run lint
- pnpm --dir web run test:unit
- pnpm --dir web run tsc (known root script failure: pnpm exec does not
support --if-present)
- pnpm --dir web --filter @zooclaw/web-app exec tsc --noEmit
- pnpm --dir web --filter @zooclaw/enterprise-admin exec tsc --noEmit
- pnpm --dir web --filter @zooclaw/auth-client exec tsc --noEmit
```

### PR Description

Linear: https://linear.app/srpone/issue/ECA-763/admin-console-web-phase-1-packs-module

Summary:
- Hide Org Settings from enterprise admin desktop and mobile navigation for now.
- Add a global Sonner toaster to enterprise admin.
- Show success/error toasts for invite, user actions, pack review/deprecate, pack creation, version submission, and org-settings save flows.

Test plan:
- pnpm --dir web run lint
- pnpm --dir web run test:unit
- pnpm --dir web run tsc (known root script failure: pnpm exec does not support --if-present)
- pnpm --dir web --filter @zooclaw/web-app exec tsc --noEmit
- pnpm --dir web --filter @zooclaw/enterprise-admin exec tsc --noEmit
- pnpm --dir web --filter @zooclaw/auth-client exec tsc --noEmit

---

## [9] feat(enterprise-admin): add pack version submissions (#1890)
- **SHA**: `1495a949ad9834456c3e1f812e79dc7c210ad543`
- **作者**: bill-srp
- **日期**: 2026-05-24T04:30:52Z
- **PR**: #1890

### 完整 Commit Message

```
feat(enterprise-admin): add pack version submissions (#1890)

## Summary
- add Submit new version flow on pack detail pages
- allow resubmission when rejected packs have no current pending
submission
- let admins choose a reviewed parent version and review the submitted
version label

## Stack
1. #1888: core pack API/list/review wiring
2. #1889: add pack creation and upload form
3. This PR: add new-version submission flow

## Linear

https://linear.app/srpone/issue/ECA-763/admin-console-web-phase-1-packs-module

## Tests
- pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit
- pnpm --filter @zooclaw/enterprise-admin exec vitest run --config
./vitest.config.mts focused pack suite
- pnpm --filter @zooclaw/enterprise-admin lint
```

### PR Description

## Summary
- add Submit new version flow on pack detail pages
- allow resubmission when rejected packs have no current pending submission
- let admins choose a reviewed parent version and review the submitted version label

## Stack
1. #1888: core pack API/list/review wiring
2. #1889: add pack creation and upload form
3. This PR: add new-version submission flow

## Linear
https://linear.app/srpone/issue/ECA-763/admin-console-web-phase-1-packs-module

## Tests
- pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit
- pnpm --filter @zooclaw/enterprise-admin exec vitest run --config ./vitest.config.mts focused pack suite
- pnpm --filter @zooclaw/enterprise-admin lint

---

## [10] feat(enterprise-admin): add pack creation uploads (#1889)
- **SHA**: `a8d8e4a0bf2684202b6b14149cac42d5aa789d10`
- **作者**: bill-srp
- **日期**: 2026-05-24T04:19:01Z
- **PR**: #1889

### 完整 Commit Message

```
feat(enterprise-admin): add pack creation uploads (#1889)

## Summary
- add Add pack dialog on the enterprise-admin packs page
- upload pack ZIPs through R2 and create org packs with returned asset
IDs
- support local/test manual asset ID creation and optional avatar upload

## Stack
1. #1888: core pack API/list/review wiring
2. This PR: add pack creation and upload form
3. feat/enterprise-admin-pack-versions: add new-version submission flow

## Linear

https://linear.app/srpone/issue/ECA-763/admin-console-web-phase-1-packs-module

## Tests
- pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit
- pnpm --filter @zooclaw/enterprise-admin exec vitest run --config
./vitest.config.mts focused pack suite
- pnpm --filter @zooclaw/enterprise-admin lint
```

### PR Description

## Summary
- add Add pack dialog on the enterprise-admin packs page
- upload pack ZIPs through R2 and create org packs with returned asset IDs
- support local/test manual asset ID creation and optional avatar upload

## Stack
1. #1888: core pack API/list/review wiring
2. This PR: add pack creation and upload form
3. feat/enterprise-admin-pack-versions: add new-version submission flow

## Linear
https://linear.app/srpone/issue/ECA-763/admin-console-web-phase-1-packs-module

## Tests
- pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit
- pnpm --filter @zooclaw/enterprise-admin exec vitest run --config ./vitest.config.mts focused pack suite
- pnpm --filter @zooclaw/enterprise-admin lint

---

## [11] feat(enterprise-admin): wire org pack review API (#1888)
- **SHA**: `dee8f0c28bcfd9c8b166d90b7ee921aa6e848eb7`
- **作者**: bill-srp
- **日期**: 2026-05-24T04:06:33Z
- **PR**: #1888

### 完整 Commit Message

```
feat(enterprise-admin): wire org pack review API (#1888)

## Summary
- wire enterprise-admin packs list/detail/review/deprecate UI to org
pack APIs
- restore responsive tabs and page size controls
- refine pack list request behavior and review panel focus styling

## Stack
1. This PR: core pack API/list/review wiring
2. feat/enterprise-admin-pack-create: add pack creation and upload form
3. feat/enterprise-admin-pack-versions: add new-version submission flow

## Linear

https://linear.app/srpone/issue/ECA-763/admin-console-web-phase-1-packs-module

## Tests
- pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit
- pnpm --filter @zooclaw/enterprise-admin exec vitest run --config
./vitest.config.mts focused pack suite
- pnpm --filter @zooclaw/enterprise-admin lint
```

### PR Description

## Summary
- wire enterprise-admin packs list/detail/review/deprecate UI to org pack APIs
- restore responsive tabs and page size controls
- refine pack list request behavior and review panel focus styling

## Stack
1. This PR: core pack API/list/review wiring
2. feat/enterprise-admin-pack-create: add pack creation and upload form
3. feat/enterprise-admin-pack-versions: add new-version submission flow

## Linear
https://linear.app/srpone/issue/ECA-763/admin-console-web-phase-1-packs-module

## Tests
- pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit
- pnpm --filter @zooclaw/enterprise-admin exec vitest run --config ./vitest.config.mts focused pack suite
- pnpm --filter @zooclaw/enterprise-admin lint

---

## [12] fix(claw-interface): finalize warm-pool materialization (#1882)
- **SHA**: `3c607dd72b2b9cf95d614272fc6c1525e862cf21`
- **作者**: tim-srp
- **日期**: 2026-05-24T02:49:32Z
- **PR**: #1882

### 完整 Commit Message

```
fix(claw-interface): finalize warm-pool materialization (#1882)

## Summary
- add warm-pool registration materialization/finalization with finalize
lease ownership and refresh
- claim warm-pool assets only after account materialization completes,
using `materialized -> claimed`
- fix `/users/create` warm-pool semantics so only actual finalization
reports `created=true`, while nonclaimable/unfinalized entries fall back
to normal existing-user initialization
- add focused unit coverage for finalize idempotency, asset repair,
lease contention, and route responses

## Verification
- `.venv/bin/pytest tests/unit/test_warm_pool.py
tests/unit/test_warm_pool_additional_coverage.py
tests/unit/test_warm_pool_assets_repo.py
tests/unit/test_warm_pool_materialization.py` → `42 passed in 2.87s`
- `.venv/bin/ruff check .` → `All checks passed!`
- `.venv/bin/ruff format --check .` → `559 files already formatted`
- `.venv/bin/pyright --pythonpath .venv/bin/python app/ tests/` → `0
errors, 0 warnings, 0 informations`
- `git diff --check` → passed

## Notes
- Rebased onto latest `origin/main` (`1943aaa02`) before commit.
- Daily registration remains the simple CAS-before-Redis-increment path;
no persisted exemption replay complexity added.

---------

Co-authored-by: A-Q <a-q@A-QdeMac-mini.local>
```

### PR Description

## Summary
- add warm-pool registration materialization/finalization with finalize lease ownership and refresh
- claim warm-pool assets only after account materialization completes, using `materialized -> claimed`
- fix `/users/create` warm-pool semantics so only actual finalization reports `created=true`, while nonclaimable/unfinalized entries fall back to normal existing-user initialization
- add focused unit coverage for finalize idempotency, asset repair, lease contention, and route responses

## Verification
- `.venv/bin/pytest tests/unit/test_warm_pool.py tests/unit/test_warm_pool_additional_coverage.py tests/unit/test_warm_pool_assets_repo.py tests/unit/test_warm_pool_materialization.py` → `42 passed in 2.87s`
- `.venv/bin/ruff check .` → `All checks passed!`
- `.venv/bin/ruff format --check .` → `559 files already formatted`
- `.venv/bin/pyright --pythonpath .venv/bin/python app/ tests/` → `0 errors, 0 warnings, 0 informations`
- `git diff --check` → passed

## Notes
- Rebased onto latest `origin/main` (`1943aaa02`) before commit.
- Daily registration remains the simple CAS-before-Redis-increment path; no persisted exemption replay complexity added.


---

