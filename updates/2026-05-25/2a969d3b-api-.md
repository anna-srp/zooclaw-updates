---
title: "企业账户 API 核心功能上线"
type: "新功能上线"
priority: "中"
date: "2026-05-25"
status: "待审核"
channels: ""
---

# 企业账户 API 核心功能上线

## 核心宣传点

企业账户注册和账户信息 API 正式上线，为企业版功能提供基础支撑

## 原始内容

**仓库**: SerendipityOneInc/ecap-workspace  
**Commit**: 2a969d3b9cf6b2aed29b64607d2f3fdb6afd8112  
**作者**: bill-srp  
**日期**: 2026-05-25T07:01:30Z  

**Commit Message**:

```
feat(account): add enterprise account API core (#1903)

Linear:
https://linear.app/srpone/issue/ECA-764/phase-1-backend-changes-enterprise-data-model-warm-pool-cross-service

## Summary
- Add /account registration and /account/me core response surface
- Add token-only registration auth dependency and account-backed auth
dependency
- Finalize warm-pool registration before falling back to normal account
upsert

## Split
This is PR 1 of the enterprise account stack. Follow-ups add BDD
coverage, org billing/invite behavior, and profile enrichment.

## Checks
- devcontainer: ruff check focused account files
- devcontainer: pyright focused account files
- devcontainer: pytest tests/unit/test_routes_account.py
- size check: under budget
```

**PR Description**:

Linear: https://linear.app/srpone/issue/ECA-764/phase-1-backend-changes-enterprise-data-model-warm-pool-cross-service

## Summary
- Add /account registration and /account/me core response surface
- Add token-only registration auth dependency and account-backed auth dependency
- Finalize warm-pool registration before falling back to normal account upsert

## Split
This is PR 1 of the enterprise account stack. Follow-ups add BDD coverage, org billing/invite behavior, and profile enrichment.

## Checks
- devcontainer: ruff check focused account files
- devcontainer: pyright focused account files
- devcontainer: pytest tests/unit/test_routes_account.py
- size check: under budget
