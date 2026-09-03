---
title: "飞书渠道升级：Agent 能直接读写飞书云文档、云盘和知识库"
type: "产品基础功能更新"
priority: "高"
date: "2026-09-02"
status: "待审核"
channels: "站内弹窗+Use Case+Discord+changelog"
---

# 飞书渠道升级：Agent 能直接读写飞书云文档、云盘和知识库

## 核心宣传点

接了飞书渠道的托管 Engine Agent，现在不只是「在飞书里聊天」，还能直接操作飞书文档本身：新增一组原生的飞书文档能力，覆盖云文档（Docx）读写与结构编辑、云盘文件与文件夹管理、知识库/Wiki 节点浏览，以及文档权限管理。这些能力以托管 Skill 的形式随渠道能力自动下发到 Agent，不需要你自己去配 API、贴 Token 或装第三方插件。

权限管理这一项按账号能力开关控制：只有当该 Agent 聚合出的 `feishu.permission_admin_available` 为真时才会下发对应技能，Web 端可以在飞书渠道设置里单独开关「权限管理」，并能分别看到能力同步状态和 Provider 连接状态两层信息。对外只暴露这一个专门的权限字段作为可写入口，原始 `config.tools` 被明确拒绝，实际存储的 `tools.perm` 由 ACS 统一持有，避免手工改配置把状态改乱。

架构上把「事实来源 / 期望能力 / 已生效的 Engine 状态」拆成三层独立建模，引擎侧下发的技能用 `managed_by='capability'` + `installed_by='agent-channel-service'` 标识，方便与用户自己安装的技能区分。当前版本明确是「渠道驱动」的：能力跟着已连接的飞书渠道走，纯工具模式（不连渠道也能用飞书文档工具）需要另一套 Provider 账号绑定模型，作为后续迭代。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `cb3e690218ff0a553970cdbebb2b3a41c0e2f72d`
- PR: #3605
- 作者: kaka-srp
- 日期: 2026-09-02T02:46:08Z

### Commit Message

```
feat(channels): expose Feishu document capabilities (#3605)

## Linear

None — this cross-repository implementation was approved without a
Linear issue.

## Summary

- Add the reviewed design for channel-backed native Feishu/Lark document
tools on managed Engine v2 Agents.
- Add claw-interface request/projection support for account-level
`permission_admin_enabled`, Agent-level capability sync, and
account-level Provider status.
- Add Web controls and separate sync/provider status presentation for
Engine Feishu channels.
- Make the dedicated permission field the only public mutation surface;
raw `config.tools` is rejected and ACS owns the stored `tools.perm`
block.

## Review decisions implemented

- Model source fact, desired capability, and applied Engine state as
separate layers.
- Keep v1 explicitly channel-backed; tool-only mode is a follow-up that
requires a separate Provider account/binding model.
- Aggregate `permission_admin_available` at Agent scope without using it
to authorize a selected account.
- Identify Engine-owned Skills with `managed_by='capability'` plus
`installed_by='agent-channel-service'`.
- Split capability sync state from per-account Provider scope/approval
state.

## Related PRs

- Engine contract, capability endpoint, and runner:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1078
- ACS execution and reconciliation:
https://github.com/SerendipityOneInc/agent-channel-service/pull/103
- Managed Skills:
https://github.com/SerendipityOneInc/ecap-skills/pull/272

## Validation

- `bash scripts/verify-py.sh` passed.
- Ownership/projection targeted backend suite: 126 passed.
- Web TypeScript and targeted ESLint passed.
- Web targeted suites: 203 passed, 69 skipped.
- Push-time changed-surface verification passed.
- Engine `verify:quick`: light tier 2785 passed, 2 skipped; heavy tier
1814 passed.
- ACS TypeScript, oxlint, build, and targeted unit/contract suites
passed.
- Skills repository linter passed with only 12 unrelated pre-existing
warnings.
- ACS PostgreSQL integration suite is present but was skipped locally
because `TEST_DATABASE_URL` is not configured.
- Staging Feishu/Lark end-to-end validation remains a rollout gate.

## Rollout dependencies

1. Merge Engine and publish `@zooclaw/channel-tools-contract@0.1.0`.
2. Refresh the ACS lockfile from the registry, then merge/deploy ACS
feature-off.
3. Merge and publish the managed Skills.
4. Enable Staging reconciliation, run dry-run backfill, and complete
Feishu/Lark E2E acceptance before Production.
```

### PR Body

