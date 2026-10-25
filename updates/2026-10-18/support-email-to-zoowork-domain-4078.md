---
title: "全站客服邮箱统一改为 support@zoowork.ai"
type: "体验优化"
priority: "低"
date: "2026-10-18"
status: "待审核"
channels: ""
---

# 全站客服邮箱统一改为 support@zoowork.ai

## 核心宣传点

把全站对外展示的客服邮箱从 support@zooclaw.ai 换成 support@zoowork.ai，团队已确认这是正式的客服信箱，2026-10-14 的测试邮件已成功进入工单系统。覆盖 26 个文件的邮箱字符串：隐私政策、服务条款、退款、DMCA、短信隐私等法务页面，首页 7 天试点的 mailto 与页脚联系方式，SEO 结构化数据里的 supportEmail，以及工单弹窗、地区访问受限弹窗、套餐摘要、旧版 Agent 下线提示等应用内入口，6 个单测同步更新。zooclaw.ai 的域名与链接、统计代码均未改动。

## 分级

- 内部：P3
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## 备注

BossClaw 注册报错里的 marketing@zooclaw.ai 属于另一个信箱，本次未动，需单独决策；联系页当前仍被 CONTACT_PAGE_ENABLED = false 关闭。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `90e1c2b85aebbca18b1108181f0689ab944ff632`
- PR: #4078
- 作者：Mori-srp
- 日期：2026-10-18T09:21:37Z

### Commit Message

```
fix(site): use support@zoowork.ai as the support email (#4078)

## What
Replace the user-facing support address `support@zooclaw.ai` with
`support@zoowork.ai` across the site (team confirmed support@zoowork.ai
is the support mailbox; a test email landed in the support ticket system
on 2026-10-14).

## Where (26 files, email string only)
- Legal: privacy, terms, refund, DMCA, SMS privacy / terms / opt-in
(both `about/` and `[locale]` versions)
- Homepage: 7-Day Pilot mailto and footer Contact
- Contact page `SALES_EMAIL` (page currently disabled via
`CONTACT_PAGE_ENABLED = false`)
- `_seo.ts` supportEmail (structured data)
- In-app: SupportTicketModal, DomesticAccessRestrictedDialog,
PlanSummary, LegacyAgentSunsetNotice
- 6 unit tests updated to expect the new address

## Not changed
- No zooclaw.ai URLs/domains, no analytics code
- `marketing@zooclaw.ai` in BossClaw sign-up error
(`lib/auth/manager.ts`) left as is; a different mailbox, needs a
separate decision
- Internal spec doc and mock/placeholder addresses

## Checks
- Affected unit tests pass (149), `tsc --noEmit` and eslint on changed
files pass
- Local screenshots of privacy / terms / sms-terms / DMCA show the new
address; homepage HTML contains only `mailto:support@zoowork.ai` links
```

