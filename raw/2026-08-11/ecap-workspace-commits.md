# SerendipityOneInc/ecap-workspace commits 2026-08-11

## fix(chat): add Auto to composer model picker (#3307)

- sha: `94e746b42104cb16d9122420f6f4c3a08e4ca344`
- 作者: siqiao-srp
- 日期: 2026-08-11T11:50:45Z
- PR: 3307


### 完整 commit message

```
fix(chat): add Auto to composer model picker (#3307)

## Summary

- add `Auto` as the first option in the active composer model dropdown
for supported computer workspaces
- treat Auto as an Agent-scoped virtual model through
`agentModes.<agentId>`, not a bot-global routing toggle
- preserve each Agent's concrete model and route only its delegated
native subagent spawns
- keep session `/auto` and `/auto off` as narrower overrides
- use atomic Agent + router configuration writes and per-key deep merge
so concurrent edits to different Agents do not clobber each other

## Runtime contract

Companion model-router PR:
https://github.com/SerendipityOneInc/zooclaw-extras/pull/214

Selection precedence is session override, then Agent mode, then routing
off. The router evaluates every `sessions_spawn` independently. OpenClaw
persists the selected concrete model on the child session. Explicit
spawn models are preserved, and media-bearing spawns fail open unless
the candidate declares all required input modalities.

## Verification

- [x] focused web verification: TypeScript, ESLint, 123 tests
- [x] focused backend model/router tests: 33 passed
- [x] related Agent and OpenClaw settings suites: 332 passed
- [x] full backend Pyright with a clean Python 3.12 environment: 0
errors
- [x] Ruff and import contracts
- [x] companion router tests: 189 passed, typecheck, lint, pre-push
suite

The first local ECAP push attempt used the conda interpreter selected by
`verify-py.sh`; that interpreter could not resolve the worktree
environment. The same full Pyright command passed with the clean Python
3.12 environment used for the backend tests.
```


### PR body

## Summary

- add `Auto` as the first option in the active composer model dropdown for supported computer workspaces
- treat Auto as an Agent-scoped virtual model through `agentModes.<agentId>`, not a bot-global routing toggle
- preserve each Agent's concrete model and route only its delegated native subagent spawns
- keep session `/auto` and `/auto off` as narrower overrides
- use atomic Agent + router configuration writes and per-key deep merge so concurrent edits to different Agents do not clobber each other

## Runtime contract

Companion model-router PR: https://github.com/SerendipityOneInc/zooclaw-extras/pull/214

Selection precedence is session override, then Agent mode, then routing off. The router evaluates every `sessions_spawn` independently. OpenClaw persists the selected concrete model on the child session. Explicit spawn models are preserved, and media-bearing spawns fail open unless the candidate declares all required input modalities.

## Verification

- [x] focused web verification: TypeScript, ESLint, 123 tests
- [x] focused backend model/router tests: 33 passed
- [x] related Agent and OpenClaw settings suites: 332 passed
- [x] full backend Pyright with a clean Python 3.12 environment: 0 errors
- [x] Ruff and import contracts
- [x] companion router tests: 189 passed, typecheck, lint, pre-push suite

The first local ECAP push attempt used the conda interpreter selected by `verify-py.sh`; that interpreter could not resolve the worktree environment. The same full Pyright command passed with the clean Python 3.12 environment used for the backend tests.



### 变更文件

- architecture.md
- architecture.zh-CN.md
- docs/superpowers/specs/2026-08-09-auto-model-composer-dropdown.md
- services/claw-interface/AGENTS.md
- services/claw-interface/app/routes/computer/agents.py
- services/claw-interface/app/routes/openclaw_settings/core.py
- services/claw-interface/app/routes/openclaw_settings/multi_agent.py
- services/claw-interface/app/schema/agent_model.py
- services/claw-interface/app/services/agents/agent_model_service.py
- services/claw-interface/app/services/openclaw/agent_settings_service.py
- services/claw-interface/app/services/openclaw/agent_settings_types.py
- services/claw-interface/app/services/openclaw/bot_config_payload.py
- services/claw-interface/app/services/openclaw/model_router_capability.py
- services/claw-interface/app/services/openclaw/model_routing.py
- services/claw-interface/app/services/plan_models.py
- services/claw-interface/app/settings.py
- services/claw-interface/tests/unit/test_agent_model_service.py
- services/claw-interface/tests/unit/test_agent_routes.py
- services/claw-interface/tests/unit/test_agent_settings_effective_model.py
- services/claw-interface/tests/unit/test_bot_config_payload_routing_mode.py
- services/claw-interface/tests/unit/test_model_catalog.py
- services/claw-interface/tests/unit/test_model_router_capability.py
- services/claw-interface/tests/unit/test_openclaw_settings_routes.py
- web/app/AGENTS.md
- web/app/src/app/[locale]/(app)/claw-settings/components/BotModelSection.tsx
- web/app/src/components/chat/unified-chat-composer/composer-model-presentations.ts
- web/app/src/components/chat/unified-chat-composer/types.ts
- web/app/src/components/chat/unified-chat-composer/useComposerModelState.ts
- web/app/src/hooks/queries/models/useAgentModelQuery.ts
- web/app/src/hooks/queries/openclaw/useAgentSettingsQuery.ts
- web/app/src/models/agent-model.ts
- web/app/tests/unit/components/chat/composer-model-presentations.unit.spec.ts
- web/app/tests/unit/hooks/queries/openclaw/useAgentSettingsQuery.unit.spec.ts
- web/app/tests/unit/hooks/useAgentSettings.unit.spec.ts

---

## feat(agent-builder): isolate v2 project runtimes (#3326)

- sha: `85a304fdfcdbd766cb40ae9ca71ca6aceb1d0acd`
- 作者: kaka-srp
- 日期: 2026-08-11T11:35:38Z
- PR: 3326


### 完整 commit message

```
feat(agent-builder): isolate v2 project runtimes (#3326)

## Summary

- give every Agent Builder v2 Project its own hidden Engine Agent while
keeping Sandbox allocation lazy
- enforce at most three active/cooldown Project runtimes per uid and org
with fixed Mongo slots and fenced writes
- make Project open/read paths mutation-free and remove the v2 page
lease, activate route, shared-root materialization, and migration
machinery
- keep chat ordering and active-run ownership in Engine/ACS/Mattermost;
ECAP only delivers messages and accounts for Project capacity
- remove the redundant AuthoringTurn collection, Project current-turn
field, stop-dispatch latch, and chat recovery state machine
- preserve the Test Agent model selector/control-plane flow delivered by
the dependent Pack change

## Scope

- v2 only; v1 behavior is unchanged
- no data migration because v2 has not launched
- no browser-tab lock, cross-tab scheduler, or requirement for the
current Project to reach a terminal state before another Project can run
- same Project opened in multiple pages is supported; page open itself
does not claim capacity or start a Sandbox
- same-Project next turns supersede only the capacity fence and are
never rejected by an ECAP chat lock

## Engine / ACS contract fixes

- call Engine start on every v2 message, even when desired state is
already running, so the ACS route is reloaded
- treat terminal Engine assistant segments (`terminal=true`, phase
`final|error`) as the real completion signal
- finish exact turn capacity after a confirmed `/stop`, because ACS
`chat.aborted` does not emit a terminal assistant segment
- leave failed or unconfirmed stop dispatches unlatching and immediately
retryable

## Dependency

Depends on SerendipityOneInc/ecap-agent-pack#236:
https://github.com/SerendipityOneInc/ecap-agent-pack/pull/236

## Verification

- 514 Agent Builder, runtime, Engine install/lifecycle, lifetime, and
scheduler backend tests passed
- 51 final turn/slot/recovery focused regression tests passed after the
last audit fix
- 450 focused Agent Builder frontend tests passed
- Ruff, formatting, Pyright, import-linter, complexity, file-length,
collection-name, repo-sync, dead-code, and database-return checks passed
- TypeScript and ESLint passed
- `verify-changed` passed for backend and frontend
- `git diff --check` passed; unrelated local `settings.py` edits were
excluded from the commit

## Review note

This PR exceeds the mechanical size budget primarily because it removes
the obsolete lease/migration implementation and its tests. It has the
approved `size-override` label. The final simplification commit removes
more code than it adds and leaves one capacity state machine instead of
separate Project, AuthoringTurn, slot, stop-dispatch, and recovery
state.
```


