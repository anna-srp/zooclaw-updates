---
title: "修复新版机器人网页聊天连不上、报「Something went wrong」"
type: "Bug Fix"
priority: "高"
date: "2026-06-12"
status: "待审核"
channels: ""
---
# 修复新版机器人网页聊天连不上、报「Something went wrong」

## 核心宣传点
升级到新版运行时（openclaw 2026.6.5）的机器人，网页聊天和控制台之前会连接失败、反复报「Something went wrong」，现已修复，网页端可正常连接、加载历史并实时收发消息。

## 原始内容

fix(openclaw-ws): accept protocol range [3,4] for openclaw 2026.6.5 (WS protocol v4) (#2409)

## Problem

openclaw 2026.6.5 (staging canary track) bumps the gateway WS protocol 3 → 4 and **hard-rejects pure-v3 clients** — no compat window (`maxProtocol >= 4 && minProtocol <= 4`). Our WS clients hardcode `min=max=3`, so webchat/control-ui against 6.5 bots is fully broken, surfacing as the generic "Something went wrong":

- bot `a8c4d697`: 47+ `protocol mismatch ... expected 4` in 2h
- bot `046db9e1`: 1267 rejected connections in 4h

## Fix

Advertise **`minProtocol: 3, maxProtocol: 4`** in both WS clients:
- `web/app/src/hooks/useOpenClawWebSocket.ts` (webchat / control-ui)
- `desktop/main/openclaw/bridge.ts` (desktop node-host bridge — same latent defect)

Verified against both runtime packages' handshake validation that one range-client passes both: 2026.5.7 checks `max>=3 && min<=3` (negotiates 3), 2026.6.5 checks `max>=4 && min<=4` (negotiates 4). The v4 `ConnectParams` schema is shape-compatible with the frames we already send (checked against `packages/gateway-protocol/src/schema/frames.ts` in the 2026.6.5 dist).

## Validation

- [ ] Webchat against a 6.5 staging canary bot (a8c4d697 / f7b48e07) — connects, chat history loads, messages stream
- [ ] Webchat against a 5.7 bot — no regression (negotiates 3)
- [ ] v4 negotiated session: verify event-stream handling end-to-end (protocol bump may carry frame-semantics changes beyond the handshake)

Companion fixes: backend WSS client SerendipityOneInc/fastclaw#124; feishu dispatch crash SerendipityOneInc/openclaw-docker#135.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
