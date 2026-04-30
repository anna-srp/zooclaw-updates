---
title: "支持导入外部 Agent 并安装到 ZooClaw"
type: "新功能上线"
priority: "高"
date: "2026-04-29"
status: "待审核"
channels: "站内弹窗, Use Case, Discord, changelog"
---

# 支持导入外部 Agent 并安装到 ZooClaw

## 核心宣传点

现在可以将外部自定义 Agent 导入并安装到 ZooClaw，灵活扩展你的 Agent 生态，不再局限于官方上架的 Agent。

## 原始内容

**Commit:** `e4addf6f` — 2026-04-29T10:16:38Z
**Repo:** ecap-workspace
**Author:** nolan-srp

**Commit Message:**
```
feat(openclaw): support imported agent installs (#1470)

## Summary
- add import agent support to OpenClaw install and uninstall request
handling
- persist imported agents as custom metadata and preserve their source
in backend responses
- extend web API helpers and unit tests for import async operations and
validation

## Context
- enables import-based agent installs to use raw remote archive URLs end
to end
```

**PR #1470:** feat(openclaw): support imported agent installs

**PR Body:**
## Summary
- add import agent support to OpenClaw install and uninstall request handling
- persist imported agents as custom metadata and preserve their source in backend responses
- extend web API helpers and unit tests for import async operations and validation

## Context
- enables import-based agent installs to use raw remote archive URLs end to end

