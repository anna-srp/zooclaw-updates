---
title: "修复桌面客户端聊天一直卡在「正在接通你的 Claw…」连不上"
type: "Bug Fix"
priority: "高"
date: "2026-06-18"
status: "待审核"
channels: "Discord+changelog"
---
# 修复桌面客户端聊天一直卡在「正在接通你的 Claw…」连不上
## 核心宣传点
修复打包版桌面客户端因端口随机导致后端拒绝其来源、聊天一直卡在「正在接通你的 Claw…」无法连接实时消息的问题。现在打包应用固定使用 3000 端口，登录与实时聊天恢复正常。
## 原始内容
fix(desktop): pin packaged Next server to port 3000 so backends accept its origin (#2503)

## Problem
The packaged PandaClaw desktop app served its renderer from
`http://localhost:<random free port>`. The app's backends gate
cross-origin requests on an **Origin allow-list that only permits
`http://localhost:3000`** (the dev origin) — verified directly:
Mattermost returns no `Access-Control-Allow-Origin` for
`localhost:55477`/`:3001`/etc., only for `:3000`. So a packaged build
(random port) had its Mattermost WS/REST origin rejected → chat stuck on
"正在接通你的 Claw…", realtime never connects. (Dev worked because `next dev`
is always on `:3000`.)

## Fix
- **Pin the packaged Next server to port 3000** so the packaged origin
is identical to dev's, which the backends already allow. No CORS bridge
/ header rewriting needed. Falls back to a free port only if 3000 is
taken.
- **Inject `CLAW_INTERFACE_URL` into the spawned standalone server's
env** — the packaged standalone has no `.env`, so the BFF proxy would
fall back to `localhost:8000`. Selectable per build via the tsup-inlined
`DESKTOP_BACKEND_URL` (prod vs staging); defaults to staging.

## Verification
Built a local staging DMG: confirmed the packaged app listens on
`:3000`, login (Google) works, and Mattermost realtime connects (chat
"Claw 已连接"). Same behavior as `pnpm dev`.

## Scope
Two files, desktop-only (`desktop/main/next-server.ts`,
`desktop/tsup.config.ts`). No web/runtime behavior change.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>

## PR Description
## Problem
The packaged PandaClaw desktop app served its renderer from `http://localhost:<random free port>`. The app's backends gate cross-origin requests on an **Origin allow-list that only permits `http://localhost:3000`** (the dev origin) — verified directly: Mattermost returns no `Access-Control-Allow-Origin` for `localhost:55477`/`:3001`/etc., only for `:3000`. So a packaged build (random port) had its Mattermost WS/REST origin rejected → chat stuck on "正在接通你的 Claw…", realtime never connects. (Dev worked because `next dev` is always on `:3000`.)

## Fix
- **Pin the packaged Next server to port 3000** so the packaged origin is identical to dev's, which the backends already allow. No CORS bridge / header rewriting needed. Falls back to a free port only if 3000 is taken.
- **Inject `CLAW_INTERFACE_URL` into the spawned standalone server's env** — the packaged standalone has no `.env`, so the BFF proxy would fall back to `localhost:8000`. Selectable per build via the tsup-inlined `DESKTOP_BACKEND_URL` (prod vs staging); defaults to staging.

## Verification
Built a local staging DMG: confirmed the packaged app listens on `:3000`, login (Google) works, and Mattermost realtime connects (chat "Claw 已连接"). Same behavior as `pnpm dev`.

## Scope
Two files, desktop-only (`desktop/main/next-server.ts`, `desktop/tsup.config.ts`). No web/runtime behavior change.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
