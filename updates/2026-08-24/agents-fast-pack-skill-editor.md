---
title: "Agent 管理页新增「快速编辑 Pack 技能」，改技能不用再开 Agent Builder"
type: "新功能上线"
priority: "高"
date: "2026-08-24"
status: "待审核"
channels: ""
---

# Agent 管理页新增「快速编辑 Pack 技能」，改技能不用再开 Agent Builder

## 核心宣传点

以前想改一个已上架 Pack 的 Skill，得打开 Agent Builder、拉起预览 Agent、走一整套构建流程，改一行提示词也要等半天。现在 Agents 管理页里直接有一个轻量的 Pack 技能编辑器：改完即可发布一个只含 Skill 变更的新版本，人设文件、非文本素材、运行时变体和环境内容锁定都原样保留。发布后还会自动向市场提交对应的上架更新走正常审核，另有一个默认关闭的「更新所有已安装 Agent」选项，可以一次把已安装该 Pack 的 Agent 升到新版本，且不会动各自的凭据。管理页和侧边栏都能看到这个更新入口。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `15967d27f1872c3f5feb4b0d607cd99a62caf79c`
- PR: #3499
- 作者: kaka-srp
- 日期: 2026-08-24T12:18:44Z

### Commit Message

```
feat(agents): add fast pack skill editor (#3499)

## Linear

N/A — this work was explicitly requested without a Linear issue.

## Summary

- add an archive-native v2 Pack Skills editor under Agents Manager,
without opening Agent Builder or starting a preview/test Agent
- publish immutable Skill-only Pack versions while preserving persona
files, non-text Skill assets, runtime variants, and Environment content
pins
- automatically submit origin-linked Marketplace listing updates for
normal review, with a separate pending pointer and an idempotent handoff
retry path
- offer a default-off “Update all installed Agents” option that updates
active v2 installs without copying or refreshing each owner's
credentials
- show the same lightweight update action in Agents Manager and the main
sidebar, querying availability once on page entry/refresh without focus
refetch or polling
- keep the new route on the repository's MVVM boundary and avoid
changing reconnect behavior for unrelated Pack query consumers

## Test plan

- [x] backend feature/regression suite: 188 tests passed
- [x] frontend feature/regression suite: 112 tests passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh --no-test`
- [x] post-rebase conflict checks: Agent workspace indexes and SideNav
actions

## Review notes

- The PR is 4,917 lines after repository exclusions, primarily complete
backend services, the editor UI, and regression tests. It intentionally
uses the repository's `size-override` path so the
source/Marketplace/update flow can be reviewed as one end-to-end change.
- No new collection/table is introduced. Marketplace review state uses
the existing Pack row plus `pending_submission_id`; immutable Pack
assets and submissions remain the source of truth.
```

### PR Body

## Linear

N/A — this work was explicitly requested without a Linear issue.

## Summary

- add an archive-native v2 Pack Skills editor under Agents Manager, without opening Agent Builder or starting a preview/test Agent
- publish immutable Skill-only Pack versions while preserving persona files, non-text Skill assets, runtime variants, and Environment content pins
- automatically submit origin-linked Marketplace listing updates for normal review, with a separate pending pointer and an idempotent handoff retry path
- offer a default-off “Update all installed Agents” option that updates active v2 installs without copying or refreshing each owner's credentials
- show the same lightweight update action in Agents Manager and the main sidebar, querying availability once on page entry/refresh without focus refetch or polling
- keep the new route on the repository's MVVM boundary and avoid changing reconnect behavior for unrelated Pack query consumers

## Test plan

- [x] backend feature/regression suite: 188 tests passed
- [x] frontend feature/regression suite: 112 tests passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh --no-test`
- [x] post-rebase conflict checks: Agent workspace indexes and SideNav actions

## Review notes

- The PR is 4,917 lines after repository exclusions, primarily complete backend services, the editor UI, and regression tests. It intentionally uses the repository's `size-override` path so the source/Marketplace/update flow can be reviewed as one end-to-end change.
- No new collection/table is introduced. Marketplace review state uses the existing Pack row plus `pending_submission_id`; immutable Pack assets and submissions remain the source of truth.

