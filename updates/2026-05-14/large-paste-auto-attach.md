---
title: "聊天框大段粘贴自动转附件，支持预览"
type: "新功能上线"
priority: "中"
date: "2026-05-14"
status: "待审核"
channels: ""
---
# 聊天框大段粘贴自动转附件，支持预览

## 核心宣传点

在聊天框粘贴超大段文字（超 5KB 或 4000 字符）时，系统自动将其转为文件附件发送，避免消息过长报错；同时支持发送前点击预览附件内容。

## 原始内容

**Commit**: eaf23e78 | feat(web): large-paste auto-attach + click-to-preview pending chips (#1631)

**Commit Message**:
```
feat(web): large-paste auto-attach + click-to-preview pending chips (#1631)
```

**PR Body**:
## Summary

Two related composer features for the Mattermost-backed chat surface:

- **Large pasted text auto-converts to a `.txt` attachment** instead of being inserted inline. Trigger: `bytes > 5KB || chars > MM_MAX_MESSAGE_LENGTH (4000)`. The byte rule catches CJK/emoji-heavy pastes; the char rule catches ASCII pastes that would otherwise hit Mattermost's send-time length check. Gated by `isFileTypeAccepted` so canvas's media-only composer falls back to the existing inline behavior with zero parent-side changes.
- **Pending attachment chips become clickable** for previewable text-like files (`.txt`, `.md`, `.json`, code) in the existing artifact sidebar — previously users had no way to inspect content before send. Implementation extracts `MmPendingAttachmentChip` as a standalone component with an `onClick` handler that opens the sidebar viewer with a synthetic `AnnotatedFile` wrapper.

## Motivation

- Sending a very long paste currently hits Mattermost's 4 000-char limit and fails silently or with a confusing error.
- Users need a way to verify the attachment content before committing to send.

## Test plan

- [x] Paste < 5KB text → still inserts inline (no regression)
- [x] Paste > 5KB text (or > 4 000 chars) → auto-attaches as `.txt`, chip appears
- [x] Click chip for `.txt`/`.md`/`.json`/code file → sidebar opens with content
- [x] `pnpm lint` clean / `tsc --noEmit` clean
- [x] Unit tests added: `AutoAttachPasteHandler.test.ts`, `MmPendingAttachmentChip.test.tsx`
