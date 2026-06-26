---
title: "按订阅套餐限制可雇佣的 Agent 数量"
type: "产品基础功能更新"
priority: "中"
date: "2026-06-25"
status: "待审核"
channels: ""
---

# 按订阅套餐限制可雇佣的 Agent 数量

## 核心宣传点

雇佣 Agent 的数量现在会根据你的订阅套餐档位来计算，套餐权益更清晰；同一 Agent 的重装/更新不会额外占用名额。

## 原始内容

### Commit Message

```
feat(agents): limit v2 installs by plan (#2597)

## Summary

- limit V2 computer-scoped agent installs by subscription tier
- count only active/non-terminal V2 agent workspace rows for the target
computer
- keep existing same-agent reinstall/update paths from consuming an
extra quota slot

## Linear


https://linear.app/srpone/issue/ECA-841/limit-hired-agents-by-subscription-tier

## Validation

- `/Users/bill/.venvs/claw-interface/bin/pytest
services/claw-interface/tests/unit/test_agent_install_service.py
services/claw-interface/tests/unit/test_agent_workspace_repo.py -q`
- `PATH="/Users/bill/.venvs/claw-interface/bin:$PATH" bash
scripts/verify-py.sh`
- `PATH="/Users/bill/.venvs/claw-interface/bin:$PATH" bash
scripts/verify-changed.sh`
```

### PR Description

## Summary

- limit V2 computer-scoped agent installs by subscription tier
- count only active/non-terminal V2 agent workspace rows for the target computer
- keep existing same-agent reinstall/update paths from consuming an extra quota slot

## Linear

https://linear.app/srpone/issue/ECA-841/limit-hired-agents-by-subscription-tier

## Validation

- `/Users/bill/.venvs/claw-interface/bin/pytest services/claw-interface/tests/unit/test_agent_install_service.py services/claw-interface/tests/unit/test_agent_workspace_repo.py -q`
- `PATH="/Users/bill/.venvs/claw-interface/bin:$PATH" bash scripts/verify-py.sh`
- `PATH="/Users/bill/.venvs/claw-interface/bin:$PATH" bash scripts/verify-changed.sh`

