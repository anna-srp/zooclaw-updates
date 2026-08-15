# SerendipityOneInc/ecap-workspace commits — 2026-08-14

## fix(agent-builder): 优化首页响应式布局与交互 (#3390)

- sha: `0e8069c1acaf9ecdd68b3bc3fc015764ff8148c6`
- author: lynn Zhuang
- date: 2026-08-14T11:26:55Z
- PR: 3390

### Commit message

```
fix(agent-builder): 优化首页响应式布局与交互 (#3390)

## 概要

- 将 Agent Builder 首页内容区居中，最大阅读宽度设为 896px，并按不同视口逐级调整页面边距。
- 使用容器断点优化列表响应式布局：窄屏将更新时间和发布状态收进 Agent 信息区，宽屏保持四列展示，操作按钮始终可见且不产生横向滚动。
- 简化列表排版：移除描述文字，Agent 名称改为常规字重；表头统一左对齐并降低视觉强调；同时优化行距、列间距和 hover 反馈。
- 优化 Edit、已发布 Agent 的 Chat 及 More 操作：使用紧凑的圆角矩形，窄屏只显示图标，宽屏显示文字，Edit 与
Chat 的间距调整为 12px。
- 简化 Rename 弹窗：移除重复展示的当前名称，只保留预填输入框；输入框和按钮统一为圆角矩形；Rename 菜单项的高亮仅在 Agent
Builder 页面内生效。
- 本 PR 严格限定在 Agent Builder 首页，不包含共享 Chat UI、Design System 包、Create
dialog 以及登录/认证改动。Preview composer 共享逻辑已通过 #3374 合入 `main`，本 PR 不重复提交。

## 根因

原 Agent Builder
首页使用全宽固定列布局，并直接继承共享组件的通用操作样式。宽屏下列表被过度拉伸，影响可读性；窄屏下更新时间、状态和右侧操作会争抢空间。Rename
弹窗同时重复展示当前名称，默认圆角和 hover 样式也让部分控件呈现胶囊感、交互反馈不够清晰。

## 测试计划

- [x] `bash scripts/verify-web.sh
'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderHome.tsx'
web/app/tests/unit/app/agent-builder-entry.unit.spec.tsx
web/app/tests/unit/app/agent-builder-production-home.unit.spec.tsx`
- [x] 相关 Vitest：2 个测试文件、84 个测试全部通过
- [x] `bash scripts/verify-changed.sh`
- [x] `bash scripts/check-pr-size.sh`（792 / 3000 行）
- [x] 范围审计确认没有 Chat UI、Design System、Create dialog 或登录/认证文件
```

### PR body

## 概要

- 将 Agent Builder 首页内容区居中，最大阅读宽度设为 896px，并按不同视口逐级调整页面边距。
- 使用容器断点优化列表响应式布局：窄屏将更新时间和发布状态收进 Agent 信息区，宽屏保持四列展示，操作按钮始终可见且不产生横向滚动。
- 简化列表排版：移除描述文字，Agent 名称改为常规字重；表头统一左对齐并降低视觉强调；同时优化行距、列间距和 hover 反馈。
- 优化 Edit、已发布 Agent 的 Chat 及 More 操作：使用紧凑的圆角矩形，窄屏只显示图标，宽屏显示文字，Edit 与 Chat 的间距调整为 12px。
- 简化 Rename 弹窗：移除重复展示的当前名称，只保留预填输入框；输入框和按钮统一为圆角矩形；Rename 菜单项的高亮仅在 Agent Builder 页面内生效。
- 本 PR 严格限定在 Agent Builder 首页，不包含共享 Chat UI、Design System 包、Create dialog 以及登录/认证改动。Preview composer 共享逻辑已通过 #3374 合入 `main`，本 PR 不重复提交。

## 根因

原 Agent Builder 首页使用全宽固定列布局，并直接继承共享组件的通用操作样式。宽屏下列表被过度拉伸，影响可读性；窄屏下更新时间、状态和右侧操作会争抢空间。Rename 弹窗同时重复展示当前名称，默认圆角和 hover 样式也让部分控件呈现胶囊感、交互反馈不够清晰。

## 测试计划

- [x] `bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderHome.tsx' web/app/tests/unit/app/agent-builder-entry.unit.spec.tsx web/app/tests/unit/app/agent-builder-production-home.unit.spec.tsx`
- [x] 相关 Vitest：2 个测试文件、84 个测试全部通过
- [x] `bash scripts/verify-changed.sh`
- [x] `bash scripts/check-pr-size.sh`（792 / 3000 行）
- [x] 范围审计确认没有 Chat UI、Design System、Create dialog 或登录/认证文件


## fix(org): accept nested team models for invite handoff (#3391)

- sha: `c9555e9c14c74ddaf6122047fd1cf3be9f91f376`
- author: kaka-srp
- date: 2026-08-14T11:25:16Z
- PR: 3391

### Commit message

```
fix(org): accept nested team models for invite handoff (#3391)

## Summary
- Accept the production Billing Gateway team response shape when
validating enterprise invitation handoffs.
- Add a regression test using the nested team_info model allowlist
returned in production.

## Root cause
The handoff readiness check only read models from team.models. Billing
Gateway returns production team models under team.team_info.models, so a
fully subscribed enterprise with an active wallet was incorrectly
rejected as billing-not-ready.

## Test plan
- [x] pytest tests/unit/test_enterprise_invite_handoff.py -q (19 passed)
- [x] bash scripts/verify-py.sh
```

### PR body

## Summary
- Accept the production Billing Gateway team response shape when validating enterprise invitation handoffs.
- Add a regression test using the nested team_info model allowlist returned in production.

## Root cause
The handoff readiness check only read models from team.models. Billing Gateway returns production team models under team.team_info.models, so a fully subscribed enterprise with an active wallet was incorrectly rejected as billing-not-ready.

## Test plan
- [x] pytest tests/unit/test_enterprise_invite_handoff.py -q (19 passed)
- [x] bash scripts/verify-py.sh


## fix(settings): clarify API key descriptions (#3394)

