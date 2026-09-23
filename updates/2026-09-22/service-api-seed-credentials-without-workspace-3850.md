---
title: "修复：通过 SDK / Service API 创建的 Agent 不再因缺少工作区而拿不到凭证"
type: "Bug Fix"
priority: "中"
date: "2026-09-22"
status: "待审核"
channels: ""
---

# 修复：通过 SDK / Service API 创建的 Agent 不再因缺少工作区而拿不到凭证

## 核心宣传点

用 SDK 创建 service-API Agent 时，创建接口会返回 502，留下一个停止状态、且没有 litellm 和 user-internal-token 凭证的 Agent。根因是写凭证之前会先初始化「工作区拥有的资源策略」，而 SDK 创建的 Agent 本来就有意不带工作区文档，于是 Engine 那边创建成功了，凭证初始化却以 agent.resources_not_ready 失败。现在这类 Agent 不再要求存在工作区即可完成凭证初始化，有工作区的 Agent 生命周期里资源策略初始化行为保持不变，两条路径的凭证写入顺序都补了回归测试。

## 分级

- 内部：P1
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary

- seed credentials for SDK-created service-API Agents without requiring
an `EngineAgentWorkspace`
- keep resource-policy initialization unchanged for workspace-backed
Agent lifecycles
- add regression coverage for both service-API and workspace-backed
credential ordering

## Root cause

`seed_engine_agent_credentials` began initializing the workspace-owned
resource policy before writing credentials. SDK-created Agents
intentionally have no workspace document, so Engine creation succeeded
but credential initialization failed with `agent.resources_not_ready`.
The public create call then returned 502 and left a stopped Agent
without `litellm` or `user-internal-token` credentials.

## Validation

- 126 targeted tests passed; 2 Mongo-backed BDD scenarios skipped
because the local Mongo service was not running
- `bash scripts/verify-py.sh`
- `bash scripts/verify-changed.sh`

No staging write smoke was run. After deployment, verify the legacy
service-token flow with create, start, and delete.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `ebc66f2272bb8668457773eeea7cb24de799c72e`
- PR: #3850
- 作者：finn-srp
- 日期：2026-09-22T02:22:28Z

### Commit Message

```
fix(service-api): seed credentials without workspace (#3850)

## Summary

- seed credentials for SDK-created service-API Agents without requiring
an `EngineAgentWorkspace`
- keep resource-policy initialization unchanged for workspace-backed
Agent lifecycles
- add regression coverage for both service-API and workspace-backed
credential ordering

## Root cause

`seed_engine_agent_credentials` began initializing the workspace-owned
resource policy before writing credentials. SDK-created Agents
intentionally have no workspace document, so Engine creation succeeded
but credential initialization failed with `agent.resources_not_ready`.
The public create call then returned 502 and left a stopped Agent
without `litellm` or `user-internal-token` credentials.

## Validation

- 126 targeted tests passed; 2 Mongo-backed BDD scenarios skipped
because the local Mongo service was not running
- `bash scripts/verify-py.sh`
- `bash scripts/verify-changed.sh`

No staging write smoke was run. After deployment, verify the legacy
service-token flow with create, start, and delete.
```

来源：SerendipityOneInc/ecap-workspace @ ebc66f22，PR #3850，作者 finn-srp。
