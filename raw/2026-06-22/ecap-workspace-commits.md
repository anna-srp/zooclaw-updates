# ecap-workspace commits — 2026-06-22

共 8 个 commit

---

## refactor(web): centralize agent service models (#2556)

- **SHA**: `9c88d5794a9df40ccdae94c126354b6ca1cf1329`
- **作者**: bill-srp
- **日期**: 2026-06-22T11:50:52Z
- **PR**: #2556
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/9c88d5794a9df40ccdae94c126354b6ca1cf1329

### 完整 Commit Message

```
refactor(web): centralize agent service models (#2556)

## Summary
- Route computer and computer-agent conversation calls through service
helpers and the shared claw proxy instead of openclaw computer BFF
routes.
- Centralize computer-agent React Query access in `useComputerAgents`.
- Move agent/computer/pack/conversation DTOs into `web/app/src/models`
and remove frontend-derived `AgentPack.id` / `OrgAgentPack.id`.

## Local checks
- `pnpm --dir web/app exec vitest run ...` for affected computer-agent,
conversation, pack, agents-manager, onboarding, deep-link, and
landing-flow tests: passed.
- `pnpm --dir web/app exec eslint ...` for affected files: passed.
- `bash scripts/verify-changed.sh`: failed only at `tsc` because
`GenClawInput.tsx` cannot resolve `ldrs/react`; eslint passed.

## Notes
- `useUserAgents` still uses the legacy `GET /api/openclaw/agents` path.
This PR prepares and centralizes the computer-agent path but does not
replace the main installed-agent facade yet.
```

### PR Body

## Summary
- Route computer and computer-agent conversation calls through service helpers and the shared claw proxy instead of openclaw computer BFF routes.
- Centralize computer-agent React Query access in `useComputerAgents`.
- Move agent/computer/pack/conversation DTOs into `web/app/src/models` and remove frontend-derived `AgentPack.id` / `OrgAgentPack.id`.

## Local checks
- `pnpm --dir web/app exec vitest run ...` for affected computer-agent, conversation, pack, agents-manager, onboarding, deep-link, and landing-flow tests: passed.
- `pnpm --dir web/app exec eslint ...` for affected files: passed.
- `bash scripts/verify-changed.sh`: failed only at `tsc` because `GenClawInput.tsx` cannot resolve `ldrs/react`; eslint passed.

## Notes
- `useUserAgents` still uses the legacy `GET /api/openclaw/agents` path. This PR prepares and centralizes the computer-agent path but does not replace the main installed-agent facade yet.


---

## fix(web): add ECA-1008 connection diagnostics (#2552)

- **SHA**: `f62a3b37b6f37204a3fbfa4ca2e82fc912d593a7`
- **作者**: sharplee-srp
- **日期**: 2026-06-22T11:37:47Z
- **PR**: #2552
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/f62a3b37b6f37204a3fbfa4ca2e82fc912d593a7

### 完整 Commit Message

```
fix(web): add ECA-1008 connection diagnostics (#2552)

## Summary
- Add connection display episode diagnostics with bot, agent, user,
platform readiness, poll metadata, and WS signal fields.
- Add deduped `chat.connection.platform_status_poll_failed` logging to
separate status API failures from explicit `ready:false` platform
responses.
- Propagate route context into chat connection status recording and
extend focused unit coverage.

## Validation
- `pnpm exec vitest run
tests/unit/lib/sentry/connection-status-recorder.unit.spec.ts
tests/unit/lib/sentry/connection-mismatch-monitor.unit.spec.ts
tests/unit/components/ClawConnectionStatus-recorder.unit.spec.tsx
tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx` 70 tests
passed.
- `pnpm exec eslint ...` passed for touched source and test files.
- `pnpm exec tsc --noEmit --project tsconfig.json` passed after clearing
stale local `.next/types` generated before rebase.
- `git diff --check origin/main...HEAD` passed.

## Real staging E2E
- Ran read-only browser E2E against staging bot
`31b7ba01-5b22-4c7c-a3aa-45f0e4def472` with real staging auth, real
staging APIs, real OpenClaw WS, and real Mattermost REST/WS.
- FastClaw preflight showed `running` / `ready`; real
`getComputerStatus` returned HTTP 200 with `ready:true`.
- Verified OpenClaw WS opened, challenge was received, connect was sent,
and handshake completed.
- Verified Mattermost WS opened, hello was received, auth was sent,
`/api/v4/users/me` returned 200, and posts GET returned 200.
- Browser-side read-only injections confirmed envelopes for
`display_episode` start on `ready:false`, `platform_status_poll_failed`
on poll abort, and `display_episode` recovered end after returning to
real status.
- Mutating OpenClaw and Mattermost requests were blocked during the E2E
run.
```

