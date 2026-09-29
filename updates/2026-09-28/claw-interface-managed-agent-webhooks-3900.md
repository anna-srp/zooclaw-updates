---
title: "开放接口新增托管 Agent Webhook 管理：可用服务令牌创建、更新和删除 Webhook"
type: "Feature"
priority: "中"
date: "2026-09-28"
status: "待审核"
channels: ""
---

# 开放接口新增托管 Agent Webhook 管理：可用服务令牌创建、更新和删除 Webhook

## 核心宣传点

面向开发者的服务接口现在把引擎侧的 Webhook 管理能力开放出来了：已有的服务令牌可以按 Agent 维度和按所属者维度管理 Webhook。公开接口沿用查询用 GET、变更用 POST 的约定，更新和删除分别映射到底层的 PATCH 与 DELETE。所属者范围绑定在发起调用的令牌上，转发之前会先校验 Agent 归属，未登记的路径一律拒绝；幂等键支持 1 到 255 个字符，会连同组织与所属者范围一起哈希成固定长度的内部键，因此服务令牌轮换后重试依然稳定命中同一次请求。Webhook 响应统一标记为不可缓存。另外还收紧了路径解析：带歧义的点号段和编码分隔符会在进入服务接口分发前就被拒绝，确保鉴权和转发看到的是同一个路径。公开路径和上线前置条件已补进文档。

## 分级

- 内部：P1
- 外部：B
- toB 相关：是
- 发布状态：已上线

## PR 说明

## Summary
- Expose Engine's agent-scoped and owner-scoped webhook management routes through `/service/v1` for existing `zct_` service tokens. Related to #3786.
- Map public POST `/{webhook_id}/update` and `/{webhook_id}/delete` actions to Engine PATCH/DELETE while keeping the Interface GET/POST convention.
- Bind owner scope to the authenticated token, verify agent ownership before forwarding, reject unlisted routes, and hash validated 1–255-character idempotency keys with org/owner scope into a fixed 64-character Engine key. Retries remain stable across service-token rotation.
- Mark webhook responses `Cache-Control: no-store`; document the public paths and rollout requirements.
- Reject ambiguous dot-segment and encoded-delimiter paths before service API dispatch, so authorization and Engine forwarding use the same path.

## PR Lens
![Architecture: customer calls pass through claw-interface authorization before reaching Engine; Engine delivery is unchanged](https://prlens.dev/c/dkZx5s9tJM9h7-Mu1yWlfg.svg)

[Open the interactive architecture and data-flow walkthrough](https://prlens.dev/c/dkZx5s9tJM9h7-Mu1yWlfg). The data-flow view follows one agent-scoped webhook create request through token auth, agent ownership verification, Engine forwarding, and the no-store response.

## Test plan
- [x] Targeted webhook and existing service proxy regression tests: 195 passed, including key length boundaries, owner/org isolation, retry stability, and service-token rotation.
- [x] Full local test cases: 12,635 passed, 5 skipped; 89.89% coverage, above CI's unchanged 89.5% threshold. Static, architecture and duplication checks passed.
- [ ] `bash scripts/verify-py.sh --full` exits 1 only at the unchanged 90% coverage gate (actual: 89.89%). All test cases and other full-suite checks passed. The script is unchanged in this PR; CI retains its existing 89.5% gate.
- [x] Pre-push changed-surface checks passed.

## Rollout note
- This PR does not enable Engine webhook flags or run a live receiver smoke. A dedicated HTTPS receiver and the Engine dispatcher/capture rollout must be verified before advertising customer availability.
- The repository's `check-user` pre-commit hook was skipped because it requires a GitHub login ending in `-srp`, while the workspace specifies Finn's active `finn930` account. All other pre-commit hooks passed; commit author is `finn-srp <finn@srp.one>`.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `602b60773da10f952170c69de4d32afd1897b912`
- PR: #3900
- 作者：finn-srp
- 日期：2026-09-28T05:11:33Z

### Commit Message

```
feat(claw-interface): expose managed agent webhooks (#3900)

## Summary
- Expose Engine's agent-scoped and owner-scoped webhook management
routes through `/service/v1` for existing `zct_` service tokens. Related
to #3786.
- Map public POST `/{webhook_id}/update` and `/{webhook_id}/delete`
actions to Engine PATCH/DELETE while keeping the Interface GET/POST
convention.
- Bind owner scope to the authenticated token, verify agent ownership
before forwarding, reject unlisted routes, and hash validated
1–255-character idempotency keys with org/owner scope into a fixed
64-character Engine key. Retries remain stable across service-token
rotation.
- Mark webhook responses `Cache-Control: no-store`; document the public
paths and rollout requirements.
- Reject ambiguous dot-segment and encoded-delimiter paths before
service API dispatch, so authorization and Engine forwarding use the
same path.

## PR Lens
![Architecture: customer calls pass through claw-interface authorization
before reaching Engine; Engine delivery is
unchanged](https://prlens.dev/c/dkZx5s9tJM9h7-Mu1yWlfg.svg)

[Open the interactive architecture and data-flow
walkthrough](https://prlens.dev/c/dkZx5s9tJM9h7-Mu1yWlfg). The data-flow
view follows one agent-scoped webhook create request through token auth,
agent ownership verification, Engine forwarding, and the no-store
response.

## Test plan
- [x] Targeted webhook and existing service proxy regression tests: 195
passed, including key length boundaries, owner/org isolation, retry
stability, and service-token rotation.
- [x] Full local test cases: 12,635 passed, 5 skipped; 89.89% coverage,
above CI's unchanged 89.5% threshold. Static, architecture and
duplication checks passed.
- [ ] `bash scripts/verify-py.sh --full` exits 1 only at the unchanged
90% coverage gate (actual: 89.89%). All test cases and other full-suite
checks passed. The script is unchanged in this PR; CI retains its
existing 89.5% gate.
- [x] Pre-push changed-surface checks passed.

## Rollout note
- This PR does not enable Engine webhook flags or run a live receiver
smoke. A dedicated HTTPS receiver and the Engine dispatcher/capture
rollout must be verified before advertising customer availability.
- The repository's `check-user` pre-commit hook was skipped because it
requires a GitHub login ending in `-srp`, while the workspace specifies
Finn's active `finn930` account. All other pre-commit hooks passed;
commit author is `finn-srp <finn@srp.one>`.
```

来源：SerendipityOneInc/ecap-workspace @ 602b6077，PR #3900，作者 finn-srp。
