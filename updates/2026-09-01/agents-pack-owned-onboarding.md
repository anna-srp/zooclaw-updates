---
title: "Agent Pack 可以自带专属新手引导：装完 Agent 跑的是 Pack 作者写的开场流程"
type: "产品基础功能更新"
priority: "中"
date: "2026-09-01"
status: "待审核"
channels: "Discord+changelog"
---

# Agent Pack 可以自带专属新手引导：装完 Agent 跑的是 Pack 作者写的开场流程

## 核心宣传点

以前一个 Agent 装好之后的首次引导，走的是引擎侧一套通用流程，Pack 作者没法决定自己的 Agent 第一次见用户时说什么、先问什么。现在改成由 Pack 自己声明：Pack 清单里可以写 `onboarding.skill`，指定一个随 Pack 打包的引导技能，安装时平台会解析校验这个声明、把选择结果和解析状态随 Pack 一起快照下来，再把这个确切的技能注册进引擎，用 `onboarding: { skill_id }` 创建 Agent。

引擎侧默认不再跑任何通用引导，只跑创建者明确选中的那一个技能；没有声明引导的 Agent 就明确跳过，不会退回旧流程。Pack Test 在引导是显式声明、或属于遗留/未知情况时，会重新分配一个全新的引擎 Agent，避免复用已经跑完一次性引导的旧状态导致测不出效果。

跨仓库的契约文档也一并定稿：明确了「精确名称 + Pack 作用域」的选择规则、引擎为生命周期状态的唯一权威、失败即拒绝（fail-closed）的行为，以及上线顺序——引擎切换前必须先完成待创建 Agent 的渲染配置回填与审计，遇到遗留的固定引导技能有对应回滚处置方案；引擎还需拦截生命周期成功结束后同一条消息里的兄弟工具调用。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `6bbae276e4f0b4aa59ea325d8e71494abc6fc414`
- PR: #3610
- 作者: kaka-srp
- 日期: 2026-09-01T09:34:04Z

### Commit Message

```
feat(agents): install explicit pack onboarding (#3610)

## Summary

Install Pack onboarding as an explicit Engine skill selection instead of
relying on Engine's generic onboarding.

## Why

The Pack should own its onboarding playbook. Engine now defaults to no
onboarding and only runs the exact skill selected by the Agent creator.

## Changes

- Parse and validate `onboarding.skill` from Pack manifests.
- Snapshot the onboarding selection and resolution state with the
installed Pack.
- Register the exact bundled skill in Engine and create the Agent with
`onboarding: { skill_id }`.
- Keep Agents without a declared Pack onboarding explicitly skipped.
- Make Pack Test provision a fresh Engine Agent whenever onboarding is
explicit or legacy/unknown, avoiding reuse of an already-completed
one-shot onboarding state.
- Add the cross-repository design contract and focused tests.

## Testing

- `bash scripts/verify-py.sh` passed (ruff, format, pyright,
import-linter).
- 360 focused affected-surface tests passed during implementation.
- 212 focused tests passed after the service refactor.
- Pre-commit and pre-push quality/size gates passed.

## Risk & Rollback

Deploy after the companion Engine PR and before updated Pack assets.
Existing snapshots remain readable; legacy/unknown Pack Test runs fail
safe by provisioning a fresh Agent. Roll back the ECAP backend if Agent
creation rejects the new field.

## Release notes

Pack-defined onboarding now runs as the only onboarding playbook; Agents
without an onboarding declaration start normally without an Engine
identity wizard.

## Related

Design:
`docs/superpowers/specs/2026-09-01-explicit-agent-onboarding-contract.md`

Companion PRs:

+- Engine: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1071
- ECAP: https://github.com/SerendipityOneInc/ecap-workspace/pull/3610
- Pack: https://github.com/SerendipityOneInc/ecap-agent-pack/pull/253
```

### PR Body

```
## Summary

Install Pack onboarding as an explicit Engine skill selection instead of relying on Engine's generic onboarding.

## Why

The Pack should own its onboarding playbook. Engine now defaults to no onboarding and only runs the exact skill selected by the Agent creator.

## Changes

- Parse and validate `onboarding.skill` from Pack manifests.
- Snapshot the onboarding selection and resolution state with the installed Pack.
- Register the exact bundled skill in Engine and create the Agent with `onboarding: { skill_id }`.
- Keep Agents without a declared Pack onboarding explicitly skipped.
- Make Pack Test provision a fresh Engine Agent whenever onboarding is explicit or legacy/unknown, avoiding reuse of an already-completed one-shot onboarding state.
- Add the cross-repository design contract and focused tests.

## Testing

- `bash scripts/verify-py.sh` passed (ruff, format, pyright, import-linter).
- 360 focused affected-surface tests passed during implementation.
- 212 focused tests passed after the service refactor.
- Pre-commit and pre-push quality/size gates passed.

## Risk & Rollback

Deploy after the companion Engine PR and before updated Pack assets. Existing snapshots remain readable; legacy/unknown Pack Test runs fail safe by provisioning a fresh Agent. Roll back the ECAP backend if Agent creation rejects the new field.

## Release notes

Pack-defined onboarding now runs as the only onboarding playbook; Agents without an onboarding declaration start normally without an Engine identity wizard.

## Related

Design: `docs/superpowers/specs/2026-09-01-explicit-agent-onboarding-contract.md`

Companion PRs:

+- Engine: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1071
- ECAP: https://github.com/SerendipityOneInc/ecap-workspace/pull/3610
- Pack: https://github.com/SerendipityOneInc/ecap-agent-pack/pull/253

```

## 备注

需引擎侧配套版本按约定顺序上线后完全生效。
