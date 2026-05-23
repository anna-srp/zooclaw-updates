---
title: "修复聊天内存泄漏问题，长时间使用不再卡顿"
type: "Bug Fix"
priority: "高"
date: "2026-05-22"
status: "待审核"
channels: ""
---

# 修复聊天内存泄漏问题，长时间使用不再卡顿

## 核心宣传点

修复了长时间使用聊天时浏览器内存泄漏的问题，App 不再因为内存积累而变慢或崩溃，使用体验更流畅。

## 原始内容

**Commit**: ecc37ad04d025fffb998302b149b484eb80396b5
**Author**: Chris@ZooClaw
**Date**: 2026-05-22T16:08:11Z
**PR**: #1858

### Commit Message
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

### PR Description
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


