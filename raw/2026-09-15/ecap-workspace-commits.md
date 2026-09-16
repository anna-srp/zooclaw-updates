# SerendipityOneInc/ecap-workspace — commits 2026-09-15

## fix(billing): round credits at API response boundaries (#3743)

- **SHA**: `a09d7320fdf4f7b37604bbe7d384482b913d863a`
- **作者**: tim-srp
- **日期**: 2026-09-15T13:15:53Z
- **PR**: #3743

### Commit Message

```
fix(billing): round credits at API response boundaries (#3743)

## Problem and behavior
Credits balance and usage APIs expose long decimal tails, so clients
show inconsistent precision. Round credit amounts with Decimal
ROUND_HALF_UP at the HTTP response boundary (12.5 → 13), after precise
aggregation and without changing stored data or internal billing
calculations.

## Explicit product decision
The product owner explicitly requires backend rounding for **all
client-facing credit amounts**, including task history and usage
details, and accepts a one-credit display difference.
`/users/credits/usage/details` is intentionally included: returning
`"1"` instead of `"1.230001"` is the requested behavior, not loss of an
exact-value guarantee that should be restored. Its `attribution:
"exact"` describes session ownership, not display precision. The task
consumer stores each already-aggregated session total unchanged; it does
not sum rounded records. Internal aggregation remains decimal-precise,
with no persisted billing changes.

## Changes
- Share CreditsJSONResponse across user credits/balance/usage routes,
staff balance lookup, member quota responses, and Council estimates.
- Make rounding best-effort per field: conversion failures (including
empty/non-numeric strings and non-finite numeric strings) preserve the
original value, while other fields continue rounding. This formatting
must not turn an otherwise valid response into HTTP 500.
- Preserve existing string-versus-number types and null semantics;
currency amounts, conversion rates, counts, and durations remain
precise.
- Remove forced `.00` padding in the web usage record. Clients no longer
need separate credit-rounding changes.

## Validation
- 23 response tests passed after adding invalid-value HTTP 200 and
fallback regression coverage.
- 110 targeted backend tests passed before the fallback follow-up;
includes HTTP response serialization, route registration, half-up ties,
nested wallets, exact aggregate preservation, and estimates.
- 8 web usage-record tests and 6 task-credit consumer tests passed;
changed-file ESLint passed.
- Backend verify-py.sh passed (ruff, format, pyright, import contracts).
- Full local web typecheck was blocked by reused workspace dependencies:
unrelated chat-ui interface mismatches and missing React resolution. CI
installs the pinned dependencies and remains the full frontend gate.

## Deployment
Deploy claw-interface for consistent API values across clients. Deploy
web/app to remove the usage record's forced decimal padding.


## Verified response-field inventory
The allowlist contains 13 fields, traced to the response producers on
the registered routes:
- `services/user/credits_read.py`: `total_credits_balance`,
`current_usage_credits`, `available_credits`, `total_available`,
`subscription_credits`, `topup_credits`.
- `services/billing.py::_normalize_wallets`: `credits_balance`,
`consumed_credits`.
- `services/billing_usage_records.py` and
`services/billing_usage_attribution.py`: `credits` in totals,
buckets/models, groups, and records.
- `schema/member_quota.py::MemberLlmQuota`: `used_credits`,
`quota_credits`.
- `schema/council.py::CouncilEstimate`: `cost_low_credits`,
`cost_high_credits`.

`total_available` and `consumed_credits` are emitted response fields; no
direct client read was found in this repository. They are retained as
existing API outputs, not claimed to be active UI consumers.

Removed unsupported entries: `remaining_credits` (no producer found),
`total_credits` (legacy account storage, not these response fields),
`granted_credits` and `voided_credits` (outgoing billing-service request
parameters, not verified response fields on these routes). A regression
test confirms these names remain untouched.
```

### PR Body

## Problem and behavior
Credits balance and usage APIs expose long decimal tails, so clients show inconsistent precision. Round credit amounts with Decimal ROUND_HALF_UP at the HTTP response boundary (12.5 → 13), after precise aggregation and without changing stored data or internal billing calculations.

## Explicit product decision
The product owner explicitly requires backend rounding for **all client-facing credit amounts**, including task history and usage details, and accepts a one-credit display difference. `/users/credits/usage/details` is intentionally included: returning `"1"` instead of `"1.230001"` is the requested behavior, not loss of an exact-value guarantee that should be restored. Its `attribution: "exact"` describes session ownership, not display precision. The task consumer stores each already-aggregated session total unchanged; it does not sum rounded records. Internal aggregation remains decimal-precise, with no persisted billing changes.

## Changes
- Share CreditsJSONResponse across user credits/balance/usage routes, staff balance lookup, member quota responses, and Council estimates.
- Make rounding best-effort per field: conversion failures (including empty/non-numeric strings and non-finite numeric strings) preserve the original value, while other fields continue rounding. This formatting must not turn an otherwise valid response into HTTP 500.
- Preserve existing string-versus-number types and null semantics; currency amounts, conversion rates, counts, and durations remain precise.
- Remove forced `.00` padding in the web usage record. Clients no longer need separate credit-rounding changes.

## Validation
- 23 response tests passed after adding invalid-value HTTP 200 and fallback regression coverage.
- 110 targeted backend tests passed before the fallback follow-up; includes HTTP response serialization, route registration, half-up ties, nested wallets, exact aggregate preservation, and estimates.
- 8 web usage-record tests and 6 task-credit consumer tests passed; changed-file ESLint passed.
- Backend verify-py.sh passed (ruff, format, pyright, import contracts).
- Full local web typecheck was blocked by reused workspace dependencies: unrelated chat-ui interface mismatches and missing React resolution. CI installs the pinned dependencies and remains the full frontend gate.

## Deployment
Deploy claw-interface for consistent API values across clients. Deploy web/app to remove the usage record's forced decimal padding.


