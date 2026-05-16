---
title: "hotfix v1.2.1 — move user pack files under agent/, auto-recover affected workspaces"
type: "Bug Fix"
priority: "高"
date: "2026-05-15"
status: "待审核"
channels: ""
repo: "SerendipityOneInc/ecap-agent-pack"
sha: "b99e6add0585d77d047f3d97ac46cb24d312591e"
---

# hotfix v1.2.1 — move user pack files under agent/, auto-recover affected workspaces

## 核心宣传点

修复了影响用户使用的重要问题：hotfix v1.2.1 — move user pack files under agent/, auto-recover affected workspaces

## 原始内容

**Commit**: `b99e6add0585d77d047f3d97ac46cb24d312591e`
**Author**: felix-srp
**Date**: 2026-05-15T03:57:30Z
**PR**: #125 — https://github.com/SerendipityOneInc/ecap-agent-pack/pull/125

### Commit Message

```
fix(agent-studio): hotfix v1.2.1 — move user pack files under agent/, auto-recover affected workspaces (#125)

* fix(agent-studio): move user pack manifest to agent/agent-pack.yaml

The user pack manifest used to live at workspace root, colliding with
Agent Studio's own agent-pack.yaml that the workspace itself ships
with. On scaffold the user's manifest was written over Agent Studio's
manifest; on the next Agent Studio update the workspace's seed step
wrote Agent Studio's manifest back, clobbering the user's pack identity
(name, version, skills[]). Two prod incidents — agent_studio bots
4baa8c76 and f7bd58dc — lost their pack manifests this way; the
in-progress skill directories under skills/ survived because they live
in a different path, but the manifest had to be restored from git.

Move the user pack manifest to agent/agent-pack.yaml, alongside the
pack's other identity files (AGENTS.md, IDENTITY.md, SOUL.md, ...).
package.py still strips it to archive root so the install-time
contract is unchanged.

Changes
- scaffold.py: write agent/agent-pack.yaml; files_created reports the
  new path.
- _common.py: new find_pack_manifest() helper. Prefers
  agent/agent-pack.yaml; falls back to legacy <root>/agent-pack.yaml
  only when its top-level name != "agent-studio", so we never return
  Agent Studio's own manifest as if it were the user's pack.
- validate.py, package.py, generate_description.py: route through
  find_pack_manifest so legacy workspaces still validate / package /
  describe during the transition.
- clean.py (/studio new): sweep both the canonical and legacy slots,
  with the same name-check guard so we don't delete Agent Studio's
  own manifest.
- SKILL.md / AGENTS.md / references/*.md: tell the model to read /
  write agent/agent-pack.yaml.

Existing workspaces don't need manual migration to keep working — the
fallback handles them. To get them onto the new layout, the creator
can `git mv agent-pack.yaml agent/agent-pack.yaml` (or, for the two
clobbered bots above, `git restore agent-pack.yaml` then mv).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): clean.py only touches agent/agent-pack.yaml

Root agent-pack.yaml belongs to Agent Studio itself; the prior sweep-
with-name-guard was unnecessary defensive code that crossed a layering
boundary. /studio new only resets the user pack's manifest under agent/.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* feat(agent-studio): auto-migrate legacy manifest from git history

Adds migrate_manifest.py, run at dev-mode session start via AGENTS.md.
Idempotent, three branches:

A. Legacy workspace, root agent-pack.yaml still has the user's pack
   (name != agent-studio) → mv to agent/agent-pack.yaml.
B. Update already clobbered root → recover from git HEAD (git show
   HEAD:agent-pack.yaml) and write to agent/agent-pack.yaml. Never
   touches the live root file.
C. Already migrated, or no user manifest anywhere → noop.

Without this, every workspace that hits an Agent Studio update before
its creator manually migrates loses its pack identity on the spot. The
two prod incidents (4baa8c76, f7bd58dc) are recoverable this way as
soon as the new agent-studio ships, no manual intervention needed.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): move user description.json to agent/ + migrate

Same architectural principle as agent-pack.yaml: the user pack's
listing-card lives under agent/ alongside the rest of the pack identity
files, not at workspace root. Agent Studio happens to not ship its own
description.json so this never visibly broke anyone — but the layering
was wrong, and a future Agent Studio release that ever needed one would
have replayed the agent-pack.yaml collision incident.

Changes
- _common.py: USER_PACK_DESCRIPTION_REL + find_pack_description helper
  (canonical agent/description.json with legacy-root fallback).
- scripts (validate, package, generate_description, install) route
  through find_pack_description.
- generate_description.py default --output is agent/description.json.
- clean.py removes agent/description.json (root description.json
  never touched by clean; it's user territory but legacy and Agent
  Studio doesn't ship one of its own).
- migrate_manifest.py also migrates description.json: same A/B/C
  pattern (legacy root mv → restore-from-git → noop).
- SKILL.md / references docs point at agent/description.json.

Existing workspaces with description.json at root keep working via
the legacy fallback, and the migration script lifts them onto the
new layout at next dev-mode session start.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): move user avatar.png to agent/ + migrate

Last of the three user-pack files that lived at workspace root. Avatar
never collided because Agent Studio doesn't ship one, but the principle
is consistent: pack files live under agent/, root is Agent Studio's.

Changes
- _common.py: USER_PACK_AVATAR_REL + find_pack_avatar helper. Search
  order: agent/avatar.png (canonical) → root avatar.png (legacy) →
  artifacts/avatar.png (designer-skill output).
- package.py: remove the local _find_avatar; use the shared helper.
- validate.py: listing-asset check goes through find_pack_avatar.
- clean.py: sweep agent/avatar.png + artifacts/avatar.png; never touch
  root.
- migrate_manifest.py: _migrate_avatar handles three cases —
  legacy root mv, artifacts/ lift, or restore-from-git (binary-safe
  via subprocess capture_output=True without text mode).
- packaging.md §5b: designer output now copied to agent/avatar.png.
- SKILL.md asset-routing line updated.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor(agent-studio): drop legacy fallback for description/avatar helpers

description.json and avatar.png never collided with an Agent-Studio-owned
file at workspace root, so the defensive legacy-fallback in
find_pack_description / find_pack_avatar bought nothing — migrate_manifest.py
already lifts pre-existing root copies to agent/ on first session.

find_pack_manifest keeps its legacy fallback (with the name-guard against
returning Agent Studio's own manifest); that's where the real collision
risk lives.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor(agent-studio): drop find_pack_description, inline the one-liner

It was just `canonical.exists()` after the legacy fallback got removed —
the helper added no value over `(pack_dir / USER_PACK_DESCRIPTION_REL).exists()`
at the call sites. find_pack_avatar stays because it really searches two
locations with a symlink guard.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor(agent-studio): post-review cleanup (correctness + dedupe + trim)

Acting on parallel review of fix/agent-studio-manifest-collision:

Correctness
- install.py:read_current_pack_preview — was still reading legacy root
  agent-pack.yaml; now goes through find_pack_manifest like the rest
  of the branch. Without this, --source current would have broken on
  every workspace post-migration.

Dedupe
- migrate_manifest.py — drop the locally-copied _extract_name in favor
  of _common.extract_field; collapse the text+bytes git wrappers into
  one bytes-returning helper plus a thin text decorator; cache the
  extracted name in _migrate_manifest so it isn't computed twice;
  fold the two-source avatar move into a single loop.
- package.py — remove the dead _within_pack check after
  find_pack_manifest (helper returns a literal pack_dir-rooted path,
  not a resolved one, so the escape-via-symlink concern doesn't apply).

Comment / token trim
- scaffold.py, clean.py, validate.py — drop comments that narrated the
  refactor; keep the one-line "why" each.
- AGENTS.md — tighten the dev-mode migration step.
- packaging.md §5e — collapse the long parenthetical into a single
  sentence; same content, less prose.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): patch the remaining root-manifest readers + tighten Case A

Two findings from independent reviewers:

- run_share.py:68 was the symmetric miss of the install.py bug fixed
  in e6f3e9b. /studio share (and /studio install --source current,
  which calls into share staging) would have read Agent Studio's own
  manifest on every migrated workspace and either failed or
  impersonated agent-studio in the archive identity. Route through
  find_pack_manifest like every other reader on this branch.

- migrate_manifest._migrate_manifest Case A's name-guard was
  asymmetric with Case B: Case A moved any legacy root manifest as
  long as name != "agent-studio", which would lift a name-less /
  corrupt file into agent/. Case B already had the stricter
  name not in ("", "agent-studio") guard. Align Case A.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): tighten find_pack_manifest legacy-fallback guard

extract_field returns "" when name: is missing or unparseable. The
previous != "agent-studio" guard would silently return a name-less
legacy root manifest as if it were the user pack, which is looser
than _migrate_manifest's guard. Use the same `not in ("", "agent-studio")`
check so the two stay symmetric.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(agent-studio): sync docstrings with the tightened name-guard

Three docstring/comment drifts after 34deeb0 tightened the legacy-root
acceptance to `name not in ("", "agent-studio")`. No code change.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(agent-studio): bump version to 1.2.1

Patch release: manifest-collision fix + auto-recovery migration.
Layout change is backward compatible via find_pack_manifest fallback.

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary
**Emergency hotfix.** Two prod bots (`4baa8c76`, `f7bd58dc`) lost their pack identity during an Agent Studio update because the user-pack manifest lived at workspace root and got clobbered by Agent Studio's own root files. This PR moves user-pack files under `agent/` and ships a migration that auto-recovers already-affected workspaces on their next dev-mode session.

## What changed

### Layout (v1.2.1)
| File | Old | New |
|---|---|---|
| pack manifest | `<root>/agent-pack.yaml` (collided w/ Agent Studio's) | `<root>/agent/agent-pack.yaml` |
| listing card | `<root>/description.json` | `<root>/agent/description.json` |
| avatar | `<root>/avatar.png` | `<root>/agent/avatar.png` |

Archive layout produced by `package.py` is **unchanged** — these files are stripped to archive root at packaging time, same as the rest of `agent/*`.

### Auto-recovery (`migrate_manifest.py`)
New script, runs at every dev-mode session start via `AGENTS.md`. Per file, three cases:
- **A.** Legacy root file present → `mv` to `agent/`
- **B.** Live root file gone (clobbered by update) → restore from `git show HEAD:<file>` (binary-safe for avatar.png)
- **C.** Already migrated or fresh workspace → no-op

Name-guard: a legacy `agent-pack.yaml` at root is only accepted as user content when its top-level `name:` parses to a non-empty value other than `agent-studio`. Same guard applies in both `find_pack_manifest` and the migration logic.

### Consumer scripts
All readers/writers updated to use the canonical `agent/` path with a legacy-root fallback through `find_pack_manifest` (manifest only — the other two helpers are canonical-only since they never collided):
- `scaffold.py`, `validate.py`, `package.py`, `clean.py`, `generate_description.py`
- `agent-studio-install/scripts/install.py` (both `source_info_from_current_pack` and `read_current_pack_preview`)
- `agent-studio-share/scripts/run_share.py`

### Docs
`AGENTS.md` / `SKILL.md` / `references/*.md` / `agent-studio-install/SKILL.md` updated to point at the new paths; misc trim of narrating prose to reduce model-side tokens.

## Affected workspaces
- **No manual recovery needed.** On the first dev-mode session after this ships, `migrate_manifest.py` recovers the lost manifest from `git show HEAD:agent-pack.yaml` (the two prod bots both have it in HEAD).
- Workspaces still on the legacy layout but not yet clobbered keep working via the helper's fallback; migration moves them to `agent/` on next session.

## Review history
13 commits, head `69283fd`. Two independent agent reviewers (Claude + Codex) ran in three rounds; converged on no remaining issues. Key fixes surfaced by review:
- Round 1: `run_share.py` was reading root manifest → patched (was the symmetric miss of `install.py`)
- Round 2: `find_pack_manifest`'s name-guard was looser than the migration's → aligned
- Round 3: docstrings synced

## Test plan — local smoke ✅

All scenarios run against an isolated `mktemp` workspace with the branch HEAD scripts:

- [x] **Fresh scaffold**: `scaffold.py --name foo --output .` → creates `agent/agent-pack.yaml`; root `agent-pack.yaml` NOT created
- [x] **Legacy workspace validates via fallback**: minimal pack with manifest at root → `validate.py` structure check reports `4/4 required files present` (find_pack_manifest fallback resolves the root manifest as the user pack)
- [x] **Helper refuses Agent Studio's own manifest at root**: `find_pack_manifest` returns `None` when root `agent-pack.yaml` has `name: agent-studio` (no false-positive recovery)
- [x] **Migration recovers from git HEAD** (the headline scenario for the affected prod bots):
  ```json
  {"file": "agent-pack.yaml", "action": "restored_from_git",
   "source": "HEAD:agent-pack.yaml", "to": "agent/agent-pack.yaml",
   "pack_name": "clobbered-pack"}
  ```
  Live root stayed `name: agent-studio` (Agent Studio's manifest untouched); `agent/agent-pack.yaml` populated with the user's pack.
- [x] **package.py archive layout unchanged**: archive root contains `agent-pack.yaml`, `AGENTS.md`, `IDENTITY.md`, `SOUL.md` — passes `assert_archive_layout`
- [x] **clean.py only sweeps `agent/`**: deletes `agent/agent-pack.yaml`; live root `agent-pack.yaml` (Agent Studio's) untouched after `/studio new`

## Test plan — staging / prod (needs deploy)

- [ ] **End-to-end migration on real affected bot**: ship this image to bot `4baa8c76` and/or `f7bd58dc`, restart pod, observe `migrate_manifest.py` output in next dev-mode session, confirm `agent/agent-pack.yaml` populated with user's `amazon-research-frankkk` manifest
- [ ] **`/studio share` and `/studio install --source current`** on a migrated workspace (was the round-1 review catch — exercises the `run_share.py` patch)
- [ ] **Agent Studio update on a freshly scaffolded workspace** (post-deploy) — confirm new layout survives a re-install of Agent Studio (no clobber)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
