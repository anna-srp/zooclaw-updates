---
title: "修复：新建的个人组织被默默打上「中国区」标记，导致境外邮箱登录被挡"
type: "Bug Fix"
priority: "中"
date: "2026-09-04"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：新建的个人组织被默默打上「中国区」标记，导致境外邮箱登录被挡

## 核心宣传点

这是昨天那条「个人版用户在境外用邮箱登录被区域校验挡住」的根因续集。数据模型给组织的 `region_code` 设了一个默认值 CN，于是每一个新建的组织——哪怕创建时压根没人指定过区域——落库时都会被写上一个「中国区」的标记。这个隐式默认值一旦存进去，后续的邮箱验证码登录准入就会拿它当权威区域来判定，把明明人在境外的用户挡在门外。

现在创建组织时，没有显式提供区域就不再写入 `region_code` 字段，显式配置过的区域和其他默认字段一律保持原样。行为上：没配区域的新个人组织，邮箱 OTP 的准入回落到请求方 IP 所属国家判定；IP 国家是 CN、缺失或非法时依旧拦截；有效的非中国 IP 国家则放行。团队组织的登录资格判定完全不变。

这次改动**不迁移也不修改任何已有的组织数据**，历史上已经存下 CN 的组织仍按原值生效；没有新增设置项，也没有前端改动。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `c3a977f4e11166cc80c056f598b23ff7488efa4b`
- PR: #3648
- 作者: sam-srp
- 日期: 2026-09-04T08:39:35Z

### Commit Message

```
fix(org): avoid persisting implicit CN region on creation (#3648)

## Summary
- Omit region_code from new Org documents when it was not explicitly
supplied, instead of persisting the model default CN.
- Preserve explicitly configured regions and all other default fields.
- Add regression tests for personal/team creation and login eligibility
after persistence.

## Behavior
- New personal Orgs without a configured region fall back to request IP
country for email OTP eligibility.
- CN, missing, or invalid IP country remains blocked; valid non-CN IP
country is allowed.
- Team login eligibility is unchanged.
- No existing Org data is migrated or modified; existing stored CN
values remain effective.
- No new settings or frontend changes.

## Verification
- 121 related unit tests passed (Org repository/service, domestic access
and routes, regional model display).
- Targeted Pyright: 0 errors, 0 warnings.
- Ruff lint and format checks passed.
- Import contracts: 8 kept, 0 broken.
- git diff --check passed.
```

### PR Body

```
## Summary
- Omit region_code from new Org documents when it was not explicitly supplied, instead of persisting the model default CN.
- Preserve explicitly configured regions and all other default fields.
- Add regression tests for personal/team creation and login eligibility after persistence.

## Behavior
- New personal Orgs without a configured region fall back to request IP country for email OTP eligibility.
- CN, missing, or invalid IP country remains blocked; valid non-CN IP country is allowed.
- Team login eligibility is unchanged.
- No existing Org data is migrated or modified; existing stored CN values remain effective.
- No new settings or frontend changes.

## Verification
- 121 related unit tests passed (Org repository/service, domestic access and routes, regional model display).
- Targeted Pyright: 0 errors, 0 warnings.
- Ruff lint and format checks passed.
- Import contracts: 8 kept, 0 broken.
- git diff --check passed.
```
