---
title: "用模板创建 Agent 快了很多：实测从 25 秒以上降到 3 到 6 秒"
type: "Improvement"
priority: "高"
date: "2026-09-29"
status: "待审核"
channels: ""
---

# 用模板创建 Agent 快了很多：实测从 25 秒以上降到 3 到 6 秒

## 核心宣传点

从预置模板创建 Agent 以前要在请求里现场上传技能、现场发起运行环境构建，等待时间很长。现在改成复用不可变的共享技能锚点和已经预构建好的运行环境。在真实预发环境做的本地 HTTP 测试里，Amazon Analyst 的创建时间从大约 25 到 29 秒降到 2.8 到 5.7 秒（两次采样，不代表生产环境的延迟承诺）。配套加了离线的准备、校验、发布链路，带不可变运行时绑定、注册表回读和发布 CAS；运行环境的资源规格跟随账号套餐，预发环境的 Pro 环境按 4 核 4 GiB 验证。离线校验复用原有的来源校验逻辑，负载完整性、绑定与配置检查、可变字段校验和模型权限检查都保留，普通创建、分享和编辑路径的完整校验一律不变。模板工作区里引擎原生的技能目录软链保持不变，修复工具会新建不可变模板和辅助技能版本，不覆盖旧的。

## 分级

- 内部：P0
- 外部：A
- toB 相关：否
- 发布状态：已随正式 release 上线

## PR 说明

## Summary

Fixes #3922. Creating an Agent from a prepared template now reuses immutable shared Skill pins and a prebuilt Environment instead of uploading Skills and initiating an Environment build in the request. Local HTTP tests against real staging reduced Amazon Analyst creation from about 25–29 seconds to 2.8–5.7 seconds (two samples, not a production latency guarantee).

- Add offline prepare/verify/publish support with immutable runtime bindings, registry readback and publication CAS. Runtime resource class follows the account plan; staging Pro Environments were verified at 4 CPU / 4 GiB.
- Reuse offline source validation while retaining payload integrity, binding/configuration checks, mutable-field validation and model access checks. Ordinary creation, sharing and editing retain their existing full validation.
- Preserve Engine's native `.agents/skills -> /skills` link in the template workspace helper. The repair utility creates a new immutable template and helper Skill version, preserving existing Agents and other resource pins.

## Root cause

Template creation synchronously repeated source scans, uploaded each template Skill and waited on Environment preparation. After moving resource preparation offline, three full source scans still dominated request time. The converted template helper also rejected the native Skill link already created by Engine, preventing workspace initialization.

## Test plan

- [x] 481 template / Agent development regressions passed during implementation.
- [x] Independent branch code review: no actionable findings; 109 targeted tests passed.
- [x] Helper repair and template suites: 54 tests passed, including native/legacy/absent aliases, repeated initialization and conflict preservation.
- [x] Ruff, formatting, backend Pyright, import-linter and offline-script Pyright passed; push gate runs changed-surface checks.
- [x] Real staging HTTP + ACP + Mattermost + ACS + Engine + E2B validation using the authorized test account. Latest repaired-template sample: create 5.815s, idempotent replay 0.250s; helper ran twice with exit 0, preserved the native link and user profile, and the run succeeded.
- [x] Prepared/published eight repaired staging templates; catalog remains nine including unaffected Deco. Exact registry manifests and unchanged old sources/bindings were independently read back.

## Rollout and validation limits

Backend-only change; no Engine change or frontend deployment required. Prepare and verify production template runtime bindings and required resource-class builds before enabling this backend path for the production catalog. Templates without a valid prepared binding fail closed. Production data and deployments have not been changed by this work.

Existing Agents retain their previous pinned versions. Real repaired-template business execution covered Amazon Analyst; the other seven received source-layout checks plus offline registry verification. Browser UI, cross-account sharing/editing and production preflight were not rerun in this task.

Design and detailed receipts: [offline runtime spec](docs/superpowers/specs/2026-09-29-template-offline-runtime.md).

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `e223aebf96cae97bb2042d0cfa66dd076411e22a`
- PR: #3925
- 作者：kaka-srp
- 日期：2026-09-29T08:22:18Z

### Commit Message

```
fix(agents): prepare template runtime offline and speed up creation (#3925)

## Summary

Fixes #3922. Creating an Agent from a prepared template now reuses
immutable shared Skill pins and a prebuilt Environment instead of
uploading Skills and initiating an Environment build in the request.
Local HTTP tests against real staging reduced Amazon Analyst creation
from about 25–29 seconds to 2.8–5.7 seconds (two samples, not a
production latency guarantee).

- Add offline prepare/verify/publish support with immutable runtime
bindings, registry readback and publication CAS. Runtime resource class
follows the account plan; staging Pro Environments were verified at 4
CPU / 4 GiB.
- Reuse offline source validation while retaining payload integrity,
binding/configuration checks, mutable-field validation and model access
checks. Ordinary creation, sharing and editing retain their existing
full validation.
- Preserve Engine's native `.agents/skills -> /skills` link in the
template workspace helper. The repair utility creates a new immutable
template and helper Skill version, preserving existing Agents and other
resource pins.

## Root cause

Template creation synchronously repeated source scans, uploaded each
template Skill and waited on Environment preparation. After moving
resource preparation offline, three full source scans still dominated
request time. The converted template helper also rejected the native
Skill link already created by Engine, preventing workspace
initialization.

## Test plan

- [x] 481 template / Agent development regressions passed during
implementation.
- [x] Independent branch code review: no actionable findings; 109
targeted tests passed.
- [x] Helper repair and template suites: 54 tests passed, including
native/legacy/absent aliases, repeated initialization and conflict
preservation.
- [x] Ruff, formatting, backend Pyright, import-linter and
offline-script Pyright passed; push gate runs changed-surface checks.
- [x] Real staging HTTP + ACP + Mattermost + ACS + Engine + E2B
validation using the authorized test account. Latest repaired-template
sample: create 5.815s, idempotent replay 0.250s; helper ran twice with
exit 0, preserved the native link and user profile, and the run
succeeded.
- [x] Prepared/published eight repaired staging templates; catalog
remains nine including unaffected Deco. Exact registry manifests and
unchanged old sources/bindings were independently read back.

## Rollout and validation limits

Backend-only change; no Engine change or frontend deployment required.
Prepare and verify production template runtime bindings and required
resource-class builds before enabling this backend path for the
production catalog. Templates without a valid prepared binding fail
closed. Production data and deployments have not been changed by this
work.

Existing Agents retain their previous pinned versions. Real
repaired-template business execution covered Amazon Analyst; the other
seven received source-layout checks plus offline registry verification.
Browser UI, cross-account sharing/editing and production preflight were
not rerun in this task.

Design and detailed receipts: [offline runtime
spec](docs/superpowers/specs/2026-09-29-template-offline-runtime.md).
```

来源：SerendipityOneInc/ecap-workspace @ e223aebf，PR #3925，作者 kaka-srp。
