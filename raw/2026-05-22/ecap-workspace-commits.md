# ecap-workspace — 2026-05-22

共 19 条 commits

---

## 8c4c3be8 fix: gate billing migration by marker

- **SHA**: 8c4c3be8cc07a05e273a8756c3e259f9a1e386a0

- **Author**: kaka-srp

- **Date**: 2026-05-22T16:19:10Z


### Full Commit Message
```
fix: gate billing migration by marker
```

---

## ecc37ad0 feat(web): browser memory monitor + chat leak fixes (ECA-450) (#1858)

- **SHA**: ecc37ad04d025fffb998302b149b484eb80396b5

- **Author**: Chris@ZooClaw

- **Date**: 2026-05-22T16:08:11Z

- **PR**: #1858


### Full Commit Message
```
feat(web): browser memory monitor + chat leak fixes (ECA-450) (#1858)

## Summary

解决用户反馈的“网页长时间（小时～天级）打开后逐渐变卡 / 卡死”问题。监控 + Top 3 高危泄漏修复同一 PR
交付，因为监控是验证修复是否真正起效的 baseline。

Linear: https://linear.app/srpone/issue/ECA-450/web-版内存泄漏长时间不关页面内存几乎占满

### Monitoring（新增）

- `lib/sentry/memory-monitor.ts` — `performance.memory` 采样 + Sentry
上报。fingerprint 第 0 段编码 severity + route，以匹配 `sentry.client.config.ts`
的限频 key。
- `hooks/useMemoryMonitor.ts` — 30s 周期采样，`visibilityState !== 'visible'`
时跳过；阈值：high >=80%、critical >=90%、sustained_growth = 5 个连续样本单调递增且总涨幅
>=50MB。Chromium-only，其他浏览器静默 no-op。
- 在 `ClientLayout` 中与 `usePageTracking()` 同位置挂载。

不接 GA4、不开 `/api/metrics/memory`、不切 `measureUserAgentSpecificMemory()`（需
COOP/COEP，会影响 GA4 / Reddit Pixel / MM 嵌入）。

### Leak fixes（Top 3）

1. **`lib/mattermost/websocket.ts`** — `disconnect()` 末尾清空 4 个 handler
Set（`handlers` / `disconnectHandlers` / `helloHandlers` /
`activityHandlers`），同时保留 `notify:true` 在真实浏览器 async `onclose` 下的通知契约。
2. **chat typewriter** — 修复 bot message typewriter 的 long-session state
泄漏和 WS re-render 重启动画问题。原始实现位于 `useMattermostIntegration.ts`；合入最新 `main`
后，该中间层已被拆除，当前实现落在 `chat/hooks/useMmTypewriter.ts`：`streamingContents` /
`charIndexRef` / `fullTextRef` / `activeTimerRef` 分离，并在 id 离开
`recentBotMessageIds` 时显式 evict。
3. **`hooks/useOpenClawWebSocket.ts`** — 审计 3 个 `onEvent`
消费者（`useSubagentSessions`、`useSubagentChat` x2），全部正确从 useEffect 返回
`unsubscribe`；新增 dev-only handler count warning，防未来回归。

剩下 7 个 MED/LOW 候选（`useMmAttachments` upload
controllers、`useMattermost.postStore` 无界增长、`useLandingContextFlow`
轮询、`reactionsByPostId` 等）等监控上线后用真实数据决定下一波。

## Review-driven fixes

- 修复 Sentry fingerprint 与限频器 key 不兼容的问题：severity + route 编码进
`fingerprint[0]`，避免 high 告警压住后续 critical 告警。
- 修复 `disconnect()` 清空 handler Set 后真实浏览器 async `onclose`
无法通知的问题：snapshot disconnect handlers，同步 fire snapshot，并用
`notifyDisconnectHandlers=false` 静默后续 async path。
- 新增 `useMemoryMonitor` hook-level 测试，覆盖 threshold、dedup、visibility
hidden、sustained growth、unmount cleanup。
- 修复 typewriter 在 `mm.messages` 每次 WS 事件重建时重置 `charIndex=0`
的问题，并新增“不重启”和“离开 recent window 后 evict”回归测试。
- 修复 `useMemoryMonitor` hook 内只按 `reason` 去重导致 route 切换期间同一高压 streak 被错误
suppress 的问题；dedupe key 现在包含 severity + reason + route，并新增 route-change
回归测试。

## Merge conflict resolution

合入最新 `main` 后，`useMattermostIntegration.ts` /
`useMattermostIntegration.unit.spec.ts` 已由 `#1857` 删除并拆成
`useChatMessaging`、`useMmChannelSync`、`useMmTypewriter`。本 PR 的
typewriter leak/restart 修复已迁移到 `useMmTypewriter.ts` 和对应单测，没有恢复旧中间层。

## Test plan

- [x] `pnpm --dir web/app run lint`
- [x] `pnpm --dir web exec tsc --noEmit --project app/tsconfig.json`
- [x] `pnpm --dir web/app exec vitest run
tests/unit/hooks/useMemoryMonitor.unit.spec.ts
tests/unit/lib/sentry/memory-monitor.unit.spec.ts`
- [x] `pnpm --dir web/app exec vitest run
tests/unit/hooks/useMmTypewriter.unit.spec.ts
tests/unit/hooks/useMmChannelSync.unit.spec.ts`
- [x] `pnpm --dir web/app exec vitest run
tests/unit/hooks/useMmTypewriter.unit.spec.ts
tests/unit/hooks/useMmChannelSync.unit.spec.ts
tests/unit/app/chat/useChatMessaging.unit.spec.ts`
- [x] Prior full PR validation before merge conflict resolution: `pnpm
test:unit` 5633 tests passed.
- [ ] 本地手测监控：DevTools console 模拟堆增长，30s 内应触发 Sentry warning，severity
随增长升级 high -> critical。
- [ ] 本地手测 Leak 1：MM 反复 reconnect，Heap snapshot 看
`MattermostWebSocketService` handler Set 不再累积。
- [ ] 本地手测 Leak 2：长会话快速发 bot 消息 50+ 条，DevTools Memory tab 看 typewriter
state 随消息完成 / eviction 下降。
- [ ] 上线 1 周后查 Sentry `monitor:memory` 标签：(a) 上报频次合理（不是每分钟刷屏也不是 0 条）(b)
`usagePercent` 中位数 + `sessionAgeMs` 长尾与卡死报告对得上 (c) 关联 Session Replay
能复现卡顿。

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```


### PR Body
## Summary

解决用户反馈的“网页长时间（小时～天级）打开后逐渐变卡 / 卡死”问题。监控 + Top 3 高危泄漏修复同一 PR 交付，因为监控是验证修复是否真正起效的 baseline。

Linear: https://linear.app/srpone/issue/ECA-450/web-版内存泄漏长时间不关页面内存几乎占满

### Monitoring（新增）

- `lib/sentry/memory-monitor.ts` — `performance.memory` 采样 + Sentry 上报。fingerprint 第 0 段编码 severity + route，以匹配 `sentry.client.config.ts` 的限频 key。
- `hooks/useMemoryMonitor.ts` — 30s 周期采样，`visibilityState !== 'visible'` 时跳过；阈值：high >=80%、critical >=90%、sustained_growth = 5 个连续样本单调递增且总涨幅 >=50MB。Chromium-only，其他浏览器静默 no-op。
- 在 `ClientLayout` 中与 `usePageTracking()` 同位置挂载。

不接 GA4、不开 `/api/metrics/memory`、不切 `measureUserAgentSpecificMemory()`（需 COOP/COEP，会影响 GA4 / Reddit Pixel / MM 嵌入）。

### Leak fixes（Top 3）

1. **`lib/mattermost/websocket.ts`** — `disconnect()` 末尾清空 4 个 handler Set（`handlers` / `disconnectHandlers` / `helloHandlers` / `activityHandlers`），同时保留 `notify:true` 在真实浏览器 async `onclose` 下的通知契约。
2. **chat typewriter** — 修复 bot message typewriter 的 long-session state 泄漏和 WS re-render 重启动画问题。原始实现位于 `useMattermostIntegration.ts`；合入最新 `main` 后，该中间层已被拆除，当前实现落在 `chat/hooks/useMmTypewriter.ts`：`streamingContents` / `charIndexRef` / `fullTextRef` / `activeTimerRef` 分离，并在 id 离开 `recentBotMessageIds` 时显式 evict。
3. **`hooks/useOpenClawWebSocket.ts`** — 审计 3 个 `onEvent` 消费者（`useSubagentSessions`、`useSubagentChat` x2），全部正确从 useEffect 返回 `unsubscribe`；新增 dev-only handler count warning，防未来回归。

剩下 7 个 MED/LOW 候选（`useMmAttachments` upload controllers、`useMattermost.postStore` 无界增长、`useLandingContextFlow` 轮询、`reactionsByPostId` 等）等监控上线后用真实数据决定下一波。

## Review-driven fixes

- 修复 Sentry fingerprint 与限频器 key 不兼容的问题：severity + route 编码进 `fingerprint[0]`，避免 high 告警压住后续 critical 告警。
- 修复 `disconnect()` 清空 handler Set 后真实浏览器 async `onclose` 无法通知的问题：snapshot disconnect handlers，同步 fire snapshot，并用 `notifyDisconnectHandlers=false` 静默后续 async path。
- 新增 `useMemoryMonitor` hook-level 测试，覆盖 threshold、dedup、visibility hidden、sustained growth、unmount cleanup。
- 修复 typewriter 在 `mm.messages` 每次 WS 事件重建时重置 `charIndex=0` 的问题，并新增“不重启”和“离开 recent window 后 evict”回归测试。
- 修复 `useMemoryMonitor` hook 内只按 `reason` 去重导致 route 切换期间同一高压 streak 被错误 suppress 的问题；dedupe key 现在包含 severity + reason + route，并新增 route-change 回归测试。

## Merge conflict resolution

合入最新 `main` 后，`useMattermostIntegration.ts` / `useMattermostIntegration.unit.spec.ts` 已由 `#1857` 删除并拆成 `useChatMessaging`、`useMmChannelSync`、`useMmTypewriter`。本 PR 的 typewriter leak/restart 修复已迁移到 `useMmTypewriter.ts` 和对应单测，没有恢复旧中间层。

