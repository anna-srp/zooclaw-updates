# SerendipityOneInc/ecap-workspace commits - 2026-08-26

## fix(billing): tolerate Airwallex period correction on scheduled cancellation (#3538)
- sha: `c699341914c4dddc02233de390644c92b1dcd08e`
- 作者: tim-srp <tim@srp.one>
- 日期: 2026-08-26T14:45:28Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/c699341914c4dddc02233de390644c92b1dcd08e
- 改动文件: services/claw-interface/app/services/airwallex/subscription_changes.py, services/claw-interface/app/services/billing_v2/subscription_agreement_upsert.py, services/claw-interface/tests/unit/test_airwallex_subscription_changes.py, services/claw-interface/tests/unit/test_billing_v2_subscription_agreements.py

### 完整 commit message

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

### PR #3538: fix(billing): tolerate Airwallex period correction on scheduled cancellation

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
- sha: `dbdc4ab5ca4ba9e787404e4dc8ffbcfaf1d8080d`
- 作者: tim-srp <tim@srp.one>
- 日期: 2026-08-26T14:14:09Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/dbdc4ab5ca4ba9e787404e4dc8ffbcfaf1d8080d
- 改动文件: web/app/src/app/[locale]/bossclaw/BossclawClient.tsx, web/app/src/app/[locale]/bossclaw/agent-install.ts, web/app/src/app/[locale]/bossclaw/bossclaw.module.css, web/app/src/app/[locale]/bossclaw/components/CapabilitiesStep.tsx, web/app/src/app/[locale]/bossclaw/components/DoneStep.tsx, web/app/src/app/[locale]/bossclaw/components/IntroHeroStep.tsx, web/app/src/app/[locale]/bossclaw/components/LoginStep.tsx, web/app/src/app/[locale]/bossclaw/components/PhoneLoginStep.tsx, web/app/src/app/[locale]/bossclaw/components/Preloader.tsx, web/app/src/app/[locale]/bossclaw/components/RedeemStep.tsx, web/app/src/app/[locale]/bossclaw/components/WechatBindStep.tsx, web/app/src/app/[locale]/bossclaw/legacy-redirect.ts, web/app/src/app/[locale]/bossclaw/login/page.tsx, web/app/src/app/[locale]/bossclaw/page.tsx, web/app/src/app/[locale]/bossclaw/wizard-state.ts, web/app/src/app/[locale]/invitation/login/BossclawLoginClient.tsx, web/app/src/app/[locale]/invitation/login/useBossclawLoginFlow.ts, web/app/src/app/[locale]/invitation/page.tsx, web/app/tests/unit/bossclaw/agent-install.unit.spec.ts, web/app/tests/unit/bossclaw/bossclaw-client-intro.unit.spec.tsx, web/app/tests/unit/bossclaw/bossclaw-client.unit.spec.tsx, web/app/tests/unit/bossclaw/bossclaw-layout-css.unit.spec.ts, web/app/tests/unit/bossclaw/bossclaw-login-flow.unit.spec.ts, web/app/tests/unit/bossclaw/done-step.unit.spec.tsx, web/app/tests/unit/bossclaw/legacy-redirects.unit.spec.ts, web/app/tests/unit/bossclaw/login-client.unit.spec.tsx, web/app/tests/unit/bossclaw/login-step.unit.spec.tsx, web/app/tests/unit/bossclaw/page.unit.spec.tsx, web/app/tests/unit/bossclaw/phone-login-step.unit.spec.tsx, web/app/tests/unit/bossclaw/redeem-step.unit.spec.tsx, web/app/tests/unit/bossclaw/wechat-bind-step.unit.spec.tsx, web/app/tests/unit/bossclaw/wizard-steps.unit.spec.ts

### 完整 commit message

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

### PR #3536: fix(invitation): restore BossClaw registration route

## Summary

- Restore the campaign and registration page at `/[locale]/bossclaw`.
- Keep the login page at `/[locale]/invitation/login`.
- Remove `/[locale]/bossclaw/login` and the `/[locale]/invitation` page so only the requested URLs are exposed.
- Update return-to validation and route-dependent tests for this split URL structure.