### PR Body

## Summary
- Add connection display episode diagnostics with bot, agent, user, platform readiness, poll metadata, and WS signal fields.
- Add deduped `chat.connection.platform_status_poll_failed` logging to separate status API failures from explicit `ready:false` platform responses.
- Propagate route context into chat connection status recording and extend focused unit coverage.

## Validation
- `pnpm exec vitest run tests/unit/lib/sentry/connection-status-recorder.unit.spec.ts tests/unit/lib/sentry/connection-mismatch-monitor.unit.spec.ts tests/unit/components/ClawConnectionStatus-recorder.unit.spec.tsx tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx` 70 tests passed.
- `pnpm exec eslint ...` passed for touched source and test files.
- `pnpm exec tsc --noEmit --project tsconfig.json` passed after clearing stale local `.next/types` generated before rebase.
- `git diff --check origin/main...HEAD` passed.

## Real staging E2E
- Ran read-only browser E2E against staging bot `31b7ba01-5b22-4c7c-a3aa-45f0e4def472` with real staging auth, real staging APIs, real OpenClaw WS, and real Mattermost REST/WS.
- FastClaw preflight showed `running` / `ready`; real `getComputerStatus` returned HTTP 200 with `ready:true`.
- Verified OpenClaw WS opened, challenge was received, connect was sent, and handshake completed.
- Verified Mattermost WS opened, hello was received, auth was sent, `/api/v4/users/me` returned 200, and posts GET returned 200.
- Browser-side read-only injections confirmed envelopes for `display_episode` start on `ready:false`, `platform_status_poll_failed` on poll abort, and `display_episode` recovered end after returning to real status.
- Mutating OpenClaw and Mattermost requests were blocked during the E2E run.

---

## feat(onboarding): add /welcome first-run 3-step flow (name → role → scenario) (#2502)

- **SHA**: `3db328b83f615acfe378313a2d6f71c68e1aefd7`
- **作者**: lynn Zhuang
- **日期**: 2026-06-22T11:16:10Z
- **PR**: #2502
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/3db328b83f615acfe378313a2d6f71c68e1aefd7

### 完整 Commit Message

