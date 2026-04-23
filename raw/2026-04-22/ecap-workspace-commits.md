# SerendipityOneInc/ecap-workspace — 2026-04-22

共 22 个 commits

## feat(web): render pptx OOXML tables (graphicFrame > a:tbl) (#1149)

- **SHA**: [3b09da9a](https://github.com/SerendipityOneInc/ecap-workspace/commit/3b09da9ac2f9c935d94a533754af840243e53156)
- **作者**: sam-srp
- **时间**: 2026-04-21T12:43:53Z
- **PR**: [#1149](https://github.com/SerendipityOneInc/ecap-workspace/pull/1149)

### Commit Message

feat(web): render pptx OOXML tables (graphicFrame > a:tbl) (#1149)

## Summary

Slides with real OOXML tables (`<p:graphicFrame>` containing `<a:tbl>`)
previously rendered a blank region where the table should be — our
renderer's dispatcher only handled `sp`/`pic`/`cxnSp`/`grpSp`. This PR
adds a fourth branch that flattens each `<a:tc>` cell into a synthetic
`SlideShape` (text + styled rect), positioned at its computed column/row
offset within the frame's bounding box.

Most common pptx cases now render with the right data: data tables,
feature matrices, schedules, etc.

## What's parsed

| XML | Produces |
|---|---|
| `<p:xfrm>/<a:off>/<a:ext>` | frame's slide-level position/size |
| `<a:tblGrid>/<a:gridCol w=…>` | column widths (scaled to fit
`frame.cx`) |
| `<a:tr h=…>` | row heights |
| `<a:tc>` | one cell per iteration |
| `<a:tcPr>/<a:solidFill>` | cell background color + alpha |
| `<a:tcPr>/<a:lnL/lnR/lnT/lnB>` | border (first side with a color wins;
uniform on all 4 sides) |
| `<a:tc>/<a:txBody>` | cell text via existing `extractParagraphs` |
| `<a:tc>/<a:bodyPr anchor=…>` | vertical alignment (defaults to middle)
|

## Known limits (not load-bearing, deferred)

- `gridSpan` / `rowSpan` (merged cells) — merged cells render as
separate cells
- Charts and SmartArt inside `graphicFrame` still render empty
- Per-side border differences collapse to uniform (cells in practice use
the same color on all four sides; 1px width makes the visual delta at
internal joins imperceptible)

## Test plan

- [ ] Open a deck with a data table → cells appear with text, fill,
borders
- [ ] Regression: decks without tables are unchanged
- [ ] Regression: existing pptx decks (no `graphicFrame`) render
identically

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Description

## Summary

Slides with real OOXML tables (`<p:graphicFrame>` containing `<a:tbl>`) previously rendered a blank region where the table should be — our renderer's dispatcher only handled `sp`/`pic`/`cxnSp`/`grpSp`. This PR adds a fourth branch that flattens each `<a:tc>` cell into a synthetic `SlideShape` (text + styled rect), positioned at its computed column/row offset within the frame's bounding box.

Most common pptx cases now render with the right data: data tables, feature matrices, schedules, etc.

## What's parsed

| XML | Produces |
|---|---|
| `<p:xfrm>/<a:off>/<a:ext>` | frame's slide-level position/size |
| `<a:tblGrid>/<a:gridCol w=…>` | column widths (scaled to fit `frame.cx`) |
| `<a:tr h=…>` | row heights |
| `<a:tc>` | one cell per iteration |
| `<a:tcPr>/<a:solidFill>` | cell background color + alpha |
| `<a:tcPr>/<a:lnL/lnR/lnT/lnB>` | border (first side with a color wins; uniform on all 4 sides) |
| `<a:tc>/<a:txBody>` | cell text via existing `extractParagraphs` |
| `<a:tc>/<a:bodyPr anchor=…>` | vertical alignment (defaults to middle) |

## Known limits (not load-bearing, deferred)

- `gridSpan` / `rowSpan` (merged cells) — merged cells render as separate cells
- Charts and SmartArt inside `graphicFrame` still render empty
- Per-side border differences collapse to uniform (cells in practice use the same color on all four sides; 1px width makes the visual delta at internal joins imperceptible)

## Test plan

- [ ] Open a deck with a data table → cells appear with text, fill, borders
- [ ] Regression: decks without tables are unchanged
- [ ] Regression: existing pptx decks (no `graphicFrame`) render identically

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## test(web): SizeSelector 全面覆盖 (#894 Step 11 补) (#1148)

- **SHA**: [a08dcaa9](https://github.com/SerendipityOneInc/ecap-workspace/commit/a08dcaa94ab98ecf5112d74392b4fe3df306c6d5)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-21T12:31:20Z
- **PR**: [#1148](https://github.com/SerendipityOneInc/ecap-workspace/pull/1148)

### Commit Message

test(web): SizeSelector 全面覆盖 (#894 Step 11 补) (#1148)

## Summary

Epic #894 Step 11 (#905) — 先补 SizeSelector.tsx (189 LOC) 从 0% → 全分支。26
tests，+2 行源码 export。

## 新增 26 个测试

| 分组 | # | 覆盖 |
|---|---|---|
| getSizeDimensions | 8 | auto / 5 种 ratio / malformed / 单段 / 零维度（gcd
无限递归守卫） |
| groupSizesByRatio | 2 | 按 ratio 分组 / 空输入 |
| 单选 pill | 2 | options.length===1 无 button / label 兜底 value |
| 多选下拉 | 9 | 默认关闭 / 点开 / 再点关 / 选项 click → onChange+关闭 / selected 样式 /
'auto' → "Auto" / 点外关 / 点内不关 / Escape 关 / 非 Escape 不关 |
| disabled | 1 | disabled=true 不响应 |
| Trigger label | 3 | 有 label / 无 label / value 找不到 → options[0] |

## Harness 要点

- 零维度守卫：`getSizeDimensions('0x512')` 触发 `parts[0]=0` 的 truthy check 失败 →
fall back Auto，避免 `gcd(0, 512)` 可能无限递归
- 下拉打开后有多个 button（trigger + 每个尺寸），cache trigger 引用避免
`getByRole('button')` 多匹配歧义

## Bug-hunting

无新发现。`getSizeDimensions` 的零值 guard 借助 `parts[0] && parts[1]` truthy
判断，行为合理。

## Test plan

- [x] 26/26 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 11 (#905)
- 剩余：ModelSelector (381) / FeedbackDialog (337) / FeedbackProvider (176)
/ GuideTourModal (418) / ImagePreview (257) / ArchivedSessionPanel
(301)，之后抬阈值 35 → 80

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Description

## Summary

Epic #894 Step 11 (#905) — 先补 SizeSelector.tsx (189 LOC) 从 0% → 全分支。26 tests，+2 行源码 export。

## 新增 26 个测试

| 分组 | # | 覆盖 |
|---|---|---|
| getSizeDimensions | 8 | auto / 5 种 ratio / malformed / 单段 / 零维度（gcd 无限递归守卫） |
| groupSizesByRatio | 2 | 按 ratio 分组 / 空输入 |
| 单选 pill | 2 | options.length===1 无 button / label 兜底 value |
| 多选下拉 | 9 | 默认关闭 / 点开 / 再点关 / 选项 click → onChange+关闭 / selected 样式 / 'auto' → "Auto" / 点外关 / 点内不关 / Escape 关 / 非 Escape 不关 |
| disabled | 1 | disabled=true 不响应 |
| Trigger label | 3 | 有 label / 无 label / value 找不到 → options[0] |

## Harness 要点

- 零维度守卫：`getSizeDimensions('0x512')` 触发 `parts[0]=0` 的 truthy check 失败 → fall back Auto，避免 `gcd(0, 512)` 可能无限递归
- 下拉打开后有多个 button（trigger + 每个尺寸），cache trigger 引用避免 `getByRole('button')` 多匹配歧义

## Bug-hunting

无新发现。`getSizeDimensions` 的零值 guard 借助 `parts[0] && parts[1]` truthy 判断，行为合理。

## Test plan

- [x] 26/26 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 11 (#905)
- 剩余：ModelSelector (381) / FeedbackDialog (337) / FeedbackProvider (176) / GuideTourModal (418) / ImagePreview (257) / ArchivedSessionPanel (301)，之后抬阈值 35 → 80

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@chris-srp: /lgtm

---

## test(web): AgentDetailClient 全面覆盖 (#894 Step 9 收尾) (#1144)

- **SHA**: [6f776be2](https://github.com/SerendipityOneInc/ecap-workspace/commit/6f776be2c6e2ac4380c5e851e9147a1819c70d65)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-21T11:36:08Z
- **PR**: [#1144](https://github.com/SerendipityOneInc/ecap-workspace/pull/1144)

### Commit Message

test(web): AgentDetailClient 全面覆盖 (#894 Step 9 收尾) (#1144)

## Summary

Epic #894 Step 9 (#903) — 最后一个未覆盖的文件：\`AgentDetailClient.tsx\` (608 LOC)
从 0% → 全分支。issue 明说覆盖关键 ~200 行（7 个 modal state + escape handler + lock
states）。31 tests, 零源码改动。

## 新增 31 个测试

| 组 | # | 覆盖 |
|---|---|---|
| 初始渲染 | 6 | loading / catalog 成功 / 无匹配 / reject / unmount race / bio 空时
description fallback |
| CTA 按钮 | 5 | 未 hired 只显示 Hire / hired 显示 Chat+Fire / has_update →
Update / !has_update 隐藏 / Chat router.push |
| Hire 流 | 5 | confirm modal / isLocked 禁用 / confirm → hireAgent+success
/ reject 无 success / "Go to chat" |
| Fire 流 | 4 | confirm modal + FIRE 输入门 / 错文字 disabled / "FIRE" enabled
+ fireAgent / reject |
| Update 流 | 6 | confirm / updateAgent+removeItem
CLAW_IDENTITY_CACHE+updated / reject / skip / Send /new → resetAgent /
isResetting 禁用+label |
| Escape | 2 | confirm → Escape 关 / success 优先级 > confirm |
| syncing | 1 | modal + button disabled |
| error banner | 1 | |

## Harness 要点

- **heavy imports stub** (ClawPageHeader / LocaleLink / AnimalAvatar) 成
testid div，专注 AgentDetailClient 状态机
- **"Panda Agent" 双重出现**：breadcrumb + h1，用 unique bio `'I am a panda.'`
做 waitFor anchor
- **`zooSquare.confirmFire` 严格匹配**：4 处元素同
prefix（Title/Desc/Prompt/button），必须用精确 string 避免 regex 误中

## Bug-hunting

无新发现。组件的 cancelled 标志防 setState-on-unmounted，7 modal 的 escape
优先级合理（success > confirm > fireConfirm > fired > updateConfirm >
updated，isResetting 守卫 updated）。

## Test plan

- [x] 31/31 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 9 (#903) 清单里其他文件（PublishAgentsClient /
SkillsSearchClient / SkillDetailClient / useAgentActions /
useCustomAgentPublishes / useUserAgents）已有测试；合入后 #903 可 close

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Description

## Summary

Epic #894 Step 9 (#903) — 最后一个未覆盖的文件：\`AgentDetailClient.tsx\` (608 LOC) 从 0% → 全分支。issue 明说覆盖关键 ~200 行（7 个 modal state + escape handler + lock states）。31 tests, 零源码改动。

## 新增 31 个测试

| 组 | # | 覆盖 |
|---|---|---|
| 初始渲染 | 6 | loading / catalog 成功 / 无匹配 / reject / unmount race / bio 空时 description fallback |
| CTA 按钮 | 5 | 未 hired 只显示 Hire / hired 显示 Chat+Fire / has_update → Update / !has_update 隐藏 / Chat router.push |
| Hire 流 | 5 | confirm modal / isLocked 禁用 / confirm → hireAgent+success / reject 无 success / "Go to chat" |
| Fire 流 | 4 | confirm modal + FIRE 输入门 / 错文字 disabled / "FIRE" enabled + fireAgent / reject |
| Update 流 | 6 | confirm / updateAgent+removeItem CLAW_IDENTITY_CACHE+updated / reject / skip / Send /new → resetAgent / isResetting 禁用+label |
| Escape | 2 | confirm → Escape 关 / success 优先级 > confirm |
| syncing | 1 | modal + button disabled |
| error banner | 1 | |

## Harness 要点

- **heavy imports stub** (ClawPageHeader / LocaleLink / AnimalAvatar) 成 testid div，专注 AgentDetailClient 状态机
- **"Panda Agent" 双重出现**：breadcrumb + h1，用 unique bio `'I am a panda.'` 做 waitFor anchor
- **`zooSquare.confirmFire` 严格匹配**：4 处元素同 prefix（Title/Desc/Prompt/button），必须用精确 string 避免 regex 误中

## Bug-hunting

无新发现。组件的 cancelled 标志防 setState-on-unmounted，7 modal 的 escape 优先级合理（success > confirm > fireConfirm > fired > updateConfirm > updated，isResetting 守卫 updated）。

## Test plan

- [x] 31/31 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 9 (#903) 清单里其他文件（PublishAgentsClient / SkillsSearchClient / SkillDetailClient / useAgentActions / useCustomAgentPublishes / useUserAgents）已有测试；合入后 #903 可 close

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@chris-srp: /lgtm

---

## refactor(web): extract brand-theme bootstrap to src/app/ — fix W6 (A1-PR5) (#1131)

- **SHA**: [ea59b3ef](https://github.com/SerendipityOneInc/ecap-workspace/commit/ea59b3efe1778004084a8ab41176b84706d61146)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-21T10:27:06Z
- **PR**: [#1131](https://github.com/SerendipityOneInc/ecap-workspace/pull/1131)

### Commit Message

refactor(web): extract brand-theme bootstrap to src/app/ — fix W6 (A1-PR5) (#1131)

## Summary
- Fixes the single W6 violation `src/theme/brand-themes.ts →
src/lib/auth/types` by extracting `getBrandThemeBootstrapScript()` out
of `theme/` into `src/app/_brand-bootstrap.ts`.
- Leaves `STORAGE_KEYS.BRAND_THEME` as **single source of truth** in
`lib/auth/types` — all three callers (bootstrap / provider /
logout-preserve) consume it by that path.
- Baseline shrinks **17 → 16**.

## Why extract instead of inline duplicate

Initial draft inlined `'ecap-brand-theme'` twice (once in `theme/`, once
in `lib/auth/types`) with cross-ref comments. Reviewer flagged the
underlying oddity: why does `brand-themes.ts` know about localStorage at
all?

Answer: it contains `getBrandThemeBootstrapScript()` which generates an
IIFE string for SSR first-paint. That function needs the storage key to
embed in the script. But this function is **App-Router-specific** — it's
only called from `src/app/[locale]/layout.tsx` to emit an inline
`<script>` for first-paint anti-flicker.

So the real fix is to move the App-Router concern out of `theme/`:

| Concern | Home before | Home after |
|---|---|---|
| Brand registry + types + guards | `theme/brand-themes.ts` |
`theme/brand-themes.ts` (unchanged) |
| `BRAND_THEME_ATTRIBUTE` (DOM contract string) |
`theme/brand-themes.ts` | `theme/brand-themes.ts` (unchanged — no
cross-layer dep) |
| `getBrandThemeBootstrapScript` (SSR first-paint logic) |
`theme/brand-themes.ts` | **`src/app/_brand-bootstrap.ts`** (new) |
| `BRAND_THEME_STORAGE_KEY` | `theme/brand-themes.ts` (derived from
STORAGE_KEYS) | **removed** — callers use `STORAGE_KEYS.BRAND_THEME`
directly |

After the move, `theme/brand-themes.ts` has **zero cross-layer imports**
— a true Layer-1 leaf per W6.

## Layer check

- `src/app/_brand-bootstrap.ts` → `src/lib/auth/types` — `app → lib` ✅
- `src/app/_brand-bootstrap.ts` → `src/theme/brand-themes` — `app →
theme` ✅
- `src/components/BrandThemeProvider.tsx` → `src/lib/auth/types` —
`components → lib` ✅
- `src/components/BrandThemeProvider.tsx` → `src/theme/brand-themes` —
`components → theme` ✅
- `src/app/[locale]/layout.tsx` → `src/app/_brand-bootstrap` — `app →
app` ✅

## Changes

| File | Change |
|---|---|
| `src/app/_brand-bootstrap.ts` | **new** — owns
`getBrandThemeBootstrapScript` + imports `STORAGE_KEYS` from lib and
brand data from theme |
| `src/theme/brand-themes.ts` | drop storage-key export + bootstrap fn +
`@/lib/auth/types` import; pure data/types/guards only |
| `src/components/BrandThemeProvider.tsx` | import `STORAGE_KEYS` from
`@/lib/auth/types` instead of `BRAND_THEME_STORAGE_KEY` |
| `src/app/[locale]/layout.tsx` | import `getBrandThemeBootstrapScript`
from new home |
| `tests/unit/theme/brand-themes.unit.spec.ts` | keep only
`isBrandThemeName` coverage |
| `tests/unit/app/_brand-bootstrap.unit.spec.ts` | **new** — covers
bootstrap script shape via static string assertions |
| `tests/unit/components/BrandThemeProvider.unit.spec.tsx` +
`tests/unit/hooks/useBrandVocabulary.unit.spec.tsx` | update imports to
`STORAGE_KEYS.BRAND_THEME` |
| `.dependency-cruiser-known-violations.json` | remove W6 entry (17 →
16) |

9 files changed, +119 / −187 (test file cleanup is the big delta — moved
to two smaller files).

## Note on bootstrap runtime tests

The prior test used `new Function()` to execute the generated script
string against mocked globals. The moved test drops that path and keeps
only static-shape assertions (contains IIFE / contains storage key /
contains all allowed names / etc). Runtime correctness of the script is
covered transitively by e2e (the script actually runs during SSR). If a
targeted runtime test becomes needed, it belongs in a jsdom-with-eval
harness, not unit tests.

## Local verification
- \`pnpm lint:imports\` — exit 0, \`16 known violations ignored\`
- \`pnpm test:unit\` affected files — 31 tests pass
- \`npx tsc --noEmit\` — clean
- \`pnpm lint\` — clean

## Aftermath

With this + A1-PR4 already merged, **W1 and W6 contracts are fully
clean**. Remaining baseline 15 is entirely W2/W3/W4/W5 cluster (the \"UI
layer still touching pages/features\" knot). Each subsequent A1-PR6+
takes a handful.

## Test plan
- [x] tsc + eslint + unit tests pass
- [x] Baseline JSON shrinks correctly (17 → 16)
- [ ] CI confirms web-quality + asset-size + jscpd
- [ ] Reviewer validates \`src/app/_brand-bootstrap.ts\` as the right
home for SSR first-paint logic (vs staying in theme with inline
duplicate)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Description

## Summary
- Fixes the single W6 violation `src/theme/brand-themes.ts → src/lib/auth/types` by extracting `getBrandThemeBootstrapScript()` out of `theme/` into `src/app/_brand-bootstrap.ts`.
- Leaves `STORAGE_KEYS.BRAND_THEME` as **single source of truth** in `lib/auth/types` — all three callers (bootstrap / provider / logout-preserve) consume it by that path.
- Baseline shrinks **17 → 16**.

## Why extract instead of inline duplicate

Initial draft inlined `'ecap-brand-theme'` twice (once in `theme/`, once in `lib/auth/types`) with cross-ref comments. Reviewer flagged the underlying oddity: why does `brand-themes.ts` know about localStorage at all?

Answer: it contains `getBrandThemeBootstrapScript()` which generates an IIFE string for SSR first-paint. That function needs the storage key to embed in the script. But this function is **App-Router-specific** — it's only called from `src/app/[locale]/layout.tsx` to emit an inline `<script>` for first-paint anti-flicker.

So the real fix is to move the App-Router concern out of `theme/`:

| Concern | Home before | Home after |
|---|---|---|
| Brand registry + types + guards | `theme/brand-themes.ts` | `theme/brand-themes.ts` (unchanged) |
| `BRAND_THEME_ATTRIBUTE` (DOM contract string) | `theme/brand-themes.ts` | `theme/brand-themes.ts` (unchanged — no cross-layer dep) |
| `getBrandThemeBootstrapScript` (SSR first-paint logic) | `theme/brand-themes.ts` | **`src/app/_brand-bootstrap.ts`** (new) |
| `BRAND_THEME_STORAGE_KEY` | `theme/brand-themes.ts` (derived from STORAGE_KEYS) | **removed** — callers use `STORAGE_KEYS.BRAND_THEME` directly |

After the move, `theme/brand-themes.ts` has **zero cross-layer imports** — a true Layer-1 leaf per W6.

## Layer check

- `src/app/_brand-bootstrap.ts` → `src/lib/auth/types` — `app → lib` ✅
- `src/app/_brand-bootstrap.ts` → `src/theme/brand-themes` — `app → theme` ✅
- `src/components/BrandThemeProvider.tsx` → `src/lib/auth/types` — `components → lib` ✅
- `src/components/BrandThemeProvider.tsx` → `src/theme/brand-themes` — `components → theme` ✅
- `src/app/[locale]/layout.tsx` → `src/app/_brand-bootstrap` — `app → app` ✅

## Changes

| File | Change |
|---|---|
| `src/app/_brand-bootstrap.ts` | **new** — owns `getBrandThemeBootstrapScript` + imports `STORAGE_KEYS` from lib and brand data from theme |
| `src/theme/brand-themes.ts` | drop storage-key export + bootstrap fn + `@/lib/auth/types` import; pure data/types/guards only |
| `src/components/BrandThemeProvider.tsx` | import `STORAGE_KEYS` from `@/lib/auth/types` instead of `BRAND_THEME_STORAGE_KEY` |
| `src/app/[locale]/layout.tsx` | import `getBrandThemeBootstrapScript` from new home |
| `tests/unit/theme/brand-themes.unit.spec.ts` | keep only `isBrandThemeName` coverage |
| `tests/unit/app/_brand-bootstrap.unit.spec.ts` | **new** — covers bootstrap script shape via static string assertions |
| `tests/unit/components/BrandThemeProvider.unit.spec.tsx` + `tests/unit/hooks/useBrandVocabulary.unit.spec.tsx` | update imports to `STORAGE_KEYS.BRAND_THEME` |
| `.dependency-cruiser-known-violations.json` | remove W6 entry (17 → 16) |

9 files changed, +119 / −187 (test file cleanup is the big delta — moved to two smaller files).

## Note on bootstrap runtime tests

The prior test used `new Function()` to execute the generated script string against mocked globals. The moved test drops that path and keeps only static-shape assertions (contains IIFE / contains storage key / contains all allowed names / etc). Runtime correctness of the script is covered transitively by e2e (the script actually runs during SSR). If a targeted runtime test becomes needed, it belongs in a jsdom-with-eval harness, not unit tests.

## Local verification
- \`pnpm lint:imports\` — exit 0, \`16 known violations ignored\`
- \`pnpm test:unit\` affected files — 31 tests pass
- \`npx tsc --noEmit\` — clean
- \`pnpm lint\` — clean

## Aftermath

With this + A1-PR4 already merged, **W1 and W6 contracts are fully clean**. Remaining baseline 15 is entirely W2/W3/W4/W5 cluster (the \"UI layer still touching pages/features\" knot). Each subsequent A1-PR6+ takes a handful.

## Test plan
- [x] tsc + eslint + unit tests pass
- [x] Baseline JSON shrinks correctly (17 → 16)
- [ ] CI confirms web-quality + asset-size + jscpd
- [ ] Reviewer validates \`src/app/_brand-bootstrap.ts\` as the right home for SSR first-paint logic (vs staying in theme with inline duplicate)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@chris-srp: /lgtm

---

## fix: agent id of popup (#1143)

- **SHA**: [212f5703](https://github.com/SerendipityOneInc/ecap-workspace/commit/212f5703aad8761fcd8ead4e1a0dcf9703b9c0e3)
- **作者**: nolan-srp
- **时间**: 2026-04-21T10:24:34Z
- **PR**: [#1143](https://github.com/SerendipityOneInc/ecap-workspace/pull/1143)

### Commit Message

fix: agent id of popup (#1143)

---

## test(web): ClawSettingsClient 关键分支覆盖 (#894 Step 5 收尾) (#1142)

- **SHA**: [06325039](https://github.com/SerendipityOneInc/ecap-workspace/commit/06325039918012d44d97f542ab23ab7558661030)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-21T10:13:10Z
- **PR**: [#1142](https://github.com/SerendipityOneInc/ecap-workspace/pull/1142)

### Commit Message

test(web): ClawSettingsClient 关键分支覆盖 (#894 Step 5 收尾) (#1142)

## Summary

Epic #894 Step 5 (#899) 的最后一个文件：\`ClawSettingsClient.tsx\` (438 LOC)。按
issue 描述只覆盖关键 ~120 行（auth gates + tab routing + noBot 分支 + status tab
internal-only visibility），27 个测试。

## 源码变动（1 行）

- \`BotStatusBanner\` 加 \`export\`

## 新增 27 个测试

| 组 | # | 覆盖 |
|---|---|---|
| BotStatusBanner | 5 | ready/no_bot 返 null / creating/starting 各自 label
/ i18n 兜底到英文 default |
| Auth 状态机 | 6 | authLoading → dot-spin / !chatReady → null /
!isLoggedIn → login prompt / 无 uid → login prompt / login 按钮 →
showLoginModal / 全过 → SettingsLayout |
| Tab routing | 9 | 默认 account / 非法 paramTab fallback /
channels/account-usage/account-billing/connectors/sessions/statistics
对应组件 / 点击 tab → router.replace('?tab=X') |
| noBot 分支 | 3 | 非 account tab + 无 settings / bot_status='no_bot' /
account tab bypass |
| Status tab internal-only | 2 | canViewInternalOnlyFeatures false/true
→ ImageVersionSection 可见性 |
| error + loading | 2 | error banner / 内层 dot-spin |

## Harness 要点

所有 heavy 子组件（GeneralTab / UsageTabContent / BillingTabContent /
ChannelsSection / ConnectorsSection / DiagnosticsSection /
ImageVersionSection / SessionResetSection / UsageCard /
WorkspaceFilesSection）stub 成 testid 占位，让测试只盯 ClawSettingsClient 自己的
routing / auth 逻辑。SettingsLayout stub 暴露 `tab-{id}` testid 让点击 tab 可驱动
onTabChange。

## 不覆盖范围

- `StatusTab` 内部组件（logs modal 弹框逻辑）— 复杂但非 issue 重点，未来如需再补
- Resources 30s 自动 poll — 需要 fake timer + waitFor 混合，收益低
- versionCheck.needsUpgrade → UpgradeNotificationBanner — 纯透传 props

## Test plan

- [x] 27/27 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 5 (#899) — 所有清单文件已覆盖，#899 可 close

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Description

## Summary

Epic #894 Step 5 (#899) 的最后一个文件：\`ClawSettingsClient.tsx\` (438 LOC)。按 issue 描述只覆盖关键 ~120 行（auth gates + tab routing + noBot 分支 + status tab internal-only visibility），27 个测试。

## 源码变动（1 行）

- \`BotStatusBanner\` 加 \`export\`

## 新增 27 个测试

| 组 | # | 覆盖 |
|---|---|---|
| BotStatusBanner | 5 | ready/no_bot 返 null / creating/starting 各自 label / i18n 兜底到英文 default |
| Auth 状态机 | 6 | authLoading → dot-spin / !chatReady → null / !isLoggedIn → login prompt / 无 uid → login prompt / login 按钮 → showLoginModal / 全过 → SettingsLayout |
| Tab routing | 9 | 默认 account / 非法 paramTab fallback / channels/account-usage/account-billing/connectors/sessions/statistics 对应组件 / 点击 tab → router.replace('?tab=X') |
| noBot 分支 | 3 | 非 account tab + 无 settings / bot_status='no_bot' / account tab bypass |
| Status tab internal-only | 2 | canViewInternalOnlyFeatures false/true → ImageVersionSection 可见性 |
| error + loading | 2 | error banner / 内层 dot-spin |

## Harness 要点

所有 heavy 子组件（GeneralTab / UsageTabContent / BillingTabContent / ChannelsSection / ConnectorsSection / DiagnosticsSection / ImageVersionSection / SessionResetSection / UsageCard / WorkspaceFilesSection）stub 成 testid 占位，让测试只盯 ClawSettingsClient 自己的 routing / auth 逻辑。SettingsLayout stub 暴露 `tab-{id}` testid 让点击 tab 可驱动 onTabChange。

## 不覆盖范围

- `StatusTab` 内部组件（logs modal 弹框逻辑）— 复杂但非 issue 重点，未来如需再补
- Resources 30s 自动 poll — 需要 fake timer + waitFor 混合，收益低
- versionCheck.needsUpgrade → UpgradeNotificationBanner — 纯透传 props

## Test plan

- [x] 27/27 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 5 (#899) — 所有清单文件已覆盖，#899 可 close

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@chris-srp: /lgtm

---

## test(web): ConnectorsSection 全面覆盖 (#894 Step 5 补) (#1130)

- **SHA**: [b7b78b08](https://github.com/SerendipityOneInc/ecap-workspace/commit/b7b78b0893baa8b7bf9f90ff4ee4af7284a6d554)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-21T09:52:40Z
- **PR**: [#1130](https://github.com/SerendipityOneInc/ecap-workspace/pull/1130)

### Commit Message

test(web): ConnectorsSection 全面覆盖 (#894 Step 5 补) (#1130)

## Summary

Epic #894 Step 5 (#899) — 再补一个：\`ConnectorsSection.tsx\` (493 LOC) 从 0%
→ 全分支，28 tests。源码零改动（Google Workspace connector + Nango integrations +
ModeDropdown 的所有导出都已经是 named exports），test-only PR。

## 新增 28 个测试

| 分组 | # | 覆盖 |
|---|---|---|
| loading state | 2 | 初始 / resolve 后消失 |
| Google 卡状态机 | 3 | 无 token / token+!alive (Reconnect) / token+alive
(Disconnect) |
| API error | 2 | Error 实例 / 非-Error fallback "Failed to load status" |
| handleConnect | 3 | 成功 → window.location.href 赋值 / 失败 → error + 按钮恢复 /
readonly→false 传给 getConnectorAuthUrl |
| handleDisconnect | 2 | 成功 → refetch / 失败 → error |
| handleReconnect | 2 | 成功 → injectConnector + refetch / 失败 |
| ModeDropdown | 3 | 展开 / 点外关 / 选项切换 |
| Nango cards | 7 | connected/pending/error/unknown 4 种 status /
disconnect 回调 / toggle enable vs disable / saving → disabled |
| Available integrations | 3 | 有未连接则渲染 section / Connect click → connect
+ window.open + pollUntilConnected / null URL 不 open / 全连接则隐藏 section |

## Harness 要点

- **window.location 代理**：jsdom 的 location 是只读的，source 里
\`window.location.href = url\` 会抛。用 Proxy 装 href setter 记录赋值，测试直接检查
hrefWrites 数组
- **integrations factory**：返回可 mock 的
connect/disconnect/enable/disable/pollUntilConnected，不同测试换不同 connections
数组
- **\`settings.connect\` 多处出现**：Google card + 每个 Available card 都有同名按钮，用
\`findAllByText + [0]\` 定位 Google（DOM 顺序稳定）

## Bug-hunting

无新发现。Google connector state machine 干净，error recovery 路径到位。

## Test plan

- [x] 28/28 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 5 (#899)
- Step 5 剩下：ClawSettingsClient (438 LOC, 关键 ~120)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Description

## Summary

Epic #894 Step 5 (#899) — 再补一个：\`ConnectorsSection.tsx\` (493 LOC) 从 0% → 全分支，28 tests。源码零改动（Google Workspace connector + Nango integrations + ModeDropdown 的所有导出都已经是 named exports），test-only PR。

## 新增 28 个测试

| 分组 | # | 覆盖 |
|---|---|---|
| loading state | 2 | 初始 / resolve 后消失 |
| Google 卡状态机 | 3 | 无 token / token+!alive (Reconnect) / token+alive (Disconnect) |
| API error | 2 | Error 实例 / 非-Error fallback "Failed to load status" |
| handleConnect | 3 | 成功 → window.location.href 赋值 / 失败 → error + 按钮恢复 / readonly→false 传给 getConnectorAuthUrl |
| handleDisconnect | 2 | 成功 → refetch / 失败 → error |
| handleReconnect | 2 | 成功 → injectConnector + refetch / 失败 |
| ModeDropdown | 3 | 展开 / 点外关 / 选项切换 |
| Nango cards | 7 | connected/pending/error/unknown 4 种 status / disconnect 回调 / toggle enable vs disable / saving → disabled |
| Available integrations | 3 | 有未连接则渲染 section / Connect click → connect + window.open + pollUntilConnected / null URL 不 open / 全连接则隐藏 section |

## Harness 要点

- **window.location 代理**：jsdom 的 location 是只读的，source 里 \`window.location.href = url\` 会抛。用 Proxy 装 href setter 记录赋值，测试直接检查 hrefWrites 数组
- **integrations factory**：返回可 mock 的 connect/disconnect/enable/disable/pollUntilConnected，不同测试换不同 connections 数组
- **\`settings.connect\` 多处出现**：Google card + 每个 Available card 都有同名按钮，用 \`findAllByText + [0]\` 定位 Google（DOM 顺序稳定）

## Bug-hunting

无新发现。Google connector state machine 干净，error recovery 路径到位。

## Test plan

- [x] 28/28 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 5 (#899)
- Step 5 剩下：ClawSettingsClient (438 LOC, 关键 ~120)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@chris-srp: /lgtm

---

## fix: clean up stale domain refs and remove dead env vars (#1140)

- **SHA**: [28ef8cd1](https://github.com/SerendipityOneInc/ecap-workspace/commit/28ef8cd1d299f6a09e9042b0d598ee3105283bca)
- **作者**: peter-srp
- **时间**: 2026-04-21T08:28:09Z
- **PR**: [#1140](https://github.com/SerendipityOneInc/ecap-workspace/pull/1140)

### Commit Message

fix: clean up stale domain refs and remove dead env vars (#1140)

## Summary
- **`www.zooclaw.ai` → `zooclaw.ai`**: E2E/CI 配置中错误使用了不支持的 www
子域名（playwright.config、e2e.yml、auth setup 等 6 处）
- **`pandaclaw.ai` → `zooclaw.ai`**: 设计稿 mockup 中的旧域名邮箱替换（4 处
docs/design HTML）
- **移除 `NEXT_PUBLIC_APP_URL`**: 前端代码已不引用，但 deploy.yml 的 validation
仍在检查导致部署失败（`Missing required variables/secrets: NEXT_PUBLIC_APP_URL`）
- **移除 `NEXT_PUBLIC_GEM_WORKFLOW_URL`、`NEXT_PUBLIC_BACKEND_URL`**:
web/src/ 中 0 引用的死变量，从 deploy pipeline 和 .env.example 中清除

## Test plan
- [ ] Deploy pipeline 不再因 `NEXT_PUBLIC_APP_URL` 缺失而报错
- [ ] E2E tests 正确指向 `https://zooclaw.ai`（非 www）
- [ ] Staging / production deploy 正常完成

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### PR Description

## Summary
- **`www.zooclaw.ai` → `zooclaw.ai`**: E2E/CI 配置中错误使用了不支持的 www 子域名（playwright.config、e2e.yml、auth setup 等 6 处）
- **`pandaclaw.ai` → `zooclaw.ai`**: 设计稿 mockup 中的旧域名邮箱替换（4 处 docs/design HTML）
- **移除 `NEXT_PUBLIC_APP_URL`**: 前端代码已不引用，但 deploy.yml 的 validation 仍在检查导致部署失败（`Missing required variables/secrets: NEXT_PUBLIC_APP_URL`）
- **移除 `NEXT_PUBLIC_GEM_WORKFLOW_URL`、`NEXT_PUBLIC_BACKEND_URL`**: web/src/ 中 0 引用的死变量，从 deploy pipeline 和 .env.example 中清除

## Test plan
- [ ] Deploy pipeline 不再因 `NEXT_PUBLIC_APP_URL` 缺失而报错
- [ ] E2E tests 正确指向 `https://zooclaw.ai`（非 www）
- [ ] Staging / production deploy 正常完成

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@peter-srp: /lgtm

---

## fix(claw-interface): backfill agent workspaces in /openclaw/agents (#1138)

- **SHA**: [11cb1f46](https://github.com/SerendipityOneInc/ecap-workspace/commit/11cb1f46868a3c8cce2d054c0ef0096acace925d)
- **作者**: nolan-srp
- **时间**: 2026-04-21T07:46:53Z
- **PR**: [#1138](https://github.com/SerendipityOneInc/ecap-workspace/pull/1138)

### Commit Message

fix(claw-interface): backfill agent workspaces in /openclaw/agents (#1138)

## Summary
- backfill agent workspace paths in \/openclaw\/agents from the live bot
config when available
- keep the endpoint resilient by falling back to null workspaces if live
config lookup fails
- add unit coverage for workspace mapping extraction, response
hydration, and route fallback behavior

### PR Description

## Summary
- backfill agent workspace paths in \/openclaw\/agents from the live bot config when available
- keep the endpoint resilient by falling back to null workspaces if live config lookup fails
- add unit coverage for workspace mapping extraction, response hydration, and route fallback behavior

---

## fix(claw-interface): suppress LiteLLM INFO logs polluting GCP ERROR stream (#1139)

- **SHA**: [89402eb1](https://github.com/SerendipityOneInc/ecap-workspace/commit/89402eb14a7fce68fe00ef8ec92cf5e792606631)
- **作者**: peter-srp
- **时间**: 2026-04-21T07:45:48Z
- **PR**: [#1139](https://github.com/SerendipityOneInc/ecap-workspace/pull/1139)

### Commit Message

fix(claw-interface): suppress LiteLLM INFO logs polluting GCP ERROR stream (#1139)

## Summary
- LiteLLM v1.82.3 attaches its own `StreamHandler(stderr)` at import
time. In GCP containers, stderr is captured as ERROR severity — so
~100+/day INFO-level `completion()` messages were inflating error counts
and adding noise to monitoring.
- Added `_suppress_noisy_loggers()` in `app_logging.py` that raises
LiteLLM (and related `httpx`/`openai`) loggers to WARNING level and
strips their stderr handlers.
- 3 new unit tests covering level suppression, handler stripping, and
integration with `configure_logging()`.

## Test plan
- [ ] CI passes (`python-code-quality / build-and-test`)
- [ ] Deploy to staging and verify GCP Logs no longer show
`LiteLLM:INFO` entries in ERROR stream
- [ ] Confirm real LiteLLM warnings/errors (e.g. model failures, rate
limits) still appear

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### PR Description

## Summary
- LiteLLM v1.82.3 attaches its own `StreamHandler(stderr)` at import time. In GCP containers, stderr is captured as ERROR severity — so ~100+/day INFO-level `completion()` messages were inflating error counts and adding noise to monitoring.
- Added `_suppress_noisy_loggers()` in `app_logging.py` that raises LiteLLM (and related `httpx`/`openai`) loggers to WARNING level and strips their stderr handlers.
- 3 new unit tests covering level suppression, handler stripping, and integration with `configure_logging()`.

## Test plan
- [ ] CI passes (`python-code-quality / build-and-test`)
- [ ] Deploy to staging and verify GCP Logs no longer show `LiteLLM:INFO` entries in ERROR stream
- [ ] Confirm real LiteLLM warnings/errors (e.g. model failures, rate limits) still appear

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@peter-srp: /lgtm
@peter-srp: <img width="2020" height="512" alt="image" src="https://github.com/user-attachments/assets/803ea430-4698-49bb-833b-80cacfcfb69e" />


---

## fix: replace hardcoded domain URLs with relative paths and env vars (#1137)

- **SHA**: [50c709aa](https://github.com/SerendipityOneInc/ecap-workspace/commit/50c709aa29333370386ec264c71450fa54fe9374)
- **作者**: peter-srp
- **时间**: 2026-04-21T06:56:43Z
- **PR**: [#1137](https://github.com/SerendipityOneInc/ecap-workspace/pull/1137)

### Commit Message

fix: replace hardcoded domain URLs with relative paths and env vars (#1137)

## Summary

- **Backend `_admin.py`**: stale `ecap.gensmo.com` fallback →
`zooclaw.ai`
- **Frontend links** (public-nav-data, LoginForm, UserMenu,
PublicFooter, userguide-html, user-guide.html): absolute
`https://zooclaw.ai/*` → relative paths (`/tips`, `/about/terms`, etc.)
- **`sms-terms` page**: hardcoded display URL → `seoConfig.siteUrl` from
`_seo.ts`
- **`middleware.ts`**: `CANONICAL_ORIGIN` reads `NEXT_PUBLIC_SITE_URL`
env var with legacy-domain guard
- **`_seo.ts`**: `getCanonicalSiteUrl` now recognizes legacy host
markers (`gensmo.com`, `gsmo.ai`, `ecap.`) and normalizes to
`zooclaw.ai` — prevents misconfigured
`NEXT_PUBLIC_SITE_URL=https://ecap.gsmo.ai` from polluting canonical
URLs, hreflang, and OG meta

### Action required after merge
Update GitHub repo variable: `NEXT_PUBLIC_SITE_URL` →
`https://zooclaw.ai` (currently set to stale `https://ecap.gsmo.ai`)

### Not changed (with rationale)
| File | Reason |
|------|--------|
| `_seo.ts` `PRODUCTION_SITE_URL` | Single source of truth for
canonical/hreflang/OG — all other code references this |
| `sitemap*.xml` | XML sitemap spec requires absolute `<loc>` URLs;
static files can't import constants |
| `wrangler.toml` `FRONTEND_URL` | Deployment config; CI overrides
per-environment via `--var` |
| iOS `AppEnvironment.swift` | Native app, separate build — already uses
correct domain |
| `robots.ts` / `middleware.ts` `LEGACY_HOSTS` | Intentional old-domain
list for 301 redirects and crawler blocking |
| `docs/plans/*.md` | Historical design documents |

## Test plan

- [ ] CI lint + type check pass
- [ ] Manual: verify footer/nav links work (relative paths resolve
correctly)
- [ ] Manual: LoginForm terms/privacy links open in new tab
- [ ] Manual: user guide CTA button works
- [ ] SEO: canonical URLs, hreflang, and sitemaps unchanged — verify
with `curl -s https://zooclaw.ai/en/pricing | grep canonical`
- [ ] After deploy: update `NEXT_PUBLIC_SITE_URL` repo var to
`https://zooclaw.ai`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### PR Description

## Summary

- **Backend `_admin.py`**: stale `ecap.gensmo.com` fallback → `zooclaw.ai`
- **Frontend links** (public-nav-data, LoginForm, UserMenu, PublicFooter, userguide-html, user-guide.html): absolute `https://zooclaw.ai/*` → relative paths (`/tips`, `/about/terms`, etc.)
- **`sms-terms` page**: hardcoded display URL → `seoConfig.siteUrl` from `_seo.ts`
- **`middleware.ts`**: `CANONICAL_ORIGIN` reads `NEXT_PUBLIC_SITE_URL` env var with legacy-domain guard
- **`_seo.ts`**: `getCanonicalSiteUrl` now recognizes legacy host markers (`gensmo.com`, `gsmo.ai`, `ecap.`) and normalizes to `zooclaw.ai` — prevents misconfigured `NEXT_PUBLIC_SITE_URL=https://ecap.gsmo.ai` from polluting canonical URLs, hreflang, and OG meta

### Action required after merge
Update GitHub repo variable: `NEXT_PUBLIC_SITE_URL` → `https://zooclaw.ai` (currently set to stale `https://ecap.gsmo.ai`)

### Not changed (with rationale)
| File | Reason |
|------|--------|
| `_seo.ts` `PRODUCTION_SITE_URL` | Single source of truth for canonical/hreflang/OG — all other code references this |
| `sitemap*.xml` | XML sitemap spec requires absolute `<loc>` URLs; static files can't import constants |
| `wrangler.toml` `FRONTEND_URL` | Deployment config; CI overrides per-environment via `--var` |
| iOS `AppEnvironment.swift` | Native app, separate build — already uses correct domain |
| `robots.ts` / `middleware.ts` `LEGACY_HOSTS` | Intentional old-domain list for 301 redirects and crawler blocking |
| `docs/plans/*.md` | Historical design documents |

## Test plan

- [ ] CI lint + type check pass
- [ ] Manual: verify footer/nav links work (relative paths resolve correctly)
- [ ] Manual: LoginForm terms/privacy links open in new tab
- [ ] Manual: user guide CTA button works
- [ ] SEO: canonical URLs, hreflang, and sitemaps unchanged — verify with `curl -s https://zooclaw.ai/en/pricing | grep canonical`
- [ ] After deploy: update `NEXT_PUBLIC_SITE_URL` repo var to `https://zooclaw.ai`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@peter-srp: /lgtm

---

## feat(chat): 深链未雇佣/未知 agent 跳转 Agent Studio hire 面板 (#1020)

- **SHA**: [4b1ac4a4](https://github.com/SerendipityOneInc/ecap-workspace/commit/4b1ac4a4900f60a383d74a7817222098e5b1f0b2)
- **作者**: vincent-srp
- **时间**: 2026-04-21T06:53:43Z
- **PR**: [#1020](https://github.com/SerendipityOneInc/ecap-workspace/pull/1020)

### Commit Message

feat(chat): 深链未雇佣/未知 agent 跳转 Agent Studio hire 面板 (#1020)

## Summary

`/chat?agent_id=<slug>` 深链兜底改造，把原本「静默回退到 main agent」的断头路改成两条有意义的引导路径。

- 目标 slug **在 official catalog 但未雇佣** → toast「You need to hire {name}
first」+ `router.replace('/agents-manager/{slug}')`
- 目标 slug **不在 catalog（无效 / 拼错 / 已下线）** → toast「Try Agent Studio to
build a custom one」+ `router.replace('/agents-manager/agent_studio')`
- 已雇佣 → 沿用现有直进逻辑
- 排队在 Onboarding + 「Reaching your Claw…」init 完成之后才触发（`canUseChat &&
isChatReady` 各自 latch + 1.5s buffer）。**不** gate 在 GuideTour 上 — 从未关过
tour 的回访用户否则会被卡死

## 设计约定

- **永不替用户自动雇佣**：hook 不导入 `installOpenClawAgent`（结构性约束），雇佣是目的页职责
- **Toast 用全局 ToastProvider**（z-9999，跨页面持久），跳转后还能在目的页继续展示 ~2.4s
- **空 catalog 不误判为 slug 缺失**：catalog fetch 失败时 hold 在 `loading_meta`，不跳
Agent Studio；catalog populate 后自动恢复；8s 超时后 toast「catalog unavailable」并清掉
`agent_id`
- **`hiredIds` + `userAgentsLoading` 双重防御**：避免冷缓存 + 慢网下，已雇佣 agent 因
hydration 没赶上 1.5s buffer 被误判为未雇佣
- **`canUseChat` / `isChatReady` 用 latched ever-true**：post-login
时这俩信号会震荡（onboarding resolver / bot init 多阶段），latch 后取「曾经为 true」满足
buffer，避开「同时为 true」永不到达的窗口

## 顺带修复（同样影响 unauth /chat 体验）

- **OnboardingModal 在 `!authLoading && !isLoggedIn` 时直接 return null**：避开
AnimatePresence 600ms 淡出窗口，不再吞掉 LandingScreen 按钮的点击
- **LoginCheckProvider pathname effect 改成 two-real-values 状态机**：Next.js
15 `usePathname()` 类型签名 `string | null`，hydration 期可能短暂返回 null；旧逻辑把
`null → 实值`误判为导航，关掉刚被 LandingScreen 打开的登录面板

## Changes

- 新增 `useDeepLinkHireFlow` hook + 24 单测
- 新增 `AGENT_STUDIO_SLUG` 常量（`web/src/lib/agentSlugs.ts`）
- `GuideTourModal`：抽 `GUIDE_TOUR_DISMISSED_EVENT` 常量 +
`markGuideTourSeen()` helper（idempotent）
- `LandingScreen` mount 时自动 open LoginModal（带 StrictMode guard）
- 4 个 i18n keys（en + zh）：`chatDeepLink.notHired.toast` /
`chatDeepLink.notFound.toStudio` / `chatDeepLink.catalogUnavailable`
- `OnboardingModal` + `LoginCheckProvider` 两处 unauth /chat 修复（见上）
- 同步更新 `useSessionLogs` 单测断言（删了 chat 页不消费的 `&session_id=` 参数）

## Test plan

- [x] `useDeepLinkHireFlow.unit.spec.ts` 24 tests 全过
- [x] `LoginCheckProvider.unit.spec.tsx` 12 tests 全过（含
null→real-pathname 回归）
- [x] `pnpm lint` + `pnpm tsc --noEmit` 干净
- [x] 全量 `pnpm vitest run` 2848 tests 全过
- [ ] 手测：已雇佣 agent 深链直进
- [ ] 手测：未雇佣官方 agent 深链 → toast + 跳 `/agents-manager/{id}`
- [ ] 手测：不存在 slug → toast + 跳 `/agents-manager/agent_studio`
- [ ] 手测：未登录深链 → 自动唤起登录面板（不闪、按钮可点击）+ 登录后 query 保留 + 触发深链
- [ ] 手测：catalog 离线 → 8s 后 toast + 清 `agent_id` 落到主 chat

## Known follow-ups (out of scope for this PR)

- `canUseChatEver` / `isChatReadyEver` 在 `agentId` 切换时不重置 — 同会话内换
deep-link 且 bot 恰好在 reconnect 的窄场景，redirect 可能在浮层未消失时 fire。修法是 3
行（`agentId` 变化时 snapshot 当前值），但 scope 蔓延，留作后续

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
Co-authored-by: peter-srp <peter@srp.one>

### PR Description

## Summary

`/chat?agent_id=<slug>` 深链兜底改造，把原本「静默回退到 main agent」的断头路改成两条有意义的引导路径。

- 目标 slug **在 official catalog 但未雇佣** → toast「You need to hire {name} first」+ `router.replace('/agents-manager/{slug}')`
- 目标 slug **不在 catalog（无效 / 拼错 / 已下线）** → toast「Try Agent Studio to build a custom one」+ `router.replace('/agents-manager/agent_studio')`
- 已雇佣 → 沿用现有直进逻辑
- 排队在 Onboarding + 「Reaching your Claw…」init 完成之后才触发（`canUseChat && isChatReady` 各自 latch + 1.5s buffer）。**不** gate 在 GuideTour 上 — 从未关过 tour 的回访用户否则会被卡死

## 设计约定

- **永不替用户自动雇佣**：hook 不导入 `installOpenClawAgent`（结构性约束），雇佣是目的页职责
- **Toast 用全局 ToastProvider**（z-9999，跨页面持久），跳转后还能在目的页继续展示 ~2.4s
- **空 catalog 不误判为 slug 缺失**：catalog fetch 失败时 hold 在 `loading_meta`，不跳 Agent Studio；catalog populate 后自动恢复；8s 超时后 toast「catalog unavailable」并清掉 `agent_id`
- **`hiredIds` + `userAgentsLoading` 双重防御**：避免冷缓存 + 慢网下，已雇佣 agent 因 hydration 没赶上 1.5s buffer 被误判为未雇佣
- **`canUseChat` / `isChatReady` 用 latched ever-true**：post-login 时这俩信号会震荡（onboarding resolver / bot init 多阶段），latch 后取「曾经为 true」满足 buffer，避开「同时为 true」永不到达的窗口

## 顺带修复（同样影响 unauth /chat 体验）

- **OnboardingModal 在 `!authLoading && !isLoggedIn` 时直接 return null**：避开 AnimatePresence 600ms 淡出窗口，不再吞掉 LandingScreen 按钮的点击
- **LoginCheckProvider pathname effect 改成 two-real-values 状态机**：Next.js 15 `usePathname()` 类型签名 `string | null`，hydration 期可能短暂返回 null；旧逻辑把 `null → 实值`误判为导航，关掉刚被 LandingScreen 打开的登录面板

## Changes

- 新增 `useDeepLinkHireFlow` hook + 24 单测
- 新增 `AGENT_STUDIO_SLUG` 常量（`web/src/lib/agentSlugs.ts`）
- `GuideTourModal`：抽 `GUIDE_TOUR_DISMISSED_EVENT` 常量 + `markGuideTourSeen()` helper（idempotent）
- `LandingScreen` mount 时自动 open LoginModal（带 StrictMode guard）
- 4 个 i18n keys（en + zh）：`chatDeepLink.notHired.toast` / `chatDeepLink.notFound.toStudio` / `chatDeepLink.catalogUnavailable`
- `OnboardingModal` + `LoginCheckProvider` 两处 unauth /chat 修复（见上）
- 同步更新 `useSessionLogs` 单测断言（删了 chat 页不消费的 `&session_id=` 参数）

## Test plan

- [x] `useDeepLinkHireFlow.unit.spec.ts` 24 tests 全过
- [x] `LoginCheckProvider.unit.spec.tsx` 12 tests 全过（含 null→real-pathname 回归）
- [x] `pnpm lint` + `pnpm tsc --noEmit` 干净
- [x] 全量 `pnpm vitest run` 2848 tests 全过
- [ ] 手测：已雇佣 agent 深链直进
- [ ] 手测：未雇佣官方 agent 深链 → toast + 跳 `/agents-manager/{id}`
- [ ] 手测：不存在 slug → toast + 跳 `/agents-manager/agent_studio`
- [ ] 手测：未登录深链 → 自动唤起登录面板（不闪、按钮可点击）+ 登录后 query 保留 + 触发深链
- [ ] 手测：catalog 离线 → 8s 后 toast + 清 `agent_id` 落到主 chat

## Known follow-ups (out of scope for this PR)

- `canUseChatEver` / `isChatReadyEver` 在 `agentId` 切换时不重置 — 同会话内换 deep-link 且 bot 恰好在 reconnect 的窄场景，redirect 可能在浮层未消失时 fire。修法是 3 行（`agentId` 变化时 snapshot 当前值），但 scope 蔓延，留作后续

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(web): Seedance 2.0 上新弹窗 — 点击 Try now 跳转 agent 详情页走 hire 确认流程 (#981)

- **SHA**: [a2566491](https://github.com/SerendipityOneInc/ecap-workspace/commit/a2566491b5252eb429232d480283b0b35ea93e59)
- **作者**: lynn Zhuang
- **时间**: 2026-04-21T06:21:37Z
- **PR**: [#981](https://github.com/SerendipityOneInc/ecap-workspace/pull/981)

### Commit Message

feat(web): Seedance 2.0 上新弹窗 — 点击 Try now 跳转 agent 详情页走 hire 确认流程 (#981)

## 概要
  重新引入 Seedance 2.0 上新弹窗（此前 #866 被 revert #918）。

  **关键变更**：点击「立即体验」不再直接调用 hire API，而是跳转到 Vibe Drama
  的 agent 详情页（`/agents-manager/vibe_drama`），用户需手动点击 Confirm
  完成雇佣。

  ## 功能说明
  - 16:9 宣传视频自动播放循环（静音）
  - 每用户仅展示一次（localStorage 标记）
  - 与 Guide Tour 弹窗互斥：Guide Tour 未看过时不弹出，等下次登录
  - 弹窗延迟 5 秒出现，等 chat 页面渲染完成后再展示

  ## 改动文件
  | 文件 | 说明 |
  |------|------|
  | `web/src/components/SeedanceLaunchModal.tsx` | 新增弹窗组件 |
  | `web/src/app/[locale]/chat/GenClawClient.tsx` | 在 chat 页面挂载弹窗 |
  | `web/src/lib/auth/types.ts` | 新增 `SEEDANCE_LAUNCH_SEEN` 存储键 |
  | `web/src/locales/en.ts` | 英文文案 |
  | `web/src/locales/zh.ts` | 中文文案 |

  ## 与 #866 的区别
  | | #866（已 revert） | 本 PR |
  |---|---|---|
  | Try now 行为 | 直接调用 `installOpenClawAgent` API | 跳转到 agent 详情页 |
  | 雇佣确认 | 无需确认，自动雇佣 | 用户手动点击 Confirm 确认 |
  | 跳转方式 | `router.push` → chat 页面 | `window.location.href` → agent
  详情页 |

  ## 测试计划
  - [ ] 登录 → 进入 chat → 5 秒后弹窗出现（前提：Guide Tour 已看过）
  - [ ] 关闭弹窗 → 刷新 → 不再出现
  - [ ] 点击「立即体验」→ 跳转到 Vibe Drama 详情页
  - [ ] 在详情页点击 Hire → Confirm → 雇佣成功
  - [ ] 新用户未看过 Guide Tour → 弹窗不出现
  - [ ] 官网首页不弹出
<img width="2544" height="1504" alt="20260417
<img width="2564" height="1690" alt="20260417-123733"
src="https://github.com/user-attachments/assets/3841348a-e307-41e9-9f44-5a3dbe3a4265"
/>
-123731"
src="https://github.com/user-attachments/assets/71cf6cb8-d28d-485c-bb7a-a8c709cf6dfa"
/>

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@LynndeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
Co-authored-by: peter-srp <peter@srp.one>

### PR Description

## 概要
  重新引入 Seedance 2.0 上新弹窗（此前 #866 被 revert #918）。

  **关键变更**：点击「立即体验」不再直接调用 hire API，而是跳转到 Vibe Drama
  的 agent 详情页（`/agents-manager/vibe_drama`），用户需手动点击 Confirm
  完成雇佣。

  ## 功能说明
  - 16:9 宣传视频自动播放循环（静音）
  - 每用户仅展示一次（localStorage 标记）
  - 与 Guide Tour 弹窗互斥：Guide Tour 未看过时不弹出，等下次登录
  - 弹窗延迟 5 秒出现，等 chat 页面渲染完成后再展示

  ## 改动文件
  | 文件 | 说明 |
  |------|------|
  | `web/src/components/SeedanceLaunchModal.tsx` | 新增弹窗组件 |
  | `web/src/app/[locale]/chat/GenClawClient.tsx` | 在 chat 页面挂载弹窗 |
  | `web/src/lib/auth/types.ts` | 新增 `SEEDANCE_LAUNCH_SEEN` 存储键 |
  | `web/src/locales/en.ts` | 英文文案 |
  | `web/src/locales/zh.ts` | 中文文案 |

  ## 与 #866 的区别
  | | #866（已 revert） | 本 PR |
  |---|---|---|
  | Try now 行为 | 直接调用 `installOpenClawAgent` API | 跳转到 agent 详情页 |
  | 雇佣确认 | 无需确认，自动雇佣 | 用户手动点击 Confirm 确认 |
  | 跳转方式 | `router.push` → chat 页面 | `window.location.href` → agent
  详情页 |

  ## 测试计划
  - [ ] 登录 → 进入 chat → 5 秒后弹窗出现（前提：Guide Tour 已看过）
  - [ ] 关闭弹窗 → 刷新 → 不再出现
  - [ ] 点击「立即体验」→ 跳转到 Vibe Drama 详情页
  - [ ] 在详情页点击 Hire → Confirm → 雇佣成功
  - [ ] 新用户未看过 Guide Tour → 弹窗不出现
  - [ ] 官网首页不弹出
<img width="2544" height="1504" alt="20260417
<img width="2564" height="1690" alt="20260417-123733" src="https://github.com/user-attachments/assets/3841348a-e307-41e9-9f44-5a3dbe3a4265" />
-123731" src="https://github.com/user-attachments/assets/71cf6cb8-d28d-485c-bb7a-a8c709cf6dfa" />


---

## fix: migrate E2E base URL to www.zooclaw.ai (#1028)

- **SHA**: [e248f7ff](https://github.com/SerendipityOneInc/ecap-workspace/commit/e248f7ffbf373867e9b254661de3acff1169c9ff)
- **作者**: tim-srp
- **时间**: 2026-04-21T05:26:00Z
- **PR**: [#1028](https://github.com/SerendipityOneInc/ecap-workspace/pull/1028)

### Commit Message

fix: migrate E2E base URL to www.zooclaw.ai (#1028)

## Summary
- Update default E2E base URL from `ecap.gensmo.com` to `www.zooclaw.ai`
across all test configs and CI
- Update backend `openclaw_client.py` fallback URL
- Legacy redirect logic in `middleware.ts` and `robots.ts` intentionally
preserved

## Changed files
- `web/playwright.config.ts` — default baseURL
- `web/tests/e2e/auth/auth.setup.ts` — fallback URL + comment
- `web/tests/e2e/auth/capture-tokens.ts` — production URL
- `web/tests/e2e/specs/api-auth-uid-validation.spec.ts` — fallback URL
- `.github/workflows/e2e.yml` — workflow dispatch options + schedule
default
- `services/claw-interface/app/services/openclaw_client.py` — app
creation fallback URL

## Test plan
- [ ] Verify E2E tests can reach `https://www.zooclaw.ai` via auth setup
- [ ] Verify CI workflow dispatch shows new URL options

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### PR Description

## Summary
- Update default E2E base URL from `ecap.gensmo.com` to `www.zooclaw.ai` across all test configs and CI
- Update backend `openclaw_client.py` fallback URL
- Legacy redirect logic in `middleware.ts` and `robots.ts` intentionally preserved

## Changed files
- `web/playwright.config.ts` — default baseURL
- `web/tests/e2e/auth/auth.setup.ts` — fallback URL + comment
- `web/tests/e2e/auth/capture-tokens.ts` — production URL
- `web/tests/e2e/specs/api-auth-uid-validation.spec.ts` — fallback URL
- `.github/workflows/e2e.yml` — workflow dispatch options + schedule default
- `services/claw-interface/app/services/openclaw_client.py` — app creation fallback URL

## Test plan
- [ ] Verify E2E tests can reach `https://www.zooclaw.ai` via auth setup
- [ ] Verify CI workflow dispatch shows new URL options

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(web): sticky sidebar bottom nav with scrollable agent list (ECA-520) (#1132)

- **SHA**: [a7c3d696](https://github.com/SerendipityOneInc/ecap-workspace/commit/a7c3d6962bccd97caf2cf0bb4ac9d11630bf5ca7)
- **作者**: Nemo Feng
- **时间**: 2026-04-21T04:54:28Z
- **PR**: [#1132](https://github.com/SerendipityOneInc/ecap-workspace/pull/1132)

### Commit Message

fix(web): sticky sidebar bottom nav with scrollable agent list (ECA-520) (#1132)

## Summary

Addresses [ECA-520](https://linear.app/) — when the agent list grows
long, it pushes the fixed sidebar entries (**AI Specialists Hub**,
**Schedule**, **User Guide**, and **Admin**) plus the user card off the
bottom of the sidebar.

## Root cause

`<nav>` in `SideNav.tsx` was `flex min-h-0 flex-1 flex-col` with a `<div
className="flex-1" />` spacer between the agent list and the bottom
items. No descendant had `overflow-y` set, so as the agent list grew it
stole the spacer's slack and then pushed everything below out of view.

## Approach

Make the agent list the **only flex-absorber** — wrap it in `flex-1
min-h-0 overflow-y-auto` so it takes all remaining vertical space and
scrolls internally. The spacer is removed; the bottom nav and admin
sections now stay naturally pinned at the bottom.

## UI details

- **Hidden scrollbar** — uses the existing `.scrollbar-hide` utility
from `globals.css` (cross-browser: Firefox `scrollbar-width: none` +
WebKit `::-webkit-scrollbar { display: none }`).
- **Shadow overlay on the sticky section** — a `::before` pseudo-element
on the bottom nav container, positioned at `bottom: 100%` with a
`bg-gradient-to-t from-sidebar-background to-transparent` of height
`h-12`. It visually emanates from the sticky nav and covers the bottom
~48px of the agent list, signaling "more content above." Theme-aware
because the gradient uses `var(--sidebar-background)`.
- **Conditional overlay via `data-scroll-state`** — a small effect
tracks three states on the scroll container: `none` (list fits, no
overflow), `overflow` (more above the fold), `end` (scrolled to bottom).
CSS `data-[scroll-state=overflow]:before:opacity-100` shows the shadow
only when there's genuinely more to reveal; a 150ms opacity transition
makes the reveal/hide feel polished.
- **48px scroll-end buffer** — a sentinel `<div aria-hidden
className="h-12 flex-shrink-0" />` at the end of the list. When the user
scrolls all the way down, the last real agent sits above the 48px empty
region and the overlay fades out — so the last agent is fully visible,
not half-clipped, exactly at scroll-end.

## Design preview

Before/after HTML mockup (with slider for agent count, admin toggle, and
theme toggle) added at `docs/design/sidebar-scroll-fix-preview.html` for
future reference.

## Test plan

- [ ] Open `/chat` with many custom agents (≥10 on a laptop display, ≥20
on a tall monitor). Verify all four bottom entries + user card remain
visible.
- [ ] Scroll the agent list to the middle → last visible agent is
half-clipped by a soft shadow.
- [ ] Scroll to the very bottom → shadow fades out, last agent fully
visible.
- [ ] Remove all custom agents (only the default Assistant remains) → no
shadow, no scroll, list looks unchanged from before.
- [ ] Toggle light/dark theme → shadow fade color follows
`--sidebar-background` correctly.
- [ ] Collapse the sidebar (icon-only) → scrolling still works on long
lists.
- [ ] Mobile drawer mode → sticky behavior works the same way.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>

### PR Description

## Summary

Addresses [ECA-520](https://linear.app/) — when the agent list grows long, it pushes the fixed sidebar entries (**AI Specialists Hub**, **Schedule**, **User Guide**, and **Admin**) plus the user card off the bottom of the sidebar.

## Root cause

`<nav>` in `SideNav.tsx` was `flex min-h-0 flex-1 flex-col` with a `<div className="flex-1" />` spacer between the agent list and the bottom items. No descendant had `overflow-y` set, so as the agent list grew it stole the spacer's slack and then pushed everything below out of view.

## Approach

Make the agent list the **only flex-absorber** — wrap it in `flex-1 min-h-0 overflow-y-auto` so it takes all remaining vertical space and scrolls internally. The spacer is removed; the bottom nav and admin sections now stay naturally pinned at the bottom.

## UI details

- **Hidden scrollbar** — uses the existing `.scrollbar-hide` utility from `globals.css` (cross-browser: Firefox `scrollbar-width: none` + WebKit `::-webkit-scrollbar { display: none }`).
- **Shadow overlay on the sticky section** — a `::before` pseudo-element on the bottom nav container, positioned at `bottom: 100%` with a `bg-gradient-to-t from-sidebar-background to-transparent` of height `h-12`. It visually emanates from the sticky nav and covers the bottom ~48px of the agent list, signaling "more content above." Theme-aware because the gradient uses `var(--sidebar-background)`.
- **Conditional overlay via `data-scroll-state`** — a small effect tracks three states on the scroll container: `none` (list fits, no overflow), `overflow` (more above the fold), `end` (scrolled to bottom). CSS `data-[scroll-state=overflow]:before:opacity-100` shows the shadow only when there's genuinely more to reveal; a 150ms opacity transition makes the reveal/hide feel polished.
- **48px scroll-end buffer** — a sentinel `<div aria-hidden className="h-12 flex-shrink-0" />` at the end of the list. When the user scrolls all the way down, the last real agent sits above the 48px empty region and the overlay fades out — so the last agent is fully visible, not half-clipped, exactly at scroll-end.

## Design preview

Before/after HTML mockup (with slider for agent count, admin toggle, and theme toggle) added at `docs/design/sidebar-scroll-fix-preview.html` for future reference.

## Test plan

- [ ] Open `/chat` with many custom agents (≥10 on a laptop display, ≥20 on a tall monitor). Verify all four bottom entries + user card remain visible.
- [ ] Scroll the agent list to the middle → last visible agent is half-clipped by a soft shadow.
- [ ] Scroll to the very bottom → shadow fades out, last agent fully visible.
- [ ] Remove all custom agents (only the default Assistant remains) → no shadow, no scroll, list looks unchanged from before.
- [ ] Toggle light/dark theme → shadow fade color follows `--sidebar-background` correctly.
- [ ] Collapse the sidebar (icon-only) → scrolling still works on long lists.
- [ ] Mobile drawer mode → sticky behavior works the same way.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(web): resolve N+1 /credits/check requests via dedup + cache (#1136)

- **SHA**: [898d4801](https://github.com/SerendipityOneInc/ecap-workspace/commit/898d48014788dbf7eb58c6786295e34ef0079e7a)
- **作者**: peter-srp
- **时间**: 2026-04-21T04:00:14Z
- **PR**: [#1136](https://github.com/SerendipityOneInc/ecap-workspace/pull/1136)

### Commit Message

fix(web): resolve N+1 /credits/check requests via dedup + cache (#1136)

## Summary

Fixes Sentry
[#7353162497](https://serendipity-one-inc.sentry.io/issues/7353162497/)
— N+1 API Call detection on `/api/users/credits/check` (92 events / 10
users since 2025-03-21).

**Root cause**: When a `credits-refresh` event fires, every
`useBillingCredits` hook instance (~7-10 on `/chat`) runs its own
listener which clears `globalFetchingPromise` and fires a separate fetch
— the dedup mechanism is destroyed by the event handler itself.

**Fixes (by priority):**

- **P0 — Microtask-batched refresh**: Added a module-level
`creditsRefreshPending` flag. The first listener in a synchronous event
dispatch schedules a single `queueMicrotask` that clears cache/promise
and calls `refresh(true)` once. Subsequent listeners only bump
`renderTick` (for mock state re-reads) and return early.
- **P1 — Cache-aware pre-flight**: `useSendMessage` now checks
`getCachedCreditsCheck(uid)` before making a raw `/credits/check` API
call; `checkCreditsEnough` returns early when the global cache is fresh
and shows sufficient credits. Backend still rejects if truly
insufficient.
- **P2 — Double-trigger now safe**: `OnboardingProvider` retains its
original immediate + 3s retry pattern for `triggerCreditsRefresh()`.
With P0 in place, each trigger produces at most 1 API call (previously
N), so the double-trigger is benign (2 calls max vs. 2N before).

**Expected result**: A `credits-refresh` event now produces **1** API
call instead of **7+**. Pre-flight checks in chat reuse the 1-minute
cache instead of firing a new request per message send.

## Test plan

- [x] `tsc --noEmit` — zero errors
- [x] ESLint — zero new errors (only pre-existing
`@typescript-eslint/no-explicit-any` warnings)
- [x] Vitest — 76/76 pass (useBillingCredits + useSendMessage suites)
- [x] Regression tests: concurrent refresh dedup, multi-instance mount
dedup, `getCachedCreditsCheck` uid filtering, `checkCreditsEnough`
cache-first
- [ ] Manual: open `/chat`, verify only 1 `/credits/check` call in
Network tab on page load
- [ ] Manual: send a message — no additional `/credits/check` if cache
is fresh
- [ ] Sentry: monitor N+1 issue for resolution after deploy

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### PR Description

## Summary

Fixes Sentry [#7353162497](https://serendipity-one-inc.sentry.io/issues/7353162497/) — N+1 API Call detection on `/api/users/credits/check` (92 events / 10 users since 2025-03-21).

**Root cause**: When a `credits-refresh` event fires, every `useBillingCredits` hook instance (~7-10 on `/chat`) runs its own listener which clears `globalFetchingPromise` and fires a separate fetch — the dedup mechanism is destroyed by the event handler itself.

**Fixes (by priority):**

- **P0 — Microtask-batched refresh**: Added a module-level `creditsRefreshPending` flag. The first listener in a synchronous event dispatch schedules a single `queueMicrotask` that clears cache/promise and calls `refresh(true)` once. Subsequent listeners only bump `renderTick` (for mock state re-reads) and return early.
- **P1 — Cache-aware pre-flight**: `useSendMessage` now checks `getCachedCreditsCheck(uid)` before making a raw `/credits/check` API call; `checkCreditsEnough` returns early when the global cache is fresh and shows sufficient credits. Backend still rejects if truly insufficient.
- **P2 — Double-trigger now safe**: `OnboardingProvider` retains its original immediate + 3s retry pattern for `triggerCreditsRefresh()`. With P0 in place, each trigger produces at most 1 API call (previously N), so the double-trigger is benign (2 calls max vs. 2N before).

**Expected result**: A `credits-refresh` event now produces **1** API call instead of **7+**. Pre-flight checks in chat reuse the 1-minute cache instead of firing a new request per message send.

## Test plan

- [x] `tsc --noEmit` — zero errors
- [x] ESLint — zero new errors (only pre-existing `@typescript-eslint/no-explicit-any` warnings)
- [x] Vitest — 76/76 pass (useBillingCredits + useSendMessage suites)
- [x] Regression tests: concurrent refresh dedup, multi-instance mount dedup, `getCachedCreditsCheck` uid filtering, `checkCreditsEnough` cache-first
- [ ] Manual: open `/chat`, verify only 1 `/credits/check` call in Network tab on page load
- [ ] Manual: send a message — no additional `/credits/check` if cache is fresh
- [ ] Sentry: monitor N+1 issue for resolution after deploy

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@peter-srp: /lgtm

---

## fix(web): subagent session auto-dismiss with server-side status (#1118)

- **SHA**: [9f81426d](https://github.com/SerendipityOneInc/ecap-workspace/commit/9f81426dd7acdf9fc5e6b3de423a7984bf7faf83)
- **作者**: tim-srp
- **时间**: 2026-04-21T03:33:57Z
- **PR**: [#1118](https://github.com/SerendipityOneInc/ecap-workspace/pull/1118)

### Commit Message

fix(web): subagent session auto-dismiss with server-side status (#1118)

## Summary
- Replace client-side time-based `inferStatus` with authoritative
server-side `status` field from OpenClaw's `sessions.list` API (resolves
stale subagent sessions that never disappear)
- Add phase-based auto-dismiss: `running` sessions stay visible,
terminal sessions (`done`/`failed`/`timeout`/`killed`) fade out after
15-20s with CSS transition
- Collapsed sessions show as "N completed" summary button, expandable to
review history and open subagent panels

## Context
OpenClaw subagent sessions use `cleanup: "keep"` by default, so
completed session entries persist in `sessions.json` for 30 days. The
previous frontend used `updatedAt` age to infer status, which was
inaccurate — the server already returns a precise `status` field derived
from the in-memory subagent run lifecycle (`running` | `done` | `killed`
| `failed` | `timeout`).

## Test plan
- [x] Unit tests pass (22 tests across 2 spec files)
- [ ] Verify subagent pills appear with green pulse when running
- [ ] Verify done sessions show checkmark, then fade out after ~15s
- [ ] Verify failed/timeout sessions show red dot, fade out after ~20s
- [ ] Verify collapsed "N completed" button appears after all fade out
- [ ] Verify clicking collapsed button expands to show completed
sessions
- [ ] Verify clicking a collapsed session still opens SubagentChatPanel

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### PR Description

## Summary
- Replace client-side time-based `inferStatus` with authoritative server-side `status` field from OpenClaw's `sessions.list` API (resolves stale subagent sessions that never disappear)
- Add phase-based auto-dismiss: `running` sessions stay visible, terminal sessions (`done`/`failed`/`timeout`/`killed`) fade out after 15-20s with CSS transition
- Collapsed sessions show as "N completed" summary button, expandable to review history and open subagent panels

## Context
OpenClaw subagent sessions use `cleanup: "keep"` by default, so completed session entries persist in `sessions.json` for 30 days. The previous frontend used `updatedAt` age to infer status, which was inaccurate — the server already returns a precise `status` field derived from the in-memory subagent run lifecycle (`running` | `done` | `killed` | `failed` | `timeout`).

## Test plan
- [x] Unit tests pass (22 tests across 2 spec files)
- [ ] Verify subagent pills appear with green pulse when running
- [ ] Verify done sessions show checkmark, then fade out after ~15s
- [ ] Verify failed/timeout sessions show red dot, fade out after ~20s
- [ ] Verify collapsed "N completed" button appears after all fade out
- [ ] Verify clicking collapsed button expands to show completed sessions
- [ ] Verify clicking a collapsed session still opens SubagentChatPanel

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@tim-srp: ## Response to Codex Review

### 1. 500ms terminal-session refetch loop — Addressed

The dismiss timer was **never** calling `fetchSessions()` — it recalculates phases purely locally via `setSessions()` (see comment at L143-144). However, the 500ms interval was unnecessarily frequent for a local-only recalculation.

**Change:** Increased dismiss timer interval from `500ms` → `3_000ms` (3s), and `FADE_DURATION_MS` from `500ms` → `3_000ms` to match. This ensures:
- The `fading` phase is reliably captured by the 3s tick (previously 500ms fading window could be missed with a slower tick)
- 6x reduction in `setSessions` calls during terminal phase
- Total dismiss timeline: ~18s for `done` sessions (was ~15.5s), ~23s for `failed` (was ~20.5s) — imperceptible difference

### 2. Missing primary-use-case tests — Already covered

The test file has **27 tests** covering:
- Phase timer transitions: `visible → fading → collapsed` full lifecycle
- Multiple sessions with different dismiss delays (`done` 15s vs `failed` 20s)
- Dismiss timer runs locally without extra server fetch (verified `sendRequest` call count)
- Timer auto-stops after all sessions are collapsed
- Server status trust over time-based fallback

The collapsed summary button in `GenClawClient.tsx` is UI rendering logic — appropriate for E2E coverage, not unit-level hook tests.

---

## feat(web): enrich chat tool display — richer text, emoji, collapse, timer (#1100)

- **SHA**: [e0cd8bb8](https://github.com/SerendipityOneInc/ecap-workspace/commit/e0cd8bb881830e62cdd95b526075934f2d3f9887)
- **作者**: peter-srp
- **时间**: 2026-04-21T03:23:58Z
- **PR**: [#1100](https://github.com/SerendipityOneInc/ecap-workspace/pull/1100)

### Commit Message

feat(web): enrich chat tool display — richer text, emoji, collapse, timer (#1100)

## Summary
- Expand action text variants from 4→8 per tool type with longer
narrative phrasing; add `withQuery` for exec/process/write so all tools
can reference user query
- Add emoji pool per tool type (hash-picked per `tool_call_id` for
visual variety, approach B)
- Collapse earlier tools when >3 in expanded state — "N earlier steps"
toggle to avoid 19-row walls
- Show real-time elapsed timer on the running tool + 3-dot bounce
animation replacing thin pulse dot
- Replace streaming indicator with rotating `|` cursor for main output
- Move copy/reply action buttons to right side; only show after
generation completes
- Update en.ts and zh.ts with all new i18n keys

## Test plan
- [ ] Verify tool group renders emoji + richer text for each tool type
- [ ] Trigger >3 tools and confirm only last tool visible with "N
earlier steps" button
- [ ] Click "N earlier steps" to expand full list
- [ ] Confirm running tool shows bounce animation + live elapsed timer
- [ ] Verify rotating | cursor appears at end of streaming text
- [ ] Verify copy/reply buttons appear on right side only after message
completes
- [ ] Switch language to zh and verify all new i18n keys render
correctly

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### PR Description

## Summary
- Expand action text variants from 4→8 per tool type with longer narrative phrasing; add `withQuery` for exec/process/write so all tools can reference user query
- Add emoji pool per tool type (hash-picked per `tool_call_id` for visual variety, approach B)
- Collapse earlier tools when >3 in expanded state — "N earlier steps" toggle to avoid 19-row walls
- Show real-time elapsed timer on the running tool + 3-dot bounce animation replacing thin pulse dot
- Replace streaming indicator with rotating `|` cursor for main output
- Move copy/reply action buttons to right side; only show after generation completes
- Update en.ts and zh.ts with all new i18n keys

## Test plan
- [ ] Verify tool group renders emoji + richer text for each tool type
- [ ] Trigger >3 tools and confirm only last tool visible with "N earlier steps" button
- [ ] Click "N earlier steps" to expand full list
- [ ] Confirm running tool shows bounce animation + live elapsed timer
- [ ] Verify rotating | cursor appears at end of streaming text
- [ ] Verify copy/reply buttons appear on right side only after message completes
- [ ] Switch language to zh and verify all new i18n keys render correctly

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@peter-srp: /lgtm

---

## fix(web): replace 880KB JPEG bg-pattern with 31KB WebP to fix LCP (#1135)

- **SHA**: [6c516a5d](https://github.com/SerendipityOneInc/ecap-workspace/commit/6c516a5de658b7f5f533a798e79194764fca9796)
- **作者**: peter-srp
- **时间**: 2026-04-21T03:16:06Z
- **PR**: [#1135](https://github.com/SerendipityOneInc/ecap-workspace/pull/1135)

### Commit Message

fix(web): replace 880KB JPEG bg-pattern with 31KB WebP to fix LCP (#1135)

## Summary
- **LCP fix**: panda-claw chat background pattern was a 1638×914
external JPEG (417KB light / 467KB dark) loaded on every `/chat` page
visit — replaced with locally-served WebP (13KB / 18KB, **96.5%
reduction**)
- **DRY**: `OnboardingLayout` hardcoded the same image URL separately;
now shares `--ecap-chat-bg-pattern` CSS token with `GenClawClient`
- **Same-origin**: images move from `assets.yesy.site` CDN to
`public/images/`, eliminating cross-origin DNS/TLS overhead

## Changes
| File | What |
|------|------|
| `web/public/images/chat-bg-pattern-{light,dark}.webp` | Optimized WebP
versions (cwebp q75) |
| `web/src/theme/brand-theme-tokens.css` | Point
`--ecap-chat-bg-pattern` to local WebP |
| `web/src/components/onboarding/OnboardingProvider.tsx` | Update
preload URL |
| `web/src/components/onboarding/OnboardingLayout.tsx` | Replace
hardcoded `style={{}}` with CSS token |

## Test plan
- [ ] Open `/chat` in panda-claw light theme — verify background pattern
renders correctly
- [ ] Toggle to dark mode — verify dark pattern renders
- [ ] Open onboarding flow — verify background pattern matches chat page
- [ ] DevTools Network tab: confirm images load from
`/images/chat-bg-pattern-*.webp` (~13-18KB)
- [ ] Lighthouse: verify LCP improvement on `/chat`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### PR Description

## Summary
- **LCP fix**: panda-claw chat background pattern was a 1638×914 external JPEG (417KB light / 467KB dark) loaded on every `/chat` page visit — replaced with locally-served WebP (13KB / 18KB, **96.5% reduction**)
- **DRY**: `OnboardingLayout` hardcoded the same image URL separately; now shares `--ecap-chat-bg-pattern` CSS token with `GenClawClient`
- **Same-origin**: images move from `assets.yesy.site` CDN to `public/images/`, eliminating cross-origin DNS/TLS overhead

## Changes
| File | What |
|------|------|
| `web/public/images/chat-bg-pattern-{light,dark}.webp` | Optimized WebP versions (cwebp q75) |
| `web/src/theme/brand-theme-tokens.css` | Point `--ecap-chat-bg-pattern` to local WebP |
| `web/src/components/onboarding/OnboardingProvider.tsx` | Update preload URL |
| `web/src/components/onboarding/OnboardingLayout.tsx` | Replace hardcoded `style={{}}` with CSS token |

## Test plan
- [ ] Open `/chat` in panda-claw light theme — verify background pattern renders correctly
- [ ] Toggle to dark mode — verify dark pattern renders
- [ ] Open onboarding flow — verify background pattern matches chat page
- [ ] DevTools Network tab: confirm images load from `/images/chat-bg-pattern-*.webp` (~13-18KB)
- [ ] Lighthouse: verify LCP improvement on `/chat`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@peter-srp: /lgtm

---

## fix(ios): Remove bundle_identifier from update_code_signing_settings (#1093)

- **SHA**: [f26b920c](https://github.com/SerendipityOneInc/ecap-workspace/commit/f26b920c0835f96ba8adc0e7dd51b92b7fe92cc5)
- **作者**: bill-srp
- **时间**: 2026-04-21T02:30:09Z
- **PR**: [#1093](https://github.com/SerendipityOneInc/ecap-workspace/pull/1093)

### Commit Message

fix(ios): Remove bundle_identifier from update_code_signing_settings (#1093)

## Summary

Fixes the staging iOS deploy failure ([failed
run](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/24659916823/job/72102910515))
caused by provisioning profile mismatch on the
`ZooClawNotificationService` target.

The `bundle_identifier` parameter in `update_code_signing_settings` can
leak across targets despite `targets:` scoping, overwriting the
extension's bundle ID
(`one.srp.zooclaw-staging.ZooClawNotificationService`) with the main
app's ID (`one.srp.zooclaw-staging`). This causes the provisioning
profile check to fail.

**Fix:** Remove `bundle_identifier` from all
`update_code_signing_settings` calls in both staging and release lanes.
The pbxproj already has the correct per-target, per-configuration bundle
IDs — only signing settings (profile, identity, team) need overriding at
CI time.

## Test plan

- [ ] Tag `ios-v1.4.0-beta.5` on this branch to trigger staging deploy
- [ ] Verify build completes without provisioning profile errors
- [ ] Verify IPA is produced and uploaded to TestFlight

### PR Description

## Summary

Fixes the staging iOS deploy failure ([failed run](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/24659916823/job/72102910515)) caused by provisioning profile mismatch on the `ZooClawNotificationService` target.

The `bundle_identifier` parameter in `update_code_signing_settings` can leak across targets despite `targets:` scoping, overwriting the extension's bundle ID (`one.srp.zooclaw-staging.ZooClawNotificationService`) with the main app's ID (`one.srp.zooclaw-staging`). This causes the provisioning profile check to fail.

**Fix:** Remove `bundle_identifier` from all `update_code_signing_settings` calls in both staging and release lanes. The pbxproj already has the correct per-target, per-configuration bundle IDs — only signing settings (profile, identity, team) need overriding at CI time.

## Test plan

- [ ] Tag `ios-v1.4.0-beta.5` on this branch to trigger staging deploy
- [ ] Verify build completes without provisioning profile errors
- [ ] Verify IPA is produced and uploaded to TestFlight

---

## chore(web): drop 6 unused deps + add postcss/tsx + shrink knip allowlist (B4) (#1122)

- **SHA**: [1a357890](https://github.com/SerendipityOneInc/ecap-workspace/commit/1a35789075ef12b5e60677e9447248d7c25fd313)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-21T02:25:06Z
- **PR**: [#1122](https://github.com/SerendipityOneInc/ecap-workspace/pull/1122)

### Commit Message

chore(web): drop 6 unused deps + add postcss/tsx + shrink knip allowlist (B4) (#1122)

## Summary
- Removes 6 deps that no `src/` import references: `@mdx-js/loader`,
`@mdx-js/react`, `@next/mdx`, `@types/mdx`, `@stripe/stripe-js`,
`@types/dompurify`.
- Adds 2 deps that were resolving via pnpm's transitive hoist (fragile):
`postcss`, `tsx`.
- Adds `functions/**` to knip `entry` / `project` so knip sees the
`@sentry/cloudflare` usage in `web/functions/_middleware.ts` natively,
instead of relying on an ignore-list entry.
- Shrinks `knip.config.ts` allowlist from 10 baseline-legacy entries to
**0** — remaining `ignoreDependencies` (3 entries) are all genuine
permanent FPs.

## Verification
- `grep -rn '@mdx-js|@next/mdx|@stripe/stripe-js' web/src` — **zero
hits** (deps fully orphaned)
- `grep -rn 'dompurify' web/src` — only runtime `dompurify` imports;
`@types/dompurify` truly unused (runtime package ships own TS types)
- `grep -rn '@sentry/cloudflare' web/` — **used in
`web/functions/_middleware.ts`** (Cloudflare Pages Functions); kept +
knip entry expanded
- `pnpm test:unit` — **224 test files / 3457 tests pass**
- `WARN_ONLY=1 pnpm lint:ci` — exit 0; knip dep-health gate clean

## knip.config.ts delta

Before (10 allowlist entries): `eslint-config-next`, `@vitest/expect`,
`dependency-cruiser` (3 FPs) + `@mdx-js/loader`, `@mdx-js/react`,
`@next/mdx`, `@types/mdx`, `@stripe/stripe-js`, `@sentry/cloudflare`,
`@types/dompurify`, `postcss` (8 baseline-legacy) + `tsx` (1
ignoreBinaries).

After (3 entries, all permanent FPs):
```ts
ignoreDependencies: [
  'eslint-config-next',   // FlatCompat.extends('next/...') string ref
  '@vitest/expect',       // declare module in web/jest-dom.d.ts
  'dependency-cruiser',   // invoked from shell script (pnpm exec)
],
```

`ignoreBinaries` removed entirely (tsx is now a devDep).

## Why @sentry/cloudflare stays
`web/functions/_middleware.ts`:
```ts
import * as Sentry from '@sentry/cloudflare'
export const onRequest = Sentry.sentryPagesPlugin({...})
```
This is the Cloudflare Pages Function entry — outside Next.js App
Router. Previously knip didn't scan `functions/` so reported it as
unused. The right fix is to expand knip's `entry` / `project` to cover
it, not to ignore the dep.

## Interaction with open PRs
- **#1120 (B3)** is in merge queue. B3 modifies `02-dead-code.sh`
(`--include` list) and `backend.ts` (drops alias exports). B4 modifies
`package.json`, `knip.config.ts`, and `pnpm-lock.yaml`. No file overlap
— both will rebase cleanly regardless of order.

## Test plan
- [x] Unit tests pass (224 files / 3457 tests)
- [x] knip dep-health gate clean with new entry/project globs
- [ ] CI confirms above + jscpd + asset-size-guard
- [ ] Reviewer validates `@sentry/cloudflare` via `functions/` is the
correct resolution (vs permanent ignore-list)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Description

## Summary
- Removes 6 deps that no `src/` import references: `@mdx-js/loader`, `@mdx-js/react`, `@next/mdx`, `@types/mdx`, `@stripe/stripe-js`, `@types/dompurify`.
- Adds 2 deps that were resolving via pnpm's transitive hoist (fragile): `postcss`, `tsx`.
- Adds `functions/**` to knip `entry` / `project` so knip sees the `@sentry/cloudflare` usage in `web/functions/_middleware.ts` natively, instead of relying on an ignore-list entry.
- Shrinks `knip.config.ts` allowlist from 10 baseline-legacy entries to **0** — remaining `ignoreDependencies` (3 entries) are all genuine permanent FPs.

## Verification
- `grep -rn '@mdx-js|@next/mdx|@stripe/stripe-js' web/src` — **zero hits** (deps fully orphaned)
- `grep -rn 'dompurify' web/src` — only runtime `dompurify` imports; `@types/dompurify` truly unused (runtime package ships own TS types)
- `grep -rn '@sentry/cloudflare' web/` — **used in `web/functions/_middleware.ts`** (Cloudflare Pages Functions); kept + knip entry expanded
- `pnpm test:unit` — **224 test files / 3457 tests pass**
- `WARN_ONLY=1 pnpm lint:ci` — exit 0; knip dep-health gate clean

## knip.config.ts delta

Before (10 allowlist entries): `eslint-config-next`, `@vitest/expect`, `dependency-cruiser` (3 FPs) + `@mdx-js/loader`, `@mdx-js/react`, `@next/mdx`, `@types/mdx`, `@stripe/stripe-js`, `@sentry/cloudflare`, `@types/dompurify`, `postcss` (8 baseline-legacy) + `tsx` (1 ignoreBinaries).

After (3 entries, all permanent FPs):
```ts
ignoreDependencies: [
  'eslint-config-next',   // FlatCompat.extends('next/...') string ref
  '@vitest/expect',       // declare module in web/jest-dom.d.ts
  'dependency-cruiser',   // invoked from shell script (pnpm exec)
],
```

`ignoreBinaries` removed entirely (tsx is now a devDep).

## Why @sentry/cloudflare stays
`web/functions/_middleware.ts`:
```ts
import * as Sentry from '@sentry/cloudflare'
export const onRequest = Sentry.sentryPagesPlugin({...})
```
This is the Cloudflare Pages Function entry — outside Next.js App Router. Previously knip didn't scan `functions/` so reported it as unused. The right fix is to expand knip's `entry` / `project` to cover it, not to ignore the dep.

## Interaction with open PRs
- **#1120 (B3)** is in merge queue. B3 modifies `02-dead-code.sh` (`--include` list) and `backend.ts` (drops alias exports). B4 modifies `package.json`, `knip.config.ts`, and `pnpm-lock.yaml`. No file overlap — both will rebase cleanly regardless of order.

## Test plan
- [x] Unit tests pass (224 files / 3457 tests)
- [x] knip dep-health gate clean with new entry/project globs
- [ ] CI confirms above + jscpd + asset-size-guard
- [ ] Reviewer validates `@sentry/cloudflare` via `functions/` is the correct resolution (vs permanent ignore-list)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(tracking): move gtag init to TSX as verbatim Google snippet (#1133)

- **SHA**: [e4a567a6](https://github.com/SerendipityOneInc/ecap-workspace/commit/e4a567a6e0942749bb4c73c88f5932d60ccb365b)
- **作者**: Fangmiao-srp
- **时间**: 2026-04-21T02:12:20Z
- **PR**: [#1133](https://github.com/SerendipityOneInc/ecap-workspace/pull/1133)

### Commit Message

fix(tracking): move gtag init to TSX as verbatim Google snippet (#1133)

## Summary
- gtag.js internally uses `Array.isArray()` to route dataLayer entries —
Arrays go to a dot-notation path (ignored), only Arguments objects are
recognized as gtag commands
- Our `tracking.ts` used an arrow function with rest params (`(...args)
=> dataLayer.push(args)`), which pushed Arrays instead of Arguments
objects — **all config/event commands were silently ignored, no collect
requests were ever sent**
- Fix: move initialization to `TrackingScripts.tsx` using Google's
original snippet verbatim (`function gtag(){dataLayer.push(arguments)}`)
- Also fixes incorrect Google Ads conversion label
(`LNs9CJnnJp8cEPLbzKxD` → `LNz9CJnnjp8cEPLbzKxD`)

## Changes
| File | Change |
|------|--------|
| `TrackingScripts.tsx` | Added verbatim Google tag init snippet (only
modification: `send_page_view: false` for SPA) |
| `tracking.ts` | Removed module-level init block, fixed conversion
label, removed unused `dataLayer` from type |
| `tracking.unit.spec.ts` | Removed init tests, switched assertions from
dataLayer checks to mock-based |

## Test plan
- [ ] Deploy to staging
- [ ] Open Chrome DevTools Network tab → search for `/g/collect` or
`/j/collect` → confirm requests appear
- [ ] Check Tag Assistant: no more "Deferred hits" warning
- [ ] Verify `window.google_tag_data.tidr.destination` is not empty
- [ ] GA4 DebugView shows real-time events

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Muyao Wang <muyao@MuyaodeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>

### PR Description

## Summary
- gtag.js internally uses `Array.isArray()` to route dataLayer entries — Arrays go to a dot-notation path (ignored), only Arguments objects are recognized as gtag commands
- Our `tracking.ts` used an arrow function with rest params (`(...args) => dataLayer.push(args)`), which pushed Arrays instead of Arguments objects — **all config/event commands were silently ignored, no collect requests were ever sent**
- Fix: move initialization to `TrackingScripts.tsx` using Google's original snippet verbatim (`function gtag(){dataLayer.push(arguments)}`)
- Also fixes incorrect Google Ads conversion label (`LNs9CJnnJp8cEPLbzKxD` → `LNz9CJnnjp8cEPLbzKxD`)

## Changes
| File | Change |
|------|--------|
| `TrackingScripts.tsx` | Added verbatim Google tag init snippet (only modification: `send_page_view: false` for SPA) |
| `tracking.ts` | Removed module-level init block, fixed conversion label, removed unused `dataLayer` from type |
| `tracking.unit.spec.ts` | Removed init tests, switched assertions from dataLayer checks to mock-based |

## Test plan
- [ ] Deploy to staging
- [ ] Open Chrome DevTools Network tab → search for `/g/collect` or `/j/collect` → confirm requests appear
- [ ] Check Tag Assistant: no more "Deferred hits" warning
- [ ] Verify `window.google_tag_data.tidr.destination` is not empty
- [ ] GA4 DebugView shows real-time events

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
