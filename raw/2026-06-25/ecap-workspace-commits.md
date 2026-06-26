# SerendipityOneInc/ecap-workspace — commits 2026-06-25


共 16 个 commit


---

## refactor(claw-interface): split openclaw init responsibilities (#2557)

- **SHA**: 16ae42a943304fe9a3761eff7f9872b2bf64ca92
- **作者**: bill-srp (@bill-srp)
- **日期**: 2026-06-25T13:49:05Z
- **PR**: #2557
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/16ae42a943304fe9a3761eff7f9872b2bf64ca92

### 完整 Commit Message

```
refactor(claw-interface): split openclaw init responsibilities (#2557)

## Summary

- Move account-root Mattermost user initialization into account
registration and fail registration when it cannot be created.
- Keep normalized computer creation focused on bot/agent resources,
including agent Mattermost provisioning, without re-reading account data
inside helpers.
- Block expired subscriptions before `POST /computers` starts quota
checks, reservations, Mattermost setup, or FastClaw bot creation.

## Tests

- `PATH="$PWD/services/claw-interface/.venv/bin:$PATH" bash
scripts/verify-py.sh`
- `cd services/claw-interface && .venv/bin/pytest
tests/unit/test_account_service.py
tests/unit/test_computer_create_service.py
tests/unit/test_computer_service.py
tests/unit/test_mattermost_provisioner.py
tests/unit/test_bot_state_service.py -q --tb=short`
```

### 完整 PR Body

## Summary

- Move account-root Mattermost user initialization into account registration and fail registration when it cannot be created.
- Keep normalized computer creation focused on bot/agent resources, including agent Mattermost provisioning, without re-reading account data inside helpers.
- Block expired subscriptions before `POST /computers` starts quota checks, reservations, Mattermost setup, or FastClaw bot creation.

## Tests

- `PATH="$PWD/services/claw-interface/.venv/bin:$PATH" bash scripts/verify-py.sh`
- `cd services/claw-interface && .venv/bin/pytest tests/unit/test_account_service.py tests/unit/test_computer_create_service.py tests/unit/test_computer_service.py tests/unit/test_mattermost_provisioner.py tests/unit/test_bot_state_service.py -q --tb=short`



---

## fix(vertical-pack): expose package quick commands (#2605)

- **SHA**: 876eacf18d2ece775d96f3ea8cffa2e557636719
- **作者**: bill-srp (@bill-srp)
- **日期**: 2026-06-25T13:42:19Z
- **PR**: #2605
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/876eacf18d2ece775d96f3ea8cffa2e557636719

### 完整 Commit Message

```
fix(vertical-pack): expose package quick commands (#2605)

## Summary
- Return purchased vertical package agent pack metadata from `GET
/vertical-pack/package/current`.
- Merge current vertical package packs into New Task quick-command
lookup so hidden package agents can show Quick Start cards.
- Cover backend current-package pack details and frontend hidden
vertical-pack quick commands with focused tests.

## Root cause
Vertical package installation used package pack IDs, but New Task quick
commands only read the public `/agent-packs` catalog. Packs hidden from
the public market were installable through vertical packages but
unavailable to the New Task metadata lookup, so their `quick_commands`
were not rendered.

## Test plan
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_vertical_pack_plans_routes.py
services/claw-interface/tests/unit/test_schema_vertical_pack_package.py
-q`
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh
'web/app/src/app/[locale]/(app)/new-chat/useViewModel.ts'
web/app/src/hooks/useVerticalPackPackageInstaller.ts
web/app/src/services/vertical-pack-package.ts
web/app/tests/unit/app/new-chat/NewChatClient.unit.spec.tsx
web/app/tests/unit/app/new-chat/useViewModel.unit.spec.tsx
web/app/tests/unit/services/vertical-pack-package.unit.spec.ts`
```

### 完整 PR Body

## Summary
- Return purchased vertical package agent pack metadata from `GET /vertical-pack/package/current`.
- Merge current vertical package packs into New Task quick-command lookup so hidden package agents can show Quick Start cards.
- Cover backend current-package pack details and frontend hidden vertical-pack quick commands with focused tests.

## Root cause
Vertical package installation used package pack IDs, but New Task quick commands only read the public `/agent-packs` catalog. Packs hidden from the public market were installable through vertical packages but unavailable to the New Task metadata lookup, so their `quick_commands` were not rendered.

## Test plan
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_vertical_pack_plans_routes.py services/claw-interface/tests/unit/test_schema_vertical_pack_package.py -q`
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/new-chat/useViewModel.ts' web/app/src/hooks/useVerticalPackPackageInstaller.ts web/app/src/services/vertical-pack-package.ts web/app/tests/unit/app/new-chat/NewChatClient.unit.spec.tsx web/app/tests/unit/app/new-chat/useViewModel.unit.spec.tsx web/app/tests/unit/services/vertical-pack-package.unit.spec.ts`



---

## fix(agents): wire publish delete to deprecate org packs (#2602)

- **SHA**: 0869fce58993a525be618daab5c840234d6426fe
- **作者**: bill-srp (@bill-srp)
- **日期**: 2026-06-25T12:54:07Z
- **PR**: #2602
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/0869fce58993a525be618daab5c840234d6426fe

### 完整 Commit Message

```
fix(agents): wire publish delete to deprecate org packs (#2602)

## Summary
- Wire the publish-page Delete action to org pack deprecation.
- Add a confirmation modal and preserve backend pack_id for the
deprecate call.
- Keep Delete disabled for installed agents and non-deprecatable publish
records.

## Tests
- pnpm --dir web/app exec vitest run
tests/unit/app/agents-manager-publish.unit.spec.tsx
- bash scripts/verify-web.sh
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/PublishAgentsClient.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/components/PublishDeleteConfirmModal.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/components/types.ts'
web/app/src/models/org-agent-pack.ts
web/app/src/services/org-agent-packs.ts
web/app/tests/unit/app/agents-manager-publish.unit.spec.tsx
- bash scripts/verify-changed.sh
```

