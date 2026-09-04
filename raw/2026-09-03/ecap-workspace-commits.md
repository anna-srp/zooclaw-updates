# SerendipityOneInc/ecap-workspace — commits 2026-09-03

## feat(chat): show delegated work progress (#3640)

- **SHA**: `84e12b5872281dc4b72457262e7809edf23d3e56`
- **作者**: kaka-srp
- **日期**: 2026-09-03T13:41:54Z
- **PR**: #3640

### Commit Message

```
feat(chat): show delegated work progress (#3640)

## Linear

Not applicable — requested without a Linear issue.

## Summary

- document the complete v2 Engine → ACS channel delivery → Web rendering
design
- render delegated child work as a dedicated progress group with
running, attention, completed, and elapsed states
- expand long child-task details inline in the conversation instead of
inside a small nested scroll box
- keep status summaries internally consistent by counting only tasks in
the displayed priority state
- add English/Chinese copy and parser/rendering regression coverage

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] Web parser and locale tests (59 tests)
- [x] `@zooclaw/chat-ui` tests (61 tests), typecheck, and lint
- [x] local Web + local ACS + local Engine end-to-end acceptance with a
staging account and live child Agent progress

## Companion changes

- Engine producer:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1146
- Agent Channel Service contract coverage:
https://github.com/SerendipityOneInc/agent-channel-service/pull/112
```

### PR Body

## Linear

Not applicable — requested without a Linear issue.

## Summary

- document the complete v2 Engine → ACS channel delivery → Web rendering design
- render delegated child work as a dedicated progress group with running, attention, completed, and elapsed states
- expand long child-task details inline in the conversation instead of inside a small nested scroll box
- keep status summaries internally consistent by counting only tasks in the displayed priority state
- add English/Chinese copy and parser/rendering regression coverage

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] Web parser and locale tests (59 tests)
- [x] `@zooclaw/chat-ui` tests (61 tests), typecheck, and lint
- [x] local Web + local ACS + local Engine end-to-end acceptance with a staging account and live child Agent progress

## Companion changes

- Engine producer: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1146
- Agent Channel Service contract coverage: https://github.com/SerendipityOneInc/agent-channel-service/pull/112


---

## docs(analytics): define GA4 v2 tracking (#3626)

- **SHA**: `fc3a5f98c0dfcd33aca9d5b7655671013827467f`
- **作者**: winston-srp
- **日期**: 2026-09-03T11:54:15Z
- **PR**: #3626

### Commit Message

```
docs(analytics): define GA4 v2 tracking (#3626)

## Linear

N/A

## Summary

- 新增 GA4 V2 跨端埋点语义规范，定义 Event、字段、Flow/Operation、Page
Context、隐私边界、no-throw 要求和外部管道约束。
- 新增 Web V2 开发与迁移清单，按埋点粒度记录现有实现、升级动作、触发时机和验收要求。
- 在 `web/AGENTS.md` 增加埋点开发与 Review 入口：修改或审查 Web Tracking 前必须阅读语义规范和 Web
实施清单。
- 文档作为统一 Web 实现 PR #3625 的需求基线；iOS 和外部 Tips 仓库的运行时代码不在本 PR 范围内。

## Test plan

- [x] `git diff --check`
- [x] PR 体量检查通过：3 个文件，1,422 行
- [x] 两份文档已与 Web 实现逐项核对 Event、Flow/Operation、异步结果、Card 业务 UUID、no-throw
和外部管道边界

## Scope and side effects

- 仅修改规范、开发清单和 Agent 开发指引，不修改 runtime、API 或存储。
- Web 埋点编码和 Code Review 必须以 `docs/data/ga4_tracking_spec.md` 为语义基线，并以
`docs/data/ga4_event_tracking_web_v2.md` 核对调用点和迁移动作。
- Tracking `operation_id` 只用于埋点关联；Card API 的业务 `operation_id` 独立生成
UUID4，二者不互相降级。
```

### PR Body

## Linear

N/A

## Summary

- 新增 GA4 V2 跨端埋点语义规范，定义 Event、字段、Flow/Operation、Page Context、隐私边界、no-throw 要求和外部管道约束。
- 新增 Web V2 开发与迁移清单，按埋点粒度记录现有实现、升级动作、触发时机和验收要求。
- 在 `web/AGENTS.md` 增加埋点开发与 Review 入口：修改或审查 Web Tracking 前必须阅读语义规范和 Web 实施清单。
- 文档作为统一 Web 实现 PR #3625 的需求基线；iOS 和外部 Tips 仓库的运行时代码不在本 PR 范围内。

## Test plan

- [x] `git diff --check`
- [x] PR 体量检查通过：3 个文件，1,422 行
- [x] 两份文档已与 Web 实现逐项核对 Event、Flow/Operation、异步结果、Card 业务 UUID、no-throw 和外部管道边界

## Scope and side effects

- 仅修改规范、开发清单和 Agent 开发指引，不修改 runtime、API 或存储。
- Web 埋点编码和 Code Review 必须以 `docs/data/ga4_tracking_spec.md` 为语义基线，并以 `docs/data/ga4_event_tracking_web_v2.md` 核对调用点和迁移动作。
- Tracking `operation_id` 只用于埋点关联；Card API 的业务 `operation_id` 独立生成 UUID4，二者不互相降级。


---

## feat(analytics): upgrade GA4 v2 web event tracking (#3625)

- **SHA**: `4bb87a9a92c9724392d66328ac07df8baca72bc7`
- **作者**: winston-srp
- **日期**: 2026-09-03T11:39:59Z
- **PR**: #3625

### Commit Message

