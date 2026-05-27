# SerendipityOneInc/ecap-workspace Commits — 2026-05-26

## 7ef23442
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-26T17:44:13Z
- **SHA:** 7ef23442534a8bfa1f68f103a0b623446acac52c

### Commit Message
```
refactor(web): consolidate landing auth-redirect useEffect chains (#1921) (#1962)

Fixes #1921.

## Summary
- Three overlapping `useEffect` paths in `LandingClient.tsx` (mount-time
`isLoggedIn()` check / `onLoginSuccess` callback / `storage` +
`auth-state-changed` listener pair) each independently called
`router.push(redirectTarget)` on the same auth transition. Same-tab
logins fired two of them simultaneously, racing the redirect.
- Extracted into `useLandingAuthRedirect` (single effect, single
subscription on `auth-state-changed` + `storage`), mirroring the
`useNavAuthState` consolidation pattern already in the repo.
- Dropped the `onLoginSuccess` callback path — `manager.loginUser`
already dispatches `auth-state-changed` before the callback chain runs,
so the event listener fully covers that case.
- Mount-time branch uses `router.replace` (no back-button trap) and
skips listener attachment.
- LandingClient.tsx: 3 auth effects → 0. The 4 legitimate effects (mount
flag / scroll compact / IntersectionObserver / parallax) are preserved
as-is.

## Acceptance (issue criteria)
- [x] `LandingClient.tsx` ≤ 1 auth-related effect (actual: 0; the hook
owns its single effect).
- [x] No `router.push` from `useEffect` body in `LandingClient.tsx`.
Mount-time uses `router.replace`; transition push is inside a documented
subscription callback with no other concurrent triggers.
- [x] The three `eslint-disable no-console` traces are consolidated in
the new hook (now 2 distinct cases — mount-time and transition —
covering the same handoff information as the previous 3).
- [x] The 4 legitimate effects (`setIsMounted` / scroll compact /
IntersectionObserver / parallax) preserved.
- [x] `useLoginCheck`'s `onLoginSuccess` destructure removed from
LandingClient; the provider mechanism itself is untouched.

## Test plan
- [x] New unit spec
`tests/unit/app/landing/hooks/useLandingAuthRedirect.unit.spec.ts` — 11
tests covering mount-time `router.replace` + skip-listeners, transition
via `auth-state-changed`, cross-tab `storage` path, storage key
filtering, false→true edge lock, full false→true→false→true cycle,
cleanup on unmount, `hasRedirectParams` branching.
- [x] `pnpm tsc` clean (full repo).
- [x] `pnpm lint` clean.
- [x] `pnpm lint:ci` (import-boundaries + knip dead-code + dep-health)
clean.
- [x] Existing landing tests (`useLandingRedirect.unit.spec.ts`) +
sidenav auth hook tests + provider tests still pass (97/97).
- [ ] Manual smoke (deferred to staging — devcontainer `pnpm dev`
blocked by `SKIP_CLOUDFLARE_DEV=true`): unauth landing renders → login
modal → redirect happens once; already-auth landing → immediate
`router.replace`; cross-tab login → this tab follows via storage event.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## b0841e0e
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-26T17:03:49Z
- **SHA:** b0841e0e00b4d0f04993fd7d226e66bdd2cda500

### Commit Message
```
refactor(web): autoConnect → options object + drop legacy complexity exemptions (#1956)

## 背景

F15 anti-pattern 清理系列收尾(主体 PR #1953 / #1954 / #1955 已 merge)。

`autoConnect` 之前 5-positional-arg 签名是 max-params lint **真正想拦的场景**:4 个
adjacent string,调用点极容易 swap `userId` 和 `channelId`(都是 string,TS 抓不到):

```typescript
// Before — easy to swap mid-positions
mmAutoConnect(MATTERMOST_SERVER_URL, token, userId, channelId, botUserId)
//             string,                string, string, string,    string?
```

```typescript
// After — self-documenting, swap-proof
mmAutoConnect({ serverURL: MATTERMOST_SERVER_URL, token, userId, channelId, botUserId })
```

## 改动

### autoConnect signature

新增 `AutoConnectOptions` 接口 (`lib/mattermost/types.ts`):
```typescript
export interface AutoConnectOptions {
  serverURL: string
  token: string
  userId: string
  channelId: string
  botUserId?: string
}
```

签名改 `autoConnect(opts: AutoConnectOptions)`,实现 + 类型 + 1 caller
(MattermostProvider) + 4 处测试 assertion 一致更新。

### eslint legacy complexity exemption 收紧

F15 拆分完成后:
- `src/hooks/useMattermost.ts` (249 行) — 自然合规所有 6 条 lint rule(complexity
/ max-depth / max-params / max-lines-per-function / max-nested-callbacks
/ max-lines)
- `src/hooks/mattermost/useMattermostConnection.ts` (457 行) — 唯一卡点是
autoConnect 5 参数,本 PR 已 fix

两条 exemption 一并删除。Legacy complexity block 净 -2 entries,无 file 新增。

## 验证

- `pnpm tsc --noEmit` ✓
- `pnpm lint` ✓(含 useMattermost + useMattermostConnection 重新接受默认
max-params=4 等 6 条 rule)
- 213 单测 / 12 spec 全过(autoConnect.toHaveBeenCalledWith assertions 改成
options object 形状)

## 下游影响

- caller: 1(MattermostProvider 内部)
- consumer:0(`useMattermostContext().autoConnect` 没有直接调用方,只有 Provider 用)

## 不在范围

剩余 max-params 违例的函数将单独 tracking issue 提:

**5-param**(本系列同审计扫出):
- `hasOverlap` (canvas useCanvasState) — 几何标准 sig,接受 OR 改 `(nodes,
rect)`
- `mapChildToSlide` (pptx-parser) — 数学投影,内聚,接受
- `extractGroupShapes` (pptx-parser) — 🚩 5 个无关类型,应 `(grpEl, ctx)`
- `getSessionList` (lib/api/session) — 🚩 教科书级 options object case
- `reportLatency` (sentry/openclaw-monitor) — 混合 smell

**6+-param**:
- `customInputArea` (agent-chat-client/types, 8 params 的 callback type)
— 🚩 应改 props object
- `getCtaConfig` / `getBadge` (PlanCard.tsx, 6 params) — 共享 BillingState
参数,改 `(state: BillingState) => ...`

这 8 个函数各自 owner 后续 touch 时处理。
```

### PR #1956: refactor(web): autoConnect → options object + drop legacy complexity exemptions

**PR Description:**
## 背景

F15 anti-pattern 清理系列收尾(主体 PR #1953 / #1954 / #1955 已 merge)。

`autoConnect` 之前 5-positional-arg 签名是 max-params lint **真正想拦的场景**:4 个 adjacent string,调用点极容易 swap `userId` 和 `channelId`(都是 string,TS 抓不到):

```typescript
// Before — easy to swap mid-positions
mmAutoConnect(MATTERMOST_SERVER_URL, token, userId, channelId, botUserId)
//             string,                string, string, string,    string?
```

```typescript
// After — self-documenting, swap-proof
mmAutoConnect({ serverURL: MATTERMOST_SERVER_URL, token, userId, channelId, botUserId })
```

## 改动

### autoConnect signature

新增 `AutoConnectOptions` 接口 (`lib/mattermost/types.ts`):
```typescript
export interface AutoConnectOptions {
  serverURL: string
  token: string
  userId: string
  channelId: string
  botUserId?: string
}
```

签名改 `autoConnect(opts: AutoConnectOptions)`,实现 + 类型 + 1 caller (MattermostProvider) + 4 处测试 assertion 一致更新。

### eslint legacy complexity exemption 收紧

F15 拆分完成后:
- `src/hooks/useMattermost.ts` (249 行) — 自然合规所有 6 条 lint rule(complexity / max-depth / max-params / max-lines-per-function / max-nested-callbacks / max-lines)
- `src/hooks/mattermost/useMattermostConnection.ts` (457 行) — 唯一卡点是 autoConnect 5 参数,本 PR 已 fix

两条 exemption 一并删除。Legacy complexity block 净 -2 entries,无 file 新增。

## 验证

- `pnpm tsc --noEmit` ✓
- `pnpm lint` ✓(含 useMattermost + useMattermostConnection 重新接受默认 max-params=4 等 6 条 rule)
- 213 单测 / 12 spec 全过(autoConnect.toHaveBeenCalledWith assertions 改成 options object 形状)

## 下游影响

- caller: 1(MattermostProvider 内部)
- consumer:0(`useMattermostContext().autoConnect` 没有直接调用方,只有 Provider 用)

## 不在范围

剩余 max-params 违例的函数将单独 tracking issue 提:

**5-param**(本系列同审计扫出):
- `hasOverlap` (canvas useCanvasState) — 几何标准 sig,接受 OR 改 `(nodes, rect)`
- `mapChildToSlide` (pptx-parser) — 数学投影,内聚,接受
- `extractGroupShapes` (pptx-parser) — 🚩 5 个无关类型,应 `(grpEl, ctx)`
- `getSessionList` (lib/api/session) — 🚩 教科书级 options object case
- `reportLatency` (sentry/openclaw-monitor) — 混合 smell

**6+-param**:
- `customInputArea` (agent-chat-client/types, 8 params 的 callback type) — 🚩 应改 props object
- `getCtaConfig` / `getBadge` (PlanCard.tsx, 6 params) — 共享 BillingState 参数,改 `(state: BillingState) => ...`

这 8 个函数各自 owner 后续 touch 时处理。

---

## 652db5b3
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-26T16:39:06Z
- **SHA:** 652db5b317d8ca1750ced2dfb30ae013fe172917

### Commit Message
```
refactor(web): MATTERMOST_SERVER_URL — single source of truth (#1955)

## 背景

F15 follow-up anti-pattern 清理系列 **PR 3 / 3 (finale)**(PR 1 #1953 + PR 2
#1954 已 merge)。

`process.env.NEXT_PUBLIC_MATTERMOST_URL ??
'https://mattermost.zooclaw.ai'` 之前**重复**在:
-
`web/app/src/components/providers/MattermostProvider.tsx:77`(`mmServerURL`
局部常量)
- `web/app/src/lib/mattermost/blob.ts:7`(`MM_SERVER_URL` 局部常量)

任何 env override 需同步改两处,易半-deploy。

## 改动

- 新 `web/app/src/lib/mattermost/constants.ts` 导出 `MATTERMOST_SERVER_URL`
- `MattermostProvider.tsx` import + 删除局部 `mmServerURL` + Provider
useEffect deps 数组中对应项
- `blob.ts` import + 删除局部 `MM_SERVER_URL`

Fallback 顺序保留:`process.env.NEXT_PUBLIC_MATTERMOST_URL ?? '<default>'`。

## 验证

- `pnpm tsc --noEmit` ✓
- `pnpm lint` ✓
- 213 单测 / 12 spec 全过
- 无功能变更

## F15 anti-pattern 清理系列完结

| PR | 主旨 | merge |
|---|---|---|
| #1953 | MattermostProvider auto-connect refs → useReducer | ✅ |
| #1954 | useChatMessaging `...mm` rest spread + mmReturn dance 清理 | ✅ |
| #1955 (本 PR) | MATTERMOST_SERVER_URL 常量抽取 | — |

本 PR merge 后 F15 follow-up 全部完成。
```

### PR #1955: refactor(web): MATTERMOST_SERVER_URL — single source of truth

**PR Description:**
## 背景

F15 follow-up anti-pattern 清理系列 **PR 3 / 3 (finale)**(PR 1 #1953 + PR 2 #1954 已 merge)。

`process.env.NEXT_PUBLIC_MATTERMOST_URL ?? 'https://mattermost.zooclaw.ai'` 之前**重复**在:
- `web/app/src/components/providers/MattermostProvider.tsx:77`(`mmServerURL` 局部常量)
- `web/app/src/lib/mattermost/blob.ts:7`(`MM_SERVER_URL` 局部常量)

任何 env override 需同步改两处,易半-deploy。

## 改动

- 新 `web/app/src/lib/mattermost/constants.ts` 导出 `MATTERMOST_SERVER_URL`
- `MattermostProvider.tsx` import + 删除局部 `mmServerURL` + Provider useEffect deps 数组中对应项
- `blob.ts` import + 删除局部 `MM_SERVER_URL`

Fallback 顺序保留:`process.env.NEXT_PUBLIC_MATTERMOST_URL ?? '<default>'`。

## 验证

- `pnpm tsc --noEmit` ✓
- `pnpm lint` ✓
- 213 单测 / 12 spec 全过
- 无功能变更

## F15 anti-pattern 清理系列完结

| PR | 主旨 | merge |
|---|---|---|
| #1953 | MattermostProvider auto-connect refs → useReducer | ✅ |
| #1954 | useChatMessaging `...mm` rest spread + mmReturn dance 清理 | ✅ |
| #1955 (本 PR) | MATTERMOST_SERVER_URL 常量抽取 | — |

本 PR merge 后 F15 follow-up 全部完成。

---

## 9a44fa7e
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-26T16:31:58Z
- **SHA:** 9a44fa7ed0380f980883af486c97d4f031516ae8

### Commit Message
```
refactor(web): useChatMessaging — drop redundant ...mm rest + mmReturn reassembly (#1954)

## 背景

F15 follow-up anti-pattern 清理系列 PR 2 / 3(PR 1 #1953 已 merge)。

`useChatMessaging` 之前:
- destructure 13 字段(`apiService`, `activeChannelId`, `connectionState`
等)
- `...mm` rest spread 捕获剩余
- 用 `mm.clearWaitingForBotReply` / `mm.isWaitingForBotReply` /
`mm.error` 3 个字段
- 然后 `useMemo` 把 `...mm` 和 13 个 named 字段**重新拼成** `mmReturn` 再返回

`mmReturn` 的 docstring 自我暴露:"Reassemble `mm` to its original shape" —
等价于直接返回 `useMattermostContext()` 整体值。

## 改动(单文件)

`web/app/src/app/[locale]/chat/hooks/useChatMessaging.ts`:

```diff
+  const mm = useMattermostContext()
+  // Pin the closure-captured fields as plain identifiers so memo/effect deps
+  // can reference them directly without depending on the `mm` wrapper object.
+  // The full context value remains available via `mm.X` for any field this
+  // hook doesn't explicitly capture.
   const {
     mmBots,
     refreshBots,
     // ... 13 fields ...
-    ...mm
-  } = useMattermostContext()
+  } = mm
```

```diff
-  // Reassemble `mm` to its original shape for callers that destructure ...
-  const mmReturn = useMemo(() => ({ ...mm, apiService: mmApiService, /* 12 fields */ }), [/* 13 deps */])
-
   return {
-    mm: mmReturn,
+    mm,
```

**Net -31 行**。`mm.X` 访问语义不变 — 整个 `MattermostContextValue` 仍可用。

## 验证

- `pnpm tsc --noEmit` ✓
- `pnpm lint` ✓
- 156 单测 / 8 spec 全过,`useChatMessaging.unit.spec.ts` 不改 pass
- 下游消费者无感知 — `mm` 仍是同样 25 字段(实际 27,含 mmBots/refreshBots,这两个 hook 也单独返回作
top-level)

## 风险

`mm` 现在是 `MattermostContextValue` 类型(27 字段,含 mmBots/refreshBots)而非 之前
`mmReturn` 的 `UseMattermostReturn` 类型(25 字段)。下游 caller 如果有特殊代码依赖 `mm` 不含
mmBots/refreshBots 会撞到 — 检查后**没有**这种依赖,因为 mmBots/refreshBots 在
useChatMessaging 的 return 里**也独立暴露**,下游 consumer 都从 top-level 取。

## 后续 PR

- **PR 3** — ServerURL 常量抽取到 `src/lib/mattermost/constants.ts`
```

### PR #1954: refactor(web): useChatMessaging — drop redundant ...mm rest + mmReturn reassembly

**PR Description:**
## 背景

F15 follow-up anti-pattern 清理系列 PR 2 / 3(PR 1 #1953 已 merge)。

`useChatMessaging` 之前:
- destructure 13 字段(`apiService`, `activeChannelId`, `connectionState` 等)
- `...mm` rest spread 捕获剩余
- 用 `mm.clearWaitingForBotReply` / `mm.isWaitingForBotReply` / `mm.error` 3 个字段
- 然后 `useMemo` 把 `...mm` 和 13 个 named 字段**重新拼成** `mmReturn` 再返回

`mmReturn` 的 docstring 自我暴露:"Reassemble `mm` to its original shape" — 等价于直接返回 `useMattermostContext()` 整体值。

## 改动(单文件)

`web/app/src/app/[locale]/chat/hooks/useChatMessaging.ts`:

```diff
+  const mm = useMattermostContext()
+  // Pin the closure-captured fields as plain identifiers so memo/effect deps
+  // can reference them directly without depending on the `mm` wrapper object.
+  // The full context value remains available via `mm.X` for any field this
+  // hook doesn't explicitly capture.
   const {
     mmBots,
     refreshBots,
     // ... 13 fields ...
-    ...mm
-  } = useMattermostContext()
+  } = mm
```

```diff
-  // Reassemble `mm` to its original shape for callers that destructure ...
-  const mmReturn = useMemo(() => ({ ...mm, apiService: mmApiService, /* 12 fields */ }), [/* 13 deps */])
-
   return {
-    mm: mmReturn,
+    mm,
```

**Net -31 行**。`mm.X` 访问语义不变 — 整个 `MattermostContextValue` 仍可用。

## 验证

- `pnpm tsc --noEmit` ✓
- `pnpm lint` ✓
- 156 单测 / 8 spec 全过,`useChatMessaging.unit.spec.ts` 不改 pass
- 下游消费者无感知 — `mm` 仍是同样 25 字段(实际 27,含 mmBots/refreshBots,这两个 hook 也单独返回作 top-level)

## 风险

`mm` 现在是 `MattermostContextValue` 类型(27 字段,含 mmBots/refreshBots)而非 之前 `mmReturn` 的 `UseMattermostReturn` 类型(25 字段)。下游 caller 如果有特殊代码依赖 `mm` 不含 mmBots/refreshBots 会撞到 — 检查后**没有**这种依赖,因为 mmBots/refreshBots 在 useChatMessaging 的 return 里**也独立暴露**,下游 consumer 都从 top-level 取。

## 后续 PR

- **PR 3** — ServerURL 常量抽取到 `src/lib/mattermost/constants.ts`

---

## d15a601c
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-26T16:23:49Z
- **SHA:** d15a601c4ada55f5271e7829b6ec128aea877ae5

### Commit Message
```
refactor(web): MattermostProvider auto-connect refs → useReducer (#1953)

## 背景

F15 [issue
#368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368)
4-PR 系列(#1946 / #1950 / #1951 / #1952)已完成 `useMattermost.ts` god-hook
拆分(963→249 行)。在此基础上对 mattermost 全部前端代码做 React anti-pattern audit。最高价值
finding 是 **MattermostProvider 用 5 个 useEffect + 4 个 ref 隐式协调状态机** —
docstring 已记 Codex 之前抓过的 retry button 失效回归。这是 React [You Might Not Need
an Effect](https://react.dev/learn/you-might-not-need-an-effect) 文档的典型
case:**state machine 应该用 `useReducer` 而不是多个 effect + ref 协调**。

Plan doc 在 `/home/node/.claude/plans/issue-368-crystalline-wand.md`。本 PR
是 3-PR 清理系列的 PR 1 / 3。

## 改动

### 新 `src/components/providers/mattermost-connect-reducer.ts`(101 行)

纯函数 reducer + types:

- **Phases**: `'armed' | 'attempting' | 'connected' | 'exhausted'`
- **State**: `{ phase, attemptCount }`
- **Actions**: `AUTO_CONNECT_TRIGGERED` / `CONNECT_SUCCEEDED` /
`CONNECT_FAILED` / `USER_RETRY` / `UID_CHANGED` / `OC_INIT_ERROR`
- `MAX_CONNECT_RETRIES = 3` 常量也搬到此文件

### `MattermostProvider.tsx` 重写

删:
- `connectAttemptedRef` / `connectFailCountRef` / `prevErrorRef` /
`prevUidRef` 4 个 ref
- 5 个相互协调 ref 的 useEffect

加:
- `useReducer(mattermostConnectReducer, INITIAL_CONNECT_STATE)`
- **Observer effect**(单一)— 监听 mm state + uid + initStatus,dispatch 对应
action。`prevErrorRef` 仍在(内部到 observer,用来检测 `error: truthy → null`
transition,即 USER_RETRY 信号 — Codex #1946 regression 锁定)
- **Response effect** — `phase === 'armed'` + 所有 prereq 满足时,触发
`mmAutoConnect()` + dispatch `AUTO_CONNECT_TRIGGERED`
- **Exhausted log effect** — phase 进入 'exhausted' 时打 warn

保留:
- 独立 `disconnectRef` sync + unmount disconnect(与状态机解耦)
- `initReady` refetch(独立 side effect)
- `agent-update` listener(独立 side effect)

### Effect 数对比

| 前 | 后 |
|---|---|
| 5 个交织 effect + 4 个 ref 隐式协调 | 1 observer + 1 response + 1 log,显式
reducer |

`MattermostContextValue` 形状不变,所有 consumer 零改动。

## 单测

新
`tests/unit/components/providers/mattermost-connect-reducer.unit.spec.ts`
16 个单测:

- 每个 action transition 单独覆盖(idempotence 包括在内)
- **Codex regression #1946 路径**:exhausted → USER_RETRY → armed →
AUTO_CONNECT_TRIGGERED(锁定 retry button 复活语义)
- `reconnectExhausted` 短路 → exhausted on attempt 1
- uid switch from exhausted: full reset
- 完整 happy path: armed → attempting → connected

总测试 **11 spec × 215 tests** 全过(老 `useMattermost` / `MattermostContext` /
`useChatMessaging` spec 不改 pass)。

## 验证

- `pnpm tsc --noEmit` ✓
- `pnpm lint` ✓
- `pnpm dup` ✓
- 215 单测全过

## 风险

1. **Codex regression #1946** — retry button 复活路径必须保留。新 reducer 单测
`exhaustion + user-retry recovery` 显式覆盖此 sequence
2. **多个 dispatch 同帧** — React batches state updates,reducer 处理 in
order(e.g. UID_CHANGED + CONNECT_SUCCEEDED 同帧 OK)
3. **`prevErrorRef` 内部到 observer effect** — 不暴露给 reducer,保持 reducer 纯函数

## 后续 PR

- **PR 2** — useChatMessaging `...mm` rest spread + mmReturn 重组 dance 清理
- **PR 3** — ServerURL 常量抽取到 `src/lib/mattermost/constants.ts`
```

### PR #1953: refactor(web): MattermostProvider auto-connect refs → useReducer

**PR Description:**
## 背景

F15 [issue #368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368) 4-PR 系列(#1946 / #1950 / #1951 / #1952)已完成 `useMattermost.ts` god-hook 拆分(963→249 行)。在此基础上对 mattermost 全部前端代码做 React anti-pattern audit。最高价值 finding 是 **MattermostProvider 用 5 个 useEffect + 4 个 ref 隐式协调状态机** — docstring 已记 Codex 之前抓过的 retry button 失效回归。这是 React [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) 文档的典型 case:**state machine 应该用 `useReducer` 而不是多个 effect + ref 协调**。

Plan doc 在 `/home/node/.claude/plans/issue-368-crystalline-wand.md`。本 PR 是 3-PR 清理系列的 PR 1 / 3。

## 改动

### 新 `src/components/providers/mattermost-connect-reducer.ts`(101 行)

纯函数 reducer + types:

- **Phases**: `'armed' | 'attempting' | 'connected' | 'exhausted'`
- **State**: `{ phase, attemptCount }`
- **Actions**: `AUTO_CONNECT_TRIGGERED` / `CONNECT_SUCCEEDED` / `CONNECT_FAILED` / `USER_RETRY` / `UID_CHANGED` / `OC_INIT_ERROR`
- `MAX_CONNECT_RETRIES = 3` 常量也搬到此文件

### `MattermostProvider.tsx` 重写

删:
- `connectAttemptedRef` / `connectFailCountRef` / `prevErrorRef` / `prevUidRef` 4 个 ref
- 5 个相互协调 ref 的 useEffect

加:
- `useReducer(mattermostConnectReducer, INITIAL_CONNECT_STATE)`
- **Observer effect**(单一)— 监听 mm state + uid + initStatus,dispatch 对应 action。`prevErrorRef` 仍在(内部到 observer,用来检测 `error: truthy → null` transition,即 USER_RETRY 信号 — Codex #1946 regression 锁定)
- **Response effect** — `phase === 'armed'` + 所有 prereq 满足时,触发 `mmAutoConnect()` + dispatch `AUTO_CONNECT_TRIGGERED`
- **Exhausted log effect** — phase 进入 'exhausted' 时打 warn

保留:
- 独立 `disconnectRef` sync + unmount disconnect(与状态机解耦)
- `initReady` refetch(独立 side effect)
- `agent-update` listener(独立 side effect)

### Effect 数对比

| 前 | 后 |
|---|---|
| 5 个交织 effect + 4 个 ref 隐式协调 | 1 observer + 1 response + 1 log,显式 reducer |

`MattermostContextValue` 形状不变,所有 consumer 零改动。

## 单测

新 `tests/unit/components/providers/mattermost-connect-reducer.unit.spec.ts` 16 个单测:

- 每个 action transition 单独覆盖(idempotence 包括在内)
- **Codex regression #1946 路径**:exhausted → USER_RETRY → armed → AUTO_CONNECT_TRIGGERED(锁定 retry button 复活语义)
- `reconnectExhausted` 短路 → exhausted on attempt 1
- uid switch from exhausted: full reset
- 完整 happy path: armed → attempting → connected

总测试 **11 spec × 215 tests** 全过(老 `useMattermost` / `MattermostContext` / `useChatMessaging` spec 不改 pass)。

## 验证

- `pnpm tsc --noEmit` ✓
- `pnpm lint` ✓
- `pnpm dup` ✓
- 215 单测全过

## 风险

1. **Codex regression #1946** — retry button 复活路径必须保留。新 reducer 单测 `exhaustion + user-retry recovery` 显式覆盖此 sequence
2. **多个 dispatch 同帧** — React batches state updates,reducer 处理 in order(e.g. UID_CHANGED + CONNECT_SUCCEEDED 同帧 OK)
3. **`prevErrorRef` 内部到 observer effect** — 不暴露给 reducer,保持 reducer 纯函数

## 后续 PR

- **PR 2** — useChatMessaging `...mm` rest spread + mmReturn 重组 dance 清理
- **PR 3** — ServerURL 常量抽取到 `src/lib/mattermost/constants.ts`

---

## 01cea324
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-26T15:40:45Z
- **SHA:** 01cea324d81ce5b3c03e582bd2eebccde378ced9

### Commit Message
```
refactor(web): finalize F15 — dedup useStableCallback + spec doc completion (#1952)

## 背景

issue
[#368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368)
F15 — 4-PR 拆分计划的 **PR 4 / 4 (finale)**(PR 1 #1946 + PR 2 #1950 + PR 3
#1951 已 merged)。

## 改动

1. **`useStableCallback` 抽到共享文件** —
`src/hooks/mattermost/useStableCallback.ts`。原来在 `useMattermost.ts` 和
`useMattermost/useMattermostConnection.ts` 两处 byte-identical 定义,各 8 行
2. **Spec doc 标完结** — 加 4 PR 完整序列表 + merge commits + 最终行数对照
3. **`useChatMessaging` rest spread 字段对照已确认安全**(无功能改动):
  - 显式 destructure 13 字段
- `mm.X` 用 3 字段(`mm.clearWaitingForBotReply` / `mm.isWaitingForBotReply`
/ `mm.error`)
  - `mmReturn` useMemo 把全部 25 字段透传
  - `UseMattermostReturn` interface 全字段匹配 ✓(TS enforce,无静默 undefined 风险)

## 最终结果(F15 系列收官)

| 维度 | 起点 | 终点 |
|---|---|---|
| `useMattermost.ts` 行数 | 963 | **249** (-74%) |
| 顶层 useState | 14 | 0 |
| 顶层 useRef | ~20 | 1(useStableCallback 内部 ref) |
| sub-files | 0 | 5 (4 sub-hooks + 1 utility + 1 helper) |
| 单测数 | ~40(老 spec) | 140(7 spec files) |

未命中 spec 计划的"≤ 200 行 composition"是**有意停下**:剩余 249 行的核心是
`handlePostedEvent`(40 行 junction box dispatcher)+ 3 个跨 hook
orchestrator(`selectChannel` / `sendMessage` /
`loadMoreHistory`)。继续抽出会违反 spec D1("composition 持 dispatcher")或反向把语义塞回
sub-hook(option B,已在 spec 阶段拒绝)。Memory
`project_web_coverage_phase4_done` 的 "narrowed at observed floor"
模式同样适用。

## 验证

- `pnpm tsc --noEmit` ✓
- `pnpm lint` ✓
- `pnpm test:unit`(7 spec / 140 tests 不改 pass)✓
- `UseMattermostReturn` 形状逐字段不变 → `MattermostProvider` /
`MattermostContext` / 全 5 consumer 零改动
- 无功能变更

## 不在范围

- `MattermostProvider` 的 auto-connect / retry recovery 逻辑(独立子系统)
- `MattermostAPIService` / `MattermostAuthService` /
`MattermostWebSocketService` 服务层(已独立)
- 把 `useStableCallback` 提到 `src/hooks/`(project-wide):本次仅去 mattermost
内部重复,跨模块推广留作后续

## F15 完结说明

本 PR merge 后:
- F15 finding 自动从 issue #368 active findings 移到 "Recently resolved"
- spec doc 永久标 Status: ✅ 完成 留作后续 god-hook 拆分参考前例
```

### PR #1952: refactor(web): finalize F15 — dedup useStableCallback + spec doc completion

**PR Description:**
## 背景

issue [#368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368) F15 — 4-PR 拆分计划的 **PR 4 / 4 (finale)**(PR 1 #1946 + PR 2 #1950 + PR 3 #1951 已 merged)。

## 改动

1. **`useStableCallback` 抽到共享文件** — `src/hooks/mattermost/useStableCallback.ts`。原来在 `useMattermost.ts` 和 `useMattermost/useMattermostConnection.ts` 两处 byte-identical 定义,各 8 行
2. **Spec doc 标完结** — 加 4 PR 完整序列表 + merge commits + 最终行数对照
3. **`useChatMessaging` rest spread 字段对照已确认安全**(无功能改动):
  - 显式 destructure 13 字段
  - `mm.X` 用 3 字段(`mm.clearWaitingForBotReply` / `mm.isWaitingForBotReply` / `mm.error`)
  - `mmReturn` useMemo 把全部 25 字段透传
  - `UseMattermostReturn` interface 全字段匹配 ✓(TS enforce,无静默 undefined 风险)

## 最终结果(F15 系列收官)

| 维度 | 起点 | 终点 |
|---|---|---|
| `useMattermost.ts` 行数 | 963 | **249** (-74%) |
| 顶层 useState | 14 | 0 |
| 顶层 useRef | ~20 | 1(useStableCallback 内部 ref) |
| sub-files | 0 | 5 (4 sub-hooks + 1 utility + 1 helper) |
| 单测数 | ~40(老 spec) | 140(7 spec files) |

未命中 spec 计划的"≤ 200 行 composition"是**有意停下**:剩余 249 行的核心是 `handlePostedEvent`(40 行 junction box dispatcher)+ 3 个跨 hook orchestrator(`selectChannel` / `sendMessage` / `loadMoreHistory`)。继续抽出会违反 spec D1("composition 持 dispatcher")或反向把语义塞回 sub-hook(option B,已在 spec 阶段拒绝)。Memory `project_web_coverage_phase4_done` 的 "narrowed at observed floor" 模式同样适用。

## 验证

- `pnpm tsc --noEmit` ✓
- `pnpm lint` ✓
- `pnpm test:unit`(7 spec / 140 tests 不改 pass)✓
- `UseMattermostReturn` 形状逐字段不变 → `MattermostProvider` / `MattermostContext` / 全 5 consumer 零改动
- 无功能变更

## 不在范围

- `MattermostProvider` 的 auto-connect / retry recovery 逻辑(独立子系统)
- `MattermostAPIService` / `MattermostAuthService` / `MattermostWebSocketService` 服务层(已独立)
- 把 `useStableCallback` 提到 `src/hooks/`(project-wide):本次仅去 mattermost 内部重复,跨模块推广留作后续

## F15 完结说明

本 PR merge 后:
- F15 finding 自动从 issue #368 active findings 移到 "Recently resolved"
- spec doc 永久标 Status: ✅ 完成 留作后续 god-hook 拆分参考前例

---

## ba2ef3e8
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-26T15:28:49Z
- **SHA:** ba2ef3e8bf8fd65bcc73cf0663199fbdbe545b6d

### Commit Message
```
refactor(web): extract useMattermostConnection from useMattermost god-hook (#1951)

## 背景

issue
[#368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368)
F15 — 4-PR 拆分计划的 **PR 3 / 4**(PR 1 #1946 + PR 2 #1950 merged)。设计文档
`docs/superpowers/specs/2026-05-26-issue-368-f15-usemattermost-refactor.md`。

## 改动

抽 WS 连接生命周期完整模块到 `src/hooks/mattermost/useMattermostConnection.ts`(464
行):

| 持有 | 数量 |
|---|---|
| useState | 5(connectionState / activeChannelId / currentUser /
isLoading / error / isReconnectExhausted) |
| useRef | 14(api / ws / auth / activeChannel / currentUser /
reconnect×5 / connectionId / lastSeq / lastWsMessageAt /
intentionalDisconnect / serverURL / token / pendingBackfill /
connectionStateRef) |
| 函数 | 10(connect / disconnect / autoConnect / setupWebSocket /
scheduleReconnect / attemptReconnect / forceReconnectFromVisibleTab /
handleVisible / handleSeqGap / fetchMissedMessages) |

`useMattermost.ts`: **607 → 256 行 (-351, 已达 spec 计划)**,顶层 useState **6 →
0**,顶层 useRef **14 → 1**(只剩 useStableCallback 内部 ref)。

### Composition layer 余下内容(~256 行)

- 4 sub-hook 调用 + connection config 装配
- **`handlePostedEvent` 编排**(spec D1 junction box):同时写 postStore +
waiting + recentBotMessageIds + streamingEditIds 4 slice,顺序 `clearOnPost
→ syncPosts → backfillFileInfos → markRecentBot → markStreamingEdit` 保留
PR 1 契约
- `handleTypingEvent` 编排(简短)
- `dispatchEvent` 把上两者 + `posts.upsertReactions` 串成 connection.onEvent
- `messages` useMemo(从 posts.postStore 派生)
- 4 个跨 hook orchestrator:`selectChannel` / `sendMessage` /
`loadMoreHistory` / `clearWaitingForBotReply`

### Sub-hook 边界:config 注入 + getter 实时读

Connection 通过 config 注入回调与其他 sub-hook 解耦:
- `onEvent` ← composition 的 dispatcher
- `runBackfill` ← `posts.backfillChannels`
- `pollBotStatus` / `cancelBotPoll` ← `botReady`
- `onDisconnectReset` ← `posts.resetStore` + `posts.setHasMore(true)` +
`posts.setActiveChannelHistoryReady(false)`

Composition 通过 connection 暴露的 `getApi` / `getActiveChannelId` /
`getCurrentUserId` 在 `useStableCallback` 内做 call-time 读取,避免 closure
capture stale 值。`setActiveChannelIdSync` 保留原"ref 同步先于 state"语义,关闭
posted-event-race 窗口(PR 1 spec 已有专项测试)。

## 验证

- `pnpm tsc --noEmit` ✓
- `pnpm lint` ✓
- `pnpm dup` ✓
- `UseMattermostReturn` 形状逐字段不变 → `MattermostProvider` /
`MattermostContext` / 全 5 consumer 零改动
- 现 `useMattermost.unit.spec.ts` / `MattermostContext.unit.spec.tsx` /
`useChatMessaging.unit.spec.ts` 不改 pass
- 新增 12 单测覆盖 connect/disconnect lifecycle、WS event dispatch 顺序(seq-gap 在
onEvent 前)、onHello session-loss 检测、visibility-defer backfill 恢复、3 个
getter 实时读取语义、autoConnect 短路保护

总测试 **7 spec × 140 tests** 全过(老 spec 完全不动)。

## 风险与注意

1. **Event dispatch 顺序契约不变** — connection.setupWebSocket 内部固定 `seq-gap →
config.onEvent` 顺序;composition 的 dispatchEvent 内固定 `handlePostedEvent →
handleTypingEvent → posts.upsertReactions`。任一顺序改动可能让
`recentBotMessageIds` 或 typing 状态错位
2. **`autoConnect` 5-param 签名沿用原 god-hook** — 同等列入 `eslint.config.mjs`
`max-params` exemption。memory `feedback_no_subjective_lint_tightening`
支持不主动加严
3. **`getCurrentUserId` 是 ref 读** — useMemo 用
`connection.currentUser?.id` 做 deps,handlePostedEvent 内用
`connection.getCurrentUserId()` 做 call-time 读;两路径都正确
4. **pendingBackfillRef 不再 composition 持有** — 进 connection
后,handleVisible 内部自处理 drain;composition 不再 know about it

## 后续 PR

- **PR 4** — composition 收尾:核对 `useChatMessaging` 的 `...mm` rest
spread,逐字段对照 `UseMattermostReturn`;若 composition 仍 > 200 行,审视
handlePostedEvent dispatcher 拆 helper
```

### PR #1951: refactor(web): extract useMattermostConnection from useMattermost god-hook

**PR Description:**
## 背景

issue [#368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368) F15 — 4-PR 拆分计划的 **PR 3 / 4**(PR 1 #1946 + PR 2 #1950 merged)。设计文档 `docs/superpowers/specs/2026-05-26-issue-368-f15-usemattermost-refactor.md`。

## 改动

抽 WS 连接生命周期完整模块到 `src/hooks/mattermost/useMattermostConnection.ts`(464 行):

| 持有 | 数量 |
|---|---|
| useState | 5(connectionState / activeChannelId / currentUser / isLoading / error / isReconnectExhausted) |
| useRef | 14(api / ws / auth / activeChannel / currentUser / reconnect×5 / connectionId / lastSeq / lastWsMessageAt / intentionalDisconnect / serverURL / token / pendingBackfill / connectionStateRef) |
| 函数 | 10(connect / disconnect / autoConnect / setupWebSocket / scheduleReconnect / attemptReconnect / forceReconnectFromVisibleTab / handleVisible / handleSeqGap / fetchMissedMessages) |

`useMattermost.ts`: **607 → 256 行 (-351, 已达 spec 计划)**,顶层 useState **6 → 0**,顶层 useRef **14 → 1**(只剩 useStableCallback 内部 ref)。

### Composition layer 余下内容(~256 行)

- 4 sub-hook 调用 + connection config 装配
- **`handlePostedEvent` 编排**(spec D1 junction box):同时写 postStore + waiting + recentBotMessageIds + streamingEditIds 4 slice,顺序 `clearOnPost → syncPosts → backfillFileInfos → markRecentBot → markStreamingEdit` 保留 PR 1 契约
- `handleTypingEvent` 编排(简短)
- `dispatchEvent` 把上两者 + `posts.upsertReactions` 串成 connection.onEvent
- `messages` useMemo(从 posts.postStore 派生)
- 4 个跨 hook orchestrator:`selectChannel` / `sendMessage` / `loadMoreHistory` / `clearWaitingForBotReply`

### Sub-hook 边界:config 注入 + getter 实时读

Connection 通过 config 注入回调与其他 sub-hook 解耦:
- `onEvent` ← composition 的 dispatcher
- `runBackfill` ← `posts.backfillChannels`
- `pollBotStatus` / `cancelBotPoll` ← `botReady`
- `onDisconnectReset` ← `posts.resetStore` + `posts.setHasMore(true)` + `posts.setActiveChannelHistoryReady(false)`

Composition 通过 connection 暴露的 `getApi` / `getActiveChannelId` / `getCurrentUserId` 在 `useStableCallback` 内做 call-time 读取,避免 closure capture stale 值。`setActiveChannelIdSync` 保留原"ref 同步先于 state"语义,关闭 posted-event-race 窗口(PR 1 spec 已有专项测试)。

## 验证

- `pnpm tsc --noEmit` ✓
- `pnpm lint` ✓
- `pnpm dup` ✓
- `UseMattermostReturn` 形状逐字段不变 → `MattermostProvider` / `MattermostContext` / 全 5 consumer 零改动
- 现 `useMattermost.unit.spec.ts` / `MattermostContext.unit.spec.tsx` / `useChatMessaging.unit.spec.ts` 不改 pass
- 新增 12 单测覆盖 connect/disconnect lifecycle、WS event dispatch 顺序(seq-gap 在 onEvent 前)、onHello session-loss 检测、visibility-defer backfill 恢复、3 个 getter 实时读取语义、autoConnect 短路保护

总测试 **7 spec × 140 tests** 全过(老 spec 完全不动)。

## 风险与注意

1. **Event dispatch 顺序契约不变** — connection.setupWebSocket 内部固定 `seq-gap → config.onEvent` 顺序;composition 的 dispatchEvent 内固定 `handlePostedEvent → handleTypingEvent → posts.upsertReactions`。任一顺序改动可能让 `recentBotMessageIds` 或 typing 状态错位
2. **`autoConnect` 5-param 签名沿用原 god-hook** — 同等列入 `eslint.config.mjs` `max-params` exemption。memory `feedback_no_subjective_lint_tightening` 支持不主动加严
3. **`getCurrentUserId` 是 ref 读** — useMemo 用 `connection.currentUser?.id` 做 deps,handlePostedEvent 内用 `connection.getCurrentUserId()` 做 call-time 读;两路径都正确
4. **pendingBackfillRef 不再 composition 持有** — 进 connection 后,handleVisible 内部自处理 drain;composition 不再 know about it

## 后续 PR

- **PR 4** — composition 收尾:核对 `useChatMessaging` 的 `...mm` rest spread,逐字段对照 `UseMattermostReturn`;若 composition 仍 > 200 行,审视 handlePostedEvent dispatcher 拆 helper

---

## 7fb27eed
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-26T15:09:04Z
- **SHA:** 7fb27eed0c86f18aaa35504f19739fe79d37571f

### Commit Message
```
refactor(web): extract useMattermostPosts from useMattermost god-hook (#1950)

## 背景

issue
[#368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368)
F15 — 4-PR 拆分计划的 **PR 2 / 4**(PR 1 #1946 已 merge)。设计文档
`docs/superpowers/specs/2026-05-26-issue-368-f15-usemattermost-refactor.md`。

## 改动

抽 **post 数据层**(状态 + 分页 + 历史/backfill + 反应)为独立 sub-hook:

| 模块 | 行数 | 内容 |
|---|---|---|
| `src/hooks/mattermost/useMattermostPosts.ts` | 317 | 4 state(postStore
/ hasMore / activeChannelHistoryReady / reactionsByPostId)+ 2
ref(lastCreateAt / pageByChannel)+ 5 mutator + 4 async helper + reaction
event 处理 |
| `src/lib/mattermost/post-store.ts` | 50 | `PostStore`
类型、`EMPTY_STORE`、`propsEqual`(JSON 深比较)、`postToMessage` 纯函数 |

`useMattermost.ts`: **870 → 607 行 (-263)**,顶层 useState **11 → 6**,顶层
useRef **16 → 14**。

### Composition layer 保留的内容

- `isLoading` / `error` / `setError`(跨多个 hook 的操作错误)
- `pendingBackfillRef`(visibility-defer 是连接侧关注)
- `lastSeqRef`(WS sequence 跟踪,PR 3 时随连接一起搬)
- 所有 `useStableCallback` 编排:`connect` / `disconnect` / `selectChannel` /
`sendMessage` / `autoConnect` / `loadMoreHistory` /
`clearWaitingForBotReply`
- 事件分发(`ws.onEvent` 回调):调
posts.upsertReactions、posts.syncPosts、posts.backfillFileInfos 三个 mutator
- `fetchMissedMessages` 薄包装(visibility check +
`posts.backfillChannels(api)`)

### 事件次序契约(PR 1 junction box)保留

`handlePostedEvent` 调用次序与原一致:`typing.clearOnPost → posts.syncPosts →
posts.backfillFileInfos → typing.markRecentBot →
typing.markStreamingEdit`。

## 验证

- `pnpm tsc --noEmit` ✓
- `pnpm lint` ✓
- `pnpm dup` ✓(tests dup 6.1% 远低 7.5% 阈值)
- `UseMattermostReturn` 形状逐字段不变 → `MattermostProvider` /
`MattermostContext` / 全 5 consumer 零改动
- 现 `useMattermost.unit.spec.ts` / `MattermostContext.unit.spec.tsx` /
`useChatMessaging.unit.spec.ts` 不改 pass
- 新增 17 单测覆盖 syncPosts / removePost(含 idempotent + props-only edit 检测)/
resetStore(保留 reactions + hasMore 的原 god-hook semantic)/
upsertReactions(含 add/remove/duplicate-no-op/malformed JSON)/
fetchInitialHistory / loadMorePage(每次 page+1)/ backfillChannels(含
exhausted retry + Sentry breadcrumb)/ backfillFileInfos(含 skip 路径)

总测试 **6 spec × 128 tests** 全过。

## 风险

1. `syncPosts` 的 prop-only edit 检测(bot streaming finalize)逻辑 263 行整块搬,保持
`propsEqual` 行为完全一致(JSON 比较);新 spec 单独覆盖此分支
2. `backfillChannels` 取自原 `fetchMissedMessages` 内圈,4 次指数退避 + Sentry
breadcrumb 在 online 时上报 — 新 spec 用 fake timers 模拟完整 retry 序列
3. `useChatMessaging` 的 `...mm` rest spread 仍存在(PR 4 收尾);本次 spec
已确认其使用的字段全部依然在 `UseMattermostReturn` 中
4. `pendingBackfillRef` / `lastSeqRef` 仍在 composition,PR 3 抽
`useMattermostConnection` 时会随之迁出
5. `resetStore()` 保留原 god-hook 不重置 `reactionsByPostId` 和 `hasMore`
的语义(memory 记录该 semantic 跨 disconnect/reconnect cycle 保留,仅 uid-key 外层
remount 才清)

## 后续 PR

- **PR 3** — 抽 `useMattermostConnection`(WS 生命周期 + 指数退避重连 + visibility
恢复 + currentUser / activeChannelId / isLoading / error 等)
- **PR 4** — composition 收尾,目标 `useMattermost.ts` ≤ 200
行;`useChatMessaging` 的 `...mm` rest spread 逐字段对照
```

### PR #1950: refactor(web): extract useMattermostPosts from useMattermost god-hook

**PR Description:**
## 背景

issue [#368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368) F15 — 4-PR 拆分计划的 **PR 2 / 4**(PR 1 #1946 已 merge)。设计文档 `docs/superpowers/specs/2026-05-26-issue-368-f15-usemattermost-refactor.md`。

## 改动

抽 **post 数据层**(状态 + 分页 + 历史/backfill + 反应)为独立 sub-hook:

| 模块 | 行数 | 内容 |
|---|---|---|
| `src/hooks/mattermost/useMattermostPosts.ts` | 317 | 4 state(postStore / hasMore / activeChannelHistoryReady / reactionsByPostId)+ 2 ref(lastCreateAt / pageByChannel)+ 5 mutator + 4 async helper + reaction event 处理 |
| `src/lib/mattermost/post-store.ts` | 50 | `PostStore` 类型、`EMPTY_STORE`、`propsEqual`(JSON 深比较)、`postToMessage` 纯函数 |

`useMattermost.ts`: **870 → 607 行 (-263)**,顶层 useState **11 → 6**,顶层 useRef **16 → 14**。

### Composition layer 保留的内容

- `isLoading` / `error` / `setError`(跨多个 hook 的操作错误)
- `pendingBackfillRef`(visibility-defer 是连接侧关注)
- `lastSeqRef`(WS sequence 跟踪,PR 3 时随连接一起搬)
- 所有 `useStableCallback` 编排:`connect` / `disconnect` / `selectChannel` / `sendMessage` / `autoConnect` / `loadMoreHistory` / `clearWaitingForBotReply`
- 事件分发(`ws.onEvent` 回调):调 posts.upsertReactions、posts.syncPosts、posts.backfillFileInfos 三个 mutator
- `fetchMissedMessages` 薄包装(visibility check + `posts.backfillChannels(api)`)

### 事件次序契约(PR 1 junction box)保留

`handlePostedEvent` 调用次序与原一致:`typing.clearOnPost → posts.syncPosts → posts.backfillFileInfos → typing.markRecentBot → typing.markStreamingEdit`。

## 验证

- `pnpm tsc --noEmit` ✓
- `pnpm lint` ✓
- `pnpm dup` ✓(tests dup 6.1% 远低 7.5% 阈值)
- `UseMattermostReturn` 形状逐字段不变 → `MattermostProvider` / `MattermostContext` / 全 5 consumer 零改动
- 现 `useMattermost.unit.spec.ts` / `MattermostContext.unit.spec.tsx` / `useChatMessaging.unit.spec.ts` 不改 pass
- 新增 17 单测覆盖 syncPosts / removePost(含 idempotent + props-only edit 检测)/ resetStore(保留 reactions + hasMore 的原 god-hook semantic)/ upsertReactions(含 add/remove/duplicate-no-op/malformed JSON)/ fetchInitialHistory / loadMorePage(每次 page+1)/ backfillChannels(含 exhausted retry + Sentry breadcrumb)/ backfillFileInfos(含 skip 路径)

总测试 **6 spec × 128 tests** 全过。

## 风险

1. `syncPosts` 的 prop-only edit 检测(bot streaming finalize)逻辑 263 行整块搬,保持 `propsEqual` 行为完全一致(JSON 比较);新 spec 单独覆盖此分支
2. `backfillChannels` 取自原 `fetchMissedMessages` 内圈,4 次指数退避 + Sentry breadcrumb 在 online 时上报 — 新 spec 用 fake timers 模拟完整 retry 序列
3. `useChatMessaging` 的 `...mm` rest spread 仍存在(PR 4 收尾);本次 spec 已确认其使用的字段全部依然在 `UseMattermostReturn` 中
4. `pendingBackfillRef` / `lastSeqRef` 仍在 composition,PR 3 抽 `useMattermostConnection` 时会随之迁出
5. `resetStore()` 保留原 god-hook 不重置 `reactionsByPostId` 和 `hasMore` 的语义(memory 记录该 semantic 跨 disconnect/reconnect cycle 保留,仅 uid-key 外层 remount 才清)

## 后续 PR

- **PR 3** — 抽 `useMattermostConnection`(WS 生命周期 + 指数退避重连 + visibility 恢复 + currentUser / activeChannelId / isLoading / error 等)
- **PR 4** — composition 收尾,目标 `useMattermost.ts` ≤ 200 行;`useChatMessaging` 的 `...mm` rest spread 逐字段对照

---

## 7aedc51c
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-26T14:41:23Z
- **SHA:** 7aedc51cb47c1ffa07b015c7bcc38c780f2f1d27

### Commit Message
```
refactor(web): extract useMattermostBotReady + useMattermostTyping from useMattermost god-hook (#1946)

## 背景

issue
[#368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368)
F15 — `useMattermost.ts` 963 行 god-hook,14 个 `useState` 混合七项职责。本 PR 是 4
PR 拆分计划的 **PR 1**,设计文档
`docs/superpowers/specs/2026-05-26-issue-368-f15-usemattermost-refactor.md`。

## 改动

抽出两个**互相独立、低耦合**的 sub-hook 到 `web/app/src/hooks/mattermost/`:

| Sub-hook | 行数 | 持有 |
|---|---|---|
| `useMattermostBotReady` | 79 | `botPollAttempt` state +
`botPollTimerRef`,Bot 上线 24 次轮询 + Sentry exhaustion 上报 |
| `useMattermostTyping` | 181 | `waitingByChannel` /
`recentBotMessageIds` / `streamingEditIds` state + 3 类 timer ref,负责 10
分钟 typing 超时 / 60s 自动消波等候 / 类型机 / 流式编辑跟踪 |

`useMattermost.ts` 行数 **963 → 867** (-96),顶层 useState **14 → 11**,顶层
useRef **20 → 16**。`handlePostedEvent` / `handleTypingEvent` /
`selectChannel` / `sendMessage` / `clearWaitingForBotReply` / `connect`
/ `disconnect` 都改成委托给 sub-hook mutator,不直接操作 setState/refs/timer。

## 验证

- `UseMattermostReturn` 形状逐字段不变 → `MattermostProvider` /
`MattermostContext` / 所有 5 个 consumer 零改动
- 现 `useMattermost.unit.spec.ts` / `MattermostContext.unit.spec.tsx` /
`useChatMessaging.unit.spec.ts` 不改 pass(107 tests 全过)
- 新增 23 单测覆盖两个 sub-hook 的状态切片、timer 行为、cancel/reset 路径,使用
`vi.advanceTimersByTimeAsync` 跑长轮询
- `pnpm tsc --noEmit` 通过
- `pnpm lint` / `pnpm dup` 通过(tests dup 6.13% 远低于 7.5% 阈值)

## 后续 PR(占位)

- **PR 2**: 抽 `useMattermostPosts`(postStore + 历史分页 + reactions +
propsEqual)
- **PR 3**: 抽 `useMattermostConnection`(WS 生命周期 + 指数退避重连 + visibility
恢复)
- **PR 4**: composition layer 收尾,目标 `useMattermost.ts` ≤ 200 行

## 风险

`handlePostedEvent` 是 god-hook 最高耦合点(一发同时写 postStore + waitingByChannel
+ recentBotMessageIds + streamingEditIds 4 个 slice)。本 PR 把后 3 个委托到
typing sub-hook,顺序保持 `clearOnPost → syncPosts(留主 hook)→ markRecentBot →
markStreamingEdit`,等同原序;`useMattermost.unit.spec.ts` 的跨频道隔离 + dedup + 重连
backfill 等用例继续 pass,验证语义未漂移。

## Out of scope

- `MattermostProvider` 的 auto-connect / retry recovery 逻辑(独立子系统)
- `MattermostAPIService` / `MattermostAuthService` /
`MattermostWebSocketService` 服务层(已独立)
- `useChatMessaging` 的 `...mm` rest spread 治理(PR 4 再收口)
```

### PR #1946: refactor(web): extract useMattermostBotReady + useMattermostTyping from useMattermost god-hook

**PR Description:**
## 背景

issue [#368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368) F15 — `useMattermost.ts` 963 行 god-hook,14 个 `useState` 混合七项职责。本 PR 是 4 PR 拆分计划的 **PR 1**,设计文档 `docs/superpowers/specs/2026-05-26-issue-368-f15-usemattermost-refactor.md`。

## 改动

抽出两个**互相独立、低耦合**的 sub-hook 到 `web/app/src/hooks/mattermost/`:

| Sub-hook | 行数 | 持有 |
|---|---|---|
| `useMattermostBotReady` | 79 | `botPollAttempt` state + `botPollTimerRef`,Bot 上线 24 次轮询 + Sentry exhaustion 上报 |
| `useMattermostTyping` | 181 | `waitingByChannel` / `recentBotMessageIds` / `streamingEditIds` state + 3 类 timer ref,负责 10 分钟 typing 超时 / 60s 自动消波等候 / 类型机 / 流式编辑跟踪 |

`useMattermost.ts` 行数 **963 → 867** (-96),顶层 useState **14 → 11**,顶层 useRef **20 → 16**。`handlePostedEvent` / `handleTypingEvent` / `selectChannel` / `sendMessage` / `clearWaitingForBotReply` / `connect` / `disconnect` 都改成委托给 sub-hook mutator,不直接操作 setState/refs/timer。

## 验证

- `UseMattermostReturn` 形状逐字段不变 → `MattermostProvider` / `MattermostContext` / 所有 5 个 consumer 零改动
- 现 `useMattermost.unit.spec.ts` / `MattermostContext.unit.spec.tsx` / `useChatMessaging.unit.spec.ts` 不改 pass(107 tests 全过)
- 新增 23 单测覆盖两个 sub-hook 的状态切片、timer 行为、cancel/reset 路径,使用 `vi.advanceTimersByTimeAsync` 跑长轮询
- `pnpm tsc --noEmit` 通过
- `pnpm lint` / `pnpm dup` 通过(tests dup 6.13% 远低于 7.5% 阈值)

## 后续 PR(占位)

- **PR 2**: 抽 `useMattermostPosts`(postStore + 历史分页 + reactions + propsEqual)
- **PR 3**: 抽 `useMattermostConnection`(WS 生命周期 + 指数退避重连 + visibility 恢复)
- **PR 4**: composition layer 收尾,目标 `useMattermost.ts` ≤ 200 行

## 风险

`handlePostedEvent` 是 god-hook 最高耦合点(一发同时写 postStore + waitingByChannel + recentBotMessageIds + streamingEditIds 4 个 slice)。本 PR 把后 3 个委托到 typing sub-hook,顺序保持 `clearOnPost → syncPosts(留主 hook)→ markRecentBot → markStreamingEdit`,等同原序;`useMattermost.unit.spec.ts` 的跨频道隔离 + dedup + 重连 backfill 等用例继续 pass,验证语义未漂移。

## Out of scope

- `MattermostProvider` 的 auto-connect / retry recovery 逻辑(独立子系统)
- `MattermostAPIService` / `MattermostAuthService` / `MattermostWebSocketService` 服务层(已独立)
- `useChatMessaging` 的 `...mm` rest spread 治理(PR 4 再收口)

---

## 6c7cc1ed
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-26T14:18:11Z
- **SHA:** 6c7cc1ed21eb73c7c4407929a3f222e5a5cfa36e

### Commit Message
```
fix(ci): restore Deploy badges via gist-backed shields.io endpoint (#1948)

## Summary

#1943 switched the three Deploy badges (Web / Enterprise Admin / Claw
Interface) to shields.io's `github/actions/workflow/status` endpoint to
get `style=for-the-badge` rendering, but this repo is **INTERNAL** —
shields.io has no access to private/internal repos and the README
currently renders **`DEPLOY: REPO OR WORKFLOW NOT FOUND`** for all three
rows.

This PR keeps the bigger `for-the-badge` style by mirroring the existing
coverage / E2E badge pattern:

1. Each deploy workflow gets a new `update-deploy-badge` job that writes
a `{label,message,color}` JSON to the public gist
[`7780840fe…`](https://gist.github.com/chris-srp/7780840fe6a8c160e1a73fdbcd5b786a)
(owned by chris-srp, already used for coverage + E2E badges) via
`schneegans/dynamic-badges-action@v1.7.0`.
2. The README's three Deploy badges now read those gist files via
`img.shields.io/endpoint?url=…&style=for-the-badge`. Public gist → no
auth needed → shields.io can fetch even though the source repo is
internal.
3. Gist files (`web-deploy-badge.json`,
`enterprise-admin-deploy-badge.json`, `service-deploy-badge.json`)
**seeded manually** with `{"message":"unknown","color":"lightgrey"}` so
the README renders immediately, not after the next production deploy.

### Scope of badge updates

- **Only production deploys** touch the badge
(`needs.setup.outputs.environment == 'production'` for `deploy.yml` /
`deploy-enterprise-admin.yml`, and the `deploy-to-production` job's own
`-release` / `inputs.environment == 'production'` gating for
`service-deploy.yml`).
- Both **success and failure** write the badge (`if: always() && result
!= 'skipped' && result != 'cancelled'`) — `cancelled` doesn't flip the
badge to red.
- Dev / staging deploys never touch the badge → badge semantics: "last
production release status".

### Why not just revert to native `actions/workflows/X.yml/badge.svg`?

That works for internal repos (GitHub serves badges via viewer session
cookie) but doesn't support `style=for-the-badge` — the badges render as
the small thin style that #1943 was trying to escape. Going via a public
gist is the only way to combine "rendered for an internal repo" + "big
readable style".

## Test plan

- [ ] After merge, confirm README shows `DEPLOY: UNKNOWN` (grey) for all
three Deploy rows — the seeded gist content — instead of `REPO OR
WORKFLOW NOT FOUND`.
- [ ] On next production deploy (Web / Enterprise Admin / Claw
Interface), confirm the corresponding badge flips to `passing` (green)
and the run logs show the `update-deploy-badge` job ran exactly once.
- [ ] On a staging-only `main` push, confirm `update-deploy-badge` is
**skipped** (badge stays at last production value).
- [ ] Inject a production deploy failure (or eyeball the conditional
logic) — badge should flip to `failing` (red), not stay green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1948: fix(ci): restore Deploy badges via gist-backed shields.io endpoint

**PR Description:**
## Summary

#1943 switched the three Deploy badges (Web / Enterprise Admin / Claw Interface) to shields.io's `github/actions/workflow/status` endpoint to get `style=for-the-badge` rendering, but this repo is **INTERNAL** — shields.io has no access to private/internal repos and the README currently renders **`DEPLOY: REPO OR WORKFLOW NOT FOUND`** for all three rows.

This PR keeps the bigger `for-the-badge` style by mirroring the existing coverage / E2E badge pattern:

1. Each deploy workflow gets a new `update-deploy-badge` job that writes a `{label,message,color}` JSON to the public gist [`7780840fe…`](https://gist.github.com/chris-srp/7780840fe6a8c160e1a73fdbcd5b786a) (owned by chris-srp, already used for coverage + E2E badges) via `schneegans/dynamic-badges-action@v1.7.0`.
2. The README's three Deploy badges now read those gist files via `img.shields.io/endpoint?url=…&style=for-the-badge`. Public gist → no auth needed → shields.io can fetch even though the source repo is internal.
3. Gist files (`web-deploy-badge.json`, `enterprise-admin-deploy-badge.json`, `service-deploy-badge.json`) **seeded manually** with `{"message":"unknown","color":"lightgrey"}` so the README renders immediately, not after the next production deploy.

### Scope of badge updates

- **Only production deploys** touch the badge (`needs.setup.outputs.environment == 'production'` for `deploy.yml` / `deploy-enterprise-admin.yml`, and the `deploy-to-production` job's own `-release` / `inputs.environment == 'production'` gating for `service-deploy.yml`).
- Both **success and failure** write the badge (`if: always() && result != 'skipped' && result != 'cancelled'`) — `cancelled` doesn't flip the badge to red.
- Dev / staging deploys never touch the badge → badge semantics: "last production release status".

### Why not just revert to native `actions/workflows/X.yml/badge.svg`?

That works for internal repos (GitHub serves badges via viewer session cookie) but doesn't support `style=for-the-badge` — the badges render as the small thin style that #1943 was trying to escape. Going via a public gist is the only way to combine "rendered for an internal repo" + "big readable style".

## Test plan

- [ ] After merge, confirm README shows `DEPLOY: UNKNOWN` (grey) for all three Deploy rows — the seeded gist content — instead of `REPO OR WORKFLOW NOT FOUND`.
- [ ] On next production deploy (Web / Enterprise Admin / Claw Interface), confirm the corresponding badge flips to `passing` (green) and the run logs show the `update-deploy-badge` job ran exactly once.
- [ ] On a staging-only `main` push, confirm `update-deploy-badge` is **skipped** (badge stays at last production value).
- [ ] Inject a production deploy failure (or eyeball the conditional logic) — badge should flip to `failing` (red), not stay green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 96cfed99
- **Author:** bill-srp
- **Date:** 2026-05-26T08:46:43Z
- **SHA:** 96cfed9987cb3c998c3bb3fb95804907be985f1e

### Commit Message
```
feat(enterprise): pass team wallet billing mode (#1944)

## Summary
- Pass billing_mode through BillingGatewayClient add-user-to-team calls.
- Set business billing mode for team org creation and invite joins;
leave personal org creation unchanged for backward compatibility.
- Accept the billing metadata fields returned by the billing-gateway
add-user-to-team API.

Linear:
https://linear.app/srpone/issue/ECA-827/support-team-wallet-user-usage-billing

## Test plan
- docker exec enterprise-bill bash -lc "cd
/workspaces/enterprise/services/claw-interface &&
/home/node/.venvs/claw-interface/bin/ruff check ."
- docker exec enterprise-bill bash -lc "cd
/workspaces/enterprise/services/claw-interface &&
/home/node/.venvs/claw-interface/bin/ruff format --check
app/services/billing_client_user_keys.py
app/services/org/membership_service.py app/services/org/org_service.py
app/schema/billing_gateway.py tests/unit/test_billing_client.py
tests/unit/test_membership_service.py tests/unit/test_org_service.py"
- docker exec enterprise-bill bash -lc "cd
/workspaces/enterprise/services/claw-interface &&
/home/node/.venvs/claw-interface/bin/pytest
tests/unit/test_billing_client.py tests/unit/test_membership_service.py
tests/unit/test_org_service.py -q"
- pyright: not run locally; pyright is not installed in the
devcontainer.
- Full pytest coverage attempted locally; failed due existing/local
suite issues (deptry worktree git path, unclosed socket warnings in
openclaw tests, and 87.94% total coverage vs 90% gate).
```

### PR #1944: feat(enterprise): pass team wallet billing mode

**PR Description:**
## Summary
- Pass billing_mode through BillingGatewayClient add-user-to-team calls.
- Set business billing mode for team org creation and invite joins; leave personal org creation unchanged for backward compatibility.
- Accept the billing metadata fields returned by the billing-gateway add-user-to-team API.

Linear: https://linear.app/srpone/issue/ECA-827/support-team-wallet-user-usage-billing

## Test plan
- docker exec enterprise-bill bash -lc "cd /workspaces/enterprise/services/claw-interface && /home/node/.venvs/claw-interface/bin/ruff check ."
- docker exec enterprise-bill bash -lc "cd /workspaces/enterprise/services/claw-interface && /home/node/.venvs/claw-interface/bin/ruff format --check app/services/billing_client_user_keys.py app/services/org/membership_service.py app/services/org/org_service.py app/schema/billing_gateway.py tests/unit/test_billing_client.py tests/unit/test_membership_service.py tests/unit/test_org_service.py"
- docker exec enterprise-bill bash -lc "cd /workspaces/enterprise/services/claw-interface && /home/node/.venvs/claw-interface/bin/pytest tests/unit/test_billing_client.py tests/unit/test_membership_service.py tests/unit/test_org_service.py -q"
- pyright: not run locally; pyright is not installed in the devcontainer.
- Full pytest coverage attempted locally; failed due existing/local suite issues (deptry worktree git path, unclosed socket warnings in openclaw tests, and 87.94% total coverage vs 90% gate).

---

## e2e1b7fe
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-26T07:29:46Z
- **SHA:** e2e1b7fe7e6c1c38dd6101a1be3aaf49d8ba71e0

### Commit Message
```
docs: restructure README badges layout (#1943)

## Summary

- Trim the main status table to two columns: **Deploy** and **Test
Coverage** (was Platform / Deploy / Tests / Coverage)
- Move the Web E2E test badges (E2E Tests workflow status,
total/passing/duration) into a dedicated **E2E Tests (Web)** section
below the table, where they have room to render on one wide line instead
of being squeezed into a narrow cell
- Switch the Deploy badges (Web / Enterprise Admin / Claw Interface) to
shields.io's `style=for-the-badge` rendering so the labels are readable
at a glance — the previous `actions/workflows/X.yml/badge.svg` badges
rendered very small and thin

## Test plan

- [ ] Confirm README renders correctly on GitHub (table layout, badge
sizes, E2E section below table)
- [ ] Verify Deploy badges still link to the correct workflow runs
- [ ] Verify Coverage and E2E badges still resolve from the existing
gist endpoints
```

### PR #1943: docs: restructure README badges layout

**PR Description:**
## Summary

- Trim the main status table to two columns: **Deploy** and **Test Coverage** (was Platform / Deploy / Tests / Coverage)
- Move the Web E2E test badges (E2E Tests workflow status, total/passing/duration) into a dedicated **E2E Tests (Web)** section below the table, where they have room to render on one wide line instead of being squeezed into a narrow cell
- Switch the Deploy badges (Web / Enterprise Admin / Claw Interface) to shields.io's `style=for-the-badge` rendering so the labels are readable at a glance — the previous `actions/workflows/X.yml/badge.svg` badges rendered very small and thin

## Test plan

- [ ] Confirm README renders correctly on GitHub (table layout, badge sizes, E2E section below table)
- [ ] Verify Deploy badges still link to the correct workflow runs
- [ ] Verify Coverage and E2E badges still resolve from the existing gist endpoints

---

## 5aa4ad5b
- **Author:** bill-srp
- **Date:** 2026-05-26T07:13:20Z
- **SHA:** 5aa4ad5b208ee333ad37c484e741a7be3998992a

### Commit Message
```
fix(enterprise): authenticate pack asset downloads (#1942)

## Summary
- Change pack submission asset download from direct cross-origin fetch
to a same-origin Next.js API route
- Send the account token to `/api/r2/pack-assets/<asset_id>`; the API
validates it against `/account/me`
- Require the requested R2 key to be under the caller membership org id
before reading from `R2_AGENT_PACKS_BUCKET`
- Stream the ZIP with attachment headers
- Revert pack archive uploads to returning only the internal R2 key, not
a public URL
- Add route coverage for auth rejection, forbidden missing membership,
cross-org rejection, R2 streaming, and 404s

## Root cause
Pack asset downloads require an auth token in the request header. A
direct browser request to `agentpack.zooclaw.ai` would depend on
cross-origin CORS/preflight behavior in deployment. A same-origin API
route is a tighter contract: the browser calls the enterprise admin app,
the app validates auth and org scope, then reads the R2 binding
directly.

## Test plan
- [x] pnpm --dir web/enterprise-admin test
components/packs/__tests__/SubmissionList.test.tsx
app/(dashboard)/packs/[packId]/__tests__/pack-detail-page.test.tsx
lib/r2/__tests__/index.test.ts app/api/r2/upload/__tests__/route.test.ts
app/api/r2/pack-assets/[...key]/__tests__/route.test.ts
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit
- [x] pnpm --dir web/enterprise-admin exec eslint . --max-warnings=0
--cache --cache-location .eslintcache --cache-strategy content
--ignore-pattern coverage
```

### PR #1942: fix(enterprise): authenticate pack asset downloads

**PR Description:**
## Summary
- Change pack submission asset download from direct cross-origin fetch to a same-origin Next.js API route
- Send the account token to `/api/r2/pack-assets/<asset_id>`; the API validates it against `/account/me`
- Require the requested R2 key to be under the caller membership org id before reading from `R2_AGENT_PACKS_BUCKET`
- Stream the ZIP with attachment headers
- Revert pack archive uploads to returning only the internal R2 key, not a public URL
- Add route coverage for auth rejection, forbidden missing membership, cross-org rejection, R2 streaming, and 404s

## Root cause
Pack asset downloads require an auth token in the request header. A direct browser request to `agentpack.zooclaw.ai` would depend on cross-origin CORS/preflight behavior in deployment. A same-origin API route is a tighter contract: the browser calls the enterprise admin app, the app validates auth and org scope, then reads the R2 binding directly.

## Test plan
- [x] pnpm --dir web/enterprise-admin test components/packs/__tests__/SubmissionList.test.tsx app/(dashboard)/packs/[packId]/__tests__/pack-detail-page.test.tsx lib/r2/__tests__/index.test.ts app/api/r2/upload/__tests__/route.test.ts app/api/r2/pack-assets/[...key]/__tests__/route.test.ts
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit
- [x] pnpm --dir web/enterprise-admin exec eslint . --max-warnings=0 --cache --cache-location .eslintcache --cache-strategy content --ignore-pattern coverage

---

## 6b57c598
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-26T05:28:57Z
- **SHA:** 6b57c598a36940af87b03cdffe2aef326f9e07f0

### Commit Message
```
chore(web): drop stale SideNav.tsx exemptions (#1941)

## Summary

Post-refactor cleanup of stale `src/components/SideNav.tsx` path
references in two config files. The file moved to
`src/components/sidenav/SideNav.tsx` as part of the 4-PR split (#1935 /
#1937 / #1938 / #1939, all merged).

Both entries are **deletions only** — there's no need to update the path
to the new location, because:

- **`eslint.config.mjs`** (legacy complexity override): The new
`sidenav/SideNav.tsx` is 172 lines with the main function body under 150
lines. It complies with the default `complexity` / `max-depth` /
`max-params` / `max-lines-per-function` / `max-nested-callbacks` /
`max-lines` thresholds without needing exemption. Verified: `pnpm lint`
green without the override.
- **`vitest.config.mts`** (coverage exclude — "Pure UI components,
shadcn, nav, layout shells"): The refactored sub-components (8
components + 2 hooks + 1 builder) are individually unit-tested via 11
spec files / 72 cases, so the "skip from coverage" carve-out no longer
applies. We **want** the new files counted toward coverage.

## Test plan

- [x] `pnpm exec tsc --noEmit` → 0 errors
- [x] `pnpm lint` → 0 errors / 0 warnings (proves new files comply
without the complexity exemption)
- [x] `pnpm test:unit` → 5792 passed (no regression from removing the
coverage exclude)

## Other locations audited (no changes needed)

- `web/scripts/check-*-shrink-only.sh`: no `SideNav` entries
- ESLint shrink-only blocks (`no-raw-fetch`, `svg-inline`,
`react/forbid-dom-props`, `filename-naming`): no `SideNav` entries
- `knip.config.ts` / `.dependency-cruiser.cjs` /
`.jscpd.{src,tests}.json`: no `SideNav` entries
- `web/app/CLAUDE.md`: no `SideNav` mentions (and per
`feedback_claude_md_no_inventory`, we don't list canonical module
references there)
- Other `SideNav` mentions in source (Sentry message strings, comments
in `useBillingCredits.ts` / `useNavIdentity.ts` / `useOpenClawInit.ts`):
describe behavior, not paths — kept as-is

Tracks the refactor closure noted in #368 manual notes (2026-05-26
Progress update) and the closed #1926.
```

### PR #1941: chore(web): drop stale SideNav.tsx exemptions

**PR Description:**
## Summary

Post-refactor cleanup of stale `src/components/SideNav.tsx` path references in two config files. The file moved to `src/components/sidenav/SideNav.tsx` as part of the 4-PR split (#1935 / #1937 / #1938 / #1939, all merged).

Both entries are **deletions only** — there's no need to update the path to the new location, because:

- **`eslint.config.mjs`** (legacy complexity override): The new `sidenav/SideNav.tsx` is 172 lines with the main function body under 150 lines. It complies with the default `complexity` / `max-depth` / `max-params` / `max-lines-per-function` / `max-nested-callbacks` / `max-lines` thresholds without needing exemption. Verified: `pnpm lint` green without the override.
- **`vitest.config.mts`** (coverage exclude — "Pure UI components, shadcn, nav, layout shells"): The refactored sub-components (8 components + 2 hooks + 1 builder) are individually unit-tested via 11 spec files / 72 cases, so the "skip from coverage" carve-out no longer applies. We **want** the new files counted toward coverage.

## Test plan

- [x] `pnpm exec tsc --noEmit` → 0 errors
- [x] `pnpm lint` → 0 errors / 0 warnings (proves new files comply without the complexity exemption)
- [x] `pnpm test:unit` → 5792 passed (no regression from removing the coverage exclude)

## Other locations audited (no changes needed)

- `web/scripts/check-*-shrink-only.sh`: no `SideNav` entries
- ESLint shrink-only blocks (`no-raw-fetch`, `svg-inline`, `react/forbid-dom-props`, `filename-naming`): no `SideNav` entries
- `knip.config.ts` / `.dependency-cruiser.cjs` / `.jscpd.{src,tests}.json`: no `SideNav` entries
- `web/app/CLAUDE.md`: no `SideNav` mentions (and per `feedback_claude_md_no_inventory`, we don't list canonical module references there)
- Other `SideNav` mentions in source (Sentry message strings, comments in `useBillingCredits.ts` / `useNavIdentity.ts` / `useOpenClawInit.ts`): describe behavior, not paths — kept as-is

Tracks the refactor closure noted in #368 manual notes (2026-05-26 Progress update) and the closed #1926.

---

## bd6b24f8
- **Author:** bill-srp
- **Date:** 2026-05-26T04:32:49Z
- **SHA:** bd6b24f807a11138981dc45daa55978602bcccd6

### Commit Message
```
fix(enterprise): clean up pack submission history (#1940)

## Summary
- Remove the duplicated Version history section from the pack detail
page
- Add per-submission asset links pointing at
https://agentpack.zooclaw.ai
- Define the pack archive public domain in the R2 upload contract/config
- Cover the visible history behavior, generated asset URLs, and pack
archive public URLs with tests

## Root cause
The pack detail page rendered both Submission history and Version
history from the same versions API payload, so admins saw duplicated
rows. The remaining history table also did not expose the uploaded asset
URL, and the storage contract previously treated pack archives as having
no public URL.

## Test plan
- [x] pnpm --dir web/enterprise-admin exec eslint . --max-warnings=0
--cache --cache-location .eslintcache --cache-strategy content
--ignore-pattern coverage
- [x] pnpm --dir web/enterprise-admin run test
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit

Note: `pnpm --dir web/enterprise-admin run lint` hits an ignored local
coverage artifact in this worktree
(`web/enterprise-admin/coverage/block-navigation.js`). The equivalent
eslint check above ignores coverage and passed.
```

### PR #1940: fix(enterprise): clean up pack submission history

**PR Description:**
## Summary
- Remove the duplicated Version history section from the pack detail page
- Add per-submission asset download actions for https://agentpack.zooclaw.ai assets
- Fetch pack assets with the stored account token in the Authorization header before saving the blob
- Define the pack archive public domain in the R2 upload contract/config
- Cover the visible history behavior, authenticated asset fetch, and pack archive public URLs with tests

## Root cause
The pack detail page rendered both Submission history and Version history from the same versions API payload, so admins saw duplicated rows. The remaining history table also did not expose the uploaded asset URL. Pack asset downloads require authenticated requests, so a direct anchor link could not attach the required Authorization header.

## Test plan
- [x] pnpm --dir web/enterprise-admin exec eslint . --max-warnings=0 --cache --cache-location .eslintcache --cache-strategy content --ignore-pattern coverage
- [x] pnpm --dir web/enterprise-admin test components/packs/__tests__/SubmissionList.test.tsx app/(dashboard)/packs/[packId]/__tests__/pack-detail-page.test.tsx
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit

Note: `pnpm --dir web/enterprise-admin run lint` hits an ignored local coverage artifact in this worktree (`web/enterprise-admin/coverage/block-navigation.js`). The equivalent eslint check above ignores coverage and passed.

---

## 9a216d2c
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-26T04:01:13Z
- **SHA:** 9a216d2c56125542750e50a56be3598f967487c3

### Commit Message
```
refactor(web): tighten SideNav data flow and drop useNavAuthState cascade (#1939)

## Summary

Follow-up to the SideNav refactor series (#1935 / #1937 / #1938).
Addresses the 5 React anti-patterns identified in the post-merge audit —
all behavior-preserving cleanups, no UI / network / event changes.

**Tracking**: #1926 (umbrella issue #368 F11) — series was already
closed; these are post-merge polish items.

Two commits:

### Commit 1 — `refactor(web): drop useNavAuthState cold-start cascade`

The two effects in `useNavAuthState` were calling `checkUserStatus()`
twice on initial mount: once directly from the mount effect, then again
when `setIsMounted(true)` flipped `isMounted` and tripped the pathname
effect's dep array. Both calls were idempotent (sync localStorage), but
the cascade is exactly the "derived-via-effect" pattern React's docs
warn against.

Consolidate the initial read into the pathname effect (it already fires
on mount via the `pathname` dep) and drop the redundant
`checkUserStatus()` in the mount effect. The `isMounted` guard in the
pathname effect was protecting against an SSR-time call that can't
happen — `useEffect` doesn't run during SSR — so it goes too.

Regression test asserts `isLoggedIn()` is called exactly once on cold
start.

### Commit 2 — `refactor(web): tighten SideNav data flow and rename
useBottomNavItems`

Four cleanups bundled because they share the same audit motivation
(parent component as accidental data funnel):

1. **Lift `useBillingCredits` / `useBrandVocabulary` /
`useLocalizedRouter` into `SideNavUserSection`.** The parent was only
consuming these to forward them as props — the actual consumer was
always `UserInfoSection` (and `t` for `LoginButton`). Calling the hooks
where the data is actually used drops **7 props** from `SideNav →
SideNavUserSection` (`availableCredits`, `billingPlan`,
`hookSubscriptionStatus`, `hookTrialEndTime`, `creditsUnitLower`,
`router`, `t`).
2. **Replace `getUserInfo().uid` with `userInfo.uid`** from
`useNavAuthState`. The hook already owns the listener pair that keeps
`userInfo` fresh on cross-tab + same-tab auth changes (including in-app
account switches that emit `auth-state-changed`), so the parallel
localStorage read was redundant.
3. **Hoist `formatCredits` to module scope.** Pure function with no
closure capture.
4. **Rename `useBottomNavItems` → `buildBottomNavItems`** at
`sidenav/build-bottom-nav-items.ts`. PR 2 (#1937) review flagged the
`use*` prefix as misleading: no `useState` / `useEffect` inside, so it's
a pure derivation. Filename moves to kebab-case per the
`components/**/!(use[A-Z]*).ts` rule.

### Out of scope (deferred to a separate spec)

- **`useAgentScrollOverlay` rename re-measure gap** (Codex #1937
finding): production key `extraAgents.map(a => a.id).join(',')` doesn't
fire on rename. The proper fix is `ResizeObserver` (layout-driven
re-measure picks up rename, image load, font swap), which is a
behavior-changing improvement and warrants its own spec.

## Diff stats

| | Lines |
|---|---:|
| `SideNav.tsx` | -16 |
| `SideNavUserSection.tsx` props | 14 → 9 (-5) |
| `SideNavUserSection.tsx` body | net no change (hook calls moved in,
prop reads moved out) |
| `useNavAuthState.ts` | +5 / -3 (comment + structural) |
| `buildBottomNavItems` file move | rename only |
| Tests | +9 / -7 |

## Test plan

- [x] `pnpm exec tsc --noEmit` → 0 errors
- [x] `pnpm lint` → 0 errors / 0 warnings
- [x] `pnpm test:unit` → 5792 passed / 1 todo (381 files); 1 new
regression test, ~10 existing tests updated for new prop shapes
- [x] `pnpm dup:src` → 3.76% (< 4.5% threshold)
- [x] `pnpm dup:tests` → 6.15% (< 7.0% threshold)
- [x] `pnpm lint:ci` (import-boundaries + knip + shrink-only) → all pass

### Staging smoke check (post-merge)

- [ ] Cold start (logged-in): `/chat` loads, SideNav renders user card;
DevTools "Performance" cold-start profile shows one `isLoggedIn`
invocation in `useNavAuthState` instead of two
- [ ] Cross-tab logout: tab A logs out → tab B's `LoginButton` appears
without manual refresh (same as before — the listener path didn't
change)
- [ ] Account switch within same tab (impersonate flow):
`auth-state-changed` fires → `userInfo.uid` updates → `useNavIdentity`
requeries with the new uid (validates the navUid switch)
- [ ] Collapsed-desktop logged-in: `UserInfoSection` hover tooltip shows
credits + plan label correctly (validates lifted `useBillingCredits` +
`useBrandVocabulary`)
- [ ] Bottom nav `Zoo Square` click while badge present → badge clears;
`Schedule` / `User Guide` route correctly
```

### PR #1939: refactor(web): tighten SideNav data flow and drop useNavAuthState cascade

**PR Description:**
## Summary

Follow-up to the SideNav refactor series (#1935 / #1937 / #1938). Addresses the 5 React anti-patterns identified in the post-merge audit — all behavior-preserving cleanups, no UI / network / event changes.

**Tracking**: #1926 (umbrella issue #368 F11) — series was already closed; these are post-merge polish items.

Two commits:

### Commit 1 — `refactor(web): drop useNavAuthState cold-start cascade`

The two effects in `useNavAuthState` were calling `checkUserStatus()` twice on initial mount: once directly from the mount effect, then again when `setIsMounted(true)` flipped `isMounted` and tripped the pathname effect's dep array. Both calls were idempotent (sync localStorage), but the cascade is exactly the "derived-via-effect" pattern React's docs warn against.

Consolidate the initial read into the pathname effect (it already fires on mount via the `pathname` dep) and drop the redundant `checkUserStatus()` in the mount effect. The `isMounted` guard in the pathname effect was protecting against an SSR-time call that can't happen — `useEffect` doesn't run during SSR — so it goes too.

Regression test asserts `isLoggedIn()` is called exactly once on cold start.

### Commit 2 — `refactor(web): tighten SideNav data flow and rename useBottomNavItems`

Four cleanups bundled because they share the same audit motivation (parent component as accidental data funnel):

1. **Lift `useBillingCredits` / `useBrandVocabulary` / `useLocalizedRouter` into `SideNavUserSection`.** The parent was only consuming these to forward them as props — the actual consumer was always `UserInfoSection` (and `t` for `LoginButton`). Calling the hooks where the data is actually used drops **7 props** from `SideNav → SideNavUserSection` (`availableCredits`, `billingPlan`, `hookSubscriptionStatus`, `hookTrialEndTime`, `creditsUnitLower`, `router`, `t`).
2. **Replace `getUserInfo().uid` with `userInfo.uid`** from `useNavAuthState`. The hook already owns the listener pair that keeps `userInfo` fresh on cross-tab + same-tab auth changes (including in-app account switches that emit `auth-state-changed`), so the parallel localStorage read was redundant.
3. **Hoist `formatCredits` to module scope.** Pure function with no closure capture.
4. **Rename `useBottomNavItems` → `buildBottomNavItems`** at `sidenav/build-bottom-nav-items.ts`. PR 2 (#1937) review flagged the `use*` prefix as misleading: no `useState` / `useEffect` inside, so it's a pure derivation. Filename moves to kebab-case per the `components/**/!(use[A-Z]*).ts` rule.

### Out of scope (deferred to a separate spec)

- **`useAgentScrollOverlay` rename re-measure gap** (Codex #1937 finding): production key `extraAgents.map(a => a.id).join(',')` doesn't fire on rename. The proper fix is `ResizeObserver` (layout-driven re-measure picks up rename, image load, font swap), which is a behavior-changing improvement and warrants its own spec.

## Diff stats

| | Lines |
|---|---:|
| `SideNav.tsx` | -16 |
| `SideNavUserSection.tsx` props | 14 → 9 (-5) |
| `SideNavUserSection.tsx` body | net no change (hook calls moved in, prop reads moved out) |
| `useNavAuthState.ts` | +5 / -3 (comment + structural) |
| `buildBottomNavItems` file move | rename only |
| Tests | +9 / -7 |

## Test plan

- [x] `pnpm exec tsc --noEmit` → 0 errors
- [x] `pnpm lint` → 0 errors / 0 warnings
- [x] `pnpm test:unit` → 5792 passed / 1 todo (381 files); 1 new regression test, ~10 existing tests updated for new prop shapes
- [x] `pnpm dup:src` → 3.76% (< 4.5% threshold)
- [x] `pnpm dup:tests` → 6.15% (< 7.0% threshold)
- [x] `pnpm lint:ci` (import-boundaries + knip + shrink-only) → all pass

### Staging smoke check (post-merge)

- [ ] Cold start (logged-in): `/chat` loads, SideNav renders user card; DevTools "Performance" cold-start profile shows one `isLoggedIn` invocation in `useNavAuthState` instead of two
- [ ] Cross-tab logout: tab A logs out → tab B's `LoginButton` appears without manual refresh (same as before — the listener path didn't change)
- [ ] Account switch within same tab (impersonate flow): `auth-state-changed` fires → `userInfo.uid` updates → `useNavIdentity` requeries with the new uid (validates the navUid switch)
- [ ] Collapsed-desktop logged-in: `UserInfoSection` hover tooltip shows credits + plan label correctly (validates lifted `useBillingCredits` + `useBrandVocabulary`)
- [ ] Bottom nav `Zoo Square` click while badge present → badge clears; `Schedule` / `User Guide` route correctly

---

## 3bc3dbb6
- **Author:** bill-srp
- **Date:** 2026-05-26T03:37:26Z
- **SHA:** 3bc3dbb678ce16dde659171137188195a9326d27

### Commit Message
```
fix(enterprise): align invite onboarding flow (#1936)

## Summary
- split account registration into explicit `/account`,
`/account/personal-org`, and `/account/invite` paths
- document that old combined `POST /account` compatibility is
intentionally not kept because the split happened before release
- route enterprise join through `/account/invite` and guard missing
invite context before firing the mutation
- include non-expired pending org invites in `/orgs/{org_id}/users` and
render pending invite rows in admin users
- provision team org billing plan and grant initial team credits with a
retry-safe idempotent topup transaction

## Reviewer Notes
- `POST /account` is intentionally account-only; org creation and invite
redemption must use the split routes.
- Trial credits remain limited to newly created personal registrations.
- Duplicate-subscription handling is narrowed to duplicate-looking
Billing Gateway 400 responses.
- Pending invite rows exclude expired invites.

## Tests
- `docker exec enterprise-bill sh -lc "cd
/workspaces/enterprise/services/claw-interface && .venv/bin/python -m
ruff check app/services/org/org_service.py
tests/unit/test_org_service.py && .venv/bin/python -m pytest
tests/unit/test_org_service.py -q"`
- `docker exec enterprise-bill sh -lc "cd
/workspaces/enterprise/services/claw-interface && .venv/bin/python -m
ruff check app/routes/account.py"`
- `docker exec enterprise-bill sh -lc "cd
/workspaces/enterprise/services/claw-interface && .venv/bin/python -m
pytest tests/unit/test_org_invite_repo.py
tests/unit/test_routes_org_users.py -q"`
- focused backend account/org/org-users pytest suites passed
- `pnpm --dir web/enterprise-admin test
hooks/__tests__/useInvite.test.tsx`
- `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- focused enterprise-admin invite/users vitest suites passed
- `pnpm --dir web run test:unit`
- `pnpm --dir web/app exec tsc --noEmit`
- `pnpm --dir web/packages/auth-client exec tsc --noEmit`

## Local Check Notes
- `pnpm --dir web run lint` fails on pre-existing generated coverage
warning: `web/enterprise-admin/coverage/block-navigation.js`
- `pnpm --dir web run tsc` fails because the root script passes
unsupported `--if-present` to this local pnpm
- backend `pyright` is not installed in the devcontainer venv
- full backend pytest hits local worktree/devcontainer issues in deptry
and OpenClaw unclosed socket warnings; focused touched suites pass
```

### PR #1936: fix(enterprise): align invite onboarding flow

**PR Description:**
## Summary
- split account registration into explicit `/account`, `/account/personal-org`, and `/account/invite` paths
- document that old combined `POST /account` compatibility is intentionally not kept because the split happened before release
- route enterprise join through `/account/invite` and guard missing invite context before firing the mutation
- include non-expired pending org invites in `/orgs/{org_id}/users` and render pending invite rows in admin users
- provision team org billing plan and grant initial team credits with a retry-safe idempotent topup transaction

## Reviewer Notes
- `POST /account` is intentionally account-only; org creation and invite redemption must use the split routes.
- Trial credits remain limited to newly created personal registrations.
- Duplicate-subscription handling is narrowed to duplicate-looking Billing Gateway 400 responses.
- Pending invite rows exclude expired invites.

## Tests
- `docker exec enterprise-bill sh -lc "cd /workspaces/enterprise/services/claw-interface && .venv/bin/python -m ruff check app/services/org/org_service.py tests/unit/test_org_service.py && .venv/bin/python -m pytest tests/unit/test_org_service.py -q"`
- `docker exec enterprise-bill sh -lc "cd /workspaces/enterprise/services/claw-interface && .venv/bin/python -m ruff check app/routes/account.py"`
- `docker exec enterprise-bill sh -lc "cd /workspaces/enterprise/services/claw-interface && .venv/bin/python -m pytest tests/unit/test_org_invite_repo.py tests/unit/test_routes_org_users.py -q"`
- focused backend account/org/org-users pytest suites passed
- `pnpm --dir web/enterprise-admin test hooks/__tests__/useInvite.test.tsx`
- `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- focused enterprise-admin invite/users vitest suites passed
- `pnpm --dir web run test:unit`
- `pnpm --dir web/app exec tsc --noEmit`
- `pnpm --dir web/packages/auth-client exec tsc --noEmit`

## Local Check Notes
- `pnpm --dir web run lint` fails on pre-existing generated coverage warning: `web/enterprise-admin/coverage/block-navigation.js`
- `pnpm --dir web run tsc` fails because the root script passes unsupported `--if-present` to this local pnpm
- backend `pyright` is not installed in the devcontainer venv
- full backend pytest hits local worktree/devcontainer issues in deptry and OpenClaw unclosed socket warnings; focused touched suites pass

---

## d0b6148f
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-26T03:32:48Z
- **SHA:** d0b6148f52cb582cd24f32157c39485bcd96ab8f

### Commit Message
```
refactor(web): finalize SideNav split and relocate to sidenav/ (#1938)

## Summary

PR 3 of 3 in the SideNav refactor series — the finale. Continues #1937.
Two ordered commits:

1. **Extract**: `SideNavBottomNav` + `SideNavUserSection` extracted;
`PLAN_PRICES` moved to `sidenav/constants.ts`. `SideNav.tsx` goes 248 →
189 lines (function body ~150).
2. **Rename**: `git mv web/app/src/components/SideNav.tsx →
web/app/src/components/sidenav/SideNav.tsx`; only the one external
importer (`AppLayout.tsx`) updates; internal imports switch from
`@/components/sidenav/X` to `./X`.

The rename is the **last commit** so reviewers can read the extract diff
cleanly first.

**Spec**:
[`docs/superpowers/specs/2026-05-25-issue-368-f11-sidenav-refactor.md`](https://github.com/SerendipityOneInc/ecap-workspace/blob/main/docs/superpowers/specs/2026-05-25-issue-368-f11-sidenav-refactor.md)
**Tracking**: #1926 (umbrella issue #368 F11)
**Depends on**: #1937 (merged)

### Series outcome

| | Before PR 1 | After PR 3 |
|---|---|---|
| `SideNav.tsx` total | 876 | **189** (-78%) |
| Main function body | 506 | ~150 |
| Files in `sidenav/` | 0 | 8 components + 3 hooks + 2 module files |
| New unit tests | 0 | 71 across 8 spec files |

F11 issue goal "< 200 lines" met; spec aspirational target "≤ 150 lines
for the main function" met.

### Changes

- `sidenav/SideNavBottomNav.tsx` — sticky bottom-nav `<div>` + admin nav
block. Owns the `data-scroll-state` attr that `useAgentScrollOverlay`
drives.
- `sidenav/SideNavUserSection.tsx` — logged-in / logged-out branching
with `UserMenu` + `UserCard` + `UserInfoSection` + `LoginButton` +
`MobileAppModal`. Encapsulates `isUserMenuOpen`, `showMobileApp`, and
crucially `settingsMenuRef`. **Risk note** (per spec D2): the ref must
enclose both the trigger and the popup or `UserMenu`'s click-outside
detection breaks — guarded by a dedicated test.
- `sidenav/constants.ts` — gain `PLAN_PRICES` (moved from
`UserInfoSection`'s deferred inline copy).
- `UserInfoSection.tsx` — now imports `PLAN_PRICES` from `./constants`
instead of duplicating it.

### Final layout

```
web/app/src/components/sidenav/
  LoginButton.tsx            # PR 1
  NavItemComponent.tsx       # PR 1
  SideNav.tsx                # PR 3 (relocated from components/SideNav.tsx)
  SideNavAgentList.tsx       # PR 2
  SideNavBottomNav.tsx       # PR 3 (new)
  SideNavLogo.tsx            # PR 2
  SideNavUserSection.tsx     # PR 3 (new)
  UserInfoSection.tsx        # PR 1
  constants.ts               # PR 1, gains PLAN_PRICES in PR 3
  types.ts                   # PR 1
  hooks/
    useAgentScrollOverlay.ts # PR 2
    useBottomNavItems.ts     # PR 2
    useNavAuthState.ts       # PR 1
```

## Test plan

- [x] `pnpm exec tsc --noEmit` → 0 errors
- [x] `pnpm lint` → 0 errors / 0 warnings
- [x] `pnpm test:unit` → 5791 passed / 1 todo (381 files); 15 new tests
in PR 3
- [x] `pnpm dup:src` → 3.76% (< 4.5% threshold)
- [x] `pnpm dup:tests` → 6.15% (< 7.0% threshold)
- [x] `pnpm lint:ci` (import-boundaries + knip + shrink-only) → all pass

### Staging manual smoke (full F11 checklist post-merge)

- [ ] Desktop expanded + logged-in: `/chat` → switch `agent_id` → Zoo
Square / Schedule / User Guide
- [ ] Desktop collapsed + logged-in: nav-item hover tooltips +
`UserInfoSection` credits tooltip + avatar fallback char
- [ ] Desktop collapsed + logged-out: login icon + tooltip + LoginModal
- [ ] Mobile (< 768px) + hamburger: SideNav slides in, click closes menu
- [ ] **User menu click-outside** (PR 3 risk path): UserCard click opens
UserMenu → click anywhere outside the sticky-bottom section → UserMenu
closes
- [ ] ≥ 10 extra agents: scroll list → bottom-nav fade overlay shows →
scroll to bottom → fade disappears
- [ ] admin nav visible for admin / hidden for non-admin
- [ ] trial → "X days left"; pro → "Pro" label
- [ ] Cross-tab logout sync (PR 1 listener-merge)

### Size note

Per `feedback_pr_size_rename_doubles` the rename ~doubles `--shortstat`
counts (delete + add). The actual content change is the 9-line import
block at the top of the relocated file plus the 1-line `AppLayout`
import. Adding a `size-override` label if the size check trips would be
appropriate here.
```

### PR #1938: refactor(web): finalize SideNav split and relocate to sidenav/

**PR Description:**
## Summary

PR 3 of 3 in the SideNav refactor series — the finale. Continues #1937. Two ordered commits:

1. **Extract**: `SideNavBottomNav` + `SideNavUserSection` extracted; `PLAN_PRICES` moved to `sidenav/constants.ts`. `SideNav.tsx` goes 248 → 189 lines (function body ~150).
2. **Rename**: `git mv web/app/src/components/SideNav.tsx → web/app/src/components/sidenav/SideNav.tsx`; only the one external importer (`AppLayout.tsx`) updates; internal imports switch from `@/components/sidenav/X` to `./X`.

The rename is the **last commit** so reviewers can read the extract diff cleanly first.

**Spec**: [`docs/superpowers/specs/2026-05-25-issue-368-f11-sidenav-refactor.md`](https://github.com/SerendipityOneInc/ecap-workspace/blob/main/docs/superpowers/specs/2026-05-25-issue-368-f11-sidenav-refactor.md)
**Tracking**: #1926 (umbrella issue #368 F11)
**Depends on**: #1937 (merged)

### Series outcome

| | Before PR 1 | After PR 3 |
|---|---|---|
| `SideNav.tsx` total | 876 | **189** (-78%) |
| Main function body | 506 | ~150 |
| Files in `sidenav/` | 0 | 8 components + 3 hooks + 2 module files |
| New unit tests | 0 | 71 across 8 spec files |

F11 issue goal "< 200 lines" met; spec aspirational target "≤ 150 lines for the main function" met.

### Changes

- `sidenav/SideNavBottomNav.tsx` — sticky bottom-nav `<div>` + admin nav block. Owns the `data-scroll-state` attr that `useAgentScrollOverlay` drives.
- `sidenav/SideNavUserSection.tsx` — logged-in / logged-out branching with `UserMenu` + `UserCard` + `UserInfoSection` + `LoginButton` + `MobileAppModal`. Encapsulates `isUserMenuOpen`, `showMobileApp`, and crucially `settingsMenuRef`. **Risk note** (per spec D2): the ref must enclose both the trigger and the popup or `UserMenu`'s click-outside detection breaks — guarded by a dedicated test.
- `sidenav/constants.ts` — gain `PLAN_PRICES` (moved from `UserInfoSection`'s deferred inline copy).
- `UserInfoSection.tsx` — now imports `PLAN_PRICES` from `./constants` instead of duplicating it.

### Final layout

```
web/app/src/components/sidenav/
  LoginButton.tsx            # PR 1
  NavItemComponent.tsx       # PR 1
  SideNav.tsx                # PR 3 (relocated from components/SideNav.tsx)
  SideNavAgentList.tsx       # PR 2
  SideNavBottomNav.tsx       # PR 3 (new)
  SideNavLogo.tsx            # PR 2
  SideNavUserSection.tsx     # PR 3 (new)
  UserInfoSection.tsx        # PR 1
  constants.ts               # PR 1, gains PLAN_PRICES in PR 3
  types.ts                   # PR 1
  hooks/
    useAgentScrollOverlay.ts # PR 2
    useBottomNavItems.ts     # PR 2
    useNavAuthState.ts       # PR 1
```

## Test plan

- [x] `pnpm exec tsc --noEmit` → 0 errors
- [x] `pnpm lint` → 0 errors / 0 warnings
- [x] `pnpm test:unit` → 5791 passed / 1 todo (381 files); 15 new tests in PR 3
- [x] `pnpm dup:src` → 3.76% (< 4.5% threshold)
- [x] `pnpm dup:tests` → 6.15% (< 7.0% threshold)
- [x] `pnpm lint:ci` (import-boundaries + knip + shrink-only) → all pass

### Staging manual smoke (full F11 checklist post-merge)

- [ ] Desktop expanded + logged-in: `/chat` → switch `agent_id` → Zoo Square / Schedule / User Guide
- [ ] Desktop collapsed + logged-in: nav-item hover tooltips + `UserInfoSection` credits tooltip + avatar fallback char
- [ ] Desktop collapsed + logged-out: login icon + tooltip + LoginModal
- [ ] Mobile (< 768px) + hamburger: SideNav slides in, click closes menu
- [ ] **User menu click-outside** (PR 3 risk path): UserCard click opens UserMenu → click anywhere outside the sticky-bottom section → UserMenu closes
- [ ] ≥ 10 extra agents: scroll list → bottom-nav fade overlay shows → scroll to bottom → fade disappears
- [ ] admin nav visible for admin / hidden for non-admin
- [ ] trial → "X days left"; pro → "Pro" label
- [ ] Cross-tab logout sync (PR 1 listener-merge)

### Size note

Per `feedback_pr_size_rename_doubles` the rename ~doubles `--shortstat` counts (delete + add). The actual content change is the 9-line import block at the top of the relocated file plus the 1-line `AppLayout` import. Adding a `size-override` label if the size check trips would be appropriate here.

---

## 45fa6b7f
- **Author:** Nemo Feng
- **Date:** 2026-05-26T02:54:04Z
- **SHA:** 45fa6b7fdb77535907b610c2dc3fd853b402cf3b

### Commit Message
```
fix(web): wrap long unbreakable strings in chat markdown content (#1934)

## Problem

Sending a long unbreakable token (e.g. a base64 blob with no spaces)
into the chat made the rendered message bubble overflow horizontally
outside the chatbox.

## Root cause

`MarkdownContent` applied two conflicting values of the same CSS
property — `[overflow-wrap:anywhere]` **and** `break-words`
(`overflow-wrap: break-word`). In Tailwind v4's generated stylesheet,
`.break-words` is emitted after the arbitrary property, so the effective
computed value was `break-word`.

Unlike `anywhere`, `break-word` does **not** introduce soft-wrap
opportunities when computing an element's **min-content width**. So a
long unbreakable string keeps a huge min-content. Combined with the user
bubble's `w-fit` (shrink-to-fit), `fit-content` collapses to the full
string width and the bubble blows past the chat column.

## Fix

Replace the conflicting pair with Tailwind v4's native `wrap-anywhere`
utility (`overflow-wrap: anywhere`) — a single, unambiguous declaration.
`anywhere` reduces min-content, so the bubble wraps within its
container, and it also removes the latent cascade-order fragility.

`wrap-anywhere` over `break-all`: `break-all` (`word-break`) chops every
word mid-character and harms normal/CJK text; `anywhere` only breaks a
word when it would otherwise overflow.

## Verification

Reproduced against the real Tailwind v4 engine with the exact chat DOM
(user + assistant bubbles):

| Check | Before | After |
| --- | --- | --- |
| Computed `overflow-wrap` | `break-word` | `anywhere` |
| User bubble width (820px viewport) | 2892px (overflows) | 649px
(contained) |
| Assistant bubble | contained | contained |
| Short message | hugs content | hugs content |

Confirmed visually: the long string now wraps inside the bubble; short
messages still hug their content.

Linear: https://linear.app/srpone/issue/ECA-820/

Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>
```

### PR #1934: fix(web): wrap long unbreakable strings in chat markdown content

**PR Description:**
## Problem

Sending a long unbreakable token (e.g. a base64 blob with no spaces) into the chat made the rendered message bubble overflow horizontally outside the chatbox.

## Root cause

`MarkdownContent` applied two conflicting values of the same CSS property — `[overflow-wrap:anywhere]` **and** `break-words` (`overflow-wrap: break-word`). In Tailwind v4's generated stylesheet, `.break-words` is emitted after the arbitrary property, so the effective computed value was `break-word`.

Unlike `anywhere`, `break-word` does **not** introduce soft-wrap opportunities when computing an element's **min-content width**. So a long unbreakable string keeps a huge min-content. Combined with the user bubble's `w-fit` (shrink-to-fit), `fit-content` collapses to the full string width and the bubble blows past the chat column.

## Fix

Replace the conflicting pair with Tailwind v4's native `wrap-anywhere` utility (`overflow-wrap: anywhere`) — a single, unambiguous declaration. `anywhere` reduces min-content, so the bubble wraps within its container, and it also removes the latent cascade-order fragility.

`wrap-anywhere` over `break-all`: `break-all` (`word-break`) chops every word mid-character and harms normal/CJK text; `anywhere` only breaks a word when it would otherwise overflow.

## Verification

Reproduced against the real Tailwind v4 engine with the exact chat DOM (user + assistant bubbles):

| Check | Before | After |
| --- | --- | --- |
| Computed `overflow-wrap` | `break-word` | `anywhere` |
| User bubble width (820px viewport) | 2892px (overflows) | 649px (contained) |
| Assistant bubble | contained | contained |
| Short message | hugs content | hugs content |

Confirmed visually: the long string now wraps inside the bubble; short messages still hug their content.

Linear: https://linear.app/srpone/issue/ECA-820/

---

## 8983f52b
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-26T02:52:51Z
- **SHA:** 8983f52b5840d4e7107a33e2b5e652c40dcbd4a6

### Commit Message
```
refactor(web): split SideNav logo, agent list, and scroll hook (#1937)

## Summary

PR 2 of 3 in the SideNav refactor series. Continues #1935. Drops the
remaining region-level JSX (`SideNavLogo`, `SideNavAgentList`) and the
two layout-derived hooks (`useAgentScrollOverlay`, `useBottomNavItems`)
out of the main component. `SideNav.tsx` goes from **504 → 246 lines**.

**Spec**:
[`docs/superpowers/specs/2026-05-25-issue-368-f11-sidenav-refactor.md`](https://github.com/SerendipityOneInc/ecap-workspace/blob/main/docs/superpowers/specs/2026-05-25-issue-368-f11-sidenav-refactor.md)
**Tracking**: #1926 (umbrella issue #368 F11)
**Depends on**: #1935 (merged)

### Changes

- `sidenav/SideNavLogo.tsx` — expand / collapse / mobile branches of the
top-of-sidebar logo + toggle, with the two tooltip variants the original
inlined.
- `sidenav/SideNavAgentList.tsx` — AGENT header + main chat link +
per-agent rendering + the 48px scroll-end buffer. Receives `scrollRef` +
identity slice from the parent so `resolveChatIdentity` stays the one
source of truth.
- `sidenav/hooks/useAgentScrollOverlay.ts` — owns the `scrollHeight` /
`clientHeight` / `scrollTop` measurement + window resize listener.
Effect deps stay as the explicit `[extraAgentIdsKey, isCollapsed,
isMobile]` triple. **Regression guard**: agent rename changes
`extraAgentIdsKey` but not `extraAgents.length`, and the rendered width
can flip across the overflow line, so a `.length` shortcut would miss
it.
- `sidenav/hooks/useBottomNavItems.ts` — collects the three bottom nav
entries + admin entry + the `isActive(href)` matcher with all four
branches (`/chat`-without-agent_id / `/profile`-exact /
`/claw-settings`-nested / prefix match). Uses `React.createElement` for
icons so the file stays `.ts` per the `**/use[A-Z]*.ts` filename rule.

### Out of scope for this PR (PR 3)

- Sticky bottom-nav + user-section split into `SideNavBottomNav` /
`SideNavUserSection`.
- Move `PLAN_PRICES` from `UserInfoSection` into `sidenav/constants.ts`.
- `git mv web/app/src/components/SideNav.tsx → sidenav/SideNav.tsx` +
update `AppLayout` import.

### File layout after this PR

```
web/app/src/components/sidenav/
  LoginButton.tsx                # PR 1
  NavItemComponent.tsx           # PR 1
  SideNavAgentList.tsx           # PR 2 (new)
  SideNavLogo.tsx                # PR 2 (new)
  UserInfoSection.tsx            # PR 1
  constants.ts                   # PR 1
  types.ts                       # PR 1
  hooks/
    useAgentScrollOverlay.ts     # PR 2 (new)
    useBottomNavItems.ts         # PR 2 (new)
    useNavAuthState.ts           # PR 1
```

## Test plan

- [x] `pnpm exec tsc --noEmit` → 0 errors
- [x] `pnpm lint` → 0 errors / 0 warnings
- [x] `pnpm test:unit` → 5777 passed / 1 todo (379 files); 28 new tests
in PR 2
- [x] `pnpm dup:src` → 3.76% (< 4.5% threshold)
- [x] `pnpm dup:tests` → 6.15% (< 7.0% threshold)
- [x] `pnpm lint:ci` (import-boundaries + knip + shrink-only gates) →
all pass

### Staging manual smoke (post-merge, before PR 3 opens)

- [ ] Desktop expanded + logged-in: `/chat` → switch `agent_id` → click
Zoo Square / Schedule / User Guide
- [ ] Desktop collapsed: logo-mark + expand button hover tooltip works;
toggle expands
- [ ] Mobile (< 768px) + hamburger: SideNav slides in, agent click
closes menu
- [ ] **Agent rename** (the PR 2 risk path): rename an agent in
agents-manager → SideNav re-renders new name → if the list was
overflowing, the fade overlay state remains correct (no stuck
`data-scroll-state="overflow"` after the rename)
- [ ] `≥ 10` extra agents: scroll list → bottom-nav fade overlay shows →
scroll to bottom → fade disappears (`data-scroll-state="end"`)
- [ ] admin account shows Admin nav; non-admin hides it
```

### PR #1937: refactor(web): split SideNav logo, agent list, and scroll hook

**PR Description:**
## Summary

PR 2 of 3 in the SideNav refactor series. Continues #1935. Drops the remaining region-level JSX (`SideNavLogo`, `SideNavAgentList`) and the two layout-derived hooks (`useAgentScrollOverlay`, `useBottomNavItems`) out of the main component. `SideNav.tsx` goes from **504 → 246 lines**.

**Spec**: [`docs/superpowers/specs/2026-05-25-issue-368-f11-sidenav-refactor.md`](https://github.com/SerendipityOneInc/ecap-workspace/blob/main/docs/superpowers/specs/2026-05-25-issue-368-f11-sidenav-refactor.md)
**Tracking**: #1926 (umbrella issue #368 F11)
**Depends on**: #1935 (merged)

### Changes

- `sidenav/SideNavLogo.tsx` — expand / collapse / mobile branches of the top-of-sidebar logo + toggle, with the two tooltip variants the original inlined.
- `sidenav/SideNavAgentList.tsx` — AGENT header + main chat link + per-agent rendering + the 48px scroll-end buffer. Receives `scrollRef` + identity slice from the parent so `resolveChatIdentity` stays the one source of truth.
- `sidenav/hooks/useAgentScrollOverlay.ts` — owns the `scrollHeight` / `clientHeight` / `scrollTop` measurement + window resize listener. Effect deps stay as the explicit `[extraAgentIdsKey, isCollapsed, isMobile]` triple. **Regression guard**: agent rename changes `extraAgentIdsKey` but not `extraAgents.length`, and the rendered width can flip across the overflow line, so a `.length` shortcut would miss it.
- `sidenav/hooks/useBottomNavItems.ts` — collects the three bottom nav entries + admin entry + the `isActive(href)` matcher with all four branches (`/chat`-without-agent_id / `/profile`-exact / `/claw-settings`-nested / prefix match). Uses `React.createElement` for icons so the file stays `.ts` per the `**/use[A-Z]*.ts` filename rule.

### Out of scope for this PR (PR 3)

- Sticky bottom-nav + user-section split into `SideNavBottomNav` / `SideNavUserSection`.
- Move `PLAN_PRICES` from `UserInfoSection` into `sidenav/constants.ts`.
- `git mv web/app/src/components/SideNav.tsx → sidenav/SideNav.tsx` + update `AppLayout` import.

### File layout after this PR

```
web/app/src/components/sidenav/
  LoginButton.tsx                # PR 1
  NavItemComponent.tsx           # PR 1
  SideNavAgentList.tsx           # PR 2 (new)
  SideNavLogo.tsx                # PR 2 (new)
  UserInfoSection.tsx            # PR 1
  constants.ts                   # PR 1
  types.ts                       # PR 1
  hooks/
    useAgentScrollOverlay.ts     # PR 2 (new)
    useBottomNavItems.ts         # PR 2 (new)
    useNavAuthState.ts           # PR 1
```

## Test plan

- [x] `pnpm exec tsc --noEmit` → 0 errors
- [x] `pnpm lint` → 0 errors / 0 warnings
- [x] `pnpm test:unit` → 5777 passed / 1 todo (379 files); 28 new tests in PR 2
- [x] `pnpm dup:src` → 3.76% (< 4.5% threshold)
- [x] `pnpm dup:tests` → 6.15% (< 7.0% threshold)
- [x] `pnpm lint:ci` (import-boundaries + knip + shrink-only gates) → all pass

### Staging manual smoke (post-merge, before PR 3 opens)

- [ ] Desktop expanded + logged-in: `/chat` → switch `agent_id` → click Zoo Square / Schedule / User Guide
- [ ] Desktop collapsed: logo-mark + expand button hover tooltip works; toggle expands
- [ ] Mobile (< 768px) + hamburger: SideNav slides in, agent click closes menu
- [ ] **Agent rename** (the PR 2 risk path): rename an agent in agents-manager → SideNav re-renders new name → if the list was overflowing, the fade overlay state remains correct (no stuck `data-scroll-state="overflow"` after the rename)
- [ ] `≥ 10` extra agents: scroll list → bottom-nav fade overlay shows → scroll to bottom → fade disappears (`data-scroll-state="end"`)
- [ ] admin account shows Admin nav; non-admin hides it

---

## 6b43aaed
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-26T02:26:09Z
- **SHA:** 6b43aaed10f937f57fa732168ae739c1001231cf

### Commit Message
```
refactor(web): extract SideNav helpers and useNavAuthState hook (#1935)

## Summary

PR 1 of 3 in the SideNav refactor series. Carves the smallest standalone
unit out of `SideNav.tsx` (876 → 504 lines) into a new
`components/sidenav/` module and collapses two duplicate auth-listener
pairs into a single hook.

**Spec**:
[`docs/superpowers/specs/2026-05-25-issue-368-f11-sidenav-refactor.md`](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/refactor-sidebar/docs/superpowers/specs/2026-05-25-issue-368-f11-sidenav-refactor.md)
**Tracking**: #1926 (umbrella issue #368 F11)

### Changes

- Extracted `NavItemComponent`, `LoginButton`, `UserInfoSection` into
`web/app/src/components/sidenav/`.
- Added `useNavAuthState(pathname)` as the single owner of `isMounted` /
`userLoggedIn` / `userInfo` / `photoURL` / `subscriptionInfo` /
`hasClickedHire`. Merges the `auth-state-changed` + `storage` listener
pair that previously lived in both the main `SideNav` component and the
collapsed-mode `UserInfoSection`.
- `UserInfoSection` now reads `userInfo` / `photoURL` from props so both
consumers update from **one** subscription rather than two — eliminates
a state-skew window where the collapsed avatar fallback could flicker
during cross-tab logout.
- Swapped `innerHTML` assignment on the avatar fallback for
`textContent` (semantically equivalent for a single character, CSP/lint
friendlier).
- Hoisted the nested-ternary plan-label resolution into a module-scoped
`resolvePlanLabel` helper to keep `UserInfoSection` within the existing
complexity-25 budget.
- New `components/sidenav/types.ts` (`NavItem`, `NavItemComponentProps`)
and `constants.ts` (`NAV_ITEM_*_CLASSES`).

### Out of scope for this PR (will land in PR 2 / PR 3)

- Logo + agent-list regions and `useAgentScrollOverlay` /
`useBottomNavItems` hooks → PR 2.
- Bottom-nav + user-section split, `PLAN_PRICES` move to `constants.ts`,
and the `git mv` of `SideNav.tsx` into `sidenav/` → PR 3.

### File layout after this PR

```
web/app/src/components/sidenav/
  LoginButton.tsx
  NavItemComponent.tsx
  UserInfoSection.tsx
  constants.ts
  types.ts
  hooks/
    useNavAuthState.ts
```

## Test plan

- [x] `pnpm exec tsc --noEmit` → 0 errors
- [x] `pnpm lint` → 0 errors / 0 warnings
- [x] `pnpm test:unit` → 5749 passed / 1 todo (375 files); 28 new tests
in PR 1
- [x] `pnpm dup:src` → 3.77% (< 4.5% threshold)
- [x] `pnpm dup:tests` → 6.16% (< 7.0% threshold)
- [x] `pnpm lint:ci` (import-boundaries + knip + shrink-only gates) →
all pass

### Staging manual smoke (post-merge, before PR 2 opens)

- [ ] Desktop expanded + logged-in: `/chat` → switch `agent_id` → click
Zoo Square / Schedule / User Guide (new tab →
`https://zooclaw.ai/tips/{locale}/`)
- [ ] Desktop collapsed + logged-in: avatar fallback char + credits
tooltip on hover
- [ ] Desktop collapsed + logged-out: login icon + tooltip + modal opens
- [ ] Mobile (< 768px) + hamburger: SideNav slides in, nav click closes
menu
- [ ] admin account shows Admin nav; non-admin hides it
- [ ] trial plan → "X days left"; pro plan → "Pro" label
- [ ] **Cross-tab sync**: log out in tab A → tab B switches to
LoginButton without manual refresh (the listener-merge change is most
observable here)
```

### PR #1935: refactor(web): extract SideNav helpers and useNavAuthState hook

**PR Description:**
## Summary

PR 1 of 3 in the SideNav refactor series. Carves the smallest standalone unit out of `SideNav.tsx` (876 → 504 lines) into a new `components/sidenav/` module and collapses two duplicate auth-listener pairs into a single hook.

**Spec**: [`docs/superpowers/specs/2026-05-25-issue-368-f11-sidenav-refactor.md`](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/refactor-sidebar/docs/superpowers/specs/2026-05-25-issue-368-f11-sidenav-refactor.md)
**Tracking**: #1926 (umbrella issue #368 F11)

### Changes

- Extracted `NavItemComponent`, `LoginButton`, `UserInfoSection` into `web/app/src/components/sidenav/`.
- Added `useNavAuthState(pathname)` as the single owner of `isMounted` / `userLoggedIn` / `userInfo` / `photoURL` / `subscriptionInfo` / `hasClickedHire`. Merges the `auth-state-changed` + `storage` listener pair that previously lived in both the main `SideNav` component and the collapsed-mode `UserInfoSection`.
- `UserInfoSection` now reads `userInfo` / `photoURL` from props so both consumers update from **one** subscription rather than two — eliminates a state-skew window where the collapsed avatar fallback could flicker during cross-tab logout.
- Swapped `innerHTML` assignment on the avatar fallback for `textContent` (semantically equivalent for a single character, CSP/lint friendlier).
- Hoisted the nested-ternary plan-label resolution into a module-scoped `resolvePlanLabel` helper to keep `UserInfoSection` within the existing complexity-25 budget.
- New `components/sidenav/types.ts` (`NavItem`, `NavItemComponentProps`) and `constants.ts` (`NAV_ITEM_*_CLASSES`).

### Out of scope for this PR (will land in PR 2 / PR 3)

- Logo + agent-list regions and `useAgentScrollOverlay` / `useBottomNavItems` hooks → PR 2.
- Bottom-nav + user-section split, `PLAN_PRICES` move to `constants.ts`, and the `git mv` of `SideNav.tsx` into `sidenav/` → PR 3.

### File layout after this PR

```
web/app/src/components/sidenav/
  LoginButton.tsx
  NavItemComponent.tsx
  UserInfoSection.tsx
  constants.ts
  types.ts
  hooks/
    useNavAuthState.ts
```

## Test plan

- [x] `pnpm exec tsc --noEmit` → 0 errors
- [x] `pnpm lint` → 0 errors / 0 warnings
- [x] `pnpm test:unit` → 5749 passed / 1 todo (375 files); 28 new tests in PR 1
- [x] `pnpm dup:src` → 3.77% (< 4.5% threshold)
- [x] `pnpm dup:tests` → 6.16% (< 7.0% threshold)
- [x] `pnpm lint:ci` (import-boundaries + knip + shrink-only gates) → all pass

### Staging manual smoke (post-merge, before PR 2 opens)

- [ ] Desktop expanded + logged-in: `/chat` → switch `agent_id` → click Zoo Square / Schedule / User Guide (new tab → `https://zooclaw.ai/tips/{locale}/`)
- [ ] Desktop collapsed + logged-in: avatar fallback char + credits tooltip on hover
- [ ] Desktop collapsed + logged-out: login icon + tooltip + modal opens
- [ ] Mobile (< 768px) + hamburger: SideNav slides in, nav click closes menu
- [ ] admin account shows Admin nav; non-admin hides it
- [ ] trial plan → "X days left"; pro plan → "Pro" label
- [ ] **Cross-tab sync**: log out in tab A → tab B switches to LoginButton without manual refresh (the listener-merge change is most observable here)

---
