---
title: "体验优化：Agent 安装链接弹窗去掉重复的「关闭」按钮"
type: "体验优化"
priority: "低"
date: "2026-10-10"
status: "待审核"
channels: ""
---

# 体验优化：Agent 安装链接弹窗去掉重复的「关闭」按钮

## 核心宣传点

Agent 安装链接弹窗此前在底部还放了一个「关闭」按钮，与右上角的 × 功能完全重复，容易让用户误以为是两种不同操作。这次移除底部多余的关闭按钮，底部只保留「发布」和「创建安装链接」两个真正的操作，关闭统一用右上角的 ×。相关的关闭/重开测试也改为走右上角控件。纯前端细节清理，不影响发布与安装链接本身的行为，无需后端配套发版。

## 分级

- 内部：P3
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## 备注

作者本地完整 TypeScript 检查未通过（worktree 复用了旧检出的依赖，解析到过期的 design-system / chat-ui 契约），依赖安装与类型、构建以 CI 结果为准。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `d4d774a456b176a1dbf9df8dc325d98a226a8f49`
- PR: #4048
- 作者：kaka-srp
- 日期：2026-10-10T08:31:49Z

### Commit Message

```
fix(agents): remove redundant install link close button (#4048)

## Summary
Remove the redundant footer Close button from the Agent install link
dialog. The existing top-right × closes the dialog, while the footer
keeps Publish and Create install link.

## Root cause
The dialog offered two controls for the same close action. Remove the
unused footer label and update the existing close/reopen test to use the
top-right control.

## Test plan
- [x] Related publication tests: 8 passed.
- [x] ESLint on all three changed files.
- [x] Git diff whitespace check.
- [x] Frontend governance guards.
- Local full TypeScript check did not pass: this `--no-node` worktree
reused dependencies from the older primary checkout, resolving stale
`@zooclaw/design-system` / `@zooclaw/chat-ui` contracts and missing
newer dependencies (for example `fast-xml-parser`). CI will validate the
complete dependency installation, types, and build.
```

