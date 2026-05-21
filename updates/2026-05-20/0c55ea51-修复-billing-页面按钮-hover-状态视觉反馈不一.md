---
title: "修复 Billing 页面按钮 hover 状态视觉反馈不一致"
type: "Bug Fix"
priority: "低"
date: "2026-05-20"
status: "待审核"
channels: ""
repo: "ecap-workspace"
sha: "0c55ea515e97f45e41efae757622ce13f411217f"
pr: 1762
---
# 修复 Billing 页面按钮 hover 状态视觉反馈不一致

## 核心宣传点

Billing 页面三个操作按钮的鼠标悬停视觉效果现已统一，界面更美观一致。

## 原始内容

### Commit Message

```
fix(billing): 统一 Billing 页面三个 action button 的 hover 视觉反馈 (#1762)

## 概要
Billing 设置页里 **Edit**（Payment Method）、**View all invoices** 和
**Download**（每行发票）三个 button 之前要嘛完全没有 hover 背景、要嘛只是文字微微变淡，跟项目里其他 action
button
  的反馈不一致 —— 用户能点但不知道点到了哪。

三个按钮统一加 `hover:bg-muted` + `rounded-md` + `px-2 py-1`，hover
时呈现一个柔和的圆角灰色背景，反馈层级一致。

- `--muted` 是 shadcn 双 theme 都铺好的语义 token（light `#f4f4f5` / dark
`#21262d`），自动适配 darkmode 无需写 `dark:` 变体
- 行内按钮（Edit / View all invoices）用 `-mr-2` 负 margin 抵消新加的水平
padding，文字仍贴在原来的右边线，不会因为加 padding 看起来"内缩"破坏对齐
- Edit 原本的 `hover:text-foreground/80`（文字变淡）被移除 —— 加了 bg
反馈之后再让文字变淡跟交互语义冲突（hover 该让按钮"更显眼"而不是"更模糊"）

  ## 测试清单
- [ ] `/en/subscription` 进入 Billing 设置页，hover 三个按钮（Edit / View all
invoices / Download），都呈现圆角灰色背景
  - [ ] 切到 dark mode（系统主题或测试切换），hover 背景颜色自动变成暗灰色，不出现纯白色或残留 light token
  - [ ] Edit / View all invoices 按钮文字位置在 hover 时没有位移（`-mr-2` 抵消生效）
  - [ ] Download 按钮多行排列时每行 hover 独立响应，不互相影响

  ## 关于 #1653
本 PR 是 #1653 的内容 port 到最新 main 上的等价分支——原 #1653 的源分支基于 5 天前的 main（在
`#1713 Nest pnpm workspace under web/` 之前），路径是 `web/src/...`；新 main
的对应路径是
`web/app/src/...`，cherry-pick 会全路径冲突。所以手工 port 了同一个 className
改动到新分支上。改动内容 **逐字符等价**于 #1653 的 commit `eb9c6acf`。原 #1653 可以关闭。

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

 ## 概要
  Billing 设置页里 **Edit**（Payment Method）、**View all invoices** 和 **Download**（每行发票）三个 button 之前要嘛完全没有 hover 背景、要嘛只是文字微微变淡，跟项目里其他 action button
  的反馈不一致 —— 用户能点但不知道点到了哪。

  三个按钮统一加 `hover:bg-muted` + `rounded-md` + `px-2 py-1`，hover 时呈现一个柔和的圆角灰色背景，反馈层级一致。

  - `--muted` 是 shadcn 双 theme 都铺好的语义 token（light `#f4f4f5` / dark `#21262d`），自动适配 darkmode 无需写 `dark:` 变体
  - 行内按钮（Edit / View all invoices）用 `-mr-2` 负 margin 抵消新加的水平 padding，文字仍贴在原来的右边线，不会因为加 padding 看起来"内缩"破坏对齐
  - Edit 原本的 `hover:text-foreground/80`（文字变淡）被移除 —— 加了 bg 反馈之后再让文字变淡跟交互语义冲突（hover 该让按钮"更显眼"而不是"更模糊"）

  ## 测试清单
  - [ ] `/en/subscription` 进入 Billing 设置页，hover 三个按钮（Edit / View all invoices / Download），都呈现圆角灰色背景
  - [ ] 切到 dark mode（系统主题或测试切换），hover 背景颜色自动变成暗灰色，不出现纯白色或残留 light token
  - [ ] Edit / View all invoices 按钮文字位置在 hover 时没有位移（`-mr-2` 抵消生效）
  - [ ] Download 按钮多行排列时每行 hover 独立响应，不互相影响

  ## 关于 #1653
  本 PR 是 #1653 的内容 port 到最新 main 上的等价分支——原 #1653 的源分支基于 5 天前的 main（在 `#1713 Nest pnpm workspace under web/` 之前），路径是 `web/src/...`；新 main 的对应路径是
  `web/app/src/...`，cherry-pick 会全路径冲突。所以手工 port 了同一个 className 改动到新分支上。改动内容 **逐字符等价**于 #1653 的 commit `eb9c6acf`。原 #1653 可以关闭。
