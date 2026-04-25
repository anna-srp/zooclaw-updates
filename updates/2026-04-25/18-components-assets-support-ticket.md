---
title: "资产面板 & 支持工单界面组件化完成"
type: "产品基础功能更新"
priority: "低"
date: "2026-04-25"
status: "待审核"
channels: "Discord + changelog"
---

# 资产面板 & 支持工单界面组件化完成

## 核心宣传点

资产面板（AssetsPanel）和支持工单（SupportTicket）界面完成组件化重构，界面更稳定，后续更新更快。

## 原始内容

Commit: 923da54dbb2b545f0eff3bc9fa38699e9cf5898e

Message:
feat(web): components-4 — finish top-level components (AssetsPanel + SupportTicketModal) (#1325)

## Summary

Continues #1321 / #1323. Migrates the last 2 non-special top-level
\`components/\` files (13 svg occurrences) to \`ui/icons/\` wrappers and
shrinks the \`svg-inline\` baseline from **80 → 78**. Top-level
\`components/*.tsx\` baseline now empty except \`ProviderLogo\` (30
brand logos — separate PR) and \`UserAvatar\` (pre-existing dead code).

## Files migrated

| File | svgs | wrappers |
|---|---|---|
| \`AssetsPanel.tsx\` | 9 | ChevronRightPathIcon (reused),
PhotoThickIcon, WarningCircleTallIcon, SearchPlusIcon, DownloadThickIcon
×2, SpinnerIcon (reused), CheckSolidIcon (reused), PlusLargeIcon |
| \`SupportTicketModal.tsx\` | 4 | SupportOwlIcon, SupportRaccoonIcon,
SupportFoxIcon (3 mascot illustrations) + CloseIcon (reused) |

## Stroke/element diff against existing wrappers (per #1323 lesson)

Per the PR #1323 learning, every reused wrapper here was diffed against
the original svg for \`strokeWidth\` / \`strokeLinecap\` /
\`strokeLinejoin\` / element-type before reuse. Where mismatches
existed, a new byte-exact variant wrapper was created instead of
reusing:

- AssetsPanel original \`PhotoIcon\` is **stroke=2** (not the existing
\`PhotoIcon\` stroke=1.5) → new \`PhotoThickIcon\`
- AssetsPanel original \`DownloadIcon\` is **stroke=2** (not the
existing \`DownloadIcon\` stroke=1.5) → new \`DownloadThickIcon\`
- AssetsPanel original exclamation-circle has taller \`!\` (y=8..12)
than \`WarningCircleIcon\` (y=9..11) → new \`WarningCircleTallIcon\`
- AssetsPanel original \`+\` has wider span (\`M12 4v16m8-8H4\`) than
\`PlusIcon\` (\`M12 6v6m0 0v6m0-6h6m-6 0H6\`) → new \`PlusLargeIcon\`

Verified byte-exact reuses: \`ChevronRightPathIcon\`, \`SpinnerIcon\`,
\`CheckSolidIcon\`, \`CloseIcon\`.

## SupportTicketModal mascots

\`SupportTicketModal.tsx\` had a local \`SupportIllustration\` switch
function returning 3 hand-drawn 88x80 SVG mascots (each ~30 lines of
paths/circles/ellipses with hardcoded brand-color hexes). Each extracted
as a self-contained wrapper:

- \`SupportOwlIcon\` — owl + magnifying glass, brown tones (bug-report)
- \`SupportRaccoonIcon\` — raccoon + receipt, gray tones (billing)
- \`SupportFoxIcon\` — fox + lightbulb, orange tones (suggestion /
default)

The local \`SupportIllustration\` switch function was kept (rewritten to
dispatch to the 3 wrappers) so the call-site API doesn't change.

## Visual fidelity: 0 risk

All wrappers preserve \`path\` / \`viewBox\` / \`fill\` / \`stroke\` /
\`strokeWidth\` / \`strokeLinecap\` / \`strokeLinejoin\` byte-for-byte.

## Test plan

- [x] \`pnpm lint\` clean
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint:ci\` clean (\`✓ All web/ ci-lint checks passed\`)
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` shows 80 → 78 (✓
shrink, exactly 2 files)
- [x] Sibling shrink scripts (react/forbid-dom-props 45→45, no-raw-fetch
8→8) unchanged
- [x] Both migrated files: \`grep -c '<svg'\` returns 0
- [x] Related unit tests pass (AssetsPanel + SupportTicketModal — 13
tests)
- [ ] Visual regression on staging: assets panel (empty / error /
per-asset toolbar download/zoom/spinner/check), support ticket modal (3
mascots × bug/billing/suggestion, close X) — each pixel-identical to
main

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

PR Description:
## Summary

Continues #1321 / #1323. Migrates the last 2 non-special top-level \`components/\` files (13 svg occurrences) to \`ui/icons/\` wrappers and shrinks the \`svg-inline\` baseline from **80 → 78**. Top-level \`components/*.tsx\` baseline now empty except \`ProviderLogo\` (30 brand logos — separate PR) and \`UserAvatar\` (pre-existing dead code).

## Files migrated

| File | svgs | wrappers |
|---|---|---|
| \`AssetsPanel.tsx\` | 9 | ChevronRightPathIcon (reused), PhotoThickIcon, WarningCircleTallIcon, SearchPlusIcon, DownloadThickIcon ×2, SpinnerIcon (reused), CheckSolidIcon (reused), PlusLargeIcon |
| \`SupportTicketModal.tsx\` | 4 | SupportOwlIcon, SupportRaccoonIcon, SupportFoxIcon (3 mascot illustrations) + CloseIcon (reused) |

## Stroke/element diff against existing wrappers (per #1323 lesson)

Per the PR #1323 learning, every reused wrapper here was diffed against the original svg for \`strokeWidth\` / \`strokeLinecap\` / \`strokeLinejoin\` / element-type before reuse. Where mismatches existed, a new byte-exact variant wrapper was created instead of reusing:

- AssetsPanel original \`PhotoIcon\` is **stroke=2** (not the existing \`PhotoIcon\` stroke=1.5) → new \`PhotoThickIcon\`
- AssetsPanel original \`DownloadIcon\` is **stroke=2** (not the existing \`DownloadIcon\` stroke=1.5) → new \`DownloadThickIcon\`
- AssetsPanel original exclamation-circle has taller \`!\` (y=8..12) than \`WarningCircleIcon\` (y=9..11) → new \`WarningCircleTallIcon\`
- AssetsPanel original \`+\` has wider span (\`M12 4v16m8-8H4\`) than \`PlusIcon\` (\`M12 6v6m0 0v6m0-6h6m-6 0H6\`) → new \`PlusLargeIcon\`

Verified byte-exact reuses: \`ChevronRightPathIcon\`, \`SpinnerIcon\`, \`CheckSolidIcon\`, \`CloseIcon\`.

## SupportTicketModal mascots

\`SupportTicketModal.tsx\` had a local \`SupportIllustration\` switch function returning 3 hand-drawn 88x80 SVG mascots (each ~30 lines of paths/circles/ellipses with hardcoded brand-color hexes). Each extracted as a self-contained wrapper:

- \`SupportOwlIcon\` — owl + magnifying glass, brown tones (bug-report)
- \`SupportRaccoonIcon\` — raccoon + receipt, gray tones (billing)
- \`SupportFoxIcon\` — fox + lightbulb, orange tones (suggestion / default)

The local \`SupportIllustration\` switch function was kept (rewritten to dispatch to the 3 wrappers) so the call-site API doesn't change.

## Visual fidelity: 0 risk

All wrappers preserve \`path\` / \`viewBox\` / \`fill\` / \`stroke\` / \`strokeWidth\` / \`strokeLinecap\` / \`strokeLinejoin\` byte-for-byte.

## Test plan

- [x] \`pnpm lint\` clean
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint:ci\` clean (\`✓ All web/ ci-lint checks passed\`)
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` shows 80 → 78 (✓ shrink, exactly 2 files)
- [x] Sibling shrink scripts (react/forbid-dom-props 45→45, no-raw-fetch 8→8) unchanged
- [x] Both migrated files: \`grep -c '<svg'\` returns 0
- [x] Related unit tests pass (AssetsPanel + SupportTicketModal — 13 tests)
- [ ] Visual regression on staging: assets panel (empty / error / per-asset toolbar download/zoom/spinner/check), support ticket modal (3 mascots × bug/billing/suggestion, close X) — each pixel-identical to main

🤖 Generated with [Claude Code](https://claude.com/claude-code)
