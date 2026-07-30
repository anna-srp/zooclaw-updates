# SerendipityOneInc/ecap-skills commits — 2026-07-29

## feat(council): topic rewrite, citation completeness, blind-spot triage, member-chairs (#247)

- sha: edc97f48dfdc6cf31f48f47dfc4d1502abec2cfa
- author: felix-srp
- date: 2026-07-29T19:39:19Z
- PR: #247

### Commit message



### PR body

Staging-driven improvements across four areas (validated on betas v0.6.12-beta.6–.7, bot 9d52c157; design doc §9.9–§9.11).

## 1. Topic rewrite at Stage 0

Same input ("调研今年上半赛季F1") produced a 2025 full-season report on one pod and 2026-H1 on another — ambiguity resolution was implicit and per-model. Now: the topic is rewritten before `init` (same language, disambiguated only) and the rewrite is the sole topic everywhere. Deterministic references resolve against the CURRENT date silently; judgment calls surface as the panel's `Assumed:` line; an unattended coin-flip referent refuses the run (zero spend). The rewrite resolves references and never ASSERTS new facts (staging: an invented "第14站" fed members a false premise — caught and corrected by the report itself). Members get a `Today:` anchor. Referent-only boundary: no shared dimension framework is ever dispatched (anti-anchoring).

## 2. Citation completeness

Load-bearing secondhand claims: members chase them upstream before breadth, unreachable ones land in Risks, the composer's blind-spots section carries them onto the delivery's follow-up path. Data tables carry a source line beneath (member + composer/fallback templates, drift-gated pair).

## 3. Blind-spot triage replaces the mandatory gap-research pass

Forensics showed the old delivery gate was silently skipped, and following it would have spent deep-research passes on member-chased-dry items. Now: disclosed items stand; synthesis-emergent questions answerable by ≤3 direct searches get checked inline (no spawn); user-dependent items become questions; the triage outcome is one delivery line — never silent.

## 4. Member-chairs permitted (synthesizer∉members gate removed)

User decision: the blinding scrub stays, and the v3 composer merges rather than scores. Auto-picked chairs still prefer fresh eyes; only an explicit `synthesizer <model>` override seats a member as chair. The one real side effect — cast-pricing identity collisions letting an unpriced chair twin clobber a priced member entry — is fixed with a regression test. A two-topic appendix-blind A/B (design doc §9.11) validated the same-tier-chair option for fact-recap topics (~25–40% cheaper, equal quality) while confirming the opus default for judgment-heavy ones (it caught an arithmetic contradiction in circulating GMV figures that the same-tier chair credited).

## Review trail

13 bot rounds. Three codex P1s adjudicated: unattended judgment-call spend → fixed (Stage-0 refusal); non-version-suffix resolution → documented design boundary; cost-join collision → fixed (c51dbae). Final verdicts APPROVE / severity NONE; claude's last minor note (missing regression test) is factually covered by `test_cli_member_chair_overlap_keeps_the_priced_entry`.

## Testing

`uv run --with pytest,pyyaml,jsonschema -m pytest council/tests/` — 271 passed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01THqUHU4BtCMq7xLxE7ZPKa

---

## feat(council): one-expert-author synthesis, live series resolution, at-claim-site citations (#246)

- sha: a0f3b96ee56441185be15672cfe026654280f14e
- author: felix-srp
- date: 2026-07-29T08:25:58Z
- PR: #246

### Commit message



### PR body

Three staging-driven improvements to the council skill (validated on betas v0.6.12-beta.1–.5, bot 9d52c157).

## 1. Synthesize as one expert author (topic-matched persona, silent consensus)

A real staging report spent ~30% of its body on meta-commentary (methodology preamble, "四份分析高度一致" tags, per-section consensus grades). Recast synthesis deep-research-style:

- Composer picks the expert whose judgment the topic deserves and writes the whole report in that voice; the reader must never sense assembly from multiple reports — consensus tags/counts forbidden.
- Claim map demoted to private bookkeeping (travels only in the machine-read `council_analysis` fence).
- Calibration survives quietly: contradictions still present both sides (analyst voice), single-source hedges only on load-bearing claims, compact blind-spots section near the end.
- Reviser gains a voice hunt; composer + fallback `_SYNTHESIS_TEMPLATE` edited in lockstep, now **drift-gated by CI** (`test_composer_md_and_fallback_template_share_rules_1_to_6`).

