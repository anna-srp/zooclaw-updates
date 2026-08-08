# SerendipityOneInc/ecap-skills — commits 2026-08-07

## feat: gate image and video generation with Creem moderation (#258)

- **SHA**: `af3919905a7968533b6472023c69715f31315d3f`
- **作者**: tim-srp
- **日期**: 2026-08-07T11:27:07Z
- **PR**: #258

### Commit Message

```
feat: gate image and video generation with Creem moderation (#258)

## Summary

- add Creem prompt moderation before `designer` image generation
- add the same gate before `video-generator` model discovery and
generation
- stop only for a successful moderation response with `decision: deny`;
fail open for all other decisions and moderation errors
- authenticate moderation requests with `USER_INTERNAL_TOKEN` and send
only the text prompt
- add focused unit coverage for decisions, authentication, failure
modes, and backend short-circuiting

## Impact

Published image and video generation CLIs now consult the
ecap-proxy-service moderation endpoint before invoking generation
providers. Existing generation behavior remains unchanged unless Creem
explicitly denies the prompt.

## Validation

- `python -m pytest -p no:cacheprovider
designer/tests/test_designer_creem_moderation.py
video-generator/tests/test_video_creem_moderation.py -q` — 22 passed
- `python -m py_compile designer/scripts/image_generation_cli.py
video-generator/scripts/video_generation_cli.py` — passed
- `python .github/scripts/lint_skills.py` — passed with 12 pre-existing
warnings
- `git diff --check` — passed

## Known repository baseline

Running the entire repository test suite currently stops during
collection with 19 unrelated errors in existing `pptx` and `council`
tests, caused by `pptx` module shadowing and conflicting `conftest.py`
imports.
```

### PR Body

## Summary

- add Creem prompt moderation before `designer` image generation
- add the same gate before `video-generator` model discovery and generation
- stop only for a successful moderation response with `decision: deny`; fail open for all other decisions and moderation errors
- authenticate moderation requests with `USER_INTERNAL_TOKEN` and send only the text prompt
- add focused unit coverage for decisions, authentication, failure modes, and backend short-circuiting

## Impact

Published image and video generation CLIs now consult the ecap-proxy-service moderation endpoint before invoking generation providers. Existing generation behavior remains unchanged unless Creem explicitly denies the prompt.

## Validation

- `python -m pytest -p no:cacheprovider designer/tests/test_designer_creem_moderation.py video-generator/tests/test_video_creem_moderation.py -q` — 22 passed
- `python -m py_compile designer/scripts/image_generation_cli.py video-generator/scripts/video_generation_cli.py` — passed
- `python .github/scripts/lint_skills.py` — passed with 12 pre-existing warnings
- `git diff --check` — passed

## Known repository baseline

Running the entire repository test suite currently stops during collection with 19 unrelated errors in existing `pptx` and `council` tests, caused by `pptx` module shadowing and conflicting `conftest.py` imports.


---

## feat: sync published skills to v2 registry (#249)

- **SHA**: `30916e14709d1e1dde96e790bf7dffd75d9d277d`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-07T04:00:48Z
- **PR**: #249

### Commit Message

