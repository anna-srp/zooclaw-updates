# SerendipityOneInc/ecap-workspace — commits 2026-10-19

## feat(chat): 优化模型选择与思考强度交互 (#4083)

- **SHA**: `7d529d27428e029f542f718869c13303066d6c70`
- **作者**: lynn Zhuang
- **日期**: 2026-10-19T11:40:35Z
- **PR**: #4083

### Commit Message

```
feat(chat): 优化模型选择与思考强度交互 (#4083)

## 改动说明

关联 #4079。将输入框中的模型选择改为两层面板：选择并保存模型后进入思考强度面板，可以返回切换模型。

- 使用设计系统 Slider 提供 Low、Medium、High、Max 四个节点；拖动时预览，松开后保存，兼容模型支持的档位、Auto
和已有 Off 配置，保存失败时恢复原值。
- 思考强度居中显示在模型名称上方，使用品牌紫色；选择强度时，下方按钮显示“选择模型”。移除原先的 Follow Agent、Model
default 和滑块底部标签。
- Max 使用紫绿渐变、向左流动的光效和控制点左侧的疏密粒子；刚进入 Max 时触发一次自然发散，白色控制点悬停放大，并适配减少动态效果设置。
- 模型列表固定搜索框和底部 Show more / Show less 按钮，每次展开 5 个模型；使用设计系统细滚动条，搜索时保持面板高度。
- 模型与思考强度面板之间增加淡入淡出、位移和尺寸过渡，改善切换闪烁。

## 验证

- 应用层 8 组相关单元测试：211 个通过，包含 CI 首轮失败的 3 组用例。
- chat-ui 模型选择相关测试：39 个通过。
- 设计系统 Slider 和 token 合约测试：24 个通过。
- 应用层治理检查、TypeScript、ESLint，以及两个共享包的 TypeScript 和相关 ESLint 检查通过。
- 浏览器验证：拖动松开后仅保存一次、搜索 0/1/多条结果高度稳定、面板切换过渡、控制点 hover、Max 单次发散及减少动态效果设置。
- 已更新至最新 main；仅涉及前端及共享 UI 包，无需后端部署。

## 设计意图与审查处理

- 按已确认的交互要求，输入框内不再提供 Follow Agent / Model default 操作；这是有意的产品调整。底层继承能力及
Agent 设置中的独立思考强度控件仍保留。
- 修复 Codex 指出的旧 Off 值可访问性问题：始终渲染可聚焦的语义滑块，读出真实 Off
状态；只有用户通过键盘或点击、拖动主动选择时才写入新值。
- 首轮 CI 的 16 个失败用例来自 3 组共享菜单测试缺少 jsdom ResizeObserver
初始化；已在统一测试环境补齐，并通过相关回归测试。



## 10 月 19 日补充修复

- 修复人工审查指出的 Off → High/Max → Low 拖拽后未保存问题：松开时依据已保存值判断是否需要提交，避免预览值遮蔽旧 Off
状态。
- 新增经过真实设计系统 Slider / Radix 的 pointerdown → pointermove → 返回起点 →
pointerup 回归，验证松开前不写入、松开后只保存一次；覆盖保存失败恢复 Off，以及已保存 Low 时不重复提交。
- 本次 4 组相关应用测试共 106 个通过（包含 20 个思考强度测试）；已合入最新 main。
```

### PR Body

## 改动说明

关联 #4079。将输入框中的模型选择改为两层面板：选择并保存模型后进入思考强度面板，可以返回切换模型。

- 使用设计系统 Slider 提供 Low、Medium、High、Max 四个节点；拖动时预览，松开后保存，兼容模型支持的档位、Auto 和已有 Off 配置，保存失败时恢复原值。
- 思考强度居中显示在模型名称上方，使用品牌紫色；选择强度时，下方按钮显示“选择模型”。移除原先的 Follow Agent、Model default 和滑块底部标签。
- Max 使用紫绿渐变、向左流动的光效和控制点左侧的疏密粒子；刚进入 Max 时触发一次自然发散，白色控制点悬停放大，并适配减少动态效果设置。
- 模型列表固定搜索框和底部 Show more / Show less 按钮，每次展开 5 个模型；使用设计系统细滚动条，搜索时保持面板高度。
- 模型与思考强度面板之间增加淡入淡出、位移和尺寸过渡，改善切换闪烁。

## 验证

