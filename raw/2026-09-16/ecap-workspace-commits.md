# SerendipityOneInc/ecap-workspace — commits 2026-09-16

## fix(billing): allow card checkout without account email (#3756)

- **SHA**: `f8ebfc194ca27597dc0aec87adb3916342db6d8f`
- **作者**: tim-srp
- **日期**: 2026-09-16T11:15:21Z
- **PR**: #3756

### Commit Message

```
fix(billing): allow card checkout without account email (#3756)

## Summary
- Allow phone-login accounts to create subscription, trial, upgrade, and
top-up Card checkouts without an account email.
- Prefill Airwallex `customer_data.email` when an email is available;
otherwise omit `customer_data` so hosted checkout can collect it. Do not
send phone numbers.
- Preserve UID validation, order ownership, trial eligibility, and
checkout replay/idempotency behavior.

## Root cause
The route and service required a non-empty authenticated email even
though the existing Airwallex checkout request did not use it.
Phone-login accounts therefore received HTTP 400 before reaching
checkout creation.

Airwallex supports optional email prefill and collects email on the
hosted page when omitted:
https://www.airwallex.com/docs/api/billing/billing_checkouts/api

## Test plan
- [x] 211 targeted tests passed across Card routes, subscription/trial,
upgrade, top-up, Airwallex client, and schemas.
- [x] Cover missing/blank email, email prefill, monthly/yearly trials,
checkout reuse, invalid UID rejection, and outgoing JSON omission.
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright, and all 8
import contracts passed.
- [x] `git diff --check`.
- [ ] Staging smoke test after backend deployment; no live checkout or
payment was created during local validation.

Backend-only change. No frontend deployment required.
```

### PR Body

## Summary
- Allow phone-login accounts to create subscription, trial, upgrade, and top-up Card checkouts without an account email.
- Prefill Airwallex `customer_data.email` when an email is available; otherwise omit `customer_data` so hosted checkout can collect it. Do not send phone numbers.
- Preserve UID validation, order ownership, trial eligibility, and checkout replay/idempotency behavior.

## Root cause
The route and service required a non-empty authenticated email even though the existing Airwallex checkout request did not use it. Phone-login accounts therefore received HTTP 400 before reaching checkout creation.

Airwallex supports optional email prefill and collects email on the hosted page when omitted: https://www.airwallex.com/docs/api/billing/billing_checkouts/api

## Test plan
- [x] 211 targeted tests passed across Card routes, subscription/trial, upgrade, top-up, Airwallex client, and schemas.
- [x] Cover missing/blank email, email prefill, monthly/yearly trials, checkout reuse, invalid UID rejection, and outgoing JSON omission.
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright, and all 8 import contracts passed.
- [x] `git diff --check`.
- [ ] Staging smoke test after backend deployment; no live checkout or payment was created during local validation.

Backend-only change. No frontend deployment required.


---

## fix(agent-builder): 新建 Agent 默认命名为 Untitled Agent (#3753)

- **SHA**: `62dacee8de7cdef8871aa072c4c9c4f9d328fe88`
- **作者**: lynn Zhuang
- **日期**: 2026-09-16T10:03:03Z
- **PR**: #3753

### Commit Message

```
fix(agent-builder): 新建 Agent 默认命名为 Untitled Agent (#3753)

## 修复内容

新建 Agent 统一使用 `Untitled Agent`
作为默认名称。无论创建时是否填写需求，发送第一条消息后都保留该名称，用户可以通过现有入口手动改名。

## 原因

原逻辑会将初始需求或首条消息直接作为名称，导致未命名 Agent
显示整段需求文本。本次仅统一默认值并移除首条消息自动改名逻辑，不新增接口、状态字段或 LLM
调用。初始需求仍正常保存，旧项目与复制项目的名称不变。

## 验证

- [x] Agent Builder 前端测试：80 项通过，覆盖首条消息不触发改名及原有手动改名流程。
- [x] Agent Builder 后端测试：196 项通过，覆盖空白创建与带初始需求创建时的默认名称。
- [x] `git diff --check` 通过。

修改涉及前后端，需要同时发布才能获得完整行为。
```

### PR Body

## 修复内容

