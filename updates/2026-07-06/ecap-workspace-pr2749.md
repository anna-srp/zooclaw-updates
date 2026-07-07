---
title: "Agent Builder 操作按钮支持中文显示"
type: "体验优化"
priority: "中"
date: "2026-07-06"
status: "待审核"
channels: ""
---

# Agent Builder 操作按钮支持中文显示

## 核心宣传点

用中文创建 Agent 时，Builder 里的操作按钮（如「重新打包并测试」）也会显示中文名称，不再中英混杂，指引更清楚。

## 原始内容

[23d1bc5d] fix(agent-builder): localize builder prompt actions (#2749)

## Summary

- Update the Agent Builder runtime bootstrap prompt so Builder UI action
names follow the creator language: Chinese UI names for Chinese
conversations, English names otherwise.
- Align Pack Test feedback repair guidance so Chinese users are told to
use `重新打包并测试` instead of the English `Package & Test Again`.
- Pair with Agent Studio prompt pack update:
https://github.com/SerendipityOneInc/ecap-agent-pack/pull/199

## Tests

- `python -m py_compile
services/claw-interface/app/services/agent_builder_service.py`
- `git diff --cached --check`
- pre-push `verify-changed` via `git push`

--- PR #2749 body ---
## Summary

- Update the Agent Builder runtime bootstrap prompt so Builder UI action names follow the creator language: Chinese UI names for Chinese conversations, English names otherwise.
- Align Pack Test feedback repair guidance so Chinese users are told to use `重新打包并测试` instead of the English `Package & Test Again`.
- Pair with Agent Studio prompt pack update: https://github.com/SerendipityOneInc/ecap-agent-pack/pull/199

## Tests

- `python -m py_compile services/claw-interface/app/services/agent_builder_service.py`
- `git diff --cached --check`
- pre-push `verify-changed` via `git push`



[fef77df5] fix(agent-studio): localize builder UI action prompts (#199)

--- PR #199 body ---
## Summary

- Update Agent Studio bootstrap and root skill prompts so Builder UI action names follow the creator language: Chinese UI names for Chinese conversations, English names otherwise.
- Align packaging and delivery guidance for localized Package & Test, Package & Test Again, Accept Test, Submit, Share, and Open references.
- Pair with Agent Builder runtime prompt update: https://github.com/SerendipityOneInc/ecap-workspace/pull/2749

## Tests

- `git diff --cached --check`

