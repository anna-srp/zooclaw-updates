# SerendipityOneInc/ecap-workspace — Commits 2026-06-16

共 19 个 commit

---

## fix(bossclaw): render wechat qr as image (#2496)

- **SHA**: `cb7ece66ca44e153a8e6b02e18a64c4700cc9e2b`
- **作者**: tim-srp (tim-srp)
- **日期**: 2026-06-16T16:07:08Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/cb7ece66ca44e153a8e6b02e18a64c4700cc9e2b
- **PR**: #2496

### 完整 Commit Message

```
fix(bossclaw): render wechat qr as image (#2496)

## Summary
- Render Bossclaw WeChat setup QR codes as real PNG image elements so
mobile long-press recognition works.
- Keep inline backend QR image URLs as direct image sources.
- Add unit coverage for generated and inline QR image rendering paths.

## Test plan
- `bash scripts/verify-web.sh
web/app/src/app/[locale]/bossclaw/components/WechatBindStep.tsx
web/app/src/app/[locale]/bossclaw/bossclaw.module.css
web/app/tests/unit/bossclaw/wechat-bind-step.unit.spec.tsx`
- Manual local smoke: `http://localhost:3000/zh/bossclaw` responds 200
with current branch running.

Co-authored-by: Developer <dev@srp.one>
```

### PR Body

## Summary
- Render Bossclaw WeChat setup QR codes as real PNG image elements so mobile long-press recognition works.
- Keep inline backend QR image URLs as direct image sources.
- Add unit coverage for generated and inline QR image rendering paths.

## Test plan
- `bash scripts/verify-web.sh web/app/src/app/[locale]/bossclaw/components/WechatBindStep.tsx web/app/src/app/[locale]/bossclaw/bossclaw.module.css web/app/tests/unit/bossclaw/wechat-bind-step.unit.spec.tsx`
- Manual local smoke: `http://localhost:3000/zh/bossclaw` responds 200 with current branch running.


---

## fix(deploy): pass bossclaw agent env (#2495)

- **SHA**: `4c41a5fdaa8a59b2d9220b03edea98f9314ef24c`
- **作者**: tim-srp (tim-srp)
- **日期**: 2026-06-16T15:39:34Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/4c41a5fdaa8a59b2d9220b03edea98f9314ef24c
- **PR**: #2495

### 完整 Commit Message

```
fix(deploy): pass bossclaw agent env (#2495)

## Summary
- Pass `NEXT_PUBLIC_BOSSCLAW_AGENT_ID` from GitHub environment variables
into the web deploy environment.
- Include the variable in the generated frontend `.env` file and
Cloudflare `wrangler deploy --var` runtime vars.
- Validate the variable during deploy so dev, staging, and production
fail early if it is missing.

## Test plan
- `git diff --check --cached` before commit
- Workflow-only change; no frontend/backend runtime tests run.

Co-authored-by: Developer <dev@srp.one>
```

### PR Body

## Summary
- Pass `NEXT_PUBLIC_BOSSCLAW_AGENT_ID` from GitHub environment variables into the web deploy environment.
- Include the variable in the generated frontend `.env` file and Cloudflare `wrangler deploy --var` runtime vars.
- Validate the variable during deploy so dev, staging, and production fail early if it is missing.

## Test plan
- `git diff --check --cached` before commit
- Workflow-only change; no frontend/backend runtime tests run.


---

## fix(enterprise-admin): keep incomplete org onboarding on setup (#2492)

- **SHA**: `da5a453c7907afac082cf7ae1007bf6942458575`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-06-16T15:08:15Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/da5a453c7907afac082cf7ae1007bf6942458575
- **PR**: #2492

### 完整 Commit Message

```
fix(enterprise-admin): keep incomplete org onboarding on setup (#2492)

## Summary
- Keep incomplete enterprise-admin orgs on onboarding Step 1 so admins
can review and edit the org name/logo before continuing.
- Update Step 1 for existing incomplete orgs via `POST /orgs/{org_id}`
instead of creating a new org.
- Expose `logo_url` in `/account/me` org context and allow org `name` in
`OrgUpdateRequest`.

## Root cause
The split onboarding flow treated `registration_completed=false` as
meaning Step 1 was already complete and mapped the initial onboarding
step directly to `invite-team`. That skipped the only UI where admins
can edit org name and logo. The `/account/me` org projection also did
not expose `logo_url`, and backend org updates did not accept `name`, so
the frontend could not safely prefill and persist those Step 1 edits.

## Test plan
- [x] `bash scripts/verify-changed.sh` (reported no locally verifiable
surfaces changed vs `origin/main`)
- [x] `pnpm --dir web/enterprise-admin exec vitest run
app/onboarding/__tests__/onboarding-page.test.tsx`
- [x] `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- [x] `pnpm --dir web/enterprise-admin exec eslint
app/onboarding/useOnboardingViewModel.ts
app/onboarding/__tests__/onboarding-page.test.tsx types/org.ts
types/user-me.ts`
- [x] `/Users/bill/.venvs/claw-interface/bin/pytest
services/claw-interface/tests/unit/test_schema_org.py
services/claw-interface/tests/unit/test_routes_account.py::TestGetMeHandler
services/claw-interface/tests/unit/test_account_team_org_route.py -q`
- [x] `/Users/bill/.venvs/claw-interface/bin/ruff check
app/schema/org.py app/schema/account_api.py
tests/unit/test_schema_org.py tests/unit/test_routes_account.py`
- [x] `/Users/bill/.venvs/claw-interface/bin/ruff format --check
app/schema/org.py app/schema/account_api.py
tests/unit/test_schema_org.py tests/unit/test_routes_account.py`
- [x] `/Users/bill/.venvs/claw-interface/bin/pyright --pythonpath
/Users/bill/.venvs/claw-interface/bin/python app/schema/org.py
app/schema/account_api.py tests/unit/test_schema_org.py
tests/unit/test_routes_account.py`
```

### PR Body

## Summary
- Keep incomplete enterprise-admin orgs on onboarding Step 1 so admins can review and edit the org name/logo before continuing.
- Update Step 1 for existing incomplete orgs via `POST /orgs/{org_id}` instead of creating a new org.
- Expose `logo_url` in `/account/me` org context and allow org `name` in `OrgUpdateRequest`.

## Root cause
The split onboarding flow treated `registration_completed=false` as meaning Step 1 was already complete and mapped the initial onboarding step directly to `invite-team`. That skipped the only UI where admins can edit org name and logo. The `/account/me` org projection also did not expose `logo_url`, and backend org updates did not accept `name`, so the frontend could not safely prefill and persist those Step 1 edits.

## Test plan
- [x] `bash scripts/verify-changed.sh` (reported no locally verifiable surfaces changed vs `origin/main`)
- [x] `pnpm --dir web/enterprise-admin exec vitest run app/onboarding/__tests__/onboarding-page.test.tsx`
- [x] `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- [x] `pnpm --dir web/enterprise-admin exec eslint app/onboarding/useOnboardingViewModel.ts app/onboarding/__tests__/onboarding-page.test.tsx types/org.ts types/user-me.ts`
- [x] `/Users/bill/.venvs/claw-interface/bin/pytest services/claw-interface/tests/unit/test_schema_org.py services/claw-interface/tests/unit/test_routes_account.py::TestGetMeHandler services/claw-interface/tests/unit/test_account_team_org_route.py -q`
- [x] `/Users/bill/.venvs/claw-interface/bin/ruff check app/schema/org.py app/schema/account_api.py tests/unit/test_schema_org.py tests/unit/test_routes_account.py`
- [x] `/Users/bill/.venvs/claw-interface/bin/ruff format --check app/schema/org.py app/schema/account_api.py tests/unit/test_schema_org.py tests/unit/test_routes_account.py`
- [x] `/Users/bill/.venvs/claw-interface/bin/pyright --pythonpath /Users/bill/.venvs/claw-interface/bin/python app/schema/org.py app/schema/account_api.py tests/unit/test_schema_org.py tests/unit/test_routes_account.py`


---

## feat(bossclaw): one-off onboarding wizard with post-signup agent auto-install (#2412)

- **SHA**: `a882154c1793f0a37a5abfd78e3c6bf2570c7c33`
- **作者**: tim-srp (tim-srp)
- **日期**: 2026-06-16T15:07:45Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/a882154c1793f0a37a5abfd78e3c6bf2570c7c33
- **PR**: #2412

### 完整 Commit Message

