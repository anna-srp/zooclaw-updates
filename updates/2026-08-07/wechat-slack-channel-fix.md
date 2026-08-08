---
title: "修复微信凭据与 Slack 会话异常"
type: "Bug Fix"
priority: "高"
date: "2026-08-07"
status: "待审核"
channels: ""
---

## 核心宣传点

修复微信扫码绑定后凭据存错字段导致插件读不到的问题，同时修正 Slack 多轮回复会串会话的缺陷，渠道连接更可靠。

## 原始内容

### fix(channels): repair Slack sessions and WeChat credentials (#3293)

- SHA: `6936130fe844ba70a8121c237385e6fb63c34330`
- 仓库: 见 raw/2026-08-07

**Commit Message:**

```
fix(channels): repair Slack sessions and WeChat credentials (#3293)

## Summary

- Fix the engine Weixin QR boundary so the ilink `bot_token` is sent to
ACS as the maintained WeChat plugin config key `token`, not the
unrelated `botToken` key.
- Cover both create and reconnect/update paths in unit tests, and update
the engine-agent Weixin BDD contract.
- Correct the authoritative WeChat design and implementation-plan
documents to distinguish gateway `{bot_token, baseurl}` from ACS
`{token, baseUrl}`.
- Document the companion cross-repository Slack thread-session repair
for ACS and ZooClaw Engine.

## Root causes

### WeChat

The QR gateway correctly returned `bot_token`, but claw-interface
translated it to `config.botToken`. The maintained WeChat plugin reads
`config.token`, so ACS stored a credential under a key the plugin does
not consume.

### Slack

ACS treated Slack `ReplyToId` as thread identity, so a follow-up could
change the canonical session key. Engine then attempted to persist the
same trusted session ID under the new key and retried a deterministic
unique conflict.

## Validation

- [x] `pytest -q tests/unit/test_engine_weixin_channel_service.py` — 23
passed.
- [x] `bash scripts/verify-py.sh` — ruff, format, pyright, and
import-linter passed.
- [x] Pre-commit backend guards passed.
- [x] Pre-push changed-surface verification passed.
- [x] WeChat create and reconnect/update assertions require `{token,
baseUrl}` and reject accidental `botToken` drift by exact dictionary
equality.
- [ ] The focused Weixin BDD scenario was collected locally but skipped
because the local Mongo fixture was unavailable; CI runs it with the
Mongo service container.
- [ ] Merge and deploy the ACS and Engine implementation PRs before
running the guarded Slack staging data repair.

## Companion implementation PRs

- ACS Slack identity/config fix:
https://github.com/SerendipityOneInc/agent-channel-service/pull/64
- Engine session-identity defense:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/628

## Rollout notes

- Existing WeChat rows containing only `botToken` still require
credential repair. Re-running the authenticated Weixin QR flow updates
the fixed `default` account in place with `token` and preserves
unrelated policies/config.
- The affected Slack data repair remains gated on both companion
implementation PRs being deployed.
```

**PR Body:**

## Summary

- Fix the engine Weixin QR boundary so the ilink `bot_token` is sent to ACS as the maintained WeChat plugin config key `token`, not the unrelated `botToken` key.
- Cover both create and reconnect/update paths in unit tests, and update the engine-agent Weixin BDD contract.
- Correct the authoritative WeChat design and implementation-plan documents to distinguish gateway `{bot_token, baseurl}` from ACS `{token, baseUrl}`.
- Document the companion cross-repository Slack thread-session repair for ACS and ZooClaw Engine.

## Root causes

### WeChat

The QR gateway correctly returned `bot_token`, but claw-interface translated it to `config.botToken`. The maintained WeChat plugin reads `config.token`, so ACS stored a credential under a key the plugin does not consume.

### Slack

ACS treated Slack `ReplyToId` as thread identity, so a follow-up could change the canonical session key. Engine then attempted to persist the same trusted session ID under the new key and retried a deterministic unique conflict.

## Validation

- [x] `pytest -q tests/unit/test_engine_weixin_channel_service.py` — 23 passed.
- [x] `bash scripts/verify-py.sh` — ruff, format, pyright, and import-linter passed.
- [x] Pre-commit backend guards passed.
- [x] Pre-push changed-surface verification passed.
- [x] WeChat create and reconnect/update assertions require `{token, baseUrl}` and reject accidental `botToken` drift by exact dictionary equality.
- [ ] The focused Weixin BDD scenario was collected locally but skipped because the local Mongo fixture was unavailable; CI runs it with the Mongo service container.
- [ ] Merge and deploy the ACS and Engine implementation PRs before running the guarded Slack staging data repair.

## Companion implementation PRs

- ACS Slack identity/config fix: https://github.com/SerendipityOneInc/agent-channel-service/pull/64
- Engine session-identity defense: https://github.com/SerendipityOneInc/zooclaw-engine/pull/628

## Rollout notes

- Existing WeChat rows containing only `botToken` still require credential repair. Re-running the authenticated Weixin QR flow updates the fixed `default` account in place with `token` and preserves unrelated policies/config.
- The affected Slack data repair remains gated on both companion implementation PRs being deployed.


