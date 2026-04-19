# ecap-workspace Commits - 2026-04-19
共 25 条 commits

## [0429559b](https://github.com/SerendipityOneInc/ecap-workspace/commit/0429559b22a1ee5c676670898d40e7132cc59449)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T10:28:08Z
- **消息**: test(web): useMattermost reconnect / bot poll / connect 错误分支覆盖 (#1075)

```
## Summary

延续 #1071 merged 的进展，覆盖之前 deferred 的三块源码分支 — **reconnect
scheduling**、**pollBotStatus**、**connect() 错误路径**，不改动产线代码。

### 新增 11 个测试

**reconnect scheduling (5)**
- ws onDisconnect → `scheduleReconnect` → state=`reconnecting`
- intentionalDisconnect 守卫：`disconnect()` 后 ws onDisconnect 不重启
- duplicate timer 守卫：重复 onDisconnect 不重复 scheduleReconnect
- 成功 reconnect → 回到 `connected`、`isReconnectExhausted=false`
- MAX_RECONNECT_ATTEMPTS (5) 耗尽 → `isReconnectExhausted=true` + 错误消息

**pollBotSt
```

## [1695dcdd](https://github.com/SerendipityOneInc/ecap-workspace/commit/1695dcdd9d0aeab9b6b942a3e66da49877646d08)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T09:49:31Z
- **消息**: test(web): useMattermost 补覆盖 reaction/typing/sendMessage/杂项 (#901 Step 7b) (#1071)

```
## Summary

Plan Step 7b——useMattermost hook (839 行) 原 48% 覆盖，~400 行未覆盖。本 PR 针对
reaction events / typing events / sendMessage / loadMoreHistory /
disconnect / autoConnect / clearWaitingForBotReply 这些高 ROI 分支补齐 **23
tests**，推到 **65.6% lines / 68.1% statements**（+20 pp）。

## 23 新 tests / 365 行

| 分组 | tests | 覆盖点 |
|---|---|---|
| reaction events | 8 | reaction_added 追加 / 幂等 / 累积 / reaction_removed
匹配移除 / 单条时删 key / 非匹配 no-op / malformed JSON 吞 / 字段缺失吞 |
| typing events | 4 | bot typing → waiting=
```

## [79ac2db4](https://github.com/SerendipityOneInc/ecap-workspace/commit/79ac2db475084e22e0789b8633df1df6d58ba2ee)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T09:11:53Z
- **消息**: test(web): ChannelsSection 全面覆盖 (#899 Step 5e — 收尾) (#1070)

```
## Summary

Step 5 收尾——Claw Settings 的 \`ChannelsSection\` (869 行) 原先 0 测试。Step 5
最后一块。

子 wizards (Feishu/Telegram/Slack/Discord) 各自独立 spec 已合入；本 PR 将它们 mock 为
stub，聚焦 Section + ChannelCard + StatusBadge + AddChannelModal 的编排 / 渲染 /
状态机。

## 47 tests / 576 行

| 分组 | tests | 覆盖点 |
|---|---|---|
| render gates | 6 | botRunning × redeploying 矩阵 / empty state /
restarting banner / button disabled |
| channel card 渲染 | 4 | platform / account / status / group policy /
emoji fallback |
| StatusBadge |
```

## [2dba8928](https://github.com/SerendipityOneInc/ecap-workspace/commit/2dba8928d8048c9d49d5ae269ad2a45f8f4816d5)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T07:21:43Z
- **消息**: test(web): IntegrationsSection 全面覆盖 (#899 Step 5d) (#1068)

```
## Summary

Step 5 追加——claw-settings \`IntegrationsSection\` (194 行) 原先 0
测试。Third-party OAuth 连接管理 UI：Connected Services 区 + Available
Integrations 区 + toggle / disconnect / connect 交互 + 异步 \`handleConnect\`
流程（window.open popup）。

## 22 tests / 235 行

| 分组 | tests | 覆盖点 |
|---|---|---|
| section 可见性 | 3 | 空状态 / 部分连 / 全连时的 heading 显隐 |
| status badge | 4 | \`connected\`/\`pending\`/\`error\` 各 badge + 未知不渲染
(it.each) |
| 可选字段 | 3 | account_name / error_message / 都空 |
| ConnectedCard 交互 | 6 | di
```

## [da1a18ff](https://github.com/SerendipityOneInc/ecap-workspace/commit/da1a18ff2e050e8d3993964a73479283313e1b96)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T07:01:43Z
- **消息**: chore(web): 收紧 jscpd 阈值 + spec 收尾(web dedup 系列完成) (#1067)

```
## Summary

web 代码重复率系列 13 PR 执行完毕(#1017 基建起,至 #1063 跨 6% 目标)。**最后一步** —— 收紧 jscpd
阈值 + 更新 spec 状态为 done。

## 阈值变更

按 `ceil(obs) + 1.5%` 规则(memory `project_test_dedup_done`,Python dedup
经验沉淀):

| 配置 | 旧阈值 | obs | 新阈值 | buffer |
|------|--------|-----|--------|--------|
| `.jscpd.src.json` | 6% | 3.90% | **5.5%** | 1.6% |
| `.jscpd.tests.json` | 10% | 5.87% | **7.5%** | 1.63% |

阈值下调 **0.5%** 对 src、**2.5%** 对 tests,同时保留 1.6% 缓冲让新代码有生长空间,突破前触发 CI gate
预警。

## 系列最终成果

| 范围 | Before | After | 变化 |
|
```

## [c7b0f59e](https://github.com/SerendipityOneInc/ecap-workspace/commit/c7b0f59e6b8928c175f83b73cb9f433df73c558c)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T06:54:55Z
- **消息**: test(web): SlackSetupWizard 全面覆盖 (#899 Step 5c) (#1065)

```
## Summary

Step 5 三件套收尾——Claw Settings Slack setup wizard (428 行) 原先 0 测试。接 #1047
Feishu / #1056 Telegram 之后第三个 wizard。

吸收前两个 PR 的 review 教训，spec 一次到位：
- **jest-dom matchers** (`toBeInTheDocument` / `toBeDisabled` /
`not.toBeInTheDocument`)
- **强断言**（验 API payload 精确）
- **无 `.not.toThrow()` 噪音 / 无冗余 waitFor**
- **前瞻处理 unhandled rejection**（源 `handleCopyManifest` 无 `.catch()`）

## 30 tests / 454 行

| 分组 | tests | 覆盖点 |
|---|---|---|
| welcome | 3 | 渲染 / cancel / getStarted |
| create-app | 6 | 
```

## [891d7007](https://github.com/SerendipityOneInc/ecap-workspace/commit/891d70075bf27c286a87ef21f706331ddc955702)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T06:51:11Z
- **消息**: refactor(web): T2-g useCanvasSession spec 抽 renderSessionAndInit helper(跨 6% 目标) (#1063)

```
## Summary

useCanvasSession spec 17 个 test 重复 6 行 pattern:

```ts
const setMessages = vi.fn()
const { result } = renderHook(() => useCanvasSession({ setMessages }))

await act(async () => {
  await result.current.initializeSession()
})
```

**抽 `renderSessionAndInit()` helper** 返回 `{ setMessages, result
}`;`replace_all` 一次吃 16+ 处 identical block。

**刻意保留** 1 处 `'should return expected shape'` test — 它不走
`initializeSession`,pattern 不匹配,inline 最清晰。

## 重复率变化 🎯

- **tests: 6.13% → 5.87%**(253 → 24
```

## [4f52af7b](https://github.com/SerendipityOneInc/ecap-workspace/commit/4f52af7b22525cb9607fd5949ea0324c7b886ca6)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T06:42:14Z
- **消息**: test(web): TelegramSetupWizard 全面覆盖 (#899 Step 5b) (#1056)

```
## Summary

Coverage 推进 plan Step 5b——Claw Settings Telegram setup wizard (336 行) 原先
0 测试。接 #1047 FeishuSetupModal 之后的同 wizard 主题。

吸收 PR #1047 多轮 review 教训，spec 一次到位：
- **jest-dom matchers** (`toBeInTheDocument` / `not.toBeInTheDocument`) 
- **强断言**（验 API 被调用 + payload）
- **无 `.not.toThrow()` 噪音** / **无多余 `waitFor`**
- 本组件无 polling / countdown → `waitFor` 仅在 `addClawChannel` Promise
成功/失败后的 DOM 更新用（真 async，合理）

## 24 tests / 328 行

| 分组 | tests | 覆盖点 |
|---|---|---|
| welcome | 3 | 渲染 / cancel 
```

## [dd641f16](https://github.com/SerendipityOneInc/ecap-workspace/commit/dd641f16bfd744dd1c15ef492366ece9628135a6)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T06:31:27Z
- **消息**: chore: add .nvmrc pinning Node to 24 (#1062)

```
## Summary
Add a one-line `.nvmrc` file at the repo root with `24`. Complements
#1061 (tightening `engines.node` to `>=24 <25`) — the `engines` field
*fails* CI/install when the wrong Node is used; `.nvmrc` lets nvm/fnm
*auto-switch* to the right one before that check runs.

## What changes for contributors
- `nvm use` (no arguments, from the repo root) — auto-switches to Node
24.
- `fnm use` — same; fnm reads `.nvmrc`.
- `direnv` users can add `use node` to a `.envrc` and it follows this
file.

```

## [1c0abf0d](https://github.com/SerendipityOneInc/ecap-workspace/commit/1c0abf0d3bd07040e903ce40e9c2467eeb525b32)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T06:31:10Z
- **消息**: chore: tighten engines.node to >=24 <25 (#1061)

```
## Summary
Restrict `engines.node` from `>=24` to `>=24 <25`. Node 25 produces
silently-broken local dev state:
- vitest v4 + jsdom 26 + Node 25 combo leaves `localStorage` without a
`.clear` method at test runtime — 114 tests fail locally with
`TypeError: localStorage.clear is not a function` while CI (Node 24)
runs the same tests all green.
- In some vitest invocations on Node 25, the test discovery loop never
completes — 60+ seconds of environment boot followed by "0 tests loaded"
and non-zer
```

## [fdfcbfac](https://github.com/SerendipityOneInc/ecap-workspace/commit/fdfcbfac19611e976530e1c5d36f913b041c7ecc)
- **作者**: tim-srp
- **时间**: 2026-04-18T06:29:49Z
- **消息**: fix(openclaw): correct redeploy allowlist to preserve user data (#1060)

```
## Summary
Fix the pack redeploy allowlist — it was protecting pack templates
(TOOLS.md, AGENTS.md) while exposing user data (SOUL.md, IDENTITY.md,
memory/, media/).

## Changes

**File allowlist (never overwrite):**

| Before | After |
|--------|-------|
| MEMORY.md, USER.md, TOOLS.md, AGENTS.md | MEMORY.md, USER.md, SOUL.md,
IDENTITY.md |

**Copy-if-missing (new mechanism):**
- BOOTSTRAP.md — skip when local file exists (preserve in-progress
onboarding), copy when absent. Agents use its presen
```

## [4beb5a91](https://github.com/SerendipityOneInc/ecap-workspace/commit/4beb5a91a9bcab6f7df8b425f968cb7ebe1965d6)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T06:13:29Z
- **消息**: refactor(web): T2-f useCanvasChat spec 抽 renderAgentAndSend helper (#1059)

```
## Summary

useCanvasChat spec 12 个 streaming test 重复 7 行 pattern:

```ts
const params = makeDefaultParams()
params.chatMode = 'agent' as const
const { result } = renderHook(() => useCanvasChat(params))

await act(async () => {
  await result.current.sendMessage('Agent task')
})

const callbacks = mockStartStream.mock.calls[0][1]
```

这是 jscpd 识别的**最大 block**:L291-334 master,被 10+ 处 clone(14 行块 × 2 + 12 行块
× 多),贡献 tests dup 的 ~0.4%。

**抽 `renderAgentAndSend(message)` helper**:
- 内嵌 `makeDefaultP
```

## [0785e4e8](https://github.com/SerendipityOneInc/ecap-workspace/commit/0785e4e855cb7c2f20c380a5f779abb037043577)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T06:07:36Z
- **消息**: test(web): finish jest-dom migration for components/ (variable-ref form) (#1058)

```
## Summary
- Finish the components/ jest-dom migration started in #1029: 12
variable-reference presence assertions across 6 files, swapped from
`.toBeDefined()` / `.not.toBeNull()` / `.toBeNull()` to the jest-dom
semantic equivalents.
- Pure 1:1 matcher swap — net line change is 0 (12 insertions / 12
deletions).

## Context
#1029 migrated 148 inline-query sites
(`expect(screen.getByX(...)).toBeDefined()`) but intentionally left the
variable-reference form (`const el = getByX(...);
expect(el).toB
```

## [4b194c48](https://github.com/SerendipityOneInc/ecap-workspace/commit/4b194c48a7ca874b14d36d46f01aca9ab7dee46a)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T06:03:37Z
- **消息**: refactor(web): T2-e useOpenClawChat spec 抽 renderClawChat/renderStreamingChat helper (#1054)

```
## Summary

useOpenClawChat spec 30 个 test 有 2 大重复簇:

1. **send-message flow 样板**(15 处):`mockWsStatus = 'connected'` + `const
{ result } = renderHook(() => useOpenClawChat(getMockWs()))`
2. **streaming test 样板**(8 处):`const { handlers } =
setupWithEventCapture()` + `renderHook(...)` + `const sessionKey =
result.current.sessionKey` + `const chatHandler = handlers[0]`

**抽 2 个 helper 到顶层**:
- `renderClawChat(wsStatus?)` — 设 status + renderHook,default
`'connected'`
- `renderStreamingChat()` — 捕获 o
```

## [77493608](https://github.com/SerendipityOneInc/ecap-workspace/commit/774936080f34250030631b69eebccf3d65bed89f)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T06:02:33Z
- **消息**: refactor(claw-interface): openclaw_client.py → mixin package (1333→max 346) (#1055)

```
## Summary
- Convert 1333-line `openclaw_client.py` into a package with 8 mixin
files (max 346 lines each)
- `OpenClawPlatformClient` class assembled via multiple inheritance in
`__init__.py`
- **Zero caller changes** — all 30+ callers keep using `from
app.services.openclaw_client import get_openclaw_client`
- Only 4 test patch paths updated (logger/SETTINGS/asyncio moved to
mixin modules)

### Mixin files
| File | Lines | Domain |
|------|------:|--------|
| `_base.py` | 97 | HTTP pool, connect
```

## [aa03774c](https://github.com/SerendipityOneInc/ecap-workspace/commit/aa03774cfa5da2a4f0db3e26ee64ff580c51822e)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T05:55:17Z
- **消息**: refactor(web): T2-d upload spec 抽 setupUploadBrowserMocks helper (#1052)

```
## Summary

upload spec 3 个 describe 重复 29 行 identical beforeEach + afterEach 样板:
- `uploadToR2 — behavior tests`(L39-67)
- `onProgress callbacks`(L431-459)
- `uploadToR2 error paths`(L613-641)

`useUploadState` 里还有个 inline test(`'upload function calls
uploadToR2...'`)也用同 17 行 setup。

**抽 `setupUploadBrowserMocks(opts?)` helper 到模块顶层**:
- 构造 fetchSpy + 覆盖 `global.fetch`
- stub `URL.createObjectURL` / `revokeObjectURL`
- `vi.stubGlobal('Image', class {...})` 默认 width=800 height=600,可
overrides
- 
```

## [38117d18](https://github.com/SerendipityOneInc/ecap-workspace/commit/38117d1892769bf98f732ecb7fe33d9169f8ab3b)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T05:54:05Z
- **消息**: test(web): FeishuSetupModal 全面覆盖 (#899 Step 5) (#1047)

```
## Summary

Coverage 推进 plan Step 5——Claw Settings 的 Feishu setup modal (246 行) 原先 0
测试。Step 5 三个 wizards 里最小 / 自包含度最高，先拿下作为热身。

## 24 tests / 365 行 / 覆盖清单

**4 phase 迁移 × 2 种 timer**：

| 分组 | tests | 覆盖点 |
|---|---|---|
| initial render | 2 | loading phase + startFeishuSetup 参数映射 |
| QR phase | 3 | QR SVG value / 5:00 格式 / 0:09 leading-zero |
| startSetup 失败 | 2 | Error 消息 + 非 Error "Failed to start setup"
fallback |
| polling 正常结果 | 6 | success / expired / denied / error+message /
error+fallba
```

## [e6b7c81a](https://github.com/SerendipityOneInc/ecap-workspace/commit/e6b7c81a08ff849c1a0aa980bb917b61ed296a6f)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T05:44:40Z
- **消息**: chore(web): remove dead pnpm block from web/package.json (#1051)

```
## Summary
Delete `web/package.json`'s `pnpm.overrides` +
`pnpm.onlyBuiltDependencies`. pnpm ≥ 8 ignores `pnpm.*` in workspace
child packages — only the root `package.json` block is honored. CI has
been printing two warnings on every install for this reason, and the
block has been dead code since the switch.

## Why this is a behavioral no-op
- **`overrides`** — `{flatted, fast-xml-parser, undici}` is
character-for-character identical to the root's block. Only the root
copy was ever honored.
- *
```

## [48266f6b](https://github.com/SerendipityOneInc/ecap-workspace/commit/48266f6bcee0e75ce78ecaac775e49cf2e85ac60)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T05:42:47Z
- **消息**: refactor(claw-interface): agent_deploy 拆 3 modules — 全 ≤500 (#1015)

```
## Summary

agent_deploy.py(961 行)拆为 3 sibling + 主文件,全部 ≤500:

| 文件 | 行数 |
|---|---:|
| agent_deploy.py | 305 |
| agent_deploy_pack.py | 350 |
| agent_deploy_phases.py | 188 |
| agent_deploy_workspace.py | 177 |

主文件 re-export 全部 moved symbols(noqa:F401),caller 零改动。
测试用 monkeypatch proxy fixture 同步 sub-module bindings,不需要每个 test 加
dual-patch。

pyright 0 errors / 2521 passed / agent_deploy 从 file-length WARNING 消失。
需 size-override。

🤖 Generated with [Claude Code](https://claude.com/claude-code)


```

## [52060f9f](https://github.com/SerendipityOneInc/ecap-workspace/commit/52060f9f6079ba701e097cc776ff3d58aef6803c)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T05:39:53Z
- **消息**: refactor(web): T2-c useLiteLLMApi spec 引入 renderLiteLLMApi helper (#1050)

```
## Summary

useLiteLLMApi spec 21 处 test 重复同样的 9 行 `renderHook(() => useLiteLLMApi({
... 4 fields ... }))` 样板,只有 `sessionId` 有 3 种变化(`null` / `'s1'` /
`'session-1'`),其他字段全默认。

**抽 `renderLiteLLMApi(overrides?: Partial<LiteLLMHookOptions>)`
helper**:
- 默认 `sessionId: null, selectedModel: 'gpt-4', agentName: 'test',
setShowInsufficientCreditsModal: vi.fn()`
- `overrides` 浅覆盖,spread 模式

**3 次 `replace_all` 按 sessionId 值分组吃完 21 处**:
- 17 处 `sessionId: null` → `renderLiteLLMApi()`
- 2 处 `sessionId: '
```

## [77d8365a](https://github.com/SerendipityOneInc/ecap-workspace/commit/77d8365ab86ee2681532ee8d86eecd26dce0014c)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T05:29:35Z
- **消息**: chore(web): pin vitest via pnpm.overrides, drop #1029 runtime workaround (#1049)

```
## Summary
- Root `pnpm.overrides` pins the vitest family (`vitest`,
`@vitest/expect`, `@vitest/runner`, `@vitest/spy`, `@vitest/utils`,
`@vitest/snapshot`) to `^4`. Prior state had `vitest@4.0.18` (web's
direct dep) and `vitest@1.6.1` (transitive) coexisting, which caused the
class of bugs #1029 had to work around.
- Drop the manual `expect.extend(matchers)` from `web/vitest.setup.ts`.
With one-and-only-one vitest in the graph, jest-dom's `/vitest` entry
binds to the right `expect` on its own.

```

## [2065b660](https://github.com/SerendipityOneInc/ecap-workspace/commit/2065b66021b972639bd68f31a4ed9bbcd9105b67)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T04:56:22Z
- **消息**: docs: add asset size guide for designers and engineers (#1048)

```
## 背景

PR #1039 刚合入了 pre-commit 自动压缩 + CI 硬上限拦截的素材大小控制机制。本 PR
补一份面向使用者的指南文档，方便设计师和工程师了解如何启用、日常怎么使用、遇到问题怎么处理。

## 文档位置

`docs/asset-size-guide.md`（顶层，和 `docs/local-dev-guide.md` /
`docs/ci-review-and-merge-queue.md` 同级，kebab-case 沿袭现有命名）。

## 覆盖内容

- 两层防线的职责边界（pre-commit warn-only + CI 硬上限 fail）
- 硬上限阈值表
- 设计师一次性启用：`pnpm install` 在仓库根即可
- 日常 commit 会看到的两种输出（自动压缩成功 / 压不下去 warning）
- **工具坏掉时 commit 会被阻断**（刻意行为，避免 sharp 缺失时静默放过素材）
- 如何从 `.git/asset-backup/` 按时间戳恢复被误优化的原件
- 超阈值时的常规处理建议（squoosh / WebP
```

## [1f5718d8](https://github.com/SerendipityOneInc/ecap-workspace/commit/1f5718d8486f84a5e1d75d44eb6e1b410753ad1a)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T04:45:27Z
- **消息**: feat(ci): block oversized assets with pre-commit hook and CI gate (#1039)

```
## 背景

设计师偶尔把未优化的大图/GIF 直接 commit 进仓库（存量如 `web/public/themes/panda-claw/w.gif`
13M、`nano-banana-2-hero.png` 6M），增加前端 bundle 体积和首屏负担。现有
`scripts/check-pr-size.sh` 主动排除所有二进制文件（职责是行数预算），素材字节数完全不设防。

本 PR 建立两层防线：

1. **本地 pre-commit**：自动用 sharp 无损压缩新增/修改的 PNG/JPG/WebP 并
re-stage，超阈值只警告不阻断 —— 保证设计师工作流顺畅。
2. **CI `asset-size-guard`**：硬上限，压缩后仍超阈值直接 fail PR。

## 设计要点

- **范围**：`web/public/**` + `ios/ZooClaw/ZooClaw/Assets.xcassets/**`（iOS
CLAUDE.md 不动）
- **阈值**：PNG/JPG 500KB · WebP 300KB · GIF 1MB · MP4
```

## [091bd65e](https://github.com/SerendipityOneInc/ecap-workspace/commit/091bd65e5916b4e7446f22083dd963276f0991d3)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T04:40:23Z
- **消息**: refactor(web): T2-b useSSEStream spec 引入 runStartStream helper (#1041)

```
## Summary

useSSEStream spec 947 行,18 处重复 ~15 行 startStream 样板(renderHook +
3-callback bag + DEFAULT_PAYLOAD + `await act(() => startStream(...))`)。

**抽 2 个 helper**:
- `makeCallbacks(withCredits?)` — 构造 3-cb 或 4-cb
bag(onInsufficientCredits 可选)
- `runStartStream(opts?)` — `renderHook` + `startStream` 一体,return `{
result, callbacks }`。payload 默认 `{ agentName: 'test-agent', uid:
'user-1', sessionId: 'sess-1', message: 'Hello' }`,hookOptions 默认 `{
sessionId: 'sess-1' }`,都可通过 `opts` 覆盖

**替换方式**(
```

## [1fa0e19d](https://github.com/SerendipityOneInc/ecap-workspace/commit/1fa0e19d910d52f1fcffa3fda8a4ad1aa6c9b0d2)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T04:38:54Z
- **消息**: chore(web): eslint 规则拦截 expect(getBy*/findBy*).toBeDefined() (#1037)

```
## Summary

Follow-up to #1035——加规则防复发。

#1035 清除了仓库里 29 处冗余 `expect(getBy*/findBy*).toBeDefined()`。但"冗余 +
易复制"的模板一旦存在就会持续传染（本仓库同模式跨 3 PR、3 个文件、半年时间）。加 ESLint 规则在 CI
层硬阻断，让下一个开发者复制粘贴时秒报错。

## 规则

`tests/**/*.{ts,tsx,js,jsx}` override block 下 `no-restricted-syntax` 新增
2 条 selector：

| Selector | 匹配 |
|---|---|
| sync | `expect(getByX(...)).toBeDefined()` |
| async | `expect(await findByX(...)).toBeDefined()` |

前缀 `getBy / findBy / getAllBy / findAllBy` 精确命中 RTL 查询 API，不误伤：
- `querySelector(...)`
```

