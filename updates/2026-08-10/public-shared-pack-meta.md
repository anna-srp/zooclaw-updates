---
title: "Agent 分享页展示作者、版本与快捷指令"
type: "体验优化"
priority: "中"
date: "2026-08-10"
status: "待审核"
channels: ""
---

# Agent 分享页展示作者、版本与快捷指令

## 核心宣传点

通过分享链接查看 Agent 时，现在能直接看到作者名、当前版本、发布时间和可用的快捷指令，不用装上才知道它能干什么。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `6b563417097c5459db314274c9733f35474968a5`
- PR: #3319

### Commit Message

```
feat(pack): expose public shared pack metadata (#3319)

## Linear

N/A

## Summary

- expose author name, current version, publication timestamp, and quick
commands from the anonymous shared-pack response
- keep the public payload allowlisted while preserving protected asset,
owner-id, organization, and billing fields
- preserve shared-pack version metadata and quick commands when mapping
the response into frontend agent detail state

## Test plan

- [x] `pytest -q tests/unit/test_shared_listing_service.py
tests/unit/test_public_agent_packs_routes.py
tests/unit/test_schema_pack.py
tests/unit/test_pack_schema_default_model.py` (69 passed)
- [x] backend Ruff check and format check
- [x] backend Pyright over `app/ tests/` (0 errors)
- [x] backend import-linter contracts
- [x] `bash scripts/verify-web.sh` for changed frontend files
(TypeScript, 38 related tests, ESLint)
```

### PR Body

## Linear

N/A

## Summary

- expose author name, current version, publication timestamp, and quick commands from the anonymous shared-pack response
- keep the public payload allowlisted while preserving protected asset, owner-id, organization, and billing fields
- preserve shared-pack version metadata and quick commands when mapping the response into frontend agent detail state

## Test plan

- [x] `pytest -q tests/unit/test_shared_listing_service.py tests/unit/test_public_agent_packs_routes.py tests/unit/test_schema_pack.py tests/unit/test_pack_schema_default_model.py` (69 passed)
- [x] backend Ruff check and format check
- [x] backend Pyright over `app/ tests/` (0 errors)
- [x] backend import-linter contracts
- [x] `bash scripts/verify-web.sh` for changed frontend files (TypeScript, 38 related tests, ESLint)

