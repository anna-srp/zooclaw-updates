---
title: "工作区文件与产出物（Artifacts）新增网页浏览、预览与下载"
type: 产品基础功能更新
priority: 中
date: 2026-08-01
status: 待审核
channels: ""
---

## 核心宣传点

现在可以直接在网页端浏览你的工作区文件和已发布产出物（Artifacts），支持列表查看、在线预览与一键下载，历史消息里的旧链接也照常可用。

## 原始内容

**PR #3181 — feat(web): consume V2 artifacts and workspace files**

SHA: `8ee27ed3d6`
作者: Chris@ZooClaw
日期: 2026-08-01T13:11:01Z

### Commit Message / PR Body

## What changed

- adds Artifact list/detail, preview and download UI using stable URLs;
- consumes additive structured refs when present but retains URL-only rendering;
- keeps Files UI independent from Published Artifact snapshots.

## Why

Controlled ecap clients can use Artifact IDs for richer presentation, but forwarded/V1/old-ACS messages still need the same preview and download behavior from URLs alone.

## Validation

- frontend/backend targeted Artifact tests pass;
- the complete stack passes the Python validation recorded in #3180;
- URL-only and structured-ref cases are included in the staging canary defined by SerendipityOneInc/zooclaw-dev#18.

This is PR 2/3 and is based on #3180.
