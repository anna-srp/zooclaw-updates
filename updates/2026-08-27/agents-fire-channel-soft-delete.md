---
title: "修复：解雇 Agent 后，它占用的聊天频道连接没有真正断开"
type: "Bug Fix"
priority: "中"
date: "2026-08-27"
status: "待审核"
channels: ""
---

# 修复：解雇 Agent 后，它占用的聊天频道连接没有真正断开

## 核心宣传点

解雇（Fire）或卸载 Agent 时，原来只是把它绑定的聊天频道「停用」，长连接并没有被真正关掉，被解雇的 Agent 仍可能挂在你的 IM 上。现在终态清理会改为真正删除这些频道，网关随即断开对应的连接。可恢复的场景（Agent Studio 暂存、订阅或运行时挂起）保持原来的「停用」语义不变，不会误删。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `566c4150ecf1672dce851bcf9d465299e5f7426f`
- PR: #3562
- 作者: kaka-srp
- 日期: 2026-08-27T17:39:05Z

### Commit Message

```
fix(agents): soft-delete channels on fire (#3562)

## Summary

- switch terminal Agent fire/uninstall cleanup from bulk disable to ACS
bulk soft delete
- keep recoverable Agent Studio and subscription/runtime suspension
flows on bulk disable
- use the same terminal cleanup for temporary pack-test Agents
- retain best-effort cleanup semantics after the Agent reaches its
terminal state

## Behavior

ACS publishes a delete reconcile for every soft-deleted channel.
Existing gateway reconciliation removes the account from desired state
and invokes the platform plugin's `stopAccount`, closing its WebSocket
or other long-lived connection.

## Validation

- 12 directly related pytest cases passed across the ACS client, Agent
channel helper, uninstall lifecycle, service proxy, and pack-test
cleanup
- changed-file Ruff and formatting checks passed
- changed-file Pyright passed with 0 errors
- `bash scripts/verify-changed.sh` (pre-push): Ruff, formatting,
full-repo Pyright, and import-linter passed
- full local pytest suite not run per request

## Rollout

Depends on
[agent-channel-service#100](https://github.com/SerendipityOneInc/agent-channel-service/pull/100),
which adds `POST
/v1/computers/{computer_id}/agents/{agent_id}/channels/delete`. Deploy
ACS first.

## Design

See
`docs/superpowers/specs/2026-08-27-agent-channel-fire-soft-delete-design.md`.
```

### PR Description

```
## Summary

- switch terminal Agent fire/uninstall cleanup from bulk disable to ACS bulk soft delete
- keep recoverable Agent Studio and subscription/runtime suspension flows on bulk disable
- use the same terminal cleanup for temporary pack-test Agents
- retain best-effort cleanup semantics after the Agent reaches its terminal state

## Behavior

ACS publishes a delete reconcile for every soft-deleted channel. Existing gateway reconciliation removes the account from desired state and invokes the platform plugin's `stopAccount`, closing its WebSocket or other long-lived connection.

## Validation

- 12 directly related pytest cases passed across the ACS client, Agent channel helper, uninstall lifecycle, service proxy, and pack-test cleanup
- changed-file Ruff and formatting checks passed
- changed-file Pyright passed with 0 errors
- `bash scripts/verify-changed.sh` (pre-push): Ruff, formatting, full-repo Pyright, and import-linter passed
- full local pytest suite not run per request

## Rollout

Depends on [agent-channel-service#100](https://github.com/SerendipityOneInc/agent-channel-service/pull/100), which adds `POST /v1/computers/{computer_id}/agents/{agent_id}/channels/delete`. Deploy ACS first.

## Design

See `docs/superpowers/specs/2026-08-27-agent-channel-fire-soft-delete-design.md`.

```

---
