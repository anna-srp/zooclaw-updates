---
title: "开发者平台各类 ID 加上一键复制按钮"
type: "体验优化"
priority: "中"
date: "2026-10-22"
status: "待审核"
channels: ""
---

# 开发者平台各类 ID 加上一键复制按钮

## 核心宣传点

此前平台上的组织 ID 很难手动选中复制（来自一线支持同学反馈）。本次新增共享的复制按钮组件，并给组织 ID、项目 ID（列表与详情）、Webhook 端点地址与端点 ID、投递 ID / 事件 ID、测试回执 ID、用量页的会话 ID 都加上了复制按钮，账户页原有的复制按钮也统一换成同一组件。项目和用量表格中每行按钮的可访问名称会带上所属行的标识，避免多个同名按钮混淆；投递详情是弹窗，复制结果会在弹窗内单独播报，弹窗打开时焦点也改为落在弹窗本身，不再误触到第一个复制按钮并弹出提示。

## 分级

- 内部：P2
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## 备注

未处理：投递历史列表中的事件 ID 位于可点击按钮内无法嵌套按钮，只能在详情弹窗复制；API key 列表只显示前缀，不提供复制。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `514d8ecbbe8d9f4270cdfd2526291ea262213114`
- PR: #4115
- 作者：finn-srp
- 日期：2026-10-22T08:43:54Z

### Commit Message

```
feat(platform): 给显示 ID 的地方加复制按钮 (#4115)

## Linear


## Summary
- Platform 上的 Organization ID 不好选中复制（群里 FDE 反馈）。新增共享的 `CopyButton` 和
`CopyableValue`（`web/platform/src/components/copy-button.tsx`），给以下值加了复制按钮：Organization
ID、Project ID（列表和详情）、Webhook Endpoint URL / Endpoint ID、Delivery ID /
Event ID、测试 Receipt ID、Usage 的 Session ID。Account 页原有的复制按钮改用同一组件。
- Projects 和 Usage 表格每行的按钮在 accessible name 里带上行标识（例如 `Copy Project ID
for Production API`），避免多个同名按钮。
- Delivery 详情是 modal，Radix 会把弹窗外的 Toaster 设为
`aria-hidden`，所以按钮在弹窗内另外渲染一个 sr-only 的 `role="status"` 来播报复制结果。
- Delivery 详情弹窗打开时，焦点改为落在弹窗本身。之前数据从缓存渲染时，焦点会落在第一个复制按钮上，并直接弹出 tooltip。
- 未处理：Delivery history 列表里的 event_id 在一个可点击的 `<button>`
里，不能再嵌套按钮，可在详情弹窗复制；API key 列表只显示前缀，不加。

## Test plan
- [x] `web/platform`（Node 24）：`pnpm lint`、`pnpm typecheck`、`pnpm
test`（312 passed）、`pnpm build`
- [x] 新增 `copy-button.test.tsx`：复制成功和失败、行标识、弹窗内 status、空值显示
- [x] 新增 webhooks 测试：从缓存重新打开 Delivery 详情时焦点在弹窗上；去掉修复后该测试失败
- [x] 本地 preview 实际点击 Organization ID 的复制按钮，出现 "Organization ID
copied."；Projects 列表布局正常

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

