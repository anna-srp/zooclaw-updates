# ecap-workspace — 2026-07-02 commits

## feat(agent-packs): add paid purchase frontend (#2713)

- **SHA**: 06b48d34d16a134baf0629a2a0b0d8bf452128a1
- **作者**: bill-srp
- **日期**: 2026-07-02T15:41:31Z
- **PR**: #2713

### Commit Message

```
feat(agent-packs): add paid purchase frontend (#2713)

## Summary
- Wire Agent Manager to load the current user's purchased paid packs on
page entry.
- Switch paid agent cards between Purchase and the normal
install/uninstall actions after purchase is confirmed.
- Add Stripe checkout popup handling, cancel handling, manual Paid
confirmation, success-url auto-install, and targeted paid-pack UI tests.

## Split rollout
- Stacked on backend PR #2712 (`codex/agent-pack-purchase-backend`).
- Backend PR #2712 must merge and deploy before this frontend PR is
merged/deployed.
- This frontend intentionally does not include a
`/agent-packs/purchases` 404 fallback; the backend endpoint is treated
as required.

## Test plan
- [x] `git diff --check codex/agent-pack-purchase-backend...HEAD`
- [ ] `pnpm --dir web/app exec vitest run
tests/unit/app/agents-manager/useViewModel.unit.spec.tsx
tests/unit/hooks/usePurchasedAgentPacks.unit.spec.ts
tests/unit/services/agent-packs.unit.spec.ts
tests/unit/app/agents-manager/AgentCard.unit.spec.tsx
tests/unit/hooks/useAgentActions.unit.spec.ts` blocked locally by
`ERR_PNPM_MISSING_TARBALL_INTEGRITY` for
`xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`
```

### PR Body

## Summary
- Wire Agent Manager to load the current user's purchased paid packs on page entry.
- Switch paid agent cards between Purchase and the normal install/uninstall actions after purchase is confirmed.
- Add Stripe checkout popup handling, cancel handling, manual Paid confirmation, success-url auto-install, and targeted paid-pack UI tests.

## Split rollout
- Stacked on backend PR #2712 (`codex/agent-pack-purchase-backend`).
- Backend PR #2712 must merge and deploy before this frontend PR is merged/deployed.
- This frontend intentionally does not include a `/agent-packs/purchases` 404 fallback; the backend endpoint is treated as required.

