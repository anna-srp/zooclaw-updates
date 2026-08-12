---
title: "自定义专家详情页可一键复制 Agent ID"
type: "体验优化"
priority: "中"
date: "2026-08-11"
status: "待审核"
channels: ""
---

## 核心宣传点

My Custom Specialists 的详情弹窗现在会显示已安装 Agent 的后端 Agent ID，并支持一键复制——在 Agent Builder 里写引用或提工单时直接拿来用。

## 原始内容

### commit message

```
feat(publish): show installed agent id in the detail modal (#3328)

## Linear

无（用户直接提出的 UI 需求）。

## Summary

My Custom Specialists 的详情弹窗此前只展示 pack 身份，没有已安装 agent 的后端
`agent_id`——而用户在 Agent Builder 里写 ref、提工单时需要的正是这个值。

- `PublishAgentCardItem` 新增 `agentId`，由 `card-model.ts` 从已安装 agent
带出（org-pack 行取 `installedAgent?.id`，db-only 行取
`agent.id`）。这个字段**不能**用已有的 `id` 代替：org-pack 行的 `id` 是 `display_id ||
pack_id`，只有 db-only 行两者才恰好相同，类型上加了 JSDoc 说明。
- 弹窗在 Description 与 Archive File 之间渲染 **Agent ID**（mono 字体）+
一个复制按钮。未安装的记录没有该字段，整行不渲染。
- 复制走仓库已有的 `copyToClipboard`（`@zooclaw/chat-ui`，失败会经 logger 上报），而不是再手搓一遍
`navigator.clipboard.writeText` + `try/catch`。
- 「已复制」的闪烁状态属于纯展示态，按 `web/app/AGENTS.md` 的 MVVM 约定留在 view 层；定时器由 effect
持有，弹窗在闪烁期间被关掉会自动取消，不会向已卸载组件 setState。
- 新增 `common.copied`（`common.copy` 已存在）与页面级的
`zooSquare.publish.detail.agentId`，en/zh 双语。

### 已知的相关问题（本 PR 未处理）

- `src/components/settings/GeneralTab.tsx` 的 `CopyButton` 与本 PR
的复制按钮是近乎逐字的重复（同 2000ms、同图标尺寸、同配色），全仓类似形态共 8 处。提取共享组件需要一并迁移
GeneralTab，超出本 PR 范围，建议单独开一个 PR 做。
- 安装确认弹窗的文案是裸 key（`zooSquare.publish.installConfirmTitle` /
`installConfirmDesc`），en/zh 都缺翻译。与本 PR 无关的既有问题。

## Test plan

- [x] `bash scripts/verify-web.sh
'src/app/[locale]/(app)/agents-manager/publish' src/locales
tests/unit/app` — guards + tsc + vitest + eslint 全绿
- [x] `bash scripts/verify-changed.sh` — 变更面 gate 全绿
- [x] 新增 2
个单测（`tests/unit/app/agents-manager-publish.unit.spec.tsx`）：已安装时弹窗展示
`agent_id`（断言的是 agent 身份而非 pack 身份）；未安装时该行不渲染
- [ ] **未做**：登录态下的真机 UI 验证。本地 `pnpm dev:staging` 已跑通、路由
200、编译无新增报错，但该弹窗需要真实 staging 账号登录后才能看到，需人工点一次确认复制手感

> 备注：本地 staging dev server 日志里的 `Failed to generate static paths for
/[locale]/agents-manager: SyntaxError: Unexpected end of JSON input`
在本改动之前就存在（stash 后跑基线复现），与本 PR 无关。

Co-authored-by: wangfulong <wfllike@gmail.com>
```

### PR body

## Linear

无（用户直接提出的 UI 需求）。

## Summary

My Custom Specialists 的详情弹窗此前只展示 pack 身份，没有已安装 agent 的后端 `agent_id`——而用户在 Agent Builder 里写 ref、提工单时需要的正是这个值。

- `PublishAgentCardItem` 新增 `agentId`，由 `card-model.ts` 从已安装 agent 带出（org-pack 行取 `installedAgent?.id`，db-only 行取 `agent.id`）。这个字段**不能**用已有的 `id` 代替：org-pack 行的 `id` 是 `display_id || pack_id`，只有 db-only 行两者才恰好相同，类型上加了 JSDoc 说明。
- 弹窗在 Description 与 Archive File 之间渲染 **Agent ID**（mono 字体）+ 一个复制按钮。未安装的记录没有该字段，整行不渲染。
- 复制走仓库已有的 `copyToClipboard`（`@zooclaw/chat-ui`，失败会经 logger 上报），而不是再手搓一遍 `navigator.clipboard.writeText` + `try/catch`。
- 「已复制」的闪烁状态属于纯展示态，按 `web/app/AGENTS.md` 的 MVVM 约定留在 view 层；定时器由 effect 持有，弹窗在闪烁期间被关掉会自动取消，不会向已卸载组件 setState。
- 新增 `common.copied`（`common.copy` 已存在）与页面级的 `zooSquare.publish.detail.agentId`，en/zh 双语。

### 已知的相关问题（本 PR 未处理）

- `src/components/settings/GeneralTab.tsx` 的 `CopyButton` 与本 PR 的复制按钮是近乎逐字的重复（同 2000ms、同图标尺寸、同配色），全仓类似形态共 8 处。提取共享组件需要一并迁移 GeneralTab，超出本 PR 范围，建议单独开一个 PR 做。
- 安装确认弹窗的文案是裸 key（`zooSquare.publish.installConfirmTitle` / `installConfirmDesc`），en/zh 都缺翻译。与本 PR 无关的既有问题。

## Test plan

- [x] `bash scripts/verify-web.sh 'src/app/[locale]/(app)/agents-manager/publish' src/locales tests/unit/app` — guards + tsc + vitest + eslint 全绿
- [x] `bash scripts/verify-changed.sh` — 变更面 gate 全绿
- [x] 新增 2 个单测（`tests/unit/app/agents-manager-publish.unit.spec.tsx`）：已安装时弹窗展示 `agent_id`（断言的是 agent 身份而非 pack 身份）；未安装时该行不渲染
- [ ] **未做**：登录态下的真机 UI 验证。本地 `pnpm dev:staging` 已跑通、路由 200、编译无新增报错，但该弹窗需要真实 staging 账号登录后才能看到，需人工点一次确认复制手感

> 备注：本地 staging dev server 日志里的 `Failed to generate static paths for /[locale]/agents-manager: SyntaxError: Unexpected end of JSON input` 在本改动之前就存在（stash 后跑基线复现），与本 PR 无关。