## Validation

- `pnpm --dir web/app exec vitest run tests/unit/bossclaw` (96 passed)


---

## fix(r2): update allowed origin to zoowork.ai (#3535)
- sha: `8940bf7d236ca1d64b59e96264753347ea8b68cd`
- 作者: tim-srp <tim@srp.one>
- 日期: 2026-08-26T13:55:23Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/8940bf7d236ca1d64b59e96264753347ea8b68cd
- 改动文件: services/r2-access-worker/src/__tests__/copy.test.ts, services/r2-access-worker/src/__tests__/index.test.ts, services/r2-access-worker/src/__tests__/upload-service-token.test.ts, services/r2-access-worker/wrangler.toml

### 完整 commit message

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

### PR #3535: fix(r2): update allowed origin to zoowork.ai

## Summary

- Update the production R2 access worker CORS origin from `https://zooclaw.ai` to `https://zoowork.ai`.
- Update the worker tests to cover the migrated origin.

## Validation

- `git diff --check`
- Vitest and TypeScript checks could not run because this worktree has no installed `node_modules`.


---

## fix(web): hide unsupported session delete action (#3534)
- sha: `fdcd34db3ff42415400000f173021415039f3c04`
- 作者: sharplee-srp <sharplee@srp.one>
- 日期: 2026-08-26T13:42:03Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/fdcd34db3ff42415400000f173021415039f3c04
- 改动文件: web/app/src/components/sidenav/SideNavSessionRow.tsx, web/app/tests/unit/components/sidenav/SideNavSessionRow.unit.spec.tsx

### 完整 commit message

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

### PR #3534: fix(web): hide unsupported session delete action

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
- sha: `2f5ff75cc502e7eb31507d7569de82ed872b5047`
- 作者: finn-srp <finn@srp.one>
- 日期: 2026-08-26T13:36:07Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/2f5ff75cc502e7eb31507d7569de82ed872b5047
- 改动文件: web/app/src/app/[locale]/(app)/claw-settings/components/ApiKeysGuidance.tsx, web/app/src/app/[locale]/(app)/claw-settings/components/ApiKeysTab.tsx, web/app/src/app/[locale]/(app)/claw-settings/components/useApiKeysController.ts, web/app/src/locales/en.ts, web/app/src/locales/zh.ts, web/app/tests/unit/app/claw-settings/ApiKeysTab.unit.spec.tsx

### 完整 commit message

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

### PR #3533: feat(settings): tell users what to do with an API key

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
- sha: `466df714fcb9757f996ff55f07a39e57e87f957c`
- 作者: tim-srp <tim@srp.one>
- 日期: 2026-08-26T11:27:29Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/466df714fcb9757f996ff55f07a39e57e87f957c
- 改动文件: docs/plans/2026-08-21-bossclaw-v2-migration-summary.md, docs/superpowers/specs/2026-08-26-v2-registration-drop-v1-app-dependency.md, services/claw-interface/app/services/user/account_service.py, services/claw-interface/tests/unit/test_account_service.py

### 完整 commit message

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

### PR #3532: fix(registration): skip warm pool and V1 app creation for V2-eligible users

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
- sha: `b8ff412af9d6913c4dda511221714f27f695ab8e`
- 作者: sam-srp <sam@srp.one>
- 日期: 2026-08-26T11:23:06Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/b8ff412af9d6913c4dda511221714f27f695ab8e
- 改动文件: services/claw-interface/app/services/agent_builder_engine_model_service.py, services/claw-interface/app/services/agent_builder_model_service.py, services/claw-interface/app/services/agent_builder_model_visibility.py, services/claw-interface/app/services/model_catalog.py, services/claw-interface/app/services/regional_model_display.py, services/claw-interface/tests/unit/test_agent_builder_model_service.py, services/claw-interface/tests/unit/test_model_catalog.py, services/claw-interface/tests/unit/test_regional_model_display.py

### 完整 commit message

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

