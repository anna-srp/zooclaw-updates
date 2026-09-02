# SerendipityOneInc/ecap-workspace — commits 2026-09-01

## fix(billing): support historical airwallex price ids (#3611)

- **SHA**: `6992ea2da9ed5edd46a71fcbd7fcd47ab83cf20c`
- **作者**: tim-srp
- **日期**: 2026-09-01T12:49:39Z
- **PR**: #3611

### Commit Message

```
fix(billing): support historical airwallex price ids (#3611)

## Summary

- Accept known retired individual-subscription Airwallex Price IDs for
existing agreement upgrade, renewal, downgrade, and
cancellation-restoration flows.
- Keep new checkout creation on the currently configured Price IDs only.
- Continue rejecting unknown or semantically mismatched Price IDs.

## Scope

- Covers Starter, Pro, and Ultra individual subscription IDs, including
Starter trial IDs.
- Top-up and Vertical Pack use separate flows and are intentionally
outside this PR.

## Validation

- `python -m pytest tests/unit/test_airwallex_catalog.py
tests/unit/test_card_checkout_upgrade.py
tests/unit/test_airwallex_renewal.py
tests/unit/test_airwallex_subscription_plan_changes.py -q` (75 passed)
- `bash scripts/verify-py.sh`
- Pre-push changed-surface verification

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## Summary

- Accept known retired individual-subscription Airwallex Price IDs for existing agreement upgrade, renewal, downgrade, and cancellation-restoration flows.
- Keep new checkout creation on the currently configured Price IDs only.
- Continue rejecting unknown or semantically mismatched Price IDs.

## Scope

- Covers Starter, Pro, and Ultra individual subscription IDs, including Starter trial IDs.
- Top-up and Vertical Pack use separate flows and are intentionally outside this PR.

## Validation

- `python -m pytest tests/unit/test_airwallex_catalog.py tests/unit/test_card_checkout_upgrade.py tests/unit/test_airwallex_renewal.py tests/unit/test_airwallex_subscription_plan_changes.py -q` (75 passed)
- `bash scripts/verify-py.sh`
- Pre-push changed-surface verification


---

## fix(web): rename login branding to ZooWork (#3616)

- **SHA**: `1035f54ef0bb3302089b7fe3709284be56163624`
- **作者**: tim-srp
- **日期**: 2026-09-01T12:46:42Z
- **PR**: #3616

### Commit Message

```
fix(web): rename login branding to ZooWork (#3616)

## Summary

- Add regression coverage for the ZooWork login brand across every
supported theme.
- Cover the default login title, terms text, and all supported landing
locales.
- Correct legacy ZooClaw assertions in the login test suite without
changing authentication behavior or logo assets.

## Root cause

The visual login path had ZooWork branding in the current
implementation, but its tests retained ZooClaw expectations and did not
cover all themes or localized landing login text. That allowed old
branding to reappear without a focused regression signal.

## Test plan

- [x] `pnpm exec vitest run tests/unit/theme/brand-themes.unit.spec.ts
tests/unit/components/LoginForm.unit.spec.tsx
tests/unit/locales/login-branding.unit.spec.ts`
- [x] `bash scripts/verify-web.sh web/app/src/components/LoginForm.tsx
web/app/src/theme/brand-themes.ts
web/app/tests/unit/components/LoginForm.unit.spec.tsx
web/app/tests/unit/theme/brand-themes.unit.spec.ts
web/app/tests/unit/locales/login-branding.unit.spec.ts`
- [x] `bash scripts/verify-changed.sh`
```

### PR Body

## Summary

- Add regression coverage for the ZooWork login brand across every supported theme.
- Cover the default login title, terms text, and all supported landing locales.
- Correct legacy ZooClaw assertions in the login test suite without changing authentication behavior or logo assets.

## Root cause

The visual login path had ZooWork branding in the current implementation, but its tests retained ZooClaw expectations and did not cover all themes or localized landing login text. That allowed old branding to reappear without a focused regression signal.

## Test plan

- [x] `pnpm exec vitest run tests/unit/theme/brand-themes.unit.spec.ts tests/unit/components/LoginForm.unit.spec.tsx tests/unit/locales/login-branding.unit.spec.ts`
- [x] `bash scripts/verify-web.sh web/app/src/components/LoginForm.tsx web/app/src/theme/brand-themes.ts web/app/tests/unit/components/LoginForm.unit.spec.tsx web/app/tests/unit/theme/brand-themes.unit.spec.ts web/app/tests/unit/locales/login-branding.unit.spec.ts`
- [x] `bash scripts/verify-changed.sh`


---

## fix(billing): limit sidebar expiry warning (#3613)

- **SHA**: `374be8b587b7de364bd28a48fd585945bc80aa94`
- **作者**: tim-srp
- **日期**: 2026-09-01T11:30:13Z
- **PR**: #3613

### Commit Message

```
fix(billing): limit sidebar expiry warning (#3613)

## Summary

- Show the sidebar's red subscription-ending warning only when the
current period ends within 30 days.
- Preserve Billing-page ending and renewal behavior, while displaying
four-digit years for ending dates.
- Add regression coverage for the 30-day boundary and cross-year date
labels.

## Test Plan

- [x] `pnpm exec vitest run
tests/unit/components/billing/subscription-expiry.unit.spec.ts
tests/unit/components/UserCard.unit.spec.tsx
tests/unit/components/billing/SharedPlanCard.unit.spec.tsx --config
./vitest.config.mts`
- [x] `bash scripts/verify-changed.sh`
- [ ] Full `pnpm test` remains blocked by unrelated
`mock-backend-agent-builder` jsdom navigation failures.
```

### PR Body

## Summary

- Show the sidebar's red subscription-ending warning only when the current period ends within 30 days.
- Preserve Billing-page ending and renewal behavior, while displaying four-digit years for ending dates.
- Add regression coverage for the 30-day boundary and cross-year date labels.

## Test Plan

- [x] `pnpm exec vitest run tests/unit/components/billing/subscription-expiry.unit.spec.ts tests/unit/components/UserCard.unit.spec.tsx tests/unit/components/billing/SharedPlanCard.unit.spec.tsx --config ./vitest.config.mts`
- [x] `bash scripts/verify-changed.sh`
- [ ] Full `pnpm test` remains blocked by unrelated `mock-backend-agent-builder` jsdom navigation failures.


---

## fix(chat): preserve avatar when tool steps are hidden (#3615)

- **SHA**: `31d495c6cf1380a11570f0a2320f5f4612978d25`
- **作者**: sam-srp
- **日期**: 2026-09-01T11:15:33Z
- **PR**: #3615

### Commit Message

```
fix(chat): preserve avatar when tool steps are hidden (#3615)

## Summary
- compute assistant message grouping for both visible and hidden
tool-step modes
- preserve the avatar on the first visible assistant response when tool
steps are hidden
- keep later messages in the same run consecutive to avoid duplicate
avatars

## Root cause
Hidden tool-group messages still consumed the run identity before the
renderer returned `null`, so the first visible text response was
incorrectly marked consecutive and rendered an empty avatar spacer.

## Verification
- `pnpm --filter @zooclaw/web-app exec vitest run --config
./vitest.config.mts tests/unit/chat/useOpenClawRuntime.unit.spec.ts`
- targeted ESLint checks
- `pnpm --filter @zooclaw/web-app exec tsc --noEmit`
```

### PR Body

## Summary
- compute assistant message grouping for both visible and hidden tool-step modes
- preserve the avatar on the first visible assistant response when tool steps are hidden
- keep later messages in the same run consecutive to avoid duplicate avatars

## Root cause
Hidden tool-group messages still consumed the run identity before the renderer returned `null`, so the first visible text response was incorrectly marked consecutive and rendered an empty avatar spacer.

## Verification
- `pnpm --filter @zooclaw/web-app exec vitest run --config ./vitest.config.mts tests/unit/chat/useOpenClawRuntime.unit.spec.ts`
- targeted ESLint checks
- `pnpm --filter @zooclaw/web-app exec tsc --noEmit`

---

## feat(ios): refresh ZooWork onboarding branding (#3614)

- **SHA**: `2aced668de6254de8c22647f124db1aef6227dfe`
- **作者**: shana-srp
- **日期**: 2026-09-01T11:06:57Z
- **PR**: #3614

### Commit Message

```
feat(ios): refresh ZooWork onboarding branding (#3614)

## Summary

- replace the sidebar, launch, and onboarding logos with the supplied
ZooWork artwork
- refresh the welcome hero background, copy, typography, spacing, and
button radius to match the approved preview
- update onboarding notification examples from ZooClaw to ZooWork

## Testing

- `env DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer
xcodebuild -project ios/ZooClaw/ZooClaw.xcodeproj -scheme ZooClaw
-configuration Debug -destination 'platform=iOS
Simulator,id=C0CBC067-D5B6-43EC-A85A-8F6542210C2E' -derivedDataPath
.build/ios-logo-update build`
- manually previewed the signed build in the iOS 26.5 simulator while
preserving the existing authenticated session

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary

- replace the sidebar, launch, and onboarding logos with the supplied ZooWork artwork
- refresh the welcome hero background, copy, typography, spacing, and button radius to match the approved preview
- update onboarding notification examples from ZooClaw to ZooWork

## Testing

- `env DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer xcodebuild -project ios/ZooClaw/ZooClaw.xcodeproj -scheme ZooClaw -configuration Debug -destination 'platform=iOS Simulator,id=C0CBC067-D5B6-43EC-A85A-8F6542210C2E' -derivedDataPath .build/ios-logo-update build`
- manually previewed the signed build in the iOS 26.5 simulator while preserving the existing authenticated session


---

## feat(agents): install explicit pack onboarding (#3610)

- **SHA**: `6bbae276e4f0b4aa59ea325d8e71494abc6fc414`
- **作者**: kaka-srp
- **日期**: 2026-09-01T09:34:04Z
- **PR**: #3610

### Commit Message

```
feat(agents): install explicit pack onboarding (#3610)

## Summary

Install Pack onboarding as an explicit Engine skill selection instead of
relying on Engine's generic onboarding.

## Why

The Pack should own its onboarding playbook. Engine now defaults to no
onboarding and only runs the exact skill selected by the Agent creator.

## Changes

- Parse and validate `onboarding.skill` from Pack manifests.
- Snapshot the onboarding selection and resolution state with the
installed Pack.
- Register the exact bundled skill in Engine and create the Agent with
`onboarding: { skill_id }`.
- Keep Agents without a declared Pack onboarding explicitly skipped.
- Make Pack Test provision a fresh Engine Agent whenever onboarding is
explicit or legacy/unknown, avoiding reuse of an already-completed
one-shot onboarding state.
- Add the cross-repository design contract and focused tests.

## Testing

- `bash scripts/verify-py.sh` passed (ruff, format, pyright,
import-linter).
- 360 focused affected-surface tests passed during implementation.
- 212 focused tests passed after the service refactor.
- Pre-commit and pre-push quality/size gates passed.

## Risk & Rollback

Deploy after the companion Engine PR and before updated Pack assets.
Existing snapshots remain readable; legacy/unknown Pack Test runs fail
safe by provisioning a fresh Agent. Roll back the ECAP backend if Agent
creation rejects the new field.

## Release notes

Pack-defined onboarding now runs as the only onboarding playbook; Agents
without an onboarding declaration start normally without an Engine
identity wizard.

## Related

Design:
`docs/superpowers/specs/2026-09-01-explicit-agent-onboarding-contract.md`

Companion PRs:

+- Engine: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1071
- ECAP: https://github.com/SerendipityOneInc/ecap-workspace/pull/3610
- Pack: https://github.com/SerendipityOneInc/ecap-agent-pack/pull/253
```

### PR Body

## Summary

Install Pack onboarding as an explicit Engine skill selection instead of relying on Engine's generic onboarding.

## Why

The Pack should own its onboarding playbook. Engine now defaults to no onboarding and only runs the exact skill selected by the Agent creator.

## Changes

- Parse and validate `onboarding.skill` from Pack manifests.
- Snapshot the onboarding selection and resolution state with the installed Pack.
- Register the exact bundled skill in Engine and create the Agent with `onboarding: { skill_id }`.
- Keep Agents without a declared Pack onboarding explicitly skipped.
- Make Pack Test provision a fresh Engine Agent whenever onboarding is explicit or legacy/unknown, avoiding reuse of an already-completed one-shot onboarding state.
- Add the cross-repository design contract and focused tests.

## Testing

- `bash scripts/verify-py.sh` passed (ruff, format, pyright, import-linter).
- 360 focused affected-surface tests passed during implementation.
- 212 focused tests passed after the service refactor.
- Pre-commit and pre-push quality/size gates passed.

## Risk & Rollback

Deploy after the companion Engine PR and before updated Pack assets. Existing snapshots remain readable; legacy/unknown Pack Test runs fail safe by provisioning a fresh Agent. Roll back the ECAP backend if Agent creation rejects the new field.

## Release notes

Pack-defined onboarding now runs as the only onboarding playbook; Agents without an onboarding declaration start normally without an Engine identity wizard.

## Related

Design: `docs/superpowers/specs/2026-09-01-explicit-agent-onboarding-contract.md`

Companion PRs:

+- Engine: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1071
- ECAP: https://github.com/SerendipityOneInc/ecap-workspace/pull/3610
- Pack: https://github.com/SerendipityOneInc/ecap-agent-pack/pull/253


---

## fix(billing): add stable gemini-3.1-flash-image to image degradation mapping (#3601)

- **SHA**: `90d9bbb6609eac5b843dc35362cde9a6fb8f5a3f`
- **作者**: sharplee-srp
- **日期**: 2026-09-01T09:25:11Z
- **PR**: #3601

### Commit Message

```
fix(billing): add stable gemini-3.1-flash-image to image degradation mapping (#3601)

## Summary
- Add the stable `gemini-3.1-flash-image` alias to
`MODEL_DEGRADATION_MAPPINGS` (→ `hunyuan-image-3`), alongside the
existing `-preview` entry.
- Pin it in `test_tier_writer.py`'s image-model degradation check.

## Root cause
zooclaw-engine PR
[#999](https://github.com/SerendipityOneInc/zooclaw-engine/pull/999)
changes the v2 managed image-generation default to `gpt-image-2` →
`gemini-3.1-flash-image` (stable Vertex alias; already registered on
staging LiteLLM with `starter/pro/ultra-image_generation` access
groups). The degradation table only knew the preview alias, so a
credits-depleted user whose image call fell through to the stable model
would have no degradation route.

## Test plan
- [x] `ruff check` / `ruff format --check` on the two files
- [x] `pytest tests/unit/test_tier_writer.py
tests/unit/test_plan_models.py` — 50 passed

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01KK2cYPdkCp1Uxnzb2konn8

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## Summary
- Add the stable `gemini-3.1-flash-image` alias to `MODEL_DEGRADATION_MAPPINGS` (→ `hunyuan-image-3`), alongside the existing `-preview` entry.
- Pin it in `test_tier_writer.py`'s image-model degradation check.

## Root cause
zooclaw-engine PR [#999](https://github.com/SerendipityOneInc/zooclaw-engine/pull/999) changes the v2 managed image-generation default to `gpt-image-2` → `gemini-3.1-flash-image` (stable Vertex alias; already registered on staging LiteLLM with `starter/pro/ultra-image_generation` access groups). The degradation table only knew the preview alias, so a credits-depleted user whose image call fell through to the stable model would have no degradation route.

## Test plan
- [x] `ruff check` / `ruff format --check` on the two files
- [x] `pytest tests/unit/test_tier_writer.py tests/unit/test_plan_models.py` — 50 passed

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01KK2cYPdkCp1Uxnzb2konn8


---

## fix(web): 修复深色主题刷新后丢失 (#3596)

- **SHA**: `b3da84fb05cd61a13993a35c3a5864072cec2bb1`
- **作者**: lynn Zhuang
- **日期**: 2026-09-01T09:21:51Z
- **PR**: #3596

### Commit Message

```
fix(web): 修复深色主题刷新后丢失 (#3596)

## Summary
- 在认证存储清理时保留用户显式选择的 `light`、`dark`、`system` 主题模式
- 增加 `clearUserStorage()` 的主题持久化契约测试，同时保持用户数据隔离与现有清理范围
- 补强 Dark mode E2E，覆盖 Settings → General → Dark → Chat → 强制刷新，并在系统 Light
模式下同时断言存储值和 `html.dark`
- 保留 marketing 页面强制 Light、但不覆盖已保存主题偏好的现有契约

## Root cause
`next-themes` 使用 localStorage 键 `ecap-theme` 持久化主题模式，但认证流程的
`clearUserStorage()` 只保留设备 ID 和品牌主题键。登录清理、身份恢复或无效身份处理调用该函数时，会误删
`ecap-theme`。页面强制刷新后 `next-themes` 因找不到保存值而回退到 `system`，在系统配色为 Light
时表现为用户选择的 Dark 丢失。

本修复仅将非敏感的主题模式偏好加入固定 allowlist；sessionStorage、React Query、Zustand
以及其他用户范围数据的清理逻辑保持不变。

## Test plan
- [x] TDD 红灯验证：新增的 light/dark/system 三个契约测试在修复前全部失败
- [x] 聚焦 Vitest：108/108 通过
- [x] `bash scripts/verify-web.sh`：guards、完整 TypeScript、130 个匹配测试和
ESLint 通过
- [x] `bash scripts/verify-changed.sh` 通过
- [x] 本地 `ready-user` mock stack + Chromium E2E：认证 setup 与主题持久化场景共 2
个测试通过
- [x] E2E 将系统 `colorScheme` 固定为 Light，并断言 `localStorage['ecap-theme']
=== 'dark'` 与 `html.dark`
- [ ] 部署到 Staging 后执行最终冒烟验证
```

### PR Body

## Summary
- 在认证存储清理时保留用户显式选择的 `light`、`dark`、`system` 主题模式
- 增加 `clearUserStorage()` 的主题持久化契约测试，同时保持用户数据隔离与现有清理范围
- 补强 Dark mode E2E，覆盖 Settings → General → Dark → Chat → 强制刷新，并在系统 Light 模式下同时断言存储值和 `html.dark`
- 保留 marketing 页面强制 Light、但不覆盖已保存主题偏好的现有契约

## Root cause
`next-themes` 使用 localStorage 键 `ecap-theme` 持久化主题模式，但认证流程的 `clearUserStorage()` 只保留设备 ID 和品牌主题键。登录清理、身份恢复或无效身份处理调用该函数时，会误删 `ecap-theme`。页面强制刷新后 `next-themes` 因找不到保存值而回退到 `system`，在系统配色为 Light 时表现为用户选择的 Dark 丢失。

本修复仅将非敏感的主题模式偏好加入固定 allowlist；sessionStorage、React Query、Zustand 以及其他用户范围数据的清理逻辑保持不变。

## Test plan
- [x] TDD 红灯验证：新增的 light/dark/system 三个契约测试在修复前全部失败
- [x] 聚焦 Vitest：108/108 通过
- [x] `bash scripts/verify-web.sh`：guards、完整 TypeScript、130 个匹配测试和 ESLint 通过
- [x] `bash scripts/verify-changed.sh` 通过
- [x] 本地 `ready-user` mock stack + Chromium E2E：认证 setup 与主题持久化场景共 2 个测试通过
- [x] E2E 将系统 `colorScheme` 固定为 Light，并断言 `localStorage['ecap-theme'] === 'dark'` 与 `html.dark`
- [ ] 部署到 Staging 后执行最终冒烟验证


---

## fix(brand): complete ZooWork user-facing rebrand (#3609)

- **SHA**: `064f4800f2698db905cd1f1f4473e7f18a8f8e12`
- **作者**: shana-srp
- **日期**: 2026-09-01T08:41:56Z
- **PR**: #3609

### Commit Message

```
fix(brand): complete ZooWork user-facing rebrand (#3609)

## Summary
- Center the homepage hero content as a cohesive desktop group and keep
rotating agent roles centered by rendered width
- Keep every localized rotating role mobile-wrappable, including the
longest Spanish and Italian variants
- Replace all remaining user-visible ZooClaw / Claw product wording with
ZooWork across the main app, enterprise admin, and dashboard console
- Update all 10 locale dictionaries, page metadata, SEO/share metadata,
manifest copy, static guide text, image alt text, and displayed wordmark
assets
- Make `/identity` the canonical Identity page URL and permanently
redirect the legacy `/claw-settings` path while preserving query
parameters
- Preserve internal package names, APIs, identifiers, compatibility
routes, OpenClaw terminology, domains, and support email addresses

## Test plan
- [x] `bash scripts/verify-web.sh` — TypeScript, full Vitest suite
(9,411 passed), and ESLint
- [x] `bash scripts/verify-web.sh --no-test` after final formatting pass
- [x] `pnpm --dir web/enterprise-admin test` — 421 passed
- [x] `pnpm --dir web/enterprise-admin lint`
- [x] `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- [x] `pnpm --dir web/dashboard-console test` — 651 passed
- [x] `pnpm --dir web/dashboard-console lint`
- [x] `pnpm --dir web/dashboard-console exec react-router typegen`
- [x] `pnpm --dir web/dashboard-console exec tsc -b --pretty false`
- [x] AST residual scan across production source roots; only the
intentionally preserved `ZooClaw.ai` legal-domain references remain
- [x] Added regression coverage that rejects capitalized legacy product
wording in every supported locale dictionary

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary
- Center the homepage hero content as a cohesive desktop group and keep rotating agent roles centered by rendered width
- Keep every localized rotating role mobile-wrappable, including the longest Spanish and Italian variants
- Replace all remaining user-visible ZooClaw / Claw product wording with ZooWork across the main app, enterprise admin, and dashboard console
- Update all 10 locale dictionaries, page metadata, SEO/share metadata, manifest copy, static guide text, image alt text, and displayed wordmark assets
- Make `/identity` the canonical Identity page URL and permanently redirect the legacy `/claw-settings` path while preserving query parameters
- Preserve internal package names, APIs, identifiers, compatibility routes, OpenClaw terminology, domains, and support email addresses

## Test plan
- [x] `bash scripts/verify-web.sh` — TypeScript, full Vitest suite (9,411 passed), and ESLint
- [x] `bash scripts/verify-web.sh --no-test` after final formatting pass
- [x] `pnpm --dir web/enterprise-admin test` — 421 passed
- [x] `pnpm --dir web/enterprise-admin lint`
- [x] `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- [x] `pnpm --dir web/dashboard-console test` — 651 passed
- [x] `pnpm --dir web/dashboard-console lint`
- [x] `pnpm --dir web/dashboard-console exec react-router typegen`
- [x] `pnpm --dir web/dashboard-console exec tsc -b --pretty false`
- [x] AST residual scan across production source roots; only the intentionally preserved `ZooClaw.ai` legal-domain references remain
- [x] Added regression coverage that rejects capitalized legacy product wording in every supported locale dictionary


---

## docs(agent): define Pack-owned onboarding contract (#3603)

- **SHA**: `b7326d0435c082e23e9fdd30fd554efa9e9ec404`
- **作者**: kaka-srp
- **日期**: 2026-09-01T03:17:03Z
- **PR**: #3603

### Commit Message

```
docs(agent): define Pack-owned onboarding contract (#3603)

## Summary

- Define the cross-repository contract that makes a Pack-owned
`pack-onboarding` skill the only first-run playbook.
- Specify exact-name plus Pack-scope selection, Engine-authoritative
lifecycle state, fail-closed behavior, and the rollout order.
- Require pending-Agent rendered-config backfill/audit before Engine
cutover, with rollback remediation for any legacy pinned skill.
- Require Engine to block same-message sibling tools after successful
lifecycle completion.
- Record the Agent Studio validation and regression matrix required by
the implementation PRs.

## Test plan

- [x] `git diff origin/main...HEAD --check`
- [x] Contract reviewed against the Agent Pack and Engine
implementations

## Rollout

The Agent Pack changes must be published first. Every affected pending
Agent must then receive and pass an audit of its pinned rendered config
before the Engine behavior is deployed; registry publication alone is
not sufficient.

- Agent Pack implementation:
https://github.com/SerendipityOneInc/ecap-agent-pack/pull/252
- Engine implementation:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1064
```

### PR Body

## Summary

- Define the cross-repository contract that makes a Pack-owned `pack-onboarding` skill the only first-run playbook.
- Specify exact-name plus Pack-scope selection, Engine-authoritative lifecycle state, fail-closed behavior, and the rollout order.
- Require pending-Agent rendered-config backfill/audit before Engine cutover, with rollback remediation for any legacy pinned skill.
- Require Engine to block same-message sibling tools after successful lifecycle completion.
- Record the Agent Studio validation and regression matrix required by the implementation PRs.

## Test plan

- [x] `git diff origin/main...HEAD --check`
- [x] Contract reviewed against the Agent Pack and Engine implementations

## Rollout

The Agent Pack changes must be published first. Every affected pending Agent must then receive and pass an audit of its pinned rendered config before the Engine behavior is deployed; registry publication alone is not sufficient.

- Agent Pack implementation: https://github.com/SerendipityOneInc/ecap-agent-pack/pull/252
- Engine implementation: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1064


---

## fix(agent-builder): remove legacy cron key (#3604)

- **SHA**: `40d0c9b6b8767e6e6a2c63923d74526533288865`
- **作者**: kaka-srp
- **日期**: 2026-09-01T03:08:47Z
- **PR**: #3604

### Commit Message

```
fix(agent-builder): remove legacy cron key (#3604)

## Summary

- Remove the legacy warm-pool service-key dependency from the Agent
Builder runtime cleanup cron endpoint.
- Keep the endpoint behind the existing `/admin/cron` deployment access
boundary.
- Add HTTP and direct-call regression coverage for the key-free trigger
contract.

## Root cause

The new Builder cleanup endpoint copied authentication from older
warm-pool-related cron routes even though Builder runtime cleanup does
not use warm-pool resources. This unnecessarily required Scheduler
operators to configure `X-Warm-Pool-Key`.

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] Targeted cron endpoint tests (2 passed)
- [x] Pre-commit and pre-push changed-surface checks
```

### PR Body

## Summary

- Remove the legacy warm-pool service-key dependency from the Agent Builder runtime cleanup cron endpoint.
- Keep the endpoint behind the existing `/admin/cron` deployment access boundary.
- Add HTTP and direct-call regression coverage for the key-free trigger contract.

## Root cause

The new Builder cleanup endpoint copied authentication from older warm-pool-related cron routes even though Builder runtime cleanup does not use warm-pool resources. This unnecessarily required Scheduler operators to configure `X-Warm-Pool-Key`.

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] Targeted cron endpoint tests (2 passed)
- [x] Pre-commit and pre-push changed-surface checks


---

## refactor(agent-builder): simplify runtime resource lifecycle (#3602)

- **SHA**: `1e7750d26ccfd484d7246f637afb9d4a63dc8979`
- **作者**: kaka-srp
- **日期**: 2026-09-01T02:41:16Z
- **PR**: #3602

### Commit Message

```
refactor(agent-builder): simplify runtime resource lifecycle (#3602)

## Summary

- Replace the fixed Agent Builder Project slot/capacity state machine
with a Project-owned lifecycle: no Project quota, 24-hour idle ingress
cleanup, and Archive-only deep runtime cleanup.
- Idle cleanup disables ACS Channels and removes the dedicated Builder
bot from the Mattermost team; the next real Builder action restores
route, membership, and Channels idempotently.
- Archive immediately deep-cleans the dedicated Workspace, Engine Agent
runtime/Sandbox, ACS Channels, and Mattermost membership. Failed
external steps retain Project identity for hourly retry.
- Serialize Archive with every Builder post (ordinary message, `/stop`,
Test feedback, and Preflight feedback) through one short renewable
Project lease. Archive cannot retire resources during an accepted-post
window, while `/stop` remains available against the exact current
runtime even when a newer Builder release exists.
- Keep claim release best-effort so a Mongo release failure cannot turn
an already accepted post or persisted Archive into a client-visible
failure; the two-minute lease TTL remains the fallback.
- Restrict cleanup adoption to `engine_v2` Projects with the exact
`dedicated_project_agent` layout. Historical shared-Agent rows and old
archived rows that were not written by this lifecycle are excluded.
- Keep partially initialized runtimes cleanup-visible even when session
creation fails or the setup lease is lost, using a narrow identity CAS
that cannot overwrite a newer setup owner.
- Reuse the existing Engine cleanup contract (`status=cleaned`, matching
Agent identity, and `sandbox_released=true`); no Engine change or
rolling compatibility branch is required.
- Add an externally triggered hourly cleanup endpoint and remove the old
in-process slot reconciler.

This supersedes #3577. The diff exceeds the normal size budget because
it removes the old slot/capacity implementation and tests while adding
the smaller lifecycle. The changed-line total is dominated by 4,343
deletions; splitting deletion and replacement would leave an unsafe
intermediate release, so this PR carries `size-override`.

## Deployment

1. Deploy this ECAP PR.
2. Configure Cloud Scheduler to call `POST
/admin/cron/cleanup-agent-builder-runtime` hourly with
`X-Warm-Pool-Key`.

## Validation

- [x] `bash scripts/verify-changed.sh`: Ruff, format, Pyright, and all 8
import-linter contracts passed after merging current `main`.
- [x] 359 Agent Builder lifecycle, service, route, feedback, recovery,
Mattermost, and turn tests passed on the final change.
- [x] Independent review agent completed design,
concurrency/failure-window, scope, and regression passes. All reported
P2/P3 findings were fixed; final verdict is PASS with no remaining
actionable findings.
- [x] The setup/Archive race false positive was traced through both
service and repo CAS layers; an explicit regression test now proves the
losing setup write returns the latest archived snapshot.
- [x] Local real Archive test confirmed Project identity, Workspace,
Engine Agent/Sandbox, ACS Channel, and Mattermost membership cleanup.
- [x] Local real idle task processed all 31 eligible dedicated Projects
successfully; final idle and archived-retry candidate counts were both
zero, and sampled Agents/Workspaces remained intact while ACS/Mattermost
ingress was released.
- [x] Latest PR merge-ref CI passed 38/38 checks, including backend
tests, lint/typecheck, duplication, CodeQL, and both automated reviews.
- [ ] After deployment, configure and smoke-test the external hourly
scheduler.
```

### PR Body

## Summary

- Replace the fixed Agent Builder Project slot/capacity state machine with a Project-owned lifecycle: no Project quota, 24-hour idle ingress cleanup, and Archive-only deep runtime cleanup.
- Idle cleanup disables ACS Channels and removes the dedicated Builder bot from the Mattermost team; the next real Builder action restores route, membership, and Channels idempotently.
- Archive immediately deep-cleans the dedicated Workspace, Engine Agent runtime/Sandbox, ACS Channels, and Mattermost membership. Failed external steps retain Project identity for hourly retry.
- Serialize Archive with every Builder post (ordinary message, `/stop`, Test feedback, and Preflight feedback) through one short renewable Project lease. Archive cannot retire resources during an accepted-post window, while `/stop` remains available against the exact current runtime even when a newer Builder release exists.
- Keep claim release best-effort so a Mongo release failure cannot turn an already accepted post or persisted Archive into a client-visible failure; the two-minute lease TTL remains the fallback.
- Restrict cleanup adoption to `engine_v2` Projects with the exact `dedicated_project_agent` layout. Historical shared-Agent rows and old archived rows that were not written by this lifecycle are excluded.
- Keep partially initialized runtimes cleanup-visible even when session creation fails or the setup lease is lost, using a narrow identity CAS that cannot overwrite a newer setup owner.
- Reuse the existing Engine cleanup contract (`status=cleaned`, matching Agent identity, and `sandbox_released=true`); no Engine change or rolling compatibility branch is required.
- Add an externally triggered hourly cleanup endpoint and remove the old in-process slot reconciler.

This supersedes #3577. The diff exceeds the normal size budget because it removes the old slot/capacity implementation and tests while adding the smaller lifecycle. The changed-line total is dominated by 4,343 deletions; splitting deletion and replacement would leave an unsafe intermediate release, so this PR carries `size-override`.

## Deployment

1. Deploy this ECAP PR.
2. Configure Cloud Scheduler to call `POST /admin/cron/cleanup-agent-builder-runtime` hourly with `X-Warm-Pool-Key`.

## Validation

- [x] `bash scripts/verify-changed.sh`: Ruff, format, Pyright, and all 8 import-linter contracts passed after merging current `main`.
- [x] 359 Agent Builder lifecycle, service, route, feedback, recovery, Mattermost, and turn tests passed on the final change.
- [x] Independent review agent completed design, concurrency/failure-window, scope, and regression passes. All reported P2/P3 findings were fixed; final verdict is PASS with no remaining actionable findings.
- [x] The setup/Archive race false positive was traced through both service and repo CAS layers; an explicit regression test now proves the losing setup write returns the latest archived snapshot.
- [x] Local real Archive test confirmed Project identity, Workspace, Engine Agent/Sandbox, ACS Channel, and Mattermost membership cleanup.
- [x] Local real idle task processed all 31 eligible dedicated Projects successfully; final idle and archived-retry candidate counts were both zero, and sampled Agents/Workspaces remained intact while ACS/Mattermost ingress was released.
- [x] Latest PR merge-ref CI passed 38/38 checks, including backend tests, lint/typecheck, duplication, CodeQL, and both automated reviews.
- [ ] After deployment, configure and smoke-test the external hourly scheduler.


---
