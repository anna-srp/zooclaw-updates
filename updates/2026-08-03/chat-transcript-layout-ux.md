---
title: "聊天消息流与布局体验优化"
type: "体验优化"
priority: "中"
date: "2026-08-03"
status: "待审核"
channels: ""
---

## 核心宣传点

聊天界面更顺手：消息列宽统一、历史消息滚动更稳、空会话展示头像与快捷指令，整体阅读与操作体验更清爽。

## 原始内容

**Commit**: `98a6b5626fa3d7bcc037886eb9cea4ffb21953f3` — david-srp — 2026-08-03T12:08:00Z

### Commit Message

```
feat(web): chat transcript and layout UX improvements (#3101)

## 背景

聊天消息流与布局优化，并补齐旧 engine workspace 的前端头像解析。此前 #3100 已先行合入 P0 bugfix
子集；本分支现已合并最新 main，PR 只保留尚未合入的 transcript/layout 改动与本次头像修正。

## 改动

| 范围 | 说明 |
|---|---|
| 宽度统一 | session 路由与主 chat 使用一致的消息列宽 |
| 历史加载 | prepend 时保持滚动锚点，靠近顶部自动加载，按钮仍作兜底 |
| 流式指示 | 使用共享 `LoadingDots` 替代 ASCII 轮转 |
| 空状态 | 空会话展示头像、名称、问候语与最多 4 个 quick commands |
| 头像解析 | 新增共享 workspace presentation resolver；engine workspace 用
`pack_id` 查 pack avatar/animal，computer workspace 仍用 `agent_id`；主
chat、session thread、sidebar、composer 共用 |

## 测试

- [x] 头像修正红绿 TDD：旧实现无法用 `pack_id` 找到 engine avatar
- [x] 头像与四个入口相关测试：145 passed
- [x] merge 冲突相关测试：131 passed
- [x] `bash scripts/verify-web.sh ...`：governance
guards、tsc、vitest、eslint 全通过
- [x] pre-push：PR size 1577 / 3000，guards、tsc、eslint 全通过

## 部署注意

纯前端。#3099 已删除后端头像读时回填；旧 workspace 的头像展示由本 PR 的前端 pack metadata fallback
负责。

---------

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

```
## 背景

聊天消息流与布局优化，并补齐旧 engine workspace 的前端头像解析。此前 #3100 已先行合入 P0 bugfix 子集；本分支现已合并最新 main，PR 只保留尚未合入的 transcript/layout 改动与本次头像修正。

## 改动

| 范围 | 说明 |
|---|---|
| 宽度统一 | session 路由与主 chat 使用一致的消息列宽 |
| 历史加载 | prepend 时保持滚动锚点，靠近顶部自动加载，按钮仍作兜底 |
| 流式指示 | 使用共享 `LoadingDots` 替代 ASCII 轮转 |
| 空状态 | 空会话展示头像、名称、问候语与最多 4 个 quick commands |
| 头像解析 | 新增共享 workspace presentation resolver；engine workspace 用 `pack_id` 查 pack avatar/animal，computer workspace 仍用 `agent_id`；主 chat、session thread、sidebar、composer 共用 |

## 测试

- [x] 头像修正红绿 TDD：旧实现无法用 `pack_id` 找到 engine avatar
- [x] 头像与四个入口相关测试：145 passed
- [x] merge 冲突相关测试：131 passed
- [x] `bash scripts/verify-web.sh ...`：governance guards、tsc、vitest、eslint 全通过
- [x] pre-push：PR size 1577 / 3000，guards、tsc、eslint 全通过

## 部署注意

纯前端。#3099 已删除后端头像读时回填；旧 workspace 的头像展示由本 PR 的前端 pack metadata fallback 负责。

```
