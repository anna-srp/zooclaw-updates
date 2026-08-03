---
title: "Council 多模型专家研讨功能上线（Beta）：一个问题，多位 AI 专家协同产出深度报告"
type: "新功能上线"
priority: "高"
外部: "A"
date: "2026-07-29"
status: "待审核"
channels: ""
---

## 核心宣传点

现在你可以在网页端发起「Council 专家研讨」：系统会围绕你的议题自动组建多位 AI 专家分头调研、交叉引用、彼此挑刺，最终合成一份带完整引用的深度报告，适合行业调研、竞品分析、复杂决策。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- commit：a85f7f5505665c876add7e2befaf49fc312981d3
- PR：#3132
- 日期：2026-07-29T16:54:14Z

### Commit message

```
feat(council): build the Council surface on the runs API (#3132)

Linear:
https://linear.app/srpone/issue/ECA-1211/council-多模型调研功能上线-beta-版

## Summary

Builds the Council surface in `web/app`: the prototype becomes a real
feature backed by the runs API, dispatch moves into a proper agent
session thread, and the page adopts the design system.

Frontend and docs only — **zero files under `services/`**. The backend
half landed separately in #3120 (dispatch thread persistence), #3113 /
#3115 / #3123 (pod file reads), and #3129 (folder discovery), so this
deploys after them with no ordering to coordinate.

24 commits, grouped by what they do:

**Wired to the real API**
- `feat(council): replace the mocked prototype with the real runs API` —
the page now creates, lists, refreshes and cancels real runs
- `fix(council): scope refresh failures per run and guard IME submits` —
a failed refresh no longer poisons unrelated runs; CJK/IME composition
no longer submits mid-word

**Dispatch correctness** — the substantive fix
- `fix(council): dispatch to the main agent thread, not whichever is
active`
- `fix(council): dispatch into a session thread, not the DM channel
root`
- `refactor(council): derive the session channel instead of storing it`
- `fix(council): never gate cancel on the agent thread`

**Design system**
- `refactor(council): align page with design system`
- `refactor(council): give run status one owner and a tone`
- `refactor(council): replace council.css with Tailwind utilities`
- `fix(council): restore ellipsis on truncated history titles`

**Docs** — the interactive prototype specs, plus
`docs/council-skill-contract.md` (new, see below)

## Root cause

Two defects worth calling out, both about *where* Council was talking.

**Council posted into the wrong channel, at the wrong level.** `/council
{topic}`, `go` and `cancel` went out as root-level posts in the main
agent's `dm_channel_id`. Every other agent conversation in the product
is a threaded reply in the agent's `session_channel_id` under a
session's `root_post_id` — two different channels on
`AgentMattermostPublic`, and the frontend type never declared the second
one, so it arrived and was dropped.

The consequences: the exchange had no session record, so it never
appeared in the session list and the results view promised a thread the
user could not open; `go` and `cancel` landed as bare words in the
user's ordinary main-agent chat with nothing scoping them to the run;
and because the thread lived only in client state, approval was
reachable only from the tab that started the run. Council now mirrors
`new-chat` — create a session, require its root post, reply into that
thread — and the run carries the root post, so `go` and `cancel` survive
a reload and work from another device.

**Cancel was gated on that same thread, which deadlocked the feature.**
Go genuinely needs the thread: the skill proceeds only after reading
consent there, so approving locally would be a lie. Cancel needs nothing
— the backend records it as a state transition and reads no dispatch
data at all. Sharing one guard meant a run with no
`dispatch_root_post_id` was unapprovable (correct), uncancellable
(wrong), *and* admission-blocking, since `create_run` rejects a second
run while one is active. Council became permanently unusable for that
account with no way out through the UI.

The backend had already anticipated this — `cancelling` is deliberately
excluded from `ADMISSION_BLOCKING_STATES` so a cancelled run cannot gate
its replacement. The backend built the escape hatch; the frontend
padlocked it. The rule now encoded: cancel must never depend on anything
but the run's own state.

## `docs/council-skill-contract.md`

New, and aimed outside this repo — at whoever maintains the Council
skill in `ecap-skills`.

Every Council outage so far has been a contract mismatch with the skill
rather than a bug in either side's own logic: we read the wrong
workspace path, called a list endpoint expecting file contents, required
the topic to come back verbatim, and typed `eta_minutes` as an integer
against a JSON number. All cheap to fix, all expensive to find, because
the contract existed only as our inference about the skill's output.

The doc writes it down — the two one-way channels, the `status.json`
field contract including the stricter `awaiting_go` gate, the stage
mapping, artifact path rules, read cadence — and asks for three things:
a way to pass our run id in (which would make folder binding exact
instead of inferred), confirmation that `status.json` writes are atomic
(we read without taking the lock file beside it), and confirmation that
`estimate.unpriced` and `premium_alt_*` are stable so we can surface
them.

## Test plan

- [x] `bash scripts/verify-web.sh` green — guards, tsc, eslint, and 7434
vitest tests across 553 files
- [x] Rebased onto current `origin/main`; the superseded backend commit
was dropped, since #3120 landed a newer collapsed form of the same
change
- [x] Council unit tests cover: a session is created before the run; the
topic posts under the session root rather than at channel root; `go` /
`cancel` reply into the run's stored thread rather than any active
channel; `go` is disabled without a dispatch; **cancel is enabled
without one** and warns that the skill may keep running on the pod
- [ ] Staging: one real run driven end to end — topic → gate → `go` →
`done` — including member reports. This has never been exercised against
a live pod, because the frontend has not shipped until now.
- [ ] Staging: confirm the history rail, gate and results render
correctly at 320 / 768 / 1440

## Notes for review

The wide test-fixture diff comes from `session_channel_id` becoming a
declared field on `OpenClawAgentMattermost`. The backend has always sent
it; the type simply never declared it, so it was silently dropped.
Making it required touches every fixture that builds an agent.

`MattermostProvider` is gone from Council. It was mounted only to reach
`sendMessage`, which posts to whatever channel is active — the source of
the dispatch defect. Council now builds a standalone
`MattermostAPIService` and posts to an explicit `(channel, root)` pair,
so the active-channel concept and its race leave Council entirely.
```

