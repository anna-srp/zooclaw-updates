---
title: "后端：语音转写接口支持短期专用令牌，录音客户端不再携带长期会话凭证"
type: "后端功能"
priority: "高"
date: "2026-10-16"
status: "待审核"
channels: ""
---

# 后端：语音转写接口支持短期专用令牌，录音客户端不再携带长期会话凭证

## 核心宣传点

ASR（语音转写）路由除会话 JWT 外，现在还接受账号服务通过 RFC 8693 交换（POST /auth/token-exchange）签发的短期、绑定受众的资源令牌，录音 App 这类原生客户端因此不必再把长期会话 JWT 发到转写服务，凭证一旦泄露的影响面大幅收窄。新增 ASR_RESOURCE_AUDIENCE（批量转写）与 ASR_REALTIME_RESOURCE_AUDIENCE（实时转写）两项配置，在配置加载时就做严格校验：留空即关闭，否则必须是 https://host[:port] 加对应路由路径，且两者不能相同。对终端用户无界面变化，属于安全加固。

## 分级

- 内部：P1
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## 备注

需与 ecap-proxy-service #212（TRANSCRIPTION_RESOURCE_AUDIENCE）配套发版，并在账号服务侧配置受众白名单；实时路由的受众需写成 https 形式（客户端实际用 wss）。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `85eedd826d90f2a1c3c0cfdb385ce81a0111ea16`
- PR: #4082
- 作者：sharplee-srp
- 日期：2026-10-16T08:35:01Z

### Commit Message

```
feat(claw-interface): accept audience-bound resource tokens on ASR routes (#4082)

## Linear
None.

## Summary
Lets the ASR routes accept a short-lived, audience-bound resource token
from the account service's RFC 8693 exchange (`POST
/auth/token-exchange`), besides the session JWT, so native clients such
as the recorder app never send the long-lived session JWT here. Mirrors
ecap-proxy-service PR #212 (`TRANSCRIPTION_RESOURCE_AUDIENCE`).

- **Settings**: `ASR_RESOURCE_AUDIENCE` (batch,
`https://<host>/asr/v1/audio/transcriptions`) and
`ASR_REALTIME_RESOURCE_AUDIENCE` (realtime,
`https://<host>/asr/v1/realtime`; an https URL even though clients use
wss, because the account-service allow-list takes HTTPS URLs). Validated
at settings load: empty disables; otherwise exactly
`https://host[:port]<route path>`. Rejects http/wss, uppercase scheme,
query, fragment, userinfo, whitespace, bad port, trailing slash, any
other path; the two must differ. This service has no MCP
resource-audience setting, so there is nothing else to compare against;
the exact path check already keeps an MCP audience out.
- **Auth**: new `require_asr_token` / `require_asr_realtime_token` in
`app/middleware/auth.py` (L0, return `VerifiedToken`). A bearer whose
unverified payload says `token_use: "resource"` goes only to `GET
/auth/verify-resource?audience=<route URL>` (new
`verify_resource_token`, own per-audience cache, same retry and 401/503
semantics as `verify_user_token`); every other bearer goes to
`/auth/verify`. No fallback between the two. Feature off = exactly the
old behavior.
- **Other routes refuse resource tokens**: `verify_user_token` now
rejects a bearer claiming `token_use=resource` locally with 401 before
calling the account service (which also rejects it, since PyJWT refuses
an `aud`-bearing token when no audience is expected). This is a
deliberate tightening over #212.
- **uid-only callers**: the ASR routes use only the uid (record
persistence); no quota, billing, or user lookups. The account service's
`/auth/verify-resource` already requires a registered user, so no extra
account read is added, matching the session path here (zero DB reads).
- **Refactors**: ASR moves off the legacy `get_current_user` stack; the
router-level `Depends(get_current_user)` is removed (it would refuse
resource tokens), and each endpoint declares its own dependency.
`schedule_ws_persist` and the WS helpers take `uid: str` instead of a
`current_user` dict. The account-service GET + retry is shared by both
verifiers (`_get_with_retry`), keeping the `/auth/verify` call shape
unchanged.

Deliberate choices reviewers may ask about:
- WebSocket auth runs before `accept()`, so a failure is an HTTP
handshake denial (401, or 503 when the account service is unavailable),
not an accepted socket closed with 1008. That is the existing behavior
and the safer one.
- Tokens come from the `Authorization` header only. The route never
supported query-string tokens and still does not.
- The new dependency's missing/malformed-header detail is the L0
contract string (`Missing authentication token`) rather than the legacy
`get_current_user` strings.

Deployment (per environment): add both URLs, byte for byte, to the
account service's `RESOURCE_TOKEN_ALLOWED_AUDIENCES`, then set the two
env vars here. Details in
`services/claw-interface/docs/asr-resource-tokens.md`. Backend-only; no
web change.

## Test plan
- [x] `tests/unit/test_settings_asr_resource_audience.py`: settings
matrix for both fields
- [x] `tests/unit/test_asr_resource_token_auth.py`: auth matrix for both
routes (resource token with exact audience, session token, other
audiences incl. MCP refused without fallback, invalid session token
without resource fallback, 503 on verifier outage, missing/malformed
header, query-string token ignored, WS denial statuses and `ready` on
success), feature off, other routes (L0 and legacy) refuse resource
tokens, `verify_resource_token` HTTP behavior (exact URL/params,
per-audience cache, 401/503, unconfigured), local refusal in
`verify_user_token`
- [x] Existing `test_asr_routes.py`, `test_auth.py`,
`test_middleware_auth_and_org.py`, `test_auth_level_dedup.py` pass
- [x] `bash scripts/verify-py.sh --full` static gates (ruff, ruff
format, pyright, import-linter, ci-lint guards) pass
- [ ] Staging: exchange a token for each audience and call both routes
(needs the account-service allow-list change)
```

