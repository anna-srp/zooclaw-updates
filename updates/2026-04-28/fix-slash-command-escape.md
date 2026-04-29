---
title: "修复：聊天框输入 /xxx 不再被误识别为系统命令"
type: "Bug Fix"
priority: "中"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# 修复：聊天框输入 /xxx 不再被误识别为系统命令

## 核心宣传点

修复了用户在聊天框输入以 / 开头的普通文本（如 /foo）被误解析为命令的问题，输入体验更准确。

## 原始内容

**Commit**: `cf64ac7e70a5a909525ab933e77c45abb6e418c4`
**仓库**: ecap-workspace
**作者**: nolan-srp
**时间**: 2026-04-28T09:32:26Z

### 完整 Commit Message

```
fix(web): escape non-whitelisted chat slash commands (#1440)

## Summary
- escape slash-prefixed chat input by default so plain messages like
`/foo` are sent literally instead of being interpreted as chat commands
- preserve the existing behavior for the supported slash commands
`/new`, `/stop`, and `/reset`
- apply the same normalization when composing a quoted reply
- add focused unit coverage for escaped slash input, whitelisted
commands, whitespace trimming, and quoted replies
```

### PR #1440 完整描述

## Summary
- escape slash-prefixed chat input by default so plain messages like `/foo` are sent literally instead of being interpreted as chat commands
- preserve the existing behavior for the supported slash commands `/new`, `/stop`, and `/reset`
- apply the same normalization when composing a quoted reply
- add focused unit coverage for escaped slash input, whitelisted commands, whitespace trimming, and quoted replies
