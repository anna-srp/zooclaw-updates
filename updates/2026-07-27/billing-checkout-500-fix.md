---
title: 修复结账/支付偶发 500 错误
type: Bug Fix
priority: 高
date: 2026-07-27
status: 待审核
channels: ""
---

## 核心宣传点

修复了一个会导致订阅结账失败的严重问题：此前生产环境的结账流程在创建支付时可能直接返回 500 错误、付款发起不了。现已修复，结账与支付创建恢复正常稳定。

## 原始内容

fix(billing): make checkout lease CSFLE-safe (#3073)

## Summary

- replace the CSFLE-incompatible checkout lease aggregation pipeline with classic atomic compare-and-set updates
- preserve stable lease timestamps for same-order retries and exclusion for competing orders
- add focused regression coverage for fresh claims, idempotent retries, release races, and active-owner conflicts

## Root cause

The subscription checkout lease used an aggregation-pipeline `find_one_and_update`. Production `crypt_shared 8.2.1` rejects that update shape with MongoDB error `31146` before the Antom provider call, causing `/antom/create-payment` to return HTTP 500.

## Validation

- `pytest -q tests/unit/test_user_repo.py tests/unit/test_billing_v2_order_requests.py tests/unit/test_antom_billing_v2_checkout.py` — 80 passed
- `bash scripts/verify-local.sh --py-static` — Ruff, format, Pyright, and import-linter passed
- pre-commit and pre-push repository gates passed
- staging Mongo/CSFLE probe reproduced `31146` with the old pipeline and confirmed the classic update succeeds
- staging race probe confirmed two concurrent owners produce exactly one winner
- all temporary staging test accounts were removed

## Scope

Only the checkout lease repository implementation and its unit tests are changed. No payment-provider calls, plan rules, frontend behavior, indexes, or other collections are modified.
