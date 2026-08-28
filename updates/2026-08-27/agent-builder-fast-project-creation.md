---
title: "Agent Builder 新建项目不再干等半分钟，点完立刻进入项目页"
type: "体验优化"
priority: "高"
date: "2026-08-27"
status: "待审核"
channels: ""
---

# Agent Builder 新建项目不再干等半分钟，点完立刻进入项目页

## 核心宣传点

以前在 Agent Builder 点「新建项目」后，页面要一直卡在创建界面，等运行环境、模型、附件和第一轮对话全部准备完才跳转——线上实测光是标题生成一项就要 21~28 秒。现在项目记录一存下来就立即跳进项目页（这一步只要几十毫秒），剩下的准备工作在项目页里带进度动画继续跑，你能立刻看到项目已经建好了。同时修掉了多台服务器重复执行准备流程、重复调用标题生成的浪费。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `71a591f55b46017b875519a958ed97d6247f2e37`
- PR: #3545
- 作者: kaka-srp
- 日期: 2026-08-27T06:14:14Z

### Commit Message

```
perf(agent-builder): speed up project creation (#3545)

## Summary

- Navigate to the new Agent Builder Project page as soon as the Project
record is persisted, then continue model, attachment, and first-turn
initialization on that page.
- Serialize Engine v2 setup across pods with a renewable Mongo lease and
skip redundant synchronous LLM title generation for the dedicated
Builder session.
- Preserve same-tab `File` objects for the full setup window, keep
interactions locked from the first preparing frame, and show accessible
animated progress plus explicit retry only when recovery is possible.
- Document the production trace findings, ownership model, failure
recovery, and cross-Project callback isolation in
`docs/superpowers/specs/2026-08-27-agent-builder-fast-project-creation.md`.

## Root cause

The Project document itself was created in roughly 32 ms, but the create
screen waited for runtime/session setup, selected-model application,
attachments, and the first turn before navigating. Duplicate setup
runners on separate pods also each made an unnecessary synchronous
title-generation call; the observed calls took about 21 and 28 seconds.

## Test plan

- [x] `255` targeted backend unit tests passed for Project repository,
routes, and service setup behavior.
- [x] `139` targeted frontend unit tests passed for create navigation,
pending initialization, Project interaction locking, recovery, and
preparing UI.
- [x] Full pre-commit gates passed: frontend ESLint; Python ruff/format,
file length, dependency consistency, import-linter, repo-list sync, and
Pyright.
- [x] `pnpm exec tsc --noEmit` passed.
- [x] Pyright on every changed Python file passed with `0 errors`.
- [x] Final independent code review passed with no findings after fixes
for lease ownership, handoff lifetime, retry semantics, first-frame
locking, and cross-Project async callback isolation.
- [x] CI checks pass (`45/45`).

## Known baseline issue

The full local `verify-changed` Pyright run still reports four existing
errors in unchanged route-helper tests (`_route_helpers.py`,
`test_org_skills_routes.py`, and `test_skills_manager_routes.py`). Those
files are identical to `origin/main`; all Python files changed by this
PR pass Pyright. The branch was pushed with only that local verification
step bypassed after the remaining web, Python, import-contract,
unit-test, and size gates passed.
```

### PR Description

```
## Summary

- Navigate to the new Agent Builder Project page as soon as the Project record is persisted, then continue model, attachment, and first-turn initialization on that page.
- Serialize Engine v2 setup across pods with a renewable Mongo lease and skip redundant synchronous LLM title generation for the dedicated Builder session.
- Preserve same-tab `File` objects for the full setup window, keep interactions locked from the first preparing frame, and show accessible animated progress plus explicit retry only when recovery is possible.
- Document the production trace findings, ownership model, failure recovery, and cross-Project callback isolation in `docs/superpowers/specs/2026-08-27-agent-builder-fast-project-creation.md`.

## Root cause

The Project document itself was created in roughly 32 ms, but the create screen waited for runtime/session setup, selected-model application, attachments, and the first turn before navigating. Duplicate setup runners on separate pods also each made an unnecessary synchronous title-generation call; the observed calls took about 21 and 28 seconds.

## Test plan

- [x] `255` targeted backend unit tests passed for Project repository, routes, and service setup behavior.
- [x] `139` targeted frontend unit tests passed for create navigation, pending initialization, Project interaction locking, recovery, and preparing UI.
- [x] Full pre-commit gates passed: frontend ESLint; Python ruff/format, file length, dependency consistency, import-linter, repo-list sync, and Pyright.
- [x] `pnpm exec tsc --noEmit` passed.
- [x] Pyright on every changed Python file passed with `0 errors`.
- [x] Final independent code review passed with no findings after fixes for lease ownership, handoff lifetime, retry semantics, first-frame locking, and cross-Project async callback isolation.
- [x] CI checks pass (`45/45`).

## Known baseline issue

The full local `verify-changed` Pyright run still reports four existing errors in unchanged route-helper tests (`_route_helpers.py`, `test_org_skills_routes.py`, and `test_skills_manager_routes.py`). Those files are identical to `origin/main`; all Python files changed by this PR pass Pyright. The branch was pushed with only that local verification step bypassed after the remaining web, Python, import-contract, unit-test, and size gates passed.

```

---
