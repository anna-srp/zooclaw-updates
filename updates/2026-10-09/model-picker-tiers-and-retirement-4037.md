---
title: "模型选择器分层展示：常用 8 个直接可选，其余收进「更多模型」，下线模型会给替代项"
type: "体验优化"
priority: "高"
date: "2026-10-09"
status: "待审核"
channels: ""
---

# 模型选择器分层展示：常用 8 个直接可选，其余收进「更多模型」，下线模型会给替代项

## 核心宣传点

模型列表变清爽了。后端会读取 LiteLLM 的展示层级并在模型接口中返回，只认 1 和 2 两个层级，布尔值、数字字符串和小数会被忽略并记日志，未指定时默认按一级处理，多部署间层级冲突会告警并回落到一级，地区化的模型显示名不影响层级。前端共享的模型选择器固定展示 8 个主要模型（含当前已选），当前选中的模型即使属于二级、不可用或已下线也始终留在主列表，但不会重新变成可选项；二级模型和溢出的模型统一收进可折叠的「更多模型」，搜索仍然覆盖完整模型目录，中英文文案都已本地化。另外同时上线了 Web 端模型下线替换：命中已退役模型时会给出替代模型，权益、排序与定价规则保持不变。

## 分级

- 内部：P1
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## 备注

设计说明见 docs/superpowers/specs/2026-10-08-model-display-tiers-and-retirement.md。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `1638b8a7df0b56282e1662a0b9455f39ab59f7f8`
- PR: #4037
- 作者：tim-srp
- 日期：2026-10-09T07:34:41Z

### Commit Message