### PR body

## Summary

- give every Agent Builder v2 Project its own hidden Engine Agent while keeping Sandbox allocation lazy
- enforce at most three active/cooldown Project runtimes per uid and org with fixed Mongo slots and fenced writes
- make Project open/read paths mutation-free and remove the v2 page lease, activate route, shared-root materialization, and migration machinery
- keep chat ordering and active-run ownership in Engine/ACS/Mattermost; ECAP only delivers messages and accounts for Project capacity
- remove the redundant AuthoringTurn collection, Project current-turn field, stop-dispatch latch, and chat recovery state machine
- preserve the Test Agent model selector/control-plane flow delivered by the dependent Pack change

## Scope

- v2 only; v1 behavior is unchanged
- no data migration because v2 has not launched
- no browser-tab lock, cross-tab scheduler, or requirement for the current Project to reach a terminal state before another Project can run
- same Project opened in multiple pages is supported; page open itself does not claim capacity or start a Sandbox
- same-Project next turns supersede only the capacity fence and are never rejected by an ECAP chat lock

## Engine / ACS contract fixes

- call Engine start on every v2 message, even when desired state is already running, so the ACS route is reloaded
- treat terminal Engine assistant segments (`terminal=true`, phase `final|error`) as the real completion signal
- finish exact turn capacity after a confirmed `/stop`, because ACS `chat.aborted` does not emit a terminal assistant segment
- leave failed or unconfirmed stop dispatches unlatching and immediately retryable

## Dependency

Depends on SerendipityOneInc/ecap-agent-pack#236: https://github.com/SerendipityOneInc/ecap-agent-pack/pull/236

## Verification

- 514 Agent Builder, runtime, Engine install/lifecycle, lifetime, and scheduler backend tests passed
- 51 final turn/slot/recovery focused regression tests passed after the last audit fix
- 450 focused Agent Builder frontend tests passed
- Ruff, formatting, Pyright, import-linter, complexity, file-length, collection-name, repo-sync, dead-code, and database-return checks passed
- TypeScript and ESLint passed
- `verify-changed` passed for backend and frontend
- `git diff --check` passed; unrelated local `settings.py` edits were excluded from the commit

## Review note

This PR exceeds the mechanical size budget primarily because it removes the obsolete lease/migration implementation and its tests. It has the approved `size-override` label. The final simplification commit removes more code than it adds and leaves one capacity state machine instead of separate Project, AuthoringTurn, slot, stop-dispatch, and recovery state.



### 变更文件

- docs/superpowers/plans/2026-07-24-agent-builder-v2.md
- docs/superpowers/plans/2026-08-03-agent-builder-backend-capability-integration.md
- docs/superpowers/plans/2026-08-10-agent-builder-v2-project-runtime-isolation.md
- docs/superpowers/plans/2026-08-11-agent-builder-v1-project-recovery.md
- docs/superpowers/specs/2026-07-24-agent-builder-v2-design.md
- docs/superpowers/specs/2026-08-03-agent-builder-workspace-access-state.md
- docs/superpowers/specs/2026-08-05-agent-builder-v2-recovery-model-artifact.md
- docs/superpowers/specs/2026-08-10-agent-builder-v2-project-runtime-isolation-design.md
- docs/superpowers/specs/2026-08-11-agent-builder-v1-project-recovery-design.md
- services/claw-interface/app/database/agent_builder_project_repo.py
- services/claw-interface/app/database/agent_builder_project_runtime_repo.py
- services/claw-interface/app/database/agent_builder_runtime_slot_repo.py
- services/claw-interface/app/database/agent_builder_workspace_lease_repo.py
- services/claw-interface/app/database/agent_workspace_index_repo.py
- services/claw-interface/app/database/agent_workspace_repo.py
- services/claw-interface/app/database/collections.py
- services/claw-interface/app/database/engine_agent_workspace_repo.py
- services/claw-interface/app/lifetime.py
- services/claw-interface/app/routes/agent_builder_entry.py
- services/claw-interface/app/routes/agent_builder_v2.py
- services/claw-interface/app/routes/service_api/_agents.py
- services/claw-interface/app/scheduler.py
- services/claw-interface/app/schema/agent_builder.py
- services/claw-interface/app/schema/agent_builder_recovery.py
- services/claw-interface/app/schema/agent_builder_runtime_slot.py
- services/claw-interface/app/schema/agent_builder_turn.py
- services/claw-interface/app/schema/agent_builder_workspace_lease.py
- services/claw-interface/app/schema/agent_workspace.py
- services/claw-interface/app/services/agent_builder_diagnostics.py
- services/claw-interface/app/services/agent_builder_diagnostics_shapes.py
- services/claw-interface/app/services/agent_builder_migration_service.py
- services/claw-interface/app/services/agent_builder_package_capacity_policy.py
- services/claw-interface/app/services/agent_builder_recovery_archive.py
- services/claw-interface/app/services/agent_builder_recovery_service.py
- services/claw-interface/app/services/agent_builder_recovery_source_service.py
- services/claw-interface/app/services/agent_builder_runtime_capacity_service.py
- services/claw-interface/app/services/agent_builder_runtime_diagnostics.py
- services/claw-interface/app/services/agent_builder_runtime_recovery_service.py
- services/claw-interface/app/services/agent_builder_runtime_service.py
- services/claw-interface/app/services/agent_builder_sandbox_operation_service.py
- services/claw-interface/app/services/agent_builder_service.py
- services/claw-interface/app/services/agent_builder_turn_service.py
- services/claw-interface/app/services/agent_builder_turn_status_service.py
- services/claw-interface/app/services/agent_builder_v1_service.py
- services/claw-interface/app/services/agent_builder_v2_runtime_service.py
- services/claw-interface/app/services/agent_builder_v2_service.py
- services/claw-interface/app/services/agent_builder_workspace_lease_service.py
- services/claw-interface/app/services/agents/engine_agent_credential_service.py
- services/claw-interface/app/services/agents/engine_agent_install_context.py
- services/claw-interface/app/services/agents/engine_agent_install_service.py

---

## fix(chat): 优化 Skill 菜单入口与溢出提示 (#3335)

- sha: `b5cbf92198d1c1429dac36417503e4d2d015aeee`
- 作者: lynn Zhuang
- 日期: 2026-08-11T11:11:33Z
- PR: 3335


### 完整 commit message

```
fix(chat): 优化 Skill 菜单入口与溢出提示 (#3335)

## 变更摘要
- 移除 Profile 菜单中重复的 Skill Store 入口；Skills 已可通过 Plugins 页面访问
- Composer 的 Skill 子菜单最多展示 4.5 行，并在内容溢出时显示渐变提示
- 子菜单支持短视口自适应，Skill 列表可独立滚动，底部操作入口保持可见
- 统一 Skill 行与父级菜单的 Hover 圆角，并让子菜单底部对齐、向上展开

## 问题原因
Profile 菜单与 Plugins 页面重复提供了 Skill Store 入口。Composer 的 Skill
子菜单原先只有固定的三行高度，缺少“还有更多内容”的视觉提示；同时 Radix
默认使用顶部对齐，列表变高后会继续向下延伸，在较矮视口中可能裁切内容。

## 测试计划
- [x] `pnpm --filter @zooclaw/chat-ui tsc`
- [x] `pnpm --filter @zooclaw/chat-ui test` (351 tests)
- [x] `pnpm --filter @zooclaw/chat-ui lint`
- [x] `bash scripts/verify-web.sh web/app/src/components/UserMenu.tsx
web/app/tests/unit/components/UserMenu.unit.spec.tsx` (67 tests)
- [x] `bash scripts/verify-web.sh --test-only
web/app/tests/unit/app/agent-builder-create-dialog.unit.spec.tsx` (19
tests)
- [x] `bash scripts/verify-changed.sh`
- [x] 浏览器验证：子菜单与触发行底边偏差为 0px；滚动到底部后渐变消失
- [x] 短视口验证：窗口高度为 280px 时，菜单限制为 280px，Skill 列表在 191px
高度内滚动，两个底部操作入口均完整可见
```


