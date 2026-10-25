# SerendipityOneInc/ecap-workspace — commits 2026-10-22

## fix(authoring): preserve pending tests and expose bounded receipts (#4121)

- **SHA**: `b6375f431aa73b3b60d0f03aa294e12070f6cd64`
- **作者**: kaka-srp
- **日期**: 2026-10-22T14:01:05Z
- **PR**: #4121

### Commit Message

```
fix(authoring): preserve pending tests and expose bounded receipts (#4121)

## Summary
When a Build preview outlives the gateway wait window, the old receipt
reports a timeout even while its child is still running. Return
`running`, `passed: null`, and an opaque `test_ref` so Build can observe
that same pinned test without creating another execution.

Receipts now include bounded existing tool-event evidence and the
original source digest/config version. Continuation checks the Agent and
Build-session scope before reading events. Keep the original
session-create body/idempotency key compatible with deployed callers;
register continuation metadata through the existing Engine PATCH API.
Drain full legacy event pages without an extra poll delay.
Missing/stale/other-Agent test references return the same scoped domain
404 as provenance rejections; unrelated upstream failures retain their
existing semantics.

Companion Engine PR:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/2092 (tool
schema and proportional verification guidance). Deploy this backend
before enabling the Engine continuation schema. No migrations, new
dependencies, model changes, or production data mutations.

## Test plan
- [x] 156 focused Python cases: authoring, evaluation, continuation
scope, idempotent metadata-write recovery, client wire contract, source
security, turn snapshot, and Skill evaluation.
- [x] `bash scripts/verify-py.sh`: ruff, formatting, Pyright, and all
eight import contracts.
- [x] Astra local review and targeted re-review: pagination and
missing-reference error mapping findings fixed; no remaining local
findings. The real EngineClient/HTTP legacy-page regression fails before
the fix (one unexpected sleep) and passes after it. For error mapping, a
one-line negative control fails exactly the missing-reference case while
17 receipt cases pass; restoring it passes all 18. Real HTTP 409/503
cases confirm upstream errors are not rewritten as missing references.
- [x] Real local Engine/Temporal/E2B/model functional run: six
continuation assertions; twelve paired Build runs, plus twelve
independent ordinary tasks. See
`docs/research/2026-10-22-build-execution-efficiency-validation.md` with
the retained key statistics and experimental source fingerprints.

In this exploratory two-repeat-per-case pilot, normal-edit model calls
fell from 33 to 27 with the same four test invocations; slow-preview
cases saved successfully in 2/2 optimized runs versus 0/2 baseline runs.
These are small local samples: ECAP repositories were in memory,
slow-preview waits were injected at one second, and the original
long-history/production/Mongo-CSFLE/browser/channel path was not
replayed. Experimental hashes preserve the snapshot before the later
pagination correction. No production speedup guarantee.

Raw experiment JSON has been removed from the PR. The report retains the
results, limits, cleanup conclusions, and source fingerprints; the
change no longer requires a size exception.
```

### PR Body

## Summary
When a Build preview outlives the gateway wait window, the old receipt reports a timeout even while its child is still running. Return `running`, `passed: null`, and an opaque `test_ref` so Build can observe that same pinned test without creating another execution.

Receipts now include bounded existing tool-event evidence and the original source digest/config version. Continuation checks the Agent and Build-session scope before reading events. Keep the original session-create body/idempotency key compatible with deployed callers; register continuation metadata through the existing Engine PATCH API. Drain full legacy event pages without an extra poll delay. Missing/stale/other-Agent test references return the same scoped domain 404 as provenance rejections; unrelated upstream failures retain their existing semantics.

Companion Engine PR: https://github.com/SerendipityOneInc/zooclaw-engine/pull/2092 (tool schema and proportional verification guidance). Deploy this backend before enabling the Engine continuation schema. No migrations, new dependencies, model changes, or production data mutations.

## Test plan
- [x] 156 focused Python cases: authoring, evaluation, continuation scope, idempotent metadata-write recovery, client wire contract, source security, turn snapshot, and Skill evaluation.
- [x] `bash scripts/verify-py.sh`: ruff, formatting, Pyright, and all eight import contracts.
- [x] Astra local review and targeted re-review: pagination and missing-reference error mapping findings fixed; no remaining local findings. The real EngineClient/HTTP legacy-page regression fails before the fix (one unexpected sleep) and passes after it. For error mapping, a one-line negative control fails exactly the missing-reference case while 17 receipt cases pass; restoring it passes all 18. Real HTTP 409/503 cases confirm upstream errors are not rewritten as missing references.
- [x] Real local Engine/Temporal/E2B/model functional run: six continuation assertions; twelve paired Build runs, plus twelve independent ordinary tasks. See `docs/research/2026-10-22-build-execution-efficiency-validation.md` with the retained key statistics and experimental source fingerprints.

In this exploratory two-repeat-per-case pilot, normal-edit model calls fell from 33 to 27 with the same four test invocations; slow-preview cases saved successfully in 2/2 optimized runs versus 0/2 baseline runs. These are small local samples: ECAP repositories were in memory, slow-preview waits were injected at one second, and the original long-history/production/Mongo-CSFLE/browser/channel path was not replayed. Experimental hashes preserve the snapshot before the later pagination correction. No production speedup guarantee.

