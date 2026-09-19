---
title: "feat(agents): configure per-Agent connectors, MCP and knowledge bases (#3802)"
type: "新功能上线"
priority: "高"
date: "2026-09-18"
status: "待审核"
channels: ""
---

# Agent 可以单独配置 Connector、MCP 和知识库了

## 核心宣传点

每个 Agent 现在都能在 Settings 页里单独勾选自己要用的 Connector、个人 MCP 服务和知识库，不再是全账号资源一锅端。新建的 Agent 默认不挂任何资源，老 Agent 在你第一次编辑某类资源之前保持原来的自动继承行为，不会被静默改掉。保存和撤销沿用设置页原有的 Save/Undo，失败重试和撤销都会先确认 Engine 的真实结果再收尾，不会出现"界面显示成功、实际没生效"。注意本次需要前端、Proxy 和 Engine 一起发布才完整生效；Main Agent 默认值和 Agent Pack 安装支持留到下一阶段。

## 分级

- 内部：P1
- 外部：A
- 发布状态：已合并待发版

## PR 说明

## Summary

Add per-Agent selection of Connectors, personal MCP servers, and named knowledge bases in the existing Settings page, using its shared Save/Undo flow. New Agents start with empty explicit selections; existing Agents retain dynamic legacy inheritance until a resource category is edited.

claw-interface owns one versioned resource policy store in the existing Mongo database. Engine application precedes activation; retries and Undo inspect the actual Engine result before finalizing or restoring pending settings. Proxy reads the active policy with existing account authentication and Agent identity. No new deployment settings, dedicated runtime credentials, or Proxy-to-claw-interface calls are introduced.

Default Main Agent and Pack installation support are outside phase 1. Full metrics and unfiled knowledge-source/index migration remain deferred. Includes regression fixes for pending-operation recovery and runtime resource references being incorrectly treated as source drift.

## Related PRs and rollout

- Engine: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1523
- Proxy: https://github.com/SerendipityOneInc/ecap-proxy-service/pull/202
- Deploy compatible Proxy and Engine support before enabling the new defaults in claw-interface. Both frontend and backend deployment are required for this PR.
- See `docs/agent-resource-bindings-rollout.md` and `docs/superpowers/specs/2026-09-18-agent-resource-bindings-simplification.md`.

## Validation

- After integrating latest main: 217 distinct targeted backend tests passed; 405 Agent frontend tests passed (nine fixture failures fixed and rerun), plus 15 avatar/mock-route tests.
- Backend ruff, format, pyright, import contracts and file-length checks passed. Frontend governance, TypeScript and ESLint checks passed; refreshed dependencies from the frozen lockfile after main added scheduling packages.
- Independent cross-review completed for the original regression fixes; related runtime tests are documented in the companion PRs.
- The first full CI run exposed four legacy fixture files missing the new resource initialization/revocation boundaries and cohort assertion. Updated only the fixtures, retaining initialization/revocation call assertions; 66 targeted tests pass locally. The 12 local BDD scenarios skip because no local test Mongo is running; CI provides the existing Mongo service for the full rerun.
- Final CI on `66bbb03231`: backend 11,383 passed / 5 skipped (89.53% coverage); frontend 10,263 passed / 70 skipped / 1 todo. All required checks, build and CodeQL passed. Review adjudication is recorded in the PR comments; human approval is still required.
- Integration with latest main retains shared-Agent write protection, inherited skill pins, exact environment revisions, avatar routes, and shared-link refresh feedback.
- Staging CSFLE activation/rollback compatibility was verified through the running local claw-interface environment and the actual encrypted client: initial activation, stale Revision/head rejection, idempotent replay, rollback after both real writes, retry, and revoke all passed. All 5 isolated fixture records were removed and zero remaining records verified. Detailed evidence is in the PR validation comment.
- No new browser or complete Engine/Sandbox end-to-end run during this PR preparation; the Mongo transaction result is separate from those paths.

## Size exception

