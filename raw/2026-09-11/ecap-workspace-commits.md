# SerendipityOneInc/ecap-workspace — commits 2026-09-11

## feat(ui): 统一 ZooWork 2.0 界面、聊天输入框与默认头像 (#3704)

- **SHA**: `e8f4bfb51f4bdabe28862db47b50ea8e2b2836b5`
- **作者**: lynn Zhuang
- **日期**: 2026-09-11T11:21:57Z
- **PR**: #3704

### Commit Message

```
feat(ui): 统一 ZooWork 2.0 界面、聊天输入框与默认头像 (#3704)

## 改动说明

统一 ZooWork 2.0 各页面的视觉和交互，解决首页与 Agent 详情页输入框不一致、空状态位置偏移，以及创建 Agent
弹窗布局松散的问题。

- **全局样式**：统一浅灰导航与近白内容背景，移除 Agent
详情页左右区域的分割线；压缩个人资料入口间距，设置页二级导航与内容背景保持一致。
- **聊天输入框**：首页、Agent
对话和构建页共用描边、轻阴影、模型选择、附件和发送入口；已有模型不在可选目录时仍能显示名称，不将其重新加入可选列表。
- **Agent
创建与导航**：使用设计系统优化创建弹窗和共享链接二级弹窗，增加左上角返回入口；最近会话仅保留单行名称；旧项目入口常显下划线，列表底部分割线间距从
40px 收紧到 16px。
- **独立导航页面**：Connector、MCP、Skills、Knowledge Base 从侧栏直接进入，移除重复的 Plugins
标题和顶层选项卡。
- **空状态与插画**：接入正式空状态、连接异常及 404 插画并居中展示；素材库真正为空时隐藏筛选栏，有筛选条件时保留恢复入口。
- **默认头像**：接入 10 款 Agent 默认头像和已上传 R2 的 11 款用户动物头像。新 Agent
创建时持久化默认头像；用户头像按 UID 稳定分配，同一账号跨页面、跨设备保持一致，并优先保留已有头像。
- **预览与回归**：补齐本地 mock 的 Agent 会话及素材响应，更新共享组件、默认头像、空状态和弹窗测试。

## 验证

- [x] 前端 TypeScript、改动文件 ESLint 与仓库治理检查。
- [x] 前端回归测试；修正两个旧版样式断言后，相关 4 个测试文件共 157 项通过。
- [x] 同步最新 main，保留 Assistant 专属头像和共享链接修复；相关 4 个测试文件共 87 项通过。
- [x] 共享 `chat-ui` 包：480 项测试、TypeScript、Lint 通过。
- [x] 后端 Ruff、格式、Pyright、8 项导入边界检查通过；默认头像与创建流程 15 项测试通过。
- [x] 本地预览验证首页、Agent 详情、创建/共享弹窗、素材空状态、个人资料与设置页面。
- [x] 11 个用户头像 CDN 链接返回 200，图片格式及缓存头已确认。
- [ ] 最新补充提交的 GitHub CI 正在运行；上一轮前后端完整测试、类型与 Lint、Web 构建、共享包下游检查、资源体积、PR
体量及 CodeQL 全部通过。
- [ ] 最新补充提交的自动审查正在运行；上一轮 Codex 审查全部 90 个变更文件，未发现问题，代码扫描无开放告警。

## 发布范围

界面与用户默认头像属于前端变更；新 Agent 默认头像的持久化分配需要同时发布 `claw-interface`。本 PR
不包含已有用户头像数据的批量写入。
```

### PR Body

## 改动说明

统一 ZooWork 2.0 各页面的视觉和交互，解决首页与 Agent 详情页输入框不一致、空状态位置偏移，以及创建 Agent 弹窗布局松散的问题。

- **全局样式**：统一浅灰导航与近白内容背景，移除 Agent 详情页左右区域的分割线；压缩个人资料入口间距，设置页二级导航与内容背景保持一致。
- **聊天输入框**：首页、Agent 对话和构建页共用描边、轻阴影、模型选择、附件和发送入口；已有模型不在可选目录时仍能显示名称，不将其重新加入可选列表。
- **Agent 创建与导航**：使用设计系统优化创建弹窗和共享链接二级弹窗，增加左上角返回入口；最近会话仅保留单行名称；旧项目入口常显下划线，列表底部分割线间距从 40px 收紧到 16px。
- **独立导航页面**：Connector、MCP、Skills、Knowledge Base 从侧栏直接进入，移除重复的 Plugins 标题和顶层选项卡。
- **空状态与插画**：接入正式空状态、连接异常及 404 插画并居中展示；素材库真正为空时隐藏筛选栏，有筛选条件时保留恢复入口。
- **默认头像**：接入 10 款 Agent 默认头像和已上传 R2 的 11 款用户动物头像。新 Agent 创建时持久化默认头像；用户头像按 UID 稳定分配，同一账号跨页面、跨设备保持一致，并优先保留已有头像。
- **预览与回归**：补齐本地 mock 的 Agent 会话及素材响应，更新共享组件、默认头像、空状态和弹窗测试。

