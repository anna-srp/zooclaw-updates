# ecap-workspace commits — 2026-06-30


共 18 个 commit

---

## fix(agent-builder): allow deprecated pack submit reuse (#2671)

- **SHA**: `2f3aeeb1239bbc6ee562d9e501064a516fd4abb2`
- **作者**: bill-srp
- **日期**: 2026-06-30T13:34:03Z
- **PR**: #2671

### 完整 Commit Message

```
fix(agent-builder): allow deprecated pack submit reuse (#2671)

## Summary

- Remove the Agent Builder submit-time guard that rejected deprecated
packs.
- Update the Agent Builder service test so deprecated packs reuse the
existing pack instead of creating a new one or failing.

## Validation

- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_agent_builder_service.py -q`
- [x] `/Users/bill/.venvs/claw-interface/bin/ruff check
services/claw-interface/app/services/agent_builder_service.py
services/claw-interface/tests/unit/test_agent_builder_service.py`
- [x] `/Users/bill/.venvs/claw-interface/bin/ruff format --check
services/claw-interface/app/services/agent_builder_service.py
services/claw-interface/tests/unit/test_agent_builder_service.py`
- [x] `bash scripts/verify-py.sh` partial: ruff check passed, ruff
format passed, import-linter passed
- [x] `bash scripts/verify-changed.sh` partial: ruff check passed, ruff
format passed, import-linter passed
- [ ] `bash scripts/verify-py.sh` full local pass: blocked by repo-local
`services/claw-interface/.venv` pyright missing imports (`fastapi`,
`pytest`, `favie_common`, `pymongo`, etc.)
- [ ] `bash scripts/verify-changed.sh` full local pass: same repo-local
pyright missing-import failure
```

### PR Body

## Summary

- Remove the Agent Builder submit-time guard that rejected deprecated packs.
- Update the Agent Builder service test so deprecated packs reuse the existing pack instead of creating a new one or failing.

## Validation

- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_agent_builder_service.py -q`
- [x] `/Users/bill/.venvs/claw-interface/bin/ruff check services/claw-interface/app/services/agent_builder_service.py services/claw-interface/tests/unit/test_agent_builder_service.py`
- [x] `/Users/bill/.venvs/claw-interface/bin/ruff format --check services/claw-interface/app/services/agent_builder_service.py services/claw-interface/tests/unit/test_agent_builder_service.py`
- [x] `bash scripts/verify-py.sh` partial: ruff check passed, ruff format passed, import-linter passed
- [x] `bash scripts/verify-changed.sh` partial: ruff check passed, ruff format passed, import-linter passed
- [ ] `bash scripts/verify-py.sh` full local pass: blocked by repo-local `services/claw-interface/.venv` pyright missing imports (`fastapi`, `pytest`, `favie_common`, `pymongo`, etc.)
- [ ] `bash scripts/verify-changed.sh` full local pass: same repo-local pyright missing-import failure


---

## fix(pack-store): reactivate deprecated packs on submission (#2669)

- **SHA**: `d077f1797d70f52418e9f70ce318b803998cc5f5`
- **作者**: bill-srp
- **日期**: 2026-06-30T12:59:29Z
- **PR**: #2669

### 完整 Commit Message

```
fix(pack-store): reactivate deprecated packs on submission (#2669)

## Summary
- Allow a new pack submission to recover a deprecated pack without
bypassing org permissions.
- Admin submissions create the submission and let the existing approve
transaction restore the pack to active.
- Non-admin submissions atomically create the submission and move the
deprecated pack to submitted for review.
- Internal staff submissions do not auto-approve, so deprecated packs
move to submitted on that surface.
- Cover admin, non-admin, route forwarding, and CAS-miss behavior in
pack store tests.

## Root cause
The submission service rejected deprecated packs before creating a new
submission. Deprecated submissions now reuse the same atomic
`create_submission_and_mark_submitted` path as draft packs, so the pack
enters `submitted` while the submission is created. Callers that provide
an admin auto-approve reviewer then rely on `review_service.approve()`
to publish the pack as active in the existing approve transaction;
callers without auto-approval remain submitted for review.
`update_agent_studio_pack` is unchanged because Agent Studio updates do
not submit deprecated packs.

## Test plan
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_pack_services.py -q`
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_pack_store_txn_repo.py -q`
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_routes_pack_store.py -q`
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_internal_agent_packs_routes.py::TestInternalAgentPacksRoutes::test_submit_agent_pack_version_creates_submission_without_approving
services/claw-interface/tests/unit/test_internal_agent_packs_routes.py::TestInternalAgentPacksRoutes::test_submit_agent_pack_version_ignores_pack_test_fields
-q`
- [x] `bash scripts/verify-py.sh` partial: ruff check passed, ruff
format passed, import-linter passed
- [ ] `bash scripts/verify-py.sh` full local pass: blocked by repo-local
`services/claw-interface/.venv` pyright missing imports (`fastapi`,
`pytest`, `favie_common`, `pymongo`, etc.)
- [ ] `bash scripts/verify-changed.sh`: same local pyright
missing-import failure after running `verify-py.sh`
```

### PR Body

## Summary
- Allow a new pack submission to recover a deprecated pack without bypassing org permissions.
- Admin submissions create the submission and let the existing approve transaction restore the pack to active.
- Non-admin submissions atomically create the submission and move the deprecated pack to submitted for review.
- Internal staff submissions do not auto-approve, so deprecated packs move to submitted on that surface.
- Cover admin, non-admin, route forwarding, and CAS-miss behavior in pack store tests.

