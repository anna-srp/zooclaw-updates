---
title: "Agent Studio v1.4.0：规格驱动的构建流程上线"
type: "产品基础功能更新"
priority: "高"
date: "2026-05-27"
status: "待审核"
channels: ""
---

# Agent Studio v1.4.0：规格驱动的构建流程上线

## 核心宣传点

Agent Studio 现在支持上传需求规格文档来驱动 Agent 构建，并在发布前自动校验所有需求是否已被实现，让 Agent 构建过程更加规范可靠。

## 原始内容

**仓库**: SerendipityOneInc/ecap-agent-pack  
**SHA**: [3c486753](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/3c486753dcbe3f0433d5d544eaf23cd283092991)
**PR**: [#145](https://github.com/SerendipityOneInc/ecap-agent-pack/pull/145)  
**作者**: felix-srp  
**日期**: 2026-05-27T10:21:53Z

**Commit Message:**

```
feat(agent-studio): v1.4.0 — spec-driven build flow + release-zip filter (#145)

* test(agent-studio): scaffold pytest layout

* feat(agent-studio): spec extract data model

* feat(agent-studio): mechanical satisfied_by pattern resolver

* test(agent-studio): fixtures for spec-coverage round-trip

* feat(agent-studio): spec_coverage.py render subcommand

* feat(agent-studio): spec_coverage.py sync subcommand

* feat(agent-studio): validate.py --check-spec flag (no-op stub)

* feat(agent-studio): validate.py walks spec items, gates Stage 4

* feat(agent-studio): scaffold.py --from-spec seeds identity + skills

* feat(agent-studio): Studio SOP for spec extraction

* feat(agent-studio): wire spec coverage into stage references

* test(agent-studio): end-to-end spec flow integration

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): preserve unsynced waivers; raise on .arr[].field selectors

* fix(agent-studio): yaml equality, notes round-trip, semantic edit persistence, --lang default + trim SOP

Addresses 4 high-severity findings from final code review:

1. yaml: patterns now support `==<value>` equality (not just truthiness).
   `yaml:agent/agent-pack.yaml:.name=="nutrition-buddy"` enforces the exact
   value the spec pinned, rather than ticking for any non-empty name.

2. `## Notes (unparsed)` round-trips: _render emits the section when
   notes_unparsed is non-empty; _apply_md_to_extract only overwrites the
   field when the md actually contained a Notes section, so prior notes
   survive when the creator removes the section from the .md.

3. validate.py persists semantic md edits by dumping the extract whenever
   the .md was applied (not just on auto_ticked). Re-render is still gated
   on auto_ticked so the existing notes-preservation behavior holds.

4. scaffold.py --lang default restored. `default=None` lets spec hydration
   take precedence; if both hydration and --lang are absent, `zh,en`
   applies. --lang is dropped from the required-fields list.

Trim pass on prose to recover tokens: references/spec-extraction.md
102→77 lines; compressed spec_coverage.py docstring and _shorten comment;
tightened _spec_patterns.py module docstring.

Tests: 32 pass (29 existing + 3 new: yaml_equality_match,
sync_preserves_existing_notes_when_md_lacks_section,
check_spec_persists_semantic_md_edits).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): address remaining 11 spec gate findings

- _spec_schema: add SpecItem.value field; reject mechanical items with
  empty satisfied_by at load time.
- _spec_patterns: tighten selector grammar (hyphen support, negative
  indices, full-path consumption check); reject absolute paths and
  `..` traversal; validate cron/data_source handler names; convert
  YAMLError to PatternError.
- spec_coverage: render id markers in bullets (<!-- id=... -->); sync
  now parses by id (dict-by-id), deletes items absent from md, and
  clears stale waiver_reason on done transition.
- validate: tighten _safe_resolve and check_spec exception handling
  to (PatternError, OSError) tuples.
- scaffold: use load_extract for hydration; prefer SpecItem.value over
  evidence parsing; reject invalid kebab-case names; clean error
  messages on missing/invalid spec files; lang now in required field
  list with from-spec-aware hint.
- Fixtures: add value field to identity items; regenerate golden md
  with id markers.
- Tests: add 12 new tests covering schema rejection, selector grammar,
  path security, handler name validation, id-tracked deletion,
  waiver-cleared-on-done, value-field hydration, kebab-name
  validation, and missing-file clean error.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): prevent silent data loss + 6 spec-gate issues from Claude/Codex review

* fix(agent-studio): round-2 review hardening — unknown-id wipe guard, stale evidence, empty == rhs, demotion re-render, atomic dump

