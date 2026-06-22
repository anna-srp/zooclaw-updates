---
title: "聊天显示「轮次状态」，更准确地知道智能体是否在生成"
type: "体验优化"
priority: "中"
date: "2026-06-18"
status: "待审核"
channels: "Discord+changelog"
---
# 聊天显示「轮次状态」，更准确地知道智能体是否在生成
## 核心宣传点
聊天现在解析并展示持久化的轮次状态（turn status），用更权威的信号判断智能体是否正在生成回复，支持主聊天与会话线程视图，并在心跳过期时显示「未知」状态，让「正在处理中」的提示更准确可靠。
## 原始内容
feat(chat): show turn status (#2507)

## Linear
https://linear.app/srpone/issue/ECA-1011

## Summary
- Add durable Mattermost turn_status parsing and rendering for
chat/user-message state.
- Use fresh turn status as the authoritative generating signal while
preserving old waiting heuristics when status is missing.
- Support main chat and session-thread views, including stale-heartbeat
unknown state and same-post status edit ordering.
- Emit a 2-minute `chat.message.slow_response` Sentry log with uid, bot
id, message id, elapsed time, and unresolved ack/reply state.
- Document the cross-repo producer/consumer contract for Mattermost turn
status.

## Test plan
- [x] `pnpm exec vitest run
tests/unit/app/chat/turnStatusParser.unit.spec.ts
tests/unit/hooks/useMmTypewriter.unit.spec.ts
tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx
tests/unit/app/chat-thread/useLiveThread.unit.spec.ts
tests/unit/hooks/mattermost/useMattermostPosts.unit.spec.ts
tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts`
- [x] `pnpm exec vitest run
tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts
tests/unit/app/chat/useChatMessaging.unit.spec.ts
tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh --no-test
web/app/src/lib/mattermost/post-store.ts
web/app/src/hooks/mattermost/useMattermostPosts.ts
web/app/src/app/[locale]/(app)/(chat)/chat/[computerId]/[agentId]/[sessionId]/hooks/useLiveThread.ts
web/app/src/app/[locale]/(app)/(chat)/chat/[computerId]/[agentId]/[sessionId]/hooks/useSessionThreadDisplayMessages.ts
web/app/src/app/[locale]/(app)/(chat)/chat/lib/turnStatusParser.ts
web/app/src/lib/sentry/message-latency-monitor.ts
web/app/src/app/[locale]/(app)/(chat)/chat/components/ChatBody.tsx
web/app/tests/unit/hooks/mattermost/useMattermostPosts.unit.spec.ts
web/app/tests/unit/app/chat-thread/useLiveThread.unit.spec.ts
web/app/tests/unit/app/chat/turnStatusParser.unit.spec.ts
web/app/tests/unit/hooks/useMmTypewriter.unit.spec.ts
web/app/tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx
web/app/tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts`
- [x] `bash scripts/verify-web.sh --no-test
web/app/src/lib/sentry/message-latency-monitor.ts
web/app/src/app/[locale]/(app)/(chat)/chat/hooks/useChatMessaging.ts
web/app/src/app/[locale]/(app)/(chat)/chat/GenClawClient.tsx
web/app/src/app/[locale]/(app)/(chat)/chat/[computerId]/[agentId]/[sessionId]/SessionThreadClient.tsx
web/app/tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts
web/app/tests/unit/app/chat/useChatMessaging.unit.spec.ts
web/app/tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx`
- [x] `git diff --check origin/main...HEAD`

## PR Description
## Linear
https://linear.app/srpone/issue/ECA-1011

## Summary
- Add durable Mattermost turn_status parsing and rendering for chat/user-message state.
- Use fresh turn status as the authoritative generating signal while preserving old waiting heuristics when status is missing.
- Support main chat and session-thread views, including stale-heartbeat unknown state and same-post status edit ordering.
- Emit a 2-minute `chat.message.slow_response` Sentry log with uid, bot id, message id, elapsed time, and unresolved ack/reply state.
- Document the cross-repo producer/consumer contract for Mattermost turn status.

## Test plan
- [x] `pnpm exec vitest run tests/unit/app/chat/turnStatusParser.unit.spec.ts tests/unit/hooks/useMmTypewriter.unit.spec.ts tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx tests/unit/app/chat-thread/useLiveThread.unit.spec.ts tests/unit/hooks/mattermost/useMattermostPosts.unit.spec.ts tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts`
- [x] `pnpm exec vitest run tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts tests/unit/app/chat/useChatMessaging.unit.spec.ts tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh --no-test web/app/src/lib/mattermost/post-store.ts web/app/src/hooks/mattermost/useMattermostPosts.ts web/app/src/app/[locale]/(app)/(chat)/chat/[computerId]/[agentId]/[sessionId]/hooks/useLiveThread.ts web/app/src/app/[locale]/(app)/(chat)/chat/[computerId]/[agentId]/[sessionId]/hooks/useSessionThreadDisplayMessages.ts web/app/src/app/[locale]/(app)/(chat)/chat/lib/turnStatusParser.ts web/app/src/lib/sentry/message-latency-monitor.ts web/app/src/app/[locale]/(app)/(chat)/chat/components/ChatBody.tsx web/app/tests/unit/hooks/mattermost/useMattermostPosts.unit.spec.ts web/app/tests/unit/app/chat-thread/useLiveThread.unit.spec.ts web/app/tests/unit/app/chat/turnStatusParser.unit.spec.ts web/app/tests/unit/hooks/useMmTypewriter.unit.spec.ts web/app/tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx web/app/tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts`
- [x] `bash scripts/verify-web.sh --no-test web/app/src/lib/sentry/message-latency-monitor.ts web/app/src/app/[locale]/(app)/(chat)/chat/hooks/useChatMessaging.ts web/app/src/app/[locale]/(app)/(chat)/chat/GenClawClient.tsx web/app/src/app/[locale]/(app)/(chat)/chat/[computerId]/[agentId]/[sessionId]/SessionThreadClient.tsx web/app/tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts web/app/tests/unit/app/chat/useChatMessaging.unit.spec.ts web/app/tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx`
- [x] `git diff --check origin/main...HEAD`

