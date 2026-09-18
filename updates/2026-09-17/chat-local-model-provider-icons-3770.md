---
title: "fix(chat): render model provider icons locally (#3770)"
type: "Bug 修复"
priority: "低"
date: "2026-09-17"
status: "待审核"
channels: ""
---

# fix(chat): render model provider icons locally (#3770)

## 核心宣传点

聊天里的模型厂商图标改为本地内置 SVG，不再依赖后端或 CDN 图片，加载更快也不会出现空白方块。

## PR 说明

## Summary

- render model provider logos as local React SVG components instead of backend/CDN image URLs
- map the staging catalog metadata to Claude, DeepSeek, Doubao/Seed, Gemini, GLM, Grok, Kimi, OpenAI, Qwen, and ZooWork icons
- use a fixed CPU icon for unknown/private providers
- cover staging catalog labels and known/unknown rendering behavior with unit tests

## Verification

- `pnpm --filter @zooclaw/chat-ui test`
- `pnpm --filter @zooclaw/chat-ui tsc`
- `pnpm --filter @zooclaw/chat-ui lint`
- targeted `web/app` Vitest suite: 71 tests passed
- `bash scripts/verify-web.sh <changed app paths>`
- `bash scripts/verify-changed.sh`

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `82b8f6355fab065be659c5c9203d5d97d9fefa91`
- PR: #3770
- 作者：finn-srp
- 日期：2026-09-17T07:11:53Z

### Commit Message

```
fix(chat): render model provider icons locally (#3770)

## Summary

- render model provider logos as local React SVG components instead of
backend/CDN image URLs
- map the staging catalog metadata to Claude, DeepSeek, Doubao/Seed,
Gemini, GLM, Grok, Kimi, OpenAI, Qwen, and ZooWork icons
- use a fixed CPU icon for unknown/private providers
- cover staging catalog labels and known/unknown rendering behavior with
unit tests

## Verification

- `pnpm --filter @zooclaw/chat-ui test`
- `pnpm --filter @zooclaw/chat-ui tsc`
- `pnpm --filter @zooclaw/chat-ui lint`
- targeted `web/app` Vitest suite: 71 tests passed
- `bash scripts/verify-web.sh <changed app paths>`
- `bash scripts/verify-changed.sh`
```
