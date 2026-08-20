---
title: "所有聊天界面统一显示 AI 当前状态：正在思考 / 正在执行任务 / 正在组织回复"
type: "体验优化"
priority: "中"
date: "2026-08-19"
status: "待审核"
channels: ""
---

# 所有聊天界面统一显示 AI 当前状态：正在思考 / 正在执行任务 / 正在组织回复

## 核心宣传点

主聊天、会话线程、Agent Builder、Agent 预览和子 Agent 聊天现在共用同一套状态提示，中英文各三个统一文案（正在思考… / 正在执行任务… / 正在组织回复…）。多个会话之间状态互不串台，只读回放不会误报，也遵循系统「减少动态效果」设置。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `ac5f6529e12be8fa798ccd73ef1b42c201ea0d04`
- PR: #3392
- 作者: lynn Zhuang
- 日期: 2026-08-19T10:09:16Z

### Commit Message

```
feat(chat): show v2 activity across interactive surfaces (#3392)

## Summary

- Add one shared V2 Chat activity model (`thinking | tool | responding |
null`) and neutral presentation for Main Chat, Session Thread, Agent
Builder, Agent Preview, and interactive Subagent Chat.
- Derive Mattermost/ACS activity from real `tool_status` and
`assistant_segment` events, and derive Gateway activity from
`chat.send`, scoped agent/tool/delta events, and terminal lifecycle
events.
- Preserve run/session isolation, ignore V1 `custom_turn_status`, and
keep replacement-run state safe from late abort confirmations and
retired-run events.
- Use exactly three localized global labels, with English fallback:
- English: `Thinking…`, `Working on the task…`, `Preparing the
response…`
  - Chinese: `正在思考…`, `正在执行任务…`, `正在组织回复…`
- Preserve connection-warning priority, read-only/replay suppression,
polite live-region semantics, and reduced-motion behavior in both main
and compact composers.

## Signal contracts

- Mattermost/ACS: pending, queued, or running `tool_status` events map
to working; nonterminal streaming/assistant segments map to preparing;
waiting maps to thinking. Final streams, terminal segments/status, and
ordinary visible replies are terminal boundaries. Pending ownership is
isolated by channel + root/session, including typing events, so one
thread cannot show or clear another thread or Main. Tool names and
arguments are never shown.
- Gateway: `chat.send` establishes the active run; scoped tool events
map to working; assistant deltas map to preparing. A transport-ambiguous
send replays on stable reconnect with the same idempotency key before
abort/reconciliation. Definitive not-sent/rejected failures remove only
their optimistic row and preserve the draft; ambiguous failures remain
visibly fenced. Terminal lifecycle, error, confirmed abort, and
disconnect paths clear per the implementation. Events from other
sessions or runs are ignored.
- Late abort confirmations are attempt- and run-scoped: they cannot
clear or otherwise mutate a replacement run.

## Visual treatment

- Neutral `#a1a1aa` text, regular weight, and a white shimmer are shared
by all five V2 surfaces.
- The fixed neutral color is an accepted product tradeoff against strict
contrast guidance for this transient status text.

## Verification

The branch previously merged `origin/main` at `5b15d93ad`. For fix round
1, `origin/main` was fetched at `ac6581ec`; GitHub CI validates the
current merge ref. These local commands passed at the final review-round
head:

```bash
cd web/app
pnpm exec vitest run \
  tests/unit/app/chat/chatActivity.unit.spec.ts \
  tests/unit/app/chat/ChatBody.unit.spec.tsx \
  tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx \
  tests/unit/app/agent-builder-client.unit.spec.tsx \
  tests/unit/app/agent-builder-test-chat.unit.spec.tsx \
  tests/unit/app/chat/GenClawInput.unit.spec.tsx \
  tests/unit/app/chat/OpenClawChatSurface.unit.spec.tsx \
  tests/unit/app/chat/useSubagentChat.unit.spec.ts \
  tests/unit/app/chat/SubagentChatPanel.unit.spec.tsx
```

Result: 9 files and 394 tests passed. The complete directly impacted
suite passed 13 files and 492 tests.

```bash
cd web/packages/chat-ui
pnpm exec tsc --noEmit
pnpm exec vitest run src/__tests__/chat-composer.test.tsx
pnpm exec eslint src
```

Result: typecheck and lint passed; 1 file and 48 tests passed.

```bash
bash scripts/verify-web.sh \
  web/app/src/lib/chat/chat-activity.ts \
  web/app/src/app/[locale]/\(app\)/\(chat\)/chat \
  web/app/src/app/[locale]/\(app\)/\(chat\)/agent-builder \
  web/packages/chat-ui/src/composer/parts/ComposerNotices.tsx
bash scripts/verify-changed.sh
git diff --check
git diff --check origin/main...HEAD
```

Result: repository guards, TypeScript, 129 files / 1840 tests, ESLint,
changed-surface verification, and diff checks passed. ESLint retains one
unrelated existing `LandingStartupOverlay.tsx` accessibility warning;
the focused Vite runs retain the existing `vite-tsconfig-paths`
migration advisory.

