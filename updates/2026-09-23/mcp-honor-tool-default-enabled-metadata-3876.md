---
title: "MCP 工具支持按服务端推荐的默认开关状态初始化"
type: "新功能上线"
priority: "中"
date: "2026-09-23"
status: "待审核"
channels: ""
---

# MCP 工具支持按服务端推荐的默认开关状态初始化

## 核心宣传点

MCP 服务端现在可以通过 _meta["ecap/defaultEnabled"] 告诉平台某个工具初始应该是关闭的。每个个人连接在第一次成功拉取工具目录时会把明确标为 false 的工具写进自己的 disabled_tools，创建探测失败后恢复的场景也一样处理。之后用户自己的开关操作照旧走原有的持久化和 Engine 同步路径，不会被服务端元数据反复覆盖。效果是接入一个工具很多的 MCP 服务时，默认不会一股脑全打开。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Behavior

MCP tools can recommend an initial enabled state through `_meta["ecap/defaultEnabled"]`. Each personal connection applies explicit false values to its own `disabled_tools` on its first successful catalog discovery, including recovery after a failed creation probe. User toggles then continue through the existing persistence and Engine synchronization paths.

Metadata survives model serialization and public projection. Missing metadata keeps the existing enabled-by-default behavior.

## Scope and review resolution

- Fixed the Codex P1: failed initial discovery no longer bypasses defaults on recovery.
- Fixed the Claude alias observation: metadata survives a model dump/validation round trip.
- Existing initialized connections retain their settings. Newly added tools on a later refresh do not receive defaults in this change; this preserves the agreed initialization-only scope. A successful empty catalog also counts as initialized. Regression coverage pins this boundary.
- No existing-user migration or server/tool-name special cases.

## Validation

25 targeted service/schema/sync tests pass; Ruff passes. Failed-probe recovery and metadata round-trip regressions were reproduced before the fix.

Producer: https://github.com/SerendipityOneInc/ecap-mcp/pull/123. Deploy the consumer before the producer to interpret metadata on newly created connections.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `c2ff27963f2e3d9bef010ca719af0c3ff263e368`
- PR: #3876
- 作者：tim-srp
- 日期：2026-09-23T07:17:30Z

### Commit Message

```
feat(mcp): honor tool default enabled metadata (#3876)

## Behavior

MCP tools can recommend an initial enabled state through
`_meta["ecap/defaultEnabled"]`. Each personal connection applies
explicit false values to its own `disabled_tools` on its first
successful catalog discovery, including recovery after a failed creation
probe. User toggles then continue through the existing persistence and
Engine synchronization paths.

Metadata survives model serialization and public projection. Missing
metadata keeps the existing enabled-by-default behavior.

## Scope and review resolution

- Fixed the Codex P1: failed initial discovery no longer bypasses
defaults on recovery.
- Fixed the Claude alias observation: metadata survives a model
dump/validation round trip.
- Existing initialized connections retain their settings. Newly added
tools on a later refresh do not receive defaults in this change; this
preserves the agreed initialization-only scope. A successful empty
catalog also counts as initialized. Regression coverage pins this
boundary.
- No existing-user migration or server/tool-name special cases.

## Validation

25 targeted service/schema/sync tests pass; Ruff passes. Failed-probe
recovery and metadata round-trip regressions were reproduced before the
fix.

Producer: https://github.com/SerendipityOneInc/ecap-mcp/pull/123. Deploy
the consumer before the producer to interpret metadata on newly created
connections.
```

来源：SerendipityOneInc/ecap-workspace @ c2ff2796，PR #3876，作者 tim-srp。