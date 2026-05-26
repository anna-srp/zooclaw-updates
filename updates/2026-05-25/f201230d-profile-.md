---
title: "账户信息自动从 Profile 补全"
type: "产品基础功能更新"
priority: "低"
date: "2026-05-25"
status: "待审核"
channels: ""
---

# 账户信息自动从 Profile 补全

## 核心宣传点

账户和组织成员的邮件、姓名信息现自动从 Profile 补全，减少重复填写

## 原始内容

**仓库**: SerendipityOneInc/ecap-workspace  
**Commit**: f201230d48adc04cbc4418ea0164c03f8dee328b  
**作者**: bill-srp  
**日期**: 2026-05-25T08:02:58Z  

**Commit Message**:

```
feat(account): enrich account and org users from profiles (#1906)

Linear:
https://linear.app/srpone/issue/ECA-764/phase-1-backend-changes-enterprise-data-model-warm-pool-cross-service

## Summary
- Fill /account/me email and name from profile lookup when available
- Enrich org user list rows with profile email/name
- Tighten list-users response typing so internal billing fields cannot
leak

## Stack
Depends on #1905.

## Checks
- devcontainer: ruff check focused profile-enrichment files
- devcontainer: pyright focused profile-enrichment files
- devcontainer: pytest focused profile-enrichment unit suite (86 passed)
- size check: under budget
```

**PR Description**:

Linear: https://linear.app/srpone/issue/ECA-764/phase-1-backend-changes-enterprise-data-model-warm-pool-cross-service

## Summary
- Fill /account/me email and name from profile lookup when available
- Enrich org user list rows with profile email/name
- Tighten list-users response typing so internal billing fields cannot leak

## Stack
Depends on #1905.

## Checks
- devcontainer: ruff check focused profile-enrichment files
- devcontainer: pyright focused profile-enrichment files
- devcontainer: pytest focused profile-enrichment unit suite (86 passed)
- size check: under budget
