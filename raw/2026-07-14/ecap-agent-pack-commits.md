# ecap-agent-pack commits — 2026-07-14

## fix(agent-studio): bump pack version 2.2.5 -> 2.2.6 for the kb_ref release (#207)
- sha: `1b681a6a42dbb0172c2baac62013ff2afbe4e91a`
- 作者: kyle-srp
- 日期: 2026-07-14T03:30:42Z
- PR: #207 by kyle-srp — https://github.com/SerendipityOneInc/ecap-agent-pack/pull/207

**Commit message:**

```
fix(agent-studio): bump pack version 2.2.5 -> 2.2.6 for the kb_ref release (#207)

#206 bumped agent-studio to 2.2.5 and published it; #205 (merged after)
changed agent-studio content (kb_ref references + validator) but left the
version at 2.2.5, so re-publishing 409s with pack.version_exists. Bump to
2.2.6 so the kb_ref-aware Studio content can ship.

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

**PR body:**

## Why

The staging deploy of the kb_ref change (#205) failed at *Upload agent-studio release* with:

```
409 {"code":"pack.version_exists","detail":"Pack version already exists"}
```

Root cause: #206 bumped `agent-studio/agent-pack.yaml` to `2.2.5` **and published it**. #205 merged afterward and changed agent-studio content (`references/knowledge-base.md`, `references/skill-design.md`, `references/description-schema.ts`, `scripts/validate.py`, `AGENTS.md`) but left the version at `2.2.5` — so re-publishing the same version 409s. `version-check` didn't flag it because those paths aren't in its bump-required set.

## Fix

Bump to `2.2.6` so the kb_ref-aware Studio content (declaration guidance + validator) actually ships.

## After merge

Re-tag a staging beta (`v2.2.7-beta.0`) to trigger the release; it will publish agent-studio `2.2.6` cleanly.

Note: this only affects Agent Studio's authoring-time guidance/validation. The runtime kb_ref sharing path (publish → binding registration → install → search) is claw-interface + proxy and is already deployed to staging.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