```
feat(bossclaw): one-off onboarding wizard with post-signup agent auto-install (#2412)

## Linear

https://linear.app/srpone/issue/ECA-983/bossclaw-one-off-onboarding-flow-with-dedicated-warm-pool

## Summary
- **V3 design — zero backend changes**: bossclaw users are plain ECAP
users on the shared warm pool; the only channel difference is the page
auto-installing a configured agent (`NEXT_PUBLIC_BOSSCLAW_AGENT_ID`)
after signup via the existing hire pipeline (`install/async` + operation
polling).
- Standalone mobile-first wizard at `app/[locale]/bossclaw`
(self-contained for one-shot removal): Firebase phone login + Turnstile
→ optional subscription-code redemption (existing
`/api/gift-code/redeem`) → WeChat-binding QR bound to the installed
agent (personal WeChat binds exactly one agent). The install runs in the
background during the subscription-code step; the WeChat step waits for
it with a retry path.
- Spec v3
(`docs/superpowers/specs/2026-06-11-bossclaw-onboarding-design.md`)
records the design evolution and the three accepted trade-offs: no
dedicated 100-bot pool (bump `WARM_POOL_TARGET_SIZE` for the campaign
window), agent installs ~30–60s after signup, trial credits granted
normally.
- Supersedes #2405 (v2 pool-segmentation approach, closed); the
companion user-interface PR #138 is closed unmerged since `role` is no
longer touched.

**Deploy config**: frontend `NEXT_PUBLIC_BOSSCLAW_AGENT_ID`; ops bumps
`WARM_POOL_TARGET_SIZE` during the campaign. Teardown = revert the env
bump + delete the `bossclaw/` directory.

## Test plan
- [x] Frontend: 7164 unit tests passed (new: install state machine +
wizard resume), `tsc --noEmit` + eslint clean
- [ ] Staging smoke: signup → agent auto-install completes → WeChat QR
binds to the agent

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Size override justification
- This PR is intentionally self-contained for the BossClaw one-off
onboarding surface: route, wizard state, login/redeem/WeChat binding UI,
agent auto-install glue, and targeted unit coverage must ship together
for staging smoke testing.
- The largest added file is the dedicated BossClaw CSS module; keeping
the styling local avoids touching shared design-system surfaces and
keeps teardown to deleting the bossclaw directory.
- Follow-up fixes in this pass add regression tests for QR rendering,
UID-scoped wizard progress, partial-login handling, and SMS OTP request
shape.

---------

Co-authored-by: Developer <dev@srp.one>
```

### PR Body

## Linear
https://linear.app/srpone/issue/ECA-983/bossclaw-one-off-onboarding-flow-with-dedicated-warm-pool

## Summary
- **V3 design — zero backend changes**: bossclaw users are plain ECAP users on the shared warm pool; the only channel difference is the page auto-installing a configured agent (`NEXT_PUBLIC_BOSSCLAW_AGENT_ID`) after signup via the existing hire pipeline (`install/async` + operation polling).
- Standalone mobile-first wizard at `app/[locale]/bossclaw` (self-contained for one-shot removal): Firebase phone login + Turnstile → optional subscription-code redemption (existing `/api/gift-code/redeem`) → WeChat-binding QR bound to the installed agent (personal WeChat binds exactly one agent). The install runs in the background during the subscription-code step; the WeChat step waits for it with a retry path.
- Spec v3 (`docs/superpowers/specs/2026-06-11-bossclaw-onboarding-design.md`) records the design evolution and the three accepted trade-offs: no dedicated 100-bot pool (bump `WARM_POOL_TARGET_SIZE` for the campaign window), agent installs ~30–60s after signup, trial credits granted normally.
- Supersedes #2405 (v2 pool-segmentation approach, closed); the companion user-interface PR #138 is closed unmerged since `role` is no longer touched.

**Deploy config**: frontend `NEXT_PUBLIC_BOSSCLAW_AGENT_ID`; ops bumps `WARM_POOL_TARGET_SIZE` during the campaign. Teardown = revert the env bump + delete the `bossclaw/` directory.

## Test plan
- [x] Frontend: 7164 unit tests passed (new: install state machine + wizard resume), `tsc --noEmit` + eslint clean
- [ ] Staging smoke: signup → agent auto-install completes → WeChat QR binds to the agent

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Size override justification
- This PR is intentionally self-contained for the BossClaw one-off onboarding surface: route, wizard state, login/redeem/WeChat binding UI, agent auto-install glue, and targeted unit coverage must ship together for staging smoke testing.
- The largest added file is the dedicated BossClaw CSS module; keeping the styling local avoids touching shared design-system surfaces and keeps teardown to deleting the bossclaw directory.
- Follow-up fixes in this pass add regression tests for QR rendering, UID-scoped wizard progress, partial-login handling, and SMS OTP request shape.

---

## fix(web): align new chat agent identity (#2491)

- **SHA**: `47e04894f614910544c29c3094d40e0a329af8bd`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-06-16T13:22:24Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/47e04894f614910544c29c3094d40e0a329af8bd
- **PR**: #2491

### 完整 Commit Message

```
fix(web): align new chat agent identity (#2491)

## Summary
- Align /new-chat selected agent name and avatar resolution with the
sidebar.
- Reuse one presentation resolver for the headline, composer
placeholder, and selector chips.
- Add regression coverage for customized specialist identity plus
workspace avatar precedence.

## Tests
- `bash scripts/verify-web.sh
'web/app/src/app/[locale]/(app)/new-chat/agentIdentity.ts'
'web/app/src/app/[locale]/(app)/new-chat/useViewModel.ts'
'web/app/src/app/[locale]/(app)/new-chat/components/AgentSelector.tsx'
'web/app/src/app/[locale]/(app)/new-chat/NewChatClient.tsx'
'web/app/tests/unit/app/new-chat/NewChatClient.unit.spec.tsx'
'web/app/tests/unit/app/new-chat/AgentSelector.unit.spec.tsx'`
```

### PR Body

## Summary
- Align /new-chat selected agent name and avatar resolution with the sidebar.
- Reuse one presentation resolver for the headline, composer placeholder, and selector chips.
- Add regression coverage for customized specialist identity plus workspace avatar precedence.

## Tests
- `bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/new-chat/agentIdentity.ts' 'web/app/src/app/[locale]/(app)/new-chat/useViewModel.ts' 'web/app/src/app/[locale]/(app)/new-chat/components/AgentSelector.tsx' 'web/app/src/app/[locale]/(app)/new-chat/NewChatClient.tsx' 'web/app/tests/unit/app/new-chat/NewChatClient.unit.spec.tsx' 'web/app/tests/unit/app/new-chat/AgentSelector.unit.spec.tsx'`


---

## fix(web): make the desktop app window draggable (#2477)

- **SHA**: `d426c4e21c301cb8ebde51a980b58bf6314aa9ab`
- **作者**: zayne-srp (zayne-srp)
- **日期**: 2026-06-16T12:54:44Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/d426c4e21c301cb8ebde51a980b58bf6314aa9ab
- **PR**: #2477

### 完整 Commit Message

```
fix(web): make the desktop app window draggable (#2477)

## Problem

The desktop (Electron) window can't be dragged to move it. The shell
creates its `BrowserWindow` with `titleBarStyle: 'hiddenInset'`
(`desktop/main/index.ts`), which hides the native title bar — so macOS
provides no draggable region. The renderer (this web app) declared no
`-webkit-app-region: drag` area anywhere, so there was nothing to grab.

## Fix

Add a thin draggable strip across the top of the content area in
`AppLayout`, rendered **only under Electron**:

- **`useIsElectron` hook** (new) — detects the desktop shell via the
preload's `window.electronAPI`; SSR-safe (false → flips after mount,
like `useIsDesktop`). In a plain browser it's always `false`, so the
strip is never rendered there → the web build is unaffected.
- **Scoped to the content area** (not full width) so it doesn't cover
the sidebar's top-left link; verified the top 32px of the content area
has no interactive elements.
- **Inline `-webkit-app-region`** — Lightning CSS strips this
non-standard property out of compiled stylesheet rules (a class-based
version had no effect at runtime), so it's set via inline style.
`AppLayout.tsx` is already in the `react/forbid-dom-props` allowlist.

## Test

Verified in the running desktop app: the strip computes
`-webkit-app-region: drag` over the content-area top (`left:260, w:585,
h:32`), and the window drags from that band while the sidebar link stays
clickable. Browser build renders no strip.

Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>
```

### PR Body

## Problem

The desktop (Electron) window can't be dragged to move it. The shell creates its `BrowserWindow` with `titleBarStyle: 'hiddenInset'` (`desktop/main/index.ts`), which hides the native title bar — so macOS provides no draggable region. The renderer (this web app) declared no `-webkit-app-region: drag` area anywhere, so there was nothing to grab.

## Fix

Add a thin draggable strip across the top of the content area in `AppLayout`, rendered **only under Electron**:

- **`useIsElectron` hook** (new) — detects the desktop shell via the preload's `window.electronAPI`; SSR-safe (false → flips after mount, like `useIsDesktop`). In a plain browser it's always `false`, so the strip is never rendered there → the web build is unaffected.
- **Scoped to the content area** (not full width) so it doesn't cover the sidebar's top-left link; verified the top 32px of the content area has no interactive elements.
- **Inline `-webkit-app-region`** — Lightning CSS strips this non-standard property out of compiled stylesheet rules (a class-based version had no effect at runtime), so it's set via inline style. `AppLayout.tsx` is already in the `react/forbid-dom-props` allowlist.

