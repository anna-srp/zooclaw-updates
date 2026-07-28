# SerendipityOneInc/ecap-workspace commits — 2026-07-27


## 39f54714f9  (PR #3074)

- **SHA**: `39f54714f9d78cadebcb0a567e0ce6ff1bb37ab3`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-07-27T13:09:54Z
- **PR**: #3074 — docs(council): add council runs api spec and implementation plan

### Commit message

```
docs(council): add council runs api spec and implementation plan (#3074)

## Summary

Design spec + implementation plan for the **Council Runs API**: the
`claw-interface` backend that lets the upcoming `/council` web page
execute real multi-model council runs through the `council` skill
(SerendipityOneInc/ecap-skills) on the user's OpenClaw bot pod.

- `docs/superpowers/specs/2026-07-27-council-runs-api.md` — the design:
backend as a **run broker** (never an orchestrator), preset tiers with
skill-side casting, unattended dispatch via a versioned Mattermost
message template, token-authenticated pod callback events, `result.json`
v1 contract ingested from R2, per-stage watchdog, static tier×depth
estimate bands.
- `docs/superpowers/plans/2026-07-27-council-runs-api.md` — 12
bite-sized TDD tasks with test/implementation code, grounded in existing
claw-interface conventions (favie_common mongo wrapper + CAS
`find_one_and_update` transitions, typed repo pattern,
`get_current_user` auth, APScheduler jobs, import-linter triple-list
rule).

## Key v1 decisions (from design discussion)

1. Preset tiers only (`economy`/`standard`); the skill's own `roster.py`
resolves the concrete cast on the pod — no models API, no live estimates
in v1.
2. **Attended gate, mirrored in the web UI**: the skill runs its native
confirm gate; a structured `awaiting_go` callback carries the real cast
+ the pod's own quote to a web confirmation view; the user's Go posts
the literal `go` into the run thread. Runs are created in the DB at
topic submission (`go` is a transition, not a creation); unaccepted
gates expire to `cancelled` via watchdog.
2b. **Per-run Mattermost thread** as the dispatch vehicle
(session-channel flow, template as the initial thread message) — the
skill's organic progress one-liners and delivery summary stay contained
in one thread instead of spamming the user's DM; machine status still
flows through callbacks only.
3. **Two callbacks only + snapshot polling**: the pod POSTs
`awaiting_go` (proposal + its self-named `run_dir` + a `status_url` for
its uploaded `status.json`) and the terminal `completed`/`failed`
(per-run hashed token). Mid-run progress = a claw-interface poller
fetching the status snapshot (~20s, stage/member mapping pinned to
ecap-skills `status_schema.json`, write-on-change so watchdog staleness
survives). The skill runs fully native — nothing imposed on its folder
naming; linkage is reported, and the backend only ever follows reported
URLs. Frontend still polls `GET /council/runs/{id}` only.
4. Results as a script-assembled, schema-validated `result.json` on R2;
raw reports served only through an owner-checked proxy.
5. Fewer-than-2-survivors, watchdog timeouts, and dispatch failures all
land as explicit `failed` runs — the UI never spins forever.

## Open questions flagged in the spec

- Bot identity (v1 default: the user's own bot; isolated in one
function)
- Plan gating for tiers
- Callback ingress base URL per environment

## Test plan

- [x] Docs-only change — no code, no CI-affecting surfaces
- [ ] Follow-up PRs implement the plan task-by-task (backend slice),
plus the ecap-skills export/callback PR and frontend de-fixturing
tracked in the spec's Dependencies/Out-of-scope sections
```

### PR body

## Summary

Design spec + implementation plan for the **Council Runs API**: the `claw-interface` backend that lets the upcoming `/council` web page execute real multi-model council runs through the `council` skill (SerendipityOneInc/ecap-skills) on the user's OpenClaw bot pod.

- `docs/superpowers/specs/2026-07-27-council-runs-api.md` — the design: backend as a **run broker** (never an orchestrator), preset tiers with skill-side casting, unattended dispatch via a versioned Mattermost message template, token-authenticated pod callback events, `result.json` v1 contract ingested from R2, per-stage watchdog, static tier×depth estimate bands.
- `docs/superpowers/plans/2026-07-27-council-runs-api.md` — 12 bite-sized TDD tasks with test/implementation code, grounded in existing claw-interface conventions (favie_common mongo wrapper + CAS `find_one_and_update` transitions, typed repo pattern, `get_current_user` auth, APScheduler jobs, import-linter triple-list rule).

## Key v1 decisions (from design discussion)

1. Preset tiers only (`economy`/`standard`); the skill's own `roster.py` resolves the concrete cast on the pod — no models API, no live estimates in v1.
2. **Attended gate, mirrored in the web UI**: the skill runs its native confirm gate; a structured `awaiting_go` callback carries the real cast + the pod's own quote to a web confirmation view; the user's Go posts the literal `go` into the run thread. Runs are created in the DB at topic submission (`go` is a transition, not a creation); unaccepted gates expire to `cancelled` via watchdog.
2b. **Per-run Mattermost thread** as the dispatch vehicle (session-channel flow, template as the initial thread message) — the skill's organic progress one-liners and delivery summary stay contained in one thread instead of spamming the user's DM; machine status still flows through callbacks only.
3. **Two callbacks only + snapshot polling**: the pod POSTs `awaiting_go` (proposal + its self-named `run_dir` + a `status_url` for its uploaded `status.json`) and the terminal `completed`/`failed` (per-run hashed token). Mid-run progress = a claw-interface poller fetching the status snapshot (~20s, stage/member mapping pinned to ecap-skills `status_schema.json`, write-on-change so watchdog staleness survives). The skill runs fully native — nothing imposed on its folder naming; linkage is reported, and the backend only ever follows reported URLs. Frontend still polls `GET /council/runs/{id}` only.
4. Results as a script-assembled, schema-validated `result.json` on R2; raw reports served only through an owner-checked proxy.
5. Fewer-than-2-survivors, watchdog timeouts, and dispatch failures all land as explicit `failed` runs — the UI never spins forever.

## Open questions flagged in the spec

