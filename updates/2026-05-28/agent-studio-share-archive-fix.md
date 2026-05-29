---
title: "修复 Agent Studio 分享包无法正常生成可安装链接的问题"
type: "Bug Fix"
priority: "中"
date: "2026-05-28"
status: "待审核"
channels: ""
---

# 修复 Agent Studio 分享包无法正常生成可安装链接的问题

## 核心宣传点

通过 Agent Studio 分享 Agent 时，生成的链接现在可以被正确安装使用，解决了之前分享链接失效的问题。

## 原始内容

fix(agent-studio): stage tmp share archives in public artifacts (#151)
fix(agent-studio): generate installable artifact share urls (#149)

PR #151: Detect Agent Studio source packs under workspace tmp directories and stage shared archives in the parent workspace public artifacts/shares directory. Build share URLs from the public workspace root while keeping delivery state on the source pack.

PR #149: Use zooclaw-artifact-url when staging Agent Studio shares so generated URLs include bot and agent path segments. Add runtime URL projection for check-only previews via PUBLIC_URL_PREFIX and BOT_ID. Keep local fallback behavior for non-runtime development.
