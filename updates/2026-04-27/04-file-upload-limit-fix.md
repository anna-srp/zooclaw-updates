---
title: "文件上传数量限制修复（上传中拖入绕限漏洞）"
type: "Bug Fix"
priority: "中"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# 文件上传数量限制修复（上传中拖入绕限漏洞）

## 核心宣传点
修复了上传文件时，趁上传进行中拖入更多文件可以突破 10 个文件上限的 Bug，文件数量限制现在会被正确执行。

## 原始内容
**Commit**: fix(web): enforce file upload limit during in-progress uploads (#1385)  
**PR Body**:  
修复上传进行中拖入更多文件可绕过10文件限制的竞态条件。根因：count检查读取的是异步React state，尚未更新（第一批上传触发的state更新还在队列中）。新增同步ref计数器（pendingFileCountRef）+ R2 placeholder计数来关闭这个竞态窗口。  
测试场景：上传8文件→进行中拖入5个→应提示并只允许2个；上传10文件→完成后拖入1个→应阻止。
