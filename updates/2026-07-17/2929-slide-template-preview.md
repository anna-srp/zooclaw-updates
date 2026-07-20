---
title: 修复落地页所选幻灯片模板预览
type: Bug Fix
priority: B
date: 2026-07-17
status: 已合并待发版
pr: 2929
author: shana-maker
url: https://github.com/SerendipityOneInc/ecap-workspace/pull/2929
---

## 更新内容

优化落地页对话输入框中「所选幻灯片模板」的展示：

- 将原来的纯文字描述替换为带边框的缩略图预览
- 新增显式的「移除」按钮，访客可清除已选模板并重新选择
- `Add & Use` 改为幂等操作，重复点击仍保持模板选中状态

## 用户价值

访客在落地页选择幻灯片模板后能直观看到模板预览，并可随时更换，交互更清晰。
