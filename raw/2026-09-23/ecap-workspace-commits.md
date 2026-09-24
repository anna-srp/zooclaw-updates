# SerendipityOneInc/ecap-workspace — commits 2026-09-23

## feat(auth): allow team invitees through region checks (#3884)

- **SHA**: `a128850465d270dfed26ad514f94bb3edc0f4cae`
- **作者**: sam-srp
- **日期**: 2026-09-23T10:10:53Z
- **PR**: #3884

### Commit Message

```
feat(auth): allow team invitees through region checks (#3884)

## Summary

- pass the organization invite code through email OTP send and verify
- validate email-bound, active team invitations before bypassing
mainland or missing-region signup restrictions
- preserve existing-user and normal signup behavior; the eligibility
precheck stays read-only and final invite redemption remains atomic

## Validation

- `bash scripts/verify-web.sh --no-test`
- `bash scripts/verify-py.sh`
- targeted Web unit tests: 59 passed
- targeted claw-interface unit tests: 46 passed
- `git diff --check`

## Rollout

- deploy claw-interface before Web so the backend accepts the extended
eligibility contract
- no database migration, new environment variable, or Account Service
change
```

### PR Body

## Summary

- pass the organization invite code through email OTP send and verify
- validate email-bound, active team invitations before bypassing mainland or missing-region signup restrictions
- preserve existing-user and normal signup behavior; the eligibility precheck stays read-only and final invite redemption remains atomic

## Validation

- `bash scripts/verify-web.sh --no-test`
- `bash scripts/verify-py.sh`
- targeted Web unit tests: 59 passed
- targeted claw-interface unit tests: 46 passed
- `git diff --check`

## Rollout

- deploy claw-interface before Web so the backend accepts the extended eligibility contract
- no database migration, new environment variable, or Account Service change

---

## fix(agents): 修复从模板创建Agent路径的交互和视觉 (#3879)

- **SHA**: `ca6fc23c0cd4af8afcbb27a1d5abf038c5877bdd`
- **作者**: lynn Zhuang
- **日期**: 2026-09-23T09:51:14Z
- **PR**: #3879

### Commit Message

```
fix(agents): 修复从模板创建Agent路径的交互和视觉 (#3879)

## Changes

Improve the Create Agent and template-selection flow: neutral entry
cards, overlapping avatars, fixed-size template cards, content-adaptive
dialog height and consistent navigation, balanced margins, fixed
header/footer, and a pale edge scrollbar. Include an opt-in
nine-template local mock preview based on user screenshots. Avatar
images are delivered separately; this PR contains no generated avatar
assets or hardcoded template-to-image mapping. Cards and details use the
API-provided avatar_url.

## Explicit design requirement

The user explicitly requires ALL chat inputs on ALL pages to have NO
additional focus-state border, outline, or ring of any color. Remove the
ring added during earlier review from the shared ChatComposer itself.
Preserve the normal resting border and text caret. Buttons and other
controls retain their focus styling. This applies through
UnifiedChatComposer to new chat, sessions, Create Agent and Agent
Builder, and directly to the subagent panel. Do not reintroduce a ring
to obtain review approval; this is an explicit product decision.

The previous Codex APPROVE applied to commit 6a39119e0, before this
updated user requirement, and must not be reported as approval of the
current head.

## Validation

- ChatComposer: 51 tests passed; focused package ESLint passed.
- Template/create dialog: 9 tests passed in the preceding UI change.
- After merging current main: 30 focused app tests, full app TypeScript,
ESLint and push governance checks passed.
- Latest focus-ring removal verified in shared component source and
consumer overrides; final browser visual validation remains pending.
- No staging deployment or live template data mutation.

## Base

The PR currently targets main after an external base change. It
initially targeted feature/retire-v1-runtime to backport a focus
override fix already present on main. Current main is now merged; the
stale test conflict was resolved against current Engine behavior and
tested.

## Latest layout refinement

Dialog height follows content, capped at min(640px, 80dvh). Long content
scrolls internally; short forms no longer reserve empty space before the
footer. Entry title is centered at 24px with increased top spacing.
Template and copy steps retain their back navigation and alignment. Nine
relevant app tests pass. Browser capture is currently unavailable due to
native pipe startup failure.

Template cards use the existing brand composer shadow token, with the
shared card-elevation fallback, for a subtle resting shadow.

## Avatar handoff

Removed the three generated WebP files and local name-based avatar
resolver from the PR diff. The user received a ZIP with PNG originals,
256px WebP versions, and a template-to-filename README for engineering
to upload and configure via avatar_url.

---------

Co-authored-by: kaka-srp <kaka@srp.one>
```

### PR Body

## Changes

Improve the Create Agent and template-selection flow: neutral entry cards, overlapping avatars, fixed-size template cards, content-adaptive dialog height and consistent navigation, balanced margins, fixed header/footer, and a pale edge scrollbar. Include an opt-in nine-template local mock preview based on user screenshots. Avatar images are delivered separately; this PR contains no generated avatar assets or hardcoded template-to-image mapping. Cards and details use the API-provided avatar_url.

## Explicit design requirement

The user explicitly requires ALL chat inputs on ALL pages to have NO additional focus-state border, outline, or ring of any color. Remove the ring added during earlier review from the shared ChatComposer itself. Preserve the normal resting border and text caret. Buttons and other controls retain their focus styling. This applies through UnifiedChatComposer to new chat, sessions, Create Agent and Agent Builder, and directly to the subagent panel. Do not reintroduce a ring to obtain review approval; this is an explicit product decision.

The previous Codex APPROVE applied to commit 6a39119e0, before this updated user requirement, and must not be reported as approval of the current head.

## Validation

- ChatComposer: 51 tests passed; focused package ESLint passed.
- Template/create dialog: 9 tests passed in the preceding UI change.
- After merging current main: 30 focused app tests, full app TypeScript, ESLint and push governance checks passed.
- Latest focus-ring removal verified in shared component source and consumer overrides; final browser visual validation remains pending.
- No staging deployment or live template data mutation.

## Base

The PR currently targets main after an external base change. It initially targeted feature/retire-v1-runtime to backport a focus override fix already present on main. Current main is now merged; the stale test conflict was resolved against current Engine behavior and tested.

## Latest layout refinement

Dialog height follows content, capped at min(640px, 80dvh). Long content scrolls internally; short forms no longer reserve empty space before the footer. Entry title is centered at 24px with increased top spacing. Template and copy steps retain their back navigation and alignment. Nine relevant app tests pass. Browser capture is currently unavailable due to native pipe startup failure.

Template cards use the existing brand composer shadow token, with the shared card-elevation fallback, for a subtle resting shadow.

## Avatar handoff

Removed the three generated WebP files and local name-based avatar resolver from the PR diff. The user received a ZIP with PNG originals, 256px WebP versions, and a template-to-filename README for engineering to upload and configure via avatar_url.


---

## fix(web): 优化聊天消息与图片附件交互并统一首页 Agent 卡片尺寸 (#3880)

- **SHA**: `aa12a69ec730d19d4ed4d0c77d53879d1558e28c`
- **作者**: lynn Zhuang
- **日期**: 2026-09-23T09:26:55Z
- **PR**: #3880

### Commit Message

