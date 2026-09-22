---
title: "fix(schedule): translate dispatched / awaiting_approval / unknown engine run statuses (#3829)"
type: "Bug Fix"
priority: "低"
date: "2026-09-21"
status: "待审核"
channels: ""
---

# 修复：日程运行历史里三种状态显示成原始英文字符串

## 核心宣传点

Engine 现在会给日程运行记录的每一行返回显式状态，其中 dispatched、awaiting_approval、unknown 三个值前端没有对应翻译，于是直接以灰色原始字符串显示。这次给运行状态徽章补上这三个映射，中英文各加三条文案（已派发 / 等待审批 / 未知），其余 8 种语言按约定回退英文；等待审批沿用和「运行中」一样的信息色。

## 分级

- 内部：P2
- 外部：C
- 发布状态：已上线

## PR 说明

## Summary
- `RunStatusBadge`（`web/app/src/components/agent-schedules/DailyTaskList.tsx`）补上 engine run 行的三个状态映射：`dispatched` → `schedule.runDispatched`、`awaiting_approval` → `schedule.runAwaitingApproval`、`unknown` → `schedule.runUnknown`；`awaiting_approval` 用和 `running` 一样的 info 色调。
- `en.ts` / `zh.ts` 各加三条文案（Dispatched / Awaiting approval / Unknown；已派发 / 等待审批 / 未知）。其余 8 种语言按 `locales/README.md` 的约定回退英文。

## Root cause
zooclaw-engine [#1499](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1499) 让 `GET …/schedules/{id}/runs` 的每个关联行都带显式 `status`（turn 未结束时是 `dispatched` / `running` / `awaiting_approval`，无法归因时是 `unknown`，结束后是 schedule 自己的 verdict）。claw-interface 的 `engine_run_entry_to_model` 直接透传字符串（schema 是 `str | None`），前端 badge 只有 `running` 等几个 key 的翻译，新值以原始字符串灰色显示。`dispatched` 是 claw 对无 status 行的既有合成值，此前也一直是原始字符串，一并补上。

## Test plan
- [x] `bash scripts/verify-web.sh` 对三个文件：guards / tsc / vitest（480 文件 6112 例）/ eslint 全过
- [ ] staging 上打开一个正在跑或等审批的 engine schedule 的运行历史，badge 显示"运行中 / 等待审批 / 已派发"而不是原始字符串

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01Q5ZYBmHaNT8LvcEazcXv7i


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `7069ae4929621f3928feaaf56c4e98d77e418728`
- PR: #3829
- 作者：Chris@ZooClaw
- 日期：2026-09-21T02:15:30Z

### Commit Message

```
fix(schedule): translate dispatched / awaiting_approval / unknown engine run statuses (#3829)

## Summary
-
`RunStatusBadge`（`web/app/src/components/agent-schedules/DailyTaskList.tsx`）补上
engine run 行的三个状态映射：`dispatched` →
`schedule.runDispatched`、`awaiting_approval` →
`schedule.runAwaitingApproval`、`unknown` →
`schedule.runUnknown`；`awaiting_approval` 用和 `running` 一样的 info 色调。
- `en.ts` / `zh.ts` 各加三条文案（Dispatched / Awaiting approval / Unknown；已派发
/ 等待审批 / 未知）。其余 8 种语言按 `locales/README.md` 的约定回退英文。

## Root cause
zooclaw-engine
[#1499](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1499) 让
`GET …/schedules/{id}/runs` 的每个关联行都带显式 `status`（turn 未结束时是 `dispatched`
/ `running` / `awaiting_approval`，无法归因时是 `unknown`，结束后是 schedule 自己的
verdict）。claw-interface 的 `engine_run_entry_to_model` 直接透传字符串（schema 是
`str | None`），前端 badge 只有 `running` 等几个 key
的翻译，新值以原始字符串灰色显示。`dispatched` 是 claw 对无 status 行的既有合成值，此前也一直是原始字符串，一并补上。

## Test plan
- [x] `bash scripts/verify-web.sh` 对三个文件：guards / tsc / vitest（480 文件
6112 例）/ eslint 全过
- [ ] staging 上打开一个正在跑或等审批的 engine schedule 的运行历史，badge 显示"运行中 / 等待审批 /
已派发"而不是原始字符串

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01Q5ZYBmHaNT8LvcEazcXv7i

Co-authored-by: Claude Opus 5 (1M context) <noreply@anthropic.com>
```

来源：SerendipityOneInc/ecap-workspace @ 7069ae49，PR #3829，作者 Chris@ZooClaw。