### PR body

## 变更摘要
- 移除 Profile 菜单中重复的 Skill Store 入口；Skills 已可通过 Plugins 页面访问
- Composer 的 Skill 子菜单最多展示 4.5 行，并在内容溢出时显示渐变提示
- 子菜单支持短视口自适应，Skill 列表可独立滚动，底部操作入口保持可见
- 统一 Skill 行与父级菜单的 Hover 圆角，并让子菜单底部对齐、向上展开

## 问题原因
Profile 菜单与 Plugins 页面重复提供了 Skill Store 入口。Composer 的 Skill 子菜单原先只有固定的三行高度，缺少“还有更多内容”的视觉提示；同时 Radix 默认使用顶部对齐，列表变高后会继续向下延伸，在较矮视口中可能裁切内容。

## 测试计划
- [x] `pnpm --filter @zooclaw/chat-ui tsc`
- [x] `pnpm --filter @zooclaw/chat-ui test` (351 tests)
- [x] `pnpm --filter @zooclaw/chat-ui lint`
- [x] `bash scripts/verify-web.sh web/app/src/components/UserMenu.tsx web/app/tests/unit/components/UserMenu.unit.spec.tsx` (67 tests)
- [x] `bash scripts/verify-web.sh --test-only web/app/tests/unit/app/agent-builder-create-dialog.unit.spec.tsx` (19 tests)
- [x] `bash scripts/verify-changed.sh`
- [x] 浏览器验证：子菜单与触发行底边偏差为 0px；滚动到底部后渐变消失
- [x] 短视口验证：窗口高度为 280px 时，菜单限制为 280px，Skill 列表在 191px 高度内滚动，两个底部操作入口均完整可见



### 变更文件

- docs/superpowers/plans/2026-08-11-profile-skill-menu-cleanup.md
- web/app/src/components/UserMenu.tsx
- web/app/tests/unit/components/UserMenu.unit.spec.tsx
- web/packages/chat-ui/src/__tests__/skills-sub-menu.test.tsx
- web/packages/chat-ui/src/composer/SkillsSubMenu.tsx

---

## feat(billing): support Card trial upgrades (#3327)

- sha: `ba03ecd12ace7af24e2524626aa1d5d2a6d2f513`
- 作者: tim-srp
- 日期: 2026-08-11T10:49:46Z
- PR: 3327


### 完整 commit message

```
feat(billing): support Card trial upgrades (#3327)
```


### PR body

## Summary

- complete Creem trial payment orders and preserve exact idempotent replay for webhook and reconciliation retries
- allow eligible Starter Card Trial subscriptions to upgrade immediately to paid Pro or Ultra on either billing cycle
- atomically promote the paid replacement, retain existing Trial credits, and immediately cancel the superseded Creem Trial
- persist replacement cleanup intent and retry incomplete provider cancellation from hourly reconciliation
- recover legacy partial Trial orders after Creem has already transitioned the subscription to `active`
- keep immediate cleanup pending until Creem reports terminal `canceled`, and block expired Trial upgrades in the client
- keep existing active Card upgrade rules and Antom/Alipay behavior unchanged

## Behavior

- Eligible Trial upgrade: current Creem/Card agreement is `trialing`, Starter, unexpired, current, and not scheduled for cancellation
- Paid replacement checkout: `expects_trial=false` and `checkout_intent=upgrade`
- Entitlements: the paid subscription becomes current; Trial credits are not revoked or duplicated
- Provider cleanup: Trial replacement uses Creem `mode=immediate`; active paid replacement remains `mode=scheduled`
- Recovery: atomic handoff stores an immutable cleanup mode; hourly reconciliation retries incomplete cleanup and narrowly repairs identity-matched partial Trial projections without issuing duplicate entitlements

## Validation

- `bash scripts/verify-web.sh ...` — TypeScript passed; 89 frontend tests passed; ESLint passed with one pre-existing warning
- targeted backend unit suite — 355 passed
- targeted Pyright for all changed backend files and tests — 0 errors
- `bash scripts/verify-py.sh --no-types` — Ruff, formatting, and import-linter passed
- all eight custom Python lint guards passed (line limit, architecture, complexity, dependency, collection, repo-list, dead-code and database-return checks)
- `bash scripts/check-pr-size.sh` — 1256 / 3000 lines
- real Mongo transaction test remains opt-in and was not run locally; its updated call contract passes Pyright

## Risk

Medium. The change touches Card/Creem subscription replacement and reconciliation, with strict current-agreement, provider, environment, plan, cycle, expiry, cancellation, and immutable-linkage guards. Antom/Alipay files and behavior are unchanged.



### 变更文件

- docs/superpowers/plans/2026-08-11-creem-card-trial-upgrade.md
- docs/superpowers/specs/2026-08-11-creem-card-trial-upgrade-design.md
- services/claw-interface/app/database/card_checkout_order_repo.py
- services/claw-interface/app/database/creem_replacement_cleanup_repo.py
- services/claw-interface/app/database/subscription_agreement_indexes.py
- services/claw-interface/app/database/subscription_agreement_repo.py
- services/claw-interface/app/schema/billing_v2.py
- services/claw-interface/app/schema/creem.py
- services/claw-interface/app/services/billing_v2/creem_upgrade_admission.py
- services/claw-interface/app/services/creem/checkout_replacement.py
- services/claw-interface/app/services/creem/client.py
- services/claw-interface/app/services/creem/reconciliation.py
- services/claw-interface/app/services/creem/replacement_cleanup_state.py
- services/claw-interface/app/services/creem/replacement_reconciliation.py
- services/claw-interface/app/services/creem/trial_lifecycle.py
- services/claw-interface/pyproject.toml
- services/claw-interface/tests/integration/test_creem_replacement_handoff.py
- services/claw-interface/tests/unit/test_billing_summary_v2.py
- services/claw-interface/tests/unit/test_billing_v2_repos.py
- services/claw-interface/tests/unit/test_card_checkout_upgrade.py
- services/claw-interface/tests/unit/test_creem_checkout_replacement.py
- services/claw-interface/tests/unit/test_creem_client.py
- services/claw-interface/tests/unit/test_creem_first_payment_repo.py
- services/claw-interface/tests/unit/test_creem_reconciliation.py
- services/claw-interface/tests/unit/test_creem_trial_lifecycle.py
- services/claw-interface/tests/unit/test_creem_upgrade_admission.py
- services/claw-interface/tests/unit/test_subscription_agreement_replacement_repo.py
- web/app/src/components/billing/SubscriptionPanel.tsx
- web/app/src/components/billing/hooks/useCheckoutFlow.ts
- web/app/src/components/billing/hooks/useSubscriptionActions.ts
- web/app/tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx

---

## feat(theme): add Paper Focus global skin (#3288)

- sha: `89a7ef226a99655a02218fcaced0fdb143c90c80`
- 作者: shana-srp
- 日期: 2026-08-11T10:10:38Z
- PR: 3288


### 完整 commit message

```
feat(theme): add Paper Focus global skin (#3288)

## Linear

N/A

## Summary
- Add the global Paper Focus theme with Manus-inspired typography,
surfaces, spacing, borders, and responsive shell layout.
- Apply the theme across new chat, navigation, plugins, channels,
schedule, settings, user menu, and subscription pricing surfaces in
light and dark modes.
- Add theme-specific assets, font variables, design reference
documentation, and regression coverage.

## Test plan
- [x] `PATH=/opt/homebrew/opt/node@24/bin:$PATH bash
scripts/verify-web.sh`
- [x] `PATH=/opt/homebrew/opt/node@24/bin:$PATH bash
scripts/verify-changed.sh`
- [x] Local mock-stack visual review across Paper Focus light and dark
pages

## Notes
- The branch was merged with the latest `origin/main` before push.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```


### PR body

## Linear

N/A

