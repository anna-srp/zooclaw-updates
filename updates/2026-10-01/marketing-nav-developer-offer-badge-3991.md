---
title: "官网导航新增 Developer 文档入口，Pricing 加上 70% OFF 优惠角标"
type: "体验优化"
priority: "中"
date: "2026-10-01"
status: "待审核"
channels: "Discord+changelog"
---

# 官网导航新增 Developer 文档入口，Pricing 加上 70% OFF 优惠角标

## 核心宣传点

官网共享导航在 Enterprise 和 Resources 之间新增了 Developer 入口，在新标签页打开文档站。同时移除了重复的 Home 导航项（Logo 仍可回首页），并在 Pricing 右上角加了一个紧凑的红色 70% OFF 角标，颜色复用定价页的优惠配色，优惠信息在导航层就能看到。

## 分级

- 内部：P2
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary
官网共享导航新增 Developer 入口，放在 Enterprise 与 Resources 之间，在新标签页打开 https://zoowork.ai/docs/。移除重复的 Home 导航项，保留 Logo 返回首页；Pricing 右上角增加紧凑的红色 `70% OFF` 角标，复用定价页的优惠颜色。

Add a Developer link between Enterprise and Resources, opening the docs in a new tab. Remove the redundant Home item while preserving logo navigation, and show a compact red `70% OFF` badge above Pricing using the existing pricing offer color. Shared marketing pages and the mobile menu inherit these changes.

## Test plan
- [x] Rebased onto latest main; preserved the recently added navigation and mobile download behavior.
- [x] Targeted landing content, header and marketing chrome suites: 54 tests passed.
- [x] TypeScript, ESLint and repository governance checks through the pre-push gate.
- [x] Browser-checked 1440px desktop, 1103px narrow desktop and 390px mobile; verified Developer destination/new-tab attributes, logo home link and no badge overlap.
- [x] Confirmed the navigation and Pricing page offer badges render the same red color.

仅涉及官网展示，未修改价格、结算或权益逻辑。Presentation only; no pricing, checkout or entitlement logic changes.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `a5c182616b5ce2761d6f821d7bbb4f9596bbfedb`
- PR: #3991
- 作者：david-srp
- 日期：2026-10-01T15:50:05Z

### Commit Message

```
feat(marketing): 优化官网导航与优惠角标 / refine navigation and offer badge (#3991)

## Summary
官网共享导航新增 Developer 入口，放在 Enterprise 与 Resources 之间，在新标签页打开
https://zoowork.ai/docs/。移除重复的 Home 导航项，保留 Logo 返回首页；Pricing 右上角增加紧凑的红色
`70% OFF` 角标，复用定价页的优惠颜色。

Add a Developer link between Enterprise and Resources, opening the docs
in a new tab. Remove the redundant Home item while preserving logo
navigation, and show a compact red `70% OFF` badge above Pricing using
the existing pricing offer color. Shared marketing pages and the mobile
menu inherit these changes.

## Test plan
- [x] Rebased onto latest main; preserved the recently added navigation
and mobile download behavior.
- [x] Targeted landing content, header and marketing chrome suites: 54
tests passed.
- [x] TypeScript, ESLint and repository governance checks through the
pre-push gate.
- [x] Browser-checked 1440px desktop, 1103px narrow desktop and 390px
mobile; verified Developer destination/new-tab attributes, logo home
link and no badge overlap.
- [x] Confirmed the navigation and Pricing page offer badges render the
same red color.

仅涉及官网展示，未修改价格、结算或权益逻辑。Presentation only; no pricing, checkout or
entitlement logic changes.
```

来源：SerendipityOneInc/ecap-workspace @ a5c18261，PR #3991，作者 david-srp。
