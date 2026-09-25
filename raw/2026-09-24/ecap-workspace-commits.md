# SerendipityOneInc/ecap-workspace — commits 2026-09-24

## fix(web): 优化模板弹窗、任务文案及首页与文件页展示 (#3903)

- **SHA**: `9367ad27376a384c638b8ceffbb0a02f94dc2569`
- **作者**: lynn Zhuang
- **日期**: 2026-09-24T11:13:20Z
- **PR**: #3903

### Commit Message

```
fix(web): 优化模板弹窗、任务文案及首页与文件页展示 (#3903)

## 修改内容

- 模板选择弹窗底部增加 32px 渐隐和留白，仅在下方仍有内容时显示；滚到底后移除渐隐，完整展示最后一排卡片。
- Agent 侧栏将 `Recents` 改为 `Recent tasks`，中文及空状态同步统一为任务表述。
- 首页保留 `Most Used Agents`，移除重复的 `Agents You Recently Chatted With`
模块，并清理其专用排序、文案和双列布局逻辑；保留 `Recent Activity` 和 `Schedule`。

- Artifacts 浏览页移除来源 Tab，直接加载 AI 生成文件；页面说明同步调整，聊天附件选择器维持原有来源切换。

## 原因与范围

模板列表原先在滚动容器边界直接裁切，视觉过渡突兀；侧栏的新建入口与历史列表命名不一致；首页两组 Agent
基于同一份数据排序，容易出现重复展示。

仅调整前端展示，模板继续从现有 API 获取真实内容，无后端或模板目录数据变更。

## 验证

- Artifacts 页面和附件选择器相关 9 项测试通过。
- TypeScript、ESLint、仓库前端治理检查通过。
- 模板弹窗和侧栏相关 23 项测试通过；首页相关 155 项测试通过。
- 浏览器验证内容不足一屏、桌面溢出、滚到底、手机宽度变化等状态。
- 已启动连接真实 staging 后端的本地预览，用户确认展示效果。
```

### PR Body

## 修改内容

- 模板选择弹窗底部增加 32px 渐隐和留白，仅在下方仍有内容时显示；滚到底后移除渐隐，完整展示最后一排卡片。
- Agent 侧栏将 `Recents` 改为 `Recent tasks`，中文及空状态同步统一为任务表述。
- 首页保留 `Most Used Agents`，移除重复的 `Agents You Recently Chatted With` 模块，并清理其专用排序、文案和双列布局逻辑；保留 `Recent Activity` 和 `Schedule`。

- Artifacts 浏览页移除来源 Tab，直接加载 AI 生成文件；页面说明同步调整，聊天附件选择器维持原有来源切换。

## 原因与范围

模板列表原先在滚动容器边界直接裁切，视觉过渡突兀；侧栏的新建入口与历史列表命名不一致；首页两组 Agent 基于同一份数据排序，容易出现重复展示。

仅调整前端展示，模板继续从现有 API 获取真实内容，无后端或模板目录数据变更。

## 验证

- Artifacts 页面和附件选择器相关 9 项测试通过。
- TypeScript、ESLint、仓库前端治理检查通过。
- 模板弹窗和侧栏相关 23 项测试通过；首页相关 155 项测试通过。
- 浏览器验证内容不足一屏、桌面溢出、滚到底、手机宽度变化等状态。
- 已启动连接真实 staging 后端的本地预览，用户确认展示效果。


---

## fix(marketing): preserve language in industry links (#3899)

- **SHA**: `05e0720402c2b668cdb90d702c9786958c406d59`
- **作者**: ericma-srp
- **日期**: 2026-09-24T08:49:40Z
- **PR**: #3899

### Commit Message

