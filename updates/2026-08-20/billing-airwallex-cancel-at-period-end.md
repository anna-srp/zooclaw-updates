---
title: "修复：取消订阅改为周期末生效，不再立即失效"
type: "Bug Fix"
priority: "高"
date: "2026-08-20"
status: "待审核"
channels: ""
---

# 修复：取消订阅改为周期末生效，不再立即失效

## 核心宣传点

此前用信用卡（Airwallex）取消订阅时会误走「立即取消」接口，导致已付费的剩余周期直接作废。现已改为周期末取消——取消后仍可正常使用到当前计费周期结束。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `68e0059dbedbab6c80a4dc4c3e864e755b23f4e9`
- PR: #3459
- 作者: tim-srp
- 日期: 2026-08-20T08:00:34Z

### Commit Message

```
fix(billing): correct Airwallex subscription cancellation (#3459)

## Summary

- 修复 Airwallex 订阅取消误走立即取消接口的问题，改为周期末取消。
- 兼容官方 subscription retrieve 与 webhook payload 字段。
- 保留 webhook Event ID 的幂等语义。

## Root cause

订阅 schema 未建模官方 `starts_at` / `ends_at`
字段，导致变更已提交后本地响应校验仍误判周期不一致。取消操作使用了立即取消 endpoint，且 webhook 仅支持
`data.object` 嵌套结构。

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] 运行 108 个 Airwallex 相关单元测试

Closes #3456
```

### PR Body

## Summary

- 修复 Airwallex 订阅取消误走立即取消接口的问题，改为周期末取消。
- 兼容官方 subscription retrieve 与 webhook payload 字段。
- 保留 webhook Event ID 的幂等语义。

## Root cause

订阅 schema 未建模官方 `starts_at` / `ends_at` 字段，导致变更已提交后本地响应校验仍误判周期不一致。取消操作使用了立即取消 endpoint，且 webhook 仅支持 `data.object` 嵌套结构。

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] 运行 108 个 Airwallex 相关单元测试

Closes #3456


