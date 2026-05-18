# ecap-agent-pack — 2026-05-17 commits

## [1] e719ed00

- **Author**: felix-srp
- **Date**: 2026-05-17T11:11:03Z
- **PR**: #129

### Commit Message

```
fix(agent-studio): package.py refuses mismatched description.json (#129)

* fix(agent-studio): identity-drift detector + package.py description.json guard

Closes the workspace-pollution bug class observed on prod bot
oc-53bfc1d0…ppz7n: a pack pivot (coros-coach → fitbeing-health-agent)
was made by editing agent/agent-pack.yaml in place, without /studio new.
The previous pack's description.json survived in agent/ and got bundled
verbatim into the new archive — shipping COROS Coach's listing under
the Fitbeing pack name.

Two complementary layers:

1. **Drift detector** (`validate.py:check_identity_drift`). Compares
   manifest `name:` against `data/.identity-state.json` (seeded by
   scaffold.py, wiped by clean.py). On rename, scans for strong
   prior-pack residue — mismatched `description.json#agentPack_id`,
   skill dirs absent from current manifest. No residue → silent state
   advance (covers typo fix). Residue → hard fail pointing at /studio
   new. New `validate.py --check-identity` subcommand; AGENTS.md gates
   every DEV session-start on it; package.py and install.py --source
   current call it before doing anything destructive.

2. **package.py guard**. Last-line defense: refuses to package when
   description.json's `agentPack_id` doesn't match manifest `name:`.
   Catches the bug even if the drift detector is somehow bypassed
   (legacy workspace with no .identity-state.json, hand-run script).

Tests: 11 cases covering pre-scaffold no-op, first-run seeding,
stable-identity pass, silent rename, mismatched description.json,
orphan skill dirs, empty-dir / pack-onboarding ignores, corrupt state
file recovery, and end-to-end package.py guard pass/fail.

Bumps agent-studio v1.2.2 → v1.2.3.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor(agent-studio): /simplify pass on identity-drift PR

- lift `_read_description_json` from install.py + `_read_description_pack_id`
  from package.py into a shared `_common.read_description_json` (3 copies → 1)
- move `from validate import check_identity_drift` to module top in package.py
  and install.py — no cycle exists, local imports were unjustified
- inline `_run_identity_drift_check` wrapper in package.py (was just dict
  reshaping)
- drop `write_identity_state` read-then-skip dedup (skip path costs ≈ write
  it avoids; dead in practice since drift detector's stable-name branch
  returns before calling write_identity_state)
- pass `current_name` into `_scan_identity_residue` instead of re-extracting
  from manifest
- replace TOCTOU exists/read pair in residue scan with the shared reader
- trim defensive `isinstance(str) and x` chains where `or None` suffices
- trim WHAT/narrative comments; keep only WHY (e.g. "no SKILL.md = transient
  mkdir, not residue")
- drop prod pod ID coupling from test module docstring
- delete pre-existing `pack_root = pack_dir.resolve()` unused-var in
  package.py:main (dead code surfaced during simplify)
- packaging.md §5a: note that regen is mandatory after pivots (the guard
  enforces it now)

Tests: same 11 cases still pass.

Net: -75 lines across the diff.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): address Codex review findings on drift detector

Three real bugs flagged in the Codex review:

1. **Corrupt/missing state file masks drift.** Previously, if
   `.identity-state.json` was missing or unparseable, the detector
   silently re-seeded from the current manifest *before* scanning for
   residue — so a truncated state file (or a legacy pre-this-PR
   workspace) with prior-pack `description.json` would pass clean.
   Now: residue scan runs regardless of whether the baseline was
   "missing", "corrupt", or "drifted"; only a clean workspace gets
   the silent-seed. Failure mode reports baseline as "(missing
   baseline)" when state was absent/corrupt.

