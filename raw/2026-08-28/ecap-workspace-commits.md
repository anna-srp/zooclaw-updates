# SerendipityOneInc/ecap-workspace — commits 2026-08-28

## fix(chat): clarify tool activity outcomes (#3540)

- **SHA**: `650f6bb55264b92f36017b195acb6fda354946a8`
- **作者**: rayrain-srp
- **日期**: 2026-08-28T11:19:24Z
- **PR**: #3540

### Commit Message

```
fix(chat): clarify tool activity outcomes (#3540)

## Summary

- Project an allowlisted activity action from structured tool args and
resolve accurate labels for image status/model queries, async waits,
subtask inspection, workspace saves, session-status inspection, and
failed commands.
- Make `tool_call_id` outcome merging monotonic (`running < done <
cancelled < error`) so late/replayed completion events cannot erase an
observed failure or cancellation; keep the first observed action stable.
- Preserve only allowlisted actions when replay snapshot input already
contains structured `tool_steps`, and carry them back into the shared
`ToolStep` model as forward-compatible serialization plumbing.
- Show failed commands with the correct failure label/icon while keeping
raw `resultPreview`-derived `errorMessage`/`summary`/unclassified
progress out of the timeline until a producer-sanitized failure field
exists.
- Label the existing wall-clock activity span as `Total elapsed` /
`总历时`, and preserve English fallback for locales without dedicated
activity copy.
- Keep polling collapse, cross-bubble causal grouping, and the
association of standalone V2 `tool_status` posts into public-share
replay out of scope until the upstream correlation contract tracked by
ECA-1410 exists.

Linear: ECA-1409

## Root cause

The activity UI selected copy from the tool name alone and did not
retain the safe `action` field from structured args. Its replay merge
guarded terminal states only against later non-terminal events, so a
later `completed` event could replace an earlier `failed` or `cancelled`
outcome for the same call. Where structured replay `tool_steps` are
present, snapshot normalization also dropped the new action field. The
group duration was already a wall-clock span, but the copy presented it
as an unlabeled duration. The V2 producer currently derives generic
failure fields from raw tool `resultPreview`, so those fields are not a
safe human-facing detail contract.

Current V2 public shares expose a separate upstream boundary: tool
activity is stored in standalone Mattermost `tool_status` posts, while
selected user/assistant posts do not contain persisted `tool_steps`.
ECA-1409 preserves `action` when structured steps are supplied, but does
not guess how to associate standalone tool posts with a selected
assistant turn. That association requires the causal correlation
contract tracked by ECA-1410.

## Test plan

- [x] `pnpm exec vitest run src/__tests__/tool-presentation.test.ts
src/__tests__/tool-group.test.tsx` (`@zooclaw/chat-ui`: 119 tests)
- [x] App adapter/MM/i18n targeted Vitest suites and the final
reordered/stable-action parser suite; `subagents({})` compatibility is
intentionally out of scope until upstream projects an allowlisted action
- [x] Replay snapshot conversion Vitest suite (15 tests) and
claw-interface replay creation suite (37 tests); these verify action
preservation when structured `tool_steps` are present
- [x] Failed-command result-preview safety regression in the ToolGroup
suite (54 tests after current `origin/main` merge)
- [x] `pnpm tsc` and `pnpm lint` in `web/packages/chat-ui`
- [x] `bash scripts/verify-changed.sh` after merging the latest
`origin/main` (Web guards/tsc/ESLint; Python
ruff/format/Pyright/import-linter)
- [x] Repository pre-push size gate and changed-surface verification
- [x] V2 staging E2E on `runtime=engine`: action-aware image/subagent
labels, failed-command presentation, monotonic error precedence under a
late completion, total-elapsed copy, English/Chinese rendering, and
fresh-page persisted rendering
- [x] Public-share boundary diagnostic: current V2 snapshots contain no
`tool_steps`; public replay E2E is therefore deferred to ECA-1410 rather
than implemented with adjacency/time/tool-name heuristics
```

### PR Body

## Summary

- Project an allowlisted activity action from structured tool args and resolve accurate labels for image status/model queries, async waits, subtask inspection, workspace saves, session-status inspection, and failed commands.
- Make `tool_call_id` outcome merging monotonic (`running < done < cancelled < error`) so late/replayed completion events cannot erase an observed failure or cancellation; keep the first observed action stable.
- Preserve only allowlisted actions when replay snapshot input already contains structured `tool_steps`, and carry them back into the shared `ToolStep` model as forward-compatible serialization plumbing.
- Show failed commands with the correct failure label/icon while keeping raw `resultPreview`-derived `errorMessage`/`summary`/unclassified progress out of the timeline until a producer-sanitized failure field exists.
- Label the existing wall-clock activity span as `Total elapsed` / `总历时`, and preserve English fallback for locales without dedicated activity copy.
- Keep polling collapse, cross-bubble causal grouping, and the association of standalone V2 `tool_status` posts into public-share replay out of scope until the upstream correlation contract tracked by ECA-1410 exists.

