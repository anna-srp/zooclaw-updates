# ecap-workspace commits — 2026-06-26


## hotfix(billing): restore invite trial credits (#2620)

- **sha**: `d2518dbbabdd56fa3e56b421f3ee251075bb8d30`
- **author**: tim-srp
- **date**: 2026-06-26T12:04:41Z
- **PR**: #2620
- **url**: https://github.com/SerendipityOneInc/ecap-workspace/commit/d2518dbbabdd56fa3e56b421f3ee251075bb8d30

### Full commit message

```
hotfix(billing): restore invite trial credits (#2620)
```


## fix(bossclaw): prefill subscription code from url (#2618)

- **sha**: `3901785a60c7c26a9e3610e9239211510272a45f`
- **author**: tim-srp
- **date**: 2026-06-26T11:19:59Z
- **PR**: #2618
- **url**: https://github.com/SerendipityOneInc/ecap-workspace/commit/3901785a60c7c26a9e3610e9239211510272a45f

### Full commit message

```
fix(bossclaw): prefill subscription code from url (#2618)

## Summary
- Support `subscription_code=...` on the BossClaw onboarding URL.
- Prefill the redeem-code input from the server-provided query param or
browser URL fallback.
- Keep the typed value intact if the user has already entered a code
before the initial code arrives.

## Root cause
The BossClaw campaign page only forwarded `boss_key`; the redeem step
always initialized with an empty code and did not react to a
late-arriving initial value.

## Test plan
- [x] `pnpm --dir web/app test:unit tests/unit/bossclaw`
- [x] `pnpm --dir web/app exec eslint
'src/app/[locale]/bossclaw/BossclawClient.tsx'
'src/app/[locale]/bossclaw/components/RedeemStep.tsx'
'src/app/[locale]/bossclaw/page.tsx'
tests/unit/bossclaw/bossclaw-client-intro.unit.spec.tsx
tests/unit/bossclaw/page.unit.spec.tsx
tests/unit/bossclaw/redeem-step.unit.spec.tsx --quiet`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `git diff --check origin/main..HEAD`
```

### PR body

## Summary
- Support `subscription_code=...` on the BossClaw onboarding URL.
- Prefill the redeem-code input from the server-provided query param or browser URL fallback.
- Keep the typed value intact if the user has already entered a code before the initial code arrives.

## Root cause
The BossClaw campaign page only forwarded `boss_key`; the redeem step always initialized with an empty code and did not react to a late-arriving initial value.

## Test plan
- [x] `pnpm --dir web/app test:unit tests/unit/bossclaw`
- [x] `pnpm --dir web/app exec eslint 'src/app/[locale]/bossclaw/BossclawClient.tsx' 'src/app/[locale]/bossclaw/components/RedeemStep.tsx' 'src/app/[locale]/bossclaw/page.tsx' tests/unit/bossclaw/bossclaw-client-intro.unit.spec.tsx tests/unit/bossclaw/page.unit.spec.tsx tests/unit/bossclaw/redeem-step.unit.spec.tsx --quiet`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `git diff --check origin/main..HEAD`



## feat(openclaw): add dingtalk im channel (#2616)

- **sha**: `dff938ad649e8d80655f62f78ed490c6612899e2`
- **author**: kaka-srp
- **date**: 2026-06-26T10:17:33Z
- **PR**: #2616
- **url**: https://github.com/SerendipityOneInc/ecap-workspace/commit/dff938ad649e8d80655f62f78ed490c6612899e2

### Full commit message

