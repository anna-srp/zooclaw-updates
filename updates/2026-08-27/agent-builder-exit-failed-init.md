---
title: "修复：Agent Builder 初始化失败后被困在同一个项目里，怎么点都退不出去"
type: "Bug Fix"
priority: "中"
date: "2026-08-27"
status: "待审核"
channels: ""
---

# 修复：Agent Builder 初始化失败后被困在同一个项目里，怎么点都退不出去

## 核心宣传点

项目第一轮初始化失败后，只要再打开 Agent Builder 首页，就会被自动带回那个失败的项目，形成一个退不出去的跳转循环。现在初始化失败时你可以正常返回项目列表，同时你输入的提示词、已上传的附件进度和选好的模型都会保留，手动重新打开或点重试仍然能安全恢复。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `5f7f08971f15913c7445ee1cd9b1cacf55c80ac6`
- PR: #3560
- 作者: kaka-srp
- 日期: 2026-08-27T15:07:41Z

### Commit Message

```
fix(agent-builder): allow exiting failed initialization (#3560)

## Summary
- Let users return to the Agent Builder Project list after a first-turn
initialization error instead of being routed back into the same failed
Project.
- Preserve the pending prompt, attachment progress, model choice, and
idempotency key so manual reopen and explicit retry still recover
safely.
- Keep automatic navigation for new and legacy in-flight handoffs, and
add regression coverage plus a design spec.

## Root cause
The pending initialization record represented both durable recovery data
and the Agent Builder home page's auto-navigation policy. Initialization
errors intentionally preserved that record for retry, so every visit to
`/agent-builder` interpreted it as an instruction to reopen the failed
Project and trapped the user in a redirect loop.

## Test plan
- [x] `bash scripts/verify-web.sh <changed Agent Builder source and test
files>`
- [x] 61 targeted Vitest cases passed across the entry page and
pending-initialization hook suites
- [x] TypeScript, ESLint, all seven frontend governance guards, and `git
diff --check` passed
- [x] Pre-push changed-surface verification passed
```

### PR Description

```
## Summary
- Let users return to the Agent Builder Project list after a first-turn initialization error instead of being routed back into the same failed Project.
- Preserve the pending prompt, attachment progress, model choice, and idempotency key so manual reopen and explicit retry still recover safely.
- Keep automatic navigation for new and legacy in-flight handoffs, and add regression coverage plus a design spec.

## Root cause
The pending initialization record represented both durable recovery data and the Agent Builder home page's auto-navigation policy. Initialization errors intentionally preserved that record for retry, so every visit to `/agent-builder` interpreted it as an instruction to reopen the failed Project and trapped the user in a redirect loop.

## Test plan
- [x] `bash scripts/verify-web.sh <changed Agent Builder source and test files>`
- [x] 61 targeted Vitest cases passed across the entry page and pending-initialization hook suites
- [x] TypeScript, ESLint, all seven frontend governance guards, and `git diff --check` passed
- [x] Pre-push changed-surface verification passed

```

---
