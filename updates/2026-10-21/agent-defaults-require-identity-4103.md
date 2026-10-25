---
title: "修复：新建 Agent 不再默认挂上无权使用的知识库技能"
type: "Bug Fix"
priority: "高"
date: "2026-10-21"
status: "待审核"
channels: ""
---

# 修复：新建 Agent 不再默认挂上无权使用的知识库技能

## 核心宣传点

平台侧创建的 Agent 过去会默认带上 Work 知识库技能，但它的身份根本无法授权该技能，使用时必然失败。本次只在凭据激活或沙箱准备之前，对这一项隐式全局默认做对齐，显式绑定、固定版本、自定义技能和其他默认项都原样保留；已存在运行时绑定时，创建重放会保留用户后来的修改并继续完成凭据交接，不会关闭用户之后选择的知识库或清掉它的固定版本。同时移除了新建 Agent 的第一阶段灰度开关，所有创建入口都会申请运行时身份，幂等重试沿用首次持久化的模式。无新增设置项、接口、表结构或批量迁移。

## 分级

- 内部：P1
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## 备注

存量 Agent 仍需单独迁移；启动依赖既有环境变量、introspection key 与 MCP 地址。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `aeac09d07f3985b762f32c6692dea01e80db2571`
- PR: #4103
- 作者：kaka-srp
- 日期：2026-10-21T00:21:59Z

### Commit Message

```
fix(platform): align runtime defaults and require identity for new agents (#4103)

## Problem and change

Platform Agents received the default Work knowledge-base Skill even
though their identity cannot authorize it. Align only that implicit
global default before credential activation or Sandbox preparation,
using the existing Engine toggle. Preserve explicit bindings/pins,
custom Skills and other defaults. Once a runtime binding exists,
creation replays preserve later user edits and still resume credential
handoff; they cannot disable a later KB selection, clear its pin or fail
on a source-owned binding.

Remove the first-phase new-Agent rollout switch. All creation entry
points request runtime identity; idempotent retries keep the persisted
original mode, and existing Agents remain subject to explicit migration.
Startup requires the existing environment, introspection key and MCP
URL. No new settings, endpoint, schema or bulk migration.

## Validation

- 302 targeted tests passed across creation, persisted identity/binding,
caller overrides, Platform defaults/tenancy/payer, credential recovery
and startup configuration. Six new cases cover pending/active/revoked
replay and interruptions before defaults, before binding and after
binding. Four regressions fail on the unfixed source; all 11
default-capability tests pass on the fix.
- `verify-py.sh`, commit hooks and all eight import contracts passed.
- Local Astra reviewed all 34 changed files across the three PRs. Its
single P2 (replay overwriting later explicit Skills) is fixed in
`83e2ac48e`; targeted re-review closed it with no new findings and 20
tests passed. Initial independent CI 196 / Proxy 325 tests also passed.
Proxy and Skills had no findings requiring changes.
- All applicable GitHub checks passed after syncing main at `07b99c343`
(22 passed, 25 skipped), including full backend CI: 12,655 passed, 14
skipped, 89.60% coverage
([run](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/39450138439)).
Codex found no issues; Claude found no code defect and requested
release-precondition confirmation. Mandatory startup settings were
verified in staging/production; dev/preview was not inspected and
requires its own configuration preflight before deployment. Interrupted
default initialization and credential handoff are covered by the new
regressions.

## Delivery

The preceding `d48073feb` was directly published as
`service-v0.18.41-beta.runtimecapabilities.2` ([staging
run](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/39414740356)),
with the obsolete switch removed from staging
Vault/Secret/Deployment/process. Real model calls, published audio
scripts, private voice/speaker isolation, Work KB success and Platform
KB denial passed; all test resources were cleaned up.

The replay fix is now accepted against real staging Engine on
`07b99c343` (backend tree identical to Astra-reviewed `83e2ac48e`),
deployed as `service-v0.18.41-beta.runtimecapabilities.3`
([run](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/39450155667)).
Actual API replays preserve a later enabled KB and its persisted v2 pin;
source-owned Skills retain their 409 toggle guard while replay succeeds.
Platform/Work model replies, Sandbox opaque aliases and Proxy
authorization passed, with all test Agents/keys cleaned up.
Interrupted-create failure cases remain unit-tested rather than live
fault-injected. PR remains unmerged and no stock migration was applied.
Publish [Proxy
#218](https://github.com/SerendipityOneInc/ecap-proxy-service/pull/218)
before CI; [Skills
#298](https://github.com/SerendipityOneInc/ecap-skills/pull/298)
supplies documentation only and is deferred at the user's request; it is
not a runtime dependency. Existing-Agent/Session migration and
third-party consumers remain separate.
```

