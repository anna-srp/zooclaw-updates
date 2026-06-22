---
title: "修复多个 Agent Pack 技能路径错误导致技能在线上静默失效"
type: "Skill 上架/更新"
priority: "中"
date: "2026-06-19"
status: "待审核"
channels: "Discord+changelog"
---
# 修复多个 Agent Pack 技能路径错误导致技能在线上静默失效
## 核心宣传点
修复 amazon-analyst、stock-analyst、tvc-studio、leofit 等多个 Agent Pack 因文档里技能调用路径写成 skills/ 而非 .agents/skills/，导致技能在 Pod 上静默失效的问题，并相应升级补丁版本，让这些智能体的技能恢复正常可用。
## 原始内容
fix(packs): correct shipped skill paths + .agents/skills script root depth (#182)

* fix(packs): normalize skill paths to .agents/skills/ in shipped agent docs

Same class of bug PR #180 fixed for the agent-studio packaging boundary, but
in the packs shipped straight from this repo. CI's agent_release.py zips each
pack directory as-is (no skills/ -> .agents/skills/ relocation, no path
rewriting), so the committed docs are exactly what runs on the pod. Skills
live at .agents/skills/<name>/, but several packs' agent docs invoked them by
the literal shell path skills/<name>/... — which doesn't exist on the pod, so
it silently broke at runtime.

Fix: rewrite skills/<name>/ -> .agents/skills/<name>/ in the prose/shell-
invocation docs only, using the exact normalization from PR #180. The
manifest (agent-pack.yaml) keeps skills/<name>/ — those fields are
openclaw-resolved and added raw, never rewritten.

Packs fixed (+ patch version bump so clients pick them up):
- amazon-analyst  1.0.0 -> 1.0.1  (AGENTS.md, templated {skill_name})
- stock-analyst   0.3.0 -> 0.3.1  (AGENTS.md, TOOLS.md)
- tvc-studio      0.3.9 -> 0.3.10 (AGENTS.md)
- leofit          4.2.2 -> 4.2.3  (AGENTS.md, TOOLS.md)

Not addressed here (pre-existing staleness, separate from this path bug):
- leofit references a fit-challenge skill and a scripts/test.sh (shared/,
  fitpack-router) that don't exist on disk; a prefix fix can't make those
  resolve.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(leofit): repair incomplete .agents/skills migration (runtime broken)

The v4.2.1 -> 4.2.2 migration moved skills from top-level skills/<name>/ to
.agents/skills/<name>/ and deleted the top-level shared/ module, but never
updated the scripts. As shipped, leofit v4.2.2 was broken at runtime:

- Every skill script computed WORKSPACE = dirname x3, which from the new
  .agents/skills/<name>/<script>.py location resolves to .agents/ instead of
  the pack root. So DATA_DIR pointed at a non-existent .agents/data/, and
  fit-exercises / fit-planner could not find the seed exercise DB. Fixed to
  dirname x4 (pack root), matching where data/ actually lives. Verified:
  index.json, muscle-maps, and gen_muscle_map paths now resolve.

- fit-coach/coach.py and fit-planner/planner.py did
  `from shared.utils import normalize_goal`, but shared/ was deleted ->
  ModuleNotFoundError. normalize_goal was the ONLY symbol any script ever
  imported from shared (true in v4.2.1 too); inlined it into both scripts
  (parity-tested against the original). The other shared modules
  (database/models/calculations.py) were never imported by any script.

Doc + dead-code cleanup from the same migration:
- TOOLS.md: dropped the "Shared Python Modules" table (deleted modules,
  never imported), the fit-challenge row + "Challenge Templates" section +
  "Challenge data" path (no such skill exists), .
- AGENTS.md: onboarding referenced a `leofit-init` skill; the actual skill is
  `fitpack-init`.
- Removed scripts/{install,uninstall,test}.sh — legacy manual-install helpers
  referencing a pre-migration workspace/skills/ + shared/ + fitpack-router
  layout that no longer exists; not referenced by the manifest or docs.

Verified locally: all 9 scripts py_compile; coach.py runs (was crashing);
planner.generate_plan reads the exercise DB and builds a plan. Could not
verify on a live pod. Version 4.2.3 -> 4.2.4.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(zoo-buddy,tvc-studio): correct skill-script root depth after .agents/skills move

Same migration-class bug as leofit: scripts anchor a pack-root path off
__file__ but the dirname/`..` depth wasn't increased when skills moved into
.agents/skills/<name>/scripts/, so the computed root lands on .agents/ instead
of the pack root.

- zoo-buddy pack-onboarding provision.py + finalize.py: BASE used dirname x4
  (-> .agents), so config.json was written to .agents/data/ while AGENTS.md
  checks the sentinel at data/config.json -> onboarding never registered as
  complete and re-triggered every session. Fixed to dirname x5 (pack root).
- tvc-studio tvc-post/fetch_bgm.py: WORKSPACE_ROOT went up 3 levels (-> .agents),
  so the default data/bgm/* and data/bgm-r2/catalog.jsonl paths pointed into a
  non-existent .agents/data/ (data/bgm-r2/ lives at the pack root). Fixed to 4
  levels. (Masked only when invoked with explicit --index/--bgm_dir.)

Verified: BASE/WORKSPACE_ROOT == pack root for all three; scripts py_compile.
zoo-buddy 0.1.0 -> 0.1.1; tvc-studio stays 0.3.10 (already bumped this PR).

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* refactor(leofit): drop redundant priority-list literal in normalize_goal

The inlined normalize_goal repeated goal_map's keys as a separate priority
list; the dict literal already encodes that order (insertion-ordered on
py3.12). Iterate goal_map directly — removes the duplicated list and the risk
of the two drifting. Behavior-identical (parity-tested).

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(leofit): restore shared/calculations.py (deterministic math layer)

The .agents/skills migration deleted shared/, but 6 SKILL.md files still
instruct the LLM to `from calculations import calc_targets/get_pr/append_weight/
days_since_last_training/plan_age_days` (BMR/TDEE/targets, PR detection, weight
history, training gap). On the pod that import failed and the model fell back to
inline LLM math — the exact anti-pattern the deterministic layer exists to avoid.

Restore the module verbatim from v4.2.1 (043b48d). It's self-contained
(stdlib only) and its WORKSPACE = dirname x2 correctly resolves to the pack root
from <root>/shared/calculations.py, so DATA_DIR -> <root>/data. Verified the
SKILL.md import idiom end to end: sys.path.insert(WORKSPACE/shared) +
`from calculations import ...` resolves, all referenced symbols present,
calc_targets returns {bmr,tdee,calorie_target,protein_g,carb_g,fat_g,bmi}.

Only calculations.py is restored — database/models/utils.py stay deleted (no
script or doc references them; normalize_goal was already inlined). 4.2.4 -> 4.2.5.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(leofit): make SKILL.md calculations imports self-contained

After restoring shared/calculations.py, four SKILL.md snippets still showed a
bare `from calculations import ...` without the sys.path setup (fit-logger,
fit-profile, fit-remind) or omitted `import os` (fit-planner). Propagate the
same preamble fit-nutrition already uses so each snippet imports the
deterministic module reliably instead of risking an inline-math fallback:

    import sys, os
    sys.path.insert(0, os.path.join(WORKSPACE, 'shared'))
    from calculations import ...

Consistency-only (matches the in-pack working pattern); no new convention.
4.2.5 -> 4.2.6.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(leofit): point CRON_FILE at ~/.openclaw/cron/jobs.json

remind.py derived the cron path as WORKSPACE/../../../cron/jobs.json. That
relative offset was calibrated against the old (shallower, broken) WORKSPACE;
after the dirname depth fix it resolved even further above ~/.openclaw, so
reminder setup/teardown read/wrote the wrong jobs.json and silently no-op'd.

Replace the fragile relative walk with the absolute location the platform
actually uses (matches the working restaurant-review-monitor pack:
~/.openclaw/cron/jobs.json). Decouples it from pack-root depth entirely.
4.2.6 -> 4.2.7.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* Revert all leofit changes — stale/unmaintained agent, out of scope

leofit is no longer maintained, so it shouldn't be touched by this PR. Revert
the entire pack (skill-path doc rewrites, migration/runtime repair, normalize_goal
inline, restored shared/calculations.py, SKILL.md edits, CRON_FILE, version bump,
and the deleted legacy scripts) back to main. The pre-existing runtime/domain
bugs in leofit are left as-is by design.

This PR now covers only the maintained packs: amazon-analyst, stock-analyst,
tvc-studio, zoo-buddy.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

## PR Description
Fixes for packs shipped straight from this repo. CI's `.github/scripts/agent_release.py` **zips each pack directory as-is** (no `skills/` → `.agents/skills/` relocation, no path rewriting), so the committed tree is exactly what runs on the pod.

> **Note:** an earlier revision of this PR also repaired `leofit`, but leofit is a stale/unmaintained agent and has been reverted out entirely. This PR now touches only maintained packs.

## 1. Skill-path normalization in shipped agent docs

PR #180 fixed broken skill paths at the agent-studio **packaging** boundary — that helps Studio users packaging their own packs, but not the packs committed here. Skills live at `.agents/skills/<name>/`, but several packs' agent docs invoked them by the literal shell path `skills/<name>/...`, which doesn't exist on the pod → silent runtime breakage.

Fix: rewrite `skills/<name>/` → `.agents/skills/<name>/` in the prose / shell-invocation docs only, using PR #180's exact regex. The manifest (`agent-pack.yaml`) keeps `skills/<name>/` — those fields are openclaw-resolved and added raw, never rewritten.

## 2. Skill-script root-depth fix (`.agents/skills/` migration fallout)

Scripts anchor a pack-root path off `__file__`, but the `dirname`/`..` depth wasn't increased when skills moved into `.agents/skills/<name>/scripts/`, so the computed root lands on `.agents/` instead of the pack root:

- **zoo-buddy** `provision.py` + `finalize.py`: `dirname×4` (→ `.agents/`) wrote `config.json` to `.agents/data/`, but `AGENTS.md` checks the onboarding sentinel at `data/config.json` → onboarding never registered, re-triggered every session. → `dirname×5`.
- **tvc-studio** `tvc-post/fetch_bgm.py`: `WORKSPACE_ROOT` went up 3 levels (→ `.agents/`), so default `data/bgm/*` + `data/bgm-r2/catalog.jsonl` pointed into a non-existent `.agents/data/` (`data/bgm-r2/` is at the pack root). → up 4. (Masked only when called with explicit `--index`/`--bgm_dir`.)

> Audited all packs for this depth bug; **coros-coach** uses `join(SCRIPT_DIR, "..","..","..","..")` correctly and was left untouched.

## Versions

| Pack | Change | Version |
|---|---|---|
| amazon-analyst | §1 | 1.0.0 → 1.0.1 |
| stock-analyst | §1 | 0.3.0 → 0.3.1 |
| tvc-studio | §1 + §2 | 0.3.9 → 0.3.10 |
| zoo-buddy | §2 | 0.1.0 → 0.1.1 |

## Verification (local)

zoo-buddy/tvc-studio: `BASE`/`WORKSPACE_ROOT` resolve to the pack root; scripts `py_compile`. All rewritten doc paths resolve to real files. Not verified on a live pod.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