## Review follow-up

- The earlier confirmed-abort defect is fixed: exact authoritative abort
confirmation releases only the matching direct or deferred attempt,
while false, malformed, or rejected responses remain fenced.
- Fix round 1 adds two deferred race regressions for confirmations that
arrive after old-run lifecycle end and a replacement send. Temporarily
removing the corresponding attempt-identity or run guard made each new
test fail; restoring the guards returned the suite to green. The current
production implementation was already correct, so this round required
test and evidence changes only.
- The final review fix wave addresses all six confirmed Important
findings test-first: nonfinal posted stream previews; root/session
pending isolation (including `parent_id` typing); stable reconnect
replay/reconciliation; successful hidden-Stop activity suppression;
visible terminal backfill boundaries (including attachment-only
`file_ids`); and definitive optimistic-row rollback with single-turn
retry. Main null-root behavior, acknowledged in-flight dedupe, and
ambiguous-send retention remain covered.
- Final automated feedback was checked against the supported OpenClaw
v2026.5.7 protocol: `agent` payloads require `runId`, `seq`, `stream`,
`ts`, and nested `data`, so accepting the older identity-free flat
lifecycle shape would break the run fence. Likewise, a non-throwing
`chat.send` result without `runId` is intentionally ambiguous rather
than definitive; it keeps the row/fence and is reconciled by the
same-key stable-reconnect replay. No further code change was warranted.

## Genuine local evidence

Validated with `bash scripts/dev-mock.sh --scenario ready-user` at the
actual printed URL and production routes; the standalone timer demo was
not used. Local ignored captures:

- `.screenshots/v2-chat-activity-main.png` — genuine Main Chat waiting
state after a real send.
- `.screenshots/v2-chat-activity-session.png` — genuine settled Session
Thread route/reply.
- `.screenshots/v2-chat-activity-builder.png` — genuine Agent Builder
waiting state.
- `.screenshots/v2-chat-activity-preview.png` — genuine Agent Preview
waiting state.
- `.screenshots/v2-chat-activity-subagent.png` — genuine interactive
Subagent Chat available state.

The deterministic `ready-user` fixture does not emit Mattermost
`tool_status` or nonterminal assistant segments, so working/preparing
could not be captured visually. Its Subagent Chat send returns no run id
or agent events, so an active subagent state is likewise unavailable.
The focused signal/state tests cover those paths; unavailable
screenshots were not fabricated.

## Scope notes

- Repository size-gate result against current `origin/main`: 4,415
filtered lines (`+4025 / -390`) across 49 files. The full text diff is
6,395 lines (`+6005 / -390`) across 56 files. The final six-finding fix
wave itself is 1,445 lines (`+1179 / -266`) across 32 files from its
fixed base.
- The `size-override` label remains justified because the shared state
adapter, five production surfaces, and focused regression coverage form
one atomic V2 contract.
- No backend API or persisted-data migration.
- No screenshots are tracked.
- `.impeccable.md` predates this V2 implementation on the existing
feature branch and is retained unchanged.
```

### PR Body

## Summary

- Add one shared V2 Chat activity model (`thinking | tool | responding | null`) and neutral presentation for Main Chat, Session Thread, Agent Builder, Agent Preview, and interactive Subagent Chat.
- Derive Mattermost/ACS activity from real `tool_status` and `assistant_segment` events, and derive Gateway activity from `chat.send`, scoped agent/tool/delta events, and terminal lifecycle events.
- Preserve run/session isolation, ignore V1 `custom_turn_status`, and keep replacement-run state safe from late abort confirmations and retired-run events.
- Use exactly three localized global labels, with English fallback:
  - English: `Thinking…`, `Working on the task…`, `Preparing the response…`
  - Chinese: `正在思考…`, `正在执行任务…`, `正在组织回复…`
- Preserve connection-warning priority, read-only/replay suppression, polite live-region semantics, and reduced-motion behavior in both main and compact composers.

## Signal contracts

- Mattermost/ACS: pending, queued, or running `tool_status` events map to working; nonterminal streaming/assistant segments map to preparing; waiting maps to thinking. Final streams, terminal segments/status, and ordinary visible replies are terminal boundaries. Pending ownership is isolated by channel + root/session, including typing events, so one thread cannot show or clear another thread or Main. Tool names and arguments are never shown.
- Gateway: `chat.send` establishes the active run; scoped tool events map to working; assistant deltas map to preparing. A transport-ambiguous send replays on stable reconnect with the same idempotency key before abort/reconciliation. Definitive not-sent/rejected failures remove only their optimistic row and preserve the draft; ambiguous failures remain visibly fenced. Terminal lifecycle, error, confirmed abort, and disconnect paths clear per the implementation. Events from other sessions or runs are ignored.
- Late abort confirmations are attempt- and run-scoped: they cannot clear or otherwise mutate a replacement run.

## Visual treatment

- Neutral `#a1a1aa` text, regular weight, and a white shimmer are shared by all five V2 surfaces.
- The fixed neutral color is an accepted product tradeoff against strict contrast guidance for this transient status text.

