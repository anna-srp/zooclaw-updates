# ecap-workspace — 2026-04-25 Commits

Total: 27 commits (since: 2026-04-25T00:00:00Z, until: 2026-04-26T00:00:00Z)

---

## 1. feat(ios): Redesign paywall and sidebar UserCard to match Figma (#1297)

- **SHA:** 16e9feec080ea31c84687f284510557665317831
- **Author:** bill-srp
- **Date:** 2026-04-25T02:45:41Z
- **PR:** #1297

### Full Commit Message & PR Body

feat(ios): Redesign paywall and sidebar UserCard to match Figma (#1297)

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

---

## 2. tools: heroicons Tier 3 review HTML generator + decisions template (#1366)

- **SHA:** 926e2bb12a2d
- **Author:** (ecap-workspace contributor)
- **Date:** 2026-04-25T16:23:22Z
- **PR:** #1366

### Full Commit Message

tools: heroicons Tier 3 review HTML generator + decisions template (#1366)

## Summary

Generator + outputs for side-by-side visual review of the 90 remaining Tier 3 wrappers vs their Heroicons v2 candidates. Self-contained static HTML, no dev-server needed — checkout + double-click → browser.

---

## 3–27. refactor(web): heroicons/svg-inline migration (multiple PRs)

The remaining 25 commits are all refactor/cleanup work:
- heroicons Tier 1/2/3 migration to @heroicons/react v2 (PRs #1358–#1368)
- svg-inline migrations for various UI components (PRs #1342–#1355)
- React Query migration cleanup (PR #1332)
- docs: React Query migration v2 spec (#1346)
- refactor(web): delete dead ChatWelcome + ToolProgressFloat (#1356)
- refactor(web): consolidate svg wrapper clusters (#1359–#1361)
- refactor(web): ProviderLogo brand logo extractions (#1357–#1358)

All are internal refactoring, no user-facing changes.

---

*Full JSON available in ecap-workspace-commits.json*
