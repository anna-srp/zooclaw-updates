# ecap-agent-pack Commits — 2026-05-20

## 8c36cfa2 — fix(agent-studio): anchor package.py --output to pack-dir (#136)

- **Author**: felix-srp
- **Date**: 2026-05-20T11:43:12Z
- **PR**: #136

### Commit Message

```
fix(agent-studio): anchor package.py --output to pack-dir (#136)

* fix(agent-studio): anchor package.py --output to pack-dir

`--output zip/` was a CWD-relative path. If the studio session's bash CWD
drifted into another workspace (e.g. an installed pack inspected during the
build), package.py silently created `zip/` there instead of in the studio
workspace — so the archive existed but the install UI, which only scans the
studio workspace, couldn't see it.

Anchor a relative `--output` to `pack-dir`. Absolute paths are unchanged for
backward compatibility.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): anchor install.py --output to pack-dir

Same CWD-vs-pack-dir bug as the previous commit, in install.py's
`list-sources` and `install` commands. install.py is usually called from
the studio workspace so the impact is smaller than package.py's, but
keeping the two scripts symmetric removes a latent footgun if the agent
ever drifts CWD between packaging and installing.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): anchor run_share.py --output to pack-dir

Final piece of the CWD-vs-pack-dir symmetry. run_share.py is invoked
both directly (/studio share) and as a subprocess from install.py;
either path could in principle stage the archive under the wrong
workspace if CWD drifted. Aligns with the same fix in package.py and
install.py.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(agent-studio): bump version 1.3.1 → 1.3.2

Patch bump for the package.py / install.py / run_share.py output-anchor fix.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Anchor `--output` to `--pack-dir` (rather than CWD) in three studio scripts so a session-CWD drift can't silently misdirect packaging / scanning / sharing into the wrong workspace.

- **`package.py`** — original reported bug. With `--output zip/` resolved against CWD, an in-session `cd` into another workspace (e.g. an installed pack inspected during the build) silently created `zip/` there. The install UI only scans the studio workspace, so the archive existed but couldn't be selected.
- **`install.py`** (`list-sources` + `install`) — same latent footgun on the install side: a CWD-drifted invocation would either scan the wrong `zip/` (`list-sources`) or stage the current pack's archive into the wrong workspace (`install --source current`, via `run_share.py`).
- **`run_share.py`** — same anchoring on the share path, both for direct `/studio share` and for the `install.py` subprocess call.

In all three: relative `--output` is now resolved against `pack_dir.resolve()`; absolute paths pass through unchanged.

## Repro / evidence

On the affected prod pod (`oc-f0dcf1f4-94f9cc886-c9jkg`):

```
workspace-agent_studio/zip/                                   ← correct
  xiaohongshu-publisher-{0.1.0, 0.2.0, 0.2.1, 0.2.2}.tar.gz   (09:57–09:58, after agent noticed and re-packaged)

workspace-custom-xiaohongshu-publisher-0-1-0/zip/             ← wrong
  xiaohongshu-publisher-{0.2.0, 0.2.1, 0.2.2}.tar.gz          (08:49–09:46)
