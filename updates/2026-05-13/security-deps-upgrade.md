---
title: "安全漏洞修复：清零 31 条 Dependabot + 3 条 CodeQL 告警"
type: "Bug Fix"
priority: "中"
date: "2026-05-13"
status: "待审核"
channels: "Discord + changelog"
---

# 安全漏洞修复：清零 31 条 Dependabot + 3 条 CodeQL 告警

## 核心宣传点

ZooClaw 平台完成了一轮重要的安全加固，修复了包含 Next.js 中间件绕过、SSRF、DoS、XSS 在内的多个已知安全漏洞，让你的使用更加安全。

## 原始内容

**来源**: ecap-workspace PR #1607 | SHA: f72f8834

**Commit Message**:
```
fix: 清 31 条 Dependabot + 3 条 CodeQL 安全告警(收编 #1576) (#1607)

合并 dependabot PR #1576 的 8 个 minor/patch bump，叠加 GitHub Security 上 31 条
open Dependabot alerts + 3 条 CodeQL alerts 的全量修复。

主要升级：
- next: ^15.5.15 → ^15.5.18
  security: middleware bypass / SSRF / DoS / XSS (13 alerts)
- mermaid: ^11.14.0 → ^11.15.0 (security: 4 alerts)
- wrangler: ^4.85.0 → ^4.86.0
- @opennextjs/cloudflare: ^1.19.4 → ^1.19.5
- dompurify: ^3.4.1 → ^3.4.2
- marked: ^18.0.0 → ^18.0.3
```

**PR #1607 Description**:
```
合并 dependabot PR #1576 的 8 个 minor/patch bump，叠加 GitHub Security 上 31 条
open Dependabot alerts + 3 条 CodeQL alerts 的全量修复。Supersedes #1576。

PR #1576 处于 CONFLICTING 状态：Dependabot 把 @opennextjs/cloudflare 从 1.19.4 bump 到
1.19.5，但没同步 bump wrangler。本 PR 把 wrangler 一起带到 ^4.86.0 解开冲突，顺便把整批
31 条 Dependabot 安全告警与 3 条 CodeQL 告警一并清零。

直接依赖升级：
- next: ^15.5.15 → ^15.5.18 (security: middleware bypass / SSRF / DoS / XSS, 13 alerts)
- mermaid: ^11.14.0 → ^11.15.0 (security: 4 alerts)
- eslint-config-next: ^15.5.15 → ^15.5.18
- wrangler: ^4.85.0 → ^4.86.0
- @opennextjs/cloudflare: ^1.19.4 → ^1.19.5
- dompurify: ^3.4.1 → ^3.4.2
- marked: ^18.0.0 → ^18.0.3
```
