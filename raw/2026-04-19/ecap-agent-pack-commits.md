# ecap-agent-pack Commits - 2026-04-19
共 2 条 commits

## [9382535b](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/9382535b39b73a6a3dd1626fb733702e3e20cdc4)
- **作者**: felix-srp
- **时间**: 2026-04-18T06:55:03Z
- **消息**: fix(soulmate-pack): moments paths + heartbeat intimacy gate + fresh-install signal + robustness (#96)

```
* fix(soulmate-pack): moments paths, heartbeat intimacy gate, stable fresh-install signal

- moments.py: store workspace-relative paths (artifacts/moments/...) instead of
  bare (voice/x.ogg) so the viewer works when served from any URL base, plus
  auto-migrate legacy bare entries on add/list/view. moments.html resolver
  prepends "/" for workspace-relative paths and falls back to /artifacts/moments/
  for legacy entries.
- should_message.py: gate action_type by intimacy level (voice >= L2, sel
```

## [029e6f1c](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/029e6f1c4f8bec819b648d14ba811a7c9c042eb6)
- **作者**: felix-srp
- **时间**: 2026-04-18T05:41:21Z
- **消息**: fix: drop broken {baseDir} placeholder from all SKILL.md files (#98)

```
* fix: drop broken {baseDir} placeholder from all SKILL.md files

Nothing in openclaw or pi-coding-agent substitutes {baseDir}. Agents saw
the literal token and had to guess what directory it meant. In prod this
produced wrong paths (e.g. `skills/sm-relationship/scripts/intimacy.py`
instead of the correct `.agents/skills/sm-relationship/scripts/intimacy.py`).

openclaw's skills prompt already instructs: "When a skill file references
a relative path, resolve it against the skill directory." So pl
```

