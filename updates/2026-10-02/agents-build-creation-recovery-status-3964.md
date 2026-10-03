---
title: "新增 owner 维度的 Agent Build 创建状态查询接口，用于找回丢失的创建结果"
type: "产品基础功能更新"
priority: "中"
date: "2026-10-02"
status: "内部-跳过"
channels: ""
---

# 新增 owner 维度的 Agent Build 创建状态查询接口，用于找回丢失的创建结果

## 核心宣传点

新增 owner 维度的 POST /agent-definitions/creation-status 接口，只接受原始幂等键，用来恢复那些响应丢失、或者 ECAP 卸载早于 Engine 拆除的 Agent Build 创建请求。接口按与创建相同的方式推导工作区身份，明确返回 absent / partial / terminal 三种状态、运行时 ID 和定义的不透明运行时归属，并拒绝 main、内部、已收养、模板和共享副本记录。它是只读的，复用已有的单集合 owned 查询，没有新增查询形式、数据迁移或生命周期租约。另外只读的 source-root 发现接口现在会一并返回已保存的 change_set_id，这样调用方可以直接用现成的 owned ChangeSet API，而不必让模型自己编一个 ID。

## 分级

- 内部：P1
- 外部：内部
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Problem and behavior

New Agent Build smoke (zooclaw-engine#1784) needs to recover a creation
whose response was lost, or whose ECAP uninstall completed before Engine
teardown. Public definition reads require a revision and hide terminal
workspaces; replaying creation cannot recover terminal identity.

Add owner-scoped `POST /agent-definitions/creation-status` accepting
only the original idempotency key. It derives the same workspace
identity as creation and returns explicit absent/partial/terminal
status, runtime IDs and the definition's opaque runtime ownership. It
rejects main, internal, adopted, template and shared-copy records. The
endpoint is read-only and reuses the existing single-collection owned
lookup; no new query form, migration or lifecycle lease.

The existing read-only source-root discovery response also exposes its
saved `change_set_id`, so B02 can use the existing owned ChangeSet API
instead of asking the model to invent an ID. No additional write API or
server ID algorithm is duplicated.

## Validation

- 98 targeted tests passed: new lifecycle/ownership/HTTP contracts plus
existing creation and route boundaries.
- `bash scripts/verify-py.sh` passed: ruff, format, pyright and import
contracts.
- Commit hooks passed, including CSFLE-related repository guards and
architecture checks.
- Live encrypted-client/staging acceptance remains pending deployment
with the Engine smoke companion. No shared staging or production data
was mutated.

Related:
https://github.com/SerendipityOneInc/zooclaw-engine/issues/1784.
Server-side stuck lifecycle and late authoring fencing remain separate
product issues #3960 and #3963. This PR does not claim to fix those
lifecycle races.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `0ae9eec1fa36a23c891aa7d65dce3756e9d8a801`
- PR: #3964
- 作者：Chris@ZooClaw
- 日期：2026-10-02T03:55:32Z

### Commit Message

```
feat(agents): expose owned Build creation recovery status (#3964)

## Problem and behavior

New Agent Build smoke (zooclaw-engine#1784) needs to recover a creation
whose response was lost, or whose ECAP uninstall completed before Engine
teardown. Public definition reads require a revision and hide terminal
workspaces; replaying creation cannot recover terminal identity.

Add owner-scoped `POST /agent-definitions/creation-status` accepting
only the original idempotency key. It derives the same workspace
identity as creation and returns explicit absent/partial/terminal
status, runtime IDs and the definition's opaque runtime ownership. It
rejects main, internal, adopted, template and shared-copy records. The
endpoint is read-only and reuses the existing single-collection owned
lookup; no new query form, migration or lifecycle lease.

The existing read-only source-root discovery response also exposes its
saved `change_set_id`, so B02 can use the existing owned ChangeSet API
instead of asking the model to invent an ID. No additional write API or
server ID algorithm is duplicated.

## Validation

- 98 targeted tests passed: new lifecycle/ownership/HTTP contracts plus
existing creation and route boundaries.
- `bash scripts/verify-py.sh` passed: ruff, format, pyright and import
contracts.
- Commit hooks passed, including CSFLE-related repository guards and
architecture checks.
- Live encrypted-client/staging acceptance remains pending deployment
with the Engine smoke companion. No shared staging or production data
was mutated.

Related:
https://github.com/SerendipityOneInc/zooclaw-engine/issues/1784.
Server-side stuck lifecycle and late authoring fencing remain separate
product issues #3960 and #3963. This PR does not claim to fix those
lifecycle races.
```

来源：SerendipityOneInc/ecap-workspace @ 0ae9eec1，PR #3964，作者 Chris@ZooClaw。