2. **pack-onboarding whitelist leaked stale onboarding.** Previously
   any `skills/pack-onboarding/` was skipped from residue scanning
   because it's auto-generated and not in `manifest.skills`. But
   `write_onboarding.py` embeds the pack name into the SKILL.md
   description ("First-time setup for <pack_name>") and H1 ("Onboarding
   — <pack_name> Setup") — so a stale onboarding from a prior pack
   still ships the old pack name. Now the scan checks pack-onboarding's
   SKILL.md content and flags it when the embedded pack name doesn't
   match the current manifest.

3. **`write_identity_state` raised raw `OSError`.** Disk pressure or
   permission issues would surface as unhandled tracebacks at session-
   start (highest-risk site) instead of structured JSON. Now returns
   `bool` and swallows OSError — the drift detector loses its baseline
   (next run re-seeds) but no script crashes.

5 new tests cover: pack-onboarding matching current (pass), pack-
onboarding stale flagged, pack-onboarding without markers ignored,
missing-state + residue fails loudly, corrupt-state + residue fails
loudly, disk-error swallowed. 16 tests total, all passing.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): address Codex pass-2 findings (3 more bugs)

1. **pack-onboarding OR-logic gap.** Previous `_pack_onboarding_targets_other_pack`
   returned False if EITHER the description marker OR the H1 marker matched
   the current pack name — so a half-pivoted file (one marker fresh, one
   stale) silently passed. Rewrite with regex extraction: pull ALL
   `First-time setup for <X>.` and `Onboarding — <Y> Setup` names out of the
   content; flag as residue iff any embedded name differs from current.

2. **Unreadable description.json silently passed.** `read_description_json`
   collapses PermissionError to None (treated as "absent" by callers). A
   workspace where prior-pack description.json exists but is mode 0 would
   thus produce no residue signal. Add `desc_path.exists()` guard in
   `_scan_identity_residue`: present-but-unreadable now surfaces as residue
   ("agent/description.json present but unreadable").

3. **Unreadable .identity-state.json silently re-seeded.** Same shape as
   #2 — `read_identity_state` collapses OSError to None, indistinguishable
   from "absent". A permission-denied state file with a clean workspace
   would silent-seed and erase the baseline. Add `IDENTITY_STATE_REL.exists()`
   guard in `check_identity_drift`: present-but-unreadable adds an explicit
   residue entry so the silent-seed path doesn't fire.

3 new tests + 1 deleted-now-contradictory test. 19 cases total, all passing.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): unreadable pack-onboarding SKILL.md must not silent-pass

Codex pass-3 finding (symmetric to the description.json / identity-state
fixes in 8d541cb that I missed for the third helper).

`_pack_onboarding_targets_other_pack` swallowed OSError and returned False
("not residue"), so an unreadable stale `skills/pack-onboarding/SKILL.md`
silently passed both the orphan-skill check and the embedded-name check.

Rename helper to `_pack_onboarding_residue` and return `str | None` so it
can surface "present but unreadable" as residue alongside the existing
"targets a different pack" signal.

20 tests total, all passing.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(agent-studio): untrack script test suite; keep dev-only

The drift detector / package.py guard tests under
`agent-studio/.agents/skills/agent-studio/scripts/tests/` were tracked
by mistake — anything under `.agents/skills/<pack>/scripts/` ships to
the customer pod via the agent-pack distribution. They have no business
being on a customer's filesystem.

`git rm --cached` to untrack while keeping them on disk locally for
dev. Repo-root `.gitignore` now excludes
`**/.agents/skills/*/scripts/tests/` so they (and any sibling pack's
future test suites) stay untracked by default.

This matches the pre-existing convention (the original repo had no
test files committed to script directories). Tests still run locally
via `uv run --python 3.12 --with pytest python -m pytest tests/ -v`
in the scripts dir.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor(agent-studio): fold drift check into migrate_manifest.py subprocess

AGENTS.md previously ran two `uv run --python 3.12 ...` invocations at
every DEV session-start — migrate_manifest.py + validate.py --check-
identity. Both are idempotent-when-nothing-changed but each pays ~300ms
of cold uv subprocess startup. And two steps in AGENTS.md = two LLM
instructions to follow, two opportunities for variation.

Fold the drift check into migrate_manifest.py: same single subprocess
runs the (idempotent) migration and then `check_identity_drift()`,
returning a combined JSON with `identity_drift` field and exiting non-
zero on drift. AGENTS.md collapses to one line — fewer tokens, no
two-step variation risk, half the session-start cold-start cost.

