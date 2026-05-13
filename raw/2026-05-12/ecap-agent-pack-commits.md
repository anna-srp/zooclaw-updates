# ecap-agent-pack Commits — 2026-05-12

## a6da8fd5928b
- **Author:** felix-srp
- **Date:** 2026-05-12T09:37:56Z

### Commit Message

```
feat(agent-studio): publish/install/share hardening + Stage 5/6 split (v1.1.0) (#118)

* fix(agent-studio): prevent hand-crafted publish archives shipping Agent Studio identity

When the LLM driving /studio publish bypassed publish.py and ran a raw
tar/npm-pack against the workspace, the resulting archive carried the
Studio workspace's own root SOUL.md/IDENTITY.md/AGENTS.md plus the
unstripped agent/ subdirectory. Once deployed as a custom agent, that
shape made the new bot greet users as Agent Studio (in DEV mode for the
agent they thought they were running).

This change:

- publishing.md: adds a CRITICAL block forbidding ad-hoc archivers and
  documents the exact forbidden layout for sanity-checking outputs.
- SKILL.md: restates the constraint on the /studio publish command entry.
- publish.py: self-checks the produced tar.gz against the install-time
  contract (no top-level agent/, skills/, or package/; agent-pack.yaml
  present at root) and surfaces a JSON error if the contract breaks,
  deleting the malformed archive instead of silently shipping it.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(agent-studio): tighten publish.md and SKILL.md prose

Trim the publish guardrails added in 34ae5ae: the CRITICAL block, layout
diagram, and forbidden-layout checklist were verbose for what is now a
single rule ("use publish.py only") with the WHY ("workspace root .md
is Agent Studio's"). The structural rejects (top-level agent/skills/
package/) are enforced by publish.py's self-check, so prose doesn't need
to enumerate byte fingerprints or recapitulate the layout map.

Roughly 60% token reduction on the new content, same runtime directive.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(agent-studio): stitch share/install into Stage 5 + layer model + harden share

The share and install skills (added in #103) bridged the gap from
"tar.gz exists" to "agent loaded in account", but the narrative layer
never caught up:

- Stage 5f (publishing.md) still pointed creators at the manual
  AI Specialists upload, ignoring /studio install entirely. Replace with
  layered next-steps: install (self) → share (others) → manual fallback.
- Main SKILL.md treated publish/share/install as parallel sibling
  commands. Add a "layered, not parallel" preamble before the command
  list so the LLM has the right call-graph mental model.
- agent-studio-share's "package first through the existing Agent Studio
  publisher" was vague enough to license a hand-crafted tar fallback —
  the same shape we just fixed in publish.py. Replace with an explicit
  reference to publish.py and the §5e rule.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(agent-studio-install): preflight gate + actionable token guidance

- Add a pre-flight rule for /studio install --source current: require
  description.json (not just agent-pack.yaml). Without it the install
  succeeds but produces a half-baked catalog card; route the creator
  back to Stage 5a instead.
- Rewrite the USER_INTERNAL_TOKEN error message. The old wording asked
  the creator to "set" the token, but it's injected by the OpenClaw
  runtime — the creator can't set it from chat. Reframe as a platform
  config issue with a clear escalation path.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor(agent-studio): split publishing into Stage 5 (Packaging) + Stage 6 (Delivery)

Previously Stage 5 conflated two concerns: producing the tar.gz and
deploying it. /studio install (added in #103) made delivery a first-class
step, but it stayed buried under 5f as "what's next" with a manual-upload
fallback that was actually the entry point for the bad-tar.gz bug.

This commit splits them:

- Stage 5 (Packaging): 5a–5f end with the pack on disk and a GATE that
  asks install / share / stop. Drops the manual-upload fallback —
  /studio install is the canonical deployment path; if it errors,
  fix the error rather than retreating to a riskier path.
- Stage 6 (Delivery, new): 6a install, 6b share, 6c reserved. Lives in
  references/delivery.md and routes to the existing install/share
  skills without duplicating their procedures.
- Main SKILL.md "Current stage" resume heuristic adds two new states:
  archive missing → Stage 5; archive present, no deploy → Stage 6.

The split makes "package without deploying" a legitimate end state
(e.g. hand the tar.gz to a coworker out-of-band) and gives the LLM a
real gate between artifact creation and deployment.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor(agent-studio): rename publishing.md → packaging.md to match Stage 5

After splitting Stage 5 (Packaging) and Stage 6 (Delivery), the
"publishing" name only fits the old conflated meaning. Rename the
reference file and heading to match the Stage 5 scope (artifact
production, no deployment).

Updates all in-tree references: main SKILL.md (2x), delivery.md (1x),
agent-studio-share/SKILL.md (1x), and a stale comment in publish.py.

Not renamed (out of scope for now; flagged in conversation):
- /studio publish slash command (user-facing, still reasonable).
- publish.py script (imported by run_share.py + install.py; cost > benefit).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(agent-studio): redefine /studio publish as Stage 5 + 6 orchestrator

The §5f gate already routes creators into Stage 6, so /studio publish
was de-facto an end-to-end command — but the doc still described it as
Stage 5 only. Make the orchestrator vs shortcut relationship explicit:

- /studio publish = end-to-end (Stage 5 packaging → §5f gate → Stage 6
  install/share/stop per creator choice). Matches the natural English
  meaning of "publish" (produce + make available).
- /studio install = shortcut to Stage 6a (skip Stage 5 when a pack
  already exists in zip/).
- /studio share = shortcut to Stage 6b.

The publish.py script keeps its narrow scope (packaging primitive); only
the slash command grows to cover end-to-end. No code changes.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(agent-studio): add /studio package for Stage-5-only entry point

After renaming Stage 5 to "Packaging" and redefining /studio publish as
end-to-end (Stage 5 + 6), there was no command whose name matched the
new stage name. Creators who only want a tar.gz had to run /studio
publish and pick "stop" at the §5f gate — an extra interaction for a
real use case (artifact to email or hand off out-of-band).

Add /studio package as the Stage-5-only entry point:

- /studio package → runs 5a–5e, stops at "pack ready", no §5f gate.
- /studio publish → unchanged; same packaging then §5f gate into Stage 6.

The §5f section in packaging.md branches on entry point — package stops,
publish gates. Both share the same packaging rules; only the post-pack
behavior differs.

This restores command/stage name symmetry: package↔Packaging,
publish↔end-to-end, install↔Stage 6a, share↔Stage 6b.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(agent-studio): sync root AGENTS.md, BOOTSTRAP.md, share SKILL.md to 6-stage model

PR #118 split Stage 5 into Packaging + Delivery and added /studio package
as a stage-5-only command, but two session-startup files still taught the
old 5-stage pipeline:

- AGENTS.md (root) — command table missed /studio package entirely;
  /studio publish description still said "Package the agent" (old
  semantics); /studio install/share descriptions didn't reflect their
  shortcut-into-Stage-6 role.
- BOOTSTRAP.md — first-run greeting taught new creators "5 stages:
  Discovery → ... → Publishing".

Both are read at session start (alongside .agents/skills/agent-studio/
SKILL.md), so leaving them stale meant the LLM ingested two contradicting
command tables and an outdated pipeline on every run.

Also cleans up agent-studio-share/SKILL.md "Fixed flow" — the old listing
mixed agent actions with run_share.py's internal behavior, which could
mislead an LLM into re-implementing those steps by hand (defeats PR
#118's hand-crafted-tar guard). The flow now has two agent actions; the
internal behaviors live in a separate explanatory subsection.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(agent-studio): record review follow-ups from PR #118

A full review of Agent Studio (during PR #118) surfaced ~12 issues that
are out of scope for this PR — pre-existing bugs (clean.py not clearing
zip/), gaps that need a code change (install.py description.json gate,
post-install identity verification), and design questions (delivery
state sentinel, single source of truth for stage list).

Recording them in FOLLOWUPS.md at the agent-studio root (not under
docs/, which the repo .gitignore excludes) so each one can be turned
into a separate PR or issue. Not packaged (publish.py only ships
agent/, skills/, scripts/, manifest fields).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(agent-studio): move follow-ups out of repo — design docs live in ~/workspace/design-doc

FOLLOWUPS.md was added in c1666cd as an in-repo tracking file, but the
project convention is that design docs / followup backlogs live at
~/workspace/design-doc/<repo>/<area>/, not in the repo itself. The
content has been moved to:

  ~/workspace/design-doc/ecap-agent-pack/agent-studio/pr-118-followups.md

Removing the in-repo copy keeps the repo focused on shipped behavior.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): close 5 review gaps — clean zip/, gate install on description.json, validate listing assets, expand /studio status, sync-note BOOTSTRAP

Five low-risk follow-ups from the PR #118 review:

- clean.py — clear zip/ on /studio new. Same failure shape as the PR
  #118 bug (wrong artifact deployed): without this, a stale tar.gz from
  the previous build can be picked up by /studio install --source local.
- install.py — require description.json at pack root for --source
  current (matches the new SKILL.md hard rule with a code-level gate).
  Routes the creator back to Stage 5a generate_description.py.
- validate.py — new check_listing_assets that warns (doesn't fail) when
  description.json or avatar.png are missing. Closes the gap where
  "Stage 4 validate passed" didn't imply "Stage 6 install will succeed".
- main SKILL.md — /studio status now also reports archive presence in
  zip/ and the delivery state file (the file itself lands in commit B).
- BOOTSTRAP.md — note that the stage list mirrors SKILL.md §Stages;
  edit SKILL.md first, then mirror. (Discipline only — no programmatic
  enforcement; full dedup tracked as F12 in the design-doc.)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* feat(agent-studio): close Stage 6 logic — delivery sentinel + mechanical package/publish signal

Two complementary changes that finish the Stage 5/6 split introduced
earlier in this PR:

1. publish.py grows a --continue-into-delivery flag, echoed back in the
   result JSON as `continue_into_delivery`. /studio publish passes the
   flag, /studio package omits it. packaging.md §5f now branches on the
   JSON field instead of asking the LLM to remember which slash command
   was typed (fragile across heartbeats, subagent calls, long contexts).

2. install.py and run_share.py write `data/.delivery-state.json` on
   success (method=install or method=share, with timestamp + pack
   metadata). The main SKILL.md "Current stage" detector reads it to
   tell "pack delivered" from "pack just sitting in zip/", so Studio
   stops re-prompting install/share/stop every session after a
   successful delivery. clean.py's data/ wipe already resets this on
   /studio new — no extra cleanup needed.

Tested: publish.py with and without the flag emits the expected
continue_into_delivery value; all 5 scripts pass py_compile.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* feat(agent-studio): factor archive contract + scaffold state file + truth-source clarity

Three follow-ups that improve the structural guarantees Agent Studio
relies on:

1. F3 — archive layout contract moves to _common.py (assert_archive_layout).
   install.py calls it inside normalize_local_archive_path, refusing any
   --source local archive that doesn't pass. Previously the contract was
   enforced only by publish.py's post-build self-check; install would
   happily submit a hand-crafted archive someone else gave us. (Remote
   archives are downloaded backend-side; we don't validate those locally
   yet — tracked in F4 of the design doc.)

2. F6 — scaffold.py writes data/.scaffold-state.json with
   agent_dir_filled=false. AGENTS.md's /test gate now reads that field
   (fail-safe to "not filled" on any read error) instead of grepping the
   literal "To be filled" placeholder text. automation.md's Stage 3
   completion instruction tells the agent to flip the field to true.
   Localizing or rewording the scaffold placeholder no longer silently
   breaks TEST mode entry.

3. F10 — new "Truth sources (don't conflate)" section in main SKILL.md
   names the four signals that previously felt overlapping:
   .scaffold-state.json (Stage 3 done), .delivery-state.json (Stage 6
   done), validate.py output (Stage 4 correctness), data/config.json
   (runtime, end-user onboarded — not Studio's concern).

Tested: assert_archive_layout rejects a hand-crafted top-level
agent/+skills/ archive via _common.py; install.py's
normalize_local_archive_path rejects the same archive at install time
and accepts a clean publish.py output; scaffold.py writes the state
file with agent_dir_filled=false on a fresh scaffold.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor(agent-studio): rename publish.py → package.py to match its actual job

After the Stage 5/6 split, publish.py only does packaging — it never
deploys anything. The slash command /studio publish stayed (it
orchestrates Stage 5 + 6 via the §5f gate, matching "publish" in natural
English), but the underlying script is purely a packaging primitive
shared by /studio package, /studio publish, /studio share, and (through
the archive layout contract) /studio install.

Renaming publish.py → package.py:

- Aligns with what the script does. Every other lifecycle script in this
  tree is named after its action (scaffold/validate/clean/
  generate_description/write_*) — publish.py was the odd one out, named
  after an old conflated meaning of /studio publish.
- Aligns with /studio package (the slash command that exists precisely
  to invoke this script and stop).
- Doesn't conflict with /studio publish — the orchestrator is the
  package.py invocation PLUS LLM-driven §5f routing; they're at
  different layers.

All references are within agent-studio (single repo, no external
service consumes the script by name) — git mv + a sweep of doc/code
references is enough. Verified with grep (zero stale refs) and a
smoke-test of package.py + run_share.py's package_script invocation
+ py_compile of all five scripts.

Also synced agent-pack.yaml's own description (still said "5-stage
build") to the 6-stage model.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* revert(agent-studio): drop /studio package — covered by /studio publish + "stop"

/studio package was added earlier in this PR (commit 192ecad) for
command/stage-name symmetry ("Stage 5 is named Packaging, so the
command should be /studio package"). User feedback during review:
"feels like too many commands". Reassessing honestly, the only use
case it served — "I want the tar.gz but not deployment" — is covered
by /studio publish reaching the §5f gate and the creator picking
option 3 (stop here). The cost of having a separate command was:

- /studio package as an extra entry in BOOTSTRAP and the AGENTS.md
  command table
- §5f branching on continue_into_delivery (true vs false), with
  package.py needing a --continue-into-delivery flag echoed in JSON
- Doc fragmentation: SKILL.md "Package / publish / share / install"
  section + per-command entries had to enumerate both
- LLM having to decide which command to use for a niche case

Removing:

- package.py — drop the --continue-into-delivery flag and its
  continue_into_delivery JSON field. Script becomes a pure packaging
  primitive again.
- packaging.md §5f — single branch: always run the install / share /
  stop gate. Kept a short note explaining "option 3 covers the bare
  tar.gz case" so future readers understand why there's no command.
- Main SKILL.md — drop /studio package from the Studio commands table,
  drop it from the Package/publish/share/install section (now
  Publish/share/install), drop the Stage 5 dual-entry-point preamble.
- AGENTS.md command table — drop the /studio package row.
- install.py error message — refer only to /studio publish.

Keeping:

- package.py script name (rename in fc64549). The rename was based on
  what the script DOES (packaging), independent of whether /studio
  package exists. Script naming alignment with its action remains
  correct.
- /studio share and /studio install as Stage 6 shortcuts — both have
  use cases /studio publish doesn't trivially cover (re-share without
  re-publish; install a third-party archive).

This is honest course correction: /studio package was added in this PR
and dropped in this PR. Better to fix before merge than ship a
command-surface that doesn't pay for itself.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* revert(agent-studio): drop /studio status — agent leads with stage info at session start anyway

/studio status was just a structured read (agent-pack.yaml + ls zip/ +
delivery-state.json) — no orchestration, no state transition, no
destructive effect. The SKILL.md "Current stage" detector already runs
at every session start and reports the same info naturally; creators
asking "where am I?" in plain language get the same answer.

Following the same principle as the /studio package drop: commands
without an irreplaceable mechanical role shouldn't have a slash.
/studio validate stays — it maps to a real script (validate.py) and
creators benefit from on-demand re-validation after edits.

Net command surface: 7

  /dev, /test
  /studio new, /studio validate
  /studio publish (Stage 5 + 6)
  /studio share, /studio install (Stage 6 shortcuts)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): close 4 critical findings from independent code review

Independent reviews by Claude (feature-dev:code-reviewer) and Codex
(codex:codex-rescue) both flagged real regressions and gaps in PR #118's
restructure. This commit closes the four that block correct operation.

C1 (Critical) — Stage 3 sentinel never mechanically written.

scaffold.py wrote data/.scaffold-state.json with agent_dir_filled=false,
AGENTS.md's /test gate read that field, but nothing flipped it true.
automation.md only had a prose instruction asking the LLM to hand-write
the JSON — fragile. validate.py now writes the sentinel as a side
effect of check_agent_completeness: when all three agent/*.md files
have substantive (non-placeholder) content, agent_dir_filled becomes
true. Running validate at end of Stage 3 (already in automation.md) is
now sufficient — no separate LLM-driven write step. automation.md prose
updated to point at validate.py instead of a raw JSON write.

C4 (Critical) — install.py list-sources blocked by missing description.json.

The description.json gate added in commit 76fde6d lived inside
read_current_pack_preview, which is called by BOTH the install command
(--source current) AND the list-sources command. Result: a creator who
wanted to /studio install a third-party archive or share URL got
blocked because their own workspace was missing description.json —
which is irrelevant to non-current sources. Moved the check from
read_current_pack_preview to source_info_from_current_pack so it only
fires for --source current.

C5 (Critical) — .zip archives bypassed assert_archive_layout.

normalize_local_archive_path only ran the layout check on .tar.gz and
.tgz, but SUPPORTED_ARCHIVE_SUFFIXES included .zip — meaning a
hand-crafted .zip with forbidden top-level agent/ or skills/ dirs
would install unchallenged, recreating the exact bug PR #118 fixed for
tar archives. Since we have no zipfile-based layout check today (and
no test coverage on the .zip path at all), dropped .zip from
SUPPORTED_ARCHIVE_SUFFIXES. SKILL.md updated to reflect that .zip is
not supported.

C3 (High) — agent-pack.yaml root description still said "5 stages".

The top-level description field — which surfaces in ZooClaw's catalog
card — still listed "Discovery, Skill Design, Agent Setup, Testing,
and Publishing", missing the Packaging/Delivery split done elsewhere
in this PR. Updated to the 6-stage terminology.

Tested locally:
- C1: validate.py on a workspace with substantive agent/*.md flips
  data/.scaffold-state.json from {agent_dir_filled: false} to true.
- C4: list-sources on a workspace without description.json now
  returns status=ok with the manifest preview, no error.
- C5: install.py rejects /tmp/fake.zip with "Unsupported archive
  format" instead of accepting it unchecked.
- C3: yaml text change only.

The other findings (scaffold/clean.py IDENTITY.md interaction,
write_cron forces heartbeat, /studio share could reuse corrupt
leftover archive, install.py --check-only requires token, etc.) are
pre-existing or independent — recorded in design-doc as follow-ups.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): close 6 critical findings from round-2 independent review

Round-2 Claude (feature-dev:code-reviewer) and Codex (codex-rescue)
flagged new issues plus convergent regressions still open after the
round-1 fixes. This commit closes the six that block correct operation
or recreate the original tar.gz-impersonator bug.

R2-C1 (Critical) — validate.py reported overall "pass" with placeholder agent files.

`check_agent_completeness` returned `status: warn` (not `fail`) when
agent/AGENTS.md / SOUL.md / IDENTITY.md still had the scaffold
placeholder text. The overall validate result therefore became "pass"
(only `failed == 0` is checked), misleading the LLM into reporting
Stage 4 success on a pack that would deploy an identity-less bot.
Changed to `status: fail` so the overall result blocks the
"ready to publish" gate until Stage 3 fills in real content.

R2-C2 (Critical) — install.py silently reused stale cards on same-version republish.

`determine_card_action` returned `action: reuse / reason: same_version`
whenever the version string matched, even if the path_value (source URL
or local path) differed from the existing card. Re-publishing the same
version with new content would therefore install the old card pointing
at the old artifact — the classic "I republished but nothing changed"
silent stale-deploy. Same-version + different-source now requires
explicit reuse/replace confirmation (`needs_confirmation`,
reason=source_changed_same_version). Same-version + identical source
is still handled by the earlier same_source branch (still silent reuse,
which is correct for no-op republishes).

R2-C3 (High) — clean.py wrote a placeholder manifest, breaking Stage 1 stage detection.

The SKILL.md "Current stage" detector treats "no manifest" as Stage 1.
clean.py wrote a placeholder agent-pack.yaml after /studio new, so the
detector saw a file with no name/version fields and got confused about
which stage to resume. Now clean.py deletes the manifest outright;
scaffold.py recreates it at the end of Stage 1.

R2-C4 (High) — /studio share reused existing archives without layout validation.

run_share.py's ensure_archive returned an existing zip/<pack>.tar.gz
unchanged. A hand-crafted archive placed there manually (or left over
from a pre-PR-118 workspace) would be silently staged into
artifacts/shares/ and a share URL handed out — exactly the failure
mode PR #118 fixed for new archives. Added _validate_archive() that
runs assert_archive_layout on every reuse path (zip/ cache and explicit
--archive arg); fails fast with a re-package instruction.

R2-C5 (Medium) — SKILL.md Truth Sources still claimed the LLM flips .scaffold-state.json.

The "Truth sources" section read "Written false by scaffold.py; flipped
true by the agent at end of Stage 3" — but commit f97a0cd made
validate.py the canonical writer. Updated to reflect that validate.py
now writes the field based on check_agent_completeness output.

R2-C6 (High, convergent across both rounds) — write_cron.py force-enabled heartbeat.

Adding cron jobs unconditionally flipped heartbeat.enabled to true,
even though references/automation.md §3c treats heartbeat and cron as
independent automation choices. Creators who deliberately chose
cron-only had their manifest silently overridden. Removed the
heartbeat-enable side effect from write_cron.py; heartbeat enabling
remains the job of write_heartbeat.py or manual manifest edit.

Tested locally:
- R2-C1: validate.py on a placeholder agent/ pack now returns
  overall status=fail (was pass).
- R2-C3: clean.py on a workspace deletes agent-pack.yaml (was reset
  to a comment-only placeholder).
- R2-C4: run_share.py on a workspace with a hand-crafted forbidden-
  layout archive in zip/ now refuses with a re-package instruction
  (was silently staged and shared).
- R2-C6: write_cron.py no longer touches heartbeat.enabled.
- All 5 modified scripts pass py_compile.

The other round-2 findings (provision.py/finalize.py stubs in
write_onboarding.py; check_crossrefs validates workspace paths but
package.py rewrites to .agents/skills/; package.py YAML parser brittle
for data_templates blocks; avatar location inconsistency between
validate.py and package.py; SOUL.md required-vs-optional drift;
generate_description.py emits relative avatar_url; scaffold.py omits
cli_dependencies and data_sources) are pre-existing or independent —
recorded in design-doc as a third batch of follow-ups.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(agent-studio): aggressive prompt-token trim — -251 lines across 5 files

The instructional .md files grew significantly across PR #118's
restructure (Stage 5/6 split, 6 critical fixes, multi-round reviews).
Several patterns of bloat accumulated:

- "Never hand-craft tar" warning repeated in 4 places — the package.py
  self-check + install.py archive validation are the real defense; one
  canonical doc warning (packaging.md §5e) is enough.
- "Publish/share/install — orchestrator and shortcuts" section in main
  SKILL.md duplicated the Studio commands table immediately below.
- Per-stage GATE clauses ("present summary → ASK before next") repeated
  5 times — collapsed into one global rule.
- install/SKILL.md had 6 separate preview/install code blocks for 3 ×
  {preview, install} source variants — collapsed into one parametric
  block + table of source flag mappings.
- Stage 1's full scaffold.py invocation lived in main SKILL.md
  duplicating references/discovery.md.
- AGENTS.md command table duplicated main SKILL.md's Studio commands.

The runtime contract is unchanged:
- All gates (TEST entry, §5f delivery choice, Stage 4 fail-on-
  placeholder) are still spelled out where they're enforced.
- Truth-source semantics (.scaffold-state.json, .delivery-state.json,
  validate.py, data/config.json) still listed in main SKILL.md.
- Hand-craft-tar prohibition still in packaging.md §5e (the canonical
  spot) and referenced from /studio publish, share, install.
- Stage detection logic still in main SKILL.md "Current stage".

Sizes:
- AGENTS.md: 58 → 38 (-34%)
- main SKILL.md: 155 → 67 (-57%)
- packaging.md: 68 → 53 (-22%)
- agent-studio-share/SKILL.md: 59 → 36 (-39%)
- agent-studio-install/SKILL.md: 163 → 58 (-64%)

Every-session load (root + always-loaded SKILL.md): 241 → 133 lines (-45%).

Verified validate.py still runs and returns sensible structured output
after the trim.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(agent-studio): second-pass token trim on references/*.md — -146 lines

After the first prompt-token trim covered always-loaded files (main
SKILL.md, AGENTS.md, install/share SKILLs, packaging.md), the per-stage
references were the next biggest cost. They load on demand once per
stage, but the longest ones (automation.md at 206 lines, skill-design.md
at 142) still dominate stage-3 / stage-2 token cost.

Trims preserve every gate, rule, and contract:

- automation.md (206 → 109, -47%): collapse the inline "Required
  sections" code-block examples (Session Startup, Memory) into single-
  sentence bullets — the LLM has the same content but doesn't need
  example block scaffolds. Drop redundant prose paragraphs ("All four
  delivery fields are required" was repeated). Compress step lists
  into single-line items. Keep all 4 required delivery fields enumerated
  (load-bearing for cron correctness) and the placeholder-vs-substantive
  test-state notes (load-bearing for /test gate).

- skill-design.md (142 → 126, -11%): compress prose around the 9-step
  flow (2a-2i) and the upload procedure. Keep the cli_dependencies
  YAML example (used as a copy-paste template). Keep CLI runtime auth
  modes (QR / CAPTCHA / OAuth / cookie) since each behaves differently.

- data-sources.md (84 → 70, -17%): collapse layer-3 search instructions
  into one merged list. Trim repeated install-target reminders.

- discovery.md (50 → 43, -14%): merge "Strategy" bullets, compress
  scaffold.py command formatting.

- delivery.md (34 → 24, -29%): merge sub-bullets, drop the "Done" prose
  that paraphrased the celebration in packaging.md §5f.

- testing.md (39 → 37, -5%): fold validate.py's checks into one line
  (the script itself documents them in JSON output anyway).

Combined with the first trim pass (commit e395f5a), total markdown
reduction across this PR's docs is ~400 lines. Every gate, sentinel
write/read, and "never hand-craft tar" rule still has a single
canonical statement where it's enforced.

Verified validate.py still runs and emits sensible JSON structure.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(agent-studio): apply /simplify review — dedup write_delivery_state, drop narrating comments, idempotent state writes

Three parallel /simplify reviewers (code reuse, code quality,
efficiency) ran against PR #118's Python diff. Applied the convergent
high-value findings; skipped over-engineering / false positives.

Reuse: dedup write_delivery_state

write_delivery_state was defined verbatim in both install.py and
run_share.py with divergent signatures (one took SourceInfo and emitted
agent_id; the other took flat strings and emitted share_url). Both
deferred `from datetime import datetime, timezone` into the function
body. Moved to _common.py as a single keyword-args helper with
DELIVERY_METHOD_INSTALL / DELIVERY_METHOD_SHARE constants for the
method field (was a raw string in two places).

Quality: drop narrating comments

- write_cron.py block comment explained that the function used to flip
  heartbeat on and that this was wrong — changelog prose. The current
  code (no heartbeat mutation) is self-evident; rationale lives in
  references/automation.md §3c where it belongs.
- install.py read_current_pack_preview had a 4-line comment explaining
  where the description.json check does NOT live. Navigational author-
  comment, no value to a future reader.

Efficiency: idempotent state writes + redundant operations

- validate.py _sync_scaffold_state now reads the current file and skips
  the write when the value is unchanged. validate.py runs frequently
  (Stage 4, TEST-mode gate, on-demand) — idempotent rewrites show up
  as fs activity on slow filesystems. Verified second-run mtime matches
  first-run mtime.
- scaffold.py was calling state_dir.mkdir() right after the directory-
  creation loop had already created data/. Removed the redundant call.
- package.py _generate_summary was opening agent-pack.yaml a second
  time after main() already had manifest_content in memory. Passed the
  string through instead of re-reading.

Reuse / Quality: clean.py extract _clear_dir helper

Five copy-paste blocks for "iterate a directory and delete each entry"
(skills/, scripts/, data/, deps/, artifacts/, zip/) consolidated into a
single _clear_dir(dir, label, cleaned) helper.

Skipped:

- Quality "agent_dir_filled is derived state, compute on demand" —
  reviewer missed that the AGENTS.md TEST gate runs on the LLM side
  via `cat`, not via Python. The cached file IS the on-demand
  interface; validate.py is the canonical writer.
- ShareError/InstallError type parity — over-engineering for a
  thin 2-call wrapper inside one file.
- Streaming tarfile reads — agent pack archives are tens of KB to
  a few MB with dozens of files; O(N) memory on member-list scan is
  imperceptible. The reviewer flagged it as worth doing on large
  archives that don't exist here.
- description.json TOCTOU — the explicit .exists() check produces a
  clear actionable error pointing to Stage 5a; converting to
  try/except FileNotFoundError on a later read scatters the same
  semantics for no real benefit.

Tested: all 8 scripts pass py_compile; package.py still produces a
clean archive; validate.py second run no longer touches the state
file (mtime unchanged); clean.py with _clear_dir helper cleared all
expected dirs.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): close 3 round-3 bugs — stale delivery sentinel, uncaught tarfile.TarError, version-blind Stage 6

Three real correctness bugs found in round-3 review (Codex). All
introduced by earlier PR-118 changes; all caught before merge.

R3-H1 — install via /studio install --source current wrote
.delivery-state.json before the actual install completed.

install.py's stage_archive_via_share() shells into run_share.py to
build the share URL backend installs from. run_share.py was
unconditionally writing the share-side delivery sentinel at the end —
which fired BEFORE the subsequent backend install API call. If
conflict resolution returned needs_confirmation, or the async install
failed, the sentinel was already on disk and Studio's "Current stage"
detector treated the workspace as Stage-6-complete on the next session.

Added a --internal-stage flag to run_share.py that suppresses the
sentinel write. install.py's stage_archive_via_share always passes it.
The user-visible "delivered" moment for /studio install is the install
API success in install.py's main(), where write_delivery_state already
runs. Direct /studio share still writes the sentinel unchanged.

R3-H2 — assert_archive_layout let corrupt archives escape as raw tracebacks.

_common.py:assert_archive_layout called tarfile.open(..., "r:gz") and
caught nothing. A corrupt or non-tar file raises tarfile.ReadError /
TarError, which is NOT a RuntimeError — so the exception bypassed the
"except RuntimeError" handlers in package.py, install.py, and
run_share.py, propagating as an unhandled traceback. This undermined
the PR's whole point (reject malformed archives, surface a structured
refusal).

Wrapped the tarfile.open call in try/except tarfile.TarError; re-raise
as RuntimeError with an explanatory message so the existing callers'
RuntimeError handlers work unchanged. Verified with `echo "junk" >
fake.tar.gz` — caller now gets a clean RuntimeError, not a traceback.

R3-M3 — Stage 6 detector was version-blind.

SKILL.md's "Current stage" check classified "archive in zip/ + any
.delivery-state.json file present" as done. After v1 install → bump
manifest to v2 → repackage, the stale v1 sentinel still marked the
workspace as Stage-6-complete for v2 — silently skipping the new
version's delivery prompt.

The sentinel already records pack_name + version (added in this PR);
the detector just never compared them. Updated SKILL.md's Stage
detector to require sentinel pack_name+version to match the current
manifest; mismatch → still Stage 6 (a new version isn't yet delivered).

Tested: corrupt .tar.gz produces a RuntimeError with a useful message
(not a traceback); run_share.py with --internal-stage no longer
writes the sentinel, without the flag it still does; all 3 scripts
pass py_compile.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): close 4 round-4 bugs — path normalization, OSError, list-sources resilience, --source local sentinel

Round-4 review (Claude + Codex) surfaced 4 real correctness bugs in the
prior commits. All caught before merge.

R4-H1 — assert_archive_layout bypassed by ./-prefixed members.

`./agent/foo.md` split on `/` yields first-segment `.`, not `agent`,
slipping past the forbidden-prefix check. A hand-crafted archive using
`tar`'s `--transform=s,^,./,` (or any tool that prepends `./` to
member names) recreated the exact bug PR #118 was written to block.

Normalize each member via `posixpath.normpath(raw).lstrip("/")` before
the forbidden-prefix and required-file checks. Also reject `..`
traversals outright (defense against extracting outside the workspace).
Verified: a Python-built archive with `./agent/IDENTITY.md` now raises
"archive has forbidden top-level entries: ['agent/']".

R4-H2 — assert_archive_layout leaked OSError / FileNotFoundError.

The function's docstring promised "any I/O failure surfaces as a
RuntimeError so callers don't have to know tarfile internals." But the
`except tarfile.TarError` block only catches tarfile-specific
exceptions. `tarfile.open` raises `FileNotFoundError`/`OSError` when
the path is missing or unreadable — these propagated as raw tracebacks
through run_share.py's `_validate_archive` and out of `main`.

Widened to `except (tarfile.TarError, OSError)`. Verified: calling
`assert_archive_layout` on a nonexistent path now returns a clean
RuntimeError.

R4-M1 — list-sources aborted on a single bad archive.

`install.py list_sources` iterated `zip/` and called
`source_info_from_archive` on each entry. After round-3's fix added
`assert_archive_layout` validation to `normalize_local_archive_path`,
any single corrupt or hand-crafted archive in `zip/` raised
`InstallError` out of the loop and killed the whole listing — the
creator couldn't see their valid current pack alongside a stale broken
one.

Per-archive try/except around the conversion; rejected archives now
land in a separate `rejected_archives` field of the JSON output with
the file path + reason. Verified: a `junk.tar.gz` and a clean current
pack now both appear in the response, junk in `rejected_archives`.

R4-H3 — /studio install --source local wrote a delivery sentinel keyed
to the FOREIGN archive's name/version.

`source_info.name` and `source_info.version` for `--source local` /
`--source remote` come from `derive_archive_metadata(archive_name)` —
the filename of the imported archive. Writing a delivery sentinel with
those values, while the workspace's own `agent-pack.yaml` says
something different, made SKILL.md's Stage 6 detector forever
mismatch and re-prompt install/share/stop every session.

Conceptually, `--source local`/`--source remote` install someone
else's pack into the creator's account — they don't represent the
workspace's own build progressing to delivered. Restrict the
`write_delivery_state` call to `args.source == "current"`. Foreign
installs still succeed via the backend API; they just don't claim
to advance THIS workspace's Stage 6.

R4-related — Stage 6 detector tightened to match specific archive.

SKILL.md's stage flow now keys Stage 5 vs 6 on
`zip/<name>-<version>.tar.gz` existing for the CURRENT manifest, not
"any archive in zip/". A stale older-version archive no longer counts
as a v2 deliverable. Also aligns with R4-H3: the sentinel pack_name +
version is compared against the current manifest, ensuring foreign
installs (which don't write the sentinel) don't trip the detector.

Tested: all four fixes verified via the smoke-tests above; 3 modified
scripts pass py_compile; the round-3 bug fixtures still pass.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): close 4 round-5 bugs — clean.py leaks, list-sources Stage-1 fragility, foreign-archive identity

Round-5 review (Claude + Codex) found four more real bugs. All caught
before merge.

R5-H1 — clean.py leaked avatar.png + agent/ subdirs across /studio new.

Two adjacent leak paths:
- avatar.png at the workspace root survived /studio new. package.py's
  _find_avatar checks the root before artifacts/, so the next pack
  would silently include the previous pack's avatar in its archive.
  Now deleted alongside description.json on reset.
- agent/ cleanup iterated entries but only `unlink()`d files
  (`fpath.is_file()`). Subdirectories from a previous pack
  (e.g. agent/memory/, agent/scripts/) survived and would be
  re-packaged by package.py's `agent_dir.rglob("*")`. Now
  shutil.rmtree's any non-skeleton subdirectory too.

R5-H2 — list-sources died on missing agent-pack.yaml.

`/studio install` step 2 calls list-sources. After round-3's check
moved description.json's gate to source_info_from_current_pack,
read_current_pack_preview still raises FileNotFoundError when
agent-pack.yaml is absent — which kills the entire listing for a
fresh-workspace creator who only wants to install a foreign archive
from zip/. Wrapped read_current_pack_preview in try/except inside
list_sources; the result now has `current: null` + `current_error: <reason>`
when the workspace has no manifest, and zip/ archives still enumerate.

R5-M3 — /studio share --archive labeled foreign archive with workspace identity.

run_share.py read pack_name/version from the current workspace's
agent-pack.yaml even when --archive pointed at a foreign archive.
The script then returned those workspace values in its JSON output
and (without --internal-stage) wrote .delivery-state.json with the
workspace's name/version while actually staging pack A's bytes. Now
when --archive is supplied, identity comes from the archive's
filename (`<name>-<version>.tar.gz`) via a new
`_identity_from_archive_name` helper. Workspace manifest is only
read when --archive is absent.

Tested: clean.py removes avatar.png + agent/subdir/; list-sources
without agent-pack.yaml returns current=null + listed rejected
archives; run_share --archive foreign-7.7.7.tar.gz reports
pack_name=foreign / version=7.7.7 (not the workspace's
workspace-pack/0.1.0); all 3 scripts pass py_compile.

Skipped (pre-existing, not introduced by this PR, tracked separately):
- write_cron.py multi-line YAML prompts
- write_cron.py empty cron_jobs serialized as `cron_jobs:` (null)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): close 5 round-6 bugs — version sentinel, archive contract, YAML quoting, missing-version package, Studio-emoji leak

Round-6 review (Claude + Codex) found 5 more real bugs.

R6-C1 — derive_archive_metadata returned version=base for unversioned archive names.

`derive_archive_metadata("my-agent.tar.gz")` returned
`("my-agent", "my-agent", "my-agent")` — version equal to the full
stem. The declared return type was `tuple[str, str | None, str]` and
every other version helper returns `None` for the no-match case;
this lone outlier broke `determine_card_action`'s
`requested_version and existing_version` guard and forced spurious
`needs_confirmation` on every install of a non-semver archive.
Returns `(base, None, base)` now.

R6-H1 — assert_archive_layout's REQUIRED_TOP_LEVEL_FILES was too thin.

Only required `agent-pack.yaml`. package.py guarantees AGENTS.md /
SOUL.md / IDENTITY.md at archive root too (scaffold creates them
unconditionally; check_agent_completeness blocks Stage 4 on
placeholders); their absence in an archive is a strong signal of
hand-crafting. Added all three to REQUIRED_TOP_LEVEL_FILES — the
deployed bot now provably has a root SOP, persona, and name.

R6-H2 — write_cron.py raw f-string YAML interpolation broke on
colons, hashes, and multi-line prompts.

The function built YAML by interpolating raw job-field values into
f-strings. Any value containing `:`, `#`, `>`, `|`, leading/trailing
whitespace, or `\n` produced silently malformed YAML — the most
common case being a multi-line prompt where only the first line got
indented under `prompt: >`. Replaced with `json.dumps(v)` for each
scalar: YAML 1.2 is a strict superset of JSON for quoted strings, so
this handles colons, multi-line via `\n`, unicode, and edge whitespace
in one place. Verified by emitting a cron job with embedded colons +
newlines + `#` and parsing the output back through PyYAML.

