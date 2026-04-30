---
title: "修复：视频 URL 安全漏洞修复"
type: "Bug Fix"
priority: "中"
date: "2026-04-29"
status: "待审核"
channels: "Discord, changelog"
---

# 修复：视频 URL 安全漏洞修复

## 核心宣传点

修复了网页端视频组件中潜在的 URL 注入安全问题，提升平台整体安全性。

## 原始内容

**Commit:** `8ac54c60` — 2026-04-29T12:45:02Z
**Repo:** ecap-workspace
**Author:** Chris@ZooClaw

**Commit Message:**
```
fix(web): sanitize video URL in <video> attribute (#1328) (#1462)

## Summary

`lib/api/chat.ts` 的 `sendVideoGeneration` 之前把 `videoItem.url` 原样塞进
template literal 的 \`<video controls src=\"\${url}\">\`。如果 URL 出现
\`\"\`,attribute 边界被打破,后面的内容会被 HTML 解析成相邻属性(如 \`onload=\"alert(1)\"\`)——
而这串内容是会被存进 chat session 然后回放成 HTML 的。\`b64_json\` 分支由 data-URL 前缀和
base64 字符集约束,实际暴露面是 URL 分支。

抽 \`buildVideoResponseContentHtml(src)\`,改用
\`document.createElement('video')\` + \`outerHTML\` —— 让浏览器 HTML
serializer 按 WHATWG 规范处理 attribute escaping(\`&\` → \`&amp;\`, \`\"\` →
\`&quot;\`)。一个含 \`\"\` 的 URL 在序列化→重解析后会**圆环回到原值**,不会冒出新属性。

## Test

新建 \`tests/unit/lib/api/chat.unit.spec.ts\`,3 个用例:

- 安全 URL 输出 baseline 形式(controls + src + style)
- \`data:video/mp4;base64,...\` 原样保留
- **回归断言**(#1328):一组带 \`\"\` / \`&\` / \`<\` / 拼接 \`onerror=...\` 的
tricky URL,断言 \`getAttribute('src')\` 与原 URL 完全相等,且 attribute 名集合恒为
\`['controls', 'src', 'style']\`(无注入)

本地反向验证:把 helper 临时改回 template-literal 形式,回归用例报 \`expected
'https://x.com/a' to be 'https://x.com/a\"b.mp4'\` —— 测试确实拦得住
regression。

## Closes

Closes #1328

## Test plan

- [x] \`pnpm test:unit tests/unit/lib/api/chat.unit.spec.ts\` (3/3)
- [x] \`pnpm test:unit tests/unit/hooks/useLiteLLMApi.unit.spec.ts\` (现有
caller 不受影响)
- [x] \`npx tsc --noEmit\` clean
- [x] \`npx eslint\` / \`npx prettier --check\` clean
- [ ] CI: code-quality / lint-and-test
```

**PR #1328:** 
