---
title: "修复：模型下线迁移对已采用基线的 Agent 误判，中断的迁移现在可以续跑"
type: "Bug Fix"
priority: "中"
date: "2026-09-30"
status: "待审核"
channels: ""
---

# 修复：模型下线迁移对已采用基线的 Agent 误判，中断的迁移现在可以续跑

## 核心宣传点

修复了模型下线迁移的两个问题。一是预检只比对投影字段，而采用了既有基线的 Agent 走的是基线指纹约定，因此会被误判；现在复用统一的 Revision 匹配逻辑。二是预检会把迁移自己保存但尚未生效的 Revision 当成无关草稿，导致重新生成计划时无法续跑中断的操作；现在只读的计划阶段支持显式传入待恢复的操作 ID，可以针对未完成的 Agent 继续推进，审阅新摘要后照常走金丝雀和应用流程。恢复过程会先校验已提交变更集的归属、原始操作、基线、当前工作 Revision、生效基线，以及是否确实是「仅改模型」的源变换，全部通过才重试原有的应用路径；它不会创建第二个产品 Revision，也不会顺带发布无关草稿。同时修回了一个已提交到数据库但在引擎侧激活失败的模型 Revision。

## 分级

- 内部：P1
- 外部：C
- toB 相关：否
- 发布状态：已随正式 release 上线

## PR 说明

## Summary
Fix model retirement preflight for adopted editing baselines and recover
a model-only Revision that was committed to Mongo but failed to activate
in Engine.

#3766 has merged (8156c3048); this PR is now rebased directly onto main
as a single commit (ac65222df).

## Root cause
Preflight compared only projection keys, although adopted Agents use the
existing baseline fingerprint contract. It also treated a migration’s
own saved-but-unapplied Revision as an unrelated draft, so generating a
fresh plan could not resume the operation.

Reuse `matches_revision` and add an explicit `resume_operation_id` to
read-only planning. For example, plan unfinished Agents with
`"resume_operation_id": "github:123456789"`, the operation prefix in the
failed run’s request artifact. Review the new digest and use normal
canary/apply. Recovery verifies the committed ChangeSet’s owner,
original operation, base, current Working Revision, active base, and
exact model-only source transformation before retrying the existing
apply path. It does not create a second product Revision or publish
unrelated drafts. Engine migration uses the new workflow operation ID.

## Test plan
- 37 focused retirement and Revision-application tests passed.
- Regression tests exercise failed activation followed by a read-only
recovery plan and successful application, baseline fingerprint matching,
unrelated edits, wrong operation/owner/base, changed replacement, and
state changes after plan review.
- `bash scripts/verify-py.sh`: Ruff, formatting, Pyright and all 8
import contracts passed.
- The changed-surface verifier passed the backend gate; inherited
frontend changes from #3766 were skipped locally because this backend
worktree has no frontend dependencies. Branch quality CI was explicitly
dispatched because stacked PRs do not automatically trigger the
main-targeted quality workflow.
- No new Mongo query forms; recovery uses existing bounded repository
reads and existing commit/apply behavior. No staging or production data
was changed.

Companion Engine fix and canonical runbook update:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1495

## CI
Branch Code Quality Check passed on `80afc10dd`
(https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/35190058005).
Automated review reported no findings. Now that it targets main,
main-targeted merge validation runs on ac65222df. Locally: 216 focused
backend tests and `verify-py` pass.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `9e4e42ce1effb185436a348c32f0562afc2073d3`
- PR: #3769
- 作者：Chris@ZooClaw
- 日期：2026-09-30T12:27:22Z

### Commit Message

```
fix(models): recover retirement revisions and recognize adopted baselines (#3769)

## Summary
Fix model retirement preflight for adopted editing baselines and recover
a model-only Revision that was committed to Mongo but failed to activate
in Engine.

#3766 has merged (8156c3048); this PR is now rebased directly onto main
as a single commit (ac65222df).

## Root cause
Preflight compared only projection keys, although adopted Agents use the
existing baseline fingerprint contract. It also treated a migration’s
own saved-but-unapplied Revision as an unrelated draft, so generating a
fresh plan could not resume the operation.

Reuse `matches_revision` and add an explicit `resume_operation_id` to
read-only planning. For example, plan unfinished Agents with
`"resume_operation_id": "github:123456789"`, the operation prefix in the
failed run’s request artifact. Review the new digest and use normal
canary/apply. Recovery verifies the committed ChangeSet’s owner,
original operation, base, current Working Revision, active base, and
exact model-only source transformation before retrying the existing
apply path. It does not create a second product Revision or publish
unrelated drafts. Engine migration uses the new workflow operation ID.

## Test plan
- 37 focused retirement and Revision-application tests passed.
- Regression tests exercise failed activation followed by a read-only
recovery plan and successful application, baseline fingerprint matching,
unrelated edits, wrong operation/owner/base, changed replacement, and
state changes after plan review.
- `bash scripts/verify-py.sh`: Ruff, formatting, Pyright and all 8
import contracts passed.
- The changed-surface verifier passed the backend gate; inherited
frontend changes from #3766 were skipped locally because this backend
worktree has no frontend dependencies. Branch quality CI was explicitly
dispatched because stacked PRs do not automatically trigger the
main-targeted quality workflow.
- No new Mongo query forms; recovery uses existing bounded repository
reads and existing commit/apply behavior. No staging or production data
was changed.

Companion Engine fix and canonical runbook update:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1495

## CI
Branch Code Quality Check passed on `80afc10dd`
(https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/35190058005).
Automated review reported no findings. Now that it targets main,
main-targeted merge validation runs on ac65222df. Locally: 216 focused
backend tests and `verify-py` pass.
```

来源：SerendipityOneInc/ecap-workspace @ 9e4e42ce，PR #3769，作者 Chris@ZooClaw。