## Summary
- Add the global Paper Focus theme with Manus-inspired typography, surfaces, spacing, borders, and responsive shell layout.
- Apply the theme across new chat, navigation, plugins, channels, schedule, settings, user menu, and subscription pricing surfaces in light and dark modes.
- Add theme-specific assets, font variables, design reference documentation, and regression coverage.

## Test plan
- [x] `PATH=/opt/homebrew/opt/node@24/bin:$PATH bash scripts/verify-web.sh`
- [x] `PATH=/opt/homebrew/opt/node@24/bin:$PATH bash scripts/verify-changed.sh`
- [x] Local mock-stack visual review across Paper Focus light and dark pages

## Notes
- The branch was merged with the latest `origin/main` before push.



### 变更文件

- docs/references/manus-brand/DESIGN.md
- docs/superpowers/specs/2026-08-06-paper-focus-theme.md
- web/app/public/images/landing/hero-category-design-dark.svg
- web/app/public/images/landing/hero-category-research-dark.svg
- web/app/src/app/[locale]/(app)/channels/ChannelsPageClient.tsx
- web/app/src/app/[locale]/(app)/channels/components/channels/PlatformCards.tsx
- web/app/src/app/[locale]/(app)/new-chat/NewChatClient.module.css
- web/app/src/app/[locale]/(app)/new-chat/NewChatClient.tsx
- web/app/src/app/[locale]/(app)/plugins/PluginsClient.tsx
- web/app/src/app/[locale]/(app)/schedule/ScheduleWeekView.tsx
- web/app/src/app/[locale]/layout.tsx
- web/app/src/app/globals.css
- web/app/src/app/share/layout.tsx
- web/app/src/components/AppLayout.tsx
- web/app/src/components/UserMenu.tsx
- web/app/src/components/billing/PlanCard.tsx
- web/app/src/components/billing/PromoBadge.tsx
- web/app/src/components/billing/SubscriptionPanel.tsx
- web/app/src/components/chat/unified-chat-composer/UnifiedChatComposer.tsx
- web/app/src/components/composio-connectors/components/ConnectorToolbar.tsx
- web/app/src/components/composio-connectors/components/ProviderCard.tsx
- web/app/src/components/settings/GeneralTab.tsx
- web/app/src/components/settings/ThemeSkinSelector.tsx
- web/app/src/components/sidenav/NavItemComponent.tsx
- web/app/src/components/sidenav/SideNavLogo.tsx
- web/app/src/components/ui/icons/SidebarPanelIcon.tsx
- web/app/src/hooks/queries/billing/useCardCheckoutCapability.ts
- web/app/src/lib/fonts.ts
- web/app/src/lib/new-task-starter-catalog.tsx
- web/app/src/locales/en.ts
- web/app/src/locales/zh.ts
- web/app/src/theme/brand-assets.ts
- web/app/src/theme/brand-theme-tokens.css
- web/app/src/theme/brand-themes.ts
- web/app/tests/unit/app/locale-layout-direction.unit.spec.tsx
- web/app/tests/unit/app/schedule/cron-client.unit.spec.tsx
- web/app/tests/unit/components/AppLayout.unit.spec.tsx
- web/app/tests/unit/components/BrandThemeProvider.unit.spec.tsx
- web/app/tests/unit/components/settings/GeneralTab.unit.spec.tsx

---

## fix(analytics): restore gtag on flight routes (#3329)

- sha: `37aaaaf149cb9548ff2e1e3c1d7322eeaf5c1ae4`
- 作者: Mori-srp
- 日期: 2026-08-11T09:28:54Z
- PR: 3329


### 完整 commit message

```
fix(analytics): restore gtag on flight routes (#3329)

## Summary

- keep the existing parser-executed `<head>` gtag bootstrap as the fast
path
- add an idempotent layout-effect fallback when an OpenNext Flight route
hydrates without `window.gtag`
- restore the direct gtag queue before passive Page View, Auth Action,
Entry Context, and User-ID effects can emit
- keep `send_page_view: false`, environment-specific GA4 IDs, and the
existing Ads/Reddit gates unchanged

## Why

Some deployed locale-rewrite routes return a React Flight fragment. The
nested locale layout's raw bootstrap is then serialized instead of
parser-executed, so the DOM may contain the script text while
`window.gtag` is still missing. Direct GA4 commands consequently
fail-soft and are not sent.

This PR restores the browser sender after hydration. It intentionally
does not restructure the OpenNext/Cloudflare document shell or change
Auth, Account, event contracts, GTM, Ads, Reddit, Consent, or Page View
producers.

## Verification

- TDD: 3 expected failures before implementation; focused bootstrap
tests now 21/21
- related tracking regression: 88/88
- TypeScript, ESLint, repository guards, and `git diff --check`
- full unit run: 644/645 test files passed in the sandbox; the only
listener-based file was blocked by sandbox `EPERM` and passed 32/32 when
rerun outside the sandbox
- Staging Next build and OpenNext/Cloudflare build
- local OpenNext browser receipt on a real Flight-fragment route, direct
load and hard reload:
  - `window.gtag` is a function
  - Staging GA config = 1
  - Ads config = 0
  - `page_view` = 1
  - `web_page_viewed` = 1
- full HTML control route also remains exactly once

## Known boundary and merge gate

The raw HTTP response for affected routes can still be a Flight
fragment; this PR is a sender-receipt fallback, not a document-shell
rewrite.

Before marking the bootstrap gap complete, deploy to Staging and verify
`/new-chat`, Email OTP verify, and Google popup/redirect in Network,
DebugView, and BigQuery. Account confirmation must set GA4 User-ID
before exactly one `account_created` or `login_succeeded`, without
additional Ads/Reddit conversions.
```


### PR body

## Summary

- keep the existing parser-executed `<head>` gtag bootstrap as the fast path
- add an idempotent layout-effect fallback when an OpenNext Flight route hydrates without `window.gtag`
- restore the direct gtag queue before passive Page View, Auth Action, Entry Context, and User-ID effects can emit
- keep `send_page_view: false`, environment-specific GA4 IDs, and the existing Ads/Reddit gates unchanged

## Why

Some deployed locale-rewrite routes return a React Flight fragment. The nested locale layout's raw bootstrap is then serialized instead of parser-executed, so the DOM may contain the script text while `window.gtag` is still missing. Direct GA4 commands consequently fail-soft and are not sent.

This PR restores the browser sender after hydration. It intentionally does not restructure the OpenNext/Cloudflare document shell or change Auth, Account, event contracts, GTM, Ads, Reddit, Consent, or Page View producers.

## Verification

- TDD: 3 expected failures before implementation; focused bootstrap tests now 21/21
- related tracking regression: 88/88
- TypeScript, ESLint, repository guards, and `git diff --check`
- full unit run: 644/645 test files passed in the sandbox; the only listener-based file was blocked by sandbox `EPERM` and passed 32/32 when rerun outside the sandbox
- Staging Next build and OpenNext/Cloudflare build
- local OpenNext browser receipt on a real Flight-fragment route, direct load and hard reload:
  - `window.gtag` is a function
  - Staging GA config = 1
  - Ads config = 0
  - `page_view` = 1
  - `web_page_viewed` = 1
- full HTML control route also remains exactly once

## Known boundary and merge gate

The raw HTTP response for affected routes can still be a Flight fragment; this PR is a sender-receipt fallback, not a document-shell rewrite.

Before marking the bootstrap gap complete, deploy to Staging and verify `/new-chat`, Email OTP verify, and Google popup/redirect in Network, DebugView, and BigQuery. Account confirmation must set GA4 User-ID before exactly one `account_created` or `login_succeeded`, without additional Ads/Reddit conversions.



### 变更文件

- web/app/src/components/TrackingScripts.tsx
- web/app/src/lib/gtag-bootstrap.ts
- web/app/tests/unit/components/TrackingScripts.unit.spec.tsx
- web/app/tests/unit/lib/gtag-bootstrap.unit.spec.ts

---

## fix(dashboard-console): show owned package plan names (#3334)

- sha: `fa579422309167f63599c1a530c73ae978597c8b`
- 作者: bill-srp
- 日期: 2026-08-11T09:13:49Z
- PR: 3334


