# ecap-workspace commits — 2026-06-17

共 7 个 commit

---

## `3a47a6af1b`

- **作者**: tim-srp
- **日期**: 2026-06-17T14:09:25Z
- **PR**: #2509
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/3a47a6af1b9a5e916e58ed4186d3539fd43d6c5f

### 完整 commit message

```
fix(bossclaw): clarify wechat binding flow (#2509)

## Summary
- add a back button for BossClaw app steps so users can return to the
previous step
- update the WeChat bind copy to tell users to long-press the QR code
instead of saving a screenshot
- add a confirmation guide showing that `WeixinClawBot` appearing in
WeChat means binding succeeded

## Local validation
- `git diff --check` passed
- `curl http://localhost:3000/zh/bossclaw` returned 200
- `bash scripts/verify-web.sh
web/app/src/app/[locale]/bossclaw/BossclawClient.tsx
web/app/src/app/[locale]/bossclaw/components/WechatBindStep.tsx
web/app/src/app/[locale]/bossclaw/bossclaw.module.css` partially passed:
guards, vitest, and eslint passed; global `tsc` is blocked by existing
`src/app/[locale]/(app)/(chat)/chat/components/GenClawInput.tsx` missing
`ldrs/react` type resolution in this local checkout

---------

Co-authored-by: Developer <dev@srp.one>
```

### PR Description

## Summary
- add a back button for BossClaw app steps so users can return to the previous step
- update the WeChat bind copy to tell users to long-press the QR code instead of saving a screenshot
- add a confirmation guide showing that `WeixinClawBot` appearing in WeChat means binding succeeded

## Local validation
- `git diff --check` passed
- `curl http://localhost:3000/zh/bossclaw` returned 200
- `bash scripts/verify-web.sh web/app/src/app/[locale]/bossclaw/BossclawClient.tsx web/app/src/app/[locale]/bossclaw/components/WechatBindStep.tsx web/app/src/app/[locale]/bossclaw/bossclaw.module.css` partially passed: guards, vitest, and eslint passed; global `tsc` is blocked by existing `src/app/[locale]/(app)/(chat)/chat/components/GenClawInput.tsx` missing `ldrs/react` type resolution in this local checkout


---

## `83fa6a9b63`

- **作者**: Chris@ZooClaw
- **日期**: 2026-06-17T10:58:43Z
- **PR**: #2504
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/83fa6a9b6350a4be1c9aed41d6255e1fe5e9b2d4

### 完整 commit message

