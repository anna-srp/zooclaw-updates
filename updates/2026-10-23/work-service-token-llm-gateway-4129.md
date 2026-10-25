---
title: "Work 托管 Agent 密钥也能直连模型网关，按本人账户计费"
type: "新功能"
priority: "高"
date: "2026-10-23"
status: "待审核"
channels: ""
---

# Work 托管 Agent 密钥也能直连模型网关，按本人账户计费

## 核心宣传点

在上一条模型网关能力的基础上补齐一类凭据：此前在 Work 中创建的托管 Agent 密钥调用服务版模型接口会直接返回 404，无法从桌面端等场景直接调模型。现在这类令牌会绑定到对应成员自己的计费档案密钥，和该成员网页端使用的是同一把密钥、同一个付费主体；只有当成员当前所属组织与令牌所属组织一致时才放行，否则直接拒绝，确保一个令牌永远不会把账单记到别的组织头上。Platform 侧的 API key 行为不变，仍使用组织付费密钥。

## 分级

- 内部：P1
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## 备注

依赖 #4128 的网关能力，需一并发版。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `bc775898554a72788a7af478a8657d97d023368c`
- PR: #4129
- 作者：tim-srp
- 日期：2026-10-23T07:28:07Z

### Commit Message

```
feat(claw-interface): serve Work service tokens on the service-API LLM gateway (#4129)

## Summary

Follow-up to #4128. `/service/v1/llm/models` and
`/service/v1/llm/chat/completions` returned `404 service_api.not_found`
for `zct_` Work service tokens, so a managed-agent key created in
ZooWork Work could not call models directly (for example from the
ZooWork desktop).

- A `zct_` token now gets its bound member's own Billing Profile key
(`llm_gateway.resolve_billing_key`). That is the same key and payer as
the member's web usage and `/llm/v1`.
- The call is refused with `409 llm.billing_owner_mismatch` unless the
member's current organization is the token's organization, so a token
can never bill a different org.
- `zwp_live_` Platform keys are unchanged and keep the organization
payer key.

## Test plan

- [x] `tests/unit/test_service_api_llm.py`: a zct token uses the member
key; a member with no current org or a different org gets 409 before
LiteLLM is called
- [x] Full claw-interface unit suite: 12519 passed, 14 skipped
- [x] `scripts/ci-lint/*.sh`, ruff, pyright clean
- [ ] Staging: `GET /service/v1/llm/models` and a streamed completion
with a staging `zct_` token

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

