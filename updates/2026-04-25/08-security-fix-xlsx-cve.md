---
title: "安全修复：解决 xlsx 库 4 个高危漏洞"
type: "Bug Fix"
priority: "高"
date: "2026-04-25"
status: "待审核"
channels: "Discord + changelog"
---

# 安全修复：解决 xlsx 库 4 个高危漏洞

## 核心宣传点

替换了存在安全漏洞的 xlsx 组件，修复 4 个高危 CVE，保障数据安全。

## 原始内容

Commit: 539e72006d75061520e5a1af2d21e03a50048ac7

Message:
fix(web): replace xlsx with read-excel-file to close 4 high CVEs (#1299)

## Summary
- Removes `xlsx@^0.18.5` and replaces with `read-excel-file@^8.0.3` in
the single consumer,
`web/src/components/artifacts/renderers/ExcelRenderer.tsx`.
- Closes 4 open Dependabot alerts on `xlsx` (#23 prototype pollution,
#24 ReDoS, #25, #26) — SheetJS removed the patched `0.19.3`/`0.20.2`
releases from npm, so no bump or `pnpm.overrides` can close these.
- Usage in this repo is **Import/Parse user uploads** (URL → Blob → rows
for preview), which is the "must migrate" path from #1254 — accept-risk
is not defensible.

## Why `read-excel-file` over SheetJS CDN tarball
- Option A (CDN tarball `https://cdn.sheetjs.com/...`) bypasses npm
provenance and the repo's `minimumReleaseAge` supply-chain gate, and
keeps the same SheetJS code that produced the CVE class.
- Option B with `read-excel-file`: npm-native, browser-focused, still
under ecosystem review. API (`readXlsxFile(blob, { sheet })` +
`readSheetNames(blob)`) maps 1:1 onto the existing `(rows, sheets,
activeSheet)` state — minimal-diff migration.
- Bundle shrinks from ~400KB (xlsx) to ~100KB (read-excel-file) inside
the dynamically-imported chunk.

## Behavior diff for users
| Case | Before | After |
|---|---|---|
| Text / number / formula-result cells | ✅ | ✅ |
| Date cells | ❌ Rendered as Excel serial number (e.g. `45291`) because
`cellDates: true` was not set | ✅ Native `Date` → `toLocaleDateString()`
|
| Multi-sheet tabs | ✅ | ✅ |
| Merged cells, styling, virtualization | ❌ (unchanged) | ❌ (unchanged —
out of scope) |
| Exotic/malformed xlsx files | Sometimes parsed by SheetJS's lenient
parser | May fall through to existing `.catch()` → "Failed to load" +
download link (no crash) |

## Test plan
- [ ] Open an xlsx attachment preview in chat artifacts — rows render
- [ ] Open an xlsx in Assets preview area — rows render
- [ ] Multi-sheet xlsx: sheet tabs switch content
- [ ] Spreadsheet with date column: dates render as dates, not
`45291`-style serial numbers
- [ ] Broken/corrupt xlsx URL: shows error message + Download link, no
white screen
- [ ] CI: `code-quality / lint-and-test` green

Closes #1254

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

PR Description:
## Summary
- Removes `xlsx@^0.18.5` and replaces with `read-excel-file@^8.0.3` in the single consumer, `web/src/components/artifacts/renderers/ExcelRenderer.tsx`.
- Closes 4 open Dependabot alerts on `xlsx` (#23 prototype pollution, #24 ReDoS, #25, #26) — SheetJS removed the patched `0.19.3`/`0.20.2` releases from npm, so no bump or `pnpm.overrides` can close these.
- Usage in this repo is **Import/Parse user uploads** (URL → Blob → rows for preview), which is the "must migrate" path from #1254 — accept-risk is not defensible.

## Why `read-excel-file` over SheetJS CDN tarball
- Option A (CDN tarball `https://cdn.sheetjs.com/...`) bypasses npm provenance and the repo's `minimumReleaseAge` supply-chain gate, and keeps the same SheetJS code that produced the CVE class.
- Option B with `read-excel-file`: npm-native, browser-focused, still under ecosystem review. API (`readXlsxFile(blob, { sheet })` + `readSheetNames(blob)`) maps 1:1 onto the existing `(rows, sheets, activeSheet)` state — minimal-diff migration.
- Bundle shrinks from ~400KB (xlsx) to ~100KB (read-excel-file) inside the dynamically-imported chunk.

## Behavior diff for users
| Case | Before | After |
|---|---|---|
| Text / number / formula-result cells | ✅ | ✅ |
| Date cells | ❌ Rendered as Excel serial number (e.g. `45291`) because `cellDates: true` was not set | ✅ Native `Date` → `toLocaleDateString()` |
| Multi-sheet tabs | ✅ | ✅ |
| Merged cells, styling, virtualization | ❌ (unchanged) | ❌ (unchanged — out of scope) |
| Exotic/malformed xlsx files | Sometimes parsed by SheetJS's lenient parser | May fall through to existing `.catch()` → "Failed to load" + download link (no crash) |

## Test plan
- [ ] Open an xlsx attachment preview in chat artifacts — rows render
- [ ] Open an xlsx in Assets preview area — rows render
- [ ] Multi-sheet xlsx: sheet tabs switch content
- [ ] Spreadsheet with date column: dates render as dates, not `45291`-style serial numbers
- [ ] Broken/corrupt xlsx URL: shows error message + Download link, no white screen
- [ ] CI: `code-quality / lint-and-test` green

Closes #1254

🤖 Generated with [Claude Code](https://claude.com/claude-code)
