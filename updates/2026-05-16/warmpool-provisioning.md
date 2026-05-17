---
title: "Bot 启动速度提升：预热池机制上线"
type: "产品基础功能更新"
priority: "中"
date: "2026-05-16"
status: "待审核"
channels: ""
---
# Bot 启动速度提升：预热池机制上线

## 核心宣传点
平台新增预热池机制，提前准备好账号资源，让你的 Bot 启动更快、响应更顺畅。

## 原始内容
**Commit**: 878e408637e4f0eb1de91c2d188533f0e388847d
**作者**: tim-srp
**日期**: 2026-05-16T15:29:11Z
**PR**: #1715

### Commit Message
Implement warm-pool provisioning in claw-interface (#1715)

## Summary
- add warm-pool repo, schema, account-service client, and provisioner
- add warm-pool cron/status endpoints and dedicated key-only auth
- finalize claimed warm-pool registrations in /users/create and add
coverage tests

## Testing
- pytest -W ignore::PendingDeprecationWarning
services/claw-interface/tests/unit/test_warm_pool.py
services/claw-interface/tests/unit/test_user_routes_coverage.py -q
- bash services/claw-interface/scripts/ci-lint/01-file-length.sh
- bash services/claw-interface/scripts/ci-lint/02-import-linter.sh

### PR Description
## Summary
- add warm-pool repo, schema, account-service client, and provisioner
- add warm-pool cron/status endpoints and dedicated key-only auth
- finalize claimed warm-pool registrations in /users/create and add coverage tests

## Testing
- pytest -W ignore::PendingDeprecationWarning services/claw-interface/tests/unit/test_warm_pool.py services/claw-interface/tests/unit/test_user_routes_coverage.py -q
- bash services/claw-interface/scripts/ci-lint/01-file-length.sh
- bash services/claw-interface/scripts/ci-lint/02-import-linter.sh