- Bot identity (v1 default: the user's own bot; isolated in one function)
- Plan gating for tiers
- Callback ingress base URL per environment

## Test plan

- [x] Docs-only change — no code, no CI-affecting surfaces
- [ ] Follow-up PRs implement the plan task-by-task (backend slice), plus the ecap-skills export/callback PR and frontend de-fixturing tracked in the spec's Dependencies/Out-of-scope sections


---

## cb0107224c  (PR #3084)

- **SHA**: `cb0107224c781c347b8bb19650d55168a0924c39`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-07-27T12:51:06Z
- **PR**: #3084 — docs: refresh workspace AGENTS.md set and add enterprise-admin guide

### Commit message

```
docs: refresh workspace AGENTS.md set and add enterprise-admin guide (#3084)

## Summary

Docs-only refresh of the workspace `AGENTS.md` set (every file has a
`CLAUDE.md` symlink, so both Codex and Claude pick these up).

- **`web/app/AGENTS.md`** — two new rules requested by Bill:
1. **API access goes through the claw proxy, split into models +
services**: default transport is `callClawInterfaceAPI` →
`/api/claw/[...path]`; per domain, types in `src/models/<domain>.ts` +
data access in `src/services/<domain>.ts` + RQ hooks in
`src/hooks/queries/<domain>/`.
2. **Page-style changes use design-system components first**: priority
`@zooclaw/design-system` → `@/components/ds/*` shadcn primitives →
last-resort hand-rolled. Section renamed "shadcn-first" → "design-system
first" to match.
- **`web/enterprise-admin/AGENTS.md`** — new file (+ `CLAUDE.md`
symlink), written from a read of the app, covering its deliberate
divergences from `web/app`: MVVM zero-logic pages (`useXxxViewModel`
co-located hooks), single claw-proxy transport + `api<T>()` +
`types/<domain>.ts` layering, `zc-*` token design language with local
`ui.tsx` primitives (lucide icons, no `@zooclaw/design-system` dep),
context-based i18n, no-`.env`-wiring gotcha, co-located Vitest tests,
`enterprise-admin-quality` CI, and the `eslint-config-next@16` hoist
trap.
- **Root `AGENTS.md`** — fixed stale Project/Stack/CI sections: the
monorepo is 3 frontend apps + 4 services (`whatsapp-business-service`,
`oauth-worker`, `r2-access-worker` were unmentioned) + iOS; CI section
now names the real `code-quality.yml` jobs (the previous `code-quality /
lint-and-test` and `python-code-quality / build-and-test` don't exist).
Sub-project Context links all five sub-docs.
- **`ios/ZooClaw/AGENTS.md`** — the most drifted: removed the invalid
macOS build recipe (`SUPPORTED_PLATFORMS = iphoneos iphonesimulator`, no
macOS destination) and related stale claims (multi-platform targets,
AuthService-on-macOS issue, wrong `ios/` git-root claim); documented the
simulator build/test recipe, the clang-probe-hang-under-load gotcha, the
`ios-quality` CI job (SwiftLint `--strict` + sim build/test pinned to
`iPhone 16,OS=18.6`), and the tag-driven release flow
(`ios-v*-beta.*`/`-rc.*`/`-release`); fixed renamed chat views
(`ChatListView` → `ChatMessageList`) and replaced the Design Documents
section whose 8 linked docs no longer exist.
- **`services/claw-interface/AGENTS.md`** — retitled to AGENTS.md, added
the CI job name, and codified standing API design conventions previously
living only in review feedback: GET/POST only, runtime-agnostic agent
APIs, PATCH schemas rejecting explicit null + `exclude_none`, typed
Pydantic repo boundaries with `model_validate`, `datetime.UTC`,
`mongo.update`/`mongo.delete` wrappers.
- **`web/AGENTS.md`** — enumerated the actual four `packages/` (incl.
`zooclaw-design-system`) and linked both app-level docs.

All factual claims (CI job names, iOS `SUPPORTED_PLATFORMS`, view/file
renames, package lists, env vars, proxy modules) were verified against
the current tree before writing.

## Test plan
- [x] Docs-only change — no code paths affected; `git diff` reviewed
- [x] Verified referenced files/jobs exist (`code-quality.yml` jobs,
`lib/claw-proxy.ts`, `zooclaw-design-system` exports, iOS pbxproj
platforms)
- [x] `web/enterprise-admin/CLAUDE.md` symlink matches the repo-wide
`CLAUDE.md → AGENTS.md` convention
```

### PR body

## Summary

Docs-only refresh of the workspace `AGENTS.md` set (every file has a `CLAUDE.md` symlink, so both Codex and Claude pick these up).

- **`web/app/AGENTS.md`** — two new rules requested by Bill:
  1. **API access goes through the claw proxy, split into models + services**: default transport is `callClawInterfaceAPI` → `/api/claw/[...path]`; per domain, types in `src/models/<domain>.ts` + data access in `src/services/<domain>.ts` + RQ hooks in `src/hooks/queries/<domain>/`.
  2. **Page-style changes use design-system components first**: priority `@zooclaw/design-system` → `@/components/ds/*` shadcn primitives → last-resort hand-rolled. Section renamed "shadcn-first" → "design-system first" to match.
- **`web/enterprise-admin/AGENTS.md`** — new file (+ `CLAUDE.md` symlink), written from a read of the app, covering its deliberate divergences from `web/app`: MVVM zero-logic pages (`useXxxViewModel` co-located hooks), single claw-proxy transport + `api<T>()` + `types/<domain>.ts` layering, `zc-*` token design language with local `ui.tsx` primitives (lucide icons, no `@zooclaw/design-system` dep), context-based i18n, no-`.env`-wiring gotcha, co-located Vitest tests, `enterprise-admin-quality` CI, and the `eslint-config-next@16` hoist trap.
- **Root `AGENTS.md`** — fixed stale Project/Stack/CI sections: the monorepo is 3 frontend apps + 4 services (`whatsapp-business-service`, `oauth-worker`, `r2-access-worker` were unmentioned) + iOS; CI section now names the real `code-quality.yml` jobs (the previous `code-quality / lint-and-test` and `python-code-quality / build-and-test` don't exist). Sub-project Context links all five sub-docs.
- **`ios/ZooClaw/AGENTS.md`** — the most drifted: removed the invalid macOS build recipe (`SUPPORTED_PLATFORMS = iphoneos iphonesimulator`, no macOS destination) and related stale claims (multi-platform targets, AuthService-on-macOS issue, wrong `ios/` git-root claim); documented the simulator build/test recipe, the clang-probe-hang-under-load gotcha, the `ios-quality` CI job (SwiftLint `--strict` + sim build/test pinned to `iPhone 16,OS=18.6`), and the tag-driven release flow (`ios-v*-beta.*`/`-rc.*`/`-release`); fixed renamed chat views (`ChatListView` → `ChatMessageList`) and replaced the Design Documents section whose 8 linked docs no longer exist.
- **`services/claw-interface/AGENTS.md`** — retitled to AGENTS.md, added the CI job name, and codified standing API design conventions previously living only in review feedback: GET/POST only, runtime-agnostic agent APIs, PATCH schemas rejecting explicit null + `exclude_none`, typed Pydantic repo boundaries with `model_validate`, `datetime.UTC`, `mongo.update`/`mongo.delete` wrappers.
- **`web/AGENTS.md`** — enumerated the actual four `packages/` (incl. `zooclaw-design-system`) and linked both app-level docs.

All factual claims (CI job names, iOS `SUPPORTED_PLATFORMS`, view/file renames, package lists, env vars, proxy modules) were verified against the current tree before writing.

## Test plan
- [x] Docs-only change — no code paths affected; `git diff` reviewed
- [x] Verified referenced files/jobs exist (`code-quality.yml` jobs, `lib/claw-proxy.ts`, `zooclaw-design-system` exports, iOS pbxproj platforms)
- [x] `web/enterprise-admin/CLAUDE.md` symlink matches the repo-wide `CLAUDE.md → AGENTS.md` convention


---

## ece7573ef6  (PR #3082)

- **SHA**: `ece7573ef6330a2da46dd9728e0d2ef59b72521d`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-07-27T11:43:59Z
- **PR**: #3082 — fix(claw-interface): whitelist engine persona docs

### Commit message

```
fix(claw-interface): whitelist engine persona docs (#3082)

## Summary
- define the exact case-sensitive zooclaw-engine persona document
allowlist, including `BOOTSTRAP.md`
- filter unsupported root Markdown during pack translation, Mongo
snapshot writes/reads, and agent create/update requests
- update the pack environment design contract and add regression
coverage for unsupported and legacy documents

## Root cause
claw-interface treated every workspace-root `*.md` file as a persona
document, while zooclaw-engine only consumes seven named files. As a
result, files such as `README.md`, `MEMORY.md`, and incorrectly cased
names could be persisted and sent to the engine.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] 219 related claw-interface unit tests
- [x] ruff, formatting, pyright, and import-linter
```

### PR body

## Summary
- define the exact case-sensitive zooclaw-engine persona document allowlist, including `BOOTSTRAP.md`
- filter unsupported root Markdown during pack translation, Mongo snapshot writes/reads, and agent create/update requests
- update the pack environment design contract and add regression coverage for unsupported and legacy documents

## Root cause
claw-interface treated every workspace-root `*.md` file as a persona document, while zooclaw-engine only consumes seven named files. As a result, files such as `README.md`, `MEMORY.md`, and incorrectly cased names could be persisted and sent to the engine.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] 219 related claw-interface unit tests
- [x] ruff, formatting, pyright, and import-linter


---

## 03e7052eae  (PR #3081)

- **SHA**: `03e7052eae01623f0cbbb4b60cda3db9e51d02f6`
- **作者**: shana-srp (shana-maker)
- **日期**: 2026-07-27T11:25:39Z
- **PR**: #3081 — fix(theme): align custom skin dark modes

### Commit message

```
fix(theme): align custom skin dark modes (#3081)

## Summary

- allow theme skin selection in light, dark, and system appearance modes
- add distinct Warm Ember and Mono OLED dark treatments for the two
selectable skins
- preserve each skin's light-mode icon, button, hover, and focus colors
in dark mode
- fix dark backgrounds on AI Specialists pages
- keep the page header status pill and settings navigation fixed when
switching skins

## Testing

- `PATH=/opt/homebrew/opt/node@24/bin:$PATH bash scripts/verify-web.sh
src/components/settings/GeneralTab.tsx
src/components/settings/SettingsLayout.tsx
src/theme/brand-theme-tokens.css
tests/unit/components/settings/GeneralTab.unit.spec.tsx
tests/unit/theme/brand-themes.unit.spec.ts`
- browser-verified light and dark switching for ZooClaw Editorial and
Productivity Flat
- browser-verified AI Specialists backgrounds and primary controls for
both skins
- browser-measured identical header and settings-nav coordinates across
all skins

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR body

## Summary

- allow theme skin selection in light, dark, and system appearance modes
- add distinct Warm Ember and Mono OLED dark treatments for the two selectable skins
- preserve each skin's light-mode icon, button, hover, and focus colors in dark mode
- fix dark backgrounds on AI Specialists pages
- keep the page header status pill and settings navigation fixed when switching skins

## Testing

- `PATH=/opt/homebrew/opt/node@24/bin:$PATH bash scripts/verify-web.sh src/components/settings/GeneralTab.tsx src/components/settings/SettingsLayout.tsx src/theme/brand-theme-tokens.css tests/unit/components/settings/GeneralTab.unit.spec.tsx tests/unit/theme/brand-themes.unit.spec.ts`
- browser-verified light and dark switching for ZooClaw Editorial and Productivity Flat
- browser-verified AI Specialists backgrounds and primary controls for both skins
- browser-measured identical header and settings-nav coordinates across all skins


---

## 31c5e062a8  (PR #3078)

- **SHA**: `31c5e062a8d467236952f073c5486368c730f16f`
- **作者**: kaka-srp (kaka-srp)
- **日期**: 2026-07-27T09:50:50Z
- **PR**: #3078 — fix(agent-builder): queue reconciled builder installs

### Commit message

```
fix(agent-builder): queue reconciled builder installs (#3078)

## Summary
- Preserve the Agent Builder install claim returned while project state
polling reconciles a newly ready Claw.
- Queue the existing background Agent Studio installer from the `/state`
route.
- Add regression coverage for the `computer_not_ready` → `ready`
transition.

## Root cause
When a project was created before its Claw became ready, the create
request correctly deferred Agent Studio installation. A later `/state`
poll claimed the workspace and returned `background_install_pack`, but
the service reduced that result to the project alone. The route
therefore never queued the installer, and every later poll only observed
the permanently `installing` workspace.

## Test plan
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest -q
tests/unit/test_agent_builder_routes.py
tests/unit/test_agent_builder_service.py`
- [x] Exact transition tests for the reconciled install claim and route
background task
- [x] `bash scripts/verify-py.sh`
- [x] Pre-push changed-surface verification
```

### PR body

## Summary
- Preserve the Agent Builder install claim returned while project state polling reconciles a newly ready Claw.
- Queue the existing background Agent Studio installer from the `/state` route.
- Add regression coverage for the `computer_not_ready` → `ready` transition.

## Root cause
When a project was created before its Claw became ready, the create request correctly deferred Agent Studio installation. A later `/state` poll claimed the workspace and returned `background_install_pack`, but the service reduced that result to the project alone. The route therefore never queued the installer, and every later poll only observed the permanently `installing` workspace.

## Test plan
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest -q tests/unit/test_agent_builder_routes.py tests/unit/test_agent_builder_service.py`
- [x] Exact transition tests for the reconciled install claim and route background task
- [x] `bash scripts/verify-py.sh`
- [x] Pre-push changed-surface verification


---

## c1bdc6c1e7  (PR #3075)

- **SHA**: `c1bdc6c1e7c7eb324c7083919e77a5f048878f8e`
- **作者**: srp-claude-assistant[bot] (srp-claude-assistant[bot])
- **日期**: 2026-07-27T08:21:04Z
- **PR**: #3075 — docs: sync-docs weekly sweep (2026-07-27)

### Commit message

```
docs: sync-docs weekly sweep (2026-07-27) (#3075)

## Tier 1 — Deterministic fixes

None. `drift-probe.sh` reported clean.

## Tier 2 — Semantic fixes (evidence-grounded)

- **`web/app/AGENTS.md` — `@zooclaw/chat-ui` barrel exports stale**
(evidence: `web/packages/chat-ui/src/index.ts` + PRs #2979, #2982,
#2985, #2990, #2994, #2996, #3010, #3011, #3013)
The doc said "the app currently consumes only `ChatComposer`". Since the
anchor commit (f5f63135), a series of extraction PRs moved ERMP cards,
file/image/audio/video attachments, specialist cards, `ModelPicker`,
`AgentPicker`, `SkillStoreDialog`, `SkillsSubMenu`, `UserMessage`,
`ToolGroup`, `InteractiveCards`, `ModelDegradationBanner`, and
`ChatUiProvider` into the package. The barrel export list in the doc now
matches `src/index.ts`.

- **`architecture.md` + `architecture.zh-CN.md` — `zooclaw-engine`
missing from Section B inventory** (evidence: architecture.md §C line
167, §E line 288, env var `ZOOCLAW_ENGINE_URL`)
`zooclaw-engine` is referenced in the data-flow section and the env-var
table but had no row in the external repository inventory (Section B).
Every other external service `claw-interface` depends on has an entry
there. Added a bilingual row describing its role as the managed-agent
runtime for engine-backed agents v2.

**Docs changed:** `web/app/AGENTS.md`, `architecture.md`,
`architecture.zh-CN.md`
**Window reviewed:** `f5f63135..HEAD` (2026-07-20 → 2026-07-27)

## Tier 3 — Suggestions (not applied)

- **`services/claw-interface/AGENTS.md` monorepo context table** still
lists `ecap-agent-platform (external) | 8001` as a local port. With the
engine-backed agents v2 architecture, the equivalent external runtime is
now `zooclaw-engine` reached via `ZOOCLAW_ENGINE_URL`. Whether to retire
the `ecap-agent-platform` row or update it requires a human decision
about whether that platform is still in active use.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: ecap-bot <ecap-bot@users.noreply.github.com>
Co-authored-by: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### PR body

## Tier 1 — Deterministic fixes

None. `drift-probe.sh` reported clean.

## Tier 2 — Semantic fixes (evidence-grounded)

- **`web/app/AGENTS.md` — `@zooclaw/chat-ui` barrel exports stale** (evidence: `web/packages/chat-ui/src/index.ts` + PRs #2979, #2982, #2985, #2990, #2994, #2996, #3010, #3011, #3013)
  The doc said "the app currently consumes only `ChatComposer`". Since the anchor commit (f5f63135), a series of extraction PRs moved ERMP cards, file/image/audio/video attachments, specialist cards, `ModelPicker`, `AgentPicker`, `SkillStoreDialog`, `SkillsSubMenu`, `UserMessage`, `ToolGroup`, `InteractiveCards`, `ModelDegradationBanner`, and `ChatUiProvider` into the package. The barrel export list in the doc now matches `src/index.ts`.

- **`architecture.md` + `architecture.zh-CN.md` — `zooclaw-engine` missing from Section B inventory** (evidence: architecture.md §C line 167, §E line 288, env var `ZOOCLAW_ENGINE_URL`)
  `zooclaw-engine` is referenced in the data-flow section and the env-var table but had no row in the external repository inventory (Section B). Every other external service `claw-interface` depends on has an entry there. Added a bilingual row describing its role as the managed-agent runtime for engine-backed agents v2.

**Docs changed:** `web/app/AGENTS.md`, `architecture.md`, `architecture.zh-CN.md`
**Window reviewed:** `f5f63135..HEAD` (2026-07-20 → 2026-07-27)

## Tier 3 — Suggestions (not applied)

- **`services/claw-interface/AGENTS.md` monorepo context table** still lists `ecap-agent-platform (external) | 8001` as a local port. With the engine-backed agents v2 architecture, the equivalent external runtime is now `zooclaw-engine` reached via `ZOOCLAW_ENGINE_URL`. Whether to retire the `ecap-agent-platform` row or update it requires a human decision about whether that platform is still in active use.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## 287855c6e4  (PR #3071)

- **SHA**: `287855c6e4f5fb209f6ac5716d0d8f529bfc59bd`
- **作者**: Chris@ZooClaw (chris-srp)
- **日期**: 2026-07-27T08:01:14Z
- **PR**: #3071 — feat(claw-interface): register pack skills into engine and pin on hire

### Commit message

```
feat(claw-interface): register pack skills into engine and pin on hire (#3071)

## 背景

Agent pack 自带 skills（`.agents/skills/*`）在 v2 迁移里被烤进 E2B
environment（`/opt/zooclaw/environment/pack/`），但**从未注册进 zooclaw-engine
registry**，所以引擎的 `renderSkills()` 从不把它们写进 agent 系统提示——模型看不到、永不触发。根因：走了
environment lane，而只有 skills-render lane 才喂 context。

本 PR 是 claw-interface 侧（跨仓 Part B），把 pack skills 改走规范 registry
lane。**配套引擎
PR**：[zooclaw-engine#435](https://github.com/SerendipityOneInc/zooclaw-engine/pull/435)（开
pack 注册写入口 `PUT /admin/v1/skills/pack/{pack_id}/{name}/versions`）。

## 改动

- **翻译**（`engine_pack_translation.py`）：`repack_workspace_zip` 把
`.agents/skills/**` 整棵子树排除出 environment 归档；新增 `extract_pack_skills` 抽出每个
skill（文件 + SKILL.md frontmatter，`yaml.safe_load`）。
- **引擎客户端**（`engine_client`）：新增 `admin_upsert_pack_skill_version` → `PUT
/admin/v1/skills/pack/{pack_id}/{name}/versions`（inline base64 files，复用
`/admin/v1` 同一 service token）；`create_agent`/`update_agent` 加可选 `skills`
参数。
- **approval
注册**（`pack_environment_service.run_post_approval`）：best-effort 注册每个
skill（单个失败告警跳过、不阻断 env build），把 `{skill_id, version}` 快照存进新的
submission-scoped repo（镜像 `pack_persona_docs`）。
- **装配**（`engine_agent_install_service`）：`_resolve_pack_skills` 读快照（缺失时
archive fallback 重新注册、幂等；与 persona 共用一次缓存的 translation），按与
`environment_id` 相同的可见性闸（`pack.org_id in (ZOOCLAW_ORG_ID, org_id)`）把
`skills=[{skill_id, version}]` pin 到 create + update 两条路径。

## 存储

新增 `ecap-pack-skill-versions` 集合 +
`pack_skill_versions_repo`（`upsert`/`get_by_submission`，唯一键
`pack_id+submission_id`），与 `pack_persona_docs` 同构；import-linter 三处清单同步。

## 测试

`tests/unit/` 扩展 4 个模块共 11 个新用例：translation 排除/抽取、client admin 路由 +
base64 body、approval 注册 + 快照、install 传 `skills=` + 快照缺失走 fallback。子代理本地跑
**135 passed** + ruff 全绿（用主 checkout 空 venv 无法联网装私有 `favie-common`，以公有
PyPI + `favie_common` stub 跑通；真实依赖集由本仓 CI 校验）。

## 边界 / 后续

- pack skill 受众当前恒 global（引擎 schema CHECK 禁止 pack 行带
org/owner；org/private pack 分树待引擎放宽）。
- 文档（Cloudflare managed-agents-site）已随引擎 PR #435 更新。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_012dJLqQhKkq4eZaQYDZg1Pm
```

### PR body

## 背景

Agent pack 自带 skills（`.agents/skills/*`）在 v2 迁移里被烤进 E2B environment（`/opt/zooclaw/environment/pack/`），但**从未注册进 zooclaw-engine registry**，所以引擎的 `renderSkills()` 从不把它们写进 agent 系统提示——模型看不到、永不触发。根因：走了 environment lane，而只有 skills-render lane 才喂 context。

本 PR 是 claw-interface 侧（跨仓 Part B），把 pack skills 改走规范 registry lane。**配套引擎 PR**：[zooclaw-engine#435](https://github.com/SerendipityOneInc/zooclaw-engine/pull/435)（开 pack 注册写入口 `PUT /admin/v1/skills/pack/{pack_id}/{name}/versions`）。

## 改动

- **翻译**（`engine_pack_translation.py`）：`repack_workspace_zip` 把 `.agents/skills/**` 整棵子树排除出 environment 归档；新增 `extract_pack_skills` 抽出每个 skill（文件 + SKILL.md frontmatter，`yaml.safe_load`）。
- **引擎客户端**（`engine_client`）：新增 `admin_upsert_pack_skill_version` → `PUT /admin/v1/skills/pack/{pack_id}/{name}/versions`（inline base64 files，复用 `/admin/v1` 同一 service token）；`create_agent`/`update_agent` 加可选 `skills` 参数。
- **approval 注册**（`pack_environment_service.run_post_approval`）：best-effort 注册每个 skill（单个失败告警跳过、不阻断 env build），把 `{skill_id, version}` 快照存进新的 submission-scoped repo（镜像 `pack_persona_docs`）。
- **装配**（`engine_agent_install_service`）：`_resolve_pack_skills` 读快照（缺失时 archive fallback 重新注册、幂等；与 persona 共用一次缓存的 translation），按与 `environment_id` 相同的可见性闸（`pack.org_id in (ZOOCLAW_ORG_ID, org_id)`）把 `skills=[{skill_id, version}]` pin 到 create + update 两条路径。

## 存储

新增 `ecap-pack-skill-versions` 集合 + `pack_skill_versions_repo`（`upsert`/`get_by_submission`，唯一键 `pack_id+submission_id`），与 `pack_persona_docs` 同构；import-linter 三处清单同步。

## 测试

`tests/unit/` 扩展 4 个模块共 11 个新用例：translation 排除/抽取、client admin 路由 + base64 body、approval 注册 + 快照、install 传 `skills=` + 快照缺失走 fallback。子代理本地跑 **135 passed** + ruff 全绿（用主 checkout 空 venv 无法联网装私有 `favie-common`，以公有 PyPI + `favie_common` stub 跑通；真实依赖集由本仓 CI 校验）。

## 边界 / 后续

- pack skill 受众当前恒 global（引擎 schema CHECK 禁止 pack 行带 org/owner；org/private pack 分树待引擎放宽）。
- 文档（Cloudflare managed-agents-site）已随引擎 PR #435 更新。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_012dJLqQhKkq4eZaQYDZg1Pm


---

## efe35d7f8f  (PR #3027)

- **SHA**: `efe35d7f8fe7943b08203f0c8200e691e75fb5a8`
- **作者**: Chris@ZooClaw (chris-srp)
- **日期**: 2026-07-27T07:01:17Z
- **PR**: #3027 — docs(e2e): plan remaining production failures

### Commit message

```
docs(e2e): plan remaining production failures (#3027)

## Summary

- documents the 2026-07-22 production E2E baseline: 75 stable passes, 5
flaky, 12 failed, 4 intentional skips, and 26 tests blocked by serial
suites
- maps every final failure and every did-not-run scenario to its
blocker, with evidence and confidence levels
- proposes five implementation phases in execution order: shared harness
fixes, removal of unnecessary serial coupling,
file-generation/low-credit and remaining targeted fixes, the four
fixture/CSS gaps, then targeted-to-full production validation
- defines completion as two consecutive full production runs with all
122 discovered tests passing and zero skipped, flaky, failed, or
did-not-run outcomes

## Key findings

- `openAgentChat` waits for the full page `load` event after the correct
chat URL is already reached; this causes four direct failures and hides
ten additional serial tests
- `waitForResponseComplete` can spend the full caller timeout in its
stability phase, explaining the PDF failure and HTML flake
- the remaining persistent signals require product/integration
diagnosis: voice transcription, GIF rendering/tool output, auto-title
updates, WebSocket status, concurrent-session isolation, and agent hire
state
- broad serial groups make the headline pass rate incomplete because 26
discovered tests never execute

## Test plan

- [x] parsed the complete Production E2E #29925988390 log and all retry
summaries
- [x] cross-checked failure sites against current E2E helpers and specs
on latest `main`
- [x] reconciled 12 failed + 5 flaky + 4 skipped + 26 did not run + 75
passed = 122 discovered tests
- [x] ran `git diff --check`
- [ ] implementation and production reruns are intentionally deferred to
the follow-up fix PRs described in the plan

Plan: `docs/superpowers/plans/2026-07-23-production-e2e-failure-plan.md`
```

### PR body

## Summary

- documents the 2026-07-22 production E2E baseline: 75 stable passes, 5 flaky, 12 failed, 4 intentional skips, and 26 tests blocked by serial suites
- maps every final failure and every did-not-run scenario to its blocker, with evidence and confidence levels
- proposes five implementation phases in execution order: shared harness fixes, removal of unnecessary serial coupling, file-generation/low-credit and remaining targeted fixes, the four fixture/CSS gaps, then targeted-to-full production validation
- defines completion as two consecutive full production runs with all 122 discovered tests passing and zero skipped, flaky, failed, or did-not-run outcomes

## Key findings

- `openAgentChat` waits for the full page `load` event after the correct chat URL is already reached; this causes four direct failures and hides ten additional serial tests
- `waitForResponseComplete` can spend the full caller timeout in its stability phase, explaining the PDF failure and HTML flake
- the remaining persistent signals require product/integration diagnosis: voice transcription, GIF rendering/tool output, auto-title updates, WebSocket status, concurrent-session isolation, and agent hire state
- broad serial groups make the headline pass rate incomplete because 26 discovered tests never execute

## Test plan

- [x] parsed the complete Production E2E #29925988390 log and all retry summaries
- [x] cross-checked failure sites against current E2E helpers and specs on latest `main`
- [x] reconciled 12 failed + 5 flaky + 4 skipped + 26 did not run + 75 passed = 122 discovered tests
- [x] ran `git diff --check`
- [ ] implementation and production reruns are intentionally deferred to the follow-up fix PRs described in the plan

Plan: `docs/superpowers/plans/2026-07-23-production-e2e-failure-plan.md`


---

## 05a6118206  (PR #3068)

- **SHA**: `05a611820621836e6afea4246819224edf4623bf`
- **作者**: dependabot[bot] (dependabot[bot])
- **日期**: 2026-07-27T07:00:30Z
- **PR**: #3068 — chore(deps-dev): update ruff requirement from >=0.15.21 to >=0.15.22 in /services/claw-interface

### Commit message

```
chore(deps-dev): update ruff requirement from >=0.15.21 to >=0.15.22 in /services/claw-interface (#3068)

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to
permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/releases">ruff's
releases</a>.</em></p>
<blockquote>
<h2>0.15.22</h2>
<h2>Release Notes</h2>
<p>Released on 2026-07-16.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>pycodestyle</code>] Add an autofix for <code>E402</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/22212">#22212</a>)</li>
<li>[<code>refurb</code>] Allow subclassing builtins in stub files
(<code>FURB189</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26812">#26812</a>)</li>
<li>[<code>ruff</code>] Add rule to replace <code>noqa</code> comments
with <code>ruff:ignore</code> (<code>RUF105</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26423">#26423</a>)</li>
<li>[<code>ruff</code>] Add rule to use human-readable names in
<code>ruff:ignore</code> comments (<code>RUF106</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26682">#26682</a>)</li>
<li>[<code>ruff</code>] Add rule to use human-readable names in
configuration selectors (<code>RUF201</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26772">#26772</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>flake8-pyi</code>] Fix false positive in <code>__all__</code>
(<code>PYI053</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26872">#26872</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>pylint</code>] Ignore mutable type updates in
<code>redefined-loop-name</code> (<code>PLW2901</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25733">#25733</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Avoid redundant lexer token bookkeeping (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26765">#26765</a>)</li>
<li>Avoid redundant pending-indentation writes (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26774">#26774</a>)</li>
<li>Avoid unnecessary identifier lookahead (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26525">#26525</a>)</li>
<li>Reuse parser scratch buffers (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26798">#26798</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Document argfile support (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26803">#26803</a>)</li>
<li>[<code>flake8-datetimez</code>] Clarify naming guidance for
<code>datetime.today</code> (<code>DTZ002</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26658">#26658</a>)</li>
<li>[<code>pycodestyle</code>] Document <code>E731</code> fix safety (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26847">#26847</a>)</li>
<li>[<code>ruff</code>] Clarify intentional async contexts for
<code>unused-async</code> (<code>RUF029</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26641">#26641</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/dwego"><code>@​dwego</code></a></li>
<li><a
href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
<li><a href="https://github.com/Joosboy"><code>@​Joosboy</code></a></li>
<li><a
href="https://github.com/KaufmanDmitriy"><code>@​KaufmanDmitriy</code></a></li>
<li><a
href="https://github.com/PeterJCLaw"><code>@​PeterJCLaw</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a
href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
</ul>
<h2>Install ruff 0.15.22</h2>
<h3>Install prebuilt binaries via shell script</h3>
<pre lang="sh"><code>&lt;/tr&gt;&lt;/table&gt; 
</code></pre>
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/blob/0.15.22/CHANGELOG.md">ruff's
changelog</a>.</em></p>
<blockquote>
<h2>0.15.22</h2>
<p>Released on 2026-07-16.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>pycodestyle</code>] Add an autofix for <code>E402</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/22212">#22212</a>)</li>
<li>[<code>refurb</code>] Allow subclassing builtins in stub files
(<code>FURB189</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26812">#26812</a>)</li>
<li>[<code>ruff</code>] Add rule to replace <code>noqa</code> comments
with <code>ruff:ignore</code> (<code>RUF105</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26423">#26423</a>)</li>
<li>[<code>ruff</code>] Add rule to use human-readable names in
<code>ruff:ignore</code> comments (<code>RUF106</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26682">#26682</a>)</li>
<li>[<code>ruff</code>] Add rule to use human-readable names in
configuration selectors (<code>RUF201</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26772">#26772</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>flake8-pyi</code>] Fix false positive in <code>__all__</code>
(<code>PYI053</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26872">#26872</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>pylint</code>] Ignore mutable type updates in
<code>redefined-loop-name</code> (<code>PLW2901</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25733">#25733</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Avoid redundant lexer token bookkeeping (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26765">#26765</a>)</li>
<li>Avoid redundant pending-indentation writes (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26774">#26774</a>)</li>
<li>Avoid unnecessary identifier lookahead (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26525">#26525</a>)</li>
<li>Reuse parser scratch buffers (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26798">#26798</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Document argfile support (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26803">#26803</a>)</li>
<li>[<code>flake8-datetimez</code>] Clarify naming guidance for
<code>datetime.today</code> (<code>DTZ002</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26658">#26658</a>)</li>
<li>[<code>pycodestyle</code>] Document <code>E731</code> fix safety (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26847">#26847</a>)</li>
<li>[<code>ruff</code>] Clarify intentional async contexts for
<code>unused-async</code> (<code>RUF029</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26641">#26641</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/dwego"><code>@​dwego</code></a></li>
<li><a
href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
<li><a href="https://github.com/Joosboy"><code>@​Joosboy</code></a></li>
<li><a
href="https://github.com/KaufmanDmitriy"><code>@​KaufmanDmitriy</code></a></li>
<li><a
href="https://github.com/PeterJCLaw"><code>@​PeterJCLaw</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a
href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
</ul>
<h2>0.15.21</h2>
<p>Released on 2026-07-09.</p>
<h3>Preview features</h3>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/astral-sh/ruff/commit/0177a7e0d2c4a3805afa1960f106d72878766cbc"><code>0177a7e</code></a>
Bump 0.15.22 (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26884">#26884</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/fe8ba85a55b76d838e6058d813b64468b5f81eca"><code>fe8ba85</code></a>
[<code>pycodestyle</code>] Document <code>E731</code> fix safety (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26847">#26847</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/f3cf7c81fa35f8b819a719303bf1789714f1c780"><code>f3cf7c8</code></a>
[<code>ruff</code>] Add <code>rule-codes-in-selectors</code>
(<code>RUF201</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26772">#26772</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/d244fd75e9036e61be4896b823fe760d7aa632a3"><code>d244fd7</code></a>
Document argfile support (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26803">#26803</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/f23975849a0db64a2851029c68fc054799d5e7da"><code>f239758</code></a>
[<code>flake8-pyi</code>] Fix false positive in <code>__all__</code>
(<code>PYI053</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26872">#26872</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/54acbcde56d76bc47b0b3dfe61e57fbaadd2c06b"><code>54acbcd</code></a>
[ty] Support <code>TypeVarTuple</code> and <code>Unpack</code> (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25240">#25240</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/87fc38cacd7e2bd906674c6dc5b8be97aa3a5bc3"><code>87fc38c</code></a>
[ty] Parallelize subtype hierarchy search (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26875">#26875</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/e454f91fa63bd745d874ead751ad15d9f521195a"><code>e454f91</code></a>
[ty] Share interned query keys across Salsa queries (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26794">#26794</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/6f361a74a232ad283cc6e5e5d3a62109802aab65"><code>6f361a7</code></a>
[ty] only collect expected types for files open in the editor (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25546">#25546</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/6d6b2b37686da8b1ee56e54fd99831f1f5fa0381"><code>6d6b2b3</code></a>
[ty] Avoid allocations during Salsa interned lookups (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26877">#26877</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/astral-sh/ruff/compare/0.15.21...0.15.22">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR body

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's releases</a>.</em></p>
<blockquote>
<h2>0.15.22</h2>
<h2>Release Notes</h2>
<p>Released on 2026-07-16.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>pycodestyle</code>] Add an autofix for <code>E402</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/22212">#22212</a>)</li>
<li>[<code>refurb</code>] Allow subclassing builtins in stub files (<code>FURB189</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26812">#26812</a>)</li>
<li>[<code>ruff</code>] Add rule to replace <code>noqa</code> comments with <code>ruff:ignore</code> (<code>RUF105</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26423">#26423</a>)</li>
<li>[<code>ruff</code>] Add rule to use human-readable names in <code>ruff:ignore</code> comments (<code>RUF106</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26682">#26682</a>)</li>
<li>[<code>ruff</code>] Add rule to use human-readable names in configuration selectors (<code>RUF201</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26772">#26772</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>flake8-pyi</code>] Fix false positive in <code>__all__</code> (<code>PYI053</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26872">#26872</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>pylint</code>] Ignore mutable type updates in <code>redefined-loop-name</code> (<code>PLW2901</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25733">#25733</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Avoid redundant lexer token bookkeeping (<a href="https://redirect.github.com/astral-sh/ruff/pull/26765">#26765</a>)</li>
<li>Avoid redundant pending-indentation writes (<a href="https://redirect.github.com/astral-sh/ruff/pull/26774">#26774</a>)</li>
<li>Avoid unnecessary identifier lookahead (<a href="https://redirect.github.com/astral-sh/ruff/pull/26525">#26525</a>)</li>
<li>Reuse parser scratch buffers (<a href="https://redirect.github.com/astral-sh/ruff/pull/26798">#26798</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Document argfile support (<a href="https://redirect.github.com/astral-sh/ruff/pull/26803">#26803</a>)</li>
<li>[<code>flake8-datetimez</code>] Clarify naming guidance for <code>datetime.today</code> (<code>DTZ002</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26658">#26658</a>)</li>
<li>[<code>pycodestyle</code>] Document <code>E731</code> fix safety (<a href="https://redirect.github.com/astral-sh/ruff/pull/26847">#26847</a>)</li>
<li>[<code>ruff</code>] Clarify intentional async contexts for <code>unused-async</code> (<code>RUF029</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26641">#26641</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/dwego"><code>@​dwego</code></a></li>
<li><a href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
<li><a href="https://github.com/Joosboy"><code>@​Joosboy</code></a></li>
<li><a href="https://github.com/KaufmanDmitriy"><code>@​KaufmanDmitriy</code></a></li>
<li><a href="https://github.com/PeterJCLaw"><code>@​PeterJCLaw</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
</ul>
<h2>Install ruff 0.15.22</h2>
<h3>Install prebuilt binaries via shell script</h3>
<pre lang="sh"><code>&lt;/tr&gt;&lt;/table&gt; 
</code></pre>
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/blob/0.15.22/CHANGELOG.md">ruff's changelog</a>.</em></p>
<blockquote>
<h2>0.15.22</h2>
<p>Released on 2026-07-16.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>pycodestyle</code>] Add an autofix for <code>E402</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/22212">#22212</a>)</li>
<li>[<code>refurb</code>] Allow subclassing builtins in stub files (<code>FURB189</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26812">#26812</a>)</li>
<li>[<code>ruff</code>] Add rule to replace <code>noqa</code> comments with <code>ruff:ignore</code> (<code>RUF105</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26423">#26423</a>)</li>
<li>[<code>ruff</code>] Add rule to use human-readable names in <code>ruff:ignore</code> comments (<code>RUF106</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26682">#26682</a>)</li>
<li>[<code>ruff</code>] Add rule to use human-readable names in configuration selectors (<code>RUF201</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26772">#26772</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>flake8-pyi</code>] Fix false positive in <code>__all__</code> (<code>PYI053</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26872">#26872</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>pylint</code>] Ignore mutable type updates in <code>redefined-loop-name</code> (<code>PLW2901</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25733">#25733</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Avoid redundant lexer token bookkeeping (<a href="https://redirect.github.com/astral-sh/ruff/pull/26765">#26765</a>)</li>
<li>Avoid redundant pending-indentation writes (<a href="https://redirect.github.com/astral-sh/ruff/pull/26774">#26774</a>)</li>
<li>Avoid unnecessary identifier lookahead (<a href="https://redirect.github.com/astral-sh/ruff/pull/26525">#26525</a>)</li>
<li>Reuse parser scratch buffers (<a href="https://redirect.github.com/astral-sh/ruff/pull/26798">#26798</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Document argfile support (<a href="https://redirect.github.com/astral-sh/ruff/pull/26803">#26803</a>)</li>
<li>[<code>flake8-datetimez</code>] Clarify naming guidance for <code>datetime.today</code> (<code>DTZ002</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26658">#26658</a>)</li>
<li>[<code>pycodestyle</code>] Document <code>E731</code> fix safety (<a href="https://redirect.github.com/astral-sh/ruff/pull/26847">#26847</a>)</li>
<li>[<code>ruff</code>] Clarify intentional async contexts for <code>unused-async</code> (<code>RUF029</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26641">#26641</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/dwego"><code>@​dwego</code></a></li>
<li><a href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
<li><a href="https://github.com/Joosboy"><code>@​Joosboy</code></a></li>
<li><a href="https://github.com/KaufmanDmitriy"><code>@​KaufmanDmitriy</code></a></li>
<li><a href="https://github.com/PeterJCLaw"><code>@​PeterJCLaw</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
</ul>
<h2>0.15.21</h2>
<p>Released on 2026-07-09.</p>
<h3>Preview features</h3>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/astral-sh/ruff/commit/0177a7e0d2c4a3805afa1960f106d72878766cbc"><code>0177a7e</code></a> Bump 0.15.22 (<a href="https://redirect.github.com/astral-sh/ruff/issues/26884">#26884</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/fe8ba85a55b76d838e6058d813b64468b5f81eca"><code>fe8ba85</code></a> [<code>pycodestyle</code>] Document <code>E731</code> fix safety (<a href="https://redirect.github.com/astral-sh/ruff/issues/26847">#26847</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/f3cf7c81fa35f8b819a719303bf1789714f1c780"><code>f3cf7c8</code></a> [<code>ruff</code>] Add <code>rule-codes-in-selectors</code> (<code>RUF201</code>) (<a href="https://redirect.github.com/astral-sh/ruff/issues/26772">#26772</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/d244fd75e9036e61be4896b823fe760d7aa632a3"><code>d244fd7</code></a> Document argfile support (<a href="https://redirect.github.com/astral-sh/ruff/issues/26803">#26803</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/f23975849a0db64a2851029c68fc054799d5e7da"><code>f239758</code></a> [<code>flake8-pyi</code>] Fix false positive in <code>__all__</code> (<code>PYI053</code>) (<a href="https://redirect.github.com/astral-sh/ruff/issues/26872">#26872</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/54acbcde56d76bc47b0b3dfe61e57fbaadd2c06b"><code>54acbcd</code></a> [ty] Support <code>TypeVarTuple</code> and <code>Unpack</code> (<a href="https://redirect.github.com/astral-sh/ruff/issues/25240">#25240</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/87fc38cacd7e2bd906674c6dc5b8be97aa3a5bc3"><code>87fc38c</code></a> [ty] Parallelize subtype hierarchy search (<a href="https://redirect.github.com/astral-sh/ruff/issues/26875">#26875</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/e454f91fa63bd745d874ead751ad15d9f521195a"><code>e454f91</code></a> [ty] Share interned query keys across Salsa queries (<a href="https://redirect.github.com/astral-sh/ruff/issues/26794">#26794</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/6f361a74a232ad283cc6e5e5d3a62109802aab65"><code>6f361a7</code></a> [ty] only collect expected types for files open in the editor (<a href="https://redirect.github.com/astral-sh/ruff/issues/25546">#25546</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/6d6b2b37686da8b1ee56e54fd99831f1f5fa0381"><code>6d6b2b3</code></a> [ty] Avoid allocations during Salsa interned lookups (<a href="https://redirect.github.com/astral-sh/ruff/issues/26877">#26877</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.15.21...0.15.22">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---

## 84363002a3  (PR #3069)

- **SHA**: `84363002a3d595d717a50d6b88c861fd4993a334`
- **作者**: dependabot[bot] (dependabot[bot])
- **日期**: 2026-07-27T07:00:18Z
- **PR**: #3069 — chore(deps): update openai requirement from <2.46.0,>=2.45.0 to >=2.46.0,<2.47.0 in /services/claw-interface

### Commit message

```
chore(deps): update openai requirement from <2.46.0,>=2.45.0 to >=2.46.0,<2.47.0 in /services/claw-interface (#3069)

Updates the requirements on
[openai](https://github.com/openai/openai-python) to permit the latest
version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/openai/openai-python/releases">openai's
releases</a>.</em></p>
<blockquote>
<h2>v2.46.0</h2>
<h2>2.46.0 (2026-07-17)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.45.0...v2.46.0">v2.45.0...v2.46.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong>
/organization/projects/{project_id}/service_accounts/{service_account_id}/api_keys&quot;
endpoint (<a
href="https://github.com/openai/openai-python/commit/5a0094194eac9c605c8ca84d47d1c5518f8e2131">5a00941</a>)</li>
<li><strong>api:</strong> add owner_project_access to APIKeyListParams
(<a
href="https://github.com/openai/openai-python/commit/f589d04bf9f377ecb1f54335ab3ab9d825b5dfee">f589d04</a>)</li>
<li><strong>api:</strong> manual updates (<a
href="https://github.com/openai/openai-python/commit/980f176e83ee5d991bf9e8e4def80d9905ade5ec">980f176</a>)</li>
<li><strong>api:</strong> manual updates (<a
href="https://github.com/openai/openai-python/commit/2eae984315580cdbf9ceb14d6cb568c581baa768">2eae984</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> preserve generated type compatibility (<a
href="https://github.com/openai/openai-python/commit/00bd72adbe03f4b5c4b89d91b8d317f11b58bbdf">00bd72a</a>)</li>
<li><strong>api:</strong> remove beta annotation compatibility aliases
(<a
href="https://github.com/openai/openai-python/commit/99dbd15ff3ad1628b94a729a6b688212d4655908">99dbd15</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/openai/openai-python/blob/main/CHANGELOG.md">openai's
changelog</a>.</em></p>
<blockquote>
<h2>2.46.0 (2026-07-17)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.45.0...v2.46.0">v2.45.0...v2.46.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong>
/organization/projects/{project_id}/service_accounts/{service_account_id}/api_keys&quot;
endpoint (<a
href="https://github.com/openai/openai-python/commit/5a0094194eac9c605c8ca84d47d1c5518f8e2131">5a00941</a>)</li>
<li><strong>api:</strong> add owner_project_access to APIKeyListParams
(<a
href="https://github.com/openai/openai-python/commit/f589d04bf9f377ecb1f54335ab3ab9d825b5dfee">f589d04</a>)</li>
<li><strong>api:</strong> manual updates (<a
href="https://github.com/openai/openai-python/commit/980f176e83ee5d991bf9e8e4def80d9905ade5ec">980f176</a>)</li>
<li><strong>api:</strong> manual updates (<a
href="https://github.com/openai/openai-python/commit/2eae984315580cdbf9ceb14d6cb568c581baa768">2eae984</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> preserve generated type compatibility (<a
href="https://github.com/openai/openai-python/commit/00bd72adbe03f4b5c4b89d91b8d317f11b58bbdf">00bd72a</a>)</li>
<li><strong>api:</strong> remove beta annotation compatibility aliases
(<a
href="https://github.com/openai/openai-python/commit/99dbd15ff3ad1628b94a729a6b688212d4655908">99dbd15</a>)</li>
</ul>
<h2>2.45.0 (2026-07-09)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.44.0...v2.45.0">v2.44.0...v2.45.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> gpt-5.6-sol updates (<a
href="https://github.com/openai/openai-python/commit/039d1feb264a2dca7195ba5028e9fb47a5e04987">039d1fe</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> restore beta resource accessors (<a
href="https://github.com/openai/openai-python/commit/2dfc130b8f0fdb0049e075aac21aaef29482b4e3">2dfc130</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li>retrigger release automation (<a
href="https://github.com/openai/openai-python/commit/7b61351b014bb6ca4623ff6cce7f32f45038a92e">7b61351</a>)</li>
</ul>
<h2>2.44.0 (2026-06-24)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.43.0...v2.44.0">v2.43.0...v2.44.0</a></p>
<h3>Bug Fixes</h3>
<ul>
<li><strong>auth:</strong> prioritize first auth header (<a
href="https://github.com/openai/openai-python/commit/797e3362e222ae14e587a4543b76a54d8992d66c">797e336</a>)</li>
</ul>
<h2>2.43.0 (2026-06-17)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.42.0...v2.43.0">v2.42.0...v2.43.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> update OpenAPI spec or Stainless config (<a
href="https://github.com/openai/openai-python/commit/22542358490ef8f31f0d373e17f7b791b3d983ca">2254235</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/openai/openai-python/commit/0e6adb15adc1e74087bcb402de7a75e4fbc0aecb"><code>0e6adb1</code></a>
release: 2.46.0 (<a
href="https://redirect.github.com/openai/openai-python/issues/3501">#3501</a>)</li>
<li>See full diff in <a
href="https://github.com/openai/openai-python/compare/v2.45.0...v2.46.0">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR body

Updates the requirements on [openai](https://github.com/openai/openai-python) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/openai/openai-python/releases">openai's releases</a>.</em></p>
<blockquote>
<h2>v2.46.0</h2>
<h2>2.46.0 (2026-07-17)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.45.0...v2.46.0">v2.45.0...v2.46.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> /organization/projects/{project_id}/service_accounts/{service_account_id}/api_keys&quot; endpoint (<a href="https://github.com/openai/openai-python/commit/5a0094194eac9c605c8ca84d47d1c5518f8e2131">5a00941</a>)</li>
<li><strong>api:</strong> add owner_project_access to APIKeyListParams (<a href="https://github.com/openai/openai-python/commit/f589d04bf9f377ecb1f54335ab3ab9d825b5dfee">f589d04</a>)</li>
<li><strong>api:</strong> manual updates (<a href="https://github.com/openai/openai-python/commit/980f176e83ee5d991bf9e8e4def80d9905ade5ec">980f176</a>)</li>
<li><strong>api:</strong> manual updates (<a href="https://github.com/openai/openai-python/commit/2eae984315580cdbf9ceb14d6cb568c581baa768">2eae984</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> preserve generated type compatibility (<a href="https://github.com/openai/openai-python/commit/00bd72adbe03f4b5c4b89d91b8d317f11b58bbdf">00bd72a</a>)</li>
<li><strong>api:</strong> remove beta annotation compatibility aliases (<a href="https://github.com/openai/openai-python/commit/99dbd15ff3ad1628b94a729a6b688212d4655908">99dbd15</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/openai/openai-python/blob/main/CHANGELOG.md">openai's changelog</a>.</em></p>
<blockquote>
<h2>2.46.0 (2026-07-17)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.45.0...v2.46.0">v2.45.0...v2.46.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> /organization/projects/{project_id}/service_accounts/{service_account_id}/api_keys&quot; endpoint (<a href="https://github.com/openai/openai-python/commit/5a0094194eac9c605c8ca84d47d1c5518f8e2131">5a00941</a>)</li>
<li><strong>api:</strong> add owner_project_access to APIKeyListParams (<a href="https://github.com/openai/openai-python/commit/f589d04bf9f377ecb1f54335ab3ab9d825b5dfee">f589d04</a>)</li>
<li><strong>api:</strong> manual updates (<a href="https://github.com/openai/openai-python/commit/980f176e83ee5d991bf9e8e4def80d9905ade5ec">980f176</a>)</li>
<li><strong>api:</strong> manual updates (<a href="https://github.com/openai/openai-python/commit/2eae984315580cdbf9ceb14d6cb568c581baa768">2eae984</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> preserve generated type compatibility (<a href="https://github.com/openai/openai-python/commit/00bd72adbe03f4b5c4b89d91b8d317f11b58bbdf">00bd72a</a>)</li>
<li><strong>api:</strong> remove beta annotation compatibility aliases (<a href="https://github.com/openai/openai-python/commit/99dbd15ff3ad1628b94a729a6b688212d4655908">99dbd15</a>)</li>
</ul>
<h2>2.45.0 (2026-07-09)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.44.0...v2.45.0">v2.44.0...v2.45.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> gpt-5.6-sol updates (<a href="https://github.com/openai/openai-python/commit/039d1feb264a2dca7195ba5028e9fb47a5e04987">039d1fe</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> restore beta resource accessors (<a href="https://github.com/openai/openai-python/commit/2dfc130b8f0fdb0049e075aac21aaef29482b4e3">2dfc130</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li>retrigger release automation (<a href="https://github.com/openai/openai-python/commit/7b61351b014bb6ca4623ff6cce7f32f45038a92e">7b61351</a>)</li>
</ul>
<h2>2.44.0 (2026-06-24)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.43.0...v2.44.0">v2.43.0...v2.44.0</a></p>
<h3>Bug Fixes</h3>
<ul>
<li><strong>auth:</strong> prioritize first auth header (<a href="https://github.com/openai/openai-python/commit/797e3362e222ae14e587a4543b76a54d8992d66c">797e336</a>)</li>
</ul>
<h2>2.43.0 (2026-06-17)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.42.0...v2.43.0">v2.42.0...v2.43.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> update OpenAPI spec or Stainless config (<a href="https://github.com/openai/openai-python/commit/22542358490ef8f31f0d373e17f7b791b3d983ca">2254235</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/openai/openai-python/commit/0e6adb15adc1e74087bcb402de7a75e4fbc0aecb"><code>0e6adb1</code></a> release: 2.46.0 (<a href="https://redirect.github.com/openai/openai-python/issues/3501">#3501</a>)</li>
<li>See full diff in <a href="https://github.com/openai/openai-python/compare/v2.45.0...v2.46.0">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---

## 55b7fdf055  (PR #3073)

- **SHA**: `55b7fdf05596aadc0765c42984c8e867d55c508d`
- **作者**: kaka-srp (kaka-srp)
- **日期**: 2026-07-27T06:49:24Z
- **PR**: #3073 — fix(billing): make checkout lease CSFLE-safe

### Commit message

```
fix(billing): make checkout lease CSFLE-safe (#3073)

## Summary

- replace the CSFLE-incompatible checkout lease aggregation pipeline
with classic atomic compare-and-set updates
- preserve stable lease timestamps for same-order retries and exclusion
for competing orders
- add focused regression coverage for fresh claims, idempotent retries,
release races, and active-owner conflicts

## Root cause

The subscription checkout lease used an aggregation-pipeline
`find_one_and_update`. Production `crypt_shared 8.2.1` rejects that
update shape with MongoDB error `31146` before the Antom provider call,
causing `/antom/create-payment` to return HTTP 500.

## Validation

- `pytest -q tests/unit/test_user_repo.py
tests/unit/test_billing_v2_order_requests.py
tests/unit/test_antom_billing_v2_checkout.py` — 80 passed
- `bash scripts/verify-local.sh --py-static` — Ruff, format, Pyright,
and import-linter passed
- pre-commit and pre-push repository gates passed
- staging Mongo/CSFLE probe reproduced `31146` with the old pipeline and
confirmed the classic update succeeds
- staging race probe confirmed two concurrent owners produce exactly one
winner
- all temporary staging test accounts were removed

## Scope

Only the checkout lease repository implementation and its unit tests are
changed. No payment-provider calls, plan rules, frontend behavior,
indexes, or other collections are modified.
```

### PR body

## Summary

- replace the CSFLE-incompatible checkout lease aggregation pipeline with classic atomic compare-and-set updates
- preserve stable lease timestamps for same-order retries and exclusion for competing orders
- add focused regression coverage for fresh claims, idempotent retries, release races, and active-owner conflicts

## Root cause

The subscription checkout lease used an aggregation-pipeline `find_one_and_update`. Production `crypt_shared 8.2.1` rejects that update shape with MongoDB error `31146` before the Antom provider call, causing `/antom/create-payment` to return HTTP 500.

## Validation

- `pytest -q tests/unit/test_user_repo.py tests/unit/test_billing_v2_order_requests.py tests/unit/test_antom_billing_v2_checkout.py` — 80 passed
- `bash scripts/verify-local.sh --py-static` — Ruff, format, Pyright, and import-linter passed
- pre-commit and pre-push repository gates passed
- staging Mongo/CSFLE probe reproduced `31146` with the old pipeline and confirmed the classic update succeeds
- staging race probe confirmed two concurrent owners produce exactly one winner
- all temporary staging test accounts were removed

## Scope

Only the checkout lease repository implementation and its unit tests are changed. No payment-provider calls, plan rules, frontend behavior, indexes, or other collections are modified.


---

## 87b8fc9b1f  (PR #3063)

- **SHA**: `87b8fc9b1f2b1ca79ec58f0a217207b94e9cc0fb`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-07-27T04:20:46Z
- **PR**: #3063 — feat(claw-interface): pin per-submission environment version on engine install

### Commit message

```
feat(claw-interface): pin per-submission environment version on engine install (#3063)

## Summary

Implements per-submission environment version pinning for engine-agent
installs. Each approved pack submission records the exact zooclaw-engine
environment version created for it; installs pin that version once
recorded instead of always resolving latest-ready.

Backend-only (`claw-interface`). Dark until agents-v2 and the engine
Environments API are live; no web release.

### What changed

- **Engine version parsing.** `EngineEnvironmentCreated` normalizes both
engine response shapes: create-environment returns a nested version
record, while create-version returns a top-level integer.
- **Submission schema/repository.** `PackSubmission` gains
`environment_version`; `pack_submission_repo.record_environment`
persists the per-submission version. The environment id remains the
per-pack `Pack.environment_id`.
- **Pipeline write-back.** The post-approval environment pipeline
records the returned version on the create, create-version, and CAS-loss
reconcile paths.
- **Engine client.** `create_agent` sends `environment_version` only
when `environment_id` is also present.
- **Install resolution.** A recorded version pins `(Pack.environment_id,
submission.environment_version)`. A missing version—pipeline record
window, skipped oversized archive, failed pipeline, or legacy row—uses
an unpinned pack binding and lets the engine resolve latest-ready.
Foreign flag-shared packs continue to use the engine default.
- **No manual rebuild route.** The proposed `POST
/orgs/{org_id}/packs/{pack_id}/environment/rebuild` action and its
supporting service/model were removed; automated recovery remains a
reconcile/poller follow-up.

### Engine contract

Verified against `zooclaw-engine@main`: `create_agent` accepts
`resource.environment_id` plus a positive integer
`resource.environment_version`; version requires id, and pinned versions
that are not ready return `409 environment_not_ready`.

## Test plan

- [x] Focused unit tests for version parsing, repository write-back,
pipeline paths, engine-client payloads, install resolution, and route
wiring
- [x] Local Python static gate: ruff, ruff-format, pyright, and
import-linter
- [x] Prior full local gate on this branch: 6861 tests passed; whole-app
coverage 90.03%
- [ ] Staging smoke after agents-v2 and the engine Environments API are
available: approve → build ready → pinned install
- [ ] Link the correct Linear issue if one exists

## Rollout / follow-ups

- Keep dark until agents-v2 and the engine Environments API are
available.
- Backfill pre-amendment submissions so their exact environment versions
can be pinned.
- Add a reconcile/poller for interrupted pipelines and engine-side
failed builds.
- Add engine-side environment re-pin/migration support for
already-created agents.
```

### PR body

## Summary

Implements per-submission environment version pinning for engine-agent installs. Each approved pack submission records the exact zooclaw-engine environment version created for it; installs pin that version once recorded instead of always resolving latest-ready.

Backend-only (`claw-interface`). Dark until agents-v2 and the engine Environments API are live; no web release.

### What changed

- **Engine version parsing.** `EngineEnvironmentCreated` normalizes both engine response shapes: create-environment returns a nested version record, while create-version returns a top-level integer.
- **Submission schema/repository.** `PackSubmission` gains `environment_version`; `pack_submission_repo.record_environment` persists the per-submission version. The environment id remains the per-pack `Pack.environment_id`.
- **Pipeline write-back.** The post-approval environment pipeline records the returned version on the create, create-version, and CAS-loss reconcile paths.
- **Engine client.** `create_agent` sends `environment_version` only when `environment_id` is also present.
- **Install resolution.** A recorded version pins `(Pack.environment_id, submission.environment_version)`. A missing version—pipeline record window, skipped oversized archive, failed pipeline, or legacy row—uses an unpinned pack binding and lets the engine resolve latest-ready. Foreign flag-shared packs continue to use the engine default.
- **No manual rebuild route.** The proposed `POST /orgs/{org_id}/packs/{pack_id}/environment/rebuild` action and its supporting service/model were removed; automated recovery remains a reconcile/poller follow-up.

### Engine contract

Verified against `zooclaw-engine@main`: `create_agent` accepts `resource.environment_id` plus a positive integer `resource.environment_version`; version requires id, and pinned versions that are not ready return `409 environment_not_ready`.

## Test plan

- [x] Focused unit tests for version parsing, repository write-back, pipeline paths, engine-client payloads, install resolution, and route wiring
- [x] Local Python static gate: ruff, ruff-format, pyright, and import-linter
- [x] Prior full local gate on this branch: 6861 tests passed; whole-app coverage 90.03%
- [ ] Staging smoke after agents-v2 and the engine Environments API are available: approve → build ready → pinned install
- [ ] Link the correct Linear issue if one exists

## Rollout / follow-ups

- Keep dark until agents-v2 and the engine Environments API are available.
- Backfill pre-amendment submissions so their exact environment versions can be pinned.
- Add a reconcile/poller for interrupted pipelines and engine-side failed builds.
- Add engine-side environment re-pin/migration support for already-created agents.


---

## 4caa4572d7  (PR #3066)

- **SHA**: `4caa4572d7d316b238865edd305775ecbb15fad0`
- **作者**: kaka-srp (kaka-srp)
- **日期**: 2026-07-27T02:47:13Z
- **PR**: #3066 — fix(agent-builder): isolate project workspace activation

### Commit message

```
fix(agent-builder): isolate project workspace activation (#3066)

## Summary
- Split Agent Builder state polling from explicit workspace activation
so ready projects are not repeatedly materialized.
- Hold browser workspace ownership through the complete Agent turn,
including ambiguous Mattermost POST outcomes reconciled by
`pending_post_id`.
- Preserve persisted create/fork project IDs and fork target
reservations when workspace setup fails transiently.
- Fall back to the legacy project GET route when `/state` or `/activate`
is absent during a staggered web/backend rollout.

## Root cause
The project read endpoint also materialized the shared Agent Studio
root, so polling and navigation could switch workspaces behind an
in-flight conversation. A successful Mattermost POST only confirmed
message creation, not completion of the Agent turn. Separately,
create/fork persisted the project before workspace setup but propagated
transient setup errors, causing the client to lose the already-reserved
project identity.

## Test plan
- [x] `pytest -q tests/unit/test_agent_builder_service.py
tests/unit/test_agent_builder_routes.py
tests/unit/test_openclaw_client.py` — 341 passed
- [x] Focused frontend Vitest suites for Agent Builder activation,
sending, conversation threads, API behavior, and Mattermost errors — 81
passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh --no-test`
- [x] TypeScript, ESLint, Ruff, Pyright, import contracts, and diff
whitespace checks

## Notes
The complete frontend unit suite was attempted locally but was not used
as the gate because unrelated existing tests hit parallel timeouts and a
shared dependency-resolution failure. Focused affected-surface tests and
frontend static checks passed; CI remains authoritative for the full
suite.
```

### PR body

## Summary
- Split Agent Builder state polling from explicit workspace activation so ready projects are not repeatedly materialized.
- Hold browser workspace ownership through the complete Agent turn, including ambiguous Mattermost POST outcomes reconciled by `pending_post_id`.
- Preserve persisted create/fork project IDs and fork target reservations when workspace setup fails transiently.
- Fall back to the legacy project GET route when `/state` or `/activate` is absent during a staggered web/backend rollout.

## Root cause
The project read endpoint also materialized the shared Agent Studio root, so polling and navigation could switch workspaces behind an in-flight conversation. A successful Mattermost POST only confirmed message creation, not completion of the Agent turn. Separately, create/fork persisted the project before workspace setup but propagated transient setup errors, causing the client to lose the already-reserved project identity.

## Test plan
- [x] `pytest -q tests/unit/test_agent_builder_service.py tests/unit/test_agent_builder_routes.py tests/unit/test_openclaw_client.py` — 341 passed
- [x] Focused frontend Vitest suites for Agent Builder activation, sending, conversation threads, API behavior, and Mattermost errors — 81 passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh --no-test`
- [x] TypeScript, ESLint, Ruff, Pyright, import contracts, and diff whitespace checks

## Notes
The complete frontend unit suite was attempted locally but was not used as the gate because unrelated existing tests hit parallel timeouts and a shared dependency-resolution failure. Focused affected-surface tests and frontend static checks passed; CI remains authoritative for the full suite.


---
