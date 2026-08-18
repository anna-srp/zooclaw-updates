# SerendipityOneInc/ecap-workspace — commits 2026-08-17

## fix(agent-builder): refine create dialog composer (#3395)

- **SHA**: `21d032c5c549d3f242258addc17a7f184562ef22`
- **作者**: lynn Zhuang
- **日期**: 2026-08-17T11:58:59Z
- **PR**: #3395

### Commit Message

```
fix(agent-builder): refine create dialog composer (#3395)

## Summary
- update the Agent Builder Create dialog heading to ask what kind of
agent the user wants to create
- replace the shared Landing examples with five Agent Builder-specific
sample prompts; clicking a short title inserts its full prompt
- reuse the shared `UnifiedChatComposer` used by chat sessions instead
of maintaining a separate Create-dialog composer
- replace the clipped model avatar/readout with the shared model picker
and preserve the catalog logo and display name for Builder model aliases
- limit the picker to Builder-authorized models when that list is
available
- apply the selected model before the first Builder turn; blank creation
saves the model without sending a message
- keep legacy pending-creation recovery records compatible

## Root cause
The Create dialog had its own partial composer implementation and
rendered the model through a circular avatar, so its behavior and
presentation had drifted from chat sessions. Builder model aliases also
did not resolve to their matching catalog presentation metadata.

The Create dialog also reused Landing prompt keys, which prevented its
examples from changing independently.

## Test plan
- [x] selected frontend verification: TypeScript, 9 test files / 180
tests, and ESLint passed
- [x] pre-push changed-surface verification passed
- [x] local mock preview verified the shared composer, intact provider
logo, and working model dropdown
```

### PR Body

## Summary
- update the Agent Builder Create dialog heading to ask what kind of agent the user wants to create
- replace the shared Landing examples with five Agent Builder-specific sample prompts; clicking a short title inserts its full prompt
- reuse the shared `UnifiedChatComposer` used by chat sessions instead of maintaining a separate Create-dialog composer
- replace the clipped model avatar/readout with the shared model picker and preserve the catalog logo and display name for Builder model aliases
- limit the picker to Builder-authorized models when that list is available
- apply the selected model before the first Builder turn; blank creation saves the model without sending a message
- keep legacy pending-creation recovery records compatible

## Root cause
The Create dialog had its own partial composer implementation and rendered the model through a circular avatar, so its behavior and presentation had drifted from chat sessions. Builder model aliases also did not resolve to their matching catalog presentation metadata.

The Create dialog also reused Landing prompt keys, which prevented its examples from changing independently.

## Test plan
- [x] selected frontend verification: TypeScript, 9 test files / 180 tests, and ESLint passed
- [x] pre-push changed-surface verification passed
- [x] local mock preview verified the shared composer, intact provider logo, and working model dropdown


---

## fix(billing): release personal agreement on enterprise handoff (#3407)

- **SHA**: `f103dbe53aa6d217846e6efae57bd4c041d64c00`
- **作者**: kaka-srp
- **日期**: 2026-08-17T07:46:13Z
- **PR**: #3407

### Commit Message

```
fix(billing): release personal agreement on enterprise handoff (#3407)
```

---

## fix(agent-builder): add animated home loading skeleton (#3396)

- **SHA**: `719cdd79c36bfa487152cffef405abf7a525d2b2`
- **作者**: lynn Zhuang
- **日期**: 2026-08-17T07:18:25Z
- **PR**: #3396

### Commit Message

```
fix(agent-builder): add animated home loading skeleton (#3396)

## Summary
- Replace the bordered pulse wireframe on the Agent Builder home page
with a responsive three-row skeleton aligned to the agent list.
- Remove loading-only table headers and divider lines, and add staggered
1.4-second shimmer motion with a reduced-motion fallback.
- Fix the shared shimmer utility so its animated background position is
no longer pinned by an important background shorthand.

## Root cause
The loading state used a generic bordered pulse block instead of
mirroring the eventual list layout. The initial shimmer implementation
also used an important `background` shorthand, which implicitly fixed
`background-position` and prevented the running keyframes from producing
visible motion.

## Test plan
- [x] `bash scripts/verify-local.sh --web-static 'src/app/globals.css'
'src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderHome.tsx'
'tests/unit/app/agent-builder-production-home.unit.spec.tsx'`
- [x] `bash scripts/verify-changed.sh`
- [x] Local `ready-user` mock with the projects request delayed:
confirmed three skeleton rows, no loading table/header chrome, and
changing shimmer background positions.
- [x] Verified `prefers-reduced-motion` still disables the skeleton
animation.
```

### PR Body

## Summary
- Replace the bordered pulse wireframe on the Agent Builder home page with a responsive three-row skeleton aligned to the agent list.
- Remove loading-only table headers and divider lines, and add staggered 1.4-second shimmer motion with a reduced-motion fallback.
- Fix the shared shimmer utility so its animated background position is no longer pinned by an important background shorthand.

