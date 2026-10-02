---
title: "定价页新增「Building with APIs?」入口，可直接跳转 Managed Agent API 充值"
type: "新功能"
priority: "中"
date: "2026-10-01"
status: "待审核"
channels: "Discord+changelog"
---

# 定价页新增「Building with APIs?」入口，可直接跳转 Managed Agent API 充值

## 核心宣传点

定价页在 Pro 和 Enterprise 对比之上新增了一块独立的「Building with APIs?」说明区，「Explore Managed Agent API」按钮走共享的平台地址常量，点击后直接打开平台的充值页（带 addFunds=1）。未登录访问也能看到这个入口，面向 API 开发者的分流路径更清楚。

## 分级

- 内部：P2
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary

- Add a separate “Building with APIs?” callout above the Pro and Enterprise comparison. “Explore Managed Agent API” uses the shared Platform host constant and opens billing with `addFunds=1`.
- Signed-out visitors see Platform login first, then email or Google sign-in continues to billing and opens the existing Add funds dialog. Preserve the requested path, query and hash in router history state, including session restoration after a refresh. One shared resolver restricts return destinations to internal `/settings` routes; ordinary homepage sign-in still opens API keys. Once explicit sign-out deletes the session cookie, the auth provider marks the logout and the route guard clears the previous destination, including a later Firebase cleanup rejection. A failed cookie deletion stays on the current page; the login route also clears any existing target before rendering sign-in, so a refresh cannot resurrect it. The existing cross-tab revision notification now distinguishes sign-in/sign-out using only an event type and random revision. Receiving tabs clear old protected URLs before session recovery; the logout marker resets only when a new session is verified or published, including rapid account replacement. Legacy revision consumers remain compatible. Billing permissions and readiness continue to gate the dialog, and navigation creates no top-up order.
- Center the pricing hero, use the final audience copy (“Flexible plans for domain experts and enterprises, with API pricing for FDEs.”), enlarge the subtitle and API callout text, and keep equal spacing above and below the callout. Preserve the original subscription cards and Custom Pricing label; update the comparison heading and Enterprise tagline.
- Update all 10 supported locales, preserving the supplied FDE terminology. The marketing web and Platform frontends both need deployment; no backend or payment-processing changes.

## Product contract

The product owner explicitly requested the final CTA wording **Explore Managed Agent API** on 2026-10-02 and required translation into all supported languages. This is the accepted product decision, including the existing Platform billing/Add funds destination described below. The product owner also directed follow-up review fixes to address technical implementation issues while preserving the confirmed product design.

Product-owner instruction: “按钮你从view api pricing，改为 Explore Managed Agent API 注意翻译成各国语言。”

“Explore Managed Agent API” opens Platform billing with the existing Add funds amount chooser. Signed-out visitors log in first and continue to the same destination. Opening the page or chooser does not create a top-up or Stripe Checkout; only explicit “Buy Credits” confirmation creates the order. Billing permissions and wallet readiness remain mandatory.

## Test plan

- [x] Web governance guards, TypeScript and ESLint; Platform TypeScript, changed-file ESLint and production build.
- [x] Latest CTA copy: all 10 supported locales translated, with 54 marketing entry/locale-completeness tests passing. The full 185-test Platform suite passed for the authentication changes. Router regressions reproduce the review findings, then cover email sign-in, Google sign-in, refreshed-session continuation, ordinary homepage sign-in, explicit sign-out followed by a different account signing in through either method, cookie-deletion failure, Firebase cleanup failure after local logout, reset of the explicit-logout marker on a new login, login-page target clearing before refresh/re-login, and zero top-up POSTs. Integrated regressions use the real auth provider and router with mocked account/session boundaries to cover cross-tab logout, email re-login, incoming replacement sessions, and replacement before or during restoration. Notification tests cover event types and unique revisions without credentials. Destination tests reject external and malformed return targets. Existing router cases exercise the exact `?addFunds=1` URL without billing permission and while initialization is pending, and assert that the chooser remains closed; billing failure also preserves history without creating Checkout.
- [x] Local browser preview with mock auth/data: email sign-in, Google sign-in and restored-session continuation all open Add funds on billing and clear the return state. Account-menu sign-out followed by mock Google sign-in reaches API keys with no saved target or Add funds dialog. Production authentication and payment were not exercised.
- [x] Pricing layout checked at 1440×900, 375×667 and 320×568; equal callout spacing, visible API entry and no horizontal overflow. Sampled English, Chinese and French layouts. After the CTA rename, all 10 locales were browser-checked at 375×667 with a fully visible API button and no horizontal/text overflow; English desktop at 1440×900 and English/German at 320×568 were also checked. Fresh Arabic RTL browser checks at 1440×900 and 375×667 confirm `lang=ar`, `dir=rtl`, correct CTA direction, first-screen visibility, and no horizontal/text overflow.

