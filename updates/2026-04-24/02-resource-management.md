---
title: "资源面板：聊天页直接浏览 Workspace 文件 & 历史上传"
type: "新功能上线"
priority: "高"
date: "2026-04-24"
status: "待审核"
channels: "Discord+changelog"
---
# 资源面板：聊天页直接浏览 Workspace 文件 & 历史上传

## 核心宣传点
聊天页新增资源面板，可以随时浏览 Workspace 里的文件，也能查看和复用之前上传过的附件——不用再重复上传，文件管理更顺手。

## 原始内容

feat: resource management — workspace file browser + upload assets tracking (#1134)

### Summary
- Add **Resources Panel** sidebar to chat page for browsing workspace files and user uploads
- Redesign **attachment button** with popover for referencing existing files or uploading new ones
- Store user upload metadata in MongoDB for retrieval and reuse across conversations
- Proxy FastClaw's new `GET /files/list` endpoint for real-time workspace directory browsing

### Architecture
```
Frontend (ResourcesPanel)
  → claw-interface (GET /conversation/workspace/files)
    → FastClaw (GET /bots/{id}/files/list)

Frontend (MyUploadsTab / UploadPopover)
  → claw-interface (GET/POST /conversation/assets)
    → MongoDB (ecap-conversation-assets)
```
