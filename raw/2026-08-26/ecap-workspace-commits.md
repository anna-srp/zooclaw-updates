# SerendipityOneInc/ecap-workspace — commits 2026-08-26

## fix(billing): tolerate Airwallex period correction on scheduled cancellation (#3538)

- **SHA**: `c699341914c4dddc02233de390644c92b1dcd08e`
- **作者**: tim-srp
- **日期**: 2026-08-26T14:45:28Z
- **PR**: #3538

### Commit Message

```
fix(billing): tolerate Airwallex period correction on scheduled cancellation (#3538)

## Summary

- 用户在 zooclaw.ai 取消 Airwallex 订阅时报错 `Airwallex returned a different
subscription period`,取消操作被本地拒绝
- 放宽 `_validate_provider_response` 的 period 校验:provider
是计费周期的权威来源,period 漂移时接受并以 provider 为准回写,同时记录
`airwallex_provider_period_drift` warning 日志便于观测
- 受影响用户重新点一次「取消订阅」即可自动对齐本地与 provider 的周期,无需数据修补

## Root cause

Airwallex 对 trial 订阅,`current_period_ends_at` 定义为「当前已开票周期的结束」= trial
结束后第一个付费周期结束(trial_ends_at + 一个计费月)。本地在创建时(webhook
快照)忠实记录该值。取消订阅(`cancel_at_period_end=true`)后,Airwallex 把
`current_period_ends_at` 修正为实际到期日(trial 结束)——字段是动态变化的,并非稳定周期边界。本地取消路径对
provider 返回的 period 做严格相等校验 → 对 trial 订阅必然失败(差 30 天整,2592000 秒)。

## Changes

- `app/services/airwallex/subscription_changes.py` —
`_validate_provider_response`:保持 identity / terminal status / period
缺失校验严格;period 与本地不一致改为接受 + 回写 provider 值 +
`airwallex_provider_period_drift` warning 日志
- `tests/unit/test_airwallex_subscription_changes.py` — 移除「period 漂移 →
拒绝」case;新增 cancel 接受修正周期并写回、resume 恢复完整周期并写回 2 个测试

## Test plan

- [x] `verify-py.sh`(ruff + pyright + import-linter)通过
- [x] `test_airwallex_subscription_changes.py` +
`test_airwallex_subscription_plan_changes.py` 46 个测试全部通过(plan change
复用同一校验函数,语义一致)

---------

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

## Summary

- 用户在 zooclaw.ai 取消 Airwallex 订阅时报错 `Airwallex returned a different subscription period`,取消操作被本地拒绝
- 放宽 `_validate_provider_response` 的 period 校验:provider 是计费周期的权威来源,period 漂移时接受并以 provider 为准回写,同时记录 `airwallex_provider_period_drift` warning 日志便于观测
- 受影响用户重新点一次「取消订阅」即可自动对齐本地与 provider 的周期,无需数据修补

## Root cause

Airwallex 对 trial 订阅,`current_period_ends_at` 定义为「当前已开票周期的结束」= trial 结束后第一个付费周期结束(trial_ends_at + 一个计费月)。本地在创建时(webhook 快照)忠实记录该值。取消订阅(`cancel_at_period_end=true`)后,Airwallex 把 `current_period_ends_at` 修正为实际到期日(trial 结束)——字段是动态变化的,并非稳定周期边界。本地取消路径对 provider 返回的 period 做严格相等校验 → 对 trial 订阅必然失败(差 30 天整,2592000 秒)。

## Changes

- `app/services/airwallex/subscription_changes.py` — `_validate_provider_response`:保持 identity / terminal status / period 缺失校验严格;period 与本地不一致改为接受 + 回写 provider 值 + `airwallex_provider_period_drift` warning 日志
- `tests/unit/test_airwallex_subscription_changes.py` — 移除「period 漂移 → 拒绝」case;新增 cancel 接受修正周期并写回、resume 恢复完整周期并写回 2 个测试

## Test plan

- [x] `verify-py.sh`(ruff + pyright + import-linter)通过
- [x] `test_airwallex_subscription_changes.py` + `test_airwallex_subscription_plan_changes.py` 46 个测试全部通过(plan change 复用同一校验函数,语义一致)


---

## fix(invitation): restore BossClaw registration route (#3536)

- **SHA**: `dbdc4ab5ca4ba9e787404e4dc8ffbcfaf1d8080d`
- **作者**: tim-srp
- **日期**: 2026-08-26T14:14:09Z
- **PR**: #3536

### Commit Message

```
fix(invitation): restore BossClaw registration route (#3536)

## Summary

- Restore the campaign and registration page at `/[locale]/bossclaw`.
- Keep the login page at `/[locale]/invitation/login`.
- Remove `/[locale]/bossclaw/login` and the `/[locale]/invitation` page
so only the requested URLs are exposed.
- Update return-to validation and route-dependent tests for this split
URL structure.

## Validation

- `pnpm --dir web/app exec vitest run tests/unit/bossclaw` (96 passed)
```

### PR Body

## Summary

- Restore the campaign and registration page at `/[locale]/bossclaw`.
- Keep the login page at `/[locale]/invitation/login`.
- Remove `/[locale]/bossclaw/login` and the `/[locale]/invitation` page so only the requested URLs are exposed.
- Update return-to validation and route-dependent tests for this split URL structure.

## Validation

- `pnpm --dir web/app exec vitest run tests/unit/bossclaw` (96 passed)


---

## fix(r2): update allowed origin to zoowork.ai (#3535)

- **SHA**: `8940bf7d236ca1d64b59e96264753347ea8b68cd`
- **作者**: tim-srp
- **日期**: 2026-08-26T13:55:23Z
- **PR**: #3535

### Commit Message

```
fix(r2): update allowed origin to zoowork.ai (#3535)

## Summary

- Update the production R2 access worker CORS origin from
`https://zooclaw.ai` to `https://zoowork.ai`.
- Update the worker tests to cover the migrated origin.

## Validation

- `git diff --check`
- Vitest and TypeScript checks could not run because this worktree has
no installed `node_modules`.
```

### PR Body

## Summary

- Update the production R2 access worker CORS origin from `https://zooclaw.ai` to `https://zoowork.ai`.
- Update the worker tests to cover the migrated origin.

## Validation

- `git diff --check`
- Vitest and TypeScript checks could not run because this worktree has no installed `node_modules`.


---

## fix(web): hide unsupported session delete action (#3534)

- **SHA**: `fdcd34db3ff42415400000f173021415039f3c04`
- **作者**: sharplee-srp
- **日期**: 2026-08-26T13:42:03Z
- **PR**: #3534

### Commit Message

```
fix(web): hide unsupported session delete action (#3534)

## Summary
- Hide the unsupported Delete action from the session overflow menu
until its dependencies are implemented.
- Keep the existing Delete item behind a temporary off switch and a TODO
so it can be restored without reconstructing the UI.
- Let the menu collapse to its single Rename action while preserving its
existing width and styling.
- Add a regression assertion that the Delete action is not rendered.

## Root cause
The session menu rendered a disabled Delete item even though no frontend
mutation or backend service exists for deleting sessions. This exposed
an action that could never succeed.

## Test plan
- [x] `bash scripts/verify-web.sh
web/app/src/components/sidenav/SideNavSessionRow.tsx
web/app/tests/unit/components/sidenav/SideNavSessionRow.unit.spec.tsx`
- [x] `pnpm exec vitest run
tests/unit/components/sidenav/SideNavSessionRow.unit.spec.tsx` (24
tests)
- [x] Pre-push changed-surface verification (`bash
scripts/verify-changed.sh`)
```

### PR Body

## Summary
- Hide the unsupported Delete action from the session overflow menu until its dependencies are implemented.
- Keep the existing Delete item behind a temporary off switch and a TODO so it can be restored without reconstructing the UI.
- Let the menu collapse to its single Rename action while preserving its existing width and styling.
- Add a regression assertion that the Delete action is not rendered.

## Root cause
The session menu rendered a disabled Delete item even though no frontend mutation or backend service exists for deleting sessions. This exposed an action that could never succeed.

## Test plan
- [x] `bash scripts/verify-web.sh web/app/src/components/sidenav/SideNavSessionRow.tsx web/app/tests/unit/components/sidenav/SideNavSessionRow.unit.spec.tsx`
- [x] `pnpm exec vitest run tests/unit/components/sidenav/SideNavSessionRow.unit.spec.tsx` (24 tests)
- [x] Pre-push changed-surface verification (`bash scripts/verify-changed.sh`)


---

## feat(settings): tell users what to do with an API key (#3533)

- **SHA**: `2f5ff75cc502e7eb31507d7569de82ed872b5047`
- **作者**: finn-srp
- **日期**: 2026-08-26T13:36:07Z
- **PR**: #3533

### Commit Message

```
feat(settings): tell users what to do with an API key (#3533)

## Linear
<!-- 无关联 issue -->

## Summary

API Keys tab 发得出密钥，但从不说这密钥能干什么。三个触点补上：

- **页头**加常驻「文档」链接，指向 quickstart（不是文档根）。始终英文——文档站自带语言切换，而 App 有 10 个
locale、文档站只有 2 个，按 locale 拼路径迟早拼出 404。
- **空状态**改成讲用途（脚本 / 后端服务 / AI 编码助手），并直接给出 skill
安装命令。落在这一屏、手上还没有密钥的人，就是接下来要接入的那个人——personal org
里创建者和接入者按定义是同一个人（`ClawSettingsClient.tsx` 的门是 `org_type === 'personal'
|| role === 'admin'`）。
- **创建成功后的密钥弹窗**给出「下一步」。**轮换不给**——轮换的人早已接入过，此时他要的是速度。

顺带修掉引导过程中量出来的两个既有缺陷：

- **弹窗在手机上横向溢出 229px。** `DialogContent` 是 grid，隐式单列轨道按最宽子元素的 max-content
定宽，而 `code` 是 `whitespace-nowrap`，把轨道撑爆视口，密钥的 Copy 按钮整个跑到屏幕外。给轨道加
`grid-cols-[minmax(0,1fr)]` 后，滚动交回给 `code` 自己已有的 `overflow-x-auto`。375px
实测溢出 229 → 0。
- **页头操作行 `shrink-0`，撑破 settings 内容区而不是换行。** 内容区远比视口窄，所以横排断点从 `sm:` 挪到
`lg:`，并在 `lg:` 以上钉住行宽让标题让位。768px 实测行内溢出 376 → 0。

### 密钥弹窗的关闭规则

**Escape 照常关闭，点弹窗外面不关。** Escape
是刻意按下的，不是需要防的那种误触；停在遮罩上的一次误点才是，而这一屏的内容关掉就再也拿不回来。实测「从密钥文字上开始拖选、松手落在弹窗外」也不会关（文字照常能选中）。

规则只有一行 `onInteractOutside`，不需要按「屏幕上有没有密钥」分支——Escape
永远可用，就不存在把人锁死的风险，标准键盘行为也原样保留。

同时加了「完成 / Done」按钮：原本唯一的显式出口是右上角 32px 的 ×（实测对比度 3.74:1），作为这一屏的主要退出方式太小了。

### 复制走 `useCopyToClipboard`

命令块最初手写了一条 promise chain。这有个真实后果：`navigator.clipboard` 是 secure-context
gated 的，`http://` 源上这个属性根本不存在，于是读 `.writeText` 会在 `.catch()`
挂上之前同步抛错，我们承诺的「复制失败，请手动选中」提示永远不显示——恰恰在最需要它的场景里失灵。

`usehooks-ts` 是本 workspace 对浏览器 API hook 的既定选型（见
`web/app/AGENTS.md`「默认技术选型」），已经在依赖里，且自带 `useCopyToClipboard`：API
缺失和写入被拒都返回 `false`。改用它是**删代码**，不是再加一层防护。

> 全站另有 12 处手写 `clipboard.writeText`，5 种不同的错误处理策略（静默吞、裸
await、守卫后静默返回、发射后不管、`.then` 链）。不在本 PR 范围，值得单开清理。

### 文案

产品名改为 **ZooWork**（原文写的是「调用 ZooClaw API」，而它指向的文档、SDK 包、skill 仓都叫
ZooWork）。只有 `settings.apiKeys.description` 带产品名，且只有 en/zh 翻译了这个块，其余 8
个语言走英文 fallback，所以两条字符串覆盖全部读者。

**docs host 仍是
`zooclaw.ai`**，等文档站迁移完再换。常量处加了注释，说明这个与周边文案的品牌不一致是有意的，不是笔误。

## Test plan

- [x] `bash scripts/verify-web.sh` 全绿：tsc + eslint + **9222 项单测**（本文件 50
条）
- [x] `pnpm run lint:ci` 全绿（dependency-cruiser + knip；这层 `verify-web.sh`
不覆盖）
- [x] 本地 mock 栈实测创建与轮换两条流程，中英双语 × 明暗双主题
- [x] 375 / 768 / 1280 三档宽度实测：页面级 `scrollWidth > clientWidth` 均为 false
- [x] 真浏览器逐条验证关闭规则：点遮罩不关、拖选出界不关、Escape 关闭、「完成」关闭
- [x] 实测剪贴板缺失（`navigator.clipboard` 置 undefined）时会显示手动复制提示
- [x] 实测「复制命令」写入的是命令而非密钥

## 已知未解

375px 下这一屏依然散架，但根因是 claw-settings 这个壳没有移动端布局，内容区被压到 0–75px；未改动的 General
tab 一样如此（实测其 h2 仅 48px 宽）。不在本 PR 范围。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: wangfulong <wfllike@gmail.com>
Co-authored-by: Claude Opus 5 <noreply@anthropic.com>
```

### PR Body

## Linear
<!-- 无关联 issue -->

## Summary

API Keys tab 发得出密钥，但从不说这密钥能干什么。三个触点补上：

- **页头**加常驻「文档」链接，指向 quickstart（不是文档根）。始终英文——文档站自带语言切换，而 App 有 10 个 locale、文档站只有 2 个，按 locale 拼路径迟早拼出 404。
- **空状态**改成讲用途（脚本 / 后端服务 / AI 编码助手），并直接给出 skill 安装命令。落在这一屏、手上还没有密钥的人，就是接下来要接入的那个人——personal org 里创建者和接入者按定义是同一个人（`ClawSettingsClient.tsx` 的门是 `org_type === 'personal' || role === 'admin'`）。
- **创建成功后的密钥弹窗**给出「下一步」。**轮换不给**——轮换的人早已接入过，此时他要的是速度。

顺带修掉引导过程中量出来的两个既有缺陷：

- **弹窗在手机上横向溢出 229px。** `DialogContent` 是 grid，隐式单列轨道按最宽子元素的 max-content 定宽，而 `code` 是 `whitespace-nowrap`，把轨道撑爆视口，密钥的 Copy 按钮整个跑到屏幕外。给轨道加 `grid-cols-[minmax(0,1fr)]` 后，滚动交回给 `code` 自己已有的 `overflow-x-auto`。375px 实测溢出 229 → 0。
- **页头操作行 `shrink-0`，撑破 settings 内容区而不是换行。** 内容区远比视口窄，所以横排断点从 `sm:` 挪到 `lg:`，并在 `lg:` 以上钉住行宽让标题让位。768px 实测行内溢出 376 → 0。

### 密钥弹窗的关闭规则

**Escape 照常关闭，点弹窗外面不关。** Escape 是刻意按下的，不是需要防的那种误触；停在遮罩上的一次误点才是，而这一屏的内容关掉就再也拿不回来。实测「从密钥文字上开始拖选、松手落在弹窗外」也不会关（文字照常能选中）。

规则只有一行 `onInteractOutside`，不需要按「屏幕上有没有密钥」分支——Escape 永远可用，就不存在把人锁死的风险，标准键盘行为也原样保留。

同时加了「完成 / Done」按钮：原本唯一的显式出口是右上角 32px 的 ×（实测对比度 3.74:1），作为这一屏的主要退出方式太小了。

### 复制走 `useCopyToClipboard`

命令块最初手写了一条 promise chain。这有个真实后果：`navigator.clipboard` 是 secure-context gated 的，`http://` 源上这个属性根本不存在，于是读 `.writeText` 会在 `.catch()` 挂上之前同步抛错，我们承诺的「复制失败，请手动选中」提示永远不显示——恰恰在最需要它的场景里失灵。

`usehooks-ts` 是本 workspace 对浏览器 API hook 的既定选型（见 `web/app/AGENTS.md`「默认技术选型」），已经在依赖里，且自带 `useCopyToClipboard`：API 缺失和写入被拒都返回 `false`。改用它是**删代码**，不是再加一层防护。

> 全站另有 12 处手写 `clipboard.writeText`，5 种不同的错误处理策略（静默吞、裸 await、守卫后静默返回、发射后不管、`.then` 链）。不在本 PR 范围，值得单开清理。

### 文案

产品名改为 **ZooWork**（原文写的是「调用 ZooClaw API」，而它指向的文档、SDK 包、skill 仓都叫 ZooWork）。只有 `settings.apiKeys.description` 带产品名，且只有 en/zh 翻译了这个块，其余 8 个语言走英文 fallback，所以两条字符串覆盖全部读者。

**docs host 仍是 `zooclaw.ai`**，等文档站迁移完再换。常量处加了注释，说明这个与周边文案的品牌不一致是有意的，不是笔误。

## Test plan

- [x] `bash scripts/verify-web.sh` 全绿：tsc + eslint + **9222 项单测**（本文件 50 条）
- [x] `pnpm run lint:ci` 全绿（dependency-cruiser + knip；这层 `verify-web.sh` 不覆盖）
- [x] 本地 mock 栈实测创建与轮换两条流程，中英双语 × 明暗双主题
- [x] 375 / 768 / 1280 三档宽度实测：页面级 `scrollWidth > clientWidth` 均为 false
- [x] 真浏览器逐条验证关闭规则：点遮罩不关、拖选出界不关、Escape 关闭、「完成」关闭
- [x] 实测剪贴板缺失（`navigator.clipboard` 置 undefined）时会显示手动复制提示
- [x] 实测「复制命令」写入的是命令而非密钥

## 已知未解

375px 下这一屏依然散架，但根因是 claw-settings 这个壳没有移动端布局，内容区被压到 0–75px；未改动的 General tab 一样如此（实测其 h2 仅 48px 宽）。不在本 PR 范围。

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## fix(registration): skip warm pool and V1 app creation for V2-eligible users (#3532)

- **SHA**: `466df714fcb9757f996ff55f07a39e57e87f957c`
- **作者**: tim-srp
- **日期**: 2026-08-26T11:27:29Z
- **PR**: #3532

### Commit Message

```
fix(registration): skip warm pool and V1 app creation for V2-eligible users (#3532)

## Problem

Staging `POST /account/personal-org` fails for new users with 503
`account.openclaw_app_initialization_failed`. Root-cause chain:

```
node-pool scale-down (infra-pool -> 0) -> V1 FastClaw has no instances
-> Envoy overload 503 -> register() unconditionally calls V1 create_app in its fallback -> registration 503
```

Even with `AGENTS_V2_ENABLED=true`, `register()` has no V2 branch:
warm-pool claims require V1-provisioned `openclaw_app` assets, and the
fallback always creates a V1 app.

## Fix

`register()` now judges V2 eligibility with the same
`get_agents_v2_eligibility` gate engine agent install uses
(`engine_main_agent_service`):

- **V2-eligible**: skip `claim_warm_pool_account` and
`create_openclaw_app_record` entirely; `openclaw_app` stays `None`.
Billing init + upsert unchanged — the proven fallback path minus the V1
app. A FastClaw outage (or an empty/disabled warm pool) no longer blocks
registration.
- **Non-eligible**: legacy warm-pool → V1-app flow untouched (safe for
future production partial rollout).

Downstream is already decoupled: org creation only needs the billing
`team_id`, billing keys come from `ensure_billing_initialized`, and
default-main-agent provisioning only reads `(uid, org_id, token)` with
the same eligibility gate as its first check. The register response
schema never serialized `openclaw_app`, so there is no API-compat
impact.

Complements the already-merged frontend BossClaw V2 migration (#3501)
and route rename (#3528): the frontend runs engine-only, and
registration no longer drags V1 in.

## Tests

- New: V2-eligible registration skips warm-pool claim and V1 app
creation (zero-call assertions, `openclaw_app=None`, billing intact)
- New: V2-eligible registration succeeds when FastClaw app creation
fails (simulates the staging outage)
- Existing 13 register tests, route tests, and eligibility tests all
pass; `verify-py.sh` (ruff + format + pyright + import-linter) clean

Design spec:
`docs/superpowers/specs/2026-08-26-v2-registration-drop-v1-app-dependency.md`

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

## Problem

Staging `POST /account/personal-org` fails for new users with 503 `account.openclaw_app_initialization_failed`. Root-cause chain:

```
node-pool scale-down (infra-pool -> 0) -> V1 FastClaw has no instances
-> Envoy overload 503 -> register() unconditionally calls V1 create_app in its fallback -> registration 503
```

Even with `AGENTS_V2_ENABLED=true`, `register()` has no V2 branch: warm-pool claims require V1-provisioned `openclaw_app` assets, and the fallback always creates a V1 app.

## Fix

`register()` now judges V2 eligibility with the same `get_agents_v2_eligibility` gate engine agent install uses (`engine_main_agent_service`):

- **V2-eligible**: skip `claim_warm_pool_account` and `create_openclaw_app_record` entirely; `openclaw_app` stays `None`. Billing init + upsert unchanged — the proven fallback path minus the V1 app. A FastClaw outage (or an empty/disabled warm pool) no longer blocks registration.
- **Non-eligible**: legacy warm-pool → V1-app flow untouched (safe for future production partial rollout).

Downstream is already decoupled: org creation only needs the billing `team_id`, billing keys come from `ensure_billing_initialized`, and default-main-agent provisioning only reads `(uid, org_id, token)` with the same eligibility gate as its first check. The register response schema never serialized `openclaw_app`, so there is no API-compat impact.

Complements the already-merged frontend BossClaw V2 migration (#3501) and route rename (#3528): the frontend runs engine-only, and registration no longer drags V1 in.

## Tests

- New: V2-eligible registration skips warm-pool claim and V1 app creation (zero-call assertions, `openclaw_app=None`, billing intact)
- New: V2-eligible registration succeeds when FastClaw app creation fails (simulates the staging outage)
- Existing 13 register tests, route tests, and eligibility tests all pass; `verify-py.sh` (ruff + format + pyright + import-linter) clean

Design spec: `docs/superpowers/specs/2026-08-26-v2-registration-drop-v1-app-dependency.md`


---

## fix(models): preserve models without regional overrides (#3531)

- **SHA**: `b8ff412af9d6913c4dda511221714f27f695ab8e`
- **作者**: sam-srp
- **日期**: 2026-08-26T11:23:06Z
- **PR**: #3531

### Commit Message

```
fix(models): preserve models without regional overrides (#3531)

## Summary
- resolve model display overrides from any active team organization
region_code instead of hardcoding CN
- apply regional aliases only to configured models while preserving
entitled unmapped models with their original LiteLLM metadata
- stop treating regional display configuration as an Agent Builder
allowlist
- fall back to original model metadata when regional override
configuration is unavailable

## Testing
- ruff check and format checks
- targeted Pyright: 0 errors
- 61 related claw-interface unit tests passed
```

### PR Body

## Summary
- resolve model display overrides from any active team organization region_code instead of hardcoding CN
- apply regional aliases only to configured models while preserving entitled unmapped models with their original LiteLLM metadata
- stop treating regional display configuration as an Agent Builder allowlist
- fall back to original model metadata when regional override configuration is unavailable

## Testing
- ruff check and format checks
- targeted Pyright: 0 errors
- 61 related claw-interface unit tests passed

---

## fix(web): preserve app on transient account refresh errors (#3527)

- **SHA**: `2b17d0f8ec7522cfea9e2176c6c21c18acd8bd90`
- **作者**: sharplee-srp
- **日期**: 2026-08-26T09:25:29Z
- **PR**: #3527

### Commit Message

```
fix(web): preserve app on transient account refresh errors (#3527)

## Summary
- Keep the current app mounted when `/account/me` has a transient
non-auth failure and a local or cached session is already usable.
- Preserve the existing Retry gate when no usable session exists or
account bootstrap remains incomplete.
- Cover both the pending transport-retry window and the exhausted
account-bootstrap path with focused regression tests.

## Root cause
`AccountSessionGate` replaced the entire app with a session-verification
error for every non-401/403 `/account/me` failure. During React Query's
automatic transport retries, the final `error` is still empty and the
active `TypeError` is exposed through `failureReason`; the gate
therefore fell through to `return null`, producing a blank screen for an
already signed-in user.

The fix only changes those non-auth paths: a pending `TypeError` retry
or another terminal non-auth failure may continue rendering when a local
or cached session is already usable, while anonymous/first-load
failures, 401/403 responses, and exhausted `account.not_found` bootstrap
retries retain the current gate behavior.

## Test plan
- [x] `pnpm exec vitest run
tests/unit/components/AccountSessionGate.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh
web/app/src/components/AccountSessionGate.tsx
web/app/tests/unit/components/AccountSessionGate.unit.spec.tsx`
- [x] `bash scripts/verify-changed.sh`
```

### PR Body

## Summary
- Keep the current app mounted when `/account/me` has a transient non-auth failure and a local or cached session is already usable.
- Preserve the existing Retry gate when no usable session exists or account bootstrap remains incomplete.
- Cover both the pending transport-retry window and the exhausted account-bootstrap path with focused regression tests.

## Root cause
`AccountSessionGate` replaced the entire app with a session-verification error for every non-401/403 `/account/me` failure. During React Query's automatic transport retries, the final `error` is still empty and the active `TypeError` is exposed through `failureReason`; the gate therefore fell through to `return null`, producing a blank screen for an already signed-in user.

The fix only changes those non-auth paths: a pending `TypeError` retry or another terminal non-auth failure may continue rendering when a local or cached session is already usable, while anonymous/first-load failures, 401/403 responses, and exhausted `account.not_found` bootstrap retries retain the current gate behavior.

## Test plan
- [x] `pnpm exec vitest run tests/unit/components/AccountSessionGate.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh web/app/src/components/AccountSessionGate.tsx web/app/tests/unit/components/AccountSessionGate.unit.spec.tsx`
- [x] `bash scripts/verify-changed.sh`


---

## feat: add phase-one mainland web compliance (#3508)

- **SHA**: `ca35c19935e6bf3facc4f77cf7d1ae328cdfd25a`
- **作者**: sam-srp
- **日期**: 2026-08-26T08:38:24Z
- **PR**: #3508

### Commit Message

```
feat: add phase-one mainland web compliance (#3508)

## Summary

- restrict mainland China Web email OTP entry for personal accounts
while allowing users with an active Team organization
- add the organization region field and keep access eligibility
independent from model presentation
- apply CN-only model display overrides from the Flow Jobs managed
collection, hiding unconfigured models only for CN Team users
- preserve LiteLLM names and the full entitled model catalog outside CN
- prevent hidden regional models from reappearing or being saved through
the composer or Agent Builder
- add end-to-end regional compliance observability without logging
email, raw IP, full UID, or model/configuration content

## Meeting-aligned behavior

- mainland IP plus active Team organization: allow email OTP regardless
of organization region
- mainland IP plus personal or missing active Team organization: block
before sending OTP
- model white-labeling: controlled only by Team organization
`region_code` equal to `CN`
- no separate contracted-enterprise field and no coupling between
contract state and region display

## Regional compliance logging

- log normalized `CF-IPCountry`; missing values are `empty` and
malformed values are `invalid`
- log the final Web outcome: invalid request, personal blocked,
eligibility dependency error, OTP error, OTP sent, or Team allowed and
OTP sent
- log Organization `region_code` as configured; a missing legacy value
is `empty` with effective `CN`
- log invalid persisted Organization regions with masked UID and
Organization ID
- log model override configuration version, modification time,
declared/actual row counts, regional matches, invalid rows, duplicate
rows, missing active configuration, and invalid data shape
- log model catalog mode and entitled/override/visible counts, with a
warning for an empty catalog
- Flow Jobs executes outside this repository; this PR observes the
resulting Mongo sync document rather than duplicating its job logs

## Scope

Phase one is Web-only. It does not add iOS enforcement, session
enforcement for already logged-in users, domain migration, or HMAC
signing. It adds one server-only deployment secret,
`DOMESTIC_ACCESS_BFF_TOKEN`, shared by Web and claw-interface for the
pre-auth eligibility call.

## Deployment prerequisite

- configure `DOMESTIC_ACCESS_BFF_TOKEN` in the GitHub `staging` and
`production` Environment Secrets
- configure the matching per-environment value in the claw-interface
Vault path `srp/ecap/claw-interface/env`
- roll the claw-interface pods before deploying Web; the Web workflow
validates and injects the secret into the Cloudflare Worker

## Verification

- Claw Interface full suite: 9236 passed, 269 skipped
- deployment/authentication contract suite: 9 passed
- scoped Web verifier: 77 passed
- repository pre-commit and pre-push gates passed, including ESLint,
TypeScript, Ruff, Pyright, import contracts, dependency checks, and YAML
validation
- local end-to-end QA completed for CN and non-CN entry paths
```

### PR Body

## Summary

- restrict mainland China Web email OTP entry for personal accounts while allowing users with an active Team organization
- add the organization region field and keep access eligibility independent from model presentation
- apply CN-only model display overrides from the Flow Jobs managed collection, hiding unconfigured models only for CN Team users
- preserve LiteLLM names and the full entitled model catalog outside CN
- prevent hidden regional models from reappearing or being saved through the composer or Agent Builder
- add end-to-end regional compliance observability without logging email, raw IP, full UID, or model/configuration content

## Meeting-aligned behavior

- mainland IP plus active Team organization: allow email OTP regardless of organization region
- mainland IP plus personal or missing active Team organization: block before sending OTP
- model white-labeling: controlled only by Team organization `region_code` equal to `CN`
- no separate contracted-enterprise field and no coupling between contract state and region display

## Regional compliance logging

- log normalized `CF-IPCountry`; missing values are `empty` and malformed values are `invalid`
- log the final Web outcome: invalid request, personal blocked, eligibility dependency error, OTP error, OTP sent, or Team allowed and OTP sent
- log Organization `region_code` as configured; a missing legacy value is `empty` with effective `CN`
- log invalid persisted Organization regions with masked UID and Organization ID
- log model override configuration version, modification time, declared/actual row counts, regional matches, invalid rows, duplicate rows, missing active configuration, and invalid data shape
- log model catalog mode and entitled/override/visible counts, with a warning for an empty catalog
- Flow Jobs executes outside this repository; this PR observes the resulting Mongo sync document rather than duplicating its job logs

## Scope

Phase one is Web-only. It does not add iOS enforcement, session enforcement for already logged-in users, domain migration, or HMAC signing. It adds one server-only deployment secret, `DOMESTIC_ACCESS_BFF_TOKEN`, shared by Web and claw-interface for the pre-auth eligibility call.

## Deployment prerequisite

- configure `DOMESTIC_ACCESS_BFF_TOKEN` in the GitHub `staging` and `production` Environment Secrets
- configure the matching per-environment value in the claw-interface Vault path `srp/ecap/claw-interface/env`
- roll the claw-interface pods before deploying Web; the Web workflow validates and injects the secret into the Cloudflare Worker

## Verification

- Claw Interface full suite: 9236 passed, 269 skipped
- deployment/authentication contract suite: 9 passed
- scoped Web verifier: 77 passed
- repository pre-commit and pre-push gates passed, including ESLint, TypeScript, Ruff, Pyright, import contracts, dependency checks, and YAML validation
- local end-to-end QA completed for CN and non-CN entry paths


---

## fix(invitation): rename BossClaw route (#3528)

- **SHA**: `9847266732c86719dc3ee8559f045266b67e68a0`
- **作者**: tim-srp
- **日期**: 2026-08-26T08:21:30Z
- **PR**: #3528

### Commit Message

```
fix(invitation): rename BossClaw route (#3528)

## Summary

- Rename the localized BossClaw App Router segment from `bossclaw` to
`invitation`.
- Update login and `return_to` URLs so the invitation flow remains
within `/[locale]/invitation`.
- Update route-dependent unit tests while retaining the current BossClaw
login flow coverage.

## Validation

- `pnpm --dir web/app exec vitest run tests/unit/bossclaw` (96 passed)
- `bash scripts/verify-changed.sh` (no locally verifiable surface
detected for the pure route rename)

## Notes

- Static assets remain under `/bossclaw/*`; only the public page route
changed.
- Existing `/[locale]/bossclaw/login` URLs are not redirected by this
PR.
```

### PR Body

## Summary

- Rename the localized BossClaw App Router segment from `bossclaw` to `invitation`.
- Update login and `return_to` URLs so the invitation flow remains within `/[locale]/invitation`.
- Update route-dependent unit tests while retaining the current BossClaw login flow coverage.

## Validation

- `pnpm --dir web/app exec vitest run tests/unit/bossclaw` (96 passed)
- `bash scripts/verify-changed.sh` (no locally verifiable surface detected for the pure route rename)

## Notes

- Static assets remain under `/bossclaw/*`; only the public page route changed.
- Existing `/[locale]/bossclaw/login` URLs are not redirected by this PR.


---

## fix(agent-builder): recover ready test archives (#3529)

- **SHA**: `c441a41913625d472d3861e35e483230e790ba2e`
- **作者**: kaka-srp
- **日期**: 2026-08-26T08:11:25Z
- **PR**: #3529

### Commit Message

```
fix(agent-builder): recover ready test archives (#3529)

## Summary
- recover archive-bearing iterations already in `ready_to_test`,
`testing`, `reviewing_test`, or `accepted`
- recover a stale `deploying_test` iteration only when its same-owner,
same-Project TestRun has reached a stable authoritative status
- record the resolved ready/testing/accepted iteration phase in recovery
audit fields and keep the frontend contract synchronized

## Root cause
The recovery fallback only queried `accepted` and `reviewing_test`
iterations. A Pack Test can already be `ready_for_preview` while the
Project and iteration projection still says `deploying_test`; even after
reconciliation it maps to `ready_to_test`, which was also excluded. The
archive key, SHA-256, and R2 object could therefore exist while the
recovery candidate query returned zero rows.

## Safety
- active TestRuns such as `bot_allocating` remain ineligible
- a stale iteration is accepted only when the TestRun belongs to the
same org, owner, Project, and iteration
- existing newest-to-oldest archive validation, SHA-256 verification,
bounded extraction, and submitted-asset fallback remain unchanged

## Test plan
- [x] `pytest tests/unit/test_agent_builder_recovery_source_service.py
tests/unit/test_agent_builder_project_repo.py -q` — 32 passed
- [x] changed-file Ruff and Pyright — 0 errors
- [x] Python pre-commit hooks, file/complexity guards, import contracts,
and Pyright passed
- [x] frontend ESLint passed for `src/models/agent-builder.ts`
- [ ] local full `verify-changed.sh` is blocked by four pre-existing
Pyright errors in `_route_helpers.py`, `test_org_skills_routes.py`, and
`test_skills_manager_routes.py`; none of those files differ in this PR
- [ ] local full web verification used stale shared dependencies in the
no-node worktree: unrelated TypeScript package-contract errors appeared
and 33 Vitest workers timed out; clean-install CI remains authoritative
```

### PR Body

## Summary
- recover archive-bearing iterations already in `ready_to_test`, `testing`, `reviewing_test`, or `accepted`
- recover a stale `deploying_test` iteration only when its same-owner, same-Project TestRun has reached a stable authoritative status
- record the resolved ready/testing/accepted iteration phase in recovery audit fields and keep the frontend contract synchronized

## Root cause
The recovery fallback only queried `accepted` and `reviewing_test` iterations. A Pack Test can already be `ready_for_preview` while the Project and iteration projection still says `deploying_test`; even after reconciliation it maps to `ready_to_test`, which was also excluded. The archive key, SHA-256, and R2 object could therefore exist while the recovery candidate query returned zero rows.

## Safety
- active TestRuns such as `bot_allocating` remain ineligible
- a stale iteration is accepted only when the TestRun belongs to the same org, owner, Project, and iteration
- existing newest-to-oldest archive validation, SHA-256 verification, bounded extraction, and submitted-asset fallback remain unchanged

## Test plan
- [x] `pytest tests/unit/test_agent_builder_recovery_source_service.py tests/unit/test_agent_builder_project_repo.py -q` — 32 passed
- [x] changed-file Ruff and Pyright — 0 errors
- [x] Python pre-commit hooks, file/complexity guards, import contracts, and Pyright passed
- [x] frontend ESLint passed for `src/models/agent-builder.ts`
- [ ] local full `verify-changed.sh` is blocked by four pre-existing Pyright errors in `_route_helpers.py`, `test_org_skills_routes.py`, and `test_skills_manager_routes.py`; none of those files differ in this PR
- [ ] local full web verification used stale shared dependencies in the no-node worktree: unrelated TypeScript package-contract errors appeared and 33 Vitest workers timed out; clean-install CI remains authoritative


---

## feat(agents): make v2 the default runtime (#3525)

- **SHA**: `dec93c8767a18760a4015d98ea12f250d7aa3d2c`
- **作者**: kaka-srp
- **日期**: 2026-08-26T06:44:05Z
- **PR**: #3525

### Commit Message

```
feat(agents): make v2 the default runtime (#3525)

## Summary

- make Agent V2 the default runtime for every account while the global
V2 switch is enabled
- keep a temporary Vault-backed UID exception list for the explicitly
deferred V1 accounts
- remove obsolete email-allowlist deployment wiring
- verify exception values remain outside Git and are injected through
the Vault-managed secret

## Validation

- `bash scripts/verify-py.sh` with the Python 3.12 backend toolchain
(Ruff, Pyright, import contracts)
- 74 relevant unit tests covering V2 access, deployment wiring, routes,
main-agent behavior, and builder runtime services
- post-rebase access and Vault-wiring suite: 14 passed
- production Vault sync checked read-only: exception key present with
the expected five-entry set; values were not exposed or committed
```

### PR Body

## Summary

- make Agent V2 the default runtime for every account while the global V2 switch is enabled
- keep a temporary Vault-backed UID exception list for the explicitly deferred V1 accounts
- remove obsolete email-allowlist deployment wiring
- verify exception values remain outside Git and are injected through the Vault-managed secret

## Validation

- `bash scripts/verify-py.sh` with the Python 3.12 backend toolchain (Ruff, Pyright, import contracts)
- 74 relevant unit tests covering V2 access, deployment wiring, routes, main-agent behavior, and builder runtime services
- post-rebase access and Vault-wiring suite: 14 passed
- production Vault sync checked read-only: exception key present with the expected five-entry set; values were not exposed or committed



---

## fix(agent-builder): recover reviewing test archives (#3520)

- **SHA**: `0823428d09979db01d8df8ab0dc941378a51dc8f`
- **作者**: kaka-srp
- **日期**: 2026-08-26T06:12:13Z
- **PR**: #3520

### Commit Message

```
fix(agent-builder): recover reviewing test archives (#3520)

## Summary
- allow Agent Builder v1 recovery to use archived `reviewing_test`
iterations as well as `accepted` iterations
- validate recoverable iteration archives newest-to-oldest before
falling back to the submitted Pack asset
- persist the exact `reviewing_test_iteration` recovery audit source and
keep the frontend contract in sync
- document the recovery-source contract and add repository/service
regression coverage

## Root cause
When live v1 workspace export was unavailable, the fallback queried only
iterations whose status was `accepted`. Projects with a successfully
packaged and user-tested iteration in `reviewing_test`, but no accepted
iteration or published asset, therefore failed with
`agent_builder.recovery_source_missing` even though a readable archive
and SHA-256 were present.

## Test plan
- [x] `pytest tests/unit/test_agent_builder_recovery_source_service.py
tests/unit/test_agent_builder_project_repo.py
tests/unit/test_agent_builder_recovery_service.py
tests/unit/test_agent_builder_routes.py -q` — 80 passed
- [x] changed-file Pyright — 0 errors
- [x] frontend governance guards, full TypeScript check, and ESLint
passed after rebasing onto current `origin/main`
- [x] Ruff and import-linter passed
- [x] pre-commit hooks passed
- [ ] Full `verify-changed.sh` is blocked by four pre-existing Pyright
errors on `origin/main` in `tests/unit/_route_helpers.py`,
`tests/unit/test_org_skills_routes.py`, and
`tests/unit/test_skills_manager_routes.py`; none of those files differ
in this PR
```

### PR Body

## Summary
- allow Agent Builder v1 recovery to use archived `reviewing_test` iterations as well as `accepted` iterations
- validate recoverable iteration archives newest-to-oldest before falling back to the submitted Pack asset
- persist the exact `reviewing_test_iteration` recovery audit source and keep the frontend contract in sync
- document the recovery-source contract and add repository/service regression coverage

## Root cause
When live v1 workspace export was unavailable, the fallback queried only iterations whose status was `accepted`. Projects with a successfully packaged and user-tested iteration in `reviewing_test`, but no accepted iteration or published asset, therefore failed with `agent_builder.recovery_source_missing` even though a readable archive and SHA-256 were present.

## Test plan
- [x] `pytest tests/unit/test_agent_builder_recovery_source_service.py tests/unit/test_agent_builder_project_repo.py tests/unit/test_agent_builder_recovery_service.py tests/unit/test_agent_builder_routes.py -q` — 80 passed
- [x] changed-file Pyright — 0 errors
- [x] frontend governance guards, full TypeScript check, and ESLint passed after rebasing onto current `origin/main`
- [x] Ruff and import-linter passed
- [x] pre-commit hooks passed
- [ ] Full `verify-changed.sh` is blocked by four pre-existing Pyright errors on `origin/main` in `tests/unit/_route_helpers.py`, `tests/unit/test_org_skills_routes.py`, and `tests/unit/test_skills_manager_routes.py`; none of those files differ in this PR


---

## fix(billing): exclude historical orders from checkout alerts (#3523)

- **SHA**: `35533904395128fcc1c6c4ba8ef7dff41e41514b`
- **作者**: sharplee-srp
- **日期**: 2026-08-26T06:06:26Z
- **PR**: #3523

### Commit Message

```
fix(billing): exclude historical orders from checkout alerts (#3523)

## Summary
- scope the subscription manual-review PagerDuty queue to
provider-started checkouts that do not already have an entitlement
- update the alert remediation text and cron runbook with the exact
queue predicate
- lock the checkout-only predicate in the Billing v2 repository test

## Root cause
The provider-neutral manual-review monitor introduced in #3494 dropped
the existing `provider_checkout_requested_at` predicate. As a result,
historical renewal and backfill payment orders with
`status=manual_review` were counted as unresolved checkouts, including
orders that already had an entitlement.

A read-only production check confirmed that the sole alerting row had no
checkout-request marker and already had an entitlement; the corrected
predicate returns zero rows.

## Test plan
- [x] `.venv/bin/python -m pytest tests/unit/test_billing_v2_repos.py
tests/unit/test_orphaned_entitlements_cron.py -q` — 109 passed
- [x] `bash scripts/verify-py.sh` — ruff check/format, pyright, and
import-linter passed
- [x] pre-push changed-surface verification passed
```

### PR Body

## Summary
- scope the subscription manual-review PagerDuty queue to provider-started checkouts that do not already have an entitlement
- update the alert remediation text and cron runbook with the exact queue predicate
- lock the checkout-only predicate in the Billing v2 repository test

## Root cause
The provider-neutral manual-review monitor introduced in #3494 dropped the existing `provider_checkout_requested_at` predicate. As a result, historical renewal and backfill payment orders with `status=manual_review` were counted as unresolved checkouts, including orders that already had an entitlement.

A read-only production check confirmed that the sole alerting row had no checkout-request marker and already had an entitlement; the corrected predicate returns zero rows.

## Test plan
- [x] `.venv/bin/python -m pytest tests/unit/test_billing_v2_repos.py tests/unit/test_orphaned_entitlements_cron.py -q` — 109 passed
- [x] `bash scripts/verify-py.sh` — ruff check/format, pyright, and import-linter passed
- [x] pre-push changed-surface verification passed


---

## fix(billing): normalize historical creem channels (#3521)

- **SHA**: `8650ee79a15ffdfde7b3cb903d21ebe74bcabdb7`
- **作者**: tim-srp
- **日期**: 2026-08-26T05:34:33Z
- **PR**: #3521

### Commit Message

```
fix(billing): normalize historical creem channels (#3521)

## Summary
- Normalize historical account `payment_channel=creem` values to public
`card` responses, preventing `/account/me` validation failures.
- Preserve the original provider in historical subscription agreements;
no production data migration is required.

## Root cause

Creem was removed from the public response literal while active
historical subscription agreements can still project `provider=creem`
into the account response. Pydantic therefore rejected affected
`/account/me` responses with HTTP 500.

## Test plan

- [x] `services/claw-interface/.venv/bin/pytest
services/claw-interface/tests/unit/test_billing_v2_user_public_response.py
-q`
- [x] `bash scripts/verify-py.sh`
```

### PR Body

## Summary
- Normalize historical account `payment_channel=creem` values to public `card` responses, preventing `/account/me` validation failures.
- Preserve the original provider in historical subscription agreements; no production data migration is required.

## Root cause

Creem was removed from the public response literal while active historical subscription agreements can still project `provider=creem` into the account response. Pydantic therefore rejected affected `/account/me` responses with HTTP 500.

## Test plan

- [x] `services/claw-interface/.venv/bin/pytest services/claw-interface/tests/unit/test_billing_v2_user_public_response.py -q`
- [x] `bash scripts/verify-py.sh`


---

## fix(landing): link business entry to enterprise login (#3519)

- **SHA**: `af55006818ddbfccfa58b599d1ae1b4485fc7859`
- **作者**: tim-srp
- **日期**: 2026-08-26T03:39:46Z
- **PR**: #3519

### Commit Message

```
fix(landing): link business entry to enterprise login (#3519)

## Summary

- Point the landing-page Business navigation link to the ZooWork
Enterprise Admin login page.
- Align the ZooWork footer link with the same enterprise login
destination.

## Validation

- `git diff --check`
- `bash scripts/verify-web.sh web/app/src/lib/landing-content.ts`
(governance checks passed; TypeScript, Vitest, and ESLint unavailable
because this worktree has no frontend tool binaries)
```

### PR Body

## Summary

- Point the landing-page Business navigation link to the ZooWork Enterprise Admin login page.
- Align the ZooWork footer link with the same enterprise login destination.

## Validation

- `git diff --check`
- `bash scripts/verify-web.sh web/app/src/lib/landing-content.ts` (governance checks passed; TypeScript, Vitest, and ESLint unavailable because this worktree has no frontend tool binaries)


---

## chore(config): remove deprecated dupe gateway setting (#3518)

- **SHA**: `7f23fd55850f4b65a4555d0d54be909e29397e47`
- **作者**: tim-srp
- **日期**: 2026-08-26T03:34:21Z
- **PR**: #3518

### Commit Message

```
chore(config): remove deprecated dupe gateway setting (#3518)

## Summary

- remove the deprecated `DUPE_GATEWAY_URL` backend settings field
- remove its stale entry from `.env.example`

## Validation

- `bash scripts/verify-py.sh`
- pre-push changed-surface verification

## Notes

- This repository change removes the application-supported configuration
entry. Removing the obsolete value from external Vault/environment
stores is a separate operational step.
- `E2B_API_KEY`, `STRIPE_PRODUCT_ID_MONTHLY`, and
`VERTICAL_PACK_PLAN_ID_RESTAURANT_AI_TEAM_MONTHLY` are intentionally out
of scope because they still have active consumers.
```

### PR Body

## Summary

- remove the deprecated `DUPE_GATEWAY_URL` backend settings field
- remove its stale entry from `.env.example`

## Validation

- `bash scripts/verify-py.sh`
- pre-push changed-surface verification

## Notes

- This repository change removes the application-supported configuration entry. Removing the obsolete value from external Vault/environment stores is a separate operational step.
- `E2B_API_KEY`, `STRIPE_PRODUCT_ID_MONTHLY`, and `VERTICAL_PACK_PLAN_ID_RESTAURANT_AI_TEAM_MONTHLY` are intentionally out of scope because they still have active consumers.


---