新建 Agent 统一使用 `Untitled Agent` 作为默认名称。无论创建时是否填写需求，发送第一条消息后都保留该名称，用户可以通过现有入口手动改名。

## 原因

原逻辑会将初始需求或首条消息直接作为名称，导致未命名 Agent 显示整段需求文本。本次仅统一默认值并移除首条消息自动改名逻辑，不新增接口、状态字段或 LLM 调用。初始需求仍正常保存，旧项目与复制项目的名称不变。

## 验证

- [x] Agent Builder 前端测试：80 项通过，覆盖首条消息不触发改名及原有手动改名流程。
- [x] Agent Builder 后端测试：196 项通过，覆盖空白创建与带初始需求创建时的默认名称。
- [x] `git diff --check` 通过。

修改涉及前后端，需要同时发布才能获得完整行为。


---

## fix(web): 移除全站悬浮反馈入口，避免遮挡页面操作 (#3752)

- **SHA**: `7e504d2b5436a0d9f400fd2d38b344d506584418`
- **作者**: lynn Zhuang
- **日期**: 2026-09-16T08:21:18Z
- **PR**: #3752

### Commit Message

```
fix(web): 移除全站悬浮反馈入口，避免遮挡页面操作 (#3752)

## 修改说明
移除全站右下角的悬浮反馈入口，手机端和桌面端均不再显示，避免遮挡聊天输入框的发送按钮及其他页面操作。

## 实现
- 删除悬浮按钮组件及全局反馈宿主中的挂载和相关状态订阅。
- 保留崩溃反馈弹窗、健康监测和错误上报能力。
- 更新反馈组件测试，验证默认不渲染悬浮入口，以及反馈弹窗与崩溃上报仍能正常工作。

## 验证
- [x] 反馈组件 19 项单元测试通过
- [x] 修改文件的 ESLint 检查通过
- [x] 前端治理检查及 git diff --check 通过
- 未运行全量 TypeScript 检查、完整本地测试套件或浏览器实测；完整构建与检查交由 CI。
```

### PR Body

## 修改说明
移除全站右下角的悬浮反馈入口，手机端和桌面端均不再显示，避免遮挡聊天输入框的发送按钮及其他页面操作。

## 实现
- 删除悬浮按钮组件及全局反馈宿主中的挂载和相关状态订阅。
- 保留崩溃反馈弹窗、健康监测和错误上报能力。
- 更新反馈组件测试，验证默认不渲染悬浮入口，以及反馈弹窗与崩溃上报仍能正常工作。

## 验证
- [x] 反馈组件 19 项单元测试通过
- [x] 修改文件的 ESLint 检查通过
- [x] 前端治理检查及 git diff --check 通过
- 未运行全量 TypeScript 检查、完整本地测试套件或浏览器实测；完整构建与检查交由 CI。


---

## feat(agents): 优化Agent Settings 设置面板 (#3748)

- **SHA**: `95f5c6d669e8940b607ccb48a066491aeb198806`
- **作者**: lynn Zhuang
- **日期**: 2026-09-16T07:59:50Z
- **PR**: #3748

### Commit Message