(`validate.py --check-identity` stays for manual debugging and tests;
just no longer wired into AGENTS.md.)

Verified end-to-end: clean workspace returns exit 0 with `identity_drift.
status="pass"`; pivoted workspace returns exit 1 with drift details. All
20 dev-only tests still pass.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(agent-studio): break dev-mode session-start back into one-line-per-step

The merged-subprocess commit collapsed the dev-mode bullet into a single
dense paragraph that doesn't match the rhythm of the surrounding bullets.
Restore the original three-line shape (command on its own line, drift
note, then read-files instruction).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(agent-studio): tighten dev-mode session-start bullet

~50% fewer tokens by:
- dropping explanatory color ("idempotent; legacy-layout migration +
  identity-drift gate") that's for human readers, not the LLM
- letting the script's structured JSON (which already includes a
  `resolution` field) self-describe failure instead of restating it
- explicit "Otherwise" branching makes exit-code semantics obvious
- four lines → two

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(agent-studio): drop redundant --pack-dir . — it's the default

migrate_manifest.py defines `--pack-dir` with `default="."`, so the
explicit flag at the session-start invocation is noise. Session-start
runs from the workspace root anyway, so the default resolves correctly.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor: carve PR #129 down to package.py description.json guard only

After working through the design with the user, the drift detector was
solving the wrong problem: creators iterate on multiple packs over
time, and the root cause is the missing /studio open capability. With
/studio open available, creators wouldn't be tempted to edit the
manifest in place — the drift detector becomes a "you forgot to /studio
open" guard, which is much lower-value than the framing implied.

Drop the drift-detector half of the PR. Keep only the genuinely
independent package.py guard + shared description.json reader — these
catch description.json/manifest mismatches caused by ANY path (partial
regen, manual edit, future feature bug), independent of the pack-
switching workflow.

This commit reverts the following to main:
- validate.py (no check_identity_drift, no --check-identity flag)
- scaffold.py (no write_identity_state seed)
- migrate_manifest.py (no drift integration)
- AGENTS.md (no session-start drift gate)
- .gitignore (no tests/ exclusion — kept dev-only, no PR exposure)

And surgically removes drift bits from:
- _common.py (drop IDENTITY_STATE_REL + read/write_identity_state;
  keep read_description_json)
- package.py (drop drift check call; keep description.json/manifest
  guard + the pre-existing pack_root dead-var removal)
- install.py (drop drift check call + validate import; keep the
  refactor to use the shared read_description_json)

A new PR will land /studio open + workflow prompts.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor: /simplify pass on carved PR

Three findings from parallel reuse / quality / efficiency reviewers:

