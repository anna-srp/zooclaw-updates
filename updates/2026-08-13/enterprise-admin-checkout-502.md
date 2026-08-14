---
title: "修复：企业管理后台用信用卡结算时报错打不开"
type: "Bug Fix"
priority: "中"
date: "2026-08-13"
status: "待审核"
channels: ""
---

## 核心宣传点

修复企业管理后台在信用卡支付或订阅处于人工审核状态时页面报错、结算页提示「无法开始结算」的问题，现在可以正常进入付款流程。

## 原始内容

仓库：SerendipityOneInc/ecap-workspace
commit：d0368608ccc089dd67079411c8e0788484fd862c
作者：tim-srp
日期：2026-08-13T12:14:57Z

**Commit message**

```
fix(enterprise-admin): accept card channel and manual-review status in auth/me (#3373)

<!-- PR 标题：fix(enterprise-admin): accept card channel and manual-review
status in auth/me -->

## Summary
- Enterprise Admin `/api/auth/me` 返回 502 的场景:用户通过 Creem
银行卡(Card)支付后,`GET /account/me` 返回 `payment_channel: "card"`;或订阅处于人工审核时返回
`subscription_status: "manual_review"`。前端 zod 契约只允许
`stripe/antom/apple/offline` 和旧的 subscription status 集合,校验失败后 BFF 兜底成
502,checkout 页面错误显示 "We couldn't start checkout"。
- 修复:`types/user-me.ts` 两个枚举对齐后端 `UserMeResponse` Literal(`card` +
`manual_review`),并补契约测试(客户端登录流 + BFF 路由两层)。

## Root cause
- `account_api.py` 的 `UserMeResponse`(后端契约)已支持 `payment_channel:
"card"`(Creem card checkout 的 `creem → "card"` 映射在 `order_requests.py` /
`billing_summary/adapters.py`,均为 main 上已有行为)和 `subscription_status:
"manual_review"`。
- enterprise-admin 的 zod schema(`types/user-me.ts`)未跟随该契约更新;ZodError 无
HTTP status,`app/api/auth/me/route.ts` catch 后兜底返回 502。
- web/app(main app)的模型已包含 `"card"`,仅 enterprise-admin 遗漏。

## Test plan
- [x] `pnpm test`:52 files / 375 tests 通过(含新增 3 个契约用例)
- [x] `pnpm run lint`、`pnpm exec tsc --noEmit` 通过
- [x] 新增用例:
- 客户端 `completeLogin`:`payment_channel: "card"` / `subscription_status:
"manual_review"` 解析成功
  - BFF `GET /api/auth/me`:claw 返回上述字段时响应 200(而非 502)

Co-authored-by: Claude <noreply@anthropic.com>
```

**PR #3373 body**

<!-- PR 标题：fix(enterprise-admin): accept card channel and manual-review status in auth/me -->

## Summary
- Enterprise Admin `/api/auth/me` 返回 502 的场景:用户通过 Creem 银行卡(Card)支付后,`GET /account/me` 返回 `payment_channel: "card"`;或订阅处于人工审核时返回 `subscription_status: "manual_review"`。前端 zod 契约只允许 `stripe/antom/apple/offline` 和旧的 subscription status 集合,校验失败后 BFF 兜底成 502,checkout 页面错误显示 "We couldn't start checkout"。
- 修复:`types/user-me.ts` 两个枚举对齐后端 `UserMeResponse` Literal(`card` + `manual_review`),并补契约测试(客户端登录流 + BFF 路由两层)。

## Root cause
- `account_api.py` 的 `UserMeResponse`(后端契约)已支持 `payment_channel: "card"`(Creem card checkout 的 `creem → "card"` 映射在 `order_requests.py` / `billing_summary/adapters.py`,均为 main 上已有行为)和 `subscription_status: "manual_review"`。
- enterprise-admin 的 zod schema(`types/user-me.ts`)未跟随该契约更新;ZodError 无 HTTP status,`app/api/auth/me/route.ts` catch 后兜底返回 502。
- web/app(main app)的模型已包含 `"card"`,仅 enterprise-admin 遗漏。

## Test plan
- [x] `pnpm test`:52 files / 375 tests 通过(含新增 3 个契约用例)
- [x] `pnpm run lint`、`pnpm exec tsc --noEmit` 通过
- [x] 新增用例:
  - 客户端 `completeLogin`:`payment_channel: "card"` / `subscription_status: "manual_review"` 解析成功
  - BFF `GET /api/auth/me`:claw 返回上述字段时响应 200(而非 502)


