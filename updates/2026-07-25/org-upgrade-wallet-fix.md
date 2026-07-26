---
title: "修复组织升级时的钱包重复配置问题"
type: "Bug Fix"
priority: "中"
date: "2026-07-25"
status: "待审核"
channels: ""
---

## 核心宣传点

个人组织升级为团队组织时不再错误地重新创建钱包，已有的订阅和充值钱包信息保持不变，升级流程只做计费模式转换，避免了升级过程中的账务异常。

## 原始内容

- **仓库**: SerendipityOneInc/ecap-workspace
- **SHA**: `9050e66efd1756ed9fcf45ed2523cb6c00ff9003`
- **PR**: #3070
- **作者**: bill-srp | **日期**: 2026-07-25T03:54:29Z

### Commit Message
```
fix(org): skip wallet provisioning during org upgrade (#3070)

## Summary
- stop looking up or creating wallets when upgrading a personal org to a
team org
- leave existing `wallet_subscription_id` and `wallet_topup_id` values
untouched by removing them from the upgrade CAS contract
- keep the existing billing-mode conversion, Mattermost repair, tests,
and design documents aligned with the new behavior

## Root cause
The upgrade flow reused wallet provisioning behavior from fresh team-org
creation. Upgrading an existing org should only convert its existing
billing team to business mode; wallet setup belongs to the later
plan-purchase flow.

## Test plan
- [x] `pytest tests/unit/test_org_service.py tests/unit/test_org_repo.py
tests/unit/test_routes_internal_orgs.py
tests/unit/test_internal_users_orgs.py -q` — 64 passed
- [x] `bash scripts/verify-changed.sh` — ruff, format, pyright, and
import-linter passed
- [x] pre-commit and pre-push hooks passed
- [ ] Local BDD execution was unavailable because MongoDB was not
running; CI remains authoritative for the BDD scenario
```

### PR Body
```
## Summary
- stop looking up or creating wallets when upgrading a personal org to a team org
- leave existing `wallet_subscription_id` and `wallet_topup_id` values untouched by removing them from the upgrade CAS contract
- keep the existing billing-mode conversion, Mattermost repair, tests, and design documents aligned with the new behavior

## Root cause
The upgrade flow reused wallet provisioning behavior from fresh team-org creation. Upgrading an existing org should only convert its existing billing team to business mode; wallet setup belongs to the later plan-purchase flow.

## Test plan
- [x] `pytest tests/unit/test_org_service.py tests/unit/test_org_repo.py tests/unit/test_routes_internal_orgs.py tests/unit/test_internal_users_orgs.py -q` — 64 passed
- [x] `bash scripts/verify-changed.sh` — ruff, format, pyright, and import-linter passed
- [x] pre-commit and pre-push hooks passed
- [ ] Local BDD execution was unavailable because MongoDB was not running; CI remains authoritative for the BDD scenario

```
