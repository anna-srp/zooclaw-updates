---
title: "临时存储空间不足时给出提醒"
type: "体验优化"
priority: "中"
date: "2026-06-23"
status: "待审核"
channels: ""
---
# 临时存储空间不足时给出提醒

## 核心宣传点
当 Agent 临时存储空间使用接近上限时，输入框会出现温馨提醒，避免因空间满导致任务异常。

## 原始内容
```
feat(openclaw): warn on ephemeral storage risk (#2562)

## Linear
https://linear.app/srpone/issue/ECA-1058/ephemeral-storage-risk-warning

## Summary
- Add ephemeral storage typing and parsing for FastClaw resources,
including request, limit, and used quantities.
- Poll main bot resources and show a reminder-only composer warning when
used / limit reaches 80%, clearing only below 75%.
- Suppress the uid-scoped warning on computer-specific chats and guard
against stale or mismatched bot resources.
- Add mock backend data and unit coverage for parsing, the risk hook,
composer forwarding, and API pass-through.

## Test plan
- [x] bash scripts/verify-changed.sh
- [x] bash scripts/verify-web.sh selected changed frontend paths
- [x] bash scripts/verify-py.sh
- [x] Focused frontend vitest for storage parser, risk hook, composer,
chat surface, and API route coverage
- [x] Focused backend pytest for OpenClaw resources pass-through
```

### PR description
## Linear
https://linear.app/srpone/issue/ECA-1058/ephemeral-storage-risk-warning

## Summary
- Add ephemeral storage typing and parsing for FastClaw resources, including request, limit, and used quantities.
- Poll main bot resources and show a reminder-only composer warning when used / limit reaches 80%, clearing only below 75%.
- Suppress the uid-scoped warning on computer-specific chats and guard against stale or mismatched bot resources.
- Add mock backend data and unit coverage for parsing, the risk hook, composer forwarding, and API pass-through.

## Test plan
- [x] bash scripts/verify-changed.sh
- [x] bash scripts/verify-web.sh selected changed frontend paths
- [x] bash scripts/verify-py.sh
- [x] Focused frontend vitest for storage parser, risk hook, composer, chat surface, and API route coverage
- [x] Focused backend pytest for OpenClaw resources pass-through

