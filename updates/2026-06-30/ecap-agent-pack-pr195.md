---
title: "Agent Studio 打包测试前提前校验元信息"
type: "体验优化"
priority: "中"
date: "2026-06-30"
status: "待审核"
channels: ""
---
# Agent Studio 打包测试前提前校验元信息
## 核心宣传点
Agent Studio 在你点击「打包并测试」之前就会校验 quick_commands、description.json 等元信息，若有问题会在搭建对话里由 AI 直接提示修复，避免到后期才报错。
## 原始内容
fix(agent-studio): validate pack test metadata before handoff (#195)

* fix(agent-studio): validate pack test metadata before handoff

* test(agent-studio): cover quick commands in pack test gate

* fix(agent-studio): address pack test gate review findings

---

### PR Description

## Context

Linear: https://linear.app/srpone/issue/ECA-1095/agent-builder-%E6%B5%8B%E8%AF%95%E8%BF%AD%E4%BB%A3%E5%A4%B1%E8%B4%A5-quick-commands-%E5%AD%97%E6%AE%B5-json-%E6%A0%BC%E5%BC%8F%E6%A0%A1%E9%AA%8C%E9%94%99%E8%AF%AF

The failure mode here is not just "block bad metadata eventually." The important part is where the error lands: Agent Studio's build agent needs to see validation failures before the creator clicks Package & Test, so the agent can fix the pack in the build chat instead of surfacing a late UI/backend error to the user.

## Solution

This PR adds an Agent Studio pre-Package & Test validation path:

- Adds `validate.py --pack-test-gate`.
- Keeps regular Stage 4 validation unchanged: missing listing assets stay warnings because `description.json` is generated later in Stage 5a.
- In `--pack-test-gate` mode, `validate.py` still runs the existing suite, including `quick_commands`, and adds a strict `description_json` check.
- That means invalid `quick_commands` in `agent/agent-pack.yaml` fail in the same build-chat preflight as listing metadata, so Agent Studio can repair the manifest before the creator clicks Package & Test.
- The new `description_json` check validates that `agent/description.json` exists, is a JSON object, has an `agentPack_id` matching `agent/agent-pack.yaml#name`, has required listing fields filled, rejects TODO placeholders, and checks schema-sensitive fields like `category`, `badge`, `pickedCount`, and text lists.
- Updates Agent Studio docs so Stage 5 requires the build agent to run `validate.py --skip-online-validation --pack-test-gate` before asking the creator to click Package & Test.

I intentionally did not add a new hard gate inside `publish.py start` in this PR. A `publish.py` failure would happen after the UI handoff; this change keeps the fix loop inside Agent Studio where the agent can inspect the JSON result, edit the pack, and rerun validation before involving the creator.

## Purpose

The goal is to prevent invalid `quick_commands` / listing metadata from reaching Pack Test while preserving the right UX loop:

- build agent sees structured validation errors
- build agent repairs `agent/description.json` or `agent/agent-pack.yaml`
- creator is only asked to click Package & Test after the preflight passes

## Tests

- `python -m pytest agent-studio/.agents/skills/agent-studio/tests`
- `python -m unittest discover -s agent-studio/.agents/skills/agent-studio/scripts/tests -p 'test_*.py'`

