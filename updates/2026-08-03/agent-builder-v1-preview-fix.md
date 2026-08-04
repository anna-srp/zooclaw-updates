---
title: "修复 Agent Builder v1 Pack 测试预览"
type: "Bug Fix"
priority: "中"
date: "2026-08-03"
status: "待审核"
channels: ""
---

## 核心宣传点

在 Agent Builder 里测试 v1 Pack 时，预览对话框恢复可用，改动能即时看到反馈，创建/调试 Agent 更顺畅。

## 原始内容

**Commit**: `4cc91bf5b6128f3a40896c3be6cafc45febded72` — kaka-srp — 2026-08-03T12:03:07Z

### Commit Message

```
fix(agent-builder): restore v1 pack test preview (#3207)

## Summary

- restore channel-scoped preview behavior for `computer_v1` Agent
Builder Pack Test sessions
- restore v1 terminal-turn detection and Builder feedback from
`turn_status`
- ignore late v1 terminal statuses that belong to a turn before a reset
boundary
- keep `engine_v2` previews isolated by `root_post_id`
- add regression coverage for v1 null-root, plain-response feedback, and
the v2 missing-root guard

## Root cause

The Agent Builder v2 rollout made the shared preview chat require
`root_post_id` for every runtime. A v1 Pack Test preview is scoped by
its Mattermost DM channel and intentionally returns a null root, so the
composer stayed disabled even though the bot connection was healthy.

The same shared component also derived reviewable turns only from v2
`assistant_segment` metadata. Normal v1 replies terminate through
`turn_status` and do not carry that metadata, preventing automatic and
manual feedback from reaching Builder after chat connectivity was
restored.

## Validation

- `bash scripts/verify-changed.sh`
- `bash scripts/verify-local.sh --web-static
'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderTestChat.tsx'
web/app/tests/unit/app/agent-builder-test-chat.unit.spec.tsx`
- 23 targeted Vitest cases passed, including a real v1 terminal status
with a plain assistant reply and a late status after `/new`

## Risk

Frontend-only runtime branching. v1 restores its pre-v2 channel and
terminal-status behavior; v2 root-scoped and terminal-segment behavior
is unchanged.
```

### PR Body

```
## Summary

- restore channel-scoped preview behavior for `computer_v1` Agent Builder Pack Test sessions
- restore v1 terminal-turn detection and Builder feedback from `turn_status`
- ignore late v1 terminal statuses that belong to a turn before a reset boundary
- keep `engine_v2` previews isolated by `root_post_id`
- add regression coverage for v1 null-root, plain-response feedback, and the v2 missing-root guard

## Root cause

The Agent Builder v2 rollout made the shared preview chat require `root_post_id` for every runtime. A v1 Pack Test preview is scoped by its Mattermost DM channel and intentionally returns a null root, so the composer stayed disabled even though the bot connection was healthy.

The same shared component also derived reviewable turns only from v2 `assistant_segment` metadata. Normal v1 replies terminate through `turn_status` and do not carry that metadata, preventing automatic and manual feedback from reaching Builder after chat connectivity was restored.

## Validation

- `bash scripts/verify-changed.sh`
- `bash scripts/verify-local.sh --web-static 'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderTestChat.tsx' web/app/tests/unit/app/agent-builder-test-chat.unit.spec.tsx`
- 23 targeted Vitest cases passed, including a real v1 terminal status with a plain assistant reply and a late status after `/new`

## Risk

Frontend-only runtime branching. v1 restores its pre-v2 channel and terminal-status behavior; v2 root-scoped and terminal-segment behavior is unchanged.

```
