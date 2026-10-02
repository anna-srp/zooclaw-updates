---
title: "修复：iOS 上的 Google 登录不再失效，Firebase 就绪后才放开按钮"
type: "Bug Fix"
priority: "高"
date: "2026-10-01"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：iOS 上的 Google 登录不再失效，Firebase 就绪后才放开按钮

## 核心宣传点

修复了 WebApp 在 iOS 上的 Google 登录路径：登录表单挂载时会先等 Firebase 的 authStateReady() 完成，准备好之后才启用 Google 按钮；iPhone 和 iPad 改用由点击直接触发的 popup，避免被浏览器拦截。准备失败时会显示提示，邮箱和手机登录照常可用。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary

修复 webapp 在 iOS 上的 Google 登录路径：登录表单挂载时等待 Firebase `authStateReady()`，准备完成后才启用 Google 按钮；iPhone/iPad 改用直接由点击触发的 popup。准备失败时显示提示，邮箱与手机登录继续可用。

Prepare Firebase before enabling Google sign-in and use the existing popup/token-exchange flow on iOS. Apply the readiness state to the default, landing, and legacy Platform login forms. Preserve Android redirect behavior and existing session-reset/profile-persistence safeguards.

## Root cause

当前 webapp 将 iOS 导向 `signInWithRedirect`，该流程可能受 Safari 的跨域存储限制影响。直接切换 popup 仍需处理首次初始化耗时：Firebase 在 Safari 上会提前初始化 popup resolver，等待这一步完成后再允许点击，可以避免初始化消耗点击的 transient user activation。点击 handler 内不再等待准备过程。

The existing mobile branch sends iOS through Firebase redirect sign-in, which is sensitive to third-party storage restrictions. This adopts the preparation approach from Finn's #3974: finish Firebase startup before the click, then invoke `signInWithPopup` directly from the click handler. Firebase token exchange and profile persistence still use the existing desktop path.

References: #3974 (Platform popup initialization), #3972 (separate first-party auth-domain approach for redirects).

## Test plan

- [x] 231 targeted tests passed across 7 suites: login form, redirect completion, login modal, app-shell auth, standalone login page, landing login modal, and auth manager.
- [x] New preparation and iPhone/iPad popup regression cases failed against the original implementation, then passed with the fix.
- [x] `bash scripts/verify-web.sh --no-test src/components/LoginForm.tsx src/components/login/PlatformLoginFields.tsx src/locales/en.ts src/locales/zh.ts tests/unit/components/LoginForm.unit.spec.tsx` — TypeScript, ESLint, and governance checks passed.
- [x] `git diff --check`.
- [ ] Real-device iOS Google authorization and callback/session acceptance test. Unit tests stub Firebase; this PR does not claim a completed live OAuth round trip.

仅需 web 部署。No backend changes or auth-domain configuration changes.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `ef3b0f9ccd69446d5290e18d0d2fc0c59764743e`
- PR: #3983
- 作者：david-srp
- 日期：2026-10-01T12:17:24Z

### Commit Message

```
fix(web): 修复 iOS Google 登录 / prepare Google sign-in on iOS (#3983)

## Summary

修复 webapp 在 iOS 上的 Google 登录路径：登录表单挂载时等待 Firebase
`authStateReady()`，准备完成后才启用 Google 按钮；iPhone/iPad 改用直接由点击触发的
popup。准备失败时显示提示，邮箱与手机登录继续可用。

Prepare Firebase before enabling Google sign-in and use the existing
popup/token-exchange flow on iOS. Apply the readiness state to the
default, landing, and legacy Platform login forms. Preserve Android
redirect behavior and existing session-reset/profile-persistence
safeguards.

## Root cause

当前 webapp 将 iOS 导向 `signInWithRedirect`，该流程可能受 Safari 的跨域存储限制影响。直接切换
popup 仍需处理首次初始化耗时：Firebase 在 Safari 上会提前初始化 popup
resolver，等待这一步完成后再允许点击，可以避免初始化消耗点击的 transient user activation。点击 handler
内不再等待准备过程。

The existing mobile branch sends iOS through Firebase redirect sign-in,
which is sensitive to third-party storage restrictions. This adopts the
preparation approach from Finn's #3974: finish Firebase startup before
the click, then invoke `signInWithPopup` directly from the click
handler. Firebase token exchange and profile persistence still use the
existing desktop path.

References: #3974 (Platform popup initialization), #3972 (separate
first-party auth-domain approach for redirects).

## Test plan

- [x] 231 targeted tests passed across 7 suites: login form, redirect
completion, login modal, app-shell auth, standalone login page, landing
login modal, and auth manager.
- [x] New preparation and iPhone/iPad popup regression cases failed
against the original implementation, then passed with the fix.
- [x] `bash scripts/verify-web.sh --no-test src/components/LoginForm.tsx
src/components/login/PlatformLoginFields.tsx src/locales/en.ts
src/locales/zh.ts tests/unit/components/LoginForm.unit.spec.tsx` —
TypeScript, ESLint, and governance checks passed.
- [x] `git diff --check`.
- [ ] Real-device iOS Google authorization and callback/session
acceptance test. Unit tests stub Firebase; this PR does not claim a
completed live OAuth round trip.

仅需 web 部署。No backend changes or auth-domain configuration changes.
```

来源：SerendipityOneInc/ecap-workspace @ ef3b0f9c，PR #3983，作者 david-srp。