## Root cause
The loading state used a generic bordered pulse block instead of mirroring the eventual list layout. The initial shimmer implementation also used an important `background` shorthand, which implicitly fixed `background-position` and prevented the running keyframes from producing visible motion.

## Test plan
- [x] `bash scripts/verify-local.sh --web-static 'src/app/globals.css' 'src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderHome.tsx' 'tests/unit/app/agent-builder-production-home.unit.spec.tsx'`
- [x] `bash scripts/verify-changed.sh`
- [x] Local `ready-user` mock with the projects request delayed: confirmed three skeleton rows, no loading table/header chrome, and changing shimmer background positions.
- [x] Verified `prefers-reduced-motion` still disables the skeleton animation.


---

## feat(agent-marketplace): add scoped agent catalogs (#3368)

- **SHA**: `c5b88ecb35463bd4e8dd6e5d436a60ac7b10f0ec`
- **作者**: lynn Zhuang
- **日期**: 2026-08-17T05:55:32Z
- **PR**: #3368

### Commit Message

```
feat(agent-marketplace): add scoped agent catalogs (#3368)

## Linear

N/A

## Summary

- Refactor Agent Marketplace into independent Public, Shared with me,
and My Agents catalogs.
- Keep share-link agents out of Shared with me until they are hired,
while preserving installed snapshots if sharing later ends.
- Surface Agent Builder records directly in My Agents with lifecycle
badges and ZooClaw Design System card actions.
- Preserve existing public card styling, detail dialogs,
install/update/fire flows, and add mock scenarios for all visibility
states.
- Add regression coverage for lifecycle rendering, exact
shared-workspace updates, install-state loading, bio fallback, dialog
embedding, and card keyboard semantics.

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] Targeted `verify-web.sh`: TypeScript, 32 Vitest files / 401 tests,
and ESLint
- [x] `agents-manager.spec.ts`: 9 Playwright scenarios against the local
mock stack
- [x] Manual review at `http://localhost:3006/agents-manager`

## Size override

This is one cohesive Marketplace information-architecture refactor
spanning the catalog model, three scoped views, shared lookup state,
embedded My Agents cards, mocks, and regression tests. Splitting those
contracts would leave intermediate branches with mismatched UI/data
behavior. The branch exceeds the normal size budget, so this PR requires
the `size-override` label.
```

### PR Body

## Linear

N/A

## Summary

- Refactor Agent Marketplace into independent Public, Shared with me, and My Agents catalogs.
- Keep share-link agents out of Shared with me until they are hired, while preserving installed snapshots if sharing later ends.
- Surface Agent Builder records directly in My Agents with lifecycle badges and ZooClaw Design System card actions.
- Preserve existing public card styling, detail dialogs, install/update/fire flows, and add mock scenarios for all visibility states.
- Add regression coverage for lifecycle rendering, exact shared-workspace updates, install-state loading, bio fallback, dialog embedding, and card keyboard semantics.

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] Targeted `verify-web.sh`: TypeScript, 32 Vitest files / 401 tests, and ESLint
- [x] `agents-manager.spec.ts`: 9 Playwright scenarios against the local mock stack
- [x] Manual review at `http://localhost:3006/agents-manager`

## Size override

This is one cohesive Marketplace information-architecture refactor spanning the catalog model, three scoped views, shared lookup state, embedded My Agents cards, mocks, and regression tests. Splitting those contracts would leave intermediate branches with mismatched UI/data behavior. The branch exceeds the normal size budget, so this PR requires the `size-override` label.


---

## fix(agents): start default main agent after install (#3406)

- **SHA**: `17892c22fe853ce99bdcd868076201f173a340d7`
- **作者**: bill-srp
- **日期**: 2026-08-17T04:01:01Z
- **PR**: #3406

### Commit Message

```
fix(agents): start default main agent after install (#3406)

# What

Start the V2 default main agent on the engine immediately after a fresh
install, instead of leaving it provisioned-but-stopped.

`_install_bare_main_agent` (in
`app/services/agents/engine_main_agent_service.py`) previously called
`client.start_agent(...)` only when reviving a `disabled` workspace row
(`restart_existing`). A brand-new registration created the engine agent,
seeded credentials, bound the Mattermost channel, and marked the row
`active` — but never started the agent. The 2026-07-14 engine design
spec's "active = provisioned, NOT running; no auto-start" behavior is
intentionally changed here for the default main agent per product
decision.

# How

- `start_agent` is now awaited unconditionally after
`seed_engine_agent_credentials` (credentials are seeded right before, so
the engine's `platform_credentials_required` 409 gate is satisfied).
- `restart_existing` keeps its one remaining job: skipping the
Mattermost channel re-bind on revival.
- A start failure propagates unchanged: the row is marked
`install_failed` (reclaimable) and the agents-list `retry_only` path
retries it on the next `GET /agents`, so registration is never blocked.

# Tests (TDD)

- `test_fresh_create_is_bare_and_activates` now asserts `start_agent` is
awaited with the created agent id, and pins seed → start ordering via an
events list.
- `test_reclaimed_engine_row_skips_create_and_starts` (renamed) asserts
a reclaimed installing row is also started.
- New `test_start_failure_marks_install_failed_and_raises` mirrors the
create-failure test for the start step.
- `test_disabled_existing_main_agent_is_started_before_reactivation`
unchanged and passing.

# Test plan

- [x] `bash scripts/verify-py.sh` — ruff, ruff-format, pyright,
import-linter all green
- [x] `pytest tests/unit/test_engine_main_agent_service.py -q` — 12
passed
- [ ] CI (`claw-interface-quality`) green
- [ ] Staging smoke after backend release: register a fresh user,
confirm the main agent reports running without manual start
```