- sha: `9818454213926b7e7c46182ef345f3b9c351cd6f`
- author: finn-srp
- date: 2026-08-14T10:48:13Z
- PR: 3394

### Commit message

```
fix(settings): clarify API key descriptions (#3394)

## 背景

设置页 API Keys tab 的副标题原文是 "Create org service tokens for scripts and
external services that need to call your organization."：页面标题叫 API
Keys，正文却引入第二个术语「org service token」，且 "call your organization / 调用你的组织"
语义不明。内部反馈看不懂这句话在说什么。

## 改动

仅改 `en.ts` / `zh.ts` 中 `apiKeys.description` 与
`apiKeys.emptyDescription` 四条字符串：

| 位置 | 旧 | 新 |
|---|---|---|
| 副标题 EN | Create org service tokens for scripts and external services
that need to call your organization. | API keys let your scripts and
backend services call the ZooClaw API, with full access to this
organization's agents. |
| 副标题 ZH | 为脚本和外部服务创建组织服务令牌，以便调用你的组织。 | API 密钥供你的脚本和后端服务调用 ZooClaw
API，对本组织的全部 Agent 有完整访问权限。 |
| 空状态 EN | API keys are org service tokens for automations and
integrations. Create one when a script needs access. | Create one when a
script or external service needs to call this organization's agents. |
| 空状态 ZH | API 密钥是供自动化流程和集成使用的组织服务令牌。脚本需要访问时即可创建。 | 当脚本或外部服务需要调用本组织的
Agent 时，创建一个即可。 |

写法对齐主流产品的 API key 页面文案（Stripe / Anthropic / Cloudflare / Manus 调研）：

- **只用一个术语**：全文只说 API key（ZH：API 密钥），不再出现「服务令牌」。
- **用途优先**：一句话说清「谁用它访问什么」（scripts/backend services → ZooClaw API）。
- **权限直接披露**：我们的组织级 key 无 scope、对组织内全部 Agent 完整读写，参照 Stripe 对
unrestricted secret key 的写法直说，而非回避。
- 空状态正文不再复读上方标题 "No API keys yet"。

## 影响面

- 其余 8 个 locale（ar/de/es/fr/it/ja/ko/pt）没有 `apiKeys`
块，服务端字典深合并会自动回落到新英文，无需改动。
- 与 #3371（API key 管理页 redesign）无冲突：本分支基于最新 main，两句旧文案在 redesign
后原样保留，此处仅替换字符串。

## 验证

- `tsc` 单文件编译通过。
- 本地 `dev:staging` 起服渲染过目。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: wangfulong <wfllike@gmail.com>
Co-authored-by: Claude Opus 5 <noreply@anthropic.com>
```

### PR body

## 背景

设置页 API Keys tab 的副标题原文是 "Create org service tokens for scripts and external services that need to call your organization."：页面标题叫 API Keys，正文却引入第二个术语「org service token」，且 "call your organization / 调用你的组织" 语义不明。内部反馈看不懂这句话在说什么。

## 改动

仅改 `en.ts` / `zh.ts` 中 `apiKeys.description` 与 `apiKeys.emptyDescription` 四条字符串：

| 位置 | 旧 | 新 |
|---|---|---|
| 副标题 EN | Create org service tokens for scripts and external services that need to call your organization. | API keys let your scripts and backend services call the ZooClaw API, with full access to this organization's agents. |
| 副标题 ZH | 为脚本和外部服务创建组织服务令牌，以便调用你的组织。 | API 密钥供你的脚本和后端服务调用 ZooClaw API，对本组织的全部 Agent 有完整访问权限。 |
| 空状态 EN | API keys are org service tokens for automations and integrations. Create one when a script needs access. | Create one when a script or external service needs to call this organization's agents. |
| 空状态 ZH | API 密钥是供自动化流程和集成使用的组织服务令牌。脚本需要访问时即可创建。 | 当脚本或外部服务需要调用本组织的 Agent 时，创建一个即可。 |

写法对齐主流产品的 API key 页面文案（Stripe / Anthropic / Cloudflare / Manus 调研）：

- **只用一个术语**：全文只说 API key（ZH：API 密钥），不再出现「服务令牌」。
- **用途优先**：一句话说清「谁用它访问什么」（scripts/backend services → ZooClaw API）。
- **权限直接披露**：我们的组织级 key 无 scope、对组织内全部 Agent 完整读写，参照 Stripe 对 unrestricted secret key 的写法直说，而非回避。
- 空状态正文不再复读上方标题 "No API keys yet"。

## 影响面

- 其余 8 个 locale（ar/de/es/fr/it/ja/ko/pt）没有 `apiKeys` 块，服务端字典深合并会自动回落到新英文，无需改动。
- 与 #3371（API key 管理页 redesign）无冲突：本分支基于最新 main，两句旧文案在 redesign 后原样保留，此处仅替换字符串。

## 验证

- `tsc` 单文件编译通过。
- 本地 `dev:staging` 起服渲染过目。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## fix(agent-builder): align composer gutters (#3389)

- sha: `3651d484782716c82589d0d51e7abacb5cad717b`
- author: lynn Zhuang
- date: 2026-08-14T10:06:50Z
- PR: 3389

### Commit message

```
fix(agent-builder): align composer gutters (#3389)

## Summary
- Align the Agent Builder and Preview composer side and bottom gutters
at 16px.
- Keep the regular chat composer defaults unchanged by threading scoped
layout classes through the shared composer wrappers.

## Root cause
Agent Builder reused the regular chat composer's default `px-6` content
gutter and `pb-2` root gutter. When Preview opened beside Builder, the
two composer cards had mismatched side and bottom spacing.

## Test plan
- [x] `pnpm exec vitest run --config ./vitest.config.mts
--passWithNoTests agent-builder GenClawInput OpenClawChatSurface
UnifiedChatComposer` — 37 files / 524 tests passed
- [x] Pre-push changed-surface verification — governance guards,
TypeScript, and ESLint passed
- [x] Local mock-stack visual verification — Builder and Preview
measured 16px on the left, right, and bottom
```

### PR body