## Root cause
The submission service rejected deprecated packs before creating a new submission. Deprecated submissions now reuse the same atomic `create_submission_and_mark_submitted` path as draft packs, so the pack enters `submitted` while the submission is created. Callers that provide an admin auto-approve reviewer then rely on `review_service.approve()` to publish the pack as active in the existing approve transaction; callers without auto-approval remain submitted for review. `update_agent_studio_pack` is unchanged because Agent Studio updates do not submit deprecated packs.

## Test plan
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_pack_services.py -q`
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_pack_store_txn_repo.py -q`
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_routes_pack_store.py -q`
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_internal_agent_packs_routes.py::TestInternalAgentPacksRoutes::test_submit_agent_pack_version_creates_submission_without_approving services/claw-interface/tests/unit/test_internal_agent_packs_routes.py::TestInternalAgentPacksRoutes::test_submit_agent_pack_version_ignores_pack_test_fields -q`
- [x] `bash scripts/verify-py.sh` partial: ruff check passed, ruff format passed, import-linter passed
- [ ] `bash scripts/verify-py.sh` full local pass: blocked by repo-local `services/claw-interface/.venv` pyright missing imports (`fastapi`, `pytest`, `favie_common`, `pymongo`, etc.)
- [ ] `bash scripts/verify-changed.sh`: same local pyright missing-import failure after running `verify-py.sh`


---

## feat(pack-store): create Stripe resources for paid packs (#2668)

- **SHA**: `c583b4b63a9f88464c1a32f8e96c43a8135ef68f`
- **作者**: bill-srp
- **日期**: 2026-06-30T10:55:54Z
- **PR**: #2668

### 完整 Commit Message

```
feat(pack-store): create Stripe resources for paid packs (#2668)

## Summary
- create Stripe product/price resources when a paid agent-pack listing
is approved
- store Stripe product/price ids on `PaidPackPrice`
- copy those Stripe ids into `PackPurchase` snapshots when recording a
purchase

## Tests
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH pytest
services/claw-interface/tests/unit/test_paid_pack_price_repo.py
services/claw-interface/tests/unit/test_pack_services.py -q`
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH pytest
services/claw-interface/tests/unit/test_pack_purchase_repo.py
services/claw-interface/tests/unit/test_pack_purchase_service.py -q`
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-changed.sh`
```

### PR Body

## Summary
- create Stripe product/price resources when a paid agent-pack listing is approved
- store Stripe product/price ids on `PaidPackPrice`
- copy those Stripe ids into `PackPurchase` snapshots when recording a purchase

## Tests
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH pytest services/claw-interface/tests/unit/test_paid_pack_price_repo.py services/claw-interface/tests/unit/test_pack_services.py -q`
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH pytest services/claw-interface/tests/unit/test_pack_purchase_repo.py services/claw-interface/tests/unit/test_pack_purchase_service.py -q`
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-changed.sh`


---

## fix(enterprise-admin): stabilize otp login flow (#2666)

- **SHA**: `fa77dfb60b60c439834201dbe94babb79bf44601`
- **作者**: bill-srp
- **日期**: 2026-06-30T09:14:49Z
- **PR**: #2666

### 完整 Commit Message

```
fix(enterprise-admin): stabilize otp login flow (#2666)

## Summary
- Check `/account/me` after OTP verification so existing
enterprise-admin users do not re-register `/account/team-org`.
- Stop `/verify` from using render-time pending OTP state as a redirect
guard; missing OTP state now surfaces as an inline submit-time error
instead of bouncing to `/login`.
- Update verify/auth tests around existing accounts and the
no-login-bounce behavior.

## Root cause
`completeLogin()` previously called `/account/team-org` unconditionally
after OTP verification, so already registered users hit
`account.already_exists`.

Separately, `/verify` read pending OTP state from localStorage during
render and redirected to `/login` whenever it was absent. Successful
verification clears that pending state before navigation completes, so a
later render could briefly observe `pending=null`, route back to the
email form, and then continue into the app.

## Test plan
- [x] `git diff --check`
- [x] `bash scripts/verify-changed.sh` (no locally verifiable surface
for `web/enterprise-admin`; CI covers it)
- [ ] `pnpm --dir web/enterprise-admin test --
app/verify/__tests__/verify.test.tsx lib/__tests__/auth.test.ts`
(blocked before Vitest by local pnpm install/status check:
`ERR_PNPM_MISSING_TARBALL_INTEGRITY` for
`xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`)
```

### PR Body

## Summary
- Check `/account/me` after OTP verification so existing enterprise-admin users do not re-register `/account/team-org`.
- Stop `/verify` from using render-time pending OTP state as a redirect guard; missing OTP state now surfaces as an inline submit-time error instead of bouncing to `/login`.
- Update verify/auth tests around existing accounts and the no-login-bounce behavior.

## Root cause
`completeLogin()` previously called `/account/team-org` unconditionally after OTP verification, so already registered users hit `account.already_exists`.

Separately, `/verify` read pending OTP state from localStorage during render and redirected to `/login` whenever it was absent. Successful verification clears that pending state before navigation completes, so a later render could briefly observe `pending=null`, route back to the email form, and then continue into the app.

