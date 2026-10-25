---
title: "官网首页首屏按设计稿重排，页脚社交链接换成官方账号"
type: "体验优化"
priority: "中"
date: "2026-10-16"
status: "待审核"
channels: ""
---

# 官网首页首屏按设计稿重排，页脚社交链接换成官方账号

## 核心宣传点

官网首页首屏按 Figma 设计稿重新排版：顶部留白加大，大标题移到描述文案和行动按钮旁边，产品截图加上连续的白色描边；首屏的 Product Hunt 徽章移除，页脚徽章保留。原有的浅色背景图和静态背景裁切保持不变，宽屏下限制插画高度让截图底部保持裁切效果，760px 以下的手机和小平板则完整显示截图，保留完整底边和内外圆角，响应式布局与 CTA 行为均不变。页脚社交链接更新为 ZooWork 官方 X、YouTube 和 Product Hunt 主页，其中 Product Hunt 产品页地址与获奖徽章地址分开管理。

## 分级

- 内部：P2
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `15024b1669afff68ef5aecdba43df9b78b26c6a5`
- PR: #4038
- 作者：shana-srp
- 日期：2026-10-16T04:14:11Z

### Commit Message

```
fix(landing): align homepage hero and update social links (#4038)

## Summary
Align the homepage hero with the supplied Figma layout: increase top
spacing, position the headline beside the description and CTA buttons,
and frame the product screenshot with a continuous white border. Remove
the hero Product Hunt badge; the footer badge remains.

Keep the original light background image and static background crop.
Bound the artwork height on wide screens so the screenshot remains
cropped at the bottom. On phones and small tablets below 760px, keep the
full screenshot visible with a complete bottom border and rounded inner
and outer corners. Preserve responsive layouts and existing CTA
behavior.

Update the footer social links to the official ZooWork X, YouTube, and
Product Hunt profiles. Manage the Product Hunt product-page URL
separately from the awards badge URL.

Design:
https://www.figma.com/design/IgzHI9jcrXpME6PVaZJRJs/zoowork?node-id=1198-3992

## Validation
- Web governance guards, full TypeScript checking, changed-file ESLint,
and `git diff --check` passed after syncing the branch with current
main.
- All 9 landing-page Playwright scenarios passed against the local mock
preview.
- The mobile regression verifies complete bottom borders and rounded
inner/outer corners at 320, 375, 640, and 759px, with no horizontal
overflow. It reproduced the original zero-radius bottom edge before the
fix.
- The desktop crop regression passes at 761, 1024, 1505, 2048, 2560, and
3440px. Together with the 759px mobile case, this covers both sides of
the mobile breakpoint and the previously reported ultrawide sizes.
- Visually checked the actual hero at 320, 640, and 1505px; the original
light background and completed mobile frame render correctly.
- The standard local unit-test run remains affected by duplicate React
installations in the reused dependency setup. Unit tests are not
reported as passing locally; CI remains the clean-environment gate.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

