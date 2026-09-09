---
title: "上线企业官网页 /business：十种语言、动效架构图、Book a demo 一键回到表单"
type: "产品基础功能更新"
priority: "高"
date: "2026-09-08"
status: "待审核"
channels: "站内弹窗+Use Case+Discord+changelog"
---

# 上线企业官网页 /business：十种语言、动效架构图、Book a demo 一键回到表单

## 核心宣传点

面向企业客户的落地页正式上线，地址是 `/{locale}/business`，一共支持**十种语言**：英语、中文、日语、韩语、法语、德语、意大利语、西班牙语、阿拉伯语、葡萄牙语——不只是正文，页面的元信息（SEO metadata）和架构图里的 SVG 文字标签也都做了本地化。同时首页与页脚的跳转会**保留访客当前的语言**，不会点一下就被甩回英文。

页面内容按企业采购关心的顺序铺开：平台、Agents、模型网关、数据资产、模型训练、持续学习、交付、客户案例、安全，配套一组动效 SVG 架构图，深色区块用 `#0E0522`、深底上走白色信号线。英文版首屏标题用了自托管的 GFS Didot 字体、桌面端 64px 分两行，右侧留白加大给销售表单。

体验上有个小细节值得说：底部那个 **Book a demo** 不是跳新页，而是**滚回首屏的表单**、播一小段到达高亮、并自动聚焦邮箱输入框。反复点有效，中途手动滚动会被尊重，开了「减少动效」偏好的用户不会被强行播动画。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `38e1a1c5`
- PR: #3665
- 日期: 2026-09-08

### Commit Message

```
feat(business): add multilingual enterprise page and animated contact flow (#3665)

## Summary

Add the enterprise landing page at `/{locale}/business` and preserve the
visitor’s language in homepage/footer navigation. The page supports
English, Chinese, Japanese, Korean, French, German, Italian, Spanish,
Arabic, and Portuguese, including localized metadata and SVG labels.

- Reuse the official marketing header, footer, language picker, and
login dialogs. The English hero uses a self-hosted GFS Didot heading at
64px on desktop, split into two lines, with a white background and
increased spacing beside the sales form.
- Add the platform, agents, model gateway, data assets, model training,
continuous learning, delivery, cases, and security sections. Use the
approved animated SVG diagrams, `#0E0522` dark sections, white signals
on dark backgrounds, and refined borders, labels, and responsive
layouts. SVG localization uses bundled templates compatible with
Workers.
- Make the bottom Book a demo link scroll to the first-screen form, play
a short arrival highlight, and focus email. Repeated clicks work;
interrupted scrolling and reduced-motion preferences are respected.
- Replace the copy-summary dialog with inline feedback: the form fades
out, the success icon and text appear in sequence, and the card retains
its height. Keep native validation, accessible focus handling, and the
clearly labeled example testimonial.

**Form scope:** this remains an approved frontend prototype. Submission
changes local presentation state and displays the requested
confirmation; it does not send or persist a sales lead. Connecting a
delivery API is a separate follow-up. No backend APIs or dependencies
are added. The font’s OFL license is included. The removed summary/copy
workflow has no remaining state, clipboard handlers, or dictionary
entries.

## Test plan

- [x] Targeted frontend verification: governance guards, TypeScript,
ESLint, and 59 tests across seven relevant suites passed.
- [x] All 27 SVG assets parse, and generated SVG templates match their
sources. Shared orbit geometry reduces the animated loop to 98KB, below
the 100KB limit; its timing and labels are preserved.
- [x] Browser checks covered locale switching, English/Chinese layouts,
desktop and mobile sizing, the shared header, form validation, CTA
navigation/focus, and submission transitions. Form card height stays
unchanged in the tested desktop and phone layouts.
- [x] Only enterprise-page implementation and supporting specifications
are included; independent local reference previews are excluded.
- [x] Merged current main (`4c93ca2e`) without conflicts; the resulting
PR is within the 3,000-line size budget. Full import-boundary/dead-code
CI lint and the asset-size gate pass locally.
- [x] CI checks passed on final commit `ad845130`: build,
lint/typecheck, unit tests, asset-size gate, CodeQL, and both automatic
reviews. No open code-scanning alerts or current-commit inline findings.
Human review is still required before merge.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

## 备注

发布状态：已合并待发版（尚未包含在最新的 `ecap-*-release` 前端正式发布中）。
