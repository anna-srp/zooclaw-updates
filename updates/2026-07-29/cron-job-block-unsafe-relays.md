---
title: "cron-job 技能安全加固：拦截把定时任务当作消息中继的不安全用法"
type: "Skill 上架/更新"
priority: "高"
date: "2026-07-29"
status: "待审核"
channels: ""
---

## 核心宣传点

定时任务（cron-job）技能新增安全防护：当存储的任务负载试图用 `openclaw message send` 或把 `sessions_send` 当作常驻会话中继时会被拦截，并提供只读的隐患扫描（用稳定的隐患码报告、不回显原始负载文本），让定时任务更安全、可诊断。

## 原始内容

- 仓库：SerendipityOneInc/ecap-skills
- commit：db36893defa94c55bfd003b259a5b012b0145b08
- PR：#245
- 日期：2026-07-29T07:06:38Z

### Commit message

```
fix(cron-job): block unsafe message relays (#245)

## Summary

- Make `cron-job` discoverable for creating, updating, repairing, and
diagnosing scheduled jobs, and define it as the Cron workflow source of
truth.
- Block preparation when a stored payload invokes `openclaw message
send` or uses `sessions_send` as a persistent-session relay.
- Add a read-only stored-job scan that reports stable hazard codes
without emitting raw payload text.
- Preserve explicit provider-consistency checks and require confirmation
instead of guessing when routing is ambiguous.
- Document the routing decision order and the residual risk that direct
production Cron mutations can still bypass the workflow until a runtime
guard exists.

## Root cause

The messaging CLI bypasses the in-process `message` tool's routing
policy and produces no `messageToolSentTo` evidence. The incident jobs
previously appeared healthy only while their orchestration content used
that CLI path. A later repair attempted `sessions_send`, which cannot
relay from an isolated Cron into an unrelated persistent session under
`tools.sessions.visibility=tree`.

Detailed Cron behavior also needs one authoritative home. Agent-level
policies now state when to invoke this skill and provide only a minimal
fallback when it is unavailable.

## Impact

Unsafe messaging paths are rejected before scheduler mutation and can be
flagged in read-only job snapshots. Provider/account mismatches and
ambiguous routes stop for confirmation, and session-tree isolation is
not relaxed.

This PR adds procedural workflow enforcement only; it does not claim to
prevent direct in-process Cron tool bypasses at runtime.

## Validation

- `python3 -m py_compile cron-job/scripts/cron_workflow.py`
- `python3 cron-job/scripts/cron_workflow.py --self-test` — 139
assertions passed
- `uv run --with pyyaml python3 .github/scripts/lint_skills.py` — passed
with 15 pre-existing warnings
- Exercised the new `--scan-jobs` CLI against a safe/unsafe fixture.
- `git diff --check`

## Companion changes

Companion PRs reduce `openclaw-docker` and `ecap-agent-pack` policies to
skill delegation plus a minimal safe fallback.
```

### PR body

## Summary

- Make `cron-job` discoverable for creating, updating, repairing, and diagnosing scheduled jobs, and define it as the Cron workflow source of truth.
- Block preparation when a stored payload invokes `openclaw message send` or uses `sessions_send` as a persistent-session relay.
- Add a read-only stored-job scan that reports stable hazard codes without emitting raw payload text.
- Preserve explicit provider-consistency checks and require confirmation instead of guessing when routing is ambiguous.
- Document the routing decision order and the residual risk that direct production Cron mutations can still bypass the workflow until a runtime guard exists.

## Root cause

The messaging CLI bypasses the in-process `message` tool's routing policy and produces no `messageToolSentTo` evidence. The incident jobs previously appeared healthy only while their orchestration content used that CLI path. A later repair attempted `sessions_send`, which cannot relay from an isolated Cron into an unrelated persistent session under `tools.sessions.visibility=tree`.

Detailed Cron behavior also needs one authoritative home. Agent-level policies now state when to invoke this skill and provide only a minimal fallback when it is unavailable.

## Impact

Unsafe messaging paths are rejected before scheduler mutation and can be flagged in read-only job snapshots. Provider/account mismatches and ambiguous routes stop for confirmation, and session-tree isolation is not relaxed.

This PR adds procedural workflow enforcement only; it does not claim to prevent direct in-process Cron tool bypasses at runtime.

## Validation

- `python3 -m py_compile cron-job/scripts/cron_workflow.py`
- `python3 cron-job/scripts/cron_workflow.py --self-test` — 139 assertions passed
- `uv run --with pyyaml python3 .github/scripts/lint_skills.py` — passed with 15 pre-existing warnings
- Exercised the new `--scan-jobs` CLI against a safe/unsafe fixture.
- `git diff --check`

## Companion changes

Companion PRs reduce `openclaw-docker` and `ecap-agent-pack` policies to skill delegation plus a minimal safe fallback.

