---
title: "交互卡片未处理时隐藏输入框"
type: "体验优化"
priority: "中"
date: "2026-07-14"
status: "待审核"
channels: ""
---

# 交互卡片未处理时隐藏输入框

## 核心宣传点
当助手发来带按钮/下拉的交互卡片且尚未处理时，主对话输入框会隐藏，引导先完成卡片操作。

## 原始内容
### PR #2864 — feat(web): hide composer for unresolved interactive cards (#2864)
作者: bill-srp | https://github.com/SerendipityOneInc/ecap-workspace/pull/2864

## Linear

N/A

## Summary

- hide the main chat composer while an assistant Mattermost card still exposes button or select actions
- derive the lock from the server-backed message lifecycle so the composer returns when the post becomes a completion banner
- keep the change scoped to the Mattermost-backed main chat; gateway subagent messages do not carry interactive attachments

## Test plan

- [x] `bash scripts/verify-web.sh <changed paths>`
- [x] `bash scripts/verify-changed.sh`
- [x] TDD red/green coverage for main chat, button/select cards, and completion banners
