---
title: "feat(assets): preview generated files in chat artifact sidebar (#3751)"
type: "新功能"
priority: "中"
date: "2026-09-16"
status: "待审核"
channels: ""
---

# feat(assets): preview generated files in chat artifact sidebar (#3751)

## 核心宣传点

在 Artifacts 里点击 AI 生成的文件不再新开标签页触发下载，而是直接在聊天侧栏预览，并支持切换文件、关闭、调整宽度、刷新和下载。

## PR 说明

## Summary
Clicking AI-generated files in Artifacts previously opened the file URL in a new tab, often triggering a download. Browse mode now opens the existing Chat artifact sidebar, with file switching, close, resize, refresh and download controls.

- Reuse `ArtifactsSidebar` and its existing file renderers; no backend changes.
- Size the file grid by available container width so multiple cards fit naturally alongside the preview. On small screens the preview overlays the list.
- Preserve My uploads and attachment-selector behavior.

## Test plan
- [x] 52 targeted AssetLibraryContent and UploadsFeed tests passed, including grid/list preview callbacks without a popup, file switching, close/reopen and tab switching.
- [x] Whole-app TypeScript check passed.
- [x] ESLint for all changed files and frontend governance guards passed.
- [x] `git diff --check` passed.
- [ ] Browser-level visual validation has not been performed.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `ae21ecf4f4138edfd9174703f5b530f5ece2a69c`
- PR: #3751
- 作者：tim-srp
- 日期：2026-09-16T07:56:02Z

### Commit Message

```
feat(assets): preview generated files in chat artifact sidebar (#3751)

## Summary
Clicking AI-generated files in Artifacts previously opened the file URL
in a new tab, often triggering a download. Browse mode now opens the
existing Chat artifact sidebar, with file switching, close, resize,
refresh and download controls.

- Reuse `ArtifactsSidebar` and its existing file renderers; no backend
changes.
- Size the file grid by available container width so multiple cards fit
naturally alongside the 
```