* fix(agent-studio): require explicit --prune for item deletion (round-3 hardening)

* fix(agent-studio): v2 review pass — schema tightening, parser hardening, atomic md write, SOP value field

Schema (load_extract / dump_extract):
- reject newlines in title/description (would have triggered --prune wipe)
- reject non-string `value` (would have crashed scaffold)
- reject duplicate item ids
- atomic_write_text helper preserves existing file mode (0o644 lost on rewrite)

Parser (_apply_md_to_extract):
- _BULLET_RE accepts leading whitespace and arbitrary trailing text after id marker
- track ``` fence state at EOF — unclosed fence skips deletion (parallels the all-unknown-id guard)
- explicit pending_item reset for any non-bullet/non-continuation line — stray prose can't hijack waiver_reason / # evidence
- box transition [x]→[~] now clears stale evidence_of_satisfaction
- returns bool indicating mutation

validate.py:
- uses _apply_md_to_extract's bool return — no spurious spec-extract.json rewrites when nothing changed
- routes md re-render through atomic_write_text

scaffold.py:
- skill name extraction uses full slug between `skill.` prefix and `.scaffold` suffix (dotted segments preserved)
- error message maps required flags to their actual spec item ids (display_name → identity.pack_name, lang → identity.languages)

tests/conftest.py: importorskip yaml so missing PyYAML produces a clean skip instead of opaque subprocess failures.

SOP (references/spec-extraction.md): Output section now documents the `value` field for identity items. Trimmed prose across spec-extraction.md / discovery.md / testing.md (10 lines saved).

Tests: 59 → 69 (10 new regression tests).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* feat(agent-studio): surface spec-doc entry path in first-run greeting

Opening question now offers three explicit paths: (a) chat through it,
(b) attach a spec/design/requirements doc to parse, or (c) resume an
existing pack. The spec-doc path was already supported by Studio's
detection logic but wasn't visible to creators until they spontaneously
pasted one.

* chore(agent-studio): bump to 1.4.0; untrack tests/ for client ship

- agent-pack.yaml: 1.3.4 → 1.4.0 (spec-driven build flow, PR #145)
- .gitignore: tests/, .pytest_cache/, __pycache__/, *.pyc
- untrack the 11 test files (kept on disk for dev; clients receive a
  test-free pack via release-agent-zips.yml)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore: re-track tests/ in repo; exclude from release zips

Reverses the tests/ untrack from ccf6997. Tests stay in git (CI + contributor
visibility); release-agent-zips.yml now produces zips without dev-only paths.

- .github/scripts/agent_release.py: replace shutil.make_archive with a
  filtered zipfile walk that skips tests/, __pycache__/, .pytest_cache/, *.pyc
  in both package-release and package-legacy-release.
- agent-studio/.gitignore: drop tests/, keep build-artifact patterns.
- agent-studio/.agents/skills/agent-studio/tests/: re-tracked (11 files).

Smoke: confirmed agent-studio-1.4.0.zip excludes tests/__pycache__/.pyc; spot
check across all 28 packs in the workspace shows none ship dev-only paths.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(agent-studio): drop scope-creep .gitignore patterns

Reverts .gitignore to its pre-PR state (just BOOTSTRAP.md.done). The
.pytest_cache/__pycache__/*.pyc patterns added in ccf6997 were never part
of this PR's scope — release-zip exclusion is now handled by agent_release.py.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Ning Hu <ning@gensmo.ai>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```


**PR Description:**

## Summary

Makes Agent Studio's **spec-doc → agent build** flow explicit, surfaced, and gated:

- **Discoverable** — first-run greeting offers spec-doc upload as one of three explicit entry paths.
- **Structured** — spec is parsed into `data/spec-extract.json` (machine) + `data/spec-coverage.md` (human-editable), round-tripped deterministically.
- **Gated** — `validate.py` refuses Stage 4 if any spec item is unbuilt without a waiver.

When no spec is provided, all new code paths no-op — existing conversational discovery is unchanged.

Ships as `agent-studio` **v1.4.0**.

## What's new

