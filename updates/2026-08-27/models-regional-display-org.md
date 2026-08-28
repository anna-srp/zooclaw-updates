---
title: "模型显示名称改为按你当前所在组织的区域解析，个人账号也生效"
type: "体验优化"
priority: "中"
date: "2026-08-27"
status: "待审核"
channels: ""
---

# 模型显示名称改为按你当前所在组织的区域解析，个人账号也生效

## 核心宣传点

区域化的模型显示名称此前只对团队组织生效，个人账号一律看到原始名称；用量页面也没跟着走同一套规则，同一个模型在聊天页和用量页可能显示成两个名字。现在个人和团队账号都按你当前所在组织的区域来解析显示名称，组织没有配置区域时按访问来源国家兜底；聊天页的模型列表和「设置-用量」采用同一套显示规则，模型 ID 和你的权限范围完全不变。同时，大陆邮箱验证码登录的判定改用账号档案里的权威标识，不再依赖那个可能为空的邮箱字段。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `3acaa2defcf62b52152913fb0be39276933d95d5`
- PR: #3553
- 作者: sam-srp
- 日期: 2026-08-27T10:21:42Z

### Commit Message

```
fix(models): resolve display region from current org (#3553)

## Summary
- Resolve model display region from the user's single active
organization for both personal and team orgs.
- Fall back to the Cloudflare `cf-ipcountry` region, then `CN`, when the
active org has no valid `region_code`.
- Apply the same display-name policy to the chat model catalog and
Settings Usage while preserving model IDs, entitlements, and unmapped
models.
- Forward `cf-ipcountry` through the web BFF to claw-interface; no new
environment variables are required.

## Root cause
The existing regional display resolver only applied organization
overrides to team orgs and returned original metadata for personal
users. It also had no request-region input, because the generic web BFF
did not forward Cloudflare's country header to the model catalog or
usage-record endpoints.

## Test plan
- [x] Backend regional policy tests cover personal/team org overrides,
missing org fields, CF fallback, `XX`, invalid values, and `CN`
fallback.
- [x] Backend model catalog and Settings Usage route tests verify the
request region reaches the shared display resolver.
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh web/app/src/lib/api/claw-proxy.ts
web/app/tests/unit/lib/api/claw-proxy.unit.spec.ts`
- [x] 66 focused backend unit tests.
```

### PR Description

```
## Summary
- Resolve model display region from the user's single active organization for both personal and team orgs.
- Fall back to the Cloudflare `cf-ipcountry` region, then `CN`, when the active org has no valid `region_code`.
- Apply the same display-name policy to the chat model catalog and Settings Usage while preserving model IDs, entitlements, and unmapped models.
- Forward `cf-ipcountry` through the web BFF to claw-interface; no new environment variables are required.

## Root cause
The existing regional display resolver only applied organization overrides to team orgs and returned original metadata for personal users. It also had no request-region input, because the generic web BFF did not forward Cloudflare's country header to the model catalog or usage-record endpoints.

## Test plan
- [x] Backend regional policy tests cover personal/team org overrides, missing org fields, CF fallback, `XX`, invalid values, and `CN` fallback.
- [x] Backend model catalog and Settings Usage route tests verify the request region reaches the shared display resolver.
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh web/app/src/lib/api/claw-proxy.ts web/app/tests/unit/lib/api/claw-proxy.unit.spec.ts`
- [x] 66 focused backend unit tests.

```

---

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `11e74bde540bdaf0c5cb89c8dc9e4068308862e2`
- PR: #3543
- 作者: sam-srp
- 日期: 2026-08-27T04:17:10Z

### Commit Message

```
fix(compliance): align regional model display and login (#3543)

## Summary

- resolve mainland email OTP eligibility from the authoritative
gem_account profile identifier instead of the optional account email
field
- reuse generic region_code model display overrides in usage records
while preserving raw model IDs
- render configured display names in Settings usage with
backward-compatible fallback to original LiteLLM model names

## Validation

- backend targeted unit suite: 79 passed
- frontend unit suite: 9,236 passed, 70 skipped, 1 todo
- Ruff check/format, targeted Pyright, import-linter
- frontend ESLint, TypeScript, and CI lint hard gates
```

### PR Description

```
## Summary

- resolve mainland email OTP eligibility from the authoritative gem_account profile identifier instead of the optional account email field
- reuse generic region_code model display overrides in usage records while preserving raw model IDs
- render configured display names in Settings usage with backward-compatible fallback to original LiteLLM model names

## Validation

- backend targeted unit suite: 79 passed
- frontend unit suite: 9,236 passed, 70 skipped, 1 todo
- Ruff check/format, targeted Pyright, import-linter
- frontend ESLint, TypeScript, and CI lint hard gates
```

---
