---
title: "上线 OpenAI 兼容模型网关：用登录态或平台 API key 就能直接调模型"
type: "新功能"
priority: "高"
date: "2026-10-23"
status: "待审核"
channels: ""
---

# 上线 OpenAI 兼容模型网关：用登录态或平台 API key 就能直接调模型

## 核心宣传点

以前要直接调用平台模型，客户端必须自己持有底层模型网关的密钥，实际上没法开放给用户。现在新增一组 OpenAI 兼容的透传接口：用用户登录态即可调用模型列表和对话补全，服务端自动附上调用者自己的计费档案密钥（档案还没有密钥时会自动完成一次计费初始化），密钥全程不下发；也可以用开发者平台的 API key 调用服务版接口，服务端附上组织付费密钥，和 Agent 运行时使用的是同一把。可选的组织标识请求头会在调用者并非该组织计费主体时直接拒绝，避免错记账单。等于把「拿平台身份直接当 OpenAI 端点用」这件事从做不到变成开箱可用。

## 分级

- 内部：P1
- 外部：S
- toB 相关：是
- 发布状态：已合并待发版

## 备注

Work 服务令牌在本次仍返回 404，由后续的 #4129 补齐。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `518b4e81be6305baa9ae9d2e711024bbc46eb87d`
- PR: #4128
- 作者：tim-srp
- 日期：2026-10-23T05:49:18Z

### Commit Message

```
feat(claw-interface): OpenAI-compatible LLM gateway for user JWTs and Platform API keys (#4128)

## Summary

An OpenAI-compatible pass-through to LiteLLM, so clients can call models
without holding a LiteLLM key. The key is attached server-side and is
never returned.

- `GET /llm/v1/models` and `POST /llm/v1/chat/completions` authenticate
with a **user JWT** and attach the caller's Billing Profile key. If the
profile has no key yet, billing initialization runs once. An optional
`X-ECAP-Org-Id` header rejects the call when the caller is not billed to
that org.
- `GET /service/v1/llm/models` and `POST
/service/v1/llm/chat/completions` authenticate with a **Platform API
key** (`zwp_live_`) and attach the organization's payer key through
`require_billing_key`, the same key Agents run with. Work service tokens
(`zct_`) get 404.
- Request bodies are restricted to public Chat Completions fields;
`api_key`, `api_base` and other routing overrides are rejected. Requests
are never retried. Upstream headers and error bodies are masked into
stable `llm.*` codes.
- LiteLLM handles provider adaptation; this service streams bytes
through unchanged.

The first consumer is the ZooWork desktop (`ecap-workforce`), which can
then take a Platform key instead of a LiteLLM key.

Docs: `services/claw-interface/docs/llm-gateway.md`.

## Test plan

- [x] `tests/unit/test_llm_gateway.py` and
`tests/unit/test_service_api_llm.py`
- [x] Full claw-interface unit suite: 12514 passed, 14 skipped
- [x] ruff format / ruff check / pyright clean on changed files
- [ ] Staging: call `/service/v1/llm/chat/completions` with a bound
`zwp_live_` key and stream a reply

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