```
feat: sync published skills to v2 registry (#249)

## What changed

> Reworked 2026-08-07 on top of the registry-publish relay that landed
in #252 — the earlier direct-controld approach
(`CONTROLD_BASE_URL`/`CONTROLD_ADMIN_TOKEN`) in this PR's first
iteration is gone.

- Add `PUBLISHED_SKILLS_V2` — a curated v2 registry allowlist (18
skills). v2 publication becomes a deliberate subset of
`PUBLISHED_SKILLS` instead of #252's publish-everything: held out with
reasons documented in the file are `ecap-io` (v1 ecap-card frontend
contract unverified in v2 channels), `cron-job` (targets the OpenClaw
built-in `cron` tool; v2 parity unverified), `specialist-manager`
(v1-only value chain), `_fonts` / `_BGM` (asset libraries, S3-only).
- Replace the staging job's inline registry-publish bash loop with
`.github/scripts/sync-v2-registry.mjs` (same relay transport and step
semantics — `POST /skills/registry-publish` with
`X-Skills-Publish-Token`, still blocking), adding:
- pre-upload guards, one directory walk per skill: un-hydrated Git LFS
pointers, symlinks (`zip -r` would embed target content past the
guards), uncompressed content > 50 MiB (the engine checks expanded
bytes);
- deterministic archives (staged copy, normalized mtimes, `zip -qrX`) —
defense-in-depth; the engine hashes the expanded manifest so idempotency
never depended on zip bytes;
- per-attempt timeouts and 3 retries with backoff on network errors/5xx
(4xx never retries; retries are safe — content-hash dedup);
- failure aggregation: attempt every skill, exit non-zero listing
failures;
- `--validate` (config + allowlist invariants, no network — wired into
the pre-S3 "Validate" step so a broken allowlist stops the publish
before the bucket mutates), `--dry-run`, `--only=a,b`.
- After all skills publish (and never for `--only` runs): `POST
/skills/registry-reconcile` with the full allowlist — registry skills
absent from it are deprecated (dropped from default auto-assembly; no
files/versions deleted). Endpoint added in ecap-workspace#3294.
- Dev and production jobs untouched (staging-only, matching #252).

## Why

v2 auto-assembles every active global skill into every agent, so the
registry set should be curated: some v1-published skills are broken or
meaningless in v2. Publish alone can only add — without reconcile,
narrowing the allowlist would leave retired skills active forever.

## Merge order

**ecap-workspace#3294 must merge and deploy to staging first** — the
registry step here calls `/skills/registry-reconcile` and (by landed
#252 design) fails the staging publish on error. No new secrets needed:
the step reuses `SKILLS_PUBLISH_BASE_URL` / `SKILLS_PUBLISH_TOKEN`
already configured for staging.

## Validation

- `node --check .github/scripts/sync-v2-registry.mjs`
- `--dry-run` → exactly the 18 allowlisted names, heldOut `[cron-job,
ecap-io, specialist-manager]`, wouldFail `[]`
- `--validate` → passes with env set, fails fast (`PUBLISH_BASE_URL is
required`) without
- Deterministic zip verified: two packagings with a perturbed mtime in
between → byte-identical archives
- `python3 .github/scripts/lint_skills.py` — all skills pass (12
pre-existing warnings)
- YAML parse + actionlint (only pre-existing custom runner-label
notices)

## Related

- Reconcile relay endpoint: SerendipityOneInc/ecap-workspace#3294
- Landed relay transport: #252, ecap-workspace#3198
- Engine auto-assembly deployment switch:
SerendipityOneInc/zooclaw-engine#573
- Dual-runtime skill hardening: #251 (merged)
- Phase 2 follow-up:
https://github.com/SerendipityOneInc/zooclaw-engine/issues/557

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01YSusgGXGYznJqAyiHnDyNz
```

### PR Body

## What changed

> Reworked 2026-08-07 on top of the registry-publish relay that landed in #252 — the earlier direct-controld approach (`CONTROLD_BASE_URL`/`CONTROLD_ADMIN_TOKEN`) in this PR's first iteration is gone.

- Add `PUBLISHED_SKILLS_V2` — a curated v2 registry allowlist (18 skills). v2 publication becomes a deliberate subset of `PUBLISHED_SKILLS` instead of #252's publish-everything: held out with reasons documented in the file are `ecap-io` (v1 ecap-card frontend contract unverified in v2 channels), `cron-job` (targets the OpenClaw built-in `cron` tool; v2 parity unverified), `specialist-manager` (v1-only value chain), `_fonts` / `_BGM` (asset libraries, S3-only).
- Replace the staging job's inline registry-publish bash loop with `.github/scripts/sync-v2-registry.mjs` (same relay transport and step semantics — `POST /skills/registry-publish` with `X-Skills-Publish-Token`, still blocking), adding:
  - pre-upload guards, one directory walk per skill: un-hydrated Git LFS pointers, symlinks (`zip -r` would embed target content past the guards), uncompressed content > 50 MiB (the engine checks expanded bytes);
  - deterministic archives (staged copy, normalized mtimes, `zip -qrX`) — defense-in-depth; the engine hashes the expanded manifest so idempotency never depended on zip bytes;
  - per-attempt timeouts and 3 retries with backoff on network errors/5xx (4xx never retries; retries are safe — content-hash dedup);
  - failure aggregation: attempt every skill, exit non-zero listing failures;
  - `--validate` (config + allowlist invariants, no network — wired into the pre-S3 "Validate" step so a broken allowlist stops the publish before the bucket mutates), `--dry-run`, `--only=a,b`.
