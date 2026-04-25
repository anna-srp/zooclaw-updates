---
title: "Artifact 预览修复与 React 生命周期优化"
type: "Bug Fix"
priority: "中"
date: "2026-04-25"
status: "待审核"
channels: "Discord + changelog"
---

# Artifact 预览修复与 React 生命周期优化

## 核心宣传点

修复了 Artifact 预览界面多处显示问题，同时清理 React 组件生命周期，提升稳定性。

## 原始内容

Commit: 931eaf0cb2ba75b22eb8b47c715e1ff96d771595

Message:
fix(web): artifacts preview fixes + React lifecycle cleanup (#1292)

Artifact preview:
- FileAvailabilityGate: use HEAD with redirect:'manual' to avoid hitting
S3 presigned URLs (method mismatch → 403); only retry on 404
- Remove _t cache-buster from renderUrl — breaks presigned S3 signatures
when carried through 307 redirects; key-based remount handles reload
- Add aspect-ratio viewport control (16:9, 4:3, 9:16, 1:1) for visual
file types (html, pdf, svg, pptx, mermaid)
- Sidebar max width: 2/3 viewport; chat area min-width: 320px
- Workspace files: module-level cache (30s TTL) so panel reopen doesn't
refetch

Session lifecycle:
- useArtifactsSidebar: add sessionKey param, reset state on session
change; split auto-open / URL-sync into separate effects
- Fix onSubagentClose missing from effect deps

React lifecycle cleanup:
- GenClawClient: add cancellation to getClawSettings + getSubagentTasks
fetches; add uid to channel sessions effect deps
- useSubagentSessions: derive hasTerminalVisible boolean so dismiss
interval isn't torn down on every poll

Misc:
- .gitignore: .venv/ → .venv (match symlinks)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

PR Description:
Artifact preview:
- FileAvailabilityGate: use HEAD with redirect:'manual' to avoid hitting S3 presigned URLs (method mismatch → 403); only retry on 404
- Remove _t cache-buster from renderUrl — breaks presigned S3 signatures when carried through 307 redirects; key-based remount handles reload
- Add aspect-ratio viewport control (16:9, 4:3, 9:16, 1:1) for visual file types (html, pdf, svg, pptx, mermaid)
- Sidebar max width: 2/3 viewport; chat area min-width: 320px
- Workspace files: module-level cache (30s TTL) so panel reopen doesn't refetch

Session lifecycle:
- useArtifactsSidebar: add sessionKey param, reset state on session change; split auto-open / URL-sync into separate effects
- Fix onSubagentClose missing from effect deps

React lifecycle cleanup:
- GenClawClient: add cancellation to getClawSettings + getSubagentTasks fetches; add uid to channel sessions effect deps
- useSubagentSessions: derive hasTerminalVisible boolean so dismiss interval isn't torn down on every poll

Misc:
- .gitignore: .venv/ → .venv (match symlinks)