## Verification

The branch previously merged `origin/main` at `5b15d93ad`. For fix round 1, `origin/main` was fetched at `ac6581ec`; GitHub CI validates the current merge ref. These local commands passed at the final review-round head:

```bash
cd web/app
pnpm exec vitest run \
  tests/unit/app/chat/chatActivity.unit.spec.ts \
  tests/unit/app/chat/ChatBody.unit.spec.tsx \
  tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx \
  tests/unit/app/agent-builder-client.unit.spec.tsx \
  tests/unit/app/agent-builder-test-chat.unit.spec.tsx \
  tests/unit/app/chat/GenClawInput.unit.spec.tsx \
  tests/unit/app/chat/OpenClawChatSurface.unit.spec.tsx \
  tests/unit/app/chat/useSubagentChat.unit.spec.ts \
  tests/unit/app/chat/SubagentChatPanel.unit.spec.tsx
```

Result: 9 files and 394 tests passed. The complete directly impacted suite passed 13 files and 492 tests.

```bash
cd web/packages/chat-ui
pnpm exec tsc --noEmit
pnpm exec vitest run src/__tests__/chat-composer.test.tsx
pnpm exec eslint src
```

Result: typecheck and lint passed; 1 file and 48 tests passed.

```bash
bash scripts/verify-web.sh \
  web/app/src/lib/chat/chat-activity.ts \
  web/app/src/app/[locale]/\(app\)/\(chat\)/chat \
  web/app/src/app/[locale]/\(app\)/\(chat\)/agent-builder \
  web/packages/chat-ui/src/composer/parts/ComposerNotices.tsx
bash scripts/verify-changed.sh
git diff --check
git diff --check origin/main...HEAD
```

Result: repository guards, TypeScript, 129 files / 1840 tests, ESLint, changed-surface verification, and diff checks passed. ESLint retains one unrelated existing `LandingStartupOverlay.tsx` accessibility warning; the focused Vite runs retain the existing `vite-tsconfig-paths` migration advisory.

## Review follow-up

- The earlier confirmed-abort defect is fixed: exact authoritative abort confirmation releases only the matching direct or deferred attempt, while false, malformed, or rejected responses remain fenced.
- Fix round 1 adds two deferred race regressions for confirmations that arrive after old-run lifecycle end and a replacement send. Temporarily removing the corresponding attempt-identity or run guard made each new test fail; restoring the guards returned the suite to green. The current production implementation was already correct, so this round required test and evidence changes only.
- The final review fix wave addresses all six confirmed Important findings test-first: nonfinal posted stream previews; root/session pending isolation (including `parent_id` typing); stable reconnect replay/reconciliation; successful hidden-Stop activity suppression; visible terminal backfill boundaries (including attachment-only `file_ids`); and definitive optimistic-row rollback with single-turn retry. Main null-root behavior, acknowledged in-flight dedupe, and ambiguous-send retention remain covered.
- Final automated feedback was checked against the supported OpenClaw v2026.5.7 protocol: `agent` payloads require `runId`, `seq`, `stream`, `ts`, and nested `data`, so accepting the older identity-free flat lifecycle shape would break the run fence. Likewise, a non-throwing `chat.send` result without `runId` is intentionally ambiguous rather than definitive; it keeps the row/fence and is reconciled by the same-key stable-reconnect replay. No further code change was warranted.

## Genuine local evidence

Validated with `bash scripts/dev-mock.sh --scenario ready-user` at the actual printed URL and production routes; the standalone timer demo was not used. Local ignored captures:

- `.screenshots/v2-chat-activity-main.png` — genuine Main Chat waiting state after a real send.
- `.screenshots/v2-chat-activity-session.png` — genuine settled Session Thread route/reply.
- `.screenshots/v2-chat-activity-builder.png` — genuine Agent Builder waiting state.
- `.screenshots/v2-chat-activity-preview.png` — genuine Agent Preview waiting state.
- `.screenshots/v2-chat-activity-subagent.png` — genuine interactive Subagent Chat available state.

The deterministic `ready-user` fixture does not emit Mattermost `tool_status` or nonterminal assistant segments, so working/preparing could not be captured visually. Its Subagent Chat send returns no run id or agent events, so an active subagent state is likewise unavailable. The focused signal/state tests cover those paths; unavailable screenshots were not fabricated.

## Scope notes

- Repository size-gate result against current `origin/main`: 4,415 filtered lines (`+4025 / -390`) across 49 files. The full text diff is 6,395 lines (`+6005 / -390`) across 56 files. The final six-finding fix wave itself is 1,445 lines (`+1179 / -266`) across 32 files from its fixed base.
- The `size-override` label remains justified because the shared state adapter, five production surfaces, and focused regression coverage form one atomic V2 contract.
- No backend API or persisted-data migration.
- No screenshots are tracked.
- `.impeccable.md` predates this V2 implementation on the existing feature branch and is retained unchanged.

