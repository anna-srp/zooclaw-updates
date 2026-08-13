---
title: "修复：用户菜单里看不到订阅续费／到期日期"
type: "Bug Fix"
priority: "中"
date: "2026-08-12"
status: "待审核"
channels: ""
---

# 修复：用户菜单里看不到订阅续费／到期日期

## 核心宣传点

侧边栏用户菜单重新显示订阅的续费日期；已取消自动续费的会显示服务到期日，试用倒计时与积分余额显示保持不变。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `ec90a2adbfab9704304605c3cbb4c5609f557c0e`
- PR: #3346

### Commit Message

```
fix(billing): show subscription period in user menu (#3346)

## Summary
- Show the localized renewal date for active subscriptions in the user
menu.
- Show the period ending date when auto-renewal is canceled.
- Preserve the existing Trial countdown and actual credits balance
display.
- Avoid presenting `past_due` subscriptions as normal renewals.

## Root cause
The detailed plan card already rendered `currentPeriodEnd`, but the
compact user menu always assigned a null sub-label to active
subscriptions. This caused a real paid subscription to lose its renewal
or ending date in the sidebar even though the backend returned the
correct period boundary.

## Test plan
- [x] Verify an active subscription renders its localized renewal date.
- [x] Verify cancel-at-period-end renders an ending date.
- [x] Verify `past_due` does not render a normal renewal or ending
label.
- [x] Verify existing Trial and credits display tests remain green.
- [x] Run `bash scripts/verify-web.sh src/components/UserMenu.tsx
tests/unit/components/UserMenu.unit.spec.tsx`.
- [x] Run the pre-push changed-surface gate.
```

### PR Body

## Summary
- Show the localized renewal date for active subscriptions in the user menu.
- Show the period ending date when auto-renewal is canceled.
- Preserve the existing Trial countdown and actual credits balance display.
- Avoid presenting `past_due` subscriptions as normal renewals.

## Root cause
The detailed plan card already rendered `currentPeriodEnd`, but the compact user menu always assigned a null sub-label to active subscriptions. This caused a real paid subscription to lose its renewal or ending date in the sidebar even though the backend returned the correct period boundary.

## Test plan
- [x] Verify an active subscription renders its localized renewal date.
- [x] Verify cancel-at-period-end renders an ending date.
- [x] Verify `past_due` does not render a normal renewal or ending label.
- [x] Verify existing Trial and credits display tests remain green.
- [x] Run `bash scripts/verify-web.sh src/components/UserMenu.tsx tests/unit/components/UserMenu.unit.spec.tsx`.
- [x] Run the pre-push changed-surface gate.


---