The full marketing web suite and build run in CI.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `82dd578cd98730fb24ee141643e7082e515363b4`
- PR: #3994
- 作者：ericma-srp
- 日期：2026-10-01T20:07:33Z

### Commit Message

```
feat(pricing): add Managed Agent API pricing entry (#3994)

## Summary

- Add a separate “Building with APIs?” callout above the Pro and
Enterprise comparison. “Explore Managed Agent API” uses the shared
Platform host constant and opens billing with `addFunds=1`.
- Signed-out visitors see Platform login first, then email or Google
sign-in continues to billing and opens the existing Add funds dialog.
Preserve the requested path, query and hash in router history state,
including session restoration after a refresh. One shared resolver
restricts return destinations to internal `/settings` routes; ordinary
homepage sign-in still opens API keys. Once explicit sign-out deletes
the session cookie, the auth provider marks the logout and the route
guard clears the previous destination, including a later Firebase
cleanup rejection. A failed cookie deletion stays on the current page;
the login route also clears any existing target before rendering
sign-in, so a refresh cannot resurrect it. The existing cross-tab
revision notification now distinguishes sign-in/sign-out using only an
event type and random revision. Receiving tabs clear old protected URLs
before session recovery; the logout marker resets only when a new
session is verified or published, including rapid account replacement.
Legacy revision consumers remain compatible. Billing permissions and
readiness continue to gate the dialog, and navigation creates no top-up
order.
- Center the pricing hero, use the final audience copy (“Flexible plans
for domain experts and enterprises, with API pricing for FDEs.”),
enlarge the subtitle and API callout text, and keep equal spacing above
and below the callout. Preserve the original subscription cards and
Custom Pricing label; update the comparison heading and Enterprise
tagline.
- Update all 10 supported locales, preserving the supplied FDE
terminology. The marketing web and Platform frontends both need
deployment; no backend or payment-processing changes.

## Product contract

The product owner explicitly requested the final CTA wording **Explore
Managed Agent API** on 2026-10-02 and required translation into all
supported languages. This is the accepted product decision, including
the existing Platform billing/Add funds destination described below. The
product owner also directed follow-up review fixes to address technical
implementation issues while preserving the confirmed product design.

Product-owner instruction: “按钮你从view api pricing，改为 Explore Managed
Agent API 注意翻译成各国语言。”

“Explore Managed Agent API” opens Platform billing with the existing Add
funds amount chooser. Signed-out visitors log in first and continue to
the same destination. Opening the page or chooser does not create a
top-up or Stripe Checkout; only explicit “Buy Credits” confirmation
creates the order. Billing permissions and wallet readiness remain
mandatory.

## Test plan

- [x] Web governance guards, TypeScript and ESLint; Platform TypeScript,
changed-file ESLint and production build.
- [x] Latest CTA copy: all 10 supported locales translated, with 54
marketing entry/locale-completeness tests passing. The full 185-test
Platform suite passed for the authentication changes. Router regressions
reproduce the review findings, then cover email sign-in, Google sign-in,
refreshed-session continuation, ordinary homepage sign-in, explicit
sign-out followed by a different account signing in through either
method, cookie-deletion failure, Firebase cleanup failure after local
logout, reset of the explicit-logout marker on a new login, login-page
target clearing before refresh/re-login, and zero top-up POSTs.
Integrated regressions use the real auth provider and router with mocked
account/session boundaries to cover cross-tab logout, email re-login,
incoming replacement sessions, and replacement before or during
restoration. Notification tests cover event types and unique revisions
without credentials. Destination tests reject external and malformed
return targets. Existing router cases exercise the exact `?addFunds=1`
URL without billing permission and while initialization is pending, and
assert that the chooser remains closed; billing failure also preserves
history without creating Checkout.
- [x] Local browser preview with mock auth/data: email sign-in, Google
sign-in and restored-session continuation all open Add funds on billing
and clear the return state. Account-menu sign-out followed by mock
Google sign-in reaches API keys with no saved target or Add funds
dialog. Production authentication and payment were not exercised.
- [x] Pricing layout checked at 1440×900, 375×667 and 320×568; equal
callout spacing, visible API entry and no horizontal overflow. Sampled
English, Chinese and French layouts. After the CTA rename, all 10
locales were browser-checked at 375×667 with a fully visible API button
and no horizontal/text overflow; English desktop at 1440×900 and
English/German at 320×568 were also checked. Fresh Arabic RTL browser
checks at 1440×900 and 375×667 confirm `lang=ar`, `dir=rtl`, correct CTA
direction, first-screen visibility, and no horizontal/text overflow.

The full marketing web suite and build run in CI.
```

来源：SerendipityOneInc/ecap-workspace @ 82dd578c，PR #3994，作者 ericma-srp。
