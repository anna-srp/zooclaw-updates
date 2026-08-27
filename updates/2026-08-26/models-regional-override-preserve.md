---
title: "修复：部分可用模型在模型列表里凭空消失"
type: "Bug Fix"
priority: "中"
date: "2026-08-26"
status: "待审核"
channels: ""
---

# 修复：部分可用模型在模型列表里凭空消失

## 核心宣传点

区域化的模型展示配置此前被当成了一份「白名单」，凡是没在配置里出现的模型都会被从列表里抹掉，导致你明明有权限用的模型却选不到。现在区域配置只负责给已配置的模型改个显示名，没被配置到的模型一律保留原样和原有权限；配置本身读取失败时也会回退到模型的原始信息，而不是把列表清空。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `b8ff412af9d6913c4dda511221714f27f695ab8e`
- PR: #3531
- 作者: sam-srp
- 日期: 2026-08-26T11:23:06Z

### Commit Message

```
fix(models): preserve models without regional overrides (#3531)

## Summary
- resolve model display overrides from any active team organization
region_code instead of hardcoding CN
- apply regional aliases only to configured models while preserving
entitled unmapped models with their original LiteLLM metadata
- stop treating regional display configuration as an Agent Builder
allowlist
- fall back to original model metadata when regional override
configuration is unavailable

## Testing
- ruff check and format checks
- targeted Pyright: 0 errors
- 61 related claw-interface unit tests passed
```

### PR Description

```
## Summary
- resolve model display overrides from any active team organization region_code instead of hardcoding CN
- apply regional aliases only to configured models while preserving entitled unmapped models with their original LiteLLM metadata
- stop treating regional display configuration as an Agent Builder allowlist
- fall back to original model metadata when regional override configuration is unavailable

## Testing
- ruff check and format checks
- targeted Pyright: 0 errors
- 61 related claw-interface unit tests passed
```