## Verified response-field inventory
The allowlist contains 13 fields, traced to the response producers on the registered routes:
- `services/user/credits_read.py`: `total_credits_balance`, `current_usage_credits`, `available_credits`, `total_available`, `subscription_credits`, `topup_credits`.
- `services/billing.py::_normalize_wallets`: `credits_balance`, `consumed_credits`.
- `services/billing_usage_records.py` and `services/billing_usage_attribution.py`: `credits` in totals, buckets/models, groups, and records.
- `schema/member_quota.py::MemberLlmQuota`: `used_credits`, `quota_credits`.
- `schema/council.py::CouncilEstimate`: `cost_low_credits`, `cost_high_credits`.

`total_available` and `consumed_credits` are emitted response fields; no direct client read was found in this repository. They are retained as existing API outputs, not claimed to be active UI consumers.

Removed unsupported entries: `remaining_credits` (no producer found), `total_credits` (legacy account storage, not these response fields), `granted_credits` and `voided_credits` (outgoing billing-service request parameters, not verified response fields on these routes). A regression test confirms these names remain untouched.


---

## fix(landing): stabilize Safari scrolling and pause hidden demos (#3744)

- **SHA**: `3fa71042a69d542540cba4c479d8cf2c8598b1cc`
- **作者**: shana-srp
- **日期**: 2026-09-15T13:00:04Z
- **PR**: #3744

### Commit Message

