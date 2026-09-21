---
title: "feat(agents): sync user timezone to engine Agents (#3813)"
type: "新功能"
priority: "中"
date: "2026-09-20"
status: "待审核"
channels: ""
---

# Agent 创建与更新会同步用户时区

## 核心宣传点

所有 Agent 创建入口（默认主 Agent、Pack 安装、Agent Builder 的 Pack 测试预览、v2 Agent 开发流程）现在都会读取账号 locale 里的时区，并传给 Engine；更新 Agent 时也会带上。对用户的实际意义是：定时任务、日程和时间相关的表达会按你自己的时区来算，不再默认按 UTC 处理。

## 分级

- 内部：P1
- 外部：B
- 发布状态：已合并待发版

## PR 说明

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


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `87b4dd8e4fe37e6485e9b18e69374898fb9e99df`
- PR: #3813
- 作者：tim-srp
- 日期：2026-09-20T14:59:46Z

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

来源：SerendipityOneInc/ecap-workspace @ 87b4dd8e，PR #3813，作者 tim-srp。