- 应用层 8 组相关单元测试：211 个通过，包含 CI 首轮失败的 3 组用例。
- chat-ui 模型选择相关测试：39 个通过。
- 设计系统 Slider 和 token 合约测试：24 个通过。
- 应用层治理检查、TypeScript、ESLint，以及两个共享包的 TypeScript 和相关 ESLint 检查通过。
- 浏览器验证：拖动松开后仅保存一次、搜索 0/1/多条结果高度稳定、面板切换过渡、控制点 hover、Max 单次发散及减少动态效果设置。
- 已更新至最新 main；仅涉及前端及共享 UI 包，无需后端部署。

## 设计意图与审查处理

- 按已确认的交互要求，输入框内不再提供 Follow Agent / Model default 操作；这是有意的产品调整。底层继承能力及 Agent 设置中的独立思考强度控件仍保留。
- 修复 Codex 指出的旧 Off 值可访问性问题：始终渲染可聚焦的语义滑块，读出真实 Off 状态；只有用户通过键盘或点击、拖动主动选择时才写入新值。
- 首轮 CI 的 16 个失败用例来自 3 组共享菜单测试缺少 jsdom ResizeObserver 初始化；已在统一测试环境补齐，并通过相关回归测试。



## 10 月 19 日补充修复

- 修复人工审查指出的 Off → High/Max → Low 拖拽后未保存问题：松开时依据已保存值判断是否需要提交，避免预览值遮蔽旧 Off 状态。
- 新增经过真实设计系统 Slider / Radix 的 pointerdown → pointermove → 返回起点 → pointerup 回归，验证松开前不写入、松开后只保存一次；覆盖保存失败恢复 Off，以及已保存 Low 时不重复提交。
- 本次 4 组相关应用测试共 106 个通过（包含 20 个思考强度测试）；已合入最新 main。


---

## fix(platform): 统一空状态插画、布局规范与交互 (#4089)

- **SHA**: `5fc5a2159f4fa4b2d454e9e3d4359b3255bf5bcc`
- **作者**: lynn Zhuang
- **日期**: 2026-10-19T11:28:45Z
- **PR**: #4089

### Commit Message

```
fix(platform): 统一空状态插画、布局规范与交互 (#4089)

## 改动说明
Platform 的 API keys、Webhooks、Usage、付款历史和不可用页面此前使用小图标空状态，与 ZooWork
的插画风格和排版不一致。本次统一调用共享 PluginEmptyState，以实际 Platform
页面验收，补齐插画素材与尺寸、文字、操作间距规范。

- 新增凭据、连接、记录、功能不可用四张插画；筛选无结果和404复用已有插画。源图、生成提示词和语义映射一同入库。
- 共享组件增加 section
布局和标题级别；占位小屏192×144px、桌面224×168px，插画/标题/描述/操作之间为16/8/24px。原 ZooWork page
默认布局保持兼容。
- 投递历史区分“尚无记录”和“筛选无结果”，后者可清除全部已应用筛选并恢复列表，焦点回到持续存在的 Clear 筛选控件。
- 修复本轮验收发现的原有焦点问题：取消 API key 创建弹窗后返回实际触发按钮，表单转入密钥弹窗时不抢走焦点。

共享组件、四张插画和规范已同步至 [Design System PR
#8](https://github.com/SerendipityOneInc/Zoowork-design-system/pull/8)，提交
`0bd31ac`。此 PR 是已合并
[#4084](https://github.com/SerendipityOneInc/ecap-workspace/pull/4084)
的独立后续优化，不改接口、权限或支付逻辑。

## 分批提交
- `b3b0f0f88`：共享插画、组件 API、目录与规范。
- `c9466d596`：Platform 页面接入、筛选和创建弹窗焦点修复。
- `6eaf3ffee`：清除空结果筛选后的键盘焦点回归修复。

## 验证
- Platform lint、typecheck、生产 build 通过；全量300项测试通过，焦点修复后 router
100项（含新增2项）和 Webhooks 26项通过。
- 本仓共享 DS tsc、lint、空状态组件测试通过。
- 真实 Chrome：7种页面 × 桌面/375px ×
浅/深色，共28组新版检查；另有7组旧版截图。所有新版插画成功加载、占位与16/8/24px间距一致，无横向溢出。
- API key/Webhook 空状态入口打开弹窗、Esc关闭、焦点恢复；投递筛选清除回列表并保留焦点；404返回入口均通过。
- 独立DS仓全量构建、类型、lint、组件/Chat
UI/预览测试及发布脚本测试通过；pack和独立Vite/Next消费者验证通过，四张资产均进入包。


本地预览：`http://127.0.0.1:4180/__preview/settings/api-keys?scenario=empty`。截图与对比HTML保存在本地Obsidian，未向生产环境发布。