```
feat(analytics): upgrade GA4 v2 web event tracking (#3625)

## Linear

N/A

## Summary

- upgrade Web Page, authentication, message submission, Agent
installation, Plan Management, Checkout, and Purchase tracking to the
GA4 V2 contract
- add the shared typed V2 sender, filtered Page Context, Flow/Operation
correlation, stable Object projection, and HTTP result fields for
asynchronous business events
- remove the retired `signup_started` write contract and Signup
Attribution snapshot chain while retaining read compatibility for active
legacy Auth Contexts
- keep Tracking fail-soft and isolated from authentication, messaging,
installation, payment, navigation, and storage behavior

The semantic and implementation documents are isolated in #3626. iOS is
intentionally outside this implementation.

## Tracking privacy and value policy

This cutover intentionally identifies PII only by the registered source
or Query Key. Tracking does not infer PII or business validity from a
Value's shape, including email-like, phone-like, numeric, URL-like,
title, ID, or display-name content. Business producers own value
legality; the Tracking boundary only applies the registered Event/field
projection, primitive type checks, and GA4 transport limits.

Unknown Query Keys remain available for current and future attribution
unless they match the sensitive Key Registry. This is a best-effort
compatibility policy and accepts the documented residual risk that an
unknown Key may carry personal-looking content. Registered `object_name`
values, including Agent display names, are collected; `object_id`
remains the association key.

## Size override

This PR has 6,948 changed lines (+3,134 / -3,814; net -680) across 85
files after repository exclusions and carries the `size-override` label.
Of those changes, business code is +1,719 / -1,311 (net +408) and test
code is +1,415 / -2,503 (net -1,088).

The code is intentionally released as one Web Cutover because the shared
sender, Page Context, authentication Flow, and downstream business
producers must switch to the same Event version and field contract
together. Splitting those runtime layers would create deployable
intermediate states in which producers and the shared Tracking boundary
use different protocols. Documentation remains separate in #3626, while
tests stay beside the code they protect.

## Validation

- `bash scripts/verify-local.sh --changed` passed: repository guards,
TypeScript, and ESLint
- latest Auth/Plan Flow, Checkout, Agent-install, messaging, and
Tracking regression set passed: 13 files / 445 tests
- Agent Catalog and Agent Detail integration tests passed after the
explicit user-confirmation contract update: 2 files / 102 tests
- retired Signup Attribution/V1 Auth-state cleanup regression set
passed: 8 files / 267 tests
- Checkout Operation guard, terminal-failure cleanup, resumed
Agent-install, payment return, and Plan Snapshot regression set passed:
5 files / 125 tests
- Plan Controller public-lifecycle and V2 authentication diagnostic
regression set passed: 2 files / 29 tests
- Auth and Plan Flow scenarios validated with the local mock backend
- Staging validated Landing UTM/sensitive-Key filtering, a real message
send, and a real Agent installation
- GA4 network calls for `send_message(success, 200)` and
`add_agent(success, 200)` returned 204 and reused the request
`operation_id`
- live Plan Gate validation emitted `flow_start(event_version=2.0.0,
flow_type=plan_management, trigger=gift_paywall_click)` and GA4 returned
204
- SPA Page View testing found and fixed SDK fallback to an unsafe raw
Referrer by explicitly sending empty Page-field clear instructions
- after merging current `main`, all 32 changed test files passed locally
(907/907); repository guards, TypeScript, and ESLint also passed
- GitHub CI passed 42/42 checks at HEAD `5c5e0bed5`, including Web
tests, build, lint/typecheck, CodeQL, and automated reviews

## Cutover prerequisites

- disable GA4 Enhanced Measurement browser-history Page Views for the
target Data Stream and verify that each Navigation Fact produces only
the manual V2 `page_view`
- disable GA4 Enhanced Measurement Site Search and verify that URLs
containing `q` do not produce `view_search_results/search_term`
- local Staging network inspection confirmed that both automatic
settings are currently still enabled; the application code cannot
disable these Data Stream settings with `send_page_view:false`

## Scope and side effects

- Web tracking and tests only
- no backend API or business-data schema changes
- no authentication, request, retry, navigation, installation, payment,
or entitlement behavior changes
- no iOS implementation
- no documentation files; they are reviewed separately in #3626
- Staging sandbox validation created one test message and installed the
Oura Ring Agent
```

### PR Body

## Linear

N/A

## Summary

- upgrade Web Page, authentication, message submission, Agent installation, Plan Management, Checkout, and Purchase tracking to the GA4 V2 contract
- add the shared typed V2 sender, filtered Page Context, Flow/Operation correlation, stable Object projection, and HTTP result fields for asynchronous business events
- remove the retired `signup_started` write contract and Signup Attribution snapshot chain while retaining read compatibility for active legacy Auth Contexts
- keep Tracking fail-soft and isolated from authentication, messaging, installation, payment, navigation, and storage behavior

The semantic and implementation documents are isolated in #3626. iOS is intentionally outside this implementation.

## Tracking privacy and value policy

This cutover intentionally identifies PII only by the registered source or Query Key. Tracking does not infer PII or business validity from a Value's shape, including email-like, phone-like, numeric, URL-like, title, ID, or display-name content. Business producers own value legality; the Tracking boundary only applies the registered Event/field projection, primitive type checks, and GA4 transport limits.

Unknown Query Keys remain available for current and future attribution unless they match the sensitive Key Registry. This is a best-effort compatibility policy and accepts the documented residual risk that an unknown Key may carry personal-looking content. Registered `object_name` values, including Agent display names, are collected; `object_id` remains the association key.

## Size override

This PR has 6,948 changed lines (+3,134 / -3,814; net -680) across 85 files after repository exclusions and carries the `size-override` label. Of those changes, business code is +1,719 / -1,311 (net +408) and test code is +1,415 / -2,503 (net -1,088).

The code is intentionally released as one Web Cutover because the shared sender, Page Context, authentication Flow, and downstream business producers must switch to the same Event version and field contract together. Splitting those runtime layers would create deployable intermediate states in which producers and the shared Tracking boundary use different protocols. Documentation remains separate in #3626, while tests stay beside the code they protect.

## Validation

- `bash scripts/verify-local.sh --changed` passed: repository guards, TypeScript, and ESLint
- latest Auth/Plan Flow, Checkout, Agent-install, messaging, and Tracking regression set passed: 13 files / 445 tests
- Agent Catalog and Agent Detail integration tests passed after the explicit user-confirmation contract update: 2 files / 102 tests
- retired Signup Attribution/V1 Auth-state cleanup regression set passed: 8 files / 267 tests
- Checkout Operation guard, terminal-failure cleanup, resumed Agent-install, payment return, and Plan Snapshot regression set passed: 5 files / 125 tests
- Plan Controller public-lifecycle and V2 authentication diagnostic regression set passed: 2 files / 29 tests
- Auth and Plan Flow scenarios validated with the local mock backend
- Staging validated Landing UTM/sensitive-Key filtering, a real message send, and a real Agent installation
- GA4 network calls for `send_message(success, 200)` and `add_agent(success, 200)` returned 204 and reused the request `operation_id`
- live Plan Gate validation emitted `flow_start(event_version=2.0.0, flow_type=plan_management, trigger=gift_paywall_click)` and GA4 returned 204
- SPA Page View testing found and fixed SDK fallback to an unsafe raw Referrer by explicitly sending empty Page-field clear instructions
- after merging current `main`, all 32 changed test files passed locally (907/907); repository guards, TypeScript, and ESLint also passed
- GitHub CI passed 42/42 checks at HEAD `5c5e0bed5`, including Web tests, build, lint/typecheck, CodeQL, and automated reviews

## Cutover prerequisites

- disable GA4 Enhanced Measurement browser-history Page Views for the target Data Stream and verify that each Navigation Fact produces only the manual V2 `page_view`
- disable GA4 Enhanced Measurement Site Search and verify that URLs containing `q` do not produce `view_search_results/search_term`
- local Staging network inspection confirmed that both automatic settings are currently still enabled; the application code cannot disable these Data Stream settings with `send_page_view:false`

