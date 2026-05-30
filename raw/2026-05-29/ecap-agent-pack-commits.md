# ecap-agent-pack - 2026-05-29

## fc07868 - 2026-05-29
**Author**: vincent-srp
**SHA**: fc078685443eb0ca40d9c9412576405f3fb19981
**Date**: 2026-05-29T10:01:02Z

**Message**:
```
feat(agent-studio): author quick_commands in pack manifest (#153)

* feat(agent-studio): author quick_commands in pack manifest

Let Agent Studio declare card quick-commands in agent/agent-pack.yaml:
- scaffold.py + template seed an empty `quick_commands: []` slot
- Stage 3 + /studio open SOP (new references/quick-commands.md) covering
  selection (2-4, derived from the pack's own skills/commands), sentence-case
  English label + auto-translated label_cn, and canonical block YAML
- validate.py check_quick_commands: canonical-block-only parser using
  json.loads for double-quoted id/label/label_cn/prompt; kebab-unique ids;
  >4 warns (Web shows first 4); flow/nested/single-quoted forms fail
- single source: kept out of description.json (schema comment + test)
- regression tests under the skill tests/ dir

Bumps Studio 1.4.1 -> 1.4.2.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* feat(agent-studio): warn when a pack has no quick_commands slot

A wholly absent quick_commands field now produces a validate.py warning
(not a failure): the pack predates the feature and its Web card would show
no one-tap quick-action menu, so iteration reliably surfaces it. An explicit
`quick_commands: []` remains the clean opt-out and passes silently — so new
scaffolds (which seed `[]`) and deliberate "no buttons" packs stay quiet.
Updates references/testing.md, references/quick-commands.md, and tests.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): validate.py refuses non-workspace layouts

Pointed at a published archive (identity files at root, skills under
.agents/skills/), validate.py previously passed the manifest check via
find_pack_manifest's root fallback but false-failed every agent/-path check
(structure, agent_completeness, listing_assets). Add a check_workspace_layout
pre-check: when agent/agent-pack.yaml is absent, return one clear, actionable
error (restore via snapshot.py / point at the workspace root) and short-circuit
instead of emitting the misleading cascade. Adds layout regression tests; notes
the workspace requirement in references/testing.md.

* docs(agent-studio): ground quick_commands in four pillars incl. commands

Refine the quick_commands authoring SOP so generated commands are (1) phrased
in the user's voice for real scenarios, (2) traceable to the pack's own
definition, and (3) sized by value rather than padded:

- Sources are four pillars — goal, persona, skills, and commands (the
  agent/AGENTS.md Commands table, the most direct source: each user-facing
  slash command is a prime one-tap candidate).
- Add a command->user-voice translation pattern (good/bad contrast) and a
  per-entry self-check (source / voice / standalone+safe / lifecycle value /
  distinct).
- Selection judges value across the pack's whole lifecycle (setup, daily,
  maintenance, troubleshooting), not raw frequency — quick_commands are a
  durable menu, not a quick start; operational/maintenance actions are
  eligible. Only bare destructive one-taps (must confirm first) and
  context-missing actions are excluded.
- Stage 3 gate lists each quick_command next to the command/skill/goal it
  derives from so the creator can confirm it is grounded, not invented.

SOP-only (references/quick-commands.md + automation.md); no validate/scaffold
change. All 86 tests pass.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(agent-studio): trim quick_commands SOP redundancy

Tighten quick-commands.md: drop the misleading `/studio install` example
(that is Studio's own command, not a built pack's), fold the duplicate
example_prompts/distinct check into one line, and shorten the example
commentary. No rule changes.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): address quick_commands review (fail-open + false-fails)

Resolve felix-srp's CHANGES_REQUESTED on validate.py's canonical-block parser:

- Blocking: require >=1 space after the colon on both field and id lines
  (`\s*` -> `\s+`). `label:"Hi"` / `id:x` are not YAML mappings — PyYAML
  raises on them, so accepting them green-lit a manifest the resolver drops.
- Allow a trailing `# comment` after a quoted value via JSONDecoder.raw_decode
  (mirrors PyYAML), while keeping `#` literal inside the quotes.
- Resolve quoted / comment-trailed `id` the way PyYAML does before the
  kebab check, removing the false-fail.
- check_workspace_layout: .exists() -> .is_file() so a directory at the
  manifest path fails the gate cleanly.
- Emit the structural block guidance once instead of per offending line.
- check_structure: drop the now-dead legacy-root branch + stale comment
  (the workspace gate already guarantees agent/agent-pack.yaml); leave the
  shared find_pack_manifest fallback intact for archive-layout callers.
- Add regression tests: missing-space (field+id) fail, inline comment pass,
  quoted/commented id pass, wrong-indent reports structural issue once.
- Docs: apply review's token-trim suggestions across SKILL.md, quick-commands,
  testing, automation, packaging (redundancy removal; all rules preserved).

