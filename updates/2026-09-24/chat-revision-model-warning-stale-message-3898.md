---
title: "修复：编辑 Agent 时选到不可用模型会提示更换，聊天列表不再因消息移除而崩"
type: "Bug Fix"
priority: "中"
date: "2026-09-24"
status: "待审核"
channels: ""
---

# 修复：编辑 Agent 时选到不可用模型会提示更换，聊天列表不再因消息移除而崩

## 核心宣传点

两个聊天侧的问题。第一个：可编辑的 Revision Agent 之前被排除在「模型不可用」提示之外，于是 staging 上编辑 Agent 时会一直往已经下线的 deepseek-v4-flash-0731 发请求，拿回一串 403 却看不到任何换模型的提示。现在只要模型目录拉取成功且非空、而所选模型不在目录里，就会弹出不可用提示，替换走原有的 Revision 提交/应用流程，不再走旧的直连模型接口。第二个：聊天消息渲染原先按列表下标订阅，列表变短时子组件的查询会先失效，抛出 tapClientLookup: Index 2 out of bounds 这种错误（错误边界能恢复，但异常挡不住）。现在改用稳定的消息 ID 和逐条快照，未变化的消息行做了 memo，别人的流式更新不会再触发它们重渲染。空目录、加载中和出错的目录仍然按「放行」处理，只读 Agent 和其他 Builder/草稿控制器保持排除。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已上线

## PR 说明

## Summary

Editable Revision Agents now receive the unavailable-model prompt when their selected model is absent from a successfully fetched, nonempty catalog. Replacements use the existing Revision commit/apply flow, rather than the legacy direct model API. This fixes the staging Edit Agent case that continued sending to `deepseek-v4-flash-0731` and received 403 responses without a replacement prompt.

Chat message rendering now uses stable message IDs and per-message snapshots instead of list-index subscriptions. This prevents a removed message's queued reader from throwing `tapClientLookup: Index 2 out of bounds (length: 2)`. Unchanged message rows are memoized so another message's streaming updates do not rerender them.

## Root cause

- PR #3819 excluded every external model controller, including editable Revision Agents; the workspace page also omitted the workspace ID whenever a controller was present.
- The upstream message list subscribed by index. A shrinking list could invalidate a child's lookup before its subscription finished. The existing error boundary recovered afterward but could not prevent the exception.

Revision controllers explicitly opt into catalog validation. Other Builder/draft controllers and read-only Agents remain excluded. Empty/error/loading catalogs still fail open; dismissal/send interception and API-only model options are unchanged. No continue-sending bypass was added.

## Test plan

- [x] Reproduced the missing Revision prompt and workspace ID with failing regressions before the fix.
- [x] Reproduced the exact stale-index error with the actual assistant-ui runtime; verified safe stale reads after removal, reorder, empty/repopulate, and streaming render isolation.
- [x] 357 targeted tests passed across 21 files, including message presentation/actions, Revision settings, and composer behavior.
- [x] Frontend TypeScript, ESLint, and governance guards passed.
- [ ] Full build and suites run in CI.

Frontend deployment only. No live Agent configuration was changed, and no authenticated staging writes were performed. The repair has not yet been validated after staging deployment. Resource-preload performance warnings are outside this fix.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `66f90a497be4e6017db3d3b407e03a9bbfca8922`
- PR: #3898
- 作者：tim-srp
- 日期：2026-09-24T08:43:08Z

### Commit Message

```
fix(chat): cover revision model warnings and stale message lookups (#3898)

## Summary

Editable Revision Agents now receive the unavailable-model prompt when
their selected model is absent from a successfully fetched, nonempty
catalog. Replacements use the existing Revision commit/apply flow,
rather than the legacy direct model API. This fixes the staging Edit
Agent case that continued sending to `deepseek-v4-flash-0731` and
received 403 responses without a replacement prompt.

Chat message rendering now uses stable message IDs and per-message
snapshots instead of list-index subscriptions. This prevents a removed
message's queued reader from throwing `tapClientLookup: Index 2 out of
bounds (length: 2)`. Unchanged message rows are memoized so another
message's streaming updates do not rerender them.

## Root cause

- PR #3819 excluded every external model controller, including editable
Revision Agents; the workspace page also omitted the workspace ID
whenever a controller was present.
- The upstream message list subscribed by index. A shrinking list could
invalidate a child's lookup before its subscription finished. The
existing error boundary recovered afterward but could not prevent the
exception.

Revision controllers explicitly opt into catalog validation. Other
Builder/draft controllers and read-only Agents remain excluded.
Empty/error/loading catalogs still fail open; dismissal/send
interception and API-only model options are unchanged. No
continue-sending bypass was added.

## Test plan

- [x] Reproduced the missing Revision prompt and workspace ID with
failing regressions before the fix.
- [x] Reproduced the exact stale-index error with the actual
assistant-ui runtime; verified safe stale reads after removal, reorder,
empty/repopulate, and streaming render isolation.
- [x] 357 targeted tests passed across 21 files, including message
presentation/actions, Revision settings, and composer behavior.
- [x] Frontend TypeScript, ESLint, and governance guards passed.
- [ ] Full build and suites run in CI.

Frontend deployment only. No live Agent configuration was changed, and
no authenticated staging writes were performed. The repair has not yet
been validated after staging deployment. Resource-preload performance
warnings are outside this fix.
```

来源：SerendipityOneInc/ecap-workspace @ 66f90a49，PR #3898，作者 tim-srp。