---
title: "知识库支持上传 JSON / Markdown 文件"
type: "新功能上线"
priority: "中"
date: "2026-07-14"
status: "待审核"
channels: ""
---

# 知识库支持上传 JSON / Markdown 文件

## 核心宣传点
知识库上传新增支持 .json / .md / .markdown 格式文件。

## 原始内容
### PR #2869 — feat(kb-sharing): accept JSON + Markdown uploads (#2869)
作者: kyle-srp | https://github.com/SerendipityOneInc/ecap-workspace/pull/2869

## ⚠️ RELEASE GATE — deploy proxy first

**SerendipityOneInc/ecap-proxy-service#153 (backend allowlist) MUST be deployed to the target environment BEFORE this PR.** (codex P1, accepted.)

This PR advertises `.json`/`.md`/`.markdown` in the file picker; an old proxy without the paired allowlist rejects them. Worst case is a **failed upload with a server error** (no corruption, no crash — the intended soft-validation degradation, per claude-review). Still, deploy proxy first so users are never offered a type the backend rejects.

Staging order: merge proxy #153 → beta tag → rollout → then merge this.

## What

Accept **JSON** + **Markdown** uploads (+ the `.htm` alias the backend already accepted).

## Why

Vertex AI Search indexes TXT, **JSON**, **Markdown**, PDF, HTML, DOCX, PPTX, XLSX, XLSM ([Google docs](https://docs.cloud.google.com/generative-ai-app-builder/docs/prepare-data)); the allowlist omitted JSON + Markdown. Not added: MP4/video, audio, standalone images, legacy binary Office (`.doc`/`.ppt`/`.xls`) — Vertex doesn't index those.

## Design

Single source of truth `CANONICAL_FORMATS` (one entry per format: label + extension aliases). `ALLOWED_EXTENSIONS` (validation + picker `accept`) and the dropzone hint both derive from it — they can't drift (claude-review note addressed).

## Tests (TDD)

accepts json/md/markdown/htm (case-insensitive) · rejects mp4/doc/png · hint dedupes aliases · accept list includes aliases.

## Pairs with

ecap-proxy-service#153.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
