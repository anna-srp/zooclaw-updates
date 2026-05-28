# ecap-skills Commits - 2026-05-27

共 1 条 commits

---

## feat(docx): Pipeline D (read) + SKILL.md modernization (#206)

- **SHA**: [236ef78e](https://github.com/SerendipityOneInc/ecap-skills/commit/236ef78e18aa929edf79072b863818b09f4c7d80)
- **作者**: felix-srp
- **日期**: 2026-05-27T12:25:37Z
- **PR**: #206

### Commit Message

```
feat(docx): Pipeline D (read) + SKILL.md modernization (#206)

* feat(docx): add Pipeline D — read .docx as GFM markdown with images

New `docx_read.sh` wraps pandoc to deliver:
- GFM markdown to stdout (or --out <file>), tracked changes inlined
- embedded images extracted to a media dir (auto-temp, <out>.media, or --media-dir)
- stderr summary: paragraph/word/drawing/image/comment counts + media path
- drop warning when drawings > image refs (catches charts/shapes pandoc cannot
  render — silent loss is the main failure mode of a pure-pandoc read)

Mirrors Anthropic's docx skill read approach but adds a default-on image
extract (the read use case the user actually has), the lossage warning, and a
stderr contract callers can parse for the media path.

SKILL.md: bumps to four pipelines, adds Pipeline D section + Quick Reference
row + Pipeline Router branch.

env_check.sh: pandoc is now Pipeline-D-critical, not just preview-optional.

smoke_test.sh: asserts both markdown output and the stderr summary contract.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(docx): address review findings from claude + codex

- stderr summary now emits BEFORE stdout cat, so the `media:` line that tells
  callers where the images live is delivered even when downstream truncates
  stdout (e.g. `docx_read.sh foo.docx | head`). Cat now tolerates SIGPIPE.
- Track `PANDOC_OK` so a downstream SIGPIPE (rc≠0) doesn't nuke the temp
  media dir that already holds the extracted images.
- `mkdir -p "$MEDIA_DIR/media"` up front so the `media:` path always exists
  even on docs with no images (pandoc skips the subdir when nothing extracts).
- Auto-derived `${OUT%.md}.media` is now marked for failure-cleanup only when
  it didn't pre-exist — no surprise nuke of user-owned directories.
- `env_check.sh`: unzip warning calls out Pipeline D specifically.
- `smoke_test.sh`: skips Pipeline D (not fails) when unzip is absent; stale
  "three pipelines" header bumped to four.
- `SKILL.md` H1 mentions Read.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(docx): address codex round-2 minors

- `cat "$TMP_MD" || true` was masking real read errors. Differentiate: rc=141
  (SIGPIPE from downstream) is silenced; any other non-zero exit gets a clear
  error message and propagates. Removes the asymmetry vs the `--out` path.
- Stop eagerly creating `$MEDIA_DIR/media`. Only emit the `media:` stderr line
  when at least one image was actually extracted. Avoids littering empty
  `media/` subdirectories in caller-supplied `--media-dir` paths when the
  source doc has no images.
- SKILL.md + smoke_test.sh updated to match the conditional `media:` contract.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(docx): correct rc-capture pattern for cat under set -e

Codex + claude round 3 flagged the same blocker: the `if ! cat …; then rc=$?` pattern
captures rc=0 (the negation's exit code), not cat's. So the round-2 SIGPIPE
differentiation was wrong in both directions:
- legitimate SIGPIPE (`docx_read.sh foo.docx | head`) printed a spurious
  "Error: failed to emit markdown (cat rc=0)" on stderr (rc=0 ≠ 141 trips the
  guard) while exiting 0
- legitimate cat failures were silenced

The idiomatic `cat "$TMP_MD" || cat_rc=$?` correctly captures cat's exit
without tripping set -e. SIGPIPE (141) is silenced; everything else surfaces
loudly and exits with the underlying rc.

Also updated the script header comment to reflect the conditional `media:`
contract.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(docx): final trim on Pipeline D stderr description

Shorter wording for the stderr contract bullets while keeping all four
markers (read:/media:/warning:/note:) discoverable.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(docx): rewrite SKILL.md description — denser triggers, narrower scope

Compared against anthropic/skills and MiniMax-AI/skills docx descriptions.
Net -85 chars vs the pre-PR original (513 → 428) AND covers strictly more
routing signals:

Added:
- Word-specific feature triggers (TOC, headings, tracked changes, comments,
  embedded images, find-replace) — covers requests that name an operation
  without saying "docx" explicitly
- Negative scope ("NOT for PDFs, spreadsheets, Google Docs") — keeps the
  router from over-triggering this skill in a repo with sibling pdf/xlsx
  skills

Removed:
- 7-item doc-type list (reports/proposals/contracts/letters/resumes/manuals/
  SOPs) — already covered by the trigger phrases below it
- "Use whenever the deliverable is .docx/Word or the task references one" — verbose
- Redundant Chinese: "生成Word文档", redundant EN: "make a contract"
- "reformat to match this template" → "apply template" (matches Pipeline C name)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(readme): update docx row — Pipeline D + correct engines

Was: ".NET OpenXML SDK + Python XML editing, docx-js fallback" — but the
create pipeline is docx-js (Node.js), C# samples are reference material
only, and Pipeline D (read) is now present.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(docx): aggressive token trim across SKILL.md

Goal: reduce runtime token cost without sacrificing routing or instruction
fidelity. Net -644 bytes on SKILL.md while keeping every command, file
path, and rule intact. After this trim, the entire Pipeline D feature only
adds +258 bytes vs origin/main.

What changed:
- H1: "DOCX — Create, Edit, Read, and Format Word Documents" → "DOCX —
  Create, Edit, Read, Format" (DOCX already implies "Word Documents").
- Intro one-liner: drop the engine annotations — Quick Reference + Pipeline
  sections + Pipeline Router each cover engines downstream.
- Pipeline Router: drop the verbose "User task / Has input .docx, …"
  prefixes; the table form is denser and clearer.
- Setup heading: "First operation" → "Each session" (clearer intent).
- Pipeline A intro: collapse two sentences naming the same docs file set.
- Pipeline B: "Step 1/2/3" → "1./2./3."; smart-quotes table → inline; key
  files list strips redundant `word/` prefix.
- Pipeline C: tighten Overlay/Base-replace bullets.
- OpenXML reference intro: drop "how OpenXML elements work" filler.
- TOC critical rule: replace prose with the same info, half the chars.
- Validation Pipeline trailing paragraphs: collapsed.
- "Reference Loading Guide" → "Reference Loading".

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(docx): restore full paths in SKILL.md trims that lost addressability

Previous trim pass (fb3d4aa) over-shortened four spots, leaving an LLM
consumer with no addressable path. Restored:

- Pipeline A: `design_principles.md` and `cjk_typography.md` now carry their
  full `{baseDir}/references/` prefix again (the line had one full path and
  two bare names, ambiguous).
- Pipeline B "Key files" — restored `word/` prefix on styles.xml /
  numbering.xml / _rels/document.xml.rels, and made the unpack location
  explicit ("inside `unpacked/`").
- Pipeline B comments block — `xml_editing_guide.md` now has its
  `{baseDir}/references/` prefix again.
- Validation Pipeline trailing line — `fix_order.py` and `gate_check.py`
  references now include the full `uv run --with lxml python {baseDir}/...`
  invocation; the previous bare names weren't runnable.

Net SKILL.md is still -438 bytes vs pre-trim state.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(docx): declare runtime dependencies in metadata.openclaw.requires

Mirrors pptx/SKILL.md's `bins` / `pip` / `npm` schema so the OpenClaw runtime
provisions everything the skill needs without the user touching install
commands in SKILL.md.

Declared:
- bins: uv, node, pandoc (Pipeline D), unzip (Pipeline D), soffice (.doc
  conversion + PDF export)
- pip:  lxml, defusedxml (used by every office/*.py script)
- npm:  docx (Pipeline A engine)

Removed the now-redundant `Install: npm install -g docx` hint from the
Pipeline A intro — the npm dep is declared above.

`scripts/setup.sh` and `scripts/env_check.sh` remain useful as local-dev
install + per-session verification, untouched.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(docx): align metadata block with pptx schema (version/category/sources)

Adds the same top-level metadata fields pptx uses, keeping the skill
registry consistent across the repo:

- `version: "2.0"` — Pipeline D is a major addition.
- `category: "productivity"` — matches pptx.
- `sources` — upstream library references (docx-js, pandoc, OpenXML SDK).

Also normalized the compact JSON-in-YAML layout to match pptx's style.
Frontmatter parses cleanly; smoke 7/7.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(docx): drop redundant `sources` field from metadata

The sources list was external library URLs already discoverable from the
SKILL.md body (docx-js / pandoc / OpenXML mentions). Drop.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(docx): drop non-functional metadata fields (version/category/emoji)

Per OpenClaw docs (https://docs.openclaw.ai/tools/creating-skills), only
`name`, `description`, and `metadata.openclaw.requires.bins/config` are
documented as load-bearing. `version`, `category`, and `emoji` are display-
or registry-decoration only and aren't honored by the runtime.

Kept `pip` and `npm` under requires (also undocumented) to match pptx
convention so the repo stays internally consistent; pip/npm install is
handled by setup.sh today regardless.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(docx): drop setup.sh + env_check.sh — zooclaw pre-installs everything

These scripts existed for local-dev install + per-session verification, but
this skill runs on zooclaw (cloud OpenClaw) where:

- Binaries declared in `metadata.openclaw.requires.bins` are pre-provisioned
  by the runtime
- pip/npm deps in `metadata.openclaw.requires` likewise provisioned (or
  bundled into the skill image)
- Per-session env_check.sh adds no signal a failed Bash invocation wouldn't
  already surface
- pptx, the sibling skill we aligned with, doesn't ship either script

Net -547 lines. Removed the Setup section from SKILL.md as well; smoke_test
is the only remaining script and is unaffected (no dependency on either).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

> [!IMPORTANT]
> **Runtime dependency** — Pipeline D needs `pandoc` on the zooclaw image. Tracking PR: [openclaw-docker#109](https://github.com/SerendipityOneInc/openclaw-docker/pull/109). Merging this PR before that one will leave Pipeline D non-functional in zooclaw until the next image rebuild.

## Summary

Adds a fourth pipeline to the docx skill — **read** an existing `.docx` as LLM-friendly GFM markdown with embedded images extracted to disk — and modernizes SKILL.md alongside it (description rewrite, aggressive trim, metadata-declared deps, drop local setup scripts to align with the pptx convention).

Net diff: **+170 / −585 lines**.

### Pipeline D — Read

- New `docx/scripts/docx_read.sh` (~95 lines bash, `set -euo pipefail`).
- Pandoc wrapper: `pandoc -f docx -t gfm --track-changes=all --extract-media=…`.
- Stderr emitted **before** stdout so `… | head` consumers can't truncate the contract.
- Stderr keys: `read:` (always); `media:` (only when images extracted); `warning:` (drawings > image refs — pandoc dropped charts/shapes); `note:` (comments present — not inlined; use Pipeline B).
- `cat` differentiates SIGPIPE (rc=141, silenced) from real read failures.
- Auto media-dir resolution: tempdir by default, `<out>.media` next to `--out`, or explicit `--media-dir`. Failure cleanup only nukes dirs the script created itself.

```bash
bash docx/scripts/docx_read.sh doc.docx                                # md → stdout, images → tempdir
bash docx/scripts/docx_read.sh doc.docx --out out.md                   # md → out.md, images → out.media/media/
bash docx/scripts/docx_read.sh doc.docx --out out.md --media-dir dir   # explicit media dir
```

### SKILL.md modernization

- **Description rewrite** (compared against [anthropic/skills](https://github.com/anthropics/skills/blob/main/skills/docx/SKILL.md) and [MiniMax-AI/skills](https://github.com/MiniMax-AI/skills/blob/main/skills/minimax-docx/SKILL.md)): `description:` is 428 chars (−85 vs original) **and** broader coverage — adds Word-feature triggers (TOC, headings, tracked changes, comments, embedded images, find-replace) and explicit negative scope (`NOT for PDFs, spreadsheets, Google Docs`).
- **Body trim across H1 / one-liner / Pipeline Router / Pipeline A-C prose / Validation Pipeline / Reference Loading**. Net SKILL.md is *smaller* than `origin/main` despite adding the new Pipeline D section. Post-trim audit caught four over-shortened spots (bare filename refs that lost their `{baseDir}/…` prefix and one non-runnable bash shortening); all restored in `474d40b`.
- **Metadata declares runtime deps** — `metadata.openclaw.requires` now lists `bins`, `pip`, `npm` so the registry has the full dep picture (load-bearing only on `bins` per current OpenClaw docs; `pip`/`npm` mirror the pptx convention):
  ```yaml
  "openclaw": {
    "requires": {
      "bins": ["uv", "node", "pandoc", "unzip", "soffice"],
      "pip":  ["lxml", "defusedxml"],
      "npm":  ["docx"]
    }
  }
  ```
- **Dropped `setup.sh` (-374 lines) + `env_check.sh` (-169 lines)** — the skill runs on zooclaw, where the Dockerfile installs deps. pptx doesn't ship these either. The `## Setup` section in SKILL.md was removed accordingly.
- **Dropped `Install: npm install -g docx` body hint** — the npm dep is declared in metadata and the cloud image installs `docx` globally.

### Other

- `README.md` docx row updated: Pipeline D + corrected engine info (the row previously claimed `.NET OpenXML SDK + docx-js fallback`; actually docx-js is primary, C# is reference-only).
- `smoke_test.sh` — adds Pipeline D test (skips if pandoc or unzip missing), asserts both markdown body and the stderr `read:` summary; H1 comment bumped to "four pipelines".

## Review history (4 rounds)

Independent review by `pr-review-toolkit:code-reviewer` (Claude) and `codex:codex-rescue` (Codex). All findings landed:

- **Round 1** — GNU mktemp portability, `pipefail`+`unzip -p` of missing `comments.xml`, drawing-regex breadth, trap leaks temp media dir, smoke-test stderr coverage, replace full-archive unzip with streaming, env_check pandoc wording.
- **Round 2** — SIGPIPE truncating the stderr contract; `media:` path advertised when no images; H1 missing "Read"; auto-derived `${OUT%.md}.media` cleanup symmetry; unzip env/smoke inconsistency.
- **Round 3** — `cat … || true` swallowing real read errors; empty `media/` subdir litter in caller-supplied `--media-dir`.
- **Round 4** — `if ! cat …; then rc=$?` always captures rc=0 (the `!` itself is the last command). Replaced with canonical `cat … || cat_rc=$?` capture.

Final round (post-fix): both reviewers — **ship it.**

## Test plan

- [x] `bash docx/scripts/smoke_test.sh` — 7/7 passing
- [x] Real CJK + image docx — markdown + 2 PNGs extracted, no false drop warning
- [x] `docx_read.sh foo.docx | head` (SIGPIPE) — rc=0, stderr summary preserved, images preserved
- [x] No-image docx with `--media-dir` — no `media:` line, no empty `media/` litter
- [x] Corrupt zip — fails cleanly, tempdir cleaned up, no leak
- [x] Missing pandoc / missing unzip — clear hint, exit 3
- [x] Unknown flag / two positional inputs — usage, exit 2
- [x] SKILL.md frontmatter parses; every `{baseDir}/…` reference resolvable
- [ ] **After zooclaw image rebuild with [openclaw-docker#109](https://github.com/SerendipityOneInc/openclaw-docker/pull/109):** confirm Pipeline D runs end-to-end in a live pod

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

