---
title: "BossClaw 电脑端登录页焕新"
type: "体验优化"
priority: "低"
date: "2026-07-06"
status: "待审核"
channels: ""
---

# BossClaw 电脑端登录页焕新

## 核心宣传点

BossClaw 老用户登录页在电脑上全新改版：品牌主视觉 + 磨砂玻璃登录卡片，登录过程中的错误与成功提示也更清晰美观。

## 原始内容

[ff11a7a8] feat(bossclaw): redesign returning-user login page for PC (#2733)

## What

Redesign the returning-user login page (`/bossclaw/login`) for **PC**,
matching the established bossclaw brand style. Before, it was the mobile
phone-frame card centered on a big empty desktop screen.

## Design

**Desktop** — one unified, premium canvas (no hard split):
- **Left**: brand hero, reusing the intro-page Hero elements — ZooClaw
logo + 「Boss 专用版」, kicker, gold title 「为决策者而生的 · 专属智能幕僚」, subtitle, and
the 3 stats.
- **Right**: the login form as a **frosted-glass card** floating on the
shared canvas.
- Gold ambient auras span the full width and glow **through** the glass
(bridging both sides); subtle film-grain for depth.

**Mobile** — single-column form card + a compact brand lockup (keeps the
existing mobile UX), same warm ambient glow (toned down for legibility).

## Login-flow feedback ("弹窗")

All the in-flow states are styled to match the PC/bossclaw look:
- **Errors** → a styled notice (red mark + card) instead of bare text;
covers SMS-send failure, wrong code, login failure, the **returning-user
rejection** (`仅支持用户登陆…marketing@zooclaw.ai`), and boss-bind failure.
- **Success** → a login-success card (gold ✓ + 「正在进入 BossClaw 管理工作台…」)
shown during the redirect.
- Loading / resend-cooldown as before.

## Copy

Destination reframed from a "chat space" to a **management console**:
- Title: 登录您的 **BossClaw 管理工作台** (was ZooClaw 聊天空间)
- Button: **进入管理工作台**
- Success: 正在进入 **BossClaw 管理工作台**…
- Added a "还不是 BossClaw 用户？请联系 marketing@zooclaw.ai 申请开通" helper.

## Scope

Frontend / CSS only — **login logic, `return_to` binding, and redirects
are unchanged**. Regenerated the subset fonts for the new copy; updated
the login unit test's button name.

## Testing

- vitest (login-client spec + bossclaw suite) + eslint green.
- Rendered at 1440 / 1680 / 390 px: desktop unified canvas + glass card,
mobile single-column, error notice.

> Note: local `tsc` flags `useSearchParams`/`useParams` as possibly-null
in `RedeemStep.tsx` (untouched) and the original `searchParams.get` in
`BossclawLoginClient` — but the installed next types are non-null and
this exact code is already live on main, so it's a local `.next`-cache
resolution quirk that does not reproduce in CI.

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>

--- PR #2733 body ---
## What

Redesign the returning-user login page (`/bossclaw/login`) for **PC**, matching the established bossclaw brand style. Before, it was the mobile phone-frame card centered on a big empty desktop screen.

## Design

**Desktop** — one unified, premium canvas (no hard split):
- **Left**: brand hero, reusing the intro-page Hero elements — ZooClaw logo + 「Boss 专用版」, kicker, gold title 「为决策者而生的 · 专属智能幕僚」, subtitle, and the 3 stats.
- **Right**: the login form as a **frosted-glass card** floating on the shared canvas.
- Gold ambient auras span the full width and glow **through** the glass (bridging both sides); subtle film-grain for depth.

**Mobile** — single-column form card + a compact brand lockup (keeps the existing mobile UX), same warm ambient glow (toned down for legibility).

## Login-flow feedback ("弹窗")

All the in-flow states are styled to match the PC/bossclaw look:
- **Errors** → a styled notice (red mark + card) instead of bare text; covers SMS-send failure, wrong code, login failure, the **returning-user rejection** (`仅支持用户登陆…marketing@zooclaw.ai`), and boss-bind failure.
- **Success** → a login-success card (gold ✓ + 「正在进入 BossClaw 管理工作台…」) shown during the redirect.
- Loading / resend-cooldown as before.

## Copy

Destination reframed from a "chat space" to a **management console**:
- Title: 登录您的 **BossClaw 管理工作台** (was ZooClaw 聊天空间)
- Button: **进入管理工作台**
- Success: 正在进入 **BossClaw 管理工作台**…
- Added a "还不是 BossClaw 用户？请联系 marketing@zooclaw.ai 申请开通" helper.

## Scope

Frontend / CSS only — **login logic, `return_to` binding, and redirects are unchanged**. Regenerated the subset fonts for the new copy; updated the login unit test's button name.

## Testing

- vitest (login-client spec + bossclaw suite) + eslint green.
- Rendered at 1440 / 1680 / 390 px: desktop unified canvas + glass card, mobile single-column, error notice.

> Note: local `tsc` flags `useSearchParams`/`useParams` as possibly-null in `RedeemStep.tsx` (untouched) and the original `searchParams.get` in `BossclawLoginClient` — but the installed next types are non-null and this exact code is already live on main, so it's a local `.next`-cache resolution quirk that does not reproduce in CI.