Raw experiment JSON has been removed from the PR. The report retains the results, limits, cleanup conclusions, and source fingerprints; the change no longer requires a size exception.


---

## feat(platform): add Sentry browser error monitoring (#4122)

- **SHA**: `e4a9ccc67c94bc8996186e582d285655e0043baa`
- **作者**: finn-srp
- **日期**: 2026-10-22T12:12:23Z
- **PR**: #4122

### Commit Message

```
feat(platform): add Sentry browser error monitoring (#4122)

## Summary

Platform currently has no browser error monitoring, so render failures
only appear in the browser console. Initialize `@sentry/react` before
the application and report to the dedicated `zoowork-platform` project,
with separate staging/production environments and commit-scoped
releases.

- Capture render and root errors with React component stacks while
preserving console output. Fallback/recoverable errors are handled;
uncaught root errors remain unhandled.
- Filter known cancellation/ResizeObserver noise and group chunk-loading
failures without dropping them. Disable console/DOM breadcrumbs and
scrub request credentials and URL parameters.
- Reuse the repository `SENTRY_AUTH_TOKEN` for source maps. Uploads
require an explicit flag and a scoped release; plugin failures stop the
build. Delete hidden source maps before Cloudflare deployment.

## Test plan

- [x] Rebased on current `main` (`f4aee46783`); Node 24: `pnpm lint`,
`pnpm typecheck`, `pnpm test` (31 files / 377 tests), and `pnpm build`
passed.
- [x] Real Vite 8/Sentry plugin offline success path: all 32 runtime
debug IDs matched prepared upload comments/maps; all 32 generated `.map`
files were removed from `dist`. The Sentry CLI was replaced with a local
success stub; the actual plugin performed ID injection, artifact
preparation and cleanup.
- [x] Real Vite builds failed on simulated release-creation and
source-map-upload failures; no live Sentry requests were sent.
- [x] Validated workflow YAML/shell configuration and missing-token
failures for both environments.

Live Sentry upload permissions and event ingestion remain to be verified
in staging. This PR covers browser exceptions; Worker monitoring and
handled API/network-error reporting are separate work.
```

### PR Body

## Summary

Platform currently has no browser error monitoring, so render failures only appear in the browser console. Initialize `@sentry/react` before the application and report to the dedicated `zoowork-platform` project, with separate staging/production environments and commit-scoped releases.

- Capture render and root errors with React component stacks while preserving console output. Fallback/recoverable errors are handled; uncaught root errors remain unhandled.
- Filter known cancellation/ResizeObserver noise and group chunk-loading failures without dropping them. Disable console/DOM breadcrumbs and scrub request credentials and URL parameters.
- Reuse the repository `SENTRY_AUTH_TOKEN` for source maps. Uploads require an explicit flag and a scoped release; plugin failures stop the build. Delete hidden source maps before Cloudflare deployment.

## Test plan

- [x] Rebased on current `main` (`f4aee46783`); Node 24: `pnpm lint`, `pnpm typecheck`, `pnpm test` (31 files / 377 tests), and `pnpm build` passed.
- [x] Real Vite 8/Sentry plugin offline success path: all 32 runtime debug IDs matched prepared upload comments/maps; all 32 generated `.map` files were removed from `dist`. The Sentry CLI was replaced with a local success stub; the actual plugin performed ID injection, artifact preparation and cleanup.
- [x] Real Vite builds failed on simulated release-creation and source-map-upload failures; no live Sentry requests were sent.
- [x] Validated workflow YAML/shell configuration and missing-token failures for both environments.

Live Sentry upload permissions and event ingestion remain to be verified in staging. This PR covers browser exceptions; Worker monitoring and handled API/network-error reporting are separate work.


---

## fix(platform): 修复登录后重复跳转导致充值弹窗重置 (#4120)

- **SHA**: `f4aee4678372c76f72f0d0b4a9fbbd03a3f1b29f`
- **作者**: lynn Zhuang
- **日期**: 2026-10-22T10:26:02Z
- **PR**: #4120

### Commit Message

