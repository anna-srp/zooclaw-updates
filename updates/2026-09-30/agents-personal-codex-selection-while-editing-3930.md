---
title: "编辑 Agent 时也能选个人 Codex 订阅模型了，和新建任务保持一致"
type: "Improvement"
priority: "中"
date: "2026-09-30"
status: "待审核"
channels: ""
---

# 编辑 Agent 时也能选个人 Codex 订阅模型了，和新建任务保持一致

## 核心宣传点

编辑 Agent 现在提供和「新建任务」一样的个人 Codex 可用模型列表。选择器会显示当前生效的个人运行时模型，而普通的 API 模型编辑继续走 Revision 流程保存。原因是工作区此前只在「使用」模式下传入订阅模型选项，而共享的编辑器只要检测到有 Revision 模型控制器就会把这些选项全部屏蔽掉。后端的运行时授权本来就是通的，所以这次主要是前端把可选项正确地透出来。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已随正式 release 上线

## PR 说明

## Summary

Edit Agent now offers the same admitted Personal Codex models as New
Task. The picker displays an active personal runtime model, while
ordinary API model edits continue to save through the Revision flow.

## Root cause

The workspace passed subscription choices only in use mode, and the
shared composer additionally suppressed them whenever a Revision model
controller was present. The backend runtime grants in #3927 and
zooclaw-engine#1761 were already available, but Edit Agent never exposed
the selection.

Personal connections remain runtime bindings rather than source content.
Selecting a different API model first saves the Revision choice and then
explicitly clears an active personal binding. Restoring the same
normalized source model skips the Revision write and only clears the
runtime subscription, including when source/picker IDs use different
provider prefixes. A failed clear remains visible and retryable. When
the source model changes, Revision saves await backend Apply before
clearing the runtime binding. Dirty/read-only revisions and busy/loading
states keep subscription selection disabled. Both sources now wait for a
successful runtime model lookup: before that read, an absent connection
means unknown, so an API-only source save could silently leave an
unobserved subscription active. This includes provisioning/lookup
failures and is covered by a regression test.

Save failures no longer hide the model list: Edit Agent retains its
Settings error, while the launcher reports failure through the existing
toast. Only query/load errors enter the picker error state, so a failed
save can be retried by selecting the model again. New Chat Retry also
refetches the Agent definition and its working/active Revision queries;
missing Revision IDs are skipped and identical IDs share one refetch.

## Test plan

- [x] 93 targeted tests passed after the same-model restoration fix. The
new real Settings/controller regression fails on the old implementation
for `litellm/` and bare source IDs; it now passes without any Revision
commit. Also covers unchanged-source gates, changed-model save ordering,
and clear-failure retry.

- [x] 110 targeted tests passed after the review fix: workspace model
flow, shared composer, Revision warnings, Settings flow, and launcher
Revision query/save behavior.
- [x] Regression checks retain selection after a failed Settings save
and retry a failed launcher model save with the same idempotency key.
Genuine runtime lookup errors still expose Retry.
- [x] 97 targeted tests passed after the launcher Retry fix, including
definition/working/active lookup failure recovery through the picker
controller and no requests for missing Revision IDs.
- [x] Frontend TypeScript, changed-file ESLint, and governance guards.
- [x] Covered Edit Agent/New Task selection, active model display,
reconnection, API return, failed saves/retries, backend admission, and
runtime lookup errors with an actionable Retry button.
- Full frontend suites/build/security checks run in CI. Local pnpm
global virtual-store resolution initially prevented test startup;
reinstalled this worktree with the local virtual store, with no
dependency/lockfile changes.

Frontend-only follow-up; the existing staging Engine beta and backend
authorization endpoints are sufficient. This PR requires the ECAP web
deployment after merge, with no additional Engine release.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `afd87ea99b6e8ca4f044ab2bd47be17725b0842b`
- PR: #3930
- 作者：Chris@ZooClaw
- 日期：2026-09-30T03:21:39Z

### Commit Message

```
fix(agents): allow personal Codex selection while editing (#3930)

## Summary

Edit Agent now offers the same admitted Personal Codex models as New
Task. The picker displays an active personal runtime model, while
ordinary API model edits continue to save through the Revision flow.

## Root cause

The workspace passed subscription choices only in use mode, and the
shared composer additionally suppressed them whenever a Revision model
controller was present. The backend runtime grants in #3927 and
zooclaw-engine#1761 were already available, but Edit Agent never exposed
the selection.

Personal connections remain runtime bindings rather than source content.
Selecting a different API model first saves the Revision choice and then
explicitly clears an active personal binding. Restoring the same
normalized source model skips the Revision write and only clears the
runtime subscription, including when source/picker IDs use different
provider prefixes. A failed clear remains visible and retryable. When
the source model changes, Revision saves await backend Apply before
clearing the runtime binding. Dirty/read-only revisions and busy/loading
states keep subscription selection disabled. Both sources now wait for a
successful runtime model lookup: before that read, an absent connection
means unknown, so an API-only source save could silently leave an
unobserved subscription active. This includes provisioning/lookup
failures and is covered by a regression test.

Save failures no longer hide the model list: Edit Agent retains its
Settings error, while the launcher reports failure through the existing
toast. Only query/load errors enter the picker error state, so a failed
save can be retried by selecting the model again. New Chat Retry also
refetches the Agent definition and its working/active Revision queries;
missing Revision IDs are skipped and identical IDs share one refetch.

## Test plan

- [x] 93 targeted tests passed after the same-model restoration fix. The
new real Settings/controller regression fails on the old implementation
for `litellm/` and bare source IDs; it now passes without any Revision
commit. Also covers unchanged-source gates, changed-model save ordering,
and clear-failure retry.

- [x] 110 targeted tests passed after the review fix: workspace model
flow, shared composer, Revision warnings, Settings flow, and launcher
Revision query/save behavior.
- [x] Regression checks retain selection after a failed Settings save
and retry a failed launcher model save with the same idempotency key.
Genuine runtime lookup errors still expose Retry.
- [x] 97 targeted tests passed after the launcher Retry fix, including
definition/working/active lookup failure recovery through the picker
controller and no requests for missing Revision IDs.
- [x] Frontend TypeScript, changed-file ESLint, and governance guards.
- [x] Covered Edit Agent/New Task selection, active model display,
reconnection, API return, failed saves/retries, backend admission, and
runtime lookup errors with an actionable Retry button.
- Full frontend suites/build/security checks run in CI. Local pnpm
global virtual-store resolution initially prevented test startup;
reinstalled this worktree with the local virtual store, with no
dependency/lockfile changes.

Frontend-only follow-up; the existing staging Engine beta and backend
authorization endpoints are sufficient. This PR requires the ECAP web
deployment after merge, with no additional Engine release.
```

来源：SerendipityOneInc/ecap-workspace @ afd87ea9，PR #3930，作者 Chris@ZooClaw。
