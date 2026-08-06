---
title: "修复 Agent Builder 误报「工作区被占用」"
type: "Bug Fix"
priority: "中"
date: "2026-08-05"
status: "待审核"
channels: ""
---

# 修复 Agent Builder 误报「工作区被占用」

## 核心宣传点

同一页面刷新组件时不会再自己锁住自己，不会无故出现等待其他设备释放工作区的提示。

## 原始内容

- 仓库：`SerendipityOneInc/ecap-workspace`
- Commit：`0dd04f7454c7dfe16cf84f0babef52ec459c11fc`
- 作者：kaka-srp
- 日期：2026-08-05T04:13:45Z
- PR：#3243

### Commit Message

```
fix(agent-builder): prevent same-page workspace self-lock (#3243)

## Summary
- Reuse the retained V1 workspace coordinator when the same `uid` /
computer / project / session remounts in one page.
- Carry an in-flight activation promise and its error state across that
handoff, avoiding duplicate Web Lock and activation requests.
- Add regression coverage for remounts during both a retained Agent turn
and a pending project activation.

This is intentionally limited to the retiring V1 Agent Builder hook. It
does not change V2, backend APIs, or cross-project workspace
exclusivity.

## Root cause
V1 holds a computer-scoped Web Lock while a workspace operation is still
active. If the React workspace hook unmounted and remounted during that
lifetime, the old hook retained the lock but the new hook created a
separate coordinator and requested the same lock. After five seconds it
incorrectly showed the shared-workspace waiting state even though no
other ZooClaw page was open.

The same self-contention could happen while project activation was
pending because aborting the lock request does not release a lock that
has already been granted. The coordinator is now retained before
activation starts and can be adopted only by the exact same page
context.

## Test plan
- [x] `pnpm exec vitest run
tests/unit/app/agent-builder-workspace-activation.unit.spec.tsx` (10/10)
- [x] `bash scripts/verify-local.sh --web-static ...` (TypeScript,
targeted tests, ESLint, governance guards)
- [x] `bash scripts/verify-changed.sh`
- [x] Independent read-only review: no findings; related tests 70/70
```

### PR Body

## Summary
- Reuse the retained V1 workspace coordinator when the same `uid` / computer / project / session remounts in one page.
- Carry an in-flight activation promise and its error state across that handoff, avoiding duplicate Web Lock and activation requests.
- Add regression coverage for remounts during both a retained Agent turn and a pending project activation.

This is intentionally limited to the retiring V1 Agent Builder hook. It does not change V2, backend APIs, or cross-project workspace exclusivity.

## Root cause
V1 holds a computer-scoped Web Lock while a workspace operation is still active. If the React workspace hook unmounted and remounted during that lifetime, the old hook retained the lock but the new hook created a separate coordinator and requested the same lock. After five seconds it incorrectly showed the shared-workspace waiting state even though no other ZooClaw page was open.

The same self-contention could happen while project activation was pending because aborting the lock request does not release a lock that has already been granted. The coordinator is now retained before activation starts and can be adopted only by the exact same page context.

## Test plan
- [x] `pnpm exec vitest run tests/unit/app/agent-builder-workspace-activation.unit.spec.tsx` (10/10)
- [x] `bash scripts/verify-local.sh --web-static ...` (TypeScript, targeted tests, ESLint, governance guards)
- [x] `bash scripts/verify-changed.sh`
- [x] Independent read-only review: no findings; related tests 70/70

