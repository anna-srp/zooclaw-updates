---
title: "Artifact 预览缓存刷新统一修复"
type: "Bug Fix"
priority: "中"
date: "2026-06-04"
status: "待审核"
channels: ""
sha: "b19bc44b47fbfff3c468a27c6737cadabad281ca"
repo: "ecap-workspace"
pr: "2207"
---

# Artifact 预览缓存刷新统一修复

## 核心宣传点

修复了 Artifact（如生成的网页/文件）重新生成后，预览窗口可能仍显示旧版本的问题，现在刷新后始终展示最新内容。

## 原始内容

### Commit Message

```
fix(web): unify artifact preview cache buster (#2207)

## Summary
- Reintroduce a unified `_t=<timestamp>` cache-buster for artifact proxy
preview URLs.
- Move cache-busting from `HtmlRenderer` into `ArtifactPreview` so all
artifact preview renderers share the same behavior.
- Remove the HTML-only `_cb` parameter and keep non-artifact/presigned
URLs unchanged.

## Root cause
Artifact previews can serve stale content when the browser caches the
same artifact proxy URL after a regenerated file keeps the same path.
HTML previously had a renderer-local `_cb` workaround, but other preview
types still used unchanged artifact proxy URLs. A prior global `_t`
implementation was removed because it also modified
presigned/non-artifact URLs, which can break S3/R2 signature validation.
This change applies `_t` only to known artifact proxy hosts.

## Test plan
- [x] `git diff --check`
- [ ] Not run: app instructions say not to run tests/lint/build unless
explicitly requested.
```

### PR Description

## Summary
- Reintroduce a unified `_t=<timestamp>` cache-buster for artifact proxy preview URLs.
- Move cache-busting from `HtmlRenderer` into `ArtifactPreview` so all artifact preview renderers share the same behavior.
- Remove the HTML-only `_cb` parameter and keep non-artifact/presigned URLs unchanged.

## Root cause
Artifact previews can serve stale content when the browser caches the same artifact proxy URL after a regenerated file keeps the same path. HTML previously had a renderer-local `_cb` workaround, but other preview types still used unchanged artifact proxy URLs. A prior global `_t` implementation was removed because it also modified presigned/non-artifact URLs, which can break S3/R2 signature validation. This change applies `_t` only to known artifact proxy hosts.

## Test plan
- [x] `git diff --check`
- [ ] Not run: app instructions say not to run tests/lint/build unless explicitly requested.