### 完整 commit message

```
fix(dashboard-console): show owned package plan names (#3334)

## Summary
- show the catalog plan name for owned packages in the offline-order
picker
- retain the plan ID as a fallback when the referenced plan is
unavailable
- keep package selection and submission identity unchanged

## Root cause
The owned-package option rendered its raw `plan_id`, even though the
same dialog already loads the plan catalog for the new-purchase options.
The UI did not join those two in-memory datasets for display.

## Test plan
- [x] `pnpm exec vitest run
app/routes/offline-orders/create-order-dialog.test.tsx`
- [x] `pnpm exec eslint
app/routes/offline-orders/create-order-dialog.tsx
app/routes/offline-orders/create-order-dialog.test.tsx`
- [x] `pnpm exec react-router typegen && pnpm exec tsc -b`
```


### PR body

## Summary
- show the catalog plan name for owned packages in the offline-order picker
- retain the plan ID as a fallback when the referenced plan is unavailable
- keep package selection and submission identity unchanged

## Root cause
The owned-package option rendered its raw `plan_id`, even though the same dialog already loads the plan catalog for the new-purchase options. The UI did not join those two in-memory datasets for display.

## Test plan
- [x] `pnpm exec vitest run app/routes/offline-orders/create-order-dialog.test.tsx`
- [x] `pnpm exec eslint app/routes/offline-orders/create-order-dialog.tsx app/routes/offline-orders/create-order-dialog.test.tsx`
- [x] `pnpm exec react-router typegen && pnpm exec tsc -b`



### 变更文件

- web/dashboard-console/app/routes/offline-orders/create-order-dialog.test.tsx
- web/dashboard-console/app/routes/offline-orders/create-order-dialog.tsx

---

## refactor(claw): introduce leveled auth dependencies and migrate typed consumers (#3322)

- sha: `feb2f00449332cf67357056fccff4686bceb22f0`
- 作者: bill-srp
- 日期: 2026-08-11T07:35:31Z
- PR: 3322


### 完整 commit message

```
refactor(claw): introduce leveled auth dependencies and migrate typed consumers (#3322)

## Summary
- Introduce a leveled, nested auth dependency hierarchy in
`services/claw-interface` so each request resolves each auth level at
most once (FastAPI per-request dependency cache is the dedup mechanism —
no custom caching):
- **L0 `require_verified_token`** → `VerifiedToken` (verified identity +
raw bearer, zero DB)
- **L1 `require_account`** → `AuthedAccount` (L0 + one Account fetch,
verified-email overlay)
- **L2a/L3 org guards** → `OrgMember` (membership + org;
`require_org_admin` now nests on `require_org_member` instead of
re-querying)
- **L2b `require_srp_account`** → rebased onto L1 (still checks the
verified token email)
- **L2 current-org level** `require_current_org` /
`require_current_org_optional` → `CurrentOrgAccount` /
`OrgScopedAccount` (for routes with no `org_id` in the path); all 16
routes that paired `require_account` with the `get_current_org*`
resolvers now take a single leveled dep
- Tiered accumulating principal schemas (`VerifiedToken` →
`AuthedAccount` → `OrgMember`) in `app/schema/auth.py`, mirroring the
existing `ServiceTokenPrincipal` pattern; wrong-level wiring is now a
pyright error.
- Migrate every typed-v2-family consumer (~42 route files) and delete
the old dep names (`get_bearer_token`, `get_token_identity`,
`get_current_account`). The legacy dict stack (`get_current_user`, 47
files) is untouched — that migration is PR 2/3 per the spec.
- **Zero client-visible change**: every HTTP status and `detail` string
is byte-identical (pinned by tests, including guard check ordering).
- New dedup proof test: `tests/unit/test_auth_level_dedup.py` asserts
the Account fetch runs exactly once when L1 + L2 chain on one request.
- Design spec:
`docs/superpowers/specs/2026-08-10-claw-auth-dependency-levels-design.md`;
implementation plan:
`docs/superpowers/plans/2026-08-10-claw-auth-levels-pr1.md` (both
included).

## Test plan
- [x] Unit suite: 8,444 passed (includes new schema, level, and dedup
tests)
- [x] BDD suite with local Mongo: 262 passed, 0 skipped
- [x] Static gate: ruff check + format, pyright (0 errors),
import-linter (8 contracts kept)
- [x] Teardown audit: zero references to the deleted dep names across
`app/` + `tests/`
- [x] Whole-app coverage gate (≥90%) — enforced green in CI's
`claw-interface-quality / test`
```


### PR body

## Summary
- Introduce a leveled, nested auth dependency hierarchy in `services/claw-interface` so each request resolves each auth level at most once (FastAPI per-request dependency cache is the dedup mechanism — no custom caching):
  - **L0 `require_verified_token`** → `VerifiedToken` (verified identity + raw bearer, zero DB)
  - **L1 `require_account`** → `AuthedAccount` (L0 + one Account fetch, verified-email overlay)
  - **L2a/L3 org guards** → `OrgMember` (membership + org; `require_org_admin` now nests on `require_org_member` instead of re-querying)
  - **L2b `require_srp_account`** → rebased onto L1 (still checks the verified token email)
  - **L2 current-org level** `require_current_org` / `require_current_org_optional` → `CurrentOrgAccount` / `OrgScopedAccount` (for routes with no `org_id` in the path); all 16 routes that paired `require_account` with the `get_current_org*` resolvers now take a single leveled dep
- Tiered accumulating principal schemas (`VerifiedToken` → `AuthedAccount` → `OrgMember`) in `app/schema/auth.py`, mirroring the existing `ServiceTokenPrincipal` pattern; wrong-level wiring is now a pyright error.
- Migrate every typed-v2-family consumer (~42 route files) and delete the old dep names (`get_bearer_token`, `get_token_identity`, `get_current_account`). The legacy dict stack (`get_current_user`, 47 files) is untouched — that migration is PR 2/3 per the spec.
- **Zero client-visible change**: every HTTP status and `detail` string is byte-identical (pinned by tests, including guard check ordering).
- New dedup proof test: `tests/unit/test_auth_level_dedup.py` asserts the Account fetch runs exactly once when L1 + L2 chain on one request.
- Design spec: `docs/superpowers/specs/2026-08-10-claw-auth-dependency-levels-design.md`; implementation plan: `docs/superpowers/plans/2026-08-10-claw-auth-levels-pr1.md` (both included).

## Test plan
- [x] Unit suite: 8,444 passed (includes new schema, level, and dedup tests)
- [x] BDD suite with local Mongo: 262 passed, 0 skipped
- [x] Static gate: ruff check + format, pyright (0 errors), import-linter (8 contracts kept)
- [x] Teardown audit: zero references to the deleted dep names across `app/` + `tests/`
- [x] Whole-app coverage gate (≥90%) — enforced green in CI's `claw-interface-quality / test`



### 变更文件

