---
title: "修复微信扫码绑定 100% 失败的问题"
type: "Bug Fix"
priority: "高"
date: "2026-08-06"
status: "待审核"
channels: ""
---

## 核心宣传点

此前用户扫码确认后微信渠道始终绑定失败（后台平台名不一致导致请求被拒），现已修复，微信扫码绑定恢复正常。

## 原始内容

**fix(claw-interface): map weixin to ACS wechat platform at channel boundary (#3283)**

- sha: `cebe769db5702a9365da4bb0ae5835703d6a9851`
- PR: #3283

```
fix(claw-interface): map weixin to ACS wechat platform at channel boundary (#3283)

## Summary
- Translate the product platform name `weixin` to the ACS platform name
`wechat` at every agent-channel-service boundary in
`engine_agent_channels_service.py`, in both directions:
- outbound: `_create_channel_acs`, `update_channel`, `remove_channel`
send/address `wechat`
- inbound: `list_channels`, `update_channel`, `_create_channel_acs` map
returned `wechat` rows back to `weixin` via immutable `model_copy`
before they reach routes/frontend
- `add_channel` now rejects both spellings (`weixin` and `wechat`) with
`channel.weixin_setup_required`, so the direct-add path cannot bypass
the QR setup flow by using the ACS spelling.
- `engine_weixin_channel_service.py` (QR flow) is unchanged — its
`weixin` constant is the product name; existing-channel detection and
create/update go through the mapped service functions.

## Root cause
The engine-agent WeChat QR bind has failed 100% since #2973: after the
user scans and confirms the QR, claw-interface calls ACS
`create_channel` with `platform: "weixin"`, but ACS
`ManagedChannelPlatformSchema` only accepts `["feishu", "mattermost",
"slack", "wechat", "wecom"]` — the request dies with 400 `request failed
validation` (surfaced as `channel.invalid_request`). The ACS channel-API
design doc maps the product WeChat platform to ACS `wechat`;
claw-interface never implemented that translation, while sibling flows
(`wecom`, `feishu`) happen to use enum-valid names. Diagnosed in staging
for uid `7268822997437874176` / workspace
`49593ba04519473d805a98745ae56a0b` (3 bind attempts 2026-08-06
08:19–08:25 UTC, each `confirmed` then ACS 400).

The frontend contract stays `weixin` throughout (`isWeixinPlatform()`
accepts `weixin`/`openclaw-weixin`, not `wechat`), so responses are
mapped back symmetrically. The v1 computer-runtime flow
(`openclaw-weixin`) never touches ACS and is unaffected.

## Test plan
- [x] TDD: new unit tests written first (red), then implementation
(green)
- create for weixin sends `platform="wechat"` to the ACS client
(idempotency key keeps the product name)
  - update/remove with `weixin` address the ACS channel as `wechat`
- `list_channels` maps a `wechat` row back to `weixin` (immutable copy,
original row untouched), passes `feishu`/`wecom`/`slack` through, still
filters `mattermost`
- `update_channel`/create return product-named rows (route
`AgentChannelPublic` never sees `wechat`)
- `add_channel` rejects both `weixin` and `wechat` with
`channel.weixin_setup_required`
- end-to-end QR poll test: existing-channel detection matches when ACS
returns a `wechat` row, `update_channel` called with `wechat`, no
duplicate create
- [x] `bash scripts/verify-py.sh` green (ruff, ruff-format, pyright,
import-linter 8/8 contracts)
- [x] 128 unit tests pass across
`test_engine_agent_channels_service.py`,
`test_engine_weixin_channel_service.py`,
`test_agents_v2_channels_routes.py`
- [ ] Post-deploy: staging QR bind smoke (scan → confirmed → channel row
created in ACS, listed as `weixin` in UI) — cross-service enum drift is
invisible to static checks, needs one real end-to-end pass
```

**PR Body:**

## Summary
- Translate the product platform name `weixin` to the ACS platform name `wechat` at every agent-channel-service boundary in `engine_agent_channels_service.py`, in both directions:
  - outbound: `_create_channel_acs`, `update_channel`, `remove_channel` send/address `wechat`
  - inbound: `list_channels`, `update_channel`, `_create_channel_acs` map returned `wechat` rows back to `weixin` via immutable `model_copy` before they reach routes/frontend
- `add_channel` now rejects both spellings (`weixin` and `wechat`) with `channel.weixin_setup_required`, so the direct-add path cannot bypass the QR setup flow by using the ACS spelling.
- `engine_weixin_channel_service.py` (QR flow) is unchanged — its `weixin` constant is the product name; existing-channel detection and create/update go through the mapped service functions.

## Root cause
The engine-agent WeChat QR bind has failed 100% since #2973: after the user scans and confirms the QR, claw-interface calls ACS `create_channel` with `platform: "weixin"`, but ACS `ManagedChannelPlatformSchema` only accepts `["feishu", "mattermost", "slack", "wechat", "wecom"]` — the request dies with 400 `request failed validation` (surfaced as `channel.invalid_request`). The ACS channel-API design doc maps the product WeChat platform to ACS `wechat`; claw-interface never implemented that translation, while sibling flows (`wecom`, `feishu`) happen to use enum-valid names. Diagnosed in staging for uid `7268822997437874176` / workspace `49593ba04519473d805a98745ae56a0b` (3 bind attempts 2026-08-06 08:19–08:25 UTC, each `confirmed` then ACS 400).

The frontend contract stays `weixin` throughout (`isWeixinPlatform()` accepts `weixin`/`openclaw-weixin`, not `wechat`), so responses are mapped back symmetrically. The v1 computer-runtime flow (`openclaw-weixin`) never touches ACS and is unaffected.

## Test plan
- [x] TDD: new unit tests written first (red), then implementation (green)
  - create for weixin sends `platform="wechat"` to the ACS client (idempotency key keeps the product name)
  - update/remove with `weixin` address the ACS channel as `wechat`
  - `list_channels` maps a `wechat` row back to `weixin` (immutable copy, original row untouched), passes `feishu`/`wecom`/`slack` through, still filters `mattermost`
  - `update_channel`/create return product-named rows (route `AgentChannelPublic` never sees `wechat`)
  - `add_channel` rejects both `weixin` and `wechat` with `channel.weixin_setup_required`
  - end-to-end QR poll test: existing-channel detection matches when ACS returns a `wechat` row, `update_channel` called with `wechat`, no duplicate create
- [x] `bash scripts/verify-py.sh` green (ruff, ruff-format, pyright, import-linter 8/8 contracts)
- [x] 128 unit tests pass across `test_engine_agent_channels_service.py`, `test_engine_weixin_channel_service.py`, `test_agents_v2_channels_routes.py`
- [ ] Post-deploy: staging QR bind smoke (scan → confirmed → channel row created in ACS, listed as `weixin` in UI) — cross-service enum drift is invisible to static checks, needs one real end-to-end pass