```
feat(models): add picker display tiers and web model retirement replacement (#4037)

## Linear
None linked.

## Summary
This PR ships two features. Design spec:
`docs/superpowers/specs/2026-10-08-model-display-tiers-and-retirement.md`.

### 1. Model picker display tiers
- **Backend (`claw-interface`).** The backend reads LiteLLM
`model_info.display_tier` and returns it on `/models`.
- Only the integers `1` and `2` are accepted. `bool`, numeric strings
and floats are logged and ignored.
  - The default is `1`, including when metadata is unavailable.
- Across deployments, an unspecified tier is ignored. Conflicting
explicit tiers log a warning and fall back to `1`.
  - Regional display-name overrides keep the tier.
  - The existing 300-second metadata cache is reused.
- **Shared `ModelPicker` (`@zooclaw/chat-ui`).**
- Eight primary rows, including the selected model. The selected model
stays primary even when it is tier 2, unavailable or retired, and it is
never made selectable again.
- Tier-2 and overflow models sit under a collapsed **More models** row.
  - Search covers the full catalog.
  - Copy is localized in en and zh.
- Entitlements, order, pricing, the default model and the saved Agent
model are unchanged.
- **Rollout note:** every catalog with more than eight models gets the
**More models** row and search as soon as this ships, even before any
tier is assigned.

### 2. Model retirement: web app experience only
- **Contract.** `/models` and `GET /agents/{workspace_id}/model` gain an
optional `retirement_at` field (UTC Unix seconds). The Agent model read
carries the deadline even after the model has left the selectable
catalog; the model label still comes from the catalog `display_name` or
the model-ID label.
- **Deadline mapping.** `retirement_at` is copied only from Engine
`expired_at`.
- In Engine, `expired_at` is the **admission cutoff** for new
selections. It does not stop execution.
  - Engine `retired_at` is never in the future, so it is not used.
- An unselectable model, a model absent from Engine, or a failed catalog
request never produces a deadline.
- The Agent model read is Engine-only (FastClaw V1 was removed on main
in #4028). `/models` without `runtime=engine` never reads Engine
lifecycle and has no `retirement_at`.
- **Before the deadline.** A dismissible notice appears directly above
the composer. It shows the deadline in the user's timezone with a
timezone label, and offers **Change model** (nothing preselected) and
**Dismiss**.
- It is shown at most once per rolling 24 hours, measured from when it
is displayed.
- The 24-hour limit is shared per user, model and deadline, so it holds
across refreshes, revisits and other Agents.
- A rescheduled deadline is a new notice. A cancelled deadline removes
it.
  - An open conversation never gets the notice re-inserted.
- **From the deadline.** The existing unavailable-model dialog is reused
as a required replacement.
- It opens on entry, when the deadline passes while the chat is open,
and on any send attempt. Notice suppression does not delay it.
- It has no Later or close button, and Escape and backdrop clicks are
ignored. **Back to chats** leads to `/tasks`.
- It offers only selectable, concrete, eligible models that are not the
current one, in API order, with nothing preselected or recommended.
  - The draft and history are kept.
- A failed save keeps the selected replacement, shows an inline error
and reloads the options. A chosen model that disappears from the options
is rejected.
- The dialog closes only once the Agent's model really is the
replacement. Revision controllers stay blocked until the new Revision is
active, and the computer restart flow is unchanged.
- Users who cannot change the model see a short explanation and no
confirm button.
  - A catalog load failure shows a retryable error.
- **Recommendation and preselection removed.**
- The existing missing-model dialog no longer preselects the catalog
default.
- The picker lifecycle text no longer names `expired_fallback_to` as a
"planned replacement".

### Post-PR review fixes (commit `95738ffdd`)
- **Optional change never reopens by itself.** The **Change model**
request is tied to the Agent, model and deadline it was made for. It is
cleared as soon as the dialog leaves `change` mode, for example when the
deadline passes, the missing-model prompt or billing takes over, or the
model or Agent changes.
- **A failed background refetch does not lift a known retired gate.**
TanStack keeps the last data when a refetch fails, so a deadline already
read for this Agent model stays in force.
  - A first read that fails still invents nothing.
- A later successful read with no deadline lifts the gate, so a
cancelled schedule is honoured.
- While the read is failing, a user who cannot change the model sees a
retryable load error instead of "ask an administrator".
- **App locale.** Picker lifecycle dates use the app locale in the
composer and Agent Settings, matching the notice.
- **Launcher Revision activation recovery.**
- Before this fix, a failed apply left the definition `pending`
indefinitely, with only **Back to chats**.
- The `activating` dialog now shows an inline error and **Retry**. Retry
replays the original idempotent save, or, after a reload, re-applies the
working Revision through the existing settings commit without
operations.
- Retry is not treated as activation: sending stays blocked until the
definition reports the Revision active.
  - Engine is unchanged.
- **Notice buttons.** These now have `type="button"`, so they cannot
submit the surrounding composer form. A regression spec covers this.

### Final review follow-ups
- Long retirement deadlines now schedule bounded timer wake-ups and
re-arm until the exact deadline; fake-clock tests cover a 30-day
deadline, cancellation, rescheduling and unmount cleanup. No early
retirement and send-time guard unchanged.
- Removed the unused helper export flagged by knip.
- (Superseded) An earlier session-reset test typing fix is no longer in
this PR: main #4028 deleted that V1 test file and the merge accepted the
deletion.

### Merge of origin/main (`c27748263`)
- Merged `7cb5df1dd` (#4028, FastClaw V1 removal). Conflicts:
`agent_model_service.py` kept main's Engine-only read and re-applied
only `retirement_at`; `test_openclaw_settings_routes.py` deletion
accepted. No V1 code, no `model_display_name`, no Engine edits.

### Scope reduction
- Removed the newly added `model_display_name` from the Agent model read
(schema, backend population, frontend type/query/composer, mock, tests,
spec). The retirement label uses the existing catalog `display_name`,
then the existing model-ID label. `retirement_at` is unchanged. No
replacement field.

### What this PR does not do
- **The required replacement is enforced only in the web composer.**
Engine, ACS/IM channels, the public API, schedules, ACP and WhatsApp are
**not** blocked; Engine keeps running an Agent whose model passed
`expired_at`.
- **No Engine changes** and no cross-repository changes. Engine
lifecycle semantics, the operator migration to `expired_fallback_to` and
the Auto/inherited fallbacks are unchanged.
- No deployment, no production tier assignment and no data analysis.

## Test plan
- [x] Final CI-like full web coverage on Node 24: **885 files, 11,195
passed, 0 failed**. Timer regression asserts only hook-owned
wakeups/cleanup rather than framework-global fake-timer counts; the
pre-fix hook still fails both new cases.
- [x] Backend `bash scripts/verify-py.sh`: ruff, ruff format, pyright
and import-linter all pass. The `scripts/ci-lint` guards (01–07) also
pass.
- [x] Backend pytest, model-related files
(`test_model_retirement_deadline`, `test_model_catalog_display_tier`,
`test_model_catalog`, `test_agent_model_service`,
`test_agent_model_routes`, `test_agent_builder_test_model_service`,
`test_model_retirement`, `test_model_retirement_recovery`,
`test_agent_model_environment_isolation`): 128 passed. The full backend
suite was not run locally; it runs in CI.
- [x] Web `vitest run`, full suite at `95738ffdd`: 884 files, 11191
passed, 70 skipped, 1 todo. (It was 11183 at `a34d970ec`.)
- [x] Post-review mutation checks. Each fix, when reverted on its own,
makes its new tests fail:
  - the change-flag scope: 2 tests;
  - the stale-known gate: 1 test;
  - the locale: 1 test;
  - the activation Retry: 1 test.
- [x] `@zooclaw/chat-ui` vitest: 523 passed.
- [x] Web `tsc`, eslint, governance guards, `pnpm lint:ci`
(dependency-cruiser, knip) and `pnpm dup`: all pass.
- [x] Mutation check: making the retirement send gate always allow
causes 5 of the new tests to fail.
- [x] Long-deadline hook tests: 11 passed, including 2 new regressions
that fail on old code; lint and TypeScript passed.
- [x] ~~Pydantic typing compatibility~~: superseded; those session-reset
tests were deleted on main (#4028). Post-merge pyright is covered below.
- [x] Mock backend: `MOCK_MODEL_RETIREMENT=upcoming|retired`. `/models`
and the Agent model read return `retirement_at` (checked with curl).
- [x] **Local browser walkthrough (mock only): 66/66 assertions passed,
zero page errors.** Picker/upcoming/deadline-crossing 33; retired 16;
notice-button/draft/stability supplement 17. Change/Dismiss generate no
message or conversation POST and preserve the draft; no replacement
preselection; Escape/backdrop cannot bypass the retired dialog. Reminder
stayed visible in all 40 samples over 20 seconds without a rebuild, and
refresh suppression passed. The Firebase blocker was resolved with
temporary worktree-only placeholder env; the original symlink was
restored and owned servers stopped. Shared root env was untouched. This
does not verify real Engine activation. Main runs used `95738ffdd`;
later runs included only the unused-export removal subsequently
committed as `d1dc95480`.
- [x] After removing `model_display_name` (`febff8f02`): `verify-py`
passes; backend model/agent-model pytest 52 + 403 passed; `verify-web`
(guards, tsc, eslint) and vitest on composer/agent/revision-model
suites, 116 files, 1271 tests passed. Earlier full-suite and browser
results above predate this commit.
- [x] After merging origin/main (`c27748263`): `verify-py` (ruff, ruff
format, pyright `app/ tests/`, import-linter 8/8) passed; pytest on
`test_agent_model_service`, `test_model_retirement_deadline`,
`test_model_catalog`, `test_model_catalog_display_tier`,
`test_agent_model_routes`: 84 passed; `verify-web` on
composer/agent/revision-model suites: 116 files, 1271 tests passed; CI
on `c27748263`: 41/41 non-skipped checks passed. Full backend pytest,
full web suite and browser checks were not re-run after the merge. The
follow-up spec commit `b81193599` is documentation-only.
- [ ] **Not verified: staging.** Not exercised against a real Engine
catalog with a scheduled `expired_at`.
- [ ] E2E helper (`composer-picker-controls.ts`): earlier typecheck,
lint and `--list` checks passed. The specs were not run here, against
production or staging.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

