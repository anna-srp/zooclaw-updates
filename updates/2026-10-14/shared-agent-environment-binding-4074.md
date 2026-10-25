---
title: "分享安装的 Agent 现在会带上作者自定义环境里的软件，不再缺东西"
type: "新功能"
priority: "高"
date: "2026-10-14"
status: "待审核"
channels: ""
---

# 分享安装的 Agent 现在会带上作者自定义环境里的软件，不再缺东西

## 核心宣传点

此前通过原生分享安装别人的 Agent 时，只存在于作者自定义环境镜像里的软件会丢失，接收方装完就少了关键依赖。现在分享会绑定已发布 Revision 中记录的那份确切软件模板，每个接收方都拿到独立的 Agent 和沙箱，不需要接收方自己开开关。实现上复用 Engine 已有的精确版本授权，并持久化已验证的发布者归属。凭据、频道、会话和沙箱私有文件在接收方之间仍相互独立。

## 分级

- 内部：P1
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## 备注

Project 作用域的分发仍不支持。生产盘点：14 个在架已发布 Agent 的发布版本均已有完整的 ID/版本固定值，四个非基础模板均可读且就绪。environment/binding.json 只是设置提交时选择模板的撰写机制，分享本身不要求它存在。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `5732ee0d68f4cbdc2fd3b53aba73a800d027ac95`
- PR: #4074
- 作者：kaka-srp
- 日期：2026-10-14T10:56:53Z

### Commit Message

```
feat(agents): preserve explicit shared environment bindings (#4074)

## Summary

Native shared installations lost software that was present only in an
author's custom Environment image. Sharing now binds the exact software
template recorded in the published Revision, with an independent Agent
and Sandbox for every recipient. There is no recipient share toggle and
no package-only rebuilding compatibility branch.

Reuse Engine's existing exact-version grants for org templates; global
templates use the global registry without a tenant grant. Persist
verified publisher ownership for later edits, copies and updates,
clearing stale ownership when the pin changes. Registry scope resolution
tries global only after a tenant 404, never another org or an
authorization/availability failure. Project-scope distribution remains
unsupported.

`environment/binding.json` is an authoring mechanism for selecting a
template during Settings commits; it is not required for sharing.
Credentials, channels, sessions and private Sandbox files stay
independent. Production inventory found 14 active published Agents and
56 share-install audit rows; all 14 published revisions already have
complete ID/version pins, and all four non-base templates are readable
and ready with matching declarations. No historic source rewrite is
needed.

The credential-free image is maintained in [Steward PR
#173](https://github.com/SerendipityOneInc/claw-steward/pull/173). This
backend must ship before selecting it through the new authoring source
path. No frontend or Engine deployment is required. Neither the
production backend nor the original Sherlock has been switched.

## Validation

- Astra independently reviewed the full implementation and fixes; the
global-registry regression and both ownership-lifecycle findings are
addressed. Subsequent test-isolation fixes also passed independent
review.
- Backend unit suite: 12,039 passed, 5 skipped; Ruff, format, Pyright
and import-linter passed. CI's missing-configuration failure was
isolated to a mocked installation test that still constructed a real
client; its corrected private-template pin assertions and 20 sharing
tests pass independently.
- Real staging Mongo/CSFLE, Redis, Engine and E2B exercised fresh share
installation, idempotent install replay, independent
runtimes/private-file isolation, fork followed by re-sharing, template
v1-to-v2 update with confirmation while another install retained v1, and
global-template share installation.
- Staging business code ran from this branch in an isolated subprocess
overlay, not a deployed HTTP service. Synthetic account eligibility and
dummy credentials were fixtures; no LLM turns or real customer
credentials were used. HTTP authentication, paid-model behavior and
production Sherlock diagnosis are not claimed by this smoke.
- All 11 disposable Agents from successful and earlier smoke attempts
were uninstalled and finalized through Engine's supported runtime
cleanup API. Independent PG verification found 11 deleted/stopped
runtimes and zero running Sandbox bindings (10 absent bindings).
Immutable template/grant history remains where Engine's retention guards
require it.

## Review disposition

The incremental CI Codex review still asks for the old package-only
rebuilding fallback. That assumption was explicitly superseded by the
requested product contract: Environment is a reusable template and every
share reuses the published exact pin. Astra independently reviewed this
revised contract and the full implementation, found the three previous
defects addressed, and found no remaining actionable defect. Published
production pins/readiness were inventoried before removing the old
behavior. Reintroducing the requested fallback would violate the agreed
uniform-template behavior.
```

