---
title: "对话体验优化：Agent 回复不再重复显示头像和名称"
type: "体验优化"
priority: "中"
date: "2026-07-20"
status: "待审核"
channels: ""
---

## 核心宣传点

优化了聊天中 Agent 回复的展示：当一次回复包含中间文本、工具调用和最终结果多段时，不再重复显示头像和名称，界面更清爽，同时保留消息的真实顺序。

### 原始内容

**Commit message:**

```
fix(chat): group ordered assistant reply segments (#2950)

## 背景

Mattermost 按真实顺序分别投递中间文本、工具状态和最终文本。前端此前把这些物理消息渲染成多次独立 agent
回复，重复展示头像和名称；仅比较紧邻消息还会让 tool-first 回复完全没有 agent 身份。当前仍有部署在 K8s、尚未切换
ZooClaw Engine 的旧 OpenClaw bot，因此新归组规则必须保留无 run_id 消息的原有展示行为。

## 改动

- 从 Mattermost post props 读取 run_id、turn 和 segment，并传入 assistant-ui
message metadata。
- 有 run_id 时，在同一 run 内向前跨过 tool group 查找已有文本段，只在已经展示过 assistant
身份时隐藏后续头像和名称。
- tool → text 保留最终文本的头像和名称。
- text → tool → text 只展示一次 assistant 身份，同时保持三段消息的真实顺序。
- 没有 run_id 时保留旧 OpenClaw 的紧邻 assistant 归组行为，tool group 仍作为边界。
- 新旧消息格式交界、不同 run 之间均不归组，避免误合并。

## 验证

- bash scripts/verify-web.sh 相关文件
- 原实现相关 133 tests passed
- 兼容加固后 OpenClawThread 38 tests passed
- TypeScript、eslint 和全部治理 guards 通过
- agent review 最终无剩余 actionable finding

## 关联

- Linear:
https://linear.app/srpone/issue/ECA-1278/fix-mattermost-reply-grouping-and-output-ack-delay
- ACS 配套 PR:
https://github.com/SerendipityOneInc/agent-channel-service/pull/34
```

**PR body:**

## 背景

Mattermost 按真实顺序分别投递中间文本、工具状态和最终文本。前端此前把这些物理消息渲染成多次独立 agent 回复，重复展示头像和名称；仅比较紧邻消息还会让 tool-first 回复完全没有 agent 身份。当前仍有部署在 K8s、尚未切换 ZooClaw Engine 的旧 OpenClaw bot，因此新归组规则必须保留无 run_id 消息的原有展示行为。

## 改动

- 从 Mattermost post props 读取 run_id、turn 和 segment，并传入 assistant-ui message metadata。
- 有 run_id 时，在同一 run 内向前跨过 tool group 查找已有文本段，只在已经展示过 assistant 身份时隐藏后续头像和名称。
- tool → text 保留最终文本的头像和名称。
- text → tool → text 只展示一次 assistant 身份，同时保持三段消息的真实顺序。
- 没有 run_id 时保留旧 OpenClaw 的紧邻 assistant 归组行为，tool group 仍作为边界。
- 新旧消息格式交界、不同 run 之间均不归组，避免误合并。

## 验证

- bash scripts/verify-web.sh 相关文件
- 原实现相关 133 tests passed
- 兼容加固后 OpenClawThread 38 tests passed
- TypeScript、eslint 和全部治理 guards 通过
- agent review 最终无剩余 actionable finding

## 关联

- Linear: https://linear.app/srpone/issue/ECA-1278/fix-mattermost-reply-grouping-and-output-ack-delay
- ACS 配套 PR: https://github.com/SerendipityOneInc/agent-channel-service/pull/34
