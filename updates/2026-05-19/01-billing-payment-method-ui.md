---
title: "支付方式选择弹窗界面全面升级"
type: "产品基础功能更新"
priority: "中"
date: "2026-05-19"
status: "待审核"
channels: ""
---
# 支付方式选择弹窗界面全面升级

## 核心宣传点
支付时选择付款方式的弹窗更美观了——信用卡和支付宝图标更清晰，布局更规范，操作更直观。

## 原始内容
```
commit: a384add8ad230d714f2d17e424ebaacf7137be7b
repo: SerendipityOneInc/ecap-workspace
author: lynn Zhuang
date: 2026-05-19T12:18:57Z

feat(billing): Select Payment Method 弹窗UI优化 (#1735)

## 概要
- 按 Figma 节点 `2718:1057` 重做 Select Payment Method 弹窗：22px 加粗标题、右上角 X
关闭按钮、两个选项卡片（左对齐
radio + label + 真实品牌 logo 横排）、底部居中显示禁用提示。替换原本的 emoji 图标 + 底部 Cancel
按钮布局。
- 在 `web/app/public/billing/` 新增两个品牌资源：`card-brands.png`（Visa /
MasterCard / Amex / Discover 合并图）和
`alipay-logo.svg`（修掉了 Figma 导出时塞入的 `preserveAspectRatio="none"`，原本会导致
SVG
  拉伸填满父容器、长宽比失真）。
- `PaymentMethodModal` 的 props 接口和行为合约**完全不变**：已有的 5 个 unit test
无需任何修改直接通过（测试的是
  `onSelect / onClose / disabled / isOpen` 行为合约，不锁定 DOM 结构）。

  ## 测试清单
  - [ ] 打开 `/en/subscription`，点任意非当前 plan 的 Upgrade —— 新弹窗按重做后的布局渲染。
- [ ] Stripe 流程：点 Card 卡片 → 出现 spinner + "Opening..."，下方显示
secure-checkout 提示。
- [ ] Antom 流程：点 Alipay 卡片 → 出现 spinner + "Redirecting..."，下方显示 Alipay
跳转提示。
- [ ] 已订阅 Stripe 的活跃用户：Alipay 卡片显示禁用态 + 下方居中显示 "Cancel your current
subscription first to
  switch payment method."
  - [ ] 已订阅 Antom 的活跃用户：Card 卡片显示同样的禁用态。
  - [ ] 关闭路径：右上角 X、背景点击、Esc 都能正常关闭；`processingChannel`
  非空时这三种关闭方式都被禁用（防止支付跳转中被中断）。

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

--- PR #1735 Body ---
## 概要
  - 按 Figma 节点 `2718:1057` 重做 Select Payment Method 弹窗：22px 加粗标题、右上角 X 关闭按钮、两个选项卡片（左对齐
  radio + label + 真实品牌 logo 横排）、底部居中显示禁用提示。替换原本的 emoji 图标 + 底部 Cancel 按钮布局。
  - 在 `web/app/public/billing/` 新增两个品牌资源：`card-brands.png`（Visa / MasterCard / Amex / Discover 合并图）和
  `alipay-logo.svg`（修掉了 Figma 导出时塞入的 `preserveAspectRatio="none"`，原本会导致 SVG
  拉伸填满父容器、长宽比失真）。
  - `PaymentMethodModal` 的 props 接口和行为合约**完全不变**：已有的 5 个 unit test 无需任何修改直接通过（测试的是
  `onSelect / onClose / disabled / isOpen` 行为合约，不锁定 DOM 结构）。

  ## 测试清单
  - [ ] 打开 `/en/subscription`，点任意非当前 plan 的 Upgrade —— 新弹窗按重做后的布局渲染。
  - [ ] Stripe 流程：点 Card 卡片 → 出现 spinner + "Opening..."，下方显示 secure-checkout 提示。
  - [ ] Antom 流程：点 Alipay 卡片 → 出现 spinner + "Redirecting..."，下方显示 Alipay 跳转提示。
  - [ ] 已订阅 Stripe 的活跃用户：Alipay 卡片显示禁用态 + 下方居中显示 "Cancel your current subscription first to
  switch payment method."
  - [ ] 已订阅 Antom 的活跃用户：Card 卡片显示同样的禁用态。
  - [ ] 关闭路径：右上角 X、背景点击、Esc 都能正常关闭；`processingChannel`
  非空时这三种关闭方式都被禁用（防止支付跳转中被中断）。
```
