---
title: "iOS 新用户引导流程全面改版"
type: "产品基础功能更新"
priority: "中"
date: "2026-04-30"
status: "待审核"
channels: ""
---
# iOS 新用户引导流程全面改版

## 核心宣传点
全新设计的 iOS 注册引导流程，视觉更现代、步骤更清晰，帮助新用户快速完成角色选择和使用场景设置，开启专属 AI 体验。

## 原始内容
**Commit A**: feat(ios): Pre-auth onboarding redesign with role + use-case screens (#1458)
**Commit B**: feat(ios): Post-auth onboarding view redesigns (PR-B of 2) (#1467)
**Date**: 2026-04-29

```
feat(ios): Pre-auth onboarding redesign with role + use-case screens (#1458)

PR-A of 2. Builds on the infrastructure landed in #1452 and ships the
redesigned pre-auth flow: hero → name → role → use case → register.

feat(ios): Post-auth onboarding view redesigns (PR-B of 2) (#1467)

PR-B of 2. Ships the Figma redesigns of the four post-auth views.
After this PR lands, the visual onboarding refresh is feature-complete:
hero → name → role → useCase → register → OTP → agentSelect → notifications
```

**PR #1458 Summary**: Builds on onboarding infrastructure and ships redesigned pre-auth flow including hero screen, name entry, role selection, and use-case screens. Extracted from #1450 to fit PR size budget.

**PR #1467 Summary**: Ships the Figma redesigns of all four post-auth views. Completes the visual onboarding refresh end-to-end.
