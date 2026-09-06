---
title: "官网首页：已登录用户点 Get Started 时会显示「正在跳转」，不再像是没点上"
type: "体验优化"
priority: "中"
date: "2026-09-05"
status: "待审核"
channels: "Discord+changelog"
---

# 官网首页：已登录用户点 Get Started 时会显示「正在跳转」，不再像是没点上

## 核心宣传点

老用户回到官网首页时，页面会自动帮你跳进工作台，但跳转前要先等账号会话校验完成。以前这段等待是完全没有反馈的：顶部导航和首屏的 Get Started 按钮照旧显示成可点状态，你点一下没动静，就会以为按钮坏了，然后连点好几次。

问题出在首页把这个「跳转进行中」的状态算出来之后又丢掉了，头部和首屏组件根本拿不到。现在这个真实的等待状态被暴露出来并共享给营销页头部：导航栏和首屏第一个 Get Started 会换成本地化的「正在跳转」文案，配一组错峰跳动的小圆点（尊重系统的「减少动态效果」设置，开了这个偏好就不会跳动），同时这两个按钮在跳转期间被置灰不可点。页面下方的其他 CTA 保持原样，不受影响。

## 原始内容

### fix(landing): show redirect progress for returning users (#3643)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `ec0781d6bf9a21e2d5c7636e2048fe501e25967e`
- PR: #3643
- 作者: Nemo Feng
- 日期: 2026-09-05T01:03:54Z

### Commit Message

```
fix(landing): show redirect progress for returning users (#3643)

## Summary

- expose the landing auth redirect's real pending state and share it
with the marketing header
- replace the header and first hero Get Started labels with localized
Redirecting feedback and staggered, reduced-motion-safe dots
- disable both affected CTAs during the handoff while leaving lower-page
CTAs unchanged

## Root cause

The landing redirect waited for account-session validation before
navigating, but its state was discarded by the page orchestrator. The
header and hero therefore kept rendering interactive Get Started buttons
throughout that wait with no indication that navigation was already in
progress.

## Test plan

- [x] `TZ=UTC bash scripts/verify-web.sh` — 689 files, 9,456 tests
passed; TypeScript, ESLint, and governance guards passed
- [x] `TZ=UTC bash scripts/verify-changed.sh`
- [x] focused redirect-hook, landing-client, header, marketing-chrome,
and homepage component tests — 93 passed
- [ ] browser auth-flow smoke test — local checkout does not have the
full auth runtime environment; pending and completed handoffs are
covered by hook and component tests
```

### PR Body

```
## Summary

- expose the landing auth redirect's real pending state and share it with the marketing header
- replace the header and first hero Get Started labels with localized Redirecting feedback and staggered, reduced-motion-safe dots
- disable both affected CTAs during the handoff while leaving lower-page CTAs unchanged

## Root cause

The landing redirect waited for account-session validation before navigating, but its state was discarded by the page orchestrator. The header and hero therefore kept rendering interactive Get Started buttons throughout that wait with no indication that navigation was already in progress.

## Test plan

- [x] `TZ=UTC bash scripts/verify-web.sh` — 689 files, 9,456 tests passed; TypeScript, ESLint, and governance guards passed
- [x] `TZ=UTC bash scripts/verify-changed.sh`
- [x] focused redirect-hook, landing-client, header, marketing-chrome, and homepage component tests — 93 passed
- [ ] browser auth-flow smoke test — local checkout does not have the full auth runtime environment; pending and completed handoffs are covered by hook and component tests

```
