---
title: "企业咨询表单新增公司名必填，并拦截个人邮箱提交"
type: "体验优化"
priority: "中"
date: "2026-10-14"
status: "待审核"
channels: ""
---

# 企业咨询表单新增公司名必填，并拦截个人邮箱提交

## 核心宣传点

企业「联系销售」表单新增公司名称必填项，并作为 company 字段随现有的 /business/contact 请求一起提交，方便销售侧直接拿到客户归属。提交时会拦截常见的个人邮箱域名，提示「请使用您的企业邮箱」，同时保留已填内容供用户修正，不会清空重填。原有的咨询选项和提交生命周期完全保留。所有支持的商务页语种都补了公司名标签与校验提示文案，并带无障碍字段错误播报和回归用例覆盖。后端请求结构已同步接受可选的公司名（提供时去空白并限制 1–200 字符），省略该字段的旧客户端仍然兼容。

## 分级

- 内部：P2
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## 备注

后端已向前兼容，但前后端建议同期发版以保证新字段能被正确接收；作者本地完整 TypeScript 检查因复用本地依赖缺包未通过，以 CI 为准。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `50445b1be96949753c9fb4b61b3b5903414a2e66`
- PR: #4044
- 作者：shana-srp
- 日期：2026-10-14T03:20:06Z

### Commit Message

```
feat(enterprise): require company and validate work email (#4044)

## Summary
Require a Company name in the enterprise Contact sales form and include
it as `company` in the existing `/business/contact` request. Block
common personal email domains on submit with “Please use your business
email address.”, retaining inputs for correction. Existing consultation
options and submission lifecycle are preserved.

Add localized company labels and validation feedback for all supported
business-page locales, plus accessible field errors and regression
coverage.

## Validation
- 19 related unit tests passed, including personal email rejection,
required company, request payload, retry, duplicate submission
prevention, and demo navigation.
- Scoped ESLint and frontend governance guards passed.
- Local browser verified the Company field and personal-email rejection.
- Full TypeScript check could not pass with the reused local
dependencies: missing fast-xml-parser, cron-parser, cronstrue, and yaml
modules. CI should verify against the pinned installation.

## Backend compatibility and deployment
The backend request schema now accepts an optional, trimmed company name
(1–200 characters when supplied), preserving existing clients that omit
it. Existing application-log recording includes company automatically;
the sales Feishu notification includes the company name. Unknown fields
remain forbidden.

Deploy the backend before the frontend to prevent the previously
deployed schema rejecting the new company property with HTTP 422. Both
frontend and backend deployment are required.

## Review fix validation
- 39 backend contact endpoint tests passed, including the actual
frontend payload, trimmed company in logs and notification,
invalid-company rejection, and legacy requests without company.
- Frontend CI lint/typecheck, tests, and build passed on the initial
revision.

## Contact form error-state fix
After a failed backend request, rejecting a personal email now clears
the obsolete request-failure alert and shows only the business-email
correction message. Form values and email focus are preserved, and a
corrected business email can retry successfully.

Validation:
- Added a regression test for failed request → personal-email rejection
→ corrected retry; confirmed it fails before the fix and passes
afterward. The rejected attempt sends no additional request.
- All 20 related contact and demo-navigation tests pass under Node 24.
- Scoped ESLint and all seven frontend governance guards pass.
- Full local TypeScript checking remains limited by the reused
dependency installation missing fast-xml-parser, cron-parser, cronstrue,
and yaml; CI uses the pinned installation.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

