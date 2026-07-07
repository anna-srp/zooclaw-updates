---
title: "Agent 包支持公开分享链接"
type: "新功能上线"
priority: "高"
date: "2026-07-06"
status: "待审核"
channels: ""
---

# Agent 包支持公开分享链接

## 核心宣传点

你现在可以把自己的私有 Agent 包生成公开分享链接，任何人无需登录即可打开链接查看包的介绍页并了解其能力，分享你的 Agent 更简单。

## 原始内容

[039636e1] feat(pack-store): add public listing share flow (#2735)

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

--- PR #2735 body ---
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


[1bf24c0c] feat(pack-store): add public shared pack page and unauthenticated detail API (#2745)

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

--- PR #2745 body ---
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

