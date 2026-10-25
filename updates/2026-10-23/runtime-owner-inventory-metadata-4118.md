---
title: "修复：运行时凭据下资产清点技能拿不到归属者与账号信息"
type: "Bug Fix"
priority: "高"
date: "2026-10-23"
status: "待审核"
channels: ""
---

# 修复：运行时凭据下资产清点技能拿不到归属者与账号信息

## 核心宣传点

换用不透明运行时凭据后，既有的产品资产清点技能无法再支撑归属者选择器和账号清点，同时又要保留用户显式选定的资源。本次在 Agent 列表/详情、渠道、日程和会话这几个既有查询接口上新增单一的元数据视图：请求时会校验有效的 Work 主体、已生效投影、当前活跃绑定以及归属者与组织成员身份，然后只返回技能实际用到的字段，其中元数据列表提供权威的归属者标识字符串和账号邮箱。普通查询仍维持原有的旧版限制，登录态请求即使带上元数据参数也返回原有结构；运行时元数据会省略日程的消息与投递结果、渠道密钥与能力、会话标题等无关字段。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `21d1f7a24b83c26cc5a76636d06883705d321aa0`
- PR: #4118
- 作者：kaka-srp
- 日期：2026-10-23T06:55:49Z

### Commit Message

```
fix(agents): preserve runtime owner inventory metadata (#4118)

Opaque runtime credentials cannot support the existing product inventory
Skill's owner selector and account inventory while retaining explicit
resource selections. Add a single `metadata=true` view to the existing
Agent list/detail, channel, schedule and conversation GETs. It verifies
the live Work subject, applied projection, current active binding and
active owner/org membership, then returns only the fields the Skill
actually uses. The metadata list supplies authoritative string owner_uid
and account email.

Ordinary four GETs retain their legacy-only gate; JWT responses retain
their original DTO even with the metadata query. Runtime metadata omits
schedule message/spec/delivery/outcome, channel secrets/capabilities,
and conversation title/body/preview. Conversations preserve the existing
chat-only query; build and preview sessions remain excluded. Existing
owner/org target checks remain, and runtime GET list cannot provision an
Agent. No new endpoint, policy model, login capability or mutation is
added.

Validation: 169 related tests pass; full backend Ruff, formatting,
Pyright app/tests and eight import contracts pass. Feature staging at
service-v0.18.45-beta.runtimeinventory.1 verified real public TLS
requests: explicit/legacy own+sibling metadata, foreign-owner/org 404,
ordinary explicit 403, context spoof rejection, nonempty
schedule/conversation redaction, original JWT field retention,
current-head mismatch rejection and revoked-credential 401. The official
Skill code also called this public staging API. No production release or
customer Skill/pin changes.

Related official consumer fix:
https://github.com/SerendipityOneInc/claw-steward/pull/175

## Local review and follow-up validation

Reviewed the complete PR against its main merge base, including
ownership/current-binding authorization, explicit versus legacy resource
selection, DTO redaction, ordinary JWT compatibility, and the real
service/repository call chains.

Resolved the prior conversation-contract finding: the original mock
returned build sessions even though the production query excludes them.
The runtime schema, defensive route filter, test expectations, and spec
now consistently describe the existing chat-only inventory. A new
HTTP-to-repository regression test checks the actual owner/Agent/purpose
query and limit for both runtime and JWT callers, including JWT field
retention with `metadata=true`. The database query and JWT
implementation are unchanged.

- Local regression: 229 tests passed across runtime inventory/reader,
Agent/channel/schedule/conversation routes, and conversation
repository/service tests. The tightened route regression failed before
the fix and passed afterward.
- Full backend static verification passed: Ruff check/format, Pyright
app/tests, and all eight import contracts.
- Targeted re-review of the fix found no remaining actionable findings.
- This follow-up was validated locally; the earlier staging evidence
above predates this follow-up. No new staging deployment, provider
calls, production data changes, or release was performed.
```