- docs/superpowers/plans/2026-08-10-claw-auth-levels-pr1.md
- docs/superpowers/specs/2026-08-10-claw-auth-dependency-levels-design.md
- services/claw-interface/AGENTS.md
- services/claw-interface/app/middleware/auth.py
- services/claw-interface/app/middleware/org.py
- services/claw-interface/app/routes/account.py
- services/claw-interface/app/routes/agent_builder.py
- services/claw-interface/app/routes/agent_builder_entry.py
- services/claw-interface/app/routes/agent_builder_v2.py
- services/claw-interface/app/routes/agent_packs.py
- services/claw-interface/app/routes/agents/artifacts.py
- services/claw-interface/app/routes/agents/channels.py
- services/claw-interface/app/routes/agents/conversations.py
- services/claw-interface/app/routes/agents/crud.py
- services/claw-interface/app/routes/agents/lifecycle.py
- services/claw-interface/app/routes/agents/model.py
- services/claw-interface/app/routes/agents/schedules.py
- services/claw-interface/app/routes/computer/agents.py
- services/claw-interface/app/routes/computer/computers.py
- services/claw-interface/app/routes/computer/conversations.py
- services/claw-interface/app/routes/council.py
- services/claw-interface/app/routes/enterprise/org.py
- services/claw-interface/app/routes/enterprise/org_skills.py
- services/claw-interface/app/routes/enterprise/pack_test_runs.py
- services/claw-interface/app/routes/enterprise/service_tokens.py
- services/claw-interface/app/routes/enterprise/users.py
- services/claw-interface/app/routes/internal/agent_packs.py
- services/claw-interface/app/routes/internal/skills.py
- services/claw-interface/app/routes/skills_manager.py
- services/claw-interface/app/routes/vertical_pack/package.py
- services/claw-interface/app/routes/vertical_pack/plan.py
- services/claw-interface/app/schema/account_api.py
- services/claw-interface/app/schema/auth.py
- services/claw-interface/app/services/org/membership_service.py
- services/claw-interface/tests/bdd/step_defs/test_engine_agents_steps.py
- services/claw-interface/tests/bdd/step_defs/test_org_lifecycle.py
- services/claw-interface/tests/bdd/step_defs/test_registration.py
- services/claw-interface/tests/bdd/step_defs/test_service_tokens.py
- services/claw-interface/tests/unit/_builders.py
- services/claw-interface/tests/unit/test_account_team_org_route.py
- services/claw-interface/tests/unit/test_agent_artifact_routes.py
- services/claw-interface/tests/unit/test_agent_builder_routes.py
- services/claw-interface/tests/unit/test_agent_conversations.py
- services/claw-interface/tests/unit/test_agent_routes.py
- services/claw-interface/tests/unit/test_agents_v2_channels_routes.py
- services/claw-interface/tests/unit/test_agents_v2_routes.py
- services/claw-interface/tests/unit/test_agents_v2_schedules_routes.py
- services/claw-interface/tests/unit/test_auth_level_dedup.py
- services/claw-interface/tests/unit/test_auth_schemas.py
- services/claw-interface/tests/unit/test_computer_routes.py

---

## fix(design-system): 统一 Dialog 与 AlertDialog 的视觉和关闭交互 (#3332)

- sha: `f07e46070d62241693bf049b8a7bf9e879110404`
- 作者: lynn Zhuang
- 日期: 2026-08-11T07:23:06Z
- PR: 3332


### 完整 commit message

```
fix(design-system): 统一 Dialog 与 AlertDialog 的视觉和关闭交互 (#3332)

## 变更摘要

- 为 Dialog 与 AlertDialog 提取共享的 modal 视觉规则，统一遮罩、实体弹层、圆角、边框、阴影、标题、说明和操作区布局
- 将 AlertDialog 从低对比度玻璃表面调整为与 Dialog 一致的实体浮层，并移除突兀的底部分割线
- 为 AlertDialog 增加与 Dialog 一致的 Heroicon 关闭按钮，支持通过
`showCloseButton={false}` 隐藏
- 保持 AlertDialog 的取消语义：右上角关闭按钮使用 Cancel primitive，默认焦点落在底部
Cancel，关闭后焦点返回触发按钮
- 增加视觉契约、关闭交互、默认焦点及可选关闭按钮的回归测试

## 根因

AlertDialog 仍在独立使用旧的 Liquid Glass 表面、模糊遮罩、标题字体和带分割线的 footer，而普通 Dialog
已经切换到实体浮层语言。两套组件缺少共享视觉契约，导致同属 modal 家族的组件在亮暗模式、关闭入口和交互焦点上逐渐分叉。

## 测试计划

- [x] `pnpm --filter @zooclaw/design-system test --
alert-dialog.test.tsx dialog.test.tsx`（53 个测试文件、301 项测试通过）
- [x] `pnpm --filter @zooclaw/design-system tsc`
- [x] `pnpm --filter @zooclaw/design-system lint`
- [x] `pnpm --filter @zooclaw/design-system build:preview`
- [x] 浏览器走查亮色与暗色 AlertDialog
- [x] 验证右上角关闭、底部 Cancel 默认焦点以及关闭后焦点回归

## 备注

`scripts/verify-changed.sh` 当前未给 `web/packages` 提供独立本地入口，因此统一 verifier
提示由 CI 兜底；上述设计系统包级检查均已通过。
```


### PR body

## 变更摘要

- 为 Dialog 与 AlertDialog 提取共享的 modal 视觉规则，统一遮罩、实体弹层、圆角、边框、阴影、标题、说明和操作区布局
- 将 AlertDialog 从低对比度玻璃表面调整为与 Dialog 一致的实体浮层，并移除突兀的底部分割线
- 为 AlertDialog 增加与 Dialog 一致的 Heroicon 关闭按钮，支持通过 `showCloseButton={false}` 隐藏
- 保持 AlertDialog 的取消语义：右上角关闭按钮使用 Cancel primitive，默认焦点落在底部 Cancel，关闭后焦点返回触发按钮
- 增加视觉契约、关闭交互、默认焦点及可选关闭按钮的回归测试

## 根因

AlertDialog 仍在独立使用旧的 Liquid Glass 表面、模糊遮罩、标题字体和带分割线的 footer，而普通 Dialog 已经切换到实体浮层语言。两套组件缺少共享视觉契约，导致同属 modal 家族的组件在亮暗模式、关闭入口和交互焦点上逐渐分叉。

## 测试计划

- [x] `pnpm --filter @zooclaw/design-system test -- alert-dialog.test.tsx dialog.test.tsx`（53 个测试文件、301 项测试通过）
- [x] `pnpm --filter @zooclaw/design-system tsc`
- [x] `pnpm --filter @zooclaw/design-system lint`
- [x] `pnpm --filter @zooclaw/design-system build:preview`
- [x] 浏览器走查亮色与暗色 AlertDialog
- [x] 验证右上角关闭、底部 Cancel 默认焦点以及关闭后焦点回归

## 备注

`scripts/verify-changed.sh` 当前未给 `web/packages` 提供独立本地入口，因此统一 verifier 提示由 CI 兜底；上述设计系统包级检查均已通过。



### 变更文件

- web/packages/zooclaw-design-system/src/components/alert-dialog.test.tsx
- web/packages/zooclaw-design-system/src/components/alert-dialog.tsx
- web/packages/zooclaw-design-system/src/components/dialog.tsx
- web/packages/zooclaw-design-system/src/components/modal-styles.ts

---

## feat(dashboard): allow zero-value offline orders (#3331)

- sha: `6b2317392f50a413aa81f5d419ed736914011da7`
- 作者: bill-srp
- 日期: 2026-08-11T06:22:36Z
- PR: 3331


### 完整 commit message

```
feat(dashboard): allow zero-value offline orders (#3331)

## Summary

- allow the dashboard offline-order dialog to submit a zero amount for
package and Vertical Plan orders
- keep organization top-ups strictly positive
- preserve the existing positive-only parser while adding an explicit
non-negative parser for package/plan flows
- add dialog and parser regression coverage for zero-value plans and
rejected zero-value top-ups

## Test plan

- [x] Dashboard Console Vitest suite: 71 files, 634 tests passed
- [x] Dashboard Console ESLint
- [x] Dashboard Console typecheck (`wrangler types`, React Router
typegen, and `tsc -b`)

## Dependency

- Backend support was merged in #3330.
```


### PR body

## Summary

- allow the dashboard offline-order dialog to submit a zero amount for package and Vertical Plan orders
- keep organization top-ups strictly positive
- preserve the existing positive-only parser while adding an explicit non-negative parser for package/plan flows
- add dialog and parser regression coverage for zero-value plans and rejected zero-value top-ups

## Test plan

- [x] Dashboard Console Vitest suite: 71 files, 634 tests passed
- [x] Dashboard Console ESLint
- [x] Dashboard Console typecheck (`wrangler types`, React Router typegen, and `tsc -b`)

## Dependency

- Backend support was merged in #3330.




### 变更文件

- web/dashboard-console/app/lib/offline-orders.test.ts
- web/dashboard-console/app/lib/offline-orders.ts
- web/dashboard-console/app/routes/offline-orders/create-order-dialog.test.tsx
- web/dashboard-console/app/routes/offline-orders/create-order-dialog.tsx

---

