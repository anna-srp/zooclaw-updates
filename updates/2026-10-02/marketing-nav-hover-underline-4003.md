---
title: "官网导航改用下划线提示 hover 与当前项，页眉 Get Started 按钮留白加大"
type: "体验优化"
priority: "低"
date: "2026-10-02"
status: "待审核"
channels: ""
---

# 官网导航改用下划线提示 hover 与当前项，页眉 Get Started 按钮留白加大

## 核心宣传点

官网顶层导航以前靠降低文字不透明度来表示 hover，辨识度偏弱。现在 Products、Solutions、Pricing、Enterprise、Developer、Resources 在 hover 时显示 2px 下划线，键盘焦点和菜单展开态用同一套反馈，并且尊重系统的「减少动态效果」设置。桌面下拉菜单补齐了列表项焦点背景和 Solutions 分组标题的 hover / 焦点背景；手机导航也补上分组标题与 Pricing、Enterprise 等顶层链接的 hover / 焦点背景，禁用项不再误显示高亮。页眉主按钮 Get Started 的左右内边距从 8px 增加到 16px，窄屏下页眉不会横向溢出。

## 分级

- 内部：P2
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary

官网顶层导航原先通过降低文字不透明度反馈 hover，辨识度偏弱。现在使用细下划线提示当前项目，并为页眉主按钮增加留白。

- 桌面导航
`Products`、`Solutions`、`Pricing`、`Enterprise`、`Developer`、`Resources`：hover
显示 2px 下划线，键盘焦点和菜单展开态使用同一反馈；支持减少动态效果设置。
- 桌面下拉菜单：补齐列表项的焦点背景和 Solutions 分组标题的 hover / 焦点背景；共享导航文字保持完整对比度。
- 移动导航：补齐分组标题与 Pricing、Enterprise 等顶层链接的 hover / 焦点背景；禁用项不显示高亮。
- 桌面页眉 `Get Started`：左右内边距由 8px 增至 16px。

以上变更通过 `LandingHeader`、`LandingMobileNav` 和 `LandingNavItem`
覆盖使用共享页眉的官网营销页面。

## Test plan

- [x] `bash scripts/verify-web.sh`：TypeScript、ESLint 和仓库治理检查通过。
- [x] 提交钩子全量 ESLint 通过。
- [x] 本地浏览器检查导航反馈、菜单展开状态和键盘焦点；最终版本在 1117px 视口验证按钮左右留白为 16px，页眉布局无横向溢出。
- [x] 首轮在 1200px、1440px 视口检查导航项无重叠。
- [x] 根据 Tim review，在 1000px 本地页面验证移动菜单 Pricing 链接的键盘焦点背景已生效，并重新运行
`verify-web.sh` 与推送前检查。

本次为样式调整，未新增单元测试；验证脚本的 Vitest 定向筛选未匹配到对应测试文件。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `b9197fa39664180f45a7c7b992e5ccff4546648c`
- PR: #4003
- 作者：david-srp
- 日期：2026-10-02T14:38:23Z

### Commit Message

```
style(marketing): 优化官网导航反馈与页眉按钮留白 (#4003)

## Summary

官网顶层导航原先通过降低文字不透明度反馈 hover，辨识度偏弱。现在使用细下划线提示当前项目，并为页眉主按钮增加留白。

- 桌面导航
`Products`、`Solutions`、`Pricing`、`Enterprise`、`Developer`、`Resources`：hover
显示 2px 下划线，键盘焦点和菜单展开态使用同一反馈；支持减少动态效果设置。
- 桌面下拉菜单：补齐列表项的焦点背景和 Solutions 分组标题的 hover / 焦点背景；共享导航文字保持完整对比度。
- 移动导航：补齐分组标题与 Pricing、Enterprise 等顶层链接的 hover / 焦点背景；禁用项不显示高亮。
- 桌面页眉 `Get Started`：左右内边距由 8px 增至 16px。

以上变更通过 `LandingHeader`、`LandingMobileNav` 和 `LandingNavItem`
覆盖使用共享页眉的官网营销页面。

## Test plan

- [x] `bash scripts/verify-web.sh`：TypeScript、ESLint 和仓库治理检查通过。
- [x] 提交钩子全量 ESLint 通过。
- [x] 本地浏览器检查导航反馈、菜单展开状态和键盘焦点；最终版本在 1117px 视口验证按钮左右留白为 16px，页眉布局无横向溢出。
- [x] 首轮在 1200px、1440px 视口检查导航项无重叠。
- [x] 根据 Tim review，在 1000px 本地页面验证移动菜单 Pricing 链接的键盘焦点背景已生效，并重新运行
`verify-web.sh` 与推送前检查。

本次为样式调整，未新增单元测试；验证脚本的 Vitest 定向筛选未匹配到对应测试文件。
```

来源：SerendipityOneInc/ecap-workspace @ b9197fa3，PR #4003，作者 david-srp。
