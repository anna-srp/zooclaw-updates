---
title: "修复企业管理后台：线下付费企业账户登录卡在验证页"
type: "Bug Fix"
priority: "中"
date: "2026-07-23"
status: "待审核"
channels: ""
---

## 核心宣传点

修复了一个企业管理后台的登录 Bug：使用线下付款（offline）方式购买套餐的企业账户，在通过 OTP 短信验证码验证后会卡在验证页面无法进入。现在这类账户可以正常登录了。

## 原始内容

**PR #3038 — fix(enterprise-admin): accept offline payment accounts**
SHA: 2eab857f0bc71500433ee6d0daba596e6f26aa33 ｜ 作者: bill-srp

- Accept the backend `offline` payment channel in the Enterprise Admin `/account/me` contract.
- Add regression coverage for OTP login by an existing offline-paid enterprise account.

### Root cause
The backend added `payment_channel: "offline"` for offline enterprise packages, but the Enterprise Admin Zod schema still accepted only `stripe`, `antom`, and `apple`. After OTP verification, parsing `/account/me` raised a Zod error and left the user on the verification screen.
