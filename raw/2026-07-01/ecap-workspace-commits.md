# ecap-workspace — commits 2026-07-01

共 8 个 commit


## fix(agent-diagnostics): resolve agent builder by bot id (#2692)

- **SHA**: `053b6dc4134e0876ff0c4f47781785e4d71ed5bc`
- **作者**: Chris@ZooClaw <chris@srp.one>
- **日期**: 2026-07-01T16:36:59Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/053b6dc4134e0876ff0c4f47781785e4d71ed5bc
- **PR**: #2692

### 完整 Commit Message

```
fix(agent-diagnostics): resolve agent builder by bot id (#2692)

## Summary
- Add bot_id and builder_computer_id lookups to the Agent Builder
diagnostics endpoint.
- Return builder workspace metadata so diagnose can pull builder
workspace logs and sessions, not only Pack Test test bot data.
- Add an index for active project lookup by builder computer id.

## Root cause
Agent Builder diagnostics only accepted project, test run, or Pack Test
temporary computer identifiers. A normal bot id from diagnose could not
locate the Builder workspace project, so Preparing Agent Builder cases
were skipped or required manual project ids.

## Test plan
- [x] pytest -q
services/claw-interface/tests/unit/test_agent_builder_diagnostics.py
- [x] ruff check targeted changed files
- [x] ruff format --check targeted changed files
- [x] bash scripts/verify-py.sh partial: ruff, format, and import-linter
passed; pyright failed because this local worktree environment is
missing common dependencies such as fastapi, pytest, and favie_common
across the repo
```

### PR Body

## Summary
- Add bot_id and builder_computer_id lookups to the Agent Builder diagnostics endpoint.
- Return builder workspace metadata so diagnose can pull builder workspace logs and sessions, not only Pack Test test bot data.
- Add an index for active project lookup by builder computer id.

## Root cause
Agent Builder diagnostics only accepted project, test run, or Pack Test temporary computer identifiers. A normal bot id from diagnose could not locate the Builder workspace project, so Preparing Agent Builder cases were skipped or required manual project ids.

## Test plan
- [x] pytest -q services/claw-interface/tests/unit/test_agent_builder_diagnostics.py
- [x] ruff check targeted changed files
- [x] ruff format --check targeted changed files
- [x] bash scripts/verify-py.sh partial: ruff, format, and import-linter passed; pyright failed because this local worktree environment is missing common dependencies such as fastapi, pytest, and favie_common across the repo


## feat(bossclaw): align onboarding UI & motion to zooclaw-boss reference (#2691)

- **SHA**: `0f4b1a24a95ac520eef53ca3c06d002c5ce9716b`
- **作者**: david-srp <david@srp.one>
- **日期**: 2026-07-01T14:03:44Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/0f4b1a24a95ac520eef53ca3c06d002c5ce9716b
- **PR**: #2691

### 完整 Commit Message

```
feat(bossclaw): align onboarding UI & motion to zooclaw-boss reference (#2691)

## What

Pixel-level **visual + motion** alignment of the BossClaw onboarding
wizard (`web/app/src/app/[locale]/bossclaw`) to the `zooclaw-boss`
reference. **UX flow, step structure, and all backend/functional
behavior are frozen** — this is a re-skin + motion port, not a flow
change.

Spec: `docs/superpowers/specs/2026-07-01-bossclaw-ui-align.md`.

## Highlights

**Design system**
- `--boss-*` scoped token layer on `.bossclawRoot` (was fully hardcoded
hex); satisfies the no-hardcoded-color lint.
- Self-hosted **subset** Noto Serif SC / Noto Sans SC (variable wght,
~120–150KB each) + regen script `bossclaw-subset-fonts.sh` (rerun on
copy changes).
- Type scale corrected to the reference (weights/sizes were
systematically heavier/larger).

**New signature elements**
- First-load **Preloader** (gold mark pulse + progress bar + reveal,
gated on font/asset ready).
- Unified single animated **gold-dot progress** across all 6 steps
(replaced the dual brand-header + segmented-bar system).
- Screen-enter transitions, hero glow/sheen/CTA breathing + shine,
done-page draw-check + halo + live dot.
- Official **SVG wordmark** + gold app-icon claw marks (preloader / done
/ QR) + campaign **favicon** scoped to the route.

**Per-screen**
- Hero, Capabilities (reworked to the 6 canonical capabilities, grouped,
with a pinned + glowing CTA), Login/Redeem (reference single-form +
fields), WeChat bind (pod-steps checklist + QR frame + guide), Done.
- Layout fixes: hero fill-height, headline→form spacing, 28px gutter,
back-button centering, done title/subtitle.

**Preserved (frozen)**
- Real OTP login / `boss-info/bind` / `subscription-code/redeem` / agent
install / multi-channel switcher.
- `#2663` mobile scroll, `#2665` weixin-only bind guide,
`?fresh=1`/`subscription_code` URL prefill.

