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

## `40ae2169` Align designer CLI usage and fix hardcoded /extra-skills paths (#85)
- **作者**: tim-srp
- **时间**: 2026-04-16T09:46:26Z
- **链接**: [40ae2169](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/40ae2169550f77e265de9c66dd394c4d9f841aee)

## `440dde63` chore: remove obsolete /extra-skills path references from prompts and docs (#84)
- **作者**: tim-srp
- **时间**: 2026-04-16T09:20:32Z
- **链接**: [440dde63](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/440dde63bfce0bdeac8d09842d6ed2249b797752)

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