## Test plan
- [x] `git diff --check codex/agent-pack-purchase-backend...HEAD`
- [ ] `pnpm --dir web/app exec vitest run tests/unit/app/agents-manager/useViewModel.unit.spec.tsx tests/unit/hooks/usePurchasedAgentPacks.unit.spec.ts tests/unit/services/agent-packs.unit.spec.ts tests/unit/app/agents-manager/AgentCard.unit.spec.tsx tests/unit/hooks/useAgentActions.unit.spec.ts` blocked locally by `ERR_PNPM_MISSING_TARBALL_INTEGRITY` for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`


---

## docs(review): calibrate review severity guidance (#2714)

- **SHA**: e163a56e4e252b0186e68f030e1cd1d56c49d339
- **作者**: bill-srp
- **日期**: 2026-07-02T14:59:59Z
- **PR**: #2714

### Commit Message

```
docs(review): calibrate review severity guidance (#2714)

## Summary

- Calibrate `code-review.md` severity guidance so recurring bug classes
are treated as a priority checklist, not automatic blockers.
- Require `REQUEST_CHANGES` findings to include PR ownership, a concrete
trigger, and severe runtime impact.
- Route unclear ownership/state/fallback-contract readability or
duplication concerns to `NEED_HUMAN_REVIEW`, while leaving pure polish
as non-blocking notes.

## Testing

- Not run; documentation-only change.
```

### PR Body

## Summary

- Calibrate `code-review.md` severity guidance so recurring bug classes are treated as a priority checklist, not automatic blockers.
- Require `REQUEST_CHANGES` findings to include PR ownership, a concrete trigger, and severe runtime impact.
- Route unclear ownership/state/fallback-contract readability or duplication concerns to `NEED_HUMAN_REVIEW`, while leaving pure polish as non-blocking notes.

## Testing

- Not run; documentation-only change.


---

## feat(agent-packs): add paid purchase backend (#2712)

- **SHA**: 1646ea5c97f55dd9ce56599faa093bab2726e622
- **作者**: bill-srp
- **日期**: 2026-07-02T13:41:50Z
- **PR**: #2712

### Commit Message

```
feat(agent-packs): add paid purchase backend (#2712)

## Summary
- Add the current-user purchased pack listing endpoint for Agent
Manager.
- Validate each returned pack through the active ECAP pack purchase
agreement contract.
- Harden paid pack checkout resume/retry behavior for pending,
paid-but-reconciling, stale, and invalid Stripe sessions.

## Split rollout
- Backend-only PR. Merge and deploy this before the frontend purchase UI
PR.
- The frontend PR should no longer need a `/agent-packs/purchases` 404
fallback once this is live.

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH python -m pytest
services/claw-interface/tests/unit/test_public_agent_packs_routes.py
services/claw-interface/tests/unit/test_ecap_pack_subscription_service.py
services/claw-interface/tests/unit/test_billing_v2_repos.py
services/claw-interface/tests/unit/test_pack_purchase_repo.py -q`
- [x] `git diff --check`
```

### PR Body

## Summary
- Add the current-user purchased pack listing endpoint for Agent Manager.
- Validate each returned pack through the active ECAP pack purchase agreement contract.
- Harden paid pack checkout resume/retry behavior for pending, paid-but-reconciling, stale, and invalid Stripe sessions.

## Split rollout
- Backend-only PR. Merge and deploy this before the frontend purchase UI PR.
- The frontend PR should no longer need a `/agent-packs/purchases` 404 fallback once this is live.

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH python -m pytest services/claw-interface/tests/unit/test_public_agent_packs_routes.py services/claw-interface/tests/unit/test_ecap_pack_subscription_service.py services/claw-interface/tests/unit/test_billing_v2_repos.py services/claw-interface/tests/unit/test_pack_purchase_repo.py -q`
- [x] `git diff --check`


---

## fix(auth): repair orgless accounts via org endpoint (#2710)

- **SHA**: 20e6f8270c48c6efcfacdadafa85d6e83c8ed50f
- **作者**: bill-srp
- **日期**: 2026-07-02T12:37:23Z
- **PR**: #2710

### Commit Message

```
fix(auth): repair orgless accounts via org endpoint (#2710)

## Summary
- Repair existing webapp accounts with `org: null` through the dedicated
personal-org endpoint.
- Keep new-account bootstrap on `/account/personal-org`; only existing
orgless accounts use `/orgs/personal`.

## Root cause
The webapp treated both `account.not_found` and `200 + org: null` as the
same bootstrap case, so existing accounts missing org membership retried
`/account/personal-org`. That endpoint is for account registration plus
personal-org creation and rejects already existing accounts.

## Test plan
- [x] `git diff --check`
- [x] Backend smoke for existing org route behavior:
`/Users/bill/.venvs/claw-interface/bin/pytest
services/claw-interface/tests/unit/test_routes_account.py::TestRegisterHandler::test_personal_org_route_creates_personal_org
services/claw-interface/tests/unit/test_routes_account.py::TestRegisterHandler::test_personal_org_route_returns_existing_membership
-q`
- [ ] Frontend Vitest/tsc/eslint could not run locally: `pnpm` is
blocked by `ERR_PNPM_MISSING_TARBALL_INTEGRITY` for
`xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`, and local
`node_modules/.bin/{vitest,tsc,eslint}` point at missing packages.
```

### PR Body

## Summary
- Repair existing webapp accounts with `org: null` through the dedicated personal-org endpoint.
- Keep new-account bootstrap on `/account/personal-org`; only existing orgless accounts use `/orgs/personal`.

## Root cause
The webapp treated both `account.not_found` and `200 + org: null` as the same bootstrap case, so existing accounts missing org membership retried `/account/personal-org`. That endpoint is for account registration plus personal-org creation and rejects already existing accounts.

## Test plan
- [x] `git diff --check`
- [x] Backend smoke for existing org route behavior: `/Users/bill/.venvs/claw-interface/bin/pytest services/claw-interface/tests/unit/test_routes_account.py::TestRegisterHandler::test_personal_org_route_creates_personal_org services/claw-interface/tests/unit/test_routes_account.py::TestRegisterHandler::test_personal_org_route_returns_existing_membership -q`
- [ ] Frontend Vitest/tsc/eslint could not run locally: `pnpm` is blocked by `ERR_PNPM_MISSING_TARBALL_INTEGRITY` for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`, and local `node_modules/.bin/{vitest,tsc,eslint}` point at missing packages.


---

## style(sidenav): polish homepage sidebar glass UI (#2709)

- **SHA**: 666159d7bb5f78912e4b11d2f718042b2975f927
- **作者**: lynn Zhuang
- **日期**: 2026-07-02T11:13:49Z
- **PR**: #2709

### Commit Message

```
style(sidenav): polish homepage sidebar glass UI (#2709)

## Summary
- Polish the homepage sidenav glass surface, nav row active states, logo
treatment, agent row density, and profile card styling.
- Move raw glass gradients into CSS modules so JSX stays within lint
rules and dark glass states avoid bright white blocks.
- Preserve visible keyboard focus states, keep the profile card styled
on non-glass app routes, and remove the now-unused legacy wordmark
export.
- Add a null-pathname guard in `PublicHeader` so the global TypeScript
check passes with current Next types.

## Test plan
- [x] `CI=true
PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin bash
scripts/verify-web.sh web/app/src/components/UserCard.tsx
web/app/src/components/UserCard.module.css
web/app/src/components/sidenav/NavItemComponent.tsx
web/app/src/components/sidenav/NavItemComponent.module.css
web/app/src/components/sidenav/SideNav.tsx
web/app/src/components/sidenav/SideNav.module.css
web/app/src/components/sidenav/SideNavAgentList.tsx
web/app/src/components/sidenav/SideNavAgentRow.tsx
web/app/src/components/sidenav/SideNavAgentSessions.tsx
web/app/src/components/sidenav/SideNavAgentSessions.module.css
web/app/src/components/sidenav/SideNavLogo.tsx
web/app/src/components/sidenav/SideNavUserSection.tsx
web/app/src/components/sidenav/constants.ts
web/app/src/components/public/PublicHeader.tsx`
- [x] `CI=true
PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin pnpm
run lint:ci` from `web/app`

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
```

### PR Body

## Summary
- Polish the homepage sidenav glass surface, nav row active states, logo treatment, agent row density, and profile card styling.
- Move raw glass gradients into CSS modules so JSX stays within lint rules and dark glass states avoid bright white blocks.
- Preserve visible keyboard focus states, keep the profile card styled on non-glass app routes, and remove the now-unused legacy wordmark export.
- Add a null-pathname guard in `PublicHeader` so the global TypeScript check passes with current Next types.

## Test plan
- [x] `CI=true PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin bash scripts/verify-web.sh web/app/src/components/UserCard.tsx web/app/src/components/UserCard.module.css web/app/src/components/sidenav/NavItemComponent.tsx web/app/src/components/sidenav/NavItemComponent.module.css web/app/src/components/sidenav/SideNav.tsx web/app/src/components/sidenav/SideNav.module.css web/app/src/components/sidenav/SideNavAgentList.tsx web/app/src/components/sidenav/SideNavAgentRow.tsx web/app/src/components/sidenav/SideNavAgentSessions.tsx web/app/src/components/sidenav/SideNavAgentSessions.module.css web/app/src/components/sidenav/SideNavLogo.tsx web/app/src/components/sidenav/SideNavUserSection.tsx web/app/src/components/sidenav/constants.ts web/app/src/components/public/PublicHeader.tsx`
- [x] `CI=true PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin pnpm run lint:ci` from `web/app`


---

## fix(settings): deprecate legacy agent routes (#2705)

- **SHA**: 8071436a94f7421ceb368abddd39ad71dc81b78d
- **作者**: bill-srp
- **日期**: 2026-07-02T08:58:47Z
- **PR**: #2705

### Commit Message

```
fix(settings): deprecate legacy agent routes (#2705)

## Summary

- mark the legacy per-agent identity/model routes as deprecated
- keep identity-only updates working when the agent catalog is
temporarily unavailable

## Validation

- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH pytest
services/claw-interface/tests/unit/test_openclaw_settings_routes.py::test_per_agent_identity_and_model_routes_are_marked_deprecated
services/claw-interface/tests/unit/test_openclaw_settings_routes.py::TestUpdateAgentIdentityEndpoint
services/claw-interface/tests/unit/test_openclaw_settings_routes.py::TestAgentSettingsServiceRegressions::test_identity_update_skips_catalog_lookup_when_model_is_unchanged
-q`
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`
```

### PR Body

## Summary

- mark the legacy per-agent identity/model routes as deprecated
- keep identity-only updates working when the agent catalog is temporarily unavailable

## Validation

- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH pytest services/claw-interface/tests/unit/test_openclaw_settings_routes.py::test_per_agent_identity_and_model_routes_are_marked_deprecated services/claw-interface/tests/unit/test_openclaw_settings_routes.py::TestUpdateAgentIdentityEndpoint services/claw-interface/tests/unit/test_openclaw_settings_routes.py::TestAgentSettingsServiceRegressions::test_identity_update_skips_catalog_lookup_when_model_is_unchanged -q`
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`


---

## fix(auth): retry /api/auth/me on transport-layer failures (ECA-1154) (#2700)

- **SHA**: 3d071ab67b88aef7020f97ae83df2c3550dea3c6
- **作者**: siqiao-srp
- **日期**: 2026-07-02T08:22:23Z
- **PR**: #2700

### Commit Message

```
fix(auth): retry /api/auth/me on transport-layer failures (ECA-1154) (#2700)

<!-- PR 标题：fix(scope): description —— 必须遵循 Conventional Commits -->

Linear: https://linear.app/srpone/issue/ECA-1154

## Summary
- 在 `useAccountMeQuery` 的 retry predicate 里增加对**传输层失败**（Firefox
`TypeError: NetworkError when attempting to fetch resource`、Chrome
`TypeError: Failed to fetch`、`AbortError`）的识别，最多 3 次退避重试（500ms / 1500ms
/ 3000ms）。
- 原有的 404 `account.not_found` / 401 legacy `"Account not found, please
register"` 引导注册重试路径完全保留，不改动 delay 序列。
- 把 retry 判定和 delay 抽成命名函数（`shouldRetryAccountMeQuery` /
`accountMeRetryDelayMs`）并导出，让预判逻辑可直接单测。
- 新增 12 个单元断言覆盖：Firefox / Chrome / AbortError 三种传输层形态、重试上限 3、原有
bootstrap-pending 行为、真正的 401/403/5xx **不重试**、null/undefined
**不重试**、delay 槽位与上限。

## Root cause
ECA-1154 报障：Nemo 用 Firefox 152 (Linux) 打开 Zooclaw，`/api/auth/me` 在传输层直接抛
`TypeError: NetworkError`（无 HTTP status），`useAccountMeQuery` 的旧 retry 谓词
`isAccountBootstrapPendingError` 只识别 `ApiError` 且 status ∈ {404,
401}，所以传输层错误 **一次都不重试**，直接落到 `AccountSessionGate` 非 auth-error 分支 →
用户看到「Unable to verify your session」黑屏，只能手动 Retry。Firefox 报此错的一秒稳定复现 =
Firefox 对短暂网络中断 / 边缘策略变化的容错比 Chrome 更严格；本次不定位 Firefox-only 的具体触发源（可能是
Cloudflare Worker / CORS / SameSite），先修补客户端容错。

## Test plan
- [x] `bash scripts/verify-web.sh src/hooks/queries/useAccountMeQuery.ts
tests/unit/hooks/queries/useAccountMeQuery.unit.spec.ts` — 8 guards +
tsc + vitest (12/12) + eslint 全绿
- [ ] CI `code-quality / lint-and-test` 全绿
- [ ] 手动验证（合并到 staging 后，Firefox 152）：DevTools Network → Offline 快速开关
1-2 秒，模拟传输层瞬时失败；会话验证应在 3 次退避内自愈，不再落到手动 Retry 页
- [ ] 回归：真实 401（token 过期）仍应触发 `router.replace('/')`，不进入重试循环

## Out of scope（避免和 ticket 二次误诊）
- Ticket 的「结论二」（bot pod `openclaw.sqlite` init WARN）**不在本 PR 内**。经诊断为
`openclaw-docker` PR #152 (`fix(litestream): per-version configs to stop
benign db-init-timeout noise`) 已明确定性为**良性日志噪声**，是 stale image 上残留的
litestream config 引用（Nemo 的 bot 目前在 `2026.5.7.63`，`Up to date:
false`；已单独 restart 验证过 bot 功能正常）。本 PR 只修真正影响用户可见的前端容错缺陷。
- 未额外调整 `AccountSessionGate.tsx`。原来的 manual Retry 按钮作为「3
次自动重试仍失败」的兜底继续存在，UX 语义合理，不做扩大化改动。
```

### PR Body

<!-- PR 标题：fix(scope): description —— 必须遵循 Conventional Commits -->

Linear: https://linear.app/srpone/issue/ECA-1154

## Summary
- 在 `useAccountMeQuery` 的 retry predicate 里增加对**传输层失败**（Firefox `TypeError: NetworkError when attempting to fetch resource`、Chrome `TypeError: Failed to fetch`、`AbortError`）的识别，最多 3 次退避重试（500ms / 1500ms / 3000ms）。
- 原有的 404 `account.not_found` / 401 legacy `"Account not found, please register"` 引导注册重试路径完全保留，不改动 delay 序列。
- 把 retry 判定和 delay 抽成命名函数（`shouldRetryAccountMeQuery` / `accountMeRetryDelayMs`）并导出，让预判逻辑可直接单测。
- 新增 12 个单元断言覆盖：Firefox / Chrome / AbortError 三种传输层形态、重试上限 3、原有 bootstrap-pending 行为、真正的 401/403/5xx **不重试**、null/undefined **不重试**、delay 槽位与上限。

## Root cause
ECA-1154 报障：Nemo 用 Firefox 152 (Linux) 打开 Zooclaw，`/api/auth/me` 在传输层直接抛 `TypeError: NetworkError`（无 HTTP status），`useAccountMeQuery` 的旧 retry 谓词 `isAccountBootstrapPendingError` 只识别 `ApiError` 且 status ∈ {404, 401}，所以传输层错误 **一次都不重试**，直接落到 `AccountSessionGate` 非 auth-error 分支 → 用户看到「Unable to verify your session」黑屏，只能手动 Retry。Firefox 报此错的一秒稳定复现 = Firefox 对短暂网络中断 / 边缘策略变化的容错比 Chrome 更严格；本次不定位 Firefox-only 的具体触发源（可能是 Cloudflare Worker / CORS / SameSite），先修补客户端容错。

## Test plan
- [x] `bash scripts/verify-web.sh src/hooks/queries/useAccountMeQuery.ts tests/unit/hooks/queries/useAccountMeQuery.unit.spec.ts` — 8 guards + tsc + vitest (12/12) + eslint 全绿
- [ ] CI `code-quality / lint-and-test` 全绿
- [ ] 手动验证（合并到 staging 后，Firefox 152）：DevTools Network → Offline 快速开关 1-2 秒，模拟传输层瞬时失败；会话验证应在 3 次退避内自愈，不再落到手动 Retry 页
- [ ] 回归：真实 401（token 过期）仍应触发 `router.replace('/')`，不进入重试循环

## Out of scope（避免和 ticket 二次误诊）
- Ticket 的「结论二」（bot pod `openclaw.sqlite` init WARN）**不在本 PR 内**。经诊断为 `openclaw-docker` PR #152 (`fix(litestream): per-version configs to stop benign db-init-timeout noise`) 已明确定性为**良性日志噪声**，是 stale image 上残留的 litestream config 引用（Nemo 的 bot 目前在 `2026.5.7.63`，`Up to date: false`；已单独 restart 验证过 bot 功能正常）。本 PR 只修真正影响用户可见的前端容错缺陷。
- 未额外调整 `AccountSessionGate.tsx`。原来的 manual Retry 按钮作为「3 次自动重试仍失败」的兜底继续存在，UX 语义合理，不做扩大化改动。


---

## feat(bossclaw): use the new navy ZooClaw app icon for tiles & favicon (#2703)

- **SHA**: 362fa642d9a960b5b84a2f16fb410f78a599516f
- **作者**: david-srp
- **日期**: 2026-07-02T07:39:18Z
- **PR**: #2703

### Commit Message

```
feat(bossclaw): use the new navy ZooClaw app icon for tiles & favicon (#2703)

## What

Refresh the bossclaw campaign's **square app icon + favicon** to the new
**navy gold-claw ZooClaw mark**, replacing the old gold-chip +
white-claw composite and the gold app-icon favicon.

## Changes

- **New asset** `public/bossclaw/appicon.png` (192×192, ~12 KB,
pngquant-optimized) — one shared brand mark for every square-icon
surface.
- **On-page tiles** (Preloader loading mark, Done-card avatar, WeChat
QR-center badge) now point at `appicon.png` and render **full-bleed**
(`object-fit: cover` + `border-radius: inherit`); their chips drop the
now-covered gold gradient and the dead flex-centering.
- **Favicon + apple-touch icon** (`page.tsx` metadata) → `appicon.png`.
- **Removed** the two superseded assets (`claw-appicon-white.png`,
`favicon.png`); no references remain.

## Scope

Frontend-only, and **scoped strictly to the app icon / favicon** — no
greeting, flow, copy, or backend changes. (This is the standalone logo
half extracted from the earlier combined PR.)

## Testing

- `bash scripts/verify-web.sh 'web/app/src/app/[locale]/bossclaw'` —
guards + vitest + eslint green; the bossclaw sources are tsc-clean.
- Rendered at mobile size (previously verified): the navy tile shows
correctly in the preloader and done-card, gold claw legible against the
dark page.

> Note: a local `tsc` run flags a pre-existing, unrelated error in
`src/components/public/PublicHeader.tsx` (a node_modules resolution
quirk after a branch switch; `usePathname` is `string`). It does not
reproduce in CI — current main passes `web-quality / lint-and-typecheck`
— and this PR does not touch that file.

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
```

### PR Body

## What

Refresh the bossclaw campaign's **square app icon + favicon** to the new **navy gold-claw ZooClaw mark**, replacing the old gold-chip + white-claw composite and the gold app-icon favicon.

## Changes

- **New asset** `public/bossclaw/appicon.png` (192×192, ~12 KB, pngquant-optimized) — one shared brand mark for every square-icon surface.
- **On-page tiles** (Preloader loading mark, Done-card avatar, WeChat QR-center badge) now point at `appicon.png` and render **full-bleed** (`object-fit: cover` + `border-radius: inherit`); their chips drop the now-covered gold gradient and the dead flex-centering.
- **Favicon + apple-touch icon** (`page.tsx` metadata) → `appicon.png`.
- **Removed** the two superseded assets (`claw-appicon-white.png`, `favicon.png`); no references remain.

## Scope

Frontend-only, and **scoped strictly to the app icon / favicon** — no greeting, flow, copy, or backend changes. (This is the standalone logo half extracted from the earlier combined PR.)

## Testing

- `bash scripts/verify-web.sh 'web/app/src/app/[locale]/bossclaw'` — guards + vitest + eslint green; the bossclaw sources are tsc-clean.
- Rendered at mobile size (previously verified): the navy tile shows correctly in the preloader and done-card, gold claw legible against the dark page.

> Note: a local `tsc` run flags a pre-existing, unrelated error in `src/components/public/PublicHeader.tsx` (a node_modules resolution quirk after a branch switch; `usePathname` is `string`). It does not reproduce in CI — current main passes `web-quality / lint-and-typecheck` — and this PR does not touch that file.


---

## fix(desktop): restore Windows ZooClaw build compatibility (#2685)

- **SHA**: 49dd6a868605dbf9b45d3e118d96b209523a02d4
- **作者**: zayne-srp
- **日期**: 2026-07-02T06:33:08Z
- **PR**: #2685

### Commit Message

```
fix(desktop): restore Windows ZooClaw build compatibility (#2685)

## Summary
- restore cross-platform shell command handling for OpenClaw node
commands
- rebrand the desktop package to ZooClaw and update desktop
icons/protocol metadata
- retry desktop window loading and log packaged Next server output to
aid Windows white-screen diagnosis
- report the real desktop platform in OpenClaw connect instead of
hardcoding darwin

## Verification
- Cherry-picked the four Windows/ZooClaw desktop commits onto the latest
origin/main
- Ran git diff --check successfully
- The corresponding zooclaw-desktop CI run 28360651111 succeeded and
produced a valid ZooClaw Setup 0.1.0.exe artifact from the previous
branch head

## Notes
- Local typecheck was not run in the temporary worktree because
desktop/node_modules is not installed there
- Follow-up zooclaw-desktop PR should point its ecap-workspace submodule
at this PR branch head

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary
- restore cross-platform shell command handling for OpenClaw node commands
- rebrand the desktop package to ZooClaw and update desktop icons/protocol metadata
- retry desktop window loading and log packaged Next server output to aid Windows white-screen diagnosis
- report the real desktop platform in OpenClaw connect instead of hardcoding darwin

## Verification
- Cherry-picked the four Windows/ZooClaw desktop commits onto the latest origin/main
- Ran git diff --check successfully
- The corresponding zooclaw-desktop CI run 28360651111 succeeded and produced a valid ZooClaw Setup 0.1.0.exe artifact from the previous branch head

## Notes
- Local typecheck was not run in the temporary worktree because desktop/node_modules is not installed there
- Follow-up zooclaw-desktop PR should point its ecap-workspace submodule at this PR branch head

---

## fix(agent-builder): show no-running-bot notice (#2699)

- **SHA**: 0879d1ff930b2ac26825747fc53d79b2eaab38e0
- **作者**: kaka-srp
- **日期**: 2026-07-02T06:16:46Z
- **PR**: #2699

### Commit Message

```
fix(agent-builder): show no-running-bot notice (#2699)

## Summary
- Show a clear Agent Builder notice when the builder workspace reports
`computer_not_ready` or `missing_computer`.
- Reuse the chat-page-style dormant wording for the no-running-Claw
state.
- Share the same workspace notice between the status pane and the Build
fallback card.

## Root cause
Agent Builder treated a non-running or missing Claw bot as a generic
preparing state, so users saw an indefinite workspace preparation
message instead of an actionable explanation.

## Test plan
- [x] `bash scripts/verify-web.sh
'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderClient.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderStatusPane.tsx'
web/app/src/locales/en.ts web/app/src/locales/zh.ts`
- [x] pre-push changed-surface check (`verify-web.sh --no-test` via
hook)
```

### PR Body

## Summary
- Show a clear Agent Builder notice when the builder workspace reports `computer_not_ready` or `missing_computer`.
- Reuse the chat-page-style dormant wording for the no-running-Claw state.
- Share the same workspace notice between the status pane and the Build fallback card.

## Root cause
Agent Builder treated a non-running or missing Claw bot as a generic preparing state, so users saw an indefinite workspace preparation message instead of an actionable explanation.

## Test plan
- [x] `bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderClient.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderStatusPane.tsx' web/app/src/locales/en.ts web/app/src/locales/zh.ts`
- [x] pre-push changed-surface check (`verify-web.sh --no-test` via hook)


---

## fix(agent-diagnostics): select live builder project candidates (#2698)

- **SHA**: 8f3e47256762d29cf883c6bab24a34a1b396d396
- **作者**: Chris@ZooClaw
- **日期**: 2026-07-02T04:37:57Z
- **PR**: #2698

### Commit Message

```
fix(agent-diagnostics): select live builder project candidates (#2698)

## Summary
- Prefer live Agent Builder projects when a builder computer maps to
multiple projects
- Fall back to the unique latest candidate before returning an ambiguous
lookup error
- Cover active/latest and failed-vs-live candidate selection in unit
tests

## Validation
- ruff check
services/claw-interface/app/services/agent_builder_lookup.py
services/claw-interface/tests/unit/test_agent_builder_diagnostics.py
- ruff format --check
services/claw-interface/app/services/agent_builder_lookup.py
services/claw-interface/tests/unit/test_agent_builder_diagnostics.py
- PYTHONPATH=services/claw-interface/app python -m pytest
services/claw-interface/tests/unit/test_agent_builder_diagnostics.py

Note: bash scripts/verify-py.sh was attempted, but this fresh worktree
has no installed claw-interface venv dependencies, so pyright reported
repository-wide missing imports. Targeted ruff and pytest passed.
```

### PR Body

## Summary
- Prefer live Agent Builder projects when a builder computer maps to multiple projects
- Fall back to the unique latest candidate before returning an ambiguous lookup error
- Cover active/latest and failed-vs-live candidate selection in unit tests

## Validation
- ruff check services/claw-interface/app/services/agent_builder_lookup.py services/claw-interface/tests/unit/test_agent_builder_diagnostics.py
- ruff format --check services/claw-interface/app/services/agent_builder_lookup.py services/claw-interface/tests/unit/test_agent_builder_diagnostics.py
- PYTHONPATH=services/claw-interface/app python -m pytest services/claw-interface/tests/unit/test_agent_builder_diagnostics.py

Note: bash scripts/verify-py.sh was attempted, but this fresh worktree has no installed claw-interface venv dependencies, so pyright reported repository-wide missing imports. Targeted ruff and pytest passed.

---

## feat(dashboard-console): add official pack submissions (#2683)

- **SHA**: 6ce9e697edf614469155ad43438ae59668a47edb
- **作者**: bill-srp
- **日期**: 2026-07-02T04:20:50Z
- **PR**: #2683

### Commit Message

```
feat(dashboard-console): add official pack submissions (#2683)

## Linear
N/A

## Summary
- Add dashboard-console official submissions page for SRP users to
submit their own private packs into the ZooClaw official review flow.
- Add internal backend source/submission/create APIs with source
ownership checks, R2 source-prefix validation, origin metadata, and
create/update target handling.
- Parse agent-pack archives in the dialog to prefill metadata, quick
commands, and avatar, then upload archive/avatar assets before creating
the official submission.
- Harden review semantics so update submissions persist pack name
metadata and approval syncs it onto the visible pack.

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH python -m pytest
services/claw-interface/tests/unit/test_official_pack_submission_service.py
services/claw-interface/tests/unit/test_internal_agent_packs_routes.py
services/claw-interface/tests/unit/test_pack_services.py
services/claw-interface/tests/unit/test_pack_store_txn_repo.py -q`
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-changed.sh`
- [x] `git diff --check origin/main..HEAD`
- [ ] dashboard-console focused Vitest could not run locally because
pnpm install stops before test execution with
`ERR_PNPM_MISSING_TARBALL_INTEGRITY` for
`xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`; CI remains
the source of truth for that frontend surface.

---------

Co-authored-by: claude[bot] <41898282+claude[bot]@users.noreply.github.com>
Co-authored-by: bill-srp <undefined@users.noreply.github.com>
```

### PR Body

## Linear
N/A

## Summary
- Add dashboard-console official submissions page for SRP users to submit their own private packs into the ZooClaw official review flow.
- Add internal backend source/submission/create APIs with source ownership checks, R2 source-prefix validation, origin metadata, and create/update target handling.
- Parse agent-pack archives in the dialog to prefill metadata, quick commands, and avatar, then upload archive/avatar assets before creating the official submission.
- Harden review semantics so update submissions persist pack name metadata and approval syncs it onto the visible pack.

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH python -m pytest services/claw-interface/tests/unit/test_official_pack_submission_service.py services/claw-interface/tests/unit/test_internal_agent_packs_routes.py services/claw-interface/tests/unit/test_pack_services.py services/claw-interface/tests/unit/test_pack_store_txn_repo.py -q`
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-changed.sh`
- [x] `git diff --check origin/main..HEAD`
- [ ] dashboard-console focused Vitest could not run locally because pnpm install stops before test execution with `ERR_PNPM_MISSING_TARBALL_INTEGRITY` for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`; CI remains the source of truth for that frontend surface.


---

## feat(enterprise-admin): rebrand sign-in surfaces to ZooWork and polish UI (#2614)

- **SHA**: 4221d7a93fe2bd53c634b106f29a72c726ae071c
- **作者**: shana-srp
- **日期**: 2026-07-02T04:20:40Z
- **PR**: #2614

### Commit Message

```
feat(enterprise-admin): rebrand sign-in surfaces to ZooWork and polish UI (#2614)

## Summary

Polishes and rebrands the **enterprise-admin** business sign-in surfaces
(`/login` + `/verify`) at `business.zooclaw.ai`, and rebrands
user-facing copy from **ZooClaw → ZooWork**.

Both auth screens now render through a single shared `BRAND_AUTH_SHELL`
config so they stay visually identical from one source of truth. `/join`
and the onboarding forms (which also use `AuthShell` / `OtpGrid`) are
intentionally **unchanged** — every new shell behavior is opt-in and
defaults off.

## What changed

**Visual polish (login + verify)**
- Staggered entrance animation (reuses the previously-unused
`login-reveal` keyframes), brand-red → **gray-black** input focus ring,
equal-height (48px) centered black/white primary CTA.
- Left hero now uses an editorial bronze photo (`login-hero-bg.webp`,
53KB) with a left+bottom legibility scrim so white text stays readable
over the artwork.
- Dark `#272420` page backdrop; white hero shield icon (only when a hero
photo is set).
- Form panel restructured: dropped the eyebrow + divider, sentence-case
bold field labels, and a "Talk to our team" contact line.
- All type on these surfaces is **Roboto** (scoped via a `.login-roboto`
rule + `next/font`).
- OTP underline fill is now a prop (`fillClassName`); verify passes
gray-black, `/join` keeps the default red.

**Rebrand (ZooClaw → ZooWork)**
- New white "ZOOWORK | BUSINESS" hero lockup + new favicon
(`favicon.png`).
- Page title → "ZooWork Enterprise Admin".
- Hero eyebrow/title/subtitle + "New to … Business?" + onboarding © +
Chinese catalog (`i18n-zh.ts`) updated to ZooWork.
- Hero headline reworded to "Orchestrate your entire digital workforce."
and the subtitle to a plain-language security line.

## Testing

- `pnpm exec tsc --noEmit` — pass
- `pnpm exec eslint . --max-warnings=0` (full enterprise-admin) — pass
- Verified every change via rendered computed styles in a local dev
browser (`/login` and `/verify`, EN).
- **Unit tests (vitest) were not run locally**: the local Node is
20.11.1 and vitest 4 needs ≥20.12 (`node:util.styleText`). CI (Node 24+)
runs them. No existing test assertions depend on the changed
copy/structure (checked `AuthShell`, `Brand`, `verify` tests).

## Known follow-ups (not in this PR)

- "Talk to our team" link target is a placeholder
(`https://zooclaw.ai/contact`) pending the real sales/contact URL.
- The `ZooClawWordmark` SVG logo (mobile auth wordmark, sidebar,
onboarding header, checkout) still shows **ZooClaw** — its `alt` was
intentionally left as-is since the image is unchanged; replacing it
needs a ZooWork wordmark SVG (black + white).

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Body

## Summary

Polishes and rebrands the **enterprise-admin** business sign-in surfaces (`/login` + `/verify`) at `business.zooclaw.ai`, and rebrands user-facing copy from **ZooClaw → ZooWork**.

Both auth screens now render through a single shared `BRAND_AUTH_SHELL` config so they stay visually identical from one source of truth. `/join` and the onboarding forms (which also use `AuthShell` / `OtpGrid`) are intentionally **unchanged** — every new shell behavior is opt-in and defaults off.

## What changed

**Visual polish (login + verify)**
- Staggered entrance animation (reuses the previously-unused `login-reveal` keyframes), brand-red → **gray-black** input focus ring, equal-height (48px) centered black/white primary CTA.
- Left hero now uses an editorial bronze photo (`login-hero-bg.webp`, 53KB) with a left+bottom legibility scrim so white text stays readable over the artwork.
- Dark `#272420` page backdrop; white hero shield icon (only when a hero photo is set).
- Form panel restructured: dropped the eyebrow + divider, sentence-case bold field labels, and a "Talk to our team" contact line.
- All type on these surfaces is **Roboto** (scoped via a `.login-roboto` rule + `next/font`).
- OTP underline fill is now a prop (`fillClassName`); verify passes gray-black, `/join` keeps the default red.

**Rebrand (ZooClaw → ZooWork)**
- New white "ZOOWORK | BUSINESS" hero lockup + new favicon (`favicon.png`).
- Page title → "ZooWork Enterprise Admin".
- Hero eyebrow/title/subtitle + "New to … Business?" + onboarding © + Chinese catalog (`i18n-zh.ts`) updated to ZooWork.
- Hero headline reworded to "Orchestrate your entire digital workforce." and the subtitle to a plain-language security line.

## Testing

- `pnpm exec tsc --noEmit` — pass
- `pnpm exec eslint . --max-warnings=0` (full enterprise-admin) — pass
- Verified every change via rendered computed styles in a local dev browser (`/login` and `/verify`, EN).
- **Unit tests (vitest) were not run locally**: the local Node is 20.11.1 and vitest 4 needs ≥20.12 (`node:util.styleText`). CI (Node 24+) runs them. No existing test assertions depend on the changed copy/structure (checked `AuthShell`, `Brand`, `verify` tests).

## Known follow-ups (not in this PR)

- "Talk to our team" link target is a placeholder (`https://zooclaw.ai/contact`) pending the real sales/contact URL.
- The `ZooClawWordmark` SVG logo (mobile auth wordmark, sidebar, onboarding header, checkout) still shows **ZooClaw** — its `alt` was intentionally left as-is since the image is unchanged; replacing it needs a ZooWork wordmark SVG (black + white).


---

## style(landing): aquavoice-style light theme + hero/header refresh (#2577)

- **SHA**: 92a87d00617483ac9b18c05fa4f1e41d649d4dfc
- **作者**: shana-srp
- **日期**: 2026-07-02T03:34:02Z
- **PR**: #2577

### Commit Message

```
style(landing): aquavoice-style light theme + hero/header refresh (#2577)

## What

Landing-page visual refresh toward an Aqua-style (aquavoice.com) **light
theme**, plus several hero/header polish items requested along the way.

### Hero (first screen — kept dark on purpose)
- Replaced the background **video** with a background **image**
(`object-fit: cover` + `object-position: center 65%` so the round-table
subject survives cropping on any width).
- Removed the embedded demo video.
- Moved the copy/buttons into the upper area so they never overlap the
people in the lower part of the image.

### Header / nav
- Full-bleed, fixed liquid-glass nav (5% white glass + blur + saturate +
top highlight), no drop shadow.
- In compact/scrolled state it switches to a **solid dark bar** so the
white logo + white nav text stay readable over the now-light page body.
- New logo asset.

### Light theme (the rest of the page)
- Flipped the `--landing-*` token palette in `landing.css` from the old
dark scheme to an Aqua-style light scheme (near-white bg, dark-charcoal
text, white cards with thin borders, soft blue accent on the comparison
table).
- **Hero** and the bottom **CTA** re-declare the dark token values in
their own scope, so they stay dark as intentional contrast sections
(matching aquavoice's dark interludes).
- Fixed hardcoded-white surfaces that would otherwise vanish on a light
background: integration chips, comparison-table highlight column +
dividers, security-card icon backgrounds; mobile sticky CTA keeps its
dark scope.

## Scope
Only the public marketing landing surface (`landing/` + shared
`PublicHeader`). Token changes to `--marketing-header-*` are shared by
the other marketing pages (pricing / userguide) by design — header stays
visually in sync.

## Testing
- Verified locally across widths (1000 / 1440 / 1512 / 2200 / 2560 /
3000 and mobile 390) — full-width with no letterboxing, hero locked
dark, all sections legible in light mode, compact header dark bar
readable over light content.
- `tsc` + `eslint` pass via the pre-push changed-surface gate.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>
Co-authored-by: claude[bot] <41898282+claude[bot]@users.noreply.github.com>
Co-authored-by: shana-srp <undefined@users.noreply.github.com>
Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
```

### PR Body

## What

Landing-page visual refresh toward an Aqua-style (aquavoice.com) **light theme**, plus several hero/header polish items requested along the way.

### Hero (first screen — kept dark on purpose)
- Replaced the background **video** with a background **image** (`object-fit: cover` + `object-position: center 65%` so the round-table subject survives cropping on any width).
- Removed the embedded demo video.
- Moved the copy/buttons into the upper area so they never overlap the people in the lower part of the image.

### Header / nav
- Full-bleed, fixed liquid-glass nav (5% white glass + blur + saturate + top highlight), no drop shadow.
- In compact/scrolled state it switches to a **solid dark bar** so the white logo + white nav text stay readable over the now-light page body.
- New logo asset.

### Light theme (the rest of the page)
- Flipped the `--landing-*` token palette in `landing.css` from the old dark scheme to an Aqua-style light scheme (near-white bg, dark-charcoal text, white cards with thin borders, soft blue accent on the comparison table).
- **Hero** and the bottom **CTA** re-declare the dark token values in their own scope, so they stay dark as intentional contrast sections (matching aquavoice's dark interludes).
- Fixed hardcoded-white surfaces that would otherwise vanish on a light background: integration chips, comparison-table highlight column + dividers, security-card icon backgrounds; mobile sticky CTA keeps its dark scope.

## Scope
Only the public marketing landing surface (`landing/` + shared `PublicHeader`). Token changes to `--marketing-header-*` are shared by the other marketing pages (pricing / userguide) by design — header stays visually in sync.

## Testing
- Verified locally across widths (1000 / 1440 / 1512 / 2200 / 2560 / 3000 and mobile 390) — full-width with no letterboxing, hero locked dark, all sections legible in light mode, compact header dark bar readable over light content.
- `tsc` + `eslint` pass via the pre-push changed-surface gate.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(agent-packs): return checkout for purchase (#2689)

- **SHA**: b7320389e513d1d450d99a2152628acc0ab7367a
- **作者**: bill-srp
- **日期**: 2026-07-02T03:04:28Z
- **PR**: #2689

### Commit Message

```
feat(agent-packs): return checkout for purchase (#2689)

## Linear


## Summary
- Wire public agent-pack purchase route to create the purchase snapshot
first, then create an ECAP pack checkout and return the checkout URL
response.
- Resolve buyer identity from the current org membership, validate the
current org through org service, and require a personal org.
- Require an active ECAP pack purchase agreement before installing paid
packs, so abandoned checkout snapshots do not unlock installs.
- Add request/response models and route tests for checkout response,
current-org identity, forbidden client-supplied internal fields, and
team-org rejection.

## Test plan
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_public_agent_packs_routes.py
services/claw-interface/tests/unit/test_pack_purchase_service.py
services/claw-interface/tests/unit/test_ecap_pack_subscription_service.py
-q`
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_public_agent_packs_routes.py
services/claw-interface/tests/unit/test_pack_purchase_service.py
services/claw-interface/tests/unit/test_ecap_pack_subscription_service.py
services/claw-interface/tests/unit/test_agent_install_service.py -q`
(`106 passed`)
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`
```

### PR Body

## Linear


## Summary
- Wire public agent-pack purchase route to create the purchase snapshot first, then create an ECAP pack checkout and return the checkout URL response.
- Resolve buyer identity from the current org membership, validate the current org through org service, and require a personal org.
- Require an active ECAP pack purchase agreement before installing paid packs, so abandoned checkout snapshots do not unlock installs.
- Add request/response models and route tests for checkout response, current-org identity, forbidden client-supplied internal fields, and team-org rejection.

## Test plan
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_public_agent_packs_routes.py services/claw-interface/tests/unit/test_pack_purchase_service.py services/claw-interface/tests/unit/test_ecap_pack_subscription_service.py -q`
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_public_agent_packs_routes.py services/claw-interface/tests/unit/test_pack_purchase_service.py services/claw-interface/tests/unit/test_ecap_pack_subscription_service.py services/claw-interface/tests/unit/test_agent_install_service.py -q` (`106 passed`)
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`


---

## feat(knowledge-base): owner-only document delete + settings nav entry (#2688)

- **SHA**: 8b19b761ba63f598984c55f022f96968f81dcd2a
- **作者**: kevin
- **日期**: 2026-07-02T02:54:57Z
- **PR**: #2688

### Commit Message

```
feat(knowledge-base): owner-only document delete + settings nav entry (#2688)

## Summary

Adds knowledge-base document **management** to the web app +
claw-interface BFF, and surfaces the page in Settings.

Pairs with
**[ecap-proxy-service#141](https://github.com/SerendipityOneInc/ecap-proxy-service/issues/141)**
(owner-only delete enforcement + `is_owner` in the documents listing),
already implemented and deployed to staging (`v0.6.31-beta.6`). This PR
is the `ecap-workspace` side.

Closes #2687

## What's included

- **Delete a document** from the knowledge-base page
- `deleteDocument()` service + React Query mutation (invalidates the
documents list on success)
  - Per-row delete control with a confirm dialog + success/error toast
- claw-interface BFF `DELETE /knowledge-base/documents/{id}` —
transparent passthrough forwarding the caller's bearer token; upstream
status codes (incl. `403`/`404`) pass through verbatim (no BFF change
needed to error handling)
- **Owner-only gating (UX):** the delete control is hidden when
`is_owner === false`. The field is optional for backward-compat (missing
→ shown); the **real** authorization gate is the upstream `403` on a
non-owner delete.
- **Status label copy:** `indexed → Uploaded / 已上传`, `pending → Parsing…
/ 解析中`; the date column header `Indexed → Upload time / 上传时间`. Status
*values* stay backend-owned — only the localized display text changes.
- **Settings navigation:** a **Knowledge Base** entry under **IM
Channels** in `claw-settings`, linking out to the standalone
`/knowledge-base` page (org-scoped, so it is not placed behind the
bot-gated settings tabs).

## Testing

- **Unit:** `verify-web.sh` green — `tsc` + `vitest` (added service /
hook / `DocumentList` cases incl. the `is_owner` three-state gate) +
`eslint`; claw-settings suite 555/555. Backend `verify-py.sh` green —
`ruff` + `pyright` + import-linter; added BFF delete-route unit tests
(owner passthrough + 403/404 propagation).
- **End-to-end (local → staging):** validated the full delete flow
against staging `ecap-proxy-service` through a local claw-interface +
Telepresence tunnel: delete of an owned document succeeds (toast + list
refresh); the deployed schema returns `is_owner`; non-owner delete
returns the upstream `403`.

## Notes

- Delete authorization + `is_owner` computation live in
`ecap-proxy-service` (#141), not here.
- No auto-merge requested.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

Adds knowledge-base document **management** to the web app + claw-interface BFF, and surfaces the page in Settings.

Pairs with **[ecap-proxy-service#141](https://github.com/SerendipityOneInc/ecap-proxy-service/issues/141)** (owner-only delete enforcement + `is_owner` in the documents listing), already implemented and deployed to staging (`v0.6.31-beta.6`). This PR is the `ecap-workspace` side.

Closes #2687

## What's included

- **Delete a document** from the knowledge-base page
  - `deleteDocument()` service + React Query mutation (invalidates the documents list on success)
  - Per-row delete control with a confirm dialog + success/error toast
  - claw-interface BFF `DELETE /knowledge-base/documents/{id}` — transparent passthrough forwarding the caller's bearer token; upstream status codes (incl. `403`/`404`) pass through verbatim (no BFF change needed to error handling)
- **Owner-only gating (UX):** the delete control is hidden when `is_owner === false`. The field is optional for backward-compat (missing → shown); the **real** authorization gate is the upstream `403` on a non-owner delete.
- **Status label copy:** `indexed → Uploaded / 已上传`, `pending → Parsing… / 解析中`; the date column header `Indexed → Upload time / 上传时间`. Status *values* stay backend-owned — only the localized display text changes.
- **Settings navigation:** a **Knowledge Base** entry under **IM Channels** in `claw-settings`, linking out to the standalone `/knowledge-base` page (org-scoped, so it is not placed behind the bot-gated settings tabs).

## Testing

- **Unit:** `verify-web.sh` green — `tsc` + `vitest` (added service / hook / `DocumentList` cases incl. the `is_owner` three-state gate) + `eslint`; claw-settings suite 555/555. Backend `verify-py.sh` green — `ruff` + `pyright` + import-linter; added BFF delete-route unit tests (owner passthrough + 403/404 propagation).
- **End-to-end (local → staging):** validated the full delete flow against staging `ecap-proxy-service` through a local claw-interface + Telepresence tunnel: delete of an owned document succeeds (toast + list refresh); the deployed schema returns `is_owner`; non-owner delete returns the upstream `403`.

## Notes

- Delete authorization + `is_owner` computation live in `ecap-proxy-service` (#141), not here.
- No auto-merge requested.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
