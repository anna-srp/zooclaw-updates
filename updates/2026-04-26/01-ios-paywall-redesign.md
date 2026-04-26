---
title: "iOS 付费页面全新改版，升级体验更清晰"
type: "产品基础功能更新"
priority: "中"
date: "2026-04-26"
status: "待审核"
channels: "Discord + changelog"
---

# iOS 付费页面全新改版，升级体验更清晰

## 核心宣传点

ZooClaw iOS 应用的付费/升级页面经过全面重新设计：更清晰的套餐对比表、更流畅的升级路径，以及更快的聊天体验——让你的每一次升级决策都一目了然。

## 原始内容

**Commit:** feat(ios): Redesign paywall and sidebar UserCard to match Figma (#1297)
**Author:** bill-srp
**Date:** 2026-04-25T02:45:41Z
**PR:** #1297

---

## Summary

Redesign the iOS paywall, sidebar UserCard, and chat UX with
Figma-matching designs and performance improvements.

### Paywall
- Remove Ultra plan — Pro is now the highest tier
- Both plans use comparison table layout (Free vs Starter, Free vs Pro)
with matching feature rows
- CTA button: "Get Starter" / "Get Pro" for free users, "Upgrade to ..."
for subscribers
- Trial badge ("7-Day Free Trial") overlaid on CTA button top-right (not
in feature card)
- Replace scrolling brand logos with marquee `paywall_models` image
- Pro plan monthly only (no yearly option)
- Remove savings labels, billed labels, /mo suffix from billing cards
- Fix Starter-to-Pro upgrade path — Starter subscribers land on Pro tab
- Feature card + billing cards + CTA scroll together; footer pinned at bottom

### Paywall Gating (extracted to `PaywallGating` enum)
- `isHighestTier` blocks Pro/Ultra from paywall
- `initialPlanIndex` auto-advances to next tier for subscribers
- `ctaLabel` reflects selected plan name dynamically
- `shouldShowUpgradeButton` hides for Pro/Ultra in settings
- 45 tests covering all subscriber flow scenarios

### Sidebar UserCard
- Three-part layout: avatar | name + plan | upgrade button

### Chat UX
- Reduce scroll jumping with content-based height estimation and height caching
- Pre-fetch image attachments for latest page on sync
- Sharpen photo picker thumbnails (screen-scale-aware, opportunistic delivery)
- Square crop thumbnails with GeometryReader

### Other
- Opt-in `liquidGlass` flag on GlassButton for iOS 26 (`#if swift(>=6.2)`)
- Fix redeem modal keyboard avoidance and smooth dismiss
- Increase default API timeout from 30s to 60s
- Upload dSYMs to Sentry via fastlane for crash symbolication
- Pass `SENTRY_AUTH_TOKEN` in iOS deploy workflow
