---
title: "自定义 Agent 上传界面按钮文字修正"
type: "Bug Fix"
priority: "低"
date: "2026-05-27"
status: "待审核"
channels: ""
---

# 自定义 Agent 上传界面按钮文字修正

## 核心宣传点

上传自定义 Agent 对话框中，"Link" 按钮已更名为 "Code"，更准确反映其功能。

## 原始内容

**仓库**: SerendipityOneInc/ecap-workspace  
**SHA**: [2ffed1da](https://github.com/SerendipityOneInc/ecap-workspace/commit/2ffed1da907ec1c7fd7824e2f1aeee6397843872)
**PR**: [#1983](https://github.com/SerendipityOneInc/ecap-workspace/pull/1983)  
**作者**: tim-srp  
**日期**: 2026-05-27T09:16:11Z

**Commit Message:**

```
fix(web): rename "Link" to "Code" in custom agent upload dialog (#1983)

## Summary
- Rename "Link" label to "Code" in the Upload Custom Agent dialog
- The remote path type accepts a base64-encoded URL (a code), not a raw
link — the label was misleading

## Changes
- `PublishCreateModal.tsx`: Tab button "Link" → "Code", input label
"Link *" → "Code *"
- `PublishDetailModal.tsx`: Detail view label "Link" → "Code"

## Test plan
- [ ] Open Upload Custom Agent dialog, select remote type — tab shows
"Code", field label shows "Code *"
- [ ] View detail of an existing remote custom agent — label shows
"Code"

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```


**PR Description:**

## Summary
- Rename "Link" label to "Code" in the Upload Custom Agent dialog
- The remote path type accepts a base64-encoded URL (a code), not a raw link — the label was misleading

## Changes
- `PublishCreateModal.tsx`: Tab button "Link" → "Code", input label "Link *" → "Code *"
- `PublishDetailModal.tsx`: Detail view label "Link" → "Code"

## Test plan
- [ ] Open Upload Custom Agent dialog, select remote type — tab shows "Code", field label shows "Code *"
- [ ] View detail of an existing remote custom agent — label shows "Code"

🤖 Generated with [Claude Code](https://claude.com/claude-code)
