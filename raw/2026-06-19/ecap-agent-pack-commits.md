# ecap-agent-pack commits — 2026-06-19

共 3 个 commit

---

## `2991c5351f`

- **作者**: felix-srp
- **日期**: 2026-06-19T15:30:45Z
- **PR**: #182
- **链接**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/2991c5351f34dc04b46c23d821a391bf1ad39b80

### 完整 commit message

```
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
```

### PR Description

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

---

## `26cbf11e7d`

- **作者**: felix-srp
- **日期**: 2026-06-19T07:50:27Z
- **PR**: #181
- **链接**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/26cbf11e7d7ba500120808373295c72666104f6b

### 完整 commit message

```
fix(agent-studio): harden publish flow + unify quick_commands parser with validate (v1.7.2) (#181)

* fix(agent-studio): harden publish.py YAML parsing + backend-response handling

Follow-up review of publish.py (from #177) surfaced four issues:

1. strip_yaml_scalar truncated quoted scalars containing ` #`: comment-
   stripping ran before quote handling, so a quick_command label/prompt like
   `"summarize the #1 item"` or `"找 #话题 趋势"` was cut at the `#` (and a
   single-quoted value even kept its opening quote). These values ship in the
   Pack Store submission body. Now quotes are decoded first; comments are only
   stripped from unquoted scalars; single-quoted `''` escaping is handled.
2. start_publish reported a failed/timed_out run as status "pending" (reads as
   "still working"). Now mapped to "error" and the failure_code/failure_summary
   are surfaced in the payload.
3. submit_publish accessed backend fields with `[...]`, so a malformed response
   raised a bare KeyError → traceback on stdout, breaking the JSON contract the
   Studio parses. Added a require_field helper (asset_id, submission_id,
   pack_id, test_run_id) and a KeyError backstop in main().
4. parse_quick_commands silently returned [] for non-empty inline/flow style,
   shipping empty quick_commands. Now fails loud, requiring block style.

Added 6 tests (quoted-hash preservation incl. single-quote escaping, failed-run
status, missing-asset_id clean error, inline-list rejection). Full suite green
(124 scripts tests). Bump 1.7.1 → 1.7.2.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(agent-studio): publish.py terminal-status mapping + non-object responses (review round 1)

Two-reviewer round 1 (Claude + Codex):

- Claude: _overall_start_status returned "pending" for the terminal "cleaned"
  and "promoted" states (both in TERMINAL_PREVIEW_STATUSES). "pending" tells the
  caller to keep polling, so a cleaned/expired run would loop forever. Map
  cleaned → "error" and promoted → "ok"; every terminal state now resolves to
  ok/error.
- Codex: a valid-but-non-object JSON response ([], "str", 42) passed json.loads
  then hit .get() → uncaught AttributeError, escaping main()'s JSON contract.
  Added parse_json_object() (rejects non-dict) and routed both BackendClient
  and R2 upload responses through it.

Added tests for the full status mapping and non-object/invalid response
rejection (incl. a BackendClient._send path). 129 scripts tests pass.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(agent-studio): guard remaining non-dict/non-string response paths (review round 2)

Codex round 2 found three more instances of the same malformed-response class
fixed for the HTTP clients in round 1:

- run_package parsed package.py stdout raw — a non-object payload reached
  `.get()` (AttributeError) and a non-string `archive` reached Path(...)
  (TypeError). Now validates the payload is a dict and `archive` a non-empty
  string before returning.
- get_or_create_pack iterated the packs list and called `.get()` on each entry;
  a null element → AttributeError. Now skips non-dict entries.

Claude round 2 found no issues. Added tests for non-object/non-string-archive
package output and null pack entries. 133 scripts tests pass.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* refactor(agent-studio): simplify single-quoted YAML scalar parsing

/simplify pass: replace the 16-line hand-rolled `_single_quoted_end` scanner
with a one-line regex (`'((?:[^']|'')*)'`) that encodes the same rule — runs of
non-quote chars or escaped `''`, up to the closing quote. Behavior-preserving;
all 23 publish tests pass (escaping, ` #` preservation, trailing comments,
malformed no-close).

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* refactor(agent-studio): share one quick_commands parser between validate and publish

/simplify follow-up — fix the architectural findings instead of deferring them.

The publish gate (validate.py) and the shipper (publish.py) each had their own
quick_commands block parser, and they had DIVERGED: validate requires
double-quoted JSON text fields, while publish's `strip_yaml_scalar` also
accepted bare and single-quoted scalars. So publish could serialize a shape the
validator would have rejected.

