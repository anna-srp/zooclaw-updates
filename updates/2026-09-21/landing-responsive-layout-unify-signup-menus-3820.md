---
title: "fix(landing): improve responsive layout and unify signup menus (#3820)"
type: "Bug Fix"
priority: "中"
date: "2026-09-21"
status: "待审核"
channels: ""
---

# 官网首页响应式布局修复，注册菜单统一

## 核心宣传点

首页标题和行动按钮在某些宽度下会重叠，原因是 hero 区用了固定网格宽度、文案不换行再加上定位偏移。现在改成流式网格、文案可换行，并调整了移动端间距；移动端点击区域加大，Agent 卡片在 iPhone 宽度下内容也能看清。餐厅 Agent 的截图换成了提供方给的 2087×1398 PNG，按字节原样拷入，没有 AI 重绘、没有缩放和有损重编码，显示宽度限制在 1043 CSS 像素、居中画布 1252 像素，保证桌面 2 倍屏够清晰；加载占位图和 10 种语言的 alt 文案一起更新。另外页头、hero 和页脚现在复用同一个注册下拉菜单和「Managed Agent API」标签，页脚不再绕过共享菜单，但三处的来源埋点仍然区分开。移动端轮播标题会按当前语言预留最高的那个角色名高度，轮播过程中不再跳动。

## 分级

- 内部：P1
- 外部：B
- 发布状态：已上线

## PR 说明

## Summary
- Fix homepage headline/CTA overlap with a fluid hero grid, wrapping copy, and mobile spacing. Increase mobile touch targets and keep agent-card content readable at iPhone widths.
- Replace the restaurant-agent screenshot/overlay with the supplied **2087 × 1398 PNG**, copied byte-for-byte without AI reconstruction, resizing, or lossy re-encoding. Limit the displayed image to **1043 CSS px** and its centered canvas to 1252 px, so the source covers desktop 2× density. Refresh the loading placeholder and all 10 locale alt texts.
- Reuse the same signup dropdown and **Managed Agent API** label for header, hero, and footer. Preserve distinct source context: `header_sign_up`, `landing_hero`, and `marketing_cta`.

## Root cause
Fixed hero grid widths, non-wrapping copy, and positional offsets allowed the headline to overlap the adjacent actions. Mobile agent cards relied on independent absolute text positions. The footer bypassed the shared menu.

The mobile rotating title now reserves the tallest role in the current language using an invisible, accessibility-hidden CSS grid layer. All translated roles fit without fixed line limits or height changes during rotation. Desktop indicator bars retain their original 26 px bottom offset while their button hit areas remain 44 px tall.

## Test plan
- [x] Frontend governance guards, TypeScript type-check, ESLint, formatting, and `git diff --check`.
- [x] Homepage, header, and login-page unit tests: **78 passed**; verifies separate CTA source context and accessible active headings across 10 locales.
- [x] Spanish and Italian at **320, 375, and 430 px**; every role measured within its container, no horizontal page overflow. At 375 px all six role transitions retain a stable 112 px title height.
- [x] Desktop checks at **1024, 1440, and 1920 px**: image loads at its original 2087 × 1398 dimensions, displayed width never exceeds 1043 px, source covers 2× rendering, indicator visual bottom is 26 px, and touch targets remain 44 px tall.
- [x] All three menus open/close with the keyboard and produce the expected distinct source parameters; shared menu labels and interaction remain consistent.
- [x] Original implementation also checked across 16 Chromium/WebKit responsive configurations, including iPhone layouts.

Frontend-only change. The final asset is the original supplied screenshot; no higher-resolution source or AI-enhanced output is claimed. Retaining a wider-than-1043 px image at 2× density would require a larger native export.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `ce681320f669b509145d63593600c847e0279efa`
- PR: #3820
- 作者：shana-srp
- 日期：2026-09-21T03:38:51Z

### Commit Message

```
fix(landing): improve responsive layout and unify signup menus (#3820)

## Summary
- Fix homepage headline/CTA overlap with a fluid hero grid, wrapping
copy, and mobile spacing. Increase mobile touch targets and keep
agent-card content readable at iPhone widths.
- Replace the restaurant-agent screenshot/overlay with the supplied
**2087 × 1398 PNG**, copied byte-for-byte without AI reconstruction,
resizing, or lossy re-encoding. Limit the displayed image to **1043 CSS
px** and its centered canvas to 1252 px, so the source covers desktop 2×
density. Refresh the loading placeholder and all 10 locale alt texts.
- Reuse the same signup dropdown and **Managed Agent API** label for
header, hero, and footer. Preserve distinct source context:
`header_sign_up`, `landing_hero`, and `marketing_cta`.

## Root cause
Fixed hero grid widths, non-wrapping copy, and positional offsets
allowed the headline to overlap the adjacent actions. Mobile agent cards
relied on independent absolute text positions. The footer bypassed the
shared menu.

The mobile rotating title now reserves the tallest role in the current
language using an invisible, accessibility-hidden CSS grid layer. All
translated roles fit without fixed line limits or height changes during
rotation. Desktop indicator bars retain their original 26 px bottom
offset while their button hit areas remain 44 px tall.

## Test plan
- [x] Frontend governance guards, TypeScript type-check, ESLint,
formatting, and `git diff --check`.
- [x] Homepage, header, and login-page unit tests: **78 passed**;
verifies separate CTA source context and accessible active headings
across 10 locales.
- [x] Spanish and Italian at **320, 375, and 430 px**; every role
measured within its container, no horizontal page overflow. At 375 px
all six role transitions retain a stable 112 px title height.
- [x] Desktop checks at **1024, 1440, and 1920 px**: image loads at its
original 2087 × 1398 dimensions, displayed width never exceeds 1043 px,
source covers 2× rendering, indicator visual bottom is 26 px, and touch
targets remain 44 px tall.
- [x] All three menus open/close with the keyboard and produce the
expected distinct source parameters; shared menu labels and interaction
remain consistent.
- [x] Original implementation also checked across 16 Chromium/WebKit
responsive configurations, including iPhone layouts.

Frontend-only change. The final asset is the original supplied
screenshot; no higher-resolution source or AI-enhanced output is
claimed. Retaining a wider-than-1043 px image at 2× density would
require a larger native export.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

来源：SerendipityOneInc/ecap-workspace @ ce681320，PR #3820，作者 shana-srp。