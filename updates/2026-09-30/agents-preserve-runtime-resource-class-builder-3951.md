---
title: "修复：编辑 Pro / Ultra 版 Agent 时运行环境被降级成 Starter，测试和提交报 environment_not_ready"
type: "Bug Fix"
priority: "高"
date: "2026-09-30"
status: "待审核"
channels: ""
---

# 修复：编辑 Pro / Ultra 版 Agent 时运行环境被降级成 Starter，测试和提交报 environment_not_ready

## 核心宣传点

Agent Builder 的测试和提交现在会按 Agent 实际的引擎运行时规格来准备依赖环境：Starter 还是 Starter，Pro 用 Pro，Ultra 用 Ultra，历史数据缺值的仍按原有 Starter 兜底。问题出在两个编辑入口调用环境物化时都没传规格，默认落成了 Starter；在创建流程改为按账号规格选择之后，编辑一个 Pro 的 Agent 会准备出 Starter 变体，然后在引擎的真实运行时校验上报 409 environment_not_ready，前端表现为 agent.runtime_error。修复直接复用已经加载好的 Agent 详情，和既有的更新路径保持一致，而不是重新推算当前账号套餐。环境还在构建中时依然不能产出候选配置或提交 Revision，这个就绪性检查保留。本次只覆盖新物化的环境，规格或套餐变更后复用旧环境是另一条已知路径，单独跟踪。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已随正式 release 上线

## PR 说明

## Summary
- Fixes #3950. Builder test and commit now prepare dependency
environments using the Agent's actual Engine runtime resource class:
Starter stays Starter, Pro uses Pro, and Ultra uses Ultra. Missing
legacy values retain the existing Starter fallback.
- Preserve readiness checks: an environment that is still building
cannot produce a candidate configuration or committed revision.

## Root cause
Both authoring entrypoints omitted `resource_class` when calling
`materialize_environment`, so it defaulted to Starter. After #3925 made
Agent creation select the account's resource class, editing a Pro Agent
could prepare a Starter variant and then fail Engine's actual-runtime
validation with `409 environment_not_ready` (`environment pro variant is
not ready`), surfaced as `agent.runtime_error`.

Use the already-loaded Agent detail, matching the existing update path,
rather than recomputing the current account plan. No Engine validation,
billing, model selection, data migration, or frontend change is needed.

## Scope
The fix covers newly materialized environments. Reusing an unchanged
environment after a runtime class/plan change is an independent
pre-existing path tracked in #3952; this PR does not rebuild or replace
retained/imported environment pins.

## Test plan
- [x] Regression demonstrated before fix: 8 Pro/Ultra cases failed while
8 Starter/legacy cases passed.
- [x] 75 targeted authoring/environment tests passed, including 16 new
cases across both entrypoints, all supported classes plus legacy
fallback, and ready/building states. Tests exercise real environment
materialization and assert Engine build/read parameters and the
no-commit readiness gate.
- [x] Backend static checks (ruff, format, pyright, import-linter).
- [x] CI backend full tests, lint/typecheck, and CodeQL passed for
`805b3be55`; no open code-scanning alerts on the PR merge ref.
- [x] CI aggregate summary passed; all reported checks settled without
failures.

Backend-only deployment. The fix has not been deployed or retested
against live staging; no production/staging data was modified by this
PR.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `1f7ad2d957c7000628bdcd606d23930434c972de`
- PR: #3951
- 作者：Chris@ZooClaw
- 日期：2026-09-30T08:48:07Z

### Commit Message

```
fix(agents): preserve runtime resource class in builder environments (#3951)

## Summary
- Fixes #3950. Builder test and commit now prepare dependency
environments using the Agent's actual Engine runtime resource class:
Starter stays Starter, Pro uses Pro, and Ultra uses Ultra. Missing
legacy values retain the existing Starter fallback.
- Preserve readiness checks: an environment that is still building
cannot produce a candidate configuration or committed revision.

## Root cause
Both authoring entrypoints omitted `resource_class` when calling
`materialize_environment`, so it defaulted to Starter. After #3925 made
Agent creation select the account's resource class, editing a Pro Agent
could prepare a Starter variant and then fail Engine's actual-runtime
validation with `409 environment_not_ready` (`environment pro variant is
not ready`), surfaced as `agent.runtime_error`.

Use the already-loaded Agent detail, matching the existing update path,
rather than recomputing the current account plan. No Engine validation,
billing, model selection, data migration, or frontend change is needed.

## Scope
The fix covers newly materialized environments. Reusing an unchanged
environment after a runtime class/plan change is an independent
pre-existing path tracked in #3952; this PR does not rebuild or replace
retained/imported environment pins.

## Test plan
- [x] Regression demonstrated before fix: 8 Pro/Ultra cases failed while
8 Starter/legacy cases passed.
- [x] 75 targeted authoring/environment tests passed, including 16 new
cases across both entrypoints, all supported classes plus legacy
fallback, and ready/building states. Tests exercise real environment
materialization and assert Engine build/read parameters and the
no-commit readiness gate.
- [x] Backend static checks (ruff, format, pyright, import-linter).
- [x] CI backend full tests, lint/typecheck, and CodeQL passed for
`805b3be55`; no open code-scanning alerts on the PR merge ref.
- [x] CI aggregate summary passed; all reported checks settled without
failures.

Backend-only deployment. The fix has not been deployed or retested
against live staging; no production/staging data was modified by this
PR.
```

来源：SerendipityOneInc/ecap-workspace @ 1f7ad2d9，PR #3951，作者 Chris@ZooClaw。
