---
title: "知识库上传页新增「所属库」列与独立筛选"
type: "体验优化"
priority: "中"
date: "2026-07-14"
status: "待审核"
channels: ""
---

# 知识库上传页新增「所属库」列与独立筛选

## 核心宣传点
上传页文档列表新增所属库一列并支持按库筛选，不再出现同一文档在每个库下都显示的混淆。

## 原始内容
### PR #2854 — feat(knowledge-base): document Library column + independent per-library filter (#2854)
作者: kyle-srp | https://github.com/SerendipityOneInc/ecap-workspace/pull/2854

## What

Fixes a UX ambiguity found during staging E2E: the upload-page document list is org-wide, but the Library dropdown only sets the **upload target** — it didn't scope the list, so a document appeared under every library selection.

Now:
- **Library column** — each document row shows which library it belongs to (name resolved from the loaded library list; `—` when untagged / org-level).
- **Independent filter** above the list (`All` / `No library` / each library) — narrows the view *without* touching the upload-target selector. Default `All` keeps "see everything" as the landing view.

The list stays org-wide (server resolves org from token); filtering is client-side on the `kb_id` now returned per document.

## Depends on

`ecap-proxy-service#147` — surfaces each document's `kb_id` in `GET /knowledge-base/documents`. Backward-compatible: `kb_id` is optional on the client type, so this degrades to `—`/unfiltered against an older proxy.

## Test

- `DocumentList`: renders the library name for a tagged doc, `—` for untagged.
- `KnowledgeBaseClient`: the filter narrows the list to a library / to untagged, independent of the upload selector.
- verify-web green (tsc + vitest + eslint).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