```
feat(openclaw): add dingtalk im channel (#2616)

## Linear
https://linear.app/srpone/issue/ECA-1098/add-dingtalk-im-channel

## Summary
- Add DingTalk (`dingtalk-connector`) as an OpenClaw IM channel in ECAP
settings, including QR registration setup, manual credential setup,
polling/cancel APIs, and frontend setup UX.
- Store DingTalk connector credentials through FastClaw channel account
config and add safeguards for poll interval throttling, single-flight
success configuration, late modal cancellation, and sanitized backend
errors.
- Add DingTalk UI labels/locales/tests plus the Antom receipt repo
skill/symlink requested for this feature branch.
- Deliberately does not write
`plugins.entries["dingtalk-connector"].enabled = true` in this repo;
plugin packaging/enablement is expected to be handled outside ECAP via
openclaw-docker/runtime configuration.

## Size note
This PR carries `size-override` because it intentionally bundles the
DingTalk backend/frontend channel implementation, focused tests, and the
requested Antom receipt skill files. The effective size-check diff is
2596 lines, with the largest contributors being the Antom receipt
script, DingTalk channel backend, and DingTalk setup tests.

## Test plan
- [x] `pytest tests/unit/test_openclaw_settings_dingtalk.py -q`
- [x] `bash scripts/verify-py.sh`
- [x] `pnpm exec vitest run
tests/unit/app/api/openclaw-settings-dingtalk-routes.unit.spec.ts`
- [x] `bash scripts/verify-web.sh
web/app/src/app/[locale]/\\(app\\)/\\(chat\\)/claw-settings/components/channels/DingTalkSetupModal.tsx
web/app/src/app/[locale]/\\(app\\)/\\(chat\\)/claw-settings/components/channels/ChannelCard.tsx
web/app/src/app/api/openclaw/settings/channels/dingtalk-connector/setup/route.ts
web/app/src/app/api/openclaw/settings/channels/dingtalk-connector/poll/route.ts
web/app/src/app/api/openclaw/settings/channels/dingtalk-connector/cancel/route.ts
web/app/tests/unit/app/claw-settings/DingTalkSetupModal.unit.spec.tsx
web/app/tests/unit/app/claw-settings/ChannelsSection.unit.spec.tsx
web/app/tests/unit/app/api/openclaw-settings-dingtalk-routes.unit.spec.ts`
- [x] `bash scripts/sync-agent-skills.sh --check`
- [x] `bash scripts/verify-changed.sh`
```

### PR body

## Linear
https://linear.app/srpone/issue/ECA-1098/add-dingtalk-im-channel

## Summary
- Add DingTalk (`dingtalk-connector`) as an OpenClaw IM channel in ECAP settings, including QR registration setup, manual credential setup, polling/cancel APIs, and frontend setup UX.
- Store DingTalk connector credentials through FastClaw channel account config and add safeguards for poll interval throttling, single-flight success configuration, late modal cancellation, and sanitized backend errors.
- Add DingTalk UI labels/locales/tests plus the Antom receipt repo skill/symlink requested for this feature branch.
- Deliberately does not write `plugins.entries["dingtalk-connector"].enabled = true` in this repo; plugin packaging/enablement is expected to be handled outside ECAP via openclaw-docker/runtime configuration.

## Size note
This PR carries `size-override` because it intentionally bundles the DingTalk backend/frontend channel implementation, focused tests, and the requested Antom receipt skill files. The effective size-check diff is 2596 lines, with the largest contributors being the Antom receipt script, DingTalk channel backend, and DingTalk setup tests.

## Test plan
- [x] `pytest tests/unit/test_openclaw_settings_dingtalk.py -q`
- [x] `bash scripts/verify-py.sh`
- [x] `pnpm exec vitest run tests/unit/app/api/openclaw-settings-dingtalk-routes.unit.spec.ts`
- [x] `bash scripts/verify-web.sh web/app/src/app/[locale]/\\(app\\)/\\(chat\\)/claw-settings/components/channels/DingTalkSetupModal.tsx web/app/src/app/[locale]/\\(app\\)/\\(chat\\)/claw-settings/components/channels/ChannelCard.tsx web/app/src/app/api/openclaw/settings/channels/dingtalk-connector/setup/route.ts web/app/src/app/api/openclaw/settings/channels/dingtalk-connector/poll/route.ts web/app/src/app/api/openclaw/settings/channels/dingtalk-connector/cancel/route.ts web/app/tests/unit/app/claw-settings/DingTalkSetupModal.unit.spec.tsx web/app/tests/unit/app/claw-settings/ChannelsSection.unit.spec.tsx web/app/tests/unit/app/api/openclaw-settings-dingtalk-routes.unit.spec.ts`
- [x] `bash scripts/sync-agent-skills.sh --check`
- [x] `bash scripts/verify-changed.sh`