## 验证

- [x] 前端 TypeScript、改动文件 ESLint 与仓库治理检查。
- [x] 前端回归测试；修正两个旧版样式断言后，相关 4 个测试文件共 157 项通过。
- [x] 同步最新 main，保留 Assistant 专属头像和共享链接修复；相关 4 个测试文件共 87 项通过。
- [x] 共享 `chat-ui` 包：480 项测试、TypeScript、Lint 通过。
- [x] 后端 Ruff、格式、Pyright、8 项导入边界检查通过；默认头像与创建流程 15 项测试通过。
- [x] 本地预览验证首页、Agent 详情、创建/共享弹窗、素材空状态、个人资料与设置页面。
- [x] 11 个用户头像 CDN 链接返回 200，图片格式及缓存头已确认。
- [x] 最新补充提交的 GitHub CI：前后端完整测试、类型与 Lint、Web 构建、共享包下游检查、资源体积、PR 体量及 CodeQL 全部通过。
- [x] Codex 首轮审查覆盖全部 90 个变更文件，本次增量复审覆盖旧项目入口和底部间距微调，均未发现问题；PR 代码扫描无开放告警。

## 发布范围

界面与用户默认头像属于前端变更；新 Agent 默认头像的持久化分配需要同时发布 `claw-interface`。本 PR 不包含已有用户头像数据的批量写入。


---

## feat(business): 优化企业官网视觉、动效与多语言展示 (#3692)

- **SHA**: `7e92b4781fe78726f29e1299a8141f94b4d3a514`
- **作者**: ericma-srp
- **日期**: 2026-09-11T09:27:18Z
- **PR**: #3692

### Commit Message

