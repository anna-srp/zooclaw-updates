---
title: "fix(platform): preserve selected project after refresh (#3825)"
type: "Bug Fix"
priority: "中"
date: "2026-09-21"
status: "待审核"
channels: ""
---

# 修复：开发者平台刷新页面后会丢掉当前选中的项目

## 核心宣传点

此前当前项目只存在前端组件状态里，整页刷新后 provider 重建、选中项丢失，于是每次都退回到引导阶段的默认项目。现在选中的项目会被持久化，并且按 Clerk 用户和当前组织分别隔离保存；恢复时直接按 ID 读取，不再翻遍分页列表。为此后端新增了一个组织范围内的单项目读取接口，缺失的项目和跨组织访问返回同样的 404 契约；如果保存的项目已经 404，则回退到默认项目。游标分页只留给项目选择器浏览用。刷新恢复、直接读取、失效选中项和跨组织隔离都补了回归测试。

## 分级

- 内部：P1
- 外部：B
- 发布状态：已上线

## PR 说明

## Summary

- preserve the active Project across a full page refresh
- scope the saved selection by Clerk user and active Organization
- add an Organization-scoped GET /platform/v1/projects/{project_id} endpoint
- restore a saved Project directly by ID instead of scanning paginated lists
- fall back to Default Project when the saved Project returns 404
- keep cursor pagination dedicated to Project selector browsing
- add regression coverage for reload, direct retrieval, stale selections, and cross-Organization isolation

Closes #3823.

## Root cause

The active Project existed only in React component state. A full page refresh rebuilt the provider with no selected Project, so it always fell back to the bootstrap Default Project. The first fix persisted the ID but had to scan every Project page because the backend did not expose a single-Project read endpoint.

## API addition

GET /platform/v1/projects/{project_id} reads one Project using both the requested Project ID and the current Clerk Organization scope. Missing and cross-Organization Projects return the same 404 contract.

## Test plan

- [x] Platform lint
- [x] Platform typecheck
- [x] Platform unit/component tests (18 passed)
- [x] Platform production build
- [x] claw-interface ruff, format, pyright, and import-linter
- [x] Platform route unit tests (5 passed)
- [x] Real MongoDB Platform repository/lifecycle tests (6 passed)


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `df48d5a71a571187c9389cbe6508289a2f96bc2b`
- PR: #3825
- 作者：finn-srp
- 日期：2026-09-21T04:19:38Z

### Commit Message

```
fix(platform): preserve selected project after refresh (#3825)

## Summary

- preserve the active Project across a full page refresh
- scope the saved selection by Clerk user and active Organization
- add an Organization-scoped GET /platform/v1/projects/{project_id}
endpoint
- restore a saved Project directly by ID instead of scanning paginated
lists
- fall back to Default Project when the saved Project returns 404
- keep cursor pagination dedicated to Project selector browsing
- add regression coverage for reload, direct retrieval, stale
selections, and cross-Organization isolation

Closes #3823.

## Root cause

The active Project existed only in React component state. A full page
refresh rebuilt the provider with no selected Project, so it always fell
back to the bootstrap Default Project. The first fix persisted the ID
but had to scan every Project page because the backend did not expose a
single-Project read endpoint.

## API addition

GET /platform/v1/projects/{project_id} reads one Project using both the
requested Project ID and the current Clerk Organization scope. Missing
and cross-Organization Projects return the same 404 contract.

## Test plan

- [x] Platform lint
- [x] Platform typecheck
- [x] Platform unit/component tests (18 passed)
- [x] Platform production build
- [x] claw-interface ruff, format, pyright, and import-linter
- [x] Platform route unit tests (5 passed)
- [x] Real MongoDB Platform repository/lifecycle tests (6 passed)
```

来源：SerendipityOneInc/ecap-workspace @ df48d5a7，PR #3825，作者 finn-srp。