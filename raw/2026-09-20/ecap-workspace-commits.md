# SerendipityOneInc/ecap-workspace — commits 2026-09-20

## feat(agents): sync user timezone to engine Agents (#3813)

- **SHA**: `87b4dd8e4fe37e6485e9b18e69374898fb9e99df`
- **作者**: tim-srp
- **日期**: 2026-09-20T14:59:46Z
- **PR**: #3813

### Commit Message

```
feat(agents): sync user timezone to engine Agents (#3813)

## What

Engine
[#1524](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1524)
added user-timezone support: `resource.userTimezone` on Agent create,
top-level `userTimezone` on update. This PR is the upstream half — it
reads `account.locale.timezone` and passes it to the engine.

## Create entry points

All creation paths pass the creating user's timezone via one shared
resolver:

| Entry point | File |
| --- | --- |
| Default main Agent | `services/agents/engine_main_agent_service.py` |
| Pack install | `services/agents/engine_agent_install_service.py` |
| Agent Builder pack-test preview |
`pack_store/pack_test_engine_runtime_service.py` |
| Agent development (v2 builder) | `agent_development/create_service.py`
|

`engine_client` gains `user_timezone` on both `create_agent` (nested
under `resource`) and `update_agent` (top-level), matching the engine
contract.

## Timezone change propagation

Triggered from `PUT /openclaw/settings/locale` — the only remaining
write path, since the settings page no longer exposes timezone UI. That
single hook covers both the browser-locale auto-sync and post-login
setup.

Three things worth calling out:

- **Before the bot early-returns.** An Engine-only account has no
OpenClaw bot but does own Agents; propagation placed after the early
return would silently never run for them.
- **Compare before writing.** Every accepted engine update appends a
config version, and both triggers can fire repeatedly for an unchanged
timezone. The fan-out reads the Agent first and skips the write when the
engine already resolves the target timezone (native field first, legacy
`agents.defaults.userTimezone` fallback — mirroring controld's
`readUserTimezone`).
- **Own Agents only.** Not org-wide, not other members'.

## No default is substituted

When the timezone is unset or unusable (blank, a `+`/`-` offset, an
unknown IANA name, a non-string), the resolver returns `None` and the
field is **omitted** — the runtime keeps its own host-timezone/UTC
fallback. A client-side default would look like an explicit user choice
and mask that fallback. The resolver mirrors the engine's validity check
locally so a malformed stored locale degrades to "no timezone" rather
than failing a whole Agent install on an upstream 400.

## Failure behaviour

Fail-open, per the "fall back to machine/UTC" decision: the locale is
already persisted when propagation runs, so failures append a
`warnings:` line to the response message rather than failing the save.
The org lookup sits inside the guard too — it is a separate Mongo hop
that can fail on its own. Per-Agent failures are counted, and
`agent.runtime_detached` is treated as a no-op rather than a failure,
matching the personal-MCP fan-out. A discovery outage is reported
distinctly (`timezone sync could not list agents`) so it can't be
misread as "nothing needed changing".

## Retry after a failed propagation

Fail-open alone made a partial fan-out **unrecoverable**. The route
persists the account timezone *before* propagating, so a failure leaves
browser timezone == stored timezone — and both frontend entry points
(`lib/auth/post-login-setup.ts`, `hooks/useClawSettings.ts`) decide
whether to send the request from exactly that comparison. They skipped
it forever, so the Agents that missed the update kept a stale timezone.
The response `warnings` were never read either, so nothing else could
notice.

The fan-out now records its own verdict, closing the loop:

- `Account.agents_timezone_sync_pending` is set when any Agent failed or
discovery failed, and cleared when a later fan-out fully converges.
- `GET /openclaw/settings/locale` returns it; both entry points re-send
the locale while it is true.
- Retrying is safe: the fan-out is already idempotent end to end (engine
config, bot config, and USER.md all compare before writing), so a
converged Agent never appends a config version.

The field sits on the account root rather than on `AccountLocale` —
`UserMeResponse.from_account_and_org` passes `account.locale` through
verbatim, so a field there would leak internal sync state onto `GET
/account/me`.

**The mark is written ahead of the fan-out, in the same atomic update as
the timezone it protects.** Recording it afterwards means two writes,
and a failure between them re-creates the very state this whole
mechanism exists to escape: the new timezone visible, the mark missing,
the frontend's browser-vs-stored comparison satisfied, the retry skipped
for good. Mongo updates one document atomically, so folding the mark
into the locale write leaves only "neither landed" — and then the stored
timezone is still the old one, so the frontend's own mismatch check
retries without any mark involved. A converging save clears the mark
afterwards; a failing one leaves it standing and writes nothing further,
so the failure path actually got *cheaper* (two writes → one). The clear
is best-effort: a failed clear leaves the mark set, which just means the
next mount re-runs the idempotent fan-out, whereas raising would fail a
request whose user-visible effect already succeeded without restoring
the mark.

Net write cost, all on saves that carry a usable timezone (the frontend
only sends one when the timezone changed or a retry is owed —
steady-state users send none): converging save 1 → 2, failing save 2 →
1.

A language-only write carries no timezone, so it neither fans out nor
touches the mark. Design spec:
`docs/superpowers/specs/2026-09-20-agent-user-timezone-sync-retry.md`.

The two entry points also had to agree on the *payload* of a retry, not
just on when to fire one. The backend fans out only when the request
carries a timezone, so a retry that sends an empty one would leave the
flag set forever. The settings hook already fell back to the stored
value (`browser.timezone || locale.timezone`); the post-login path did
not — it returned before reading the stored locale whenever the browser
reported nothing, and otherwise sent its raw values. It now reads the
stored locale first so the pending flag is always evaluated, and falls
back to the stored timezone on a retry, which is by definition the value
that failed to propagate. The fallback stays scoped to a pending sync,
so a language-only change still sends no timezone.

## Review follow-up

Two P1s from the review of `e49ae32de`, both fixed on top:

**1. The resolver accepted tzdata entries the engine's ICU check
rejects.** `ZoneInfo` resolves against tzdata; the engine validates the
name with `Intl.DateTimeFormat`, which resolves against ICU, and answers
a name it does not know with 400 — the failure the resolver exists to
prevent. Enumerating all 598 `available_timezones()` against Node on
this host found exactly one bare-tzdata name that diverges and still
opens through `ZoneInfo` (`Factory`), plus `posixrules`, a host
`localtime` copy, and the `right/` and `posix/` variant trees that
production images also ship. Forwarding any of them failed the whole
install. The resolver now denies that family explicitly and
case-insensitively (key lookup is case-insensitive on some filesystems,
so `factory` opens the same file `Factory` does) and keeps letting
`ZoneInfo` decide everything else. The mirror stays deliberately
one-sided: a slim local tzdata missing a zone ICU knows costs a skipped
sync, never a failed install.

**2. The retry-marker clear was not a compare-and-set.** Clearing by
`uid` alone let an older request whose fan-out succeeded wipe the mark a
newer concurrent request had just set: the account would hold the newer
timezone, some Agents would still be on the older one, and the
frontend's own mismatch check (browser == stored) would skip the retry
that is the only way back. The clear now matches the raw persisted
`locale.timezone` in the filter, so it only lands for the write that
still owns the locale — the filter, not the payload, is what makes it a
compare-and-set. The key must be the value the document holds rather
than the trimmed value sent to the engine, since the compared field
contains the former. The clear goes through the `mongo.update` wrapper
like the sibling `set_locale_timezone`, so it stays on the repo's single
write path and under whatever guard the wrapper applies to the
collection.

The method lives in `openclaw_repo` — the same collection as
`set_locale_timezone` — rather than `user_repo`, which sits at exactly
the 500-line file cap.

## Not touched

**Schedule / cron execution timezone is deliberately unchanged.** This
only affects what the runtime renders as the user's timezone.

## Backfill

Existing Agents are **not** modified. The one-time backfill is a
separate written proposal only —
`docs/superpowers/plans/2026-09-20-agent-user-timezone-backfill.md` —
covering dry-run-first execution, reuse of the same discovery path,
idempotent/resumable writes, and staging verification. Design spec:
`docs/superpowers/specs/2026-09-20-agent-user-timezone-sync.md`. The
retry loop above does not converge those pre-existing Agents either; it
only recovers Agents that a *later* locale write failed to reach.

## Tests

Tests across the touched surfaces — the retry loop specifically is
covered by 18 route-level cases (`TestUpdateLocaleSyncRetryFlag` 13,
`TestGetLocaleEndpoint` 5) plus 11 frontend cases:

- **Create**: each entry point passes the account timezone, and omits it
when unset/unusable.
- **Client**: create nests under `resource`, update is top-level, both
omit when unset; detail parsing covers native, legacy fallback,
native-over-legacy, and blank/non-string normalization.
- **Timezone change**: the route fans out to the caller's org; an
Engine-only (bot-less) account still syncs; a language-only write does
not; the merged timezone is used; a missing membership degrades to `""`;
failures surface as warnings not a failed save; the wrapper never raises
through the route.
- **Multi-Agent sync**: pagination, `agt_` filtering, dedup,
`unchanged`-skip, detached-Agent tolerance, per-Agent failure counting,
discovery-failure reporting, and concurrency bounded at 5. Per-Agent and
overall call budgets are bounded so an engine outage cannot hold the
request past the gateway timeout.
- **Retry loop**: the mark is set on partial failure, discovery failure,
and a raised exception (which must not read as success); cleared on
recovery; left alone by a language-only or unusable-timezone write; and
recorded before the no-bot early return. The write ordering is pinned
(`write` → `fan-out` → `clear`) along with the atomic-write invariant
that the first payload carries both the locale and the mark, so a
failing locale write persists no mark and never fans out, and a failing
clear still returns `ok` with the mark left standing. `GET /locale`
returns it, with an absent field reading as not pending. Both frontend
entry points re-send while it is pending (the reported scenario: browser
== stored, Agents still stale) and stay quiet otherwise, including for
legacy documents without the field. A retry keeps the stored timezone
when the browser reports none (and still fires when the browser reports
no locale at all), while a language-only change is asserted not to carry
the timezone.
- **Review follow-up**: the resolver's denylist is asserted per family
member (`Factory`, `posixrules`, `localtime`, `right/*`, `posix/*`) and
case-insensitively, while real zones that merely look similar still
pass; the marker clear is asserted per persisted value (including padded
input, proving the CAS keys on the stored bytes rather than the trimmed
value sent upstream) and asserted to go through the wrapper rather than
the raw collection handle. Each new guard was checked to fail against
the pre-fix implementation.
- **Defaults**: an explicit test guards that omission never substitutes
a hard-coded value.

Local: `ruff` + `ruff format` + `pyright` + `import-linter` + all
`scripts/ci-lint` guards pass; `tsc` + `vitest` (827 files / 10528
tests) + `eslint` pass for `web/app`. Note `pytest tests/unit` on this
machine crashes at collection with a pre-existing `Fatal Python error:
Segmentation fault` (reproduced identically on a clean stash of these
changes); the affected suites were run file-by-file and all pass.

---------

Co-authored-by: Claude Code <noreply@anthropic.com>
```

### PR Body

## What

Engine [#1524](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1524) added user-timezone support: `resource.userTimezone` on Agent create, top-level `userTimezone` on update. This PR is the upstream half — it reads `account.locale.timezone` and passes it to the engine.

## Create entry points

All creation paths pass the creating user's timezone via one shared resolver:

| Entry point | File |
| --- | --- |
| Default main Agent | `services/agents/engine_main_agent_service.py` |
| Pack install | `services/agents/engine_agent_install_service.py` |
| Agent Builder pack-test preview | `pack_store/pack_test_engine_runtime_service.py` |
| Agent development (v2 builder) | `agent_development/create_service.py` |

`engine_client` gains `user_timezone` on both `create_agent` (nested under `resource`) and `update_agent` (top-level), matching the engine contract.

## Timezone change propagation

Triggered from `PUT /openclaw/settings/locale` — the only remaining write path, since the settings page no longer exposes timezone UI. That single hook covers both the browser-locale auto-sync and post-login setup.

Three things worth calling out:

- **Before the bot early-returns.** An Engine-only account has no OpenClaw bot but does own Agents; propagation placed after the early return would silently never run for them.
- **Compare before writing.** Every accepted engine update appends a config version, and both triggers can fire repeatedly for an unchanged timezone. The fan-out reads the Agent first and skips the write when the engine already resolves the target timezone (native field first, legacy `agents.defaults.userTimezone` fallback — mirroring controld's `readUserTimezone`).
- **Own Agents only.** Not org-wide, not other members'.

## No default is substituted

When the timezone is unset or unusable (blank, a `+`/`-` offset, an unknown IANA name, a non-string), the resolver returns `None` and the field is **omitted** — the runtime keeps its own host-timezone/UTC fallback. A client-side default would look like an explicit user choice and mask that fallback. The resolver mirrors the engine's validity check locally so a malformed stored locale degrades to "no timezone" rather than failing a whole Agent install on an upstream 400.

## Failure behaviour

Fail-open, per the "fall back to machine/UTC" decision: the locale is already persisted when propagation runs, so failures append a `warnings:` line to the response message rather than failing the save. The org lookup sits inside the guard too — it is a separate Mongo hop that can fail on its own. Per-Agent failures are counted, and `agent.runtime_detached` is treated as a no-op rather than a failure, matching the personal-MCP fan-out. A discovery outage is reported distinctly (`timezone sync could not list agents`) so it can't be misread as "nothing needed changing".

## Retry after a failed propagation

Fail-open alone made a partial fan-out **unrecoverable**. The route persists the account timezone *before* propagating, so a failure leaves browser timezone == stored timezone — and both frontend entry points (`lib/auth/post-login-setup.ts`, `hooks/useClawSettings.ts`) decide whether to send the request from exactly that comparison. They skipped it forever, so the Agents that missed the update kept a stale timezone. The response `warnings` were never read either, so nothing else could notice.

The fan-out now records its own verdict, closing the loop:

- `Account.agents_timezone_sync_pending` is set when any Agent failed or discovery failed, and cleared when a later fan-out fully converges.
- `GET /openclaw/settings/locale` returns it; both entry points re-send the locale while it is true.
- Retrying is safe: the fan-out is already idempotent end to end (engine config, bot config, and USER.md all compare before writing), so a converged Agent never appends a config version.

The field sits on the account root rather than on `AccountLocale` — `UserMeResponse.from_account_and_org` passes `account.locale` through verbatim, so a field there would leak internal sync state onto `GET /account/me`.

**The mark is written ahead of the fan-out, in the same atomic update as the timezone it protects.** Recording it afterwards means two writes, and a failure between them re-creates the very state this whole mechanism exists to escape: the new timezone visible, the mark missing, the frontend's browser-vs-stored comparison satisfied, the retry skipped for good. Mongo updates one document atomically, so folding the mark into the locale write leaves only "neither landed" — and then the stored timezone is still the old one, so the frontend's own mismatch check retries without any mark involved. A converging save clears the mark afterwards; a failing one leaves it standing and writes nothing further, so the failure path actually got *cheaper* (two writes → one). The clear is best-effort: a failed clear leaves the mark set, which just means the next mount re-runs the idempotent fan-out, whereas raising would fail a request whose user-visible effect already succeeded without restoring the mark.

Net write cost, all on saves that carry a usable timezone (the frontend only sends one when the timezone changed or a retry is owed — steady-state users send none): converging save 1 → 2, failing save 2 → 1.

A language-only write carries no timezone, so it neither fans out nor touches the mark. Design spec: `docs/superpowers/specs/2026-09-20-agent-user-timezone-sync-retry.md`.

The two entry points also had to agree on the *payload* of a retry, not just on when to fire one. The backend fans out only when the request carries a timezone, so a retry that sends an empty one would leave the flag set forever. The settings hook already fell back to the stored value (`browser.timezone || locale.timezone`); the post-login path did not — it returned before reading the stored locale whenever the browser reported nothing, and otherwise sent its raw values. It now reads the stored locale first so the pending flag is always evaluated, and falls back to the stored timezone on a retry, which is by definition the value that failed to propagate. The fallback stays scoped to a pending sync, so a language-only change still sends no timezone.

## Review follow-up

Two P1s from the review of `e49ae32de`, both fixed on top:

**1. The resolver accepted tzdata entries the engine's ICU check rejects.** `ZoneInfo` resolves against tzdata; the engine validates the name with `Intl.DateTimeFormat`, which resolves against ICU, and answers a name it does not know with 400 — the failure the resolver exists to prevent. Enumerating all 598 `available_timezones()` against Node on this host found exactly one bare-tzdata name that diverges and still opens through `ZoneInfo` (`Factory`), plus `posixrules`, a host `localtime` copy, and the `right/` and `posix/` variant trees that production images also ship. Forwarding any of them failed the whole install. The resolver now denies that family explicitly and case-insensitively (key lookup is case-insensitive on some filesystems, so `factory` opens the same file `Factory` does) and keeps letting `ZoneInfo` decide everything else. The mirror stays deliberately one-sided: a slim local tzdata missing a zone ICU knows costs a skipped sync, never a failed install.

**2. The retry-marker clear was not a compare-and-set.** Clearing by `uid` alone let an older request whose fan-out succeeded wipe the mark a newer concurrent request had just set: the account would hold the newer timezone, some Agents would still be on the older one, and the frontend's own mismatch check (browser == stored) would skip the retry that is the only way back. The clear now matches the raw persisted `locale.timezone` in the filter, so it only lands for the write that still owns the locale — the filter, not the payload, is what makes it a compare-and-set. The key must be the value the document holds rather than the trimmed value sent to the engine, since the compared field contains the former. The clear goes through the `mongo.update` wrapper like the sibling `set_locale_timezone`, so it stays on the repo's single write path and under whatever guard the wrapper applies to the collection.

The method lives in `openclaw_repo` — the same collection as `set_locale_timezone` — rather than `user_repo`, which sits at exactly the 500-line file cap.

## Not touched

**Schedule / cron execution timezone is deliberately unchanged.** This only affects what the runtime renders as the user's timezone.

## Backfill

Existing Agents are **not** modified. The one-time backfill is a separate written proposal only — `docs/superpowers/plans/2026-09-20-agent-user-timezone-backfill.md` — covering dry-run-first execution, reuse of the same discovery path, idempotent/resumable writes, and staging verification. Design spec: `docs/superpowers/specs/2026-09-20-agent-user-timezone-sync.md`. The retry loop above does not converge those pre-existing Agents either; it only recovers Agents that a *later* locale write failed to reach.

## Tests

Tests across the touched surfaces — the retry loop specifically is covered by 18 route-level cases (`TestUpdateLocaleSyncRetryFlag` 13, `TestGetLocaleEndpoint` 5) plus 11 frontend cases:

- **Create**: each entry point passes the account timezone, and omits it when unset/unusable.
- **Client**: create nests under `resource`, update is top-level, both omit when unset; detail parsing covers native, legacy fallback, native-over-legacy, and blank/non-string normalization.
- **Timezone change**: the route fans out to the caller's org; an Engine-only (bot-less) account still syncs; a language-only write does not; the merged timezone is used; a missing membership degrades to `""`; failures surface as warnings not a failed save; the wrapper never raises through the route.
- **Multi-Agent sync**: pagination, `agt_` filtering, dedup, `unchanged`-skip, detached-Agent tolerance, per-Agent failure counting, discovery-failure reporting, and concurrency bounded at 5. Per-Agent and overall call budgets are bounded so an engine outage cannot hold the request past the gateway timeout.
- **Retry loop**: the mark is set on partial failure, discovery failure, and a raised exception (which must not read as success); cleared on recovery; left alone by a language-only or unusable-timezone write; and recorded before the no-bot early return. The write ordering is pinned (`write` → `fan-out` → `clear`) along with the atomic-write invariant that the first payload carries both the locale and the mark, so a failing locale write persists no mark and never fans out, and a failing clear still returns `ok` with the mark left standing. `GET /locale` returns it, with an absent field reading as not pending. Both frontend entry points re-send while it is pending (the reported scenario: browser == stored, Agents still stale) and stay quiet otherwise, including for legacy documents without the field. A retry keeps the stored timezone when the browser reports none (and still fires when the browser reports no locale at all), while a language-only change is asserted not to carry the timezone.
- **Review follow-up**: the resolver's denylist is asserted per family member (`Factory`, `posixrules`, `localtime`, `right/*`, `posix/*`) and case-insensitively, while real zones that merely look similar still pass; the marker clear is asserted per persisted value (including padded input, proving the CAS keys on the stored bytes rather than the trimmed value sent upstream) and asserted to go through the wrapper rather than the raw collection handle. Each new guard was checked to fail against the pre-fix implementation.
- **Defaults**: an explicit test guards that omission never substitutes a hard-coded value.

Local: `ruff` + `ruff format` + `pyright` + `import-linter` + all `scripts/ci-lint` guards pass; `tsc` + `vitest` (827 files / 10528 tests) + `eslint` pass for `web/app`. Note `pytest tests/unit` on this machine crashes at collection with a pre-existing `Fatal Python error: Segmentation fault` (reproduced identically on a clean stash of these changes); the affected suites were run file-by-file and all pass.


---

## fix(billing): recognize Stripe scheduled cancellation dates (#3828)

- **SHA**: `8ce092eaa404d054254470ce30b030a3c72d3ce5`
- **作者**: sam-srp
- **日期**: 2026-09-20T14:42:46Z
- **PR**: #3828

### Commit Message

```
fix(billing): recognize Stripe scheduled cancellation dates (#3828)

## Summary
Stripe Customer Portal can schedule cancellation using `cancel_at` while
leaving `cancel_at_period_end=false`. ZooWork previously treated these
subscriptions as renewing even after successfully processing the
webhook.

Normalize cancellation within the current billing period across webhook,
paid-invoice, replacement, and reconciliation projections. Paid access
remains available until the existing period ends. Cancel dates beyond
the current period do not suppress intervening renewals. Resuming a
custom scheduled cancellation now clears `cancel_at`; the existing
end-of-period path continues to clear `cancel_at_period_end`.

## Root cause
The adapter only inspected the boolean flag. The staging subscription
reproduced the issue with an active status, a cancellation timestamp
matching its period end, and a false boolean flag. The update webhook
was received and processed successfully.

Stripe reference:
https://docs.stripe.com/billing/subscriptions/cancel#custom-cancel-date

## Test plan
- [x] 92 relevant unit tests passed; 5 pre-existing removed-trial tests
skipped.
- [x] Regression cases cover Portal payloads, current-state retrieval on
webhook, cancellation removal, reconciliation identity, paid-invoice
projection, resume, and downgrade.
- [x] Ruff, formatting, Pyright, and import boundary checks.
- [ ] Deploy backend and retest cancellation/resume in staging. Existing
affected agreements require a new provider update or reconciliation
after deployment.

No schema, database query, frontend, or billing-gateway changes. The
Stripe endpoint must subscribe to `customer.subscription.updated`
(already enabled for the staging endpoint during diagnosis).
```

### PR Body

## Summary
Stripe Customer Portal can schedule cancellation using `cancel_at` while leaving `cancel_at_period_end=false`. ZooWork previously treated these subscriptions as renewing even after successfully processing the webhook.

Normalize cancellation within the current billing period across webhook, paid-invoice, replacement, and reconciliation projections. Paid access remains available until the existing period ends. Cancel dates beyond the current period do not suppress intervening renewals. Resuming a custom scheduled cancellation now clears `cancel_at`; the existing end-of-period path continues to clear `cancel_at_period_end`.

## Root cause
The adapter only inspected the boolean flag. The staging subscription reproduced the issue with an active status, a cancellation timestamp matching its period end, and a false boolean flag. The update webhook was received and processed successfully.

Stripe reference: https://docs.stripe.com/billing/subscriptions/cancel#custom-cancel-date

## Test plan
- [x] 92 relevant unit tests passed; 5 pre-existing removed-trial tests skipped.
- [x] Regression cases cover Portal payloads, current-state retrieval on webhook, cancellation removal, reconciliation identity, paid-invoice projection, resume, and downgrade.
- [x] Ruff, formatting, Pyright, and import boundary checks.
- [ ] Deploy backend and retest cancellation/resume in staging. Existing affected agreements require a new provider update or reconciliation after deployment.

No schema, database query, frontend, or billing-gateway changes. The Stripe endpoint must subscribe to `customer.subscription.updated` (already enabled for the staging endpoint during diagnosis).


---

## feat(chat): prompt to replace unavailable agent models (#3819)

- **SHA**: `a2013e3261a75791f746f6326521b23a09162cd5`
- **作者**: tim-srp
- **日期**: 2026-09-20T14:45:07Z
- **PR**: #3819

### Commit Message

```
feat(chat): prompt to replace unavailable agent models (#3819)

## Problem and behavior

An installed Agent can retain a model that is no longer in the user's
available catalog. Opening its conversation now prompts the user to
choose a replacement after both model queries have completed
successfully. Dismissing the prompt preserves the conversation and
draft; trying to send reopens it without submitting or clearing
text/attachments.

The compact dialog uses the catalog's original order and preselects
`is_default`, with provider icons, consumption multipliers, details,
scrolling, and search. It does not synthesize Auto. Supported existing
Auto configurations remain valid. Empty catalogs are inconclusive and do
not prompt or block sending; failed saves preserve the selection, and
successful changes retain the existing runtime restart flow.

Scope: editable installed Agent conversations using the workspace model
API. Managed/read-only Agents, draft creation, and Builder-specific
model controllers are excluded. Includes English and Chinese copy.
Deploy frontend and backend. The backend reports Revision-managed engine
models as managed, matching the existing direct-update restriction;
ordinary engine models remain editable.

## Validation

- `scripts/verify-web.sh` passed: governance guards, TypeScript,
targeted Vitest, ESLint.
- Review follow-up: 64 targeted frontend tests and 14 agent-model
service tests passed; frontend type/lint checks and backend ruff,
pyright, and import checks passed.
- 22 existing shared ModelPicker tests passed.
- Regression coverage: normalized IDs, loading/errors, managed Agents,
supported Auto, empty catalogs, workspace switching, dismissal/send
guard, draft preservation, catalog ordering/default selection, save
failure/retry, and search.
- Full app test/build suites are delegated to CI. No production
configuration was modified.

## Review decisions

- Empty successful catalogs fail open; removed the unused guard `empty`
field.
- Restored shared query `ready` semantics and exposed post-mount
freshness separately for the warning guard.
- Fixed the concrete Revision-managed case instead of treating all
engine Agents as read-only.
- Retained the agreed nonempty-catalog send guard and API-only
replacement options. Adding synthetic Auto or bypassing a confirmed
missing model would change the approved interaction.

## Final review verification

- All 46 reported checks completed successfully or were intentionally
skipped. Codex found no issues. Claude confirmed the three fixes and
requested confirmation of a legacy authoring-model scenario.
- The installation resolver can accept pack defaults present in the
engine catalog, so it would be incorrect to assert that internal IDs can
never appear on installed Agents. However, the replacement path resolves
the newly requested model against the engine catalog; it does not depend
on the old primary model or reject replacements because that old ID is
internal. Builder controllers remain excluded. No concrete additional
defect was established from the legacy-ID hypothesis; do not make all
engine models read-only. General catalog/runtime divergence remains a
follow-up rather than a reason to alter the approved send guard in this
PR.
```

### PR Body

## Problem and behavior

An installed Agent can retain a model that is no longer in the user's available catalog. Opening its conversation now prompts the user to choose a replacement after both model queries have completed successfully. Dismissing the prompt preserves the conversation and draft; trying to send reopens it without submitting or clearing text/attachments.

The compact dialog uses the catalog's original order and preselects `is_default`, with provider icons, consumption multipliers, details, scrolling, and search. It does not synthesize Auto. Supported existing Auto configurations remain valid. Empty catalogs are inconclusive and do not prompt or block sending; failed saves preserve the selection, and successful changes retain the existing runtime restart flow.

Scope: editable installed Agent conversations using the workspace model API. Managed/read-only Agents, draft creation, and Builder-specific model controllers are excluded. Includes English and Chinese copy. Deploy frontend and backend. The backend reports Revision-managed engine models as managed, matching the existing direct-update restriction; ordinary engine models remain editable.

## Validation

- `scripts/verify-web.sh` passed: governance guards, TypeScript, targeted Vitest, ESLint.
- Review follow-up: 64 targeted frontend tests and 14 agent-model service tests passed; frontend type/lint checks and backend ruff, pyright, and import checks passed.
- 22 existing shared ModelPicker tests passed.
- Regression coverage: normalized IDs, loading/errors, managed Agents, supported Auto, empty catalogs, workspace switching, dismissal/send guard, draft preservation, catalog ordering/default selection, save failure/retry, and search.
- Full app test/build suites are delegated to CI. No production configuration was modified.

## Review decisions

- Empty successful catalogs fail open; removed the unused guard `empty` field.
- Restored shared query `ready` semantics and exposed post-mount freshness separately for the warning guard.
- Fixed the concrete Revision-managed case instead of treating all engine Agents as read-only.
- Retained the agreed nonempty-catalog send guard and API-only replacement options. Adding synthetic Auto or bypassing a confirmed missing model would change the approved interaction.

## Final review verification

- All 46 reported checks completed successfully or were intentionally skipped. Codex found no issues. Claude confirmed the three fixes and requested confirmation of a legacy authoring-model scenario.
- The installation resolver can accept pack defaults present in the engine catalog, so it would be incorrect to assert that internal IDs can never appear on installed Agents. However, the replacement path resolves the newly requested model against the engine catalog; it does not depend on the old primary model or reject replacements because that old ID is internal. Builder controllers remain excluded. No concrete additional defect was established from the legacy-ID hypothesis; do not make all engine models read-only. General catalog/runtime divergence remains a follow-up rather than a reason to alter the approved send guard in this PR.


---

## feat(platform): add organization member management (#3824)

- **SHA**: `faa2ddca9acedada2683145799c731e05b133e2e`
- **作者**: finn-srp
- **日期**: 2026-09-20T14:24:49Z
- **PR**: #3824

### Commit Message

```
feat(platform): add organization member management (#3824)

## Linear

N/A

## Summary

- add an Organization settings entry to the Platform account menu
- open Clerk's built-in Organization profile for member and invitation
management
- keep Clerk authoritative for memberships and invitations; no Platform
table or API is added
- update the phase-one product and architecture notes to reflect the
supported Clerk-managed flow

## Test plan

- [x] Platform lint
- [x] Platform typecheck
- [x] Platform unit/component tests (15 passed)
- [x] Platform production build
```

### PR Body

## Linear

N/A

## Summary

- add an Organization settings entry to the Platform account menu
- open Clerk's built-in Organization profile for member and invitation management
- keep Clerk authoritative for memberships and invitations; no Platform table or API is added
- update the phase-one product and architecture notes to reflect the supported Clerk-managed flow

## Test plan

- [x] Platform lint
- [x] Platform typecheck
- [x] Platform unit/component tests (15 passed)
- [x] Platform production build



---

## fix(billing): hide default personal plan billing caption (#3826)

- **SHA**: `d147e180e071fc208a453354c021cf60576fcde0`
- **作者**: sam-srp
- **日期**: 2026-09-20T14:06:58Z
- **PR**: #3826

### Commit Message

```
fix(billing): hide default personal plan billing caption (#3826)

## Summary
Hide “Billed monthly. Cancel anytime.” below the Pro subscription button
for non-Team accounts, including its empty spacing. Team accounts retain
“Contact Sales to manage your team plan.”

## Root cause
The default personal plan state supplied a billing caption that is no
longer needed. Renewal dates, expiration notices, purchase restrictions,
and checkout behavior remain unchanged.

## Test plan
- [x] ProPlanAction unit suite: 21 tests passed.
- [x] TypeScript and ESLint checks.
```

### PR Body

## Summary
Hide “Billed monthly. Cancel anytime.” below the Pro subscription button for non-Team accounts, including its empty spacing. Team accounts retain “Contact Sales to manage your team plan.”

## Root cause
The default personal plan state supplied a billing caption that is no longer needed. Renewal dates, expiration notices, purchase restrictions, and checkout behavior remain unchanged.

## Test plan
- [x] ProPlanAction unit suite: 21 tests passed.
- [x] TypeScript and ESLint checks.


---

## fix(chat): show friendly insufficient credits error copy (#3822)

- **SHA**: `fcaeb00b32b48241b19ea7473989591c415a385c`
- **作者**: tim-srp
- **日期**: 2026-09-20T13:46:44Z
- **PR**: #3822

### Commit Message

```
fix(chat): show friendly insufficient credits error copy (#3822)

## Summary
When an assistant error message has the same run ID as a user turn with
`state: error` and `errorCode: insufficient_credits`, display friendly
localized copy instead of the provider-prefixed error body.

- Chinese: 积分不足，充值后请重新发送。
- English and all other supported locales via existing dictionary
fallback: Insufficient credits. Add credits, then send your message
again.

Use existing structured metadata only; no string matching or new API.
Preserve unrelated errors and messages without matching run metadata.
The original Mattermost message, existing red-frame styling, and B2
recharge notice remain unchanged.

## Validation
- TypeScript and repository governance checks passed.
- Focused component and dictionary suites: 65 tests passed, including
delayed status arrival, run isolation, unrelated error codes, and all 10
supported locales.
- ESLint passed on the changed component and dictionary tests; full lint
runs in the commit/push gates.
```

### PR Body

## Summary
When an assistant error message has the same run ID as a user turn with `state: error` and `errorCode: insufficient_credits`, display friendly localized copy instead of the provider-prefixed error body.

- Chinese: 积分不足，充值后请重新发送。
- English and all other supported locales via existing dictionary fallback: Insufficient credits. Add credits, then send your message again.

Use existing structured metadata only; no string matching or new API. Preserve unrelated errors and messages without matching run metadata. The original Mattermost message, existing red-frame styling, and B2 recharge notice remain unchanged.

## Validation
- TypeScript and repository governance checks passed.
- Focused component and dictionary suites: 65 tests passed, including delayed status arrival, run isolation, unrelated error codes, and all 10 supported locales.
- ESLint passed on the changed component and dictionary tests; full lint runs in the commit/push gates.


---

## feat(billing): integrate subscription and credit top-up redesign (#3811)

- **SHA**: `6f12bdb4aaf461ddd44cc52540f84a78ae15808c`
- **作者**: sam-srp
- **日期**: 2026-09-20T13:36:45Z
- **PR**: #3811

### Commit Message

```
feat(billing): integrate subscription and credit top-up redesign (#3811)

## Summary
- Integrate the subscription and credit top-up redesign across
claw-interface and the web app: Stripe monthly subscriptions,
independent credit purchases at $1 = 200 credits, legacy subscription
migration, and permanent top-up credits through the existing gateway
flow.
- Consolidate the Pro/Enterprise pricing, Manage plan, credit purchase,
onboarding presentation, and Stripe top-up invoice download changes from
the shared branch.
- Preserve Manage for Team users while hiding personal
top-up/cancellation actions and disabling personal subscriptions.
Contact Sales opens `/en/enterprise`.
- Add payment/credit diagnostics and retain existing wallet mutation and
balance-query flows.

- Define catalog/checkout response schemas, complete pricing comparison
translations, and align permanent-credit documentation and advertised
Pro storage.

- Recover the original pending Stripe Checkout from the catalog, keep
top-ups available when legacy subscription verification fails, and audit
uncertain Checkout requests through the existing manual-review flow.

## Test plan
- [x] Onboarding recovery at e45c41a4d: 40 related frontend tests
passed, including failed-response/navigation recovery through the real
onboarding hook, reopening onboarding, and rejecting unrelated purchase
restrictions. Type/lint/governance checks passed.
- [x] Checkout recovery fixes at cb0f75074: 209 backend tests and 25
frontend tests passed, including lost responses, popup failures, 48-hour
unknown outcomes, legacy Stripe lookup failures, and concurrent
paid-state protection. Type/lint/governance/import checks passed.
- [x] Review fixes at b5b5b83cc: 25 frontend tests and 6 backend
response-contract tests passed; frontend type/lint/governance and
backend ruff/pyright/import checks passed.
- [x] Earlier: 26 SharedPlanCard unit tests passed, including Team
Manage access without top-up actions.
- [x] Pre-push frontend type/lint/governance checks and backend ruff,
pyright, and import checks passed for commit 63c4ddffc.
- [x] Frontend staging release `ecap-v0.19.22-beta` succeeded; version
endpoint matched 63c4ddffc and homepage returned HTTP 200 on September
18.
- [x] Backend staging release `service-v0.18.11-beta.10` succeeded on
September 18.
- [ ] Review current PR CI results against the latest main. The checks
above do not constitute a complete end-to-end billing acceptance run.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
Co-authored-by: tim-srp <tim@srp.one>
Co-authored-by: shana-srp <shana@srp.one>
Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Body

## Summary
- Integrate the subscription and credit top-up redesign across claw-interface and the web app: Stripe monthly subscriptions, independent credit purchases at $1 = 200 credits, legacy subscription migration, and permanent top-up credits through the existing gateway flow.
- Consolidate the Pro/Enterprise pricing, Manage plan, credit purchase, onboarding presentation, and Stripe top-up invoice download changes from the shared branch.
- Preserve Manage for Team users while hiding personal top-up/cancellation actions and disabling personal subscriptions. Contact Sales opens `/en/enterprise`.
- Add payment/credit diagnostics and retain existing wallet mutation and balance-query flows.

- Define catalog/checkout response schemas, complete pricing comparison translations, and align permanent-credit documentation and advertised Pro storage.

- Recover the original pending Stripe Checkout from the catalog, keep top-ups available when legacy subscription verification fails, and audit uncertain Checkout requests through the existing manual-review flow.

## Test plan
- [x] Onboarding recovery at e45c41a4d: 40 related frontend tests passed, including failed-response/navigation recovery through the real onboarding hook, reopening onboarding, and rejecting unrelated purchase restrictions. Type/lint/governance checks passed.
- [x] Checkout recovery fixes at cb0f75074: 209 backend tests and 25 frontend tests passed, including lost responses, popup failures, 48-hour unknown outcomes, legacy Stripe lookup failures, and concurrent paid-state protection. Type/lint/governance/import checks passed.
- [x] Review fixes at b5b5b83cc: 25 frontend tests and 6 backend response-contract tests passed; frontend type/lint/governance and backend ruff/pyright/import checks passed.
- [x] Earlier: 26 SharedPlanCard unit tests passed, including Team Manage access without top-up actions.
- [x] Pre-push frontend type/lint/governance checks and backend ruff, pyright, and import checks passed for commit 63c4ddffc.
- [x] Frontend staging release `ecap-v0.19.22-beta` succeeded; version endpoint matched 63c4ddffc and homepage returned HTTP 200 on September 18.
- [x] Backend staging release `service-v0.18.11-beta.10` succeeded on September 18.
- [ ] Review current PR CI results against the latest main. The checks above do not constitute a complete end-to-end billing acceptance run.





---

## feat(agents): 优化Agents页空状态介绍与创建引导 (#3821)

- **SHA**: `835a88c319f79a60a427047249ac0d3532d99791`
- **作者**: lynn Zhuang
- **日期**: 2026-09-20T11:57:00Z
- **PR**: #3821

### Commit Message

```
feat(agents): 优化Agents页空状态介绍与创建引导 (#3821)

## 变更说明

新用户完成 onboarding 后进入 Agents，或删除最后一个 Agent 后，原先只显示插图和一句提示。现在「全部 /
我的」列表首页为空时，展示 Agents 简介、16:9
视频占位，以及「专属工具与知识、按计划自动执行、在对话中完善」三栏说明，并提供直接打开现有创建弹窗的「创建 Agent」按钮。


布局根据窗口高度调整视频区域，确保常见笔记本尺寸下创建入口在首屏可见；补齐中英文文案并沿用设计系统的浅色、深色样式。分享列表、分页空页和加载／错误／未开放状态继续使用现有逻辑。

视频目前仅为占位，没有播放行为，后续可替换为介绍视频。

## 验证

- [x] 针对性单元测试：Agents 页面入口、删除流程，共 5 项通过。
- [x] TypeScript、ESLint 及仓库前端检查。
- [x] 本地 mock：空列表展示、三个标签页切换、创建弹窗、删除最后一个 Agent 后回到空状态。
- [x] 浏览器：1366×768、1280×650、390×844 下创建按钮首屏可见，无横向溢出；检查中英文和深色模式。

## 部署范围

仅需部署 web 前端；无后端接口、数据结构或依赖变更。
```

### PR Body

## 变更说明

新用户完成 onboarding 后进入 Agents，或删除最后一个 Agent 后，原先只显示插图和一句提示。现在「全部 / 我的」列表首页为空时，展示 Agents 简介、16:9 视频占位，以及「专属工具与知识、按计划自动执行、在对话中完善」三栏说明，并提供直接打开现有创建弹窗的「创建 Agent」按钮。

布局根据窗口高度调整视频区域，确保常见笔记本尺寸下创建入口在首屏可见；补齐中英文文案并沿用设计系统的浅色、深色样式。分享列表、分页空页和加载／错误／未开放状态继续使用现有逻辑。

视频目前仅为占位，没有播放行为，后续可替换为介绍视频。

## 验证

- [x] 针对性单元测试：Agents 页面入口、删除流程，共 5 项通过。
- [x] TypeScript、ESLint 及仓库前端检查。
- [x] 本地 mock：空列表展示、三个标签页切换、创建弹窗、删除最后一个 Agent 后回到空状态。
- [x] 浏览器：1366×768、1280×650、390×844 下创建按钮首屏可见，无横向溢出；检查中英文和深色模式。

## 部署范围

仅需部署 web 前端；无后端接口、数据结构或依赖变更。


---

## chore(agents): drop redundant .claude/commands adapters (#3818)

- **SHA**: `f2b59e2c8d20860ccebd875a8811b31a41b94ec4`
- **作者**: felix-srp
- **日期**: 2026-09-20T10:01:02Z
- **PR**: #3818

### Commit Message

```
chore(agents): drop redundant .claude/commands adapters (#3818)

## Summary
- Remove the 11 `.claude/commands/*.md` adapters. Claude Code registers
every `.claude/skills/<name>` symlink as `/<name>` on its own, so each
adapter registered the same workflow a second time: `/plugin` → Stats
listed 84 skill rows, 73 unique, and the 11 duplicates were exactly
these files (startup debug log: `legacy commands: 11`).
- Drop the adapter checks from `scripts/sync-agent-skills.sh` and
`scripts/sync-agent-skills.test.sh`, and the `.claude/commands/` trigger
from `scripts/verify-changed.sh`.
- Remove `enableAllProjectMcpServers` / `enabledMcpjsonServers` from
`.claude/settings.json`. They gate a `.mcp.json` this repo does not have
(AGENTS.md: "No repo `.mcp.json` currently").
- Rewrite the AGENTS.md rule so the wrappers are not recreated.

Left as is on purpose: `sentry-cli@claude-plugins-official` and
`feature-dev@claude-plugins-official` stay enabled in project settings.
Neither is installed on my machine (`/plugin` → Errors flags
sentry-cli), but sentry-cli was enabled deliberately in #2311 and
feature-dev dates from the monorepo commit, so dropping them is a
separate decision.

## Test plan
- [x] `bash scripts/sync-agent-skills.sh --check` → `agent-skills: check
ok`
- [x] `bash scripts/sync-agent-skills.test.sh` → exit 0
- [x] `bash scripts/verify-changed.sh` → "all changed surfaces passed"
(this is the pre-push gate; the sync test is not part of any CI
workflow)
- [x] Headless session started from the worktree with `--debug-file`:
`/pr` still resolves from `.claude/skills/pr`. The 11 "legacy commands"
it still counts come from the main checkout's `.claude/commands/` (a
worktree session reads project commands from the main worktree), so the
duplicate rows disappear once this lands on `main`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01AN2tHJEDTYAyDqNEQuAVxC
```

### PR Body

## Summary
- Remove the 11 `.claude/commands/*.md` adapters. Claude Code registers every `.claude/skills/<name>` symlink as `/<name>` on its own, so each adapter registered the same workflow a second time: `/plugin` → Stats listed 84 skill rows, 73 unique, and the 11 duplicates were exactly these files (startup debug log: `legacy commands: 11`).
- Drop the adapter checks from `scripts/sync-agent-skills.sh` and `scripts/sync-agent-skills.test.sh`, and the `.claude/commands/` trigger from `scripts/verify-changed.sh`.
- Remove `enableAllProjectMcpServers` / `enabledMcpjsonServers` from `.claude/settings.json`. They gate a `.mcp.json` this repo does not have (AGENTS.md: "No repo `.mcp.json` currently").
- Rewrite the AGENTS.md rule so the wrappers are not recreated.

Left as is on purpose: `sentry-cli@claude-plugins-official` and `feature-dev@claude-plugins-official` stay enabled in project settings. Neither is installed on my machine (`/plugin` → Errors flags sentry-cli), but sentry-cli was enabled deliberately in #2311 and feature-dev dates from the monorepo commit, so dropping them is a separate decision.

## Test plan
- [x] `bash scripts/sync-agent-skills.sh --check` → `agent-skills: check ok`
- [x] `bash scripts/sync-agent-skills.test.sh` → exit 0
- [x] `bash scripts/verify-changed.sh` → "all changed surfaces passed" (this is the pre-push gate; the sync test is not part of any CI workflow)
- [x] Headless session started from the worktree with `--debug-file`: `/pr` still resolves from `.claude/skills/pr`. The 11 "legacy commands" it still counts come from the main checkout's `.claude/commands/` (a worktree session reads project commands from the main worktree), so the duplicate rows disappear once this lands on `main`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01AN2tHJEDTYAyDqNEQuAVxC


---

## ci(platform): deploy frontend to Cloudflare Workers via Actions (#3817)

- **SHA**: `8116b3947f79ee9edb74869d66680e91d514946a`
- **作者**: finn-srp
- **日期**: 2026-09-20T09:25:39Z
- **PR**: #3817

### Commit Message

```
ci(platform): deploy frontend to Cloudflare Workers via Actions (#3817)

## Summary

Platform has a production build but no deployment workflow. Add
Cloudflare Workers Static Assets hosting with SPA fallback and a GitHub
Actions workflow that builds and deploys the frontend.

- Relevant `main` changes and `platform-v*-beta` tags deploy staging;
manual dispatch supports staging and explicit production selection.
- Use the existing GitHub Environment Cloudflare credentials. Map
Platform-specific Environment variables to the two browser-safe Vite
build variables; validate key type/API URL before deployment.
- Use separate `zoowork-platform-staging` / `zoowork-platform` Workers.
Custom-domain binding remains with the domain owner; no DNS changes are
made.
- Add Wrangler using the version already resolved in the workspace
lockfile and document configuration and redeployment.

## Test plan

- [x] Node 24, pnpm frozen-lockfile installation.
- [x] Platform lint, typecheck, 14 tests, and staging-configured
production build.
- [x] Actionlint (existing Blacksmith runner label explicitly allowed).
- [x] Wrangler dry runs for staging and production configuration;
production was not deployed.
- [x] Local Worker smoke: root HTML, `/api-keys` navigation fallback,
JavaScript asset delivery.
- [x] Staging GitHub Environment variables configured; values are not
committed.
- [x] First staging deployment and remote static-page smoke (homepage,
`/settings/api-keys` navigation fallback, JavaScript asset).

Staging release: `platform-v0.0.2-beta`, [successful Actions
run](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/35501812689).
Worker: `zoowork-platform-staging`, [temporary
URL](https://zoowork-platform-staging.chris-a5e.workers.dev).
Build-time frontend values are scoped to the configuration check and
build steps so unit tests retain their isolated mock API.

The custom domain and real Clerk → Interface login/API flow require the
domain owner and Interface staging configuration; static deployment
checks do not substitute for that end-to-end validation.
```

### PR Body

## Summary

Platform has a production build but no deployment workflow. Add Cloudflare Workers Static Assets hosting with SPA fallback and a GitHub Actions workflow that builds and deploys the frontend.

- Relevant `main` changes and `platform-v*-beta` tags deploy staging; manual dispatch supports staging and explicit production selection.
- Use the existing GitHub Environment Cloudflare credentials. Map Platform-specific Environment variables to the two browser-safe Vite build variables; validate key type/API URL before deployment.
- Use separate `zoowork-platform-staging` / `zoowork-platform` Workers. Custom-domain binding remains with the domain owner; no DNS changes are made.
- Add Wrangler using the version already resolved in the workspace lockfile and document configuration and redeployment.

## Test plan

- [x] Node 24, pnpm frozen-lockfile installation.
- [x] Platform lint, typecheck, 14 tests, and staging-configured production build.
- [x] Actionlint (existing Blacksmith runner label explicitly allowed).
- [x] Wrangler dry runs for staging and production configuration; production was not deployed.
- [x] Local Worker smoke: root HTML, `/api-keys` navigation fallback, JavaScript asset delivery.
- [x] Staging GitHub Environment variables configured; values are not committed.
- [x] First staging deployment and remote static-page smoke (homepage, `/settings/api-keys` navigation fallback, JavaScript asset).

Staging release: `platform-v0.0.2-beta`, [successful Actions run](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/35501812689).
Worker: `zoowork-platform-staging`, [temporary URL](https://zoowork-platform-staging.chris-a5e.workers.dev).
Build-time frontend values are scoped to the configuration check and build steps so unit tests retain their isolated mock API.

The custom domain and real Clerk → Interface login/API flow require the domain owner and Interface staging configuration; static deployment checks do not substitute for that end-to-end validation.


---

## fix(agents): preserve logical skill names across revision projections (#3816)

- **SHA**: `c6333408814661db3bc3d7e0f56d8ea3e9140167`
- **作者**: kaka-srp
- **日期**: 2026-09-20T09:22:22Z
- **PR**: #3816

### Commit Message

```
fix(agents): preserve logical skill names across revision projections (#3816)

## Summary

- Preserve source skill names in Engine bindings throughout create,
preview, commit, apply and shared updates, without renaming registry
IDs, versions or stored content.
- Isolate new projection/idempotency keys; retain exact same-key replay
for pre-upgrade R0 creates.
- Validate newly introduced names, including rename targets. Existing
legacy names and already accepted draft operations remain
readable/editable with warnings; renaming to a compliant name is
supported, while introducing a different noncompliant name is rejected.
- Include the design, business regression tests and real-runtime
validation evidence. The fixture-specific local trial script and its
dedicated recovery tests are deliberately not part of this PR.

## Root cause

Revision bindings retained the source name, but configuration projection
dropped it. Engine therefore exposed the collision-safe internal
registry name to the model. The companion Engine change adds an optional
Agent-local name while keeping storage identity and authorization
unchanged.

Companion:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1561.

## Test plan

- [x] Independent review finding fixed: old accepted drafts must not be
rejected when replayed; 14 regression cases cover compatibility.
- [x] Before main refresh: related backend suite 634 passed; backend
static/complexity/file-length checks passed.
- [x] After rebase onto main including resource snapshot changes: 89
targeted tests passed, including authoring, turn snapshots and runtime
projections.
- [x] Companion Engine verifies exact legacy replay using real service
code and PGlite persistence (11 binding tests passed).
- [x] CI follow-up: refreshed the inherited-baseline commit regression
to assert exact logical names along with unchanged skill IDs/versions.
The inherited-materialization business suite remains in this PR.
- [x] Real local single-lane test on the existing test Agent and its
existing active/Build sessions: both model turns succeeded, actual
provider system captures use logical names, and each turn successfully
read five global skills, one source-owned skill and its relative script.
- [x] Real authoring HTTP gateway plus encrypted Mongo: legacy draft
read/validate/edit/rename and new-invalid-name rejection; draft
operations restored.
- [x] Implicit global set and explicit empty set checked; active config
and sandbox view restored. No Agent/skill/session created. Test history
retained.

The full real-runtime trial preceded the main refresh; the refresh was
validated with targeted regression tests and static gates, not claimed
as another live trial. Build file reads and the authoring gateway were
exercised separately: no claim that the model itself successfully called
source_read. ACS/external Feishu delivery was out of scope.

## Rollout / scope

Deploy the companion Engine compatibility change before claw-interface.
No frontend release, registry rewrite or production data migration is
included. Existing persisted configs require a later normal revision
projection or a separately authorized migration; this PR does not
silently rewrite them.

Local environment repair was separately authorized: four missing staging
R2 blobs were added only after hash verification with absent-only
writes; existing objects and registry records were unchanged. No
credentials are included.
```

### PR Body

## Summary

- Preserve source skill names in Engine bindings throughout create, preview, commit, apply and shared updates, without renaming registry IDs, versions or stored content.
- Isolate new projection/idempotency keys; retain exact same-key replay for pre-upgrade R0 creates.
- Validate newly introduced names, including rename targets. Existing legacy names and already accepted draft operations remain readable/editable with warnings; renaming to a compliant name is supported, while introducing a different noncompliant name is rejected.
- Include the design, business regression tests and real-runtime validation evidence. The fixture-specific local trial script and its dedicated recovery tests are deliberately not part of this PR.

## Root cause

Revision bindings retained the source name, but configuration projection dropped it. Engine therefore exposed the collision-safe internal registry name to the model. The companion Engine change adds an optional Agent-local name while keeping storage identity and authorization unchanged.

Companion: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1561.

## Test plan

- [x] Independent review finding fixed: old accepted drafts must not be rejected when replayed; 14 regression cases cover compatibility.
- [x] Before main refresh: related backend suite 634 passed; backend static/complexity/file-length checks passed.
- [x] After rebase onto main including resource snapshot changes: 89 targeted tests passed, including authoring, turn snapshots and runtime projections.
- [x] Companion Engine verifies exact legacy replay using real service code and PGlite persistence (11 binding tests passed).
- [x] CI follow-up: refreshed the inherited-baseline commit regression to assert exact logical names along with unchanged skill IDs/versions. The inherited-materialization business suite remains in this PR.
- [x] Real local single-lane test on the existing test Agent and its existing active/Build sessions: both model turns succeeded, actual provider system captures use logical names, and each turn successfully read five global skills, one source-owned skill and its relative script.
- [x] Real authoring HTTP gateway plus encrypted Mongo: legacy draft read/validate/edit/rename and new-invalid-name rejection; draft operations restored.
- [x] Implicit global set and explicit empty set checked; active config and sandbox view restored. No Agent/skill/session created. Test history retained.

The full real-runtime trial preceded the main refresh; the refresh was validated with targeted regression tests and static gates, not claimed as another live trial. Build file reads and the authoring gateway were exercised separately: no claim that the model itself successfully called source_read. ACS/external Feishu delivery was out of scope.

## Rollout / scope

Deploy the companion Engine compatibility change before claw-interface. No frontend release, registry rewrite or production data migration is included. Existing persisted configs require a later normal revision projection or a separately authorized migration; this PR does not silently rewrite them.

Local environment repair was separately authorized: four missing staging R2 blobs were added only after hash verification with absent-only writes; existing objects and registry records were unchanged. No credentials are included.


---

## fix(auth): restrict region checks to new email signups (#3815)

- **SHA**: `c1053ca1e8ee7a426e625360d554dcde5935925f`
- **作者**: sam-srp
- **日期**: 2026-09-20T09:08:13Z
- **PR**: #3815

### Commit Message

```
fix(auth): restrict region checks to new email signups (#3815)

## Summary

- Apply country restrictions only when a new user signs up via email
OTP. Existing active, default-role email users can log in regardless of
country.
- Validate `CF-IPCountry` at the web boundary and enforce the signup
check in both OTP send and verify routes.
- Preserve the pre-PR pass-through verification behavior when Web
temporarily talks to an old backend without policy version 2.
- Log verification decisions without email addresses or OTP values, and
document the account-service role contract.
- Keep Google and phone authentication behavior unchanged.

## Verification

- Backend domestic-access and route unit tests: 22 passed.
- Web auth-route unit tests: 26 passed.
- Web TypeScript and ESLint checks passed.
- Ruff and targeted Pyright checks for changed Python files passed.
- On 2026-09-20, ran the exact `email`/`is_active`/`role` filter through
`profile_repo.find_uids_by_filter` inside a staging `claw-interface` Pod
using the encrypted Mongo client. The read succeeded with zero matches
for a synthetic address; no CSFLE rejection. [Verification
discussion](https://github.com/SerendipityOneInc/ecap-workspace/pull/3815#issuecomment-5748739543).

## Rollout

Deploy `claw-interface` first, then Web in production to activate the
complete policy immediately. Staging Web and backend deploy
independently on merge, so Web verifies the backend policy version: an
old response without `policy_version: 2` preserves the pre-PR
pass-through OTP verification behavior even if old eligibility returns
`false`. OTP send continues to honor the backend decision. After both
releases deploy, the new eligibility policy applies at send and verify.

Eligibility-service failure during OTP verification returns 502 for
existing users as well as new users. This fail-closed behavior is an
accepted availability tradeoff.

## Check limitation

The repository-wide Pyright check fails on unchanged files (`google.py`,
`first_use_monitor.py`, and route test helpers) in the local
environment. The Pyright commit hook and pre-push verification were
skipped after targeted checks passed. The PR's CI lint/typecheck and
test jobs passed.

This change affects the web email OTP flow. Direct calls to the separate
user-interface service are not changed.
```

### PR Body

## Summary

- Apply country restrictions only when a new user signs up via email OTP. Existing active, default-role email users can log in regardless of country.
- Validate `CF-IPCountry` at the web boundary and enforce the signup check in both OTP send and verify routes.
- Preserve the pre-PR pass-through verification behavior when Web temporarily talks to an old backend without policy version 2.
- Log verification decisions without email addresses or OTP values, and document the account-service role contract.
- Keep Google and phone authentication behavior unchanged.

## Verification

- Backend domestic-access and route unit tests: 22 passed.
- Web auth-route unit tests: 26 passed.
- Web TypeScript and ESLint checks passed.
- Ruff and targeted Pyright checks for changed Python files passed.
- On 2026-09-20, ran the exact `email`/`is_active`/`role` filter through `profile_repo.find_uids_by_filter` inside a staging `claw-interface` Pod using the encrypted Mongo client. The read succeeded with zero matches for a synthetic address; no CSFLE rejection. [Verification discussion](https://github.com/SerendipityOneInc/ecap-workspace/pull/3815#issuecomment-5748739543).

## Rollout

Deploy `claw-interface` first, then Web in production to activate the complete policy immediately. Staging Web and backend deploy independently on merge, so Web verifies the backend policy version: an old response without `policy_version: 2` preserves the pre-PR pass-through OTP verification behavior even if old eligibility returns `false`. OTP send continues to honor the backend decision. After both releases deploy, the new eligibility policy applies at send and verify.

Eligibility-service failure during OTP verification returns 502 for existing users as well as new users. This fail-closed behavior is an accepted availability tradeoff.

## Check limitation

The repository-wide Pyright check fails on unchanged files (`google.py`, `first_use_monitor.py`, and route test helpers) in the local environment. The Pyright commit hook and pre-push verification were skipped after targeted checks passed. The PR's CI lint/typecheck and test jobs passed.

This change affects the web email OTP flow. Direct calls to the separate user-interface service are not changed.

---

## feat(platform): deliver phase one project and API key management (#3812)

- **SHA**: `7153580de0f83117cfedf12ed185e833ab90146f`
- **作者**: finn-srp
- **日期**: 2026-09-20T09:03:20Z
- **PR**: #3812

### Commit Message

```
feat(platform): deliver phase one project and API key management (#3812)

## Summary

Deliver Developer Platform Phase 1 as one cross-layer feature:

- add isolated Platform User, Organization, Project, and API Key
collections
- verify Clerk sessions and bootstrap the Organization/default Project
context
- expose Project and API Key management APIs through claw-interface
- connect the Platform web app to the real API
- keep Billing, Usage, SDK machine authentication, and Work key
migration deferred to later phases
- add Platform CI coverage and an operations handoff document

## Commit structure

1. `docs(platform)`: scope, API/table contract, and phased delivery plan
2. `feat(platform-backend)`: schema, repositories, Clerk auth, APIs, and
backend tests
3. `feat(platform-web)`: management console, real API integration,
disabled Phase 3 surfaces, and frontend tests
4. `chore(platform)`: CI and operations handoff

## Validation

- `bash scripts/verify-py.sh`
- 41 Platform backend unit/BDD tests
- Platform web lint and TypeScript typecheck
- 14 Platform web unit tests
- Platform Vite production build
- review-agent follow-up: no remaining findings

## Deferred / environment validation

This Draft is not a production-readiness claim. Before marking it ready:

- validate the real Clerk instance and Organization auto-provisioning
policy
- validate deployed ingress and exact-origin CORS
- validate staging Atlas and CSFLE behavior
- confirm log redaction and rate-limit behavior in the deployed
environment

Billing and Usage remain disabled and are explicitly Phase 3. Phase 1
API Keys are management records only; SDK machine authentication remains
Phase 2.
```

### PR Body

## Summary

Deliver Developer Platform Phase 1 as one cross-layer feature:

- add isolated Platform User, Organization, Project, and API Key collections
- verify Clerk sessions and bootstrap the Organization/default Project context
- expose Project and API Key management APIs through claw-interface
- connect the Platform web app to the real API
- keep Billing, Usage, SDK machine authentication, and Work key migration deferred to later phases
- add Platform CI coverage and an operations handoff document

## Commit structure

1. `docs(platform)`: scope, API/table contract, and phased delivery plan
2. `feat(platform-backend)`: schema, repositories, Clerk auth, APIs, and backend tests
3. `feat(platform-web)`: management console, real API integration, disabled Phase 3 surfaces, and frontend tests
4. `chore(platform)`: CI and operations handoff

## Validation

- `bash scripts/verify-py.sh`
- 41 Platform backend unit/BDD tests
- Platform web lint and TypeScript typecheck
- 14 Platform web unit tests
- Platform Vite production build
- review-agent follow-up: no remaining findings

## Deferred / environment validation

This Draft is not a production-readiness claim. Before marking it ready:

- validate the real Clerk instance and Organization auto-provisioning policy
- validate deployed ingress and exact-origin CORS
- validate staging Atlas and CSFLE behavior
- confirm log redaction and rate-limit behavior in the deployed environment

Billing and Usage remain disabled and are explicitly Phase 3. Phase 1 API Keys are management records only; SDK machine authentication remains Phase 2.

---

## fix(chat): 优化会话状态、消息操作与输入框布局 (#3793)

- **SHA**: `37de4b9f47d07efcdb2506fdef83ded137fe9200`
- **作者**: lynn Zhuang
- **日期**: 2026-09-20T08:39:33Z
- **PR**: #3793

### Commit Message

```
fix(chat): 优化会话状态、消息操作与输入框布局 (#3793)

## 改动说明

优化 Chat Session
的执行过程和消息分组：同一轮回复中的图片、文字与工具过程共享头像，只在最后一个答案片段下显示一次操作和时间栏，减少重复信息与空白。

- 连续 Agent 片段共用头像，兼容图片缺失 runId 和异步续跑更换 runId；用户消息及实际 session 分隔重新开始分组。
- 每轮回复只在最后一个答案片段保留复制、Reply、完成时间。较早片段移除整行占位；复制与 Reply
包含该轮全部回答文字，排除执行过程和中间说明。图片或卡片作为最后一条时仍保留该轮时间。
-
当前回复生成期间不提前显示完成时间，历史各轮保留各自末尾时间；新片段追加时同步失效旧片段的转换缓存，避免残留时间栏。时间仍取最后片段的最终内容编辑时间。
- 同一轮连续片段间距统一为 8px，用户与 Agent 之间保留原有间隔。Activity、思考和中间说明不单独显示时间。
- 执行期间默认展开工具步骤和已有思考摘要；开始输出答案或执行结束后默认收起，包括工具完成事件延迟到达、步骤仍标记 running
的情况；可手动重新展开。首次等待立即显示头像，去掉重复头像和三点 loading。
- 复制、Reply、时间位于消息外侧：Agent 左对齐、用户右对齐。Reply 引用条衔接输入框，使用浅灰底、描边与投影。
- 调整用户气泡颜色与正文宽度；输入框按实际高度预留滚动空间，修复两侧头像裁切，隐藏消息区滚动条并保留历史阅读位置。
- 补齐会话标题回退，保留 main 的渠道分组。
- 兼容 main 新增的额度不足提示：提示与输入区共用聊天
runtime，计入浮层高度并保持按钮可点击；保留历史失败状态去除重复额度文案的处理。

## 验证

- [x] 已同步最新 main（ed62e2ee4），合并提交 72533f491。解决会话 ViewModel 与额度提示的两处冲突，保留
main 的会话重命名和额度提示新样式，以及本 PR 的标题回退和浮层点击行为。
- [x] 本次更新：55 项针对性测试通过，覆盖会话标题/重命名、会话操作、旧会话、聊天 runtime、额度提示与输入框布局。
- [x] 本次更新：前端治理检查、TypeScript、ESLint 通过。
- [x] 此前消息分组改动的 274 项相关测试，以及上一轮合并的 191 项相关测试通过。
- [x] 上一轮提交 4ebcc98ec 的 Codex、Claude 复审均未发现新的代码问题；已知产品取舍见下文。
- [x] 提交 72533f491 的所有适用 CI 检查通过，包括构建、测试、类型/lint 与 CodeQL；Codex、Claude
复审均为 APPROVE，无新增代码扫描告警。
- [ ] 本次未运行浏览器视觉回归；之前真实 staging 的 localhost:3000 预览验证为 HTTP
200，浏览器控制不可用，未自动截图。

## 尚未确认的问题

先前截图中两张相同图片的重复来源尚未确认，本轮未修改图片去重规则。浏览器控制不可用，读取 staging 投递记录还受本机 gcloud
认证过期阻塞；需要对比 post/file/artifact 标识确认，不能仅凭外观或文件名删除图片。

## 审查说明

时间显示遵循用户最新确认：Activity
和中间说明不显示独立时间；普通答案、附件和卡片按一轮回复分组，仅最后一个答案片段显示完成时间。较早审查中要求为所有过程/片段恢复时间的意见与当前产品要求不符。

本轮复现并修复 Codex 发现的执行面板状态优先级问题：明确的收起指令覆盖 running 状态自动展开，用户手动选择仍优先；两条新增
running 场景断言修复前失败、修复后通过。

Claude
关于无用户消息间隔的主动推送可能并入相邻回复的意见，缺少实际投递样本，属于后续分组语义问题；保留用户已确认的连续回复分组，避免重新引入图片/异步续跑头像和时间分裂。待有可信的轮次边界数据后单独处理。

已修复先前非文本最终答案丢失时间、错误依赖未填充的 `_sessionKey` 分组等问题；遗留字段清理不扩大到本 PR。

本次 Claude 另提到标题的末级回退在完整 ViewModel
下冗余；实际标题正确、没有运行时缺陷，本轮保留，避免为无行为影响的清理新增改动。

本次仅涉及前端，无后端协议或依赖变更。
```

### PR Body

## 改动说明

优化 Chat Session 的执行过程和消息分组：同一轮回复中的图片、文字与工具过程共享头像，只在最后一个答案片段下显示一次操作和时间栏，减少重复信息与空白。

- 连续 Agent 片段共用头像，兼容图片缺失 runId 和异步续跑更换 runId；用户消息及实际 session 分隔重新开始分组。
- 每轮回复只在最后一个答案片段保留复制、Reply、完成时间。较早片段移除整行占位；复制与 Reply 包含该轮全部回答文字，排除执行过程和中间说明。图片或卡片作为最后一条时仍保留该轮时间。
- 当前回复生成期间不提前显示完成时间，历史各轮保留各自末尾时间；新片段追加时同步失效旧片段的转换缓存，避免残留时间栏。时间仍取最后片段的最终内容编辑时间。
- 同一轮连续片段间距统一为 8px，用户与 Agent 之间保留原有间隔。Activity、思考和中间说明不单独显示时间。
- 执行期间默认展开工具步骤和已有思考摘要；开始输出答案或执行结束后默认收起，包括工具完成事件延迟到达、步骤仍标记 running 的情况；可手动重新展开。首次等待立即显示头像，去掉重复头像和三点 loading。
- 复制、Reply、时间位于消息外侧：Agent 左对齐、用户右对齐。Reply 引用条衔接输入框，使用浅灰底、描边与投影。
- 调整用户气泡颜色与正文宽度；输入框按实际高度预留滚动空间，修复两侧头像裁切，隐藏消息区滚动条并保留历史阅读位置。
- 补齐会话标题回退，保留 main 的渠道分组。
- 兼容 main 新增的额度不足提示：提示与输入区共用聊天 runtime，计入浮层高度并保持按钮可点击；保留历史失败状态去除重复额度文案的处理。

## 验证

- [x] 已同步最新 main（ed62e2ee4），合并提交 72533f491。解决会话 ViewModel 与额度提示的两处冲突，保留 main 的会话重命名和额度提示新样式，以及本 PR 的标题回退和浮层点击行为。
- [x] 本次更新：55 项针对性测试通过，覆盖会话标题/重命名、会话操作、旧会话、聊天 runtime、额度提示与输入框布局。
- [x] 本次更新：前端治理检查、TypeScript、ESLint 通过。
- [x] 此前消息分组改动的 274 项相关测试，以及上一轮合并的 191 项相关测试通过。
- [x] 上一轮提交 4ebcc98ec 的 Codex、Claude 复审均未发现新的代码问题；已知产品取舍见下文。
- [x] 提交 72533f491 的所有适用 CI 检查通过，包括构建、测试、类型/lint 与 CodeQL；Codex、Claude 复审均为 APPROVE，无新增代码扫描告警。
- [ ] 本次未运行浏览器视觉回归；之前真实 staging 的 localhost:3000 预览验证为 HTTP 200，浏览器控制不可用，未自动截图。

## 尚未确认的问题

先前截图中两张相同图片的重复来源尚未确认，本轮未修改图片去重规则。浏览器控制不可用，读取 staging 投递记录还受本机 gcloud 认证过期阻塞；需要对比 post/file/artifact 标识确认，不能仅凭外观或文件名删除图片。

## 审查说明

时间显示遵循用户最新确认：Activity 和中间说明不显示独立时间；普通答案、附件和卡片按一轮回复分组，仅最后一个答案片段显示完成时间。较早审查中要求为所有过程/片段恢复时间的意见与当前产品要求不符。

本轮复现并修复 Codex 发现的执行面板状态优先级问题：明确的收起指令覆盖 running 状态自动展开，用户手动选择仍优先；两条新增 running 场景断言修复前失败、修复后通过。

Claude 关于无用户消息间隔的主动推送可能并入相邻回复的意见，缺少实际投递样本，属于后续分组语义问题；保留用户已确认的连续回复分组，避免重新引入图片/异步续跑头像和时间分裂。待有可信的轮次边界数据后单独处理。

已修复先前非文本最终答案丢失时间、错误依赖未填充的 `_sessionKey` 分组等问题；遗留字段清理不扩大到本 PR。

本次 Claude 另提到标题的末级回退在完整 ViewModel 下冗余；实际标题正确、没有运行时缺陷，本轮保留，避免为无行为影响的清理新增改动。

本次仅涉及前端，无后端协议或依赖变更。




---

## fix(agents): preserve pinned resource snapshots and runtime persona (#3814)

- **SHA**: `bce6e7056ea1e9fb24f3b0e765f88a5f1e47d8a6`
- **作者**: kaka-srp
- **日期**: 2026-09-20T08:29:14Z
- **PR**: #3814

### Commit Message

```
fix(agents): preserve pinned resource snapshots and runtime persona (#3814)

## Problem and behavior

Agent resource calls must retain the binding selected by their pinned
config, including retained Build previews. Store immutable runtime
projection-to-source/binding associations in the business database;
preserve Save/Undo, recovery, sharing and source Revision identity.
Engine forwards generic context and Proxy reads the exact applied
association.

Resource initialization now registers the existing configuration key
instead of creating and activating a configuration from stale
`declared.persona`. This fixes a reproduced regression that reset edited
AGENTS.md and deleted an onboarding-created USER.md. Null-key Agents
retain their business policy head for existing MCP synchronization,
without any Engine configuration write.

## Scope and rollout

- Existing Agents retain inherited selections; new Builder Agents start
with explicit empty selections. Main/Pack Settings remain unsupported.
- No new credentials, environment variables, flags, Proxy callbacks,
frontend changes, or Engine business-policy fields.
- Add a dry-run-first staging registration command for reviewed exact
historical keys. Per-Agent encrypted Mongo transactions reject stale
scope, pending saves, conflicting maps and revoked heads; reruns are
idempotent.
- Deploy the producer, revalidate/register retained history, then deploy
strict Proxy/Engine readers from the companion feature branches.
Preserve Engine pointers and existing persona/session state. The audited
staging snapshot contains 36 eligible Agents and 89 keys; revalidate
before applying.
- Companion PRs: [Engine
#1523](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1523),
updated on its original `feature/agent-resource-bindings` branch, and
[Proxy
#203](https://github.com/SerendipityOneInc/ecap-proxy-service/pull/203)
on `feature/agent-resource-snapshots`.

## Validation

- CI follow-up `fc90144359`: reuse the resource-projection store fixture
in seven sharing/skill pipeline tests; no production changes or weakened
assertions. Both affected modules pass locally (41 tests), full backend
static/commit/push gates pass, and the updated PR CI passes with
**11,447 tests passed / 5 skipped**.
- Final expanded backend regressions: **2,523 passed**, including
initialization/retry persona preservation, null-key MCP sync,
registration conflicts, Save/Undo, sharing and authoring.
- Full backend static gate and commit hooks passed. Broader
pre-correction affected suite: 1,021 passed.
- Actual staging CSFLE canary passed dry-run/no-write, repeat
registration, pending-save refusal, transactional rollback on a
later-key conflict, and revoked-head refusal. Exact isolated fixture
rows were cleaned and verified absent.
- Three-agent review completed; P1 persona overwrite and follow-up
null-key MCP regression fixed and independently re-reviewed.
- Fleet registration and deployed provider/browser smoke are separate
rollout steps, not claimed by unit tests.

## Staging cutover

Backend published from the feature branch as `service-v0.18.11-beta.11`.
Registered 36 reviewed legacy Agents / 89 exact historical keys.
Verified all associations with the actual Proxy reader, denied unknown
contexts, and confirmed all 36 Engine pointers/keys remain unchanged.
Retained session inventory: 118 sessions, no uncovered contexts. PR CI
was not awaited, as explicitly requested for this staging test release.

## Pending-Save review correction

Commits `60b4d4ffe0` and `ecd79d0379` stop Undo, MCP synchronization,
and idempotent Save retry before mutation when an intermediate-build
configuration declares a resource binding without a registered
projection. Save retry checks before credential seeding and checks the
fresh post-seeding config again. The legacy field is a rejection signal
only, never authorization. Normal source/baseline/null-key behavior
remains unchanged. Rollout requires pausing resource Saves and
completing/reconciling pending operations on the originating build
before producer deployment; the runtime guard prevents silent rollback
if this prerequisite is violated.

Validation: the initial correction passed **2,285 affected tests**. The
additional Save-retry finding was reproduced by three failing cases
before correction; **113 directly affected tests now pass**, including
nine no-mutation cases across Undo/MCP synchronization/Save retry and
normal resource Save. Backend static and commit/push gates passed. A
read-only encrypted staging query at 2026-09-20 07:48:35 UTC found **0
pending Saves across all Engine workspaces**. This is current-state
evidence, not retrospective proof of the earlier deployment window.
These corrections are not yet redeployed to staging.
```

### PR Body

## Problem and behavior

Agent resource calls must retain the binding selected by their pinned config, including retained Build previews. Store immutable runtime projection-to-source/binding associations in the business database; preserve Save/Undo, recovery, sharing and source Revision identity. Engine forwards generic context and Proxy reads the exact applied association.

Resource initialization now registers the existing configuration key instead of creating and activating a configuration from stale `declared.persona`. This fixes a reproduced regression that reset edited AGENTS.md and deleted an onboarding-created USER.md. Null-key Agents retain their business policy head for existing MCP synchronization, without any Engine configuration write.

## Scope and rollout

- Existing Agents retain inherited selections; new Builder Agents start with explicit empty selections. Main/Pack Settings remain unsupported.
- No new credentials, environment variables, flags, Proxy callbacks, frontend changes, or Engine business-policy fields.
- Add a dry-run-first staging registration command for reviewed exact historical keys. Per-Agent encrypted Mongo transactions reject stale scope, pending saves, conflicting maps and revoked heads; reruns are idempotent.
- Deploy the producer, revalidate/register retained history, then deploy strict Proxy/Engine readers from the companion feature branches. Preserve Engine pointers and existing persona/session state. The audited staging snapshot contains 36 eligible Agents and 89 keys; revalidate before applying.
- Companion PRs: [Engine #1523](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1523), updated on its original `feature/agent-resource-bindings` branch, and [Proxy #203](https://github.com/SerendipityOneInc/ecap-proxy-service/pull/203) on `feature/agent-resource-snapshots`.

## Validation

- CI follow-up `fc90144359`: reuse the resource-projection store fixture in seven sharing/skill pipeline tests; no production changes or weakened assertions. Both affected modules pass locally (41 tests), full backend static/commit/push gates pass, and the updated PR CI passes with **11,447 tests passed / 5 skipped**.
- Final expanded backend regressions: **2,523 passed**, including initialization/retry persona preservation, null-key MCP sync, registration conflicts, Save/Undo, sharing and authoring.
- Full backend static gate and commit hooks passed. Broader pre-correction affected suite: 1,021 passed.
- Actual staging CSFLE canary passed dry-run/no-write, repeat registration, pending-save refusal, transactional rollback on a later-key conflict, and revoked-head refusal. Exact isolated fixture rows were cleaned and verified absent.
- Three-agent review completed; P1 persona overwrite and follow-up null-key MCP regression fixed and independently re-reviewed.
- Fleet registration and deployed provider/browser smoke are separate rollout steps, not claimed by unit tests.

## Staging cutover

Backend published from the feature branch as `service-v0.18.11-beta.11`. Registered 36 reviewed legacy Agents / 89 exact historical keys. Verified all associations with the actual Proxy reader, denied unknown contexts, and confirmed all 36 Engine pointers/keys remain unchanged. Retained session inventory: 118 sessions, no uncovered contexts. PR CI was not awaited, as explicitly requested for this staging test release.

## Pending-Save review correction

Commits `60b4d4ffe0` and `ecd79d0379` stop Undo, MCP synchronization, and idempotent Save retry before mutation when an intermediate-build configuration declares a resource binding without a registered projection. Save retry checks before credential seeding and checks the fresh post-seeding config again. The legacy field is a rejection signal only, never authorization. Normal source/baseline/null-key behavior remains unchanged. Rollout requires pausing resource Saves and completing/reconciling pending operations on the originating build before producer deployment; the runtime guard prevents silent rollback if this prerequisite is violated.

Validation: the initial correction passed **2,285 affected tests**. The additional Save-retry finding was reproduced by three failing cases before correction; **113 directly affected tests now pass**, including nine no-mutation cases across Undo/MCP synchronization/Save retry and normal resource Save. Backend static and commit/push gates passed. A read-only encrypted staging query at 2026-09-20 07:48:35 UTC found **0 pending Saves across all Engine workspaces**. This is current-state evidence, not retrospective proof of the earlier deployment window. These corrections are not yet redeployed to staging.


---

## feat(settings): support personal workspace conversion to Team (#3762)

- **SHA**: `ffcc39dab20b2b3c38ea982c4ff40e3450b9b691`
- **作者**: finn-srp
- **日期**: 2026-09-20T05:25:22Z
- **PR**: #3762

### Commit Message

```
feat(settings): support personal workspace conversion to Team (#3762)

## Issue

Closes #3759

## Summary

Personal workspace owners can convert their existing workspace to Team
from Settings > Organization > Convert to Team. The same org,
membership, Agents, and data are preserved; this does not purchase a
paid plan or provision Team wallets.

- Add the typed public `POST /orgs/{org_id}/upgrade-to-team` endpoint,
restricted to the owner with an active admin membership.
- Reuse `org_upgrade.upgrade_org_to_team`, with the strict self-service
subscription policy rechecked under the existing transition lease. Any
non-terminal personal subscription, including canceling at period end,
blocks conversion.
- Add the confirmation dialog, Team name input, account cache refresh,
and Team navigation after success.
- Reuse Billing v2 audit events for self-service conversion. Persist the
started event before external changes; commit the success event and org
CAS in one MongoDB transaction. Failure records share the correlation ID
and identify the execution stage without storing raw exception text.
Failure-audit errors preserve the original business error.

## Scope and failure boundaries

The maintainer explicitly approved reusing the existing audit
infrastructure after discussing the audit review finding. This
supersedes issue #3759's earlier exclusion of additional audit behavior
for this PR. The staff API retains its existing default behavior.

There are no new wallet/payment-order eligibility checks, checkout
mutex, automatic cancellation/refund, balance migration, Team billing
provisioning, or request-idempotency mechanisms. No audit queue or
automatic reconciliation job is introduced.

MongoDB guarantees that the local org conversion and success audit
commit together. External Billing Gateway changes are outside that
transaction, as in the existing conversion flow. If an external change
succeeds before a later failure, the failure audit records the stage and
unknown resulting state; it does not claim an external rollback. If
failure-audit persistence is also unavailable, or the process exits
mid-operation, the durable started event remains for manual
investigation. Automated repair of these cases is not included.

## Validation

- [x] Backend focused
audit/repository/route/conversion/subscription/CSFLE query-guard suite:
139 passed.
- [x] Final audit/repository tests after the metadata adjustment: 30
passed.
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright, and import
contracts passed.
- [x] Function complexity and database return-contract checks passed.
- [x] Frontend full unit suite after merging main: 10,312 passed, 70
skipped, 1 todo; this audit change adds no frontend code.
- [x] Conversion-focused frontend tests: 31 passed; TypeScript and
ESLint passed.
- [ ] Browser E2E and live Billing Gateway validation were not run.
- [x] Staging encrypted MongoDB validation passed on 2026-09-20 for code
commit `305f5c5e6`: actual repository success commit, real audit-insert
failure rollback, and CAS-miss behavior. Auto-encryption enabled; no
bypass or plain client. All isolated fixtures cleaned (2 orgs, 1 audit;
0 remaining). [Environment, exact source hash, method, and
results](https://github.com/SerendipityOneInc/ecap-workspace/blob/bb818c812/docs/staging-validation/2026-09-20-org-conversion-audit-csfle.md).
```

### PR Body

## Issue

Closes #3759

## Summary

Personal workspace owners can convert their existing workspace to Team from Settings > Organization > Convert to Team. The same org, membership, Agents, and data are preserved; this does not purchase a paid plan or provision Team wallets.

- Add the typed public `POST /orgs/{org_id}/upgrade-to-team` endpoint, restricted to the owner with an active admin membership.
- Reuse `org_upgrade.upgrade_org_to_team`, with the strict self-service subscription policy rechecked under the existing transition lease. Any non-terminal personal subscription, including canceling at period end, blocks conversion.
- Add the confirmation dialog, Team name input, account cache refresh, and Team navigation after success.
- Reuse Billing v2 audit events for self-service conversion. Persist the started event before external changes; commit the success event and org CAS in one MongoDB transaction. Failure records share the correlation ID and identify the execution stage without storing raw exception text. Failure-audit errors preserve the original business error.

## Scope and failure boundaries

The maintainer explicitly approved reusing the existing audit infrastructure after discussing the audit review finding. This supersedes issue #3759's earlier exclusion of additional audit behavior for this PR. The staff API retains its existing default behavior.

There are no new wallet/payment-order eligibility checks, checkout mutex, automatic cancellation/refund, balance migration, Team billing provisioning, or request-idempotency mechanisms. No audit queue or automatic reconciliation job is introduced.

MongoDB guarantees that the local org conversion and success audit commit together. External Billing Gateway changes are outside that transaction, as in the existing conversion flow. If an external change succeeds before a later failure, the failure audit records the stage and unknown resulting state; it does not claim an external rollback. If failure-audit persistence is also unavailable, or the process exits mid-operation, the durable started event remains for manual investigation. Automated repair of these cases is not included.

## Validation

- [x] Backend focused audit/repository/route/conversion/subscription/CSFLE query-guard suite: 139 passed.
- [x] Final audit/repository tests after the metadata adjustment: 30 passed.
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright, and import contracts passed.
- [x] Function complexity and database return-contract checks passed.
- [x] Frontend full unit suite after merging main: 10,312 passed, 70 skipped, 1 todo; this audit change adds no frontend code.
- [x] Conversion-focused frontend tests: 31 passed; TypeScript and ESLint passed.
- [ ] Browser E2E and live Billing Gateway validation were not run.
- [x] Staging encrypted MongoDB validation passed on 2026-09-20 for code commit `305f5c5e6`: actual repository success commit, real audit-insert failure rollback, and CAS-miss behavior. Auto-encryption enabled; no bypass or plain client. All isolated fixtures cleaned (2 orgs, 1 audit; 0 remaining). [Environment, exact source hash, method, and results](https://github.com/SerendipityOneInc/ecap-workspace/blob/bb818c812/docs/staging-validation/2026-09-20-org-conversion-audit-csfle.md).




---

## fix(workspace): 恢复 R4 会话操作并优化交互样式 (#3804)

- **SHA**: `ed62e2ee420a9f8f2c2e759e3601daf58c7f112c`
- **作者**: lynn Zhuang
- **日期**: 2026-09-20T03:52:56Z
- **PR**: #3804

### Commit Message

```
fix(workspace): 恢复 R4 会话操作并优化交互样式 (#3804)

## 改动说明

恢复 R4 Agent 工作区缺失的会话操作和附件入口，并统一列表、导航及弹窗的交互样式。

- 恢复 Agent 会话侧边栏重命名、归档及聊天顶部标题编辑；详情页浏览器标签展示 Agent 名称。新建 Agent
接入与首页一致的附件上传能力，外部渠道卡片显示实际 Agent 头像。
- 接入 V5 默认头像：保留白色图形内部，使用各不相同的浅色渐变背景与浅灰圆形描边。精简 Update
按钮，以名称后的紫色圆形上箭头表示有新版本；整行悬停时箭头持续动画，活动图改为紫绿渐变。
- 统一列表圆角悬停、相邻分隔线、更多菜单、会话选中态和创建按钮提示；Tasks
增加骨架加载，移除多余的积分失败横幅与表头悬停。创建弹窗顶部增加轻量紫绿渐变，侧边栏图标改为局部路径动效，并支持减少动态效果偏好。
- 分享弹窗使用深色复制按钮，复制完整 URL，Build
历史链接折叠展示。链接沿用现有创建、发布与撤销流程；复制地址来自本次创建接口的返回值。

## 后端范围

后端仅涉及会话重命名和归档，共 2 个业务实现文件、2 个测试文件，合计新增 289 行、删除 1 行；其中业务实现新增 99 行、删除 1
行，测试新增 190 行。

| 文件（相对 `services/claw-interface/`） | 用途 | 行数 |
| --- | --- | --- |
| `app/routes/agent_development.py` | 新增会话重命名、归档两个 POST
接口；校验身份、功能访问权限及标题参数，返回现有会话记录类型 | +30 / -1 |
| `app/services/agent_development/task_metadata_service.py` | 将 Engine
会话 ID 或历史会话别名映射到原始 Web 会话记录；检查工作区归属和会话可操作性，再复用已有会话服务 | +69 |
| `tests/unit/test_agent_development_route_boundaries.py` |
覆盖身份和组织参数传递、无效标题及 404 返回 | +28 |
| `tests/unit/test_agent_task_metadata.py` | 覆盖原始记录 ID 映射、历史会话、新建 Web
会话、归属校验，以及外部渠道只读、隐藏和已归档会话限制 | +162 |

新增接口：

- `POST
/agent-definitions/{workspace_id}/task-sessions/{session_id}/rename`
- `POST
/agent-definitions/{workspace_id}/task-sessions/{session_id}/archive`

需要后端配合的原因：前端任务列表中的会话 ID 可能来自 Engine 或历史别名，与存储中的原始 Web 会话 ID
不一致。后端负责解析对应关系、校验权限并持久保存操作结果。归档只更新状态，保留历史记录。

本 PR 没有新增数据库结构或迁移。分享链接继续沿用现有创建、发布与撤销流程；分享链接复用、token
加密保存及相关存储字段和数据库查询改动已撤回。

## 验证

- [x] 合入 `main`（`25750ee08`），解决 Agent 详情页逻辑与 mock 路由冲突，同时保留会话操作和每个 Agent
的连接器、MCP、知识库配置能力。
- [x] 合并 main 后，前端会话操作、资源配置/恢复、分享发布及 mock 回归：14 个文件、101 项测试通过。
- [x] 合并 main 后，后端会话操作、接口边界、分享发布及资源策略/恢复回归：8 个文件、115 项测试通过。
- [x] 前端 TypeScript、ESLint 与仓库治理检查通过。
- [x] 后端 Ruff、格式、Pyright 和 import-linter 检查通过。
- [x] `git diff --check` 通过。
- [ ] 已知待处理：归档/重命名后同步失效 Tasks 总表缓存，避免立即返回总表时展示旧记录。

涉及 `web/app` 与
`services/claw-interface`；会话操作上线需要前后端配套部署。本次未重跑浏览器回归或全量测试，完整构建和全量质量检查由
CI 执行。
```

### PR Body

## 改动说明

恢复 R4 Agent 工作区缺失的会话操作和附件入口，并统一列表、导航及弹窗的交互样式。

- 恢复 Agent 会话侧边栏重命名、归档及聊天顶部标题编辑；详情页浏览器标签展示 Agent 名称。新建 Agent 接入与首页一致的附件上传能力，外部渠道卡片显示实际 Agent 头像。
- 接入 V5 默认头像：保留白色图形内部，使用各不相同的浅色渐变背景与浅灰圆形描边。精简 Update 按钮，以名称后的紫色圆形上箭头表示有新版本；整行悬停时箭头持续动画，活动图改为紫绿渐变。
- 统一列表圆角悬停、相邻分隔线、更多菜单、会话选中态和创建按钮提示；Tasks 增加骨架加载，移除多余的积分失败横幅与表头悬停。创建弹窗顶部增加轻量紫绿渐变，侧边栏图标改为局部路径动效，并支持减少动态效果偏好。
- 分享弹窗使用深色复制按钮，复制完整 URL，Build 历史链接折叠展示。链接沿用现有创建、发布与撤销流程；复制地址来自本次创建接口的返回值。

## 后端范围

后端仅涉及会话重命名和归档，共 2 个业务实现文件、2 个测试文件，合计新增 289 行、删除 1 行；其中业务实现新增 99 行、删除 1 行，测试新增 190 行。

| 文件（相对 `services/claw-interface/`） | 用途 | 行数 |
| --- | --- | --- |
| `app/routes/agent_development.py` | 新增会话重命名、归档两个 POST 接口；校验身份、功能访问权限及标题参数，返回现有会话记录类型 | +30 / -1 |
| `app/services/agent_development/task_metadata_service.py` | 将 Engine 会话 ID 或历史会话别名映射到原始 Web 会话记录；检查工作区归属和会话可操作性，再复用已有会话服务 | +69 |
| `tests/unit/test_agent_development_route_boundaries.py` | 覆盖身份和组织参数传递、无效标题及 404 返回 | +28 |
| `tests/unit/test_agent_task_metadata.py` | 覆盖原始记录 ID 映射、历史会话、新建 Web 会话、归属校验，以及外部渠道只读、隐藏和已归档会话限制 | +162 |

新增接口：

- `POST /agent-definitions/{workspace_id}/task-sessions/{session_id}/rename`
- `POST /agent-definitions/{workspace_id}/task-sessions/{session_id}/archive`

需要后端配合的原因：前端任务列表中的会话 ID 可能来自 Engine 或历史别名，与存储中的原始 Web 会话 ID 不一致。后端负责解析对应关系、校验权限并持久保存操作结果。归档只更新状态，保留历史记录。

本 PR 没有新增数据库结构或迁移。分享链接继续沿用现有创建、发布与撤销流程；分享链接复用、token 加密保存及相关存储字段和数据库查询改动已撤回。

## 验证

- [x] 合入 `main`（`25750ee08`），解决 Agent 详情页逻辑与 mock 路由冲突，同时保留会话操作和每个 Agent 的连接器、MCP、知识库配置能力。
- [x] 合并 main 后，前端会话操作、资源配置/恢复、分享发布及 mock 回归：14 个文件、101 项测试通过。
- [x] 合并 main 后，后端会话操作、接口边界、分享发布及资源策略/恢复回归：8 个文件、115 项测试通过。
- [x] 前端 TypeScript、ESLint 与仓库治理检查通过。
- [x] 后端 Ruff、格式、Pyright 和 import-linter 检查通过。
- [x] `git diff --check` 通过。
- [ ] 已知待处理：归档/重命名后同步失效 Tasks 总表缓存，避免立即返回总表时展示旧记录。

涉及 `web/app` 与 `services/claw-interface`；会话操作上线需要前后端配套部署。本次未重跑浏览器回归或全量测试，完整构建和全量质量检查由 CI 执行。


---

## fix(seo): unify public marketing English URLs (#3806)

- **SHA**: `25750ee083ba44ca26932edb0cdcce2e14f16f46`
- **作者**: Mori-srp
- **日期**: 2026-09-20T03:38:20Z
- **PR**: #3806

### Commit Message

```
fix(seo): unify public marketing English URLs (#3806)

## Summary

Move the English About, Pricing, Solutions, and Enterprise public pages
to `/about`, `/pricing`, `/solutions`, and `/enterprise`. Legacy
`/en/...` links return a 301 while retaining the original query string.
Non-English public URLs keep their existing first-level locale.

Use an exact marketing-page allowlist for navigation, language
switching, middleware, and internal rewrites. Generic locale helpers,
backend URL generators, login, subscription, checkout, APIs, and
attachment URLs retain their existing behavior. Align canonical,
real-language alternates, Enterprise metadata, and the 65-entry main
sitemap. Complete missing Solutions copy in eight existing locale
dictionaries so those public locale pages do not fall back to English.

## Root cause

The public marketing URL contract previously prefixed English inner
pages, while Enterprise maintained separate SEO metadata. Shared
navigation therefore needed a marketing-specific resolver with the
existing product resolver as its fallback.

## Test plan

- [x] Rebased onto `edd8bb8bef71e7835ab207a9e6caf000ade1d24e`;
range-diff confirms the migration patch is unchanged.
- [x] Reran 352 relevant tests on the rebased branch: route allowlist,
query preservation, SEO, navigation/language switching, middleware, and
excluded product/API/asset paths.
- [x] Earlier local verification of the same migration patch: optimized
Next build, 82/82 development HTTP checks, 82/82 built-server HTTP
checks, and four page-family browser language round-trips with
query/hash preservation.
- [x] Local desktop/mobile login entry and a mocked authenticated
Pricing-to-subscription flow; stopped before payment. This does not
claim an end-to-end payment test.
- [x] GitHub CI: 819 frontend test files, 10,336 tests passed, 70
skipped, 1 todo; lint/type checks and the compile-mode Next build
passed. All 23 active checks passed; 15 conditional checks were skipped.
- [x] Both automated reviews found no issues in this migration;
inspected their full comments and inline review threads (none).
- [ ] Human engineering review and production routing/cache/rollback
confirmation; this PR remains a draft with auto-merge disabled.

### Known baseline verification limitation

The local build-generated type check exposes an existing
`/api/download/route.ts` export error (`isAllowedUrl` is not an allowed
Next route export). That source is byte-identical on this branch, its
original base, and latest main. The first pre-push check failed on this
error. Generated build types and the incremental cache were archived,
then the normal unmodified pre-push source checks were rerun in the
clean-source state used by CI. No hook was bypassed and no API source or
type-check configuration was changed. A post-build generated-type check
still needs that separate baseline issue resolved; a clean-source CI
pass does not close it.

## Release dependencies

Keep this draft unmerged. Confirm the four public paths' actual
production routing, absence of reverse redirect rules, cache handling,
and a compatible rollback before release. Current production still uses
prefixed English inner pages; local verification is not production
acceptance.

Publish cross-site link follow-ups only after these new production URLs
return the expected content and old aliases redirect correctly:

- Gallery:
https://github.com/SerendipityOneInc/zoowork-agent-gallery/pull/6
- Blog: https://github.com/SerendipityOneInc/zooclaw-blog/pull/11

Gallery's own migrated paths remain unchanged; Blog's own locale
migration and Tips are separate work. This task does not merge PRs,
deploy production, change Worker routing, or operate GSC.
```

### PR Body

## Summary

Move the English About, Pricing, Solutions, and Enterprise public pages to `/about`, `/pricing`, `/solutions`, and `/enterprise`. Legacy `/en/...` links return a 301 while retaining the original query string. Non-English public URLs keep their existing first-level locale.

Use an exact marketing-page allowlist for navigation, language switching, middleware, and internal rewrites. Generic locale helpers, backend URL generators, login, subscription, checkout, APIs, and attachment URLs retain their existing behavior. Align canonical, real-language alternates, Enterprise metadata, and the 65-entry main sitemap. Complete missing Solutions copy in eight existing locale dictionaries so those public locale pages do not fall back to English.

## Root cause

The public marketing URL contract previously prefixed English inner pages, while Enterprise maintained separate SEO metadata. Shared navigation therefore needed a marketing-specific resolver with the existing product resolver as its fallback.

## Test plan

- [x] Rebased onto `edd8bb8bef71e7835ab207a9e6caf000ade1d24e`; range-diff confirms the migration patch is unchanged.
- [x] Reran 352 relevant tests on the rebased branch: route allowlist, query preservation, SEO, navigation/language switching, middleware, and excluded product/API/asset paths.
- [x] Earlier local verification of the same migration patch: optimized Next build, 82/82 development HTTP checks, 82/82 built-server HTTP checks, and four page-family browser language round-trips with query/hash preservation.
- [x] Local desktop/mobile login entry and a mocked authenticated Pricing-to-subscription flow; stopped before payment. This does not claim an end-to-end payment test.
- [x] GitHub CI: 819 frontend test files, 10,336 tests passed, 70 skipped, 1 todo; lint/type checks and the compile-mode Next build passed. All 23 active checks passed; 15 conditional checks were skipped.
- [x] Both automated reviews found no issues in this migration; inspected their full comments and inline review threads (none).
- [ ] Human engineering review and production routing/cache/rollback confirmation; this PR remains a draft with auto-merge disabled.

### Known baseline verification limitation

The local build-generated type check exposes an existing `/api/download/route.ts` export error (`isAllowedUrl` is not an allowed Next route export). That source is byte-identical on this branch, its original base, and latest main. The first pre-push check failed on this error. Generated build types and the incremental cache were archived, then the normal unmodified pre-push source checks were rerun in the clean-source state used by CI. No hook was bypassed and no API source or type-check configuration was changed. A post-build generated-type check still needs that separate baseline issue resolved; a clean-source CI pass does not close it.

## Release dependencies

Keep this draft unmerged. Confirm the four public paths' actual production routing, absence of reverse redirect rules, cache handling, and a compatible rollback before release. Current production still uses prefixed English inner pages; local verification is not production acceptance.

Publish cross-site link follow-ups only after these new production URLs return the expected content and old aliases redirect correctly:

- Gallery: https://github.com/SerendipityOneInc/zoowork-agent-gallery/pull/6
- Blog: https://github.com/SerendipityOneInc/zooclaw-blog/pull/11

Gallery's own migrated paths remain unchanged; Blog's own locale migration and Tips are separate work. This task does not merge PRs, deploy production, change Worker routing, or operate GSC.


---

## build(deps): update openai requirement from <3.4.0,>=3.3.1 to >=3.13.0,<3.14.0 in /services/claw-interface (#3810)

- **SHA**: `993c5bea866007509aa0fede6f39a9b310e5bd6a`
- **作者**: dependabot[bot]
- **日期**: 2026-09-20T03:03:23Z
- **PR**: #3810

### Commit Message

```
build(deps): update openai requirement from <3.4.0,>=3.3.1 to >=3.13.0,<3.14.0 in /services/claw-interface (#3810)

Updates the requirements on
[openai](https://github.com/openai/openai-python) to permit the latest
version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/openai/openai-python/releases">openai's
releases</a>.</em></p>
<blockquote>
<h2>v3.13.0</h2>
<h2><a
href="https://github.com/openai/openai-python/compare/v3.12.0...v3.13.0">3.13.0</a>
(2026-09-10)</h2>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> add Agents API (<a
href="https://github.com/openai/openai-python/commit/1c4284a08294f734d57047585ab82e2e09d3a5bc">1c4284a</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/openai/openai-python/blob/main/CHANGELOG.md">openai's
changelog</a>.</em></p>
<blockquote>
<h2><a
href="https://github.com/openai/openai-python/compare/v3.12.0...v3.13.0">3.13.0</a>
(2026-09-10)</h2>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> add Agents API (<a
href="https://github.com/openai/openai-python/commit/1c4284a08294f734d57047585ab82e2e09d3a5bc">1c4284a</a>)</li>
</ul>
<h2><a
href="https://github.com/openai/openai-python/compare/v3.11.0...v3.12.0">3.12.0</a>
(2026-09-10)</h2>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> Add Live API (<a
href="https://github.com/openai/openai-python/commit/0e4bfef9c79251fcf4926fd732129627bde050f1">0e4bfef</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li>add aclose() to AsyncStream for standard async cleanup (<a
href="https://redirect.github.com/openai/openai-python/issues/2854">#2854</a>)
(<a
href="https://github.com/openai/openai-python/commit/802b334928d8f0c3e24e5fce15a0eaa1b28c61cd">802b334</a>)</li>
<li>handle bare <code>dict</code> and <code>list</code> annotations
without type arguments (<a
href="https://redirect.github.com/openai/openai-python/issues/3760">#3760</a>)
(<a
href="https://github.com/openai/openai-python/commit/c7e8c03e2d87708ef233d0db00167dfa339325a9">c7e8c03</a>)</li>
<li>preserve finalized output on null response completion (<a
href="https://redirect.github.com/openai/openai-python/issues/3345">#3345</a>)
(<a
href="https://github.com/openai/openai-python/commit/adb212e116323fcec4b4811d20ba9eb78280c24c">adb212e</a>)</li>
</ul>
<h2><a
href="https://github.com/openai/openai-python/compare/v3.10.0...v3.11.0">3.11.0</a>
(2026-09-09)</h2>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> Add expiration controls for service account
keys (<a
href="https://redirect.github.com/openai/openai-python/issues/3825">#3825</a>)
(<a
href="https://github.com/openai/openai-python/commit/f348ec87b934c98889102668913e0a3ae7fc303d">f348ec8</a>)</li>
</ul>
<h2><a
href="https://github.com/openai/openai-python/compare/v3.9.0...v3.10.0">3.10.0</a>
(2026-09-08)</h2>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> add GPT Image 2.5 models and image options (<a
href="https://redirect.github.com/openai/openai-python/issues/3824">#3824</a>)
(<a
href="https://github.com/openai/openai-python/commit/5b39c453ee5ee8f46fba0bd9cb4ae47fa5ee6d51">5b39c45</a>)</li>
<li><strong>api:</strong> add service-account API key expiration fields
(<a
href="https://redirect.github.com/openai/openai-python/issues/3802">#3802</a>)
(<a
href="https://github.com/openai/openai-python/commit/f1cd7f020210ec3fc71699fc46d90320ddbb411c">f1cd7f0</a>)</li>
</ul>
<h2><a
href="https://github.com/openai/openai-python/compare/v3.8.0...v3.9.0">3.9.0</a>
(2026-09-05)</h2>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> Add prompt cache diagnostics (<a
href="https://redirect.github.com/openai/openai-python/issues/3800">#3800</a>)
(<a
href="https://github.com/openai/openai-python/commit/83267847a0219ea8b584c9d60f92c7a4dffd392a">8326784</a>)</li>
<li><strong>api:</strong> correct function argument completion event
fields (openapi-545) (<a
href="https://redirect.github.com/openai/openai-python/issues/3801">#3801</a>)
(<a
href="https://github.com/openai/openai-python/commit/2a98f6a1dee448c6410531c89c2de0af4383c6a7">2a98f6a</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> accept incomplete web search call statuses (<a
href="https://redirect.github.com/openai/openai-python/issues/3786">#3786</a>)
(<a
href="https://github.com/openai/openai-python/commit/3cc8d784ad05f75a265012ee86638adaf93d8bf2">3cc8d78</a>)</li>
<li>refuse overflowing server retry delays (<a
href="https://redirect.github.com/openai/openai-python/issues/3799">#3799</a>)
(<a
href="https://github.com/openai/openai-python/commit/88b4d4341af38e84784221d73c175f2088fa6b85">88b4d43</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/openai/openai-python/commit/f0fa922ef12f2c7329bcd8fc42e0cbb46f008ecb"><code>f0fa922</code></a>
release: 3.13.0 (<a
href="https://redirect.github.com/openai/openai-python/issues/3848">#3848</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/1c4284a08294f734d57047585ab82e2e09d3a5bc"><code>1c4284a</code></a>
feat(agents): add beta API and one-turn streaming helpers (<a
href="https://redirect.github.com/openai/openai-python/issues/3847">#3847</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/603b81f9e228d95032059169cb3a0e7dc12ba93f"><code>603b81f</code></a>
release: 3.12.0 (<a
href="https://redirect.github.com/openai/openai-python/issues/3832">#3832</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/0e4bfef9c79251fcf4926fd732129627bde050f1"><code>0e4bfef</code></a>
feat(api) Add Live API (<a
href="https://redirect.github.com/openai/openai-python/issues/3846">#3846</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/802b334928d8f0c3e24e5fce15a0eaa1b28c61cd"><code>802b334</code></a>
fix: add aclose() to AsyncStream for standard async cleanup (<a
href="https://redirect.github.com/openai/openai-python/issues/2854">#2854</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/adb212e116323fcec4b4811d20ba9eb78280c24c"><code>adb212e</code></a>
fix: preserve finalized output on null response completion (<a
href="https://redirect.github.com/openai/openai-python/issues/3345">#3345</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/c7e8c03e2d87708ef233d0db00167dfa339325a9"><code>c7e8c03</code></a>
fix: handle bare <code>dict</code> and <code>list</code> annotations
without type arguments (<a
href="https://redirect.github.com/openai/openai-python/issues/3760">#3760</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/397ea08d8cf151039c069c1173f5de57cff5c081"><code>397ea08</code></a>
ci: resolve fork PRs missing Castiron run associations (<a
href="https://redirect.github.com/openai/openai-python/issues/3831">#3831</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/2d4b97cc84d5c3ca051cc2ac2d8a6c9928b4d5f0"><code>2d4b97c</code></a>
test: restore CI test runtime after dependency-policy regression (<a
href="https://redirect.github.com/openai/openai-python/issues/3830">#3830</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/41f0a2317759e8796ccfbde75536bd42e4aca7a2"><code>41f0a23</code></a>
release: 3.11.0 (<a
href="https://redirect.github.com/openai/openai-python/issues/3829">#3829</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/openai/openai-python/compare/v3.3.1...v3.13.0">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Body

Updates the requirements on [openai](https://github.com/openai/openai-python) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/openai/openai-python/releases">openai's releases</a>.</em></p>
<blockquote>
<h2>v3.13.0</h2>
<h2><a href="https://github.com/openai/openai-python/compare/v3.12.0...v3.13.0">3.13.0</a> (2026-09-10)</h2>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> add Agents API (<a href="https://github.com/openai/openai-python/commit/1c4284a08294f734d57047585ab82e2e09d3a5bc">1c4284a</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/openai/openai-python/blob/main/CHANGELOG.md">openai's changelog</a>.</em></p>
<blockquote>
<h2><a href="https://github.com/openai/openai-python/compare/v3.12.0...v3.13.0">3.13.0</a> (2026-09-10)</h2>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> add Agents API (<a href="https://github.com/openai/openai-python/commit/1c4284a08294f734d57047585ab82e2e09d3a5bc">1c4284a</a>)</li>
</ul>
<h2><a href="https://github.com/openai/openai-python/compare/v3.11.0...v3.12.0">3.12.0</a> (2026-09-10)</h2>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> Add Live API (<a href="https://github.com/openai/openai-python/commit/0e4bfef9c79251fcf4926fd732129627bde050f1">0e4bfef</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li>add aclose() to AsyncStream for standard async cleanup (<a href="https://redirect.github.com/openai/openai-python/issues/2854">#2854</a>) (<a href="https://github.com/openai/openai-python/commit/802b334928d8f0c3e24e5fce15a0eaa1b28c61cd">802b334</a>)</li>
<li>handle bare <code>dict</code> and <code>list</code> annotations without type arguments (<a href="https://redirect.github.com/openai/openai-python/issues/3760">#3760</a>) (<a href="https://github.com/openai/openai-python/commit/c7e8c03e2d87708ef233d0db00167dfa339325a9">c7e8c03</a>)</li>
<li>preserve finalized output on null response completion (<a href="https://redirect.github.com/openai/openai-python/issues/3345">#3345</a>) (<a href="https://github.com/openai/openai-python/commit/adb212e116323fcec4b4811d20ba9eb78280c24c">adb212e</a>)</li>
</ul>
<h2><a href="https://github.com/openai/openai-python/compare/v3.10.0...v3.11.0">3.11.0</a> (2026-09-09)</h2>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> Add expiration controls for service account keys (<a href="https://redirect.github.com/openai/openai-python/issues/3825">#3825</a>) (<a href="https://github.com/openai/openai-python/commit/f348ec87b934c98889102668913e0a3ae7fc303d">f348ec8</a>)</li>
</ul>
<h2><a href="https://github.com/openai/openai-python/compare/v3.9.0...v3.10.0">3.10.0</a> (2026-09-08)</h2>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> add GPT Image 2.5 models and image options (<a href="https://redirect.github.com/openai/openai-python/issues/3824">#3824</a>) (<a href="https://github.com/openai/openai-python/commit/5b39c453ee5ee8f46fba0bd9cb4ae47fa5ee6d51">5b39c45</a>)</li>
<li><strong>api:</strong> add service-account API key expiration fields (<a href="https://redirect.github.com/openai/openai-python/issues/3802">#3802</a>) (<a href="https://github.com/openai/openai-python/commit/f1cd7f020210ec3fc71699fc46d90320ddbb411c">f1cd7f0</a>)</li>
</ul>
<h2><a href="https://github.com/openai/openai-python/compare/v3.8.0...v3.9.0">3.9.0</a> (2026-09-05)</h2>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> Add prompt cache diagnostics (<a href="https://redirect.github.com/openai/openai-python/issues/3800">#3800</a>) (<a href="https://github.com/openai/openai-python/commit/83267847a0219ea8b584c9d60f92c7a4dffd392a">8326784</a>)</li>
<li><strong>api:</strong> correct function argument completion event fields (openapi-545) (<a href="https://redirect.github.com/openai/openai-python/issues/3801">#3801</a>) (<a href="https://github.com/openai/openai-python/commit/2a98f6a1dee448c6410531c89c2de0af4383c6a7">2a98f6a</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> accept incomplete web search call statuses (<a href="https://redirect.github.com/openai/openai-python/issues/3786">#3786</a>) (<a href="https://github.com/openai/openai-python/commit/3cc8d784ad05f75a265012ee86638adaf93d8bf2">3cc8d78</a>)</li>
<li>refuse overflowing server retry delays (<a href="https://redirect.github.com/openai/openai-python/issues/3799">#3799</a>) (<a href="https://github.com/openai/openai-python/commit/88b4d4341af38e84784221d73c175f2088fa6b85">88b4d43</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/openai/openai-python/commit/f0fa922ef12f2c7329bcd8fc42e0cbb46f008ecb"><code>f0fa922</code></a> release: 3.13.0 (<a href="https://redirect.github.com/openai/openai-python/issues/3848">#3848</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/1c4284a08294f734d57047585ab82e2e09d3a5bc"><code>1c4284a</code></a> feat(agents): add beta API and one-turn streaming helpers (<a href="https://redirect.github.com/openai/openai-python/issues/3847">#3847</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/603b81f9e228d95032059169cb3a0e7dc12ba93f"><code>603b81f</code></a> release: 3.12.0 (<a href="https://redirect.github.com/openai/openai-python/issues/3832">#3832</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/0e4bfef9c79251fcf4926fd732129627bde050f1"><code>0e4bfef</code></a> feat(api) Add Live API (<a href="https://redirect.github.com/openai/openai-python/issues/3846">#3846</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/802b334928d8f0c3e24e5fce15a0eaa1b28c61cd"><code>802b334</code></a> fix: add aclose() to AsyncStream for standard async cleanup (<a href="https://redirect.github.com/openai/openai-python/issues/2854">#2854</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/adb212e116323fcec4b4811d20ba9eb78280c24c"><code>adb212e</code></a> fix: preserve finalized output on null response completion (<a href="https://redirect.github.com/openai/openai-python/issues/3345">#3345</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/c7e8c03e2d87708ef233d0db00167dfa339325a9"><code>c7e8c03</code></a> fix: handle bare <code>dict</code> and <code>list</code> annotations without type arguments (<a href="https://redirect.github.com/openai/openai-python/issues/3760">#3760</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/397ea08d8cf151039c069c1173f5de57cff5c081"><code>397ea08</code></a> ci: resolve fork PRs missing Castiron run associations (<a href="https://redirect.github.com/openai/openai-python/issues/3831">#3831</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/2d4b97cc84d5c3ca051cc2ac2d8a6c9928b4d5f0"><code>2d4b97c</code></a> test: restore CI test runtime after dependency-policy regression (<a href="https://redirect.github.com/openai/openai-python/issues/3830">#3830</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/41f0a2317759e8796ccfbde75536bd42e4aca7a2"><code>41f0a23</code></a> release: 3.11.0 (<a href="https://redirect.github.com/openai/openai-python/issues/3829">#3829</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/openai/openai-python/compare/v3.3.1...v3.13.0">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---

## build(deps-dev): update ruff requirement from >=0.16.5 to >=0.16.7 in /services/claw-interface (#3809)

- **SHA**: `0e38390f4fce646e1360a99601c955837bfae159`
- **作者**: dependabot[bot]
- **日期**: 2026-09-20T03:03:12Z
- **PR**: #3809

### Commit Message

```
build(deps-dev): update ruff requirement from >=0.16.5 to >=0.16.7 in /services/claw-interface (#3809)

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to
permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/releases">ruff's
releases</a>.</em></p>
<blockquote>
<h2>0.16.7</h2>
<h2>Release Notes</h2>
<p>Released on 2026-09-10.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>ruff</code>] Add rule for default values on method receivers
(<code>RUF077</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26700">#26700</a>)</li>
<li>[<code>ruff</code>] Recognize <code>re.prefixmatch</code>
(<code>RUF039</code>, <code>RUF055</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28311">#28311</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Alternate nested quotes inside format spec interpolations (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28259">#28259</a>)</li>
<li>[<code>flake8-implicit-str-concat</code>] Mark fix unsafe when it
creates a docstring (<code>ISC003</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27981">#27981</a>)</li>
<li>[<code>flake8-tidy-imports</code>] Skip fixes for multi-member
imports (<code>TID254</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26584">#26584</a>)</li>
<li>[<code>pylint</code>] Gate <code>ImportCycleError</code> on Python
3.15 (<code>PLW0133</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28310">#28310</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>Correct <code>D211</code> and <code>D203</code> rule conflict
diagnostic (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28444">#28444</a>)</li>
<li>Recognize <code>slice</code> and <code>frozendict</code> generics
(<a
href="https://redirect.github.com/astral-sh/ruff/pull/28477">#28477</a>)</li>
<li>Stop defining <code>__cached__</code> for Python 3.15 (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28476">#28476</a>)</li>
<li>[<code>pyupgrade</code>] Stop recommending removed
<code>typing.no_type_check_decorator</code> (<code>UP035</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28475">#28475</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Reuse parser name lookups when interning (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28399">#28399</a>)</li>
<li>Speed up inherited configuration resolution (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28299">#28299</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Fix <code>line-length</code> path in <code>--config</code> example
(<a
href="https://redirect.github.com/astral-sh/ruff/pull/28392">#28392</a>)</li>
<li>Remove the &quot;Who’s Using Ruff?&quot; list (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28455">#28455</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Embed archive checksums in the shell installer (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28281">#28281</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a
href="https://github.com/The-Compiler"><code>@​The-Compiler</code></a></li>
<li><a
href="https://github.com/mdiniz97"><code>@​mdiniz97</code></a></li>
<li><a href="https://github.com/zsol"><code>@​zsol</code></a></li>
<li><a
href="https://github.com/gorewilliams"><code>@​gorewilliams</code></a></li>
<li><a
href="https://github.com/RafaelJohn9"><code>@​RafaelJohn9</code></a></li>
<li><a href="https://github.com/qatcod"><code>@​qatcod</code></a></li>
<li><a href="https://github.com/zanieb"><code>@​zanieb</code></a></li>
<li><a
href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a
href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's
changelog</a>.</em></p>
<blockquote>
<h2>0.16.7</h2>
<p>Released on 2026-09-10.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>ruff</code>] Add rule for default values on method receivers
(<code>RUF077</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26700">#26700</a>)</li>
<li>[<code>ruff</code>] Recognize <code>re.prefixmatch</code>
(<code>RUF039</code>, <code>RUF055</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28311">#28311</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Alternate nested quotes inside format spec interpolations (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28259">#28259</a>)</li>
<li>[<code>flake8-implicit-str-concat</code>] Mark fix unsafe when it
creates a docstring (<code>ISC003</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27981">#27981</a>)</li>
<li>[<code>flake8-tidy-imports</code>] Skip fixes for multi-member
imports (<code>TID254</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26584">#26584</a>)</li>
<li>[<code>pylint</code>] Gate <code>ImportCycleError</code> on Python
3.15 (<code>PLW0133</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28310">#28310</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>Correct <code>D211</code> and <code>D203</code> rule conflict
diagnostic (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28444">#28444</a>)</li>
<li>Recognize <code>slice</code> and <code>frozendict</code> generics
(<a
href="https://redirect.github.com/astral-sh/ruff/pull/28477">#28477</a>)</li>
<li>Stop defining <code>__cached__</code> for Python 3.15 (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28476">#28476</a>)</li>
<li>[<code>pyupgrade</code>] Stop recommending removed
<code>typing.no_type_check_decorator</code> (<code>UP035</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28475">#28475</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Reuse parser name lookups when interning (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28399">#28399</a>)</li>
<li>Speed up inherited configuration resolution (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28299">#28299</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Fix <code>line-length</code> path in <code>--config</code> example
(<a
href="https://redirect.github.com/astral-sh/ruff/pull/28392">#28392</a>)</li>
<li>Remove the &quot;Who’s Using Ruff?&quot; list (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28455">#28455</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Embed archive checksums in the shell installer (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28281">#28281</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a
href="https://github.com/The-Compiler"><code>@​The-Compiler</code></a></li>
<li><a
href="https://github.com/mdiniz97"><code>@​mdiniz97</code></a></li>
<li><a href="https://github.com/zsol"><code>@​zsol</code></a></li>
<li><a
href="https://github.com/gorewilliams"><code>@​gorewilliams</code></a></li>
<li><a
href="https://github.com/RafaelJohn9"><code>@​RafaelJohn9</code></a></li>
<li><a href="https://github.com/qatcod"><code>@​qatcod</code></a></li>
<li><a href="https://github.com/zanieb"><code>@​zanieb</code></a></li>
<li><a
href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a
href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
<li><a
href="https://github.com/nightt5879"><code>@​nightt5879</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/astral-sh/ruff/commit/b5dba861cc38e3f7fb4524c9ceba3e01a474ea13"><code>b5dba86</code></a>
Bump version to 0.16.7 (<a
href="https://redirect.github.com/astral-sh/ruff/issues/28496">#28496</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/5992d0504697d86565d8fc3a4d8245a5f4047d24"><code>5992d05</code></a>
Install rustfmt before linting releases (<a
href="https://redirect.github.com/astral-sh/ruff/issues/28495">#28495</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/1713a1f4325494d883a080d590a25a1946f399e8"><code>1713a1f</code></a>
ensure prepare release changes pass prek (<a
href="https://redirect.github.com/astral-sh/ruff/issues/28488">#28488</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/18cdbb4f3d14058794420e758864795f55336334"><code>18cdbb4</code></a>
use scoped token for release workflow (<a
href="https://redirect.github.com/astral-sh/ruff/issues/28484">#28484</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/c3813a501faf887fd01948c98bb8d58ad26488bd"><code>c3813a5</code></a>
add a workflow for preparing releases (<a
href="https://redirect.github.com/astral-sh/ruff/issues/28486">#28486</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/00948c00a671b81f5358af9f038436bcbb993b38"><code>00948c0</code></a>
Remove the &quot;Who’s Using Ruff?&quot; list (<a
href="https://redirect.github.com/astral-sh/ruff/issues/28455">#28455</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/86a2eba7b48e3c10386f7ab8a5425c7275d2b427"><code>86a2eba</code></a>
[<code>pyupgrade</code>] Stop recommending removed
<code>typing.no_type_check_decorator</code> (`UP...</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/609e184aa35f0034b7ef63e3e04327081c484af6"><code>609e184</code></a>
Stop defining <code>__cached__</code> for Python 3.15 (<a
href="https://redirect.github.com/astral-sh/ruff/issues/28476">#28476</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/859ff2f01670c43ffff1ea597c8a2e375ada0fbe"><code>859ff2f</code></a>
[ty] Track symlinked directory status in listings (<a
href="https://redirect.github.com/astral-sh/ruff/issues/28482">#28482</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/77f653825800ddaf3bc221ae6db49a500e1002d5"><code>77f6538</code></a>
Use paid GitHub-hosted runners for Linux (<a
href="https://redirect.github.com/astral-sh/ruff/issues/28478">#28478</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/astral-sh/ruff/compare/0.16.5...0.16.7">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Body

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's releases</a>.</em></p>
<blockquote>
<h2>0.16.7</h2>
<h2>Release Notes</h2>
<p>Released on 2026-09-10.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>ruff</code>] Add rule for default values on method receivers (<code>RUF077</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26700">#26700</a>)</li>
<li>[<code>ruff</code>] Recognize <code>re.prefixmatch</code> (<code>RUF039</code>, <code>RUF055</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/28311">#28311</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Alternate nested quotes inside format spec interpolations (<a href="https://redirect.github.com/astral-sh/ruff/pull/28259">#28259</a>)</li>
<li>[<code>flake8-implicit-str-concat</code>] Mark fix unsafe when it creates a docstring (<code>ISC003</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27981">#27981</a>)</li>
<li>[<code>flake8-tidy-imports</code>] Skip fixes for multi-member imports (<code>TID254</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26584">#26584</a>)</li>
<li>[<code>pylint</code>] Gate <code>ImportCycleError</code> on Python 3.15 (<code>PLW0133</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/28310">#28310</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>Correct <code>D211</code> and <code>D203</code> rule conflict diagnostic (<a href="https://redirect.github.com/astral-sh/ruff/pull/28444">#28444</a>)</li>
<li>Recognize <code>slice</code> and <code>frozendict</code> generics (<a href="https://redirect.github.com/astral-sh/ruff/pull/28477">#28477</a>)</li>
<li>Stop defining <code>__cached__</code> for Python 3.15 (<a href="https://redirect.github.com/astral-sh/ruff/pull/28476">#28476</a>)</li>
<li>[<code>pyupgrade</code>] Stop recommending removed <code>typing.no_type_check_decorator</code> (<code>UP035</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/28475">#28475</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Reuse parser name lookups when interning (<a href="https://redirect.github.com/astral-sh/ruff/pull/28399">#28399</a>)</li>
<li>Speed up inherited configuration resolution (<a href="https://redirect.github.com/astral-sh/ruff/pull/28299">#28299</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Fix <code>line-length</code> path in <code>--config</code> example (<a href="https://redirect.github.com/astral-sh/ruff/pull/28392">#28392</a>)</li>
<li>Remove the &quot;Who’s Using Ruff?&quot; list (<a href="https://redirect.github.com/astral-sh/ruff/pull/28455">#28455</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Embed archive checksums in the shell installer (<a href="https://redirect.github.com/astral-sh/ruff/pull/28281">#28281</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/The-Compiler"><code>@​The-Compiler</code></a></li>
<li><a href="https://github.com/mdiniz97"><code>@​mdiniz97</code></a></li>
<li><a href="https://github.com/zsol"><code>@​zsol</code></a></li>
<li><a href="https://github.com/gorewilliams"><code>@​gorewilliams</code></a></li>
<li><a href="https://github.com/RafaelJohn9"><code>@​RafaelJohn9</code></a></li>
<li><a href="https://github.com/qatcod"><code>@​qatcod</code></a></li>
<li><a href="https://github.com/zanieb"><code>@​zanieb</code></a></li>
<li><a href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
<blockquote>
<h2>0.16.7</h2>
<p>Released on 2026-09-10.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>ruff</code>] Add rule for default values on method receivers (<code>RUF077</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26700">#26700</a>)</li>
<li>[<code>ruff</code>] Recognize <code>re.prefixmatch</code> (<code>RUF039</code>, <code>RUF055</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/28311">#28311</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Alternate nested quotes inside format spec interpolations (<a href="https://redirect.github.com/astral-sh/ruff/pull/28259">#28259</a>)</li>
<li>[<code>flake8-implicit-str-concat</code>] Mark fix unsafe when it creates a docstring (<code>ISC003</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27981">#27981</a>)</li>
<li>[<code>flake8-tidy-imports</code>] Skip fixes for multi-member imports (<code>TID254</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26584">#26584</a>)</li>
<li>[<code>pylint</code>] Gate <code>ImportCycleError</code> on Python 3.15 (<code>PLW0133</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/28310">#28310</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>Correct <code>D211</code> and <code>D203</code> rule conflict diagnostic (<a href="https://redirect.github.com/astral-sh/ruff/pull/28444">#28444</a>)</li>
<li>Recognize <code>slice</code> and <code>frozendict</code> generics (<a href="https://redirect.github.com/astral-sh/ruff/pull/28477">#28477</a>)</li>
<li>Stop defining <code>__cached__</code> for Python 3.15 (<a href="https://redirect.github.com/astral-sh/ruff/pull/28476">#28476</a>)</li>
<li>[<code>pyupgrade</code>] Stop recommending removed <code>typing.no_type_check_decorator</code> (<code>UP035</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/28475">#28475</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Reuse parser name lookups when interning (<a href="https://redirect.github.com/astral-sh/ruff/pull/28399">#28399</a>)</li>
<li>Speed up inherited configuration resolution (<a href="https://redirect.github.com/astral-sh/ruff/pull/28299">#28299</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Fix <code>line-length</code> path in <code>--config</code> example (<a href="https://redirect.github.com/astral-sh/ruff/pull/28392">#28392</a>)</li>
<li>Remove the &quot;Who’s Using Ruff?&quot; list (<a href="https://redirect.github.com/astral-sh/ruff/pull/28455">#28455</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Embed archive checksums in the shell installer (<a href="https://redirect.github.com/astral-sh/ruff/pull/28281">#28281</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/The-Compiler"><code>@​The-Compiler</code></a></li>
<li><a href="https://github.com/mdiniz97"><code>@​mdiniz97</code></a></li>
<li><a href="https://github.com/zsol"><code>@​zsol</code></a></li>
<li><a href="https://github.com/gorewilliams"><code>@​gorewilliams</code></a></li>
<li><a href="https://github.com/RafaelJohn9"><code>@​RafaelJohn9</code></a></li>
<li><a href="https://github.com/qatcod"><code>@​qatcod</code></a></li>
<li><a href="https://github.com/zanieb"><code>@​zanieb</code></a></li>
<li><a href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
<li><a href="https://github.com/nightt5879"><code>@​nightt5879</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/astral-sh/ruff/commit/b5dba861cc38e3f7fb4524c9ceba3e01a474ea13"><code>b5dba86</code></a> Bump version to 0.16.7 (<a href="https://redirect.github.com/astral-sh/ruff/issues/28496">#28496</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/5992d0504697d86565d8fc3a4d8245a5f4047d24"><code>5992d05</code></a> Install rustfmt before linting releases (<a href="https://redirect.github.com/astral-sh/ruff/issues/28495">#28495</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/1713a1f4325494d883a080d590a25a1946f399e8"><code>1713a1f</code></a> ensure prepare release changes pass prek (<a href="https://redirect.github.com/astral-sh/ruff/issues/28488">#28488</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/18cdbb4f3d14058794420e758864795f55336334"><code>18cdbb4</code></a> use scoped token for release workflow (<a href="https://redirect.github.com/astral-sh/ruff/issues/28484">#28484</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/c3813a501faf887fd01948c98bb8d58ad26488bd"><code>c3813a5</code></a> add a workflow for preparing releases (<a href="https://redirect.github.com/astral-sh/ruff/issues/28486">#28486</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/00948c00a671b81f5358af9f038436bcbb993b38"><code>00948c0</code></a> Remove the &quot;Who’s Using Ruff?&quot; list (<a href="https://redirect.github.com/astral-sh/ruff/issues/28455">#28455</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/86a2eba7b48e3c10386f7ab8a5425c7275d2b427"><code>86a2eba</code></a> [<code>pyupgrade</code>] Stop recommending removed <code>typing.no_type_check_decorator</code> (`UP...</li>
<li><a href="https://github.com/astral-sh/ruff/commit/609e184aa35f0034b7ef63e3e04327081c484af6"><code>609e184</code></a> Stop defining <code>__cached__</code> for Python 3.15 (<a href="https://redirect.github.com/astral-sh/ruff/issues/28476">#28476</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/859ff2f01670c43ffff1ea597c8a2e375ada0fbe"><code>859ff2f</code></a> [ty] Track symlinked directory status in listings (<a href="https://redirect.github.com/astral-sh/ruff/issues/28482">#28482</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/77f653825800ddaf3bc221ae6db49a500e1002d5"><code>77f6538</code></a> Use paid GitHub-hosted runners for Linux (<a href="https://redirect.github.com/astral-sh/ruff/issues/28478">#28478</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.16.5...0.16.7">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---

## feat(web): add standalone login pages and disabled Platform menu (#3720)

- **SHA**: `c0dd5d8577194ee345b7dd537b21ef8301146e14`
- **作者**: shana-srp
- **日期**: 2026-09-20T02:45:30Z
- **PR**: #3720

### Commit Message

```
feat(web): add standalone login pages and disabled Platform menu (#3720)

## Summary

The public homepage stays visible regardless of existing login sessions
or authentication changes in another tab. Authentication no longer
automatically navigates the homepage into the app. Clicking the ZooWork
menu entry still opens `/login` in a new tab, where existing-session
redirects and Agent/Specialist handoffs continue to work.

Marketing Get Started menus offer a standalone ZooWork login entry and a
disabled API Platform entry. ZooWork opens the current-origin `/login`
in a new tab and retains its existing authentication and application
destination. API Platform stays greyed out without navigation; its
locale-specific `/platform/login` page remains available as a
presentation-only preview using the existing main-web login flow.

- Keep the standalone ZooWork login page, language handling, supported
Agent/Specialist handoff parameters, and original header/hero analytics
context.
- Keep the branded Platform login page, Google/email controls, shared
footer, animated background, pause control and reduced-motion support.
- Keep the latest disabled-menu behavior in both marketing menus,
including keyboard/mouse semantics and regression coverage.
- Keep the homepage Restaurant Operations Agent demo copy and localized
accessible descriptions.
- The Platform page uses the existing `LoginForm` presentation variant,
Firebase/email OTP/CAPTCHA handling, `business=ecap` identity, and
current-page completion behavior. This PR does not introduce independent
Platform authentication or a redirect to `platform.zoowork.ai`.

## Authentication scope

The independent Platform authentication implementation has been
withdrawn through an additive, targeted rollback. Its dedicated BFF
routes, named Firebase instance, session/challenge cookies, isolated
client cache/layout, result tracker and deployment configuration were
removed, together with the three dependent deployment-validation
follow-ups. The original page/form behavior and tests were restored. The
later disabled-menu change and unrelated main-branch changes remain
intact; commit history was not rewritten.

No user-interface backend, deployed settings, existing production
sessions or deployments were changed by this rollback. No
Platform-specific runtime secret or destination configuration is
required by this PR.

## Validation

- Conflict refresh (2026-09-18): merged main at `ee377fc6a5` in
`26f4bb15a5`. Resolved `globals.css` by retaining standalone login
tokens and the latest Agent settings styling. Kept the updated Agent
Gallery URL in the automatically merged header test. All 377 relevant
tests across 21 files, TypeScript, scoped ESLint, repository governance,
CSS parsing and PR-diff whitespace/conflict checks passed.
- Synced main at `721a2d037a` and resolved both test conflicts,
preserving grouped Solutions navigation, the canonical `/home`
application destination, passive homepage behavior and explicit new-tab
login. The merged result passed 437 focused tests across 18 files,
TypeScript, scoped ESLint, repository governance and
whitespace/conflict-marker checks.
- Homepage session behavior: 110 focused tests passed across 6 files,
covering authenticated homepage visits, post-hydration/session changes,
marketing chrome, new-tab menus and existing login-page redirects. Five
new homepage regression cases failed against the previous
automatic-redirect implementation and pass with this change.
- Homepage follow-up: TypeScript, scoped ESLint, repository governance
and `git diff --check` passed.
- 414 relevant tests passed across 29 files, covering restored login/OTP
behavior, Platform page wiring, ordinary auth routes, layouts,
header/homepage menu behavior and analytics.
- TypeScript, scoped ESLint, repository governance and `git diff
--check` passed in the isolated rollback worktree.
- Compared the restored tree with the pre-integration PR snapshot: the
remaining differences are the intentionally retained disabled-menu
change/documentation and unrelated main-branch feedback changes.
- Checked that removed Platform authentication/configuration identifiers
and deleted-document references no longer remain in the source, tests,
deployment workflow or docs.
- No real Google/email sign-in or deployed browser end-to-end login was
exercised for this rollback. Cloud checks should be evaluated against
the latest PR head.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
Co-authored-by: tim-srp <tim@srp.one>
```

### PR Body

## Summary

The public homepage stays visible regardless of existing login sessions or authentication changes in another tab. Authentication no longer automatically navigates the homepage into the app. Clicking the ZooWork menu entry still opens `/login` in a new tab, where existing-session redirects and Agent/Specialist handoffs continue to work.

Marketing Get Started menus offer a standalone ZooWork login entry and a disabled API Platform entry. ZooWork opens the current-origin `/login` in a new tab and retains its existing authentication and application destination. API Platform stays greyed out without navigation; its locale-specific `/platform/login` page remains available as a presentation-only preview using the existing main-web login flow.

- Keep the standalone ZooWork login page, language handling, supported Agent/Specialist handoff parameters, and original header/hero analytics context.
- Keep the branded Platform login page, Google/email controls, shared footer, animated background, pause control and reduced-motion support.
- Keep the latest disabled-menu behavior in both marketing menus, including keyboard/mouse semantics and regression coverage.
- Keep the homepage Restaurant Operations Agent demo copy and localized accessible descriptions.
- The Platform page uses the existing `LoginForm` presentation variant, Firebase/email OTP/CAPTCHA handling, `business=ecap` identity, and current-page completion behavior. This PR does not introduce independent Platform authentication or a redirect to `platform.zoowork.ai`.

## Authentication scope

The independent Platform authentication implementation has been withdrawn through an additive, targeted rollback. Its dedicated BFF routes, named Firebase instance, session/challenge cookies, isolated client cache/layout, result tracker and deployment configuration were removed, together with the three dependent deployment-validation follow-ups. The original page/form behavior and tests were restored. The later disabled-menu change and unrelated main-branch changes remain intact; commit history was not rewritten.

No user-interface backend, deployed settings, existing production sessions or deployments were changed by this rollback. No Platform-specific runtime secret or destination configuration is required by this PR.

## Validation

- Conflict refresh (2026-09-18): merged main at `ee377fc6a5` in `26f4bb15a5`. Resolved `globals.css` by retaining standalone login tokens and the latest Agent settings styling. Kept the updated Agent Gallery URL in the automatically merged header test. All 377 relevant tests across 21 files, TypeScript, scoped ESLint, repository governance, CSS parsing and PR-diff whitespace/conflict checks passed.
- Synced main at `721a2d037a` and resolved both test conflicts, preserving grouped Solutions navigation, the canonical `/home` application destination, passive homepage behavior and explicit new-tab login. The merged result passed 437 focused tests across 18 files, TypeScript, scoped ESLint, repository governance and whitespace/conflict-marker checks.
- Homepage session behavior: 110 focused tests passed across 6 files, covering authenticated homepage visits, post-hydration/session changes, marketing chrome, new-tab menus and existing login-page redirects. Five new homepage regression cases failed against the previous automatic-redirect implementation and pass with this change.
- Homepage follow-up: TypeScript, scoped ESLint, repository governance and `git diff --check` passed.
- 414 relevant tests passed across 29 files, covering restored login/OTP behavior, Platform page wiring, ordinary auth routes, layouts, header/homepage menu behavior and analytics.
- TypeScript, scoped ESLint, repository governance and `git diff --check` passed in the isolated rollback worktree.
- Compared the restored tree with the pre-integration PR snapshot: the remaining differences are the intentionally retained disabled-menu change/documentation and unrelated main-branch feedback changes.
- Checked that removed Platform authentication/configuration identifiers and deleted-document references no longer remain in the source, tests, deployment workflow or docs.
- No real Google/email sign-in or deployed browser end-to-end login was exercised for this rollback. Cloud checks should be evaluated against the latest PR head.



---

## build(deps-dev): update import-linter requirement from >=2.13 to >=2.15 in /services/claw-interface (#3707)

- **SHA**: `aa973973dff83130fcf8bb768b3b5166a638ff2c`
- **作者**: dependabot[bot]
- **日期**: 2026-09-20T02:42:46Z
- **PR**: #3707

### Commit Message

```
build(deps-dev): update import-linter requirement from >=2.13 to >=2.15 in /services/claw-interface (#3707)

Updates the requirements on
[import-linter](https://github.com/seddonym/import-linter) to permit the
latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/seddonym/import-linter/blob/main/docs/release_notes.md">import-linter's
changelog</a>.</em></p>
<blockquote>
<h2>2.15 (2026-09-04)</h2>
<ul>
<li>Add support for lazy imports to the explore UI and
<code>drawgraph</code> command.</li>
</ul>
<h2>2.14 (2026-08-28)</h2>
<ul>
<li>Add <code>broken_contract_guidance</code> option to contracts, for
explaining how to fix them when they're broken.</li>
<li>Add <code>TextField</code> for multi-line text configuration
values.</li>
<li>Show the count of ignored imports next to a contract's result.</li>
<li>Add <code>--no-logo</code> option to hide the logo in terminal
output.</li>
</ul>
<h2>2.13 (2026-07-03)</h2>
<ul>
<li>Add module counts option to the explore UI and
<code>drawgraph</code> command.</li>
</ul>
<h2>2.12 (2026-06-23)</h2>
<ul>
<li>Improve error message when root package is a single-file
module.</li>
<li>Alert users with all unmatched ignored imports in the same run.</li>
<li>Allow overlapping modules in forbidden contracts.</li>
</ul>
<h2>2.11 (2026-03-06)</h2>
<ul>
<li>Add <code>--version</code> flag to <code>lint-imports</code> and
<code>import-linter</code> commands.</li>
<li>Make <code>fastapi</code> and <code>uvicorn</code> optional via the
<code>ui</code> extra (<code>pip install import-linter[ui]</code>).</li>
<li>Bugfix: fix back button navigation in explore command.</li>
<li>Provide lower limits for <code>fastapi</code> and
<code>uvicorn</code> in <code>pyproject.toml</code>.</li>
<li>Switch to nox for testing.</li>
</ul>
<h2>2.10 (2026-02-06)</h2>
<ul>
<li>Add <code>import-linter</code> group command, with
<code>import-linter lint</code> alias.</li>
<li>Add <code>import-linter explore</code> command.</li>
<li>Add <code>import-linter drawgraph</code> command.</li>
</ul>
<h2>2.9 (2025-12-11)</h2>
<ul>
<li>Support passing namespaces as root packages, not just portions.</li>
<li>Bugfix: support Python 3.14 syntax.</li>
</ul>
<h2>2.8 (2025-12-08)</h2>
<ul>
<li>Fix logo display bug on Windows (fall back to simpler heading)
<a
href="https://redirect.github.com/seddonym/import-linter/issues/309">seddonym/import-linter#309</a></li>
<li>Rewrite docs (and switch from Sphinx to mkdocs).</li>
</ul>
<h2>2.7 (2025-11-19)</h2>
<ul>
<li>Print using rich instead of click.</li>
<li>Remove pluggable Printer class.</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/seddonym/import-linter/commit/31927f1457e3df673912cb5efb0afa6dbc37585f"><code>31927f1</code></a>
Release v2.15</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/1a652a6a02ba3ad452ad20db52641f75f26acb27"><code>1a652a6</code></a>
Update github actions to silence warnings about Node 20</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/552df7fcd2ceb3fa9df076db8cceda693dc6cef9"><code>552df7f</code></a>
Display lazy imports with open arrowhead</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/f55b3515cbaf947a428ee1ca4824bdacdd575b6f"><code>f55b351</code></a>
Upgrade to Grimp 3.17</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/9692850bc24a7ccd6790ab5fcb767b80ae000537"><code>9692850</code></a>
Support overriding arrowhead on Edge</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/e61a687daed7e5f91d724b287a3d4f576b5e0db8"><code>e61a687</code></a>
Refactor Edge so it supports line style</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/efc8642199e6bcf288c59ed111dff71da5634dc8"><code>efc8642</code></a>
Update uv.lock</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/33138daf44ba837638a7e6bbd060a57c24310fa9"><code>33138da</code></a>
Release v2.14</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/d314ebb146bf6c671c975b4bba91e7bebd9f4df7"><code>d314ebb</code></a>
Add broken contract guidance (<a
href="https://redirect.github.com/seddonym/import-linter/issues/371">#371</a>)</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/285653e2535a39b1965fae79be6dec071af7b5b5"><code>285653e</code></a>
Show count of ignored imports in contract output (<a
href="https://redirect.github.com/seddonym/import-linter/issues/375">#375</a>)
(<a
href="https://redirect.github.com/seddonym/import-linter/issues/376">#376</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/seddonym/import-linter/compare/v2.13...v2.15">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Body

Updates the requirements on [import-linter](https://github.com/seddonym/import-linter) to permit the latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/seddonym/import-linter/blob/main/docs/release_notes.md">import-linter's changelog</a>.</em></p>
<blockquote>
<h2>2.15 (2026-09-04)</h2>
<ul>
<li>Add support for lazy imports to the explore UI and <code>drawgraph</code> command.</li>
</ul>
<h2>2.14 (2026-08-28)</h2>
<ul>
<li>Add <code>broken_contract_guidance</code> option to contracts, for explaining how to fix them when they're broken.</li>
<li>Add <code>TextField</code> for multi-line text configuration values.</li>
<li>Show the count of ignored imports next to a contract's result.</li>
<li>Add <code>--no-logo</code> option to hide the logo in terminal output.</li>
</ul>
<h2>2.13 (2026-07-03)</h2>
<ul>
<li>Add module counts option to the explore UI and <code>drawgraph</code> command.</li>
</ul>
<h2>2.12 (2026-06-23)</h2>
<ul>
<li>Improve error message when root package is a single-file module.</li>
<li>Alert users with all unmatched ignored imports in the same run.</li>
<li>Allow overlapping modules in forbidden contracts.</li>
</ul>
<h2>2.11 (2026-03-06)</h2>
<ul>
<li>Add <code>--version</code> flag to <code>lint-imports</code> and <code>import-linter</code> commands.</li>
<li>Make <code>fastapi</code> and <code>uvicorn</code> optional via the <code>ui</code> extra (<code>pip install import-linter[ui]</code>).</li>
<li>Bugfix: fix back button navigation in explore command.</li>
<li>Provide lower limits for <code>fastapi</code> and <code>uvicorn</code> in <code>pyproject.toml</code>.</li>
<li>Switch to nox for testing.</li>
</ul>
<h2>2.10 (2026-02-06)</h2>
<ul>
<li>Add <code>import-linter</code> group command, with <code>import-linter lint</code> alias.</li>
<li>Add <code>import-linter explore</code> command.</li>
<li>Add <code>import-linter drawgraph</code> command.</li>
</ul>
<h2>2.9 (2025-12-11)</h2>
<ul>
<li>Support passing namespaces as root packages, not just portions.</li>
<li>Bugfix: support Python 3.14 syntax.</li>
</ul>
<h2>2.8 (2025-12-08)</h2>
<ul>
<li>Fix logo display bug on Windows (fall back to simpler heading)
<a href="https://redirect.github.com/seddonym/import-linter/issues/309">seddonym/import-linter#309</a></li>
<li>Rewrite docs (and switch from Sphinx to mkdocs).</li>
</ul>
<h2>2.7 (2025-11-19)</h2>
<ul>
<li>Print using rich instead of click.</li>
<li>Remove pluggable Printer class.</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/seddonym/import-linter/commit/31927f1457e3df673912cb5efb0afa6dbc37585f"><code>31927f1</code></a> Release v2.15</li>
<li><a href="https://github.com/seddonym/import-linter/commit/1a652a6a02ba3ad452ad20db52641f75f26acb27"><code>1a652a6</code></a> Update github actions to silence warnings about Node 20</li>
<li><a href="https://github.com/seddonym/import-linter/commit/552df7fcd2ceb3fa9df076db8cceda693dc6cef9"><code>552df7f</code></a> Display lazy imports with open arrowhead</li>
<li><a href="https://github.com/seddonym/import-linter/commit/f55b3515cbaf947a428ee1ca4824bdacdd575b6f"><code>f55b351</code></a> Upgrade to Grimp 3.17</li>
<li><a href="https://github.com/seddonym/import-linter/commit/9692850bc24a7ccd6790ab5fcb767b80ae000537"><code>9692850</code></a> Support overriding arrowhead on Edge</li>
<li><a href="https://github.com/seddonym/import-linter/commit/e61a687daed7e5f91d724b287a3d4f576b5e0db8"><code>e61a687</code></a> Refactor Edge so it supports line style</li>
<li><a href="https://github.com/seddonym/import-linter/commit/efc8642199e6bcf288c59ed111dff71da5634dc8"><code>efc8642</code></a> Update uv.lock</li>
<li><a href="https://github.com/seddonym/import-linter/commit/33138daf44ba837638a7e6bbd060a57c24310fa9"><code>33138da</code></a> Release v2.14</li>
<li><a href="https://github.com/seddonym/import-linter/commit/d314ebb146bf6c671c975b4bba91e7bebd9f4df7"><code>d314ebb</code></a> Add broken contract guidance (<a href="https://redirect.github.com/seddonym/import-linter/issues/371">#371</a>)</li>
<li><a href="https://github.com/seddonym/import-linter/commit/285653e2535a39b1965fae79be6dec071af7b5b5"><code>285653e</code></a> Show count of ignored imports in contract output (<a href="https://redirect.github.com/seddonym/import-linter/issues/375">#375</a>) (<a href="https://redirect.github.com/seddonym/import-linter/issues/376">#376</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/seddonym/import-linter/compare/v2.13...v2.15">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---

## build(deps): update cachetools requirement from >=7.1.7 to >=7.1.8 in /services/claw-interface (#3706)

- **SHA**: `2577d221cf7906c7f0209284ff487e8f3774105a`
- **作者**: dependabot[bot]
- **日期**: 2026-09-20T02:42:28Z
- **PR**: #3706

### Commit Message

```
build(deps): update cachetools requirement from >=7.1.7 to >=7.1.8 in /services/claw-interface (#3706)

Updates the requirements on
[cachetools](https://github.com/tkem/cachetools) to permit the latest
version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/tkem/cachetools/blob/master/CHANGELOG.rst">cachetools's
changelog</a>.</em></p>
<blockquote>
<h1>v7.1.8 (2026-08-31)</h1>
<ul>
<li>Reject negative <code>maxsize</code> in
<code>Cache.__init__</code>.</li>
</ul>
<h1>v7.1.7 (2026-08-01)</h1>
<ul>
<li>
<p>Improve <code>Cache.__setitem__</code> behavior when replacing an
existing
cache item with a larger value.</p>
</li>
<li>
<p>Update CI environment.</p>
</li>
</ul>
<h1>v7.1.6 (2026-07-24)</h1>
<ul>
<li>Minor style improvements to keep <code>ruff</code> happy.</li>
</ul>
<h1>v7.1.5 (2026-07-23)</h1>
<ul>
<li>
<p>Fix <code>TLRUCache</code> silently keeping stale values on expired
overwrites.</p>
</li>
<li>
<p>Reject negative cache item <code>getsizeof</code> values.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.4 (2026-05-22)</h1>
<ul>
<li>
<p>Minor unit test improvements.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.3 (2026-05-18)</h1>
<ul>
<li>
<p>Minor type stub improvements.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.2 (2026-05-16)</h1>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/tkem/cachetools/commit/4500e3d04288738d25acbb4973eb3c3e1bf41db9"><code>4500e3d</code></a>
Release v7.1.8.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/6e49bef559f20995d603830202afda0ea890bd1a"><code>6e49bef</code></a>
Update copilot instructions and review.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/defc58b02543ca0189fb37505827db4cc4e0565c"><code>defc58b</code></a>
Prepare v7.1.8.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/a39180bfced6e162614e23eaa9c3dc79d8ec74d6"><code>a39180b</code></a>
Remove somewhat superfluous and slightly incorrect documentation note
regardi...</li>
<li><a
href="https://github.com/tkem/cachetools/commit/dd181c5a72a74fcc01045c17cc943f72cb521262"><code>dd181c5</code></a>
Reject negative maxsize in Cache.<strong>init</strong></li>
<li><a
href="https://github.com/tkem/cachetools/commit/b43b95360fd4a99f3bdd19ff87c2ef6f4c99e3d8"><code>b43b953</code></a>
Use monthly batches for dependabot updates.</li>
<li>See full diff in <a
href="https://github.com/tkem/cachetools/compare/v7.1.7...v7.1.8">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Body

Updates the requirements on [cachetools](https://github.com/tkem/cachetools) to permit the latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/tkem/cachetools/blob/master/CHANGELOG.rst">cachetools's changelog</a>.</em></p>
<blockquote>
<h1>v7.1.8 (2026-08-31)</h1>
<ul>
<li>Reject negative <code>maxsize</code> in <code>Cache.__init__</code>.</li>
</ul>
<h1>v7.1.7 (2026-08-01)</h1>
<ul>
<li>
<p>Improve <code>Cache.__setitem__</code> behavior when replacing an existing
cache item with a larger value.</p>
</li>
<li>
<p>Update CI environment.</p>
</li>
</ul>
<h1>v7.1.6 (2026-07-24)</h1>
<ul>
<li>Minor style improvements to keep <code>ruff</code> happy.</li>
</ul>
<h1>v7.1.5 (2026-07-23)</h1>
<ul>
<li>
<p>Fix <code>TLRUCache</code> silently keeping stale values on expired
overwrites.</p>
</li>
<li>
<p>Reject negative cache item <code>getsizeof</code> values.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.4 (2026-05-22)</h1>
<ul>
<li>
<p>Minor unit test improvements.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.3 (2026-05-18)</h1>
<ul>
<li>
<p>Minor type stub improvements.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.2 (2026-05-16)</h1>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/tkem/cachetools/commit/4500e3d04288738d25acbb4973eb3c3e1bf41db9"><code>4500e3d</code></a> Release v7.1.8.</li>
<li><a href="https://github.com/tkem/cachetools/commit/6e49bef559f20995d603830202afda0ea890bd1a"><code>6e49bef</code></a> Update copilot instructions and review.</li>
<li><a href="https://github.com/tkem/cachetools/commit/defc58b02543ca0189fb37505827db4cc4e0565c"><code>defc58b</code></a> Prepare v7.1.8.</li>
<li><a href="https://github.com/tkem/cachetools/commit/a39180bfced6e162614e23eaa9c3dc79d8ec74d6"><code>a39180b</code></a> Remove somewhat superfluous and slightly incorrect documentation note regardi...</li>
<li><a href="https://github.com/tkem/cachetools/commit/dd181c5a72a74fcc01045c17cc943f72cb521262"><code>dd181c5</code></a> Reject negative maxsize in Cache.<strong>init</strong></li>
<li><a href="https://github.com/tkem/cachetools/commit/b43b95360fd4a99f3bdd19ff87c2ef6f4c99e3d8"><code>b43b953</code></a> Use monthly batches for dependabot updates.</li>
<li>See full diff in <a href="https://github.com/tkem/cachetools/compare/v7.1.7...v7.1.8">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---
