---
title: "计费可靠性提升：支付成功后自动重试授权并监控孤立订单"
type: "产品基础功能更新"
priority: "高"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# 计费可靠性提升：支付成功后自动重试授权并监控孤立订单

## 核心宣传点

修复了支付成功但权益未开通的问题：新增 Lago 失败自动重试机制和孤立订单监控报警，确保付款后权益及时到账。

## 原始内容

**Commit**: `edff7b86269967faa92498ca775f287a6552cb52`
**仓库**: ecap-workspace
**作者**: kaka-srp
**时间**: 2026-04-28T06:30:31Z

### 完整 Commit Message

```
feat(billing): retry Lago 5xx + orphan-entitlement monitor (ECA-572) (#1425)

## Summary

Two-layer defense for the silent revenue leak documented in
[ECA-572](https://linear.app/srpone/issue/ECA-572): customer paid
Stripe, claw-interface never granted entitlement, no alarm fires. Root
cause is a Lago internal Postgres deadlock between concurrent
\`subscribe\` and \`wallet_transactions\` calls on the same customer's
wallets — reachable on every paid upgrade.

- **P1 — Retry on Lago 5xx** in \`billing_client.subscribe\` and
\`billing_client.topup_wallet\`. 4 attempts (0.2/0.8/2.0s backoffs),
only on response status 500/502/503/504. Eliminates ~all
deadlock-induced abandonments because PG resolves the deadlock by
killing the loser transaction; the next attempt finds the rows free.
- **P2 — Orphan-entitlement monitor cron** at \`POST
/admin/cron/check-orphaned-entitlements\`. Detects \`status=paid AND
entitlement_granted!=True AND created_time<now-5min\` and pages
PagerDuty (deduped by \`order_id\`). Detection-only; does NOT
auto-reconcile.
- **Foundation — PagerDuty wrapper** at
\`app/services/pagerduty_client.py\`. Generic Events API V2 client;
empty integration key → no-op for local/CI. Never raises — alerting
failure must not propagate.

## Why retry, why no auto-reconcile

- Retry is safe on **5xx response** (definitive rollback signal — Lago
has no idempotency key but PG already killed the txn). Retry is **NOT
safe on ConnectError / ReadTimeout** because the request might have
committed; the orphan cron is the safety net for that case.
- Auto-reconciling from cron would require the same Stripe/MongoDB
context the webhook handler had. Getting that wrong risks duplicate
grants; doing it right is a followup.

## Files

| Layer | Files |
|---|---|
| PagerDuty wrapper | \`app/services/pagerduty_client.py\`,
\`tests/unit/test_pagerduty_client.py\` |
| Retry (P1) | \`app/services/billing_client.py\`,
\`tests/unit/test_billing_client.py\` |
| Orphan cron (P2) | \`app/cron/orphaned_entitlements.py\`,
\`tests/unit/test_orphaned_entitlements_cron.py\`,
\`app/database/orders_repo.py\`, \`tests/unit/test_orders_repo.py\` |
| Endpoint | \`app/routes/admin_cron.py\`,
\`tests/unit/test_admin_cron.py\` |
| Config | \`app/settings.py\` (\`PAGERDUTY_INTEGRATION_KEY\`) |
| Docs | \`docs/cron-triggers.md\` |

## Deployment requirement (NOT in this PR)

\`PAGERDUTY_INTEGRATION_KEY\` must be added to the prod k8s secret and
wired into \`claw-interface-deployment\`. Without it the cron will
detect orphans but pages will be silently dropped (a WARNING is logged
once at startup). See
\`services/claw-interface/kustomize/overlays/production/\`.

External cron scheduler must also be configured to call \`POST
/admin/cron/check-orphaned-entitlements\` every 5 minutes.

## Test plan

- [x] \`ruff check\` + \`ruff format --check\` clean
- [x] \`pyright\` clean
- [x] \`lint-imports\` — 8/8 contracts kept
- [x] All 6 \`scripts/ci-lint/\` guards pass (file length ≤500,
complexity ≤20, deptry, no-collection-strings, importlinter sync)
- [x] 102 unit tests pass across the impacted files: 14 PD wrapper + 13
retry + 16 orders_repo + 7 cron + 8 admin endpoint + 44 existing billing
client
- [x] Pre-commit hooks all pass
- [ ] Smoke test on staging: \`POST
/admin/cron/check-orphaned-entitlements\` returns 202 + cron-run record
visible in \`ecap-cron-runs\`
- [ ] Verify a synthetic 500 from BG triggers exactly 4 attempts in
staging logs

## Followups (separate work)

- Manually remediate \`ORD-20260427-F99576E7\` (\$200 ultra, customer
\`10c458c0-eef7-4ca9-8397-b230aceedea8\`) — refund vs grant decision is
outside this PR's scope.
- Run historical sweep since 4-1 for \`wallet_transactions\` 5xx +
orphan orders to size impact.
- File upstream Lago issue against \`Customers::RefreshWalletsService\`
for deterministic wallet lock order (eliminates deadlock for all
callers).
- Add auto-reconcile to the orphan cron once the manual remediation flow
is well-understood.
```

