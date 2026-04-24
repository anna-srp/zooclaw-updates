---
title: "修复：反馈提交失败时不再清空已输入的内容"
type: "Bug Fix"
priority: "低"
date: "2026-04-24"
status: "待审核"
channels: "Discord+changelog"
---
# 修复：反馈提交失败时不再清空已输入的内容

## 核心宣传点
反馈对话框提交失败后，你输入的内容不会消失了——可以直接重试，不用重新填写。

## 原始内容

fix(web): preserve textarea input on FeedbackDialog submit failure (#1268)

Preserve user input if feedback submission fails.