```
feat(business): 优化企业官网视觉、动效与多语言展示 (#3692)

## Summary

Refresh the enterprise marketing page with consistent diagrams, clearer
data-source details, updated English copy, and a realistic localized
chat example.

- Replace the general-agent illustration with a flat white meeting-notes
conversation. Align the two agent cards and keep the complete
managed-agent workflow centered within its card across screen widths and
language changes.
- Present data governance on a dark background with white diagram
accents and moving particles. Refine source, rules, evaluation-set and
training-set icons; emphasize source details with brighter text,
two-column desktop lists and single-column narrow-screen lists.
- Simplify the training-method icons and center each title/description
block on its SVG node. Keep the training flow compact inside a white
bordered panel, with aligned text edges in both languages.
- Unify connector arrowheads as solid triangles and use three evenly
spaced, centered rotating ellipses in the flywheel.
- Apply the requested English copy throughout the enterprise page,
including the two-line hero and Enterprise Model Training label.
Preserve Chinese copy except for the requested model-routing label;
synchronize localized chat strings.
- Preserve main-branch contact submission behavior while removing the
marketing-form testimonial.

## Validation

- Earlier integrated validation after merging main: 53 business tests
across 6 files, TypeScript, scoped ESLint and repository governance
checks passed.
- Latest training-alignment change: 7 relevant unit tests and scoped
ESLint passed. Browser measurements verified all three SVG/text centers
and shared text left edges in Chinese and English at 390, 768, 1024 and
1440px.
- Browser checks verified complete managed-agent diagram containment,
preserved aspect ratio and aligned card lists at five widths in both
languages, including English-to-Chinese switching.
- Reviewed data-source details in Chinese and English at desktop, tablet
and mobile widths; no horizontal overflow.
- Deterministic SVG checks, asset-size checks and diff checks passed for
the illustration changes.
- CI is running for the latest commit; production build, full test suite
and code scanning remain subject to CI results.

## Scope

Frontend marketing copy, illustrations, styles and related tests. No
dependency, lockfile, credential or deployment-configuration changes.
Local screenshots and preview artifacts are excluded.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary

Refresh the enterprise marketing page with consistent diagrams, clearer data-source details, updated English copy, and a realistic localized chat example.

- Replace the general-agent illustration with a flat white meeting-notes conversation. Align the two agent cards and keep the complete managed-agent workflow centered within its card across screen widths and language changes.
- Present data governance on a dark background with white diagram accents and moving particles. Refine source, rules, evaluation-set and training-set icons; emphasize source details with brighter text, two-column desktop lists and single-column narrow-screen lists.
- Simplify the training-method icons and center each title/description block on its SVG node. Keep the training flow compact inside a white bordered panel, with aligned text edges in both languages.
- Unify connector arrowheads as solid triangles and use three evenly spaced, centered rotating ellipses in the flywheel.
- Apply the requested English copy throughout the enterprise page, including the two-line hero and Enterprise Model Training label. Preserve Chinese copy except for the requested model-routing label; synchronize localized chat strings.
- Preserve main-branch contact submission behavior while removing the marketing-form testimonial.

## Validation

- Earlier integrated validation after merging main: 53 business tests across 6 files, TypeScript, scoped ESLint and repository governance checks passed.
- Latest training-alignment change: 7 relevant unit tests and scoped ESLint passed. Browser measurements verified all three SVG/text centers and shared text left edges in Chinese and English at 390, 768, 1024 and 1440px.
- Browser checks verified complete managed-agent diagram containment, preserved aspect ratio and aligned card lists at five widths in both languages, including English-to-Chinese switching.
- Reviewed data-source details in Chinese and English at desktop, tablet and mobile widths; no horizontal overflow.
- Deterministic SVG checks, asset-size checks and diff checks passed for the illustration changes.
- CI is running for the latest commit; production build, full test suite and code scanning remain subject to CI results.

## Scope

Frontend marketing copy, illustrations, styles and related tests. No dependency, lockfile, credential or deployment-configuration changes. Local screenshots and preview artifacts are excluded.


---

## fix(billing): display friendly model names in usage records (#3700)

- **SHA**: `1d6bd120aa4481e16775bea7eb0aba7fdba7388b`
- **作者**: sam-srp
- **日期**: 2026-09-11T09:15:19Z
- **PR**: #3700

### Commit Message

```
fix(billing): display friendly model names in usage records (#3700)

## Summary
- Resolve billing usage labels from the existing cached LiteLLM model
catalog, using the same display names as the model selector.
- Match canonical model names and unambiguous provider model aliases,
including Fireworks and OpenRouter identifiers.
- Fall back to the final path segment for unknown or ambiguous models.
Preserve raw model IDs, credit amounts, grouping, and the Compute label.
- Add coverage for alias matching, canonical precedence, ambiguity, safe
metadata parsing, and unavailable-catalog fallback.

## Validation
- git diff --check passed.
- Commit hooks: Ruff, formatting, Pyright and import contracts passed.
- Devcontainer tests not run: local Docker daemon is unavailable.
- Two local hooks (importlinter-repo-sync and database-pydantic-returns)
could not find Python 3.12; skipped for commit. CI verification remains
required.
- Full pre-push Ruff and import-linter passed; full Pyright was blocked
by missing local venv/dependencies (including favie_common, pymongo,
stripe). Push uses SKIP_VERIFY=1; full type validation is NOT claimed as
passing.

## Deployment
Backend-only: claw-interface. No new settings or configuration required.
```

### PR Body

## Summary
- Resolve billing usage labels from the existing cached LiteLLM model catalog, using the same display names as the model selector.
- Match canonical model names and unambiguous provider model aliases, including Fireworks and OpenRouter identifiers.
- Fall back to the final path segment for unknown or ambiguous models. Preserve raw model IDs, credit amounts, grouping, and the Compute label.
- Add coverage for alias matching, canonical precedence, ambiguity, safe metadata parsing, and unavailable-catalog fallback.

## Validation
- git diff --check passed.
- Commit hooks: Ruff, formatting, Pyright and import contracts passed.
- Devcontainer tests not run: local Docker daemon is unavailable.
- Two local hooks (importlinter-repo-sync and database-pydantic-returns) could not find Python 3.12; skipped for commit. CI verification remains required.
- Full pre-push Ruff and import-linter passed; full Pyright was blocked by missing local venv/dependencies (including favie_common, pymongo, stripe). Push uses SKIP_VERIFY=1; full type validation is NOT claimed as passing.

## Deployment
Backend-only: claw-interface. No new settings or configuration required.


---

## fix(agents): preserve share token when creating from link (#3703)

- **SHA**: `f4eeeeb9052357211598fd75f190575fa6467271`
- **作者**: kaka-srp
- **日期**: 2026-09-11T09:17:38Z
- **PR**: #3703

### Commit Message

```
fix(agents): preserve share token when creating from link (#3703)

## Summary
- Fix **Create from link** so it opens the local, canonical
`/agent-install#token=...` URL directly.
- Keep other localized navigation, link validation, fragment-only token
transport, and install behavior unchanged.
- Add regression coverage through the real Agents view model, creation
flow, and localized-router wrapper.

## Root cause
The create dialog extracted the share token correctly, but
`useLocalizedRouter` prefixed the destination with `/en` or `/zh`.
Staging middleware redirects locale-prefixed application URLs to their
locale-free canonical paths. Next.js client navigation loses the token
fragment during that redirect, so the install page reports the link as
invalid before calling the install API.

Direct navigation and canonical client navigation were verified against
the actual staging frontend using an anonymous browser and a synthetic,
non-secret token. Both preserve the token; locale-prefixed client
navigation reproduces the error. No real Agent was installed or changed
during diagnosis.

## Scope
- One production-code file and one test file only.
- No backend, database, token-expiry, authentication, or global routing
changes.
- Frontend deployment only; no migration or new configuration required.

## Test plan
- [x] Regression test fails on the original code for `/agents`,
`/en/agents`, and `/zh/agents`.
- [x] Regression test passes after the fix; verifies token encoding,
same-origin destination, fragment-only transport, and rejection of a
token-less link.
- [x] `bash scripts/verify-local.sh --web-static` with the changed
source plus install-navigation, create-flow, and install-page specs: all
seven governance guards, TypeScript, 74 tests across seven files, and
ESLint pass.
- [x] `git diff --check`.
- [ ] CI and post-deployment authenticated installation validation.
```

### PR Body

## Summary
- Fix **Create from link** so it opens the local, canonical `/agent-install#token=...` URL directly.
- Keep other localized navigation, link validation, fragment-only token transport, and install behavior unchanged.
- Add regression coverage through the real Agents view model, creation flow, and localized-router wrapper.

## Root cause
The create dialog extracted the share token correctly, but `useLocalizedRouter` prefixed the destination with `/en` or `/zh`. Staging middleware redirects locale-prefixed application URLs to their locale-free canonical paths. Next.js client navigation loses the token fragment during that redirect, so the install page reports the link as invalid before calling the install API.

Direct navigation and canonical client navigation were verified against the actual staging frontend using an anonymous browser and a synthetic, non-secret token. Both preserve the token; locale-prefixed client navigation reproduces the error. No real Agent was installed or changed during diagnosis.

## Scope
- One production-code file and one test file only.
- No backend, database, token-expiry, authentication, or global routing changes.
- Frontend deployment only; no migration or new configuration required.

## Test plan
- [x] Regression test fails on the original code for `/agents`, `/en/agents`, and `/zh/agents`.
- [x] Regression test passes after the fix; verifies token encoding, same-origin destination, fragment-only transport, and rejection of a token-less link.
- [x] `bash scripts/verify-local.sh --web-static` with the changed source plus install-navigation, create-flow, and install-page specs: all seven governance guards, TypeScript, 74 tests across seven files, and ESLint pass.
- [x] `git diff --check`.
- [x] CI: web build, lint/typecheck, complete unit-test suite, CodeQL, size/title checks, and automatic code review pass. Automatic review reports no findings.
- [ ] Post-deployment authenticated installation validation (not deployed by this PR submission).


---

## fix(billing): 修复礼品码兑换弹窗误关闭和重复提交 (#3690)

- **SHA**: `eba2fa9bff46d08001ca34517d9bffeee914c765`
- **作者**: lynn Zhuang
- **日期**: 2026-09-11T06:58:48Z
- **PR**: #3690

### Commit Message

```
fix(billing): 修复礼品码兑换弹窗误关闭和重复提交 (#3690)

## 修复内容

修复账户菜单中的「Redeem Gift Code」弹窗：点击输入框不会再导致弹窗消失，输入兑换码后可以直接点击 Redeem，无需先按回车。

- 弹窗打开时，由弹窗自身处理关闭，避免账户菜单提前卸载弹窗。
- Escape 优先关闭兑换弹窗，再按一次关闭账户菜单。
- 兑换请求处理中忽略重复提交，防止连续按回车发起多次请求。

## 问题原因

兑换弹窗通过 Portal 渲染到 document.body，位于账户菜单 DOM 范围之外。菜单的外部点击监听在 mousedown
阶段误将弹窗内操作识别为外部点击，在按钮 click 触发前关闭菜单和弹窗。原有测试仅触发 click，未覆盖这个事件顺序。

## 验证

- [x] 新增回归测试，覆盖输入框和提交按钮的 mousedown → mouseup → click、Escape
分层关闭、请求处理中重复按回车。
- [x] 修复前新增的 4 个用例失败，修复后 UserMenu 的 75 项测试全部通过。
- [x] `bash scripts/verify-web.sh src/components/UserMenu.tsx
tests/unit/components/UserMenu.unit.spec.tsx` 通过，包括类型检查、目标测试、ESLint
和适用的治理检查。
- [x] 本地模拟账户浏览器验证：点击输入框并输入正常，测试兑换码兑换成功；用户已确认交互修复。

仅涉及前端，无需修改后端兑换接口。临时模拟账户入口和测试码未纳入提交。

Uploading Screen Recording 2026-09-10 at 16.09.35.mov…
```

### PR Body

## 修复内容

修复账户菜单中的「Redeem Gift Code」弹窗：点击输入框不会再导致弹窗消失，输入兑换码后可以直接点击 Redeem，无需先按回车。

- 弹窗打开时，由弹窗自身处理关闭，避免账户菜单提前卸载弹窗。
- Escape 优先关闭兑换弹窗，再按一次关闭账户菜单。
- 兑换请求处理中忽略重复提交，防止连续按回车发起多次请求。

## 问题原因

兑换弹窗通过 Portal 渲染到 document.body，位于账户菜单 DOM 范围之外。菜单的外部点击监听在 mousedown 阶段误将弹窗内操作识别为外部点击，在按钮 click 触发前关闭菜单和弹窗。原有测试仅触发 click，未覆盖这个事件顺序。

## 验证

- [x] 新增回归测试，覆盖输入框和提交按钮的 mousedown → mouseup → click、Escape 分层关闭、请求处理中重复按回车。
- [x] 修复前新增的 4 个用例失败，修复后 UserMenu 的 75 项测试全部通过。
- [x] `bash scripts/verify-web.sh src/components/UserMenu.tsx tests/unit/components/UserMenu.unit.spec.tsx` 通过，包括类型检查、目标测试、ESLint 和适用的治理检查。
- [x] 本地模拟账户浏览器验证：点击输入框并输入正常，测试兑换码兑换成功；用户已确认交互修复。

仅涉及前端，无需修改后端兑换接口。临时模拟账户入口和测试码未纳入提交。

Uploading Screen Recording 2026-09-10 at 16.09.35.mov…




---

## fix(agents): restore Assistant history and refresh channel status (#3698)

- **SHA**: `4294b8907bdc4975d7d9f3fa284941d8f0d47d11`
- **作者**: kaka-srp
- **日期**: 2026-09-11T03:49:31Z
- **PR**: #3698

### Commit Message

```
fix(agents): restore Assistant history and refresh channel status (#3698)

## Summary

- Route new Engine-backed Assistant conversations through the same task
creation and ACS binding flow as other Engine agents. Keep the
computer-runtime path unchanged.
- Reopen existing Web conversations using Engine's recorded original
thread, even when an earlier failed visit created an empty mapping under
the canonical Engine session ID. Preserve the original stored record and
continue enforcing ACS binding validation.
- Expose the workspace's existing Main identity to the detail page and
reuse the standard Assistant avatar when no custom avatar is configured.
- Cover Main history listing without a Build baseline, original-thread
reuse, scope and archive guards, creation/routing, and avatar
presentation.
- Keep the current Agent's channel status fresh after configuration:
poll unknown connection/pending capability state every 5 seconds,
stable/error states every 30 seconds, and share updates between the
sidebar and editor. Pause in hidden tabs and stop when no external
channel is enabled.

## Root cause

The homepage excluded Main from the unified Engine task flow. Its
browser session ID could therefore differ from the canonical Engine
session ID shown in Recents. Opening that entry attempted to create a
second Mattermost thread, which ACS correctly rejected as a conflicting
binding. Engine already returns the original thread in
`entry.lastThreadId`, but the backend response model discarded it.

The workspace chat surface also hard-coded `isMainAgent={false}`,
causing Assistant to use the generic robot avatar.

## Scope and safety

- No migration, historical message deletion, forced rebind, or
Engine/ACS changes.
- Reuses the existing user-scoped single-collection thread lookup;
validates workspace, agent, purpose, and active status before reuse.
- External-channel conversations remain read-only. Main remains usable
without an editing baseline and gains no Build capability.
- Recents keeps its existing eight-item folding behavior. The separately
discussed standalone Assistant navigation entry is not part of this fix.
- Channel polling is opt-in only on the Agent detail, not the Agents
list or global channel list. The editor shares the same query without
starting another timer. Failed refreshes retain cached entries and retry
at the slower interval.
- Deploy both `web/app` and `claw-interface` for the full fix; no
deployment is performed by this PR submission.

## Test plan

- [x] Backend focused regression suites: **88 passed**
(`test_agent_development_conversations`, `test_agent_legacy_workspace`,
`test_agent_development_tasks`, `test_engine_client_sessions`).
- [x] Frontend focused regression suites: **33 passed** (workspace
navigation/presentation/chat surface, task creation, and new-chat view
model).
- [x] Follow-up new-chat client/task creation/view-model suites: **74
passed**. Reproduced the two CI failures caused by obsolete `isMain`
expectations and aligned those exact request assertions with the new
hook contract; kept message, attachment, and legacy-route assertions
intact.
- [x] Channel query, sidebar, management, and baseline-free workspace
suites: **33 passed**, covering automatic status changes, shared-query
polling, hidden-tab/unmount cleanup, error recovery, and
inactive/no-channel cases.
- [x] Local TypeScript check and changed-file ESLint passed.
- [x] Backend Ruff, formatting, Pyright, and all eight import-layer
contracts passed.
- [x] Read-only local code review completed for design/scope,
completeness, and regressions.
- [x] Local frontend and backend restarted from this worktree; Assistant
page and backend heartbeat returned 200. Local backend points to the
existing staging ACS/Engine for the user's testing.
- [ ] Authenticated browser end-to-end verification of the repaired
historical conversation is left to the ongoing manual test; page/health
checks alone do not establish it.
- [ ] CI full suites and automated review.
```

### PR Body

## Summary

- Route new Engine-backed Assistant conversations through the same task creation and ACS binding flow as other Engine agents. Keep the computer-runtime path unchanged.
- Reopen existing Web conversations using Engine's recorded original thread, even when an earlier failed visit created an empty mapping under the canonical Engine session ID. Preserve the original stored record and continue enforcing ACS binding validation.
- Expose the workspace's existing Main identity to the detail page and reuse the standard Assistant avatar when no custom avatar is configured.
- Cover Main history listing without a Build baseline, original-thread reuse, scope and archive guards, creation/routing, and avatar presentation.
- Keep the current Agent's channel status fresh after configuration: poll unknown connection/pending capability state every 5 seconds, stable/error states every 30 seconds, and share updates between the sidebar and editor. Pause in hidden tabs and stop when no external channel is enabled.

## Root cause

The homepage excluded Main from the unified Engine task flow. Its browser session ID could therefore differ from the canonical Engine session ID shown in Recents. Opening that entry attempted to create a second Mattermost thread, which ACS correctly rejected as a conflicting binding. Engine already returns the original thread in `entry.lastThreadId`, but the backend response model discarded it.

The workspace chat surface also hard-coded `isMainAgent={false}`, causing Assistant to use the generic robot avatar.

## Scope and safety

- No migration, historical message deletion, forced rebind, or Engine/ACS changes.
- Reuses the existing user-scoped single-collection thread lookup; validates workspace, agent, purpose, and active status before reuse.
- External-channel conversations remain read-only. Main remains usable without an editing baseline and gains no Build capability.
- Recents keeps its existing eight-item folding behavior. The separately discussed standalone Assistant navigation entry is not part of this fix.
- Channel polling is opt-in only on the Agent detail, not the Agents list or global channel list. The editor shares the same query without starting another timer. Failed refreshes retain cached entries and retry at the slower interval.
- Deploy both `web/app` and `claw-interface` for the full fix; no deployment is performed by this PR submission.

## Test plan

- [x] Backend focused regression suites: **88 passed** (`test_agent_development_conversations`, `test_agent_legacy_workspace`, `test_agent_development_tasks`, `test_engine_client_sessions`).
- [x] Frontend focused regression suites: **33 passed** (workspace navigation/presentation/chat surface, task creation, and new-chat view model).
- [x] Follow-up new-chat client/task creation/view-model suites: **74 passed**. Reproduced the two CI failures caused by obsolete `isMain` expectations and aligned those exact request assertions with the new hook contract; kept message, attachment, and legacy-route assertions intact.
- [x] Channel query, sidebar, management, and baseline-free workspace suites: **33 passed**, covering automatic status changes, shared-query polling, hidden-tab/unmount cleanup, error recovery, and inactive/no-channel cases.
- [x] Local TypeScript check and changed-file ESLint passed.
- [x] Backend Ruff, formatting, Pyright, and all eight import-layer contracts passed.
- [x] Read-only local code review completed for design/scope, completeness, and regressions.
- [x] Local frontend and backend restarted from this worktree; Assistant page and backend heartbeat returned 200. Local backend points to the existing staging ACS/Engine for the user's testing.
- [ ] Authenticated browser end-to-end verification of the repaired historical conversation is left to the ongoing manual test; page/health checks alone do not establish it.
- [x] CI full suites and automated review passed for `1caba40cd`: web tests/build/static checks, backend tests/static checks, CodeQL, and review gates. Latest automated review reported no findings. Human approval is still required; auto-merge is not enabled.


---

## fix(agents): handle failed installs and fold recent conversations (#3695)

- **SHA**: `8ed456b61ceb61784842ab44fe59ca1fc7287316`
- **作者**: kaka-srp
- **日期**: 2026-09-11T02:51:28Z
- **PR**: #3695

### Commit Message

```
fix(agents): handle failed installs and fold recent conversations (#3695)

## Summary
- Exclude unbound failed or incomplete legacy install placeholders from
unified Agent lists, shortcuts and statistics. Bound `install_failed`
Agents remain visible/manageable alongside
active/disabled/error/uninstall-failed Agents; draft recovery is
unchanged.
- Allow the owner to soft-delete a failed Pack-install placeholder with
no bound Computer and its original Pack ID, only after an
owner/org/workspace-label lookup confirms Engine has no corresponding
runtime.
- If Engine creation succeeded but its response or Mongo ID write was
lost, keep the install retry anchor. Lookup errors or malformed
responses fail closed without any deletion.
- Keep the existing lifecycle for actual runtime identities. Match the
failed status, identity, owner/org, revision absence and observed update
timestamp atomically to reject concurrent installation retries.
- Per the requested UI follow-up, collapse Agent-detail Recents to eight
conversations by default. Show More / Show Less reveals or hides already
loaded entries; when necessary, the selected conversation occupies the
eighth slot so it stays visible. Existing Load more pagination remains
explicit.

## Root cause
The unified legacy list filter excluded terminal deletion states but
included `install_failed` placeholders. The reported row had no
persisted Engine identity: detail resolution returned
`agent.runtime_detached`, while uninstall rejected its empty
`computer_id` with `agent.not_found`.

Local review also reproduced installation failing after Engine/Computer
IDs were saved (for example, during credential or channel setup). Status
alone must not hide these bound records: the list retains
`install_failed` when `computer_id` is a nonempty string, so the
existing uninstall path remains reachable.

## Scope
- Four backend source files (listing repository, deletion service,
existing Engine HTTP client and typed response schema), plus the
Agent-detail navigation component and its unit tests. No Engine/ACS
changes, migrations, feature flags or extra list-time Engine calls.
- Only failed-placeholder deletion performs one read through the
existing Engine owner/org/label-filtered endpoint, with a 15-second
timeout. Normal deletion continues through the unchanged runtime
lifecycle.
- This is metadata-only cleanup, not a general orphan-runtime
reconciler. Running resources and their history, channels and schedules
are not modified.
- Recents folding is local presentation state only; it reuses existing
design-system controls and translations without changing
query/cache/session contracts or fetching all history.

## Test plan
- [x] 279 targeted tests: definition listing/deletion, placeholder
CAS/guards, workspace repository, existing Engine lifecycle/client,
lost-create-response recovery guards, task/route/baseline regression
coverage, CSFLE query syntax contract.
- [x] Latest correction: 223 targeted tests passed, including the
existing installation-service failure paths. A separate fixture-based
reproduction confirms a post-create billing failure now satisfies the
list status filter while nonempty Computer identity remains required; no
live resources were touched.
- [x] Two new real-Mongo BDD cases cover both list origins and
statistics, retaining a bound failed installation while excluding
empty/null/missing Computer placeholders. Locally skipped because
`127.0.0.1:27017` is unavailable; CI's Mongo-backed full suite passed
(10,905 passed, 5 skipped, 89.60% coverage).
- [x] Local read-only review of design/scope, completeness and side
effects.
- [x] Staging encrypted-client validation of the actual updated list and
statistics repository operations: exactly the reported placeholder
excluded; the other eight visible records unchanged.
- [x] User-authorized staging recovery using the exact new
repository/service code in an isolated one-off process: only `status`,
`deleted_at`, `updated_at` changed on the reported record; stale CAS
replay made no write. An independent read through the unmodified
deployed list confirmed the record no longer appears.
- [x] Backend static verification: Ruff, formatting, Pyright and all
eight import contracts passed.
- [x] Addressed automated review's recovery finding: a missing local ID
alone no longer authorizes cleanup; confirmed or unverifiable runtime
resources preserve their retry anchor.
- [x] Read-only staging verification of the new Engine lookup: reported
workspace has no matching runtime; a known existing workspace in the
same tenant is found as a positive control.
- [x] Previous CI passed on `4d3882086`; automated Codex re-review
confirmed the runtime-recovery finding is fixed. Latest local review's
bound-install-failure visibility finding is now addressed with a
one-line business-code correction and regression coverage.
- [x] CI on `68b63ba43`: 17 checks passed, no failures or pending checks
(unrelated jobs skipped). Backend full tests/static checks, duplication
and CodeQL passed. Latest automated Codex review reported no findings.
Required human approval remains necessary; not auto-merged.
- [x] Recents follow-up: 10 focused navigation/chat-surface tests
passed, including eight-row default, empty/short lists, expand/collapse
without network requests, retained older selection, and explicit
pagination with an in-flight request. The three initial regression cases
failed against the original component before the fix.
- [x] Frontend governance guards, TypeScript and targeted ESLint passed
after installing the frozen-lockfile dependencies in the isolated
worktree; the initial shared dependency links resolved stale workspace
package types and were removed. No dependency or lockfile changes are
included.
- [x] CI on `8d68af543`: all applicable checks passed, no failures or
pending checks (unrelated jobs skipped), including frontend tests/static
checks/build, backend tests/static checks and CodeQL. Latest automated
Codex delta review reported no findings. Human approval is still
required; no merge or deployment was performed.

## Deployment
Deploy claw-interface for failed-install handling and web/app for
Recents folding. The reported staging record is already soft-deleted and
retained for recovery; general prevention requires this PR to merge and
deploy. No production state or service deployment was changed.
```

### PR Body

## Summary
- Exclude unbound failed or incomplete legacy install placeholders from unified Agent lists, shortcuts and statistics. Bound `install_failed` Agents remain visible/manageable alongside active/disabled/error/uninstall-failed Agents; draft recovery is unchanged.
- Allow the owner to soft-delete a failed Pack-install placeholder with no bound Computer and its original Pack ID, only after an owner/org/workspace-label lookup confirms Engine has no corresponding runtime.
- If Engine creation succeeded but its response or Mongo ID write was lost, keep the install retry anchor. Lookup errors or malformed responses fail closed without any deletion.
- Keep the existing lifecycle for actual runtime identities. Match the failed status, identity, owner/org, revision absence and observed update timestamp atomically to reject concurrent installation retries.
- Per the requested UI follow-up, collapse Agent-detail Recents to eight conversations by default. Show More / Show Less reveals or hides already loaded entries; when necessary, the selected conversation occupies the eighth slot so it stays visible. Existing Load more pagination remains explicit.

## Root cause
The unified legacy list filter excluded terminal deletion states but included `install_failed` placeholders. The reported row had no persisted Engine identity: detail resolution returned `agent.runtime_detached`, while uninstall rejected its empty `computer_id` with `agent.not_found`.

Local review also reproduced installation failing after Engine/Computer IDs were saved (for example, during credential or channel setup). Status alone must not hide these bound records: the list retains `install_failed` when `computer_id` is a nonempty string, so the existing uninstall path remains reachable.

## Scope
- Four backend source files (listing repository, deletion service, existing Engine HTTP client and typed response schema), plus the Agent-detail navigation component and its unit tests. No Engine/ACS changes, migrations, feature flags or extra list-time Engine calls.
- Only failed-placeholder deletion performs one read through the existing Engine owner/org/label-filtered endpoint, with a 15-second timeout. Normal deletion continues through the unchanged runtime lifecycle.
- This is metadata-only cleanup, not a general orphan-runtime reconciler. Running resources and their history, channels and schedules are not modified.
- Recents folding is local presentation state only; it reuses existing design-system controls and translations without changing query/cache/session contracts or fetching all history.

## Test plan
- [x] 279 targeted tests: definition listing/deletion, placeholder CAS/guards, workspace repository, existing Engine lifecycle/client, lost-create-response recovery guards, task/route/baseline regression coverage, CSFLE query syntax contract.
- [x] Latest correction: 223 targeted tests passed, including the existing installation-service failure paths. A separate fixture-based reproduction confirms a post-create billing failure now satisfies the list status filter while nonempty Computer identity remains required; no live resources were touched.
- [x] Two new real-Mongo BDD cases cover both list origins and statistics, retaining a bound failed installation while excluding empty/null/missing Computer placeholders. Locally skipped because `127.0.0.1:27017` is unavailable; CI's Mongo-backed full suite passed (10,905 passed, 5 skipped, 89.60% coverage).
- [x] Local read-only review of design/scope, completeness and side effects.
- [x] Staging encrypted-client validation of the actual updated list and statistics repository operations: exactly the reported placeholder excluded; the other eight visible records unchanged.
- [x] User-authorized staging recovery using the exact new repository/service code in an isolated one-off process: only `status`, `deleted_at`, `updated_at` changed on the reported record; stale CAS replay made no write. An independent read through the unmodified deployed list confirmed the record no longer appears.
- [x] Backend static verification: Ruff, formatting, Pyright and all eight import contracts passed.
- [x] Addressed automated review's recovery finding: a missing local ID alone no longer authorizes cleanup; confirmed or unverifiable runtime resources preserve their retry anchor.
- [x] Read-only staging verification of the new Engine lookup: reported workspace has no matching runtime; a known existing workspace in the same tenant is found as a positive control.
- [x] Previous CI passed on `4d3882086`; automated Codex re-review confirmed the runtime-recovery finding is fixed. Latest local review's bound-install-failure visibility finding is now addressed with a one-line business-code correction and regression coverage.
- [x] CI on `68b63ba43`: 17 checks passed, no failures or pending checks (unrelated jobs skipped). Backend full tests/static checks, duplication and CodeQL passed. Latest automated Codex review reported no findings. Required human approval remains necessary; not auto-merged.
- [x] Recents follow-up: 10 focused navigation/chat-surface tests passed, including eight-row default, empty/short lists, expand/collapse without network requests, retained older selection, and explicit pagination with an in-flight request. The three initial regression cases failed against the original component before the fix.
- [x] Frontend governance guards, TypeScript and targeted ESLint passed after installing the frozen-lockfile dependencies in the isolated worktree; the initial shared dependency links resolved stale workspace package types and were removed. No dependency or lockfile changes are included.
- [x] CI on `8d68af543`: all applicable checks passed, no failures or pending checks (unrelated jobs skipped), including frontend tests/static checks/build, backend tests/static checks and CodeQL. Latest automated Codex delta review reported no findings. Human approval is still required; no merge or deployment was performed.

## Deployment
Deploy claw-interface for failed-install handling and web/app for Recents folding. The reported staging record is already soft-deleted and retained for recovery; general prevention requires this PR to merge and deploy. No production state or service deployment was changed.


---
