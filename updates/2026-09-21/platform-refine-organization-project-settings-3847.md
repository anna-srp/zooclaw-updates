---
title: "feat(platform): refine organization and project settings (#3847)"
type: "新功能"
priority: "中"
date: "2026-09-21"
status: "待审核"
channels: ""
---

# 开发者平台：组织与项目设置继续打磨

## 核心宣传点

开发者平台把个人资料和组织设置统一收进同一个设置入口，Clerk 的账号资料管理仍然可见。组织下新增 People 和 Projects 的预览流程，但暂时不开放邀请成员和修改项目成员关系。项目管理留在主项目外壳里：侧边栏有 Settings，页面内分 General、Members、Limits 三个标签。项目列表简化成一个 Manage 操作，并且在设置页之间来回切换时会保持当前选中的项目。

## 分级

- 内部：P1
- 外部：B
- 发布状态：已合并待发版

## PR 说明

## Linear

N/A

## Summary

- unify personal profile and Organization settings behind one settings entry while keeping Clerk profile management visible
- add Organization People and Projects preview flows without enabling invitation or Project membership mutations
- keep Project management inside the main Project shell, with Settings in the sidebar and General, Members, and Limits tabs in the page
- simplify the Projects list to a single Manage action and preserve the selected Project across settings navigation

## Test plan

- [x] `fnm exec --using=24 pnpm --dir web/platform lint`
- [x] `fnm exec --using=24 pnpm --dir web/platform typecheck`
- [x] `fnm exec --using=24 pnpm --dir web/platform test`
- [x] `fnm exec --using=24 pnpm --dir web/platform build`
- [x] `cd web/app && fnm exec --using=24 pnpm test:unit`
- [x] Manually verified the Projects → Manage → Project Settings → Members flow with the local app, real Clerk session, Organization, and Project data


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `dd71e532ac698d23126941ddbc020f179290582b`
- PR: #3847
- 作者：finn-srp
- 日期：2026-09-21T13:27:30Z

### Commit Message

```
feat(platform): refine organization and project settings (#3847)

## Linear

N/A

## Summary

- unify personal profile and Organization settings behind one settings
entry while keeping Clerk profile management visible
- add Organization People and Projects preview flows without enabling
invitation or Project membership mutations
- keep Project management inside the main Project shell, with Settings
in the sidebar and General, Members, and Limits tabs in the page
- simplify the Projects list to a single Manage action and preserve the
selected Project across settings navigation

## Test plan

- [x] `fnm exec --using=24 pnpm --dir web/platform lint`
- [x] `fnm exec --using=24 pnpm --dir web/platform typecheck`
- [x] `fnm exec --using=24 pnpm --dir web/platform test`
- [x] `fnm exec --using=24 pnpm --dir web/platform build`
- [x] `cd web/app && fnm exec --using=24 pnpm test:unit`
- [x] Manually verified the Projects → Manage → Project Settings →
Members flow with the local app, real Clerk session, Organization, and
Project data
```

来源：SerendipityOneInc/ecap-workspace @ dd71e532，PR #3847，作者 finn-srp。