---
title: "新增面向企业团队钱包的后台积分发放接口，重复提交不会重复到账"
type: "后端功能"
priority: "高"
date: "2026-10-10"
status: "待审核"
channels: ""
---

# 新增面向企业团队钱包的后台积分发放接口，重复提交不会重复到账

## 核心宣传点

claw-interface 新增通用内部发放接口 POST /internal/orgs/{org_id}/credits，运营可向已存在的企业团队钱包发放积分，同一请求重复调用不会重复到账。沿用现有 SRP 员工加管理员鉴权，校验配置 business 与目标组织创建者是否一致、操作人是否为生效中的组织管理员；积分必须为正整数，payload 不可变。发放走现有权益流水与团队充值钱包，不发个人钱包、不绕过付费门槛、不伪造支付订单。相比初版去掉了四个 Workforce 专用 API 与企业映射表，映射和兑换码交由 Workforce 侧负责。

## 分级

- 内部：P1
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## 备注

网关结果不明时「失败即停」：认领后不会自动重派，返回 409 grant.reconciliation_required 且兑换码保持占用，必须由运营人工对账后处理。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `0534daf5c3a83e71ff5b3a8a5e3817283a14cb98`
- PR: #4047
- 作者：tim-srp
- 日期：2026-10-10T07:37:43Z

### Commit Message

```
feat: add idempotent administrative org credit grants (#4047)

## Summary

Revised per requested minimal architecture: Workforce owns enterprise
mapping, member orchestration, credit codes, admin-only redemption and
UI. Claw-interface adds one generic staff-admin grant endpoint targeting
an existing team wallet:

`POST /internal/orgs/{org_id}/credits`

This forward revision removes the original four Workforce-specific APIs,
service-token setting, enterprise mapping schema, and special
membership/billing changes. Existing
account/org/invite/join/agent/balance behavior remains unchanged. No
payment order or bank record is fabricated.

## Safety and behavior

- Existing SRP staff + admin authentication; validates configured
business against target creator and active org-admin actor.
- Strict positive integer credits; immutable payload and
business/org/key namespace.
- Existing entitlement ledger and team-topup wallet fulfillment, no
personal-wallet grant or paid subscription gate.
- Atomic pending→granting claim, one dispatch winner, stable completed
receipts.
- **Unknown gateway/finalization outcome fails closed:** no automatic
redispatch after claim; `409 grant.reconciliation_required`, code stays
reserved. Operator reconciliation is required for stranded grants. No
claim of automatically recoverable exactly-once delivery across process
failures.
- Receipt contains no balance: balance refresh is separate and cannot
invalidate grant success.

## Integration contract

[Revised complete
contract](docs/superpowers/specs/2026-10-10-workforce-enterprise-credits.md)
lists endpoint schemas/errors, Workforce W1–W9, existing API sequence
and recovery requirements.

Existing reusable flow has explicit constraints: verified email
invitation, existing default main Agent on join, personal-org migration
confirmation/paid-plan eligibility, model/metering prerequisites,
existing rounded balance response. Original
no-default-agent/silent-membership-upsert/phone-only promises are **not
implemented** by this narrowed change. Backend staff JWT is broad
privilege, not business-scoped machine auth.

## Verification

- Final unit suite: **11,891 passed, 5 skipped**, 4 warnings (99.94
seconds).
- Focused org/invite/billing/business/auth/grant suite: **198 passed**.
- `scripts/verify-py.sh`: ruff, format, pyright and all 8 import
contracts passed.
- Parent independent review and remote CI are still pending; native
implementation/review fallback was disclosed because Claude Fable quota
is unavailable. No claim of a fresh Claude review for this rewrite.

## Release boundary

Draft; no deployment, merge, Vault/token changes or live billing
requests. Staging encrypted-Mongo CAS, actual LLM/tool/sandbox shared
debits, model bootstrap, member Mattermost behavior, zero-balance errors
and operational reconciliation still require live acceptance. Unit mocks
do not prove these boundaries.

---------

Co-authored-by: Claude Fable 5.1 <noreply@anthropic.com>
```

