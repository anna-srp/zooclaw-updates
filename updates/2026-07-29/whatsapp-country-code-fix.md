---
title: "修复 WhatsApp 部分海外号码被误加 +86 导致无法接入的问题"
type: "Bug Fix"
priority: "中"
date: "2026-07-29"
status: "待审核"
channels: ""
---

## 核心宣传点

修复了 WhatsApp 桥接时把某些 11 位美国号码错误识别成中国手机号（误加 +86）从而被账号服务拒绝的问题；现在号码统一按 E.164 规范传递，海外用户接入更可靠。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- commit：e307c19e49230e826c42e6a39610dee958a5a67f
- PR：#3105
- 日期：2026-07-29T03:31:56Z

### Commit message

```
fix(whatsapp): preserve sender country code (#3105)

## Summary
- send the WhatsApp sender phone number to the account service in E.164
form
- keep the original Meta `wa_id` unchanged for WhatsApp identity
matching
- lock the account-service request contract with a regression test

## Root cause
The bridge sent an eleven-digit US `wa_id` as a bare `phone_number`. The
account service reused its domestic SMS normalizer and interpreted any
eleven-digit value beginning with `1` as a Chinese mobile number,
prepending `+86`. Claw Interface then rejected the account because the
stored phone digits no longer matched the WhatsApp identity.

## Test plan
- [x] `pnpm test`
- [x] `pnpm typecheck`
- [x] `pnpm build`
- [x] targeted Claw Interface matching-phone test

## Operational note
Accounts already persisted with the incorrect `+86` prefix still require
a staging data repair or recreation before they can bind successfully.
```

### PR body

## Summary
- send the WhatsApp sender phone number to the account service in E.164 form
- keep the original Meta `wa_id` unchanged for WhatsApp identity matching
- lock the account-service request contract with a regression test

## Root cause
The bridge sent an eleven-digit US `wa_id` as a bare `phone_number`. The account service reused its domestic SMS normalizer and interpreted any eleven-digit value beginning with `1` as a Chinese mobile number, prepending `+86`. Claw Interface then rejected the account because the stored phone digits no longer matched the WhatsApp identity.

## Test plan
- [x] `pnpm test`
- [x] `pnpm typecheck`
- [x] `pnpm build`
- [x] targeted Claw Interface matching-phone test

## Operational note
Accounts already persisted with the incorrect `+86` prefix still require a staging data repair or recreation before they can bind successfully.