- **`BOOTSTRAP.md` first-run greeting** — three explicit entry paths: (a) chat-through, (b) attach a spec/design/requirements doc, (c) resume an existing pack.
- **`references/spec-extraction.md`** — Studio's operating SOP for parsing a spec doc into `data/spec-extract.json` (Studio writes the JSON directly using its multimodal capabilities; no Python LLM-call layer).
- **`scripts/spec_coverage.py`** — deterministic round-trip between `data/spec-extract.json` (machine source of truth) and `data/spec-coverage.md` (human-editable checklist). Subcommands: `render`, `sync`. `sync --prune` required to delete items (silent deletion guard).
- **`scripts/_spec_schema.py`** — `SpecItem` + `SpecExtract` dataclasses with load/dump validation (9 item kinds, 2 tick kinds, 3 statuses). Atomic dump, multiline-title rejection, duplicate-id rejection.
- **`scripts/_spec_patterns.py`** — mechanical `satisfied_by` resolver supporting file paths, `yaml:<file>:<selector>`, `yaml:<...>==<value>` (with empty-RHS guard), `cron:<handler>`, `data_source:<name>`.
- **`scripts/validate.py --check-spec`** — auto-on when `data/spec-extract.json` exists. Walks the pack, auto-ticks mechanical items, demotes stale-evidence items, gates Stage 4 on remaining open items. Merges unsynced `data/spec-coverage.md` edits so creator-added waivers aren't clobbered.
- **`scripts/scaffold.py --from-spec`** — seeds identity + skill list + languages from the extract via the canonical `value` field; `--agent-name` is the only required override.
- **References wired in** — `discovery.md` branches into the SOP when a spec is detected; `skill-design.md` / `automation.md` instruct Studio to tick semantic items at stage gates; `testing.md` documents the gate behavior and creator exits (build / waive / drop); `SKILL.md` adds the two new truth sources.

## Hardening

Three rounds of adversarial review (Claude + Codex) addressed: silent data loss on unknown ids, stale-evidence persistence, `==no` boolean-vs-string ambiguity, demotion re-render, atomic md write, schema tightening, `--prune` required for deletions, unsynced-waiver preservation. See `76e5f72`, `93f0858`, `01b2264`, `5f53676`, `0ea517a`.

## Release packaging (affects all packs)

- **`.github/scripts/agent_release.py`** — replaced `shutil.make_archive` with a `zipfile`-based walk that skips `tests/`, `__pycache__/`, `.pytest_cache/`, and `*.pyc`. Applies to both `package-release` (the main release flow) and `package-legacy-release`. Tests stay in the repo (CI runs them, contributors can run them); client zips no longer carry dev-only paths.
- **`agent-studio/.gitignore`** — unchanged from main; exclusion is enforced at release time, not via gitignore.

## Test plan

- [x] **Automated** — 69 unit + integration tests via `cd agent-studio/.agents/skills/agent-studio && uv run --python 3.12 --with pytest --with pyyaml -m pytest tests/ -v`. Also confirmed clean run (9.2s, 69 passed) inside `ghcr.io/serendipityoneinc/openclaw-docker:2026.5.7`.
- [x] **End-to-end pipeline (in-container)** — scaffolded the nutrition-buddy fixture through `spec_coverage.py render` → `scaffold.py --from-spec` → `validate.py` (correctly reports `4/8 passed, 3 failed, 1 warnings` for a fresh scaffold; auto-ticks 2 mechanical items; flags 9 open items with actionable hints) → `package.py` produces `zip/nutrition-buddy-0.1.0.tar.gz` (843 B).
- [x] **Manual smoke (live openclaw gateway)** — agent-studio registered via `openclaw agents add agent-studio --workspace /workspace/agent-studio`; first-run greeting confirmed to surface the spec-doc entry path; gateway-driven scaffold from a real spec doc completed end-to-end.
- [x] **Release-zip smoke** — ran `agent_release.py package-release` and `package-legacy-release` locally; resulting `agent-studio-1.4.0.zip` (106 KB) contains no `tests/`, `__pycache__/`, `.pytest_cache/`, or `.pyc` entries. Spot-checked all 28 packs — none ship dev-only paths.

## Observed during smoke (separate PR)

When the creator uploads a `.docx` spec, Studio's model bypasses the ecap-skills `docx` skill (its SKILL.md description doesn't surface `read`/`analyze` — only `create`/`edit`/`fill`/`reformat`) and falls back to ad-hoc `pip install python-docx` + per-doc extraction scripts, which can time out on image-heavy decks. `xlsx` parses fine because its description leads with `read`. Fix is a one-line description tweak in `ecap-skills/docx/SKILL.md` — not in scope for this PR.

## Design docs

- Design spec: `~/Workspace/design-doc/2026-05-25-spec-driven-agent-build-design.md`
- Implementation plan: `~/Workspace/design-doc/2026-05-26-spec-driven-agent-build-plan.md`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

