---
title: "修复：下载图片/视频时文件名变成一串时间戳，原始文件名丢失"
type: "Bug Fix"
priority: "中"
date: "2026-08-24"
status: "待审核"
channels: ""
---

# 修复：下载图片/视频时文件名变成一串时间戳，原始文件名丢失

## 核心宣传点

在聊天附件、回放、我的上传、Markdown 媒体、素材面板和图片画廊里下载图片或视频时，原始文件名会丢失，统一变成 gensmo-时间戳.png 这种旧品牌的兜底名，一次下载多张就完全分不清谁是谁。现在这些入口都会把原始文件名一路带到下载按钮；确实拿不到文件名时的兜底名也改成了 zooclaw-时间戳。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `ea8ea177ecb6bf1f2104afcaf01a996b236fc797`
- PR: #3480
- 作者: rayrain-srp
- 日期: 2026-08-24T07:23:54Z

### Commit Message

```
fix(web): preserve media download filenames (#3480)

## Summary

- Preserve original image and video filenames across Mattermost
attachments, replay, My Uploads, Markdown media, AssetsPanel, and
gallery navigation.
- Replace the legacy `gensmo-<timestamp>` fallback with
`zooclaw-<timestamp>` in both the browser download helper and download
proxy.
- Add regression coverage for filename propagation, raw HTML table-image
galleries, and the ZooClaw fallback.
- Linear:
[ECA-1392](https://linear.app/srpone/issue/ECA-1392/zoowork-%E4%B8%8B%E8%BD%BD%E5%9B%BE%E7%89%87%E6%97%B6%E6%96%87%E4%BB%B6%E5%90%8D%E4%BB%8D%E4%BD%BF%E7%94%A8-gensmo-timestamppng)

## Root cause

Mattermost attachment views already carried `file.name`, but the
image-preview open call forwarded only the resolved URL. The preview
context and gallery item contract also had no filename field, so the
download button received `undefined` and fell back to the old
Gensmo-branded name. Markdown and other shared download surfaces had the
same missing-name path.

## Test plan

- [x] `VITEST_MAX_WORKERS=1 bash scripts/verify-web.sh <changed web/app
paths>` (guards, full TypeScript, 351/351 related tests, ESLint)
- [x] Review follow-up scoped verification (126/126 tests, full
TypeScript, ESLint)
- [x] `bash scripts/verify-changed.sh`
- [x] Pre-commit and pre-push repository hooks
- [x] GitHub CI, including full `web-quality / test`, build, CodeQL, and
auto-review (41/41 settled without failures)

Note: the initial unscoped local Vitest run passed 9,016 tests and hit
two unrelated load-sensitive timeouts. Both affected files passed in
isolated single-worker reruns, and GitHub's full Web test suite is
green.
```

### PR Body

## Summary

- Preserve original image and video filenames across Mattermost attachments, replay, My Uploads, Markdown media, AssetsPanel, and gallery navigation.
- Replace the legacy `gensmo-<timestamp>` fallback with `zooclaw-<timestamp>` in both the browser download helper and download proxy.
- Add regression coverage for filename propagation, raw HTML table-image galleries, and the ZooClaw fallback.
- Linear: [ECA-1392](https://linear.app/srpone/issue/ECA-1392/zoowork-%E4%B8%8B%E8%BD%BD%E5%9B%BE%E7%89%87%E6%97%B6%E6%96%87%E4%BB%B6%E5%90%8D%E4%BB%8D%E4%BD%BF%E7%94%A8-gensmo-timestamppng)

## Root cause

Mattermost attachment views already carried `file.name`, but the image-preview open call forwarded only the resolved URL. The preview context and gallery item contract also had no filename field, so the download button received `undefined` and fell back to the old Gensmo-branded name. Markdown and other shared download surfaces had the same missing-name path.

## Test plan

- [x] `VITEST_MAX_WORKERS=1 bash scripts/verify-web.sh <changed web/app paths>` (guards, full TypeScript, 351/351 related tests, ESLint)
- [x] Review follow-up scoped verification (126/126 tests, full TypeScript, ESLint)
- [x] `bash scripts/verify-changed.sh`
- [x] Pre-commit and pre-push repository hooks
- [x] GitHub CI, including full `web-quality / test`, build, CodeQL, and auto-review (41/41 settled without failures)

Note: the initial unscoped local Vitest run passed 9,016 tests and hit two unrelated load-sensitive timeouts. Both affected files passed in isolated single-worker reruns, and GitHub's full Web test suite is green.