CI（最新 `6eaf3ffee`）：全部适用检查通过，包括 Platform quality、Web
lint/typecheck/test/build、Admin/Dashboard、CodeQL；两轮自动评审未发现需要修复的问题。两个PR均未合并。


## 验收修复：长表单弹窗滚动

Create/Edit webhook 原来让整窗和事件列表分别滚动，短窗口中底部按钮会被裁切并随滚动上移。现在直接调用共享
`DialogContent scrollable` /
`DialogBody`：仅正文滚动，标题、关闭入口和操作区固定；默认短弹窗保持兼容。通过原生 form ID 关联底部提交按钮，保留
Enter、pending 和 secret 面板衔接；校验/服务端错误聚焦到可见正文。

独立提交：`ac7211fde`。共享组件、规范和真实目录回归同步至 Design System PR #8（`2b55bc2`）。

本轮验证：Platform 306 项测试、lint、类型检查/构建；Chrome
1440×760、1280×600、375×667、844×390 的实际滚动头尾坐标、最后事件选择、无溢出、浅深色、打开后
resize、校验聚焦、Enter 创建、secret 衔接、编辑保存、Esc/焦点返回均通过。远端 CI 以最新提交检查为准。
```

### PR Body

## 改动说明
Platform 的 API keys、Webhooks、Usage、付款历史和不可用页面此前使用小图标空状态，与 ZooWork 的插画风格和排版不一致。本次统一调用共享 PluginEmptyState，以实际 Platform 页面验收，补齐插画素材与尺寸、文字、操作间距规范。

- 新增凭据、连接、记录、功能不可用四张插画；筛选无结果和404复用已有插画。源图、生成提示词和语义映射一同入库。
- 共享组件增加 section 布局和标题级别；占位小屏192×144px、桌面224×168px，插画/标题/描述/操作之间为16/8/24px。原 ZooWork page 默认布局保持兼容。
- 投递历史区分“尚无记录”和“筛选无结果”，后者可清除全部已应用筛选并恢复列表，焦点回到持续存在的 Clear 筛选控件。
- 修复本轮验收发现的原有焦点问题：取消 API key 创建弹窗后返回实际触发按钮，表单转入密钥弹窗时不抢走焦点。

共享组件、四张插画和规范已同步至 [Design System PR #8](https://github.com/SerendipityOneInc/Zoowork-design-system/pull/8)，提交 `0bd31ac`。此 PR 是已合并 [#4084](https://github.com/SerendipityOneInc/ecap-workspace/pull/4084) 的独立后续优化，不改接口、权限或支付逻辑。

## 分批提交
- `b3b0f0f88`：共享插画、组件 API、目录与规范。
- `c9466d596`：Platform 页面接入、筛选和创建弹窗焦点修复。
- `6eaf3ffee`：清除空结果筛选后的键盘焦点回归修复。

## 验证
- Platform lint、typecheck、生产 build 通过；全量300项测试通过，焦点修复后 router 100项（含新增2项）和 Webhooks 26项通过。
- 本仓共享 DS tsc、lint、空状态组件测试通过。
- 真实 Chrome：7种页面 × 桌面/375px × 浅/深色，共28组新版检查；另有7组旧版截图。所有新版插画成功加载、占位与16/8/24px间距一致，无横向溢出。
- API key/Webhook 空状态入口打开弹窗、Esc关闭、焦点恢复；投递筛选清除回列表并保留焦点；404返回入口均通过。
- 独立DS仓全量构建、类型、lint、组件/Chat UI/预览测试及发布脚本测试通过；pack和独立Vite/Next消费者验证通过，四张资产均进入包。

本地预览：`http://127.0.0.1:4180/__preview/settings/api-keys?scenario=empty`。截图与对比HTML保存在本地Obsidian，未向生产环境发布。

CI（最新 `6eaf3ffee`）：全部适用检查通过，包括 Platform quality、Web lint/typecheck/test/build、Admin/Dashboard、CodeQL；两轮自动评审未发现需要修复的问题。两个PR均未合并。


## 验收修复：长表单弹窗滚动

