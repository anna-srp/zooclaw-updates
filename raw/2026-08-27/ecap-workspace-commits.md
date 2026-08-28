# SerendipityOneInc/ecap-workspace commits - 2026-08-27

## fix(pack-test): build only selected sandbox class (#3563)
- sha: `ad7bc8401b2a6532e1d3265dc86679b3b6287834`
- 作者: kaka-srp
- 日期: 2026-08-27T18:29:20Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/ad7bc8401b2a6532e1d3265dc86679b3b6287834
- PR: #3563

### 完整 commit message

```
fix(pack-test): build only selected sandbox class (#3563)

## Summary

- Make every production Pack Test creation path explicitly use
`engine_v2`; remove the unused v1 installer and its v1-only tests.
- Resolve and persist the user's sandbox resource class before runtime
reuse or Environment creation.
- Prepare the Environment archive once with the same translation inputs
used by installation, and persist its content hash so identical Engine
runtimes remain reusable.
- Request only the selected class from Engine and use it consistently
for build status, logs, and Agent create/update.
- Reject runtime reuse when either Environment content or the user's
current class differs from the prior Test Run.

## Root cause

Pack Test omitted the requested resource class, so Engine used its
compatibility default and built `starter`, `pro`, and `ultra`. An
unrelated class failure could block preview startup. The direct Pack
Test route also still selected the retired v1 installer; after moving it
to Engine, it needed the Environment content hash to preserve safe
runtime reuse.

## Dependencies

- Engine single-class Environment API:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/969
- Azure shared upload signing key:
https://github.com/SerendipityOneInc/infra/pull/26

## Test plan

- [x] 64 focused pytest cases for Pack Test creation, cleanup/recovery,
Engine runtime installation, runtime reuse, and Agent Builder handoff
- [x] Full Ruff and Ruff format checks
- [x] Full Pyright: 0 errors
- [x] Import-linter: all 8 architecture contracts kept
- [x] Pre-commit hooks, dead-code check, and pre-push `verify-changed`
- [x] `git diff --check`

## Review findings resolved

- [x] Prevent stale resource-class runtime reuse.
- [x] Keep the direct Pack Test route on Engine rather than adding
billing dependency to a v1 path.
- [x] Preserve Environment hash-based reuse on that Engine route.
- [x] Offload archive translation/repacking/hashing from the async
request event loop.
- [x] Remove the now-orphaned v1 installer and its self-only tests.

## Rollout and rollback

Deploy the infrastructure PR first, then Engine, then this caller. For
rollback, stop or roll back this caller first, drain in-flight
single-job builds, then roll back Engine.
```

### PR description

```
## Summary

- Make every production Pack Test creation path explicitly use `engine_v2`; remove the unused v1 installer and its v1-only tests.
- Resolve and persist the user's sandbox resource class before runtime reuse or Environment creation.
- Prepare the Environment archive once with the same translation inputs used by installation, and persist its content hash so identical Engine runtimes remain reusable.
- Request only the selected class from Engine and use it consistently for build status, logs, and Agent create/update.
- Reject runtime reuse when either Environment content or the user's current class differs from the prior Test Run.

## Root cause

Pack Test omitted the requested resource class, so Engine used its compatibility default and built `starter`, `pro`, and `ultra`. An unrelated class failure could block preview startup. The direct Pack Test route also still selected the retired v1 installer; after moving it to Engine, it needed the Environment content hash to preserve safe runtime reuse.

## Dependencies

- Engine single-class Environment API: https://github.com/SerendipityOneInc/zooclaw-engine/pull/969
- Azure shared upload signing key: https://github.com/SerendipityOneInc/infra/pull/26

## Test plan

- [x] 64 focused pytest cases for Pack Test creation, cleanup/recovery, Engine runtime installation, runtime reuse, and Agent Builder handoff
- [x] Full Ruff and Ruff format checks
- [x] Full Pyright: 0 errors
- [x] Import-linter: all 8 architecture contracts kept
- [x] Pre-commit hooks, dead-code check, and pre-push `verify-changed`
- [x] `git diff --check`

## Review findings resolved

- [x] Prevent stale resource-class runtime reuse.
- [x] Keep the direct Pack Test route on Engine rather than adding billing dependency to a v1 path.
- [x] Preserve Environment hash-based reuse on that Engine route.
- [x] Offload archive translation/repacking/hashing from the async request event loop.
- [x] Remove the now-orphaned v1 installer and its self-only tests.

## Rollout and rollback

Deploy the infrastructure PR first, then Engine, then this caller. For rollback, stop or roll back this caller first, drain in-flight single-job builds, then roll back Engine.

```

---

## fix(agents): soft-delete channels on fire (#3562)
- sha: `566c4150ecf1672dce851bcf9d465299e5f7426f`
- 作者: kaka-srp
- 日期: 2026-08-27T17:39:05Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/566c4150ecf1672dce851bcf9d465299e5f7426f
- PR: #3562

### 完整 commit message

```
fix(agents): soft-delete channels on fire (#3562)

## Summary

- switch terminal Agent fire/uninstall cleanup from bulk disable to ACS
bulk soft delete
- keep recoverable Agent Studio and subscription/runtime suspension
flows on bulk disable
- use the same terminal cleanup for temporary pack-test Agents
- retain best-effort cleanup semantics after the Agent reaches its
terminal state

## Behavior

ACS publishes a delete reconcile for every soft-deleted channel.
Existing gateway reconciliation removes the account from desired state
and invokes the platform plugin's `stopAccount`, closing its WebSocket
or other long-lived connection.

## Validation

- 12 directly related pytest cases passed across the ACS client, Agent
channel helper, uninstall lifecycle, service proxy, and pack-test
cleanup
- changed-file Ruff and formatting checks passed
- changed-file Pyright passed with 0 errors
- `bash scripts/verify-changed.sh` (pre-push): Ruff, formatting,
full-repo Pyright, and import-linter passed
- full local pytest suite not run per request

## Rollout

Depends on
[agent-channel-service#100](https://github.com/SerendipityOneInc/agent-channel-service/pull/100),
which adds `POST
/v1/computers/{computer_id}/agents/{agent_id}/channels/delete`. Deploy
ACS first.

## Design

See
`docs/superpowers/specs/2026-08-27-agent-channel-fire-soft-delete-design.md`.
```

### PR description

```
## Summary

- switch terminal Agent fire/uninstall cleanup from bulk disable to ACS bulk soft delete
- keep recoverable Agent Studio and subscription/runtime suspension flows on bulk disable
- use the same terminal cleanup for temporary pack-test Agents
- retain best-effort cleanup semantics after the Agent reaches its terminal state

## Behavior

ACS publishes a delete reconcile for every soft-deleted channel. Existing gateway reconciliation removes the account from desired state and invokes the platform plugin's `stopAccount`, closing its WebSocket or other long-lived connection.

## Validation

- 12 directly related pytest cases passed across the ACS client, Agent channel helper, uninstall lifecycle, service proxy, and pack-test cleanup
- changed-file Ruff and formatting checks passed
- changed-file Pyright passed with 0 errors
- `bash scripts/verify-changed.sh` (pre-push): Ruff, formatting, full-repo Pyright, and import-linter passed
- full local pytest suite not run per request

## Rollout

Depends on [agent-channel-service#100](https://github.com/SerendipityOneInc/agent-channel-service/pull/100), which adds `POST /v1/computers/{computer_id}/agents/{agent_id}/channels/delete`. Deploy ACS first.

## Design

See `docs/superpowers/specs/2026-08-27-agent-channel-fire-soft-delete-design.md`.

```

---

## fix(agent-builder): recover slow publish submissions (#3561)
- sha: `d3730c7f4ef2ad7f63c0440013f8c2d53d85d42a`
- 作者: kaka-srp
- 日期: 2026-08-27T15:08:10Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/d3730c7f4ef2ad7f63c0440013f8c2d53d85d42a
- PR: #3561

### 完整 commit message

```
fix(agent-builder): recover slow publish submissions (#3561)

## Summary
- Extend Agent Builder v2 iteration submission to a 90-second client
timeout.
- Recover an aborted submission by polling the authoritative project
state and continuing only when the same iteration and test run was
persisted as submitted.
- Replace the raw AbortError with localized recovery guidance and add
regression coverage for timeout, polling, and cross-iteration safety.

## Root cause
Agent Builder submission performs validation and Pack promotion
synchronously and can take longer than the API client's 30-second
default timeout. The browser aborted first while the backend continued
and successfully persisted the submission. Retrying from the error
dialog then issued a duplicate submit against an already-promoted test
run.

## Test plan
- [x] `pnpm exec vitest run
tests/unit/services/agent-builder-v2.unit.spec.ts
tests/unit/services/agent-builder-publish.unit.spec.ts` (27 tests)
- [x] `pnpm exec vitest run
tests/unit/app/agent-builder-client.unit.spec.tsx -t "shows a
recovery-safe message instead of the raw AbortError when Publish times
out"`
- [x] `bash scripts/verify-changed.sh`
- [x] Pre-push size, TypeScript, and ESLint gates
```

### PR description

```
## Summary
- Extend Agent Builder v2 iteration submission to a 90-second client timeout.
- Recover an aborted submission by polling the authoritative project state and continuing only when the same iteration and test run was persisted as submitted.
- Replace the raw AbortError with localized recovery guidance and add regression coverage for timeout, polling, and cross-iteration safety.

## Root cause
Agent Builder submission performs validation and Pack promotion synchronously and can take longer than the API client's 30-second default timeout. The browser aborted first while the backend continued and successfully persisted the submission. Retrying from the error dialog then issued a duplicate submit against an already-promoted test run.

## Test plan
- [x] `pnpm exec vitest run tests/unit/services/agent-builder-v2.unit.spec.ts tests/unit/services/agent-builder-publish.unit.spec.ts` (27 tests)
- [x] `pnpm exec vitest run tests/unit/app/agent-builder-client.unit.spec.tsx -t "shows a recovery-safe message instead of the raw AbortError when Publish times out"`
- [x] `bash scripts/verify-changed.sh`
- [x] Pre-push size, TypeScript, and ESLint gates

