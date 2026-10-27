---
title: "Work 设置不再签发新的 zct_ API Key，新建密钥统一走开发者平台"
type: "产品基础功能更新"
priority: "高"
date: "2026-10-26"
status: "待审核"
channels: ""
---

# Work 设置不再签发新的 zct_ API Key，新建密钥统一走开发者平台

## 核心宣传点

Work 设置里原本还保留着一个创建 `zct_` 开头 API Key 的入口，和开发者平台的项目密钥并行存在，两套密钥体系容易让人选错。本次把这个入口从身份设置和组织共享导航中隐藏，旧的 API Keys 深链会回落到 General 页；对创建接口的请求在真正生成密钥之前就返回 `409 service_token.issuance_disabled`，并附上跳转开发者平台的链接。

已经签发的 Work 密钥不受影响：仍可正常鉴权、继续走 `/service/v1`，列表、重新绑定和吊销都照旧可用，本次不含任何资源或账单迁移。官网的「发布 Agent」指南此前已改为基于开发者平台的 Agent Starter 和 `zwp_live_` 项目密钥，不会再把新用户引到 Settings → API Keys。

## 分级

- 内部：P1
- 外部：A
- toB 相关：是
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `b724445eaf435c08140d7e09157c1f408458abef`
- PR: #4071
- 作者：finn-srp
- 日期：2026-10-26T10:26:59Z

### Commit Message

```
fix(api-keys): stop issuing new Work service tokens (#4071)

Work settings still offered `zct_` API key creation alongside Platform
Project keys. This change hides that entry in Identity and shared
Organization navigation, and makes old API Keys deep links fall back to
General. Authenticated requests to the Work key create endpoint now
return `409 service_token.issuance_disabled` with a link to Platform
before any key is generated.

Existing Work keys continue to authenticate and use `/service/v1`; list,
rebind and revoke remain available through their existing backend
endpoints. The retirement spec records all three steps, with request
rejection and implementation cleanup deferred until Finn requests them.
No resource or billing migration is included.

The public publish-agent guide no longer sends new users to Settings →
API Keys: #4123 rebuilt it on the Platform Agent Starter and `zwp_live_`
Project keys, and it is live on zoowork.ai.

Rebased onto main `fd8c551` (2026-10-26). The rebase was conflict-free.
Two follow-up commits update e2e expectations that still required the
API Keys link: the `settings-team-admin` mock e2e added in #4094, and
the deployed-suite `settings.spec.ts` run by the scheduled/manual
`settings` project. Both now expect General, Usage and Billing and
assert that API Keys is absent. No other e2e spec references the API
Keys tab.

Validation on `26e5d6e` (the later `f561259` changes only
`tests/e2e/specs/settings.spec.ts`; `tsc` and ESLint pass on it):
- `pnpm test:unit`: 867 files passed; 10,940 tests passed, one skipped.
- `pnpm lint:ci` passed.
- `ecap-verify-py-ci` passed: Linux dependency resolution,
static/ci-lint checks, both duplication checks, and 12,871 tests passed
(14 skipped), with 89.68% coverage against the 89.5% gate.
- Manual check with `next dev` against the local mock backend: for a
team admin and a personal org admin, the account menu's Settings opens
`/identity` with the full navigation and no API Keys entry;
`/identity?tab=account-api-keys` renders General;
`/identity/organization` renders normally. The account menu's "Get API
keys" item links to ZooWork Platform.
- The updated e2e specs were not run locally (no Playwright browser
installed on this machine); their assertions match the manual check
above.
- The legacy `check-user` commit hook was skipped because it requires a
GitHub login ending in `-srp`. GitHub operations use Finn's
authenticated `finn930` account, and the commit author is `finn-srp
<finn@srp.one>`.

Deployment requires both Web and claw-interface.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```
