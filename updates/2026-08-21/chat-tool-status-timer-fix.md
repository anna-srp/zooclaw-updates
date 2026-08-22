---
title: "修复：工具已执行结束，界面上的计时器却还在跑"
type: "Bug Fix"
priority: "中"
date: "2026-08-21"
status: "待审核"
channels: ""
---

# 修复：工具已执行结束，界面上的计时器却还在跑

## 核心宣传点

工具执行很快就失败时，结束消息有可能比开始消息更早送达界面，于是一条已经报错的步骤会被后到的「运行中」状态覆盖，计时器继续往上跳，看起来像卡住了。现在步骤一旦进入完成、出错或已取消状态就不会再被改回运行中，后到的补充信息照常合并，但计时不会被重新唤醒。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `aec8ed32c56daeba1f50e268302638b7f95ee4be`
- PR: #3470
- 作者: rayrain-srp
- 日期: 2026-08-21T03:50:59Z

### Commit Message

```
fix(chat): preserve terminal tool status (#3470)

## Summary
- keep legacy Mattermost tool states terminal once they reach `done`,
`error`, or `cancelled`
- still merge late descriptive metadata without letting a delayed
`running` event restart the timer
- add regression coverage for out-of-order terminal/start/running posts
and replayed running events

## Root cause
OpenClaw emits tool callbacks best-effort, and the Mattermost plugin
publishes lifecycle posts independently. For fast tool failures, the
terminal post can reach Mattermost before the start/running posts. The
ECAP parser merged by Mattermost arrival order and allowed the later
`running` status to overwrite an already-terminal step, so the UI
resumed an elapsed timer for a tool that had already failed.

This PR adds the agreed ECAP consumer-side protection only. It does not
change Mattermost/OpenClaw publishing or project/workspace association
behavior.

Linear:
https://linear.app/srpone/issue/ECA-1388/agent-builder-%E5%B7%A5%E5%85%B7%E7%BB%88%E6%80%81%E8%A2%AB%E8%BF%9F%E5%88%B0%E7%9A%84-running-%E8%A6%86%E7%9B%96%E5%AF%BC%E8%87%B4%E6%8C%81%E7%BB%AD%E8%AE%A1%E6%97%B6

## Test plan
- [x] `git diff --check`
- [x] Prettier check for both changed files
- [x] web governance guards
- [ ] targeted Vitest, TypeScript, and ESLint locally: attempted, but
Node workers repeatedly blocked in kernel `wait_on_page_bit_common`
before producing test/type/lint results; GitHub CI is the authoritative
clean-runner validation
- [x] GitHub CI: 38/38 checks passed, including web tests,
lint/typecheck, build, and CodeQL
```

### PR Body

## Summary
- keep legacy Mattermost tool states terminal once they reach `done`, `error`, or `cancelled`
- still merge late descriptive metadata without letting a delayed `running` event restart the timer
- add regression coverage for out-of-order terminal/start/running posts and replayed running events

## Root cause
OpenClaw emits tool callbacks best-effort, and the Mattermost plugin publishes lifecycle posts independently. For fast tool failures, the terminal post can reach Mattermost before the start/running posts. The ECAP parser merged by Mattermost arrival order and allowed the later `running` status to overwrite an already-terminal step, so the UI resumed an elapsed timer for a tool that had already failed.

This PR adds the agreed ECAP consumer-side protection only. It does not change Mattermost/OpenClaw publishing or project/workspace association behavior.

Linear: https://linear.app/srpone/issue/ECA-1388/agent-builder-%E5%B7%A5%E5%85%B7%E7%BB%88%E6%80%81%E8%A2%AB%E8%BF%9F%E5%88%B0%E7%9A%84-running-%E8%A6%86%E7%9B%96%E5%AF%BC%E8%87%B4%E6%8C%81%E7%BB%AD%E8%AE%A1%E6%97%B6

## Test plan
- [x] `git diff --check`
- [x] Prettier check for both changed files
- [x] web governance guards
- [ ] targeted Vitest, TypeScript, and ESLint locally: attempted, but Node workers repeatedly blocked in kernel `wait_on_page_bit_common` before producing test/type/lint results; GitHub CI is the authoritative clean-runner validation
- [x] GitHub CI: 38/38 checks passed, including web tests, lint/typecheck, build, and CodeQL

