---
title: "OpenClaw 支持从外部导入安装 Agent"
type: "产品基础功能更新"
priority: "中"
date: "2026-04-30"
status: "待审核"
channels: ""
---
# OpenClaw 支持从外部导入安装 Agent

## 核心宣传点
现在可以通过外部链接直接安装 Agent，不限于官方目录，扩大了 Agent 生态的可能性。

## 原始内容
**Commit**: feat(openclaw): support imported agent installs (#1470)
**Author**: （merge commit）
**Date**: 2026-04-29

```
feat(openclaw): support imported agent installs (#1470)

## Summary
- add import agent support to OpenClaw install and uninstall request handling
- persist imported agents as custom metadata and preserve their source
  in backend responses
- extend web API helpers and unit tests for import async operations and validation
```

**PR #1470 Body**:
## Summary
- add import agent support to OpenClaw install and uninstall request handling
- persist imported agents as custom metadata and preserve their source in backend responses
- extend web API helpers and unit tests for import async operations and validation

## Context
- enables import-based agent installs to use raw remote archive URLs end to end
