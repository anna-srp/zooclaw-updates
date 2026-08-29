---
title: "聊天里的工具执行过程显示更准：失败就是失败，不会被后到的事件抹掉"
type: "体验优化"
priority: "中"
date: "2026-08-28"
status: "待审核"
channels: ""
---

# 聊天里的工具执行过程显示更准：失败就是失败，不会被后到的事件抹掉

## 核心宣传点

聊天中展示的「工具活动」以前只靠工具名猜文案，图片状态查询、异步等待、子任务查看、工作区保存、会话状态查询这些操作经常显示成看不懂的通用标签。现在会从结构化参数里解析出具体动作，给出准确的中文说明。更重要的是执行结果的合并改成了单向递进（运行中 < 完成 < 已取消 < 出错）——迟到或重放的完成事件再也不能把你已经看到的失败或取消覆盖成「成功」。命令执行失败时会显示正确的失败标签和图标，同时把未经处理的原始错误文本挡在时间线外，不会糊你一脸堆栈。底部那条耗时统计也正名为「总历时」。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `650f6bb55264b92f36017b195acb6fda354946a8`
- PR: #3540
- 作者: rayrain-srp
- 日期: 2026-08-28T11:19:24Z

### Commit Message

```
fix(chat): clarify tool activity outcomes (#3540)

## Summary

- Project an allowlisted activity action from structured tool args and
resolve accurate labels for image status/model queries, async waits,
subtask inspection, workspace saves, session-status inspection, and
failed commands.
- Make `tool_call_id` outcome merging monotonic (`running < done <
cancelled < error`) so late/replayed completion events cannot erase an
observed failure or cancellation; keep the first observed action stable.
- Preserve only allowlisted actions when replay snapshot input already
contains structured `tool_steps`, and carry them back into the shared
`ToolStep` model as forward-compatible serialization plumbing.
- Show failed commands with the correct failure label/icon while keeping
raw `resultPreview`-derived `errorMessage`/`summary`/unclassified
progress out of the timeline until a producer-sanitized failure field
exists.
- Label the existing wall-clock activity span as `Total elapsed` /
`总历时`, and preserve English fallback for locales without dedicated
activity copy.
- Keep polling collapse, cross-bubble causal grouping, and the
association of standalone V2 `tool_status` posts into public-share
replay out of scope until the upstream correlation contract tracked by
ECA-1410 exists.

Linear: ECA-1409

## Root cause

The activity UI selected copy from the tool name alone and did not
retain the safe `action` field from structured args. Its replay merge
guarded terminal states only against later non-terminal events, so a
later `completed` event could replace an earlier `failed` or `cancelled`
outcome for the same call. Where structured replay `tool_steps` are
present, snapshot normalization also dropped the new action field. The
group duration was already a wall-clock span, but the copy presented it
as an unlabeled duration. The V2 producer currently derives generic
failure fields from raw tool `resultPreview`, so those fields are not a
safe human-facing detail contract.

Current V2 public shares expose a separate upstream boundary: tool
activity is stored in standalone Mattermost `tool_status` posts, while
selected user/assistant posts do not contain persisted `tool_steps`.
ECA-1409 preserves `action` when structured steps are supplied, but does
not guess how to associate standalone tool posts with a selected
assistant turn. That association requires the causal correlation
contract tracked by ECA-1410.

## Test plan

- [x] `pnpm exec vitest run src/__tests__/tool-presentation.test.ts
src/__tests__/tool-group.test.tsx` (`@zooclaw/chat-ui`: 119 tests)
- [x] App adapter/MM/i18n targeted Vitest suites and the final
reordered/stable-action parser suite; `subagents({})` compatibility is
intentionally out of scope until upstream projects an allowlisted action
- [x] Replay snapshot conversion Vitest suite (15 tests) and
claw-interface replay creation suite (37 tests); these verify action
preservation when structured `tool_steps` are present
- [x] Failed-command result-preview safety regression in the ToolGroup
suite (54 tests after current `origin/main` merge)
- [x] `pnpm tsc` and `pnpm lint` in `web/packages/chat-ui`
- [x] `bash scripts/verify-changed.sh` after merging the latest
`origin/main` (Web guards/tsc/ESLint; Python
ruff/format/Pyright/import-linter)
- [x] Repository pre-push size gate and changed-surface verification
- [x] V2 staging E2E on `runtime=engine`: action-aware image/subagent
labels, failed-command presentation, monotonic error precedence under a
late completion, total-elapsed copy, English/Chinese rendering, and
fresh-page persisted rendering
- [x] Public-share boundary diagnostic: current V2 snapshots contain no
`tool_steps`; public replay E2E is therefore deferred to ECA-1410 rather
than implemented with adjacency/time/tool-name heuristics
```