## Summary
- Align the Agent Builder and Preview composer side and bottom gutters at 16px.
- Keep the regular chat composer defaults unchanged by threading scoped layout classes through the shared composer wrappers.

## Root cause
Agent Builder reused the regular chat composer's default `px-6` content gutter and `pb-2` root gutter. When Preview opened beside Builder, the two composer cards had mismatched side and bottom spacing.

## Test plan
- [x] `pnpm exec vitest run --config ./vitest.config.mts --passWithNoTests agent-builder GenClawInput OpenClawChatSurface UnifiedChatComposer` — 37 files / 524 tests passed
- [x] Pre-push changed-surface verification — governance guards, TypeScript, and ESLint passed
- [x] Local mock-stack visual verification — Builder and Preview measured 16px on the left, right, and bottom


## fix(agent-builder): recover preview runtime slots under CSFLE (#3388)

- sha: `ee46f412276f546cc8d233adb2458e0e806b7b91`
- author: kaka-srp
- date: 2026-08-14T09:45:07Z
- PR: 3388

### Commit message

```
fix(agent-builder): recover preview runtime slots under CSFLE (#3388)

## Summary

- replace the Agent Builder package-to-turn aggregation-pipeline update
with a CSFLE-compatible classic update
- preserve the package/turn handoff with exact activity, post, and fence
CAS guards
- skip the transfer path when no Builder turn exists and retry once when
a turn races with cooldown
- add regression coverage for the production-incompatible update shape
and both recovery paths

## Root cause

Staging Mongo's CSFLE analyzer rejects aggregation-pipeline updates on
`ecap-agent-builder-runtime-slots`. `transfer_package_to_active_turn`
used a pipeline even when no active turn matched, so package-test
completion and the recovery cron failed before the slot could enter
cooldown. Expired slots remained in `recovery_required`, and later
requests received the misleading `agent_builder.project_busy` response
indefinitely.

The affected reporter's stale slot was separately released with exact
project/activity/fence preconditions after confirming that the Project
had no workspace operation, TestRun, or active Builder turn.

## Test plan

- [x] `pytest tests/unit/test_agent_builder_runtime_slot_repo.py
tests/unit/test_agent_builder_runtime_capacity_service.py
tests/unit/test_agent_builder_runtime_recovery_service.py -q` — 26
passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
```

### PR body

## Summary

- replace the Agent Builder package-to-turn aggregation-pipeline update with a CSFLE-compatible classic update
- preserve the package/turn handoff with exact activity, post, and fence CAS guards
- skip the transfer path when no Builder turn exists and retry once when a turn races with cooldown
- add regression coverage for the production-incompatible update shape and both recovery paths

## Root cause

Staging Mongo's CSFLE analyzer rejects aggregation-pipeline updates on `ecap-agent-builder-runtime-slots`. `transfer_package_to_active_turn` used a pipeline even when no active turn matched, so package-test completion and the recovery cron failed before the slot could enter cooldown. Expired slots remained in `recovery_required`, and later requests received the misleading `agent_builder.project_busy` response indefinitely.

The affected reporter's stale slot was separately released with exact project/activity/fence preconditions after confirming that the Project had no workspace operation, TestRun, or active Builder turn.

## Test plan