R6-M2 — package.py didn't validate empty version.

It rejected an empty `name:` but happily proceeded with an empty
`version:`, producing `<name>-.tar.gz`. Downstream install / share
parse the version from the filename and got broken state. Now fails
with "Could not read 'version' from manifest" — same shape as the
existing name check.

R6-M3 — read_pack_emoji preferred workspace root IDENTITY.md.

In an Agent Studio workspace, root `IDENTITY.md` belongs to Agent
Studio itself; the pack-being-built's identity is `agent/IDENTITY.md`.
`read_pack_emoji` checked root first → install previews and catalog
cards inherited Studio's emoji for the new pack. Swapped lookup order
to prefer `agent/IDENTITY.md`.

Tested: derive_archive_metadata returns None for unversioned;
assert_archive_layout rejects archives missing any of agent-pack.yaml /
AGENTS.md / SOUL.md / IDENTITY.md; write_cron.py's output round-trips
through PyYAML with colons + newlines + hashes intact; package.py
fails missing-version with the expected JSON error; read_pack_emoji
returns the pack's emoji (📣) even when root IDENTITY.md says 🛠️;
all 4 modified scripts pass py_compile.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): close 3 round-7 bugs — remote install bypass (critical), SOUL.md regex truncation, --archive unversioned mismatch