```
fix(arch-review): enum contract + value normalization + failure alert (#2504)

## Problem

The weekly **Architectural Code Review** workflow
(`claude-arch-review.yaml`, Mondays 09:00 UTC) looked like it "didn't
run" this week. It **did** fire on 2026-06-15 — but **failed**, as it
has every Monday since the 2026-05-28 cohort-issues migration. Last
green scheduled run: **2026-05-25** (3 weeks red).

2026-06-15: `web` ✅, `claw-interface` ❌, `ios` ❌ — both died at
**Validate finding schema**:
- `Effort='Small'/'Large'/'Low'/'Medium'/'High'` instead of `S`/`M`/`L`
- `Category='Architecture / Duplication'` (slash-compound) instead of
one value

**Root cause:** the migration tightened the validator to strict
`Priority`/`Impact`/`Effort`/`Category` enums but the legal *values*
were never written into any prompt the model loads at runtime —
`SKILL.md` names the fields but never enumerates the tokens, and
`.claude/commands/arch-review.md` is now a pure thin wrapper. The model
guesses and drifts. There was also **no failure alerting**, so 3 weeks
of red went unnoticed.

## Changes

1. **`SKILL.md` — enum contract + worked example** (root fix). The model
now sees the closed enum lists (`Effort: S|M|L`, single-value
`Category`, …) and a copy-pasteable finding block.
2. **`normalize.py` + `_parse.py` + a new "Normalize finding values"
workflow step** (defense-in-depth). Rewrites `findings.md` **in place**
(so the corrected value flows into the issue body — downstream steps
copy each block verbatim), canonicalizing only **known** synonyms
(`Small`/`Low`→`S`, `Large`/`High`→`L`, compound Category→first valid
value). Unknown / structurally-broken blocks pass through untouched and
still fail the gate loudly.
3. **`notify-failure` job** — mirrors the `sentry-memory-rollup.yml`
broadcast pattern; pings the ZooClaw dev group once on any failure
(`needs: review` + `always() && result == 'failure'`, works with
`fail-fast:false`).
4. **`test_normalize.py`** — unit + end-to-end coverage of the exact
slips that red'd the 2026-06-15 run, plus a guard that
structurally-broken blocks are NOT silently rescued.

## Verification

- `pytest .github/scripts/arch-review/tests/` — 86 passed (incl. new
normalize tests); `ruff check`/`format` clean; `sync-agent-skills.sh
--check` ok.
- Dispatched `claude-arch-review` on this branch (`dry_run=true`) for
`claw-interface`+`ios` → confirms the previously-red **Validate finding
schema** step now passes. (Run link in a comment.)
- Real (non-dry-run) dispatch to confirm proper GitHub issue
create/update.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## Problem

The weekly **Architectural Code Review** workflow (`claude-arch-review.yaml`, Mondays 09:00 UTC) looked like it "didn't run" this week. It **did** fire on 2026-06-15 — but **failed**, as it has every Monday since the 2026-05-28 cohort-issues migration. Last green scheduled run: **2026-05-25** (3 weeks red).

2026-06-15: `web` ✅, `claw-interface` ❌, `ios` ❌ — both died at **Validate finding schema**:
- `Effort='Small'/'Large'/'Low'/'Medium'/'High'` instead of `S`/`M`/`L`
- `Category='Architecture / Duplication'` (slash-compound) instead of one value

**Root cause:** the migration tightened the validator to strict `Priority`/`Impact`/`Effort`/`Category` enums but the legal *values* were never written into any prompt the model loads at runtime — `SKILL.md` names the fields but never enumerates the tokens, and `.claude/commands/arch-review.md` is now a pure thin wrapper. The model guesses and drifts. There was also **no failure alerting**, so 3 weeks of red went unnoticed.

## Changes

1. **`SKILL.md` — enum contract + worked example** (root fix). The model now sees the closed enum lists (`Effort: S|M|L`, single-value `Category`, …) and a copy-pasteable finding block.
2. **`normalize.py` + `_parse.py` + a new "Normalize finding values" workflow step** (defense-in-depth). Rewrites `findings.md` **in place** (so the corrected value flows into the issue body — downstream steps copy each block verbatim), canonicalizing only **known** synonyms (`Small`/`Low`→`S`, `Large`/`High`→`L`, compound Category→first valid value). Unknown / structurally-broken blocks pass through untouched and still fail the gate loudly.
3. **`notify-failure` job** — mirrors the `sentry-memory-rollup.yml` broadcast pattern; pings the ZooClaw dev group once on any failure (`needs: review` + `always() && result == 'failure'`, works with `fail-fast:false`).
4. **`test_normalize.py`** — unit + end-to-end coverage of the exact slips that red'd the 2026-06-15 run, plus a guard that structurally-broken blocks are NOT silently rescued.

## Verification

- `pytest .github/scripts/arch-review/tests/` — 86 passed (incl. new normalize tests); `ruff check`/`format` clean; `sync-agent-skills.sh --check` ok.
- Dispatched `claude-arch-review` on this branch (`dry_run=true`) for `claw-interface`+`ios` → confirms the previously-red **Validate finding schema** step now passes. (Run link in a comment.)
- Real (non-dry-run) dispatch to confirm proper GitHub issue create/update.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## `2387f00c2b`

- **作者**: lynn Zhuang
- **日期**: 2026-06-17T08:22:28Z
- **PR**: #2331
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/2387f00c2ba083ca93314040264b7089f1a6b49c

### 完整 commit message

```
fix(chat): 输入框上方展示agent 链接中状态 (#2331)

## Summary
- 在 chat 输入框上方新增 connection-warning slot，当 WebSocket 稳态为 `reconnecting |
disconnected | error` 时显示
"Reaching your Claw..." 提示（`ldrs` 的 JellyTriangle 8px loader +
caution-text 橙色 + 金黄色扫光动效）。
  - 该 slot 优先级高于已有的 typing indicator —— 一个掉线的 agent 不可能在"打字"，所以两者互斥。
  - 不覆盖 init / restart 阶段（那段由 `InitBanner` 头部条幅负责），避免重复信号。

  ## Implementation notes
- `ChatBody.tsx`：根据 `stableStatus` 派生 `connectionWarning` 对象，从 i18n
`genClaw.connecting` key
  取文案（fallback `"Reaching your Claw..."`），透传给 `GenClawInput`。
- `GenClawInput.tsx`：新增可选 prop `connectionWarning`；在 typing-indicator
同位置渲染，三元优先级
  `connectionWarning ? ... : typingLabel ? ... : null`。
- `globals.css`：新增 `.shimmer-claw`，用 `background-clip: text` +
`background-size: 200%` + `no-repeat` + 关键帧
`100% → 0%` 把金黄 (`#fcd34d` / dark 下 `#fffbeb`) 高光带在深橙文字上从左扫到右，1.8s
一个周期、无死时间。
  - 新增依赖 `ldrs@^1.1.9`（提供 JellyTriangle web component）。

  ## Test plan
- [ ] 断开后端 WS / 拔网线，输入框上方出现 "Reaching your Claw..." + 橙色三角形 loader +
金黄扫光
  - [ ] 网络恢复后提示自动消失
  - [ ] Agent 正在打字时不应同时显示该警告
  - [ ] init / restart 阶段仍由 `InitBanner` 占用顶部，不应重复出现该警告
  - [ ] Dark 模式下高光带改为暖白 (`#fffbeb`)，深底上仍清晰可见
  - [ ] JellyTriangle 8px 在 `text-xs`（12px）行高里垂直居中对齐


https://github.com/user-attachments/assets/80106084-ec15-40c8-b9fc-84c5ffb5ba37

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary
  - 在 chat 输入框上方新增 connection-warning slot，当 WebSocket 稳态为 `reconnecting | disconnected | error` 时显示
  "Reaching your Claw..." 提示（`ldrs` 的 JellyTriangle 8px loader + caution-text 橙色 + 金黄色扫光动效）。
  - 该 slot 优先级高于已有的 typing indicator —— 一个掉线的 agent 不可能在"打字"，所以两者互斥。
  - 不覆盖 init / restart 阶段（那段由 `InitBanner` 头部条幅负责），避免重复信号。

  ## Implementation notes
  - `ChatBody.tsx`：根据 `stableStatus` 派生 `connectionWarning` 对象，从 i18n `genClaw.connecting` key
  取文案（fallback `"Reaching your Claw..."`），透传给 `GenClawInput`。
  - `GenClawInput.tsx`：新增可选 prop `connectionWarning`；在 typing-indicator 同位置渲染，三元优先级
  `connectionWarning ? ... : typingLabel ? ... : null`。
  - `globals.css`：新增 `.shimmer-claw`，用 `background-clip: text` + `background-size: 200%` + `no-repeat` + 关键帧
  `100% → 0%` 把金黄 (`#fcd34d` / dark 下 `#fffbeb`) 高光带在深橙文字上从左扫到右，1.8s 一个周期、无死时间。
  - 新增依赖 `ldrs@^1.1.9`（提供 JellyTriangle web component）。

  ## Test plan
  - [ ] 断开后端 WS / 拔网线，输入框上方出现 "Reaching your Claw..." + 橙色三角形 loader + 金黄扫光
  - [ ] 网络恢复后提示自动消失
  - [ ] Agent 正在打字时不应同时显示该警告
  - [ ] init / restart 阶段仍由 `InitBanner` 占用顶部，不应重复出现该警告
  - [ ] Dark 模式下高光带改为暖白 (`#fffbeb`)，深底上仍清晰可见
  - [ ] JellyTriangle 8px 在 `text-xs`（12px）行高里垂直居中对齐

https://github.com/user-attachments/assets/80106084-ec15-40c8-b9fc-84c5ffb5ba37



---

## `4b84268db9`

- **作者**: kaka-srp
- **日期**: 2026-06-17T08:05:32Z
- **PR**: #2501
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/4b84268db93af0f1a469d096f7b02ed769bae02c

### 完整 commit message

```
fix(billing): show vertical package subscription status (#2501)

## Summary
- Surface enterprise vertical package subscription metadata through
billing summary, user responses, and credits-check responses.
- Show active enterprise package subscriptions as `Vertical Plan` across
sidebar/user menu/usage surfaces.
- Resolve team billing display context from the team owner while keeping
balances on the org billing team, so non-owner members inherit the
package display state.
- Avoid stale localStorage fallback after the billing hook has fetched
fresh null subscription metadata.

Linear:
https://linear.app/srpone/issue/ECA-1022/show-enterprise-package-subscription-status

## Root cause
Vertical package subscriptions are recorded as provider agreements on
the purchasing owner UID while credits are granted to the org
`billing_team_id`. The old UI mostly inferred labels from legacy `plan`
/ `user_type`, and team credits paths did not derive display metadata
from the team owner, so package users could fall back to `Pro` or `No
Plan` depending on which endpoint populated the view.

## Test plan
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_billing_summary_v2.py tests/unit/test_user_credits.py`
- [x] `pnpm exec vitest run
tests/unit/components/credits/CreditsDisplay.unit.spec.tsx
tests/unit/components/sidenav/UserInfoSection.unit.spec.tsx`
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh
web/app/src/components/credits/CreditsDisplay.tsx
web/app/src/components/sidenav/UserInfoSection.tsx
web/app/src/components/sidenav/SideNavUserSection.tsx
web/app/tests/unit/components/credits/CreditsDisplay.unit.spec.tsx
web/app/tests/unit/components/sidenav/UserInfoSection.unit.spec.tsx
web/app/src/components/billing/plan-label.ts
web/app/src/hooks/useBillingCredits.ts web/app/src/lib/api/user.ts
web/app/src/lib/auth/types.ts`
- [x] `bash scripts/verify-changed.sh`
```

### PR Description

## Summary
- Surface enterprise vertical package subscription metadata through billing summary, user responses, and credits-check responses.
- Show active enterprise package subscriptions as `Vertical Plan` across sidebar/user menu/usage surfaces.
- Resolve team billing display context from the team owner while keeping balances on the org billing team, so non-owner members inherit the package display state.
- Avoid stale localStorage fallback after the billing hook has fetched fresh null subscription metadata.

Linear: https://linear.app/srpone/issue/ECA-1022/show-enterprise-package-subscription-status

## Root cause
Vertical package subscriptions are recorded as provider agreements on the purchasing owner UID while credits are granted to the org `billing_team_id`. The old UI mostly inferred labels from legacy `plan` / `user_type`, and team credits paths did not derive display metadata from the team owner, so package users could fall back to `Pro` or `No Plan` depending on which endpoint populated the view.

## Test plan
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_billing_summary_v2.py tests/unit/test_user_credits.py`
- [x] `pnpm exec vitest run tests/unit/components/credits/CreditsDisplay.unit.spec.tsx tests/unit/components/sidenav/UserInfoSection.unit.spec.tsx`
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh web/app/src/components/credits/CreditsDisplay.tsx web/app/src/components/sidenav/UserInfoSection.tsx web/app/src/components/sidenav/SideNavUserSection.tsx web/app/tests/unit/components/credits/CreditsDisplay.unit.spec.tsx web/app/tests/unit/components/sidenav/UserInfoSection.unit.spec.tsx web/app/src/components/billing/plan-label.ts web/app/src/hooks/useBillingCredits.ts web/app/src/lib/api/user.ts web/app/src/lib/auth/types.ts`
- [x] `bash scripts/verify-changed.sh`


---

## `9462ad76a5`

- **作者**: kaka-srp
- **日期**: 2026-06-17T06:33:50Z
- **PR**: #2498
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/9462ad76a5f1aac8c7ce8333595e3d35506c1b20

### 完整 commit message

```
fix(agent-packs): relax internal submission test gate (#2498)

## Summary

- Keep public `/orgs/{org_id}/packs/{pack_id}/submissions` behind the
Agent Studio pack-test gate.
- Allow internal `/internal/agent-packs/{pack_id}/submissions` to submit
without `test_run_id` or `schema_validated`.
- Add service and route tests covering the internal no-gate path.

## Testing

- `/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_internal_agent_packs_routes.py
tests/unit/test_pack_services.py`
- `bash scripts/verify-py.sh`
```

### PR Description

## Summary

- Keep public `/orgs/{org_id}/packs/{pack_id}/submissions` behind the Agent Studio pack-test gate.
- Allow internal `/internal/agent-packs/{pack_id}/submissions` to submit without `test_run_id` or `schema_validated`.
- Add service and route tests covering the internal no-gate path.

## Testing

- `/home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_internal_agent_packs_routes.py tests/unit/test_pack_services.py`
- `bash scripts/verify-py.sh`


---

## `4d30b0b5a6`

- **作者**: bill-srp
- **日期**: 2026-06-17T04:04:38Z
- **PR**: #2497
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/4d30b0b5a68a9b6258b362b2fa3fc80d9f2ac89b

### 完整 commit message

```
fix(enterprise-admin): remove org gate and use dropdown menu (#2497)

## Summary
- Remove the `NEXT_PUBLIC_ORG_MODULE_ENABLED` build/runtime gate so
enterprise-admin org settings are always enabled.
- Replace the hand-rolled `AccountMenu` dropdown with a shadcn/Radix
`DropdownMenu` primitive.
- Add regression coverage for org settings without the env var and
keyboard-open/focus behavior in the account menu.

## Root cause
The org settings backend is already deployed, but enterprise-admin still
carried an old public env gate and deployment injection from the earlier
phased rollout. The account menu also duplicated dropdown behavior
manually instead of using the shared Radix/shadcn primitive pattern.

## Test plan
- [x] `pnpm --dir web/enterprise-admin exec vitest run
'app/(dashboard)/org/__tests__/org-page.test.tsx'
components/layout/__tests__/AccountMenu.test.tsx`
- [x] `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- [x] `pnpm --dir web/enterprise-admin run lint`
- [x] `bash scripts/verify-changed.sh` (reports `web/enterprise-admin`
has no local verify script; CI enforces sibling web packages)
```

### PR Description

## Summary
- Remove the `NEXT_PUBLIC_ORG_MODULE_ENABLED` build/runtime gate so enterprise-admin org settings are always enabled.
- Replace the hand-rolled `AccountMenu` dropdown with a shadcn/Radix `DropdownMenu` primitive.
- Add regression coverage for org settings without the env var and keyboard-open/focus behavior in the account menu.

## Root cause
The org settings backend is already deployed, but enterprise-admin still carried an old public env gate and deployment injection from the earlier phased rollout. The account menu also duplicated dropdown behavior manually instead of using the shared Radix/shadcn primitive pattern.

## Test plan
- [x] `pnpm --dir web/enterprise-admin exec vitest run 'app/(dashboard)/org/__tests__/org-page.test.tsx' components/layout/__tests__/AccountMenu.test.tsx`
- [x] `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- [x] `pnpm --dir web/enterprise-admin run lint`
- [x] `bash scripts/verify-changed.sh` (reports `web/enterprise-admin` has no local verify script; CI enforces sibling web packages)


---

## `f42b98379d`

- **作者**: david-srp
- **日期**: 2026-06-17T03:26:03Z
- **PR**: #2494
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/f42b98379d9c4baa60c9a08d824a242351c91a89

### 完整 commit message

```
feat(enterprise-admin): all-light UI, SaaS account menu & org settings hub (#2494)

## What & Why

Enterprise Admin 的三项 UI 迭代,让后台对齐正常 SaaS 企业管理后台的体验。

### Part 1 — 整站浅色
此前仅鉴权页强制浅色,内页(users / packs / org)仍跟随系统暗色。本 PR 移除 `globals.css` 的暗色
token / 滚动条覆盖块,并中和 `UserActions` / `PackTable` / `PackReviewPanel` /
`packs` 页上的 `dark:` 工具类。`force-light-surface` 保留为无害
no-op。无手动暗色开关(按产品决策)。

### Part 2 — SaaS 账户菜单
新增自包含、零依赖的 `AccountMenu`(未引入 Radix dropdown):`useState` 控制开合、`mousedown`
/ `Escape` 关闭、`role="menu"` / `menuitem` + `aria-haspopup` /
`aria-expanded` 无障碍语义。

- 菜单:头部(头像 · 姓名 · 邮箱 · 组织 · 角色)→ **组织设置** → **成员管理**(仅管理员)→
**语言**(中/EN)→ **退出登录**——全部对应真实后端接口。
- 接入 Sidebar 左下(`variant="card"`,向上弹)与 TopBar
头像(`variant="compact"`,向下弹),并把原 TopBar 独立的「退出」按钮合并进菜单。
- TopBar 在移动端(Sidebar 隐藏时)是唯一账户入口。

### Part 3 — 组织设置页补全
`/org` 由仅编辑 3 个配额,扩展为组织信息中心:

- **可编辑**(`POST /orgs/{id}`):Logo(复用
`OrgLogoField`)、组织名称、`default_computer_quota`、`default_ephemeral_quota`、`warm_pool_size`。
- **组织名称**:本 PR 合并 `origin/main` 后,后端 `OrgUpdateRequest` 已接受
`name`(1–128 字符、拒绝显式 null,见 #2412 / #2492),故移除了临时的
`ORG_NAME_UPDATE_SUPPORTED` 开关与占位提示 —— 名称现为普通可保存字段。
- **只读**:`org_type`、`created_at`(经 `formatDate` 人性化)。
- Logo 上传进行中禁用 保存/放弃。

### 部署
在 enterprise-admin 构建步骤内联
`NEXT_PUBLIC_ORG_MODULE_ENABLED=true`(`NEXT_PUBLIC_*`
为构建期变量),使账户菜单的「组织设置」在 staging/prod 进入真实页面而非 coming-soon 占位。

## 验证
- `pnpm exec tsc --noEmit` ✓
- `eslint` ✓(改动面)
- `vitest run` ✓ —— **272 passed (47 files)**,含新增的 `AccountMenu`(开合 /
角色门控 / 退出 / Escape)与 org 改名保存用例。

## 备注 / 后续
- **套餐卡片**暂未做:`useAuth` / `parseAccountMeResponse` 会丢弃订阅字段,需单独走一条
`/account/me` 查询,超出本轮范围。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What & Why

Enterprise Admin 的三项 UI 迭代,让后台对齐正常 SaaS 企业管理后台的体验。

### Part 1 — 整站浅色
此前仅鉴权页强制浅色,内页(users / packs / org)仍跟随系统暗色。本 PR 移除 `globals.css` 的暗色 token / 滚动条覆盖块,并中和 `UserActions` / `PackTable` / `PackReviewPanel` / `packs` 页上的 `dark:` 工具类。`force-light-surface` 保留为无害 no-op。无手动暗色开关(按产品决策)。

### Part 2 — SaaS 账户菜单
新增自包含、零依赖的 `AccountMenu`(未引入 Radix dropdown):`useState` 控制开合、`mousedown` / `Escape` 关闭、`role="menu"` / `menuitem` + `aria-haspopup` / `aria-expanded` 无障碍语义。

- 菜单:头部(头像 · 姓名 · 邮箱 · 组织 · 角色)→ **组织设置** → **成员管理**(仅管理员)→ **语言**(中/EN)→ **退出登录**——全部对应真实后端接口。
- 接入 Sidebar 左下(`variant="card"`,向上弹)与 TopBar 头像(`variant="compact"`,向下弹),并把原 TopBar 独立的「退出」按钮合并进菜单。
- TopBar 在移动端(Sidebar 隐藏时)是唯一账户入口。

### Part 3 — 组织设置页补全
`/org` 由仅编辑 3 个配额,扩展为组织信息中心:

- **可编辑**(`POST /orgs/{id}`):Logo(复用 `OrgLogoField`)、组织名称、`default_computer_quota`、`default_ephemeral_quota`、`warm_pool_size`。
- **组织名称**:本 PR 合并 `origin/main` 后,后端 `OrgUpdateRequest` 已接受 `name`(1–128 字符、拒绝显式 null,见 #2412 / #2492),故移除了临时的 `ORG_NAME_UPDATE_SUPPORTED` 开关与占位提示 —— 名称现为普通可保存字段。
- **只读**:`org_type`、`created_at`(经 `formatDate` 人性化)。
- Logo 上传进行中禁用 保存/放弃。

### 部署
在 enterprise-admin 构建步骤内联 `NEXT_PUBLIC_ORG_MODULE_ENABLED=true`(`NEXT_PUBLIC_*` 为构建期变量),使账户菜单的「组织设置」在 staging/prod 进入真实页面而非 coming-soon 占位。

## 验证
- `pnpm exec tsc --noEmit` ✓
- `eslint` ✓(改动面)
- `vitest run` ✓ —— **272 passed (47 files)**,含新增的 `AccountMenu`(开合 / 角色门控 / 退出 / Escape)与 org 改名保存用例。

## 备注 / 后续
- **套餐卡片**暂未做:`useAuth` / `parseAccountMeResponse` 会丢弃订阅字段,需单独走一条 `/account/me` 查询,超出本轮范围。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

