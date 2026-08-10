# SerendipityOneInc/ecap-skills — 2026-08-09

## ac638466a2a5a5844d45f15dcc25b9e0aa963dc1

- 作者: felix-srp
- 日期: 2026-08-09T02:54:12Z

### Commit Message

```
feat(council): composer answer-skeleton, section pyramid, tightness+scope (RACE wording port) (#260)

## Why

PR #259 (deep-research) established via DeepResearch Bench criterion
mining that the RACE deficit is presentation-side — scope discipline,
answer-shaped organization, tightness — and probe-validated three
write-time wording fixes (scope → task 54 readability +2.6 with criteria
flipping to wins; answer-skeleton → task 52 +2.5, directness flipped).
This PR ports the same wording family to the council composer, whose
failure mode is identical: section-by-section append composition with no
whole-report pass (reviser retired at standard depth in #255), so
diffuseness has nothing bounding it at write time.

## What changed (`council/references/synthesis-prompts.md`, composer
template only)

1. **Answer skeleton** (item 2): after the cross-report claim map,
distill it into an answer skeleton — a few sentences per asked question
+ key findings/tensions/blind spots; the report expands only those
sentences; non-expanding material stays in the source reports.
2. **Section-level pyramid** (item 6): open every section with its key
finding, then evidence (explicitly presentation order, not advocacy).
3. **Tightness + scope** (new item 7): say each thing once, length is
not rigor; everything serves the topic's questions —
interesting-but-unasked findings get one line or nothing.
4. **Unanswered-question routing** (item 7): an asked-but-unanswered
question goes to "Blind spots and open questions", never silently
dropped.

Old item 7 (write mechanics) renumbered to 8 with a terminal gate check
(every asked question answered, sections open with findings, blind-spots
+ Sources present — fix only what fails; a gate inside the same
completion, not a revision pass). Reviser untouched — consistent with
#255/§9.12 (post-draft reflection unproven; these are write-time rules,
which is also where #259's probes localized the effect).

Also in this PR:
- **member-prompt.md** (light ports, unvalidated by the A/B, flagged for
review): `[HIGH]/[MEDIUM]/[LOW]` confidence tag on key claims
(cross-model calibration signal for the blinded composer) +
search-the-topic's-languages clause.
- **trim-md pass** on the four runtime .md files: −36 tok; dual-reviewed
(claude + codex), zero constraints lost (one initially-cut hard rule
restored after review caught its wider scope).
- **fallback parity** (review round 1): composer rules 2/6/7 ported into
`final_synthesis.py`'s `_SYNTHESIS_TEMPLATE` per the README/pytest
pairing contract; drift guard widened to rules 1–7 (round 2); stale
rule-number refs fixed (round 3). 275 council tests pass.
- **Stage-0 language pin** (probe evidence): the DRB task-52 council
probe (`zoo_drb_council52_main_20260807`) rewrote an English commission
into Chinese — the chair followed the bot persona language because
member-prompt's slot said "user's language" and the rewrite rule said
only "same language". Both now pin to the topic's own language (the
language the commission text is written in). Evidence:
`design-doc/ecap-skills/council/2026-08-07-council-drb-task52-baseline.md`
— where council@main scored RACE 53.65 on task 52 (beats deep-research's
best arm, 52.72) despite that language flip.

## Review rounds

- Round 1: codex P1 + claude (independently confirmed) —
composer/fallback template drift breaking the md<->py pairing test;
fixed in `5b3e629`.
- Round 2: codex clean; claude non-blocking — widen drift guard to rules
1-7; adopted in `9bfbf15`.
- Round 3: codex clean; claude minor — stale "Hard Rule 4" cross-refs
after the trim renumber; fixed in `a7c525a`.
- Round 4: both bots zero findings.
- Round 5 (Stage-0 language pin `072552a`): claude clean; codex P1 —
"commission text" ambiguous for mixed-language invocations (EN sentence
wrapping a JA topic) — fixed in `6bb7cec` (language = the topic span
itself, post knob-stripping).
- Round 6: both bots zero findings; CI green throughout. Zero false
positives dismissed.

## Verification — fixed-evidence composer A/B

Evidence frozen to staging run `temu-shein-tiktok-2026h1-001` (4
members, standard depth, multi-entity comparison); composer =
claude-opus-5 (the run's real synthesizer); 2 generations per arm;
GPT-5.5 solo rubric judge ×3 passes (pairwise preference votes discarded
— measured 8/8 position-biased).

- One-shot proxy: null on both arms (single-completion mechanics itself
eliminates diffuseness — the failure mode never appears).
- Section-by-section simulation (faithful to the real append mechanics):
**B (this PR) leads on all 5 dimensions** — directness +0.13, scope
+0.21, concision **+0.47**, navigability +0.16, overall +0.21 — at
**−22% length** (49.8K → 38.7K chars), matching #259's 19–25%
tightening. A-arm worst case (54K chars, concision 5.77) is the
unbounded-bloat tail; the B arm never produced it.
- Caveats: n=2 gens/arm, deltas ≈ within-arm spread; the signal is
direction-consistency (5/5 dims, no instrument showing A ahead where the
failure mode exists) plus the same wording family's DRB validation in
#259.

**On-bot verification (v0.6.15-beta.1 staging tag = this PR, 5-task DRB
slice, GPT-5.5 official judge):**
- RACE aggregate 54.16 vs main-baseline 53.95 — non-regression; flat
within judge noise (excluding one task that ran on the gateway's stale
skill cache, dead flat). At council's baseline (readability criterion
already 8.4 vs 8.6 near reference parity) the composer wording acts as a
guardrail against the A/B-measured bloat tail, not a score lever — the
A/B predicted exactly this (null on healthy mechanics, wins under
stressed mechanics).
- **Stage-0 language pin behaviorally validated**: all four
post-cache-refresh EN tasks delivered EN; the pre-fix baseline flipped
2/5 EN tasks to Chinese.
- Both council arms clear deep-research on the same slice by >1.3 points
(52.64 July / 52.08 PR#259). Full data:
`design-doc/ecap-skills/council/2026-08-07-council-drb-task52-baseline.md`.

Full method, tables, and reusable harness notes:
`design-doc/ecap-skills/council/2026-08-07-composer-ab-race-wording.md`.
Linter clean (12 pre-existing warnings).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01A9rjGtByhu2o7aDZTXRKPE

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## Why

PR #259 (deep-research) established via DeepResearch Bench criterion mining that the RACE deficit is presentation-side — scope discipline, answer-shaped organization, tightness — and probe-validated three write-time wording fixes (scope → task 54 readability +2.6 with criteria flipping to wins; answer-skeleton → task 52 +2.5, directness flipped). This PR ports the same wording family to the council composer, whose failure mode is identical: section-by-section append composition with no whole-report pass (reviser retired at standard depth in #255), so diffuseness has nothing bounding it at write time.

## What changed (`council/references/synthesis-prompts.md`, composer template only)

1. **Answer skeleton** (item 2): after the cross-report claim map, distill it into an answer skeleton — a few sentences per asked question + key findings/tensions/blind spots; the report expands only those sentences; non-expanding material stays in the source reports.
2. **Section-level pyramid** (item 6): open every section with its key finding, then evidence (explicitly presentation order, not advocacy).
3. **Tightness + scope** (new item 7): say each thing once, length is not rigor; everything serves the topic's questions — interesting-but-unasked findings get one line or nothing.
4. **Unanswered-question routing** (item 7): an asked-but-unanswered question goes to "Blind spots and open questions", never silently dropped.

Old item 7 (write mechanics) renumbered to 8 with a terminal gate check (every asked question answered, sections open with findings, blind-spots + Sources present — fix only what fails; a gate inside the same completion, not a revision pass). Reviser untouched — consistent with #255/§9.12 (post-draft reflection unproven; these are write-time rules, which is also where #259's probes localized the effect).

Also in this PR:
- **member-prompt.md** (light ports, unvalidated by the A/B, flagged for review): `[HIGH]/[MEDIUM]/[LOW]` confidence tag on key claims (cross-model calibration signal for the blinded composer) + search-the-topic's-languages clause.
- **trim-md pass** on the four runtime .md files: −36 tok; dual-reviewed (claude + codex), zero constraints lost (one initially-cut hard rule restored after review caught its wider scope).
- **fallback parity** (review round 1): composer rules 2/6/7 ported into `final_synthesis.py`'s `_SYNTHESIS_TEMPLATE` per the README/pytest pairing contract; drift guard widened to rules 1–7 (round 2); stale rule-number refs fixed (round 3). 275 council tests pass.
- **Stage-0 language pin** (probe evidence): the DRB task-52 council probe (`zoo_drb_council52_main_20260807`) rewrote an English commission into Chinese — the chair followed the bot persona language because member-prompt's slot said "user's language" and the rewrite rule said only "same language". Both now pin to the topic's own language (the language the commission text is written in). Evidence: `design-doc/ecap-skills/council/2026-08-07-council-drb-task52-baseline.md` — where council@main scored RACE 53.65 on task 52 (beats deep-research's best arm, 52.72) despite that language flip.

## Review rounds

- Round 1: codex P1 + claude (independently confirmed) — composer/fallback template drift breaking the md<->py pairing test; fixed in `5b3e629`.
- Round 2: codex clean; claude non-blocking — widen drift guard to rules 1-7; adopted in `9bfbf15`.
- Round 3: codex clean; claude minor — stale "Hard Rule 4" cross-refs after the trim renumber; fixed in `a7c525a`.
- Round 4: both bots zero findings.
- Round 5 (Stage-0 language pin `072552a`): claude clean; codex P1 — "commission text" ambiguous for mixed-language invocations (EN sentence wrapping a JA topic) — fixed in `6bb7cec` (language = the topic span itself, post knob-stripping).
- Round 6: both bots zero findings; CI green throughout. Zero false positives dismissed.

## Verification — fixed-evidence composer A/B

Evidence frozen to staging run `temu-shein-tiktok-2026h1-001` (4 members, standard depth, multi-entity comparison); composer = claude-opus-5 (the run's real synthesizer); 2 generations per arm; GPT-5.5 solo rubric judge ×3 passes (pairwise preference votes discarded — measured 8/8 position-biased).

- One-shot proxy: null on both arms (single-completion mechanics itself eliminates diffuseness — the failure mode never appears).
- Section-by-section simulation (faithful to the real append mechanics): **B (this PR) leads on all 5 dimensions** — directness +0.13, scope +0.21, concision **+0.47**, navigability +0.16, overall +0.21 — at **−22% length** (49.8K → 38.7K chars), matching #259's 19–25% tightening. A-arm worst case (54K chars, concision 5.77) is the unbounded-bloat tail; the B arm never produced it.
- Caveats: n=2 gens/arm, deltas ≈ within-arm spread; the signal is direction-consistency (5/5 dims, no instrument showing A ahead where the failure mode exists) plus the same wording family's DRB validation in #259.

**On-bot verification (v0.6.15-beta.1 staging tag = this PR, 5-task DRB slice, GPT-5.5 official judge):**
- RACE aggregate 54.16 vs main-baseline 53.95 — non-regression; flat within judge noise (excluding one task that ran on the gateway's stale skill cache, dead flat). At council's baseline (readability criterion already 8.4 vs 8.6 near reference parity) the composer wording acts as a guardrail against the A/B-measured bloat tail, not a score lever — the A/B predicted exactly this (null on healthy mechanics, wins under stressed mechanics).
- **Stage-0 language pin behaviorally validated**: all four post-cache-refresh EN tasks delivered EN; the pre-fix baseline flipped 2/5 EN tasks to Chinese.
- Both council arms clear deep-research on the same slice by >1.3 points (52.64 July / 52.08 PR#259). Full data: `design-doc/ecap-skills/council/2026-08-07-council-drb-task52-baseline.md`.

Full method, tables, and reusable harness notes: `design-doc/ecap-skills/council/2026-08-07-composer-ab-race-wording.md`. Linter clean (12 pre-existing warnings).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01A9rjGtByhu2o7aDZTXRKPE


### 变更文件

- council/README.md
- council/SKILL.md
- council/references/member-prompt.md
- council/references/synthesis-prompts.md
- council/scripts/final_synthesis.py
- council/tests/test_final_synthesis.py