## Testing
- `bash scripts/verify-web.sh <bossclaw>` — **guards + tsc + 60 unit
tests + eslint all green**.
- Rendered every step at 390px and diffed against the reference
(typography, layout, motion).
- WeChat bind (pod-loader + QR) validated against **staging** backend
(mock can't drive the real install).

## Notes
- Mobile-first; the pinned bottom CTA uses `position: fixed` on mobile
(phone container body-scrolls) and an in-flow footer on desktop
(fixed-height card).
- No Linear issue (frontend re-skin of an existing campaign page).

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
```

### PR Body

## What

Pixel-level **visual + motion** alignment of the BossClaw onboarding wizard (`web/app/src/app/[locale]/bossclaw`) to the `zooclaw-boss` reference. **UX flow, step structure, and all backend/functional behavior are frozen** — this is a re-skin + motion port, not a flow change.

Spec: `docs/superpowers/specs/2026-07-01-bossclaw-ui-align.md`.

## Highlights

**Design system**
- `--boss-*` scoped token layer on `.bossclawRoot` (was fully hardcoded hex); satisfies the no-hardcoded-color lint.
- Self-hosted **subset** Noto Serif SC / Noto Sans SC (variable wght, ~120–150KB each) + regen script `bossclaw-subset-fonts.sh` (rerun on copy changes).
- Type scale corrected to the reference (weights/sizes were systematically heavier/larger).

**New signature elements**
- First-load **Preloader** (gold mark pulse + progress bar + reveal, gated on font/asset ready).
- Unified single animated **gold-dot progress** across all 6 steps (replaced the dual brand-header + segmented-bar system).
- Screen-enter transitions, hero glow/sheen/CTA breathing + shine, done-page draw-check + halo + live dot.
- Official **SVG wordmark** + gold app-icon claw marks (preloader / done / QR) + campaign **favicon** scoped to the route.

**Per-screen**
- Hero, Capabilities (reworked to the 6 canonical capabilities, grouped, with a pinned + glowing CTA), Login/Redeem (reference single-form + fields), WeChat bind (pod-steps checklist + QR frame + guide), Done.
- Layout fixes: hero fill-height, headline→form spacing, 28px gutter, back-button centering, done title/subtitle.

**Preserved (frozen)**
- Real OTP login / `boss-info/bind` / `subscription-code/redeem` / agent install / multi-channel switcher.
- `#2663` mobile scroll, `#2665` weixin-only bind guide, `?fresh=1`/`subscription_code` URL prefill.

## Testing
- `bash scripts/verify-web.sh <bossclaw>` — **guards + tsc + 60 unit tests + eslint all green**.
- Rendered every step at 390px and diffed against the reference (typography, layout, motion).
- WeChat bind (pod-loader + QR) validated against **staging** backend (mock can't drive the real install).

## Notes
- Mobile-first; the pinned bottom CTA uses `position: fixed` on mobile (phone container body-scrolls) and an in-flow footer on desktop (fixed-height card).
- No Linear issue (frontend re-skin of an existing campaign page).



## style(agent-builder): 调整Agent  Builder 操作区布局 (#2682)

- **SHA**: `bcdcd22969d05b326eb335e6cec68531a82ad3d5`
- **作者**: lynn Zhuang <lynn@srp.one>
- **日期**: 2026-07-01T10:47:00Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/bcdcd22969d05b326eb335e6cec68531a82ad3d5
- **PR**: #2682

### 完整 Commit Message

```
style(agent-builder): 调整Agent  Builder 操作区布局 (#2682)

## 变更摘要
- 将 Agent Builder 右上角的次级操作收进 More 菜单，并统一为 icon + 文案的菜单项。
- 将项目状态标签放到顶部标题栏，保留 New project 在 More 菜单左侧。
- 将 Package/Test 操作放到输入框上方；drafting 状态下隐藏右侧测试区域，并禁用顶部测试模式按钮。
- 增加 composer prefix 的复用路径，让 Agent Builder 可以替换默认输入框快捷操作，同时不影响其他聊天页面行为。

## 验证
- `bash scripts/verify-web.sh web/app/src/components/ClawPageHeader.tsx
web/app/src/app/'[locale]'/'(app)'/'(chat)'/chat/components/GenClawInput.tsx
web/app/src/app/'[locale]'/'(app)'/'(chat)'/chat/components/OpenClawChatSurface.tsx
web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderClient.tsx
web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderProjectActionControls.tsx
web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderProjectActions.tsx
web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderStatusPane.tsx
web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderTestPane.tsx
web/app/tests/unit/app/agent-builder-client.unit.spec.tsx`
- `pnpm --dir web/app lint:ci`
- GitHub PR checks：`43/43 passed`

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: kaka-srp <kaka@srp.one>
```

### PR Body

## 变更摘要
- 将 Agent Builder 右上角的次级操作收进 More 菜单，并统一为 icon + 文案的菜单项。
- 将项目状态标签放到顶部标题栏，保留 New project 在 More 菜单左侧。
- 将 Package/Test 操作放到输入框上方；drafting 状态下隐藏右侧测试区域，并禁用顶部测试模式按钮。
- 增加 composer prefix 的复用路径，让 Agent Builder 可以替换默认输入框快捷操作，同时不影响其他聊天页面行为。

## 验证
- `bash scripts/verify-web.sh web/app/src/components/ClawPageHeader.tsx web/app/src/app/'[locale]'/'(app)'/'(chat)'/chat/components/GenClawInput.tsx web/app/src/app/'[locale]'/'(app)'/'(chat)'/chat/components/OpenClawChatSurface.tsx web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderClient.tsx web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderProjectActionControls.tsx web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderProjectActions.tsx web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderStatusPane.tsx web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderTestPane.tsx web/app/tests/unit/app/agent-builder-client.unit.spec.tsx`
- `pnpm --dir web/app lint:ci`
- GitHub PR checks：`43/43 passed`



## fix(agent-builder): serialize project workspace mutations (#2686)

- **SHA**: `70792a456ebaaf9eb6a8f1a8ac5610bb841285a0`
- **作者**: kaka-srp <kaka@srp.one>
- **日期**: 2026-07-01T10:33:54Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/70792a456ebaaf9eb6a8f1a8ac5610bb841285a0
- **PR**: #2686

### 完整 Commit Message

```
fix(agent-builder): serialize project workspace mutations (#2686)

## Summary
- Serialize Agent Builder live workspace mutations in backend runtime
wrappers for clean, import, legacy restore, and publish.
- Guard each wrapper with the active project marker so stale concurrent
requests fail instead of modifying another project workspace.
- Treat `source_import_status=importing` as in-flight to avoid
reset/materialize/import races, and mark Open Project imports failed
when materialization/reset fails.
- Add focused tests for wrapper generation, heredoc syntax, in-flight
import behavior, and failure status updates.

## Tests
- `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/ruff check
app/services/agent_builder_service.py
tests/unit/test_agent_builder_service.py`
- `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/pyright
app/services/agent_builder_service.py
tests/unit/test_agent_builder_service.py`
- `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_agent_builder_service.py`
- pre-push `verify-changed` / `verify-py.sh` passed

## Notes
- Did not repack
`services/claw-interface/packs/agent-studio-pack.tar.gz`.
```

### PR Body

## Summary
- Serialize Agent Builder live workspace mutations in backend runtime wrappers for clean, import, legacy restore, and publish.
- Guard each wrapper with the active project marker so stale concurrent requests fail instead of modifying another project workspace.
- Treat `source_import_status=importing` as in-flight to avoid reset/materialize/import races, and mark Open Project imports failed when materialization/reset fails.
- Add focused tests for wrapper generation, heredoc syntax, in-flight import behavior, and failure status updates.

## Tests
- `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/ruff check app/services/agent_builder_service.py tests/unit/test_agent_builder_service.py`
- `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/pyright app/services/agent_builder_service.py tests/unit/test_agent_builder_service.py`
- `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_agent_builder_service.py`
- pre-push `verify-changed` / `verify-py.sh` passed

## Notes
- Did not repack `services/claw-interface/packs/agent-studio-pack.tar.gz`.



## fix(agent-builder): use display name for pack_name (#2681)

- **SHA**: `7d94250b102b26835f0e4fbca71db365161c80fa`
- **作者**: kaka-srp <kaka@srp.one>
- **日期**: 2026-07-01T09:50:00Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/7d94250b102b26835f0e4fbca71db365161c80fa
- **PR**: #2681

### 完整 Commit Message

```
fix(agent-builder): use display name for pack_name (#2681)

## Summary
- treat `pack_name` as the editable display name from the accepted Pack
Test run
- validate archive manifest identity against stable `display_id`, not
mutable `pack_name`
- stop candidate/test-run/submission matching from depending on mutable
names and keep Pack rows synced on submit/approve
- remove the vendored
`services/claw-interface/packs/agent-studio-pack.tar.gz`; Agent Studio
source stays in `.external-repos/ecap-agent-pack/agent-studio`

## Tests
- `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_pack_test_service.py::test_create_test_run_creates_new_run_for_repeated_same_hash_upload
tests/unit/test_pack_test_service.py::test_create_test_run_supersedes_prior_candidate_after_create
tests/unit/test_pack_test_service.py::test_validate_submission_gate_accepts_matching_promoted_asset
tests/unit/test_pack_test_service.py::test_promote_test_run_asset_rejects_run_for_different_pack
tests/unit/test_pack_test_repos.py::test_pack_test_run_repo_list_queries
tests/unit/test_pack_test_repos.py::test_pack_test_run_repo_ensure_indexes_success_and_failure
tests/unit/test_pack_services.py::test_submit_new_version_inserts_submission_only
tests/unit/test_pack_services.py::test_approve_marks_submission_and_syncs_pack_with_org_scope
tests/unit/test_pack_store_txn_repo.py::test_approve_submission_and_sync_pack_updates_both_inside_transaction
tests/unit/test_agent_builder_service.py::test_submit_test_iteration_promotes_and_submits_pack_store_directly
-q`
- `bash scripts/verify-changed.sh`
```

### PR Body

## Summary
- treat `pack_name` as the editable display name from the accepted Pack Test run
- validate archive manifest identity against stable `display_id`, not mutable `pack_name`
- stop candidate/test-run/submission matching from depending on mutable names and keep Pack rows synced on submit/approve
- remove the vendored `services/claw-interface/packs/agent-studio-pack.tar.gz`; Agent Studio source stays in `.external-repos/ecap-agent-pack/agent-studio`

## Tests
- `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_pack_test_service.py::test_create_test_run_creates_new_run_for_repeated_same_hash_upload tests/unit/test_pack_test_service.py::test_create_test_run_supersedes_prior_candidate_after_create tests/unit/test_pack_test_service.py::test_validate_submission_gate_accepts_matching_promoted_asset tests/unit/test_pack_test_service.py::test_promote_test_run_asset_rejects_run_for_different_pack tests/unit/test_pack_test_repos.py::test_pack_test_run_repo_list_queries tests/unit/test_pack_test_repos.py::test_pack_test_run_repo_ensure_indexes_success_and_failure tests/unit/test_pack_services.py::test_submit_new_version_inserts_submission_only tests/unit/test_pack_services.py::test_approve_marks_submission_and_syncs_pack_with_org_scope tests/unit/test_pack_store_txn_repo.py::test_approve_submission_and_sync_pack_updates_both_inside_transaction tests/unit/test_agent_builder_service.py::test_submit_test_iteration_promotes_and_submits_pack_store_directly -q`
- `bash scripts/verify-changed.sh`



## feat(agent-builder): add onboarding home page (#2676)

- **SHA**: `0df516541c4ee7db6f3f1a0360fb929245521513`
- **作者**: Nemo Feng <nemo@srp.one>
- **日期**: 2026-07-01T09:07:47Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/0df516541c4ee7db6f3f1a0360fb929245521513
- **PR**: #2676

### 完整 Commit Message

```
feat(agent-builder): add onboarding home page (#2676)

## What

`/agent-builder` now opens an onboarding-focused **home page** instead
of auto-redirecting to the last-opened project.

- **New user (empty):** prominent Create / Open buttons.
- **Returning user:** a "Continue where you left off" hero plus a
recent-projects list (status chip + updated time) with an inline "Show
all".
- **Deep link (`?prompt=`):** a card to create an agent from the pending
prompt.
- **Breadcrumb:** "Agent Builder" is now a link back to the home.

## Scope

Frontend-only — no backend / API / schema changes. Reuses the existing
`/agent-builder/projects` endpoints and the existing header action
cluster. Adds new presentational components under the `agent-builder/`
route; the only behavior changes to existing code are removing the entry
redirect and making the breadcrumb a link. Existing patterns are reused
(date formatter, button/chip/avatar styles).

## Testing

- Changes were built test-first; full `verify-web` passes locally
(project-wide `tsc` + vitest 3824 + eslint).
- `next build` is left to CI.

## Notes

- Visuals were validated against a local static demo that compiles the
real `globals.css` (this environment can't run a dev server); a preview
deploy is the final visual check.
- In the project view the breadcrumb is now a link, so that component no
longer renders an `<h1>` there.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What

`/agent-builder` now opens an onboarding-focused **home page** instead of auto-redirecting to the last-opened project.

- **New user (empty):** prominent Create / Open buttons.
- **Returning user:** a "Continue where you left off" hero plus a recent-projects list (status chip + updated time) with an inline "Show all".
- **Deep link (`?prompt=`):** a card to create an agent from the pending prompt.
- **Breadcrumb:** "Agent Builder" is now a link back to the home.

## Scope

Frontend-only — no backend / API / schema changes. Reuses the existing `/agent-builder/projects` endpoints and the existing header action cluster. Adds new presentational components under the `agent-builder/` route; the only behavior changes to existing code are removing the entry redirect and making the breadcrumb a link. Existing patterns are reused (date formatter, button/chip/avatar styles).

## Testing

- Changes were built test-first; full `verify-web` passes locally (project-wide `tsc` + vitest 3824 + eslint).
- `next build` is left to CI.

## Notes

- Visuals were validated against a local static demo that compiles the real `globals.css` (this environment can't run a dev server); a preview deploy is the final visual check.
- In the project view the breadcrumb is now a link, so that component no longer renders an `<h1>` there.

🤖 Generated with [Claude Code](https://claude.com/claude-code)



## feat(web): apply design system to specialist hub (#2679)

- **SHA**: `941deaf46af41e0b0052c44c56c0aebb4fa52f7b`
- **作者**: lynn Zhuang <lynn@srp.one>
- **日期**: 2026-07-01T08:17:15Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/941deaf46af41e0b0052c44c56c0aebb4fa52f7b
- **PR**: #2679

### 完整 Commit Message

```
feat(web): apply design system to specialist hub (#2679)

## Summary
- Apply `@zooclaw/design-system` components to the Specialist Hub page:
cards, tags, tabs, dialog, dropdown, buttons, inputs, alerts, and
skeletons.
- Tune the actual `/agents-manager` page shell: neutral page background,
white Specialist Hub panel, diffuse shadows, unclipped card/panel
shadows, and scrollbar placement at the panel edge.
- Add app-side design-system wiring via workspace dependency, token
import, Tailwind source scan, and Next transpilation.

## Verification
- `bash scripts/verify-web.sh 'web/app/next.config.ts'
'web/app/package.json'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/AgentsManagerClient.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentCard.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentCard.module.css'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentModal.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/SkillTags.tsx'
'web/app/src/app/globals.css' 'web/app/src/components/AppLayout.tsx'
'web/app/src/components/ClawConnectionStatus.tsx'`
- pre-commit frontend lint
- pre-push changed-surface verification

## Notes
- Local generated `.next.old*` folders and the temporary
`ds-pilot-preview` route were not included.

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
```

### PR Body

## Summary
- Apply `@zooclaw/design-system` components to the Specialist Hub page: cards, tags, tabs, dialog, dropdown, buttons, inputs, alerts, and skeletons.
- Tune the actual `/agents-manager` page shell: neutral page background, white Specialist Hub panel, diffuse shadows, unclipped card/panel shadows, and scrollbar placement at the panel edge.
- Add app-side design-system wiring via workspace dependency, token import, Tailwind source scan, and Next transpilation.

## Verification
- `bash scripts/verify-web.sh 'web/app/next.config.ts' 'web/app/package.json' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/AgentsManagerClient.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentCard.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentCard.module.css' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentModal.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/SkillTags.tsx' 'web/app/src/app/globals.css' 'web/app/src/components/AppLayout.tsx' 'web/app/src/components/ClawConnectionStatus.tsx'`
- pre-commit frontend lint
- pre-push changed-surface verification

## Notes
- Local generated `.next.old*` folders and the temporary `ds-pilot-preview` route were not included.



## feat(agent-diagnostics): add agent builder status endpoint (#2678)

- **SHA**: `e5178514c15e4834bb6ec85d84f41b553b25570d`
- **作者**: Chris@ZooClaw <chris@srp.one>
- **日期**: 2026-07-01T07:44:22Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/e5178514c15e4834bb6ec85d84f41b553b25570d
- **PR**: #2678

### 完整 Commit Message

```
feat(agent-diagnostics): add agent builder status endpoint (#2678)

## Summary
- Add a read-only `/agent-diagnostics/agent-builder/status` endpoint for
Harold Finch and other ops agents.
- Resolve Agent Builder projects, iterations, Pack Test runs, runtime
assets, and temporary test bot identifiers by project, test run, or
computer id.
- Add unit coverage for aggregation, sanitization, failure reporting,
and route wiring.

## Why
Harold needs a supported claw-interface surface for Agent Builder
incidents instead of guessing from user-facing routes or probing
databases directly.

## Test Plan
- `uv run --no-project --with-requirements requirements.txt
--with-requirements requirements-dev.txt python -m pytest
tests/unit/test_agent_diagnostics_billing.py
tests/unit/test_agent_builder_routes.py
tests/unit/test_pack_test_runtime_service.py
tests/unit/test_agent_builder_diagnostics.py -q`
```

### PR Body

## Summary
- Add a read-only `/agent-diagnostics/agent-builder/status` endpoint for Harold Finch and other ops agents.
- Resolve Agent Builder projects, iterations, Pack Test runs, runtime assets, and temporary test bot identifiers by project, test run, or computer id.
- Add unit coverage for aggregation, sanitization, failure reporting, and route wiring.

## Why
Harold needs a supported claw-interface surface for Agent Builder incidents instead of guessing from user-facing routes or probing databases directly.

## Test Plan
- `uv run --no-project --with-requirements requirements.txt --with-requirements requirements-dev.txt python -m pytest tests/unit/test_agent_diagnostics_billing.py tests/unit/test_agent_builder_routes.py tests/unit/test_pack_test_runtime_service.py tests/unit/test_agent_builder_diagnostics.py -q`
