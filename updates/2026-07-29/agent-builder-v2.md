---
title: "Agent Builder v2 上线：由全新引擎驱动，搭建 Agent 更强更稳"
type: "新功能上线"
priority: "高"
外部: "B"
date: "2026-07-29"
status: "待审核"
channels: ""
---

## 核心宣传点

全新的 Engine 版 Agent Builder 上线，符合条件的用户会自动进入 v2 体验，搭建自定义 Agent 的能力与稳定性显著增强，同时保持与旧版兼容、可平滑过渡。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- commit：7f5dfa0725dfdfb237dcff76cd3b9cbbda650f03
- PR：#3121
- 日期：2026-07-29T12:29:37Z

### Commit message

```
feat(agent-builder): add engine-backed builder v2 (#3121)

## Linear

https://linear.app/srpone/issue/ECA-1315/agent-builder-v2

## Summary

- Introduce a fully versioned Agent Builder entry boundary so v1 and v2
use separate frontend APIs, clients, backend routers, runtime services,
and project ownership checks. This keeps v1 compatible while making it
removable later.
- Route eligible users to Engine-backed Agent Builder v2 using the same
backend capability rule as Agent v2 installation. Staging and local
development are open; production remains controlled by the configured
email allowlist and global kill switch.
- Provision one hidden, warm Agent Studio Engine Agent per account/org
and reuse its Sandbox across Builder projects. Each project receives an
independent Engine session and Mattermost channel.
- Implement shared-Sandbox project isolation with
capture/activate/restore operations, backend operation leases,
stale-operation recovery, and first-activation initialization for new
projects.
- Add v1 project upgrade gating and migration into v2. Migration
captures the legacy workspace, imports it through Agent Studio tooling,
preserves the original project on failure, and switches runtime metadata
with compare-and-set protection.
- Move Pack Test v2 to managed Engine Test Agents. Reuse the physical
Test Agent when the Environment hash is unchanged, create a fresh
session per run, and replace the Agent when Environment content changes.
- Integrate Engine Sandbox prepare/exec/cleanup APIs, exact
environment-version polling and logs, scoped archive upload validation,
Pack skill pins, warm creation, model selection, and runtime cleanup.
- Use ACS terminal-message metadata for reliable Pack Test completion
and prevent premature or missing candidate-response handoff.
- Simplify the v2 UI by removing legacy Claw connection/header model
controls, adding explicit preparation and migration states, and keeping
model selection in the chat composer.
- Update the Agent Builder v2 design and implementation documents with
runtime ownership, workspace isolation, migration, Pack Test,
submission, cleanup, and rollout decisions.

Related Agent Studio work:

- https://github.com/SerendipityOneInc/ecap-agent-pack/pull/209

The required Engine changes have been merged and released to staging as
`v0.1.0-beta.75`.

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] `bash scripts/verify-py.sh`
- [x] Backend targeted suite: 306 passed
- [x] Frontend selected verification: TypeScript, 481 Vitest tests, and
ESLint passed
- [x] Manual staging-backed local validation of project creation,
activation, migration, Pack Test, submission, update, and Engine runtime
preparation

## Review notes

- This is intentionally a large feature PR because the version boundary
must land atomically across frontend routing, backend ownership, runtime
orchestration, persistence, migration, and tests. Splitting those
contracts would leave an intermediate state where v1 and v2 can call
each other's endpoints.
- Please apply the `size-override` label for the repository size gate.
- Local tests must override `AGENTS_V2_ENABLED=false` when running with
the developer staging `.env`; otherwise existing install tests
intentionally contact the configured staging ACS.
```

### PR body

## Linear

https://linear.app/srpone/issue/ECA-1315/agent-builder-v2

## Summary

- Introduce a fully versioned Agent Builder entry boundary so v1 and v2 use separate frontend APIs, clients, backend routers, runtime services, and project ownership checks. This keeps v1 compatible while making it removable later.
- Route eligible users to Engine-backed Agent Builder v2 using the same backend capability rule as Agent v2 installation. Staging and local development are open; production remains controlled by the configured email allowlist and global kill switch.
- Provision one hidden, warm Agent Studio Engine Agent per account/org and reuse its Sandbox across Builder projects. Each project receives an independent Engine session and Mattermost channel.
- Implement shared-Sandbox project isolation with capture/activate/restore operations, backend operation leases, stale-operation recovery, and first-activation initialization for new projects.
- Add v1 project upgrade gating and migration into v2. Migration captures the legacy workspace, imports it through Agent Studio tooling, preserves the original project on failure, and switches runtime metadata with compare-and-set protection.
- Move Pack Test v2 to managed Engine Test Agents. Reuse the physical Test Agent when the Environment hash is unchanged, create a fresh session per run, and replace the Agent when Environment content changes.
- Integrate Engine Sandbox prepare/exec/cleanup APIs, exact environment-version polling and logs, scoped archive upload validation, Pack skill pins, warm creation, model selection, and runtime cleanup.
- Use ACS terminal-message metadata for reliable Pack Test completion and prevent premature or missing candidate-response handoff.
- Simplify the v2 UI by removing legacy Claw connection/header model controls, adding explicit preparation and migration states, and keeping model selection in the chat composer.
- Update the Agent Builder v2 design and implementation documents with runtime ownership, workspace isolation, migration, Pack Test, submission, cleanup, and rollout decisions.

Related Agent Studio work:

- https://github.com/SerendipityOneInc/ecap-agent-pack/pull/209

The required Engine changes have been merged and released to staging as `v0.1.0-beta.75`.

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] `bash scripts/verify-py.sh`
- [x] Backend targeted suite: 306 passed
- [x] Frontend selected verification: TypeScript, 481 Vitest tests, and ESLint passed
- [x] Manual staging-backed local validation of project creation, activation, migration, Pack Test, submission, update, and Engine runtime preparation

## Review notes

- This is intentionally a large feature PR because the version boundary must land atomically across frontend routing, backend ownership, runtime orchestration, persistence, migration, and tests. Splitting those contracts would leave an intermediate state where v1 and v2 can call each other's endpoints.
- Please apply the `size-override` label for the repository size gate.
- Local tests must override `AGENTS_V2_ENABLED=false` when running with the developer staging `.env`; otherwise existing install tests intentionally contact the configured staging ACS.