## Scope and side effects

- Web tracking and tests only
- no backend API or business-data schema changes
- no authentication, request, retry, navigation, installation, payment, or entitlement behavior changes
- no iOS implementation
- no documentation files; they are reviewed separately in #3626
- Staging sandbox validation created one test message and installed the Oura Ring Agent


---

## docs(architecture): engine-backed agents 已上生产，去掉 staging-only 表述 (#3641)

- **SHA**: `b6c34675798c5ecc08d2f34fca889e281e1b9cdc`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-03T09:29:34Z
- **PR**: #3641

### Commit Message

```
docs(architecture): engine-backed agents 已上生产，去掉 staging-only 表述 (#3641)

## 改了什么

`architecture.md` 和 `architecture.zh-CN.md` 各 6 处：把 engine-backed
agents（v2）"staging-only / 目前仅 staging" 改为"已在生产与 staging 启用，由
`AGENTS_V2_ENABLED` 控制；新建 agent 默认走 v2，`AGENTS_V1_ONLY_UIDS`
是临时例外名单"。小节标题去掉 "staging"，第 13 行的锚点同步改为 `#engine-backed-agents-v2` /
`#engine-backed-agentv2`。

## 为什么

- v2 自 #3525（2026-08-26）起是默认 runtime，iOS 已切
v2（#3526），`agents_v2_access.py` 只剩 `AGENTS_V1_ONLY_UIDS` 例外。
- zooclaw-engine `v0.1.21-release` 已部署
production，`production-full-smoke` 2026-09-03 通过。
- 这段过期表述是 zooclaw-engine 文档审计机器人的证据源，它据此把 capability-status 里 8 项能力误降为
Not production-wired（zooclaw-engine#1131）。不改根源，机器人会反复生成同样的降级 PR。

对应 zooclaw-engine 生产上线计划 §4 "文档联动：architecture.md 四处 staging-only 随本节 PR
翻转"。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01Q4ZrEupV7DRiTeDEH57uip
```

### PR Body

## 改了什么

`architecture.md` 和 `architecture.zh-CN.md` 各 6 处：把 engine-backed agents（v2）"staging-only / 目前仅 staging" 改为"已在生产与 staging 启用，由 `AGENTS_V2_ENABLED` 控制；新建 agent 默认走 v2，`AGENTS_V1_ONLY_UIDS` 是临时例外名单"。小节标题去掉 "staging"，第 13 行的锚点同步改为 `#engine-backed-agents-v2` / `#engine-backed-agentv2`。

## 为什么

- v2 自 #3525（2026-08-26）起是默认 runtime，iOS 已切 v2（#3526），`agents_v2_access.py` 只剩 `AGENTS_V1_ONLY_UIDS` 例外。
- zooclaw-engine `v0.1.21-release` 已部署 production，`production-full-smoke` 2026-09-03 通过。
- 这段过期表述是 zooclaw-engine 文档审计机器人的证据源，它据此把 capability-status 里 8 项能力误降为 Not production-wired（zooclaw-engine#1131）。不改根源，机器人会反复生成同样的降级 PR。

对应 zooclaw-engine 生产上线计划 §4 "文档联动：architecture.md 四处 staging-only 随本节 PR 翻转"。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01Q4ZrEupV7DRiTeDEH57uip


---

## fix(billing): refresh expiring Airwallex checkout links (#3639)

- **SHA**: `f5cb9e02deda6836c3c17ad6043fc2f08e065fd8`
- **作者**: tim-srp
- **日期**: 2026-09-03T09:05:25Z
- **PR**: #3639

### Commit Message

```
fix(billing): refresh expiring Airwallex checkout links (#3639)

## Summary

- Decode the Airwallex Checkout URL JWT expiry without adding a
persisted field.
- Reuse a pending Checkout only when it remains valid beyond a
five-minute safety window.
- Safely cancel an active non-reusable Checkout before retiring its
local order and creating a replacement.
- Preserve manual-review and concurrency fences when provider outcomes
are ambiguous.

## Root cause

The enterprise vertical-package flow replayed every pending URL on an
official Airwallex host without checking the JWT `exp`. A local order
could remain pending after the provider URL expired, so later purchase
attempts repeatedly received the same unusable link.

## Test plan

- [x] `pytest tests/unit/test_airwallex_enterprise_checkout.py -q` — 45
passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
```

### PR Body

## Summary

- Decode the Airwallex Checkout URL JWT expiry without adding a persisted field.
- Reuse a pending Checkout only when it remains valid beyond a five-minute safety window.
- Safely cancel an active non-reusable Checkout before retiring its local order and creating a replacement.
- Preserve manual-review and concurrency fences when provider outcomes are ambiguous.

## Root cause

The enterprise vertical-package flow replayed every pending URL on an official Airwallex host without checking the JWT `exp`. A local order could remain pending after the provider URL expired, so later purchase attempts repeatedly received the same unusable link.

## Test plan

