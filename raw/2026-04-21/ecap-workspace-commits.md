# ecap-workspace Commits — 2026-04-21

共 41 条 commits

---

## [5fc68303](https://github.com/SerendipityOneInc/ecap-workspace/commit/5fc683030b31de7be479be7141aa4abf894ae1e8)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T15:30:49Z

**Message:**
```
refactor(web): relocate seo.ts from lib/ to app/_seo.ts — fix W1 (A1-PR4) (#1128)

## Summary
- Fixes the remaining W1 violation `lib/seo.ts → @/theme/brand-assets`
by relocating `seo.ts` up one layer (lib → app).
- `seo.ts` is page-metadata logic exclusive to the App Router — all 4
callers already live under `src/app/`. Moving the module is simpler than
restructuring `theme/`.
- Baseline shrinks **17 → 16**. W6 (`theme/brand-themes →
lib/auth/types`) stays in baseline for a separate small PR.

## Why relocate instead of restructuring theme/

Reviewer-suggested approach.

| Scope | This PR (relocate `seo.ts`) | Alternative (split
`theme/brand-*` → `config/brand/*`) |
|---|---|---|
| Files touched | **7** | ~23 |
| Diff | **+5 / −14** | +31 / −49 |
| Violations fixed | W1 | W1 + W6 |
| theme/ structure | unchanged | rewritten |

The alternative required relocating 2 files from `theme/` plus 16 caller
import rewrites. This PR only moves `seo.ts` + its test and updates 4
callers. W6 is a 1-line fix (move `STORAGE_KEYS.BRAND_THEME` out of
`lib/auth/types`) deferred to its own PR.

## Why `@/app/_seo`

`src/app/` forbids top consumer imports from nothing (app is Layer 4),
so `app → theme` is allowed by W1-W6. Leading underscore matches the
existing `src/app/[locale]/_presignedFactory.ts` convention — Next.js
ignores underscore-prefixed non-route files.

Alternative homes considered + rejected:
- `src/app/seo.ts` — no underscore convention in this codebase
- `src/lib/app-metadata/seo.ts` — still `lib/`, W1 still fails
- `src/app/[locale]/_seo.ts` — locks it under [locale]; `app/robots.ts`
and `app/layout.tsx` are root-level

## Changes

| File | Change |
|---|---|
| `web/src/lib/seo.ts` | `git mv` → `web/src/app/_seo.ts` |
| `web/tests/unit/lib/seo.unit.spec.ts` | `git mv` →
`web/tests/unit/app/_seo.unit.spec.ts` |
| `web/src/app/[locale]/about/page.tsx` | import `@/lib/seo` →
`@/app/_seo` |
| `web/src/app/[locale]/layout.tsx` | same + import sort reshuffled |
| `web/src/app/layout.tsx` | same |
| `web/src/app/robots.ts` | same |
| `web/.dependency-cruiser-known-violations.json` | remove W1 seo entry
(17 → 16) |

## Local verification
- `pnpm lint:imports` — exit 0, \`16 known violations ignored\`
- `pnpm test:unit tests/unit/app/_seo.unit.spec.ts` — 6 tests pass
- `npx tsc --noEmit` — clean
- `pnpm lint` — clean

## Remaining baseline 16

After this PR lands: W2(3) / W3(5) / W4(2) / W5(4) / W6(2) — fully
UI-and-feature-isolation cluster + 2 theme-leaf entries (brand-themes →
lib/auth/types + brand-assets → theme internal). Each subsequent cleanup
PR removes a handful.

## Test plan
- [x] Unit tests pass (6 tests)
- [x] dep-cruiser hard gate still green (17 → 16 known violations)
- [x] tsc + eslint clean
- [ ] CI confirms web-quality + asset-size-guard + jscpd
- [ ] Reviewer validates `_seo` underscore naming + relocation approach

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [329248c5](https://github.com/SerendipityOneInc/ecap-workspace/commit/329248c52269a61a9b8fd52c0c4db1347ba4657d)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T15:26:20Z

**Message:**
```
test(web): DiagnosticsSection 全面覆盖 (#894 Step 5 补) (#1129)

## Summary

Epic #894 Step 5 (#899) — 再补一个：\`DiagnosticsSection.tsx\` (338 LOC) 从 0%
→ 全分支。49 tests.

## 源码变动（极小）

- 6 个 pure helper (parseCpu/Memory/Disk + formatCpu/Memory/Disk) 加
export
- 零语义变化、零 runtime 行为变化

## 新增 49 个测试

| 分组 | # | 覆盖 |
|---|---|---|
| parseCpuMillicores | 4 | 空串 / nanocores / millicores / 整核 |
| parseMemoryMiB | 7 | 空串 / Gi/Mi/Ki (binary) / G/M (decimal) / 裸 bytes
|
| parseDiskGiB | 5 | 空串 / Gi / Mi/Ki 降级 / 裸 bytes |
| formatCpu | 4 | 空串 / >= 1000ms / 中段 / sub-milli |
| formatMemory | 4 | 空串 / >= 1024 / 中段 / sub-MiB |
| formatDisk | 4 | 空串 / Gi / Mi / Ki |
| DiagnosticsSection gate | 2 | !botRunning → 提示 / true → Card 渲染 |
| ResourcesCard | 10 | loading/error/empty/data 状态机 / bot_id & pod_name
可选 / disk gauge 有无 / usage=undefined 提示 / refresh 回调 / SemiCircleGauge
>=80% destructive / <80% success / 0% → "—" |
| LogsViewer | 6 | loading/empty/logs / Tail select default=100 + change
传给 refresh / Timestamps checkbox / loading 按钮 disabled |

## Bug-hunting

无新发现。状态机清晰；gauge 阈值切换（80%）逻辑对；parse/format 单位处理完整。

## Test plan

- [x] 49/49 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 5 (#899)
- 剩余：ConnectorsSection (493) / ClawSettingsClient (438 关键 ~120)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [420c5898](https://github.com/SerendipityOneInc/ecap-workspace/commit/420c589893122447d887fb939d69ea02638b555c)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T15:07:53Z

**Message:**
```
test(web): DiaryCards 全面覆盖 (#894 Step 5 补) (#1121)

## Summary

Epic #894 Step 5 (#899) — 再补一个：\`DiaryCards.tsx\` (150 LOC) 从 0% →
全分支，19 tests。

## 新增 19 个测试

| 组 | # | 覆盖 |
|---|---|---|
| 加载状态 | 1 | 3 个 animate-pulse skeleton |
| 空状态 | 3 | success=true+空文件 / success=false / API reject（finally 清
loading） |
| 列表渲染 | 4 | sort desc + slice(0,10) / first_user_message 兜底 session_id
/ archive_reason 兜底 "Archived session" / 卡片点击 →
router.push('/session-history') |
| formatDate | 6 | ISO 当天 "Today" / 其他日 weekday / Unix seconds / Unix ms
/ invalid → 原样 / 空串 → "Unknown" |
| 滚动控件 | 4 | files ≤ 3 隐藏箭头 / > 3 显示 / 点左 scrollBy(-280) / 点右
scrollBy(+280) |
| Unmount 竞态 | 1 | cancelled flag 防卸载后 setState |

## Harness 要点

- `vi.useFakeTimers()` 先于 `vi.setSystemTime()` — 吃过 #1119 round 2
的教训，`formatDate` 的 "Today" 判断依赖确定"今天"
- i18n mock 对 `t(key) || 'English'` 模式的 key 返回 `''` 触发英文兜底
- jsdom 不实现 `HTMLElement.scrollBy`，用 `Object.defineProperty` 手搭（同
ScrollToBottomButton）

## Bug-hunting

无新发现。组件 unmount race 有正确的 cancelled flag；三个 fallback 链都有。

## Test plan

- [x] 19/19 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 5 (#899)
- Step 5 已覆盖：ChannelsSection / Slack/Telegram/Discord/FeishuSetup
wizards / Integrations / ModelSection / TimezoneSection / SaveButton /
useClawSettings / useIntegrations / UsageCard (#1119) / 本 PR
- 剩余：ConnectorsSection (493 LOC) / DiagnosticsSection (338 LOC) /
ClawSettingsClient (438 LOC key ~120)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [36d1152b](https://github.com/SerendipityOneInc/ecap-workspace/commit/36d1152b198548cf9d9b5d61d63de5fb9a40e23e)

**Author:** tim-srp  
**Date:** 2026-04-20T15:06:53Z

**Message:**
```
feat(web): replace degraded banner with IQ bar (#1123)

## Summary
- Replace the text-only "积分已用完，正在使用基础模型运行中" degraded banner with a
visual **intelligence bar** (gradient red→green, indicator at 25/100)
- New messaging: "AI 变笨了" / "AI is underpowered" — users immediately
understand quality trade-off instead of being confused by "basic model"
wording
- Theme-aware: IQ bar gradient colors defined as CSS vars
(`ecap-iq-bar-*`) with dark mode support
- 3 new i18n keys (`degradedTitle`, `degradedScore`, `boostAI`) across
all 7 languages

## Motivation
Users on free models attributed poor AI output quality to product bugs
rather than model capability. This redesign makes the quality difference
unmistakably clear.

## Test plan
- [ ] Verify degraded banner renders IQ bar in light mode
- [ ] Verify degraded banner renders correctly in dark mode
- [ ] Verify `expired` and `expiryWarning` variants are unchanged
- [ ] Check all 7 languages display correctly (zh, en, ja, ko, es, pt,
ar)
- [ ] Click "充值提升" / "Boost AI" navigates to `/subscription`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

---

## [9ab17392](https://github.com/SerendipityOneInc/ecap-workspace/commit/9ab17392e774753118be0685696f635b9c3a725e)

**Author:** sam-srp  
**Date:** 2026-04-20T14:50:35Z

**Message:**
```
feat(web): preview Mattermost attachments + pptx rendering fixes (#1125)

## Summary

- **Preview MM attachments inline**: clicking a previewable file
attachment (pdf / xlsx / docx / pptx / html / md / code / ...) on a
Mattermost message now opens the artifact preview side panel, and
bot-sent attachments auto-open like today's in-text artifact URLs.
- **Infrastructure**: adds an optional `PreviewSource` on `PreviewFile`
carrying the MM Bearer token. A new `useResolvedUrl` hook fetches MM
URLs with auth once per preview, caches them as blob URLs, and cleans up
on unmount — renderers stay auth-unaware.
- **pptx renderer overhaul**: the existing hand-rolled OOXML renderer
had a long tail of bugs exposed by real-world decks. This PR fixes each
one with a principled spec-based solution.

## What changed in pptx rendering

Text:
- Strip BiDi control chars (stray `U+202E` was reversing titles)
- Drop `display: flex` on paragraphs → flex items were trimming
leading/trailing whitespace, dropping spaces between
differently-formatted runs
- `overflow: visible` on text shapes — PowerPoint lets text overflow
shape bounds; we were clipping tight table cells
- Honor `<a:ea>` / `<a:latin>` typeface with CJK-aware fallback stack
(YaHei → PingFang → Noto CJK)
- Font size in `cqw` units against a per-slide CSS variable → text
scales with the slide container (same behavior as PowerPoint canvas
resize)
- Parse `<a:spcBef>`, `<a:spcAft>`, `<a:lnSpc>` with sensible default
(0.4em) when master defaults would have applied
- Render `<a:buChar>` bullets with hanging indent from `marL` + `indent`

Shapes:
- Parse `<a:custGeom>` paths (moveTo / lnTo / cubicBezTo / quadBezTo /
arcTo / close) to SVG
- Multi-subpath support (was only reading first `<a:path>` of
`<a:pathLst>`)
- `prstGeom` presets as SVG paths: ellipse, line, triangle, diamond,
parallelogram, hexagon, arrows, star5, arc, blockArc
- `prst="arc"` sweep angles from `<a:avLst>` adj1/adj2 with correct
normalization (`?: sw1 sw1 sw2`)
- `xfrm` `rot` / `flipH` / `flipV` applied as CSS transforms
- `roundRect` corner radius uses spec formula `adj / 100000 × min(w, h)
/ 2`
- Border `<a:alpha>` now applied (was ignored — borders rendered at 100%
opacity)

Layout:
- Drop the `max-w-3xl` cap on the preview container so slides fill the
preview pane

Misc:
- Force correct MIME on MM blob URLs (MM serves
`application/octet-stream`, which made `<iframe>` show HTML source text)
- Hide "copy link" on MM-sourced previews (blob URLs aren't shareable)

## Files

- New: `web/src/components/artifacts/useResolvedUrl.ts`,
`docs/superpowers/specs/2026-04-20-mm-attachment-preview.md`
- Modified: `ArtifactPreview.tsx`, `types.ts`, `MMAttachments.tsx`,
`useArtifactsSidebar.ts`, `MarkdownContent.tsx`, `GenClawClient.tsx`,
`PptxRenderer.tsx`

## Test plan

- [ ] Send pdf / xlsx / docx / pptx / html / md / code / csv as MM
attachments → each opens in preview on click; bot-sent attachments
auto-open
- [ ] Download button downloads original file (not blob) with correct
extension
- [ ] Copy-link hidden for MM previews, visible for artifact URLs
- [ ] Existing artifact URL previews unchanged (regression check on
public URLs)
- [ ] pptx: text renders correctly (no reversed titles, no missing
spaces, Chinese fonts OK)
- [ ] pptx: curves / arcs / non-rect shapes render (not collapsed to
rectangles)
- [ ] pptx: preview fills full preview pane width; fonts scale
proportionally

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [00d19e47](https://github.com/SerendipityOneInc/ecap-workspace/commit/00d19e47f27bc9ee1d211d5b73f23954f60c88f1)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T14:56:14Z

**Message:**
```
refactor(web): extract triggerCreditsRefresh to src/lib (A1-PR3) (#1124)

## Summary
- First A1 cleanup PR — fixes 1 of the 2 W1 violations in the baseline.
- Moves the plain-function `triggerCreditsRefresh` out of
`src/hooks/useBillingCredits.ts` into a new
`src/lib/billing-credits.ts`.
- Rewrites **all 3** call sites (no re-export shim) and shrinks the
baseline 18 → 17.

## Why `triggerCreditsRefresh` doesn't belong in `hooks/`
```ts
export function triggerCreditsRefresh(): void {
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new CustomEvent('credits-refresh'))
  }
}
```
No React state, no `use*` dependency — it's a plain event dispatcher
that happened to live alongside the `useBillingCredits` hook. Any `lib/`
module needing to signal "refresh credits" had to import from
`@/hooks/*`, which is exactly the W1 contract violation (`lib → hooks` —
upward dependency).

## Changes

| File | Action |
|---|---|
| `web/src/lib/billing-credits.ts` | **new** — 14 lines, single function
|
| `web/src/hooks/useBillingCredits.ts` | drop the function + its
comment; `getCachedCredits` / `clearCreditsCache` / hook stay |
| `src/components/billing/SubscriptionPanel.tsx` | `@/hooks` →
`@/lib/billing-credits` for this symbol |
| `src/components/onboarding/OnboardingProvider.tsx` | same |
| `src/lib/payment/handlePaymentSuccess.ts` | same (the W1 violator) |
| `tests/unit/lib/billing-credits.unit.spec.ts` | **new** — 2 tests
moved from hooks spec |
| `tests/unit/hooks/useBillingCredits.unit.spec.ts` | describe block
removed + import trimmed |
| `tests/unit/lib/payment/handlePaymentSuccess.unit.spec.ts` | mock path
+ dynamic-import path |
| `tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx` |
split single `vi.mock(@/hooks/useBillingCredits)` into 2 mocks |
| `web/.dependency-cruiser-known-violations.json` | removed the fixed
`handlePaymentSuccess.ts → useBillingCredits.ts` entry |

No re-export shim is left behind, per the project convention
(`feedback_no_reexport_shim` in the author's memory).

## Baseline shrinks 18 → 17
The `depcruise-baseline` pattern designed in A1-PR2 works as expected:
each cleanup PR removes one entry from the baseline JSON and fixes the
corresponding import. When the JSON is `[]` the baseline file itself can
be deleted.

Remaining W1: `src/lib/seo.ts → @/theme/brand-assets` (11-caller
refactor, deferred to its own PR).

## Local verification
- `pnpm lint:imports` — exit 0, prints `17 known violations ignored`
- `pnpm test:unit` on the 4 affected files — **68 tests pass**
- `pnpm lint` — clean (simple-import-sort auto-fixed during commit)
- `npx tsc --noEmit` — clean

## Test plan
- [x] Unit tests pass (all 4 affected files)
- [x] dep-cruiser hard gate still green (baseline shrinks 18 → 17)
- [ ] CI confirms above
- [ ] Reviewer validates split mock approach in
`SubscriptionPanel.unit.spec.tsx` (one `vi.mock` per module)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [36587abd](https://github.com/SerendipityOneInc/ecap-workspace/commit/36587abd8cc613e6d841b13fe3237f0a2e602273)

**Author:** tim-srp  
**Date:** 2026-04-20T14:34:53Z

**Message:**
```
test(e2e): add model switching, onboarding & subscription E2E tests (#1019)

## Summary
- **Model Switching**: selector button, dropdown tabs, tab filtering,
model selection, ESC close
- **Onboarding Flow**: full 4-step UI via `?onboarding=preview` mode
(invite code → name → companion → loading)
- **Subscription & Pricing**: public pricing page, subscription panel,
billing toggle, plan CTAs; staging-only Stripe sandbox tests (upgrade
redirect, downgrade/cancel modals)

## Files
- `web/tests/e2e/specs/model-switching.spec.ts` — 5 scenarios
- `web/tests/e2e/specs/onboarding-flow.spec.ts` — 5 scenarios
- `web/tests/e2e/specs/subscription-pricing.spec.ts` — 10 scenarios (3
staging-only)
- `web/playwright.config.ts` — register 3 new projects

## Test plan
- [ ] `pnpm exec playwright test --project=model-switching`
- [ ] `pnpm exec playwright test --project=onboarding-flow`
- [ ] `pnpm exec playwright test --project=subscription-pricing`
- [ ] Staging: `E2E_ENV=staging pnpm exec playwright test
--project=subscription-pricing`

## Follow-up fixes

### `onboarding-flow` — preview-mode starts on step 1 again
Local run against staging surfaced one real bug:

**Symptom**: Scenario 1 "Step 1 — Invite Code entry" timed out with
Continue button `[disabled]`; 3 downstream scenarios skipped via serial
mode.

**Root cause**: two conflicts with the shared auth state / page chrome:
1. `auth.setup.ts` seeds `ecap:onboarding:progress` marking every step
completed (so other specs bypass the modal). This spec inherited that
storage state and was landing on Companion Select instead of step 1.
2. `GuideTourModal` (`fixed inset-0 z-[100]`) overlays the viewport on
fresh sessions and intercepts pointer events on the invite code form —
Playwright log: `<img alt="One brain. Full crew." ... from <div
data-sentry-component="GuideTourModal" ...> subtree intercepts pointer
events`.

**Fix** (`onboarding-flow.spec.ts` `beforeAll`, no business-code
changes):
- Strip `ecap:onboarding:progress*` keys via `addInitScript` so React
reads `DEFAULT_PROGRESS` and renders step 1.
- Apply `E2E_OVERLAY_SUPPRESSION` (same set used by `model-switching` /
`agent-hire-fire`) to dismiss `GuideTourModal` + compensation popup.
- Scenario 1: wait for `"Got an invite code?"` prompt before
interacting, switch to `input[placeholder="Enter code"]` +
`pressSequentially('TESTCODE', { delay: 30 })` so the controlled input's
`onChange` (with `.toUpperCase()` transform) reliably fires, and `await
expect(continueBtn).toBeEnabled()` before click so a future state-sync
regression surfaces in 5s rather than a 180s disabled-click timeout.

**Local verification**: `E2E_ENV=staging pnpm test:e2e
--project=onboarding-flow` → **6/6 passed in 21.5s**.

### Auto-review follow-ups
- **Stripe popup race** (subscription-pricing Upgrade scenario):
`popup.url()` was read the instant the event fired, but Stripe opens
`about:blank` first and then redirects — capture could be `about:blank`
and silently fail. Also, `page.on('popup', ...)` leaks a long-lived
handler across tests. Switched to a scoped `page.waitForEvent('popup')`
raced against the click, then
`popup.waitForURL(/checkout\.stripe\.com/)` before reading the URL.
- **Tailwind-class locator** (model-switching selection scenario):
`option.locator('.text-sm.font-medium')` violated `web/CLAUDE.md`'s
"Tailwind class strings are styling, not contract" rule. Added
`data-testid="model-option-name"` on the model display-name div and
updated the test to use `getByTestId`.
- **Dead redirect fallback in upgrade assertion**: `SubscriptionPanel`
always uses `window.open(..., '_blank', 'noopener,noreferrer')` — there
is no in-tab redirect path. The previous `else {
expect(page.url()).toContain(...) }` was dead code that produced a
confusing `/en/subscription does not contain checkout.stripe.com`
message when the popup event was missed. Replaced with two explicit
assertions: popup must be captured (self-explanatory failure message) +
captured URL must contain `checkout.stripe.com`.

### Known non-blockers (not addressed in this PR)
- `waitForTimeout(300)` after tab clicks in a few places — pragmatic
transition-animation padding; would only be worth revisiting if slow CI
produces flake.
- Hardcoded `100`/`200` price assertions — already scoped to
`plan-card-pro` / `plan-card-ultra` so no broad matching; easier to
update when prices actually change.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

---

## [7660252d](https://github.com/SerendipityOneInc/ecap-workspace/commit/7660252dcc693d25b259cc801db9a8c012d58cb7)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T14:14:29Z

**Message:**
```
refactor(web): drop backend.ts BackendAPI aliases + promote duplicates gate (B3) (#1120)

## Summary
- Cleans the 6 legacy `*BackendAPI` alias exports in
`web/src/lib/api/backend.ts` — the sole content of knip's "duplicate
exports" baseline.
- Promotes the `duplicates` category to knip's hard gate in
`02-dead-code.sh` so new aliases fail CI.
- First content-cleanup PR of the B track.

## Scope
- `web/src/lib/api/backend.ts`: remove the 6 alias exports
(`callBackendAPI` = `callAPI`, etc). Only reference in src/ is
`backend.ts` itself.
- `web/tests/unit/lib/api/backend.unit.spec.ts`: remove the "backward
compatible exports" `describe` block (sole consumer of the aliases). 19
functional tests remain.
- `web/scripts/ci-lint/02-dead-code.sh`: add `duplicates` to knip
`--include`; header comment updated to match the new incremental-gate
roadmap.

## Why this was safe to drop
`grep -r '(call|get|post|put|delete|patch)BackendAPI' web/` returned
only:
1. `web/src/lib/api/backend.ts` — the 6 `export const` lines themselves
2. `web/tests/unit/lib/api/backend.unit.spec.ts` — the one test block
that asserted they === the canonical functions

No production code (src/ or tests/e2e/) imports the alias form. The
"向后兼容" comment suggests they were kept during a rename from `BackendAPI`
→ `API`; the rename is now fully absorbed.

## Local verification
- `pnpm test:unit tests/unit/lib/api/backend.unit.spec.ts` — **19 tests
pass**
- `WARN_ONLY=1 pnpm lint:ci` — **exit 0**; knip dep-health gate (now
including `duplicates`) reports 0 violations
- `pnpm lint` — clean (prettier fixed one trailing-newline issue
post-edit)

## Interaction with open PRs
- **#1115 (A1-PR2)** is in merge queue. B3 doesn't touch
`01-import-boundaries.sh`, the baseline JSON, or the workflow step, so
order-of-merge doesn't matter. Whichever lands first, the other rebases
cleanly.

## Test plan
- [x] 19 existing backend.ts unit tests pass
- [x] Orchestrator runs knip with `duplicates` included, 0 violations
- [ ] CI confirms above
- [ ] Reviewer validates that `backward compatible exports` describe was
the only test coupling to the aliases

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [4248accc](https://github.com/SerendipityOneInc/ecap-workspace/commit/4248acccde09e22c372b02bac94d64a44cd534b5)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T14:12:45Z

**Message:**
```
test(web): UsageCard 全面覆盖 (#894 Step 5 补) (#1119)

## Summary

Epic #894 Step 5 (#899) — 再补一个：\`UsageCard.tsx\` (249 LOC) 从 0% → 全分支，20
tests。

## 新增测试

| 组 | # | 覆盖 |
|---|---|---|
| 内容状态机 | 4 | error / no-data / loading / usage 呈现 |
| Stat tile 值 | 6 | messages user/asst 分解 / latency.count=0 → "—" /
ms→秒格式 (1.2s, p95 2.5s) / sessions / errors + "of N messages" /
toolCalls + uniqueTools |
| 日期预设 | 5 | default=today / yesterday / 7days / preset sticky / loading
→ refresh disabled |
| DailyStrip | 3 | empty / length=1 (阈值>1 隐藏) / length>=2 渲染 bar+tooltip
|
| TopTools | 2 | 空数组隐藏 / slice(0,5) 截断 |

## Harness 要点

- \`vi.setSystemTime(new Date('2026-04-20T12:00:00Z'))\` 固定让
\`dateRange()\` preset 派生日期确定
- i18n mock 返回 key，文案断言全走 key

## Bug-hunting

无新发现。状态机切换合理，preset sticky 逻辑对。

## Test plan

- [x] 20/20 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 5 (#899) 
- 续 DiscordSetupWizard #1112 / ChannelsSection / Slack / Telegram /
Feishu / ModelSection / TimezoneSection / SaveButton (这些已有测试)
- 剩余 Step 5 未覆盖：ConnectorsSection (493 LOC) / DiagnosticsSection (338
LOC) / DiaryCards (150 LOC) / ClawSettingsClient (438 LOC, key parts
~120)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [83a5cade](https://github.com/SerendipityOneInc/ecap-workspace/commit/83a5cade46d88463393461e8d375b8a47bc2d7ef)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T14:01:19Z

**Message:**
```
feat(web): freeze import-boundaries baseline + flip hard gate (A1-PR2) (#1115)

## Summary
- Merges original A1-PR2 (baseline) + A1-PR3 (hard gate) into one
rollout step — same 2-phase pattern as deptry / B2.
- Generates `.dependency-cruiser-known-violations.json` containing the
18 legacy violations frozen via `depcruise-baseline`.
- `01-import-boundaries.sh` drops `WARN_ONLY`, uses `--ignore-known` —
baseline passes, new violations fail CI.
- CI step no longer sets `WARN_ONLY=1`.

## Baseline contents

18 known violations (14 errors + 4 warnings) — same numbers reported in
#1098 warn-mode run:

| Contract | Count |
|----------|-------|
| W1 (lib pure) | 2 |
| W2 (hooks pure) | 3 |
| W3 (contexts pure) | 5 |
| W4 (components below pages) | 2 |
| W5 (feature isolation) | 4 |
| W6 (theme leaf) | 1 |

## Maintenance

Each A1-PR3+ cleanup PR removes a batch of entries from
`web/.dependency-cruiser-known-violations.json` and fixes the matching
imports. The file shrinks monotonically until empty.

Regenerate with:
```bash
pnpm exec depcruise-baseline --config .dependency-cruiser.cjs 'src/**/*.{ts,tsx}'
```

## Local verification
- `pnpm lint:imports` — exit 0, prints `18 known violations ignored`.
- A novel violation (e.g. `src/lib/foo.ts` importing `@/components/Bar`)
would fail the gate since it's not in the baseline.

## Spec changes
The PR matrix in
`docs/superpowers/specs/2026-04-20-web-import-boundaries.md` is updated
from 5 phases to 3 (PR0 spec / PR1 warn / PR2 baseline + hard gate /
PR3+ cleanup). Rationale: after PR1 landed, the `@/*` alias resolver
risk was confirmed resolved, so the extra "soft baseline freeze" step
between warn and hard gate added no safety margin. Mirrors the B track's
2-phase approach.

## Interaction with open PRs
- **#1106 (B2)**: currently sets `WARN_ONLY=1` on its `Web CI-lint
orchestrator` step because A1 was still in warn mode. Once this PR
lands, B2 rebase will drop that env block — the `WARN_ONLY` path is gone
from `01-import-boundaries.sh` and no longer needed.

## Test plan
- [ ] CI `web-quality` job runs new step, `01-import-boundaries.sh`
passes on baseline, exit 0
- [ ] Existing ESLint / TS / unit-test / jscpd / asset-size steps
unchanged
- [ ] PR-size gate passes
- [ ] Reviewer validates the baseline file format (each entry has
`type`, `from`, `to`, `rule.name`, `rule.severity`) and that W1-W6 all
represented

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [ef416402](https://github.com/SerendipityOneInc/ecap-workspace/commit/ef4164027d04434ec615b6b486a51fcf1b00c26c)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T13:57:30Z

**Message:**
```
ci: skip redundant gating on push:main in code-quality.yml (#1038) (#1111)

## Context

Closes #1038. After merge queue was enabled, every PR merge produces
**two** `code-quality` runs against the same commit SHA:

1. **merge_group** (gating, before fast-forward) — must pass to allow
merge
2. **push:main** (after fast-forward) — duplicates all gating, and
occasionally red-crosses main from unrelated flakes

Example: PR #994's merge produced runs
[24558845557](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/24558845557)
(merge_group ✅) and
[24559126136](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/24559126136)
(push ❌, Simulator CoreData teardown flake).

## Approach (issue option A — minimal)

Guard pure gating steps with `if: github.event_name != 'push'` so they
skip on main-branch pushes. Test + coverage + badge publishing steps are
untouched so the iOS/web coverage badges keep updating on every merge.

### Affected steps

| Job | Gating steps now skipped on `push:main` |
|---|---|
| `web-quality` | Lint, ignores SHRINK-ONLY check, Import boundaries
(warn-mode), Type check, jscpd src + tests |
| `ios-quality` | SwiftLint, jscpd src + tests |
| `python-duplication-check` | entire job (guarded at job level) |
| `claw-interface-quality` | entire reusable-workflow job (guarded at
job level) |

The aggregator `code-quality` step is updated to treat `skipped` status
on python jobs as non-failure (previously required `success`).

## Intentionally not addressed

- **iOS unit tests still run on push:main**, because they produce the
coverage artifact the iOS badge step consumes. A Simulator flake during
that step can still red-cross main (which is **issue #1038 acceptance
item 3**). Fixing that requires moving iOS test + badge publishing into
the `merge_group` event instead of `push:main`, which is a larger
architectural change. Tracked in #1116.
- **`on: push: branches: [main]` trigger kept intentionally** so a
manual/bypass push still triggers a run (not a silent no-op). The
improvement comes from step-level skipping, not trigger removal.

## Verification

`act` isn't available in this worktree, so the real verification is the
first post-merge `push:main` run: look for Lint / tsc / jscpd /
SwiftLint rows marked `skipped` in the `ios-quality` + `web-quality`
jobs under the main-branch run.

Meanwhile this PR's own CI (which runs under `pull_request` event)
executes the **full** gating path — confirming the added `if` conditions
don't break the PR-time gate.

## Test plan

- [x] YAML structure reviewed for unintended step ordering / missing-if
errors
- [x] `code-quality` aggregator updated so `python*` jobs in `skipped`
state don't falsely fail
- [ ] Post-merge verification: first `push:main` run after merge should
show Lint/tsc/jscpd/SwiftLint as `skipped`, with `Unit Tests with
Coverage` + badge steps still running

Closes #1038

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [11143a30](https://github.com/SerendipityOneInc/ecap-workspace/commit/11143a3096ff4636f461ff364fcdb2c4ec56eef8)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T13:43:45Z

**Message:**
```
test(web): DiscordSetupWizard 全面覆盖 (#894 Step 5 补) (#1112)

## Summary

Epic #894 Step 5 (#899) 的 setup wizard 三件套对齐 — Slack / Telegram 已有测试，本
PR 补 Discord。
20 tests / +320 source LOC from 0% → 全分支。

## 新增 20 个测试

| 分组 | # | 覆盖点 |
|---|---|---|
| welcome step | 3 | 渲染 / Cancel → onClose / getStarted 推进 |
| create-app step | 3 | 6 步说明 + developer portal link target/rel / back
→ welcome / next → input-token |
| input-token validation | 4 | 空 token / <50 字符 invalid hint / >=50
enabled / back 清 error |
| advanced config toggle | 3 | 折叠默认 / 展开后 dm/group select + account
input / 透传到 addClawChannel payload |
| handleConnect | 5 | 成功路径 + addClawChannel 默认参数 / Error 实例 message 显示 /
非 Error fallback / account 空白→"default" / token trim |
| invite step | 2 | 5 步 invite 说明 / Done → onSuccess+onClose |

## Bug-hunting

`complete` step 是源码 dead branch — 没有 handler 会触发它，纯 UI 无障碍路径。提 issue
或清理看后续收尾 PR。

## Test plan

- [x] 20/20 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 5 (#899)
- 续 Slack / Telegram wizard specs

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [05353087](https://github.com/SerendipityOneInc/ecap-workspace/commit/0535308785099c80be50f745cfadd7b708cc06f0)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T13:42:23Z

**Message:**
```
test(web): GenClawClient 内部组件覆盖 (#894 Step 4) (#1110)

## Summary

Epic #894 Step 4 (#898)。\`GenClawClient.tsx\` 默认导出 1100+ LOC 是整合组件（hooks
+ 布局 + provider 链），走 E2E 更合适。本 PR 聚焦 issue #898
明确点名的两块（**ChatErrorBoundary** + **连接错误 modal**），加上几个纯 UI helper，从
GenClawClient.tsx 导出内部组件让它们可独立受测。

## 源码变动（极小）

- 8 处 \`function\` → \`export function\` / \`class\` → \`export class\`
- 零语义变化、零 runtime 行为变化

## 新增 48 个测试

| 组件 | # | 覆盖点 |
|---|---|---|
| \`formatChannelTime\` | 8 | pure function — 空值 / NaN / 秒 vs 毫秒 自动缩放 /
分钟/小时/天分段 |
| \`ChannelIcon\` | 7 | 6 种平台 emoji 渲染 / 未知平台 SVG fallback /
case-insensitive |
| \`RemoteStatusBadge\` | 8 | 5 种 status → dot 颜色 / unknown fallback /
waiting pulse / message vs status 降级 |
| \`Toast\` | 4 | 渲染 + 4000ms 自动 dismiss / X 按钮立即关闭 / unmount 清 timer |
| \`ConfirmModal\` | 6 | open=false 不渲染 / 默认/自定义 labels /
onConfirm/onCancel / typeToConfirm gate / destructive variant / close 重置
typed |
| \`AdvancedRecreate\` | 5 | 展开/收起 / RECREATE 输入门 / onRecreate 触发 /
Cancel 路径 |
| \`ConnectionErrorModal\` | 5 | headline + status badge / wsError 段 /
reconnect 按钮 / redeploy→ConfirmModal→Confirm / redeploy Cancel |
| \`ChatErrorBoundary\` | 3 | 无错误透传子组件 / getDerivedStateFromError 返回空
partial / componentDidCatch 打 logger.warn + setState updater 增 errorKey
|

## 测试策略

### ChatErrorBoundary — 直接调类方法
React 19 concurrent replay 会同步重放 render 跳过正常 commit 路径，用 \`throw\`
驱动错误边界会 flaky。改为：直接 \`new ChatErrorBoundary()\`，spy setState，调
componentDidCatch 和 getDerivedStateFromError — 100% 确定。

### 其他内部组件 — render + testid + 行为断言
ConfirmModal 里的 "Confirm"/"Cancel" 按钮实际 label 是 t(key) ||
'fallback'。i18n mock 返回 key，所以 DOM 上显示 \`common.cancel\` /
\`genClaw.recreateClaw\`。getAllByText 处理同 label 多元素（modal h3 + button
同文本）。

## 不在本 PR 范围

- **auth 检查分支**：位于默认导出内部（async useEffect 里校 uid + router.push）。要测就得 mock
60+ 依赖或直接渲染默认导出 — 性价比太低，issue 里"auth 检查"留给 E2E 或后续独立 PR。
- **useEffect 里抛错是否被 ErrorBoundary 捕获**：issue bug-hunting 里提到；已在
ChatErrorBoundary 说明 componentDidCatch 只捕 render/children 抛错，effect 抛错是
React 已知 gotcha，不在本 PR 范围。

## Test plan

- [x] 48/48 GenClawClient.internals 测试通过
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [ ] CI 绿

## 关联

- Epic #894 Step 4 (#898)
- #898 还剩 \`GenClawClient.tsx\` 默认导出的 auth 检查分支（超出本 PR），建议等 E2E 补

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [630953e5](https://github.com/SerendipityOneInc/ecap-workspace/commit/630953e573fcf8f3ec9e2929f2b5f9d25ff07366)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T13:38:44Z

**Message:**
```
feat(web): wire knip for dead code / dep health gate (B2) (#1106)

## Summary
- Wires **knip** as a hard gate for dep-health categories in `web/` CI.
- Content-level categories (files / exports / types / duplicates) are
reported informationally; hard-gated in later B-track PRs.
- Implements all three rounds of #1095 review feedback directly.
- B2 scope: **install + baseline freeze + hard gate for dep-health
only**.

## Baseline (absorbed in `knip.config.ts`)

| Category | Count | Handling |
|----------|-------|----------|
| Unused dependencies | 7 | `ignoreDependencies` baseline legacy — B4
cleans |
| Unlisted dependencies | 1 (`postcss`) | `ignoreDependencies` — B4 adds
explicitly |
| Unlisted binaries | 1 (`tsx`) | `ignoreBinaries` — B4 `pnpm add -D
tsx` |
| Permanent FPs | 2 | `eslint-config-next` + `@vitest/expect` — kept
separate |
| Unused files | 28 | Informational (B5) |
| Unused exports | 39 | Informational (B6+) |
| Unused types | 58 | Informational (B6+) |
| Duplicate exports | 6 | Informational (B3 first target) |

`pnpm lint:deadcode` exit 0 locally. Dep-health hard gate clean: 0
violations outside the allowlist.

## #1095 review feedback addressed in this PR

From round 2:
- ✅ `eslint-config-next` as permanent FP (FlatCompat string ref)
- ✅ `@vitest/expect` as permanent FP (`declare module` augmentation in
`web/jest-dom.d.ts:20`)
- ✅ App Router metadata entries (`robots.ts` + preventive `sitemap` /
`manifest` / OG images / icons)
- ✅ knip version pinned to exact `6.5.0` (no caret)

From round 3:
- ✅ `project` glob includes `.mts`
- ✅ `tsx` correctly scoped to `ignoreBinaries` (rather than
`ignoreDependencies`)
- ✅ Independent `02-dead-code.sh` script, decoupled from A1's
`00-run-all.sh` to avoid merge-order coupling between A track and B
track

## Rollout contract
B2 gate covers: `dependencies / devDependencies / unlisted / binaries /
unresolved / optionalPeerDependencies`. Content categories ship in:
- **B3** → promote `duplicates` to hard gate + clean 6 in
`src/lib/api/backend.ts`
- **B5** → promote `files` + delete 28 unused files
- **B6+** → promote `exports / types / enumMembers / ...`
module-by-module

Each category-promotion PR adds its type to the `--include` list in
`02-dead-code.sh` and removes the corresponding allowlist entries.

## Test plan
- [x] `pnpm lint:deadcode` exit 0 locally
- [x] Full report prints 131 informational items then dep-health gate
prints 0 violations
- [ ] CI `code-quality / web-quality` runs new step, gate passes
- [ ] Existing ESLint / TS / unit-test / jscpd steps unchanged
- [ ] Reviewer validates `ignoreDependencies` permanent vs legacy split
is correctly commented

## Notes
- Runs independently of A1-PR1 (#1098). Both PRs add files under
`web/scripts/ci-lint/` but non-overlapping (`02-*` here, `00-*` / `01-*`
there); git auto-merge should resolve cleanly.
- `@sentry/cloudflare` in the legacy list with a comment — may resolve
via `src/instrumentation.ts`; B4 to verify before removing.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [20e8e062](https://github.com/SerendipityOneInc/ecap-workspace/commit/20e8e0623c0bfa80b73e5d8d1dedc170d9917490)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T13:33:15Z

**Message:**
```
chore(web): promote tests/ no-unused-vars from warn to error (#1073) (#1114)

Follow-up to #1109, which cleared the 23-warning backlog.

With the backlog at zero, flipping severity to `error` is the missing
piece — the lint script runs `eslint src/ tests/ --quiet`, which
silently filters warnings out of CI output, so warn-level here was
effectively a no-op. Error-level means future regressions actually break
the build.

## Summary

- `web/eslint.config.mjs` `tests/` override:
`@typescript-eslint/no-unused-vars` from `'warn'` → `'error'`
- Kept the existing `^_`-prefix ignore patterns untouched (so
deliberately-unused destructures like `_setMessages` still pass)

## Test plan

- [x] `pnpm --filter web lint` — clean (exit 0)
- [x] Quick sanity: manually introduced a bogus unused var locally,
confirmed lint now fails
- [x] Depends on #1109 being merged to main (confirmed at the time of
branching this PR off `origin/main`)

Closes #1073

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [7fdf7f08](https://github.com/SerendipityOneInc/ecap-workspace/commit/7fdf7f08be76b0b096cc76ab65fcc0eff5c15844)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T13:16:52Z

**Message:**
```
chore(web): clean up 23 no-unused-vars warnings in tests/ (#1109)

Preparatory cleanup so the follow-up PR can promote
`@typescript-eslint/no-unused-vars` from `warn` to `error` in the
`tests/` override without CI going red. Currently silenced by `eslint
src/ tests/ --quiet` in the `lint` script, so warnings have been
accumulating invisibly.

## Summary

- 3 unused imports: `beforeEach`, `waitFor`, `AuthSubscribe` type
- 1 motion stub destructure in PaywallContent: rename
`initial`/`animate`/`exit`/`transition` to underscore-prefixed so they
still get stripped out of DOM props but satisfy the `/^_/u` pattern
- 12 unused `setMessages` destructures in
`useCanvasSession.unit.spec.ts`: rename to `_setMessages` (helper
returns both the mock and `result`; tests only assert on `result`)
- 3 unused `handlers` destructures in `useOpenClawChat.unit.spec.ts`:
dropped from destructuring
- 1 unused `callbacks` destructure in `useSSEStream.unit.spec.ts`:
dropped
- 4 stale `// eslint-disable-next-line
@typescript-eslint/no-explicit-any` directives that had no matching
warning (auto-fixed by `eslint --fix`)

Zero behavior change, zero test coverage change — purely removing dead
bindings.

## Follow-up

Next PR will:
1. Promote `@typescript-eslint/no-unused-vars` from `warn` to `error` in
the tests/ override (`web/eslint.config.mjs:458-466`)
2. Keep `--quiet` in the lint script (other warning-level rules would
otherwise flood CI logs)

Tracking #1073.

## Test plan

- [x] `npx eslint tests/ --rule '{"@typescript-eslint/no-explicit-any":
"off"}'` — 0 warnings, 0 errors (was 23+4)
- [x] `pnpm --filter web test:unit useCanvasSession useOpenClawChat
useSSEStream useArtifactsSidebar useMattermostIntegration GeneralTab
PaywallContent` — 160/160 pass
- [x] `pnpm --filter web lint` — clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [01f9c695](https://github.com/SerendipityOneInc/ecap-workspace/commit/01f9c69550b6b738aa89fcdc5095517debecf6cf)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T13:09:21Z

**Message:**
```
test(web): OpenClawThread 全面覆盖 (#894 Step 3 补) (#1107)

## Summary

Epic #894 Step 3 (#897) 剩下的最后一个文件。其余 5 个 Step 3
文件（OpenClawAssistantMessage / OpenClawUserMessage / useArtifactsSidebar
/ useMattermostIntegration / useOpenClawRuntime）都已经有测试 — 本 PR 把
\`OpenClawThread.tsx\` (380 LOC) 从 0% 补到全分支。

## 新增 30 个测试

| 分组 | 数量 | 覆盖点 |
|---|---|---|
| historyLoaded / awaitingGreeting 门控 | 5 | Empty 分支 / "Setting things
up" 横幅 / compact 变体 bypass |
| Load older messages | 4 | hasMore / loadingMore disabled / 点击回调 |
| QuickActionCards 可见性 | 8 | 8 条显示门控全覆盖（messageCount / historyLoaded /
awaitingGreeting / thread.isRunning / compact / onSendMessage /
showQuickActions / agentId 透传）|
| UserMessageFactory | 4 | \`__SESSION_DIVIDER__\` → SessionDivider 分流 /
isLastMessage / compact 透传 |
| AssistantMessageFactory | 5 | isConsecutive 4 种组合（首条 / 前条 user / 前条
assistant / 前条 tool-group）+ props 透传 |
| auto-scroll 副作用 | 2 | 新 user 消息 → scrollTo instant / 新 assistant 不触发 |
| ScrollToBottomButton | 2 | 阈值下隐藏 / 阈值上显示+点击滚动 |

## Harness 要点

**\`@assistant-ui/react\` mock**：\`useMessage()\` 需要 per-message 上下文，用
\`React.createContext\` 模拟 — 模块级变量会被 lazy JSX eval 覆盖成最后一次迭代值（classic
closure pitfall，已踩过一次）。

**jsdom \`scrollTo\` 缺失**：\`HTMLElement.scrollTo\` 在 jsdom 里没实现；用
\`Object.defineProperty(el, 'scrollTo', { configurable: true, value:
vi.fn() })\` 手搭，不能用 \`vi.spyOn\`（spyOn 要求属性存在）。

**子组件 stub**：OpenClawUserMessage / OpenClawAssistantMessage /
QuickActionCards 都 stub 成 testid + 数据属性，让 factory 透传逻辑能够直接 snapshot。

## Bug-hunting

无新发现。ackActive / isConsecutive / isLastMessage 计算逻辑都合理；auto-scroll 只在新
user 消息上触发（正确）；ScrollToBottomButton 的 200px 阈值 + scrollHeight
判可滚动的条件都合理。

## Test plan

- [x] 30/30 OpenClawThread 测试通过
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [ ] CI 绿

## 关联

- Epic #894 Step 3 (#897)
- Step 3 所有文件覆盖后 #897 可 close（5 个已测 + OpenClawThread 本 PR）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [3715f6c2](https://github.com/SerendipityOneInc/ecap-workspace/commit/3715f6c2a66cf3b0219f9d698adcbcaa20079584)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T13:04:12Z

**Message:**
```
test(web): SlackSetupWizard try/finally + ChannelsSection effect deps (#1066 + #1074 part 1) (#1105)

Two non-bug hygiene items from the review follow-up queue. Small PR
intentionally — each item alone is < 10 lines, but they share the
"review follow-up polish" model, so bundling avoids churn.

## 1. SlackSetupWizard spec robustness (#1066)

- Wrap the `process.on('unhandledRejection', ...)` listener in
`try/finally` so the handler is removed even if an `expect()` above
throws. This matches the `try/finally` pattern already in place for the
fake-timer test earlier in the same file.
- Fix the `onUnhandled` signature from `(e: PromiseRejectionEvent |
Error)` to `(reason: unknown)`. Runtime behavior was fine — Node calls
the handler with `(reason, promise)` and the existing `caught.push(e)`
happened to receive `reason` — but the type was misleading to future
readers.

## 2. ChannelsSection `ChannelCard` effect deps (#1074 part 1)

- Add `onPairingExpanded` to the `useEffect` deps array; remove the
`eslint-disable-line react-hooks/exhaustive-deps`.
- Parent re-renders pass a fresh closure each render, but
`autoExpandPairing` only flips true when the channel list changes, so in
the worst case this fires one extra idempotent `setPairing(true)` +
`onPairingExpanded?.()`. Both are no-ops on repeat.
- Benefit: removes a stale-closure risk for any future caller whose
callback identity is less stable than today's `onClearLastAdded`.

### Skipped: #1074 part 2 (spec file split)

Not included. Low-priority maintainability; splitting ~600-line spec
into 3–4 files would risk jscpd duplication drift (mocks/factories
replicated across files). Can revisit if the spec ever becomes painful
to debug.

## Test plan

- [x] `pnpm --filter web test:unit SlackSetupWizard ChannelsSection` —
79/79 pass (30 + 49)
- [x] `pnpm --filter web lint` — clean
- [x] `npx tsc --noEmit` — clean

Closes #1066
Closes #1074

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [54b6a7b8](https://github.com/SerendipityOneInc/ecap-workspace/commit/54b6a7b847321cb1a3ce7497829b45890cabc2f6)

**Author:** peter-srp  
**Date:** 2026-04-20T12:51:03Z

**Message:**
```
fix(web): stop reporting MM connection errors to Sentry (#1103)

## Summary
- Removes `Sentry.logger.error/warn` calls from
`captureMMConnectionFailure` — these bypass `beforeSend` and were still
consuming 10K+ events/user/hour, overwhelming Sentry quota
- Retains breadcrumb-only reporting (free, provides context for
subsequent real errors)
- `beforeSend` filter in `sentry.client.config.ts` kept as safety net
for old cached releases
- Removes now-unused `sanitizeURL` helper and `sanitizeUrl` import

## Context
Sentry issue: https://serendipity-one-inc.sentry.io/issues/7401127622/

Previous attempts (dedup windows → Sentry Logs migration) failed because
`Sentry.logger.*` with `enableLogs: true` still creates issues and
consumes event quota, unlike `beforeSend` which only intercepts
`captureException`/`captureMessage`.

## Test plan
- [x] Unit tests updated and passing (`connectionDedup.unit.spec.ts` — 6
tests)
- [x] Lint passes
- [ ] Verify on staging that the Sentry issue stops receiving new events

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

---

## [6202a27b](https://github.com/SerendipityOneInc/ecap-workspace/commit/6202a27b3c2956ca4ac68a208d6d6738c392e044)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T12:49:24Z

**Message:**
```
feat(web): wire dependency-cruiser for import boundaries (A1-PR1, warn mode) (#1098)

## Summary
- Wires **dependency-cruiser** as the engine for W1–W6 import
architecture contracts.
- CI runs in **warning mode** (`WARN_ONLY=1`) — violations print but
don't fail the build.
- A1-PR2 freezes the baseline into an allowlist; A1-PR3 flips the hard
gate.
- Also applies review feedback on the A1 spec merged in #1094.

## Baseline (from this config)
**14 errors + 4 warnings** across the 609 modules / 1645 dependencies
cruised. Hot spots:

| Contract | Count |
|----------|-------|
| W1 (lib pure) | 2 |
| W2 (hooks pure) | 3 |
| W3 (contexts pure) | 5 |
| W4 (components below pages) | 2 |
| W5 (feature isolation, warn-level) | 4 |
| W6 (theme leaf) | 1 |

More than the ~6 grep-based estimate in the spec because
dependency-cruiser also follows relative-path imports and re-exports,
which grep missed.

## Changes

### New files
- `web/.dependency-cruiser.cjs` — W1–W6 rules, proper `\[locale\]` regex
escaping, tsconfig resolver
- `web/scripts/ci-lint/00-run-all.sh` — CI-lint orchestrator (mirrors
`services/claw-interface/scripts/ci-lint/` layout)
- `web/scripts/ci-lint/01-import-boundaries.sh` — dep-cruiser runner
with `WARN_ONLY` switch

### Modified
- `web/package.json` — `lint:imports` / `lint:ci` scripts,
`dependency-cruiser` devDep
- `.github/workflows/code-quality.yml` — new "Import boundaries check
(warn mode, A1-PR1)" step in `web-quality` job
- `docs/superpowers/specs/2026-04-20-web-import-boundaries.md` — applies
review feedback from #1094 (see below)

## #1094 review feedback addressed
1. **W1 extended to forbid `lib → theme`** (Option A per decision).
`seo.ts → brand-assets` becomes a real W1 violation, fixable in A1-PR4+
by moving brand-assets to `src/config/brand/` or `src/lib/brand/`.
2. **`[locale]` regex pitfall** documented in spec's 风险与缓解 section and
applied to W5 patterns in the config (`\\[locale\\]`).
3. **Layer diagram** clarified with explicit `hooks → contexts`
direction annotation.

Non-blocking Codex suggestions (W5 shared-directory definition, grep
reproducibility) deferred to A1-PR2.

## Local verification
- `pnpm lint` (ESLint) — pass
- `pnpm lint:imports` (WARN_ONLY=0) — exit 14, prints all 14 errors + 4
warns
- `WARN_ONLY=1 pnpm lint:ci` — exit 0, prints warnings but doesn't fail
- Config uses escaped `\\[locale\\]` and `tsConfig +
enhancedResolveOptions` — verified dep-cruiser resolves `@/*` aliases
(609 modules cruised vs earlier 2-module dry-run without resolver)

## Test plan
- [ ] CI `code-quality / web-quality` job runs new step, logs baseline
violations, does not fail build
- [ ] Existing ESLint / TS / unit-test / jscpd steps still pass
- [ ] PR-size gate passes (~180 new lines excluding lockfile)
- [ ] Reviewer to validate the W5 regex capture-group approach (`$1`
reference) works as expected vs an explicit feature-name whitelist

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [57aad0ba](https://github.com/SerendipityOneInc/ecap-workspace/commit/57aad0baa3c275600285a5224efeda027163e181)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T12:46:51Z

**Message:**
```
chore(web): remove dead verify step from TelegramSetupWizard (#1096)

## Summary

- Removes the unreachable `verify` step from `TelegramSetupWizard`
(`setStep('verify')` was never called)
- Drops the dead `pairCode`/`pairSaving` state, `handleApprovePairing`
handler, verify UI block, `approveChannelPairing` import
- Drops `verifyTitle` / `verifyDesc` i18n keys across 10 locale files
(unused after the UI block removal)
- Strips the corresponding mock + comment from the wizard's unit spec

The API-level `approveChannelPairing` is retained — it is still used by
the generic pairing flow in `useClawSettings.ts` (surfaced through
`ChannelsSection`'s inline pairing panel). `pairingCodePlaceholder` also
stays for that reason.

Fixes #1064 (part 1 of 2). Part 2 (hardcoded `allow_from: ['*']` while
the `allowlist` policy is still offered) is left open pending a product
decision on whether `allowlist` mode should expose a real whitelist UI
control.

## Test plan

- [x] `pnpm --filter web test:unit TelegramSetupWizard` — 24/24 tests
pass
- [x] `pnpm --filter web lint` — clean
- [x] `npx tsc --noEmit` — clean
- [x] Verified `grep -r "verifyTitle\|verifyDesc"` returns no matches
- [x] Verified wizard happy path tests still cover welcome → create-bot
→ input-token → configuring → complete

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [c70ae11c](https://github.com/SerendipityOneInc/ecap-workspace/commit/c70ae11cbedf41563024e2ccb05730e7fee8404d)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T12:44:35Z

**Message:**
```
docs(web): add dead code / dep health spec (B1) (#1095)

## Summary
- Design spec for dead code + dependency health CI gate in `web/` using
**knip**.
- First PR of the **B track** (parallel to the A track / import
boundaries via dependency-cruiser, spec merged in #1094).
- Pure doc — no code changes, no CI gates added.

## Context
Mirrors the claw-interface CI quality bar (ruff / pyright / 6
import-linter contracts / jscpd / **deptry** / coverage 90%). `web/` has
`@typescript-eslint/no-unused-vars` (single-file) but **no cross-file
dead code / dep health tooling**. This spec fills that gap with a single
tool (knip) covering unused exports / files / deps / devDeps / unlisted
/ duplicates / binaries.

See `docs/superpowers/specs/2026-04-20-web-dead-code.md` for:
- Tool selection rationale (knip over ts-prune + depcheck +
eslint-plugin-unused-imports)
- Baseline from `npx knip` dry-run: ~120 violations (6 files, 6 unused
deps, 3 unused devDeps, 1 unlisted dep, 1 unlisted binary, 39 unused
exports, 58 unused exported types, 6 duplicate exports)
- 2-stage rollout (spec → wire-up + baseline freeze + hard gate in one
PR)
- Category-based cleanup order (duplicates → unused deps → unused files
→ exports by module)
- FP risk areas (Playwright setup files, dynamic imports, pnpm-hoisted
transitives)

## Non-goals
- Does **not** tighten existing thresholds (complexity 25 / max-lines
500 / coverage 55% stay).
- Does **not** tighten `tsconfig` (already strict).
- Does **not** introduce ts-prune / depcheck /
eslint-plugin-unused-imports (knip covers all).

## Test plan
- [x] Markdown renders correctly
- [ ] Reviewer validates knip over three-tool composite rationale
- [ ] Reviewer reviews baseline categorization (duplicate exports in
`src/lib/api/backend.ts` are 1st target — low-risk, high signal)
- [ ] No CI gates triggered (pure doc PR)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [5ef59521](https://github.com/SerendipityOneInc/ecap-workspace/commit/5ef5952169254093fa33a5d9108f8d87d8a880b5)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T12:42:47Z

**Message:**
```
test(web): SubscriptionPanel 全面覆盖 (#896 Step 2 Part B) (#1097)

## Summary

Epic #894 Step 2 Part B — 覆盖 701 LOC 的 SubscriptionPanel.tsx 从 0% → 全分支。
续 #1076（Part A：SuccessClient + OnboardingSuccessClient）。

### 新增 35 个测试

| 分组 | 数量 | 覆盖点 |
|---|---|---|
| Provider + context | 3 | openPanel / closePanel / outside-provider
no-op |
| Close behaviors | 1 | Escape key 关面板 |
| Billing cycle toggle | 1 | yearly 默认 + Monthly 切换传递到 PlanCard |
| handleAction (subscribe/upgrade/switch-cycle) | 6 | !isLoggedIn /
downgrade 分流 / happy path / createOrder fail / postAPI 无 url / 无 uid 静默
|
| handleTopupPurchase (Buy) | 4 | active 付费 / 非 active toast /
!isLoggedIn / createOrder fail |
| openCustomerPortal (Edit billing) | 5 | 无 uid / 成功 /
no-Stripe-customer / 通用错误 / 异常 finally 清 portalLoading |
| handleDowngradeConfirm | 4 | 成功 refresh+toast / 失败保留模态 / 异常 / close
按钮清 target |
| Cancel subscription onConfirm | 4 | 成功关 panel / 失败保留 / 网络异常 / 无 uid 静默
|
| Conditional UI | 6 | pendingDowngrade 横幅 / cancelAtPeriodEnd+Renew /
错误 banner / isActiveSub 切换 / Keep Current Plan toast |
| Contact Support | 1 | openSupportTicket('billing') |

### Harness 要点（踩坑记录）

**Modal stub 必须 stopPropagation**：DowngradeConfirmModal /
CancelConfirmModal 在源码里是 backdrop div (onClick=onClose) 的子节点，真实 modal 用
React portal 绕开；stub 直接内联在同一棵 DOM 里，测试里 fireEvent.click 会冒泡到 backdrop →
关掉整个 panel 让后续断言挂掉。两个 stub 的外层 div 加 `onClick={e =>
e.stopPropagation()}`。

**PlanCard stub**：PlanCard 有独立 spec 覆盖渲染；这里只 stub 成
subscribe/upgrade/downgrade 三个 testid 按钮，专注测 panel 自己的 handleAction
分流逻辑。

## Bug-hunting

无发现需 follow-up 的 bug。Panel 的错误处理合理，三个主要异步 handler (handleAction /
handleTopupPurchase / openCustomerPortal) 都有 try/catch，Sentry capture
正确绑 \`confirm_api_error\`。

## Test plan

- [x] 35/35 SubscriptionPanel 测试
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [ ] CI 绿

## 关联

- Epic #894 Step 2 (#896) — Part A #1076 + Part B 本 PR → #896 可 close
- 续 #1076（Part A post-purchase UX）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [bb826bdb](https://github.com/SerendipityOneInc/ecap-workspace/commit/bb826bdb2a6bdcac5f97d8dc1a49687f225aa4e9)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T11:26:03Z

**Message:**
```
test(web): payment success clients 覆盖 (#896 Step 2 Part A) (#1076)

## Summary

Epic #894 Step 2 的第一部分。覆盖两个 payment-success UI entry point，从 0% → 全分支。
SubscriptionPanel.tsx (701 LOC) 作为 Part B 单独 PR（体量不宜合并）。

### 新增 24 个测试

**SuccessClient** (14 tests, subscription/success/SuccessClient.tsx 298
LOC)
- 参数校验：missing session_id / missing order_id → error UI
- 4 个主状态分支：loading → redirecting、loading → pending refresh、loading →
error、loading → success-render
- 3 条 redirect
触发条件：`order_status='completed'`、`payment_status='paid'`、`payment_status='no_payment_required'`（free
tier）
- subscription vs credits 分支渲染
- 未知 plan tier → 回退 "Pro" + 20,000 credits
- subscription_info 缺失 → 不渲染 details 块
- localStorage ONBOARDING_PROGRESS paymentCompleted 标记
- JSON.parse 坏数据 → 静默 catch，redirect 仍进行

**OnboardingSuccessClient** (10 tests,
onboarding/success/OnboardingSuccessClient.tsx 92 LOC)
- userInfo.uid gate：无 uid → 停在 loading
- missing session_id / missing order_id → error 状态
- success 流：localStorage 标记 + router.push('/chat') 1500ms 后
- processedRef 防重复执行（re-render 不再触发 handlePaymentSuccess）
- `Error` 实例 vs bare object 错误兜底（'Unexpected error'）
- error 状态 "Go to chat" 按钮

### 不在本 PR 范围

- SubscriptionPanel.tsx (701 LOC, 0%) — Part B 单独 PR
- BillingTab.tsx — 已被移除（current: GeneralTab + UsageTab）
- 其他 Step 2 清单文件已有测试（DowngradeConfirmModal / InvoiceHistory /
SharedPlanCard / PaywallContent / CreditsDisplay / stripe API routes）

### Bug-hunting

未发现需要 follow-up issue 的 bug。两份 UI 的状态机合理，localStorage 使用有合理 catch；Stripe
params 在 \`handlePaymentSuccess\` 里处理（已有测试）。

## Test plan

- [x] 14/14 SuccessClient + 10/10 OnboardingSuccessClient 通过
- [x] 3273/3273 全量 unit 测试
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [ ] CI 绿

## 关联
- Epic #894 Step 2 (#896)
- 续：Part B 即将覆盖 SubscriptionPanel.tsx

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [5d45acf3](https://github.com/SerendipityOneInc/ecap-workspace/commit/5d45acf3e55844f293aa5d5774e06a88ec8110f8)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T11:30:52Z

**Message:**
```
docs(web): add import boundaries spec (A1-PR0) (#1094)

## Summary
- Design spec for web/ import architecture constraints (W1–W6).
- First PR of the **A1 track** (import boundaries via
dependency-cruiser).
- Paired B1 track (dead code via knip) will ship in parallel.
- Pure doc — no code changes, no CI gates added.

## Context
Mirrors the claw-interface CI quality bar (ruff / pyright / 6
import-linter contracts / jscpd / deptry / coverage 90%). `web/` already
covers per-file rules (complexity 25 / max-lines 500 / jscpd 5.5% /
Tailwind semantics / asset-size-guard / PR-size gate) but has **zero
tooling for cross-file architectural constraints**. This spec fills that
gap.

See `docs/superpowers/specs/2026-04-20-web-import-boundaries.md` for:
- Layer model (theme/config → lib → hooks/contexts → components → app)
- W1–W6 contracts
- Tool selection rationale (dependency-cruiser over
eslint-plugin-boundaries)
- Initial grep-based baseline (~6 direct violations — W3 already clean)
- 5-PR rollout sequence (spec → wire-up in warn mode → baseline freeze →
hard gate → violation cleanup)

## Non-goals
- Does **not** tighten existing thresholds (complexity 25 / max-lines
500 / coverage 55% stay).
- Does **not** add pre-commit hook (worktree + husky conflict per
existing convention).
- Does **not** introduce sonarjs / type-coverage.

## Test plan
- [x] Markdown renders correctly (GitHub preview)
- [ ] Reviewer validates W1–W6 contract semantics against web/ domain
intent
- [ ] Reviewer confirms dependency-cruiser > eslint-plugin-boundaries
trade-off
- [ ] No CI gates triggered (pure doc PR)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [16f7f368](https://github.com/SerendipityOneInc/ecap-workspace/commit/16f7f3680bd84e0310f0701160623ada0b1efbf7)

**Author:** bill-srp  
**Date:** 2026-04-20T09:26:34Z

**Message:**
```
fix(ios): Scope code signing settings to correct targets (#1091)

## Summary

Fixes the **Deploy iOS (Staging)** build failure caused by provisioning
profile mismatch ([failed
run](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/24656532866/job/72091350956)).

`update_code_signing_settings` without a `targets` parameter applies to
**all** native targets. The second call (NotificationService extension)
was overwriting the first (main app), leaving the `ZooClaw` target with
the extension's provisioning profile — which lacks Push Notifications
and Sign In with Apple capabilities.

**Fix:** Add `targets:` parameter to scope each call to its intended
target:
- `ZooClaw` → main app profile
- `ZooClawNotificationService` → extension profile

Applied to both `staging` and `release` lanes.

## Test plan

- [ ] Re-run Deploy iOS (Staging) workflow on this branch
- [ ] Verify build completes without provisioning profile errors
- [ ] Verify IPA is produced and uploaded to TestFlight
```

---

## [21f5edeb](https://github.com/SerendipityOneInc/ecap-workspace/commit/21f5edeb8ad8b10117e8edccf2dbba14203cdb8d)

**Author:** peter-srp  
**Date:** 2026-04-20T09:23:49Z

**Message:**
```
feat(web): replace admin session logs with order history (#1092)

## Summary
- Replace the deprecated "日志" (session logs) button with "充值历史" (order
history) in the admin users table
- New `OrderHistoryModal` displays date, type, credits, amount, and
status columns — reuses existing `getOrdersList` API
- Remove deprecated `SessionLogsModal`, `useSessionLogs` hook, and
associated tests

## Test plan
- [ ] Open admin dashboard → Users tab → click "充值历史" button on a user
row
- [ ] Verify modal shows order history table with correct data
- [ ] Verify modal shows empty state for users with no orders
- [ ] Verify loading spinner appears while fetching
- [ ] Verify Escape key closes the modal
- [ ] Verify error toast on API failure
- [ ] `pnpm vitest run tests/unit/app/admin/` — all 43 tests pass

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

---

## [7643e984](https://github.com/SerendipityOneInc/ecap-workspace/commit/7643e9844bf8aa5ad61d7121fd3ec8063f4f936b)

**Author:** Fangmiao-srp  
**Date:** 2026-04-20T08:50:16Z

**Message:**
```
feat(web): add page_view conversion label for Google Ads (#1089)

## What
在 `tracking.ts` 的 `CONVERSION_LABELS` 中填入 page_view 的 Google Ads
conversion label。

## Why
Google Ads 需要 conversion label 才能追踪 page_view 转化。之前 label 为
null，`sendConversion` 直接跳过。

## Changes
- `tracking.ts`: `page_view: null` → `page_view:
'AW-18078707186/LNs9CJnnJp8cEPLbzKxD'`

## Impact
用户触发 `trackPageView` 时，除了发 GA4 事件和 Reddit Pixel，现在会额外发一条 Google Ads
conversion 事件。

---------

Co-authored-by: Muyao Wang <muyao@MuyaodeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```

---

## [2748e8c6](https://github.com/SerendipityOneInc/ecap-workspace/commit/2748e8c6bd25c601578864f7261d9ea7ea433bc7)

**Author:** peter-srp  
**Date:** 2026-04-20T08:44:24Z

**Message:**
```
fix(web): require both WS+MM for connection status + anti-jitter debounce (#1090)

## Summary
- **双通道状态判定**：连接状态现在要求 WebSocket（bot 健康探针）和
Mattermost（消息通道）同时连接才显示"已连接"。修复了 MM 连接但 bot 实际不可达时仍显示绿色的问题。
- **非对称防抖**：connected → 断开方向延迟 3 秒（抑制网络抖动闪烁），恢复连接立即生效，error/initializing
等紧急状态立即穿透。
- **统一状态源**：Header badge 和 Input 框现在共享同一个 `useStableConnectionStatus`
hook，不再各自计算。

## Changes
- New: `web/src/hooks/useStableConnectionStatus.ts` — 统一状态计算 + 非对称防抖
hook
- Modified: `web/src/components/ClawPageHeader.tsx` — 使用新 hook 替代内联状态计算
- Modified: `web/src/app/[locale]/chat/GenClawClient.tsx` — Input 状态改用
stableStatus
- Updated: `web/tests/unit/components/ClawPageHeader.unit.spec.ts` —
测试覆盖新语义

## Test plan
- [ ] tsc --noEmit 通过
- [ ] 单元测试通过（8 cases）
- [ ] 验证正常连接时显示绿色"已连接"
- [ ] 断开网络 < 3 秒，右上角状态不变
- [ ] 断开网络 > 3 秒，显示"重新连接"
- [ ] 恢复网络后立即变回绿色
- [ ] Bot 重启时显示"重启中"（橙色）
- [ ] WS 连接但 MM 未连接时显示"重新连接"

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

---

## [e7a8a69b](https://github.com/SerendipityOneInc/ecap-workspace/commit/e7a8a69bc9fd01aba25fb734ce7361eddd33882c)

**Author:** nolan-srp  
**Date:** 2026-04-20T08:06:33Z

**Message:**
```
fix(web): filter HEARTBEAT status summaries from chat (#1087)

## Summary
- filter assistant/system chat output that contains HEARTBEAT.md status
summaries
- keep ordinary HEARTBEAT.md mentions and generic status messages
visible
- cover history and streaming message paths for the new filtering
behavior
```

---

## [99018c24](https://github.com/SerendipityOneInc/ecap-workspace/commit/99018c2402f1fb9797b7aa04e1d528bb409932b5)

**Author:** bill-srp  
**Date:** 2026-04-20T07:54:23Z

**Message:**
```
fix(ios): add NotificationService extension provisioning to Fastfile (#1088)

## Summary
- Add provisioning profile setup for `ZooClawNotificationService`
extension in both staging and release Fastlane lanes
- `match` now fetches profiles for both the main app and the
notification extension
- `update_code_signing_settings` and
`export_options.provisioningProfiles` updated to include extension
bundle IDs
- Fixes TestFlight upload failure: `CFBundleIdentifier Collision` caused
by missing extension provisioning

## Test plan
- [ ] Re-run staging build workflow and verify TestFlight upload
succeeds
- [ ] Verify production release lane also works with extension
provisioning
```

---

## [ebfb1676](https://github.com/SerendipityOneInc/ecap-workspace/commit/ebfb1676cc17f72fb101e1f6c45253468dfeaa8c)

**Author:** Leo-srp  
**Date:** 2026-04-20T07:26:08Z

**Message:**
```
feat: proxy_client_id_header + fix Claw Tools toggle (#987)

## Summary

**Backend:**
- `proxy_client_id_header` in SKILL.md metadata for providers needing
OAuth client_id as a header
- Fetch client_id from Nango via `GET
/integrations/{provider}?include=credentials`
- Inject as `Nango-Proxy-{header}` at tool execution time

**Frontend:**
- Fix invisible toggle switch: `bg-input` track + `ring-1 ring-black/5`
knob

Replaces #926 (closed due to merge conflicts from executor extraction)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## [eb1c7333](https://github.com/SerendipityOneInc/ecap-workspace/commit/eb1c733310e9a5f7c3cee153f9dc43111e5228b3)

**Author:** kaka-srp  
**Date:** 2026-04-20T07:16:54Z

**Message:**
```
fix(eca-501): skip new-user wallet probe + retry bootstrap on 502/504 (#1086)

## Context

Linear: [ECA-501](https://linear.app/srpone/issue/ECA-501) —
billing-gateway + claw-interface emit ~1,265 / 24h billing 404 errors in
prod.

Prod log analysis broke this down into three classes:

| Class | 24h count | Source |
|---|---:|---|
| `[BILLING_CLIENT] HTTP 404` on `get_credits` after new-user bootstrap
| **126** | `_resolve_existing_wallets` probe; self-healing; not
user-facing |
| `[BILLING_INIT] Failed to initialize` (409 → `get_user` 404) | ~11 |
409/404 race when bg has partial state from a prior failed bootstrap |
| `[BILLING_INIT] Failed to initialize` (500 from bg bootstrap) | ~27 |
bg's upstream LiteLLM call times out |

This PR targets the first two classes. The 500 class is on the bg side
and will be tracked separately.

## Changes

### 1. Skip `_resolve_existing_wallets` probe for newly-created users

`bootstrap_user` now returns `_newly_created: bool` in the response
dict:
- `True` when bg returns 2xx (customer created this call)
- `False` when bg returns 409 (user existed) — via either the 409 body
or the `get_user` fallback

`_do_billing_init` skips the `get_credits` probe when
`_newly_created=True`. For new users, the probe was guaranteed to 404
because Lago's wallets index hadn't caught up with the just-created
customer (~300ms lag) and was then swallowed — pure log noise. The probe
is still useful for 409 / partial-init recovery, so it stays on that
path.

Expected effect: **~126/24h `BILLING_CLIENT HTTP 404` → ~0**.

### 2. Retry bootstrap POST on 502/504

Bg's distributed lock now makes bootstrap idempotent, so retries are
safe. On gateway-level transients (502/504, typically LiteLLM upstream
hiccup), we retry 2 more times with 0.5s + 1.5s backoff (3 attempts
total).

Explicitly does not retry:
- **500**: application-level bug — amplifying would mask, not help
- **Timeout**: separate concern, deferred

Expected effect: most 502/504-driven `BILLING_INIT Failed` events
self-recover within one request instead of requiring the user to retry.

## Test plan

- [x] 9 new/updated `bootstrap_user` unit tests (200 / 409 /
409-fallback / 502 retry / 504 retry / retry-exhaust / 500 no-retry /
json-parse-error fallback)
- [x] 2 updated `_do_billing_init` unit tests: verifies `get_credits` is
NOT called for new users, IS called for 409 recovery
- [x] `ruff check` + `ruff format` + `pyright` clean
- [x] `python-code-quality / file-length` check (file at exactly 500 /
500)
- [ ] Post-merge: monitor `[BILLING_CLIENT] HTTP 404` count over 48h;
expect drop from ~130/24h to <10/24h

## Notes

- RC-1 (cross-pod concurrent bootstrap creating duplicate teams) is
already mitigated by bg's distributed lock — no claw-interface change
needed.
- RC-3 (bg bootstrap returning 500 when LiteLLM upstream times out) is a
bg-side issue; 502/504 retry here handles the gateway-level variant of
the same root cause.
```

---

## [63bd907c](https://github.com/SerendipityOneInc/ecap-workspace/commit/63bd907c6ee471269dd551243ec787bd2febced9)

**Author:** peter-srp  
**Date:** 2026-04-20T06:35:41Z

**Message:**
```
Feature/fix ws status (#1085)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

---

## [ed3339ca](https://github.com/SerendipityOneInc/ecap-workspace/commit/ed3339cac1e71d3a29cf77790ee91b737896d023)

**Author:** bill-srp  
**Date:** 2026-04-20T06:35:00Z

**Message:**
```
ci(ios): Switch staging to TestFlight and add AppsFlyer config (#1084)

## Summary

Switch iOS staging distribution from Pgyer to TestFlight and configure
AppsFlyer keys for production builds.

### Changes
- **Fastlane staging lane**: Ad Hoc signing → App Store signing, Pgyer
upload → TestFlight upload
- **Bundle ID override**: staging builds use `one.srp.zooclaw-staging`
via `xcargs` (project default remains `one.srp.zooclaw`)
- **Build number**: extracted from tag sequence (`ios-v1.2.3-beta.7` →
build `7`), falls back to Xcode project value
- **Secrets.xcconfig**: production gets `APPSFLYER_DEV_KEY` +
`APPSFLYER_APP_ID`, staging gets empty file. Removed unused `SENTRY_DSN`
(hardcoded in app)
- **Cleanup**: removed `fastlane-plugin-pgyer` from Pluginfile, updated
PR comment and Feishu notification text

### Prerequisites (manual)
- [x] Register `one.srp.zooclaw-staging` in App Store Connect
- [x] App Store provisioning profile exists in Match repo
- [x] Firebase staging plist matches staging bundle ID
- [ ] Add `APPSFLYER_DEV_KEY` and `APPSFLYER_APP_ID` to GitHub Secrets
- [ ] Optionally remove `IOS_SENTRY_DSN` secret (no longer used)

## Test plan

- [ ] Trigger staging build via `gh workflow run "Deploy iOS" --ref
feat/ios-workflow -f environment=staging`
- [ ] Verify IPA is uploaded to TestFlight under the staging app
- [ ] Verify build number matches tag sequence
- [ ] Trigger production build and verify AppsFlyer keys are in the IPA

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## [9ac2bc28](https://github.com/SerendipityOneInc/ecap-workspace/commit/9ac2bc2810908d0cfb0f4ac3e1bdf1ecfbd5cf1c)

**Author:** peter-srp  
**Date:** 2026-04-20T06:26:35Z

**Message:**
```
chore(web): remove 29MB of unreferenced static assets (#1082)

Full-repo grep + manifest/CI/config scan confirmed zero references for
all deleted files:

- themes/panda-claw/w.gif (12.7MB) — w.webp is the version in use
- images/nano-banana-2-hero.png (6.1MB) — leftover from initial extract
- themes/panda-claw/logo-panda-claw-full.png (4.1MB) — unused since
theme refactor
- themes/panda-claw/loading.gif (2.9MB) — replaced, never cleaned up
- themes/panda-claw/panda-takeoff.gif (663KB) — unused onboarding
animation
- images/upgrade-mascot.png (647KB) — widget switched to CDN image
- images/assets-demo/ (1.75MB, 5 files) — demo placeholders never wired
up
- images/onboarding-panel.png (259KB) — superseded by redesign
- images/gradient_BG.png (88KB) — unused background

Also removes the now-stale w.gif example from docs/asset-size-guide.md.

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

---

## [3e22ace0](https://github.com/SerendipityOneInc/ecap-workspace/commit/3e22ace0049f5694f70e0183c241ed19961d1963)

**Author:** Nemo Feng  
**Date:** 2026-04-20T05:50:33Z

**Message:**
```
fix(agents-manager): force fresh agent list after hire/fire/update (#1044)

## Summary
- Hiring multiple specialists in quick succession (<3 s apart) and
clicking **Start Chat** on the latest success modal appeared to open the
*previous* agent's chat. Route was correct (`/chat?agent_id=<new>`), but
header/avatar/MM channel rendered the prior agent.
- Root cause: `refreshUserAgentsCache` has a 3 s read-throttle that
returned the pre-mutation `_lastResult` and skipped the
`ecap:agents:updated` dispatch. The chat page's identity lookup
(`userAgents.find(a => a.id === agentId)`) then fell through to the
previously-active agent until the next real fetch.
- Fix: add an opt-in `force` flag to `refreshUserAgentsCache` and pass
`force: true` from the mutation path in `useAgentActions.refreshAgents`.
Read-only callers (mount, tab visibility, WS events) still benefit from
the throttle.

## Trade-off
One extra `GET /agents` + catalog warm-up per hire/fire/update (~100–300
ms). Acceptable for correctness; the throttle was designed for burst
*reads*, not post-mutation refreshes.

## Test plan
- [ ] AI Specialists Hub → hire agent A → dismiss success modal → hire
agent B → click **Start Chat** on B's modal → chat opens with B's
avatar/name/MM channel (not A's).
- [ ] Repeat the above 3+ hires in a row; every "Start Chat" opens the
correct agent.
- [ ] Fire a hired agent → list updates immediately (no 3 s staleness).
- [ ] Update an agent with a new version → post-update refresh still
reflects the latest state.
- [ ] Normal mount/tab-switch flow: `userAgents` still debounces bursty
reads (no regression in request volume from passive callers).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Nemo Feng <nemofq@gmail.com>
Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>
```

---

## [bb75eb79](https://github.com/SerendipityOneInc/ecap-workspace/commit/bb75eb79c6911352735f25f1165c5895334e3a7d)

**Author:** sam-srp  
**Date:** 2026-04-20T05:21:04Z

**Message:**
```
fix(claw-interface): correct FastClaw cron.runs endpoint (#1083)

## Summary

- Reports from the schedule page threw a hard `404 Not Found` on every
call to `GET /cron/jobs/{job_id}/runs`, even on freshly created bots.
- Root cause: the client used a nested path
`/runtime/cron/jobs/{job_id}/runs` that **does not exist** on FastClaw.
Verified against `fastclaw/handler/api/v1/bot_cron.go:251` (`CronRuns`)
and the route registration at `fastclaw/cmd/server.go:191`, which
register a **flat** endpoint: `GET
/bots/:id/runtime/cron/runs?id={job_id}&limit={n}`.
- Fix: switch to the flat path with `id` as a query param. Drop
unsupported `offset` / `sortDir` from the outbound request (FastClaw
ignores them anyway); keep them on the Python signature so callers
(route layer, frontend) don't break.

## Test plan

- [x] `pytest tests/unit/test_openclaw_client.py::TestGetCronRuns` — 4/4
pass (2 new assertions: flat URL + `id` query, unsupported params
ignored)
- [x] `ruff check` / `ruff format --check` / `pyright` clean
- [x] `lint-imports` — 8/8 contracts kept
- [x] `deptry` — no dependency issues
- [ ] Manual: open `/schedule` on staging after deploy, verify cron run
history loads without 500 errors

## Notes

- `offset` / `sortDir` are kept on the Python signature only for
compatibility — FastClaw has no pagination/sorting on this endpoint yet.
Frontend's "load more" will return the same first-page until FastClaw
adds it upstream.
- Also already merged into `staging` (via a main-sync merge) and pushed,
so staging deploy picks this up without waiting for main.
```

---

## [46de46b1](https://github.com/SerendipityOneInc/ecap-workspace/commit/46de46b13d6bfc4cdc14d1c42d156a2a81c1447d)

**Author:** peter-srp  
**Date:** 2026-04-20T02:32:33Z

**Message:**
```
fix(web): resolve Sentry errors — JSON-LD, hydration, 401 noise (#1080)

## Summary

Fixes 3 categories of Sentry errors (4 issues total) identified from the
24h health overview:

- **JSON-LD `@context` TypeError** (Sentry
[#7347020751](https://serendipity-one-inc.sentry.io/issues/7347020751/)
/
[#7344333754](https://serendipity-one-inc.sentry.io/issues/7344333754/)):
`getStructuredDataSchemas()` returned a bare JSON array, causing Safari
parsers to access `@context` on the array root (undefined). Now uses the
standard `{ @context, @graph: [...] }` wrapper.

- **Hydration mismatch** (Sentry
[#7238337700](https://serendipity-one-inc.sentry.io/issues/7238337700/)):
`GenClawClient` and `SideNav` read `sessionStorage`/`localStorage` in
`useState` initializers — server rendered with `{}` while client
hydrated with cached data. Moved browser storage reads to `useEffect` so
initial render is identical on both sides.

- **HTTP 401 noise** (Sentry
[#7416524759](https://serendipity-one-inc.sentry.io/issues/7416524759/)):
`httpClientIntegration` captured all 400-599 status codes including 401,
which is expected when tokens expire. Excluded 401 from capture range
(`[400, [402, 599]]`).

## Changes

| File | Change |
|------|--------|
| `web/src/lib/seo.ts` | `@graph` wrapper for JSON-LD structured data |
| `web/src/app/[locale]/chat/GenClawClient.tsx` | `useState` →
`useEffect` for sessionStorage/localStorage |
| `web/src/components/SideNav.tsx` | Same hydration fix for identity
cache + hire CTA state |
| `web/sentry.client.config.ts` | Exclude 401 from
`httpClientIntegration` |

## Test plan

- [ ] Visit homepage (`/en`, `/zh`) in Safari — no console errors,
JSON-LD validates in [Schema.org
validator](https://validator.schema.org/)
- [ ] Visit `/chat` page — no hydration warnings in console;
identity/settings load correctly after mount
- [ ] Trigger a 401 (expired token) — verify it does NOT appear in
Sentry
- [ ] Trigger a 403/500 — verify it DOES appear in Sentry
- [ ] `tsc --noEmit` passes (verified locally)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

---

## [6d98c1c3](https://github.com/SerendipityOneInc/ecap-workspace/commit/6d98c1c360e0a658b5b48d689354ad35e272a1dd)

**Author:** peter-srp  
**Date:** 2026-04-20T01:50:26Z

**Message:**
```
fix(web): resolve hydration mismatch from browser storage reads in us… (#1078)

…eState initializers

SideNav and GenClawClient read localStorage/sessionStorage in useState
initializers, producing different values on server ({}) vs client
(cached data). Move storage reads to useEffect so first render matches
SSR output.

Fixes Sentry ECAP-WEBSITE-2 (Hydration Error — 2,876 events / 114
users).

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

---

## [35ebc0da](https://github.com/SerendipityOneInc/ecap-workspace/commit/35ebc0dafc695924ecd0c00ccb04b8b36779cf35)

**Author:** peter-srp  
**Date:** 2026-04-20T01:50:15Z

**Message:**
```
fix(web): use theme-aware text color on CompensationPopup button (#1079)

Replace hardcoded `text-white` with `text-ecap-primary-text` so the "Got
it" button has correct contrast in panda-claw dark mode where the
primary color inverts to a light shade (#e8e8e4).

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```
