---
title: "手机号登录的国家列表移除中国大陆 +86，其他国家短信登录保持不变"
type: "体验优化"
priority: "中"
date: "2026-09-24"
status: "待审核"
channels: ""
---

# 手机号登录的国家列表移除中国大陆 +86，其他国家短信登录保持不变

## 核心宣传点

手机号注册/登录的国家或地区下拉里去掉了中国大陆 +86 选项，同时把它对应的国家码映射和那条已经用不到的中国专属校验分支一并清掉。美国、加拿大、墨西哥、印度、菲律宾、越南、韩国等选项全部保留，手机号入口、表单、短信验证和 reCAPTCHA 处理也都还在——这次不是下线全部短信登录。改动通过共享的 LoginForm 同时生效于三处：独立的 /login 页面、官网落地页的登录弹窗、产品内的登录弹窗。邮箱登录和 Google 登录不受影响；这是前端选择器层面的调整，后端并没有对 +86 号码做全局限制，/user/verify、BossClaw 登录和后端认证都不在本次范围内。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已上线

## PR 说明

## Confirmed requirement / 已确认需求

**本次仅从手机号注册／登录的国家或地区列表中移除中国大陆 +86 选项。保留其他国家／地区的手机号登录和短信验证。不是移除全部 SMS 登录。**

This PR removes only the China (+86) country-code option. Retaining the phone entry, phone form, and SMS verification for the remaining countries is explicitly required.

## Scope

The shared `LoginForm` applies this change to all three web surfaces:

- Standalone `/login` page.
- Landing-page login modal.
- In-product login modal.

Remove the +86 option, its country-code mapping, and its now-unused China-specific validation branch. Keep the existing United States, Canada, Mexico, India, Philippines, Vietnam, and South Korea options.

Phone buttons, SMS/reCAPTCHA handling, verification handoff, styles, and translations remain available. Email and Google login are unchanged. This is a frontend selector change, not a backend-wide restriction on +86 numbers. `/user/verify`, BossClaw login, and backend authentication are outside this change.

## Review clarification

The earlier description proposing removal of all phone/SMS login was based on a misunderstanding and is superseded by the confirmed requirement above.

The finding titled “[P1] 完成 PR 所述的 SMS 登录移除” assumes that earlier scope. Its observation that phone buttons and `sendSMSVerification` remain is correct, but that behavior is intentional and required. Removing all phone login would violate the confirmed requirement. Regression tests therefore assert that phone login remains available while the country selector excludes +86.

## Validation

- 70 LoginForm unit tests passed, covering retained SMS behavior and the country options in both shared form variants.
- TypeScript, ESLint, and frontend governance checks passed.
- All three surfaces were manually checked in the local mock preview: phone login is present and the country list excludes +86.
- Real SMS delivery was not tested in the mock environment.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `6b5cc7aa3bcb9c5b82cba19d6d69a391dfc637c9`
- PR: #3892
- 作者：tim-srp
- 日期：2026-09-24T02:42:31Z

### Commit Message

```
fix(auth): remove China +86 option while retaining SMS login (#3892)

## Confirmed requirement / 已确认需求

**本次仅从手机号注册／登录的国家或地区列表中移除中国大陆 +86 选项。保留其他国家／地区的手机号登录和短信验证。不是移除全部 SMS
登录。**

This PR removes only the China (+86) country-code option. Retaining the
phone entry, phone form, and SMS verification for the remaining
countries is explicitly required.

## Scope

The shared `LoginForm` applies this change to all three web surfaces:

- Standalone `/login` page.
- Landing-page login modal.
- In-product login modal.

Remove the +86 option, its country-code mapping, and its now-unused
China-specific validation branch. Keep the existing United States,
Canada, Mexico, India, Philippines, Vietnam, and South Korea options.

Phone buttons, SMS/reCAPTCHA handling, verification handoff, styles, and
translations remain available. Email and Google login are unchanged.
This is a frontend selector change, not a backend-wide restriction on
+86 numbers. `/user/verify`, BossClaw login, and backend authentication
are outside this change.

## Review clarification

The earlier description proposing removal of all phone/SMS login was
based on a misunderstanding and is superseded by the confirmed
requirement above.

The finding titled “[P1] 完成 PR 所述的 SMS 登录移除” assumes that earlier scope.
Its observation that phone buttons and `sendSMSVerification` remain is
correct, but that behavior is intentional and required. Removing all
phone login would violate the confirmed requirement. Regression tests
therefore assert that phone login remains available while the country
selector excludes +86.

## Validation

- 70 LoginForm unit tests passed, covering retained SMS behavior and the
country options in both shared form variants.
- TypeScript, ESLint, and frontend governance checks passed.
- All three surfaces were manually checked in the local mock preview:
phone login is present and the country list excludes +86.
- Real SMS delivery was not tested in the mock environment.

---------

Co-authored-by: Claude Code <noreply@anthropic.com>
```

来源：SerendipityOneInc/ecap-workspace @ 6b5cc7aa，PR #3892，作者 tim-srp。