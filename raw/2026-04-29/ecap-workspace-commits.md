# ecap-workspace — 2026-04-29 Commits
## ae86454e — 2026-04-29T14:10:29Z
**Author:** bill-srp

**Message:**
```
feat(ios): redesign AgentsView, add agent update flow (#1469)

## Summary

Redesigns AgentsView (the agent catalog) to match the Zoo Square v2
EXPLORE design and adds a new agent-update affordance plus a global
"agent hired" toast that survives tab switches.

### Key changes
- **EXPLORE-style row layout**: gradient background, HankenGrotesk
typography, dark navy active pill, dynamic category tabs driven by the
catalog response
- **Liquid glass menu button** (iOS 26) — fixed a latent `#if
swift(>=6.2)` gate that was preprocessing the effect out under
`SWIFT_VERSION=5.0`
- **API-driven categories**: removed the hardcoded `AgentCategory` enum;
`selectedCategory: String?` filters live against catalog `category`
values, deduped case-insensitively
- **Reusable `Toast` component** (`Views/Components/Toast.swift`) with
optional avatar/icon/emoji + action button, plus a
`.toast(item:autoDismissAfter:)` view modifier
- **Agent update flow**: when `UserAgent.has_update == true`, row shows
`plus.arrow.trianglehead.clock` + a "NEW" pill; tap calls `POST
/openclaw/agents/{id}/redeploy` (synchronous), refreshes user agents
- **Hired toast is now global** — lives on `AppShellView` (Layer 4 in
the shell ZStack) so it persists across tab switches; "Say hi" navigates
to chat
- **Hired-action simplification**: ellipsis sheet (Chat Now / Fire /
Cancel) replaced with a direct `ellipsis.message`-tap that opens chat
- **Centralized colors**: promoted `deepNavy` (#0B0F1A), `accentRed`
(#E63946), `coolTextSecondary` (#5A6478), `coolBorderLight` (#E8EBF0) to
top-level AppTheme; collapsed 5+ duplicate hex literals across
PaywallView, VoiceWaveformView, RedeemGiftCodeView, ComposeInputPanel
- **Model alignment with backend**: removed `AgentCatalogItem.isNew`
(backend never produced `is_new`); removed `UserAgent.isDefault`
(backend never produced it either; SidebarDrawerView now distinguishes
the main agent by `id == "main"`)

### Backend touchpoints (already shipped)
- `POST /openclaw/agents/{agent_id}/redeploy` — used by the new update
flow
- `GET /openclaw/agents` — `has_update` field per agent (computed in
`services/openclaw/agent_response.py`)

## Test plan
- [ ] Open AgentsView — verify EXPLORE layout, gradient background,
category tabs populated from catalog
- [ ] Liquid glass menu button visible at top-left and refracts content
beneath
- [ ] Tap `+` on an unhired agent — verify hire completes, "Hired!"
toast slides in from the top with avatar + "Say hi"
- [ ] Switch to chat tab while toast is on screen — toast persists
- [ ] Tap "Say hi" — navigates to chat with that agent
- [ ] Wait 5s without action — toast auto-dismisses
- [ ] Hire a second agent rapidly — second toast replaces the first with
a fresh 5s timer
- [ ] For an agent with `has_update == true` — NEW pill on title and
update icon on the right; tap shows spinner during redeploy and clears
`has_update` after refresh
- [ ] For a hired agent — tap `ellipsis.message` icon — opens chat
directly (no sheet)
- [ ] Filter by category — verify only matching agents show; tap "All"
pill returns full catalog
- [ ] `xcodebuild test -only-testing:ZooClawTests/AgentServiceTests
-only-testing:ZooClawTests/AgentViewModelTests` passes
- [ ] `swiftlint --strict` — 0 violations

## Notes
- 11 commits, each independently buildable. Linear history, fully
rebased on latest `main`.
- Backend has no per-agent `update` endpoint; we use the existing
`redeploy` which atomically pulls the latest catalog version.
Synchronous on the server, so iOS doesn't need polling.
- The new `Toast` component is generic — `RedeemSuccessToast` /
`ModelDegradationToast` could migrate to it in a follow-up if desired.
```

**PR #1469:** feat(ios): redesign AgentsView, add agent update flow

**PR Body:**
## Summary

Redesigns AgentsView (the agent catalog) to match the Zoo Square v2 EXPLORE design and adds a new agent-update affordance plus a global "agent hired" toast that survives tab switches.

