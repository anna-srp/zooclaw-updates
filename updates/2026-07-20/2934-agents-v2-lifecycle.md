---
title: "Agent 管理增强：支持对引擎版 Agent 卸载与更新"
type: "产品基础功能更新"
priority: "中"
date: "2026-07-20"
status: "待审核"
channels: ""
---

## 核心宣传点

Agent 生命周期管理增强：现在可以对运行在 ZooClaw Engine 上的 Agent 进行卸载和更新，并且可以从界面移除处于错误/安装失败状态的 Agent 行，恢复更方便。（当前面向灰度用户）

### 原始内容

**Commit message:**

```
feat(web): branch agent uninstall and update on workspace runtime (#2934)

## Summary

**Agents v2 phase 2, P2-3** — lifecycle branching. Uninstall and update
now work for engine agents: the lifecycle initiators branch on the
workspace row's `runtime` — engine rows use the existing authenticated
claw proxy for `/agents/{workspace_id}/uninstall|update`, while computer
rows keep the v1 leg byte-for-byte. This also delivers the error-row
recovery flagged by #2927's review: a stuck engine row (`error` /
`install_failed`) is now removable from the UI.

Spec: `docs/superpowers/specs/2026-07-16-agents-v2-install-phase2.md`
(locked decision: lifecycle branches on row `runtime`, client-passed as
routing info — wrong routing fails safe via ownership-scoped 404; no
allowlist involvement)
Plan:
`docs/superpowers/plans/2026-07-17-agents-v2-p2-3-lifecycle-branching.md`
Linear: https://linear.app/srpone/issue/ECA-1259/... (phase-2 successor
work)

### Backend semantics (verified read-only before implementation)

Engine uninstall/update are SYNCHRONOUS — uninstall returns terminal
`uninstalled`/`deleted`, update returns `active` — so the engine leg
needs no polling. Uninstall is accepted from `error` and post-creation
`install_failed` rows (the recovery case); update only from `active`.
Early `install_failed` rows without a persisted identity are excluded
from the unified list and can't reach this path.

### What's in it

- **Shared claw proxy lifecycle calls**: `uninstallEngineAgent` /
`updateEngineAgent` call
`/api/claw/agents/{workspaceId}/uninstall|update` through
`callClawInterfaceAPI`; the two redundant one-line lifecycle BFF routes
and their route-only tests were removed. The install start route keeps
its dedicated BFF because it owns install-specific policy.
- **Client helpers** (`src/services/agent-install.ts`): no polling (sync
backend), with best-effort unified-cache refresh scoped to the
initiating uid. The claw proxy's 30s timeout is intentional; work that
cannot meet it must become async rather than approach Cloudflare's 100s
synchronous connection ceiling.
- **Branching**: `useAgentActions.fireAgent`/`updateAgent` and publish's
`useAgentInstallToggle`/`useAgentUpdateAction` branch on the row's
runtime — engine ops use the exact unified-row `workspace_id`, fail fast
with domain errors, and ignore unrelated computer/WebSocket readiness;
computer flows (waits, refreshes, sentinels) are byte-identical.
- **Lifecycle UI gates lifted** on manager/detail/publish: engine rows
expose uninstall from `error` and addressable post-creation
`install_failed` rows, and update only from `active` rows. Fire/update
confirmation revalidates against the latest workspace row; engine update
never routes into the computer-only `/new`-chat flow.
- **Stateful mock**: engine uninstall/update lifecycle in the mock
backend (update advances `submission_id`, clears stale errors; recovery
statuses covered).

### Deliberately out

Start/stop UI (spec-deferred; `startEngineAgent` exists from P2-2),
AgentBuilderClient (dedicated builder computer — always v1), bossclaw +
landing (deferred initiators), vertical-pack, engine settings panel
(P2-5).

### Rollout

Frontend only; backend routes already live (#2871/#2923). Engine legs
only trigger for rows that already exist as engine installs (allowlisted
dogfood). Concurrent-PR note: developed in parallel with #2932 (engine
chat) on disjoint function surfaces of the shared files; whichever
merges second absorbs main normally.

Size override rationale: after consolidating duplicate review tests,
this coherent lifecycle slice is 3,104 counted lines, 104 lines (3.5%)
over the 3,000-line threshold. Splitting it would separate the shared
selector/action-eligibility/cache-scope contracts from their
manager/detail/publish consumers and regression coverage.

## Test plan

- [x] Task-1 read-only backend semantics verification (report
in-worktree)
- [x] TDD review regression run: 5 spec files / 218 tests green (6
targeted failures observed before implementation)
- [x] `bash scripts/verify-web.sh` — full guards + tsc + 523 unit files
(7021 passed, 1 skipped, 1 todo) + eslint
- [x] Coverage over thresholds; knip clean; jscpd (`--no-gitignore` real
runs) under thresholds
- [ ] CI `code-quality / lint-and-test`
- [ ] Staging: engine uninstall of an `error` row + update of an
`active` row (recovery + happy path)
```