- [x] `pytest tests/unit/test_airwallex_enterprise_checkout.py -q` — 45 passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`


---

## fix(sidenav): replace asleep state with paused (#3634)

- **SHA**: `1fa96b521cbe82812e7548c4e0b3f9202d8d6bca`
- **作者**: shana-srp
- **日期**: 2026-09-03T07:34:50Z
- **PR**: #3634

### Commit Message

```
fix(sidenav): replace asleep state with paused (#3634)

## Summary

- replace the customer-facing `Asleep` / sleeping metaphor with the
clearer B2B status `Paused` across the sidebar, account menu, credits,
and chat gate copy
- swap the custom Zzz icon for Heroicons' pause-circle and use the
existing warning semantic color instead of a neutral or destructive
state
- explain on hover or keyboard focus that agents are paused while
memories and data remain safely preserved, with matching accessible text
and localized copy in all 10 locales
- open the subscription recovery panel directly from the paused profile
card while keeping the arrow button as the account-menu control

## Testing

- `pnpm exec vitest run tests/unit/components/UserCard.unit.spec.tsx
tests/unit/components/UserMenu.unit.spec.tsx
tests/unit/components/credits/CreditsDisplay.unit.spec.tsx` (123 passed)
- `bash scripts/verify-web.sh` (TypeScript and ESLint passed; the full
unit run reported only a sandbox `listen EPERM` in the mock-backend
socket test)
- `pnpm exec vitest run
tests/unit/scripts/mock-backend-agent-builder.unit.spec.ts` outside the
socket-restricted sandbox (34 passed)
- `bash scripts/verify-changed.sh`
- local browser verification that clicking the paused card opens the
subscription panel and leaves the account menu closed

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary

- replace the customer-facing `Asleep` / sleeping metaphor with the clearer B2B status `Paused` across the sidebar, account menu, credits, and chat gate copy
- swap the custom Zzz icon for Heroicons' pause-circle and use the existing warning semantic color instead of a neutral or destructive state
- explain on hover or keyboard focus that agents are paused while memories and data remain safely preserved, with matching accessible text and localized copy in all 10 locales
- open the subscription recovery panel directly from the paused profile card while keeping the arrow button as the account-menu control

## Testing

- `pnpm exec vitest run tests/unit/components/UserCard.unit.spec.tsx tests/unit/components/UserMenu.unit.spec.tsx tests/unit/components/credits/CreditsDisplay.unit.spec.tsx` (123 passed)
- `bash scripts/verify-web.sh` (TypeScript and ESLint passed; the full unit run reported only a sandbox `listen EPERM` in the mock-backend socket test)
- `pnpm exec vitest run tests/unit/scripts/mock-backend-agent-builder.unit.spec.ts` outside the socket-restricted sandbox (34 passed)
- `bash scripts/verify-changed.sh`
- local browser verification that clicking the paused card opens the subscription panel and leaves the account menu closed


---

## fix(auth): honor personal org region for email login (#3633)

- **SHA**: `f2254e5657bd697a20b3c20b5bf76b0e78d40052`
- **作者**: sam-srp
- **日期**: 2026-09-03T07:34:30Z
- **PR**: #3633

### Commit Message

```
fix(auth): honor personal org region for email login (#3633)

## Summary
- keep active Team Org email login eligibility unchanged regardless of
region
- let Personal Org users authenticate using an explicitly configured
non-CN `region_code`
- fall back to normalized `cf-ipcountry` when no authoritative
personal-org region exists, and fail closed when the IP country is
missing or invalid
- pass the request IP country through the Web email-OTP BFF to
`claw-interface`
- preserve login behavior against the previous strict backend schema
during a staggered Web/backend rollout
- constrain AnyIO below 4.15 until the pinned Starlette version stops
importing its newly deprecated alias

## Root cause
The existing Web route only called the eligibility service for
`cf-ipcountry=CN`, while the backend only accepted active Team Orgs.
This ignored the authoritative region already stored on Personal Orgs
and allowed a missing country header to bypass regional eligibility
checks.

## Test plan
- [x] `pytest -q tests/unit/test_domestic_access.py
tests/unit/test_domestic_access_routes.py` (23 passed)
- [x] `bash scripts/verify-web.sh
web/app/src/app/api/auth/email-otp/send/route.ts
web/app/src/lib/auth/domestic-access-bff.ts
web/app/tests/unit/app/api/auth-routes.unit.spec.ts` (12 files, 91 tests
passed)
- [x] rollout compatibility tests for legacy CN, non-CN, and
unknown-country eligibility paths (19 focused route tests passed)
- [x] Ruff check/format, targeted Pyright for all changed Python files,
and import-linter contracts
- [ ] Full local Pyright is blocked by an existing environment-dependent
type error in unchanged `app/connectors/google.py:131`; CI will run in
the repository-pinned environment
```

### PR Body

## Summary
- keep active Team Org email login eligibility unchanged regardless of region
- let Personal Org users authenticate using an explicitly configured non-CN `region_code`
- fall back to normalized `cf-ipcountry` when no authoritative personal-org region exists, and fail closed when the IP country is missing or invalid
- pass the request IP country through the Web email-OTP BFF to `claw-interface`
- preserve login behavior against the previous strict backend schema during a staggered Web/backend rollout
- constrain AnyIO below 4.15 until the pinned Starlette version stops importing its newly deprecated alias

## Root cause
The existing Web route only called the eligibility service for `cf-ipcountry=CN`, while the backend only accepted active Team Orgs. This ignored the authoritative region already stored on Personal Orgs and allowed a missing country header to bypass regional eligibility checks.

## Test plan
- [x] `pytest -q tests/unit/test_domestic_access.py tests/unit/test_domestic_access_routes.py` (23 passed)
- [x] `bash scripts/verify-web.sh web/app/src/app/api/auth/email-otp/send/route.ts web/app/src/lib/auth/domestic-access-bff.ts web/app/tests/unit/app/api/auth-routes.unit.spec.ts` (12 files, 91 tests passed)
- [x] rollout compatibility tests for legacy CN, non-CN, and unknown-country eligibility paths (19 focused route tests passed)
- [x] Ruff check/format, targeted Pyright for all changed Python files, and import-linter contracts
- [ ] Full local Pyright is blocked by an existing environment-dependent type error in unchanged `app/connectors/google.py:131`; CI will run in the repository-pinned environment

---

## fix(agent-builder): 线程翻页补 fromCreateAt，否则长线程必挂 (#3636)

- **SHA**: `f98a9116997bcef65ab6ecaf28b65c496fc17c1d`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-03T07:32:29Z
- **PR**: #3636

### Commit Message

```
fix(agent-builder): 线程翻页补 fromCreateAt，否则长线程必挂 (#3636)

## 问题

staging 验收 #3606/#3607/#3608 时实测到的：**任何超过一页（200 条）的 Builder 线程，取证端点都读不出
`run_id`**。

Mattermost 11.5.1 对只带 `fromPost` 的线程请求返回 400：

```
{"id":"api.context.invalid_body_param.app_error",
 "message":"Invalid or missing if fromPost is set, then fromCreateAt must also be set in request body.",
 "status_code":400}
```

`_fetch_thread_pages` 第一页不带游标（200 OK），第二页起只传 `fromPost`，于是第二页必然
400，`raise_for_status` 抛 `HTTPStatusError`，整段 `builder_thread` 退化成
`mm_thread_unavailable`。

后果正好打在这段代码要解决的问题上：分页是为了**不在长对话里漏掉 `props.run_id`** 才加的（#3606 的 Codex R1
P1），而端点存在的意义就是从长对话里捞 `run_id`。

## 实测证据

staging 上一个真实 project（553
条线程）：`project`、`workspaces`、`engine_sessions`、`acs_channels` 全部正常填充，唯独
`distinct_run_ids` 为空、`ok=false`、`thread_runs=0`。

在 pod 内对同一个 root post 逐个参数组合探测：

| 参数 | 结果 |
| --- | --- |
| `perPage` + `direction` | HTTP 200，posts=200 |
| `perPage` + `direction` + `fromPost` | **HTTP 400** |
| `perPage` + `fromPost` | **HTTP 400** |
| `fromPost` 单独 | **HTTP 400** |
| `perPage` + `direction` + `fromPost` + `fromCreateAt` | **HTTP
200，posts=201** |

顺带确认了两件此前有争议的事：`perPage` 驼峰是对的（不带分页 553 条，`perPage=200` 正好 200 条），频道与
bot 权限都正常。

## 为什么单测没抓到

MM client 在测试里是 mock 的，永远返回构造好的 payload，看不到真实的 400。同理
`mm_thread_pagination_unsupported` 那条优雅降级也永远走不到——它设计来应对「服务器忽略 `fromPost`
重发第一页」，而真实行为是直接 400。

## 改动

- `get_post_thread` 增加 `from_create_at` →
`fromCreateAt`；并在客户端边界**强制成对**，只给一半直接
`ValueError`。半个游标只会在超过一页的线程上显形，让它在调用点就炸，好过留到线上 400。
- `newest_post_id` → `newest_post_cursor`，返回 `(id, create_at)`
二元组。返回一对而不是分两次取，是为了让两半没有机会在调用点漂移。
- `_fetch_thread_pages` 按对传递游标。

## 回归护栏

- 客户端：钉住 `fromPost`/`fromCreateAt` 同时出现在 wire 上；钉住只给一半会 `ValueError`
且**不发请求**。
- service：钉住翻页 kwargs 序列 `from_create_at == [None, 110]` 与 `from_post ==
[None, "seg_1"]` 逐位对齐。

139 个相关单测本地全绿。

合入后建议重跑一次 staging
验收（`zooclaw-dev/verify-agent-builder-forensics-staging.sh`），对那个 553
条线程确认 `distinct_run_ids` 非空——这个 bug 的性质决定了它只能由真实长线程证伪。
```

### PR Body

## 问题

staging 验收 #3606/#3607/#3608 时实测到的：**任何超过一页（200 条）的 Builder 线程，取证端点都读不出 `run_id`**。

Mattermost 11.5.1 对只带 `fromPost` 的线程请求返回 400：

```
{"id":"api.context.invalid_body_param.app_error",
 "message":"Invalid or missing if fromPost is set, then fromCreateAt must also be set in request body.",
 "status_code":400}
```

`_fetch_thread_pages` 第一页不带游标（200 OK），第二页起只传 `fromPost`，于是第二页必然 400，`raise_for_status` 抛 `HTTPStatusError`，整段 `builder_thread` 退化成 `mm_thread_unavailable`。

后果正好打在这段代码要解决的问题上：分页是为了**不在长对话里漏掉 `props.run_id`** 才加的（#3606 的 Codex R1 P1），而端点存在的意义就是从长对话里捞 `run_id`。

## 实测证据

staging 上一个真实 project（553 条线程）：`project`、`workspaces`、`engine_sessions`、`acs_channels` 全部正常填充，唯独 `distinct_run_ids` 为空、`ok=false`、`thread_runs=0`。

在 pod 内对同一个 root post 逐个参数组合探测：

| 参数 | 结果 |
| --- | --- |
| `perPage` + `direction` | HTTP 200，posts=200 |
| `perPage` + `direction` + `fromPost` | **HTTP 400** |
| `perPage` + `fromPost` | **HTTP 400** |
| `fromPost` 单独 | **HTTP 400** |
| `perPage` + `direction` + `fromPost` + `fromCreateAt` | **HTTP 200，posts=201** |

顺带确认了两件此前有争议的事：`perPage` 驼峰是对的（不带分页 553 条，`perPage=200` 正好 200 条），频道与 bot 权限都正常。

## 为什么单测没抓到

MM client 在测试里是 mock 的，永远返回构造好的 payload，看不到真实的 400。同理 `mm_thread_pagination_unsupported` 那条优雅降级也永远走不到——它设计来应对「服务器忽略 `fromPost` 重发第一页」，而真实行为是直接 400。

## 改动

- `get_post_thread` 增加 `from_create_at` → `fromCreateAt`；并在客户端边界**强制成对**，只给一半直接 `ValueError`。半个游标只会在超过一页的线程上显形，让它在调用点就炸，好过留到线上 400。
- `newest_post_id` → `newest_post_cursor`，返回 `(id, create_at)` 二元组。返回一对而不是分两次取，是为了让两半没有机会在调用点漂移。
- `_fetch_thread_pages` 按对传递游标。

## 回归护栏

- 客户端：钉住 `fromPost`/`fromCreateAt` 同时出现在 wire 上；钉住只给一半会 `ValueError` 且**不发请求**。
- service：钉住翻页 kwargs 序列 `from_create_at == [None, 110]` 与 `from_post == [None, "seg_1"]` 逐位对齐。

139 个相关单测本地全绿。

合入后建议重跑一次 staging 验收（`zooclaw-dev/verify-agent-builder-forensics-staging.sh`），对那个 553 条线程确认 `distinct_run_ids` 非空——这个 bug 的性质决定了它只能由真实长线程证伪。


---

## feat(agent-builder): 取证端点 —— 离线 Mongo 回退脚本与操作文档 (#3608)

- **SHA**: `46e58a3da890571ceed735f7f688b3aee45aa816`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-03T06:56:39Z
- **PR**: #3608

### Commit Message

```
feat(agent-builder): 取证端点 —— 离线 Mongo 回退脚本与操作文档 (#3608)

## 本 PR（栈第 3 段，基于 `feat/agent-builder-forensics-engine-acs`）

- `scripts/agent_builder_forensics_dump.py`：端点不可达时的离线回退。主路径直接 import
`build_agent_builder_forensics` 打印同一契约；镜像里没有 `scripts/`，所以用 `kubectl
exec -i <pod> -- python3 - --project-id abp_… <
scripts/agent_builder_forensics_dump.py` 从 stdin 喂入。旧镜像 import 失败时走
`_legacy_projection()`（只用 `app.database.*`，每个用到的 repo 方法都核对过在 main
上存在；PR1 新增的 `list_by_internal_ref_any_status` 不在时用 `getattr` 探测后回退成等价
Mongo filter），输出仍必须通过
`AgentBuilderForensicsResponse.model_validate`（契约测试钉住），并带
`offline_legacy_projection` issue 列出缺的段。
- `docs/agent-builder-forensics.md`：为什么需要这个端点、取 token / base URL 的
kubectl 命令、`curl` + `jq` 示例、离线脚本用法、各段说明、issue code 词表（含三条 anomaly 的成因）、与
engine 侧 `scripts/dev/session-forensics --builder-json` 的衔接、两条
production 验收（`abp_c49ba34aee844619aa83ce0757d480e6` 应报
`dedicated_agent_no_sessions` 且 run id 落到 session
`aeb290aa-…`；`abp_fcd637e6e02849e580645d3b1b777c0a` → `0e879ff9-…`）。
- `.agents/skills/zooclaw-diagnose` 加 Agent Builder 一节指向端点与脚本。

## 验证

pytest 155 passed（含 10 个新契约/脚本测试）；pyright 0；全部 ci-lint 绿；`python -m
scripts.agent_builder_forensics_dump --help` 在无 Mongo env 下可运行（repo
import 延迟到函数内）。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_012SrM5f5Z94j2xA3FP8YKXB
```

### PR Body

## 本 PR（栈第 3 段，基于 `feat/agent-builder-forensics-engine-acs`）

- `scripts/agent_builder_forensics_dump.py`：端点不可达时的离线回退。主路径直接 import `build_agent_builder_forensics` 打印同一契约；镜像里没有 `scripts/`，所以用 `kubectl exec -i <pod> -- python3 - --project-id abp_… < scripts/agent_builder_forensics_dump.py` 从 stdin 喂入。旧镜像 import 失败时走 `_legacy_projection()`（只用 `app.database.*`，每个用到的 repo 方法都核对过在 main 上存在；PR1 新增的 `list_by_internal_ref_any_status` 不在时用 `getattr` 探测后回退成等价 Mongo filter），输出仍必须通过 `AgentBuilderForensicsResponse.model_validate`（契约测试钉住），并带 `offline_legacy_projection` issue 列出缺的段。
- `docs/agent-builder-forensics.md`：为什么需要这个端点、取 token / base URL 的 kubectl 命令、`curl` + `jq` 示例、离线脚本用法、各段说明、issue code 词表（含三条 anomaly 的成因）、与 engine 侧 `scripts/dev/session-forensics --builder-json` 的衔接、两条 production 验收（`abp_c49ba34aee844619aa83ce0757d480e6` 应报 `dedicated_agent_no_sessions` 且 run id 落到 session `aeb290aa-…`；`abp_fcd637e6e02849e580645d3b1b777c0a` → `0e879ff9-…`）。
- `.agents/skills/zooclaw-diagnose` 加 Agent Builder 一节指向端点与脚本。

## 验证

pytest 155 passed（含 10 个新契约/脚本测试）；pyright 0；全部 ci-lint 绿；`python -m scripts.agent_builder_forensics_dump --help` 在无 Mongo env 下可运行（repo import 延迟到函数内）。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_012SrM5f5Z94j2xA3FP8YKXB

---

## feat(agent-builder): 取证端点 —— engine session / ACS 通道段与 anomaly 检测 (#3607)

- **SHA**: `757367159fcc9ad041b56853d651dd2dc469cde6`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-03T06:51:58Z
- **PR**: #3607

### Commit Message

```
feat(agent-builder): 取证端点 —— engine session / ACS 通道段与 anomaly 检测 (#3607)

## 本 PR（栈第 2 段，基于 `feat/agent-builder-forensics-endpoint`）

给取证端点补上两个运行时的实况，并据此判 anomaly：

- **engine 段**：对每个 workspace 与每个 pack test 的 engine agent 调
`EngineClient.list_agent_sessions`（最多 3 页，超出 issue
`engine_sessions_truncated`），出 `engine_sessions[]{agent_id, source,
sessions[]{session_id, session_key, status, is_mattermost},
mattermost_session_count}`；`agent_not_running|session_not_found` → 空列表 +
info issue，其他异常 → 段内 `error` + warning，每个 agent 单独超时、互不拖累。engine 侧无需
actor（service token 即可，`engine_client/_base.py`）。
- **ACS 段**：按 `(computer_id, channel_agent_id)` 调
`list_agent_channels`——迁移 agent 在 ACS 里绑的是
`migration_v1_to_v2.internal_agent_id`（`agent_workspace.py:210-214`），有测试钉住用
internal id 而非 public id。
- **三条 anomaly issue**（`agent_builder_forensics_issues.py`，纯函数）：
- `agent_builder_dedicated_agent_no_sessions`：dedicated agent 零
Mattermost session 但线程里有 run id；message 列三种成因及代码路径（空闲时 ACS 通道被禁用 / MM
bot 绑定陈旧 / `builder_agent_id` 漂移），details 带该 agent 当前 ACS `enabled` 与
bot id 对照。
- `agent_builder_thread_bot_mismatch`：线程里发 assistant_segment 的 bot 不属于任何
workspace——这是 zooclaw-engine#1055 异常（真会话跑在另一 agent 上）的直接签名。
  - `pack_test_run_engine_agent_no_sessions`(info)。
- 路由加 `include_engine`；`engine_sections_not_enabled` 只在段被跳过时出现并带
`reason`。

## 验证

pytest 132 passed；pyright 0；ci-lint 01/02/03 绿；哨兵测试在有 engine/ACS
行的响应上仍通过。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_012SrM5f5Z94j2xA3FP8YKXB
```

### PR Body

## 本 PR（栈第 2 段，基于 `feat/agent-builder-forensics-endpoint`）

给取证端点补上两个运行时的实况，并据此判 anomaly：

- **engine 段**：对每个 workspace 与每个 pack test 的 engine agent 调 `EngineClient.list_agent_sessions`（最多 3 页，超出 issue `engine_sessions_truncated`），出 `engine_sessions[]{agent_id, source, sessions[]{session_id, session_key, status, is_mattermost}, mattermost_session_count}`；`agent_not_running|session_not_found` → 空列表 + info issue，其他异常 → 段内 `error` + warning，每个 agent 单独超时、互不拖累。engine 侧无需 actor（service token 即可，`engine_client/_base.py`）。
- **ACS 段**：按 `(computer_id, channel_agent_id)` 调 `list_agent_channels`——迁移 agent 在 ACS 里绑的是 `migration_v1_to_v2.internal_agent_id`（`agent_workspace.py:210-214`），有测试钉住用 internal id 而非 public id。
- **三条 anomaly issue**（`agent_builder_forensics_issues.py`，纯函数）：
  - `agent_builder_dedicated_agent_no_sessions`：dedicated agent 零 Mattermost session 但线程里有 run id；message 列三种成因及代码路径（空闲时 ACS 通道被禁用 / MM bot 绑定陈旧 / `builder_agent_id` 漂移），details 带该 agent 当前 ACS `enabled` 与 bot id 对照。
  - `agent_builder_thread_bot_mismatch`：线程里发 assistant_segment 的 bot 不属于任何 workspace——这是 zooclaw-engine#1055 异常（真会话跑在另一 agent 上）的直接签名。
  - `pack_test_run_engine_agent_no_sessions`(info)。
- 路由加 `include_engine`；`engine_sections_not_enabled` 只在段被跳过时出现并带 `reason`。

## 验证

pytest 132 passed；pyright 0；ci-lint 01/02/03 绿；哨兵测试在有 engine/ACS 行的响应上仍通过。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_012SrM5f5Z94j2xA3FP8YKXB

---

## feat(agent-builder): 取证端点 —— 项目/测试运行到 engine run 的映射（Mongo + MM 线程段） (#3606)

- **SHA**: `43d79008c431f9719e2c2a3db961cc2dd7426010`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-03T06:44:37Z
- **PR**: #3606

### Commit Message

```
feat(agent-builder): 取证端点 —— 项目/测试运行到 engine run 的映射（Mongo + MM 线程段） (#3606)

## 背景

zooclaw-engine#1055 排查时，从 agent-builder 项目 id（`abp_…`）找到 engine session
花了 3 轮：`AgentBuilderProject.builder_session_id`（sha256 规则）只是 claw 侧会话
id，从不下发 engine/ACS；dedicated builder agent（`internal_ref=abp`）可能零
session；真正能桥到 engine 的只有 Mattermost 线程里 assistant post 的
`props.run_id`。现有 `GET /agent-diagnostics/agent-builder/status` 不出任何
run/session id。

## 本 PR（栈第 1 段）

新增 sibling 端点 `GET
/agent-diagnostics/agent-builder/sessions?project_id=abp_…|test_run_id=…`（auth
复用 `require_billing_diagnostics_agent`，`_audit_lookup` 记审计），返回把一个
Project 桥到 engine run 所需的全部 id：

- `project`（含 #3602 之后的生命周期字段 `builder_runtime_last_active_at` /
`builder_ingress_active` /
`builder_lifecycle_claim_*`）、`workspaces[]`（`internal_ref` 命中 + 当前
`builder_agent_id`，不过滤已卸载，`relation` 标 current_builder /
internal_ref_match / historical）、`conversation`（带常量 note：claw 侧 id，不是
engine session id）。
- `builder_thread`：读 MM 线程，纯函数 `extract_thread_runs` 聚合 `props.run_id` →
`runs[]{run_id, turn, segments, terminal_phase, user_post_id,
bot_user_id}` 与 `distinct_run_ids[]`（engine 侧 CLI 拿它 ⋈
`run_status.run_id`）。只复制 identity props，不复制 post 正文。
- `pack_test_runs[]`：engine_* 全字段 + 各自线程 + test turns。
- `issues[]`：`agent_builder_project_not_found` / `pack_test_run_*` /
`agent_builder_runtime_computer_v1`(→`v1_pointer`) /
`agent_builder_builder_agent_drift` / `builder_conversation_missing` /
`mm_thread_truncated|unavailable` /
`engine_sections_not_enabled`（engine/ACS 段在栈第 2 段）。
- repo 增量：`engine_agent_workspace_repo.list_by_internal_ref_any_status /
get_by_agent_id_any_status`、`agent_builder_test_turn_repo.list_by_project`、`pack_test_run_repo.get_by_temp_computer_id`
补 `engine_computer_id`、`compact_run` 补 engine_* 键（/status
受益）、`get_post_thread` 可选分页参数（不传即老行为）。

所有响应模型 `extra="forbid"`，只出 id/时间/枚举；有哨兵测试断言 `model_dump_json()` 不含 post
正文 / bot token / prompt。

## 验证

pytest 113 passed（forensics 4 文件 + diagnostics / pack_test_repos /
mattermost_client）；pyright 0；ci-lint 01/02/03 绿。已 rebase 到 #3602 之后的
main（runtime slot 机制已删，本 PR 不再读 slot）。

Stacked：后续 `feat/agent-builder-forensics-engine-acs` →
`feat/agent-builder-forensics-offline`。消费方：zooclaw-engine#1066 的
`session-forensics locate --builder-json`。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_012SrM5f5Z94j2xA3FP8YKXB
```

### PR Body

## 背景

zooclaw-engine#1055 排查时，从 agent-builder 项目 id（`abp_…`）找到 engine session 花了 3 轮：`AgentBuilderProject.builder_session_id`（sha256 规则）只是 claw 侧会话 id，从不下发 engine/ACS；dedicated builder agent（`internal_ref=abp`）可能零 session；真正能桥到 engine 的只有 Mattermost 线程里 assistant post 的 `props.run_id`。现有 `GET /agent-diagnostics/agent-builder/status` 不出任何 run/session id。

## 本 PR（栈第 1 段）

新增 sibling 端点 `GET /agent-diagnostics/agent-builder/sessions?project_id=abp_…|test_run_id=…`（auth 复用 `require_billing_diagnostics_agent`，`_audit_lookup` 记审计），返回把一个 Project 桥到 engine run 所需的全部 id：

- `project`（含 #3602 之后的生命周期字段 `builder_runtime_last_active_at` / `builder_ingress_active` / `builder_lifecycle_claim_*`）、`workspaces[]`（`internal_ref` 命中 + 当前 `builder_agent_id`，不过滤已卸载，`relation` 标 current_builder / internal_ref_match / historical）、`conversation`（带常量 note：claw 侧 id，不是 engine session id）。
- `builder_thread`：读 MM 线程，纯函数 `extract_thread_runs` 聚合 `props.run_id` → `runs[]{run_id, turn, segments, terminal_phase, user_post_id, bot_user_id}` 与 `distinct_run_ids[]`（engine 侧 CLI 拿它 ⋈ `run_status.run_id`）。只复制 identity props，不复制 post 正文。
- `pack_test_runs[]`：engine_* 全字段 + 各自线程 + test turns。
- `issues[]`：`agent_builder_project_not_found` / `pack_test_run_*` / `agent_builder_runtime_computer_v1`(→`v1_pointer`) / `agent_builder_builder_agent_drift` / `builder_conversation_missing` / `mm_thread_truncated|unavailable` / `engine_sections_not_enabled`（engine/ACS 段在栈第 2 段）。
- repo 增量：`engine_agent_workspace_repo.list_by_internal_ref_any_status / get_by_agent_id_any_status`、`agent_builder_test_turn_repo.list_by_project`、`pack_test_run_repo.get_by_temp_computer_id` 补 `engine_computer_id`、`compact_run` 补 engine_* 键（/status 受益）、`get_post_thread` 可选分页参数（不传即老行为）。

所有响应模型 `extra="forbid"`，只出 id/时间/枚举；有哨兵测试断言 `model_dump_json()` 不含 post 正文 / bot token / prompt。

## 验证

pytest 113 passed（forensics 4 文件 + diagnostics / pack_test_repos / mattermost_client）；pyright 0；ci-lint 01/02/03 绿。已 rebase 到 #3602 之后的 main（runtime slot 机制已删，本 PR 不再读 slot）。

Stacked：后续 `feat/agent-builder-forensics-engine-acs` → `feat/agent-builder-forensics-offline`。消费方：zooclaw-engine#1066 的 `session-forensics locate --builder-json`。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_012SrM5f5Z94j2xA3FP8YKXB

---

## fix(chat): restore neutral degradation banner (#3632)

- **SHA**: `3101fe99d46aba80400b887ebd73efa9e8295c28`
- **作者**: shana-srp
- **日期**: 2026-09-03T05:49:29Z
- **PR**: #3632

### Commit Message

```
fix(chat): restore neutral degradation banner (#3632)

## Summary
- restyle the degraded-model banner with a transparent neutral surface
and white bordered action button
- replace the legacy four-stop IQ bar tokens with the approved shared
gradient token across all theme scopes
- add focused regression assertions for the restored banner classes and
gradient

This is the degradation-banner-only replacement for #3339; it
intentionally excludes the guide-tour behavior changes from that PR.

## Root cause
The approved banner restyle previously lived only in closed, unmerged PR
#3339, so both `main` and the production release continued to build the
legacy warning-colored banner.

## Test plan
- [x] `pnpm exec vitest run
src/__tests__/model-degradation-banner.test.tsx` (5 tests)
- [x] `pnpm tsc` and `pnpm lint` in `web/packages/chat-ui`
- [x] `bash scripts/verify-web.sh --no-test --no-lint
web/app/src/app/globals.css`
- [x] pre-commit and pre-push changed-surface verification

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary
- restyle the degraded-model banner with a transparent neutral surface and white bordered action button
- replace the legacy four-stop IQ bar tokens with the approved shared gradient token across all theme scopes
- add focused regression assertions for the restored banner classes and gradient

This is the degradation-banner-only replacement for #3339; it intentionally excludes the guide-tour behavior changes from that PR.

## Root cause
The approved banner restyle previously lived only in closed, unmerged PR #3339, so both `main` and the production release continued to build the legacy warning-colored banner.

## Test plan
- [x] `pnpm exec vitest run src/__tests__/model-degradation-banner.test.tsx` (5 tests)
- [x] `pnpm tsc` and `pnpm lint` in `web/packages/chat-ui`
- [x] `bash scripts/verify-web.sh --no-test --no-lint web/app/src/app/globals.css`
- [x] pre-commit and pre-push changed-surface verification


---

## fix(seo): narrow ZooWork root sitemap to main and docs (#3622)

- **SHA**: `2b78e55e3fb3b442f5c98d0da78dd2c6858f6eeb`
- **作者**: Mori-srp
- **日期**: 2026-09-03T03:43:29Z
- **PR**: #3622

### Commit Message

```
fix(seo): narrow ZooWork root sitemap to main and docs (#3622)

## Summary

- add the ZooWork marketing URL and SEO route contract under `docs/seo`
- document the executable source of truth, URL modes, locale
eligibility, canonical/hreflang/x-default rules, sitemap
responsibilities, and the change workflow
- narrow the checked-in root sitemap index to exactly two leaves: Main
(`/sitemap-main.xml`) and Docs (`/docs/sitemap.xml`)
- keep Blog and Tips independently indexable, but outside the root
sitemap aggregation
- update the root-index contract test and production audit expectation
from four children to two
- retain timestamped historical Staging/Production evidence without
treating a PR, merge, or Staging result as a production or GSC result

## Scope boundaries

- this PR does not change the 55-URL main-site sitemap or the marketing
route inventory
- this PR does not modify Docs sitemap output; that remains owned by the
Docs repository and must be deployed and production-validated separately
- removing Blog and Tips from the root index does not add `noindex` and
does not make their pages non-indexable
- this PR does not deploy production and does not submit anything to
Google Search Console

## Discovery trade-off

The 2026-09-03 rollout decision intentionally limits this phase's root
sitemap and GSC scope to Main + Docs. No independent GSC submission or
extra `robots.txt` Sitemap directive has been confirmed for Blog or
Tips. Consequently, crawlers relying only on the root robots/sitemap
path will not receive their complete URL sets; individual pages may
still be discovered through links, which is not equivalent to sitemap
discovery. The contract records this accepted phase boundary and
requires a separate owner decision and production/GSC receipt before
active Blog/Tips sitemap discovery is restored.

## Test plan

- [x] merge the latest `origin/main` into this branch without conflicts
- [x] verify every repository-relative link in the SEO document resolves
- [x] run focused frontend verification for the changed XML, audit, and
contract-test files
  - governance guards passed
  - TypeScript passed
  - 2 test files / 8 tests passed
- ESLint passed (the XML asset is intentionally outside the ESLint file
configuration)
- [x] run the pre-push changed-surface gate; TypeScript, frontend lint,
and governance guards passed
- [x] run `git diff --check origin/main...HEAD`
- [x] run the PR size gate: 409 / 3000 changed lines

## Release gate

After merge, production release and GSC submission remain separate
evidence stages:

1. deploy and validate the updated Docs sitemap in production;
2. deploy this main-site root index;
3. audit the production URLs, XML, canonical, hreflang, and x-default
output;
4. only after the audit passes, submit `https://zoowork.ai/sitemap.xml`
to the verified ZooWork Search Console property.
```

### PR Body

## Summary

- add the ZooWork marketing URL and SEO route contract under `docs/seo`
- document the executable source of truth, URL modes, locale eligibility, canonical/hreflang/x-default rules, sitemap responsibilities, and the change workflow
- narrow the checked-in root sitemap index to exactly two leaves: Main (`/sitemap-main.xml`) and Docs (`/docs/sitemap.xml`)
- keep Blog and Tips independently indexable, but outside the root sitemap aggregation
- update the root-index contract test and production audit expectation from four children to two
- retain timestamped historical Staging/Production evidence without treating a PR, merge, or Staging result as a production or GSC result

## Scope boundaries

- this PR does not change the 55-URL main-site sitemap or the marketing route inventory
- this PR does not modify Docs sitemap output; that remains owned by the Docs repository and must be deployed and production-validated separately
- removing Blog and Tips from the root index does not add `noindex` and does not make their pages non-indexable
- this PR does not deploy production and does not submit anything to Google Search Console

## Discovery trade-off

The 2026-09-03 rollout decision intentionally limits this phase's root sitemap and GSC scope to Main + Docs. No independent GSC submission or extra `robots.txt` Sitemap directive has been confirmed for Blog or Tips. Consequently, crawlers relying only on the root robots/sitemap path will not receive their complete URL sets; individual pages may still be discovered through links, which is not equivalent to sitemap discovery. The contract records this accepted phase boundary and requires a separate owner decision and production/GSC receipt before active Blog/Tips sitemap discovery is restored.

## Test plan

- [x] merge the latest `origin/main` into this branch without conflicts
- [x] verify every repository-relative link in the SEO document resolves
- [x] run focused frontend verification for the changed XML, audit, and contract-test files
  - governance guards passed
  - TypeScript passed
  - 2 test files / 8 tests passed
  - ESLint passed (the XML asset is intentionally outside the ESLint file configuration)
- [x] run the pre-push changed-surface gate; TypeScript, frontend lint, and governance guards passed
- [x] run `git diff --check origin/main...HEAD`
- [x] run the PR size gate: 409 / 3000 changed lines

## Release gate

After merge, production release and GSC submission remain separate evidence stages:

1. deploy and validate the updated Docs sitemap in production;
2. deploy this main-site root index;
3. audit the production URLs, XML, canonical, hreflang, and x-default output;
4. only after the audit passes, submit `https://zoowork.ai/sitemap.xml` to the verified ZooWork Search Console property.


---