## Test plan
- [x] `git diff --check`
- [x] `bash scripts/verify-changed.sh` (no locally verifiable surface for `web/enterprise-admin`; CI covers it)
- [ ] `pnpm --dir web/enterprise-admin test -- app/verify/__tests__/verify.test.tsx lib/__tests__/auth.test.ts` (blocked before Vitest by local pnpm install/status check: `ERR_PNPM_MISSING_TARBALL_INTEGRITY` for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`)


---

## feat(dashboard-console): add listing review page (#2667)

- **SHA**: `780d2d81134a98ae318187b597a33e8abc2d6af1`
- **作者**: bill-srp
- **日期**: 2026-06-30T09:09:28Z
- **PR**: #2667

### 完整 Commit Message

```
feat(dashboard-console): add listing review page (#2667)

## Linear
N/A

## Summary
- Add a dashboard-console Listing reviews page for paid agent-pack
listing submissions.
- Reuse the existing internal agent-packs list API with
`status=listing_review` and `submission_status=submitted` filters.
- Wire review actions through the existing approve/reject submission
endpoints and cover listing rejection state handling.

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_internal_agent_packs_routes.py -q`
- [x] `git diff --check origin/main...HEAD`
- [ ] `pnpm --dir web/dashboard-console exec vitest run
app/lib/claw-api.test.ts app/routes/agent-packs/reviews/route.test.tsx
tests/packs.test.ts` blocked before tests by
`ERR_PNPM_MISSING_TARBALL_INTEGRITY` for
`xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`.
```

### PR Body

## Linear
N/A

## Summary
- Add a dashboard-console Listing reviews page for paid agent-pack listing submissions.
- Reuse the existing internal agent-packs list API with `status=listing_review` and `submission_status=submitted` filters.
- Wire review actions through the existing approve/reject submission endpoints and cover listing rejection state handling.

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest tests/unit/test_internal_agent_packs_routes.py -q`
- [x] `git diff --check origin/main...HEAD`
- [ ] `pnpm --dir web/dashboard-console exec vitest run app/lib/claw-api.test.ts app/routes/agent-packs/reviews/route.test.tsx tests/packs.test.ts` blocked before tests by `ERR_PNPM_MISSING_TARBALL_INTEGRITY` for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`.


---

## fix(bossclaw): hide bind guide for work channels (#2665)

- **SHA**: `2fa1c098cfbcace533b7a7ce911d1ad632c74a5e`
- **作者**: tim-srp
- **日期**: 2026-06-30T08:58:05Z
- **PR**: #2665

### 完整 Commit Message

```
fix(bossclaw): hide bind guide for work channels (#2665)

## Summary
- Hide the “怎么确认绑定成功” guide when BossClaw bind channel is 企业微信 or 飞书.
- Keep the guide visible for personal WeChat only.
- Add a unit test covering personal WeChat, WeCom, and Feishu channel
switching.

## Root cause
The bind confirmation guide was rendered unconditionally in the QR step,
so all binding channels inherited the personal WeChat confirmation
instructions.

## Test plan
- [x] pnpm --dir web/app test:unit
tests/unit/bossclaw/wechat-bind-step.unit.spec.tsx
tests/unit/bossclaw/bossclaw-layout-css.unit.spec.ts
tests/unit/bossclaw/bossclaw-client-intro.unit.spec.tsx
- [x] pnpm --dir web lint
- [x] pnpm --dir web exec tsc --noEmit --project app/tsconfig.json
- [x] git diff --check
- [x] GitHub CI for PR #2665
```

### PR Body

## Summary
- Hide the “怎么确认绑定成功” guide when BossClaw bind channel is 企业微信 or 飞书.
- Keep the guide visible for personal WeChat only.
- Add a unit test covering personal WeChat, WeCom, and Feishu channel switching.

## Root cause
The bind confirmation guide was rendered unconditionally in the QR step, so all binding channels inherited the personal WeChat confirmation instructions.

## Test plan
- [x] pnpm --dir web/app test:unit tests/unit/bossclaw/wechat-bind-step.unit.spec.tsx tests/unit/bossclaw/bossclaw-layout-css.unit.spec.ts tests/unit/bossclaw/bossclaw-client-intro.unit.spec.tsx
- [x] pnpm --dir web lint
- [x] pnpm --dir web exec tsc --noEmit --project app/tsconfig.json
- [x] git diff --check
- [x] GitHub CI for PR #2665

---

## fix(agent-builder): submit current run metadata (#2660)

- **SHA**: `82a1be8b87a0ed024a22719f3e20fe422f22347a`
- **作者**: kaka-srp
- **日期**: 2026-06-30T08:40:05Z
- **PR**: #2660

### 完整 Commit Message

```
fix(agent-builder): submit current run metadata (#2660)

## Summary
- Submit Agent Builder Pack Store metadata from the current accepted
Pack Test run for both new packs and existing pack updates.
- Centralize the metadata mapping for `avatar_url`, `category`,
`short_bio`, `bio`, `skills`, `integrations`, `automations`, and
`quick_commands`.
- Add regression coverage proving an existing pack's stale metadata is
not reused when submitting a new version.

## Root cause
Agent Builder submit derives submission data from the latest Pack Test
run. The create-pack branch already used current run metadata, but the
existing-pack update branch passed metadata from the persisted `Pack`
row into `submit_new_version`. That meant changes made in the current
`description.json` or `agent-pack.yaml` `quick_commands` could be lost
when submitting a new version for an existing pack.

## Test plan
- [x] `python -m pytest
services/claw-interface/tests/unit/test_agent_builder_service.py`
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh` during push hook
```

### PR Body

## Summary
- Submit Agent Builder Pack Store metadata from the current accepted Pack Test run for both new packs and existing pack updates.
- Centralize the metadata mapping for `avatar_url`, `category`, `short_bio`, `bio`, `skills`, `integrations`, `automations`, and `quick_commands`.
- Add regression coverage proving an existing pack's stale metadata is not reused when submitting a new version.

## Root cause
Agent Builder submit derives submission data from the latest Pack Test run. The create-pack branch already used current run metadata, but the existing-pack update branch passed metadata from the persisted `Pack` row into `submit_new_version`. That meant changes made in the current `description.json` or `agent-pack.yaml` `quick_commands` could be lost when submitting a new version for an existing pack.

## Test plan
- [x] `python -m pytest services/claw-interface/tests/unit/test_agent_builder_service.py`
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh` during push hook


---

## fix(bossclaw): allow mobile QR step scrolling (#2663)

- **SHA**: `78da4c2ccdfb4cf8e81f7d39cca94c5dcc1fd2d5`
- **作者**: tim-srp
- **日期**: 2026-06-30T08:36:23Z
- **PR**: #2663

### 完整 Commit Message

```
fix(bossclaw): allow mobile QR step scrolling (#2663)

## Summary
- Fix BossClaw mobile layout so tall QR binding content can scroll
instead of being clipped.
- Add CSS regression coverage for both mobile scrollability and desktop
phone-frame height capping.

## Confirmation / Evidence
- Latest `origin/main` still has `.stage { height: 100dvh; overflow:
hidden; }` and `.phone { height: 100dvh; overflow: hidden; }`. `.screen`
only has `min-height`, so it grows with content instead of becoming the
scroll container.
- User screenshot uses a 402 x 874 iPhone 17 Pro viewport and shows the
QR step continuing below the visible bottom.
- Minimal Chrome reproduction at 402 x 874, using the same BossClaw
shell rules and QR-step content height:
- Before fix: `documentScrollHeight=874`, `phoneClientHeight=874`,
`phoneScrollHeight=1010`, `phoneOverflowY=hidden`; after wheel:
`windowScrollY=0`, `screenScrollTop=0`. This confirms content exists
below the viewport but neither page nor inner screen scrolls.
- After fix: `documentScrollHeight=1010`, `phoneOverflowY=visible`;
after wheel: `windowScrollY=136`. This confirms the same tall content
becomes reachable.

## Root cause
The BossClaw shell used fixed `100dvh` height plus `overflow: hidden` on
the outer containers. The QR step content could exceed the available
viewport height, but the `.screen` element only had `min-height`, so it
grew past the parent and was clipped instead of becoming scrollable.
This is visible on smaller/taller mobile emulations and in embedded
browsers such as WeChat.

## Test plan
- [x] `pnpm --dir web/app exec eslint
tests/unit/bossclaw/bossclaw-layout-css.unit.spec.ts --quiet`
- [x] `pnpm --dir web/app test:unit
tests/unit/bossclaw/bossclaw-layout-css.unit.spec.ts
tests/unit/bossclaw/wechat-bind-step.unit.spec.tsx
tests/unit/bossclaw/bossclaw-client-intro.unit.spec.tsx`
- [x] PR CI: `web-quality / lint-and-typecheck`, `web-quality / test`,
`web-build-check`, Codex/Claude review
```

### PR Body

## Summary
- Fix BossClaw mobile layout so tall QR binding content can scroll instead of being clipped.
- Add CSS regression coverage for both mobile scrollability and desktop phone-frame height capping.

## Confirmation / Evidence
- Latest `origin/main` still has `.stage { height: 100dvh; overflow: hidden; }` and `.phone { height: 100dvh; overflow: hidden; }`. `.screen` only has `min-height`, so it grows with content instead of becoming the scroll container.
- User screenshot uses a 402 x 874 iPhone 17 Pro viewport and shows the QR step continuing below the visible bottom.
- Minimal Chrome reproduction at 402 x 874, using the same BossClaw shell rules and QR-step content height:
  - Before fix: `documentScrollHeight=874`, `phoneClientHeight=874`, `phoneScrollHeight=1010`, `phoneOverflowY=hidden`; after wheel: `windowScrollY=0`, `screenScrollTop=0`. This confirms content exists below the viewport but neither page nor inner screen scrolls.
  - After fix: `documentScrollHeight=1010`, `phoneOverflowY=visible`; after wheel: `windowScrollY=136`. This confirms the same tall content becomes reachable.

## Root cause
The BossClaw shell used fixed `100dvh` height plus `overflow: hidden` on the outer containers. The QR step content could exceed the available viewport height, but the `.screen` element only had `min-height`, so it grew past the parent and was clipped instead of becoming scrollable. This is visible on smaller/taller mobile emulations and in embedded browsers such as WeChat.

## Test plan
- [x] `pnpm --dir web/app exec eslint tests/unit/bossclaw/bossclaw-layout-css.unit.spec.ts --quiet`
- [x] `pnpm --dir web/app test:unit tests/unit/bossclaw/bossclaw-layout-css.unit.spec.ts tests/unit/bossclaw/wechat-bind-step.unit.spec.tsx tests/unit/bossclaw/bossclaw-client-intro.unit.spec.tsx`
- [x] PR CI: `web-quality / lint-and-typecheck`, `web-quality / test`, `web-build-check`, Codex/Claude review

---

## feat(design-system): add compact tag and elevated card (#2664)

- **SHA**: `98278be09e00bc9d0eb2a75c3b078713806e8af5`
- **作者**: lynn Zhuang
- **日期**: 2026-06-30T08:27:20Z
- **PR**: #2664

### 完整 Commit Message

```
feat(design-system): add compact tag and elevated card (#2664)

## Summary
- add a compact `Tag` component for text-only and icon+text labels
- lighten neutral tag surfaces so gray tags read closer to the current
web/app style
- update `Card` to a no-border elevated surface with subtle shadow
- refresh the design-system preview for Tag and Card examples

## Validation
- `pnpm --filter @zooclaw/design-system test src/components/tag.test.tsx
src/components/card.test.tsx`
- `pnpm --filter @zooclaw/design-system tsc`
- pre-push size/changed-surface gate passed

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
```

### PR Body

## Summary
- add a compact `Tag` component for text-only and icon+text labels
- lighten neutral tag surfaces so gray tags read closer to the current web/app style
- update `Card` to a no-border elevated surface with subtle shadow
- refresh the design-system preview for Tag and Card examples

## Validation
- `pnpm --filter @zooclaw/design-system test src/components/tag.test.tsx src/components/card.test.tsx`
- `pnpm --filter @zooclaw/design-system tsc`
- pre-push size/changed-surface gate passed


---

## feat(claw-interface): log v2 agent install timings (#2661)

- **SHA**: `22700aa9b33c4bfdc7f4867b8493847accbe90ec`
- **作者**: bill-srp
- **日期**: 2026-06-30T06:51:19Z
- **PR**: #2661

### 完整 Commit Message

```
feat(claw-interface): log v2 agent install timings (#2661)

## Summary

- Add V2 agent install timing logs with the `[agent-install-v2-trace]`
prefix.
- Emit per-stage `duration_ms` plus cumulative `total_ms` for the
background install pipeline.
- Log final completed/skipped/failed outcomes, including the failing
stage and error type.

## Validation

- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`
- `/Users/bill/.venvs/claw-interface/bin/pytest -q
services/claw-interface/tests/unit/test_agent_install_service.py`
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-changed.sh`
```

### PR Body

## Summary

- Add V2 agent install timing logs with the `[agent-install-v2-trace]` prefix.
- Emit per-stage `duration_ms` plus cumulative `total_ms` for the background install pipeline.
- Log final completed/skipped/failed outcomes, including the failing stage and error type.

## Validation

- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`
- `/Users/bill/.venvs/claw-interface/bin/pytest -q services/claw-interface/tests/unit/test_agent_install_service.py`
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-changed.sh`


---

## refactor(claw-interface): move agent services out of computer package (#2662)

- **SHA**: `1c88a154f8d04d9d692b31aa7d87feccec3615f6`
- **作者**: bill-srp
- **日期**: 2026-06-30T06:38:41Z
- **PR**: #2662

### 完整 Commit Message

```
refactor(claw-interface): move agent services out of computer package (#2662)

## Summary

- Move computer-scoped agent service modules from
`app.services.computer` into a dedicated `app.services.agents` package.
- Update production imports and test patch targets to use the new
package path.
- Include the latest paid-pack install purchase guard in the new agents
package after rebasing onto current `main`.
- Keep computer/runtime services in `app.services.computer` and preserve
existing route/runtime behavior.

## Tests

- `PATH="/Users/bill/.venvs/claw-interface/bin:$PATH" bash
scripts/verify-changed.sh`
- `cd services/claw-interface &&
PATH="/Users/bill/.venvs/claw-interface/bin:$PATH" pytest
tests/unit/test_agent_service.py
tests/unit/test_agent_install_service.py
tests/unit/test_agent_multi_install_service.py
tests/unit/test_agent_uninstall_service.py
tests/unit/test_agent_update_service.py
tests/unit/test_agent_mm_state_service.py
tests/unit/test_vertical_pack_plans_routes.py
tests/unit/test_computer_service.py -q` (`230 passed`)
```

### PR Body

## Summary

- Move computer-scoped agent service modules from `app.services.computer` into a dedicated `app.services.agents` package.
- Update production imports and test patch targets to use the new package path.
- Include the latest paid-pack install purchase guard in the new agents package after rebasing onto current `main`.
- Keep computer/runtime services in `app.services.computer` and preserve existing route/runtime behavior.

## Tests

- `PATH="/Users/bill/.venvs/claw-interface/bin:$PATH" bash scripts/verify-changed.sh`
- `cd services/claw-interface && PATH="/Users/bill/.venvs/claw-interface/bin:$PATH" pytest tests/unit/test_agent_service.py tests/unit/test_agent_install_service.py tests/unit/test_agent_multi_install_service.py tests/unit/test_agent_uninstall_service.py tests/unit/test_agent_update_service.py tests/unit/test_agent_mm_state_service.py tests/unit/test_vertical_pack_plans_routes.py tests/unit/test_computer_service.py -q` (`230 passed`)


---

## feat(claw-interface): add agent pack purchase records (#2658)

- **SHA**: `ee15d266eaf75f4ea366ff517c0f61bf18ed1219`
- **作者**: bill-srp
- **日期**: 2026-06-30T06:12:06Z
- **PR**: #2658

### 完整 Commit Message

```
feat(claw-interface): add agent pack purchase records (#2658)

## Summary

- add a paid agent-pack purchase snapshot model and repository
- expose `POST /agent-packs/{pack_id}/purchase` to record the current
org/user purchase
- snapshot pack metadata and the active paid price without checkout or
billing-status handling

## Validation

- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`
- `/Users/bill/.venvs/claw-interface/bin/pytest
services/claw-interface/tests/unit/test_pack_purchase_repo.py
services/claw-interface/tests/unit/test_pack_purchase_service.py
services/claw-interface/tests/unit/test_public_agent_packs_routes.py
services/claw-interface/tests/unit/test_paid_pack_price_repo.py -q`
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-changed.sh`
```

### PR Body

## Summary

- add a paid agent-pack purchase snapshot model and repository
- expose `POST /agent-packs/{pack_id}/purchase` to record the current org/user purchase
- snapshot pack metadata and the active paid price without checkout or billing-status handling

## Validation

- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`
- `/Users/bill/.venvs/claw-interface/bin/pytest services/claw-interface/tests/unit/test_pack_purchase_repo.py services/claw-interface/tests/unit/test_pack_purchase_service.py services/claw-interface/tests/unit/test_public_agent_packs_routes.py services/claw-interface/tests/unit/test_paid_pack_price_repo.py -q`
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-changed.sh`


---

## fix(onboarding): handle bossclaw mobile registration (#2641)

- **SHA**: `5bd5f943688a75f5cf7ba1abc2c2e65ba6645f73`
- **作者**: tim-srp
- **日期**: 2026-06-30T05:21:57Z
- **PR**: #2641

### 完整 Commit Message

```
fix(onboarding): handle bossclaw mobile registration (#2641)

## Summary
- Refresh BossClaw landing context when a new URL payload arrives so
cached WeChat WebView state does not reuse an old context.
- Make mobile app and channel QR modals scrollable on short Safari
viewports.
- Keep gift-code redemption inside the current registration flow without
navigating to chat.

## Root cause
Cached landing context could be preserved even when a fresh BossClaw URL
payload was present, so WeChat WebView users could continue with stale
registration context. QR modals also used centered fixed overlays
without scroll bounds, which clipped content on short iPhone screens.

## Test plan
- [x] `pnpm --dir web run lint`
- [x] `pnpm --dir web -r --workspace-concurrency=1 --if-present run tsc`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `pnpm --dir web run test:unit`
- [x] Targeted mobile/onboarding tests: `pnpm --dir web/app test:unit
tests/unit/components/UserMenu.unit.spec.tsx
tests/unit/app/landing/hooks/useLandingRedirect.unit.spec.ts
tests/unit/components/MobileAppModal.unit.spec.tsx
tests/unit/app/claw-settings/WeixinSetupModal.unit.spec.tsx
tests/unit/app/claw-settings/WecomSetupModal.unit.spec.tsx
tests/unit/app/claw-settings/FeishuSetupModal.unit.spec.tsx`

Note: `pnpm --dir web run tsc` currently fails because the repo script
invokes `pnpm ... exec` with unsupported `--if-present`; the equivalent
workspace run-command plus `web/app` tsc passed.
```

### PR Body

## Summary
- Refresh BossClaw landing context when a new URL payload arrives so cached WeChat WebView state does not reuse an old context.
- Make mobile app and channel QR modals scrollable on short Safari viewports.
- Keep gift-code redemption inside the current registration flow without navigating to chat.

## Root cause
Cached landing context could be preserved even when a fresh BossClaw URL payload was present, so WeChat WebView users could continue with stale registration context. QR modals also used centered fixed overlays without scroll bounds, which clipped content on short iPhone screens.

## Test plan
- [x] `pnpm --dir web run lint`
- [x] `pnpm --dir web -r --workspace-concurrency=1 --if-present run tsc`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `pnpm --dir web run test:unit`
- [x] Targeted mobile/onboarding tests: `pnpm --dir web/app test:unit tests/unit/components/UserMenu.unit.spec.tsx tests/unit/app/landing/hooks/useLandingRedirect.unit.spec.ts tests/unit/components/MobileAppModal.unit.spec.tsx tests/unit/app/claw-settings/WeixinSetupModal.unit.spec.tsx tests/unit/app/claw-settings/WecomSetupModal.unit.spec.tsx tests/unit/app/claw-settings/FeishuSetupModal.unit.spec.tsx`

Note: `pnpm --dir web run tsc` currently fails because the repo script invokes `pnpm ... exec` with unsupported `--if-present`; the equivalent workspace run-command plus `web/app` tsc passed.

---

## fix(openclaw): make computer create idempotent (#2639)

- **SHA**: `08fcfcd4832457ee0ad1cef79e91f1a801ec8500`
- **作者**: bill-srp
- **日期**: 2026-06-30T05:20:46Z
- **PR**: #2639

### 完整 Commit Message

```
fix(openclaw): make computer create idempotent (#2639)

## Summary
- Make `POST /computers` idempotently return an existing user computer
instead of starting another cold create.
- Treat any live non-`pack_test` computer, including `stopped` and
`error` rows, as satisfying the create-existence check.
- Add a Mongo partial unique index on `(uid, org_id)` for live user
computers (`deleted_at: None`, `source: user`) to enforce one
non-`pack_test` computer per user/org.
- Cleanup early Mattermost resources only for clear FastClaw client-side
4xx create failures, including the concurrent duplicate path before
returning the existing computer.
- Preserve early Mattermost resources on uncertain/non-4xx FastClaw
create failures.
- Collapse frontend computer creation behind one global
`ensureUserComputer()` path during auth bootstrap; init/recreate
recovery no longer calls `POST /computers`.

## Root cause
Concurrent `POST /computers` requests can both observe no existing
durable user computer before either write lands. One request may create
the FastClaw bot without Mattermost config while the other creates
Mattermost resources, then fails on duplicate slug and cleans them up.
The surviving bot is left running without `mattermost/default`
configured.

## Behavior boundary
The normalized create path is intentionally idempotent for the current
product path: once a user has any live non-`pack_test` computer in the
org, another `POST /computers` returns that existing computer even if
the request uses a different `computer_name` and quota would otherwise
allow more. This avoids duplicate FastClaw/Mattermost provisioning races
during initialization and retry flows.

`pack_test` computers remain excluded because they are temporary preview
computers scoped to pack-test runs. `stopped` and `error` user computers
still count as existing durable computers and therefore block a fresh
product create until the row is soft-deleted.

On the web app, the only runtime path that can create a normalized user
computer is now the auth-manager bootstrap when the user enters the
system. `useOpenClawInit` only observes/redeploys/recreates existing
computers; if bootstrap has not produced the computer yet, init waits
and polls instead of provisioning a replacement.

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_computer_service.py
services/claw-interface/tests/unit/test_computer_repo.py` — 55 passed
- [x] `git diff --check`
- [x] `rg -n "\bcreateComputer\(|\bensureUserComputer\(" web/app/src`
- [ ] `bash scripts/verify-web.sh ...` blocked locally before
tsc/vitest/eslint by pnpm lockfile integrity for
`xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`
```

### PR Body

## Summary
- Make `POST /computers` idempotently return an existing user computer instead of starting another cold create.
- Treat any live non-`pack_test` computer, including `stopped` and `error` rows, as satisfying the create-existence check.
- Add a Mongo partial unique index on `(uid, org_id)` for live user computers (`deleted_at: None`, `source: user`) to enforce one non-`pack_test` computer per user/org.
- Cleanup early Mattermost resources only for clear FastClaw client-side 4xx create failures, including the concurrent duplicate path before returning the existing computer.
- Preserve early Mattermost resources on uncertain/non-4xx FastClaw create failures.
- Collapse frontend computer creation behind one global `ensureUserComputer()` path during auth bootstrap; init/recreate recovery no longer calls `POST /computers`.

## Root cause
Concurrent `POST /computers` requests can both observe no existing durable user computer before either write lands. One request may create the FastClaw bot without Mattermost config while the other creates Mattermost resources, then fails on duplicate slug and cleans them up. The surviving bot is left running without `mattermost/default` configured.

## Behavior boundary
The normalized create path is intentionally idempotent for the current product path: once a user has any live non-`pack_test` computer in the org, another `POST /computers` returns that existing computer even if the request uses a different `computer_name` and quota would otherwise allow more. This avoids duplicate FastClaw/Mattermost provisioning races during initialization and retry flows.

`pack_test` computers remain excluded because they are temporary preview computers scoped to pack-test runs. `stopped` and `error` user computers still count as existing durable computers and therefore block a fresh product create until the row is soft-deleted.

On the web app, the only runtime path that can create a normalized user computer is now the auth-manager bootstrap when the user enters the system. `useOpenClawInit` only observes/redeploys/recreates existing computers; if bootstrap has not produced the computer yet, init waits and polls instead of provisioning a replacement.

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_computer_service.py services/claw-interface/tests/unit/test_computer_repo.py` — 55 passed
- [x] `git diff --check`
- [x] `rg -n "\bcreateComputer\(|\bensureUserComputer\(" web/app/src`
- [ ] `bash scripts/verify-web.sh ...` blocked locally before tsc/vitest/eslint by pnpm lockfile integrity for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`


---

## feat(web): migrate agent settings to computer scope (#2645)

- **SHA**: `75ce7ba895ad9a95b5e1a0402763b0433ce90064`
- **作者**: bill-srp
- **日期**: 2026-06-30T04:04:01Z
- **PR**: #2645

### 完整 Commit Message

```
feat(web): migrate agent settings to computer scope (#2645)

## Linear
N/A

## Summary
- Migrate web agent settings reads/writes to the computer-scoped backend
route from #2637.
- Remove the old single-agent BFF settings routes under
`/api/openclaw/settings/agent/[agentId]`.
- Keep settings query keys and UI hooks scoped by `computerId` +
`agentId`.

## Split
This is the frontend slice split out from the original large agent
settings migration PR.

Stack:
- Backend base: #2637
- Docs slice: #2644

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH
PYTHONPATH=services/claw-interface pytest
services/claw-interface/tests/unit/test_agent_routes.py
services/claw-interface/tests/unit/test_openclaw_settings_routes.py -q`
passed on the backend base (`281 passed`)
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh` passed on the backend base
- [ ] `bash scripts/verify-web.sh ...` attempted, but local Codex pnpm
install is blocked by the existing lockfile entry for
`xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz` missing an
`integrity` field before `tsc`/`vitest`/`eslint` can run
```

### PR Body

## Linear
N/A

## Summary
- Migrate web agent settings reads/writes to the computer-scoped backend route from #2637.
- Remove the old single-agent BFF settings routes under `/api/openclaw/settings/agent/[agentId]`.
- Keep settings query keys and UI hooks scoped by `computerId` + `agentId`.

## Split
This is the frontend slice split out from the original large agent settings migration PR.

Stack:
- Backend base: #2637
- Docs slice: #2644

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH PYTHONPATH=services/claw-interface pytest services/claw-interface/tests/unit/test_agent_routes.py services/claw-interface/tests/unit/test_openclaw_settings_routes.py -q` passed on the backend base (`281 passed`)
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh` passed on the backend base
- [ ] `bash scripts/verify-web.sh ...` attempted, but local Codex pnpm install is blocked by the existing lockfile entry for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz` missing an `integrity` field before `tsc`/`vitest`/`eslint` can run


---

## fix(web): validate guide tour locale before CTA navigation (#2659)

- **SHA**: `bb5c874af805a51d4f25eb0531335a0908540f96`
- **作者**: tim-srp
- **日期**: 2026-06-30T03:45:06Z
- **PR**: #2659

### 完整 Commit Message

```
fix(web): validate guide tour locale before CTA navigation (#2659)

## Summary
- Fix guide tour CTA links when the current route first segment is not a
supported locale.
- Reuse existing i18n locale parsing and fall back to the current
LanguageContext locale for locale-free app routes.
- Add regression coverage for `/new-chat` opening the CTA destination in
the active language.

## Root cause
The guide tour CTA used `window.location.pathname.split("/")[1]` as the
locale. On app routes like `/new-chat`, that first segment is not a
locale, so the CTA opened `/new-chat/agents-manager`, which 404s.

## Test plan
- [x] `pnpm --dir web/app test:unit
tests/unit/components/GuideTourModal.unit.spec.tsx`
- [x] `pnpm --dir web/app exec tsc --noEmit --pretty false`
- [x] `pnpm --dir web/app exec eslint src/components/GuideTourModal.tsx
tests/unit/components/GuideTourModal.unit.spec.tsx --quiet`
```

### PR Body

## Summary
- Fix guide tour CTA links when the current route first segment is not a supported locale.
- Reuse existing i18n locale parsing and fall back to the current LanguageContext locale for locale-free app routes.
- Add regression coverage for `/new-chat` opening the CTA destination in the active language.

## Root cause
The guide tour CTA used `window.location.pathname.split("/")[1]` as the locale. On app routes like `/new-chat`, that first segment is not a locale, so the CTA opened `/new-chat/agents-manager`, which 404s.

## Test plan
- [x] `pnpm --dir web/app test:unit tests/unit/components/GuideTourModal.unit.spec.tsx`
- [x] `pnpm --dir web/app exec tsc --noEmit --pretty false`
- [x] `pnpm --dir web/app exec eslint src/components/GuideTourModal.tsx tests/unit/components/GuideTourModal.unit.spec.tsx --quiet`

---

## fix(agent-builder): reset pack test chat sessions (#2656)

- **SHA**: `026cd494498dbecc83c6747d94d9f85c0e3e2edc`
- **作者**: kaka-srp
- **日期**: 2026-06-30T03:09:12Z
- **PR**: #2656

### 完整 Commit Message

```
fix(agent-builder): reset pack test chat sessions (#2656)

## Summary

- Automatically sends `/new` once when an Agent Builder Pack Test
preview chat is connected and its history is ready.
- Keeps the reset scoped to the current `test_run_id`, so rerenders of
the same preview do not send duplicate `/new` commands.
- Excludes `/new` / `/reset` / `/compact` control-command turns from
Agent Builder test feedback detection, so the automatic reset does not
get auto-reviewed back into the builder chat.

## Why

Pack Test preview chats can reuse an existing bot session. That leaves
stale conversation context in the test bot and forces the creator to
manually type `/new` after every Package & Test. The preview should
start from a fresh runtime session as soon as it is ready, without
requiring user input.

## Tests

- `corepack pnpm exec vitest run
tests/unit/app/agent-builder-test-chat.unit.spec.tsx --config
./vitest.config.mts`
- `bash scripts/verify-web.sh --no-test
web/app/src/app/[locale]/\(app\)/\(chat\)/agent-builder/AgentBuilderTestChat.tsx
web/app/tests/unit/app/agent-builder-test-chat.unit.spec.tsx`
- pre-push `verify-changed`: passed
```

### PR Body

## Summary

- Automatically sends `/new` once when an Agent Builder Pack Test preview chat is connected and its history is ready.
- Keeps the reset scoped to the current `test_run_id`, so rerenders of the same preview do not send duplicate `/new` commands.
- Excludes `/new` / `/reset` / `/compact` control-command turns from Agent Builder test feedback detection, so the automatic reset does not get auto-reviewed back into the builder chat.

## Why

Pack Test preview chats can reuse an existing bot session. That leaves stale conversation context in the test bot and forces the creator to manually type `/new` after every Package & Test. The preview should start from a fresh runtime session as soon as it is ready, without requiring user input.

## Tests

- `corepack pnpm exec vitest run tests/unit/app/agent-builder-test-chat.unit.spec.tsx --config ./vitest.config.mts`
- `bash scripts/verify-web.sh --no-test web/app/src/app/[locale]/\(app\)/\(chat\)/agent-builder/AgentBuilderTestChat.tsx web/app/tests/unit/app/agent-builder-test-chat.unit.spec.tsx`
- pre-push `verify-changed`: passed


---

## feat(claw-interface): add computer-scoped agent settings (#2637)

- **SHA**: `3242b3597bb813995c9c0422e0b31030a0b59e56`
- **作者**: bill-srp
- **日期**: 2026-06-30T02:56:43Z
- **PR**: #2637

### 完整 Commit Message

```
feat(claw-interface): add computer-scoped agent settings (#2637)

## Linear
N/A

## Summary
- Extract the shared backend `AgentSettingsService` and channel helpers
out of the legacy route module.
- Add computer-scoped backend settings reads/writes under
`/computers/{computer_id}/agents/{agent_id}/settings`.
- Resolve settings against the selected computer instead of falling back
to the primary bot.
- Persist agent identity name/avatar into the agent workspace row while
keeping live config writes limited to the fields still owned there.
- Expose the channel helper module through a small facade
(`parse_channel_infos`, `annotate_channel_bindings`,
`get_agent_channel_bindings`) instead of cross-module private helper
imports.

## Split
This is now the backend slice of the original large PR.

Follow-up PRs:
- Docs slice: #2644
- Frontend slice: #2645, stacked on this backend branch

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH
PYTHONPATH=services/claw-interface pytest
services/claw-interface/tests/unit/test_agent_settings_channels.py -q`
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH
PYTHONPATH=services/claw-interface pytest
services/claw-interface/tests/unit/test_agent_settings_channels.py
services/claw-interface/tests/unit/test_openclaw_settings_routes.py
services/claw-interface/tests/unit/test_agent_routes.py -q` (`283
passed`)
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`
```

### PR Body

## Linear
N/A

## Summary
- Extract the shared backend `AgentSettingsService` and channel helpers out of the legacy route module.
- Add computer-scoped backend settings reads/writes under `/computers/{computer_id}/agents/{agent_id}/settings`.
- Resolve settings against the selected computer instead of falling back to the primary bot.
- Persist agent identity name/avatar into the agent workspace row while keeping live config writes limited to the fields still owned there.
- Expose the channel helper module through a small facade (`parse_channel_infos`, `annotate_channel_bindings`, `get_agent_channel_bindings`) instead of cross-module private helper imports.

## Split
This is now the backend slice of the original large PR.

Follow-up PRs:
- Docs slice: #2644
- Frontend slice: #2645, stacked on this backend branch

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH PYTHONPATH=services/claw-interface pytest services/claw-interface/tests/unit/test_agent_settings_channels.py -q`
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH PYTHONPATH=services/claw-interface pytest services/claw-interface/tests/unit/test_agent_settings_channels.py services/claw-interface/tests/unit/test_openclaw_settings_routes.py services/claw-interface/tests/unit/test_agent_routes.py -q` (`283 passed`)
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`

