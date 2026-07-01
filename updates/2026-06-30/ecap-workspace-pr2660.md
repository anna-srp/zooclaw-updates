---
title: "修复 Agent Builder 提交新版本时元信息被旧数据覆盖"
type: "Bug Fix"
priority: "中"
date: "2026-06-30"
status: "待审核"
channels: ""
---
# 修复 Agent Builder 提交新版本时元信息被旧数据覆盖
## 核心宣传点
在 Agent Builder 更新已有 Agent 包并提交新版本时，本次修改的头像、分类、简介、技能、快捷指令等信息能被正确提交，不再沿用旧版本的过期内容。
## 原始内容
fix(agent-builder): submit current run metadata (#2660)

## Summary
- Submit Agent Builder Pack Store metadata from the current accepted
Pack Test run for both new packs and existing pack updates.
- Centralize the metadata mapping for `avatar_url`, `category`,
`short_bio`, `bio`, `skills`, `integrations`, `automations`, and
`quick_commands`.
- Add regression coverage proving an existing pack's stale metadata is
not reused when submitting a new version.

## Root cause
Agent Builder submit derives submission data from the latest Pack Test
run. The create-pack branch already used current run metadata, but the
existing-pack update branch passed metadata from the persisted `Pack`
row into `submit_new_version`. That meant changes made in the current
`description.json` or `agent-pack.yaml` `quick_commands` could be lost
when submitting a new version for an existing pack.

## Test plan
- [x] `python -m pytest
services/claw-interface/tests/unit/test_agent_builder_service.py`
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh` during push hook

---

### PR Description

## Summary
- Submit Agent Builder Pack Store metadata from the current accepted Pack Test run for both new packs and existing pack updates.
- Centralize the metadata mapping for `avatar_url`, `category`, `short_bio`, `bio`, `skills`, `integrations`, `automations`, and `quick_commands`.
- Add regression coverage proving an existing pack's stale metadata is not reused when submitting a new version.

## Root cause
Agent Builder submit derives submission data from the latest Pack Test run. The create-pack branch already used current run metadata, but the existing-pack update branch passed metadata from the persisted `Pack` row into `submit_new_version`. That meant changes made in the current `description.json` or `agent-pack.yaml` `quick_commands` could be lost when submitting a new version for an existing pack.

## Test plan
- [x] `python -m pytest services/claw-interface/tests/unit/test_agent_builder_service.py`
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh` during push hook

