# SerendipityOneInc/ecap-workspace — commits 2026-10-10

## feat(marketing): add agent publishing guide at /guides/publish-agent (#4049)

- **SHA**: `194efc7720f0e4bd16fb1030f6cbdb86f8aaaf03`
- **作者**: Mori-srp
- **日期**: 2026-10-10T12:20:19Z
- **PR**: #4049

### Commit Message

```
feat(marketing): add agent publishing guide at /guides/publish-agent (#4049)

## What

Adds the ZooWork Agent publishing guide as an official marketing page,
in English and Chinese.

- English: `https://zoowork.ai/guides/publish-agent` · Chinese:
`https://zoowork.ai/zh/guides/publish-agent`. `/en/guides/publish-agent`
301s to the canonical English URL; other locales return 404.
- Uses the shared `MarketingChrome` header and footer. Resources
dropdown is now Blog, Docs, Publishing Guide, Events (hrefs collected in
`resource-hrefs.ts`). Footer unchanged.
- SEO: absolute title, description, single H1, self canonical, hreflang
`en` / `zh` / `x-default`, `HowTo` JSON-LD with the six stages, both
URLs in `sitemap-main.xml` (regenerated with `pnpm
render:sitemap-main`).
- Content ported from the internal guide v2.01 (Chinese text verbatim,
English from the guide's own translation). The in-page language toggle,
personal `workers.dev` demo link and internal Feishu link are not
published.
- API key screenshot: the token column is covered with a gray box on the
original image.
- Styles in Tailwind only (no route-level CSS). README in the guide
folder for future edits.

## Reconciled with Events (#4045)

Merged latest `main`. One shared fallback: a locale a route does not
offer goes to that locale's homepage in the language switcher, and
middleware returns 404 for it. The Events-only middleware branch is
replaced by this generic rule; `/zh/events` is still 404 and
`/en/events` still 301.

## Checks

Prettier, full ESLint, `tsc --noEmit`, 332 unit tests across events,
guides, route contract, sitemap, middleware, LanguageContext, LocaleLink
and landing-content. Manual: `/events`, `/guides/publish-agent`,
`/zh/guides/publish-agent` 200; `/zh/events`, `/ja/guides/publish-agent`
404.

No UTM on internal links.

---------

Co-authored-by: Mori-srp <266966641+Mori-srp@users.noreply.github.com>
```

### PR Body

## What

Adds the ZooWork Agent publishing guide as an official marketing page, in English and Chinese.

- English: `https://zoowork.ai/guides/publish-agent` · Chinese: `https://zoowork.ai/zh/guides/publish-agent`. `/en/guides/publish-agent` 301s to the canonical English URL; other locales return 404.
- Uses the shared `MarketingChrome` header and footer. Resources dropdown is now Blog, Docs, Publishing Guide, Events (hrefs collected in `resource-hrefs.ts`). Footer unchanged.
- SEO: absolute title, description, single H1, self canonical, hreflang `en` / `zh` / `x-default`, `HowTo` JSON-LD with the six stages, both URLs in `sitemap-main.xml` (regenerated with `pnpm render:sitemap-main`).
- Content ported from the internal guide v2.01 (Chinese text verbatim, English from the guide's own translation). The in-page language toggle, personal `workers.dev` demo link and internal Feishu link are not published.
- API key screenshot: the token column is covered with a gray box on the original image.
- Styles in Tailwind only (no route-level CSS). README in the guide folder for future edits.

## Reconciled with Events (#4045)

Merged latest `main`. One shared fallback: a locale a route does not offer goes to that locale's homepage in the language switcher, and middleware returns 404 for it. The Events-only middleware branch is replaced by this generic rule; `/zh/events` is still 404 and `/en/events` still 301.

## Checks

Prettier, full ESLint, `tsc --noEmit`, 332 unit tests across events, guides, route contract, sitemap, middleware, LanguageContext, LocaleLink and landing-content. Manual: `/events`, `/guides/publish-agent`, `/zh/guides/publish-agent` 200; `/zh/events`, `/ja/guides/publish-agent` 404.

No UTM on internal links.


---

## feat(claw-interface): add team org members directly by uid (#4050)

- **SHA**: `42928f0d76eb855337fd967d4d865bf3980c2cd4`
- **作者**: tim-srp
- **日期**: 2026-10-10T10:09:32Z
- **PR**: #4050

### Commit Message

```
feat(claw-interface): add team org members directly by uid (#4050)

## Summary

Adds `POST /internal/orgs/{org_id}/members`, which puts an existing
account
into a **team** organization by uid — no invite code, no email matching,
no
source-organization shutdown, and no Agent provisioning. It is the
claw-interface half of the Workforce enterprise feature: members added
this way
have their billing key bound to the enterprise org's team, so their
usage
bills the enterprise's shared wallet.

The existing `POST /orgs/{org_id}/join` cannot serve this: it requires
the
invite's email to equal the joining account's email (so a phone-only
identity
can never use it), requires an explicit confirmation that the caller's
own
personal environment will be shut down, and provisions a default main
Agent.
`docs/superpowers/specs/2026-10-10-workforce-enterprise-credits.md`
records
that the Agent creation is not suppressible in that flow, so this adds a
separate administrative path instead of changing it. The invite flow is
untouched.

### Contract

Request (unknown fields rejected, 422):

| Field | Type | Constraint |
|---|---|---|
| `business` | string | required, trimmed, 1–64; accepted business equal
to the target org creator's business |
| `uid` | string | required, trimmed, 1–128 |
| `role` | `"admin"` \| `"user"` | optional, default `"user"`; an
explicit `null` is rejected — omit it to leave an existing role alone |

Response 200:

```json
{"org_id":"existing-org-id","uid":"751","role":"user","status":"active","created":true,"joined_at":"2026-10-10T07:00:00Z"}
```

Errors, in the service's `{"code","detail"}` shape:

| Status | Code |
|---|---|
| 404 | `org.not_found` |
| 404 | `account.not_found` |
| 403 | `member.business_forbidden` |
| 400 | `member.org_not_team` |
| 409 | `member.active_membership_conflict` (existing org id kept in the
server-side context) |
| 409 | `member.add_conflict` (concurrent writer; retry) |
| 503 | `billing.unavailable` (local write compensated, so retrying the
same request is safe) |

Auth is the same as the neighbouring `POST
/internal/orgs/{org_id}/credits`:
the `/internal` router's `require_srp_account` gate plus
`require_admin_user`.

### Reuse, not a second membership path

Activation goes through a new shared helper,
`app/services/org/member_key_binding.py`, which performs the same three
steps
the invite join performs inline: bind the key to the org's billing team,
sync
the profile team projection, ensure the member usage-tracking row. The
invite
join's own copy is deliberately left alone — 18 tests patch its
module-level
binding calls, and redirecting it would rewrite coverage of the handoff
flow
for no behavioural gain. A bind failure compensates the local
membership: a row
this endpoint created is deleted, a retained row returns to its previous
status, so a membership is never left without its billing binding.

### `POST /orgs {"org_type":"team"}` as a target — verified, no code
change needed

The consumer creates the enterprise org itself with the creator's own
user JWT,
so I verified that org is a valid target rather than assuming it:

- `POST /orgs` (`app/routes/enterprise/org.py`) requires only
`require_account`
  (L1) — there is **no** paid-product-subscription gate anywhere in
  `org_service.create_org`.
- For `org_type == "team"` it subscribes the billing team to the default
  `starter_20_month` plan, creates the subscription and top-up wallets,
persists `billing_team_id` (the field this endpoint binds against), and
runs
  the creator's usage-tracking ensure.
- Blast-radius check on the new business:
`sales_policy.is_api_platform()`
raises `billing.unknown_business` for an unconfigured business, and that
is
called from Agent install (sandbox class), purchase and the credits read
—
**not** from `POST /orgs`. The endpoint that matters here is gated only
by
  token verification.

**Config prerequisite, not a code change:** the deployed environment
must list
the business in `EXTRA_ACCOUNT_BUSINESSES` (e.g.
`workforce-training,workforce-agency`; it lives in the Vault-backed
`vault-claw-interface-env` secret). Without it, token verification
rejects the
business with 401 on every authenticated route, `POST /orgs` never runs,
and
this endpoint returns `403 member.business_forbidden`. I did not change
any
deployment config — this is a note for whoever enables the feature.

### Docs

`docs/superpowers/specs/2026-10-10-workforce-org-member-add.md` — a
companion
note next to the credits contract, covering the auth, the exact
semantics
table against the email-invite path, the explicit no-Agent /
no-source-org-
shutdown statement, the error table, the target-org provisioning
finding, and
the config prerequisites.

## Test plan

- [x] `tests/unit/test_internal_org_member_add.py` — 22 tests: auth gate
+
route registration, happy path with the billing bind asserted on the
org's
  `billing_team_id`, idempotent replay with and without an explicit role
  change, `409` conflict when the uid is active in another org, inactive
other-org row not blocking, suspended same-org row reactivated in place,
personal-org `400`, unknown org/creator/account, business mismatch at
three
values, unconfigured-gateway `503` with nothing written, both
compensation
  branches, and Agent provisioning not happening (asserted at the shared
provisioning entry point plus a structural guard on the module source).
- [x] Full unit suite: **11,913 passed, 5 skipped** (baseline `11,891
passed,
  5 skipped` + the 22 new).
- [x] `bash scripts/verify-py.sh` — ruff check, ruff format --check,
pyright
  `app/ tests/`, import-linter **8 contracts kept**.
- [x] All 8 `scripts/ci-lint/*.sh` guards pass (file length, complexity,
  deptry, collection-name, importlinter repo sync, dead code, pydantic
  returns).
- [ ] Not verified locally: `tests/bdd` and the real-Mongo paths. This
machine
has no Mongo with the `mongo`/`mongo` credentials
`tests/bdd/conftest.py`
  expects (255 skipped locally; CI supplies one), and there is no
`tests/integration` directory in this service. Unit stubs do not
exercise the
  encrypted Mongo client, so the membership write still needs staging
verification — called out in the spec's verification-boundary section
rather
  than claimed here.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5 <noreply@anthropic.com>
```

### PR Body

## Summary

Adds `POST /internal/orgs/{org_id}/members`, which puts an existing account
into a **team** organization by uid — no invite code, no email matching, no
source-organization shutdown, and no Agent provisioning. It is the
claw-interface half of the Workforce enterprise feature: members added this way
have their billing key bound to the enterprise org's team, so their usage
bills the enterprise's shared wallet.

The existing `POST /orgs/{org_id}/join` cannot serve this: it requires the
invite's email to equal the joining account's email (so a phone-only identity
can never use it), requires an explicit confirmation that the caller's own
personal environment will be shut down, and provisions a default main Agent.
`docs/superpowers/specs/2026-10-10-workforce-enterprise-credits.md` records
that the Agent creation is not suppressible in that flow, so this adds a
separate administrative path instead of changing it. The invite flow is
untouched.

### Contract

Request (unknown fields rejected, 422):

| Field | Type | Constraint |
|---|---|---|
| `business` | string | required, trimmed, 1–64; accepted business equal to the target org creator's business |
| `uid` | string | required, trimmed, 1–128 |
| `role` | `"admin"` \| `"user"` | optional, default `"user"`; an explicit `null` is rejected — omit it to leave an existing role alone |

Response 200:

```json
{"org_id":"existing-org-id","uid":"751","role":"user","status":"active","created":true,"joined_at":"2026-10-10T07:00:00Z"}
```

Errors, in the service's `{"code","detail"}` shape:

| Status | Code |
|---|---|
| 404 | `org.not_found` |
| 404 | `account.not_found` |
| 403 | `member.business_forbidden` |
| 400 | `member.org_not_team` |
| 409 | `member.active_membership_conflict` (existing org id kept in the server-side context) |
| 409 | `member.add_conflict` (concurrent writer; retry) |
| 503 | `billing.unavailable` (local write compensated, so retrying the same request is safe) |

Auth is the same as the neighbouring `POST /internal/orgs/{org_id}/credits`:
the `/internal` router's `require_srp_account` gate plus `require_admin_user`.

### Reuse, not a second membership path

Activation goes through a new shared helper,
`app/services/org/member_key_binding.py`, which performs the same three steps
the invite join performs inline: bind the key to the org's billing team, sync
the profile team projection, ensure the member usage-tracking row. The invite
join's own copy is deliberately left alone — 18 tests patch its module-level
binding calls, and redirecting it would rewrite coverage of the handoff flow
for no behavioural gain. A bind failure compensates the local membership: a row
this endpoint created is deleted, a retained row returns to its previous
status, so a membership is never left without its billing binding.

### `POST /orgs {"org_type":"team"}` as a target — verified, no code change needed

The consumer creates the enterprise org itself with the creator's own user JWT,
so I verified that org is a valid target rather than assuming it:

- `POST /orgs` (`app/routes/enterprise/org.py`) requires only `require_account`
  (L1) — there is **no** paid-product-subscription gate anywhere in
  `org_service.create_org`.
- For `org_type == "team"` it subscribes the billing team to the default
  `starter_20_month` plan, creates the subscription and top-up wallets,
  persists `billing_team_id` (the field this endpoint binds against), and runs
  the creator's usage-tracking ensure.
- Blast-radius check on the new business: `sales_policy.is_api_platform()`
  raises `billing.unknown_business` for an unconfigured business, and that is
  called from Agent install (sandbox class), purchase and the credits read —
  **not** from `POST /orgs`. The endpoint that matters here is gated only by
  token verification.

**Config prerequisite, not a code change:** the deployed environment must list
the business in `EXTRA_ACCOUNT_BUSINESSES` (e.g.
`workforce-training,workforce-agency`; it lives in the Vault-backed
`vault-claw-interface-env` secret). Without it, token verification rejects the
business with 401 on every authenticated route, `POST /orgs` never runs, and
this endpoint returns `403 member.business_forbidden`. I did not change any
deployment config — this is a note for whoever enables the feature.

### Docs

`docs/superpowers/specs/2026-10-10-workforce-org-member-add.md` — a companion
note next to the credits contract, covering the auth, the exact semantics
table against the email-invite path, the explicit no-Agent / no-source-org-
shutdown statement, the error table, the target-org provisioning finding, and
the config prerequisites.

## Test plan

- [x] `tests/unit/test_internal_org_member_add.py` — 22 tests: auth gate +
  route registration, happy path with the billing bind asserted on the org's
  `billing_team_id`, idempotent replay with and without an explicit role
  change, `409` conflict when the uid is active in another org, inactive
  other-org row not blocking, suspended same-org row reactivated in place,
  personal-org `400`, unknown org/creator/account, business mismatch at three
  values, unconfigured-gateway `503` with nothing written, both compensation
  branches, and Agent provisioning not happening (asserted at the shared
  provisioning entry point plus a structural guard on the module source).
- [x] Full unit suite: **11,913 passed, 5 skipped** (baseline `11,891 passed,
  5 skipped` + the 22 new).
- [x] `bash scripts/verify-py.sh` — ruff check, ruff format --check, pyright
  `app/ tests/`, import-linter **8 contracts kept**.
- [x] All 8 `scripts/ci-lint/*.sh` guards pass (file length, complexity,
  deptry, collection-name, importlinter repo sync, dead code, pydantic
  returns).
- [ ] Not verified locally: `tests/bdd` and the real-Mongo paths. This machine
  has no Mongo with the `mongo`/`mongo` credentials `tests/bdd/conftest.py`
  expects (255 skipped locally; CI supplies one), and there is no
  `tests/integration` directory in this service. Unit stubs do not exercise the
  encrypted Mongo client, so the membership write still needs staging
  verification — called out in the spec's verification-boundary section rather
  than claimed here.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(marketing): add official Events page at /events (#4045)

- **SHA**: `d38db0883ba0d3284949da07624af70ee9c2bf05`
- **作者**: Mori-srp
- **日期**: 2026-10-10T08:52:35Z
- **PR**: #4045

### Commit Message

```
feat(marketing): add official Events page at /events (#4045)

## What

Adds an official Events page at `https://zoowork.ai/events`, built
inside the main site so it uses the shared `LandingHeader` /
`LandingFooter`.

- Page under `web/app/src/app/[locale]/(marketing)/events/`; English
only (`availableLocales: ['en']`).
- `/en/events` 301s to `/events`; non-English `/events` (e.g.
`/zh/events`) return a real 404 from middleware (the page-level
`notFound()` streamed a 200 because of the parent `loading.tsx`).
- Resources nav gets `Events` (internal link, same tab). Footer
unchanged.
- `sitemap-main.xml` regenerated with `https://zoowork.ai/events` (66
URLs). Root `sitemap.xml` unchanged.
- SEO: title, description, canonical, OG/Twitter share image (1200×630),
and 7 `Event` JSON-LD items generated from the same data as the visible
cards.
- All event content lives in `events-data.ts` so marketing can update
events by editing one file.

Supersedes #4042 and SerendipityOneInc/zoowork-events#1 (separate-repo
approach dropped).

## Checks run locally

Prettier, ESLint, `tsc --noEmit`, 272 unit tests in the affected suites
plus a new `events-schema` spec, middleware suites (159). Manual:
`/events` 200, `/en/events` 301, `/zh/events` 404.

No UTM on internal links. No new analytics or consent code.

---------

Co-authored-by: Mori-srp <266966641+Mori-srp@users.noreply.github.com>
```

### PR Body

## What

Adds an official Events page at `https://zoowork.ai/events`, built inside the main site so it uses the shared `LandingHeader` / `LandingFooter`.

- Page under `web/app/src/app/[locale]/(marketing)/events/`; English only (`availableLocales: ['en']`).
- `/en/events` 301s to `/events`; non-English `/events` (e.g. `/zh/events`) return a real 404 from middleware (the page-level `notFound()` streamed a 200 because of the parent `loading.tsx`).
- Resources nav gets `Events` (internal link, same tab). Footer unchanged.
- `sitemap-main.xml` regenerated with `https://zoowork.ai/events` (66 URLs). Root `sitemap.xml` unchanged.
- SEO: title, description, canonical, OG/Twitter share image (1200×630), and 7 `Event` JSON-LD items generated from the same data as the visible cards.
- All event content lives in `events-data.ts` so marketing can update events by editing one file.

Supersedes #4042 and SerendipityOneInc/zoowork-events#1 (separate-repo approach dropped).

## Checks run locally

Prettier, ESLint, `tsc --noEmit`, 272 unit tests in the affected suites plus a new `events-schema` spec, middleware suites (159). Manual: `/events` 200, `/en/events` 301, `/zh/events` 404.

No UTM on internal links. No new analytics or consent code.


---

## feat(seo): advertise blog sitemap in robots.txt and allow Google-Extended (#4041)

- **SHA**: `85f50312c0011b0bd66cc00a023e620dfe8e6f10`
- **作者**: Mori-srp
- **日期**: 2026-10-10T08:52:23Z
- **PR**: #4041

### Commit Message

```
feat(seo): advertise blog sitemap in robots.txt and allow Google-Extended (#4041)

## What

Two small changes to `robots.txt` on zoowork.ai:

1. **Advertise the Blog sitemap.** Add `Sitemap:
https://zoowork.ai/blog/sitemap-index.xml` next to the existing root
sitemap, so search engines can discover all Blog posts. The Blog index
is itself a sitemap index, so it is declared in `robots.txt` instead of
being nested inside the root index. Tips is intentionally **not** added
(content quality still being fixed).
2. **Allow `Google-Extended`.** Remove the `Disallow: /` rule for
`Google-Extended`, so Gemini can use our public pages. All other AI
crawler blocks (GPTBot, ClaudeBot, CCBot, Applebot-Extended, Amazonbot,
meta-externalagent) are unchanged.

## Also updated

- `web/app/scripts/audit-public-seo.ts`: expected sitemap directives now
include the Blog index.
- `tests/unit/app/_seo.unit.spec.ts`: asserts exactly these two sitemap
lines.
- `docs/seo/zoowork_marketing_url_contract.md`: records the 2026-10-09
decision.

## Checks

- `_seo.unit.spec.ts`: 18 passed.
- Reviewed separately; no blocking issues.

Note: `audit-public-seo.ts` already fails on `main` because it expects 2
root sitemap children while `public/sitemap.xml` has 3 (agent-gallery
was added). That is pre-existing and not touched here.

---------

Co-authored-by: Mori-srp <266966641+Mori-srp@users.noreply.github.com>
```

### PR Body

## What

Two small changes to `robots.txt` on zoowork.ai:

1. **Advertise the Blog sitemap.** Add `Sitemap: https://zoowork.ai/blog/sitemap-index.xml` next to the existing root sitemap, so search engines can discover all Blog posts. The Blog index is itself a sitemap index, so it is declared in `robots.txt` instead of being nested inside the root index. Tips is intentionally **not** added (content quality still being fixed).
2. **Allow `Google-Extended`.** Remove the `Disallow: /` rule for `Google-Extended`, so Gemini can use our public pages. All other AI crawler blocks (GPTBot, ClaudeBot, CCBot, Applebot-Extended, Amazonbot, meta-externalagent) are unchanged.

## Also updated

- `web/app/scripts/audit-public-seo.ts`: expected sitemap directives now include the Blog index.
- `tests/unit/app/_seo.unit.spec.ts`: asserts exactly these two sitemap lines.
- `docs/seo/zoowork_marketing_url_contract.md`: records the 2026-10-09 decision.

## Checks

- `_seo.unit.spec.ts`: 18 passed.
- Reviewed separately; no blocking issues.

Note: `audit-public-seo.ts` already fails on `main` because it expects 2 root sitemap children while `public/sitemap.xml` has 3 (agent-gallery was added). That is pre-existing and not touched here.


---

## fix(agents): remove redundant install link close button (#4048)

- **SHA**: `d4d774a456b176a1dbf9df8dc325d98a226a8f49`
- **作者**: kaka-srp
- **日期**: 2026-10-10T08:31:49Z
- **PR**: #4048

### Commit Message

```
fix(agents): remove redundant install link close button (#4048)

## Summary
Remove the redundant footer Close button from the Agent install link
dialog. The existing top-right × closes the dialog, while the footer
keeps Publish and Create install link.

## Root cause
The dialog offered two controls for the same close action. Remove the
unused footer label and update the existing close/reopen test to use the
top-right control.

## Test plan
- [x] Related publication tests: 8 passed.
- [x] ESLint on all three changed files.
- [x] Git diff whitespace check.
- [x] Frontend governance guards.
- Local full TypeScript check did not pass: this `--no-node` worktree
reused dependencies from the older primary checkout, resolving stale
`@zooclaw/design-system` / `@zooclaw/chat-ui` contracts and missing
newer dependencies (for example `fast-xml-parser`). CI will validate the
complete dependency installation, types, and build.
```

### PR Body

## Summary
Remove the redundant footer Close button from the Agent install link dialog. The existing top-right × closes the dialog, while the footer keeps Publish and Create install link.

## Root cause
The dialog offered two controls for the same close action. Remove the unused footer label and update the existing close/reopen test to use the top-right control.

## Test plan
- [x] Related publication tests: 8 passed.
- [x] ESLint on all three changed files.
- [x] Git diff whitespace check.
- [x] Frontend governance guards.
- Local full TypeScript check did not pass: this `--no-node` worktree reused dependencies from the older primary checkout, resolving stale `@zooclaw/design-system` / `@zooclaw/chat-ui` contracts and missing newer dependencies (for example `fast-xml-parser`). CI will validate the complete dependency installation, types, and build.


---

## feat: add idempotent administrative org credit grants (#4047)

- **SHA**: `0534daf5c3a83e71ff5b3a8a5e3817283a14cb98`
- **作者**: tim-srp
- **日期**: 2026-10-10T07:37:43Z
- **PR**: #4047

### Commit Message

```
feat: add idempotent administrative org credit grants (#4047)

## Summary

Revised per requested minimal architecture: Workforce owns enterprise
mapping, member orchestration, credit codes, admin-only redemption and
UI. Claw-interface adds one generic staff-admin grant endpoint targeting
an existing team wallet:

`POST /internal/orgs/{org_id}/credits`

This forward revision removes the original four Workforce-specific APIs,
service-token setting, enterprise mapping schema, and special
membership/billing changes. Existing
account/org/invite/join/agent/balance behavior remains unchanged. No
payment order or bank record is fabricated.

## Safety and behavior

- Existing SRP staff + admin authentication; validates configured
business against target creator and active org-admin actor.
- Strict positive integer credits; immutable payload and
business/org/key namespace.
- Existing entitlement ledger and team-topup wallet fulfillment, no
personal-wallet grant or paid subscription gate.
- Atomic pending→granting claim, one dispatch winner, stable completed
receipts.
- **Unknown gateway/finalization outcome fails closed:** no automatic
redispatch after claim; `409 grant.reconciliation_required`, code stays
reserved. Operator reconciliation is required for stranded grants. No
claim of automatically recoverable exactly-once delivery across process
failures.
- Receipt contains no balance: balance refresh is separate and cannot
invalidate grant success.

## Integration contract

[Revised complete
contract](docs/superpowers/specs/2026-10-10-workforce-enterprise-credits.md)
lists endpoint schemas/errors, Workforce W1–W9, existing API sequence
and recovery requirements.

Existing reusable flow has explicit constraints: verified email
invitation, existing default main Agent on join, personal-org migration
confirmation/paid-plan eligibility, model/metering prerequisites,
existing rounded balance response. Original
no-default-agent/silent-membership-upsert/phone-only promises are **not
implemented** by this narrowed change. Backend staff JWT is broad
privilege, not business-scoped machine auth.

## Verification

- Final unit suite: **11,891 passed, 5 skipped**, 4 warnings (99.94
seconds).
- Focused org/invite/billing/business/auth/grant suite: **198 passed**.
- `scripts/verify-py.sh`: ruff, format, pyright and all 8 import
contracts passed.
- Parent independent review and remote CI are still pending; native
implementation/review fallback was disclosed because Claude Fable quota
is unavailable. No claim of a fresh Claude review for this rewrite.

## Release boundary

Draft; no deployment, merge, Vault/token changes or live billing
requests. Staging encrypted-Mongo CAS, actual LLM/tool/sandbox shared
debits, model bootstrap, member Mattermost behavior, zero-balance errors
and operational reconciliation still require live acceptance. Unit mocks
do not prove these boundaries.

---------

Co-authored-by: Claude Fable 5.1 <noreply@anthropic.com>
```

### PR Body

## Summary

Revised per requested minimal architecture: Workforce owns enterprise mapping, member orchestration, credit codes, admin-only redemption and UI. Claw-interface adds one generic staff-admin grant endpoint targeting an existing team wallet:

`POST /internal/orgs/{org_id}/credits`

This forward revision removes the original four Workforce-specific APIs, service-token setting, enterprise mapping schema, and special membership/billing changes. Existing account/org/invite/join/agent/balance behavior remains unchanged. No payment order or bank record is fabricated.

## Safety and behavior

- Existing SRP staff + admin authentication; validates configured business against target creator and active org-admin actor.
- Strict positive integer credits; immutable payload and business/org/key namespace.
- Existing entitlement ledger and team-topup wallet fulfillment, no personal-wallet grant or paid subscription gate.
- Atomic pending→granting claim, one dispatch winner, stable completed receipts.
- **Unknown gateway/finalization outcome fails closed:** no automatic redispatch after claim; `409 grant.reconciliation_required`, code stays reserved. Operator reconciliation is required for stranded grants. No claim of automatically recoverable exactly-once delivery across process failures.
- Receipt contains no balance: balance refresh is separate and cannot invalidate grant success.

## Integration contract

[Revised complete contract](docs/superpowers/specs/2026-10-10-workforce-enterprise-credits.md) lists endpoint schemas/errors, Workforce W1–W9, existing API sequence and recovery requirements.

Existing reusable flow has explicit constraints: verified email invitation, existing default main Agent on join, personal-org migration confirmation/paid-plan eligibility, model/metering prerequisites, existing rounded balance response. Original no-default-agent/silent-membership-upsert/phone-only promises are **not implemented** by this narrowed change. Backend staff JWT is broad privilege, not business-scoped machine auth.

## Verification

- Final unit suite: **11,891 passed, 5 skipped**, 4 warnings (99.94 seconds).
- Focused org/invite/billing/business/auth/grant suite: **198 passed**.
- `scripts/verify-py.sh`: ruff, format, pyright and all 8 import contracts passed.
- Parent independent review and remote CI are still pending; native implementation/review fallback was disclosed because Claude Fable quota is unavailable. No claim of a fresh Claude review for this rewrite.

## Release boundary

Draft; no deployment, merge, Vault/token changes or live billing requests. Staging encrypted-Mongo CAS, actual LLM/tool/sandbox shared debits, model bootstrap, member Mattermost behavior, zero-balance errors and operational reconciliation still require live acceptance. Unit mocks do not prove these boundaries.


---

## feat(auth): accept configured extra account businesses (#4043)

- **SHA**: `f6c29b83a7739d1f3eb446ef38176e323117e09c`
- **作者**: tim-srp
- **日期**: 2026-10-10T03:42:51Z
- **PR**: #4043

### Commit Message

```
feat(auth): accept configured extra account businesses (#4043)

claw-interface accepted only `ecap` and `ecap-platform`, and rejected
every other account business in two places: the token routing hint (`401
Unsupported account business`) and the billing policy branch
(`billing.unknown_business` — which also governs the Agent sandbox class
and the credits read). A new product business therefore could not be
onboarded without a code change.

Read extra businesses from `EXTRA_ACCOUNT_BUSINESSES` (comma-separated,
empty by default) so onboarding becomes a configuration change. `ecap`
and `ecap-platform` stay built in and cannot be configured away; a
configured business bills as an ordinary product account rather than as
Platform. Unconfigured environments keep rejecting everything else, so
this ships closed.

## Summary
- Add `EXTRA_ACCOUNT_BUSINESSES` and `accepted_businesses()`, and drive
the token business gate from it. Extract the repeated `"ecap"` fallback
into `DEFAULT_BUSINESS`.
- Treat a configured business as an ordinary product account in
`is_api_platform()`, instead of raising `billing.unknown_business`. That
error previously broke Agent install (sandbox class) and the credits
read for any business outside the two built-ins.
- Document the setting in `.env.example` and the Platform operations
runbook.

## Test plan
- [x] `tests/unit/test_business_allowlist.py` — 33 passed. Covers both
gates for configured and unconfigured environments, the two values this
unblocks (`workforce-training`, `workforce-agency`), the built-in
fallbacks, and the legacy `zoowork` billing row.
- [x] Related existing suites (auth, middleware, platform, billing) —
215 passed.
- [x] `bash scripts/verify-py.sh` passed: ruff, ruff-format, pyright and
import-linter (8 contracts kept).

## Rollout
The values only take effect once an environment sets
`EXTRA_ACCOUNT_BUSINESSES` (for example
`workforce-training,workforce-agency`). This PR adds the switch;
enabling a specific business remains a deployment configuration step.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Review follow-up
- Codex flagged (P1) that a malformed `business` claim — a JSON list or
object — escaped as `TypeError: unhashable type` from the new set
membership, producing a 500 on every authenticated route. Reproduced
against the PR head and against `origin/main` (the previous tuple
comparison simply rejected it), then fixed: only a missing or empty
claim means a pre-claim ZooWork token; any other non-string claim
returns the same 401 as an unknown business. `is_api_platform()` now
fails closed on an unhashable value from a dict caller. Regression cases
added for list, dict, number, boolean, empty list and empty object
claims.
- Test count is now 42 in `test_business_allowlist.py`; 272 passed
across the related suites.
```

### PR Body

claw-interface accepted only `ecap` and `ecap-platform`, and rejected every other account business in two places: the token routing hint (`401 Unsupported account business`) and the billing policy branch (`billing.unknown_business` — which also governs the Agent sandbox class and the credits read). A new product business therefore could not be onboarded without a code change.

Read extra businesses from `EXTRA_ACCOUNT_BUSINESSES` (comma-separated, empty by default) so onboarding becomes a configuration change. `ecap` and `ecap-platform` stay built in and cannot be configured away; a configured business bills as an ordinary product account rather than as Platform. Unconfigured environments keep rejecting everything else, so this ships closed.

## Summary
- Add `EXTRA_ACCOUNT_BUSINESSES` and `accepted_businesses()`, and drive the token business gate from it. Extract the repeated `"ecap"` fallback into `DEFAULT_BUSINESS`.
- Treat a configured business as an ordinary product account in `is_api_platform()`, instead of raising `billing.unknown_business`. That error previously broke Agent install (sandbox class) and the credits read for any business outside the two built-ins.
- Document the setting in `.env.example` and the Platform operations runbook.

## Test plan
- [x] `tests/unit/test_business_allowlist.py` — 33 passed. Covers both gates for configured and unconfigured environments, the two values this unblocks (`workforce-training`, `workforce-agency`), the built-in fallbacks, and the legacy `zoowork` billing row.
- [x] Related existing suites (auth, middleware, platform, billing) — 215 passed.
- [x] `bash scripts/verify-py.sh` passed: ruff, ruff-format, pyright and import-linter (8 contracts kept).

## Rollout
The values only take effect once an environment sets `EXTRA_ACCOUNT_BUSINESSES` (for example `workforce-training,workforce-agency`). This PR adds the switch; enabling a specific business remains a deployment configuration step.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Review follow-up
- Codex flagged (P1) that a malformed `business` claim — a JSON list or object — escaped as `TypeError: unhashable type` from the new set membership, producing a 500 on every authenticated route. Reproduced against the PR head and against `origin/main` (the previous tuple comparison simply rejected it), then fixed: only a missing or empty claim means a pre-claim ZooWork token; any other non-string claim returns the same 401 as an unknown business. `is_api_platform()` now fails closed on an unhashable value from a dict caller. Regression cases added for list, dict, number, boolean, empty list and empty object claims.
- Test count is now 42 in `test_business_allowlist.py`; 272 passed across the related suites.


---
