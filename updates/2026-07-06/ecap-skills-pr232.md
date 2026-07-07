---
title: "Deep Research 深度研究可靠性升级"
type: "Skill 上架/更新"
priority: "中"
date: "2026-07-06"
status: "待审核"
channels: ""
---

# Deep Research 深度研究可靠性升级

## 核心宣传点

深度研究经过真实环境实测调优：多路调研的结果汇报不再被截断丢失，研究报告内容更完整、引用来源更可靠。

## 原始内容

[7514b6f2] fix(deep-research): correct digest-cap contract + harden subagent-delivery rules (live-tested, dual-reviewed) (#232)

Single file: `deep-research/SKILL.md`. Seven commits in three phases;
net size vs main is **+182 chars** (11,116 → 11,298) — this PR trades
~1.6K chars of redundant prose for ~1.8K chars of empirically-derived
behavioral contract. It is a correctness/quality PR, not a token-savings
PR (that was the original intent; the live test changed the story).

## Phase 1 — fix the digest-cap misreading (commits 1–2)

The skill claimed subagent returns are "capped at ~24K chars" and told
investigators to target 10–15K. Actual openclaw caps
(`agent-steering-queue.ts:13-15`, since v2026.6.1):

| Constant | Value | Semantics |
|---|--:|---|
| `MAX_RESULT_CHARS_PER_ITEM` | **6,000** | per-return **hard slice** on
the queued path, no truncation marker |
| `MAX_MERGED_STEERING_CHARS` | 24,000 | merged-batch bound — **defers**
overflow to later turns, never clips |

→ digest target re-set to **~5K chars** EN (~1/3 CJK), front-load
findings/confidence/sources; write dossiers incrementally; redundant
prose trimmed.

## Phase 2 — live devcontainer test (commits 3–4)

Full run on openclaw-docker **2026.6.6** (Sonnet 4.6 via LiteLLM, quick
depth, 5 investigators, real web research):

- ✅ 5/5 complete dossiers written unprompted (17–24KB, incremental
mtimes); front-loading followed; after total digest loss one recovery
turn read all dossiers and delivered a complete 15.4K-char report with
all required sections.
- ⚠️ Digest compliance is soft: 5.6K–8.3K actual vs ~5K target (3/5
overshoot) — front-loading is the real guard.
- ⚠️ The 6K slice is **path-dependent**: direct announce deliveries
arrive uncut (verified 7,978-char digest intact); queued/steering path
slices. Wording corrected.
- 🔴 **Runtime bug found (≤2026.6.6)**: announce delivery counts a parent
`NO_REPLY` as failure → 3 retries → **result permanently discarded**; no
settle-wake exists → run stalls. 4/5 digests lost in the test; the
parent even NO_REPLYed a direct user question afterwards. Upstream fix
(openclaw#97090) first ships in v2026.7.1-beta.1. Skill-side mitigations
added: visible-ack rule + dossier-first completeness gate.

## Phase 3 — review fixes (commits 5–7)

Codex REQUEST_CHANGES round: partial-dossier quality gate (a timed-out
investigator's half-written dossier no longer counts as done);
defer-vs-clip wording separated (verified in source that the 24K bound
defers, never clips).

Dual-agent review pass (independent Claude + Codex, same rubric):
- **Q2 both: BALANCED** — trim is not lossy; do not trim further. One
restore adopted: the anti-hedging clause ("a balanced-sounding summary
that takes no position isn't useful"), the doc's only counterweight to
its objectivity rules.
- **Q1 merged fixes**: dispatch prompts must restate the digest contract
(investigators never read SKILL.md); ack rule widened to all subagent
results incl. section drafters and explicitly overrides envelope
NO_REPLY affordances; defined post-cap exit (state missing dimensions
plainly, not as Limitations); synthesis-time recovery defers to the
thin-dossier rule; recovery reads are the explicit exception to
read-sparingly; provenance comment version-pins both the caps and the
NO_REPLY bug.
- **Rejected with rationale**: "make 6K a hard limit" — unenforceable
numbers are theater; the dispatch-relay rule + split-the-dimension
escape hatch address the risk at the source.

## Notes

- Dossier sizing (~10–15K tokens) unchanged; files are unaffected by any
cap.
- `ecap-skills-council/deep-research/SKILL.md` is an identical copy —
needs the same changes as a follow-up after merge.
- Platform follow-up (separate from this PR): bump the openclaw-docker
baseline when 2026.7.x GA lands — until then, **any** orchestrator skill
can hit the NO_REPLY discard/stall; the ack rule here only mitigates.
- Full investigation record:
`design-doc/zooclaw-extras/2026-07-06-context-offload-decision.md`
(addenda A/A2).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01TvmJccjKM3DJaQtMQ7vUqz

---------

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Fable 5 <noreply@anthropic.com>

--- PR #232 body ---
Single file: `deep-research/SKILL.md`. Seven commits in three phases; net size vs main is **+182 chars** (11,116 → 11,298) — this PR trades ~1.6K chars of redundant prose for ~1.8K chars of empirically-derived behavioral contract. It is a correctness/quality PR, not a token-savings PR (that was the original intent; the live test changed the story).

## Phase 1 — fix the digest-cap misreading (commits 1–2)

The skill claimed subagent returns are "capped at ~24K chars" and told investigators to target 10–15K. Actual openclaw caps (`agent-steering-queue.ts:13-15`, since v2026.6.1):

| Constant | Value | Semantics |
|---|--:|---|
| `MAX_RESULT_CHARS_PER_ITEM` | **6,000** | per-return **hard slice** on the queued path, no truncation marker |
| `MAX_MERGED_STEERING_CHARS` | 24,000 | merged-batch bound — **defers** overflow to later turns, never clips |

→ digest target re-set to **~5K chars** EN (~1/3 CJK), front-load findings/confidence/sources; write dossiers incrementally; redundant prose trimmed.

## Phase 2 — live devcontainer test (commits 3–4)

Full run on openclaw-docker **2026.6.6** (Sonnet 4.6 via LiteLLM, quick depth, 5 investigators, real web research):

- ✅ 5/5 complete dossiers written unprompted (17–24KB, incremental mtimes); front-loading followed; after total digest loss one recovery turn read all dossiers and delivered a complete 15.4K-char report with all required sections.
- ⚠️ Digest compliance is soft: 5.6K–8.3K actual vs ~5K target (3/5 overshoot) — front-loading is the real guard.
- ⚠️ The 6K slice is **path-dependent**: direct announce deliveries arrive uncut (verified 7,978-char digest intact); queued/steering path slices. Wording corrected.
- 🔴 **Runtime bug found (≤2026.6.6)**: announce delivery counts a parent `NO_REPLY` as failure → 3 retries → **result permanently discarded**; no settle-wake exists → run stalls. 4/5 digests lost in the test; the parent even NO_REPLYed a direct user question afterwards. Upstream fix (openclaw#97090) first ships in v2026.7.1-beta.1. Skill-side mitigations added: visible-ack rule + dossier-first completeness gate.

## Phase 3 — review fixes (commits 5–7)

Codex REQUEST_CHANGES round: partial-dossier quality gate (a timed-out investigator's half-written dossier no longer counts as done); defer-vs-clip wording separated (verified in source that the 24K bound defers, never clips).

Dual-agent review pass (independent Claude + Codex, same rubric):
- **Q2 both: BALANCED** — trim is not lossy; do not trim further. One restore adopted: the anti-hedging clause ("a balanced-sounding summary that takes no position isn't useful"), the doc's only counterweight to its objectivity rules.
- **Q1 merged fixes**: dispatch prompts must restate the digest contract (investigators never read SKILL.md); ack rule widened to all subagent results incl. section drafters and explicitly overrides envelope NO_REPLY affordances; defined post-cap exit (state missing dimensions plainly, not as Limitations); synthesis-time recovery defers to the thin-dossier rule; recovery reads are the explicit exception to read-sparingly; provenance comment version-pins both the caps and the NO_REPLY bug.
- **Rejected with rationale**: "make 6K a hard limit" — unenforceable numbers are theater; the dispatch-relay rule + split-the-dimension escape hatch address the risk at the source.

## Notes

- Dossier sizing (~10–15K tokens) unchanged; files are unaffected by any cap.
- `ecap-skills-council/deep-research/SKILL.md` is an identical copy — needs the same changes as a follow-up after merge.
- Platform follow-up (separate from this PR): bump the openclaw-docker baseline when 2026.7.x GA lands — until then, **any** orchestrator skill can hit the NO_REPLY discard/stall; the ack rule here only mitigates.
- Full investigation record: `design-doc/zooclaw-extras/2026-07-06-context-offload-decision.md` (addenda A/A2).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01TvmJccjKM3DJaQtMQ7vUqz