```
feat(agents): 优化Agent Settings 设置面板 (#3748)

## 变更摘要

Agent 编辑页的设置原先使用弹窗，内容组织、间距与设计稿不一致。本次改为默认展开的右侧面板，按 Figma 拆分 Settings /
Profile 两个 tab，并统一各模块的布局和交互。

- **Settings**：按设计稿调整 Agent Preferences、Skills 与 Danger
zone；统一模块分割线、字号、浅灰色输入区域和按钮尺寸。
- **Profile**：对齐头像与名称、描述、Agent Details 和四个 Quick commands
的布局；显示创建者头像与相对更新时间；保留旧版超出四条命令的显式迁移提示。
- **编辑体验**：切换 tab 保留草稿；设置面板默认展开，展开/收起带过渡；折叠后简介和建议提示与输入框居中对齐。
- **顶部与创建流程**：标题统一为 Edit Agent，编辑历史移入 More 菜单；创建中的 loading
在原有区域覆盖显示，不再撑高弹窗。
- **复用现有入口**：Add skill 与 Skills 页面使用同一个 ZIP 上传弹窗；Instructions 和已有 Skill
的正文通过编辑弹窗修改。

## 设计稿

-
[Settings（789:2094）](https://www.figma.com/design/IgzHI9jcrXpME6PVaZJRJs/zoowork?node-id=789-2094)
-
[Profile（798:3511）](https://www.figma.com/design/IgzHI9jcrXpME6PVaZJRJs/zoowork?node-id=798-3511)

## 能力边界

本次为前端面板和交互调整，没有新增后端能力。ZIP 上传沿用现有页面的预览状态，尚不可提交；Self-update 开关已移除；AI Skill
Editing 显示为不可用。Knowledge Sources 与 Connectors 暂无 Agent
级后端支持，已移除模块和相关请求、弹窗。Tools 因缺少 Agent
级真实调用数据，暂不展示，也不保留占位提示。模型与用户资料使用实际数据，不硬编码设计稿示例。

## 验证

- 提交前全量 ESLint 通过。
- 已同步最新 main，治理检查、TypeScript 和变更文件 ESLint 通过。测试选择器扩展运行了 454 个文件：453
个通过，另一个文件的旧界面断言已更新，定向复跑 3 个用例全部通过。
- 本地浏览器检查 Settings / Profile、设置展开与收起、Instructions 编辑、共享 Skill 上传弹窗、资源模块及
Tools 区块移除。
- 检查 628px 面板及 390px 窄屏布局，无面板横向溢出；Profile 三个模块高度与设计稿对齐。
- 未运行本地生产构建，由 CI 继续验证。

## 部署

仅需前端部署。
```

### PR Body

## 变更摘要

Agent 编辑页的设置原先使用弹窗，内容组织、间距与设计稿不一致。本次改为默认展开的右侧面板，按 Figma 拆分 Settings / Profile 两个 tab，并统一各模块的布局和交互。

- **Settings**：按设计稿调整 Agent Preferences、Skills 与 Danger zone；统一模块分割线、字号、浅灰色输入区域和按钮尺寸。
- **Profile**：对齐头像与名称、描述、Agent Details 和四个 Quick commands 的布局；显示创建者头像与相对更新时间；保留旧版超出四条命令的显式迁移提示。
- **编辑体验**：切换 tab 保留草稿；设置面板默认展开，展开/收起带过渡；折叠后简介和建议提示与输入框居中对齐。
- **顶部与创建流程**：标题统一为 Edit Agent，编辑历史移入 More 菜单；创建中的 loading 在原有区域覆盖显示，不再撑高弹窗。
- **复用现有入口**：Add skill 与 Skills 页面使用同一个 ZIP 上传弹窗；Instructions 和已有 Skill 的正文通过编辑弹窗修改。

## 设计稿