### PR body

Linear: https://linear.app/srpone/issue/ECA-1211/council-多模型调研功能上线-beta-版

## Summary

Builds the Council surface in `web/app`: the prototype becomes a real feature backed by the runs API, dispatch moves into a proper agent session thread, and the page adopts the design system.

Frontend and docs only — **zero files under `services/`**. The backend half landed separately in #3120 (dispatch thread persistence), #3113 / #3115 / #3123 (pod file reads), and #3129 (folder discovery), so this deploys after them with no ordering to coordinate.

24 commits, grouped by what they do:

**Wired to the real API**
- `feat(council): replace the mocked prototype with the real runs API` — the page now creates, lists, refreshes and cancels real runs
- `fix(council): scope refresh failures per run and guard IME submits` — a failed refresh no longer poisons unrelated runs; CJK/IME composition no longer submits mid-word

**Dispatch correctness** — the substantive fix
- `fix(council): dispatch to the main agent thread, not whichever is active`
- `fix(council): dispatch into a session thread, not the DM channel root`
- `refactor(council): derive the session channel instead of storing it`
- `fix(council): never gate cancel on the agent thread`

**Design system**
- `refactor(council): align page with design system`
- `refactor(council): give run status one owner and a tone`
- `refactor(council): replace council.css with Tailwind utilities`
- `fix(council): restore ellipsis on truncated history titles`

**Docs** — the interactive prototype specs, plus `docs/council-skill-contract.md` (new, see below)

## Root cause

Two defects worth calling out, both about *where* Council was talking.

**Council posted into the wrong channel, at the wrong level.** `/council {topic}`, `go` and `cancel` went out as root-level posts in the main agent's `dm_channel_id`. Every other agent conversation in the product is a threaded reply in the agent's `session_channel_id` under a session's `root_post_id` — two different channels on `AgentMattermostPublic`, and the frontend type never declared the second one, so it arrived and was dropped.

The consequences: the exchange had no session record, so it never appeared in the session list and the results view promised a thread the user could not open; `go` and `cancel` landed as bare words in the user's ordinary main-agent chat with nothing scoping them to the run; and because the thread lived only in client state, approval was reachable only from the tab that started the run. Council now mirrors `new-chat` — create a session, require its root post, reply into that thread — and the run carries the root post, so `go` and `cancel` survive a reload and work from another device.

**Cancel was gated on that same thread, which deadlocked the feature.** Go genuinely needs the thread: the skill proceeds only after reading consent there, so approving locally would be a lie. Cancel needs nothing — the backend records it as a state transition and reads no dispatch data at all. Sharing one guard meant a run with no `dispatch_root_post_id` was unapprovable (correct), uncancellable (wrong), *and* admission-blocking, since `create_run` rejects a second run while one is active. Council became permanently unusable for that account with no way out through the UI.

The backend had already anticipated this — `cancelling` is deliberately excluded from `ADMISSION_BLOCKING_STATES` so a cancelled run cannot gate its replacement. The backend built the escape hatch; the frontend padlocked it. The rule now encoded: cancel must never depend on anything but the run's own state.

## `docs/council-skill-contract.md`

New, and aimed outside this repo — at whoever maintains the Council skill in `ecap-skills`.

Every Council outage so far has been a contract mismatch with the skill rather than a bug in either side's own logic: we read the wrong workspace path, called a list endpoint expecting file contents, required the topic to come back verbatim, and typed `eta_minutes` as an integer against a JSON number. All cheap to fix, all expensive to find, because the contract existed only as our inference about the skill's output.

The doc writes it down — the two one-way channels, the `status.json` field contract including the stricter `awaiting_go` gate, the stage mapping, artifact path rules, read cadence — and asks for three things: a way to pass our run id in (which would make folder binding exact instead of inferred), confirmation that `status.json` writes are atomic (we read without taking the lock file beside it), and confirmation that `estimate.unpriced` and `premium_alt_*` are stable so we can surface them.

## Test plan

- [x] `bash scripts/verify-web.sh` green — guards, tsc, eslint, and 7434 vitest tests across 553 files
- [x] Rebased onto current `origin/main`; the superseded backend commit was dropped, since #3120 landed a newer collapsed form of the same change
- [x] Council unit tests cover: a session is created before the run; the topic posts under the session root rather than at channel root; `go` / `cancel` reply into the run's stored thread rather than any active channel; `go` is disabled without a dispatch; **cancel is enabled without one** and warns that the skill may keep running on the pod
- [ ] Staging: one real run driven end to end — topic → gate → `go` → `done` — including member reports. This has never been exercised against a live pod, because the frontend has not shipped until now.
- [ ] Staging: confirm the history rail, gate and results render correctly at 320 / 768 / 1440

## Notes for review

The wide test-fixture diff comes from `session_channel_id` becoming a declared field on `OpenClawAgentMattermost`. The backend has always sent it; the type simply never declared it, so it was silently dropped. Making it required touches every fixture that builds an agent.

`MattermostProvider` is gone from Council. It was mounted only to reach `sendMessage`, which posts to whatever channel is active — the source of the dispatch defect. Council now builds a standalone `MattermostAPIService` and posts to an explicit `(channel, root)` pair, so the active-channel concept and its race leave Council entirely.