R7-H1 — /studio install --source remote bypassed assert_archive_layout.

Round-4 added layout validation for --source local but the remote path
still submitted the share URL to the backend without local inspection
of the archive's contents. The exact bug class PR #118 was written to
block (hand-crafted tar.gz deploying as the wrong bot) was therefore
still open when the archive arrives via a share URL.

Added _validate_remote_archive() in install.py: streams the URL to a
temp file (32-byte chunks, 64 MiB cap, 30s timeout — prevents OOM /
hang on hostile URLs), runs assert_archive_layout, deletes the temp
file. The backend still downloads its own copy; this is a pre-submit
local guard, not a swap. Verified end-to-end with a local
http.server fixture: a bad archive at http://localhost/bad.tar.gz now
gets a clean InstallError pointing at the forbidden top-level dirs,
not silently submitted.

R7-H2 — package.py's SOUL.md cleaner regex truncated at the first --> in onboarding config.

provision.py appends `<!-- User preferences: <json> -->` as a single
line. package.py's `re.sub(r'\n*<!-- User preferences:.*?-->\n*', ...)`
used lazy `.*?` with DOTALL, so any `-->` substring INSIDE the JSON
config (e.g., a user preference like `"use --> to indicate flow"`)
terminated the match early — leaving trailing JSON fragments and a
stray `-->` literal in the packaged SOUL.md. Replaced with
`[^\n]*-->` which stays on one line and is greedy by default,
matching the LAST `-->` on the comment line. Verified: a SOUL.md with
an embedded "use --> arrow" preference now strips cleanly with no
leftover content.

