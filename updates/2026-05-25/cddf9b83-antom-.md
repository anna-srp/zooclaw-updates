---
title: "修复 Antom 支付跳转地址错误"
type: "Bug Fix"
priority: "中"
date: "2026-05-25"
status: "待审核"
channels: ""
---

# 修复 Antom 支付跳转地址错误

## 核心宣传点

修复支付完成后可能跳转到错误地址的问题，确保支付回调正常

## 原始内容

**仓库**: SerendipityOneInc/ecap-workspace  
**Commit**: cddf9b83eb27d309e3e843b4a8d4714a692aa7a8  
**作者**: kaka-srp  
**日期**: 2026-05-25T07:15:31Z  

**Commit Message**:

```
fix(web): use canonical origin for Antom redirects (#1910)

## Summary
- Use configured `NEXT_PUBLIC_SITE_URL` as the canonical Antom
success/cancel redirect origin.
- Keep request `Origin` as a local/dev fallback when no canonical site
URL is configured.
- Add unit coverage for `www.zooclaw.ai` requests producing `zooclaw.ai`
redirect URLs.

## Root cause
The Antom BFF built redirect URLs directly from the browser `Origin`
header. Requests from `https://www.zooclaw.ai` therefore sent
`www.zooclaw.ai` to claw-interface, whose redirect-host allowlist only
includes configured canonical frontend/backend hosts, so it rejected the
request before reaching Antom.

## Test plan
- [x] `git diff --check --
web/app/src/app/api/antom/create-payment/route.ts
web/app/tests/unit/app/api/antom-create-payment.unit.spec.ts`
- [ ] Not run: web unit tests require installing `web/node_modules`;
install was stopped per request because local dependency download was
too slow and space-heavy.
```

**PR Description**:

## Summary
- Use configured `NEXT_PUBLIC_SITE_URL` as the canonical Antom success/cancel redirect origin.
- Keep request `Origin` as a local/dev fallback when no canonical site URL is configured.
- Add unit coverage for `www.zooclaw.ai` requests producing `zooclaw.ai` redirect URLs.

## Root cause
The Antom BFF built redirect URLs directly from the browser `Origin` header. Requests from `https://www.zooclaw.ai` therefore sent `www.zooclaw.ai` to claw-interface, whose redirect-host allowlist only includes configured canonical frontend/backend hosts, so it rejected the request before reaching Antom.

## Test plan
- [x] `git diff --check -- web/app/src/app/api/antom/create-payment/route.ts web/app/tests/unit/app/api/antom-create-payment.unit.spec.ts`
- [ ] Not run: web unit tests require installing `web/node_modules`; install was stopped per request because local dependency download was too slow and space-heavy.