**PR body:**

## Summary

**Agents v2 phase 2, P2-3** — lifecycle branching. Uninstall and update now work for engine agents: the lifecycle initiators branch on the workspace row's `runtime` — engine rows use the existing authenticated claw proxy for `/agents/{workspace_id}/uninstall|update`, while computer rows keep the v1 leg byte-for-byte. This also delivers the error-row recovery flagged by #2927's review: a stuck engine row (`error` / `install_failed`) is now removable from the UI.

Spec: `docs/superpowers/specs/2026-07-16-agents-v2-install-phase2.md` (locked decision: lifecycle branches on row `runtime`, client-passed as routing info — wrong routing fails safe via ownership-scoped 404; no allowlist involvement)
Plan: `docs/superpowers/plans/2026-07-17-agents-v2-p2-3-lifecycle-branching.md`
Linear: https://linear.app/srpone/issue/ECA-1259/... (phase-2 successor work)

### Backend semantics (verified read-only before implementation)

Engine uninstall/update are SYNCHRONOUS — uninstall returns terminal `uninstalled`/`deleted`, update returns `active` — so the engine leg needs no polling. Uninstall is accepted from `error` and post-creation `install_failed` rows (the recovery case); update only from `active`. Early `install_failed` rows without a persisted identity are excluded from the unified list and can't reach this path.

### What's in it

- **Shared claw proxy lifecycle calls**: `uninstallEngineAgent` / `updateEngineAgent` call `/api/claw/agents/{workspaceId}/uninstall|update` through `callClawInterfaceAPI`; the two redundant one-line lifecycle BFF routes and their route-only tests were removed. The install start route keeps its dedicated BFF because it owns install-specific policy.
- **Client helpers** (`src/services/agent-install.ts`): no polling (sync backend), with best-effort unified-cache refresh scoped to the initiating uid. The claw proxy's 30s timeout is intentional; work that cannot meet it must become async rather than approach Cloudflare's 100s synchronous connection ceiling.
- **Branching**: `useAgentActions.fireAgent`/`updateAgent` and publish's `useAgentInstallToggle`/`useAgentUpdateAction` branch on the row's runtime — engine ops use the exact unified-row `workspace_id`, fail fast with domain errors, and ignore unrelated computer/WebSocket readiness; computer flows (waits, refreshes, sentinels) are byte-identical.
- **Lifecycle UI gates lifted** on manager/detail/publish: engine rows expose uninstall from `error` and addressable post-creation `install_failed` rows, and update only from `active` rows. Fire/update confirmation revalidates against the latest workspace row; engine update never routes into the computer-only `/new`-chat flow.
- **Stateful mock**: engine uninstall/update lifecycle in the mock backend (update advances `submission_id`, clears stale errors; recovery statuses covered).

### Deliberately out

Start/stop UI (spec-deferred; `startEngineAgent` exists from P2-2), AgentBuilderClient (dedicated builder computer — always v1), bossclaw + landing (deferred initiators), vertical-pack, engine settings panel (P2-5).

### Rollout

Frontend only; backend routes already live (#2871/#2923). Engine legs only trigger for rows that already exist as engine installs (allowlisted dogfood). Concurrent-PR note: developed in parallel with #2932 (engine chat) on disjoint function surfaces of the shared files; whichever merges second absorbs main normally.

Size override rationale: after consolidating duplicate review tests, this coherent lifecycle slice is 3,104 counted lines, 104 lines (3.5%) over the 3,000-line threshold. Splitting it would separate the shared selector/action-eligibility/cache-scope contracts from their manager/detail/publish consumers and regression coverage.

## Test plan

- [x] Task-1 read-only backend semantics verification (report in-worktree)
- [x] TDD review regression run: 5 spec files / 218 tests green (6 targeted failures observed before implementation)
- [x] `bash scripts/verify-web.sh` — full guards + tsc + 523 unit files (7021 passed, 1 skipped, 1 todo) + eslint
- [x] Coverage over thresholds; knip clean; jscpd (`--no-gitignore` real runs) under thresholds
- [ ] CI `code-quality / lint-and-test`
- [ ] Staging: engine uninstall of an `error` row + update of an `active` row (recovery + happy path)

