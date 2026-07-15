---
title: "知识库选择器显示「共享给我」的库（只读）"
type: "体验优化"
priority: "中"
date: "2026-07-14"
status: "待审核"
channels: ""
---

# 知识库选择器显示「共享给我」的库（只读）

## 核心宣传点
被他人共享给你的知识库会在选择器的「共享给我」分组里出现，可只读查看，不会再是一片空白。

## 原始内容
### PR #2858 — feat(kb-sharing): show shared-with-me libraries read-only in the selector (#2858)
作者: kyle-srp | https://github.com/SerendipityOneInc/ecap-workspace/pull/2858

## What

Shared-with-me libraries (proxy `role: "editor"`) appear in the Library selector under a **Shared with me** optgroup. Selecting one is read-only:

- no Delete button, no Sharing panel (owner controls)
- uploads refused client-side with a clear message — upstream is owner-only anyway (S1.3); this replaces a raw 403 with a friendly toast

Editors previously saw a completely empty KB page and couldn't confirm what they'd been handed. Installers still see nothing (search-only by design — locked by proxy test).

## Wire

`KnowledgeBaseLibrary.role?: 'owner' | 'editor'` — optional; an older proxy (no role field) keeps today's fully-owned behavior (regression-tested). Pairs with SerendipityOneInc/ecap-proxy-service#150. Any deploy order safe.

## Tests (TDD, red first)

- shared library renders under its own optgroup
- selected shared library: no delete / no grants panel
- upload into shared library blocked, `upload()` never called
- role-less libraries stay fully owned (older-proxy regression)

## Note

Branches from main; expect a small merge with #2854 (document Library column) in `KnowledgeBaseClient.tsx` — both touch the selector area.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
