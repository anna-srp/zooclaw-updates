# SerendipityOneInc/ecap-skills — 2026-04-22

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
