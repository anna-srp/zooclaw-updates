# ecap-skills - 2026-05-14 Commits
共 1 条 commit

---
## [1] 93b1c9c5
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T11:52:43Z
- **SHA**: 93b1c9c54b46e82fbed92398d5b764043342c2ac
- **PR**: #195

### Commit Message

```
docs: link to ecap-workspace architecture guide (#195)

Add a Cross-repo architecture section pointing to ecap-workspace's
architecture & external dependencies guide (EN + 中文), which documents
the full ECAP platform topology: which repo owns which piece, env var to
service map, and control-plane vs data-plane separation.

Originating PR: https://github.com/SerendipityOneInc/ecap-workspace/pull/1627

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

- Add a `## Cross-repo architecture` section to `CLAUDE.md` linking to ecap-workspace's architecture guide (EN + 中文).
- Originating PR: https://github.com/SerendipityOneInc/ecap-workspace/pull/1627 documents the full ECAP platform topology; this repo is named there as the LLM-driven skill code loaded by OpenClaw bot pods at runtime.

## Test plan

- [ ] Confirm the two links resolve once the ecap-workspace PR lands on main.
- [ ] No other content in `CLAUDE.md` is modified.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