```
fix(marketing): preserve language in industry links (#3899)

## Summary
- Preserve the main site's language when opening an industry solution:
Chinese (`zh`) opens `?lang=zh`; English and every other supported
locale open `?lang=en`.
- Apply the shared URL builder to the Solutions navigation menu,
Solutions cards, shared and standalone footers, and homepage/enterprise
industry cases. For example, English Pricing now links to
`/industry/cn-cbec/?lang=en` instead of the language-unspecified page.

## Root cause
Industry links used fixed URLs without the language parameter supported
by the separate industry site. Translating the main site's link labels
did not select the destination page's language.

## Test plan
- [x] Scoped `scripts/verify-web.sh`: governance guards, TypeScript, 89
existing tests across 7 files, and ESLint passed.
- [x] Runtime check of all 10 supported locales: 27 industry links per
locale across the navigation, Solutions catalog, and footer use the
expected language.
- [x] Browser verification of English, Chinese, and German Pricing
links, the English Solutions dropdown, and Chinese Solutions cards.
- [x] Local rendered-page checks for Chinese/German Solutions and
Chinese homepage/enterprise industry links.
- [x] Production industry page with `?lang=en` renders English and
`?lang=zh` renders Chinese; the legacy enterprise-case domain redirect
preserves the query parameter.
- [x] `git diff --check`.

No industry-site content, SEO canonical URLs, or deployment
configuration is changed.
```

### PR Body

## Summary
- Preserve the main site's language when opening an industry solution: Chinese (`zh`) opens `?lang=zh`; English and every other supported locale open `?lang=en`.
- Apply the shared URL builder to the Solutions navigation menu, Solutions cards, shared and standalone footers, and homepage/enterprise industry cases. For example, English Pricing now links to `/industry/cn-cbec/?lang=en` instead of the language-unspecified page.

## Root cause
Industry links used fixed URLs without the language parameter supported by the separate industry site. Translating the main site's link labels did not select the destination page's language.

## Test plan
- [x] Scoped `scripts/verify-web.sh`: governance guards, TypeScript, 89 existing tests across 7 files, and ESLint passed.
- [x] Runtime check of all 10 supported locales: 27 industry links per locale across the navigation, Solutions catalog, and footer use the expected language.
- [x] Browser verification of English, Chinese, and German Pricing links, the English Solutions dropdown, and Chinese Solutions cards.
- [x] Local rendered-page checks for Chinese/German Solutions and Chinese homepage/enterprise industry links.
- [x] Production industry page with `?lang=en` renders English and `?lang=zh` renders Chinese; the legacy enterprise-case domain redirect preserves the query parameter.
- [x] `git diff --check`.

No industry-site content, SEO canonical URLs, or deployment configuration is changed.


---

## fix(chat): cover revision model warnings and stale message lookups (#3898)

- **SHA**: `66f90a497be4e6017db3d3b407e03a9bbfca8922`
- **作者**: tim-srp
- **日期**: 2026-09-24T08:43:08Z
- **PR**: #3898

### Commit Message

```
fix(chat): cover revision model warnings and stale message lookups (#3898)

## Summary

Editable Revision Agents now receive the unavailable-model prompt when
their selected model is absent from a successfully fetched, nonempty
catalog. Replacements use the existing Revision commit/apply flow,
rather than the legacy direct model API. This fixes the staging Edit
Agent case that continued sending to `deepseek-v4-flash-0731` and
received 403 responses without a replacement prompt.

Chat message rendering now uses stable message IDs and per-message
snapshots instead of list-index subscriptions. This prevents a removed
message's queued reader from throwing `tapClientLookup: Index 2 out of
bounds (length: 2)`. Unchanged message rows are memoized so another
message's streaming updates do not rerender them.

## Root cause

- PR #3819 excluded every external model controller, including editable
Revision Agents; the workspace page also omitted the workspace ID
whenever a controller was present.
- The upstream message list subscribed by index. A shrinking list could
invalidate a child's lookup before its subscription finished. The
existing error boundary recovered afterward but could not prevent the
exception.

Revision controllers explicitly opt into catalog validation. Other
Builder/draft controllers and read-only Agents remain excluded.
Empty/error/loading catalogs still fail open; dismissal/send
interception and API-only model options are unchanged. No
continue-sending bypass was added.

## Test plan

- [x] Reproduced the missing Revision prompt and workspace ID with
failing regressions before the fix.
- [x] Reproduced the exact stale-index error with the actual
assistant-ui runtime; verified safe stale reads after removal, reorder,
empty/repopulate, and streaming render isolation.
- [x] 357 targeted tests passed across 21 files, including message
presentation/actions, Revision settings, and composer behavior.
- [x] Frontend TypeScript, ESLint, and governance guards passed.
- [ ] Full build and suites run in CI.

Frontend deployment only. No live Agent configuration was changed, and
no authenticated staging writes were performed. The repair has not yet
been validated after staging deployment. Resource-preload performance
warnings are outside this fix.
```