## Test

Verified in the running desktop app: the strip computes `-webkit-app-region: drag` over the content-area top (`left:260, w:585, h:32`), and the window drags from that band while the sidebar link stays clickable. Browser build renders no strip.

---

## fix(web): initialize OpenClaw on new chat (#2490)

- **SHA**: `887a54e5993bf906ab18c10748fe409e92145673`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-06-16T12:50:05Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/887a54e5993bf906ab18c10748fe409e92145673
- **PR**: #2490

### 完整 Commit Message

```
fix(web): initialize OpenClaw on new chat (#2490)

## Summary

- Move `OpenClawProvider` to the authenticated app layout so `/new-chat`
and `/chat` share the same lazily activated init state.
- Activate OpenClaw from `/new-chat`, then enable the vertical pack
installer once init reaches `ready`.
- Update layout coverage and add a focused new-chat view-model test for
init activation plus vertical-pack enablement.

## Tests

- `bash scripts/verify-web.sh
'web/app/src/app/[locale]/(app)/layout.tsx'
'web/app/src/app/[locale]/(app)/(chat)/layout.tsx'
'web/app/src/app/[locale]/(app)/new-chat/useViewModel.ts'
'web/app/tests/unit/app/new-chat/useViewModel.unit.spec.tsx'
'web/app/tests/unit/app/app-group-layout.unit.spec.tsx'
'web/app/tests/unit/app/chat-group-layout.unit.spec.tsx'`
- `bash scripts/verify-changed.sh`
```

### PR Body

## Summary

- Move `OpenClawProvider` to the authenticated app layout so `/new-chat` and `/chat` share the same lazily activated init state.
- Activate OpenClaw from `/new-chat`, then enable the vertical pack installer once init reaches `ready`.
- Update layout coverage and add a focused new-chat view-model test for init activation plus vertical-pack enablement.

## Tests

- `bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/layout.tsx' 'web/app/src/app/[locale]/(app)/(chat)/layout.tsx' 'web/app/src/app/[locale]/(app)/new-chat/useViewModel.ts' 'web/app/tests/unit/app/new-chat/useViewModel.unit.spec.tsx' 'web/app/tests/unit/app/app-group-layout.unit.spec.tsx' 'web/app/tests/unit/app/chat-group-layout.unit.spec.tsx'`
- `bash scripts/verify-changed.sh`


---

## refactor(enterprise-admin): auth/onboarding/checkout 迁移至 enterprise-app 交互风格 + editorial 页强制浅色 (#2473)

- **SHA**: `5ac6b0746f95bd4df64d5663d5c596bd71400a3f`
- **作者**: david-srp (david-srp)
- **日期**: 2026-06-16T12:19:46Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/5ac6b0746f95bd4df64d5663d5c596bd71400a3f
- **PR**: #2473

### 完整 Commit Message

```
refactor(enterprise-admin): auth/onboarding/checkout 迁移至 enterprise-app 交互风格 + editorial 页强制浅色 (#2473)

## 背景
延续「editorial 页太黑」的修复，进一步把 enterprise-admin 的
**登录/验证/邀请/onboarding/checkout** 全部重构为 **enterprise-app 的交互组件风格**（分栏卡片 +
圆角盒子输入 + red 按钮），并保持这些 editorial 页在系统 dark 下强制浅色。

设计
spec：`docs/superpowers/specs/2026-06-15-enterprise-admin-auth-checkout-interaction-port.md`

## 改动（分阶段）
0. **editorial 页强制浅色**：`:root:has(.force-light-surface)` 在 dark
下把整文档钉回浅色（Tailwind v4 只在 :root 保留 token 覆盖，故用 :has()）；`ZooClawWordmark`
支持 `theme=auto|light|dark`；favicon 换 ZooClaw mark。
1. **Login → 分栏卡片**：抽出 `components/auth/AuthShell`（居中 rounded-2xl 卡片 +
深色 ink hero + 共享样式常量）。
2. **Verify + Join**：改用 AuthShell + boxed 输入 + red 按钮 + 共享 `OtpGrid`（6
格验证码、红色填充下划线）。
3. **Onboarding**：表单（OrgSetup/BulkInvite/WarmPool）从 hairline 改为
boxed/red；StepIndicator 红色 current。向导布局保留（enterprise-app 无 onboarding
对应）。
4. **Checkout**：force-light 卡片 + ZooClaw logo；付款
Stripe(red)/支付宝(secondary)；**购买报错时显示固定中文提示**「仅支持企业账号购买 Vertical
Plan，一个企业账号仅支持购买一个套餐」**并显示 Log out 按钮**（viewModel 增加 logout）。

## 验证
- ✅ `pnpm lint` / `tsc --noEmit` / `pnpm test`（221 tests）/ `next build`
- ✅ 本地 dark 模式截图确认：login / join 分栏卡片、onboarding 表单、checkout 报错态（中文提示 +
Log out 按钮）均为 enterprise-app 浅色风格

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
Co-authored-by: claude[bot] <41898282+claude[bot]@users.noreply.github.com>
```

### PR Body

## 背景
延续「editorial 页太黑」的修复，进一步把 enterprise-admin 的 **登录/验证/邀请/onboarding/checkout** 全部重构为 **enterprise-app 的交互组件风格**（分栏卡片 + 圆角盒子输入 + red 按钮），并保持这些 editorial 页在系统 dark 下强制浅色。

设计 spec：`docs/superpowers/specs/2026-06-15-enterprise-admin-auth-checkout-interaction-port.md`

## 改动（分阶段）
0. **editorial 页强制浅色**：`:root:has(.force-light-surface)` 在 dark 下把整文档钉回浅色（Tailwind v4 只在 :root 保留 token 覆盖，故用 :has()）；`ZooClawWordmark` 支持 `theme=auto|light|dark`；favicon 换 ZooClaw mark。
1. **Login → 分栏卡片**：抽出 `components/auth/AuthShell`（居中 rounded-2xl 卡片 + 深色 ink hero + 共享样式常量）。
2. **Verify + Join**：改用 AuthShell + boxed 输入 + red 按钮 + 共享 `OtpGrid`（6 格验证码、红色填充下划线）。
3. **Onboarding**：表单（OrgSetup/BulkInvite/WarmPool）从 hairline 改为 boxed/red；StepIndicator 红色 current。向导布局保留（enterprise-app 无 onboarding 对应）。
4. **Checkout**：force-light 卡片 + ZooClaw logo；付款 Stripe(red)/支付宝(secondary)；**购买报错时显示固定中文提示**「仅支持企业账号购买 Vertical Plan，一个企业账号仅支持购买一个套餐」**并显示 Log out 按钮**（viewModel 增加 logout）。

