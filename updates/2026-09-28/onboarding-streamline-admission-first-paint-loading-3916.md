---
title: "打开或刷新工作区更快了：去掉多出来的一屏订阅检查，首屏立刻播 Logo 加载动画"
type: "Improvement"
priority: "中"
date: "2026-09-28"
status: "待审核"
channels: ""
---

# 打开或刷新工作区更快了：去掉多出来的一屏订阅检查，首屏立刻播 Logo 加载动画

## 核心宣传点

以前打开或刷新工作区页面时，会先插一屏独立的订阅检查界面，而且页面自己的请求要等检查跑完才开始发，体感就是白屏加等待叠在一起。这次只把检查收缩到真正需要权益的功能路由上——Agents、聊天、任务、成果、Agent Builder、首页、Mini Chat、Agent 管理、知识库、定时任务、技能、插件、集成与渠道（含子页面），而个人资料、组织与账号设置、订阅购买与支付返回页保留原有的登录校验、不再套结账门禁。已审计过的独立数据读取现在和校验并行，不再串行等待。加载态复用原来的全页 Logo 动画，但动画改由 CSS 驱动 SVG，在应用脚本初始化、window.load 触发之前的第一帧就开始转，水合后动画连续不跳。加载中依然可以直接退出登录或手动重试。纯前端改动。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary

Opening or refreshing workspace pages currently adds a separate subscription-check screen and delays page requests until admission completes. This frontend-only change limits the check to workspace capability routes, plays the existing Logo animation from first paint and overlaps independent, audited reads with verification.

- Check Agents, Chat, Tasks, Assets, Agent Builder, Home, Mini Chat, agent management, knowledge base, schedules, skills, plugins, integrations and channels (including descendants). Profile, organization/account settings, subscription purchase and return routes keep their existing authentication checks without the checkout gate.
- `/claw-settings` is a legacy redirect to `/identity`, not a separately protected settings screen. The `/identity` hub remains exempt from checkout admission, including its General, Usage, Billing and visible API Keys tabs, plus legacy Status/Sessions/Statistics tabs when enabled. Existing authentication, organization access and feature visibility still apply. Its old connector/channel/knowledge-base tabs redirect to protected Plugins/Channels destinations.
- Reuse the existing full-page ClawSpinner, with immediate sign-out and manual retry. The same Logo brush geometry and timing now run through CSS on SVG segments, so the first paint animates before application scripts initialize or window.load fires. Hydration retains that animation instead of replacing a static mark. Theme color and reduced-motion preferences remain supported. No new workspace skeleton. Protected content, runtime initialization, session creation and package installation remain behind successful admission.
- Preload Agent capability, the requested Agent definition or the first Artifact Library page while account verification runs. Start organization-scoped Agent/Home definition queries once the verified account is available, overlapping any remaining order verification. Page hooks and preloads share query options, keys, in-flight work, freshness and retry policies.
- Do not speculatively call `GET /agents`: that existing backend handler can repair the default Agent. Tasks/Chat runtime reads therefore remain gated. Only the requested route is prepared; anonymous visitors, exempt routes and already-denied/error states do not start speculative reads.
- Share account results with the session gate and reuse positive admission in UID-scoped memory for 30 seconds. Stale navigation revalidates in the background. Transient admission failures retry twice with short backoff, then recover every 15 seconds/on reconnect. Negative results/auth rejection still block access; explicit checkout completion still forces a fresh verification. No payment-evidence rules or backend files change.

## Validation

- Browser follow-up for Claude’s recovery concern: force `/account/me` to return 503 until the real AuthManager account-confirmation failure is observed, hold successful reads, then release server account truth. All three cases pass: completed + admitted enters Agents and navigates to Tasks without an onboarding flash; incomplete + admitted stays in onboarding despite stale completed browser progress; completed + unpaid stays gated. Both gated cases can advance through the welcome screen without mounting the workspace or issuing runtime initialization, order creation or account-completion writes. Auth bootstrap, provider, resolver and admission service run unmodified.
- Negative control: temporarily removing the account-completion fallback makes the first two browser cases fail. Restoring the original source makes the full 13-case suite pass (48.1s). The committed follow-up changes only E2E coverage; TypeScript, ESLint and frontend governance pass.
- Latest commit `957e6be2c`: CI settled with 23 passing checks and no failures; code-scanning alerts for the PR merge ref are empty. Both Codex and Claude now return APPROVE with no findings. Claude explicitly confirms the new browser coverage addresses the previous bootstrap-recovery validation gap.
- Review follow-up: 128 targeted tests pass across billing, admission service and hook suites, including 33 new cases that run the real HTTP adapter → billing result conversion → admission service → React Query policy. Only fetch/account/auth are mocked. Personal order history, team order history and enterprise credits all cover 503/429/network retries, background retry exhaustion and 15-second recovery, timeout recovery without immediate repeats, 401/403/plain-error/business-error blocking, and legacy status-bearing failure envelopes.
- 25 targeted spinner/admission component tests pass. The earlier admission/preload implementation also passed 387 relevant unit cases across 23 suites. These animation/preload results precede the latest billing error-propagation fix.
- All 13 local Playwright cases pass on the current tree (including the three bootstrap-recovery cases below): desktop/mobile refresh, paid navigation without a loading flash, unpaid/anonymous protection, automatic retry recovery, exempt Profile to protected Home navigation, and held account/order responses proving parallel reads without premature protected DOM/runtime requests or duplicate page reads.
- The new first-paint test holds application scripts, verifies changing brush frames before document load, then releases scripts and confirms the same SVG remains mounted and animated while account verification is held. Reduced-motion presentation works before hydration as well.
- TypeScript, full frontend ESLint, the Knip dead-code gate, frontend governance and diff checks pass. The existing cache-governance guard reports its baseline bootstrap skip.
- Verification uses local mock accounts. No live Stripe payment, production latency benchmark or deployment; genuine account/organization dependencies still apply.