- After all skills publish (and never for `--only` runs): `POST /skills/registry-reconcile` with the full allowlist — registry skills absent from it are deprecated (dropped from default auto-assembly; no files/versions deleted). Endpoint added in ecap-workspace#3294.
- Dev and production jobs untouched (staging-only, matching #252).

## Why

v2 auto-assembles every active global skill into every agent, so the registry set should be curated: some v1-published skills are broken or meaningless in v2. Publish alone can only add — without reconcile, narrowing the allowlist would leave retired skills active forever.

## Merge order

**ecap-workspace#3294 must merge and deploy to staging first** — the registry step here calls `/skills/registry-reconcile` and (by landed #252 design) fails the staging publish on error. No new secrets needed: the step reuses `SKILLS_PUBLISH_BASE_URL` / `SKILLS_PUBLISH_TOKEN` already configured for staging.

## Validation

- `node --check .github/scripts/sync-v2-registry.mjs`
- `--dry-run` → exactly the 18 allowlisted names, heldOut `[cron-job, ecap-io, specialist-manager]`, wouldFail `[]`
- `--validate` → passes with env set, fails fast (`PUBLISH_BASE_URL is required`) without
- Deterministic zip verified: two packagings with a perturbed mtime in between → byte-identical archives
- `python3 .github/scripts/lint_skills.py` — all skills pass (12 pre-existing warnings)
- YAML parse + actionlint (only pre-existing custom runner-label notices)

## Related

- Reconcile relay endpoint: SerendipityOneInc/ecap-workspace#3294
- Landed relay transport: #252, ecap-workspace#3198
- Engine auto-assembly deployment switch: SerendipityOneInc/zooclaw-engine#573
- Dual-runtime skill hardening: #251 (merged)
- Phase 2 follow-up: https://github.com/SerendipityOneInc/zooclaw-engine/issues/557

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01YSusgGXGYznJqAyiHnDyNz


---

## ci: move claude-review to Azure Foundry wiring (#257)

- **SHA**: `cdf634268b6f7c6b5ff60f9e356af9fc2dc591f7`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-07T03:55:51Z
- **PR**: #257

### Commit Message

```
ci: move claude-review to Azure Foundry wiring (#257)

## What changed

Swap the claude-review reusable's secret from `AWS_ROLE_TO_ASSUME`
(Bedrock) to `AZURE_OPENAI_API_KEY`, and pin `model: claude-sonnet-5` +
`effort: medium` — mirroring ecap-workspace's working wiring verbatim.

## Why

Every claude-review run in this repo currently fails: the model call
errors out (`is_error: true`, `total_cost_usd: 0`, no verdict) and the
reusable defaults to REQUEST_CHANGES, blocking the auto-review gate on
every PR (see #249's runs today — two identical "I'll analyze this and
get back to you" stubs). ecap-workspace migrated to Azure Foundry and
its claude-review passes; this repo's codex-review job already uses
`AZURE_OPENAI_API_KEY`, so the secret is present here.

## Validation

- YAML parses; diff is the secrets/with block only.
- Real validation is the first claude-review run on this PR itself.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01YSusgGXGYznJqAyiHnDyNz
```

### PR Body

## What changed

Swap the claude-review reusable's secret from `AWS_ROLE_TO_ASSUME` (Bedrock) to `AZURE_OPENAI_API_KEY`, and pin `model: claude-sonnet-5` + `effort: medium` — mirroring ecap-workspace's working wiring verbatim.

## Why

Every claude-review run in this repo currently fails: the model call errors out (`is_error: true`, `total_cost_usd: 0`, no verdict) and the reusable defaults to REQUEST_CHANGES, blocking the auto-review gate on every PR (see #249's runs today — two identical "I'll analyze this and get back to you" stubs). ecap-workspace migrated to Azure Foundry and its claude-review passes; this repo's codex-review job already uses `AZURE_OPENAI_API_KEY`, so the secret is present here.

## Validation

- YAML parses; diff is the secrets/with block only.
- Real validation is the first claude-review run on this PR itself.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01YSusgGXGYznJqAyiHnDyNz

---

## fix: v1/v2 dual-runtime hardening for published skills (#251)

- **SHA**: `9bb726a27f7f78560988051934544b4bd39e1880`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-07T03:02:44Z
- **PR**: #251

### Commit Message

```
fix: v1/v2 dual-runtime hardening for published skills (#251)

## What changed

- browser-skill: remove the git-tracked `.state.json` (contained a live
user JWT) and ignore it going forward; all invocation paths switch from
cwd-relative `node skills/browser-skill/...` to `{baseDir}/...`; the MCP
endpoint becomes overridable via `BROWSER_SKILL_MCP_URL`, and an
explicit env value now always wins over an endpoint persisted in the
state file.
- deep-research / ecap-io: drop dead `install: litellm` entries (neither
skill has scripts; `install: []` is the sanctioned form).
- xlsx: convert all `SKILL_DIR/` placeholders to `{baseDir}/` in
SKILL.md and every references/*.md.
- pptx: replace `~/.claude/skills/...` example paths in
references/shape-cli.md with the `{baseDir}` convention.
- CLAUDE.md + code-review.md: add v1/v2 dual-runtime compatibility rules
and a matching review checklist (path discipline via `{baseDir}`,
env-declared endpoints only, no committed credentials/state, skill dir
read-only at runtime, ≤50 MiB per skill, LFS hydration, both publish
whitelists considered).

## Why

v2 (zooclaw-engine) materializes skills content-addressed at
`/skills/{name}/` with v1-compat symlinks. Most skills port cleanly, but
cwd-relative paths, v1-mount hardcodes, and writable-skill-dir
assumptions silently break. These are the mechanical fixes; the
governance sections make dual-runtime compatibility a check-in
requirement so future skills stay portable.

## Impact

No behavior change in v1: `{baseDir}` is substituted by both runtimes,
and the browser-skill endpoint default is byte-identical when
`BROWSER_SKILL_MCP_URL` is unset.

## Security note (action required)

`browser-skill/.state.json` contained a live Bearer JWT (allenz@srp.one,
exp 2027-02). Deleting the file does not revoke it and it remains in git
history — **the token must be rotated out-of-band**.

## Validation

- `python3 .github/scripts/lint_skills.py` — all skills pass, 12
pre-existing warnings, none introduced
- `node --check` on both browser-skill scripts
- `grep` confirms zero remaining `node skills/browser-skill` refs, zero
`SKILL_DIR`, no tracked `.state.json`

## Related

- v2 registry sync + `PUBLISHED_SKILLS_V2` allowlist: #249
- Engine auto-assembly switch: SerendipityOneInc/zooclaw-engine (PR from
`feat/global-skills-auto-enable-switch`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01YSusgGXGYznJqAyiHnDyNz
```

### PR Body

## What changed

- browser-skill: remove the git-tracked `.state.json` (contained a live user JWT) and ignore it going forward; all invocation paths switch from cwd-relative `node skills/browser-skill/...` to `{baseDir}/...`; the MCP endpoint becomes overridable via `BROWSER_SKILL_MCP_URL`, and an explicit env value now always wins over an endpoint persisted in the state file.
- deep-research / ecap-io: drop dead `install: litellm` entries (neither skill has scripts; `install: []` is the sanctioned form).
- xlsx: convert all `SKILL_DIR/` placeholders to `{baseDir}/` in SKILL.md and every references/*.md.
- pptx: replace `~/.claude/skills/...` example paths in references/shape-cli.md with the `{baseDir}` convention.
- CLAUDE.md + code-review.md: add v1/v2 dual-runtime compatibility rules and a matching review checklist (path discipline via `{baseDir}`, env-declared endpoints only, no committed credentials/state, skill dir read-only at runtime, ≤50 MiB per skill, LFS hydration, both publish whitelists considered).

## Why

v2 (zooclaw-engine) materializes skills content-addressed at `/skills/{name}/` with v1-compat symlinks. Most skills port cleanly, but cwd-relative paths, v1-mount hardcodes, and writable-skill-dir assumptions silently break. These are the mechanical fixes; the governance sections make dual-runtime compatibility a check-in requirement so future skills stay portable.

## Impact

No behavior change in v1: `{baseDir}` is substituted by both runtimes, and the browser-skill endpoint default is byte-identical when `BROWSER_SKILL_MCP_URL` is unset.

## Security note (action required)

`browser-skill/.state.json` contained a live Bearer JWT (allenz@srp.one, exp 2027-02). Deleting the file does not revoke it and it remains in git history — **the token must be rotated out-of-band**.

## Validation

- `python3 .github/scripts/lint_skills.py` — all skills pass, 12 pre-existing warnings, none introduced
- `node --check` on both browser-skill scripts
- `grep` confirms zero remaining `node skills/browser-skill` refs, zero `SKILL_DIR`, no tracked `.state.json`

## Related

- v2 registry sync + `PUBLISHED_SKILLS_V2` allowlist: #249
- Engine auto-assembly switch: SerendipityOneInc/zooclaw-engine (PR from `feat/global-skills-auto-enable-switch`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01YSusgGXGYznJqAyiHnDyNz


---

## fix(council): estimate K_BY_DEPTH follows PR #255 schedule (#256)

- **SHA**: `044d8742100b19cb804b347a535786c1c430f3f5`
- **作者**: felix-srp
- **日期**: 2026-08-07T01:59:09Z
- **PR**: #256

### Commit Message

```
fix(council): estimate K_BY_DEPTH follows PR #255 schedule (#256)

## Problem (codex post-merge P1 on #255)

PR #255 changed SKILL.md's Stage 5 reviser schedule (`quick 0 · standard
0 · deep 1`) but `estimate_band.py` carries its own hardcoded
`K_BY_DEPTH` copy and prices synthesis as `1+K` spawns — so the confirm
gate overquoted every standard run (2 synthesis spawns priced, 1
actually spawned) and every deep run (3 vs 2). The gate is the user's
go/cancel decision point, so this is message-fidelity, not stale prose.
My #255 claim of "prose-only change" was wrong — codex caught it in
post-outage review.

## Fix

- `K_BY_DEPTH` → `{quick: 0, standard: 0, deep: 1}`; standard
fallback-band example now quotes 495/2580 (was 660/3440).
- Updated the pricing test's expectations.
- **New drift-gate test**
`test_k_by_depth_matches_skill_md_stage5_schedule`: parses the schedule
out of SKILL.md and enforces equality with the estimator's table — the
"MUST match SKILL.md" comment just failed its live trial, so the sync is
now machine-checked (same pattern as the composer-template drift gate).

## Verification

275 council tests pass (274 + new gate), lint clean.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## Problem (codex post-merge P1 on #255)

PR #255 changed SKILL.md's Stage 5 reviser schedule (`quick 0 · standard 0 · deep 1`) but `estimate_band.py` carries its own hardcoded `K_BY_DEPTH` copy and prices synthesis as `1+K` spawns — so the confirm gate overquoted every standard run (2 synthesis spawns priced, 1 actually spawned) and every deep run (3 vs 2). The gate is the user's go/cancel decision point, so this is message-fidelity, not stale prose. My #255 claim of "prose-only change" was wrong — codex caught it in post-outage review.

## Fix

- `K_BY_DEPTH` → `{quick: 0, standard: 0, deep: 1}`; standard fallback-band example now quotes 495/2580 (was 660/3440).
- Updated the pricing test's expectations.
- **New drift-gate test** `test_k_by_depth_matches_skill_md_stage5_schedule`: parses the schedule out of SKILL.md and enforces equality with the estimator's table — the "MUST match SKILL.md" comment just failed its live trial, so the sync is now machine-checked (same pattern as the composer-template drift gate).

## Verification

275 council tests pass (274 + new gate), lint clean.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## perf(council): revision only at deep depth (K: standard 1→0, deep 2→1) (#255)

- **SHA**: `0d503bb63b16a82e67578555dc46afb6b56b41fc`
- **作者**: felix-srp
- **日期**: 2026-08-07T01:10:36Z
- **PR**: #255

### Commit Message

```
perf(council): revision only at deep depth (K: standard 1→0, deep 2→1) (#255)

## What

One-line change to Stage 5's K schedule: `quick 0 · standard 1 · deep 2`
→ `quick 0 · standard 0 · deep 1`. Standard runs (the default) become
composer-only; deep keeps one batched revision pass.

## Why

**Cost basis broke.** K-by-depth was ruled (design doc, 2026-07-11 blind
eval) when a full Stage 5 ran ~8–11 min. Production passes now cost
15–25 min each (bigger reports, 140K-context ingests, and an openclaw
idle-watchdog bug that kills+respawns long opus calls — 4/4 recent
aborts were synthesis sessions), making synthesis run 25–35 min against
the design doc's documented 3–5 min envelope.

**Quality evidence was always a weak trade.** The vault's blind eval
recorded: coverage/actionability ↑, calibration/citation ↓, K=2 over K=0
only 3-1 with a judge position-flip, diminishing pass-2 returns;
composer-only (K=0) beat the old v3 pipeline 4-0.

**A 2026 reflection survey confirms it on every axis** (30+ papers +
shipping systems): revision gains concentrate in pass 1 (Self-Refine,
Chain-of-Density, RefineBench); second passes undo earlier fixes and
citation faithfulness degrades universally across deep-research agents
(Mr DRE, ACL 2026 — break rate ~31%, worst-case −67pt faithfulness); no
flagship ships holistic draft revision (LangChain ODR explicitly
retreated to one-shot synthesis; the only shipped post-draft passes are
narrow grounded verification like Anthropic's CitationAgent). Deep's
single batched ≤8-edit pass is the literature-optimal form (Mr DRE
k-scaling: batching targets into one pass lowers break rate 32%→20%).

Full reconciliation recorded in the design doc as §9.12 (reviser origin,
cost drift, survey, ruling, shelved propose+apply redesign).

## Verification

274 council tests pass, lint clean. Prose-only change; the reviser
template and Stage 5(b) mechanics are unchanged (still used at deep).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## What

One-line change to Stage 5's K schedule: `quick 0 · standard 1 · deep 2` → `quick 0 · standard 0 · deep 1`. Standard runs (the default) become composer-only; deep keeps one batched revision pass.

## Why

**Cost basis broke.** K-by-depth was ruled (design doc, 2026-07-11 blind eval) when a full Stage 5 ran ~8–11 min. Production passes now cost 15–25 min each (bigger reports, 140K-context ingests, and an openclaw idle-watchdog bug that kills+respawns long opus calls — 4/4 recent aborts were synthesis sessions), making synthesis run 25–35 min against the design doc's documented 3–5 min envelope.

**Quality evidence was always a weak trade.** The vault's blind eval recorded: coverage/actionability ↑, calibration/citation ↓, K=2 over K=0 only 3-1 with a judge position-flip, diminishing pass-2 returns; composer-only (K=0) beat the old v3 pipeline 4-0.

**A 2026 reflection survey confirms it on every axis** (30+ papers + shipping systems): revision gains concentrate in pass 1 (Self-Refine, Chain-of-Density, RefineBench); second passes undo earlier fixes and citation faithfulness degrades universally across deep-research agents (Mr DRE, ACL 2026 — break rate ~31%, worst-case −67pt faithfulness); no flagship ships holistic draft revision (LangChain ODR explicitly retreated to one-shot synthesis; the only shipped post-draft passes are narrow grounded verification like Anthropic's CitationAgent). Deep's single batched ≤8-edit pass is the literature-optimal form (Mr DRE k-scaling: batching targets into one pass lowers break rate 32%→20%).

Full reconciliation recorded in the design doc as §9.12 (reviser origin, cost drift, survey, ruling, shelved propose+apply redesign).

## Verification

274 council tests pass, lint clean. Prose-only change; the reviser template and Stage 5(b) mechanics are unchanged (still used at deep).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
