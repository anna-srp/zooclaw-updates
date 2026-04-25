# ecap-skills - 2026-04-25

共 2 条 commits

---

## chore(deep-research): trim SKILL.md ~32% with eval-driven preservation (#162)

- **SHA**: `d3f957429f3d50d48c1110fcdb1b029af2bb190b`
- **作者**: felix-srp
- **日期**: 2026-04-24T16:24:02Z
- **PR**: #162

### Commit Message

```
chore(deep-research): trim SKILL.md ~32% with eval-driven preservation (#162)

* chore(deep-research): simplify SKILL.md for tighter runtime context

Rewrite the deep-research skill prompt to cut redundancy and verbose
prose while preserving every operational rule. Goes from 196 → 116 lines
(~40% fewer tokens), which matters because this skill loads into
zooclaw's context on every invocation.

Key consolidations:
- Merge "Follow the trail" + "Go where the information is" into one
  section on source escalation.
- Merge the two depth-mode tables (investigators/time + analysis/cases)
  into a single table.
- Inline the A/B/C/D/E source-grade table as a single line.
- Collapse the 7-row self-challenge rubric to a one-line scorecard.
- Fold Additional Rules → Fault tolerance back into the Completeness
  gate (it was a duplicate).
- Drop moralizing prose, rhetorical flourishes, and meta-commentary
  (e.g. parallel triplets, "judgment call is always" pep talks).

Preserved verbatim: frontmatter + metadata, 5 done criteria, 5 question
patterns, source grades A–E, confidence tiers HIGH/MED/LOW/SPEC,
auto-cap rule, completeness gate with execution-failure recovery,
depth-mode parameters (3–5/5–8/10–15, max 5 parallel, 2-extra-round
cap), required/optional report sections, inline citation format,
language-consistency and local-files-as-A-grade rules.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(deep-research): restore concrete operational anchors

An independent evaluator compared the simplified SKILL.md against the
original and found the compression had gone too far on concrete
examples and imperative verbs — the anchors an LLM agent needs to turn
abstract principles into actions. Nine specific directives were
weakened or dropped. Restore them.

Fixes:
1. Challenge pattern — restore the three named-critic archetypes
   (analyst who called it overhyped, researcher who found the flaw,
   user who tried and failed).
2. Go-where-info-is — restore the "Did I get the content I need?"
   judgment rule and the concrete escalation hints (paywalled →
   browser-with-user-session / preprint / author pages; anti-scrape →
   browser; date filtering → news endpoints; many targets → parallel
   subagents).
3. Completeness gate — restore the "don't paper over contradictions"
   directive; contradictions are often the most interesting part.
4. Done Criteria #4 — restore the "clearly X is best, rewrite as a
   comparison" self-monitor.
5. Done Criteria #2 — restore the "actively search for what's new"
   imperative and "stale on arrival" framing.
6. Writing principles — restore "Popular ≠ good / Funded ≠ profitable /
   Cited ≠ correct / state what you excluded and why."
7. Over-specifying-subagents anti-pattern — restore the concrete
   good-vs-bad contrast ("Investigate current state of X" beats "Search
   X on Google, visit top 3").
8. Retrying-failing-search anti-pattern — restore the three-keyword
   threshold.
9. Rules — restore the fault-tolerance cross-reference pointing
   investigator failures to the Completeness gate recovery ladder.

Stats: 195 → 119 lines (~39% fewer lines, ~44% fewer words than the
pre-simplify original). Quality-first, tokens-second — recovers all
the operational anchors the evaluator flagged while still saving
~900 words of runtime context.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(deep-research): address PR review findings from Claude + Codex

Two independent reviewers (pr-review-toolkit and codex-rescue) flagged
7 HIGH, 2 Major, and 1 MEDIUM regression from the simplify pass. All
are restored here.

HIGH / Major fixes:
- Done Criteria: restore "Define 'done' before you start" framing line
  that made the criteria applicable mid-research, not only at delivery
  (was lines 39+47 of original).
- Done Criteria #3: restore "Grade every important claim" directive
  (was narrowed from claims → sources).
- One-question-per-investigator: restore recency investigator's
  concrete channel list ("date-filtered searches, news, social
  platforms, and industry forums").
- Go-where-info-is: re-bold "Every investigator must be able to
  discover new sources" so the imperative matches its peers.
- Depth Modes: mark standard as default in the merged table — the
  default signal was load-bearing and got dropped with the old
  Use-Case column.
- Writing principles: restore "Investigate all sides with equal rigor"
  to the landscape-vs-verdict bullet.
- Writing principles: restore the question marks and "actually" in
  "Question everything" (who said it? / what does the number actually
  measure?) — the original cued the LLM to *ask* the questions.
- Writing principles: restore "every key claim needs a source where
  it appears" — had narrowed from claims → numbers.
- Pre-delivery Check: restore skeptic-response and falsify-thesis
  prompts; add "gradings honest / uncertainties acknowledged / named
  critics, risks, failures" qualifiers that tie back to earlier
  principles.

MEDIUM fix (logical bug):
- Pre-delivery Check: the post-restore wording said "Share the score
  alongside the report, never inside it" as an imperative — which
  contradicts the Process-leakage anti-pattern that requires keeping
  self-challenge scores OUT of the deliverable. Restore the original's
  optional phrasing: "If you share the score with the user, do so
  *alongside* the report, never inside it."

Minor fix:
- Process-leakage anti-pattern: restore the concrete forbidden-phrase
  example ("e.g. 'these are genuine gaps, not execution failures'")
  and the "Limitations lists what's unknown — it does not justify the
  classification" clarifier.

Stats: 195 → 121 lines (~38% fewer lines, ~39% fewer words vs the
pre-simplify original).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(deep-research): restore broad tool-inventory sentence

Codex flagged that the "Go where the information is" section's
escalation ladder (search → fetch → browser → ask user) lost the
original's explicit broad tool inventory: "Use whatever tools are
available — web search, browser, code execution, file access."
Code-execution and file-access were dropped as explicit research
tools.

Restore the one-sentence tool inventory ahead of the escalation
ladder. This matters because the deep-research skill description
itself advertises "exec" (code execution) and "sessions_spawn" as
research capabilities — the skill body should match.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(deep-research): strengthen verdict-refusal under bait framing

Adversarial A/B testing (plant-based vs Mediterranean diet, "give me
the answer") showed a small but real directive-compliance gap: under
explicit verdict-bait framing, the simplified-version agent produced a
synthesized soft recommendation instead of refusing the verdict the
way the original-version agent did ("There is no defensible verdict").

The "clearly X is best → rewrite as comparison" self-monitor in Done
Criteria #4 is present but apparently not prominent enough to fire
reliably on bait questions. Add a standalone directive to the
Writing-principles "landscape-not-verdict" bullet that makes the
refusal behavior explicit.

Stats: 121 → 121 lines (1 line stays, +16 words). Recovers the
adversarial probe gap without touching any other directive.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(deep-research): structural emphasis for anti-advocacy + self-review

Follow-up to the adversarial A/B findings. The root cause analysis
showed the simplify pass stripped behavioral weight that the original
prompt was carrying via redundancy, standalone imperatives, and a
visible scoring table. The one-line verdict-refusal patch addressed
the symptom but not the class. These two changes address the class
structurally:

1. **Done Criteria #4** — move "If you catch yourself writing 'clearly
   X is best,' rewrite as a comparison" to the end as a bolded
   standalone sentence. Restore the "reader can disagree with your
   advice" framing that anchors why recommendations are separated from
   analysis. Restores the two anti-advocacy emphasis mechanisms the
   simplify pass had flattened.

2. **Pre-delivery Check** — restore the 7-row scorecard as a visible
   table (Dimension · Check · /10) instead of a single inline prose
   sentence. A table format triggers a literal self-review pass in
   ways an inline checklist does not; this is the format the original
   used, and the one the agent actually executes against.

Stats: 121 → 133 lines (+12), 1289 → 1362 words (+73). Still ~32%
smaller than main's pre-simplify version (195/2066). Net trade: ~6%
token giveback in exchange for recovering behavioral emphasis on the
two places the adversarial eval flagged as weak (verdict-refusal,
self-review activation).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary
Rewrite `deep-research/SKILL.md` to cut redundancy while preserving every operational rule, validated via reviewer agents + 8 blind A/B research runs (including one **inside the zooclaw runtime** isolating SKILL content from all other variables).

**Final size:** 195 → 133 lines (~32% fewer lines, ~34% fewer words).

## What changed in the prompt

**Consolidated:** "Follow the trail" + "Go where the information is" merged · two depth-mode tables merged · A/B/C/D/E source grades inlined · persona examples condensed.

**Preserved verbatim:** frontmatter + metadata · 5 done criteria · 5 question patterns · source grades A–E · confidence tiers HIGH/MED/LOW/SPEC · auto-cap rule · completeness gate with execution-failure recovery · depth-mode parameters (3–5 / 5–8 / 10–15, max 5 parallel per batch, 2-extra-round cap) · required/optional report sections · inline citation format · language-consistency · local-files-as-A-grade · fault-tolerance.

**Restored after eval feedback** (would have regressed without these): challenge-pattern archetypes · "Did I get the content I need?" judgment rule + tool-escalation hints · "don't paper over contradictions" · "actively search for what's new" imperative · Popular≠good heuristics · three-keyword retry threshold · broad tool inventory (web search, browser, code execution, file access) · standalone "rewrite as comparison" self-monitor · visible 7-row pre-delivery scorecard table.

## Validation

**Reviewer agents (Claude pr-review-toolkit + Codex):** flagged 9 HIGH/Major directive losses + 1 MEDIUM logical contradiction. All 10 fixed.

**A/B research runs** — same prompt, original vs this branch's SKILL, LLM judge scored blind:

| Round | Scope | Topics | Simplified wins | Original wins |
|---|---|---|---|---|
| Standard (out-of-container) | On-device LLM inference; K8s for startups | 2 | 2 | 0 |
| Adversarial round 1 (out-of-container) | Plant-vs-Med diet (verdict-bait); RSC named critics | 2 | 1 + 1 split | 0 + 1 probe |
| Adversarial round 2 (out-of-container, post-fix) | Bronze Age (recency-skip); China semis (multi-lang); eggs/heart (verdict-bait) | 3 | 3 | 0 |
| **In-container A/B (openclaw + LiteLLM + sonnet, only SKILL varied)** | TTS benchmark comparison | 1 | **1 (75 vs 62 standard, 16 vs 11 probes)** | 0 |
| **Total** | | **8** | **7 wins** | **1 partial** |

In the controlled in-container run, the original SKILL agent fabricated benchmark numbers (~2.1%/~2.4%) while the simplified agent surfaced real decimals (1.23/0.97) and flagged missing data with explicit confidence markers — the auto-cap behavior the skill's directives encode. Simplified also ran 10 tool-use rounds vs original's 5, consistent with the restored "every investigator must discover new sources" and stricter completeness-gate language.

## Caveats
- n=8 topics is a small sample; strong direction but not statistical proof.
- In-container test used `claude-sonnet-4-6` via LiteLLM. Actual zooclaw production may use opus — worth one post-merge spot-check.
- Judges were LLM reviewers, not humans.

## Test plan
- [x] Render check / markdown correctness — frontmatter parses, 2 tables column-consistent, 15 headings no level-jumps, 0 trailing whitespace; CI Skill Lint + CodeQL green
- [x] Persona / framework / parallel investigators / source grading / completeness gate / report structure — validated across 8 A/B runs
- [x] Verdict-bait spot-check — plant-vs-Med (refused on inconclusive evidence) and eggs/heart (gave calibrated yes/no + nested auto-caps); probes ≥ original
- [x] In-container behavioral test (same model, same env, only SKILL varied) — simplified outperformed on 13 of 15 dimensions
- [ ] **(Post-merge)** One live `深度调研 <real topic>` invocation in production zooclaw with opus to confirm no surprise from the sonnet→opus delta

If the post-merge live check reveals a regression, revert is single-file and one commit.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## chore(pptx): simplify runtime skill docs (~30% token reduction, behaviorally A/B-verified) (#167)

- **SHA**: `5c9a57269ccb4fc0f3b6239da3f79db33c46b7b8`
- **作者**: felix-srp
- **日期**: 2026-04-24T14:38:16Z
- **PR**: #167

### Commit Message

```
chore(pptx): simplify runtime skill docs (~30% token reduction, behaviorally A/B-verified) (#167)

* chore(pptx): simplify skill markdown for tighter runtime context

Reduce pptx/ reference tokens by ~30% for better context engineering in
zooclaw. Deduplicate content across SKILL.md and reference files,
consolidate slide-type tables, condense color/style-recipe tables, and
drop the pitfalls.md hub (SKILL.md links directly).

No functional changes — smoke test passes (11 PASS, 1 pre-existing
regex-in-codeblock link-checker false positive, 7 SKIP for missing tools).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(pptx): apply follow-up cuts from simplification eval

Implements the 3 additional cut opportunities flagged by the evaluation
agent in PR #167:

1. SKILL.md: merged "DO NOT bypass shape-cli" whitelist and "Common
   rationalizations" into one anti-pattern list. Same guardrails, less
   repetition.
2. SKILL.md: moved the inline 6-op "Worked example" out of the
   always-loaded file into shape-batch.md (lazy-loaded). SKILL.md now
   links to it.
3. images.md: collapsed Composition / Lighting / Style reference tables
   into a single "Prompt Vocabulary" table with a Category column.

Net: SKILL.md -39 lines, images.md -8 lines, shape-batch.md +33 lines
(example moved in). All 73 internal links validate.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(pptx): address Claude+Codex reviewer findings on PR #167

Two parallel reviewers (Claude pr-review-toolkit + Codex rescue) flagged
real information losses from the simplification pass. Restoring each
while keeping the overall token budget within target:

- design-system.md: restore operational tips inline on palettes #5 and
  #9 ("use dark gray/black for text", "dark mode only"). These are
  constraints (not aesthetic advice) that agents need to read palette
  values correctly. Codex M1.
- color-tokens.md: restore opacity stops at 2 / 15 / 25 / 70% (UI-state
  tokens: subtle overlay, pressed, medium, deep). Add alpha-from-pct
  formula so agents can derive intermediate values. Codex M2.
- style-recipes.md: restore the 4x4 "Corner radius by element height"
  matrix. Without it an agent sizing a 0.4" button has no concrete
  rectRadius to pick per style recipe. Codex L3 / Claude M2.
- SKILL.md shape_set_text row: restore concrete examples of what
  text_frame.text flattens (empty runs carrying explicit sz,
  normAutofit, smart-quote glyphs). Codex L4.
- images.md: restore "Mixed-media half-slide" and "Testimonial portrait"
  example prompts. The preset table references card/portrait use cases
  but had no worked prompt after the earlier trim. Claude M1.
- SKILL.md theme-key rule: re-insert concrete forbidden aliases
  ("never background / text / muted / darkest / lightest") so the
  whitelist primes against common LLM defaults. Claude L2.

All 73 internal links still validate. Smoke test: 12 PASS / 0 FAIL / 8
SKIP (same skips as prior, all for missing local tools).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(pptx): correct opacity alpha bytes at 70% and 90%

Codex re-review on PR #167 flagged the 70% row's alpha as off-by-one:
round(0.70 * 255) = 178.5 → 179 = 0xb3 (not 0xb2). Same logic applies
at 90% (229.5 → 230 = 0xe6, not 0xe5) — a parallel inconsistency that
was inherited from origin/main and not flagged the first time.

Standardize on round-half-up (the most common design-system convention)
and note it explicitly in the formula so the table is internally
consistent and unambiguous.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(pptx): restore correct palette→theme-contract mapping

A/B caveat-testing against the simplified PR flagged a real regression:
the merged 28-row palette table in design-system.md mechanically mapped
5 palette hex values to the theme-contract columns
(primary/secondary/accent/light/bg), but palettes 1-18 in the origin
listed colors in aesthetic order (dark-to-light, not theme-contract
semantic order). Column-wise assignment produced semantically wrong
mappings for ~17 of 18 palettes — most visibly palette #9 "Tech & Night"
where bg became bright gold (ffd60a) instead of near-black (000814).

Fix: split the table in two:
- Palettes 1-18: single `Colors` column with 5 hex values + instruction
  that the agent must map them to the theme contract (with special-case
  inversion rule for dark-mode palette #9).
- Palettes 19-28: keep explicit theme-contract columns (they were
  pre-curated for that schema in origin/main — e.g. #19 has primary=bg
  intentionally).

A/B re-test on the fixed file: the same prompt that produced
`bg: ffd60a` before now produces `bg: 000814` with the correct
primary=gold inversion for dark mode.

design-system.md: 78 → 85 lines (+7). Links 73/73 valid. Smoke test 12
PASS / 0 FAIL.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Reduce pptx skill runtime context by ~30% so zooclaw loads less boilerplate when the skill activates. Pure doc simplification — no functional code changes beyond two docstring trims on `clean.py` / `add_slide.py`.

**Net: 18 files, +419 / -1213 lines (-794 net).**

## What changed

- **SKILL.md**: merged the "DO NOT bypass shape-cli" whitelist and "Common rationalizations" sections into one 6-bullet anti-pattern list; moved the inline 6-op `shape_batch` worked example out to `shape-batch.md` (lazy-loaded); dropped duplicate Quick Reference table and the Visual QA Platform Support prose block.
- **references/slide-types.md**: removed 22 ASCII layout diagrams and 5 nearly-identical per-type Workflow/Key-Principles/Design-Decisions subsections; consolidated 5 font-hierarchy tables into one matrix (Cover / TOC / Divider / Content / Summary columns).
- **references/design-system.md**: palettes 19-28 keep explicit `primary|secondary|accent|light|bg` columns (they were pre-curated for that schema); palettes 1-18 keep a single `Colors` column with 5 hex values + explicit instruction that the agent must map them to the theme contract (with a dark-mode inversion note on #9). This structure was chosen after A/B testing (see below).
- **references/color-tokens.md**: 4 × 13-row scales collapsed to 4 × 5-row anchors + one 12-row opacity table with `round-half-up(pct × 255)` formula.
- **references/style-recipes.md**: 4 per-style tables + Component Mapping + 4×4 height matrix + Quick Selection Guide → one master style table, one 4×4 Corner-Radius-by-Height table, and Mixing Rules.
- **references/images.md**: 3 separate Composition / Lighting / Style tables merged into one Prompt Vocabulary table with a Category column; kept all 20 vocabulary entries.
- **references/pitfalls.md**: deleted (it was a 9-line hub; SKILL.md links directly to the 3 child files).
- **references/pptxgenjs\*.md, typography.md, editing.md**: dropped "split reference" preambles and duplicated cross-file guidance.

## Verification

**Static (both reviewers clean on final commit):**
- Claude (pr-review-toolkit:code-reviewer) — verified consolidated tables cell-by-cell, all 12 opacity alpha values match round-half-up formula, every anti-pattern scenario preserved. Recommends merge.
- Codex (codex-rescue) — found 5 real regressions across two review rounds (dropped Tips, dropped opacity stops, dropped height matrix, dropped shape_set_text examples, off-by-one alpha bytes); each fixed in `89f7692` + `460edc0`. Final review: recommends merge.

**Behavioral A/B test (10 subagents, 5 scenarios × original-vs-simplified):**

| Scenario | Original | Simplified | Status |
|---|---|---|---|
| Dark-mode palette + theme-contract mapping | `bg: 000814` ✓ | initially `bg: ffd60a` ✗ → fixed → ✓ | **real regression found & fixed** |
| Rounded button at 0.45″ height (uses restored matrix) | `rectRadius: 0.12` ✓ | `rectRadius: 0.12` ✓ | clean |
| 15% white overlay hex + PptxGenJS call | `ffffff26`, `transparency: 85` ✓ | same ✓ | clean |
| Bulk 200-slide font change (stresses anti-pattern guardrail) | `shape_batch.py` flow ✓ | same ✓ | clean |
| CJK mixed stat `¥300 亿 / 季度` | Microsoft YaHei, single run, half-width slash ✓ | same ✓ | clean |

The palette-mapping regression (commit `6e9a692`) was caught only by A/B behavioral testing, not by static review. After fix, all 5 scenarios produce equivalent answers across versions.

**Smoke test / link check:** `pptx/tests/smoke_test.sh` → 12 PASS / 0 FAIL / 8 SKIP (skips are missing local tools, same as pre-PR). `pptx/tests/check_links.py` → 73/73 internal links valid across 19 files.

## Commit history

1. `3faa153` — initial simplification pass (~800 line cut)
2. `5ee0639` — follow-up cuts from evaluation agent (merged SKILL.md anti-pattern sections, moved worked example, collapsed image tables)
3. `89f7692` — address Claude + Codex round-1 review findings (restored palette tips, opacity stops, height matrix, shape_set_text examples, images example prompts, theme-key forbidden aliases)
4. `460edc0` — round-2 Codex finding: opacity byte math (`b2`→`b3`, `e5`→`e6`) + explicit round-half-up formula
5. `6e9a692` — A/B test finding: restore correct palette→theme-contract mapping (split aesthetic swatches from curated schemas)

## Test plan

- [x] `bash pptx/tests/smoke_test.sh` → 12 PASS / 0 FAIL / 8 SKIP
- [x] `uv run pptx/tests/check_links.py pptx/` → 73/73 valid
- [x] Cell-by-cell verification of all consolidated tables against origin/main
- [x] Claude PR reviewer sign-off
- [x] Codex reviewer sign-off
- [x] Behavioral A/B on 5 high-risk scenarios with paired subagents
- [x] Reviewer: spot-check a slide-generation round-trip with the simplified doc set in a real zooclaw session

🤖 Generated with [Claude Code](https://claude.com/claude-code)