The feature is slightly over the repository's 3,000-line threshold after exclusions. Use the existing `size-override` label to retain the recovery/compatibility regression tests and one coherent Settings/API/persistence change. No quality or test checks are waived.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `919e3644bdb4dfb90d91924c727a6412ab16b847`
- PR: #3802
- 作者：kaka-srp
- 日期：2026-09-18T11:42:48Z

### Commit Message

```
feat(agents): configure per-Agent connectors, MCP and knowledge bases (#3802)

## Summary

Add per-Agent selection of Connectors, personal MCP servers, and named
knowledge bases in the existing Settings page, using its shared
Save/Undo flow. New Agents start with empty explicit selections;
existing Agents retain dynamic legacy inheritance until a resource
category is edited.

claw-interface owns one versioned resource policy store in the existing
Mongo database. Engine application precedes activation; retries and Undo
inspect the actual Engine result before finalizing or restoring pending
settings. Proxy reads the active policy with existing account
authentication and Agent identity. No new deployment settings, dedicated
runtime credentials, or Proxy-to-claw-interface calls are introduced.

Default Main Agent and Pack installation support are outside phase 1.
Full metrics and unfiled knowledge-source/index migration remain
deferred. Includes regression fixes for pending-operation recovery and
runtime resource references being incorrectly treated as source drift.

## Related PRs and rollout

- Engine: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1523
- Proxy:
https://github.com/SerendipityOneInc/ecap-proxy-service/pull/202
- Deploy compatible Proxy and Engine support before enabling the new
defaults in claw-interface. Both frontend and backend deployment are
required for this PR.
- See `docs/agent-resource-bindings-rollout.md` and
`docs/superpowers/specs/2026-09-18-agent-resource-bindings-simplification.md`.

## Validation

- After integrating latest main: 217 distinct targeted backend tests
passed; 405 Agent frontend tests passed (nine fixture failures fixed and
rerun), plus 15 avatar/mock-route tests.
- Backend ruff, format, pyright, import contracts and file-length checks
passed. Frontend governance, TypeScript and ESLint checks passed;
refreshed dependencies from the frozen lockfile after main added
scheduling packages.
- Independent cross-review completed for the original regression fixes;
related runtime tests are documented in the companion PRs.
- The first full CI run exposed four legacy fixture files missing the
new resource initialization/revocation boundaries and cohort assertion.
Updated only the fixtures, retaining initialization/revocation call
assertions; 66 targeted tests pass locally. The 12 local BDD scenarios
skip because no local test Mongo is running; CI provides the existing
Mongo service for the full rerun.
- Final CI on `66bbb03231`: backend 11,383 passed / 5 skipped (89.53%
coverage); frontend 10,263 passed / 70 skipped / 1 todo. All required
checks, build and CodeQL passed. Review adjudication is recorded in the
PR comments; human approval is still required.
- Integration with latest main retains shared-Agent write protection,
inherited skill pins, exact environment revisions, avatar routes, and
shared-link refresh feedback.
- Staging CSFLE activation/rollback compatibility was verified through
the running local claw-interface environment and the actual encrypted
client: initial activation, stale Revision/head rejection, idempotent
replay, rollback after both real writes, retry, and revoke all passed.
All 5 isolated fixture records were removed and zero remaining records
verified. Detailed evidence is in the PR validation comment.
- No new browser or complete Engine/Sandbox end-to-end run during this
PR preparation; the Mongo transaction result is separate from those
paths.

## Size exception

The feature is slightly over the repository's 3,000-line threshold after
exclusions. Use the existing `size-override` label to retain the
recovery/compatibility regression tests and one coherent
Settings/API/persistence change. No quality or test checks are waived.
```

## 备注

发布状态：已合并待发版（尚未包含在任何 ecap-*-release tag 中，最新正式 release 为 ecap-v0.19.16-release）。

来源：SerendipityOneInc/ecap-workspace @ 919e3644，PR #3802，作者 kaka-srp。
