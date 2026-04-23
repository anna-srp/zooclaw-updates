# ecap-agent-pack Commits - Last 7 Days


## 2026-04-23


今日无更新

## 2026-04-22


今日无更新

## 2026-04-21


共 1 条 commits

---

## [47f5fba8](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/47f5fba81927d466d60269731d750ece13ac9b8b)

**Author:** david-srp  
**Date:** 2026-04-20T07:45:22Z

**Message:**
```
feat(vibe-drama): upgrade to v1.0.9 workflow (#99)
```

## 2026-04-20


今日无更新

## 2026-04-19

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

## 2026-04-18


共 12 条 commits

- **[525fda8](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/525fda8d003353a173f624c2863c423edb6a18f4)** `2026-04-17` — fix(soulmate-pack): stop heartbeat spam + tune for real-partner cadence (#95)  
  作者: felix-srp

- **[a1cb0c9](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/a1cb0c92b0d696c6c7d8f6ebc6ac031c2448c851)** `2026-04-17` — feat(release): add versioned packaging and release compatibility (#94)  
  作者: nolan-srp

- **[6153a2f](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/6153a2fc3d21b144f6ba29646574a9a1890345e6)** `2026-04-17` — feat(release): add versioned agent packaging and validation (#93)  
  作者: nolan-srp

- **[8539d6e](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/8539d6e746f2e109266c9891dcbce535d240f7dc)** `2026-04-17` — soulmate-pack: simplify, fix stale code, align docs to code (#92)  
  作者: felix-srp

- **[09462d6](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/09462d61397d106b7438bff3ca0f8fde62c9ea68)** `2026-04-17` — agent-studio: explicit cron + heartbeat delivery policy (#91)  
  作者: felix-srp

- **[05ca59c](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/05ca59cbf690bfd7c800f7ab7278326feee8e28c)** `2026-04-17` — refactor: move pack skills under .agents (#90)  
  作者: nolan-srp

- **[669e486](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/669e4861462850bd2b3eb62b5d5d19e8b728cbd3)** `2026-04-17` — agent-studio: simplify instructions (-36% words) + clean up lifecycle scripts (#89)  
  作者: felix-srp

- **[8338793](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/8338793632a6d94db7f3dca24dc57406729f6baa)** `2026-04-17` — refactor: move agent-studio to .agents/skills/, pack skills under .agents/skills/, avatar & hidden-dir fixes (#79)  
  作者: felix-srp

- **[01ddc4e](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/01ddc4e258e2f1ae63b409ae7b48a0f4ce24667f)** `2026-04-17` — feat: add Deco home decor pack (v0.3.1) (#88)  
  作者: vincent-srp

- **[2219fc0](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/2219fc0c23732e566c29e9749f6a60f41712b60a)** `2026-04-17` — fix: backward compat for /extra-skills mount on older pods (#87)  
  作者: tim-srp

- **[54f755f](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/54f755f5c3d6baae9c24194e61049bfc313d241c)** `2026-04-17` — fix: soulmate session cooldown detection was completely broken (#74)  
  作者: tim-srp

- **[1be38e9](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/1be38e956d6c3026574455c36cf658a5de7dc7d3)** `2026-04-17` — improve: make bootstrap and session-start checks silent until onboarding begins (#67)  
  作者: Nemo Feng

## 2026-04-17

共 5 条 commits

## `5662c905` feat(podcast-pal): replace xelatex PDF pipeline with platform pdf skill (#80)
- **作者**: Nemo Feng
- **时间**: 2026-04-16T19:45:08Z
- **链接**: [5662c905](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/5662c90515940d55071b859446e04dd17982e0ca)

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

