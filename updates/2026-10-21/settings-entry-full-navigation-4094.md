---
title: "修复：头像菜单进设置只剩 General，现已恢复完整设置导航"
type: "Bug Fix"
priority: "高"
date: "2026-10-21"
status: "待审核"
channels: ""
---

# 修复：头像菜单进设置只剩 General，现已恢复完整设置导航

## 核心宣传点

上一版为接入 Cookie 管理，把头像菜单里的 Settings 指向了只含 General 的旧单页设置视图，导致 Usage、Billing、API Keys 和组织设置等导航全部消失。本次把 Settings 入口恢复到完整设置页，并把折叠侧栏点击头像的目标地址一并统一；由于完整设置页复用同一个 General 面板，上一版接通的 Cookie 管理功能依然可用。同时补了桌面、移动端和折叠侧栏的端到端回归，从真实入口进入设置后逐项检查导航，并实际开关 Cookie 管理弹窗。个人账号、团队管理员和成员的导航权限差异也在用例中覆盖。

## 分级

- 内部：P1
- 外部：A
- toB 相关：是
- 发布状态：已合并待发版

## 备注

仅需 Web 前端发布。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `35a811e9d3c3731b2447ddd21992ed1c42d57628`
- PR: #4094
- 作者：shana-srp
- 日期：2026-10-21T08:31:03Z

### Commit Message

```
fix(settings): 恢复 Settings 入口的完整导航 (#4094)

## Summary
- 修复 #4090 引入的设置入口回归：头像菜单 Settings 从 `/profile` 恢复进入完整的 `/identity`
设置页，并统一折叠侧栏点击头像的目标地址。
- 恢复 General、Usage、Billing，以及按权限显示的 API Keys 和组织设置导航。完整设置页复用同一个
GeneralTab，因此上一版接通的 Cookie 管理功能仍然可用。
- 新增桌面、移动端和折叠侧栏端到端回归，从实际入口进入 Settings 后检查完整导航，并实际打开和关闭 Cookie 管理弹窗。

## Root cause
`/profile` 是只包含 General 的旧单页设置视图。#4090 为接入 Cookie 管理改用了这个地址，导致 Settings
入口失去其他设置导航。原有 `/identity` 页面已经复用 GeneralTab，恢复正确入口即可同时保留完整导航和 Cookie
管理。审查中同时确认折叠侧栏的头像入口也独立指向 `/profile`，一并统一到完整设置页。

## Test plan
- [x] 前端治理规则、TypeScript 检查和改动文件 ESLint 通过。
- [x] 11 个测试文件、336 条相关单测通过，覆盖设置入口、个人账号 / 团队管理员 / 成员导航权限和 Cookie 管理。
- [x] 7 条完整本地端到端回归通过（team-admin 模拟账号）：覆盖 1440px / 390px /
折叠侧栏实际入口、完整导航、Cookie 弹窗焦点恢复、组织资料保存、成员管理、配额持久化和手机导航。统一为本地设置测试准备有效的 Cookie
偏好，避免首次访问提示遮挡操作。
- [x] 逐个点击 General、Usage、Billing、API Keys 验证实际页面内容，并通过本地截图核对完整导航。
- [x] 最新提交 GitHub Actions 完整构建、全量测试及覆盖率、质量检查和两轮自动审查通过；PR 代码扫描无告警。

仅需 Web 前端发布。

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

