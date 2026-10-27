---
title: "修复：官网活动页切中文被甩回首页，现已上线完整中文版"
type: "Bug Fix"
priority: "中"
date: "2026-10-26"
status: "待审核"
channels: ""
---

# 修复：官网活动页切中文被甩回首页，现已上线完整中文版

## 核心宣传点

官网活动页此前只登记了英文版本，在该页面把语言切到中文时，语言切换器会按既定逻辑回落到中文首页，等于把访客直接甩出活动页。现在补上了完整的 `/zh/events` 页面：九张活动卡片、导航、筛选项、日期、无障碍标签、页面元数据和结构化数据全部改写为中文编辑文案，图片、事实信息和跳转链接保持原样；切换语言时会停留在活动页，并保留当前的查询参数和章节锚点。

中文排版改用官方的 Noto Serif SC 标题字体与 Noto Sans SC 正文字体，配合中文字距和响应式标题字号；字体注册表只在活动页路由加载，英文版和共享的页头页脚排版不受影响。`/zh/events` 已登记进路由契约与站点地图。本地在 390 / 768 / 1440 三档宽度下验证通过。

## 分级

- 内部：P2
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `5aae85bac7c69e31a99e88a6152ae15b197cbfcc`
- PR: #4141
- 作者：anna-srp
- 日期：2026-10-26T11:09:48Z

### Commit Message

```
fix(events): add Chinese localization and brand typography (#4141)

## Summary

Selecting Chinese from Events previously returned visitors to the
homepage. Add a complete `/zh/events` page and keep visitors on Events
when switching languages, including their query string and section
anchor.

- Localize all nine event cards, navigation, filters, dates,
accessibility labels, metadata and structured data with editorial
Chinese copy. Keep the original images, facts and destination links.
- Use the official Noto Serif SC display face and Noto Sans SC content
face with Chinese spacing and responsive heading sizes. Load the font
registry only from the Events route; Events-specific aliases leave
English and shared Header/Footer typography unchanged.
- Register `/zh/events` in the route contract and sitemap. Document
bilingual content maintenance and provide a deterministic font-manifest
generator using the existing design-system assets and licenses.

## Root cause

Events was registered as English-only, so the shared language switcher
correctly fell back to the selected language's homepage. The page also
had no Chinese content or explicitly loaded Chinese brand fonts.

## Test plan

- [x] Seven targeted unit-test files: 146 tests passed, covering
localized rendering, filtering, source-link preservation, structured
data, SEO, sitemap, route boundaries and language switching with
query/hash preservation. After review fixes, reran the three affected
files plus the new font contract test: 43 tests passed.
- [x] Font manifest generation check is included in the unit suite; all
202 official font faces preserve their Unicode subsets and variable
weights without duplicating font binaries.
- [x] Local browser verification at 390, 768 and 1440 px; Chinese fonts
load, no horizontal overflow, English and shared chrome retain their
typography.
- [x] Repository pre-commit lint and pre-push changed-surface
verification.
- [x] Reproduced CI's three stale `LocaleLink` expectations locally,
updated them for the now-published Chinese route, and added the reverse
English-navigation case. All 101 tests in the four directly related
files pass; query strings and anchors remain covered.

Review follow-up: the generated stylesheet contains font-face asset
registration only, with no component selectors or layout rules; all page
styling remains Tailwind. It is imported at the Events entry rather than
globally. Local asset inspection confirms the homepage includes no
Events font registrations and the Events CSS includes the expected 202
faces. The font sync check runs in the unit suite. Existing scoped
heading overrides and the intentionally omitted Chinese state
abbreviation are unchanged.

Frontend-only change. No backend or configuration migration.

---------

Co-authored-by: Yueru Wang <yueruwang@Yuerus-MacBook-Air.local>
```
