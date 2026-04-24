---
title: "安全加固：修复多项 Dependabot 漏洞 + 日志脱敏"
type: "Bug Fix"
priority: "高"
date: "2026-04-24"
status: "待审核"
channels: "Discord+changelog"
---
# 安全加固：修复多项 Dependabot 漏洞 + 日志脱敏

## 核心宣传点
本次完成一批安全修复：升级存在漏洞的依赖包（包括 Electron、Next.js、uuid、lodash 等），并从日志中移除敏感信息，降低安全风险。

## 原始内容

fix(security): close 4 remaining Dependabot alerts — uuid / fast-xml-parser / lodash / dompurify (#1235)

fix(security): scrub uid in mattermost provisioning logs — 4 CodeQL alerts (#1241)

fix(security): scrub bot_id in openclaw-family logs — clears 7 CodeQL alerts (#1242)

fix(security): bump electron 35 → 39 in desktop (#1248)

fix(security): pnpm.overrides for 10 transitive vuln packages (#1247)

fix(security): bump next to ^15.5.15 (#1239)