```
fix(landing): stabilize Safari scrolling and pause hidden demos (#3744)

## Summary
- Fix homepage jumps in desktop and mobile Safari by keeping all
workplace carousel panels in one stable, intrinsically sized grid row.
Inactive panels are invisible, inert, and excluded from accessibility
APIs.
- Pause carousel timers and repeating platform/runtime animations
outside the viewport, in background tabs, and when reduced motion is
enabled. Preserve manual selection, replay cadence, and keyboard
controls.
- Keep the header's glass effect constant while transitioning its
background and border, avoiding scroll-triggered blur interpolation.

## Root cause
The workplace carousel rendered entering and exiting panels in normal
block flow. Every 2.4 seconds, their heights briefly added together and
then collapsed, moving the content below them. Different final panel
heights also shifted the document. Other homepage demos continued
rendering off-screen, and the fixed header animated its 22px backdrop
blur when scrolling started.

The shared visibility hook now requires 10% intersection, so a thin
strip of section padding at the bottom of a phone viewport does not
start an otherwise hidden demo.

## Test plan
- [x] Frontend governance guards, TypeScript, ESLint, and 77 focused
unit tests (including off-screen/background pause, live reduced motion,
viewport-edge visibility, manual cadence reset, and timer cleanup).
- [x] Playwright WebKit 26.4: desktop English, mobile English, and
mobile Chinese. Automatic cycling visits all three workplace panels with
**0px panel-height variation and no viewport movement**.
- [x] The same Chromium desktop/mobile and Chinese checks passed;
reduced-motion checks wait for the emulated media change to propagate.
- [x] Both engines: keyboard/manual selection, hidden-panel focus
exclusion, no horizontal page overflow, visible-demo updates, and zero
off-screen demo DOM mutations during sampled windows.

| WebKit viewport | Before: panel height during a cycle | After |
| --- | --- | --- |
| 1440 × 900 | 637–1377px | 723px, stable |
| 390 × 844 | 750–2154px | 1259px, stable |

Browser validation used automated WebKit and Chromium on the local mock
stack; physical iPhone/Safari testing has not been performed. These
measurements establish layout stability and stopped off-screen work, not
device FPS.

Design and validation notes:
`docs/superpowers/specs/2026-09-15-safari-landing-render.md`.

The existing homepage dictionary test now supplies the browser
`matchMedia` API required by the visibility hook; its copy assertions
remain unchanged.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary
- Fix homepage jumps in desktop and mobile Safari by keeping all workplace carousel panels in one stable, intrinsically sized grid row. Inactive panels are invisible, inert, and excluded from accessibility APIs.
- Pause carousel timers and repeating platform/runtime animations outside the viewport, in background tabs, and when reduced motion is enabled. Preserve manual selection, replay cadence, and keyboard controls.
- Keep the header's glass effect constant while transitioning its background and border, avoiding scroll-triggered blur interpolation.

## Root cause
The workplace carousel rendered entering and exiting panels in normal block flow. Every 2.4 seconds, their heights briefly added together and then collapsed, moving the content below them. Different final panel heights also shifted the document. Other homepage demos continued rendering off-screen, and the fixed header animated its 22px backdrop blur when scrolling started.

The shared visibility hook now requires 10% intersection, so a thin strip of section padding at the bottom of a phone viewport does not start an otherwise hidden demo.

## Test plan
- [x] Frontend governance guards, TypeScript, ESLint, and 77 focused unit tests (including off-screen/background pause, live reduced motion, viewport-edge visibility, manual cadence reset, and timer cleanup).
- [x] Playwright WebKit 26.4: desktop English, mobile English, and mobile Chinese. Automatic cycling visits all three workplace panels with **0px panel-height variation and no viewport movement**.
- [x] The same Chromium desktop/mobile and Chinese checks passed; reduced-motion checks wait for the emulated media change to propagate.
- [x] Both engines: keyboard/manual selection, hidden-panel focus exclusion, no horizontal page overflow, visible-demo updates, and zero off-screen demo DOM mutations during sampled windows.

| WebKit viewport | Before: panel height during a cycle | After |
| --- | --- | --- |
| 1440 × 900 | 637–1377px | 723px, stable |
| 390 × 844 | 750–2154px | 1259px, stable |

Browser validation used automated WebKit and Chromium on the local mock stack; physical iPhone/Safari testing has not been performed. These measurements establish layout stability and stopped off-screen work, not device FPS.

Design and validation notes: `docs/superpowers/specs/2026-09-15-safari-landing-render.md`.

The existing homepage dictionary test now supplies the browser `matchMedia` API required by the visibility hook; its copy assertions remain unchanged.


---

## feat(tasks): 接入真实任务历史、执行状态和积分用量 (#3737)

- **SHA**: `8c4bc93d6944c1bbe4dd9a28cf020eff28f0a642`
- **作者**: lynn Zhuang
- **日期**: 2026-09-15T10:08:31Z
- **PR**: #3737

### Commit Message

```
feat(tasks): 接入真实任务历史、执行状态和积分用量 (#3737)

## 变更说明

将 Tasks 预览页接入当前用户所属 Agent 的真实聊天记录，包含 Assistant 和自定义
Agent，按最近活动时间排序。保留真实侧边栏 Agent
列表，并区分部分请求失败、历史读取上限及未包含的旧版私信记录，避免把加载失败显示成空列表。

- 通过现有任务会话接口透出 Engine 执行状态，不将聊天生命周期状态当作执行结果。
- 复用现有用量接口，显示近 30
个自然日可精确归属到会话的积分；分页固定查询快照，缓存按用户和组织隔离。不完整或缺失的用量显示为未知，不当作零，也不分摊共享及未归属费用。
- Engine 会话统一进入按 session ID 读取的详情页，修复较早的 Assistant 会话及外部渠道只读历史无法打开的问题。
- 增加刷新按钮，同时重试任务和积分请求；请求期间禁用按钮。积分显示保留两位小数，小额非零费用显示为 `<0.01`。

## 验证结果

- [x] 修复前通过回归测试复现错误跳转和缺少刷新入口。
- [x] Tasks 单元测试：19 个通过。
- [x] 合入最新 main 后，Tasks 及聊天详情相关测试：27 个通过。
- [x] 后端任务历史测试：15 个通过。
- [x] 前端 TypeScript 和 ESLint 通过。
- [x] 后端 Ruff、格式检查、Pyright 和导入边界检查通过。
- [x] 扩大前端验证：431 个测试文件通过；另一个 Mock Backend 文件因本地沙箱禁止监听端口而失败，沙箱外重跑 34
个测试全部通过。
- [x] 已合入最新主线；推送前的改动范围检查全部通过。
- [x] 删除无引用的预览侧边栏组件及样例数据，Knip 死代码／依赖门禁通过。
- [x] 最新提交 `2baa5f5af` 的 GitHub CI 全部完成：前后端质量检查、测试、生产构建、CodeQL
及汇总门禁均通过；不适用的检查正常跳过。
- [x] Codex Review 已正式发布 `APPROVE`，P0／P1／P2 均为 0，审查对应最新提交 `2baa5f5af`。
- [ ] staging／真实环境的聊天历史、渠道跳转及积分归属端到端验证。

## 上线说明

需要同时部署 `claw-interface` 和 `web`。执行状态字段为兼容性新增，旧后端未返回该字段时显示未知。

积分为近 30 天的计量用量，不是会话生命周期总费用，也不是扣除退款等调整后的钱包净变动。此前已有计费验证记录，但本 PR
尚未重新完成生产环境验证。
```

### PR Body

## 变更说明

将 Tasks 预览页接入当前用户所属 Agent 的真实聊天记录，包含 Assistant 和自定义 Agent，按最近活动时间排序。保留真实侧边栏 Agent 列表，并区分部分请求失败、历史读取上限及未包含的旧版私信记录，避免把加载失败显示成空列表。

- 通过现有任务会话接口透出 Engine 执行状态，不将聊天生命周期状态当作执行结果。
- 复用现有用量接口，显示近 30 个自然日可精确归属到会话的积分；分页固定查询快照，缓存按用户和组织隔离。不完整或缺失的用量显示为未知，不当作零，也不分摊共享及未归属费用。
- Engine 会话统一进入按 session ID 读取的详情页，修复较早的 Assistant 会话及外部渠道只读历史无法打开的问题。
- 增加刷新按钮，同时重试任务和积分请求；请求期间禁用按钮。积分显示保留两位小数，小额非零费用显示为 `<0.01`。

## 验证结果

- [x] 修复前通过回归测试复现错误跳转和缺少刷新入口。
- [x] Tasks 单元测试：19 个通过。
- [x] 合入最新 main 后，Tasks 及聊天详情相关测试：27 个通过。
- [x] 后端任务历史测试：15 个通过。
- [x] 前端 TypeScript 和 ESLint 通过。
- [x] 后端 Ruff、格式检查、Pyright 和导入边界检查通过。
- [x] 扩大前端验证：431 个测试文件通过；另一个 Mock Backend 文件因本地沙箱禁止监听端口而失败，沙箱外重跑 34 个测试全部通过。
- [x] 已合入最新主线；推送前的改动范围检查全部通过。
- [x] 删除无引用的预览侧边栏组件及样例数据，Knip 死代码／依赖门禁通过。
- [x] 最新提交 `2baa5f5af` 的 GitHub CI 全部完成：前后端质量检查、测试、生产构建、CodeQL 及汇总门禁均通过；不适用的检查正常跳过。
- [x] Codex Review 已正式发布 `APPROVE`，P0／P1／P2 均为 0，审查对应最新提交 `2baa5f5af`。
- [ ] staging／真实环境的聊天历史、渠道跳转及积分归属端到端验证。

## 上线说明

需要同时部署 `claw-interface` 和 `web`。执行状态字段为兼容性新增，旧后端未返回该字段时显示未知。

积分为近 30 天的计量用量，不是会话生命周期总费用，也不是扣除退款等调整后的钱包净变动。此前已有计费验证记录，但本 PR 尚未重新完成生产环境验证。


---

## refactor(settings): remove Business Pack management and Web R2 bindings (#3733)

- **SHA**: `869e02589ae22c69985091cfa912e19947b5004a`
- **作者**: finn-srp
- **日期**: 2026-09-15T08:58:13Z
- **PR**: #3733

### Commit Message

```
refactor(settings): remove Business Pack management and Web R2 bindings (#3733)

## Summary

- remove the old Business Organization Packs management surface from the
main Web app: pages, navigation, client models/services/hooks, mock
routes, locale strings, and tests
- remove the old `/api/r2/upload` and `/api/r2/pack-assets/*` routes
plus the main Web `R2_PUBLIC_BUCKET` and `R2_AGENT_PACKS_BUCKET`
bindings
- upload organization logos through the existing authenticated
`/storage/r2/presign` flow, followed by a browser PUT
- keep the App Builder Pack publish, submission, install, and
distribution flow unchanged

## Scope

This is a follow-up to the merged Business-to-Settings migration. The
old Business Packs admin UI is not part of the migration and is deleted
rather than hidden behind a feature flag.

There is no `claw-interface` API change, deploy-token change, bucket
migration, object migration, or production deployment in this PR. The
previous token workaround in #3732 was closed because the main Web
Worker no longer needs native R2 bindings.

If Organization Packs management is introduced later, it needs a
backend-owned presigned upload/private-read/auth contract first. This PR
does not leave a dormant frontend implementation or an
`ORGANIZATION_PACKS_ENABLED` switch.

This also avoids the R2 permission failure seen in [the earlier staging
deploy
run](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34940217021).

## Size override

The PR exceeds the normal line limit because it deletes the
migrated-but-unused Business Packs implementation. Most of the diff is a
single bounded removal: more than 4,600 deleted lines across the old UI,
API routes, mocks, locale strings, and their tests. Keeping the deletion
together makes the product boundary reviewable and avoids leaving
partial Pack/R2 code in the main Web app.

## Verification

- Web governance guards passed
- TypeScript passed
- full Vitest suite passed: 794 files, 10,097 tests passed, 70 skipped,
1 todo
- ESLint passed
- dead-code dependency gate passed
- GitHub `web-build-check`, Web lint/typecheck, Web tests, CodeQL, PR
size checks, and automated code review passed

---------

Co-authored-by: wangfulong <wfllike@gmail.com>
```

### PR Body

## Summary

- remove the old Business Organization Packs management surface from the main Web app: pages, navigation, client models/services/hooks, mock routes, locale strings, and tests
- remove the old `/api/r2/upload` and `/api/r2/pack-assets/*` routes plus the main Web `R2_PUBLIC_BUCKET` and `R2_AGENT_PACKS_BUCKET` bindings
- upload organization logos through the existing authenticated `/storage/r2/presign` flow, followed by a browser PUT
- keep the App Builder Pack publish, submission, install, and distribution flow unchanged

## Scope

This is a follow-up to the merged Business-to-Settings migration. The old Business Packs admin UI is not part of the migration and is deleted rather than hidden behind a feature flag.

There is no `claw-interface` API change, deploy-token change, bucket migration, object migration, or production deployment in this PR. The previous token workaround in #3732 was closed because the main Web Worker no longer needs native R2 bindings.

If Organization Packs management is introduced later, it needs a backend-owned presigned upload/private-read/auth contract first. This PR does not leave a dormant frontend implementation or an `ORGANIZATION_PACKS_ENABLED` switch.

This also avoids the R2 permission failure seen in [the earlier staging deploy run](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34940217021).

## Size override

The PR exceeds the normal line limit because it deletes the migrated-but-unused Business Packs implementation. Most of the diff is a single bounded removal: more than 4,600 deleted lines across the old UI, API routes, mocks, locale strings, and their tests. Keeping the deletion together makes the product boundary reviewable and avoids leaving partial Pack/R2 code in the main Web app.

## Verification

- Web governance guards passed
- TypeScript passed
- full Vitest suite passed: 794 files, 10,097 tests passed, 70 skipped, 1 todo
- ESLint passed
- dead-code dependency gate passed
- GitHub `web-build-check`, Web lint/typecheck, Web tests, CodeQL, PR size checks, and automated code review passed


---

## fix(chat): restore Agent workspace replay sharing controls (#3735)

- **SHA**: `8baf71341395aeb415b84e3ab3fe96178936015c`
- **作者**: kaka-srp
- **日期**: 2026-09-15T08:32:48Z
- **PR**: #3735

### Commit Message

```
fix(chat): restore Agent workspace replay sharing controls (#3735)

## Summary

修复 Agent 工作区点击 Share
后能选择消息，却看不到后续操作的问题。分享操作栏现在位于聊天列底部，选择模式下替换输入框；窄屏时自动换行，确保取消和 Share
按钮可见。展开文件预览时，操作栏仍限制在聊天列内。

## Root cause

PR #3724 将 `ChatShareFlowFrame`
包在整个满高工作区外面，导致它追加的操作栏排在可视区域下方；页面也未向聊天组件传递分享模式对应的
`hideComposer`。同时，操作栏固定高度且不换行，窄屏下 Share 按钮会横向溢出。

本次将分享框架移到聊天列内，连接分享状态与输入框显隐，并允许操作栏随可用宽度换行。仅涉及前端，无需后端部署或数据修改。

## Test plan

- [x] 49 项相关现有单元测试通过，覆盖工作区聊天组件、replay 选择状态、操作栏、复选框与分享弹窗；最终改动对应测试已复测。
- [x] TypeScript、改动文件 ESLint、前端治理检查及 `git diff --check` 通过。
- [x] 本地真实浏览器验证桌面 1440×900、平板 768×700、手机 390×844：操作栏及按钮均在可视区域内。
- [x] 验证单选、全选、清空、取消后恢复输入框，以及生成分享链接弹窗；请求仅包含选中的消息。
- [x] 验证展开文件预览时操作栏不越入预览面板。

浏览器验证使用模拟对话；创建 replay 接口返回模拟响应，用于验证前端请求与弹窗。未创建生产分享链接，也未验证真实后端持久化。
```

### PR Body

## Summary

修复 Agent 工作区点击 Share 后能选择消息，却看不到后续操作的问题。分享操作栏现在位于聊天列底部，选择模式下替换输入框；窄屏时自动换行，确保取消和 Share 按钮可见。展开文件预览时，操作栏仍限制在聊天列内。

## Root cause

PR #3724 将 `ChatShareFlowFrame` 包在整个满高工作区外面，导致它追加的操作栏排在可视区域下方；页面也未向聊天组件传递分享模式对应的 `hideComposer`。同时，操作栏固定高度且不换行，窄屏下 Share 按钮会横向溢出。

本次将分享框架移到聊天列内，连接分享状态与输入框显隐，并允许操作栏随可用宽度换行。仅涉及前端，无需后端部署或数据修改。

## Test plan

- [x] 49 项相关现有单元测试通过，覆盖工作区聊天组件、replay 选择状态、操作栏、复选框与分享弹窗；最终改动对应测试已复测。
- [x] TypeScript、改动文件 ESLint、前端治理检查及 `git diff --check` 通过。
- [x] 本地真实浏览器验证桌面 1440×900、平板 768×700、手机 390×844：操作栏及按钮均在可视区域内。
- [x] 验证单选、全选、清空、取消后恢复输入框，以及生成分享链接弹窗；请求仅包含选中的消息。
- [x] 验证展开文件预览时操作栏不越入预览面板。

浏览器验证使用模拟对话；创建 replay 接口返回模拟响应，用于验证前端请求与弹窗。未创建生产分享链接，也未验证真实后端持久化。


---

## fix(chat): 修复 Agent 工作区引用回复无响应 (#3731)

- **SHA**: `f61a712a8cceeee01c02c8c77d1913d1948c8584`
- **作者**: lynn Zhuang
- **日期**: 2026-09-15T07:16:54Z
- **PR**: #3731

### Commit Message

```
fix(chat): 修复 Agent 工作区引用回复无响应 (#3731)

## 修复内容

修复 Agent 工作区中点击消息下方 Reply
没有反应的问题。点击后，输入框会显示引用内容；发送回复时携带引用，也可以手动清除。切换任务、Build
或其他视图时丢弃旧引用，避免带入另一段会话。

未提供引用回复回调的页面不再显示无效的 Reply 按钮。

## 根因

Agent 工作区使用共享聊天组件时，遗漏了 `onQuoteReply`、`quotedText` 和 `onClearQuote`
的连接。同时，消息列表总是提供一个稳定的包装函数，即使上层没有传入回调，消息组件仍会误判为支持引用回复。

## 验证

- [x] 新增回归检查在修复前失败，修复后通过。
- [x] 相关单元测试共 204 项通过，覆盖引用选择、替换、清除、会话切换、页面参数连接及引用发送。
- [x] TypeScript、改动文件 ESLint 和前端治理检查通过。
- [x] 本地浏览器使用模拟后端实测：点击 Reply 显示引用、发送后消息包含引用、Clear reply 正常清除。

仅涉及前端，不需要后端部署；浏览器验证使用模拟数据，未向生产环境发送测试消息。
```

### PR Body

## 修复内容

修复 Agent 工作区中点击消息下方 Reply 没有反应的问题。点击后，输入框会显示引用内容；发送回复时携带引用，也可以手动清除。切换任务、Build 或其他视图时丢弃旧引用，避免带入另一段会话。

未提供引用回复回调的页面不再显示无效的 Reply 按钮。

## 根因

Agent 工作区使用共享聊天组件时，遗漏了 `onQuoteReply`、`quotedText` 和 `onClearQuote` 的连接。同时，消息列表总是提供一个稳定的包装函数，即使上层没有传入回调，消息组件仍会误判为支持引用回复。

## 验证

- [x] 新增回归检查在修复前失败，修复后通过。
- [x] 相关单元测试共 204 项通过，覆盖引用选择、替换、清除、会话切换、页面参数连接及引用发送。
- [x] TypeScript、改动文件 ESLint 和前端治理检查通过。
- [x] 本地浏览器使用模拟后端实测：点击 Reply 显示引用、发送后消息包含引用、Clear reply 正常清除。

仅涉及前端，不需要后端部署；浏览器验证使用模拟数据，未向生产环境发送测试消息。


---

## feat(settings): migrate Business organization management into Settings (#3715)

- **SHA**: `0eafabb67bb74c64a865c9aaf824bce62c11592b`
- **作者**: finn-srp
- **日期**: 2026-09-15T07:03:50Z
- **PR**: #3715

### Commit Message

```
feat(settings): migrate Business organization management into Settings (#3715)

## Linear

N/A — migration spec:
`docs/superpowers/specs/2026-09-14-settings-business-migration.md`

## Summary

- Moves the existing Business organization experience into the main
Settings shell: General, Members, Packs, and Usage.
- Preserves the existing setup, invite acceptance, organization join,
and checkout flows under the main web app.
- Migrates only the file routes required by existing Business behavior:
organization logos in `R2_PUBLIC_BUCKET` and Pack archives/assets in
`R2_AGENT_PACKS_BUCKET`.
- Adds an isolated `team-admin` local mock and four loopback-only
Playwright scenarios.
- Does not add or change any `services/claw-interface` API, move R2
objects, deploy, or cut over a domain.

The `business.zoowork.ai` invite/domain cutover is tracked separately in
#3727. Removal of the old Business frontend remains tracked by #3713 and
must happen only after deployment and observation.

## Review order

The PR is intentionally one migration unit, but the history is split
into seven reviewable commits:

1. `docs(settings): define Business migration boundary`
2. `feat(settings): migrate Business file storage routes`
3. `feat(settings): add organization management pages`
4. `feat(settings): migrate organization Pack management`
5. `feat(settings): migrate setup invite and checkout flows`
6. `test(settings): add team admin mock coverage`
7. `fix(settings): reject oversized R2 uploads before parsing`

The diff exceeds the normal 3,000-line budget because the old Business
surface is being moved as one deployable flow. Splitting General,
Members, Packs, setup/invite, and checkout into separate PRs would leave
intermediate states where navigation or entry flows point to missing
pages. The `size-override` label is therefore retained; reviewers can
follow the commit order above.

## Test plan

- [x] Governance guards, TypeScript, ESLint, and `git diff --check`
passed on Node 24 after rebasing onto current `origin/main`.
- [x] Full frontend unit suite passed: 798 files; 10,112 tests passed,
70 skipped, 1 todo.
- [x] R2 upload route tests passed 7/7, including pre-parse
`Content-Length` rejection and invalid-header fallback.
- [x] Stateful local Playwright suite passed 4/4 against the
loopback-only `team-admin` mock: General/logo persistence, member
lifecycle, quota persistence, and mobile navigation.
- [x] Next production webpack compilation completed successfully
locally.
- [ ] CI `web-build-check` currently fails while fetching existing
Google Fonts (`Inter`, `DM Sans`, and `Cormorant Garamond`) with
`ETIMEDOUT`; no migration module fails compilation.

No production deployment, domain change, payment, real invitation, or
production data write was performed.

---------

Co-authored-by: wangfulong <wfllike@gmail.com>
```

### PR Body

## Linear

N/A — migration spec: `docs/superpowers/specs/2026-09-14-settings-business-migration.md`

## Summary

- Moves the existing Business organization experience into the main Settings shell: General, Members, Packs, and Usage.
- Preserves the existing setup, invite acceptance, organization join, and checkout flows under the main web app.
- Migrates only the file routes required by existing Business behavior: organization logos in `R2_PUBLIC_BUCKET` and Pack archives/assets in `R2_AGENT_PACKS_BUCKET`.
- Adds an isolated `team-admin` local mock and four loopback-only Playwright scenarios.
- Does not add or change any `services/claw-interface` API, move R2 objects, deploy, or cut over a domain.

The `business.zoowork.ai` invite/domain cutover is tracked separately in #3727. Removal of the old Business frontend remains tracked by #3713 and must happen only after deployment and observation.

## Review order

The PR is intentionally one migration unit, but the history is split into seven reviewable commits:

1. `docs(settings): define Business migration boundary`
2. `feat(settings): migrate Business file storage routes`
3. `feat(settings): add organization management pages`
4. `feat(settings): migrate organization Pack management`
5. `feat(settings): migrate setup invite and checkout flows`
6. `test(settings): add team admin mock coverage`
7. `fix(settings): reject oversized R2 uploads before parsing`

The diff exceeds the normal 3,000-line budget because the old Business surface is being moved as one deployable flow. Splitting General, Members, Packs, setup/invite, and checkout into separate PRs would leave intermediate states where navigation or entry flows point to missing pages. The `size-override` label is therefore retained; reviewers can follow the commit order above.

## Test plan

- [x] Governance guards, TypeScript, ESLint, and `git diff --check` passed on Node 24 after rebasing onto current `origin/main`.
- [x] Full frontend unit suite passed: 798 files; 10,112 tests passed, 70 skipped, 1 todo.
- [x] R2 upload route tests passed 7/7, including pre-parse `Content-Length` rejection and invalid-header fallback.
- [x] Stateful local Playwright suite passed 4/4 against the loopback-only `team-admin` mock: General/logo persistence, member lifecycle, quota persistence, and mobile navigation.
- [x] Next production webpack compilation completed successfully locally.
- [ ] CI `web-build-check` currently fails while fetching existing Google Fonts (`Inter`, `DM Sans`, and `Cormorant Garamond`) with `ETIMEDOUT`; no migration module fails compilation.

No production deployment, domain change, payment, real invitation, or production data write was performed.


---

## feat(web): 优化导航、任务预览与智能体详情交互 (#3724)

- **SHA**: `2c9420b9f525c08b1439975f6a501d7c8bf56b29`
- **作者**: lynn Zhuang
- **日期**: 2026-09-15T04:01:59Z
- **PR**: #3724

### Commit Message

```
feat(web): 优化导航、任务预览与智能体详情交互 (#3724)

## 改动说明

统一侧栏导航、Tasks 预览和 Agent 详情页的交互，使创建任务、编辑 Agent、分享聊天与分享 Agent 的入口更清楚。

- 侧栏移除原首页入口，将 Agents 改名为 Home，仍指向 `/agents`；统一 Artifacts、Tasks、Knowledge
文案。
- 整合 `/tasks` 页面：展示任务概览、状态筛选、搜索、分页和带 Actions 表头的聊天跳转入口。
- 收紧 Agents 列表空状态，移除 Mine / Shared with me 标签，将视图切换与新建按钮放到标题同行，并增强
Legacy 入口。
- Agent 详情页增加名称下拉切换，New Task 使用加号，Edit Agent 增加选中态，IM Channels
使用聊天气泡；Recents 隐藏空会话并显示空状态。
- Agent 设置仅在编辑模式展示；编辑模式使用「链接图标 + Share Agent」按钮，聊天模式使用 Recap
选择消息分享，并在切换会话时清空选择。
- 保留 `/new-chat` 的输入框与概览优化：统一内容宽度、缩短标题、调整间距，仅将用户创建的 Agents 纳入常用列表。

## 数据范围

Tasks 当前为带 Preview
标识和明确说明的交互预览，统计与任务记录来自示例数据，尚未接入真实账号的任务状态及额度统计。`/new-chat`
概览继续使用账号查询。原首页仅从侧栏移除，路由保留。

正式环境禁用示例会话跳转，侧栏展示账号自身的 Agent；本地 mock 模式保留完整预览交互。`/new-chat`
活动查询复用聊天页的后端选择与缓存配置。

## 验证

- [x] 提交前 622 项 Agents、Home、Tasks、侧栏相关测试通过。
- [x] Agent 详情与历史查询边界复测通过，覆盖 URL 选中会话、只读历史和 Recents 空状态。
- [x] 34 项 mock Agent 接口测试通过。
- [x] TypeScript、ESLint、治理检查及 PR 体量检查通过。
- [x] 本地浏览器验证导航、任务筛选与跳转、Agent 切换、编辑选中态、设置可见性、Recap 选择消息及生成／撤销示例分享链接。
- [x] 36 项预览边界和查询相关的定向回归测试通过，覆盖 Tasks 搜索、预览跳转限制、mock 分页和会话后端选择。

- [x] CI 完整测试、前端构建、类型与治理检查通过；自动评审未发现问题，代码扫描无开放问题。

CI 中已有的桌面聊天消息排序测试出现一次时间戳相关的非稳定失败，重跑通过；该测试及业务实现未由本 PR 修改。

仅涉及 Web 前端与本地 mock；无需后端或数据库变更。
```

### PR Body

## 改动说明

统一侧栏导航、Tasks 预览和 Agent 详情页的交互，使创建任务、编辑 Agent、分享聊天与分享 Agent 的入口更清楚。

- 侧栏移除原首页入口，将 Agents 改名为 Home，仍指向 `/agents`；统一 Artifacts、Tasks、Knowledge 文案。
- 整合 `/tasks` 页面：展示任务概览、状态筛选、搜索、分页和带 Actions 表头的聊天跳转入口。
- 收紧 Agents 列表空状态，移除 Mine / Shared with me 标签，将视图切换与新建按钮放到标题同行，并增强 Legacy 入口。
- Agent 详情页增加名称下拉切换，New Task 使用加号，Edit Agent 增加选中态，IM Channels 使用聊天气泡；Recents 隐藏空会话并显示空状态。
- Agent 设置仅在编辑模式展示；编辑模式使用「链接图标 + Share Agent」按钮，聊天模式使用 Recap 选择消息分享，并在切换会话时清空选择。
- 保留 `/new-chat` 的输入框与概览优化：统一内容宽度、缩短标题、调整间距，仅将用户创建的 Agents 纳入常用列表。

## 数据范围

Tasks 当前为带 Preview 标识和明确说明的交互预览，统计与任务记录来自示例数据，尚未接入真实账号的任务状态及额度统计。`/new-chat` 概览继续使用账号查询。原首页仅从侧栏移除，路由保留。

正式环境禁用示例会话跳转，侧栏展示账号自身的 Agent；本地 mock 模式保留完整预览交互。`/new-chat` 活动查询复用聊天页的后端选择与缓存配置。

## 验证

- [x] 提交前 622 项 Agents、Home、Tasks、侧栏相关测试通过。
- [x] Agent 详情与历史查询边界复测通过，覆盖 URL 选中会话、只读历史和 Recents 空状态。
- [x] 34 项 mock Agent 接口测试通过。
- [x] TypeScript、ESLint、治理检查及 PR 体量检查通过。
- [x] 本地浏览器验证导航、任务筛选与跳转、Agent 切换、编辑选中态、设置可见性、Recap 选择消息及生成／撤销示例分享链接。
- [x] 36 项预览边界和查询相关的定向回归测试通过，覆盖 Tasks 搜索、预览跳转限制、mock 分页和会话后端选择。

- [x] CI 完整测试、前端构建、类型与治理检查通过；自动评审未发现问题，代码扫描无开放问题。

CI 中已有的桌面聊天消息排序测试出现一次时间戳相关的非稳定失败，重跑通过；该测试及业务实现未由本 PR 修改。

仅涉及 Web 前端与本地 mock；无需后端或数据库变更。


---

## feat(web): rename business marketing routes to enterprise (#3726)

- **SHA**: `cf91f444ea83d5e8e1b331671a77acbd99c029e5`
- **作者**: ericma-srp
- **日期**: 2026-09-15T03:19:04Z
- **PR**: #3726

### Commit Message

```
feat(web): rename business marketing routes to enterprise (#3726)

## Summary

- Rename the enterprise marketing page from `/{locale}/business` to
`/{locale}/enterprise` for all 10 supported locales.
- Update shared navigation/footer links, English labels to
**Enterprise**, and canonical/Open Graph/hreflang URLs.
- Hide the hero eyebrow “Built for AI agents in production” only in
English; preserve Chinese and all other locales.
- Preserve the enterprise page's existing rounded-corner treatment on
the new route (verified automated-review finding).
- Permanently redirect legacy business page URLs to the corresponding
enterprise page, retaining query parameters and browser fragments. Keep
diagram assets and contact APIs unchanged.

## Test plan

- [x] Targeted Vitest suite: **209 tests passed across 12 files**,
covering localization/metadata, navigation/footer, marketing chrome,
redirects, SEO contracts and hero eyebrow visibility across all 10
locales.
- [x] TypeScript check passed during implementation.
- [x] Live local HTTP checks: all 10 enterprise locale pages return 200
with correct canonical URLs; all legacy locale URLs redirect with 301
and preserve query parameters.
- [x] Browser verification: English header/footer display Enterprise; a
legacy URL preserves its query and `#training` anchor after redirect.
- [x] Browser verification: English hero eyebrow removed; Chinese hero
eyebrow unchanged.
- [x] Browser computed-style check: enterprise contact form Submit
button retains the intended 6px corner radius after the route migration.
- [x] `git diff --check`.
- Full test suite and production build are left to CI. Local preview
uses preview-only environment configuration; no environment files or
dependency changes are included.
```

### PR Body

## Summary

- Rename the enterprise marketing page from `/{locale}/business` to `/{locale}/enterprise` for all 10 supported locales.
- Update shared navigation/footer links, English labels to **Enterprise**, and canonical/Open Graph/hreflang URLs.
- Hide the hero eyebrow “Built for AI agents in production” only in English; preserve Chinese and all other locales.
- Preserve the enterprise page's existing rounded-corner treatment on the new route (verified automated-review finding).
- Permanently redirect legacy business page URLs to the corresponding enterprise page, retaining query parameters and browser fragments. Keep diagram assets and contact APIs unchanged.

## Test plan

- [x] Targeted Vitest suite: **209 tests passed across 12 files**, covering localization/metadata, navigation/footer, marketing chrome, redirects, SEO contracts and hero eyebrow visibility across all 10 locales.
- [x] TypeScript check passed during implementation.
- [x] Live local HTTP checks: all 10 enterprise locale pages return 200 with correct canonical URLs; all legacy locale URLs redirect with 301 and preserve query parameters.
- [x] Browser verification: English header/footer display Enterprise; a legacy URL preserves its query and `#training` anchor after redirect.
- [x] Browser verification: English hero eyebrow removed; Chinese hero eyebrow unchanged.
- [x] Browser computed-style check: enterprise contact form Submit button retains the intended 6px corner radius after the route migration.
- [x] `git diff --check`.
- Full test suite and production build are left to CI. Local preview uses preview-only environment configuration; no environment files or dependency changes are included.


---

## feat(billing): add Session and API key usage views (#3723)

- **SHA**: `4164775572e91c5788f3c3e02e335a7c875c4c0e`
- **作者**: kaka-srp
- **日期**: 2026-09-15T02:47:50Z
- **PR**: #3723

### Commit Message

```
feat(billing): add Session and API key usage views (#3723)

## Summary

Billing now supports Session and Managed Agents API key views alongside
account-wide Time usage. New Lago events carry the triggering
session/key; ECAP reads the existing events, applies authorized scope
before aggregation/pagination, preserves Decimal amounts, and explicitly
marks incomplete scans. No new BG usage store or historical backfill.

- Managed API credentials establish producer attribution and `GET
/service/v1/usage` is limited to the authenticated key. Web `GET
/users/credits/usage/details` preserves team member visibility and
revoked-key names.
- Session/API key views request exact attribution;
historical/unattributed rows are hidden, and API key excludes
non-API/shared usage. Time remains account-wide.
- Full cross-repo review fixed BSON UTC membership boundaries and
retained the existing regional/catalog model display names in detail
rows.

## Test plan

- Backend usage/access/events/model display/Service API: 40 tests
passed, including an actual ASGI route with the BFF `cf-ipcountry`
header and BSON round-trip membership dates.
- Existing aligned Time-window semantics are preserved at fixed cutoffs;
24h/7d/30d boundary and cross-view amount regressions passed (22 tests
with the existing Time suite).
- Frontend UsageRecord, UsageDimensions, billing service: 31 tests
passed.
- `verify-py.sh` and `verify-web.sh --no-test` passed; independent fix
review passed.
- Real local/staging-backed acceptance already reconciled same-session
K1/K2/K1, key self-query and cross-key denial, revocation, child
Session, async image, and compute against Lago. Latest extended run: 12
events / 18.4145088888 credits with unchanged payer/cost.
- Final head `2b8de70aa` passed all applicable PR CI and final Codex
review returned APPROVE / no findings. The final commit only completes
cross-repo review documentation.
- Design, implementation and validation evidence are in
`docs/superpowers/` and
`docs/validation/2026-09-14-session-api-key-billing-*.md`.

## Dependencies and limits

[BG #71](https://github.com/SerendipityOneInc/billing-gateway/pull/71),
[GCP
#542](https://github.com/SerendipityOneInc/gcp-foundation/pull/542),
[Proxy
#196](https://github.com/SerendipityOneInc/ecap-proxy-service/pull/196),
and [Engine
#1437](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1437).
Deploy consumers, then Engine migration/API/worker, then ECAP.

No added runtime configuration. Attribution is reporting metadata, not
an authentication or tamper-proof audit credential. Existing charging
credentials determine the payer. Shared agent compute stays shared; the
new Proxy deployment/live acceptance remains explicitly deferred. This
PR is not a production deployment or merge request.
```

### PR Body

## Summary

Billing now supports Session and Managed Agents API key views alongside account-wide Time usage. New Lago events carry the triggering session/key; ECAP reads the existing events, applies authorized scope before aggregation/pagination, preserves Decimal amounts, and explicitly marks incomplete scans. No new BG usage store or historical backfill.

- Managed API credentials establish producer attribution and `GET /service/v1/usage` is limited to the authenticated key. Web `GET /users/credits/usage/details` preserves team member visibility and revoked-key names.
- Session/API key views request exact attribution; historical/unattributed rows are hidden, and API key excludes non-API/shared usage. Time remains account-wide.
- Full cross-repo review fixed BSON UTC membership boundaries and retained the existing regional/catalog model display names in detail rows.

## Test plan

- Backend usage/access/events/model display/Service API: 40 tests passed, including an actual ASGI route with the BFF `cf-ipcountry` header and BSON round-trip membership dates.
- Existing aligned Time-window semantics are preserved at fixed cutoffs; 24h/7d/30d boundary and cross-view amount regressions passed (22 tests with the existing Time suite).
- Frontend UsageRecord, UsageDimensions, billing service: 31 tests passed.
- `verify-py.sh` and `verify-web.sh --no-test` passed; independent fix review passed.
- Real local/staging-backed acceptance already reconciled same-session K1/K2/K1, key self-query and cross-key denial, revocation, child Session, async image, and compute against Lago. Latest extended run: 12 events / 18.4145088888 credits with unchanged payer/cost.
- Final head `2b8de70aa` passed all applicable PR CI and final Codex review returned APPROVE / no findings. The final commit only completes cross-repo review documentation.
- Design, implementation and validation evidence are in `docs/superpowers/` and `docs/validation/2026-09-14-session-api-key-billing-*.md`.

## Dependencies and limits

[BG #71](https://github.com/SerendipityOneInc/billing-gateway/pull/71), [GCP #542](https://github.com/SerendipityOneInc/gcp-foundation/pull/542), [Proxy #196](https://github.com/SerendipityOneInc/ecap-proxy-service/pull/196), and [Engine #1437](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1437). Deploy consumers, then Engine migration/API/worker, then ECAP.

No added runtime configuration. Attribution is reporting metadata, not an authentication or tamper-proof audit credential. Existing charging credentials determine the payer. Shared agent compute stays shared; the new Proxy deployment/live acceptance remains explicitly deferred. This PR is not a production deployment or merge request.


---
