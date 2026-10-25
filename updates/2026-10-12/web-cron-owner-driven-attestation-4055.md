---
title: "修复：网页端创建的定时任务会携带所有者校验标记，Engine 可区分本人操作与服务调用"
type: "后端功能"
priority: "中"
date: "2026-10-12"
status: "待审核"
channels: ""
---

# 修复：网页端创建的定时任务会携带所有者校验标记，Engine 可区分本人操作与服务调用

## 核心宣传点

此前网页端创建的定时任务到达 Engine 时属于「未经证明的管理写入」，worker 无法区分发起方是通过鉴权的 Agent 所有者还是组织服务 API 调用方。现在只有在网页端定时任务创建/更新服务完成工作区 UID 与组织归属校验之后，才会带上 x-zooclaw-owner-driven: true 这个标记。客户端选项默认 false，通用的组织服务 API 转发仍会重建上游 header，无法中转调用方自行伪造的所有者断言。新建且通过所有者校验的任务会记录所有者权限；更新只保留已有标记，不会补写或恢复缺失的标记。无前端改动，无数据库迁移。

## 分级

- 内部：P2
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## 备注

需与 Engine 侧实现 zooclaw-engine#1961 配套发版才生效；历史存量任务需由所有者重新创建才会带上该标记，Heartbeat 不在本次范围内。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `38521dc252fce583d6b3e2607312afc64dde147f`
- PR: #4055
- 作者：kaka-srp
- 日期：2026-10-12T09:16:36Z

### Commit Message

```
fix(schedules): attest owner-checked Web cron writes (#4055)

Web-created schedules currently reach Engine as unproved management
writes, so the worker cannot distinguish the authenticated Agent owner
from an org service-API caller. Send `x-zooclaw-owner-driven: true` only
from the existing Web schedule create/update service after its workspace
UID/org ownership check succeeds.

The client option defaults to false; generic org service-API forwarding
continues to rebuild upstream headers and cannot relay a caller-supplied
owner assertion. No frontend changes or database migration.

Companion Engine implementation:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1961 (related
to Engine #1738 and the cron part of #1739). New owner-checked Web
creation records owner authority; updates only preserve an existing
mark, never add or restore a missing one. Old tasks require owner
recreation. Heartbeat is outside this change.

Validation: 76 targeted schedule client/service/routes and authenticated
service-API tests passed; `scripts/verify-py.sh` and
`scripts/verify-changed.sh` passed (ruff, formatting, pyright and import
boundaries). Tests cover workspace owner/org mismatch, explicit header
emission and stripping forged headers from service API requests. CI
passed, including 12,192 Python tests (5 existing skips) and both
automated reviews.

Rollout: Engine controld support → this backend header → Engine worker
memory gate. All old workers must be replaced to close the runtime
vulnerability. Neither PR is a deployment.
```

