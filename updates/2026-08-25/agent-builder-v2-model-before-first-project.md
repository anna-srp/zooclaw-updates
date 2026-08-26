---
title: "修复：Agent Builder 首次建项目时显示的模型和实际跑的模型对不上"
type: "Bug Fix"
priority: "中"
date: "2026-08-25"
status: "待审核"
channels: ""
---

# 修复：Agent Builder 首次建项目时显示的模型和实际跑的模型对不上

## 核心宣传点

当账号里还没有任何 Agent Builder 项目时，新建对话框会退回去显示一个通用的聊天默认模型，而创建请求里其实没带模型，Agent 真正启动后用的是它自己那套安装默认值——于是你看到的模型和它实际在用的模型是两回事。现在空项目状态下也会先把你这个账号真正可用的模型清单读出来，让你在建项目前就选定模型并带进第一轮对话；模型信息还没加载好时，界面宁可先不给选，也不会拿一个假的默认值糊弄你。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `5b29dde3ec5f408600db9438260b9ae37fce540c`
- PR: #3500
- 作者: rayrain-srp
- 日期: 2026-08-25T11:31:32Z

### Commit Message

```
fix(agent-builder): load v2 model before first project (#3500)

## Summary
- expose an authenticated V2 new-project model state using the same
active Pack and Engine catalog resolution as Agent installation
- load that state on an empty Agent Builder home, allow an entitled
model to be selected, and pass it through draft initialization before
the first turn
- fail closed while Builder model state is loading or unavailable
instead of presenting the generic Chat default as the applied model

Fixes [ECA-1396](https://linear.app/srpone/issue/ECA-1396).

## Root cause
When `projects=[]`, the home model query had no Project identity and
stayed disabled. The create dialog then rendered the generic Chat
catalog default, while project creation submitted no model. The
dedicated Engine Agent therefore used its independent Pack/Engine
install default, so the displayed model and actual runtime model could
diverge.

## Test plan
- [x] `pytest tests/unit/test_agent_builder_model_service.py
tests/unit/test_agent_builder_routes.py
tests/unit/test_agent_builder_v2_runtime_service.py -q` (87 passed)
- [x] `pytest tests/unit/test_agent_builder_runtime_services.py -q` (29
passed)
- [x] targeted Vitest coverage for the create dialog, empty-home flow,
V2 client, and mock backend (118 passed)
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh --no-test <changed web/app paths>`
- [x] pre-push PR-size and `bash scripts/verify-changed.sh` gates
```

### PR Description

```
## Summary
- expose an authenticated V2 new-project model state using the same active Pack and Engine catalog resolution as Agent installation
- load that state on an empty Agent Builder home, allow an entitled model to be selected, and pass it through draft initialization before the first turn
- fail closed while Builder model state is loading or unavailable instead of presenting the generic Chat default as the applied model

Fixes [ECA-1396](https://linear.app/srpone/issue/ECA-1396).

## Root cause
When `projects=[]`, the home model query had no Project identity and stayed disabled. The create dialog then rendered the generic Chat catalog default, while project creation submitted no model. The dedicated Engine Agent therefore used its independent Pack/Engine install default, so the displayed model and actual runtime model could diverge.

## Test plan
- [x] `pytest tests/unit/test_agent_builder_model_service.py tests/unit/test_agent_builder_routes.py tests/unit/test_agent_builder_v2_runtime_service.py -q` (87 passed)
- [x] `pytest tests/unit/test_agent_builder_runtime_services.py -q` (29 passed)
- [x] targeted Vitest coverage for the create dialog, empty-home flow, V2 client, and mock backend (118 passed)
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh --no-test <changed web/app paths>`
- [x] pre-push PR-size and `bash scripts/verify-changed.sh` gates

```
