# SerendipityOneInc/ecap-workspace — commits 2026-08-25

## fix(bossclaw): account-status uses active-profile existence, not uid resolution (#3515)

- **SHA**: `4d54b7f48fa168c797d2efcd11b0ec8204260df8`
- **作者**: tim-srp
- **日期**: 2026-08-25T13:14:30Z
- **PR**: #3515

### Commit Message

```
fix(bossclaw): account-status uses active-profile existence, not uid resolution (#3515)

## Summary

Staging test of the merged #3513 exposed a false "unregistered" for a
real user: `18610983415` matched **45** `gem_account` profiles (most
were inactive test rows), and `get_by_phone_number`'s fallback — shared
with KB/Twilio — fails closed on ambiguous matches, so the
account-status endpoint returned `registered: false` for a registered
user.

The account-status endpoint only needs boolean existence (it returns no
uid, and the OTP step binds identity exactly via the account service),
so ambiguity is harmless there:

- `user_repo.has_top_level_phone` — top-level `ecap-account` phone hit
short-circuits.
- `profile_repo.has_active_identifier` — any **`is_active: true`**
`gem_account` profile match. Inactive profiles (test/history rows) are
excluded.
- `routes/bossclaw.py` combines the two; `get_by_phone_number`
(Twilio/KB fail-closed uid resolution) is untouched.

Verified on the staging pod: `is_active` filtering reduces the 45
matches to the single real uid.

Also in this PR (from the same staging round):
- Success copy `正在进入 ZooClaw…` → `正在进入 ZooWork…` (domain migration).
- The two `new URL(x, 'https://zooclaw.ai')` parse bases updated to
`zoowork.ai`.

## Test plan

- Backend: 90 passed (account-status, user_repo, profile_repo,
subscription_code); ruff + pyright 0 errors; user_repo stays under the
500-line guard (491).
- Staging verification: pod-level queries confirmed `is_active: true`
matches the user's own uid.

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

## Summary

Staging test of the merged #3513 exposed a false "unregistered" for a real user: `18610983415` matched **45** `gem_account` profiles (most were inactive test rows), and `get_by_phone_number`'s fallback — shared with KB/Twilio — fails closed on ambiguous matches, so the account-status endpoint returned `registered: false` for a registered user.

The account-status endpoint only needs boolean existence (it returns no uid, and the OTP step binds identity exactly via the account service), so ambiguity is harmless there:

- `user_repo.has_top_level_phone` — top-level `ecap-account` phone hit short-circuits.
- `profile_repo.has_active_identifier` — any **`is_active: true`** `gem_account` profile match. Inactive profiles (test/history rows) are excluded.
- `routes/bossclaw.py` combines the two; `get_by_phone_number` (Twilio/KB fail-closed uid resolution) is untouched.

Verified on the staging pod: `is_active` filtering reduces the 45 matches to the single real uid.

Also in this PR (from the same staging round):
- Success copy `正在进入 ZooClaw…` → `正在进入 ZooWork…` (domain migration).
- The two `new URL(x, 'https://zooclaw.ai')` parse bases updated to `zoowork.ai`.

## Test plan

- Backend: 90 passed (account-status, user_repo, profile_repo, subscription_code); ruff + pyright 0 errors; user_repo stays under the 500-line guard (491).
- Staging verification: pod-level queries confirmed `is_active: true` matches the user's own uid.


---

## feat(bossclaw): migrate new-user flow to V2 engine install & workspace channels (#3501)

- **SHA**: `1c255b4c081d15ce106a526c754a56992b9d89a3`
- **作者**: tim-srp
- **日期**: 2026-08-25T13:06:15Z
- **PR**: #3501

### Commit Message

```
feat(bossclaw): migrate new-user flow to V2 engine install & workspace channels (#3501)

## Summary
- Agent install: V1 computer 流程（/computers + redeploy）替换为 V2 pack
安装（install-capability → pack_id 恢复 → /api/agents/install → wait active →
start → workspace_id）
- 渠道绑定: V1 bot API（uid+agent_id+account）替换为 workspace V2
API（/agents/{workspace_id}/channels/{platform}/setup|poll|cancel），sessionStorage
key 含 workspace_id，刷新按 pack_id 找回
- 配置: NEXT_PUBLIC_BOSSCLAW_AGENT_ID 退役，新增
NEXT_PUBLIC_BOSSCLAW_PACK_ID（.env.example + deploy.yml）
- 文案: 删除 waiting-bot/V1 pod 文案，完成页按实际渠道显示
- 失败不回退 V1（capability 非 engine 直接报错）

## Test plan
- [x] pnpm exec vitest run tests/unit/bossclaw/（68 cases）
- [x] bash scripts/verify-web.sh（tsc + vitest + eslint）

---------

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

## Summary
- Agent install: V1 computer 流程（/computers + redeploy）替换为 V2 pack 安装（install-capability → pack_id 恢复 → /api/agents/install → wait active → start → workspace_id）
- 渠道绑定: V1 bot API（uid+agent_id+account）替换为 workspace V2 API（/agents/{workspace_id}/channels/{platform}/setup|poll|cancel），sessionStorage key 含 workspace_id，刷新按 pack_id 找回
- 配置: NEXT_PUBLIC_BOSSCLAW_AGENT_ID 退役，新增 NEXT_PUBLIC_BOSSCLAW_PACK_ID（.env.example + deploy.yml）
- 文案: 删除 waiting-bot/V1 pod 文案，完成页按实际渠道显示
- 失败不回退 V1（capability 非 engine 直接报错）

## Test plan
- [x] pnpm exec vitest run tests/unit/bossclaw/（68 cases）
- [x] bash scripts/verify-web.sh（tsc + vitest + eslint）


---

## feat(bossclaw): add invite-gated registration flow (#3513)

- **SHA**: `1a1a610960b7b4b5cd7c3834d18a83270df510b8`
- **作者**: tim-srp
- **日期**: 2026-08-25T12:31:41Z
- **PR**: #3513

### Commit Message

```
feat(bossclaw): add invite-gated registration flow (#3513)

## Summary

Implement invite-gated registration for BossClaw (design:
`docs/superpowers/specs/2026-08-25-bossclaw-invite-registration-design.md`):
existing ZooClaw accounts can sign in with email/phone OTP, while new
users must first validate an invitation code.

**Backend (`services/claw-interface`)**
- `subscription_code.py` — extract shared subscription-code validation
(`_assert_code_redeemable` / `check_subscription_code_usable`) reused by
the new read-only `POST /api/subscription-code/validate` endpoint
(request/response Pydantic schemas).
- `user_repo.py` — add `get_by_email` (normalized) and
`get_by_phone_number` lookups with a `gem_account` (profile store)
fallback when the `ecap-account` doc lacks top-level contact fields
(mirrors `knowledge_base._resolve_grantee_uid`: ambiguous or failing
lookups return `None`, never an arbitrary match). Adds non-unique
identifier indexes (log-only) plus
`profile_repo.find_uid_by_identifier`.
- `bossclaw.py` — new public `POST /api/bossclaw/account-status`
endpoint returning `{registered}` for email/phone identifiers (E.164
phone validation).

**Frontend (`web/app`)**
- `middleware.ts` — public-route allowlist for the two new endpoints.
- `services/boss.ts` — `checkBossclawAccountStatus` /
`validateSubscriptionCode` with fail-closed error mapping
(`SubscriptionCodeError`).
- `auth/manager.ts` — `loginExistingWithEmailOTP` plus a named
`loginWithSmsOTP` re-export for the login flow.
- `useBossclawLoginFlow` — four-step state machine hook (identifier →
invitation → verification → success) driving the render-only
`BossclawLoginClient` (4 screens).

## Test plan

- Backend: `env NODE_OPTIONS= bash scripts/verify-py.sh` — ruff +
pyright + import-linter 8/8 KEPT; branch test files 156 passed
(subscription_code, routes, bossclaw account-status, user_repo,
profile_repo, main_app).
- Frontend: `env NODE_OPTIONS= bash scripts/verify-web.sh` — full-app
tsc + vitest 9207 passed | 70 skipped | 1 todo + eslint clean.
- Manual: fresh phone/email → invitation-code gate; existing account
(incl. warm-pool-claimed, contact only in profile store) → OTP sign-in
with `registered: true`.

---------

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

## Summary

Implement invite-gated registration for BossClaw (design: `docs/superpowers/specs/2026-08-25-bossclaw-invite-registration-design.md`): existing ZooClaw accounts can sign in with email/phone OTP, while new users must first validate an invitation code.

**Backend (`services/claw-interface`)**
- `subscription_code.py` — extract shared subscription-code validation (`_assert_code_redeemable` / `check_subscription_code_usable`) reused by the new read-only `POST /api/subscription-code/validate` endpoint (request/response Pydantic schemas).
- `user_repo.py` — add `get_by_email` (normalized) and `get_by_phone_number` lookups with a `gem_account` (profile store) fallback when the `ecap-account` doc lacks top-level contact fields (mirrors `knowledge_base._resolve_grantee_uid`: ambiguous or failing lookups return `None`, never an arbitrary match). Adds non-unique identifier indexes (log-only) plus `profile_repo.find_uid_by_identifier`.
- `bossclaw.py` — new public `POST /api/bossclaw/account-status` endpoint returning `{registered}` for email/phone identifiers (E.164 phone validation).

**Frontend (`web/app`)**
- `middleware.ts` — public-route allowlist for the two new endpoints.
- `services/boss.ts` — `checkBossclawAccountStatus` / `validateSubscriptionCode` with fail-closed error mapping (`SubscriptionCodeError`).
- `auth/manager.ts` — `loginExistingWithEmailOTP` plus a named `loginWithSmsOTP` re-export for the login flow.
- `useBossclawLoginFlow` — four-step state machine hook (identifier → invitation → verification → success) driving the render-only `BossclawLoginClient` (4 screens).

## Test plan

- Backend: `env NODE_OPTIONS= bash scripts/verify-py.sh` — ruff + pyright + import-linter 8/8 KEPT; branch test files 156 passed (subscription_code, routes, bossclaw account-status, user_repo, profile_repo, main_app).
- Frontend: `env NODE_OPTIONS= bash scripts/verify-web.sh` — full-app tsc + vitest 9207 passed | 70 skipped | 1 todo + eslint clean.
- Manual: fresh phone/email → invitation-code gate; existing account (incl. warm-pool-claimed, contact only in profile store) → OTP sign-in with `registered: true`.


---

## chore(billing): clean retired Creem references (#3514)

- **SHA**: `5c782160a03657ac7cc3edda436e899f87d453d9`
- **作者**: tim-srp
- **日期**: 2026-08-25T12:30:25Z
- **PR**: #3514

### Commit Message

```
chore(billing): clean retired Creem references (#3514)

## Summary

Final sweep of retired Creem references after the cleanup series (#3460
→ #3485):

- remove stale Creem module paths from `.jscpd.src.json` ignore config —
the modules were deleted across the series, so the exclude entries are
dead config
- replace provider-specific `CREEM_PROVIDER_CANCELED` cron label with
provider-neutral `PROVIDER_CANCELED` in `test_subscription_expiry.py` —
the label is a log-only argument, no behavioral impact

## Verification

- [x] `bash scripts/verify-py.sh` — ruff, ruff-format, pyright,
import-linter all passed
- [x] pre-commit and pre-push changed-surface gates passed

## Risk

None. Test label change is behavior-neutral; jscpd config removal only
drops paths that no longer exist. Intentionally kept (not part of this
PR): negative contract tests asserting Creem is rejected, the retired
webhook 404 passthrough in `web/app/src/middleware.ts`, and the legacy
index migration constant in `subscription_agreement_indexes.py`.

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

## Summary

Final sweep of retired Creem references after the cleanup series (#3460 → #3485):

- remove stale Creem module paths from `.jscpd.src.json` ignore config — the modules were deleted across the series, so the exclude entries are dead config
- replace provider-specific `CREEM_PROVIDER_CANCELED` cron label with provider-neutral `PROVIDER_CANCELED` in `test_subscription_expiry.py` — the label is a log-only argument, no behavioral impact

## Verification

- [x] `bash scripts/verify-py.sh` — ruff, ruff-format, pyright, import-linter all passed
- [x] pre-commit and pre-push changed-surface gates passed

## Risk

None. Test label change is behavior-neutral; jscpd config removal only drops paths that no longer exist. Intentionally kept (not part of this PR): negative contract tests asserting Creem is rejected, the retired webhook 404 passthrough in `web/app/src/middleware.ts`, and the legacy index migration constant in `subscription_agreement_indexes.py`.


---

## fix(agent-builder): load v2 model before first project (#3500)

- **SHA**: `5b29dde3ec5f408600db9438260b9ae37fce540c`
- **作者**: rayrain-srp
- **日期**: 2026-08-25T11:31:32Z
- **PR**: #3500

### Commit Message

```
fix(agent-builder): load v2 model before first project (#3500)

## Summary
- expose an authenticated V2 new-project model state using the same
active Pack and Engine catalog resolution as Agent installation
- load that state on an empty Agent Builder home, allow an entitled
model to be selected, and pass it through draft initialization before
the first turn
- fail closed while Builder model state is loading or unavailable
instead of presenting the generic Chat default as the applied model

Fixes [ECA-1396](https://linear.app/srpone/issue/ECA-1396).

## Root cause
When `projects=[]`, the home model query had no Project identity and
stayed disabled. The create dialog then rendered the generic Chat
catalog default, while project creation submitted no model. The
dedicated Engine Agent therefore used its independent Pack/Engine
install default, so the displayed model and actual runtime model could
diverge.

## Test plan
- [x] `pytest tests/unit/test_agent_builder_model_service.py
tests/unit/test_agent_builder_routes.py
tests/unit/test_agent_builder_v2_runtime_service.py -q` (87 passed)
- [x] `pytest tests/unit/test_agent_builder_runtime_services.py -q` (29
passed)
- [x] targeted Vitest coverage for the create dialog, empty-home flow,
V2 client, and mock backend (118 passed)
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh --no-test <changed web/app paths>`
- [x] pre-push PR-size and `bash scripts/verify-changed.sh` gates
```

### PR Body

## Summary
- expose an authenticated V2 new-project model state using the same active Pack and Engine catalog resolution as Agent installation
- load that state on an empty Agent Builder home, allow an entitled model to be selected, and pass it through draft initialization before the first turn
- fail closed while Builder model state is loading or unavailable instead of presenting the generic Chat default as the applied model

Fixes [ECA-1396](https://linear.app/srpone/issue/ECA-1396).

## Root cause
When `projects=[]`, the home model query had no Project identity and stayed disabled. The create dialog then rendered the generic Chat catalog default, while project creation submitted no model. The dedicated Engine Agent therefore used its independent Pack/Engine install default, so the displayed model and actual runtime model could diverge.

## Test plan
- [x] `pytest tests/unit/test_agent_builder_model_service.py tests/unit/test_agent_builder_routes.py tests/unit/test_agent_builder_v2_runtime_service.py -q` (87 passed)
- [x] `pytest tests/unit/test_agent_builder_runtime_services.py -q` (29 passed)
- [x] targeted Vitest coverage for the create dialog, empty-home flow, V2 client, and mock backend (118 passed)
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh --no-test <changed web/app paths>`
- [x] pre-push PR-size and `bash scripts/verify-changed.sh` gates


---

## feat(claw-interface): wecom/weixin guided channel setup for service-API agents (#3512)

- **SHA**: `790e9816918822ae4304d26d6cc7c1f63c921a45`
- **作者**: finn-srp
- **日期**: 2026-08-25T11:31:28Z
- **PR**: #3512

### Commit Message

```
feat(claw-interface): wecom/weixin guided channel setup for service-API agents (#3512)

## Linear
<!-- 待补：如有对应 issue，贴完整 Linear URL -->

## Summary

PR #3502 shipped channel binding for service-API agents with **Feishu
only** — the wecom/weixin
guided flows were an explicit v1 non-goal, and slack was untested. The
product ask was always the
**channel** capability, not one platform. This PR finishes it: every
platform the web surface can
bind, a service-token caller can bind.

The four platforms turned out to have three different server-side
shapes, so "finish it" meant less
code than it sounds:

| platform | shape | work here |
|---|---|---|
| feishu | QR device flow | none — shipped in #3502, regression-tested |
| wecom | server-driven QR (`wecom_registration`) | migrate to target +
3 routes |
| weixin | server-driven QR (`weixin_gateway`, own claim/redirect state
machine) | migrate to target + 3 routes |
| slack | **no server-side flow at all** | none — already worked;
contract documented + pinned |

**wecom/weixin migration.** Both services were the last things in their
chains still resolving a
Mongo `AgentWorkspace` themselves — which is exactly why service-API
agents (no workspace document)
couldn't reach them. Their six public functions now take the same
`EngineChannelTarget` the shared
setup layer already speaks; the ownership gate moved up into the web
route handlers, preserving the
`require_active` value each service used internally (setup `True`,
poll/cancel `False` — the
no-behavior-change contract, now pinned for **all thirteen routes** by
one shared table in
`test_agents_v2_channels_routes.py`). `_configure_*`'s duplicate
`workspace_id`+`target` parameters
were collapsed across feishu/wecom/weixin, and `get_channel_workspace`
lost its silent
`require_active=True` default — the type checker now forces every caller
to state it.

weixin deliberately stays off the shared `engine_channel_setup_service`:
its policy set
(`open`/`disabled` only, own `allowlist_unsupported` error, no group
policy) doesn't fit the shared
contract. The spec bounds that exemption precisely so it can't be cited
to keep future platforms'
session plumbing private.

**Service-API routes.** `_channels.py` gains
`_handle_wecom`/`_handle_weixin` and dispatches guided
platforms through a `_GUIDED_HANDLERS` table (the branch-chain shape
would hit ruff `PLR0911` at
platform six). The byte-identical poll/cancel legs are shared via
`_handle_session_actions`; each
platform keeps its own setup leg, where the real differences live
(feishu's `brand`, wecom's account
validation, weixin's deliberately absent `_require_account_id` —
`EngineWeixinSetupRequest` carries
no account; the service pins it to `default`). Platform actions still
match before guided handlers,
so `weixin/update`/`weixin/remove` keep reaching the generic handler —
pinned, since these two
worked since #3502 with zero coverage.

**Slack + contract documentation.** Verified on deployed staging: `POST
/channels` with
`{"platform":"slack","config":{botToken,appToken}}` → 201, config passed
to ACS untouched; ACS
does not validate credential format (fake tokens → 201, then `health:
unhealthy`). Also measured
the ACS idempotency semantics (key `{scope}:{platform}:{account}`):
identical body replays 201,
same account with different config → 409 `channel.conflict`,
**credential rotation is
remove-then-add**. All of it now lives in the `_channels.py` module
docstring — these routes sit
under the `include_in_schema=False` catch-all, so that docstring is the
only machine-adjacent API
reference, and it now carries the per-platform QR shapes (feishu: URL to
encode + `poll_interval`;
wecom: URL, no interval; weixin: URL *or* inline `data:image/`) and
config keys.

**Product decisions taken for this change** (recorded in the spec so the
asymmetries read as
decisions, not oversights): no `require_agents_v2` on the service API,
and no active-agent
precondition — both match the Feishu precedent from #3502. Consequence
worth knowing: binding
slack to a stopped agent is 409 on the web surface and 201 on the
service API, by design.

Spec:
`docs/superpowers/specs/2026-08-25-service-api-all-channel-platforms.md`
— supersedes the
v1 non-goals of the 2026-08-24 spec (pointer added there) and corrects
its stale rate-limiting
claim; also fixes the 2026-07-29 spec's now-false "wecom is structured
like weixin" passage.

## Test plan

- [x] Full unit suite green: 9224 passed, 5 skipped; ruff, ruff format,
pyright, import-linter
      (8 contracts) all clean.
- [x] The six channel test files: 206 passed. New coverage: wecom/weixin
setup/poll/cancel through
the real FastAPI app on both surfaces; the 13-route `require_active`
table (the single most
likely silent regression, previously zero route-level coverage);
dispatch-ordering pins for
`weixin|wecom / update|remove`; slack config passthrough; weixin setup
must NOT validate an
account it doesn't carry; cross-org tenant-hiding 404; session-id and
wrong-method guards for
every guided platform (parametrized — feishu gained the two cases it was
missing).
- [x] Mutation-tested the new pins: flipping a `require_active` boolean,
passing a wrong target to
the ACS write, and deleting the session scope check each fail exactly
the intended test.
- [x] Unfalsifiable assertions replaced: the wecom suite's
`get_channel_workspace.assert_not_awaited()`
guards could never fail after the import was removed — now a static
`assert not hasattr(module, "engine_agent_channels_service")` that bites
if the Mongo
      fallback ever returns.
- [x] Staging, end to end against a local claw-interface on the real
staging stack (Mongo/engine/ACS
via port-forward): **weixin full QR bind with a real phone scan** —
session expiry, re-scan,
and the cross-agent `(owner, platform, account)` 409 all exercised on
the way; channel landed
`healthy/running`, then `weixin/update` (dm_policy flip and back)
through the generic handler.
Feishu setup/poll/cancel as regression. wecom setup → QR issued → poll
pending → cancel →
session gone (no real WeCom scan — deliberately skipped, same shared
code path weixin proved).
Slack add/remove/re-add measured on deployed staging. Negative sweep:
weixin generic add 400,
`pairing`/`allowlist` 400, missing session_id 400, wrong method 404,
unknown platform 404,
      foreign-org agent 404.

## Known follow-ups (deliberately out of scope)

1. **Cross-agent weixin conflict surfaces after the scan.** ACS's
`(owner, platform, account)`
uniqueness is owner-wide and weixin's account is pinned `default`, but
the pre-QR availability
check is per-agent — so a second agent's bind fails only at the
post-scan ACS write, with a 409
that doesn't name the occupying agent. Pre-existing, both surfaces
behave identically; hit for
   real during staging validation.
2. **Declarative routes / OpenAPI** for the `/service/v1` channels
family — unchanged from #3502.
3. **weixin session plumbing** duplicates the shared setup helpers for
no policy reason (only a
   user-visible wording change blocks adoption); bounded in the spec.
4. The engine channel routes have **no rate limiting** on either
surface; the 2026-08-24 spec
claimed otherwise and has been corrected. Legacy FastClaw routes keep
theirs.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: wangfulong <wfllike@gmail.com>
Co-authored-by: Claude Opus 5 <noreply@anthropic.com>
```

### PR Body

## Linear
<!-- 待补：如有对应 issue，贴完整 Linear URL -->

## Summary

PR #3502 shipped channel binding for service-API agents with **Feishu only** — the wecom/weixin
guided flows were an explicit v1 non-goal, and slack was untested. The product ask was always the
**channel** capability, not one platform. This PR finishes it: every platform the web surface can
bind, a service-token caller can bind.

The four platforms turned out to have three different server-side shapes, so "finish it" meant less
code than it sounds:

| platform | shape | work here |
|---|---|---|
| feishu | QR device flow | none — shipped in #3502, regression-tested |
| wecom | server-driven QR (`wecom_registration`) | migrate to target + 3 routes |
| weixin | server-driven QR (`weixin_gateway`, own claim/redirect state machine) | migrate to target + 3 routes |
| slack | **no server-side flow at all** | none — already worked; contract documented + pinned |

**wecom/weixin migration.** Both services were the last things in their chains still resolving a
Mongo `AgentWorkspace` themselves — which is exactly why service-API agents (no workspace document)
couldn't reach them. Their six public functions now take the same `EngineChannelTarget` the shared
setup layer already speaks; the ownership gate moved up into the web route handlers, preserving the
`require_active` value each service used internally (setup `True`, poll/cancel `False` — the
no-behavior-change contract, now pinned for **all thirteen routes** by one shared table in
`test_agents_v2_channels_routes.py`). `_configure_*`'s duplicate `workspace_id`+`target` parameters
were collapsed across feishu/wecom/weixin, and `get_channel_workspace` lost its silent
`require_active=True` default — the type checker now forces every caller to state it.

weixin deliberately stays off the shared `engine_channel_setup_service`: its policy set
(`open`/`disabled` only, own `allowlist_unsupported` error, no group policy) doesn't fit the shared
contract. The spec bounds that exemption precisely so it can't be cited to keep future platforms'
session plumbing private.

**Service-API routes.** `_channels.py` gains `_handle_wecom`/`_handle_weixin` and dispatches guided
platforms through a `_GUIDED_HANDLERS` table (the branch-chain shape would hit ruff `PLR0911` at
platform six). The byte-identical poll/cancel legs are shared via `_handle_session_actions`; each
platform keeps its own setup leg, where the real differences live (feishu's `brand`, wecom's account
validation, weixin's deliberately absent `_require_account_id` — `EngineWeixinSetupRequest` carries
no account; the service pins it to `default`). Platform actions still match before guided handlers,
so `weixin/update`/`weixin/remove` keep reaching the generic handler — pinned, since these two
worked since #3502 with zero coverage.

**Slack + contract documentation.** Verified on deployed staging: `POST /channels` with
`{"platform":"slack","config":{botToken,appToken}}` → 201, config passed to ACS untouched; ACS
does not validate credential format (fake tokens → 201, then `health: unhealthy`). Also measured
the ACS idempotency semantics (key `{scope}:{platform}:{account}`): identical body replays 201,
same account with different config → 409 `channel.conflict`, **credential rotation is
remove-then-add**. All of it now lives in the `_channels.py` module docstring — these routes sit
under the `include_in_schema=False` catch-all, so that docstring is the only machine-adjacent API
reference, and it now carries the per-platform QR shapes (feishu: URL to encode + `poll_interval`;
wecom: URL, no interval; weixin: URL *or* inline `data:image/`) and config keys.

**Product decisions taken for this change** (recorded in the spec so the asymmetries read as
decisions, not oversights): no `require_agents_v2` on the service API, and no active-agent
precondition — both match the Feishu precedent from #3502. Consequence worth knowing: binding
slack to a stopped agent is 409 on the web surface and 201 on the service API, by design.

Spec: `docs/superpowers/specs/2026-08-25-service-api-all-channel-platforms.md` — supersedes the
v1 non-goals of the 2026-08-24 spec (pointer added there) and corrects its stale rate-limiting
claim; also fixes the 2026-07-29 spec's now-false "wecom is structured like weixin" passage.

## Test plan

- [x] Full unit suite green: 9224 passed, 5 skipped; ruff, ruff format, pyright, import-linter
      (8 contracts) all clean.
- [x] The six channel test files: 206 passed. New coverage: wecom/weixin setup/poll/cancel through
      the real FastAPI app on both surfaces; the 13-route `require_active` table (the single most
      likely silent regression, previously zero route-level coverage); dispatch-ordering pins for
      `weixin|wecom / update|remove`; slack config passthrough; weixin setup must NOT validate an
      account it doesn't carry; cross-org tenant-hiding 404; session-id and wrong-method guards for
      every guided platform (parametrized — feishu gained the two cases it was missing).
- [x] Mutation-tested the new pins: flipping a `require_active` boolean, passing a wrong target to
      the ACS write, and deleting the session scope check each fail exactly the intended test.
- [x] Unfalsifiable assertions replaced: the wecom suite's `get_channel_workspace.assert_not_awaited()`
      guards could never fail after the import was removed — now a static
      `assert not hasattr(module, "engine_agent_channels_service")` that bites if the Mongo
      fallback ever returns.
- [x] Staging, end to end against a local claw-interface on the real staging stack (Mongo/engine/ACS
      via port-forward): **weixin full QR bind with a real phone scan** — session expiry, re-scan,
      and the cross-agent `(owner, platform, account)` 409 all exercised on the way; channel landed
      `healthy/running`, then `weixin/update` (dm_policy flip and back) through the generic handler.
      Feishu setup/poll/cancel as regression. wecom setup → QR issued → poll pending → cancel →
      session gone (no real WeCom scan — deliberately skipped, same shared code path weixin proved).
      Slack add/remove/re-add measured on deployed staging. Negative sweep: weixin generic add 400,
      `pairing`/`allowlist` 400, missing session_id 400, wrong method 404, unknown platform 404,
      foreign-org agent 404.

## Known follow-ups (deliberately out of scope)

1. **Cross-agent weixin conflict surfaces after the scan.** ACS's `(owner, platform, account)`
   uniqueness is owner-wide and weixin's account is pinned `default`, but the pre-QR availability
   check is per-agent — so a second agent's bind fails only at the post-scan ACS write, with a 409
   that doesn't name the occupying agent. Pre-existing, both surfaces behave identically; hit for
   real during staging validation.
2. **Declarative routes / OpenAPI** for the `/service/v1` channels family — unchanged from #3502.
3. **weixin session plumbing** duplicates the shared setup helpers for no policy reason (only a
   user-visible wording change blocks adoption); bounded in the spec.
4. The engine channel routes have **no rate limiting** on either surface; the 2026-08-24 spec
   claimed otherwise and has been corrected. Legacy FastClaw routes keep theirs.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(enterprise-admin): add resend for pending invitation emails (#3509)

- **SHA**: `4f978865f235ff92e380dd1107ec73be539f2220`
- **作者**: bill-srp
- **日期**: 2026-08-25T09:49:58Z
- **PR**: #3509

### Commit Message

```
feat(enterprise-admin): add resend for pending invitation emails (#3509)

## Linear
https://linear.app/srpone/issue/ECA-1399

## Summary
Admins can now re-send the invitation email for a still-pending invite
from the enterprise-admin Members page. Pending rows previously had no
row action at all (`UserActions` bailed out on `uid === null`), so a
lost or expired-inbox email left the admin with no recourse short of
revoking and re-inviting.

**Backend (`claw-interface`)**
- New `POST /orgs/{org_id}/invites/resend` (`require_org_admin`), body
`{ "email" }` — keyed by email because `GET /orgs/{org_id}/users` never
exposes invite codes. Returns the `OrgInvite`.
- `invite_service.resend_invite`: looks up the pending (active,
unredeemed, unexpired) invite for the org + email → 404
`org_invite.not_found` otherwise; refreshes `expires_at` to a fresh
30-day TTL via a CAS update gated on `used_by IS NULL AND is_active`
(409 `org_invite.already_used` on a concurrent redeem/revoke). The
**code is kept**, so links in earlier emails stay valid. Error context
carries only `org_id` (no email PII).
- `org_invite_repo`: `get_pending_for_org_and_email` + `extend_expiry`.
- Route schedules `send_invite_email` via `BackgroundTasks` exactly like
the create path, using `admin.org.name` (no extra org lookup).
- `ORG_INVITE_TTL_SECONDS` moved from `membership_service` into
`schema/org_invite.py` so both callers share it.

**Frontend (`web/enterprise-admin`)**
- `useResendInviteMutation` (`hooks/useUsers.ts`) → invalidates
`["users", orgId]`.
- `UserActions` renders a **Resend invite** chip for pending rows
(disabled + "Sending…" while in flight); threaded through `UserTable →
page.tsx → useUsersViewModel` (MVVM: handler, toast, in-flight email,
and error/dismiss state live in the VM).
- zh strings: `users.resendInvite`, `toast.inviteResent`.

## Test plan
- [x] Backend: `pytest
tests/unit/test_org_invite_{schema,repo,service}.py
tests/unit/test_routes_org_users.py
tests/unit/test_membership_service.py
tests/unit/test_routes_org_invites.py tests/unit/test_invite_email.py` —
138 passed (new: schema normalization/extra-forbid, repo filter shapes +
CAS miss, service not-found / refresh / conflict, route POST + admin
guard + one scheduled email + no email on 404)
- [x] `bash scripts/verify-py.sh` — ruff, ruff-format, import-linter
green; pyright reports 4 pre-existing `fastapi.routing.RouteContext`
errors in untouched test helpers (host venv FastAPI version drift; CI's
pinned FastAPI has the symbol)
- [x] `web/enterprise-admin`: `pnpm test` 421/421, `pnpm exec tsc
--noEmit` clean, `pnpm lint` (`--max-warnings=0`) clean
- [ ] Staging smoke after backend + web release: invite a fresh email →
Members page shows the pending row with **Resend invite** → click →
toast "Invitation resent." and a second EngageLab email arrives with the
same link; row disappears after the invitee joins

## Deployment
Cross-surface: backend (`claw-interface`) must ship before or with the
web release — the button 404s against an old backend.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Body

## Linear
https://linear.app/srpone/issue/ECA-1399

## Summary
Admins can now re-send the invitation email for a still-pending invite from the enterprise-admin Members page. Pending rows previously had no row action at all (`UserActions` bailed out on `uid === null`), so a lost or expired-inbox email left the admin with no recourse short of revoking and re-inviting.

**Backend (`claw-interface`)**
- New `POST /orgs/{org_id}/invites/resend` (`require_org_admin`), body `{ "email" }` — keyed by email because `GET /orgs/{org_id}/users` never exposes invite codes. Returns the `OrgInvite`.
- `invite_service.resend_invite`: looks up the pending (active, unredeemed, unexpired) invite for the org + email → 404 `org_invite.not_found` otherwise; refreshes `expires_at` to a fresh 30-day TTL via a CAS update gated on `used_by IS NULL AND is_active` (409 `org_invite.already_used` on a concurrent redeem/revoke). The **code is kept**, so links in earlier emails stay valid. Error context carries only `org_id` (no email PII).
- `org_invite_repo`: `get_pending_for_org_and_email` + `extend_expiry`.
- Route schedules `send_invite_email` via `BackgroundTasks` exactly like the create path, using `admin.org.name` (no extra org lookup).
- `ORG_INVITE_TTL_SECONDS` moved from `membership_service` into `schema/org_invite.py` so both callers share it.

**Frontend (`web/enterprise-admin`)**
- `useResendInviteMutation` (`hooks/useUsers.ts`) → invalidates `["users", orgId]`.
- `UserActions` renders a **Resend invite** chip for pending rows (disabled + "Sending…" while in flight); threaded through `UserTable → page.tsx → useUsersViewModel` (MVVM: handler, toast, in-flight email, and error/dismiss state live in the VM).
- zh strings: `users.resendInvite`, `toast.inviteResent`.

## Test plan
- [x] Backend: `pytest tests/unit/test_org_invite_{schema,repo,service}.py tests/unit/test_routes_org_users.py tests/unit/test_membership_service.py tests/unit/test_routes_org_invites.py tests/unit/test_invite_email.py` — 138 passed (new: schema normalization/extra-forbid, repo filter shapes + CAS miss, service not-found / refresh / conflict, route POST + admin guard + one scheduled email + no email on 404)
- [x] `bash scripts/verify-py.sh` — ruff, ruff-format, import-linter green; pyright reports 4 pre-existing `fastapi.routing.RouteContext` errors in untouched test helpers (host venv FastAPI version drift; CI's pinned FastAPI has the symbol)
- [x] `web/enterprise-admin`: `pnpm test` 421/421, `pnpm exec tsc --noEmit` clean, `pnpm lint` (`--max-warnings=0`) clean
- [ ] Staging smoke after backend + web release: invite a fresh email → Members page shows the pending row with **Resend invite** → click → toast "Invitation resent." and a second EngageLab email arrives with the same link; row disappears after the invitee joins

## Deployment
Cross-surface: backend (`claw-interface`) must ship before or with the web release — the button 404s against an old backend.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(theme): make Paper Focus the primary skin (#3507)

- **SHA**: `978d1a6fa8fe076857fc996c4dd36c070dca03a5`
- **作者**: shana-srp
- **日期**: 2026-08-25T07:59:19Z
- **PR**: #3507

### Commit Message

```
feat(theme): make Paper Focus the primary skin (#3507)

## Linear

N/A — no linked Linear issue was provided.

## Summary

- make Paper Focus the default primary skin and reset target for
Appearance Light
- expose the former `panda-claw` treatment as the optional Pure Glass
skin, with clean white neutral styling and no duplicate Paper Focus card
- align the Paper Focus desktop sidebar to 260px and cover bootstrap,
persistence, provider, asset, and selector behavior with focused tests

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] `bash scripts/verify-web.sh --no-test <changed TypeScript files>`
- [x] focused Vitest suite: 5 files, 87 tests passed
- [x] `git diff --check origin/main...HEAD`

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Linear

N/A — no linked Linear issue was provided.

## Summary

- make Paper Focus the default primary skin and reset target for Appearance Light
- expose the former `panda-claw` treatment as the optional Pure Glass skin, with clean white neutral styling and no duplicate Paper Focus card
- align the Paper Focus desktop sidebar to 260px and cover bootstrap, persistence, provider, asset, and selector behavior with focused tests

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] `bash scripts/verify-web.sh --no-test <changed TypeScript files>`
- [x] focused Vitest suite: 5 files, 87 tests passed
- [x] `git diff --check origin/main...HEAD`


---

## fix(deps): resolve dependabot alerts across services, desktop (55/73) (#3498)

- **SHA**: `3e54a5678befc6be3a6bf80b89dad2121f3b38c9`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-25T04:33:36Z
- **PR**: #3498

### Commit Message

```
fix(deps): resolve dependabot alerts across services, desktop (55/73) (#3498)

## 内容

处理 services / desktop / ios 的 73 条 open Dependabot 告警：**修复 58 条，dismiss
2 条，litellm 13 条转 ECA-1397**（codex-coder 实现、Claude review）。

### claw-interface（Python）⚠️ 含框架迁移，重点 review
- `starlette` 0.52.1 → **1.3.1**（安全补丁在 1.x 线）、`fastapi` <0.137 →
**0.139.2**。
- 这解除了 requirements 里原有的注释 pin——注释本身写明"等迁移到 Starlette 1.x lifespan API
时一起解除"，本 PR 完成了该迁移：`app/lifetime.py` 从
`add_event_handler("startup"/"shutdown")` 改为 `@asynccontextmanager
lifespan`（`finally` 保证 shutdown），`create_app` 经构造参数传入；路由测试适配
`tests/unit/_route_helpers.py`。
- 验证：独立 uv 环境 150 包解析一致；`bash scripts/verify-py.sh` 全过；相关路由单测通过。CI 全量
pytest 是最终把关。

### Node 服务
- whatsapp-business-service：`vitest` 1.x → 3.2.7，刷新 vite / esbuild /
postcss / fast-uri / find-my-way（42 tests + typecheck + build 通过）
- r2-access-worker / oauth-worker：`vitest` 3.2.7、`wrangler` 4.125.0，刷新
undici / sharp / ws 等（39 + 17 tests 通过）；oauth-worker 补建独立
`pnpm-lock.yaml`
- desktop：`electron-builder` → 26.15.3（未跨 major），刷新 app-builder-lib /
builder-util-runtime / tar / undici / js-yaml / form-data 等（typecheck
通过）
- 各目录 `pnpm install --frozen-lockfile` 均通过

### iOS（后续 commit 补充）
- `jwt` → 2.10.3、`json` → 2.19.9、`faraday` → 1.10.6：三者均在 fastlane
既有约束范围内，直接更新 lockfile（specs + CHECKSUMS，sha256 取自 rubygems API），由
ios-quality CI 的 bundle install 验证。

### 后续 commit：FastAPI 0.137+ 路由测试补迁
- codex 首轮漏迁 3 个路由契约测试（`include_router` 变懒挂载后 `router.routes`
不再展开子路由），已迁到 `api_routes` helper；本地全量 unit 套件 9082 passed。

### 未在本 PR 解决
1. **litellm 13 条（含 3 critical）**：被 `favie-common v0.3.69` 的
OpenTelemetry 1.25.0 pin 阻塞（importlib-metadata 冲突），跟踪
issue：[ECA-1397](https://linear.app/srpone/issue/ECA-1397)。
2. **excon 1 条**：补丁 1.5.0 超出 fastlane `< 1.0.0` 约束，已 dismiss（tolerable
risk，dev-time 工具链）。
3. **desktop extract-zip 1 条**：上游无 patched version，已 dismiss。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01NWHV9vozVf6qN6zB5cUUdv

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## 内容

处理 services / desktop / ios 的 73 条 open Dependabot 告警：**修复 58 条，dismiss 2 条，litellm 13 条转 ECA-1397**（codex-coder 实现、Claude review）。

### claw-interface（Python）⚠️ 含框架迁移，重点 review
- `starlette` 0.52.1 → **1.3.1**（安全补丁在 1.x 线）、`fastapi` <0.137 → **0.139.2**。
- 这解除了 requirements 里原有的注释 pin——注释本身写明"等迁移到 Starlette 1.x lifespan API 时一起解除"，本 PR 完成了该迁移：`app/lifetime.py` 从 `add_event_handler("startup"/"shutdown")` 改为 `@asynccontextmanager lifespan`（`finally` 保证 shutdown），`create_app` 经构造参数传入；路由测试适配 `tests/unit/_route_helpers.py`。
- 验证：独立 uv 环境 150 包解析一致；`bash scripts/verify-py.sh` 全过；相关路由单测通过。CI 全量 pytest 是最终把关。

### Node 服务
- whatsapp-business-service：`vitest` 1.x → 3.2.7，刷新 vite / esbuild / postcss / fast-uri / find-my-way（42 tests + typecheck + build 通过）
- r2-access-worker / oauth-worker：`vitest` 3.2.7、`wrangler` 4.125.0，刷新 undici / sharp / ws 等（39 + 17 tests 通过）；oauth-worker 补建独立 `pnpm-lock.yaml`
- desktop：`electron-builder` → 26.15.3（未跨 major），刷新 app-builder-lib / builder-util-runtime / tar / undici / js-yaml / form-data 等（typecheck 通过）
- 各目录 `pnpm install --frozen-lockfile` 均通过

### iOS（后续 commit 补充）
- `jwt` → 2.10.3、`json` → 2.19.9、`faraday` → 1.10.6：三者均在 fastlane 既有约束范围内，直接更新 lockfile（specs + CHECKSUMS，sha256 取自 rubygems API），由 ios-quality CI 的 bundle install 验证。

### 后续 commit：FastAPI 0.137+ 路由测试补迁
- codex 首轮漏迁 3 个路由契约测试（`include_router` 变懒挂载后 `router.routes` 不再展开子路由），已迁到 `api_routes` helper；本地全量 unit 套件 9082 passed。

### 未在本 PR 解决
1. **litellm 13 条（含 3 critical）**：被 `favie-common v0.3.69` 的 OpenTelemetry 1.25.0 pin 阻塞（importlib-metadata 冲突），跟踪 issue：[ECA-1397](https://linear.app/srpone/issue/ECA-1397)。
2. **excon 1 条**：补丁 1.5.0 超出 fastlane `< 1.0.0` 约束，已 dismiss（tolerable risk，dev-time 工具链）。
3. **desktop extract-zip 1 条**：上游无 patched version，已 dismiss。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01NWHV9vozVf6qN6zB5cUUdv


---

## feat(web): route composer skills by agent runtime for engine workspaces (#3504)

- **SHA**: `a0015785f1aaf7acb766c03829a9e4c1e9513a17`
- **作者**: sharplee-srp
- **日期**: 2026-08-25T03:05:43Z
- **PR**: #3504

### Commit Message

```
feat(web): route composer skills by agent runtime for engine workspaces (#3504)

## Linear

[ECA-1394](https://linear.app/srpone/issue/ECA-1394/) — Skill Store:
composer 'Could not load Skills' when bot not ready + no search in
composer Skill Store dialog

## Summary

**Problem.** The Composer Skills menu always called the uid-scoped V1
`/openclaw/runtime-skills` endpoint. For users migrated to a V2 Engine
Agent there is no V1 bot behind that uid, so the Session and New-Chat
composers rendered "Could not load Skills".

**Fix.** Route the Composer's Skills read by the Agent's runtime.

- **`ComposerSkillContext { runtime, workspaceId }`**
(`src/models/skill.ts`) is resolved from the already-known Agent
identity by `resolveComposerSkillContext()` and threaded
`SessionThreadClient` / `ChatBody` / `NewChatClient` → `GenClawInput` /
`OpenClawChatSurface` → `UnifiedChatComposer` → `ComposerAddMenu` →
`ComposerSkillsMenu`. It is kept parallel to — never merged with — the
existing `modelSettings*` props: Model and Skills are independent
capability contracts. Runtime is never guessed from an allowlist or a
catalog card; anything that is not `engine` + a real `workspace_id` (no
Agent, draft Agent, Engine Agent not yet installed into a workspace)
falls back to V1.
- **`useComposerSkills`** is runtime-neutral: one `useQuery` over a
precomputed descriptor, so the two runtimes never conditionally call two
different hooks.
- **computer branch** reuses the newly factored
`runtimeSkillsQueryOptions(uid)` verbatim, so the Composer keeps sharing
the `skillsKeys.runtime(uid)` cache bucket with the Skill Store —
install/uninstall invalidation of that key still updates the Composer
list.
- **engine branch** adds `skillsKeys.engineWorkspace(uid, workspaceId)`
over `GET /agents/{workspaceId}/skills` through the generic
claw-interface proxy (ownership, the `runtime === 'engine'` check, and
the workspace → Engine `agt_*` id mapping are all enforced downstream;
the browser never sees a bare Engine id). Deliberately **not** added to
`PERSIST_ALLOWLIST_PREFIXES`: effective Skills follow the Agent's
rendered config version, so a sessionStorage snapshot could outlive what
it describes.
- **Adapters** normalize V1 `RuntimeSkill` and V2 `EngineWorkspaceSkill`
into a shared `ComposerSkill` display model. The `disabled !== true &&
eligible !== false` filter stays V1-only — the V2 response is already an
effective set; V2 only dedupes by `name` (defensive, because the shared
`SkillsSubMenuItem` keys rows by name).
- **No cross-runtime fallback.** A failed Engine query shows the error
state; it never retries against `/openclaw/runtime-skills` and never
wakes a stopped V1 bot.
- Selection behavior is unchanged (still inserts `Use <name> to…`);
`onSelectSkill` is retyped from `RuntimeSkill` to `ComposerSkill`.
**`@zooclaw/chat-ui` is untouched** — the shared package never learns
about runtimes or APIs.

**Dependency / rollout.** Requires the backend PR
*"feat(claw-interface): add workspace-owned engine agent skills
listing"* — #3505. **That endpoint must deploy before this frontend
change**; until then Engine sessions keep the same failure they have
today, and the V1 path is unaffected either way.

## Test plan

- [x] `bash scripts/verify-web.sh <30 changed paths>` — guards + `tsc
--noEmit` + targeted `vitest` (36 files / 750 tests) + `eslint`, all
green
- [x] `pnpm lint:deadcode`, `pnpm lint:imports`, `pnpm dup` — clean
- [x] `TZ=UTC pnpm test:unit:coverage` — 9182 pass (8 pre-existing
timezone-dependent failures without `TZ=UTC` in
`agent-builder-home-model` / `agent-builder-production-home` /
`UserMenu` / `billing/SubscriptionPanel`; untouched by this PR)
- [x] New unit specs: `composer-skills` adapters + context resolution,
`useComposerSkills` runtime split (key/queryFn/adapter per branch, no
fallback), `useEngineWorkspaceSkills`, plus persist-allowlist assertions
that the engine family is never dehydrated
- [x] Updated specs assert the context is threaded through every
intermediate component and that V2 skips the V1 eligibility filter
- [ ] Post-deploy manual check on a migrated V2 Agent (blocked on the
backend endpoint shipping)
```

### PR Body

## Linear

[ECA-1394](https://linear.app/srpone/issue/ECA-1394/) — Skill Store: composer 'Could not load Skills' when bot not ready + no search in composer Skill Store dialog

## Summary

**Problem.** The Composer Skills menu always called the uid-scoped V1 `/openclaw/runtime-skills` endpoint. For users migrated to a V2 Engine Agent there is no V1 bot behind that uid, so the Session and New-Chat composers rendered "Could not load Skills".

**Fix.** Route the Composer's Skills read by the Agent's runtime.

- **`ComposerSkillContext { runtime, workspaceId }`** (`src/models/skill.ts`) is resolved from the already-known Agent identity by `resolveComposerSkillContext()` and threaded `SessionThreadClient` / `ChatBody` / `NewChatClient` → `GenClawInput` / `OpenClawChatSurface` → `UnifiedChatComposer` → `ComposerAddMenu` → `ComposerSkillsMenu`. It is kept parallel to — never merged with — the existing `modelSettings*` props: Model and Skills are independent capability contracts. Runtime is never guessed from an allowlist or a catalog card; anything that is not `engine` + a real `workspace_id` (no Agent, draft Agent, Engine Agent not yet installed into a workspace) falls back to V1.
- **`useComposerSkills`** is runtime-neutral: one `useQuery` over a precomputed descriptor, so the two runtimes never conditionally call two different hooks.
  - **computer branch** reuses the newly factored `runtimeSkillsQueryOptions(uid)` verbatim, so the Composer keeps sharing the `skillsKeys.runtime(uid)` cache bucket with the Skill Store — install/uninstall invalidation of that key still updates the Composer list.
  - **engine branch** adds `skillsKeys.engineWorkspace(uid, workspaceId)` over `GET /agents/{workspaceId}/skills` through the generic claw-interface proxy (ownership, the `runtime === 'engine'` check, and the workspace → Engine `agt_*` id mapping are all enforced downstream; the browser never sees a bare Engine id). Deliberately **not** added to `PERSIST_ALLOWLIST_PREFIXES`: effective Skills follow the Agent's rendered config version, so a sessionStorage snapshot could outlive what it describes.
- **Adapters** normalize V1 `RuntimeSkill` and V2 `EngineWorkspaceSkill` into a shared `ComposerSkill` display model. The `disabled !== true && eligible !== false` filter stays V1-only — the V2 response is already an effective set; V2 only dedupes by `name` (defensive, because the shared `SkillsSubMenuItem` keys rows by name).
- **No cross-runtime fallback.** A failed Engine query shows the error state; it never retries against `/openclaw/runtime-skills` and never wakes a stopped V1 bot.
- Selection behavior is unchanged (still inserts `Use <name> to…`); `onSelectSkill` is retyped from `RuntimeSkill` to `ComposerSkill`. **`@zooclaw/chat-ui` is untouched** — the shared package never learns about runtimes or APIs.

**Dependency / rollout.** Requires the backend PR *"feat(claw-interface): add workspace-owned engine agent skills listing"* — #3505. **That endpoint must deploy before this frontend change**; until then Engine sessions keep the same failure they have today, and the V1 path is unaffected either way.

## Test plan

- [x] `bash scripts/verify-web.sh <30 changed paths>` — guards + `tsc --noEmit` + targeted `vitest` (36 files / 750 tests) + `eslint`, all green
- [x] `pnpm lint:deadcode`, `pnpm lint:imports`, `pnpm dup` — clean
- [x] `TZ=UTC pnpm test:unit:coverage` — 9182 pass (8 pre-existing timezone-dependent failures without `TZ=UTC` in `agent-builder-home-model` / `agent-builder-production-home` / `UserMenu` / `billing/SubscriptionPanel`; untouched by this PR)
- [x] New unit specs: `composer-skills` adapters + context resolution, `useComposerSkills` runtime split (key/queryFn/adapter per branch, no fallback), `useEngineWorkspaceSkills`, plus persist-allowlist assertions that the engine family is never dehydrated
- [x] Updated specs assert the context is threaded through every intermediate component and that V2 skips the V1 eligibility filter
- [ ] Post-deploy manual check on a migrated V2 Agent (blocked on the backend endpoint shipping)




---

## feat(claw-interface): add workspace-owned engine agent skills listing (#3505)

- **SHA**: `708e5cc0c7b611ac91b1574a18bb7f28ee74114a`
- **作者**: sharplee-srp
- **日期**: 2026-08-25T03:05:17Z
- **PR**: #3505

### Commit Message

```
feat(claw-interface): add workspace-owned engine agent skills listing (#3505)

## Linear

[ECA-1394](https://linear.app/srpone/issue/ECA-1394/) — Skill Store:
composer 'Could not load Skills' when bot not ready + no search in
composer Skill Store dialog

## Summary

Adds `GET /agents/{workspace_id}/skills`: a **workspace-owned,
Engine-runtime-only** listing of the effective (prompt-visible) skills
of a V2 Engine Agent.

**Why.** The web Composer Skills menu today calls the uid-scoped V1
`/openclaw/runtime-skills` endpoint. V2 Engine Agents have no such
uid-scoped runtime, so V2 users see "Could not load Skills". This PR is
the backend half; the web Composer change is a separate PR and **this
must deploy first**.

### What's in it

- **`EngineClient.list_agent_skills(agent_id, *, verbose=False)`** —
`GET /v1/agents/{id}/skills`.
- Pins a **15s per-call timeout**: this is an interactive read behind a
browser request whose own client timeout is 30s, so the 120s client
default would leave the service waiting after the browser has already
given up.
- `_raise_for_agent_status()` so a workspace whose engine-side Agent is
gone maps to **409 detached**, not a bare 404.
  - `_parse_success_response()` for body validation.
- `verbose=True` exists for diagnostics only (it returns excluded
entries plus engine-internal materialization fields) and is never
proxied to a browser.
- **Schemas.** `EngineAgentSkill` / `EngineAgentSkillsResponse` model
the engine contract with `extra="ignore"`; `version` accepts `str | int`
defensively. The public `AgentRuntimeSkillPublic` /
`AgentRuntimeSkillsResponse` use `extra="forbid"` and carry no
`eligible` / `excluded` flags — everything listed is usable.
- **Service** (`agent_runtime_skills_service`) — ownership → runtime
check → entitlement, in that order:
  1. `get_owned_workspace()` scopes to the caller's uid + org.
2. A non-`engine` runtime raises a **masked `agent.not_found`**, so a
computer-runtime workspace cannot probe that a different runtime
topology exists.
  3. `require_agents_v2()` gates the V2 surface.
4. Re-applies the `eligible and excluded is None` prompt-visibility
filter. This is deliberately redundant with the engine's own default
filter — that filter is an inline, untested implementation detail, and
if it regresses an excluded skill must still never reach a browser. Same
semantics as `isPromptVisible()` in `@zooclaw/skills-render`.
5. On upstream `ServiceError`, logs a structured warning with **no
message bodies, skill contents, or service tokens** — only operation,
runtime, workspace id, error code, and upstream status, routed through
`safe_enum()`.

Design spec (see the "PR 2" section):
`docs/superpowers/specs/2026-08-24-v2-composer-runtime-skills-integration.md`.

## Test plan

- [x] `bash scripts/verify-py.sh` — ruff, ruff-format, pyright,
import-linter all green (8 import contracts kept).
- [x] `pytest tests/unit/test_agent_runtime_skills_routes.py
tests/unit/test_engine_client_agent_skills.py -q` — **27 passed** (new).
- Engine client: escaped route, `verbose` default false / true
forwarding, explicit short timeout (not the client default),
engine-internal fields kept out of the model, integer `version`
tolerated, 404 → detached, 5xx → runtime unavailable, transport timeout
→ runtime unavailable, other 4xx → runtime error, malformed body →
invalid response.
- Routes/service: ownership scoping, non-engine runtime masked as 404,
`require_agents_v2` gating, prompt-visibility filter, response shape,
failure logging without sensitive fields.
- [x] Regression set `pytest tests/unit/test_engine_client.py
tests/unit/test_engine_client_skills.py
tests/unit/test_agent_database_routes.py
tests/unit/test_agent_model_routes.py
tests/unit/test_agent_conversations.py
tests/unit/test_agents_v2_access.py -q` — **149 passed**.
- [ ] Full pytest + coverage suite deliberately **not** run locally
(needs local mongo); left to CI's `claw-interface-quality` job.

Backend-only change; no web or iOS surface is touched by this PR.
```

### PR Body

## Linear

[ECA-1394](https://linear.app/srpone/issue/ECA-1394/) — Skill Store: composer 'Could not load Skills' when bot not ready + no search in composer Skill Store dialog

## Summary

Adds `GET /agents/{workspace_id}/skills`: a **workspace-owned, Engine-runtime-only** listing of the effective (prompt-visible) skills of a V2 Engine Agent.

**Why.** The web Composer Skills menu today calls the uid-scoped V1 `/openclaw/runtime-skills` endpoint. V2 Engine Agents have no such uid-scoped runtime, so V2 users see "Could not load Skills". This PR is the backend half; the web Composer change is a separate PR and **this must deploy first**.

### What's in it

- **`EngineClient.list_agent_skills(agent_id, *, verbose=False)`** — `GET /v1/agents/{id}/skills`.
  - Pins a **15s per-call timeout**: this is an interactive read behind a browser request whose own client timeout is 30s, so the 120s client default would leave the service waiting after the browser has already given up.
  - `_raise_for_agent_status()` so a workspace whose engine-side Agent is gone maps to **409 detached**, not a bare 404.
  - `_parse_success_response()` for body validation.
  - `verbose=True` exists for diagnostics only (it returns excluded entries plus engine-internal materialization fields) and is never proxied to a browser.
- **Schemas.** `EngineAgentSkill` / `EngineAgentSkillsResponse` model the engine contract with `extra="ignore"`; `version` accepts `str | int` defensively. The public `AgentRuntimeSkillPublic` / `AgentRuntimeSkillsResponse` use `extra="forbid"` and carry no `eligible` / `excluded` flags — everything listed is usable.
- **Service** (`agent_runtime_skills_service`) — ownership → runtime check → entitlement, in that order:
  1. `get_owned_workspace()` scopes to the caller's uid + org.
  2. A non-`engine` runtime raises a **masked `agent.not_found`**, so a computer-runtime workspace cannot probe that a different runtime topology exists.
  3. `require_agents_v2()` gates the V2 surface.
  4. Re-applies the `eligible and excluded is None` prompt-visibility filter. This is deliberately redundant with the engine's own default filter — that filter is an inline, untested implementation detail, and if it regresses an excluded skill must still never reach a browser. Same semantics as `isPromptVisible()` in `@zooclaw/skills-render`.
  5. On upstream `ServiceError`, logs a structured warning with **no message bodies, skill contents, or service tokens** — only operation, runtime, workspace id, error code, and upstream status, routed through `safe_enum()`.

Design spec (see the "PR 2" section): `docs/superpowers/specs/2026-08-24-v2-composer-runtime-skills-integration.md`.

## Test plan

- [x] `bash scripts/verify-py.sh` — ruff, ruff-format, pyright, import-linter all green (8 import contracts kept).
- [x] `pytest tests/unit/test_agent_runtime_skills_routes.py tests/unit/test_engine_client_agent_skills.py -q` — **27 passed** (new).
  - Engine client: escaped route, `verbose` default false / true forwarding, explicit short timeout (not the client default), engine-internal fields kept out of the model, integer `version` tolerated, 404 → detached, 5xx → runtime unavailable, transport timeout → runtime unavailable, other 4xx → runtime error, malformed body → invalid response.
  - Routes/service: ownership scoping, non-engine runtime masked as 404, `require_agents_v2` gating, prompt-visibility filter, response shape, failure logging without sensitive fields.
- [x] Regression set `pytest tests/unit/test_engine_client.py tests/unit/test_engine_client_skills.py tests/unit/test_agent_database_routes.py tests/unit/test_agent_model_routes.py tests/unit/test_agent_conversations.py tests/unit/test_agents_v2_access.py -q` — **149 passed**.
- [ ] Full pytest + coverage suite deliberately **not** run locally (needs local mongo); left to CI's `claw-interface-quality` job.

Backend-only change; no web or iOS surface is touched by this PR.



---

## feat(marketing): launch localized ZooWork homepage (#3401)

- **SHA**: `f392cde8dee9f30e454374464a144c1b86b9ab3b`
- **作者**: shana-srp
- **日期**: 2026-08-25T02:57:33Z
- **PR**: #3401

### Commit Message

```
feat(marketing): launch localized ZooWork homepage (#3401)

## Linear

N/A

## Summary

- Replace the public homepage body with the new ZooWork marketing
experience.
- Render the supplied eight-section experience in isolated, same-origin
auto-height frames so its CSS and JavaScript cannot leak into the shared
Next.js marketing chrome.
- Merge the approved Runtime and Security redesign from
`zoowork-official-demo#1`: a six-capability Agent Runtime grid and a
six-principle security-boundary model.
- Refresh the shared header, footer, brand assets, and App Store dialog
while preserving the existing authentication behavior.
- Localize the homepage, shared chrome, App Store dialog, metadata, and
refreshed Runtime/Security content across all 10 supported locales,
including RTL document direction for Arabic.
- Keep Get Started connected to the existing login flow and route Talk
to Sales to a pre-addressed system email.
- Add focused unit coverage for the embedded homepage, translations,
metadata, shared marketing chrome, brand assets, and App Store
interactions.
- Features, Contact, and Pricing page changes were extracted to #3429,
#3430, and #3431 respectively.

## Test plan

- [x] `bash scripts/verify-web.sh`
- [x] TypeScript passed.
- [x] 656 test files passed (8,872 tests passed; 70 skipped; 1 todo).
- [x] ESLint passed.
- [x] Verified all 10 supported locales and complete runtime homepage
translations: 368/368 keys per translated bundle.
- [x] Browser-smoke-tested the homepage and English-to-Chinese locale
switch, including shared chrome and embedded section content.
- [x] Verified Arabic RTL handling, localized iframe metadata, dynamic
demo copy, and App Store dialog copy.

## Notes

- This PR intentionally exceeds the normal line budget because it
vendors the approved static homepage experience and complete homepage
translation bundles; the PR already carries the required size override
handling.
- The separately scoped Features, Contact, and Pricing work is tracked
in #3429, #3430, and #3431.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
Co-authored-by: bill-srp <bill@srp.one>
```

### PR Body

## Linear

N/A

## Summary

- Replace the public homepage body with the new ZooWork marketing experience.
- Render the supplied eight-section experience in isolated, same-origin auto-height frames so its CSS and JavaScript cannot leak into the shared Next.js marketing chrome.
- Merge the approved Runtime and Security redesign from `zoowork-official-demo#1`: a six-capability Agent Runtime grid and a six-principle security-boundary model.
- Refresh the shared header, footer, brand assets, and App Store dialog while preserving the existing authentication behavior.
- Localize the homepage, shared chrome, App Store dialog, metadata, and refreshed Runtime/Security content across all 10 supported locales, including RTL document direction for Arabic.
- Keep Get Started connected to the existing login flow and route Talk to Sales to a pre-addressed system email.
- Add focused unit coverage for the embedded homepage, translations, metadata, shared marketing chrome, brand assets, and App Store interactions.
- Features, Contact, and Pricing page changes were extracted to #3429, #3430, and #3431 respectively.

## Test plan

- [x] `bash scripts/verify-web.sh`
- [x] TypeScript passed.
- [x] 656 test files passed (8,872 tests passed; 70 skipped; 1 todo).
- [x] ESLint passed.
- [x] Verified all 10 supported locales and complete runtime homepage translations: 368/368 keys per translated bundle.
- [x] Browser-smoke-tested the homepage and English-to-Chinese locale switch, including shared chrome and embedded section content.
- [x] Verified Arabic RTL handling, localized iframe metadata, dynamic demo copy, and App Store dialog copy.

## Notes

- This PR intentionally exceeds the normal line budget because it vendors the approved static homepage experience and complete homepage translation bundles; the PR already carries the required size override handling.
- The separately scoped Features, Contact, and Pricing work is tracked in #3429, #3430, and #3431.


---

## test(e2e): remove Sora video generation scenario (#3503)

- **SHA**: `812e9036ab52d44eb16f42343d5445f6c6e90fdb`
- **作者**: tim-srp
- **日期**: 2026-08-25T02:58:32Z
- **PR**: #3503

### Commit Message

```
test(e2e): remove Sora video generation scenario (#3503)

## Summary

- Remove the Sora-backed video-generation scenario from the
`basic-usage` E2E project.
- Remove its fixture, timeout, and stale Sora test metadata while
retaining video upload and frame-extraction coverage.
- Add a regression test that prevents restoring the removed
`video_reply` scenario.

## Test plan

- [x] `bash scripts/verify-web.sh
web/app/tests/e2e/fixtures/scenario-data.ts
web/app/tests/e2e/fixtures/test-data.ts
web/app/tests/e2e/specs/scenarios/basic-usage.spec.ts
web/app/tests/e2e/page-objects/zooclaw-chat.page.ts
web/app/tests/unit/e2e/scenario-data.unit.spec.ts`
- [x] `pnpm exec playwright test --project=basic-usage --list`
```

### PR Body

## Summary

- Remove the Sora-backed video-generation scenario from the `basic-usage` E2E project.
- Remove its fixture, timeout, and stale Sora test metadata while retaining video upload and frame-extraction coverage.
- Add a regression test that prevents restoring the removed `video_reply` scenario.

## Test plan

- [x] `bash scripts/verify-web.sh web/app/tests/e2e/fixtures/scenario-data.ts web/app/tests/e2e/fixtures/test-data.ts web/app/tests/e2e/specs/scenarios/basic-usage.spec.ts web/app/tests/e2e/page-objects/zooclaw-chat.page.ts web/app/tests/unit/e2e/scenario-data.unit.spec.ts`
- [x] `pnpm exec playwright test --project=basic-usage --list`


---

## feat(claw-interface): channel binding for service-API agents (#3502)

- **SHA**: `f6d8e71dfea965f5f9866e03c621fe1eecb178a2`
- **作者**: finn-srp
- **日期**: 2026-08-25T02:47:33Z
- **PR**: #3502

### Commit Message

```
feat(claw-interface): channel binding for service-API agents (#3502)

## Linear
<!-- 待补：如有对应 issue，贴完整 Linear URL -->

## Summary

Agents created through `/service/v1` (org service tokens) exist only in
the Engine's Postgres and have no Mongo workspace document. Every
channel entry point resolved a workspace as its first step, so those
agents could not bind Feishu at all — even though ACS, the system of
record for bindings, keys on `(computer_id, agent_id)` and never looks
at workspaces.

This adds `/service/v1/agents/{agent_id}/channels/…`, mirroring the
seven web-surface routes so a service-token caller can list, bind (QR
device flow or direct appId/appSecret), update, and unbind. The caller
owns the UI: `feishu/setup` returns the verification URI and poll
metadata, and the caller renders the QR and drives the poll loop.

To get there, the shared channel services now take a resolved target
instead of a `workspace_id` they look up themselves:

- `EngineChannelTarget` is a `Protocol` that `AgentWorkspace` already
satisfies structurally, so the web surface passes its workspace
unchanged and only the service API needs a concrete
`ResolvedChannelTarget`. That target stores one agent id and derives the
other two roles as properties, so a target whose ids disagree cannot be
constructed.
- The target is a **required** parameter, not optional-with-fallback.
The type checker then enumerates every call site, so no path can
silently fall back to the Mongo lookup and 404 for a service-API agent.
- `get_channel_workspace()` keeps validating exactly as today and its
result *is* the web surface's target. Each of the seven web handlers
keeps the `require_active` value its service used internally (`True` for
add and Feishu setup, `False` for the rest) — that mapping is the
no-behavior-change contract.
- wecom and weixin intentionally keep their workspace-only flows; they
change only where they call the now-target-based shared helpers.

Incidentally removes redundant Mongo reads: Feishu setup 2→1, WeCom
setup 2→1, WeChat confirm-poll 3→1.

**One behavior change for existing traffic** (added in review, see
below): `DELETE /service/v1/agents/{id}` now best-effort disables the
agent's ACS channels after a successful delete. Everything else is
purely additive — the channels path 404s today via engine passthrough,
so no existing caller can be affected. No feature flag: the additive
half needs none, and the delete cleanup must run unconditionally anyway.
Rationale in §3 of the spec.

Design doc:
`docs/superpowers/specs/2026-08-24-service-api-agent-channels.md` — it
also records the three places the implementation diverged from the plan,
and the follow-ups this change deliberately leaves open.

## Test plan

- [x] Full unit suite green (9056 passed, 5 skipped); `ruff`, `ruff
format`, `pyright`, `import-linter` clean.
- [x] New route coverage: every endpoint through the real FastAPI app
with a mocked engine transport, plus cross-org tenant-hiding 404,
fail-closed 502 when the engine omits `computer_id`, invalid body /
account id / missing `session_id`, unknown action, method mismatch.
- [x] Closed a pre-existing gap found while reviewing coverage:
`cancel_wecom_setup`'s ownership gate moved out of
`cancel_setup_session` in this change, and the wecom suite had **no**
cancel tests at all — a relocated security check would have gone
unnoticed. Two tests added; its weixin twin was already pinned.
- [x] Existing suites retargeted rather than deleted: the runtime /
terminal-status / non-active guards now exercise
`get_channel_workspace`, which still owns them.
- [x] Manual: Feishu binding driven against the service API end to end
(QR device flow and direct appId/appSecret).

Before production, see §5 of the spec for the staging pass — in
particular the web-surface regression list (this change moved workspace
resolution into the route handlers, so the `require_active` mapping is
what can drift) and one **unverified** claim worth settling: binding a
v1→v2 *migrated* agent is expected to get an ACS 404, derived from
reading ACS's `resolveIdentity`, never observed.

## Review response

The Codex P1 (bindings survive agent delete) is **fixed in `a8720de95`**
rather than deferred. The deciding fact, verified in engine code: a
deleted agent 404s on the ownership pre-fetch (`resolveAgent` filters
`deleted_at`), so after delete there is no user-facing route left to
remove the binding — and create → bind → delete is this feature's
primary bulk workflow. The DELETE branch now forwards buffered and
best-effort disables the agent's channels on 2xx, using the same ACS
admin call the UI uninstall path already uses; failures log and never
alter the delete result, and a refused delete leaves channels alone.
Still tracked separately (pre-existing gap, ACS owned by another team):
cleaning up already-orphaned channels, an ACS-side reconciler, and
whether an orphaned row holds the `(owner, platform, account)`
uniqueness slot.

## Known follow-ups (deliberately out of scope)
1. **Declarative routes.** `_channels.py` hand-parses paths and wraps
validation errors because it lives under the `/service/v1` catch-all; a
real `APIRouter` registered ahead of the catch-all would own that and
restore OpenAPI for these endpoints. Two independent reviews flagged it;
skipped here because it restructures `service_api/router.py` and turns
the ownership pre-fetch into a dependency.
2. **Feishu poll cost.** Each poll tick pays one engine round-trip (~120
per binding at the default interval) purely to re-derive a `computer_id`
the Redis session already stores.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: wangfulong <wfllike@gmail.com>
Co-authored-by: Claude Opus 5 <noreply@anthropic.com>
```

### PR Body

## Linear
<!-- 待补：如有对应 issue，贴完整 Linear URL -->

## Summary

Agents created through `/service/v1` (org service tokens) exist only in the Engine's Postgres and have no Mongo workspace document. Every channel entry point resolved a workspace as its first step, so those agents could not bind Feishu at all — even though ACS, the system of record for bindings, keys on `(computer_id, agent_id)` and never looks at workspaces.

This adds `/service/v1/agents/{agent_id}/channels/…`, mirroring the seven web-surface routes so a service-token caller can list, bind (QR device flow or direct appId/appSecret), update, and unbind. The caller owns the UI: `feishu/setup` returns the verification URI and poll metadata, and the caller renders the QR and drives the poll loop.

To get there, the shared channel services now take a resolved target instead of a `workspace_id` they look up themselves:

- `EngineChannelTarget` is a `Protocol` that `AgentWorkspace` already satisfies structurally, so the web surface passes its workspace unchanged and only the service API needs a concrete `ResolvedChannelTarget`. That target stores one agent id and derives the other two roles as properties, so a target whose ids disagree cannot be constructed.
- The target is a **required** parameter, not optional-with-fallback. The type checker then enumerates every call site, so no path can silently fall back to the Mongo lookup and 404 for a service-API agent.
- `get_channel_workspace()` keeps validating exactly as today and its result *is* the web surface's target. Each of the seven web handlers keeps the `require_active` value its service used internally (`True` for add and Feishu setup, `False` for the rest) — that mapping is the no-behavior-change contract.
- wecom and weixin intentionally keep their workspace-only flows; they change only where they call the now-target-based shared helpers.

Incidentally removes redundant Mongo reads: Feishu setup 2→1, WeCom setup 2→1, WeChat confirm-poll 3→1.

**One behavior change for existing traffic** (added in review, see below): `DELETE /service/v1/agents/{id}` now best-effort disables the agent's ACS channels after a successful delete. Everything else is purely additive — the channels path 404s today via engine passthrough, so no existing caller can be affected. No feature flag: the additive half needs none, and the delete cleanup must run unconditionally anyway. Rationale in §3 of the spec.

Design doc: `docs/superpowers/specs/2026-08-24-service-api-agent-channels.md` — it also records the three places the implementation diverged from the plan, and the follow-ups this change deliberately leaves open.

## Test plan

- [x] Full unit suite green (9056 passed, 5 skipped); `ruff`, `ruff format`, `pyright`, `import-linter` clean.
- [x] New route coverage: every endpoint through the real FastAPI app with a mocked engine transport, plus cross-org tenant-hiding 404, fail-closed 502 when the engine omits `computer_id`, invalid body / account id / missing `session_id`, unknown action, method mismatch.
- [x] Closed a pre-existing gap found while reviewing coverage: `cancel_wecom_setup`'s ownership gate moved out of `cancel_setup_session` in this change, and the wecom suite had **no** cancel tests at all — a relocated security check would have gone unnoticed. Two tests added; its weixin twin was already pinned.
- [x] Existing suites retargeted rather than deleted: the runtime / terminal-status / non-active guards now exercise `get_channel_workspace`, which still owns them.
- [x] Manual: Feishu binding driven against the service API end to end (QR device flow and direct appId/appSecret).

Before production, see §5 of the spec for the staging pass — in particular the web-surface regression list (this change moved workspace resolution into the route handlers, so the `require_active` mapping is what can drift) and one **unverified** claim worth settling: binding a v1→v2 *migrated* agent is expected to get an ACS 404, derived from reading ACS's `resolveIdentity`, never observed.

## Review response

The Codex P1 (bindings survive agent delete) is **fixed in `a8720de95`** rather than deferred. The deciding fact, verified in engine code: a deleted agent 404s on the ownership pre-fetch (`resolveAgent` filters `deleted_at`), so after delete there is no user-facing route left to remove the binding — and create → bind → delete is this feature's primary bulk workflow. The DELETE branch now forwards buffered and best-effort disables the agent's channels on 2xx, using the same ACS admin call the UI uninstall path already uses; failures log and never alter the delete result, and a refused delete leaves channels alone. Still tracked separately (pre-existing gap, ACS owned by another team): cleaning up already-orphaned channels, an ACS-side reconciler, and whether an orphaned row holds the `(owner, platform, account)` uniqueness slot.

## Known follow-ups (deliberately out of scope)
1. **Declarative routes.** `_channels.py` hand-parses paths and wraps validation errors because it lives under the `/service/v1` catch-all; a real `APIRouter` registered ahead of the catch-all would own that and restore OpenAPI for these endpoints. Two independent reviews flagged it; skipped here because it restructures `service_api/router.py` and turns the ownership pre-fetch into a dependency.
2. **Feishu poll cost.** Each poll tick pays one engine round-trip (~120 per binding at the default interval) purely to re-derive a `computer_id` the Redis session already stores.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(assets): redesign unified asset library (#3225)

- **SHA**: `07feaace1e8d8d931de7b447a7b48a85e2eb862a`
- **作者**: shana-srp
- **日期**: 2026-08-25T02:41:10Z
- **PR**: #3225

### Commit Message

```
feat(assets): redesign unified asset library (#3225)

## Summary

- restore the original #3225 Library frontend with separate My uploads
and AI generated tabs
- keep the shared file-type and Agent filters, search, grid/list
layouts, date grouping, image preview, and Composer selection flow
- connect AI generated files to the account-scoped cursor endpoint from
#3372: `GET /agents/artifacts/library`
- keep structured-file grid previews fixed-cost; PDF, DOCX, PPTX, and
XLSX covers do not parse the full document
- discard authenticated preview completions if the account or Mattermost
token changes while a Blob request is in flight

## Conflict resolution

- merged the latest `origin/main` into the existing #3225 branch with
the PR branch as first parent
- restored the last known-good Library frontend from `dd34a2ae` on top
of current main instead of resolving conflicts by taking main's empty
tree
- GitHub reports the PR as `MERGEABLE`; the PR now contains the Library
implementation rather than a zero-file diff

## Validation

- `bash scripts/verify-web.sh` passed TypeScript, focused Vitest,
ESLint, and all frontend governance guards
- restored Library suite: 84 relevant tests passed
- authenticated-preview regression suite: 39 UploadsFeed tests passed
- dependency-boundary and dead-code gates passed
- first GitHub run passed web build, web lint/typecheck, web tests,
CodeQL, title, and size checks; the follow-up review fix is running the
same gates again

## Size override

The restored page crosses the 3,000-line budget because it reintroduces
the complete Library feed and its comprehensive regression suite while
deleting the superseded workspace-browser implementation. The
`size-override` label keeps the production behavior and tests together
in the original #3225 PR instead of dropping coverage to trim 63 lines.

## Dependency

The backend Library route is already on `main` via #3372. This PR
restores and adapts the frontend only.

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary

- restore the original #3225 Library frontend with separate My uploads and AI generated tabs
- keep the shared file-type and Agent filters, search, grid/list layouts, date grouping, image preview, and Composer selection flow
- connect AI generated files to the account-scoped cursor endpoint from #3372: `GET /agents/artifacts/library`
- keep structured-file grid previews fixed-cost; PDF, DOCX, PPTX, and XLSX covers do not parse the full document
- discard authenticated preview completions if the account or Mattermost token changes while a Blob request is in flight

## Conflict resolution

- merged the latest `origin/main` into the existing #3225 branch with the PR branch as first parent
- restored the last known-good Library frontend from `dd34a2ae` on top of current main instead of resolving conflicts by taking main's empty tree
- GitHub reports the PR as `MERGEABLE`; the PR now contains the Library implementation rather than a zero-file diff

## Validation

- `bash scripts/verify-web.sh` passed TypeScript, focused Vitest, ESLint, and all frontend governance guards
- restored Library suite: 84 relevant tests passed
- authenticated-preview regression suite: 39 UploadsFeed tests passed
- dependency-boundary and dead-code gates passed
- first GitHub run passed web build, web lint/typecheck, web tests, CodeQL, title, and size checks; the follow-up review fix is running the same gates again

## Size override

The restored page crosses the 3,000-line budget because it reintroduces the complete Library feed and its comprehensive regression suite while deleting the superseded workspace-browser implementation. The `size-override` label keeps the production behavior and tests together in the original #3225 PR instead of dropping coverage to trim 63 lines.

## Dependency

The backend Library route is already on `main` via #3372. This PR restores and adapts the frontend only.



---
