---
title: "修复：Pro / Ultra 版 Agent 应用自进化版本时不再报环境构建 404"
type: "Bug Fix"
priority: "高"
date: "2026-10-08"
status: "待审核"
channels: ""
---

# 修复：Pro / Ultra 版 Agent 应用自进化版本时不再报环境构建 404

## 核心宣传点

修复了高配 Agent 套用历史版本失败的问题。此前应用一个已保存的自进化 Revision 时，Pro 和 Ultra 规格的 Agent 即使对应环境版本已经就绪，也可能报出环境构建 404。原因是就绪校验一律去查 Starter 规格的构建，而环境物化只会为 Agent 实际所属规格构建，Starter 变体根本不存在。现在改为按 Engine 上报的沙箱资源规格做校验，和环境物化、预览保持一致；当规格信息缺失时仍走原有的 Starter 兜底。已覆盖 Starter、Pro、Ultra 与规格缺失兜底四种情况，重复应用同一个成功 Revision 保持幂等。

## 分级

- 内部：P1
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `789e9b4226dbdbe29938b961838ff4573e807875`
- PR: #4032
- 作者：kaka-srp
- 日期：2026-10-08T07:54:16Z

### Commit Message

```
fix(agents): validate environment using runtime resource class (#4032)

## Summary

Applying a saved self-evolving Agent Revision could fail with an
environment-build 404 for Pro or Ultra Agents even when their exact
environment version was ready. Validate the environment using the
Agent's Engine-reported Sandbox resource class, matching environment
materialization and preview; retain the existing Starter fallback when
the projection is absent.

## Root cause

The application readiness gate always queried the Starter build.
Environment materialization builds only the actual Agent class, so the
requested Starter variant could be missing. The Revision was already
saved while the active runtime configuration remained unchanged.

## Test plan

- [x] New regressions run through the real readiness gate and
application path. Before the fix, the selected tests produced 6 failures
and 2 passes; after the fix they pass.
- [x] Cover Starter, Pro, Ultra and the absent-class fallback; a missing
unrelated class must not block a ready environment. Reapplying a
successful Revision remains idempotent.
- [x] Cover building/failed dependencies blocking activation and an
empty-operations Settings retry applying the same saved Revision after
readiness recovers.
- [x] Six related test files: 101 passed.
- [x] `bash scripts/verify-local.sh --py-static`: Ruff, formatting,
Pyright and all eight import contracts passed.
- [ ] Staging and production recovery after backend deployment; no live
Agent was modified during implementation.
```

