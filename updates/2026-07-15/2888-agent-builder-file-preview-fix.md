---
title: "修复 Agent Builder 共享输入框在无文件预览时崩溃"
type: "Bug Fix"
priority: "中"
date: "2026-07-15"
status: "待审核"
channels: ""
tags: []
---

# 修复 Agent Builder 共享输入框在无文件预览时崩溃

## 核心宣传点
修复 Agent Builder 里共享对话输入框在没有挂载文件预览组件的界面上直接崩溃（Something went wrong）的问题；有预览的界面继续正常预览，无预览的界面仅禁用预览动作而不再报错。

## 原始内容
### PR #2888 — fix(agent-builder): handle missing file preview provider (#2888)
作者: bill-srp | https://github.com/SerendipityOneInc/ecap-workspace/pull/2888

## Summary
- prevent Agent Builder's shared chat composer from crashing when no `FilePreviewProvider` is mounted
- keep file preview available on surfaces with the provider and disable only the preview action on providerless surfaces
- add regression coverage for rendering previewable attachments without the provider

## Root cause
`GenClawInput` unconditionally called `useFilePreview()`, but Agent Builder intentionally renders the shared composer without an artifacts sidebar or `FilePreviewProvider`. The strict hook therefore threw during render before the expired pack-test preview state could be handled by the page.

Linear: https://linear.app/srpone/issue/ECA-1245/staging-agent-builder-preview-page-something-went-wrong-pack-test

Sentry: https://serendipity-one-inc.sentry.io/issues/7536880272/?environment=staging&project=4510776018075648

## Test plan
- [x] `bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/(chat)/chat/components/GenClawInput.tsx' web/app/tests/unit/app/chat/GenClawInput.unit.spec.tsx web/app/tests/unit/app/chat/GenClawInput-extras.unit.spec.tsx`
- [x] regression test verifies a previewable attachment renders without a preview action when no provider is mounted
- [x] existing provider-backed preview test still opens the file preview and revokes its Blob URL

## 备注
外部B级。本条为 2026-07-15 每日同步补录（原 cron 仅写入 raw，未落 updates/ 与多维表）。
