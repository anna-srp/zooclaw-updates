# ecap-agent-pack — 2026-04-17
共 5 条 commits

## `5662c905` feat(podcast-pal): replace xelatex PDF pipeline with platform pdf skill (#80)
- **作者**: Nemo Feng
- **时间**: 2026-04-16T19:45:08Z
- **链接**: [5662c905](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/5662c90515940d55071b859446e04dd17982e0ca)

**PR #80 Description:**
## Summary

- Remove all LaTeX/xelatex machinery from the `podcast-pdf` skill: deleted the 197-line `.tex` template and 168-line `compile-pdf.sh` compilation script
- Replace the 8-step xelatex workflow with a 6-step workflow that invokes the pre-loaded platform **pdf skill** for rendering
- Rewrite `paper-notes.md` writing rules in Markdown (headings, blockquotes, image syntax) instead of LaTeX commands
- Strip `xelatex` from `cli_dependencies`, `integrations`, and lazy-dependency-check rules across `agent-pack.yaml`, `AGENTS.md`, `SOUL.md`, `description.json`, and `pack-onboarding/SKILL.md`
- All content-quality rules preserved: thematic organization, direct quotes with attribution, highlight callouts, figures, bilingual support, no-fabrication rule

## Test plan

- [ ] Verify `grep -ri "xelatex\|texlive\|ctex\|compile-pdf\|kpsewhich" podcast-pal/` returns no results
- [ ] Confirm `podcast-pal/skills/podcast-pdf/assets/` and `scripts/` directories no longer exist
- [ ] Read `SKILL.md` — confirm 6-step flow with clear pdf-skill invocation instruction in Step 5
- [ ] Read `paper-notes.md` — confirm all writing rules use Markdown syntax, no LaTeX, no dependency section

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `e9b98246` Fix generate_collage.py fallback: emit path, not image_url (#86)
- **作者**: tim-srp
- **时间**: 2026-04-16T10:18:56Z
- **链接**: [e9b98246](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/e9b98246a52855692215c1db10308c40691a7213)

**PR #86 Description:**
## Summary

Follow-up to #85. The designer CLI writes its output to a local file and prints the file path on stdout (not a URL). After that rename was picked up in #85, the `generate_collage.py` fallback branch started storing the local path under the `image_url` JSON key — callers then tried to use it as a remote URL and failed.

## Why

- `litellm.aimage_generation` (primary path) returns a real URL — safe to emit as `image_url`.
- The designer CLI (fallback path) only writes a local file at `/tmp/openclaw/designer/<hash>.png` and prints that path on stdout. A local path under a key named `image_url` is a lie — downstream callers (Step 8 in `outfit-recommendation/SKILL.md`) treated it as a URL and the image failed to attach.
- The sibling `make_product_grid.py` in the same directory already established the convention: when the value is a local file, use `path`. This PR aligns `generate_collage.py`'s fallback branch with that convention.

## Changes

- `generate_collage.py` (fallback branch of `main()`): emit `{"status": "ok", "path": "/tmp/openclaw/designer/...", "fallback": true, ...}` instead of stuffing a local path under `image_url`.
- Update `outfit-recommendation/SKILL.md` Step 7 to document the two possible return shapes (primary → `image_url`, fallback → `path`).
- Update `generate_collage.py` module docstring to describe the two stdout JSON shapes.

## Contract change

`generate_collage.py` now emits either `image_url` (remote URL from primary path) or `path` (local file from fallback) — never both. Callers must check for both keys.

## Test plan

- [ ] Exercise the primary path — confirm output still contains `image_url`
- [ ] Force the fallback path (e.g. by disabling network to litellm) — confirm output contains `path` with a real local file
- [ ] Confirm downstream flow in `outfit-recommendation/SKILL.md` Step 8 attaches the collage correctly in both cases

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `40ae2169` Align designer CLI usage and fix hardcoded /extra-skills paths (#85)
- **作者**: tim-srp
- **时间**: 2026-04-16T09:46:26Z
- **链接**: [40ae2169](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/40ae2169550f77e265de9c66dd394c4d9f841aee)

**PR #85 Description:**
## Summary

Follow-up to #84. Handles two remaining issues that #84 did not cover:

1. **Hardcoded `/extra-skills/...` paths in bash blocks and Python subprocess calls** — these were out of scope for #84 (which only handled prose references) but still break after fastclaw PR #56 remapped the mount point.
2. **Designer CLI upstream renamed `--image-urls` to `--images`** and changed stdout from JSON to a plain file path.

## Changes

- Replace `--image-urls` → `--images` across all bash examples, docs, and prose (stylist-agent, soulmate-pack)
- Replace `/extra-skills/<skill>/...` → `~/.openclaw/skills/<skill>/...`
  - Bash blocks rely on shell tilde expansion
  - Python `subprocess.run` call sites use `os.path.expanduser(...)`
- Update `stylist-agent/.../generate_collage.py` `fallback_generate()` to parse the new plain-path stdout and widen return type to `str | None`

## Affected agents

- stylist-agent
- soulmate-pack
- restaurant-review-monitor
- zoodance-vibe-drama

## Test plan

- [ ] Verify `stylist-agent` virtual try-on runs end-to-end with the new `--images` flag
- [ ] Verify `soulmate-pack` onboarding face-blend and sm-photo selfie generation still work
- [ ] Verify `restaurant-review-monitor` daily digest cron can resolve `~/.openclaw/skills/websearch/...` at runtime
- [ ] Verify `zoodance-vibe-drama` beat generation can resolve `~/.openclaw/skills/chameleon/...`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `440dde63` chore: remove obsolete /extra-skills path references from prompts and docs (#84)
- **作者**: tim-srp
- **时间**: 2026-04-16T09:20:32Z
- **链接**: [440dde63](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/440dde63bfce0bdeac8d09842d6ed2249b797752)

**PR #84 Description:**
## Summary

Part 1 of cleanup following [fastclaw#56](https://github.com/SerendipityOneInc/fastclaw/pull/56), which remounted ecap-skills at `~/.openclaw/skills/` (managed priority level 3) instead of `/extra-skills/` (extra priority level 1). Since managed > bundled in OpenClaw's load order, the old \"Prefer /extra-skills\" prompt hack and hardcoded `/extra-skills/xxx` path references in docs are obsolete — skills are now referenced by name and resolved by the skill system.

## Changes

**A. Delete obsolete \"Tool Routing Policy (Extra Skills First)\" section — 5 files**
- `careerbloom/AGENTS.md`
- `oura-ring-connector/AGENTS.md`
- `podcast-pal/AGENTS.md`
- `restaurant-review-monitor/AGENTS.md`
- `stylist-agent/AGENTS.md`

**B. Drop Path column from TOOLS.md skill table — 1 file**
- `design-researcher/TOOLS.md`

**C. Replace `/extra-skills/<name>` text references with skill names — 3 files**
- `design-researcher/skills/dr-report-builder/SKILL.md` (2 refs)
- `foxmkt-metaads/skills/mkt-meta-ads-pro/SKILL.md` (2 refs)
- `stylist-agent/TOOLS.md` (1 ref — prose only, executable bash block kept for follow-up)

## Out of scope (follow-up PR)

Remaining 15 `/extra-skills/` references split into two categories that require more thought — intentionally deferred:

- **D. Executable bash blocks in SKILL.md** (9 occurrences, 6 files): `python3 /extra-skills/websearch/scripts/websearch.py ...` — these are instructions the LLM literally executes. To remove the path, they need to be refactored into \"call the `<name>` skill with params X\" so the LLM routes through the skill system.
- **E. Python scripts with hardcoded subprocess paths** (6 occurrences, 3 files): `WS_SCRIPT = '/extra-skills/...'` + `subprocess.run([...])` — needs either an `OPENCLAW_HOME` env var or a deeper refactor to remove cross-skill subprocess coupling.

## Test plan

- [ ] Manual review of each modified AGENTS.md to confirm the surrounding document still reads correctly (no orphaned \"## Output Format Policy\" gap)
- [ ] Manual review of TOOLS.md tables still render
- [ ] No behavior change expected at runtime — these are all prompt/documentation-layer strings. Skill loading still works via OpenClaw's managed-priority resolution (fastclaw#56)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `ac399082` fix(oura-ring-connector, podcast-pal): move config to ~/.config for persistence across claw restarts (#83)
- **作者**: Nemo Feng
- **时间**: 2026-04-16T02:40:52Z
- **链接**: [ac399082](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/ac399082c54faecaba307d7fe5299aac9e39ff85)

**PR #83 Description:**
## Summary
- Migrate all runtime data paths in `oura-ring-connector` from `~/.oura-ring/` to `~/.config/oura-ring/`
- Migrate all runtime data paths in `podcast-pal` from `~/.podcast-pal/` to `~/.config/podcast-pal/`
- Ensures config, auth tokens, and cached data persist across claw container restarts, since `~/.config` is a preserved mount point

## Files changed
29 files across both agent packs (AGENTS.md, BOOTSTRAP.md, HEARTBEAT.md, SOUL.md, agent-pack.yaml, skill definitions, and scripts)

## Test plan
- [ ] Verify onboarding writes config to the new `~/.config/<pack-name>/` path
- [ ] Verify heartbeat checks read from the updated paths
- [ ] Confirm data persists after a claw restart

🤖 Generated with [Claude Code](https://claude.com/claude-code)