Linear: ECA-1409

## Root cause

The activity UI selected copy from the tool name alone and did not retain the safe `action` field from structured args. Its replay merge guarded terminal states only against later non-terminal events, so a later `completed` event could replace an earlier `failed` or `cancelled` outcome for the same call. Where structured replay `tool_steps` are present, snapshot normalization also dropped the new action field. The group duration was already a wall-clock span, but the copy presented it as an unlabeled duration. The V2 producer currently derives generic failure fields from raw tool `resultPreview`, so those fields are not a safe human-facing detail contract.

Current V2 public shares expose a separate upstream boundary: tool activity is stored in standalone Mattermost `tool_status` posts, while selected user/assistant posts do not contain persisted `tool_steps`. ECA-1409 preserves `action` when structured steps are supplied, but does not guess how to associate standalone tool posts with a selected assistant turn. That association requires the causal correlation contract tracked by ECA-1410.

## Test plan

- [x] `pnpm exec vitest run src/__tests__/tool-presentation.test.ts src/__tests__/tool-group.test.tsx` (`@zooclaw/chat-ui`: 119 tests)
- [x] App adapter/MM/i18n targeted Vitest suites and the final reordered/stable-action parser suite; `subagents({})` compatibility is intentionally out of scope until upstream projects an allowlisted action
- [x] Replay snapshot conversion Vitest suite (15 tests) and claw-interface replay creation suite (37 tests); these verify action preservation when structured `tool_steps` are present
- [x] Failed-command result-preview safety regression in the ToolGroup suite (54 tests after current `origin/main` merge)
- [x] `pnpm tsc` and `pnpm lint` in `web/packages/chat-ui`
- [x] `bash scripts/verify-changed.sh` after merging the latest `origin/main` (Web guards/tsc/ESLint; Python ruff/format/Pyright/import-linter)
- [x] Repository pre-push size gate and changed-surface verification
- [x] V2 staging E2E on `runtime=engine`: action-aware image/subagent labels, failed-command presentation, monotonic error precedence under a late completion, total-elapsed copy, English/Chinese rendering, and fresh-page persisted rendering
- [x] Public-share boundary diagnostic: current V2 snapshots contain no `tool_steps`; public replay E2E is therefore deferred to ECA-1410 rather than implemented with adjacency/time/tool-name heuristics


---

## feat(channels): add removal audit logging (#3576)

- **SHA**: `9db1c9f94a7b63abc943cdffec7e2dad4c08bfca`
- **作者**: sharplee-srp
- **日期**: 2026-08-28T11:08:37Z
- **PR**: #3576

### Commit Message

```
feat(channels): add removal audit logging (#3576)

## Summary

- capture client-side evidence for the two-step channel removal
interaction, including a per-action ID, trusted-event/input-method
signals, confirmation timing, WebDriver hint, and client version
- forward the optional audit payload through the Engine channel removal
request while keeping older clients compatible
- keep channel removal fail-open when client-side audit evidence
collection is unavailable
- emit structured `Requested` and `Completed` logs around ACS channel
deletion so successful removals can be correlated by `action_id`
- mark requests without audit data explicitly, which helps identify
old/cached clients or direct API calls

## Diagnostic interpretation

- trusted open + confirm events with a plausible confirmation interval
indicate a real browser interaction, but cannot distinguish an
intentional click from a user mistake
- `automation_hint=true`, untrusted events, or
`input_method=programmatic` are automation/script signals
- `interaction_start_present=false` or a near-zero confirmation interval
are signals for state/event reuse bugs
- `audit_present=false` identifies legacy/cached clients or requests
that bypass the new UI instrumentation

These fields are client-provided diagnostic signals, not authoritative
proof of user intent.

## Validation

- frontend targeted unit tests: 29 passed
- backend route/schema/service unit tests: 129 passed
- frontend TypeScript and ESLint: passed
- changed backend files: Ruff check/format and Pyright passed
- pre-commit frontend/Python hooks, import contracts, and Pyright:
passed
- `verify-changed.sh`: frontend surface passed; the backend
full-repository check is blocked by existing `main` baseline findings
outside this PR (72 Ruff findings, 20 pre-existing format findings, and
4 Pyright errors). The changed backend files pass the same scoped
checks.
```

### PR Body

## Summary

- capture client-side evidence for the two-step channel removal interaction, including a per-action ID, trusted-event/input-method signals, confirmation timing, WebDriver hint, and client version
- forward the optional audit payload through the Engine channel removal request while keeping older clients compatible
- keep channel removal fail-open when client-side audit evidence collection is unavailable
- emit structured `Requested` and `Completed` logs around ACS channel deletion so successful removals can be correlated by `action_id`
- mark requests without audit data explicitly, which helps identify old/cached clients or direct API calls

## Diagnostic interpretation

