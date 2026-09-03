---
title: "修复：Agent Pack 测试预览有时读不到技能内容"
type: "Bug Fix"
priority: "中"
date: "2026-09-02"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：Agent Pack 测试预览有时读不到技能内容

## 核心宣传点

Pack 测试的预览路径以前在启动 Engine Agent 之后就立刻创建预览会话，没有等沙箱和技能严格就绪。这中间如果发生一次配置更新，第一个工作流在完成初次同步之前就已经过期，导致预览的第一轮对话去读 `SKILL.md` 时看到的是一个空的共享技能视图——表现为技能像是没装上。

现在在预览 Agent 启动之后、创建会话之前，会先跑一遍已有的严格沙箱准备屏障，并复用有边界的配置版本重试路径，把配置竞争解析到最新的活跃版本。如果沙箱或技能准备失败，预览会明确保持不可用状态，而不是给出一个内容不完整的预览。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `e43138cd3fd477d72a28bea604260ced3aa9caf4`
- PR: #3574
- 作者: sharplee-srp
- 日期: 2026-09-02T03:37:23Z

### Commit Message

```
fix(pack-tests): wait for sandbox readiness before preview (#3574)

## Summary

- run the existing strict Agent Sandbox preparation barrier after the
preview Agent starts and before creating its Session
- reuse the bounded config-version retry path so config races are
resolved against the latest active version
- keep the preview unavailable when Sandbox or Skill preparation fails

## Root cause

The Pack test preview path started the Engine Agent and immediately
created a preview Session without waiting for strict Sandbox/Skill
readiness. A config update could therefore make the first workflow stale
before its initial sync, leaving the shared Skill view empty when the
first preview turn attempted to read `SKILL.md`.

## Dependency and rollout

Depends on SerendipityOneInc/zooclaw-engine#991. Deploy the Engine PR
first, then this ECAP change.

## Test plan

- [x] `pytest tests/unit/test_pack_test_engine_runtime_service.py
tests/unit/test_engine_agent_resource_class.py -q` — 22 passed
- [x] Ruff check and format check on both changed Python files
- [x] Pyright on both changed Python files — 0 errors
- [x] pre-commit changed-file checks, import contracts, and PR size gate
- [ ] Repository-wide `bash scripts/verify-py.sh` is blocked by existing
unrelated main-branch baseline issues: 72 Ruff findings, 20 files
requiring formatting, and 4 route-helper Pyright errors; all 8
import-linter contracts pass
```

### PR Body

```
## Summary

- run the existing strict Agent Sandbox preparation barrier after the preview Agent starts and before creating its Session
- reuse the bounded config-version retry path so config races are resolved against the latest active version
- keep the preview unavailable when Sandbox or Skill preparation fails

## Root cause

The Pack test preview path started the Engine Agent and immediately created a preview Session without waiting for strict Sandbox/Skill readiness. A config update could therefore make the first workflow stale before its initial sync, leaving the shared Skill view empty when the first preview turn attempted to read `SKILL.md`.

## Dependency and rollout

Depends on SerendipityOneInc/zooclaw-engine#991. Deploy the Engine PR first, then this ECAP change.

## Test plan

- [x] `pytest tests/unit/test_pack_test_engine_runtime_service.py tests/unit/test_engine_agent_resource_class.py -q` — 22 passed
- [x] Ruff check and format check on both changed Python files
- [x] Pyright on both changed Python files — 0 errors
- [x] pre-commit changed-file checks, import contracts, and PR size gate
- [ ] Repository-wide `bash scripts/verify-py.sh` is blocked by existing unrelated main-branch baseline issues: 72 Ruff findings, 20 files requiring formatting, and 4 route-helper Pyright errors; all 8 import-linter contracts pass

```

