---
title: Agent Builder 仅允许对已雇佣 Agent 进行 Fork
type: Bug Fix
priority: B
date: 2026-07-17
status: 已合并待发版
pr: 2924
author: kaka-srp
url: https://github.com/SerendipityOneInc/ecap-workspace/pull/2924
---

## 更新内容

收紧 Agent Builder 的 Fork 权限：

- 仅允许 Fork 当前电脑上已雇佣（hired）的 Agent
- 后端同步强制「已雇佣」校验，使用持久化 pack ID + 命名空间安全的旧版回退
- 隐藏发布页上不可用的 Fork 入口，覆盖 ID 冲突、加载/错误态、直接进入绕过等场景

## 用户价值

修复 Fork 可用性此前基于全局显示匹配导致的越权 Fork 问题，确保用户只能 Fork 自己已获取的 Agent。