## feat(billing): allow zero-value offline orders (#3330)

- sha: `07a4dbcdbf7840b0c1a3ffef3bdf3ac651344280`
- 作者: bill-srp
- 日期: 2026-08-11T05:51:38Z
- PR: 3330


### 完整 commit message

```
feat(billing): allow zero-value offline orders (#3330)

## Linear

No Linear issue linked.

## Summary

- allow package/plan offline orders whose amount and monthly credits are
both zero
- keep mixed zero/non-zero values invalid, and keep org top-ups plus
online provider flows positive-only
- carry explicit zero-credit handling through confirmation,
compensation, and calendar credit resets so Billing Gateway receives the
real zero-value request
- add regression coverage for request validation, plan provisioning,
snapshots, fulfillment, reset, revoke, and offline-order creation

## Test plan

- [x] `pytest -q` for the six affected offline-order,
enterprise-package, fulfillment, and yearly-reset unit suites (214
passed)
- [x] Ruff check and format check
- [x] import-linter architecture contracts
- [ ] Full local Pyright could not run cleanly because the configured
local venv cannot resolve existing dependencies including FastAPI,
pytest, and favie-common; rely on CI for the authoritative type check

## Follow-up

- Validate a real zero-credit request against Billing Gateway; this PR
deliberately removes the claw-interface restriction without claiming
downstream production support.
- The dashboard offline-order dialog still rejects zero amounts and is
outside this backend-only change.
```


### PR body

## Linear

No Linear issue linked.

## Summary

- allow package/plan offline orders whose amount and monthly credits are both zero
- keep mixed zero/non-zero values invalid, and keep org top-ups plus online provider flows positive-only
- carry explicit zero-credit handling through confirmation, compensation, and calendar credit resets so Billing Gateway receives the real zero-value request
- add regression coverage for request validation, plan provisioning, snapshots, fulfillment, reset, revoke, and offline-order creation

## Test plan

- [x] `pytest -q` for the six affected offline-order, enterprise-package, fulfillment, and yearly-reset unit suites (214 passed)
- [x] Ruff check and format check
- [x] import-linter architecture contracts
- [ ] Full local Pyright could not run cleanly because the configured local venv cannot resolve existing dependencies including FastAPI, pytest, and favie-common; rely on CI for the authoritative type check

## Follow-up

- Validate a real zero-credit request against Billing Gateway; this PR deliberately removes the claw-interface restriction without claiming downstream production support.
- The dashboard offline-order dialog still rejects zero amounts and is outside this backend-only change.



### 变更文件

- services/claw-interface/app/routes/internal/offline_order.py
- services/claw-interface/app/services/billing_v2/credit_reset_sources.py
- services/claw-interface/app/services/billing_v2/enterprise_packages.py
- services/claw-interface/app/services/billing_v2/fulfillment.py
- services/claw-interface/app/services/billing_v2/offline_order_agreements.py
- services/claw-interface/app/services/billing_v2/offline_order_compensation.py
- services/claw-interface/app/services/billing_v2/offline_order_creation.py
- services/claw-interface/app/services/billing_v2/offline_order_plan_purchase.py
- services/claw-interface/app/services/billing_v2/offline_orders.py
- services/claw-interface/app/services/billing_v2/yearly_credits_reset.py
- services/claw-interface/tests/unit/test_billing_v2_fulfillment.py
- services/claw-interface/tests/unit/test_enterprise_package_subscription.py
- services/claw-interface/tests/unit/test_offline_order_plan_purchase.py
- services/claw-interface/tests/unit/test_offline_orders_routes.py
- services/claw-interface/tests/unit/test_offline_orders_service.py

---

## feat(analytics): capture web session entry identity (#3324)

- sha: `f13b24ba99a9ea5bdddf62f342dd08b1c8555614`
- 作者: Mori-srp
- 日期: 2026-08-11T03:37:58Z
- PR: 3324


### 完整 commit message

```
feat(analytics): capture web session entry identity (#3324)

## Linear

Not linked. This owner-approved analytics phase is tracked in the local
ZooClaw traffic-audit Task.

## Summary

- Add the missing Session-entry receipts: `entry_captured` and
`entry_identity_resolved`.
- Start entry tracking once after the first manual Page View for every
normal `ClientLayout` Web entry; do not hard-code an acquisition-page
allowlist in the frontend.
- Freeze one immutable `entry_context_id` plus the eleven reviewed
attribution fields, then perform one fresh, read-only `/account/me`
observation.
- Resolve entry identity as `authenticated`, `anonymous_confirmed`, or
`unresolved`; later authentication cannot overwrite the entry fact.
- Treat an Account request timeout as `unresolved`, while a real page
unmount remains an intentionally incomplete receipt.
- Keep both events on the canonical GA4/dataLayer path only. They do not
trigger Google Ads or Reddit conversions and do not modify Account,
authentication, cookies, User-ID, GTM, or terminal-event truth.

## Why

GA4 all-site Sessions and `first_visit` cannot serve as the denominator
for new-account acquisition. This change records whether a Web entry was
actually authenticated, confirmed anonymous, or unresolved so a later
BigQuery Session fact can connect entry → `auth_started` →
`account_created` / `login_succeeded`.

The frontend observes broadly and classifies later. Acquisition
eligibility remains a versioned BigQuery/report rule, so future landing
pages are not silently lost when no new pathname is added to frontend
code.

## Scope boundaries

- This PR does not add BigQuery SQL, weekly-report logic, GTM,
Ads/Reddit conversion behavior, or the separate gtag-bootstrap repair.
- This PR explicitly projects reviewed source fields but does not claim
the current GA4 chain is `PII-safe`; broader URL/PII redaction remains a
separate follow-up.
- Network, DebugView, BigQuery, Staging, and Production receipt
validation remain later gates.

## Test plan

- [x] Six focused Phase 2/Auth attribution test files: 146/146 passed.
- [x] Scoped ESLint passed.
- [x] Pre-push size Gate passed: 703/3000 counted source/test lines.
- [x] Seven repository governance guards passed.
- [x] TypeScript and full frontend ESLint passed in the pre-push
changed-surface Gate.
- [x] Remote compare verified: one commit, nine files, no duplicated
Auth Action V2 changes.
- [ ] GitHub CI build, CodeQL, Codex, and Claude review.
- [ ] Staging Network / DebugView / BigQuery receipt validation after
the independent gtag-bootstrap Gate.
```


### PR body

## Linear

Not linked. This owner-approved analytics phase is tracked in the local ZooClaw traffic-audit Task.

## Summary

- Add the missing Session-entry receipts: `entry_captured` and `entry_identity_resolved`.
- Start entry tracking once after the first manual Page View for every normal `ClientLayout` Web entry; do not hard-code an acquisition-page allowlist in the frontend.
- Freeze one immutable `entry_context_id` plus the eleven reviewed attribution fields, then perform one fresh, read-only `/account/me` observation.
- Resolve entry identity as `authenticated`, `anonymous_confirmed`, or `unresolved`; later authentication cannot overwrite the entry fact.
- Treat an Account request timeout as `unresolved`, while a real page unmount remains an intentionally incomplete receipt.
- Keep both events on the canonical GA4/dataLayer path only. They do not trigger Google Ads or Reddit conversions and do not modify Account, authentication, cookies, User-ID, GTM, or terminal-event truth.

## Why

GA4 all-site Sessions and `first_visit` cannot serve as the denominator for new-account acquisition. This change records whether a Web entry was actually authenticated, confirmed anonymous, or unresolved so a later BigQuery Session fact can connect entry → `auth_started` → `account_created` / `login_succeeded`.

The frontend observes broadly and classifies later. Acquisition eligibility remains a versioned BigQuery/report rule, so future landing pages are not silently lost when no new pathname is added to frontend code.

## Scope boundaries

- This PR does not add BigQuery SQL, weekly-report logic, GTM, Ads/Reddit conversion behavior, or the separate gtag-bootstrap repair.
- This PR explicitly projects reviewed source fields but does not claim the current GA4 chain is `PII-safe`; broader URL/PII redaction remains a separate follow-up.
- Network, DebugView, BigQuery, Staging, and Production receipt validation remain later gates.

