---
title: "修复：切换 Agent 模型时聊天和输入框不再被清空，未发送的草稿也能保留"
type: "Bug Fix"
priority: "中"
date: "2026-09-27"
status: "待审核"
channels: ""
---

# 修复：切换 Agent 模型时聊天和输入框不再被清空，未发送的草稿也能保留

## 核心宣传点

以前改 Agent 模型会让整棵定义树失效、工作版本短暂消失，导致聊天区和输入框被卸载重建，正在打的内容也没了。现在保存设置会直接复用返回的新版本，只刷新设置相关的元数据；同工作区的版本切换期间保留上一份快照（此时设置控件置灰），即使轮询先看到新版本也一样。实测把保存响应延迟 5 秒、从 Claude Sonnet 4.6 切到 GPT 5.4，输入框和未发送草稿都还在，URL 不变。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

Changing an Agent model invalidated the entire definition subtree and briefly removed the working revision, unmounting the chat and composer. Settings saves now seed the returned revision and refresh only settings metadata. Same-workspace revision transitions retain the previous snapshot with settings controls disabled, including when polling sees the new revision before the save response.

Validation:
- Targeted Vitest run: 112 tests passed, including delayed revision, save success/failure, cache invalidation, and account/workspace isolation.
- TypeScript, ESLint, governance guards and pre-push checks passed.
- Playwright against the local mock: delayed the save response by five seconds, switched from Claude Sonnet 4.6 to GPT 5.4, and verified the same composer DOM node and unsent draft survived, the URL did not change, and no conversation-binding request ran.

Frontend-only deployment. Task titles and credits are separate work.

Review follow-up: added a real QueryClient test for a terminal revision-read failure. The installed TanStack Query clears placeholder data on error (`isPlaceholderData: false`) and recovers on refetch, so the reported indefinite-placeholder failure did not reproduce. Added a guard/test for late save responses after workspace navigation. Updated avatar and legacy-workspace regression fixtures to follow the actual authenticated, immutable-revision contract; the final focused run passed 19 tests.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `52d3aa94b583e6a8ce42d188edb7427ae827efe0`
- PR: #3905
- 作者：Nemo Feng
- 日期：2026-09-27T02:54:47Z

### Commit Message

```
fix(agents): preserve chat while switching models (#3905)

Changing an Agent model invalidated the entire definition subtree and
briefly removed the working revision, unmounting the chat and composer.
Settings saves now seed the returned revision and refresh only settings
metadata. Same-workspace revision transitions retain the previous
snapshot with settings controls disabled, including when polling sees
the new revision before the save response.

Validation:
- Targeted Vitest run: 112 tests passed, including delayed revision,
save success/failure, cache invalidation, and account/workspace
isolation.
- TypeScript, ESLint, governance guards and pre-push checks passed.
- Playwright against the local mock: delayed the save response by five
seconds, switched from Claude Sonnet 4.6 to GPT 5.4, and verified the
same composer DOM node and unsent draft survived, the URL did not
change, and no conversation-binding request ran.

Frontend-only deployment. Task titles and credits are separate work.

Review follow-up: added a real QueryClient test for a terminal
revision-read failure. The installed TanStack Query clears placeholder
data on error (`isPlaceholderData: false`) and recovers on refetch, so
the reported indefinite-placeholder failure did not reproduce. Added a
guard/test for late save responses after workspace navigation. Updated
avatar and legacy-workspace regression fixtures to follow the actual
authenticated, immutable-revision contract; the final focused run passed
19 tests.
```

来源：SerendipityOneInc/ecap-workspace @ 52d3aa94，PR #3905，作者 Nemo Feng。