### PR Body

# What

Start the V2 default main agent on the engine immediately after a fresh install, instead of leaving it provisioned-but-stopped.

`_install_bare_main_agent` (in `app/services/agents/engine_main_agent_service.py`) previously called `client.start_agent(...)` only when reviving a `disabled` workspace row (`restart_existing`). A brand-new registration created the engine agent, seeded credentials, bound the Mattermost channel, and marked the row `active` — but never started the agent. The 2026-07-14 engine design spec's "active = provisioned, NOT running; no auto-start" behavior is intentionally changed here for the default main agent per product decision.

# How

- `start_agent` is now awaited unconditionally after `seed_engine_agent_credentials` (credentials are seeded right before, so the engine's `platform_credentials_required` 409 gate is satisfied).
- `restart_existing` keeps its one remaining job: skipping the Mattermost channel re-bind on revival.
- A start failure propagates unchanged: the row is marked `install_failed` (reclaimable) and the agents-list `retry_only` path retries it on the next `GET /agents`, so registration is never blocked.

# Tests (TDD)

- `test_fresh_create_is_bare_and_activates` now asserts `start_agent` is awaited with the created agent id, and pins seed → start ordering via an events list.
- `test_reclaimed_engine_row_skips_create_and_starts` (renamed) asserts a reclaimed installing row is also started.
- New `test_start_failure_marks_install_failed_and_raises` mirrors the create-failure test for the start step.
- `test_disabled_existing_main_agent_is_started_before_reactivation` unchanged and passing.

# Test plan

- [x] `bash scripts/verify-py.sh` — ruff, ruff-format, pyright, import-linter all green
- [x] `pytest tests/unit/test_engine_main_agent_service.py -q` — 12 passed
- [ ] CI (`claw-interface-quality`) green
- [ ] Staging smoke after backend release: register a fresh user, confirm the main agent reports running without manual start


---

## fix(web): update and smooth sidebar logo (#3393)

- **SHA**: `03222a3be6220dfa957f76a501665333a68eb8ef`
- **作者**: lynn Zhuang
- **日期**: 2026-08-17T03:59:31Z
- **PR**: #3393

### Commit Message

```
fix(web): update and smooth sidebar logo (#3393)

## Summary
- replace the expanded web sidebar logo with the supplied ZooWork navy
and white assets for light and dark themes
- keep the collapsed web icon and Electron branding unchanged while
cross-fading persistent logo layers
- synchronize sidebar width and content offset motion, respect
reduced-motion preferences, and compensate the Liquid Glass border for
accurate centering

## Root cause
The expanded and collapsed logo variants were conditionally mounted, so
the compact mark could appear a frame late during the sidebar width
transition. Broad `transition-all` rules also animated unrelated
properties with a different easing curve, while the Liquid Glass border
shifted the apparent center by one pixel.

## Test plan
- [x] `bash scripts/verify-web.sh
web/app/src/components/sidenav/SideNavLogo.tsx
web/app/src/components/sidenav/SideNav.tsx
web/app/src/components/AppLayout.tsx
web/app/tests/unit/components/sidenav/SideNavLogo.unit.spec.tsx`
- [x] `bash scripts/verify-changed.sh`
- [x] manually verified light/dark expanded logos, repeated
collapse/expand transitions, centered collapsed mark, and unchanged
collapsed asset at `http://localhost:3005/chat`
```

### PR Body

## Summary
- replace the expanded web sidebar logo with the supplied ZooWork navy and white assets for light and dark themes
- keep the collapsed web icon and Electron branding unchanged while cross-fading persistent logo layers
- synchronize sidebar width and content offset motion, respect reduced-motion preferences, and compensate the Liquid Glass border for accurate centering

## Root cause
The expanded and collapsed logo variants were conditionally mounted, so the compact mark could appear a frame late during the sidebar width transition. Broad `transition-all` rules also animated unrelated properties with a different easing curve, while the Liquid Glass border shifted the apparent center by one pixel.

## Test plan
- [x] `bash scripts/verify-web.sh web/app/src/components/sidenav/SideNavLogo.tsx web/app/src/components/sidenav/SideNav.tsx web/app/src/components/AppLayout.tsx web/app/tests/unit/components/sidenav/SideNavLogo.unit.spec.tsx`
- [x] `bash scripts/verify-changed.sh`
- [x] manually verified light/dark expanded logos, repeated collapse/expand transitions, centered collapsed mark, and unchanged collapsed asset at `http://localhost:3005/chat`


---
