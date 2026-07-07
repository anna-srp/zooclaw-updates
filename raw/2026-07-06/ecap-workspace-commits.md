# ecap-workspace — 2026-07-06 commits

共 21 个 commits

---

## feat(pack-store): add public shared pack page and unauthenticated detail API (#2745)

- **SHA**: `1bf24c0c6517a908ada189855ffaeadf7944a12e`
- **作者**: bill-srp
- **日期**: 2026-07-06T13:12:02Z
- **PR**: #2745

### Commit Message

```
feat(pack-store): add public shared pack page and unauthenticated detail API (#2745)

## Linear
<!-- no Linear issue for this feature yet -->

## Summary
- **Public shared-pack page** at `/<locale>/packs/<display_id>` under
the unauthenticated `(marketing)` route group — the landing target for
pack share links (follow-up to #2735). Server component fetches the
backend directly (`fetchSharedPackServer`, mirrors
`chat-replay-server.ts`), so no `middleware.ts` public-allowlist change;
`generateMetadata` emits OG title/description for link unfurls; 404 →
`notFound()`.
- **New unauthenticated API** `GET /agent-packs/shared/{display_id}`:
serves any **active** ZooClaw listing by display_id, **including
`hide_market=true`** (hiding removes a listing from the browsable store,
not from direct links). Returns a strict-allowlist `SharedPackResponse`
(`pack_id`, name, display_id, avatar, category, bios,
skills/integrations/automations, `requires_payment`, derived
`is_official`) — `published_by`, `asset_id`, `origin_*`, `price_id`,
`latest_submission_id` are excluded by schema, with a route test
asserting exclusion and a `create_app` test asserting the mounted route
carries no auth dependency. Agent-studio display_ids are rejected before
the DB read; lookup logic lives in
`app/services/pack_store/shared_listing_service.py`.
- **Style reuse via extraction**: the presentational core of
`AgentDetailClient` (avatar/name/badge/bio/capabilities) is now a shared
`PackDetailView` component with an `actions` slot; the authed detail
page injects its hire/fire/update/chat buttons (behavior unchanged), the
public page injects a hire CTA deep-linking to
`/agents-manager/<display_id>`.
- Design spec:
`docs/superpowers/specs/2026-07-06-shared-pack-public-page-design.md`;
implementation plan:
`docs/superpowers/plans/2026-07-06-shared-pack-public-page.md`.

**Rollout note:** cross-surface — backend must deploy with (or before)
the frontend; during a skew window the page 404s gracefully.

## Test plan
- [x] Backend: `test_shared_listing_service.py` — active listing served,
hidden listing served, missing/non-active/agent-studio →
`pack.not_found`, schema-level sensitive-field disjointness
- [x] Backend: `test_public_agent_packs_routes.py` — no-auth request
succeeds, sensitive fields absent from response JSON, mounted route has
no `get_current_account` dependency
- [x] Frontend: `shared-pack-server.unit.spec.ts`
(200/404/5xx/URL-encoding), `PackDetailView.unit.spec.tsx`
(render/badge/actions/empty rows), `SharedPackClient.unit.spec.tsx` (CTA
link, badge gating)
- [x] `bash scripts/verify-web.sh` — guards + tsc + full vitest (7464
passed) + eslint clean
- [x] Local static: ruff, ruff-format, pyright via pre-commit (deptry /
import-linter / vulture unavailable on host — CI authoritative)
- [ ] CI: `claw-interface-quality` (pytest + coverage ≥90%) +
`web-quality` + `web-build-check`
```

### PR Body

## Linear
<!-- no Linear issue for this feature yet -->

