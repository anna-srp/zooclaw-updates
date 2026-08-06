# SerendipityOneInc/ecap-skills — commits 2026-08-05

## feat(council): report genre follows the commission (#254)

- **SHA**: `a768d150896e81f63ff2f33b7f13a7de1f44e5b3`
- **作者**: felix-srp
- **日期**: 2026-08-05T20:23:47Z
- **PR**: #254

### Commit Message

```
feat(council): report genre follows the commission (#254)

## Problem

Every council report ships in the same fixed format — research-survey
structure opening with a 30-second summary — regardless of what the
topic commissioned. Staging run `ai-native-crm-designdoc` (2026-08) made
it concrete: a **design-doc** commission produced an option-survey with
zero committed decisions. Root cause: the composer template hardcodes
"ONE high-quality **research report**" and rule 6 hardcodes the
30-second-summary opening.

## Design

Genre is a property of the **commission**, not the evidence — classified
at Stage 0 (which holds the original topic), not guessed by the chair
(which only sees anonymized reports). Same pattern as depth
auto-classification: labeled on the confirm panel (`Genre: 设计文档
(auto)`), corrected at the gate via `set-cast --genre` (no init
teardown). Zero extra spawns or searches.

- **SKILL.md**: Stage 0 "Genre follows the commission" paragraph; panel
`Genre:` line + `genre <g>` adjust token; Delivery wording de-hardcoded.
- **synthesis-prompts.md**: composer preamble and reviser take a
`<genre>` slot; rule 6 maps genre → skeleton/opening (research report →
30-sec summary; design doc → goals/non-goals + COMMITTED decisions with
alternatives-and-why-they-lost; decision memo → recommendation first;
comparative review → verdict + scorecard; other → field conventions).
Revisers also sweep mechanical defects (garbled chars, typos, malformed
URLs, duplicated blocks) outside the 8-change cap.
- **Persistence (codex round-1 P1)**: `init --genre` writes genre to
status.json (authoritative for the Stage 5 `<genre>` slot and the
composer-failure fallback); `set-cast --genre` adjusts it at the gate;
schema field optional so pre-genre runs keep revalidating mid-upgrade.
- **final_synthesis.py**: `_SYNTHESIS_TEMPLATE` mirrors rules 1–6 (drift
gate green); `--genre` on the fallback CLI.

## Invocation contract

Programmatic callers can invoke as `/council ${topic}` followed by knob
lines (`depth: ${d}`, `tier: ${t}`, …). Trailing
`depth:/tier:/genre:/evidence:/synthesizer:` lines are settings, never
topic text; `auto`, blank, or an unsubstituted `${…}` literal means
unset — **code-enforced** where values become authoritative
(`_normalize_genre` in run_status, `_genre_or_default` in
final_synthesis), not just prose.

## Incident-residue cleanup (user decision 2026-08-05)

One-off incidents don't earn permanent runtime-token rules: the
exactly-once appendix guard (single occurrence, cosmetic blast radius)
and the 第14站 incident citation were removed. Codex's P0 objection to the
guard removal was adjudicated as intentional risk-acceptance; its final
round is APPROVE.

## Verification

- 274 council tests pass; drift gate green; `lint_skills.py` clean;
staged as `v0.6.12-beta.9`.
- Codex: 3 findings raised across rounds (P1 persistence — fixed; P0
guard removal — adjudicated intentional; final verdict APPROVE).
claude-review check failures are a workflow infra fault (0-second stub,
no verdict, 6× today incl. on unrelated deltas) — overridden with
--admin.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## Problem

Every council report ships in the same fixed format — research-survey structure opening with a 30-second summary — regardless of what the topic commissioned. Staging run `ai-native-crm-designdoc` (2026-08) made it concrete: a **design-doc** commission produced an option-survey with zero committed decisions. Root cause: the composer template hardcodes "ONE high-quality **research report**" and rule 6 hardcodes the 30-second-summary opening.

## Design

Genre is a property of the **commission**, not the evidence — classified at Stage 0 (which holds the original topic), not guessed by the chair (which only sees anonymized reports). Same pattern as depth auto-classification: labeled on the confirm panel (`Genre: 设计文档 (auto)`), corrected at the gate via `set-cast --genre` (no init teardown). Zero extra spawns or searches.

- **SKILL.md**: Stage 0 "Genre follows the commission" paragraph; panel `Genre:` line + `genre <g>` adjust token; Delivery wording de-hardcoded.
- **synthesis-prompts.md**: composer preamble and reviser take a `<genre>` slot; rule 6 maps genre → skeleton/opening (research report → 30-sec summary; design doc → goals/non-goals + COMMITTED decisions with alternatives-and-why-they-lost; decision memo → recommendation first; comparative review → verdict + scorecard; other → field conventions). Revisers also sweep mechanical defects (garbled chars, typos, malformed URLs, duplicated blocks) outside the 8-change cap.
- **Persistence (codex round-1 P1)**: `init --genre` writes genre to status.json (authoritative for the Stage 5 `<genre>` slot and the composer-failure fallback); `set-cast --genre` adjusts it at the gate; schema field optional so pre-genre runs keep revalidating mid-upgrade.
- **final_synthesis.py**: `_SYNTHESIS_TEMPLATE` mirrors rules 1–6 (drift gate green); `--genre` on the fallback CLI.

## Invocation contract

Programmatic callers can invoke as `/council ${topic}` followed by knob lines (`depth: ${d}`, `tier: ${t}`, …). Trailing `depth:/tier:/genre:/evidence:/synthesizer:` lines are settings, never topic text; `auto`, blank, or an unsubstituted `${…}` literal means unset — **code-enforced** where values become authoritative (`_normalize_genre` in run_status, `_genre_or_default` in final_synthesis), not just prose.

## Incident-residue cleanup (user decision 2026-08-05)

One-off incidents don't earn permanent runtime-token rules: the exactly-once appendix guard (single occurrence, cosmetic blast radius) and the 第14站 incident citation were removed. Codex's P0 objection to the guard removal was adjudicated as intentional risk-acceptance; its final round is APPROVE.

## Verification

- 274 council tests pass; drift gate green; `lint_skills.py` clean; staged as `v0.6.12-beta.9`.
- Codex: 3 findings raised across rounds (P1 persistence — fixed; P0 guard removal — adjudicated intentional; final verdict APPROVE). claude-review check failures are a workflow infra fault (0-second stub, no verdict, 6× today incl. on unrelated deltas) — overridden with --admin.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(council): surface economy tier in SKILL.md (#253)

- **SHA**: `8159a6dc33a7b84b76763f839bac919a46a26603`
- **作者**: felix-srp
- **日期**: 2026-08-05T04:41:36Z
- **PR**: #253

### Commit Message

```
fix(council): surface economy tier in SKILL.md (#253)

## Problem

`economy` tier doesn't work in practice: `roster.py` has carried a full
economy lineup since the 2026-07-20 tier redesign (members `claude-haiku
· gpt-luna · gemini-flash-lite · grok · glm · kimi · qwen`, sonnet
chair), the status schema accepts `tier: economy`, and the cast gates
pass it — verified with a local `--propose-cast --tier economy` repro
that resolves cleanly. But **SKILL.md never mentions the tier**: the
only vocabulary the orchestrating agent gets is "Default standard; offer
premium", and the confirm-gate panel's adjust tokens omit `economy`. A
user asking for an economy/cheap run has no documented path to `--tier
economy`.

## Fix (SKILL.md only, 2 lines)

- Tier paragraph now enumerates the three tiers — `economy / standard
(default) / premium` — and maps cheap/budget requests to economy
(mirroring the existing `ultra` → premium mapping).
- Confirm-gate panel adjust tokens: `premium` → `tier
economy|standard|premium` — the `tier` prefix keeps `standard`
unambiguous vs the `quick|standard|deep` depth tokens and gives a
one-token path back to the default tier (codex round-1 P1).

No script changes; `roster.py` already resolves the economy lineup.

## Verification

- `lint_skills.py`: all skills pass.
- Council suite: 271 passed.
- Local repro against a snapshot-shaped catalog: economy cast =
`claude-haiku-4-5 · gpt-5.6-luna · gemini-3.1-flash-lite · grok-4.5`,
synthesizer `claude-sonnet-5`, no skips, no unfilled seats.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## Problem

`economy` tier doesn't work in practice: `roster.py` has carried a full economy lineup since the 2026-07-20 tier redesign (members `claude-haiku · gpt-luna · gemini-flash-lite · grok · glm · kimi · qwen`, sonnet chair), the status schema accepts `tier: economy`, and the cast gates pass it — verified with a local `--propose-cast --tier economy` repro that resolves cleanly. But **SKILL.md never mentions the tier**: the only vocabulary the orchestrating agent gets is "Default standard; offer premium", and the confirm-gate panel's adjust tokens omit `economy`. A user asking for an economy/cheap run has no documented path to `--tier economy`.

## Fix (SKILL.md only, 2 lines)

- Tier paragraph now enumerates the three tiers — `economy / standard (default) / premium` — and maps cheap/budget requests to economy (mirroring the existing `ultra` → premium mapping).
- Confirm-gate panel adjust tokens: `premium` → `tier economy|standard|premium` — the `tier` prefix keeps `standard` unambiguous vs the `quick|standard|deep` depth tokens and gives a one-token path back to the default tier (codex round-1 P1).

No script changes; `roster.py` already resolves the economy lineup.

## Verification

- `lint_skills.py`: all skills pass.
- Council suite: 271 passed.
- Local repro against a snapshot-shaped catalog: economy cast = `claude-haiku-4-5 · gpt-5.6-luna · gemini-3.1-flash-lite · grok-4.5`, synthesizer `claude-sonnet-5`, no skips, no unfilled seats.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
