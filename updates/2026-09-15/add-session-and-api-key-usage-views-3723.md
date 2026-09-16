---
title: "feat(billing): add Session and API key usage views (#3723)"
type: "新功能"
priority: "低"
date: "2026-09-15"
status: "待审核"
channels: ""
---

# feat(billing): add Session and API key usage views (#3723)

## 核心宣传点

## Summary

Billing now supports Session and Managed Agents API key views alongside account-wide Time usage. New Lago events carry the triggering session/key; ECAP reads the existing events, applies authorized scope before aggregation/pagination, preserves Decimal amounts, and explicitly marks incomplete scans. No new BG usage store or historical backfill.

- Managed API credentials establish producer attribution and `GET /service/v1/usage` is limited to the authenticated key. Web `GET /users/credits/usage/details` preserves team member visibility and revoked-key names.
- Session/API key views request exact attribution; historical/unattributed rows are hidden, and API key excludes non-API/shared usage. Time remains account-wide.
- Full cross-repo review fixed BSON UTC membership boundaries and retained the existing regional/catalog model display names in detail rows.

## Test plan

- Backend usage/access/events/model display/Service API: 40 tests passed, including an actual ASGI route with the BFF `cf-ipcountry` header and BSON round-trip membership dates.
- Existing aligned Time-window semantics are preserved at fixed cutoffs; 24h/7d/30d boundary and cross-view amount regressions passed (22 tests with the existing Time suite).
- Frontend UsageRecord, UsageDimensions, billing service: 31 tests passed.
- `verify-py.sh` and `verify-web.sh --no-test` passed; independent fix review passed.
- Real local/staging-backed acceptance already reconciled same-session K1/K2/K1, key self-query and cross-key denial, revocation, child Session, async image, and compute against Lago. Latest extended run: 12 events / 18.4145088888 credits with unchanged payer/cost.
- Final head `2b8de70aa` passed all applicable PR CI and final Codex review returned APPROVE / no findings. The final commit only completes cross-repo review documentation.
- Design, implementation and validation evidence are in `docs/superpowers/` and `docs/validation/2026-09-14-session-api-key-billing-*.md`.

## Dependencies and limits

[BG #71](https://github.com/SerendipityOneInc/billing-gateway/pull/71), [GCP #542](https://github.com/SerendipityOneInc/gcp-foundation/pull/542), [Proxy #196](https://github.com/SerendipityOneInc/ecap-proxy-service/pull/196), and [Engine #1437](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1437). Deploy consumers, then Engine migration/API/worker, then ECAP.

No added runtime configuration. Attribution is reporting metadata, not an authentication or tamper-proof audit credential. Existing charging credentials determine the payer. Shared agent compute stays shared; the new Proxy deployment/live acceptance remains explicitly deferred. This PR is not a production deployment or merge request.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `4164775572e91c5788f3c3e02e335a7c875c4c0e`
- PR: #3723
- 作者：kaka-srp
- 日期：2026-09-15T02:47:50Z

### Commit Message

```
feat(billing): add Session and API key usage views (#3723)

## Summary

Billing now supports Session and Managed Agents API key views alongside
account-wide Time usage. New Lago events carry the triggering
session/key; ECAP reads the existing events, applies authorized scope
before aggregation/pagination, preserves Decimal amounts, and explicitly
marks incomplete scans. No new BG usage store or historical backfill.

- Managed API credentials establish producer attribution and `GET
/service/v1/us
```
