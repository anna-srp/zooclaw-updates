---
title: "一键复制知识库 Library ID"
type: "体验优化"
priority: "低"
date: "2026-07-14"
status: "待审核"
channels: ""
---

# 一键复制知识库 Library ID

## 核心宣传点
知识库选择器旁新增一键复制按钮，方便在 Agent Builder 里填写 kb_ref 所需的库 ID。

## 原始内容
### PR #2861 — feat(kb-sharing): one-click copy of the selected library id (#2861)
作者: kyle-srp | https://github.com/SerendipityOneInc/ecap-workspace/pull/2861

## What

A ghost clipboard button next to the Library selector copies the selected library's raw `kb_id`, with success/failure toasts (en/zh).

## Why

Declaring `kb_ref: { "kb_id": ... }` in Agent Builder needs the 32-char id, but the KB page only shows library names — the only way to get the id was digging through API responses.

## Tests (TDD, red first)

- button hidden with no selection; appears on selection; click writes the kb_id via `navigator.clipboard` (installed/restored per repo jsdom guidance)

## Note

Touches the same selector row as #2858 — whichever merges second gets a trivial conflict I'll resolve.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
