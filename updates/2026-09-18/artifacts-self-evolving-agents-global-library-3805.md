---
title: "fix(artifacts): include self-evolving agents in global library (#3805)"
type: "Bug Fix"
priority: "高"
date: "2026-09-18"
status: "待审核"
channels: ""
---

# 修复：自进化 Agent 产出的文件现在会出现在全局 Artifacts 里

## 核心宣传点

全局 Artifacts 之前会漏掉自进化 Agent（包括在 Build 页管理的那些 Agent）发布的文件，找东西时要一个个进工作区翻。现在枚举工作区时带上了 definitions，这些文件会正常收进全局库。无需数据库迁移或重新上传，已有文件会直接出现。

## 分级

- 内部：P1
- 外部：B
- 发布状态：已合并待发版

## PR 说明

## Summary
Global Artifacts now includes published files from self-evolving Agents, including Agents managed through the Build page. The production change is one line: pass the existing `include_definitions=True` option when enumerating workspaces.

## Root cause
The library reused the workspace list's default behavior, which excludes self-evolving definitions before their artifacts are queried. Existing artifact registration and runtime ownership translation already work.

No database migration, backfill, upload, or Engine change is needed. Existing registered files become visible after the backend deployment. Existing ownership and visibility filters remain in place.

## Test plan
- [x] New regression fails before the fix and passes afterward; verifies the published artifact is returned using its runtime actor.
- [x] Artifact library unit suite: 20 passed.
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright, and all 8 import contracts passed.
- [x] Read-only production diagnosis confirmed ready artifact records and successful workspace enumeration with the existing option enabled.

Deployment: claw-interface backend only.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `8568b87582a972fab1ff30d26d719779dd56e54a`
- PR: #3805
- 作者：tim-srp
- 日期：2026-09-18T11:48:21Z

### Commit Message

```
fix(artifacts): include self-evolving agents in global library (#3805)

## Summary
Global Artifacts now includes published files from self-evolving Agents,
including Agents managed through the Build page. The production change
is one line: pass the existing `include_definitions=True` option when
enumerating workspaces.

## Root cause
The library reused the workspace list's default behavior, which excludes
self-evolving definitions before their artifacts are queried. Existing
artifact registration and runtime ownership translation already work.

No database migration, backfill, upload, or Engine change is needed.
Existing registered files become visible after the backend deployment.
Existing ownership and visibility filters remain in place.

## Test plan
- [x] New regression fails before the fix and passes afterward; verifies
the published artifact is returned using its runtime actor.
- [x] Artifact library unit suite: 20 passed.
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright, and all 8
import contracts passed.
- [x] Read-only production diagnosis confirmed ready artifact records
and successful workspace enumeration with the existing option enabled.

Deployment: claw-interface backend only.
```

## 备注

发布状态：已合并待发版（尚未包含在任何 ecap-*-release tag 中，最新正式 release 为 ecap-v0.19.16-release）。

来源：SerendipityOneInc/ecap-workspace @ 8568b875，PR #3805，作者 tim-srp。