### PR Body

## Summary

Editable Revision Agents now receive the unavailable-model prompt when their selected model is absent from a successfully fetched, nonempty catalog. Replacements use the existing Revision commit/apply flow, rather than the legacy direct model API. This fixes the staging Edit Agent case that continued sending to `deepseek-v4-flash-0731` and received 403 responses without a replacement prompt.

Chat message rendering now uses stable message IDs and per-message snapshots instead of list-index subscriptions. This prevents a removed message's queued reader from throwing `tapClientLookup: Index 2 out of bounds (length: 2)`. Unchanged message rows are memoized so another message's streaming updates do not rerender them.

## Root cause

- PR #3819 excluded every external model controller, including editable Revision Agents; the workspace page also omitted the workspace ID whenever a controller was present.
- The upstream message list subscribed by index. A shrinking list could invalidate a child's lookup before its subscription finished. The existing error boundary recovered afterward but could not prevent the exception.

Revision controllers explicitly opt into catalog validation. Other Builder/draft controllers and read-only Agents remain excluded. Empty/error/loading catalogs still fail open; dismissal/send interception and API-only model options are unchanged. No continue-sending bypass was added.

## Test plan

- [x] Reproduced the missing Revision prompt and workspace ID with failing regressions before the fix.
- [x] Reproduced the exact stale-index error with the actual assistant-ui runtime; verified safe stale reads after removal, reorder, empty/repopulate, and streaming render isolation.
- [x] 357 targeted tests passed across 21 files, including message presentation/actions, Revision settings, and composer behavior.
- [x] Frontend TypeScript, ESLint, and governance guards passed.
- [ ] Full build and suites run in CI.

Frontend deployment only. No live Agent configuration was changed, and no authenticated staging writes were performed. The repair has not yet been validated after staging deployment. Resource-preload performance warnings are outside this fix.


---

## fix(perf): cut CPU-load amplification across auth, recovery, builder and billing (#3885)

- **SHA**: `500f68e29a1ccea9334fbb9132b96a8dae18780c`
- **作者**: tim-srp
- **日期**: 2026-09-24T07:10:07Z
- **PR**: #3885

### Commit Message

