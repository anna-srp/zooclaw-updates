---
title: "定时任务支持私聊消息推送"
type: "新功能上线"
priority: "高"
date: "2026-08-07"
status: "待审核"
channels: ""
---

## 核心宣传点

定时任务现在可以把结果直接推送到你本人的私聊会话，需先完成身份验证，执行结果与投递结果分开展示，失败不再一直卡在「进行中」。

## 原始内容

### feat(schedule): configure verified DM delivery (#3291)

- SHA: `3877f34b0fcc304430de4e33655acdb333327389`
- 仓库: 见 raw/2026-08-07

**Commit Message:**

```
feat(schedule): configure verified DM delivery (#3291)

## Linear

N/A

## Summary

- add explicit `none | announce` schedule-delivery contracts and
server-side validation of verified owner targets
- proxy the agent-scoped DM verification lifecycle through
claw-interface without exposing ACS credentials or runtime identity
- add private-chat target setup to the Schedule UI and show execution
and delivery outcomes independently
- prevent terminal failed executions without a receipt from remaining
permanently pending
- document the complete design, security boundaries, rollout order, and
staging smoke plan

## Dependency and rollout

- Depends on
https://github.com/SerendipityOneInc/agent-channel-service/pull/63
- Deploy ACS first, then claw-interface, then Web

## Test plan

- [x] Ruff and Ruff format checks
- [x] Pyright on the changed schedule service and tests
- [x] 116 focused claw-interface tests
- [x] Full Web TypeScript check and changed-file ESLint
- [x] 130 focused Web tests
- [x] `git diff --check`
- [ ] After deployment, run the six-step staging smoke documented in the
design spec

## Review follow-up

- preserve the one-time DM token while status polling returns token-free
responses
- resolve Engine delivery references through live ACS targets before
returning public target IDs
- move run-delivery projection into the delivery service to satisfy the
backend file-length gate
```

**PR Body:**

## Linear

N/A

## Summary

- add explicit `none | announce` schedule-delivery contracts and server-side validation of verified owner targets
- proxy the agent-scoped DM verification lifecycle through claw-interface without exposing ACS credentials or runtime identity
- add private-chat target setup to the Schedule UI and show execution and delivery outcomes independently
- prevent terminal failed executions without a receipt from remaining permanently pending
- document the complete design, security boundaries, rollout order, and staging smoke plan

## Dependency and rollout

- Depends on https://github.com/SerendipityOneInc/agent-channel-service/pull/63
- Deploy ACS first, then claw-interface, then Web

## Test plan

- [x] Ruff and Ruff format checks
- [x] Pyright on the changed schedule service and tests
- [x] 116 focused claw-interface tests
- [x] Full Web TypeScript check and changed-file ESLint
- [x] 130 focused Web tests
- [x] `git diff --check`
- [ ] After deployment, run the six-step staging smoke documented in the design spec

## Review follow-up

- preserve the one-time DM token while status polling returns token-free responses
- resolve Engine delivery references through live ACS targets before returning public target IDs
- move run-delivery projection into the delivery service to satisfy the backend file-length gate


