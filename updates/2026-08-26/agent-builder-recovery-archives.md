---
title: "修复：Agent Builder 恢复项目时报「找不到可恢复的内容」，测试过的版本白白丢失"
type: "Bug Fix"
priority: "中"
date: "2026-08-26"
status: "待审核"
channels: ""
---

# 修复：Agent Builder 恢复项目时报「找不到可恢复的内容」，测试过的版本白白丢失

## 核心宣传点

Agent Builder 在恢复项目时，只会去找「已验收」状态的历史版本，于是那些已经打包成功、甚至你已经测过用过的版本（准备测试中／测试中／测试评审中）全都不被认账，明明存档还在却报「找不到可恢复的内容」。现在这些状态的存档都能参与恢复，并按从新到旧的顺序逐个校验后取用；处于部署中的版本只有在对应测试任务确实跑到稳定状态后才会被采纳，避免恢复到一个还没成型的版本。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `c441a41913625d472d3861e35e483230e790ba2e`
- PR: #3529
- 作者: kaka-srp
- 日期: 2026-08-26T08:11:25Z

### Commit Message

```
fix(agent-builder): recover ready test archives (#3529)

## Summary
- recover archive-bearing iterations already in `ready_to_test`,
`testing`, `reviewing_test`, or `accepted`
- recover a stale `deploying_test` iteration only when its same-owner,
same-Project TestRun has reached a stable authoritative status
- record the resolved ready/testing/accepted iteration phase in recovery
audit fields and keep the frontend contract synchronized

## Root cause
The recovery fallback only queried `accepted` and `reviewing_test`
iterations. A Pack Test can already be `ready_for_preview` while the
Project and iteration projection still says `deploying_test`; even after
reconciliation it maps to `ready_to_test`, which was also excluded. The
archive key, SHA-256, and R2 object could therefore exist while the
recovery candidate query returned zero rows.

## Safety
- active TestRuns such as `bot_allocating` remain ineligible
- a stale iteration is accepted only when the TestRun belongs to the
same org, owner, Project, and iteration
- existing newest-to-oldest archive validation, SHA-256 verification,
bounded extraction, and submitted-asset fallback remain unchanged

## Test plan
- [x] `pytest tests/unit/test_agent_builder_recovery_source_service.py
tests/unit/test_agent_builder_project_repo.py -q` — 32 passed
- [x] changed-file Ruff and Pyright — 0 errors
- [x] Python pre-commit hooks, file/complexity guards, import contracts,
and Pyright passed
- [x] frontend ESLint passed for `src/models/agent-builder.ts`
- [ ] local full `verify-changed.sh` is blocked by four pre-existing
Pyright errors in `_route_helpers.py`, `test_org_skills_routes.py`, and
`test_skills_manager_routes.py`; none of those files differ in this PR
- [ ] local full web verification used stale shared dependencies in the
no-node worktree: unrelated TypeScript package-contract errors appeared
and 33 Vitest workers timed out; clean-install CI remains authoritative
```

### PR Description

```
## Summary
- recover archive-bearing iterations already in `ready_to_test`, `testing`, `reviewing_test`, or `accepted`
- recover a stale `deploying_test` iteration only when its same-owner, same-Project TestRun has reached a stable authoritative status
- record the resolved ready/testing/accepted iteration phase in recovery audit fields and keep the frontend contract synchronized

## Root cause
The recovery fallback only queried `accepted` and `reviewing_test` iterations. A Pack Test can already be `ready_for_preview` while the Project and iteration projection still says `deploying_test`; even after reconciliation it maps to `ready_to_test`, which was also excluded. The archive key, SHA-256, and R2 object could therefore exist while the recovery candidate query returned zero rows.

## Safety
- active TestRuns such as `bot_allocating` remain ineligible
- a stale iteration is accepted only when the TestRun belongs to the same org, owner, Project, and iteration
- existing newest-to-oldest archive validation, SHA-256 verification, bounded extraction, and submitted-asset fallback remain unchanged

## Test plan
- [x] `pytest tests/unit/test_agent_builder_recovery_source_service.py tests/unit/test_agent_builder_project_repo.py -q` — 32 passed
- [x] changed-file Ruff and Pyright — 0 errors
- [x] Python pre-commit hooks, file/complexity guards, import contracts, and Pyright passed
- [x] frontend ESLint passed for `src/models/agent-builder.ts`
- [ ] local full `verify-changed.sh` is blocked by four pre-existing Pyright errors in `_route_helpers.py`, `test_org_skills_routes.py`, and `test_skills_manager_routes.py`; none of those files differ in this PR
- [ ] local full web verification used stale shared dependencies in the no-node worktree: unrelated TypeScript package-contract errors appeared and 33 Vitest workers timed out; clean-install CI remains authoritative

```

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `0823428d09979db01d8df8ab0dc941378a51dc8f`
- PR: #3520
- 作者: kaka-srp
- 日期: 2026-08-26T06:12:13Z