### PR #3531: fix(models): preserve models without regional overrides

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
- sha: `2b17d0f8ec7522cfea9e2176c6c21c18acd8bd90`
- 作者: sharplee-srp <sharplee@srp.one>
- 日期: 2026-08-26T09:25:29Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/2b17d0f8ec7522cfea9e2176c6c21c18acd8bd90
- 改动文件: web/app/src/components/AccountSessionGate.tsx, web/app/tests/unit/components/AccountSessionGate.unit.spec.tsx

### 完整 commit message

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

### PR #3527: fix(web): preserve app on transient account refresh errors

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
- sha: `ca35c19935e6bf3facc4f77cf7d1ae328cdfd25a`
- 作者: sam-srp <sam@srp.one>
- 日期: 2026-08-26T08:38:24Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/ca35c19935e6bf3facc4f77cf7d1ae328cdfd25a
- 改动文件: .env.example, .github/workflows/deploy.yml, docs/superpowers/specs/2026-08-25-web-cn-compliance-phase1.md, services/claw-interface/app/auth/domestic_access.py, services/claw-interface/app/create_app.py, services/claw-interface/app/database/account_org_repo.py, services/claw-interface/app/database/model_display_override_repo.py, services/claw-interface/app/database/org_repo.py, services/claw-interface/app/database/user_repo.py, services/claw-interface/app/routes/domestic_access.py, services/claw-interface/app/routes/internal/orgs.py, services/claw-interface/app/routes/internal/users.py, services/claw-interface/app/schema/account_api.py, services/claw-interface/app/schema/domestic_access.py, services/claw-interface/app/schema/model_catalog.py, services/claw-interface/app/schema/model_display_override.py, services/claw-interface/app/schema/org.py, services/claw-interface/app/services/agent_builder_engine_model_service.py, services/claw-interface/app/services/agent_builder_model_service.py, services/claw-interface/app/services/agent_builder_model_visibility.py, services/claw-interface/app/services/domestic_access.py, services/claw-interface/app/services/model_catalog.py, services/claw-interface/app/services/org/region_service.py, services/claw-interface/app/services/regional_model_display.py, services/claw-interface/app/services/user/list_service.py, services/claw-interface/app/settings.py, services/claw-interface/pyproject.toml, services/claw-interface/tests/unit/test_agent_builder_model_service.py, services/claw-interface/tests/unit/test_domestic_access.py, services/claw-interface/tests/unit/test_domestic_access_deployment_wiring.py, services/claw-interface/tests/unit/test_domestic_access_routes.py, services/claw-interface/tests/unit/test_internal_users_routes.py, services/claw-interface/tests/unit/test_model_catalog.py, services/claw-interface/tests/unit/test_model_display_override_repo.py, services/claw-interface/tests/unit/test_org_region_service.py, services/claw-interface/tests/unit/test_org_repo.py, services/claw-interface/tests/unit/test_regional_model_display.py, services/claw-interface/tests/unit/test_routes_internal_orgs.py, services/claw-interface/tests/unit/test_schema_org.py, services/claw-interface/tests/unit/test_user_repo.py, web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderCreateDialog.tsx, web/app/src/app/[locale]/(marketing)/MarketingChrome.tsx, web/app/src/app/api/auth/email-otp/send/route.ts, web/app/src/components/DomesticAccessRestrictedDialog.tsx, web/app/src/components/LoginForm.tsx, web/app/src/components/chat/unified-chat-composer/UnifiedChatComposer.tsx, web/app/src/components/chat/unified-chat-composer/composer-model-presentations.ts, web/app/src/components/chat/unified-chat-composer/useComposerModelState.ts, web/app/src/hooks/queries/models/useChatModelCatalogQuery.ts, web/app/src/lib/auth/domestic-access-bff.ts, web/app/src/lib/auth/errors.ts, web/app/src/lib/logger.ts, web/app/src/locales/en.ts, web/app/src/locales/zh.ts, web/app/src/models/model-catalog.ts, web/app/tests/unit/app/api/auth-routes.unit.spec.ts, web/app/tests/unit/app/marketing-chrome.unit.spec.tsx, web/app/tests/unit/components/LoginForm.unit.spec.tsx, web/app/tests/unit/components/chat/unified-chat-composer/UnifiedChatComposer.unit.spec.tsx, web/app/tests/unit/components/chat/unified-chat-composer/composer-model-presentations.unit.spec.ts