- Move the canonical parser into `_common.py` (the shared home):
  `decode_quoted_scalar`, `resolve_id_scalar`, `quick_commands_section_lines`,
  `parse_quick_commands_block`, plus the block-error message constant.
- validate.py drops its four private copies and imports the shared ones —
  behavior unchanged (all 104 skill tests pass).
- publish.py drops its forked parser + `strip_yaml_scalar` and uses the shared
  one, so it now enforces the same double-quoted contract as the gate. The
  ` #`-inside-double-quotes correctness is retained (validate's raw_decode).
- Route `create_test_run`'s inline key check through `require_field` for
  consistency.

Tests updated: the fixture now uses canonical double-quoted fields; added cases
proving publish preserves ` #` in double quotes and rejects non-double-quoted
fields (matching validate). 131 scripts + 104 skill tests pass.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(agent-studio): publish enforces quick_commands semantic checks too (review round 1)

Codex review of the parser-sharing refactor: publish.py shared validate's
*structural* parse but not its *semantic* checks, so a structurally-valid block
missing required fields (label_cn/prompt), with a non-kebab id, or a duplicate
id would still be shipped — the divergence wasn't fully closed.

- Extract validate's semantic loop into `_common.quick_commands_semantic_issues`
  (id presence/kebab/uniqueness, required non-empty text fields). The
  >4-actions and absent-slot *warnings* stay caller policy.
- validate.py calls it (behavior unchanged — 104 skill tests pass).
- publish.py runs it after the structural parse, so the shipper now rejects
  exactly what the gate rejects.
- Fix the test fixture's invalid id `all_features` → `all-features` (underscore
  isn't lower-kebab-case; the old fixture would have failed validate). Added a
  test for the semantically-incomplete block.

Claude review found no issues. 132 scripts + 104 skill tests pass.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* refactor(agent-studio): share quick_commands header classifier; drop redundant ok flag

/simplify follow-up on the parser-sharing refactor.

- The `quick_commands:` header ladder (find headers, multiple-check, inline `[]`
  check, inline-garbage check) was still copy-pasted in validate.py and
  publish.py — the last must-not-diverge piece the parser-sharing left behind.
  Extract `classify_quick_commands(manifest) -> (kind, section_lines)` into
  `_common.py`; both callers switch on `kind` and apply their own policy
  (validate: warn/pass/fail; publish: raise/[]). The header regex now has a
  single source of truth.
- `decode_quoted_scalar` returned `(value, ok)` where `ok` was just
  `value is not None` — collapse to `str | None`, which removes the redundant
  flag and the `value is not None` guards (and keeps the type checker happy).
- Drop the now-unused `import re` from publish.py.

validate behavior unchanged (104 skill tests pass); 132 scripts tests pass.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

Follow-up to #180: a review of `publish.py` (introduced in #177), hardened through two-reviewer convergence loops and `/simplify` passes. Two thrusts: (A) make the Pack Test / Pack Store publish flow robust against malformed input, and (B) eliminate a divergent, duplicated quick_commands parser between the validate gate and the publish shipper.

## A. Publish-flow robustness

1. **`strip_yaml_scalar` corrupted quoted values containing ` #`** — comment-stripping ran before quote handling, truncating `"summarize the #1 item"` / `"找 #话题 趋势"` (which ship in the submission). *(Subsumed by the shared parser in B.)*
2. **Failed runs reported as `pending`** — `start_publish` now maps every terminal status (`failed`/`timed_out`/`cleaned` → `error`, `promoted` → `ok`) and surfaces `failure_code`/`failure_summary`. A terminal-but-dead run no longer reads as "keep polling."
3. **Uncaught exceptions on malformed responses** — `require_field` + `parse_json_object` (rejects non-object JSON from both the backend and R2 clients) + a `KeyError` backstop in `main()`. `run_package` validates package.py's payload (dict + non-empty string `archive`); `get_or_create_pack` skips `null` packs entries. Malformed external data now surfaces as a clean `PublishError`, never a traceback that breaks the JSON-stdout contract.
4. **`parse_quick_commands` silently dropped inline-list style** — now fails loud.

## B. Unify the quick_commands parser (validate ↔ publish)

`validate.py` (the gate) and `publish.py` (the shipper) each had their own quick_commands parser, and they had **diverged** — validate required double-quoted text fields + enforced semantic rules; publish accepted bare/single-quoted and skipped semantic checks. So publish could ship a shape validate rejects. Consolidated the entire pipeline into `_common.py`, consumed identically by both:

- `classify_quick_commands` — header classification (absent / multiple / `[]` / inline-garbage / block), single source of truth.
- `parse_quick_commands_block` + `decode_quoted_scalar` / `resolve_id_scalar` — structural parse (double-quoted text fields, ` #` preserved inside quotes).
- `quick_commands_semantic_issues` — id presence/kebab/uniqueness + required non-empty fields.

Now the shipper rejects exactly what the gate rejects, structurally and semantically. `create_test_run`'s key check also routes through `require_field`.

## Review

Reviewed clean by both a Claude reviewer and a Codex reviewer after each stage: original review, robustness loop (3 rounds), parser-sharing refactor (2 rounds), semantic enforcement (2 rounds), and the header-classifier extraction (1 round). `validate.py`'s behavior is provably unchanged — its **104 skill tests pass after each refactor**.

## Tests

Publish suite grew from 8 → 22 focused cases. Full suite green: **132 scripts + 104 skill tests**. Version bump **1.7.1 → 1.7.2**.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## `e04fba5129`

- **作者**: felix-srp
- **日期**: 2026-06-19T05:37:57Z
- **PR**: #180
- **链接**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/e04fba5129e9662e27ea373e0b79a77fa565ba1e

### 完整 commit message

```
fix(agent-studio): normalize skill paths to .agents/skills/ at packaging (v1.7.1) (#180)

* fix(agent-studio): rewrite skill paths to .agents/skills/ at packaging

Agent docs invoke a pack's skill scripts by literal shell path. In the dev
workspace a skill lives at `skills/<name>/`, but package.py relocates it to
`.agents/skills/<name>/` in the archive (and that's where it lands on the
installed pod). Packaging moved the files but never rewrote the path strings
in AGENTS.md/HEARTBEAT.md/etc., so a `skills/<name>/...` reference shipped
verbatim and silently broke at runtime (no top-level `skills/` on the pod).
amazon-analyst and stock-analyst shipped with this exact bug; validate.py
accepts both prefixes, so it passed unnoticed.

Fix it deterministically at the packaging boundary — the same place that
relocates the files — via `_rewrite_skill_paths`: normalize `skills/<name>/`
to `.agents/skills/<name>/` in the packed agent docs, scoped to real skill
directory names. Token-boundary lookbehinds leave already-correct
`.agents/skills/`, nested `../skills/`, `~/.openclaw/skills/`, and the
top-level pack `scripts/` untouched.

The dev source is never mutated: `/dev` and `/test` keep resolving the
`skills/<name>/` paths because the files are there in the workspace; only the
archived copy is rewritten. Stage 3a guidance updated to say so (author the
dev path, packaging converts it). The manifest's openclaw-resolved
`onboarding.*.script:` fields stay `skills/<name>/...`.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* refactor(agent-studio): simplify skill-path rewrite to unconditional + trim docs

Cleanup pass on the packaging rewrite:

- Drop the name-scoped alternation (and the `skill_names` set computed in
  main() + threaded through `_clean_agent_file`). Rewrite `skills/<seg>/`
  unconditionally at a token boundary instead. This is simpler (no per-pack
  skill list, no longest-first sort) and strictly more correct: it now also
  catches templated segments like `skills/{skill_name}/` — the actual
  amazon-analyst case the name-scoped version silently left broken.
- Precompile the regex once at module level (`_SKILL_PATH_RE`) rather than
  rebuilding it per agent doc.
- Collapse the 14-line docstring to a tight comment; trim the automation.md
  guidance paragraph (Studio-loaded reference doc — fewer runtime tokens).

False-positive surface verified empty against real SOP lines: bare prose
("the skills/ folder"), top-level `scripts/`, and nested `.agents/skills/` /
`../skills/` / `~/.openclaw/skills/` references are all left untouched.
210 tests pass; e2e packaging confirmed end to end.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(agent-studio): harden skill-path regex + fix inert test (review round 1)

Two reviewers (Claude + Codex) flagged:

- Codex: `./skills/<x>/` (relative-prefix dev path) was not rewritten — the
  lookbehind blocked the leading `.`. Now matches an optional `./` prefix.
- Claude: segment class `[^/\s]+` could swallow a `)` (e.g. `skills/foo)/…`),
  producing an invalid `.agents/skills/foo)/…`. Restricted the class to real
  skill-dir name chars `[\w.{}-]+` (covers kebab names and `{skill_name}`
  templates) so a stray `)`/backtick can't be absorbed.
- Claude: the AGENTS.md test asserted `assertNotIn("` skills/...")` — a string
  that never appears in the input, so it couldn't catch a no-op rewrite.
  Replaced with `assertNotIn("uv run skills/", ...)`.
- Codex: my refactor made the SOUL.md `rstrip()` fire on rewrite-only changes,
  not just footer removal. Gated it back to footer removal so unrelated
  trailing whitespace is preserved.

Added tests for the `./` prefix, the `)` non-corruption case, and the SOUL.md
rewrite-only path. 109 scripts tests pass.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(agent-studio): reject traversal segment in skill-path regex (review round 2)

Codex round-2 review: the segment class `[\w.{}-]+` admitted dots, so
`skills/../scripts/x.py` matched (segment `..`) and rewrote to
`.agents/skills/../scripts/x.py`, escaping the skills subtree. Real skill dir
names are `[a-z0-9-]` (scaffold-enforced) and never contain dots, so the dot
was over-broad — dropped it (`[\w{}-]+`). This rejects both `skills/../` and
`skills/./` while keeping every real name and the `{skill_name}` template.
Added a traversal-segment test. Claude round-2 review found no issues.

110 scripts tests pass.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* chore(agent-studio): bump version 1.7.0 → 1.7.1

Packaging fix: skill paths in agent docs are normalized to the deployed
`.agents/skills/<name>/...` layout at packaging time.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## Problem

Agent docs invoke a pack's skill scripts by **literal shell path**. In a Studio dev workspace a skill lives at `skills/<name>/`, but `package.py` relocates it to `.agents/skills/<name>/` in the published archive — which is where it lands on the installed pod. Packaging moved the *files* but never rewrote the *path strings* in `AGENTS.md` / `HEARTBEAT.md` / etc., so a line like:

```
uv run skills/knowledge-qa/scripts/query_kb.py
```

shipped verbatim and **silently broke at runtime** (there is no top-level `skills/` on the pod).

Not isolated: `amazon-analyst` and `stock-analyst` shipped with this exact bug (the latter also via a templated `skills/{skill_name}/...` path). `validate.py` accepted *both* prefixes, so the broken form passed validation unnoticed.

## Fix

Normalize deterministically at the packaging boundary — the same place that already relocates the files — in `_clean_agent_file` via:

```python
_SKILL_PATH_RE = re.compile(r'(?<![\w./\-])(?:\./)?skills/([\w{}-]+)/')
```

- Rewrites `skills/…`, `./skills/…`, and templated `skills/{skill_name}/…` → `.agents/skills/…` in the packed agent docs.
- Excludes already-correct `.agents/skills/`, nested `../skills/` and `~/.openclaw/skills/`, the top-level pack `scripts/`, bare prose (`the skills/ folder`), traversal segments (`skills/../`), and won't swallow a stray `)`/backtick into the skill name.
- Segment class is the scaffold-enforced skill-name set (`[a-z0-9-]`, plus `{}` for templates) — no dots.

### Dev/test is unaffected

The dev source is **never mutated** — `_clean_agent_file` reads the source and writes the rewritten copy into the archive staging dir only. `/dev` and `/test` keep resolving `skills/<name>/` (the files are there in the workspace); only the archived copy is rewritten.

| Stage | path in AGENTS.md | file location | resolves |
|------|------|------|------|
| `/dev` `/test` | `skills/<name>/...` (source untouched) | `skills/<name>/...` | ✅ |
| packaging | rewritten in archive copy → `.agents/skills/<name>/...` | archive `.agents/skills/...` | ✅ |
| installed pod | `.agents/skills/<name>/...` | pod `.agents/skills/...` | ✅ |

Stage 3a guidance (`references/automation.md`) updated to match: author the **dev path** `skills/<name>/...` (so `/test` works); packaging converts it. The manifest's openclaw-resolved `onboarding.*.script:` fields stay `skills/<name>/...` (manifest is added raw, never rewritten).

## Review & hardening

Hardened over 4 adversarial review rounds (Claude + Codex each round); 5 issues found and fixed, then **two consecutive clean rounds**:
- `[^/\s]+` could swallow `)` and corrupt the path → restricted segment class
- `./skills/<x>/` relative prefix wasn't rewritten → optional `./` prefix
- `skills/../<x>/` traversal segment got rewritten (escaped the subtree) → dropped dot from segment class
- SOUL.md `rstrip()` over-fired on rewrite-only changes → gated back to footer-removal only
- an inert test assertion that couldn't catch a no-op rewrite → replaced with a meaningful one

## Tests

12 focused cases in `scripts/tests/test_package_agent_md.py` (literal/`./`/templated rewrites, `)` non-corruption, traversal rejection, exclusions, SOUL trailing-whitespace preservation). Full suite green: `scripts/tests` 110 passed, `tests` 104 passed. End-to-end packaging verified the archived AGENTS.md contains the rewritten paths with all exclusions honored.

Version bumped **1.7.0 → 1.7.1**.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