## ci(claw-interface): require python 3.12+ for ci-lint helpers (#2609)

- **sha**: `8855074dc3d96a6f80f35b108e7700fbe21c6ae8`
- **author**: Chris@ZooClaw
- **date**: 2026-06-26T10:10:12Z
- **PR**: #2609
- **url**: https://github.com/SerendipityOneInc/ecap-workspace/commit/8855074dc3d96a6f80f35b108e7700fbe21c6ae8

### Full commit message

```
ci(claw-interface): require python 3.12+ for ci-lint helpers (#2609)

## Summary
- Keep ci-lint Python resolution order aligned with the other lint
helpers: PATH first, then `services/claw-interface/.venv`, then
`/home/node/.venvs/claw-interface`.
- Require selected Python interpreters used by Python lint helpers to
satisfy Python 3.12+, matching the backend `requires-python = ">=3.12"`
contract.
- Make `scripts/verify-py.sh` and `scripts/verify-changed.sh` PATH-first
too, so devcontainer, GitHub CI, and activated local envs share the same
primary contract; known venv paths are fallback only.

## Verification
- `bash -n
services/claw-interface/scripts/ci-lint/06-importlinter-repo-sync.sh`
- `bash -n
services/claw-interface/scripts/ci-lint/08-database-pydantic-returns.sh`
- `services/claw-interface/scripts/ci-lint/06-importlinter-repo-sync.sh`
-
`services/claw-interface/scripts/ci-lint/08-database-pydantic-returns.sh`
- `bash -n scripts/verify-py.sh`
- `bash -n scripts/verify-changed.sh`
- fake PATH smoke: `PATH=<fake ruff/pyright/lint-imports> bash
scripts/verify-py.sh`
- fake PATH smoke: `PATH=<fake ruff/pyright/lint-imports> bash
scripts/verify-changed.sh`
- `git diff --check`

Note: this worktree does not have the backend Python toolchain
installed, so real `verify-py.sh` reports missing `ruff`/`lint-imports`;
the PATH smoke verifies resolver behavior without silently picking a
wrong toolchain.
```

### PR body

## Summary
- Keep ci-lint Python resolution order aligned with the other lint helpers: PATH first, then `services/claw-interface/.venv`, then `/home/node/.venvs/claw-interface`.
- Require selected Python interpreters used by Python lint helpers to satisfy Python 3.12+, matching the backend `requires-python = ">=3.12"` contract.
- Make `scripts/verify-py.sh` and `scripts/verify-changed.sh` PATH-first too, so devcontainer, GitHub CI, and activated local envs share the same primary contract; known venv paths are fallback only.

## Verification
- `bash -n services/claw-interface/scripts/ci-lint/06-importlinter-repo-sync.sh`
- `bash -n services/claw-interface/scripts/ci-lint/08-database-pydantic-returns.sh`
- `services/claw-interface/scripts/ci-lint/06-importlinter-repo-sync.sh`
- `services/claw-interface/scripts/ci-lint/08-database-pydantic-returns.sh`
- `bash -n scripts/verify-py.sh`
- `bash -n scripts/verify-changed.sh`
- fake PATH smoke: `PATH=<fake ruff/pyright/lint-imports> bash scripts/verify-py.sh`
- fake PATH smoke: `PATH=<fake ruff/pyright/lint-imports> bash scripts/verify-changed.sh`
- `git diff --check`

Note: this worktree does not have the backend Python toolchain installed, so real `verify-py.sh` reports missing `ruff`/`lint-imports`; the PATH smoke verifies resolver behavior without silently picking a wrong toolchain.


## feat(sidenav): 把 Session History 移到 agent 展开列表底部 (#2612)

