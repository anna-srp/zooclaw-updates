---
title: "feat(platform): deliver phase one project and API key management (#3812)"
type: "新功能"
priority: "高"
date: "2026-09-20"
status: "待审核"
channels: ""
---

# 开发者平台第一阶段：项目与 API Key 管理

## 核心宣传点

Developer Platform 第一期作为一个跨层功能整体交付：独立的 Platform User / Organization / Project / API Key 数据结构，通过 Clerk 会话校验并自动初始化组织与默认项目，Project 和 API Key 的管理接口通过 claw-interface 暴露，Platform 前端已接到真实接口。计费、用量统计、SDK 机器认证和 Work key 迁移留给后续阶段，第三期相关界面暂时置灰。

## 分级

- 内部：P0
- 外部：A
- 发布状态：已合并待发版

## PR 说明

## Summary

Deliver Developer Platform Phase 1 as one cross-layer feature:

- add isolated Platform User, Organization, Project, and API Key collections
- verify Clerk sessions and bootstrap the Organization/default Project context
- expose Project and API Key management APIs through claw-interface
- connect the Platform web app to the real API
- keep Billing, Usage, SDK machine authentication, and Work key migration deferred to later phases
- add Platform CI coverage and an operations handoff document

## Commit structure

1. `docs(platform)`: scope, API/table contract, and phased delivery plan
2. `feat(platform-backend)`: schema, repositories, Clerk auth, APIs, and backend tests
3. `feat(platform-web)`: management console, real API integration, disabled Phase 3 surfaces, and frontend tests
4. `chore(platform)`: CI and operations handoff

## Validation

- `bash scripts/verify-py.sh`
- 41 Platform backend unit/BDD tests
- Platform web lint and TypeScript typecheck
- 14 Platform web unit tests
- Platform Vite production build
- review-agent follow-up: no remaining findings

## Deferred / environment validation

This Draft is not a production-readiness claim. Before marking it ready:

- validate the real Clerk instance and Organization auto-provisioning policy
- validate deployed ingress and exact-origin CORS
- validate staging Atlas and CSFLE behavior
- confirm log redaction and rate-limit behavior in the deployed environment

Billing and Usage remain disabled and are explicitly Phase 3. Phase 1 API Keys are management records only; SDK machine authentication remains Phase 2.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `7153580de0f83117cfedf12ed185e833ab90146f`
- PR: #3812
- 作者：finn-srp
- 日期：2026-09-20T09:03:20Z

### Commit Message

```
feat(platform): deliver phase one project and API key management (#3812)

## Summary

Deliver Developer Platform Phase 1 as one cross-layer feature:

- add isolated Platform User, Organization, Project, and API Key
collections
- verify Clerk sessions and bootstrap the Organization/default Project
context
- expose Project and API Key management APIs through claw-interface
- connect the Platform web app to the real API
- keep Billing, Usage, SDK machine authentication, and Work key
migration deferred to later phases
- add Platform CI coverage and an operations handoff document

## Commit structure

1. `docs(platform)`: scope, API/table contract, and phased delivery plan
2. `feat(platform-backend)`: schema, repositories, Clerk auth, APIs, and
backend tests
3. `feat(platform-web)`: management console, real API integration,
disabled Phase 3 surfaces, and frontend tests
4. `chore(platform)`: CI and operations handoff

## Validation

- `bash scripts/verify-py.sh`
- 41 Platform backend unit/BDD tests
- Platform web lint and TypeScript typecheck
- 14 Platform web unit tests
- Platform Vite production build
- review-agent follow-up: no remaining findings

## Deferred / environment validation

This Draft is not a production-readiness claim. Before marking it ready:

- validate the real Clerk instance and Organization auto-provisioning
policy
- validate deployed ingress and exact-origin CORS
- validate staging Atlas and CSFLE behavior
- confirm log redaction and rate-limit behavior in the deployed
environment

Billing and Usage remain disabled and are explicitly Phase 3. Phase 1
API Keys are management records only; SDK machine authentication remains
Phase 2.
```

来源：SerendipityOneInc/ecap-workspace @ 7153580d，PR #3812，作者 finn-srp。