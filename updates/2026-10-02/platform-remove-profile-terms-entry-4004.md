---
title: "修复：开发者平台个人设置页去掉 Terms 入口，登录页与充值弹窗的条款链接保持不变"
type: "Bug Fix"
priority: "低"
date: "2026-10-02"
status: "待审核"
channels: ""
---

# 修复：开发者平台个人设置页去掉 Terms 入口，登录页与充值弹窗的条款链接保持不变

## 核心宣传点

开发者平台 /settings/profile 页面底部的 Terms 链接和那条分隔线按产品负责人要求移除了，个人设置页现在只剩账号和外观两组设置。登录页、充值弹窗里的 API Credit Terms 链接以及随附协议都没有变化，想查条款仍然可以从这两处打开。原因是此前条款页上线时顺手在个人设置里加了入口，10 月 2 日的产品决定是撤掉它。

## 分级

- 内部：P2
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary
Remove the Terms footer and its divider from Platform's
`/settings/profile` page, as requested by the product owner. The login
and credit-purchase Terms links and the supplied agreement remain
unchanged.

## Root cause
The earlier terms rollout added a Profile entry. The owner's October 2
follow-up removes that entry; the product rule and existing Profile
assertion now reflect this decision.

## Test plan
- [x] Platform lint and production build, including TypeScript checks.
- [x] All 53 router tests passed, including the updated Profile
assertion and existing public Terms / purchase-entry coverage.
- [x] Local browser preview: Profile renders account and appearance
settings with zero Terms links. Uses sample data; no live account or
payment changes.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `98c4bd443f7edfc5a0c5a7b1636a4a7383082a6b`
- PR: #4004
- 作者：ericma-srp
- 日期：2026-10-02T14:28:13Z

### Commit Message

```
fix(platform): remove terms entry from profile settings (#4004)

## Summary
Remove the Terms footer and its divider from Platform's
`/settings/profile` page, as requested by the product owner. The login
and credit-purchase Terms links and the supplied agreement remain
unchanged.

## Root cause
The earlier terms rollout added a Profile entry. The owner's October 2
follow-up removes that entry; the product rule and existing Profile
assertion now reflect this decision.

## Test plan
- [x] Platform lint and production build, including TypeScript checks.
- [x] All 53 router tests passed, including the updated Profile
assertion and existing public Terms / purchase-entry coverage.
- [x] Local browser preview: Profile renders account and appearance
settings with zero Terms links. Uses sample data; no live account or
payment changes.
```

来源：SerendipityOneInc/ecap-workspace @ 98c4bd44，PR #4004，作者 ericma-srp。