R7-H3 — run_share.py --archive rejected unversioned filenames; install.py accepted them.

`_identity_from_archive_name` raised ValueError when the archive
filename had no semver suffix (e.g., `my-agent.tar.gz`), while
install.py's `derive_archive_metadata` gracefully returned
`(base, None, base)` for the same input. A creator could install a
hand-named archive but not share it — asymmetric and surprising.
Aligned: unversioned filenames return `(base, "unknown")` from
run_share.py, mirroring install.py's permissive behavior. Both code
paths now accept the same set of archive names.

Tested: all three fixes pass with smoke fixtures; the 3 modified
scripts pass py_compile.

Deferred to design-doc followups (not introduced by this PR):
- Filename-vs-embedded-manifest identity for install (Codex H2)
- provision.py {{agent_name}} placeholder substitution (R3-1)
- package.py agent/ rglob allows arbitrary nested files (R3-2-related)
- files_skipped count overcounts cleaned agent/*.md (Claude M3, cosmetic)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): close round-8 — reject non-regular tar members; document remote-validate TOCTOU honestly

R8-H1 — assert_archive_layout only inspected member names, not types.

A symlink, hardlink, or device-node entry in a tar.gz could pass the
layout check (the name didn't trip any forbidden prefix) and still
extract to a path outside the workspace or impersonate an identity
file at runtime. Now iterate `tarfile.TarInfo` objects and refuse
anything that isn't `isfile()` or `isdir()` — symlinks (`SYMTYPE`),
hardlinks (`LNKTYPE`), char/block devices, and fifos all reject with
a clear "non-regular entry" error. Verified: an archive carrying an
otherwise-valid layout plus an `evil-link → /etc/passwd` symlink is
now rejected before any extraction can happen; legitimate
package.py output still validates.

R8-Note — remote-validate TOCTOU is a known limitation, not a bug.

_validate_remote_archive downloads the URL once, validates the bytes
it got, then submits the URL — and the backend independently
re-fetches. A mutable / one-shot URL could in principle serve A to us
and B to the backend. The architecturally clean fix (download, stage
to a controlled location, submit a hash-pinned URL) is out of scope
for this PR — it would also re-host third-party share archives in our
artifacts/, which is a policy decision. Updated the docstring to be
honest: this check exists to catch the common "creator pasted a
non-package.py URL" case early, not as a defense against actively
hostile URLs. Backend should also validate.

Tested: symlink fixture rejected; agent-studio's own packaged output
still validates; both modified scripts pass py_compile.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): close round-9 — required identity files must be regular files, not directories

assert_archive_layout's required-name check collected top-level entries
by name only. A hand-crafted archive containing a DIRECTORY named
`AGENTS.md` (or `SOUL.md` / `IDENTITY.md`) would satisfy the membership
test while leaving the deployed bot without an SOP / persona / name.
The round-8 non-regular-member rejection caught symlinks and devices
but not directories — directories are legitimate at top level (e.g.,
`.agents/`), they just can't substitute for the required identity
files.

Now collect normalized entries as `(name, is_file)` pairs and require
the four members of REQUIRED_TOP_LEVEL_FILES to be present AS REGULAR
FILES. Directory entries with matching names no longer count. Verified:
an archive with `AGENTS.md` as a directory now rejects with "missing
required regular-file entries: ['AGENTS.md']"; legitimate package.py
output continues to validate.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): close round-10 — reject absolute-path tar entries instead of silently laundering them

The previous normalization used `posixpath.normpath(info.name).lstrip("/")`,
which silently converted `/agent-pack.yaml` → `agent-pack.yaml` for the
layout check. The validator then accepted the archive even though a
naive extractor honoring absolute paths would write the files outside
the workspace root — a path-escape vector AND a validator bypass
(handcrafted archives can spell required files with leading `/` and
pass).

Reject absolute-path entries explicitly with a dedicated error,
parallel to the existing `..` traversal rejection. A legitimate
package.py archive never contains absolute-path members; rejecting
them is strictly safer than normalizing. Verified: an archive with
`/agent-pack.yaml` etc. is now rejected with "archive contains an
absolute-path entry: '/agent-pack.yaml'"; legitimate package.py
output continues to validate.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* revert(agent-studio): clean.py preserves zip/ across /studio new — versioned archives are user history, not scratch

Commit 76fde6d added zip/ to clean.py's cleared-on-reset list under the
theory that "stale archives must not survive /studio new (otherwise
/studio install --source local could deploy yesterday's pack)". That
was a misread of the design.

Each archive in zip/ is named `<pack-name>-<version>.tar.gz`. After
/studio new, the new pack has a different name (scaffold.py prompts
for one), so the new pack's archive can't collide with old ones — the
listing in /studio install --source local shows distinct entries the
creator must pick from explicitly. There is no silent
wrong-archive-deploys-as-current-pack failure mode: the user does the
picking.

Removing zip/ on reset throws away the creator's build history. If
they /studio new and then change their mind, the previous version is
gone. Treating zip/ as a versioned output directory (preserved across
resets) is the correct design — same shape as `dist/` in npm
packages or `target/` in cargo workspaces.

Tested: /studio new on a workspace with pack-v1.tar.gz + pack-v2.tar.gz
in zip/ now keeps both; data/, agent/ non-skeleton files, artifacts/,
agent-pack.yaml etc. still cleared as before.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(agent-studio): bump version 1.0.1 → 1.1.0 for PR #118

Minor bump reflects the scope of this PR:

- Stage 5 split into Stage 5 (Packaging) + Stage 6 (Delivery) — user-
  visible workflow change
- ~30 correctness / security bugs closed across the publish / install /
  share pipeline (handcrafted-tar bypass + 10 more bypasses found by
  iterative review)
- New state sentinels: data/.scaffold-state.json, data/.delivery-state.json
- New _common.py module factoring assert_archive_layout +
  write_delivery_state
- Command surface adjusted: /studio package and /studio status removed
  after their use cases were absorbed; /studio publish redefined as
  end-to-end orchestrator
- publish.py renamed to package.py to match what the script actually does
- ~45% reduction in always-loaded markdown tokens (aggressive trim of
  main SKILL.md + AGENTS.md + sub-skill SKILLs)

No breaking change to the install API contract (path_type/path_value
semantics unchanged); ecosystem packs built before this version remain
installable. Marketplace catalog will see the bumped version next time
the agent-studio pack is republished.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #118 Body

## Summary

Started as a fix for a production bug (a packed `zooclaw-social-0.1.0.tar.gz` deployed a bot that still self-identified as "Agent Studio"). Through 11 rounds of iterative independent review (Claude + Codex subagents), grew into a comprehensive hardening of the publish → install → share pipeline plus the Stage 5/6 architecture split. **Version bumped 1.0.1 → 1.1.0.**

## What's in this PR

### Architecture
- **Stage 5 "Publishing" → Stage 5 (Packaging) + Stage 6 (Delivery)**
- `publish.py` → `package.py` rename (script does packaging only; `/studio publish` is the end-to-end orchestrator)
- Two new state sentinels: `data/.scaffold-state.json` (Stage 3 done), `data/.delivery-state.json` (Stage 6 done)
- New `_common.py` module: shared `assert_archive_layout` + `write_delivery_state` + `DELIVERY_METHOD_*` constants
- Command surface settled to 7: `/dev` `/test` `/studio new` `/studio validate` `/studio publish` `/studio share` `/studio install`

### Bugs closed (~30 across the review loop)
The original publish bug + many derivatives, all introduced or exposed through normal use of the publish/install/share path:

- **Path safety**: `./agent/foo`, `/agent/foo`, `agent/../etc` all rejected
- **Member types**: symlinks / hardlinks / devices rejected
- **Required entry types**: required files must be regular files, not directories
- **Remote install**: now downloads + validates layout before submit (was the last bypass of the original PR mission)
- **Stage 6 detector**: version-aware (matches specific `<name>-<version>.tar.gz`, not "any archive")
- **`--source local` / `--source remote`**: don't write workspace's delivery sentinel for foreign archives
- **Install layout check**: applied to `.tar.gz` / `.tgz`; `.zip` removed from supported formats
- **`write_cron.py`**: no longer force-enables heartbeat as a side effect; YAML output via `json.dumps` handles colons / hashes / multi-line
- **`clean.py`**: deletes root `avatar.png`, recursively clears `agent/` subdirs, deletes manifest (so Stage 1 detector works), preserves `zip/` (versioned build history by design)
- **`derive_archive_metadata`**: unversioned filename returns `None` (was returning the full stem)
- **`read_pack_emoji`**: prefers `agent/IDENTITY.md` (pack's) over root `IDENTITY.md` (Studio's)
- **Validate**: `check_agent_completeness` now fails (not warns) on placeholder content; writes scaffold-state sentinel; new `check_listing_assets` warns on missing `description.json` / `avatar.png`
- TOCTOU on remote validation documented as a known architectural limitation (closing it requires backend hash-pin support)

### Documentation
- **-45% always-loaded markdown tokens** (aggressive trim of main SKILL.md / AGENTS.md / sub-skill SKILLs; per-stage references trimmed)
- New "Truth sources" section names the 4 distinct signals (`.scaffold-state.json`, `.delivery-state.json`, `validate.py`, `data/config.json`) and their scopes
- agent-pack.yaml description, BOOTSTRAP.md, AGENTS.md command table all sync to 6-stage flow
- New `references/delivery.md` for Stage 6

## Why so many commits

11 rounds of independent code review (Claude `feature-dev:code-reviewer` + Codex `codex:codex-rescue`) consistently surfaced additional bugs adjacent to each fix. The dual-source review caught 3 Critical bugs in rounds 8-10 (symlink bypass, directory-as-required-file, absolute-path entries) that single-source review would have missed — Claude reached "PR ready" at round 8; Codex kept finding until round 11.

## Test plan

- [x] All Python scripts pass `py_compile`
- [x] `package.py` emits a clean archive that passes its own `assert_archive_layout` self-check
- [x] Symlink / directory / absolute-path / parent-traversal hand-crafted archives all rejected with clear errors
- [x] `/studio install --source remote` downloads + validates before submit (tested with local `http.server` serving a bad archive)
- [x] `/studio share --internal-stage` (used by `install.py` staging) skips delivery sentinel; without the flag still writes it
- [x] `/studio new` preserves `zip/` (versioned build history); clears `data/`, `agent/` subdirs, root listing assets
- [x] `validate.py` second run on unchanged state is idempotent (no fs write)
- [x] Pack identity for foreign archives derives from filename, not workspace manifest
- [x] PR description, manifest, root docs all reference 6-stage flow consistently

## Independent in-pod verification

Bundled this `agent-studio@1.1.0` into a 5.7 docker image (test-only branch in `openclaw-docker`, PR SerendipityOneInc/openclaw-docker#76 — not for merge) and drove a full Stage 1 → 5 build with Studio acting as a creator-facing agent. Confirmed:

- **Stage 1–3**: Studio's bundled archive layout passes `assert_archive_layout`; on first message it ran discovery → skill-design → scaffolded a fresh creator workspace (`agent/AGENTS.md`/`SOUL.md`/`IDENTITY.md`/`HEARTBEAT.md` plus a `gmail-digest` skill and an auto-added `pack-onboarding` skill, scripts compiled, `data/.scaffold-state.json` flipped to `agent_dir_filled: true`)
- **Stage 5 packaging**: Studio's `/studio publish` produced `zip/gmail-digest-0.1.0.tar.gz` (13 entries, 10 KB). Independent `assert_archive_layout` check on the result: **layout ok** (root files present, skills under `.agents/skills/`, no forbidden top-level dirs)
- **Stage 6 install/share guardrails**: with `PUBLIC_URL_PREFIX` deliberately unset (local Mac, no public artifact host), `/studio install` and `/studio share` **both refused to submit**, surfacing a clear diagnostic and three sensible recovery paths instead of silently misdelivering. This is exactly the failure-mode the publish/install/share hardening was meant to produce — no silent fallthrough to a bad backend submission
- **`agent-studio-install` env requirements**: skill correctly blocked when `USER_INTERNAL_TOKEN` was missing from the container env; cleared when the env var was set

What in-pod verification did NOT cover (requires a deployed pod, not in scope for this PR): full ECAP backend round-trip, `/studio install --source remote` against a real share URL, and `/test`-mode behavior of the built pack.

## Migration

- Packs at `agent-studio` 1.0.x continue to install; no breaking change to install API
- Workspaces upgraded from 1.0.x: state files are forward-compatible (validate.py recreates `.scaffold-state.json` on first run)
- Marketplace catalog updates to `v1.1.0` on next republish

## Follow-ups (not blocking)

~20 deferred items tracked at `~/workspace/design-doc/ecap-agent-pack/agent-studio/pr-118-followups.md`, organized by area:
- **Highest priority**: `write_onboarding.py` generated `provision.py` / `finalize.py` are stubs (don't implement what `automation.md` promises)
- Embedded-manifest identity for install (vs filename heuristic)
- `package.py agent/` rglob whitelist
- `validate.py` + `scaffold.py` alignment with manifest schema
- `clean.py` --confirm dead flag + failure containment

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
