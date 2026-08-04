---
title: "修复 Agent Builder 工作区状态误报"
type: "Bug Fix"
priority: "中"
date: "2026-08-03"
status: "待审核"
channels: ""
---

## 核心宣传点

当工作区访问临时排队或失败时，Agent Builder 不再误报“配置失败”，项目与工作区健康状态显示更准确。

## 原始内容

**Commit**: `e5595b19cde7b893c028a57563aa656a4a8c5a6f` — kaka-srp — 2026-08-03T07:35:55Z

### Commit Message

```
fix(agent-builder): separate workspace access from project state (#3194)

## Summary
- keep persisted Agent Builder project lifecycle and workspace-health
state unchanged when workspace access is waiting or fails
- contain v1 with an independent browser-lock access state and a waiting
banner, without adding new v1 backend infrastructure
- gate v1 chat, Package/Test, and live model changes on active workspace
access
- return structured v2 lease-holder metadata, preserve same-project
multi-page acquisition, and classify waiting only from
`agent_builder.workspace_in_use`
- retry recoverable v2 renewal failures after lease expiry, prevent late
activation from restoring a lost lease, and distinguish live, expired,
recovery, and unknown holders
- keep Builder update/reinstall available as a control-plane recovery
action when workspace health is failed

Linear:
[ECA-1351](https://linear.app/srpone/issue/ECA-1351/separate-agent-builder-workspace-access-state)

## Root cause
The v1 Web Lock and v2 Mongo lease adapters converted temporary access
failures into copied `AgentBuilderProject` objects with
`builder_workspace_status = failed`. The UI therefore rendered a setup
failure even though the persisted project and workspace were healthy.
The v2 client also treated every HTTP 409 as workspace contention, so it
could not distinguish another project, a same-project operation, or an
unrelated conflict.

## Review fixes
- disable the v1 live model selector while another page holds the
workspace lock
- reacquire after retryable renewal errors outlive the v2 lease, without
retrying unrelated business conflicts
- ignore activation results from a lease cycle that has already been
invalidated
- filter expired page holders and avoid mislabeling unknown or
same-project page races
- classify expired running operations as recovery-required instead of
still active
- prioritize workspace-access waiting/error notices in the Test pane
while persisted workspace health remains ready
- preserve validation feedback while workspace access is only
initializing

## Test plan
- [x] targeted review-fix frontend suites: 87 passed, plus 9
status-notice tests after the final review fixes
- [x] targeted backend lease service tests: 14 passed
- [x] selected frontend guards, TypeScript, unit tests, and ESLint via
`scripts/verify-web.sh`
- [x] backend ruff, formatting, pyright, and import contracts via
`scripts/verify-py.sh`
- [x] changed-surface verification via `scripts/verify-changed.sh`
- [x] pre-commit and pre-push hooks
```

### PR Body

```
## Summary
- keep persisted Agent Builder project lifecycle and workspace-health state unchanged when workspace access is waiting or fails
- contain v1 with an independent browser-lock access state and a waiting banner, without adding new v1 backend infrastructure
- gate v1 chat, Package/Test, and live model changes on active workspace access
- return structured v2 lease-holder metadata, preserve same-project multi-page acquisition, and classify waiting only from `agent_builder.workspace_in_use`
- retry recoverable v2 renewal failures after lease expiry, prevent late activation from restoring a lost lease, and distinguish live, expired, recovery, and unknown holders
- keep Builder update/reinstall available as a control-plane recovery action when workspace health is failed

Linear: [ECA-1351](https://linear.app/srpone/issue/ECA-1351/separate-agent-builder-workspace-access-state)

## Root cause
The v1 Web Lock and v2 Mongo lease adapters converted temporary access failures into copied `AgentBuilderProject` objects with `builder_workspace_status = failed`. The UI therefore rendered a setup failure even though the persisted project and workspace were healthy. The v2 client also treated every HTTP 409 as workspace contention, so it could not distinguish another project, a same-project operation, or an unrelated conflict.

## Review fixes
- disable the v1 live model selector while another page holds the workspace lock
- reacquire after retryable renewal errors outlive the v2 lease, without retrying unrelated business conflicts
- ignore activation results from a lease cycle that has already been invalidated
- filter expired page holders and avoid mislabeling unknown or same-project page races
- classify expired running operations as recovery-required instead of still active
- prioritize workspace-access waiting/error notices in the Test pane while persisted workspace health remains ready
- preserve validation feedback while workspace access is only initializing

## Test plan
- [x] targeted review-fix frontend suites: 87 passed, plus 9 status-notice tests after the final review fixes
- [x] targeted backend lease service tests: 14 passed
- [x] selected frontend guards, TypeScript, unit tests, and ESLint via `scripts/verify-web.sh`
- [x] backend ruff, formatting, pyright, and import contracts via `scripts/verify-py.sh`
- [x] changed-surface verification via `scripts/verify-changed.sh`
- [x] pre-commit and pre-push hooks

```
