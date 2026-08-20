---
title: "聊天界面新增 Codex 风格「Agent 活动时间线」，AI 每一步都看得见"
type: "新功能上线"
priority: "高"
date: "2026-08-19"
status: "待审核"
channels: ""
---

# 聊天界面新增 Codex 风格「Agent 活动时间线」，AI 每一步都看得见

## 核心宣传点

主聊天、会话线程、Agent Builder 和预览测试聊天全部统一为「思考说明 → 执行动作 → 最终回答」的时间线视图：AI 正在调用什么能力、跑了多久、成功还是失败、被取消，全程一目了然，长步骤可折叠，不用再对着空白等待猜它在干嘛。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `2afc874595cab5436570b5357caf2f44023d5c98`
- PR: #3438
- 作者: kaka-srp
- 日期: 2026-08-19T12:55:15Z

### Commit Message

```
feat(chat): add Codex-style agent activity timeline (#3438)

## Linear

N/A — 按需求不创建 Linear issue。

## Summary

- 将 Main Chat、Session Thread、Agent Builder 和 Preview/Test Chat 统一为 Codex
风格的 `commentary → activity → final answer` 时间线，并复用
`zooclaw-design-system` 的 disclosure、item、spinner 和 alert 组件。
- 完成当前 v2 工具面与实际返回通道盘点；activity 只展示工具级正向 allowlist 中的调用意图，以及
command/patch/plan 的安全运行时投影，不再展示 Web、文件、MCP、Composio、内存等工具的 raw result
preview。
- 保留运行、完成、失败、取消、真实耗时、长步骤折叠和 Agent 身份连续性，并在消息区出现可渲染事件后接管 composer
activity 状态。
- 保持 Markdown、附件、Artifact、交互卡片、分享和 legacy Mattermost 历史兼容；设计与工具输出契约记录在本
PR 的 spec 中。

## Test plan

- [x] `bash scripts/verify-web.sh --no-clean <10 related unit specs>` —
10 files / 326 tests passed，包含 TypeScript、ESLint 与 governance guards。
- [x] `cd web/packages/chat-ui && pnpm test && pnpm tsc && pnpm lint` —
33 files / 431 tests passed。
- [x] `bash scripts/verify-changed.sh` — all changed surfaces passed
after merging latest `origin/main`。
- [x] `git diff --check origin/main...HEAD`。
```

### PR Body

## Linear

N/A — 按需求不创建 Linear issue。

## Summary

- 将 Main Chat、Session Thread、Agent Builder 和 Preview/Test Chat 统一为 Codex 风格的 `commentary → activity → final answer` 时间线，并复用 `zooclaw-design-system` 的 disclosure、item、spinner 和 alert 组件。
- 完成当前 v2 工具面与实际返回通道盘点；activity 只展示工具级正向 allowlist 中的调用意图，以及 command/patch/plan 的安全运行时投影，不再展示 Web、文件、MCP、Composio、内存等工具的 raw result preview。
- 保留运行、完成、失败、取消、真实耗时、长步骤折叠和 Agent 身份连续性，并在消息区出现可渲染事件后接管 composer activity 状态。
- 保持 Markdown、附件、Artifact、交互卡片、分享和 legacy Mattermost 历史兼容；设计与工具输出契约记录在本 PR 的 spec 中。

## Test plan

- [x] `bash scripts/verify-web.sh --no-clean <10 related unit specs>` — 10 files / 326 tests passed，包含 TypeScript、ESLint 与 governance guards。
- [x] `cd web/packages/chat-ui && pnpm test && pnpm tsc && pnpm lint` — 33 files / 431 tests passed。
- [x] `bash scripts/verify-changed.sh` — all changed surfaces passed after merging latest `origin/main`。
- [x] `git diff --check origin/main...HEAD`。