## Test plan

- [x] Six focused Phase 2/Auth attribution test files: 146/146 passed.
- [x] Scoped ESLint passed.
- [x] Pre-push size Gate passed: 703/3000 counted source/test lines.
- [x] Seven repository governance guards passed.
- [x] TypeScript and full frontend ESLint passed in the pre-push changed-surface Gate.
- [x] Remote compare verified: one commit, nine files, no duplicated Auth Action V2 changes.
- [ ] GitHub CI build, CodeQL, Codex, and Claude review.
- [ ] Staging Network / DebugView / BigQuery receipt validation after the independent gtag-bootstrap Gate.



### 变更文件

- docs/superpowers/specs/2026-08-10-session-entry-context-v1.md
- web/app/src/hooks/useEntryContextTracking.ts
- web/app/src/hooks/usePageTracking.ts
- web/app/src/lib/entry-context.ts
- web/app/src/lib/tracking.ts
- web/app/tests/unit/hooks/useEntryContextTracking.unit.spec.ts
- web/app/tests/unit/hooks/usePageTracking.unit.spec.ts
- web/app/tests/unit/lib/entry-context.unit.spec.ts
- web/app/tests/unit/lib/tracking.unit.spec.ts

---

## feat(publish): show installed agent id in the detail modal (#3328)

- sha: `066d0eeef20c7063ffe09c6851fdfcde0fc541cf`
- 作者: finn-srp
- 日期: 2026-08-11T03:28:57Z
- PR: 3328


### 完整 commit message

```
feat(publish): show installed agent id in the detail modal (#3328)

## Linear

无（用户直接提出的 UI 需求）。

## Summary

My Custom Specialists 的详情弹窗此前只展示 pack 身份，没有已安装 agent 的后端
`agent_id`——而用户在 Agent Builder 里写 ref、提工单时需要的正是这个值。

- `PublishAgentCardItem` 新增 `agentId`，由 `card-model.ts` 从已安装 agent
带出（org-pack 行取 `installedAgent?.id`，db-only 行取
`agent.id`）。这个字段**不能**用已有的 `id` 代替：org-pack 行的 `id` 是 `display_id ||
pack_id`，只有 db-only 行两者才恰好相同，类型上加了 JSDoc 说明。
- 弹窗在 Description 与 Archive File 之间渲染 **Agent ID**（mono 字体）+
一个复制按钮。未安装的记录没有该字段，整行不渲染。
- 复制走仓库已有的 `copyToClipboard`（`@zooclaw/chat-ui`，失败会经 logger 上报），而不是再手搓一遍
`navigator.clipboard.writeText` + `try/catch`。
- 「已复制」的闪烁状态属于纯展示态，按 `web/app/AGENTS.md` 的 MVVM 约定留在 view 层；定时器由 effect
持有，弹窗在闪烁期间被关掉会自动取消，不会向已卸载组件 setState。
- 新增 `common.copied`（`common.copy` 已存在）与页面级的
`zooSquare.publish.detail.agentId`，en/zh 双语。

### 已知的相关问题（本 PR 未处理）

- `src/components/settings/GeneralTab.tsx` 的 `CopyButton` 与本 PR
的复制按钮是近乎逐字的重复（同 2000ms、同图标尺寸、同配色），全仓类似形态共 8 处。提取共享组件需要一并迁移
GeneralTab，超出本 PR 范围，建议单独开一个 PR 做。
- 安装确认弹窗的文案是裸 key（`zooSquare.publish.installConfirmTitle` /
`installConfirmDesc`），en/zh 都缺翻译。与本 PR 无关的既有问题。

## Test plan

- [x] `bash scripts/verify-web.sh
'src/app/[locale]/(app)/agents-manager/publish' src/locales
tests/unit/app` — guards + tsc + vitest + eslint 全绿
- [x] `bash scripts/verify-changed.sh` — 变更面 gate 全绿
- [x] 新增 2
个单测（`tests/unit/app/agents-manager-publish.unit.spec.tsx`）：已安装时弹窗展示
`agent_id`（断言的是 agent 身份而非 pack 身份）；未安装时该行不渲染
- [ ] **未做**：登录态下的真机 UI 验证。本地 `pnpm dev:staging` 已跑通、路由
200、编译无新增报错，但该弹窗需要真实 staging 账号登录后才能看到，需人工点一次确认复制手感

> 备注：本地 staging dev server 日志里的 `Failed to generate static paths for
/[locale]/agents-manager: SyntaxError: Unexpected end of JSON input`
在本改动之前就存在（stash 后跑基线复现），与本 PR 无关。

Co-authored-by: wangfulong <wfllike@gmail.com>
```


### PR body

## Linear

无（用户直接提出的 UI 需求）。

## Summary

My Custom Specialists 的详情弹窗此前只展示 pack 身份，没有已安装 agent 的后端 `agent_id`——而用户在 Agent Builder 里写 ref、提工单时需要的正是这个值。

- `PublishAgentCardItem` 新增 `agentId`，由 `card-model.ts` 从已安装 agent 带出（org-pack 行取 `installedAgent?.id`，db-only 行取 `agent.id`）。这个字段**不能**用已有的 `id` 代替：org-pack 行的 `id` 是 `display_id || pack_id`，只有 db-only 行两者才恰好相同，类型上加了 JSDoc 说明。
- 弹窗在 Description 与 Archive File 之间渲染 **Agent ID**（mono 字体）+ 一个复制按钮。未安装的记录没有该字段，整行不渲染。
- 复制走仓库已有的 `copyToClipboard`（`@zooclaw/chat-ui`，失败会经 logger 上报），而不是再手搓一遍 `navigator.clipboard.writeText` + `try/catch`。
- 「已复制」的闪烁状态属于纯展示态，按 `web/app/AGENTS.md` 的 MVVM 约定留在 view 层；定时器由 effect 持有，弹窗在闪烁期间被关掉会自动取消，不会向已卸载组件 setState。
- 新增 `common.copied`（`common.copy` 已存在）与页面级的 `zooSquare.publish.detail.agentId`，en/zh 双语。

### 已知的相关问题（本 PR 未处理）

- `src/components/settings/GeneralTab.tsx` 的 `CopyButton` 与本 PR 的复制按钮是近乎逐字的重复（同 2000ms、同图标尺寸、同配色），全仓类似形态共 8 处。提取共享组件需要一并迁移 GeneralTab，超出本 PR 范围，建议单独开一个 PR 做。
- 安装确认弹窗的文案是裸 key（`zooSquare.publish.installConfirmTitle` / `installConfirmDesc`），en/zh 都缺翻译。与本 PR 无关的既有问题。

## Test plan

- [x] `bash scripts/verify-web.sh 'src/app/[locale]/(app)/agents-manager/publish' src/locales tests/unit/app` — guards + tsc + vitest + eslint 全绿
- [x] `bash scripts/verify-changed.sh` — 变更面 gate 全绿
- [x] 新增 2 个单测（`tests/unit/app/agents-manager-publish.unit.spec.tsx`）：已安装时弹窗展示 `agent_id`（断言的是 agent 身份而非 pack 身份）；未安装时该行不渲染
- [ ] **未做**：登录态下的真机 UI 验证。本地 `pnpm dev:staging` 已跑通、路由 200、编译无新增报错，但该弹窗需要真实 staging 账号登录后才能看到，需人工点一次确认复制手感

> 备注：本地 staging dev server 日志里的 `Failed to generate static paths for /[locale]/agents-manager: SyntaxError: Unexpected end of JSON input` 在本改动之前就存在（stash 后跑基线复现），与本 PR 无关。



### 变更文件

- web/app/src/app/[locale]/(app)/agents-manager/publish/components/PublishDetailModal.tsx
- web/app/src/app/[locale]/(app)/agents-manager/publish/components/types.ts
- web/app/src/app/[locale]/(app)/agents-manager/publish/lib/card-model.ts
- web/app/src/locales/en.ts
- web/app/src/locales/zh.ts
- web/app/tests/unit/app/agents-manager-publish.unit.spec.tsx

---