```
fix(perf): cut CPU-load amplification across auth, recovery, builder and billing (#3885)

## Summary

Reduce duplicate authentication, recovery and Builder polling work while
preserving normal billing behavior. This PR includes the auth
single-flight change from #3878, which it supersedes.

- Coalesce concurrent cache misses for the same token within one
process. A disconnected caller cannot cancel verification for other
waiters; failed verifications are not cached.
- Classify only Billing Gateway's exact `400` / `detail.error ==
"no_active_subscription"` response as a settled absence of access.
Preserve other failures, jitter deferred rechecks and aggregate recovery
logs.
- Back off failed Builder thread reads, reset backoff after successful
reads and prevent duplicate monitors for the same post within one
process.
- Reuse a shared Billing client **only for GET requests**, and close it
through application shutdown. GET retries once on connection failures,
`RemoteProtocolError`, `ReadError` or `WriteError`.
- Keep all 12 Billing mutation entry points on caller-owned clients with
keepalive disabled. Existing HTTP-status retries and compatibility
fallbacks remain unchanged; transport failures never introduce a
mutation replay.

## Review fixes

The latest P1/P2 findings identified two genuine gaps in the previous
revision:

1. Sharing idle connections with non-idempotent writes introduced
peer-disconnect failures. Writes now use fresh connections, including
attempts within existing status-code retry loops, avoiding the need to
guess whether a failed write executed upstream.
2. GET disconnect retries omitted `ReadError` and `WriteError`. Both are
now covered by the existing one-retry limit; cancellation and repeated
failures still propagate.

No payment, subscription, authorization or quota API contract was
changed. The existing HTTP client library is retained; an aiohttp
migration is outside this repair.

## Validation

- 804 relevant billing, model-catalog and recovery tests passed.
- `bash scripts/verify-py.sh` passed: Ruff, formatting, Pyright and all
8 import contracts.
- Regression coverage checks all 12 mutation entry points, client
closure, no mutation transport replay, bounded GET retries and
cancellation.
- Real loopback TCP test confirms GET reuse and distinct connections for
writes, including an existing HTTP 500 retry.
- The repaired working tree was exercised against real staging
dependencies under source fingerprint `PR-working-fix-e8e9ae419c6e`:
- 44/44 query requests succeeded. At concurrency 30, one actual upstream
auth call and P95 3817.47 ms.
- Builder creation, both runtime-recovery paths and actual post-recovery
conversations succeeded.
- Two actual Billing duplicate-wallet POST requests returned the
expected 409s on two independent connections; both clients closed,
wallet inventory remained unchanged, and surrounding GETs reused one
connection.
- Temporary subscription/free-access expiry changes were restored. The
test project was archived and cleaned; the original six instances
remained running.

[Staging
report](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/cpu-remediation-followup/docs/validation/2026-09-24-pr3885/rerun-after-review-fix.md)
· [Sanitized measurements and source
hashes](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/cpu-remediation-followup/docs/validation/2026-09-24-pr3885/rerun-after-review-fix.json)

Staging validation used isolated processes loading the changed modules
over the deployed staging image, not a deployment of the complete PR
image. No production mutation or deployment was performed.
Wallet-conflict checks are not successful topup/payment-flow validation.

## Remaining validation limits

- Full-image deployment, startup/shutdown lifecycle, browser flows,
successful topup and payment callbacks were not exercised in the staging
run.
- No-entitlement/no-credit behavior and transport-fault paths have
unit/local fault-injection evidence, not complete live failure
scenarios.
- The shared GET pool retains default capacity (100 total / 20
keepalive); production peak capacity and CPU improvements remain
unmeasured. The staging concurrency sample is not a performance
benchmark.
- Cross-process deduplication, progressive recovery intervals,
incremental thread reads and request-scoped read deduplication remain
outside scope.

Deploy `claw-interface` after merge. New-commit CI and review results
are authoritative and must settle before merge.

---------

Co-authored-by: chris-srp <chris@srp.one>
```

### PR Body

## Summary

Reduce duplicate authentication, recovery and Builder polling work while preserving normal billing behavior. This PR includes the auth single-flight change from #3878, which it supersedes.

- Coalesce concurrent cache misses for the same token within one process. A disconnected caller cannot cancel verification for other waiters; failed verifications are not cached.
- Classify only Billing Gateway's exact `400` / `detail.error == "no_active_subscription"` response as a settled absence of access. Preserve other failures, jitter deferred rechecks and aggregate recovery logs.
- Back off failed Builder thread reads, reset backoff after successful reads and prevent duplicate monitors for the same post within one process.
- Reuse a shared Billing client **only for GET requests**, and close it through application shutdown. GET retries once on connection failures, `RemoteProtocolError`, `ReadError` or `WriteError`.
- Keep all 12 Billing mutation entry points on caller-owned clients with keepalive disabled. Existing HTTP-status retries and compatibility fallbacks remain unchanged; transport failures never introduce a mutation replay.

## Review fixes

The latest P1/P2 findings identified two genuine gaps in the previous revision:

1. Sharing idle connections with non-idempotent writes introduced peer-disconnect failures. Writes now use fresh connections, including attempts within existing status-code retry loops, avoiding the need to guess whether a failed write executed upstream.
2. GET disconnect retries omitted `ReadError` and `WriteError`. Both are now covered by the existing one-retry limit; cancellation and repeated failures still propagate.

No payment, subscription, authorization or quota API contract was changed. The existing HTTP client library is retained; an aiohttp migration is outside this repair.

## Validation

