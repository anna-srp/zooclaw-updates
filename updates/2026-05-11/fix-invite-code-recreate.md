---
title: "修复：重建 Claw 后邀请码状态正确保留"
type: "Bug Fix"
priority: "中"
date: "2026-05-11"
status: "待审核"
channels: ""
---

# 修复：重建 Claw 后邀请码状态正确保留

## 核心宣传点

老用户重建 AI 伙伴后，不再被要求重新输入邀请码，邀请码完成状态正确保留。

## 原始内容

Commit message:
fix(web): preserve inviteCodeCompleted during recreate re-onboarding (#1587)

## Summary
- **Bug**: Recreate Claw 后用户被错误导航到 invite code 输入页面，即使已经绑定过 invite code
- **Root cause**: `resolveOnboardingStatus()` 在 `reOnboarding=true` 时返回
`DEFAULT_PROGRESS`（所有字段 false），丢弃了 localStorage 中保留的
`inviteCodeCompleted=true`
- **Fix**: re-onboarding 时从 `localProgress` 继承
`inviteCodeCompleted`，其他字段仍重置为 false

## Test plan
- [ ] 用已完成 onboarding 的账号登录
- [ ] 进入聊天页 → 设置 → Advanced Options → Recreate Claw
- [ ] 验证 reload 后直接跳到 name 步骤，不再显示 invite code 页面
- [ ] 验证新用户首次 onboarding 流程不受影响（invite code 步骤正常显示）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

PR Description:
## Summary
- **Bug**: Recreate Claw 后用户被错误导航到 onboarding 流程（invite code / name 步骤），即使是已完成过 onboarding 的老用户
- **Root cause**: recreate handler 设置了 `ONBOARDING_RECREATE` 标志强制触发 re-onboarding，但 recreate 是老用户重建机器人，不应走 onboarding
- **Fix**: 移除 recreate 流程中的 re-onboarding 触发逻辑，依赖现有的 `hasBoundInviteCode` 检查自然跳过 onboarding

## Test plan
- [ ] 用已完成 onboarding 的账号登录
- [ ] 进入聊天页 → 设置 → Advanced Options → Recreate Claw
- [ ] 验证 reload 后不显示任何 onboarding 步骤，直接进入聊天页（bot 初始化由聊天页自己处理）
- [ ] 验证新用户首次 onboarding 流程不受影响

🤖 Generated with [Claude Code](https://claude.com/claude-code)
