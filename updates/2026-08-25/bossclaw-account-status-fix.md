---
title: "修复：BossClaw 登录时把已注册用户误判为「未注册」，逼着老用户去要邀请码"
type: "Bug Fix"
priority: "中"
date: "2026-08-25"
status: "待审核"
channels: ""
---

# 修复：BossClaw 登录时把已注册用户误判为「未注册」，逼着老用户去要邀请码

## 核心宣传点

上线前的验证发现一个卡人的问题：有的手机号在账号库里对应着几十条历史/测试记录，系统在这种「对不上唯一一个人」的情况下会保守地判定为未注册，导致真实老用户在 BossClaw 登录时被要求提供邀请码，等于被挡在门外。现在登录页只判断「这个号码是否存在一个仍然有效的账号」，历史遗留的失效记录不再参与判断，老用户可以正常收验证码登录。同时页面文案从「正在进入 ZooClaw…」更新为「正在进入 ZooWork…」，与域名迁移保持一致。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `4d54b7f48fa168c797d2efcd11b0ec8204260df8`
- PR: #3515
- 作者: tim-srp
- 日期: 2026-08-25T13:14:30Z

### Commit Message

```
fix(bossclaw): account-status uses active-profile existence, not uid resolution (#3515)

## Summary

Staging test of the merged #3513 exposed a false "unregistered" for a
real user: `18610983415` matched **45** `gem_account` profiles (most
were inactive test rows), and `get_by_phone_number`'s fallback — shared
with KB/Twilio — fails closed on ambiguous matches, so the
account-status endpoint returned `registered: false` for a registered
user.

The account-status endpoint only needs boolean existence (it returns no
uid, and the OTP step binds identity exactly via the account service),
so ambiguity is harmless there:

- `user_repo.has_top_level_phone` — top-level `ecap-account` phone hit
short-circuits.
- `profile_repo.has_active_identifier` — any **`is_active: true`**
`gem_account` profile match. Inactive profiles (test/history rows) are
excluded.
- `routes/bossclaw.py` combines the two; `get_by_phone_number`
(Twilio/KB fail-closed uid resolution) is untouched.

Verified on the staging pod: `is_active` filtering reduces the 45
matches to the single real uid.

Also in this PR (from the same staging round):
- Success copy `正在进入 ZooClaw…` → `正在进入 ZooWork…` (domain migration).
- The two `new URL(x, 'https://zooclaw.ai')` parse bases updated to
`zoowork.ai`.

## Test plan

- Backend: 90 passed (account-status, user_repo, profile_repo,
subscription_code); ruff + pyright 0 errors; user_repo stays under the
500-line guard (491).
- Staging verification: pod-level queries confirmed `is_active: true`
matches the user's own uid.

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Description

```
## Summary

Staging test of the merged #3513 exposed a false "unregistered" for a real user: `18610983415` matched **45** `gem_account` profiles (most were inactive test rows), and `get_by_phone_number`'s fallback — shared with KB/Twilio — fails closed on ambiguous matches, so the account-status endpoint returned `registered: false` for a registered user.

The account-status endpoint only needs boolean existence (it returns no uid, and the OTP step binds identity exactly via the account service), so ambiguity is harmless there:

- `user_repo.has_top_level_phone` — top-level `ecap-account` phone hit short-circuits.
- `profile_repo.has_active_identifier` — any **`is_active: true`** `gem_account` profile match. Inactive profiles (test/history rows) are excluded.
- `routes/bossclaw.py` combines the two; `get_by_phone_number` (Twilio/KB fail-closed uid resolution) is untouched.

Verified on the staging pod: `is_active` filtering reduces the 45 matches to the single real uid.

Also in this PR (from the same staging round):
- Success copy `正在进入 ZooClaw…` → `正在进入 ZooWork…` (domain migration).
- The two `new URL(x, 'https://zooclaw.ai')` parse bases updated to `zoowork.ai`.

## Test plan

- Backend: 90 passed (account-status, user_repo, profile_repo, subscription_code); ruff + pyright 0 errors; user_repo stays under the 500-line guard (491).
- Staging verification: pod-level queries confirmed `is_active: true` matches the user's own uid.

```