- [Settings（789:2094）](https://www.figma.com/design/IgzHI9jcrXpME6PVaZJRJs/zoowork?node-id=789-2094)
- [Profile（798:3511）](https://www.figma.com/design/IgzHI9jcrXpME6PVaZJRJs/zoowork?node-id=798-3511)

## 能力边界

本次为前端面板和交互调整，没有新增后端能力。ZIP 上传沿用现有页面的预览状态，尚不可提交；Self-update 开关已移除；AI Skill Editing 显示为不可用。Knowledge Sources 与 Connectors 暂无 Agent 级后端支持，已移除模块和相关请求、弹窗。Tools 因缺少 Agent 级真实调用数据，暂不展示，也不保留占位提示。模型与用户资料使用实际数据，不硬编码设计稿示例。

## 验证

- 提交前全量 ESLint 通过。
- 已同步最新 main，治理检查、TypeScript 和变更文件 ESLint 通过。测试选择器扩展运行了 454 个文件：453 个通过，另一个文件的旧界面断言已更新，定向复跑 3 个用例全部通过。
- 本地浏览器检查 Settings / Profile、设置展开与收起、Instructions 编辑、共享 Skill 上传弹窗、资源模块及 Tools 区块移除。
- 检查 628px 面板及 390px 窄屏布局，无面板横向溢出；Profile 三个模块高度与设计稿对齐。
- 未运行本地生产构建，由 CI 继续验证。

## 部署

仅需前端部署。





---

## feat(assets): preview generated files in chat artifact sidebar (#3751)

- **SHA**: `ae21ecf4f4138edfd9174703f5b530f5ece2a69c`
- **作者**: tim-srp
- **日期**: 2026-09-16T07:56:02Z
- **PR**: #3751

### Commit Message

```
feat(assets): preview generated files in chat artifact sidebar (#3751)

## Summary
Clicking AI-generated files in Artifacts previously opened the file URL
in a new tab, often triggering a download. Browse mode now opens the
existing Chat artifact sidebar, with file switching, close, resize,
refresh and download controls.

- Reuse `ArtifactsSidebar` and its existing file renderers; no backend
changes.
- Size the file grid by available container width so multiple cards fit
naturally alongside the preview. On small screens the preview overlays
the list.
- Preserve My uploads and attachment-selector behavior.

## Test plan
- [x] 52 targeted AssetLibraryContent and UploadsFeed tests passed,
including grid/list preview callbacks without a popup, file switching,
close/reopen and tab switching.
- [x] Whole-app TypeScript check passed.
- [x] ESLint for all changed files and frontend governance guards
passed.
- [x] `git diff --check` passed.
- [ ] Browser-level visual validation has not been performed.
```

### PR Body

## Summary
Clicking AI-generated files in Artifacts previously opened the file URL in a new tab, often triggering a download. Browse mode now opens the existing Chat artifact sidebar, with file switching, close, resize, refresh and download controls.

- Reuse `ArtifactsSidebar` and its existing file renderers; no backend changes.
- Size the file grid by available container width so multiple cards fit naturally alongside the preview. On small screens the preview overlays the list.
- Preserve My uploads and attachment-selector behavior.

## Test plan
- [x] 52 targeted AssetLibraryContent and UploadsFeed tests passed, including grid/list preview callbacks without a popup, file switching, close/reopen and tab switching.
- [x] Whole-app TypeScript check passed.
- [x] ESLint for all changed files and frontend governance guards passed.
- [x] `git diff --check` passed.
- [ ] Browser-level visual validation has not been performed.


---

## fix(web): show wrong-account invite error (#3749)

- **SHA**: `8c3ae58942d22901be7bd0f80fb2541b622361fc`
- **作者**: finn-srp
- **日期**: 2026-09-16T07:13:54Z
- **PR**: #3749

### Commit Message

```
fix(web): show wrong-account invite error (#3749)

## Summary

- map the backend `invite_code.email_mismatch` response to the existing
`organizationJoin.errors.wrongAccount` copy
- keep the invited email private while telling the user to sign in with
the address that received the invitation
- cover the error mapper and the unauthenticated OTP-to-join flow

## Testing

- `bash scripts/verify-web.sh
web/app/src/app/[locale]/join/lib/join-state.ts
web/app/tests/unit/app/organization-join-flow.unit.spec.tsx
web/app/tests/unit/app/organization-join-state.unit.spec.ts`
- TypeScript, 7 related Vitest tests, and ESLint passed

Related to #3727 and follow-up to #3746.

Co-authored-by: wangfulong <wfllike@gmail.com>
```

### PR Body

## Summary

- map the backend `invite_code.email_mismatch` response to the existing `organizationJoin.errors.wrongAccount` copy
- keep the invited email private while telling the user to sign in with the address that received the invitation
- cover the error mapper and the unauthenticated OTP-to-join flow

## Testing

- `bash scripts/verify-web.sh web/app/src/app/[locale]/join/lib/join-state.ts web/app/tests/unit/app/organization-join-flow.unit.spec.tsx web/app/tests/unit/app/organization-join-state.unit.spec.ts`
- TypeScript, 7 related Vitest tests, and ESLint passed

Related to #3727 and follow-up to #3746.

---

## feat(web): 完善首页 Agent 入口、卡片滚动与侧边栏体验 (#3736)

- **SHA**: `b5008ae10f570bec6cf3631a73b8b24872e9cd9f`
- **作者**: lynn Zhuang
- **日期**: 2026-09-16T06:21:31Z
- **PR**: #3736

### Commit Message

```
feat(web): 完善首页 Agent 入口、卡片滚动与侧边栏体验 (#3736)

## 改动说明

完善侧边栏与首页 Agent 入口：默认使用 Agent Builder 创建 Agent，也可切换已有 Agent
发起独立任务；保留输入文字、附件及失败重试能力。

- 恢复独立 Home / Agents 导航，补充 Agent 列表空状态与展开、收起入口；仅 Agent
列表区域滚动，Connector、MCP、Skills、Knowledge Base 保持可见。
- 首页两个 Agent 模块各不超过一张卡片时左右排列，否则上下排列；卡片保持单行横向滚动，多卡片时露出下一张卡片，隐藏原生滚动条。
- 左右渐变分别根据实际滚动位置显示：起点不遮挡第一张卡片，末尾不遮挡最后一张卡片；容器尺寸变化后重新判断。
- 放大首页卡片头像，统一默认头像 v4 素材及旧 URL 映射，保留自定义头像。移除会染色图形内部的混色，当前保留原图白底。
- 修复首页概览误用输入框 Engine 筛选结果、遗漏 Computer Agent 活动与计划任务的问题。
- 知识库页面与侧边栏统一使用 Knowledge Base 文案。
- 用户菜单移除 User Guide、Join Discord、Prompt Gallery，增加 Managed Agent API
外链；移除侧边栏 Asleep 状态提示，头像点击统一打开用户菜单。
- 完善本地 mock 数据、创建与会话流程及自定义端口登录配置，支持稳定预览。

## Codex 审查修复

- 修复 Builder 多附件部分失败后重试会重复上传的问题：仅复用同频道已成功上传的文件 ID，并保持附件状态同步。
- 新增同频道重试和跨频道重传的回归用例，相关 17 项测试通过。

- 清理移除 Discord 菜单后遗留的图标和导出，修复 CI 的未使用代码检查；本地 Knip 对应检查通过。

## 验证

- 本地 mock 预览：http://localhost:3001/new-chat，首页和模拟后端均返回 200。
- 前端治理检查、TypeScript、改动文件 ESLint 通过。测试筛选匹配到 454 个文件：5,981 项通过，1
项头像容器断言失败；修正断言后，该文件 47 项测试全部重跑通过，另有 1 项 todo。
- 同步主线 Tasks 等更新并解决侧边栏冲突后，16 个文件、240 项侧边栏/首页/mock 测试全部通过。
- 原有创建、重试、头像兼容及 mock 登录测试继续保留。

## 发布范围与限制

仅前端发布，无数据库迁移。预览使用模拟数据；真实登录、附件上传仍需 staging
验收。头像轮廓外渐变待透明原始素材补齐，当前版本不对图形内部染色。
```

### PR Body

## 改动说明

完善侧边栏与首页 Agent 入口：默认使用 Agent Builder 创建 Agent，也可切换已有 Agent 发起独立任务；保留输入文字、附件及失败重试能力。

- 恢复独立 Home / Agents 导航，补充 Agent 列表空状态与展开、收起入口；仅 Agent 列表区域滚动，Connector、MCP、Skills、Knowledge Base 保持可见。
- 首页两个 Agent 模块各不超过一张卡片时左右排列，否则上下排列；卡片保持单行横向滚动，多卡片时露出下一张卡片，隐藏原生滚动条。
- 左右渐变分别根据实际滚动位置显示：起点不遮挡第一张卡片，末尾不遮挡最后一张卡片；容器尺寸变化后重新判断。
- 放大首页卡片头像，统一默认头像 v4 素材及旧 URL 映射，保留自定义头像。移除会染色图形内部的混色，当前保留原图白底。
- 修复首页概览误用输入框 Engine 筛选结果、遗漏 Computer Agent 活动与计划任务的问题。
- 知识库页面与侧边栏统一使用 Knowledge Base 文案。
- 用户菜单移除 User Guide、Join Discord、Prompt Gallery，增加 Managed Agent API 外链；移除侧边栏 Asleep 状态提示，头像点击统一打开用户菜单。
- 完善本地 mock 数据、创建与会话流程及自定义端口登录配置，支持稳定预览。

## Codex 审查修复

- 修复 Builder 多附件部分失败后重试会重复上传的问题：仅复用同频道已成功上传的文件 ID，并保持附件状态同步。
- 新增同频道重试和跨频道重传的回归用例，相关 17 项测试通过。

- 清理移除 Discord 菜单后遗留的图标和导出，修复 CI 的未使用代码检查；本地 Knip 对应检查通过。

## 验证

- 本地 mock 预览：http://localhost:3001/new-chat，首页和模拟后端均返回 200。
- 前端治理检查、TypeScript、改动文件 ESLint 通过。测试筛选匹配到 454 个文件：5,981 项通过，1 项头像容器断言失败；修正断言后，该文件 47 项测试全部重跑通过，另有 1 项 todo。
- 同步主线 Tasks 等更新并解决侧边栏冲突后，16 个文件、240 项侧边栏/首页/mock 测试全部通过。
- 原有创建、重试、头像兼容及 mock 登录测试继续保留。

## 发布范围与限制

仅前端发布，无数据库迁移。预览使用模拟数据；真实登录、附件上传仍需 staging 验收。头像轮廓外渐变待透明原始素材补齐，当前版本不对图形内部染色。


---

## fix(agent-development): expose skill authoring guidance and receipts (#3747)

- **SHA**: `411a656a81b0c1e3341442d22115f799f9a3be47`
- **作者**: kaka-srp
- **日期**: 2026-09-16T06:22:51Z
- **PR**: #3747

### Commit Message

```
fix(agent-development): expose skill authoring guidance and receipts (#3747)

## Summary

Build could save a reusable capability entirely in AGENTS.md without
creating an Engine skill. Expose the skill source layout and a valid
instruction-only template even when the source has no skills, then
return effective artifact changes from validate and registered skill
versions from commit.

## Root cause

The existing registration path works, but the authoring contract did not
explain which artifact to create or provide registration feedback. This
change keeps that existing path and adds guidance and content-free
receipts. Persona-only changes remain valid with zero skills; no
existing Agent source is migrated.

The companion Engine PR
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1468 updates
the Build policy and tool descriptions. Deploy claw-interface first,
then Engine. The detailed design and reproducible real-model check are
in docs/superpowers/specs/2026-09-16-build-skill-artifacts-design.md.

## Test plan

- [x] Backend static checks: ruff, formatting, pyright, import-linter.
- [x] Agent Development regression suite: 331 passed, including 7 cases
added after independent agent review for immutable post-commit reads,
exact skill identity/version and cleanup failure handling.
- [x] Independent agent review: three harness findings fixed and
re-reviewed; no remaining findings. Real-model scenarios rerun
successfully with the stricter assertions.
- [x] Real gpt-5.6-terra source-contract check using the exported Engine
policy: created skill v1, retained skills for a tone change, and
upgraded the same capability to v2 with a script. Actual local Engine
registry and eligible bindings were checked; test resources were cleaned
up.
- [ ] Full ordinary-task worker/Temporal/sandbox skill-read path: not
covered by this source-contract harness. Revision/ChangeSet persistence
is in-memory in the harness; no production deployment or source repair
was performed.
```

### PR Body

## Summary

Build could save a reusable capability entirely in AGENTS.md without creating an Engine skill. Expose the skill source layout and a valid instruction-only template even when the source has no skills, then return effective artifact changes from validate and registered skill versions from commit.

## Root cause

The existing registration path works, but the authoring contract did not explain which artifact to create or provide registration feedback. This change keeps that existing path and adds guidance and content-free receipts. Persona-only changes remain valid with zero skills; no existing Agent source is migrated.

The companion Engine PR https://github.com/SerendipityOneInc/zooclaw-engine/pull/1468 updates the Build policy and tool descriptions. Deploy claw-interface first, then Engine. The detailed design and reproducible real-model check are in docs/superpowers/specs/2026-09-16-build-skill-artifacts-design.md.

## Test plan

- [x] Backend static checks: ruff, formatting, pyright, import-linter.
- [x] Agent Development regression suite: 331 passed, including 7 cases added after independent agent review for immutable post-commit reads, exact skill identity/version and cleanup failure handling.
- [x] Independent agent review: three harness findings fixed and re-reviewed; no remaining findings. Real-model scenarios rerun successfully with the stricter assertions.
- [x] Real gpt-5.6-terra source-contract check using the exported Engine policy: created skill v1, retained skills for a tone change, and upgraded the same capability to v2 with a script. Actual local Engine registry and eligible bindings were checked; test resources were cleaned up.
- [ ] Full ordinary-task worker/Temporal/sandbox skill-read path: not covered by this source-contract harness. Revision/ChangeSet persistence is in-memory in the harness; no production deployment or source repair was performed.


---

## fix(organization): replace enterprise admin URL with app frontend (#3746)

- **SHA**: `95da5f1c1ad7b9d398ec183f849775e016924ba0`
- **作者**: finn-srp
- **日期**: 2026-09-16T06:00:59Z
- **PR**: #3746

### Commit Message

```
fix(organization): replace enterprise admin URL with app frontend (#3746)

## Summary

- Build organization invitation links from `APP_FRONTEND_URL` and send
invitees to `/join?orgId=...&code=...` on the main Web app.
- Remove `ENTERPRISE_ADMIN_URL` from claw-interface settings, checkout
redirect allowlists, and the Airwallex vertical-pack capability gate.
- Fail closed when invite email delivery is configured but
`APP_FRONTEND_URL` is missing, and URL-encode invitation query values.
- Add regression coverage for invitation links and for rejecting legacy
Business redirect hosts in both checkout paths.

Refs #3727.

## Root cause

Business organization management moved into the main Web app in #3715,
but claw-interface still preferred the old enterprise-admin base URL for
invitation emails. The same retired setting remained in vertical
checkout capability and redirect-host validation, so runtime behavior
still depended on the Business deployment.

This PR intentionally does not preserve or redirect legacy Business
URLs. The external Vertical Plan CTA and callback URLs are tracked
separately in
[zooclaw-vertical-plan#83](https://github.com/SerendipityOneInc/zooclaw-vertical-plan/issues/83).

## Test plan

- [x] `python -m pytest` for the seven affected unit-test modules: 199
passed.
- [x] `bash scripts/verify-py.sh`: Ruff, Ruff format, Pyright, and
import-linter passed.
- [ ] Deploy claw-interface to staging and confirm
`APP_FRONTEND_URL=https://ecap.gensmo.nosay.live`.
- [ ] Invite an unused test email from staging, verify the email URL
starts with `https://ecap.gensmo.nosay.live/join`, and complete
login/OTP plus organization join.
- [ ] Before production rollout, confirm
`APP_FRONTEND_URL=https://zoowork.ai` and coordinate the Vertical Plan
callback migration tracked in zooclaw-vertical-plan#83.

Co-authored-by: wangfulong <wfllike@gmail.com>
```

### PR Body

## Summary

- Build organization invitation links from `APP_FRONTEND_URL` and send invitees to `/join?orgId=...&code=...` on the main Web app.
- Remove `ENTERPRISE_ADMIN_URL` from claw-interface settings, checkout redirect allowlists, and the Airwallex vertical-pack capability gate.
- Fail closed when invite email delivery is configured but `APP_FRONTEND_URL` is missing, and URL-encode invitation query values.
- Add regression coverage for invitation links and for rejecting legacy Business redirect hosts in both checkout paths.

Refs #3727.

## Root cause

Business organization management moved into the main Web app in #3715, but claw-interface still preferred the old enterprise-admin base URL for invitation emails. The same retired setting remained in vertical checkout capability and redirect-host validation, so runtime behavior still depended on the Business deployment.

This PR intentionally does not preserve or redirect legacy Business URLs. The external Vertical Plan CTA and callback URLs are tracked separately in [zooclaw-vertical-plan#83](https://github.com/SerendipityOneInc/zooclaw-vertical-plan/issues/83).

## Test plan

- [x] `python -m pytest` for the seven affected unit-test modules: 199 passed.
- [x] `bash scripts/verify-py.sh`: Ruff, Ruff format, Pyright, and import-linter passed.
- [ ] Deploy claw-interface to staging and confirm `APP_FRONTEND_URL=https://ecap.gensmo.nosay.live`.
- [ ] Invite an unused test email from staging, verify the email URL starts with `https://ecap.gensmo.nosay.live/join`, and complete login/OTP plus organization join.
- [ ] Before production rollout, confirm `APP_FRONTEND_URL=https://zoowork.ai` and coordinate the Vertical Plan callback migration tracked in zooclaw-vertical-plan#83.


---
