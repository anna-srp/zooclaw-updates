---
title: "Bossclaw 权益展示文案从「Token」改为「credit（额度）」"
type: "体验优化"
priority: "低"
date: "2026-06-22"
status: "待审核"
channels: "Discord + changelog"
---
# Bossclaw 权益展示文案从「Token」改为「credit（额度）」
## 核心宣传点
Bossclaw 兑换页展示的权益单位文案从「Token」调整为「credit（额度）」，措辞更贴近用户对额度的直观理解，避免与技术术语 token 混淆。
## 原始内容
hotfix(bossclaw): sync benefit copy to main (#2549)

## Summary

- Forward-sync #2542's BossClaw benefit copy fix to main.
- Change displayed benefit from ` Token` to ` credit`.
- Update the focused RedeemStep unit test assertion.

## Scope

Display copy and test assertion only. No API, backend, binding, login, install, polling, or wizard-state logic changed.

## Testing

- `bash scripts/verify-web.sh 'src/app/[locale]/bossclaw'`
