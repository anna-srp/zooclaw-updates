---
title: "Agent Builder 全新对话式界面与发布流程"
type: "产品基础功能更新"
priority: "中"
date: "2026-08-10"
status: "待审核"
channels: ""
---

# Agent Builder 全新对话式界面与发布流程

## 核心宣传点

Agent Builder 换成以对话为核心的新界面（首页/创建/构建/预览/发布），发布环节整合了原先的验收与提交步骤，可一步选择「仅自己可见 / 私密链接 / 上架市场」，也能直接把已安装的 Agent 更新到新版本。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `152529cb255da9522990eb484058e112bd86bae2`
- PR: #3299

### Commit Message

```
feat(agent-builder): integrate home chat and publishing flows (#3299)

## Linear

N/A

## Summary

- Replace the legacy Agent Builder screens with the latest chat-first
home, creation, Builder, Preview, and Publish UI while keeping Agent
Builder V1 and V2 fully decoupled behind their own adapters.
- Complete the new Publish orchestration: Publish now covers the former
Accept Test and Submit workflow, updates an already installed V1 or V2
agent to the newly published version, and supports Only me, private
link, and Marketplace destinations.
- Restore generic chat composer Skill and Connector behavior instead of
introducing Agent Builder project-level bindings; keep Agent settings,
User feedback, and Analysis disabled until their new-UI workflows are
defined.
- Harden long-running Builder flows: retain publish selection during
polling, keep active V2 workspaces visible across lease renewal, release
acquired leases during cleanup, recover interrupted project
initialization without duplicate posts, and make Preview feedback retry
finite and recoverable.
- Align user-facing copy and actions with the new UI by removing
obsolete Accept Test, Cancel Test, Submit, and Review affordances while
preserving the backend Accept/Submit APIs used internally by Publish.

## Test plan

- [x] `bash scripts/verify-local.sh --changed` — frontend
TypeScript/ESLint and backend Ruff/Pyright/import-linter passed.
- [x] Agent Builder frontend unit suite — 33 files, 341 tests passed.
- [x] Web CI lint orchestrator (`pnpm run lint:ci`) passed, including
dependency boundaries and the Knip dead-code hard gate.
- [x] Agent Builder backend route/service unit suite — 203 tests passed
with V2 disabled for the V1 contract run.
- [x] `git diff --check` passed.
- [x] Local staging-backed smoke: Agent Builder route returned 200, V2
lease/activate calls returned 200, and the page rendered without console
errors.
- [x] GitHub CI validates the PR merge result against current `main` —
Code Quality, CodeQL, build, frontend/backend tests, and automated
review passed.

## Notes

- V1 and V2 remain separate runtime implementations. V1 is retained only
for the migration window and can be removed independently when it is
retired.
- `.external-worktrees/` is local-only and intentionally excluded from
the PR.

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>
Co-authored-by: kaka-srp <kaka@srp.one>
```

### PR Body

## Linear

N/A

## Summary

- Replace the legacy Agent Builder screens with the latest chat-first home, creation, Builder, Preview, and Publish UI while keeping Agent Builder V1 and V2 fully decoupled behind their own adapters.
- Complete the new Publish orchestration: Publish now covers the former Accept Test and Submit workflow, updates an already installed V1 or V2 agent to the newly published version, and supports Only me, private link, and Marketplace destinations.
- Restore generic chat composer Skill and Connector behavior instead of introducing Agent Builder project-level bindings; keep Agent settings, User feedback, and Analysis disabled until their new-UI workflows are defined.
- Harden long-running Builder flows: retain publish selection during polling, keep active V2 workspaces visible across lease renewal, release acquired leases during cleanup, recover interrupted project initialization without duplicate posts, and make Preview feedback retry finite and recoverable.
- Align user-facing copy and actions with the new UI by removing obsolete Accept Test, Cancel Test, Submit, and Review affordances while preserving the backend Accept/Submit APIs used internally by Publish.

## Test plan

- [x] `bash scripts/verify-local.sh --changed` — frontend TypeScript/ESLint and backend Ruff/Pyright/import-linter passed.
- [x] Agent Builder frontend unit suite — 33 files, 341 tests passed.
- [x] Web CI lint orchestrator (`pnpm run lint:ci`) passed, including dependency boundaries and the Knip dead-code hard gate.
- [x] Agent Builder backend route/service unit suite — 203 tests passed with V2 disabled for the V1 contract run.
- [x] `git diff --check` passed.
- [x] Local staging-backed smoke: Agent Builder route returned 200, V2 lease/activate calls returned 200, and the page rendered without console errors.
- [x] GitHub CI validates the PR merge result against current `main` — Code Quality, CodeQL, build, frontend/backend tests, and automated review passed.

## Notes

- V1 and V2 remain separate runtime implementations. V1 is retained only for the migration window and can be removed independently when it is retired.
- `.external-worktrees/` is local-only and intentionally excluded from the PR.