Full suite: 90 passed.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: vincent-srp <180138700+vincent-srp@users.noreply.github.com>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR #153 Body**:
## Summary
Lets **Agent Studio** declare card **quick_commands** in a pack's `agent/agent-pack.yaml`, closing the producer-side gap so the field can flow `pack → resolver → prefill` (resolver side tracked separately in `zooclaw-agent-admin`).

- **Slot**: `scaffold.py` + `agent-pack.yaml.tmpl` seed an empty `quick_commands: []` with a pointer to the new reference doc.
- **SOP** (new `references/quick-commands.md` + wiring in `SKILL.md` Stage 3 / `/studio open` / `automation.md` / `packaging.md` / `testing.md`): select 2–4 actions derived from the pack's own skills/commands, sentence-case English `label` with an auto-translated `label_cn` (confirm only the primary language), canonical block YAML, distinct from `commands`/`example_prompts`.
- **Validation** (`validate.py` `check_quick_commands`): canonical-block-only parser using `json.loads` for double-quoted `id`/`label`/`label_cn`/`prompt`; kebab-unique ids; `>4` warns (Web shows first 4); flow / nested / single-quoted / dangling forms **fail** (so a malformed action can't be silently dropped by the resolver).
- **Single source**: kept out of `description.json` (schema comment + regression test).
- Bumps Studio **1.4.1 → 1.4.2**.

## Test Plan
- [x] Full suite green: `uv run --python 3.12 --with pytest --with pyyaml -m pytest agent-studio/.agents/skills/agent-studio/tests/` → **82 passed** (13 new quick_commands tests + existing spec/share suites).
- [x] `validate.py`: accepts canonical + escaped specials (`\"`/`\\`/`#`/emoji/`\n`); fails flow-mapping/flow-sequence/dangling/nested/non-string/single-quoted; `>4` warns.
- [x] `scaffold.py` emits the `quick_commands: []` slot; `agent-pack.yaml.tmpl` matches.
- [x] `package.py` passes the field through to the archive-root `agent-pack.yaml`.
- [x] `generate_description.py` output excludes `quick_commands`.
- [x] Merged latest `main` (incl. #149/#151); no changes outside `agent-studio/`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fce445e - 2026-05-29
**Author**: vincent-srp
**SHA**: fce445e2ed0a17e094cbef43097512aa8ead3320
**Date**: 2026-05-29T06:33:11Z

**Message**:
```
feat(pptx-master): upgrade to 2.0.9 — gdoc-import (Google Docs/Sheets/Slides, no login) (#154)

Apply build/pptx-master-2.0.9.zip. Adds the gdoc-import skill (import public
Google Docs/Sheets/Slides via Google's export endpoints, no OAuth), version
bump 2.0.8 → 2.0.9, plus routing.yaml + description.json entries.

The build artifact's CHANGELOG had regressed to a v2.0.7 top (dropping v2.0.8,
no v2.0.9) and test_pack.py's docstring read 2.0.7; both corrected here so the
repo carries full release history and a proper v2.0.9 entry. Tests: 70/0 + 36/0.

Co-authored-by: vincent-srp <180138700+vincent-srp@users.noreply.github.com>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

**PR #154 Body**:
## Summary

Upgrades the `pptx-master` pack to **2.0.9** from `build/pptx-master-2.0.9.zip`.

### New feature — Google Import (`gdoc-import` skill)
- New skill `.agents/skills/gdoc-import/SKILL.md`: import public Google Docs / Sheets / Slides via Google's built-in export endpoints — no OAuth, no login. Auto-detects type from the URL, exports to the deck-optimal format, detects login-wall / permission failures (never fabricates), routes into narrative / data-viz / Path B template pipeline.
- `routing.yaml`: new `external_doc_import` section (detect regex, type→endpoint map, format options, multi-sheet handling, failure detection, red lines) + skill registry entry.
- `description.json`: "Google Import" feature + skill line.
- `agent-pack.yaml`: version `2.0.8 → 2.0.9`.
- Identity preserved: `name: pptx-master`, `display_name: PPT Master`, `agentPack_id: pptx-master`.

### Build-artifact fixes (surfaced by the diff check)
The zip's `CHANGELOG.md` had regressed to a v2.0.7 top — missing the v2.0.8 entry and lacking a v2.0.9 entry. Restored the exact **v2.0.8** entry and wrote a new **v2.0.9** entry. Also fixed `tests/test_pack.py` docstring `2.0.7 → 2.0.9`.

> ⚠️ The source zip still carries the stale CHANGELOG/docstring, so repo and zip are no longer byte-identical. Regenerate the artifact upstream so they reconverge.

## Test
- `python3 tests/test_pack.py` → **70 pass / 0 fail**
- `python3 tests/test_extra.py` → **36 pass / 0 fail**

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