## Test plan

- [x] `pnpm --dir web/app run lint`
- [x] `pnpm --dir web exec tsc --noEmit --project app/tsconfig.json`
- [x] `pnpm --dir web/app exec vitest run tests/unit/hooks/useMemoryMonitor.unit.spec.ts tests/unit/lib/sentry/memory-monitor.unit.spec.ts`
- [x] `pnpm --dir web/app exec vitest run tests/unit/hooks/useMmTypewriter.unit.spec.ts tests/unit/hooks/useMmChannelSync.unit.spec.ts`
- [x] `pnpm --dir web/app exec vitest run tests/unit/hooks/useMmTypewriter.unit.spec.ts tests/unit/hooks/useMmChannelSync.unit.spec.ts tests/unit/app/chat/useChatMessaging.unit.spec.ts`
- [x] Prior full PR validation before merge conflict resolution: `pnpm test:unit` 5633 tests passed.
- [ ] 本地手测监控：DevTools console 模拟堆增长，30s 内应触发 Sentry warning，severity 随增长升级 high -> critical。
- [ ] 本地手测 Leak 1：MM 反复 reconnect，Heap snapshot 看 `MattermostWebSocketService` handler Set 不再累积。
- [ ] 本地手测 Leak 2：长会话快速发 bot 消息 50+ 条，DevTools Memory tab 看 typewriter state 随消息完成 / eviction 下降。
- [ ] 上线 1 周后查 Sentry `monitor:memory` 标签：(a) 上报频次合理（不是每分钟刷屏也不是 0 条）(b) `usagePercent` 中位数 + `sessionAgeMs` 长尾与卡死报告对得上 (c) 关联 Session Replay 能复现卡顿。


---

## 612a77f4 refactor(chat): delete useMattermostIntegration middle layer + extract 2 hooks + remove all 4 exhaustive-deps disables (#1711 step 2/2) (#1857)

- **SHA**: 612a77f43cb4d67e18c0fe84e6092e01bdbd4031

- **Author**: Chris@ZooClaw

- **Date**: 2026-05-22T14:25:04Z

- **PR**: #1857


### Full Commit Message
```
refactor(chat): delete useMattermostIntegration middle layer + extract 2 hooks + remove all 4 exhaustive-deps disables (#1711 step 2/2) (#1857)

**Closes #1711.** Step 2/2 of the F-bucket residual from epic #1526.

## What changes

- **Delete `useMattermostIntegration.ts`**. `useChatMessaging` was the
sole caller and now consumes the focused hooks directly while keeping
the same caller-facing return shape.
- **Extract `useMmTypewriter`** for streaming buffer state and
`mmDisplayMessages` derivation. The typewriter buffer is state-backed,
so the memo dependencies are reactive without `streamingTick`.
- **Extract `useMmChannelSync`** for Mattermost channel alignment. Agent
switches select the already-resolved `activeAgentChannelId`;
unchanged-agent channel drift still uses the 500ms correction debounce.
- **All 4 `react-hooks/exhaustive-deps` disables removed** from the
Mattermost chat path.
- **`useEffect` count in the chat MM path drops 3 to 2**: typewriter
plus merged channel sync. The `mm.error` toast effect is unchanged.

## Caller impact

`ChatBody` / `GenClawInput` / `OpenClawThread` see zero API changes.
`useChatMessaging` still returns the same shape, including a reassembled
`mm` object for callers that destructure `mm.*`.

## Review-driven fixes

- Fixed the `agentId="main"` channel-switch edge case by making
`useMmChannelSync` consume the caller-resolved `activeAgentChannelId`
instead of re-deriving bot/channel mapping internally.
- Restored missing-channel recovery for main-agent switch-back paths:
when an agent switch has no resolved `activeAgentChannelId`,
`useMmChannelSync` now calls `refreshBots()` instead of silently falling
through.
- Added regression coverage for both main-agent representations
(`agentId=null` and `agentId="main"`) when the main channel is not yet
resolved.
- Restored explicit `/stop` slash-command regression coverage proving
`consumeAttachments: false` preserves staged attachment state and does
not call `clearMmAttachments()`.
- Verified the callback-dependency concern separately: `selectChannel`
is stable via `useStableCallback`, and `refreshBots` is stable via
`useCallback`, so no extra production change is needed there.
- Opened follow-up issue #1862 for the broader canonicalization of
`/chat?agent_id=main` to the main-agent URL state.

## Test changes

- Delete `tests/unit/app/chat/useMattermostIntegration.unit.spec.ts` +
`tests/unit/hooks/useMattermostIntegration.unit.spec.ts`.
- Add `tests/unit/hooks/useMmTypewriter.unit.spec.ts` for props mapping,
reactions, and streaming gating.
- Add/update `tests/unit/hooks/useMmChannelSync.unit.spec.ts` for agent
switch, main-agent switch, missing-channel refresh fallback, debounce,
and cancellation behavior.
- Rewrite `tests/unit/app/chat/useChatMessaging.unit.spec.ts` mocks to
stub `useMattermostContext` plus the extracted hooks, with `mmConnected`
derivation coverage and `/stop` attachment-preservation coverage.

## PR size

This remains slightly over the 2000-line budget because deleting the
middle layer and replacing it with focused hooks/tests counts as add
plus delete on near-renames. The `size-override` label is intentional.

Refs: #1711, #1862, [[project-react-hooks-1526-done]] F bucket. Builds
on #1854.

## Test plan

- [x] `pnpm -C web/app exec vitest run
tests/unit/hooks/useMmChannelSync.unit.spec.ts
tests/unit/hooks/useMmTypewriter.unit.spec.ts
tests/unit/app/chat/useChatMessaging.unit.spec.ts` — 41 / 41 passed
- [x] `pnpm -C web/app run lint` — passes
- [x] `pnpm -C web/app exec tsc --noEmit` — passes
- [ ] Manual smoke (recommended before merge): upload attachment / agent
switch / channel drift recovery / typewriter streaming + edit-mode flip
/ disconnect and reconnect

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```


### PR Body
**Closes #1711.** Step 2/2 of the F-bucket residual from epic #1526.

## What changes

- **Delete `useMattermostIntegration.ts`**. `useChatMessaging` was the sole caller and now consumes the focused hooks directly while keeping the same caller-facing return shape.
- **Extract `useMmTypewriter`** for streaming buffer state and `mmDisplayMessages` derivation. The typewriter buffer is state-backed, so the memo dependencies are reactive without `streamingTick`.
- **Extract `useMmChannelSync`** for Mattermost channel alignment. Agent switches select the already-resolved `activeAgentChannelId`; unchanged-agent channel drift still uses the 500ms correction debounce.
- **All 4 `react-hooks/exhaustive-deps` disables removed** from the Mattermost chat path.
- **`useEffect` count in the chat MM path drops 3 to 2**: typewriter plus merged channel sync. The `mm.error` toast effect is unchanged.

## Caller impact

`ChatBody` / `GenClawInput` / `OpenClawThread` see zero API changes. `useChatMessaging` still returns the same shape, including a reassembled `mm` object for callers that destructure `mm.*`.

## Review-driven fixes

- Fixed the `agentId="main"` channel-switch edge case by making `useMmChannelSync` consume the caller-resolved `activeAgentChannelId` instead of re-deriving bot/channel mapping internally.
- Restored missing-channel recovery for main-agent switch-back paths: when an agent switch has no resolved `activeAgentChannelId`, `useMmChannelSync` now calls `refreshBots()` instead of silently falling through.
- Added regression coverage for both main-agent representations (`agentId=null` and `agentId="main"`) when the main channel is not yet resolved.
- Restored explicit `/stop` slash-command regression coverage proving `consumeAttachments: false` preserves staged attachment state and does not call `clearMmAttachments()`.
- Verified the callback-dependency concern separately: `selectChannel` is stable via `useStableCallback`, and `refreshBots` is stable via `useCallback`, so no extra production change is needed there.
- Opened follow-up issue #1862 for the broader canonicalization of `/chat?agent_id=main` to the main-agent URL state.

## Test changes

- Delete `tests/unit/app/chat/useMattermostIntegration.unit.spec.ts` + `tests/unit/hooks/useMattermostIntegration.unit.spec.ts`.
- Add `tests/unit/hooks/useMmTypewriter.unit.spec.ts` for props mapping, reactions, and streaming gating.
- Add/update `tests/unit/hooks/useMmChannelSync.unit.spec.ts` for agent switch, main-agent switch, missing-channel refresh fallback, debounce, and cancellation behavior.
- Rewrite `tests/unit/app/chat/useChatMessaging.unit.spec.ts` mocks to stub `useMattermostContext` plus the extracted hooks, with `mmConnected` derivation coverage and `/stop` attachment-preservation coverage.

## PR size

This remains slightly over the 2000-line budget because deleting the middle layer and replacing it with focused hooks/tests counts as add plus delete on near-renames. The `size-override` label is intentional.

Refs: #1711, #1862, [[project-react-hooks-1526-done]] F bucket. Builds on #1854.

## Test plan

