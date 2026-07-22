# SerendipityOneInc/ecap-workspace commits 2026-07-21

## test(web): fix flaky AccountSessionGate login-modal assertions (#3003)

- **SHA**: befe2c9385f12850fdb1d4dbff46851bb7ba3461
- **作者**: Chris@ZooClaw
- **日期**: 2026-07-21T17:55:28Z
- **PR**: #3003

### Commit Message

```
test(web): fix flaky AccountSessionGate login-modal assertions (#3003)

## 问题

`web-quality / test` 在 main 的 `5bf159a72`（#3001）上变红：

```
FAIL tests/unit/components/AccountSessionGate.unit.spec.tsx
  > clears a rejected stale session without leaving the specialist chat deep link
AssertionError: expected false to be true
  ❯ 186 | expect(loginCheckStore.getState().open).toBe(true)
```

跟 #3001 无关——那个 PR 没碰 `AccountSessionGate` /
`login-check-store`，只是加了几个新测试文件。这是一个**既有的不稳定测试**，只在机器繁忙时暴露。

## 根因

两个 specialist deep-link 用例在 `findByText('Get started')` resolve 的同一 tick
上直接断言 store：

```tsx
expect(await screen.findByText('Get started')).toBeInTheDocument()
const { loginCheckStore } = await import('@/lib/login-check-store')
expect(loginCheckStore.getState().open).toBe(true)   // ← race
```

但 `LandingScreen` 是在 **passive effect** 里 `showLoginModal()` 的，而挂载它的
state 更新来自 `act()` 作用域**之外**——`AccountSessionGate` 里的 `void
logoutUser().then(completeSpecialistLogout)`。React 提交 DOM 之后才通过
Scheduler 排 passive effect，而 RTL 靠 MutationObserver（微任务）观察 DOM。所以「文本出现在
DOM 里」并不是 effect 已执行的同步点，机器一忙两者顺序就翻转。

复现时的插桩时间线：

```
FOUND-Get-started | open=true | open-arrived-LATE   openAtAssert=false
```

store 确实翻到了 `open`，只是在断言之后。**产品行为没问题，是测试同步不足。**

## 改动

两处断言改成 `await waitFor(...)`，并写清为什么不能同 tick 断言。仅测试文件，无生产代码改动。

## 验证

| | 旧代码 | 新代码 |
|---|---|---|
| 单跑 ×20 | 1 次失败 | — |
| 6 并发 × 12 轮（模拟 CI 负载） | 复现失败 | **72/72 通过** |
| `scripts/verify-web.sh` | — | 全绿（tsc + 7126 单测 + eslint + 7 guards） |

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## 问题

`web-quality / test` 在 main 的 `5bf159a72`（#3001）上变红：

```
FAIL tests/unit/components/AccountSessionGate.unit.spec.tsx
  > clears a rejected stale session without leaving the specialist chat deep link
AssertionError: expected false to be true
  ❯ 186 | expect(loginCheckStore.getState().open).toBe(true)
