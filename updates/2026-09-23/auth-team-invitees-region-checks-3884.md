---
title: "被团队邀请的成员可以跳过地区限制完成注册"
type: "新功能上线"
priority: "中"
date: "2026-09-23"
status: "待审核"
channels: ""
---

# 被团队邀请的成员可以跳过地区限制完成注册

## 核心宣传点

企业/团队把成员邀请进来时，如果对方所在地区本来受注册限制（或者地区信息缺失），流程会直接卡住。现在邀请码会跟着邮箱验证码一起走：系统先校验这是一张绑定该邮箱、仍然有效的团队邀请，确认后才放行地区限制。普通注册和已有账号的行为完全不变，资格预检是只读的，最终的邀请兑换仍然是原子操作，不会出现「放行了但席位没占上」的情况。

## 分级

- 内部：P1
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary

- pass the organization invite code through email OTP send and verify
- validate email-bound, active team invitations before bypassing mainland or missing-region signup restrictions
- preserve existing-user and normal signup behavior; the eligibility precheck stays read-only and final invite redemption remains atomic

## Validation

- `bash scripts/verify-web.sh --no-test`
- `bash scripts/verify-py.sh`
- targeted Web unit tests: 59 passed
- targeted claw-interface unit tests: 46 passed
- `git diff --check`

## Rollout

- deploy claw-interface before Web so the backend accepts the extended eligibility contract
- no database migration, new environment variable, or Account Service change

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `a128850465d270dfed26ad514f94bb3edc0f4cae`
- PR: #3884
- 作者：sam-srp
- 日期：2026-09-23T10:10:53Z

### Commit Message

```
feat(auth): allow team invitees through region checks (#3884)

## Summary

- pass the organization invite code through email OTP send and verify
- validate email-bound, active team invitations before bypassing
mainland or missing-region signup restrictions
- preserve existing-user and normal signup behavior; the eligibility
precheck stays read-only and final invite redemption remains atomic

## Validation

- `bash scripts/verify-web.sh --no-test`
- `bash scripts/verify-py.sh`
- targeted Web unit tests: 59 passed
- targeted claw-interface unit tests: 46 passed
- `git diff --check`

## Rollout

- deploy claw-interface before Web so the backend accepts the extended
eligibility contract
- no database migration, new environment variable, or Account Service
change
```

来源：SerendipityOneInc/ecap-workspace @ a1288504，PR #3884，作者 sam-srp。