- [x] `pnpm -C web/app exec vitest run tests/unit/hooks/useMmChannelSync.unit.spec.ts tests/unit/hooks/useMmTypewriter.unit.spec.ts tests/unit/app/chat/useChatMessaging.unit.spec.ts` — 41 / 41 passed
- [x] `pnpm -C web/app run lint` — passes
- [x] `pnpm -C web/app exec tsc --noEmit` — passes
- [ ] Manual smoke (recommended before merge): upload attachment / agent switch / channel drift recovery / typewriter streaming + edit-mode flip / disconnect and reconnect


---

## 2e388e71 fix(web): scope onboarding status by user (#1860)

- **SHA**: 2e388e717c16c6e4b39101707adead53d261d22c

- **Author**: Chris@ZooClaw

- **Date**: 2026-05-22T13:46:47Z

- **PR**: #1860


### Full Commit Message
```
fix(web): scope onboarding status by user (#1860)

## Summary
- Scope cached onboarding backend status snapshots by uid so login-time
status events survive auth uid transitions.
- Filter stale onboarding snapshots in OnboardingProvider instead of
clearing the shared cache on every uid change.
- Add regression coverage for the ECA-800 login/onboarding race and
phone verify duplicate-click behavior.

## Linear

https://linear.app/srpone/issue/ECA-800/bug-手机验证码登录后重复出现验证码输入框并进入-unable-to-connect-页面

## Tests
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir
web/app exec vitest run tests/unit/lib/auth/manager.unit.spec.ts
tests/unit/components/providers/OnboardingProvider.unit.spec.tsx
tests/unit/app/user-verify-phone.unit.spec.tsx
tests/unit/components/LoginForm.unit.spec.tsx --config
./vitest.config.mts`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir
web/app exec tsc --noEmit --project app/tsconfig.json`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir
web/app run lint`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir
web/app run test:unit`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir
web run lint`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir
web run test:unit`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir
web/enterprise-admin exec tsc --noEmit`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir
web/packages/auth-client exec tsc --noEmit`

Note: `pnpm --dir web run tsc` currently exits before typechecking with
pnpm `Unknown option: if-present`; package-level tsc checks above were
used as the workaround.
```


### PR Body
## Summary
- Scope cached onboarding backend status snapshots by uid so login-time status events survive auth uid transitions.
- Filter stale onboarding snapshots in OnboardingProvider instead of clearing the shared cache on every uid change.
- Add regression coverage for the ECA-800 login/onboarding race and phone verify duplicate-click behavior.

## Linear
https://linear.app/srpone/issue/ECA-800/bug-手机验证码登录后重复出现验证码输入框并进入-unable-to-connect-页面

## Tests
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir web/app exec vitest run tests/unit/lib/auth/manager.unit.spec.ts tests/unit/components/providers/OnboardingProvider.unit.spec.tsx tests/unit/app/user-verify-phone.unit.spec.tsx tests/unit/components/LoginForm.unit.spec.tsx --config ./vitest.config.mts`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir web/app exec tsc --noEmit --project app/tsconfig.json`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir web/app run lint`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir web/app run test:unit`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir web run lint`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir web run test:unit`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir web/enterprise-admin exec tsc --noEmit`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir web/packages/auth-client exec tsc --noEmit`

Note: `pnpm --dir web run tsc` currently exits before typechecking with pnpm `Unknown option: if-present`; package-level tsc checks above were used as the workaround.


---

## 35fb3f8c refactor(chat): extract useMmAttachments from useMattermostIntegration (#1711 step 1/2) (#1854)

- **SHA**: 35fb3f8c483410fbea695bdc6c8b99559e11bb88

- **Author**: Chris@ZooClaw

- **Date**: 2026-05-22T12:14:04Z

- **PR**: #1854


### Full Commit Message
```
refactor(chat): extract useMmAttachments from useMattermostIntegration (#1711 step 1/2) (#1854)

## Summary

Step 1 of 2 for #1711 — pure extraction with zero behavior change.

- Move the upload-management section of `useMattermostIntegration` (5
callbacks + 4 refs + `mmAttachments` state + 2 module-level helpers)
into a new `useMmAttachments` hook with an explicit `{ agentId,
apiService, activeChannelId, serverURL, token }` input contract.
- Main hook now consumes `useMmAttachments` internally and re-exports
the same fields, so all callers (`useChatMessaging` / `ChatBody` /
`GenClawInput`) see an unchanged public API.
- Upload-related unit tests (16 tests across mmUploadFiles /
onRemoveMmAttachment / concurrent guard / retryMmAttachment / failReason
classification) move to `tests/unit/hooks/useMmAttachments.unit.spec.ts`
and now exercise `useMmAttachments` directly via `renderHook` with
explicit param values — no `useMattermostContext` mock.

Step 2 (separate PR, opened after this merges) will extract
`useMmTypewriter` + `useMmChannelSync`, **delete the
`useMattermostIntegration` middle layer entirely**, and consolidate the
channel-alignment + agent-switch effects into a single useEffect — at
which point all 4 `react-hooks/exhaustive-deps` disables in the file go
away, and the chat MM `useEffect` count drops from 3 → 2. This PR is
purely structural — no `disable` removed yet.

Refs: #1711, [[project-react-hooks-1526-done]] F bucket residual.

## Test plan

- [x] `pnpm tsc --noEmit` — passes
- [x] `pnpm lint` — passes
- [x] `pnpm test:unit` — 5613 / 5613 passed (1 todo unchanged)
- [x] 4 shrink-only guards — all unchanged (filename / forbid-dom-props
/ no-raw-fetch / svg-inline)
- [ ] Manual smoke (deferred to step 2 along with disable removal):
upload image / non-image / HEIC / retry path — public API is identical
so the existing test surface should be sufficient signal

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```


### PR Body
## Summary

Step 1 of 2 for #1711 — pure extraction with zero behavior change.

- Move the upload-management section of `useMattermostIntegration` (5 callbacks + 4 refs + `mmAttachments` state + 2 module-level helpers) into a new `useMmAttachments` hook with an explicit `{ agentId, apiService, activeChannelId, serverURL, token }` input contract.
- Main hook now consumes `useMmAttachments` internally and re-exports the same fields, so all callers (`useChatMessaging` / `ChatBody` / `GenClawInput`) see an unchanged public API.
- Upload-related unit tests (16 tests across mmUploadFiles / onRemoveMmAttachment / concurrent guard / retryMmAttachment / failReason classification) move to `tests/unit/hooks/useMmAttachments.unit.spec.ts` and now exercise `useMmAttachments` directly via `renderHook` with explicit param values — no `useMattermostContext` mock.

Step 2 (separate PR, opened after this merges) will extract `useMmTypewriter` + `useMmChannelSync`, **delete the `useMattermostIntegration` middle layer entirely**, and consolidate the channel-alignment + agent-switch effects into a single useEffect — at which point all 4 `react-hooks/exhaustive-deps` disables in the file go away, and the chat MM `useEffect` count drops from 3 → 2. This PR is purely structural — no `disable` removed yet.

Refs: #1711, [[project-react-hooks-1526-done]] F bucket residual.

## Test plan

- [x] `pnpm tsc --noEmit` — passes
- [x] `pnpm lint` — passes
- [x] `pnpm test:unit` — 5613 / 5613 passed (1 todo unchanged)
- [x] 4 shrink-only guards — all unchanged (filename / forbid-dom-props / no-raw-fetch / svg-inline)
- [ ] Manual smoke (deferred to step 2 along with disable removal): upload image / non-image / HEIC / retry path — public API is identical so the existing test surface should be sufficient signal

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## e66a880b docs(spec): RichTextInput migration to TipTap design spec (ECA-802) (#1855)

- **SHA**: e66a880b7317603acbc59dd3b4f8d8aca81b094c

- **Author**: Chris@ZooClaw

- **Date**: 2026-05-22T12:08:16Z

- **PR**: #1855


### Full Commit Message
```
docs(spec): RichTextInput migration to TipTap design spec (ECA-802) (#1855)

## Summary

Design spec for migrating `web/app/src/components/RichTextInput.tsx`
(838 行 controlled contentEditable) to **TipTap (ProseMirror + React)**.
起源是 GitHub issue #1686 (epic #1526 react-hooks/exhaustive-deps 治理的 leaf
follow-up),经过四轮方案推翻,最终决策为整体迁移。

**当前状态: Design approved, 暂不实施**,等待 priority 评估。后续实施工作通过 Linear epic 跟踪:

🔗 [ECA-802 — [Epic] RichTextInput 迁移到 TipTap
(ProseMirror)](https://linear.app/srpone/issue/ECA-802/epic-richtextinput-迁移到-tiptap-prosemirror)

GitHub issue #1686 已 close (supersede)。

## 四轮决策演进(spec 含完整 archeology)

1. ❌ **Hoist + helper 改签 (~40 行)** — 治标不治本
2. ❌ **Lexical 整体迁移 (12 PR)** — `@assistant-ui/react` 已是 dep,Lexical
是再造轮子
3. ❌ **assistant-ui ComposerPrimitive (5 PR / ~0KB)** — thumbnail bar UX
不支持未来富文本扩展
4. ✅ **TipTap (11 PR / +76KB)** — 行业标杆 (Claude.ai / ChatGPT / Notion
等),兼顾 inline chip + 富文本扩展未来

## Spec 涵盖

- 当前 838 行 RichTextInput 完整功能 inventory(14 props / 7 paste 分支 / 3 chip
三态 / 4 caller)
- TipTap 设计要点(extension 按需注册,atom node,自写 markdown 双向,InputRule)
- 11 PR 拆分(Phase 1 foundation 3 / Phase 2 behavior parity 4 / Phase 3
switchover 4 含 sunset 同轮)
- 切换机制 (URL `?richtext=v2` query param flag)
- 风险 & 缓解 (PM 学习曲线 / Bundle 限额 / IME 差异 / round-trip byte-equality)
- 验证策略 (22+ 老 spec 复用 + 新 unit + 新 e2e)

## 启动条件 (任一满足重新评估)

- 富文本编辑产品需求 surface (@mention / slash commands / bold-italic)
- 团队带宽允许 11 PR 系列投入
- TipTap / Lexical 生态重要更新影响选型

启动后第一步:PR 1 起手前做 50 行 spike (`editorProps.handlePaste` × PM transaction
可行性);失败可回退到 Lexical 方案。

## Test plan

Docs-only PR, 无需 functional testing:

- [ ] CI lint / spell check 通过
- [ ] Linear ECA-802 attachment 中的 spec doc URL
(`/blob/main/docs/superpowers/specs/...`) 在 merge 后可访问
- [ ] GitHub issue #1686 close comment 中的 spec doc URL 在 merge 后可访问

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```


