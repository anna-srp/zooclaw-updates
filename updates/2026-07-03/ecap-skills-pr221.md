---
title: "Deep Research 深度研究提速：多路调研汇总不再卡死"
type: "Skill 上架/更新"
priority: "中"
date: "2026-07-03"
status: "待审核"
channels: ""
---

# Deep Research 深度研究提速：多路调研汇总不再卡死

## 核心宣传点

深度研究任务的多路调研结果汇总环节大幅提速，长研究不再在最后一步卡住十几分钟，报告质量和引用来源也更可靠。

## 原始内容

feat(deep-research): bounded synthesis via dossier files + compact digests (#221)

## Problem

A standard-mode `deep-research` run stalled at the end: 5 investigators
finished in ~7.5 min, but final synthesis took ~12 min with no visible
progress. Cause: each investigator returned 58k–107k tokens; all 5
collected into one main-agent context hit the **~400k window ceiling**,
so the report was one slow, quality-degraded LLM call. Cost scaled with
`Σ(investigator output)`, not investigator count.

## Fix (prompt-only — prose edits to `deep-research/SKILL.md`, +19/−8)

Collect by reference: files are the source of truth; the main thread
keeps only a small working set. Written as **principles, not a runbook**
— the skill states only what the model can't derive (platform facts,
thresholds) or won't do consistently unprompted; mechanics are left to
model judgment.

- **`### Collect by reference`** — each investigator writes full
findings (evidence, graded sources with URLs, gaps) to a dossier file
(~10–15K tokens, curated) in one fresh, uniquely-named **workspace**
folder per run (e.g. `research/<topic-slug>-<id>/`, never inside the
skill directory; paths assigned at dispatch), and returns only a compact
digest. Returns are capped at ~24K chars → digest targets ~10–15K chars
in English, ~1/3 in CJK, tighter at deep breadth. Too-broad dimension →
say so and split.
- **Bounded synthesis** — work from the digests, mapping
claims/agreement/contradictions/gaps/sources; open a full file only when
a specific claim needs the depth; carry recorded sources into inline
citations + bibliography.
- **Deep mode delegates** — section drafters inherit the same contract:
inline-cited draft to a file in the run folder, short brief back;
assemble by stitching the files with Pre-delivery spot-checks.
- **Mode selection** — default standard; breadth × stakes picks
quick/deep; propose depth at framework confirmation; headless/unattended
runs proceed at standard. Replaces the undefined `Cases` column.
- **Progress** — signal at dispatch, as findings land, and at writing.
- **Anti-pattern** — *Flooding your own context*.

## Verification