## Summary
- **Public shared-pack page** at `/<locale>/packs/<display_id>` under the unauthenticated `(marketing)` route group — the landing target for pack share links (follow-up to #2735). Server component fetches the backend directly (`fetchSharedPackServer`, mirrors `chat-replay-server.ts`), so no `middleware.ts` public-allowlist change; `generateMetadata` emits OG title/description for link unfurls; 404 → `notFound()`.
- **New unauthenticated API** `GET /agent-packs/shared/{display_id}`: serves any **active** ZooClaw listing by display_id, **including `hide_market=true`** (hiding removes a listing from the browsable store, not from direct links). Returns a strict-allowlist `SharedPackResponse` (`pack_id`, name, display_id, avatar, category, bios, skills/integrations/automations, `requires_payment`, derived `is_official`) — `published_by`, `asset_id`, `origin_*`, `price_id`, `latest_submission_id` are excluded by schema, with a route test asserting exclusion and a `create_app` test asserting the mounted route carries no auth dependency. Agent-studio display_ids are rejected before the DB read; lookup logic lives in `app/services/pack_store/shared_listing_service.py`.
- **Style reuse via extraction**: the presentational core of `AgentDetailClient` (avatar/name/badge/bio/capabilities) is now a shared `PackDetailView` component with an `actions` slot; the authed detail page injects its hire/fire/update/chat buttons (behavior unchanged), the public page injects a hire CTA deep-linking to `/agents-manager/<display_id>`.
- Design spec: `docs/superpowers/specs/2026-07-06-shared-pack-public-page-design.md`; implementation plan: `docs/superpowers/plans/2026-07-06-shared-pack-public-page.md`.

**Rollout note:** cross-surface — backend must deploy with (or before) the frontend; during a skew window the page 404s gracefully.

## Test plan
- [x] Backend: `test_shared_listing_service.py` — active listing served, hidden listing served, missing/non-active/agent-studio → `pack.not_found`, schema-level sensitive-field disjointness
- [x] Backend: `test_public_agent_packs_routes.py` — no-auth request succeeds, sensitive fields absent from response JSON, mounted route has no `get_current_account` dependency
- [x] Frontend: `shared-pack-server.unit.spec.ts` (200/404/5xx/URL-encoding), `PackDetailView.unit.spec.tsx` (render/badge/actions/empty rows), `SharedPackClient.unit.spec.tsx` (CTA link, badge gating)
- [x] `bash scripts/verify-web.sh` — guards + tsc + full vitest (7464 passed) + eslint clean
- [x] Local static: ruff, ruff-format, pyright via pre-commit (deptry / import-linter / vulture unavailable on host — CI authoritative)
- [ ] CI: `claw-interface-quality` (pytest + coverage ≥90%) + `web-quality` + `web-build-check`


---

## fix(dashboard-console): trust backend source submission scope (#2752)

- **SHA**: `02226ec124de11332696985c41d0cebfe062324c`
- **作者**: bill-srp
- **日期**: 2026-07-06T12:49:11Z
- **PR**: #2752

### Commit Message

```
fix(dashboard-console): trust backend source submission scope (#2752)

## Summary
- trust the backend private submission response as the source scope for
dashboard R2 copy
- remove `source_org_id` from the dashboard R2 copy request payload
- use the backend submission org for submit-from-private copy and origin
fields
- allow backend-owned legacy archive keys when R2 metadata matches the
selected private pack
- drop the backend source `asset_id` path-prefix gate for official
submission origins; origin authorization now comes from the internal
private-pack lookup plus org match

## Testing
- `./node_modules/.bin/vitest app/routes/api/r2-copy.test.ts
app/routes/agent-packs/submit-from-private-dialog.test.tsx --run`
- `npm run typecheck`
- `./node_modules/.bin/eslint app/lib/r2-copy.ts
app/routes/api/r2-copy.ts app/routes/api/r2-copy.test.ts
app/routes/agent-packs/submit-from-private-dialog.tsx
app/routes/agent-packs/submit-from-private-dialog.test.tsx`
- `PYTHONPATH=services/claw-interface
/Users/bill/.venvs/claw-interface/bin/pytest
services/claw-interface/tests/unit/test_internal_agent_packs_routes.py
-q`
- `bash scripts/verify-py.sh` partially passed: ruff check, ruff format,
and import-linter passed; pyright failed because
`services/claw-interface/.venv` is missing dependencies such as
`fastapi`, `pytest`, and `favie_common`

## Notes
- `pnpm --dir web/dashboard-console exec vitest ...` is still blocked
before Vitest by `ERR_PNPM_MISSING_TARBALL_INTEGRITY` for
`xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`.
```

### PR Body

## Summary
- trust the backend private submission response as the source scope for dashboard R2 copy
- remove `source_org_id` from the dashboard R2 copy request payload
- use the backend submission org for submit-from-private copy and origin fields
- allow backend-owned legacy archive keys when R2 metadata matches the selected private pack
- drop the backend source `asset_id` path-prefix gate for official submission origins; origin authorization now comes from the internal private-pack lookup plus org match

## Testing
- `./node_modules/.bin/vitest app/routes/api/r2-copy.test.ts app/routes/agent-packs/submit-from-private-dialog.test.tsx --run`
- `npm run typecheck`
- `./node_modules/.bin/eslint app/lib/r2-copy.ts app/routes/api/r2-copy.ts app/routes/api/r2-copy.test.ts app/routes/agent-packs/submit-from-private-dialog.tsx app/routes/agent-packs/submit-from-private-dialog.test.tsx`
- `PYTHONPATH=services/claw-interface /Users/bill/.venvs/claw-interface/bin/pytest services/claw-interface/tests/unit/test_internal_agent_packs_routes.py -q`
- `bash scripts/verify-py.sh` partially passed: ruff check, ruff format, and import-linter passed; pyright failed because `services/claw-interface/.venv` is missing dependencies such as `fastapi`, `pytest`, and `favie_common`

## Notes
- `pnpm --dir web/dashboard-console exec vitest ...` is still blocked before Vitest by `ERR_PNPM_MISSING_TARBALL_INTEGRITY` for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`.


---

## fix(agent-builder): keep validation failures repairable (#2748)

- **SHA**: `dcb28a420e3edc7e11e20990eb5225bffe8e9edd`
- **作者**: kaka-srp
- **日期**: 2026-07-06T11:13:20Z
- **PR**: #2748

### Commit Message

```
fix(agent-builder): keep validation failures repairable (#2748)

## Summary
- send Agent Builder preflight validation failures back into the builder
conversation thread
- keep validation failures repairable by returning the project to
drafting instead of surfacing them as UI errors
- preserve internal iteration failure details for diagnostics

## Tests
- `/home/node/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_agent_builder_service.py::test_run_test_iteration_background_stops_when_preflight_validation_fails
-q`
- `bash scripts/verify-py.sh`
```

### PR Body

## Summary
- send Agent Builder preflight validation failures back into the builder conversation thread
- keep validation failures repairable by returning the project to drafting instead of surfacing them as UI errors
- preserve internal iteration failure details for diagnostics

## Tests
- `/home/node/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_agent_builder_service.py::test_run_test_iteration_background_stops_when_preflight_validation_fails -q`
- `bash scripts/verify-py.sh`


---

## fix(agent-builder): localize builder prompt actions (#2749)

- **SHA**: `23d1bc5d8177a7f711c95f981c1d1ee9be70b3a6`
- **作者**: kaka-srp
- **日期**: 2026-07-06T11:12:48Z
- **PR**: #2749

### Commit Message

```
fix(agent-builder): localize builder prompt actions (#2749)

## Summary

- Update the Agent Builder runtime bootstrap prompt so Builder UI action
names follow the creator language: Chinese UI names for Chinese
conversations, English names otherwise.
- Align Pack Test feedback repair guidance so Chinese users are told to
use `重新打包并测试` instead of the English `Package & Test Again`.
- Pair with Agent Studio prompt pack update:
https://github.com/SerendipityOneInc/ecap-agent-pack/pull/199

## Tests

- `python -m py_compile
services/claw-interface/app/services/agent_builder_service.py`
- `git diff --cached --check`
- pre-push `verify-changed` via `git push`
```

### PR Body

## Summary

- Update the Agent Builder runtime bootstrap prompt so Builder UI action names follow the creator language: Chinese UI names for Chinese conversations, English names otherwise.
- Align Pack Test feedback repair guidance so Chinese users are told to use `重新打包并测试` instead of the English `Package & Test Again`.
- Pair with Agent Studio prompt pack update: https://github.com/SerendipityOneInc/ecap-agent-pack/pull/199

## Tests

- `python -m py_compile services/claw-interface/app/services/agent_builder_service.py`
- `git diff --cached --check`
- pre-push `verify-changed` via `git push`



---

## fix(agent-builder): harden package test gates (#2744)

- **SHA**: `fadb1927664b781e39342d2142bde564fc2d0ae2`
- **作者**: kaka-srp
- **日期**: 2026-07-06T09:23:02Z
- **PR**: #2744

### Commit Message

```
fix(agent-builder): harden package test gates (#2744)

## Summary
- Enforce Agent Builder managed Pack & Test ownership at the
`/pack-test-runs` endpoint with a CAS claim/finalize/release flow.
- Add backend preflight validation before packaging, including
`validate.py --skip-online-validation --pack-test-gate`, metadata
parsing, and duplicate pack version checks.
- Add first-install Agent Studio runtime routing verification with retry
and recoverable reopen behavior.

Linear: https://linear.app/srpone/issue/ECA-1177

## Root cause
Agent Builder could proceed into Pack Test after local validation
errors, and the generic Pack Test endpoint could create runs without
atomically writing `current_test_run_id` back to the Agent Builder
project. Separately, Agent Studio install success did not verify that
the runtime Mattermost routing config was actually active before opening
the builder conversation.

## Test plan
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_agent_builder_service.py
services/claw-interface/tests/unit/test_pack_test_routes.py -q`
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
```

### PR Body

## Summary
- Enforce Agent Builder managed Pack & Test ownership at the `/pack-test-runs` endpoint with a CAS claim/finalize/release flow.
- Add backend preflight validation before packaging, including `validate.py --skip-online-validation --pack-test-gate`, metadata parsing, and duplicate pack version checks.
- Add first-install Agent Studio runtime routing verification with retry and recoverable reopen behavior.

Linear: https://linear.app/srpone/issue/ECA-1177

## Root cause
Agent Builder could proceed into Pack Test after local validation errors, and the generic Pack Test endpoint could create runs without atomically writing `current_test_run_id` back to the Agent Builder project. Separately, Agent Studio install success did not verify that the runtime Mattermost routing config was actually active before opening the builder conversation.

## Test plan
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_agent_builder_service.py services/claw-interface/tests/unit/test_pack_test_routes.py -q`
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`


---

## feat(bossclaw): redesign returning-user login page for PC (#2733)

- **SHA**: `ff11a7a8f944b51159442c4000614e5e05f38ed4`
- **作者**: david-srp
- **日期**: 2026-07-06T08:51:34Z
- **PR**: #2733

### Commit Message

```
feat(bossclaw): redesign returning-user login page for PC (#2733)

## What

Redesign the returning-user login page (`/bossclaw/login`) for **PC**,
matching the established bossclaw brand style. Before, it was the mobile
phone-frame card centered on a big empty desktop screen.

## Design

**Desktop** — one unified, premium canvas (no hard split):
- **Left**: brand hero, reusing the intro-page Hero elements — ZooClaw
logo + 「Boss 专用版」, kicker, gold title 「为决策者而生的 · 专属智能幕僚」, subtitle, and
the 3 stats.
- **Right**: the login form as a **frosted-glass card** floating on the
shared canvas.
- Gold ambient auras span the full width and glow **through** the glass
(bridging both sides); subtle film-grain for depth.

**Mobile** — single-column form card + a compact brand lockup (keeps the
existing mobile UX), same warm ambient glow (toned down for legibility).

## Login-flow feedback ("弹窗")

All the in-flow states are styled to match the PC/bossclaw look:
- **Errors** → a styled notice (red mark + card) instead of bare text;
covers SMS-send failure, wrong code, login failure, the **returning-user
rejection** (`仅支持用户登陆…marketing@zooclaw.ai`), and boss-bind failure.
- **Success** → a login-success card (gold ✓ + 「正在进入 BossClaw 管理工作台…」)
shown during the redirect.
- Loading / resend-cooldown as before.

## Copy

Destination reframed from a "chat space" to a **management console**:
- Title: 登录您的 **BossClaw 管理工作台** (was ZooClaw 聊天空间)
- Button: **进入管理工作台**
- Success: 正在进入 **BossClaw 管理工作台**…
- Added a "还不是 BossClaw 用户？请联系 marketing@zooclaw.ai 申请开通" helper.

## Scope

Frontend / CSS only — **login logic, `return_to` binding, and redirects
are unchanged**. Regenerated the subset fonts for the new copy; updated
the login unit test's button name.

## Testing

- vitest (login-client spec + bossclaw suite) + eslint green.
- Rendered at 1440 / 1680 / 390 px: desktop unified canvas + glass card,
mobile single-column, error notice.

> Note: local `tsc` flags `useSearchParams`/`useParams` as possibly-null
in `RedeemStep.tsx` (untouched) and the original `searchParams.get` in
`BossclawLoginClient` — but the installed next types are non-null and
this exact code is already live on main, so it's a local `.next`-cache
resolution quirk that does not reproduce in CI.

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
```

### PR Body

## What

Redesign the returning-user login page (`/bossclaw/login`) for **PC**, matching the established bossclaw brand style. Before, it was the mobile phone-frame card centered on a big empty desktop screen.

## Design

**Desktop** — one unified, premium canvas (no hard split):
- **Left**: brand hero, reusing the intro-page Hero elements — ZooClaw logo + 「Boss 专用版」, kicker, gold title 「为决策者而生的 · 专属智能幕僚」, subtitle, and the 3 stats.
- **Right**: the login form as a **frosted-glass card** floating on the shared canvas.
- Gold ambient auras span the full width and glow **through** the glass (bridging both sides); subtle film-grain for depth.

**Mobile** — single-column form card + a compact brand lockup (keeps the existing mobile UX), same warm ambient glow (toned down for legibility).

## Login-flow feedback ("弹窗")

All the in-flow states are styled to match the PC/bossclaw look:
- **Errors** → a styled notice (red mark + card) instead of bare text; covers SMS-send failure, wrong code, login failure, the **returning-user rejection** (`仅支持用户登陆…marketing@zooclaw.ai`), and boss-bind failure.
- **Success** → a login-success card (gold ✓ + 「正在进入 BossClaw 管理工作台…」) shown during the redirect.
- Loading / resend-cooldown as before.

## Copy

Destination reframed from a "chat space" to a **management console**:
- Title: 登录您的 **BossClaw 管理工作台** (was ZooClaw 聊天空间)
- Button: **进入管理工作台**
- Success: 正在进入 **BossClaw 管理工作台**…
- Added a "还不是 BossClaw 用户？请联系 marketing@zooclaw.ai 申请开通" helper.

## Scope

Frontend / CSS only — **login logic, `return_to` binding, and redirects are unchanged**. Regenerated the subset fonts for the new copy; updated the login unit test's button name.

## Testing

- vitest (login-client spec + bossclaw suite) + eslint green.
- Rendered at 1440 / 1680 / 390 px: desktop unified canvas + glass card, mobile single-column, error notice.

> Note: local `tsc` flags `useSearchParams`/`useParams` as possibly-null in `RedeemStep.tsx` (untouched) and the original `searchParams.get` in `BossclawLoginClient` — but the installed next types are non-null and this exact code is already live on main, so it's a local `.next`-cache resolution quirk that does not reproduce in CI.


---

## fix(claw-interface): treat noop watcher lease update as success (#2746)

- **SHA**: `c9ea745736103592aab94d1ce6e4b61b1c1b2297`
- **作者**: sam-srp
- **日期**: 2026-07-06T08:51:29Z
- **PR**: #2746

### Commit Message

```
fix(claw-interface): treat noop watcher lease update as success (#2746)

## Summary
- treat watcher lease renewal as successful when Mongo matches the
current owner/status, even if the update is a no-op
- apply the same matched-count semantics to binding lease renewal
- add unit coverage for matched-but-unmodified lease updates

## Why
Staging showed boss Weixin setup watcher jobs being claimed but never
polled. Logs showed repeated `watcher lease extend failed` with
`poll_attempts=0`. The immediate lease renewal can write the same lease
value that `claim_for_watch` just set, causing Mongo to return
`modified_count=0` even though the watcher still owns the lease.

## Validation
- `conda run -n base ruff check
app/database/boss_channel_setup_job_repo.py
tests/unit/test_boss_channel_setup_watcher.py`
- `conda run -n base pytest
tests/unit/test_boss_channel_setup_watcher.py`
```

### PR Body

## Summary
- treat watcher lease renewal as successful when Mongo matches the current owner/status, even if the update is a no-op
- apply the same matched-count semantics to binding lease renewal
- add unit coverage for matched-but-unmodified lease updates

## Why
Staging showed boss Weixin setup watcher jobs being claimed but never polled. Logs showed repeated `watcher lease extend failed` with `poll_attempts=0`. The immediate lease renewal can write the same lease value that `claim_for_watch` just set, causing Mongo to return `modified_count=0` even though the watcher still owns the lease.

## Validation
- `conda run -n base ruff check app/database/boss_channel_setup_job_repo.py tests/unit/test_boss_channel_setup_watcher.py`
- `conda run -n base pytest tests/unit/test_boss_channel_setup_watcher.py`


---

## docs: sync-docs weekly sweep (2026-07-06) (#2743)

- **SHA**: `c69e3bd69967cd53f823506bf7487bc3b0e740a0`
- **作者**: srp-claude-assistant[bot]
- **日期**: 2026-07-06T08:41:15Z
- **PR**: #2743

### Commit Message

```
docs: sync-docs weekly sweep (2026-07-06) (#2743)

## Tier 1 — Deterministic fixes

_Probe reported clean (no path/version/structure hits)._

## Tier 2 — Semantic fixes (evidence-grounded)

- [ ] **`services/whatsapp-business-service/` is now a first-party
in-repo service** (PR #2522, commit `04b3bec42`).
Previously all three docs described the WhatsApp bridge as "an external
WhatsApp Business bridge". The service now lives at
`services/whatsapp-business-service/` in this repo and is built +
deployed by `service-deploy.yml` under the
`whatsapp-business-service-v*` tag family (evidence:
`services/whatsapp-business-service/`,
`.github/workflows/service-deploy.yml` lines 11-14, 72-78, 382-562).

  **Changes applied:**
- `README.md` — Added `whatsapp-business-service-v*` row to the Tag
Conventions table.
- `architecture.md` (Section C, "WhatsApp Business bridge") — Updated
description from "external … bridge" to the in-repo Node.js/Fastify
service; described the bidirectional flow (webhook → Mattermost →
WhatsApp) and the Mattermost WebSocket pool; preserved the
`claw-interface` `/whatsapp` API surface description.
- `architecture.md` (Section D) — Added `whatsapp-business-service`
exception entry with tag prefix, deploy gating vars, and image name.
- `architecture.zh-CN.md` — Identical bilingual edits in both Section C
and Section D.

## Tier 3 — Suggestions (not applied)

- The `services/claw-interface/AGENTS.md` now mentions a `app/watchers/`
package (boss channel setup watcher, added in PR #2701 + #2741). The
top-level architecture docs don't describe watcher-pattern internals —
this is an internal implementation detail best left to the
`claw-interface/AGENTS.md` itself.
- The `dashboard-console` submit-from-private-pack flow (PR #2727) and
pack store public sharing (PR #2735 / PR #2739) are product features
whose routing exists in the architecture already. No architecture-level
entry needed.

---

**Docs changed:** `README.md`, `architecture.md`,
`architecture.zh-CN.md`
**Anchor window reviewed:**
`cd594816eff952a6203155fa7862f12c823f5486..HEAD` (last 90 days, ~277
files, 20 commits)

Co-authored-by: ecap-bot <ecap-bot@users.noreply.github.com>
```

### PR Body

## Tier 1 — Deterministic fixes

_Probe reported clean (no path/version/structure hits)._

## Tier 2 — Semantic fixes (evidence-grounded)

- [ ] **`services/whatsapp-business-service/` is now a first-party in-repo service** (PR #2522, commit `04b3bec42`).  
  Previously all three docs described the WhatsApp bridge as "an external WhatsApp Business bridge". The service now lives at `services/whatsapp-business-service/` in this repo and is built + deployed by `service-deploy.yml` under the `whatsapp-business-service-v*` tag family (evidence: `services/whatsapp-business-service/`, `.github/workflows/service-deploy.yml` lines 11-14, 72-78, 382-562).

  **Changes applied:**
  - `README.md` — Added `whatsapp-business-service-v*` row to the Tag Conventions table.
  - `architecture.md` (Section C, "WhatsApp Business bridge") — Updated description from "external … bridge" to the in-repo Node.js/Fastify service; described the bidirectional flow (webhook → Mattermost → WhatsApp) and the Mattermost WebSocket pool; preserved the `claw-interface` `/whatsapp` API surface description.
  - `architecture.md` (Section D) — Added `whatsapp-business-service` exception entry with tag prefix, deploy gating vars, and image name.
  - `architecture.zh-CN.md` — Identical bilingual edits in both Section C and Section D.

## Tier 3 — Suggestions (not applied)

- The `services/claw-interface/AGENTS.md` now mentions a `app/watchers/` package (boss channel setup watcher, added in PR #2701 + #2741). The top-level architecture docs don't describe watcher-pattern internals — this is an internal implementation detail best left to the `claw-interface/AGENTS.md` itself.
- The `dashboard-console` submit-from-private-pack flow (PR #2727) and pack store public sharing (PR #2735 / PR #2739) are product features whose routing exists in the architecture already. No architecture-level entry needed.

---

**Docs changed:** `README.md`, `architecture.md`, `architecture.zh-CN.md`  
**Anchor window reviewed:** `cd594816eff952a6203155fa7862f12c823f5486..HEAD` (last 90 days, ~277 files, 20 commits)


---

## fix(claw-interface): add boss channel setup watcher logging (#2741)

- **SHA**: `07f0433789b1bf3f30d5950124b3ed1843054d46`
- **作者**: sam-srp
- **日期**: 2026-07-06T08:26:21Z
- **PR**: #2741

### Commit Message

```
fix(claw-interface): add boss channel setup watcher logging (#2741)

## Summary
- log uncaught boss channel setup watcher task failures with tracebacks
- add watcher lifecycle logs around claim, lease, sleep, poll, and
terminal exits
- add unit coverage for tracked task exception logging

## Why
We saw Weixin setup jobs repeatedly claim watcher leases but expire with
`poll_attempts=0`, leaving no traceback or actionable reason. These logs
make the next occurrence diagnosable.

## Validation
- `conda run -n base ruff check
app/watchers/boss_channel_setup_watcher.py
tests/unit/test_boss_channel_setup_watcher.py`
- `conda run -n base pytest
tests/unit/test_boss_channel_setup_watcher.py`
```

### PR Body

## Summary
- log uncaught boss channel setup watcher task failures with tracebacks
- add watcher lifecycle logs around claim, lease, sleep, poll, and terminal exits
- add unit coverage for tracked task exception logging

## Why
We saw Weixin setup jobs repeatedly claim watcher leases but expire with `poll_attempts=0`, leaving no traceback or actionable reason. These logs make the next occurrence diagnosable.

## Validation
- `conda run -n base ruff check app/watchers/boss_channel_setup_watcher.py tests/unit/test_boss_channel_setup_watcher.py`
- `conda run -n base pytest tests/unit/test_boss_channel_setup_watcher.py`


---

## docs(review): require recoverability check before calling states stuck (#2740)

- **SHA**: `2b3c26ec371dee0af191de05c997953f82f4bf4a`
- **作者**: bill-srp
- **日期**: 2026-07-06T07:58:00Z
- **PR**: #2740

### Commit Message

```
docs(review): require recoverability check before calling states stuck (#2740)

## Summary
- Extend the "Atomicity & compensation" bullet in `code-review.md` (the
per-project AI review guide read by the Codex/Claude auto-review):
before a finding describes a partial-write state as "stuck", "hidden",
or "unrecoverable", the reviewer must check whether an existing flow
(admin review queue, reconcile cron, retry endpoint) already surfaces
and repairs that state — and if so, describe it as "blocked until that
flow completes" and weigh severity accordingly.
- Motivation: on PR #2735 the Codex review flagged an active-listing
reshare failure window as a high-risk "stuck retry path" with a "hidden
pending submission". Verification showed the pending submission is
visible in the normal admin review queue
(`pack_submission_repo.list_by_org` filters submission status, not pack
status) and the approve transaction force-syncs the pack regardless of
its stuck status — the state self-heals through the standard review
flow. The verdict routing (NEED_HUMAN_REVIEW) was correct; only the
severity narrative was overstated. This tweak targets that narrative
without loosening the escalation ladder.

## Test plan
- [x] Docs-only change; no runtime surface. The guide is read from the
base branch by `srp-actions/codex-review.yaml`, so it takes effect on
PRs opened after this merges.
```

### PR Body

## Summary
- Extend the "Atomicity & compensation" bullet in `code-review.md` (the per-project AI review guide read by the Codex/Claude auto-review): before a finding describes a partial-write state as "stuck", "hidden", or "unrecoverable", the reviewer must check whether an existing flow (admin review queue, reconcile cron, retry endpoint) already surfaces and repairs that state — and if so, describe it as "blocked until that flow completes" and weigh severity accordingly.
- Motivation: on PR #2735 the Codex review flagged an active-listing reshare failure window as a high-risk "stuck retry path" with a "hidden pending submission". Verification showed the pending submission is visible in the normal admin review queue (`pack_submission_repo.list_by_org` filters submission status, not pack status) and the approve transaction force-syncs the pack regardless of its stuck status — the state self-heals through the standard review flow. The verdict routing (NEED_HUMAN_REVIEW) was correct; only the severity narrative was overstated. This tweak targets that narrative without loosening the escalation ladder.

## Test plan
- [x] Docs-only change; no runtime surface. The guide is read from the base branch by `srp-actions/codex-review.yaml`, so it takes effect on PRs opened after this merges.


---

## feat(pack-store): add public listing share flow (#2735)

- **SHA**: `039636e11a4e93d77b9ba17cf95059b9eb013953`
- **作者**: bill-srp
- **日期**: 2026-07-06T07:46:48Z
- **PR**: #2735

### Commit Message

```
feat(pack-store): add public listing share flow (#2735)

## Linear


## Summary
- add public/free listing creation and listing-state endpoints alongside
the existing paid listing flow
- add listing visibility controls (`hide_market`) for shared packs,
including repository update support and public listing UI
- extend publish UI services, hooks, modal flow, localized copy, and
unit coverage for sharing private packs publicly

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`
- [x] `cd services/claw-interface &&
PATH=/Users/bill/.venvs/claw-interface/bin:$PATH pytest
tests/unit/test_pack_repo.py tests/unit/test_pack_services.py
tests/unit/test_routes_pack_store.py
tests/unit/test_public_listing_service.py -q`
- [x] `cd web/app && corepack pnpm exec tsc --noEmit`
- [x] `cd web/app && corepack pnpm exec eslint
'src/app/[locale]/(app)/(chat)/agents-manager/publish'
src/hooks/useOrgPackListing.ts src/services/org-agent-packs.ts
src/models/org-agent-pack.ts`
- [x] `cd web/app && corepack pnpm exec vitest run
tests/unit/app/agents-manager-publish.unit.spec.tsx
tests/unit/services/org-agent-packs.unit.spec.ts
tests/unit/hooks/useOrgPackListing.unit.spec.ts --passWithNoTests`

Note: `bash scripts/verify-web.sh --no-test ...` was blocked locally
because the PATH `pnpm` is 11.7.0 while this workspace declares
`pnpm@10.26.2`; the equivalent tsc/eslint/vitest checks above were run
with Corepack using the project-declared pnpm version.
```

### PR Body

## Linear


## Summary
- add public/free listing creation and listing-state endpoints alongside the existing paid listing flow
- add listing visibility controls (`hide_market`) for shared packs, including repository update support and public listing UI
- extend publish UI services, hooks, modal flow, localized copy, and unit coverage for sharing private packs publicly

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`
- [x] `cd services/claw-interface && PATH=/Users/bill/.venvs/claw-interface/bin:$PATH pytest tests/unit/test_pack_repo.py tests/unit/test_pack_services.py tests/unit/test_routes_pack_store.py tests/unit/test_public_listing_service.py -q`
- [x] `cd web/app && corepack pnpm exec tsc --noEmit`
- [x] `cd web/app && corepack pnpm exec eslint 'src/app/[locale]/(app)/(chat)/agents-manager/publish' src/hooks/useOrgPackListing.ts src/services/org-agent-packs.ts src/models/org-agent-pack.ts`
- [x] `cd web/app && corepack pnpm exec vitest run tests/unit/app/agents-manager-publish.unit.spec.tsx tests/unit/services/org-agent-packs.unit.spec.ts tests/unit/hooks/useOrgPackListing.unit.spec.ts --passWithNoTests`

Note: `bash scripts/verify-web.sh --no-test ...` was blocked locally because the PATH `pnpm` is 11.7.0 while this workspace declares `pnpm@10.26.2`; the equivalent tsc/eslint/vitest checks above were run with Corepack using the project-declared pnpm version.


---

## fix(theme): bootstrap dark mode before hydration (#2720)

- **SHA**: `3f6d03ee395365162e7c4cfdf172a433df7a6912`
- **作者**: lynn Zhuang
- **日期**: 2026-07-06T07:38:49Z
- **PR**: #2720

### Commit Message

```
fix(theme): bootstrap dark mode before hydration (#2720)

## Summary
- Add a head bootstrap script that mirrors next-themes class mode before
hydration.
- Share the ecap-theme storage key between ThemeProvider and the
bootstrap script.
- Apply the same theme-mode bootstrap to standalone /share and /about
root layouts.
- Cover dark, light, system, missing storage, storage-error, and
matchMedia-error behavior in unit tests.

## Root cause
The app dark variant depends on html.dark, but the App Router locale
layout only bootstrapped the brand theme before hydration. next-themes
persisted ecap-theme correctly, but its client provider runs from the
body, so a refresh could paint before html.dark was applied. Standalone
root layouts also need the same pre-hydration class bootstrap because
they bypass the locale layout and ThemeProvider.

## Test plan
- [x] corepack pnpm exec vitest run --config ./vitest.config.mts
tests/unit/app/_brand-bootstrap.unit.spec.ts
- [x] corepack pnpm exec tsc --noEmit
- [x] corepack pnpm exec eslint src/app/_brand-bootstrap.ts
src/app/[locale]/layout.tsx src/app/share/layout.tsx
src/app/about/layout.tsx src/components/providers/ThemeProvider.tsx
src/theme/theme-mode.ts tests/unit/app/_brand-bootstrap.unit.spec.ts
- [x] git diff --check
- [x] web governance guard scripts

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
```

### PR Body

## Summary
- Add a head bootstrap script that mirrors next-themes class mode before hydration.
- Share the ecap-theme storage key between ThemeProvider and the bootstrap script.
- Apply the same theme-mode bootstrap to standalone /share and /about root layouts.
- Cover dark, light, system, missing storage, storage-error, and matchMedia-error behavior in unit tests.

## Root cause
The app dark variant depends on html.dark, but the App Router locale layout only bootstrapped the brand theme before hydration. next-themes persisted ecap-theme correctly, but its client provider runs from the body, so a refresh could paint before html.dark was applied. Standalone root layouts also need the same pre-hydration class bootstrap because they bypass the locale layout and ThemeProvider.

## Test plan
- [x] corepack pnpm exec vitest run --config ./vitest.config.mts tests/unit/app/_brand-bootstrap.unit.spec.ts
- [x] corepack pnpm exec tsc --noEmit
- [x] corepack pnpm exec eslint src/app/_brand-bootstrap.ts src/app/[locale]/layout.tsx src/app/share/layout.tsx src/app/about/layout.tsx src/components/providers/ThemeProvider.tsx src/theme/theme-mode.ts tests/unit/app/_brand-bootstrap.unit.spec.ts
- [x] git diff --check
- [x] web governance guard scripts


---

## fix(dashboard-console): split r2 source mismatch errors (#2739)

- **SHA**: `5071ac2080c91e4b72ab2ca5a162af9dc2a1261c`
- **作者**: bill-srp
- **日期**: 2026-07-06T06:30:19Z
- **PR**: #2739

### Commit Message

```
fix(dashboard-console): split r2 source mismatch errors (#2739)

## Summary

- Split the dashboard-console `/api/r2/copy` source-submission mismatch
guard into specific 403 codes/messages.
- Preserve the internal source-submission lookup and Worker-side R2 copy
behavior from #2738.
- Add route tests for asset scope mismatch, unapproved submission, org
mismatch, and missing archive key responses.

## Testing

- Blocked locally: `pnpm --dir web/dashboard-console exec vitest
app/routes/api/r2-copy.test.ts --run`
- Local pnpm dependency check fails before Vitest starts with
`ERR_PNPM_MISSING_TARBALL_INTEGRITY` for
`xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`.
```

### PR Body

## Summary

- Split the dashboard-console `/api/r2/copy` source-submission mismatch guard into specific 403 codes/messages.
- Preserve the internal source-submission lookup and Worker-side R2 copy behavior from #2738.
- Add route tests for asset scope mismatch, unapproved submission, org mismatch, and missing archive key responses.

## Testing

- Blocked locally: `pnpm --dir web/dashboard-console exec vitest app/routes/api/r2-copy.test.ts --run`
  - Local pnpm dependency check fails before Vitest starts with `ERR_PNPM_MISSING_TARBALL_INTEGRITY` for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`.


---

## chore: upgrade claude code action (#2737)

- **SHA**: `4ae765762e5268ae020b7e7815ad1ef8f44f6082`
- **作者**: Chris@ZooClaw
- **日期**: 2026-07-06T06:22:36Z
- **PR**: #2737

### Commit Message

```
chore: upgrade claude code action (#2737)

## Summary
- upgrade direct ecap Claude Code Action callers to
anthropics/claude-code-action@v1.0.165
- pass Bedrock model selection through claude_args instead of
ANTHROPIC_MODEL
- restore srp-actions reusable workflow refs to @main now that
SerendipityOneInc/srp-actions#118 has merged

## Validation
- Ruby Psych parsed changed workflow YAML files
- actionlint passed with the existing runner/shellcheck ignores
- git diff --check passed
- tested srp-actions#118 from this PR before merge, including Opus 4.8
with --effort high and release-notify dry-run

## Notes
- srp-actions#118 is merged, so this PR no longer points at a temporary
srp-actions branch.
```

### PR Body

## Summary
- upgrade direct ecap Claude Code Action callers to anthropics/claude-code-action@v1.0.165
- pass Bedrock model selection through claude_args instead of ANTHROPIC_MODEL
- restore srp-actions reusable workflow refs to @main now that SerendipityOneInc/srp-actions#118 has merged

## Validation
- Ruby Psych parsed changed workflow YAML files
- actionlint passed with the existing runner/shellcheck ignores
- git diff --check passed
- tested srp-actions#118 from this PR before merge, including Opus 4.8 with --effort high and release-notify dry-run

## Notes
- srp-actions#118 is merged, so this PR no longer points at a temporary srp-actions branch.

---

## fix(dashboard-console): validate r2 copy sources via internal api (#2738)

- **SHA**: `2a39b5b406e623e6a77fe55eb02a5ff4522475fb`
- **作者**: bill-srp
- **日期**: 2026-07-06T06:05:02Z
- **PR**: #2738

### Commit Message

```
fix(dashboard-console): validate r2 copy sources via internal api (#2738)

## Summary

- Switch dashboard-console `/api/r2/copy` source-submission validation
from the org-scoped pack versions API to the existing internal
private-pack submission API.
- Keep the actual R2 copy in the dashboard Worker and preserve the local
source org/pack/status/key/metadata checks.
- Update the route unit test mocks and URL assertion for the internal `{
submission }` response shape.

## Testing

- Blocked: `pnpm --dir web/dashboard-console exec vitest
app/routes/api/r2-copy.test.ts --run`
- Local pnpm dependency check fails before Vitest starts with
`ERR_PNPM_MISSING_TARBALL_INTEGRITY` for
`xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`.
```

### PR Body

## Summary

- Switch dashboard-console `/api/r2/copy` source-submission validation from the org-scoped pack versions API to the existing internal private-pack submission API.
- Keep the actual R2 copy in the dashboard Worker and preserve the local source org/pack/status/key/metadata checks.
- Update the route unit test mocks and URL assertion for the internal `{ submission }` response shape.

## Testing

- Blocked: `pnpm --dir web/dashboard-console exec vitest app/routes/api/r2-copy.test.ts --run`
  - Local pnpm dependency check fails before Vitest starts with `ERR_PNPM_MISSING_TARBALL_INTEGRITY` for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`.


---

## fix(web): suppress expected account-bootstrap 404 and firebase assertion noise in Sentry (#2651)

- **SHA**: `65b23b72096d6c1a97e0822b6f4312c3cfc0e7fb`
- **作者**: Chris@ZooClaw
- **日期**: 2026-07-06T04:29:16Z
- **PR**: #2651

### Commit Message

```
fix(web): suppress expected account-bootstrap 404 and firebase assertion noise in Sentry (#2651)

## Summary

Three reporting-layer telemetry-hygiene fixes in
`web/app/sentry.client.config.ts`. All suppress expected /
non-actionable Sentry noise **at the reporting layer only** — no change
to live app behavior, the backend contract, or
`httpClientIntegration.failedRequestStatusCodes`.

### ECA-1053 — account-bootstrap 404 leaks as a Sentry issue
`GET /api/claw/account/me` deliberately returns `404
{"code":"account.not_found"}` during the post-login account-bootstrap
race. The frontend already handles it (`useAccountMeQuery` retries;
`manager._createAndSyncUser` registers the personal org).
`EXPECTED_HTTP_ERRORS` had the `401` `/account/me` entry but no `404`
one, so the 404 variant leaked as signature `http_404:claw_account_me`
(114 events / 21 users).

Fix: one new allowlist entry, right after the existing 401 `/account/me`
entry, mirroring its shape. Narrow by status + URL — unexpected 404s on
other endpoints stay visible.

Linear: https://linear.app/srpone/issue/ECA-1053

### ECA-1049 — Firebase upstream internal-assertion noise
`@firebase/auth INTERNAL ASSERTION FAILED: Pending promise was never
set` is a known non-actionable upstream firebase-js-sdk race (userCount
0). New `beforeSend` rule (mirrors the ECA-684 browser-injected-script
handling): **downgrades** matching events to `level: 'warning'` and
collapses them under a single `['firebase-internal-assertion']`
fingerprint. Deliberately not dropped outright, so a real post-deploy
spike stays visible.

Linear: https://linear.app/srpone/issue/ECA-1049

### ECA-1102 — staging client-navigation "Failed to fetch" noise
`TypeError: Failed to fetch` thrown inside Next's client router
(`fetchServerResponse`) on staging hosts. Next already degrades to a
full-page navigation, so it is non-actionable. The config deliberately
keeps own-domain "Failed to fetch" visible for production diagnostics,
so the filter is **narrow**: it drops only when the throw site is Next's
`fetchServerResponse` **and** the env/host is staging
(`NEXT_PUBLIC_APP_ENV === 'staging'` or hostname matches the `_seo.ts`
`STAGING_HOST_MARKERS`). Production own-domain "Failed to fetch" is
never dropped.

Linear: https://linear.app/srpone/issue/ECA-1102

## Tests

Added vitest coverage to
`tests/unit/config/sentry-client-config.unit.spec.ts`:
- 404 `/account/me` event dropped; an unexpected 404 on another
`/account/*` endpoint kept.
- Firebase assertion event downgraded to `warning` under the single
fingerprint (not dropped); unrelated firebase errors untouched.
- Staging `fetchServerResponse` "Failed to fetch" dropped; production
own-domain one kept; a non-router "Failed to fetch" kept even on
staging.

`bash scripts/verify-web.sh` (guards + tsc + vitest + eslint) passes —
43/43 tests green.

## Risk
Reporting-layer only. No backend contract change, no
`failedRequestStatusCodes` change, no live UX change.

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

Three reporting-layer telemetry-hygiene fixes in `web/app/sentry.client.config.ts`. All suppress expected / non-actionable Sentry noise **at the reporting layer only** — no change to live app behavior, the backend contract, or `httpClientIntegration.failedRequestStatusCodes`.

### ECA-1053 — account-bootstrap 404 leaks as a Sentry issue
`GET /api/claw/account/me` deliberately returns `404 {"code":"account.not_found"}` during the post-login account-bootstrap race. The frontend already handles it (`useAccountMeQuery` retries; `manager._createAndSyncUser` registers the personal org). `EXPECTED_HTTP_ERRORS` had the `401` `/account/me` entry but no `404` one, so the 404 variant leaked as signature `http_404:claw_account_me` (114 events / 21 users).

Fix: one new allowlist entry, right after the existing 401 `/account/me` entry, mirroring its shape. Narrow by status + URL — unexpected 404s on other endpoints stay visible.

Linear: https://linear.app/srpone/issue/ECA-1053

### ECA-1049 — Firebase upstream internal-assertion noise
`@firebase/auth INTERNAL ASSERTION FAILED: Pending promise was never set` is a known non-actionable upstream firebase-js-sdk race (userCount 0). New `beforeSend` rule (mirrors the ECA-684 browser-injected-script handling): **downgrades** matching events to `level: 'warning'` and collapses them under a single `['firebase-internal-assertion']` fingerprint. Deliberately not dropped outright, so a real post-deploy spike stays visible.

Linear: https://linear.app/srpone/issue/ECA-1049

### ECA-1102 — staging client-navigation "Failed to fetch" noise
`TypeError: Failed to fetch` thrown inside Next's client router (`fetchServerResponse`) on staging hosts. Next already degrades to a full-page navigation, so it is non-actionable. The config deliberately keeps own-domain "Failed to fetch" visible for production diagnostics, so the filter is **narrow**: it drops only when the throw site is Next's `fetchServerResponse` **and** the env/host is staging (`NEXT_PUBLIC_APP_ENV === 'staging'` or hostname matches the `_seo.ts` `STAGING_HOST_MARKERS`). Production own-domain "Failed to fetch" is never dropped.

Linear: https://linear.app/srpone/issue/ECA-1102

## Tests

Added vitest coverage to `tests/unit/config/sentry-client-config.unit.spec.ts`:
- 404 `/account/me` event dropped; an unexpected 404 on another `/account/*` endpoint kept.
- Firebase assertion event downgraded to `warning` under the single fingerprint (not dropped); unrelated firebase errors untouched.
- Staging `fetchServerResponse` "Failed to fetch" dropped; production own-domain one kept; a non-router "Failed to fetch" kept even on staging.

`bash scripts/verify-web.sh` (guards + tsc + vitest + eslint) passes — 43/43 tests green.

## Risk
Reporting-layer only. No backend contract change, no `failedRequestStatusCodes` change, no live UX change.


---

## style(app): unify glass shell panels (#2722)

- **SHA**: `7b80a1319da9f75de7167cf83405aa90ff0eade3`
- **作者**: lynn Zhuang
- **日期**: 2026-07-06T03:43:23Z
- **PR**: #2722

### Commit Message

```
style(app): unify glass shell panels (#2722)

## Summary
- 统一 Agent Builder、Schedule、AI Specialists
Hub、Settings/Profile、Connector 等页面的右侧全局玻璃主面板样式，内部页面背景在 glass shell
下改为透明，避免盖住全局框架。
- 替换侧边栏收起态 logo，补上 profile 入口 hover 降低透明度效果，并移除 chat 内容区额外背景层/底纹。
- 补充本地 mock 登录态自动恢复，顺带加一个很小的 Bossclaw nullable route params guard，用来解除最新
main 上的 tsc 阻塞。

## Test plan
- [x] `bash scripts/verify-web.sh ...` targeted check: 18 files / 240
tests passed, tsc and eslint passed.
- [x] Browser preview on `http://localhost:3003`: verified Agent
Builder, Schedule, AI Specialists Hub, Settings/Profile, Connector share
the same panel computed styles.
- [x] `bash scripts/verify-changed.sh`

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>
```

### PR Body

## Summary
- 统一 Agent Builder、Schedule、AI Specialists Hub、Settings/Profile、Connector 等页面的右侧全局玻璃主面板样式，内部页面背景在 glass shell 下改为透明，避免盖住全局框架。
- 替换侧边栏收起态 logo，补上 profile 入口 hover 降低透明度效果，并移除 chat 内容区额外背景层/底纹。
- 补充本地 mock 登录态自动恢复，顺带加一个很小的 Bossclaw nullable route params guard，用来解除最新 main 上的 tsc 阻塞。

## Test plan
- [x] `bash scripts/verify-web.sh ...` targeted check: 18 files / 240 tests passed, tsc and eslint passed.
- [x] Browser preview on `http://localhost:3003`: verified Agent Builder, Schedule, AI Specialists Hub, Settings/Profile, Connector share the same panel computed styles.
- [x] `bash scripts/verify-changed.sh`


---

## feat: refresh boss channel setup status in backend (#2701)

- **SHA**: `513e495fe75cecbef9d41cc9532a03869d24ff8c`
- **作者**: sam-srp
- **日期**: 2026-07-06T03:40:23Z
- **PR**: #2701

### Commit Message

```
feat: refresh boss channel setup status in backend (#2701)

## Summary
- remove the public boss key to boss name lookup endpoint and frontend
proxy from this branch
- keep the backend boss channel setup job watcher/status refresh flow
- keep boss info binding compatibility for existing cold-start setup

## Tests
- conda run -n base ruff check app/routes/zooclaw_boss_info.py
app/schema/zooclaw_boss_info.py app/database/zooclaw_boss_info_repo.py
tests/unit/test_zooclaw_boss_info.py
- PYTHONPATH=~/favie/favie-common conda run -n base pyright
app/routes/zooclaw_boss_info.py app/schema/zooclaw_boss_info.py
app/database/zooclaw_boss_info_repo.py
tests/unit/test_zooclaw_boss_info.py
- conda run -n base pytest tests/unit/test_zooclaw_boss_info.py -q
- conda run -n base pytest tests/unit/test_boss_channel_setup_watcher.py
tests/unit/test_openclaw_settings_wecom.py -q
- conda run -n base pytest tests/unit/test_openclaw_settings_routes.py
-k "weixin_setup or weixin_poll or weixin_cancel or weixin_session" -q

## Local note
- frontend targeted vitest could not run locally because pnpm install
fails on the existing xlsx tarball integrity lockfile issue.
```

### PR Body

## Summary
- remove the public boss key to boss name lookup endpoint and frontend proxy from this branch
- keep the backend boss channel setup job watcher/status refresh flow
- keep boss info binding compatibility for existing cold-start setup

## Tests
- conda run -n base ruff check app/routes/zooclaw_boss_info.py app/schema/zooclaw_boss_info.py app/database/zooclaw_boss_info_repo.py tests/unit/test_zooclaw_boss_info.py
- PYTHONPATH=~/favie/favie-common conda run -n base pyright app/routes/zooclaw_boss_info.py app/schema/zooclaw_boss_info.py app/database/zooclaw_boss_info_repo.py tests/unit/test_zooclaw_boss_info.py
- conda run -n base pytest tests/unit/test_zooclaw_boss_info.py -q
- conda run -n base pytest tests/unit/test_boss_channel_setup_watcher.py tests/unit/test_openclaw_settings_wecom.py -q
- conda run -n base pytest tests/unit/test_openclaw_settings_routes.py -k "weixin_setup or weixin_poll or weixin_cancel or weixin_session" -q

## Local note
- frontend targeted vitest could not run locally because pnpm install fails on the existing xlsx tarball integrity lockfile issue.

---

## feat(ios): prepare ZooClaw 1.8.0 (#2734)

- **SHA**: `3af1a6c7c88dfc5694ac1ffea1338918e561a3ee`
- **作者**: bill-srp
- **日期**: 2026-07-06T03:33:13Z
- **PR**: #2734

### Commit Message

```
feat(ios): prepare ZooClaw 1.8.0 (#2734)

## Summary

- Prepare the ZooClaw iOS 1.8.0 branch for review.
- Move iOS bot/account flows onto the current computer-scoped APIs and
remove stale wrappers.
- Add conversation session/thread UI and Mattermost thread routing.
- Refresh launch/onboarding assets, app icon, and subscription/status
handling.

## Validation

- `swiftlint`
- `xcodebuild -project ZooClaw.xcodeproj -scheme ZooClaw -destination
'platform=iOS Simulator,name=iPhone 17 Pro' build`
- `bash scripts/verify-changed.sh` returned no locally verifiable
surfaces for this iOS-only diff.
- `git merge-tree --write-tree HEAD origin/main` completed without
conflicts.

## Notes

- `xcodebuild -project ZooClaw.xcodeproj -scheme ZooClaw -destination
'platform=macOS' build` could not run locally because the current
`ZooClaw` scheme exposes no macOS destination in this checkout.

---------

Co-authored-by: shana-srp <shana@srp.one>
Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Body

## Summary

- Prepare the ZooClaw iOS 1.8.0 branch for review.
- Move iOS bot/account flows onto the current computer-scoped APIs and remove stale wrappers.
- Add conversation session/thread UI and Mattermost thread routing.
- Refresh launch/onboarding assets, app icon, and subscription/status handling.

## Validation

- `swiftlint`
- `xcodebuild -project ZooClaw.xcodeproj -scheme ZooClaw -destination 'platform=iOS Simulator,name=iPhone 17 Pro' build`
- `bash scripts/verify-changed.sh` returned no locally verifiable surfaces for this iOS-only diff.
- `git merge-tree --write-tree HEAD origin/main` completed without conflicts.

## Notes

- `xcodebuild -project ZooClaw.xcodeproj -scheme ZooClaw -destination 'platform=macOS' build` could not run locally because the current `ZooClaw` scheme exposes no macOS destination in this checkout.


---

## feat(services): add whatsapp business bridge (#2522)

- **SHA**: `04b3bec42a549cde4f5385a207a2a5ea129ade27`
- **作者**: bill-srp
- **日期**: 2026-07-06T03:26:47Z
- **PR**: #2522

### Commit Message

```
feat(services): add whatsapp business bridge (#2522)

## Summary

- Adds a standalone `services/whatsapp-business-service` Fastify worker
for WhatsApp Cloud API webhook intake.
- Verifies Meta webhook signatures, parses inbound WhatsApp messages,
and routes known users to Mattermost.
- Adds Claw Interface service-client calls for WhatsApp message
claim/complete, user lookup/register, and Mattermost outbound target
resolution.
- Adds Mattermost WebSocket forwarding so Mattermost replies can be sent
back through WhatsApp Graph API.
- Adds the matching Claw Interface WhatsApp routes/service logic
(claim/complete lease contract, user lookup/register/bind, outbound
target resolution with bot-author proof) plus deploy/tag workflows for
the new service.
- Hardens the bridge against malformed signatures, retryable per-message
routing failures, duplicate same-token websocket setup, stale Mattermost
websocket pool entries, missing required integration config, duplicate
Meta webhook delivery via exclusive `message_id` claim/complete
contracts, and inbound WhatsApp echo-back through Mattermost outbound
routing.
- Serializes same-sender webhook batches (later messages stay unclaimed
after an earlier retryable failure) so Meta replay preserves
conversation order; distinct senders still route concurrently.
- Replies through WhatsApp instead of silently consuming messages the
bridge cannot forward: unsupported non-text types, unbound first-time
senders, and bound users whose workspace routing is still being
repaired.
- Treats every completion-persistence failure (lost lease or exhausted
retries) as a retryable batch failure so Meta replays drive the claim
row to a terminal completed state — at-least-once delivery with
`message_id` dedupe, never a permanently incomplete row.
- Reconnects Mattermost websockets with exponential backoff (initial
connect failures included) instead of tight-looping on revoked tokens.
- Outbound resolution fails closed unless the Mattermost post author is
proven to be the workspace bot.
- Staging deploys are gated on `services/whatsapp-business-service/**`
changes so unrelated main merges cannot restart the bridge; release tags
pin the merged commit.
- Documents the business flow, runtime config, and local service
commands.

## Local checks

- `CI=true pnpm --dir services/whatsapp-business-service
--config.confirmModulesPurge=false typecheck`
- `CI=true pnpm --dir services/whatsapp-business-service
--config.confirmModulesPurge=false test` (5 files, 48 tests)
- `CI=true pnpm --dir services/whatsapp-business-service
--config.confirmModulesPurge=false build`
- claw-interface: pytest unit suites for whatsapp routes/service, ruff,
pyright, import-linter

## Notes

- Reply listening is still registered in-process from inbound traffic
only. Durable listener bootstrap across restarts is intentionally
deferred: deploys are double-gated behind
`WHATSAPP_BUSINESS_SERVICE_DEPLOY_ENABLED` and
`WHATSAPP_BUSINESS_LISTENER_BOOTSTRAP_READY`, and a follow-up PR with a
design spec will move watched-token state into Claw Interface.
```

### PR Body

## Summary

- Adds a standalone `services/whatsapp-business-service` Fastify worker for WhatsApp Cloud API webhook intake.
- Verifies Meta webhook signatures, parses inbound WhatsApp messages, and routes known users to Mattermost.
- Adds Claw Interface service-client calls for WhatsApp message claim/complete, user lookup/register, and Mattermost outbound target resolution.
- Adds Mattermost WebSocket forwarding so Mattermost replies can be sent back through WhatsApp Graph API.
- Adds the matching Claw Interface WhatsApp routes/service logic (claim/complete lease contract, user lookup/register/bind, outbound target resolution with bot-author proof) plus deploy/tag workflows for the new service.
- Hardens the bridge against malformed signatures, retryable per-message routing failures, duplicate same-token websocket setup, stale Mattermost websocket pool entries, missing required integration config, duplicate Meta webhook delivery via exclusive `message_id` claim/complete contracts, and inbound WhatsApp echo-back through Mattermost outbound routing.
- Serializes same-sender webhook batches (later messages stay unclaimed after an earlier retryable failure) so Meta replay preserves conversation order; distinct senders still route concurrently.
- Replies through WhatsApp instead of silently consuming messages the bridge cannot forward: unsupported non-text types, unbound first-time senders, and bound users whose workspace routing is still being repaired.
- Treats every completion-persistence failure (lost lease or exhausted retries) as a retryable batch failure so Meta replays drive the claim row to a terminal completed state — at-least-once delivery with `message_id` dedupe, never a permanently incomplete row.
- Reconnects Mattermost websockets with exponential backoff (initial connect failures included) instead of tight-looping on revoked tokens.
- Outbound resolution fails closed unless the Mattermost post author is proven to be the workspace bot.
- Staging deploys are gated on `services/whatsapp-business-service/**` changes so unrelated main merges cannot restart the bridge; release tags pin the merged commit.
- Documents the business flow, runtime config, and local service commands.

## Local checks

- `CI=true pnpm --dir services/whatsapp-business-service --config.confirmModulesPurge=false typecheck`
- `CI=true pnpm --dir services/whatsapp-business-service --config.confirmModulesPurge=false test` (5 files, 48 tests)
- `CI=true pnpm --dir services/whatsapp-business-service --config.confirmModulesPurge=false build`
- claw-interface: pytest unit suites for whatsapp routes/service, ruff, pyright, import-linter

## Notes

- Reply listening is still registered in-process from inbound traffic only. Durable listener bootstrap across restarts is intentionally deferred: deploys are double-gated behind `WHATSAPP_BUSINESS_SERVICE_DEPLOY_ENABLED` and `WHATSAPP_BUSINESS_LISTENER_BOOTSTRAP_READY`, and a follow-up PR with a design spec will move watched-token state into Claw Interface.


---

## fix(web): mount preview providers for mini-chat and agent-builder surfaces (#2652)

- **SHA**: `783f741c50fb9bd7445aa5f4061d9702f4a0e5f1`
- **作者**: Chris@ZooClaw
- **日期**: 2026-07-06T02:57:17Z
- **PR**: #2652

### Commit Message

```
fix(web): mount preview providers for mini-chat and agent-builder surfaces (#2652)

## Problem

React render-time crash: `useImagePreview must be used within
ImagePreviewProvider`.

`ImagePreviewProvider` and `FilePreviewProvider` are mounted
**per-surface only** — in `GenClawClient`, `SessionThreadClient`,
`agent-chat-client`, and `share/ReplayPlayer`. But the **same** OpenClaw
message tree is also rendered by surfaces that mount neither:

- **mini-chat** — `MiniChatClient` → `SubagentChatPanel` →
`OpenClawThread` (compact)
- **agent-builder test pane** — `OpenClawChatSurface` → `OpenClawThread`

That tree renders `MMAttachments`, whose `ImageAttachment` /
`VideoAttachment` / `ReplayAttachment` / `FileAttachment` call the
**throwing** `useImagePreview()` / `useFilePreview()`. So the first
image / video / replay / file attachment crashes the whole subtree on
those surfaces. (ECA-1120, also the frontend half of ECA-1085 /
ECA-1118.)

## Root-cause fix

1. **Defense-in-depth (the crash-stopper).** All four attachment
components now read the context through the existing **optional**
variants `useOptionalImagePreview` / `useOptionalFilePreview` and
**no-op `open()` when the context is null** — the same pattern
`MarkdownContent` already uses. This removes the hard throw from the
shared message tree regardless of which provider is mounted where.

2. **Mount `ImagePreviewProvider` on the standalone mini-chat route** so
its image/video lightbox actually works (the main chat already mounts it
per-surface; agent-builder already mounts `ImagePreviewProvider` via
#2635).

### Why `FilePreviewProvider` is not hoisted

`FilePreviewProvider` requires a per-surface `state` prop computed by
`useArtifactsSidebar(...)` (tied to that surface's `displayMessages` /
`mm` wiring and the artifacts sidebar UI). mini-chat and the
agent-builder test pane have **no artifacts sidebar**, so there is
nothing to hoist a meaningful provider into. On those surfaces file
clicks gracefully **no-op** via the optional hook while the file
**download button keeps working** (it never depended on the provider).
The full chat and the public replay viewer are unchanged — they still
mount both providers and the lightbox/sidebar behave exactly as before.

## Test

New
`web/app/tests/unit/components/mattermost/MMAttachmentsNoPreviewProvider.unit.spec.tsx`
renders `MMAttachments` (image, video, previewable file) **with no
preview providers in scope** — exactly the mini-chat / agent-builder
condition — and asserts it does **not** throw.

- **Red before the fix:** fails with `useImagePreview must be used
within ImagePreviewProvider` (verified by temporarily restoring the
throwing hook).
- **Green after:** renders cleanly.

Also updated the existing `MMAttachments.unit.spec.tsx` provider mocks
to export the optional hooks (`useOptionalImagePreview` /
`useOptionalFilePreview`) the components now consume.

## Files changed

- `web/app/src/components/mattermost/attachments/ImageAttachment.tsx`
- `web/app/src/components/mattermost/attachments/VideoAttachment.tsx`
- `web/app/src/components/mattermost/attachments/ReplayAttachment.tsx`
- `web/app/src/components/mattermost/attachments/FileAttachment.tsx`
-
`web/app/src/app/[locale]/(app)/(chat)/mini-chat/[sessionKey]/MiniChatClient.tsx`
- `web/app/tests/unit/components/mattermost/MMAttachments.unit.spec.tsx`
-
`web/app/tests/unit/components/mattermost/MMAttachmentsNoPreviewProvider.unit.spec.tsx`
(new)

## Links

- https://linear.app/srpone/issue/ECA-1120
- https://linear.app/srpone/issue/ECA-1085

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## Problem

React render-time crash: `useImagePreview must be used within ImagePreviewProvider`.

`ImagePreviewProvider` and `FilePreviewProvider` are mounted **per-surface only** — in `GenClawClient`, `SessionThreadClient`, `agent-chat-client`, and `share/ReplayPlayer`. But the **same** OpenClaw message tree is also rendered by surfaces that mount neither:

- **mini-chat** — `MiniChatClient` → `SubagentChatPanel` → `OpenClawThread` (compact)
- **agent-builder test pane** — `OpenClawChatSurface` → `OpenClawThread`

That tree renders `MMAttachments`, whose `ImageAttachment` / `VideoAttachment` / `ReplayAttachment` / `FileAttachment` call the **throwing** `useImagePreview()` / `useFilePreview()`. So the first image / video / replay / file attachment crashes the whole subtree on those surfaces. (ECA-1120, also the frontend half of ECA-1085 / ECA-1118.)

## Root-cause fix

1. **Defense-in-depth (the crash-stopper).** All four attachment components now read the context through the existing **optional** variants `useOptionalImagePreview` / `useOptionalFilePreview` and **no-op `open()` when the context is null** — the same pattern `MarkdownContent` already uses. This removes the hard throw from the shared message tree regardless of which provider is mounted where.

2. **Mount `ImagePreviewProvider` on the standalone mini-chat route** so its image/video lightbox actually works (the main chat already mounts it per-surface; agent-builder already mounts `ImagePreviewProvider` via #2635).

### Why `FilePreviewProvider` is not hoisted

`FilePreviewProvider` requires a per-surface `state` prop computed by `useArtifactsSidebar(...)` (tied to that surface's `displayMessages` / `mm` wiring and the artifacts sidebar UI). mini-chat and the agent-builder test pane have **no artifacts sidebar**, so there is nothing to hoist a meaningful provider into. On those surfaces file clicks gracefully **no-op** via the optional hook while the file **download button keeps working** (it never depended on the provider). The full chat and the public replay viewer are unchanged — they still mount both providers and the lightbox/sidebar behave exactly as before.

## Test

New `web/app/tests/unit/components/mattermost/MMAttachmentsNoPreviewProvider.unit.spec.tsx` renders `MMAttachments` (image, video, previewable file) **with no preview providers in scope** — exactly the mini-chat / agent-builder condition — and asserts it does **not** throw.

- **Red before the fix:** fails with `useImagePreview must be used within ImagePreviewProvider` (verified by temporarily restoring the throwing hook).
- **Green after:** renders cleanly.

Also updated the existing `MMAttachments.unit.spec.tsx` provider mocks to export the optional hooks (`useOptionalImagePreview` / `useOptionalFilePreview`) the components now consume.

## Files changed

- `web/app/src/components/mattermost/attachments/ImageAttachment.tsx`
- `web/app/src/components/mattermost/attachments/VideoAttachment.tsx`
- `web/app/src/components/mattermost/attachments/ReplayAttachment.tsx`
- `web/app/src/components/mattermost/attachments/FileAttachment.tsx`
- `web/app/src/app/[locale]/(app)/(chat)/mini-chat/[sessionKey]/MiniChatClient.tsx`
- `web/app/tests/unit/components/mattermost/MMAttachments.unit.spec.tsx`
- `web/app/tests/unit/components/mattermost/MMAttachmentsNoPreviewProvider.unit.spec.tsx` (new)

## Links

- https://linear.app/srpone/issue/ECA-1120
- https://linear.app/srpone/issue/ECA-1085

🤖 Generated with [Claude Code](https://claude.com/claude-code)