### PR Description

```
## Summary

- Project an allowlisted activity action from structured tool args and resolve accurate labels for image status/model queries, async waits, subtask inspection, workspace saves, session-status inspection, and failed commands.
- Make `tool_call_id` outcome merging monotonic (`running < done < cancelled < error`) so late/replayed completion events cannot erase an observed failure or cancellation; keep the first observed action stable.
- Preserve only allowlisted actions when replay snapshot input already contains structured `tool_steps`, and carry them back into the shared `ToolStep` model as forward-compatible serialization plumbing.
- Show failed commands with the correct failure label/icon while keeping raw `resultPreview`-derived `errorMessage`/`summary`/unclassified progress out of the timeline until a producer-sanitized failure field exists.
- Label the existing wall-clock activity span as `Total elapsed` / `总历时`, and preserve English fallback for locales without dedicated activity copy.
- Keep polling collapse, cross-bubble causal grouping, and the association of standalone V2 `tool_status` posts into public-share replay out of scope until the upstream correlation contract tracked by ECA-1410 exists.

Linear: ECA-1409

## Root cause

The activity UI selected copy from the tool name alone and did not retain the safe `action` field from structured args. Its replay merge guarded terminal states only against later non-terminal events, so a later `completed` event could replace an earlier `failed` or `cancelled` outcome for the same call. Where structured replay `tool_steps` are present, snapshot normalization also dropped the new action field. The group duration was already a wall-clock span, but the copy presented it as an unlabeled duration. The V2 producer currently derives generic failure fields from raw tool `resultPreview`, so those fields are not a safe human-facing detail contract.

Current V2 public shares expose a separate upstream boundary: tool activity is stored in standalone Mattermost `tool_status` posts, while selected user/assistant posts do not contain persisted `tool_steps`. ECA-1409 preserves `action` when structured steps are supplied, but does not guess how to associate standalone tool posts with a selected assistant turn. That association requires the causal correlation contract tracked by ECA-1410.

## Test plan

- [x] `pnpm exec vitest run src/__tests__/tool-presentation.test.ts src/__tests__/tool-group.test.tsx` (`@zooclaw/chat-ui`: 119 tests)
- [x] App adapter/MM/i18n targeted Vitest suites and the final reordered/stable-action parser suite; `subagents({})` compatibility is intentionally out of scope until upstream projects an allowlisted action
- [x] Replay snapshot conversion Vitest suite (15 tests) and claw-interface replay creation suite (37 tests); these verify action preservation when structured `tool_steps` are present
- [x] Failed-command result-preview safety regression in the ToolGroup suite (54 tests after current `origin/main` merge)
- [x] `pnpm tsc` and `pnpm lint` in `web/packages/chat-ui`
- [x] `bash scripts/verify-changed.sh` after merging the latest `origin/main` (Web guards/tsc/ESLint; Python ruff/format/Pyright/import-linter)
- [x] Repository pre-push size gate and changed-surface verification
- [x] V2 staging E2E on `runtime=engine`: action-aware image/subagent labels, failed-command presentation, monotonic error precedence under a late completion, total-elapsed copy, English/Chinese rendering, and fresh-page persisted rendering
- [x] Public-share boundary diagnostic: current V2 snapshots contain no `tool_steps`; public replay E2E is therefore deferred to ECA-1410 rather than implemented with adjacency/time/tool-name heuristics

```
