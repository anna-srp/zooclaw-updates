---
title: "中国大陆网页端合规调整：个人账号暂停邮箱验证码登录，团队账号不受影响"
type: "产品基础功能更新"
priority: "高"
date: "2026-08-26"
status: "待审核"
channels: ""
---

# 中国大陆网页端合规调整：个人账号暂停邮箱验证码登录，团队账号不受影响

## 核心宣传点

网页端针对中国大陆访问做了第一期合规调整：从大陆 IP 访问时，个人账号暂时无法通过邮箱验证码进入，而拥有生效中的团队组织的账号不受任何影响，照常收码登录。同时，团队组织所在区域为中国大陆时，模型列表会按统一的区域展示配置显示名称；大陆以外的用户看到的模型名称和可用范围完全不变。本期仅覆盖网页端。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `ca35c19935e6bf3facc4f77cf7d1ae328cdfd25a`
- PR: #3508
- 作者: sam-srp
- 日期: 2026-08-26T08:38:24Z

### Commit Message

```
feat: add phase-one mainland web compliance (#3508)

## Summary

- restrict mainland China Web email OTP entry for personal accounts
while allowing users with an active Team organization
- add the organization region field and keep access eligibility
independent from model presentation
- apply CN-only model display overrides from the Flow Jobs managed
collection, hiding unconfigured models only for CN Team users
- preserve LiteLLM names and the full entitled model catalog outside CN
- prevent hidden regional models from reappearing or being saved through
the composer or Agent Builder
- add end-to-end regional compliance observability without logging
email, raw IP, full UID, or model/configuration content

## Meeting-aligned behavior

- mainland IP plus active Team organization: allow email OTP regardless
of organization region
- mainland IP plus personal or missing active Team organization: block
before sending OTP
- model white-labeling: controlled only by Team organization
`region_code` equal to `CN`
- no separate contracted-enterprise field and no coupling between
contract state and region display

## Regional compliance logging

- log normalized `CF-IPCountry`; missing values are `empty` and
malformed values are `invalid`
- log the final Web outcome: invalid request, personal blocked,
eligibility dependency error, OTP error, OTP sent, or Team allowed and
OTP sent
- log Organization `region_code` as configured; a missing legacy value
is `empty` with effective `CN`
- log invalid persisted Organization regions with masked UID and
Organization ID
- log model override configuration version, modification time,
declared/actual row counts, regional matches, invalid rows, duplicate
rows, missing active configuration, and invalid data shape
- log model catalog mode and entitled/override/visible counts, with a
warning for an empty catalog
- Flow Jobs executes outside this repository; this PR observes the
resulting Mongo sync document rather than duplicating its job logs

## Scope

Phase one is Web-only. It does not add iOS enforcement, session
enforcement for already logged-in users, domain migration, or HMAC
signing. It adds one server-only deployment secret,
`DOMESTIC_ACCESS_BFF_TOKEN`, shared by Web and claw-interface for the
pre-auth eligibility call.

## Deployment prerequisite

- configure `DOMESTIC_ACCESS_BFF_TOKEN` in the GitHub `staging` and
`production` Environment Secrets
- configure the matching per-environment value in the claw-interface
Vault path `srp/ecap/claw-interface/env`
- roll the claw-interface pods before deploying Web; the Web workflow
validates and injects the secret into the Cloudflare Worker

## Verification

- Claw Interface full suite: 9236 passed, 269 skipped
- deployment/authentication contract suite: 9 passed
- scoped Web verifier: 77 passed
- repository pre-commit and pre-push gates passed, including ESLint,
TypeScript, Ruff, Pyright, import contracts, dependency checks, and YAML
validation
- local end-to-end QA completed for CN and non-CN entry paths
```

### PR Description

```
## Summary

- restrict mainland China Web email OTP entry for personal accounts while allowing users with an active Team organization
- add the organization region field and keep access eligibility independent from model presentation
- apply CN-only model display overrides from the Flow Jobs managed collection, hiding unconfigured models only for CN Team users
- preserve LiteLLM names and the full entitled model catalog outside CN
- prevent hidden regional models from reappearing or being saved through the composer or Agent Builder
- add end-to-end regional compliance observability without logging email, raw IP, full UID, or model/configuration content

## Meeting-aligned behavior

- mainland IP plus active Team organization: allow email OTP regardless of organization region
- mainland IP plus personal or missing active Team organization: block before sending OTP
- model white-labeling: controlled only by Team organization `region_code` equal to `CN`
- no separate contracted-enterprise field and no coupling between contract state and region display

## Regional compliance logging

- log normalized `CF-IPCountry`; missing values are `empty` and malformed values are `invalid`
- log the final Web outcome: invalid request, personal blocked, eligibility dependency error, OTP error, OTP sent, or Team allowed and OTP sent
- log Organization `region_code` as configured; a missing legacy value is `empty` with effective `CN`
- log invalid persisted Organization regions with masked UID and Organization ID
- log model override configuration version, modification time, declared/actual row counts, regional matches, invalid rows, duplicate rows, missing active configuration, and invalid data shape
- log model catalog mode and entitled/override/visible counts, with a warning for an empty catalog
- Flow Jobs executes outside this repository; this PR observes the resulting Mongo sync document rather than duplicating its job logs

## Scope

Phase one is Web-only. It does not add iOS enforcement, session enforcement for already logged-in users, domain migration, or HMAC signing. It adds one server-only deployment secret, `DOMESTIC_ACCESS_BFF_TOKEN`, shared by Web and claw-interface for the pre-auth eligibility call.

## Deployment prerequisite

- configure `DOMESTIC_ACCESS_BFF_TOKEN` in the GitHub `staging` and `production` Environment Secrets
- configure the matching per-environment value in the claw-interface Vault path `srp/ecap/claw-interface/env`
- roll the claw-interface pods before deploying Web; the Web workflow validates and injects the secret into the Cloudflare Worker

## Verification

- Claw Interface full suite: 9236 passed, 269 skipped
- deployment/authentication contract suite: 9 passed
- scoped Web verifier: 77 passed
- repository pre-commit and pre-push gates passed, including ESLint, TypeScript, Ruff, Pyright, import contracts, dependency checks, and YAML validation
- local end-to-end QA completed for CN and non-CN entry paths

```