- 804 relevant billing, model-catalog and recovery tests passed.
- `bash scripts/verify-py.sh` passed: Ruff, formatting, Pyright and all 8 import contracts.
- Regression coverage checks all 12 mutation entry points, client closure, no mutation transport replay, bounded GET retries and cancellation.
- Real loopback TCP test confirms GET reuse and distinct connections for writes, including an existing HTTP 500 retry.
- The repaired working tree was exercised against real staging dependencies under source fingerprint `PR-working-fix-e8e9ae419c6e`:
  - 44/44 query requests succeeded. At concurrency 30, one actual upstream auth call and P95 3817.47 ms.
  - Builder creation, both runtime-recovery paths and actual post-recovery conversations succeeded.
  - Two actual Billing duplicate-wallet POST requests returned the expected 409s on two independent connections; both clients closed, wallet inventory remained unchanged, and surrounding GETs reused one connection.
  - Temporary subscription/free-access expiry changes were restored. The test project was archived and cleaned; the original six instances remained running.

[Staging report](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/cpu-remediation-followup/docs/validation/2026-09-24-pr3885/rerun-after-review-fix.md) · [Sanitized measurements and source hashes](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/cpu-remediation-followup/docs/validation/2026-09-24-pr3885/rerun-after-review-fix.json)

Staging validation used isolated processes loading the changed modules over the deployed staging image, not a deployment of the complete PR image. No production mutation or deployment was performed. Wallet-conflict checks are not successful topup/payment-flow validation.

## Remaining validation limits

- Full-image deployment, startup/shutdown lifecycle, browser flows, successful topup and payment callbacks were not exercised in the staging run.
- No-entitlement/no-credit behavior and transport-fault paths have unit/local fault-injection evidence, not complete live failure scenarios.
- The shared GET pool retains default capacity (100 total / 20 keepalive); production peak capacity and CPU improvements remain unmeasured. The staging concurrency sample is not a performance benchmark.
- Cross-process deduplication, progressive recovery intervals, incremental thread reads and request-scoped read deduplication remain outside scope.

Deploy `claw-interface` after merge. New-commit CI and review results are authoritative and must settle before merge.


---

## fix(billing): unblock legacy agent data and models after expiry (#3894)

- **SHA**: `2d46a3f55616f053589b36cd72b8e793813f580e`
- **作者**: sam-srp
- **日期**: 2026-09-24T03:11:33Z
- **PR**: #3894

### Commit Message

```
fix(billing): unblock legacy agent data and models after expiry (#3894)

## Summary
- 个人订阅过期后，旧 Agent 的归档聊天、成果列表/详情/删除和工作区文件访问不再要求有效订阅，也不额外要求余额。
- 旧 Agent 的模型设置读取、单独修改模型及旧版主模型接口移除订阅前置限制，继续使用现有积分驱动的模型目录校验。
- 保留账号、组织、工作区/Computer 归属、路径校验及 runtime 就绪检查。共享 helper
默认仍校验订阅，其他运行操作和身份设置修改不在此次放开范围。

## Root cause
旧接口复用的 bot/token 与 ready-bot helper
在查询资源前统一检查订阅有效性，因此即使用户有充值积分，仍会被旧订阅门禁提前拦截。为明确的已有数据/模型入口增加显式选择，避免全局放开共享
helper。

## Test plan
- [x] 512 个相关 pytest 测试通过，覆盖旧模型、成果、归档、共享 helper 与原有 runtime 门禁。
- [x] 新增回归使用真实 helper，验证订阅不满足时仍能读写目标数据，并验证其他用户的 Computer 不可访问、未知模型仍拒绝。
- [x] Ruff、格式、Pyright、import-linter 及提交 hooks 通过。
- [ ] staging/production 实际账号验证；尚未部署。本次只需发布后端。
```

### PR Body

## Summary
- 个人订阅过期后，旧 Agent 的归档聊天、成果列表/详情/删除和工作区文件访问不再要求有效订阅，也不额外要求余额。
- 旧 Agent 的模型设置读取、单独修改模型及旧版主模型接口移除订阅前置限制，继续使用现有积分驱动的模型目录校验。
- 保留账号、组织、工作区/Computer 归属、路径校验及 runtime 就绪检查。共享 helper 默认仍校验订阅，其他运行操作和身份设置修改不在此次放开范围。

## Root cause
旧接口复用的 bot/token 与 ready-bot helper 在查询资源前统一检查订阅有效性，因此即使用户有充值积分，仍会被旧订阅门禁提前拦截。为明确的已有数据/模型入口增加显式选择，避免全局放开共享 helper。

