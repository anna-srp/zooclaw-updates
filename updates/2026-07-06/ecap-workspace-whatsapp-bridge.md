---
title: "新增 WhatsApp Business 渠道接入"
type: "新功能上线"
priority: "高"
date: "2026-07-06"
status: "待审核"
channels: ""
---

# 新增 WhatsApp Business 渠道接入

## 核心宣传点

ZooClaw 新增 WhatsApp Business 渠道桥接：绑定后可以直接在 WhatsApp 里和你的 Agent 对话，消息双向互通，海外用户从此多了一个常用 IM 入口。

## 原始内容

[04b3bec4] feat(services): add whatsapp business bridge (#2522)

## Summary

- Adds a standalone `services/whatsapp-business-service` Fastify worker
for WhatsApp Cloud API webhook intake.
- Verifies Meta webhook signatures, parses inbound WhatsApp messages,
and routes known users to Mattermost.
- Adds Claw Interface service-client calls for WhatsApp message
claim/complete, user lookup/register, and Mattermost outbound target
resolution.
- Adds Mattermost WebSocket forwarding so Mattermost replies can be sent
back through WhatsApp Graph API.
- Adds the matching Claw Interface WhatsApp routes/service logic
(claim/complete lease contract, user lookup/register/bind, outbound
target resolution with bot-author proof) plus deploy/tag workflows for
the new service.
- Hardens the bridge against malformed signatures, retryable per-message
routing failures, duplicate same-token websocket setup, stale Mattermost
websocket pool entries, missing required integration config, duplicate
Meta webhook delivery via exclusive `message_id` claim/complete
contracts, and inbound WhatsApp echo-back through Mattermost outbound
routing.
- Serializes same-sender webhook batches (later messages stay unclaimed
after an earlier retryable failure) so Meta replay preserves
conversation order; distinct senders still route concurrently.
- Replies through WhatsApp instead of silently consuming messages the
bridge cannot forward: unsupported non-text types, unbound first-time
senders, and bound users whose workspace routing is still being
repaired.
- Treats every completion-persistence failure (lost lease or exhausted
retries) as a retryable batch failure so Meta replays drive the claim
row to a terminal completed state — at-least-once delivery with
`message_id` dedupe, never a permanently incomplete row.
- Reconnects Mattermost websockets with exponential backoff (initial
connect failures included) instead of tight-looping on revoked tokens.
- Outbound resolution fails closed unless the Mattermost post author is
proven to be the workspace bot.
- Staging deploys are gated on `services/whatsapp-business-service/**`
changes so unrelated main merges cannot restart the bridge; release tags
pin the merged commit.
- Documents the business flow, runtime config, and local service
commands.

## Local checks

- `CI=true pnpm --dir services/whatsapp-business-service
--config.confirmModulesPurge=false typecheck`
- `CI=true pnpm --dir services/whatsapp-business-service
--config.confirmModulesPurge=false test` (5 files, 48 tests)
- `CI=true pnpm --dir services/whatsapp-business-service
--config.confirmModulesPurge=false build`
- claw-interface: pytest unit suites for whatsapp routes/service, ruff,
pyright, import-linter

## Notes

- Reply listening is still registered in-process from inbound traffic
only. Durable listener bootstrap across restarts is intentionally
deferred: deploys are double-gated behind
`WHATSAPP_BUSINESS_SERVICE_DEPLOY_ENABLED` and
`WHATSAPP_BUSINESS_LISTENER_BOOTSTRAP_READY`, and a follow-up PR with a
design spec will move watched-token state into Claw Interface.

--- PR #2522 body ---
## Summary

- Adds a standalone `services/whatsapp-business-service` Fastify worker for WhatsApp Cloud API webhook intake.
- Verifies Meta webhook signatures, parses inbound WhatsApp messages, and routes known users to Mattermost.
- Adds Claw Interface service-client calls for WhatsApp message claim/complete, user lookup/register, and Mattermost outbound target resolution.
- Adds Mattermost WebSocket forwarding so Mattermost replies can be sent back through WhatsApp Graph API.
- Adds the matching Claw Interface WhatsApp routes/service logic (claim/complete lease contract, user lookup/register/bind, outbound target resolution with bot-author proof) plus deploy/tag workflows for the new service.
- Hardens the bridge against malformed signatures, retryable per-message routing failures, duplicate same-token websocket setup, stale Mattermost websocket pool entries, missing required integration config, duplicate Meta webhook delivery via exclusive `message_id` claim/complete contracts, and inbound WhatsApp echo-back through Mattermost outbound routing.
- Serializes same-sender webhook batches (later messages stay unclaimed after an earlier retryable failure) so Meta replay preserves conversation order; distinct senders still route concurrently.
- Replies through WhatsApp instead of silently consuming messages the bridge cannot forward: unsupported non-text types, unbound first-time senders, and bound users whose workspace routing is still being repaired.
- Treats every completion-persistence failure (lost lease or exhausted retries) as a retryable batch failure so Meta replays drive the claim row to a terminal completed state — at-least-once delivery with `message_id` dedupe, never a permanently incomplete row.
- Reconnects Mattermost websockets with exponential backoff (initial connect failures included) instead of tight-looping on revoked tokens.
- Outbound resolution fails closed unless the Mattermost post author is proven to be the workspace bot.
- Staging deploys are gated on `services/whatsapp-business-service/**` changes so unrelated main merges cannot restart the bridge; release tags pin the merged commit.
- Documents the business flow, runtime config, and local service commands.

## Local checks

- `CI=true pnpm --dir services/whatsapp-business-service --config.confirmModulesPurge=false typecheck`
- `CI=true pnpm --dir services/whatsapp-business-service --config.confirmModulesPurge=false test` (5 files, 48 tests)
- `CI=true pnpm --dir services/whatsapp-business-service --config.confirmModulesPurge=false build`
- claw-interface: pytest unit suites for whatsapp routes/service, ruff, pyright, import-linter

## Notes

- Reply listening is still registered in-process from inbound traffic only. Durable listener bootstrap across restarts is intentionally deferred: deploys are double-gated behind `WHATSAPP_BUSINESS_SERVICE_DEPLOY_ENABLED` and `WHATSAPP_BUSINESS_LISTENER_BOOTSTRAP_READY`, and a follow-up PR with a design spec will move watched-token state into Claw Interface.