- **TOCTOU + double work in package.py guard.** Old code did
  `desc_path.exists()` (stat #1) then `read_description_json` which
  itself stats and reads (#2). Plus a latent race: if the file
  vanished between stats, the helper returned None but `files_to_include
  .append(("description.json", desc_path))` still queued the missing
  path, which would fail later in tar.add. Fix: drop the .exists()
  check, gate the entire branch (and the append) on `desc_data is not
  None`. One stat instead of two; race closed.
- **Lost UnicodeDecodeError coverage.** install.py's old local reader
  caught `(FileNotFoundError, IsADirectoryError, NotADirectoryError,
  UnicodeDecodeError, json.JSONDecodeError)`. New shared
  `read_description_json` catches `(OSError, json.JSONDecodeError)` —
  but `UnicodeDecodeError` inherits from `ValueError`, not `OSError`,
  so a bad-encoding description.json would now crash instead of
  returning None. Add `UnicodeDecodeError` to the except tuple.
- **Stale comment.** Old guard comment referenced a "drift check" /
  "identity-state.json" — neither exists in the carved PR. Rewrote to
  describe what the guard actually does: catch the exact prod symptom
  (pivoted workspace silently shipping prior pack's listing).
- **Docstring caller-list rot.** Dropped "Used by the package.py guard
  and install.py's pre-card builder" — caller lists go stale.

Verified end-to-end: mismatched description.json refused, matched
description.json packages cleanly, missing description.json still
treated as optional (same as before).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix: narrow read_description_json except tuple to match install.py's prior contract

Both Codex and Claude reviewers flagged the same parity drift: the new
shared helper caught `OSError`, which subsumes `PermissionError`,
`BlockingIOError`, disk-full errors, etc. The old `install.py`
`_read_description_json` deliberately caught only the narrow set
"malformed/missing user content" and let env errors propagate — its
comment said "let env errors (PermissionError, disk) propagate"
explicitly.

With the broadened catch, a permission-denied description.json on a
customer pod would silently return None instead of surfacing — install
would proceed with manifest-fallback metadata, package.py would skip
the file from the archive, and the operator would see no signal.

Narrow back to `(FileNotFoundError, IsADirectoryError,
NotADirectoryError, UnicodeDecodeError, json.JSONDecodeError)`.
Permission errors and disk failures now propagate as before. Updated
the docstring to make the principle explicit ("user content = no
overlay, env errors propagate").

Verified end-to-end:
- missing file → None silently
- malformed JSON → None silently
- chmod 000 file → PermissionError propagates

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Bug

Prod bot `oc-53bfc1d0-6f5b59cb49-ppz7n` shipped a Fitbeing Health Agent pack whose `description.json` still described the previous pack (COROS Coach), because nothing verified the file matched the current pack before bundling it.

## Fix

`package.py` refuses to package when `agent/description.json#agentPack_id` doesn't match `agent-pack.yaml#name`. The error message points the creator at `generate_description.py` (Stage 5a):

```
package.py: agent/description.json describes 'coros-coach' but manifest is
'fitbeing-health-agent'. Re-run generate_description.py (Stage 5a) before
packaging.
```

Plus drive-by cleanup: `install.py`'s local `_read_description_json` and the new guard now share `_common.read_description_json`. A stale `pack_root = pack_dir.resolve()` dead var in `package.py:main` is removed.

## What's not in this PR

The earlier rev attempted to catch the broader workspace-pollution class — leftover skill dirs, mismatched identity state, etc. — via a residue-based "drift detector" that ran at session start. While working through the design we realized the bug is a *symptom* of a missing capability: creators iterate on multiple packs over time, but the only way to switch packs is `/studio new` (which wipes). With no "open a previously-built pack" affordance, creators are pushed toward "just edit the manifest in place" → workspace pollution.

A follow-up PR will land `/studio open` (extract a previous archive from `zip/` back into the workspace) + proactive post-delivery prompts ("iterate this pack? start a new one? open an existing one?"). The drift detector becomes redundant once creators have a clean switching path — and may not be needed at all.

This PR therefore stays focused on the **packaging-boundary symptom** that's genuinely independent: a description.json/manifest mismatch caused by ANY path (partial regen, manual edit, future bug) is caught before the archive ships.

## Review iteration

Multiple parallel Codex + Claude review passes. Two real issues caught and fixed:

| Pass | Issue | Fix |
|---|---|---|
| /simplify | TOCTOU + double work (`.exists()` then `read_text` in helper); race where file vanishes between check and read; lost `UnicodeDecodeError` coverage from install.py's original except tuple | dropped `.exists()` check, gated on `desc_data is not None`; added `UnicodeDecodeError` to except tuple |
| Codex 1 / Claude 1 | broadened `OSError` catch silently swallowed `PermissionError` / disk errors that install.py's original reader deliberately let propagate ("user content = no overlay; env errors propagate") | narrowed except tuple back to `(FileNotFoundError, IsADirectoryError, NotADirectoryError, UnicodeDecodeError, json.JSONDecodeError)`; docstring documents the principle |
| Codex 2 / Claude 2 | — | both clean |

## End-to-end verification

- Mismatched `description.json#agentPack_id` → packaging refused with exit 1 and clear message
- Matched → packaging succeeds normally
- Missing `agent/description.json` → still treated as optional (same as before)
- `chmod 000 agent/description.json` → `PermissionError` propagates (env errors don't silently degrade to wrong-pack install)

## Version

Bumps agent-studio v1.2.2 → v1.2.3.

## Files

5 files, +36 / -18 lines.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

