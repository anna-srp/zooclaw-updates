---
title: "修复表格内图片无法点击放大预览"
type: "Bug Fix"
priority: "中"
date: "2026-05-07"
status: "待审核"
channels: ""
---
# 修复表格内图片无法点击放大预览

## 核心宣传点
AI 回复的表格里包含图片时，现在可以正常点击放大预览，与普通消息中的图片体验一致。

## 原始内容

### Commit Message
```
fix(web): enable image preview for images inside tables (#1501)
```

### PR Description
## Summary
- LLM 返回的 HTML 表格中的 `<img>` 标签（非 markdown 语法渲染）之前点击无法放大预览，因为 click handler 仅识别 `markdown-image` class
- 扩展 click handler fallback：`.prose` 内任意 `<img>` 点击均可触发预览，优先用 `data-image-url`，fallback 到 `src`
- Gallery 选择器同步扩展，表格内图片也参与多图导航
- 表格内图片 CSS：`height: auto; max-height: 200px; cursor: pointer`（300px 对表格太高）

## Test plan
- [x] 新增单元测试：markdown 图片在 markdown 表格中可点击预览
- [x] 新增单元测试：raw HTML `<img>` 在表格中可点击预览
- [x] 原有 32 个测试全部通过