Create/Edit webhook 原来让整窗和事件列表分别滚动，短窗口中底部按钮会被裁切并随滚动上移。现在直接调用共享 `DialogContent scrollable` / `DialogBody`：仅正文滚动，标题、关闭入口和操作区固定；默认短弹窗保持兼容。通过原生 form ID 关联底部提交按钮，保留 Enter、pending 和 secret 面板衔接；校验/服务端错误聚焦到可见正文。

独立提交：`ac7211fde`。共享组件、规范和真实目录回归同步至 Design System PR #8（`2b55bc2`）。

本轮验证：Platform 306 项测试、lint、类型检查/构建；Chrome 1440×760、1280×600、375×667、844×390 的实际滚动头尾坐标、最后事件选择、无溢出、浅深色、打开后 resize、校验聚焦、Enter 创建、secret 衔接、编辑保存、Esc/焦点返回均通过。远端 CI 以最新提交检查为准。


---

## test(e2e): migrate text and image judges to Jev (#4086)

- **SHA**: `eff57e696a06dcd4c63ddc5deaa86506e56cefdd`
- **作者**: rayhuang198212
- **日期**: 2026-10-19T10:47:51Z
- **PR**: #4086

### Commit Message

```
test(e2e): migrate text and image judges to Jev (#4086)

## Summary
- Replace LiteLLM with Jev through OpenRouter for text,
conversation-title, and image evaluation, keeping the implementation in
llm-judge.ts.
- Use OpenRouter Decisions API with typesafe/jev-1.14 and
OPENROUTER_API_KEY. Images are sent as normalized PNG image_url parts in
JSON.
- Handle cookie consent banners that block chat input.
- Set the basic-usage video response budget to 360 seconds, with an
outer Playwright timeout that includes initialization and Judge
headroom.

## Validation
- Basic usage E2E against staging: 7/7 passed, including authentication
setup and real OpenRouter text/image judgments.
- Judge unit tests: 44 passed.
- TypeScript, ESLint, and CI lint checks passed.

## Configuration
- Configure OPENROUTER_API_KEY for the e2e-staging and e2e-production
GitHub Environments.
- For local runs, set OPENROUTER_API_KEY in web/app/.env.staging.local.
- TypeSafe credentials are no longer used. There is no provider
fallback.
```

### PR Body

## Summary
- Replace LiteLLM with Jev through OpenRouter for text, conversation-title, and image evaluation, keeping the implementation in llm-judge.ts.
- Use OpenRouter Decisions API with typesafe/jev-1.14 and OPENROUTER_API_KEY. Images are sent as normalized PNG image_url parts in JSON.
- Handle cookie consent banners that block chat input.
- Set the basic-usage video response budget to 360 seconds, with an outer Playwright timeout that includes initialization and Judge headroom.

## Validation
- Basic usage E2E against staging: 7/7 passed, including authentication setup and real OpenRouter text/image judgments.
- Judge unit tests: 44 passed.
- TypeScript, ESLint, and CI lint checks passed.

## Configuration
- Configure OPENROUTER_API_KEY for the e2e-staging and e2e-production GitHub Environments.
- For local runs, set OPENROUTER_API_KEY in web/app/.env.staging.local.
- TypeSafe credentials are no longer used. There is no provider fallback.

---

## fix(web): 将登录后的 Cookie 入口统一到设置页 (#4090)

- **SHA**: `7bec112fbd0adff3a257c59db0d022b5d78f3e73`
- **作者**: shana-srp
- **日期**: 2026-10-19T09:25:35Z
- **PR**: #4090

### Commit Message