## 2. Live series version resolution — series_latest pins removed

Staging caught the pinned map's blind spot: `claude-opus-5` was live on litellm but the standard chair kept resolving the hand-declared pin (`claude-opus-4-8`) — removals fail loud, arrivals told no one. User decision: version bumps must cost zero maintenance.

- `--propose-cast` resolves each preset series against the pod's per-run litellm catalog by version-free signature (`series_of`): newest version wins, stable ahead of prerelease at equal version.
- Line tokens survive the signature, so `flash-lite` never masquerades as `flash`; a non-version suffix (`-thinking`/`-mini`) is a product-line variant by design — seat skips visibly, remedy is a one-line `SERIES_STEMS` entry (adjudicated; asserted explicitly in tests).
- `series_latest` deleted from `price_snapshot.json` (prices only); a version newer than the snapshot seats unpriced until `--refresh-prices`. Design doc §9.8 records the reversal of §9.6.

## 3. Citations at the claim site

Staging report had a Sources bank but almost no in-text citations. Restored the #126/D12-strength mandate in all three templates (member, composer, fallback): every key claim carries an inline markdown-link citation at the claim site — a trailing Sources list alone is NOT citation; reviser hunts uncited key claims.

## Review trail

9 bot review rounds. Both codex P1s adjudicated: opus-pin concern superseded by live resolution; non-version-suffix boundary is the documented, user-decided design (final claude verdict: severity NONE, "Both prior P1s resolved"). `need-human-review` labels removed after adjudication comment.

## Testing

- `uv run --with pytest,pyyaml,jsonschema -m pytest council/tests/` — 271 passed.
- End-to-end against the real staging catalog (39 ids): economy/standard/premium casts all resolve correctly (standard chair = claude-opus-5); image/video/wrapper ids excluded.
- Staging betas .1–.5 published for live validation.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01THqUHU4BtCMq7xLxE7ZPKa

---

## fix(cron-job): block unsafe message relays (#245)

- sha: db36893defa94c55bfd003b259a5b012b0145b08
- author: sharplee-srp
- date: 2026-07-29T07:06:38Z
- PR: #245

### Commit message



### PR body

## Summary

- Make `cron-job` discoverable for creating, updating, repairing, and diagnosing scheduled jobs, and define it as the Cron workflow source of truth.
- Block preparation when a stored payload invokes `openclaw message send` or uses `sessions_send` as a persistent-session relay.
- Add a read-only stored-job scan that reports stable hazard codes without emitting raw payload text.
- Preserve explicit provider-consistency checks and require confirmation instead of guessing when routing is ambiguous.
- Document the routing decision order and the residual risk that direct production Cron mutations can still bypass the workflow until a runtime guard exists.

## Root cause

The messaging CLI bypasses the in-process `message` tool's routing policy and produces no `messageToolSentTo` evidence. The incident jobs previously appeared healthy only while their orchestration content used that CLI path. A later repair attempted `sessions_send`, which cannot relay from an isolated Cron into an unrelated persistent session under `tools.sessions.visibility=tree`.

Detailed Cron behavior also needs one authoritative home. Agent-level policies now state when to invoke this skill and provide only a minimal fallback when it is unavailable.

## Impact

Unsafe messaging paths are rejected before scheduler mutation and can be flagged in read-only job snapshots. Provider/account mismatches and ambiguous routes stop for confirmation, and session-tree isolation is not relaxed.

This PR adds procedural workflow enforcement only; it does not claim to prevent direct in-process Cron tool bypasses at runtime.

## Validation

- `python3 -m py_compile cron-job/scripts/cron_workflow.py`
- `python3 cron-job/scripts/cron_workflow.py --self-test` — 139 assertions passed
- `uv run --with pyyaml python3 .github/scripts/lint_skills.py` — passed with 15 pre-existing warnings
- Exercised the new `--scan-jobs` CLI against a safe/unsafe fixture.
- `git diff --check`

## Companion changes

Companion PRs reduce `openclaw-docker` and `ecap-agent-pack` policies to skill delegation plus a minimal safe fallback.


---