## Review notes

Tim’s [P2 on lost billing error categories](https://github.com/SerendipityOneInc/ecap-workspace/pull/3916#issuecomment-5873907605) is fixed: billing results retain the original client-side error, and admission rethrows it or reconstructs `ApiError` from legacy status/code fields. This preserves HTTP, network and timeout classification without treating ordinary errors as transient. Existing non-throwing billing consumers keep their result contract. The new regression suite reproduced 21 failures before the fix; all 33 cases now pass. No backend or payment-evidence changes.

The legacy `/claw-settings` allowlist entry remains unchanged. Middleware redirects it to the intentionally exempt `/identity` route before rendering, so removing that entry would not change current access or loading behavior. The actual route behavior is documented above; this non-blocking cleanup suggestion is outside the animation correction.

Claude’s [bootstrap-recovery validation gap](https://github.com/SerendipityOneInc/ecap-workspace/pull/3916#issuecomment-5874198853) is now covered by three real-browser scenarios plus a negative control, described above. They verify the intended product behavior: recovered server completion avoids restarting onboarding for an admitted returning user, explicit incomplete accounts still require onboarding, and completed onboarding never replaces admission evidence. No product or backend changes were needed.

The latest Claude review also notes the intentional conservative treatment of legacy failure envelopes without an original error or HTTP status: these remain blocking and do not automatically retry. This is covered by the business-failure tests and preserves Tim’s request not to classify all ordinary errors as transient; no change is warranted.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `2cdfd5ce9ee4d5d11d01fb37c803df2d52702229`
- PR: #3916
- 作者：ericma-srp
- 日期：2026-09-28T23:57:38Z

### Commit Message

```
fix(onboarding): streamline admission and animate loading from first paint (#3916)

## Summary

Opening or refreshing workspace pages currently adds a separate
subscription-check screen and delays page requests until admission
completes. This frontend-only change limits the check to workspace
capability routes, plays the existing Logo animation from first paint
and overlaps independent, audited reads with verification.

- Check Agents, Chat, Tasks, Assets, Agent Builder, Home, Mini Chat,
agent management, knowledge base, schedules, skills, plugins,
integrations and channels (including descendants). Profile,
organization/account settings, subscription purchase and return routes
keep their existing authentication checks without the checkout gate.
- `/claw-settings` is a legacy redirect to `/identity`, not a separately
protected settings screen. The `/identity` hub remains exempt from
checkout admission, including its General, Usage, Billing and visible
API Keys tabs, plus legacy Status/Sessions/Statistics tabs when enabled.
Existing authentication, organization access and feature visibility
still apply. Its old connector/channel/knowledge-base tabs redirect to
protected Plugins/Channels destinations.
- Reuse the existing full-page ClawSpinner, with immediate sign-out and
manual retry. The same Logo brush geometry and timing now run through
CSS on SVG segments, so the first paint animates before application
scripts initialize or window.load fires. Hydration retains that
animation instead of replacing a static mark. Theme color and
reduced-motion preferences remain supported. No new workspace skeleton.
Protected content, runtime initialization, session creation and package
installation remain behind successful admission.
- Preload Agent capability, the requested Agent definition or the first
Artifact Library page while account verification runs. Start
organization-scoped Agent/Home definition queries once the verified
account is available, overlapping any remaining order verification. Page
hooks and preloads share query options, keys, in-flight work, freshness
and retry policies.
- Do not speculatively call `GET /agents`: that existing backend handler
can repair the default Agent. Tasks/Chat runtime reads therefore remain
gated. Only the requested route is prepared; anonymous visitors, exempt
routes and already-denied/error states do not start speculative reads.
- Share account results with the session gate and reuse positive
admission in UID-scoped memory for 30 seconds. Stale navigation
revalidates in the background. Transient admission failures retry twice
with short backoff, then recover every 15 seconds/on reconnect. Negative
results/auth rejection still block access; explicit checkout completion
still forces a fresh verification. No payment-evidence rules or backend
files change.

## Validation

- Browser follow-up for Claude’s recovery concern: force `/account/me`
to return 503 until the real AuthManager account-confirmation failure is
observed, hold successful reads, then release server account truth. All
three cases pass: completed + admitted enters Agents and navigates to
Tasks without an onboarding flash; incomplete + admitted stays in
onboarding despite stale completed browser progress; completed + unpaid
stays gated. Both gated cases can advance through the welcome screen
without mounting the workspace or issuing runtime initialization, order
creation or account-completion writes. Auth bootstrap, provider,
resolver and admission service run unmodified.
- Negative control: temporarily removing the account-completion fallback
makes the first two browser cases fail. Restoring the original source
makes the full 13-case suite pass (48.1s). The committed follow-up
changes only E2E coverage; TypeScript, ESLint and frontend governance
pass.
- Latest commit `957e6be2c`: CI settled with 23 passing checks and no
failures; code-scanning alerts for the PR merge ref are empty. Both
Codex and Claude now return APPROVE with no findings. Claude explicitly
confirms the new browser coverage addresses the previous
bootstrap-recovery validation gap.
- Review follow-up: 128 targeted tests pass across billing, admission
service and hook suites, including 33 new cases that run the real HTTP
adapter → billing result conversion → admission service → React Query
policy. Only fetch/account/auth are mocked. Personal order history, team
order history and enterprise credits all cover 503/429/network retries,
background retry exhaustion and 15-second recovery, timeout recovery
without immediate repeats, 401/403/plain-error/business-error blocking,
and legacy status-bearing failure envelopes.
- 25 targeted spinner/admission component tests pass. The earlier
admission/preload implementation also passed 387 relevant unit cases
across 23 suites. These animation/preload results precede the latest
billing error-propagation fix.
- All 13 local Playwright cases pass on the current tree (including the
three bootstrap-recovery cases below): desktop/mobile refresh, paid
navigation without a loading flash, unpaid/anonymous protection,
automatic retry recovery, exempt Profile to protected Home navigation,
and held account/order responses proving parallel reads without
premature protected DOM/runtime requests or duplicate page reads.
- The new first-paint test holds application scripts, verifies changing
brush frames before document load, then releases scripts and confirms
the same SVG remains mounted and animated while account verification is
held. Reduced-motion presentation works before hydration as well.
- TypeScript, full frontend ESLint, the Knip dead-code gate, frontend
governance and diff checks pass. The existing cache-governance guard
reports its baseline bootstrap skip.
- Verification uses local mock accounts. No live Stripe payment,
production latency benchmark or deployment; genuine account/organization
dependencies still apply.

## Review notes

Tim’s [P2 on lost billing error
categories](https://github.com/SerendipityOneInc/ecap-workspace/pull/3916#issuecomment-5873907605)
is fixed: billing results retain the original client-side error, and
admission rethrows it or reconstructs `ApiError` from legacy status/code
fields. This preserves HTTP, network and timeout classification without
treating ordinary errors as transient. Existing non-throwing billing
consumers keep their result contract. The new regression suite
reproduced 21 failures before the fix; all 33 cases now pass. No backend
or payment-evidence changes.

The legacy `/claw-settings` allowlist entry remains unchanged.
Middleware redirects it to the intentionally exempt `/identity` route
before rendering, so removing that entry would not change current access
or loading behavior. The actual route behavior is documented above; this
non-blocking cleanup suggestion is outside the animation correction.

Claude’s [bootstrap-recovery validation
gap](https://github.com/SerendipityOneInc/ecap-workspace/pull/3916#issuecomment-5874198853)
is now covered by three real-browser scenarios plus a negative control,
described above. They verify the intended product behavior: recovered
server completion avoids restarting onboarding for an admitted returning
user, explicit incomplete accounts still require onboarding, and
completed onboarding never replaces admission evidence. No product or
backend changes were needed.

The latest Claude review also notes the intentional conservative
treatment of legacy failure envelopes without an original error or HTTP
status: these remain blocking and do not automatically retry. This is
covered by the business-failure tests and preserves Tim’s request not to
classify all ordinary errors as transient; no change is warranted.
```

来源：SerendipityOneInc/ecap-workspace @ 2cdfd5ce，PR #3916，作者 ericma-srp。
