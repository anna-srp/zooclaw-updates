# SerendipityOneInc/ecap-skills — 2026-04-16 Commits

共 4 条 commits

| SHA | 作者 | 日期 | Message | 链接 |
|-----|------|------|---------|------|
| `58392420` | allenz-srp | 2026-04-16 | feat: add VS Code devcontainer with openclaw-docker image (#148) | [link](https://github.com/SerendipityOneInc/ecap-skills/commit/583924205bb20f7464bed43c2fb5ae9a3aa1a41a) |
| `fce74446` | felix-srp | 2026-04-15 | fix(web-designer): move build/artifacts out of read-only skill directory (#152) | [link](https://github.com/SerendipityOneInc/ecap-skills/commit/fce74446bf0f48e2a7cb148916c1ffb35b3457f5) |
| `68449c40` | tim-srp | 2026-04-15 | Remove skill-crafting from published skills whitelist (#151) | [link](https://github.com/SerendipityOneInc/ecap-skills/commit/68449c40771f8a5585b43d2e919ef1c8dfba792a) |
| `88c50d4c` | tim-srp | 2026-04-15 | Add web-designer and skill-crafting to published skills whitelist (#150) | [link](https://github.com/SerendipityOneInc/ecap-skills/commit/88c50d4ca601ae1599f7e68370875e119dc42fc3) |

---
## PR Descriptions

### PR #148 — feat: add VS Code devcontainer with openclaw-docker image (#148)

## Summary
- Add `.devcontainer/` setup using `ghcr.io/serendipityoneinc/openclaw-docker:2026.3.13.36` as base image
- Mounts host `~/.claude`, `~/.claude.json`, `~/.config` into container for Claude Code and GCP auth
- Forces `linux/amd64` platform for Apple Silicon Mac compatibility
- VS Code opens at `/home/node/.openclaw/skills` matching production skill layout

## Test plan
- [ ] `Reopen in Container` on Mac (Apple Silicon)
- [ ] Verify `claude` CLI works inside container
- [ ] Verify skills directory matches `/home/node/.openclaw/skills/`

🤖 Generated with [Claude Code](https://claude.com/claude-code)
### PR #152 — fix(web-designer): move build/artifacts out of read-only skill directory (#152)

## Summary

- Redirect `.build/` (transient Vite workspace) from `$SKILL_DIR/.build/` to `/tmp/openclaw/web-designer/.build/` — matches the `/tmp` pattern used by pdf, pptx, docx, and other skills
- Redirect `artifacts/` (final bundled HTML output) from `$SKILL_DIR/artifacts/` to `$(pwd)/artifacts/` — the agent `cd`s to the workspace before calling `bundle.sh`, so `pwd` = workspace path
- Update SKILL.md to use `{workspace}` notation (workspace path is injected into the agent's system prompt at runtime)
- The skill directory is now fully read-only (only templates, scripts, and references are read from it)

## Test plan

- [ ] Deploy to zooclaw and run `bash scripts/init.sh test-project` — verify `.build/` is created under `/tmp/openclaw/web-designer/`, not the skill directory
- [ ] Run `cd {workspace} && bash scripts/bundle.sh test-project` — verify output lands in `{workspace}/artifacts/test-project/`
- [ ] Confirm the skill directory has zero new files written to it
- [ ] Verify the bundled HTML is accessible via zooclaw's HTTP serving

🤖 Generated with [Claude Code](https://claude.com/claude-code)
