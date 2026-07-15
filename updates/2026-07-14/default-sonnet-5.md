---
title: "对话默认升级到 Claude Sonnet 5"
type: "体验优化"
priority: "高"
date: "2026-07-14"
status: "待审核"
channels: ""
---

# 对话默认升级到 Claude Sonnet 5

## 核心宣传点
Free/Starter/Pro/Ultra 各套餐的对话默认模型升级为更强的 Claude Sonnet 5，回答质量更好。

## 原始内容
### PR #2853 — feat(claw-interface): default chats to Claude Sonnet 5 (#2853)
作者: rayrain-srp | https://github.com/SerendipityOneInc/ecap-workspace/pull/2853

## Linear

https://linear.app/srpone/issue/ECA-1232/

## Summary

- make `claude-sonnet-5` the default chat model for Free, Starter, Pro, Ultra, empty, and unknown plans
- keep the OpenClaw primary model derived from the baseline plan as `openai/claude-sonnet-5`
- add the Sonnet 5 chat degradation mapping while retaining Sonnet 4.6 support
- lock new-bot creation and missing-model repair behavior with focused tests

## Release ordering

Blocked by https://github.com/SerendipityOneInc/gcp-foundation/pull/454. Merge, deploy, and verify the FastClaw runtime registration first; only then deploy this product-default change. Use the same order in staging and production.

## Scope note

This rotates defaults for new bots and the existing missing-`model.primary` repair path. It intentionally does not migrate bots that already have an explicit primary model or overwrite a user's current selection in the settings route. Model availability in settings remains governed by the dynamic plan access groups.

## Test plan

- [x] Verify TDD RED against the old defaults, then GREEN after the minimal product change
- [x] Run all three affected unit-test files (`217 passed`)
- [x] Run `bash scripts/verify-py.sh` (Ruff, format, Pyright, import-linter)
- [x] Run `git diff --check` and verify only the four intended files changed
- [ ] After the infrastructure rollout, create a staging bot and verify text and image requests
- [ ] Repeat the ordered rollout and smoke test in production
