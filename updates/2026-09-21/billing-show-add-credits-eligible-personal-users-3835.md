---
title: "fix(billing): show Add Credits for all eligible personal users (#3835)"
type: "Bug Fix"
priority: "高"
date: "2026-09-21"
status: "待审核"
channels: ""
---

# 修复：订阅过期的个人账号看不到「充值积分」

## 核心宣传点

积分本来就支持不订阅单独买，但订阅已过期的个人账号在计费卡片上只能看到「激活」按钮，根本找不到充值入口。现在「充值积分」的显示不再跟订阅状态绑定，只按既有的个人计费资格判断。Team 用户保持现有的只有 Manage 的行为，加载和错误状态的保护逻辑也没变。没有后端、配置或支付处理层的改动。

## 分级

- 内部：P1
- 外部：A
- 发布状态：已上线

## PR 说明

Personal accounts whose subscriptions expired only saw Activate and could not find Add Credits, despite top-ups being available without a subscription. Render Add Credits independently of subscription display status, using the existing personal-billing eligibility check. Team users keep their current Manage-only actions, and loading/error states remain guarded.

Validation: 36 SharedPlanCard component tests pass, covering personal subscription states, Team restrictions, and unresolved billing eligibility. No backend, configuration, or payment-processing changes. Not deployed.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `bb0c9cc85fa3177cb6ec5b02daa4f2e59300cefb`
- PR: #3835
- 作者：sam-srp
- 日期：2026-09-21T05:58:25Z

### Commit Message

```
fix(billing): show Add Credits for all eligible personal users (#3835)

Personal accounts whose subscriptions expired only saw Activate and
could not find Add Credits, despite top-ups being available without a
subscription. Render Add Credits independently of subscription display
status, using the existing personal-billing eligibility check. Team
users keep their current Manage-only actions, and loading/error states
remain guarded.

Validation: 36 SharedPlanCard component tests pass, covering personal
subscription states, Team restrictions, and unresolved billing
eligibility. No backend, configuration, or payment-processing changes.
Not deployed.
```

来源：SerendipityOneInc/ecap-workspace @ bb0c9cc8，PR #3835，作者 sam-srp。