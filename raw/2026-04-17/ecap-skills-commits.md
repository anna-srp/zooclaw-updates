# ecap-skills — 2026-04-17
共 1 条 commits

## `58392420` feat: add VS Code devcontainer with openclaw-docker image (#148)
- **作者**: allenz-srp
- **时间**: 2026-04-16T06:34:48Z
- **链接**: [58392420](https://github.com/SerendipityOneInc/ecap-skills/commit/583924205bb20f7464bed43c2fb5ae9a3aa1a41a)


**PR #148 Description:**
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