- trusted open + confirm events with a plausible confirmation interval indicate a real browser interaction, but cannot distinguish an intentional click from a user mistake
- `automation_hint=true`, untrusted events, or `input_method=programmatic` are automation/script signals
- `interaction_start_present=false` or a near-zero confirmation interval are signals for state/event reuse bugs
- `audit_present=false` identifies legacy/cached clients or requests that bypass the new UI instrumentation

These fields are client-provided diagnostic signals, not authoritative proof of user intent.

## Validation

- frontend targeted unit tests: 29 passed
- backend route/schema/service unit tests: 129 passed
- frontend TypeScript and ESLint: passed
- changed backend files: Ruff check/format and Pyright passed
- pre-commit frontend/Python hooks, import contracts, and Pyright: passed
- `verify-changed.sh`: frontend surface passed; the backend full-repository check is blocked by existing `main` baseline findings outside this PR (72 Ruff findings, 20 pre-existing format findings, and 4 Pyright errors). The changed backend files pass the same scoped checks.


---

## fix(agent-builder): 优化agent builder 项目列表交互 (#3572)

- **SHA**: `eea665533acbffb5379281550557ec659487e85b`
- **作者**: lynn Zhuang
- **日期**: 2026-08-28T10:52:06Z
- **PR**: #3572

### Commit Message

```
fix(agent-builder): 优化agent builder 项目列表交互 (#3572)

## 变更概要
- Agent Builder 项目列表支持点击整行进入编辑器，并将 More 保留为唯一显式行操作
- 优化列表列宽、行间距、骨架屏、Hover 表面、创建卡片箭头间距和项目标题样式
- 将“我的 Agent”范围计数优化为对比度更清晰的圆形徽标

## 问题原因
项目列表同时提供整行编辑入口以及 Edit、Chat 快捷按钮，导致操作列拥挤且表头难以稳定对齐。部分交互表面也存在视觉层级问题，包括过重的
Hover 填充、项目名称的链接下划线、对比度不足的矩形计数徽标，以及距离卡片边缘过近的箭头。

## 测试计划
- [x] `bash scripts/verify-web.sh <本次变更的 Agent Builder 文件>`
- [x] `bash scripts/verify-changed.sh`
- [x] 93 个 Agent Builder 定向单元测试
- [x] 在本地浏览器中手动验证整行点击、More 对齐、Hover 透明度、箭头边距、标题装饰和计数徽标尺寸
```

### PR Body

## 变更概要
- Agent Builder 项目列表支持点击整行进入编辑器，并将 More 保留为唯一显式行操作
- 优化列表列宽、行间距、骨架屏、Hover 表面、创建卡片箭头间距和项目标题样式
- 将“我的 Agent”范围计数优化为对比度更清晰的圆形徽标

## 问题原因
项目列表同时提供整行编辑入口以及 Edit、Chat 快捷按钮，导致操作列拥挤且表头难以稳定对齐。部分交互表面也存在视觉层级问题，包括过重的 Hover 填充、项目名称的链接下划线、对比度不足的矩形计数徽标，以及距离卡片边缘过近的箭头。

## 测试计划
- [x] `bash scripts/verify-web.sh <本次变更的 Agent Builder 文件>`
- [x] `bash scripts/verify-changed.sh`
- [x] 93 个 Agent Builder 定向单元测试
- [x] 在本地浏览器中手动验证整行点击、More 对齐、Hover 透明度、箭头边距、标题装饰和计数徽标尺寸


---

## docs(architecture): remove retired warm-pool references (#3575)

- **SHA**: `061a0fcee1163e07bf150dc905f12a0622449f8c`
- **作者**: tim-srp
- **日期**: 2026-08-28T10:53:17Z
- **PR**: #3575

### Commit Message

