---
title: "修复：手机浏览器打开登录页不再上下跳动、露出黑色背景"
type: "Bug Fix"
priority: "中"
date: "2026-10-01"
status: "待审核"
channels: ""
---

# 修复：手机浏览器打开登录页不再上下跳动、露出黑色背景

## 核心宣传点

WebApp 和开发者平台的登录页在手机浏览器里会随视口变化上下跳动、顶部不好返回，还会露出黑色背景。现在移动端改为顶部自然排列并使用稳定的 svh 最小高度，保留整页原生滚动；桌面端仍是双栏居中。白色画布也只作用在独立登录路由上，不影响其他页面。

## 分级

- 内部：P2
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary / 改动
- 修复 Web App 与 Platform 登录页在手机浏览器中随视口变化上下跳动、顶部不易返回及露出黑色背景的问题。移动端采用顶部自然排列和稳定的 `svh` 最小高度，保留整页原生滚动；桌面保留双栏居中。
- Stabilize both mobile login layouts and scope the white document canvas to the standalone login route. Authentication behavior is unchanged; the selected theme returns when leaving login.

## Root cause / 原因
动态视口高度配合垂直居中会在地址栏伸缩时移动内容；Platform 外层仍使用 `100vh`，与登录容器高度不一致；两端登录页外层还会继承深色背景。The fix removes mobile recentering and aligns the login document canvas without introducing scroll locks or viewport JavaScript.

## Test plan / 验证
- [x] Web App governance guards, TypeScript, login-related tests, targeted ESLint, and pre-commit full ESLint.
- [x] Platform TypeScript, 22 login/theme tests, and targeted ESLint.
- [x] Chromium mobile widths 320 / 393 / 430 and landscape 844; viewport heights 850 → 680 → 320 → 850; heading stays at 104px for width 393.
- [x] Focus input in a short viewport, touch-scroll back to the header, reach bottom terms, and check horizontal overflow.
- [x] Light/dark login canvas, theme restoration after login unmount, and desktop 1440 × 900 screenshots.
- [ ] iPhone Chrome device verification. Chromium emulation does not reproduce native iOS browser chrome or keyboard; supplemental WebKit download was stopped due to slow transfer.

Review focus: mobile scroll recovery and scoped document styles in both login surfaces. No backend deployment is required; Web App and Platform are separate frontend deployments.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `5450405d1a895cd1618c0c7872129c0136d4e269`
- PR: #3985
- 作者：david-srp
- 日期：2026-10-01T12:42:04Z

### Commit Message

```
fix(auth): 修复移动端登录页滚动 / stabilize mobile login scrolling (#3985)

## Summary / 改动
- 修复 Web App 与 Platform
登录页在手机浏览器中随视口变化上下跳动、顶部不易返回及露出黑色背景的问题。移动端采用顶部自然排列和稳定的 `svh`
最小高度，保留整页原生滚动；桌面保留双栏居中。
- Stabilize both mobile login layouts and scope the white document
canvas to the standalone login route. Authentication behavior is
unchanged; the selected theme returns when leaving login.

## Root cause / 原因
动态视口高度配合垂直居中会在地址栏伸缩时移动内容；Platform 外层仍使用
`100vh`，与登录容器高度不一致；两端登录页外层还会继承深色背景。The fix removes mobile recentering
and aligns the login document canvas without introducing scroll locks or
viewport JavaScript.

## Test plan / 验证
- [x] Web App governance guards, TypeScript, login-related tests,
targeted ESLint, and pre-commit full ESLint.
- [x] Platform TypeScript, 22 login/theme tests, and targeted ESLint.
- [x] Chromium mobile widths 320 / 393 / 430 and landscape 844; viewport
heights 850 → 680 → 320 → 850; heading stays at 104px for width 393.
- [x] Focus input in a short viewport, touch-scroll back to the header,
reach bottom terms, and check horizontal overflow.
- [x] Light/dark login canvas, theme restoration after login unmount,
and desktop 1440 × 900 screenshots.
- [ ] iPhone Chrome device verification. Chromium emulation does not
reproduce native iOS browser chrome or keyboard; supplemental WebKit
download was stopped due to slow transfer.

Review focus: mobile scroll recovery and scoped document styles in both
login surfaces. No backend deployment is required; Web App and Platform
are separate frontend deployments.
```

来源：SerendipityOneInc/ecap-workspace @ 5450405d，PR #3985，作者 david-srp。
