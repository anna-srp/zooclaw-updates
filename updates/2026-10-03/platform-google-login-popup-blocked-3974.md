---
title: "修复：手机 Safari 上第一次点开发者平台的 Google 登录不再被浏览器拦掉弹窗"
type: "Bug Fix"
priority: "中"
date: "2026-10-03"
status: "待审核"
channels: ""
---

# 修复：手机 Safari 上第一次点开发者平台的 Google 登录不再被浏览器拦掉弹窗

## 核心宣传点

开发者平台以前是在你第一次点「用 Google 登录」时才初始化登录组件，在手机 Safari 上这个初始化会把这次点击的「用户操作授权」消耗掉，等到真要弹窗时浏览器已经不认了，第一次点击经常直接报弹窗被拦截，得再点一次才行。现在登录页一加载就先把 Google 登录准备好，准备完成后才把 Google 按钮点亮；准备期间邮箱登录照常可用，所以不会卡住你。如果准备失败或者超过 10 秒还没好，页面会提示改用邮箱登录或刷新；要是之后准备又成功了，提示会自动消失、Google 按钮恢复可点。点击本身仍然直接触发弹窗，不会在点击里再等一次，所以不会重新踩到同一个坑。现有的登录态保持、多标签页恢复、重复登录拦截和登录后跳回原页面都没有改动。本次只覆盖开发者平台的登录页，ZooWork 主站那边的同类修复在 #3983 单独合过了。

## 分级

- 内部：P2
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `27fb5cb71056e6a23959055b64e2466157ece173`
- PR: #3974
- 作者：finn-srp
- 日期：2026-10-03T08:26:40Z

### Commit Message

```
fix(platform): initialize Google auth before login clicks (#3974)

Platform initializes Firebase on the first Google click. On mobile
Safari, initialization can consume the click's transient user activation
before Firebase opens the popup, producing `auth/popup-blocked` on the
first attempt.

Prepare Firebase when the standalone Platform sign-in form mounts, then
enable Google only after `authStateReady()` resolves. Email remains
available during preparation. Preparation errors and a 10-second delay
show an email/reload fallback; a late successful preparation clears the
fallback and enables Google.

The click still invokes `signInWithPopup` directly, without waiting for
preparation inside the handler. Retain current HttpOnly Cookie sessions,
cross-tab recovery, focus/login guards, and protected-route
continuation. Update Preview auth and regression fixtures to the current
Cookie flow.

Scope: `web/platform`. The WebApp counterpart in `web/app` was merged
separately in #3983.

## Validation

- Node 24: `pnpm lint`, `pnpm typecheck`, `pnpm test` (194 tests in 22
suites), and `pnpm build` passed after integrating current main.
- Regression coverage verifies preparation before clicks, disabled
clicks while pending, Firebase token exchange into the Cookie session
flow, email fallback on failure/delay, and recovery after delayed
preparation.
- Existing persistent-session, focus/login, and route-continuation tests
pass.
- The new delay regression failed before the fallback was added, then
passed.
- Tests mock Firebase and Account responses. Real-device OAuth
authorization and the live callback/session exchange remain unverified.
```

来源：SerendipityOneInc/ecap-workspace @ 27fb5cb7，PR #3974，作者 finn-srp。
