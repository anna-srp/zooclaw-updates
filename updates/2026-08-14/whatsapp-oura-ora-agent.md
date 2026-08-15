---
title: "WhatsApp 版 Oura 健康助手「Ora」正式接入"
type: "Agent 上架/更新"
priority: "高"
date: "2026-08-14"
status: "待审核"
channels: ""
---

## 核心宣传点

WhatsApp 上的 Oura 用户现在对接的是全新专属助手「Ora」：每天三次健康简报、为 WhatsApp 排版优化的回复，还会主动提醒你同步戒指数据。

## 原始内容

feat(whatsapp): switch bridge agent pack to oura_ring_whatsapp (#3379)

<!-- PR 标题：feat(whatsapp): switch bridge agent pack to
oura_ring_whatsapp -->

## Linear
None — direct cutover task planned with the maintainer on 2026-08-12
(Option A: constants edit).

## Summary
- Switch the WhatsApp bridge's bound agent pack from `oura_ring` (shared
Oura connector pack) to `oura_ring_whatsapp`, the new WhatsApp-only lite
variant (persona "Ora": three daily briefings, WhatsApp-native output
contract, sync nudges).
- Value-only constant edit in
`services/claw-interface/app/services/whatsapp_service.py` — the
`_OURA_RING_*` constant/function names, log strings, and comments are
intentionally unchanged (Option A as planned).
- **Model override decision: kept.** `_OURA_RING_MODEL_PRIMARY =
"litellm/deepseek-v4-flash-0731"` stays as the install-time override.
Engine pack manifests carry no model (it's an install-time concern), so
dropping the override would silently move WhatsApp installs to the
platform default model. Veto here if the new pack should run a different
model.
- Two small review-driven hardenings (adjudicated from an independent
Opus review of the diff):
- `_resolve_routable_user`'s missing-pack log raised `info` → `warning`:
during the gated deploy window this line is the only signal that the
pack isn't live yet, a state that presents as a product-wide WhatsApp
outage ("being prepared" for everyone).
- New unit test pinning `_oura_ring_pack` →
`get_by_org_and_display_id(OFFICIAL_PACK_ORG_ID, "oura_ring_whatsapp")`.
No existing test pinned the display_id (they all patch at the function
boundary), so a typo'd id would have sailed through CI into that same
silent outage. This restores the guard the cutover plan assumed existed.

## ⚠️ Cross-repo dependency — merge/deploy order matters
This PR **relies on SerendipityOneInc/ecap-agent-pack#242** (adds the
`oura_ring_whatsapp` pack: catalog entry + both runtime variants):
https://github.com/SerendipityOneInc/ecap-agent-pack/pull/242

That PR must be merged and the pack live in Pack Store **before this
deploys** — if this ships first, `_oura_ring_pack()` resolves `None`,
every user gets "workspace is being prepared" indefinitely, and the only
telemetry is the (now-`warning`) missing-pack log line.

## Pre-deploy checklist
1. ecap-agent-pack#242 merged; `oura_ring_whatsapp` pack **active** in
Pack Store (org `zooclaw`) with an approved submission carrying a
registered **engine runtime asset**. Install fails pre-claim
(`agent.pack_runtime_variant_unavailable`) if the runtime asset isn't
resolvable — and pre-claim failures leave no `install_failed` row, so
they retry-loop on every inbound message instead of self-healing.
2. `ENGINE_PACK_RUNTIME_ASSETS_PACK_IDS` (env, gcp-foundation)
references the **new pack's pack_id** (or `*`). Env preconditions were
verified 2026-08-12; note the new pack_id only exists once the pack is
created, so re-confirm the list at flip time. If the new pack is absent
from an explicit list, installs silently take the legacy archive path
(different environment pinning/validation regime).
3. New pack is listed **free** (`requires_payment` unset). A paid
listing would fail every bridge install pre-claim with
`agent.purchase_required` — same non-converging loop.
4. **At-cap users check** (found in review; real but population-gated):
the cutover install consumes a visible quota slot
(`consumes_visible_quota=True` default) while the old `oura_ring`
workspace still occupies one. A user already at their plan cap
(free/starter 5, pro 10, ultra 20; vertical-pack holders exempt) fails
`agent.limit_exceeded` **pre-claim** → permanent "being prepared" loop,
one notice per message. Before deploying, count WhatsApp-bound users at
their plan cap; if nonzero, options: uninstall their old `oura_ring`
workspace first, or set `consumes_visible_quota=False` on
`_OURA_RING_INSTALL_CONTEXT` (one line, but a product/billing-semantics
call — deliberately **not** made in this PR).

## Expected post-deploy behavior (not a bug)
- Each already-bound user gets one "workspace is being prepared" notice
while the new pack auto-installs; subsequent replies come from the new
agent.
- Old `oura_ring` workspaces stay installed until manually uninstalled;
conversation memory does not carry over.

## Deployment
Backend-only (`services/claw-interface`). `whatsapp-business-service`
and `web` are untouched. (FYI: `web/app/src/lib/landing-content.ts`
still shows an `oura_ring` landing card — display-only, unrelated to
Pack Store lookup; follow up separately if the card should advertise the
new pack.)

## Test plan
- [x] `bash scripts/verify-py.sh` — ruff-check, ruff-format, pyright (0
errors), import-linter (8/8 contracts) all pass
- [x] Targeted `pytest tests/unit/test_whatsapp_service.py
tests/unit/test_whatsapp_legacy_resolution.py` — green at baseline,
after the constant flip, and after the review hardenings (incl. the new
display_id pinning test)
- [x] Repo-wide sweep for `oura_ring` / `oura-ring` literals — only the
constant changed; remaining hits are private function names
(intentional) and synthetic test fixture ids
- [x] Independent Opus review of the diff: completeness confirmed
(single resolution site; `whatsapp_session_service` inherits via
`_resolve_routable_user`; no stale second path)
- Full `pytest --cov` suite intentionally left to CI
(`claw-interface-quality`) per risk-based local validation