```

Same Studio session packaged three versions into the installed pack's workspace before the agent caught it and re-packaged into the right place. Deterministic given the CWD drift — not intermittent.

## Test plan

- [x] Manual: `package.py --pack-dir /abs/path --output zip/` from `/tmp` — archive lands at `/abs/path/zip/`, not `/tmp/zip/`.
- [x] Manual: `install.py list-sources --pack-dir /abs/path --output zip/` from `/tmp` — no `/tmp/zip/` created; scan reads `/abs/path/zip/`.
- [x] Manual: `run_share.py --pack-dir /abs/path --output zip/` from `/tmp` — no `/tmp/zip/` created (errors expected before staging since the studio repo itself isn't a user pack).
- [x] AST parse-check on all three files.
- [ ] Reviewer: confirm normal `/studio publish` / `/studio install --source current` / `/studio share` paths still behave identically when invoked from the studio workspace (CWD == pack-dir, so the new anchoring is a no-op there).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 3b9362f6 — fix(agent-studio): surface --archive flag in share + pack/command hints at session start (#133)

- **Author**: felix-srp
- **Date**: 2026-05-19T17:47:48Z
- **PR**: #133

### Commit Message

```
fix(agent-studio): surface --archive flag in share + pack/command hints at session start (#133)

* fix(agent-studio): surface --archive flag in share + pack/command hints at session start

- agent-studio-share/SKILL.md: document the existing `--archive <path>` flag so
  creators can share a pre-packed `.tar.gz` without repackaging the current
  workspace. The Python already supported it; SKILL.md was hiding it from agents.
- AGENTS.md: add a one-line orientation on first DEV reply (active pack name +
  `/studio` prefix reminder) so creators stop typing `/new` instead of
  `/studio new` and always know which pack the workspace is editing.
- Bump version 1.3.0 → 1.3.1.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(agent-studio): trim tokens in share SKILL.md + AGENTS.md THIRD step

Tighten the prose added in the previous commit. No behavioral change.

- agent-studio-share/SKILL.md: collapse the `--archive` bullet (was ~70 words,
  now ~20) — drop where-to-find-archives illustration and the "package.py
  skipped" sentence (already covered in Internal behavior). Shorten
  `--artifacts-base-url` to `<url>` placeholder. Trim "that path … no
  packaging step" → "directly, no packaging".
- AGENTS.md: trim THIRD step ~30 tokens — drop "mode" / "of session"
  (parallel with FIRST/SECOND), drop "(the name: from agent/agent-pack.yaml)"
  (already read in SECOND), drop ", not /new" (positive example suffices),
  make skip-condition mechanically checkable ("starts with /studio").

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(agent-studio): tighten --archive fallback note + THIRD-step scope

Address review feedback on PR #133:
- SKILL.md: disclose the unversioned-filename fallback for --archive
  (version="unknown") so the documented identity contract matches
  run_share.py's actual parsing behavior.
- AGENTS.md THIRD step: state DEV-only / once-per-session scope and
  explicit TEST = no orientation, removing ambiguity around when the
  one-line orientation fires.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Ning Hu <ning@gensmo.ai>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Two small docs/SOP fixes for Agent Studio v1.3.1, motivated by friction seen with real creators.

- **`/studio share --archive <path>` is now reachable.** `run_share.py` already supported the flag (validates and stages a pre-packed `.tar.gz` without invoking `package.py`), but `agent-studio-share/SKILL.md` never told the agent it existed — so the share flow was locked to "repackage the current workspace" with no way to share a foreign archive. SKILL.md now documents the flag, the no-repackage path, and that an unversioned filename falls back to `version="unknown"` (mirrors `run_share.py`'s actual parsing).
- **Session-start orientation in DEV mode.** AGENTS.md now asks the agent to lead its first reply of a DEV session with a one-line orientation: which pack is active (`name:` from `agent/agent-pack.yaml`) and that creator commands use the `/studio` prefix (e.g. `/studio new`, not `/new`). Scope is explicit: DEV only, once per session, skipped when the user's first message already starts with `/studio`, and silent in TEST so the pack-agent persona is preserved.
- Version bump `1.3.0 → 1.3.1`.

No Python changes.

## Test plan

Verified in a sibling openclaw-docker container (`ghcr.io/serendipityoneinc/openclaw-docker:2026.5.7`) on the patched workspace.

Script-level (run via `uv run --python 3.12 .agents/skills/agent-studio-share/scripts/run_share.py`):

- [x] No `--archive`, no existing `zip/<pack>-<version>.tar.gz` → calls `package.py`; `archive_reused=false`, archive built and staged into `artifacts/shares/`.
- [x] No `--archive`, matching zip already in `zip/` → reuse path; `archive_reused=true`, `package.py` not invoked.
- [x] `--archive zip/imported-pack-2.0.5.tar.gz` → skips `package.py`; `pack_name=imported-pack`, `version=2.0.5` parsed from filename even though the workspace manifest says otherwise (workspace manifest correctly ignored).
- [x] `--archive zip/myarchive.tar.gz` (no version segment) → succeeds with `pack_name=myarchive`, `version="unknown"` (documented fallback).

LLM-level (manual webchat session against the deployed pack):

- [x] DEV first session, neutral message → first reply names the active pack and mentions the `/studio` prefix.
- [x] DEV first message is itself `/studio …` → orientation line skipped, command handled directly.
- [x] TEST mode first reply → pack-agent persona, no orientation line.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

