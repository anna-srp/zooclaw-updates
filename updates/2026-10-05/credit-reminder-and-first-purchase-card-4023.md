---
title: "优化：充值到账期间不再重复提醒余额不足，首充卡片按钮样式统一"
type: "体验优化"
priority: "高"
date: "2026-10-05"
status: "待审核"
channels: ""
---

# 优化：充值到账期间不再重复提醒余额不足，首充卡片按钮样式统一

## 核心宣传点

修正了侧边栏充值提醒的时机。此前支付已确认、额度还在入账的几十秒内，侧边栏仍会按「余额为零」提示你再买一次，容易造成重复充值。现在本金正在发放或赠金待入账时，会隐藏这条普通的零余额提醒，但「充值」入口依旧保留，随时可点。首充赠金卡片的按钮也统一成与「前往账单」一致的黑白默认样式，两张侧边栏卡片保持互斥，不会同时出现。入账期间页面每 3 秒刷新一次到账状态，最多持续 3 分钟，之后降频到 5 分钟一次，读取失败同样降频，发放完成即停止轮询，重新发起充值会重新开启观察窗口。界面文案与状态没有新增，用户只会感觉到提示更准了。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## 备注

赠金相关开关此次在 Staging 环境开启，正式环境放量时间需与运营确认。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `bf8d0b79112d8b6c385c55004dc928ef7e653a52`
- PR: #4023
- 作者：ericma-srp
- 日期：2026-10-05T02:39:06Z

### Commit Message

```
fix(platform): refine credit reminders and enable staging bonus (#4023)

The sidebar could prompt a second purchase while a confirmed payment was
still posting credits. Hide the ordinary zero-balance reminder during
principal delivery or a pending bonus, keep the normal Add funds link
available, and use the same default black/white Button for the
first-purchase card as Go to Billing. The two sidebar cards remain
mutually exclusive; no new customer-facing state or copy.

The existing billing response adds hasPendingTopup from an
Organization/environment-scoped existence read with a matching compound
index, covering all history pages. Read delivery state before balance.
The shell refreshes normal delivery every 3 seconds for at most 3
minutes, then backs off to every 5 minutes; failed reads also back off.
Unchanged responses and page remounts do not renew the window.
Completion stops principal polling, and an explicit new purchase gets a
fresh window. Payment, eligibility and credit mutations are unchanged.

The product owner explicitly requested staging activation after the
deployed eric account returned firstTopupBonus: null. Enable
PLATFORM_FIRST_TOPUP_BONUS_ENABLED only in the staging deployment
overlay; base defaults and production/dev overlays remain unchanged.
Platform sandbox Checkout already rejects live Stripe keys. This is a
follow-up to merged #4018.

Validation: 244 Platform tests, including normal completion,
unchanged/error backoff across remounts, delayed completion, and a fresh
purchase during an older pending delivery; Platform lint/build. Earlier
checks for the unchanged backend/UI: 74 targeted
backend/query/deployment tests, Python static/import checks and commit
hooks, and desktop browser verification of matching black/white buttons,
mutually exclusive cards, and hidden zero-balance reminder while credits
settle.

Deployment verification remains distinct from local checks. This host
has no authenticated Kubernetes context; actual CSFLE execution,
historical payment facts, and Stripe Sandbox → Lago credit delivery are
not claimed as tested. After normal review/merge and staging deployment,
verify the live billing response and eligible card. Production
activation is outside this PR.
```

