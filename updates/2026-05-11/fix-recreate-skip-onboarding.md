---
title: "修复：重建 Claw 后不再被迫走注册引导流程"
type: "Bug Fix"
priority: "高"
date: "2026-05-11"
status: "待审核"
channels: "Discord, changelog"
---

# 修复：重建 Claw 后不再被迫走注册引导流程

## 核心宣传点

老用户重建 AI 伙伴（Recreate Claw）后，不再被错误引导重新填写姓名/角色等注册信息，直接回到聊天。

## 原始内容

Commit message:
fix(web): skip onboarding entirely after recreate (#1595)

## Summary
- **Bug**: Recreate Claw 后用户被强制走 onboarding 流程（name/role 步骤），但 recreate
是老用户重建机器人，不应再走 onboarding
- **Fix**: 移除 recreate 流程中的 `ONBOARDING_RECREATE` 标志和 progress
重置逻辑，依赖现有的 `hasBoundInviteCode` 检查自然跳过 onboarding，聊天页自行处理 bot 初始化状态
- 同时还原 `resolveStatus.ts` 的 reOnboarding 分支（recreate 不再触发它），还原对应测试

Follow-up to #1587

## Test plan
- [ ] 用已完成 onboarding 的账号登录
- [ ] 进入聊天页 → 设置 → Advanced Options → Recreate Claw
- [ ] 验证 reload 后不显示任何 onboarding 步骤，直接进入聊天页
- [ ] 验证新用户首次 onboarding 流程不受影响

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

PR Description:
## Summary
- **Bug**: Recreate Claw 后用户被强制走 onboarding 流程（name/role 步骤），但 recreate 是老用户重建机器人，不应再走 onboarding
- **Fix**: 移除 recreate 流程中的 `ONBOARDING_RECREATE` 标志和 progress 重置逻辑，依赖现有的 `hasBoundInviteCode` 检查自然跳过 onboarding，聊天页自行处理 bot 初始化状态
- 同时还原 `resolveStatus.ts` 的 reOnboarding 分支（recreate 不再触发它），还原对应测试

Follow-up to #1587

## Test plan
- [ ] 用已完成 onboarding 的账号登录
- [ ] 进入聊天页 → 设置 → Advanced Options → Recreate Claw
- [ ] 验证 reload 后不显示任何 onboarding 步骤，直接进入聊天页
- [ ] 验证新用户首次 onboarding 流程不受影响

🤖 Generated with [Claude Code](https://claude.com/claude-code)