```
fix(platform): 修复登录后重复跳转导致充值弹窗重置 (#4120)

## Summary

修复登录成功后重复导航导致充值弹窗被重新创建的问题。用户从 `?addFunds=1`
进入登录页，登录后开始填写金额时，稍后完成的登录回调可能再次跳转，清空金额草稿。现在由 `HomeRoute`
根据已发布的登录状态统一跳转，邮箱和 Google 登录表单只完成认证。

这是 [Platform 0.0.11
生产发布失败](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/39748356053)
的修复。失败发生在测试阶段，构建及 Cloudflare 上传均未执行，未覆盖生产版本。已推送的
`platform-v0.0.11-release` 不会移动；修复合并、staging 验收后应使用新版本标签发布。

## Root cause

`PasswordlessSignIn` 等待认证 Promise 后主动调用 `navigate`；与此同时，认证状态发布后
`HomeRoute` 已渲染 `Navigate`。两次导航会生成不同的 location key，`AddFundsProvider` 按
location key 管理的弹窗会话随之被重新创建。

CI 表现为 `findByRole` 找到的弹窗在断言前已脱离 DOM。控制认证状态先发布、Promise 后完成的时序后，邮箱和
Google 两个场景都能稳定复现：已输入的 `37` 被重置为
`20`。此次修复移除表单中的重复导航，保留首页的深链接解析、普通登录及恢复会话逻辑；没有增加 sleep、重试或放宽原测试。

## Test plan

- [x] 修改实现前，新增的邮箱 / Google 两项回归测试均因弹窗重建和草稿丢失失败；修改后通过。
- [x] 登录与路由相关 4 个测试文件、140 项测试通过，包含真实 auth provider 的跨标签页退出 / 重新登录用例。
- [x] Platform 全量 26 个测试文件、339 项测试通过。
- [x] Platform lint、TypeScript 检查及生产构建通过（`pnpm build` 包含 `tsc -b`）。
- [x] 仅修改登录表单与回归测试两个文件，无新增后端接口、依赖或支付操作。
- [x] 所有适用 CI 检查通过；[Code
Quality](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/39757342024)
与
[自动审查](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/39757341928)
成功。Claude / Codex 均给出 APPROVE，无需修改的发现，CodeQL 未处理告警为 0。
- [ ] 合并后部署 staging，再发布新的 Platform 补丁版本。

真实 Google / 邮箱登录及真实付款未在本轮执行。没有创建订单、扣款或修改余额。
```

### PR Body

## Summary

修复登录成功后重复导航导致充值弹窗被重新创建的问题。用户从 `?addFunds=1` 进入登录页，登录后开始填写金额时，稍后完成的登录回调可能再次跳转，清空金额草稿。现在由 `HomeRoute` 根据已发布的登录状态统一跳转，邮箱和 Google 登录表单只完成认证。

这是 [Platform 0.0.11 生产发布失败](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/39748356053) 的修复。失败发生在测试阶段，构建及 Cloudflare 上传均未执行，未覆盖生产版本。已推送的 `platform-v0.0.11-release` 不会移动；修复合并、staging 验收后应使用新版本标签发布。

## Root cause

`PasswordlessSignIn` 等待认证 Promise 后主动调用 `navigate`；与此同时，认证状态发布后 `HomeRoute` 已渲染 `Navigate`。两次导航会生成不同的 location key，`AddFundsProvider` 按 location key 管理的弹窗会话随之被重新创建。

CI 表现为 `findByRole` 找到的弹窗在断言前已脱离 DOM。控制认证状态先发布、Promise 后完成的时序后，邮箱和 Google 两个场景都能稳定复现：已输入的 `37` 被重置为 `20`。此次修复移除表单中的重复导航，保留首页的深链接解析、普通登录及恢复会话逻辑；没有增加 sleep、重试或放宽原测试。

## Test plan

- [x] 修改实现前，新增的邮箱 / Google 两项回归测试均因弹窗重建和草稿丢失失败；修改后通过。
- [x] 登录与路由相关 4 个测试文件、140 项测试通过，包含真实 auth provider 的跨标签页退出 / 重新登录用例。
- [x] Platform 全量 26 个测试文件、339 项测试通过。
- [x] Platform lint、TypeScript 检查及生产构建通过（`pnpm build` 包含 `tsc -b`）。
- [x] 仅修改登录表单与回归测试两个文件，无新增后端接口、依赖或支付操作。
- [x] 所有适用 CI 检查通过；[Code Quality](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/39757342024) 与 [自动审查](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/39757341928) 成功。Claude / Codex 均给出 APPROVE，无需修改的发现，CodeQL 未处理告警为 0。
- [ ] 合并后部署 staging，再发布新的 Platform 补丁版本。

真实 Google / 邮箱登录及真实付款未在本轮执行。没有创建订单、扣款或修改余额。


---

## refactor(platform): 统一 clipboard 写入 (#4116)

- **SHA**: `f693b99315bce3301e8db8e526b0175793fdd4fe`
- **作者**: finn-srp
- **日期**: 2026-10-22T09:39:20Z
- **PR**: #4116

### Commit Message

