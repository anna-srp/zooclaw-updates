---
title: "首页产品卡片补上明确的 CTA 与 hover 反馈，不再像静态介绍"
type: "体验优化"
priority: "中"
date: "2026-10-01"
status: "待审核"
channels: ""
---

# 首页产品卡片补上明确的 CTA 与 hover 反馈，不再像静态介绍

## 核心宣传点

首页的产品卡片虽然可以点，但看起来像纯静态介绍，访客意识不到那是入口。现在每张卡片都加了常驻的、按产品定制的 CTA 文案，并补上更清晰的 hover 和 focus 反馈，四个产品入口更容易被识别和点击。

## 分级

- 内部：P2
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary / 改动说明

The homepage product cards looked like static descriptions despite being clickable. Add always-visible, product-specific CTAs and clearer hover/focus feedback so visitors can recognize the four entry points and their next actions.

首页四个产品入口原本容易被误认为静态介绍。本次增加常显 CTA 和清晰的悬停、键盘焦点反馈，让用户直观看出入口可点击。

- Redraw all four product diagrams as consistent SVG illustrations using the homepage palette; preserve static/reduced-motion variants and visibility-based animation.
- Replace the section headline, subtitle, and product descriptions with the approved copy, and synchronize all ten homepage language dictionaries.
- Keep existing link destinations, new-tab behavior, and login locale handling. Align desktop CTAs and adapt icon/text spacing for narrow screens.

统一四组 SVG 的轮廓和品牌配色，更新中英文及其他语言文案，并优化桌面 CTA 对齐与手机布局。链接目标、新标签页行为及登录语言传递保持原样。

## Test plan / 验证

- [x] TypeScript type-check and repository frontend governance checks.
- [x] ESLint and formatting checks; pre-commit and pre-push gates.
- [x] Homepage rendering and localization tests: 95 tests across two suites.
- [x] Browser validation at 320, 390, 768, 1024, and 1440px: loaded SVGs, complete text, no horizontal overflow, aligned desktop CTAs.
- [x] English and Chinese screenshots reviewed locally; keyboard focus and reduced-motion behavior verified.

Frontend-only change. No production deployment is included.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `2cb678187cdab2b87cebd1aa17ce361cc9a74bce`
- PR: #3990
- 作者：david-srp
- 日期：2026-10-01T15:14:53Z

### Commit Message

```
style(landing): 优化首页产品入口 / refine homepage product navigation (#3990)

## Summary / 改动说明

The homepage product cards looked like static descriptions despite being
clickable. Add always-visible, product-specific CTAs and clearer
hover/focus feedback so visitors can recognize the four entry points and
their next actions.

首页四个产品入口原本容易被误认为静态介绍。本次增加常显 CTA 和清晰的悬停、键盘焦点反馈，让用户直观看出入口可点击。

- Redraw all four product diagrams as consistent SVG illustrations using
the homepage palette; preserve static/reduced-motion variants and
visibility-based animation.
- Replace the section headline, subtitle, and product descriptions with
the approved copy, and synchronize all ten homepage language
dictionaries.
- Keep existing link destinations, new-tab behavior, and login locale
handling. Align desktop CTAs and adapt icon/text spacing for narrow
screens.

统一四组 SVG 的轮廓和品牌配色，更新中英文及其他语言文案，并优化桌面 CTA 对齐与手机布局。链接目标、新标签页行为及登录语言传递保持原样。

## Test plan / 验证

- [x] TypeScript type-check and repository frontend governance checks.
- [x] ESLint and formatting checks; pre-commit and pre-push gates.
- [x] Homepage rendering and localization tests: 95 tests across two
suites.
- [x] Browser validation at 320, 390, 768, 1024, and 1440px: loaded
SVGs, complete text, no horizontal overflow, aligned desktop CTAs.
- [x] English and Chinese screenshots reviewed locally; keyboard focus
and reduced-motion behavior verified.

Frontend-only change. No production deployment is included.
```

来源：SerendipityOneInc/ecap-workspace @ 2cb67818，PR #3990，作者 david-srp。
