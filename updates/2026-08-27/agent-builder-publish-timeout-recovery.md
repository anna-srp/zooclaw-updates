---
title: "修复：Agent Builder 发布慢一点就报错，重试还会重复提交一次"
type: "Bug Fix"
priority: "中"
date: "2026-08-27"
status: "待审核"
channels: ""
---

# 修复：Agent Builder 发布慢一点就报错，重试还会重复提交一次

## 核心宣传点

Agent Builder 的发布要同步跑完校验和打包，耗时可能超过浏览器 30 秒的请求上限——于是前端先超时报出一串看不懂的错误，后端其实已经发布成功了；你从错误弹窗点重试，就会对着已经成功的版本再提交一遍。现在等待时间放宽到 90 秒，超时后会去核对项目的真实状态，确认同一版本已经提交成功就直接继续，并把原来的报错换成看得懂的中文提示。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `d3730c7f4ef2ad7f63c0440013f8c2d53d85d42a`
- PR: #3561
- 作者: kaka-srp
- 日期: 2026-08-27T15:08:10Z

### Commit Message

```
fix(agent-builder): recover slow publish submissions (#3561)

## Summary
- Extend Agent Builder v2 iteration submission to a 90-second client
timeout.
- Recover an aborted submission by polling the authoritative project
state and continuing only when the same iteration and test run was
persisted as submitted.
- Replace the raw AbortError with localized recovery guidance and add
regression coverage for timeout, polling, and cross-iteration safety.

## Root cause
Agent Builder submission performs validation and Pack promotion
synchronously and can take longer than the API client's 30-second
default timeout. The browser aborted first while the backend continued
and successfully persisted the submission. Retrying from the error
dialog then issued a duplicate submit against an already-promoted test
run.

## Test plan
- [x] `pnpm exec vitest run
tests/unit/services/agent-builder-v2.unit.spec.ts
tests/unit/services/agent-builder-publish.unit.spec.ts` (27 tests)
- [x] `pnpm exec vitest run
tests/unit/app/agent-builder-client.unit.spec.tsx -t "shows a
recovery-safe message instead of the raw AbortError when Publish times
out"`
- [x] `bash scripts/verify-changed.sh`
- [x] Pre-push size, TypeScript, and ESLint gates
```

### PR Description

```
## Summary
- Extend Agent Builder v2 iteration submission to a 90-second client timeout.
- Recover an aborted submission by polling the authoritative project state and continuing only when the same iteration and test run was persisted as submitted.
- Replace the raw AbortError with localized recovery guidance and add regression coverage for timeout, polling, and cross-iteration safety.

## Root cause
Agent Builder submission performs validation and Pack promotion synchronously and can take longer than the API client's 30-second default timeout. The browser aborted first while the backend continued and successfully persisted the submission. Retrying from the error dialog then issued a duplicate submit against an already-promoted test run.

## Test plan
- [x] `pnpm exec vitest run tests/unit/services/agent-builder-v2.unit.spec.ts tests/unit/services/agent-builder-publish.unit.spec.ts` (27 tests)
- [x] `pnpm exec vitest run tests/unit/app/agent-builder-client.unit.spec.tsx -t "shows a recovery-safe message instead of the raw AbortError when Publish times out"`
- [x] `bash scripts/verify-changed.sh`
- [x] Pre-push size, TypeScript, and ESLint gates

```

---
