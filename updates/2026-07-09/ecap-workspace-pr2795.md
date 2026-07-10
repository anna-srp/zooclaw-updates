---
title: "修复中文/输入法状态下回车误发送消息"
type: "Bug Fix"
priority: "中"
date: "2026-07-09"
status: "待审核"
channels: ""
---

## 核心宣传点

使用中文等输入法打字时，按回车确认候选词不会再误触发送消息；正常的回车发送、Shift+回车换行保持不变。中文用户输入体验更顺手。

## 原始内容

**fix(web): avoid sending chat on IME commit enter (#2795)**

SHA: `2bd72630066dd617dee78220a02e713c7594452a` | 作者: bill-srp | PR #2795

```
fix(web): avoid sending chat on IME commit enter (#2795)

## Summary

- Treat IME Enter commit events with keyCode/which 229 as composition
events in RichTextInput.
- Keep normal Enter-to-send and Shift+Enter newline behavior unchanged.
- Add a regression test for IME Enter committing preedit text without
triggering submit.

## Tests

- `./node_modules/.bin/vitest run
tests/unit/components/RichTextInput.unit.spec.tsx`
- `./node_modules/.bin/tsc --noEmit --target ES2022 --module ESNext
--moduleResolution bundler --jsx react-jsx --types react
src/components/rich-text-input/hooks/useRichTextKeyboard.ts`
- `git diff --check --
web/app/src/components/rich-text-input/hooks/useRichTextKeyboard.ts
web/app/tests/unit/components/RichTextInput.unit.spec.tsx`

## Notes

- `bash scripts/verify-web.sh
web/app/src/components/rich-text-input/hooks/useRichTextKeyboard.ts
web/app/tests/unit/components/RichTextInput.unit.spec.tsx` could not
complete locally because its `pnpm exec` steps hit
`ERR_PNPM_MISSING_TARBALL_INTEGRITY` for
`xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`; the
verifier's governance guards passed before that dependency-resolution
failure.
```

**PR body:**

## Summary

- Treat IME Enter commit events with keyCode/which 229 as composition events in RichTextInput.
- Keep normal Enter-to-send and Shift+Enter newline behavior unchanged.
- Add a regression test for IME Enter committing preedit text without triggering submit.

## Tests

- `./node_modules/.bin/vitest run tests/unit/components/RichTextInput.unit.spec.tsx`
- `./node_modules/.bin/tsc --noEmit --target ES2022 --module ESNext --moduleResolution bundler --jsx react-jsx --types react src/components/rich-text-input/hooks/useRichTextKeyboard.ts`
- `git diff --check -- web/app/src/components/rich-text-input/hooks/useRichTextKeyboard.ts web/app/tests/unit/components/RichTextInput.unit.spec.tsx`

## Notes

- `bash scripts/verify-web.sh web/app/src/components/rich-text-input/hooks/useRichTextKeyboard.ts web/app/tests/unit/components/RichTextInput.unit.spec.tsx` could not complete locally because its `pnpm exec` steps hit `ERR_PNPM_MISSING_TARBALL_INTEGRITY` for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`; the verifier's governance guards passed before that dependency-resolution failure.

