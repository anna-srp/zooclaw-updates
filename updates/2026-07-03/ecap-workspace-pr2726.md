---
title: "知识库支持一次上传多个文件"
type: "Bug Fix"
priority: "中"
date: "2026-07-03"
status: "待审核"
channels: ""
---

# 知识库支持一次上传多个文件

## 核心宣传点

知识库上传现在真正支持多选和多文件拖拽，一次能传多个文档，不再只上传第一个。

## 原始内容

fix(knowledge-base): support multi-file upload (#2726)

## Summary

Fixes the Knowledge Base upload so it actually accepts **multiple
files**, which the UI implied but the code never supported.

Two root causes in `UploadDropzone.tsx`:
- the `<input type="file">` had no `multiple` attribute → the OS picker
allowed only one file;
- the drag-and-drop handler passed the list to `pick()`, which read only
`files?.[0]` → dragging several files uploaded just the first.

## Changes

- **`UploadDropzone.tsx`** — add `multiple` to the input; rewrite
`pick()` to iterate the whole `FileList` (picker + drop), split into
accepted vs. rejected, and dedupe rejection reasons (three unsupported
files → one toast). Prop renamed `onFile` → `onFiles: (files: File[]) =>
void`.
- **`KnowledgeBaseClient.tsx`** — `handleFile` → `handleFiles`; upload
accepted files **sequentially** (each success invalidates the documents
query; the hook's existing 10s `staleTime` already anticipates
back-to-back uploads). In a batch, failure toasts name the file;
single-file behavior is unchanged.
- **`locales/en.ts` / `locales/zh.ts`** — pluralize dropzone copy
("Choose files" / "Drag files here" / "拖拽文件到此(可多选)") and fix the
empty-state hint direction ("below" → "above", the upload box is above
the list).
- **`UploadDropzone.unit.spec.tsx`** — migrate to `onFiles`, assert the
`File[]` payload, and add coverage for multi-select, multi-drop,
`input.multiple`, mixed accept/reject batches, and reason dedup.

## Testing

- `scripts/verify-web.sh` on the changed files: **tsc clean** (changed
files), **vitest 3900 passed**, **eslint passed**.
- Manually verified against the staging backend: multi-select picker,
multi-file drag/drop, and mixed valid/invalid batches all behave
correctly.

Closes #2724

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

---

**PR Description:**

## Summary

Fixes the Knowledge Base upload so it actually accepts **multiple files**, which the UI implied but the code never supported.

Two root causes in `UploadDropzone.tsx`:
- the `<input type="file">` had no `multiple` attribute → the OS picker allowed only one file;
- the drag-and-drop handler passed the list to `pick()`, which read only `files?.[0]` → dragging several files uploaded just the first.

## Changes

- **`UploadDropzone.tsx`** — add `multiple` to the input; rewrite `pick()` to iterate the whole `FileList` (picker + drop), split into accepted vs. rejected, and dedupe rejection reasons (three unsupported files → one toast). Prop renamed `onFile` → `onFiles: (files: File[]) => void`.
- **`KnowledgeBaseClient.tsx`** — `handleFile` → `handleFiles`; upload accepted files **sequentially** (each success invalidates the documents query; the hook's existing 10s `staleTime` already anticipates back-to-back uploads). In a batch, failure toasts name the file; single-file behavior is unchanged.
- **`locales/en.ts` / `locales/zh.ts`** — pluralize dropzone copy ("Choose files" / "Drag files here" / "拖拽文件到此(可多选)") and fix the empty-state hint direction ("below" → "above", the upload box is above the list).
- **`UploadDropzone.unit.spec.tsx`** — migrate to `onFiles`, assert the `File[]` payload, and add coverage for multi-select, multi-drop, `input.multiple`, mixed accept/reject batches, and reason dedup.

## Testing

- `scripts/verify-web.sh` on the changed files: **tsc clean** (changed files), **vitest 3900 passed**, **eslint passed**.
- Manually verified against the staging backend: multi-select picker, multi-file drag/drop, and mixed valid/invalid batches all behave correctly.

Closes #2724