```
## Linear

None — this cross-repository implementation was approved without a Linear issue.

## Summary

- Add the reviewed design for channel-backed native Feishu/Lark document tools on managed Engine v2 Agents.
- Add claw-interface request/projection support for account-level `permission_admin_enabled`, Agent-level capability sync, and account-level Provider status.
- Add Web controls and separate sync/provider status presentation for Engine Feishu channels.
- Make the dedicated permission field the only public mutation surface; raw `config.tools` is rejected and ACS owns the stored `tools.perm` block.

## Review decisions implemented

- Model source fact, desired capability, and applied Engine state as separate layers.
- Keep v1 explicitly channel-backed; tool-only mode is a follow-up that requires a separate Provider account/binding model.
- Aggregate `permission_admin_available` at Agent scope without using it to authorize a selected account.
- Identify Engine-owned Skills with `managed_by='capability'` plus `installed_by='agent-channel-service'`.
- Split capability sync state from per-account Provider scope/approval state.

## Related PRs

- Engine contract, capability endpoint, and runner: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1078
- ACS execution and reconciliation: https://github.com/SerendipityOneInc/agent-channel-service/pull/103
- Managed Skills: https://github.com/SerendipityOneInc/ecap-skills/pull/272

## Validation

- `bash scripts/verify-py.sh` passed.
- Ownership/projection targeted backend suite: 126 passed.
- Web TypeScript and targeted ESLint passed.
- Web targeted suites: 203 passed, 69 skipped.
- Push-time changed-surface verification passed.
- Engine `verify:quick`: light tier 2785 passed, 2 skipped; heavy tier 1814 passed.
- ACS TypeScript, oxlint, build, and targeted unit/contract suites passed.
- Skills repository linter passed with only 12 unrelated pre-existing warnings.
- ACS PostgreSQL integration suite is present but was skipped locally because `TEST_DATABASE_URL` is not configured.
- Staging Feishu/Lark end-to-end validation remains a rollout gate.

## Rollout dependencies

1. Merge Engine and publish `@zooclaw/channel-tools-contract@0.1.0`.
2. Refresh the ACS lockfile from the registry, then merge/deploy ACS feature-off.
3. Merge and publish the managed Skills.
4. Enable Staging reconciliation, run dry-run backfill, and complete Feishu/Lark E2E acceptance before Production.

```

- 仓库: SerendipityOneInc/ecap-skills
- SHA: `d54fd1c60a8f59e92ad16d4a5e2cb92c85797bfc`
- PR: #272
- 作者: kaka-srp
- 日期: 2026-09-02T02:55:35Z

### Commit Message

```
feat(feishu): add managed document skills (#272)

## Linear

None — this cross-repository implementation was approved without a
Linear issue.

## Summary

- Add managed Skills for native Feishu Docx, Drive, Wiki, and permission
administration workflows.
- Gate the permission-management Skill on the Agent aggregate
`feishu.permission_admin_available` capability.
- Keep Provider execution and account-level authorization in ACS.

## Related work

- Design and ECAP integration:
https://github.com/SerendipityOneInc/ecap-workspace/pull/3605
- Engine contract/runner:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1078
- ACS execution/reconciliation:
https://github.com/SerendipityOneInc/agent-channel-service/pull/103

## Validation

- Repository Skill linter passed.
- The linter reports only 12 pre-existing warnings unrelated to these
Skills.

## Release order

Keep this PR in draft until the Engine contract and ACS execution path
are reviewed. Publish the Skills before enabling Staging reconciliation.
```

### PR Body

```
## Linear

None — this cross-repository implementation was approved without a Linear issue.

## Summary

- Add managed Skills for native Feishu Docx, Drive, Wiki, and permission administration workflows.
- Gate the permission-management Skill on the Agent aggregate `feishu.permission_admin_available` capability.
- Keep Provider execution and account-level authorization in ACS.

## Related work

- Design and ECAP integration: https://github.com/SerendipityOneInc/ecap-workspace/pull/3605
- Engine contract/runner: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1078
- ACS execution/reconciliation: https://github.com/SerendipityOneInc/agent-channel-service/pull/103

## Validation

- Repository Skill linter passed.
- The linter reports only 12 pre-existing warnings unrelated to these Skills.

## Release order

Keep this PR in draft until the Engine contract and ACS execution path are reviewed. Publish the Skills before enabling Staging reconciliation.

```


## 备注

跨仓改动：ecap-skills#272 提供托管技能，ecap-workspace#3605 提供 ECAP 侧接入与 Web 控制，另配套 zooclaw-engine#1078（契约/runner）与 agent-channel-service#103（执行与对账）。上线顺序为 Engine → Skills → ACS，需按序部署后完全生效。
