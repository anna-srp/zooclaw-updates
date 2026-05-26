---
title: "修复 Pack Store 排序问题"
type: "Bug Fix"
priority: "中"
date: "2026-05-25"
status: "待审核"
channels: ""
---

# 修复 Pack Store 排序问题

## 核心宣传点

修复 Pack Store 中 Agent 排序可能出错的问题，浏览 Agent 商店时排序更稳定

## 原始内容

**仓库**: SerendipityOneInc/ecap-workspace  
**Commit**: 074b68d2f70fd8fd418cadda6f9808fee3463060  
**作者**: bill-srp  
**日期**: 2026-05-25T07:11:25Z  

**Commit Message**:

```
fix(pack-store): use mongo-compatible sort arguments (#1907)

## Summary
- Use Mongo-compatible sort argument shapes in pack repositories
- Add unit coverage for pack and pack-submission sort behavior

## Split
Independent cleanup split out of the enterprise account PR because it is
unrelated to account/org registration.

## Checks
- devcontainer: ruff check pack repository files
- devcontainer: pyright pack repository files
- devcontainer: pytest tests/unit/test_pack_repo.py
tests/unit/test_pack_submission_repo.py (14 passed)
- size check: under budget
```

**PR Description**:

## Summary
- Use Mongo-compatible sort argument shapes in pack repositories
- Add unit coverage for pack and pack-submission sort behavior

## Split
Independent cleanup split out of the enterprise account PR because it is unrelated to account/org registration.

## Checks
- devcontainer: ruff check pack repository files
- devcontainer: pyright pack repository files
- devcontainer: pytest tests/unit/test_pack_repo.py tests/unit/test_pack_submission_repo.py (14 passed)
- size check: under budget
