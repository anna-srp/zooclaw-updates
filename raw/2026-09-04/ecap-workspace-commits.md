# SerendipityOneInc/ecap-workspace — commits 2026-09-04

## fix(billing): expose recoverable Airwallex invoices (#3653)

- **SHA**: `5376f5bdb51f202be9874275c45b24eea56de76a`
- **作者**: tim-srp
- **日期**: 2026-09-04T13:24:25Z
- **PR**: #3653

### Commit Message

```
fix(billing): expose recoverable Airwallex invoices (#3653)

## Summary

- expose the invoice download action for successful Airwallex orders
that can recover an invoice by subscription or customer identity
- keep Stripe invoice availability dependent on a persisted provider
invoice ID
- preserve the existing paid-status and provider restrictions

## Root cause

The download endpoint can safely recover a missing Airwallex invoice ID
on demand, but the order history response reported
`invoice_available=false` until that ID was already persisted. The
frontend therefore hid the only action capable of triggering recovery.

## Tests

- `services/claw-interface/.venv/bin/pytest
tests/unit/test_billing_v2_order_requests.py -q --disable-warnings`
- `bash scripts/verify-py.sh`
- `bash scripts/verify-changed.sh`

## Staging evidence

UID `7501615744291966976` has a successful Airwallex order without a
persisted invoice ID. Its exact subscription filter returns one
FINALIZED, PAID, amount-matching invoice with a PDF.
```

### PR Body

## Summary

- expose the invoice download action for successful Airwallex orders that can recover an invoice by subscription or customer identity
- keep Stripe invoice availability dependent on a persisted provider invoice ID
- preserve the existing paid-status and provider restrictions

## Root cause

The download endpoint can safely recover a missing Airwallex invoice ID on demand, but the order history response reported `invoice_available=false` until that ID was already persisted. The frontend therefore hid the only action capable of triggering recovery.

## Tests

- `services/claw-interface/.venv/bin/pytest tests/unit/test_billing_v2_order_requests.py -q --disable-warnings`
- `bash scripts/verify-py.sh`
- `bash scripts/verify-changed.sh`

## Staging evidence

UID `7501615744291966976` has a successful Airwallex order without a persisted invoice ID. Its exact subscription filter returns one FINALIZED, PAID, amount-matching invoice with a PDF.


---

## fix(billing): resolve subscription checkout changes safely (#3642)

- **SHA**: `d10b224cd446b3d2a96e68e84b94663d57b155c2`
- **作者**: tim-srp
- **日期**: 2026-09-04T12:10:33Z
- **PR**: #3642

### Commit Message

```
fix(billing): resolve subscription checkout changes safely (#3642)

## Summary
- resolve subscription checkout state automatically when the user
selects a payment channel
- reopen a live checkout only when channel, plan, and billing cycle all
match
- otherwise cancel the previous Antom or Airwallex checkout before
creating a replacement
- remove the checkout-in-progress / Reopen payment page interaction

## Root cause
The frontend treated the subscription checkout lease as a global
45-minute lock and only offered the stored provider URL. It did not
model the selected channel, plan, and billing cycle as one checkout
intent, so users could not safely switch payment channels and could
reopen a checkout for an outdated plan.

The replacement flow now fails closed: if provider cancellation fails or
its outcome is unknown, the old lease remains held and no second
checkout is created.

## Test plan
- [x] Antom request-ID cancellation succeeds before Card checkout
creation
- [x] Airwallex cancellation succeeds before Antom checkout creation
- [x] unknown cancellation outcome keeps the old order and lease
- [x] identical channel, plan, and billing cycle resumes the live URL
- [x] changed plan, billing cycle, or channel replaces the old checkout
- [x] frontend automatically resolves checkout conflicts and opens the
returned URL without a Reopen button
- [x] backend related tests: 78 passed
- [x] frontend billing tests: 102 passed
- [x] backend ruff, formatting, Pyright, and import-linter passed
- [x] targeted frontend ESLint passed with one pre-existing test warning

## Local validation note
`verify-changed.sh` passed backend verification but skipped its web
phase because the worktree does not have `web/node_modules`. The
directly relevant frontend ESLint and Vitest commands were run from
`web/app` and passed. Full frontend TypeScript validation remains
blocked by pre-existing chat/design-system/SEO dependency errors outside
the files changed by this PR.
```

### PR Body

## Summary
- resolve subscription checkout state automatically when the user selects a payment channel
- reopen a live checkout only when channel, plan, and billing cycle all match
- otherwise cancel the previous Antom or Airwallex checkout before creating a replacement
- remove the checkout-in-progress / Reopen payment page interaction

## Root cause
The frontend treated the subscription checkout lease as a global 45-minute lock and only offered the stored provider URL. It did not model the selected channel, plan, and billing cycle as one checkout intent, so users could not safely switch payment channels and could reopen a checkout for an outdated plan.

The replacement flow now fails closed: if provider cancellation fails or its outcome is unknown, the old lease remains held and no second checkout is created.