### Commit Message

```
fix(agent-builder): recover reviewing test archives (#3520)

## Summary
- allow Agent Builder v1 recovery to use archived `reviewing_test`
iterations as well as `accepted` iterations
- validate recoverable iteration archives newest-to-oldest before
falling back to the submitted Pack asset
- persist the exact `reviewing_test_iteration` recovery audit source and
keep the frontend contract in sync
- document the recovery-source contract and add repository/service
regression coverage

## Root cause
When live v1 workspace export was unavailable, the fallback queried only
iterations whose status was `accepted`. Projects with a successfully
packaged and user-tested iteration in `reviewing_test`, but no accepted
iteration or published asset, therefore failed with
`agent_builder.recovery_source_missing` even though a readable archive
and SHA-256 were present.

## Test plan
- [x] `pytest tests/unit/test_agent_builder_recovery_source_service.py
tests/unit/test_agent_builder_project_repo.py
tests/unit/test_agent_builder_recovery_service.py
tests/unit/test_agent_builder_routes.py -q` — 80 passed
- [x] changed-file Pyright — 0 errors
- [x] frontend governance guards, full TypeScript check, and ESLint
passed after rebasing onto current `origin/main`
- [x] Ruff and import-linter passed
- [x] pre-commit hooks passed
- [ ] Full `verify-changed.sh` is blocked by four pre-existing Pyright
errors on `origin/main` in `tests/unit/_route_helpers.py`,
`tests/unit/test_org_skills_routes.py`, and
`tests/unit/test_skills_manager_routes.py`; none of those files differ
in this PR
```

### PR Description

```
## Summary
- allow Agent Builder v1 recovery to use archived `reviewing_test` iterations as well as `accepted` iterations
- validate recoverable iteration archives newest-to-oldest before falling back to the submitted Pack asset
- persist the exact `reviewing_test_iteration` recovery audit source and keep the frontend contract in sync
- document the recovery-source contract and add repository/service regression coverage

## Root cause
When live v1 workspace export was unavailable, the fallback queried only iterations whose status was `accepted`. Projects with a successfully packaged and user-tested iteration in `reviewing_test`, but no accepted iteration or published asset, therefore failed with `agent_builder.recovery_source_missing` even though a readable archive and SHA-256 were present.

## Test plan
- [x] `pytest tests/unit/test_agent_builder_recovery_source_service.py tests/unit/test_agent_builder_project_repo.py tests/unit/test_agent_builder_recovery_service.py tests/unit/test_agent_builder_routes.py -q` — 80 passed
- [x] changed-file Pyright — 0 errors
- [x] frontend governance guards, full TypeScript check, and ESLint passed after rebasing onto current `origin/main`
- [x] Ruff and import-linter passed
- [x] pre-commit hooks passed
- [ ] Full `verify-changed.sh` is blocked by four pre-existing Pyright errors on `origin/main` in `tests/unit/_route_helpers.py`, `tests/unit/test_org_skills_routes.py`, and `tests/unit/test_skills_manager_routes.py`; none of those files differ in this PR

```