### 完整 commit message

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

### PR #3508: feat: add phase-one mainland web compliance

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
- sha: `9847266732c86719dc3ee8559f045266b67e68a0`
- 作者: tim-srp <tim@srp.one>
- 日期: 2026-08-26T08:21:30Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/9847266732c86719dc3ee8559f045266b67e68a0
- 改动文件: web/app/src/app/[locale]/bossclaw/legacy-redirect.ts, web/app/src/app/[locale]/bossclaw/login/page.tsx, web/app/src/app/[locale]/bossclaw/page.tsx, web/app/src/app/[locale]/invitation/BossclawClient.tsx, web/app/src/app/[locale]/invitation/agent-install.ts, web/app/src/app/[locale]/invitation/bossclaw.module.css, web/app/src/app/[locale]/invitation/components/CapabilitiesStep.tsx, web/app/src/app/[locale]/invitation/components/DoneStep.tsx, web/app/src/app/[locale]/invitation/components/IntroHeroStep.tsx, web/app/src/app/[locale]/invitation/components/LoginStep.tsx, web/app/src/app/[locale]/invitation/components/PhoneLoginStep.tsx, web/app/src/app/[locale]/invitation/components/Preloader.tsx, web/app/src/app/[locale]/invitation/components/RedeemStep.tsx, web/app/src/app/[locale]/invitation/components/WechatBindStep.tsx, web/app/src/app/[locale]/invitation/login/BossclawLoginClient.tsx, web/app/src/app/[locale]/invitation/login/page.tsx, web/app/src/app/[locale]/invitation/login/useBossclawLoginFlow.ts, web/app/src/app/[locale]/invitation/page.tsx, web/app/src/app/[locale]/invitation/wizard-state.ts, web/app/tests/unit/bossclaw/agent-install.unit.spec.ts, web/app/tests/unit/bossclaw/bossclaw-client-intro.unit.spec.tsx, web/app/tests/unit/bossclaw/bossclaw-client.unit.spec.tsx, web/app/tests/unit/bossclaw/bossclaw-layout-css.unit.spec.ts, web/app/tests/unit/bossclaw/bossclaw-login-flow.unit.spec.ts, web/app/tests/unit/bossclaw/done-step.unit.spec.tsx, web/app/tests/unit/bossclaw/legacy-redirects.unit.spec.ts, web/app/tests/unit/bossclaw/login-client.unit.spec.tsx, web/app/tests/unit/bossclaw/login-step.unit.spec.tsx, web/app/tests/unit/bossclaw/page.unit.spec.tsx, web/app/tests/unit/bossclaw/phone-login-step.unit.spec.tsx, web/app/tests/unit/bossclaw/redeem-step.unit.spec.tsx, web/app/tests/unit/bossclaw/wechat-bind-step.unit.spec.tsx, web/app/tests/unit/bossclaw/wizard-steps.unit.spec.ts

### 完整 commit message

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

### PR #3528: fix(invitation): rename BossClaw route

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
- sha: `c441a41913625d472d3861e35e483230e790ba2e`
- 作者: kaka-srp <kaka@srp.one>
- 日期: 2026-08-26T08:11:25Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/c441a41913625d472d3861e35e483230e790ba2e
- 改动文件: docs/superpowers/specs/2026-08-11-agent-builder-v1-project-recovery-design.md, services/claw-interface/app/database/agent_builder_iteration_repo.py, services/claw-interface/app/schema/agent_builder.py, services/claw-interface/app/services/agent_builder_recovery_source_service.py, services/claw-interface/tests/unit/test_agent_builder_project_repo.py, services/claw-interface/tests/unit/test_agent_builder_recovery_source_service.py, web/app/src/models/agent-builder.ts

### 完整 commit message

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

