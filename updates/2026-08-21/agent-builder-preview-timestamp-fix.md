---
title: "修复：Agent Builder 测试环境构建中时预览接口报错"
type: "Bug Fix"
priority: "中"
date: "2026-08-21"
status: "待审核"
channels: ""
---

# 修复：Agent Builder 测试环境构建中时预览接口报错

## 核心宣传点

新建 Pack 测试环境时，如果环境还在构建中就去看预览，接口会因为时间格式不一致直接抛错，页面看不到「正在构建」的真实状态，只能干等。现在读取环境时间戳时会统一时区，构建中和超时两种情况都能正常返回状态。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `6dfdac721dad39465a6b517fbe3a0a9a84973ed0`
- PR: #3474
- 作者: kaka-srp
- 日期: 2026-08-21T03:30:35Z

### Commit Message

```
fix(agent-builder): normalize preview environment timestamps (#3474)

## Summary

- Normalize persisted Pack Test Environment timestamps before Preview
deadline comparisons.
- Cover MongoDB-decoded naïve timestamps while an Environment is
building and when it times out.

## Root cause

MongoDB decodes persisted datetimes without timezone information, while
the Preview runtime compares them with `datetime.now(UTC)`. When a new
Pack Test Environment was still building, that mixed naïve and aware
values and raised `TypeError: can't compare offset-naive and
offset-aware datetimes` instead of returning the build status.

## Test plan

- [x] `pytest -q tests/unit/test_pack_test_engine_runtime_service.py` (9
passed)
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
```

### PR Body

## Summary

- Normalize persisted Pack Test Environment timestamps before Preview deadline comparisons.
- Cover MongoDB-decoded naïve timestamps while an Environment is building and when it times out.

## Root cause

MongoDB decodes persisted datetimes without timezone information, while the Preview runtime compares them with `datetime.now(UTC)`. When a new Pack Test Environment was still building, that mixed naïve and aware values and raised `TypeError: can't compare offset-naive and offset-aware datetimes` instead of returning the build status.

## Test plan

- [x] `pytest -q tests/unit/test_pack_test_engine_runtime_service.py` (9 passed)
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`

