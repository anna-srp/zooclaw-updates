---
title: "fix(billing): remove credit expiration promises from UI copy (#3836)"
type: "体验优化"
priority: "中"
date: "2026-09-21"
status: "待审核"
channels: ""
---

# 计费文案去掉关于积分有效期的承诺

## 核心宣传点

计费界面里关于积分有效期的表述做了清理，避免和实际规则打架。账号卡片现在只说明充值积分可以在没有订阅的情况下使用，10 种语言全部同步；购买成功页去掉了「永不过期」那条以及相关翻译键，老版 Stripe 购买组件里同类说法也一并移除。About Credits 里互相矛盾的「一年有效」和「过期积分可恢复」措辞也清理掉了，月订阅积分按期重置的说明保留。钱包过期逻辑、积分发放和所有支付行为本身都没有改动——这次只改文案。

## 分级

- 内部：P2
- 外部：B
- 发布状态：已上线

## PR 说明

Remove credit-expiration promises from billing UI copy. Account cards now only explain that top-up credits can be used without a subscription, across all 10 supported locales. Remove the no-expiration bullet and translation keys from the purchase success page, and remove the equivalent claim in the older Stripe purchase component.

Clean up the contradictory one-year validity and expired-credit restoration wording in About Credits. Monthly subscription credit reset wording remains. Wallet expiration, credit grants, and all payment behavior are unchanged.

Validation: existing billing card, Stripe purchase and purchase-success tests; TypeScript, ESLint and repository frontend checks. Not deployed.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `9901b22e4609fb1fac17bd8880426389d86b22a6`
- PR: #3836
- 作者：sam-srp
- 日期：2026-09-21T06:31:49Z

### Commit Message

```
fix(billing): remove credit expiration promises from UI copy (#3836)

Remove credit-expiration promises from billing UI copy. Account cards
now only explain that top-up credits can be used without a subscription,
across all 10 supported locales. Remove the no-expiration bullet and
translation keys from the purchase success page, and remove the
equivalent claim in the older Stripe purchase component.

Clean up the contradictory one-year validity and expired-credit
restoration wording in About Credits. Monthly subscription credit reset
wording remains. Wallet expiration, credit grants, and all payment
behavior are unchanged.

Validation: existing billing card, Stripe purchase and purchase-success
tests; TypeScript, ESLint and repository frontend checks. Not deployed.
```

来源：SerendipityOneInc/ecap-workspace @ 9901b22e，PR #3836，作者 sam-srp。