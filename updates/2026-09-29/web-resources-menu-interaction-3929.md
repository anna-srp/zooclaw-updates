---
title: "官网 Resources 菜单改为点击展开，入口精简为 Blog、Docs、ZooData"
type: "Improvement"
priority: "低"
date: "2026-09-29"
status: "待审核"
channels: ""
---

# 官网 Resources 菜单改为点击展开，入口精简为 Blog、Docs、ZooData

## 核心宣传点

官网导航里的 Resources 虽然有下拉菜单，但标题本身还是个外链，点一下会直接跳走打开 Tips，跟菜单的预期完全不符。现在它改成按钮，点击展开或收起菜单，并支持点击外部区域、失焦和 Escape 关闭。下拉里的 Learn 和 What’s New 被移除，只保留 Blog、Docs、ZooData，菜单高度随内容收缩。首页、Pricing 等页面共用这套导航，改动统一生效；Solutions 的链接行为和页脚入口保持不变。

## 分级

- 内部：P2
- 外部：C
- toB 相关：否
- 发布状态：已随正式 release 上线

## PR 说明

## 问题与修改

官网导航中的 Resources 虽然有下拉菜单，但标题仍是外链，点击后会直接打开 Tips。改为按钮，点击展开或收起菜单，并支持点击外部、失焦和 Escape 关闭。

移除 Resources 下拉菜单中的 Learn 和 What’s New，仅保留 Blog、Docs、ZooData，同时让菜单高度随内容收缩。首页、Pricing 等页面共用导航，统一生效。Solutions 的链接行为及页脚入口保持不变。

## 验证

- 14 个相关单元测试通过，覆盖点击切换、焦点顺序、Escape、外部点击及菜单内容。
- TypeScript、修改文件的 ESLint、仓库前端治理检查通过。
- `git diff --check` 通过。
- 本地首页返回 HTTP 200；浏览器交互验证因用户正在操作 Chrome 而中断，未完成实测。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `faa0dfbd4b662210657878af7fac43afb42b10f0`
- PR: #3929
- 作者：lynn Zhuang
- 日期：2026-09-29T09:56:22Z

### Commit Message

```
fix(web): 修复官网 Resources 菜单交互并精简入口 (#3929)

## 问题与修改

官网导航中的 Resources 虽然有下拉菜单，但标题仍是外链，点击后会直接打开
Tips。改为按钮，点击展开或收起菜单，并支持点击外部、失焦和 Escape 关闭。

移除 Resources 下拉菜单中的 Learn 和 What’s New，仅保留
Blog、Docs、ZooData，同时让菜单高度随内容收缩。首页、Pricing 等页面共用导航，统一生效。Solutions
的链接行为及页脚入口保持不变。

## 验证

- 14 个相关单元测试通过，覆盖点击切换、焦点顺序、Escape、外部点击及菜单内容。
- TypeScript、修改文件的 ESLint、仓库前端治理检查通过。
- `git diff --check` 通过。
- 本地首页返回 HTTP 200；浏览器交互验证因用户正在操作 Chrome 而中断，未完成实测。
```

来源：SerendipityOneInc/ecap-workspace @ faa0dfbd，PR #3929，作者 lynn Zhuang。
