---
title: 引擎版与电脑版 Agent 会话线程统一到同一入口
type: 新功能
priority: B
date: 2026-07-22
status: 已合并待发版
pr: 3014
author: bill-srp
url: https://github.com/SerendipityOneInc/ecap-workspace/pull/3014
---

引擎版与电脑版 Agent 会话线程统一到同一入口

## Summary

Frontend slice of **ECA-1269** (engine agent session threads), stacked on the merged backend (#2998). Engine agents had no thread-per-session chat: the session-thread route and its conversation list were computer-id-keyed and filtered to computer agents, and engine rows had their sidenav session accordion suppressed. This migrates **both runtimes** onto a single **workspace-keyed** surface backed by Slice 1's `/agents/{workspace_id}/conversations*` routes.

Linear: https://linear.app/srpone/issue/ECA-1269
Plan: `docs/superpowers/plans/2026-07-21-eca-1269-engine-session-threads.md`

