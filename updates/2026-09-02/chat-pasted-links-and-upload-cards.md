---
title: "聊天输入框：粘贴的链接完整可点，非图片附件改成卡片显示"
type: "体验优化"
priority: "中"
date: "2026-09-02"
status: "待审核"
channels: "Discord+changelog"
---

# 聊天输入框：粘贴的链接完整可点，非图片附件改成卡片显示

## 核心宣传点

以前在聊天输入框里粘贴一个网址，富文本编辑器会把它截断显示，而且链接不可点。现在粘贴的 URL 在输入框和对话记录里都完整展示，并且可以直接点开。

非图片类的上传文件也换了呈现方式：以前它们被当作 Markdown 链接处理，最后落到通用的行内链接小徽章上；现在统一渲染成紧凑的附件卡片，带本地化的上传进度状态，复用产品自己的文件类型图标，上传完成后的卡片可以点击打开对应文件。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `7d15a631cd8eef34d8cc9c366c073edf181ee302`
- PR: #3620
- 作者: shana-srp
- 日期: 2026-09-02T08:44:17Z

### Commit Message

```
fix(chat): improve pasted links and upload cards (#3620)

## Summary
- show pasted URLs in full and keep them directly clickable in the
composer and transcript
- render non-image uploads as compact attachment cards with localized
progress state
- reuse the existing app-owned file-type icons and make resolved file
cards open their target URL

## Root cause
The rich-text editor truncated URL labels and disabled link interaction.
Non-image R2 uploads were represented as Markdown links, so they fell
through to the generic inline link badge instead of the existing
attachment-card visual system.

## Test plan
- [x] `pnpm exec vitest run src/__tests__/rich-text-input.test.tsx
src/__tests__/rich-text-input-utils.test.ts
src/__tests__/rich-text-input-url.test.ts` (103 tests)
- [x] `pnpm exec vitest run
tests/unit/components/markdown/render-markdown-to-html.unit.spec.ts` (68
tests)
- [x] `pnpm exec vitest run
tests/unit/components/chat/unified-chat-composer/UnifiedChatComposer.unit.spec.tsx
tests/unit/components/chat/unified-chat-composer/composer-file-type-icons.unit.spec.ts`
(56 tests)
- [x] `bash scripts/verify-changed.sh`
- [x] manually verified uploading and resolved file-card states in the
local mock Chat preview

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

```
## Summary
- show pasted URLs in full and keep them directly clickable in the composer and transcript
- render non-image uploads as compact attachment cards with localized progress state
- reuse the existing app-owned file-type icons and make resolved file cards open their target URL

## Root cause
The rich-text editor truncated URL labels and disabled link interaction. Non-image R2 uploads were represented as Markdown links, so they fell through to the generic inline link badge instead of the existing attachment-card visual system.

## Test plan
- [x] `pnpm exec vitest run src/__tests__/rich-text-input.test.tsx src/__tests__/rich-text-input-utils.test.ts src/__tests__/rich-text-input-url.test.ts` (103 tests)
- [x] `pnpm exec vitest run tests/unit/components/markdown/render-markdown-to-html.unit.spec.ts` (68 tests)
- [x] `pnpm exec vitest run tests/unit/components/chat/unified-chat-composer/UnifiedChatComposer.unit.spec.tsx tests/unit/components/chat/unified-chat-composer/composer-file-type-icons.unit.spec.ts` (56 tests)
- [x] `bash scripts/verify-changed.sh`
- [x] manually verified uploading and resolved file-card states in the local mock Chat preview

```

