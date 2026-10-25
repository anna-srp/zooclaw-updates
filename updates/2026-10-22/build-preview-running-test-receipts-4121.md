---
title: "修复：Build 预览测试还在跑时不再误报超时，可继续观察同一次执行"
type: "Bug Fix"
priority: "高"
date: "2026-10-22"
status: "待审核"
channels: ""
---

# 修复：Build 预览测试还在跑时不再误报超时，可继续观察同一次执行

## 核心宣传点

当 Build 预览的测试执行超过网关等待窗口时，旧回执会直接报超时，哪怕子任务其实还在运行，用户只能重跑一次。现在这种情况会返回「运行中」状态和一个不透明的测试引用，Build 可以继续观察同一次被固定的执行，而不会再创建一次新执行。回执里还会带上有界的既有工具事件证据以及原始源码摘要和配置版本，便于定位问题；续查前会校验 Agent 与 Build 会话范围，引用缺失、过期或属于其他 Agent 时返回一致的受限错误。创建会话的请求体与幂等键对已发布的调用方保持兼容。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## 备注

续查元数据通过既有 Engine PATCH 接口注册，需与 Engine 侧保持一致。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `b6375f431aa73b3b60d0f03aa294e12070f6cd64`
- PR: #4121
- 作者：kaka-srp
- 日期：2026-10-22T14:01:05Z

### Commit Message

```
fix(authoring): preserve pending tests and expose bounded receipts (#4121)

## Summary
When a Build preview outlives the gateway wait window, the old receipt
reports a timeout even while its child is still running. Return
`running`, `passed: null`, and an opaque `test_ref` so Build can observe
that same pinned test without creating another execution.

Receipts now include bounded existing tool-event evidence and the
original source digest/config version. Continuation checks the Agent and
Build-session scope before reading events. Keep the original
session-create body/idempotency key compatible with deployed callers;
register continuation metadata through the existing Engine PATCH API.
Drain full legacy event pages without an extra poll delay.
Missing/stale/other-Agent test references return the same scoped domain
404 as provenance rejections; unrelated upstream failures retain their
existing semantics.

Companion Engine PR:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/2092 (tool
schema and proportional verification guidance). Deploy this backend
before enabling the Engine continuation schema. No migrations, new
dependencies, model changes, or production data mutations.

## Test plan
- [x] 156 focused Python cases: authoring, evaluation, continuation
scope, idempotent metadata-write recovery, client wire contract, source
security, turn snapshot, and Skill evaluation.
- [x] `bash scripts/verify-py.sh`: ruff, formatting, Pyright, and all
eight import contracts.
- [x] Astra local review and targeted re-review: pagination and
missing-reference error mapping findings fixed; no remaining local
findings. The real EngineClient/HTTP legacy-page regression fails before
the fix (one unexpected sleep) and passes after it. For error mapping, a
one-line negative control fails exactly the missing-reference case while
17 receipt cases pass; restoring it passes all 18. Real HTTP 409/503
cases confirm upstream errors are not rewritten as missing references.
- [x] Real local Engine/Temporal/E2B/model functional run: six
continuation assertions; twelve paired Build runs, plus twelve
independent ordinary tasks. See
`docs/research/2026-10-22-build-execution-efficiency-validation.md` with
the retained key statistics and experimental source fingerprints.

In this exploratory two-repeat-per-case pilot, normal-edit model calls
fell from 33 to 27 with the same four test invocations; slow-preview
cases saved successfully in 2/2 optimized runs versus 0/2 baseline runs.
These are small local samples: ECAP repositories were in memory,
slow-preview waits were injected at one second, and the original
long-history/production/Mongo-CSFLE/browser/channel path was not
replayed. Experimental hashes preserve the snapshot before the later
pagination correction. No production speedup guarantee.

Raw experiment JSON has been removed from the PR. The report retains the
results, limits, cleanup conclusions, and source fingerprints; the
change no longer requires a size exception.
```

