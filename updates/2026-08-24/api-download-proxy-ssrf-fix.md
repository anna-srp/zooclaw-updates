---
title: "安全修复：下载代理堵住可绕过域名白名单的 SSRF 风险"
type: "Bug Fix"
priority: "中"
date: "2026-08-24"
status: "待审核"
channels: ""
---

# 安全修复：下载代理堵住可绕过域名白名单的 SSRF 风险

## 核心宣传点

文件下载代理原本只在第一跳校验域名白名单，之后会自动跟随跳转；由于白名单里包含 CloudFront、Shopify 这类任何人都能托管内容的域，攻击者可以在自己的空间上返回一个跳转、把请求引向内网地址，从而绕过白名单。现在每一次跳转都会重新做白名单校验，跳到不允许的地址直接返回 403 且不会真的发出请求，跳转次数也限制在 5 跳以内。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `46e6a071637b8a06031350e2c08226ee3c28beee`
- PR: #3495
- 作者: Chris@ZooClaw
- 日期: 2026-08-24T10:50:19Z

### Commit Message

```
fix(security): validate redirect hops in /api/download proxy (CodeQL #617) (#3495)

## 问题

CodeQL alert #617（`js/request-forgery`，critical）：`/api/download` 代理虽然有
hostname 白名单，但 `fetch(url)` 默认自动跟随重定向。白名单里包含
`cloudfront.net`、`myshopify.com` 这类任何人都可托管内容的域——攻击者在自己的 CloudFront
发行版上返回 302 指向内网地址（如云 metadata endpoint），即可绕过白名单发起 SSRF。

## 修复

- `fetch` 改为 `redirect: 'manual'`，手动跟随重定向，每一跳的 `Location`（含相对路径解析）都重新过
`isAllowedUrl` 白名单校验。
- 命中不允许的重定向目标返回 403（不发起该请求）。
- 重定向上限 5 跳，超出返回 500。

## 测试

- 新增 4 个单测：允许域间重定向正常流式返回、重定向到内网地址被 403 拦截且不发请求、相对 Location
正确解析、重定向循环在上限处终止。
- `bash scripts/verify-web.sh` 全绿（tsc / vitest 9041 passed / eslint）。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01NWHV9vozVf6qN6zB5cUUdv

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## 问题

CodeQL alert #617（`js/request-forgery`，critical）：`/api/download` 代理虽然有 hostname 白名单，但 `fetch(url)` 默认自动跟随重定向。白名单里包含 `cloudfront.net`、`myshopify.com` 这类任何人都可托管内容的域——攻击者在自己的 CloudFront 发行版上返回 302 指向内网地址（如云 metadata endpoint），即可绕过白名单发起 SSRF。

## 修复

- `fetch` 改为 `redirect: 'manual'`，手动跟随重定向，每一跳的 `Location`（含相对路径解析）都重新过 `isAllowedUrl` 白名单校验。
- 命中不允许的重定向目标返回 403（不发起该请求）。
- 重定向上限 5 跳，超出返回 500。

## 测试

- 新增 4 个单测：允许域间重定向正常流式返回、重定向到内网地址被 403 拦截且不发请求、相对 Location 正确解析、重定向循环在上限处终止。
- `bash scripts/verify-web.sh` 全绿（tsc / vitest 9041 passed / eslint）。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01NWHV9vozVf6qN6zB5cUUdv

