# ecap-agent-pack Commits — 2026-05-13

仓库: SerendipityOneInc/ecap-agent-pack  
日期: 2026-05-13 (UTC)  
Commits 数量: 1

---

## Commit 1

**SHA**: d38d7430  
**作者**: 未知  
**日期**: 2026-05-13  
**PR**: #120

### 完整 Commit Message

```
feat(agent-studio): v1.2.0 — close 20 PR #118 follow-ups (onboarding scripts, package hardening, validate/scaffold alignment, clean.py rewrite) (#120)

* fix(agent-studio): real onboarding scripts + tighten package.py allow-list

Closes follow-ups OB-1, OB-2, OB-3, PK-1, PK-2 from PR #118.

- OB-1/OB-2: provision.py now mechanically substitutes {{key}} /
  {{config.key}} placeholders in SOUL.md and IDENTITY.md instead of just
  appending a HTML comment; finalize.py reads data/*_baseline.json and
  writes MEMORY.md + data/plan.json instead of TODO stubs. Lift both
  scripts (plus add_cron.py) out of write_onboarding.py's triple-quoted
  string constants into templates/onboarding/*.py — kills the \{ regex
  escaping and makes the generated code directly lintable.
- OB-3: new add_cron.py mechanically resolves {{config.*}} from
  data/config.json before the agent calls the cron tool, exiting 1 on
  missing keys or delivery fields (silent-misdelivery prevention).
- PK-1: package.py walks agent/ via a strict allow-list (AGENTS.md,
  IDENTITY.md, SOUL.md, BOOTSTRAP.md, HEARTBEAT.md, TOOLS.md) instead of
  rglob — runtime residue (MEMORY.md, USER.md, memory/, helper scripts)
  no longer leaks into the archive.
- PK-2: _clean_agent_file takes has_avatar from the caller; package.py
  no longer copies avatar.png into artifacts/.agents/ as a presence
  marker, so a failed package leaves no working-tree residue.

* fix(agent-studio): close round-1 review findings

- add_cron.py: treat None/"" as missing, accept 0/False (valid falsy config values).
- provision.py: exit 1 on unresolved {{...}} placeholders; collect substitutions
  first and write atomically; skip personalization when agent/ subdir is present
  (/test mode in Agent Studio).
- finalize.py: surface corrupt baseline filenames in the output JSON.
- write_onboarding.py: render cron heredoc unindented so the EOF terminator
  stays at column 0.
- package.py: clarify SOUL.md cleaner is legacy backward-compat.

* fix(agent-studio): close round-2 review findings

- provision.py: write data/config.json AFTER validation, not before.
  The sentinel was previously persisted before the unresolved-placeholder
  check, leaving a false-complete state on _fail and suppressing re-onboarding.
```

### PR #120 Body

```
## Summary

Agent Studio v1.1.0 → **v1.2.0**. Closes 20 follow-ups from the post-PR-#118 backlog:
all 🟠 High items minus the cross-service IN-1/2/4 (need OpenClaw backend) and VA-6
(Stage-4 sentinel — separate design), plus 5 🟡 Medium and 2 🟢 Low.

## Closed (20)

**Onboarding scripts** — real implementations replace stubs / LLM string-edits:
- **OB-1** `provision.py` mechanically substitutes `{{key}}` / `{{config.key}}` in
  SOUL.md/IDENTITY.md; exits 1 on unresolved placeholders; skips in /test mode.
- **OB-2** `finalize.py` reads config + `data/*_baseline.json`, writes `MEMORY.md` +
  `data/plan.json`; corrupt baselines surfaced in `corrupt_baselines` output field.
- **OB-3** new `add_cron.py` mechanically resolves `{{config.*}}` in cron templates;
  exits 1 on missing/empty keys (accepting valid `0` / `False`) and missing required
  delivery fields — closes the silent-misdelivery hole.

**Package.py hardening**:
- **PK-1** Replaced `agent_dir.rglob` with strict `_AGENT_PACKABLE` allow-list so
  runtime residue (`MEMORY.md`, `USER.md`, `memory/`, helper scripts) no longer leaks.
- **PK-2** `_clean_agent_file` takes `has_avatar: bool`; removed the `pack_dir/artifacts/.agents/avatar.png` working-tree side effect.

**Validate / scaffold alignment**:
- **VA-1** `check_crossrefs` accepts both `skills/<n>/...` and `.agents/skills/<n>/...` reference forms.
- **VA-2** `agent/SOUL.md` now required by structure check.
- **VA-3** `scaffold.py` emits `cli_dependencies: []` and `data_sources: []` sections.
```
