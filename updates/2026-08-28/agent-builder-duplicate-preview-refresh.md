---
title: "修复：Agent Builder 连点「刷新预览」会跑出两份，卡住还得人工修数据"
type: "Bug Fix"
priority: "中"
date: "2026-08-28"
status: "待审核"
channels: ""
---

# 修复：Agent Builder 连点「刷新预览」会跑出两份，卡住还得人工修数据

## 核心宣传点

点击「刷新预览」后，前端在请求刚被接受时就把按钮重新点亮了，可实际的打包和部署还在跑——再点一下就会创建出第二个迭代，把还在收尾的那次测试运行顶掉。现在只要预览正处于打包或部署中，刷新按钮就保持禁用，后端也会拒绝重复创建（新旧两种运行时都拦）。另外，如果某次预览创建卡在 packaging 或 deploying_test 状态超过 30 分钟且没有关联的测试运行，系统会自动把它判为失败让你重试，不再需要人工去修数据。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `7ead01dbca73fe752da3965bd8385eee6811ddf1`
- PR: #3571
- 作者: kaka-srp
- 日期: 2026-08-28T08:37:22Z

### Commit Message

```
fix(agent-builder): prevent duplicate preview refresh runs (#3571)

## Summary
- Disable **Refresh preview** while an Agent Builder Preview is already
packaging or deploying.
- Reject duplicate backend test-iteration creation for both legacy and
Engine v2 runtimes.
- Recover v2 Preview creation that remains in `packaging` or
`deploying_test` without a TestRun for 30 minutes, so the user can retry
instead of requiring manual data repair.

## Root cause
The frontend enabled Refresh again as soon as the initiating `202`
request completed, even though the persisted Project was still packaging
or deploying. The backend also exempted Engine v2 from its in-progress
guard, so a repeated click created a second iteration and superseded a
TestRun that could still be finalizing.

Blocking duplicate creation alone would strand a Project if a worker
stopped before linking its TestRun. State polling now converges that
stale, unowned creation to a failed Project and iteration after the
existing 30-minute package-operation TTL.

## Test plan
- [x] Backend start-iteration tests: 4 passed.
- [x] Backend stale-creation recovery tests: 4 passed, covering both
`packaging` and `deploying_test`.
- [x] Frontend Preview workspace/state tests: 8 passed.
- [x] Targeted Ruff, Ruff format, Pyright, and ESLint checks passed.
- [ ] Full local suites were not run; CI is authoritative.

## Known follow-up
- Capacity-reservation cleanup behavior for a duplicate request that
encounters a `recovery_required` slot is intentionally unchanged in this
PR.
```

### PR Description

```
## Summary
- Disable **Refresh preview** while an Agent Builder Preview is already packaging or deploying.
- Reject duplicate backend test-iteration creation for both legacy and Engine v2 runtimes.
- Recover v2 Preview creation that remains in `packaging` or `deploying_test` without a TestRun for 30 minutes, so the user can retry instead of requiring manual data repair.

## Root cause
The frontend enabled Refresh again as soon as the initiating `202` request completed, even though the persisted Project was still packaging or deploying. The backend also exempted Engine v2 from its in-progress guard, so a repeated click created a second iteration and superseded a TestRun that could still be finalizing.

Blocking duplicate creation alone would strand a Project if a worker stopped before linking its TestRun. State polling now converges that stale, unowned creation to a failed Project and iteration after the existing 30-minute package-operation TTL.

## Test plan
- [x] Backend start-iteration tests: 4 passed.
- [x] Backend stale-creation recovery tests: 4 passed, covering both `packaging` and `deploying_test`.
- [x] Frontend Preview workspace/state tests: 8 passed.
- [x] Targeted Ruff, Ruff format, Pyright, and ESLint checks passed.
- [ ] Full local suites were not run; CI is authoritative.

## Known follow-up
- Capacity-reservation cleanup behavior for a duplicate request that encounters a `recovery_required` slot is intentionally unchanged in this PR.

```
