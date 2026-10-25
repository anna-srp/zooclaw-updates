---
title: "修复：卸载或删除 Engine Agent 时会回收其占用的团队席位，不再白白占名额"
type: "Bug Fix"
priority: "高"
date: "2026-10-12"
status: "待审核"
channels: ""
---

# 修复：卸载或删除 Engine Agent 时会回收其占用的团队席位，不再白白占名额

## 核心宣传点

此前用户卸载 Engine Agent 或在 Agent 开发里删除 Agent 后，对应 Agent Bot 仍占着组织团队的席位，成员名额被持续消耗。本次发布后的卸载与删除都会释放该席位，且不需上调团队成员上限。两条路径最终收敛到同一处，会与终态工作区状态原子写入清理记录，失败记录由调度器按租约退避重试。只要还有运行中的 Pack Test 或其他在用工作区引用该 Bot 就保留席位；Bot 账号、频道和历史消息均保留。

## 分级

- 内部：P1
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## 备注

PR 仍为 draft，staging 与 CSFLE 相关验收项未勾选完；历史遗留的孤儿席位数据不在本次范围内，需另行清理。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `cd4fca3ecdc6c0c5db2c614021a91f378365b695`
- PR: #4025
- 作者：tim-srp
- 日期：2026-10-12T11:20:47Z

### Commit Message

```
fix(claw-interface): release Mattermost seats on agent uninstall (#4025)

## Summary

Release the Mattermost Org-team seat held by an Agent Bot when a user
uninstalls an Engine Agent or deletes it from Agent development **after
this release**, without raising the Team member limit. Historical orphan
data is out of scope. This is a **draft** until the staging/CSFLE gates
below are checked.

- **Covered paths:** the ordinary Engine Agent uninstall and the
Agent-development delete. Both finish in `uninstall_engine_agent`, which
now persists an `integration_cleanup` record atomically with the
terminal workspace state. One attempt runs inline; the existing
scheduler pattern retries due rows with a Mongo lease, backoff and
recorded stage/error; rows past 12 attempts stay queryable and keep
retrying daily.
- Cleanup removes the Agent's ACS channel binding and leaves the Org
Team unless a live Pack Test run or another workspace row that is or can
become active still names the Bot (any computer-runtime row keeps the
seat, fail-safe). Retired Engine co-owners never block, because Engine
tombstones are never reclaimed. For an Engine sole owner the Bot's
access tokens are also revoked. Bot accounts, channels and historical
posts are retained.
- Cleanups that fail 12 times keep retrying daily and raise one
aggregate PagerDuty incident (`agent-integration-cleanup-stuck`) that
auto-resolves when they converge.
- **Not covered:** the service-token `DELETE /service/v1/agents/{id}`
route is unchanged from `main` (Engine delete plus best-effort ACS
channel cleanup). An Agent deleted there does not enter this cleanup;
that route is left for a separate change.

## Scope changes after merging main

- **Merged `origin/main` (#4028, FastClaw V1 removal).** #4028 deleted
the retired computer-runtime uninstall path
(`agent_uninstall_service.py`) and `mattermost_reconcile.py`, so this
PR's computer-runtime pieces went with them: the channel stage is
Engine-only (a no-op for computer-runtime rows), and the
computer-runtime reinstall fence (`install_claim_filter` /
`_INSTALL_SET_FIELDS` changes and the reinstall-race test) was reverted
to `main`, since no retained flow reinstalls those rows.
- **`ed811e17`: the service-token delete route is left unchanged.** The
earlier delete-intent flow for that route was removed to keep this PR to
the uninstall paths: `engine_delete_intent_service` and its tests, the
`reconcile_engine_delete_intents` job, the `engine_delete_intent` field
and index, and the retire/intent repo functions.
`app/routes/service_api/_agents.py` is identical to `main`, and the
stuck alert counts integration cleanups only.

## Root cause

Normal Agent uninstalls stopped the Agent and removed or soft-deleted
channel resources but never removed the associated Mattermost Bot from
the Org Team. Repeated create → chat → uninstall cycles accumulated Team
members and eventually blocked a new Bot's first Team join. Old open PR
#3567 documents the same leak for Pack Test and explicitly notes
ordinary Agent uninstalls as a separate gap; this PR addresses the
ordinary uninstall paths on current `main`.

## Test plan

Re-run on `ed811e17` unless noted:

- [x] `bash scripts/verify-py.sh` (ruff, format, pyright, import-linter)
- [x] Backend ci-lint guards (8/8)
- [x] Full backend unit suite: 11,962 passed, 5 skipped, 0 failed
- [x] Full BDD suite against local MongoDB: 255 passed, 0 failed, 0
skipped
- [x] Focused tests for shared Bots (incl. retired Engine co-owners),
Engine token revocation, Pack Test ownership, idempotency, partial
failure / backoff / daily retry / alerting, lease exclusion and stage
fencing
- [x] Staging CSFLE validation on the existing claw-interface Pod, run
on the pre-merge sources (`b667c5c6`): PR database sources exercised
against two isolated, randomly named temporary collections (74/74 query,
CAS, write, and index checks passed); both collections were dropped and
their absence verified. A separate read-only check found no collection
validators or field-encryption rules on the two real collections. The PR
application code itself is not deployed. Since then the remaining query
forms are unchanged; the delete-intent queries were removed and the
install claim filter is back to `main`.
- [ ] Staging acceptance: repeat create → chat → uninstall, and create →
chat → Agent-development delete; verify Team count returns to baseline
for sole-owner Bots, history remains and an Engine reinstall provisions
a fresh Bot. Shared Bot seats should remain.

## Known limitations

- **The service-token `DELETE /service/v1/agents/{id}` route is out of
scope.** It keeps `main`'s behavior, so an Engine Agent deleted through
it still keeps its Org-team seat.
- **Bot accounts are not deactivated or deleted, and computer-runtime
Bot tokens are kept.** Engine sole-owner tokens are revoked. Account
deactivation awaits a product decision.
- **A shared Bot whose remaining co-owner is a computer-runtime row
keeps its seat** (fail-safe). A V1-to-V2 migration writer outside this
repository could create a new owner during cleanup; that operational
race is not controlled here.
- Pre-terminal `uninstall_failed` (for example Engine stop failure)
still requires a user retry. Engine uninstall stays stop-only (Sandbox
paused, not released via `:cleanup`) pending a product decision.
- ACS listing of soft-deleted channels still needs staging confirmation.

No real business collections or production data were mutated, and the PR
was not deployed. The staging probe created and removed only two
isolated temporary collections; zero remained after verification.

🤖 Implemented and reviewed with [Claude
Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
```

