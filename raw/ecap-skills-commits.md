# ecap-skills Commits - Last 7 Days


## 2026-04-23


## 77f5798

**作者**: felix-srp
**日期**: 2026-04-23T00:18:05Z
**链接**: [https://github.com/SerendipityOneInc/ecap-skills/commit/77f5798cb84d51c8f2104f924e19c3ecfb07cbb9](https://github.com/SerendipityOneInc/ecap-skills/commit/77f5798cb84d51c8f2104f924e19c3ecfb07cbb9)

### Commit Message
```
chore(web-designer): trim skill docs ~460 lines for runtime context efficiency (#169)

* chore(web-designer): simplify skill docs and scripts

Tighten runtime skill files for better context engineering in ZooClaw.
Removes prose redundancy in SKILL.md, references/*.md, and scripts/ while
preserving all CSS themes, component recipes, CLI commands, and "why"
comments. Net: -460 lines.

Key changes:
- SKILL.md: condense overview/tech-stack/workflow, keep quality gates
- design-system.md: remove §13 (duplicated SKILL.md anti-slop), inline
  per-theme "Best for" + font bullets, trim aesthetic-direction prose
- components.md: compress §2 ECharts gotcha and §7.11.1 reduced-motion
  walls of prose into structured bullets
- content.md: collapse headline examples, shorten §9 image-search
  pipeline, trim per-framework narration
- scripts: light comment-tightening only; no logic changes

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(web-designer): restore three workflow anchors in SKILL.md

Reviewer flagged that the simplification dropped three procedural details
that change skill behavior:

- Phase 3: "(if project not yet initialized)" guard on init.sh — re-running
  clobbers customizations
- Phase 3: "Apply design system from references/design-system.md" +
  library role assignment (shadcn/ui base, ECharts viz, Framer animation)
- Phase 4: "verify every gate passes before delivery" — the workflow hook
  into the Quality Gates table below
- Also restored the build-workspace path so debugging the Vite output
  doesn't require reading scripts/init.sh

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #169: chore(web-designer): trim skill docs ~460 lines for runtime context efficiency

## Summary

Token-efficiency pass on `web-designer` runtime skill files, which are loaded into ZooClaw context on every invocation. **Net: -460 lines** (205 insertions, 665 deletions) with all technical content preserved.

## What changed

- **SKILL.md** — condense overview/tech-stack/workflow; keep full quality-gates table intact
- **design-system.md** — delete §13 (duplicated SKILL.md anti-slop); inline per-theme "Best for" + font bullets; tighten aesthetic-direction prose without losing the "Key CSS" signals
- **components.md** — compress §2 ECharts-gotcha and §7.11.1 reduced-motion walls of prose into structured bullets; **every TSX/JSX/TS code block preserved byte-identical**
- **content.md** — collapse headline examples to one per type; shorten §9 image-search pipeline; drop per-framework restatements
- **scripts** — comment-tightening only; no logic changes

Second commit `258ddeb` restored three workflow anchors flagged during review:
- Phase 3: "(if project not yet initialized)" guard on `init.sh`
- Phase 3: "Apply design system from references/design-system.md" + library role assignment
- Phase 4: "verify every gate passes before delivery" hook into the Quality Gates table
- Plus the build-workspace path for debugging

## Verification

### Static review (2 independent reviewers)
- Claude (`pr-review-toolkit:code-reviewer`): approve — 0 issues
- Codex (`codex:codex-rescue`): approve — 0 issues
- Both verified all 10 `[data-theme]` CSS blocks intact, every `--image-*` CLI flag, every §-cross-reference resolves, frontmatter JSON valid, markdown fences balanced, no logic change in scripts

### A/B docs test (6 parallel agents)
For 3 adversarial scenarios (reduced-motion handling, ECharts `hsl()` gotcha, image-search pipeline), paired agents received either the main-branch or PR-branch doc section and answered the same prompt. Output quality was **functionally identical** in every scenario — the trim removed restatement, not information.

### End-to-end build test (8 agents in `openclaw-docker`)
Two rounds of real skill invocations inside the production container:
- **Round 1** (no images): landing/slides/report/blog — all 4 bundled successfully with the PR docs as the only reference, producing 1.4–1.5 MB self-contained HTML.
- **Round 2** (with real images via `websearch`): 21 real images inlined across 4 bundles (1.5–2.1 MB each).

**13 doc ambiguities flagged across both rounds. Zero caused by this PR** — all pre-existing drift on main (notable: §5.4 vs §5.7 pull-quote styling, `variant="statement"` phantom prop in §7.11.1, template `.dark` block vs §3 `:root`-only instructions, citation color `text-accent` vs `text-primary`). Worth separate cleanup, not merge blockers.

## Test plan

- [x] `bash scripts/init.sh` + `bash scripts/bundle.sh` produce a self-contained HTML end-to-end
- [x] `optimize-image.py` works for PNG/JPG/WebP input and SVG via `rsvg-convert`
- [x] Reduced-motion handling survives headless screenshot (framer `useReducedMotion()` substitution + `InViewChart` `matchMedia`)
- [x] ECharts `themeColor()` helper correctly bridges Tailwind CSS vars to legacy `hsl(H, S, L)` syntax
- [x] Websearch pipeline (logo + real-photo fallback) runs end-to-end with real credentials
- [x] Two independent code reviews pass

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## b17a718

**作者**: felix-srp
**日期**: 2026-04-23T00:16:40Z
**链接**: [https://github.com/SerendipityOneInc/ecap-skills/commit/b17a718d77f744a565faf335394288e258b98943](https://github.com/SerendipityOneInc/ecap-skills/commit/b17a718d77f744a565faf335394288e258b98943)

### Commit Message
```
pdf: trim runtime docs (~50%) + schema/cache fixes from audit (#166)

* chore(pdf): trim runtime .md files for context efficiency

Token-efficiency pass on skill docs (loaded at runtime by zooclaw).
Total: 1919 → 947 lines (~50% reduction).

- SKILL.md: 230 → 206 (tighten route summaries, drop filler)
- references/forms.md: 427 → 241 (dedupe coord docs, compress pitfalls)
- references/images.md: 267 → 221 (tighten prose, dedupe with SKILL.md)
- design/design.md: 383 → 279 (collapse 13 cover patterns to one-liners,
  drop aspirational prose, simplify math/figure guidance)
- references/reference.md: 612 → deleted (zero incoming references,
  generic library examples unused by any route)

Preserved: all footguns, absolute-path warnings, checkbox /Yes rule,
coord-mode invariants, ReportLab superscript workaround.

* chore(pdf): safe script cleanups — dead code + hot-path hoists

- render_body.py: drop unused pdfmetrics/TTFont imports; guard
  _configure_matplotlib so repeat calls (per chart/math/flowchart) no-op
  instead of re-adding font-manager paths
- cover.py: remove orphan "Cross-hatch SVG helper" banner left behind
  after the helper was deleted
- palette.py: drop legacy tokens.json keys (font_heading, font_body_b)
  — zero readers in the tree
- pdf_tools.py: hoist watermark font selection above the per-page loop
  (watermark text doesn't change page-to-page, so the CJK scan was O(pages))
- fonts.py: memoize _needs_noto via lru_cache — called per codepoint
  from _canvas_set_font (4×/page for header/footer) and wrap_non_latin
  (every paragraph); cache hit rate ~99% on multi-page docs

* fix(pdf): schema accuracy + footguns surfaced during trim audit

Follow-up to 40a0b5c. An audit pass found load-bearing gaps that predated
the trim (both original and trimmed docs had them). Fixing while we're
in-context.

- forms.md: `fill_inspect.py` field output uses `bbox`, not `rect`
  (scripts/fill_inspect.py:108,125). Updated JSON example, coordinate
  systems reference, and the y-flip formula. Also added the real output
  envelope ({has_fields, fields}) and the no-fields shape.
- forms.md: new pitfall — fields whose page annotation cannot be
  resolved are silently dropped with a stderr warning
  (fill_inspect.py:134). If the list looks short, check stderr.
- images.md: documented both body-image error modes — `[Image not
  found: <path>]` (missing file, render_body.py:787) and `[Image
  error: <exception>]` (corrupt/0-byte, render_body.py:799). Renderer
  never fails on image load; it substitutes a caption-style placeholder.
- images.md: restored the sharper `--cover-image` phrasing — "silently
  fail to load — rendered without the image and no error is reported".
- SKILL.md: one-liner noting CJK / non-Latin auto-handling
  (render_body.py wordWrap="CJK" + wrap_non_latin). Prevents agents
  from preprocessing mixed-script content.json.

* fix(pdf): review findings — fill_annotate schema, fonts cache purity

Two code fixes from parallel review agents (Claude + Codex) plus one doc tightening.

1. fill_annotate.py: accept both Format A (nested {pages, form_fields})
   and Format B (flat array). Before, agents following references/forms.md's
   Approach A built nested JSON that passed check_bounding_boxes.py (which
   normalizes both) but then failed fill_annotate.py with "fields_json must
   contain a JSON array" — a real wall at the final step of Track B.
   Added _normalize_fields matching the logic in check_bounding_boxes.py
   and create_validation_image.py. Coord-mode signals (pdf_width/pdf_height
   vs image_width/image_height) are treated as exclusive: a field that
   declares one doesn't inherit the other from page meta.

2. fonts.py: _needs_noto read the mutable _discovered dict while being
   wrapped in @lru_cache, caching a pre-registration None forever if any
   caller hit it before register_all(). Split into pure _script_for
   (cached classification, safe) + thin _needs_noto wrapper that
   re-checks _discovered on every call. Classification is the expensive
   work; the dict gate is O(1).

3. design.md: expanded the one-line image error-mode hint so the summary
   matches the detailed block in references/images.md.

* fix(pdf): round 2 review — empty fields no-op + partial-hint warn + forms.md Format B

Round 2 review (Codex) caught two regressions from 1e6c873 and one doc gap.

1. Empty [] fields.json: original fill_annotate.py treated it as "0
   annotations to add, succeed"; my 1e6c873 rewrite conflated "bad shape"
   with "empty list" and started erroring on empty inputs. _normalize_fields
   now returns None only for truly-bad shapes (non-list, non-dict); empty
   list and empty form_fields both produce an empty list that the fill loop
   handles as a no-op.

2. Partial coord-mode hints (e.g. image_width without image_height) used
   to silently fall through to page meta, which can supply the opposite
   coord mode — an agent's intent was lost with no signal. Now logs a
   warning listing which partial keys were present; falls back to page
   meta as before. Coord modes stay exclusive.

3. references/forms.md now documents both accepted schemas — Format A
   (nested {pages, form_fields} mirroring form_structure.json) and
   Format B (flat array, leaner). Before, forms.md only showed Format A
   while SKILL.md only mentioned the flat array; neither was wrong for
   check_bounding_boxes.py but it set agents up to discover the mismatch
   only at fill_annotate.py. Also notes the empty-array no-op behaviour.

* fix(pdf): round 3 — partial coord-hint warn covers Format B too

Codex round-3 flagged a consistency gap: the partial-hint warning added
in 2a1f799 only fired on the Format A (nested) normalization path;
Format B flat-array fields bypassed normalization and reached
fill_with_annotations with partial hints silently dropped into the
page-dimension fallback.

Extracted the partial-hint check into _warn_partial_coord_hint and call
it from both branches — Format B passthrough now iterates the list and
warns per-field, same as Format A. Shared helper keeps the two paths
in sync.

(Codex also flagged the `list[dict] | None` annotation as 3.10+-only;
false positive — the rest of pdf/scripts/ has been using `str | None`
and `list[dict]` since before this PR — fill_inspect.py, fill_write.py,
extract_form_structure.py, check_bounding_boxes.py,
create_validation_image.py all already require 3.10+. No new baseline.)

* fix(pdf): left-align FreeText annotations by default

Smoke-testing Track B surfaced that filled form text was horizontally
centered in the entry rect, which reads as wrong for form-fill UX —
users expect the text to appear where they would have written it
(left-aligned at the start of the line).

Root cause: pypdf's FreeText annotation defaults to center quadding
(/Q=1) and doesn't expose a constructor argument for it.

Fix: set /Q=0 (left quadding) on the annotation dict after
construction. Accepts an optional per-field "align" key in the flat
schema (0=left/1=center/2=right) for the rare case where a caller
wants to override; default is left for both formats.

Format A (nested) fields route through _normalize_fields which
doesn't propagate alignment — intentional; if you need per-field
alignment, use Format B.

* feat(pdf): add --dpi flag to ocr subcommand

Default was pdf2image's 200 DPI, which struggles on handwritten or
small-font Chinese text — a scanned resume form with the name "胡宁"
round-tripped through OCR as "#8" (tessdata_fast/chi_sim at 200 DPI)
and "骨宁" (best model at 200 DPI). At 400 DPI with tessdata_best the
same image OCRs to "胡 宁" — searchable.

- ocr: new --dpi (default 300, was unspecified/200). Bump to 400-600
  for handwritten/small-font CJK. Matches the existing --dpi flag on
  to-images.
- SKILL.md: mention the flag in the ocr example + a one-line hint that
  tessdata_best substantially beats tessdata_fast on CJK accuracy.

No behavior change at default for non-CJK inputs aside from slightly
higher resolution (200 → 300), which produces cleaner but larger
output PDFs. Callers can pin --dpi 200 if they need the old size.

* docs(pdf): mention --dpi + tessdata_best hint in ocr usage
```

### PR #166: pdf: trim runtime docs (~50%) + schema/cache fixes from audit

## Summary

Runtime context-efficiency pass on the `pdf` skill (loaded every invocation by zooclaw) that grew — through an audit + review rounds + an A/B evaluation + end-to-end smoke tests across CREATE / FILL / TOOLS + sibling-skill integration checks — into a small set of correctness and UX fixes the original code/docs were already quietly hiding.

### 1. Runtime `.md` token reduction — 1,919 → 964 lines (~50%)

| File | Before | After | Notes |
|---|---:|---:|---|
| `SKILL.md` | 230 | 208 | tighten route summaries; added CJK auto-handling line + ocr `--dpi`/tessdata_best hint |
| `references/forms.md` | 427 | 264 | dedupe coord docs; compress pitfalls; document both fields.json schemas |
| `references/images.md` | 267 | 230 | dedupe with SKILL.md; sharper cover-image trap phrasing; documented both body-image error modes |
| `design/design.md` | 383 | 279 | collapse 13 cover patterns to one-liners; drop aspirational prose |
| `references/reference.md` | 612 | deleted | generic library examples with zero incoming references from any route; follow-up design doc captures useful bits for later promotion to `pdf_tools.py` subcommands |

**Preserved intact** — every footgun: absolute-path `--cover-image` (Playwright temp-dir), checkbox `checked_value`, coord origins (A bottom-left / B top-left), ReportLab U+2070–U+209F black-box trap, CJK auto-handling (newly explicit), body image error modes, `fill_inspect.py` silent-drop.

### 2. Safe script cleanups (no behaviour change)

- `render_body.py`: drop unused `pdfmetrics` / `TTFont` imports; guard `_configure_matplotlib` so repeat calls (per chart/math/flowchart, 10+ per doc) no-op instead of re-adding font-manager paths
- `cover.py`: remove orphan `# ── Cross-hatch SVG helper ──` banner
- `palette.py`: drop legacy `font_heading` / `font_body_b` tokens.json keys (zero readers)
- `pdf_tools.py`: hoist watermark-font selection above the per-page loop (O(pages × text_len) → O(text_len))

### 3. Correctness + UX fixes (surfaced by audit / review / smoke test)

- **`fill_inspect.py` field schema** — docs said `rect`; actual key is `bbox`. Pre-existing bug in both original and trimmed docs. Also surfaced the `{has_fields, fields}` envelope and the silent-drop warning from `fill_inspect.py:134`. (audit)
- **`fill_annotate.py` schema acceptance** — `check_bounding_boxes.py` and `create_validation_image.py` accepted both nested `{pages, form_fields}` and flat arrays, but `fill_annotate.py` only took flat, so agents following the docs' nested schema passed validation then crashed at fill. Added `_normalize_fields` matching siblings; coord modes (`pdf_*` vs `image_*`) are exclusive; partial hints log a warning; empty array remains a 0-annotation no-op. (review)
- **`fonts._needs_noto` cache purity** — was `@lru_cache`d while reading the mutable `_discovered` dict — could freeze a pre-registration `None` forever. Split into cached pure `_script_for` (classification only) and a thin live-gate `_needs_noto`. (review)
- **`fill_annotate.py` FreeText alignment** — pypdf's `FreeText` defaults to `/Q=1` (centered) and exposes no constructor arg. Filled form text appeared horizontally centered instead of where someone would have written it. Set `/Q=0` (left) on the annotation dict; accepts optional per-field `"align"` override. (smoke test)
- **`pdf_tools.py ocr --dpi` flag** — default was pdf2image's 200 DPI, too low for handwritten or small-font Chinese. On a real resume scan, "胡宁" OCR'd as "#8" at 200 DPI / tessdata_fast; at 400 DPI / tessdata_best it OCRs correctly. Added `--dpi` (default 300) + SKILL.md note recommending tessdata_best over tessdata_fast for CJK. (smoke test)
- **`references/forms.md` schemas** — now documents both Format A (nested, mirrors `form_structure.json`) and Format B (flat array) with a note that either works end-to-end and empty array is a no-op.

### 4. Review + validation process

- **Round 1** → 3 findings → fixed in `1e6c873`
- **Round 2** → 2 regressions + 1 doc gap → fixed in `2a1f799`
- **Round 3** → 1 coverage gap + 1 false positive → fixed in `f873672`
- **Round 4** → both reviewers ship ✓
- **A/B evaluation** — 4 paired agents on CJK, form-fill Track B, cover selection, Unicode sub/super. Net: trim is neutral-to-positive; Format B + code fix unblocks Track B.
- **End-to-end smoke tests in openclaw-docker** — CREATE + FILL (both tracks, both schemas, empty-array no-op) + TOOLS (merge/split/rotate/watermark/to-images/extract-images/read/encrypt/decrypt/ocr) + cover-image absolute-vs-relative trap + 4 cover patterns + non-CJK non-Latin scripts + sibling-skill integration (websearch reached end-to-end; designer reached LiteLLM but user's subscription expired — not a PR issue). Surfaced FreeText alignment and OCR DPI bugs; both fixed in the PR.

## Commit sequence

```
40a0b5c chore(pdf): trim runtime .md files for context efficiency
7f1c2b9 chore(pdf): safe script cleanups — dead code + hot-path hoists
7782c05 fix(pdf): schema accuracy + footguns surfaced during trim audit
1e6c873 fix(pdf): review findings — fill_annotate schema, fonts cache purity
2a1f799 fix(pdf): round 2 review — empty fields no-op + partial-hint warn + forms.md Format B
f873672 fix(pdf): round 3 — partial coord-hint warn covers Format B too
271add3 fix(pdf): left-align FreeText annotations by default
4069f60 feat(pdf): add --dpi flag to ocr subcommand
7be87db docs(pdf): mention --dpi + tessdata_best hint in ocr usage
```

## Verified end-to-end

- [x] All modified Python files parse (`ast.parse`)
- [x] Shell scripts parse (`bash -n`)
- [x] `make.sh` no-args prints expected usage; `make.sh check` clean
- [x] Modules import under `uv run --with reportlab --with matplotlib`
- [x] `fonts._needs_noto` preserves classification across register → de-register → re-register (purity verified via live gate)
- [x] `fill_annotate._normalize_fields` — 7 unit cases: flat passthrough, nested→flat conversion, coord-mode exclusivity, empty-list no-op, partial-hint warn on both paths, bad-shape `None` return, label-only entry skipped
- [x] 2 reviewers × 4 rounds → ship
- [x] A/B doc evaluation vs original docs → net positive
- [x] **CREATE end-to-end** (container): 11-page CJK PDF from 235-line source markdown with 41 blocks; `report/fullbleed` + `#00B4A6` teal
- [x] **Block-type coverage** (container): math×3, flowchart with back-edge, code×2, divider, spacer, pagebreak, bibliography, figure+caption, image+missing-path fallback
- [x] **Cover pattern variants** (container): `magazine` with cover_image, `atmospheric`, `terminal`, `poster`
- [x] **Multi-script body** (container): Cyrillic/Greek/Arabic/Devanagari + mixed-script line — Noto auto-wrap works
- [x] **FILL Track A** (native fields): `fill_inspect.py` output confirmed `bbox` key (not `rect`); `fill_write.py` populated text/checkbox/choice fields; re-inspect confirmed values
- [x] **FILL Track B Format A** (nested): 3 annotations via `_normalize_fields` path
- [x] **FILL Track B Format B** (flat): 3 annotations via passthrough; left-aligned correctly after `271add3`
- [x] **Empty `[]` fields.json**: exit 0, 0 annotations, PDF written
- [x] **Watermark with CJK**: stamped `机密文件 CONFIDENTIAL` on 11-page PDF (font hoist exercised live)
- [x] **TOOLS**: `merge` (2 → 14pp), `split` (11 → 2pp), `rotate` 90°, `encrypt`/`decrypt` roundtrip, `extract-images`, `read`
- [x] **OCR** (Chinese scanned resume): `chi_sim+eng` at `--dpi 400` with `tessdata_best/chi_sim` → "胡宁" and body text extractable from searchable PDF (per-char x-gap in CJK output tracked as follow-up)
- [x] **Cover-image path trap**: relative path silently fails to load image; absolute path embeds it. `~1.7 KB size delta = embedded PNG bytes`; documented silent-fail behaviour confirmed
- [x] **Sibling-skill integration**: `websearch` end-to-end (returned 10 real image hits for "Ivanpah solar farm"); `designer` reached LiteLLM (subscription-expired on upstream models — not a PR issue)

## Follow-up (tracked, not in this PR)

- `~/Workspace/design-doc/ecap-skills/pdf/2026-04-22-reference-md-promotion-plan.md` — plan for converting the most useful bits from the deleted `reference.md` (qpdf linearize/repair, `pdfimages` raw extraction, `pdftotext -bbox`) into first-class `pdf_tools.py` subcommands.
- `~/Workspace/design-doc/ecap-skills/pdf/2026-04-22-cjk-ocr-spacing-rewrite-plan.md` — plan for rewriting `cmd_ocr`'s invisible text layer using `pytesseract.image_to_data` + reportlab to produce CJK-contiguous text runs (so Cmd-F finds "胡宁" not just "胡 宁"). Pre-existing tesseract behaviour; real fix is ~100-150 lines and warrants its own PR.

## Devcontainer observations (not blocking)

- Chinese OCR requires `tessdata_best/chi_sim.traineddata` + the tesseract `configs/` dir under `$TESSDATA_PREFIX`. Worth adding `tesseract-ocr-chi-sim` to the Dockerfile.
- `designer` skill's `image_generation_cli.py` needs `aiohttp`/`litellm`/`openai`/`Pillow` but doesn't pre-declare via `uv run --with`. Running directly fails with `ModuleNotFoundError: aiohttp`. Out of scope for this PR — fix lives in the designer skill.

---

## 1ce789a

**作者**: felix-srp
**日期**: 2026-04-22T23:55:46Z
**链接**: [https://github.com/SerendipityOneInc/ecap-skills/commit/1ce789aed6ad500ba252f8ab2f96969e5c93a0e9](https://github.com/SerendipityOneInc/ecap-skills/commit/1ce789aed6ad500ba252f8ab2f96969e5c93a0e9)

### Commit Message
```
chore(meeting-notes): simplify SKILL.md, transcript prompt, speaker script (#165)

* chore(meeting-notes): simplify SKILL.md, transcript prompt, and speaker script

Reduce runtime-loaded markdown by ~23% to save LLM context budget, add the
env-check boilerplate the project CLAUDE.md requires, and fix real bugs in
the speaker-embed script (docstring flag mismatch, running-mean drift on
re-register, stdout-vs-stderr violation, dead diarization fallback).

* chore(meeting-notes): restore compression and rationale guidance

Audit pass on the prior simplify commit flagged two rules from the original
that landed implicit when they should be explicit: (1) weighting coverage by
importance (the "uniform compression" anti-pattern), and (2) capturing the
why/when for decided items so the rationale survives to future readers.

* chore(meeting-notes): address code-review findings on PR #165

Fix three items the review flagged:

- Drop `requires.env: ["HF_TOKEN"]` from the frontmatter so the zooclaw
  runtime doesn't block skill load when only the pasted-text / Gemini-only
  path is used. HF_TOKEN is genuinely optional — required solely for the
  pyannote voice-matching add-on. Prerequisites block updated to reflect
  this and now gates the env check to `speaker_embed.py extract`.

- `register_speaker`: document the legacy-profile caveat at the running-mean
  block so future readers know to re-register speakers written by the old
  `(old+new)/2` formula.

- `extract_embeddings`: log a summary warning when one or more speakers in
  the input segments produced zero successful embeddings, so the caller
  isn't silently missing them from the output JSON.

* fix(meeting-notes): HF_TOKEN prereq check exit status

Codex review caught a subtle bug in the Prerequisites block: the one-line
`[ -z "$HF_TOKEN" ] && echo ... && exit 1` pattern exits with status 1
even when HF_TOKEN is set, because the short-circuited `[ -z ... ]`
becomes the final command and returns false. Any caller treating the
prerequisite as a gate would reject a correctly-configured environment.

Replace with an explicit `if/then/fi` block so success falls through
with exit status 0.

* fix(meeting-notes): plug anti-pattern regression found in A/B test

A blinded A/B run of 3 adversarial transcripts (small-talk-heavy with one
decision; pure brainstorm with implicit action item; mixed-language with
partial speaker identification) showed the trimmed SKILL.md regressed on
the small-talk-heavy case by ~3 rubric points, specifically because it
fabricated (a) an orphan action item ("Execute cut of retargeting — Unclear
owner") and (b) a Risks &amp; Concerns section with a risk the transcript
never raised. Both failure modes were covered by the original Anti-Patterns
section that the simplify pass had removed.

Re-add a compact "Common Failure Modes" block (~50 words, 3 bullets) and
add two targeted questions to Self-Check ("Did I list any task without
both an owner and a deadline as an action item?" and a fabricated-section
guard). These directly rebut the measured regression without undoing the
broader simplification.

Net: SKILL.md 161 → 166 lines. Still well under the original 206.
```

### PR #165: chore(meeting-notes): simplify SKILL.md, transcript prompt, speaker script

## Summary

- Compress the runtime-loaded markdown (SKILL.md, prompts/transcript.md) by ~23% to save LLM context budget when the skill is loaded into Zooclaw. Removed duplicated guidance (Anti-Patterns + Self-Check restated the same rules; Output Language duplicated Multilingual Support; What-Good-Minutes duplicated Anti-Patterns; horizontal-rule decoration). All operational rules preserved (`Unknown`/`Unclear`/`Inferred` vocabulary, 0.85/0.70 thresholds, `YYYY-MM-DD_topic.md` convention, section toolkit).
- Add project CLAUDE.md §4 boilerplate: `requires.env`/`primaryEnv` in SKILL.md frontmatter and the standard Prerequisites env-check snippet for `HF_TOKEN`.
- Fix real bugs in `scripts/speaker_embed.py`:
  - Docstring advertised `--embedding` (singular) but argparse expected `--embeddings` (plural) — copy-paste from the docstring would fail.
  - `register` averaged as `(old + new) / 2`, which halves the first sample's weight every re-registration (after N registers the first sample is 1/2^N). Switched to a true running mean tracked via `num_observations`.
  - Success log lines printed to stdout alongside the JSON payload, polluting `match`'s stdout contract — moved all progress/log output to stderr per project CLAUDE.md §3.
  - Removed the dead diarization fallback in `extract_embeddings` (SKILL.md already mandates passing `--segments` from the Gemini transcript). `--segments` is now required; `load_pyannote` simplified.
  - Added early `HF_TOKEN` validation gated to the `extract` subcommand (the only one that needs pyannote).

Net: 228 insertions / 367 deletions across 3 files.

## Test plan

- [x] `uv run --with numpy scripts/speaker_embed.py --help` works without `HF_TOKEN`
- [x] `uv run --with numpy scripts/speaker_embed.py extract --audio x --segments y --out z` fails fast with `ERROR: HF_TOKEN is not set`
- [x] `match` against an empty profiles dir returns `confidence: "new"` for every speaker
- [x] `register` creates a fresh profile with `num_observations: 1`; re-registering the same speaker increments to 2 and merges via running mean
- [x] Python AST parse OK
- [ ] End-to-end run with a real audio file + Gemini transcript + HF-authenticated pyannote (requires live creds; to be verified by Ning)

---

## b544a99

**作者**: felix-srp
**日期**: 2026-04-22T17:21:01Z
**链接**: [https://github.com/SerendipityOneInc/ecap-skills/commit/b544a99dca98138d67b060406dc72a03c583e4a7](https://github.com/SerendipityOneInc/ecap-skills/commit/b544a99dca98138d67b060406dc72a03c583e4a7)

### Commit Message
```
chore(humanizer): harden fabrication guardrail (Rule 6 → Rule 1, 4 defenses) (#176)

* chore(humanizer): strengthen Rule 6 fabrication guard

Follow-up to #168, where the blind A/B test surfaced that both ZH runs
invented numeric metrics (revenue growth, margin, retention rates) not
present in the source text. The previous Rule 6 wording was too soft
and the examples.md rewrites modeled the fabricating behavior.

Four reinforcing defenses:

1. SKILL.md Rule 6 → Rule 1: promoted to first rule (priority signal),
   sharpened to enumerate every forbidden specific class (numbers, %,
   $, dates, durations, versions, counts, names, attributions, quotes).
   Added "when the input is vague, the rewrite stays vague."

2. Step 4 VERIFY: mandatory pre-output fabrication audit — enumerate
   every specific in the draft, confirm each exists in the input, drop
   anything that fails.

3. Output Format: added a visible "Fabrication audit" line so the
   check leaves an audit trail in the output, not just in the model's
   head.

4. examples.md: added a prominent note that specific figures in the
   "after" texts (23% growth, $15/seat, AES-256, etc.) came from the
   author's ground-truth knowledge of the product/quarter — NOT
   invented during rewriting. Without ground truth, the rewrite must
   match the input's specificity.

Also tightened Hard Constraints row from "Fabricated data/sources" to
"Specifics absent from source (numbers, names, dates, attributions,
quotes)" to make the constraint concrete.

Net diff: 2 files, +11/−7 — preserves PR #168's context-efficiency.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(humanizer): compress fabrication guard (~50% fewer tokens)

Runtime context optimization pass. Every token in these .md files is
loaded into Zooclaw's context window when the skill fires, so compress
aggressively while preserving every guardrail signal from the earlier
commit.

Key compressions:

1. Rule 1: collapse the class enumeration to canonical form
   ("numbers, %, $, dates, durations, versions, counts, proper nouns,
   attributions, quotes"). Drop the rhetorical flourish "adding
   plausible-sounding figures is a hallucination, not a humanization"
   (pure pathos, adds no constraint). Drop "the non-negotiable rule"
   descriptor — the ⚠️ glyph carries that weight. 88 → 48 words.

2. Step 4 VERIFY: cross-reference "Rule 1 specific" instead of
   re-enumerating the 11 classes — one source of truth. Keep the
   enumerate-then-verify procedure and the explicit
   "lost-specificity-is-acceptable" override (load-bearing — resolves
   the tradeoff the model faces). 58 → 29 words.

3. Hard Constraints row: "Fabricated specifics (per Rule 1) | 0" —
   cross-reference instead of partial re-enumeration. 9 → 5 words.

4. Output Format: "each kept specific → source phrase; or 'None'" —
   keep the visible audit trail and the None branch (which lets
   vague-input cases pass without pressure to invent). 19 → 10 words.

5. examples.md note: drop the 7-item parenthetical enumeration to 4,
   collapse the duplicated "vague in → vague out" restatement to one
   phrasing, remove the "(重要)" redundant with ⚠️. ~175 → ~90 chars.

All four reinforcing defenses still fire; each just uses fewer tokens
to do it. Net PR diff: 2 files, +6/-6 (was +11/-7).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(humanizer): address Claude + Codex review findings

Adversarial reviews (Claude + Codex) on the compression pass surfaced
three real leaks that the original PR #176 design missed or that the
compression commit (cfcf682) inadvertently exposed:

CRITICAL (Codex) — Personality directives leak. The "Have opinions,"
"Use first person," "Be specific about feelings" guidance in Soul &
Personality combined with examples that invent lived experience
("拖了一年", "三次推翻了推荐算法", "Discord 里找我", "We built this
because we had the problem ourselves") push the model to fabricate
NON-numeric specifics — and Rule 1 never triggers because its class
list was numeric-only. Fix: extend Rule 1's class list to cover
names, locations, URLs/handles, titles/roles, product capabilities,
internal history/process, motives, emotions, causal claims,
comparatives/superlatives, and hedges. Added: "First-person voice,
opinions, and lived experience must stay at the source's level of
claim."

HIGH (Codex) — "Equivalent transform" loophole. Undefined enough to
launder estimates: "many customers" → "thousands"; "significant
growth" → "20%". Fix: tighten to "arithmetic restatement of explicit
source data," with explicit counter-examples ("many" ≠ "thousands";
"significant growth" ≠ "20%").

HIGH (Claude + Codex) — examples.md note too narrow. The top note
only foregrounded "具体数字" but the examples also invent product
names (Aria), channels (Discord, Slack, Google Docs), internal
history, and motives. The "见 Rule 1" cross-ref also dangles when
examples.md loads standalone. Fix: broaden from "数字" → "事实,"
enumerate the non-numeric fabrication categories from the examples
themselves, inline the full class list so the note stands alone.

MEDIUM (Codex) — Shallow audit risk. Output Format permitted
"Pass" summary. Fix: Step 4 now requires explicit enumeration
("bare 'Pass' is insufficient"); Output Format adds "Dropped: X"
for removed specifics.

NIT (Codex) — examples.md line 121 "Replace vague claims with
specific facts or honest uncertainty" read as permission to
invent facts. Fix: "source-backed facts, or with honest
uncertainty when no source is available."

Also restored the "plausible invention is hallucination, not
humanization" framing (Codex LOW) in compact form — directly
targets the PR #168 failure mode.

Rule 1 grew from ~48 → ~95 words. Net trade: Rule 1 still shorter
than PR #176's pre-simplification original (was ~93 words, now ~95
with substantially broader coverage — the compression headroom
went into covering the gaps reviews found).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(humanizer): address Codex re-review (per-example warnings + math boundary)

Second-round review: Claude says ship; Codex says ship with two
minor fixes. Applying both.

MEDIUM (Codex, persistent across rounds) — per-example inline
warnings. Top-note-only leaves a skip-ahead imitation path: a
model jumping directly to Example 2 sees "营收同比增长 23%",
"毛利率从 38% 提到了 41%", "18 个月" without context and copies
the pattern. Fix: one-line ⚠️ warning before each "改写后"/"After"
block naming the specific invented items from that example's
ground truth ("23%, 38%→41%, 89%, 7 家, 18 个月" for ZH prof;
"版本号, AES-256, 时间线" for ZH casual; "Aria, Slack, 40%
beta metric, \$15/seat" for EN). ~20 tokens/example, eliminates
the skip-ahead loophole.

LOW (Codex) — math boundary underspecified. Without guidance a
model may confuse percentage points with percent change
("38%→41%" → "3% growth" is wrong; "3x" → "200% more" is right).
Fix: add "Preserve units; percentage points ≠ percent change
('38%→41%' is NOT '3% growth')" to Rule 1's equivalent-transform
clause, plus a positive example ("3x" → "200% more").

Skipped:
- Codex LOW on personality bullets: already covered by Rule 1's
  "First-person voice, opinions, and lived experience must stay
  at the source's level of claim"
- Codex NIT on Rule 1 compression: reviews disagree (Claude says
  current length is load-bearing, Codex proposes 72-word version);
  the 72-word version drops "quotes" from the enumeration, so
  adopting it would regress coverage

Net: Rule 1 grew ~95 → ~105 words (math clause); examples.md
grew +6 lines (3× inline warnings).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(humanizer): expand Example 1 & 3 inline warnings

Codex's final-pass audit caught that the per-example warnings added
in the previous commit named only a subset of the invented specifics
visible in the "改写后"/"After" blocks:

- Example 1 (ZH Casual) warning listed "版本号、AES-256、时间线"
  but the rewrite also invents "拖了一年", "推翻三次",
  "AES-128→AES-256", "Google Docs", "Discord", "企业版",
  "每天下午". A model imitating the example would see the full
  invented set but a narrower "these came from ground truth" list,
  teaching it that only some invented specifics need sourcing.

- Example 3 (EN Professional) warning listed "Aria, Slack, 40% beta
  metric, $15/seat" but the rewrite also invents
  "Slack/email/PM-tool integration", "free trial, no card",
  "two-week efficacy window", and the "three tools, two async
  teams" backstory.

Example 2 was already complete.

Fix: extend each warning to enumerate every fabricated specific
visible in its paired "改写后"/"After" block. Closes the partial-
warning loophole Codex flagged in the final-pass audit.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(humanizer): make per-example warnings category-exhaustive

Codex's 4th-round audit caught that the expanded warnings still
missed whole fabrication categories in each After block:

- Example 1: algorithm shift ("规则→行为数据") and onboarding
  timeline ("一周后开始认识你") not flagged
- Example 2: business judgments (企业市场押注、中小客户放缓)
  and risk prediction (续约季、两家大客户到期、决策层换人)
  not flagged — warning only covered numbers
- Example 3: UX details (unified inbox, urgency-learning),
  pricing policy (free trial, no card), and backstory (status
  meetings, "falling through the cracks") not flagged

Fix: restructure each warning as category-grouped enumeration
with "等/etc." closer to exhaustive coverage. Example 1 now
covers timeline / R&D process / technical details / naming /
team commitments. Example 2 covers numbers / business judgments
/ risk prediction. Example 3 covers product name / integrations /
UX / metrics / pricing / backstory.

Structural change: each warning now has the form "every
non-source specific — (category: examples), (category: examples)...
— comes from ground truth." This signals exhaustiveness and
keeps the inoculation complete without enumerating every phrase.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(humanizer): close remaining per-example warning gaps

Codex's 5th-round audit found three concrete specifics still
uncovered by the category-grouped warnings:

- Example 1: "升级动机'不是出问题而是准备企业版'" (causal
  claim from the After block) was absent from the 技术细节
  category
- Example 2: "好于预期"、"市场也在配合" (business judgments)
  and "3 家来自竞争对手流失" (a number) were absent from
  their respective categories
- Example 3: "workflow tool" category framing and the
  "teams spend more time routing information than acting on
  it" problem statement were absent from the product/backstory
  coverage

Fix: add each named specific to its respective category in
the per-example warning. The exhaustiveness claim now holds
against a direct cross-check of each After block.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(humanizer): add remaining motive to Example 1 warning

Codex round-6 final gap: Example 1 After block contains
the motive phrase '用不顺手的东西我们自己也不想发' (the
reason for the year-long delay), which wasn't in any
warning category. Added to 研发过程 category.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #176: chore(humanizer): harden fabrication guardrail (Rule 6 → Rule 1, 4 defenses)

## Summary

Follow-up to #168. The blind A/B test in that PR surfaced that both Chinese-language runs **fabricated numeric metrics** — `营收同比增长 23%`, `毛利率 38%→41%`, `客户续约率 89%`, `新签大客户 7 家` — none of which appear in the source input. #168 flagged this as "worth a separate PR." This is that PR.

**Root cause (two layers):**
1. Rule 6 was soft ("Don't invent statistics, sources, or attributions") and buried as the last of 6 rules.
2. `examples.md` actively *modeled* fabrication — every example's "改写后"/"After" block invents specifics (numbers, product names like `Aria`/`Discord`, pricing like `$15/seat`, backstory like `"three tools, two async teams"`) not present in its paired input. The skill was teaching the behavior it forbade.

**Net diff:** 2 files, +18/−8 (8 commits, 6 review rounds).

## Four reinforcing defenses

1. **Rule 6 → Rule 1** (`SKILL.md`) — promoted to first rule (priority signal), ⚠️ marked. Enumerates 20+ fabricable categories: numbers, `%`, currency (¥/$/€/元/万), dates, durations, versions, counts, rankings, names, locations, URLs/handles, titles/roles, attributions, quotes, product capabilities, internal history/process, motives, emotions, causal claims, comparatives/superlatives, hedges. Defines **"equivalent transform"** as arithmetic-only (`"3x" → "200% more"` OK; `"many" ≠ "thousands"`, `"38%→41%"` is NOT `"3% growth"`). Guards personality fabrication: *"First-person voice, opinions, and lived experience must stay at the source's level of claim."*

2. **Step 4 VERIFY** (`SKILL.md`) — mandatory pre-output **Fabrication audit** as the first sub-step: enumerate every Rule 1 specific, map each to its source phrase, drop any without a source. Bare `"Pass"` is explicitly insufficient.

3. **Output Format** (`SKILL.md`) — visible `Fabrication audit:` line in `[VERIFICATION]` with contract: `each kept specific → source phrase; "Dropped: X, Y" for removed; or "None"`. Audit trail is externalized, not just in the model's head.

4. **examples.md inoculation** — broad top note (`具体事实` not just `具体数字`, inlined class list so the file stands alone) + per-example ⚠️ inline warnings immediately before each `改写后`/`After` block. Each warning uses category-grouped enumeration covering every non-source specific in its paired rewrite: Example 1 (timeline / R&D process / tech details / naming / team commitments), Example 2 (numbers / business judgments / risk prediction), Example 3 (product name / category framing / integrations / UX / metrics / pricing / backstory).

Also tightened Hard Constraints row: `Fabricated data/sources | 0` → `Fabricated specifics (per Rule 1) | 0`.

## Review

6 rounds of adversarial review (Claude `pr-review-toolkit:code-reviewer` + Codex `codex:codex-rescue` in parallel). Findings closed across all severity tiers:

- **CRITICAL (Codex):** Personality directives leaking into non-numeric fabrication (lived experience, motives, emotions). Fix: Rule 1 class list expanded beyond numeric categories + *"source's level of claim"* constraint.
- **HIGH (Codex):** `"Equivalent transform"` loophole laundering estimates (`"many" → "thousands"`). Fix: arithmetic-only definition + counter-examples.
- **HIGH (Claude + Codex):** examples.md note too narrow + dangling `见 Rule 1` cross-ref. Fix: broadened to `具体事实`, inlined full class list, per-example inline warnings.
- **MEDIUM:** Missing classes (currencies beyond `$`, locations, URLs), shallow `"Pass"` audit risk. Fix: expanded enumeration + audit contract.
- **LOW:** Math boundary (percentage points vs percent change). Fix: explicit `"38%→41%" is NOT "3% growth"` guard.
- **NIT:** `examples.md:"Replace vague claims with specific facts"` read as permission to invent. Fix: `"source-backed facts, or honest uncertainty when no source is available."`

Final verdict from both reviewers: **ship**.

## Test plan

- [x] **Blind A/B re-run on ZH quarterly-report fixture from #168** — cold subagent invocation with skill content loaded. Rewrite contains zero numbers/percentages/counts/dates; only kept specific is `行业前三` which IS in the source. Agent's own audit adversarially flagged a candidate time-anchor leak (`"比上季度更紧"`) and proposed a fix — guardrail working as intended. The #168 failure mode (`23%`, `38%→41%`, `89%`, `7 家`) does not reproduce.
- [x] **`Fabrication audit:` line populated correctly** — both test runs produced explicit `specific → source phrase` mappings plus `Dropped:` enumeration; neither produced a bare `"Pass"`.
- [x] **EN product-announcement spot-check** — cold run on the vague marketing fixture. Rewrite has no `Aria`, no `$15/seat`, no `40% less time`, no Slack/email/PM-tool integrations, no beta figures, no backstory. Agent's audit explicitly enumerated all 6 invented categories as NOT invented.
- [x] **Structural integrity** — 4-Step SOP, Voice Mode, Hard Constraints, Quality Score (50-point) sections all intact.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 7d7a699

**作者**: felix-srp
**日期**: 2026-04-22T17:19:45Z
**链接**: [https://github.com/SerendipityOneInc/ecap-skills/commit/7d7a6996d42d9f9d70b2e6cafa6509a89d423c61](https://github.com/SerendipityOneInc/ecap-skills/commit/7d7a6996d42d9f9d70b2e6cafa6509a89d423c61)

### Commit Message
```
chore(docx): simplify zip iteration + compress runtime-loaded markdown (#164)

* chore(docx): simplify zip iteration and dead code

- pack.py: single rglob pass instead of 3 tree walks (xml, rels, all)
- unpack.py: single rglob with suffix filter instead of two passes
- diff_docx.py: _extract_all opens each zip once (was 3× per file); replace __import__ idiom with a top-level pathlib import
- validators/docx.py: drop ELEMENT_RELATIONSHIP_TYPES override (no-op; inherited from base.py as {})

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(docx): compress design_principles.md (819→156 lines)

Rewrite as dense spec for runtime skill context: keep all XML examples,
numerical specs, ratio tables, and the final decision checklist; drop
narrative "Why It Works" paragraphs and ASCII-art diagrams that serve
human readers but bloat model context.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(docx): dedup encyclopedia part 2/3 headers

Part 2 and Part 3 each restated the full C# namespace alias block that
Part 1 already defines. Replaced with a reference to Part 1 plus only the
additional usings specific to each part (A/DW/PIC for part 2; +M for
part 3). Part 3's EMU conversion block collapsed to a single line.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(docx): drop redundant Overview/Reference preambles

- comments_guide.md: "## Overview" header + restated-title sentence → keep the sentence, drop the header and separator
- track_changes_guide.md: same pattern → same fix
- xml_editing_guide.md: drop "## XML Reference" + meta-commentary line; promote Schema Compliance/Tracked Changes/Comments/Images from ### to ## and their children from #### to ### to keep a clean outline

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(docx): remove duplicate Content JSON Format in scenario_a

The same JSON format spec appeared twice — once at the top as a summary,
again at line 160 under "## Content Configuration JSON Format" with more
detail (example keys, CLI flag note). Keep the complete version only.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(docx): restore 'Why It Works' rationale in design_principles.md

Hybrid rewrite after review:
- Restore the pedagogical "Why It Works" paragraphs for all 6 principles
  (saccades, cultural margin signals, line-spacing physiology, Gestalt
  proximity, river-of-whitespace etymology, modular-scale harmonics) —
  these drive model judgment calls on edge cases.
- Keep modular-scale table, hierarchy table, and decision checklist
  already compressed in the previous pass.
- Drop ASCII-art page-layout diagrams from the original — spatial ASCII
  adds little for a model; the information is already in the XML and
  prose.
- Drop verbose preambles ("This produces a page where...", "Research
  on content density consistently shows...") and some narrative filler.

Net: 819 → 397 lines (~51% reduction) while preserving all load-bearing
content that drives judgment calls, not just the specs a model could
copy-paste. Quality first; tokens second.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(docx): include _rels/.rels in pack/unpack file iteration

Codex PR review caught this regression. Path("_rels/.rels").suffix is
"" (no extension before the dot), so the suffix-set filter missed the
root package relationships file present in every Office document.

- pack.py: _condense_xml was skipped for _rels/.rels — functionally
  harmless (zip still wrote it), but inconsistent with pre-change
  behavior that applied condensation to all *.rels.
- unpack.py: _pretty_print_xml and _escape_smart_quotes were skipped
  for _rels/.rels — visible regression (root rels not pretty-printed,
  smart quotes not escaped). Also caused the "unpacked N XML files"
  count to be off by one.

Fix: use name.endswith(".xml"|".rels") which matches the original
rglob("*.xml")/rglob("*.rels") glob semantics.

Verified: unpack of tests/fixtures/source.docx now reports 20 files
(was 19); round-trip diff remains clean; validate.py passes.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(docx): trim SKILL.md redundancies

Small surgical cuts — not a rewrite. SKILL.md is already well-structured;
only clear redundancies removed:

- 3-bullet pipeline overview at top duplicated the Pipeline Router ASCII
  below. Collapsed to one sentence pointing at the router.
- "OpenXML SDK reference" preamble tightened (one sentence, same info).
- Trailing "C# samples in ..." pointer at the end was redundant with the
  Samples table already referenced under Pipeline A.

Net: 204 → 199 lines. Keep Quick Reference table (lookup role), Samples
topic table (useful navigation), Reference Loading Guide (core index),
and every CRITICAL warning intact.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #164: chore(docx): simplify zip iteration + compress runtime-loaded markdown

## Summary

Simplify pass over the `docx/` skill, targeting runtime-loaded context (markdown) and low-risk Python hygiene. Net **+209 / −673 across 11 files**.

### Markdown token reduction (runtime skill context for zooclaw)
- **`design_principles.md`** — 819 → 414 lines (~51% reduction). Hybrid rewrite: **kept** all "Why It Works" pedagogical rationale, every XML example, modular-scale table, hierarchy table, decision checklist, numeric thresholds. **Dropped** ASCII-art page-layout diagrams (low signal for a model) and verbose narrative preambles. Validated against `~/Workspace/design-doc/ecap-skills/docx/docx-design-principles.md` for intent preservation.
- **`openxml_encyclopedia_part2/3.md`** — removed duplicate base C# `using` block; each part now references Part 1 plus only its own additional aliases. Part 3's 6-line EMU table collapsed to one line.
- **`xml_editing_guide.md`** — dropped redundant `## XML Reference` parent heading + meta-commentary; promoted children one level to keep a clean outline.
- **`comments_guide.md` / `track_changes_guide.md`** — dropped duplicate `## Overview` headers (the sentence they wrapped already followed as body).
- **`scenario_a_create.md`** — removed a 14-line `## Content JSON Format` section that was an exact duplicate of a later section.

### Python hygiene
- **`pack.py` / `unpack.py`** — single `rglob` pass instead of 2–3 separate pattern walks. Uses `name.endswith(".xml" | ".rels")` to preserve glob semantics for the root package `_rels/.rels` (where `Path.suffix` is `""`).
- **`diff_docx.py`** — `_extract_all()` opens each zip exactly once (was 3× per side). Also replaces the `__import__("pathlib").Path` idiom with a proper top-level import.
- **`validators/docx.py`** — removes dead `ELEMENT_RELATIONSHIP_TYPES = {}` override (no-op duplicate of the inherited definition in `base.py`).

## Commit history

| SHA | Description |
|---|---|
| `2f74041` | Python hygiene: zip iteration + dead code |
| `69c46e9` | First pass at `design_principles.md` compression (superseded) |
| `8499d95` | Dedup encyclopedia part 2/3 headers |
| `0fdbc7b` | Drop redundant Overview/Reference preambles |
| `d509d2a` | Remove duplicate Content JSON Format in scenario_a |
| `6952666` | Restore "Why It Works" rationale — hybrid (final 414 lines) |
| `c8bde21` | Fix `_rels/.rels` skipped by suffix filter (caught in Codex review) |

## Verification

**Two-model PR review (Claude + Codex in parallel), two rounds.**
- Round 1: Codex caught `Path("_rels/.rels").suffix == ""` causing root package rels to be skipped by the suffix-set filter; Claude had missed it.
- Round 1 fix landed in `c8bde21`: switched to `name.endswith(...)` which mirrors the original `rglob("*.rels")` glob semantics.
- Round 2: both reviewers LGTM.

**A/B stress tests — Python (8 cases, byte-level parity old vs new):**
- 6 DOCX fixtures full round-trip → identical unpacked lists, zip member order, and `diff_docx` JSON
- PPTX round-trip → identical
- XLSX with non-ASCII filename → identical
- Synthesized broken DOCX (missing `word/styles.xml`) → identical JSON report
- Synthesized broken DOCX (missing `word/document.xml`) → identical JSON report
- Dot-prefix `_rels/.rels` → matched on both branches after fix
- Non-ASCII filename `word/中文.xml` in tree → handled identically
- Synthetic `customXml/*` + `customXml/_rels/*` → handled identically

**A/B stress tests — Markdown (5 design-decision tasks, old 819-line vs new 414-line ref):**
- Corporate styles.xml, academic body paragraph, CJK body paragraph, anti-pattern diagnosis, "make it luxurious" judgment call — **identical XML output** from both versions; same principles cited, same thresholds applied. The hybrid compression preserves full design-decision capability.

**Smoke tests:**
- `unpack → pack` round-trip on `tests/fixtures/source.docx`: 20 XML files, 0 diff after repack
- `validate.py` passes (exercises `DOCXSchemaValidator`)
- `ast.parse` clean on all Python files
- `--help` output on `diff_docx.py`, `pack.py`, `unpack.py`

## Test plan for reviewer
- [x] Python round-trip on all 6 `tests/fixtures/*.docx` — byte-identical vs main
- [x] PPTX and XLSX round-trip — byte-identical vs main
- [x] `diff_docx.py` on missing-part docx — identical JSON vs main
- [x] `validate.py` passes
- [x] Markdown decision-parity verified with dual-agent A/B on 5 design tasks

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 7eff19d

**作者**: felix-srp
**日期**: 2026-04-22T17:11:37Z
**链接**: [https://github.com/SerendipityOneInc/ecap-skills/commit/7eff19dbd21a78a95d0f18d6a55790fb69d0bbc9](https://github.com/SerendipityOneInc/ecap-skills/commit/7eff19dbd21a78a95d0f18d6a55790fb69d0bbc9)

### Commit Message
```
chore(xlsx): simplify runtime skill docs by 50% (validated by A/B tests) (#170)

* chore(xlsx): simplify skill docs and scripts for tighter runtime context

Reduce .md files from 3481 → 1732 lines (~50%) by dropping duplicated
content across references (color table, openpyxl round-trip warning, style
append procedure), compressing verbose XML before/after blocks, collapsing
ASCII diagrams, and consolidating ownership of shared topics into one file.

Fixes:
- edit.md: `recalc.py output.xlsx /tmp/recalc.xlsx` was passing a file path
  as the timeout argument (int) and would crash. Corrected to in-place call.
- validate.md: removed stale claim that recalc uses `--convert-to xlsx`
  (it actually invokes a StarBasic macro).

Python cleanup (behavior-preserving):
- remove unused NS_DRAWING/NSMAP from xlsx_shift_rows.py
- remove unused `import sys` and `last_col_num` from xlsx_add_column.py
- remove unused `df._reader_encoding` assignment from xlsx_reader.py and
  the redundant `(UnicodeDecodeError, Exception)` tuple
- remove unused TEMPLATE_SLOT_ROLES from style_audit.py

All 21 existing tests pass; pack + formula_check smoke-tested on the
minimal_xlsx template.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(xlsx): fix recalc.py behavior docs and restore assumption ordering

Quality audit of PR #170 found two accuracy issues in validate.md and one
important content loss in format.md.

validate.md:
- Corrected default timeout from 60s → 120s (matches recalc.py argparse default)
- Corrected "works on a temp copy first" (false) → "modifies in place; temp
  directory holds only the isolated LibreOffice user profile". This matches
  recalc.py's actual behavior (oDoc.store() on the loaded URL).

format.md:
- Restored the canonical 6-category assumption ordering (revenue → cost →
  working capital → capex → financing → tax), condensed to a one-line bullet.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(xlsx): fix 6 bugs found by Claude+Codex dual review of PR #170

Blockers:
- edit.md: sharedStrings example had "...existing <si> entries..." inside an
  XML code fence, which renders as real XML with an unclosed <si> tag. Wrapped
  the placeholder in a proper <!-- ... --> comment.
- ooxml-cheatsheet.md: worked example for adding a Summary sheet used rId3,
  which contradicts the adjacent rule that rId3 is reserved for sharedStrings
  in the minimal_xlsx template. Changed to rId4 and annotated the relationship
  block with the reservation note.
- format.md: step 6 "Verify" and step 7 "Pack" pointed at /tmp/xlsx_fmt/unpacked/,
  but step 1 unpacks to /tmp/xlsx_fmt/ directly. Fixed path to /tmp/xlsx_fmt/.
- validate.md: JSON schema put `unknown_name_ref` under `errors`, but
  formula_check.py actually emits it under a separate `warnings` array with
  `warning_count`. Restructured schema to match script output (SKILL.md:121
  already matches; docs are now consistent).
- fix.md: workflow only ran `formula_check.py`, but SKILL.md requires the full
  3-stage validation before delivery. Added `recalc.py` and `office/validate.py`
  steps plus a pointer to validate.md.
- recalc.py: validate.md claims the script passes `--norestore` to LibreOffice,
  but the cmd did not. Added the flag so docs and behavior agree (prevents
  session-restore hangs in automation).

All 21 existing tests still pass.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(xlsx): preserve template <cols> widths and sheetFormatPr attrs

A/B testing surfaced a small regression from the simplify pass: agents
reading the condensed create.md could produce functionally-correct but
cosmetically-degraded files — dropping custom column widths and the
x14ac:dyDescent attribute when building multi-sheet workbooks. Files
still recalculate correctly, but they open with default widths in Excel.

Add a one-liner to the Worksheet files step explaining why copying
sheet1.xml (vs writing from scratch) matters, and include <cols> + the
namespaced <sheetFormatPr> in the example XML so the copy pattern is
obvious.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #170: chore(xlsx): simplify runtime skill docs by 50% (validated by A/B tests)

## Summary

Cuts the runtime footprint of the `xlsx/` skill's markdown by ~50% (3481 → 1745 lines across 8 files) while preserving correctness. zooclaw (openclaw cloud) loads these `.md` files on every skill invocation, so each redundant paragraph costs tokens and attention.

Also fixes pre-existing bugs surfaced during review, removes dead Python code in 4 scripts, and adds `--norestore` to `recalc.py` so it matches what the docs promise.

## Footprint changes

| File | Before | After | Δ |
|---|---:|---:|---:|
| SKILL.md | 199 | 168 | −16% |
| references/create.md | 691 | 335 | −52% |
| references/edit.md | 684 | 270 | −60% |
| references/format.md | 768 | 325 | −58% |
| references/validate.md | 774 | 312 | −60% |
| references/ooxml-cheatsheet.md | 231 | 200 | −13% |
| references/fix.md | 37 | 41 | +11% (added full 3-stage validation) |
| references/read-analyze.md | 97 | 97 | − |
| **Total .md** | **3481** | **1745** | **−50%** |

## Simplification patterns

- **Deduplication across files** — color/role table, openpyxl round-trip warning, append-only style procedure, 7 error types, and AARRGGBB format were each explained in 3-4 files. Consolidated to a single owner per topic with cross-references from others.
- **Trimmed before/after XML pairs** — kept one representative example where multiple were repeating the same pattern.
- **Removed ASCII diagrams** that restated content already in adjacent tables.
- **Compressed over-explanation** (5-step walkthroughs collapsed to 1-2 sentence summaries where the steps are self-evident from the code block).

## Bug fixes (caught during review)

### Script-vs-docs accuracy
- `edit.md`: previously instructed `recalc.py output.xlsx /tmp/recalc.xlsx` — but `recalc.py` takes `(file, timeout_int)` as positionals, so the second path would crash with an argparse type error. Corrected to the in-place invocation.
- `validate.md`: dropped stale claim about `--convert-to xlsx` + `--infilter` (script actually uses a StarBasic macro). Fixed default timeout claim (`60s` → actual `120s`) and "works on a temp copy" (false — script modifies in place; the temp directory only isolates the LibreOffice user profile).
- `validate.md` JSON schema: `unknown_name_ref` was lumped under `errors`, but `formula_check.py` emits it under a separate `warnings` array with `warning_count`. Schema restructured to match.
- `fix.md`: workflow only ran `formula_check.py` but SKILL.md requires all 3 validation stages before delivery. Added `recalc.py` and `office/validate.py` steps and a pointer to `validate.md`.

### XML-example accuracy
- `edit.md`: sharedStrings example had `...existing <si> entries...` inside a code fence, which parses as malformed XML with an unclosed `<si>` tag. Wrapped in a proper `<!-- ... -->` comment.
- `ooxml-cheatsheet.md`: Summary-sheet example used `rId3`, which collides with the adjacent rule that rId3 is reserved for sharedStrings. Changed to `rId4` and annotated with the reservation note.
- `format.md`: verify/pack steps pointed at `/tmp/xlsx_fmt/unpacked/` but the unpack step writes to `/tmp/xlsx_fmt/` directly. Fixed path consistency.

### Python
- `recalc.py`: added `--norestore` to the soffice command list. The docs claimed it was passed, but the flag was missing — without it, LibreOffice can hang on session-restore prompts in automation.
- Dead-code removal in 4 scripts (all verified unused via grep):
  - `xlsx_shift_rows.py`: dropped unused `NS_DRAWING`, `NSMAP`
  - `xlsx_add_column.py`: dropped unused `import sys`, unused `last_col_num`
  - `xlsx_reader.py`: dropped dead `df._reader_encoding` assignment; collapsed redundant `(UnicodeDecodeError, Exception)` (Exception subsumes the former)
  - `style_audit.py`: dropped unused `TEMPLATE_SLOT_ROLES` dict
- No CLI flags changed. No stdout/JSON output-shape changes.

## Validation

Every claim in this PR was checked by multiple independent passes:

1. **Initial simplification** (`cb487e1`) — reviewed by one Claude agent for redundancy and cross-reference integrity.
2. **Quality audit** (`50b9775`) — second Claude agent compared simplified vs original file-by-file; found 2 accuracy bugs + 1 content loss. All fixed.
3. **Dual PR review** (`81a2614`) — Claude's `code-reviewer` and Codex each independently audited the branch. Between them: 6 unique blockers (4 from Codex, 3 from Claude, 1 overlap). All 6 fixed. Re-reviewed by both → LGTM, no regressions.
4. **A/B caveat testing** (`b49d9b3`) — 3 caveat scenarios chosen to probe areas where the simplification cut the most content (multi-sheet CREATE, append-only style surgery, parsing human-readable FAIL output). Each scenario ran twice: once with an agent restricted to the original docs, once with an agent restricted to the simplified docs. A 7th blind evaluator compared the actual XML of the produced `.xlsx` files.

### A/B results

| Scenario | Targets cut content | main | simplified | Verdict |
|---|---|---:|---:|---|
| Multi-sheet CREATE + cross-sheet refs | Scenarios B/C dropped from create.md | 9/10 | 8/10 | Correct; slight cosmetic regression |
| Append new style slot | §3.1/§3.2 compressed in format.md | 10/10 | 10/10 | Byte-identical `styles.xml` |
| Parse FAIL output | Worked FAIL example dropped from validate.md | 9/10 | 9/10 | Equivalent diagnoses |

Both variants in every scenario passed `formula_check.py` with zero errors. LibreOffice recalc on the S1 outputs produced identical correct results (`6000` and `6900`).

**One regression surfaced**: in S1, the simplified create.md no longer taught agents to preserve the template's custom `<cols>` widths and `x14ac:dyDescent` attribute on `<sheetFormatPr>`. Files still recalculated correctly but would open with default column widths in Excel. Fixed in `b49d9b3` with a one-paragraph addition to the Worksheet-files step.

## Test plan

- [x] All 21 existing tests pass (`bash xlsx/scripts/run_tests.sh`)
- [x] Smoke-tested `xlsx_pack.py` + `formula_check.py` on `templates/minimal_xlsx/`
- [x] Verified every script invocation in every `.md` against the live argparse / `sys.argv` parsing
- [x] Verified all XML examples are well-formed
- [x] Verified `formula_check.py` warnings schema matches the docs
- [x] Verified `recalc.py` argv order: `--headless` → `--norestore` → `-env:UserInstallation` → macro URL
- [x] Two independent post-fix reviews (Claude + Codex) both returned LGTM
- [x] A/B test on 3 caveat scenarios confirmed no correctness regression
- [ ] Verify in zooclaw runtime that the slimmer skill still handles canonical CREATE / EDIT / VALIDATE flows end-to-end

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## d535fd0

**作者**: felix-srp
**日期**: 2026-04-22T13:02:55Z
**链接**: [https://github.com/SerendipityOneInc/ecap-skills/commit/d535fd0ea7186dc18600fb3bbb08d821800f88d1](https://github.com/SerendipityOneInc/ecap-skills/commit/d535fd0ea7186dc18600fb3bbb08d821800f88d1)

### Commit Message
```
chore(glossary): archive _dev/ design docs to external vault (#177)

Glossary's _dev/ design docs (decisions.md, future-options.md,
search-coverage.md) have been copied to the maintainer's external
design-doc archive (Obsidian vault via ~/Workspace/design-doc alias).

They're kept for historical reference, not needed in the runtime repo.
Runtime SKILL.md is unaffected — this removes only the dev-only folder.

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #177: chore(glossary): archive _dev/ design docs to external vault

## Summary
- Glossary's `_dev/` design docs have been copied to the maintainer's external design-doc archive (Obsidian vault via `~/Workspace/design-doc/ecap-skills/glossary/`).
- They're kept for historical reference, not needed in the runtime repo.
- Runtime `SKILL.md` is unaffected — this removes only the dev-only folder.

**Files moved (then deleted here):**
- \`glossary/_dev/decisions.md\` (195 lines — includes the two TODO items logged in PR #163)
- \`glossary/_dev/future-options.md\` (42 lines)
- \`glossary/_dev/search-coverage.md\` (41 lines)

## Test plan
- [ ] Verify the vault copy contains all three files with the merged-into-main content (decisions.md has the `## 待决策（TODO）` section from PR #163).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## d3fc590

**作者**: felix-srp
**日期**: 2026-04-22T12:54:51Z
**链接**: [https://github.com/SerendipityOneInc/ecap-skills/commit/d3fc59061ea34d6e80d70a4b6aea32695d6dc4be](https://github.com/SerendipityOneInc/ecap-skills/commit/d3fc59061ea34d6e80d70a4b6aea32695d6dc4be)

### Commit Message
```
chore(glossary): simplify runtime skill for token efficiency (−24%, zero comprehension loss) (#163)

* chore(glossary): simplify SKILL.md for token efficiency

Glossary is a runtime skill for zooclaw — fewer tokens means better
context engineering for consumers (B1/B2/B5/B6, etc.).

- Merge duplicated Phase/field-mapping tables in SKILL.md into a single
  compact 3-row phase table plus one-line field mapping.
- Drop unused "Path Resolution Rule" (skill has no scripts).
- Drop "Two-Layer Architecture (Future, Not MVP)" — already captured in
  _dev/future-options.md.
- Trim redundant tagline, verbose phase prose, and trivia ("inspired by
  Anyword").
- Delete references/cold-start-phases.md — unreferenced from SKILL.md
  and duplicated its content verbatim.

No runtime instructions removed; references/extract-terms-prompt.md and
references/dedup-merge-prompt.md are unchanged.

SKILL.md: 228 → 162 lines (-29%). Total runtime markdown: 401 → 302.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(glossary): restore concrete examples in Layer 3 capture list

Review feedback: one-liner compression lost the concrete correction
examples that let a runtime agent recognize each capture scenario.
"name formatting" alone is materially vaguer than seeing "'Ning' → '胡宁'".

Restores the three bulleted scenarios (B2 Humanizer, B5 Weekly Report,
B1 Transcription) with their original concrete examples — +3 lines,
still well below the original 228-line version.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(glossary): restore Phase C cost-reduction contrast (300K → 15K)

A/B comprehension test surfaced that the trimmed version preserved
Phase C's "title + first 200 chars" strategy and the ~15K cost, but
dropped the "~300K for full scan" counterfactual. That baseline is
decision-relevant — it explains why the truncation optimization exists.

Restores the contrast in a single inline clause (~10 tokens). Runtime
token budget still ~25% below the original.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(glossary): restore Phase B granularity from deleted reference

Audit of the (now-deleted) references/cold-start-phases.md surfaced two
runtime-relevant facts that the first-pass trim folded away:

1. Phase B cost breakdown: Gmail signatures ~20K + Calendar attendees 0
   (structured data, free). The aggregate "~20K" hid that Calendar
   parsing is free — relevant for anyone reasoning about per-source
   cost.

2. Phase B merge behavior: incrementally merges as it runs, with a
   final dedup pass after A/B/C. The original pipeline is stream-then-
   batch, not batch-only — useful for agents reasoning about interim
   state.

Both additions cost ~8 tokens combined; the trim still delivers ~25%
runtime token reduction vs main.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(glossary): log two Layer 3 spec gaps surfaced by PR #163 A/B tests

Adversarial A/B testing on PR #163 surfaced two pre-existing design
gaps in Layer 3 (correction = learning). Both existed in main before
the simplify trim, but the testing gave us a concrete write-up. Logged
to _dev/decisions.md under "待决策 (TODO)" for later resolution.

TODO 1: "3rd-occurrence re-ask" rule has no time window (cross-day?
cross-session? open).

TODO 2: If a user manually reverses a previously auto-added correction,
agent behavior is undefined (stick / undo / ask / threshold).

Neither is caused by the simplify; both need a product decision before
Layer 3 is implemented.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #163: chore(glossary): simplify runtime skill for token efficiency (−24%, zero comprehension loss)

## Summary

Trim the glossary skill's runtime markdown to reduce context cost for zooclaw consumers (B1 Transcription, B2 Humanizer, B5 Weekly Report, B6 Document Generation) without losing any runtime-actionable information.

**Result: `SKILL.md` 2,262 → 1,720 tokens (−542, −24.0%), 229 → 166 lines (−27%). Plus one dead reference file deleted (400 tokens, never loaded at runtime).**

## What changed

**`glossary/SKILL.md`** — rewritten for density:
- Fused three Phase sub-sections into one 3-row table (Phase × Source × Cost × Time).
- Collapsed "Model Selection" from 4 rows to 2 (no-LLM vs Gemini Flash groups).
- Flattened `metadata` frontmatter from 6-line JSON to one line.
- Compressed "Layer 4 Manual Maintenance" and consumer skills list.
- Dropped: unused "Path Resolution Rule" (glossary has zero scripts; `lint_skills.py` only enforces this when SKILL.md documents script execution); "Two-Layer Architecture (Future, Not MVP)" (already in `_dev/future-options.md`); redundant tagline; "inspired by Anyword" trivia.

**`glossary/references/cold-start-phases.md`** — deleted:
- Never linked from `SKILL.md` (so the on-demand-load path never fired).
- Content was duplicated verbatim into `SKILL.md`.
- No mention in any `_dev/` design doc.
- Appears to have been speculative scaffolding from initial commit that was never wired up.

**NOT touched:** `references/extract-terms-prompt.md`, `references/dedup-merge-prompt.md` — these are LLM prompt templates where wording precision matters for downstream behavior.

## Validation

### Two independent reviews — both clean
- **pr-review-toolkit:code-reviewer** — frontmatter parses, `lint_skills.py` passes, zero inbound references to deleted file, all cross-refs resolve. No blocking issues.
- **codex:codex-rescue** — all cost/latency numbers preserved (~3s / ~20K / ~15K / ~5K / 60%+), frontmatter valid YAML (Ruby Psych verified), lint schema requirements met, CI workflow PyYAML install intact. No blocking issues.

### Blinded A/B comprehension test (16 runtime-relevant Qs, two independent agents)
**15/16 answers equivalent.** One divergence (Q16: Phase C cost-reduction contrast) — fixed in commit `9e3fae2` by restoring the "~300K vs ~15K" counterfactual.

### Adversarial A/B test (12 caveat-probing Qs)
**11 ties + 1 NEW-wins, 0 regressions.** NEW wins Q6 ("Can Phase B output be used before Phase C finishes?") because commit `fc7efea` stated the stream-then-batch behavior more directly than the original prose.

Two spec gaps surfaced during adversarial testing — present in BOTH old and new versions, pre-existing to this PR:
- **Q3:** "3rd occurrence re-ask" rule has no time window (cross-day? cross-session? open question).
- **Q12:** No spec for what the agent should do when a user manually reverses a previously auto-added correction.

These are worth a follow-up issue but are not caused by this trim.

## Commits

1. `76383d8` — initial simplify (228 → 162 lines).
2. `55cf2ef` — restored concrete Layer 3 capture examples (Claude review feedback).
3. `9e3fae2` — restored Phase C 300K → 15K cost-reduction contrast (comprehension A/B fix).
4. `fc7efea` — restored Phase B granularity (Calendar=0 breakout + incremental-merge behavior) from the deleted reference.

## Final numbers

| Metric | Main | This PR | Δ |
|---|---|---|---|
| `SKILL.md` tokens | 2,262 | 1,720 | **−542 (−24.0%)** |
| `SKILL.md` lines | 229 | 166 | −27% |
| Deleted orphan reference | 400 tokens | 0 | −400 |
| Runtime comprehension fidelity (A/B) | baseline | equivalent + 1 gain | **no loss** |

## Test plan
- [ ] CI `lint_skills.py` passes (already verified locally).
- [ ] Install the branch in zooclaw and run a "glossary" trigger to confirm the cold-start description remains actionable.
- [ ] Optional: file a follow-up issue for the two spec gaps (3rd-occurrence time window; auto-add reversal behavior).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 2e31a2c

**作者**: felix-srp
**日期**: 2026-04-22T12:10:42Z
**链接**: [https://github.com/SerendipityOneInc/ecap-skills/commit/2e31a2c225f88ea9ba953423df4afbc580484125](https://github.com/SerendipityOneInc/ecap-skills/commit/2e31a2c225f88ea9ba953423df4afbc580484125)

### Commit Message
```
chore(humanizer): simplify skill markdown (−228 lines, +1pt blind A/B) (#168)

* chore(humanizer): simplify skill markdown for tighter runtime context

Tighten SKILL.md prose, strip source-attribution headers/footers from
all 12 language pattern packs, drop redundant "所做更改" recap lines
(the before/after diff already shows the change), and compress the
three worked examples (flatten score tables to totals, remove the
change-breakdown tables). All triggers, before/after pairs, and
replacement tables are preserved.

* chore(humanizer): restore Arabic RTL note and per-dimension example scores

Review found two LOW-severity regressions from the simplification pass:

1. ar-patterns.md dropped the runtime hint that Arabic is right-to-left;
   promote it to a visible blockquote below the title so the LLM still
   sees it when loading the pattern pack.
2. examples.md compressed per-dimension quality scores to totals, but
   SKILL.md's Output Format advertises 5-dimension scoring. Restore
   inline per-dimension scores (still one line each) so the examples
   model the advertised output.
```

### PR #168: chore(humanizer): simplify skill markdown (−228 lines, +1pt blind A/B)

## Summary

Runtime-focused simplification of the `humanizer/` skill (SKILL.md + 13 language pattern packs + examples.md). Every MD in this skill is loaded into Zooclaw's context window when the skill fires, so smaller files = better context engineering.

**Net diff:** 14 files, +75 / −303 lines (≈30% reduction on changed files).

## Changes

- **`SKILL.md`**: tightened prose; merged the identical Chinese/English columns in Hard Constraints into one `Limit` column; flattened the 13-line pattern-pack list to a one-line glob reference; preserved 4-step SOP, 6 Core Rules, Voice Modes, Glossary Integration, Quality Rubric, and Output Format verbatim.
- **`references/{lang}-patterns.md`** (all 12 languages): stripped `# Source:` / `# Severity:` header comments and `*Source: ...*` footer lines (non-functional attribution). Preserved every trigger word, severity label, before/after example, and replacement table.
- **`references/zh-patterns.md`**: additionally removed 10 redundant `**所做更改：**` recap lines after before/after pairs (the diff is self-explanatory); compressed the Hard Constraints checklist.
- **`references/examples.md`**: replaced per-example 5-dimension score tables with inline one-line per-dimension scoring (matching SKILL.md's Output Format spec); removed per-example `Changes Made` breakdown tables; kept all three full before/after pairs and risk reports.
- **`references/ar-patterns.md`**: Arabic RTL note repositioned as a proper blockquote below the title (was previously an H1-prefixed comment that didn't render).

## Validation

**1. Two-reviewer static review** (Claude + Codex, in parallel): no CRITICAL/HIGH issues; 2 LOW issues surfaced and fixed in commit `7062cd1` (restored Arabic RTL note; restored per-dimension scores in all three examples).

**2. Quality-preservation audit**: scored 14/14 files at 8.5–10 across 8 dimensions (trigger completeness, severity integrity, before/after examples, replacement tables, language-specific notes, cross-refs, output-format demo, token economy). No trigger word, severity label, replacement-table row, pattern number, or language-specific note is missing.

**3. Blind A/B empirical test**: ran the skill with original vs. simplified SKILL+pattern-pack on two AI-flavored inputs (EN product announcement, ZH quarterly report). A separate blind evaluator rated all four outputs without knowing which version was which:

| | Original | Simplified | Δ |
|---|---|---|---|
| English | 44/50 | **46/50** | +2 |
| Chinese | 45/50 | 45/50 | 0 |
| **Avg** | 44.5 | **45.5** | **+1** |

The simplified EN run actually showed *more* rigorous detection (per-item vocabulary tiering, explicit copula-avoidance flagging, pattern-ID citation) than the original. ZH runs were tied. Blind verdict: "normal run-to-run variance, not behavior drift" — quality is preserved or slightly improved.

## Test plan

- [x] `git show origin/chore/humanizer-simplify:humanizer/SKILL.md` — SOP, voice modes, constraints, rubric, output format all intact
- [x] Both reviewers confirm no regressions remain after fixup commit
- [x] Blind A/B test: simplified ≥ original on all measured runs
- [ ] (Follow-up, not in this PR) Strengthen SKILL.md Rule 6 fabrication guard — blind test surfaced that both ZH runs invented numeric metrics; this pre-exists the simplification but is worth a separate PR

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 7b3846d

**作者**: vincent-srp
**日期**: 2026-04-22T12:01:50Z
**链接**: [https://github.com/SerendipityOneInc/ecap-skills/commit/7b3846d5586207943832fceb89f865493df9fdd1](https://github.com/SerendipityOneInc/ecap-skills/commit/7b3846d5586207943832fceb89f865493df9fdd1)

### Commit Message
```
docs(specialist-manager): elevate convergence to three-in-one principle (#175)

* docs(specialist-manager): elevate convergence to three-in-one principle

Rewrites "Convergence-before-card discipline" as "Convergence discipline":
card IS the commit-question (convergence + ask + commit collapse into one).
Names the disguised-balanced-close variant as an explicit failure mode so
future LLM generalization catches "Ready to hire X, or look at others?" and
similar, not just the literal "Want to hire X?".

Scopes Turn 2's balanced two-option close to shortlist/menu mode only;
once focus has narrowed to one candidate, menu mode ends and Convergence
takes over. Turn 3+ detail-dive bullet now references the principle by
name instead of repeating the rule, and adds lead-avatar guidance for
image+text agent introductions.

Preserves divergence explicitly: Phase 1 still mandatory on vague
requests, detail-dive is a legitimate narrowing step within divergence.
The principle only activates AFTER focus has landed on one candidate.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(specialist-manager): tighten convergence — single anchor, comparison case, soften exclusive framing

Post-review fixes on the convergence rewrite:

- Variant `Ready to hire X, or look at others?` now named exactly once
  (in the principle section). Turn 3+ and anti-pattern entries reference
  the principle by name instead of re-quoting the variant, avoiding
  anchor-bias to one phrasing.
- Added explicit bullet for multi-candidate comparison in Turn 3+:
  comparison stays in menu mode, no card. Previous rule only covered
  detail-dive on ONE candidate.
- Softened "next agent message IS the card" → "ends with the card" so
  the informational prose summary + card in one message (already
  allowed by Turn 3+) isn't read as disallowed by the principle.
- Made the "detail-dive → card" default heuristic explicit and its
  pivot cost (user clicks cancel, which is cheap) — resolves the
  subtle tension between "detail-dive is within divergence" and
  "detail-dive triggers convergence".

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(specialist-manager): refocus description — concierge role + latent-need trigger

Old description led with verb list (discover/browse/hire/fire) and only
covered explicit asks ("find me an agent", "hire code_dev"). This missed
the skill's core value: it's the user's concierge for the Specialist
roster — the one the LLM should consult when the user describes a task
an official Specialist could handle, even without naming agents.

New description:
- Frames role as "all-round guide and living directory" (concierge + roster expert)
- Splits triggers into (a) explicit asks and (b) latent need — the user describes
  a task ("analyze competitors", "write a viral ad script") without asking for an agent
- Adds directive for calling agents: surface candidates BEFORE attempting the task

Swapped embedded colon for em-dash to avoid YAML scalar parse error on
bare "(b) latent need:" pattern.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(specialist-manager): semantic info strings + post-hire chat link card

Frontend-contract changes (requires frontend team to add new parsers):

Consent card renamed from one generic info string to two direction-specific ones:
- zooclaw-action-confirm          →  (split)
- zooclaw-hire-specialist-consent — hire consent (neutral styling)
- zooclaw-fire-specialist-consent — fire consent (destructive styling)

"confirm" described the button; "consent" now describes the card semantic.
"action" was too generic; "hire-specialist" / "fire-specialist" are specific
to the domain. Frontend can now dispatch on info string alone instead of
parsing the body to decide between hire/fire styling.

New card: zooclaw-open-specialist-chat
- Emitted after successful hire (HTTP 200 OR idempotent already_hired)
- NOT emitted on fire or hire failure
- Body: single markdown link to https://zooclaw.ai/chat?agent_id=<id>
- No locale segment — frontend handles locale routing

Outcome flow on hire success is now three parts in order:
  1. outcome sentence
  2. chat-link card (primary CTA)
  3. refresh hint (secondary recovery note)

Updates throughout:
- Consent contract section: introduces the two info strings up front
  with a routing table
- Worked examples (Phase 2, Chinese Phase 1→2): updated info strings
  and full three-part outcome illustration
- Confirmation workflow step 4: three-part outcome spec with chat-link
  rule; already_hired includes the link, not_hired on fire does not
- Anti-patterns: 4 new rules (info-string mismatch, missing chat link,
  chat link on fire, wrong URL shape); existing patterns updated to
  "consent card" generic or specific info string as context requires
- Notes for maintainers: new "Frontend rendering contract" table
  covering all three info strings with migration note on legacy
  zooclaw-action-confirm parser (keep during rollout, remove after all
  deploys switch)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(specialist-manager): drop legacy zooclaw-action-confirm fallback window

Frontend and skill deploy together — no transition period. Rewrite the
migration note to state that zooclaw-action-confirm is no longer a
recognized info string and must not be emitted, rather than prescribing
a rollout-window compatibility parser.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(specialist-manager): drop migration note

Historical context isn't load-bearing for the skill's current behavior;
removing the legacy zooclaw-action-confirm paragraph.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(specialist-manager): SSOT consolidation + @agent_id info-string pattern

Refactor per Candidate-B (Single Source of Truth): each rule lives in
exactly one section; other mentions become 1-line cross-references.
Eliminates ~18 rule-duplicates across the document.

Biggest consolidations:
- Chat-link MUST/MUST-NOT/placement:  7 places -> 1 (Post-hire section)
- Info string selection (hire/fire):  4 places -> 1 (Consent card format table)
- Convergence prose-pre-ask:          4 places -> 1 (Convergence discipline + 1 anti-pattern index)
- Language matching:                  3 places -> 1 (Language rule section)
- Image prohibition in card body:     3 places -> 1 (body-table avatar row)
- Refresh hint:                       3 places -> 1 (Confirmation step 4)
- Consent-required before CLI:        5 places -> 1 (Consent contract intro)

Info string pattern change: each card's info string now appends agent_id
after '@' separator, letting frontend dispatch on info string alone
without parsing the body:
- zooclaw-hire-specialist-consent@<agent_id>
- zooclaw-fire-specialist-consent@<agent_id>
- zooclaw-open-specialist-chat@<agent_id>

Example: zooclaw-open-specialist-chat@design_researcher

Anti-patterns section trimmed from 19 bullets to 8 (only LLM-easy-error
traps + backend-contract gotchas; rules already in main workflow removed).

Frontend rendering contract table in Notes for maintainers removed — the
authoritative spec is in the "The confirmation card format" table and
the "Post-hire chat link card" section.

Verification: 55-item preservation checklist in docs/ (gitignored working
doc) — all items verified preserved; 0 regressions.

Line count: 442 -> 412 (-30 lines). Linter: pass.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(specialist-manager): root-cause convergence rewrite — card IS the polite ask

Previous approach was symptom-patching — enumerating variants like
"Ready to hire X, or look at others?" as forbidden phrasings. The LLM
defaults to polite option-offering in prose; listing variants is
whack-a-mole as new variants emerge.

Root cause: the LLM treats the consent card as a structured artifact
that follows a prose invitation, not as the invitation itself. Its
general-purpose conversational scaffold says "present info → invite
action → wait for reply", and it inserts the prose invitation before
the card, producing the two-turn confirmation redundancy.

Root-cause rewrite addresses the LLM's mental model, not the prose:

1. Reframe politeness: "the card IS the polite ask. Its Confirm / Cancel
   buttons already perform the 'do you want this?' question. Prose that
   also asks is double-politeness — costs the user an extra turn."

2. Explicit message-shape template:
     <prose content>
     <consent card — ends the message>
   "Nothing between the last prose paragraph and the card, nothing after
   the card in the same message." LLM doesn't need to judge variants —
   just renders the template.

3. Concrete ❌/✅ side-by-side example pinning the failure mode shape.
   Market Analyst case from the observed regression shown inline. LLMs
   pattern-match against side-by-side negatives strongly; pure rules
   alone are weaker.

Turn 3+ detail-dive bullet and anti-pattern A1 simplified to point to
Convergence discipline's example — no more variant enumeration at
multiple locations.

Line count: 412 -> 444 (+32, root-cause teaching justifies).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(specialist-manager): chat-link card body is URL-only; leading prose outside the card

The chat-link card body previously contained markdown link syntax
[anchor](url), which plain-text readers can't render as a clickable
link — they see literal "[Start chatting with X](https://...)" markup.
This mirrored the same problem the skill already prohibits for
consent cards (no images / no markdown image syntax inside card body).

Fix: apply the same principle to the chat-link card.
- Card body: one line, the URL and nothing else.
- "Start chatting with X" guidance: normal prose OUTSIDE the card,
  right before it (with a trailing colon handing off to the card).

Card format section renamed "Anchor-text format" -> "Leading prose
(outside the card)" with the same multi-language translation examples.

Worked examples (English Phase 2-only + Chinese Phase 1→2) updated to
show outcome sentence + leading prose + URL-only card.

Rationale in one line: plain-text readers get a clickable / copyable
URL; rendered clients get a styled card; both readable.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(specialist-manager): trim 77 lines via 5 consolidations (449->372)

All within Option A scope — no rule removed, only duplication/verbosity cut:

1. Delete "Worked example (Phase 2 only)" section — the Chinese Phase 1→2
   worked example is a superset; specific-request shortcut is already
   documented in Recommended workflow's "Skip Phase 1 when..." line.
   Fire info-string + "no chat-link after fire" note absorbed into the
   fire subcommand section. (-38 lines)

2. Compress Convergence discipline's ❌/✅ example from multi-line
   blockquoted dialog to single-paragraph summaries. Keeps the teaching
   shape (bad/good pair) but much tighter. (-15 lines)

3. Merge Post-hire "When it appears" table + "Never before/instead of"
   + "Placement" into a single tighter subsection "When it appears, and
   where in the message". (-8 lines)

4. Compress Prerequisites topology-priority paragraph from 7 lines to
   1 multi-clause line. Same content, tighter prose. (-6 lines)

5. Inline subcommand output shapes (list-catalog, my-team) instead of
   separate code blocks. (-10 lines)

Net: 449 -> 372 lines (-77, -17%). All 55 preserved-rule checklist items
still verified; Convergence root-cause teaching (❌/✅) still present.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: shcjveg <42231536+shcjveg@users.noreply.github.com>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #175: docs(specialist-manager): elevate convergence to three-in-one principle

## Summary

- Rewrite **Convergence discipline** (formerly "Convergence-before-card discipline") as a unified principle: the `zooclaw-action-confirm` card IS the agent's commit-question — convergence, ask, and commit collapse into one artifact. Don't split them.
- Name the disguised-balanced-close variant explicitly (`Ready to hire X, or look at others?`) so LLM generalization catches it, not just the literal `Want to hire X?`.
- Scope Turn 2's balanced two-option close to **shortlist/menu mode only** — once focus narrows to one candidate, menu mode ends and Convergence takes over.
- Turn 3+ detail-dive bullet now references the principle by name (no rule repetition) and adds lead-avatar guidance (image + text agent introduction).

## Why

The prior phrasing ("card too late / redundant") only flagged the literal "want to hire X?" variant. Screenshot regression showed the agent using a balanced-looking close (`Ready to hire X, or look at others?`) post-detail-dive — disguised as two options, still a redundant turn. Patching specific phrasings doesn't generalize; elevating the underlying principle (card = convergence + ask + commit, three-in-one) does.

Divergence is preserved explicitly: Phase 1 still mandatory on vague requests, detail-dive remains a legitimate narrowing step. The principle only activates AFTER focus has landed on one candidate.

## Test plan

- [ ] Linter passes (`python3 .github/scripts/lint_skills.py` — confirmed locally)
- [ ] Staging deploy via tag `v0.5.31-beta.2` after merge
- [ ] Manual chat test: vague request → shortlist (balanced close) → detail-dive → card (no prose pre-ask)
- [ ] Manual chat test: specific request (`hire code_dev`) → card directly (Phase 2 only)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## c2d157e

**作者**: vincent-srp
**日期**: 2026-04-22T06:06:58Z
**链接**: [https://github.com/SerendipityOneInc/ecap-skills/commit/c2d157efef1969217c05fffab3db8a2761c8cb85](https://github.com/SerendipityOneInc/ecap-skills/commit/c2d157efef1969217c05fffab3db8a2761c8cb85)

### Commit Message
```
docs(specialist-manager): principle-led slim pass (1 example per point) (#174)

* refactor: migrate claw-interface URL to CLAW_INTERFACE_URL / NANGO_GATEWAY_URL topology fallback

Replaces the old `CLAW_API_BASE_URL` env name + hardcoded cluster-internal
DNS default with two platform-injected env vars read in priority order:

  1. CLAW_INTERFACE_URL  — direct URL to claw-interface (normal case)
  2. NANGO_GATEWAY_URL   — gateway fallback (traffic routes through Nango)

Only one is expected to be set per environment; the script tolerates
whichever is injected. Neither goes in requires.env (platform's flat
pre-check can't model one-of); script validates "at least one is set"
at startup instead (exit 1 on config_missing).

This is a TOPOLOGY PRIORITY — not a canonical-name alias. The two URLs
point to different physical paths, and the ordering encodes a deliberate
deployment preference. Implemented with a `_resolve_claw_url()` helper
+ explanatory comment, NOT a bare `os.getenv("A") or os.getenv("B")`
one-liner (which CLAUDE.md §1 forbids as a semantic alias).

Changes:

- specialist-manager/scripts/specialist_manager.py:
  * Replace module-level CLAW_API_BASE default with `_resolve_claw_url()`
    helper that iterates the two env vars.
  * Add startup validation in main(): empty URL → exit 1 with
    `config_missing` error naming both env vars.

- specialist-manager/SKILL.md:
  * Prerequisites: rewrite CLAW_API_BASE_URL entry as the two-env
    topology-priority section; bash env-check snippet updated to check
    "at least one of".
  * How to run: TLS note now references HTTPS for NANGO_GATEWAY_URL /
    non-cluster-internal CLAW_INTERFACE_URL cases.
  * Error-handling table: new `config_missing` row for missing URLs;
    URLError row reworded to reference both env vars.
  * Anti-patterns: "staging vs production" item no longer claims a
    hardcoded cluster-internal DNS does the switching.

- .claude/skills/zooclaw-skill-conventions/SKILL.md (convention updates
  so future skills and VERIFY-mode audits follow suit):
  * C1: replace CLAW_API_BASE_URL entry with the two-env topology-
    priority block, including the distinction from "alias fallback".
  * C4 platform-injected list: swap CLAW_API_BASE_URL for the new pair.
  * C5 example: replace the CLAW-specific snippet with a generic
    EXAMPLE_ENDPOINT_URL sample, and note that C1 is a topology-priority
    exception (NOT this env-with-default pattern).
  * Step C3A constraint block (Chinese): C1 rule rewritten to reference
    the new env var pair and validation pattern.
  * Step V2 first-party-skill detection: update env-var hint.
  * Step V3 C1 checklist: update example env-var list.

Verified: `python3 .github/scripts/lint_skills.py` exit 0 (13 pre-existing
warnings, no new issues).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(specialist-manager): principle-led slim pass — 1 example per point, compact Convergence

Re-structure SKILL.md around the rule "abstract principle leads; at most
one example per guidance point". Keeps all runtime-effecting rules
(Language rule, Reply interpretation, Subcommands, Error-handling table,
frontmatter, env-check snippet) untouched.

Example-count cuts:
- "When to use" bullets: 3 trigger phrases per bullet → 1.
- "Explicit reply instructions" row: 2 language examples + 1 forbidden
  → 1 example + tightened prose on forbidden wrappers.
- Phase 1 Turn-2 close: 3 phrasings (zh + en × 2) → 1 good close.
- Worked examples: deleted the "fire single-turn" variant (identical
  shape to "hire single-turn" with verb swap) — replaced with a 1-line
  pointer. Kept the full-arc multi-turn Chinese example.
- Anti-pattern on `[…]` tokens: 2 positive + 1 forbidden example → a
  single compact prose rule.
- Notes for maintainers: removed the cross-repo API-spec reference
  (readers in this repo can't navigate to it; it was orientation noise).

Structural consolidation (principle vs procedure):
- Convergence-before-card discipline: 20 lines → 7 lines. Kept the pure
  principle (card = commit point) + two failure modes + pending-
  confirmation discipline. Moved the "Phase 1 / Phase 2 mechanics" and
  "when to skip Phase 1" lists out to the Recommended workflow section.
- Recommended workflow: opened with a 6-line Phase 1/2 orientation +
  explicit "skip Phase 1 when …" line — so the procedural rules live
  in one place instead of being split across two sections.

Net: 355 → 334 lines (-6%). Every cut was either pure redundancy or
multi-language / multi-phrasing sprawl; no runtime behavior should
change. Verified lint still exit 0.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(specialist-manager): dedupe principles + add diverge-converge + internal-discipline + image-with-intro

Three groups of changes, stacked onto the principle-led slim pass:

1) Dedupe (6 spots) — principles were restated across sections:
   - "Match on user intent" — cut body duplicate; description field is authoritative.
   - "Notes on this multi-turn flow" block — cut 4 lines; each bullet
     restated Convergence / Language / Reply-interpretation rules
     already stated upstream.
   - "This is Phase 2. It's reached either after Phase 1 has converged…"
     — duplicates the Skip Phase 1 line in Recommended workflow intro.
   - Turn 3+ "End the turn with the card" 4-line explanation — compressed
     to a 1-line pointer (detail-dive IS convergence; prose-ask anti-pattern).
   - Anti-patterns card-too-early + card-too-late (two 3-4 line bullets)
     — compressed to one pointer that defers to Convergence discipline.
   - Vocabulary discipline — 5 softened-verb examples → 1 ("add to your
     team" as canonical example).

2) New explicit principles in Recommended workflow intro:
   - **Diverge first, then converge** — the Phase 1/Phase 2 structure
     now has the underlying principle stated plainly: broaden options
     before committing; don't skip divergence on vague asks; don't stall
     in divergence after the user has picked.
   - **Internal discipline, don't narrate** — all rules in this skill
     are the agent's mental technique; embody them silently in action.
     Don't explain "I'm in Phase 1" / "applying the convergence rule"
     etc. to the user. The user gets a natural conversation, not a
     process tour.

3) Image-with-intro requirement — explicit upgrade from permissive to
   positive:
   - Avatar row in "How to write the body" table: "optional" →
     "required when catalog provides `avatar_url`". Introduce Specialists
     with image + text whenever the catalog has an avatar URL; pure-text
     rows feel abstract.
   - Turn 2 shortlist bullet: each candidate row now starts with the
     avatar image from the catalog (if available), then emoji + name +
     pitch + fit line.

Line count: 334 → 329 (-5 lines net; deduplication offset by the two
new principle sections and the image requirement).

Verified lint exit 0, no runtime-rule changes.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: shcjveg <42231536+shcjveg@users.noreply.github.com>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #174: docs(specialist-manager): principle-led slim pass (1 example per point)

## Summary

Slim pass on `specialist-manager/SKILL.md` guided by two rules:
1. **Abstract principle leads**; procedural detail follows.
2. **At most one example per guidance point** — trust the LLM to generalize.

**Net diff**: 355 → 334 lines (−6%), 1 file changed, +22 / −43. Every cut is either pure redundancy or multi-language / multi-phrasing sprawl. No runtime-effecting rules were touched (Language rule, Reply interpretation, Subcommands specs, Error-handling table, frontmatter, Prerequisites env-check snippet).

### What was cut

| Location | Before | After |
|---|---|---|
| "When to use" bullets | 3 trigger phrases per bullet | 1 per bullet |
| "Explicit reply instructions" row | 2 language examples + 1 forbidden | 1 example + prose rule |
| Phase 1 Turn-2 close | 3 phrasings | 1 |
| Worked examples | 3 (hire-specific + fire-specific + multi-turn zh) | 2 + a 1-line verb-swap pointer (fire-specific cut) |
| Anti-pattern on `[…]` tokens | 2 positive + 1 forbidden example | compact prose rule |
| Notes for maintainers | cross-repo API spec reference | removed (unreachable from this repo) |
| Convergence-before-card discipline | 20 lines (principle + Phase 1/2 mechanics + skip-Phase-1 list + pending discipline) | 7 lines (pure principle + failure modes + pending discipline) |
| Recommended workflow | mechanics scattered | opens with Phase 1/2 orientation + explicit "skip Phase 1 when…" |

### What stayed

All runtime-behavior rules: Language rule (default English), Reply interpretation (button tokens + natural-language intents in any language), `[…]` bracket format, Subcommand output shapes, Error-handling table, Prerequisites env-check, `my team` refresh hint. Cuts only touched the *documentation* around these rules, never the rules themselves.

Stacks on #173 (CLAW_INTERFACE_URL migration). If #173 merges first, this rebases cleanly onto main; if this merges first, #173 needs a trivial rebase.

## Test plan

- [ ] CI lint: `python3 .github/scripts/lint_skills.py` exit 0 (verified locally)
- [ ] Post-merge, staging deploy — verify in a real chat session:
  - [ ] Vague request still triggers Phase 1 shortlist (no card first-turn)
  - [ ] User naming a Specialist up-front still triggers single-turn card
  - [ ] Chinese conversation still gets `[确认] / [取消]` in card body
  - [ ] `my team` refresh hint still appears after hire/fire
  - [ ] Anti-patterns still fire correctly (LLM spots convergence violations)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---


## 2026-04-22


共 4 个 commits

## docs(specialist-manager): [...] bracket tokens + 'my team' refresh hint clarity (#172)

- **SHA**: [7d3780b8](https://github.com/SerendipityOneInc/ecap-skills/commit/7d3780b8a5a030ff5b16fd9db5acac49e6286b73)
- **作者**: vincent-srp
- **时间**: 2026-04-21T12:44:59Z
- **PR**: [#172](https://github.com/SerendipityOneInc/ecap-skills/pull/172)

### Commit Message

docs(specialist-manager): [...] bracket tokens + 'my team' refresh hint clarity (#172)

* docs(specialist-manager): require [...] bracket format for action tokens in card body

Frontend action-button rendering relies on bracket-wrapped tokens (`[confirm]`,
`[cancel]`, `[确认]`, `[取消]`) to parse the body's reply instructions as
interactive UI elements, not just italicized text. Previously the skill used
`""` (English) or `「」` (Chinese) which looked fine in markdown but didn't
round-trip cleanly through the frontend's button parser.

Changes:

- "How to write the body" reply-instructions row: format rule is now `[...]`
  wrapping, with the token inside following the user's conversation language
  (English `[confirm]/[cancel]`; Chinese `[确认]/[取消]`; etc.).
- All three worked examples updated to use `[...]`:
  - Phase 2 single-turn hire (English)
  - Single-turn fire (English)
  - Multi-turn Phase 1 → Phase 2 (Chinese)
- Multi-turn example's trailing note updated to reference `[确认] / [取消]`.
- Anti-pattern rewritten: forbids `""` / `「」` / backtick wrappers; requires
  `[...]` with native-language content inside; reminds that mixing English
  literals into a non-English body (even inside brackets) is still wrong.

Linter: exit 0 (unchanged).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(specialist-manager): refresh hint targets 'my team' not Specialists Hub + dedupe anti-pattern

Two issues in the refresh-hint wording:

1. The Hub catalog is the list of *available* Specialists; it doesn't change
   when you hire/fire. What changes is the user's *own* "my team" roster.
   The previous wording said "Frontend Specialist lists may be cached" which
   reads like it means the Hub catalog — that's the wrong target for the
   refresh hint and could confuse users into refreshing the wrong view.
2. The anti-patterns list had the same refresh-hint bullet duplicated
   verbatim on consecutive lines (a stray from an earlier edit).

Fixed:
- Confirmation step 4: "frontend Specialists list" → "'my team' roster";
  example phrasing in the hint also says "my team list" explicitly.
- note handling (already_hired / not_hired): "stale list" → "stale 'my team' list".
- Anti-pattern: removed the duplicate, rewrote the remaining one to call out
  "my team" roster specifically (NOT the Specialists Hub catalog; the hub
  doesn't change on hire/fire).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: shcjveg <42231536+shcjveg@users.noreply.github.com>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Description

## Summary

Two docs-only tweaks on top of v1.0, found during staging review:

1. **Action tokens in consent card body must be wrapped in `[…]`** (not `""` / `「」` / backticks). This is what the frontend's button parser recognizes to render `Confirm` / `Cancel` buttons. The token inside the brackets still follows the user's conversation language per the Language Rule — English `[confirm]/[cancel]`, Chinese `[确认]/[取消]`, etc. Default when no conversation signal exists: English.

2. **The post-action refresh hint targets the user's "my team" roster, NOT the Specialists Hub catalog.** The previous wording said "Frontend Specialists list may be cached" which reads like the hub catalog — wrong refresh target (the hub is the list of *available* Specialists and doesn't change on hire/fire; only "my team" does). Also eliminated a duplicate anti-pattern bullet left over from an earlier edit.

Both are doc-only changes in `specialist-manager/SKILL.md`.

## Test plan

- [ ] Next staging deploy (a `v*-beta` tag after this merges) — verify in a real chat session:
  - [ ] Card renders with `[confirm]` / `[cancel]` button styling via frontend parser (no raw quote chars)
  - [ ] Chinese conversation → card body shows `[确认] / [取消]`, not `[confirm] / [cancel]`
  - [ ] English default when user's conversation language is ambiguous
  - [ ] Outcome message after successful hire/fire includes a hint like "refresh your **my team** list" — not "Specialist list" / "hub"
- [ ] CI lint: `python3 .github/scripts/lint_skills.py` exit 0 (already verified locally)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat: specialist-manager v1.0 + project conventions router (#171)

- **SHA**: [5d664569](https://github.com/SerendipityOneInc/ecap-skills/commit/5d66456955e3299a11d47e180b1a5d3e2b421377)
- **作者**: vincent-srp
- **时间**: 2026-04-21T11:17:43Z
- **PR**: [#171](https://github.com/SerendipityOneInc/ecap-skills/pull/171)

### Commit Message

feat: specialist-manager v1.0 + project conventions router (#171)

* chore: ignore docs/ and .claude/

docs/ is a local-only working area for plans/specs/notes; not part
of the shared codebase. .claude/ is Claude Code session state.

Supersedes the previous docs/pm/ ignore with a broader docs/ rule.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* feat(skill-with-env): scaffold empty skill directory

Creates the two-file structure defined in the design spec:
- skill-with-env/SKILL.md (empty)
- skill-with-env/references/standards.md (empty)

Content is filled in subsequent commits.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* feat(skill-with-env): add distilled project standards reference

Captures the project-specific rules from CLAUDE.md §1-§5 into a
curated snapshot, plus project-unique rules (3-file env consistency,
websearch as reference implementation) that the generic skill-creator
would not otherwise know.

Each rule is paired with a Why line so downstream agents can apply
it with judgment, not rigid compliance.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor(skill-with-env): relocate to project-level .claude/skills/

skill-with-env is a project-internal tool (helps maintainers build
new skills with the right project constraints); it shouldn't be
published to S3 via PUBLISHED_SKILLS. Move it under
.claude/skills/skill-with-env/ so it's available only to people
working in this repo.

Companion .gitignore change narrows .claude/ ignore to just
settings.local.json so the skill files themselves are tracked.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* feat(skill-with-env): add routing workflow SKILL.md

Implements the three-step workflow from the design spec:
- Step 1: load references/standards.md, spot-check against CLAUDE.md
- Step 2: diagnose user's starting point (clear intent vs greenfield)
- Step 3A: route to skill-creator with project constraints injected
- Step 3B: route to skill-crafting with same constraints

Hard rules enforce: never author content directly, always run spot
check, always inject constraint block when routing, fail loudly on
missing dependencies.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor(skill-with-env): make self-contained via internal proxy-client-pattern

Previously standards.md §6 and SKILL.md Step 3A pointed at the repo's
websearch/ skill as a "live reference" for the proxy HTTP client
pattern. That created a cross-skill dependency that defeats the
design goal of skill-with-env being self-contained.

Extract the full pattern (helpers, CLI skeleton, rules, anti-patterns)
into references/proxy-client-pattern.md and re-point both documents
at it. skill-with-env now owns the authoritative pattern; consuming
skills inline-copy from it rather than reading another skill's source.

Files:
- NEW:  references/proxy-client-pattern.md (authoritative pattern)
- EDIT: references/standards.md §6 — points to internal file
- EDIT: SKILL.md Step 3A constraint block — same

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(claude-md): backfill Why lines + restructure §5-§6

Absorbs the refinements that previously lived only in
skill-with-env/references/standards.md. This makes CLAUDE.md the
single source of truth the repo has always wanted it to be.

Changes:
- §1-§4: add 'Why:' paragraphs alongside each rule
- §2: add explicit 'when this rule does NOT apply' for first-party
  backends (claw-interface), resolving the ambiguity recent usage
  surfaced
- §5: new — Env Consistency (runtime contract as hard rule +
  .env.example as conditional developer doc); replaces old §5 which
  forced .env.example on every skill regardless of whether any env
  var was user-configurable
- §6: new — Naming Conventions (kebab-case dir / snake_case module),
  previously implicit
- §1: document USER_INTERNAL_TOKEN in the canonical table; previously
  only mentioned in §2

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor(zooclaw-skill-conventions): rename + switch to live-reference architecture

Rename skill-with-env → zooclaw-skill-conventions. The old name
implied 'handles env'; the skill actually bridges project conventions
between CLAUDE.md and the generic skill-authoring tools.

Architecture change — delete references/standards.md and have the
skill read CLAUDE.md directly at runtime:

- Eliminates dual-source-of-truth problem (standards.md was a distilled
  copy that required manual resync after every CLAUDE.md edit, and
  Step 1 spot-check existed only to catch that drift).
- Constraint block passed to downstream skill-creator/skill-crafting
  now references CLAUDE.md by section number instead of inlining a
  prose snapshot. Rule evolution is zero-migration: next invocation
  sees the fresh source.
- Step 2 default bias strengthened to skill-creator; skill-crafting
  is now only for explicitly-exploratory requests.
- The CLAUDE.md §2 "when this rule does NOT apply" exception (for
  first-party backends like claw-interface) is surfaced in the
  constraint block so skill-creator doesn't mechanically enforce
  /search/proxy shape when it doesn't apply.

Files:
- git mv skill-with-env/ → zooclaw-skill-conventions/
- DEL  references/standards.md (absorbed into CLAUDE.md §1-§6)
- REWRITE SKILL.md (new name, live-reference workflow, creator default)

proxy-client-pattern.md kept as-is for this round. Round 2 will split
it into proxy-specific and first-party-backend variants.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(claude-md): add CLAW_API_BASE_URL to §1 canonical env vars

First-party zooclaw backend (claw-interface) needs a canonical env
var name. Adding CLAW_API_BASE_URL per the convention established
during skill-with-env v2 usage — separates 'third-party via proxy'
(ECAP_PROXY_BASE_URL) from 'first-party backend direct'
(CLAW_API_BASE_URL).

This makes the §2 'when this rule does NOT apply' exception
concrete: skills calling CLAW_API_BASE_URL don't route through
/search/proxy.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor(zooclaw-skill-conventions): split client pattern into ecap-proxy + claw-interface

The single 'proxy-client-pattern.md' forced skills hitting first-party
backends (claw-interface, Bearer JWT + /openclaw/*) to削足适履
most of the template. Split into two self-contained patterns:

- references/ecap-proxy-client.md (renamed from proxy-client-pattern.md)
  For calls to {ECAP_PROXY_BASE_URL}/search/proxy — third-party
  providers via the proxy layer. Keeps X-Proxy-Key / X-Litellm-Api-*
  headers.

- references/claw-interface-client.md (NEW)
  For calls to {CLAW_API_BASE_URL}/openclaw/* — first-party zooclaw
  backend. Bearer JWT only, GET/POST, idempotent hire/fire error
  handling (409/404 as success).

Both files open with the same 'How to tell which pattern you need'
decision table so the consuming skill-creator session picks the
right one instead of guessing.

SKILL.md constraint block updated to point at both patterns and
add a 'none of the above → copy shared structure only' fallback.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* feat(zooclaw-skill-conventions): add VERIFY mode for reverse-audit

Extends the skill with a second mode: when the user gives a path to
an existing skill + asks to check/audit/review it, run a rule-by-rule
compliance check against CLAUDE.md §1–§6 instead of routing to
skill-creator.

Design choices:
- Agent-driven (no script). Same rule-reading logic that CREATE mode
  uses, so the generator and the auditor can never diverge.
- Structured report format with ✅/❌/⚠️ per finding, including passes
  (not just failures) — a clean sweep is itself useful information.
- Optional fix-one-re-verify loop at the end; deliberately no batch
  editing to keep the evidence trail clean.
- Mode detection signals listed explicitly (path + verify verbs) so
  ambiguous cases can ask once instead of guessing.

Also updated:
- Frontmatter description now announces both modes and their triggers.
- Intro has a two-row mode table for quick orientation.
- C2/C3A/C3B step labels (previously 2/3A/3B) to free up the V* prefix
  for VERIFY-mode steps.
- Why-this-skill-exists footer corrected: two HTTP client patterns, not one.

SKILL.md is now 230 lines — over the original <200 goal but well
under skill-creator's <500 guideline. The verify-mode content earns
its weight.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(claude-md): add §5 third pattern (skill-bundled default with env override)

Some env vars (e.g. CLAW_API_BASE_URL for first-party-backend skills) are
neither platform-injected nor expected from the user — the skill itself
carries a sensible default and the env exists only as an override knob.
Hardcoding violates §1 (no canonical-name discipline, can't override
without editing source); listing as required forces a setting nobody
normally needs to set.

This commit:
- Relaxes §5.1 runtime contract: only os.getenv calls WITHOUT defaults
  count toward the requires.env set.
- Adds §5 "Skill-bundled default with env override" subsection: use
  os.getenv("CANONICAL_NAME", "<default>"), do NOT list in requires.env,
  do NOT list in .env.example, MUST document in SKILL.md Prerequisites
  as an optional override.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* feat(specialist-manager): add Specialists Hub catalog/team/hire/fire skill

Thin CLI wrapper over claw-interface's /openclaw/* endpoints so the
calling agent can recommend, inspect, hire, and fire ZooClaw Specialists
on behalf of the user. Five subcommands (list-catalog, my-team, detail,
hire, fire) backed by an inlined first-party HTTP client (Bearer JWT,
no X-Proxy-Key) per the claw-interface pattern.

Follows the new project conventions:
- Env: CLAW_API_BASE_URL via §5 "skill-bundled default with env override"
  (cluster-internal DNS as default, env only for local debug); only
  USER_INTERNAL_TOKEN appears in requires.env per §5.1.
- All-English SKILL.md per project default; runtime behavior (input
  recognition, reply language) adapts to user's conversation language.
- Consent contract uses zooclaw-action-confirm fenced block whose body
  is plain natural language — no JSON, no metadata. Frontend detects
  the fence tag for rich-card rendering with Confirm/Cancel buttons
  that send literal "confirm"/"cancel"; plain-text readers see the
  body as the prompt itself.
- One pending confirmation at a time (no metadata to disambiguate
  concurrent cards).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(gitignore): add full macOS ignore set + group existing entries

Previously only .DS_Store was ignored. macOS systems also produce
__MACOSX/ (zip metadata), ._* AppleDouble files (resource forks
written when copying to non-HFS+/APFS volumes), and several Spotlight/
Trash/FSEvents directories. Verified no existing tracked files match
these patterns before adding.

Also grouped existing entries by purpose (Python / Env / Build /
Workspaces / macOS) with section headers for readability — no
behavioral change for the original entries.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(specialist-manager): fix double-confirm + native-language tokens + refresh hint

Three UX issues observed in real chat transcripts, now corrected in SKILL.md:

1. Native-language reply tokens in non-English card bodies
   Before: Chinese card body could still say 回复"confirm"确认添加 — awkward
   code-switching. Now "How to write the body" requires native-language
   tokens (「确认」/「取消」, 「確認」/「キャンセル」, Confirmar/Cancelar, ...).
   Safe because both the frontend Confirm/Cancel buttons and the skill's
   Reply interpretation already accept native tokens AND English literals.

2. Redundant pre-ask round before the consent card
   Before: workflow ended prose with "want to hire X?", user agreed, then
   agent still emitted a consent card — same decision confirmed twice.
   Now "Recommending an agent" step 5 and "Hiring or firing" step 3
   require going straight to the card; the card body IS the question.
   Context prose goes above or inside the card, never as a trailing ask.

3. Post-action refresh hint
   Frontend Specialist lists may be cached, so a just-hired/fired
   Specialist might not appear/disappear immediately. Workflow step 5
   now requires an end-of-response hint in the user's language
   (with en/zh/ja example phrasings); added as anti-pattern too.

Also adds a Chinese worked example showing native-token body form,
and four new anti-patterns covering the above.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(specialist-manager): keep consent card text-only; avatar goes above it

Observed in real chat: when the previous rule told the LLM it MAY
include a markdown image at the top of the card body, the LLM did so,
and plain-text readers saw raw ![...](...) markup inside the confirm
box. The card's compact layout also doesn't have room for an image.

Fix: images are now forbidden inside the card body. If an avatar is
desired, put the markdown image in the prose above the card — it
renders as a normal inline message image, separate from the text-only
card.

- "How to write the body" avatar row: inverted from "include in body"
  to "never inside; put above the card".
- "What NOT to put in the body": added "no images / inline media".
- Anti-patterns: added explicit rule against ![...](...) inside cards.
- Chinese worked example: demonstrates the correct layout
  (avatar image → capability bullets → text-only confirm card).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(specialist-manager): restructure around Phase 1 (Selection) → Phase 2 (Confirmation)

Previous "go straight to card" rule (commit ddef571) over-corrected and
caused a regression: the agent now dumps the full shortlist AND a
confirmation card in the first reply to vague requests, skipping the
selection conversation the user actually needed. Convergence on a
specific (action, agent_id) was being conflated with "the agent has
done its research."

Holistic restructure of the workflow side around two distinct phases:

- Phase 1 (Selection): conversational, multi-turn, NO card. Shortlist
  2-3 candidates, invite narrowing, run detail() on the one being
  zeroed in on, let the user pick. The card does not appear here.
- Phase 2 (Confirmation): the card appears at exactly one moment —
  when the agent and user have converged on ONE specific Specialist.
  Body asks the commit question only.

Skip Phase 1 only when (a) the user named a specific Specialist from
the start, or (b) the catalog has exactly one strong match.

Other changes in this commit:

- Avatar rule relaxed: hard rule is only "not inside the card." Where
  outside (alongside a shortlist row, leading image for one specific
  Specialist, etc.) is the agent's call based on readability.
- New "Convergence-before-card discipline" subsection makes the
  card-as-commit-point principle explicit, with both failure modes
  (too early / too late) called out.
- Worked examples reorganized: "Phase 2 only" (user was specific),
  "fire after naming target", and a full multi-turn "Phase 1 → Phase 2"
  example showing the shortlist → user picks → card → outcome flow.
- Anti-patterns revised: replaced the over-aggressive "always go
  straight to card" with two distinct ones — "don't card on first
  reply to vague requests" and "don't pre-ask before the card once
  user has picked."
- Refresh hint, native-language tokens, language-matching, no-images-
  in-card, queue-don't-stack rules all preserved.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(specialist-manager): vocabulary discipline (hire/fire) + balanced two-option close

Two issues observed in real chat: (1) the agent closed Phase 1 with
"Want me to add them to your team?" — a single-option pushy prompt
that funneled only toward action, with no offer to dig into Specialist
details first; (2) the prose used "add" everywhere while the skill's
actual capability vocabulary is hire/fire, creating drift between
how the agent talks about the action and what the action actually is.

Changes:

- Phase 1 closer rule: must offer BOTH "dig into a specific Specialist"
  AND "commit to hiring one" — never single-option pushy ("Want me to
  hire X?" alone is forbidden as a close).
- New "Vocabulary discipline" rule: skill capability is hire/fire; do
  not soften with add/remove/release/加入/移除. Prose verb and card
  body verb must match.
- All worked examples and card body templates updated: "Add X to your
  team?" → "Hire X?", "Release X" → "Fire X", "加入团队" → "雇用",
  "回复「确认」加入" → "回复「确认」雇用", and the Phase 1 closer in
  the multi-turn example shows the balanced two-option pattern.
- fire subcommand title: "release a Specialist" → "fire (un-hire) a
  Specialist" for terminology consistency.

Also de-duplicated multi-language examples added in the previous round
(refresh hint en/zh/ja triplet, reply-instructions zh/ja/es/en table,
vocabulary verb enumeration). The LLM can translate one canonical
example to the user's language at runtime; multi-language tables in
the spec were noise.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(specialist-manager): tighten "card IS the hire question" rule (no prose pre-ask after detail-dive)

Observed: after a detail-dive on Design Researcher, agent closed the
turn with "Want to hire Design Researcher, or compare with another
candidate first?", user replied "hire", then agent emitted the card —
two consecutive consent prompts for the same decision.

The previous "balanced two-option close" rule was right for the
post-shortlist stage (multiple candidates still on the table) but
wrong for the post-detail stage (one candidate already in focus —
that's convergence). Asking "want to hire X?" in prose anywhere is
the same question as the card body; doing both is the redundant
double-confirm.

Sharpened the rule:

- Convergence section "card too late" bullet: "the card IS the 'do
  you want to hire X?' question" — emit it directly whenever your
  intent is to put one specific Specialist up for a hire decision.
  The cancel button preserves the user's escape hatch.
- Phase 1 Turn 3+ deep-dive: after detail() summary, end the turn
  WITH the card, not with another prose ask. Removed the prior
  "want to hire them, or compare?" closer that was the exact
  double-confirm we're trying to avoid.
- Anti-pattern: rephrased from "don't pre-ask before the card" to
  "don't ask 'want to hire X?' in prose at all — that question IS
  the card."

The shortlist stage closer ("dig into one or pick one to hire?")
remains correct because it's a multi-target / multi-direction prompt,
not a single-Specialist hire question.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor(specialist-manager): move from .claude/skills/ to project root

Repo convention for skill directories is project root (agent-influencer/,
bot-mailbox/, designer/, pptx/, etc. all live at top level). The initial
scaffold landed under .claude/skills/ which is out of step with every
other skill in this repo.

Pure rename; git preserves file history through the move.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(gitignore): re-add docs/ and .claude/settings.local.json

During the merge with origin/main, I followed upstream's removal of these
two entries. That was the wrong call — they're user-local artifacts
(personal docs/ workspace, Claude Code local settings) that should stay
ignored in this repo. Re-adding them under a new "Local-only" group.

The macOS ignore set and the existing section structure are preserved.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(specialist-manager): clear CI linter blocker ({baseDir} paths, no hardcoded .claude/skills/)

CI linter (.github/scripts/lint_skills.py) found one blocking error and
one warning on specialist-manager's SKILL.md:

- ERROR: `.claude/skills/zooclaw-skill-conventions/references/claw-interface-client.md`
  in the maintainer note is a hardcoded Claude-local path. Rewritten to
  reference the pattern by skill name ("the `zooclaw-skill-conventions`
  skill's `references/` directory") — survives if the skill is later
  relocated.
- WARN: script path examples (`python3 scripts/...`) without
  `{baseDir}`/path-resolution guidance. Added a "## Path Resolution Rule"
  section near the top and rewrote all 6 command examples to use
  `{baseDir}/scripts/specialist_manager.py`, matching the convention
  used by zooclaw-asr, ad-video-studio, humanizer, etc.

The remaining `.env.example` warning is intentional — both env vars
(`USER_INTERNAL_TOKEN` platform-injected, `CLAW_API_BASE_URL` with
built-in default) are covered by CLAUDE.md §5's "omit .env.example"
rule. The linter can't check that condition; the warning is acceptable.

Verified: linter exit 0 after this fix.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs: elevate {baseDir} path-resolution rule to CLAUDE.md §7 + propagate via conventions router

The {baseDir} script-path rule and the "no hardcoded .claude/skills/"
cross-skill reference rule were being rediscovered per skill (already
showed up as a warning/error in the CI linter for specialist-manager,
and would repeat for any new skill built under this project). They're
project-wide portability conventions — lift them into CLAUDE.md as the
source of truth and let zooclaw-skill-conventions propagate them.

CLAUDE.md changes:
- New §7 "Path Resolution in SKILL.md" covering both cases:
  (a) in-skill script paths → use {baseDir}/scripts/...; require a
      "## Path Resolution Rule" section near the top of SKILL.md.
  (b) cross-skill references → describe siblings by skill name +
      relative path; no hardcoded .claude/skills/... prefix (also
      explicitly called out as the CI linter's hard-fail pattern).

zooclaw-skill-conventions/SKILL.md changes (router propagates §7 to
both CREATE and VERIFY paths, consistent with how §1-§6 flow):
- Step 1 section list: add §7 entry.
- Step C3A injected constraint block: add §7 with specific rules
  (baseDir for scripts, skill-name for cross-refs, linter block).
- Step V3 VERIFY checklist: new §7 block that checks
  {baseDir}/scripts usage, "Path Resolution Rule" heading presence,
  absence of any .claude/skills/ substring, and recommends running
  lint_skills.py locally before calling a skill done.
- Step V4 report skeleton: "Checked against CLAUDE.md §1–§6" → §1–§7.

Verified: lint_skills.py exit 0 (same 13 pre-existing warnings,
none new, none for specialist-manager error).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor: move project-specific rules into zooclaw-skill-conventions skill

The previous direction spread project conventions across CLAUDE.md
(baseline + my additions) + the conventions skill (router that
referenced CLAUDE.md §N). That forked CLAUDE.md from origin/main and
created two places to maintain rules. User feedback: CLAUDE.md stays
on main; project-specific rules live in the conventions skill only;
keep only what's necessary, no redundant structural re-statement of
what skill-creator already knows.

Changes:

- CLAUDE.md: reverted to origin/main state (drops my §1 CLAW_API_BASE_URL
  addition, §5 conditional .env.example + env-with-default "third
  pattern", §6 Why-backfill, §7 path-resolution — all now live in the
  conventions skill instead).

- .gitignore: slimmed to main + 4 essentials only (._* AppleDouble,
  __MACOSX/, docs/, .claude/settings.local.json). Removed the verbose
  macOS section + section headers from the earlier iteration — user
  wanted just the common stuff.

- zooclaw-skill-conventions/SKILL.md: substantial restructure.
  - New top-level "Project Conventions" section with rules C1–C6
    inline (no longer references external CLAUDE.md §N). Each rule
    is scoped tight: only what skill-creator would otherwise miss.
  - C1: project-specific canonical envs (CLAW_API_BASE_URL,
    USER_INTERNAL_TOKEN). Default value is the env-agnostic
    cluster-internal DNS; env-specific external URLs are NOT
    documented as override examples.
  - C2: ecap-proxy exception for first-party backends.
  - C3: env consistency hard rule (requires.env ≡ os.getenv without
    default).
  - C4: .env.example conditional rule (overrides CLAUDE.md §5's
    "always required").
  - C5: skill-bundled default with env override (env-agnostic URL
    example).
  - C6: path resolution ({baseDir}, no .claude/skills/ — CI-enforced).
  - Step 1 reworded: "Internalize the Project Conventions above"
    (no longer "Load from CLAUDE.md").
  - Step C3A constraint block: passes C1–C6 summary + tells
    skill-creator to read {baseDir}/SKILL.md's Project Conventions
    section.
  - Step V3 checklist: now maps to C1–C6 (was §1–§7).
  - Step V4 report template: "Checked against CLAUDE.md baseline +
    project conventions C1–C6".
  - Hard Rules rewrite: no longer "never inline CLAUDE.md" — the
    opposite now; conventions ARE inline here, CLAUDE.md stays
    baseline.
  - "Why this skill exists" section removed (redundant; covered
    by the top overview).
  - HTTP template references updated: {baseDir}/references/... (was
    hardcoded .claude/skills/zooclaw-skill-conventions/references/).

- specialist-manager/SKILL.md:
  - Prerequisites: replaced `https://clawapi.ecap.gsmo.ai` env-specific
    override example with cluster-internal DNS framing; reference
    "project §5" updated to "the zooclaw-skill-conventions skill's
    C5" (aligns with new rule naming).
  - Error-handling table: same URL substitution; removed the
    misleading "point at an external env-specific URL" example.

Verified: lint_skills.py exit 0 (13 pre-existing warnings, no errors,
no new warnings).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore: add specialist-manager to PUBLISHED_SKILLS whitelist

Publishes v1.0 of the Specialists Hub skill to the clawhub distribution.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: shcjveg <42231536+shcjveg@users.noreply.github.com>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Description

## Summary

Two related workstreams shipped on this branch:

1. **Project conventions infrastructure** — `zooclaw-skill-conventions` skill that routes skill-authoring requests to `skill-creator` or `skill-crafting` with project rules injected, plus a VERIFY mode for reverse-auditing existing skills. CLAUDE.md extended with a new §5 "skill-bundled default with env override" pattern and §1 canonical env `CLAW_API_BASE_URL` for first-party-backend skills. HTTP client references split into `ecap-proxy-client.md` (third-party proxy) and `claw-interface-client.md` (first-party Bearer JWT).

2. **`specialist-manager` skill (v1.0)** — first concrete skill built under the new conventions. Wraps `claw-interface`'s `/openclaw/*` endpoints so an agent can recommend, inspect, hire, and fire ZooClaw Specialists on behalf of the user. Five subcommands (`list-catalog` / `my-team` / `detail` / `hire` / `fire`), inlined Bearer-JWT HTTP client, stdout-JSON/stderr-logs contract, consent-card UX via `zooclaw-action-confirm` fenced block.

Key UX design captured in the skill (iterated across 7 doc commits from real chat transcripts):
- **Phase 1 (Selection) → Phase 2 (Confirmation)** workflow — shortlist in prose, narrow via `detail()`, card appears only at convergence
- **Card = commit point**: the card body IS the "do you want to hire X?" question; no prose pre-ask
- Body is natural language in the user's conversation language, text-only (no JSON / metadata / images)
- Native-language reply tokens (`「确认」/「取消」` etc.), frontend buttons still send literal English internally, Reply interpretation accepts both
- Vocabulary discipline: use `hire` / `fire`, never softened to `add` / `remove`
- Post-action refresh hint (frontend Specialist list may be cached)

Also: `.gitignore` gained full macOS ignore set (`__MACOSX/`, `._*` AppleDouble, Spotlight/Trashes/FSEvents). `specialist-manager` moved from `.claude/skills/` to project root to match repo convention.

## Test plan

- [ ] Verify `specialist-manager` CLI works against live `claw-interface`:
  - [ ] `list-catalog` returns enabled official Specialists, sorted
  - [ ] `my-team` strips the hardcoded `main` entry
  - [ ] `detail --agent-id code_dev` returns catalog entry + usecases
  - [ ] `hire --agent-id <id>` succeeds on first call, returns `already_hired` on second (idempotent)
  - [ ] `fire --agent-id <id>` succeeds; `not_hired` treated as idempotent success
- [ ] Verify consent card UX in real chat:
  - [ ] Vague request → Phase 1 shortlist (no card), not card in first reply
  - [ ] User picks a candidate → card appears, body is natural language in user's language
  - [ ] `detail` dive on one Specialist → end-of-turn card directly (no "want to hire?" pre-ask)
  - [ ] Native-language reply tokens shown in card body for non-English users
  - [ ] Buttons send literal `confirm` / `cancel` and skill recognizes them
  - [ ] Post-action message includes refresh hint in user's language
- [ ] Verify §5 env-with-default pattern: skill runs in-cluster with no env override; runs outside cluster after `export CLAW_API_BASE_URL=...`
- [ ] Verify `zooclaw-skill-conventions` VERIFY mode flags `specialist-manager` as passing (it should, since the skill was built under the new conventions)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(pptx): shape-level CLI for incremental .pptx editing (#155)

- **SHA**: [0187d1d2](https://github.com/SerendipityOneInc/ecap-skills/commit/0187d1d26366eaf702d6094a21cc84231a8ef973)
- **作者**: sharplee-srp
- **时间**: 2026-04-21T06:31:11Z
- **PR**: [#155](https://github.com/SerendipityOneInc/ecap-skills/pull/155)

### Commit Message

feat(pptx): shape-level CLI for incremental .pptx editing (#155)

### PR Description

## Real-world A/B (2026-04-17) — OLD vs NEW, 50 ops

Real download: [W3C Digital Marketing Workshop, USF 2012 TV-election deck](https://www.w3.org/2015/digital-marketing-workshop/slides/usf-w3c-ppt.pptx) (774 KB / 19 slides / 60 shapes). Same 50-op plan run through both OLD (`unpack → Read slide XML → Edit → pack`) and NEW (shape-CLI) by independent executor agents for per-pipeline token isolation.

| | OLD | NEW | NEW/OLD |
|---|---:|---:|---:|
| Anthropic `total_tokens` | 255,765 | 63,092 | **0.247** (saves **75.3%**) |
| Wall time (Phase B, 40 ops) | 146.5 s | 5.66 s | 0.039 |
| `bytes_read` across 40 ops | 317 KB | — (shape-scoped) | — |
| NEW-only ops (history/revert/undelete/diff) | 0/10 NOT_SUPPORTED | 10/10 ✅ | — |

`after-old.pptx` vs `after-new.pptx` semantic diff: 5 slides differ on revert/undelete ops OLD cannot execute (expected), plus one `smart-quote → straight-quote` encoding difference from the `set_text` rewrite contract documented in this PR.

Artefacts on [`office_benchmark`](https://github.com/SerendipityOneInc/ecap-skills/tree/office_benchmark) branch:

- [`before.pptx`](../blob/office_benchmark/benchmark/pptx/experiments/real-world-2026-04-17/before.pptx) / [`after-old.pptx`](../blob/office_benchmark/benchmark/pptx/experiments/real-world-2026-04-17/after-old.pptx) / [`after-new.pptx`](../blob/office_benchmark/benchmark/pptx/experiments/real-world-2026-04-17/after-new.pptx) — openable binaries, all three validate
- [`ops-plan.json`](../blob/office_benchmark/benchmark/pptx/experiments/real-world-2026-04-17/ops-plan.json) — shared 50-op plan (40 OLD+NEW + 10 NEW-only)
- [`ab-old-log.jsonl`](../blob/office_benchmark/benchmark/pptx/experiments/real-world-2026-04-17/ab-old-log.jsonl) + [`ab-old-summary.json`](../blob/office_benchmark/benchmark/pptx/experiments/real-world-2026-04-17/ab-old-summary.json)
- [`ab-new-log.jsonl`](../blob/office_benchmark/benchmark/pptx/experiments/real-world-2026-04-17/ab-new-log.jsonl) + [`ab-new-summary.json`](../blob/office_benchmark/benchmark/pptx/experiments/real-world-2026-04-17/ab-new-summary.json)
- [Aggregate AB-REPORT](../blob/office_benchmark/benchmark/2026-04-17-real-world-ab.md) (methodology + cross-skill comparison + capability matrix)


---

## chameleon: default watermark false + 1080p reference video input (#154)

- **SHA**: [62990df5](https://github.com/SerendipityOneInc/ecap-skills/commit/62990df52f3a57a3468539c9b0bcb7e2f19092ee)
- **作者**: david-srp
- **时间**: 2026-04-21T02:44:03Z
- **PR**: [#154](https://github.com/SerendipityOneInc/ecap-skills/pull/154)

### Commit Message

chameleon: default watermark false + 1080p reference video input (#154)

* chameleon: slim runtime refs and routing

* chameleon: default watermark to false

* chameleon: clarify 1080p support by model

* chameleon: support 1080p reference video input

### PR Description

## Summary
- slim Chameleon runtime refs and make execution routing clearer
- move long official source docs into `_dev/` and split runtime prompt guidance into shorter focused reference files
- keep `chameleon_generate.py` and `asset_register.py` as the main execution surface, with clearer script / reference boundaries
- change default Chameleon generation watermark from true to false
- clarify model-specific `1080p` output support
- add compliant `1080p` reference video input support for Seedance 2.0 and Seedance 2.0 fast
- update KB, assets reference, and reference-video normalization pixel cap accordingly

## Commit scope in this PR
- `f5ada0d` chameleon: slim runtime refs and routing
- `fa98723` chameleon: default watermark to false
- `b4e38f6` chameleon: clarify 1080p support by model
- `ea77d5e` chameleon: support 1080p reference video input

## What changed
### 1. Skill structure cleanup
- significantly slim down `chameleon/SKILL.md`
- move long official tutorial / prompt source material into `_dev/`
- split runtime-facing prompt references into:
  - `prompt-guide-foundations.md`
  - `prompt-guide-text.md`
  - `prompt-guide-image.md`
  - `prompt-guide-video.md`

### 2. Execution flow cleanup
- keep generation and asset registration centered on `chameleon_generate.py` and `asset_register.py`
- make routing boundaries between skill docs, runtime refs, and scripts more explicit
- align roadmap / reference paths with the new structure

### 3. Default behavior adjustment
- change default watermark behavior to `false`

### 4. 1080p capability clarification and support
- clarify that `1080p` output support is model-specific
- add support guidance for compliant `1080p` reference video input
- update reference-video pixel cap to `2086876` (about `2206x946`)
- apply the reference-video input capability to both Seedance 2.0 and Seedance 2.0 fast
- sync docs and `chameleon_generate.py` auto-normalization threshold

## Validation
- staging verified via `v0.5.28-beta.4`
- acceptance passed in group review

## User-visible impact
- users get cleaner Chameleon runtime guidance and less noisy docs
- default output no longer carries watermark unless explicitly requested
- reference-video workflows now reflect the newer upstream 1080p input capability instead of stale 720p-only assumptions


---

## 2026-04-21


今日无更新

## 2026-04-20


今日无更新

## 2026-04-19

今日无更新

## 2026-04-18


今日无更新

## 2026-04-17

共 1 条 commits

## `58392420` feat: add VS Code devcontainer with openclaw-docker image (#148)
- **作者**: allenz-srp
- **时间**: 2026-04-16T06:34:48Z
- **链接**: [58392420](https://github.com/SerendipityOneInc/ecap-skills/commit/583924205bb20f7464bed43c2fb5ae9a3aa1a41a)

