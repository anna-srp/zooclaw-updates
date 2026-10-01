---
title: "修复：任务跑着的时候离开再回来，「停止」按钮不再消失"
type: "Bug Fix"
priority: "中"
date: "2026-09-30"
status: "待审核"
channels: ""
---

# 修复：任务跑着的时候离开再回来，「停止」按钮不再消失

## 核心宣传点

聊天界面在任务运行过程中跳转到别的页面再回来，「停止」按钮会不见，导致没法中断正在跑的任务，只能干等。现在导航之后仍然会按任务的实际运行状态保留「停止」入口，随时可以把正在执行的任务停下来。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

（无 PR 描述）

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `5509dcd98dc2d377cb109d901748cd73db1121b2`
- PR: #3961
- 作者：tim-srp
- 日期：2026-09-30T17:38:12Z

### Commit Message

```
fix(chat): keep Stop available for running tasks after navigation (#3961)
```

来源：SerendipityOneInc/ecap-workspace @ 5509dcd9，PR #3961，作者 tim-srp。
