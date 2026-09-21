---
title: "fix(chat): show friendly insufficient credits error copy (#3822)"
type: "Bug Fix"
priority: "中"
date: "2026-09-20"
status: "待审核"
channels: ""
---

# 修复：积分不足时显示友好提示，而不是原始报错

## 核心宣传点

当一条助手错误消息与某个 state 为 error、errorCode 为 insufficient_credits 的用户轮次属于同一个 run 时，聊天里会显示本地化的友好文案（中文「积分不足」一类提示），不再把带供应商前缀的原始错误正文摔给用户。判断完全基于 error_code，不依赖服务端返回的文案。

## 分级

- 内部：P2
- 外部：B
- 发布状态：已合并待发版

## PR 说明

## Summary
When an assistant error message has the same run ID as a user turn with `state: error` and `errorCode: insufficient_credits`, display friendly localized copy instead of the provider-prefixed error body.

- Chinese: 积分不足，充值后请重新发送。
- English and all other supported locales via existing dictionary fallback: Insufficient credits. Add credits, then send your message again.

Use existing structured metadata only; no string matching or new API. Preserve unrelated errors and messages without matching run metadata. The original Mattermost message, existing red-frame styling, and B2 recharge notice remain unchanged.

## Validation
- TypeScript and repository governance checks passed.
- Focused component and dictionary suites: 65 tests passed, including delayed status arrival, run isolation, unrelated error codes, and all 10 supported locales.
- ESLint passed on the changed component and dictionary tests; full lint runs in the commit/push gates.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `fcaeb00b32b48241b19ea7473989591c415a385c`
- PR: #3822
- 作者：tim-srp
- 日期：2026-09-20T13:46:44Z

### Commit Message

```
fix(chat): show friendly insufficient credits error copy (#3822)

## Summary
When an assistant error message has the same run ID as a user turn with
`state: error` and `errorCode: insufficient_credits`, display friendly
localized copy instead of the provider-prefixed error body.

- Chinese: 积分不足，充值后请重新发送。
- English and all other supported locales via existing dictionary
fallback: Insufficient credits. Add credits, then send your message
again.

Use existing structured metadata only; no string matching or new API.
Preserve unrelated errors and messages without matching run metadata.
The original Mattermost message, existing red-frame styling, and B2
recharge notice remain unchanged.

## Validation
- TypeScript and repository governance checks passed.
- Focused component and dictionary suites: 65 tests passed, including
delayed status arrival, run isolation, unrelated error codes, and all 10
supported locales.
- ESLint passed on the changed component and dictionary tests; full lint
runs in the commit/push gates.
```

来源：SerendipityOneInc/ecap-workspace @ fcaeb00b，PR #3822，作者 tim-srp。