### 完整 PR Body

## Summary
- Wire the publish-page Delete action to org pack deprecation.
- Add a confirmation modal and preserve backend pack_id for the deprecate call.
- Keep Delete disabled for installed agents and non-deprecatable publish records.

## Tests
- pnpm --dir web/app exec vitest run tests/unit/app/agents-manager-publish.unit.spec.tsx
- bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/PublishAgentsClient.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/components/PublishDeleteConfirmModal.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/components/types.ts' web/app/src/models/org-agent-pack.ts web/app/src/services/org-agent-packs.ts web/app/tests/unit/app/agents-manager-publish.unit.spec.tsx
- bash scripts/verify-changed.sh



---

## fix: rename boss info bind route (#2603)

- **SHA**: 7f0817d0100c8367a2cc8286238deb85afac6c38
- **作者**: sam-srp (@sam-srp)
- **日期**: 2026-06-25T12:43:54Z
- **PR**: #2603
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/7f0817d0100c8367a2cc8286238deb85afac6c38

### 完整 Commit Message

```
fix: rename boss info bind route (#2603)

## Summary
- change claw-interface bind endpoint from /zooclaw/boss-info/bind to
/boss-info/bind
- update the BossClaw web BFF route to /api/boss-info/bind and proxy to
/boss-info/bind
- update BossClaw login and unit tests to use the new path

## Rollout note
This is an intentional route naming correction before the endpoint is
treated as a compatibility surface. The old zooclaw-prefixed URL should
not be kept as an alias; new callers should use /boss-info/bind only.

## Tests
- conda run -n base python -m ruff format
services/claw-interface/app/routes/zooclaw_boss_info.py
- conda run -n base python -m ruff check
services/claw-interface/app/routes/zooclaw_boss_info.py
- conda run -n base pytest
services/claw-interface/tests/unit/test_zooclaw_boss_info.py
- pnpm vitest run --config ./vitest.config.mts
tests/unit/app/api/zooclaw-boss-info-bind.unit.spec.ts
tests/unit/bossclaw/phone-login-step.unit.spec.tsx
- pnpm exec eslint
src/app/[locale]/bossclaw/components/PhoneLoginStep.tsx
src/app/api/boss-info/bind/route.ts
tests/unit/app/api/zooclaw-boss-info-bind.unit.spec.ts
tests/unit/bossclaw/phone-login-step.unit.spec.tsx --quiet
```

### 完整 PR Body

## Summary
- change claw-interface bind endpoint from /zooclaw/boss-info/bind to /boss-info/bind
- update the BossClaw web BFF route to /api/boss-info/bind and proxy to /boss-info/bind
- update BossClaw login and unit tests to use the new path

## Rollout note
This is an intentional route naming correction before the endpoint is treated as a compatibility surface. The old zooclaw-prefixed URL should not be kept as an alias; new callers should use /boss-info/bind only.

## Tests
- conda run -n base python -m ruff format services/claw-interface/app/routes/zooclaw_boss_info.py
- conda run -n base python -m ruff check services/claw-interface/app/routes/zooclaw_boss_info.py
- conda run -n base pytest services/claw-interface/tests/unit/test_zooclaw_boss_info.py
- pnpm vitest run --config ./vitest.config.mts tests/unit/app/api/zooclaw-boss-info-bind.unit.spec.ts tests/unit/bossclaw/phone-login-step.unit.spec.tsx
- pnpm exec eslint src/app/[locale]/bossclaw/components/PhoneLoginStep.tsx src/app/api/boss-info/bind/route.ts tests/unit/app/api/zooclaw-boss-info-bind.unit.spec.ts tests/unit/bossclaw/phone-login-step.unit.spec.tsx --quiet



---

## feat(zooclaw-ds): align Button to shadcn radix-nova + preview Iconography & sidebar polish (#2578)

- **SHA**: d46b294421ee54ed6d593d8da7acae9b65ee78fa
- **作者**: lynn Zhuang (@lynn-srp)
- **日期**: 2026-06-25T12:12:16Z
- **PR**: #2578
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/d46b294421ee54ed6d593d8da7acae9b65ee78fa

### 完整 Commit Message

