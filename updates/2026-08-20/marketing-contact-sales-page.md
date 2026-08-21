---
title: "新增「联系销售」页面"
type: "新功能上线"
priority: "中"
date: "2026-08-20"
status: "待审核"
channels: ""
---

# 新增「联系销售」页面

## 核心宣传点

官网新增多语言的 Contact Sales 联系销售页与表单，企业客户可以直接从官网留资沟通。该页面目前仍处于开关控制状态，开启后即可对外访问。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `4e493efabfa1306ae5977e30aebdd353fedd0ae1`
- PR: #3430
- 作者: shana-srp
- 日期: 2026-08-20T03:09:28Z

### Commit Message

```
feat(marketing): add contact sales page (#3430)

## Linear

No linked issue.

## Summary

- add the localized Contact Sales route and contact form client
- register `/contact` with public SEO and marketing-route locale
handling
- keep the route feature-gated until the Contact page is enabled

## Test plan

- [x] `bash scripts/verify-web.sh --no-test`
- [x] Contact unit tests: 2 files / 4 tests passed
- [x] TypeScript passed
- [x] ESLint passed

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Linear

No linked issue.

## Summary

- add the localized Contact Sales route and contact form client
- register `/contact` with public SEO and marketing-route locale handling
- keep the route feature-gated until the Contact page is enabled

## Test plan

- [x] `bash scripts/verify-web.sh --no-test`
- [x] Contact unit tests: 2 files / 4 tests passed
- [x] TypeScript passed
- [x] ESLint passed


