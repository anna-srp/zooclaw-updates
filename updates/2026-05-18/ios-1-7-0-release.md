---
title: "iOS App v1.7.0 上线：新手引导视频、侧边栏优化、文档内联预览"
type: "产品基础功能更新"
priority: "中"
date: "2026-05-18"
status: "待审核"
channels: ""
---
# iOS App v1.7.0 上线：新手引导视频、侧边栏优化、文档内联预览

## 核心宣传点
iOS 1.7.0 正式发布，全屏欢迎视频引导新用户上手，侧边栏展示最新消息预览，Word/Excel 等 Office 格式文件现在可以直接在 App 内打开预览。

## 原始内容

**Commit**: `7190c28b` | ecap-workspace | 2026-05-18T11:31:52Z  
**PR**: #1710 | feat(ios): 1.7.0 release

---

### Onboarding & 侧边栏

- Redesigned onboarding hero with full-bleed welcome video（全屏欢迎视频）
- Sidebar bottom-nav layout tightened and leading-aligned（侧边栏底部导航收紧）
- Sidebar agent rows show the last channel message as subtitle（侧边栏 Agent 行显示最新消息预览）
- Content panel gets a hairline outline when the sidebar is open（侧边栏展开时内容区域有细线边框）

### Chat 修复

- Inline document preview via `QLPreviewController` for Mattermost file attachments（消息中的附件现在可内联预览）
- In-content artifact links now route through `QLPreviewController`（Office 格式如 .xlsx 现在能正常打开，以前用 Safari 打不开）
- Fixed Mattermost chat author filtering（修复消息来源过滤问题）
- Force fresh SwiftUI identity per message（修复 cell 复用导致助理气泡显示成用户文字的 bug）

### 与 Soulmate Chat markdown 规范对齐（多个 commit）
