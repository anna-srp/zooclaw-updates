---
title: "网页版聊天现已支持渲染 Agent 交互卡片"
type: "新功能上线"
priority: "中"
date: "2026-07-10"
status: "待审核"
channels: ""
---

## 核心宣传点

网页版聊天现在能原生显示 Agent 发来的交互卡片（操作按钮、确认选项、下拉选择），此前这些卡片只在原生客户端可见，网页端体验和客户端对齐。

## 原始内容

**feat(web): render agent interactive cards in webapp chat (#2816)**

SHA: `dabe11c55c1e9dce5acab2610dc3ff542c2b3a03` | 作者: bill-srp | PR #2816

```
feat(web): render agent interactive cards in webapp chat (#2816)

## Summary

Renders agent-sent **interactive cards** (action buttons, confirm
presets, single-select dropdowns) natively in the webapp chat.

The agent emits cards via the `message` tool `card` param
(zooclaw-extras
[#171](https://github.com/SerendipityOneInc/zooclaw-extras/pull/171)
`@zooclaw/card-kit` +
[#169](https://github.com/SerendipityOneInc/zooclaw-extras/pull/169)
`@zooclaw/mattermost`). The Mattermost plugin renders them as native
interactive attachments (`props.attachments`, HMAC-signed actions). The
webapp is a Mattermost client on the same server but ignored those
attachments — cards were invisible in the webapp while working in the
native MM client.

**Click path is the native Mattermost round-trip:** the webapp calls
`POST /api/v4/posts/{post_id}/actions/{action_id}` (with
`selected_option` for selects); the MM server invokes the plugin's
HMAC-verified webhook; the plugin dispatches the canonical value to the
agent and edits the post into a completion banner, which re-renders over
the existing `post_edited` WebSocket path. **No backend or plugin
changes.**

## What's in this PR

- `src/lib/mattermost/interactive-attachments.ts` — pure parser
recognizing exactly the three PR #169 wire shapes (button row, single
select, text-only completion banner); everything else ignored by design
- `MattermostAPIService.doPostAction(postId, actionId, selectedOption?)`
— native post-action execution
- Pipeline: `OpenClawMessage.interactiveCards` populated in
`mmDisplayMessages`, survives `filterMessages` (card-only posts stay
visible), exposed via runtime `metadata.custom`
- `InteractiveCards` chat component — shadcn semantic tokens,
pending/disabled state during dispatch, failure toast + re-enable,
read-only disable guard, immediate-dispatch select (no submit button)
- Compact chat variant (subagent panel) renders cards too — card-only
posts don't degrade to an empty bubble
- Wired into `OpenClawAssistantMessage` (normal + tool-group branches,
emptiness guard)
- Design spec + implementation plan docs

Design decisions (from spec): card-kit shapes only (not generic MM
attachment rendering); new self-contained module rather than reusing the
ERMP renderer (ERMP clicks are `[ACTION:…]` text-postbacks; these are MM
post actions — same look via shared tokens, different wire protocol).

## Dependencies / sequencing

Independently shippable: until zooclaw-extras #171 + #169 merge,
publish, and deploy, the parser simply finds no card-shaped attachments
and nothing changes. End-to-end behavior activates once the plugin
ships.

## Test plan

- [x] `bash scripts/verify-web.sh` — guards + tsc + vitest (7,556
passed) + eslint, all green
- [x] Unit: parser (8 tests, fixtures copied from plugin wire output),
`doPostAction` request shape (3), pipeline surfacing + card-only
visibility + `propsEqual` attachments-edit guard, `InteractiveCards`
component states (6), assistant-message wiring (2)
- [ ] Live staging validation after zooclaw-extras #171/#169 deploy:
send actions/confirm/select from a real agent, click each in the webapp,
verify canonical value reaches the agent and the completion banner
replaces the card (doubles as #169's pending live-select verification)

## Known limitation — replay

Shared-replay snapshots don't carry `props.attachments` (the backend
replay pipeline only copies `ermp_cards` etc., and backend changes are
explicitly out of scope per the spec), so interactive cards are
**omitted from replays** rather than shown disabled. The component's
`useIsReplayReadOnly()` guard is defensive for any future read-only
Mattermost-backed surface. Copying `attachments` through `chat_replay`
is a possible backend follow-up.

## Docs

- Spec:
`docs/superpowers/specs/2026-07-10-webapp-interactive-cards-design.md`
- Plan: `docs/superpowers/plans/2026-07-10-webapp-interactive-cards.md`

No Linear issue exists for this feature (requested directly in session).
```

### PR body

## Summary

Renders agent-sent **interactive cards** (action buttons, confirm presets, single-select dropdowns) natively in the webapp chat.

The agent emits cards via the `message` tool `card` param (zooclaw-extras [#171](https://github.com/SerendipityOneInc/zooclaw-extras/pull/171) `@zooclaw/card-kit` + [#169](https://github.com/SerendipityOneInc/zooclaw-extras/pull/169) `@zooclaw/mattermost`). The Mattermost plugin renders them as native interactive attachments (`props.attachments`, HMAC-signed actions). The webapp is a Mattermost client on the same server but ignored those attachments — cards were invisible in the webapp while working in the native MM client.

**Click path is the native Mattermost round-trip:** the webapp calls `POST /api/v4/posts/{post_id}/actions/{action_id}` (with `selected_option` for selects); the MM server invokes the plugin's HMAC-verified webhook; the plugin dispatches the canonical value to the agent and edits the post into a completion banner, which re-renders over the existing `post_edited` WebSocket path. **No backend or plugin changes.**

## What's in this PR

- `src/lib/mattermost/interactive-attachments.ts` — pure parser recognizing exactly the three PR #169 wire shapes (button row, single select, text-only completion banner); everything else ignored by design
- `MattermostAPIService.doPostAction(postId, actionId, selectedOption?)` — native post-action execution
- Pipeline: `OpenClawMessage.interactiveCards` populated in `mmDisplayMessages`, survives `filterMessages` (card-only posts stay visible), exposed via runtime `metadata.custom`
- `InteractiveCards` chat component — shadcn semantic tokens, pending/disabled state during dispatch, failure toast + re-enable, read-only disable guard, immediate-dispatch select (no submit button)
- Compact chat variant (subagent panel) renders cards too — card-only posts don't degrade to an empty bubble
- Wired into `OpenClawAssistantMessage` (normal + tool-group branches, emptiness guard)
- Design spec + implementation plan docs

Design decisions (from spec): card-kit shapes only (not generic MM attachment rendering); new self-contained module rather than reusing the ERMP renderer (ERMP clicks are `[ACTION:…]` text-postbacks; these are MM post actions — same look via shared tokens, different wire protocol).

## Dependencies / sequencing

Independently shippable: until zooclaw-extras #171 + #169 merge, publish, and deploy, the parser simply finds no card-shaped attachments and nothing changes. End-to-end behavior activates once the plugin ships.

## Test plan

- [x] `bash scripts/verify-web.sh` — guards + tsc + vitest (7,556 passed) + eslint, all green
- [x] Unit: parser (8 tests, fixtures copied from plugin wire output), `doPostAction` request shape (3), pipeline surfacing + card-only visibility + `propsEqual` attachments-edit guard, `InteractiveCards` component states (6), assistant-message wiring (2)
- [ ] Live staging validation after zooclaw-extras #171/#169 deploy: send actions/confirm/select from a real agent, click each in the webapp, verify canonical value reaches the agent and the completion banner replaces the card (doubles as #169's pending live-select verification)

## Known limitation — replay

Shared-replay snapshots don't carry `props.attachments` (the backend replay pipeline only copies `ermp_cards` etc., and backend changes are explicitly out of scope per the spec), so interactive cards are **omitted from replays** rather than shown disabled. The component's `useIsReplayReadOnly()` guard is defensive for any future read-only Mattermost-backed surface. Copying `attachments` through `chat_replay` is a possible backend follow-up.

## Docs

- Spec: `docs/superpowers/specs/2026-07-10-webapp-interactive-cards-design.md`
- Plan: `docs/superpowers/plans/2026-07-10-webapp-interactive-cards.md`

No Linear issue exists for this feature (requested directly in session).