```
fix(web): 优化聊天消息与图片附件交互并统一首页 Agent 卡片尺寸 (#3880)

## 改动说明

统一本轮首页与聊天界面的视觉细节。优化 Chat Session
的消息排版与输入框图片附件交互：用户发送的正文图片不再包在文字气泡里，上传中的图片可直接看到缩略图和进度提示，悬停附件可查看较大预览。

- 用户消息：将 Markdown 图片提取到文字气泡外，以 80 × 80px 正方形居中裁切展示；点击可查看原图，复制保留原始消息内容。
- 消息间距：去掉 Markdown 图片内外边距的叠加，收紧文字与图片、连续图片之间的距离；移除 Agent
正文末尾额外留白，使时间戳与操作栏距内容保持 8px。
- 输入框附件：上传中显示本地图片缩略图和 loading 圆环，替换相机 emoji 与 uploading 文案；显示真实文件名，最大宽度
80px，超出省略。
- 附件 hover：提供较大图片预览，支持键盘聚焦和 Escape 关闭；使用浮层避免被输入框裁切，预览内外圆角分别为 12px /
17px。
- 附件标签：使用 6px 圆角矩形和更清晰的灰底，hover 加深；缩略图左侧、上下留白统一为 4px。
- Edit Agent：顶部标签栏横向滚动条改为细浅灰圆角，悬停或聚焦时显示，触屏保留提示。
- 同名文件上传时避免按文件名增量匹配到错误图片；本地预览 URL 在上传结束或组件卸载时释放。

另外已合入 #3882 的首页 Agent 卡片优化：Most Used Agents 与 Agents You Recently
Chatted With 两排使用相同尺寸，最大宽度 320px、高度 96px，窄屏自适应并保留横向滚动。

## 原因

上传附件与正文 Markdown 图片使用不同渲染路径，原有气泡分离样式未覆盖正文图片。Markdown
图片与正文容器存在多层边距叠加；富文本输入框上传占位原先只显示通用图标和文字状态，也没有图片 hover 预览。

## 验证

- [x] web/app 定向测试 225 项通过：输入框上传、用户消息图片分离、Markdown 图片与分段渲染。
- [x] chat-ui 定向测试 112 项通过：富文本输入框、图片预览、上传占位替换、同名文件保护、Agent 消息。
- [x] 已合并最新 main（c2ff27963）；合并后重新运行输入框定向测试，114 项通过。
- [x] TypeScript、针对改动文件的 ESLint、格式及 git diff --check 检查通过。
- [x] 本地 mock 预览已启动，用户根据实际页面多轮确认并调整间距、圆角、文件名宽度和留白。
- [x] 合入 #3882 前的 CI 检查通过，包括前端构建、完整前端测试、类型检查、lint 与 CodeQL。
- [x] 合入 #3882 并修复引用图片问题后，最新提交 4400be123 的 CI 所有适用检查通过。
- [x] 合入 #3882 前的 Codex 与 Claude 复审均 APPROVE，无新增问题。

仅涉及前端，无后端接口或依赖变更。PR 不包含本地预览示例数据，也未部署 staging。

## 自动审查处理

- 已修复紧凑型子代理聊天丢失正文图片的问题：紧凑布局现在也渲染独立附件区，并覆盖纯图片与图文混排回归测试；用户消息适配层 30
项、共享消息组件定向测试通过。
- 已修复纯图片消息复制入口消失的问题：操作栏按原始 actionText 判断，复制保留完整图片
Markdown；新增纯图片消息操作可见性及复制内容测试。
- 未采纳“已打开浮层再次 showPopover 会抛异常”的反馈：按当前 [HTML
标准](https://html.spec.whatwg.org/multipage/popover.html#check-popover-validity)，已处于目标可见状态会返回
false，show popover 随即返回；该重复调用不是 InvalidStateError 的触发条件。保留现有实现。


- 合入 #3882
后复审发现引用图片归属问题，已修复：只提取本次回复正文的图片，保留原引用前缀；新增引用旧图片、发送新图片和复制正文的组合回归测试。31
项用户消息测试、类型检查与 ESLint 通过。

- 最新 Codex 复审 APPROVE；Claude 确认引用图片修复正确，其剩余 popover 重复打开疑虑已用真实 Chromium
headless 验证：连续两次 showPopover 无异常且 :popover-open 为 true，因此不采纳该建议。
```

### PR Body

## 改动说明

统一本轮首页与聊天界面的视觉细节。优化 Chat Session 的消息排版与输入框图片附件交互：用户发送的正文图片不再包在文字气泡里，上传中的图片可直接看到缩略图和进度提示，悬停附件可查看较大预览。

- 用户消息：将 Markdown 图片提取到文字气泡外，以 80 × 80px 正方形居中裁切展示；点击可查看原图，复制保留原始消息内容。
- 消息间距：去掉 Markdown 图片内外边距的叠加，收紧文字与图片、连续图片之间的距离；移除 Agent 正文末尾额外留白，使时间戳与操作栏距内容保持 8px。
- 输入框附件：上传中显示本地图片缩略图和 loading 圆环，替换相机 emoji 与 uploading 文案；显示真实文件名，最大宽度 80px，超出省略。
- 附件 hover：提供较大图片预览，支持键盘聚焦和 Escape 关闭；使用浮层避免被输入框裁切，预览内外圆角分别为 12px / 17px。
- 附件标签：使用 6px 圆角矩形和更清晰的灰底，hover 加深；缩略图左侧、上下留白统一为 4px。
- Edit Agent：顶部标签栏横向滚动条改为细浅灰圆角，悬停或聚焦时显示，触屏保留提示。
- 同名文件上传时避免按文件名增量匹配到错误图片；本地预览 URL 在上传结束或组件卸载时释放。

另外已合入 #3882 的首页 Agent 卡片优化：Most Used Agents 与 Agents You Recently Chatted With 两排使用相同尺寸，最大宽度 320px、高度 96px，窄屏自适应并保留横向滚动。

## 原因

上传附件与正文 Markdown 图片使用不同渲染路径，原有气泡分离样式未覆盖正文图片。Markdown 图片与正文容器存在多层边距叠加；富文本输入框上传占位原先只显示通用图标和文字状态，也没有图片 hover 预览。

## 验证

- [x] web/app 定向测试 225 项通过：输入框上传、用户消息图片分离、Markdown 图片与分段渲染。
- [x] chat-ui 定向测试 112 项通过：富文本输入框、图片预览、上传占位替换、同名文件保护、Agent 消息。
- [x] 已合并最新 main（c2ff27963）；合并后重新运行输入框定向测试，114 项通过。
- [x] TypeScript、针对改动文件的 ESLint、格式及 git diff --check 检查通过。
- [x] 本地 mock 预览已启动，用户根据实际页面多轮确认并调整间距、圆角、文件名宽度和留白。
- [x] 合入 #3882 前的 CI 检查通过，包括前端构建、完整前端测试、类型检查、lint 与 CodeQL。
- [x] 合入 #3882 并修复引用图片问题后，最新提交 4400be123 的 CI 所有适用检查通过。
- [x] 合入 #3882 前的 Codex 与 Claude 复审均 APPROVE，无新增问题。

仅涉及前端，无后端接口或依赖变更。PR 不包含本地预览示例数据，也未部署 staging。

## 自动审查处理