- [x] `pytest tests/unit/test_agent_builder_runtime_slot_repo.py tests/unit/test_agent_builder_runtime_capacity_service.py tests/unit/test_agent_builder_runtime_recovery_service.py -q` — 26 passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`


## feat(settings): redesign API key management (#3371)

- sha: `f57c3cf7beb48255e32ff10a4553986a1c9661c9`
- author: lynn Zhuang
- date: 2026-08-14T09:38:33Z
- PR: 3371

### Commit message

```
feat(settings): redesign API key management (#3371)

## Linear

N/A

## Summary

- Redesign **Claw Settings → API Keys** as a ZooClaw Design System
security ledger with distinct loading, empty, populated, and error
states.
- Keep a single **Create API Key** action in the correct location and
add consistent create, one-time reveal, rotate, and revoke dialogs.
- Keep plaintext secrets only in controller memory, add local mock
service-token coverage, and refine shared dialog/control behavior needed
for safe state handoffs.

## Test plan

- [x] Web app governance guards, TypeScript, and scoped ESLint via
`scripts/verify-web.sh --no-test`
- [x] Web app focused Vitest: 4 files / 49 tests
- [x] ZooClaw Design System focused Vitest: 4 files / 36 tests
- [x] ZooClaw Design System TypeScript and ESLint
- [x] Changed-surface verification via `scripts/verify-changed.sh`
- [x] Diff whitespace check and PR size guard (1,539 / 3,000 effective
lines)

## Security notes

- The complete API key is held only in local controller state for the
reveal dialog and is cleared when the dialog closes.
- The complete key is not written to React Query cache, URL state,
browser storage, or logs.
- A successful create/rotate response that omits its one-time secret is
presented as a terminal partial-success state, preventing accidental
duplicate creation or rotation retries.
- Dialog handoff visibility is latched through predecessor exit
animations, preventing a fast-close flash of the completed Create/Rotate
dialog.
```

### PR body

## Linear

N/A

## Summary

- Redesign **Claw Settings → API Keys** as a ZooClaw Design System security ledger with distinct loading, empty, populated, and error states.
- Keep a single **Create API Key** action in the correct location and add consistent create, one-time reveal, rotate, and revoke dialogs.
- Keep plaintext secrets only in controller memory, add local mock service-token coverage, and refine shared dialog/control behavior needed for safe state handoffs.

## Test plan

- [x] Web app governance guards, TypeScript, and scoped ESLint via `scripts/verify-web.sh --no-test`
- [x] Web app focused Vitest: 4 files / 49 tests
- [x] ZooClaw Design System focused Vitest: 4 files / 36 tests
- [x] ZooClaw Design System TypeScript and ESLint
- [x] Changed-surface verification via `scripts/verify-changed.sh`
- [x] Diff whitespace check and PR size guard (1,539 / 3,000 effective lines)

## Security notes

- The complete API key is held only in local controller state for the reveal dialog and is cleared when the dialog closes.
- The complete key is not written to React Query cache, URL state, browser storage, or logs.
- A successful create/rotate response that omits its one-time secret is presented as a terminal partial-success state, preventing accidental duplicate creation or rotation retries.
- Dialog handoff visibility is latched through predecessor exit animations, preventing a fast-close flash of the completed Create/Rotate dialog.


## fix(claw): proxy agent action ownership checks (#3387)

- sha: `7f2e12d8bd9be4379dc3ec6b8eec1cf41be7ca5a`
- author: bill-srp
- date: 2026-08-14T09:28:45Z
- PR: 3387

### Commit message

```
fix(claw): proxy agent action ownership checks (#3387)

## Summary
- make the service-token Agent proxy understand controld's
`{agent_id}:action` route grammar
- preserve the complete action path, query parameters, and request body
when forwarding
- keep tenant-hiding behavior for actions targeting Agents owned by
another org

## Root cause
The service API extracted the ownership-check Agent id by splitting only
on `/`. For top-level controld actions such as `POST
/v1/agents/{agent_id}:upgrade-system-prompt`, the `:action` suffix
became part of the Agent id used by the ownership prefetch. The prefetch
therefore queried a nonexistent Agent and failed closed with 404 before
the real action could be forwarded.

## Test plan
- [x] `services/claw-interface/.venv/bin/pytest
services/claw-interface/tests/unit/test_service_proxy_agents.py -q` (22
passed)
- [x] `bash scripts/verify-changed.sh`
- [x] `git diff --check`
```

### PR body

## Summary
- make the service-token Agent proxy understand controld's `{agent_id}:action` route grammar
- preserve the complete action path, query parameters, and request body when forwarding
- keep tenant-hiding behavior for actions targeting Agents owned by another org

## Root cause
The service API extracted the ownership-check Agent id by splitting only on `/`. For top-level controld actions such as `POST /v1/agents/{agent_id}:upgrade-system-prompt`, the `:action` suffix became part of the Agent id used by the ownership prefetch. The prefetch therefore queried a nonexistent Agent and failed closed with 404 before the real action could be forwarded.

## Test plan
- [x] `services/claw-interface/.venv/bin/pytest services/claw-interface/tests/unit/test_service_proxy_agents.py -q` (22 passed)
- [x] `bash scripts/verify-changed.sh`
- [x] `git diff --check`


## fix(billing): make vertical pack Creem catalog data-driven (#3385)

- sha: `061a18bdcb98c5fb93776df834720f5146621ce4`
- author: tim-srp
- date: 2026-08-14T09:06:05Z
- PR: 3385

### Commit message

```
fix(billing): make vertical pack Creem catalog data-driven (#3385)

## Summary
- derive Restaurant vertical-pack amount and credits from the
server-owned package snapshot
- keep Creem product ID, plan ID, environment, status, currency,
recurring type, and billing-period validation intact
- cover a $1 staging catalog and reject malformed/non-positive snapshot
values

## Root cause
The Restaurant Creem catalog duplicated the business catalog with fixed
`$299` and `20,000 credits` constants. Updating both the staging
vertical-pack plan and its Creem Test Mode product to `$1` still failed
with `billing.creem.enterprise_catalog_mismatch` because the backend
constants remained unchanged.

The Stripe path already treats the server-generated package snapshot as
the business source of truth and verifies the provider price against it.
This change applies the same model to Creem while preserving the
existing provider and plan allowlists. Historical payment and
entitlement processing continues to use the immutable order snapshot.

## Test plan
- [x] regression test: a `$1` plan with `1,000` credits resolves from
the server snapshot
- [x] regression test: the Creem product price must match the
data-driven snapshot price
- [x] reject zero, negative, boolean, and string amount/credits values
- [x] verify Restaurant Creem checkout, reconciliation, renewal, refund,
and vertical-pack purchase tests (`162 passed`)
- [x] Ruff check and format
- [x] Pyright for the changed production module
- [x] pre-commit Python quality hooks, including full Pyright and import
contracts

## Local environment note
The worktree does not have the complete project dependency environment,
so the duplicate pre-push `verify-py.sh` run reported missing
third-party imports across the repository. The commit-time full Pyright
hook passed in its managed environment, targeted Pyright reported zero
errors, and CI remains the authoritative full-suite gate.
```

### PR body

## Summary
- derive Restaurant vertical-pack amount and credits from the server-owned package snapshot
- keep Creem product ID, plan ID, environment, status, currency, recurring type, and billing-period validation intact
- cover a $1 staging catalog and reject malformed/non-positive snapshot values

## Root cause
The Restaurant Creem catalog duplicated the business catalog with fixed `$299` and `20,000 credits` constants. Updating both the staging vertical-pack plan and its Creem Test Mode product to `$1` still failed with `billing.creem.enterprise_catalog_mismatch` because the backend constants remained unchanged.

The Stripe path already treats the server-generated package snapshot as the business source of truth and verifies the provider price against it. This change applies the same model to Creem while preserving the existing provider and plan allowlists. Historical payment and entitlement processing continues to use the immutable order snapshot.

## Test plan
- [x] regression test: a `$1` plan with `1,000` credits resolves from the server snapshot
- [x] regression test: the Creem product price must match the data-driven snapshot price
- [x] reject zero, negative, boolean, and string amount/credits values
- [x] verify Restaurant Creem checkout, reconciliation, renewal, refund, and vertical-pack purchase tests (`162 passed`)
- [x] Ruff check and format
- [x] Pyright for the changed production module
- [x] pre-commit Python quality hooks, including full Pyright and import contracts

## Local environment note
The worktree does not have the complete project dependency environment, so the duplicate pre-push `verify-py.sh` run reported missing third-party imports across the repository. The commit-time full Pyright hook passed in its managed environment, targeted Pyright reported zero errors, and CI remains the authoritative full-suite gate.


## fix(agent-builder): surface preview validation repairs (#3386)

- sha: `52f8fc166620ccd9183779cfeb79a1f303466d6c`
- author: kaka-srp
- date: 2026-08-14T08:53:57Z
- PR: 3386

### Commit message

```
fix(agent-builder): surface preview validation repairs (#3386)

## Summary
- Preserve repairable Preview preflight failures after they are
delivered to Builder, while returning the Project to `drafting`.
- Render the resulting state as a warning in Agent Builder and replace
the misleading success toast for synchronous failures.
- Refine Preview-result feedback so technical gaps are fixed directly,
product or interaction changes wait for explicit approval, and changes
are validated before asking for Refresh Preview.
- Document the cross-repo repair-loop contract.

## Root cause
Preview preflight correctly blocked invalid candidates and posted the
validation error to Builder, but successful delivery cleared the Project
failure fields. The frontend therefore had no state indicating that no
Test Agent was created and showed an unconditional success toast. The
feedback prompt also did not distinguish technical repairs from product
decisions or require post-change validation.

## Cross-repo dependency
Companion Agent Studio PR:
https://github.com/SerendipityOneInc/ecap-agent-pack/pull/243. It adds
the V1 and V2 feedback repair gate and bumps both Pack versions.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] `pytest tests/unit/test_agent_builder_service.py -q` — 170 passed
- [x] Targeted Agent Builder frontend tests — 81 passed
- [x] Commit hooks: frontend lint, Python
ruff/format/pyright/import-linter and repository guards
```

### PR body

## Summary
- Preserve repairable Preview preflight failures after they are delivered to Builder, while returning the Project to `drafting`.
- Render the resulting state as a warning in Agent Builder and replace the misleading success toast for synchronous failures.
- Refine Preview-result feedback so technical gaps are fixed directly, product or interaction changes wait for explicit approval, and changes are validated before asking for Refresh Preview.
- Document the cross-repo repair-loop contract.

## Root cause
Preview preflight correctly blocked invalid candidates and posted the validation error to Builder, but successful delivery cleared the Project failure fields. The frontend therefore had no state indicating that no Test Agent was created and showed an unconditional success toast. The feedback prompt also did not distinguish technical repairs from product decisions or require post-change validation.

## Cross-repo dependency
Companion Agent Studio PR: https://github.com/SerendipityOneInc/ecap-agent-pack/pull/243. It adds the V1 and V2 feedback repair gate and bumps both Pack versions.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] `pytest tests/unit/test_agent_builder_service.py -q` — 170 passed
- [x] Targeted Agent Builder frontend tests — 81 passed
- [x] Commit hooks: frontend lint, Python ruff/format/pyright/import-linter and repository guards


## feat(assets): hide uploads panel in asset library (#3381)

- sha: `b679f095107e091e5ea8e887e5380f3c77462ff4`
- author: bill-srp
- date: 2026-08-14T07:07:05Z
- PR: 3381

### Commit message

```
feat(assets): hide uploads panel in asset library (#3381)

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- 无对应 Linear issue -->

## Summary
- Hide the Uploads panel in the asset library: `AssetLibraryContent` no
longer renders the Uploads/Artifacts tab bar — the artifacts view
(workspace browser sidebar + preview area) renders directly.
Selection-mode wiring (attach-from-library) is unchanged and now flows
only through artifact previews.
- Delete the now-unreferenced `UploadsFeed.tsx` and its unit spec (the
knip dead-code gate fails CI on unused files; git history keeps it
recoverable). The chat Resources panel's separate `MyUploadsTab` is
untouched.
- Remove the now-unused `assets.uploads` / `assets.artifacts` locale
keys (en + zh), stale UploadsFeed mocks/comments in related specs, and
the stale eslint-config doc reference.
- Net −1,344 lines. Independent of #3380 (based on main); both touch the
assets surface but different files.

## Test plan
- [x] TDD: `AssetLibraryContent` spec rewritten first (no tablist
renders; workspace browser + preview render directly; selection-mode
wiring still works) — 4 expected failures against the old
implementation, then green
- [x] All touched specs pass (8 files, 147 tests)
- [x] `bash scripts/verify-web.sh` green: CI guards, tsc, eslint, full
vitest (645 files / 8,676 tests)
- [x] Coverage gate locally: 88.7 / 82.2 / 87.8 / 91.3 vs ratchet 83 /
75 / 81 / 85 (deleting well-covered UploadsFeed does not breach the
ratchet)
```

### PR body

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- 无对应 Linear issue -->

## Summary
- Hide the Uploads panel in the asset library: `AssetLibraryContent` no longer renders the Uploads/Artifacts tab bar — the artifacts view (workspace browser sidebar + preview area) renders directly. Selection-mode wiring (attach-from-library) is unchanged and now flows only through artifact previews.
- Delete the now-unreferenced `UploadsFeed.tsx` and its unit spec (the knip dead-code gate fails CI on unused files; git history keeps it recoverable). The chat Resources panel's separate `MyUploadsTab` is untouched.
- Remove the now-unused `assets.uploads` / `assets.artifacts` locale keys (en + zh), stale UploadsFeed mocks/comments in related specs, and the stale eslint-config doc reference.
- Net −1,344 lines. Independent of #3380 (based on main); both touch the assets surface but different files.

## Test plan
- [x] TDD: `AssetLibraryContent` spec rewritten first (no tablist renders; workspace browser + preview render directly; selection-mode wiring still works) — 4 expected failures against the old implementation, then green
- [x] All touched specs pass (8 files, 147 tests)
- [x] `bash scripts/verify-web.sh` green: CI guards, tsc, eslint, full vitest (645 files / 8,676 tests)
- [x] Coverage gate locally: 88.7 / 82.2 / 87.8 / 91.3 vs ratchet 83 / 75 / 81 / 85 (deleting well-covered UploadsFeed does not breach the ratchet)


## fix(agent-builder): unify chat composers (#3374)

- sha: `b14a4f1ce70d7b0035adbeec89b3e77cf397051e`
- author: lynn Zhuang
- date: 2026-08-14T03:24:36Z
- PR: 3374

### Commit message

```
fix(agent-builder): unify chat composers (#3374)

## Summary

- Route both Agent Builder and Preview through the same `GenClawInput` /
`UnifiedChatComposer` / `@zooclaw/chat-ui` composer path.
- Align composer width, page inset, quick actions, model picker,
send/stop action, disabled state, copy, accessibility labels, and test
hooks.
- Preserve Engine V2-only attachments, transactional attachment
recovery, in-flight submit locking, and Preview auto-feedback behavior.
- Keep Skills and Connectors available when a runtime does not support
file attachments, while hiding Local and Recent file actions.

## Root cause

Builder and Preview rendered separate composer implementations. The
Preview-specific `AgentBuilderTestComposer` duplicated layout and
interaction behavior, so styling and capabilities drifted from the
Builder composer. The fix removes that parallel renderer and passes
Preview-specific runtime capabilities through the shared chat surface
instead.

## Test plan

- [x] `bash scripts/verify-local.sh --changed` (governance guards, app
TypeScript, app ESLint)
- [x] Targeted app Vitest suites: 6 files / 205 tests passed
- [x] `pnpm --filter @zooclaw/chat-ui test` (32 files / 354 tests
passed)
- [x] `pnpm --filter @zooclaw/chat-ui tsc`
- [x] `pnpm --filter @zooclaw/chat-ui lint`
- [x] Authenticated staging route loaded for the real Agent Builder
project; the shared Preview composer rendered in its unavailable state
because the staging Preview build itself was failed. No Retry, Publish,
or message-send mutation was triggered.
```

### PR body

## Summary

- Route both Agent Builder and Preview through the same `GenClawInput` / `UnifiedChatComposer` / `@zooclaw/chat-ui` composer path.
- Align composer width, page inset, quick actions, model picker, send/stop action, disabled state, copy, accessibility labels, and test hooks.
- Preserve Engine V2-only attachments, transactional attachment recovery, in-flight submit locking, and Preview auto-feedback behavior.
- Keep Skills and Connectors available when a runtime does not support file attachments, while hiding Local and Recent file actions.

## Root cause

Builder and Preview rendered separate composer implementations. The Preview-specific `AgentBuilderTestComposer` duplicated layout and interaction behavior, so styling and capabilities drifted from the Builder composer. The fix removes that parallel renderer and passes Preview-specific runtime capabilities through the shared chat surface instead.

## Test plan

- [x] `bash scripts/verify-local.sh --changed` (governance guards, app TypeScript, app ESLint)
- [x] Targeted app Vitest suites: 6 files / 205 tests passed
- [x] `pnpm --filter @zooclaw/chat-ui test` (32 files / 354 tests passed)
- [x] `pnpm --filter @zooclaw/chat-ui tsc`
- [x] `pnpm --filter @zooclaw/chat-ui lint`
- [x] Authenticated staging route loaded for the real Agent Builder project; the shared Preview composer rendered in its unavailable state because the staging Preview build itself was failed. No Retry, Publish, or message-send mutation was triggered.


## feat(agents): add cross-agent artifact library API for v2 engine agents (#3372)

- sha: `c5339dd1a50083bcb3dbe87f36d00202330e64c0`
- author: bill-srp
- date: 2026-08-14T03:12:52Z
- PR: 3372

### Commit message

```
feat(agents): add cross-agent artifact library API for v2 engine agents (#3372)

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- 无对应 Linear issue -->

## Summary
- Add a cross-agent Artifact Library API for v2 engine agents: `GET
/agents/artifacts/library` lists published artifacts across **all** of
the caller's engine workspaces in the current org, merged newest-first
with a `created_before` cursor (`limit` 1–100, default 50). Design spec:
`docs/superpowers/specs/2026-08-13-artifact-library-api.md`.
- New `app/services/agents/artifact_library_service.py`:
`require_agents_v2` gate before any I/O, engine-workspace enumeration
via `list_workspace_agents(runtime="engine")` (cap 200 with warning),
concurrent fan-out to the engine's per-agent `list_artifacts` with the
authenticated `EngineActor`, per-agent `NotFoundError` tolerated (skip +
warning) so one broken agent cannot break the whole library, all other
errors propagate.
- New schemas `ArtifactLibraryEntry` (`workspace_id`, `agent_name`,
nested storage-redacted `AgentArtifactPublic`) and `ArtifactLibraryPage`
(`entries`, `has_more`, `next_cursor`), both `extra="forbid"`.
`workspace_id` lets the frontend reuse the existing per-workspace
download/delete routes.
- Computer (v1) runtime is intentionally out of scope: the FastClaw
directory projection has no stable creation-time/cursor semantics, so
the library is an engine-only capability.
- This is the backend half of the Artifact Library feature; the webapp
`/assets` integration lands in a follow-up PR.

## Test plan
- [x] 7 new service tests
(`tests/unit/test_artifact_library_service.py`): cross-workspace merge
ordering + truncation + cursor, source-level `has_more`, per-agent
not-found tolerance, non-not-found error propagation, empty workspace
list, v2 gate short-circuit, actor/cursor forwarding
- [x] 2 new route tests (`tests/unit/test_agent_artifact_routes.py`):
route registration without shadowing `/agents/{workspace_id}/artifacts`,
authenticated-identity passthrough
- [x] 26 tests pass across the three artifact suites (service + routes +
engine client untouched-regression)
- [x] `bash scripts/verify-py.sh` green: ruff, ruff-format, pyright,
import-linter (8/8 contracts kept)
- [ ] Full pytest + coverage gate runs in CI (`claw-interface-quality`)
```

### PR body

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- 无对应 Linear issue -->

## Summary
- Add a cross-agent Artifact Library API for v2 engine agents: `GET /agents/artifacts/library` lists published artifacts across **all** of the caller's engine workspaces in the current org, merged newest-first with a `created_before` cursor (`limit` 1–100, default 50). Design spec: `docs/superpowers/specs/2026-08-13-artifact-library-api.md`.
- New `app/services/agents/artifact_library_service.py`: `require_agents_v2` gate before any I/O, engine-workspace enumeration via `list_workspace_agents(runtime="engine")` (cap 200 with warning), concurrent fan-out to the engine's per-agent `list_artifacts` with the authenticated `EngineActor`, per-agent `NotFoundError` tolerated (skip + warning) so one broken agent cannot break the whole library, all other errors propagate.
- New schemas `ArtifactLibraryEntry` (`workspace_id`, `agent_name`, nested storage-redacted `AgentArtifactPublic`) and `ArtifactLibraryPage` (`entries`, `has_more`, `next_cursor`), both `extra="forbid"`. `workspace_id` lets the frontend reuse the existing per-workspace download/delete routes.
- Computer (v1) runtime is intentionally out of scope: the FastClaw directory projection has no stable creation-time/cursor semantics, so the library is an engine-only capability.
- This is the backend half of the Artifact Library feature; the webapp `/assets` integration lands in a follow-up PR.

## Test plan
- [x] 7 new service tests (`tests/unit/test_artifact_library_service.py`): cross-workspace merge ordering + truncation + cursor, source-level `has_more`, per-agent not-found tolerance, non-not-found error propagation, empty workspace list, v2 gate short-circuit, actor/cursor forwarding
- [x] 2 new route tests (`tests/unit/test_agent_artifact_routes.py`): route registration without shadowing `/agents/{workspace_id}/artifacts`, authenticated-identity passthrough
- [x] 26 tests pass across the three artifact suites (service + routes + engine client untouched-regression)
- [x] `bash scripts/verify-py.sh` green: ruff, ruff-format, pyright, import-linter (8/8 contracts kept)
- [ ] Full pytest + coverage gate runs in CI (`claw-interface-quality`)


## feat(whatsapp): switch bridge agent pack to oura_ring_whatsapp (#3379)

- sha: `8bc4afb4ac2f86d14ea6a23c03258bb46653e6b7`
- author: Nemo Feng
- date: 2026-08-14T03:03:50Z
- PR: 3379

### Commit message

```
feat(whatsapp): switch bridge agent pack to oura_ring_whatsapp (#3379)

<!-- PR 标题：feat(whatsapp): switch bridge agent pack to
oura_ring_whatsapp -->

## Linear
None — direct cutover task planned with the maintainer on 2026-08-12
(Option A: constants edit).

## Summary
- Switch the WhatsApp bridge's bound agent pack from `oura_ring` (shared
Oura connector pack) to `oura_ring_whatsapp`, the new WhatsApp-only lite
variant (persona "Ora": three daily briefings, WhatsApp-native output
contract, sync nudges).
- Value-only constant edit in
`services/claw-interface/app/services/whatsapp_service.py` — the
`_OURA_RING_*` constant/function names, log strings, and comments are
intentionally unchanged (Option A as planned).
- **Model override decision: kept.** `_OURA_RING_MODEL_PRIMARY =
"litellm/deepseek-v4-flash-0731"` stays as the install-time override.
Engine pack manifests carry no model (it's an install-time concern), so
dropping the override would silently move WhatsApp installs to the
platform default model. Veto here if the new pack should run a different
model.
- Two small review-driven hardenings (adjudicated from an independent
Opus review of the diff):
- `_resolve_routable_user`'s missing-pack log raised `info` → `warning`:
during the gated deploy window this line is the only signal that the
pack isn't live yet, a state that presents as a product-wide WhatsApp
outage ("being prepared" for everyone).
- New unit test pinning `_oura_ring_pack` →
`get_by_org_and_display_id(OFFICIAL_PACK_ORG_ID, "oura_ring_whatsapp")`.
No existing test pinned the display_id (they all patch at the function
boundary), so a typo'd id would have sailed through CI into that same
silent outage. This restores the guard the cutover plan assumed existed.

## ⚠️ Cross-repo dependency — merge/deploy order matters
This PR **relies on SerendipityOneInc/ecap-agent-pack#242** (adds the
`oura_ring_whatsapp` pack: catalog entry + both runtime variants):
https://github.com/SerendipityOneInc/ecap-agent-pack/pull/242

That PR must be merged and the pack live in Pack Store **before this
deploys** — if this ships first, `_oura_ring_pack()` resolves `None`,
every user gets "workspace is being prepared" indefinitely, and the only
telemetry is the (now-`warning`) missing-pack log line.

## Pre-deploy checklist
1. ecap-agent-pack#242 merged; `oura_ring_whatsapp` pack **active** in
Pack Store (org `zooclaw`) with an approved submission carrying a
registered **engine runtime asset**. Install fails pre-claim
(`agent.pack_runtime_variant_unavailable`) if the runtime asset isn't
resolvable — and pre-claim failures leave no `install_failed` row, so
they retry-loop on every inbound message instead of self-healing.
2. `ENGINE_PACK_RUNTIME_ASSETS_PACK_IDS` (env, gcp-foundation)
references the **new pack's pack_id** (or `*`). Env preconditions were
verified 2026-08-12; note the new pack_id only exists once the pack is
created, so re-confirm the list at flip time. If the new pack is absent
from an explicit list, installs silently take the legacy archive path
(different environment pinning/validation regime).
3. New pack is listed **free** (`requires_payment` unset). A paid
listing would fail every bridge install pre-claim with
`agent.purchase_required` — same non-converging loop.
4. **At-cap users check** (found in review; real but population-gated):
the cutover install consumes a visible quota slot
(`consumes_visible_quota=True` default) while the old `oura_ring`
workspace still occupies one. A user already at their plan cap
(free/starter 5, pro 10, ultra 20; vertical-pack holders exempt) fails
`agent.limit_exceeded` **pre-claim** → permanent "being prepared" loop,
one notice per message. Before deploying, count WhatsApp-bound users at
their plan cap; if nonzero, options: uninstall their old `oura_ring`
workspace first, or set `consumes_visible_quota=False` on
`_OURA_RING_INSTALL_CONTEXT` (one line, but a product/billing-semantics
call — deliberately **not** made in this PR).

## Expected post-deploy behavior (not a bug)
- Each already-bound user gets one "workspace is being prepared" notice
while the new pack auto-installs; subsequent replies come from the new
agent.
- Old `oura_ring` workspaces stay installed until manually uninstalled;
conversation memory does not carry over.

## Deployment
Backend-only (`services/claw-interface`). `whatsapp-business-service`
and `web` are untouched. (FYI: `web/app/src/lib/landing-content.ts`
still shows an `oura_ring` landing card — display-only, unrelated to
Pack Store lookup; follow up separately if the card should advertise the
new pack.)

## Test plan
- [x] `bash scripts/verify-py.sh` — ruff-check, ruff-format, pyright (0
errors), import-linter (8/8 contracts) all pass
- [x] Targeted `pytest tests/unit/test_whatsapp_service.py
tests/unit/test_whatsapp_legacy_resolution.py` — green at baseline,
after the constant flip, and after the review hardenings (incl. the new
display_id pinning test)
- [x] Repo-wide sweep for `oura_ring` / `oura-ring` literals — only the
constant changed; remaining hits are private function names
(intentional) and synthetic test fixture ids
- [x] Independent Opus review of the diff: completeness confirmed
(single resolution site; `whatsapp_session_service` inherits via
`_resolve_routable_user`; no stale second path)
- Full `pytest --cov` suite intentionally left to CI
(`claw-interface-quality`) per risk-based local validation
```

### PR body

<!-- PR 标题：feat(whatsapp): switch bridge agent pack to oura_ring_whatsapp -->

## Linear
None — direct cutover task planned with the maintainer on 2026-08-12 (Option A: constants edit).

## Summary
- Switch the WhatsApp bridge's bound agent pack from `oura_ring` (shared Oura connector pack) to `oura_ring_whatsapp`, the new WhatsApp-only lite variant (persona "Ora": three daily briefings, WhatsApp-native output contract, sync nudges).
- Value-only constant edit in `services/claw-interface/app/services/whatsapp_service.py` — the `_OURA_RING_*` constant/function names, log strings, and comments are intentionally unchanged (Option A as planned).
- **Model override decision: kept.** `_OURA_RING_MODEL_PRIMARY = "litellm/deepseek-v4-flash-0731"` stays as the install-time override. Engine pack manifests carry no model (it's an install-time concern), so dropping the override would silently move WhatsApp installs to the platform default model. Veto here if the new pack should run a different model.
- Two small review-driven hardenings (adjudicated from an independent Opus review of the diff):
  - `_resolve_routable_user`'s missing-pack log raised `info` → `warning`: during the gated deploy window this line is the only signal that the pack isn't live yet, a state that presents as a product-wide WhatsApp outage ("being prepared" for everyone).
  - New unit test pinning `_oura_ring_pack` → `get_by_org_and_display_id(OFFICIAL_PACK_ORG_ID, "oura_ring_whatsapp")`. No existing test pinned the display_id (they all patch at the function boundary), so a typo'd id would have sailed through CI into that same silent outage. This restores the guard the cutover plan assumed existed.

## ⚠️ Cross-repo dependency — merge/deploy order matters
This PR **relies on SerendipityOneInc/ecap-agent-pack#242** (adds the `oura_ring_whatsapp` pack: catalog entry + both runtime variants):
https://github.com/SerendipityOneInc/ecap-agent-pack/pull/242

That PR must be merged and the pack live in Pack Store **before this deploys** — if this ships first, `_oura_ring_pack()` resolves `None`, every user gets "workspace is being prepared" indefinitely, and the only telemetry is the (now-`warning`) missing-pack log line.

## Pre-deploy checklist
1. ecap-agent-pack#242 merged; `oura_ring_whatsapp` pack **active** in Pack Store (org `zooclaw`) with an approved submission carrying a registered **engine runtime asset**. Install fails pre-claim (`agent.pack_runtime_variant_unavailable`) if the runtime asset isn't resolvable — and pre-claim failures leave no `install_failed` row, so they retry-loop on every inbound message instead of self-healing.
2. `ENGINE_PACK_RUNTIME_ASSETS_PACK_IDS` (env, gcp-foundation) references the **new pack's pack_id** (or `*`). Env preconditions were verified 2026-08-12; note the new pack_id only exists once the pack is created, so re-confirm the list at flip time. If the new pack is absent from an explicit list, installs silently take the legacy archive path (different environment pinning/validation regime).
3. New pack is listed **free** (`requires_payment` unset). A paid listing would fail every bridge install pre-claim with `agent.purchase_required` — same non-converging loop.
4. **At-cap users check** (found in review; real but population-gated): the cutover install consumes a visible quota slot (`consumes_visible_quota=True` default) while the old `oura_ring` workspace still occupies one. A user already at their plan cap (free/starter 5, pro 10, ultra 20; vertical-pack holders exempt) fails `agent.limit_exceeded` **pre-claim** → permanent "being prepared" loop, one notice per message. Before deploying, count WhatsApp-bound users at their plan cap; if nonzero, options: uninstall their old `oura_ring` workspace first, or set `consumes_visible_quota=False` on `_OURA_RING_INSTALL_CONTEXT` (one line, but a product/billing-semantics call — deliberately **not** made in this PR).

## Expected post-deploy behavior (not a bug)
- Each already-bound user gets one "workspace is being prepared" notice while the new pack auto-installs; subsequent replies come from the new agent.
- Old `oura_ring` workspaces stay installed until manually uninstalled; conversation memory does not carry over.

## Deployment
Backend-only (`services/claw-interface`). `whatsapp-business-service` and `web` are untouched. (FYI: `web/app/src/lib/landing-content.ts` still shows an `oura_ring` landing card — display-only, unrelated to Pack Store lookup; follow up separately if the card should advertise the new pack.)

## Test plan
- [x] `bash scripts/verify-py.sh` — ruff-check, ruff-format, pyright (0 errors), import-linter (8/8 contracts) all pass
- [x] Targeted `pytest tests/unit/test_whatsapp_service.py tests/unit/test_whatsapp_legacy_resolution.py` — green at baseline, after the constant flip, and after the review hardenings (incl. the new display_id pinning test)
- [x] Repo-wide sweep for `oura_ring` / `oura-ring` literals — only the constant changed; remaining hits are private function names (intentional) and synthetic test fixture ids
- [x] Independent Opus review of the diff: completeness confirmed (single resolution site; `whatsapp_session_service` inherits via `_resolve_routable_user`; no stale second path)
- Full `pytest --cov` suite intentionally left to CI (`claw-interface-quality`) per risk-based local validation