### PR Body
## Summary

Design spec for migrating `web/app/src/components/RichTextInput.tsx` (838 行 controlled contentEditable) to **TipTap (ProseMirror + React)**. 起源是 GitHub issue #1686 (epic #1526 react-hooks/exhaustive-deps 治理的 leaf follow-up),经过四轮方案推翻,最终决策为整体迁移。

**当前状态: Design approved, 暂不实施**,等待 priority 评估。后续实施工作通过 Linear epic 跟踪:

🔗 [ECA-802 — [Epic] RichTextInput 迁移到 TipTap (ProseMirror)](https://linear.app/srpone/issue/ECA-802/epic-richtextinput-迁移到-tiptap-prosemirror)

GitHub issue #1686 已 close (supersede)。

## 四轮决策演进(spec 含完整 archeology)

1. ❌ **Hoist + helper 改签 (~40 行)** — 治标不治本
2. ❌ **Lexical 整体迁移 (12 PR)** — `@assistant-ui/react` 已是 dep,Lexical 是再造轮子
3. ❌ **assistant-ui ComposerPrimitive (5 PR / ~0KB)** — thumbnail bar UX 不支持未来富文本扩展
4. ✅ **TipTap (11 PR / +76KB)** — 行业标杆 (Claude.ai / ChatGPT / Notion 等),兼顾 inline chip + 富文本扩展未来

## Spec 涵盖

- 当前 838 行 RichTextInput 完整功能 inventory(14 props / 7 paste 分支 / 3 chip 三态 / 4 caller)
- TipTap 设计要点(extension 按需注册,atom node,自写 markdown 双向,InputRule)
- 11 PR 拆分(Phase 1 foundation 3 / Phase 2 behavior parity 4 / Phase 3 switchover 4 含 sunset 同轮)
- 切换机制 (URL `?richtext=v2` query param flag)
- 风险 & 缓解 (PM 学习曲线 / Bundle 限额 / IME 差异 / round-trip byte-equality)
- 验证策略 (22+ 老 spec 复用 + 新 unit + 新 e2e)

## 启动条件 (任一满足重新评估)

- 富文本编辑产品需求 surface (@mention / slash commands / bold-italic)
- 团队带宽允许 11 PR 系列投入
- TipTap / Lexical 生态重要更新影响选型

启动后第一步:PR 1 起手前做 50 行 spike (`editorProps.handlePaste` × PM transaction 可行性);失败可回退到 Lexical 方案。

## Test plan

Docs-only PR, 无需 functional testing:

- [ ] CI lint / spell check 通过
- [ ] Linear ECA-802 attachment 中的 spec doc URL (`/blob/main/docs/superpowers/specs/...`) 在 merge 后可访问
- [ ] GitHub issue #1686 close comment 中的 spec doc URL 在 merge 后可访问

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## c41cbef9 fix(chat): scope chat input draft by agent session (ECA-727) (#1853)

- **SHA**: c41cbef9b77919d1b57ce8cb4c6b0af93013e922

- **Author**: Chris@ZooClaw

- **Date**: 2026-05-22T11:27:31Z

- **PR**: #1853


### Full Commit Message
```
fix(chat): scope chat input draft by agent session (ECA-727) (#1853)

Linear:
https://linear.app/srpone/issue/ECA-727/web-切换-agent-时输入框内容被带到新-agent-会话

## Summary

The desktop chat composer persisted its draft keyed by `userId` only, so
a half-typed message under Agent A would resurface in Agent B's input
after switching — the message thread itself remounts cleanly on agent
boundary (`AssistantRuntimeProvider key={sessionKey}` in
`ChatBody.tsx`), but the composer kept reading from the same uid-only
`sessionStorage` slot.

Fix: rename the helper to
`STORAGE_KEYS.CHAT_INPUT_DRAFT_FOR_SESSION(uid, sessionId)` and feed in
the `sessionId` prop that was already wired into `GenClawInput` for
uploads / SSE. The existing `useEffect` watching `draftStorageKey`
re-reads `sessionStorage` whenever the key changes, so:

- Switching to a different Agent now shows that Agent's slot (empty or
its own prior draft).
- Switching back restores the original Agent's draft from its own slot.
- Same-Agent refresh / unmount / remount keeps the draft, as before.

No migration: stale uid-only `sessionStorage` entries from prior
versions are simply ignored (sessionStorage is per-tab anyway, so the
blast radius is "one draft lost on the first switch after deploy").

## Test plan

- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm test:unit tests/unit/app/chat/GenClawInput.unit.spec.tsx` —
51/51 pass
- [x] Falsifiability proof: reverted the storage helper to uid-only and
re-ran — both new regression tests fail with the expected leak messages
("legacy uid-only leak" and "main draft" appearing in input after
switch). Restored, tests green.

## Regression tests added

1. `ignores the pre-fix uid-only draft key shape so old leaked drafts
cannot resurface` — seeds the literal `ecap:chat:input-draft:user-1` key
(what pre-fix code wrote), renders with `sessionId='main'`, asserts
input is empty.
2. `swaps and restores the visible draft when sessionId changes between
agents` — types under `main`, switches to `agent:foo:main` (expects
empty), types under foo, switches back to `main` (expects original draft
restored), asserts both `sessionStorage` slots remain independently
populated.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```


### PR Body
Linear: https://linear.app/srpone/issue/ECA-727/web-切换-agent-时输入框内容被带到新-agent-会话

## Summary

The desktop chat composer persisted its draft keyed by `userId` only, so a half-typed message under Agent A would resurface in Agent B's input after switching — the message thread itself remounts cleanly on agent boundary (`AssistantRuntimeProvider key={sessionKey}` in `ChatBody.tsx`), but the composer kept reading from the same uid-only `sessionStorage` slot.

Fix: rename the helper to `STORAGE_KEYS.CHAT_INPUT_DRAFT_FOR_SESSION(uid, sessionId)` and feed in the `sessionId` prop that was already wired into `GenClawInput` for uploads / SSE. The existing `useEffect` watching `draftStorageKey` re-reads `sessionStorage` whenever the key changes, so:

- Switching to a different Agent now shows that Agent's slot (empty or its own prior draft).
- Switching back restores the original Agent's draft from its own slot.
- Same-Agent refresh / unmount / remount keeps the draft, as before.

No migration: stale uid-only `sessionStorage` entries from prior versions are simply ignored (sessionStorage is per-tab anyway, so the blast radius is "one draft lost on the first switch after deploy").

## Test plan

- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm test:unit tests/unit/app/chat/GenClawInput.unit.spec.tsx` — 51/51 pass
- [x] Falsifiability proof: reverted the storage helper to uid-only and re-ran — both new regression tests fail with the expected leak messages ("legacy uid-only leak" and "main draft" appearing in input after switch). Restored, tests green.

## Regression tests added

1. `ignores the pre-fix uid-only draft key shape so old leaked drafts cannot resurface` — seeds the literal `ecap:chat:input-draft:user-1` key (what pre-fix code wrote), renders with `sessionId='main'`, asserts input is empty.
2. `swaps and restores the visible draft when sessionId changes between agents` — types under `main`, switches to `agent:foo:main` (expects empty), types under foo, switches back to `main` (expects original draft restored), asserts both `sessionStorage` slots remain independently populated.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 147225df refactor(claw-interface): add warm-pool assets phase 1 foundation (#1849)

- **SHA**: 147225df1ed5e41cd43c520fbcd87ad21dcfaaa8

- **Author**: tim-srp

- **Date**: 2026-05-22T11:23:12Z

- **PR**: #1849


### Full Commit Message
```
refactor(claw-interface): add warm-pool assets phase 1 foundation (#1849)

## Summary
- add `ecap-warm-pool-assets` schema and repo foundation
- add shared base account payload builder for future claim
materialization
- add warm-pool-specific billing initialization entrypoint without
cutting existing traffic
- include warm-pool spec and implementation plan docs

## Scope
This PR is **Phase 1 / foundation only**.
It does **not** switch warm-pool provisioning or claim/finalize to the
new collection yet.

## Business impact
Expected business impact is minimal:
- no routing cutover
- no change to current warm-pool provisioning behavior
- no change to `/users/create` semantics yet

## Included
- `WARM_POOL_ASSETS_COLLECTION`
- `WarmPoolAssets` schema
- `warm_pool_assets_repo`
- `build_base_account_payload(...)`
- `ensure_billing_initialized_for_warm_pool(uid)` entrypoint
- focused unit tests
- spec + implementation plan docs

## Verification
- `pytest tests/unit/test_warm_pool_assets_repo.py
tests/unit/test_account_builder.py tests/unit/test_billing_warm_pool.py
-v`
- `ruff check app/database/collections.py app/schema/warm_pool_assets.py
app/database/warm_pool_assets_repo.py
app/services/user/account_builder.py app/services/billing.py
tests/unit/test_warm_pool_assets_repo.py
tests/unit/test_account_builder.py tests/unit/test_billing_warm_pool.py`
```


### PR Body
## Summary
- add `ecap-warm-pool-assets` schema and repo foundation
- add shared base account payload builder for future claim materialization
- add warm-pool-specific billing initialization entrypoint without cutting existing traffic
- include warm-pool spec and implementation plan docs

## Scope
This PR is **Phase 1 / foundation only**.
It does **not** switch warm-pool provisioning or claim/finalize to the new collection yet.

## Business impact
Expected business impact is minimal:
- no routing cutover
- no change to current warm-pool provisioning behavior
- no change to `/users/create` semantics yet

## Included
- `WARM_POOL_ASSETS_COLLECTION`
- `WarmPoolAssets` schema
- `warm_pool_assets_repo`
- `build_base_account_payload(...)`
- `ensure_billing_initialized_for_warm_pool(uid)` entrypoint
- focused unit tests
- spec + implementation plan docs

## Verification
- `pytest tests/unit/test_warm_pool_assets_repo.py tests/unit/test_account_builder.py tests/unit/test_billing_warm_pool.py -v`
- `ruff check app/database/collections.py app/schema/warm_pool_assets.py app/database/warm_pool_assets_repo.py app/services/user/account_builder.py app/services/billing.py tests/unit/test_warm_pool_assets_repo.py tests/unit/test_account_builder.py tests/unit/test_billing_warm_pool.py`


---

## 04691ec8 fix(web): guard sentry tracing in ios webviews (#1852)

- **SHA**: 04691ec8670a2fc2b23478d9c44756d37ac9fc55

- **Author**: bill-srp

- **Date**: 2026-05-22T11:10:45Z

- **PR**: #1852


### Full Commit Message
```
fix(web): guard sentry tracing in ios webviews (#1852)

## Summary
- Mitigate Sentry SDK startup crashes isolated to iOS WKWebView by
skipping fragile browser tracing/replay instrumentation there.
- Keep Sentry error reporting and HTTP client error capture enabled.
- Linear:
https://linear.app/srpone/issue/ECA-652/frontend-typeerror-weakmap-keys-must-be-objects-or-non-registered

## Root cause
Sentry ECAP-WEBSITE-PE events show TypeError: WeakMap keys must be
objects or non-registered symbols during Sentry client integration
setup, not app feature code. All sampled events are from Mobile Safari
UI/WKWebView, with the stack ending in WeakMap.set under Sentry.init ->
_setupIntegrations -> integration.setup.

## Test plan
- [x] pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/config/sentry-client-config.unit.spec.ts
- [x] pnpm --dir web/app exec tsc --noEmit --pretty false
- [x] pnpm --dir web -r --workspace-concurrency=1 exec tsc --noEmit
- [x] pnpm --dir web run test:unit
- [x] pnpm --dir web/app exec prettier --check sentry.client.config.ts
- [x] git diff --check -- web/app/sentry.client.config.ts
- [ ] pnpm --dir web run lint blocked before linting by existing
eslint-config-next/core-web-vitals config loading error: Unexpected
top-level property "name".
```


### PR Body
## Summary
- Mitigate Sentry SDK startup crashes isolated to iOS WKWebView by skipping fragile browser tracing/replay instrumentation there.
- Keep Sentry error reporting and HTTP client error capture enabled.
- Linear: https://linear.app/srpone/issue/ECA-652/frontend-typeerror-weakmap-keys-must-be-objects-or-non-registered

## Root cause
Sentry ECAP-WEBSITE-PE events show TypeError: WeakMap keys must be objects or non-registered symbols during Sentry client integration setup, not app feature code. All sampled events are from Mobile Safari UI/WKWebView, with the stack ending in WeakMap.set under Sentry.init -> _setupIntegrations -> integration.setup.

## Test plan
- [x] pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/config/sentry-client-config.unit.spec.ts
- [x] pnpm --dir web/app exec tsc --noEmit --pretty false
- [x] pnpm --dir web -r --workspace-concurrency=1 exec tsc --noEmit
- [x] pnpm --dir web run test:unit
- [x] pnpm --dir web/app exec prettier --check sentry.client.config.ts
- [x] git diff --check -- web/app/sentry.client.config.ts
- [ ] pnpm --dir web run lint blocked before linting by existing eslint-config-next/core-web-vitals config loading error: Unexpected top-level property "name".


---

## ebe289da chore(lint): fix pre-existing prettier + comment-as-disable-directive errors in eslint.config.mjs (#1851)

- **SHA**: ebe289da1f94c2db2148baa69c8dcdf3b93bddd0

- **Author**: Chris@ZooClaw

- **Date**: 2026-05-22T10:11:10Z

- **PR**: #1851


### Full Commit Message
```
chore(lint): fix pre-existing prettier + comment-as-disable-directive errors in eslint.config.mjs (#1851)

## Summary
- 修 `web/app/eslint.config.mjs` 25 个 pre-existing 错误（该文件不在常规 lint
glob，CI 不扫，但显式 `pnpm exec eslint eslint.config.mjs` 会报）。
- `eslint --fix` 自动清 23 个 prettier 错误（shrink-only 数组延续行 trailing
whitespace + 长 `no-restricted-syntax` selector 字符串 double→single quote
规范化）。
- 手动改 2 段 JS 注释（行 583-598 那个 `// Forbid inline style={{...}}` 块）：原文以
`eslint-disable-next-line` 作为 `//` 注释的首 token，被 ESLint
误认成真实指令并把后续散文（`with`、`a reason for` 等）当不存在的规则名报错。改为 "line-level disable
comment" 措辞，保留原意。
- 不动任何 lint 规则 / ignore 列表 / CI lint glob（issue 显式 out-of-scope）。

Linear:
https://linear.app/srpone/issue/ECA-774/chorelint-fix-pre-existing-prettier-comment-as-disable-directive

## Test plan
- [x] `pnpm exec eslint eslint.config.mjs` → 0 errors（修前 25 → 修后 0）
- [x] `git diff` 仅含 whitespace + quote style + 2
段注释措辞，无规则/message/files-globs 改动
- [x] 4 个 shrink-only sentinel 计数零变化：react/forbid-dom-props
34、svg-inline 10、no-raw-fetch 0、filename 0
- [ ] CI: `code-quality / lint-and-test` 绿（pnpm lint 不扫此文件，行为应不变）

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```


### PR Body
## Summary
- 修 `web/app/eslint.config.mjs` 25 个 pre-existing 错误（该文件不在常规 lint glob，CI 不扫，但显式 `pnpm exec eslint eslint.config.mjs` 会报）。
- `eslint --fix` 自动清 23 个 prettier 错误（shrink-only 数组延续行 trailing whitespace + 长 `no-restricted-syntax` selector 字符串 double→single quote 规范化）。
- 手动改 2 段 JS 注释（行 583-598 那个 `// Forbid inline style={{...}}` 块）：原文以 `eslint-disable-next-line` 作为 `//` 注释的首 token，被 ESLint 误认成真实指令并把后续散文（`with`、`a reason for` 等）当不存在的规则名报错。改为 "line-level disable comment" 措辞，保留原意。
- 不动任何 lint 规则 / ignore 列表 / CI lint glob（issue 显式 out-of-scope）。

Linear: https://linear.app/srpone/issue/ECA-774/chorelint-fix-pre-existing-prettier-comment-as-disable-directive

## Test plan
- [x] `pnpm exec eslint eslint.config.mjs` → 0 errors（修前 25 → 修后 0）
- [x] `git diff` 仅含 whitespace + quote style + 2 段注释措辞，无规则/message/files-globs 改动
- [x] 4 个 shrink-only sentinel 计数零变化：react/forbid-dom-props 34、svg-inline 10、no-raw-fetch 0、filename 0
- [ ] CI: `code-quality / lint-and-test` 绿（pnpm lint 不扫此文件，行为应不变）

---

## 5acb93fe fix(onboarding): handle feature launch video playback errors (#1850)

- **SHA**: 5acb93feaa6d65a296116bcc007cd4a0f67a0e92

- **Author**: bill-srp

- **Date**: 2026-05-22T10:07:27Z

- **PR**: #1850


### Full Commit Message
```
fix(onboarding): handle feature launch video playback errors (#1850)

## Summary
- Catch rejected feature-launch video playback attempts.
- Keep the modal play state accurate when the browser cannot play the
video.
- Add unit coverage for rejected media playback.

## Root cause
FeatureLaunchModal set its local playing state to true immediately after
calling video.play(). If the browser rejected playback, for example with
NotSupportedError, the promise rejection was not handled and the UI
could remain in the wrong state.

## Test plan
- [x] pnpm --dir web/app run test:unit
tests/unit/components/FeatureLaunchModal.unit.spec.tsx
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web run test:unit
- [ ] pnpm --dir web run lint (blocked locally: ESLint fails while
loading next/core-web-vitals before file analysis: Unexpected top-level
property "name")
```


### PR Body
## Summary
- Catch rejected feature-launch video playback attempts.
- Keep the modal play state accurate when the browser cannot play the video.
- Add unit coverage for rejected media playback.

## Root cause
FeatureLaunchModal set its local playing state to true immediately after calling video.play(). If the browser rejected playback, for example with NotSupportedError, the promise rejection was not handled and the UI could remain in the wrong state.

## Test plan
- [x] pnpm --dir web/app run test:unit tests/unit/components/FeatureLaunchModal.unit.spec.tsx
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web run test:unit
- [ ] pnpm --dir web run lint (blocked locally: ESLint fails while loading next/core-web-vitals before file analysis: Unexpected top-level property "name")

---

## 1c5ba698 fix(chat): handle unsupported video preview sources (#1848)

- **SHA**: 1c5ba698a454ecd51c3d66931a2e193c544a15a5

- **Author**: bill-srp

- **Date**: 2026-05-22T09:37:08Z

- **PR**: #1848


### Full Commit Message
```
fix(chat): handle unsupported video preview sources (#1848)

## Summary
- Handle unsupported or expired video sources in the chat image/video
preview modal.
- Replace native video autoplay with explicit playback handling so
NotSupportedError is caught.
- Add a video fallback state and regression test.

## Root cause
Chat video thumbnails open ImagePreview with type=video. The preview
used native video autoplay directly, so unsupported or missing media
sources could surface a browser NotSupportedError as an unhandled
production error instead of degrading to UI fallback.

Linear:
https://linear.app/srpone/issue/ECA-638/frontend-notsupportederror-media-element-has-no-supported-sources
Sentry: https://serendipity-one-inc.sentry.io/issues/7465603235/

## Test plan
- [x] pnpm test:unit tests/unit/components/ImagePreview.unit.spec.tsx
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web run test:unit
- [ ] pnpm --dir web run lint (blocked locally: ESLint fails while
loading next/core-web-vitals before file analysis: Unexpected top-level
property "name")
```


### PR Body
## Summary
- Handle unsupported or expired video sources in the chat image/video preview modal.
- Replace native video autoplay with explicit playback handling so NotSupportedError is caught.
- Add a video fallback state and regression test.

## Root cause
Chat video thumbnails open ImagePreview with type=video. The preview used native video autoplay directly, so unsupported or missing media sources could surface a browser NotSupportedError as an unhandled production error instead of degrading to UI fallback.

Linear: https://linear.app/srpone/issue/ECA-638/frontend-notsupportederror-media-element-has-no-supported-sources
Sentry: https://serendipity-one-inc.sentry.io/issues/7465603235/

## Test plan
- [x] pnpm test:unit tests/unit/components/ImagePreview.unit.spec.tsx
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web run test:unit
- [ ] pnpm --dir web run lint (blocked locally: ESLint fails while loading next/core-web-vitals before file analysis: Unexpected top-level property "name")

---

## 4e23d254 fix(chat): keep spawned sessions visible (#1847)

- **SHA**: 4e23d254e53ece8ff062e9883a205c737a2f8fbe

- **Author**: bill-srp

- **Date**: 2026-05-22T08:38:06Z

- **PR**: #1847


### Full Commit Message
```
fix(chat): keep spawned sessions visible (#1847)

## Summary
- Keep spawned subagent sessions visible after they reach terminal
status.
- Remove the local auto-collapse timer that made completed spawned
sessions disappear after switching agents.
- Update focused hook tests to cover persistent terminal sessions.

## Root cause
The chat rail locally marked terminal spawned sessions as
fading/collapsed after a short timeout. When a user switched to another
agent and returned after that timeout, the session was still known
locally but no longer in the visible rail, so it appeared to disappear.

Linear:
https://linear.app/srpone/issue/ECA-737/spawn-的-session-显示不稳定切换-agent-后消失

## Test plan
- [x] pnpm --dir web/app run lint
- [x] pnpm exec vitest run --config ./vitest.config.mts
tests/unit/app/chat/useSubagentSessions.unit.spec.ts
tests/unit/app/chat/useChatSubagentRail.unit.spec.ts
- [ ] pnpm --dir web run lint (blocked outside app:
web/packages/auth-client cannot resolve typescript-eslint)
- [ ] pnpm --dir web run tsc (workspace script fails: pnpm exec rejects
--if-present)
- [ ] pnpm --dir web/app exec tsc --noEmit (blocked:
src/lib/heic-image.ts cannot resolve heic-to/csp)
- [ ] pnpm --dir web/app run test:unit (blocked: heic-to/csp resolution
failure in unrelated heic/upload/Mattermost suites)
```


### PR Body
## Summary
- Keep spawned subagent sessions visible after they reach terminal status.
- Remove the local auto-collapse timer that made completed spawned sessions disappear after switching agents.
- Update focused hook tests to cover persistent terminal sessions.

## Root cause
The chat rail locally marked terminal spawned sessions as fading/collapsed after a short timeout. When a user switched to another agent and returned after that timeout, the session was still known locally but no longer in the visible rail, so it appeared to disappear.

Linear: https://linear.app/srpone/issue/ECA-737/spawn-的-session-显示不稳定切换-agent-后消失

## Test plan
- [x] pnpm --dir web/app run lint
- [x] pnpm exec vitest run --config ./vitest.config.mts tests/unit/app/chat/useSubagentSessions.unit.spec.ts tests/unit/app/chat/useChatSubagentRail.unit.spec.ts
- [ ] pnpm --dir web run lint (blocked outside app: web/packages/auth-client cannot resolve typescript-eslint)
- [ ] pnpm --dir web run tsc (workspace script fails: pnpm exec rejects --if-present)
- [ ] pnpm --dir web/app exec tsc --noEmit (blocked: src/lib/heic-image.ts cannot resolve heic-to/csp)
- [ ] pnpm --dir web/app run test:unit (blocked: heic-to/csp resolution failure in unrelated heic/upload/Mattermost suites)

---

## c98a8879 fix(web): consume shared RQ cache for publish install state (ECA-790) (#1845)

- **SHA**: c98a88791e65965e798c791e417653954912f861

- **Author**: Nemo Feng

- **Date**: 2026-05-22T08:11:10Z

- **PR**: #1845


### Full Commit Message
```
fix(web): consume shared RQ cache for publish install state (ECA-790) (#1845)

## Summary
- Replace the bespoke `await getOpenClawAgents()` in
`PublishAgentsClient.tsx` with `useUserAgents()` consumption + `useMemo`
projections.
- Add `isError` to `useUserAgents`'s return so the publish page can
drive its banner from the shared query.
- **Derive the load-failure banner at render** from
`isInstalledStateError` (no `useEffect` mirroring into local state) —
recovery clears it automatically.
- Post-mutation refresh now flows through `refreshUserAgentsCache({
force: true })` and reaches the shared RQ cache via the existing
`ecap:agents:updated` event bridge — no more direct fetch.

## Root cause
The publish page used a bare `useEffect` to fetch `/openclaw/agents` on
mount, missing **three** patterns the rest of the codebase already
applies to the same backend call:

1. **Auth gate (`enabled`)** — `useCustomAgentPublishes` already gates
by `authToken !== null`. This page didn't.
2. **Retry** — the global `QueryClient` sets `retry: 1`. The bespoke
fetch had no retry.
3. **Shared query key** — `useUserAgents` keys by
`openclawKeys.agents(authToken)`. Running a separate direct fetch on the
same page meant **two** parallel `/agents` calls through the same flaky
`verifyToken` boundary in `web/app/src/lib/api/token-verifier.ts` (which
deliberately does not cache transient failures — see line 82-85). When
that verifier flaked, the bespoke fetch surfaced "Failed to load install
status." while `useUserAgents` (with its retry) usually recovered.
Refreshing the page made the error disappear, which matched the
intermittent symptom reported in
[ECA-790](https://linear.app/srpone/issue/ECA-790/).

The fix is removal, not addition: by consuming the same hook that the
rest of the app uses, all three patterns come for free, and the doubled
load on `verifyToken` goes away.

## Test plan
- [x] `tests/unit/app/agents-manager-publish.unit.spec.tsx` — added a
stateful `useUserAgents` mock that mirrors the production bridge
(`mockGetOpenClawAgents` on mount + `ecap:agents:updated` listener for
refetch). The default `mockRefreshUserAgentsCache` impl now dispatches
the same event, matching the real helper.
- [x] Existing `installStateLoadFailed` test (the error-catch branch)
continues to cover the new derived-banner path — the mocked
`useUserAgents` propagates the rejection through `isError`.
- [x] **New regression test**: `clears the installStateLoadFailed banner
when a follow-up fetch recovers` — first fetch rejects (banner shows),
dispatch `ecap:agents:updated` to trigger refetch that succeeds, banner
must clear.
- [x] Removed three verbatim duplicates of the `import_url`
install/uninstall tests (pre-existing copy-paste from the file's
incremental coverage block).
- [ ] Manually verify on `/agents-manager/publish`: load the page
repeatedly; the transient banner should no longer appear, and if it does
appear from a real flake it should clear on the next successful refetch.

Linear: https://linear.app/srpone/issue/ECA-790/

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>
```


### PR Body
## Summary
- Replace the bespoke `await getOpenClawAgents()` in `PublishAgentsClient.tsx` with `useUserAgents()` consumption + `useMemo` projections.
- Add `isError` to `useUserAgents`'s return so the publish page can drive its banner from the shared query.
- **Derive the load-failure banner at render** from `isInstalledStateError` (no `useEffect` mirroring into local state) — recovery clears it automatically.
- Post-mutation refresh now flows through `refreshUserAgentsCache({ force: true })` and reaches the shared RQ cache via the existing `ecap:agents:updated` event bridge — no more direct fetch.

## Root cause
The publish page used a bare `useEffect` to fetch `/openclaw/agents` on mount, missing **three** patterns the rest of the codebase already applies to the same backend call:

1. **Auth gate (`enabled`)** — `useCustomAgentPublishes` already gates by `authToken !== null`. This page didn't.
2. **Retry** — the global `QueryClient` sets `retry: 1`. The bespoke fetch had no retry.
3. **Shared query key** — `useUserAgents` keys by `openclawKeys.agents(authToken)`. Running a separate direct fetch on the same page meant **two** parallel `/agents` calls through the same flaky `verifyToken` boundary in `web/app/src/lib/api/token-verifier.ts` (which deliberately does not cache transient failures — see line 82-85). When that verifier flaked, the bespoke fetch surfaced "Failed to load install status." while `useUserAgents` (with its retry) usually recovered. Refreshing the page made the error disappear, which matched the intermittent symptom reported in [ECA-790](https://linear.app/srpone/issue/ECA-790/).

The fix is removal, not addition: by consuming the same hook that the rest of the app uses, all three patterns come for free, and the doubled load on `verifyToken` goes away.

## Test plan
- [x] `tests/unit/app/agents-manager-publish.unit.spec.tsx` — added a stateful `useUserAgents` mock that mirrors the production bridge (`mockGetOpenClawAgents` on mount + `ecap:agents:updated` listener for refetch). The default `mockRefreshUserAgentsCache` impl now dispatches the same event, matching the real helper.
- [x] Existing `installStateLoadFailed` test (the error-catch branch) continues to cover the new derived-banner path — the mocked `useUserAgents` propagates the rejection through `isError`.
- [x] **New regression test**: `clears the installStateLoadFailed banner when a follow-up fetch recovers` — first fetch rejects (banner shows), dispatch `ecap:agents:updated` to trigger refetch that succeeds, banner must clear.
- [x] Removed three verbatim duplicates of the `import_url` install/uninstall tests (pre-existing copy-paste from the file's incremental coverage block).
- [x] Manually verify on `/agents-manager/publish`: load the page repeatedly; the transient banner should no longer appear, and if it does appear from a real flake it should clear on the next successful refetch.

Linear: https://linear.app/srpone/issue/ECA-790/

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## bc76583f chore(web): relax frontend file length limit (#1846)

- **SHA**: bc76583f68e6d8c626347cdd4041972f3822db5d

- **Author**: Chris@ZooClaw

- **Date**: 2026-05-22T07:48:32Z

- **PR**: #1846


### Full Commit Message
```
chore(web): relax frontend file length limit (#1846)

## Summary
- Raise the frontend ESLint file-level `max-lines` threshold from 500 to
600 effective lines.
- Keep `max-lines-per-function` at 300 and keep existing legacy
complexity exemptions unchanged.
- Restore `useMattermostIntegration` instead of mechanically splitting
helper code.

Linear: https://linear.app/srpone/issue/ECA-494

## Test plan
- `pnpm --dir web/app exec eslint
'src/app/[locale]/chat/hooks/useMattermostIntegration.ts' --quiet`
- `pnpm --filter @zooclaw/web-app lint`
- `git diff --check`
```


### PR Body
## Summary
- Raise the frontend ESLint file-level `max-lines` threshold from 500 to 600 effective lines.
- Keep `max-lines-per-function` at 300 and keep existing legacy complexity exemptions unchanged.
- Restore `useMattermostIntegration` instead of mechanically splitting helper code.

Linear: https://linear.app/srpone/issue/ECA-494

## Test plan
- `pnpm --dir web/app exec eslint 'src/app/[locale]/chat/hooks/useMattermostIntegration.ts' --quiet`
- `pnpm --filter @zooclaw/web-app lint`
- `git diff --check`

---

## 6645dd5f feat(enterprise): add org pack store backend (#1833)

- **SHA**: 6645dd5fd01f6d1731b2d924f65e6bd76dfeb650

- **Author**: bill-srp

- **Date**: 2026-05-22T06:29:48Z

- **PR**: #1833


### Full Commit Message
```
feat(enterprise): add org pack store backend (#1833)

## Summary
- Adds org-scoped pack store schemas, repositories, services, and
enterprise routes.
- Wires Mongo collections and startup indexes for packs and submissions.
- Covers submission/review approval/deprecation flows, including
concurrent review CAS and deprecated-pack guards.

## Linear

https://linear.app/srpone/issue/ECA-764/phase-1-backend-changes-enterprise-data-model-warm-pool-cross-service

## Tests
- `docker exec service-agent-pack-bill ... ruff check .`
- `docker exec service-agent-pack-bill ... ruff format --check app
tests`
- `docker exec service-agent-pack-bill ... lint-imports`
- `docker exec service-agent-pack-bill ... pyright app tests`
- `docker exec service-agent-pack-bill ... pytest
tests/unit/test_schema_pack.py tests/unit/test_pack_repo.py
tests/unit/test_pack_submission_repo.py tests/unit/test_pack_services.py
tests/unit/test_routes_pack_store.py
tests/unit/test_enterprise_wiring.py -q`

Note: the full repository coverage command completed test execution but
failed locally in this devcontainer because `test_ci_lint_deptry.py`
cannot resolve the host worktree `.git` path from inside the container,
and the aggregate coverage report is 87.88% against the repository-wide
90% threshold.
```


### PR Body
## Summary
- Adds org-scoped pack store schemas, repositories, services, and enterprise routes.
- Wires Mongo collections and startup indexes for packs and submissions.
- Covers submission/review approval/deprecation flows, including concurrent review CAS and deprecated-pack guards.

## Linear
https://linear.app/srpone/issue/ECA-764/phase-1-backend-changes-enterprise-data-model-warm-pool-cross-service

## Tests
- `docker exec service-agent-pack-bill ... ruff check .`
- `docker exec service-agent-pack-bill ... ruff format --check app tests`
- `docker exec service-agent-pack-bill ... lint-imports`
- `docker exec service-agent-pack-bill ... pyright app tests`
- `docker exec service-agent-pack-bill ... pytest tests/unit/test_schema_pack.py tests/unit/test_pack_repo.py tests/unit/test_pack_submission_repo.py tests/unit/test_pack_services.py tests/unit/test_routes_pack_store.py tests/unit/test_enterprise_wiring.py -q`

Note: the full repository coverage command completed test execution but failed locally in this devcontainer because `test_ci_lint_deptry.py` cannot resolve the host worktree `.git` path from inside the container, and the aggregate coverage report is 87.88% against the repository-wide 90% threshold.

---

## 23b6a5e7 fix(chat): recover Mattermost reconnect on tab resume (#1844)

- **SHA**: 23b6a5e78031f230e4162d316115aca91834fc26

- **Author**: Chris@ZooClaw

- **Date**: 2026-05-22T06:20:05Z

- **PR**: #1844


### Full Commit Message
```
fix(chat): recover Mattermost reconnect on tab resume (#1844)

## Summary
- Recover Mattermost WebSocket when returning to a tab after a stale
hidden interval.
- Re-arm Mattermost reconnect after retry exhaustion while the tab was
hidden or backgrounded.
- Track low-level Mattermost WS activity, including ping replies, so
healthy quiet sockets are not treated as stale.
- Avoid recursive reconnect scheduling when intentionally replacing a
stale Mattermost socket.

## Root cause
Mattermost chat depended on the browser delivering WebSocket close
events to enter its reconnect loop. Backgrounded tabs throttle timers
and can return with a stale socket still marked connected, or with
reconnect attempts already exhausted. Unlike the OpenClaw WS path, the
Mattermost path had no visible-tab recovery probe. The stale detector
now keys off any valid WS frame, not just user-facing Mattermost events,
so ping replies keep healthy idle sockets fresh.

## Review-driven fixes
- Addressed Codex review feedback that event-only freshness would
reconnect healthy quiet channels because Mattermost seq_reply ping
responses were ignored before onEvent.
- Added MattermostWebSocketService.onActivity and a regression test
proving idle ping activity prevents unnecessary visible-tab reconnect.

## Test plan
- [x] pnpm --dir web/app exec vitest run
tests/unit/hooks/useMattermost.unit.spec.ts
- [x] pnpm --dir web/app exec eslint src/hooks/useMattermost.ts
src/lib/mattermost/websocket.ts
tests/unit/hooks/useMattermost.unit.spec.ts
- [x] pnpm --dir web exec tsc --noEmit --project app/tsconfig.json
- [x] pnpm --dir web/app run lint
- [x] pnpm --dir web/app run test:unit
- [ ] pnpm --dir web run lint (blocked locally by
web/packages/auth-client missing typescript-eslint; web/app lint passed)
- [ ] pnpm --dir web run test:unit (one local recursive run exited
nonzero on jsdom navigation noise; direct web/app unit suite passed and
CI web-quality/test is authoritative)
```


### PR Body
## Summary
- Recover Mattermost WebSocket when returning to a tab after a stale hidden interval.
- Re-arm Mattermost reconnect after retry exhaustion while the tab was hidden or backgrounded.
- Track low-level Mattermost WS activity, including ping replies, so healthy quiet sockets are not treated as stale.
- Avoid recursive reconnect scheduling when intentionally replacing a stale Mattermost socket.

## Root cause
Mattermost chat depended on the browser delivering WebSocket close events to enter its reconnect loop. Backgrounded tabs throttle timers and can return with a stale socket still marked connected, or with reconnect attempts already exhausted. Unlike the OpenClaw WS path, the Mattermost path had no visible-tab recovery probe. The stale detector now keys off any valid WS frame, not just user-facing Mattermost events, so ping replies keep healthy idle sockets fresh.

## Review-driven fixes
- Addressed Codex review feedback that event-only freshness would reconnect healthy quiet channels because Mattermost seq_reply ping responses were ignored before onEvent.
- Added MattermostWebSocketService.onActivity and a regression test proving idle ping activity prevents unnecessary visible-tab reconnect.

## Test plan
- [x] pnpm --dir web/app exec vitest run tests/unit/hooks/useMattermost.unit.spec.ts
- [x] pnpm --dir web/app exec eslint src/hooks/useMattermost.ts src/lib/mattermost/websocket.ts tests/unit/hooks/useMattermost.unit.spec.ts
- [x] pnpm --dir web exec tsc --noEmit --project app/tsconfig.json
- [x] pnpm --dir web/app run lint
- [x] pnpm --dir web/app run test:unit
- [ ] pnpm --dir web run lint (blocked locally by web/packages/auth-client missing typescript-eslint; web/app lint passed)
- [ ] pnpm --dir web run test:unit (one local recursive run exited nonzero on jsdom navigation noise; direct web/app unit suite passed and CI web-quality/test is authoritative)

---

## fcf3c3eb fix(billing): ignore Stripe proration-only renewal invoices (#1832)

- **SHA**: fcf3c3eb76910f7b92bcb3bb5f55df0862da23dd

- **Author**: kaka-srp

- **Date**: 2026-05-22T03:00:58Z

- **PR**: #1832


### Full Commit Message
```
fix(billing): ignore Stripe proration-only renewal invoices (#1832)

## Summary
- Ignore Stripe `invoice.paid` subscription invoices that do not start a
credit-bearing service period.
- Keep `subscription_create` and `subscription_cycle` behavior
unchanged.
- For `subscription_update`, skip proration-only adjustment invoices but
allow invoices with a non-proration subscription service-period line.
- Apply the same service-period guard to cron Stripe renewal recovery.

## Root cause
Production scan found a user with two `RENEWAL-*` subscription grants
within one cycle. The earlier invoice had
`billing_reason=subscription_update` and only proration lines, produced
by a subscription item/price adjustment. That invoice is a billing
adjustment, not the start of a new monthly service period, so treating
it as a renewal incorrectly grants monthly subscription credits.

Current upgrades are handled by the checkout flow: the UI creates a
subscription order and Stripe checkout session;
`checkout.session.completed` detects old/new subscription ids, marks the
order as an upgrade, and `grant_entitlement` grants the new plan credits
immediately. This PR avoids a second grant from later proration-only
update invoices without blocking update invoices that genuinely carry a
new service period.

Related issue:
https://linear.app/srpone/issue/ECA-783/prevent-duplicate-subscription-renewal-credits

## Test plan
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_handle_invoice_paid.py
tests/unit/test_stripe_renewal_cron.py
tests/unit/test_stripe_renewal_order.py
tests/unit/test_subscription_cron.py`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff check
app/cron/stripe_renewal.py app/services/stripe/handlers/invoice.py
app/services/stripe/renewal_order.py
tests/unit/test_handle_invoice_paid.py
tests/unit/test_stripe_renewal_cron.py`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff format --check
app/cron/stripe_renewal.py app/services/stripe/handlers/invoice.py
app/services/stripe/renewal_order.py
tests/unit/test_handle_invoice_paid.py
tests/unit/test_stripe_renewal_cron.py`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pyright --pythonpath
/home/node/.venvs/claw-interface/bin/python app tests`
```


### PR Body
## Summary
- Ignore Stripe `invoice.paid` subscription invoices that do not start a credit-bearing service period.
- Keep `subscription_create` and `subscription_cycle` behavior unchanged.
- For `subscription_update`, skip proration-only adjustment invoices but allow invoices with a non-proration subscription service-period line.
- Apply the same service-period guard to cron Stripe renewal recovery.

## Root cause
Production scan found a user with two `RENEWAL-*` subscription grants within one cycle. The earlier invoice had `billing_reason=subscription_update` and only proration lines, produced by a subscription item/price adjustment. That invoice is a billing adjustment, not the start of a new monthly service period, so treating it as a renewal incorrectly grants monthly subscription credits.

Current upgrades are handled by the checkout flow: the UI creates a subscription order and Stripe checkout session; `checkout.session.completed` detects old/new subscription ids, marks the order as an upgrade, and `grant_entitlement` grants the new plan credits immediately. This PR avoids a second grant from later proration-only update invoices without blocking update invoices that genuinely carry a new service period.

Related issue: https://linear.app/srpone/issue/ECA-783/prevent-duplicate-subscription-renewal-credits

## Test plan
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_handle_invoice_paid.py tests/unit/test_stripe_renewal_cron.py tests/unit/test_stripe_renewal_order.py tests/unit/test_subscription_cron.py`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff check app/cron/stripe_renewal.py app/services/stripe/handlers/invoice.py app/services/stripe/renewal_order.py tests/unit/test_handle_invoice_paid.py tests/unit/test_stripe_renewal_cron.py`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff format --check app/cron/stripe_renewal.py app/services/stripe/handlers/invoice.py app/services/stripe/renewal_order.py tests/unit/test_handle_invoice_paid.py tests/unit/test_stripe_renewal_cron.py`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pyright --pythonpath /home/node/.venvs/claw-interface/bin/python app tests`


---

## 6b8dc587 ci(codeql): extend matrix to JavaScript, drop unused Ruby, add verify fixture (#1843)

- **SHA**: 6b8dc587563bb385d4478e8af6e4f93548c09e2a

- **Author**: Chris@ZooClaw

- **Date**: 2026-05-22T01:50:47Z

- **PR**: #1843


### Full Commit Message
```
ci(codeql): extend matrix to JavaScript, drop unused Ruby, add verify fixture (#1843)

## Summary

Follow-up to PR #1839 (ECA-693)。本 PR 两件事：

1. **Add `javascript`** — CodeQL 的 javascript language 同时覆盖 JS 和 TS，对应
`web/` 下的 Next.js 应用。补上 Codex review 在 PR #1839 round 1 提示的 gap：原
default setup 从来没扫过仓库的 JS/TS。
2. **Drop `ruby`** — 仓库唯一的 ruby 代码是
`ios/ZooClaw/fastlane/{Appfile,Fastfile,Matchfile,Pluginfile}`（4 个 DSL
文件）。历史 CodeQL alert 来自 ruby 的条数为 **0**，扫描无实际信号，仅占 CI 时间。

Linear: https://linear.app/srpone/issue/ECA-693

## ✅ Verification done

本 PR 之前临时包含 `.github/codeql/codeql-verify-sample.js` 作为 JS 扫描的正面验证
fixture。Commit `85e62e4d` 的 CodeQL run 确认：

- `Analyze (javascript)` job pass
- 86 个 default Security rules 跑完
- **`js/redos` 在 fixture 的 line 28 fire**（catastrophic backtracking
regex `/^(a+)+$/`）
- 证明：(a) JS scanning 是真的在跑、(b) default suite 包含 ReDoS 检测、(c) 扫描到
`.github/` 目录下的 JS 文件

`js/insecure-randomness` 没 fire——Math.random → crypto.hash 的 taint flow
不满足该 query 的 sink classification。但 `js/redos` 单次 fire 已足够证明 scan path
通畅。

验证完成后 commit `8f38a62b` 删除 fixture。现在 PR 净改动只剩 matrix 调整。

## What changed (final)

- `.github/workflows/codeql.yml`
- matrix.language: `[actions, python, ruby]` → `[actions, javascript,
python]`
  - 注释更新：解释 JS 加入 / Ruby 移除的依据

## Test plan

- [x] `Analyze (javascript)` job 在 commit 85e62e4d 跑通并 fire
`js/redos`（验证 fixture 触发）
- [x] 验证后删除 fixture（commit 8f38a62b）
- [ ] commit 8f38a62b 上的 CI 全 pass（包括 CodeQL aggregate check 不再因为
fixture alert 而 fail）
- [ ] `Analyze (ruby)` 不再出现在 CI

## Follow-up

- 合入后 `web/` 进入 CodeQL JS 扫描覆盖。如果首次 main scheduled scan 浮出现有 latent
alerts，按价值分批 triage（另开 issue）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```


### PR Body
## Summary

Follow-up to PR #1839 (ECA-693)。本 PR 两件事：

1. **Add `javascript`** — CodeQL 的 javascript language 同时覆盖 JS 和 TS，对应 `web/` 下的 Next.js 应用。补上 Codex review 在 PR #1839 round 1 提示的 gap：原 default setup 从来没扫过仓库的 JS/TS。
2. **Drop `ruby`** — 仓库唯一的 ruby 代码是 `ios/ZooClaw/fastlane/{Appfile,Fastfile,Matchfile,Pluginfile}`（4 个 DSL 文件）。历史 CodeQL alert 来自 ruby 的条数为 **0**，扫描无实际信号，仅占 CI 时间。

Linear: https://linear.app/srpone/issue/ECA-693

## ✅ Verification done

本 PR 之前临时包含 `.github/codeql/codeql-verify-sample.js` 作为 JS 扫描的正面验证 fixture。Commit `85e62e4d` 的 CodeQL run 确认：

- `Analyze (javascript)` job pass
- 86 个 default Security rules 跑完
- **`js/redos` 在 fixture 的 line 28 fire**（catastrophic backtracking regex `/^(a+)+$/`）
- 证明：(a) JS scanning 是真的在跑、(b) default suite 包含 ReDoS 检测、(c) 扫描到 `.github/` 目录下的 JS 文件

`js/insecure-randomness` 没 fire——Math.random → crypto.hash 的 taint flow 不满足该 query 的 sink classification。但 `js/redos` 单次 fire 已足够证明 scan path 通畅。

验证完成后 commit `8f38a62b` 删除 fixture。现在 PR 净改动只剩 matrix 调整。

## What changed (final)

- `.github/workflows/codeql.yml`
  - matrix.language: `[actions, python, ruby]` → `[actions, javascript, python]`
  - 注释更新：解释 JS 加入 / Ruby 移除的依据

## Test plan

- [x] `Analyze (javascript)` job 在 commit 85e62e4d 跑通并 fire `js/redos`（验证 fixture 触发）
- [x] 验证后删除 fixture（commit 8f38a62b）
- [ ] commit 8f38a62b 上的 CI 全 pass（包括 CodeQL aggregate check 不再因为 fixture alert 而 fail）
- [ ] `Analyze (ruby)` 不再出现在 CI

## Follow-up

- 合入后 `web/` 进入 CodeQL JS 扫描覆盖。如果首次 main scheduled scan 浮出现有 latent alerts，按价值分批 triage（另开 issue）

🤖 Generated with [Claude Code](https://claude.com/claude-code)
