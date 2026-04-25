---
title: "对话回放与分享功能上线"
type: "新功能上线"
priority: "高"
date: "2026-04-25"
status: "待审核"
channels: "站内弹窗 + Use Case + Discord + changelog"
---

# 对话回放与分享功能上线

## 核心宣传点

现在可以将你的对话生成公开分享链接，让他人直接查看完整对话流程，方便展示 AI 工作成果。

## 原始内容

Commit: a3be1850c771d9362da42f2653690b2652401219

Message:
feat(chat-replay): chat-page selection UI + share flow (ECA-548 3/3) (#1302)

## Summary

Third of three stacked PRs
([ECA-548](https://linear.app/srpone/issue/ECA-548/share-selected-chat-messages-as-replay-page)).
Adds the creator-side flow on `/chat`: a selection mode that lets users
pick messages and generate a public replay link via the BFF from #1301 →
backend from #1300.

- **`useChatReplayShare`** hook owns the selection-mode flag, selected
MM post-id set, and create/revoke plumbing. Derives the shareable set
from current `displayMessages` per render (respects the "Select visible"
spec — loaded messages only, never full channel history).
- **`getShareableMessages`** filter drops synthetic tool-group
aggregation rows and `isSystem` messages — keeps parity with the backend
visibility filter from PR 1.
- **`ChatShare*`** components under `components/share/`:
- `ChatShareCheckbox`: reads `ShareSelectionContext` so message
components don't need prop-drilling
- `ChatShareSelectionContext`: tiny provider, default `{enabled: false}`
— zero impact on chat when unmounted
- `ChatShareSelectionBar`: Cancel / Select visible / Clear / count /
Create replay
  - `ChatShareCreatedDialog`: copyable URL + Open + Revoke (idempotent)
- **Integration**: `GenClawClient` mounts the selection provider around
`OpenClawThread`, adds a Share button to the header (hidden when nothing
is shareable yet). `OpenClawUserMessage` / `OpenClawAssistantMessage`
each gain one `<ChatShareCheckbox postId={messageId} />` call.

## Stack

- PR 1 (#1300): backend ← `main`
- PR 2 (#1301): viewer + BFF ← base: `feat/eca-548-a-backend`
- **PR 3 (this one)**: `/chat` selection UI ← base:
`feat/eca-548-b-viewer`

⚠ Merge order: #1300 → #1301 → this.

## Test plan

- [x] `pnpm tsc --noEmit` clean, `pnpm exec eslint` clean
- [x] `getShareableMessages` unit tests (sync filter rules, tool-group
exclusion, order preserved)
- [x] Manual E2E: enter selection mode → select N messages → Create
replay → copy URL → open in incognito → confirm full replay
- [ ] Manual E2E: revoke from created dialog → incognito 404
- [ ] CI green

PR Description:
## Summary

Third of three stacked PRs ([ECA-548](https://linear.app/srpone/issue/ECA-548/share-selected-chat-messages-as-replay-page)). Adds the creator-side flow on `/chat`: a selection mode that lets users pick messages and generate a public replay link via the BFF from #1301 → backend from #1300.

- **`useChatReplayShare`** hook owns the selection-mode flag, selected MM post-id set, and create/revoke plumbing. Derives the shareable set from current `displayMessages` per render (respects the "Select visible" spec — loaded messages only, never full channel history).
- **`getShareableMessages`** filter drops synthetic tool-group aggregation rows and `isSystem` messages — keeps parity with the backend visibility filter from PR 1.
- **`ChatShare*`** components under `components/share/`:
  - `ChatShareCheckbox`: reads `ShareSelectionContext` so message components don't need prop-drilling
  - `ChatShareSelectionContext`: tiny provider, default `{enabled: false}` — zero impact on chat when unmounted
  - `ChatShareSelectionBar`: Cancel / Select visible / Clear / count / Create replay
  - `ChatShareCreatedDialog`: copyable URL + Open + Revoke (idempotent)
- **Integration**: `GenClawClient` mounts the selection provider around `OpenClawThread`, adds a Share button to the header (hidden when nothing is shareable yet). `OpenClawUserMessage` / `OpenClawAssistantMessage` each gain one `<ChatShareCheckbox postId={messageId} />` call.

## Stack

- PR 1 (#1300): backend ← `main`
- PR 2 (#1301): viewer + BFF ← base: `feat/eca-548-a-backend`
- **PR 3 (this one)**: `/chat` selection UI ← base: `feat/eca-548-b-viewer`

⚠ Merge order: #1300 → #1301 → this.

## Test plan

- [x] `pnpm tsc --noEmit` clean, `pnpm exec eslint` clean
- [x] `getShareableMessages` unit tests (sync filter rules, tool-group exclusion, order preserved)
- [x] Manual E2E: enter selection mode → select N messages → Create replay → copy URL → open in incognito → confirm full replay
- [ ] Manual E2E: revoke from created dialog → incognito 404
- [ ] CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)