```
feat(onboarding): add /welcome first-run 3-step flow (name → role → scenario) (#2502)

## Summary

Adds a new full-screen first-run onboarding flow at `/en/welcome`,
replacing the modal pattern for collecting `name → role → scenario` from
new users. Implemented per Figma nodes 1840-26232 / 1840-26254 /
1840-24672 / 3135-1300 (background).

## What landed

- **Route**: `web/app/src/app/[locale]/welcome/` — `page.tsx` (server,
noindex) + `WelcomeClient.tsx` (client wrapper + step state) + 3 step
components (`NameStep` / `RoleStep` / `ScenarioStep`) +
`wizard-state.ts` (localStorage with 30-min TTL for
resume-after-refresh).
- **Assets**: `web/app/public/welcome/` — 2 role illustration sprite
sheets + 4 scenario SVG icons (sourced from Figma). Background is a CSS
radial gradient (no SVG dependency).
- **Branded palette** registered in `globals.css` `@theme inline` as
`--color-welcome-*` and `--shadow-welcome-cta*` tokens — components stay
100% Tailwind utility classes (`bg-welcome-ink`, `shadow-welcome-cta`,
etc.). No module CSS file.
- **Background gradient** added as a Tailwind v4 `@utility welcome-bg`
block in `globals.css` — composes with all variants.
- **Interactions**: Continue (primary CTA, filled black with subtle
shadow + hover lift), Skip (text link with hover opacity), Back on steps
2/3 (secondary linear button, light gray border matching the cards).
Cards have hover lift + shadow-md + tint.
- **State**: localStorage draft survives reload for 30 min; submit
clears it and routes to `/[locale]/chat`.

## What is intentionally NOT in this PR

- **Backend submission**: `WelcomeClient.finish()` currently
`console.log`s the draft and routes to `/chat`. The `POST
/api/users/onboarding` wiring lands in a follow-up once the contract is
defined.
- **First-time-user auto-redirect to `/welcome`**: middleware / layout
change, broader blast radius, separate PR.
- ~~**i18n**: copy is hardcoded English for now~~ — **DONE**: copy is
now wired through the repo i18n (`useTranslation()` + a `welcome`
section in all 10 locale dictionaries). en + zh are authored; other
locales are first-pass translations to refine (with English fallback for
any missing key).
- **The existing modal-based `OnboardingProvider`** is left untouched —
coexists; can be retired in a later PR after the page replaces it
everywhere.

## Tests

- 35 vitest specs in `web/app/tests/unit/welcome/` covering:
- `wizard-state`: draft round-trip, TTL expiry, malformed JSON fallback,
clear semantics.
- Each step in isolation: render, disabled Continue gating, selection +
emit, prefill from `initial*`, Skip + Back handlers.
- `WelcomeClient`: full happy path (name → role → scenario → /chat),
draft resume on mount, Back from role/scenario preserves state, Skip
clears + routes.
- All 35 pass locally; `verify-web.sh` clean (tsc + eslint + vitest).
- Browser smoke-tested via Playwright (3 steps, hover states, Back
navigation, final submit → /chat redirect).

## Known minor visual issue

- The "Others" role card shows a leaked "Student" caption baked into the
Figma sprite sheet source. Cosmetic; designer can ship per-role clean
icons in a follow-up.

## Test plan

- [ ] CI: `code-quality / lint-and-test` passes
- [ ] CI: `e2e` daily schedule unaffected (no existing routes touched)
- [ ] Manual smoke: hit `/en/welcome`, walk all 3 steps, hit Back, hit
Skip, confirm draft persists across reload within 30 min

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

Adds a new full-screen first-run onboarding flow at `/en/welcome`, replacing the modal pattern for collecting `name → role → scenario` from new users. Implemented per Figma nodes 1840-26232 / 1840-26254 / 1840-24672 / 3135-1300 (background).

## What landed

- **Route**: `web/app/src/app/[locale]/welcome/` — `page.tsx` (server, noindex) + `WelcomeClient.tsx` (client wrapper + step state) + 3 step components (`NameStep` / `RoleStep` / `ScenarioStep`) + `wizard-state.ts` (localStorage with 30-min TTL for resume-after-refresh).
- **Assets**: `web/app/public/welcome/` — 2 role illustration sprite sheets + 4 scenario SVG icons (sourced from Figma). Background is a CSS radial gradient (no SVG dependency).
- **Branded palette** registered in `globals.css` `@theme inline` as `--color-welcome-*` and `--shadow-welcome-cta*` tokens — components stay 100% Tailwind utility classes (`bg-welcome-ink`, `shadow-welcome-cta`, etc.). No module CSS file.
- **Background gradient** added as a Tailwind v4 `@utility welcome-bg` block in `globals.css` — composes with all variants.
- **Interactions**: Continue (primary CTA, filled black with subtle shadow + hover lift), Skip (text link with hover opacity), Back on steps 2/3 (secondary linear button, light gray border matching the cards). Cards have hover lift + shadow-md + tint.
- **State**: localStorage draft survives reload for 30 min; submit clears it and routes to `/[locale]/chat`.

## What is intentionally NOT in this PR

- **Backend submission**: `WelcomeClient.finish()` currently `console.log`s the draft and routes to `/chat`. The `POST /api/users/onboarding` wiring lands in a follow-up once the contract is defined.
- **First-time-user auto-redirect to `/welcome`**: middleware / layout change, broader blast radius, separate PR.
- ~~**i18n**: copy is hardcoded English for now~~ — **DONE**: copy is now wired through the repo i18n (`useTranslation()` + a `welcome` section in all 10 locale dictionaries). en + zh are authored; other locales are first-pass translations to refine (with English fallback for any missing key).
- **The existing modal-based `OnboardingProvider`** is left untouched — coexists; can be retired in a later PR after the page replaces it everywhere.

## Tests

- 35 vitest specs in `web/app/tests/unit/welcome/` covering:
  - `wizard-state`: draft round-trip, TTL expiry, malformed JSON fallback, clear semantics.
  - Each step in isolation: render, disabled Continue gating, selection + emit, prefill from `initial*`, Skip + Back handlers.
  - `WelcomeClient`: full happy path (name → role → scenario → /chat), draft resume on mount, Back from role/scenario preserves state, Skip clears + routes.
- All 35 pass locally; `verify-web.sh` clean (tsc + eslint + vitest).
- Browser smoke-tested via Playwright (3 steps, hover states, Back navigation, final submit → /chat redirect).

## Known minor visual issue

- The "Others" role card shows a leaked "Student" caption baked into the Figma sprite sheet source. Cosmetic; designer can ship per-role clean icons in a follow-up.

## Test plan

- [ ] CI: `code-quality / lint-and-test` passes
- [ ] CI: `e2e` daily schedule unaffected (no existing routes touched)
- [ ] Manual smoke: hit `/en/welcome`, walk all 3 steps, hit Back, hit Skip, confirm draft persists across reload within 30 min



---

## feat(i18n): rename "New Chat" to "New Task" across locales (#2555)

- **SHA**: `30d63edd30b6c7500a1c2fe3b8e0deb75d595b8b`
- **作者**: lynn Zhuang
- **日期**: 2026-06-22T11:14:12Z
- **PR**: #2555
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/30d63edd30b6c7500a1c2fe3b8e0deb75d595b8b

### 完整 Commit Message

```
feat(i18n): rename "New Chat" to "New Task" across locales (#2555)

## What

Renames the sidebar "new conversation" buttons from **New Chat** to
**New Task**:

- Top sidebar button `nav.newChat` → "New Task" (translated across all
11 locales)
- Per-agent button `chat.newChat` → "New task" (en only; other locales
inherit via the English fallback in `LanguageContext`)

## Why

Product terminology shift from "Chat" to "Task" for the primary
new-conversation actions.

## Locale values

| Locale | Before (nav) | After (nav) |
|---|---|---|
| en | New Chat | New Task |
| zh | 新对话 | 新任务 |
| ja | 新しいチャット | 新しいタスク |
| ko | 새 채팅 | 새 작업 |
| de | Neuer Chat | Neue Aufgabe |
| es | Nuevo chat | Nueva tarea |
| fr | Nouvelle discussion | Nouvelle tâche |
| it | Nuova chat | Nuova attività |
| pt | Novo chat | Nova tarefa |
| ar | محادثة جديدة | مهمة جديدة |

## Scope notes

- Only the two highlighted buttons changed. The in-chat composer action
`chat.clearContext` ("Start a new chat") and the `chat.newChatFailed`
toast were intentionally left untouched.
- `chat.newChat` is only defined in `en.ts`; `t()` deep-walks the active
locale and falls back to English for missing keys, so editing `en.ts`
updates that button for all languages.

## Verification

- `bash scripts/verify-web.sh web/app/src/locales` — tsc, vitest (6/6),
eslint all pass
- Manually verified live in the running app (logged-in sidebar): top
button shows "New Task", per-agent button shows "+ New task"
![Uploading 20260622-191034.jpeg…]()

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
```

### PR Body

## What

Renames the sidebar "new conversation" buttons from **New Chat** to **New Task**:

- Top sidebar button `nav.newChat` → "New Task" (translated across all 11 locales)
- Per-agent button `chat.newChat` → "New task" (en only; other locales inherit via the English fallback in `LanguageContext`)

## Why

Product terminology shift from "Chat" to "Task" for the primary new-conversation actions.

## Locale values

| Locale | Before (nav) | After (nav) |
|---|---|---|
| en | New Chat | New Task |
| zh | 新对话 | 新任务 |
| ja | 新しいチャット | 新しいタスク |
| ko | 새 채팅 | 새 작업 |
| de | Neuer Chat | Neue Aufgabe |
| es | Nuevo chat | Nueva tarea |
| fr | Nouvelle discussion | Nouvelle tâche |
| it | Nuova chat | Nuova attività |
| pt | Novo chat | Nova tarefa |
| ar | محادثة جديدة | مهمة جديدة |

## Scope notes

- Only the two highlighted buttons changed. The in-chat composer action `chat.clearContext` ("Start a new chat") and the `chat.newChatFailed` toast were intentionally left untouched.
- `chat.newChat` is only defined in `en.ts`; `t()` deep-walks the active locale and falls back to English for missing keys, so editing `en.ts` updates that button for all languages.

## Verification

- `bash scripts/verify-web.sh web/app/src/locales` — tsc, vitest (6/6), eslint all pass
- Manually verified live in the running app (logged-in sidebar): top button shows "New Task", per-agent button shows "+ New task"
![Uploading 20260622-191034.jpeg…]()


---

## hotfix(bossclaw): sync benefit copy to main (#2549)

- **SHA**: `51a6931629266122127fadaa583604a7b48b1dd9`
- **作者**: tim-srp
- **日期**: 2026-06-22T09:21:11Z
- **PR**: #2549
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/51a6931629266122127fadaa583604a7b48b1dd9

### 完整 Commit Message

```
hotfix(bossclaw): sync benefit copy to main (#2549)

## Summary

- Forward-sync #2542's BossClaw benefit copy fix to main.
- Change displayed benefit from ` Token` to ` credit`.
- Update the focused RedeemStep unit test assertion.

## Scope

Display copy and test assertion only. No API, backend, binding, login,
install, polling, or wizard-state logic changed.

## Testing

- `bash scripts/verify-web.sh 'src/app/[locale]/bossclaw'`
```

### PR Body

## Summary

- Forward-sync #2542's BossClaw benefit copy fix to main.
- Change displayed benefit from ` Token` to ` credit`.
- Update the focused RedeemStep unit test assertion.

## Scope

Display copy and test assertion only. No API, backend, binding, login, install, polling, or wizard-state logic changed.

## Testing

- `bash scripts/verify-web.sh 'src/app/[locale]/bossclaw'`


---

## docs: sync-docs weekly sweep (2026-06-22) (#2550)

- **SHA**: `ee0066df3dd826212c086d60c770a9bb71a7881e`
- **作者**: srp-claude-assistant[bot]
- **日期**: 2026-06-22T09:16:21Z
- **PR**: #2550
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/ee0066df3dd826212c086d60c770a9bb71a7881e

### 完整 Commit Message

```
docs: sync-docs weekly sweep (2026-06-22) (#2550)

## Tier 1 — Deterministic fixes

None. The drift probe (`drift-probe.sh`) found no deterministic drift in
README / version / path / env / workflow tokens.

---

## Tier 2 — Semantic fixes (evidence-grounded, auto-applied)

All changes are in `web/app/AGENTS.md` (symlinked as
`web/app/CLAUDE.md`).

### Fix 1 — R2: all `lib/*-cache.ts` modules have been deleted (was: "5
current imports")
**Evidence:** `9788a2fa8 refactor(web): remove official agent catalog
path (#2547)` deleted `agent-catalog-cache.ts`. `find web/app/src -name
"*-cache.ts"` returns nothing; `grep` finds zero
`eslint-disable-next-line no-restricted-imports` cache entries in the
source tree.
- Removed stale list of deleted filenames (`agent-catalog-cache.ts`,
`openclaw-identity-cache.ts`, `session-cache.ts`) from the
historical-context sentence
- Replaced "5 current `lib/*-cache.ts` imports are tagged..." with
"migration complete as of PR #2547; currently zero surviving
disable-comments"
- The `no-restricted-imports` enforcement rule itself is **kept** — it
prevents regression

### Fix 2 — R2: wrong script name (`check-cache-governance-disables.sh`
→ `check-cache-governance-disables-shrink-only.sh`)
**Evidence:** `ls web/scripts/` shows
`check-cache-governance-disables-shrink-only.sh`; the shorter name never
existed.

### Fix 3 — Zustand migration section:
`custom-agent-publish-draft-store.ts` deleted; status "complete"
**Evidence:** `6a30e38d8 refactor(web): remove private agent catalog
publish path (#2545)` deleted `custom-agent-publish-draft-store.ts`. The
doc still said "are being migrated to the Zustand template".
- Updated prose from "being migrated" to "migration complete"
- Removed `custom-agent-publish-draft-store.ts` from the migration list
(it was deleted, not migrated)

### Fix 4 — `agent-description-store.ts` is Zustand-backed, not
`useSyncExternalStore`-backed
**Evidence:** `web/app/src/lib/agent-description-store.ts` line 1–3
imports `zustand/middleware` / `zustand/vanilla`; line 29 says "Migrated
from a hand-rolled `useSyncExternalStore` template in PR #2074". The
Legitimate storage uses table and Reference reading section both still
said "useSyncExternalStore".

---

## Tier 3 — Suggestions (not applied)

- **`desktop/` not in README structure tree.** `desktop/` (Electron app
`pandaclaw-desktop`) is a top-level directory that predates the anchor
and has received several fixes in this window (`81464d4e1`, `66462b24b`,
`6b4bf6979`). Not added: the README structure tree is focused on the
devcontainer + web + services workflow; desktop is a separate
deliverable. A dedicated section in the README could help onboarding if
the desktop app becomes a primary development surface.
- **CI runners on Blacksmith.** `9b7f82ca8 chore(ci): tier CI runners
onto Blacksmith (#2474)` moved CI off GitHub-hosted runners. No target
doc mentions CI runner types, and CI is intentionally described by
behavior. No doc change needed; noting for awareness.

---

**Docs changed:** `web/app/AGENTS.md` (4 lines)
**Anchor..HEAD window reviewed:**
`a9d070e081a6c4fc7dbc8e6824d0a3e3d1b26c17..HEAD` (77 commits, last 90
days)

Co-authored-by: claude[bot] <41898282+claude[bot]@users.noreply.github.com>
Co-authored-by: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### PR Body

## Tier 1 — Deterministic fixes

None. The drift probe (`drift-probe.sh`) found no deterministic drift in README / version / path / env / workflow tokens.

---

## Tier 2 — Semantic fixes (evidence-grounded, auto-applied)

All changes are in `web/app/AGENTS.md` (symlinked as `web/app/CLAUDE.md`).

### Fix 1 — R2: all `lib/*-cache.ts` modules have been deleted (was: "5 current imports")
**Evidence:** `9788a2fa8 refactor(web): remove official agent catalog path (#2547)` deleted `agent-catalog-cache.ts`. `find web/app/src -name "*-cache.ts"` returns nothing; `grep` finds zero `eslint-disable-next-line no-restricted-imports` cache entries in the source tree.
- Removed stale list of deleted filenames (`agent-catalog-cache.ts`, `openclaw-identity-cache.ts`, `session-cache.ts`) from the historical-context sentence
- Replaced "5 current `lib/*-cache.ts` imports are tagged..." with "migration complete as of PR #2547; currently zero surviving disable-comments"
- The `no-restricted-imports` enforcement rule itself is **kept** — it prevents regression

### Fix 2 — R2: wrong script name (`check-cache-governance-disables.sh` → `check-cache-governance-disables-shrink-only.sh`)
**Evidence:** `ls web/scripts/` shows `check-cache-governance-disables-shrink-only.sh`; the shorter name never existed.

### Fix 3 — Zustand migration section: `custom-agent-publish-draft-store.ts` deleted; status "complete"
**Evidence:** `6a30e38d8 refactor(web): remove private agent catalog publish path (#2545)` deleted `custom-agent-publish-draft-store.ts`. The doc still said "are being migrated to the Zustand template".
- Updated prose from "being migrated" to "migration complete"
- Removed `custom-agent-publish-draft-store.ts` from the migration list (it was deleted, not migrated)

### Fix 4 — `agent-description-store.ts` is Zustand-backed, not `useSyncExternalStore`-backed
**Evidence:** `web/app/src/lib/agent-description-store.ts` line 1–3 imports `zustand/middleware` / `zustand/vanilla`; line 29 says "Migrated from a hand-rolled `useSyncExternalStore` template in PR #2074". The Legitimate storage uses table and Reference reading section both still said "useSyncExternalStore".

---

## Tier 3 — Suggestions (not applied)

- **`desktop/` not in README structure tree.** `desktop/` (Electron app `pandaclaw-desktop`) is a top-level directory that predates the anchor and has received several fixes in this window (`81464d4e1`, `66462b24b`, `6b4bf6979`). Not added: the README structure tree is focused on the devcontainer + web + services workflow; desktop is a separate deliverable. A dedicated section in the README could help onboarding if the desktop app becomes a primary development surface.
- **CI runners on Blacksmith.** `9b7f82ca8 chore(ci): tier CI runners onto Blacksmith (#2474)` moved CI off GitHub-hosted runners. No target doc mentions CI runner types, and CI is intentionally described by behavior. No doc change needed; noting for awareness.

---

**Docs changed:** `web/app/AGENTS.md` (4 lines)
**Anchor..HEAD window reviewed:** `a9d070e081a6c4fc7dbc8e6824d0a3e3d1b26c17..HEAD` (77 commits, last 90 days)


---

## feat(account): add account update endpoint (#2548)

- **SHA**: `ff43b8d885232cd37e4875fe3d4c4d7f84e66442`
- **作者**: bill-srp
- **日期**: 2026-06-22T08:34:36Z
- **PR**: #2548
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/ff43b8d885232cd37e4875fe3d4c4d7f84e66442

### 完整 Commit Message

```
feat(account): add account update endpoint (#2548)

## Summary

- add backend `/account/update` for account-owned preference and
onboarding updates
- migrate frontend data-permission and onboarding completion writes to
`services/account.updateAccount()` through the claw proxy
- remove obsolete frontend `/api/users/update` and
`/api/users/onboarding/complete` BFF routes and tests

## Local checks

- `pnpm --dir web/app exec vitest run
tests/unit/services/account.unit.spec.ts
tests/unit/lib/api/user.unit.spec.ts
tests/unit/components/providers/OnboardingProvider.unit.spec.tsx
tests/unit/lib/auth/manager.unit.spec.ts --config ./vitest.config.mts`
- `bash scripts/verify-web.sh web/app/src/services/account.ts
web/app/src/components/settings/DataPermissionsSection.tsx
web/app/src/components/providers/OnboardingProvider.tsx
web/app/src/lib/api/user.ts
web/app/tests/unit/services/account.unit.spec.ts
web/app/tests/unit/lib/api/user.unit.spec.ts
web/app/tests/unit/components/providers/OnboardingProvider.unit.spec.tsx
web/app/tests/unit/lib/auth/manager.unit.spec.ts`
- `bash scripts/verify-changed.sh` passed frontend checks, but skipped
backend static checks because local `pyright` and `lint-imports` are not
installed
- `bash scripts/verify-py.sh` passed ruff and ruff format, then stopped
because local `pyright` and `lint-imports` are not installed

## Backend local test note

Targeted backend pytest could not run in this local macOS environment:
the system Python has a pytest/pydantic warning-filter mismatch, and `uv
run --project services/claw-interface ...` is blocked by the existing
setuptools parse failure for the bare git dependency in
`requirements.txt`. CI remains the authoritative backend gate.
```

### PR Body

## Summary

- add backend `/account/update` for account-owned preference and onboarding updates
- migrate frontend data-permission and onboarding completion writes to `services/account.updateAccount()` through the claw proxy
- remove obsolete frontend `/api/users/update` and `/api/users/onboarding/complete` BFF routes and tests

## Local checks

- `pnpm --dir web/app exec vitest run tests/unit/services/account.unit.spec.ts tests/unit/lib/api/user.unit.spec.ts tests/unit/components/providers/OnboardingProvider.unit.spec.tsx tests/unit/lib/auth/manager.unit.spec.ts --config ./vitest.config.mts`
- `bash scripts/verify-web.sh web/app/src/services/account.ts web/app/src/components/settings/DataPermissionsSection.tsx web/app/src/components/providers/OnboardingProvider.tsx web/app/src/lib/api/user.ts web/app/tests/unit/services/account.unit.spec.ts web/app/tests/unit/lib/api/user.unit.spec.ts web/app/tests/unit/components/providers/OnboardingProvider.unit.spec.tsx web/app/tests/unit/lib/auth/manager.unit.spec.ts`
- `bash scripts/verify-changed.sh` passed frontend checks, but skipped backend static checks because local `pyright` and `lint-imports` are not installed
- `bash scripts/verify-py.sh` passed ruff and ruff format, then stopped because local `pyright` and `lint-imports` are not installed

## Backend local test note

Targeted backend pytest could not run in this local macOS environment: the system Python has a pytest/pydantic warning-filter mismatch, and `uv run --project services/claw-interface ...` is blocked by the existing setuptools parse failure for the bare git dependency in `requirements.txt`. CI remains the authoritative backend gate.


---

## refactor(web): remove official agent catalog path (#2547)

- **SHA**: `9788a2fa8df51ab0b2a46b2d7985c32f99d145fe`
- **作者**: bill-srp
- **日期**: 2026-06-22T07:10:33Z
- **PR**: #2547
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/9788a2fa8df51ab0b2a46b2d7985c32f99d145fe

### 完整 Commit Message

```
refactor(web): remove official agent catalog path (#2547)

## Summary

- remove the remaining official `/api/openclaw/agent-catalog` BFF route
and frontend API helper
- delete `useOfficialAgentCatalog` and the old `agent-catalog-cache`
sync lookup shim
- remove the official catalog query key from OpenClaw query keys and the
RQ persist allowlist
- keep agent metadata consumers on the existing agent-packs-backed
helpers

Stacked after #2545. This completes the frontend catalog cleanup:
private catalog was removed in #2545, and this PR removes the remaining
official catalog path.

## Test Plan

- `pnpm --dir web/app exec vitest run
tests/unit/hooks/queries/keys.unit.spec.ts
tests/unit/lib/query/persist-client.unit.spec.ts
tests/unit/lib/api/openclaw-extras.unit.spec.ts`
- `pnpm --dir web/app exec vitest run
tests/unit/hooks/queries/keys.unit.spec.ts
tests/unit/lib/query/persist-client.unit.spec.ts
tests/unit/lib/api/openclaw-extras.unit.spec.ts
tests/unit/lib/use-cases.unit.spec.ts
tests/unit/app/chat/ChatQuickActions.unit.spec.tsx
tests/unit/app/new-chat/NewChatClient.unit.spec.tsx
tests/unit/components/sidenav/SideNavAgentList.unit.spec.tsx`
- `bash scripts/verify-web.sh --no-test`
```

### PR Body

## Summary

- remove the remaining official `/api/openclaw/agent-catalog` BFF route and frontend API helper
- delete `useOfficialAgentCatalog` and the old `agent-catalog-cache` sync lookup shim
- remove the official catalog query key from OpenClaw query keys and the RQ persist allowlist
- keep agent metadata consumers on the existing agent-packs-backed helpers

Stacked after #2545. This completes the frontend catalog cleanup: private catalog was removed in #2545, and this PR removes the remaining official catalog path.

## Test Plan

- `pnpm --dir web/app exec vitest run tests/unit/hooks/queries/keys.unit.spec.ts tests/unit/lib/query/persist-client.unit.spec.ts tests/unit/lib/api/openclaw-extras.unit.spec.ts`
- `pnpm --dir web/app exec vitest run tests/unit/hooks/queries/keys.unit.spec.ts tests/unit/lib/query/persist-client.unit.spec.ts tests/unit/lib/api/openclaw-extras.unit.spec.ts tests/unit/lib/use-cases.unit.spec.ts tests/unit/app/chat/ChatQuickActions.unit.spec.tsx tests/unit/app/new-chat/NewChatClient.unit.spec.tsx tests/unit/components/sidenav/SideNavAgentList.unit.spec.tsx`
- `bash scripts/verify-web.sh --no-test`