- 已修复紧凑型子代理聊天丢失正文图片的问题：紧凑布局现在也渲染独立附件区，并覆盖纯图片与图文混排回归测试；用户消息适配层 30 项、共享消息组件定向测试通过。
- 已修复纯图片消息复制入口消失的问题：操作栏按原始 actionText 判断，复制保留完整图片 Markdown；新增纯图片消息操作可见性及复制内容测试。
- 未采纳“已打开浮层再次 showPopover 会抛异常”的反馈：按当前 [HTML 标准](https://html.spec.whatwg.org/multipage/popover.html#check-popover-validity)，已处于目标可见状态会返回 false，show popover 随即返回；该重复调用不是 InvalidStateError 的触发条件。保留现有实现。


- 合入 #3882 后复审发现引用图片归属问题，已修复：只提取本次回复正文的图片，保留原引用前缀；新增引用旧图片、发送新图片和复制正文的组合回归测试。31 项用户消息测试、类型检查与 ESLint 通过。

- 最新 Codex 复审 APPROVE；Claude 确认引用图片修复正确，其剩余 popover 重复打开疑虑已用真实 Chromium headless 验证：连续两次 showPopover 无异常且 :popover-open 为 true，因此不采纳该建议。


---

## fix(web): refresh agent video and brand badges (#3883)

- **SHA**: `43f8dd80ded88bf1528124acf4233425b2a12188`
- **作者**: shana-srp
- **日期**: 2026-09-23T09:01:43Z
- **PR**: #3883

### Commit Message

```
fix(web): refresh agent video and brand badges (#3883)

## Summary
- Update the Agents welcome video to the supplied hosted MP4, remove the
previous video's poster, and preload metadata while keeping playback
controls and layout.
- Remove the logo from the sidebar PRO badge and reduce its displayed
height to 16px.
- Replace the homepage model section's Kimi icon with the supplied black
K and blue dot artwork.

## Root cause
The interface used the previous introduction video and branding assets.
This updates those assets and the PRO badge dimensions to the approved
design.

## Test plan
- [x] Synced branch with main at cc4281f797.
- [x] Frontend governance checks, TypeScript, and targeted ESLint passed
via scripts/verify-web.sh.
- [x] Related UserCard tests passed: 33 tests.
- [x] Asset size check and git diff --check passed.
- [x] Browser verified the Agents video loaded (107 seconds, no media
error), the compact text-only PRO badge, and the new Kimi logo.

Frontend-only change. Local mock data and Firebase preview configuration
are not included.

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary
- Update the Agents welcome video to the supplied hosted MP4, remove the previous video's poster, and preload metadata while keeping playback controls and layout.
- Remove the logo from the sidebar PRO badge and reduce its displayed height to 16px.
- Replace the homepage model section's Kimi icon with the supplied black K and blue dot artwork.

## Root cause
The interface used the previous introduction video and branding assets. This updates those assets and the PRO badge dimensions to the approved design.

## Test plan
- [x] Synced branch with main at cc4281f797.
- [x] Frontend governance checks, TypeScript, and targeted ESLint passed via scripts/verify-web.sh.
- [x] Related UserCard tests passed: 33 tests.
- [x] Asset size check and git diff --check passed.
- [x] Browser verified the Agents video loaded (107 seconds, no media error), the compact text-only PRO badge, and the new Kimi logo.

Frontend-only change. Local mock data and Firebase preview configuration are not included.


---

## refactor(agents): retire FastClaw v1 routing (#3874)

- **SHA**: `cc4281f7977e2da20d4f536177d68c786387581e`
- **作者**: kaka-srp
- **日期**: 2026-09-23T08:52:24Z
- **PR**: #3874

### Commit Message

```
refactor(agents): retire FastClaw v1 routing (#3874)

## Summary
- Remove FastClaw V1 rollout switches, account provisioning, runtime
selection, route registration, and Web compatibility fallbacks so active
product entry points use ZooClaw Engine exclusively.
- Unregister the legacy ClawHub bot endpoints and remove their Next.js
BFF route. The old Skills Store source remains for the separately scoped
step 3 cleanup; the current Skill Registry remains unchanged.
- Keep iOS source unchanged. Its existing `/agents/install-capability`
request remains compatible because the authenticated backend endpoint
now returns a constant Engine response.
- Record the completed production cleanup: 5,009 V1 bot records removed,
2,933 legacy Computer records retired, seven orphan ConfigMaps removed,
and independent readback confirming zero V1 bot workloads while 1,945
Engine workspace records remained intact.
- Remove the retired Pack Test chat preview routing and temporary
Mattermost-session UI while preserving the production-active Agent
Builder V2 flow. Leave the remaining unreachable implementation files
for the separately scoped step 3 deletion.

The `size-override` is intentional: the diff is dominated by deleting V1
compatibility tests and branches across the backend and Web. Splitting
those removals would temporarily leave mismatched runtime contracts
between the two surfaces.

## Usage verification
- Current product entry: `/plugins?tab=skills` renders
`SkillRegistryClient` and uses the `/skills` registry API. Legacy
`/skills/search` and `/skills/[category]/[slug]` pages redirect to that
entry.
- Production logs from 2026-09-18 through 2026-09-23 contain zero
requests to `/openclaw/runtime-skills` or `/bots/*/clawhub`. The last
successful requests were 2026-09-11 and 2026-08-31 respectively.
- Over the same recent window, the active `/skills` registry had 141
unique request IDs from 38 users. `/agents/{workspace}/skills` also
remains active and is unchanged.
- Based on those boundaries, this PR removes only the inactive ClawHub
route registrations. It does not migrate the dead flow or modify the
active Skill Registry.
- Marketplace `?agent_id=` deep links and Landing `?sp=` handoffs are
still active Engine flows. Their obsolete FastClaw init-status gate was
removed while auth, onboarding, catalog, agent-loading, and Mattermost
send-readiness gates remain.
- Legacy `/connectors/google/*` has no frontend caller and no production
traffic since at least 2026-08-01; Council has no product entry and no
production API traffic since at least 2026-09-01. Their backend routers
are now unregistered. Active Composio and Engine workspace connector
APIs are unchanged.
- Agent Builder V2 still had production traffic on 2026-09-21, so it was
preserved. Pack Test itself had no production request after 2026-09-09;
its `computer_id` chat override, review bar, preview-session query, and
temporary Mattermost connection are removed without changing Builder V2.

## Test plan
- [x] Production cleanup independently re-read through API, MongoDB,
PostgreSQL audit, and Kubernetes inventory; durable audit correlation:
`fastclaw-retirement-prod-20260922`.
- [x] Local services started exactly from `.vscode/tasks.json` against
staging dependencies. Authenticated Marketplace
install/detail/chat/uninstall, Builder, Council, Plugins, and active
Skill Registry flows were exercised.
- [x] Authenticated local smoke confirmed the active `/skills` API
returns 27 items and the Plugins Skills tab loads; legacy backend
`/bots/{id}/clawhub` and frontend `/api/openclaw/clawhub/{action}` now
return 404.
- [x] Backend full suite before final focused follow-up: 11,662 passed,
290 skipped, zero failed. Final route-wiring suite: 9 passed; Ruff,
format, Pyright, and import contracts passed.
- [x] Frontend full suite before final focused follow-up: 10,486 passed,
70 skipped, one todo. Active Skill Registry focused suite: 40 passed.
- [x] Landing/deep-link focused regression suite: 115 passed, including
an explicit `initStatus: idle` integration assertion. Pack
Test/chat/Mattermost focused suites: 130 passed; TypeScript,
changed-file ESLint, and `lint:ci` passed afterward.
- [x] Authenticated local staging-backed comparison of an active Engine
workspace with and without a stale `computer_id` produced identical
rendered output, zero `/computers` or Pack Test requests, and zero 5xx
responses. Mattermost HTTP authentication reached staging in the latest
rerun; the WebSocket handshake was rejected with 403 by staging Origin
policy, so message send/reply was not re-proven on the final HEAD.
- [x] Final Web `lint:ci`, TypeScript, ESLint, backend Ruff, format,
full Pyright, and import contracts passed.
- [x] Next.js production compile passed earlier on the final behavior.
The final PR has no iOS source diff.
```

### PR Body

## Summary
- Remove FastClaw V1 rollout switches, account provisioning, runtime selection, route registration, and Web compatibility fallbacks so active product entry points use ZooClaw Engine exclusively.
- Unregister the legacy ClawHub bot endpoints and remove their Next.js BFF route. The old Skills Store source remains for the separately scoped step 3 cleanup; the current Skill Registry remains unchanged.
- Keep iOS source unchanged. Its existing `/agents/install-capability` request remains compatible because the authenticated backend endpoint now returns a constant Engine response.
- Record the completed production cleanup: 5,009 V1 bot records removed, 2,933 legacy Computer records retired, seven orphan ConfigMaps removed, and independent readback confirming zero V1 bot workloads while 1,945 Engine workspace records remained intact.
- Remove the retired Pack Test chat preview routing and temporary Mattermost-session UI while preserving the production-active Agent Builder V2 flow. Leave the remaining unreachable implementation files for the separately scoped step 3 deletion.

The `size-override` is intentional: the diff is dominated by deleting V1 compatibility tests and branches across the backend and Web. Splitting those removals would temporarily leave mismatched runtime contracts between the two surfaces.

## Usage verification
- Current product entry: `/plugins?tab=skills` renders `SkillRegistryClient` and uses the `/skills` registry API. Legacy `/skills/search` and `/skills/[category]/[slug]` pages redirect to that entry.
- Production logs from 2026-09-18 through 2026-09-23 contain zero requests to `/openclaw/runtime-skills` or `/bots/*/clawhub`. The last successful requests were 2026-09-11 and 2026-08-31 respectively.
- Over the same recent window, the active `/skills` registry had 141 unique request IDs from 38 users. `/agents/{workspace}/skills` also remains active and is unchanged.
- Based on those boundaries, this PR removes only the inactive ClawHub route registrations. It does not migrate the dead flow or modify the active Skill Registry.
- Marketplace `?agent_id=` deep links and Landing `?sp=` handoffs are still active Engine flows. Their obsolete FastClaw init-status gate was removed while auth, onboarding, catalog, agent-loading, and Mattermost send-readiness gates remain.
- Legacy `/connectors/google/*` has no frontend caller and no production traffic since at least 2026-08-01; Council has no product entry and no production API traffic since at least 2026-09-01. Their backend routers are now unregistered. Active Composio and Engine workspace connector APIs are unchanged.
- Agent Builder V2 still had production traffic on 2026-09-21, so it was preserved. Pack Test itself had no production request after 2026-09-09; its `computer_id` chat override, review bar, preview-session query, and temporary Mattermost connection are removed without changing Builder V2.

## Test plan
- [x] Production cleanup independently re-read through API, MongoDB, PostgreSQL audit, and Kubernetes inventory; durable audit correlation: `fastclaw-retirement-prod-20260922`.
- [x] Local services started exactly from `.vscode/tasks.json` against staging dependencies. Authenticated Marketplace install/detail/chat/uninstall, Builder, Council, Plugins, and active Skill Registry flows were exercised.
- [x] Authenticated local smoke confirmed the active `/skills` API returns 27 items and the Plugins Skills tab loads; legacy backend `/bots/{id}/clawhub` and frontend `/api/openclaw/clawhub/{action}` now return 404.
- [x] Backend full suite before final focused follow-up: 11,662 passed, 290 skipped, zero failed. Final route-wiring suite: 9 passed; Ruff, format, Pyright, and import contracts passed.
- [x] Frontend full suite before final focused follow-up: 10,486 passed, 70 skipped, one todo. Active Skill Registry focused suite: 40 passed.
- [x] Landing/deep-link focused regression suite: 115 passed, including an explicit `initStatus: idle` integration assertion. Pack Test/chat/Mattermost focused suites: 130 passed; TypeScript, changed-file ESLint, and `lint:ci` passed afterward.
- [x] Authenticated local staging-backed comparison of an active Engine workspace with and without a stale `computer_id` produced identical rendered output, zero `/computers` or Pack Test requests, and zero 5xx responses. Mattermost HTTP authentication reached staging in the latest rerun; the WebSocket handshake was rejected with 403 by staging Origin policy, so message send/reply was not re-proven on the final HEAD.
- [x] Final Web `lint:ci`, TypeScript, ESLint, backend Ruff, format, full Pyright, and import contracts passed.
- [x] Next.js production compile passed earlier on the final behavior. The final PR has no iOS source diff.




---

## fix(chat): make task tool approvals actionable (#3870)

- **SHA**: `9296c3bf44220cf077e7f6278142209cd37f5443`
- **作者**: sharplee-srp
- **日期**: 2026-09-23T08:37:14Z
- **PR**: #3870

### Commit Message

```
fix(chat): make task tool approvals actionable (#3870)

## Summary
Web Tasks now show an actionable confirmation/cancel card when a tool
waits for approval, and display “Waiting for approval” instead of a
running tool spinner/timer. A plain “确认”/“取消” reply in the Task is
converted to an explicit approval command only when exactly one
unexpired, unsubmitted approval is present.

Metadata-only approvals are retained through runtime filtering and
rendering even when their text is empty. Cards follow durable
request/resolution metadata, survive history replay, disable after
submission/expiry/resolution, prevent duplicate clicks, and allow retry
after a failed send. Approval lifecycle events are correlated by
conversation and the Engine’s globally unique approval ID; tool-step
projection also matches the run and tool-call ID. Ordinary replies
arriving during approval display as queued. While approval is pending,
the composer remains available so a typed confirmation can be sent.
Deleted provisional status posts are excluded from thread views even if
a late WebSocket edit arrives after their deletion, preventing stale
running/unknown status after the tool has finished.

## Root cause
Task conversations are Mattermost threads with group semantics. ACS
deliberately accepts plain confirmation words only in direct chats, so
“确认” in a Task was queued as normal input. The tool UI also treated
`awaiting_approval` as actively running.

Companion contract:
https://github.com/SerendipityOneInc/agent-channel-service/pull/145.
Deploy ACS before Web. Existing historical text-only approval posts keep
their explicit slash-command path; buttons require the new structured
metadata. Feishu confirmation behavior and backend group approval
restrictions are unchanged.

## Test plan
- [x] Rebased onto `c2ff27963` (head `549f50efc`): preserved Build
`/new` validation before Task approval-reply conversion. All 239
targeted tests across 8 files passed, including both sides of the
conflict; TypeScript, ESLint and changed-surface governance checks
passed. The 5/5 local E2E below was run on the explicitly recorded
pre-rebase head, not claimed as a fresh E2E of this head.
- [x] Focused approval/card/real message component integration: 66 tests
passed.
- [x] Runtime/message integration after the metadata-only review fix: 82
tests passed.
- [x] Existing typewriter hook tests: 23 passed.
- [x] Targeted tool-status/activity/shared tool-group tests passed;
package ToolGroup suite: 70 passed.
- [x] Web TypeScript, ESLint and governance checks passed; repository
commit/push gates run before submission.
- [x] Composer confirmation/cancellation regression and approval
helpers: 63 tests passed.
- [x] Deleted-placeholder race regression (red → green), thread
component and waiting reconciliation: 85 tests passed.
- [x] Fresh isolated browser E2E (Web `21f0a1bfd`, ACS `e34f54b`, Engine
`78bd62c`): button confirm/cancel, typed 确认/取消, and reload-then-confirm
all passed. Every pending approval had zero tool executions; each
approval executed once and each denial executed zero times. All five
runs completed, and the composer returned to send mode without stale
running/unknown status.
- [x] Runtime audit: 64 outbox events published, 40 channel deliveries
sent, 45 receiver outputs acknowledged; no pending/failed deliveries.
Full-size browser screenshots inspected.
- Scope: actual local Engine/Temporal/Postgres/Redis/ACS/Mattermost and
Chrome; account/workspace metadata and a harmless MCP counter were
isolated fixtures. This does not claim deployed staging or Feishu
acceptance.
- [ ] Deployed ACS → Engine → outbox → Web/channel E2E after coordinated
rollout. No staging/production approval action or deployment was
performed for this PR.
```

### PR Body

## Summary
Web Tasks now show an actionable confirmation/cancel card when a tool waits for approval, and display “Waiting for approval” instead of a running tool spinner/timer. A plain “确认”/“取消” reply in the Task is converted to an explicit approval command only when exactly one unexpired, unsubmitted approval is present.

Metadata-only approvals are retained through runtime filtering and rendering even when their text is empty. Cards follow durable request/resolution metadata, survive history replay, disable after submission/expiry/resolution, prevent duplicate clicks, and allow retry after a failed send. Approval lifecycle events are correlated by conversation and the Engine’s globally unique approval ID; tool-step projection also matches the run and tool-call ID. Ordinary replies arriving during approval display as queued. While approval is pending, the composer remains available so a typed confirmation can be sent. Deleted provisional status posts are excluded from thread views even if a late WebSocket edit arrives after their deletion, preventing stale running/unknown status after the tool has finished.

## Root cause
Task conversations are Mattermost threads with group semantics. ACS deliberately accepts plain confirmation words only in direct chats, so “确认” in a Task was queued as normal input. The tool UI also treated `awaiting_approval` as actively running.

Companion contract: https://github.com/SerendipityOneInc/agent-channel-service/pull/145. Deploy ACS before Web. Existing historical text-only approval posts keep their explicit slash-command path; buttons require the new structured metadata. Feishu confirmation behavior and backend group approval restrictions are unchanged.

## Test plan
- [x] Rebased onto `c2ff27963` (head `549f50efc`): preserved Build `/new` validation before Task approval-reply conversion. All 239 targeted tests across 8 files passed, including both sides of the conflict; TypeScript, ESLint and changed-surface governance checks passed. The 5/5 local E2E below was run on the explicitly recorded pre-rebase head, not claimed as a fresh E2E of this head.
- [x] Focused approval/card/real message component integration: 66 tests passed.
- [x] Runtime/message integration after the metadata-only review fix: 82 tests passed.
- [x] Existing typewriter hook tests: 23 passed.
- [x] Targeted tool-status/activity/shared tool-group tests passed; package ToolGroup suite: 70 passed.
- [x] Web TypeScript, ESLint and governance checks passed; repository commit/push gates run before submission.
- [x] Composer confirmation/cancellation regression and approval helpers: 63 tests passed.
- [x] Deleted-placeholder race regression (red → green), thread component and waiting reconciliation: 85 tests passed.
- [x] Fresh isolated browser E2E (Web `21f0a1bfd`, ACS `e34f54b`, Engine `78bd62c`): button confirm/cancel, typed 确认/取消, and reload-then-confirm all passed. Every pending approval had zero tool executions; each approval executed once and each denial executed zero times. All five runs completed, and the composer returned to send mode without stale running/unknown status.
- [x] Runtime audit: 64 outbox events published, 40 channel deliveries sent, 45 receiver outputs acknowledged; no pending/failed deliveries. Full-size browser screenshots inspected.
- Scope: actual local Engine/Temporal/Postgres/Redis/ACS/Mattermost and Chrome; account/workspace metadata and a harmless MCP counter were isolated fixtures. This does not claim deployed staging or Feishu acceptance.
- [ ] Deployed ACS → Engine → outbox → Web/channel E2E after coordinated rollout. No staging/production approval action or deployment was performed for this PR.



---

## fix(landing): update GLM model logo (#3881)

- **SHA**: `30fce6f9d7a8dc95c86a04afeee918cbb1aa202c`
- **作者**: shana-srp
- **日期**: 2026-09-23T08:08:21Z
- **PR**: #3881

### Commit Message

```
fix(landing): update GLM model logo (#3881)

## Summary
Replace the homepage model row's blue GLM icon with the supplied black Z
logo. Add the original PNG and update the GLM image reference while
preserving the existing circle, sizing, and animation.

## Validation
- `bash scripts/verify-web.sh --no-test
src/app/landing/components/ZooworkHomeSections.tsx` passed (governance
guards, TypeScript, ESLint).
- Prettier and `git diff --check` passed.
- Verified the rendered homepage and replacement logo in the local
browser at `/#platform`.

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary
Replace the homepage model row's blue GLM icon with the supplied black Z logo. Add the original PNG and update the GLM image reference while preserving the existing circle, sizing, and animation.

## Validation
- `bash scripts/verify-web.sh --no-test src/app/landing/components/ZooworkHomeSections.tsx` passed (governance guards, TypeScript, ESLint).
- Prettier and `git diff --check` passed.
- Verified the rendered homepage and replacement logo in the local browser at `/#platform`.


---

## style(auth): refresh signup copy, video and typography (#3877)

- **SHA**: `50fb2c50c08a166ae97ec78f58077a53de75725c`
- **作者**: shana-srp
- **日期**: 2026-09-23T08:08:08Z
- **PR**: #3877

### Commit Message

```
style(auth): refresh signup copy, video and typography (#3877)

## Summary
- Update the signup page heading to “Deploy your expertise” and subtitle
to “Agent delivery platform for domain experts” using dedicated signup
copy keys, preserving the shared login/checkout prompts. The subtitle
intentionally has no trailing period, as explicitly requested by the
user; this is the final approved copy.
- Shorten the English email placeholder to “Enter your email”.
- Replace the right-side visual with the supplied 5.63-second video and
matching poster. The silent H.264 MP4 is 571 KB; the poster is 88 KB.
Existing layout dimensions and playback behavior are unchanged.

- Refine heading word spacing: -0.192em for the main heading and -2.8px
for the subtitle; request subtitle weight 500 (the current GFS Didot
font supplies only its regular face).

## Test plan
- [x] Verify the new copy and video in the local browser; video playback
reached readyState 4 with the expected 1080×1348 dimensions and
5.63-second duration.
- [x] Confirm both assets are below repository size limits.
- [x] Governance guards, TypeScript, and scoped ESLint pass on updated
main.
- [x] Five relevant test files pass (96 tests): SignupVisual, LoginForm,
zoowork-login-page, landing-content, and login-branding.

- [x] Browser measurements confirm heading spaces at 8.97px (56px font)
and subtitle spaces at 3.55px (18px font), matching the reference
spacing closely.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary
- Update the signup page heading to “Deploy your expertise” and subtitle to “Agent delivery platform for domain experts” using dedicated signup copy keys, preserving the shared login/checkout prompts. The subtitle intentionally has no trailing period, as explicitly requested by the user; this is the final approved copy.
- Shorten the English email placeholder to “Enter your email”.
- Replace the right-side visual with the supplied 5.63-second video and matching poster. The silent H.264 MP4 is 571 KB; the poster is 88 KB. Existing layout dimensions and playback behavior are unchanged.

- Refine heading word spacing: -0.192em for the main heading and -2.8px for the subtitle; request subtitle weight 500 (the current GFS Didot font supplies only its regular face).

## Test plan
- [x] Verify the new copy and video in the local browser; video playback reached readyState 4 with the expected 1080×1348 dimensions and 5.63-second duration.
- [x] Confirm both assets are below repository size limits.
- [x] Governance guards, TypeScript, and scoped ESLint pass on updated main.
- [x] Five relevant test files pass (96 tests): SignupVisual, LoginForm, zoowork-login-page, landing-content, and login-branding.

- [x] Browser measurements confirm heading spaces at 8.97px (56px font) and subtitle spaces at 3.55px (18px font), matching the reference spacing closely.




---

## feat(mcp): honor tool default enabled metadata (#3876)

- **SHA**: `c2ff27963f2e3d9bef010ca719af0c3ff263e368`
- **作者**: tim-srp
- **日期**: 2026-09-23T07:17:30Z
- **PR**: #3876

### Commit Message

```
feat(mcp): honor tool default enabled metadata (#3876)

## Behavior

MCP tools can recommend an initial enabled state through
`_meta["ecap/defaultEnabled"]`. Each personal connection applies
explicit false values to its own `disabled_tools` on its first
successful catalog discovery, including recovery after a failed creation
probe. User toggles then continue through the existing persistence and
Engine synchronization paths.

Metadata survives model serialization and public projection. Missing
metadata keeps the existing enabled-by-default behavior.

## Scope and review resolution

- Fixed the Codex P1: failed initial discovery no longer bypasses
defaults on recovery.
- Fixed the Claude alias observation: metadata survives a model
dump/validation round trip.
- Existing initialized connections retain their settings. Newly added
tools on a later refresh do not receive defaults in this change; this
preserves the agreed initialization-only scope. A successful empty
catalog also counts as initialized. Regression coverage pins this
boundary.
- No existing-user migration or server/tool-name special cases.

## Validation

25 targeted service/schema/sync tests pass; Ruff passes. Failed-probe
recovery and metadata round-trip regressions were reproduced before the
fix.

Producer: https://github.com/SerendipityOneInc/ecap-mcp/pull/123. Deploy
the consumer before the producer to interpret metadata on newly created
connections.
```

### PR Body

## Behavior

MCP tools can recommend an initial enabled state through `_meta["ecap/defaultEnabled"]`. Each personal connection applies explicit false values to its own `disabled_tools` on its first successful catalog discovery, including recovery after a failed creation probe. User toggles then continue through the existing persistence and Engine synchronization paths.

Metadata survives model serialization and public projection. Missing metadata keeps the existing enabled-by-default behavior.

## Scope and review resolution

- Fixed the Codex P1: failed initial discovery no longer bypasses defaults on recovery.
- Fixed the Claude alias observation: metadata survives a model dump/validation round trip.
- Existing initialized connections retain their settings. Newly added tools on a later refresh do not receive defaults in this change; this preserves the agreed initialization-only scope. A successful empty catalog also counts as initialized. Regression coverage pins this boundary.
- No existing-user migration or server/tool-name special cases.

## Validation

25 targeted service/schema/sync tests pass; Ruff passes. Failed-probe recovery and metadata round-trip regressions were reproduced before the fix.

Producer: https://github.com/SerendipityOneInc/ecap-mcp/pull/123. Deploy the consumer before the producer to interpret metadata on newly created connections.


---

## fix(landing): update ZooData copy across all locales (#3868)

- **SHA**: `bb644fa874d41ff9c739b8776f3009954c7ce433`
- **作者**: ericma-srp
- **日期**: 2026-09-23T04:02:16Z
- **PR**: #3868

### Commit Message

```
fix(landing): update ZooData copy across all locales (#3868)

## 改动概述

更新官网首页 ZooData 卡片的产品说明，并将全部 10 个语言版本统一到最终英文文案。调整集中在产品定位、Token
节省表述、付费口径和数据覆盖范围。

- **Token 节省表述**：将“约减少 75%”调整为“最多减少 75% 的 LLM Token”。
- **付费口径**：将“仅为使用的字段付费”调整为“仅为使用的数据付费”。
- **数据覆盖与定位**：将 Amazon / TikTok
的预分析商业情报描述，调整为电商、金融、外卖和社交平台的实时结构化数据描述；移除本段中的竞品、市场、流量、消费者分析及 API / CLI /
MCP 附带能力表述。
-
**多语言一致性**：以最终英文为基准，更新中文、日语、韩语、德语、法语、西班牙语、意大利语、葡萄牙语和阿拉伯语译文。英文使用正确的主谓形式“ZooData
turns”；该语法修正不改变其他语言译文。
- **页面与翻译联动**：同步首页组件及 10 份语言字典的索引，确保各语言页面能读取对应译文。

## 最终英文文案

> ZooData turns any URL into agent-ready JSON with up to 75% fewer LLM
tokens—and pay only for the data you use. Access real-time, structured
data across e-commerce, finance, food delivery, and social platforms.

## 影响范围

共修改 11 个文件：1 个首页组件和 10 份语言字典，均限于 ZooData
的这一段说明。此次为产品文案更新，不包含数据接口或后端能力实现，也不涉及其他字段、页面样式和交互行为。

## 验证结果

- 本地已核对最终英文逐字一致、10 个语言版本的语法与字典读取正常，以及其他字典字段未被改动；`git diff --check` 通过。
- 最新代码提交 `526aa2aae` 的 CI 前端代码规范／类型检查、测试、构建及 CodeQL 检查均已通过。
- 独立工作目录未安装前端依赖，本地未运行完整前端检查或浏览器视觉验收；完整前端检查由 CI 完成。
```

### PR Body

## 改动概述

更新官网首页 ZooData 卡片的产品说明，并将全部 10 个语言版本统一到最终英文文案。调整集中在产品定位、Token 节省表述、付费口径和数据覆盖范围。

- **Token 节省表述**：将“约减少 75%”调整为“最多减少 75% 的 LLM Token”。
- **付费口径**：将“仅为使用的字段付费”调整为“仅为使用的数据付费”。
- **数据覆盖与定位**：将 Amazon / TikTok 的预分析商业情报描述，调整为电商、金融、外卖和社交平台的实时结构化数据描述；移除本段中的竞品、市场、流量、消费者分析及 API / CLI / MCP 附带能力表述。
- **多语言一致性**：以最终英文为基准，更新中文、日语、韩语、德语、法语、西班牙语、意大利语、葡萄牙语和阿拉伯语译文。英文使用正确的主谓形式“ZooData turns”；该语法修正不改变其他语言译文。
- **页面与翻译联动**：同步首页组件及 10 份语言字典的索引，确保各语言页面能读取对应译文。

## 最终英文文案

> ZooData turns any URL into agent-ready JSON with up to 75% fewer LLM tokens—and pay only for the data you use. Access real-time, structured data across e-commerce, finance, food delivery, and social platforms.

## 影响范围

共修改 11 个文件：1 个首页组件和 10 份语言字典，均限于 ZooData 的这一段说明。此次为产品文案更新，不包含数据接口或后端能力实现，也不涉及其他字段、页面样式和交互行为。

## 验证结果

- 本地已核对最终英文逐字一致、10 个语言版本的语法与字典读取正常，以及其他字典字段未被改动；`git diff --check` 通过。
- 最新代码提交 `526aa2aae` 的 CI 前端代码规范／类型检查、测试、构建及 CodeQL 检查均已通过。
- 独立工作目录未安装前端依赖，本地未运行完整前端检查或浏览器视觉验收；完整前端检查由 CI 完成。


---

## fix(billing): recover Stripe checkout and subscription eligibility (#3873)

- **SHA**: `53dde279e8c5440d1a853e6002a3f7f86549cbb9`
- **作者**: sam-srp
- **日期**: 2026-09-23T04:01:13Z
- **PR**: #3873

### Commit Message

```
fix(billing): recover Stripe checkout and subscription eligibility (#3873)

## Summary
Historical revoked Stripe agreements no longer block a new subscription.
Provider lookup failures return a controlled
`billing.migration_requires_review` response and are reported to Sentry,
rather than producing an unhandled error.

Checkout creation with an explicit idempotency key and eligibility reads
now use the Stripe SDK's built-in retry/backoff policy, with at most two
retries. Requests retain the same parameters and idempotency key;
validation errors are not blindly retried.

Handle `checkout.session.expired` to atomically cancel the exactly
linked unpaid pending order (or a checkout-outcome-unknown review) with
an audit record. Subscription checkout reservations are released only
for that order. Repeated deliveries are safe, concurrent settlement and
same-status session/review changes are protected by status and
expected-field CAS, and paid/granted/unrelated-review orders are not
canceled. Existing active-subscription and Team restrictions remain in
place.

When creation succeeds at Stripe but its response is lost, the expiry
handler can recover the order by metadata order ID and UID. Recovery
requires the exact provider/environment, an uncertain checkout with a
recorded request, and no existing Session ID. The transaction persists
the Session ID together with cancellation and its audit, so delivery
retries can finish lease release safely.

## Root cause
The eligibility gate queried revoked historical subscriptions, and
Stripe lookup errors escaped the order/Checkout paths. Transient
creation failures had no explicit SDK retry budget. Expired Checkout
events were ignored, leaving local orders pending even though on-demand
eligibility queries could recognize their expiration.

A missing resource in the current Stripe account is not proof that a
historical payment failed. This PR does not automatically cancel
missing-resource orders, introduce background reconciliation, or add a
user cancellation UI.

## Test plan
- [x] 143 focused tests across Stripe SDK facade/retries, expiry
handling, adapter dispatch, checkout recovery, billing policy, legacy
eligibility, and catalog availability.
- [x] In-memory HTTP transport exercises the actual Stripe SDK retry
loop: same body/key, two-retry limit, non-retryable validation failures,
and GET retries.
- [x] Expiry regressions: subscription/top-up, repeated deliveries,
owner/environment isolation, settled/granted/manual-review protection,
settlement races, recovery after lease-release failure, and
new-subscription eligibility after cancellation.
- [x] Ruff, formatting, Pyright, and import contracts.

## Rollout
Backend-only; no new environment variables. The audit transaction adds
optional equality predicates for optimistic concurrency. CSFLE
query-contract tests pass; the expanded predicate has not been exercised
through staging’s encrypted client and requires validation before
release. Ensure the relevant Stripe webhook endpoint subscribes to
`checkout.session.expired` when deploying this change (documented in
`docs/setup/stripe.md`). Live webhook configuration and end-to-end
delivery have not been changed/tested in this PR.
```

### PR Body

## Summary
Historical revoked Stripe agreements no longer block a new subscription. Provider lookup failures return a controlled `billing.migration_requires_review` response and are reported to Sentry, rather than producing an unhandled error.

Checkout creation with an explicit idempotency key and eligibility reads now use the Stripe SDK's built-in retry/backoff policy, with at most two retries. Requests retain the same parameters and idempotency key; validation errors are not blindly retried.

Handle `checkout.session.expired` to atomically cancel the exactly linked unpaid pending order (or a checkout-outcome-unknown review) with an audit record. Subscription checkout reservations are released only for that order. Repeated deliveries are safe, concurrent settlement and same-status session/review changes are protected by status and expected-field CAS, and paid/granted/unrelated-review orders are not canceled. Existing active-subscription and Team restrictions remain in place.

When creation succeeds at Stripe but its response is lost, the expiry handler can recover the order by metadata order ID and UID. Recovery requires the exact provider/environment, an uncertain checkout with a recorded request, and no existing Session ID. The transaction persists the Session ID together with cancellation and its audit, so delivery retries can finish lease release safely.

## Root cause
The eligibility gate queried revoked historical subscriptions, and Stripe lookup errors escaped the order/Checkout paths. Transient creation failures had no explicit SDK retry budget. Expired Checkout events were ignored, leaving local orders pending even though on-demand eligibility queries could recognize their expiration.

A missing resource in the current Stripe account is not proof that a historical payment failed. This PR does not automatically cancel missing-resource orders, introduce background reconciliation, or add a user cancellation UI.

## Test plan
- [x] 143 focused tests across Stripe SDK facade/retries, expiry handling, adapter dispatch, checkout recovery, billing policy, legacy eligibility, and catalog availability.
- [x] In-memory HTTP transport exercises the actual Stripe SDK retry loop: same body/key, two-retry limit, non-retryable validation failures, and GET retries.
- [x] Expiry regressions: subscription/top-up, repeated deliveries, owner/environment isolation, settled/granted/manual-review protection, settlement races, recovery after lease-release failure, and new-subscription eligibility after cancellation.
- [x] Ruff, formatting, Pyright, and import contracts.

## Rollout
Backend-only; no new environment variables. The audit transaction adds optional equality predicates for optimistic concurrency. CSFLE query-contract tests pass; the expanded predicate has not been exercised through staging’s encrypted client and requires validation before release. Ensure the relevant Stripe webhook endpoint subscribes to `checkout.session.expired` when deploying this change (documented in `docs/setup/stripe.md`). Live webhook configuration and end-to-end delivery have not been changed/tested in this PR.



---

## fix(agents): prevent session rotation in Build conversations (#3875)

- **SHA**: `b5b781ee13f0f5b19222a86ebdea5f750af936f4`
- **作者**: kaka-srp
- **日期**: 2026-09-23T04:01:39Z
- **PR**: #3875

### Commit Message

```
fix(agents): prevent session rotation in Build conversations (#3875)

## Summary

- Block standalone `/new` commands in Agent Build, with localized
informational guidance instead of a send-failure banner. Preserve drafts
and attachments; normal task chats remain unchanged.
- Validate both the composer and the shared conversation send path,
covering runtime/programmatic sends before optimistic messages or
network requests.
- Also reject `/new` as the first Build prompt, before provisioning an
Agent/session or preparing attachments. The Home launcher and creation
dialog show creation-specific guidance and allow a corrected retry.

Related to
https://github.com/SerendipityOneInc/agent-channel-service/issues/144.

## Root cause

Build retains a canonical development session, but ACS interprets `/new`
as session rotation. Forwarding it from Build can leave the stored
development session and Mattermost thread binding inconsistent. This
change implements the agreed ECAP-side guard without changing ACS or
Engine.

The pre-submission review identified that the first Build prompt
bypassed the conversation hook. The shared creation service now guards
that path before any resource creation or attachment preparation, using
the same command matcher as ongoing Build chats.

## Scope

- Exact standalone matching, including case and surrounding whitespace;
mentions, quoted/code content, and command arguments are not treated as
`/new`.
- Explicit blank creation, normal prompts, and non-Build conversation
behavior remain available.
- No context-reset feature, historical session repair, ACS/Engine
changes, or deployment.
- This is a Web client guard, not a server-side restriction for direct
Mattermost/other clients.

## Test plan

- [x] 380 targeted Vitest tests across 15 files: conversation
guard/runtime sends, composer submission and draft preservation, Agent
creation and retries, Home launcher, and normal session chat
regressions.
- [x] TypeScript check: `bash scripts/verify-web.sh --tsc-only`.
- [x] ESLint on all changed TypeScript files.
- [x] Frontend governance guards: `bash scripts/verify-web.sh
--guards-only`.
- [x] `git diff --check`.
- [ ] Real browser / staging end-to-end smoke (not performed).

Full build and repository-wide checks are delegated to CI.
```

### PR Body

## Summary

- Block standalone `/new` commands in Agent Build, with localized informational guidance instead of a send-failure banner. Preserve drafts and attachments; normal task chats remain unchanged.
- Validate both the composer and the shared conversation send path, covering runtime/programmatic sends before optimistic messages or network requests.
- Also reject `/new` as the first Build prompt, before provisioning an Agent/session or preparing attachments. The Home launcher and creation dialog show creation-specific guidance and allow a corrected retry.

Related to https://github.com/SerendipityOneInc/agent-channel-service/issues/144.

## Root cause

Build retains a canonical development session, but ACS interprets `/new` as session rotation. Forwarding it from Build can leave the stored development session and Mattermost thread binding inconsistent. This change implements the agreed ECAP-side guard without changing ACS or Engine.

The pre-submission review identified that the first Build prompt bypassed the conversation hook. The shared creation service now guards that path before any resource creation or attachment preparation, using the same command matcher as ongoing Build chats.

## Scope

- Exact standalone matching, including case and surrounding whitespace; mentions, quoted/code content, and command arguments are not treated as `/new`.
- Explicit blank creation, normal prompts, and non-Build conversation behavior remain available.
- No context-reset feature, historical session repair, ACS/Engine changes, or deployment.
- This is a Web client guard, not a server-side restriction for direct Mattermost/other clients.

## Test plan

- [x] 380 targeted Vitest tests across 15 files: conversation guard/runtime sends, composer submission and draft preservation, Agent creation and retries, Home launcher, and normal session chat regressions.
- [x] TypeScript check: `bash scripts/verify-web.sh --tsc-only`.
- [x] ESLint on all changed TypeScript files.
- [x] Frontend governance guards: `bash scripts/verify-web.sh --guards-only`.
- [x] `git diff --check`.
- [ ] Real browser / staging end-to-end smoke (not performed).

Full build and repository-wide checks are delegated to CI.


---

## feat(feishu): notify Stripe payment and renewal failures (#3872)

- **SHA**: `605a9eb99865100a6e0f5e11a6ee0ae7e3e3e0ee`
- **作者**: tim-srp
- **日期**: 2026-09-23T03:33:29Z
- **PR**: #3872

### Commit Message

```
feat(feishu): notify Stripe payment and renewal failures (#3872)

## Summary
- Add Stripe-only Feishu notifications for failed top-up/subscription
payments and automatic renewal attempts. Antom and Airwallex are
unchanged.
- Correlate signed failure events with local
provider/environment/identity-checked billing facts. Support legacy and
modern invoice subscription references; deduplicate event replays
without suppressing a new failed attempt.
- Keep all notification-only lookups and rendering in the existing
capped background queue, with a 5-second preparation deadline and the
existing 5-second HTTP deadline. Notification errors never change
billing state or webhook responses.
- Update Stripe setup documentation. Cards explicitly describe an
attempt failure rather than final subscription termination.

## Test plan
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright, and all 8
import contracts passed.
- [x] 183 focused Feishu/Stripe tests passed, including 48 new
async-preparation and Stripe failure cases.
- [x] Independent specification and code-quality reviews passed;
original notification regression tests passed.
- [x] CI backend suite: 12,221 passed, 5 skipped; coverage 89.77% (89.5%
gate).
- [x] Both automated reviewers approved with no correctness findings.
- [ ] GitHub still reports `python-duplication-check` in progress,
although all its steps completed successfully and its parent Code
Quality workflow concluded success. Waiting on final check-state
synchronization; not claiming all PR checks are green yet.
- Local validation limits: the untouched `test_stripe_billing_v2.py`
crashes local Python 3.12.3 even during standalone compilation; that
file is deferred to CI. Coverage-instrumented local collection also
fails in the existing `AppSettings` initialization (`is_instance_of`),
while the same focused tests pass without coverage. No
runtime/dependency or old test changes are bundled.
- No real payments or live Feishu sends were performed.

## Review disposition
- Kept the call-site `notification_boundary()` despite the optional
simplification suggestion. It explicitly protects the payment handler if
the notification entrypoint itself ever raises; a regression test
injects that failure and pins the successful webhook response. No
business changes were needed after review.

## Rollout / limitations
- Backend-only change; no deployment is part of this PR.
- Confirm the Stripe webhook subscribes to
`payment_intent.payment_failed` and `invoice.payment_failed` and
`FEISHU_NOTIFY_WEBHOOK_URL` is configured. This PR does not modify live
Stripe/Vault configuration.
- Delivery is best effort: disabled/full queues and lookup/network
failures may drop alerts; process restarts, multiple workers, and dedup
TTL expiry may produce duplicates. Business processing remains
authoritative and independent.
- No new Mongo query forms, collections, dependencies, or public APIs.
```

### PR Body

## Summary
- Add Stripe-only Feishu notifications for failed top-up/subscription payments and automatic renewal attempts. Antom and Airwallex are unchanged.
- Correlate signed failure events with local provider/environment/identity-checked billing facts. Support legacy and modern invoice subscription references; deduplicate event replays without suppressing a new failed attempt.
- Keep all notification-only lookups and rendering in the existing capped background queue, with a 5-second preparation deadline and the existing 5-second HTTP deadline. Notification errors never change billing state or webhook responses.
- Update Stripe setup documentation. Cards explicitly describe an attempt failure rather than final subscription termination.

## Test plan
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright, and all 8 import contracts passed.
- [x] 183 focused Feishu/Stripe tests passed, including 48 new async-preparation and Stripe failure cases.
- [x] Independent specification and code-quality reviews passed; original notification regression tests passed.
- [x] CI backend suite: 12,221 passed, 5 skipped; coverage 89.77% (89.5% gate).
- [x] Both automated reviewers approved with no correctness findings.
- [ ] GitHub still reports `python-duplication-check` in progress, although all its steps completed successfully and its parent Code Quality workflow concluded success. Waiting on final check-state synchronization; not claiming all PR checks are green yet.
- Local validation limits: the untouched `test_stripe_billing_v2.py` crashes local Python 3.12.3 even during standalone compilation; that file is deferred to CI. Coverage-instrumented local collection also fails in the existing `AppSettings` initialization (`is_instance_of`), while the same focused tests pass without coverage. No runtime/dependency or old test changes are bundled.
- No real payments or live Feishu sends were performed.

## Review disposition
- Kept the call-site `notification_boundary()` despite the optional simplification suggestion. It explicitly protects the payment handler if the notification entrypoint itself ever raises; a regression test injects that failure and pins the successful webhook response. No business changes were needed after review.

## Rollout / limitations
- Backend-only change; no deployment is part of this PR.
- Confirm the Stripe webhook subscribes to `payment_intent.payment_failed` and `invoice.payment_failed` and `FEISHU_NOTIFY_WEBHOOK_URL` is configured. This PR does not modify live Stripe/Vault configuration.
- Delivery is best effort: disabled/full queues and lookup/network failures may drop alerts; process restarts, multiple workers, and dedup TTL expiry may produce duplicates. Business processing remains authoritative and independent.
- No new Mongo query forms, collections, dependencies, or public APIs.


---

## fix(agents): 优化 R6 运行状态提示与外部渠道导航层级 (#3864)

- **SHA**: `2a61d79d433f344e8243211ef87f677fdf570056`
- **作者**: lynn Zhuang
- **日期**: 2026-09-23T03:09:52Z
- **PR**: #3864

### Commit Message

```
fix(agents): 优化 R6 运行状态提示与外部渠道导航层级 (#3864)

## 改动说明

Agent 工具步骤完成后，整轮任务可能仍在继续，原先底部状态会交给工具记录，导致用户看不到持续的运行提示。本次让会话底部保留 Thinking
/ 执行状态，直到明确结束；工具组独立展示步骤完成情况。

- 外部渠道作为 External channels 的子项展示：增加缩进与细灰树线，图标、名称、健康标签同排；图标 16px、名称
12px、行高 32px，健康标签 10px。
- 调浅无最近聊天时的装饰图标。
- 按要求包含 #3860 的全局焦点黑框修复，移除本轮临时焦点覆盖，输入框保持原有浅色圆角边框。
- 修正本地 mock 启动时 Mattermost 地址被 .env.local 覆盖的问题，避免设置可加载但聊天一直等待。
- 增加显式开启的 R6 预览数据：`MOCK_R6_ACTIVITY=true` 下展示持续思考与两个健康渠道；默认 mock
行为不变。该场景用于视觉验收，持续保持运行状态。

- 将撤销与 Save 移到顶部标签栏右侧：Settings / Profile 下显示，文件预览时隐藏，去掉原先单独占用的一行。

- 嵌入式文件预览在窄面板下保持单行工具栏，刷新与更多按钮位于文件名右侧；长文件名自动省略，避免按钮掉到第二行。

## 根因


会话状态文案会在出现工具记录后被隐藏，消息列表也会在末条为工具组时隐藏底部状态。工具完成与整轮完成因此没有独立、连续的视觉表达。渠道原本使用与一级导航接近的尺寸，名称与状态上下堆叠，缺少从属层级。

## 验证

- [x] 前端治理检查、TypeScript、变更文件 ESLint 及提交钩子全量 ESLint 通过。

- [x] 345 项聊天状态、消息渲染、渠道交互及 Builder / Preview / Session
入口测试通过；终态与停止后的隐藏断言保留。
- [x] #3860 的设计系统 token 合约测试 18 项通过。
- [x] 在 Chrome 实际打开本地页面，确认消息加载、完成步骤、Thinking、Stop 与渠道树形布局。
- [x] 用户已逐轮验收渠道尺寸、标签、树线、空状态图标与输入框焦点样式。
- [x] 已合入最新 main，保留其模板与 onboarding 更新。

仅涉及前端及本地预览配置，不需要后端部署。未操作线上 Agent 或外部渠道。

## 审查说明

自动审查未发现阻塞问题。审查提及主 GenClaw 聊天与 Agent 会话的提示策略存在差异；本次按 R6 Agent
工作区范围保留该差异，不扩展主聊天交互。首轮 CI 的 5 条失败均为旧的工具时间线交接断言，已按新行为更新并通过对应 175 项测试，更新后的
CI 已通过（全量前端测试、生产构建、类型检查、Lint、CodeQL 及自动审查均通过）。


## 最新 main 同步

已合入 `6448fc93e`，保留 #3863 预览面板更新及 #3865 依赖安全修复。解决本地 mock 初始化冲突，分别保留
`MOCK_R6_ACTIVITY` 和 `MOCK_AGENT_PREVIEW_DEMO` 配置。合并后 170
项聊天与渠道测试通过，最新提交的全量前端测试、构建、类型检查、Lint、CodeQL 及两份自动审查均已通过。

本轮审查提及 mock 心跳可能无限追加消息；已核对 `saveMattermostPost` 按固定 ID 覆盖更新，属于误报，无需修改。


## 顶部操作栏验证

设置与标签相关 22 项测试通过，Chrome
本地预览已确认按钮位置并经用户验收；保存、撤销、禁用条件保持不变。本次提交仅移动前端操作区。最新提交 `1cea1858d` 的 CI
全部通过；Codex Review 明确 APPROVE（低风险、无问题），Claude Review 亦为 APPROVE。

文件预览补充：45 项预览与操作相关测试及变更文件 ESLint 通过。

最新 Codex
审查：[APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3864#pullrequestreview-5277055636)。Claude
提及 StatusBadge 内部结构未来变化可能影响子选择器，属于后续组件维护提醒；当前结构与尺寸正确，本次不扩大组件改造范围。
```

### PR Body

## 改动说明

Agent 工具步骤完成后，整轮任务可能仍在继续，原先底部状态会交给工具记录，导致用户看不到持续的运行提示。本次让会话底部保留 Thinking / 执行状态，直到明确结束；工具组独立展示步骤完成情况。

- 外部渠道作为 External channels 的子项展示：增加缩进与细灰树线，图标、名称、健康标签同排；图标 16px、名称 12px、行高 32px，健康标签 10px。
- 调浅无最近聊天时的装饰图标。
- 按要求包含 #3860 的全局焦点黑框修复，移除本轮临时焦点覆盖，输入框保持原有浅色圆角边框。
- 修正本地 mock 启动时 Mattermost 地址被 .env.local 覆盖的问题，避免设置可加载但聊天一直等待。
- 增加显式开启的 R6 预览数据：`MOCK_R6_ACTIVITY=true` 下展示持续思考与两个健康渠道；默认 mock 行为不变。该场景用于视觉验收，持续保持运行状态。

- 将撤销与 Save 移到顶部标签栏右侧：Settings / Profile 下显示，文件预览时隐藏，去掉原先单独占用的一行。

- 嵌入式文件预览在窄面板下保持单行工具栏，刷新与更多按钮位于文件名右侧；长文件名自动省略，避免按钮掉到第二行。

## 根因

会话状态文案会在出现工具记录后被隐藏，消息列表也会在末条为工具组时隐藏底部状态。工具完成与整轮完成因此没有独立、连续的视觉表达。渠道原本使用与一级导航接近的尺寸，名称与状态上下堆叠，缺少从属层级。

## 验证

- [x] 前端治理检查、TypeScript、变更文件 ESLint 及提交钩子全量 ESLint 通过。

- [x] 345 项聊天状态、消息渲染、渠道交互及 Builder / Preview / Session 入口测试通过；终态与停止后的隐藏断言保留。
- [x] #3860 的设计系统 token 合约测试 18 项通过。
- [x] 在 Chrome 实际打开本地页面，确认消息加载、完成步骤、Thinking、Stop 与渠道树形布局。
- [x] 用户已逐轮验收渠道尺寸、标签、树线、空状态图标与输入框焦点样式。
- [x] 已合入最新 main，保留其模板与 onboarding 更新。

仅涉及前端及本地预览配置，不需要后端部署。未操作线上 Agent 或外部渠道。

## 审查说明

自动审查未发现阻塞问题。审查提及主 GenClaw 聊天与 Agent 会话的提示策略存在差异；本次按 R6 Agent 工作区范围保留该差异，不扩展主聊天交互。首轮 CI 的 5 条失败均为旧的工具时间线交接断言，已按新行为更新并通过对应 175 项测试，更新后的 CI 已通过（全量前端测试、生产构建、类型检查、Lint、CodeQL 及自动审查均通过）。


## 最新 main 同步

已合入 `6448fc93e`，保留 #3863 预览面板更新及 #3865 依赖安全修复。解决本地 mock 初始化冲突，分别保留 `MOCK_R6_ACTIVITY` 和 `MOCK_AGENT_PREVIEW_DEMO` 配置。合并后 170 项聊天与渠道测试通过，最新提交的全量前端测试、构建、类型检查、Lint、CodeQL 及两份自动审查均已通过。

本轮审查提及 mock 心跳可能无限追加消息；已核对 `saveMattermostPost` 按固定 ID 覆盖更新，属于误报，无需修改。


## 顶部操作栏验证

设置与标签相关 22 项测试通过，Chrome 本地预览已确认按钮位置并经用户验收；保存、撤销、禁用条件保持不变。本次提交仅移动前端操作区。最新提交 `1cea1858d` 的 CI 全部通过；Codex Review 明确 APPROVE（低风险、无问题），Claude Review 亦为 APPROVE。

文件预览补充：45 项预览与操作相关测试及变更文件 ESLint 通过。

最新 Codex 审查：[APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3864#pullrequestreview-5277055636)。Claude 提及 StatusBadge 内部结构未来变化可能影响子选择器，属于后续组件维护提醒；当前结构与尺寸正确，本次不扩大组件改造范围。


---

## feat(feishu): notify a bot on registration, checkout, purchase and cancellation (#3861)

- **SHA**: `47578245ecd5b4324e1f36c4986e6b07aaddd863`
- **作者**: tim-srp
- **日期**: 2026-09-23T01:53:17Z
- **PR**: #3861

### Commit Message

```
feat(feishu): notify a bot on registration, checkout, purchase and cancellation (#3861)

## 背景与行为

向飞书群机器人发送四类业务卡片：新用户注册、发起购买、Stripe Checkout
购买成功、用户取消订阅。每张卡片标注环境，使用不同颜色；邮箱等业务字段按已确认要求完整展示。通知为尽力发送，失败不得改变业务结果。

## 实现与失败隔离

- 统一 `notify(kind, **payload)` 入口；Pydantic 校验、卡片构造和 HTTP 发送在后台完成。
- 通知专用字段提取、转换和任务调度有异常边界；异常日志只记录类型。注册、建单、支付结算和取消的业务错误仍按原有方式传播。
- 每个进程最多 32 个发送任务；容量满时直接丢弃，不等待、不创建额外排队任务。HTTP 超时为 5 秒，关闭时有界等待。
- `FEISHU_NOTIFY_WEBHOOK_URL` 为空时不发送；原商务咨询 webhook 保持独立。
- 购买消息按事件、provider、uid、订单号独立去重，不能以支付订单的 `SUCCEEDED`
状态推断已经通知。`invoice.paid` 或 `payment_intent.succeeded` 先结算时，后到的 Checkout
仍会尝试通知。
- 去重缓存为进程内最多 2048 个键、1 小时 TTL，仅在成功调度后登记；不增加支付数据库依赖。
- 订阅成功消息要求结算返回权益记录，风控拒绝的试用及其重放不会误报成功。

## 明确取舍

- 跨实例、重启、缓存淘汰或 TTL 到期后可能重复；容量满、发送失败或进程重启可能丢失。无重试队列或事务性 outbox，不承诺严格一次投递。
- 发起购买和取消按次通知，不去重。购买成功仅覆盖 Stripe Checkout，其他支付事件不直接发卡。
- 只部署 backend；Vault 中配置 `FEISHU_NOTIFY_WEBHOOK_URL`，代码可先于配置上线。

## 验证

- 253 条相关单元测试通过，覆盖四个业务落点、通知异常隔离、任务容量及恢复、去重 TTL/容量、支付事件乱序、重复 Checkout
和试用拒绝。
- `bash scripts/verify-local.sh --py-static` 通过：ruff、格式、pyright（0 错误）、8
项导入契约。
- 未调用真实飞书或生产支付服务；运行时投递由部署后的配置决定。


设计文档：`docs/superpowers/specs/2026-09-22-feishu-business-notifications.md`

---------

Co-authored-by: Claude Code <noreply@anthropic.com>
```

### PR Body

## 背景与行为

向飞书群机器人发送四类业务卡片：新用户注册、发起购买、Stripe Checkout 购买成功、用户取消订阅。每张卡片标注环境，使用不同颜色；邮箱等业务字段按已确认要求完整展示。通知为尽力发送，失败不得改变业务结果。

## 实现与失败隔离

- 统一 `notify(kind, **payload)` 入口；Pydantic 校验、卡片构造和 HTTP 发送在后台完成。
- 通知专用字段提取、转换和任务调度有异常边界；异常日志只记录类型。注册、建单、支付结算和取消的业务错误仍按原有方式传播。
- 每个进程最多 32 个发送任务；容量满时直接丢弃，不等待、不创建额外排队任务。HTTP 超时为 5 秒，关闭时有界等待。
- `FEISHU_NOTIFY_WEBHOOK_URL` 为空时不发送；原商务咨询 webhook 保持独立。
- 购买消息按事件、provider、uid、订单号独立去重，不能以支付订单的 `SUCCEEDED` 状态推断已经通知。`invoice.paid` 或 `payment_intent.succeeded` 先结算时，后到的 Checkout 仍会尝试通知。
- 去重缓存为进程内最多 2048 个键、1 小时 TTL，仅在成功调度后登记；不增加支付数据库依赖。
- 订阅成功消息要求结算返回权益记录，风控拒绝的试用及其重放不会误报成功。

## 明确取舍

- 跨实例、重启、缓存淘汰或 TTL 到期后可能重复；容量满、发送失败或进程重启可能丢失。无重试队列或事务性 outbox，不承诺严格一次投递。
- 发起购买和取消按次通知，不去重。购买成功仅覆盖 Stripe Checkout，其他支付事件不直接发卡。
- 只部署 backend；Vault 中配置 `FEISHU_NOTIFY_WEBHOOK_URL`，代码可先于配置上线。

## 验证

- 253 条相关单元测试通过，覆盖四个业务落点、通知异常隔离、任务容量及恢复、去重 TTL/容量、支付事件乱序、重复 Checkout 和试用拒绝。
- `bash scripts/verify-local.sh --py-static` 通过：ruff、格式、pyright（0 错误）、8 项导入契约。
- 未调用真实飞书或生产支付服务；运行时投递由部署后的配置决定。

设计文档：`docs/superpowers/specs/2026-09-22-feishu-business-notifications.md`


---
