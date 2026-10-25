---
title: "修复：换用运行时凭据后，旧版技能读不到自己的 Agent 与日程"
type: "Bug Fix"
priority: "高"
date: "2026-10-22"
status: "待审核"
channels: ""
---

# 修复：换用运行时凭据后，旧版技能读不到自己的 Agent 与日程

## 核心宣传点

读取归属者 Agent 列表和日程的旧版 Work 技能，在用户登录凭据被替换为不透明运行时凭据后会直接失去访问权限，相关功能静默失效。本次在 Agent 列表、Agent 详情、日程投递目标、日程列表这四个既有读接口上放行该凭据：新的读取主体会校验凭据有效性、规范来源 Agent、当前生效投影与旧版策略，以及归属者和组织成员身份是否仍然有效；原有的目标归属校验保持不变，显式上下文请求头必须匹配。运行时发起的列表请求不再触发隐式默认 Agent 的重试创建，其余接口仍然依赖用户登录态。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `bbd548237d778128d3d8e44b83db77a73f4c9a2b`
- PR: #4117
- 作者：kaka-srp
- 日期：2026-10-22T07:42:14Z

### Commit Message

```
fix(agents): allow legacy Work runtime owner reads (#4117)

## Summary

Legacy Work Skills that read the owner's Agent list and schedules
currently lose access when their user Bearer is replaced by an opaque
runtime credential. Allow that credential on four existing read
endpoints: Agent list, Agent detail, schedule delivery targets, and
schedule list.

The new read principal verifies the live credential, canonical source
Agent, current applied projection and legacy policy, and active
owner/organization membership. Existing target ownership checks remain
in place; explicit context headers must match. Runtime list requests
skip the implicit default-Agent retry/create. All other endpoints retain
their current login dependency.

## Root cause

These reads only accepted the user login principal. A runtime credential
must retain its narrower read purpose instead of becoming a user login
or authorizing Agent/schedule changes. No policy schema, customer Skill,
login or JWT changes are included.

## Test plan

- 144 related tests passed, including HTTP sibling reads, foreign
owner/org rejection, legacy/explicit/Platform/revoked/context guards,
and no implicit creation during runtime list.
- Normal pre-push changed-surface verification passed: Ruff
check/format, full application/test Pyright and all eight import
contracts. Commit hooks also passed.
- Staging acceptance for this CI change has not run. The separate Proxy
KB compatibility PR222 is independently staged and is not a prerequisite
for these reads.
```