### PR #1425 完整描述

## Summary

Two-layer defense for the silent revenue leak documented in [ECA-572](https://linear.app/srpone/issue/ECA-572): customer paid Stripe, claw-interface never granted entitlement, no alarm fires. Root cause is a Lago internal Postgres deadlock between concurrent \`subscribe\` and \`wallet_transactions\` calls on the same customer's wallets — reachable on every paid upgrade.

- **P1 — Retry on Lago 5xx** in \`billing_client.subscribe\` and \`billing_client.topup_wallet\`. 4 attempts (0.2/0.8/2.0s backoffs), only on response status 500/502/503/504. Eliminates ~all deadlock-induced abandonments because PG resolves the deadlock by killing the loser transaction; the next attempt finds the rows free.
- **P2 — Orphan-entitlement monitor cron** at \`POST /admin/cron/check-orphaned-entitlements\`. Detects \`status=paid AND entitlement_granted!=True AND created_time<now-5min\` and pages PagerDuty (deduped by \`order_id\`). Detection-only; does NOT auto-reconcile.
- **Foundation — PagerDuty wrapper** at \`app/services/pagerduty_client.py\`. Generic Events API V2 client; empty integration key → no-op for local/CI. Never raises — alerting failure must not propagate.

## Why retry, why no auto-reconcile

- Retry is safe on **5xx response** (definitive rollback signal — Lago has no idempotency key but PG already killed the txn). Retry is **NOT safe on ConnectError / ReadTimeout** because the request might have committed; the orphan cron is the safety net for that case.
- Auto-reconciling from cron would require the same Stripe/MongoDB context the webhook handler had. Getting that wrong risks duplicate grants; doing it right is a followup.

## Files

| Layer | Files |
|---|---|
| PagerDuty wrapper | \`app/services/pagerduty_client.py\`, \`tests/unit/test_pagerduty_client.py\` |
| Retry (P1) | \`app/services/billing_client.py\`, \`tests/unit/test_billing_client.py\` |
| Orphan cron (P2) | \`app/cron/orphaned_entitlements.py\`, \`tests/unit/test_orphaned_entitlements_cron.py\`, \`app/database/orders_repo.py\`, \`tests/unit/test_orders_repo.py\` |
| Endpoint | \`app/routes/admin_cron.py\`, \`tests/unit/test_admin_cron.py\` |
| Config | \`app/settings.py\` (\`PAGERDUTY_INTEGRATION_KEY\`) |
| Docs | \`docs/cron-triggers.md\` |

## Deployment requirement (NOT in this PR)

\`PAGERDUTY_INTEGRATION_KEY\` must be added to the prod k8s secret and wired into \`claw-interface-deployment\`. Without it the cron will detect orphans but pages will be silently dropped (a WARNING is logged once at startup). See \`services/claw-interface/kustomize/overlays/production/\`.

External cron scheduler must also be configured to call \`POST /admin/cron/check-orphaned-entitlements\` every 5 minutes.

## Test plan

- [x] \`ruff check\` + \`ruff format --check\` clean
- [x] \`pyright\` clean
- [x] \`lint-imports\` — 8/8 contracts kept
- [x] All 6 \`scripts/ci-lint/\` guards pass (file length ≤500, complexity ≤20, deptry, no-collection-strings, importlinter sync)
- [x] 102 unit tests pass across the impacted files: 14 PD wrapper + 13 retry + 16 orders_repo + 7 cron + 8 admin endpoint + 44 existing billing client
- [x] Pre-commit hooks all pass
- [ ] Smoke test on staging: \`POST /admin/cron/check-orphaned-entitlements\` returns 202 + cron-run record visible in \`ecap-cron-runs\`
- [ ] Verify a synthetic 500 from BG triggers exactly 4 attempts in staging logs

## Followups (separate work)

- Manually remediate \`ORD-20260427-F99576E7\` (\$200 ultra, customer \`10c458c0-eef7-4ca9-8397-b230aceedea8\`) — refund vs grant decision is outside this PR's scope.
- Run historical sweep since 4-1 for \`wallet_transactions\` 5xx + orphan orders to size impact.
- File upstream Lago issue against \`Customers::RefreshWalletsService\` for deterministic wallet lock order (eliminates deadlock for all callers).
- Add auto-reconcile to the orphan cron once the manual remediation flow is well-understood.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