```

---

## fix(agent-builder): allow exiting failed initialization (#3560)
- sha: `5f7f08971f15913c7445ee1cd9b1cacf55c80ac6`
- 作者: kaka-srp
- 日期: 2026-08-27T15:07:41Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/5f7f08971f15913c7445ee1cd9b1cacf55c80ac6
- PR: #3560

### 完整 commit message

```
fix(agent-builder): allow exiting failed initialization (#3560)

## Summary
- Let users return to the Agent Builder Project list after a first-turn
initialization error instead of being routed back into the same failed
Project.
- Preserve the pending prompt, attachment progress, model choice, and
idempotency key so manual reopen and explicit retry still recover
safely.
- Keep automatic navigation for new and legacy in-flight handoffs, and
add regression coverage plus a design spec.

## Root cause
The pending initialization record represented both durable recovery data
and the Agent Builder home page's auto-navigation policy. Initialization
errors intentionally preserved that record for retry, so every visit to
`/agent-builder` interpreted it as an instruction to reopen the failed
Project and trapped the user in a redirect loop.

## Test plan
- [x] `bash scripts/verify-web.sh <changed Agent Builder source and test
files>`
- [x] 61 targeted Vitest cases passed across the entry page and
pending-initialization hook suites
- [x] TypeScript, ESLint, all seven frontend governance guards, and `git
diff --check` passed
- [x] Pre-push changed-surface verification passed
```

### PR description

```
## Summary
- Let users return to the Agent Builder Project list after a first-turn initialization error instead of being routed back into the same failed Project.
- Preserve the pending prompt, attachment progress, model choice, and idempotency key so manual reopen and explicit retry still recover safely.
- Keep automatic navigation for new and legacy in-flight handoffs, and add regression coverage plus a design spec.

## Root cause
The pending initialization record represented both durable recovery data and the Agent Builder home page's auto-navigation policy. Initialization errors intentionally preserved that record for retry, so every visit to `/agent-builder` interpreted it as an instruction to reopen the failed Project and trapped the user in a redirect loop.

## Test plan
- [x] `bash scripts/verify-web.sh <changed Agent Builder source and test files>`
- [x] 61 targeted Vitest cases passed across the entry page and pending-initialization hook suites
- [x] TypeScript, ESLint, all seven frontend governance guards, and `git diff --check` passed
- [x] Pre-push changed-surface verification passed

```

---

## fix(invitation): keep checklist text uniform with a green done mark (#3558)
- sha: `605de3a5d33a990a0377b1541fce670dd1858be0`
- 作者: tim-srp
- 日期: 2026-08-27T13:03:59Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/605de3a5d33a990a0377b1541fce670dd1858be0
- PR: #3558

### 完整 commit message

```
fix(invitation): keep checklist text uniform with a green done mark (#3558)

## 背景

#3557 上线后在 invitation 登录成功页引入进度清单,用户反馈:**绿色对号完成后,字体颜色看不清**。

根因:`.progressItemDone` / `.progressItemRunning` 使用 `color:
var(--boss-ink)` 作为文字颜色,但 `--boss-ink` 是**卡片背景色** token(深色 #0b0d11 /
light #f7f3ec)。步骤完成后文字被涂成背景色,与卡片融为一体。

## 改动

`web/app/src/app/[locale]/bossclaw/bossclaw.module.css`

- `.progressItem` 基础文字色改为 `var(--boss-cream)`(页面主文本色)
- 删除 `.progressItemDone` / `.progressItemRunning` 两个文字颜色覆盖块
- 所有条目文字保持统一颜色,状态仅由左侧标记区分:绿色 ✓ / 金色 spinner / 灰色圆点

## 验证

- `verify-web.sh --no-test`(guards + tsc + eslint)通过
- 纯 CSS 改动,无逻辑/测试影响

---------

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR description

```
## 背景

#3557 上线后在 invitation 登录成功页引入进度清单,用户反馈:**绿色对号完成后,字体颜色看不清**。

根因:`.progressItemDone` / `.progressItemRunning` 使用 `color: var(--boss-ink)` 作为文字颜色,但 `--boss-ink` 是**卡片背景色** token(深色 #0b0d11 / light #f7f3ec)。步骤完成后文字被涂成背景色,与卡片融为一体。

## 改动

`web/app/src/app/[locale]/bossclaw/bossclaw.module.css`

- `.progressItem` 基础文字色改为 `var(--boss-cream)`(页面主文本色)
- 删除 `.progressItemDone` / `.progressItemRunning` 两个文字颜色覆盖块
- 所有条目文字保持统一颜色,状态仅由左侧标记区分:绿色 ✓ / 金色 spinner / 灰色圆点

## 验证

- `verify-web.sh --no-test`(guards + tsc + eslint)通过
- 纯 CSS 改动,无逻辑/测试影响

```

---

## feat(invitation): show progress checklist on login success screen (#3557)
- sha: `6ce1c1e2f244a0f85cff27add1162be963e0a90a`
- 作者: tim-srp
- 日期: 2026-08-27T12:40:19Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/6ce1c1e2f244a0f85cff27add1162be963e0a90a
- PR: #3557

### 完整 commit message

```
feat(invitation): show progress checklist on login success screen (#3557)

## 背景

`/invitation/login` 新用户注册成功后，过渡页长时间停留在静态的「验证完成 / 正在进入您的 ZooWork
工作区…」——期间实际在跑较慢的注册管线（OTP 验证 → 开通工作区 → 激活邀请权益 → 导航），等待过程没有任何反馈，容易引发焦虑。

## 改动

将 success 过渡页改为 **4 步执行清单**，随真实进度推进：

| 步骤 | 文案 | 状态反馈 |
| --- | --- | --- |
| identity | 验证身份 | 完成 → 绿色对勾 |
| workspace | 开通专属工作区 | 进行中 → 金色 spinner；待执行 → 灰色圆点 |
| redeem | 激活邀请权益 | 同上 |
| enter | 正在进入您的 ZooWork 工作区… | 导航前保持进行中（returnTo 存在时显示「正在返回…」） |

### 实现要点

- `lib/auth/manager.ts`：`loginWithSmsOTP` 新增**可选** `onVerified`
回调（向后兼容），在 OTP 通过、慢速注册开始前触发——这是 checklist 能反映真实进度的关键边界。
- `invitation/login/useBossclawLoginFlow.ts`：新增 `progress` state 与
`markDone/markRunning` helpers，接入新用户注册分支（含 `already_participated`
视为成功的路径）。
- `invitation/login/BossclawLoginClient.tsx` +
`bossclaw.module.css`：success 视图渲染 checklist（done → 绿勾 / running →
spinner / pending → 灰点），沿用既有品牌 token，深/浅色主题均适配。

## 测试

- hook：progress 状态推进（注册 + redeem 成功路径）、`already_participated`
分支推进；既有断言更新为三参调用。
- 组件：成功清单渲染（绿勾 / spinner / pending 无标记）、returnTo 时末步文案。

新增/更新用例后 `tests/unit/bossclaw/` 全量 115 个通过，`verify-web.sh`（guards + tsc
+ eslint）通过。

## 部署

前端-only 变更，无需后端部署。

---------

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR description

```
## 背景

`/invitation/login` 新用户注册成功后，过渡页长时间停留在静态的「验证完成 / 正在进入您的 ZooWork 工作区…」——期间实际在跑较慢的注册管线（OTP 验证 → 开通工作区 → 激活邀请权益 → 导航），等待过程没有任何反馈，容易引发焦虑。

## 改动

将 success 过渡页改为 **4 步执行清单**，随真实进度推进：

| 步骤 | 文案 | 状态反馈 |
| --- | --- | --- |
| identity | 验证身份 | 完成 → 绿色对勾 |
| workspace | 开通专属工作区 | 进行中 → 金色 spinner；待执行 → 灰色圆点 |
| redeem | 激活邀请权益 | 同上 |
| enter | 正在进入您的 ZooWork 工作区… | 导航前保持进行中（returnTo 存在时显示「正在返回…」） |

### 实现要点

- `lib/auth/manager.ts`：`loginWithSmsOTP` 新增**可选** `onVerified` 回调（向后兼容），在 OTP 通过、慢速注册开始前触发——这是 checklist 能反映真实进度的关键边界。
- `invitation/login/useBossclawLoginFlow.ts`：新增 `progress` state 与 `markDone/markRunning` helpers，接入新用户注册分支（含 `already_participated` 视为成功的路径）。
- `invitation/login/BossclawLoginClient.tsx` + `bossclaw.module.css`：success 视图渲染 checklist（done → 绿勾 / running → spinner / pending → 灰点），沿用既有品牌 token，深/浅色主题均适配。

## 测试

- hook：progress 状态推进（注册 + redeem 成功路径）、`already_participated` 分支推进；既有断言更新为三参调用。
- 组件：成功清单渲染（绿勾 / spinner / pending 无标记）、returnTo 时末步文案。

新增/更新用例后 `tests/unit/bossclaw/` 全量 115 个通过，`verify-web.sh`（guards + tsc + eslint）通过。

## 部署

前端-only 变更，无需后端部署。

```

---

## fix(sidenav): 优化侧边栏选中态 (#3555)
- sha: `8c889ecb35bb2fb3aacd3fc7e5da4890ce1f0452`
- 作者: lynn Zhuang
- 日期: 2026-08-27T11:22:59Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/8c889ecb35bb2fb3aacd3fc7e5da4890ce1f0452
- PR: #3555

### 完整 commit message

```
fix(sidenav): 优化侧边栏选中态 (#3555)

## 变更说明

- `New Task` 保持操作入口语义，仅提供点击和悬停反馈，不显示持久选中态
- 当前路由对应的侧边栏模块只使用背景色块表示选中，并添加 `aria-current="page"`
- 移除左侧指示条、边框和内描边，同时将遗留 CSS Module 迁移为 Tailwind 工具类

## 验证

- `bash scripts/verify-changed.sh`
- `pnpm exec vitest run
tests/unit/components/sidenav/build-bottom-nav-items.unit.spec.ts
tests/unit/components/sidenav/NavItemComponent.unit.spec.tsx`
- 使用本地 Mock 在 Paper Focus 浅色模式下完成浏览器验证：选中模块无边框、阴影和指示条；`New Task`
仅在悬停时显示背景
```

### PR description

```
## 变更说明

- `New Task` 保持操作入口语义，仅提供点击和悬停反馈，不显示持久选中态
- 当前路由对应的侧边栏模块只使用背景色块表示选中，并添加 `aria-current="page"`
- 移除左侧指示条、边框和内描边，同时将遗留 CSS Module 迁移为 Tailwind 工具类

## 验证

- `bash scripts/verify-changed.sh`
- `pnpm exec vitest run tests/unit/components/sidenav/build-bottom-nav-items.unit.spec.ts tests/unit/components/sidenav/NavItemComponent.unit.spec.tsx`
- 使用本地 Mock 在 Paper Focus 浅色模式下完成浏览器验证：选中模块无边框、阴影和指示条；`New Task` 仅在悬停时显示背景

```

---

## fix(ios): gate chat on runtime capability and any connectable engine agent (#3544)
- sha: `587e43710617a74f00c3376c9794b89976c65d57`
- 作者: bill-srp
- 日期: 2026-08-27T10:59:52Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/587e43710617a74f00c3376c9794b89976c65d57
- PR: #3544

### 完整 commit message

```
fix(ios): gate chat on runtime capability and any connectable engine agent (#3544)

## Linear
<!-- follow-up to #3526; no Linear issue -->

## Summary
- **Bug (TestFlight 1.9.0 build 3, prod):** an account whose main engine
agent isn't `active` with a Mattermost DM never got chat:
`AgentRuntimeViewModel.waitForMainAgent` polled `GET
/agents?runtime=engine` for the whole session, Mattermost was never
contacted, and sends failed with `noActiveChannel`. Web works on the
same account because it gates only on `install-capability == engine` and
connects to **any** active engine agent with a DM channel
(`selectChatEligibleAgents`, main preferred).
- **Fix:** readiness = capability only (main-agent poll and its
`/agents` request burst removed); `MattermostViewModel.ChatAvailability`
(`unknown | noAgent | available`) drives a "No chat agent is set up for
this account yet" banner with **Check again**; the composer is disabled
with "Connecting…" until chat is available *and* connected; one
automatic reconnect after a successful agent install or when the agent
list gains a connectable row.
- Spec: `docs/superpowers/specs/2026-08-27-ios-v2-chat-readiness.md`.
Follow-up to #3526.

## Test plan
- [x] `swiftlint --strict` 0 violations; simulator build + whole
`ZooClawTests` bundle green locally (counts in PR checks)
- [x] Unit: capability `engine` ⇒ `.ready` with no `/agents` poll;
`computer` ⇒ `.notEligible`; cancellation ⇒ `.idle`; generation guard
across reset; `.noAgent` when no DM-capable agent (no `/users/me`, no
WS); connects on a non-main DM-capable agent;
`ChatComposerState.resolve` matrix; reconnect after hire
- [ ] TestFlight re-test on the `7279764241869537280` account (org
`4ee1b7db…`): chat connects or shows the no-agent banner instead of
spinning; hire an agent → chat connects
```

### PR description

```
## Linear
<!-- follow-up to #3526; no Linear issue -->

## Summary
- **Bug (TestFlight 1.9.0 build 3, prod):** an account whose main engine agent isn't `active` with a Mattermost DM never got chat: `AgentRuntimeViewModel.waitForMainAgent` polled `GET /agents?runtime=engine` for the whole session, Mattermost was never contacted, and sends failed with `noActiveChannel`. Web works on the same account because it gates only on `install-capability == engine` and connects to **any** active engine agent with a DM channel (`selectChatEligibleAgents`, main preferred).
- **Fix:** readiness = capability only (main-agent poll and its `/agents` request burst removed); `MattermostViewModel.ChatAvailability` (`unknown | noAgent | available`) drives a "No chat agent is set up for this account yet" banner with **Check again**; the composer is disabled with "Connecting…" until chat is available *and* connected; one automatic reconnect after a successful agent install or when the agent list gains a connectable row.
- Spec: `docs/superpowers/specs/2026-08-27-ios-v2-chat-readiness.md`. Follow-up to #3526.

## Test plan
- [x] `swiftlint --strict` 0 violations; simulator build + whole `ZooClawTests` bundle green locally (counts in PR checks)
- [x] Unit: capability `engine` ⇒ `.ready` with no `/agents` poll; `computer` ⇒ `.notEligible`; cancellation ⇒ `.idle`; generation guard across reset; `.noAgent` when no DM-capable agent (no `/users/me`, no WS); connects on a non-main DM-capable agent; `ChatComposerState.resolve` matrix; reconnect after hire
- [ ] TestFlight re-test on the `7279764241869537280` account (org `4ee1b7db…`): chat connects or shows the no-agent banner instead of spinning; hire an agent → chat connects

```

---

## feat(design-system): 发布 ZooWork Design System 2.0 (#3510)
- sha: `e9e266813fec3c26b7f2f9d65b6e53a430d198bd`
- 作者: lynn Zhuang
- 日期: 2026-08-27T10:34:45Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/e9e266813fec3c26b7f2f9d65b6e53a430d198bd
- PR: #3510

### 完整 commit message

```
feat(design-system): 发布 ZooWork Design System 2.0 (#3510)

## 背景

ZooWork Design System 原有视觉语言依赖大量半透明、模糊和悬浮卡片，信息密度和层级表达不够稳定。本 PR 发布
ZooWork Design System 2.0，将整体方向调整为效率优先、简洁克制的中性界面，并以 `#5755C6` 作为品牌紫。

## 主要改动

- 重建颜色、表面、交互、圆角、间距、排版、动效和层级 Token
- 将品牌红替换为 `#5755C6`，品牌紫仅用于 Logo、手绘导航标记与品牌识别；红色仅保留给错误和破坏性操作
- 将 Canvas、Sidebar、Surface、文字、分割线和交互灰阶统一为无冷暖倾向的中性灰
- Button、Form、Switch、Checkbox、Radio、Tabs、Slider、Progress 与 Focus
状态统一使用中性灰阶
- Button 新增一等 `loading` API、`aria-busy` 语义、稳定宽度、按压反馈和 reduced-motion
降级；不可用的 `asChild` 链接同时阻断 click 与 auxclick 导航
- Button 预览升级为可交互 Button Lab，并补齐
Anatomy、Variants、Sizes、States、Composition、Usage 与无障碍说明
- Badge 新增 `notification` 消息语义、`dot` 红点、`count` 自适应圆形/胶囊形态，并复用 Tag 的
success、warning、danger、info 色板
- Dropdown、Select、菜单项的 Hover 与 Selected 背景统一为同一浅色 Token，持久选中依靠勾选等附加信号表达
- Input、Textarea、Select、NativeSelect 的 Focus Halo 调整为更浅、更窄的 `2px / 25%`
中性焦点环
- ButtonGroup 默认改为 Gumloop Agents 风格的 Segmented Control，支持文字筛选和图标视图切换；保留
`attached` 兼容模式
- ButtonGroup 文档归入 Button 模块；Attached 前缀与 ScrollArea 示例统一使用中性语义边框
- 产品标题与组件标题统一使用无衬线字体，衬线字体仅保留在品牌字标
- 移除 Dropdown、Select、Popover、ContextMenu、Dialog、Sheet、Drawer
等组件的玻璃、模糊和半透明效果
- 将侧栏和内容区改为不透明扁平色块，并使用 1px 分割线建立结构
- Select 优先在触发器下方显示并保持 4px 间距，视口空间不足时保留 Radix 自适应碰撞处理
- NativeSelect 保留系统原生弹层行为；需要完整 DS 状态控制时使用 Select
- 增加 pointer/keyboard 输入方式识别：鼠标关闭浮层后不残留焦点外圈，键盘导航仍保留焦点提示
- 程序化焦点继承最近一次输入方式，修复鼠标打开 AlertDialog 等浮层后自动聚焦控件错误显示键盘焦点描边
- Hero 使用真实 Design System 组件构成可交互物理积木，并补充手绘品牌导航标记与统一 motion tokens
- 重建 Design System 预览页，统一使用 ZooWork 品牌，覆盖浅色、暗色、移动端和全部组件状态
- 预览页品牌标题移除版本号，去掉顶部、侧栏、Hero 画布与首屏底部分割线，主题切换改为双图标 segmented ButtonGroup
- 增加版本化 Changelog 模块及 `CHANGELOG.md`，记录
Added、Changed、Removed、Fixed、Deprecated、PR 和 revision
- 包版本升级为 `2.0.0`

## 兼容与范围

- 本阶段生产代码主要修改 `@zooclaw/design-system`，并同步更新预览页和设计规范；npm scope 暂不改名
- `web/app` 除两份 Composer 菜单契约测试外，仅迁移 API Keys secret copy 按钮到新 `default`
尺寸，保持最新 main 要求的紧凑 `h-9 / w-24` 布局；未修改 `@zooclaw/chat-ui`
- 旧 Glass Token 与 `surface="glass"` 暂时保留为不透明兼容别名，后续可按迁移计划移除
- ButtonGroup 原连接按钮样式通过 `variant="attached"` 保留
- 视觉语言和部分默认交互属于 2.0 大版本变更，业务页面接入需要单独分阶段迁移

## 验证

- `pnpm test`：59 个测试文件、353 个测试通过
- `pnpm tsc`：通过
- `pnpm lint`：通过
- `pnpm build:preview`：通过
- `bash scripts/verify-local.sh --changed`：Web App TypeScript、ESLint 与
changed-surface 门禁通过
- 手动视觉验收：390px、1280px；浅色与暗色；Button
Lab、ButtonGroup、ScrollArea、loading、状态矩阵和响应式分区
- 浏览器实测：Button loading 切换前后宽度均为 111.39px；`aria-busy`、disabled、spinner
与普通状态 DOM 兼容性正确
- 浏览器实测：ButtonGroup Attached 与 ScrollArea 边框在浅色为 `rgb(229, 229,
229)`、暗色为 `rgb(46, 46, 46)`
- 浏览器实测：鼠标打开 AlertDialog 后 Cancel 自动聚焦并继承 pointer 模态，计算样式为 `box-shadow:
none`；键盘路径由回归测试覆盖
- 浏览器实测：Badge 单数字为 `20 × 20px` 正圆，`99+` 与长字段自动扩展为胶囊；notification
与四种语义色在浅色、暗色下均完成视觉验收
- 浏览器实测：顶部、侧栏、Hero 画布与首屏底部分割线计算宽度均为 `0px`；Hero 保留 `12px` 圆角与轻阴影；主题
ButtonGroup 为 `76 × 40px`，浅色/深色选中态与 `aria-pressed` 同步
- 扫描确认组件和预览页无 `backdrop-blur`、Glass class 或旧品牌红残留；`#5755C6` 仅用于品牌表达

## 设计文档

- `docs/superpowers/specs/2026-08-25-zooclaw-neutral-design-system.md`
- `docs/superpowers/plans/2026-08-25-zooclaw-design-system-2.md`

## 风险与后续

- 本 PR 是 Design System 2.0 的原子升级，当前 size gate 统计为 4,895 行，超过 3,000
行体量门槛；已添加 `size-override`，核心组件行为、预览和迁移边界仍保持在同一发布单元内
- 预览构建仍有 Vite 单 chunk 超过 500 kB 的提示，这是组件全集预览页的既有打包形态，不阻塞本次发布
- 下一阶段再将 2.0 Token 和组件逐步迁移到 `web/app` 与 `@zooclaw/chat-ui`，每次修改 chat
相关页面前需要同时读取两侧代码判断归属
```

### PR description

```
## 背景

ZooWork Design System 原有视觉语言依赖大量半透明、模糊和悬浮卡片，信息密度和层级表达不够稳定。本 PR 发布 ZooWork Design System 2.0，将整体方向调整为效率优先、简洁克制的中性界面，并以 `#5755C6` 作为品牌紫。

## 主要改动

- 重建颜色、表面、交互、圆角、间距、排版、动效和层级 Token
- 将品牌红替换为 `#5755C6`，品牌紫仅用于 Logo、手绘导航标记与品牌识别；红色仅保留给错误和破坏性操作
- 将 Canvas、Sidebar、Surface、文字、分割线和交互灰阶统一为无冷暖倾向的中性灰
- Button、Form、Switch、Checkbox、Radio、Tabs、Slider、Progress 与 Focus 状态统一使用中性灰阶
- Button 新增一等 `loading` API、`aria-busy` 语义、稳定宽度、按压反馈和 reduced-motion 降级；不可用的 `asChild` 链接同时阻断 click 与 auxclick 导航
- Button 预览升级为可交互 Button Lab，并补齐 Anatomy、Variants、Sizes、States、Composition、Usage 与无障碍说明
- Badge 新增 `notification` 消息语义、`dot` 红点、`count` 自适应圆形/胶囊形态，并复用 Tag 的 success、warning、danger、info 色板
- Dropdown、Select、菜单项的 Hover 与 Selected 背景统一为同一浅色 Token，持久选中依靠勾选等附加信号表达
- Input、Textarea、Select、NativeSelect 的 Focus Halo 调整为更浅、更窄的 `2px / 25%` 中性焦点环
- ButtonGroup 默认改为 Gumloop Agents 风格的 Segmented Control，支持文字筛选和图标视图切换；保留 `attached` 兼容模式
- ButtonGroup 文档归入 Button 模块；Attached 前缀与 ScrollArea 示例统一使用中性语义边框
- 产品标题与组件标题统一使用无衬线字体，衬线字体仅保留在品牌字标
- 移除 Dropdown、Select、Popover、ContextMenu、Dialog、Sheet、Drawer 等组件的玻璃、模糊和半透明效果
- 将侧栏和内容区改为不透明扁平色块，并使用 1px 分割线建立结构
- Select 优先在触发器下方显示并保持 4px 间距，视口空间不足时保留 Radix 自适应碰撞处理
- NativeSelect 保留系统原生弹层行为；需要完整 DS 状态控制时使用 Select
- 增加 pointer/keyboard 输入方式识别：鼠标关闭浮层后不残留焦点外圈，键盘导航仍保留焦点提示
- 程序化焦点继承最近一次输入方式，修复鼠标打开 AlertDialog 等浮层后自动聚焦控件错误显示键盘焦点描边
- Hero 使用真实 Design System 组件构成可交互物理积木，并补充手绘品牌导航标记与统一 motion tokens
- 重建 Design System 预览页，统一使用 ZooWork 品牌，覆盖浅色、暗色、移动端和全部组件状态
- 预览页品牌标题移除版本号，去掉顶部、侧栏、Hero 画布与首屏底部分割线，主题切换改为双图标 segmented ButtonGroup
- 增加版本化 Changelog 模块及 `CHANGELOG.md`，记录 Added、Changed、Removed、Fixed、Deprecated、PR 和 revision
- 包版本升级为 `2.0.0`

## 兼容与范围

- 本阶段生产代码主要修改 `@zooclaw/design-system`，并同步更新预览页和设计规范；npm scope 暂不改名
- `web/app` 除两份 Composer 菜单契约测试外，仅迁移 API Keys secret copy 按钮到新 `default` 尺寸，保持最新 main 要求的紧凑 `h-9 / w-24` 布局；未修改 `@zooclaw/chat-ui`
- 旧 Glass Token 与 `surface="glass"` 暂时保留为不透明兼容别名，后续可按迁移计划移除
- ButtonGroup 原连接按钮样式通过 `variant="attached"` 保留
- 视觉语言和部分默认交互属于 2.0 大版本变更，业务页面接入需要单独分阶段迁移

## 验证

- `pnpm test`：59 个测试文件、353 个测试通过
- `pnpm tsc`：通过
- `pnpm lint`：通过
- `pnpm build:preview`：通过
- `bash scripts/verify-local.sh --changed`：Web App TypeScript、ESLint 与 changed-surface 门禁通过
- 手动视觉验收：390px、1280px；浅色与暗色；Button Lab、ButtonGroup、ScrollArea、loading、状态矩阵和响应式分区
- 浏览器实测：Button loading 切换前后宽度均为 111.39px；`aria-busy`、disabled、spinner 与普通状态 DOM 兼容性正确
- 浏览器实测：ButtonGroup Attached 与 ScrollArea 边框在浅色为 `rgb(229, 229, 229)`、暗色为 `rgb(46, 46, 46)`
- 浏览器实测：鼠标打开 AlertDialog 后 Cancel 自动聚焦并继承 pointer 模态，计算样式为 `box-shadow: none`；键盘路径由回归测试覆盖
- 浏览器实测：Badge 单数字为 `20 × 20px` 正圆，`99+` 与长字段自动扩展为胶囊；notification 与四种语义色在浅色、暗色下均完成视觉验收
- 浏览器实测：顶部、侧栏、Hero 画布与首屏底部分割线计算宽度均为 `0px`；Hero 保留 `12px` 圆角与轻阴影；主题 ButtonGroup 为 `76 × 40px`，浅色/深色选中态与 `aria-pressed` 同步
- 扫描确认组件和预览页无 `backdrop-blur`、Glass class 或旧品牌红残留；`#5755C6` 仅用于品牌表达

## 设计文档

- `docs/superpowers/specs/2026-08-25-zooclaw-neutral-design-system.md`
- `docs/superpowers/plans/2026-08-25-zooclaw-design-system-2.md`

## 风险与后续

- 本 PR 是 Design System 2.0 的原子升级，当前 size gate 统计为 4,895 行，超过 3,000 行体量门槛；已添加 `size-override`，核心组件行为、预览和迁移边界仍保持在同一发布单元内
- 预览构建仍有 Vite 单 chunk 超过 500 kB 的提示，这是组件全集预览页的既有打包形态，不阻塞本次发布
- 下一阶段再将 2.0 Token 和组件逐步迁移到 `web/app` 与 `@zooclaw/chat-ui`，每次修改 chat 相关页面前需要同时读取两侧代码判断归属

```

---

## fix(models): resolve display region from current org (#3553)
- sha: `3acaa2defcf62b52152913fb0be39276933d95d5`
- 作者: sam-srp
- 日期: 2026-08-27T10:21:42Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/3acaa2defcf62b52152913fb0be39276933d95d5
- PR: #3553

### 完整 commit message

```
fix(models): resolve display region from current org (#3553)

## Summary
- Resolve model display region from the user's single active
organization for both personal and team orgs.
- Fall back to the Cloudflare `cf-ipcountry` region, then `CN`, when the
active org has no valid `region_code`.
- Apply the same display-name policy to the chat model catalog and
Settings Usage while preserving model IDs, entitlements, and unmapped
models.
- Forward `cf-ipcountry` through the web BFF to claw-interface; no new
environment variables are required.

## Root cause
The existing regional display resolver only applied organization
overrides to team orgs and returned original metadata for personal
users. It also had no request-region input, because the generic web BFF
did not forward Cloudflare's country header to the model catalog or
usage-record endpoints.

## Test plan
- [x] Backend regional policy tests cover personal/team org overrides,
missing org fields, CF fallback, `XX`, invalid values, and `CN`
fallback.
- [x] Backend model catalog and Settings Usage route tests verify the
request region reaches the shared display resolver.
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh web/app/src/lib/api/claw-proxy.ts
web/app/tests/unit/lib/api/claw-proxy.unit.spec.ts`
- [x] 66 focused backend unit tests.
```

### PR description

```
## Summary
- Resolve model display region from the user's single active organization for both personal and team orgs.
- Fall back to the Cloudflare `cf-ipcountry` region, then `CN`, when the active org has no valid `region_code`.
- Apply the same display-name policy to the chat model catalog and Settings Usage while preserving model IDs, entitlements, and unmapped models.
- Forward `cf-ipcountry` through the web BFF to claw-interface; no new environment variables are required.

## Root cause
The existing regional display resolver only applied organization overrides to team orgs and returned original metadata for personal users. It also had no request-region input, because the generic web BFF did not forward Cloudflare's country header to the model catalog or usage-record endpoints.

## Test plan
- [x] Backend regional policy tests cover personal/team org overrides, missing org fields, CF fallback, `XX`, invalid values, and `CN` fallback.
- [x] Backend model catalog and Settings Usage route tests verify the request region reaches the shared display resolver.
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh web/app/src/lib/api/claw-proxy.ts web/app/tests/unit/lib/api/claw-proxy.unit.spec.ts`
- [x] 66 focused backend unit tests.

```

---

## fix(web): route legacy Creem billing to support (#3546)
- sha: `5e485f139c25b27b3f04152aba0deb60bab5c5d1`
- 作者: tim-srp
- 日期: 2026-08-27T10:05:28Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/5e485f139c25b27b3f04152aba0deb60bab5c5d1
- PR: #3546

### 完整 commit message

```
fix(web): route legacy Creem billing to support (#3546)

## Summary

- recognize persisted legacy `creem` subscriptions as a non-self-service
billing channel
- hide plan changes, cancellation, Stripe portal, and payment-method
actions for those subscriptions
- keep the existing billing-support entry point visible and fail closed
before any provider request if a legacy cancellation is invoked
indirectly
- leave current Airwallex `card` subscription management unchanged

## Root cause

PR #3485 removed the Creem runtime based on the assumption that
production had no real Creem users or orders. Production still contains
active legacy agreements with `provider=creem`. The web client did not
recognize that runtime value and fell through to Stripe cancellation and
portal behavior.

Creem API configuration and lifecycle services have already been
removed, so these subscriptions cannot be canceled safely through the
current provider-neutral Card endpoint. This PR deliberately routes
affected users to billing support instead of restoring the retired
provider integration or performing a local-only cancellation.

## Test plan

- [x] TDD RED confirmed legacy Creem users saw Cancel and Stripe Payment
Method actions
- [x] TDD RED confirmed the billing service attempted a provider request
for Creem cancellation
- [x] targeted regression suite — 139 passed
- [x] `bash scripts/verify-web.sh ...` — TypeScript, 401 tests (1
skipped), ESLint passed
- [x] pre-commit frontend and backend quality hooks
```

### PR description

```
## Summary

- recognize persisted legacy `creem` subscriptions as a non-self-service billing channel
- hide plan changes, cancellation, Stripe portal, and payment-method actions for those subscriptions
- keep the existing billing-support entry point visible and fail closed before any provider request if a legacy cancellation is invoked indirectly
- leave current Airwallex `card` subscription management unchanged

## Root cause

PR #3485 removed the Creem runtime based on the assumption that production had no real Creem users or orders. Production still contains active legacy agreements with `provider=creem`. The web client did not recognize that runtime value and fell through to Stripe cancellation and portal behavior.

Creem API configuration and lifecycle services have already been removed, so these subscriptions cannot be canceled safely through the current provider-neutral Card endpoint. This PR deliberately routes affected users to billing support instead of restoring the retired provider integration or performing a local-only cancellation.

## Test plan

- [x] TDD RED confirmed legacy Creem users saw Cancel and Stripe Payment Method actions
- [x] TDD RED confirmed the billing service attempted a provider request for Creem cancellation
- [x] targeted regression suite — 139 passed
- [x] `bash scripts/verify-web.sh ...` — TypeScript, 401 tests (1 skipped), ESLint passed
- [x] pre-commit frontend and backend quality hooks

```

---

## fix(settings): refine API keys page layout (#3552)
- sha: `6d2b0f0b655b12d255632f011a77b45a127a5ae2`
- 作者: lynn Zhuang
- 日期: 2026-08-27T09:35:02Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/6d2b0f0b655b12d255632f011a77b45a127a5ae2
- PR: #3552

### 完整 commit message

```
fix(settings): refine API keys page layout (#3552)

## Summary
- align API key page actions, empty state, and one-time secret dialog
with the approved settings layout
- simplify API guidance copy and keep quickstart links contextual to
each state
- fit populated key rows within the card using compact dates,
truncation, and a stable minimum content width
- keep table rows transparent while their action menus are open

## Root cause
The API key page mixed duplicated guidance and actions with
unconstrained table content. The shared table row also applies a muted
background whenever a descendant menu trigger is expanded, which caused
an unintended row highlight.

## Test plan
- [x] `bash scripts/verify-web.sh
'src/app/[locale]/(app)/claw-settings/components/ApiKeysTab.tsx'
'tests/unit/app/claw-settings/ApiKeysTab.unit.spec.tsx'`
- [x] `bash scripts/verify-changed.sh`
- [x] `pnpm exec vitest run --config ./vitest.config.mts
tests/unit/app/claw-settings/ApiKeysTab.unit.spec.tsx` (57 tests)
- [x] Verify the populated table has no horizontal overflow
(`clientWidth === scrollWidth`)
- [x] Verify an expanded row action menu leaves the row background
transparent
```

### PR description

```
## Summary
- align API key page actions, empty state, and one-time secret dialog with the approved settings layout
- simplify API guidance copy and keep quickstart links contextual to each state
- fit populated key rows within the card using compact dates, truncation, and a stable minimum content width
- keep table rows transparent while their action menus are open

## Root cause
The API key page mixed duplicated guidance and actions with unconstrained table content. The shared table row also applies a muted background whenever a descendant menu trigger is expanded, which caused an unintended row highlight.

## Test plan
- [x] `bash scripts/verify-web.sh 'src/app/[locale]/(app)/claw-settings/components/ApiKeysTab.tsx' 'tests/unit/app/claw-settings/ApiKeysTab.unit.spec.tsx'`
- [x] `bash scripts/verify-changed.sh`
- [x] `pnpm exec vitest run --config ./vitest.config.mts tests/unit/app/claw-settings/ApiKeysTab.unit.spec.tsx` (57 tests)
- [x] Verify the populated table has no horizontal overflow (`clientWidth === scrollWidth`)
- [x] Verify an expanded row action menu leaves the row background transparent

```

---

## feat(admin): manage organization regions (#3551)
- sha: `07f75707fd21e44f76d1b3e177939568ee133713`
- 作者: sam-srp
- 日期: 2026-08-27T09:25:19Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/07f75707fd21e44f76d1b3e177939568ee133713
- PR: #3551

### 完整 commit message

```
feat(admin): manage organization regions (#3551)

## Linear

N/A

## Summary
- move region-code administration from the Users page to a dedicated
Orgs page backed by `ecap-orgs`
- add admin organization listing with pagination and filters for org ID,
org name, org type, and region code
- keep all organization fields read-only except `region_code`, and show
missing persisted regions as `Empty`
- omit the deprecated `warm_pool_size` field from the admin response and
table
- remove the obsolete Users region filter and its backend
lookup/service/repository code

## Test plan
- [x] Dashboard console full test suite: 651 tests
- [x] Dashboard console typecheck and ESLint
- [x] Dashboard console production build
- [x] Claw interface focused unit tests: 40 tests
- [x] Ruff, Pyright, and import-linter

## Deployment
- deploy `services/claw-interface`
- deploy `web/dashboard-console`
```

### PR description

```
## Linear

N/A

## Summary
- move region-code administration from the Users page to a dedicated Orgs page backed by `ecap-orgs`
- add admin organization listing with pagination and filters for org ID, org name, org type, and region code
- keep all organization fields read-only except `region_code`, and show missing persisted regions as `Empty`
- omit the deprecated `warm_pool_size` field from the admin response and table
- remove the obsolete Users region filter and its backend lookup/service/repository code

## Test plan
- [x] Dashboard console full test suite: 651 tests
- [x] Dashboard console typecheck and ESLint
- [x] Dashboard console production build
- [x] Claw interface focused unit tests: 40 tests
- [x] Ruff, Pyright, and import-linter

## Deployment
- deploy `services/claw-interface`
- deploy `web/dashboard-console`

```

---

## fix(agent-builder): start engine after only-me publish (#3547)
- sha: `5ed3dc2f6c30359236818b510657c7055153ced3`
- 作者: sharplee-srp
- 日期: 2026-08-27T09:24:04Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/5ed3dc2f6c30359236818b510657c7055153ced3
- PR: #3547

### 完整 commit message

```
fix(agent-builder): start engine after only-me publish (#3547)

## Summary
- complete every Engine Only-me installation so an `active` Workspace is
also started
- wait for an in-progress Engine install, then update to the newly
published Pack version before completing and starting it
- preserve the existing computer-runtime install/update flow and add
regression coverage for both runtimes

## Root cause

Agent Builder treated the product Workspace status `active` as proof
that an Engine runtime was already running. A newly installed Engine
therefore skipped `completeEngineInstall` and `/start`. Existing Engine
installations with a stale submission ran `/update` after the completion
decision and were never started either. Reordering those calls must also
preserve the backend's active-workspace precondition, so an existing
`installing` Engine is awaited before `/update`.

## Test plan
- [x] `pnpm exec vitest run
tests/unit/services/agent-builder-publish.unit.spec.ts`
- [x] `bash scripts/verify-web.sh
web/app/src/services/agent-builder-publish.ts
web/app/tests/unit/services/agent-builder-publish.unit.spec.ts`
- [x] `bash scripts/verify-changed.sh`
```

### PR description

```
## Summary
- complete every Engine Only-me installation so an `active` Workspace is also started
- wait for an in-progress Engine install, then update to the newly published Pack version before completing and starting it
- preserve the existing computer-runtime install/update flow and add regression coverage for both runtimes

## Root cause

Agent Builder treated the product Workspace status `active` as proof that an Engine runtime was already running. A newly installed Engine therefore skipped `completeEngineInstall` and `/start`. Existing Engine installations with a stale submission ran `/update` after the completion decision and were never started either. Reordering those calls must also preserve the backend's active-workspace precondition, so an existing `installing` Engine is awaited before `/update`.

## Test plan
- [x] `pnpm exec vitest run tests/unit/services/agent-builder-publish.unit.spec.ts`
- [x] `bash scripts/verify-web.sh web/app/src/services/agent-builder-publish.ts web/app/tests/unit/services/agent-builder-publish.unit.spec.ts`
- [x] `bash scripts/verify-changed.sh`

```

---

## fix(user-menu): 优化账户套餐卡片布局 (#3550)
- sha: `10716ef25abaa70184969de2a30744ff3066a585`
- 作者: lynn Zhuang
- 日期: 2026-08-27T09:23:45Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/10716ef25abaa70184969de2a30744ff3066a585
- PR: #3550

### 完整 commit message

```
fix(user-menu): 优化账户套餐卡片布局 (#3550)

## 变更摘要
- 确保账户套餐操作按钮始终单行显示，并保持水平、垂直居中
- 优化窄侧边栏下套餐标题、续费文案与操作按钮之间的间距
- 将“积分”文字与套餐标题左对齐，同时保留积分图标和帮助入口

## 根因

套餐操作按钮位于弹性布局中，但没有禁止收缩和中文逐字换行，因此在空间不足时“管理”会被拆成两行。套餐信息与按钮之间也没有稳定的间距约束；此外，积分图标位于文字前方，导致“积分”文字无法与套餐标题左对齐。

## 验证
- [x] `bash scripts/verify-web.sh web/app/src/components/UserMenu.tsx`
- [x] Chromium 中文模拟账户验证：“管理”单行显示并保持水平、垂直居中
- [x] Chromium 几何验证：套餐信息区与操作按钮保持 12px 间距
- [x] Chromium 几何验证：“积分”与“Ultra”左边界差值为 0px
```

### PR description

```
## 变更摘要
- 确保账户套餐操作按钮始终单行显示，并保持水平、垂直居中
- 优化窄侧边栏下套餐标题、续费文案与操作按钮之间的间距
- 将“积分”文字与套餐标题左对齐，同时保留积分图标和帮助入口

## 根因
套餐操作按钮位于弹性布局中，但没有禁止收缩和中文逐字换行，因此在空间不足时“管理”会被拆成两行。套餐信息与按钮之间也没有稳定的间距约束；此外，积分图标位于文字前方，导致“积分”文字无法与套餐标题左对齐。

## 验证
- [x] `bash scripts/verify-web.sh web/app/src/components/UserMenu.tsx`
- [x] Chromium 中文模拟账户验证：“管理”单行显示并保持水平、垂直居中
- [x] Chromium 几何验证：套餐信息区与操作按钮保持 12px 间距
- [x] Chromium 几何验证：“积分”与“Ultra”左边界差值为 0px

```

---

## fix(web): 隐藏过期的引导与功能发布弹窗 (#3549)
- sha: `5120d60ce79cb7c96e226f689c7578a8cd7880b7`
- 作者: lynn Zhuang
- 日期: 2026-08-27T08:27:27Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/5120d60ce79cb7c96e226f689c7578a8cd7880b7
- PR: #3549

### 完整 commit message

```
fix(web): 隐藏过期的引导与功能发布弹窗 (#3549)

## 背景

Guide Tour 和 Feature Launch 轮播在公告内容过期后仍会全局挂载，符合条件的用户可能继续看到旧的「One brain.
Full crew.」和「PPTX Master just leveled up」弹窗。

## 改动内容

- 通过独立开关暂停自动展示 Guide Tour，并隐藏用户菜单中的 `What's New` 入口
- 暂停聊天页的 Feature Launch / PPTX 轮播弹窗，包括仅开发环境使用的 `?force-launch=1` 路径
- 保留两个弹窗的现有实现和内容，后续有新内容时只需重新开启对应开关
- 将 Feature Launch 开关与弹窗组件模块解耦，避免整模块 mock 缺少开关导出

## 验证

- [x] 相关 TypeScript 类型检查通过
- [x] 相关 Vitest：60 个测试通过
- [x] mock backend：34 个测试通过
- [x] ESLint 通过
- [x] pre-push changed-surface 验证通过
- [x] 本地浏览器验证：Guide Tour、`What's New` 入口和 Feature Launch
弹窗均不再出现，`?force-launch=1` 也无法绕过开关
- [x] GitHub CI：38/38 检查通过

## 风险与恢复方式

本次只控制组件挂载，不删除弹窗实现，风险较低。后续需要重新展示时，将对应开关设为开启并更新内容即可。
```

### PR description

```
## 背景

Guide Tour 和 Feature Launch 轮播在公告内容过期后仍会全局挂载，符合条件的用户可能继续看到旧的「One brain. Full crew.」和「PPTX Master just leveled up」弹窗。

## 改动内容

- 通过独立开关暂停自动展示 Guide Tour，并隐藏用户菜单中的 `What's New` 入口
- 暂停聊天页的 Feature Launch / PPTX 轮播弹窗，包括仅开发环境使用的 `?force-launch=1` 路径
- 保留两个弹窗的现有实现和内容，后续有新内容时只需重新开启对应开关
- 将 Feature Launch 开关与弹窗组件模块解耦，避免整模块 mock 缺少开关导出

## 验证

- [x] 相关 TypeScript 类型检查通过
- [x] 相关 Vitest：60 个测试通过
- [x] mock backend：34 个测试通过
- [x] ESLint 通过
- [x] pre-push changed-surface 验证通过
- [x] 本地浏览器验证：Guide Tour、`What's New` 入口和 Feature Launch 弹窗均不再出现，`?force-launch=1` 也无法绕过开关
- [x] GitHub CI：38/38 检查通过

## 风险与恢复方式

本次只控制组件挂载，不删除弹窗实现，风险较低。后续需要重新展示时，将对应开关设为开启并更新内容即可。

```

---

## feat(invitation): gate the invited-trial login behind an invitation dialog (#3542)
- sha: `d99ad16170d5bc3264bde0eb4821adcaf614b11e`
- 作者: david-srp
- 日期: 2026-08-27T06:31:22Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/d99ad16170d5bc3264bde0eb4821adcaf614b11e
- PR: #3542

### 完整 commit message

```
feat(invitation): gate the invited-trial login behind an invitation dialog (#3542)

## What

Reworks `/invitation/login` — the invited-trial entry into ZooWork
Business — and leaves the `/bossclaw` campaign wizard alone.

The old flow had a specific failure: you typed a phone number, landed on
a code field, and assumed the SMS was on its way. It wasn't — that field
wanted an **invitation code**, and no SMS is sent until the code passes.
People sat waiting for a message that was never sent.

## Changes

**Invite code is now a gate, not a step.** It opens as a dialog over the
phone screen, which stays visible underneath. That frames it as "one
more thing before we continue" instead of "you advanced, here is the
code field", and carries the ceremony the route is named after. The
dialog restates the phone it is acting on, says outright that the SMS
only goes out once the code passes, shows a worked example (`例如
ZC-64ACFC`), and points at `sales@zoowork.ai` for anyone without an
invite.

It is hand-rolled rather than `@/components/ds/dialog`: this is a
branded module with a fixed palette and the shadcn primitive's
`bg-popover` / `bg-card` tokens cascade against it (per
`web/app/AGENTS.md` → Branded modules). It reuses the repo's
`useBodyLock` + `useEscapeKey`, focuses the code field on open, traps
focus, and is flex-centred inside a scrollable overlay so a mobile
keyboard can scroll it into view rather than pinning it underneath.

**SMS step says what it wants.** Copy names 短信验证码 explicitly, and the
code renders as six boxes so it reads as a 6-digit SMS code rather than
a free-text field. One real input is stretched transparently across the
boxes instead of six separate inputs — that keeps iOS one-time-code
autofill, paste and backspace working with no cross-input focus
juggling. Resend became a quiet inline link and 返回上一步 a de-emphasised
text link.

**Dropped the STEP kickers.** The numbering read as chrome; the headline
already says where you are.

**Copy rebuilt from zoowork.ai's own claims** — 不只是回答 / 交付真实成果, 按角色限权,
行业模板. Removed 工作区 and Agent Pack from the brand panel: both are internal
vocabulary that appears nowhere on the marketing site. Contact address
is `sales@zoowork.ai`.

**Light theme with a toggle** (bottom-right, follows the OS by default).
The palette is mirrored under `prefers-color-scheme` and the
`data-boss-theme` attribute is only stamped for an explicit choice, so
the default path resolves in CSS with no JS and no dark first paint —
verified before hydration.

## Review fixes folded in

A multi-agent adversarial pass produced 35 findings; 18 survived
independent verification and are fixed here. The substantive ones:

- The light palette failed the contrast bar the file documents four
lines above it — 2.35:1 on the field placeholder and 2.86:1 on
`.heroStats dd`. Retuned `--boss-muted` / `--boss-muted-2`; both now
clear 4.5:1 against the darkest stop of the stage gradient.
- Light mode painted dark first (theme applied from an effect). Fixed by
the `prefers-color-scheme` mirror above.
- The invitation screen asserted 验证码暂未发送, but `back()` re-enters that
step from verification where an SMS *had* gone out. It states the
condition now.
- 验证并进入工作区 / 正在进入您的 ZooWork 工作区 lied for `return_to` arrivals, which go
back to the campaign. Both are conditional.
- Removing the kickers left `.title`'s kicker-gap as dead space; zeroed
only where the title leads.

## Scope

`/bossclaw` is untouched — the wizard's components are not in this diff.
The shared `bossclaw.module.css` gains login-only rules; every light
rule is behind `[data-boss-theme]` or `prefers-color-scheme`, and the
wizard never sets that attribute.

Also widens `bossclaw-subset-fonts.sh` to scan `invitation/` as well. It
only scanned `bossclaw/`, so login copy never reached the glyph set —
the characters happened to be covered by the wizard's copy, not by
design.

## Testing

`bash scripts/verify-web.sh` green: guards + `tsc` + **108 vitest** +
eslint.

New coverage: the gate renders with `aria-modal` over a still-mounted
phone screen, dismisses back to it, the SMS field keeps `one-time-code`
+ `maxlength=6` while six boxes mirror it, non-digits are stripped, the
destination copy is conditional, and the theme hook's OS listener
detaches on unmount (its own helper existed for this and never asserted
it).

Rendered at 1440 / 390 in both themes.

## Known gaps

- **Android hardware back** leaves the page rather than closing the
gate. A `history.pushState` sentinel raced the App Router into a
`popstate` that dismissed the dialog on the same tick it opened, so the
step snapped straight back to the phone screen; it was removed. Doing
this properly needs intercepting routes. Behaviour matches what shipped
before, so this is not a regression.
- `lib/auth/manager.ts` still throws an error naming
`marketing@zooclaw.ai` and "注册bossclaw". It can surface on this page,
but the module is shared with the wizard, so changing it would alter
wizard-visible copy — left for a separate call.
- The brand panel names 微信 · 企微 · 飞书. zoowork.ai's marketing copy names
Slack / Teams / Lark and does not name WeChat (they exist as product
connectors). Kept deliberately for the domestic invited-enterprise
audience; flagging in case this should follow the site.
```

### PR description

```
## What

Reworks `/invitation/login` — the invited-trial entry into ZooWork Business — and leaves the `/bossclaw` campaign wizard alone.

The old flow had a specific failure: you typed a phone number, landed on a code field, and assumed the SMS was on its way. It wasn't — that field wanted an **invitation code**, and no SMS is sent until the code passes. People sat waiting for a message that was never sent.

## Changes

**Invite code is now a gate, not a step.** It opens as a dialog over the phone screen, which stays visible underneath. That frames it as "one more thing before we continue" instead of "you advanced, here is the code field", and carries the ceremony the route is named after. The dialog restates the phone it is acting on, says outright that the SMS only goes out once the code passes, shows a worked example (`例如 ZC-64ACFC`), and points at `sales@zoowork.ai` for anyone without an invite.

It is hand-rolled rather than `@/components/ds/dialog`: this is a branded module with a fixed palette and the shadcn primitive's `bg-popover` / `bg-card` tokens cascade against it (per `web/app/AGENTS.md` → Branded modules). It reuses the repo's `useBodyLock` + `useEscapeKey`, focuses the code field on open, traps focus, and is flex-centred inside a scrollable overlay so a mobile keyboard can scroll it into view rather than pinning it underneath.

**SMS step says what it wants.** Copy names 短信验证码 explicitly, and the code renders as six boxes so it reads as a 6-digit SMS code rather than a free-text field. One real input is stretched transparently across the boxes instead of six separate inputs — that keeps iOS one-time-code autofill, paste and backspace working with no cross-input focus juggling. Resend became a quiet inline link and 返回上一步 a de-emphasised text link.

**Dropped the STEP kickers.** The numbering read as chrome; the headline already says where you are.

**Copy rebuilt from zoowork.ai's own claims** — 不只是回答 / 交付真实成果, 按角色限权, 行业模板. Removed 工作区 and Agent Pack from the brand panel: both are internal vocabulary that appears nowhere on the marketing site. Contact address is `sales@zoowork.ai`.

**Light theme with a toggle** (bottom-right, follows the OS by default). The palette is mirrored under `prefers-color-scheme` and the `data-boss-theme` attribute is only stamped for an explicit choice, so the default path resolves in CSS with no JS and no dark first paint — verified before hydration.

## Review fixes folded in

A multi-agent adversarial pass produced 35 findings; 18 survived independent verification and are fixed here. The substantive ones:

- The light palette failed the contrast bar the file documents four lines above it — 2.35:1 on the field placeholder and 2.86:1 on `.heroStats dd`. Retuned `--boss-muted` / `--boss-muted-2`; both now clear 4.5:1 against the darkest stop of the stage gradient.
- Light mode painted dark first (theme applied from an effect). Fixed by the `prefers-color-scheme` mirror above.
- The invitation screen asserted 验证码暂未发送, but `back()` re-enters that step from verification where an SMS *had* gone out. It states the condition now.
- 验证并进入工作区 / 正在进入您的 ZooWork 工作区 lied for `return_to` arrivals, which go back to the campaign. Both are conditional.
- Removing the kickers left `.title`'s kicker-gap as dead space; zeroed only where the title leads.

## Scope

`/bossclaw` is untouched — the wizard's components are not in this diff. The shared `bossclaw.module.css` gains login-only rules; every light rule is behind `[data-boss-theme]` or `prefers-color-scheme`, and the wizard never sets that attribute.

Also widens `bossclaw-subset-fonts.sh` to scan `invitation/` as well. It only scanned `bossclaw/`, so login copy never reached the glyph set — the characters happened to be covered by the wizard's copy, not by design.

## Testing

`bash scripts/verify-web.sh` green: guards + `tsc` + **108 vitest** + eslint.

New coverage: the gate renders with `aria-modal` over a still-mounted phone screen, dismisses back to it, the SMS field keeps `one-time-code` + `maxlength=6` while six boxes mirror it, non-digits are stripped, the destination copy is conditional, and the theme hook's OS listener detaches on unmount (its own helper existed for this and never asserted it).

Rendered at 1440 / 390 in both themes.

## Known gaps

- **Android hardware back** leaves the page rather than closing the gate. A `history.pushState` sentinel raced the App Router into a `popstate` that dismissed the dialog on the same tick it opened, so the step snapped straight back to the phone screen; it was removed. Doing this properly needs intercepting routes. Behaviour matches what shipped before, so this is not a regression.
- `lib/auth/manager.ts` still throws an error naming `marketing@zooclaw.ai` and "注册bossclaw". It can surface on this page, but the module is shared with the wizard, so changing it would alter wizard-visible copy — left for a separate call.
- The brand panel names 微信 · 企微 · 飞书. zoowork.ai's marketing copy names Slack / Teams / Lark and does not name WeChat (they exist as product connectors). Kept deliberately for the domestic invited-enterprise audience; flagging in case this should follow the site.

```

---

## perf(agent-builder): speed up project creation (#3545)
- sha: `71a591f55b46017b875519a958ed97d6247f2e37`
- 作者: kaka-srp
- 日期: 2026-08-27T06:14:14Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/71a591f55b46017b875519a958ed97d6247f2e37
- PR: #3545

### 完整 commit message

```
perf(agent-builder): speed up project creation (#3545)

## Summary

- Navigate to the new Agent Builder Project page as soon as the Project
record is persisted, then continue model, attachment, and first-turn
initialization on that page.
- Serialize Engine v2 setup across pods with a renewable Mongo lease and
skip redundant synchronous LLM title generation for the dedicated
Builder session.
- Preserve same-tab `File` objects for the full setup window, keep
interactions locked from the first preparing frame, and show accessible
animated progress plus explicit retry only when recovery is possible.
- Document the production trace findings, ownership model, failure
recovery, and cross-Project callback isolation in
`docs/superpowers/specs/2026-08-27-agent-builder-fast-project-creation.md`.

## Root cause

The Project document itself was created in roughly 32 ms, but the create
screen waited for runtime/session setup, selected-model application,
attachments, and the first turn before navigating. Duplicate setup
runners on separate pods also each made an unnecessary synchronous
title-generation call; the observed calls took about 21 and 28 seconds.

## Test plan

- [x] `255` targeted backend unit tests passed for Project repository,
routes, and service setup behavior.
- [x] `139` targeted frontend unit tests passed for create navigation,
pending initialization, Project interaction locking, recovery, and
preparing UI.
- [x] Full pre-commit gates passed: frontend ESLint; Python ruff/format,
file length, dependency consistency, import-linter, repo-list sync, and
Pyright.
- [x] `pnpm exec tsc --noEmit` passed.
- [x] Pyright on every changed Python file passed with `0 errors`.
- [x] Final independent code review passed with no findings after fixes
for lease ownership, handoff lifetime, retry semantics, first-frame
locking, and cross-Project async callback isolation.
- [x] CI checks pass (`45/45`).

## Known baseline issue

The full local `verify-changed` Pyright run still reports four existing
errors in unchanged route-helper tests (`_route_helpers.py`,
`test_org_skills_routes.py`, and `test_skills_manager_routes.py`). Those
files are identical to `origin/main`; all Python files changed by this
PR pass Pyright. The branch was pushed with only that local verification
step bypassed after the remaining web, Python, import-contract,
unit-test, and size gates passed.
```

### PR description

```
## Summary

- Navigate to the new Agent Builder Project page as soon as the Project record is persisted, then continue model, attachment, and first-turn initialization on that page.
- Serialize Engine v2 setup across pods with a renewable Mongo lease and skip redundant synchronous LLM title generation for the dedicated Builder session.
- Preserve same-tab `File` objects for the full setup window, keep interactions locked from the first preparing frame, and show accessible animated progress plus explicit retry only when recovery is possible.
- Document the production trace findings, ownership model, failure recovery, and cross-Project callback isolation in `docs/superpowers/specs/2026-08-27-agent-builder-fast-project-creation.md`.

## Root cause

The Project document itself was created in roughly 32 ms, but the create screen waited for runtime/session setup, selected-model application, attachments, and the first turn before navigating. Duplicate setup runners on separate pods also each made an unnecessary synchronous title-generation call; the observed calls took about 21 and 28 seconds.

## Test plan

- [x] `255` targeted backend unit tests passed for Project repository, routes, and service setup behavior.
- [x] `139` targeted frontend unit tests passed for create navigation, pending initialization, Project interaction locking, recovery, and preparing UI.
- [x] Full pre-commit gates passed: frontend ESLint; Python ruff/format, file length, dependency consistency, import-linter, repo-list sync, and Pyright.
- [x] `pnpm exec tsc --noEmit` passed.
- [x] Pyright on every changed Python file passed with `0 errors`.
- [x] Final independent code review passed with no findings after fixes for lease ownership, handoff lifetime, retry semantics, first-frame locking, and cross-Project async callback isolation.
- [x] CI checks pass (`45/45`).

## Known baseline issue

The full local `verify-changed` Pyright run still reports four existing errors in unchanged route-helper tests (`_route_helpers.py`, `test_org_skills_routes.py`, and `test_skills_manager_routes.py`). Those files are identical to `origin/main`; all Python files changed by this PR pass Pyright. The branch was pushed with only that local verification step bypassed after the remaining web, Python, import-contract, unit-test, and size gates passed.

```

---

## fix(compliance): align regional model display and login (#3543)
- sha: `11e74bde540bdaf0c5cb89c8dc9e4068308862e2`
- 作者: sam-srp
- 日期: 2026-08-27T04:17:10Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/11e74bde540bdaf0c5cb89c8dc9e4068308862e2
- PR: #3543

### 完整 commit message

```
fix(compliance): align regional model display and login (#3543)

## Summary

- resolve mainland email OTP eligibility from the authoritative
gem_account profile identifier instead of the optional account email
field
- reuse generic region_code model display overrides in usage records
while preserving raw model IDs
- render configured display names in Settings usage with
backward-compatible fallback to original LiteLLM model names

## Validation

- backend targeted unit suite: 79 passed
- frontend unit suite: 9,236 passed, 70 skipped, 1 todo
- Ruff check/format, targeted Pyright, import-linter
- frontend ESLint, TypeScript, and CI lint hard gates
```

### PR description

```
## Summary

- resolve mainland email OTP eligibility from the authoritative gem_account profile identifier instead of the optional account email field
- reuse generic region_code model display overrides in usage records while preserving raw model IDs
- render configured display names in Settings usage with backward-compatible fallback to original LiteLLM model names

## Validation

- backend targeted unit suite: 79 passed
- frontend unit suite: 9,236 passed, 70 skipped, 1 todo
- Ruff check/format, targeted Pyright, import-linter
- frontend ESLint, TypeScript, and CI lint hard gates
```

---

## fix(agent-builder): finish empty engine turns (#3539)
- sha: `7b8524d3067c65774fb0cbc4d79e24feebcd4e61`
- 作者: kaka-srp
- 日期: 2026-08-27T03:34:44Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/7b8524d3067c65774fb0cbc4d79e24feebcd4e61
- PR: #3539

### 完整 commit message

```
fix(agent-builder): finish empty engine turns (#3539)

## Summary

- Accept hidden `custom_turn_status` posts in Agent Builder monitoring
and finalization.
- Treat a terminal status as the end of an Engine preview turn even when
the assistant produces no visible response.
- Keep tool-progress posts out of visible-reply detection and show the
completed-without-visible-response state.

## Root cause

Agent Builder depended on a terminal assistant segment to end an Engine
preview turn. Runs that emitted tool progress and then finished without
a visible assistant segment never reached that boundary; tool metadata
could also be mistaken for an assistant delivery. Refreshing reloaded
the same incomplete event history, so it did not resolve the stuck
state.

## Scope

- ECAP consumer changes only; no Engine changes.
- Agent Builder monitor/finalizer, preview state derivation, and shared
chat message labeling.
- Producer PR:
https://github.com/SerendipityOneInc/agent-channel-service/pull/94

## Test plan

- [x] Targeted claw-interface tests (207 passed)
- [x] Agent Builder terminal-status component regression (1 passed)
- [x] Turn-status parser regression (1 passed)
- [x] Shared chat message-helper tests (12 passed)
- [ ] Full local suite intentionally skipped at request; PR CI is
authoritative.

## Rollout

Deploy this backward-compatible consumer first, then the linked Agent
Channel Service producer.
```

### PR description

```
## Summary

- Accept hidden `custom_turn_status` posts in Agent Builder monitoring and finalization.
- Treat a terminal status as the end of an Engine preview turn even when the assistant produces no visible response.
- Keep tool-progress posts out of visible-reply detection and show the completed-without-visible-response state.

## Root cause

Agent Builder depended on a terminal assistant segment to end an Engine preview turn. Runs that emitted tool progress and then finished without a visible assistant segment never reached that boundary; tool metadata could also be mistaken for an assistant delivery. Refreshing reloaded the same incomplete event history, so it did not resolve the stuck state.

## Scope

- ECAP consumer changes only; no Engine changes.
- Agent Builder monitor/finalizer, preview state derivation, and shared chat message labeling.
- Producer PR: https://github.com/SerendipityOneInc/agent-channel-service/pull/94

## Test plan

- [x] Targeted claw-interface tests (207 passed)
- [x] Agent Builder terminal-status component regression (1 passed)
- [x] Turn-status parser regression (1 passed)
- [x] Shared chat message-helper tests (12 passed)
- [ ] Full local suite intentionally skipped at request; PR CI is authoritative.

## Rollout

Deploy this backward-compatible consumer first, then the linked Agent Channel Service producer.

```

---

## fix(marketing): restore approved ZooWork homepage (#3522)
- sha: `e1977c82b7ed84ed7d82b150c4f7385e8d44f891`
- 作者: shana-srp
- 日期: 2026-08-27T03:15:46Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/e1977c82b7ed84ed7d82b150c4f7385e8d44f891
- PR: #3522

### 完整 commit message

```
fix(marketing): restore approved ZooWork homepage (#3522)

## Linear

N/A

## Summary

- Restore the user-approved ZooWork homepage visual baseline from
[`f4c986e`](https://github.com/SerendipityOneInc/ecap-workspace/commit/f4c986e9dbe4ae9a216c8593f89db9ec47484d30)
while keeping the current WebApp architecture.
- Render all eight homepage sections as native React components styled
through the shared Tailwind token system.
- Restore the approved interaction details: five distinct run-stage
screens, three distinct Workplace screens, integration pings, the Agent
Builder publish loop, ZooData extraction motion, and the outcomes
carousel.
- Restore the full Zenith Operations API workplace instead of the
simplified replacement, and fix the header logo's intrinsic aspect ratio
so its 1446×390 source stays sharp.
- Remove the CRM header icon, Marcelo avatar, and the two decorative
animals from the App Store QR dialog.
- Retain current `main` routing, locale/SEO handling, auth tracking,
shared marketing chrome, dependency state, and later security fixes.

## Why

PR
[#3401](https://github.com/SerendipityOneInc/ecap-workspace/pull/3401)
was merged with a final tree that does not match the user-confirmed
homepage version. The acceptance baseline is the historical commit above
and this confirmed preview:

- [Approved
preview](https://pr3401-f4c986e.zoowork-preview.pages.dev/new-chat)

This repair does not reset the repository or reuse the merged feature
branch. It forward-ports only the approved homepage visuals and behavior
onto current `main`.

## Implementation

- Remove the temporary `srcDoc`/iframe implementation, embedded HTML
document, standalone CSS, and standalone JavaScript.
- Use native React sections for Hero, role carousel, run demo, platform,
Agent Runtime, workplace, outcomes, security, and final CTA.
- Keep homepage colors in shared semantic Tailwind tokens and motion in
`motion/react`; no injected `<style>` blocks or imperative DOM animation
scripts remain.
- Preserve the approved PNG canvas background while retaining the
current WebP asset used elsewhere.
- Keep native route dictionaries and current CTA/login behavior.
- Document the migration and rollback strategy in
`docs/superpowers/specs/2026-08-26-restore-approved-zoowork-homepage.md`.

## Validation

- `bash scripts/verify-web.sh` in a non-sandbox environment:
  - governance guards passed;
  - TypeScript passed;
  - 670 test files passed;
  - 9,209 tests passed, 70 skipped, 1 todo;
  - ESLint passed.
- Focused homepage verification: 48 tests passed.
- Pre-push changed-surface verification passed.
- GitHub web quality, build, CodeQL, title, and size checks passed.
- Real route checks against the local Next.js server:
  - `/` → HTTP 200;
  - `/en` → canonical HTTP 301 redirect to `/`;
  - `/zh` → HTTP 200;
- `/new-chat` → HTTP 200 as a real application route, not a homepage
fallback.

## Visual QA

- Compared Hero, role carousel, run demo, platform/Runtime, workplace,
outcomes, security, and CTA against the approved preview section by
section.
- Confirmed every run-stage tab and Workplace tab renders its own
screen, rather than only restyling a shared frame.
- Confirmed integration, Agent Builder, ZooData, and autoplay motion
runs through native React/Motion code with reduced-motion support.
- Confirmed the preview returns the original PNG/WebP/SVG bytes for Next
image URLs; the header logo renders from its 1446×390 source at the
correct aspect ratio.
- Store Analyst / Deal Desk and other autoplay areas can show a
different dynamic frame at capture time; layout and visual treatment
remain aligned.
- Verified the CRM header icon and Marcelo avatar are absent.
- Verified the QR dialog contains only the QR code and no decorative
animals.
- Screenshots are stored locally under `.screenshots/` and are
intentionally not committed.

## Rollback

The pre-migration static version remains available at commit
`51745959543727093e018607015be252588f0a22` and remote backup branch
`codex/backup-zoowork-home-static-51745959`.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR description

```
## Linear

N/A

## Summary

- Restore the user-approved ZooWork homepage visual baseline from [`f4c986e`](https://github.com/SerendipityOneInc/ecap-workspace/commit/f4c986e9dbe4ae9a216c8593f89db9ec47484d30) while keeping the current WebApp architecture.
- Render all eight homepage sections as native React components styled through the shared Tailwind token system.
- Restore the approved interaction details: five distinct run-stage screens, three distinct Workplace screens, integration pings, the Agent Builder publish loop, ZooData extraction motion, and the outcomes carousel.
- Restore the full Zenith Operations API workplace instead of the simplified replacement, and fix the header logo's intrinsic aspect ratio so its 1446×390 source stays sharp.
- Remove the CRM header icon, Marcelo avatar, and the two decorative animals from the App Store QR dialog.
- Retain current `main` routing, locale/SEO handling, auth tracking, shared marketing chrome, dependency state, and later security fixes.

## Why

PR [#3401](https://github.com/SerendipityOneInc/ecap-workspace/pull/3401) was merged with a final tree that does not match the user-confirmed homepage version. The acceptance baseline is the historical commit above and this confirmed preview:

- [Approved preview](https://pr3401-f4c986e.zoowork-preview.pages.dev/new-chat)

This repair does not reset the repository or reuse the merged feature branch. It forward-ports only the approved homepage visuals and behavior onto current `main`.

## Implementation

- Remove the temporary `srcDoc`/iframe implementation, embedded HTML document, standalone CSS, and standalone JavaScript.
- Use native React sections for Hero, role carousel, run demo, platform, Agent Runtime, workplace, outcomes, security, and final CTA.
- Keep homepage colors in shared semantic Tailwind tokens and motion in `motion/react`; no injected `<style>` blocks or imperative DOM animation scripts remain.
- Preserve the approved PNG canvas background while retaining the current WebP asset used elsewhere.
- Keep native route dictionaries and current CTA/login behavior.
- Document the migration and rollback strategy in `docs/superpowers/specs/2026-08-26-restore-approved-zoowork-homepage.md`.

## Validation

- `bash scripts/verify-web.sh` in a non-sandbox environment:
  - governance guards passed;
  - TypeScript passed;
  - 670 test files passed;
  - 9,209 tests passed, 70 skipped, 1 todo;
  - ESLint passed.
- Focused homepage verification: 48 tests passed.
- Pre-push changed-surface verification passed.
- GitHub web quality, build, CodeQL, title, and size checks passed.
- Real route checks against the local Next.js server:
  - `/` → HTTP 200;
  - `/en` → canonical HTTP 301 redirect to `/`;
  - `/zh` → HTTP 200;
  - `/new-chat` → HTTP 200 as a real application route, not a homepage fallback.

## Visual QA

- Compared Hero, role carousel, run demo, platform/Runtime, workplace, outcomes, security, and CTA against the approved preview section by section.
- Confirmed every run-stage tab and Workplace tab renders its own screen, rather than only restyling a shared frame.
- Confirmed integration, Agent Builder, ZooData, and autoplay motion runs through native React/Motion code with reduced-motion support.
- Confirmed the preview returns the original PNG/WebP/SVG bytes for Next image URLs; the header logo renders from its 1446×390 source at the correct aspect ratio.
- Store Analyst / Deal Desk and other autoplay areas can show a different dynamic frame at capture time; layout and visual treatment remain aligned.
- Verified the CRM header icon and Marcelo avatar are absent.
- Verified the QR dialog contains only the QR code and no decorative animals.
- Screenshots are stored locally under `.screenshots/` and are intentionally not committed.

## Rollback

The pre-migration static version remains available at commit `51745959543727093e018607015be252588f0a22` and remote backup branch `codex/backup-zoowork-home-static-51745959`.

```

---

## feat(ios): cut over to v2 engine agent runtime and remove v1 computer code (#3526)
- sha: `5be94784978d3379b316b6f651309574e42e0d78`
- 作者: bill-srp
- 日期: 2026-08-27T03:02:17Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/5be94784978d3379b316b6f651309574e42e0d78
- PR: #3526

### 完整 commit message

```
feat(ios): cut over to v2 engine agent runtime and remove v1 computer code (#3526)

## Linear
<!-- no Linear issue for this task -->

## Summary
- **iOS becomes V2-only.** The ZooClaw app had zero awareness of the
engine (V2) runtime: every agent call was gated on a "primary computer",
boot did `POST /computers`, and Mattermost connect required an agent
literally named `main`. For an AGENTS_V2 user this created a stray V1
computer and never connected chat (`/account/me.mattermost_bots` is
projected from the primary *computer's* workspaces → `[]`; the engine
main agent id is `agt_*`). Design:
`docs/superpowers/specs/2026-08-26-ios-v2-engine-cutover.md`.
- **Removed V1:** `BotService`, `BotViewModel(+Provisioning)`,
`ComputerModels`, `BotInfo/*Response`, `SkillsStatusReport`, untyped
cron parsing, Settings "Redeploy/Recreate Bot", agent identity/avatar
editing (no engine endpoint), `StorageService`, and every `/computers/*`
+ `/openclaw/*` call (grep is empty).
- **Runtime readiness** (`AgentRuntimeViewModel`): `GET
/agents/install-capability` → non-`engine` ⇒ `.notEligible`; else poll
`GET /agents` (2s, ≤300s) until the `is_main` row is `active` with a DM
channel ⇒ `.ready`. Never creates a computer. Retries on foreground
after `.error`; cancellation returns to `.idle`.
- **Identity rule:** every installed-agent key in the app is the
`workspace_id`; main agent = `is_main` (no string compares). Persisted
caches move to `.v2` keys so V1-shaped caches are ignored; a cached bot
list without a main bot is treated as V1 and dropped.
- **Agents:** `GET /agents` (paginated, both runtimes); hire =
duplicate-by-pack guard → `POST /agents {pack_id}` (409
`already_installed`/`operation_in_progress` ⇒ re-list and reuse) → poll
until `active` (terminal on
`install_failed|error|disabled|uninstalling|uninstall_failed|deleting`,
fail-fast if the row disappears) → `POST /agents/{ws}/start` only for
fresh installs; fire = `POST …/uninstall`; update = `POST …/update` +
poll. Failure detail comes from `engine.status_message` (backend
`AgentPublic` has no `error_message`). `hasUpdate` merges official + org
catalogs.
- **Chat:** still Mattermost — the whole `MattermostViewModel` stack is
unchanged; the per-agent channel map is now built from `/agents` rows
(best-effort: an `/agents` failure no longer fails `/account/me` or
ejects the session). Connect gate = any bot with a DM channel, main
preferred.
- **Settings sheet:** model picker only, via `GET /models` + `GET/PUT
/agents/{ws}/model` (disabled when `model_managed`).
- **Conversations:** `/agents/{ws}/conversations`; create uses the
SSE-only `…/conversations/stream` (new `NetworkService.streamLines` with
termination cleanup) — resolves on `conversation_created`, applies
`title_ready` asynchronously.
- **Skills / Schedules:** `GET /agents/{ws}/skills` (scope `global|pack`
= official, `org|personal` = community); read-only schedules fan-out
over `GET /agents/{ws}/schedules` (≤3 concurrent), typed models, error
state surfaced when every fetch fails.
- Out of scope (follow-up PR): V2 chat semantics — `assistant_segment`
terminal marker, `tool_status` activity label, hidden `/stop` control
post, `zooclaw_artifacts` envelope; schedule create/trigger/runs; engine
channels; artifact library.

## Rollout
- Legacy (computer-runtime) accounts see an explicit "not enabled for
the new runtime" state — there is no V1 fallback in this build. Ship to
TestFlight/App Store **before** the production `AGENTS_V2_ENABLED` flip;
staging is open-rollout for smoke.

## Test plan
- [x] `swiftlint --strict` — 0 violations
- [x] `xcodebuild build` (iPhone 17 Pro simulator) — BUILD SUCCEEDED
- [x] Whole `ZooClawTests` + UI bundle — all passing (counts in the PR
checks); coverage restored for install decision (POST → poll → start
ordering, 409 reuse, duplicate reuse, terminal statuses, missing row),
fire/update, runtime readiness negatives, cancellation, cache migration,
`/account/me.mattermost_bots` ignored, connect gate without literal
`main`, SSE parser, model save gating, skills scope filter, schedule
mapping/batching/failure
- [ ] Staging smoke with a fresh account: register → onboarding agent
select → main agent ready → chat round-trip → hire a pack → model picker
→ skills store → schedule tab
- [ ] Staging smoke with an existing V2 account upgrading from the
shipping build (cache migration path)
```

### PR description

```
## Linear
<!-- no Linear issue for this task -->

## Summary
- **iOS becomes V2-only.** The ZooClaw app had zero awareness of the engine (V2) runtime: every agent call was gated on a "primary computer", boot did `POST /computers`, and Mattermost connect required an agent literally named `main`. For an AGENTS_V2 user this created a stray V1 computer and never connected chat (`/account/me.mattermost_bots` is projected from the primary *computer's* workspaces → `[]`; the engine main agent id is `agt_*`). Design: `docs/superpowers/specs/2026-08-26-ios-v2-engine-cutover.md`.
- **Removed V1:** `BotService`, `BotViewModel(+Provisioning)`, `ComputerModels`, `BotInfo/*Response`, `SkillsStatusReport`, untyped cron parsing, Settings "Redeploy/Recreate Bot", agent identity/avatar editing (no engine endpoint), `StorageService`, and every `/computers/*` + `/openclaw/*` call (grep is empty).
- **Runtime readiness** (`AgentRuntimeViewModel`): `GET /agents/install-capability` → non-`engine` ⇒ `.notEligible`; else poll `GET /agents` (2s, ≤300s) until the `is_main` row is `active` with a DM channel ⇒ `.ready`. Never creates a computer. Retries on foreground after `.error`; cancellation returns to `.idle`.
- **Identity rule:** every installed-agent key in the app is the `workspace_id`; main agent = `is_main` (no string compares). Persisted caches move to `.v2` keys so V1-shaped caches are ignored; a cached bot list without a main bot is treated as V1 and dropped.
- **Agents:** `GET /agents` (paginated, both runtimes); hire = duplicate-by-pack guard → `POST /agents {pack_id}` (409 `already_installed`/`operation_in_progress` ⇒ re-list and reuse) → poll until `active` (terminal on `install_failed|error|disabled|uninstalling|uninstall_failed|deleting`, fail-fast if the row disappears) → `POST /agents/{ws}/start` only for fresh installs; fire = `POST …/uninstall`; update = `POST …/update` + poll. Failure detail comes from `engine.status_message` (backend `AgentPublic` has no `error_message`). `hasUpdate` merges official + org catalogs.
- **Chat:** still Mattermost — the whole `MattermostViewModel` stack is unchanged; the per-agent channel map is now built from `/agents` rows (best-effort: an `/agents` failure no longer fails `/account/me` or ejects the session). Connect gate = any bot with a DM channel, main preferred.
- **Settings sheet:** model picker only, via `GET /models` + `GET/PUT /agents/{ws}/model` (disabled when `model_managed`).
- **Conversations:** `/agents/{ws}/conversations`; create uses the SSE-only `…/conversations/stream` (new `NetworkService.streamLines` with termination cleanup) — resolves on `conversation_created`, applies `title_ready` asynchronously.
- **Skills / Schedules:** `GET /agents/{ws}/skills` (scope `global|pack` = official, `org|personal` = community); read-only schedules fan-out over `GET /agents/{ws}/schedules` (≤3 concurrent), typed models, error state surfaced when every fetch fails.
- Out of scope (follow-up PR): V2 chat semantics — `assistant_segment` terminal marker, `tool_status` activity label, hidden `/stop` control post, `zooclaw_artifacts` envelope; schedule create/trigger/runs; engine channels; artifact library.

## Rollout
- Legacy (computer-runtime) accounts see an explicit "not enabled for the new runtime" state — there is no V1 fallback in this build. Ship to TestFlight/App Store **before** the production `AGENTS_V2_ENABLED` flip; staging is open-rollout for smoke.

## Test plan
- [x] `swiftlint --strict` — 0 violations
- [x] `xcodebuild build` (iPhone 17 Pro simulator) — BUILD SUCCEEDED
- [x] Whole `ZooClawTests` + UI bundle — all passing (counts in the PR checks); coverage restored for install decision (POST → poll → start ordering, 409 reuse, duplicate reuse, terminal statuses, missing row), fire/update, runtime readiness negatives, cancellation, cache migration, `/account/me.mattermost_bots` ignored, connect gate without literal `main`, SSE parser, model save gating, skills scope filter, schedule mapping/batching/failure
- [ ] Staging smoke with a fresh account: register → onboarding agent select → main agent ready → chat round-trip → hire a pack → model picker → skills store → schedule tab
- [ ] Staging smoke with an existing V2 account upgrading from the shipping build (cache migration path)

```

---

## fix(billing): recover Apple paid renewals (#3524)
- sha: `63ac01c0a9850cb45d34a65fec2214635c319a5e`
- 作者: sharplee-srp
- 日期: 2026-08-27T02:41:57Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/63ac01c0a9850cb45d34a65fec2214635c319a5e
- PR: #3524

### 完整 commit message

```
fix(billing): recover Apple paid renewals (#3524)

## Summary
- allow a provider-authenticated Apple paid period to reactivate an
expired agreement only when its period end is strictly newer
- persist unexpected Apple processing errors as failed provider events,
so retries are not permanently ACKed as duplicates
- preserve a recovered paid period when an older non-revocation Apple
loss notification arrives out of order

## Root cause
Apple renewal processing persisted the succeeded payment order before
updating the subscription agreement and granting the entitlement. A
billing-recovery notification then attempted `expired -> active`, which
the generic agreement state machine rejected. That exception is a
`ValueError`, while the Apple adapter only marked `ServiceError`
failures, so the provider event remained in `processing`. Duplicate
delivery treated `processing` as a completed duplicate and returned
success, leaving the succeeded order without an entitlement.

The reactivation exception is deliberately narrow: provider actor only,
same provider, `expired -> active`, current agreement, and a strictly
newer paid period. Other terminal transitions remain invalid.

Apple loss handling ignores only non-revocation facts whose period end
is strictly older than the current paid period. Eligible loss writes use
the agreement period snapshot as a compare-and-set guard so a concurrent
recovery cannot be overwritten; `REVOKE` remains authoritative.

## Operational note
- this prevents the state-transition exception from leaving new Apple
events stuck in `processing`
- existing orphan orders are not automatically replayed because stored
Apple payloads are redacted; repair should use verified Apple source
data in a separate controlled production operation
- no production data is changed by this PR

## Test plan
- [x] `pytest -q tests/unit/test_apple_billing_v2.py
tests/unit/test_billing_v2_subscription_agreements.py` — 63 passed
- [x] `pytest -q tests/unit -k 'billing_v2 or apple'` — 749 passed, 5
skipped
- [x] `bash scripts/verify-py.sh` — Ruff, format, Pyright, and
import-linter passed
- [x] all `scripts/ci-lint/*.sh` checks passed
```

### PR description

```
## Summary
- allow a provider-authenticated Apple paid period to reactivate an expired agreement only when its period end is strictly newer
- persist unexpected Apple processing errors as failed provider events, so retries are not permanently ACKed as duplicates
- preserve a recovered paid period when an older non-revocation Apple loss notification arrives out of order

## Root cause
Apple renewal processing persisted the succeeded payment order before updating the subscription agreement and granting the entitlement. A billing-recovery notification then attempted `expired -> active`, which the generic agreement state machine rejected. That exception is a `ValueError`, while the Apple adapter only marked `ServiceError` failures, so the provider event remained in `processing`. Duplicate delivery treated `processing` as a completed duplicate and returned success, leaving the succeeded order without an entitlement.

The reactivation exception is deliberately narrow: provider actor only, same provider, `expired -> active`, current agreement, and a strictly newer paid period. Other terminal transitions remain invalid.

Apple loss handling ignores only non-revocation facts whose period end is strictly older than the current paid period. Eligible loss writes use the agreement period snapshot as a compare-and-set guard so a concurrent recovery cannot be overwritten; `REVOKE` remains authoritative.

## Operational note
- this prevents the state-transition exception from leaving new Apple events stuck in `processing`
- existing orphan orders are not automatically replayed because stored Apple payloads are redacted; repair should use verified Apple source data in a separate controlled production operation
- no production data is changed by this PR

## Test plan
- [x] `pytest -q tests/unit/test_apple_billing_v2.py tests/unit/test_billing_v2_subscription_agreements.py` — 63 passed
- [x] `pytest -q tests/unit -k 'billing_v2 or apple'` — 749 passed, 5 skipped
- [x] `bash scripts/verify-py.sh` — Ruff, format, Pyright, and import-linter passed
- [x] all `scripts/ci-lint/*.sh` checks passed

```

---

## fix(billing): use card trial end for access (#3541)
- sha: `f50c5e89c9c90e87dc64789e8d76ad8d481dbc2e`
- 作者: tim-srp
- 日期: 2026-08-27T02:43:20Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/f50c5e89c9c90e87dc64789e8d76ad8d481dbc2e
- PR: #3541

### 完整 commit message

```
fix(billing): use card trial end for access (#3541)

## Summary

- use Airwallex `trial_ends_at` as the Billing v2 trial access boundary
- keep the provider `current_period_end` as the separate billing-period
fact
- align the trial agreement, entitlement, and checkout projection end
times
- safely shorten pre-fix succeeded checkout projections during replay

## Root cause

Airwallex trial events expose both a trial end and a subscription
billing-period end. The trial settlement projected `current_period_end`
into every trial boundary. For annual Starter trials this made the UI
calculate roughly 372 days remaining instead of 7 days and could also
extend the entitlement incorrectly.

Existing succeeded projections are reconciled only when the complete
order/subscription/agreement/entitlement identity matches and the stored
trial end is longer than the corrected end.

## Test plan

- `services/claw-interface/.venv/bin/pytest
tests/unit/test_card_checkout_projection_repo.py
tests/unit/test_airwallex_trial_lifecycle.py -q`
- `bash scripts/verify-py.sh`
- pre-push `bash scripts/verify-changed.sh`
```

### PR description

```
## Summary

- use Airwallex `trial_ends_at` as the Billing v2 trial access boundary
- keep the provider `current_period_end` as the separate billing-period fact
- align the trial agreement, entitlement, and checkout projection end times
- safely shorten pre-fix succeeded checkout projections during replay

## Root cause

Airwallex trial events expose both a trial end and a subscription billing-period end. The trial settlement projected `current_period_end` into every trial boundary. For annual Starter trials this made the UI calculate roughly 372 days remaining instead of 7 days and could also extend the entitlement incorrectly.

Existing succeeded projections are reconciled only when the complete order/subscription/agreement/entitlement identity matches and the stored trial end is longer than the corrected end.

## Test plan

- `services/claw-interface/.venv/bin/pytest tests/unit/test_card_checkout_projection_repo.py tests/unit/test_airwallex_trial_lifecycle.py -q`
- `bash scripts/verify-py.sh`
- pre-push `bash scripts/verify-changed.sh`

```

---