## Test plan
- [x] Antom request-ID cancellation succeeds before Card checkout creation
- [x] Airwallex cancellation succeeds before Antom checkout creation
- [x] unknown cancellation outcome keeps the old order and lease
- [x] identical channel, plan, and billing cycle resumes the live URL
- [x] changed plan, billing cycle, or channel replaces the old checkout
- [x] frontend automatically resolves checkout conflicts and opens the returned URL without a Reopen button
- [x] backend related tests: 78 passed
- [x] frontend billing tests: 102 passed
- [x] backend ruff, formatting, Pyright, and import-linter passed
- [x] targeted frontend ESLint passed with one pre-existing test warning

## Local validation note
`verify-changed.sh` passed backend verification but skipped its web phase because the worktree does not have `web/node_modules`. The directly relevant frontend ESLint and Vitest commands were run from `web/app` and passed. Full frontend TypeScript validation remains blocked by pre-existing chat/design-system/SEO dependency errors outside the files changed by this PR.


---

## chore(ios): rename app display name to ZooWork (#3652)

- **SHA**: `93c3b4384470584f814ef33ed19916a8d7e31ae1`
- **作者**: shana-srp
- **日期**: 2026-09-04T12:02:46Z
- **PR**: #3652

### Commit Message

```
chore(ios): rename app display name to ZooWork (#3652)

## Summary
- Set the iOS app display name to **ZooWork** in both Debug and Release
configurations, and update the camera, microphone, and photo-saving
permission descriptions to match.
- Preserve bundle identifiers, URL schemes, entitlements, and the Xcode
target/product names so existing app identity and integrations stay
intact.

## Test plan
- [x] Validate the Xcode project and app Info.plist with `plutil -lint`.
- [x] Parse the app target's build configurations and verify both
display names are `ZooWork`, with the existing staging and production
bundle identifiers preserved.
- [x] Run `git diff --check`.
- [x] Run `bash scripts/check-pr-size.sh --base origin/main` (14 / 3000
lines).
- [x] Run `bash scripts/verify-changed.sh` (no locally verifiable
surfaces apply to this project-metadata-only change).
- [x] CI `ios-quality` passed. No local build or packaging was
performed.
- [x] Claude and Codex automatic reviews reported no findings; code
scanning reported no open alerts for this PR's merge ref.

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Body

## Summary
- Set the iOS app display name to **ZooWork** in both Debug and Release configurations, and update the camera, microphone, and photo-saving permission descriptions to match.
- Preserve bundle identifiers, URL schemes, entitlements, and the Xcode target/product names so existing app identity and integrations stay intact.

## Test plan
- [x] Validate the Xcode project and app Info.plist with `plutil -lint`.
- [x] Parse the app target's build configurations and verify both display names are `ZooWork`, with the existing staging and production bundle identifiers preserved.
- [x] Run `git diff --check`.
- [x] Run `bash scripts/check-pr-size.sh --base origin/main` (14 / 3000 lines).
- [x] Run `bash scripts/verify-changed.sh` (no locally verifiable surfaces apply to this project-metadata-only change).
- [x] CI `ios-quality` passed. No local build or packaging was performed.
- [x] Claude and Codex automatic reviews reported no findings; code scanning reported no open alerts for this PR's merge ref.


---

## fix(billing): converge Airwallex invoice identities (#3651)

- **SHA**: `78d26c7e7decc0a65c92938be31d38c41edd7ce1`
- **作者**: tim-srp
- **日期**: 2026-09-04T11:41:00Z
- **PR**: #3651

### Commit Message

```
fix(billing): converge Airwallex invoice identities (#3651)

## Summary

- replace the Airwallex historical invoice backfill's unsupported
checkout/period matching with exact provider-side `subscription_id` and
`billing_customer_id` filters
- handle `invoice.payment.paid` and prevent finalized-but-unpaid
invoices from settling or becoming downloadable
- reconcile missing invoice IDs hourly and recover one missing ID on
demand before download
- share one conservative matcher across backfill, maintenance
reconciliation, and download recovery

## Root cause

Airwallex invoice list/detail responses do not contain `checkout_id`,
`period_starts_at`, or `period_ends_at`. The previous backfill fixtures
supplied those fields, so its tests passed while all real staging
candidates remained unmatched.

The replacement requires exactly one server-filtered invoice with
`payment_status=PAID`, matching amount, and matching currency.
Ambiguous, unpaid, or mismatched records remain unchanged. Three known
staging orders whose test amounts differ from their Airwallex invoices
are intentionally skipped.

## Verification

- 295 targeted Airwallex lifecycle, reconciliation, backfill, download,
client, schema, and repository tests passed
- `bash scripts/verify-py.sh`
- `bash scripts/verify-changed.sh`

## Related

- follows #3650
```

### PR Body

## Summary

- replace the Airwallex historical invoice backfill's unsupported checkout/period matching with exact provider-side `subscription_id` and `billing_customer_id` filters
- handle `invoice.payment.paid` and prevent finalized-but-unpaid invoices from settling or becoming downloadable
- reconcile missing invoice IDs hourly and recover one missing ID on demand before download
- share one conservative matcher across backfill, maintenance reconciliation, and download recovery

## Root cause

Airwallex invoice list/detail responses do not contain `checkout_id`, `period_starts_at`, or `period_ends_at`. The previous backfill fixtures supplied those fields, so its tests passed while all real staging candidates remained unmatched.

The replacement requires exactly one server-filtered invoice with `payment_status=PAID`, matching amount, and matching currency. Ambiguous, unpaid, or mismatched records remain unchanged. Three known staging orders whose test amounts differ from their Airwallex invoices are intentionally skipped.

## Verification

- 295 targeted Airwallex lifecycle, reconciliation, backfill, download, client, schema, and repository tests passed
- `bash scripts/verify-py.sh`
- `bash scripts/verify-changed.sh`

## Related

- follows #3650


---

## feat(billing): add provider invoice downloads (#3650)

- **SHA**: `8481672b4717c01bae7a7e264df303c00cfe1903`
- **作者**: tim-srp
- **日期**: 2026-09-04T10:22:52Z
- **PR**: #3650

### Commit Message

```
feat(billing): add provider invoice downloads (#3650)

## Linear

N/A

## Summary

- Add a localized Download invoice column to Billing recent activity and
remove the obsolete View all invoices link while preserving Stripe
payment-method management.
- Route paid Stripe orders to their hosted invoice page, paid Airwallex
orders to the provider PDF, and show localized unsupported messaging for
Alipay/Antom; unpaid or incomplete orders remain unavailable.
- Persist provider invoice identities for future Airwallex payments and
add a dry-run-by-default script to safely backfill historical successful
Airwallex orders.

## Test plan

- [x] Backend focused unit tests: 425 passed.
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright, and all 8
import-linter contracts passed.
- [x] Frontend targeted verification: TypeScript, ESLint, and Vitest
passed (379 passed, 1 skipped).
- [x] Backfill CLI help succeeds without database initialization and
documents dry-run as the default.
- [x] Final branch review found no critical, important, or minor issues.

## Rollout notes

- Deploy the backend before or together with the frontend because the UI
uses the new per-order invoice download endpoint.
- Run `scripts/backfill_airwallex_invoice_ids.py` in dry-run mode first,
review its counters and conflicts, and only then rerun with `--write` in
the intended environment.
- No production backfill was executed as part of this PR.
```

### PR Body

## Linear

N/A

## Summary

- Add a localized Download invoice column to Billing recent activity and remove the obsolete View all invoices link while preserving Stripe payment-method management.
- Route paid Stripe orders to their hosted invoice page, paid Airwallex orders to the provider PDF, and show localized unsupported messaging for Alipay/Antom; unpaid or incomplete orders remain unavailable.
- Persist provider invoice identities for future Airwallex payments and add a dry-run-by-default script to safely backfill historical successful Airwallex orders.

## Test plan

- [x] Backend focused unit tests: 425 passed.
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright, and all 8 import-linter contracts passed.
- [x] Frontend targeted verification: TypeScript, ESLint, and Vitest passed (379 passed, 1 skipped).
- [x] Backfill CLI help succeeds without database initialization and documents dry-run as the default.
- [x] Final branch review found no critical, important, or minor issues.

## Rollout notes

- Deploy the backend before or together with the frontend because the UI uses the new per-order invoice download endpoint.
- Run `scripts/backfill_airwallex_invoice_ids.py` in dry-run mode first, review its counters and conflicts, and only then rerun with `--write` in the intended environment.
- No production backfill was executed as part of this PR.


---

## fix(agents): confirm migrated shared computer updates (#3649)

- **SHA**: `e9f91acc76aa5dfd31951ad15053b196da840c2a`
- **作者**: kaka-srp
- **日期**: 2026-09-04T09:07:02Z
- **PR**: #3649

### Commit Message

```
fix(agents): confirm migrated shared computer updates (#3649)

## Summary

- Replace the Pack-ID runtime allowlist with submission capability
detection: valid Engine assets use V2, approved legacy submissions keep
the V1 archive path, and existing V2 provenance cannot silently
downgrade.
- Mark V1-migrated Agent workspaces that may pause sibling Agents, defer
their background Pack fan-out update, and require an explicit user
confirmation before forwarding `allow_shared_computer_pause=true`.
- Add the confirmation flow to SideNav, Agents Manager, My Agents, chat
sessions, Agent Builder publish/update, and iOS.
- Publish Engine runtime assets from Agent Builder V2 and retry the
bounded async Environment-readiness window.
- Preserve `AGENTS_V1_ONLY_UIDS`; keep the deprecated Pack allowlist
values in deployment overlays only for one older-image rollback window.
New code ignores that setting.

## Root cause

The migrated Agent still shares a legacy Computer, so a Pack update that
changes its Environment can pause sibling Agents. The previous update
path neither had an explicit user-consent contract for that disruption
nor a capability-based way to distinguish legacy Pack submissions from
V2 Engine assets. A Pack-ID allowlist was therefore both too narrow and
unable to express the actual runtime compatibility.

## Behavior

- Normal Agents update without an extra prompt.
- A migrated shared-Computer Agent shows a conservative warning that
sibling Agents may be temporarily unavailable and active tasks may be
interrupted; data and memories are preserved.
- Only the confirmed retry sends `allow_shared_computer_pause=true`.
- Legacy Packs without an Engine asset continue through V1
compatibility; malformed or missing metadata for a previously V2 Agent
fails closed.

## Test plan

- [x] Backend unit suite: 647 tests passed in focused review validation.
- [x] Post-refactor backend selection/lifecycle/routes suite: 202 tests
passed.
- [x] `bash scripts/verify-py.sh` passed (Ruff, format, Pyright, import
contracts).
- [x] Web unit suite: 298 focused tests passed; the complete Web CI
suite also passed after fixing an incomplete legacy test mock.
- [x] `bash scripts/verify-web.sh --no-test` and push-gate Web checks
passed.
- [x] iOS SwiftLint, simulator build, and tests passed on macOS CI.
- [x] Three focused agent reviews and both repository auto-review gates
completed with no remaining findings.

## Rollout

Deploy the Engine companion first, then the ECAP backend, Web, and iOS
clients. This PR does not deploy or migrate user data.

## Companion PR

- Engine contract and Computer-level fence:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1229
```

### PR Body

## Summary

- Replace the Pack-ID runtime allowlist with submission capability detection: valid Engine assets use V2, approved legacy submissions keep the V1 archive path, and existing V2 provenance cannot silently downgrade.
- Mark V1-migrated Agent workspaces that may pause sibling Agents, defer their background Pack fan-out update, and require an explicit user confirmation before forwarding `allow_shared_computer_pause=true`.
- Add the confirmation flow to SideNav, Agents Manager, My Agents, chat sessions, Agent Builder publish/update, and iOS.
- Publish Engine runtime assets from Agent Builder V2 and retry the bounded async Environment-readiness window.
- Preserve `AGENTS_V1_ONLY_UIDS`; keep the deprecated Pack allowlist values in deployment overlays only for one older-image rollback window. New code ignores that setting.

## Root cause

The migrated Agent still shares a legacy Computer, so a Pack update that changes its Environment can pause sibling Agents. The previous update path neither had an explicit user-consent contract for that disruption nor a capability-based way to distinguish legacy Pack submissions from V2 Engine assets. A Pack-ID allowlist was therefore both too narrow and unable to express the actual runtime compatibility.

## Behavior

- Normal Agents update without an extra prompt.
- A migrated shared-Computer Agent shows a conservative warning that sibling Agents may be temporarily unavailable and active tasks may be interrupted; data and memories are preserved.
- Only the confirmed retry sends `allow_shared_computer_pause=true`.
- Legacy Packs without an Engine asset continue through V1 compatibility; malformed or missing metadata for a previously V2 Agent fails closed.

## Test plan

- [x] Backend unit suite: 647 tests passed in focused review validation.
- [x] Post-refactor backend selection/lifecycle/routes suite: 202 tests passed.
- [x] `bash scripts/verify-py.sh` passed (Ruff, format, Pyright, import contracts).
- [x] Web unit suite: 298 focused tests passed; the complete Web CI suite also passed after fixing an incomplete legacy test mock.
- [x] `bash scripts/verify-web.sh --no-test` and push-gate Web checks passed.
- [x] iOS SwiftLint, simulator build, and tests passed on macOS CI.
- [x] Three focused agent reviews and both repository auto-review gates completed with no remaining findings.

## Rollout

Deploy the Engine companion first, then the ECAP backend, Web, and iOS clients. This PR does not deploy or migrate user data.

## Companion PR

- Engine contract and Computer-level fence: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1229


---

## fix(org): avoid persisting implicit CN region on creation (#3648)

- **SHA**: `c3a977f4e11166cc80c056f598b23ff7488efa4b`
- **作者**: sam-srp
- **日期**: 2026-09-04T08:39:35Z
- **PR**: #3648

### Commit Message

```
fix(org): avoid persisting implicit CN region on creation (#3648)

## Summary
- Omit region_code from new Org documents when it was not explicitly
supplied, instead of persisting the model default CN.
- Preserve explicitly configured regions and all other default fields.
- Add regression tests for personal/team creation and login eligibility
after persistence.

## Behavior
- New personal Orgs without a configured region fall back to request IP
country for email OTP eligibility.
- CN, missing, or invalid IP country remains blocked; valid non-CN IP
country is allowed.
- Team login eligibility is unchanged.
- No existing Org data is migrated or modified; existing stored CN
values remain effective.
- No new settings or frontend changes.

## Verification
- 121 related unit tests passed (Org repository/service, domestic access
and routes, regional model display).
- Targeted Pyright: 0 errors, 0 warnings.
- Ruff lint and format checks passed.
- Import contracts: 8 kept, 0 broken.
- git diff --check passed.
```

### PR Body

## Summary
- Omit region_code from new Org documents when it was not explicitly supplied, instead of persisting the model default CN.
- Preserve explicitly configured regions and all other default fields.
- Add regression tests for personal/team creation and login eligibility after persistence.

## Behavior
- New personal Orgs without a configured region fall back to request IP country for email OTP eligibility.
- CN, missing, or invalid IP country remains blocked; valid non-CN IP country is allowed.
- Team login eligibility is unchanged.
- No existing Org data is migrated or modified; existing stored CN values remain effective.
- No new settings or frontend changes.

## Verification
- 121 related unit tests passed (Org repository/service, domestic access and routes, regional model display).
- Targeted Pyright: 0 errors, 0 warnings.
- Ruff lint and format checks passed.
- Import contracts: 8 kept, 0 broken.
- git diff --check passed.

---

## fix(billing): replace superseded Antom checkouts (#3646)

- **SHA**: `fc51f977c4845e0fea277d4d68c4560f274bf5bb`
- **作者**: tim-srp
- **日期**: 2026-09-04T07:51:52Z
- **PR**: #3646

### Commit Message

```
fix(billing): replace superseded Antom checkouts (#3646)

## Summary
- allow a personal Antom checkout to replace an unpaid live checkout
when the selected plan or billing cycle changes
- preserve reuse behavior for the same complete checkout intent
- reuse the existing provider inquiry, cancellation verification,
payment recheck, and guarded local cancellation flow

## Root cause
The subscription checkout lease treated every pending personal checkout
as equivalent for 45 minutes. When a user closed an Alipay Starter
checkout and selected Pro, the new order could not claim the lease and
the UI could only reopen the old Starter URL. Expiry retirement handled
dead URLs but did not consider a still-live checkout that no longer
matched the user's selected plan or billing cycle.

## Test plan
- [x] `pytest tests/unit/test_antom_billing_v2_checkout.py
tests/unit/test_antom_checkout_expiry.py -q` (29 passed)
- [x] `bash scripts/verify-py.sh`
- [x] pre-push changed-surface verification

## Safety
- replacement only applies when both old and new intents have complete
`plan` and `billing_cycle` fields and they differ
- provider payment state is checked before and after cancellation
- local cancellation is guarded by pending status and provider
identifiers; ambiguous or paid states remain fail-closed
```

### PR Body

## Summary
- allow a personal Antom checkout to replace an unpaid live checkout when the selected plan or billing cycle changes
- preserve reuse behavior for the same complete checkout intent
- reuse the existing provider inquiry, cancellation verification, payment recheck, and guarded local cancellation flow

## Root cause
The subscription checkout lease treated every pending personal checkout as equivalent for 45 minutes. When a user closed an Alipay Starter checkout and selected Pro, the new order could not claim the lease and the UI could only reopen the old Starter URL. Expiry retirement handled dead URLs but did not consider a still-live checkout that no longer matched the user's selected plan or billing cycle.

## Test plan
- [x] `pytest tests/unit/test_antom_billing_v2_checkout.py tests/unit/test_antom_checkout_expiry.py -q` (29 passed)
- [x] `bash scripts/verify-py.sh`
- [x] pre-push changed-surface verification

## Safety
- replacement only applies when both old and new intents have complete `plan` and `billing_cycle` fields and they differ
- provider payment state is checked before and after cancellation
- local cancellation is guarded by pending status and provider identifiers; ambiguous or paid states remain fail-closed


---

## feat(dashboard-console): route claw-interface calls through worker BFF with CF Access service token (#3647)

- **SHA**: `0a7ab6d19bc3f4b61e726951b790a4754ccbefbf`
- **作者**: bill-srp
- **日期**: 2026-09-04T07:25:28Z
- **PR**: #3647

### Commit Message

```
feat(dashboard-console): route claw-interface calls through worker BFF with CF Access service token (#3647)

## Linear
<!-- no Linear issue for this task -->

## Summary
- dashboard-console previously had the **browser call claw-interface
directly** (`VITE_CLAW_INTERFACE_URL` shipped in the client bundle).
With the backend moving behind Cloudflare Zero Trust, those calls can no
longer cross Access. This PR routes them through a same-origin worker
BFF that authenticates with a **CF Access service token**.
- New `app/lib/claw-proxy.ts` (ported from web/app's
`src/lib/api/claw-proxy.ts`): path allowlist (`internal/*` +
`account/me` only, encoded-`..` traversal rejected), forwards
method/query/streamed body, forwards only
`content-type`/`accept`/`authorization` request headers, injects
`CF-Access-Client-Id`/`CF-Access-Client-Secret` from worker env (omitted
when unset, so local dev against a plain backend works), strips
hop-by-hop response headers, 502 JSON on upstream failure.
- New catch-all resource route `app/routes/api/claw.ts` (`api/claw/*`).
It derives the forwarded sub-path from the **raw request pathname**, not
`params["*"]` — React Router decodes splat params, which would corrupt
encoded ids (`skl%2Fa` → `skl/a`); regression-tested.
- `app/lib/claw-api.ts` swaps every call site to the same-origin
`CLAW_BFF_BASE = "/api/claw"`; `VITE_CLAW_INTERFACE_URL` is removed from
the client env surface (`vite-env.d.ts`, `.env.example`). Browser
Bearer-token handling is unchanged (pure passthrough — backend
`require_admin_user` stays the authority). Backend CORS for this origin
becomes unnecessary.
- **Deploy-time injection via GitHub Actions**:
`deploy-dashboard-console.yml` validates all settings up front, passes
the two non-secret ones (`CLAW_INTERFACE_URL` var, `CF_ACCESS_CLIENT_ID`
var with legacy-secret fallback) as `wrangler deploy --var` flags, and
uploads `CF_ACCESS_CLIENT_SECRET` as a **Workers secret** (`wrangler
secret put -c build/server/wrangler.json` — write-only at runtime,
persists across deploys; the generated config's env is pre-resolved,
sidestepping the multi-env `secret bulk` failure that keeps web/app's
deploy.yml on `--var`). This resolves the review P1 about the secret
being an inspectable plaintext Worker variable. The old
`VITE_CLAW_INTERFACE_URL` build env, the `build/server/wrangler.json`
node-patch step (its `/api/r2/copy` rationale was stale — no such route
in this app), and the matching build-output check are removed.
- Config: commented pointer blocks in `wrangler.jsonc` (prod + staging),
`.dev.vars.example` for local dev (gitignore negation added so the
example file is actually tracked), design spec in
`docs/superpowers/specs/2026-09-04-dashboard-console-bff-design.md`.

## Staged cutover (addresses Codex review P1)
The live console still calls the backend browser-direct, so Access must
not be enforced until the BFF console is serving:
1. Issue the CF Access service token (Access app may exist,
**unenforced**).
2. GitHub Environment config — DONE: `CF_ACCESS_CLIENT_ID` now lives as
an Environment **variable** (set in staging + production, 2026-09-04);
`CF_ACCESS_CLIENT_SECRET` stays an Environment secret (existing since
March); `CLAW_INTERFACE_URL` var already exists. Both deploy workflows
read the ID vars-first with secret fallback, so the legacy
`CF_ACCESS_CLIENT_ID` secrets can be deleted after this merges.
3. Deploy this console — traffic now flows through the BFF; CF headers
are harmlessly ignored while Access is unenforced.
4. Enforce the Access policy on the claw-interface hostname.
5. If the hostname changes, repoint the `CLAW_INTERFACE_URL` var and
redeploy.

## Test plan
- [x] `pnpm run typecheck` (dashboard-console) — pass
- [x] `pnpm test` — 74 files / 672 tests pass (includes new proxy +
route suites: allowlist, CF-header injection/omission, method/body/query
forwarding, header filtering, hop-by-hop stripping, 502 path,
raw-encoding preservation)
- [x] `pnpm lint` — pass
- [x] `grep -rn VITE_CLAW_INTERFACE_URL` — zero hits in app code and
workflow
- [x] deploy workflow YAML parses (both `deploy.yml` and
`deploy-dashboard-console.yml`)
- [ ] Staging smoke after cutover steps 1–3
```

### PR Body

## Linear
<!-- no Linear issue for this task -->

## Summary
- dashboard-console previously had the **browser call claw-interface directly** (`VITE_CLAW_INTERFACE_URL` shipped in the client bundle). With the backend moving behind Cloudflare Zero Trust, those calls can no longer cross Access. This PR routes them through a same-origin worker BFF that authenticates with a **CF Access service token**.
- New `app/lib/claw-proxy.ts` (ported from web/app's `src/lib/api/claw-proxy.ts`): path allowlist (`internal/*` + `account/me` only, encoded-`..` traversal rejected), forwards method/query/streamed body, forwards only `content-type`/`accept`/`authorization` request headers, injects `CF-Access-Client-Id`/`CF-Access-Client-Secret` from worker env (omitted when unset, so local dev against a plain backend works), strips hop-by-hop response headers, 502 JSON on upstream failure.
- New catch-all resource route `app/routes/api/claw.ts` (`api/claw/*`). It derives the forwarded sub-path from the **raw request pathname**, not `params["*"]` — React Router decodes splat params, which would corrupt encoded ids (`skl%2Fa` → `skl/a`); regression-tested.
- `app/lib/claw-api.ts` swaps every call site to the same-origin `CLAW_BFF_BASE = "/api/claw"`; `VITE_CLAW_INTERFACE_URL` is removed from the client env surface (`vite-env.d.ts`, `.env.example`). Browser Bearer-token handling is unchanged (pure passthrough — backend `require_admin_user` stays the authority). Backend CORS for this origin becomes unnecessary.
- **Deploy-time injection via GitHub Actions**: `deploy-dashboard-console.yml` validates all settings up front, passes the two non-secret ones (`CLAW_INTERFACE_URL` var, `CF_ACCESS_CLIENT_ID` var with legacy-secret fallback) as `wrangler deploy --var` flags, and uploads `CF_ACCESS_CLIENT_SECRET` as a **Workers secret** (`wrangler secret put -c build/server/wrangler.json` — write-only at runtime, persists across deploys; the generated config's env is pre-resolved, sidestepping the multi-env `secret bulk` failure that keeps web/app's deploy.yml on `--var`). This resolves the review P1 about the secret being an inspectable plaintext Worker variable. The old `VITE_CLAW_INTERFACE_URL` build env, the `build/server/wrangler.json` node-patch step (its `/api/r2/copy` rationale was stale — no such route in this app), and the matching build-output check are removed.
- Config: commented pointer blocks in `wrangler.jsonc` (prod + staging), `.dev.vars.example` for local dev (gitignore negation added so the example file is actually tracked), design spec in `docs/superpowers/specs/2026-09-04-dashboard-console-bff-design.md`.

## Staged cutover (addresses Codex review P1)
The live console still calls the backend browser-direct, so Access must not be enforced until the BFF console is serving:
1. Issue the CF Access service token (Access app may exist, **unenforced**).
2. GitHub Environment config — DONE: `CF_ACCESS_CLIENT_ID` now lives as an Environment **variable** (set in staging + production, 2026-09-04); `CF_ACCESS_CLIENT_SECRET` stays an Environment secret (existing since March); `CLAW_INTERFACE_URL` var already exists. Both deploy workflows read the ID vars-first with secret fallback, so the legacy `CF_ACCESS_CLIENT_ID` secrets can be deleted after this merges.
3. Deploy this console — traffic now flows through the BFF; CF headers are harmlessly ignored while Access is unenforced.
4. Enforce the Access policy on the claw-interface hostname.
5. If the hostname changes, repoint the `CLAW_INTERFACE_URL` var and redeploy.

## Test plan
- [x] `pnpm run typecheck` (dashboard-console) — pass
- [x] `pnpm test` — 74 files / 672 tests pass (includes new proxy + route suites: allowlist, CF-header injection/omission, method/body/query forwarding, header filtering, hop-by-hop stripping, 502 path, raw-encoding preservation)
- [x] `pnpm lint` — pass
- [x] `grep -rn VITE_CLAW_INTERFACE_URL` — zero hits in app code and workflow
- [x] deploy workflow YAML parses (both `deploy.yml` and `deploy-dashboard-console.yml`)
- [ ] Staging smoke after cutover steps 1–3


---

## fix(billing): refresh expired checkout links across providers (#3645)

- **SHA**: `991a21da377a3509020830b802e32d69df5b4a9b`
- **作者**: tim-srp
- **日期**: 2026-09-04T05:47:20Z
- **PR**: #3645

### Commit Message

```
fix(billing): refresh expired checkout links across providers (#3645)

## Summary

- centralize Airwallex checkout URL JWT expiry parsing with a
five-minute reuse safety window
- refresh stale Airwallex subscription and top-up checkouts only after
provider-confirmed terminal state, including cancellation races
- add Antom checkout deadlines, safe replay rules, pre/post-cancel
payment inquiry, guarded local retirement, and one-shot card top-up
retry

## Safety

- unknown provider inquiry or mutation outcomes fail closed
- Antom replacement checks for successful payment both before and after
cancellation
- local Antom cancellation uses a pending-state and provider-identity
CAS before releasing the checkout lease
- stale provider requests are never recreated with the same Antom
idempotency key

## Test plan

- [x] 187 focused backend unit tests
- [x] 2 frontend retry unit tests
- [x] `bash scripts/verify-changed.sh`
- [x] independent `origin/main...HEAD` code review: no findings

## Deployment

- deploy both `claw-interface` and `web/app`
```

### PR Body

## Summary

- centralize Airwallex checkout URL JWT expiry parsing with a five-minute reuse safety window
- refresh stale Airwallex subscription and top-up checkouts only after provider-confirmed terminal state, including cancellation races
- add Antom checkout deadlines, safe replay rules, pre/post-cancel payment inquiry, guarded local retirement, and one-shot card top-up retry

## Safety

- unknown provider inquiry or mutation outcomes fail closed
- Antom replacement checks for successful payment both before and after cancellation
- local Antom cancellation uses a pending-state and provider-identity CAS before releasing the checkout lease
- stale provider requests are never recreated with the same Antom idempotency key

## Test plan

- [x] 187 focused backend unit tests
- [x] 2 frontend retry unit tests
- [x] `bash scripts/verify-changed.sh`
- [x] independent `origin/main...HEAD` code review: no findings

## Deployment

- deploy both `claw-interface` and `web/app`


---

## feat(agents): let an owner narrow an agent's tool and skill surface (#3630)

- **SHA**: `26910f7f0b8d78d31ad68ddde26717b724bb1848`
- **作者**: siqiao-srp
- **日期**: 2026-09-04T04:08:06Z
- **PR**: #3630

### Commit Message

```
feat(agents): let an owner narrow an agent's tool and skill surface (#3630)

## What

`POST /agents/{workspace_id}/harden` — the first user-facing way to take
tools and global skills *away* from an engine agent.

An engine agent is created with the full tool manifest and every global
skill eligible, and nothing on the user-facing surface could take either
away: `tool_policy` and per-skill enablement are controld fields, and
claw-interface exposed no route that writes them. Restricting a hired
agent required an operator with a service token.

The gap has a concrete cost. `cron` is the sharpest case: an
agent-created schedule may not carry an outcome (design/18 D-O3), so
anything a model schedules for itself runs unattended with no acceptance
criterion and delivers whatever it produced. `write` / `edit` let a
model author the raw values a research agent is supposed to obtain from
tools. A research desk carrying a video generator and a slide builder
has more ways to answer a question with the wrong tool.

## Shape

- Denies six tools: `cron`, `edit`, `message`, `user_asset_delete`,
`user_asset_upsert`, `write`.
- Disables every **global**-scope skill outside a small keep list
(`xlsx`, `docx`, `pdf`, `feishu-doc`, `feishu-drive`) that the frontdesk
routing map needs for file work. Org- and pack-scope skills are never
touched.
- **Takes no request body, on purpose.** An endpoint that accepts a
policy can also *widen* one, which would put a way to hand `write` or
`cron` back to a model on the user-facing surface. This one only ever
narrows, to a set the server owns, so there is nothing to review per
call. Restoring the full manifest stays an operator action
(`tool_policy: {}`) on the control plane.
- Idempotent: skills the engine already excludes are skipped, not
re-disabled.
- A skill the engine refuses lands in `failed_skills` instead of
aborting the pass — the tool policy has already been written by then,
and an all-or-nothing failure would tell the caller nothing it could act
on. The reported reason is the domain code, never the upstream message.
- Authorization is the same as the neighbouring v2 routes: owner-scoped
workspace lookup plus `require_agents_v2`.

## Engine client

Two new methods, both deliberately separate from the existing ones:

- `set_agent_tool_policy` — not a field on `update_agent()`, because
`tool_policy` is replace-on-write in controld while that call merges,
and a merging caller would silently keep a policy it meant to drop.
- `set_agent_skill_enabled` — not `put_agent_skill()`, because a global
skill has no version pin this service owns; the body carries `enabled`
alone.

## Tests

30 new: 11 route tests driven over HTTP with `TestClient` (owner path,
no-body-cannot-widen, idempotent second call, 404s for
unknown/hidden/deleted/uninstalled/kill-switch-off with the engine never
called, partial failure reported, tool-policy failure surfacing as 503),
6 service tests, 4 engine-client contract tests, plus one asserting the
route is reachable on the real `create_app()` via the OpenAPI schema.

Verified against staging: `/agents/{workspace_id}/harden` currently
answers 404 there while `/skills` and `/model` answer 401, i.e. the
route is genuinely new.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01NwcPcWHHzuTsqy1dU8RJgj

---------

Co-authored-by: Claude Opus 5 (1M context) <noreply@anthropic.com>
```

### PR Body

## What

`POST /agents/{workspace_id}/harden` — the first user-facing way to take tools and global skills *away* from an engine agent.

An engine agent is created with the full tool manifest and every global skill eligible, and nothing on the user-facing surface could take either away: `tool_policy` and per-skill enablement are controld fields, and claw-interface exposed no route that writes them. Restricting a hired agent required an operator with a service token.

The gap has a concrete cost. `cron` is the sharpest case: an agent-created schedule may not carry an outcome (design/18 D-O3), so anything a model schedules for itself runs unattended with no acceptance criterion and delivers whatever it produced. `write` / `edit` let a model author the raw values a research agent is supposed to obtain from tools. A research desk carrying a video generator and a slide builder has more ways to answer a question with the wrong tool.

## Shape

- Denies six tools: `cron`, `edit`, `message`, `user_asset_delete`, `user_asset_upsert`, `write`.
- Disables every **global**-scope skill outside a small keep list (`xlsx`, `docx`, `pdf`, `feishu-doc`, `feishu-drive`) that the frontdesk routing map needs for file work. Org- and pack-scope skills are never touched.
- **Takes no request body, on purpose.** An endpoint that accepts a policy can also *widen* one, which would put a way to hand `write` or `cron` back to a model on the user-facing surface. This one only ever narrows, to a set the server owns, so there is nothing to review per call. Restoring the full manifest stays an operator action (`tool_policy: {}`) on the control plane.
- Idempotent: skills the engine already excludes are skipped, not re-disabled.
- A skill the engine refuses lands in `failed_skills` instead of aborting the pass — the tool policy has already been written by then, and an all-or-nothing failure would tell the caller nothing it could act on. The reported reason is the domain code, never the upstream message.
- Authorization is the same as the neighbouring v2 routes: owner-scoped workspace lookup plus `require_agents_v2`.

## Engine client

Two new methods, both deliberately separate from the existing ones:

- `set_agent_tool_policy` — not a field on `update_agent()`, because `tool_policy` is replace-on-write in controld while that call merges, and a merging caller would silently keep a policy it meant to drop.
- `set_agent_skill_enabled` — not `put_agent_skill()`, because a global skill has no version pin this service owns; the body carries `enabled` alone.

## Tests

30 new: 11 route tests driven over HTTP with `TestClient` (owner path, no-body-cannot-widen, idempotent second call, 404s for unknown/hidden/deleted/uninstalled/kill-switch-off with the engine never called, partial failure reported, tool-policy failure surfacing as 503), 6 service tests, 4 engine-client contract tests, plus one asserting the route is reachable on the real `create_app()` via the OpenAPI schema.

Verified against staging: `/agents/{workspace_id}/harden` currently answers 404 there while `/skills` and `/model` answer 401, i.e. the route is genuinely new.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01NwcPcWHHzuTsqy1dU8RJgj

---
