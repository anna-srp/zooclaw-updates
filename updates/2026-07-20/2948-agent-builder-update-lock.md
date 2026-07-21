---
title: "修复 Agent Studio：更新 Agent 后再编辑不再失败"
type: "Bug Fix"
priority: "中"
date: "2026-07-20"
status: "待审核"
channels: ""
---

## 核心宣传点

修复了在 Agent Studio 更新已安装 Agent 时偶发的工作区冲突（更新后编辑失败）。现在更新与编辑会有序排队执行，更新过程更可靠，遇到繁忙时会给出明确的重试提示。

### 原始内容

**Commit message:**

```
fix(agent-builder): serialize workspace updates (#2948)

## Summary
- serialize Agent Studio archive workspace mutation with Agent Builder's
existing `.agent-builder-projects/.workspace.lock`
- keep archive download/extraction outside the critical section, then
bound lock acquisition to 120 seconds
- map `WORKSPACE_BUSY` to a 409-style conflict and surface that retry
hint from failed background updates
- preserve project snapshots during the normal `preserve` update path; a
`clean` overwrite keeps only the lock inode and invalidates stale
snapshots

## Root cause
Agent Builder project materialization already held a workspace lock
while it captured, cleared, and restored live project files. Agent
Studio archive deployment did not participate in that lock. An update
could therefore recreate `scripts/` after materialization cleared the
live workspace but before its restore copied the project snapshot,
causing `FileExistsError` and leaving the project in `failed` state.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] production `preserve`, `clean`, timeout, and workspace-busy
mapping regression selection: 4 passed
- [x] full `test_agent_install_service.py`: 94 passed
- [x] `agent-workspaces.unit.spec.ts`: 11 passed
- [x] backend Ruff, Pyright, and import contracts
- [x] frontend TypeScript, ESLint, and targeted Vitest verification

## Staging validation
An earlier targeted runtime integration was run from a fresh ECAP
devcontainer on A102 against a real staging bot through FastClaw runtime
exec and JuiceFS. It validated the shared lock but used `clean` mode, so
it is not presented as parity coverage for the final production
`preserve` update path or as a browser/UI `Finish update` E2E.

- materialize held the lock first: update waited 1.892s, then completed
successfully
- materialize held the lock beyond the test timeout: update returned
`WORKSPACE_BUSY` with no partial write
- update held the lock first: the materializer observed the lock and
waited 1.717s before entering
- all cases preserved the lock inode and temporary staging
workspace/A102 resources were removed

## Tracking
-
[ECA-1273](https://linear.app/srpone/issue/ECA-1273/agent-builder-%E6%9B%B4%E6%96%B0%E5%90%8E%E5%86%8D%E7%BC%96%E8%BE%91%E5%A4%B1%E8%B4%A5workspace-materialization-errno-17)
```

**PR body:**

## Summary
- serialize Agent Studio archive workspace mutation with Agent Builder's existing `.agent-builder-projects/.workspace.lock`
- keep archive download/extraction outside the critical section, then bound lock acquisition to 120 seconds
- map `WORKSPACE_BUSY` to a 409-style conflict and surface that retry hint from failed background updates
- preserve project snapshots during the normal `preserve` update path; a `clean` overwrite keeps only the lock inode and invalidates stale snapshots

## Root cause
Agent Builder project materialization already held a workspace lock while it captured, cleared, and restored live project files. Agent Studio archive deployment did not participate in that lock. An update could therefore recreate `scripts/` after materialization cleared the live workspace but before its restore copied the project snapshot, causing `FileExistsError` and leaving the project in `failed` state.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] production `preserve`, `clean`, timeout, and workspace-busy mapping regression selection: 4 passed
- [x] full `test_agent_install_service.py`: 94 passed
- [x] `agent-workspaces.unit.spec.ts`: 11 passed
- [x] backend Ruff, Pyright, and import contracts
- [x] frontend TypeScript, ESLint, and targeted Vitest verification

## Staging validation
An earlier targeted runtime integration was run from a fresh ECAP devcontainer on A102 against a real staging bot through FastClaw runtime exec and JuiceFS. It validated the shared lock but used `clean` mode, so it is not presented as parity coverage for the final production `preserve` update path or as a browser/UI `Finish update` E2E.

- materialize held the lock first: update waited 1.892s, then completed successfully
- materialize held the lock beyond the test timeout: update returned `WORKSPACE_BUSY` with no partial write
- update held the lock first: the materializer observed the lock and waited 1.717s before entering
- all cases preserved the lock inode and temporary staging workspace/A102 resources were removed

## Tracking
- [ECA-1273](https://linear.app/srpone/issue/ECA-1273/agent-builder-%E6%9B%B4%E6%96%B0%E5%90%8E%E5%86%8D%E7%BC%96%E8%BE%91%E5%A4%B1%E8%B4%A5workspace-materialization-errno-17)