## Test plan
- [x] 512 个相关 pytest 测试通过，覆盖旧模型、成果、归档、共享 helper 与原有 runtime 门禁。
- [x] 新增回归使用真实 helper，验证订阅不满足时仍能读写目标数据，并验证其他用户的 Computer 不可访问、未知模型仍拒绝。
- [x] Ruff、格式、Pyright、import-linter 及提交 hooks 通过。
- [ ] staging/production 实际账号验证；尚未部署。本次只需发布后端。


---

## fix(agents): 统一提示卡片样式与预填交互，优化滚动条和更新加载态 (#3887)

- **SHA**: `e3cb70bd5d558c75efb575b7bf17947511a27dc0`
- **作者**: lynn Zhuang
- **日期**: 2026-09-24T03:00:55Z
- **PR**: #3887

### Commit Message

```
fix(agents): 统一提示卡片样式与预填交互，优化滚动条和更新加载态 (#3887)

## Summary
统一 Agent 的 Quick Command 和 Edit Agent 提示卡片样式与交互，并修复更新按钮加载时导致列表跳动的问题。

- 提示卡片使用白底、浅灰描边、15px 灰色文字和柔和 hover 阴影，添加右下箭头。
- 卡片高度随内容自适应，最多展示两行并省略；只有一张卡片时居中，多张保持两列。
- 点击 Quick Command 或 Edit Agent 建议先将完整提示词填入输入框并聚焦，允许编辑后手动发送。
- 输入框复用聊天会话的细浅灰滚动条，悬停或聚焦时显示。
- 更新按钮加载时保留原有宽高，只显示居中旋转图标，保留无障碍状态和重复提交保护。
- 增加可选 mock 预览：长中文提示词，以及 4 秒更新加载状态，便于重复验收。

## Root cause
原提示卡片字号、布局和点击行为不统一，点击即发送不便修改；固定高度造成短文本卡片多余留白。更新按钮把文案替换为更长的加载文字，导致按钮宽度变化。

## Test plan
- [x] 6 个相关测试文件共 151 项测试通过，覆盖提示词预填、编辑后手动发送、禁用状态及更新流程。
- [x] TypeScript、ESLint、仓库前端治理检查。
- [x] 本地 mock 预览，按用户反馈调整卡片、滚动条和 loading 效果。
- [x] `git diff --check` 和 mock 脚本语法检查。
```

### PR Body

## Summary
统一 Agent 的 Quick Command 和 Edit Agent 提示卡片样式与交互，并修复更新按钮加载时导致列表跳动的问题。

- 提示卡片使用白底、浅灰描边、15px 灰色文字和柔和 hover 阴影，添加右下箭头。
- 卡片高度随内容自适应，最多展示两行并省略；只有一张卡片时居中，多张保持两列。
- 点击 Quick Command 或 Edit Agent 建议先将完整提示词填入输入框并聚焦，允许编辑后手动发送。
- 输入框复用聊天会话的细浅灰滚动条，悬停或聚焦时显示。
- 更新按钮加载时保留原有宽高，只显示居中旋转图标，保留无障碍状态和重复提交保护。
- 增加可选 mock 预览：长中文提示词，以及 4 秒更新加载状态，便于重复验收。

## Root cause
原提示卡片字号、布局和点击行为不统一，点击即发送不便修改；固定高度造成短文本卡片多余留白。更新按钮把文案替换为更长的加载文字，导致按钮宽度变化。

## Test plan
- [x] 6 个相关测试文件共 151 项测试通过，覆盖提示词预填、编辑后手动发送、禁用状态及更新流程。
- [x] TypeScript、ESLint、仓库前端治理检查。
- [x] 本地 mock 预览，按用户反馈调整卡片、滚动条和 loading 效果。
- [x] `git diff --check` 和 mock 脚本语法检查。


---

## feat(billing): support Stripe promotion codes for Pro subscriptions (#3891)

- **SHA**: `896730f7f50c5405a81d5ab5af2918596643a233`
- **作者**: sam-srp
- **日期**: 2026-09-24T02:54:58Z
- **PR**: #3891

### Commit Message

