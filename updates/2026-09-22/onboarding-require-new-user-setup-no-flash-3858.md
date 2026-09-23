---
title: "修复：新用户须先完成欢迎引导再进入 Agents，老用户刷新不再闪现引导页"
type: "Bug Fix"
priority: "高"
date: "2026-09-22"
status: "待审核"
channels: ""
---

# 修复：新用户须先完成欢迎引导再进入 Agents，老用户刷新不再闪现引导页

## 核心宣传点

新注册的账号现在必须走完「欢迎 → 能力介绍 → 选套餐」这套新引导，完成状态会被持久化，走完自动跳到本地化的 Agents 页去创建第一个 Agent。流程里那些过时的步骤（填名字、选 Specialist、设提醒、挑渠道、以及中间的加载页）都被拿掉了，结账行为保持原样，保存完成状态失败时允许重试。顺带修掉了一个很招人烦的老问题：以前已登录的老用户每次全局刷新，都会在认证和账号状态加载完之前先闪一下引导欢迎屏。根因是引导的解析器被停用了、账号同步又把后端的完成标记丢掉了，同时弹窗在私有路由上默认是打开状态、状态还在 pending 时又会重新打开。

## 分级

- 内部：P0
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary
- Require new accounts to finish the new welcome → capabilities → plan
flow, persist completion, then navigate to the localized Agents page to
create their first Agent.
- Remove the obsolete name, Specialist, reminder, channel, and loading
steps from the active flow. Keep existing checkout behavior and allow
retry when saving completion fails.
- Fix the global refresh flash: returning users no longer briefly see
the onboarding welcome screen while auth and account status load.

## Root cause
The onboarding resolver was disabled, and account sync discarded the
backend completion flag. The modal also started open on private routes
and reopened while status was pending, so returning users saw the
welcome screen before it closed.

Account sync now preserves completion status, explicit
backend-incomplete accounts must finish onboarding, and automatic modal
opening waits for a settled required result. Required onboarding cannot
be dismissed with Escape. Completed and legacy active accounts retain
their existing path.

## Completion contract
Onboarding completion records the three-screen introduction; it does not
grant a paid subscription or credits. The existing [Stripe integration
contract](https://github.com/SerendipityOneInc/ecap-workspace/blob/main/docs/superpowers/specs/2026-09-17-billing-ui-pr-integration.md#resolved-overlaps)
continues after the checkout popup successfully navigates. This PR
preserves that behavior rather than introducing a new payment gate.

After saving completion, `markOnboardingCompletedLocally()` calls
`_dispatchBackendStatus()` with `onboardingCompleted: true`, updating
the shared Zustand status store before navigation. Existing auth-manager
tests verify the snapshot update; browser checks verify that the
persistent provider does not reopen onboarding after completion.

## Test plan
- [x] Focused onboarding, account/auth and local mock scenario tests;
final refresh regression run: 112 tests passed.
- [x] TypeScript, changed-file ESLint, frontend governance guards,
import boundaries and hard-gate dead-code checks passed.
- [x] Local mock browser walkthrough: welcome → capabilities → plan →
Agents → Create Agent dialog; completion persists after reload. Checkout
was simulated; no real payment was made.
- [x] Reproduced the refresh flash before the fix with a delayed account
response. Verified every DOM insertion during initial load and refresh
across Home, Agents, Artifacts, Tasks, Connector, MCP, Skills and
Knowledge; onboarding never mounted for the completed account.
- [x] Synced the branch with latest main before submission.

Frontend-only change; no backend deployment or API migration required.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `6f73028cb88e9f1527a914296983af47688598e3`
- PR: #3858
- 作者：shana-srp
- 日期：2026-09-22T09:12:02Z

### Commit Message

```
fix(onboarding): require new-user setup before Agents without refresh flash (#3858)

## Summary
- Require new accounts to finish the new welcome → capabilities → plan
flow, persist completion, then navigate to the localized Agents page to
create their first Agent.
- Remove the obsolete name, Specialist, reminder, channel, and loading
steps from the active flow. Keep existing checkout behavior and allow
retry when saving completion fails.
- Fix the global refresh flash: returning users no longer briefly see
the onboarding welcome screen while auth and account status load.

## Root cause
The onboarding resolver was disabled, and account sync discarded the
backend completion flag. The modal also started open on private routes
and reopened while status was pending, so returning users saw the
welcome screen before it closed.

Account sync now preserves completion status, explicit
backend-incomplete accounts must finish onboarding, and automatic modal
opening waits for a settled required result. Required onboarding cannot
be dismissed with Escape. Completed and legacy active accounts retain
their existing path.

## Completion contract
Onboarding completion records the three-screen introduction; it does not
grant a paid subscription or credits. The existing [Stripe integration
contract](https://github.com/SerendipityOneInc/ecap-workspace/blob/main/docs/superpowers/specs/2026-09-17-billing-ui-pr-integration.md#resolved-overlaps)
continues after the checkout popup successfully navigates. This PR
preserves that behavior rather than introducing a new payment gate.

After saving completion, `markOnboardingCompletedLocally()` calls
`_dispatchBackendStatus()` with `onboardingCompleted: true`, updating
the shared Zustand status store before navigation. Existing auth-manager
tests verify the snapshot update; browser checks verify that the
persistent provider does not reopen onboarding after completion.

## Test plan
- [x] Focused onboarding, account/auth and local mock scenario tests;
final refresh regression run: 112 tests passed.
- [x] TypeScript, changed-file ESLint, frontend governance guards,
import boundaries and hard-gate dead-code checks passed.
- [x] Local mock browser walkthrough: welcome → capabilities → plan →
Agents → Create Agent dialog; completion persists after reload. Checkout
was simulated; no real payment was made.
- [x] Reproduced the refresh flash before the fix with a delayed account
response. Verified every DOM insertion during initial load and refresh
across Home, Agents, Artifacts, Tasks, Connector, MCP, Skills and
Knowledge; onboarding never mounted for the completed account.
- [x] Synced the branch with latest main before submission.

Frontend-only change; no backend deployment or API migration required.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

来源：SerendipityOneInc/ecap-workspace @ 6f73028c，PR #3858，作者 shana-srp。