## 验证
- ✅ `pnpm lint` / `tsc --noEmit` / `pnpm test`（221 tests）/ `next build`
- ✅ 本地 dark 模式截图确认：login / join 分栏卡片、onboarding 表单、checkout 报错态（中文提示 + Log out 按钮）均为 enterprise-app 浅色风格

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(web): forward session cookie auth to backend proxy (#2489)

- **SHA**: `0921218f859da63eeb9707fdb14d4946037582e5`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-06-16T12:13:33Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/0921218f859da63eeb9707fdb14d4946037582e5
- **PR**: #2489

### 完整 Commit Message

```
fix(web): forward session cookie auth to backend proxy (#2489)

## Summary
- Forward the HttpOnly `zc_session` token as `Authorization` when
`proxyToBackend` receives an authenticated request without an explicit
bearer header.
- Add regression coverage for cookie fallback and explicit bearer
precedence.

## Root cause
The middleware can authenticate API requests from the `zc_session`
cookie, but `proxyToBackend` only forwarded an existing `Authorization`
header to claw-interface. Cookie-authenticated BFF requests therefore
passed middleware while the backend still received no bearer token.

## Test plan
- [x] `pnpm --dir web/app exec vitest run
tests/unit/lib/api/proxy.unit.spec.ts`
- [x] `bash scripts/verify-web.sh web/app/src/lib/api/proxy.ts
web/app/tests/unit/lib/api/proxy.unit.spec.ts`
- [x] `bash scripts/verify-changed.sh`
```

### PR Body

## Summary
- Forward the HttpOnly `zc_session` token as `Authorization` when `proxyToBackend` receives an authenticated request without an explicit bearer header.
- Add regression coverage for cookie fallback and explicit bearer precedence.

## Root cause
The middleware can authenticate API requests from the `zc_session` cookie, but `proxyToBackend` only forwarded an existing `Authorization` header to claw-interface. Cookie-authenticated BFF requests therefore passed middleware while the backend still received no bearer token.

## Test plan
- [x] `pnpm --dir web/app exec vitest run tests/unit/lib/api/proxy.unit.spec.ts`
- [x] `bash scripts/verify-web.sh web/app/src/lib/api/proxy.ts web/app/tests/unit/lib/api/proxy.unit.spec.ts`
- [x] `bash scripts/verify-changed.sh`


---

## fix(desktop): repair the pandaclaw desktop build chain (#2484)

- **SHA**: `6b4bf697941df1967c9ccafe1554540fcf19763d`
- **作者**: zayne-srp (zayne-srp)
- **日期**: 2026-06-16T12:07:45Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/6b4bf697941df1967c9ccafe1554540fcf19763d
- **PR**: #2484

### 完整 Commit Message

```
fix(desktop): repair the pandaclaw desktop build chain (#2484)

## Problem

The **pandaclaw-desktop** packaging has been broken since the web app
moved from `web/` to `web/app` — the staging/server scripts still
referenced the old layout, so `pnpm build:mac` / `build:win` never
produced a working app (no `.web-stage` / `release` artifacts existed
anywhere).

Verified the full chain end-to-end after this fix: `DESKTOP_BUILD=1 next
build` → `tsup` → `stage-web` → `electron-builder --dir` emits
`PandaClaw.app` with the Next server correctly at
`Contents/Resources/web/app/server.js`.

## Fixes

| File | Change |
|---|---|
| `web/app/next.config.ts` | Set `outputFileTracingRoot` for the desktop
standalone build. Without it Next traces from the outermost lockfile
(`~/package-lock.json`) and emits
`standalone/source/zooclaw-desktop/.../server.js` — a deep, unlocatable
layout. With it: `standalone/app/server.js` + `standalone/node_modules`.
|
| `desktop/package.json` (`stage-web`) | Copy from `../web/app/.next`
(was `../web/.next`) into `.web-stage/app/` (was `.web-stage/web/`),
matching the standalone layout. |
| `desktop/scripts/flatten-pnpm.js` | Consolidate deps into
`.web-stage/app/node_modules` (was `web/`). |
| `desktop/main/next-server.ts` | Load the packaged server from
`resources/web/app/server.js` (was `resources/web/web/server.js`). |
| `desktop/scripts/prune-broken-symlinks.js` (new) | Strip the dangling
pnpm dev-dep symlinks (`shiki`/`typescript`) that Next's standalone
tracer leaves behind, so `rsync -L` no longer aborts staging with exit
23. Pure Node, so it also works on the Windows CI runner. |

## Why this PR

Prerequisite for adding desktop build CI in `zooclaw-desktop` (which
consumes this repo as a submodule) — that CI can only succeed once the
build chain itself works.

Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>
```

### PR Body

## Problem

The **pandaclaw-desktop** packaging has been broken since the web app moved from `web/` to `web/app` — the staging/server scripts still referenced the old layout, so `pnpm build:mac` / `build:win` never produced a working app (no `.web-stage` / `release` artifacts existed anywhere).

Verified the full chain end-to-end after this fix: `DESKTOP_BUILD=1 next build` → `tsup` → `stage-web` → `electron-builder --dir` emits `PandaClaw.app` with the Next server correctly at `Contents/Resources/web/app/server.js`.

## Fixes

| File | Change |
|---|---|
| `web/app/next.config.ts` | Set `outputFileTracingRoot` for the desktop standalone build. Without it Next traces from the outermost lockfile (`~/package-lock.json`) and emits `standalone/source/zooclaw-desktop/.../server.js` — a deep, unlocatable layout. With it: `standalone/app/server.js` + `standalone/node_modules`. |
| `desktop/package.json` (`stage-web`) | Copy from `../web/app/.next` (was `../web/.next`) into `.web-stage/app/` (was `.web-stage/web/`), matching the standalone layout. |
| `desktop/scripts/flatten-pnpm.js` | Consolidate deps into `.web-stage/app/node_modules` (was `web/`). |
| `desktop/main/next-server.ts` | Load the packaged server from `resources/web/app/server.js` (was `resources/web/web/server.js`). |
| `desktop/scripts/prune-broken-symlinks.js` (new) | Strip the dangling pnpm dev-dep symlinks (`shiki`/`typescript`) that Next's standalone tracer leaves behind, so `rsync -L` no longer aborts staging with exit 23. Pure Node, so it also works on the Windows CI runner. |

## Why this PR

Prerequisite for adding desktop build CI in `zooclaw-desktop` (which consumes this repo as a submodule) — that CI can only succeed once the build chain itself works.

---

## fix(claw-interface): use team billing credits (#2486)

- **SHA**: `52542c0b5782af715f8211afec6ff9aa3fc5b76f`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-06-16T10:57:19Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/52542c0b5782af715f8211afec6ff9aa3fc5b76f
- **PR**: #2486

### 完整 Commit Message

```
fix(claw-interface): use team billing credits (#2486)

## Summary

- Use the org billing team id when checking team workspace credits.
- Persist `avatar_url` on agent workspace install/update paths from pack
metadata.
- Return workspace `avatar_url` from `/openclaw/agents` and prefer it in
the sidebar when present.

## Tests

- `services/claw-interface/.venv/bin/python -m pytest
services/claw-interface/tests/unit/test_user_credits.py
services/claw-interface/tests/unit/test_agent_install_service.py
services/claw-interface/tests/unit/test_agent_multi_install_service.py
services/claw-interface/tests/unit/test_agent_update_service.py
services/claw-interface/tests/unit/test_agent_workspace_repo.py
services/claw-interface/tests/unit/test_agent_service.py
services/claw-interface/tests/unit/test_agent_response.py
services/claw-interface/tests/unit/test_openclaw_agents.py -q` (289
passed)
- `cd services/claw-interface && .venv/bin/ruff check .`
- `cd services/claw-interface && .venv/bin/ruff format --check .`
- `cd services/claw-interface && .venv/bin/pyright --pythonpath
.venv/bin/python app/ tests/`
- `cd services/claw-interface && .venv/bin/lint-imports`
- `bash scripts/verify-web.sh
web/app/src/components/sidenav/SideNavAgentList.tsx
web/app/src/hooks/useInstallingComputerAgents.ts
web/app/src/lib/api/openclaw-agents-v2-types.ts
web/app/src/lib/api/openclaw.ts
web/app/tests/unit/components/sidenav/SideNavAgentList.unit.spec.tsx`
could not complete locally because `web/node_modules` is missing (`tsc`,
`vitest`, and `eslint` commands not found).
- `bash scripts/verify-changed.sh` passed with skips only; it skipped
web due missing `web/node_modules` and skipped py because the script
could not find pyright/lint-imports on PATH, so backend checks were run
directly from the claw-interface venv above.
```

### PR Body

## Summary

- Use the org billing team id when checking team workspace credits.
- Persist `avatar_url` on agent workspace install/update paths from pack metadata.
- Return workspace `avatar_url` from `/openclaw/agents` and prefer it in the sidebar when present.

## Tests

- `services/claw-interface/.venv/bin/python -m pytest services/claw-interface/tests/unit/test_user_credits.py services/claw-interface/tests/unit/test_agent_install_service.py services/claw-interface/tests/unit/test_agent_multi_install_service.py services/claw-interface/tests/unit/test_agent_update_service.py services/claw-interface/tests/unit/test_agent_workspace_repo.py services/claw-interface/tests/unit/test_agent_service.py services/claw-interface/tests/unit/test_agent_response.py services/claw-interface/tests/unit/test_openclaw_agents.py -q` (289 passed)
- `cd services/claw-interface && .venv/bin/ruff check .`
- `cd services/claw-interface && .venv/bin/ruff format --check .`
- `cd services/claw-interface && .venv/bin/pyright --pythonpath .venv/bin/python app/ tests/`
- `cd services/claw-interface && .venv/bin/lint-imports`
- `bash scripts/verify-web.sh web/app/src/components/sidenav/SideNavAgentList.tsx web/app/src/hooks/useInstallingComputerAgents.ts web/app/src/lib/api/openclaw-agents-v2-types.ts web/app/src/lib/api/openclaw.ts web/app/tests/unit/components/sidenav/SideNavAgentList.unit.spec.tsx` could not complete locally because `web/node_modules` is missing (`tsc`, `vitest`, and `eslint` commands not found).
- `bash scripts/verify-changed.sh` passed with skips only; it skipped web due missing `web/node_modules` and skipped py because the script could not find pyright/lint-imports on PATH, so backend checks were run directly from the claw-interface venv above.


---

## fix(web): skip web onboarding and add admin app link (#2487)

- **SHA**: `78cd6201b12e7fc8971079d0c5b4a4eee752adb0`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-06-16T10:42:40Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/78cd6201b12e7fc8971079d0c5b4a4eee752adb0
- **PR**: #2487

### 完整 Commit Message

```
fix(web): skip web onboarding and add admin app link (#2487)

## Summary

- add a `Web App` entry to the enterprise-admin sidebar and mobile nav,
defaulting to `https://zooclaw.ai/new-chat`
- disable web app onboarding as a chat blocker for logged-in users
- update regression coverage for the admin app link and onboarding
resolver behavior

## Local Checks

- `bash scripts/verify-changed.sh`
- `pnpm --dir web/app exec vitest run
tests/unit/components/onboarding/resolveOnboardingStatus.unit.spec.ts`
- `pnpm --dir web/enterprise-admin exec vitest run
components/layout/__tests__/Sidebar.test.tsx`
- `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- `pnpm --dir web/enterprise-admin exec eslint
components/layout/Sidebar.tsx components/layout/MobileNav.tsx
components/layout/__tests__/Sidebar.test.tsx`
- `git diff --check origin/main...HEAD`
```

### PR Body

## Summary

- add a `Web App` entry to the enterprise-admin sidebar and mobile nav, defaulting to `https://zooclaw.ai/new-chat`
- disable web app onboarding as a chat blocker for logged-in users
- update regression coverage for the admin app link and onboarding resolver behavior

## Local Checks

- `bash scripts/verify-changed.sh`
- `pnpm --dir web/app exec vitest run tests/unit/components/onboarding/resolveOnboardingStatus.unit.spec.ts`
- `pnpm --dir web/enterprise-admin exec vitest run components/layout/__tests__/Sidebar.test.tsx`
- `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- `pnpm --dir web/enterprise-admin exec eslint components/layout/Sidebar.tsx components/layout/MobileNav.tsx components/layout/__tests__/Sidebar.test.tsx`
- `git diff --check origin/main...HEAD`


---

## fix(web): add search & filters to agent pack and vertical plan management (#2457)

- **SHA**: `6950d51aa7ab166474018f528975604d897c1cb1`
- **作者**: david-srp (david-srp)
- **日期**: 2026-06-16T09:21:18Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/6950d51aa7ab166474018f528975604d897c1cb1
- **PR**: #2457

### 完整 Commit Message

```
fix(web): add search & filters to agent pack and vertical plan management (#2457)

## What & Why

Improves management efficiency of the zooclaw admin console
(`dashboard-console`) by adding search/filtering and tidying column
semantics — across **both** catalogue surfaces: **Agent packs** and
**Vertical pack plans**.

## Agent packs

1. **Search box** — matches name, display id, version, category, short
bio, bio, status, and every skill / integration / automation tag,
case-insensitive.
2. **Market visibility filter** — `all` / `in market` / `hidden`.
3. **Default sort** — by `published_at` descending (newest first).
4. **Status filter** — defaults to `all` so a freshly created
draft/submitted pack is never hidden the moment its dialog closes;
`active` and the other statuses are available as filters.
5. **"Scope" column → short bio** — the list column now shows the pack's
short bio.
6. **"Hidden market" mark moved** — from the Scope column into the
**Status** column.

## Vertical pack plans

7. **Search box** — matches plan name, plan id, price, credits, and the
ids **and resolved display names** of included + add-on agent packs (so
searching the agent name shown in the table, e.g. "Agent Studio",
works), case-insensitive (reuses the parameterized `PackSearch`).
8. **Default sort** — by `updated_at` descending (most recently updated
first), so a just-edited plan surfaces at the top and matches the
table's "Updated" column. Applied at the view layer only; the canonical
`sortVerticalPackPlans` (name sort) used by the data layer and mutations
is untouched.

## Review follow-ups (codex)

- Reverted the agent-packs default from `active` → `all` (item 4): an
`active` default hid new draft/submitted packs after create, reading
like a failed action.
- Switched the plan sort from `created_at` → `updated_at` (item 8) so
recency tracks the last edit, consistent with the "Updated" column.

## Scope / safety

Presentation + **client-side** derivation only. No API, data-model, or
view-model behavior changes — `claw-api`, `packs`, `vertical-pack-plans`
lib, React Query wiring, and the live/seed fallback are untouched.
Filtering/sorting are pure module-level functions exercised directly by
unit tests.

## Verification

- `tsc -b` → 0 errors
- `eslint .` → 0 errors
- `vitest run` → 27 files / 200 tests pass, including view-model tests
for both surfaces (agent-packs: default-all newest-first, full-catalogue
sort, hidden/visible filter, multi-dimension search; plans: updated_at
sort proven by a created-earlier/edited-later case + multi-dimension
search).

---------

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What & Why

Improves management efficiency of the zooclaw admin console (`dashboard-console`) by adding search/filtering and tidying column semantics — across **both** catalogue surfaces: **Agent packs** and **Vertical pack plans**.

## Agent packs

1. **Search box** — matches name, display id, version, category, short bio, bio, status, and every skill / integration / automation tag, case-insensitive.
2. **Market visibility filter** — `all` / `in market` / `hidden`.
3. **Default sort** — by `published_at` descending (newest first).
4. **Status filter** — defaults to `all` so a freshly created draft/submitted pack is never hidden the moment its dialog closes; `active` and the other statuses are available as filters.
5. **"Scope" column → short bio** — the list column now shows the pack's short bio.
6. **"Hidden market" mark moved** — from the Scope column into the **Status** column.

## Vertical pack plans

7. **Search box** — matches plan name, plan id, price, credits, and the ids **and resolved display names** of included + add-on agent packs (so searching the agent name shown in the table, e.g. "Agent Studio", works), case-insensitive (reuses the parameterized `PackSearch`).
8. **Default sort** — by `updated_at` descending (most recently updated first), so a just-edited plan surfaces at the top and matches the table's "Updated" column. Applied at the view layer only; the canonical `sortVerticalPackPlans` (name sort) used by the data layer and mutations is untouched.

## Review follow-ups (codex)

- Reverted the agent-packs default from `active` → `all` (item 4): an `active` default hid new draft/submitted packs after create, reading like a failed action.
- Switched the plan sort from `created_at` → `updated_at` (item 8) so recency tracks the last edit, consistent with the "Updated" column.

## Scope / safety

Presentation + **client-side** derivation only. No API, data-model, or view-model behavior changes — `claw-api`, `packs`, `vertical-pack-plans` lib, React Query wiring, and the live/seed fallback are untouched. Filtering/sorting are pure module-level functions exercised directly by unit tests.

## Verification

- `tsc -b` → 0 errors
- `eslint .` → 0 errors
- `vitest run` → 27 files / 200 tests pass, including view-model tests for both surfaces (agent-packs: default-all newest-first, full-catalogue sort, hidden/visible filter, multi-dimension search; plans: updated_at sort proven by a created-earlier/edited-later case + multi-dimension search).


---

## feat(enterprise-admin): split onboarding registration (#2485)

- **SHA**: `b7d9ee2b290b998b4950cd79a659cc403f00daf8`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-06-16T09:04:47Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/b7d9ee2b290b998b4950cd79a659cc403f00daf8
- **PR**: #2485

### 完整 Commit Message

```
feat(enterprise-admin): split onboarding registration (#2485)

## Summary

- Add `registration_completed` to org responses and updates so
enterprise-admin can separate login from onboarding completion.
- Add `POST /account/team-org` for account registration plus team org
creation, with the new org starting incomplete.
- Update enterprise-admin signup to call `/account/team-org`; direct
signup continues to onboarding, while checkout-driven signup returns to
checkout and can purchase with an incomplete team org.

## Tests

- `/Users/bill/.venvs/claw-interface/bin/pytest
services/claw-interface/tests/unit/test_schema_org.py
services/claw-interface/tests/unit/test_account_team_org_route.py
services/claw-interface/tests/unit/test_enterprise_wiring.py::test_orgs_routes_are_registered
-q`
- `/Users/bill/.venvs/claw-interface/bin/ruff check app/schema/org.py
app/schema/account_api.py app/routes/account.py
tests/unit/test_schema_org.py tests/unit/test_account_team_org_route.py
tests/bdd/step_defs/test_registration.py`
- `/Users/bill/.venvs/claw-interface/bin/ruff format --check
app/schema/org.py app/schema/account_api.py app/routes/account.py
tests/unit/test_schema_org.py tests/unit/test_account_team_org_route.py
tests/bdd/step_defs/test_registration.py`
- `/Users/bill/.venvs/claw-interface/bin/pyright --pythonpath
/Users/bill/.venvs/claw-interface/bin/python app/schema/org.py
app/schema/account_api.py app/routes/account.py
tests/unit/test_schema_org.py tests/unit/test_account_team_org_route.py
tests/bdd/step_defs/test_registration.py`
- `/Users/bill/.venvs/claw-interface/bin/lint-imports`
- `pnpm --dir web/enterprise-admin exec vitest run
lib/__tests__/auth.test.ts app/verify/__tests__/verify.test.tsx
app/__tests__/useEntryViewModel.test.tsx
app/onboarding/__tests__/onboarding-page.test.tsx
'app/vertical-pack-plan/[planId]/checkout/__tests__/checkout-page.test.tsx'
'app/(dashboard)/__tests__/useDashboardLayoutViewModel.test.tsx'`
- `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- `pnpm --dir web/enterprise-admin exec eslint lib/auth.ts
lib/__tests__/auth.test.ts app/verify/__tests__/verify.test.tsx
app/useEntryViewModel.ts app/__tests__/useEntryViewModel.test.tsx
app/onboarding/useOnboardingViewModel.ts
app/onboarding/__tests__/onboarding-page.test.tsx
'app/vertical-pack-plan/[planId]/checkout/useCheckoutViewModel.ts'
'app/vertical-pack-plan/[planId]/checkout/__tests__/checkout-page.test.tsx'
'app/(dashboard)/useDashboardLayoutViewModel.ts'
'app/(dashboard)/__tests__/useDashboardLayoutViewModel.test.tsx'
'app/(dashboard)/users/__tests__/users-page.test.tsx' types/org.ts
types/user-me.ts`

## Notes

- `bash scripts/verify-changed.sh` was attempted after fetching latest
main, but it skipped enterprise-admin because changed web files are
outside `web/app` and skipped backend due toolchain detection not
finding the venv tools. Targeted venv and pnpm checks above passed.
```

### PR Body

## Summary

- Add `registration_completed` to org responses and updates so enterprise-admin can separate login from onboarding completion.
- Add `POST /account/team-org` for account registration plus team org creation, with the new org starting incomplete.
- Update enterprise-admin signup to call `/account/team-org`; direct signup continues to onboarding, while checkout-driven signup returns to checkout and can purchase with an incomplete team org.

## Tests

- `/Users/bill/.venvs/claw-interface/bin/pytest services/claw-interface/tests/unit/test_schema_org.py services/claw-interface/tests/unit/test_account_team_org_route.py services/claw-interface/tests/unit/test_enterprise_wiring.py::test_orgs_routes_are_registered -q`
- `/Users/bill/.venvs/claw-interface/bin/ruff check app/schema/org.py app/schema/account_api.py app/routes/account.py tests/unit/test_schema_org.py tests/unit/test_account_team_org_route.py tests/bdd/step_defs/test_registration.py`
- `/Users/bill/.venvs/claw-interface/bin/ruff format --check app/schema/org.py app/schema/account_api.py app/routes/account.py tests/unit/test_schema_org.py tests/unit/test_account_team_org_route.py tests/bdd/step_defs/test_registration.py`
- `/Users/bill/.venvs/claw-interface/bin/pyright --pythonpath /Users/bill/.venvs/claw-interface/bin/python app/schema/org.py app/schema/account_api.py app/routes/account.py tests/unit/test_schema_org.py tests/unit/test_account_team_org_route.py tests/bdd/step_defs/test_registration.py`
- `/Users/bill/.venvs/claw-interface/bin/lint-imports`
- `pnpm --dir web/enterprise-admin exec vitest run lib/__tests__/auth.test.ts app/verify/__tests__/verify.test.tsx app/__tests__/useEntryViewModel.test.tsx app/onboarding/__tests__/onboarding-page.test.tsx 'app/vertical-pack-plan/[planId]/checkout/__tests__/checkout-page.test.tsx' 'app/(dashboard)/__tests__/useDashboardLayoutViewModel.test.tsx'`
- `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- `pnpm --dir web/enterprise-admin exec eslint lib/auth.ts lib/__tests__/auth.test.ts app/verify/__tests__/verify.test.tsx app/useEntryViewModel.ts app/__tests__/useEntryViewModel.test.tsx app/onboarding/useOnboardingViewModel.ts app/onboarding/__tests__/onboarding-page.test.tsx 'app/vertical-pack-plan/[planId]/checkout/useCheckoutViewModel.ts' 'app/vertical-pack-plan/[planId]/checkout/__tests__/checkout-page.test.tsx' 'app/(dashboard)/useDashboardLayoutViewModel.ts' 'app/(dashboard)/__tests__/useDashboardLayoutViewModel.test.tsx' 'app/(dashboard)/users/__tests__/users-page.test.tsx' types/org.ts types/user-me.ts`

## Notes

- `bash scripts/verify-changed.sh` was attempted after fetching latest main, but it skipped enterprise-admin because changed web files are outside `web/app` and skipped backend due toolchain detection not finding the venv tools. Targeted venv and pnpm checks above passed.


---

## docs(dashboard-console): fix dead account URL placeholder in .env.example (#2468)

- **SHA**: `b3af49c33c2fdcfce08a0bbb5bc011d3953cc72e`
- **作者**: david-srp (david-srp)
- **日期**: 2026-06-16T08:42:14Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/b3af49c33c2fdcfce08a0bbb5bc011d3953cc72e
- **PR**: #2468

### 完整 Commit Message

```
docs(dashboard-console): fix dead account URL placeholder in .env.example (#2468)

Closes part of #2467 (the quick, low-risk piece).

## What

`web/dashboard-console/.env.example` shipped
`VITE_ACCOUNT_URL=https://account.ecap.yesy.live`, which is
**NXDOMAIN**. Anyone copying the example to `.env` and clicking
**Continue with Google** completes the Firebase popup and then fails the
token exchange with `ERR_NAME_NOT_RESOLVED`.

This PR:
1. Points `VITE_ACCOUNT_URL` at the staging account service
`https://account.favie.yesy.live` (same `*.yesy.live` family as the
existing `VITE_CLAW_INTERFACE_URL`; **verified by a successful local
login**), and notes prod is `https://account.gsmo.ai`.
2. Documents that `VITE_FIREBASE_*` are the `srp-ecap-staging` web
config values — the same ones `web/app` ships as
`NEXT_PUBLIC_FIREBASE_*`, just re-prefixed for Vite (only
`VITE_`-prefixed vars reach the browser). This rename was a non-obvious
gotcha when copying keys from web/app.

## Scope

Comment + placeholder change in a single `.env.example` template. No
code, no committed secrets (Firebase values stay blank in the template).

## Please confirm

`account.favie.yesy.live` was **inferred from the domain family +
DNS-verified + confirmed by a real login**, but the authoritative
staging hostname is owned by whoever runs the ecap deployment — please
sanity-check it. The broader doc/scripts work is tracked in #2467.

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

Closes part of #2467 (the quick, low-risk piece).

## What

`web/dashboard-console/.env.example` shipped `VITE_ACCOUNT_URL=https://account.ecap.yesy.live`, which is **NXDOMAIN**. Anyone copying the example to `.env` and clicking **Continue with Google** completes the Firebase popup and then fails the token exchange with `ERR_NAME_NOT_RESOLVED`.

This PR:
1. Points `VITE_ACCOUNT_URL` at the staging account service `https://account.favie.yesy.live` (same `*.yesy.live` family as the existing `VITE_CLAW_INTERFACE_URL`; **verified by a successful local login**), and notes prod is `https://account.gsmo.ai`.
2. Documents that `VITE_FIREBASE_*` are the `srp-ecap-staging` web config values — the same ones `web/app` ships as `NEXT_PUBLIC_FIREBASE_*`, just re-prefixed for Vite (only `VITE_`-prefixed vars reach the browser). This rename was a non-obvious gotcha when copying keys from web/app.

## Scope

Comment + placeholder change in a single `.env.example` template. No code, no committed secrets (Firebase values stay blank in the template).

## Please confirm

`account.favie.yesy.live` was **inferred from the domain family + DNS-verified + confirmed by a real login**, but the authoritative staging hostname is owned by whoever runs the ecap deployment — please sanity-check it. The broader doc/scripts work is tracked in #2467.

---

## feat(openclaw): add computer lifecycle backend (#2471)

- **SHA**: `eb803967d2be16e5080735cbaf1c58784769af94`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-06-16T08:32:13Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/eb803967d2be16e5080735cbaf1c58784769af94
- **PR**: #2471

### 完整 Commit Message

```
feat(openclaw): add computer lifecycle backend (#2471)

## Summary
- add backend computer lifecycle support for create/list/start/redeploy
flows
- move OpenClaw computer creation into a dedicated service used by
account registration and explicit computer creation
- add unit coverage for account initialization, computer routes, and
computer services

## Local Checks
- `git diff --check -- services/claw-interface` passed
- `services/claw-interface/.venv/bin/python -m py_compile ...` passed
for changed backend files
- `bash scripts/verify-py.sh` passes `ruff check` and `ruff format
--check`; local run cannot complete because `pyright` and `lint-imports`
are not installed in this environment
- targeted `services/claw-interface/.venv/bin/python -m pytest ...`
cannot run because `.venv` has no `pytest`
- targeted `uv run pytest ...` is blocked by the existing editable build
parsing issue for
`git+https://github.com/SerendipityOneInc/favie-common.git@v0.3.66`

## Notes
- Split from #2470 so backend lifecycle changes can review independently
from the frontend init-route removal.
```

### PR Body

## Summary
- add backend computer lifecycle support for create/list/start/redeploy flows
- move OpenClaw computer creation into a dedicated service used by account registration and explicit computer creation
- add unit coverage for account initialization, computer routes, and computer services

## Local Checks
- `git diff --check -- services/claw-interface` passed
- `services/claw-interface/.venv/bin/python -m py_compile ...` passed for changed backend files
- `bash scripts/verify-py.sh` passes `ruff check` and `ruff format --check`; local run cannot complete because `pyright` and `lint-imports` are not installed in this environment
- targeted `services/claw-interface/.venv/bin/python -m pytest ...` cannot run because `.venv` has no `pytest`
- targeted `uv run pytest ...` is blocked by the existing editable build parsing issue for `git+https://github.com/SerendipityOneInc/favie-common.git@v0.3.66`

## Notes
- Split from #2470 so backend lifecycle changes can review independently from the frontend init-route removal.


---

## feat(landing-context): deliver PPT Master Remix cover image as a chat attachment (#2466)

- **SHA**: `7c5838d6b86c4b6ee1d69380d15549be91dece80`
- **作者**: shana-srp (shana-maker)
- **日期**: 2026-06-16T08:22:11Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/7c5838d6b86c4b6ee1d69380d15549be91dece80
- **PR**: #2466

### 完整 Commit Message

```
feat(landing-context): deliver PPT Master Remix cover image as a chat attachment (#2466)

## What

Completes the **PPT Master "Remix"** hand-off on the chat side: a picked
template's **cover screenshot** is now delivered to the agent as a real
Mattermost **attachment** (not just a URL in the prompt text), sent
imperceptibly through the existing landing auto-send flow.

Producer side ships in `zooclaw-tips`
(SerendipityOneInc/zooclaw-tips#54): the gallery writes
`initial_query.images = [coverUrl]` + `auto_send` into
`ecap:landingContext`. This PR makes the consumer honor both.

Two commits:

1. **Carry the contract** — `landing-context.ts` previously rebuilt the
stored context as `initial_query: { text }` only, silently dropping any
producer-supplied `images` / `auto_send`. Now both are preserved
(sanitized: string-only image entries, capped at 8; `auto_send` accepts
only literal `true`), attached only when present so text-only hand-offs
keep their minimal shape.
2. **Deliver the images** — wire `initial_query.images` through the
auto-send path so they upload + attach to the message.

## How

- `blob.ts` — `fetchExternalBlob()` pulls a third-party image
**without** bearer auth (never leak the MM token to a foreign origin;
subject to the remote's CORS).
- `useMmAttachments` — `uploadExternalImageUrls()` fetches each URL,
uploads to the channel, returns file ids; isolated from the composer's
attachment UI state (the message is programmatic, no preview chips).
- `useChatMessaging` — `handleSendMessage()` accepts explicit `fileIds`
(bypasses the render-lagged attachment-state consumption that would drop
a same-tick upload); `handleSendMessageWithImages()` uploads then sends
text + ids.
- `useLandingContextFlow` / `GenClawClient` — thread images through
`onAutoSendInitialQuery`, passing them only when present.

## Notes

- **Best-effort images**: if every upload fails (CORS, network), it
falls back to sending text alone — the cover URL is already embedded in
the prompt text, so the agent isn't left empty-handed.
- **CORS caveat**: browser must fetch the image bytes to re-upload, so
delivery depends on the image origin's CORS. `raw.githubusercontent.com`
returns `ACAO:*` (works); other origins without CORS headers degrade to
text-only. A server-side proxy would remove this dependency (out of
scope here).

## Test

- `tsc --noEmit` clean.
- 132 unit tests pass across `landing-context`, `useMmAttachments`,
`useChatMessaging`, `useLandingContextFlow` (incl. new images-carry +
images-forwarding tests).

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What

Completes the **PPT Master "Remix"** hand-off on the chat side: a picked template's **cover screenshot** is now delivered to the agent as a real Mattermost **attachment** (not just a URL in the prompt text), sent imperceptibly through the existing landing auto-send flow.

Producer side ships in `zooclaw-tips` (SerendipityOneInc/zooclaw-tips#54): the gallery writes `initial_query.images = [coverUrl]` + `auto_send` into `ecap:landingContext`. This PR makes the consumer honor both.

Two commits:

1. **Carry the contract** — `landing-context.ts` previously rebuilt the stored context as `initial_query: { text }` only, silently dropping any producer-supplied `images` / `auto_send`. Now both are preserved (sanitized: string-only image entries, capped at 8; `auto_send` accepts only literal `true`), attached only when present so text-only hand-offs keep their minimal shape.
2. **Deliver the images** — wire `initial_query.images` through the auto-send path so they upload + attach to the message.

## How

- `blob.ts` — `fetchExternalBlob()` pulls a third-party image **without** bearer auth (never leak the MM token to a foreign origin; subject to the remote's CORS).
- `useMmAttachments` — `uploadExternalImageUrls()` fetches each URL, uploads to the channel, returns file ids; isolated from the composer's attachment UI state (the message is programmatic, no preview chips).
- `useChatMessaging` — `handleSendMessage()` accepts explicit `fileIds` (bypasses the render-lagged attachment-state consumption that would drop a same-tick upload); `handleSendMessageWithImages()` uploads then sends text + ids.
- `useLandingContextFlow` / `GenClawClient` — thread images through `onAutoSendInitialQuery`, passing them only when present.

## Notes

- **Best-effort images**: if every upload fails (CORS, network), it falls back to sending text alone — the cover URL is already embedded in the prompt text, so the agent isn't left empty-handed.
- **CORS caveat**: browser must fetch the image bytes to re-upload, so delivery depends on the image origin's CORS. `raw.githubusercontent.com` returns `ACAO:*` (works); other origins without CORS headers degrade to text-only. A server-side proxy would remove this dependency (out of scope here).

## Test

- `tsc --noEmit` clean.
- 132 unit tests pass across `landing-context`, `useMmAttachments`, `useChatMessaging`, `useLandingContextFlow` (incl. new images-carry + images-forwarding tests).


---

## fix(billing): reduce expected invoice and user 404 noise (#2297)

- **SHA**: `0f2c523e3339cbe23fa6abf3d9d89becf287c394`
- **作者**: Chris@ZooClaw (chris-srp)
- **日期**: 2026-06-16T07:32:25Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/0f2c523e3339cbe23fa6abf3d9d89becf287c394
- **PR**: #2297

### 完整 Commit Message

```
fix(billing): reduce expected invoice and user 404 noise (#2297)

## Summary
- Add backend `invoice_available` to order responses so invoice download
visibility follows provider invoice availability.
- Hide invoice Download for paid Stripe rows without a hosted invoice
id.
- Retry transient `/users/get` 404s during login bootstrap from the
current React Query user-business-data path.
- Mark only intermediate `/api/users/get` retry attempts for Sentry
filtering; an exhausted final 404 remains visible.
- Drop handled invoice-download 404 noise from Sentry for the precise
invoice endpoint pattern.

## Root cause
Paid Stripe order rows were rendered as downloadable based only on
`payment_channel === "stripe"`, but some renewal/payment rows do not yet
carry `provider_invoice_id`, so clicking Download correctly fell through
to `/orders/{orderId}/invoice` 404.

Separately, `/api/users/get` can briefly return 404 during account
bootstrap. The UI should retry those transient responses, but persistent
404s still need to reach Sentry because they may indicate a real missing
business-user record.

## Review follow-up
- Rebased the PR onto the latest `main` and removed the stale conflict
with the retired `user-business-data-cache.ts` module.
- Migrated the bootstrap 404 retry behavior into
`web/app/src/lib/api/user-business-data.ts`, the current shared React
Query query function.
- Kept the Codex review boundary: only explicitly marked intermediate
retry attempts use `ecap_expected_404=user_bootstrap_retry`;
unmarked/final `/api/users/get` 404s are still reported.
- Made the retry backoff abort-aware so `cancelQueries` does not wait
for the 300/800/1500ms delay before observing cancellation.
- Disabled the outer React Query retry for the user-business-data hook
and imperative `fetchQuery` paths, so the internal 4-attempt bootstrap
window does not run twice under the global `retry: 1` default.
- Kept `invoice_available` as the backend-owned invariant. Frontend uses
strict `=== true`, so old/undefined responses degrade to hiding a broken
Download button instead of showing one that 404s.

## Test plan
- [x] `bash scripts/verify-web.sh web/app/src/lib/api/user.ts
web/app/src/lib/api/user-business-data.ts
web/app/src/contexts/UserBusinessDataContext.tsx
web/app/src/components/billing/InvoiceHistory.tsx
web/app/sentry.client.config.ts
web/app/tests/unit/lib/api/user.unit.spec.ts
web/app/tests/unit/lib/api/user-business-data.unit.spec.ts
web/app/tests/unit/contexts/UserBusinessDataContext.unit.spec.tsx
web/app/tests/unit/components/billing/InvoiceHistory.unit.spec.tsx
web/app/tests/unit/config/sentry-client-config.unit.spec.ts`
- [x] `pnpm --filter @zooclaw/web-app exec vitest run --config
./vitest.config.mts tests/unit/lib/api/user-business-data.unit.spec.ts
tests/unit/contexts/UserBusinessDataContext.unit.spec.tsx`
- [x]
`/Users/xuwenhao/Codebase/srpone/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python
-m ruff check app/schema/order.py
app/services/billing_v2/order_requests.py
tests/unit/test_billing_v2_order_requests.py`
- [x]
`/Users/xuwenhao/Codebase/srpone/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python
-m ruff format --check app/schema/order.py
app/services/billing_v2/order_requests.py
tests/unit/test_billing_v2_order_requests.py`
- [x]
`/Users/xuwenhao/Codebase/srpone/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python
-m pytest tests/unit/test_billing_v2_order_requests.py -q`
- [x] `pyright app/schema/order.py
app/services/billing_v2/order_requests.py
tests/unit/test_billing_v2_order_requests.py --pythonpath
/Users/xuwenhao/Codebase/srpone/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python`
- [x]
`/Users/xuwenhao/Codebase/srpone/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/lint-imports`

Note: `bash scripts/verify-local.sh --changed` passed the web side, then
hit local macOS backend pyright dependency-resolution noise
(`reportMissingImports` across unrelated FastAPI/favie_common imports).
Targeted backend pyright for the changed files passed; CI remains the
authoritative full backend check.
```

### PR Body

## Summary
- Add backend `invoice_available` to order responses so invoice download visibility follows provider invoice availability.
- Hide invoice Download for paid Stripe rows without a hosted invoice id.
- Retry transient `/users/get` 404s during login bootstrap from the current React Query user-business-data path.
- Mark only intermediate `/api/users/get` retry attempts for Sentry filtering; an exhausted final 404 remains visible.
- Drop handled invoice-download 404 noise from Sentry for the precise invoice endpoint pattern.

## Root cause
Paid Stripe order rows were rendered as downloadable based only on `payment_channel === "stripe"`, but some renewal/payment rows do not yet carry `provider_invoice_id`, so clicking Download correctly fell through to `/orders/{orderId}/invoice` 404.

Separately, `/api/users/get` can briefly return 404 during account bootstrap. The UI should retry those transient responses, but persistent 404s still need to reach Sentry because they may indicate a real missing business-user record.

## Review follow-up
- Rebased the PR onto the latest `main` and removed the stale conflict with the retired `user-business-data-cache.ts` module.
- Migrated the bootstrap 404 retry behavior into `web/app/src/lib/api/user-business-data.ts`, the current shared React Query query function.
- Kept the Codex review boundary: only explicitly marked intermediate retry attempts use `ecap_expected_404=user_bootstrap_retry`; unmarked/final `/api/users/get` 404s are still reported.
- Made the retry backoff abort-aware so `cancelQueries` does not wait for the 300/800/1500ms delay before observing cancellation.
- Disabled the outer React Query retry for the user-business-data hook and imperative `fetchQuery` paths, so the internal 4-attempt bootstrap window does not run twice under the global `retry: 1` default.
- Kept `invoice_available` as the backend-owned invariant. Frontend uses strict `=== true`, so old/undefined responses degrade to hiding a broken Download button instead of showing one that 404s.

## Test plan
- [x] `bash scripts/verify-web.sh web/app/src/lib/api/user.ts web/app/src/lib/api/user-business-data.ts web/app/src/contexts/UserBusinessDataContext.tsx web/app/src/components/billing/InvoiceHistory.tsx web/app/sentry.client.config.ts web/app/tests/unit/lib/api/user.unit.spec.ts web/app/tests/unit/lib/api/user-business-data.unit.spec.ts web/app/tests/unit/contexts/UserBusinessDataContext.unit.spec.tsx web/app/tests/unit/components/billing/InvoiceHistory.unit.spec.tsx web/app/tests/unit/config/sentry-client-config.unit.spec.ts`
- [x] `pnpm --filter @zooclaw/web-app exec vitest run --config ./vitest.config.mts tests/unit/lib/api/user-business-data.unit.spec.ts tests/unit/contexts/UserBusinessDataContext.unit.spec.tsx`
- [x] `/Users/xuwenhao/Codebase/srpone/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python -m ruff check app/schema/order.py app/services/billing_v2/order_requests.py tests/unit/test_billing_v2_order_requests.py`
- [x] `/Users/xuwenhao/Codebase/srpone/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python -m ruff format --check app/schema/order.py app/services/billing_v2/order_requests.py tests/unit/test_billing_v2_order_requests.py`
- [x] `/Users/xuwenhao/Codebase/srpone/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python -m pytest tests/unit/test_billing_v2_order_requests.py -q`
- [x] `pyright app/schema/order.py app/services/billing_v2/order_requests.py tests/unit/test_billing_v2_order_requests.py --pythonpath /Users/xuwenhao/Codebase/srpone/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/python`
- [x] `/Users/xuwenhao/Codebase/srpone/zooclaw/ecap-workspace/services/claw-interface/.venv/bin/lint-imports`

Note: `bash scripts/verify-local.sh --changed` passed the web side, then hit local macOS backend pyright dependency-resolution noise (`reportMissingImports` across unrelated FastAPI/favie_common imports). Targeted backend pyright for the changed files passed; CI remains the authoritative full backend check.


---

## fix(web): proxy claw requests through api route (#2482)

- **SHA**: `9bd0733ef38580a4cd4e8395a4d0e3dd148050ce`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-06-16T07:27:36Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/9bd0733ef38580a4cd4e8395a4d0e3dd148050ce
- **PR**: #2482

### 完整 Commit Message

```
fix(web): proxy claw requests through api route (#2482)

## Summary
- Add a same-origin `/api/claw/[...path]` proxy for `web/app`
claw-interface traffic.
- Route `callClawInterfaceAPI` through `/api/claw` so browser callers no
longer require `NEXT_PUBLIC_CLAW_INTERFACE_URL`.
- Forward `Authorization` when present, otherwise derive bearer auth
from the HttpOnly `zc_session` cookie, and move org agent pack service
calls onto the shared helper.

## Tests
- `pnpm --dir web/app exec vitest run
tests/unit/lib/api/claw-interface.unit.spec.ts
tests/unit/lib/api/claw-proxy.unit.spec.ts
tests/unit/services/org-agent-packs.unit.spec.ts`
- `pnpm --dir web/app exec vitest run tests/unit/services`
- `pnpm --dir web/app exec tsc --noEmit`
- `bash scripts/verify-web.sh web/app/src/lib/api/claw-interface.ts
web/app/src/lib/api/claw-proxy.ts
'web/app/src/app/api/claw/[...path]/route.ts'
web/app/src/services/org-agent-packs.ts
web/app/tests/unit/lib/api/claw-interface.unit.spec.ts
web/app/tests/unit/lib/api/claw-proxy.unit.spec.ts
web/app/tests/unit/services/org-agent-packs.unit.spec.ts`
- `bash scripts/verify-changed.sh`
```

### PR Body

## Summary
- Add a same-origin `/api/claw/[...path]` proxy for `web/app` claw-interface traffic.
- Route `callClawInterfaceAPI` through `/api/claw` so browser callers no longer require `NEXT_PUBLIC_CLAW_INTERFACE_URL`.
- Forward `Authorization` when present, otherwise derive bearer auth from the HttpOnly `zc_session` cookie, and move org agent pack service calls onto the shared helper.

## Tests
- `pnpm --dir web/app exec vitest run tests/unit/lib/api/claw-interface.unit.spec.ts tests/unit/lib/api/claw-proxy.unit.spec.ts tests/unit/services/org-agent-packs.unit.spec.ts`
- `pnpm --dir web/app exec vitest run tests/unit/services`
- `pnpm --dir web/app exec tsc --noEmit`
- `bash scripts/verify-web.sh web/app/src/lib/api/claw-interface.ts web/app/src/lib/api/claw-proxy.ts 'web/app/src/app/api/claw/[...path]/route.ts' web/app/src/services/org-agent-packs.ts web/app/tests/unit/lib/api/claw-interface.unit.spec.ts web/app/tests/unit/lib/api/claw-proxy.unit.spec.ts web/app/tests/unit/services/org-agent-packs.unit.spec.ts`
- `bash scripts/verify-changed.sh`

