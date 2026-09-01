---
title: "修复：Agent Builder 里一步工具失败，整个活动就被标成「失败」并卡住计时"
type: "Bug Fix"
priority: "中"
date: "2026-08-31"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：Agent Builder 里一步工具失败，整个活动就被标成「失败」并卡住计时

## 核心宣传点

Agent Builder 的活动面板以前有个毛病：只要历史步骤里出现过一次工具失败，整条活动的标题就会被顶成「Failed at step …」，哪怕那次失败本身是可恢复的、后面已经继续跑下去了。原来正常滚动的耗时显示也会被这个失败标签永久替换掉。现在失败只停留在它自己那一行明细里，活动标题该显示「进行中」就显示进行中、跑完就正常给出完成摘要，取消的判定逻辑不变。

同时修了新建空白项目时的一个报错：服务端生成的 bootstrap 会先去探测 agent/agent-pack.yaml，但空白项目压根还没有这个清单文件。现在改成先读项目上下文，新项目直接跳过不存在的清单。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `477029a819a932f09362fe87c7b79b929a000c93`
- PR: #3599
- 作者: kaka-srp
- 日期: 2026-08-31T11:46:48Z

### Commit Message

```
fix(agent-builder): keep recoverable steps in normal flow (#3599)

## Summary

- Make the server-generated Agent Builder bootstrap read project context
first and skip the absent manifest for new projects.
- Keep tool-step failures local to their detail rows instead of turning
the whole activity header into `Failed at step …`.
- Preserve the normal elapsed-time display while the turn continues and
the normal completed activity summary after it finishes, without
changing cancellation semantics.

## Root cause

The bootstrap probed `agent/agent-pack.yaml` before reading the project
mode, although blank projects do not have a manifest yet. Separately,
`ToolGroup` promoted any historical step with `phase: error` to the
aggregate activity status, so a recoverable tool failure permanently
replaced the running/completed timer with a failure label.

## Test plan

- [x] `pnpm exec vitest run src/__tests__/tool-group.test.tsx` — 55
passed
- [x] `pnpm tsc` and `pnpm lint` in `web/packages/chat-ui`
- [x] `pytest tests/unit/test_agent_builder_service.py -q` — 190 passed
- [x] `bash scripts/verify-py.sh`
- [x] Pre-push PR-size and changed-surface gates

## Known unrelated baseline

The full `@zooclaw/chat-ui` suite passed 453/454 tests. The single
failure is the unchanged ModelPicker test expecting `rounded-[8px]`
while the current design-system component renders `rounded-md`; it
reproduces when run alone and is unrelated to the touched activity
timeline files.

## Related

- Paired V2 Agent Studio source PR:
https://github.com/SerendipityOneInc/ecap-agent-pack/pull/251
```

### PR Description

```
## Summary

- Make the server-generated Agent Builder bootstrap read project context first and skip the absent manifest for new projects.
- Keep tool-step failures local to their detail rows instead of turning the whole activity header into `Failed at step …`.
- Preserve the normal elapsed-time display while the turn continues and the normal completed activity summary after it finishes, without changing cancellation semantics.

## Root cause

The bootstrap probed `agent/agent-pack.yaml` before reading the project mode, although blank projects do not have a manifest yet. Separately, `ToolGroup` promoted any historical step with `phase: error` to the aggregate activity status, so a recoverable tool failure permanently replaced the running/completed timer with a failure label.

## Test plan

- [x] `pnpm exec vitest run src/__tests__/tool-group.test.tsx` — 55 passed
- [x] `pnpm tsc` and `pnpm lint` in `web/packages/chat-ui`
- [x] `pytest tests/unit/test_agent_builder_service.py -q` — 190 passed
- [x] `bash scripts/verify-py.sh`
- [x] Pre-push PR-size and changed-surface gates

## Known unrelated baseline

The full `@zooclaw/chat-ui` suite passed 453/454 tests. The single failure is the unchanged ModelPicker test expecting `rounded-[8px]` while the current design-system component renders `rounded-md`; it reproduces when run alone and is unrelated to the touched activity timeline files.

## Related

- Paired V2 Agent Studio source PR: https://github.com/SerendipityOneInc/ecap-agent-pack/pull/251

```

## 备注

配套的 V2 Agent Studio 源码 PR 在 ecap-agent 仓库。
