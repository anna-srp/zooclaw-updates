---
title: "fix(agents): persist exact environment pins in revisions (#3782)"
type: "产品基础功能更新"
priority: "低"
date: "2026-09-17"
status: "待审核"
channels: ""
---

# fix(agents): persist exact environment pins in revisions (#3782)

## 核心宣传点

Agent 版本会记住当时实际使用的运行环境版本，后续复用、预览、发布都锁定同一版本，不再被悄悄升级到最新环境。

## PR 说明

## Summary

- Persist Engine's actual resolved environment ID/version in the initial Agent Revision.
- Require exact pins when reusing a Revision or rendering Build/Settings/Preview/Apply candidates; never implicitly reselect the latest environment during an ordinary edit.
- Materialize an explicit environment when the last custom dependencies are removed, and retain the existing explicit-rebuild protection.
- Keep legacy data repair offline and out of this PR. Only in-use Agents are in scope for the separate repair; uninstalled Agents are excluded.

## Root cause

Default-environment creation let Engine resolve a concrete version, but R0 persisted the original null input rather than the resolved pin. Subsequent metadata-only edits inherited null and could resolve a newer default. Once a sandbox locked the old environment, activation correctly rejected that accidental upgrade with `environment_rebuild_required`.

## Review

Completed the `code-review` workflow against `origin/main`: design/scope, completeness/reliability, and regressions/side effects. Checked every candidate-rendering caller, initial creation/retries, inherited pending Revision pins, and shared updates.

Follow-up automated review found a real missing guard: legacy source Revisions with null pins could still enter shared install/link copy/fork as a fresh default-environment creation. Fixed the common `system_environment_version` boundary to reject incomplete pins, including custom-environment sources. Fork validates before its durable reservation as well, so invalid source cannot leave a failed empty copy. Added install/copy/fork regression assertions (including no reservation on rejection) and re-reviewed the correction.

The separate question about asynchronous default resolution was checked against Engine source: `createAgentTx` awaits `resolveAgentEnvironment` and `renderConfig`, then stores the rendered config and environment pin in the creation transaction; Agent detail projects `resolved_environment` from that persisted rendered config. No new polling/fallback is needed.

## Test plan

- [x] Agent development, baseline, shared-update, authoring-operation, shared-link-copy, and adopted-sharing unit suites: **459 passed**.
- [x] Final pre-reservation correction: **61 directly affected tests passed**.
- [x] `bash scripts/verify-local.sh --py-static`: Ruff, format, Pyright, and import contracts pass.
- [x] Pre-commit checks pass, including file length, complexity, dependency consistency, repository contracts, and type checks.
- [x] Regression assertions for R0 resolved-pin persistence, exact inheritance in commit/preview/apply retry, null/partial pin rejection, and dependency removal.
- [ ] CI on the PR merge ref.
- [ ] Deployment and live smoke verification (not performed by this PR).

## Rollout boundary

Backend-only change; no Engine or frontend deployment dependency. Before enabling the strict guard on existing in-use Agents, complete the separately authorized offline pin backfill using exact immutable config evidence. Coordinate rollout/backfill so the old writer does not leave new incomplete records. Without backfill, an incomplete legacy Revision will fail closed rather than silently upgrade.

No production data, sandbox, or active runtime configuration was modified in preparing this PR. General Build rebuild-confirmation UX and async image continuation's turn-to-Revision lookup are separate work, not claimed fixed here.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `2527b959c2b01aa86e1225a8d4133e696cabcd49`
- PR: #3782
- 作者：kaka-srp
- 日期：2026-09-17T12:49:49Z

### Commit Message

```
fix(agents): persist exact environment pins in revisions (#3782)

## Summary

- Persist Engine's actual resolved environment ID/version in the initial
Agent Revision.
- Require exact pins when reusing a Revision or rendering
Build/Settings/Preview/Apply candidates; never implicitly reselect the
latest environment during an ordinary edit.
- Materialize an explicit environment when the last custom dependencies
are removed, and retain the existing explicit-rebuild protection.
- Keep legacy data repair offline and out of this PR. Only in-use Agents
are in scope for the separate repair; uninstalled Agents are excluded.

## Root cause

Default-environment creation let Engine resolve a concrete version, but
R0 persisted the original null input rather than the resolved pin.
Subsequent metadata-only edits inherited null and could resolve a newer
default. Once a sandbox locked the old environment, activation correctly
rejected that accidental upgrade with `environment_rebuild_required`.

## Review

Completed the `code-review` workflow against `origin/main`:
design/scope, completeness/reliability, and regressions/side effects.
Checked every candidate-rendering caller, initial creation/retries
```
