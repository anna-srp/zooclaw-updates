---
title: "开发者平台 API Key 创建与保存弹窗优化：显示所属 Project、名称计数与一次性密钥复制"
type: "体验优化"
priority: "中"
date: "2026-10-01"
status: "待审核"
channels: "Discord+changelog"
---

# 开发者平台 API Key 创建与保存弹窗优化：显示所属 Project、名称计数与一次性密钥复制

## 核心宣传点

API Key 创建弹窗做了一轮优化：移掉了 Cancel，改为展示所属 Project、名称提示和长度计数，创建失败的错误提示直接显示在输入框旁边。密钥保存弹窗按参考图重做，明确强调密钥只会展示一次，提供带图标的 Copy key / Copied 按钮和 Done 按钮，关闭后会把页面里的密钥清掉。另外把 API Key 列表的分页大小调到 50，避免只有两条记录也冒出 Load more keys，导航品牌文字也统一成 ZooWork。

## 分级

- 内部：P2
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary / 变更概述

- 优化 API key 创建弹窗：移除 Cancel，展示所属 Project、名称提示与长度计数，并在输入旁显示创建错误。
- 按参考图调整密钥保存弹窗：强调密钥只展示一次，提供带图标的 Copy key / Copied 按钮和 Done 按钮；关闭后清除页面中的密钥。
- 将预览 API key 列表的分页大小调整为 50，避免仅有两条记录就出现 Load more keys；将导航品牌文字改为 ZooWork Platform。

- Refine the API key creation dialog with project context, name guidance, inline errors, and no Cancel button.
- Align the one-time secret dialog with the reference, including Copy key / Copied and Done actions.
- Match preview key pagination to the 50-item API default and rename the navigation brand to ZooWork Platform.

## Test plan / 验证

- [x] `pnpm lint` (web/platform)
- [x] `pnpm typecheck` (web/platform)
- [x] `pnpm test -- src/app/router.test.tsx src/preview/api-middleware.test.ts` (154 tests passed)
- [x] Local preview checked at `/__preview/settings/api-keys`

Expiry display is deferred because the current API does not expose an expiry value. / 当前 API 尚无过期时间字段，暂不显示。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `d805fb0ef6b21b76122ec8a2a6c5c64f377236e3`
- PR: #3993
- 作者：david-srp
- 日期：2026-10-01T18:34:45Z

### Commit Message

```
feat(platform): 优化 API key 创建 UI / Improve API key creation UI (#3993)

## Summary / 变更概述

- 优化 API key 创建弹窗：移除 Cancel，展示所属 Project、名称提示与长度计数，并在输入旁显示创建错误。
- 按参考图调整密钥保存弹窗：强调密钥只展示一次，提供带图标的 Copy key / Copied 按钮和 Done
按钮；关闭后清除页面中的密钥。
- 将预览 API key 列表的分页大小调整为 50，避免仅有两条记录就出现 Load more keys；将导航品牌文字改为 ZooWork
Platform。

- Refine the API key creation dialog with project context, name
guidance, inline errors, and no Cancel button.
- Align the one-time secret dialog with the reference, including Copy
key / Copied and Done actions.
- Match preview key pagination to the 50-item API default and rename the
navigation brand to ZooWork Platform.

## Test plan / 验证

- [x] `pnpm lint` (web/platform)
- [x] `pnpm typecheck` (web/platform)
- [x] `pnpm test -- src/app/router.test.tsx
src/preview/api-middleware.test.ts` (154 tests passed)
- [x] Local preview checked at `/__preview/settings/api-keys`

Expiry display is deferred because the current API does not expose an
expiry value. / 当前 API 尚无过期时间字段，暂不显示。
```

来源：SerendipityOneInc/ecap-workspace @ d805fb0e，PR #3993，作者 david-srp。