- **Live behavioral test** (devcontainer, OpenClaw 2026.6.6, quick
mode): 4 investigators wrote 15–29KB dossiers (one **28.8KB > the 24K
return wall** — proving files-as-truth) and returned digests by
reference; the orchestrator's context stayed at **7% after fan-in, 12%
after writing the report** (vs the ~400k stall). Report was well-formed
with graded bibliography. One platform caveat, independent of this PR:
the subagent-completion announce path failed to auto-resume the parent
(known OpenClaw issue) — synthesis was completed via a manual resume
turn.
- **Reviews**: multiple rounds of dual AI review (Claude + Codex) to 0
findings; an 8-angle / independently-verified review pass whose 4
confirmed findings (deep-mode drafter contract, CJK/deep digest scaling,
headless mode fallback, tracing-duty narrowing) were fixed; a final
Codex REQUEST_CHANGES round resolved by anchoring the run folder to the
workspace and making the headless fallback silent (scope gaps already
surface via Limitations' standing duty). **Current HEAD: both reviewers
APPROVE, auto-review gate green, no blocking labels.**
- Linter passes; frontmatter untouched; no new deps/scripts; no
`sessions.history`, no cache jargon.
- Deployed to staging as `v0.6.8-beta.2`/`beta.3` (pre-review-fix
snapshots; cut `beta.4` after merge or on request).

## Follow-up

- Deep-mode behavior (section delegation + stitch) is designed and
reviewed but not yet live-tested — blocked on the staging-parity
devcontainer fix for the announce path; rerun at deep depth once it
lands.
- Thresholds are research-derived + one measured run; record
digest/dossier sizes on real runs and tune.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01UKjmZWM7oy6JiEw3pptGz7

---------

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>

---

**PR Description:**

## Problem

A standard-mode `deep-research` run stalled at the end: 5 investigators finished in ~7.5 min, but final synthesis took ~12 min with no visible progress. Cause: each investigator returned 58k–107k tokens; all 5 collected into one main-agent context hit the **~400k window ceiling**, so the report was one slow, quality-degraded LLM call. Cost scaled with `Σ(investigator output)`, not investigator count.

## Fix (prompt-only — prose edits to `deep-research/SKILL.md`, +19/−8)

Collect by reference: files are the source of truth; the main thread keeps only a small working set. Written as **principles, not a runbook** — the skill states only what the model can't derive (platform facts, thresholds) or won't do consistently unprompted; mechanics are left to model judgment.

- **`### Collect by reference`** — each investigator writes full findings (evidence, graded sources with URLs, gaps) to a dossier file (~10–15K tokens, curated) in one fresh, uniquely-named **workspace** folder per run (e.g. `research/<topic-slug>-<id>/`, never inside the skill directory; paths assigned at dispatch), and returns only a compact digest. Returns are capped at ~24K chars → digest targets ~10–15K chars in English, ~1/3 in CJK, tighter at deep breadth. Too-broad dimension → say so and split.
- **Bounded synthesis** — work from the digests, mapping claims/agreement/contradictions/gaps/sources; open a full file only when a specific claim needs the depth; carry recorded sources into inline citations + bibliography.
- **Deep mode delegates** — section drafters inherit the same contract: inline-cited draft to a file in the run folder, short brief back; assemble by stitching the files with Pre-delivery spot-checks.
- **Mode selection** — default standard; breadth × stakes picks quick/deep; propose depth at framework confirmation; headless/unattended runs proceed at standard. Replaces the undefined `Cases` column.
- **Progress** — signal at dispatch, as findings land, and at writing.
- **Anti-pattern** — *Flooding your own context*.

## Verification

- **Live behavioral test** (devcontainer, OpenClaw 2026.6.6, quick mode): 4 investigators wrote 15–29KB dossiers (one **28.8KB > the 24K return wall** — proving files-as-truth) and returned digests by reference; the orchestrator's context stayed at **7% after fan-in, 12% after writing the report** (vs the ~400k stall). Report was well-formed with graded bibliography. One platform caveat, independent of this PR: the subagent-completion announce path failed to auto-resume the parent (known OpenClaw issue) — synthesis was completed via a manual resume turn.
- **Reviews**: multiple rounds of dual AI review (Claude + Codex) to 0 findings; an 8-angle / independently-verified review pass whose 4 confirmed findings (deep-mode drafter contract, CJK/deep digest scaling, headless mode fallback, tracing-duty narrowing) were fixed; a final Codex REQUEST_CHANGES round resolved by anchoring the run folder to the workspace and making the headless fallback silent (scope gaps already surface via Limitations' standing duty). **Current HEAD: both reviewers APPROVE, auto-review gate green, no blocking labels.**
- Linter passes; frontmatter untouched; no new deps/scripts; no `sessions.history`, no cache jargon.
- Deployed to staging as `v0.6.8-beta.2`/`beta.3` (pre-review-fix snapshots; cut `beta.4` after merge or on request).

## Follow-up

- Deep-mode behavior (section delegation + stitch) is designed and reviewed but not yet live-tested — blocked on the staging-parity devcontainer fix for the announce path; rerun at deep depth once it lands.
- Thresholds are research-derived + one measured run; record digest/dossier sizes on real runs and tune.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01UKjmZWM7oy6JiEw3pptGz7