### PR #3529: fix(agent-builder): recover ready test archives

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
- sha: `dec93c8767a18760a4015d98ea12f250d7aa3d2c`
- 作者: kaka-srp <kaka@srp.one>
- 日期: 2026-08-26T06:44:05Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/dec93c8767a18760a4015d98ea12f250d7aa3d2c
- 改动文件: .env.example, .github/workflows/deploy.yml, services/claw-interface/app/services/agents/agents_v2_access.py, services/claw-interface/app/settings.py, services/claw-interface/tests/unit/test_agents_v2_access.py, services/claw-interface/tests/unit/test_agents_v2_deployment_wiring.py, web/app/scripts/mock-backend.mjs, web/app/scripts/mock-backend/scenarios.mjs, web/app/tests/unit/scripts/mock-backend-agent-builder.unit.spec.ts, web/app/tests/unit/scripts/mock-backend-agent-schedules.unit.spec.ts, web/app/tests/unit/scripts/mock-backend-agents.unit.spec.ts

### 完整 commit message

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

### PR #3525: feat(agents): make v2 the default runtime

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
- sha: `0823428d09979db01d8df8ab0dc941378a51dc8f`
- 作者: kaka-srp <kaka@srp.one>
- 日期: 2026-08-26T06:12:13Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/0823428d09979db01d8df8ab0dc941378a51dc8f
- 改动文件: docs/superpowers/specs/2026-08-11-agent-builder-v1-project-recovery-design.md, services/claw-interface/app/database/agent_builder_iteration_repo.py, services/claw-interface/app/schema/agent_builder.py, services/claw-interface/app/services/agent_builder_recovery_source_service.py, services/claw-interface/tests/unit/test_agent_builder_project_repo.py, services/claw-interface/tests/unit/test_agent_builder_recovery_source_service.py, web/app/src/models/agent-builder.ts

### 完整 commit message

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

### PR #3520: fix(agent-builder): recover reviewing test archives

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
- sha: `35533904395128fcc1c6c4ba8ef7dff41e41514b`
- 作者: sharplee-srp <sharplee@srp.one>
- 日期: 2026-08-26T06:06:26Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/35533904395128fcc1c6c4ba8ef7dff41e41514b
- 改动文件: services/claw-interface/app/cron/orphaned_entitlements.py, services/claw-interface/app/database/card_checkout_order_repo.py, services/claw-interface/docs/cron-triggers.md, services/claw-interface/tests/unit/test_billing_v2_repos.py

### 完整 commit message

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

### PR #3523: fix(billing): exclude historical orders from checkout alerts

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
- sha: `8650ee79a15ffdfde7b3cb903d21ebe74bcabdb7`
- 作者: tim-srp <tim@srp.one>
- 日期: 2026-08-26T05:34:33Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/8650ee79a15ffdfde7b3cb903d21ebe74bcabdb7
- 改动文件: services/claw-interface/app/schema/account_api.py, services/claw-interface/tests/unit/test_billing_v2_user_public_response.py

### 完整 commit message

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

### PR #3521: fix(billing): normalize historical creem channels

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
- sha: `af55006818ddbfccfa58b599d1ae1b4485fc7859`
- 作者: tim-srp <tim@srp.one>
- 日期: 2026-08-26T03:39:46Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/af55006818ddbfccfa58b599d1ae1b4485fc7859
- 改动文件: web/app/src/lib/landing-content.ts

### 完整 commit message

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

### PR #3519: fix(landing): link business entry to enterprise login

## Summary

- Point the landing-page Business navigation link to the ZooWork Enterprise Admin login page.
- Align the ZooWork footer link with the same enterprise login destination.

## Validation

- `git diff --check`
- `bash scripts/verify-web.sh web/app/src/lib/landing-content.ts` (governance checks passed; TypeScript, Vitest, and ESLint unavailable because this worktree has no frontend tool binaries)


---

## chore(config): remove deprecated dupe gateway setting (#3518)
- sha: `7f23fd55850f4b65a4555d0d54be909e29397e47`
- 作者: tim-srp <tim@srp.one>
- 日期: 2026-08-26T03:34:21Z
- 链接: https://github.com/SerendipityOneInc/ecap-workspace/commit/7f23fd55850f4b65a4555d0d54be909e29397e47
- 改动文件: .env.example, services/claw-interface/app/settings.py

### 完整 commit message

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

### PR #3518: chore(config): remove deprecated dupe gateway setting

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