- **sha**: `d037d5cda519a550f25fca274447bbe6665cfcaa`
- **author**: lynn Zhuang
- **date**: 2026-06-26T07:23:19Z
- **PR**: #2612
- **url**: https://github.com/SerendipityOneInc/ecap-workspace/commit/d037d5cda519a550f25fca274447bbe6665cfcaa

### Full commit message

```
feat(sidenav): 把 Session History 移到 agent 展开列表底部 (#2612)

## What & Why

调整侧边栏中 agent 展开后「Session History」入口的排序位置。

此前 agent 行展开时，**Session History** 入口渲染在会话列表的**最上方**，下方才是该 agent
的历史会话条目。本 PR 把 Session History 移到列表**最底部**（位于所有历史会话之下），符合「先看会话、再看入口」的预期。

## Changes

- `web/app/src/components/sidenav/SideNavAgentSessions.tsx`
  - 把 `Session History` 按钮从列表顶部移动到 `sessions.map(...)` 之后（列表底部）
- 纯 JSX 顺序调整，无逻辑/props/active-route 检测变更 —— `isSessionHistoryActive` /
`aria-current` 高亮逻辑基于路由而非 DOM 位置，迁移后在新位置仍正确高亮
-
`web/app/tests/unit/components/sidenav/SideNavAgentSessions.unit.spec.tsx`
- 新增排序守卫测试：断言 Session History 是展开面板内的**最后一个**条目（位于所有 session 行之后）。原有测试均为
order-agnostic（`getByTestId` / `getByText`），不会捕捉顺序回归，故补此用例锁定意图

## Verification

- `bash scripts/verify-web.sh
src/components/sidenav/SideNavAgentSessions.tsx` —— 全绿：CI guards ✓ /
`tsc --noEmit` ✓ / vitest（16 passed，含新增排序用例）✓ / eslint ✓
- 本地 mock 栈（`scripts/dev-mock.sh`，`ready-user` 场景）人工核验：展开 Assistant
后，Session History 显示在所有历史会话条目之下；无历史会话的 agent（如 Founder IP Studio）则
Session History 单独位于底部

## Risk

低。仅 sidenav 展开面板的渲染顺序调整，无数据/接口/路由/交互行为变更。

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
```

### PR body

## What & Why

调整侧边栏中 agent 展开后「Session History」入口的排序位置。

此前 agent 行展开时，**Session History** 入口渲染在会话列表的**最上方**，下方才是该 agent 的历史会话条目。本 PR 把 Session History 移到列表**最底部**（位于所有历史会话之下），符合「先看会话、再看入口」的预期。

## Changes

- `web/app/src/components/sidenav/SideNavAgentSessions.tsx`
  - 把 `Session History` 按钮从列表顶部移动到 `sessions.map(...)` 之后（列表底部）
  - 纯 JSX 顺序调整，无逻辑/props/active-route 检测变更 —— `isSessionHistoryActive` / `aria-current` 高亮逻辑基于路由而非 DOM 位置，迁移后在新位置仍正确高亮
- `web/app/tests/unit/components/sidenav/SideNavAgentSessions.unit.spec.tsx`
  - 新增排序守卫测试：断言 Session History 是展开面板内的**最后一个**条目（位于所有 session 行之后）。原有测试均为 order-agnostic（`getByTestId` / `getByText`），不会捕捉顺序回归，故补此用例锁定意图

## Verification

- `bash scripts/verify-web.sh src/components/sidenav/SideNavAgentSessions.tsx` —— 全绿：CI guards ✓ / `tsc --noEmit` ✓ / vitest（16 passed，含新增排序用例）✓ / eslint ✓
- 本地 mock 栈（`scripts/dev-mock.sh`，`ready-user` 场景）人工核验：展开 Assistant 后，Session History 显示在所有历史会话条目之下；无历史会话的 agent（如 Founder IP Studio）则 Session History 单独位于底部

## Risk

低。仅 sidenav 展开面板的渲染顺序调整，无数据/接口/路由/交互行为变更。

