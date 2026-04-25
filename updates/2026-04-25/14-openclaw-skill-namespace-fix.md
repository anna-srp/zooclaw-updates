---
title: "OpenClaw 修复：正确识别命名空间 Skill 工作区"
type: "Bug Fix"
priority: "中"
date: "2026-04-25"
status: "待审核"
channels: "Discord + changelog"
---

# OpenClaw 修复：正确识别命名空间 Skill 工作区

## 核心宣传点

修复了 OpenClaw 在加载带命名空间的 Skill 时工作区路径解析错误的问题，Skill 现在能正确加载。

## 原始内容

Commit: 0c726998918b8124979e2fffd45776d6a82f6759

Message:
fix(openclaw): accept namespaced skill workspaces in agent archives (#1298)

## Summary
- accept when detecting archive-backed agent workspaces during OpenClaw
installs
- keep archive workspace detection working for legacy and markdown-based
layouts
- add focused backend unit coverage for the namespaced workspace
detection paths

## Behavior
- custom agent archives that package skills under no longer fail install
with solely because they omit legacy or top-level markdown files
- existing archive layouts that rely on or markdown files continue to
resolve as before

PR Description:
## Summary
- accept  when detecting archive-backed agent workspaces during OpenClaw installs
- keep archive workspace detection working for legacy  and markdown-based layouts
- add focused backend unit coverage for the namespaced workspace detection paths

## Behavior
- custom agent archives that package skills under  no longer fail install with  solely because they omit legacy  or top-level markdown files
- existing archive layouts that rely on  or markdown files continue to resolve as before