```

跟 #3001 无关——那个 PR 没碰 `AccountSessionGate` / `login-check-store`，只是加了几个新测试文件。这是一个**既有的不稳定测试**，只在机器繁忙时暴露。

## 根因

两个 specialist deep-link 用例在 `findByText('Get started')` resolve 的同一 tick 上直接断言 store：

```tsx
expect(await screen.findByText('Get started')).toBeInTheDocument()
const { loginCheckStore } = await import('@/lib/login-check-store')
expect(loginCheckStore.getState().open).toBe(true)   // ← race
```

但 `LandingScreen` 是在 **passive effect** 里 `showLoginModal()` 的，而挂载它的 state 更新来自 `act()` 作用域**之外**——`AccountSessionGate` 里的 `void logoutUser().then(completeSpecialistLogout)`。React 提交 DOM 之后才通过 Scheduler 排 passive effect，而 RTL 靠 MutationObserver（微任务）观察 DOM。所以「文本出现在 DOM 里」并不是 effect 已执行的同步点，机器一忙两者顺序就翻转。

复现时的插桩时间线：

```
FOUND-Get-started | open=true | open-arrived-LATE   openAtAssert=false
```

store 确实翻到了 `open`，只是在断言之后。**产品行为没问题，是测试同步不足。**

## 改动

两处断言改成 `await waitFor(...)`，并写清为什么不能同 tick 断言。仅测试文件，无生产代码改动。

## 验证

| | 旧代码 | 新代码 |
|---|---|---|
| 单跑 ×20 | 1 次失败 | — |
| 6 并发 × 12 轮（模拟 CI 负载） | 复现失败 | **72/72 通过** |
| `scripts/verify-web.sh` | — | 全绿（tsc + 7126 单测 + eslint + 7 guards） |


---

## perf(chat): stop re-rendering every message on each streaming frame (#3001)

- **SHA**: 5bf159a726e662bca3c03b50a86382b3bc84c604
- **作者**: Chris@ZooClaw
- **日期**: 2026-07-21T16:11:05Z
- **PR**: #3001

### Commit Message

```
perf(chat): stop re-rendering every message on each streaming frame (#3001)

## 背景

PR #2989 修好了打字机本身，但 #2991 的 staging 复测暴露了一个随会话长度恶化的问题：3 条 bot 消息时 1 个
long task / 0.2% 掉帧，**32 条时 11 个 long task（667ms）/ 34% 掉帧 / 帧 p50 从
8.4ms 劣化到 25ms**（120fps → 40fps）。而且 32 条那轮 DOM 更新反而更少（1892 vs
3236）——打字机被主线程饿着。用户感知就是"聊得越久越卡"。

spec 里 P1
写的是「把流式文本抽成独立叶子组件」。**追代码后发现这个归因不准确**，真正的每帧成本是两个具体缺陷，抽叶子替代不了它们（详见 spec
第六.七节）。

## 两个缺陷

**1. 三处无条件 spread 摧毁引用标识，让两层缓存 100% miss**

`useOpenClawRuntime.ts` 里的 per-message 转换缓存（命中条件 `cached.src ===
msg`）本来就是为这个场景写的，注释都点明了后果："would cause all message components to
re-render"。下游 assistant-ui 的 `ThreadMessageConverter` 还叠了一层按对象标识的
`WeakMap`。

但上游每帧给每条消息造新对象，三处：`useMmTypewriter` 的 mapper、它的 sentinel strip、以及
`filterMessages` 里**重复的**同一个 strip。两层缓存全部落空 → 每条消息每帧重渲染并重新解析 markdown。

**2. 每个消息组件订阅整个 thread state，各自再做 O(n) 扫描 → 每帧 O(n²)**

`useThread()` 不传 selector 时用 identity selector，thread state
一变必然重渲染，`React.memo` 挡不住（memo 挡 props，挡不住组件内部的 store
订阅）。`AssistantMessageFactory` 的 `isConsecutive` 和
`OpenClawAssistantMessage` 的 `precedingUserQuery` 还各自 `findIndex` 全表扫一遍。

讽刺的是 `OpenClawThread.tsx` 里的注释写着 "avoids useThread() in message
components"，`ThreadConfigContext` 就是为此而建——意图在，执行退化了。

## 改动

- **`useMmTypewriter`**：mapper 加 per-message memo；sentinel strip
仅在真正改变内容时才分配。**未**把 strip 提前到 mapper——当前顺序是「先 `shouldHideMessage`(未
strip) 再 strip」，提前会改变 `visibleMessages` 成员进而影响 `findActiveTurnStatus`。
- **`filterMessages` / `toolGroupAggregator`**：同样改为 identity-preserving。
- **`useOpenClawRuntime`**：一趟前向扫描算出 `isConsecutive` /
`precedingUserQuery` 塞进 `metadata.custom`。转换缓存的命中条件**必须同时**比这两个值，否则会出现
stale 的 `isConsecutive`（该显示的身份行不显示）——有测试专门钉这条。
- **三个消息组件**不再调 `useThread()`；仅剩一处改为 `useThread((s) => s.isRunning)`，让
`useSyncExternalStore` 按 `Object.is` bail out。

两个界面（`/chat` 与 session thread）共用这条管线，一处修复覆盖两边。**无可见行为变化。**

## 实测

### 生产构建 A/B（决定性数据）

本地 `next build` + `next start` 连 staging 后端，两个分支各构建一次，
测同一个 `/chat`（31 条 bot 消息）：

| 指标 | main | **本 PR** | 变化 |
|---|---|---|---|
| long task | 14（869ms） | **8（537ms）** | **−43%** |
| 帧 >33ms | 30.3% | **12.8%** | **−58%** |
| 帧 p50 | 25ms | **16.8ms** | **−33%** |
| DOM 更新 | 1872 | **2243** | **+20%** |

main 这组与部署在 staging 上的基线（11 个 long task / 34.1% / 25ms，spec 第六.六节）
在同一量级，说明本地生产构建与部署版可比。DOM 更新上升说明打字机不再被主线程饿着。

### dev 构建 A/B（先做的，方向一致）

staging 当时不可用（rollout 后 Cloudflare→GCLB 段 502，pod 本身健康），先用 dev 构建定方向：

| 运行 | 分支 | bot 消息 | 帧 p50 | 帧 >33ms | long task | DOM 更新 |
|---|---|---|---|---|---|---|
| before | main | 7 | 15.7ms | 3.2% | 5 | 2844 |
| after | 本 PR | 9 | **8.7ms** | **1.5%** | 8 | 3040 |
| before2 | main | 11 | 16.6ms | 4.4% | 9 | 2649 |

dev 下 long task 计数没降（React dev 开销把它顶在阈值上），但时长不再随线程增长
（main avg 60→66ms / max 65→82ms，本 PR avg 56ms / max 64ms）。生产构建下计数也降了。

## 剩下的（不在本 PR）

**不是 markdown 增量解析。** 把生产数据和短线程放一起看：

| | 3 条消息 | 31 条消息（本 PR 后） |
|---|---|---|
| 帧 >33ms | 0.2% | 12.8% |
| 帧 p50 | 8.4ms | 16.8ms |

长线程仍明显差于短线程，每帧成本仍与条数相关。原因是本 PR 只保住了**元素**的引用标识，
没保住**数组**的：`buildMmDisplayMessages` 的 `messages.map(...)` 每帧返回新数组，
下游一串 `useMemo` 依赖每帧都变，约 10 趟 O(n) 遍历照跑
（filterMessages / dedup / aggregateToolMessages / buildNeighbourContexts
/
stableConverted / buildTurnStatusByUserPostId / …）。

本 PR 把**每个元素的成本**从「分配新对象 + 重渲染组件 + 重解析 markdown」降到
「一次 Map 查找」——58% 的掉帧改善来自这里；但**遍历次数没变**。

**所以 spec 第五节 P1 原本的方向（把流式文本抽成独立叶子组件，让消息列表不参与每帧重渲染）
是对的**，它正是消除这最后一层 O(n) 的手段。markdown 增量解析优先级排在它之后
（短线程只有 1 个 long task，说明该路径单独开销有限）。详见 spec 第六.七节。

## 测试

新增测试钉的是**不变量**而非数字，且**每条都验证过在旧实现上会失败**：

- 未变化的消息跨帧保持 `Object.is` 相等（typewriter + runtime 两层）
- 邻居上下文变化时必须重新转换（防 stale `isConsecutive`）
- 消息列表变化时组件**不重渲染**，`isRunning` 翻转时才重渲染 —— 该用例的 `useThread` mock 由真实
`useSyncExternalStore` 支撑，量的是 React 真实 bailout 语义
- 分组规则用例整体从组件层迁到 `useOpenClawRuntime` 层

**一个刻意没写的测试**：`OpenClawThread.unit.spec.tsx` 里的渲染次数测试。该文件的 assistant-ui
mock 会无条件重渲染每个 factory，在那里数渲染次数是在量 mock 而非 React，正确实现同样会失败——属于假测试。

本地：`scripts/verify-web.sh` 全绿（7126 单测 + tsc + eslint + 7 个 guard）。

## 相关

- 前序：#2989（打字机修复）、#2991（复测数据 + 测量脚本）
- spec：`docs/superpowers/specs/2026-07-21-chat-streaming-smoothness.md`
第六.七节

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## 背景

PR #2989 修好了打字机本身，但 #2991 的 staging 复测暴露了一个随会话长度恶化的问题：3 条 bot 消息时 1 个 long task / 0.2% 掉帧，**32 条时 11 个 long task（667ms）/ 34% 掉帧 / 帧 p50 从 8.4ms 劣化到 25ms**（120fps → 40fps）。而且 32 条那轮 DOM 更新反而更少（1892 vs 3236）——打字机被主线程饿着。用户感知就是"聊得越久越卡"。

spec 里 P1 写的是「把流式文本抽成独立叶子组件」。**追代码后发现这个归因不准确**，真正的每帧成本是两个具体缺陷，抽叶子替代不了它们（详见 spec 第六.七节）。

## 两个缺陷

**1. 三处无条件 spread 摧毁引用标识，让两层缓存 100% miss**

`useOpenClawRuntime.ts` 里的 per-message 转换缓存（命中条件 `cached.src === msg`）本来就是为这个场景写的，注释都点明了后果："would cause all message components to re-render"。下游 assistant-ui 的 `ThreadMessageConverter` 还叠了一层按对象标识的 `WeakMap`。

但上游每帧给每条消息造新对象，三处：`useMmTypewriter` 的 mapper、它的 sentinel strip、以及 `filterMessages` 里**重复的**同一个 strip。两层缓存全部落空 → 每条消息每帧重渲染并重新解析 markdown。

**2. 每个消息组件订阅整个 thread state，各自再做 O(n) 扫描 → 每帧 O(n²)**

`useThread()` 不传 selector 时用 identity selector，thread state 一变必然重渲染，`React.memo` 挡不住（memo 挡 props，挡不住组件内部的 store 订阅）。`AssistantMessageFactory` 的 `isConsecutive` 和 `OpenClawAssistantMessage` 的 `precedingUserQuery` 还各自 `findIndex` 全表扫一遍。

讽刺的是 `OpenClawThread.tsx` 里的注释写着 "avoids useThread() in message components"，`ThreadConfigContext` 就是为此而建——意图在，执行退化了。

## 改动

- **`useMmTypewriter`**：mapper 加 per-message memo；sentinel strip 仅在真正改变内容时才分配。**未**把 strip 提前到 mapper——当前顺序是「先 `shouldHideMessage`(未 strip) 再 strip」，提前会改变 `visibleMessages` 成员进而影响 `findActiveTurnStatus`。
- **`filterMessages` / `toolGroupAggregator`**：同样改为 identity-preserving。
- **`useOpenClawRuntime`**：一趟前向扫描算出 `isConsecutive` / `precedingUserQuery` 塞进 `metadata.custom`。转换缓存的命中条件**必须同时**比这两个值，否则会出现 stale 的 `isConsecutive`（该显示的身份行不显示）——有测试专门钉这条。
- **三个消息组件**不再调 `useThread()`；仅剩一处改为 `useThread((s) => s.isRunning)`，让 `useSyncExternalStore` 按 `Object.is` bail out。

两个界面（`/chat` 与 session thread）共用这条管线，一处修复覆盖两边。**无可见行为变化。**

## 实测

### 生产构建 A/B（决定性数据）

本地 `next build` + `next start` 连 staging 后端，两个分支各构建一次，
测同一个 `/chat`（31 条 bot 消息）：

| 指标 | main | **本 PR** | 变化 |
|---|---|---|---|
| long task | 14（869ms） | **8（537ms）** | **−43%** |
| 帧 >33ms | 30.3% | **12.8%** | **−58%** |
| 帧 p50 | 25ms | **16.8ms** | **−33%** |
| DOM 更新 | 1872 | **2243** | **+20%** |

main 这组与部署在 staging 上的基线（11 个 long task / 34.1% / 25ms，spec 第六.六节）
在同一量级，说明本地生产构建与部署版可比。DOM 更新上升说明打字机不再被主线程饿着。

### dev 构建 A/B（先做的，方向一致）

staging 当时不可用（rollout 后 Cloudflare→GCLB 段 502，pod 本身健康），先用 dev 构建定方向：

| 运行 | 分支 | bot 消息 | 帧 p50 | 帧 >33ms | long task | DOM 更新 |
|---|---|---|---|---|---|---|
| before | main | 7 | 15.7ms | 3.2% | 5 | 2844 |
| after | 本 PR | 9 | **8.7ms** | **1.5%** | 8 | 3040 |
| before2 | main | 11 | 16.6ms | 4.4% | 9 | 2649 |

dev 下 long task 计数没降（React dev 开销把它顶在阈值上），但时长不再随线程增长
（main avg 60→66ms / max 65→82ms，本 PR avg 56ms / max 64ms）。生产构建下计数也降了。

## 剩下的（不在本 PR）

**不是 markdown 增量解析。** 把生产数据和短线程放一起看：

| | 3 条消息 | 31 条消息（本 PR 后） |
|---|---|---|
| 帧 >33ms | 0.2% | 12.8% |
| 帧 p50 | 8.4ms | 16.8ms |

长线程仍明显差于短线程，每帧成本仍与条数相关。原因是本 PR 只保住了**元素**的引用标识，
没保住**数组**的：`buildMmDisplayMessages` 的 `messages.map(...)` 每帧返回新数组，
下游一串 `useMemo` 依赖每帧都变，约 10 趟 O(n) 遍历照跑
（filterMessages / dedup / aggregateToolMessages / buildNeighbourContexts /
stableConverted / buildTurnStatusByUserPostId / …）。

本 PR 把**每个元素的成本**从「分配新对象 + 重渲染组件 + 重解析 markdown」降到
「一次 Map 查找」——58% 的掉帧改善来自这里；但**遍历次数没变**。

**所以 spec 第五节 P1 原本的方向（把流式文本抽成独立叶子组件，让消息列表不参与每帧重渲染）
是对的**，它正是消除这最后一层 O(n) 的手段。markdown 增量解析优先级排在它之后
（短线程只有 1 个 long task，说明该路径单独开销有限）。详见 spec 第六.七节。

## 测试

新增测试钉的是**不变量**而非数字，且**每条都验证过在旧实现上会失败**：

- 未变化的消息跨帧保持 `Object.is` 相等（typewriter + runtime 两层）
- 邻居上下文变化时必须重新转换（防 stale `isConsecutive`）
- 消息列表变化时组件**不重渲染**，`isRunning` 翻转时才重渲染 —— 该用例的 `useThread` mock 由真实 `useSyncExternalStore` 支撑，量的是 React 真实 bailout 语义
- 分组规则用例整体从组件层迁到 `useOpenClawRuntime` 层

**一个刻意没写的测试**：`OpenClawThread.unit.spec.tsx` 里的渲染次数测试。该文件的 assistant-ui mock 会无条件重渲染每个 factory，在那里数渲染次数是在量 mock 而非 React，正确实现同样会失败——属于假测试。

本地：`scripts/verify-web.sh` 全绿（7126 单测 + tsc + eslint + 7 个 guard）。

## 相关

- 前序：#2989（打字机修复）、#2991（复测数据 + 测量脚本）
- spec：`docs/superpowers/specs/2026-07-21-chat-streaming-smoothness.md` 第六.七节


---

## chore(deps): update openai requirement from <2.44.0,>=2.43.0 to >=2.45.0,<2.46.0 in /services/claw-interface (#2943)

- **SHA**: 95bfcc46041d68df93316022695e039125829eb1
- **作者**: dependabot[bot]
- **日期**: 2026-07-21T14:39:56Z
- **PR**: #2943

### Commit Message

```
chore(deps): update openai requirement from <2.44.0,>=2.43.0 to >=2.45.0,<2.46.0 in /services/claw-interface (#2943)

Updates the requirements on
[openai](https://github.com/openai/openai-python) to permit the latest
version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/openai/openai-python/releases">openai's
releases</a>.</em></p>
<blockquote>
<h2>v2.45.0</h2>
<h2>2.45.0 (2026-07-09)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.44.0...v2.45.0">v2.44.0...v2.45.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> gpt-5.6-sol updates (<a
href="https://github.com/openai/openai-python/commit/039d1feb264a2dca7195ba5028e9fb47a5e04987">039d1fe</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> restore beta resource accessors (<a
href="https://github.com/openai/openai-python/commit/2dfc130b8f0fdb0049e075aac21aaef29482b4e3">2dfc130</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li>retrigger release automation (<a
href="https://github.com/openai/openai-python/commit/7b61351b014bb6ca4623ff6cce7f32f45038a92e">7b61351</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/openai/openai-python/blob/main/CHANGELOG.md">openai's
changelog</a>.</em></p>
<blockquote>
<h2>2.45.0 (2026-07-09)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.44.0...v2.45.0">v2.44.0...v2.45.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> gpt-5.6-sol updates (<a
href="https://github.com/openai/openai-python/commit/039d1feb264a2dca7195ba5028e9fb47a5e04987">039d1fe</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> restore beta resource accessors (<a
href="https://github.com/openai/openai-python/commit/2dfc130b8f0fdb0049e075aac21aaef29482b4e3">2dfc130</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li>retrigger release automation (<a
href="https://github.com/openai/openai-python/commit/7b61351b014bb6ca4623ff6cce7f32f45038a92e">7b61351</a>)</li>
</ul>
<h2>2.44.0 (2026-06-24)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.43.0...v2.44.0">v2.43.0...v2.44.0</a></p>
<h3>Bug Fixes</h3>
<ul>
<li><strong>auth:</strong> prioritize first auth header (<a
href="https://github.com/openai/openai-python/commit/797e3362e222ae14e587a4543b76a54d8992d66c">797e336</a>)</li>
</ul>
<h2>2.43.0 (2026-06-17)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.42.0...v2.43.0">v2.42.0...v2.43.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> update OpenAPI spec or Stainless config (<a
href="https://github.com/openai/openai-python/commit/22542358490ef8f31f0d373e17f7b791b3d983ca">2254235</a>)</li>
</ul>
<h2>2.42.0 (2026-06-16)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.41.1...v2.42.0">v2.41.1...v2.42.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> admin spend_alerts (<a
href="https://github.com/openai/openai-python/commit/6134198a488996c4ff6fca4551afd55fb3294fdc">6134198</a>)</li>
<li><strong>api:</strong> manual updates (<a
href="https://github.com/openai/openai-python/commit/f337bf43276c880d2daf09a5d7f9fc9a886c4bf2">f337bf4</a>)</li>
<li><strong>api:</strong> update OpenAPI spec or Stainless config (<a
href="https://github.com/openai/openai-python/commit/7015158c3119acf57af6c20903587cef928530a9">7015158</a>)</li>
</ul>
<h3>Build System</h3>
<ul>
<li>fix release workflow permissions (<a
href="https://redirect.github.com/openai/openai-python/issues/3389">#3389</a>)
(<a
href="https://github.com/openai/openai-python/commit/a526ee813f085318fe3c6923ac3fa10c1cf56420">a526ee8</a>)</li>
<li>Use CI environment for examples API key (<a
href="https://redirect.github.com/openai/openai-python/issues/3394">#3394</a>)
(<a
href="https://github.com/openai/openai-python/commit/d64d811e82aff724397e32d593e50657fee3f905">d64d811</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/openai/openai-python/commit/f16fbbd2bd25dc1ff150b5f78dbd15ff6bab6d91"><code>f16fbbd</code></a>
release: 2.45.0 (<a
href="https://redirect.github.com/openai/openai-python/issues/3478">#3478</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/6d9262d5c666a1e4d47f63178db907ba3087ac5d"><code>6d9262d</code></a>
release: 2.44.0</li>
<li><a
href="https://github.com/openai/openai-python/commit/d35627525e192b7a65b556d8a79d22079ccabdf6"><code>d356275</code></a>
[codex] Add AWS Bedrock provider authentication (<a
href="https://redirect.github.com/openai/openai-python/issues/3398">#3398</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/f47f9a270861ca6a6096e8ea15ef8f3e1fb089b0"><code>f47f9a2</code></a>
fix(auth): prioritize first auth header</li>
<li>See full diff in <a
href="https://github.com/openai/openai-python/compare/v2.43.0...v2.45.0">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Body

Updates the requirements on [openai](https://github.com/openai/openai-python) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/openai/openai-python/releases">openai's releases</a>.</em></p>
<blockquote>
<h2>v2.45.0</h2>
<h2>2.45.0 (2026-07-09)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.44.0...v2.45.0">v2.44.0...v2.45.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> gpt-5.6-sol updates (<a href="https://github.com/openai/openai-python/commit/039d1feb264a2dca7195ba5028e9fb47a5e04987">039d1fe</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> restore beta resource accessors (<a href="https://github.com/openai/openai-python/commit/2dfc130b8f0fdb0049e075aac21aaef29482b4e3">2dfc130</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li>retrigger release automation (<a href="https://github.com/openai/openai-python/commit/7b61351b014bb6ca4623ff6cce7f32f45038a92e">7b61351</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/openai/openai-python/blob/main/CHANGELOG.md">openai's changelog</a>.</em></p>
<blockquote>
<h2>2.45.0 (2026-07-09)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.44.0...v2.45.0">v2.44.0...v2.45.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> gpt-5.6-sol updates (<a href="https://github.com/openai/openai-python/commit/039d1feb264a2dca7195ba5028e9fb47a5e04987">039d1fe</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> restore beta resource accessors (<a href="https://github.com/openai/openai-python/commit/2dfc130b8f0fdb0049e075aac21aaef29482b4e3">2dfc130</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li>retrigger release automation (<a href="https://github.com/openai/openai-python/commit/7b61351b014bb6ca4623ff6cce7f32f45038a92e">7b61351</a>)</li>
</ul>
<h2>2.44.0 (2026-06-24)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.43.0...v2.44.0">v2.43.0...v2.44.0</a></p>
<h3>Bug Fixes</h3>
<ul>
<li><strong>auth:</strong> prioritize first auth header (<a href="https://github.com/openai/openai-python/commit/797e3362e222ae14e587a4543b76a54d8992d66c">797e336</a>)</li>
</ul>
<h2>2.43.0 (2026-06-17)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.42.0...v2.43.0">v2.42.0...v2.43.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> update OpenAPI spec or Stainless config (<a href="https://github.com/openai/openai-python/commit/22542358490ef8f31f0d373e17f7b791b3d983ca">2254235</a>)</li>
</ul>
<h2>2.42.0 (2026-06-16)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.41.1...v2.42.0">v2.41.1...v2.42.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> admin spend_alerts (<a href="https://github.com/openai/openai-python/commit/6134198a488996c4ff6fca4551afd55fb3294fdc">6134198</a>)</li>
<li><strong>api:</strong> manual updates (<a href="https://github.com/openai/openai-python/commit/f337bf43276c880d2daf09a5d7f9fc9a886c4bf2">f337bf4</a>)</li>
<li><strong>api:</strong> update OpenAPI spec or Stainless config (<a href="https://github.com/openai/openai-python/commit/7015158c3119acf57af6c20903587cef928530a9">7015158</a>)</li>
</ul>
<h3>Build System</h3>
<ul>
<li>fix release workflow permissions (<a href="https://redirect.github.com/openai/openai-python/issues/3389">#3389</a>) (<a href="https://github.com/openai/openai-python/commit/a526ee813f085318fe3c6923ac3fa10c1cf56420">a526ee8</a>)</li>
<li>Use CI environment for examples API key (<a href="https://redirect.github.com/openai/openai-python/issues/3394">#3394</a>) (<a href="https://github.com/openai/openai-python/commit/d64d811e82aff724397e32d593e50657fee3f905">d64d811</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/openai/openai-python/commit/f16fbbd2bd25dc1ff150b5f78dbd15ff6bab6d91"><code>f16fbbd</code></a> release: 2.45.0 (<a href="https://redirect.github.com/openai/openai-python/issues/3478">#3478</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/6d9262d5c666a1e4d47f63178db907ba3087ac5d"><code>6d9262d</code></a> release: 2.44.0</li>
<li><a href="https://github.com/openai/openai-python/commit/d35627525e192b7a65b556d8a79d22079ccabdf6"><code>d356275</code></a> [codex] Add AWS Bedrock provider authentication (<a href="https://redirect.github.com/openai/openai-python/issues/3398">#3398</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/f47f9a270861ca6a6096e8ea15ef8f3e1fb089b0"><code>f47f9a2</code></a> fix(auth): prioritize first auth header</li>
<li>See full diff in <a href="https://github.com/openai/openai-python/compare/v2.43.0...v2.45.0">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---

## chore(deps-dev): update import-linter requirement from >=2.11 to >=2.13 in /services/claw-interface (#2830)

- **SHA**: 2dd9558f463f28ae462ce92c1b428d12885112f2
- **作者**: dependabot[bot]
- **日期**: 2026-07-21T14:39:39Z
- **PR**: #2830

### Commit Message

```
chore(deps-dev): update import-linter requirement from >=2.11 to >=2.13 in /services/claw-interface (#2830)

Updates the requirements on
[import-linter](https://github.com/seddonym/import-linter) to permit the
latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/seddonym/import-linter/blob/main/docs/release_notes.md">import-linter's
changelog</a>.</em></p>
<blockquote>
<h2>2.13 (2026-07-03)</h2>
<ul>
<li>Add module counts option to the explore UI and
<code>drawgraph</code> command.</li>
</ul>
<h2>2.12 (2026-06-23)</h2>
<ul>
<li>Improve error message when root package is a single-file
module.</li>
<li>Alert users with all unmatched ignored imports in the same run.</li>
<li>Allow overlapping modules in forbidden contracts.</li>
</ul>
<h2>2.11 (2026-03-06)</h2>
<ul>
<li>Add <code>--version</code> flag to <code>lint-imports</code> and
<code>import-linter</code> commands.</li>
<li>Make <code>fastapi</code> and <code>uvicorn</code> optional via the
<code>ui</code> extra (<code>pip install import-linter[ui]</code>).</li>
<li>Bugfix: fix back button navigation in explore command.</li>
<li>Provide lower limits for <code>fastapi</code> and
<code>uvicorn</code> in <code>pyproject.toml</code>.</li>
<li>Switch to nox for testing.</li>
</ul>
<h2>2.10 (2026-02-06)</h2>
<ul>
<li>Add <code>import-linter</code> group command, with
<code>import-linter lint</code> alias.</li>
<li>Add <code>import-linter explore</code> command.</li>
<li>Add <code>import-linter drawgraph</code> command.</li>
</ul>
<h2>2.9 (2025-12-11)</h2>
<ul>
<li>Support passing namespaces as root packages, not just portions.</li>
<li>Bugfix: support Python 3.14 syntax.</li>
</ul>
<h2>2.8 (2025-12-08)</h2>
<ul>
<li>Fix logo display bug on Windows (fall back to simpler heading)
<a
href="https://redirect.github.com/seddonym/import-linter/issues/309">seddonym/import-linter#309</a></li>
<li>Rewrite docs (and switch from Sphinx to mkdocs).</li>
</ul>
<h2>2.7 (2025-11-19)</h2>
<ul>
<li>Print using rich instead of click.</li>
<li>Remove pluggable Printer class.</li>
<li>Add ascii art logo.</li>
<li>Add progress animations when building graph and checking
contracts.</li>
</ul>
<h2>2.6 (2025-11-10)</h2>
<ul>
<li>Add <code>acyclic_siblings</code> contract type.</li>
<li>Add contract field <code>IntegerField</code>.</li>
<li>Drop support for Python 3.9.</li>
</ul>
<h2>2.5.2 (2025-10-09)</h2>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/seddonym/import-linter/commit/f544debbb0efe10092cd387032ea76b94a0acee0"><code>f544deb</code></a>
Release v2.13</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/ef5adf868962b073005b69abdd3ffb7b57457a2f"><code>ef5adf8</code></a>
Add more tests for drawgraph</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/73ee730c16c25b4f659dd4ecc3b7cf8ac78eddc6"><code>73ee730</code></a>
Upgrade grimp 3.14 -&gt; 3.15</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/6d0bffcd3255fb302e0e3a3371f585393f48e99d"><code>6d0bffc</code></a>
Add comma for thousands separator</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/8b0e7df5298f0b56af73cc0e9695d0fd4d828f3c"><code>8b0e7df</code></a>
Document module counts option</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/542e2c95155b96bdf33538481e0b33db9add7c02"><code>542e2c9</code></a>
Add a module count to the UI</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/ad48a961231620656267ee895bbbcb525a492d47"><code>ad48a96</code></a>
Release v2.12</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/f136ff0005d98e6a80692a705976b3e39f73919d"><code>f136ff0</code></a>
Run uv lock --upgrade (<a
href="https://redirect.github.com/seddonym/import-linter/issues/363">#363</a>)</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/5c174fce99038b18acffaa238566993c60df6468"><code>5c174fc</code></a>
Skip self-pairs in forbidden contracts so wildcards can include the
source (#...</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/c6ed24d68929500e743da7b896d4ed4fc5ac04db"><code>c6ed24d</code></a>
Bump urllib3 from 2.6.3 to 2.7.0 (<a
href="https://redirect.github.com/seddonym/import-linter/issues/356">#356</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/seddonym/import-linter/compare/v2.11...v2.13">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Body

Updates the requirements on [import-linter](https://github.com/seddonym/import-linter) to permit the latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/seddonym/import-linter/blob/main/docs/release_notes.md">import-linter's changelog</a>.</em></p>
<blockquote>
<h2>2.13 (2026-07-03)</h2>
<ul>
<li>Add module counts option to the explore UI and <code>drawgraph</code> command.</li>
</ul>
<h2>2.12 (2026-06-23)</h2>
<ul>
<li>Improve error message when root package is a single-file module.</li>
<li>Alert users with all unmatched ignored imports in the same run.</li>
<li>Allow overlapping modules in forbidden contracts.</li>
</ul>
<h2>2.11 (2026-03-06)</h2>
<ul>
<li>Add <code>--version</code> flag to <code>lint-imports</code> and <code>import-linter</code> commands.</li>
<li>Make <code>fastapi</code> and <code>uvicorn</code> optional via the <code>ui</code> extra (<code>pip install import-linter[ui]</code>).</li>
<li>Bugfix: fix back button navigation in explore command.</li>
<li>Provide lower limits for <code>fastapi</code> and <code>uvicorn</code> in <code>pyproject.toml</code>.</li>
<li>Switch to nox for testing.</li>
</ul>
<h2>2.10 (2026-02-06)</h2>
<ul>
<li>Add <code>import-linter</code> group command, with <code>import-linter lint</code> alias.</li>
<li>Add <code>import-linter explore</code> command.</li>
<li>Add <code>import-linter drawgraph</code> command.</li>
</ul>
<h2>2.9 (2025-12-11)</h2>
<ul>
<li>Support passing namespaces as root packages, not just portions.</li>
<li>Bugfix: support Python 3.14 syntax.</li>
</ul>
<h2>2.8 (2025-12-08)</h2>
<ul>
<li>Fix logo display bug on Windows (fall back to simpler heading)
<a href="https://redirect.github.com/seddonym/import-linter/issues/309">seddonym/import-linter#309</a></li>
<li>Rewrite docs (and switch from Sphinx to mkdocs).</li>
</ul>
<h2>2.7 (2025-11-19)</h2>
<ul>
<li>Print using rich instead of click.</li>
<li>Remove pluggable Printer class.</li>
<li>Add ascii art logo.</li>
<li>Add progress animations when building graph and checking contracts.</li>
</ul>
<h2>2.6 (2025-11-10)</h2>
<ul>
<li>Add <code>acyclic_siblings</code> contract type.</li>
<li>Add contract field <code>IntegerField</code>.</li>
<li>Drop support for Python 3.9.</li>
</ul>
<h2>2.5.2 (2025-10-09)</h2>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/seddonym/import-linter/commit/f544debbb0efe10092cd387032ea76b94a0acee0"><code>f544deb</code></a> Release v2.13</li>
<li><a href="https://github.com/seddonym/import-linter/commit/ef5adf868962b073005b69abdd3ffb7b57457a2f"><code>ef5adf8</code></a> Add more tests for drawgraph</li>
<li><a href="https://github.com/seddonym/import-linter/commit/73ee730c16c25b4f659dd4ecc3b7cf8ac78eddc6"><code>73ee730</code></a> Upgrade grimp 3.14 -&gt; 3.15</li>
<li><a href="https://github.com/seddonym/import-linter/commit/6d0bffcd3255fb302e0e3a3371f585393f48e99d"><code>6d0bffc</code></a> Add comma for thousands separator</li>
<li><a href="https://github.com/seddonym/import-linter/commit/8b0e7df5298f0b56af73cc0e9695d0fd4d828f3c"><code>8b0e7df</code></a> Document module counts option</li>
<li><a href="https://github.com/seddonym/import-linter/commit/542e2c95155b96bdf33538481e0b33db9add7c02"><code>542e2c9</code></a> Add a module count to the UI</li>
<li><a href="https://github.com/seddonym/import-linter/commit/ad48a961231620656267ee895bbbcb525a492d47"><code>ad48a96</code></a> Release v2.12</li>
<li><a href="https://github.com/seddonym/import-linter/commit/f136ff0005d98e6a80692a705976b3e39f73919d"><code>f136ff0</code></a> Run uv lock --upgrade (<a href="https://redirect.github.com/seddonym/import-linter/issues/363">#363</a>)</li>
<li><a href="https://github.com/seddonym/import-linter/commit/5c174fce99038b18acffaa238566993c60df6468"><code>5c174fc</code></a> Skip self-pairs in forbidden contracts so wildcards can include the source (#...</li>
<li><a href="https://github.com/seddonym/import-linter/commit/c6ed24d68929500e743da7b896d4ed4fc5ac04db"><code>c6ed24d</code></a> Bump urllib3 from 2.6.3 to 2.7.0 (<a href="https://redirect.github.com/seddonym/import-linter/issues/356">#356</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/seddonym/import-linter/compare/v2.11...v2.13">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---

## chore(deps-dev): update ruff requirement from >=0.15.18 to >=0.15.21 in /services/claw-interface (#2942)

- **SHA**: 949e820fb1b00d70db7401150ea2f4f711c8f401
- **作者**: dependabot[bot]
- **日期**: 2026-07-21T14:39:18Z
- **PR**: #2942

### Commit Message

```
chore(deps-dev): update ruff requirement from >=0.15.18 to >=0.15.21 in /services/claw-interface (#2942)

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to
permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/releases">ruff's
releases</a>.</em></p>
<blockquote>
<h2>0.15.21</h2>
<h2>Release Notes</h2>
<p>Released on 2026-07-09.</p>
<h3>Preview features</h3>
<ul>
<li>Add <code>--add-ignore</code> for adding <code>ruff:ignore</code>
comments (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26346">#26346</a>)</li>
<li>[<code>flake8-comprehensions</code>] Drop <code>C409</code> tuple
comprehension preview behavior (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25707">#25707</a>)</li>
<li>Avoid whitespace normalization when formatting comments (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26455">#26455</a>)</li>
<li>[<code>pyupgrade</code>] Lint and fix use of deprecated
<code>abc</code> decorators (<code>UP051</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26417">#26417</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Refine non-empty f-string detection (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26526">#26526</a>)</li>
<li>Detect syntax errors in individual notebook cells (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26419">#26419</a>)</li>
<li>[<code>flake8-implicit-str-concat</code>] Fix <code>ISC003</code>
autofix incorrectly stripping <code>+</code> from comments (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26554">#26554</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>flake8-executable</code>] Mark <code>EXE004</code> fix as
unsafe (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26033">#26033</a>)</li>
<li>[<code>flake8-pyi</code>] Mark <code>PYI061</code> fixes as unsafe
in Python files (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26533">#26533</a>)</li>
<li>[<code>pydocstyle</code>] Skip <code>overload-with-docstring</code>
in stub files (<code>D418</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26318">#26318</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Avoid per-token source index visitor calls (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26506">#26506</a>)</li>
<li>Cache parenthesized expression boundaries in the formatter (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26344">#26344</a>)</li>
<li>Improve performance of rendering edits in preview mode (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26565">#26565</a>)</li>
<li>Inline <code>fits_element</code> in formatter (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26429">#26429</a>)</li>
<li>Inline formatter printing hot paths (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26504">#26504</a>)</li>
<li>Lazily create builtin bindings (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26510">#26510</a>)</li>
<li>Skip empty trivia scans in the source indexer (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26507">#26507</a>)</li>
<li>Use ICF for macOS release builds (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25780">#25780</a>)</li>
</ul>
<h3>Formatter</h3>
<ul>
<li>Add <code>--extend-exclude</code> to <code>ruff format</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26372">#26372</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Add &quot;How does Ruff's import sorting compare to isort?&quot;
link to README (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26530">#26530</a>)</li>
<li>Fix Mozilla Firefox repository link in README (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26537">#26537</a>)</li>
<li>[<code>flake8-bandit</code>] Fix misleading docstring for
<code>mako-templates</code> (<code>S702</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26432">#26432</a>)</li>
<li>[<code>ruff</code>] Fix non-triggering example for
<code>if-key-in-dict-del</code> (<code>RUF051</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26433">#26433</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a
href="https://github.com/EkriirkE"><code>@​EkriirkE</code></a></li>
<li><a
href="https://github.com/tingerrr"><code>@​tingerrr</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's
changelog</a>.</em></p>
<blockquote>
<h2>0.15.21</h2>
<p>Released on 2026-07-09.</p>
<h3>Preview features</h3>
<ul>
<li>Add <code>--add-ignore</code> for adding <code>ruff:ignore</code>
comments (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26346">#26346</a>)</li>
<li>[<code>flake8-comprehensions</code>] Drop <code>C409</code> tuple
comprehension preview behavior (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25707">#25707</a>)</li>
<li>Avoid whitespace normalization when formatting comments (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26455">#26455</a>)</li>
<li>[<code>pyupgrade</code>] Lint and fix use of deprecated
<code>abc</code> decorators (<code>UP051</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26417">#26417</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Refine non-empty f-string detection (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26526">#26526</a>)</li>
<li>Detect syntax errors in individual notebook cells (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26419">#26419</a>)</li>
<li>[<code>flake8-implicit-str-concat</code>] Fix <code>ISC003</code>
autofix incorrectly stripping <code>+</code> from comments (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26554">#26554</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>flake8-executable</code>] Mark <code>EXE004</code> fix as
unsafe (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26033">#26033</a>)</li>
<li>[<code>flake8-pyi</code>] Mark <code>PYI061</code> fixes as unsafe
in Python files (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26533">#26533</a>)</li>
<li>[<code>pydocstyle</code>] Skip <code>overload-with-docstring</code>
in stub files (<code>D418</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26318">#26318</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Avoid per-token source index visitor calls (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26506">#26506</a>)</li>
<li>Cache parenthesized expression boundaries in the formatter (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26344">#26344</a>)</li>
<li>Improve performance of rendering edits in preview mode (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26565">#26565</a>)</li>
<li>Inline <code>fits_element</code> in formatter (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26429">#26429</a>)</li>
<li>Inline formatter printing hot paths (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26504">#26504</a>)</li>
<li>Lazily create builtin bindings (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26510">#26510</a>)</li>
<li>Skip empty trivia scans in the source indexer (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26507">#26507</a>)</li>
<li>Use ICF for macOS release builds (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25780">#25780</a>)</li>
</ul>
<h3>Formatter</h3>
<ul>
<li>Add <code>--extend-exclude</code> to <code>ruff format</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26372">#26372</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Add &quot;How does Ruff's import sorting compare to isort?&quot;
link to README (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26530">#26530</a>)</li>
<li>Fix Mozilla Firefox repository link in README (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26537">#26537</a>)</li>
<li>[<code>flake8-bandit</code>] Fix misleading docstring for
<code>mako-templates</code> (<code>S702</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26432">#26432</a>)</li>
<li>[<code>ruff</code>] Fix non-triggering example for
<code>if-key-in-dict-del</code> (<code>RUF051</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26433">#26433</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a
href="https://github.com/EkriirkE"><code>@​EkriirkE</code></a></li>
<li><a
href="https://github.com/tingerrr"><code>@​tingerrr</code></a></li>
<li><a
href="https://github.com/s-rigaud"><code>@​s-rigaud</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/astral-sh/ruff/commit/3e1f63645109e69f9bccc7be354c5ee4672fb8f3"><code>3e1f636</code></a>
Bump 0.15.21 (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26676">#26676</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/4059807d0c853fbb79110b1f5fd7212e1a532888"><code>4059807</code></a>
[ty] Infer metaclass-declared attributes on class instances (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26512">#26512</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/013e5d0ff64e6198af1770f8b71d35d1390def39"><code>013e5d0</code></a>
[ty] Use a dedicated project name type (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26665">#26665</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/7ad39ad5fae00226fbe6bc17a6f05d1746abbfde"><code>7ad39ad</code></a>
[ty] Avoid allocating decorated parameter names (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26666">#26666</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/c36f66207d6968dbbe1769bd50f80a4c02d17b57"><code>c36f662</code></a>
Improve performance of rendering edits in preview mode (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26565">#26565</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/ad264082c713ec6aad9191e5a6a8d342ed480a4b"><code>ad26408</code></a>
[ty] Gate membership narrowing on <code>__contains__</code> semantics
(<a
href="https://redirect.github.com/astral-sh/ruff/issues/25964">#25964</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/4594ca7366773b2a4b6d2ee08001d6e80d6e3eae"><code>4594ca7</code></a>
[ty] Add variant discriminators for <code>CodeGeneratorKind</code> (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26659">#26659</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/1af03da7b8cf1b37c344bef9ec85f9408ac3ff0e"><code>1af03da</code></a>
[ty] Pydantic: Fix float conversion in unions (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26655">#26655</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/a004a3620518d1b67f4d7aae584ab1dd156a0ef6"><code>a004a36</code></a>
[ty] Handle callable classes in solver (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26090">#26090</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/d8ef3b058704256431e50352301d5afb41ba606d"><code>d8ef3b0</code></a>
[ty] Parse all supported Google docstring sections. (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26653">#26653</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/astral-sh/ruff/compare/0.15.18...0.15.21">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Body

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's releases</a>.</em></p>
<blockquote>
<h2>0.15.21</h2>
<h2>Release Notes</h2>
<p>Released on 2026-07-09.</p>
<h3>Preview features</h3>
<ul>
<li>Add <code>--add-ignore</code> for adding <code>ruff:ignore</code> comments (<a href="https://redirect.github.com/astral-sh/ruff/pull/26346">#26346</a>)</li>
<li>[<code>flake8-comprehensions</code>] Drop <code>C409</code> tuple comprehension preview behavior (<a href="https://redirect.github.com/astral-sh/ruff/pull/25707">#25707</a>)</li>
<li>Avoid whitespace normalization when formatting comments (<a href="https://redirect.github.com/astral-sh/ruff/pull/26455">#26455</a>)</li>
<li>[<code>pyupgrade</code>] Lint and fix use of deprecated <code>abc</code> decorators (<code>UP051</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26417">#26417</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Refine non-empty f-string detection (<a href="https://redirect.github.com/astral-sh/ruff/pull/26526">#26526</a>)</li>
<li>Detect syntax errors in individual notebook cells (<a href="https://redirect.github.com/astral-sh/ruff/pull/26419">#26419</a>)</li>
<li>[<code>flake8-implicit-str-concat</code>] Fix <code>ISC003</code> autofix incorrectly stripping <code>+</code> from comments (<a href="https://redirect.github.com/astral-sh/ruff/pull/26554">#26554</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>flake8-executable</code>] Mark <code>EXE004</code> fix as unsafe (<a href="https://redirect.github.com/astral-sh/ruff/pull/26033">#26033</a>)</li>
<li>[<code>flake8-pyi</code>] Mark <code>PYI061</code> fixes as unsafe in Python files (<a href="https://redirect.github.com/astral-sh/ruff/pull/26533">#26533</a>)</li>
<li>[<code>pydocstyle</code>] Skip <code>overload-with-docstring</code> in stub files (<code>D418</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26318">#26318</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Avoid per-token source index visitor calls (<a href="https://redirect.github.com/astral-sh/ruff/pull/26506">#26506</a>)</li>
<li>Cache parenthesized expression boundaries in the formatter (<a href="https://redirect.github.com/astral-sh/ruff/pull/26344">#26344</a>)</li>
<li>Improve performance of rendering edits in preview mode (<a href="https://redirect.github.com/astral-sh/ruff/pull/26565">#26565</a>)</li>
<li>Inline <code>fits_element</code> in formatter (<a href="https://redirect.github.com/astral-sh/ruff/pull/26429">#26429</a>)</li>
<li>Inline formatter printing hot paths (<a href="https://redirect.github.com/astral-sh/ruff/pull/26504">#26504</a>)</li>
<li>Lazily create builtin bindings (<a href="https://redirect.github.com/astral-sh/ruff/pull/26510">#26510</a>)</li>
<li>Skip empty trivia scans in the source indexer (<a href="https://redirect.github.com/astral-sh/ruff/pull/26507">#26507</a>)</li>
<li>Use ICF for macOS release builds (<a href="https://redirect.github.com/astral-sh/ruff/pull/25780">#25780</a>)</li>
</ul>
<h3>Formatter</h3>
<ul>
<li>Add <code>--extend-exclude</code> to <code>ruff format</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/26372">#26372</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Add &quot;How does Ruff's import sorting compare to isort?&quot; link to README (<a href="https://redirect.github.com/astral-sh/ruff/pull/26530">#26530</a>)</li>
<li>Fix Mozilla Firefox repository link in README (<a href="https://redirect.github.com/astral-sh/ruff/pull/26537">#26537</a>)</li>
<li>[<code>flake8-bandit</code>] Fix misleading docstring for <code>mako-templates</code> (<code>S702</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26432">#26432</a>)</li>
<li>[<code>ruff</code>] Fix non-triggering example for <code>if-key-in-dict-del</code> (<code>RUF051</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26433">#26433</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/EkriirkE"><code>@​EkriirkE</code></a></li>
<li><a href="https://github.com/tingerrr"><code>@​tingerrr</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
<blockquote>
<h2>0.15.21</h2>
<p>Released on 2026-07-09.</p>
<h3>Preview features</h3>
<ul>
<li>Add <code>--add-ignore</code> for adding <code>ruff:ignore</code> comments (<a href="https://redirect.github.com/astral-sh/ruff/pull/26346">#26346</a>)</li>
<li>[<code>flake8-comprehensions</code>] Drop <code>C409</code> tuple comprehension preview behavior (<a href="https://redirect.github.com/astral-sh/ruff/pull/25707">#25707</a>)</li>
<li>Avoid whitespace normalization when formatting comments (<a href="https://redirect.github.com/astral-sh/ruff/pull/26455">#26455</a>)</li>
<li>[<code>pyupgrade</code>] Lint and fix use of deprecated <code>abc</code> decorators (<code>UP051</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26417">#26417</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Refine non-empty f-string detection (<a href="https://redirect.github.com/astral-sh/ruff/pull/26526">#26526</a>)</li>
<li>Detect syntax errors in individual notebook cells (<a href="https://redirect.github.com/astral-sh/ruff/pull/26419">#26419</a>)</li>
<li>[<code>flake8-implicit-str-concat</code>] Fix <code>ISC003</code> autofix incorrectly stripping <code>+</code> from comments (<a href="https://redirect.github.com/astral-sh/ruff/pull/26554">#26554</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>flake8-executable</code>] Mark <code>EXE004</code> fix as unsafe (<a href="https://redirect.github.com/astral-sh/ruff/pull/26033">#26033</a>)</li>
<li>[<code>flake8-pyi</code>] Mark <code>PYI061</code> fixes as unsafe in Python files (<a href="https://redirect.github.com/astral-sh/ruff/pull/26533">#26533</a>)</li>
<li>[<code>pydocstyle</code>] Skip <code>overload-with-docstring</code> in stub files (<code>D418</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26318">#26318</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Avoid per-token source index visitor calls (<a href="https://redirect.github.com/astral-sh/ruff/pull/26506">#26506</a>)</li>
<li>Cache parenthesized expression boundaries in the formatter (<a href="https://redirect.github.com/astral-sh/ruff/pull/26344">#26344</a>)</li>
<li>Improve performance of rendering edits in preview mode (<a href="https://redirect.github.com/astral-sh/ruff/pull/26565">#26565</a>)</li>
<li>Inline <code>fits_element</code> in formatter (<a href="https://redirect.github.com/astral-sh/ruff/pull/26429">#26429</a>)</li>
<li>Inline formatter printing hot paths (<a href="https://redirect.github.com/astral-sh/ruff/pull/26504">#26504</a>)</li>
<li>Lazily create builtin bindings (<a href="https://redirect.github.com/astral-sh/ruff/pull/26510">#26510</a>)</li>
<li>Skip empty trivia scans in the source indexer (<a href="https://redirect.github.com/astral-sh/ruff/pull/26507">#26507</a>)</li>
<li>Use ICF for macOS release builds (<a href="https://redirect.github.com/astral-sh/ruff/pull/25780">#25780</a>)</li>
</ul>
<h3>Formatter</h3>
<ul>
<li>Add <code>--extend-exclude</code> to <code>ruff format</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/26372">#26372</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Add &quot;How does Ruff's import sorting compare to isort?&quot; link to README (<a href="https://redirect.github.com/astral-sh/ruff/pull/26530">#26530</a>)</li>
<li>Fix Mozilla Firefox repository link in README (<a href="https://redirect.github.com/astral-sh/ruff/pull/26537">#26537</a>)</li>
<li>[<code>flake8-bandit</code>] Fix misleading docstring for <code>mako-templates</code> (<code>S702</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26432">#26432</a>)</li>
<li>[<code>ruff</code>] Fix non-triggering example for <code>if-key-in-dict-del</code> (<code>RUF051</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26433">#26433</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/EkriirkE"><code>@​EkriirkE</code></a></li>
<li><a href="https://github.com/tingerrr"><code>@​tingerrr</code></a></li>
<li><a href="https://github.com/s-rigaud"><code>@​s-rigaud</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/astral-sh/ruff/commit/3e1f63645109e69f9bccc7be354c5ee4672fb8f3"><code>3e1f636</code></a> Bump 0.15.21 (<a href="https://redirect.github.com/astral-sh/ruff/issues/26676">#26676</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/4059807d0c853fbb79110b1f5fd7212e1a532888"><code>4059807</code></a> [ty] Infer metaclass-declared attributes on class instances (<a href="https://redirect.github.com/astral-sh/ruff/issues/26512">#26512</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/013e5d0ff64e6198af1770f8b71d35d1390def39"><code>013e5d0</code></a> [ty] Use a dedicated project name type (<a href="https://redirect.github.com/astral-sh/ruff/issues/26665">#26665</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/7ad39ad5fae00226fbe6bc17a6f05d1746abbfde"><code>7ad39ad</code></a> [ty] Avoid allocating decorated parameter names (<a href="https://redirect.github.com/astral-sh/ruff/issues/26666">#26666</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/c36f66207d6968dbbe1769bd50f80a4c02d17b57"><code>c36f662</code></a> Improve performance of rendering edits in preview mode (<a href="https://redirect.github.com/astral-sh/ruff/issues/26565">#26565</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/ad264082c713ec6aad9191e5a6a8d342ed480a4b"><code>ad26408</code></a> [ty] Gate membership narrowing on <code>__contains__</code> semantics (<a href="https://redirect.github.com/astral-sh/ruff/issues/25964">#25964</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/4594ca7366773b2a4b6d2ee08001d6e80d6e3eae"><code>4594ca7</code></a> [ty] Add variant discriminators for <code>CodeGeneratorKind</code> (<a href="https://redirect.github.com/astral-sh/ruff/issues/26659">#26659</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/1af03da7b8cf1b37c344bef9ec85f9408ac3ff0e"><code>1af03da</code></a> [ty] Pydantic: Fix float conversion in unions (<a href="https://redirect.github.com/astral-sh/ruff/issues/26655">#26655</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/a004a3620518d1b67f4d7aae584ab1dd156a0ef6"><code>a004a36</code></a> [ty] Handle callable classes in solver (<a href="https://redirect.github.com/astral-sh/ruff/issues/26090">#26090</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/d8ef3b058704256431e50352301d5afb41ba606d"><code>d8ef3b0</code></a> [ty] Parse all supported Google docstring sections. (<a href="https://redirect.github.com/astral-sh/ruff/issues/26653">#26653</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.15.18...0.15.21">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---

## chore(deps): update websockets requirement from >=16.0 to >=16.1 in /services/claw-interface (#2941)

- **SHA**: f59fea0e52ae652f776c70151c8825c3e0e3ce07
- **作者**: dependabot[bot]
- **日期**: 2026-07-21T14:39:00Z
- **PR**: #2941

### Commit Message

```
chore(deps): update websockets requirement from >=16.0 to >=16.1 in /services/claw-interface (#2941)

Updates the requirements on
[websockets](https://github.com/python-websockets/websockets) to permit
the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/python-websockets/websockets/releases">websockets's
releases</a>.</em></p>
<blockquote>
<h2>16.1</h2>
<p>See <a
href="https://websockets.readthedocs.io/en/stable/project/changelog.html">https://websockets.readthedocs.io/en/stable/project/changelog.html</a>
for details.</p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/python-websockets/websockets/commit/4df6f90d0724640275157a0fa784c234d309af82"><code>4df6f90</code></a>
Release version 16.1.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/7c69ecac884abd8d70a9bcc22ef0bf0b950101d1"><code>7c69eca</code></a>
Increase timeout for building wheels.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/493864e58462138345675d9875e096c40072dd11"><code>493864e</code></a>
Complete and review changelog.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/73ff538bd7df88a08e982cd64a2ccbdfee74de6d"><code>73ff538</code></a>
Temporarily remove the trio implementation (again).</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/77f7d71870544e09e35795a8a6f48005abcb2a4b"><code>77f7d71</code></a>
Shorten changelog and docstring for previous commit.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/84859e19dd2ab3d0d482cd251518872dd604a302"><code>84859e1</code></a>
Add text argument to broadcast() to force the frame type</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/1a38f5a55b82b2883cd4e0ee09c57491e85c969c"><code>1a38f5a</code></a>
Document research on removing a workaround.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/99431eea503c70b57412fbeda43481d3081d6037"><code>99431ee</code></a>
Apply code style to docs/conf.py.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/bf97b98b03ee0fd278a782754592bf49b470589b"><code>bf97b98</code></a>
Fix typos in tests.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/21a3418cd136dbf416723ef8e71a34403e57b180"><code>21a3418</code></a>
Fix typos in comments</li>
<li>Additional commits viewable in <a
href="https://github.com/python-websockets/websockets/compare/16.0...16.1">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Body

Updates the requirements on [websockets](https://github.com/python-websockets/websockets) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/python-websockets/websockets/releases">websockets's releases</a>.</em></p>
<blockquote>
<h2>16.1</h2>
<p>See <a href="https://websockets.readthedocs.io/en/stable/project/changelog.html">https://websockets.readthedocs.io/en/stable/project/changelog.html</a> for details.</p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/python-websockets/websockets/commit/4df6f90d0724640275157a0fa784c234d309af82"><code>4df6f90</code></a> Release version 16.1.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/7c69ecac884abd8d70a9bcc22ef0bf0b950101d1"><code>7c69eca</code></a> Increase timeout for building wheels.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/493864e58462138345675d9875e096c40072dd11"><code>493864e</code></a> Complete and review changelog.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/73ff538bd7df88a08e982cd64a2ccbdfee74de6d"><code>73ff538</code></a> Temporarily remove the trio implementation (again).</li>
<li><a href="https://github.com/python-websockets/websockets/commit/77f7d71870544e09e35795a8a6f48005abcb2a4b"><code>77f7d71</code></a> Shorten changelog and docstring for previous commit.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/84859e19dd2ab3d0d482cd251518872dd604a302"><code>84859e1</code></a> Add text argument to broadcast() to force the frame type</li>
<li><a href="https://github.com/python-websockets/websockets/commit/1a38f5a55b82b2883cd4e0ee09c57491e85c969c"><code>1a38f5a</code></a> Document research on removing a workaround.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/99431eea503c70b57412fbeda43481d3081d6037"><code>99431ee</code></a> Apply code style to docs/conf.py.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/bf97b98b03ee0fd278a782754592bf49b470589b"><code>bf97b98</code></a> Fix typos in tests.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/21a3418cd136dbf416723ef8e71a34403e57b180"><code>21a3418</code></a> Fix typos in comments</li>
<li>Additional commits viewable in <a href="https://github.com/python-websockets/websockets/compare/16.0...16.1">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---

## docs(chat): record post-deploy staging measurements for the streaming fix (#2991)

- **SHA**: 5f96e6c7800c76c176fa62fae9c774d742eb15ca
- **作者**: Chris@ZooClaw
- **日期**: 2026-07-21T14:07:26Z
- **PR**: #2991

### Commit Message

```
docs(chat): record post-deploy staging measurements for the streaming fix (#2991)

## Summary

补上 #2989 唯一遗留的未测量项：**打字机跑起来后，每帧重建整个消息数组在生产构建下到底有多贵。**

结论：**不构成问题，spec 里的 P1 重构不需要立即做。**

## 复测方法

#2989 合并、staging 自动部署（`4dde531c9`）后，用 CDP
在**生产构建**下对两个界面各跑一轮完整问答。两个界面渲染链不同，必须分开测——只有 thread 走 `onPostDeleted`
fanout：

- `/chat` → channel store → `useMmTypewriter`
- `/chat/<computerId>/<agentId>/<sessionId>` → `useLiveThread` 自有 state
→ `useMmTypewriter`

## 结果

| 指标 | thread（6 条消息） | /chat（32 条消息） |
|---|---|---|
| DOM 更新间隔 p50 / p95 | 16.8 / 49.4 ms | 21.7 / 47.8 ms |
| 每次增量均值 | 3.0 字符 | 3.9 字符 |
| ≤3 字符细粒度更新占比 | 96% | 95% |
| 帧间隔 p50 / p95 | 16.7 / **17.1** ms | 16.7 / **33.3** ms |
| 帧 >33ms 占比 | **0%** | 8.5% |
| **Long task** | **0** | **3（合计 176ms / 131s）** |
| 助手消息中标记出现次数 | **1** | **1** |

**同为 32 条消息的场景，dev 构建是 135 个 long task / 9961ms，生产构建是 3 个 / 176ms——相差约
56 倍。** 当初让人担心的那组数字基本全是 dev 构建开销。

"开销随线程长度增长"的规律确实存在（6 条消息 0 个 → 32 条消息 3 个），但量级完全可接受。P1 降级为长线程场景的长期优化。

两个界面的助手消息中标记均出现 **1 次**，确认重复展示在 thread 界面也已消除——那正是 Codex review 指出的 P1
影响面，也是最初发现该 bug 的界面。

## 顺带记录了两个测量陷阱

写进文档是因为下次复测很容易再踩：

1. **body 级出现次数计数不可用。** prompt 本身包含探针标记，用户消息气泡里也有一份，所以基线是 2 不是 1。必须统计
`genclaw-bot-message` 元素内的次数。
2. **按位置索引做 per-message keying 会误报。** 用 `bot#N/total` 作
key，列表长度一变（preview 被删、final 加入）索引就指向不同消息，于是报出 -3124 / -2965
这种"巨幅回退"。实际是假象。

剩下的小幅收缩（-1 到 -24）是 markdown 增量渲染固有现象：`**粗体` 未闭合时按字面显示，闭合后渲染成
`<strong>`、4 个星号从 textContent 消失。已验证末条消息有 7 处 `<strong>` 而字面 `**` 为
0。与打字机无关，改动前同样存在。


## 测量脚本已入库

`scripts/measure-streaming-smoothness.mjs` —— 这套测量不再只存在于我的
scratchpad，下次复测直接跑：

```
bash scripts/open-chrome-debug-profile.sh --env staging   # 一次，然后登录
node scripts/measure-streaming-smoothness.mjs --url https://ecap.gensmo.nosay.live/chat
node scripts/measure-streaming-smoothness.mjs --url <session-thread-url> --label thread
```

基于已有的 `scripts/cdp/lib.mjs`（Playwright `connectOverCDP`）写的，没有重复实现裸
CDP。原始 JSON 落在 gitignored 的 `.screenshots/`。

**上面那三个测量陷阱都已经修在脚本里**，不是写在注释里让人自己小心 —— 每一个当初都先给出了一个看起来完全合理的错误数字：

- 全文计数 → 改为只统计助手气泡
- 统计所有助手气泡 → 改为只统计**本轮新增**的气泡（同会话重复跑会累计历史）
- 位置索引 keying → 改为按消息开头文本 keying（列表长度一变，索引就指向别的消息）

脚本还会在报告末尾提示：小幅 shrink 通常是 markdown 标记闭合而非文字回退，先看 innerHTML 再报 bug。

已对 staging 端到端实跑两轮验证（第二轮专门确认 turn-scoping 修复后报 1）。

## Test plan

- [x] staging 生产构建，两个界面各一轮完整问答（thread 94s / chat 131s）
- [x] 新增脚本已对 staging 端到端实跑 2 轮（`/chat`，75s + 90s 窗口）
- [x] `node --check` 语法校验 + 缺参数时正确报错
- [x] 无生产代码变更（仅 `scripts/` + `docs/`）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

补上 #2989 唯一遗留的未测量项：**打字机跑起来后，每帧重建整个消息数组在生产构建下到底有多贵。**

结论：**不构成问题，spec 里的 P1 重构不需要立即做。**

## 复测方法

#2989 合并、staging 自动部署（`4dde531c9`）后，用 CDP 在**生产构建**下对两个界面各跑一轮完整问答。两个界面渲染链不同，必须分开测——只有 thread 走 `onPostDeleted` fanout：

- `/chat` → channel store → `useMmTypewriter`
- `/chat/<computerId>/<agentId>/<sessionId>` → `useLiveThread` 自有 state → `useMmTypewriter`

## 结果

| 指标 | thread（6 条消息） | /chat（32 条消息） |
|---|---|---|
| DOM 更新间隔 p50 / p95 | 16.8 / 49.4 ms | 21.7 / 47.8 ms |
| 每次增量均值 | 3.0 字符 | 3.9 字符 |
| ≤3 字符细粒度更新占比 | 96% | 95% |
| 帧间隔 p50 / p95 | 16.7 / **17.1** ms | 16.7 / **33.3** ms |
| 帧 >33ms 占比 | **0%** | 8.5% |
| **Long task** | **0** | **3（合计 176ms / 131s）** |
| 助手消息中标记出现次数 | **1** | **1** |

**同为 32 条消息的场景，dev 构建是 135 个 long task / 9961ms，生产构建是 3 个 / 176ms——相差约 56 倍。** 当初让人担心的那组数字基本全是 dev 构建开销。

"开销随线程长度增长"的规律确实存在（6 条消息 0 个 → 32 条消息 3 个），但量级完全可接受。P1 降级为长线程场景的长期优化。

两个界面的助手消息中标记均出现 **1 次**，确认重复展示在 thread 界面也已消除——那正是 Codex review 指出的 P1 影响面，也是最初发现该 bug 的界面。

## 顺带记录了两个测量陷阱

写进文档是因为下次复测很容易再踩：

1. **body 级出现次数计数不可用。** prompt 本身包含探针标记，用户消息气泡里也有一份，所以基线是 2 不是 1。必须统计 `genclaw-bot-message` 元素内的次数。
2. **按位置索引做 per-message keying 会误报。** 用 `bot#N/total` 作 key，列表长度一变（preview 被删、final 加入）索引就指向不同消息，于是报出 -3124 / -2965 这种"巨幅回退"。实际是假象。

剩下的小幅收缩（-1 到 -24）是 markdown 增量渲染固有现象：`**粗体` 未闭合时按字面显示，闭合后渲染成 `<strong>`、4 个星号从 textContent 消失。已验证末条消息有 7 处 `<strong>` 而字面 `**` 为 0。与打字机无关，改动前同样存在。


## 测量脚本已入库

`scripts/measure-streaming-smoothness.mjs` —— 这套测量不再只存在于我的 scratchpad，下次复测直接跑：

```
bash scripts/open-chrome-debug-profile.sh --env staging   # 一次，然后登录
node scripts/measure-streaming-smoothness.mjs --url https://ecap.gensmo.nosay.live/chat
node scripts/measure-streaming-smoothness.mjs --url <session-thread-url> --label thread
```

基于已有的 `scripts/cdp/lib.mjs`（Playwright `connectOverCDP`）写的，没有重复实现裸 CDP。原始 JSON 落在 gitignored 的 `.screenshots/`。

**上面那三个测量陷阱都已经修在脚本里**，不是写在注释里让人自己小心 —— 每一个当初都先给出了一个看起来完全合理的错误数字：

- 全文计数 → 改为只统计助手气泡
- 统计所有助手气泡 → 改为只统计**本轮新增**的气泡（同会话重复跑会累计历史）
- 位置索引 keying → 改为按消息开头文本 keying（列表长度一变，索引就指向别的消息）

脚本还会在报告末尾提示：小幅 shrink 通常是 markdown 标记闭合而非文字回退，先看 innerHTML 再报 bug。

已对 staging 端到端实跑两轮验证（第二轮专门确认 turn-scoping 修复后报 1）。

## Test plan

- [x] staging 生产构建，两个界面各一轮完整问答（thread 94s / chat 131s）
- [x] 新增脚本已对 staging 端到端实跑 2 轮（`/chat`，75s + 90s 窗口）
- [x] `node --check` 语法校验 + 缺参数时正确报错
- [x] 无生产代码变更（仅 `scripts/` + `docs/`）

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## refactor(web): render specialist cards via @zooclaw/chat-ui (#2996)

- **SHA**: a9a182667c48a9f4f7313b616957bfbe09b49316
- **作者**: bill-srp
- **日期**: 2026-07-21T12:16:54Z
- **PR**: #2996

### Commit Message

```
refactor(web): render specialist cards via @zooclaw/chat-ui (#2996)

## Summary

PR **B** of the specialist-card extraction — the **app "replace"** step.
Rewrites `SpecialistCardSlot` to consume the `@zooclaw/chat-ui` cards
merged in PR A (#2994). Completes the slice: docs #2992 → package
extract #2994 → this replace.

Spec/plan:
`docs/superpowers/plans/2026-07-21-chat-ui-specialist-card-extraction.md`
(PR B = Tasks 4–6).

## What changed (all `web/app`)

- **`SpecialistCardSlot.tsx`** → now imports `SpecialistOpenCard` /
`SpecialistConsentCard` / `humanizeAgentId` from `@zooclaw/chat-ui`. It
stays the **resolver**: agent-identity
(`getAgentAvatarUrl`/`getAgentDisplayName`), i18n, kind dispatch, and
the degradation ladder. It extracts labels **once**
(`extractQuotedLabels`) and, for the consent path, passes `labels` +
`body={<MarkdownContent … variant="compact" suppressSpecialistCards />}`
into the package card. **Same default export + prop signature**, so
`MarkdownContent` (its only caller, via dynamic import) is untouched.
- **Preservation detail:** the consent **body is `variant="compact"`**
(byte-identical to the card's prior internal render); the slot's own
`variant` drives *only* the degradation fallback (empty labels → plain
markdown). This was the docs-review P1 — the code here matches it.
- **Deleted** (moved to the package in PR A): `SpecialistOpenCard.tsx`,
`SpecialistConsentCard.tsx`, and their two unit specs
(`SpecialistOpenCard.unit.spec.tsx`,
`SpecialistConsentCard.unit.spec.tsx`). `extract-quoted-labels.ts` stays
app-side.

## Test plan

- [x] `pnpm exec tsc --noEmit` (whole app) — clean.
- [x] Full unit suite: **526 files / 7115 tests pass** (1 skipped, 1
todo).
- [x] **4 protected specs pass UNCHANGED**:
`MarkdownContent.unit.spec.tsx`, `MarkdownContent-extras.unit.spec.tsx`,
`parse-markdown-segments.unit.spec.ts`,
`render-markdown-to-html.unit.spec.ts` — they drive `SpecialistCardSlot`
through the full markdown path.
- [x] Coverage ratchet holds: **stmts 88.29 / branches 81.65 / funcs 87
/ lines 90.59** (thresholds 83 / 75 / 81 / 85).
- [x] `verify-web.sh` (guards + tsc + vitest + eslint) green.
- [~] Browser check: specialist cards render from `<kind>@<agentId>`
markdown fences, which the local mock backend doesn't emit, so a live
specialist render can't be exercised in the mock. Runtime integration is
covered by CI `web-build-check` (`next build`), the byte-identical
package markup (verified in PR A), and the passing `MarkdownContent`
integration specs that drive the slot.
- [ ] CI `web-build-check` runs on this PR.

`web/packages/chat-ui` and `docs` untouched. Scope: `web/app` only (1
rewrite + 4 deletions).
```

### PR Body

## Summary

PR **B** of the specialist-card extraction — the **app "replace"** step. Rewrites `SpecialistCardSlot` to consume the `@zooclaw/chat-ui` cards merged in PR A (#2994). Completes the slice: docs #2992 → package extract #2994 → this replace.

Spec/plan: `docs/superpowers/plans/2026-07-21-chat-ui-specialist-card-extraction.md` (PR B = Tasks 4–6).

## What changed (all `web/app`)

- **`SpecialistCardSlot.tsx`** → now imports `SpecialistOpenCard` / `SpecialistConsentCard` / `humanizeAgentId` from `@zooclaw/chat-ui`. It stays the **resolver**: agent-identity (`getAgentAvatarUrl`/`getAgentDisplayName`), i18n, kind dispatch, and the degradation ladder. It extracts labels **once** (`extractQuotedLabels`) and, for the consent path, passes `labels` + `body={<MarkdownContent … variant="compact" suppressSpecialistCards />}` into the package card. **Same default export + prop signature**, so `MarkdownContent` (its only caller, via dynamic import) is untouched.
- **Preservation detail:** the consent **body is `variant="compact"`** (byte-identical to the card's prior internal render); the slot's own `variant` drives *only* the degradation fallback (empty labels → plain markdown). This was the docs-review P1 — the code here matches it.
- **Deleted** (moved to the package in PR A): `SpecialistOpenCard.tsx`, `SpecialistConsentCard.tsx`, and their two unit specs (`SpecialistOpenCard.unit.spec.tsx`, `SpecialistConsentCard.unit.spec.tsx`). `extract-quoted-labels.ts` stays app-side.

## Test plan

- [x] `pnpm exec tsc --noEmit` (whole app) — clean.
- [x] Full unit suite: **526 files / 7115 tests pass** (1 skipped, 1 todo).
- [x] **4 protected specs pass UNCHANGED**: `MarkdownContent.unit.spec.tsx`, `MarkdownContent-extras.unit.spec.tsx`, `parse-markdown-segments.unit.spec.ts`, `render-markdown-to-html.unit.spec.ts` — they drive `SpecialistCardSlot` through the full markdown path.
- [x] Coverage ratchet holds: **stmts 88.29 / branches 81.65 / funcs 87 / lines 90.59** (thresholds 83 / 75 / 81 / 85).
- [x] `verify-web.sh` (guards + tsc + vitest + eslint) green.
- [~] Browser check: specialist cards render from `<kind>@<agentId>` markdown fences, which the local mock backend doesn't emit, so a live specialist render can't be exercised in the mock. Runtime integration is covered by CI `web-build-check` (`next build`), the byte-identical package markup (verified in PR A), and the passing `MarkdownContent` integration specs that drive the slot.
- [ ] CI `web-build-check` runs on this PR.

`web/packages/chat-ui` and `docs` untouched. Scope: `web/app` only (1 rewrite + 4 deletions).


---

## refactor(chat): consume chat-ui ModelPicker in unified composer (#2995)

- **SHA**: 6734c37ace29695af14c030e85d8aa47b967bee8
- **作者**: bill-srp
- **日期**: 2026-07-21T12:10:57Z
- **PR**: #2995

### Commit Message

```
refactor(chat): consume chat-ui ModelPicker in unified composer (#2995)

## Summary

Wires the app's shared composer to consume `@zooclaw/chat-ui`'s
`ModelPicker` (relocated there in #2993) and **deletes the app-local
`ComposerModelMenu`** + its CSS module. Both the New Chat and session
chat surfaces render through the same `UnifiedChatComposer`, so this
lands on both at once.

This is the code-shrink half of the Model-menu slice of ECA-1288 — net
**-456 lines** (`ComposerModelMenu.tsx`, its `.module.css`, and its two
unit/CSS test files removed).

### What changed

- `UnifiedChatComposer` now renders `<ModelPicker>` with a 1:1 prop
mapping (`selectModel` -> `onValueChange`, `savedModel` -> `value`,
`loading`/`saving`/`managed`/`error`/`onRetry` pass through, `rootSide`
-> `side`). Orchestration — the `useAgentSettingsQuery`, `saveModel`,
`RestartPromptModal`, and the model-equality guard — stays app-side,
unchanged.
- `composer-model-presentations.ts` becomes the app-side normalizer
producing `ModelPickerOption[]` (`iconSrc` from the app's own
`/model-providers/*.png` assets, `default` badge, `monochromeIcon` for
openai/glm). `resolveComposerSelectedModel` / `normalizeAgentModelId`
are kept.
- Deleted `ComposerModelMenu.tsx` + `ComposerModelMenu.module.css` +
their unit/CSS tests. The app's `@zooclaw/chat-ui` test mock gains a
`ModelPicker` stand-in, and the `UnifiedChatComposer` / `GenClawInput`
specs now assert the **wiring** through that mock — model-menu rendering
itself is covered by chat-ui's own `ModelPicker` suite.

### Behavior change (one rare edge)

When `settings.model` is **not** present in `settings.available_models`,
the old menu synthesized a display-only trigger label for the saved
model; `ModelPicker` instead shows the first available model (or `No
models available`). The new behavior never presents an unavailable model
as selected. If exact preservation is wanted, the clean home is a small
optional `selectedOption` prop on chat-ui's `ModelPicker` (follow-up) —
not app-local presentation logic.

## Related

- Part of
[ECA-1288](https://linear.app/srpone/issue/ECA-1288/separate-shared-composer-presentation-from-application-orchestration)
— separate shared composer presentation from application orchestration
- Builds on #2993 (ModelPicker relocation to `@zooclaw/chat-ui`)

## Test plan

- [x] `bash scripts/verify-web.sh` — governance guards + tsc + Vitest
(526 files / 7117 passed) + ESLint + knip, all green
- [x] Grep: zero `ComposerModelMenu` / `ComposerModelMenu.module.css` /
legacy `composer-model-*` test-id references left in `web/app`
- [ ] Visual eyeball of the model picker on New Chat and inside a
session (trigger, dropdown, hover detail panel, managed/loading/error
states)
```

### PR Body

## Summary

Wires the app's shared composer to consume `@zooclaw/chat-ui`'s `ModelPicker` (relocated there in #2993) and **deletes the app-local `ComposerModelMenu`** + its CSS module. Both the New Chat and session chat surfaces render through the same `UnifiedChatComposer`, so this lands on both at once.

This is the code-shrink half of the Model-menu slice of ECA-1288 — net **-456 lines** (`ComposerModelMenu.tsx`, its `.module.css`, and its two unit/CSS test files removed).

### What changed

- `UnifiedChatComposer` now renders `<ModelPicker>` with a 1:1 prop mapping (`selectModel` -> `onValueChange`, `savedModel` -> `value`, `loading`/`saving`/`managed`/`error`/`onRetry` pass through, `rootSide` -> `side`). Orchestration — the `useAgentSettingsQuery`, `saveModel`, `RestartPromptModal`, and the model-equality guard — stays app-side, unchanged.
- `composer-model-presentations.ts` becomes the app-side normalizer producing `ModelPickerOption[]` (`iconSrc` from the app's own `/model-providers/*.png` assets, `default` badge, `monochromeIcon` for openai/glm). `resolveComposerSelectedModel` / `normalizeAgentModelId` are kept.
- Deleted `ComposerModelMenu.tsx` + `ComposerModelMenu.module.css` + their unit/CSS tests. The app's `@zooclaw/chat-ui` test mock gains a `ModelPicker` stand-in, and the `UnifiedChatComposer` / `GenClawInput` specs now assert the **wiring** through that mock — model-menu rendering itself is covered by chat-ui's own `ModelPicker` suite.

### Behavior change (one rare edge)

When `settings.model` is **not** present in `settings.available_models`, the old menu synthesized a display-only trigger label for the saved model; `ModelPicker` instead shows the first available model (or `No models available`). The new behavior never presents an unavailable model as selected. If exact preservation is wanted, the clean home is a small optional `selectedOption` prop on chat-ui's `ModelPicker` (follow-up) — not app-local presentation logic.

## Related

- Part of [ECA-1288](https://linear.app/srpone/issue/ECA-1288/separate-shared-composer-presentation-from-application-orchestration) — separate shared composer presentation from application orchestration
- Builds on #2993 (ModelPicker relocation to `@zooclaw/chat-ui`)

## Test plan

- [x] `bash scripts/verify-web.sh` — governance guards + tsc + Vitest (526 files / 7117 passed) + ESLint + knip, all green
- [x] Grep: zero `ComposerModelMenu` / `ComposerModelMenu.module.css` / legacy `composer-model-*` test-id references left in `web/app`
- [ ] Visual eyeball of the model picker on New Chat and inside a session (trigger, dropdown, hover detail panel, managed/loading/error states)


---

## refactor(chat-ui): extract specialist cards into @zooclaw/chat-ui (#2994)

- **SHA**: 7b3576679d7c0d76198129d5c74fba51804c78ee
- **作者**: bill-srp
- **日期**: 2026-07-21T12:00:14Z
- **PR**: #2994

### Commit Message

```
refactor(chat-ui): extract specialist cards into @zooclaw/chat-ui (#2994)

## Summary

PR **A** of the specialist-card extraction — the **package-only,
additive** step. Moves the two specialist card renderers into
`@zooclaw/chat-ui` as pure, prop-driven components. **No `web/app` or
docs changes**, so nothing consumes these yet — the app switch happens
in PR B.

Spec/plan:
`docs/superpowers/plans/2026-07-21-chat-ui-specialist-card-extraction.md`
(PR A = Tasks 1–3), merged via #2992.

## What changed (all `web/packages/chat-ui`)

- **New `src/specialist/`**: `SpecialistOpenCard.tsx` (+ the pure
`humanizeAgentId` helper), `SpecialistConsentCard.tsx`, and a barrel.
- **`SpecialistOpenCard`** — moved verbatim (only change: dropped `'use
client'`, exported its props interface). Already fully prop-driven —
every value pre-resolved by the caller.
- **`SpecialistConsentCard` — one deliberate contract change**: takes
**`labels: string[]` + `body: React.ReactNode`** instead of `markdown:
string`. It no longer imports `MarkdownContent` or
`extractQuotedLabels`; the resolver (PR B's `SpecialistCardSlot`)
extracts labels and renders the markdown body app-side, passing both in.
This is what lets the card live in a package that can't import the app
markdown pipeline — the "recursion" becomes a standard body slot. The
consent body will be rendered by the app at `variant="compact"`
(byte-identical to today).
- **Root barrel**: exports `SpecialistOpenCard`,
`SpecialistConsentCard`, `humanizeAgentId`, and the two prop types (all
new names — no collisions). `module-structure.test.ts` extended to pin
the new root exports.

## Preservation

- Markup, classNames, and `data-testid`s move byte-for-byte:
`specialist-open-card` (+ `data-agent-id`),
`specialist-consent-card-{neutral|destructive}`,
`specialist-consent-button-{label}`, `specialist-consent-chosen`; the
`✓` chosen prefix, `⚠️` destructive banner, and consumed-state disabling
are unchanged.
- No new dependencies (`@heroicons/react` already present). `'use
client'` dropped to match sibling package convention.

## Test plan

- [x] Package gate from `web/packages/chat-ui`: **`tsc` 0 errors ·
vitest 28 files / 275 tests pass · eslint 0/0** (verified independently,
not just by the implementer).
- [x] 2 new native-DOM test suites (no jest-dom): `specialist-open-card`
(name/greeting/aria, click + Enter/Space → `onOpen`, avatar→monogram
fallback, `humanizeAgentId`), `specialist-consent-card` (**new
`labels`+`body` contract**: body node + a button per label, single-fire
`onButtonClick`, consumed-state disabling + chosen line, destructive
banner, `labels: []` → null).
- [x] `web/app` + `docs` untouched (`git diff --name-only
origin/main...HEAD` is all `web/packages/chat-ui/`).
- [x] Rebased/merged current `main` (an unrelated knowledge-base commit;
no chat-ui overlap).
- [ ] CI `web-build-check` / CodeQL run on this PR.
```

### PR Body

## Summary

PR **A** of the specialist-card extraction — the **package-only, additive** step. Moves the two specialist card renderers into `@zooclaw/chat-ui` as pure, prop-driven components. **No `web/app` or docs changes**, so nothing consumes these yet — the app switch happens in PR B.

Spec/plan: `docs/superpowers/plans/2026-07-21-chat-ui-specialist-card-extraction.md` (PR A = Tasks 1–3), merged via #2992.

## What changed (all `web/packages/chat-ui`)

- **New `src/specialist/`**: `SpecialistOpenCard.tsx` (+ the pure `humanizeAgentId` helper), `SpecialistConsentCard.tsx`, and a barrel.
- **`SpecialistOpenCard`** — moved verbatim (only change: dropped `'use client'`, exported its props interface). Already fully prop-driven — every value pre-resolved by the caller.
- **`SpecialistConsentCard` — one deliberate contract change**: takes **`labels: string[]` + `body: React.ReactNode`** instead of `markdown: string`. It no longer imports `MarkdownContent` or `extractQuotedLabels`; the resolver (PR B's `SpecialistCardSlot`) extracts labels and renders the markdown body app-side, passing both in. This is what lets the card live in a package that can't import the app markdown pipeline — the "recursion" becomes a standard body slot. The consent body will be rendered by the app at `variant="compact"` (byte-identical to today).
- **Root barrel**: exports `SpecialistOpenCard`, `SpecialistConsentCard`, `humanizeAgentId`, and the two prop types (all new names — no collisions). `module-structure.test.ts` extended to pin the new root exports.

## Preservation

- Markup, classNames, and `data-testid`s move byte-for-byte: `specialist-open-card` (+ `data-agent-id`), `specialist-consent-card-{neutral|destructive}`, `specialist-consent-button-{label}`, `specialist-consent-chosen`; the `✓` chosen prefix, `⚠️` destructive banner, and consumed-state disabling are unchanged.
- No new dependencies (`@heroicons/react` already present). `'use client'` dropped to match sibling package convention.

## Test plan

- [x] Package gate from `web/packages/chat-ui`: **`tsc` 0 errors · vitest 28 files / 275 tests pass · eslint 0/0** (verified independently, not just by the implementer).
- [x] 2 new native-DOM test suites (no jest-dom): `specialist-open-card` (name/greeting/aria, click + Enter/Space → `onOpen`, avatar→monogram fallback, `humanizeAgentId`), `specialist-consent-card` (**new `labels`+`body` contract**: body node + a button per label, single-fire `onButtonClick`, consumed-state disabling + chosen line, destructive banner, `labels: []` → null).
- [x] `web/app` + `docs` untouched (`git diff --name-only origin/main...HEAD` is all `web/packages/chat-ui/`).
- [x] Rebased/merged current `main` (an unrelated knowledge-base commit; no chat-ui overlap).
- [ ] CI `web-build-check` / CodeQL run on this PR.


---

## fix(knowledge-base): poll pending document status (#2825)

- **SHA**: 7a5713674d6d4a4f6163516279bcc5a869f40fab
- **作者**: kevin
- **日期**: 2026-07-21T11:41:15Z
- **PR**: #2825

### Commit Message

```
fix(knowledge-base): poll pending document status (#2825)

## 问题分类
<!-- 在对应选项前的 [ ] 中填入 x -->
- [x] 前端 (web/)
- [x] 后端 (services/claw-interface/)
- [ ] 基础设施/CI
- [ ] 其他

## 问题描述

Fixes #2819

知识库上传页面：文档上传后显示"解析中"（`status ===
'pending'`），但前端没有任何状态轮询——必须手动刷新整页才能看到状态变成"已上传/失败"。

## 根因

`useKnowledgeBase` 的文档列表 query 只在 upload/delete 成功后 invalidate，`pending
→ indexed/failed` 的异步转变（Vertex AI Search 后台索引）没有任何触发点把新状态带回 UI。

不能简单给 list 查询加轮询：ecap-proxy-service 的 `GET /knowledge-base/documents`
实现是 1 次 GCS prefix LIST + **每文档 1 次 Vertex `get_document`**，成本随 org
文档数线性增长（其 docstring 自述 "cost is linear in the org's file
count"），不适合作为轮询目标。

## 修复方案

新增**批量状态接口**轮询链路（单文档状态推导只需 Vertex `get_document`，零 GCS 操作）：

1. **ecap-proxy-service**（外部 repo）：提出 `GET
/knowledge-base/documents/status?ids=…` 接口设计 →
SerendipityOneInc/ecap-proxy-service#145 —— **已部署至 staging**
2. **claw-interface**：新增同路径 passthrough（`_proxy` 增加 `params` 转发）
3. **前端 `useKnowledgeBase`**：
   - 仅当列表存在 `pending` 文档时，每 **30s** 轮询一次批量状态接口（tab 隐藏自动暂停）
- 终态用 `setQueryData` 写回 list 缓存（不 invalidate，避免触发昂贵的 list）→ pending 集合收缩
→ 全部终态后轮询自动停止
- id 分批：每请求最多 40 个（上游硬上限 50，见下方实测）。分片用 `Promise.allSettled`
合并：滚动发布期间并发分片可能落到不同版本的 pod（旧 pod 405 / 新 pod 200），若用 `Promise.all`，单个
rejection 会连带丢弃已成功分片的终态，>40 个 pending 文档的组织将在整个 rollout
期间看到全部文档卡在"解析中"。失败分片的 id 仍留在 pendingIds、下个 tick
重查，故容忍任意单分片失败是安全的；但**全部分片失败时仍抛错**，避免退化成"成功但无数据"导致 `isError` 永不触发。
4. **mock-backend**：补 `/knowledge-base/*` in-memory handlers（上传 45s 后翻转
indexed），支撑本地端到端验证

**优雅降级 / 部署顺序无约束**：BFF 还没部署这条路由时，轮询收到的是 **405 而非 404** —— FastAPI
先按路径匹配，`/documents/status` 落进 `DELETE /documents/{document_id}`
的模式（`document_id="status"`），路径存在但 GET 未注册，故 405（已对 staging
claw-interface 实测确认）。降级与错误码无关：前端不重试、等下一个 30s
tick，文档保持"解析中"（与现状一致，不更坏）。跨面变更：完整生效需 claw-interface 与 web 都发版。

## 与 main 的同步

本分支已 merge `origin/main`（此前落后 123 个 commit）。main 期间的 kb-sharing
特性线把知识库改成了多 library + 共享授权模型，冲突集中在作用域扩展：文档缓存 key 从 `uid` 扩为 `uid +
orgId`，身份来源从 `useAuth()` 换成 `useKbIdentity()`。轮询链路本身与 kb-sharing
正交，逻辑未做取舍，仅同步了这三处作用域：

- `knowledgeBaseKeys.documentStatuses(uid, orgId, ids)` —— 必须与
`documents` 同维度，否则 `setQueryData` 会静默写入无人订阅的缓存条目
- `enabled: loggedIn && pendingIds.length > 0`
- 写回时 spread 保留 kb-sharing 新增的 `kb_id` / `is_owner` 字段

## 测试

- [x] `verify-web.sh`：guards + tsc + eslint 全绿；KB 单测 22 passed
- [x] 后端：`verify-py.sh` 静态档全绿（ruff + ruff-format + pyright +
import-linter 8 条契约）**及完整 pytest 套件 6306 passed**（静态档默认不含 pytest，需单独跑）
- [x] **mock 端到端**（dev-mock + Playwright，不刷新页面）：上传 → 轮询于 T+2s / T+32s /
T+62s 三次命中 `/documents/status` → **T+63s 徽章翻转为"已上传"**；`navigationEntries
= 1`（全程零 reload）；轮询期间 `/documents` 列表接口零调用；终态后停止
- [x] **真实 staging 契约验证**（telepresence 直连 in-cluster
ecap-proxy-service）：
  - 响应字段 `id` / `status` / `indexed_at` / `error` 与前端类型逐字一致
- `indexed_at` / `error` 实际序列化为 `null` 而非省略字段（OpenAPI 中二者非
required，声明层无法区分，需实测）
  - 未知 / 他人 org 的 id 一律返回 `pending`（fail-closed，不泄露存在性）
- **50 id 上限为强制**：51 个 id 返回 `400 Too many ids; maximum is 50` —— 故
`KB_STATUS_IDS_PER_REQUEST = 40` 的分片是必需逻辑，非防御性冗余
- [x] 降级路径：状态接口报错时轮询按 30s 继续、徽章保持"解析中"、零页面错误

**未覆盖**：本地无 Mongo（无 docker/mongod），staging 契约验证走的是「仅挂载 knowledge_base
router 的最小 FastAPI 应用」，绕过了 `lifetime.startup()`，故不覆盖应用启动装配。本 PR 未改动该路径。

## Merge 后的语义冲突（已修）

合并 main 时 `test_knowledge_base.py` **零文本冲突自动合并**，但存在语义冲突：本分支给 `_proxy`
增加了 `params` 形参，使 `client.request()` 恒带 `params=...`，而 main 新增的两个
kb-sharing 测试逐参数断言了调用签名（写于该形参存在之前），CI 报 `expected await not found`。

修在测试侧而非让 `_proxy` 在 `params is None` 时省略该 kwarg：本文件 6 处调用断言已有 4 处显式写出
`params=`，补齐后一致；反之在生产代码里加条件分支只为迁就测试，属本末倒置。

## 影响范围

- 知识库上传页（`useKnowledgeBase` hook 的消费方）；列表 query 本身行为不变
- claw-interface `/knowledge-base/*` 既有路由行为不变（`params` 参数默认 `None`）
- 路由顺序约束：`GET /documents/status` 字面路由必须声明在 `DELETE
/documents/{document_id}` 之前，否则会被路径模式吸收（代码内已注明）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## 问题分类
<!-- 在对应选项前的 [ ] 中填入 x -->
- [x] 前端 (web/)
- [x] 后端 (services/claw-interface/)
- [ ] 基础设施/CI
- [ ] 其他

## 问题描述

Fixes #2819

知识库上传页面：文档上传后显示"解析中"（`status === 'pending'`），但前端没有任何状态轮询——必须手动刷新整页才能看到状态变成"已上传/失败"。

## 根因

`useKnowledgeBase` 的文档列表 query 只在 upload/delete 成功后 invalidate，`pending → indexed/failed` 的异步转变（Vertex AI Search 后台索引）没有任何触发点把新状态带回 UI。

不能简单给 list 查询加轮询：ecap-proxy-service 的 `GET /knowledge-base/documents` 实现是 1 次 GCS prefix LIST + **每文档 1 次 Vertex `get_document`**，成本随 org 文档数线性增长（其 docstring 自述 "cost is linear in the org's file count"），不适合作为轮询目标。

## 修复方案

新增**批量状态接口**轮询链路（单文档状态推导只需 Vertex `get_document`，零 GCS 操作）：

1. **ecap-proxy-service**（外部 repo）：提出 `GET /knowledge-base/documents/status?ids=…` 接口设计 → SerendipityOneInc/ecap-proxy-service#145 —— **已部署至 staging**
2. **claw-interface**：新增同路径 passthrough（`_proxy` 增加 `params` 转发）
3. **前端 `useKnowledgeBase`**：
   - 仅当列表存在 `pending` 文档时，每 **30s** 轮询一次批量状态接口（tab 隐藏自动暂停）
   - 终态用 `setQueryData` 写回 list 缓存（不 invalidate，避免触发昂贵的 list）→ pending 集合收缩 → 全部终态后轮询自动停止
   - id 分批：每请求最多 40 个（上游硬上限 50，见下方实测）。分片用 `Promise.allSettled` 合并：滚动发布期间并发分片可能落到不同版本的 pod（旧 pod 405 / 新 pod 200），若用 `Promise.all`，单个 rejection 会连带丢弃已成功分片的终态，>40 个 pending 文档的组织将在整个 rollout 期间看到全部文档卡在"解析中"。失败分片的 id 仍留在 pendingIds、下个 tick 重查，故容忍任意单分片失败是安全的；但**全部分片失败时仍抛错**，避免退化成"成功但无数据"导致 `isError` 永不触发。
4. **mock-backend**：补 `/knowledge-base/*` in-memory handlers（上传 45s 后翻转 indexed），支撑本地端到端验证

**优雅降级 / 部署顺序无约束**：BFF 还没部署这条路由时，轮询收到的是 **405 而非 404** —— FastAPI 先按路径匹配，`/documents/status` 落进 `DELETE /documents/{document_id}` 的模式（`document_id="status"`），路径存在但 GET 未注册，故 405（已对 staging claw-interface 实测确认）。降级与错误码无关：前端不重试、等下一个 30s tick，文档保持"解析中"（与现状一致，不更坏）。跨面变更：完整生效需 claw-interface 与 web 都发版。

## 与 main 的同步

本分支已 merge `origin/main`（此前落后 123 个 commit）。main 期间的 kb-sharing 特性线把知识库改成了多 library + 共享授权模型，冲突集中在作用域扩展：文档缓存 key 从 `uid` 扩为 `uid + orgId`，身份来源从 `useAuth()` 换成 `useKbIdentity()`。轮询链路本身与 kb-sharing 正交，逻辑未做取舍，仅同步了这三处作用域：

- `knowledgeBaseKeys.documentStatuses(uid, orgId, ids)` —— 必须与 `documents` 同维度，否则 `setQueryData` 会静默写入无人订阅的缓存条目
- `enabled: loggedIn && pendingIds.length > 0`
- 写回时 spread 保留 kb-sharing 新增的 `kb_id` / `is_owner` 字段

## 测试

- [x] `verify-web.sh`：guards + tsc + eslint 全绿；KB 单测 22 passed
- [x] 后端：`verify-py.sh` 静态档全绿（ruff + ruff-format + pyright + import-linter 8 条契约）**及完整 pytest 套件 6306 passed**（静态档默认不含 pytest，需单独跑）
- [x] **mock 端到端**（dev-mock + Playwright，不刷新页面）：上传 → 轮询于 T+2s / T+32s / T+62s 三次命中 `/documents/status` → **T+63s 徽章翻转为"已上传"**；`navigationEntries = 1`（全程零 reload）；轮询期间 `/documents` 列表接口零调用；终态后停止
- [x] **真实 staging 契约验证**（telepresence 直连 in-cluster ecap-proxy-service）：
  - 响应字段 `id` / `status` / `indexed_at` / `error` 与前端类型逐字一致
  - `indexed_at` / `error` 实际序列化为 `null` 而非省略字段（OpenAPI 中二者非 required，声明层无法区分，需实测）
  - 未知 / 他人 org 的 id 一律返回 `pending`（fail-closed，不泄露存在性）
  - **50 id 上限为强制**：51 个 id 返回 `400 Too many ids; maximum is 50` —— 故 `KB_STATUS_IDS_PER_REQUEST = 40` 的分片是必需逻辑，非防御性冗余
- [x] 降级路径：状态接口报错时轮询按 30s 继续、徽章保持"解析中"、零页面错误

**未覆盖**：本地无 Mongo（无 docker/mongod），staging 契约验证走的是「仅挂载 knowledge_base router 的最小 FastAPI 应用」，绕过了 `lifetime.startup()`，故不覆盖应用启动装配。本 PR 未改动该路径。

## Merge 后的语义冲突（已修）

合并 main 时 `test_knowledge_base.py` **零文本冲突自动合并**，但存在语义冲突：本分支给 `_proxy` 增加了 `params` 形参，使 `client.request()` 恒带 `params=...`，而 main 新增的两个 kb-sharing 测试逐参数断言了调用签名（写于该形参存在之前），CI 报 `expected await not found`。

修在测试侧而非让 `_proxy` 在 `params is None` 时省略该 kwarg：本文件 6 处调用断言已有 4 处显式写出 `params=`，补齐后一致；反之在生产代码里加条件分支只为迁就测试，属本末倒置。

## 影响范围

- 知识库上传页（`useKnowledgeBase` hook 的消费方）；列表 query 本身行为不变
- claw-interface `/knowledge-base/*` 既有路由行为不变（`params` 参数默认 `None`）
- 路由顺序约束：`GET /documents/status` 字面路由必须声明在 `DELETE /documents/{document_id}` 之前，否则会被路径模式吸收（代码内已注明）

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## refactor(chat-ui): relocate ModelPicker from design-system to chat-ui (#2993)

- **SHA**: 04f86da3d0d001934d64f9a5af007191986aa65e
- **作者**: bill-srp
- **日期**: 2026-07-21T11:39:23Z
- **PR**: #2993

### Commit Message

```
refactor(chat-ui): relocate ModelPicker from design-system to chat-ui (#2993)

## Summary

Relocates the product-specific **ModelPicker** out of
`@zooclaw/design-system` and into `@zooclaw/chat-ui` (beside
`ChatComposer`), so the design system stays pure, domain-agnostic
primitives.

This **unwinds the model-picker slice of #2986** (cc @lynn-srp). #2986's
*generic* improvements — the `Button` / `Tooltip` arrow / `Tag` /
`data-hover-surface` changes and the `--zc-tooltip-*` / `--tooltip-*`
tokens — are **kept** in the DS. Only the model-picker–specific parts
move.

### Why

A design system should hold generic primitives, not a `ModelPicker` that
encodes product/billing concepts (`Token consumption rate`, multipliers)
and hardcoded product copy. #2986 also pushed model-specific parts
(`DropdownMenuModelItem/Badge/Trigger/Detail*`, `surface="model"`) into
the generic `dropdown-menu` primitive, contaminating it.
`@zooclaw/chat-ui` — the product-shared UI layer that composes DS
primitives — is the right home. This keeps the layering clean:
`design-system (primitives)` <- `chat-ui (composer UI)` <- `webapp
(data/auth/API)`.

### What moved to chat-ui

- `model-picker.tsx` (+ its test suite) ->
`packages/chat-ui/src/composer/ModelPicker.tsx`
- The `DropdownMenuModel*` parts + the `surface="model"` styling ->
local, chat-ui-owned Tailwind inside `ModelPicker.tsx`, composing the DS
**public** exports only (no DS internals)
- The `--model-picker-*` token values -> chat-ui Tailwind arbitrary
values with the same fallbacks (`#ffffff` / `#f4f4f5` / `#e4e4e7` +
`--zc-wash` / `--zc-line`)
- `@zooclaw/chat-ui` gains a `@zooclaw/design-system` workspace dep and
exports `ModelPicker` / `ModelPickerOption` / `ModelPickerProps`

### What reverted in the design system

- Deleted `model-picker.tsx`, the `DropdownMenuModel*` +
`surface="model"` additions, the `--model-picker-*` tokens, the bundled
`assets/model-providers/*.png`, the index exports, and the preview
usage. Generic button/tooltip/tag/`data-hover-surface` improvements from
#2986 are untouched.

### Icon handling

Stays consumer-supplied via `iconSrc` + a plain `<img>` (chat-ui stays
asset-free — no bundled binaries). The webapp normalizer will set
`iconSrc` / `monochromeIcon` in the follow-up wiring slice.

### Scope

Package refactor only — **no webapp wiring**. The app does not consume
`ModelPicker` yet, so nothing app-facing changes here. A follow-up slice
points the unified composer at chat-ui's `ModelPicker` and deletes the
app-local `ComposerModelMenu`.

## Related

- Part of
[ECA-1288](https://linear.app/srpone/issue/ECA-1288/separate-shared-composer-presentation-from-application-orchestration)
— separate shared composer presentation from application orchestration
- Unwinds the model-picker slice of #2986

## Test plan

- [x] `pnpm --filter @zooclaw/design-system tsc && lint && test` — 282
tests pass
- [x] `pnpm --filter @zooclaw/chat-ui tsc && lint && test` — 263 tests
pass (incl. the 11 moved ModelPicker behavioral tests)
- [x] `bash scripts/verify-web.sh` — tsc + 7152 app tests + eslint +
governance guards pass
- [x] `pnpm install --frozen-lockfile` passes (lockfile updated for the
new workspace dep; no app-runtime version bumps)
- [x] DS residue grep: zero `ModelPicker` / `DropdownMenuModel` /
`--model-picker-*` left in `@zooclaw/design-system`
- [ ] Visual eyeball of `ModelPicker` when the app-wiring slice renders
it (panel width `w-[276px]`; detail tooltip arrow hidden since chat-ui
composes the public `TooltipContent`)
```

### PR Body

## Summary

Relocates the product-specific **ModelPicker** out of `@zooclaw/design-system` and into `@zooclaw/chat-ui` (beside `ChatComposer`), so the design system stays pure, domain-agnostic primitives.

This **unwinds the model-picker slice of #2986** (cc @lynn-srp). #2986's *generic* improvements — the `Button` / `Tooltip` arrow / `Tag` / `data-hover-surface` changes and the `--zc-tooltip-*` / `--tooltip-*` tokens — are **kept** in the DS. Only the model-picker–specific parts move.

### Why

A design system should hold generic primitives, not a `ModelPicker` that encodes product/billing concepts (`Token consumption rate`, multipliers) and hardcoded product copy. #2986 also pushed model-specific parts (`DropdownMenuModelItem/Badge/Trigger/Detail*`, `surface="model"`) into the generic `dropdown-menu` primitive, contaminating it. `@zooclaw/chat-ui` — the product-shared UI layer that composes DS primitives — is the right home. This keeps the layering clean: `design-system (primitives)` <- `chat-ui (composer UI)` <- `webapp (data/auth/API)`.

### What moved to chat-ui

- `model-picker.tsx` (+ its test suite) -> `packages/chat-ui/src/composer/ModelPicker.tsx`
- The `DropdownMenuModel*` parts + the `surface="model"` styling -> local, chat-ui-owned Tailwind inside `ModelPicker.tsx`, composing the DS **public** exports only (no DS internals)
- The `--model-picker-*` token values -> chat-ui Tailwind arbitrary values with the same fallbacks (`#ffffff` / `#f4f4f5` / `#e4e4e7` + `--zc-wash` / `--zc-line`)
- `@zooclaw/chat-ui` gains a `@zooclaw/design-system` workspace dep and exports `ModelPicker` / `ModelPickerOption` / `ModelPickerProps`

### What reverted in the design system

- Deleted `model-picker.tsx`, the `DropdownMenuModel*` + `surface="model"` additions, the `--model-picker-*` tokens, the bundled `assets/model-providers/*.png`, the index exports, and the preview usage. Generic button/tooltip/tag/`data-hover-surface` improvements from #2986 are untouched.

### Icon handling

Stays consumer-supplied via `iconSrc` + a plain `<img>` (chat-ui stays asset-free — no bundled binaries). The webapp normalizer will set `iconSrc` / `monochromeIcon` in the follow-up wiring slice.

### Scope

Package refactor only — **no webapp wiring**. The app does not consume `ModelPicker` yet, so nothing app-facing changes here. A follow-up slice points the unified composer at chat-ui's `ModelPicker` and deletes the app-local `ComposerModelMenu`.

## Related

- Part of [ECA-1288](https://linear.app/srpone/issue/ECA-1288/separate-shared-composer-presentation-from-application-orchestration) — separate shared composer presentation from application orchestration
- Unwinds the model-picker slice of #2986

## Test plan

- [x] `pnpm --filter @zooclaw/design-system tsc && lint && test` — 282 tests pass
- [x] `pnpm --filter @zooclaw/chat-ui tsc && lint && test` — 263 tests pass (incl. the 11 moved ModelPicker behavioral tests)
- [x] `bash scripts/verify-web.sh` — tsc + 7152 app tests + eslint + governance guards pass
- [x] `pnpm install --frozen-lockfile` passes (lockfile updated for the new workspace dep; no app-runtime version bumps)
- [x] DS residue grep: zero `ModelPicker` / `DropdownMenuModel` / `--model-picker-*` left in `@zooclaw/design-system`
- [ ] Visual eyeball of `ModelPicker` when the app-wiring slice renders it (panel width `w-[276px]`; detail tooltip arrow hidden since chat-ui composes the public `TooltipContent`)


---

## docs: add chat UI specialist card extraction spec and plan (#2992)

- **SHA**: bdcc2650811be5298fbd0c35f439a47683366fc5
- **作者**: bill-srp
- **日期**: 2026-07-21T11:38:42Z
- **PR**: #2992

### Commit Message

```
docs: add chat UI specialist card extraction spec and plan (#2992)

## Summary

Design spec + implementation plan for the next `@zooclaw/chat-ui`
extraction slice: the two **specialist card renderers**
(`SpecialistOpenCard`, `SpecialistConsentCard`). Docs-only — no code.
Follows the initiative's docs-first gate.

**The last meaningful render slice.** After leaves / message renderers /
attachments / ERMP, the specialist cards are the remaining reusable
chat-render piece; the only other app-side chat UI is the thread
(dep-blocked by `@assistant-ui/react`, deliberately not moving) and app
chrome.

## Design highlights (verified against source)

- **`SpecialistOpenCard` is already pure** — react + heroicons only,
every prop pre-resolved by the caller. Moves verbatim (+ the
`humanizeAgentId` helper).
- **`SpecialistConsentCard`'s only app touches** are
`extractQuotedLabels(markdown)` and one `<MarkdownContent>` body render.
Both lift out: the card takes **`labels: string[]` + `body:
React.ReactNode`** instead of `markdown`. The "markdown recursion" that
made this look hard becomes a standard **body-slot prop** — the package
never imports `MarkdownContent`.
- **`SpecialistCardSlot` stays app-side** as the resolver (identity via
`getAgentAvatarUrl`/`getAgentDisplayName`, i18n, kind dispatch, and the
degradation ladder: empty labels → plain markdown). It's the only
importer of the two cards, and `MarkdownContent` only imports the slot —
so callers are untouched.

## Delivery

- **PR A** (Tasks 1–3): package-only, additive — two cards +
`humanizeAgentId` + barrel + native-DOM tests.
- **PR B** (Tasks 4–6): app-only, replace — rewrite `SpecialistCardSlot`
to pass the body slot, delete the two moved cards, move their specs to
the package.

The `MarkdownContent{,-extras}` integration specs are the protected
harness (unchanged). Codex implements each PR via `codex:rescue`; Claude
verifies independently + runs PR mechanics.

## Files

-
`docs/superpowers/specs/2026-07-21-chat-ui-specialist-card-extraction-design.md`
-
`docs/superpowers/plans/2026-07-21-chat-ui-specialist-card-extraction.md`

## Test plan

- [x] Docs-only; no code paths touched. `git diff --stat origin/main --
web` empty.
- [ ] Review the `labels`+`body` contract change on
`SpecialistConsentCard` + the resolver split before implementation.
```

### PR Body

## Summary

Design spec + implementation plan for the next `@zooclaw/chat-ui` extraction slice: the two **specialist card renderers** (`SpecialistOpenCard`, `SpecialistConsentCard`). Docs-only — no code. Follows the initiative's docs-first gate.

**The last meaningful render slice.** After leaves / message renderers / attachments / ERMP, the specialist cards are the remaining reusable chat-render piece; the only other app-side chat UI is the thread (dep-blocked by `@assistant-ui/react`, deliberately not moving) and app chrome.

## Design highlights (verified against source)

- **`SpecialistOpenCard` is already pure** — react + heroicons only, every prop pre-resolved by the caller. Moves verbatim (+ the `humanizeAgentId` helper).
- **`SpecialistConsentCard`'s only app touches** are `extractQuotedLabels(markdown)` and one `<MarkdownContent>` body render. Both lift out: the card takes **`labels: string[]` + `body: React.ReactNode`** instead of `markdown`. The "markdown recursion" that made this look hard becomes a standard **body-slot prop** — the package never imports `MarkdownContent`.
- **`SpecialistCardSlot` stays app-side** as the resolver (identity via `getAgentAvatarUrl`/`getAgentDisplayName`, i18n, kind dispatch, and the degradation ladder: empty labels → plain markdown). It's the only importer of the two cards, and `MarkdownContent` only imports the slot — so callers are untouched.

## Delivery

- **PR A** (Tasks 1–3): package-only, additive — two cards + `humanizeAgentId` + barrel + native-DOM tests.
- **PR B** (Tasks 4–6): app-only, replace — rewrite `SpecialistCardSlot` to pass the body slot, delete the two moved cards, move their specs to the package.

The `MarkdownContent{,-extras}` integration specs are the protected harness (unchanged). Codex implements each PR via `codex:rescue`; Claude verifies independently + runs PR mechanics.

## Files

- `docs/superpowers/specs/2026-07-21-chat-ui-specialist-card-extraction-design.md`
- `docs/superpowers/plans/2026-07-21-chat-ui-specialist-card-extraction.md`

## Test plan

- [x] Docs-only; no code paths touched. `git diff --stat origin/main -- web` empty.
- [ ] Review the `labels`+`body` contract change on `SpecialistConsentCard` + the resolver split before implementation.


---

## feat(claw-interface): disable engine agent channels on uninstall (#2988)

- **SHA**: a99f7e2c0da5958e76e830ddff78c61dff9b6341
- **作者**: bill-srp
- **日期**: 2026-07-21T11:19:14Z
- **PR**: #2988

### Commit Message

```
feat(claw-interface): disable engine agent channels on uninstall (#2988)

## Summary

Firing an engine agent left its ACS channels running. Any
Slack/Feishu/WeCom/Weixin channel the user connected — plus the internal
`mattermost` bind — kept receiving and sending after the workspace
disappeared from the UI.

This PR wires ACS's purpose-built fire endpoint into the uninstall flow:

```
POST /v1/computers/{computer_id}/agents/{agent_id}/channels/disable → 202 {"channel_ids": [...]}
```

The final lifecycle is:

```
stop_agent → finalize workspace as uninstalled → await ACS bulk-disable
```

Engine uninstall deliberately stops the runtime but retains the engine
agent record; it never calls `delete_agent`. The local workspace
terminal state is authoritative. ACS cleanup is still awaited, but its
success or failure cannot change a completed uninstall. An ACS failure
emits an ERROR log with traceback and ownership/runtime scope.

**Disable, not delete** — the ACS endpoint idempotently flips every
bound channel, including `mattermost`, to `enabled=false` while
preserving rows, credentials, and configuration. ACS handles
platform-gateway notification server-side.

Lineage: ECA-1279 — https://linear.app/srpone/issue/ECA-1279

Plan:
`docs/superpowers/plans/2026-07-21-engine-agent-fire-channel-cleanup.md`

Depends on: `agent-channel-service#37` (merged).

## What's new

- **Client** (`channel_service_client/_channels.py`) —
`disable_agent_channels(actor, computer_id, agent_id) -> list[str]`
POSTs to the disable endpoint and returns the affected `channel_ids`.
- **Helper** (`engine_agent_channels_service.py`) — makes one idempotent
ACS call and never raises. Failure logs at ERROR with traceback and
returns `[]`; success logs the disabled count.
- **Lifecycle** (`engine_agent_lifecycle_service.py`) — awaits
`stop_agent`, commits local `uninstalled`, then awaits ACS cleanup
outside the fail-closed state-transition block. It does not call engine
DELETE.
- **Critical failures** — engine stop or local terminal-write failure
still persists `uninstall_failed` and propagates the error. ACS failure
leaves the workspace `uninstalled`.

## Test plan

- [x] Relevant lifecycle/channel unit tests: **95 passed**
- [x] Engine-agent BDD scenarios against throwaway Mongo: **12 passed**
- [x] `ruff check`, `ruff format --check`, and import-linter: **passed**
- [x] Targeted pyright for changed production/tests: **0 errors**
- [x] Pre-commit hooks, including pyright, dependency checks, import
contracts, and vulture: **passed**
- [ ] CI `python-code-quality / build-and-test`

## Rollout / risk

Backend-only, with no route or schema changes. If ACS is unavailable,
uninstall still returns the already-committed local terminal workspace
and logs the cleanup failure at ERROR. If engine stop or the local
terminal write fails, uninstall remains fail-closed as
`uninstall_failed`. Requires `agent-channel-service#37` in the target
environment; an older ACS returns an error that is logged without
reverting the local uninstall.
```

### PR Body

## Summary

Firing an engine agent left its ACS channels running. Any Slack/Feishu/WeCom/Weixin channel the user connected — plus the internal `mattermost` bind — kept receiving and sending after the workspace disappeared from the UI.

This PR wires ACS's purpose-built fire endpoint into the uninstall flow:

```
POST /v1/computers/{computer_id}/agents/{agent_id}/channels/disable → 202 {"channel_ids": [...]}
```

The final lifecycle is:

```
stop_agent → finalize workspace as uninstalled → await ACS bulk-disable
```

Engine uninstall deliberately stops the runtime but retains the engine agent record; it never calls `delete_agent`. The local workspace terminal state is authoritative. ACS cleanup is still awaited, but its success or failure cannot change a completed uninstall. An ACS failure emits an ERROR log with traceback and ownership/runtime scope.

**Disable, not delete** — the ACS endpoint idempotently flips every bound channel, including `mattermost`, to `enabled=false` while preserving rows, credentials, and configuration. ACS handles platform-gateway notification server-side.

Lineage: ECA-1279 — https://linear.app/srpone/issue/ECA-1279

Plan: `docs/superpowers/plans/2026-07-21-engine-agent-fire-channel-cleanup.md`

Depends on: `agent-channel-service#37` (merged).

## What's new

- **Client** (`channel_service_client/_channels.py`) — `disable_agent_channels(actor, computer_id, agent_id) -> list[str]` POSTs to the disable endpoint and returns the affected `channel_ids`.
- **Helper** (`engine_agent_channels_service.py`) — makes one idempotent ACS call and never raises. Failure logs at ERROR with traceback and returns `[]`; success logs the disabled count.
- **Lifecycle** (`engine_agent_lifecycle_service.py`) — awaits `stop_agent`, commits local `uninstalled`, then awaits ACS cleanup outside the fail-closed state-transition block. It does not call engine DELETE.
- **Critical failures** — engine stop or local terminal-write failure still persists `uninstall_failed` and propagates the error. ACS failure leaves the workspace `uninstalled`.

## Test plan

- [x] Relevant lifecycle/channel unit tests: **95 passed**
- [x] Engine-agent BDD scenarios against throwaway Mongo: **12 passed**
- [x] `ruff check`, `ruff format --check`, and import-linter: **passed**
- [x] Targeted pyright for changed production/tests: **0 errors**
- [x] Pre-commit hooks, including pyright, dependency checks, import contracts, and vulture: **passed**
- [ ] CI `python-code-quality / build-and-test`

## Rollout / risk

Backend-only, with no route or schema changes. If ACS is unavailable, uninstall still returns the already-committed local terminal workspace and logs the cleanup failure at ERROR. If engine stop or the local terminal write fails, uninstall remains fail-closed as `uninstall_failed`. Requires `agent-channel-service#37` in the target environment; an older ACS returns an error that is logged without reverting the local uninstall.


---

## refactor(web): render ERMP cards via @zooclaw/chat-ui (#2990)

- **SHA**: 9052ea842bef8e518f7a3ef51fb155225b41e9c0
- **作者**: bill-srp
- **日期**: 2026-07-21T10:55:18Z
- **PR**: #2990

### Commit Message

```
refactor(web): render ERMP cards via @zooclaw/chat-ui (#2990)

## Summary

PR **B** of the ERMP card extraction — the **app "replace"** step.
Rewrites the app ERMP path to consume the `@zooclaw/chat-ui` cards
merged in PR A (#2985). Completes the slice: docs #2984 → package
extract #2985 → this replace.

Spec/plan:
`docs/superpowers/plans/2026-07-21-chat-ui-ermp-card-extraction.md` (PR
B = Tasks 8–12).

## What changed (all `web/app`)

- **`ERMPCardRenderer.tsx`** → a thin `memo`'d wrapper over the package
renderer. Same public signature (`{ card, onCallback, onFormSubmit }`),
so `OpenClawAssistantMessage` / `OpenClawUserMessage` /
`ERMPCardSegment` are untouched. It resolves `useIsReplayReadOnly()` →
`readOnly`, injects `isSubmitted={isCardSubmitted}`, and records
`markCardSubmitted` inside wrapped callbacks — the app keeps ownership
of replay-mode and submit-state; the package cards stay pure.
- **`utils.ts`** — keeps the parsers (`parseERMPCard` /
`extractEcapCardBlocks` / `detectMediaCards` / `isERMPCard`) and the
submit-state `Set`; drops the moved formatters; repoints its
`AudioCard/ERMPCard/FileCard/VideoCard` type import from the deleted
`./types` to `@zooclaw/chat-ui` (the exact break the docs review
pre-caught).
- **`index.ts`** — re-exports the wrapper + parsers, with the `ERMPCard`
types now sourced from `@zooclaw/chat-ui`.
- **Deleted** (moved to the package in PR A): the 8 card components +
`types.ts`, and the 4 card specs (`cards` / `data-cards` /
`interactive-cards` / `renderer`) whose coverage now lives in the
package's native-DOM tests.

## Review-cleanup note

Codex's first pass kept a deep re-export `export { formatFileSize,
formatDuration } from '../../../../packages/chat-ui/src/ermp/utils'`
solely to keep `utils.unit.spec.ts`'s formatter tests green. That
reaches past the `@zooclaw/chat-ui` boundary into package internals. I
removed it and instead trimmed the two moved-formatter `describe` blocks
from `utils.unit.spec.ts` (those functions now live in — and are tested
by — the package's `ermp-utils.test.ts`). The spec still fully covers
the app-side parsers + submit-state.

## Test plan

- [x] `pnpm exec tsc --noEmit` (whole app) — clean (confirms no dangling
refs after the type-import repoint + deep-import removal).
- [x] Full unit suite: **528 files / 7115 tests pass** (1 skipped, 1
todo).
- [x] **4 protected specs pass UNCHANGED**: `OpenClawAssistantMessage`,
`OpenClawUserMessage`, `MarkdownContent`, `MarkdownContent-extras` — the
integration harness (message renderer + markdown-segment paths through
the app wrapper).
- [x] Coverage ratchet holds: **stmts 88.21 / branches 81.59 / funcs
86.97 / lines 90.54** (thresholds 83 / 75 / 81 / 85).
- [x] eslint clean; `lint:imports` 0 errors (the deep package-internals
import is gone).
- [~] Browser check: the local mock backend does not emit ERMP cards
(they arrive as bot `ermp_cards` message props / `ecap-card` fences), so
a live ERMP render can't be exercised in the mock. Runtime integration
is covered by CI `web-build-check` (`next build`), the byte-identical
package markup (verified in PR A), and the passing message-renderer +
MarkdownContent specs that drive the app wrapper.
- [ ] CI `web-build-check` runs on this PR.

`web/packages/chat-ui` and `docs` untouched. Scope: `web/app` only.
```

### PR Body

## Summary

PR **B** of the ERMP card extraction — the **app "replace"** step. Rewrites the app ERMP path to consume the `@zooclaw/chat-ui` cards merged in PR A (#2985). Completes the slice: docs #2984 → package extract #2985 → this replace.

Spec/plan: `docs/superpowers/plans/2026-07-21-chat-ui-ermp-card-extraction.md` (PR B = Tasks 8–12).

## What changed (all `web/app`)

- **`ERMPCardRenderer.tsx`** → a thin `memo`'d wrapper over the package renderer. Same public signature (`{ card, onCallback, onFormSubmit }`), so `OpenClawAssistantMessage` / `OpenClawUserMessage` / `ERMPCardSegment` are untouched. It resolves `useIsReplayReadOnly()` → `readOnly`, injects `isSubmitted={isCardSubmitted}`, and records `markCardSubmitted` inside wrapped callbacks — the app keeps ownership of replay-mode and submit-state; the package cards stay pure.
- **`utils.ts`** — keeps the parsers (`parseERMPCard` / `extractEcapCardBlocks` / `detectMediaCards` / `isERMPCard`) and the submit-state `Set`; drops the moved formatters; repoints its `AudioCard/ERMPCard/FileCard/VideoCard` type import from the deleted `./types` to `@zooclaw/chat-ui` (the exact break the docs review pre-caught).
- **`index.ts`** — re-exports the wrapper + parsers, with the `ERMPCard` types now sourced from `@zooclaw/chat-ui`.
- **Deleted** (moved to the package in PR A): the 8 card components + `types.ts`, and the 4 card specs (`cards` / `data-cards` / `interactive-cards` / `renderer`) whose coverage now lives in the package's native-DOM tests.

## Review-cleanup note

Codex's first pass kept a deep re-export `export { formatFileSize, formatDuration } from '../../../../packages/chat-ui/src/ermp/utils'` solely to keep `utils.unit.spec.ts`'s formatter tests green. That reaches past the `@zooclaw/chat-ui` boundary into package internals. I removed it and instead trimmed the two moved-formatter `describe` blocks from `utils.unit.spec.ts` (those functions now live in — and are tested by — the package's `ermp-utils.test.ts`). The spec still fully covers the app-side parsers + submit-state.

## Test plan

- [x] `pnpm exec tsc --noEmit` (whole app) — clean (confirms no dangling refs after the type-import repoint + deep-import removal).
- [x] Full unit suite: **528 files / 7115 tests pass** (1 skipped, 1 todo).
- [x] **4 protected specs pass UNCHANGED**: `OpenClawAssistantMessage`, `OpenClawUserMessage`, `MarkdownContent`, `MarkdownContent-extras` — the integration harness (message renderer + markdown-segment paths through the app wrapper).
- [x] Coverage ratchet holds: **stmts 88.21 / branches 81.59 / funcs 86.97 / lines 90.54** (thresholds 83 / 75 / 81 / 85).
- [x] eslint clean; `lint:imports` 0 errors (the deep package-internals import is gone).
- [~] Browser check: the local mock backend does not emit ERMP cards (they arrive as bot `ermp_cards` message props / `ecap-card` fences), so a live ERMP render can't be exercised in the mock. Runtime integration is covered by CI `web-build-check` (`next build`), the byte-identical package markup (verified in PR A), and the passing message-renderer + MarkdownContent specs that drive the app wrapper.
- [ ] CI `web-build-check` runs on this PR.

`web/packages/chat-ui` and `docs` untouched. Scope: `web/app` only.


---

## fix(chat): make the typewriter smooth streamed replies instead of skipping them (#2989)

- **SHA**: 4dde531c9baad08de02b9edcbfb057463fd77cd7
- **作者**: Chris@ZooClaw
- **日期**: 2026-07-21T10:57:54Z
- **PR**: #2989

### Commit Message

```
fix(chat): make the typewriter smooth streamed replies instead of skipping them (#2989)

## Summary

- 流式回复的打字机**在流式期间从来没运行过**，原始 WS 分片直接上屏——每 ~1.24 秒蹦 ~74
个字符，这就是"卡顿"的全部来源。本 PR 让打字机接管流式消息，并按 backlog 自适应配速。
- 顺带修掉一个更严重、且此前没人发现的 bug：前端从不处理 `post_deleted`，**每次长回答的前 4000
字符都会在界面上重复显示一遍**。
- 调查报告 +
实测数据：`docs/superpowers/specs/2026-07-21-chat-streaming-smoothness.md`

## Root cause

打字机被两个机制夹出了一个**零长度的启动窗口**：

1. `useMattermost.ts:102-103` 的 `markRecentBot(post.id,
post.message.length)` 只在 `posted` 触发一次，而 `useMattermostTyping.ts:140` 的
`removeDelay = Math.max(2000, messageLength * 5)` 用的是那一刻的长度——流式 preview
post 此时只有 1 个字符（实测），所以 TTL 恒为 2 秒下限。
2. 每个 `post_edited` 都调 `markStreamingEdit`，而
`useMmTypewriter.ts:104-106` 对 `streamingEditIds` 里的 id 直接
`evictTypewriter`。

结果：`posted` 后 2 秒内被 evict，2 秒后彻底移出 `recentBotMessageIds`，整个 40+
秒的流式过程打字机一次都没跑。

**外加两个衍生问题**：动画追平后会删掉全部状态，导致后续编辑**从 index 0 重播整条回答**；而 `post_deleted`
完全未接线（全仓仅在 `websocket.ts` 的枚举里出现），被删的 preview post 永远留在 store
里造成重复展示。后者已用 staging DOM 查询确认——标题字符串在页面中出现 2 次。

## 改动

- **打字机改为服务流式而非排除流式**：去掉 `streamingEditIds → evict`；单条 rAF 循环替代 per-id
`setTimeout(16)`。
- **自适应配速**：每帧推进 `remaining * dt / budgetLeft`，任意大小的 backlog 都在
~`DRAIN_MS`(1200ms) 内排空。原先固定 3 字符/16ms（约 187 字符/秒）追不上 bot
的突发节奏，即使跑起来也是"冲一段停一段"。
- **追平后保留状态**，后续编辑续播而非重播。
- **接上 `post_deleted`**，调用早已存在但从未被调用的 `removePost`。
- **无缝接管**：按 `zooclaw_root_post_id` 把 preview 的渲染进度交给替代它的 final post。注意
final post 实测比 `post_deleted` **早到 ~100ms**，所以 credit pool 在 preview
播放过程中持续更新，而不是等它退休才结算。
- **`useLayoutEffect`** 而非 `useEffect`：新 post 首帧会以完整内容渲染，必须在 paint
前拉回接管偏移量，否则文字会先出现再缩回。

## Test plan

- [x] `bash scripts/verify-web.sh` 全过：532 test files / 7160
tests、tsc、eslint、全部治理守卫
- [x] 新增 5 个单测覆盖：流式消息走打字机、离开 `recentBotMessageIds` 后动画不被掐断、增长时续播不重播、大小
backlog 排空时间接近、preview→final 接管（**含 final 先到、delete 后到的真实时序**）、历史消息即时渲染
- [x] 新增 3 个单测覆盖 `post_deleted` 分发
- [x] CDP 实测 staging（修复前）+ 本地构建连 staging 后端（修复前/后**同构对比**）

实测结果（同一构建，仅代码不同）：

| 指标 | 修复前 | 修复后 |
|---|---|---|
| DOM 更新间隔 p95 | 1220ms | **96.7ms** |
| 每次增量均值 | 30.1 字符 | 10.2 字符 |
| 流式结束后重播 | +110 次更新 | +22 次 |
| 单条消息文字倒退 | — | **0** |

## Reviewer notes

**已知代价，需要合并后在 staging 复测。** 打字机真正跑起来后，`useMmTypewriter`
每帧重建整个消息数组变成了稳态成本，且与线程消息数成正比。dev 构建下 >33ms 的帧从 2% 升到约 15%，32 条 bot
消息的线程里 long task 从 90 涨到 135。

但**生产构建下的影响未测量**：同一份修复前的代码在 prod 构建是 0 个 long task、dev 构建是 90 个，dev
有约一个数量级的放大。按比例推算 prod 增量应该很小，但这是推断不是测量。建议合并后在 staging
复测，据此决定是否立刻跟进"把流式文本抽到独立叶子组件"的重构（spec 第五节 P1）。

**一个指标勘误**：原 spec 里"字符写入放大比接近 1.0"是错的，实测稳定在 ~2.5×。preview 显示后被删、final
post 再插入同样文本，DOM 必然记两次写入——这是后端 preview→final
架构的固有开销，不是重播。判定重播应改用单条消息是否倒退 + 结束后是否仍有打字爆发。

**不在本 PR 范围**：`zooclaw-extras` 的 `MATTERMOST_STREAM_MAX_CHARS = 4000`
硬上限会让长回答流到 4000 字后冻结（带 `...` 尾巴）直到生成结束，属于独立的后端问题。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

- 流式回复的打字机**在流式期间从来没运行过**，原始 WS 分片直接上屏——每 ~1.24 秒蹦 ~74 个字符，这就是"卡顿"的全部来源。本 PR 让打字机接管流式消息，并按 backlog 自适应配速。
- 顺带修掉一个更严重、且此前没人发现的 bug：前端从不处理 `post_deleted`，**每次长回答的前 4000 字符都会在界面上重复显示一遍**。
- 调查报告 + 实测数据：`docs/superpowers/specs/2026-07-21-chat-streaming-smoothness.md`

## Root cause

打字机被两个机制夹出了一个**零长度的启动窗口**：

1. `useMattermost.ts:102-103` 的 `markRecentBot(post.id, post.message.length)` 只在 `posted` 触发一次，而 `useMattermostTyping.ts:140` 的 `removeDelay = Math.max(2000, messageLength * 5)` 用的是那一刻的长度——流式 preview post 此时只有 1 个字符（实测），所以 TTL 恒为 2 秒下限。
2. 每个 `post_edited` 都调 `markStreamingEdit`，而 `useMmTypewriter.ts:104-106` 对 `streamingEditIds` 里的 id 直接 `evictTypewriter`。

结果：`posted` 后 2 秒内被 evict，2 秒后彻底移出 `recentBotMessageIds`，整个 40+ 秒的流式过程打字机一次都没跑。

**外加两个衍生问题**：动画追平后会删掉全部状态，导致后续编辑**从 index 0 重播整条回答**；而 `post_deleted` 完全未接线（全仓仅在 `websocket.ts` 的枚举里出现），被删的 preview post 永远留在 store 里造成重复展示。后者已用 staging DOM 查询确认——标题字符串在页面中出现 2 次。

## 改动

- **打字机改为服务流式而非排除流式**：去掉 `streamingEditIds → evict`；单条 rAF 循环替代 per-id `setTimeout(16)`。
- **自适应配速**：每帧推进 `remaining * dt / budgetLeft`，任意大小的 backlog 都在 ~`DRAIN_MS`(1200ms) 内排空。原先固定 3 字符/16ms（约 187 字符/秒）追不上 bot 的突发节奏，即使跑起来也是"冲一段停一段"。
- **追平后保留状态**，后续编辑续播而非重播。
- **接上 `post_deleted`**，调用早已存在但从未被调用的 `removePost`。
- **无缝接管**：按 `zooclaw_root_post_id` 把 preview 的渲染进度交给替代它的 final post。注意 final post 实测比 `post_deleted` **早到 ~100ms**，所以 credit pool 在 preview 播放过程中持续更新，而不是等它退休才结算。
- **`useLayoutEffect`** 而非 `useEffect`：新 post 首帧会以完整内容渲染，必须在 paint 前拉回接管偏移量，否则文字会先出现再缩回。

## Test plan

- [x] `bash scripts/verify-web.sh` 全过：532 test files / 7160 tests、tsc、eslint、全部治理守卫
- [x] 新增 5 个单测覆盖：流式消息走打字机、离开 `recentBotMessageIds` 后动画不被掐断、增长时续播不重播、大小 backlog 排空时间接近、preview→final 接管（**含 final 先到、delete 后到的真实时序**）、历史消息即时渲染
- [x] 新增 3 个单测覆盖 `post_deleted` 分发
- [x] CDP 实测 staging（修复前）+ 本地构建连 staging 后端（修复前/后**同构对比**）

实测结果（同一构建，仅代码不同）：

| 指标 | 修复前 | 修复后 |
|---|---|---|
| DOM 更新间隔 p95 | 1220ms | **96.7ms** |
| 每次增量均值 | 30.1 字符 | 10.2 字符 |
| 流式结束后重播 | +110 次更新 | +22 次 |
| 单条消息文字倒退 | — | **0** |

## Reviewer notes

**已知代价，需要合并后在 staging 复测。** 打字机真正跑起来后，`useMmTypewriter` 每帧重建整个消息数组变成了稳态成本，且与线程消息数成正比。dev 构建下 >33ms 的帧从 2% 升到约 15%，32 条 bot 消息的线程里 long task 从 90 涨到 135。

但**生产构建下的影响未测量**：同一份修复前的代码在 prod 构建是 0 个 long task、dev 构建是 90 个，dev 有约一个数量级的放大。按比例推算 prod 增量应该很小，但这是推断不是测量。建议合并后在 staging 复测，据此决定是否立刻跟进"把流式文本抽到独立叶子组件"的重构（spec 第五节 P1）。

**一个指标勘误**：原 spec 里"字符写入放大比接近 1.0"是错的，实测稳定在 ~2.5×。preview 显示后被删、final post 再插入同样文本，DOM 必然记两次写入——这是后端 preview→final 架构的固有开销，不是重播。判定重播应改用单条消息是否倒退 + 结束后是否仍有打字爆发。

**不在本 PR 范围**：`zooclaw-extras` 的 `MATTERMOST_STREAM_MAX_CHARS = 4000` 硬上限会让长回答流到 4000 字后冻结（带 `...` 尾巴）直到生成结束，属于独立的后端问题。

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(design-system): add composer UI components (#2986)

- **SHA**: 0251b91be31a0987fa6fd32fe4014d1270d38514
- **作者**: lynn Zhuang
- **日期**: 2026-07-21T10:23:40Z
- **PR**: #2986

### Commit Message

```
feat(design-system): add composer UI components (#2986)

## Linear

N/A

## Summary
- extract the composer button, model picker dropdown, hover detail
panel, tooltip, and attachment tag patterns into the ZooClaw Design
System
- preserve the interaction states and visual values from #2865,
including model assets, loading/saving/managed/error states, selected
rows, hover details, and the always-arrow tooltip
- update the component exports, semantic tokens, package assets, tests,
and interactive preview for light and neutral dark themes

## Test plan
- [x] `pnpm --filter @zooclaw/design-system test` (54 files, 296 tests)
- [x] `pnpm --filter @zooclaw/design-system tsc`
- [x] `pnpm --filter @zooclaw/design-system lint`
- [x] `pnpm --filter @zooclaw/design-system build:preview`
- [x] browser-verified model picker hover/leave behavior, PR geometry,
tooltip arrow, and light/dark tooltip tokens at `http://localhost:5180/`
- [x] merged latest `origin/main` and re-ran the package validation

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>
```

### PR Body

## Linear

N/A

## Summary
- extract the composer button, model picker dropdown, hover detail panel, tooltip, and attachment tag patterns into the ZooClaw Design System
- preserve the interaction states and visual values from #2865, including model assets, loading/saving/managed/error states, selected rows, hover details, and the always-arrow tooltip
- update the component exports, semantic tokens, package assets, tests, and interactive preview for light and neutral dark themes

## Test plan
- [x] `pnpm --filter @zooclaw/design-system test` (54 files, 296 tests)
- [x] `pnpm --filter @zooclaw/design-system tsc`
- [x] `pnpm --filter @zooclaw/design-system lint`
- [x] `pnpm --filter @zooclaw/design-system build:preview`
- [x] browser-verified model picker hover/leave behavior, PR geometry, tooltip arrow, and light/dark tooltip tokens at `http://localhost:5180/`
- [x] merged latest `origin/main` and re-ran the package validation


---

## refactor(chat-ui): extract ERMP card renderers into @zooclaw/chat-ui (#2985)

- **SHA**: 33580b0ee0561edf74921a4f2d322de1dcfc4a26
- **作者**: bill-srp
- **日期**: 2026-07-21T10:19:45Z
- **PR**: #2985

### Commit Message

```
refactor(chat-ui): extract ERMP card renderers into @zooclaw/chat-ui (#2985)

## Summary

PR **A** of the ERMP card extraction — the **package-only, additive**
step. Moves the ERMP card render layer (8 cards + dispatcher) into
`@zooclaw/chat-ui` as pure, prop-driven components. **No `web/app` or
docs changes**, so nothing consumes these yet — the app switch happens
in PR B.

Spec/plan:
`docs/superpowers/plans/2026-07-21-chat-ui-ermp-card-extraction.md` (PR
A = Tasks 1–7), merged via #2984.

## What changed (all `web/packages/chat-ui`)

- **New `src/ermp/`**: `types.ts` (the `ERMPCard` union), `utils.ts`
(`formatFileSize` B→TB, `formatDuration`; re-exports `browserMimeType`
from `attachments/utils`), the 8 cards under `cards/`,
`ERMPCardRenderer.tsx` (dispatches on `card._card`), and a barrel.
- **App couplings replaced with injected props** (the whole point of
making these package-safe):
- `readOnly?: boolean` (default `false`) replaces
`useIsReplayReadOnly()`.
- `isSubmitted?: (cardId?) => boolean` (default `() => false`) replaces
the module-global submit `Set` read. Threaded through the dispatcher
**and** `CompositeCard` so nested actions/forms resolve their state. The
package cards keep only their local optimistic `已提交` toggle and no
longer call `markCardSubmitted` — PR B's app wrapper records submission.
- **Root barrel**: exports `ERMPCardRenderer` + the `ERMPCard` types.
The `VideoCard` name is split cleanly — the existing **attachment**
`VideoCard` stays a value export (the app's `ReplayAttachment` imports
it), the new **ERMP** `VideoCard` is a type export (value/type
namespaces don't collide). `module-structure.test.ts` gains a `VideoCard
=== RootVideoCard` assertion pinning that.

## Preservation

- Card markup, classNames, `data-testid`s, and Chinese labels (`已提交` /
`已复制` / `请选择` / `提交`) are byte-for-byte from the app source.
- `formatFileSize` (B→TB) is kept **distinct** from the existing
`formatAttachmentSize` (MB max) — they diverge ≥ 1 GB.
- ERMP's `BROWSER_AUDIO_TYPES` was confirmed equal to the attachments
set before reusing `browserMimeType`.
- No new dependencies (`@heroicons/react` already present). `'use
client'` dropped to match sibling package convention.

## Test plan

- [x] Package gate from `web/packages/chat-ui`: **`tsc` 0 errors ·
vitest 25 files / 252 tests pass · eslint 0/0** (verified independently,
not just by the implementer).
- [x] 4 new native-DOM test suites (no jest-dom): `ermp-utils`,
`ermp-data-cards`, `ermp-interactive-cards`, `ermp-renderer` — cover
kind dispatch, `readOnly` disabling callback/form (link/copy still
active), `isSubmitted` initial state, `CompositeCard` nesting, and media
`browserMimeType` gating.
- [x] `web/app` + `docs` untouched (`git diff --stat origin/main --
web/app docs` empty).
- [ ] CI `web-build-check` / CodeQL run on this PR.
```

### PR Body

## Summary

PR **A** of the ERMP card extraction — the **package-only, additive** step. Moves the ERMP card render layer (8 cards + dispatcher) into `@zooclaw/chat-ui` as pure, prop-driven components. **No `web/app` or docs changes**, so nothing consumes these yet — the app switch happens in PR B.

Spec/plan: `docs/superpowers/plans/2026-07-21-chat-ui-ermp-card-extraction.md` (PR A = Tasks 1–7), merged via #2984.

## What changed (all `web/packages/chat-ui`)

- **New `src/ermp/`**: `types.ts` (the `ERMPCard` union), `utils.ts` (`formatFileSize` B→TB, `formatDuration`; re-exports `browserMimeType` from `attachments/utils`), the 8 cards under `cards/`, `ERMPCardRenderer.tsx` (dispatches on `card._card`), and a barrel.
- **App couplings replaced with injected props** (the whole point of making these package-safe):
  - `readOnly?: boolean` (default `false`) replaces `useIsReplayReadOnly()`.
  - `isSubmitted?: (cardId?) => boolean` (default `() => false`) replaces the module-global submit `Set` read. Threaded through the dispatcher **and** `CompositeCard` so nested actions/forms resolve their state. The package cards keep only their local optimistic `已提交` toggle and no longer call `markCardSubmitted` — PR B's app wrapper records submission.
- **Root barrel**: exports `ERMPCardRenderer` + the `ERMPCard` types. The `VideoCard` name is split cleanly — the existing **attachment** `VideoCard` stays a value export (the app's `ReplayAttachment` imports it), the new **ERMP** `VideoCard` is a type export (value/type namespaces don't collide). `module-structure.test.ts` gains a `VideoCard === RootVideoCard` assertion pinning that.

## Preservation

- Card markup, classNames, `data-testid`s, and Chinese labels (`已提交` / `已复制` / `请选择` / `提交`) are byte-for-byte from the app source.
- `formatFileSize` (B→TB) is kept **distinct** from the existing `formatAttachmentSize` (MB max) — they diverge ≥ 1 GB.
- ERMP's `BROWSER_AUDIO_TYPES` was confirmed equal to the attachments set before reusing `browserMimeType`.
- No new dependencies (`@heroicons/react` already present). `'use client'` dropped to match sibling package convention.

## Test plan

- [x] Package gate from `web/packages/chat-ui`: **`tsc` 0 errors · vitest 25 files / 252 tests pass · eslint 0/0** (verified independently, not just by the implementer).
- [x] 4 new native-DOM test suites (no jest-dom): `ermp-utils`, `ermp-data-cards`, `ermp-interactive-cards`, `ermp-renderer` — cover kind dispatch, `readOnly` disabling callback/form (link/copy still active), `isSubmitted` initial state, `CompositeCard` nesting, and media `browserMimeType` gating.
- [x] `web/app` + `docs` untouched (`git diff --stat origin/main -- web/app docs` empty).
- [ ] CI `web-build-check` / CodeQL run on this PR.


---

## docs: add chat UI ERMP card extraction spec and plan (#2984)

- **SHA**: 59ea40e10c6275481d169408be42d36167b904de
- **作者**: bill-srp
- **日期**: 2026-07-21T09:30:13Z
- **PR**: #2984

### Commit Message

```
docs: add chat UI ERMP card extraction spec and plan (#2984)

## Summary

Design spec + implementation plan for the next `@zooclaw/chat-ui`
extraction slice: the **ERMP card render layer** (the 8 card components
+ dispatcher). Docs-only — no code. Follows the initiative's docs-first
gate (same as the attachment slice #2974).

**Why ERMP is a clean candidate** (verified against source): the render
layer's only couplings are `react` + `@heroicons/react` (already a
package dep), pure `ERMPCard` types, formatters, and — the only app
couplings — `useIsReplayReadOnly` (context) and a module-global submit
`Set`. No i18n, no `next/*`, no react-query/firebase, no
`MarkdownContent` recursion. That's why ERMP is extractable where the
**thread** is not (it would drag `@assistant-ui/react` into the package)
and the **specialist cards** are not (markdown-recursive + consent/nav).

## Design highlights

- **Parse app-side, render package-side.** App keeps
`parseERMPCard`/`extractEcapCardBlocks`/`detectMediaCards` +
Mattermost-prop plumbing; the package renders typed view-models. The
`@/components/ermp` import surface is preserved via a thin app
`ERMPCardRenderer` wrapper, so
`OpenClawAssistantMessage`/`UserMessage`/`ERMPCardSegment` and their
specs stay untouched (the regression harness).
- **Submit-state: lift, don't move.** Replaces the two app couplings
with injected props — `readOnly?: boolean` and `isSubmitted?: (cardId?)
=> boolean` — threaded through the dispatcher and `CompositeCard` into
nested cards. The mutable `Set` stays in the app; the package stays free
of module-global state. Fallback documented if review prefers minimal
risk over cleanliness.
- **Formatter compat (the attachment-slice lesson):** ERMP's
`formatFileSize` (B→TB) is kept **distinct** from the package's
`formatAttachmentSize` (stops at MB); `browserMimeType` is **reused**
from `attachments/utils` (pending a set-equality check);
`formatDuration` is net-new.

## Delivery

- **PR A** (Tasks 1–7): package-only, additive — types, formatters, 8
cards, dispatcher, barrel + native-DOM tests.
- **PR B** (Tasks 8–12): app-only, replace — parsers/submit-state stay,
thin `ERMPCardRenderer` wrapper, delete moved cards, move card specs to
the package.

Codex implements each PR via `codex:rescue`; Claude verifies
independently + runs PR mechanics.

## Files

-
`docs/superpowers/specs/2026-07-21-chat-ui-ermp-card-extraction-design.md`
- `docs/superpowers/plans/2026-07-21-chat-ui-ermp-card-extraction.md`

## Test plan

- [x] Docs-only; no code paths touched. `git diff --stat origin/main --
web` is empty.
- [ ] Review the parse/render split + the submit-state injection design
before implementation.
```

### PR Body

## Summary

Design spec + implementation plan for the next `@zooclaw/chat-ui` extraction slice: the **ERMP card render layer** (the 8 card components + dispatcher). Docs-only — no code. Follows the initiative's docs-first gate (same as the attachment slice #2974).

**Why ERMP is a clean candidate** (verified against source): the render layer's only couplings are `react` + `@heroicons/react` (already a package dep), pure `ERMPCard` types, formatters, and — the only app couplings — `useIsReplayReadOnly` (context) and a module-global submit `Set`. No i18n, no `next/*`, no react-query/firebase, no `MarkdownContent` recursion. That's why ERMP is extractable where the **thread** is not (it would drag `@assistant-ui/react` into the package) and the **specialist cards** are not (markdown-recursive + consent/nav).

## Design highlights

- **Parse app-side, render package-side.** App keeps `parseERMPCard`/`extractEcapCardBlocks`/`detectMediaCards` + Mattermost-prop plumbing; the package renders typed view-models. The `@/components/ermp` import surface is preserved via a thin app `ERMPCardRenderer` wrapper, so `OpenClawAssistantMessage`/`UserMessage`/`ERMPCardSegment` and their specs stay untouched (the regression harness).
- **Submit-state: lift, don't move.** Replaces the two app couplings with injected props — `readOnly?: boolean` and `isSubmitted?: (cardId?) => boolean` — threaded through the dispatcher and `CompositeCard` into nested cards. The mutable `Set` stays in the app; the package stays free of module-global state. Fallback documented if review prefers minimal risk over cleanliness.
- **Formatter compat (the attachment-slice lesson):** ERMP's `formatFileSize` (B→TB) is kept **distinct** from the package's `formatAttachmentSize` (stops at MB); `browserMimeType` is **reused** from `attachments/utils` (pending a set-equality check); `formatDuration` is net-new.

## Delivery

- **PR A** (Tasks 1–7): package-only, additive — types, formatters, 8 cards, dispatcher, barrel + native-DOM tests.
- **PR B** (Tasks 8–12): app-only, replace — parsers/submit-state stay, thin `ERMPCardRenderer` wrapper, delete moved cards, move card specs to the package.

Codex implements each PR via `codex:rescue`; Claude verifies independently + runs PR mechanics.

## Files

- `docs/superpowers/specs/2026-07-21-chat-ui-ermp-card-extraction-design.md`
- `docs/superpowers/plans/2026-07-21-chat-ui-ermp-card-extraction.md`

## Test plan

- [x] Docs-only; no code paths touched. `git diff --stat origin/main -- web` is empty.
- [ ] Review the parse/render split + the submit-state injection design before implementation.


---

## feat(web): engine agent channels in the settings hub (#2977)

- **SHA**: bab527dbbe3850c38ed7360d00570d178a305475
- **作者**: bill-srp
- **日期**: 2026-07-21T08:51:43Z
- **PR**: #2977

### Commit Message

```
feat(web): engine agent channels in the settings hub (#2977)

## Summary

Final slice of engine agent channels (ECA-1279) — the claw-settings
Channels hub is extended so installed engine agents become first-class
channel targets. With this, all four v1 platforms work end-to-end:
**Slack / Feishu / WeCom via manual credential entry** (pure passthrough
through E1's CRUD → ACS) and **Weixin via its QR modal** (pointed at the
#2973 engine setup endpoints).

Linear: https://linear.app/srpone/issue/ECA-1279
Spec:
`docs/superpowers/specs/2026-07-20-engine-agent-channels-design.md`
Plan:
`docs/superpowers/plans/2026-07-20-engine-channels-frontend-hub.md`
Depends on: E1 (#2957) + weixin-backend (#2973), both merged.

### What's new

- **Target selection** (`lib/agent-list.ts`, `channels/helpers.ts`) —
`selectChannelTargetEngineAgents` (active engine rows) for the ADD
picker, `selectChannelListEngineAgents` (non-terminal) for the merged
LIST so an unhealthy workspace's channels stay visible/removable.
`ChannelAgentOption` gains a `kind` discriminant.
- **BFF proxies** (`api/agents/[workspaceId]/channels/**`,
`_lib/channel-proxy.ts`) mirroring the `[workspaceId]/start` pattern,
gated by a **tri-state** `resolveAllowlistVerdict`
(`_lib/allowlist.ts`): `allowlisted`→proceed, `not_allowlisted`→404,
`unavailable`→502 (an account-resolution outage is never collapsed into
404). The install route is refactored onto the verdict helper with
behavior preserved bit-for-bit.
- **Client API + hook** (`lib/api/agent-channels.ts`,
`hooks/queries/agents/useEngineAgentChannels.ts`) — uid-scoped
per-workspace channel queries.
- **Hub wiring** (`ClawSettingsClient`, `ChannelsSection`,
`useAddChannelForm`, `AddChannelModalParts`, `ChannelCard`,
`StatusBadge`, `WeixinSetupModal`, new
`EngineChannelCards`/`EngineChannelEditModal`) — engine targets use the
manual-entry path for Slack/Feishu/WeCom and the QR modal (engine
endpoints, `dm_policy` only) for Weixin; **dm_policy/group_policy
default `open`/`open` matching the computer agent**; **pairing
excluded** for engine and its card action suppressed; engine cards show
the workspace label with no `Target Agent` line / no bound-agent select
and no `agent_id` in the submission; `StatusBadge` maps ACS `status` +
`health` (unknown→neutral, not silent green); the `botRunning` gate
scopes to the bot subtree so engine channels stay manageable when the
computer bot is down.

## Test plan

- [x] `bash scripts/verify-web.sh` — guards + tsc + 523 test files /
7035 tests + eslint, all green
- [x] `pnpm test:unit:coverage` — 87.85% stmts / 80.99% branches /
86.64% funcs / 90.21% lines (above ratchet 83/75/81/85)
- [x] `pnpm lint:deadcode && pnpm dup` — clean
- [x] New specs: target selectors, tri-state allowlist BFF (incl.
`unavailable`→502, install unchanged), client API + hook, engine
manual-entry submit carries no `agent_id`, ChannelCard
pairing-suppressed + health, StatusBadge ACS enum, WeixinSetupModal
engine wiring
- [ ] CI `code-quality / lint-and-test`
- [ ] Recommended manual: mock-stack visual smoke (`dev-mock` + connect
a Feishu channel via manual entry + Weixin QR mock) — not run here

## Rollout / risk

Frontend-only; engine operations gated by `AGENTS_V2_EMAIL_ALLOWLIST` at
the BFF. No bot-leg channel behavior changes (bot targets keep the full
platform list + guided wizards). After this + a web release, widening
the allowlist enables the feature. Accepted v1 limitations carried from
the backend: no pairing for engine channels (no ACS approve endpoint);
Weixin completion is client-poll-driven (re-scan recovers).
```

### PR Body

## Summary

Final slice of engine agent channels (ECA-1279) — the claw-settings Channels hub is extended so installed engine agents become first-class channel targets. With this, all four v1 platforms work end-to-end: **Slack / Feishu / WeCom via manual credential entry** (pure passthrough through E1's CRUD → ACS) and **Weixin via its QR modal** (pointed at the #2973 engine setup endpoints).

Linear: https://linear.app/srpone/issue/ECA-1279
Spec: `docs/superpowers/specs/2026-07-20-engine-agent-channels-design.md`
Plan: `docs/superpowers/plans/2026-07-20-engine-channels-frontend-hub.md`
Depends on: E1 (#2957) + weixin-backend (#2973), both merged.

### What's new

- **Target selection** (`lib/agent-list.ts`, `channels/helpers.ts`) — `selectChannelTargetEngineAgents` (active engine rows) for the ADD picker, `selectChannelListEngineAgents` (non-terminal) for the merged LIST so an unhealthy workspace's channels stay visible/removable. `ChannelAgentOption` gains a `kind` discriminant.
- **BFF proxies** (`api/agents/[workspaceId]/channels/**`, `_lib/channel-proxy.ts`) mirroring the `[workspaceId]/start` pattern, gated by a **tri-state** `resolveAllowlistVerdict` (`_lib/allowlist.ts`): `allowlisted`→proceed, `not_allowlisted`→404, `unavailable`→502 (an account-resolution outage is never collapsed into 404). The install route is refactored onto the verdict helper with behavior preserved bit-for-bit.
- **Client API + hook** (`lib/api/agent-channels.ts`, `hooks/queries/agents/useEngineAgentChannels.ts`) — uid-scoped per-workspace channel queries.
- **Hub wiring** (`ClawSettingsClient`, `ChannelsSection`, `useAddChannelForm`, `AddChannelModalParts`, `ChannelCard`, `StatusBadge`, `WeixinSetupModal`, new `EngineChannelCards`/`EngineChannelEditModal`) — engine targets use the manual-entry path for Slack/Feishu/WeCom and the QR modal (engine endpoints, `dm_policy` only) for Weixin; **dm_policy/group_policy default `open`/`open` matching the computer agent**; **pairing excluded** for engine and its card action suppressed; engine cards show the workspace label with no `Target Agent` line / no bound-agent select and no `agent_id` in the submission; `StatusBadge` maps ACS `status` + `health` (unknown→neutral, not silent green); the `botRunning` gate scopes to the bot subtree so engine channels stay manageable when the computer bot is down.

## Test plan

- [x] `bash scripts/verify-web.sh` — guards + tsc + 523 test files / 7035 tests + eslint, all green
- [x] `pnpm test:unit:coverage` — 87.85% stmts / 80.99% branches / 86.64% funcs / 90.21% lines (above ratchet 83/75/81/85)
- [x] `pnpm lint:deadcode && pnpm dup` — clean
- [x] New specs: target selectors, tri-state allowlist BFF (incl. `unavailable`→502, install unchanged), client API + hook, engine manual-entry submit carries no `agent_id`, ChannelCard pairing-suppressed + health, StatusBadge ACS enum, WeixinSetupModal engine wiring
- [ ] CI `code-quality / lint-and-test`
- [ ] Recommended manual: mock-stack visual smoke (`dev-mock` + connect a Feishu channel via manual entry + Weixin QR mock) — not run here

## Rollout / risk

Frontend-only; engine operations gated by `AGENTS_V2_EMAIL_ALLOWLIST` at the BFF. No bot-leg channel behavior changes (bot targets keep the full platform list + guided wizards). After this + a web release, widening the allowlist enables the feature. Accepted v1 limitations carried from the backend: no pairing for engine channels (no ACS approve endpoint); Weixin completion is client-poll-driven (re-scan recovers).


---

## refactor(web): render attachments via @zooclaw/chat-ui (#2982)

- **SHA**: 9cc898c21b1cf24280bd7b41a65ecba11adaeab5
- **作者**: bill-srp
- **日期**: 2026-07-21T08:12:32Z
- **PR**: #2982

### Commit Message

```
refactor(web): render attachments via @zooclaw/chat-ui (#2982)

## Summary

PR **B** of the chat-UI attachment extraction — the **replace** step.
Rewrites the app Mattermost attachment path to consume the
`@zooclaw/chat-ui` renderers merged in PR A (#2979). `MMAttachments`
keeps its exact props, so all four consumers are untouched.

Completes the slice: docs #2974 → package extract #2979 → this replace
PR.

Spec/plan:
`docs/superpowers/plans/2026-07-21-chat-ui-attachment-extraction.md` (PR
B = Tasks 6–8).

## What changed (9 files, all `web/app`)

- **Per-kind chat resolvers** (`attachments/ImageAttachment` /
`VideoAttachment` / `AudioAttachment` / `FileAttachment`): now thin
wrappers — `useMMAuth` + `useAuthBlob` → `AttachmentView` → the package
leaf. They **always pass `onPreview`/`onDownload` closures** (a no-op
when the optional preview provider is absent), so image/video
interactivity is preserved on no-provider surfaces (mini-chat /
agent-builder), exactly as today.
- **`MMAttachments`**: renders the package `<AttachmentGallery>` (keeps
its `AttachmentRenderer` replay-vs-chat dispatch); props unchanged.
- **`ReplayAttachment`**: import-only — `VideoCard` /
`formatAttachmentSize` / `largeImageBoxStyle` now resolve from
`@zooclaw/chat-ui`; DOM/logic byte-identical.
- **Deleted** (moved to the package): `attachments/VideoCard.tsx`,
`ScrollableImageRow.tsx`, `attachment-utils.ts`.

## Test plan

- [x] `bash scripts/verify-web.sh` — guards + `tsc` + vitest (**517
files / 6990 tests pass**) + eslint, all green.
- [x] **Four protected specs pass with zero edits** (35 tests):
`MMAttachments.unit.spec`, `MMAttachmentsNoPreviewProvider.unit.spec`,
`ReplayPlayer.unit.spec`, `ReplayClient.unit.spec` — the regression
harness (image layout-box inline styles, click→preview, file
synchronous-revoke download, no-provider rendering).
- [x] Coverage ratchet holds: statements 87.9 / branches 81.07 /
functions 86.7 / lines 90.24 (thresholds 83 / 75 / 81 / 85).
- [x] **`/chat` browser check** (mock-login): chat surface loads
logged-in and renders with **zero React / provider / component console
errors** — the resolvers + shared
`AttachmentGallery`/`ScrollableImageRow` layout mount cleanly in the
live app. (Lone console error is a mock-backend `401` on a resource
fetch — the known mock-auth artifact; warns are pre-existing Next
preload hints.)
- [~] **`/share` browser check**: the replay page loads with no console
errors / no crash, but the mock replay *snapshot* returns
`not_found_or_revoked` through the BFF (a pre-existing mock/BFF
replay-wiring limitation, unrelated to this change), so the replay
attachments couldn't be visually exercised in the mock. The
`/share`-specific risk is the shared gallery/scroll **layout** — which
is the same package code verified error-free on `/chat` — plus the
byte-identical `ReplayAttachment` leaf and the passing
`ReplayPlayer`/`ReplayClient` specs.
- [ ] CI `web-build-check` (`next build`) — runs on this PR.

`OpenClawThread` and the message-renderer containers are untouched (they
mock `MMAttachments` via slots). Scope confined to `web/app` (9 files);
package + docs untouched.
```

### PR Body

## Summary

PR **B** of the chat-UI attachment extraction — the **replace** step. Rewrites the app Mattermost attachment path to consume the `@zooclaw/chat-ui` renderers merged in PR A (#2979). `MMAttachments` keeps its exact props, so all four consumers are untouched.

Completes the slice: docs #2974 → package extract #2979 → this replace PR.

Spec/plan: `docs/superpowers/plans/2026-07-21-chat-ui-attachment-extraction.md` (PR B = Tasks 6–8).

## What changed (9 files, all `web/app`)

- **Per-kind chat resolvers** (`attachments/ImageAttachment` / `VideoAttachment` / `AudioAttachment` / `FileAttachment`): now thin wrappers — `useMMAuth` + `useAuthBlob` → `AttachmentView` → the package leaf. They **always pass `onPreview`/`onDownload` closures** (a no-op when the optional preview provider is absent), so image/video interactivity is preserved on no-provider surfaces (mini-chat / agent-builder), exactly as today.
- **`MMAttachments`**: renders the package `<AttachmentGallery>` (keeps its `AttachmentRenderer` replay-vs-chat dispatch); props unchanged.
- **`ReplayAttachment`**: import-only — `VideoCard` / `formatAttachmentSize` / `largeImageBoxStyle` now resolve from `@zooclaw/chat-ui`; DOM/logic byte-identical.
- **Deleted** (moved to the package): `attachments/VideoCard.tsx`, `ScrollableImageRow.tsx`, `attachment-utils.ts`.

## Test plan

- [x] `bash scripts/verify-web.sh` — guards + `tsc` + vitest (**517 files / 6990 tests pass**) + eslint, all green.
- [x] **Four protected specs pass with zero edits** (35 tests): `MMAttachments.unit.spec`, `MMAttachmentsNoPreviewProvider.unit.spec`, `ReplayPlayer.unit.spec`, `ReplayClient.unit.spec` — the regression harness (image layout-box inline styles, click→preview, file synchronous-revoke download, no-provider rendering).
- [x] Coverage ratchet holds: statements 87.9 / branches 81.07 / functions 86.7 / lines 90.24 (thresholds 83 / 75 / 81 / 85).
- [x] **`/chat` browser check** (mock-login): chat surface loads logged-in and renders with **zero React / provider / component console errors** — the resolvers + shared `AttachmentGallery`/`ScrollableImageRow` layout mount cleanly in the live app. (Lone console error is a mock-backend `401` on a resource fetch — the known mock-auth artifact; warns are pre-existing Next preload hints.)
- [~] **`/share` browser check**: the replay page loads with no console errors / no crash, but the mock replay *snapshot* returns `not_found_or_revoked` through the BFF (a pre-existing mock/BFF replay-wiring limitation, unrelated to this change), so the replay attachments couldn't be visually exercised in the mock. The `/share`-specific risk is the shared gallery/scroll **layout** — which is the same package code verified error-free on `/chat` — plus the byte-identical `ReplayAttachment` leaf and the passing `ReplayPlayer`/`ReplayClient` specs.
- [ ] CI `web-build-check` (`next build`) — runs on this PR.

`OpenClawThread` and the message-renderer containers are untouched (they mock `MMAttachments` via slots). Scope confined to `web/app` (9 files); package + docs untouched.


---

## fix(chat): show controls in workspace history (#2981)

- **SHA**: ea0753cb6c97d53b03b3b4cab6eff394f613f65a
- **作者**: kaka-srp
- **日期**: 2026-07-21T08:12:56Z
- **PR**: #2981

### Commit Message

```
fix(chat): show controls in workspace history (#2981)

## Summary

- Keep Share, Files, and Settings controls visible in normal
computer-runtime workspace chats.
- Restrict the compact chat header to computers identified as Pack Test
previews.
- Add regression coverage for both normal workspace and Pack Test
routes.

## Root cause

`GenClawClient` used `!!computerId` as a proxy for Pack Test mode.
Normal computer-runtime agents now also resolve a `computerId` from
`workspace_id`, so opening Session History at `/chat?workspace_id=...`
incorrectly enabled the compact header and hid its controls.

## Test plan

- [x] `bash scripts/verify-web.sh
'web/app/src/app/[locale]/(app)/(chat)/chat/GenClawClient.tsx'
web/app/tests/unit/app/chat/GenClawClient.internals.unit.spec.tsx`
- [x] `bash scripts/verify-changed.sh`
- [x] Regression test: normal computer-runtime workspace chat keeps
header controls visible.
- [x] Regression test: Pack Test chat keeps header controls hidden.

Linear:
https://linear.app/srpone/issue/ECA-1286/web-session-history-打开的会话缺少右上角功能按钮分享文件设置
```

### PR Body

## Summary

- Keep Share, Files, and Settings controls visible in normal computer-runtime workspace chats.
- Restrict the compact chat header to computers identified as Pack Test previews.
- Add regression coverage for both normal workspace and Pack Test routes.

## Root cause

`GenClawClient` used `!!computerId` as a proxy for Pack Test mode. Normal computer-runtime agents now also resolve a `computerId` from `workspace_id`, so opening Session History at `/chat?workspace_id=...` incorrectly enabled the compact header and hid its controls.

## Test plan

- [x] `bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/(chat)/chat/GenClawClient.tsx' web/app/tests/unit/app/chat/GenClawClient.internals.unit.spec.tsx`
- [x] `bash scripts/verify-changed.sh`
- [x] Regression test: normal computer-runtime workspace chat keeps header controls visible.
- [x] Regression test: Pack Test chat keeps header controls hidden.

Linear: https://linear.app/srpone/issue/ECA-1286/web-session-history-打开的会话缺少右上角功能按钮分享文件设置


---

## fix(claw-interface): add computer create diagnostics (#2983)

- **SHA**: 00027e7c678aed1b9be1ce4f8f0ebeb1174295ee
- **作者**: sam-srp
- **日期**: 2026-07-21T08:02:27Z
- **PR**: #2983

### Commit Message

```
fix(claw-interface): add computer create diagnostics (#2983)

## Summary
- add a structured failure event when FastClaw computer creation fails
and no concurrent computer can be recovered
- include create stage and upstream error metadata while truncating user
and organization identifiers
- cover the diagnostic payload and identifier sanitization with a unit
test

## Why
ECA-1275 currently surfaces a 404 during computer creation without
enough request-scoped context to identify which FastClaw operation or
response caused it. This adds a low-volume failure log without changing
API behavior.

## Validation
- `pytest tests/unit/test_computer_service.py -q` (54 passed)
- `ruff check .`
- `ruff format --check .`
- `pyright app/ tests/`
- `lint-imports`

Linear: ECA-1275
```

### PR Body

## Summary
- add a structured failure event when FastClaw computer creation fails and no concurrent computer can be recovered
- include create stage and upstream error metadata while truncating user and organization identifiers
- cover the diagnostic payload and identifier sanitization with a unit test

## Why
ECA-1275 currently surfaces a 404 during computer creation without enough request-scoped context to identify which FastClaw operation or response caused it. This adds a low-volume failure log without changing API behavior.

## Validation
- `pytest tests/unit/test_computer_service.py -q` (54 passed)
- `ruff check .`
- `ruff format --check .`
- `pyright app/ tests/`
- `lint-imports`

Linear: ECA-1275


---

## fix(web): retry transient R2 uploads (ECA-963) (#2980)

- **SHA**: 00ba378e3fd3506ddc12614fdf6e2b5cfb54e410
- **作者**: sam-srp
- **日期**: 2026-07-21T07:23:19Z
- **PR**: #2980

### Commit Message

```
fix(web): retry transient R2 uploads (ECA-963) (#2980)

## Summary

- retry direct R2 PUT uploads after transient network failures and HTTP
5xx responses
- use the same policy as the backend: two retries after the initial
request, with 500ms and 1.5s backoff
- preserve immediate failure for 4xx responses, timeouts, and caller
cancellation
- make AbortError detection work across browser and WebView realms

## Root cause

Cloudflare R2 intermittently returned HTTP 500 for valid, non-expired
presigned PUT requests. The frontend attempted the upload only once, so
a transient upstream failure became a user-visible attachment failure.

## Impact

Transient R2 failures can now recover without user action. A request is
attempted at most three times in total, matching the claw-interface
upload policy.

## Validation

- `pnpm exec vitest run --config ./vitest.config.mts
tests/unit/lib/upload.unit.spec.ts` (26 passed)
- `pnpm exec eslint src/lib/upload.ts tests/unit/lib/upload.unit.spec.ts
--quiet`
- `pnpm exec tsc --noEmit --pretty false`
- `git diff --check`

Linear:
https://linear.app/srpone/issue/ECA-963/frontend-500-on-cloudflare-r2-user-file-upload
```

### PR Body

## Summary

- retry direct R2 PUT uploads after transient network failures and HTTP 5xx responses
- use the same policy as the backend: two retries after the initial request, with 500ms and 1.5s backoff
- preserve immediate failure for 4xx responses, timeouts, and caller cancellation
- make AbortError detection work across browser and WebView realms

## Root cause

Cloudflare R2 intermittently returned HTTP 500 for valid, non-expired presigned PUT requests. The frontend attempted the upload only once, so a transient upstream failure became a user-visible attachment failure.

## Impact

Transient R2 failures can now recover without user action. A request is attempted at most three times in total, matching the claw-interface upload policy.

## Validation

- `pnpm exec vitest run --config ./vitest.config.mts tests/unit/lib/upload.unit.spec.ts` (26 passed)
- `pnpm exec eslint src/lib/upload.ts tests/unit/lib/upload.unit.spec.ts --quiet`
- `pnpm exec tsc --noEmit --pretty false`
- `git diff --check`

Linear: https://linear.app/srpone/issue/ECA-963/frontend-500-on-cloudflare-r2-user-file-upload


---

## feat(chat): unify composer and align Skill Store UI (#2865)

- **SHA**: 1522f23cdd0051c16ab593ea82e739241a7a3497
- **作者**: lynn Zhuang
- **日期**: 2026-07-21T07:13:13Z
- **PR**: #2865

### Commit Message

```
feat(chat): unify composer and align Skill Store UI (#2865)

## Summary

- 让 `/new-chat` 与 chat session 复用同一个 `UnifiedChatComposer`：输入、附件、Recent
files、Library、Skills、Connectors 与模型能力保持一致；Agent 选择仅在 New Chat 展示
- 按页面位置切换菜单展开方向：New Chat 的菜单向下展开，session 底部输入框的菜单向上展开，并保留主线新增的桌面工作目录入口与
`workspace_id` 深链行为
- 将 Library 从页面跳转改为可选择、取消、确认并回到输入框的弹窗流程，保留原有上传文件与 Artifacts 能力
- 全局统一使用 “Skill Store” 文案与 tool/skill 图标；Skill Store 卡片复用 ZooClaw Design
System 的 Card、Tag、Button，并按断点自适应 1 / 2 / 3 列
- 为本地 mock 场景补充 runtime skills，使 Use Skills 面板可直接预览真实列表与放大后的 skill icon

## Root cause

- New Chat 与 session 原先由两套输入框实现，导致附件、模型、Skills、菜单定位和后续交互持续漂移
- Library 与 Skill Store 操作依赖页面跳转，打断了用户从输入到发起/继续任务的连续路径
- Skill 相关入口存在 Market / Store 混用、emoji / wrench / tool 多套图标以及非 Design
System 卡片样式

## Size override rationale

- 本 PR 是统一 composer 迁移的连续分支，现有 `size-override` 标签覆盖 79 个文件、6873 行 diff
- New Chat、session、Library、Skills 与模型菜单共享输入草稿、附件状态、菜单状态和 surface
placement；拆分会产生无法独立验收的中间状态
- 大量 diff 来自配套单元测试、设计文档、mock 场景和图标资源

## Test plan

- [x] `bash scripts/verify-changed.sh` — 合并最新 main 后 TypeScript、ESLint 与
governance guards 全部通过
- [x] 组合回归：10 个 New Chat / session composer / Skill Store 测试文件，289 / 289
tests passed
- [x] 标准前端门禁：289 个测试文件，4022 passed、1 todo；TypeScript 与 ESLint 通过
- [x] 本地 `http://localhost:3003/new-chat` 验证统一输入框、Library 弹窗、Use Skills
列表、Skill Store 卡片与响应式布局
- [x] `git diff --cached --check` 与合并冲突检查通过

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>
```

### PR Body

## Summary

- 让 `/new-chat` 与 chat session 复用同一个 `UnifiedChatComposer`：输入、附件、Recent files、Library、Skills、Connectors 与模型能力保持一致；Agent 选择仅在 New Chat 展示
- 按页面位置切换菜单展开方向：New Chat 的菜单向下展开，session 底部输入框的菜单向上展开，并保留主线新增的桌面工作目录入口与 `workspace_id` 深链行为
- 将 Library 从页面跳转改为可选择、取消、确认并回到输入框的弹窗流程，保留原有上传文件与 Artifacts 能力
- 全局统一使用 “Skill Store” 文案与 tool/skill 图标；Skill Store 卡片复用 ZooClaw Design System 的 Card、Tag、Button，并按断点自适应 1 / 2 / 3 列
- 为本地 mock 场景补充 runtime skills，使 Use Skills 面板可直接预览真实列表与放大后的 skill icon

## Root cause

- New Chat 与 session 原先由两套输入框实现，导致附件、模型、Skills、菜单定位和后续交互持续漂移
- Library 与 Skill Store 操作依赖页面跳转，打断了用户从输入到发起/继续任务的连续路径
- Skill 相关入口存在 Market / Store 混用、emoji / wrench / tool 多套图标以及非 Design System 卡片样式

## Size override rationale

- 本 PR 是统一 composer 迁移的连续分支，现有 `size-override` 标签覆盖 79 个文件、6873 行 diff
- New Chat、session、Library、Skills 与模型菜单共享输入草稿、附件状态、菜单状态和 surface placement；拆分会产生无法独立验收的中间状态
- 大量 diff 来自配套单元测试、设计文档、mock 场景和图标资源

## Test plan

- [x] `bash scripts/verify-changed.sh` — 合并最新 main 后 TypeScript、ESLint 与 governance guards 全部通过
- [x] 组合回归：10 个 New Chat / session composer / Skill Store 测试文件，289 / 289 tests passed
- [x] 标准前端门禁：289 个测试文件，4022 passed、1 todo；TypeScript 与 ESLint 通过
- [x] 本地 `http://localhost:3003/new-chat` 验证统一输入框、Library 弹窗、Use Skills 列表、Skill Store 卡片与响应式布局
- [x] `git diff --cached --check` 与合并冲突检查通过


---

## refactor(chat-ui): extract file attachment renderers into @zooclaw/chat-ui (#2979)

- **SHA**: 0e4310abf38d974262997f3889c722df691dff70
- **作者**: bill-srp
- **日期**: 2026-07-21T07:07:51Z
- **PR**: #2979

### Commit Message

```
refactor(chat-ui): extract file attachment renderers into @zooclaw/chat-ui (#2979)

## Summary

PR **A** of the chat-UI attachment extraction — **package-only**.
Extracts the four Mattermost file-attachment renderers (image / video /
audio / file) plus the gallery/scroll layout into `@zooclaw/chat-ui`,
rendered from a plain, already-resolved `AttachmentView`. `web/app` is
untouched; the app-side resolver rewrites land in PR B.

Follows the merged spec + plan (#2974):
`docs/superpowers/plans/2026-07-21-chat-ui-attachment-extraction.md` (PR
A = Tasks 1–5).

## What's in it (`web/packages/chat-ui/src/attachments/`)

- **`AttachmentView` types** + utils: `formatAttachmentSize` (new — the
app util's exact `.toFixed(1)` logic; **not** the package's existing
`formatFileSize`), `largeImageBoxStyle`, `browserMimeType` (with its
`BROWSER_*_TYPES` sets inlined).
- **View-driven renderers**: `ImageAttachment`, `VideoAttachment` (+
`VideoCard`), `AudioAttachment`, `FileAttachment` — each takes an
`AttachmentView` + optional callbacks.
- **Layout**: `ScrollableImageRow` (generic, package-owned keys) +
`AttachmentGallery` (image/file → scroll row, audio/video stacked).
- Barrel exports from the package root.

## Design notes

- **No new package dependencies** — runtime deps stay `@heroicons/react`
+ `clsx`. No react-query / `@/` / Next.js / `MMFileInfo` in the package.
- **All Tailwind class strings + `data-testid`s copied
byte-identically** from the app renderers; the app render path (which
always wires the callbacks) is unchanged.
- **Affordances gate on their callback** (no dead affordances for a
zero-wiring consumer): image `cursor-pointer`/click on `onPreview`; the
video card renders a non-interactive `<div>` shell (no `<button>`)
without `onPreview`; file download button on `onDownload`.
- **Package owns React keys** (`<Fragment key={item.id}>`), so callers
don't key inside `renderItem`.

## Test plan

- [x] Package gate green: `pnpm test` (21 files, **226 tests**), `pnpm
lint` (0 warnings), `pnpm tsc` — all pass.
- [x] Scope confined to `web/packages/chat-ui/` — `git diff
origin/main...HEAD -- web/app docs` is empty.
- [ ] CI `web-build-check` (`next build`) — runs on this PR.
- PR B rewrites `MMAttachments` + the per-kind resolvers to consume
these; the existing `MMAttachments` specs are the protected regression
harness, plus a `/chat` + `/share` browser check.
```

### PR Body

## Summary

PR **A** of the chat-UI attachment extraction — **package-only**. Extracts the four Mattermost file-attachment renderers (image / video / audio / file) plus the gallery/scroll layout into `@zooclaw/chat-ui`, rendered from a plain, already-resolved `AttachmentView`. `web/app` is untouched; the app-side resolver rewrites land in PR B.

Follows the merged spec + plan (#2974): `docs/superpowers/plans/2026-07-21-chat-ui-attachment-extraction.md` (PR A = Tasks 1–5).

## What's in it (`web/packages/chat-ui/src/attachments/`)

- **`AttachmentView` types** + utils: `formatAttachmentSize` (new — the app util's exact `.toFixed(1)` logic; **not** the package's existing `formatFileSize`), `largeImageBoxStyle`, `browserMimeType` (with its `BROWSER_*_TYPES` sets inlined).
- **View-driven renderers**: `ImageAttachment`, `VideoAttachment` (+ `VideoCard`), `AudioAttachment`, `FileAttachment` — each takes an `AttachmentView` + optional callbacks.
- **Layout**: `ScrollableImageRow` (generic, package-owned keys) + `AttachmentGallery` (image/file → scroll row, audio/video stacked).
- Barrel exports from the package root.

## Design notes

- **No new package dependencies** — runtime deps stay `@heroicons/react` + `clsx`. No react-query / `@/` / Next.js / `MMFileInfo` in the package.
- **All Tailwind class strings + `data-testid`s copied byte-identically** from the app renderers; the app render path (which always wires the callbacks) is unchanged.
- **Affordances gate on their callback** (no dead affordances for a zero-wiring consumer): image `cursor-pointer`/click on `onPreview`; the video card renders a non-interactive `<div>` shell (no `<button>`) without `onPreview`; file download button on `onDownload`.
- **Package owns React keys** (`<Fragment key={item.id}>`), so callers don't key inside `renderItem`.

## Test plan

- [x] Package gate green: `pnpm test` (21 files, **226 tests**), `pnpm lint` (0 warnings), `pnpm tsc` — all pass.
- [x] Scope confined to `web/packages/chat-ui/` — `git diff origin/main...HEAD -- web/app docs` is empty.
- [ ] CI `web-build-check` (`next build`) — runs on this PR.
- PR B rewrites `MMAttachments` + the per-kind resolvers to consume these; the existing `MMAttachments` specs are the protected regression harness, plus a `/chat` + `/share` browser check.


---

## fix: keep desktop web origin stable (#2959)

- **SHA**: 76d239f61a12861425c42ddfe1c5a99103250cf6
- **作者**: zayne-srp
- **日期**: 2026-07-21T07:02:23Z
- **PR**: #2959

### Commit Message

```
fix: keep desktop web origin stable (#2959)

## Summary
- persist the packaged desktop web port so browser auth storage survives
restarts
- prefer canonical port `32180` whenever available
- reuse a persisted fallback while a collision continues, then return to
`32180` when it clears
- keep the development port configurable through `ELECTRON_DEV_PORT`
- fail when the Next server exits or times out instead of assuming
readiness
- add focused regression tests for persistence, collision recovery, and
dev validation

## Validation
- `pnpm exec tsx --test main/next-server-port.test.ts` (6 passed)
- `pnpm typecheck`
- `pnpm build:dir`
- launched the packaged app twice and verified both runs use
`http://localhost:32180/chat`
- verified the login state survives restart
- verified OpenClaw reports `connected` with the same device and gateway
after restart

Closes #2958
```

### PR Body

## Summary
- persist the packaged desktop web port so browser auth storage survives restarts
- prefer canonical port `32180` whenever available
- reuse a persisted fallback while a collision continues, then return to `32180` when it clears
- keep the development port configurable through `ELECTRON_DEV_PORT`
- fail when the Next server exits or times out instead of assuming readiness
- add focused regression tests for persistence, collision recovery, and dev validation

## Validation
- `pnpm exec tsx --test main/next-server-port.test.ts` (6 passed)
- `pnpm typecheck`
- `pnpm build:dir`
- launched the packaged app twice and verified both runs use `http://localhost:32180/chat`
- verified the login state survives restart
- verified OpenClaw reports `connected` with the same device and gateway after restart

Closes #2958

---

