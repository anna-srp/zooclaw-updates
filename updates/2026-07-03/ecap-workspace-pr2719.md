---
title: "修复聊天框上传失败后残留「上传中」占位导致无法发送"
type: "Bug Fix"
priority: "低"
date: "2026-07-03"
status: "待审核"
channels: ""
---

# 修复聊天框上传失败后残留「上传中」占位导致无法发送

## 核心宣传点

文件名含括号的附件上传失败后，聊天输入框不再残留「上传中」占位卡住发送按钮；连续上传多个文件也不会互相覆盖。

## 原始内容

fix(chat): clear failed upload placeholders (#2719)

## Summary
- Fix failed file-upload cleanup in the chat composer when a
pasted/copied filename contains a closing bracket.
- Sanitize uploaded file markdown labels so filenames with brackets do
not create malformed composer markdown.
- Preserve functional placeholder appends for back-to-back uploads so
concurrent uploads cannot overwrite earlier placeholders.
- Add regression tests for bracket filenames, persisted pending drafts,
opening brackets, normal uploading text, and consecutive uploads before
the first upload resolves.

## Root cause
The composer disabled send while `uploading:` placeholders remained in
the input. Failed upload cleanup used a regex that could not match
placeholder markdown when the filename contained `]`, and raw filenames
were inserted directly into markdown labels, so bracketed filenames
could create malformed attachment markup.

## Test plan
- [x]
`/Users/shiqi/pandaclaw-code/ecap-workspace/web/app/node_modules/.bin/vitest
run --config ./vitest.config.mts
tests/unit/app/chat/GenClawInput.unit.spec.tsx` (64 tests passed, run
from the isolated worktree)
- [ ] `eslint` targeted changed files (blocked locally: isolated
worktree dependency layout could not resolve
`@zooclaw/design-system/tokens.css`; CI web-quality lint-and-typecheck
runs in the proper workspace install)
- [ ] `tsc --noEmit` (blocked locally: isolated worktree dependency
layout could not resolve `@zooclaw/design-system`; CI web-quality
lint-and-typecheck runs in the proper workspace install)

---

**PR Description:**

## Summary
- Fix failed file-upload cleanup in the chat composer when a pasted/copied filename contains a closing bracket.
- Sanitize uploaded file markdown labels so filenames with brackets do not create malformed composer markdown.
- Preserve functional placeholder appends for back-to-back uploads so concurrent uploads cannot overwrite earlier placeholders.
- Add regression tests for bracket filenames, persisted pending drafts, opening brackets, normal uploading text, and consecutive uploads before the first upload resolves.

## Root cause
The composer disabled send while `uploading:` placeholders remained in the input. Failed upload cleanup used a regex that could not match placeholder markdown when the filename contained `]`, and raw filenames were inserted directly into markdown labels, so bracketed filenames could create malformed attachment markup.

## Test plan
- [x] `/Users/shiqi/pandaclaw-code/ecap-workspace/web/app/node_modules/.bin/vitest run --config ./vitest.config.mts tests/unit/app/chat/GenClawInput.unit.spec.tsx` (64 tests passed, run from the isolated worktree)
- [ ] `eslint` targeted changed files (blocked locally: isolated worktree dependency layout could not resolve `@zooclaw/design-system/tokens.css`; CI web-quality lint-and-typecheck runs in the proper workspace install)
- [ ] `tsc --noEmit` (blocked locally: isolated worktree dependency layout could not resolve `@zooclaw/design-system`; CI web-quality lint-and-typecheck runs in the proper workspace install)