```
feat(zooclaw-ds): align Button to shadcn radix-nova + preview Iconography & sidebar polish (#2578)

## What

A **Button** alignment to shadcn's radix-nova spec, plus
**preview-site** docs. No token changes; nothing in `web/app`.

### 1. Button → shadcn radix-nova (`src/components/button.tsx`)
Ported shadcn's radix-nova `Button` verbatim (base classes, all 8 sizes,
`data-icon` spacing, `data-variant`/`data-size` attrs, `aria-invalid` +
active press-down states), rendered through ZooClaw's shadcn-shaped
tokens.

- **Variants now match upstream exactly:** `default · outline · ghost ·
destructive · secondary · link`. Removed the non-standard `primary`.
- **`destructive`** is the radix-nova **soft tint** (`bg-destructive/10
text-destructive`), not a solid red fill.
- **Sizes:** `default · xs · sm · lg · icon · icon-xs · icon-sm ·
icon-lg` (was 4).
- **One deliberate deviation:** `default` keeps ZooClaw's **dark CTA
surface** instead of upstream's `bg-primary`. ZooClaw maps `--primary` →
brand red, so a verbatim port would make the default button red — which
matches neither shadcn's dark-default look nor ZooClaw's "red is an
accent, not a fill" rule. Brand red stays on `link` / focus ring /
`destructive`.
- Tests updated to the new taxonomy (variant set, soft destructive,
`size-8` icon, `data-variant`/`data-size`).

### 2. Preview (`preview/`)
- **Button section** rebuilt to the radix-nova matrix: 6 variants, 8
sizes, icon buttons, `data-icon` spacing, a `rounded-full` pill, and a
disabled state.
- **Iconography section** (new, under Foundations) documenting the
Heroicons convention — `24/outline` for decorative/actions, `16/solid`
for inline indicators, `currentColor` inheritance.
- **Sidebar:** clickable nav items now read darker than the muted,
non-clickable group headers, so they signal interactivity.

## Verification
- `pnpm exec tsc --noEmit` — clean
- `pnpm exec vitest run` — full suite green
- `pnpm run lint` — clean
- `pnpm run build:preview` — builds
- Visually confirmed in the running preview.

## Scope
Only `web/packages/zooclaw-design-system/`
(`src/components/button.{tsx,test.tsx}` +
`preview/{App.tsx,preview.css}`).

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### 完整 PR Body

## What

A **Button** alignment to shadcn's radix-nova spec, plus **preview-site** docs. No token changes; nothing in `web/app`.

### 1. Button → shadcn radix-nova (`src/components/button.tsx`)
Ported shadcn's radix-nova `Button` verbatim (base classes, all 8 sizes, `data-icon` spacing, `data-variant`/`data-size` attrs, `aria-invalid` + active press-down states), rendered through ZooClaw's shadcn-shaped tokens.

- **Variants now match upstream exactly:** `default · outline · ghost · destructive · secondary · link`. Removed the non-standard `primary`.
- **`destructive`** is the radix-nova **soft tint** (`bg-destructive/10 text-destructive`), not a solid red fill.
- **Sizes:** `default · xs · sm · lg · icon · icon-xs · icon-sm · icon-lg` (was 4).
- **One deliberate deviation:** `default` keeps ZooClaw's **dark CTA surface** instead of upstream's `bg-primary`. ZooClaw maps `--primary` → brand red, so a verbatim port would make the default button red — which matches neither shadcn's dark-default look nor ZooClaw's "red is an accent, not a fill" rule. Brand red stays on `link` / focus ring / `destructive`.
- Tests updated to the new taxonomy (variant set, soft destructive, `size-8` icon, `data-variant`/`data-size`).

### 2. Preview (`preview/`)
- **Button section** rebuilt to the radix-nova matrix: 6 variants, 8 sizes, icon buttons, `data-icon` spacing, a `rounded-full` pill, and a disabled state.
- **Iconography section** (new, under Foundations) documenting the Heroicons convention — `24/outline` for decorative/actions, `16/solid` for inline indicators, `currentColor` inheritance.
- **Sidebar:** clickable nav items now read darker than the muted, non-clickable group headers, so they signal interactivity.

## Verification
- `pnpm exec tsc --noEmit` — clean
- `pnpm exec vitest run` — full suite green
- `pnpm run lint` — clean
- `pnpm run build:preview` — builds
- Visually confirmed in the running preview.

## Scope
Only `web/packages/zooclaw-design-system/` (`src/components/button.{tsx,test.tsx}` + `preview/{App.tsx,preview.css}`).



---

## feat(sidenav): 去掉 My Team 添加专家加号并更换 AI Specialists Hub 图标 (#2601)

- **SHA**: 75afee6114f4e755f84dffdde7822358d6420c78
- **作者**: lynn Zhuang (@lynn-srp)
- **日期**: 2026-06-25T12:03:19Z
- **PR**: #2601
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/75afee6114f4e755f84dffdde7822358d6420c78

### 完整 Commit Message

```
feat(sidenav): 去掉 My Team 添加专家加号并更换 AI Specialists Hub 图标 (#2601)

## What & Why

侧边栏导航的两处微调，目标是去掉冗余的「添加专家」入口并让 Hub 图标语义更贴切：

1. **去掉 `My Team` 标题旁的「添加专家」加号按钮** —— 该 `+` 按钮指向 `/agents-manager`，与下方的
**AI Specialists Hub** 导航项完全重复（同一目标路由），属于冗余入口，移除后标题行更干净。
2. **更换 AI Specialists Hub 图标** —— 由原来的「加号圆圈」(`PlusCircleIcon`) 改为
**`UserGroupIcon`**（一组人物）。加号圆圈语义偏「新建/添加」，而 Hub
实为「浏览/雇佣专家」的目的地，人物组图标更契合，也与刚移除的 `+` 入口不再视觉撞车。

## Changes

- `web/app/src/components/sidenav/SideNavAgentList.tsx`
  - 删除 `My Team` 表头右侧的加号链接 + 其 hover tooltip
  - 顺带清理仅被该块使用的导入：`PlusCircleIcon`、`LocaleLink`、`TooltipArrowDownIcon`
  - 表头容器去掉已无意义的 `justify-between`（其唯一作用是把 `+` 推到右端）
- `web/app/src/components/sidenav/build-bottom-nav-items.ts`
  - `agents-manager` 项图标 `PlusCircleIcon`（outline 别名）→ `UserGroupIcon`
- `web/app/tests/unit/components/sidenav/SideNavAgentList.unit.spec.tsx`
- 更新两条断言：表头渲染时「不再」出现添加专家按钮；collapsed 模式下表头省略（锚点从已永久消失的按钮 label 改为 `My
Team` 标题）

> 注：`nav.addSpecialists` i18n key 现已无引用，但仍存在于 10 个 locale 文件中。本 PR
未删除它，以免把 diff 扩散到 10 个语言文件；如需清理可另起小 PR。

## Verification

- `bash scripts/verify-web.sh <changed paths>` —— 全绿：CI guards ✓ / `tsc
--noEmit` ✓ / vitest（36 passed）✓ / eslint ✓
- 本地 mock 栈（`scripts/dev-mock.sh`，`ready-user` 场景）人工核验：`My Team`
表头不再有加号；AI Specialists Hub 显示为人物组图标。每个 agent 行右侧的 `+` 是「New
Task」按钮（`SideNavAgentRow`），与本次改动无关、保持原样。

## Risk

低。仅 sidenav 渲染层改动，无数据/接口/路由变更；被移除的 `+` 入口功能由现存的 AI Specialists Hub
项完整覆盖。

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
```

### 完整 PR Body

## What & Why

侧边栏导航的两处微调，目标是去掉冗余的「添加专家」入口并让 Hub 图标语义更贴切：

1. **去掉 `My Team` 标题旁的「添加专家」加号按钮** —— 该 `+` 按钮指向 `/agents-manager`，与下方的 **AI Specialists Hub** 导航项完全重复（同一目标路由），属于冗余入口，移除后标题行更干净。
2. **更换 AI Specialists Hub 图标** —— 由原来的「加号圆圈」(`PlusCircleIcon`) 改为 **`UserGroupIcon`**（一组人物）。加号圆圈语义偏「新建/添加」，而 Hub 实为「浏览/雇佣专家」的目的地，人物组图标更契合，也与刚移除的 `+` 入口不再视觉撞车。

## Changes

- `web/app/src/components/sidenav/SideNavAgentList.tsx`
  - 删除 `My Team` 表头右侧的加号链接 + 其 hover tooltip
  - 顺带清理仅被该块使用的导入：`PlusCircleIcon`、`LocaleLink`、`TooltipArrowDownIcon`
  - 表头容器去掉已无意义的 `justify-between`（其唯一作用是把 `+` 推到右端）
- `web/app/src/components/sidenav/build-bottom-nav-items.ts`
  - `agents-manager` 项图标 `PlusCircleIcon`（outline 别名）→ `UserGroupIcon`
- `web/app/tests/unit/components/sidenav/SideNavAgentList.unit.spec.tsx`
  - 更新两条断言：表头渲染时「不再」出现添加专家按钮；collapsed 模式下表头省略（锚点从已永久消失的按钮 label 改为 `My Team` 标题）

> 注：`nav.addSpecialists` i18n key 现已无引用，但仍存在于 10 个 locale 文件中。本 PR 未删除它，以免把 diff 扩散到 10 个语言文件；如需清理可另起小 PR。

## Verification

- `bash scripts/verify-web.sh <changed paths>` —— 全绿：CI guards ✓ / `tsc --noEmit` ✓ / vitest（36 passed）✓ / eslint ✓
- 本地 mock 栈（`scripts/dev-mock.sh`，`ready-user` 场景）人工核验：`My Team` 表头不再有加号；AI Specialists Hub 显示为人物组图标。每个 agent 行右侧的 `+` 是「New Task」按钮（`SideNavAgentRow`），与本次改动无关、保持原样。

## Risk

低。仅 sidenav 渲染层改动，无数据/接口/路由变更；被移除的 `+` 入口功能由现存的 AI Specialists Hub 项完整覆盖。



---

## feat(claw-interface): add bossclaw cold start binding (#2598)

- **SHA**: 394d134b24a04bc6f59464021702f28b56b483d6
- **作者**: sam-srp (@sam-srp)
- **日期**: 2026-06-25T11:57:44Z
- **PR**: #2598
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/394d134b24a04bc6f59464021702f28b56b483d6

### 完整 Commit Message

```
feat(claw-interface): add bossclaw cold start binding (#2598)

## Summary
- add ZooClaw boss cold-start binding endpoint in claw-interface
- read prepared boss info from google_sheet_data_sync and persist
uid/boss_key/boss_info into zooclaw_boss_info
- add unique indexes for uid and boss_key plus focused unit coverage

## Validation
- conda run -n base pytest
services/claw-interface/tests/unit/test_zooclaw_boss_info.py
- conda run -n base python -m ruff check
services/claw-interface/app/create_app.py
services/claw-interface/app/lifetime.py
services/claw-interface/app/database/collections.py
services/claw-interface/app/database/zooclaw_boss_info_repo.py
services/claw-interface/app/routes/zooclaw_boss_info.py
services/claw-interface/app/schema/zooclaw_boss_info.py
services/claw-interface/tests/unit/test_zooclaw_boss_info.py
- conda run -n base python -m py_compile
services/claw-interface/app/database/zooclaw_boss_info_repo.py
services/claw-interface/app/routes/zooclaw_boss_info.py
services/claw-interface/app/schema/zooclaw_boss_info.py
services/claw-interface/tests/unit/test_zooclaw_boss_info.py
- git diff --check
```

### 完整 PR Body

## Summary
- add ZooClaw boss cold-start binding endpoint in claw-interface
- read prepared boss info from google_sheet_data_sync and persist uid/boss_key/boss_info into zooclaw_boss_info
- add unique indexes for uid and boss_key plus focused unit coverage

## Validation
- conda run -n base pytest services/claw-interface/tests/unit/test_zooclaw_boss_info.py
- conda run -n base python -m ruff check services/claw-interface/app/create_app.py services/claw-interface/app/lifetime.py services/claw-interface/app/database/collections.py services/claw-interface/app/database/zooclaw_boss_info_repo.py services/claw-interface/app/routes/zooclaw_boss_info.py services/claw-interface/app/schema/zooclaw_boss_info.py services/claw-interface/tests/unit/test_zooclaw_boss_info.py
- conda run -n base python -m py_compile services/claw-interface/app/database/zooclaw_boss_info_repo.py services/claw-interface/app/routes/zooclaw_boss_info.py services/claw-interface/app/schema/zooclaw_boss_info.py services/claw-interface/tests/unit/test_zooclaw_boss_info.py
- git diff --check


---

## feat(agents): limit v2 installs by plan (#2597)

- **SHA**: dfd5bdddaeb942264df2bd9f45d1b10bdecb14c1
- **作者**: bill-srp (@bill-srp)
- **日期**: 2026-06-25T11:37:49Z
- **PR**: #2597
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/dfd5bdddaeb942264df2bd9f45d1b10bdecb14c1

### 完整 Commit Message

```
feat(agents): limit v2 installs by plan (#2597)

## Summary

- limit V2 computer-scoped agent installs by subscription tier
- count only active/non-terminal V2 agent workspace rows for the target
computer
- keep existing same-agent reinstall/update paths from consuming an
extra quota slot

## Linear


https://linear.app/srpone/issue/ECA-841/limit-hired-agents-by-subscription-tier

## Validation

- `/Users/bill/.venvs/claw-interface/bin/pytest
services/claw-interface/tests/unit/test_agent_install_service.py
services/claw-interface/tests/unit/test_agent_workspace_repo.py -q`
- `PATH="/Users/bill/.venvs/claw-interface/bin:$PATH" bash
scripts/verify-py.sh`
- `PATH="/Users/bill/.venvs/claw-interface/bin:$PATH" bash
scripts/verify-changed.sh`
```

### 完整 PR Body

## Summary

- limit V2 computer-scoped agent installs by subscription tier
- count only active/non-terminal V2 agent workspace rows for the target computer
- keep existing same-agent reinstall/update paths from consuming an extra quota slot

## Linear

https://linear.app/srpone/issue/ECA-841/limit-hired-agents-by-subscription-tier

## Validation

- `/Users/bill/.venvs/claw-interface/bin/pytest services/claw-interface/tests/unit/test_agent_install_service.py services/claw-interface/tests/unit/test_agent_workspace_repo.py -q`
- `PATH="/Users/bill/.venvs/claw-interface/bin:$PATH" bash scripts/verify-py.sh`
- `PATH="/Users/bill/.venvs/claw-interface/bin:$PATH" bash scripts/verify-changed.sh`



---

## refactor(claw-interface): retire warm pool user finalize path (#2587)

- **SHA**: 6ee85ece471bc82bbebcdd3c32b42e9b0f14b6b4
- **作者**: bill-srp (@bill-srp)
- **日期**: 2026-06-25T11:33:11Z
- **PR**: #2587
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/6ee85ece471bc82bbebcdd3c32b42e9b0f14b6b4

### 完整 Commit Message

```
refactor(claw-interface): retire warm pool user finalize path (#2587)

## Summary

- Retire the legacy warm-pool user finalize path.
- Remove obsolete warm-pool materialization tests tied to that path.

## Stack

1. Base: #2586 / `feat/warm-pool-runtime-computer-claim`
2. This PR: #2587 legacy user finalize path cleanup.
3. Next: #2588 legacy `/openclaw/init` claim and finalize-state cleanup.

## Size

- Local size-gate estimate: 2095 lines after exclusions.
- This is 95 lines over the 2000-line gate because it is mostly deletion
of obsolete legacy tests and finalize-path coverage; applying
`size-override`.

## Verification

- `PATH="/Users/bill/.venvs/claw-interface/bin:$PATH" bash
scripts/verify-py.sh`
```

### 完整 PR Body

## Summary

- Retire the legacy warm-pool user finalize path.
- Remove obsolete warm-pool materialization tests tied to that path.

## Stack

1. Base: #2586 / `feat/warm-pool-runtime-computer-claim`
2. This PR: #2587 legacy user finalize path cleanup.
3. Next: #2588 legacy `/openclaw/init` claim and finalize-state cleanup.

## Size

- Local size-gate estimate: 2095 lines after exclusions.
- This is 95 lines over the 2000-line gate because it is mostly deletion of obsolete legacy tests and finalize-path coverage; applying `size-override`.

## Verification

- `PATH="/Users/bill/.venvs/claw-interface/bin:$PATH" bash scripts/verify-py.sh`



---

## feat(sidenav): agent 行多开手风琴与新任务入口交互重做 (#2600)

- **SHA**: 1a8bda7dfd68e12d8cbec3272035f6c07c33da9e
- **作者**: lynn Zhuang (@lynn-srp)
- **日期**: 2026-06-25T10:59:43Z
- **PR**: #2600
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/1a8bda7dfd68e12d8cbec3272035f6c07c33da9e

### 完整 Commit Message

```
feat(sidenav): agent 行多开手风琴与新任务入口交互重做 (#2600)

## 背景

侧边栏 MY TEAM 的 agent 行交互重做，覆盖「折叠/展开」与「发起新任务」两块，参考设计稿对齐。

## 改动

### 1. 多开手风琴（`SideNav.tsx` + `expanded-agents.ts`）
展开态由单值 `expandedAgentId: string | null` 改为 `Set<string>`，可**同时展开多个
agent**。集合只在手动点击时增删、在导航进某 agent 时**叠加**（保留其他已展开），收起完全靠手动。抽出纯函数
`toggleExpandedAgent` / `withExpandedAgent` 并单测。

### 2. agent 行重做（`SideNavAgentRow.tsx`）
- **去掉 hover 背景块**；agent 名字只有两态：默认 `text-muted-foreground`、hover
`text-foreground`（无选中态）。
- **箭头移到名字正后面**，且**仅在 hover 名字时出现**（group 收窄到名字按钮，所以
hover「＋」不会再触发箭头）；默认朝下（`ChevronDownIcon`），展开时 `rotate-180` 朝上。
- 每行**右侧常驻「＋」新任务按钮**，深链 `/new-chat?agent_id=X`，hover 出现
tooltip（右对齐向左展开，避免被侧栏 `overflow` 裁断）。

### 3. 移除面板内「＋ New chat」（`SideNavAgentSessions.tsx`）
新任务入口已上移到行上的「＋」，展开面板只保留 Session History + 历史会话。

### 4. 适配（`SideNavAgentList.tsx` / `useAgentScrollOverlay.ts`）
列表 prop 改 `expandedAgentIds: Set`、`isExpanded` 用 `.has()`；滚动遮罩重测依赖从单个 id
改为集合派生 key。

## 验证

- `bash scripts/verify-web.sh`：`tsc` + `eslint` + 单元测试全绿。
- 全程 TDD：`expanded-agents` 多开 toggle/叠加、列表多开渲染、行上「＋」深链、面板移除 New chat
均有用例；hook 改名同步更新。
- 本地 mock 栈逐项实测（computed style）：箭头方向（收起 ↓ / 展开 ↑）、箭头与名字变黑仅 hover
名字时成立、hover「＋」只出 tooltip 不出箭头、tooltip 不再截断、多开可同时展开。

## 影响范围

- 仅前端 `web/app` 侧边栏 agent 行，纯 UI/交互改动，无接口变更。

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
```

### 完整 PR Body

## 背景

侧边栏 MY TEAM 的 agent 行交互重做，覆盖「折叠/展开」与「发起新任务」两块，参考设计稿对齐。

## 改动

### 1. 多开手风琴（`SideNav.tsx` + `expanded-agents.ts`）
展开态由单值 `expandedAgentId: string | null` 改为 `Set<string>`，可**同时展开多个 agent**。集合只在手动点击时增删、在导航进某 agent 时**叠加**（保留其他已展开），收起完全靠手动。抽出纯函数 `toggleExpandedAgent` / `withExpandedAgent` 并单测。

### 2. agent 行重做（`SideNavAgentRow.tsx`）
- **去掉 hover 背景块**；agent 名字只有两态：默认 `text-muted-foreground`、hover `text-foreground`（无选中态）。
- **箭头移到名字正后面**，且**仅在 hover 名字时出现**（group 收窄到名字按钮，所以 hover「＋」不会再触发箭头）；默认朝下（`ChevronDownIcon`），展开时 `rotate-180` 朝上。
- 每行**右侧常驻「＋」新任务按钮**，深链 `/new-chat?agent_id=X`，hover 出现 tooltip（右对齐向左展开，避免被侧栏 `overflow` 裁断）。

### 3. 移除面板内「＋ New chat」（`SideNavAgentSessions.tsx`）
新任务入口已上移到行上的「＋」，展开面板只保留 Session History + 历史会话。

### 4. 适配（`SideNavAgentList.tsx` / `useAgentScrollOverlay.ts`）
列表 prop 改 `expandedAgentIds: Set`、`isExpanded` 用 `.has()`；滚动遮罩重测依赖从单个 id 改为集合派生 key。

## 验证

- `bash scripts/verify-web.sh`：`tsc` + `eslint` + 单元测试全绿。
- 全程 TDD：`expanded-agents` 多开 toggle/叠加、列表多开渲染、行上「＋」深链、面板移除 New chat 均有用例；hook 改名同步更新。
- 本地 mock 栈逐项实测（computed style）：箭头方向（收起 ↓ / 展开 ↑）、箭头与名字变黑仅 hover 名字时成立、hover「＋」只出 tooltip 不出箭头、tooltip 不再截断、多开可同时展开。

## 影响范围

- 仅前端 `web/app` 侧边栏 agent 行，纯 UI/交互改动，无接口变更。



---

## refactor(claw-interface): claim warm pool runtime into computers (#2586)

- **SHA**: baab78faae3d2969cc5167997c60f56e98f7d19d
- **作者**: bill-srp (@bill-srp)
- **日期**: 2026-06-25T10:56:20Z
- **PR**: #2586
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/baab78faae3d2969cc5167997c60f56e98f7d19d

### 完整 Commit Message

```
refactor(claw-interface): claim warm pool runtime into computers (#2586)

## Summary

- Claim warm-pool runtime assets into computer, bot, and Mattermost
state.
- Add coverage for computer-store projection of claimed warm-pool
runtime data.

## Stack

1. Base: #2585 / `feat/warm-pool-account-claim`
2. This PR: #2586 runtime assets claimed into the computer store.
3. Next: #2587 retire the legacy user finalize path.

## Size

- Local size-gate estimate: 707 lines after exclusions.

## Verification

- `PATH="/Users/bill/.venvs/claw-interface/bin:$PATH" bash
scripts/verify-py.sh`
```

### 完整 PR Body

## Summary

- Claim warm-pool runtime assets into computer, bot, and Mattermost state.
- Add coverage for computer-store projection of claimed warm-pool runtime data.

## Stack

1. Base: #2585 / `feat/warm-pool-account-claim`
2. This PR: #2586 runtime assets claimed into the computer store.
3. Next: #2587 retire the legacy user finalize path.

## Size

- Local size-gate estimate: 707 lines after exclusions.

## Verification

- `PATH="/Users/bill/.venvs/claw-interface/bin:$PATH" bash scripts/verify-py.sh`



---

## docs(agent): document agent diagnose auth (#2596)

- **SHA**: 6b22dd83c39afad5fdc0e20872fedd0c49cfda57
- **作者**: Chris@ZooClaw (@chris-srp)
- **日期**: 2026-06-25T09:00:23Z
- **PR**: #2596
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/6b22dd83c39afad5fdc0e20872fedd0c49cfda57

### 完整 Commit Message

```
docs(agent): document agent diagnose auth (#2596)

## Summary

- Document the cross-repo `/agent-diagnose` read-only diagnostics route
in root `AGENTS.md`.
- Add `claw-interface` guidance that `AGENT_DIAGNOSE_READ_TOKEN` is
shared with `user-interface` and must stay limited to masked read-only
diagnostic lookups.

## Validation

- `git diff --check`
- Commit pre-commit hooks passed for documentation changes.
- Push pre-push verification was attempted; `verify-py.sh` reached
pyright and failed because this lightweight worktree has no backend
venv/dependencies installed (`fastapi`, `pytest`, `favie_common`, etc.).
Pushed with `SKIP_VERIFY=1` because the branch is docs-only.
```

### 完整 PR Body

## Summary

- Document the cross-repo `/agent-diagnose` read-only diagnostics route in root `AGENTS.md`.
- Add `claw-interface` guidance that `AGENT_DIAGNOSE_READ_TOKEN` is shared with `user-interface` and must stay limited to masked read-only diagnostic lookups.

## Validation

- `git diff --check`
- Commit pre-commit hooks passed for documentation changes.
- Push pre-push verification was attempted; `verify-py.sh` reached pyright and failed because this lightweight worktree has no backend venv/dependencies installed (`fastapi`, `pytest`, `favie_common`, etc.). Pushed with `SKIP_VERIFY=1` because the branch is docs-only.



---

## refactor(claw-interface): split warm pool account claim (#2585)

- **SHA**: e286f098967bfb2cdb434777ef89d1128f6c819c
- **作者**: bill-srp (@bill-srp)
- **日期**: 2026-06-25T08:30:21Z
- **PR**: #2585
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/e286f098967bfb2cdb434777ef89d1128f6c819c

### 完整 Commit Message

```
refactor(claw-interface): split warm pool account claim (#2585)

## Summary

- Split warm-pool account claim flow from legacy user materialization.
- Remove unused account adoption hooks.

## Stack

1. Base: #2584 / `feat/warm-pool-provisioning-flow`
2. This PR: #2585 account claim flow cleanup.
3. Next: #2586 runtime assets claimed into the computer store.

## Size

- Local size-gate estimate: 1693 lines after exclusions.

## Verification

- `PATH="/Users/bill/.venvs/claw-interface/bin:$PATH" bash
scripts/verify-py.sh`
```

### 完整 PR Body

## Summary

- Split warm-pool account claim flow from legacy user materialization.
- Remove unused account adoption hooks.

## Stack

1. Base: #2584 / `feat/warm-pool-provisioning-flow`
2. This PR: #2585 account claim flow cleanup.
3. Next: #2586 runtime assets claimed into the computer store.

## Size

- Local size-gate estimate: 1693 lines after exclusions.

## Verification

- `PATH="/Users/bill/.venvs/claw-interface/bin:$PATH" bash scripts/verify-py.sh`



---

## feat(claw-interface): log agent pack deploy timings (#2595)

- **SHA**: 71b6d56a21058f0f0a5cec26b595d48425bda955
- **作者**: bill-srp (@bill-srp)
- **日期**: 2026-06-25T08:30:14Z
- **PR**: #2595
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/71b6d56a21058f0f0a5cec26b595d48425bda955

### 完整 Commit Message

```
feat(claw-interface): log agent pack deploy timings (#2595)

## Summary
- Rename the V2 pack deploy runtime script away from the official-only
name.
- Add stage timing logs for pack archive deploys, including bot id,
agent id, elapsed_ms, and total_ms.
- Forward runtime `[agent-pack-install]` lines through the
claw-interface logger so they are visible in service logs.

## Test plan
- [x] `bash scripts/verify-py.sh --ruff-only`
- [x] `/Users/bill/.venvs/claw-interface/bin/pytest -q
tests/unit/test_agent_install_service.py
tests/unit/test_pack_test_runtime_service.py`
- [x] `/Users/bill/.venvs/claw-interface/bin/lint-imports`
- [ ] `bash scripts/verify-py.sh` not fully runnable in this host
context: repo wrapper could not find `pyright` / `lint-imports`; direct
host pyright reports broad missing dependency imports such as `fastapi`,
`pytest`, and `favie_common`.
- [ ] `bash scripts/verify-changed.sh` degraded with backend tooling
missing and skipped py checks.
```

### 完整 PR Body

## Summary
- Rename the V2 pack deploy runtime script away from the official-only name.
- Add stage timing logs for pack archive deploys, including bot id, agent id, elapsed_ms, and total_ms.
- Forward runtime `[agent-pack-install]` lines through the claw-interface logger so they are visible in service logs.

## Test plan
- [x] `bash scripts/verify-py.sh --ruff-only`
- [x] `/Users/bill/.venvs/claw-interface/bin/pytest -q tests/unit/test_agent_install_service.py tests/unit/test_pack_test_runtime_service.py`
- [x] `/Users/bill/.venvs/claw-interface/bin/lint-imports`
- [ ] `bash scripts/verify-py.sh` not fully runnable in this host context: repo wrapper could not find `pyright` / `lint-imports`; direct host pyright reports broad missing dependency imports such as `fastapi`, `pytest`, and `favie_common`.
- [ ] `bash scripts/verify-changed.sh` degraded with backend tooling missing and skipped py checks.



---

## fix(new-chat): 暗色 agent 选中态适配与新任务输入框自动聚焦 (#2594)

- **SHA**: 8a9cc8396edd505342cdfb0202d109282e16d609
- **作者**: lynn Zhuang (@lynn-srp)
- **日期**: 2026-06-25T08:04:01Z
- **PR**: #2594
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/8a9cc8396edd505342cdfb0202d109282e16d609

### 完整 Commit Message

```
fix(new-chat): 暗色 agent 选中态适配与新任务输入框自动聚焦 (#2594)

## 背景 / 问题

新任务页（`/new-chat`）有两处体验问题：

1. **暗色模式下「选择 agent」选中态没适配**：暗色玻璃主题下，选中的 agent chip 仍是浅色白底 +
暗红字，和暗色界面格格不入。
2. **进入新任务后输入框未自动聚焦**：点击侧边栏「New Task」进入新任务页后，需要再次点击输入框才能开始输入。

## 改动

### 1. 暗色 agent 选中态适配（`AgentSelector.tsx`）
为选中 chip 的 active 分支补齐 `glass-dark:` 覆盖：`bg-red-500/15`（暗红底）+
`text-red-400`（亮红字）+ `border-red-500/70`（红描边）。

> 根因：active 分支此前只有 `glass:`（浅色玻璃）样式，而 `glass:` 选择器（`.liquid-glass-root
&`）在暗色玻璃（`.dark .liquid-glass-root`）下同样命中，导致白底泄漏到暗色模式。inactive 分支早已有
`glass-dark:` 覆盖，这次只是让 active 走同一套机制对齐。

### 2. 新任务输入框自动聚焦（`NewChatClient.tsx`）
用 `ref` + `useEffect`（以 URL 的 `agent_id` 为依赖）替代仅在挂载时生效的
`autoFocus`，覆盖全部进入路径：

- 顶部「New Task」从任意页进入 → 挂载即聚焦；
- 侧边栏按 agent 的「新任务」深链到 `/new-chat?agent_id=X`：当已处于 `/new-chat`
时属于**同路由切换**、组件不重新挂载，旧的 `autoFocus` 不会再次触发；以 `agent_id` 为 key
后，每次切换都会重新聚焦输入框。

### 3. 单元测试（`NewChatClient.unit.spec.tsx`）
新增两条用例：挂载即聚焦、按 agent 切换深链时重新聚焦。

## 验证

- 本地 `bash scripts/verify-web.sh`：`tsc` + `eslint` + 单元测试全绿（32 项）。
- 本地 mock 栈实测：暗色模式选中 chip 为暗红底（非白底）；侧边栏 agent「新任务」切换后，输入框自动聚焦、可直接输入。

## 影响范围

- 仅前端 `web/app` 新任务页（`/new-chat`），纯 UI/交互改动，无接口变更。
- 「选择 agent」模块在 agent 数 ≤ 1 时本就隐藏（既有逻辑，未改动）。

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
```

### 完整 PR Body

## 背景 / 问题

新任务页（`/new-chat`）有两处体验问题：

1. **暗色模式下「选择 agent」选中态没适配**：暗色玻璃主题下，选中的 agent chip 仍是浅色白底 + 暗红字，和暗色界面格格不入。
2. **进入新任务后输入框未自动聚焦**：点击侧边栏「New Task」进入新任务页后，需要再次点击输入框才能开始输入。

## 改动

### 1. 暗色 agent 选中态适配（`AgentSelector.tsx`）
为选中 chip 的 active 分支补齐 `glass-dark:` 覆盖：`bg-red-500/15`（暗红底）+ `text-red-400`（亮红字）+ `border-red-500/70`（红描边）。

> 根因：active 分支此前只有 `glass:`（浅色玻璃）样式，而 `glass:` 选择器（`.liquid-glass-root &`）在暗色玻璃（`.dark .liquid-glass-root`）下同样命中，导致白底泄漏到暗色模式。inactive 分支早已有 `glass-dark:` 覆盖，这次只是让 active 走同一套机制对齐。

### 2. 新任务输入框自动聚焦（`NewChatClient.tsx`）
用 `ref` + `useEffect`（以 URL 的 `agent_id` 为依赖）替代仅在挂载时生效的 `autoFocus`，覆盖全部进入路径：

- 顶部「New Task」从任意页进入 → 挂载即聚焦；
- 侧边栏按 agent 的「新任务」深链到 `/new-chat?agent_id=X`：当已处于 `/new-chat` 时属于**同路由切换**、组件不重新挂载，旧的 `autoFocus` 不会再次触发；以 `agent_id` 为 key 后，每次切换都会重新聚焦输入框。

### 3. 单元测试（`NewChatClient.unit.spec.tsx`）
新增两条用例：挂载即聚焦、按 agent 切换深链时重新聚焦。

## 验证

- 本地 `bash scripts/verify-web.sh`：`tsc` + `eslint` + 单元测试全绿（32 项）。
- 本地 mock 栈实测：暗色模式选中 chip 为暗红底（非白底）；侧边栏 agent「新任务」切换后，输入框自动聚焦、可直接输入。

## 影响范围

- 仅前端 `web/app` 新任务页（`/new-chat`），纯 UI/交互改动，无接口变更。
- 「选择 agent」模块在 agent 数 ≤ 1 时本就隐藏（既有逻辑，未改动）。



---

## refactor(web): remove legacy agent BFF routes (#2593)

- **SHA**: d3b368bc1fb7687a9bb07f751fa1e18b2db7c84e
- **作者**: bill-srp (@bill-srp)
- **日期**: 2026-06-25T07:16:25Z
- **PR**: #2593
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/d3b368bc1fb7687a9bb07f751fa1e18b2db7c84e

### 完整 Commit Message

```
refactor(web): remove legacy agent BFF routes (#2593)

## Summary
- remove legacy webapp agent BFF routes for
hire/fire/redeploy/reset-session
- send agent session reset directly through Mattermost `/new` from the
frontend
- keep agent install/update/uninstall on the computer-scoped frontend
services

## Tests
- `bash scripts/verify-web.sh web/app/src/hooks/useAgentActions.ts
web/app/src/lib/api/openclaw.ts
web/app/tests/unit/hooks/useAgentActions.unit.spec.ts
web/app/tests/unit/lib/api/openclaw-extras.unit.spec.ts`
- `bash scripts/verify-changed.sh` passed web checks; local backend
toolchain was missing `ruff`/`pyright`/`lint-imports`, and this PR has
no `services/` diff
```

### 完整 PR Body

## Summary
- remove legacy webapp agent BFF routes for hire/fire/redeploy/reset-session
- send agent session reset directly through Mattermost `/new` from the frontend
- keep agent install/update/uninstall on the computer-scoped frontend services

## Tests
- `bash scripts/verify-web.sh web/app/src/hooks/useAgentActions.ts web/app/src/lib/api/openclaw.ts web/app/tests/unit/hooks/useAgentActions.unit.spec.ts web/app/tests/unit/lib/api/openclaw-extras.unit.spec.ts`
- `bash scripts/verify-changed.sh` passed web checks; local backend toolchain was missing `ruff`/`pyright`/`lint-imports`, and this PR has no `services/` diff