### Key changes
- **EXPLORE-style row layout**: gradient background, HankenGrotesk typography, dark navy active pill, dynamic category tabs driven by the catalog response
- **Liquid glass menu button** (iOS 26) — fixed a latent `#if swift(>=6.2)` gate that was preprocessing the effect out under `SWIFT_VERSION=5.0`
- **API-driven categories**: removed the hardcoded `AgentCategory` enum; `selectedCategory: String?` filters live against catalog `category` values, deduped case-insensitively
- **Reusable `Toast` component** (`Views/Components/Toast.swift`) with optional avatar/icon/emoji + action button, plus a `.toast(item:autoDismissAfter:)` view modifier
- **Agent update flow**: when `UserAgent.has_update == true`, row shows `plus.arrow.trianglehead.clock` + a "NEW" pill; tap calls `POST /openclaw/agents/{id}/redeploy` (synchronous), refreshes user agents
- **Hired toast is now global** — lives on `AppShellView` (Layer 4 in the shell ZStack) so it persists across tab switches; "Say hi" navigates to chat
- **Hired-action simplification**: ellipsis sheet (Chat Now / Fire / Cancel) replaced with a direct `ellipsis.message`-tap that opens chat
- **Centralized colors**: promoted `deepNavy` (#0B0F1A), `accentRed` (#E63946), `coolTextSecondary` (#5A6478), `coolBorderLight` (#E8EBF0) to top-level AppTheme; collapsed 5+ duplicate hex literals across PaywallView, VoiceWaveformView, RedeemGiftCodeView, ComposeInputPanel
- **Model alignment with backend**: removed `AgentCatalogItem.isNew` (backend never produced `is_new`); removed `UserAgent.isDefault` (backend never produced it either; SidebarDrawerView now distinguishes the main agent by `id == "main"`)

### Backend touchpoints (already shipped)
- `POST /openclaw/agents/{agent_id}/redeploy` — used by the new update flow
- `GET /openclaw/agents` — `has_update` field per agent (computed in `services/openclaw/agent_response.py`)

## Test plan
- [ ] Open AgentsView — verify EXPLORE layout, gradient background, category tabs populated from catalog
- [ ] Liquid glass menu button visible at top-left and refracts content beneath
- [ ] Tap `+` on an unhired agent — verify hire completes, "Hired!" toast slides in from the top with avatar + "Say hi"
- [ ] Switch to chat tab while toast is on screen — toast persists
- [ ] Tap "Say hi" — navigates to chat with that agent
- [ ] Wait 5s without action — toast auto-dismisses
- [ ] Hire a second agent rapidly — second toast replaces the first with a fresh 5s timer
- [ ] For an agent with `has_update == true` — NEW pill on title and update icon on the right; tap shows spinner during redeploy and clears `has_update` after refresh
- [ ] For a hired agent — tap `ellipsis.message` icon — opens chat directly (no sheet)
- [ ] Filter by category — verify only matching agents show; tap "All" pill returns full catalog
- [ ] `xcodebuild test -only-testing:ZooClawTests/AgentServiceTests -only-testing:ZooClawTests/AgentViewModelTests` passes
- [ ] `swiftlint --strict` — 0 violations

## Notes
- 11 commits, each independently buildable. Linear history, fully rebased on latest `main`.
- Backend has no per-agent `update` endpoint; we use the existing `redeploy` which atomically pulls the latest catalog version. Synchronous on the server, so iOS doesn't need polling.
- The new `Toast` component is generic — `RedeemSuccessToast` / `ModelDegradationToast` could migrate to it in a follow-up if desired.

**Stats:** +1456 -434 (1890 changes)

---

## 68f36e2c — 2026-04-29T13:01:45Z
**Author:** Chris@ZooClaw

**Message:**
```
test(web): migrate inline queryBy*().toBeNull() to jest-dom (#1046) (#1478)

## Summary
Follow-up to #1029 jest-dom adoption. Two parts:

1. **Migrate 78 inline RTL presence assertions across 15 files**
- 46 sites in 11 `tests/unit/app/` files (the `app/` batch noted in
#1046)
- 32 sites in 4 `tests/unit/components/` files that #1029's
`.toBeDefined()` migration script didn't touch (it migrated the positive
form but not `.toBeNull()` / `.not.toBeNull()` on `queryBy*`)
   - Transforms (mirror of #1029):
- `expect((screen.)?queryBy*(...)).toBeNull()` →
`.not.toBeInTheDocument()`
- `expect((screen.)?queryBy*(...)).not.toBeNull()` →
`.toBeInTheDocument()`
- `expect(screen.getByText(...)).not.toBeNull()` →
`.toBeInTheDocument()` (one site in `agents-manager-publish`)
- Variable-reference forms (~91 sites in `app/`, getAttribute on local
consts) remain out of scope — they need per-site type tracing.

2. **Add symmetric `no-restricted-syntax` lint guards for
`tests/unit/**`** mirroring #1029's `.toBeDefined()` rule:
   - bans `expect(queryBy*(...)).toBeNull()`
   - bans `expect(queryBy*(...)).not.toBeNull()`
The rule's existing-violation list was the 32 sites in `components/`
cleaned up in part 1.

## Out of scope
- `tests/unit/hooks/` — survey found 0 zero-ambiguity inline candidates
(the issue's "biggest payoff" call was based on `render`/import counts,
not on actual assertion patterns; hook tests assert on
`result.current.*`, not DOM nodes). No PR worth doing.
- Variable-reference forms (e.g. `const el = getByTestId(...);
expect(el).not.toBeNull()`) — per-site type tracing, separate PR.
- Hygiene items still on #1046: `pnpm.overrides` location,
`@xyflow/system` transitive vitest@1.6.1 dedup.

## Test plan
- [x] `pnpm lint` green (cache clean — both new lint selectors pass
after part 1)
- [x] `npx tsc --noEmit` green
- [x] `pnpm test:unit` on all 15 affected files → 364 passed / 1 todo, 0
new failures
- [ ] CI `code-quality / lint-and-test` green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR #1046:** 

**Stats:** +114 -78 (192 changes)

---

## 8ac54c60 — 2026-04-29T12:45:02Z
**Author:** Chris@ZooClaw

**Message:**
```
fix(web): sanitize video URL in <video> attribute (#1328) (#1462)

## Summary

`lib/api/chat.ts` 的 `sendVideoGeneration` 之前把 `videoItem.url` 原样塞进
template literal 的 \`<video controls src=\"\${url}\">\`。如果 URL 出现
\`\"\`,attribute 边界被打破,后面的内容会被 HTML 解析成相邻属性(如 \`onload=\"alert(1)\"\`)——
而这串内容是会被存进 chat session 然后回放成 HTML 的。\`b64_json\` 分支由 data-URL 前缀和
base64 字符集约束,实际暴露面是 URL 分支。

抽 \`buildVideoResponseContentHtml(src)\`,改用
\`document.createElement('video')\` + \`outerHTML\` —— 让浏览器 HTML
serializer 按 WHATWG 规范处理 attribute escaping(\`&\` → \`&amp;\`, \`\"\` →
\`&quot;\`)。一个含 \`\"\` 的 URL 在序列化→重解析后会**圆环回到原值**,不会冒出新属性。

## Test

新建 \`tests/unit/lib/api/chat.unit.spec.ts\`,3 个用例:

- 安全 URL 输出 baseline 形式(controls + src + style)
- \`data:video/mp4;base64,...\` 原样保留
- **回归断言**(#1328):一组带 \`\"\` / \`&\` / \`<\` / 拼接 \`onerror=...\` 的
tricky URL,断言 \`getAttribute('src')\` 与原 URL 完全相等,且 attribute 名集合恒为
\`['controls', 'src', 'style']\`(无注入)

本地反向验证:把 helper 临时改回 template-literal 形式,回归用例报 \`expected
'https://x.com/a' to be 'https://x.com/a\"b.mp4'\` —— 测试确实拦得住
regression。

## Closes

Closes #1328

## Test plan

- [x] \`pnpm test:unit tests/unit/lib/api/chat.unit.spec.ts\` (3/3)
- [x] \`pnpm test:unit tests/unit/hooks/useLiteLLMApi.unit.spec.ts\` (现有
caller 不受影响)
- [x] \`npx tsc --noEmit\` clean
- [x] \`npx eslint\` / \`npx prettier --check\` clean
- [ ] CI: code-quality / lint-and-test
```

**PR #1328:** 

**Stats:** +76 -1 (77 changes)

---

## 1bbc071d — 2026-04-29T12:20:18Z
**Author:** nolan-srp

**Message:**
```
fix(openclaw): wait for async agent operations (#1475)

## Summary
- switch incremental hire and fire flows to the async install and
uninstall endpoints
- wait for agent operations to finish before refreshing frontend agent
state
- centralize async operation polling and failure handling in the
OpenClaw API client
```

**PR #1475:** fix(openclaw): wait for async agent operations

**PR Body:**
## Summary
- switch incremental hire and fire flows to the async install and uninstall endpoints
- wait for agent operations to finish before refreshing frontend agent state
- centralize async operation polling and failure handling in the OpenClaw API client

**Stats:** +292 -39 (331 changes)

---

## d3ef7a9d — 2026-04-29T11:33:24Z
**Author:** peter-srp

**Message:**
```
chore: remove unused STRIPE_PUBLISHABLE_KEY (#1474)

## Summary
- Remove `STRIPE_PUBLISHABLE_KEY` from backend settings, `.env.example`,
and setup docs
- This env var was defined but never referenced in any code path
(frontend or backend)
- Publishable keys (`pk_`) are public by design and don't need
server-side config
- Part of a key-leak audit; `pydantic-settings` `extra="ignore"` means
no env cleanup needed

## Test plan
- [ ] CI passes (no code references this field)
- [ ] Backend starts without `STRIPE_PUBLISHABLE_KEY` in env (already
the case — field had empty default)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

**PR #1474:** chore: remove unused STRIPE_PUBLISHABLE_KEY

**PR Body:**
## Summary
- Remove `STRIPE_PUBLISHABLE_KEY` from backend settings, `.env.example`, and setup docs
- This env var was defined but never referenced in any code path (frontend or backend)
- Publishable keys (`pk_`) are public by design and don't need server-side config
- Part of a key-leak audit; `pydantic-settings` `extra="ignore"` means no env cleanup needed

## Test plan
- [ ] CI passes (no code references this field)
- [ ] Backend starts without `STRIPE_PUBLISHABLE_KEY` in env (already the case — field had empty default)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

**Stats:** +0 -3 (3 changes)

---

## fbf78e35 — 2026-04-29T10:40:18Z
**Author:** bill-srp

**Message:**
```
feat(ios): Post-auth onboarding view redesigns (PR-B of 2) (#1467)

## Summary

**PR-B of 2** in the onboarding redesign split. Companion to #1458
(PR-A, **merged**). Ships the Figma redesigns of the four post-auth
views.

After this PR lands, the visual onboarding refresh is feature-complete:
hero → name → role → useCase → register → OTP → agentSelect →
notifications → setupLoading all use the new design.

### EmailOTPLoginView
- 6-box OTP grid with invisible `TextField` driving iOS one-time-code
autofill from SMS / Mail.
- Resend button reads the email back from `authViewModel.emailOTPState`
(fix for the bug PR-A's review caught — previously sent an empty
string).
- `HankenGrotesk-Bold` title, `Inter-Regular` subtitle/countdown.

### AgentSelectView
- Replaces the carousel with a category-tab + scrollable list.
- Multi-select; honors `OnboardingViewModel.maxSelectedAgents = 3` cap
(enforced in-view).
- Surfaces `agentViewModel.catalogError` as a "Couldn't load agents /
Retry" UI when the catalog fetch fails — no infinite spinner on network
blips.
- "Not right now" secondary action sets `selectedAgentIds = []` and
advances to notifications.

### SetupLoadingView
- Consumes `AgentViewModel.installAgent`'s `Bool` return; failed
installs are accumulated into `installFailures` and surfaced via
`errorContent` with a Retry. Removes the silent-failure path where users
were sent to the chat with broken agents.
- Cancels the install `Task` on disappear to prevent zombie polls.

### OnboardingFlowView
- Refactored to the gradient-background + arrow-back-button design.
- Routes the redesigned post-auth views with their updated init
signatures (`EmailOTPLoginView` now takes `viewModel:` alongside
`onAuthenticated:`).

## Test plan

- [ ] Onboarding end-to-end: hero → name → role → useCase → register →
OTP → agentSelect → notifications → setupLoading
- [ ] OTP autofill from SMS / Mail when verification code arrives
- [ ] Resend OTP uses the previously-entered email (not blank)
- [ ] AgentSelect catalog error path: kill network mid-load → "Couldn't
load agents / Retry" appears; retry succeeds when network returns
- [ ] AgentSelect multi-select: cap at 3
- [ ] SetupLoading install failure path: simulate a failed install →
"Couldn't install: <name>" with Retry button; Retry re-runs only failed
installs

## Notes

- Size: **873 / 2000 lines** — comfortable budget.
- Depends on #1458 (merged).
- Closes the onboarding redesign initiative — no further view PRs
anticipated.
```

**PR #1467:** feat(ios): Post-auth onboarding view redesigns (PR-B of 2)

**PR Body:**
## Summary

**PR-B of 2** in the onboarding redesign split. Companion to #1458 (PR-A, **merged**). Ships the Figma redesigns of the four post-auth views.

After this PR lands, the visual onboarding refresh is feature-complete: hero → name → role → useCase → register → OTP → agentSelect → notifications → setupLoading all use the new design.

### EmailOTPLoginView
- 6-box OTP grid with invisible `TextField` driving iOS one-time-code autofill from SMS / Mail.
- Resend button reads the email back from `authViewModel.emailOTPState` (fix for the bug PR-A's review caught — previously sent an empty string).
- `HankenGrotesk-Bold` title, `Inter-Regular` subtitle/countdown.

### AgentSelectView
- Replaces the carousel with a category-tab + scrollable list.
- Multi-select; honors `OnboardingViewModel.maxSelectedAgents = 3` cap (enforced in-view).
- Surfaces `agentViewModel.catalogError` as a "Couldn't load agents / Retry" UI when the catalog fetch fails — no infinite spinner on network blips.
- "Not right now" secondary action sets `selectedAgentIds = []` and advances to notifications.

### SetupLoadingView
- Consumes `AgentViewModel.installAgent`'s `Bool` return; failed installs are accumulated into `installFailures` and surfaced via `errorContent` with a Retry. Removes the silent-failure path where users were sent to the chat with broken agents.
- Cancels the install `Task` on disappear to prevent zombie polls.

### OnboardingFlowView
- Refactored to the gradient-background + arrow-back-button design.
- Routes the redesigned post-auth views with their updated init signatures (`EmailOTPLoginView` now takes `viewModel:` alongside `onAuthenticated:`).

## Test plan

- [ ] Onboarding end-to-end: hero → name → role → useCase → register → OTP → agentSelect → notifications → setupLoading
- [ ] OTP autofill from SMS / Mail when verification code arrives
- [ ] Resend OTP uses the previously-entered email (not blank)
- [ ] AgentSelect catalog error path: kill network mid-load → "Couldn't load agents / Retry" appears; retry succeeds when network returns
- [ ] AgentSelect multi-select: cap at 3
- [ ] SetupLoading install failure path: simulate a failed install → "Couldn't install: <name>" with Retry button; Retry re-runs only failed installs

## Notes

- Size: **873 / 2000 lines** — comfortable budget.
- Depends on #1458 (merged).
- Closes the onboarding redesign initiative — no further view PRs anticipated.

**Stats:** +825 -404 (1229 changes)

---

## e4addf6f — 2026-04-29T10:16:38Z
**Author:** nolan-srp

**Message:**
```
feat(openclaw): support imported agent installs (#1470)

## Summary
- add import agent support to OpenClaw install and uninstall request
handling
- persist imported agents as custom metadata and preserve their source
in backend responses
- extend web API helpers and unit tests for import async operations and
validation

## Context
- enables import-based agent installs to use raw remote archive URLs end
to end
```

**PR #1470:** feat(openclaw): support imported agent installs

**PR Body:**
## Summary
- add import agent support to OpenClaw install and uninstall request handling
- persist imported agents as custom metadata and preserve their source in backend responses
- extend web API helpers and unit tests for import async operations and validation

## Context
- enables import-based agent installs to use raw remote archive URLs end to end


**Stats:** +450 -34 (484 changes)

---

## 56e07b40 — 2026-04-29T10:14:48Z
**Author:** tim-srp

**Message:**
```
chore: remove unused R2 private bucket config and code (#1472)

## Summary
- Remove unused `enterprise-user-data` private bucket config — no code
path ever passes `is_private=True`
- Remove `R2_PRIVATE_BUCKET_NAME`, `R2_PRIVATE_ACCESS_KEY_ID`,
`R2_PRIVATE_ACCESS_KEY_SECRET` from settings, env, and CI
- Simplify `R2StorageClient` from dual-client (public + private) to
single client
- Remove `is_private` / `supportsPrivate` plumbing from frontend
presigned URL factory

## Files changed (10)
- `.env.example` — remove 3 R2_PRIVATE entries
- `.github/workflows/deploy.yml` — remove R2_PRIVATE vars/secrets (5
references)
- `services/claw-interface/app/settings.py` — remove 3 fields
- `services/claw-interface/app/services/r2_storage.py` — simplify to
single s3 client
- `services/claw-interface/tests/unit/test_r2_storage.py` — remove
private tests
- `web/src/lib/r2/client.ts` — remove private config and branch
- `web/src/app/[locale]/_presignedFactory.ts` — remove
supportsPrivate/isPrivate
- `web/src/app/[locale]/image/presigned/route.ts` — remove isPrivate
param
- `web/src/app/[locale]/video/presigned/route.ts` — remove
supportsPrivate
- `web/tests/unit/app/image-video-presigned.unit.spec.ts` — remove
private test

## Test plan
- [ ] CI passes (backend + frontend)
- [ ] Existing image/video upload still works (no functional change —
private path was never used)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

**PR #1472:** chore: remove unused R2 private bucket config and code

**PR Body:**
## Summary
- Remove unused `enterprise-user-data` private bucket config — no code path ever passes `is_private=True`
- Remove `R2_PRIVATE_BUCKET_NAME`, `R2_PRIVATE_ACCESS_KEY_ID`, `R2_PRIVATE_ACCESS_KEY_SECRET` from settings, env, and CI
- Simplify `R2StorageClient` from dual-client (public + private) to single client
- Remove `is_private` / `supportsPrivate` plumbing from frontend presigned URL factory

## Files changed (10)
- `.env.example` — remove 3 R2_PRIVATE entries
- `.github/workflows/deploy.yml` — remove R2_PRIVATE vars/secrets (5 references)
- `services/claw-interface/app/settings.py` — remove 3 fields
- `services/claw-interface/app/services/r2_storage.py` — simplify to single s3 client
- `services/claw-interface/tests/unit/test_r2_storage.py` — remove private tests
- `web/src/lib/r2/client.ts` — remove private config and branch
- `web/src/app/[locale]/_presignedFactory.ts` — remove supportsPrivate/isPrivate
- `web/src/app/[locale]/image/presigned/route.ts` — remove isPrivate param
- `web/src/app/[locale]/video/presigned/route.ts` — remove supportsPrivate
- `web/tests/unit/app/image-video-presigned.unit.spec.ts` — remove private test

## Test plan
- [ ] CI passes (backend + frontend)
- [ ] Existing image/video upload still works (no functional change — private path was never used)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

**Stats:** +45 -149 (194 changes)

---

## 7d0dd6b2 — 2026-04-29T09:59:06Z
**Author:** tim-srp

**Message:**
```
fix: defense-in-depth auth & clickjacking headers (exclude mini-chat embed) (#1436)

## Summary
- **admin_cron**: add `require_internal_service_key` dependency to all 6
cron trigger/query endpoints (defense-in-depth behind CF Zero Trust)
- **orders/admin/grant**: add `require_admin_user` dependency
- **next.config**: add `X-Frame-Options: DENY` +
`Content-Security-Policy: frame-ancestors 'none'` (clickjacking
protection)
- **billing_gateway**: retry `topup_wallet` once on 5xx with 1s backoff
(Lago transient error resilience)

## Context
Production incident 2026-04-27: Lago returned a transient 500 on `POST
/api/v1/wallet_transactions` during a user's subscription grant. The
user saw "Failed to confirm order" and had to re-purchase on a lower
plan. The topup retry prevents this class of failure from reaching the
user.

Security hardening prompted by external vulnerability reports — CF Zero
Trust already protects `/admin/*`, but application-layer auth adds
defense-in-depth. `X-Frame-Options` addresses a reported clickjacking
concern.

## Test plan
- [ ] `pytest tests/unit/test_stripe_billing_gateway.py` — 15 tests pass
(2 new: 500 retry success + 500 retry then raise)
- [ ] `pyright` clean on all changed files
- [ ] Verify cron scheduler passes `X-Internal-Service-Key` header
(otherwise cron triggers will 401)
- [ ] Verify `/admin/grant` still works from admin UI (JWT auth)
- [ ] Verify `zooclaw.ai` pages return `X-Frame-Options: DENY` header
after deploy

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

**PR #1436:** fix: defense-in-depth auth & clickjacking headers (exclude mini-chat embed)

**PR Body:**
## Summary
- **admin_cron**: add `require_internal_service_key` dependency to all 6 cron trigger/query endpoints (defense-in-depth behind CF Zero Trust)
- **orders/admin/grant**: add `require_admin_user` dependency
- **next.config**: add `X-Frame-Options: DENY` + `Content-Security-Policy: frame-ancestors 'none'` (clickjacking protection)
- **billing_gateway**: retry `topup_wallet` once on 5xx with 1s backoff (Lago transient error resilience)

## Context
Production incident 2026-04-27: Lago returned a transient 500 on `POST /api/v1/wallet_transactions` during a user's subscription grant. The user saw "Failed to confirm order" and had to re-purchase on a lower plan. The topup retry prevents this class of failure from reaching the user.

Security hardening prompted by external vulnerability reports — CF Zero Trust already protects `/admin/*`, but application-layer auth adds defense-in-depth. `X-Frame-Options` addresses a reported clickjacking concern.

## Test plan
- [ ] `pytest tests/unit/test_stripe_billing_gateway.py` — 15 tests pass (2 new: 500 retry success + 500 retry then raise)
- [ ] `pyright` clean on all changed files
- [ ] Verify cron scheduler passes `X-Internal-Service-Key` header (otherwise cron triggers will 401)
- [ ] Verify `/admin/grant` still works from admin UI (JWT auth)
- [ ] Verify `zooclaw.ai` pages return `X-Frame-Options: DENY` header after deploy

🤖 Generated with [Claude Code](https://claude.com/claude-code)

**Stats:** +14 -0 (14 changes)

---

## d1babf7a — 2026-04-29T09:35:59Z
**Author:** tim-srp

**Message:**
```
feat(claw-interface): add R2 presigned URL endpoint for frontend (#1465)

## Summary
- Add `GET /api/storage/r2/presign` endpoint for frontend to obtain
presigned upload URLs
- Uses existing `R2StorageClient.generate_presigned_put_url` — no extra
network hop to ecap-proxy-service
- JWT auth via `Depends(get_current_user)` at router level
- Companion to SerendipityOneInc/ecap-proxy-service#39 (same feature on
proxy side)

## API

```
GET /api/storage/r2/presign?filename=photo.png&file_type=image&content_type=image/png
Authorization: Bearer <jwt>

Response:
{
  "presigned_url": "https://r2.../presigned?sig=...",
  "public_url": "https://cdn.example.com/image/20260429/abc.png"
}
```

## Files Changed
| File | Change |
|------|--------|
| `services/claw-interface/app/routes/storage.py` | New route with
`PresignedUrlResponse` schema |
| `services/claw-interface/app/create_app.py` | Register
`storage.router` |
| `services/claw-interface/tests/unit/test_storage.py` | 9 unit tests |

## Test plan
- [x] All pre-commit hooks pass (ruff, pyright, import-linter)
- [ ] CI unit tests pass
- [ ] Manual test via telepresence after deploy

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
Co-authored-by: claude[bot] <41898282+claude[bot]@users.noreply.github.com>
Co-authored-by: tim-srp <undefined@users.noreply.github.com>
```

**PR #1465:** feat(claw-interface): add R2 presigned URL endpoint for frontend

**PR Body:**
## Summary
- Add `GET /api/storage/r2/presign` endpoint for frontend to obtain presigned upload URLs
- Uses existing `R2StorageClient.generate_presigned_put_url` — no extra network hop to ecap-proxy-service
- JWT auth via `Depends(get_current_user)` at router level
- Companion to SerendipityOneInc/ecap-proxy-service#39 (same feature on proxy side)

## API

```
GET /api/storage/r2/presign?filename=photo.png&file_type=image&content_type=image/png
Authorization: Bearer <jwt>

Response:
{
  "presigned_url": "https://r2.../presigned?sig=...",
  "public_url": "https://cdn.example.com/image/20260429/abc.png"
}
```

## Files Changed
| File | Change |
|------|--------|
| `services/claw-interface/app/routes/storage.py` | New route with `PresignedUrlResponse` schema |
| `services/claw-interface/app/create_app.py` | Register `storage.router` |
| `services/claw-interface/tests/unit/test_storage.py` | 9 unit tests |

## Test plan
- [x] All pre-commit hooks pass (ruff, pyright, import-linter)
- [ ] CI unit tests pass
- [ ] Manual test via telepresence after deploy

🤖 Generated with [Claude Code](https://claude.com/claude-code)

**Stats:** +134 -0 (134 changes)

---

## a74fd4a2 — 2026-04-29T08:49:59Z
**Author:** tim-srp

**Message:**
```
chore: remove unused LITELLM_AUTH_TOKEN from .env.example (#1466)

## Summary
- Remove `LITELLM_AUTH_TOKEN` from `.env.example` — it is not consumed
by any code (`settings.py` has no such field, no business logic
references it)
- The corresponding LiteLLM key (`sk-MRwyZJ8ZT7pAIOoESdRwsg`) has been
confirmed invalid (401 `token_not_found_in_db`)
- K8s deployments (`claw-interface`, `ecommerce-studio-service`) still
inject this env var but it is dead config — will be cleaned up
separately in infra

## Test plan
- [ ] CI passes (no code change, only `.env.example`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

**PR #1466:** chore: remove unused LITELLM_AUTH_TOKEN from .env.example

**PR Body:**
## Summary
- Remove `LITELLM_AUTH_TOKEN` from `.env.example` — it is not consumed by any code (`settings.py` has no such field, no business logic references it)
- The corresponding LiteLLM key (`sk-MRwyZJ8ZT7pAIOoESdRwsg`) has been confirmed invalid (401 `token_not_found_in_db`)
- K8s deployments (`claw-interface`, `ecommerce-studio-service`) still inject this env var but it is dead config — will be cleaned up separately in infra

## Test plan
- [ ] CI passes (no code change, only `.env.example`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

**Stats:** +0 -1 (1 changes)

---

## 4de70593 — 2026-04-29T08:41:27Z
**Author:** nolan-srp

**Message:**
```
fix(auth): require srp.one user for internal service key (#1459)

## Summary
- require internal service key requests to include a valid Bearer user
token
- allow internal mutation endpoints only when the authenticated user
email ends with `@srp.one`
- reject the legacy flow that passed only the service key in the
`Authorization` header

## Context
- internal mutation access should be bound to an authenticated internal
account, not only a shared service key
```

**PR #1459:** fix(auth): require srp.one user for internal service key

**PR Body:**
## Summary
- require internal service key requests to include a valid Bearer user token
- allow internal mutation endpoints only when the authenticated user email ends with `@srp.one`
- reject the legacy flow that passed only the service key in the `Authorization` header

## Context
- internal mutation access should be bound to an authenticated internal account, not only a shared service key

**Stats:** +89 -1 (90 changes)

---

## 8001a63d — 2026-04-29T08:33:54Z
**Author:** bill-srp

**Message:**
```
feat(ios): Pre-auth onboarding redesign with role + use-case screens (#1458)

## Summary

**PR-A of 2** in the onboarding redesign split. Builds on the
infrastructure landed in #1452 and ships the redesigned **pre-auth**
flow: hero → name → role → use case → register.

This PR was extracted from #1450 to fit the 2000-line PR size budget.
PR-B (forthcoming) will ship the post-auth view redesigns:
EmailOTPLoginView, AgentSelectView, SetupLoadingView, and the full
OnboardingFlowView refactor.

### Pre-auth view redesigns

- **HeroView** — video background loop, Montserrat + Instrument Serif
tagline.
- **NameInputView** — editorial italic-serif underline input, panda
avatar, Continue pinned bottom.
- **RoleSelectionView** *(new)* — six-card grid; default-first with VM
rehydration on back-nav.
- **UseCaseSelectionView** *(new)* — four-card grid; same rehydration
pattern.
- **RegisterView** — simplified email-only entry with Google / Apple
SSO, inline terms/privacy.

### VM scaffolding

- New `roleSelection` / `useCaseSelection` enum cases.
- `selectedRole` / `selectedUseCase` storage (drives the rehydration on
back-nav).
- `selectedAgentIds: Set<String>` with `maxSelectedAgents = 3`.
- `goBack` table aligned with `canGoBack` (no dead branches).

### NotificationsView fix

PR #1452 deleted three onboarding notification imagesets but main's
NotificationsView still references them. This PR ships the redesigned
view (logo_black + animated cards) to restore main's visual integrity
rather than leaving it broken until PR-B.

### Compatibility shims

`AgentSelectView` and `SetupLoadingView` keep their main-version designs
but are minimally updated to consume `selectedAgentIds: Set<String>`
(replacing the dropped `selectedAgentId: String?`). Their full redesigns
ship in PR-B.

## Tests

- 28/28 OnboardingViewModelTests pass.
- New coverage: rehydration, set mutations, `maxSelectedAgents`, new
screen navigation.

## Test plan

- [ ] Onboarding pre-auth flow end-to-end: hero → name → role → use case
→ register
- [ ] Back-navigation from role/use-case restores prior selection
(rehydration)
- [ ] Notifications screen renders correctly (logo + animated cards, no
missing images)
- [ ] Agent select still works end-to-end (compat shim consuming
`selectedAgentIds.first`)
- [ ] Existing chat / agents / settings flows unchanged

## Notes

- Size: **1133 / 2000 lines** — comfortable budget, no `size-override`
needed.
- Mid-flow visual mismatch is expected on TestFlight builds between this
PR and PR-B (new pre-auth + old EmailOTP / AgentSelect / SetupLoading).
- Supersedes the corresponding portions of #1450; #1450 will be closed
or rebased once both halves land.
```

**PR #1458:** feat(ios): Pre-auth onboarding redesign with role + use-case screens

**PR Body:**
## Summary

**PR-A of 2** in the onboarding redesign split. Builds on the infrastructure landed in #1452 and ships the redesigned **pre-auth** flow: hero → name → role → use case → register.

This PR was extracted from #1450 to fit the 2000-line PR size budget. PR-B (forthcoming) will ship the post-auth view redesigns: EmailOTPLoginView, AgentSelectView, SetupLoadingView, and the full OnboardingFlowView refactor.

### Pre-auth view redesigns

- **HeroView** — video background loop, Montserrat + Instrument Serif tagline.
- **NameInputView** — editorial italic-serif underline input, panda avatar, Continue pinned bottom.
- **RoleSelectionView** *(new)* — six-card grid; default-first with VM rehydration on back-nav.
- **UseCaseSelectionView** *(new)* — four-card grid; same rehydration pattern.
- **RegisterView** — simplified email-only entry with Google / Apple SSO, inline terms/privacy.

### VM scaffolding

- New `roleSelection` / `useCaseSelection` enum cases.
- `selectedRole` / `selectedUseCase` storage (drives the rehydration on back-nav).
- `selectedAgentIds: Set<String>` with `maxSelectedAgents = 3`.
- `goBack` table aligned with `canGoBack` (no dead branches).

### NotificationsView fix

PR #1452 deleted three onboarding notification imagesets but main's NotificationsView still references them. This PR ships the redesigned view (logo_black + animated cards) to restore main's visual integrity rather than leaving it broken until PR-B.

### Compatibility shims

`AgentSelectView` and `SetupLoadingView` keep their main-version designs but are minimally updated to consume `selectedAgentIds: Set<String>` (replacing the dropped `selectedAgentId: String?`). Their full redesigns ship in PR-B.

## Tests

- 28/28 OnboardingViewModelTests pass.
- New coverage: rehydration, set mutations, `maxSelectedAgents`, new screen navigation.

## Test plan

- [ ] Onboarding pre-auth flow end-to-end: hero → name → role → use case → register
- [ ] Back-navigation from role/use-case restores prior selection (rehydration)
- [ ] Notifications screen renders correctly (logo + animated cards, no missing images)
- [ ] Agent select still works end-to-end (compat shim consuming `selectedAgentIds.first`)
- [ ] Existing chat / agents / settings flows unchanged

## Notes

- Size: **1133 / 2000 lines** — comfortable budget, no `size-override` needed.
- Mid-flow visual mismatch is expected on TestFlight builds between this PR and PR-B (new pre-auth + old EmailOTP / AgentSelect / SetupLoading).
- Supersedes the corresponding portions of #1450; #1450 will be closed or rebased once both halves land.

**Stats:** +979 -359 (1338 changes)

---

## 87e629af — 2026-04-29T07:10:59Z
**Author:** Chris@ZooClaw

**Message:**
```
fix(web): AgentDetailClient Escape key listener race (#1275) (#1461)

## Summary

`AgentDetailClient` 的 Escape 处理是 `useCallback(handler, [showConfirm,
showSuccess, ...])` + `useEffect(addEventListener, [handleKeyDown])` ——
每次 modal state 翻转都会回收旧 listener、附新 listener。问题是 `confirm → await
hireAgent → setShowSuccess(true)` 这条 async 路径里,success modal 进
DOM(commit)和 listener 重新挂载是两步。中间窗口里 Escape 落到旧 closure(`showSuccess:
false`),什么都不关。

改成 ref pattern:listener 挂载一次(empty deps),每次 render 把最新 state 写到
ref;handler 调用时读 ref。优先级 / 触发链都不变。

## Repro / 验证

- 之前:`Escape key closes modals (priority order) > success open → Escape
closes success` 在 16 轮 full-suite 跑里偶发 fail ~12%
- 修复后本地 16 轮单文件全过(`pnpm test:unit AgentDetailClient.unit.spec.tsx`)

## 关闭

Closes #1275

## Test plan

- [x] `pnpm test:unit
tests/unit/app/agents-manager/AgentDetailClient.unit.spec.tsx` × 16
轮全过(31 tests)
- [x] `npx tsc --noEmit` 全仓 clean
- [x] `npx eslint
src/app/[locale]/agents-manager/[id]/AgentDetailClient.tsx` clean
- [x] `npx prettier --check` clean
- [ ] CI: code-quality / lint-and-test
```

**PR #1275:** 

**Stats:** +54 -18 (72 changes)

---

## 8298f1fe — 2026-04-29T06:16:16Z
**Author:** Chris@ZooClaw

**Message:**
```
chore(web): migrate 11 files from inline style to Tailwind (#754) (#1457)

## Summary

- 迁 11 个 grandfathered 文件 / 21 处 inline `style` → Tailwind utility
- `eslint.config.mjs` `react/forbid-dom-props` ignores: **45 →
34**(shrink-only sentinel 通过)
- 推进 #754 长 tracker;选品依据:**当前 ignores 中非 branded、纯静态可 TW 化的候选**

## Files

**Batch 1 — 5 files / 12 处**
- `PublicFooter.tsx` (5): h-8/w-auto, mt-2, h-5/w-5 ×2, justify-start
- `PublicHeader.tsx` (2): inline-flex/items-center/gap-1.5,
block/text-center
- `PlanCard.tsx` (3): w-[0.6em]/h-[1.15em]/align-bottom, leading-none
×2, layered absolute layout
- `InputArea.tsx` (1): hidden
- `FeedbackDialog.tsx` (1): max-h-[min(500px,70vh)]

**Batch 2 — 6 files / 9 处**
- `ThinkingIndicator.tsx` (3): [animation-delay:0s/0.2s/0.4s]
- `ArchivedSessionPanel.tsx` (1): min-h-[500px]
- `AssetsPanel.tsx` (1): aspect-[3/4]
- `UserMenu.tsx` (1): border-border(去掉冗余 var 引用)
- `DowngradeConfirmModal.tsx` (1):
bg-[var(--ecap-billing-badge-current)]
- `MarkdownContent.tsx` (1): [overflow-wrap:anywhere],并删去冗余的
wordBreak(已被 className `break-words` 覆盖)

## Notes

- Issue 原列的 top-5(LoginForm / verify / GeneralTab / PaywallContent /
ChannelStep)早已被前序 opportunistic PR 清理完毕,已不在 ignores 列表里。
- 当前 ignores 中量最大的几个文件(`CompanionSelectStep` 11 处、`InviteCodeStep` 9
处、`OnboardingLayout` 7 处等)都是 **branded 模块** 内的 `rgba(...)` / `#hex` 颜色,被
#796 theme refactor 阻塞,本 PR 跳过。
- **Audit gotcha**:ESLint `react/forbid-dom-props` 同时拦截 `style={var}`(单
brace)和 `style={{...}}`(双 brace)。第一轮 grep `'style={{'` 漏掉了
`MMAttachments.tsx` 里 3 处 `style={boxStyle}` 的 LEGIT 数据驱动样式(image 尺寸
from runtime metadata)。MMAttachments 保留在 ignores 内,留待后续 PR 加
inline-disable + 原因注释。
- 所有迁移都是 1:1 映射(rem 基于 root 16px);`break-words` Tailwind 即 `word-break:
break-word`,所以原 inline 的 `wordBreak: 'break-word'` 是冗余,删去。

## Test plan

- [x] `npx tsc --noEmit` clean
- [x] `npx eslint <files>` clean
- [x] `bash scripts/check-ignores-shrink-only.sh` pass(45 → 34)
- [x] `npx vitest run` 12 spec / 279 tests pass
- [ ] Visual sanity:landing footer/header,billing PlanCard 价格滚动 +
DowngradeConfirmModal,FeedbackDialog 弹窗,UserMenu
虚线分隔,ArchivedSessionPanel 列表高度,AssetsPanel 卡片纵横比,MarkdownContent 长 URL
换行,ThinkingIndicator 三点交错动画

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR #754:** 

**Stats:** +21 -66 (87 changes)

---

## 0fec950d — 2026-04-29T04:47:35Z
**Author:** Chris@ZooClaw

**Message:**
```
refactor(web): RQ v2 PR-a — useUserAgents 切 useQuery (facade 不变) (#1349)

## 背景

按
[`docs/superpowers/specs/2026-04-25-react-query-migration-v2.md`](../blob/main/docs/superpowers/specs/2026-04-25-react-query-migration-v2.md)
落地 **PR-a**(spec 拆分中的第一个,无依赖,后续 PR-b/c/d/e/f 均建在其上)。

v2 spec 要清扫的是 v1 没覆盖的"包了 `lib/api/*` wrapper 但仍 `useEffect + setState`"的
~34 个文件——它们已经避开了 v1 的 raw `fetch()` lint guard,但 RQ 的 dedup / cache /
focus refetch / 自动重试一项没拿到。本 PR 是这条尾巴的第一刀。

## 改动范围

| 文件 | 操作 | 说明 |
|---|---|---|
| `src/hooks/queries/openclaw/keys.ts` | 新建 | openclaw domain query-key
工厂,uid 进 key(D4: 跨账号缓存隔离) |
| `src/hooks/useUserAgents.ts` | 重写 hook 内部 | `useState + 3×useEffect` →
`useQuery`;模块级 `refreshUserAgentsCache` 整体保留 |
| `tests/unit/hooks/useUserAgents.unit.spec.ts` | 加 createQueryWrapper +
getUserInfo mock | 既有 19 个 case 全过 |

**Public API 完全不变**:`{ agents, isLoading, refreshAgents }` + 模块函数
`refreshUserAgentsCache({ force? })`。9 个 `useUserAgents` callsite + 5 个
`refreshUserAgentsCache` callsite 不动一行。

## 关键决策

### D2 facade 保留 — 内部切到 useQuery
照 v1 PR-7 (`useLiteLLMApi`) 的做法,从消费方看 hook 形状不变,只是内部 fetch 路径换成 RQ。这样 PR
范围 = 2 个文件改动,不是 14 个 callsite 联动。

### 模块级 `refreshUserAgentsCache` 暂不迁
该函数的 `_inflight` / `_lastResult` / `THROTTLE_MS` 对 5 个 imperative
caller(post-mutation 强刷)是契约,把它切成 `queryClient.fetchQuery` 需要先建
`getQueryClient()` 单例,工作量超出本 PR。短期"双轨"通过 `setQueryData(localStorage 值)`
listener 保持一致,后续 PR 再清理。

### `isLoading = query.isPending`(不用 `isFetching`)
旧 hook 的 `isLoading` 只在"无缓存且首次拉"时为 true,跟
`isPending`(还没拿到任何数据)语义匹配。`isFetching` 会在 background refetch / focus
refetch 时也 true,会让 SideNav 等 caller 闪 spinner。

### `initialData + initialDataUpdatedAt: 0`
从 localStorage 缓存读 `initialData` 保留"刷新页面有缓存先显示"的 UX;`updatedAt: 0` 让 RQ
仍把数据视为 stale,mount 时还是会触发网络刷新——两者结合 = 旧版"先缓存,再后台刷新"行为不变。

### Listener 用 `setQueryData` 而非 `invalidateQueries`
`refreshUserAgentsCache` 派发 `'ecap:agents:updated'` 之前已经写好了
localStorage,网络已经 settled。这种情况下 invalidate→refetch 是浪费,直接
`setQueryData(localStorage 值)` 把 RQ cache 跟模块缓存对齐最便宜。跨 tab 的 `storage`
事件同源同处理。

## 验证

- `pnpm tsc --noEmit`:无错
- `pnpm lint`:无报
- `pnpm test:unit tests/unit/hooks/useUserAgents.unit.spec.ts`:19/19
passed
- `pnpm test:unit`(全仓):4183/4183 passed,0 回归

## 不在范围内

- 模块级 `refreshUserAgentsCache` 切 RQ(后续 cleanup PR)
- PR-b: `useClawSettings` / `useBillingCredits` /
`useOfficialAgentCatalog` / `useCustomAgentPublishes`
- PR-c: `claw-settings/` 10 个组件
- PR-d: `chat/` 资源面板 / onboarding / skills 浏览
- PR-e: billing 表面(高风险,串行)
- PR-f: 长尾散点 + 复跑调研命令

## Test plan

- [ ] CI `code-quality / lint-and-test` 绿
- [ ] 手测 `/chat`:agent 列表加载,切 agent 正常
- [ ] SideNav agent 列表显示
- [ ] Skill 详情页 → "添加到我的 agents" → 列表自动刷新(验证 `'ecap:agents:updated'`
事件路径)
- [ ] 退出登录 → 重登(验证 uid 切换 key 重拉)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR #1349:** refactor(web): RQ v2 PR-a — useUserAgents 切 useQuery (facade 不变)

**PR Body:**
## 背景

按 [`docs/superpowers/specs/2026-04-25-react-query-migration-v2.md`](../blob/main/docs/superpowers/specs/2026-04-25-react-query-migration-v2.md) 落地 **PR-a**(spec 拆分中的第一个,无依赖,后续 PR-b/c/d/e/f 均建在其上)。

v2 spec 要清扫的是 v1 没覆盖的"包了 `lib/api/*` wrapper 但仍 `useEffect + setState`"的 ~34 个文件——它们已经避开了 v1 的 raw `fetch()` lint guard,但 RQ 的 dedup / cache / focus refetch / 自动重试一项没拿到。本 PR 是这条尾巴的第一刀。

## 改动范围

| 文件 | 操作 | 说明 |
|---|---|---|
| `src/hooks/queries/openclaw/keys.ts` | 新建 | openclaw domain query-key 工厂,uid 进 key(D4: 跨账号缓存隔离) |
| `src/hooks/useUserAgents.ts` | 重写 hook 内部 | `useState + 3×useEffect` → `useQuery`;模块级 `refreshUserAgentsCache` 整体保留 |
| `tests/unit/hooks/useUserAgents.unit.spec.ts` | 加 createQueryWrapper + getUserInfo mock | 既有 19 个 case 全过 |

**Public API 完全不变**:`{ agents, isLoading, refreshAgents }` + 模块函数 `refreshUserAgentsCache({ force? })`。9 个 `useUserAgents` callsite + 5 个 `refreshUserAgentsCache` callsite 不动一行。

## 关键决策

### D2 facade 保留 — 内部切到 useQuery
照 v1 PR-7 (`useLiteLLMApi`) 的做法,从消费方看 hook 形状不变,只是内部 fetch 路径换成 RQ。这样 PR 范围 = 2 个文件改动,不是 14 个 callsite 联动。

### 模块级 `refreshUserAgentsCache` 暂不迁
该函数的 `_inflight` / `_lastResult` / `THROTTLE_MS` 对 5 个 imperative caller(post-mutation 强刷)是契约,把它切成 `queryClient.fetchQuery` 需要先建 `getQueryClient()` 单例,工作量超出本 PR。短期"双轨"通过 `setQueryData(localStorage 值)` listener 保持一致,后续 PR 再清理。

### `isLoading = query.isPending`(不用 `isFetching`)
旧 hook 的 `isLoading` 只在"无缓存且首次拉"时为 true,跟 `isPending`(还没拿到任何数据)语义匹配。`isFetching` 会在 background refetch / focus refetch 时也 true,会让 SideNav 等 caller 闪 spinner。

### `initialData + initialDataUpdatedAt: 0`
从 localStorage 缓存读 `initialData` 保留"刷新页面有缓存先显示"的 UX;`updatedAt: 0` 让 RQ 仍把数据视为 stale,mount 时还是会触发网络刷新——两者结合 = 旧版"先缓存,再后台刷新"行为不变。

### Listener 用 `setQueryData` 而非 `invalidateQueries`
`refreshUserAgentsCache` 派发 `'ecap:agents:updated'` 之前已经写好了 localStorage,网络已经 settled。这种情况下 invalidate→refetch 是浪费,直接 `setQueryData(localStorage 值)` 把 RQ cache 跟模块缓存对齐最便宜。跨 tab 的 `storage` 事件同源同处理。

## 验证

- `pnpm tsc --noEmit`:无错
- `pnpm lint`:无报
- `pnpm test:unit tests/unit/hooks/useUserAgents.unit.spec.ts`:19/19 passed
- `pnpm test:unit`(全仓):4183/4183 passed,0 回归

## 不在范围内

- 模块级 `refreshUserAgentsCache` 切 RQ(后续 cleanup PR)
- PR-b: `useClawSettings` / `useBillingCredits` / `useOfficialAgentCatalog` / `useCustomAgentPublishes`
- PR-c: `claw-settings/` 10 个组件
- PR-d: `chat/` 资源面板 / onboarding / skills 浏览
- PR-e: billing 表面(高风险,串行)
- PR-f: 长尾散点 + 复跑调研命令

## Test plan

- [ ] CI `code-quality / lint-and-test` 绿
- [ ] 手测 `/chat`:agent 列表加载,切 agent 正常
- [ ] SideNav agent 列表显示
- [ ] Skill 详情页 → "添加到我的 agents" → 列表自动刷新(验证 `'ecap:agents:updated'` 事件路径)
- [ ] 退出登录 → 重登(验证 uid 切换 key 重拉)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

**Stats:** +507 -125 (632 changes)

---

## 9960bbb7 — 2026-04-29T04:42:28Z
**Author:** bill-srp

**Message:**
```
feat(ios): Onboarding infrastructure and asset cleanup (#1452)

## Summary

Foundation for the upcoming onboarding redesign — ships independently of
any view changes so the follow-up view PR can reuse it without refactor
churn. This is **PR 1 of 2**, split out so each PR fits the 2000-line
budget.

### Theme & fonts
- `AppTheme.Onboarding` palette of named tokens (text / border / badge /
avatar colors).
- `AppTheme.chatBackgroundView()` helper backed by the new
`onboarding_bg` imageset.
- Hanken Grotesk Bold + Medium TTFs registered via `Info.plist`
`UIAppFonts`.

### Services
- `AgentService.installAgent` + `agentOperation` — async install with
operation-id polling; replaces the synchronous hire path for installs
that may take >5s server-side.
- `AgentViewModel.installAgent` wraps the new API with a 60-poll cap
(5min budget) and Sentry timeout capture.
- `AgentViewModel.catalogError` surfaces fetch failures (staging for the
upcoming retry UI).

### VideoLoopView lifecycle
- `dismantleUIView` pauses the player, drains the queue, releases the
looper when SwiftUI removes the view.
- `accessibilityElementsHidden` on the wrapped UIView so VoiceOver
doesn't announce the decorative loop.

### Asset cleanup
- Remove `loading.gif` (4.4 MB unused since #208).
- Remove three unused `onboarding_*_notification` imagesets superseded
by the new design.
- Add `welcome.m4v` (3.5 MB, ffmpeg re-encoded from the larger mp4) —
consumed by `HeroView` in PR 2.
- Add new imagesets that role / use-case / register screens consume in
PR 2: `onboarding_bg`, six `job_*`, four `use_*`. **Orphaned in this
PR**; consumers land in PR 2.

### Other
- `CLAUDE.md` updated with notes on auto-bundling, font registration,
and asset-grep patterns.
- `AccountService.swift` minor 1-line phone OTP cleanup.

## Why no view changes here?

The Figma onboarding redesign would push the diff to ~2300 lines, over
the 2000 budget. Splitting along the infrastructure / view boundary lets
each PR review independently:
- Reviewers of this PR focus on services, palette, and asset hygiene
with no UI surface area.
- Reviewers of PR 2 focus on the Figma flow with all primitives already
in place.

## Test plan

- [ ] App builds and launches cleanly on iPhone 17 Pro simulator
- [ ] Existing onboarding still works (no behavior change for users —
old views consume nothing from the new infra yet)
- [ ] `swiftlint` zero violations
- [ ] No TestFlight regressions vs the previous build

## Related

- Follow-up PR (view redesigns): supersedes #1450
- Per CLAUDE.md size budget: 413 / 2000 lines (well under)
```

**PR #1452:** feat(ios): Onboarding infrastructure and asset cleanup

**PR Body:**
## Summary

Foundation for the upcoming onboarding redesign — ships independently of any view changes so the follow-up view PR can reuse it without refactor churn. This is **PR 1 of 2**, split out so each PR fits the 2000-line budget.

### Theme & fonts
- `AppTheme.Onboarding` palette of named tokens (text / border / badge / avatar colors).
- `AppTheme.chatBackgroundView()` helper backed by the new `onboarding_bg` imageset.
- Hanken Grotesk Bold + Medium TTFs registered via `Info.plist` `UIAppFonts`.

### Services
- `AgentService.installAgent` + `agentOperation` — async install with operation-id polling; replaces the synchronous hire path for installs that may take >5s server-side.
- `AgentViewModel.installAgent` wraps the new API with a 60-poll cap (5min budget) and Sentry timeout capture.
- `AgentViewModel.catalogError` surfaces fetch failures (staging for the upcoming retry UI).

### VideoLoopView lifecycle
- `dismantleUIView` pauses the player, drains the queue, releases the looper when SwiftUI removes the view.
- `accessibilityElementsHidden` on the wrapped UIView so VoiceOver doesn't announce the decorative loop.

### Asset cleanup
- Remove `loading.gif` (4.4 MB unused since #208).
- Remove three unused `onboarding_*_notification` imagesets superseded by the new design.
- Add `welcome.m4v` (3.5 MB, ffmpeg re-encoded from the larger mp4) — consumed by `HeroView` in PR 2.
- Add new imagesets that role / use-case / register screens consume in PR 2: `onboarding_bg`, six `job_*`, four `use_*`. **Orphaned in this PR**; consumers land in PR 2.

### Other
- `CLAUDE.md` updated with notes on auto-bundling, font registration, and asset-grep patterns.
- `AccountService.swift` minor 1-line phone OTP cleanup.

## Why no view changes here?

The Figma onboarding redesign would push the diff to ~2300 lines, over the 2000 budget. Splitting along the infrastructure / view boundary lets each PR review independently:
- Reviewers of this PR focus on services, palette, and asset hygiene with no UI surface area.
- Reviewers of PR 2 focus on the Figma flow with all primitives already in place.

## Test plan

- [ ] App builds and launches cleanly on iPhone 17 Pro simulator
- [ ] Existing onboarding still works (no behavior change for users — old views consume nothing from the new infra yet)
- [ ] `swiftlint` zero violations
- [ ] No TestFlight regressions vs the previous build

## Related

- Follow-up PR (view redesigns): supersedes #1450
- Per CLAUDE.md size budget: 413 / 2000 lines (well under)

**Stats:** +988 -53 (1041 changes)

---

## 36c7470b — 2026-04-29T04:23:49Z
**Author:** Chris@ZooClaw

**Message:**
```
refactor(web): final cleanup — render-phase reset + drop redundant memos (#1454)

## Summary
\`feature/use-less-effect\` 系列收尾 PR。PR 1-3 之后真实的反模式总数比初步审计预估的小得多 — 计划里
PR 4(链式 setState)和 PR 5(边角)的多数候选深读后都是 J4 (justified effect):prop-driven
mount lifecycle / debounced corrective watchdog / unmount-only timer
cleanup / SSR 敏感的 localStorage hydration。

剩下两处确实值得改的:

**useDeepLinkHireFlow**: agentId 变 reset state 的 effect 改成 render-phase
setState (PR 3 同款 latch 模式),guard \`state.targetAgentId !== null\` 防循环。

**useFreeStatus**: 
- \`refresh\` useCallback inline 进唯一的 effect
- \`isFreeUser\` useMemo 删掉(返回 boolean,primitive 天然 referentially
stable,no identity worth memoizing)
- \`isFreeExpired\` / \`freeDaysLeft\` 的 useMemo 删掉 — 这两个**反而是
bug**:\`Date.now()\` 是隐式输入,useMemo 没法 track,导致 memo 在 \`[isFreeUser,
info]\` 上,countdown 直到下一次 auth/credits 事件触发前都冻住。inline 才正确。

## Why 系列只到 5 个 PR(原计划过 5)
原审计高估了反模式数量,深读后:
- PR 4 三个 B 类候选全是 prop/事件驱动,合不进 handler
- PR 5 六个候选只一个真有效;其他要么 SSR 风险(useState initializer + localStorage),要么
unmount-only cleanup 是 canonical 写法,要么是 navigate 自动化没事件 handler 可挪
- "scaling-down" 比硬上重要 — \`feedback_review_followup_verify_first\` 的精神

## Stats
2 files / +23 / -32 / 1 effect 删除 + 1 useCallback 删除 + 3 useMemo 删除 +
顺带修一个 stale-time bug

## Test plan
- [x] \`pnpm lint\` 绿
- [x] \`npx tsc --noEmit\` 绿
- [x] 相关单测全过(30/30: useDeepLinkHireFlow + useFreeStatus)
- [ ] CI 全绿
- [ ] staging:deep-link 流换 agentId 不卡;free 用户 countdown 显示

## Series 收尾
全 5 PR 系列 (#1396 / #1414 / #1421 / #1425 / 本):
- 真正消除的反模式 effect:11(ref-sync × 5,state-reset effect → key prop ×
2,latch effect × 2,disconnect ref reset 后续维持 effect,render-phase reset ×
1)
- 顺带:1 useCallback,3 useMemo,1 stale-time bug

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR #1454:** refactor(web): final cleanup — render-phase reset + drop redundant memos

**PR Body:**
## Summary
\`feature/use-less-effect\` 系列收尾 PR。PR 1-3 之后真实的反模式总数比初步审计预估的小得多 — 计划里 PR 4(链式 setState)和 PR 5(边角)的多数候选深读后都是 J4 (justified effect):prop-driven mount lifecycle / debounced corrective watchdog / unmount-only timer cleanup / SSR 敏感的 localStorage hydration。

剩下两处确实值得改的:

**useDeepLinkHireFlow**: agentId 变 reset state 的 effect 改成 render-phase setState (PR 3 同款 latch 模式),guard \`state.targetAgentId !== null\` 防循环。

**useFreeStatus**: 
- \`refresh\` useCallback inline 进唯一的 effect
- \`isFreeUser\` useMemo 删掉(返回 boolean,primitive 天然 referentially stable,no identity worth memoizing)
- \`isFreeExpired\` / \`freeDaysLeft\` 的 useMemo 删掉 — 这两个**反而是 bug**:\`Date.now()\` 是隐式输入,useMemo 没法 track,导致 memo 在 \`[isFreeUser, info]\` 上,countdown 直到下一次 auth/credits 事件触发前都冻住。inline 才正确。

## Why 系列只到 5 个 PR(原计划过 5)
原审计高估了反模式数量,深读后:
- PR 4 三个 B 类候选全是 prop/事件驱动,合不进 handler
- PR 5 六个候选只一个真有效;其他要么 SSR 风险(useState initializer + localStorage),要么 unmount-only cleanup 是 canonical 写法,要么是 navigate 自动化没事件 handler 可挪
- "scaling-down" 比硬上重要 — \`feedback_review_followup_verify_first\` 的精神

## Stats
2 files / +23 / -32 / 1 effect 删除 + 1 useCallback 删除 + 3 useMemo 删除 + 顺带修一个 stale-time bug

## Test plan
- [x] \`pnpm lint\` 绿
- [x] \`npx tsc --noEmit\` 绿
- [x] 相关单测全过(30/30: useDeepLinkHireFlow + useFreeStatus)
- [ ] CI 全绿
- [ ] staging:deep-link 流换 agentId 不卡;free 用户 countdown 显示

## Series 收尾
全 5 PR 系列 (#1396 / #1414 / #1421 / #1425 / 本):
- 真正消除的反模式 effect:11(ref-sync × 5,state-reset effect → key prop × 2,latch effect × 2,disconnect ref reset 后续维持 effect,render-phase reset × 1)
- 顺带:1 useCallback,3 useMemo,1 stale-time bug

🤖 Generated with [Claude Code](https://claude.com/claude-code)

**Stats:** +95 -32 (127 changes)

---

## 25979563 — 2026-04-29T03:49:11Z
**Author:** Chris@ZooClaw

**Message:**
```
refactor(web): lift effect-driven latch and reset to render-time (#1421)

## Summary
\`feature/use-less-effect\` 系列第 3 PR。把两类 React 官方文档明确推荐"渲染期做"的 effect
改成渲染期表达。

- **useDeepLinkHireFlow**: \`canUseChat\` / \`isChatReady\` 两个 ever-true
latch 从 \`useEffect(() => { if (x) setX(true) }, [x])\` 改成 \`if (x &&
!xEver) setXEver(true)\`(渲染期 setState)。React 官方"Storing information from
previous
renders"(https://react.dev/reference/react/useState#storing-information-from-previous-renders)就是给这种单调
latch 设计的。
- **useSubagentChat**: \`useEffect(() => { if (ws.status !==
'connected') { reset refs }}, [ws.status])\` 是纯 idempotent ref 写,直接挪到渲染期
\`if\` 块。session-scoped reset 上一 PR 已经迁到 \`key={sessionKey}\` 父级重挂。

## Why
- **Latch**: 渲染期 setState 在 React 调度里被认为是 "current render
的一部分",不会触发额外一次组件树渲染。effect 版本要等 commit 才 setState 再触发新一轮 render。改写后单调
latch 跟收到新值的那一帧同步生效。
- **Ref reset**: ref 写不参与 React 调度;放 effect 里只是多一层 closure deps,语义没区别。
- 不再追"effect → useMemo"机械式改写——\`useAgentSettings\` / \`useClawSettings\`
的 \`useEffect(() => loadSettings(), [loadSettings])\` 表面像派生状态、实际是"deps
变就 reload data",这是 useEffect 本职、也是 RQ 迁移 v2 的范围,不在本 PR 处理。

## Stats
2 files / +14 / -14 (净 0,主要是注释扩写) / 2 effect 删除 + 1 effect 改渲染期

## Test plan
- [x] \`pnpm lint\` 绿
- [x] \`npx tsc --noEmit\` 绿
- [x] 相关单测全过(61/61)——特别是 \`useDeepLinkHireFlow.unit.spec.ts:202\` 的
latch oscillation 回归测试不动通过,直接验证 render-time setState 保留单调性
- [ ] CI 全绿
- [ ] staging 复跑:deep-link 流(login → catalog 加载 → bot init →
redirect)、subagent chat 断线重连

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR #1421:** refactor(web): lift effect-driven latch and reset to render-time

**PR Body:**
## Summary
\`feature/use-less-effect\` 系列第 3 PR。把两类 React 官方文档明确推荐"渲染期做"的 effect 改成渲染期表达。

- **useDeepLinkHireFlow**: \`canUseChat\` / \`isChatReady\` 两个 ever-true latch 从 \`useEffect(() => { if (x) setX(true) }, [x])\` 改成 \`if (x && !xEver) setXEver(true)\`(渲染期 setState)。React 官方"Storing information from previous renders"(https://react.dev/reference/react/useState#storing-information-from-previous-renders)就是给这种单调 latch 设计的。
- **useSubagentChat**: \`useEffect(() => { if (ws.status !== 'connected') { reset refs }}, [ws.status])\` 是纯 idempotent ref 写,直接挪到渲染期 \`if\` 块。session-scoped reset 上一 PR 已经迁到 \`key={sessionKey}\` 父级重挂。

## Why
- **Latch**: 渲染期 setState 在 React 调度里被认为是 "current render 的一部分",不会触发额外一次组件树渲染。effect 版本要等 commit 才 setState 再触发新一轮 render。改写后单调 latch 跟收到新值的那一帧同步生效。
- **Ref reset**: ref 写不参与 React 调度;放 effect 里只是多一层 closure deps,语义没区别。
- 不再追"effect → useMemo"机械式改写——\`useAgentSettings\` / \`useClawSettings\` 的 \`useEffect(() => loadSettings(), [loadSettings])\` 表面像派生状态、实际是"deps 变就 reload data",这是 useEffect 本职、也是 RQ 迁移 v2 的范围,不在本 PR 处理。

## Stats
2 files / +14 / -14 (净 0,主要是注释扩写) / 2 effect 删除 + 1 effect 改渲染期

## Test plan
- [x] \`pnpm lint\` 绿
- [x] \`npx tsc --noEmit\` 绿
- [x] 相关单测全过(61/61)——特别是 \`useDeepLinkHireFlow.unit.spec.ts:202\` 的 latch oscillation 回归测试不动通过,直接验证 render-time setState 保留单调性
- [ ] CI 全绿
- [ ] staging 复跑:deep-link 流(login → catalog 加载 → bot init → redirect)、subagent chat 断线重连

🤖 Generated with [Claude Code](https://claude.com/claude-code)

**Stats:** +14 -7 (21 changes)

---

## ba0bce80 — 2026-04-29T03:42:32Z
**Author:** dependabot[bot]

**Message:**
```
chore(deps-dev): bump @vitejs/plugin-react from 4.7.0 to 5.2.0 in /web (#1419)

Bumps
[@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/tree/HEAD/packages/plugin-react)
from 4.7.0 to 5.2.0.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/vitejs/vite-plugin-react/releases"><code>@​vitejs/plugin-react</code>'s
releases</a>.</em></p>
<blockquote>
<h2>plugin-react@5.2.0</h2>
<h3>Add Vite 8 to peerDependencies range <a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/1143">#1143</a></h3>
<p>This plugin is compatible with Vite 8.</p>
<h2>plugin-react@5.1.4</h2>
<h3>Fix <code>canSkipBabel</code> not accounting for
<code>babel.overrides</code> (<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/1098">#1098</a>)</h3>
<p>When configuring <code>babel.overrides</code> without top-level
plugins or presets, Babel was incorrectly skipped. The
<code>canSkipBabel</code> function now checks for
<code>overrides.length</code> to ensure override configurations are
processed.</p>
<h2>plugin-react@5.1.3</h2>
<p>No release notes provided.</p>
<h2>plugin-react@5.1.2</h2>
<p>No release notes provided.</p>
<h2>plugin-react@5.1.1</h2>
<h3>Update code to support newer <code>rolldown-vite</code> (<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/976">#976</a>)</h3>
<p><code>rolldown-vite</code> will remove
<code>optimizeDeps.rollupOptions</code> in favor of
<code>optimizeDeps.rolldownOptions</code> soon. This plugin now uses
<code>optimizeDeps.rolldownOptions</code> to support newer
<code>rolldown-vite</code>. Please update <code>rolldown-vite</code> to
the latest version if you are using an older version.</p>
<h2>plugin-react@5.1.0</h2>
<h3>Add <code>@vitejs/plugin-react/preamble</code> virtual module for
SSR HMR (<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/890">#890</a>)</h3>
<p>SSR applications can now initialize HMR runtime by importing
<code>@vitejs/plugin-react/preamble</code> at the top of their client
entry instead of manually calling <code>transformIndexHtml</code>. This
simplifies SSR setup for applications that don't use the
<code>transformIndexHtml</code> API.</p>
<h3>Fix raw Rolldown support for Rolldown 1.0.0-beta.44+ (<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/930">#930</a>)</h3>
<p>Rolldown 1.0.0-beta.44+ removed the top-level <code>jsx</code> option
in favor of <code>transform.jsx</code>. This plugin now uses the
<code>transform.jsx</code> option to support Rolldown
1.0.0-beta.44+.</p>
<h2>plugin-react@5.0.4</h2>
<h3>Perf: use native refresh wrapper plugin in rolldown-vite (<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/881">#881</a>)</h3>
<h2>plugin-react@5.0.3</h2>
<h3>HMR did not work for components imported with queries with
rolldown-vite (<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/872">#872</a>)</h3>
<h3>Perf: simplify refresh wrapper generation (<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/835">#835</a>)</h3>
<h2>plugin-react@5.0.2</h2>
<h3>Skip transform hook completely in rolldown-vite in dev if possible
(<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/783">#783</a>)</h3>
<h2>plugin-react@5.0.1</h2>
<h3>Set <code>optimizeDeps.rollupOptions.transform.jsx</code> instead of
<code>optimizeDeps.rollupOptions.jsx</code> for rolldown-vite (<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/735">#735</a>)</h3>
<p><code>optimizeDeps.rollupOptions.jsx</code> is going to be deprecated
in favor of <code>optimizeDeps.rollupOptions.transform.jsx</code>.</p>
<h3>Perf: skip <code>babel-plugin-react-compiler</code> if code has no
<code>&quot;use memo&quot;</code> when <code>{ compilationMode:
&quot;annotation&quot; }</code> (<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/734">#734</a>)</h3>
<h3>Respect tsconfig <code>jsxImportSource</code> (<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/726">#726</a>)</h3>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/vitejs/vite-plugin-react/blob/plugin-react@5.2.0/packages/plugin-react/CHANGELOG.md"><code>@​vitejs/plugin-react</code>'s
changelog</a>.</em></p>
<blockquote>
<h2>5.2.0 (2026-03-12)</h2>
<h3>Add Vite 8 to peerDependencies range <a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/1143">#1143</a></h3>
<p>This plugin is compatible with Vite 8.</p>
<h2>5.1.4 (2026-02-10)</h2>
<h3>Fix <code>canSkipBabel</code> not accounting for
<code>babel.overrides</code> (<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/1098">#1098</a>)</h3>
<p>When configuring <code>babel.overrides</code> without top-level
plugins or presets, Babel was incorrectly skipped. The
<code>canSkipBabel</code> function now checks for
<code>overrides.length</code> to ensure override configurations are
processed.</p>
<h2>5.1.3 (2026-02-02)</h2>
<h2>5.1.2 (2025-12-08)</h2>
<h2>5.1.1 (2025-11-12)</h2>
<h3>Update code to support newer <code>rolldown-vite</code> (<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/976">#976</a>)</h3>
<p><code>rolldown-vite</code> will remove
<code>optimizeDeps.rollupOptions</code> in favor of
<code>optimizeDeps.rolldownOptions</code> soon. This plugin now uses
<code>optimizeDeps.rolldownOptions</code> to support newer
<code>rolldown-vite</code>. Please update <code>rolldown-vite</code> to
the latest version if you are using an older version.</p>
<h2>5.1.0 (2025-10-24)</h2>
<h3>Add <code>@vitejs/plugin-react/preamble</code> virtual module for
SSR HMR (<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/890">#890</a>)</h3>
<p>SSR applications can now initialize HMR runtime by importing
<code>@vitejs/plugin-react/preamble</code> at the top of their client
entry instead of manually calling <code>transformIndexHtml</code>. This
simplifies SSR setup for applications that don't use the
<code>transformIndexHtml</code> API.</p>
<h3>Fix raw Rolldown support for Rolldown 1.0.0-beta.44+ (<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/930">#930</a>)</h3>
<p>Rolldown 1.0.0-beta.44+ removed the top-level <code>jsx</code> option
in favor of <code>transform.jsx</code>. This plugin now uses the
<code>transform.jsx</code> option to support Rolldown
1.0.0-beta.44+.</p>
<h2>5.0.4 (2025-09-27)</h2>
<h3>Perf: use native refresh wrapper plugin in rolldown-vite (<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/881">#881</a>)</h3>
<h2>5.0.3 (2025-09-17)</h2>
<h3>HMR did not work for components imported with queries with
rolldown-vite (<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/872">#872</a>)</h3>
<h3>Perf: simplify refresh wrapper generation (<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/835">#835</a>)</h3>
<h2>5.0.2 (2025-08-28)</h2>
<h3>Skip transform hook completely in rolldown-vite in dev if possible
(<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/783">#783</a>)</h3>
<h2>5.0.1 (2025-08-19)</h2>
<h3>Set <code>optimizeDeps.rollupOptions.transform.jsx</code> instead of
<code>optimizeDeps.rollupOptions.jsx</code> for rolldown-vite (<a
href="https://redirect.github.com/vitejs/vite-plugin-react/pull/735">#735</a>)</h3>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/vitejs/vite-plugin-react/commit/fda3a86095556b49ae3c995eb57a30d4e0b8fa8d"><code>fda3a86</code></a>
release: plugin-react@5.2.0</li>
<li><a
href="https://github.com/vitejs/vite-plugin-react/commit/99ab1b67b3ce8f67446a0f432222cbd1763cefc5"><code>99ab1b6</code></a>
feat(react): add Vite 8 to peer dependency (<a
href="https://github.com/vitejs/vite-plugin-react/tree/HEAD/packages/plugin-react/issues/1143">#1143</a>)</li>
<li><a
href="https://github.com/vitejs/vite-plugin-react/commit/f066114c3e6bf18f5209ff3d3ef6bf1ab46d3866"><code>f066114</code></a>
release: plugin-react@5.1.4</li>
<li><a
href="https://github.com/vitejs/vite-plugin-react/commit/e299dcab475952f3305b24eef6118f7f47e65f31"><code>e299dca</code></a>
fix(plugin-react): <code>canSkipBabel</code> not checking
<code>babel.overrides</code> (<a
href="https://github.com/vitejs/vite-plugin-react/tree/HEAD/packages/plugin-react/issues/1098">#1098</a>)</li>
<li><a
href="https://github.com/vitejs/vite-plugin-react/commit/12ffadcd9afdb19a703ffddb3d3cc961178066c4"><code>12ffadc</code></a>
fix(deps): update all non-major dependencies (<a
href="https://github.com/vitejs/vite-plugin-react/tree/HEAD/packages/plugin-react/issues/1103">#1103</a>)</li>
<li><a
href="https://github.com/vitejs/vite-plugin-react/commit/cf0cb8aa3398e312f4e91b702281806aad004cd7"><code>cf0cb8a</code></a>
release: plugin-react@5.1.3</li>
<li><a
href="https://github.com/vitejs/vite-plugin-react/commit/99e480cf01323268b6f7d5e582ba1662728845d9"><code>99e480c</code></a>
fix(deps): update all non-major dependencies (<a
href="https://github.com/vitejs/vite-plugin-react/tree/HEAD/packages/plugin-react/issues/1090">#1090</a>)</li>
<li><a
href="https://github.com/vitejs/vite-plugin-react/commit/77f5e429d49b53c4115581abccaa9f5405bdf079"><code>77f5e42</code></a>
fix(deps): update react 19.2.4 (<a
href="https://github.com/vitejs/vite-plugin-react/tree/HEAD/packages/plugin-react/issues/1084">#1084</a>)</li>
<li><a
href="https://github.com/vitejs/vite-plugin-react/commit/e327da491fcc0eb9e10b98d7dd674b8375cb0f4f"><code>e327da4</code></a>
fix(deps): update all non-major dependencies (<a
href="https://github.com/vitejs/vite-plugin-react/tree/HEAD/packages/plugin-react/issues/1083">#1083</a>)</li>
<li><a
href="https://github.com/vitejs/vite-plugin-react/commit/3d3dbc2c1de09f1d2bd3ff3483415a73bdf61e96"><code>3d3dbc2</code></a>
chore: add metadata for vite-plugin-registry (<a
href="https://github.com/vitejs/vite-plugin-react/tree/HEAD/packages/plugin-react/issues/1078">#1078</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/vitejs/vite-plugin-react/commits/plugin-react@5.2.0/packages/plugin-react">compare
view</a></li>
</ul>
</details>
<details>
<summary>Maintainer changes</summary>
<p>This version was pushed to npm by <a
href="https://www.npmjs.com/~GitHub%20Actions">GitHub Actions</a>, a new
releaser for <code>@​vitejs/plugin-react</code> since your current
version.</p>
</details>
<br />


[![Dependabot compatibility
score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=@vitejs/plugin-react&package-manager=npm_and_yarn&previous-version=4.7.0&new-version=5.2.0)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

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

---------

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
Co-authored-by: chris-srp <chris@srp.one>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR #1419:** chore(deps-dev): bump @vitejs/plugin-react from 4.7.0 to 5.2.0 in /web

**PR Body:**
Bumps [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/tree/HEAD/packages/plugin-react) from 4.7.0 to 5.2.0.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/vitejs/vite-plugin-react/releases"><code>@​vitejs/plugin-react</code>'s releases</a>.</em></p>
<blockquote>
<h2>plugin-react@5.2.0</h2>
<h3>Add Vite 8 to peerDependencies range <a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/1143">#1143</a></h3>
<p>This plugin is compatible with Vite 8.</p>
<h2>plugin-react@5.1.4</h2>
<h3>Fix <code>canSkipBabel</code> not accounting for <code>babel.overrides</code> (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/1098">#1098</a>)</h3>
<p>When configuring <code>babel.overrides</code> without top-level plugins or presets, Babel was incorrectly skipped. The <code>canSkipBabel</code> function now checks for <code>overrides.length</code> to ensure override configurations are processed.</p>
<h2>plugin-react@5.1.3</h2>
<p>No release notes provided.</p>
<h2>plugin-react@5.1.2</h2>
<p>No release notes provided.</p>
<h2>plugin-react@5.1.1</h2>
<h3>Update code to support newer <code>rolldown-vite</code> (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/976">#976</a>)</h3>
<p><code>rolldown-vite</code> will remove <code>optimizeDeps.rollupOptions</code> in favor of <code>optimizeDeps.rolldownOptions</code> soon. This plugin now uses <code>optimizeDeps.rolldownOptions</code> to support newer <code>rolldown-vite</code>. Please update <code>rolldown-vite</code> to the latest version if you are using an older version.</p>
<h2>plugin-react@5.1.0</h2>
<h3>Add <code>@vitejs/plugin-react/preamble</code> virtual module for SSR HMR (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/890">#890</a>)</h3>
<p>SSR applications can now initialize HMR runtime by importing <code>@vitejs/plugin-react/preamble</code> at the top of their client entry instead of manually calling <code>transformIndexHtml</code>. This simplifies SSR setup for applications that don't use the <code>transformIndexHtml</code> API.</p>
<h3>Fix raw Rolldown support for Rolldown 1.0.0-beta.44+ (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/930">#930</a>)</h3>
<p>Rolldown 1.0.0-beta.44+ removed the top-level <code>jsx</code> option in favor of <code>transform.jsx</code>. This plugin now uses the <code>transform.jsx</code> option to support Rolldown 1.0.0-beta.44+.</p>
<h2>plugin-react@5.0.4</h2>
<h3>Perf: use native refresh wrapper plugin in rolldown-vite (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/881">#881</a>)</h3>
<h2>plugin-react@5.0.3</h2>
<h3>HMR did not work for components imported with queries with rolldown-vite (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/872">#872</a>)</h3>
<h3>Perf: simplify refresh wrapper generation (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/835">#835</a>)</h3>
<h2>plugin-react@5.0.2</h2>
<h3>Skip transform hook completely in rolldown-vite in dev if possible (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/783">#783</a>)</h3>
<h2>plugin-react@5.0.1</h2>
<h3>Set <code>optimizeDeps.rollupOptions.transform.jsx</code> instead of <code>optimizeDeps.rollupOptions.jsx</code> for rolldown-vite (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/735">#735</a>)</h3>
<p><code>optimizeDeps.rollupOptions.jsx</code> is going to be deprecated in favor of <code>optimizeDeps.rollupOptions.transform.jsx</code>.</p>
<h3>Perf: skip <code>babel-plugin-react-compiler</code> if code has no <code>&quot;use memo&quot;</code> when <code>{ compilationMode: &quot;annotation&quot; }</code> (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/734">#734</a>)</h3>
<h3>Respect tsconfig <code>jsxImportSource</code> (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/726">#726</a>)</h3>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/vitejs/vite-plugin-react/blob/plugin-react@5.2.0/packages/plugin-react/CHANGELOG.md"><code>@​vitejs/plugin-react</code>'s changelog</a>.</em></p>
<blockquote>
<h2>5.2.0 (2026-03-12)</h2>
<h3>Add Vite 8 to peerDependencies range <a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/1143">#1143</a></h3>
<p>This plugin is compatible with Vite 8.</p>
<h2>5.1.4 (2026-02-10)</h2>
<h3>Fix <code>canSkipBabel</code> not accounting for <code>babel.overrides</code> (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/1098">#1098</a>)</h3>
<p>When configuring <code>babel.overrides</code> without top-level plugins or presets, Babel was incorrectly skipped. The <code>canSkipBabel</code> function now checks for <code>overrides.length</code> to ensure override configurations are processed.</p>
<h2>5.1.3 (2026-02-02)</h2>
<h2>5.1.2 (2025-12-08)</h2>
<h2>5.1.1 (2025-11-12)</h2>
<h3>Update code to support newer <code>rolldown-vite</code> (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/976">#976</a>)</h3>
<p><code>rolldown-vite</code> will remove <code>optimizeDeps.rollupOptions</code> in favor of <code>optimizeDeps.rolldownOptions</code> soon. This plugin now uses <code>optimizeDeps.rolldownOptions</code> to support newer <code>rolldown-vite</code>. Please update <code>rolldown-vite</code> to the latest version if you are using an older version.</p>
<h2>5.1.0 (2025-10-24)</h2>
<h3>Add <code>@vitejs/plugin-react/preamble</code> virtual module for SSR HMR (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/890">#890</a>)</h3>
<p>SSR applications can now initialize HMR runtime by importing <code>@vitejs/plugin-react/preamble</code> at the top of their client entry instead of manually calling <code>transformIndexHtml</code>. This simplifies SSR setup for applications that don't use the <code>transformIndexHtml</code> API.</p>
<h3>Fix raw Rolldown support for Rolldown 1.0.0-beta.44+ (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/930">#930</a>)</h3>
<p>Rolldown 1.0.0-beta.44+ removed the top-level <code>jsx</code> option in favor of <code>transform.jsx</code>. This plugin now uses the <code>transform.jsx</code> option to support Rolldown 1.0.0-beta.44+.</p>
<h2>5.0.4 (2025-09-27)</h2>
<h3>Perf: use native refresh wrapper plugin in rolldown-vite (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/881">#881</a>)</h3>
<h2>5.0.3 (2025-09-17)</h2>
<h3>HMR did not work for components imported with queries with rolldown-vite (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/872">#872</a>)</h3>
<h3>Perf: simplify refresh wrapper generation (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/835">#835</a>)</h3>
<h2>5.0.2 (2025-08-28)</h2>
<h3>Skip transform hook completely in rolldown-vite in dev if possible (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/783">#783</a>)</h3>
<h2>5.0.1 (2025-08-19)</h2>
<h3>Set <code>optimizeDeps.rollupOptions.transform.jsx</code> instead of <code>optimizeDeps.rollupOptions.jsx</code> for rolldown-vite (<a href="https://redirect.github.com/vitejs/vite-plugin-react/pull/735">#735</a>)</h3>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/vitejs/vite-plugin-react/commit/fda3a86095556b49ae3c995eb57a30d4e0b8fa8d"><code>fda3a86</code></a> release: plugin-react@5.2.0</li>
<li><a href="https://github.com/vitejs/vite-plugin-react/commit/99ab1b67b3ce8f67446a0f432222cbd1763cefc5"><code>99ab1b6</code></a> feat(react): add Vite 8 to peer dependency (<a href="https://github.com/vitejs/vite-plugin-react/tree/HEAD/packages/plugin-react/issues/1143">#1143</a>)</li>
<li><a href="https://github.com/vitejs/vite-plugin-react/commit/f066114c3e6bf18f5209ff3d3ef6bf1ab46d3866"><code>f066114</code></a> release: plugin-react@5.1.4</li>
<li><a href="https://github.com/vitejs/vite-plugin-react/commit/e299dcab475952f3305b24eef6118f7f47e65f31"><code>e299dca</code></a> fix(plugin-react): <code>canSkipBabel</code> not checking <code>babel.overrides</code> (<a href="https://github.com/vitejs/vite-plugin-react/tree/HEAD/packages/plugin-react/issues/1098">#1098</a>)</li>
<li><a href="https://github.com/vitejs/vite-plugin-react/commit/12ffadcd9afdb19a703ffddb3d3cc961178066c4"><code>12ffadc</code></a> fix(deps): update all non-major dependencies (<a href="https://github.com/vitejs/vite-plugin-react/tree/HEAD/packages/plugin-react/issues/1103">#1103</a>)</li>
<li><a href="https://github.com/vitejs/vite-plugin-react/commit/cf0cb8aa3398e312f4e91b702281806aad004cd7"><code>cf0cb8a</code></a> release: plugin-react@5.1.3</li>
<li><a href="https://github.com/vitejs/vite-plugin-react/commit/99e480cf01323268b6f7d5e582ba1662728845d9"><code>99e480c</code></a> fix(deps): update all non-major dependencies (<a href="https://github.com/vitejs/vite-plugin-react/tree/HEAD/packages/plugin-react/issues/1090">#1090</a>)</li>
<li><a href="https://github.com/vitejs/vite-plugin-react/commit/77f5e429d49b53c4115581abccaa9f5405bdf079"><code>77f5e42</code></a> fix(deps): update react 19.2.4 (<a href="https://github.com/vitejs/vite-plugin-react/tree/HEAD/packages/plugin-react/issues/1084">#1084</a>)</li>
<li><a href="https://github.com/vitejs/vite-plugin-react/commit/e327da491fcc0eb9e10b98d7dd674b8375cb0f4f"><code>e327da4</code></a> fix(deps): update all non-major dependencies (<a href="https://github.com/vitejs/vite-plugin-react/tree/HEAD/packages/plugin-react/issues/1083">#1083</a>)</li>
<li><a href="https://github.com/vitejs/vite-plugin-react/commit/3d3dbc2c1de09f1d2bd3ff3483415a73bdf61e96"><code>3d3dbc2</code></a> chore: add metadata for vite-plugin-registry (<a href="https://github.com/vitejs/vite-plugin-react/tree/HEAD/packages/plugin-react/issues/1078">#1078</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/vitejs/vite-plugin-react/commits/plugin-react@5.2.0/packages/plugin-react">compare view</a></li>
</ul>
</details>
<details>
<summary>Maintainer changes</summary>
<p>This version was pushed to npm by <a href="https://www.npmjs.com/~GitHub%20Actions">GitHub Actions</a>, a new releaser for <code>@​vitejs/plugin-react</code> since your current version.</p>
</details>
<br />


[![Dependabot compatibility score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=@vitejs/plugin-react&package-manager=npm_and_yarn&previous-version=4.7.0&new-version=5.2.0)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

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

**Stats:** +15 -15 (30 changes)

---

## 26c794d5 — 2026-04-29T03:41:56Z
**Author:** dependabot[bot]

**Message:**
```
chore(deps-dev): bump wrangler from 3.114.17 to 4.81.1 in /web (#1418)

Bumps
[wrangler](https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler)
from 3.114.17 to 4.81.1.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/cloudflare/workers-sdk/releases">wrangler's
releases</a>.</em></p>
<blockquote>
<h2>wrangler@4.81.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/cloudflare/workers-sdk/pull/13337">#13337</a>
<a
href="https://github.com/cloudflare/workers-sdk/commit/c510494e522927f60fa4915358a881cf73e31a39"><code>c510494</code></a>
Thanks <a
href="https://github.com/apps/dependabot"><code>@​dependabot</code></a>!
- Update dependencies of &quot;miniflare&quot;, &quot;wrangler&quot;</p>
<p>The following dependency versions have been updated:</p>
<table>
<thead>
<tr>
<th>Dependency</th>
<th>From</th>
<th>To</th>
</tr>
</thead>
<tbody>
<tr>
<td>workerd</td>
<td>1.20260405.1</td>
<td>1.20260408.1</td>
</tr>
</tbody>
</table>
</li>
<li>
<p><a
href="https://redirect.github.com/cloudflare/workers-sdk/pull/13362">#13362</a>
<a
href="https://github.com/cloudflare/workers-sdk/commit/8b71ecae4fed8f0bebf5789f1a617db26c0e4365"><code>8b71eca</code></a>
Thanks <a
href="https://github.com/apps/dependabot"><code>@​dependabot</code></a>!
- Update dependencies of &quot;miniflare&quot;, &quot;wrangler&quot;</p>
<p>The following dependency versions have been updated:</p>
<table>
<thead>
<tr>
<th>Dependency</th>
<th>From</th>
<th>To</th>
</tr>
</thead>
<tbody>
<tr>
<td>workerd</td>
<td>1.20260408.1</td>
<td>1.20260409.1</td>
</tr>
</tbody>
</table>
</li>
<li>
<p><a
href="https://redirect.github.com/cloudflare/workers-sdk/pull/13329">#13329</a>
<a
href="https://github.com/cloudflare/workers-sdk/commit/7ca6f6e98ff84e68e901ae35028435f4916ae1c2"><code>7ca6f6e</code></a>
Thanks <a href="https://github.com/G4brym"><code>@​G4brym</code></a>! -
fix: Treat AI Search bindings as always-remote in local dev</p>
<p>AI Search namespace (<code>ai_search_namespaces</code>) and instance
(<code>ai_search</code>) bindings are always-remote (they have no local
simulation), but <code>pickRemoteBindings()</code> did not include them
in its always-remote type list. This caused the remote proxy session to
exclude these bindings when <code>remote: true</code> was not explicitly
set in the config, resulting in broken AI Search bindings during
<code>wrangler dev</code>.</p>
<p>Additionally, <code>removeRemoteConfigFieldFromBindings()</code> in
the deploy config-diff logic was not stripping the <code>remote</code>
field from AI Search bindings, which could cause false config diffs
during deployment.</p>
</li>
<li>
<p>Updated dependencies [<a
href="https://github.com/cloudflare/workers-sdk/commit/42c7ef04385094c77f0c2830134fc38b2dc39b02"><code>42c7ef0</code></a>,
<a
href="https://github.com/cloudflare/workers-sdk/commit/c510494e522927f60fa4915358a881cf73e31a39"><code>c510494</code></a>,
<a
href="https://github.com/cloudflare/workers-sdk/commit/8b71ecae4fed8f0bebf5789f1a617db26c0e4365"><code>8b71eca</code></a>,
<a
href="https://github.com/cloudflare/workers-sdk/commit/a42e0e8b52df128513f85025f50eb985bc7f5748"><code>a42e0e8</code></a>]:</p>
<ul>
<li>miniflare@4.20260409.0</li>
</ul>
</li>
</ul>
<h2>wrangler@4.81.0</h2>
<h3>Minor Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/cloudflare/workers-sdk/pull/12932">#12932</a>
<a
href="https://github.com/cloudflare/workers-sdk/commit/96ee5d465833f4887653078115acea40de2893c0"><code>96ee5d4</code></a>
Thanks <a
href="https://github.com/thomasgauvin"><code>@​thomasgauvin</code></a>!
- feat: add <code>wrangler email routing</code> and <code>wrangler email
sending</code> commands</p>
<p>Email Routing commands:</p>
<ul>
<li><code>wrangler email routing list</code> - list zones with email
routing status</li>
<li><code>wrangler email routing settings &lt;domain&gt;</code> - get
email routing settings for a zone</li>
<li><code>wrangler email routing enable/disable &lt;domain&gt;</code> -
enable or disable email routing</li>
<li><code>wrangler email routing dns get/unlock &lt;domain&gt;</code> -
manage DNS records</li>
<li><code>wrangler email routing rules list/get/create/update/delete
&lt;domain&gt;</code> - manage routing rules (use <code>catch-all</code>
as the rule ID for the catch-all rule)</li>
<li><code>wrangler email routing addresses list/get/create/delete</code>
- manage destination addresses</li>
</ul>
<p>Email Sending commands:</p>
<ul>
<li><code>wrangler email sending list</code> - list zones with email
sending</li>
<li><code>wrangler email sending settings &lt;domain&gt;</code> - get
email sending settings for a zone</li>
<li><code>wrangler email sending enable &lt;domain&gt;</code> - enable
email sending for a zone or subdomain</li>
<li><code>wrangler email sending disable &lt;domain&gt;</code> - disable
email sending for a zone or subdomain</li>
<li><code>wrangler email sending dns get &lt;domain&gt;</code> - get DNS
records for a sending domain</li>
<li><code>wrangler email sending send</code> - send an email using the
builder API</li>
</ul>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/aad03412dd69a46331d902a1fc95611883079c3e"><code>aad0341</code></a>
Version Packages (<a
href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13355">#13355</a>)</li>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/8b71ecae4fed8f0bebf5789f1a617db26c0e4365"><code>8b71eca</code></a>
Bump the workerd-and-workers-types group with 2 updates (<a
href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13362">#13362</a>)</li>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/c510494e522927f60fa4915358a881cf73e31a39"><code>c510494</code></a>
Bump the workerd-and-workers-types group with 2 updates (<a
href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13337">#13337</a>)</li>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/ad6faef1a5cd0a6a45e22fc87f27fd05bee428c0"><code>ad6faef</code></a>
Remove some more <code>no-restricted-imports</code> lint disabling
comments from wrangle...</li>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/7ca6f6e98ff84e68e901ae35028435f4916ae1c2"><code>7ca6f6e</code></a>
[wrangler] Fix AI Search bindings not working in local dev without
explicit r...</li>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/36c2c130b991743ff203a31aff007850f08acb95"><code>36c2c13</code></a>
Version Packages (<a
href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13251">#13251</a>)</li>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/fa6d84fe4f07143522e4d41a2934c486d1c4b6d1"><code>fa6d84f</code></a>
Bump the workerd-and-workers-types group with 2 updates (<a
href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13305">#13305</a>)</li>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/6fa5dfddcbad1520db7c3d1bb12233001fe00e45"><code>6fa5dfd</code></a>
[wrangler] Use formatConfigSnippet for compatibility_date warning in dev
(<a
href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13">#13</a>...</li>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/7d318e1b7e5af62c0ed09d3e5a51af84294c372e"><code>7d318e1</code></a>
Bump the workerd-and-workers-types group across 1 directory with 2
updates (#...</li>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/8f0c5449f8c47035a8da25558ec64d119cdc14c4"><code>8f0c544</code></a>
Make <code>argsIgnorePattern</code> for <code>no-unused-vars</code> lint
rule more strict (<a
href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13180">#13180</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/cloudflare/workers-sdk/commits/wrangler@4.81.1/packages/wrangler">compare
view</a></li>
</ul>
</details>
<br />


[![Dependabot compatibility
score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=wrangler&package-manager=npm_and_yarn&previous-version=3.114.17&new-version=4.81.1)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

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

---------

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
Co-authored-by: chris-srp <chris@srp.one>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR #1418:** chore(deps-dev): bump wrangler from 3.114.17 to 4.81.1 in /web

**PR Body:**
Bumps [wrangler](https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler) from 3.114.17 to 4.81.1.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/cloudflare/workers-sdk/releases">wrangler's releases</a>.</em></p>
<blockquote>
<h2>wrangler@4.81.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/cloudflare/workers-sdk/pull/13337">#13337</a> <a href="https://github.com/cloudflare/workers-sdk/commit/c510494e522927f60fa4915358a881cf73e31a39"><code>c510494</code></a> Thanks <a href="https://github.com/apps/dependabot"><code>@​dependabot</code></a>! - Update dependencies of &quot;miniflare&quot;, &quot;wrangler&quot;</p>
<p>The following dependency versions have been updated:</p>
<table>
<thead>
<tr>
<th>Dependency</th>
<th>From</th>
<th>To</th>
</tr>
</thead>
<tbody>
<tr>
<td>workerd</td>
<td>1.20260405.1</td>
<td>1.20260408.1</td>
</tr>
</tbody>
</table>
</li>
<li>
<p><a href="https://redirect.github.com/cloudflare/workers-sdk/pull/13362">#13362</a> <a href="https://github.com/cloudflare/workers-sdk/commit/8b71ecae4fed8f0bebf5789f1a617db26c0e4365"><code>8b71eca</code></a> Thanks <a href="https://github.com/apps/dependabot"><code>@​dependabot</code></a>! - Update dependencies of &quot;miniflare&quot;, &quot;wrangler&quot;</p>
<p>The following dependency versions have been updated:</p>
<table>
<thead>
<tr>
<th>Dependency</th>
<th>From</th>
<th>To</th>
</tr>
</thead>
<tbody>
<tr>
<td>workerd</td>
<td>1.20260408.1</td>
<td>1.20260409.1</td>
</tr>
</tbody>
</table>
</li>
<li>
<p><a href="https://redirect.github.com/cloudflare/workers-sdk/pull/13329">#13329</a> <a href="https://github.com/cloudflare/workers-sdk/commit/7ca6f6e98ff84e68e901ae35028435f4916ae1c2"><code>7ca6f6e</code></a> Thanks <a href="https://github.com/G4brym"><code>@​G4brym</code></a>! - fix: Treat AI Search bindings as always-remote in local dev</p>
<p>AI Search namespace (<code>ai_search_namespaces</code>) and instance (<code>ai_search</code>) bindings are always-remote (they have no local simulation), but <code>pickRemoteBindings()</code> did not include them in its always-remote type list. This caused the remote proxy session to exclude these bindings when <code>remote: true</code> was not explicitly set in the config, resulting in broken AI Search bindings during <code>wrangler dev</code>.</p>
<p>Additionally, <code>removeRemoteConfigFieldFromBindings()</code> in the deploy config-diff logic was not stripping the <code>remote</code> field from AI Search bindings, which could cause false config diffs during deployment.</p>
</li>
<li>
<p>Updated dependencies [<a href="https://github.com/cloudflare/workers-sdk/commit/42c7ef04385094c77f0c2830134fc38b2dc39b02"><code>42c7ef0</code></a>, <a href="https://github.com/cloudflare/workers-sdk/commit/c510494e522927f60fa4915358a881cf73e31a39"><code>c510494</code></a>, <a href="https://github.com/cloudflare/workers-sdk/commit/8b71ecae4fed8f0bebf5789f1a617db26c0e4365"><code>8b71eca</code></a>, <a href="https://github.com/cloudflare/workers-sdk/commit/a42e0e8b52df128513f85025f50eb985bc7f5748"><code>a42e0e8</code></a>]:</p>
<ul>
<li>miniflare@4.20260409.0</li>
</ul>
</li>
</ul>
<h2>wrangler@4.81.0</h2>
<h3>Minor Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/cloudflare/workers-sdk/pull/12932">#12932</a> <a href="https://github.com/cloudflare/workers-sdk/commit/96ee5d465833f4887653078115acea40de2893c0"><code>96ee5d4</code></a> Thanks <a href="https://github.com/thomasgauvin"><code>@​thomasgauvin</code></a>! - feat: add <code>wrangler email routing</code> and <code>wrangler email sending</code> commands</p>
<p>Email Routing commands:</p>
<ul>
<li><code>wrangler email routing list</code> - list zones with email routing status</li>
<li><code>wrangler email routing settings &lt;domain&gt;</code> - get email routing settings for a zone</li>
<li><code>wrangler email routing enable/disable &lt;domain&gt;</code> - enable or disable email routing</li>
<li><code>wrangler email routing dns get/unlock &lt;domain&gt;</code> - manage DNS records</li>
<li><code>wrangler email routing rules list/get/create/update/delete &lt;domain&gt;</code> - manage routing rules (use <code>catch-all</code> as the rule ID for the catch-all rule)</li>
<li><code>wrangler email routing addresses list/get/create/delete</code> - manage destination addresses</li>
</ul>
<p>Email Sending commands:</p>
<ul>
<li><code>wrangler email sending list</code> - list zones with email sending</li>
<li><code>wrangler email sending settings &lt;domain&gt;</code> - get email sending settings for a zone</li>
<li><code>wrangler email sending enable &lt;domain&gt;</code> - enable email sending for a zone or subdomain</li>
<li><code>wrangler email sending disable &lt;domain&gt;</code> - disable email sending for a zone or subdomain</li>
<li><code>wrangler email sending dns get &lt;domain&gt;</code> - get DNS records for a sending domain</li>
<li><code>wrangler email sending send</code> - send an email using the builder API</li>
</ul>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/aad03412dd69a46331d902a1fc95611883079c3e"><code>aad0341</code></a> Version Packages (<a href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13355">#13355</a>)</li>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/8b71ecae4fed8f0bebf5789f1a617db26c0e4365"><code>8b71eca</code></a> Bump the workerd-and-workers-types group with 2 updates (<a href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13362">#13362</a>)</li>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/c510494e522927f60fa4915358a881cf73e31a39"><code>c510494</code></a> Bump the workerd-and-workers-types group with 2 updates (<a href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13337">#13337</a>)</li>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/ad6faef1a5cd0a6a45e22fc87f27fd05bee428c0"><code>ad6faef</code></a> Remove some more <code>no-restricted-imports</code> lint disabling comments from wrangle...</li>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/7ca6f6e98ff84e68e901ae35028435f4916ae1c2"><code>7ca6f6e</code></a> [wrangler] Fix AI Search bindings not working in local dev without explicit r...</li>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/36c2c130b991743ff203a31aff007850f08acb95"><code>36c2c13</code></a> Version Packages (<a href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13251">#13251</a>)</li>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/fa6d84fe4f07143522e4d41a2934c486d1c4b6d1"><code>fa6d84f</code></a> Bump the workerd-and-workers-types group with 2 updates (<a href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13305">#13305</a>)</li>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/6fa5dfddcbad1520db7c3d1bb12233001fe00e45"><code>6fa5dfd</code></a> [wrangler] Use formatConfigSnippet for compatibility_date warning in dev (<a href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13">#13</a>...</li>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/7d318e1b7e5af62c0ed09d3e5a51af84294c372e"><code>7d318e1</code></a> Bump the workerd-and-workers-types group across 1 directory with 2 updates (#...</li>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/8f0c5449f8c47035a8da25558ec64d119cdc14c4"><code>8f0c544</code></a> Make <code>argsIgnorePattern</code> for <code>no-unused-vars</code> lint rule more strict (<a href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13180">#13180</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/cloudflare/workers-sdk/commits/wrangler@4.81.1/packages/wrangler">compare view</a></li>
</ul>
</details>
<br />


[![Dependabot compatibility score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=wrangler&package-manager=npm_and_yarn&previous-version=3.114.17&new-version=4.81.1)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

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

**Stats:** +48 -51 (99 changes)

---

## 7fb7f8ce — 2026-04-29T03:41:27Z
**Author:** dependabot[bot]

**Message:**
```
chore(deps-dev): bump eslint from 9.39.3 to 9.39.4 in /web in the minor-and-patch group across 1 directory (#1416)

[//]: # (dependabot-start)
⚠️  **Dependabot is rebasing this PR** ⚠️ 

Rebasing might not happen immediately, so don't worry if this takes some
time.

Note: if you make any changes to this PR yourself, they will take
precedence over the rebase.

---

[//]: # (dependabot-end)

Bumps the minor-and-patch group with 1 update in the /web directory:
[eslint](https://github.com/eslint/eslint).

Updates `eslint` from 9.39.3 to 9.39.4
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/eslint/eslint/releases">eslint's
releases</a>.</em></p>
<blockquote>
<h2>v9.39.4</h2>
<h2>Bug Fixes</h2>
<ul>
<li><a
href="https://github.com/eslint/eslint/commit/f18f6c8ae92a1bcfc558f48c0bd863ea94067459"><code>f18f6c8</code></a>
fix: update dependency minimatch to ^3.1.5 (<a
href="https://redirect.github.com/eslint/eslint/issues/20564">#20564</a>)
(Milos Djermanovic)</li>
<li><a
href="https://github.com/eslint/eslint/commit/a3c868f6ef103c1caff9d15f744f9ebd995e872f"><code>a3c868f</code></a>
fix: update dependency <code>@​eslint/eslintrc</code> to ^3.3.4 (<a
href="https://redirect.github.com/eslint/eslint/issues/20554">#20554</a>)
(Milos Djermanovic)</li>
<li><a
href="https://github.com/eslint/eslint/commit/234d005da6cd3c924f359e3783fbf565a3c047c3"><code>234d005</code></a>
fix: minimatch security vulnerability patch for v9.x (<a
href="https://redirect.github.com/eslint/eslint/issues/20549">#20549</a>)
(Andrej Beles)</li>
<li><a
href="https://github.com/eslint/eslint/commit/b1b37eecaa033d2e390e1d8f1d6e68d0f5ff3a6a"><code>b1b37ee</code></a>
fix: update <code>ajv</code> to <code>6.14.0</code> to address security
vulnerabilities (<a
href="https://redirect.github.com/eslint/eslint/issues/20538">#20538</a>)
(루밀LuMir)</li>
</ul>
<h2>Documentation</h2>
<ul>
<li><a
href="https://github.com/eslint/eslint/commit/46751526037682f8b42abcfb3e06d19213719347"><code>4675152</code></a>
docs: add deprecation notice partial (<a
href="https://redirect.github.com/eslint/eslint/issues/20520">#20520</a>)
(Milos Djermanovic)</li>
</ul>
<h2>Chores</h2>
<ul>
<li><a
href="https://github.com/eslint/eslint/commit/b8b4eb15901c1bd6ef40d2589da4ae75795c0f6e"><code>b8b4eb1</code></a>
chore: update dependencies for ESLint v9.39.4 (<a
href="https://redirect.github.com/eslint/eslint/issues/20596">#20596</a>)
(Francesco Trotta)</li>
<li><a
href="https://github.com/eslint/eslint/commit/71b2f6b628b76157b4a2a296cb969dc56abb296c"><code>71b2f6b</code></a>
chore: package.json update for <code>@​eslint/js</code> release
(Jenkins)</li>
<li><a
href="https://github.com/eslint/eslint/commit/1d16c2fa3998440ae7b0f6e2612935bd6b0ded1d"><code>1d16c2f</code></a>
ci: pin Node.js 25.6.1 (<a
href="https://redirect.github.com/eslint/eslint/issues/20563">#20563</a>)
(Milos Djermanovic)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/eslint/eslint/commit/f5770b0df0d3ffff6a428d1c19a99bdb794053a3"><code>f5770b0</code></a>
9.39.4</li>
<li><a
href="https://github.com/eslint/eslint/commit/c30147a0514fdcf3711493d7beef454223c25493"><code>c30147a</code></a>
Build: changelog update for 9.39.4</li>
<li><a
href="https://github.com/eslint/eslint/commit/b8b4eb15901c1bd6ef40d2589da4ae75795c0f6e"><code>b8b4eb1</code></a>
chore: update dependencies for ESLint v9.39.4 (<a
href="https://redirect.github.com/eslint/eslint/issues/20596">#20596</a>)</li>
<li><a
href="https://github.com/eslint/eslint/commit/71b2f6b628b76157b4a2a296cb969dc56abb296c"><code>71b2f6b</code></a>
chore: package.json update for <code>@​eslint/js</code> release</li>
<li><a
href="https://github.com/eslint/eslint/commit/46751526037682f8b42abcfb3e06d19213719347"><code>4675152</code></a>
docs: add deprecation notice partial (<a
href="https://redirect.github.com/eslint/eslint/issues/20520">#20520</a>)</li>
<li><a
href="https://github.com/eslint/eslint/commit/f18f6c8ae92a1bcfc558f48c0bd863ea94067459"><code>f18f6c8</code></a>
fix: update dependency minimatch to ^3.1.5 (<a
href="https://redirect.github.com/eslint/eslint/issues/20564">#20564</a>)</li>
<li><a
href="https://github.com/eslint/eslint/commit/1d16c2fa3998440ae7b0f6e2612935bd6b0ded1d"><code>1d16c2f</code></a>
ci: pin Node.js 25.6.1 (<a
href="https://redirect.github.com/eslint/eslint/issues/20563">#20563</a>)</li>
<li><a
href="https://github.com/eslint/eslint/commit/a3c868f6ef103c1caff9d15f744f9ebd995e872f"><code>a3c868f</code></a>
fix: update dependency <code>@​eslint/eslintrc</code> to ^3.3.4 (<a
href="https://redirect.github.com/eslint/eslint/issues/20554">#20554</a>)</li>
<li><a
href="https://github.com/eslint/eslint/commit/234d005da6cd3c924f359e3783fbf565a3c047c3"><code>234d005</code></a>
fix: minimatch security vulnerability patch for v9.x (<a
href="https://redirect.github.com/eslint/eslint/issues/20549">#20549</a>)</li>
<li><a
href="https://github.com/eslint/eslint/commit/b1b37eecaa033d2e390e1d8f1d6e68d0f5ff3a6a"><code>b1b37ee</code></a>
fix: update <code>ajv</code> to <code>6.14.0</code> to address security
vulnerabilities (<a
href="https://redirect.github.com/eslint/eslint/issues/20538">#20538</a>)</li>
<li>See full diff in <a
href="https://github.com/eslint/eslint/compare/v9.39.3...v9.39.4">compare
view</a></li>
</ul>
</details>
<br />

---------

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
Co-authored-by: chris-srp <chris@srp.one>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR #1416:** chore(deps-dev): bump eslint from 9.39.3 to 9.39.4 in /web in the minor-and-patch group across 1 directory

**PR Body:**
Bumps the minor-and-patch group with 1 update in the /web directory: [eslint](https://github.com/eslint/eslint).

Updates `eslint` from 9.39.3 to 9.39.4
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/eslint/eslint/releases">eslint's releases</a>.</em></p>
<blockquote>
<h2>v9.39.4</h2>
<h2>Bug Fixes</h2>
<ul>
<li><a href="https://github.com/eslint/eslint/commit/f18f6c8ae92a1bcfc558f48c0bd863ea94067459"><code>f18f6c8</code></a> fix: update dependency minimatch to ^3.1.5 (<a href="https://redirect.github.com/eslint/eslint/issues/20564">#20564</a>) (Milos Djermanovic)</li>
<li><a href="https://github.com/eslint/eslint/commit/a3c868f6ef103c1caff9d15f744f9ebd995e872f"><code>a3c868f</code></a> fix: update dependency <code>@​eslint/eslintrc</code> to ^3.3.4 (<a href="https://redirect.github.com/eslint/eslint/issues/20554">#20554</a>) (Milos Djermanovic)</li>
<li><a href="https://github.com/eslint/eslint/commit/234d005da6cd3c924f359e3783fbf565a3c047c3"><code>234d005</code></a> fix: minimatch security vulnerability patch for v9.x (<a href="https://redirect.github.com/eslint/eslint/issues/20549">#20549</a>) (Andrej Beles)</li>
<li><a href="https://github.com/eslint/eslint/commit/b1b37eecaa033d2e390e1d8f1d6e68d0f5ff3a6a"><code>b1b37ee</code></a> fix: update <code>ajv</code> to <code>6.14.0</code> to address security vulnerabilities (<a href="https://redirect.github.com/eslint/eslint/issues/20538">#20538</a>) (루밀LuMir)</li>
</ul>
<h2>Documentation</h2>
<ul>
<li><a href="https://github.com/eslint/eslint/commit/46751526037682f8b42abcfb3e06d19213719347"><code>4675152</code></a> docs: add deprecation notice partial (<a href="https://redirect.github.com/eslint/eslint/issues/20520">#20520</a>) (Milos Djermanovic)</li>
</ul>
<h2>Chores</h2>
<ul>
<li><a href="https://github.com/eslint/eslint/commit/b8b4eb15901c1bd6ef40d2589da4ae75795c0f6e"><code>b8b4eb1</code></a> chore: update dependencies for ESLint v9.39.4 (<a href="https://redirect.github.com/eslint/eslint/issues/20596">#20596</a>) (Francesco Trotta)</li>
<li><a href="https://github.com/eslint/eslint/commit/71b2f6b628b76157b4a2a296cb969dc56abb296c"><code>71b2f6b</code></a> chore: package.json update for <code>@​eslint/js</code> release (Jenkins)</li>
<li><a href="https://github.com/eslint/eslint/commit/1d16c2fa3998440ae7b0f6e2612935bd6b0ded1d"><code>1d16c2f</code></a> ci: pin Node.js 25.6.1 (<a href="https://redirect.github.com/eslint/eslint/issues/20563">#20563</a>) (Milos Djermanovic)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/eslint/eslint/commit/f5770b0df0d3ffff6a428d1c19a99bdb794053a3"><code>f5770b0</code></a> 9.39.4</li>
<li><a href="https://github.com/eslint/eslint/commit/c30147a0514fdcf3711493d7beef454223c25493"><code>c30147a</code></a> Build: changelog update for 9.39.4</li>
<li><a href="https://github.com/eslint/eslint/commit/b8b4eb15901c1bd6ef40d2589da4ae75795c0f6e"><code>b8b4eb1</code></a> chore: update dependencies for ESLint v9.39.4 (<a href="https://redirect.github.com/eslint/eslint/issues/20596">#20596</a>)</li>
<li><a href="https://github.com/eslint/eslint/commit/71b2f6b628b76157b4a2a296cb969dc56abb296c"><code>71b2f6b</code></a> chore: package.json update for <code>@​eslint/js</code> release</li>
<li><a href="https://github.com/eslint/eslint/commit/46751526037682f8b42abcfb3e06d19213719347"><code>4675152</code></a> docs: add deprecation notice partial (<a href="https://redirect.github.com/eslint/eslint/issues/20520">#20520</a>)</li>
<li><a href="https://github.com/eslint/eslint/commit/f18f6c8ae92a1bcfc558f48c0bd863ea94067459"><code>f18f6c8</code></a> fix: update dependency minimatch to ^3.1.5 (<a href="https://redirect.github.com/eslint/eslint/issues/20564">#20564</a>)</li>
<li><a href="https://github.com/eslint/eslint/commit/1d16c2fa3998440ae7b0f6e2612935bd6b0ded1d"><code>1d16c2f</code></a> ci: pin Node.js 25.6.1 (<a href="https://redirect.github.com/eslint/eslint/issues/20563">#20563</a>)</li>
<li><a href="https://github.com/eslint/eslint/commit/a3c868f6ef103c1caff9d15f744f9ebd995e872f"><code>a3c868f</code></a> fix: update dependency <code>@​eslint/eslintrc</code> to ^3.3.4 (<a href="https://redirect.github.com/eslint/eslint/issues/20554">#20554</a>)</li>
<li><a href="https://github.com/eslint/eslint/commit/234d005da6cd3c924f359e3783fbf565a3c047c3"><code>234d005</code></a> fix: minimatch security vulnerability patch for v9.x (<a href="https://redirect.github.com/eslint/eslint/issues/20549">#20549</a>)</li>
<li><a href="https://github.com/eslint/eslint/commit/b1b37eecaa033d2e390e1d8f1d6e68d0f5ff3a6a"><code>b1b37ee</code></a> fix: update <code>ajv</code> to <code>6.14.0</code> to address security vulnerabilities (<a href="https://redirect.github.com/eslint/eslint/issues/20538">#20538</a>)</li>
<li>See full diff in <a href="https://github.com/eslint/eslint/compare/v9.39.3...v9.39.4">compare view</a></li>
</ul>
</details>
<br />

**Stats:** +68 -74 (142 changes)

---

## 40f7e5c4 — 2026-04-29T03:38:22Z
**Author:** Chris@ZooClaw

**Message:**
```
chore(deps): ignore eslint-config-next major bumps in /web (#1420)

## Summary
- 给 \`eslint-config-next\` 加 major-bump ignore；关闭 #1417 (15.5.15 →
16.2.3)

## Why
\`eslint-config-next\` 跟 Next.js 主版本绑定（16.x ↔ Next 16）。我们在
dependabot.yml 已经 ignore Next major（停在 15.x），但 eslint-config-next
是单独的包，没被 ignore 联动。如果接受 16 而 next 仍是 15，lint 规则与 runtime 行为会 drift。

## Test plan
- [x] dependabot.yml 仅追加 ignore 块
- [ ] CI 绿后 merge → dependabot 自动 close #1417

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR #1420:** chore(deps): ignore eslint-config-next major bumps in /web

**PR Body:**
## Summary
- 给 \`eslint-config-next\` 加 major-bump ignore；关闭 #1417 (15.5.15 → 16.2.3)

## Why
\`eslint-config-next\` 跟 Next.js 主版本绑定（16.x ↔ Next 16）。我们在 dependabot.yml 已经 ignore Next major（停在 15.x），但 eslint-config-next 是单独的包，没被 ignore 联动。如果接受 16 而 next 仍是 15，lint 规则与 runtime 行为会 drift。

## Test plan
- [x] dependabot.yml 仅追加 ignore 块
- [ ] CI 绿后 merge → dependabot 自动 close #1417

🤖 Generated with [Claude Code](https://claude.com/claude-code)

**Stats:** +6 -0 (6 changes)

---

## 4f0a2a64 — 2026-04-29T03:15:05Z
**Author:** kaka-srp

**Message:**
```
feat(admin): customer events viewer (ECA-579) (#1451)

## Summary

Adds an "事件" button in the admin Users table that opens a modal listing
a user's recent LLM-usage events from bg / Lago, with a 4-chip range
preset (24h default / 7d / 30d / 自定义) and pagination. Three-tier
passthrough following the existing OrderHistoryModal pattern.

- **bg/Lago key correction**: `customer_id` in bg's URL is actually the
user's `team_id` (LAGO_API_CHARGE_BY=team_id), not the uid — the route
resolves `uid → team_id` via `user_repo.get_user(uid)` before calling
bg, mirroring `routes/credits.py:65`.
- **`per_page=50`**, default range is rolling 24h. Custom mode uses two
`<input type="date">` interpreted as UTC start-of-day / end-of-day.
- **No raw-JSON drawer** — table columns: Time / Code / Model / Prompt /
Completion / Total / Cost.
- **`billing_events.py` is a separate module** (not a method on
`BillingGatewayClient`) because that file is exactly at the 500-line cap
on main; the new module reuses the client's HTTP timeout + connect-retry
helper.

Linear:
[ECA-579](https://linear.app/srpone/issue/ECA-579/view-recent-customer-events-in-admin-user-page)
Spec:
[docs/superpowers/specs/2026-04-28-eca-579-admin-customer-events.md](docs/superpowers/specs/2026-04-28-eca-579-admin-customer-events.md)

## Test plan

- [x] Backend unit tests: `pytest tests/unit/test_billing_events.py
tests/unit/test_admin_events.py tests/unit/test_admin_route_wiring.py
tests/unit/test_billing_client.py` (74 passing)
- [x] Frontend unit tests: `vitest run tests/unit/app/admin/` (62
passing) + middleware tests (63 passing)
- [x] `tsc --noEmit` clean, `eslint --max-warnings=0` clean on touched
files
- [x] Live `curl` against staging bg confirmed the response shape used
in the design (Time/Model/Tokens/Cost columns)
- [ ] Manual verification post-deploy: log in as admin, search a user
with recent activity, click "事件", verify all 4 range chips return data,
verify pagination Prev/Next bounds
```

**PR #1451:** feat(admin): customer events viewer (ECA-579)

**PR Body:**
## Summary

Adds an "事件" button in the admin Users table that opens a modal listing a user's recent LLM-usage events from bg / Lago, with a 4-chip range preset (24h default / 7d / 30d / 自定义) and pagination. Three-tier passthrough following the existing OrderHistoryModal pattern.

- **bg/Lago key correction**: `customer_id` in bg's URL is actually the user's `team_id` (LAGO_API_CHARGE_BY=team_id), not the uid — the route resolves `uid → team_id` via `user_repo.get_user(uid)` before calling bg, mirroring `routes/credits.py:65`.
- **`per_page=50`**, default range is rolling 24h. Custom mode uses two `<input type="date">` interpreted as UTC start-of-day / end-of-day.
- **No raw-JSON drawer** — table columns: Time / Code / Model / Prompt / Completion / Total / Cost.
- **`billing_events.py` is a separate module** (not a method on `BillingGatewayClient`) because that file is exactly at the 500-line cap on main; the new module reuses the client's HTTP timeout + connect-retry helper.

Linear: [ECA-579](https://linear.app/srpone/issue/ECA-579/view-recent-customer-events-in-admin-user-page)
Spec: [docs/superpowers/specs/2026-04-28-eca-579-admin-customer-events.md](docs/superpowers/specs/2026-04-28-eca-579-admin-customer-events.md)

## Test plan

- [x] Backend unit tests: `pytest tests/unit/test_billing_events.py tests/unit/test_admin_events.py tests/unit/test_admin_route_wiring.py tests/unit/test_billing_client.py` (74 passing)
- [x] Frontend unit tests: `vitest run tests/unit/app/admin/` (62 passing) + middleware tests (63 passing)
- [x] `tsc --noEmit` clean, `eslint --max-warnings=0` clean on touched files
- [x] Live `curl` against staging bg confirmed the response shape used in the design (Time/Model/Tokens/Cost columns)
- [ ] Manual verification post-deploy: log in as admin, search a user with recent activity, click "事件", verify all 4 range chips return data, verify pagination Prev/Next bounds

🤖 Generated with [Claude Code](https://claude.com/claude-code)

**Stats:** +1578 -0 (1578 changes)

---

