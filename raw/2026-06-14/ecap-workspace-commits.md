# SerendipityOneInc/ecap-workspace — commits 2026-06-14

共 1 个 commit


## chore(agents): unify repo skill configuration (#2436)

- **SHA**: `1bc75f95b914b06efaa33f275fdbcef4f5bef001`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-14T01:58:47Z
- **PR**: #2436

### 完整 Commit Message

```
chore(agents): unify repo skill configuration (#2436)

## Summary
- Add repo-level Codex config for SessionStart hooks plus pinned
Context7 and Playwright MCP servers.
- Make `.agents/skills` the canonical repo skill source and project
Claude skills as symlinks.
- Keep Sentry enabled as a skill/plugin in both Claude and Codex: Claude
uses `sentry@claude-plugins-official` plus
`sentry-cli@claude-plugins-official`; Codex uses
`sentry@openai-curated`. Live data access can still use MCP/app/CLI
surfaces, while the Sentry skill carries useful SDK/API and triage
workflow knowledge.
- Add `scripts/sync-agent-skills.sh` and external-skill lock metadata to
validate vendored skill hashes, Claude symlinks, stale symlinks, Sentry
plugin availability, and Codex config. First-party repo skills are
tracked by Git instead of hash-locked.

## Test plan
- [x] `bash -n scripts/sync-agent-skills.sh
scripts/sync-agent-skills.test.sh scripts/hooks/session-start-fetch.sh
scripts/hooks/guard-screenshot-path.sh`
- [x] `bash scripts/sync-agent-skills.test.sh`
- [x] `bash scripts/sync-agent-skills.sh --apply`
- [x] `GIT_CONFIG_GLOBAL=/dev/null bash scripts/verify-changed.sh`
- [x] Codex repo MCP smoke with temporary project trust: `context7` and
`playwright` listed from `.codex/config.toml`
- [x] Codex real-config prompt-input smoke: `sentry:sentry` appears from
`sentry@openai-curated` in this repo
```

### PR Body

## Summary
- Add repo-level Codex config for SessionStart hooks plus pinned Context7 and Playwright MCP servers.
- Make `.agents/skills` the canonical repo skill source and project Claude skills as symlinks.
- Keep Sentry enabled as a skill/plugin in both Claude and Codex: Claude uses `sentry@claude-plugins-official` plus `sentry-cli@claude-plugins-official`; Codex uses `sentry@openai-curated`. Live data access can still use MCP/app/CLI surfaces, while the Sentry skill carries useful SDK/API and triage workflow knowledge.
- Add `scripts/sync-agent-skills.sh` and external-skill lock metadata to validate vendored skill hashes, Claude symlinks, stale symlinks, Sentry plugin availability, and Codex config. First-party repo skills are tracked by Git instead of hash-locked.

## Test plan
- [x] `bash -n scripts/sync-agent-skills.sh scripts/sync-agent-skills.test.sh scripts/hooks/session-start-fetch.sh scripts/hooks/guard-screenshot-path.sh`
- [x] `bash scripts/sync-agent-skills.test.sh`
- [x] `bash scripts/sync-agent-skills.sh --apply`
- [x] `GIT_CONFIG_GLOBAL=/dev/null bash scripts/verify-changed.sh`
- [x] Codex repo MCP smoke with temporary project trust: `context7` and `playwright` listed from `.codex/config.toml`
- [x] Codex real-config prompt-input smoke: `sentry:sentry` appears from `sentry@openai-curated` in this repo


### 变更文件

- `.agents/skills/archive-shipped-doc/SKILL.md`
- `.agents/skills/archive-shipped-doc/references/classification-rules.md`
- `.agents/skills/bulk-archive-shipped-docs/SKILL.md`
- `.agents/skills/diff-stats/SKILL.md`
- `.agents/skills/diff-stats/scripts/stats.py`
- `.agents/skills/sync-docs/SKILL.md`
- `.agents/skills/sync-docs/references/drift-sources.md`
- `.agents/skills/sync-docs/scripts/drift-probe.sh`
- `.claude/commands/sync-docs.md`
- `.claude/settings.json`
- `.claude/skills/arch-review`
- `.claude/skills/archive-shipped-doc`
- `.claude/skills/bulk-archive-shipped-docs`
- `.claude/skills/diff-stats`
- `.claude/skills/feature`
- `.claude/skills/pr`
- `.claude/skills/release`
- `.claude/skills/release-notes`
- `.claude/skills/sync-docs`
- `.claude/skills/telep`
- `.codex/config.toml`
- `AGENTS.md`
- `scripts/README.md`
- `scripts/sync-agent-skills.sh`
- `scripts/sync-agent-skills.test.sh`
- `skills-lock.json`
