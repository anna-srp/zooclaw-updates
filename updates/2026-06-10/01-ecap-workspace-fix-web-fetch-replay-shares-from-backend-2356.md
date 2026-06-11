---
title: "回放分享页面修复：链接可正常打开"
type: "Bug Fix"
priority: "中"
date: "2026-06-10"
status: "待审核"
channels: ""
---
# 回放分享页面修复：链接可正常打开

## 核心宣传点
修复了部分情况下回放分享链接打不开、误显示「该回放已不可用」的问题，现在分享链接能稳定访问。

## 原始内容
```
fix(web): fetch replay shares from backend (#2356)

## Summary
- Route public replay share SSR through claw-interface directly instead
of self-fetching the public `/api` route.
- Preserve unavailable UI only for backend 404/revoked shares; surface
other upstream or routing failures through the error boundary.
- Add unit coverage for backend URL encoding, CF Access headers, 404
handling, non-JSON HTML fallback, and abort signals.

## Root cause
Staging Worker SSR fetches to its own custom domain
`/api/chat-replays/:id` could resolve through Cloudflare zone routing
and return the app HTML fallback. The share page caught that as a
generic fetch failure and rendered “This replay is no longer available,”
even though the backend replay record existed.

## Test plan
- [x] `pnpm exec vitest run --config ./vitest.config.mts
tests/unit/lib/api/chat-replay-server.unit.spec.ts
tests/unit/lib/api/chat-replay-api.unit.spec.ts`
- [x] `pnpm exec eslint 'src/app/share/[shareId]/page.tsx'
src/lib/api/chat-replay-server.ts
tests/unit/lib/api/chat-replay-server.unit.spec.ts --quiet`\n- [x] `pnpm
exec tsc --noEmit`\n- [x] commit hook frontend lint\n

---

### PR Description

## Summary
- Route public replay share SSR through claw-interface directly instead of self-fetching the public `/api` route.
- Preserve unavailable UI only for backend 404/revoked shares; surface other upstream or routing failures through the error boundary.
- Add unit coverage for backend URL encoding, CF Access headers, 404 handling, non-JSON HTML fallback, and abort signals.

## Root cause
Staging Worker SSR fetches to its own custom domain `/api/chat-replays/:id` could resolve through Cloudflare zone routing and return the app HTML fallback. The share page caught that as a generic fetch failure and rendered “This replay is no longer available,” even though the backend replay record existed.

## Test plan
- [x] `pnpm exec vitest run --config ./vitest.config.mts tests/unit/lib/api/chat-replay-server.unit.spec.ts tests/unit/lib/api/chat-replay-api.unit.spec.ts`
- [x] `pnpm exec eslint 'src/app/share/[shareId]/page.tsx' src/lib/api/chat-replay-server.ts tests/unit/lib/api/chat-replay-server.unit.spec.ts --quiet`\n- [x] `pnpm exec tsc --noEmit`\n- [x] commit hook frontend lint\n
```
