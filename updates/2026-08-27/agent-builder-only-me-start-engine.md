---
title: "修复：Agent Builder「仅自己可见」发布后 Agent 没被启动，装好了却用不了"
type: "Bug Fix"
priority: "中"
date: "2026-08-27"
status: "待审核"
channels: ""
---

# 修复：Agent Builder「仅自己可见」发布后 Agent 没被启动，装好了却用不了

## 核心宣传点

以「仅自己可见」发布 Agent 时，系统会把工作区显示为「活跃」就当作运行环境已经跑起来了，于是跳过了最后的启动步骤——结果 Agent 明明显示安装完成，实际却没运行。现在每一次「仅自己可见」的安装都会完成并真正启动运行环境；如果检测到已有安装正在进行中，会先等它结束、更新到刚发布的版本，再完成启动。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `5ed3dc2f6c30359236818b510657c7055153ced3`
- PR: #3547
- 作者: sharplee-srp
- 日期: 2026-08-27T09:24:04Z

### Commit Message

```
fix(agent-builder): start engine after only-me publish (#3547)

## Summary
- complete every Engine Only-me installation so an `active` Workspace is
also started
- wait for an in-progress Engine install, then update to the newly
published Pack version before completing and starting it
- preserve the existing computer-runtime install/update flow and add
regression coverage for both runtimes

## Root cause

Agent Builder treated the product Workspace status `active` as proof
that an Engine runtime was already running. A newly installed Engine
therefore skipped `completeEngineInstall` and `/start`. Existing Engine
installations with a stale submission ran `/update` after the completion
decision and were never started either. Reordering those calls must also
preserve the backend's active-workspace precondition, so an existing
`installing` Engine is awaited before `/update`.

## Test plan
- [x] `pnpm exec vitest run
tests/unit/services/agent-builder-publish.unit.spec.ts`
- [x] `bash scripts/verify-web.sh
web/app/src/services/agent-builder-publish.ts
web/app/tests/unit/services/agent-builder-publish.unit.spec.ts`
- [x] `bash scripts/verify-changed.sh`
```

### PR Description

```
## Summary
- complete every Engine Only-me installation so an `active` Workspace is also started
- wait for an in-progress Engine install, then update to the newly published Pack version before completing and starting it
- preserve the existing computer-runtime install/update flow and add regression coverage for both runtimes

## Root cause

Agent Builder treated the product Workspace status `active` as proof that an Engine runtime was already running. A newly installed Engine therefore skipped `completeEngineInstall` and `/start`. Existing Engine installations with a stale submission ran `/update` after the completion decision and were never started either. Reordering those calls must also preserve the backend's active-workspace precondition, so an existing `installing` Engine is awaited before `/update`.

## Test plan
- [x] `pnpm exec vitest run tests/unit/services/agent-builder-publish.unit.spec.ts`
- [x] `bash scripts/verify-web.sh web/app/src/services/agent-builder-publish.ts web/app/tests/unit/services/agent-builder-publish.unit.spec.ts`
- [x] `bash scripts/verify-changed.sh`

```

---