```
refactor(platform): 统一 clipboard 写入 (#4116)

## Summary
- #4115 已合并，本分支已 merge 最新 main，base 改为 `main`，diff 只含本 PR 的 5 个文件。
- `CopyButton`、Webhook signing secret 弹窗、API key secret 弹窗原本各自写了一份
`navigator.clipboard.writeText` 的 try/catch。现在抽成
`web/platform/src/lib/clipboard.ts` 的 `copyText(text):
Promise<boolean>`，只返回是否成功。
- 各处的提示文案和交互保持不变：CopyButton 用 toast 加弹窗内 status；Webhook secret 显示行内
status；API key 成功时按钮变为 Copied，失败时弹 toast。
- 未改动：API key secret 弹窗复制失败时只有 toast，而 modal 会把 Toaster 设为
`aria-hidden`，屏幕阅读器读不到这个失败提示。这一点改变了现有交互，没有放进这个 PR。

## Test plan
- [x] `web/platform`（Node 24）：`pnpm lint`、`pnpm typecheck`、`pnpm
test`（340 passed，merge main 之后重跑）、`pnpm build`
- [x] 新增 `clipboard.test.ts`：成功、被拒绝、clipboard API 不存在三种情况

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

### PR Body

## Summary
- #4115 已合并，本分支已 merge 最新 main，base 改为 `main`，diff 只含本 PR 的 5 个文件。
- `CopyButton`、Webhook signing secret 弹窗、API key secret 弹窗原本各自写了一份 `navigator.clipboard.writeText` 的 try/catch。现在抽成 `web/platform/src/lib/clipboard.ts` 的 `copyText(text): Promise<boolean>`，只返回是否成功。
- 各处的提示文案和交互保持不变：CopyButton 用 toast 加弹窗内 status；Webhook secret 显示行内 status；API key 成功时按钮变为 Copied，失败时弹 toast。
- 未改动：API key secret 弹窗复制失败时只有 toast，而 modal 会把 Toaster 设为 `aria-hidden`，屏幕阅读器读不到这个失败提示。这一点改变了现有交互，没有放进这个 PR。

## Test plan
- [x] `web/platform`（Node 24）：`pnpm lint`、`pnpm typecheck`、`pnpm test`（340 passed，merge main 之后重跑）、`pnpm build`
- [x] 新增 `clipboard.test.ts`：成功、被拒绝、clipboard API 不存在三种情况

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(models): use LiteLLM CN metadata for regional display (#4119)

- **SHA**: `b32bdf9af1052e1594d7925cef744b1e2f0e21ed`
- **作者**: sam-srp
- **日期**: 2026-10-22T08:55:00Z
- **PR**: #4119

### Commit Message

```
feat(models): use LiteLLM CN metadata for regional display (#4119)

## Summary

Model presentation currently reads regional overrides from Google
Sheet-synced Mongo data even though LiteLLM now provides the Chinese
metadata. Resolve the effective region using the existing current-org →
Cloudflare → CN priority, then use LiteLLM `model_info.display_name_cn`,
`description_cn`, and `logo_url_cn` for CN requests. Missing, blank, or
conflicting CN fields independently fall back to the original metadata;
other regions keep the original fields.

- Apply the same display-name selection to Settings Usage, including
unambiguous provider aliases.
- Ignore invalid types in optional CN fields with a diagnostic warning,
retaining the deployment's original metadata, prices, aliases, and
display tier.
- Preserve model IDs, entitlements, visibility, default selection,
prices, and display tiers.
- Remove the obsolete Mongo override reader, schema, related tests, and
import-contract entries. Existing database records are left intact.
- Backend-only change; no new environment variables or data migration.
Deployment should ensure the CN fields are populated in LiteLLM;
metadata retains the existing five-minute cache.

## Test plan

- [x] 176 targeted unit tests passed, covering model catalog, CN field
fallback/conflicts/invalid types, regional resolution, shared-cache
isolation, Usage aliases/routes, display tiers, and model retirement.
Invalid-type cases exercise the LiteLLM fetch path for each CN field.
- [x] `bash scripts/verify-py.sh`: Ruff lint/format, Pyright, and all
eight import contracts passed.
- [x] Complexity, repository-list synchronization, and dead-code checks
passed.
- [ ] Staging verification against real LiteLLM metadata after
deployment.
```

### PR Body

## Summary

Model presentation currently reads regional overrides from Google Sheet-synced Mongo data even though LiteLLM now provides the Chinese metadata. Resolve the effective region using the existing current-org → Cloudflare → CN priority, then use LiteLLM `model_info.display_name_cn`, `description_cn`, and `logo_url_cn` for CN requests. Missing, blank, or conflicting CN fields independently fall back to the original metadata; other regions keep the original fields.

- Apply the same display-name selection to Settings Usage, including unambiguous provider aliases.
- Ignore invalid types in optional CN fields with a diagnostic warning, retaining the deployment's original metadata, prices, aliases, and display tier.
- Preserve model IDs, entitlements, visibility, default selection, prices, and display tiers.
- Remove the obsolete Mongo override reader, schema, related tests, and import-contract entries. Existing database records are left intact.
- Backend-only change; no new environment variables or data migration. Deployment should ensure the CN fields are populated in LiteLLM; metadata retains the existing five-minute cache.

## Test plan

- [x] 176 targeted unit tests passed, covering model catalog, CN field fallback/conflicts/invalid types, regional resolution, shared-cache isolation, Usage aliases/routes, display tiers, and model retirement. Invalid-type cases exercise the LiteLLM fetch path for each CN field.
- [x] `bash scripts/verify-py.sh`: Ruff lint/format, Pyright, and all eight import contracts passed.
- [x] Complexity, repository-list synchronization, and dead-code checks passed.
- [ ] Staging verification against real LiteLLM metadata after deployment.


---

## feat(platform): 给显示 ID 的地方加复制按钮 (#4115)

- **SHA**: `514d8ecbbe8d9f4270cdfd2526291ea262213114`
- **作者**: finn-srp
- **日期**: 2026-10-22T08:43:54Z
- **PR**: #4115

### Commit Message

```
feat(platform): 给显示 ID 的地方加复制按钮 (#4115)

## Linear


## Summary
- Platform 上的 Organization ID 不好选中复制（群里 FDE 反馈）。新增共享的 `CopyButton` 和
`CopyableValue`（`web/platform/src/components/copy-button.tsx`），给以下值加了复制按钮：Organization
ID、Project ID（列表和详情）、Webhook Endpoint URL / Endpoint ID、Delivery ID /
Event ID、测试 Receipt ID、Usage 的 Session ID。Account 页原有的复制按钮改用同一组件。
- Projects 和 Usage 表格每行的按钮在 accessible name 里带上行标识（例如 `Copy Project ID
for Production API`），避免多个同名按钮。
- Delivery 详情是 modal，Radix 会把弹窗外的 Toaster 设为
`aria-hidden`，所以按钮在弹窗内另外渲染一个 sr-only 的 `role="status"` 来播报复制结果。
- Delivery 详情弹窗打开时，焦点改为落在弹窗本身。之前数据从缓存渲染时，焦点会落在第一个复制按钮上，并直接弹出 tooltip。
- 未处理：Delivery history 列表里的 event_id 在一个可点击的 `<button>`
里，不能再嵌套按钮，可在详情弹窗复制；API key 列表只显示前缀，不加。

## Test plan
- [x] `web/platform`（Node 24）：`pnpm lint`、`pnpm typecheck`、`pnpm
test`（312 passed）、`pnpm build`
- [x] 新增 `copy-button.test.tsx`：复制成功和失败、行标识、弹窗内 status、空值显示
- [x] 新增 webhooks 测试：从缓存重新打开 Delivery 详情时焦点在弹窗上；去掉修复后该测试失败
- [x] 本地 preview 实际点击 Organization ID 的复制按钮，出现 "Organization ID
copied."；Projects 列表布局正常

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

### PR Body

## Linear


## Summary
- Platform 上的 Organization ID 不好选中复制（群里 FDE 反馈）。新增共享的 `CopyButton` 和 `CopyableValue`（`web/platform/src/components/copy-button.tsx`），给以下值加了复制按钮：Organization ID、Project ID（列表和详情）、Webhook Endpoint URL / Endpoint ID、Delivery ID / Event ID、测试 Receipt ID、Usage 的 Session ID。Account 页原有的复制按钮改用同一组件。
- Projects 和 Usage 表格每行的按钮在 accessible name 里带上行标识（例如 `Copy Project ID for Production API`），避免多个同名按钮。
- Delivery 详情是 modal，Radix 会把弹窗外的 Toaster 设为 `aria-hidden`，所以按钮在弹窗内另外渲染一个 sr-only 的 `role="status"` 来播报复制结果。
- Delivery 详情弹窗打开时，焦点改为落在弹窗本身。之前数据从缓存渲染时，焦点会落在第一个复制按钮上，并直接弹出 tooltip。
- 未处理：Delivery history 列表里的 event_id 在一个可点击的 `<button>` 里，不能再嵌套按钮，可在详情弹窗复制；API key 列表只显示前缀，不加。

## Test plan
- [x] `web/platform`（Node 24）：`pnpm lint`、`pnpm typecheck`、`pnpm test`（312 passed）、`pnpm build`
- [x] 新增 `copy-button.test.tsx`：复制成功和失败、行标识、弹窗内 status、空值显示
- [x] 新增 webhooks 测试：从缓存重新打开 Delivery 详情时焦点在弹窗上；去掉修复后该测试失败
- [x] 本地 preview 实际点击 Organization ID 的复制按钮，出现 "Organization ID copied."；Projects 列表布局正常

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## fix(platform): 原地打开充值弹窗并统一购买引导样式 (#4114)

- **SHA**: `34fac52def8d8bcde0fef8bf3fe2deaa2f39e5e1`
- **作者**: lynn Zhuang
- **日期**: 2026-10-22T08:19:54Z
- **PR**: #4114

### Commit Message

```
fix(platform): 原地打开充值弹窗并统一购买引导样式 (#4114)

## 改动说明

修复点击一级侧边栏 Add funds 后先跳转 Billing、再显示弹窗的问题。现在会在 API keys、Webhooks、Usage
等当前页面上直接打开充值弹窗，保留背景页面、URL、筛选状态与滚动位置；关闭后焦点返回原入口。

- 由页面框架统一承载充值弹窗，侧边栏、账户面板和 Billing 按钮复用同一入口。保留外部 `billing?addFunds=1`
深链接，关闭时只移除该参数。
- 首充优惠卡与普通充值提醒只出现在一级导航，Settings 二级导航不重复展示。手机导航和账户弹层在打开充值弹窗前关闭。
- 引导卡采用 Platform 品牌色、填充渐变礼物与共享 outline Button。参照首页 Agent 卡片，让 48px
礼物半露出顶部，默认卡片本体由 190px 压至 138px。
- 弹窗内复用相同礼物资产和品牌文字色，保留原有 18px 图标、13px 字号及间距。
- 导航菜单与引导卡共享滚动区，账户入口固定，保证短窗口下各入口可访问。

## Review 修复

- 后台 Billing 读取失败时保留已打开的弹窗和金额，暂停提交；读取恢复后继续当前输入，避免自动关闭/重新弹出。权限失效则丢弃会话。
- 各入口显式传入焦点目标；跳过断开、disabled、inert 或无法聚焦的目标，回退到页面正文。
- 通过共享 `PrimaryNavAccountMenu.onCloseAutoFocus`
在账户面板关闭后交接弹窗，正确区分头像和箭头；移动端返回导航开关。
- 每次打开创建独立表单会话，关闭、query/hash 或组织变化时清理；同一会话内的支付重试仍保持幂等。
- 会话销毁后忽略未完成 checkout 请求的客户端跳转和提示，避免返回上一页后被旧响应带去
Stripe；新增延迟成功响应测试及未修复版本的反证验证。
- 弹窗按需挂载，统一 `canAddFunds` 和 Billing 错误展示，减少重复条件。

## 原因与实现边界

原 Add funds 入口是前往 Billing 的链接，弹窗也只挂载在 Billing 页面；Settings
侧边栏又重复渲染了购买引导。现将弹窗抽取到共享页面框架，按当前位置和 Organization 管理打开状态。


金额校验、服务端优惠资格、权限和支付请求沿用原实现；同一弹窗会话内的重试复用幂等键，关闭重开后创建新的会话；打开或关闭弹窗不创建订单。本次只修改
Platform 前端及说明文档。礼物沿用 MIT 授权的 Heroicons solid 轮廓，许可证随资产保留。

配套的导航与引导卡组合规范及账户焦点交接 API 已同步到 [Design System PR
#8](https://github.com/SerendipityOneInc/Zoowork-design-system/pull/8)，提交
`58178af`。基础库预览包 `2.2.0-pr.8.39741949566.1` 与固定公开预览已完成自动交付并核对版本。

## 验证

- [x] 已同步最新 `main`，无冲突。
- [x] Platform lint、typecheck、生产 build 通过。
- [x] 评论修复后路由回归测试 125 项、共享账户组件测试 10
项通过，覆盖轮询失败/恢复、权限与组织变化、实际入口回焦、无效焦点目标、关闭重开和 query/hash 变化；此前完整 Platform 测试
312 项通过。
- [x] 浏览器检查：桌面明暗主题、390px / 320px 手机、844×390
短窗口；礼物完整可见、无横向溢出、导航可达、弹窗底部操作固定。
- [x] 核对弹窗和侧栏的图形来源及明暗主题文字色一致，弹窗图标仍为 18×18px、文字为 13px / 20px；提示浮层正常。
- [x] 浏览器未发现控制台错误。
- [x] 最新头 `030af2398` 的全部适用 CI 检查通过：Platform、主站/其他前端检查、构建、CodeQL
和大小/标题检查；无未处理 CodeQL 告警。Claude 安装先遇到 HTTP 429，失败任务重跑后通过。
- [x] 人工 review 的 9 条意见已修复、逐项回复并解决线程；失效会话跳转已修复。最新 Claude / Codex 审查均给出
APPROVE 结论，未发现新增阻塞问题。
- [ ] 合并后按 staging 验收流程检查。

本地使用样例数据完成验证，未执行真实 Stripe 扣款或 Platform 部署。

最新审查的非阻塞建议已核对：迟到 checkout 仍由服务端保留，Billing 显示 Awaiting payment；既有
Checkout 有 24 小时有效期，expired webhook 与后台对账会取消待支付订单并记录审计。未更改后台财务流程。`open`
prop 清理属于风格简化，本轮不追加改动；移动端交接已有集成测试和浏览器验证，未添加独立 E2E 套件。

## 分批提交与回退

1. `a54ed4f30`：原地充值弹窗与一级导航引导。
2. `22f1dc895`：短视口导航和引导卡的可访问性。
3. `d9a8fb992`：紧凑卡片与礼物露出顶部。
4. `835ad17e2`：弹窗礼物与品牌文字色统一。
5. `95d33e93b`：处理 review 的 9 条意见，修复会话状态和焦点交接，收拢重复判断并补充回归覆盖。
6. `030af2398`：忽略已退出充值会话的异步跳转和提示，保留当前会话及服务端处理。

可逐批回退；本次不涉及数据库迁移或后端部署。
```

### PR Body

## 改动说明

修复点击一级侧边栏 Add funds 后先跳转 Billing、再显示弹窗的问题。现在会在 API keys、Webhooks、Usage 等当前页面上直接打开充值弹窗，保留背景页面、URL、筛选状态与滚动位置；关闭后焦点返回原入口。

- 由页面框架统一承载充值弹窗，侧边栏、账户面板和 Billing 按钮复用同一入口。保留外部 `billing?addFunds=1` 深链接，关闭时只移除该参数。
- 首充优惠卡与普通充值提醒只出现在一级导航，Settings 二级导航不重复展示。手机导航和账户弹层在打开充值弹窗前关闭。
- 引导卡采用 Platform 品牌色、填充渐变礼物与共享 outline Button。参照首页 Agent 卡片，让 48px 礼物半露出顶部，默认卡片本体由 190px 压至 138px。
- 弹窗内复用相同礼物资产和品牌文字色，保留原有 18px 图标、13px 字号及间距。
- 导航菜单与引导卡共享滚动区，账户入口固定，保证短窗口下各入口可访问。

## Review 修复

- 后台 Billing 读取失败时保留已打开的弹窗和金额，暂停提交；读取恢复后继续当前输入，避免自动关闭/重新弹出。权限失效则丢弃会话。
- 各入口显式传入焦点目标；跳过断开、disabled、inert 或无法聚焦的目标，回退到页面正文。
- 通过共享 `PrimaryNavAccountMenu.onCloseAutoFocus` 在账户面板关闭后交接弹窗，正确区分头像和箭头；移动端返回导航开关。
- 每次打开创建独立表单会话，关闭、query/hash 或组织变化时清理；同一会话内的支付重试仍保持幂等。
- 会话销毁后忽略未完成 checkout 请求的客户端跳转和提示，避免返回上一页后被旧响应带去 Stripe；新增延迟成功响应测试及未修复版本的反证验证。
- 弹窗按需挂载，统一 `canAddFunds` 和 Billing 错误展示，减少重复条件。

## 原因与实现边界

原 Add funds 入口是前往 Billing 的链接，弹窗也只挂载在 Billing 页面；Settings 侧边栏又重复渲染了购买引导。现将弹窗抽取到共享页面框架，按当前位置和 Organization 管理打开状态。

金额校验、服务端优惠资格、权限和支付请求沿用原实现；同一弹窗会话内的重试复用幂等键，关闭重开后创建新的会话；打开或关闭弹窗不创建订单。本次只修改 Platform 前端及说明文档。礼物沿用 MIT 授权的 Heroicons solid 轮廓，许可证随资产保留。

配套的导航与引导卡组合规范及账户焦点交接 API 已同步到 [Design System PR #8](https://github.com/SerendipityOneInc/Zoowork-design-system/pull/8)，提交 `58178af`。基础库预览包 `2.2.0-pr.8.39741949566.1` 与固定公开预览已完成自动交付并核对版本。

## 验证

- [x] 已同步最新 `main`，无冲突。
- [x] Platform lint、typecheck、生产 build 通过。
- [x] 评论修复后路由回归测试 125 项、共享账户组件测试 10 项通过，覆盖轮询失败/恢复、权限与组织变化、实际入口回焦、无效焦点目标、关闭重开和 query/hash 变化；此前完整 Platform 测试 312 项通过。
- [x] 浏览器检查：桌面明暗主题、390px / 320px 手机、844×390 短窗口；礼物完整可见、无横向溢出、导航可达、弹窗底部操作固定。
- [x] 核对弹窗和侧栏的图形来源及明暗主题文字色一致，弹窗图标仍为 18×18px、文字为 13px / 20px；提示浮层正常。
- [x] 浏览器未发现控制台错误。
- [x] 最新头 `030af2398` 的全部适用 CI 检查通过：Platform、主站/其他前端检查、构建、CodeQL 和大小/标题检查；无未处理 CodeQL 告警。Claude 安装先遇到 HTTP 429，失败任务重跑后通过。
- [x] 人工 review 的 9 条意见已修复、逐项回复并解决线程；失效会话跳转已修复。最新 Claude / Codex 审查均给出 APPROVE 结论，未发现新增阻塞问题。
- [ ] 合并后按 staging 验收流程检查。

本地使用样例数据完成验证，未执行真实 Stripe 扣款或 Platform 部署。

最新审查的非阻塞建议已核对：迟到 checkout 仍由服务端保留，Billing 显示 Awaiting payment；既有 Checkout 有 24 小时有效期，expired webhook 与后台对账会取消待支付订单并记录审计。未更改后台财务流程。`open` prop 清理属于风格简化，本轮不追加改动；移动端交接已有集成测试和浏览器验证，未添加独立 E2E 套件。

## 分批提交与回退

1. `a54ed4f30`：原地充值弹窗与一级导航引导。
2. `22f1dc895`：短视口导航和引导卡的可访问性。
3. `d9a8fb992`：紧凑卡片与礼物露出顶部。
4. `835ad17e2`：弹窗礼物与品牌文字色统一。
5. `95d33e93b`：处理 review 的 9 条意见，修复会话状态和焦点交接，收拢重复判断并补充回归覆盖。
6. `030af2398`：忽略已退出充值会话的异步跳转和提示，保留当前会话及服务端处理。

可逐批回退；本次不涉及数据库迁移或后端部署。



---

## fix(agents): allow legacy Work runtime owner reads (#4117)

- **SHA**: `bbd548237d778128d3d8e44b83db77a73f4c9a2b`
- **作者**: kaka-srp
- **日期**: 2026-10-22T07:42:14Z
- **PR**: #4117

### Commit Message

```
fix(agents): allow legacy Work runtime owner reads (#4117)

## Summary

Legacy Work Skills that read the owner's Agent list and schedules
currently lose access when their user Bearer is replaced by an opaque
runtime credential. Allow that credential on four existing read
endpoints: Agent list, Agent detail, schedule delivery targets, and
schedule list.

The new read principal verifies the live credential, canonical source
Agent, current applied projection and legacy policy, and active
owner/organization membership. Existing target ownership checks remain
in place; explicit context headers must match. Runtime list requests
skip the implicit default-Agent retry/create. All other endpoints retain
their current login dependency.

## Root cause

These reads only accepted the user login principal. A runtime credential
must retain its narrower read purpose instead of becoming a user login
or authorizing Agent/schedule changes. No policy schema, customer Skill,
login or JWT changes are included.

## Test plan

- 144 related tests passed, including HTTP sibling reads, foreign
owner/org rejection, legacy/explicit/Platform/revoked/context guards,
and no implicit creation during runtime list.
- Normal pre-push changed-surface verification passed: Ruff
check/format, full application/test Pyright and all eight import
contracts. Commit hooks also passed.
- Staging acceptance for this CI change has not run. The separate Proxy
KB compatibility PR222 is independently staged and is not a prerequisite
for these reads.
```

### PR Body

## Summary

Legacy Work Skills that read the owner's Agent list and schedules currently lose access when their user Bearer is replaced by an opaque runtime credential. Allow that credential on four existing read endpoints: Agent list, Agent detail, schedule delivery targets, and schedule list.

The new read principal verifies the live credential, canonical source Agent, current applied projection and legacy policy, and active owner/organization membership. Existing target ownership checks remain in place; explicit context headers must match. Runtime list requests skip the implicit default-Agent retry/create. All other endpoints retain their current login dependency.

## Root cause

These reads only accepted the user login principal. A runtime credential must retain its narrower read purpose instead of becoming a user login or authorizing Agent/schedule changes. No policy schema, customer Skill, login or JWT changes are included.

## Test plan

- 144 related tests passed, including HTTP sibling reads, foreign owner/org rejection, legacy/explicit/Platform/revoked/context guards, and no implicit creation during runtime list.
- Normal pre-push changed-surface verification passed: Ruff check/format, full application/test Pyright and all eight import contracts. Commit hooks also passed.
- Staging acceptance for this CI change has not run. The separate Proxy KB compatibility PR222 is independently staged and is not a prerequisite for these reads.


---

## fix(web): 按环境配置 Managed Agent API 的 platform 地址 (#4111)

- **SHA**: `4ade38ed6e432f9139c3d0d21617604b3a34e853`
- **作者**: finn-srp
- **日期**: 2026-10-22T01:54:40Z
- **PR**: #4111

### Commit Message

```
fix(web): 按环境配置 Managed Agent API 的 platform 地址 (#4111)

## Summary
- `PLATFORM_HREF` 改为读取构建期变量 `NEXT_PUBLIC_PLATFORM_URL`，未设置时回退到
`https://platform.zoowork.ai`。官网 Get Started 下拉、产品列表、页脚、WebApp
用户菜单、pricing 页这 5 处入口都通过它跳转，不需要逐个改。
- `deploy.yml` 在 `Set environment variables` 和 `Create env file`
中注入该变量，并在 `Validate required variables` 中设为必填。staging 漏配时 deploy
直接失败，不会静默跳回生产。
- `.env.example` 增加该变量（staging 值）。
- GitHub Environment variables 已设置：staging 为
`https://platform.ecap.nosay.live`，production 为
`https://platform.zoowork.ai`。

## Root cause
`web/app/src/lib/platform-href.ts` 把 platform 地址写死为生产域名。Agent Builder
入口用的是相对路径 `/login`，会跟随当前 host，所以 staging 上正常；platform 是独立部署的应用，只能用绝对
URL，而这个 URL 没有按环境区分，导致 staging 的 Managed Agent API 入口跳到了生产。

## Test plan
- [x] 新增
`tests/unit/lib/platform-href.unit.spec.ts`：配置变量时使用配置值，未配置时回退生产地址
- [x] `bash scripts/verify-web.sh`（guards、tsc、vitest、eslint）
- [x] Node 24 下全量 `pnpm test:unit`：866 files，10909 passed，1 skipped
- [x] Node 24 下 `pnpm lint:ci`
- [ ] 合并后 staging deploy 完成，确认 staging 官网 Get Started > Managed Agent
API 跳到 `https://platform.ecap.nosay.live`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

### PR Body

## Summary
- `PLATFORM_HREF` 改为读取构建期变量 `NEXT_PUBLIC_PLATFORM_URL`，未设置时回退到 `https://platform.zoowork.ai`。官网 Get Started 下拉、产品列表、页脚、WebApp 用户菜单、pricing 页这 5 处入口都通过它跳转，不需要逐个改。
- `deploy.yml` 在 `Set environment variables` 和 `Create env file` 中注入该变量，并在 `Validate required variables` 中设为必填。staging 漏配时 deploy 直接失败，不会静默跳回生产。
- `.env.example` 增加该变量（staging 值）。
- GitHub Environment variables 已设置：staging 为 `https://platform.ecap.nosay.live`，production 为 `https://platform.zoowork.ai`。

## Root cause
`web/app/src/lib/platform-href.ts` 把 platform 地址写死为生产域名。Agent Builder 入口用的是相对路径 `/login`，会跟随当前 host，所以 staging 上正常；platform 是独立部署的应用，只能用绝对 URL，而这个 URL 没有按环境区分，导致 staging 的 Managed Agent API 入口跳到了生产。

## Test plan
- [x] 新增 `tests/unit/lib/platform-href.unit.spec.ts`：配置变量时使用配置值，未配置时回退生产地址
- [x] `bash scripts/verify-web.sh`（guards、tsc、vitest、eslint）
- [x] Node 24 下全量 `pnpm test:unit`：866 files，10909 passed，1 skipped
- [x] Node 24 下 `pnpm lint:ci`
- [ ] 合并后 staging deploy 完成，确认 staging 官网 Get Started > Managed Agent API 跳到 `https://platform.ecap.nosay.live`

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