---
### PR Body

<!-- PR 标题：feat(whatsapp): switch bridge agent pack to oura_ring_whatsapp -->

## Linear
None — direct cutover task planned with the maintainer on 2026-08-12 (Option A: constants edit).

## Summary
- Switch the WhatsApp bridge's bound agent pack from `oura_ring` (shared Oura connector pack) to `oura_ring_whatsapp`, the new WhatsApp-only lite variant (persona "Ora": three daily briefings, WhatsApp-native output contract, sync nudges).
- Value-only constant edit in `services/claw-interface/app/services/whatsapp_service.py` — the `_OURA_RING_*` constant/function names, log strings, and comments are intentionally unchanged (Option A as planned).
- **Model override decision: kept.** `_OURA_RING_MODEL_PRIMARY = "litellm/deepseek-v4-flash-0731"` stays as the install-time override. Engine pack manifests carry no model (it's an install-time concern), so dropping the override would silently move WhatsApp installs to the platform default model. Veto here if the new pack should run a different model.
- Two small review-driven hardenings (adjudicated from an independent Opus review of the diff):
  - `_resolve_routable_user`'s missing-pack log raised `info` → `warning`: during the gated deploy window this line is the only signal that the pack isn't live yet, a state that presents as a product-wide WhatsApp outage ("being prepared" for everyone).
  - New unit test pinning `_oura_ring_pack` → `get_by_org_and_display_id(OFFICIAL_PACK_ORG_ID, "oura_ring_whatsapp")`. No existing test pinned the display_id (they all patch at the function boundary), so a typo'd id would have sailed through CI into that same silent outage. This restores the guard the cutover plan assumed existed.

## ⚠️ Cross-repo dependency — merge/deploy order matters
This PR **relies on SerendipityOneInc/ecap-agent-pack#242** (adds the `oura_ring_whatsapp` pack: catalog entry + both runtime variants):
https://github.com/SerendipityOneInc/ecap-agent-pack/pull/242

That PR must be merged and the pack live in Pack Store **before this deploys** — if this ships first, `_oura_ring_pack()` resolves `None`, every user gets "workspace is being prepared" indefinitely, and the only telemetry is the (now-`warning`) missing-pack log line.

## Pre-deploy checklist
1. ecap-agent-pack#242 merged; `oura_ring_whatsapp` pack **active** in Pack Store (org `zooclaw`) with an approved submission carrying a registered **engine runtime asset**. Install fails pre-claim (`agent.pack_runtime_variant_unavailable`) if the runtime asset isn't resolvable — and pre-claim failures leave no `install_failed` row, so they retry-loop on every inbound message instead of self-healing.
2. `ENGINE_PACK_RUNTIME_ASSETS_PACK_IDS` (env, gcp-foundation) references the **new pack's pack_id** (or `*`). Env preconditions were verified 2026-08-12; note the new pack_id only exists once the pack is created, so re-confirm the list at flip time. If the new pack is absent from an explicit list, installs silently take the legacy archive path (different environment pinning/validation regime).
3. New pack is listed **free** (`requires_payment` unset). A paid listing would fail every bridge install pre-claim with `agent.purchase_required` — same non-converging loop.
4. **At-cap users check** (found in review; real but population-gated): the cutover install consumes a visible quota slot (`consumes_visible_quota=True` default) while the old `oura_ring` workspace still occupies one. A user already at their plan cap (free/starter 5, pro 10, ultra 20; vertical-pack holders exempt) fails `agent.limit_exceeded` **pre-claim** → permanent "being prepared" loop, one notice per message. Before deploying, count WhatsApp-bound users at their plan cap; if nonzero, options: uninstall their old `oura_ring` workspace first, or set `consumes_visible_quota=False` on `_OURA_RING_INSTALL_CONTEXT` (one line, but a product/billing-semantics call — deliberately **not** made in this PR).

## Expected post-deploy behavior (not a bug)
- Each already-bound user gets one "workspace is being prepared" notice while the new pack auto-installs; subsequent replies come from the new agent.
- Old `oura_ring` workspaces stay installed until manually uninstalled; conversation memory does not carry over.

## Deployment
Backend-only (`services/claw-interface`). `whatsapp-business-service` and `web` are untouched. (FYI: `web/app/src/lib/landing-content.ts` still shows an `oura_ring` landing card — display-only, unrelated to Pack Store lookup; follow up separately if the card should advertise the new pack.)

## Test plan
- [x] `bash scripts/verify-py.sh` — ruff-check, ruff-format, pyright (0 errors), import-linter (8/8 contracts) all pass
- [x] Targeted `pytest tests/unit/test_whatsapp_service.py tests/unit/test_whatsapp_legacy_resolution.py` — green at baseline, after the constant flip, and after the review hardenings (incl. the new display_id pinning test)
- [x] Repo-wide sweep for `oura_ring` / `oura-ring` literals — only the constant changed; remaining hits are private function names (intentional) and synthetic test fixture ids
- [x] Independent Opus review of the diff: completeness confirmed (single resolution site; `whatsapp_session_service` inherits via `_resolve_routable_user`; no stale second path)
- Full `pytest --cov` suite intentionally left to CI (`claw-interface-quality`) per risk-based local validation

