---
title: "IM 频道接入体验改版"
type: "体验优化"
priority: "中"
date: "2026-08-03"
status: "待审核"
channels: ""
---

## 核心宣传点

IM 频道接入改为统一的平台卡片网格，Telegram、钉钉、Discord、Slack、飞书、企业微信、微信等设置弹窗视觉与交互统一，连接更直观。

## 原始内容

**Commit**: `b9fb66003a8bbca31eb083edfdb663c58134868f` — shana-srp — 2026-08-03T05:51:17Z

### Commit Message

```
feat(channels): redesign IM channel setup experience (#3091)

## Linear

N/A

## Summary
- 将 IM 频道平台选择重构为统一的平台卡片网格，并补齐各平台品牌图标与中英文文案。
- 统一 Telegram、DingTalk、Discord、Slack、Feishu、WeCom、Weixin
等设置弹窗的视觉、固定头部与连接方式切换交互。
- 优化 Agent 选择和引导连接流程，同时保留现有频道连接数据结构、提交参数与后端逻辑。
- 增加频道卡片与设置向导单元测试，并记录本次复杂 UI 重构设计说明。

## Test plan
- [x] Git pre-commit frontend lint
- [x] Git pre-push changed-surface verification (governance guards,
TypeScript, ESLint)
- [x] Channel-related unit tests (129 passed during implementation)
- [ ] Full local Vitest suite (current shell is Node 20; workspace
requires Node 24)

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Body

```
## Linear

N/A

## Summary
- 将 IM 频道平台选择重构为统一的平台卡片网格，并补齐各平台品牌图标与中英文文案。
- 统一 Telegram、DingTalk、Discord、Slack、Feishu、WeCom、Weixin 等设置弹窗的视觉、固定头部与连接方式切换交互。
- 优化 Agent 选择和引导连接流程，同时保留现有频道连接数据结构、提交参数与后端逻辑。
- 增加频道卡片与设置向导单元测试，并记录本次复杂 UI 重构设计说明。

## Test plan
- [x] Git pre-commit frontend lint
- [x] Git pre-push changed-surface verification (governance guards, TypeScript, ESLint)
- [x] Channel-related unit tests (129 passed during implementation)
- [ ] Full local Vitest suite (current shell is Node 20; workspace requires Node 24)

```
