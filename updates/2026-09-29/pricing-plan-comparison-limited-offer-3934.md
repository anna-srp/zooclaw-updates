---
title: "定价页改版：Pro 与 Enterprise 连续对比、限时 7 折高亮，每月 6000 credits 额外赠送 14000"
type: "Improvement"
priority: "高"
date: "2026-09-29"
status: "待审核"
channels: ""
---

# 定价页改版：Pro 与 Enterprise 连续对比、限时 7 折高亮，每月 6000 credits 额外赠送 14000

## 核心宣传点

定价页的套餐对比做了一次改版：Pro 和 Enterprise 改成连续的两列，功能分组更清楚，CTA 按钮更大，英文版加了衬线体标语，10 个语种的文案全部同步更新。限时优惠和 70% 的省钱幅度用红色高亮，明确写出每月 6000 credits 加赠送 14000 credits，并配限时脚注，另外补了一行两档共用的额外 credits 说明。设置里的「管理套餐」弹窗和定价页对齐，同样显示「6k + 14k bonus credits/mo*」和每月 14000 限时赠送的脚注。原来那条「优惠不可用」的提示被移除，两个 Contact Sales 按钮统一指向企业版页面。中文文案保留 credits 作为产品词，写成「6000 credits + 赠送 14000 credits*」和「*每月额外赠送 14000 credits，限时有效。」。纯前端改动，后端、接口、数据库、计费、商品目录和 credits 发放逻辑都没有动，Pro 注册跳转保持原样，这次也不会开启带优惠的结账。

## 分级

- 内部：P0
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary
- Refresh the pricing comparison with continuous Pro and Enterprise columns, clearer feature groups, larger CTAs, and English-only serif taglines. Update copy across all 10 locales.
- Highlight the limited offer and 70% savings in red. Show 6,000 credits plus 14,000 bonus credits with a limited-time footnote, and add a shared additional-credits row.
- Align the Manage plan dialog with the pricing page: display `6k + 14k bonus credits/mo*` and a 14k limited-time monthly bonus footnote.
- Remove the unavailable-offer notice and route both Contact Sales buttons to https://zoowork.ai/enterprise.
- Frontend only: no backend, API, database, billing, catalog, or credit-issuance changes. The existing Pro sign-up handoff remains unchanged; this does not enable promotional checkout.
- Localize the Chinese monthly-credit and limited-time bonus copy, retaining `credits` as a product term: `6000 credits + 赠送 14000 credits*` and `*每月额外赠送 14000 credits，限时有效。`.
- Preserve accessible associations between each benefit cell, its feature name, and its applicable plan header(s), including the shared additional-credits row.

## Test plan
- [x] Frontend governance guards, TypeScript, and ESLint passed after syncing the latest main.
- [x] 55 initial targeted tests passed across pricing comparison, pricing typography, marketing chrome, and locale completeness; the pricing suite was rerun with a new regression test for table header associations.
- [x] Browser checks passed for all 10 locales at 1440, 1024, 390, and 320 px, with no overflow or page errors.
- [x] Verified both Contact Sales buttons navigate to the Enterprise page.
- [x] Reviewed English and Chinese desktop/mobile previews.
- [x] Credit-split follow-up: all 61 tests passed across pricing rendering, locale completeness, Manage plan dialog, and Pro plan actions. Verified old 8k/12k offer copy is absent from both frontend surfaces.
- [x] GitHub Actions on `3cb79a589`: frontend build, lint/typecheck, full tests, and CodeQL passed; both automated reviewers reported no new issues.

## Review follow-up
- Fixed the screen-reader row-header association regression and added coverage.
- Localized the Chinese bonus message and footnote while preserving `credits`; updated the rendering and accessible-description assertions for each language. Unused `scrollHint` translation keys remain as a harmless cleanup item with no runtime effect. Manage plan keeps its existing English presentation; broader dialog localization is a pre-existing follow-up, outside this display-number correction.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `d01352eb67f819067c7ffcc8c9b4287a254dafbf`
- PR: #3934
- 作者：ericma-srp
- 日期：2026-09-29T14:19:17Z

### Commit Message

```
feat(pricing): refresh plan comparison and limited offer messaging (#3934)

## Summary
- Refresh the pricing comparison with continuous Pro and Enterprise
columns, clearer feature groups, larger CTAs, and English-only serif
taglines. Update copy across all 10 locales.
- Highlight the limited offer and 70% savings in red. Show 6,000 credits
plus 14,000 bonus credits with a limited-time footnote, and add a shared
additional-credits row.
- Align the Manage plan dialog with the pricing page: display `6k + 14k
bonus credits/mo*` and a 14k limited-time monthly bonus footnote.
- Remove the unavailable-offer notice and route both Contact Sales
buttons to https://zoowork.ai/enterprise.
- Frontend only: no backend, API, database, billing, catalog, or
credit-issuance changes. The existing Pro sign-up handoff remains
unchanged; this does not enable promotional checkout.
- Localize the Chinese monthly-credit and limited-time bonus copy,
retaining `credits` as a product term: `6000 credits + 赠送 14000
credits*` and `*每月额外赠送 14000 credits，限时有效。`.
- Preserve accessible associations between each benefit cell, its
feature name, and its applicable plan header(s), including the shared
additional-credits row.

## Test plan
- [x] Frontend governance guards, TypeScript, and ESLint passed after
syncing the latest main.
- [x] 55 initial targeted tests passed across pricing comparison,
pricing typography, marketing chrome, and locale completeness; the
pricing suite was rerun with a new regression test for table header
associations.
- [x] Browser checks passed for all 10 locales at 1440, 1024, 390, and
320 px, with no overflow or page errors.
- [x] Verified both Contact Sales buttons navigate to the Enterprise
page.
- [x] Reviewed English and Chinese desktop/mobile previews.
- [x] Credit-split follow-up: all 61 tests passed across pricing
rendering, locale completeness, Manage plan dialog, and Pro plan
actions. Verified old 8k/12k offer copy is absent from both frontend
surfaces.
- [x] GitHub Actions on `3cb79a589`: frontend build, lint/typecheck,
full tests, and CodeQL passed; both automated reviewers reported no new
issues.

## Review follow-up
- Fixed the screen-reader row-header association regression and added
coverage.
- Localized the Chinese bonus message and footnote while preserving
`credits`; updated the rendering and accessible-description assertions
for each language. Unused `scrollHint` translation keys remain as a
harmless cleanup item with no runtime effect. Manage plan keeps its
existing English presentation; broader dialog localization is a
pre-existing follow-up, outside this display-number correction.
```

来源：SerendipityOneInc/ecap-workspace @ d01352eb，PR #3934，作者 ericma-srp。
