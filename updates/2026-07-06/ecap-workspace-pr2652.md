---
title: "修复小窗聊天与 Agent Builder 中图片附件导致的页面崩溃"
type: "Bug Fix"
priority: "中"
date: "2026-07-06"
status: "待审核"
channels: ""
---

# 修复小窗聊天与 Agent Builder 中图片附件导致的页面崩溃

## 核心宣传点

在小窗聊天（mini-chat）和 Agent Builder 测试面板里收到图片、视频等附件时页面不再白屏崩溃，附件点击预览也恢复正常。

## 原始内容

[783f741c] fix(web): mount preview providers for mini-chat and agent-builder surfaces (#2652)

## Problem

React render-time crash: `useImagePreview must be used within
ImagePreviewProvider`.

`ImagePreviewProvider` and `FilePreviewProvider` are mounted
**per-surface only** — in `GenClawClient`, `SessionThreadClient`,
`agent-chat-client`, and `share/ReplayPlayer`. But the **same** OpenClaw
message tree is also rendered by surfaces that mount neither:

- **mini-chat** — `MiniChatClient` → `SubagentChatPanel` →
`OpenClawThread` (compact)
- **agent-builder test pane** — `OpenClawChatSurface` → `OpenClawThread`

That tree renders `MMAttachments`, whose `ImageAttachment` /
`VideoAttachment` / `ReplayAttachment` / `FileAttachment` call the
**throwing** `useImagePreview()` / `useFilePreview()`. So the first
image / video / replay / file attachment crashes the whole subtree on
those surfaces. (ECA-1120, also the frontend half of ECA-1085 /
ECA-1118.)

## Root-cause fix

1. **Defense-in-depth (the crash-stopper).** All four attachment
components now read the context through the existing **optional**
variants `useOptionalImagePreview` / `useOptionalFilePreview` and
**no-op `open()` when the context is null** — the same pattern
`MarkdownContent` already uses. This removes the hard throw from the
shared message tree regardless of which provider is mounted where.

2. **Mount `ImagePreviewProvider` on the standalone mini-chat route** so
its image/video lightbox actually works (the main chat already mounts it
per-surface; agent-builder already mounts `ImagePreviewProvider` via
#2635).

### Why `FilePreviewProvider` is not hoisted

`FilePreviewProvider` requires a per-surface `state` prop computed by
`useArtifactsSidebar(...)` (tied to that surface's `displayMessages` /
`mm` wiring and the artifacts sidebar UI). mini-chat and the
agent-builder test pane have **no artifacts sidebar**, so there is
nothing to hoist a meaningful provider into. On those surfaces file
clicks gracefully **no-op** via the optional hook while the file
**download button keeps working** (it never depended on the provider).
The full chat and the public replay viewer are unchanged — they still
mount both providers and the lightbox/sidebar behave exactly as before.

## Test

New
`web/app/tests/unit/components/mattermost/MMAttachmentsNoPreviewProvider.unit.spec.tsx`
renders `MMAttachments` (image, video, previewable file) **with no
preview providers in scope** — exactly the mini-chat / agent-builder
condition — and asserts it does **not** throw.

- **Red before the fix:** fails with `useImagePreview must be used
within ImagePreviewProvider` (verified by temporarily restoring the
throwing hook).
- **Green after:** renders cleanly.

Also updated the existing `MMAttachments.unit.spec.tsx` provider mocks
to export the optional hooks (`useOptionalImagePreview` /
`useOptionalFilePreview`) the components now consume.

## Files changed

- `web/app/src/components/mattermost/attachments/ImageAttachment.tsx`
- `web/app/src/components/mattermost/attachments/VideoAttachment.tsx`
- `web/app/src/components/mattermost/attachments/ReplayAttachment.tsx`
- `web/app/src/components/mattermost/attachments/FileAttachment.tsx`
-
`web/app/src/app/[locale]/(app)/(chat)/mini-chat/[sessionKey]/MiniChatClient.tsx`
- `web/app/tests/unit/components/mattermost/MMAttachments.unit.spec.tsx`
-
`web/app/tests/unit/components/mattermost/MMAttachmentsNoPreviewProvider.unit.spec.tsx`
(new)

## Links

- https://linear.app/srpone/issue/ECA-1120
- https://linear.app/srpone/issue/ECA-1085

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

--- PR #2652 body ---
## Problem

React render-time crash: `useImagePreview must be used within ImagePreviewProvider`.

`ImagePreviewProvider` and `FilePreviewProvider` are mounted **per-surface only** — in `GenClawClient`, `SessionThreadClient`, `agent-chat-client`, and `share/ReplayPlayer`. But the **same** OpenClaw message tree is also rendered by surfaces that mount neither:

- **mini-chat** — `MiniChatClient` → `SubagentChatPanel` → `OpenClawThread` (compact)
- **agent-builder test pane** — `OpenClawChatSurface` → `OpenClawThread`

That tree renders `MMAttachments`, whose `ImageAttachment` / `VideoAttachment` / `ReplayAttachment` / `FileAttachment` call the **throwing** `useImagePreview()` / `useFilePreview()`. So the first image / video / replay / file attachment crashes the whole subtree on those surfaces. (ECA-1120, also the frontend half of ECA-1085 / ECA-1118.)

## Root-cause fix

1. **Defense-in-depth (the crash-stopper).** All four attachment components now read the context through the existing **optional** variants `useOptionalImagePreview` / `useOptionalFilePreview` and **no-op `open()` when the context is null** — the same pattern `MarkdownContent` already uses. This removes the hard throw from the shared message tree regardless of which provider is mounted where.

2. **Mount `ImagePreviewProvider` on the standalone mini-chat route** so its image/video lightbox actually works (the main chat already mounts it per-surface; agent-builder already mounts `ImagePreviewProvider` via #2635).

### Why `FilePreviewProvider` is not hoisted

`FilePreviewProvider` requires a per-surface `state` prop computed by `useArtifactsSidebar(...)` (tied to that surface's `displayMessages` / `mm` wiring and the artifacts sidebar UI). mini-chat and the agent-builder test pane have **no artifacts sidebar**, so there is nothing to hoist a meaningful provider into. On those surfaces file clicks gracefully **no-op** via the optional hook while the file **download button keeps working** (it never depended on the provider). The full chat and the public replay viewer are unchanged — they still mount both providers and the lightbox/sidebar behave exactly as before.

## Test

New `web/app/tests/unit/components/mattermost/MMAttachmentsNoPreviewProvider.unit.spec.tsx` renders `MMAttachments` (image, video, previewable file) **with no preview providers in scope** — exactly the mini-chat / agent-builder condition — and asserts it does **not** throw.

- **Red before the fix:** fails with `useImagePreview must be used within ImagePreviewProvider` (verified by temporarily restoring the throwing hook).
- **Green after:** renders cleanly.

Also updated the existing `MMAttachments.unit.spec.tsx` provider mocks to export the optional hooks (`useOptionalImagePreview` / `useOptionalFilePreview`) the components now consume.

## Files changed

- `web/app/src/components/mattermost/attachments/ImageAttachment.tsx`
- `web/app/src/components/mattermost/attachments/VideoAttachment.tsx`
- `web/app/src/components/mattermost/attachments/ReplayAttachment.tsx`
- `web/app/src/components/mattermost/attachments/FileAttachment.tsx`
- `web/app/src/app/[locale]/(app)/(chat)/mini-chat/[sessionKey]/MiniChatClient.tsx`
- `web/app/tests/unit/components/mattermost/MMAttachments.unit.spec.tsx`
- `web/app/tests/unit/components/mattermost/MMAttachmentsNoPreviewProvider.unit.spec.tsx` (new)

## Links

- https://linear.app/srpone/issue/ECA-1120
- https://linear.app/srpone/issue/ECA-1085

🤖 Generated with [Claude Code](https://claude.com/claude-code)