```
docs(architecture): remove retired warm-pool references (#3575)

<!-- PR 标题:type(scope): description -->

## Summary

Follow-up to #3559 (warm-pool code removal): clean the remaining
warm-pool
references out of the two living architecture documents and the
cron-docs
redirect pointer.

- `architecture.md` / `architecture.zh-CN.md`(同步修改,各 8 处):
- Mermaid 拓扑图:`user-interface` 节点职责与 `claw → ui` 调用边去掉 "warm
pool"(只改文案,边数量不变,`linkStyle` 索引不受影响)
  - 拓扑性质第 5 条:删除 "mint/reserve accounts (warm pool)" 描述
  - B 节仓库清单:`user-interface` 行删除 warm-pool admin API 描述
- C 节数据流:删除整条 "Warm-pool account reservation" bullet(引用的
`account_service_warm_pool.py` / `warm_pool_provisioner.py` 路径已随 #3559
删除)
  - C 节 Mongo 归属段落:去掉 "warm-pool record"
- E 节环境变量表:删除 `WARM_POOL_ACCOUNT_SERVICE_ADMIN_TOKEN` 行(setting
已删);`NEXT_PUBLIC_ACCOUNT_URL` 消费方列表去掉已删文件
- `docs/cron-triggers.md`(仓根 redirect 指针):描述枚举去掉 "warm-pool"

不改动带日期的历史文档(`docs/superpowers/plans/*`、
`services/claw-interface/docs/warm-pool-staging-e2e-2026-05-16.md`)——
它们是时间点的历史记录,保留作审计轨迹。

注:user-interface 侧的 warm-pool provider 端点由 PR-B 移除(见
`docs/superpowers/specs/2026-08-27-warm-pool-removal.md`,随 #3559 合入);
本文档按终态描述。

## Test plan

- [x] 纯文档改动;`grep -i 'warm.pool'` 在两份 architecture 文档中已无残留
- [x] Mermaid 边数量未变,`linkStyle 5/6/9` 索引保持有效

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

<!-- PR 标题:type(scope): description -->

## Summary

Follow-up to #3559 (warm-pool code removal): clean the remaining warm-pool
references out of the two living architecture documents and the cron-docs
redirect pointer.

- `architecture.md` / `architecture.zh-CN.md`(同步修改,各 8 处):
  - Mermaid 拓扑图:`user-interface` 节点职责与 `claw → ui` 调用边去掉 "warm pool"(只改文案,边数量不变,`linkStyle` 索引不受影响)
  - 拓扑性质第 5 条:删除 "mint/reserve accounts (warm pool)" 描述
  - B 节仓库清单:`user-interface` 行删除 warm-pool admin API 描述
  - C 节数据流:删除整条 "Warm-pool account reservation" bullet(引用的 `account_service_warm_pool.py` / `warm_pool_provisioner.py` 路径已随 #3559 删除)
  - C 节 Mongo 归属段落:去掉 "warm-pool record"
  - E 节环境变量表:删除 `WARM_POOL_ACCOUNT_SERVICE_ADMIN_TOKEN` 行(setting 已删);`NEXT_PUBLIC_ACCOUNT_URL` 消费方列表去掉已删文件
- `docs/cron-triggers.md`(仓根 redirect 指针):描述枚举去掉 "warm-pool"

不改动带日期的历史文档(`docs/superpowers/plans/*`、
`services/claw-interface/docs/warm-pool-staging-e2e-2026-05-16.md`)——
它们是时间点的历史记录,保留作审计轨迹。

注:user-interface 侧的 warm-pool provider 端点由 PR-B 移除(见
`docs/superpowers/specs/2026-08-27-warm-pool-removal.md`,随 #3559 合入);
本文档按终态描述。

## Test plan

- [x] 纯文档改动;`grep -i 'warm.pool'` 在两份 architecture 文档中已无残留
- [x] Mermaid 边数量未变,`linkStyle 5/6/9` 索引保持有效


---

## feat(chat): 统一 Agent 更新与会话侧边栏交互 (#3573)

- **SHA**: `72eea03af29bc49cbea7ac3d1ca624fffeafbc8d`
- **作者**: lynn Zhuang
- **日期**: 2026-08-28T09:55:55Z
- **PR**: #3573

### Commit Message

```
feat(chat): 统一 Agent 更新与会话侧边栏交互 (#3573)

## 概要

- 在 Chat Session 顶部增加单个 Agent 的 **Update** 操作，并与 Agent Marketplace
统一文案、按钮样式与更新状态
- 优化侧边栏 Agent 与 Session 交互：更新提示、选中态、Hover 背景、More 菜单、Rename 和 Archive
- 补齐会话归档的前端请求、后端 API、Mock 场景和多语言文案

## 交互细节

- Update 按钮使用统一的品牌色和更新图标，与相邻工具按钮保持 12px 间距、8px 圆角
- Agent 行的 Hover 背景覆盖完整区域，包括 New Task 铅笔按钮；离开 Hover 后收起操作按钮
- 每个 Session 都有 Hover 背景；选中的 Session 在 Hover 时继续保持选中背景，只显示 More 按钮
- Session 的 More 菜单仅保留 Rename 和 Archive，暂时移除 Pin
- Agent 有可用更新时，在头像显示提示点，并在 Chat Header、Marketplace 和侧边栏共享一致的更新进度

## 验证

- `bash scripts/verify-web.sh --no-test`
- 前端目标测试：16 个测试文件、452 个用例通过
- 前端完整测试：678 个测试文件、9308 个用例通过；依赖本地监听端口的 Mock Backend 测试在非沙箱环境 34/34 通过
- `bash scripts/verify-py.sh`
- 后端目标测试：87/87 通过
- 本地浏览器验证了 Update/工具按钮样式、按钮间距、Session 选中态与 Hover 状态

<img width="2588" height="2102" alt="update1"
src="https://github.com/user-attachments/assets/20135f54-78cf-41e8-8ba1-8aa80bf59893"
/>
<img width="2584" height="1990" alt="image"
src="https://github.com/user-attachments/assets/536c4b71-65f9-42ed-bd02-874c6c5cb0c5"
/>
```

### PR Body

## 概要

- 在 Chat Session 顶部增加单个 Agent 的 **Update** 操作，并与 Agent Marketplace 统一文案、按钮样式与更新状态
- 优化侧边栏 Agent 与 Session 交互：更新提示、选中态、Hover 背景、More 菜单、Rename 和 Archive
- 补齐会话归档的前端请求、后端 API、Mock 场景和多语言文案

## 交互细节

- Update 按钮使用统一的品牌色和更新图标，与相邻工具按钮保持 12px 间距、8px 圆角
- Agent 行的 Hover 背景覆盖完整区域，包括 New Task 铅笔按钮；离开 Hover 后收起操作按钮
- 每个 Session 都有 Hover 背景；选中的 Session 在 Hover 时继续保持选中背景，只显示 More 按钮
- Session 的 More 菜单仅保留 Rename 和 Archive，暂时移除 Pin
- Agent 有可用更新时，在头像显示提示点，并在 Chat Header、Marketplace 和侧边栏共享一致的更新进度

## 验证

- `bash scripts/verify-web.sh --no-test`
- 前端目标测试：16 个测试文件、452 个用例通过
- 前端完整测试：678 个测试文件、9308 个用例通过；依赖本地监听端口的 Mock Backend 测试在非沙箱环境 34/34 通过
- `bash scripts/verify-py.sh`
- 后端目标测试：87/87 通过
- 本地浏览器验证了 Update/工具按钮样式、按钮间距、Session 选中态与 Hover 状态

<img width="2588" height="2102" alt="update1" src="https://github.com/user-attachments/assets/20135f54-78cf-41e8-8ba1-8aa80bf59893" />
<img width="2584" height="1990" alt="image" src="https://github.com/user-attachments/assets/536c4b71-65f9-42ed-bd02-874c6c5cb0c5" />


---

## refactor(claw-interface): remove dead warm-pool provisioning (#3559)

- **SHA**: `8ecda433d814a9880a9991e4b7ba97045b01f61c`
- **作者**: tim-srp
- **日期**: 2026-08-28T09:56:52Z
- **PR**: #3559

### Commit Message

```
refactor(claw-interface): remove dead warm-pool provisioning (#3559)

## Problem

Warm-pool provisioning (pre-creating uid + FastClaw app + bot + billing
before registration so new users skip cold-start) is fully dead:

- #3532 made V2-eligible registration skip warm-pool claims and V1 app
creation (`AGENTS_V2_ENABLED` on; iOS v2 runtime shipped in #3526).
- The V1 FastClaw instances the pool provisioned against are gone
(node-pool scale-down was the trigger for #3532).
- Every remaining consumer already falls back to normal creation when
claim finds nothing — claim failures were swallowed to log lines.

The cron still provisions pool assets every 10 minutes that nothing can
ever claim. Removing the code is behavior-neutral for the app and stops
wasted provisioning.

## Fix

Remove all warm-pool code from `claw-interface` (PR-A of a two-repo
split):

**Deleted**
- `app/services/warm_pool/` (provisioner, runtime_adoption, user,
billing, app, account_service)
- `app/database/warm_pool_repo.py`, `warm_pool_assets_repo.py`
- `app/schema/warm_pool.py`, `warm_pool_assets.py`
- `app/routes/warm_pool.py` (`GET /admin/warm-pool/status`),
`app/routes/warm_pool_cron.py` (`POST /cron/warm-pool-provision`;
`pack-test-cleanup` was already retired in docs)
- `app/services/openclaw/warm_pool_bot_init.py`
- `bot_lifecycle.check_and_update_bot_ready_for_warm_pool`
(`get_first_asset_bot` kept — pack-test cleanup uses it)
- `mattermost_provisioner.provision_mattermost_for_warm_pool` (pack-test
variant kept)
- settings: `WARM_POOL_ACCOUNT_SERVICE_ADMIN_TOKEN`,
`WARM_POOL_ENABLED`, `WARM_POOL_TARGET_SIZE`,
`WARM_POOL_PROVISION_BATCH`

**Kept intentionally**
- `WARM_POOL_CRON_API_KEY` + `require_warm_pool_service_key`
(`X-Warm-Pool-Key` header): still guard live
`/admin/cron/cleanup-pack-test-runs` +
`/admin/cron/engine-sandbox-resource-class-reconcile`. Renaming =
ops-coordinated follow-up.
- `AccountMetadata.created_from="warm_pool"` value handling: stored
data, no logic.
- org-level `warm_pool_size` contract field (enterprise-admin renders
it) — separate cross-surface cleanup.

**Behavior impact**: none at runtime. Only visible change: schedulers
still calling `POST /cron/warm-pool-provision` get 404 → stop that
scheduler entry with this deploy.

**Docs/tests**: `docs/cron-triggers.md` updated (job dropped, scheduler
removal note). 7 warm-pool test files deleted (~68 cases);
`test_account_service.py` rewritten for claim-free register flow; stale
patches/imports removed from 4 other suites.

Follow-ups (not this PR): PR-B removes provider endpoints from
`user-interface` after this deploys; then data cleanup
(`ecap-warm-pool`, `ecap-warm-pool-assets`) and deferred contract-field
cleanup.

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## Problem

Warm-pool provisioning (pre-creating uid + FastClaw app + bot + billing before registration so new users skip cold-start) is fully dead:

- #3532 made V2-eligible registration skip warm-pool claims and V1 app creation (`AGENTS_V2_ENABLED` on; iOS v2 runtime shipped in #3526).
- The V1 FastClaw instances the pool provisioned against are gone (node-pool scale-down was the trigger for #3532).
- Every remaining consumer already falls back to normal creation when claim finds nothing — claim failures were swallowed to log lines.

The cron still provisions pool assets every 10 minutes that nothing can ever claim. Removing the code is behavior-neutral for the app and stops wasted provisioning.

## Fix

Remove all warm-pool code from `claw-interface` (PR-A of a two-repo split):

**Deleted**
- `app/services/warm_pool/` (provisioner, runtime_adoption, user, billing, app, account_service)
- `app/database/warm_pool_repo.py`, `warm_pool_assets_repo.py`
- `app/schema/warm_pool.py`, `warm_pool_assets.py`
- `app/routes/warm_pool.py` (`GET /admin/warm-pool/status`), `app/routes/warm_pool_cron.py` (`POST /cron/warm-pool-provision`; `pack-test-cleanup` was already retired in docs)
- `app/services/openclaw/warm_pool_bot_init.py`
- `bot_lifecycle.check_and_update_bot_ready_for_warm_pool` (`get_first_asset_bot` kept — pack-test cleanup uses it)
- `mattermost_provisioner.provision_mattermost_for_warm_pool` (pack-test variant kept)
- settings: `WARM_POOL_ACCOUNT_SERVICE_ADMIN_TOKEN`, `WARM_POOL_ENABLED`, `WARM_POOL_TARGET_SIZE`, `WARM_POOL_PROVISION_BATCH`

**Kept intentionally**
- `WARM_POOL_CRON_API_KEY` + `require_warm_pool_service_key` (`X-Warm-Pool-Key` header): still guard live `/admin/cron/cleanup-pack-test-runs` + `/admin/cron/engine-sandbox-resource-class-reconcile`. Renaming = ops-coordinated follow-up.
- `AccountMetadata.created_from="warm_pool"` value handling: stored data, no logic.
- org-level `warm_pool_size` contract field (enterprise-admin renders it) — separate cross-surface cleanup.

**Behavior impact**: none at runtime. Only visible change: schedulers still calling `POST /cron/warm-pool-provision` get 404 → stop that scheduler entry with this deploy.

**Docs/tests**: `docs/cron-triggers.md` updated (job dropped, scheduler removal note). 7 warm-pool test files deleted (~68 cases); `test_account_service.py` rewritten for claim-free register flow; stale patches/imports removed from 4 other suites.

Follow-ups (not this PR): PR-B removes provider endpoints from `user-interface` after this deploys; then data cleanup (`ecap-warm-pool`, `ecap-warm-pool-assets`) and deferred contract-field cleanup.


---

## chore(chat): remove version upgrade widget (#3569)

- **SHA**: `ae418d93f368bce6476fe17cc88adc351fb7ac11`
- **作者**: sharplee-srp
- **日期**: 2026-08-28T09:09:31Z
- **PR**: #3569

### Commit Message

```
chore(chat): remove version upgrade widget (#3569)

## Summary

- remove the chat version-upgrade widget and its header wiring
- delete the widget-only translations, theme variables, and unit test
- keep shared version compatibility checks used by settings and
navigation intact

## Test plan

- [x] `bash scripts/verify-web.sh <changed chat paths and tests>`
- [x] `pnpm exec prettier --check src/app/globals.css src/locales/en.ts
src/locales/zh.ts`
- [x] verify no widget identifiers, translation keys, or theme variables
remain
```

### PR Body

## Summary

- remove the chat version-upgrade widget and its header wiring
- delete the widget-only translations, theme variables, and unit test
- keep shared version compatibility checks used by settings and navigation intact

## Test plan

- [x] `bash scripts/verify-web.sh <changed chat paths and tests>`
- [x] `pnpm exec prettier --check src/app/globals.css src/locales/en.ts src/locales/zh.ts`
- [x] verify no widget identifiers, translation keys, or theme variables remain


---

## fix(agent-builder): prevent duplicate preview refresh runs (#3571)

- **SHA**: `7ead01dbca73fe752da3965bd8385eee6811ddf1`
- **作者**: kaka-srp
- **日期**: 2026-08-28T08:37:22Z
- **PR**: #3571

### Commit Message

```
fix(agent-builder): prevent duplicate preview refresh runs (#3571)

## Summary
- Disable **Refresh preview** while an Agent Builder Preview is already
packaging or deploying.
- Reject duplicate backend test-iteration creation for both legacy and
Engine v2 runtimes.
- Recover v2 Preview creation that remains in `packaging` or
`deploying_test` without a TestRun for 30 minutes, so the user can retry
instead of requiring manual data repair.

## Root cause
The frontend enabled Refresh again as soon as the initiating `202`
request completed, even though the persisted Project was still packaging
or deploying. The backend also exempted Engine v2 from its in-progress
guard, so a repeated click created a second iteration and superseded a
TestRun that could still be finalizing.

Blocking duplicate creation alone would strand a Project if a worker
stopped before linking its TestRun. State polling now converges that
stale, unowned creation to a failed Project and iteration after the
existing 30-minute package-operation TTL.

## Test plan
- [x] Backend start-iteration tests: 4 passed.
- [x] Backend stale-creation recovery tests: 4 passed, covering both
`packaging` and `deploying_test`.
- [x] Frontend Preview workspace/state tests: 8 passed.
- [x] Targeted Ruff, Ruff format, Pyright, and ESLint checks passed.
- [ ] Full local suites were not run; CI is authoritative.

## Known follow-up
- Capacity-reservation cleanup behavior for a duplicate request that
encounters a `recovery_required` slot is intentionally unchanged in this
PR.
```

### PR Body

## Summary
- Disable **Refresh preview** while an Agent Builder Preview is already packaging or deploying.
- Reject duplicate backend test-iteration creation for both legacy and Engine v2 runtimes.
- Recover v2 Preview creation that remains in `packaging` or `deploying_test` without a TestRun for 30 minutes, so the user can retry instead of requiring manual data repair.

## Root cause
The frontend enabled Refresh again as soon as the initiating `202` request completed, even though the persisted Project was still packaging or deploying. The backend also exempted Engine v2 from its in-progress guard, so a repeated click created a second iteration and superseded a TestRun that could still be finalizing.

Blocking duplicate creation alone would strand a Project if a worker stopped before linking its TestRun. State polling now converges that stale, unowned creation to a failed Project and iteration after the existing 30-minute package-operation TTL.

## Test plan
- [x] Backend start-iteration tests: 4 passed.
- [x] Backend stale-creation recovery tests: 4 passed, covering both `packaging` and `deploying_test`.
- [x] Frontend Preview workspace/state tests: 8 passed.
- [x] Targeted Ruff, Ruff format, Pyright, and ESLint checks passed.
- [ ] Full local suites were not run; CI is authoritative.

## Known follow-up
- Capacity-reservation cleanup behavior for a duplicate request that encounters a `recovery_required` slot is intentionally unchanged in this PR.


---

## fix(agent-builder): retry install while environment builds (#3570)

- **SHA**: `aa335949c4b804f0d0234df8b9884a5c5d49d667`
- **作者**: kaka-srp
- **日期**: 2026-08-28T06:45:55Z
- **PR**: #3570

### Commit Message

```
fix(agent-builder): retry install while environment builds (#3570)

## Summary

- retry Agent Builder Only me installation while the published Pack
environment is still building
- scope retries to agent.environment_not_ready and preserve all other
failures
- bound retries to 90 seconds with exponential delays

## Verification

- agent-install unit tests: 24 passed
- agent-builder publish unit tests: 17 passed
- Prettier check passed for all four changed files
- Full local frontend gate skipped at the user's request; CI remains
authoritative

## Risk

Low. The retry is limited to one domain error and the backend reclaims
the same failed workspace with its existing idempotency key.
```

### PR Body

## Summary

- retry Agent Builder Only me installation while the published Pack environment is still building
- scope retries to agent.environment_not_ready and preserve all other failures
- bound retries to 90 seconds with exponential delays

## Verification

- agent-install unit tests: 24 passed
- agent-builder publish unit tests: 17 passed
- Prettier check passed for all four changed files
- Full local frontend gate skipped at the user's request; CI remains authoritative

## Risk

Low. The retry is limited to one domain error and the backend reclaims the same failed workspace with its existing idempotency key.


---

## feat(agent-builder): agent builder 和 marketplace 优化 (#3554)

- **SHA**: `4e00d51e0d5ee9e7c68a72564d8e06d3c4d613dc`
- **作者**: lynn Zhuang
- **日期**: 2026-08-28T03:48:39Z
- **PR**: #3554

### Commit Message

```
feat(agent-builder): agent builder 和 marketplace 优化 (#3554)

## 改动概要

- 将 Agent Builder 中的构建会话重新定义为项目，并把“从空白创建”和“从现有 Agent 创建”两种入口直接放到 Builder
首页。
- 新增 My Agent 页面，分别展示 Owned by me 和 Shared with me；Owned by me
包含所有已发布范围的 Agent，未发布的草稿仍仅作为项目保留在 Agent Builder 首页。
- Agent Marketplace 仅保留公开 Agent 市场，并抽取 Marketplace 与 My Agent 共用的目录展示能力。
- 按照 ZooWork Design System 统一创建卡片、状态标签、详情字段、复制操作和弹窗操作区的样式。

## 测试计划

- [x] `bash scripts/verify-changed.sh`
- [x] 相关 Web 单元测试：36 个文件，473 项测试通过
- [x] Agent Builder / My Agent 定向单元测试：2 个文件，41 项测试通过
- [x] `pnpm --filter @zooclaw/design-system test`：53 个文件，306 项测试通过
- [x] `pnpm --filter @zooclaw/chat-ui test`：33 个文件，441 项测试通过
- [x] 在本地 Mock 预览中手动验证 Agent Builder、My Agent 的 Tab 与卡片、Agent 详情弹窗和
Agent Marketplace

## 备注

- 本次仅涉及前端与本地 Mock 预览，不修改后端 API 契约。
- 验证前已将分支 rebase 到最新的 `origin/main`。
- 按仓库排除规则统计，本次完整迁移共 3,934 行；Builder 路由、My Agent 范围和公开 Marketplace
目录保持在同一个 PR 中，避免出现功能不一致的中间状态。
<img width="2572" height="1986" alt="image"
src="https://github.com/user-attachments/assets/770ddb54-8732-426f-a5e7-f76675a49b10"
/>
<img width="2574" height="1998" alt="image"
src="https://github.com/user-attachments/assets/52db2006-40f6-4cbc-91ff-64f41429376f"
/>
<img width="2568" height="1998" alt="image"
src="https://github.com/user-attachments/assets/6d7a50d2-c283-4855-9870-17231a801491"
/>
![Uploading image.png…]()

![Uploading 3eb44054-4528-4cf9-8afe-945114c5d7d8.jpeg…]()
```

### PR Body

## 改动概要

- 将 Agent Builder 中的构建会话重新定义为项目，并把“从空白创建”和“从现有 Agent 创建”两种入口直接放到 Builder 首页。
- 新增 My Agent 页面，分别展示 Owned by me 和 Shared with me；Owned by me 包含所有已发布范围的 Agent，未发布的草稿仍仅作为项目保留在 Agent Builder 首页。
- Agent Marketplace 仅保留公开 Agent 市场，并抽取 Marketplace 与 My Agent 共用的目录展示能力。
- 按照 ZooWork Design System 统一创建卡片、状态标签、详情字段、复制操作和弹窗操作区的样式。

## 测试计划

- [x] `bash scripts/verify-changed.sh`
- [x] 相关 Web 单元测试：36 个文件，473 项测试通过
- [x] Agent Builder / My Agent 定向单元测试：2 个文件，41 项测试通过
- [x] `pnpm --filter @zooclaw/design-system test`：53 个文件，306 项测试通过
- [x] `pnpm --filter @zooclaw/chat-ui test`：33 个文件，441 项测试通过
- [x] 在本地 Mock 预览中手动验证 Agent Builder、My Agent 的 Tab 与卡片、Agent 详情弹窗和 Agent Marketplace

## 备注

- 本次仅涉及前端与本地 Mock 预览，不修改后端 API 契约。
- 验证前已将分支 rebase 到最新的 `origin/main`。
- 按仓库排除规则统计，本次完整迁移共 3,934 行；Builder 路由、My Agent 范围和公开 Marketplace 目录保持在同一个 PR 中，避免出现功能不一致的中间状态。
<img width="2572" height="1986" alt="image" src="https://github.com/user-attachments/assets/770ddb54-8732-426f-a5e7-f76675a49b10" />
<img width="2574" height="1998" alt="image" src="https://github.com/user-attachments/assets/52db2006-40f6-4cbc-91ff-64f41429376f" />
<img width="2568" height="1998" alt="image" src="https://github.com/user-attachments/assets/6d7a50d2-c283-4855-9870-17231a801491" />
![Uploading image.png…]()

![Uploading 3eb44054-4528-4cf9-8afe-945114c5d7d8.jpeg…]()


---

## feat(marketing): refresh About page content and layout (#3556)

- **SHA**: `a987d20f2f98904c7821a4cbe0d526f3b614c6a4`
- **作者**: shana-srp
- **日期**: 2026-08-28T02:38:49Z
- **PR**: #3556

### Commit Message

```
feat(marketing): refresh About page content and layout (#3556)

## Linear

N/A

## Summary
- refresh the localized About page content and typography across all
supported languages
- replace the three-platform presentation with a single responsive
ZooWork story section and brand treatment
- align the About page CTA behavior with the shared marketing header
actions
- add focused unit coverage for localized content, CTA behavior, and the
ZooWork story section

## Test plan
- [x] `bash scripts/verify-web.sh`
- [x] `bash scripts/verify-local.sh`
- [x] desktop and mobile About page visual checks in English and Chinese
- [x] verified no horizontal overflow across supported locales

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Linear

N/A

## Summary
- refresh the localized About page content and typography across all supported languages
- replace the three-platform presentation with a single responsive ZooWork story section and brand treatment
- align the About page CTA behavior with the shared marketing header actions
- add focused unit coverage for localized content, CTA behavior, and the ZooWork story section

## Test plan
- [x] `bash scripts/verify-web.sh`
- [x] `bash scripts/verify-local.sh`
- [x] desktop and mobile About page visual checks in English and Chinese
- [x] verified no horizontal overflow across supported locales


---
