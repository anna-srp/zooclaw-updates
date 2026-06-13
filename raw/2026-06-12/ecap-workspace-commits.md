# ecap-workspace — commits 2026-06-12

共 22 个 commits（since 2026-06-12T00:00:00Z）

---

## refactor(web): unify artifact renderer dispatch and split oversized preview components (#2417)

- **SHA**: `ba6c5f9a761461787e0e03ccde6c7e24b620b4f2`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-12T17:17:18Z
- **PR**: #2417

### 完整 commit message

```
refactor(web): unify artifact renderer dispatch and split oversized preview components (#2417)

## Description

Maintainability refactor of the artifact sidebar / file-preview system.
Design spec:
`docs/superpowers/specs/2026-06-13-artifact-preview-refactor-design.md`
(included in this PR).

**Zero user-visible behavior change**, except the aspect-ratio menu now
closes via Radix (`ds/DropdownMenu`) instead of a hand-rolled
`mousedown` listener — interaction is equivalent (click outside / Esc).

### What changed

1. **Single renderer dispatch** — new `renderers/ArtifactRenderer.tsx`
replaces the two divergent `renderByExt` copies in `ArtifactPreview.tsx`
(53-branch switch) and `AssetPreviewArea.tsx`. Lazy-loading strategy
unified (heavy renderers — xlsx/docx/pptx/mermaid — stay behind
`next/dynamic`; light renderers static). Adding a new code-language ext
no longer touches any switch.
2. **`ArtifactPreview.tsx` 513 → 161 lines** — split into pure-UI
`ArtifactPreviewHeader` / `PreviewBody` / `FileAvailabilityGate` /
`PreviewStatusPanes`; all state and callbacks stay in the container.
Hand-rolled aspect-ratio popover (`useRef` + `useOnClickOutside` + open
state) migrated to ds `DropdownMenu`, matching the PDF-download menu in
the same header (shadcn-first rule).
3. **`MMAttachments.tsx` 476 → 70 lines** — per-type files under
`mattermost/attachments/`; shared `VideoCard` removes the line-for-line
chat/replay video duplication; `ScrollableImageRow` takes `renderItem`
to avoid a leaf→entry import cycle. All `data-testid`s preserved.
4. **`extractFileLinks` dedup** — the four-times-repeated eligibility
filter collapsed into one `toPreviewFile` helper (`types.unit.spec.ts`
passes unchanged).
5. **Mock backend: chat-replay fixtures** — `scripts/mock-backend.mjs`
now serves a replay snapshot + attachment bytes so the public
`/share/{shareId}` page exercises the whole preview chain locally (no
Mattermost / staging credentials needed).

### Out of scope (deliberate)
`ImagePreview`/`ImagePreviewProvider`/`ProgressiveImage` (single
implementation, fully tested, no duplication), `pptx-parser.ts`,
`useArtifactsSidebar` reducer architecture.

## Test Plan

- [x] `pnpm tsc --noEmit` — 0 errors
- [x] `pnpm test:unit` — **513/513 test files pass**; `MMAttachments` /
`types` specs pass with zero changes; `AssetPreviewArea` spec migrated
from whole-`next/dynamic` marker to per-renderer module stubs (strictly
stronger assertions); hand-rolled-popover close assertion replaced by an
Auto-reset contract test (open/close now owned by Radix)
- [x] `pnpm lint` / `lint:imports` / `lint:deadcode` — clean
- [x] `pnpm dup:src` — 3.48% (threshold 4.5%), duplication reduced
- [x] **Browser validation** (local frontend + staging public config +
mock backend, public `/share/{shareId}` replay page): image attachments
render and open the ImagePreview lightbox; shared `VideoCard` + audio
cards render; clicking the `report.md` / `script.py` file cards opens
the artifacts sidebar through the full refactored chain
(ArtifactPreviewHeader → FileAvailabilityGate → ArtifactRenderer →
MarkdownRenderer / CodeRenderer with shiki); the source-toggle appears
only for `SOURCE_VIEWABLE` exts; Close tears the panel down; 0 console
errors from the refactored code (one pre-existing availability-HEAD 401
on the BFF proxy path — documented short-circuit-to-ready behavior in
`useArtifactAvailability`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR description

## Description

Maintainability refactor of the artifact sidebar / file-preview system. Design spec: `docs/superpowers/specs/2026-06-13-artifact-preview-refactor-design.md` (included in this PR).

**Zero user-visible behavior change**, except the aspect-ratio menu now closes via Radix (`ds/DropdownMenu`) instead of a hand-rolled `mousedown` listener — interaction is equivalent (click outside / Esc).

### What changed

1. **Single renderer dispatch** — new `renderers/ArtifactRenderer.tsx` replaces the two divergent `renderByExt` copies in `ArtifactPreview.tsx` (53-branch switch) and `AssetPreviewArea.tsx`. Lazy-loading strategy unified (heavy renderers — xlsx/docx/pptx/mermaid — stay behind `next/dynamic`; light renderers static). Adding a new code-language ext no longer touches any switch.
2. **`ArtifactPreview.tsx` 513 → 161 lines** — split into pure-UI `ArtifactPreviewHeader` / `PreviewBody` / `FileAvailabilityGate` / `PreviewStatusPanes`; all state and callbacks stay in the container. Hand-rolled aspect-ratio popover (`useRef` + `useOnClickOutside` + open state) migrated to ds `DropdownMenu`, matching the PDF-download menu in the same header (shadcn-first rule).
3. **`MMAttachments.tsx` 476 → 70 lines** — per-type files under `mattermost/attachments/`; shared `VideoCard` removes the line-for-line chat/replay video duplication; `ScrollableImageRow` takes `renderItem` to avoid a leaf→entry import cycle. All `data-testid`s preserved.
4. **`extractFileLinks` dedup** — the four-times-repeated eligibility filter collapsed into one `toPreviewFile` helper (`types.unit.spec.ts` passes unchanged).
5. **Mock backend: chat-replay fixtures** — `scripts/mock-backend.mjs` now serves a replay snapshot + attachment bytes so the public `/share/{shareId}` page exercises the whole preview chain locally (no Mattermost / staging credentials needed).

### Out of scope (deliberate)
`ImagePreview`/`ImagePreviewProvider`/`ProgressiveImage` (single implementation, fully tested, no duplication), `pptx-parser.ts`, `useArtifactsSidebar` reducer architecture.

## Test Plan

- [x] `pnpm tsc --noEmit` — 0 errors
- [x] `pnpm test:unit` — **513/513 test files pass**; `MMAttachments` / `types` specs pass with zero changes; `AssetPreviewArea` spec migrated from whole-`next/dynamic` marker to per-renderer module stubs (strictly stronger assertions); hand-rolled-popover close assertion replaced by an Auto-reset contract test (open/close now owned by Radix)
- [x] `pnpm lint` / `lint:imports` / `lint:deadcode` — clean
- [x] `pnpm dup:src` — 3.48% (threshold 4.5%), duplication reduced
- [x] **Browser validation** (local frontend + staging public config + mock backend, public `/share/{shareId}` replay page): image attachments render and open the ImagePreview lightbox; shared `VideoCard` + audio cards render; clicking the `report.md` / `script.py` file cards opens the artifacts sidebar through the full refactored chain (ArtifactPreviewHeader → FileAvailabilityGate → ArtifactRenderer → MarkdownRenderer / CodeRenderer with shiki); the source-toggle appears only for `SOURCE_VIEWABLE` exts; Close tears the panel down; 0 console errors from the refactored code (one pre-existing availability-HEAD 401 on the BFF proxy path — documented short-circuit-to-ready behavior in `useArtifactAvailability`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## chore(web): instrument per-message response latency (Sentry Logs) (#2415)

- **SHA**: `899eb08a752175152df9c09707f49b82fd0a4ee6`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-12T14:34:35Z
- **PR**: #2415

### 完整 commit message

```
chore(web): instrument per-message response latency (Sentry Logs) (#2415)

## Summary

Per-message frontend response-latency instrumentation (monitoring only,
no chat behavior change), to quantify the recurring "after I send a
message I don't get a reply quickly" report. Sibling to the
connection-status instrumentation (#2413), reusing the same Sentry-Logs
conventions.

Single Sentry Logs stream `chat.message.response_latency` with a `phase`
attribute, so Sentry Explore can query `p50/p75/p90/p95(latency_ms)` and
the slow/never-replied ratio:

- **ack latency** (`phase:ack`) — send → bot emoji-ack reaction on the
user's post
- **reply-content latency** (`phase:reply_content`) — send → first
non-empty bot reply post arrives
- **timeout records** (`phase:ack_timeout` / `reply_timeout`) — emitted
when nothing arrives within 2 min, so "too slow / never replied" is
itself a ratio metric

### Design
- New `lib/sentry/message-latency-monitor.ts`: `pending` (by sent post
id, ack correlation) + `latestByChannel` (reply correlation) maps;
one-shot per-send 2-min timeout drives the timeout records.
- **Observation at the WS layer** (`useMattermost` `dispatchEvent` /
`handlePostedEvent`) because reply/ack correlation is
channel/thread-global and outlives the component — component-scoped
`onPost` would drop a reply after a channel switch. The **send** is
recorded from the chat components.
- Shared `lib/mattermost/reactions.ts` `parseReactionEvent` used by both
the post store and the monitor.
- `sendMessage` now returns the sent `MMPost` for ack correlation.
- Both timestamps use **client `Date.now()`** (never the server
`create_at`, a different clock).

### Anti-storm / performance
- Sentry Logs (separate byte quota, no issues/alerts).
- First-event latching: ≤1 ack + ≤1 reply per message; no time-dedup on
latency values (would break percentiles).
- O(1) WS-layer observation, no React/renders/new subscriptions; bounded
maps; kill switch `NEXT_PUBLIC_MESSAGE_LATENCY_LOGS=off`.

Scope: main chat + session thread (Mattermost). Subagent SSE is Phase 2.

Spec:
`docs/superpowers/specs/2026-06-13-message-response-latency-instrumentation.md`
Dashboard: Sentry "Chat Response Latency"
(serendipity-one-inc/ecap-website, id 6976829)

## Test plan
- [x] `pnpm test:unit` (513 files / 7226 pass) — new monitor + reactions
specs, plus wiring assertions in useMattermost / useChatMessaging /
SessionThreadClient
- [x] `tsc --noEmit`, `eslint`, `knip` (lint:deadcode), `pnpm dup` all
clean
- [ ] Post-deploy: confirm `chat.message.response_latency` lands in
Sentry Explore (logs dataset) and percentiles aggregate

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR description

## Summary

Per-message frontend response-latency instrumentation (monitoring only, no chat behavior change), to quantify the recurring "after I send a message I don't get a reply quickly" report. Sibling to the connection-status instrumentation (#2413), reusing the same Sentry-Logs conventions.

Single Sentry Logs stream `chat.message.response_latency` with a `phase` attribute, so Sentry Explore can query `p50/p75/p90/p95(latency_ms)` and the slow/never-replied ratio:

- **ack latency** (`phase:ack`) — send → bot emoji-ack reaction on the user's post
- **reply-content latency** (`phase:reply_content`) — send → first non-empty bot reply post arrives
- **timeout records** (`phase:ack_timeout` / `reply_timeout`) — emitted when nothing arrives within 2 min, so "too slow / never replied" is itself a ratio metric

### Design
- New `lib/sentry/message-latency-monitor.ts`: `pending` (by sent post id, ack correlation) + `latestByChannel` (reply correlation) maps; one-shot per-send 2-min timeout drives the timeout records.
- **Observation at the WS layer** (`useMattermost` `dispatchEvent` / `handlePostedEvent`) because reply/ack correlation is channel/thread-global and outlives the component — component-scoped `onPost` would drop a reply after a channel switch. The **send** is recorded from the chat components.
- Shared `lib/mattermost/reactions.ts` `parseReactionEvent` used by both the post store and the monitor.
- `sendMessage` now returns the sent `MMPost` for ack correlation.
- Both timestamps use **client `Date.now()`** (never the server `create_at`, a different clock).

### Anti-storm / performance
- Sentry Logs (separate byte quota, no issues/alerts).
- First-event latching: ≤1 ack + ≤1 reply per message; no time-dedup on latency values (would break percentiles).
- O(1) WS-layer observation, no React/renders/new subscriptions; bounded maps; kill switch `NEXT_PUBLIC_MESSAGE_LATENCY_LOGS=off`.

Scope: main chat + session thread (Mattermost). Subagent SSE is Phase 2.

Spec: `docs/superpowers/specs/2026-06-13-message-response-latency-instrumentation.md`
Dashboard: Sentry "Chat Response Latency" (serendipity-one-inc/ecap-website, id 6976829)

## Test plan
- [x] `pnpm test:unit` (513 files / 7226 pass) — new monitor + reactions specs, plus wiring assertions in useMattermost / useChatMessaging / SessionThreadClient
- [x] `tsc --noEmit`, `eslint`, `knip` (lint:deadcode), `pnpm dup` all clean
- [ ] Post-deploy: confirm `chat.message.response_latency` lands in Sentry Explore (logs dataset) and percentiles aggregate

---

## feat(web): add Sentry Logs instrumentation for connection-status mismatch monitoring (#2413)

- **SHA**: `e7d3ac1c6de1bb5ff3601a7e2cf77386fd35557e`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-12T13:31:55Z
- **PR**: #2413

### 完整 commit message

```
feat(web): add Sentry Logs instrumentation for connection-status mismatch monitoring (#2413)

## Linear

https://linear.app/srpone/issue/ECA-987/sentry-监控量化连接状态显示-reconnecting-但消息实际可收发的用户影响面

## Summary
- 监控先行（不修复行为）：量化「连接状态 pill / 全屏视图显示
connecting/reconnecting，但消息实际可收发」的真实影响面——每日次数、独立用户数、占活跃聊天用户比例，并把每次
mismatch 归因到机制（`platform_not_ready` / `grace_window` / `mm_ws_degraded`
/ `ws_stuck_reconnecting`），用数据验证 #2364 的根因主张后再决定其去留
- 新增 `lib/sentry/connection-status-recorder.ts`：模块级快照记录 pill
**实际显示**的状态（post-grace、post-override 的 `effectiveStatus` + 全部原始输入）；pill
卸载即清空，防跨路由污染。纯模块赋值，无新增 React 状态/渲染，性能影响可忽略
- 新增 `lib/sentry/connection-mismatch-monitor.ts`（仓库首个 `Sentry.logger`
使用，logs 与 error events 配额分池、不产 issue、不触发告警）：
- `chat.send.outcome`（info，每次发送成功，无去重）——分母流，带 `status_mismatch`
属性，分子分母同源
- `chat.connection.status_mismatch`（warn，60s/会话/机制/proof 去重）——分子 +
归因，proof-of-life = 发送成功或 bot 回复到达
- `mm.connection.transition`（→connected info / 异常 warn 60s 去重）——MM
连接异常次数/人数/占比，`→connected` 兼当「当天打开过聊天」分母
- 接线 5 处：`ClawConnectionStatus`（recorder
写入）、`ChatGateStates`（`WsRecoveryView`/`MmConnectingSpinner`
挂载记录）、`useChatMessaging`（发送成功 + `mm.onPost` bot
回复）、`SessionThreadClient`（thread
发送）、`useMattermostConnection`（状态转换，刻意断开不记）
- Kill switch：`NEXT_PUBLIC_CONN_MISMATCH_LOGS=off` 一键全关；**#1154 的
transient 降级（breadcrumb-only）原样保留，本 PR 是并行统计通道**
- 设计
spec：`docs/superpowers/specs/2026-06-12-connection-status-mismatch-instrumentation.md`（含查询定义、机制归因表、#2364
决策规则：基线 3-5 天，`platform_not_ready` ≥70% 且 post-fix 降 >90% 才算归因成立）

## Test plan
- [x] `pnpm test:unit` 全量 7184 passed（510 files）：recorder 快照/降级时长/gate
view、归因优先级、去重正反例、kill switch、MM transition 回填、pill→recorder 组件级（含
`platformReady=false` 强制 reconnecting 的 #2364 场景）、useChatMessaging
发送成功/失败与 bot_reply 订阅/退订
- [x] `npx tsc --noEmit` / 触达文件 eslint / `pnpm dup` 全过
- [ ] staging 部署后 Sentry Explore → Logs 验证三条流入库、`count_unique(user_id)`
可聚合（合并后执行）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
Co-authored-by: claude[bot] <41898282+claude[bot]@users.noreply.github.com>
Co-authored-by: Chris@ZooClaw <undefined@users.noreply.github.com>
```

### PR description

## Linear
https://linear.app/srpone/issue/ECA-987/sentry-监控量化连接状态显示-reconnecting-但消息实际可收发的用户影响面

## Summary
- 监控先行（不修复行为）：量化「连接状态 pill / 全屏视图显示 connecting/reconnecting，但消息实际可收发」的真实影响面——每日次数、独立用户数、占活跃聊天用户比例，并把每次 mismatch 归因到机制（`platform_not_ready` / `grace_window` / `mm_ws_degraded` / `ws_stuck_reconnecting`），用数据验证 #2364 的根因主张后再决定其去留
- 新增 `lib/sentry/connection-status-recorder.ts`：模块级快照记录 pill **实际显示**的状态（post-grace、post-override 的 `effectiveStatus` + 全部原始输入）；pill 卸载即清空，防跨路由污染。纯模块赋值，无新增 React 状态/渲染，性能影响可忽略
- 新增 `lib/sentry/connection-mismatch-monitor.ts`（仓库首个 `Sentry.logger` 使用，logs 与 error events 配额分池、不产 issue、不触发告警）：
  - `chat.send.outcome`（info，每次发送成功，无去重）——分母流，带 `status_mismatch` 属性，分子分母同源
  - `chat.connection.status_mismatch`（warn，60s/会话/机制/proof 去重）——分子 + 归因，proof-of-life = 发送成功或 bot 回复到达
  - `mm.connection.transition`（→connected info / 异常 warn 60s 去重）——MM 连接异常次数/人数/占比，`→connected` 兼当「当天打开过聊天」分母
- 接线 5 处：`ClawConnectionStatus`（recorder 写入）、`ChatGateStates`（`WsRecoveryView`/`MmConnectingSpinner` 挂载记录）、`useChatMessaging`（发送成功 + `mm.onPost` bot 回复）、`SessionThreadClient`（thread 发送）、`useMattermostConnection`（状态转换，刻意断开不记）
- Kill switch：`NEXT_PUBLIC_CONN_MISMATCH_LOGS=off` 一键全关；**#1154 的 transient 降级（breadcrumb-only）原样保留，本 PR 是并行统计通道**
- 设计 spec：`docs/superpowers/specs/2026-06-12-connection-status-mismatch-instrumentation.md`（含查询定义、机制归因表、#2364 决策规则：基线 3-5 天，`platform_not_ready` ≥70% 且 post-fix 降 >90% 才算归因成立）

## Test plan
- [x] `pnpm test:unit` 全量 7184 passed（510 files）：recorder 快照/降级时长/gate view、归因优先级、去重正反例、kill switch、MM transition 回填、pill→recorder 组件级（含 `platformReady=false` 强制 reconnecting 的 #2364 场景）、useChatMessaging 发送成功/失败与 bot_reply 订阅/退订
- [x] `npx tsc --noEmit` / 触达文件 eslint / `pnpm dup` 全过
- [ ] staging 部署后 Sentry Explore → Logs 验证三条流入库、`count_unique(user_id)` 可聚合（合并后执行）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## docs(specs): add managed agent partner API design spec (#2410)

- **SHA**: `1ebe1e03e98d2a837725fc805eaa74b4ebfd3f03`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-12T08:59:06Z
- **PR**: #2410

### 完整 commit message

```
docs(specs): add managed agent partner API design spec (#2410)

## Summary
- 新增
`docs/superpowers/specs/2026-06-12-managed-agent-partner-api-design.md`：合作伙伴通过
API 接入 Zooclaw Agent Runtime（B2B2C）的设计文档，经多轮需求澄清收敛
- 核心结论：伙伴 = team org（复用 Enterprise V1，不引入独立 partner 层）；终端用户 =
影子账号（managed member）；每任务一个 pod 实例 + Pack 构建期烘焙镜像；resume = 复活原
botID；task-scoped 文件 API（封装既有 JuiceFS S3 gateway）；org 钱包 + user quota
- 附带：按仓库的改造清单（8 仓库）、14 项风险/验证项（4 项需试点前 PoC）、工作量预估（开发按 AI 辅助 3 折：约 10–12
人周，内部交付承诺 5.5 周）与并行工作流资源分析、对原 `zooclaw-managed-agent-spec.md` 的逐条追溯表
- 文档同时修正了原 spec 的过时前提（「没有 org/RBAC」——Enterprise V1 已落地）

## Test plan
- [ ] 纯文档变更，无代码改动；review 设计内容即可（重点：§1 待定项、§6 高风险验证项、§8 两个 open question）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR description

## Summary
- 新增 `docs/superpowers/specs/2026-06-12-managed-agent-partner-api-design.md`：合作伙伴通过 API 接入 Zooclaw Agent Runtime（B2B2C）的设计文档，经多轮需求澄清收敛
- 核心结论：伙伴 = team org（复用 Enterprise V1，不引入独立 partner 层）；终端用户 = 影子账号（managed member）；每任务一个 pod 实例 + Pack 构建期烘焙镜像；resume = 复活原 botID；task-scoped 文件 API（封装既有 JuiceFS S3 gateway）；org 钱包 + user quota
- 附带：按仓库的改造清单（8 仓库）、14 项风险/验证项（4 项需试点前 PoC）、工作量预估（开发按 AI 辅助 3 折：约 10–12 人周，内部交付承诺 5.5 周）与并行工作流资源分析、对原 `zooclaw-managed-agent-spec.md` 的逐条追溯表
- 文档同时修正了原 spec 的过时前提（「没有 org/RBAC」——Enterprise V1 已落地）

## Test plan
- [ ] 纯文档变更，无代码改动；review 设计内容即可（重点：§1 待定项、§6 高风险验证项、§8 两个 open question）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(openclaw-ws): accept protocol range [3,4] for openclaw 2026.6.5 (WS protocol v4) (#2409)

- **SHA**: `ba123b64b54577e4c29b6822c1b947ccdba21a65`
- **作者**: allenz-srp
- **日期**: 2026-06-12T08:39:14Z
- **PR**: #2409

### 完整 commit message

```
fix(openclaw-ws): accept protocol range [3,4] for openclaw 2026.6.5 (WS protocol v4) (#2409)

## Problem

openclaw 2026.6.5 (staging canary track) bumps the gateway WS protocol 3
→ 4 and **hard-rejects pure-v3 clients** — no compat window
(`maxProtocol >= 4 && minProtocol <= 4`). Our WS clients hardcode
`min=max=3`, so webchat/control-ui against 6.5 bots is fully broken,
surfacing as the generic "Something went wrong":

- bot `a8c4d697`: 47+ `protocol mismatch ... expected 4` in 2h
- bot `046db9e1`: 1267 rejected connections in 4h

## Fix

Advertise **`minProtocol: 3, maxProtocol: 4`** in both WS clients:
- `web/app/src/hooks/useOpenClawWebSocket.ts` (webchat / control-ui)
- `desktop/main/openclaw/bridge.ts` (desktop node-host bridge — same
latent defect)

Verified against both runtime packages' handshake validation that one
range-client passes both: 2026.5.7 checks `max>=3 && min<=3` (negotiates
3), 2026.6.5 checks `max>=4 && min<=4` (negotiates 4). The v4
`ConnectParams` schema is shape-compatible with the frames we already
send (checked against `packages/gateway-protocol/src/schema/frames.ts`
in the 2026.6.5 dist).

## Validation

- [ ] Webchat against a 6.5 staging canary bot (a8c4d697 / f7b48e07) —
connects, chat history loads, messages stream
- [ ] Webchat against a 5.7 bot — no regression (negotiates 3)
- [ ] v4 negotiated session: verify event-stream handling end-to-end
(protocol bump may carry frame-semantics changes beyond the handshake)

Companion fixes: backend WSS client SerendipityOneInc/fastclaw#124;
feishu dispatch crash SerendipityOneInc/openclaw-docker#135.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR description

## Problem

openclaw 2026.6.5 (staging canary track) bumps the gateway WS protocol 3 → 4 and **hard-rejects pure-v3 clients** — no compat window (`maxProtocol >= 4 && minProtocol <= 4`). Our WS clients hardcode `min=max=3`, so webchat/control-ui against 6.5 bots is fully broken, surfacing as the generic "Something went wrong":

- bot `a8c4d697`: 47+ `protocol mismatch ... expected 4` in 2h
- bot `046db9e1`: 1267 rejected connections in 4h

## Fix

Advertise **`minProtocol: 3, maxProtocol: 4`** in both WS clients:
- `web/app/src/hooks/useOpenClawWebSocket.ts` (webchat / control-ui)
- `desktop/main/openclaw/bridge.ts` (desktop node-host bridge — same latent defect)

Verified against both runtime packages' handshake validation that one range-client passes both: 2026.5.7 checks `max>=3 && min<=3` (negotiates 3), 2026.6.5 checks `max>=4 && min<=4` (negotiates 4). The v4 `ConnectParams` schema is shape-compatible with the frames we already send (checked against `packages/gateway-protocol/src/schema/frames.ts` in the 2026.6.5 dist).

## Validation

- [ ] Webchat against a 6.5 staging canary bot (a8c4d697 / f7b48e07) — connects, chat history loads, messages stream
- [ ] Webchat against a 5.7 bot — no regression (negotiates 3)
- [ ] v4 negotiated session: verify event-stream handling end-to-end (protocol bump may carry frame-semantics changes beyond the handshake)

Companion fixes: backend WSS client SerendipityOneInc/fastclaw#124; feishu dispatch crash SerendipityOneInc/openclaw-docker#135.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): migrate hand-rolled DOM listeners to usehooks-ts (#2403)

- **SHA**: `ea3162288c14268495c08215bd17bfe0eb82fbbb`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-12T08:35:10Z
- **PR**: #2403

### 完整 commit message

```
refactor(web): migrate hand-rolled DOM listeners to usehooks-ts (#2403)

## Summary
- 按项目技术选型规范（web/app/CLAUDE.md → "DOM / 浏览器 API hook → usehooks-ts"），把 14
个文件里手写的 `useEffect + addEventListener/removeEventListener` 迁移到
`useEventListener` / `useOnClickOutside` / `useEscapeKey`，消除手写 cleanup
样板并统一 handler-in-ref 语义（监听器只挂一次，闭包始终读最新值）
- **Landing**：滚动逻辑抽成 `hooks/useLandingScrollState`（header compact +
mobile CTA）和 `hooks/useLandingParallax`（视差），符合 landing CLAUDE.md "新逻辑抽
hook" 约定（LandingClient 受 6 条 complexity 规则约束）。`scroll` 监听去掉了 `{ passive:
true }`——scroll 事件不可取消，该 hint 是 no-op，且 inline options 对象会让
useEventListener 每次 render 重挂监听
- **UserMenu**：`useOnClickOutside([menuRef, containerRef]) +
useEscapeKey`。原 `setTimeout(0)` 延迟挂载不再需要：监听器常挂但 handler 有 `isOpen`
guard（开菜单的 mousedown 发生在 `isOpen` 仍为 false 时），开关按钮命中被排除的 `containerRef`
- **PublicHeader / PublicFooter**：保持 `click` phase 的 outside-close
语义（useOnClickOutside 只支持 mousedown/touch 系），用 documentRef +
`useEventListener('click')`，hamburger 选择器排除逻辑原样保留
- **useModalStackEscape**：直接建立在项目 `useEscapeKey` 之上，删掉手写的 `stackRef`
模式（useEventListener 内部就是这个机制）
- 其余：OpenClawThread 滚动按钮 / useAgentScrollOverlay（element ref overload）/
useAuthBootstrap + useCustomAgentPublishes（storage 跨 tab 同步）/
useFeedbackBootstrap（error/unhandledrejection）/
useResponsiveLayout（resize）/ LoginForm（pageshow）/ PublicPricingClient +
UserGuideClient（scroll/委托点击）

## 有意不迁移（避免行为漂移）
- `useResizable`：监听器仅在拖拽期间挂载，常挂 window mousemove 会让每次鼠标移动都进 handler
- `MarkdownContent`：NodeList 多元素监听 + 随内容重渲染重挂，不映射到 useEventListener
- `useOpenClawWebSocket` /
`useOpenClawVisibilityRecovery`：监听器卸载与连接/定时器生命周期清理交织
- `WelcomeRewardToast` / `useJSBridge` / `TurnstileWidget` /
`chip-elements`：自定义事件名（不在 EventMap）或非 React 生命周期的命令式代码

## Test plan
- [x] 全量单测 507 files / 7151 passed；`pnpm lint` / `tsc --noEmit` / `pnpm
lint:ci` / `pnpm dup` 全绿
- [x] 测试契约更新：UserMenu "closed 时无监听器" 改为行为断言（closed 菜单对外部
mousedown/Escape 无反应——挂载机制是实现细节）；2 个 resize teardown 断言接受
useEventListener 透传的 undefined options 第三参
- [x] 本地 dev:staging（mock-backend 配方）+ Playwright 实测：landing header
compact + parallax translateY ✓；userguide scroll-spy 激活 + FAQ 手风琴委托点击
✓；pricing header compact ✓；footer 语言菜单外点关闭 ✓；UserMenu 开/外点关/Escape 关（含
toggle-click 不误关）✓；375px resize 出现 mobile-menu-toggle ✓；console 无新增错误

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR description

## Summary
- 按项目技术选型规范（web/app/CLAUDE.md → "DOM / 浏览器 API hook → usehooks-ts"），把 14 个文件里手写的 `useEffect + addEventListener/removeEventListener` 迁移到 `useEventListener` / `useOnClickOutside` / `useEscapeKey`，消除手写 cleanup 样板并统一 handler-in-ref 语义（监听器只挂一次，闭包始终读最新值）
- **Landing**：滚动逻辑抽成 `hooks/useLandingScrollState`（header compact + mobile CTA）和 `hooks/useLandingParallax`（视差），符合 landing CLAUDE.md "新逻辑抽 hook" 约定（LandingClient 受 6 条 complexity 规则约束）。`scroll` 监听去掉了 `{ passive: true }`——scroll 事件不可取消，该 hint 是 no-op，且 inline options 对象会让 useEventListener 每次 render 重挂监听
- **UserMenu**：`useOnClickOutside([menuRef, containerRef]) + useEscapeKey`。原 `setTimeout(0)` 延迟挂载不再需要：监听器常挂但 handler 有 `isOpen` guard（开菜单的 mousedown 发生在 `isOpen` 仍为 false 时），开关按钮命中被排除的 `containerRef`
- **PublicHeader / PublicFooter**：保持 `click` phase 的 outside-close 语义（useOnClickOutside 只支持 mousedown/touch 系），用 documentRef + `useEventListener('click')`，hamburger 选择器排除逻辑原样保留
- **useModalStackEscape**：直接建立在项目 `useEscapeKey` 之上，删掉手写的 `stackRef` 模式（useEventListener 内部就是这个机制）
- 其余：OpenClawThread 滚动按钮 / useAgentScrollOverlay（element ref overload）/ useAuthBootstrap + useCustomAgentPublishes（storage 跨 tab 同步）/ useFeedbackBootstrap（error/unhandledrejection）/ useResponsiveLayout（resize）/ LoginForm（pageshow）/ PublicPricingClient + UserGuideClient（scroll/委托点击）

## 有意不迁移（避免行为漂移）
- `useResizable`：监听器仅在拖拽期间挂载，常挂 window mousemove 会让每次鼠标移动都进 handler
- `MarkdownContent`：NodeList 多元素监听 + 随内容重渲染重挂，不映射到 useEventListener
- `useOpenClawWebSocket` / `useOpenClawVisibilityRecovery`：监听器卸载与连接/定时器生命周期清理交织
- `WelcomeRewardToast` / `useJSBridge` / `TurnstileWidget` / `chip-elements`：自定义事件名（不在 EventMap）或非 React 生命周期的命令式代码

## Test plan
- [x] 全量单测 507 files / 7151 passed；`pnpm lint` / `tsc --noEmit` / `pnpm lint:ci` / `pnpm dup` 全绿
- [x] 测试契约更新：UserMenu "closed 时无监听器" 改为行为断言（closed 菜单对外部 mousedown/Escape 无反应——挂载机制是实现细节）；2 个 resize teardown 断言接受 useEventListener 透传的 undefined options 第三参
- [x] 本地 dev:staging（mock-backend 配方）+ Playwright 实测：landing header compact + parallax translateY ✓；userguide scroll-spy 激活 + FAQ 手风琴委托点击 ✓；pricing header compact ✓；footer 语言菜单外点关闭 ✓；UserMenu 开/外点关/Escape 关（含 toggle-click 不误关）✓；375px resize 出现 mobile-menu-toggle ✓；console 无新增错误

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(agent-packs): add submission reject flow and deprecated pack restore (#2406)

- **SHA**: `adb465f0eee693502b649beccef0ae53e651cf39`
- **作者**: bill-srp
- **日期**: 2026-06-12T08:19:23Z
- **PR**: #2406

### 完整 commit message

```
feat(agent-packs): add submission reject flow and deprecated pack restore (#2406)

## Linear

https://linear.app/srpone/issue/ECA-886/agent-pack-admin-dashboard-webdashboard

## Summary

Backend (`services/claw-interface`):
- Add `POST /agent-packs/{pack_id}/submissions/{submission_id}/reject` —
admin-gated review rejection with optional `review_notes` (new
`InternalPackSubmissionRejectRequest` schema).
- Add `POST /agent-packs/{pack_id}/enable` — restore a deprecated pack
to `active`; CAS-guarded repo update (`status: "deprecated"` filter)
with `pack.not_deprecated` conflict error, mirroring the existing
deprecate flow.

Dashboard console (`web/dashboard-console`):
- Submissions review dialog gains a reject flow with review notes
alongside approve.
- Pack table gains a restore action for deprecated packs, with confirm
popovers for both restore and deprecate (shared `ConfirmPopover`, single
confirm-state).
- Split the agent-packs route into focused components (`pack-table`,
`pack-dialog`, `editor-dialog`, `stat-strip`, `status-filter-bar`,
`backend-offline-notice`) with co-located view-model hooks; canonicalize
arbitrary Tailwind values to scale utilities.
- Dedupe pure transforms in `lib/packs.ts` (shared status transition +
review-stamp helpers).

## Test plan
- [x] `web/dashboard-console`: vitest 192/192, `tsc -b`, eslint — all
pass
- [x] `services/claw-interface`: ruff check + format, pyright (0 errors)
- [x] `services/claw-interface`: full pytest suite in devcontainer image
with Mongo sidecar — 4881 passed, whole-app coverage 90.00% (gate: 90%)
- [x] New endpoints covered by unit tests
(`test_internal_agent_packs_routes`, `test_pack_repo`,
`test_pack_services`); UI flows covered by route/view-model tests
```

### PR description

## Linear
https://linear.app/srpone/issue/ECA-886/agent-pack-admin-dashboard-webdashboard

## Summary

Backend (`services/claw-interface`):
- Add `POST /agent-packs/{pack_id}/submissions/{submission_id}/reject` — admin-gated review rejection with optional `review_notes` (new `InternalPackSubmissionRejectRequest` schema).
- Add `POST /agent-packs/{pack_id}/enable` — restore a deprecated pack to `active`; CAS-guarded repo update (`status: "deprecated"` filter) with `pack.not_deprecated` conflict error, mirroring the existing deprecate flow.

Dashboard console (`web/dashboard-console`):
- Submissions review dialog gains a reject flow with review notes alongside approve.
- Pack table gains a restore action for deprecated packs, with confirm popovers for both restore and deprecate (shared `ConfirmPopover`, single confirm-state).
- Split the agent-packs route into focused components (`pack-table`, `pack-dialog`, `editor-dialog`, `stat-strip`, `status-filter-bar`, `backend-offline-notice`) with co-located view-model hooks; canonicalize arbitrary Tailwind values to scale utilities.
- Dedupe pure transforms in `lib/packs.ts` (shared status transition + review-stamp helpers).

## Test plan
- [x] `web/dashboard-console`: vitest 192/192, `tsc -b`, eslint — all pass
- [x] `services/claw-interface`: ruff check + format, pyright (0 errors)
- [x] `services/claw-interface`: full pytest suite in devcontainer image with Mongo sidecar — 4881 passed, whole-app coverage 90.00% (gate: 90%)
- [x] New endpoints covered by unit tests (`test_internal_agent_packs_routes`, `test_pack_repo`, `test_pack_services`); UI flows covered by route/view-model tests

---

## test(e2e): stabilize scenario smoke tests (#2408)

- **SHA**: `c016f300a56ab3a791622eafae0beb20f3d6a234`
- **作者**: rayhuang198212
- **日期**: 2026-06-12T08:07:36Z
- **PR**: #2408

### 完整 commit message

```
test(e2e): stabilize scenario smoke tests (#2408)

## Summary

- Run Playwright e2e tests with a single worker to avoid shared-session
interleaving.
- Replace `networkidle` waits in dark-mode smoke coverage with
`domcontentloaded` to avoid hanging on long-lived app/network activity.
- Update the GIF search scenario to assert the user-visible image
response instead of depending on internal `gifgrep` tool-step UI.
```

### PR description

## Summary

- Run Playwright e2e tests with a single worker to avoid shared-session interleaving.
- Replace `networkidle` waits in dark-mode smoke coverage with `domcontentloaded` to avoid hanging on long-lived app/network activity.
- Update the GIF search scenario to assert the user-visible image response instead of depending on internal `gifgrep` tool-step UI.

---

## ci(enterprise-admin): pass vertical pack checkout success url (#2407)

- **SHA**: `9511c837ed37663fd598b5d1aa4a86290aceb129`
- **作者**: bill-srp
- **日期**: 2026-06-12T07:52:55Z
- **PR**: #2407

### 完整 commit message

```
ci(enterprise-admin): pass vertical pack checkout success url (#2407)

## Summary
- Pass NEXT_PUBLIC_VERTICAL_PACK_CHECKOUT_SUCCESS_URL into the
enterprise-admin OpenNext build.
- Keep the value optional so the app still falls back to
https://zooclaw.ai when the GitHub Environment var is unset.

## Test plan
- [x] git diff --check
- [x] ruby -e 'require "yaml";
YAML.load_file(".github/workflows/deploy-enterprise-admin.yml"); puts
"ok"'
```

### PR description

## Summary
- Pass NEXT_PUBLIC_VERTICAL_PACK_CHECKOUT_SUCCESS_URL into the enterprise-admin OpenNext build.
- Keep the value optional so the app still falls back to https://zooclaw.ai when the GitHub Environment var is unset.

## Test plan
- [x] git diff --check
- [x] ruby -e 'require "yaml"; YAML.load_file(".github/workflows/deploy-enterprise-admin.yml"); puts "ok"'

---

## fix(enterprise-admin): Unbreak production build broken by checkout flow merge (#2404)

- **SHA**: `6a769f97b52a92d0def8a69b4390c5e92f167bed`
- **作者**: bill-srp
- **日期**: 2026-06-12T07:37:20Z
- **PR**: #2404

### 完整 commit message

```
fix(enterprise-admin): Unbreak production build broken by checkout flow merge (#2404)

## Summary
- Fix the `Deploy Enterprise Admin (Staging)` workflow failure ([run
27400306160](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/27400306160/job/80979484710))
introduced by #2401.
- Add `"use client"` to `vertical-pack-plan/[planId]/checkout/page.tsx`
— Next.js 16 rejects `next/dynamic({ ssr: false })` in Server Components
at build time. The page now matches the established `verify/page.tsx`
pattern (client wrapper + `ssr: false`, justified because the checkout
view model reads `window.location`).
- Wrap `/login` page body in a `<Suspense>` boundary — #2401 added
`useSearchParams()` to `useLoginViewModel` (returnTo flow), which fails
static prerendering without one (`missing-suspense-with-csr-bailout`).
This second error was unreachable in CI because the build died at the
Turbopack compile error first; it surfaced after fixing (1).

## Root cause
PR #2401 introduced two build-time-only errors. The `code-quality` gate
(lint + `tsc --noEmit` + vitest) cannot catch either: server/client
component boundary rules and prerender bailouts are enforced only by
`next build`, which first runs in the deploy workflow after merge.

## Test plan
- [x] `pnpm exec next build --turbopack` in `web/enterprise-admin` —
reproduced both failures on main, passes with this fix (all 11 static
pages generate; `/login` stays static ○, checkout route is dynamic ƒ)
- [x] `pnpm exec vitest run --config ./vitest.config.mts` — 221 tests
pass, including the existing `/login` returnTo tests
- [x] `pnpm exec tsc --noEmit`
- [x] `pnpm exec eslint` on both changed files, `--max-warnings=0`
```

### PR description

## Summary
- Fix the `Deploy Enterprise Admin (Staging)` workflow failure ([run 27400306160](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/27400306160/job/80979484710)) introduced by #2401.
- Add `"use client"` to `vertical-pack-plan/[planId]/checkout/page.tsx` — Next.js 16 rejects `next/dynamic({ ssr: false })` in Server Components at build time. The page now matches the established `verify/page.tsx` pattern (client wrapper + `ssr: false`, justified because the checkout view model reads `window.location`).
- Wrap `/login` page body in a `<Suspense>` boundary — #2401 added `useSearchParams()` to `useLoginViewModel` (returnTo flow), which fails static prerendering without one (`missing-suspense-with-csr-bailout`). This second error was unreachable in CI because the build died at the Turbopack compile error first; it surfaced after fixing (1).

## Root cause
PR #2401 introduced two build-time-only errors. The `code-quality` gate (lint + `tsc --noEmit` + vitest) cannot catch either: server/client component boundary rules and prerender bailouts are enforced only by `next build`, which first runs in the deploy workflow after merge.

## Test plan
- [x] `pnpm exec next build --turbopack` in `web/enterprise-admin` — reproduced both failures on main, passes with this fix (all 11 static pages generate; `/login` stays static ○, checkout route is dynamic ƒ)
- [x] `pnpm exec vitest run --config ./vitest.config.mts` — 221 tests pass, including the existing `/login` returnTo tests
- [x] `pnpm exec tsc --noEmit`
- [x] `pnpm exec eslint` on both changed files, `--max-warnings=0`

---

## feat(enterprise-admin): add vertical pack checkout flow (#2401)

- **SHA**: `48b51108fd1182362463bee6dc1f4a5ccb14906a`
- **作者**: bill-srp
- **日期**: 2026-06-12T06:58:40Z
- **PR**: #2401

### 完整 commit message

```
feat(enterprise-admin): add vertical pack checkout flow (#2401)

## Linear

https://linear.app/srpone/issue/ECA-956/enterprise-vertical-pack-subscriptions

## Summary
- Add authenticated enterprise-admin vertical pack checkout route that
creates a package and redirects to provider checkout.
- Move enterprise-admin API request helpers under services while
preserving the existing /api/claw BFF path.
- Add Stripe and Alipay payment method buttons, passing provider values
stripe and antom to the purchase API.

## Test plan
- [x] pnpm --dir web/enterprise-admin exec vitest run --config
./vitest.config.mts
'app/vertical-pack-plan/[planId]/checkout/__tests__/checkout-page.test.tsx'
services/__tests__/vertical-pack-checkout.test.ts
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit
- [x] pnpm --dir web/enterprise-admin exec eslint . --max-warnings=0
--cache --cache-location .eslintcache --cache-strategy content
```

### PR description

## Linear
https://linear.app/srpone/issue/ECA-956/enterprise-vertical-pack-subscriptions

## Summary
- Add authenticated enterprise-admin vertical pack checkout route that creates a package and redirects to provider checkout.
- Move enterprise-admin API request helpers under services while preserving the existing /api/claw BFF path.
- Add Stripe and Alipay payment method buttons, passing provider values stripe and antom to the purchase API.

## Test plan
- [x] pnpm --dir web/enterprise-admin exec vitest run --config ./vitest.config.mts 'app/vertical-pack-plan/[planId]/checkout/__tests__/checkout-page.test.tsx' services/__tests__/vertical-pack-checkout.test.ts
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit
- [x] pnpm --dir web/enterprise-admin exec eslint . --max-warnings=0 --cache --cache-location .eslintcache --cache-strategy content

---

## refactor(web): migrate user-business-data manual cache to React Query (#2402)

- **SHA**: `e86450ea646dcafeb3e551e936a2a728a95e010c`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-12T06:50:59Z
- **PR**: #2402

### 完整 commit message

```
refactor(web): migrate user-business-data manual cache to React Query (#2402)

## Summary
- 删除 `lib/api/user-business-data-cache.ts` —— 它是 #1868 治理后仅存的手写 TTL
cache，也是全 codebase 最后一个 `'ecap:*:updated'` CustomEvent fanout（R2/R3
反模式）。共享的 `getQueryClient()` 单例现在是唯一缓存。
- 新增 `lib/api/user-business-data.ts`（无 React import，与
`agent-catalog-cache.ts` 同模式的 QueryClient shim）：
- `ensureFreshUserBusinessData(uid)` = `fetchQuery({ staleTime: 5s })`
—— 完整复刻旧的 TTL + in-flight dedup 语义
- `refetchUserBusinessDataFresh(uid)` = `cancelQueries` + `fetchQuery({
staleTime: 0 })` —— 复刻旧 force-refetch 的"替换 in-flight、保证新请求"语义
- 共享 `userBusinessDataQueryFn`，hook 与 imperative 调用方在同一个 queryKey 下自动
dedup
- `UserBusinessDataContext`：删掉 `initialData` shim、event 订阅桥、手动 cache
clear —— imperative 写入经 RQ cache 自动到达 observer；`forceRefresh` mutation
不再需要 `onSuccess: setQueryData` 回写
- `MattermostProvider` / `subscription-refresh` / `auth manager` 切换到新
shim；logout 清理统一由 `clearUserStorage()` 内的 `getQueryClient().clear()` 负责
- 3 处 R2 `eslint-disable` 豁免全部移除（shrink-only 计数 3 → 0），过期的 TODO(#2001)
引用一并清掉
- 设计
spec：`docs/superpowers/specs/2026-06-12-user-business-data-rq-migration.md`（含
3 条有意的行为差异说明）

## Test plan
- [x] 新增 `tests/unit/lib/api/user-business-data.unit.spec.ts`：用真实
singleton QueryClient 验证 dedup / 5s 新鲜窗口 / force 绕过 fresh cache / force
替换 in-flight / uid 隔离 / 失败不缓存
- [x] 重写 `UserBusinessDataContext.unit.spec.tsx`：原"event 推送更新"用例改为"外部
`setQueryData` 写入共享 cache 自动到达 context"（迁移后的真实同步机制）；error-clearing
回归用例保留
- [x] `MattermostContext` / `auth manager` spec 更新 mock 路径与返回值形状
- [x] 全量单测 507 files / 7149 passed；`pnpm lint` / `tsc --noEmit` / `pnpm
lint:ci`（dependency-cruiser + knip）/ `pnpm dup` / cache-governance
shrink-only 脚本全绿
- [x] 本地 dev:staging（mock-backend 配方）实测：登录态加载 `/api/users/get`
200，UserMenu 正确渲染 Pro 徽章（context query 与 `refreshSubscriptionInfo`
共享同一次请求 = dedup 生效）；路由切换触发 `refetchOnMount: 'always'` 重新拉取；console 无新增错误

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR description

## Summary
- 删除 `lib/api/user-business-data-cache.ts` —— 它是 #1868 治理后仅存的手写 TTL cache，也是全 codebase 最后一个 `'ecap:*:updated'` CustomEvent fanout（R2/R3 反模式）。共享的 `getQueryClient()` 单例现在是唯一缓存。
- 新增 `lib/api/user-business-data.ts`（无 React import，与 `agent-catalog-cache.ts` 同模式的 QueryClient shim）：
  - `ensureFreshUserBusinessData(uid)` = `fetchQuery({ staleTime: 5s })` —— 完整复刻旧的 TTL + in-flight dedup 语义
  - `refetchUserBusinessDataFresh(uid)` = `cancelQueries` + `fetchQuery({ staleTime: 0 })` —— 复刻旧 force-refetch 的"替换 in-flight、保证新请求"语义
  - 共享 `userBusinessDataQueryFn`，hook 与 imperative 调用方在同一个 queryKey 下自动 dedup
- `UserBusinessDataContext`：删掉 `initialData` shim、event 订阅桥、手动 cache clear —— imperative 写入经 RQ cache 自动到达 observer；`forceRefresh` mutation 不再需要 `onSuccess: setQueryData` 回写
- `MattermostProvider` / `subscription-refresh` / `auth manager` 切换到新 shim；logout 清理统一由 `clearUserStorage()` 内的 `getQueryClient().clear()` 负责
- 3 处 R2 `eslint-disable` 豁免全部移除（shrink-only 计数 3 → 0），过期的 TODO(#2001) 引用一并清掉
- 设计 spec：`docs/superpowers/specs/2026-06-12-user-business-data-rq-migration.md`（含 3 条有意的行为差异说明）

## Test plan
- [x] 新增 `tests/unit/lib/api/user-business-data.unit.spec.ts`：用真实 singleton QueryClient 验证 dedup / 5s 新鲜窗口 / force 绕过 fresh cache / force 替换 in-flight / uid 隔离 / 失败不缓存
- [x] 重写 `UserBusinessDataContext.unit.spec.tsx`：原"event 推送更新"用例改为"外部 `setQueryData` 写入共享 cache 自动到达 context"（迁移后的真实同步机制）；error-clearing 回归用例保留
- [x] `MattermostContext` / `auth manager` spec 更新 mock 路径与返回值形状
- [x] 全量单测 507 files / 7149 passed；`pnpm lint` / `tsc --noEmit` / `pnpm lint:ci`（dependency-cruiser + knip）/ `pnpm dup` / cache-governance shrink-only 脚本全绿
- [x] 本地 dev:staging（mock-backend 配方）实测：登录态加载 `/api/users/get` 200，UserMenu 正确渲染 Pro 徽章（context query 与 `refreshSubscriptionInfo` 共享同一次请求 = dedup 生效）；路由切换触发 `refetchOnMount: 'always'` 重新拉取；console 无新增错误

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## test(e2e): stabilize chat tool and media scenario assertions (#2303)

- **SHA**: `b4672c9bb91ef37448883ec828b5fa27408fea51`
- **作者**: rayhuang198212
- **日期**: 2026-06-12T06:37:46Z
- **PR**: #2303

### 完整 commit message

```
test(e2e): stabilize chat tool and media scenario assertions (#2303)

## Summary

- Improve PandaClaw chat E2E response tracking so tool-assisted replies
are validated across the full current response turn, not only the final
bot message.
- Scope audio/video/image/link assertions to the current response turn
to avoid false positives from earlier messages in shared sessions.
- Update media and tool scenarios to assert generated attachments and
multi-part responses more reliably.
- Refresh scenario prompts and expectations for direct image/GIF
generation and Fibonacci output.
- Remove stale/flaky session title and concurrent session leak checks
that no longer reflect the current product behavior.
- Increase LLM judge response budget and support data URI image inputs
for browser-local media assertions.
```

### PR description

## Summary

- Improve PandaClaw chat E2E response tracking so tool-assisted replies are validated across the full current response turn, not only the final bot message.
- Scope audio/video/image/link assertions to the current response turn to avoid false positives from earlier messages in shared sessions.
- Update media and tool scenarios to assert generated attachments and multi-part responses more reliably.
- Refresh scenario prompts and expectations for direct image/GIF generation and Fibonacci output.
- Remove stale/flaky session title and concurrent session leak checks that no longer reflect the current product behavior.
- Increase LLM judge response budget and support data URI image inputs for browser-local media assertions.


---

## fix(agent-packs): refine pack submission workflow (#2397)

- **SHA**: `58573c2f92b30ad40c5356d84ab8e375ee195b80`
- **作者**: bill-srp
- **日期**: 2026-06-12T06:09:55Z
- **PR**: #2397

### 完整 commit message

```
fix(agent-packs): refine pack submission workflow (#2397)

## Summary
- add optional submission avatar handling and dashboard avatar opt-in
for archive uploads
- show submission details in an approve-only review dialog
- allow duplicate pack names while keeping display ids unique

## Tests
- services/claw-interface/.venv/bin/python -m ruff format --check app
tests
- services/claw-interface/.venv/bin/python -m ruff check app tests
- services/claw-interface/.venv/bin/python -m pytest
tests/unit/test_pack_services.py tests/unit/test_pack_repo.py
tests/unit/test_pack_store_txn_repo.py
tests/unit/test_routes_pack_store.py
tests/unit/test_internal_agent_packs_routes.py -q
- pnpm --dir web/dashboard-console exec vitest run
app/routes/agent-packs/route.test.tsx
app/routes/agent-packs/use-view-model.test.tsx
app/routes/agent-packs/submissions/route.test.tsx
app/routes/agent-packs/submissions/use-view-model.test.tsx
app/lib/claw-api.test.ts tests/packs.test.ts
- pnpm --dir web/dashboard-console exec tsc -b --pretty false
- pnpm --dir web/dashboard-console exec eslint app/lib/claw-api.ts
app/lib/packs.ts app/routes/agent-packs/route.tsx
app/routes/agent-packs/route.test.tsx
app/routes/agent-packs/use-view-model.ts
app/routes/agent-packs/use-view-model.test.tsx
app/routes/agent-packs/submissions/route.tsx
app/routes/agent-packs/submissions/route.test.tsx
app/routes/agent-packs/submissions/use-view-model.ts
app/routes/agent-packs/submissions/use-view-model.test.tsx
app/routes/agent-packs/submission-dialog.tsx
app/routes/agent-packs/submission-form.ts
app/routes/agent-packs/dialog-kit.tsx tests/packs.test.ts

## Notes
- pyright was not run locally because services/claw-interface/.venv does
not include pyright and uv run currently fails during editable build
dependency parsing for the git favie-common requirement.
```

### PR description

## Summary
- add optional submission avatar handling and dashboard avatar opt-in for archive uploads
- show submission details in an approve-only review dialog
- allow duplicate pack names while keeping display ids unique

## Tests
- services/claw-interface/.venv/bin/python -m ruff format --check app tests
- services/claw-interface/.venv/bin/python -m ruff check app tests
- services/claw-interface/.venv/bin/python -m pytest tests/unit/test_pack_services.py tests/unit/test_pack_repo.py tests/unit/test_pack_store_txn_repo.py tests/unit/test_routes_pack_store.py tests/unit/test_internal_agent_packs_routes.py -q
- pnpm --dir web/dashboard-console exec vitest run app/routes/agent-packs/route.test.tsx app/routes/agent-packs/use-view-model.test.tsx app/routes/agent-packs/submissions/route.test.tsx app/routes/agent-packs/submissions/use-view-model.test.tsx app/lib/claw-api.test.ts tests/packs.test.ts
- pnpm --dir web/dashboard-console exec tsc -b --pretty false
- pnpm --dir web/dashboard-console exec eslint app/lib/claw-api.ts app/lib/packs.ts app/routes/agent-packs/route.tsx app/routes/agent-packs/route.test.tsx app/routes/agent-packs/use-view-model.ts app/routes/agent-packs/use-view-model.test.tsx app/routes/agent-packs/submissions/route.tsx app/routes/agent-packs/submissions/route.test.tsx app/routes/agent-packs/submissions/use-view-model.ts app/routes/agent-packs/submissions/use-view-model.test.tsx app/routes/agent-packs/submission-dialog.tsx app/routes/agent-packs/submission-form.ts app/routes/agent-packs/dialog-kit.tsx tests/packs.test.ts

## Notes
- pyright was not run locally because services/claw-interface/.venv does not include pyright and uv run currently fails during editable build dependency parsing for the git favie-common requirement.

---

## refactor(web): model onboarding modal visibility as an event-driven reducer (#2400)

- **SHA**: `d62230136ca39b1ed85131bf64454415cab97b7f`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-12T05:53:44Z
- **PR**: #2400

### 完整 commit message

```
refactor(web): model onboarding modal visibility as an event-driven reducer (#2400)

## Summary
- Second half of #2196 — the `LoginCheckProvider` half already landed as
`lib/login-check-store.ts`; this PR does the remaining
`OnboardingProvider` cluster the issue identified.
- Replaces the bare `isModalOpen` `useState<boolean>` +
`userOpenedModal` arbitration flag + two transition effects (auto-open
`:293` / auto-close `:307`) with a pure `modalVisibilityReducer` in new
`web/app/src/lib/onboarding/modal-visibility.ts` (next to
`resolve-status.ts`).
- Every signal is now an event (`signals-changed` / `show-requested` /
`user-dismissed` / `completed`); the open/close decision — including
"user-opened modal survives auto-recompute" and the ECA-675
landing-context guard — lives in one unit-testable pure function. The
two transition effects collapse into a single `signals-changed`
dispatch; decisions read fresh reducer state instead of effect-dep
closures.
- Host choice is provider-local `useReducer` (the `useArtifactsSidebar`
shape), **not** a zustand store: unlike `checkLogin()`, the onboarding
modal has no non-React callers — all consumers go through
`OnboardingContext`. Rationale + behavior table in the design spec:
`docs/superpowers/specs/2026-06-12-onboarding-modal-visibility-reducer.md`.
- No behavior change; `OnboardingContext` contract unchanged.

Closes #2196

## Test plan
- [x] Characterization-first: 4 new pins (dismissal stickiness while
`required`, user-override survival, preview-mode auto-open ×2) added and
passing against the **old** implementation before the refactor
- [x] All 50 pre-existing `OnboardingProvider.unit.spec.tsx` tests pass
**unmodified** against the refactored provider (54/54 total)
- [x] New 17-case pure reducer spec
`tests/unit/lib/onboarding/modal-visibility.unit.spec.ts` covering every
decision row (incl. ECA-675 landing-context, public-page suppression,
StrictMode idempotence)
- [x] Full local gates: `pnpm tsc`, `pnpm lint`, `pnpm test:unit` (7154
passed), `pnpm dup`, `pnpm lint:ci` (dependency-cruiser + knip)
- [x] Manual validation (next dev + mock-backend recipe, staging env
vars): no modal on public landing `/` and `/en/pricing`; modal stays
closed for an onboarding-complete user on `/chat`; `?onboarding=preview`
auto-opens the immersive modal and leaving preview closes it again

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR description

## Summary
- Second half of #2196 — the `LoginCheckProvider` half already landed as `lib/login-check-store.ts`; this PR does the remaining `OnboardingProvider` cluster the issue identified.
- Replaces the bare `isModalOpen` `useState<boolean>` + `userOpenedModal` arbitration flag + two transition effects (auto-open `:293` / auto-close `:307`) with a pure `modalVisibilityReducer` in new `web/app/src/lib/onboarding/modal-visibility.ts` (next to `resolve-status.ts`).
- Every signal is now an event (`signals-changed` / `show-requested` / `user-dismissed` / `completed`); the open/close decision — including "user-opened modal survives auto-recompute" and the ECA-675 landing-context guard — lives in one unit-testable pure function. The two transition effects collapse into a single `signals-changed` dispatch; decisions read fresh reducer state instead of effect-dep closures.
- Host choice is provider-local `useReducer` (the `useArtifactsSidebar` shape), **not** a zustand store: unlike `checkLogin()`, the onboarding modal has no non-React callers — all consumers go through `OnboardingContext`. Rationale + behavior table in the design spec: `docs/superpowers/specs/2026-06-12-onboarding-modal-visibility-reducer.md`.
- No behavior change; `OnboardingContext` contract unchanged.

Closes #2196

## Test plan
- [x] Characterization-first: 4 new pins (dismissal stickiness while `required`, user-override survival, preview-mode auto-open ×2) added and passing against the **old** implementation before the refactor
- [x] All 50 pre-existing `OnboardingProvider.unit.spec.tsx` tests pass **unmodified** against the refactored provider (54/54 total)
- [x] New 17-case pure reducer spec `tests/unit/lib/onboarding/modal-visibility.unit.spec.ts` covering every decision row (incl. ECA-675 landing-context, public-page suppression, StrictMode idempotence)
- [x] Full local gates: `pnpm tsc`, `pnpm lint`, `pnpm test:unit` (7154 passed), `pnpm dup`, `pnpm lint:ci` (dependency-cruiser + knip)
- [x] Manual validation (next dev + mock-backend recipe, staging env vars): no modal on public landing `/` and `/en/pricing`; modal stays closed for an onboarding-complete user on `/chat`; `?onboarding=preview` auto-opens the immersive modal and leaving preview closes it again

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## ci(arch-review): exclude knip-frozen legacy modules from web findings (#2399)

- **SHA**: `15da3a89a4ffeedb8b5c7370b96354f62ba1cb1b`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-12T05:16:32Z
- **PR**: #2399

### 完整 commit message

```
ci(arch-review): exclude knip-frozen legacy modules from web findings (#2399)

## Summary
- `/arch-review`（每周一 cron 的 findings 生成 skill）增加规则：读取
`web/app/knip.config.ts` 中标注 **"Legacy modules preserved per product
decision"** 的 ignore
块（`canvas/**`、`agent-chat-client/**`、`example-showcase/**`、`config/examples/**`），这些冻结模块内：
  - 不再产出新 finding
  - 既有 finding（F16/F19）按 resolved 归档（产品决策 wontfix），Summary 中说明理由
- 背景：F17/F18/F20/F21 已分别由 #2392/#2398/#2396/#2395 修复合并，F16/F19
指向冻结代码永远不会被"修复"——不教会扫描器这条产品决策，cohort issues #2060/#2144 会永远挂着，且这三个 issue
被手工关闭后（baseline 只读 open issues），下周一扫描会把 F16/F19 当新 finding 重新立案。
- 时效说明：建议在下周一 09:00 UTC 的 cron 之前合并。

## Test plan
- [x] 纯 prompt/docs 变更，无代码路径；规则文本与 `web/app/knip.config.ts` ignore
列表核对一致
- [x] resolved bullet 的 regex 契约未动（理由写入 Summary 而非 bullet）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR description

## Summary
- `/arch-review`（每周一 cron 的 findings 生成 skill）增加规则：读取 `web/app/knip.config.ts` 中标注 **"Legacy modules preserved per product decision"** 的 ignore 块（`canvas/**`、`agent-chat-client/**`、`example-showcase/**`、`config/examples/**`），这些冻结模块内：
  - 不再产出新 finding
  - 既有 finding（F16/F19）按 resolved 归档（产品决策 wontfix），Summary 中说明理由
- 背景：F17/F18/F20/F21 已分别由 #2392/#2398/#2396/#2395 修复合并，F16/F19 指向冻结代码永远不会被"修复"——不教会扫描器这条产品决策，cohort issues #2060/#2144 会永远挂着，且这三个 issue 被手工关闭后（baseline 只读 open issues），下周一扫描会把 F16/F19 当新 finding 重新立案。
- 时效说明：建议在下周一 09:00 UTC 的 cron 之前合并。

## Test plan
- [x] 纯 prompt/docs 变更，无代码路径；规则文本与 `web/app/knip.config.ts` ignore 列表核对一致
- [x] resolved bullet 的 regex 契约未动（理由写入 Summary 而非 bullet）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): decompose AuthManager into auth submodules (#2398)

- **SHA**: `ea1ad9f3985f72afbbef6448ca481266240d7ed3`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-12T05:07:46Z
- **PR**: #2398

### 完整 commit message

```
refactor(web): decompose AuthManager into auth submodules (#2398)

## Summary
- 落地 arch-review
[#2144](https://github.com/SerendipityOneInc/ecap-workspace/issues/2144)
**F18**：从 802 行的 `AuthManager` god-class 中抽出三个职责清晰的模块，类本身回归 Firebase
生命周期 + 业务数据同步编排（641 行，退出 `eslint.config.mjs` 复杂度豁免列表 ✂️）：
- `lib/auth/subscription-refresh.ts` — `refreshSubscriptionInfo`
原样迁出（它本来就不用任何实例状态），并收敛**唯一一份** business-data → `SubscriptionInfo` 字段映射
- `lib/auth/billing-retry.ts` — billing 初始化轮询（`startBillingRetryPolling`
/ `cancelBillingRetryPolling`），模块级 active-uid token 复刻原
`billingRetryUid` 的登出/换号取消语义
- `lib/auth/post-login-setup.ts` — `ensurePersonalOrg`（per-uid 去重）+
`syncLocale` + 登出时 `resetPostLoginSetup`
- **顺带修复一个潜在数据 drift**：`saveSubscriptionInfo` 映射此前在 `_createAndSyncUser`
与 `refreshSubscriptionInfo` 重复存在且已漂移——create 路径漏掉 `subscription_status`
/ `cancel_at_period_end`（类型上已声明）及全部 v2 字段（`plan` / `billing_cycle` /
`trial_end_time` / `completed_billing_cycles` / `pending_downgrade`），而
`saveSubscriptionInfo` 是整体覆写，每次 create/sync 会把这些字段从 localStorage 抹掉直到下一次
refresh。统一映射后：后端不返回的字段映射为 `undefined`（`JSON.stringify`
丢弃，序列化结果与现状逐字节一致）；后端返回时则不再被抹掉
- `initialize()` 的嵌套 token 过期恢复逻辑抽为 `_refreshExistingUser` /
`_recoverFromInvalidToken`（复杂度 29→达标，嵌套 7 层→达标）
- `refreshSubscriptionInfo` 经 manager.ts re-export，6 个既有 import 点零改动
- 附带：`mock-backend.mjs` 补 `POST /users/create` handler（注意 `callAPI` 的
success-passthrough 需要双层 envelope）、`.env.mock.local` 增加
`NEXT_PUBLIC_CLAW_INTERFACE_URL`——使启动同步 + personal org + 统一映射路径在 mock
配方下可端到端验证

> 背景：F18 是 arch-review 唯一存活的 live P1 finding（F17/F20/F21 已分别由
#2392/#2396/#2395 解决，F16/F19 指向 knip 冻结的 legacy 模块）。`syncBusinessData`
编排核心按 finding 建议保留在类内。
> Spec:
`docs/superpowers/specs/2026-06-12-auth-manager-decomposition.md`

## Test plan
- [x] `pnpm lint`（manager.ts 已移出复杂度豁免列表后零违例）/ `tsc --noEmit` / `pnpm
lint:ci`（dependency-cruiser + knip）/ `pnpm dup` 全绿
- [x] `pnpm test:unit` 7132 用例全过；`manager.unit.spec.ts`（148 用例，全部 mock
叶子模块）**零修改**通过——抽取对行为完全透明
- [x] mock+staging 配方真实浏览器验证：auth bypass → `initialize()` →
`syncBusinessData` → 清空 `gensmo:auth:subscription_info` 后刷新，确认 create
路径经统一映射写入**含 v2 字段**（`plan: 'pro'`、`subscription_status:
'active'`、`payment_channel: 'stripe'` 等）的完整订阅信息；`ensurePersonalOrg` 命中
mock `/orgs/personal`；console 0 errors（此前的 `[Business Data Sync] Failed`
与 `Personal org create threw` 均消除）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR description

## Summary
- 落地 arch-review [#2144](https://github.com/SerendipityOneInc/ecap-workspace/issues/2144) **F18**：从 802 行的 `AuthManager` god-class 中抽出三个职责清晰的模块，类本身回归 Firebase 生命周期 + 业务数据同步编排（641 行，退出 `eslint.config.mjs` 复杂度豁免列表 ✂️）：
  - `lib/auth/subscription-refresh.ts` — `refreshSubscriptionInfo` 原样迁出（它本来就不用任何实例状态），并收敛**唯一一份** business-data → `SubscriptionInfo` 字段映射
  - `lib/auth/billing-retry.ts` — billing 初始化轮询（`startBillingRetryPolling` / `cancelBillingRetryPolling`），模块级 active-uid token 复刻原 `billingRetryUid` 的登出/换号取消语义
  - `lib/auth/post-login-setup.ts` — `ensurePersonalOrg`（per-uid 去重）+ `syncLocale` + 登出时 `resetPostLoginSetup`
- **顺带修复一个潜在数据 drift**：`saveSubscriptionInfo` 映射此前在 `_createAndSyncUser` 与 `refreshSubscriptionInfo` 重复存在且已漂移——create 路径漏掉 `subscription_status` / `cancel_at_period_end`（类型上已声明）及全部 v2 字段（`plan` / `billing_cycle` / `trial_end_time` / `completed_billing_cycles` / `pending_downgrade`），而 `saveSubscriptionInfo` 是整体覆写，每次 create/sync 会把这些字段从 localStorage 抹掉直到下一次 refresh。统一映射后：后端不返回的字段映射为 `undefined`（`JSON.stringify` 丢弃，序列化结果与现状逐字节一致）；后端返回时则不再被抹掉
- `initialize()` 的嵌套 token 过期恢复逻辑抽为 `_refreshExistingUser` / `_recoverFromInvalidToken`（复杂度 29→达标，嵌套 7 层→达标）
- `refreshSubscriptionInfo` 经 manager.ts re-export，6 个既有 import 点零改动
- 附带：`mock-backend.mjs` 补 `POST /users/create` handler（注意 `callAPI` 的 success-passthrough 需要双层 envelope）、`.env.mock.local` 增加 `NEXT_PUBLIC_CLAW_INTERFACE_URL`——使启动同步 + personal org + 统一映射路径在 mock 配方下可端到端验证

> 背景：F18 是 arch-review 唯一存活的 live P1 finding（F17/F20/F21 已分别由 #2392/#2396/#2395 解决，F16/F19 指向 knip 冻结的 legacy 模块）。`syncBusinessData` 编排核心按 finding 建议保留在类内。
> Spec: `docs/superpowers/specs/2026-06-12-auth-manager-decomposition.md`

## Test plan
- [x] `pnpm lint`（manager.ts 已移出复杂度豁免列表后零违例）/ `tsc --noEmit` / `pnpm lint:ci`（dependency-cruiser + knip）/ `pnpm dup` 全绿
- [x] `pnpm test:unit` 7132 用例全过；`manager.unit.spec.ts`（148 用例，全部 mock 叶子模块）**零修改**通过——抽取对行为完全透明
- [x] mock+staging 配方真实浏览器验证：auth bypass → `initialize()` → `syncBusinessData` → 清空 `gensmo:auth:subscription_info` 后刷新，确认 create 路径经统一映射写入**含 v2 字段**（`plan: 'pro'`、`subscription_status: 'active'`、`payment_channel: 'stripe'` 等）的完整订阅信息；`ensurePersonalOrg` 命中 mock `/orgs/personal`；console 0 errors（此前的 `[Business Data Sync] Failed` 与 `Personal org create threw` 均消除）

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## refactor(web): decompose RichTextInput into focused editor modules (#2396)

- **SHA**: `5e05a90e5380bbeaafe00a7eab5dac99c2c81dd5`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-12T04:18:45Z
- **PR**: #2396

### 完整 commit message

```
refactor(web): decompose RichTextInput into focused editor modules (#2396)

## Summary
- 落地 arch-review
[#2265](https://github.com/SerendipityOneInc/ecap-workspace/issues/2265)
**F20**：把 838 行的 `RichTextInput.tsx` 单体组件拆解为 ~110 行组合层 +
六个单一职责模块（`src/components/rich-text-input/`）：
  - `markdown-text.ts` — 纯字符串工具（截断、URL/markdown 检测、accept 匹配），node 环境可测
- `chip-elements.ts` — image/video/link chip 的 DOM 工厂，回调经
`ChipCallbacks` 显式传参（原为 props 闭包）
- `markdown-dom.ts` — markdown ↔ editor DOM 双向转换、uploading chip
原位增量更新、光标处 URL→chip 转换、粘贴 HTML chip 提取
- `hooks/useRichTextEditor` — editor ref + IME 组合态 + 受控 `value` 同步
effect + placeholder
- `hooks/useRichTextKeyboard` — chip 感知的 Backspace/Delete、编辑器内
Cmd+A、Enter 提交（IME guard）
- `hooks/useRichTextClipboard` — 粘贴/拖放管线（文件、大文本转 .txt、自有 markdown/HTML
重插、外部 HTML 降纯文本）
- **行为保持不变**：835 行既有黑盒测试除一处 inline-style 断言外零改动通过；公共 API 仅删除无任何调用方的
`style` prop（`outline: none` 移入 Tailwind class）
- `RichTextInput.tsx` 从两个 shrink-only ESLint 豁免列表（legacy complexity
overrides + inline-style grandfather #754）中移除 ✂️
- `RichTextInput.url.unit.spec.ts` 改为导入真实的
`truncateUrl`/`convertUrlsToLinkMarkdown`（原先断言的是测试内一份已漂移的复制实现）
- 附带：`extractChipMarkdownFromHtml` 用 `DOMParser`（惰性 document）替代 detached
div `innerHTML`，粘贴解析不再触发资源加载；chip emoji 图标 `innerHTML` → `textContent`
- 附带：`mock-backend.mjs` 补 `/computers` + conversations handlers（sidenav
读 `computers[0]`，catch-all `{}` 会让 `(chat)` 页面整页崩溃）

> 背景：本周期 open 的 arch-review findings 中 F16/F19 指向
`agent-chat-client`/`canvas`——`knip.config.ts` 标记的产品冻结 legacy
模块，故不重构；F20 是 live 代码（`GenClawInput`、`SubagentChatPanel`
主聊天输入）中优先级最高的结构债。
> Spec:
`docs/superpowers/specs/2026-06-12-rich-text-input-decomposition.md`

## Test plan
- [x] `pnpm lint`（含 shrink-only 守卫）/ `tsc --noEmit` / `pnpm
lint:ci`（dependency-cruiser + knip）/ `pnpm dup` 全绿
- [x] `pnpm test:unit` 507 文件 / 7132 用例全过；RichTextInput 三个
spec（render/keyboard/IME/paste/URL）通过
- [x] 本地 mock+staging 配方（`dotenv -e .env.mock.local -e
.env.staging.local`）真实浏览器验证 `/mini-chat` 挂载的重构组件：打字→受控值回流、URL+空格→link
chip（display 截断/完整 URL 保留）、Backspace 整体删除 chip、粘贴自有 markdown→image
chip、placeholder 显隐——均正常，无组件相关 console error

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR description

## Summary
- 落地 arch-review [#2265](https://github.com/SerendipityOneInc/ecap-workspace/issues/2265) **F20**：把 838 行的 `RichTextInput.tsx` 单体组件拆解为 ~110 行组合层 + 六个单一职责模块（`src/components/rich-text-input/`）：
  - `markdown-text.ts` — 纯字符串工具（截断、URL/markdown 检测、accept 匹配），node 环境可测
  - `chip-elements.ts` — image/video/link chip 的 DOM 工厂，回调经 `ChipCallbacks` 显式传参（原为 props 闭包）
  - `markdown-dom.ts` — markdown ↔ editor DOM 双向转换、uploading chip 原位增量更新、光标处 URL→chip 转换、粘贴 HTML chip 提取
  - `hooks/useRichTextEditor` — editor ref + IME 组合态 + 受控 `value` 同步 effect + placeholder
  - `hooks/useRichTextKeyboard` — chip 感知的 Backspace/Delete、编辑器内 Cmd+A、Enter 提交（IME guard）
  - `hooks/useRichTextClipboard` — 粘贴/拖放管线（文件、大文本转 .txt、自有 markdown/HTML 重插、外部 HTML 降纯文本）
- **行为保持不变**：835 行既有黑盒测试除一处 inline-style 断言外零改动通过；公共 API 仅删除无任何调用方的 `style` prop（`outline: none` 移入 Tailwind class）
- `RichTextInput.tsx` 从两个 shrink-only ESLint 豁免列表（legacy complexity overrides + inline-style grandfather #754）中移除 ✂️
- `RichTextInput.url.unit.spec.ts` 改为导入真实的 `truncateUrl`/`convertUrlsToLinkMarkdown`（原先断言的是测试内一份已漂移的复制实现）
- 附带：`extractChipMarkdownFromHtml` 用 `DOMParser`（惰性 document）替代 detached div `innerHTML`，粘贴解析不再触发资源加载；chip emoji 图标 `innerHTML` → `textContent`
- 附带：`mock-backend.mjs` 补 `/computers` + conversations handlers（sidenav 读 `computers[0]`，catch-all `{}` 会让 `(chat)` 页面整页崩溃）

> 背景：本周期 open 的 arch-review findings 中 F16/F19 指向 `agent-chat-client`/`canvas`——`knip.config.ts` 标记的产品冻结 legacy 模块，故不重构；F20 是 live 代码（`GenClawInput`、`SubagentChatPanel` 主聊天输入）中优先级最高的结构债。
> Spec: `docs/superpowers/specs/2026-06-12-rich-text-input-decomposition.md`

## Test plan
- [x] `pnpm lint`（含 shrink-only 守卫）/ `tsc --noEmit` / `pnpm lint:ci`（dependency-cruiser + knip）/ `pnpm dup` 全绿
- [x] `pnpm test:unit` 507 文件 / 7132 用例全过；RichTextInput 三个 spec（render/keyboard/IME/paste/URL）通过
- [x] 本地 mock+staging 配方（`dotenv -e .env.mock.local -e .env.staging.local`）真实浏览器验证 `/mini-chat` 挂载的重构组件：打字→受控值回流、URL+空格→link chip（display 截断/完整 URL 保留）、Backspace 整体删除 chip、粘贴自有 markdown→image chip、placeholder 显隐——均正常，无组件相关 console error

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## refactor(connectors): extract composio-connectors action orchestration into hooks (#2395)

- **SHA**: `6be97d9c5640243d3f989c4596aab5753ea6fbaf`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-12T03:25:16Z
- **PR**: #2395

### 完整 commit message

```
refactor(connectors): extract composio-connectors action orchestration into hooks (#2395)

## Summary
- Completes arch-review finding **F21** (#2265) —
"ComposioConnectorsClient OAuth 状态机与提供商目录 UI 深度耦合" — and removes the
F19-style setter-callback anti-pattern from the composio-connectors
module. Design spec:
`docs/superpowers/specs/2026-06-12-composio-connectors-module-refactor.md`.
- **New `hooks/useConnectorActions.ts`** owns the connector state
machine: `pendingAction` / `actionError` / `lastSyncState`, the shared
`runAction` shape, the six action wrappers (connect / disconnect /
enable / disable / refresh / request), the OAuth popup handling, and the
OAuth-return auto-enable flow (`useEnableOAuthReturnAfterConnect` is now
called inside the hook layer, so its `Dispatch<SetStateAction>` params
no longer cross the component boundary).
- **Presentational split**: `ProviderCard` (+ its private
badge/chips/actions cluster), `ConnectorToolbar`,
`ConnectProviderDialog`, `RuntimePanel`, `MetaRow` move to
`components/`; catalog merge/filter/summary derivations become pure
functions in `catalog.ts`.
- **Query keys** move to `hooks/keys.ts` and now start with
`QUERY_VERSION` per the repo data-fetching convention (these keys are
not in `PERSIST_ALLOWLIST`, so no storage migration concerns).
- `ComposioConnectorsClient.tsx` drops from 843 to ~180 lines and the
file-level `/* eslint-disable max-lines */` is removed.
- `scripts/mock-backend.mjs` gains composio endpoints (state-mutating
enable/disable/disconnect/interest + catalog/connections fixtures) so
the RQ invalidation path is verifiable locally end-to-end.

Behavior-preserving: no copy, layout, endpoint, or i18n-key changes. The
existing 590-line behavior-driven unit spec passes with only import-path
updates.

## Test plan
- [x] `pnpm tsc` clean
- [x] `pnpm lint` clean (max-lines suppression removed, no new
exemptions)
- [x] Full unit suite: 507 files / 7131 tests pass
- [x] `pnpm lint:ci` (dependency-cruiser + knip) and `pnpm dup` (jscpd)
pass
- [x] Local browser validation against `scripts/mock-backend.mjs` (mock
+ staging env recipe) on `/en/integrations/connector`: grid render &
coming-soon sorting, enable mutation → RQ invalidation → badge/summary
update (1→2), interest count 4→5 via `setQueryData`, category filter,
disconnect → Connect dialog flow, refresh status

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR description

## Summary
- Completes arch-review finding **F21** (#2265) — "ComposioConnectorsClient OAuth 状态机与提供商目录 UI 深度耦合" — and removes the F19-style setter-callback anti-pattern from the composio-connectors module. Design spec: `docs/superpowers/specs/2026-06-12-composio-connectors-module-refactor.md`.
- **New `hooks/useConnectorActions.ts`** owns the connector state machine: `pendingAction` / `actionError` / `lastSyncState`, the shared `runAction` shape, the six action wrappers (connect / disconnect / enable / disable / refresh / request), the OAuth popup handling, and the OAuth-return auto-enable flow (`useEnableOAuthReturnAfterConnect` is now called inside the hook layer, so its `Dispatch<SetStateAction>` params no longer cross the component boundary).
- **Presentational split**: `ProviderCard` (+ its private badge/chips/actions cluster), `ConnectorToolbar`, `ConnectProviderDialog`, `RuntimePanel`, `MetaRow` move to `components/`; catalog merge/filter/summary derivations become pure functions in `catalog.ts`.
- **Query keys** move to `hooks/keys.ts` and now start with `QUERY_VERSION` per the repo data-fetching convention (these keys are not in `PERSIST_ALLOWLIST`, so no storage migration concerns).
- `ComposioConnectorsClient.tsx` drops from 843 to ~180 lines and the file-level `/* eslint-disable max-lines */` is removed.
- `scripts/mock-backend.mjs` gains composio endpoints (state-mutating enable/disable/disconnect/interest + catalog/connections fixtures) so the RQ invalidation path is verifiable locally end-to-end.

Behavior-preserving: no copy, layout, endpoint, or i18n-key changes. The existing 590-line behavior-driven unit spec passes with only import-path updates.

## Test plan
- [x] `pnpm tsc` clean
- [x] `pnpm lint` clean (max-lines suppression removed, no new exemptions)
- [x] Full unit suite: 507 files / 7131 tests pass
- [x] `pnpm lint:ci` (dependency-cruiser + knip) and `pnpm dup` (jscpd) pass
- [x] Local browser validation against `scripts/mock-backend.mjs` (mock + staging env recipe) on `/en/integrations/connector`: grid render & coming-soon sorting, enable mutation → RQ invalidation → badge/summary update (1→2), interest count 4→5 via `setQueryData`, category filter, disconnect → Connect dialog flow, refresh status

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## ci(auto-review): allow ecap-pm-agent through AI review gates (#2394)

- **SHA**: `4ca36af364e35ea07e6c740dc94126019d802dc0`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-12T02:54:36Z
- **PR**: #2394

### 完整 commit message

```
ci(auto-review): allow ecap-pm-agent through AI review gates (#2394)

## Why

claw-steward#60 switched the auto-fix pipeline to open PRs as the
**ecap-pm-agent** App (so srp-claude-assistant can formally approve
them), but both AI reviewer reusables here only allowlisted
`srp-claude-assistant`:

- **claude-review** (claude-code-action) hard-fails: `Workflow initiated
by non-human actor: ecap-pm-agent (type: Bot)`
- **codex-review** (codex-action) maps `allowed_bots` →
`allow-bot-users`; ecap-pm-agent is absent, falls back to the
collaborator write-access check, and App bots get permission `none`

The `auto-review / gate` then blocks every auto-fix PR. This killed
#2380–#2383 and reproduced exactly on the re-dispatched
#2390/#2391/#2393, while same-day srp-claude-assistant PRs (#2372–#2374)
merged fine.

## What

Add `ecap-pm-agent` to both `allowed_bots` lists in
`.github/workflows/auto-review.yaml` (claude umbrella line + codex
umbrella line). No other behavior change.

## Validation

Failure evidence: claude-review job 80798890982 / codex-review job
80798890991 on #2383 (and identical signatures on #2380–#2382,
#2390/#2391/#2393).

After merge: re-trigger review on #2390/#2391/#2393 (synchronize event)
— both reviewers should start instead of failing in <30s.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR description

## Why

claw-steward#60 switched the auto-fix pipeline to open PRs as the **ecap-pm-agent** App (so srp-claude-assistant can formally approve them), but both AI reviewer reusables here only allowlisted `srp-claude-assistant`:

- **claude-review** (claude-code-action) hard-fails: `Workflow initiated by non-human actor: ecap-pm-agent (type: Bot)`
- **codex-review** (codex-action) maps `allowed_bots` → `allow-bot-users`; ecap-pm-agent is absent, falls back to the collaborator write-access check, and App bots get permission `none`

The `auto-review / gate` then blocks every auto-fix PR. This killed #2380–#2383 and reproduced exactly on the re-dispatched #2390/#2391/#2393, while same-day srp-claude-assistant PRs (#2372–#2374) merged fine.

## What

Add `ecap-pm-agent` to both `allowed_bots` lists in `.github/workflows/auto-review.yaml` (claude umbrella line + codex umbrella line). No other behavior change.

## Validation

Failure evidence: claude-review job 80798890982 / codex-review job 80798890991 on #2383 (and identical signatures on #2380–#2382, #2390/#2391/#2393).

After merge: re-trigger review on #2390/#2391/#2393 (synchronize event) — both reviewers should start instead of failing in <30s.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(billing): extract SubscriptionPanel payment orchestration into useSubscriptionActions (#2392)

- **SHA**: `7325c722b254cb6bdb9e52d47dc284c62b76e5dd`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-12T02:32:26Z
- **PR**: #2392

### 完整 commit message

```
refactor(billing): extract SubscriptionPanel payment orchestration into useSubscriptionActions (#2392)

## Summary
- Resolves arch-review **F17** (#2060): `SubscriptionPanel.tsx` (970
lines, still growing week-over-week) mixed payment-flow orchestration,
raw async API calls, ~10 hand-rolled pending/error `useState` flags, and
UI rendering in one component.
- New `src/components/billing/hooks/useSubscriptionActions.ts` owns the
checkout flow state machine and every server mutation via React Query
`useMutation` (inheriting the global `mutations.retry: 0` that protects
paid endpoints). `isLoading` / `error` / `portalLoading` /
`isRenewingSubscription` / `isCancelingDowngrade` become derived
mutation state instead of manually synced flags.
- Unifies the two ~85%-duplicated checkout handlers (subscription vs
top-up: create order → Stripe session / Antom payment → popup navigate)
into one `runCheckoutFlow` with a discriminated-union `CheckoutRequest`,
dispatched from a single payment-method handler.
- Moves the cancel-subscription flow (~40 lines of async business logic
previously inlined in `CancelConfirmModal`'s `onConfirm` JSX prop) into
the hook.
- `SubscriptionPanelInner` becomes purely presentational (~420 lines,
mostly JSX).

### Preserved invariants (verified against the old implementation)
- Popup opens **synchronously** in the click handler (Safari drops
user-activation across `await`); the handle travels in mutation
variables — `mutationFn` never opens windows.
- #1102 stuck-button guard: loading state only flips after the uid
guard, now structurally (`isPending` flips only when `mutate` is
reached).
- Trial expectation check (`expectsTrial && !is_trial` →
`TRIAL_UNAVAILABLE_MESSAGE`) before any navigation; Apple-channel
guards; popup-blocked early returns; `cancelSubmitted` optimistic flag
semantics.
- Both confirm modals keep their `onConfirm: () => Promise<void>`
spinner contract via `mutateAsync`.

Design spec:
`docs/superpowers/specs/2026-06-12-subscription-panel-actions-hook.md`

## Test plan
- [x] All 63 existing `SubscriptionPanel{,-extras}` unit tests pass
unchanged (they mock at the module boundary and exercise flows through
the rendered panel — behavior contract). Only harness change:
`renderPanel()` wraps with `createQueryWrapper()`.
- [x] Full `pnpm lint` / `pnpm tsc` / `pnpm test:unit` (7131 tests) /
`pnpm dup` green.
- [x] Browser validation against the mock backend
(`scripts/mock-backend.mjs` + staging public config): panel renders with
active-pro billing data through the RQ chain; Monthly/Annually toggle
updates prices + CTA states ("Current Plan" disabled on current cycle);
payment-method modal opens with correct channel-lock logic (Alipay
disabled for active Stripe sub); checkout error path verified end-to-end
(backend error → popup closed → modal closed → error banner derived from
`mutation.error`); Cancel-subscription modal opens with correct plan
name.
- [x] `pnpm dev:staging` smoke: pricing page renders, zero prod-domain
(`zooclaw.ai`) request leakage. (Deeper authenticated staging validation
blocked on CF Access service-token secrets, which are write-only in
GitHub and not available locally.)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR description

## Summary
- Resolves arch-review **F17** (#2060): `SubscriptionPanel.tsx` (970 lines, still growing week-over-week) mixed payment-flow orchestration, raw async API calls, ~10 hand-rolled pending/error `useState` flags, and UI rendering in one component.
- New `src/components/billing/hooks/useSubscriptionActions.ts` owns the checkout flow state machine and every server mutation via React Query `useMutation` (inheriting the global `mutations.retry: 0` that protects paid endpoints). `isLoading` / `error` / `portalLoading` / `isRenewingSubscription` / `isCancelingDowngrade` become derived mutation state instead of manually synced flags.
- Unifies the two ~85%-duplicated checkout handlers (subscription vs top-up: create order → Stripe session / Antom payment → popup navigate) into one `runCheckoutFlow` with a discriminated-union `CheckoutRequest`, dispatched from a single payment-method handler.
- Moves the cancel-subscription flow (~40 lines of async business logic previously inlined in `CancelConfirmModal`'s `onConfirm` JSX prop) into the hook.
- `SubscriptionPanelInner` becomes purely presentational (~420 lines, mostly JSX).

### Preserved invariants (verified against the old implementation)
- Popup opens **synchronously** in the click handler (Safari drops user-activation across `await`); the handle travels in mutation variables — `mutationFn` never opens windows.
- #1102 stuck-button guard: loading state only flips after the uid guard, now structurally (`isPending` flips only when `mutate` is reached).
- Trial expectation check (`expectsTrial && !is_trial` → `TRIAL_UNAVAILABLE_MESSAGE`) before any navigation; Apple-channel guards; popup-blocked early returns; `cancelSubmitted` optimistic flag semantics.
- Both confirm modals keep their `onConfirm: () => Promise<void>` spinner contract via `mutateAsync`.

Design spec: `docs/superpowers/specs/2026-06-12-subscription-panel-actions-hook.md`

## Test plan
- [x] All 63 existing `SubscriptionPanel{,-extras}` unit tests pass unchanged (they mock at the module boundary and exercise flows through the rendered panel — behavior contract). Only harness change: `renderPanel()` wraps with `createQueryWrapper()`.
- [x] Full `pnpm lint` / `pnpm tsc` / `pnpm test:unit` (7131 tests) / `pnpm dup` green.
- [x] Browser validation against the mock backend (`scripts/mock-backend.mjs` + staging public config): panel renders with active-pro billing data through the RQ chain; Monthly/Annually toggle updates prices + CTA states ("Current Plan" disabled on current cycle); payment-method modal opens with correct channel-lock logic (Alipay disabled for active Stripe sub); checkout error path verified end-to-end (backend error → popup closed → modal closed → error banner derived from `mutation.error`); Cancel-subscription modal opens with correct plan name.
- [x] `pnpm dev:staging` smoke: pricing page renders, zero prod-domain (`zooclaw.ai`) request leakage. (Deeper authenticated staging validation blocked on CF Access service-token secrets, which are write-only in GitHub and not available locally.)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(dashboard): import agent pack archive metadata in pack dialogs (#2388)

- **SHA**: `24148daf9a52c28819d4e48da28d14fa186fcee6`
- **作者**: bill-srp
- **日期**: 2026-06-12T02:25:33Z
- **PR**: #2388

### 完整 commit message

```
feat(dashboard): import agent pack archive metadata in pack dialogs (#2388)

## Linear

https://linear.app/srpone/issue/ECA-886/agent-pack-admin-dashboard-webdashboard

## Summary
- Make the dashboard-console agent pack workflow archive-first: upload a
pack archive (ZIP or TAR.GZ), parse `agent-pack.yaml` (and optional
`description.json`) in the browser, and prefill pack / submission
metadata in both the create-pack and submit-version dialogs.
- New `app/lib/agent-pack-archive.ts`: JSZip-based ZIP reader plus a
dependency-free tar.gz reader (`DecompressionStream`), per-mode
required-field validation (create vs submit), `description.json` field
overrides, and avatar extraction (PNG/JPG/JPEG/WEBP only — SVG is
rejected because extracted avatars land on the public bucket and a
script-bearing SVG would be stored XSS).
- Create-pack flow can create a pack directly from a parsed archive:
create draft → upload archive to R2 → submit the first version, with
stale-request guards so swapping archives mid-upload can't clobber
state.
- `api/r2-upload`: new `pack_archive` purpose accepting ZIP/TAR.GZ up to
100 MB with required `org_id`/`pack_id` metadata; avatar uploads reject
SVG.
- Submissions page gains the submit-version dialog with the same archive
parsing, plus the existing approve flow.
- Cleanup pass: deduplicated the seven form helpers shared by the two
view-models, extracted a single `pack-archive-extension` rule shared by
the client parser and the upload API, and `description.json` is now
parsed once per extraction.
- Design doc:
`docs/superpowers/specs/2026-06-11-agent-pack-archive-metadata-design.md`;
plan:
`docs/superpowers/plans/2026-06-11-agent-pack-archive-metadata.md`.

## Test plan
- [x] `pnpm run lint` (dashboard-console) passes
- [x] `pnpm run typecheck` (cf-typegen + react-router typegen + tsc -b)
passes
- [x] `pnpm run test` — 176 tests in 25 files pass, covering ZIP/TAR.GZ
parsing, description.json overrides, avatar extraction and SVG
rejection, dialog prefill, upload error paths, and archive replacement
guards
```

### PR description

## Linear
https://linear.app/srpone/issue/ECA-886/agent-pack-admin-dashboard-webdashboard

## Summary
- Make the dashboard-console agent pack workflow archive-first: upload a pack archive (ZIP or TAR.GZ), parse `agent-pack.yaml` (and optional `description.json`) in the browser, and prefill pack / submission metadata in both the create-pack and submit-version dialogs.
- New `app/lib/agent-pack-archive.ts`: JSZip-based ZIP reader plus a dependency-free tar.gz reader (`DecompressionStream`), per-mode required-field validation (create vs submit), `description.json` field overrides, and avatar extraction (PNG/JPG/JPEG/WEBP only — SVG is rejected because extracted avatars land on the public bucket and a script-bearing SVG would be stored XSS).
- Create-pack flow can create a pack directly from a parsed archive: create draft → upload archive to R2 → submit the first version, with stale-request guards so swapping archives mid-upload can't clobber state.
- `api/r2-upload`: new `pack_archive` purpose accepting ZIP/TAR.GZ up to 100 MB with required `org_id`/`pack_id` metadata; avatar uploads reject SVG.
- Submissions page gains the submit-version dialog with the same archive parsing, plus the existing approve flow.
- Cleanup pass: deduplicated the seven form helpers shared by the two view-models, extracted a single `pack-archive-extension` rule shared by the client parser and the upload API, and `description.json` is now parsed once per extraction.
- Design doc: `docs/superpowers/specs/2026-06-11-agent-pack-archive-metadata-design.md`; plan: `docs/superpowers/plans/2026-06-11-agent-pack-archive-metadata.md`.

## Test plan
- [x] `pnpm run lint` (dashboard-console) passes
- [x] `pnpm run typecheck` (cf-typegen + react-router typegen + tsc -b) passes
- [x] `pnpm run test` — 176 tests in 25 files pass, covering ZIP/TAR.GZ parsing, description.json overrides, avatar extraction and SVG rejection, dialog prefill, upload error paths, and archive replacement guards