```
fix(web): 将登录后的 Cookie 入口统一到设置页 (#4090)

## Summary
- 登录后的工作台侧栏不再常驻 Cookie 设置和隐私退出长链接，统一通过「设置 → 管理 Cookie」访问。
- 接通设置页原有的管理按钮，打开真实 Cookie 偏好弹窗，并在同一区域按现有地区策略提供隐私退出入口。
- 头像菜单的「设置」进入通用设置页 `/profile`，保留头像区域原有的账户身份导航。

## Root cause
Cookie 入口此前直接追加在侧栏用户卡片下方，长文案会换行占据侧栏空间；通用设置页已有的「管理 Cookie」按钮仍为 Coming
soon 占位，头像菜单中的「设置」也指向了账户身份页。

本次收敛入口位置并接通现有功能，不调整 Cookie 授权、地区判断或统计与广告追踪策略。未登录页面及官网的原有入口保持可用。仅涉及 Web
前端。

## Test plan
- [x] 仓库前端治理检查、TypeScript 检查和改动文件 ESLint 通过。
- [x] 5 个相关测试文件，145 条测试通过，覆盖设置入口、菜单导航、登录状态和地区隐私入口。
- [x] 本地浏览器验证：首页侧栏及头像菜单无独立 Cookie 项，菜单「设置」正确进入通用设置页。
- [x] 桌面及移动端验证：打开偏好弹窗、保存选择、关闭后焦点恢复；隐私退出关闭广告许可且保留统计选择。
- [x] GitHub Actions 的适用检查全部通过，包括完整前端测试、前端构建和 CodeQL；Codex 与 Claude
自动审查均通过，未发现需修复问题。

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary
- 登录后的工作台侧栏不再常驻 Cookie 设置和隐私退出长链接，统一通过「设置 → 管理 Cookie」访问。
- 接通设置页原有的管理按钮，打开真实 Cookie 偏好弹窗，并在同一区域按现有地区策略提供隐私退出入口。
- 头像菜单的「设置」进入通用设置页 `/profile`，保留头像区域原有的账户身份导航。

## Root cause
Cookie 入口此前直接追加在侧栏用户卡片下方，长文案会换行占据侧栏空间；通用设置页已有的「管理 Cookie」按钮仍为 Coming soon 占位，头像菜单中的「设置」也指向了账户身份页。

本次收敛入口位置并接通现有功能，不调整 Cookie 授权、地区判断或统计与广告追踪策略。未登录页面及官网的原有入口保持可用。仅涉及 Web 前端。

## Test plan
- [x] 仓库前端治理检查、TypeScript 检查和改动文件 ESLint 通过。
- [x] 5 个相关测试文件，145 条测试通过，覆盖设置入口、菜单导航、登录状态和地区隐私入口。
- [x] 本地浏览器验证：首页侧栏及头像菜单无独立 Cookie 项，菜单「设置」正确进入通用设置页。
- [x] 桌面及移动端验证：打开偏好弹窗、保存选择、关闭后焦点恢复；隐私退出关闭广告许可且保留统计选择。
- [x] GitHub Actions 的适用检查全部通过，包括完整前端测试、前端构建和 CodeQL；Codex 与 Claude 自动审查均通过，未发现需修复问题。


---

## fix(e2e): clean up created Agents when setup fails (#4085)

- **SHA**: `006ced8b274501a71820725d5e063aa39dce3f1a`
- **作者**: kaka-srp
- **日期**: 2026-10-19T07:24:23Z
- **PR**: #4085

### Commit Message

```
fix(e2e): clean up created Agents when setup fails (#4085)

## Summary
Production E2E created real Agents and left them enabled when setup
timed out waiting for the Build route. The incident investigation
attributed 598 of 637 new Mattermost channels in the sampled window to
that test account.

Record each successful creation response before navigation completes.
Context teardown calls the standard owner-scoped deletion endpoint; a
credential-free run/origin/UID ledger lets the final CI step compensate
for terminated workers. CI stops after five test failures and attempts
compensation before uploading artifacts.

## Root cause
The worker fixture assigned workspaceId only after navigation succeeded,
so a setup timeout skipped its finally deletion. The new registration
follows the creation response and covers shared worker, default page and
explicit browser contexts. The listener stays attached while cleanup
drains pending captures and resource IDs, so successful creation
responses arriving during another deletion are handled too. Each ID
leaves the in-memory queue before its deletion attempt, preventing
in-process retries from looping on a failed deletion. Ledger validation
completes before any compensation deletion, and cleanup failures remain
visible while other recorded IDs are attempted.

## Test plan
- [x] Independent Astra review and targeted re-review: the late-response
cleanup defect is fixed, with no remaining findings.
- [x] Ten focused unit cases and three Chromium HTTP regressions cover
capture before failed navigation, a successful creation arriving during
teardown, duplicate deletion, partial failure and scope mismatch
rejection. The new late-capture regression failed on the prior helper
and passes after the fix.
- [x] Real authorized-account local integration through Next BFF, ECAP,
Engine and ACS, with staging authentication, MongoDB CSFLE, Billing and
Mattermost: Agent creation 201 and conversation 200, followed by an
intentionally aborted navigation; context cleanup retires the Agent.
- [x] Real SIGKILL of the Playwright worker after ledger persistence:
independent reads first confirm the Agent running and one active ACS
channel; the actual compensation CLI exits 0 and retires it.
- [x] Independent persisted/provider checks: all 6 resources created
during setup and the two final scenarios are uninstalled,
integration_cleanup completed and Engine stopped. Both newly provisioned
bots have no active tokens or team seat; their ACS channels are disabled
and soft-deleted. The 5 pre-existing active local Mattermost channels
remain.
- [x] Frontend governance/type/lint and the standalone cleanup CLI are
checked locally; full product E2E/LLM conversations are outside this
validation.

Design and local validation:
`docs/superpowers/specs/2026-10-19-metrics-pipeline-root-cause-fixes.md`.
The existing shared zooclaw-dev lane and databases were reused, then
returned to the other session. No login or provider tokens are written
to the ledger or committed.

ACS retention fix:
https://github.com/SerendipityOneInc/agent-channel-service/pull/171.
Capacity mitigation ACS #170 is already merged. Historical production
resources are outside the new ledger and remain untouched; creation
without a usable success response and the underlying Build
initialization issue remain outside this bounded cleanup fix. This PR is
not a production release.
```

### PR Body

## Summary
Production E2E created real Agents and left them enabled when setup timed out waiting for the Build route. The incident investigation attributed 598 of 637 new Mattermost channels in the sampled window to that test account.

Record each successful creation response before navigation completes. Context teardown calls the standard owner-scoped deletion endpoint; a credential-free run/origin/UID ledger lets the final CI step compensate for terminated workers. CI stops after five test failures and attempts compensation before uploading artifacts.

## Root cause
The worker fixture assigned workspaceId only after navigation succeeded, so a setup timeout skipped its finally deletion. The new registration follows the creation response and covers shared worker, default page and explicit browser contexts. The listener stays attached while cleanup drains pending captures and resource IDs, so successful creation responses arriving during another deletion are handled too. Each ID leaves the in-memory queue before its deletion attempt, preventing in-process retries from looping on a failed deletion. Ledger validation completes before any compensation deletion, and cleanup failures remain visible while other recorded IDs are attempted.

## Test plan
- [x] Independent Astra review and targeted re-review: the late-response cleanup defect is fixed, with no remaining findings.
- [x] Ten focused unit cases and three Chromium HTTP regressions cover capture before failed navigation, a successful creation arriving during teardown, duplicate deletion, partial failure and scope mismatch rejection. The new late-capture regression failed on the prior helper and passes after the fix.
- [x] Real authorized-account local integration through Next BFF, ECAP, Engine and ACS, with staging authentication, MongoDB CSFLE, Billing and Mattermost: Agent creation 201 and conversation 200, followed by an intentionally aborted navigation; context cleanup retires the Agent.
- [x] Real SIGKILL of the Playwright worker after ledger persistence: independent reads first confirm the Agent running and one active ACS channel; the actual compensation CLI exits 0 and retires it.
- [x] Independent persisted/provider checks: all 6 resources created during setup and the two final scenarios are uninstalled, integration_cleanup completed and Engine stopped. Both newly provisioned bots have no active tokens or team seat; their ACS channels are disabled and soft-deleted. The 5 pre-existing active local Mattermost channels remain.
- [x] Frontend governance/type/lint and the standalone cleanup CLI are checked locally; full product E2E/LLM conversations are outside this validation.

Design and local validation: `docs/superpowers/specs/2026-10-19-metrics-pipeline-root-cause-fixes.md`. The existing shared zooclaw-dev lane and databases were reused, then returned to the other session. No login or provider tokens are written to the ledger or committed.

ACS retention fix: https://github.com/SerendipityOneInc/agent-channel-service/pull/171. Capacity mitigation ACS #170 is already merged. Historical production resources are outside the new ledger and remain untouched; creation without a usable success response and the underlying Build initialization issue remain outside this bounded cleanup fix. This PR is not a production release.


---

## feat(platform): 统一 ZooWork 设计系统并优化全站布局与交互 (#4084)

- **SHA**: `429f3585ca7b375210e8c579cdcbc1cc80980a15`
- **作者**: lynn Zhuang
- **日期**: 2026-10-19T04:14:58Z
- **PR**: #4084

### Commit Message

```
feat(platform): 统一 ZooWork 设计系统并优化全站布局与交互 (#4084)

## 改动摘要

将 Platform 从各页独立的样式与布局，统一为直接使用 ZooWork Design System 的组件，并按「导航 → 页面结构 →
操作反馈」整理信息层级。侧边栏与各业务页已经过多轮本地预览验收，最终包含桌面、平板、移动端和深色模式适配。

### 导航与品牌

- 使用指定 Figma Logo / favicon，品牌高亮色统一为 `#288DFF`。
- 主侧栏复用共享导航、Project 切换、Profile 菜单、Credits 和底部分隔线；选中项目显示对勾，创建项目使用描边按钮。
- 桌面侧栏保持展开；移动端使用抽屉，并补全当前路由的焦点行为。
- Settings 二级侧栏移除底部重复的 Profile 入口及其分隔线，保留顶部 Account
导航、页面内退出登录，以及独立的额度提示。

### 页面与交互

- API keys：统一页头、项目范围提示与表格，明确创建校验、撤销对象和处理中状态，保留密钥仅展示一次的行为。
- Projects / Project settings / Organization / Account：统一列表和分区布局、状态标识、详情
Tabs 与外观选择；未接通的 Members / Limits 如实展示不可用状态。
- Usage / Billing：梳理范围筛选、概览、明细和付款记录；保留真实余额、赠送额度与权限逻辑，补全支付处理中对弹窗的保护。
- Webhooks：按配置、密钥、投递记录和删除操作分区，保留创建、编辑、测试、轮换、删除和重试流程。
- 登录、条款、404：统一反馈与基础组件，保留现有法律正文和登录流程。
- 修复短屏菜单裁切、页面滚动、错误恢复焦点与深色 Logo 可读性。
- 自动审查后补正：Settings 侧栏关闭充值提醒时，焦点返回 Billing 导航；主侧栏仍返回 Profile，避免移除二级
Profile 后出现键盘焦点丢失。

### 共享组件与主站兼容

补齐共享的 Project 切换、账号菜单 / Credits、Footer、页头、外观选择及表格可访问性能力。主站同步复用 Footer 与
Credits；合并最新 main 时保留其新增的 Cookie 设置入口。

通用能力已同步提取到独立组件库的 [Design System PR
#8](https://github.com/SerendipityOneInc/Zoowork-design-system/pull/8)。本
PR 使用 monorepo 内的 workspace 包，不依赖该 PR 合并或 npm 发版。

## 提交与验收资料

- 按侧栏、API
keys、账号与项目、Usage、Billing、Webhooks、辅助页、回归修复、验收文档分批提交，保留逐批追溯与回滚边界。
- 设计规范：`web/platform/DESIGN.md`。
- 计划：`docs/superpowers/plans/2026-10-16-platform-full-redesign.md`。
- 截图、交互验证与 HTML 对比报告的复现入口：`web/platform/scripts/README.md`。
- 已将改动清单、组件反向补充记录和 HTML 前后对比报告写入用户的 Obsidian Platform 笔记目录；本地验收截图未提交到
Git。

## 验证

- [x] Platform：297 项单元测试、TypeScript、ESLint 通过。
- [x] Workspace Design System：477 项测试、TypeScript、ESLint 通过。
- [x] 同步最新 main 后，主站账号菜单、侧栏 Footer 与 Cookie 设置相关 94 项测试通过。
- [x] Platform 生产构建通过。
- [x] 16 条浏览器交互流程通过；13 个页面 × 4 种展示模式的改后截图共 52
张，未检测到横向溢出或页面异常，并保留同场景改前截图供对比。
- [x] 针对最新二级侧栏反馈，复验桌面、390px 移动端、深色模式、Account / Billing 导航及返回 Console
后的账号菜单。
- [x] 充值提醒焦点问题先以回归测试复现，再验证修复；相关 98 项路由测试、类型检查和定向 ESLint
通过。[二级侧栏回归测试](https://github.com/SerendipityOneInc/ecap-workspace/blob/296eaf529daf036610ae87089bb9819f4f89f8ac/web/platform/src/app/router.test.tsx#L603)
分别覆盖 Account 与 Billing 路由，直接断言关闭提醒后 Billing 导航链接获得焦点；另保留主侧栏返回 Profile
的断言。

验证基于本地样例数据；没有执行真实支付、生产 API 写入或线上部署。Billing
本次调整为展示与交互反馈，不修改支付后端、金额计算或权限边界。完整仓库检查以本 PR 的 CI 为准。
```

### PR Body

## 改动摘要

将 Platform 从各页独立的样式与布局，统一为直接使用 ZooWork Design System 的组件，并按「导航 → 页面结构 → 操作反馈」整理信息层级。侧边栏与各业务页已经过多轮本地预览验收，最终包含桌面、平板、移动端和深色模式适配。

### 导航与品牌

- 使用指定 Figma Logo / favicon，品牌高亮色统一为 `#288DFF`。
- 主侧栏复用共享导航、Project 切换、Profile 菜单、Credits 和底部分隔线；选中项目显示对勾，创建项目使用描边按钮。
- 桌面侧栏保持展开；移动端使用抽屉，并补全当前路由的焦点行为。
- Settings 二级侧栏移除底部重复的 Profile 入口及其分隔线，保留顶部 Account 导航、页面内退出登录，以及独立的额度提示。

### 页面与交互

- API keys：统一页头、项目范围提示与表格，明确创建校验、撤销对象和处理中状态，保留密钥仅展示一次的行为。
- Projects / Project settings / Organization / Account：统一列表和分区布局、状态标识、详情 Tabs 与外观选择；未接通的 Members / Limits 如实展示不可用状态。
- Usage / Billing：梳理范围筛选、概览、明细和付款记录；保留真实余额、赠送额度与权限逻辑，补全支付处理中对弹窗的保护。
- Webhooks：按配置、密钥、投递记录和删除操作分区，保留创建、编辑、测试、轮换、删除和重试流程。
- 登录、条款、404：统一反馈与基础组件，保留现有法律正文和登录流程。
- 修复短屏菜单裁切、页面滚动、错误恢复焦点与深色 Logo 可读性。
- 自动审查后补正：Settings 侧栏关闭充值提醒时，焦点返回 Billing 导航；主侧栏仍返回 Profile，避免移除二级 Profile 后出现键盘焦点丢失。

### 共享组件与主站兼容

补齐共享的 Project 切换、账号菜单 / Credits、Footer、页头、外观选择及表格可访问性能力。主站同步复用 Footer 与 Credits；合并最新 main 时保留其新增的 Cookie 设置入口。

通用能力已同步提取到独立组件库的 [Design System PR #8](https://github.com/SerendipityOneInc/Zoowork-design-system/pull/8)。本 PR 使用 monorepo 内的 workspace 包，不依赖该 PR 合并或 npm 发版。

## 提交与验收资料

- 按侧栏、API keys、账号与项目、Usage、Billing、Webhooks、辅助页、回归修复、验收文档分批提交，保留逐批追溯与回滚边界。
- 设计规范：`web/platform/DESIGN.md`。
- 计划：`docs/superpowers/plans/2026-10-16-platform-full-redesign.md`。
- 截图、交互验证与 HTML 对比报告的复现入口：`web/platform/scripts/README.md`。
- 已将改动清单、组件反向补充记录和 HTML 前后对比报告写入用户的 Obsidian Platform 笔记目录；本地验收截图未提交到 Git。

## 验证

- [x] Platform：297 项单元测试、TypeScript、ESLint 通过。
- [x] Workspace Design System：477 项测试、TypeScript、ESLint 通过。
- [x] 同步最新 main 后，主站账号菜单、侧栏 Footer 与 Cookie 设置相关 94 项测试通过。
- [x] Platform 生产构建通过。
- [x] 16 条浏览器交互流程通过；13 个页面 × 4 种展示模式的改后截图共 52 张，未检测到横向溢出或页面异常，并保留同场景改前截图供对比。
- [x] 针对最新二级侧栏反馈，复验桌面、390px 移动端、深色模式、Account / Billing 导航及返回 Console 后的账号菜单。
- [x] 充值提醒焦点问题先以回归测试复现，再验证修复；相关 98 项路由测试、类型检查和定向 ESLint 通过。[二级侧栏回归测试](https://github.com/SerendipityOneInc/ecap-workspace/blob/296eaf529daf036610ae87089bb9819f4f89f8ac/web/platform/src/app/router.test.tsx#L603) 分别覆盖 Account 与 Billing 路由，直接断言关闭提醒后 Billing 导航链接获得焦点；另保留主侧栏返回 Profile 的断言。

验证基于本地样例数据；没有执行真实支付、生产 API 写入或线上部署。Billing 本次调整为展示与交互反馈，不修改支付后端、金额计算或权限边界。完整仓库检查以本 PR 的 CI 为准。


---
