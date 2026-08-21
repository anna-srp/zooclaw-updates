---
title: "修复：部分新用户注册后环境未创建，导致安装一直等待"
type: "Bug Fix"
priority: "高"
date: "2026-08-20"
status: "待审核"
channels: ""
---

# 修复：部分新用户注册后环境未创建，导致安装一直等待

## 核心宣传点

注册时判断该给新用户开哪种运行环境的逻辑与后续安装环节不一致：邮箱缺失或不在白名单内的用户，注册时被当成新版引擎用户处理、没有创建对应的计算环境，但安装时又被引导到旧版路径，结果一直卡在等待一个并不存在的环境。现在注册与安装统一按同一套运行时判断，不再出现这种死等。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `044636aa369cc0d97b09198382e2df4266898b33`
- PR: #3423
- 作者: bill-srp
- 日期: 2026-08-20T06:48:18Z

### Commit Message

```
fix(auth): branch signup bootstrap on install-capability runtime (#3423)

## Summary
- Signup bootstrap now branches on `capability.runtime === 'engine'`
instead of `capability.reason !== 'agents_v2_disabled'` when deciding
whether to provision a v1 computer (`web/app/src/lib/auth/manager.ts`).
- Parametrizes the pinned unit test over all three computer-runtime
reasons (`agents_v2_disabled`, `email_missing`,
`email_not_allowlisted`), each asserting `createComputer` is called.

## Root cause
`GET /agents/install-capability` returns `runtime: "computer"` for every
ineligible user, but signup bootstrap only treated `reason ===
'agents_v2_disabled'` as the computer case. Users with `email_missing` /
`email_not_allowlisted` (production, `AGENTS_V2_ENABLED=true`, not
allowlisted) were treated as engine users at signup — no v1 computer
created — while every other consumer of the capability (BFF install
route, claw-settings tab, landing hire flow) branches on `runtime` and
later routes those same users to the v1 computer install path, which
then waits on a computer that never exists. Branching on `runtime` makes
signup provisioning agree with install-time routing.

## Test plan
- [x] `pnpm exec vitest run tests/unit/lib/auth/manager.unit.spec.ts` —
87/87 passed
- [x] `bash scripts/verify-web.sh --no-test` on the touched files —
guards + tsc + eslint clean
- [ ] CI (`web-quality` + `web-build-check`) green on the
merged-with-main combination
```

### PR Body

## Summary
- Signup bootstrap now branches on `capability.runtime === 'engine'` instead of `capability.reason !== 'agents_v2_disabled'` when deciding whether to provision a v1 computer (`web/app/src/lib/auth/manager.ts`).
- Parametrizes the pinned unit test over all three computer-runtime reasons (`agents_v2_disabled`, `email_missing`, `email_not_allowlisted`), each asserting `createComputer` is called.

## Root cause
`GET /agents/install-capability` returns `runtime: "computer"` for every ineligible user, but signup bootstrap only treated `reason === 'agents_v2_disabled'` as the computer case. Users with `email_missing` / `email_not_allowlisted` (production, `AGENTS_V2_ENABLED=true`, not allowlisted) were treated as engine users at signup — no v1 computer created — while every other consumer of the capability (BFF install route, claw-settings tab, landing hire flow) branches on `runtime` and later routes those same users to the v1 computer install path, which then waits on a computer that never exists. Branching on `runtime` makes signup provisioning agree with install-time routing.

## Test plan
- [x] `pnpm exec vitest run tests/unit/lib/auth/manager.unit.spec.ts` — 87/87 passed
- [x] `bash scripts/verify-web.sh --no-test` on the touched files — guards + tsc + eslint clean
- [ ] CI (`web-quality` + `web-build-check`) green on the merged-with-main combination


