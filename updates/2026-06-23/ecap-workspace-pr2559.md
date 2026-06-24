---
title: "主助手默认名称统一显示为「Assistant」"
type: "体验优化"
priority: "中"
date: "2026-06-23"
status: "待审核"
channels: ""
---
# 主助手默认名称统一显示为「Assistant」

## 核心宣传点
主助手不再显示 zoo-xxx 这类系统内部名称，统一展示为「Assistant」，同时保留你自定义的名字。

## 原始内容
```
fix(api): normalize main computer agent name (#2559)

## Summary
- Normalize the V2 computer agents response so main-agent system default
names (`zoo-{uid}` / `zoo-{uid}-{timestamp}` / blank) display as
`Assistant`.
- Preserve custom main-agent names from `AgentWorkspace.name`, so user
rename flows are not masked.
- Normalize new main Mattermost workspace projections to store
`Assistant` instead of continuing to mirror `zoo-*` defaults.

## Root cause
The V2 `/computers/{computer_id}/agents` response projected
`AgentWorkspace.name` directly, so historical main-agent rows
initialized from computer/Mattermost defaults could surface names like
`zoo-{uid}`. A previous response-layer hardcode fixed the default
display but masked valid user-renamed main agents; this version only
normalizes system default names.

## Test plan
- [x]
`/Users/bill/Github/StarQuestAI/ecap-workspace-ios-1.8.0/services/claw-interface/.venv/bin/python
-m pytest services/claw-interface/tests/unit/test_agent_service.py
services/claw-interface/tests/unit/test_agent_mm_projectors.py`
- [x]
`PATH="/Users/bill/Github/StarQuestAI/ecap-workspace-ios-1.8.0/services/claw-interface/.venv/bin:$PATH"
bash scripts/verify-py.sh`

Note: the normal commit pre-commit hook hung while running `pre-commit`
with no hook output, so commits were created with `--no-verify` after
the equivalent backend checks above passed.
```

### PR description
## Summary
- Normalize the V2 computer agents response so main-agent system default names (`zoo-{uid}` / `zoo-{uid}-{timestamp}` / blank) display as `Assistant`.
- Preserve custom main-agent names from `AgentWorkspace.name`, so user rename flows are not masked.
- Normalize new main Mattermost workspace projections to store `Assistant` instead of continuing to mirror `zoo-*` defaults.

## Root cause
The V2 `/computers/{computer_id}/agents` response projected `AgentWorkspace.name` directly, so historical main-agent rows initialized from computer/Mattermost defaults could surface names like `zoo-{uid}`. A previous response-layer hardcode fixed the default display but masked valid user-renamed main agents; this version only normalizes system default names.

## Test plan
- [x] `/Users/bill/Github/StarQuestAI/ecap-workspace-ios-1.8.0/services/claw-interface/.venv/bin/python -m pytest services/claw-interface/tests/unit/test_agent_service.py services/claw-interface/tests/unit/test_agent_mm_projectors.py`
- [x] `PATH="/Users/bill/Github/StarQuestAI/ecap-workspace-ios-1.8.0/services/claw-interface/.venv/bin:$PATH" bash scripts/verify-py.sh`

Note: the normal commit pre-commit hook hung while running `pre-commit` with no hook output, so commits were created with `--no-verify` after the equivalent backend checks above passed.

