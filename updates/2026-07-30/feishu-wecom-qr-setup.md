---
title: "飞书/企业微信一键扫码接入（引导式配置）"
type: "新功能上线"
priority: "高"
外部: "B"
date: "2026-07-30"
status: "待审核"
channels: ""
---

## 核心宣传点

接入飞书、企业微信更简单了：全新引导式扫码配置向导，自动完成应用注册握手，无需再手动打开开发者后台创建应用、复制两串密钥。手动填写仍作为备选保留。

## 原始内容

**Commit**: c868af2f (PR #3137)
**外部评级**: A | **内部**: P1 | **信息类型**: 新功能上线

### Commit Message

```
feat(channels): add engine Feishu/WeCom guided QR setup (#3137)

## Linear

No Linear issue — this is spec-driven work. Design of record:
[`docs/superpowers/specs/2026-07-29-engine-feishu-wecom-qr-setup.md`](../blob/codex/engine-feishu-wecom-qr/docs/superpowers/specs/2026-07-29-engine-feishu-wecom-qr-setup.md)
(slices EQ-0, EQ-1, EQ-2).

## Summary

Lifts the remaining half of the 2026-07-20 engine-channels non-goal —
*"No QR/guided auto-provision wizard for engine Slack/Feishu/WeCom in
v1"* — for **Feishu and WeCom**. Slack shipped separately in #3131.

Engine users could already connect both platforms by pasting console
credentials. This drives the same app-registration handshakes the bot
leg uses, so nobody has to open a developer console, create an app, and
copy two secrets by hand. **Manual entry stays** as the fallback — this
is purely additive.

### EQ-0 — generic engine setup-session store (`refactor` commit)

`engine_weixin_session.py` was never a fork of the v1 stores; it is a
claim/lease state machine that exists because the ACS terminal mutation
can span two consecutive 120s timeouts. Rather than grow two more
hand-forked copies of a ~300-line concurrency invariant, its
platform-independent half moves into a generic
`EngineSetupSessionStore[SessionT]`, parameterized by key prefix and
payload dataclass. **Weixin stays the only caller in that commit**, so
the migration is reviewable in isolation.

Behaviour is unchanged by construction: the five Lua scripts, the
`current:` claim key, the 300s lease and the Redis-absent fallback move
verbatim; Redis key prefixes, the logger name and the
`[ENGINE_WEIXIN_SETUP]` log prefix all come out identical, so sessions
in flight across the deploy keep working.

### EQ-1 / EQ-2 — Feishu and WeCom (`feat` commit)

Six routes under the `/agents` group, GET/POST only, gated by
`AGENTS_V2_ENABLED` and workspace-guarded. Setup is a credential
mutation so it requires an `active` workspace; poll and cancel follow
the Weixin precedent.

Both handshake helpers are extracted so the two runtimes share one
implementation — `_feishu_registration` into
`app/services/openclaw/feishu_registration.py`, and the WeCom QR pair
(previously inline in the v1 route) into `wecom_registration.py`. The v1
helpers remain as thin wrappers passing
`client_factory=httpx.AsyncClient`, preserving their existing HTTP patch
seam and the module constants the v1 route tests read.

Three things in the v1 terminal step do **not** carry over: the bot
lookup + `client.add_channel` becomes `_create_channel_acs`;
`enable_skills` drops (engine Weixin does not call it);
`_try_set_channel_bound_agent` drops because engine channels have no
`bound_agent_id`. The config written to ACS is exactly what the manual
engine path already sends today — `{appId, appSecret, domain}` and
`{botId, secret}` — which is the main reason this is low-risk.

Unlike Weixin, the account stays **user-chosen** rather than pinned to
`"default"`: Feishu/WeCom credentials are durable and a workspace may
legitimately hold several. Collisions are refused up front, and one
appearing between setup and the terminal write surfaces as
`channel.conflict` from ACS's 409 — never a silent credential overwrite.

Frontend: both modals take an optional `workspaceId` and branch
start/poll/cancel on it, exactly as `WeixinSetupModal` already does;
without it they keep calling the v1 bot-scoped endpoints. `feishu` and
`wecom` join `ENGINE_GUIDED_PLATFORMS`. The account field stays visible
and editable (Weixin hides it only because its backend pins the
account).

### Note on the merge commit

Main landed the Slack slice as a squash (#3131) while this branch
carried its own copy, so `origin/main` was merged in and six conflicts
resolved toward this branch — main's versions asserted the pre-change
behaviour (engine Feishu/WeCom on bare manual entry) that this PR
deliberately replaces. Both gates were re-run green on the merged tree.

## Test plan

- [x] `bash scripts/verify-py.sh` — ruff, ruff-format, pyright (0
errors), import-linter (8/8 contracts)
- [x] `bash scripts/verify-web.sh` — 7 governance guards, tsc, **7453**
vitest tests, eslint
- [x] Full backend suite incl. BDD, CI-equivalent (`-n 4 --dist
loadfile`, Mongo on `127.0.0.1`) — **7347 passed**, coverage **89.61%**
- [x] jscpd duplication **2.64%** against the 3.0% gate; file-length and
complexity guards clean
- [ ] **Staging smoke (owed before release)** — one engine Feishu QR
provision with a message round-trip, one engine WeCom QR provision. This
also settles open question 1 in the spec: whether ACS accepts the Feishu
`domain` config key on the engine leg. The bot payload includes it, but
the engine manual form collects only `appId`/`appSecret`, so if ACS
rejects unknown keys the guided flow would fail where manual entry
succeeds.

## Review findings — fixed in `0b614239b`

Three P1s, raised independently by local review and the Codex gate, all
the same class: a recoverable condition escalated into a terminal wizard
failure.

1. **Feishu poll treated every exception as terminal.** One
`httpx.ReadTimeout` inside the 10-minute QR window ended the flow.
Timeouts and network errors now return `pending`; anything else stays
terminal.
2. **WeCom poll dropped v1's 429-as-transient handling.**
`wecom_query_result()` raises on any non-2xx, so a single upstream
rate-limit aborted the engine wizard where the bot leg keeps polling — a
regression against shipped behaviour. Mapping extracted to
`_poll_outcome_from_exception`, mirroring v1's helper, including its
rule about never logging the exception (httpx stringifies the URL, which
embeds the one-time `scode`).
3. **Feishu `slow_down` save was unguarded**, so a session-store blip
turned a non-terminal provider hint into a server error. Now
best-effort, consistent with the brand persist above it.

Five tests added, each watched failing first. Two pin the boundary
rather than the fix — an unexpected Feishu exception and a WeCom 500
must still be terminal — so the retry paths cannot quietly widen into
swallowing real errors.

## Known follow-ups

Still open, not fixed here:

1. **The EQ-0 concurrency test does not test concurrency.**
`asyncio.gather` over the Redis-absent path cannot interleave — there is
no `await` between the read and write — so `["binding", "claimed"]`
holds sequentially. The property the spec asked EQ-0 to prove is
currently unproven.
2. No mock-backend handlers for engine Feishu/WeCom, so the documented
`scripts/dev-mock.sh` workflow cannot drive either new flow.
3. `_claim_terminal_write` is duplicated verbatim between the two new
services; it belongs next to its siblings in
`engine_channel_setup_service`.

## Deploy

Backend first, then web.
```

### PR Body

## Linear

No Linear issue — this is spec-driven work. Design of record: [`docs/superpowers/specs/2026-07-29-engine-feishu-wecom-qr-setup.md`](../blob/codex/engine-feishu-wecom-qr/docs/superpowers/specs/2026-07-29-engine-feishu-wecom-qr-setup.md) (slices EQ-0, EQ-1, EQ-2).

## Summary

Lifts the remaining half of the 2026-07-20 engine-channels non-goal — *"No QR/guided auto-provision wizard for engine Slack/Feishu/WeCom in v1"* — for **Feishu and WeCom**. Slack shipped separately in #3131.

Engine users could already connect both platforms by pasting console credentials. This drives the same app-registration handshakes the bot leg uses, so nobody has to open a developer console, create an app, and copy two secrets by hand. **Manual entry stays** as the fallback — this is purely additive.

### EQ-0 — generic engine setup-session store (`refactor` commit)

`engine_weixin_session.py` was never a fork of the v1 stores; it is a claim/lease state machine that exists because the ACS terminal mutation can span two consecutive 120s timeouts. Rather than grow two more hand-forked copies of a ~300-line concurrency invariant, its platform-independent half moves into a generic `EngineSetupSessionStore[SessionT]`, parameterized by key prefix and payload dataclass. **Weixin stays the only caller in that commit**, so the migration is reviewable in isolation.

Behaviour is unchanged by construction: the five Lua scripts, the `current:` claim key, the 300s lease and the Redis-absent fallback move verbatim; Redis key prefixes, the logger name and the `[ENGINE_WEIXIN_SETUP]` log prefix all come out identical, so sessions in flight across the deploy keep working.

### EQ-1 / EQ-2 — Feishu and WeCom (`feat` commit)

Six routes under the `/agents` group, GET/POST only, gated by `AGENTS_V2_ENABLED` and workspace-guarded. Setup is a credential mutation so it requires an `active` workspace; poll and cancel follow the Weixin precedent.

Both handshake helpers are extracted so the two runtimes share one implementation — `_feishu_registration` into `app/services/openclaw/feishu_registration.py`, and the WeCom QR pair (previously inline in the v1 route) into `wecom_registration.py`. The v1 helpers remain as thin wrappers passing `client_factory=httpx.AsyncClient`, preserving their existing HTTP patch seam and the module constants the v1 route tests read.

Three things in the v1 terminal step do **not** carry over: the bot lookup + `client.add_channel` becomes `_create_channel_acs`; `enable_skills` drops (engine Weixin does not call it); `_try_set_channel_bound_agent` drops because engine channels have no `bound_agent_id`. The config written to ACS is exactly what the manual engine path already sends today — `{appId, appSecret, domain}` and `{botId, secret}` — which is the main reason this is low-risk.

Unlike Weixin, the account stays **user-chosen** rather than pinned to `"default"`: Feishu/WeCom credentials are durable and a workspace may legitimately hold several. Collisions are refused up front, and one appearing between setup and the terminal write surfaces as `channel.conflict` from ACS's 409 — never a silent credential overwrite.

Frontend: both modals take an optional `workspaceId` and branch start/poll/cancel on it, exactly as `WeixinSetupModal` already does; without it they keep calling the v1 bot-scoped endpoints. `feishu` and `wecom` join `ENGINE_GUIDED_PLATFORMS`. The account field stays visible and editable (Weixin hides it only because its backend pins the account).

### Note on the merge commit

Main landed the Slack slice as a squash (#3131) while this branch carried its own copy, so `origin/main` was merged in and six conflicts resolved toward this branch — main's versions asserted the pre-change behaviour (engine Feishu/WeCom on bare manual entry) that this PR deliberately replaces. Both gates were re-run green on the merged tree.

## Test plan

- [x] `bash scripts/verify-py.sh` — ruff, ruff-format, pyright (0 errors), import-linter (8/8 contracts)
- [x] `bash scripts/verify-web.sh` — 7 governance guards, tsc, **7453** vitest tests, eslint
- [x] Full backend suite incl. BDD, CI-equivalent (`-n 4 --dist loadfile`, Mongo on `127.0.0.1`) — **7347 passed**, coverage **89.61%**
- [x] jscpd duplication **2.64%** against the 3.0% gate; file-length and complexity guards clean
- [ ] **Staging smoke (owed before release)** — one engine Feishu QR provision with a message round-trip, one engine WeCom QR provision. This also settles open question 1 in the spec: whether ACS accepts the Feishu `domain` config key on the engine leg. The bot payload includes it, but the engine manual form collects only `appId`/`appSecret`, so if ACS rejects unknown keys the guided flow would fail where manual entry succeeds.

## Review findings — fixed in `0b614239b`

Three P1s, raised independently by local review and the Codex gate, all the same class: a recoverable condition escalated into a terminal wizard failure.

1. **Feishu poll treated every exception as terminal.** One `httpx.ReadTimeout` inside the 10-minute QR window ended the flow. Timeouts and network errors now return `pending`; anything else stays terminal.
2. **WeCom poll dropped v1's 429-as-transient handling.** `wecom_query_result()` raises on any non-2xx, so a single upstream rate-limit aborted the engine wizard where the bot leg keeps polling — a regression against shipped behaviour. Mapping extracted to `_poll_outcome_from_exception`, mirroring v1's helper, including its rule about never logging the exception (httpx stringifies the URL, which embeds the one-time `scode`).
3. **Feishu `slow_down` save was unguarded**, so a session-store blip turned a non-terminal provider hint into a server error. Now best-effort, consistent with the brand persist above it.

Five tests added, each watched failing first. Two pin the boundary rather than the fix — an unexpected Feishu exception and a WeCom 500 must still be terminal — so the retry paths cannot quietly widen into swallowing real errors.

## Known follow-ups

Still open, not fixed here:

1. **The EQ-0 concurrency test does not test concurrency.** `asyncio.gather` over the Redis-absent path cannot interleave — there is no `await` between the read and write — so `["binding", "claimed"]` holds sequentially. The property the spec asked EQ-0 to prove is currently unproven.
2. No mock-backend handlers for engine Feishu/WeCom, so the documented `scripts/dev-mock.sh` workflow cannot drive either new flow.
3. `_claim_terminal_write` is duplicated verbatim between the two new services; it belongs next to its siblings in `engine_channel_setup_service`.

## Deploy

Backend first, then web.

