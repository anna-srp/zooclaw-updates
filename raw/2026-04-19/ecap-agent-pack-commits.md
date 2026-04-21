# ecap-agent-pack Commits - 2026-04-19
共 2 条 commits

## [9382535b](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/9382535b39b73a6a3dd1626fb733702e3e20cdc4)
- **作者**: felix-srp
- **时间**: 2026-04-18T06:55:03Z
- **消息**: fix(soulmate-pack): moments paths + heartbeat intimacy gate + fresh-install signal + robustness (#96)
- **description**:
  ## Summary

  Original three bugs plus a multi-round review hardened the affected paths (concurrency, locale, upgrade).

  ### Original bug fixes
  1. **Moments viewer 403s on new media** — `moments.py` stored bare paths (`voice/x.ogg`) in `index.json`, which broke when the viewer was served from any URL base other than `artifacts/moments/`. Now stores workspace-relative paths (`artifacts/moments/voice/x.ogg`); HTML resolver prepends `/` for site-root-absolute URLs; legacy bare entries auto-migrate on `add`.
  2. **Heartbeat ignored intimacy level** — proactive sender picked `voice_message` / `selfie` / `video` at L0 Stranger, and text drifted into soulmate-tier on day one. Added action gates in `should_message.py` (voice @ L2, selfie @ L3, video @ L5) and per-level tone guidance in `HEARTBEAT.md`.
  3. **Fresh-install detection broke on pack updates** — switched signal from `BOOTSTRAP.md` (restored on every update) to `data/.onboarded` sentinel written atomically last by `provision.py`.

  ### Review-round hardening (rounds 1–7)
  - **moments.py**: `save_index` atomic via `tempfile.mkstemp` + `os.replace`; `_migrate_bare_paths` guarded against non-dict / None entries; URI scheme regex prevents corrupting `data:` / `blob:` / `https:` URLs; `list`/`view` are now strictly read-only.
  - **should_message.py**: level parse wrapped in try/except + clamped to `max(0, level)`; `_persist_next_send` uses same atomic-unique-tmp pattern.
  - **intimacy.py**: `save` now atomic.
  - **provision.py + reset.py**: `.onboarded` written last during provision, cleared on reset.
  - **Upgrade path**: `AGENTS.md` + `HEARTBEAT.md` step 1 now requires both `.onboarded` AND `config.json`+`intimacy.json` check so pre-sentinel installs self-heal without re-onboarding.
  - **Locale hardening**: all JSON / MD read/write sites now pass `encoding="utf-8"` explicitly.

## [029e6f1c](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/029e6f1c4f8bec819b648d14ba811a7c9c042eb6)
- **作者**: felix-srp
- **时间**: 2026-04-18T05:41:21Z
- **消息**: fix: drop broken {baseDir} placeholder from all SKILL.md files (#98)
- **description**:
  ## Summary

  Nothing in openclaw or pi-coding-agent substitutes `{baseDir}` — it stays literal in the prompt. Agents see `{baseDir}/scripts/foo.py` and have to *guess* what directory it means. In prod this produced wrong paths (e.g. `skills/sm-relationship/scripts/intimacy.py` instead of the correct `.agents/skills/sm-relationship/scripts/intimacy.py`).

  openclaw's skills prompt already instructs: *"When a skill file references a relative path, resolve it against the skill directory."* So plain relative paths work correctly — the `{baseDir}/` prefix was pure noise across the monorepo.

  ### What changed
  - Stripped `{baseDir}/` from 32 files (173 occurrences), leaving plain relative paths.
  - Rewrote `agent-studio/.agents/skills/agent-studio/references/skill-design.md` and `SKILL.md`, which were actively recommending the broken pattern.
  - Normalized tarot `../../data` paths to `../../../data` to match stylist's convention.

  ### Scope (by pack)
  | Pack | Files |
  |---|---|
  | soulmate-pack | 2 |
  | office-pack | 6 |
  | oura-ring-connector | 1 |
  | tarot | 3 |
  | foxmkt-metaads | 1 |
  | agent-studio | 6 |
  | stylist-agent | 12 |
  | design-researcher | 1 |