```
feat(billing): support Stripe promotion codes for Pro subscriptions (#3891)

## Summary
Pro subscription Checkout now accepts Stripe promotion codes and always
collects a payment method for automatic renewal. Stripe controls code
eligibility, discount amount and duration; there is no local code
issuance or first-period restriction.

The monthly fulfillment path reads and validates the paid Stripe
invoice, records its actual paid amount, discount and customer invoice
balance evidence, and grants the full Pro entitlement for partial or
full discounts, including $0 invoices settled entirely by discounts
and/or customer balance without a PaymentIntent. Zero-amount grants
remain restricted to verified current-policy Pro subscription invoices.
Existing period-based fulfillment protects against duplicate
invoice/Checkout delivery. Financial audit events retain before/after
amounts, discounts, balance offsets and invoice/subscription identities,
including the actual prior row after a duplicate-insert race.

Topups, legacy payment flows and billing-gateway are unchanged. No new
environment variables, queries or scheduled jobs. Coupons and Promotion
Codes must be created in the intended Stripe account/environment.
Customer invoice balance supports partial/full offsets, surplus balance,
discount combinations and fully paid debit balances. Paid minimum-charge
deferrals are accepted only after a read-only Stripe query verifies the
unique invoice_too_small transaction for the same
invoice/customer/currency/environment. Deferred amounts and transaction
IDs are audited separately from discounts and balance consumption.
Cancellation does not trigger extra local collection: the debit stays in
Stripe for future applicable invoices, and may remain uncollected if no
further invoice is issued. Tax and current-invoice credit notes remain
outside the supported invoice contract.

## Test plan
- [x] 324 related unit tests passed, including full/partial/recurring
discounts, legacy/modern Stripe invoice shapes, $0 entitlement guards,
Checkout and invoice replay, cancellation periods, renewal, topup
isolation, customer balance reconciliation and durable financial audit
snapshots, small-amount carry-forward proof, rejected/ambiguous
evidence, pagination, query failures, cancellation and next-period
collection.
- [x] Backend pre-commit checks passed, including Ruff, Pyright, import
contracts, file size and complexity.
- [ ] Stripe Sandbox end-to-end acceptance: actual code redemption, $0
payment-method collection, customer balance offsets, minimum-charge
deferrals, renewal and cancellation. Not deployed by this PR.
```

### PR Body

## Summary
Pro subscription Checkout now accepts Stripe promotion codes and always collects a payment method for automatic renewal. Stripe controls code eligibility, discount amount and duration; there is no local code issuance or first-period restriction.

The monthly fulfillment path reads and validates the paid Stripe invoice, records its actual paid amount, discount and customer invoice balance evidence, and grants the full Pro entitlement for partial or full discounts, including $0 invoices settled entirely by discounts and/or customer balance without a PaymentIntent. Zero-amount grants remain restricted to verified current-policy Pro subscription invoices. Existing period-based fulfillment protects against duplicate invoice/Checkout delivery. Financial audit events retain before/after amounts, discounts, balance offsets and invoice/subscription identities, including the actual prior row after a duplicate-insert race.

Topups, legacy payment flows and billing-gateway are unchanged. No new environment variables, queries or scheduled jobs. Coupons and Promotion Codes must be created in the intended Stripe account/environment. Customer invoice balance supports partial/full offsets, surplus balance, discount combinations and fully paid debit balances. Paid minimum-charge deferrals are accepted only after a read-only Stripe query verifies the unique invoice_too_small transaction for the same invoice/customer/currency/environment. Deferred amounts and transaction IDs are audited separately from discounts and balance consumption. Cancellation does not trigger extra local collection: the debit stays in Stripe for future applicable invoices, and may remain uncollected if no further invoice is issued. Tax and current-invoice credit notes remain outside the supported invoice contract.

## Test plan
- [x] 324 related unit tests passed, including full/partial/recurring discounts, legacy/modern Stripe invoice shapes, $0 entitlement guards, Checkout and invoice replay, cancellation periods, renewal, topup isolation, customer balance reconciliation and durable financial audit snapshots, small-amount carry-forward proof, rejected/ambiguous evidence, pagination, query failures, cancellation and next-period collection.
- [x] Backend pre-commit checks passed, including Ruff, Pyright, import contracts, file size and complexity.
- [ ] Stripe Sandbox end-to-end acceptance: actual code redemption, $0 payment-method collection, customer balance offsets, minimum-charge deferrals, renewal and cancellation. Not deployed by this PR.




