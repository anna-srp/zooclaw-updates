---
title: "feat(settings): support personal workspace conversion to Team (#3762)"
type: "新功能"
priority: "高"
date: "2026-09-20"
status: "待审核"
channels: ""
---

# 个人工作区可以自助升级为 Team

## 核心宣传点

个人工作区的所有者现在可以在 Settings > Organization > Convert to Team 里把现有工作区转成 Team：组织、成员关系、Agent 和数据全部保留，不需要重建。转换本身不购买付费套餐、也不发放 Team 钱包额度。只有拥有有效管理员成员身份的 owner 能操作；如果个人订阅还处于非终态（包括「到期后取消」），转换会被拦截。界面上加了确认弹窗和 Team 名称输入，成功后自动刷新账号缓存并切到 Team 导航。

## 分级

- 内部：P1
- 外部：A
- 发布状态：已上线

## PR 说明

## Issue

Closes #3759

## Summary

Personal workspace owners can convert their existing workspace to Team from Settings > Organization > Convert to Team. The same org, membership, Agents, and data are preserved; this does not purchase a paid plan or provision Team wallets.

- Add the typed public `POST /orgs/{org_id}/upgrade-to-team` endpoint, restricted to the owner with an active admin membership.
- Reuse `org_upgrade.upgrade_org_to_team`, with the strict self-service subscription policy rechecked under the existing transition lease. Any non-terminal personal subscription, including canceling at period end, blocks conversion.
- Add the confirmation dialog, Team name input, account cache refresh, and Team navigation after success.
- Reuse Billing v2 audit events for self-service conversion. Persist the started event before external changes; commit the success event and org CAS in one MongoDB transaction. Failure records share the correlation ID and identify the execution stage without storing raw exception text. Failure-audit errors preserve the original business error.

## Scope and failure boundaries

The maintainer explicitly approved reusing the existing audit infrastructure after discussing the audit review finding. This supersedes issue #3759's earlier exclusion of additional audit behavior for this PR. The staff API retains its existing default behavior.

There are no new wallet/payment-order eligibility checks, checkout mutex, automatic cancellation/refund, balance migration, Team billing provisioning, or request-idempotency mechanisms. No audit queue or automatic reconciliation job is introduced.

MongoDB guarantees that the local org conversion and success audit commit together. External Billing Gateway changes are outside that transaction, as in the existing conversion flow. If an external change succeeds before a later failure, the failure audit records the stage and unknown resulting state; it does not claim an external rollback. If failure-audit persistence is also unavailable, or the process exits mid-operation, the durable started event remains for manual investigation. Automated repair of these cases is not included.

## Validation

- [x] Backend focused audit/repository/route/conversion/subscription/CSFLE query-guard suite: 139 passed.
- [x] Final audit/repository tests after the metadata adjustment: 30 passed.
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright, and import contracts passed.
- [x] Function complexity and database return-contract checks passed.
- [x] Frontend full unit suite after merging main: 10,312 passed, 70 skipped, 1 todo; this audit change adds no frontend code.
- [x] Conversion-focused frontend tests: 31 passed; TypeScript and ESLint passed.
- [ ] Browser E2E and live Billing Gateway validation were not run.
- [x] Staging encrypted MongoDB validation passed on 2026-09-20 for code commit `305f5c5e6`: actual repository success commit, real audit-insert failure rollback, and CAS-miss behavior. Auto-encryption enabled; no bypass or plain client. All isolated fixtures cleaned (2 orgs, 1 audit; 0 remaining). [Environment, exact source hash, method, and results](https://github.com/SerendipityOneInc/ecap-workspace/blob/bb818c812/docs/staging-validation/2026-09-20-org-conversion-audit-csfle.md).




## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `ffcc39dab20b2b3c38ea982c4ff40e3450b9b691`
- PR: #3762
- 作者：finn-srp
- 日期：2026-09-20T05:25:22Z

### Commit Message

```
feat(settings): support personal workspace conversion to Team (#3762)

## Issue

Closes #3759

## Summary

Personal workspace owners can convert their existing workspace to Team
from Settings > Organization > Convert to Team. The same org,
membership, Agents, and data are preserved; this does not purchase a
paid plan or provision Team wallets.

- Add the typed public `POST /orgs/{org_id}/upgrade-to-team` endpoint,
restricted to the owner with an active admin membership.
- Reuse `org_upgrade.upgrade_org_to_team`, with the strict self-service
subscription policy rechecked under the existing transition lease. Any
non-terminal personal subscription, including canceling at period end,
blocks conversion.
- Add the confirmation dialog, Team name input, account cache refresh,
and Team navigation after success.
- Reuse Billing v2 audit events for self-service conversion. Persist the
started event before external changes; commit the success event and org
CAS in one MongoDB transaction. Failure records share the correlation ID
and identify the execution stage without storing raw exception text.
Failure-audit errors preserve the original business error.

## Scope and failure boundaries

The maintainer explicitly approved reusing the existing audit
infrastructure after discussing the audit review finding. This
supersedes issue #3759's earlier exclusion of additional audit behavior
for this PR. The staff API retains its existing default behavior.

There are no new wallet/payment-order eligibility checks, checkout
mutex, automatic cancellation/refund, balance migration, Team billing
provisioning, or request-idempotency mechanisms. No audit queue or
automatic reconciliation job is introduced.

MongoDB guarantees that the local org conversion and success audit
commit together. External Billing Gateway changes are outside that
transaction, as in the existing conversion flow. If an external change
succeeds before a later failure, the failure audit records the stage and
unknown resulting state; it does not claim an external rollback. If
failure-audit persistence is also unavailable, or the process exits
mid-operation, the durable started event remains for manual
investigation. Automated repair of these cases is not included.

## Validation

- [x] Backend focused
audit/repository/route/conversion/subscription/CSFLE query-guard suite:
139 passed.
- [x] Final audit/repository tests after the metadata adjustment: 30
passed.
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright, and import
contracts passed.
- [x] Function complexity and database return-contract checks passed.
- [x] Frontend full unit suite after merging main: 10,312 passed, 70
skipped, 1 todo; this audit change adds no frontend code.
- [x] Conversion-focused frontend tests: 31 passed; TypeScript and
ESLint passed.
- [ ] Browser E2E and live Billing Gateway validation were not run.
- [x] Staging encrypted MongoDB validation passed on 2026-09-20 for code
commit `305f5c5e6`: actual repository success commit, real audit-insert
failure rollback, and CAS-miss behavior. Auto-encryption enabled; no
bypass or plain client. All isolated fixtures cleaned (2 orgs, 1 audit;
0 remaining). [Environment, exact source hash, method, and
results](https://github.com/SerendipityOneInc/ecap-workspace/blob/bb818c812/docs/staging-validation/2026-09-20-org-conversion-audit-csfle.md).
```

来源：SerendipityOneInc/ecap-workspace @ ffcc39da，PR #3762，作者 finn-srp。