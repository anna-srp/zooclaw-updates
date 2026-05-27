---
title: "Agent Pack 资源下载安全性修复"
type: "Bug Fix"
priority: "中"
date: "2026-05-26"
status: "待审核"
channels: "Discord + changelog"
---
# Agent Pack 资源下载安全性修复

## 核心宣传点

Agent Pack 中的资源文件下载更安全，经过身份验证才能访问，保障你的内容不被未授权获取。

## 原始内容

**Commit:** 5aa4ad5b
**Repo:** ecap-workspace
**Author:** bill-srp

**Commit Message:**
```
fix(enterprise): authenticate pack asset downloads (#1942)

## Summary
- Change pack submission asset download from direct cross-origin fetch
to a same-origin Next.js API route
- Send the account token to `/api/r2/pack-assets/<asset_id>`; the API
validates it against `/account/me`
- Require the requested R2 key to be under the caller membership org id
before reading from `R2_AGENT_PACKS_BUCKET`
- Stream the ZIP with attachment headers
- Revert pack archive uploads to returning only the internal R2 key, not
a public URL
- Add route coverage for auth rejection, forbidden missing membership,
cross-org rejection, R2 streaming, and 404s

## Root cause
Pack asset downloads require an auth token in the request header. A
direct browser request to `agentpack.zooclaw.ai` would depend on
cross-origin CORS/preflight behavior in deployment. A same-origin API
route is a tighter contract: the browser calls the enterprise admin app,
the app validates auth and org scope, then reads the R2 binding
directly.

## Test plan
- [x] pnpm --dir web/enterprise-admin test
components/packs/__tests__/SubmissionList.test.tsx
app/(dashboard)/packs/[packId]/__tests__/pack-detail-page.test.tsx
lib/r2/__tests__/index.test.ts app/api/r2/upload/__tests__/route.test.ts
app/api/r2/pack-assets/[...key]/__tests__/route.test.ts
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit
- [x] pnpm --dir web/enterprise-admin exec eslint . --max-warnings=0
--cache --cache-location .eslintcache --cache-strategy content
--ignore-pattern coverage
```

**PR #1942: fix(enterprise): authenticate pack asset downloads**

## Summary
- Change pack submission asset download from direct cross-origin fetch to a same-origin Next.js API route
- Send the account token to `/api/r2/pack-assets/<asset_id>`; the API validates it against `/account/me`
- Require the requested R2 key to be under the caller membership org id before reading from `R2_AGENT_PACKS_BUCKET`
- Stream the ZIP with attachment headers
- Revert pack archive uploads to returning only the internal R2 key, not a public URL
- Add route coverage for auth rejection, forbidden missing membership, cross-org rejection, R2 streaming, and 404s

## Root cause
Pack asset downloads require an auth token in the request header. A direct browser request to `agentpack.zooclaw.ai` would depend on cross-origin CORS/preflight behavior in deployment. A same-origin API route is a tighter contract: the browser calls the enterprise admin app, the app validates auth and org scope, then reads the R2 binding directly.

## Test plan
- [x] pnpm --dir web/enterprise-admin test components/packs/__tests__/SubmissionList.test.tsx app/(dashboard)/packs/[packId]/__tests__/pack-detail-page.test.tsx lib/r2/__tests__/index.test.ts app/api/r2/upload/__tests__/route.test.ts app/api/r2/pack-assets/[...key]/__tests__/route.test.ts
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit
- [x] pnpm --dir web/enterprise-admin exec eslint . --max-warnings=0 --cache --cache-location .eslintcache --cache-strategy content --ignore-pattern coverage
