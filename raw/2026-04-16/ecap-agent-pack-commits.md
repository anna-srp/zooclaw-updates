# SerendipityOneInc/ecap-agent-pack — 2026-04-16 Commits

共 6 条 commits

| SHA | 作者 | 日期 | Message | 链接 |
|-----|------|------|---------|------|
| `e9b98246` | tim-srp | 2026-04-16 | Fix generate_collage.py fallback: emit path, not image_url (#86) | [link](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/e9b98246a52855692215c1db10308c40691a7213) |
| `40ae2169` | tim-srp | 2026-04-16 | Align designer CLI usage and fix hardcoded /extra-skills paths (#85) | [link](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/40ae2169550f77e265de9c66dd394c4d9f841aee) |
| `440dde63` | tim-srp | 2026-04-16 | chore: remove obsolete /extra-skills path references from prompts and docs (#84) | [link](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/440dde63bfce0bdeac8d09842d6ed2249b797752) |
| `ac399082` | Nemo Feng | 2026-04-16 | fix(oura-ring-connector, podcast-pal): move config to ~/.config for persistence across claw restarts (#83) | [link](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/ac399082c54faecaba307d7fe5299aac9e39ff85) |
| `8fec0358` | Leah-srp | 2026-04-15 | chore(pptx-master): replace with pptx-master-0.1.0 release (#82) | [link](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/8fec035842d7e8e57117855a739c22b5f7679be2) |
| `d04a8106` | nolan-srp | 2026-04-15 | chore: agent pack uploaded by david@srp.one (#81) | [link](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/d04a81066de89b385b5aafdb708f3667d32b497e) |

---
## PR Descriptions

### PR #86 — Fix generate_collage.py fallback: emit path, not image_url (#86)

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
### PR #85 — Align designer CLI usage and fix hardcoded /extra-skills paths (#85)

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
### PR #83 — fix(oura-ring-connector, podcast-pal): move config to ~/.config for persistence 

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