---

## fix(auth): remove China +86 option while retaining SMS login (#3892)

- **SHA**: `6b5cc7aa3bcb9c5b82cba19d6d69a391dfc637c9`
- **作者**: tim-srp
- **日期**: 2026-09-24T02:42:31Z
- **PR**: #3892

### Commit Message

```
fix(auth): remove China +86 option while retaining SMS login (#3892)

## Confirmed requirement / 已确认需求

**本次仅从手机号注册／登录的国家或地区列表中移除中国大陆 +86 选项。保留其他国家／地区的手机号登录和短信验证。不是移除全部 SMS
登录。**

This PR removes only the China (+86) country-code option. Retaining the
phone entry, phone form, and SMS verification for the remaining
countries is explicitly required.

## Scope

The shared `LoginForm` applies this change to all three web surfaces:

- Standalone `/login` page.
- Landing-page login modal.
- In-product login modal.

Remove the +86 option, its country-code mapping, and its now-unused
China-specific validation branch. Keep the existing United States,
Canada, Mexico, India, Philippines, Vietnam, and South Korea options.

Phone buttons, SMS/reCAPTCHA handling, verification handoff, styles, and
translations remain available. Email and Google login are unchanged.
This is a frontend selector change, not a backend-wide restriction on
+86 numbers. `/user/verify`, BossClaw login, and backend authentication
are outside this change.

## Review clarification

The earlier description proposing removal of all phone/SMS login was
based on a misunderstanding and is superseded by the confirmed
requirement above.

The finding titled “[P1] 完成 PR 所述的 SMS 登录移除” assumes that earlier scope.
Its observation that phone buttons and `sendSMSVerification` remain is
correct, but that behavior is intentional and required. Removing all
phone login would violate the confirmed requirement. Regression tests
therefore assert that phone login remains available while the country
selector excludes +86.

## Validation

- 70 LoginForm unit tests passed, covering retained SMS behavior and the
country options in both shared form variants.
- TypeScript, ESLint, and frontend governance checks passed.
- All three surfaces were manually checked in the local mock preview:
phone login is present and the country list excludes +86.
- Real SMS delivery was not tested in the mock environment.

---------

Co-authored-by: Claude Code <noreply@anthropic.com>
```

### PR Body

## Confirmed requirement / 已确认需求

**本次仅从手机号注册／登录的国家或地区列表中移除中国大陆 +86 选项。保留其他国家／地区的手机号登录和短信验证。不是移除全部 SMS 登录。**

This PR removes only the China (+86) country-code option. Retaining the phone entry, phone form, and SMS verification for the remaining countries is explicitly required.

## Scope

The shared `LoginForm` applies this change to all three web surfaces:

- Standalone `/login` page.
- Landing-page login modal.
- In-product login modal.

Remove the +86 option, its country-code mapping, and its now-unused China-specific validation branch. Keep the existing United States, Canada, Mexico, India, Philippines, Vietnam, and South Korea options.

Phone buttons, SMS/reCAPTCHA handling, verification handoff, styles, and translations remain available. Email and Google login are unchanged. This is a frontend selector change, not a backend-wide restriction on +86 numbers. `/user/verify`, BossClaw login, and backend authentication are outside this change.

## Review clarification

The earlier description proposing removal of all phone/SMS login was based on a misunderstanding and is superseded by the confirmed requirement above.

The finding titled “[P1] 完成 PR 所述的 SMS 登录移除” assumes that earlier scope. Its observation that phone buttons and `sendSMSVerification` remain is correct, but that behavior is intentional and required. Removing all phone login would violate the confirmed requirement. Regression tests therefore assert that phone login remains available while the country selector excludes +86.

## Validation

- 70 LoginForm unit tests passed, covering retained SMS behavior and the country options in both shared form variants.
- TypeScript, ESLint, and frontend governance checks passed.
- All three surfaces were manually checked in the local mock preview: phone login is present and the country list excludes +86.
- Real SMS delivery was not tested in the mock environment.


---
