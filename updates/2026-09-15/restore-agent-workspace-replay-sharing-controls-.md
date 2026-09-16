---
title: "fix(chat): restore Agent workspace replay sharing controls (#3735)"
type: "Bug 修复"
priority: "高"
date: "2026-09-15"
status: "待审核"
channels: ""
---

# fix(chat): restore Agent workspace replay sharing controls (#3735)

## 核心宣传点

## Summary

修复 Agent 工作区点击 Share 后能选择消息，却看不到后续操作的问题。分享操作栏现在位于聊天列底部，选择模式下替换输入框；窄屏时自动换行，确保取消和 Share 按钮可见。展开文件预览时，操作栏仍限制在聊天列内。

## Root cause

PR #3724 将 `ChatShareFlowFrame` 包在整个满高工作区外面，导致它追加的操作栏排在可视区域下方；页面也未向聊天组件传递分享模式对应的 `hideComposer`。同时，操作栏固定高度且不换行，窄屏下 Share 按钮会横向溢出。

本次将分享框架移到聊天列内，连接分享状态与输入框显隐，并允许操作栏随可用宽度换行。仅涉及前端，无需后端部署或数据修改。

## Test plan

- [x] 49 项相关现有单元测试通过，覆盖工作区聊天组件、replay 选择状态、操作栏、复选框与分享弹窗；最终改动对应测试已复测。
- [x] TypeScript、改动文件 ESLint、前端治理检查及 `git diff --check` 通过。
- [x] 本地真实浏览器验证桌面 1440×900、平板 768×700、手机 390×844：操作栏及按钮均在可视区域内。
- [x] 验证单选、全选、清空、取消后恢复输入框，以及生成分享链接弹窗；请求仅包含选中的消息。
- [x] 验证展开文件预览时操作栏不越入预览面板。

浏览器验证使用模拟对话；创建 replay 接口返回模拟响应，用于验证前端请求与弹窗。未创建生产分享链接，也未验证真实后端持久化。


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `8baf71341395aeb415b84e3ab3fe96178936015c`
- PR: #3735
- 作者：kaka-srp
- 日期：2026-09-15T08:32:48Z

### Commit Message

```
fix(chat): restore Agent workspace replay sharing controls (#3735)

## Summary

修复 Agent 工作区点击 Share
后能选择消息，却看不到后续操作的问题。分享操作栏现在位于聊天列底部，选择模式下替换输入框；窄屏时自动换行，确保取消和 Share
按钮可见。展开文件预览时，操作栏仍限制在聊天列内。

## Root cause

PR #3724 将 `ChatShareFlowFrame`
包在整个满高工作区外面，导致它追加的操作栏排在可视区域下方；页面也未向聊天组件传递分享模式对应的
`hideComposer`。同时，操作栏固定高度且不换行，窄屏下 Share 按钮会横向溢出。

本次将分享框架移到聊天列内，连接分享状态与输入框显隐，并允许操作栏随可用宽度换行。仅涉及前端，无需后端部署或数据修改。

## Test plan

- [x] 49 项相关现有单元测试通过，覆盖工作区聊天组件、replay 选择状态、操作栏、复选框与分享弹窗；最终改动对应测试已复测。
- [x] TypeScript、
```
