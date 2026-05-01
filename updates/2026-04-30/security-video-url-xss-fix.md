---
title: "安全修复：视频链接注入漏洞修复"
type: "Bug Fix"
priority: "高"
date: "2026-04-30"
status: "待审核"
channels: ""
---
# 安全修复：视频链接注入漏洞修复

## 核心宣传点
修复了一个潜在的安全漏洞：在聊天中发送视频时，恶意构造的 URL 可能被当作代码执行，现已修复。

## 原始内容
**Commit**: fix(web): sanitize video URL in <video> attribute (#1328) (#1462)
**Author**: （merge commit）
**Date**: 2026-04-29

```
fix(web): sanitize video URL in <video> attribute (#1328) (#1462)

lib/api/chat.ts 的 sendVideoGeneration 之前把 videoItem.url 原样塞进
template literal 的 <video controls src="${url}">。如果 URL 出现 "，
attribute 边界被打破，后面的内容会被 HTML 解析成相邻属性（如 onload="alert(1)"）
—— 而这串内容是会被存进 chat session 然后回放成 HTML 的。

抽 buildVideoResponseContentHtml(src)，改用 document.createElement('video') +
outerHTML —— 让浏览器 HTML serializer 按 WHATWG 规范处理 attribute escaping。
```

**PR #1462 Body**:
Security fix: sanitize video URL to prevent XSS via malformed URLs with quote characters. Uses DOM API for proper attribute escaping instead of template literals. Includes regression test cases covering quote injection, ampersand, angle brackets, and onerror chaining patterns.
