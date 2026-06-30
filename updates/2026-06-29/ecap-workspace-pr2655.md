---
title: "应用市场支持付费 Agent 包上架"
type: "新功能上线"
priority: "中"
date: "2026-06-29"
status: "待审核"
channels: ""
---

# 应用市场支持付费 Agent 包上架

## 核心宣传点

现在 Agent 应用市场支持上架付费 Agent 包：创作者可提交带定价的付费包，经审核后绑定价格上架，让优质 Agent 能直接变现、用户也能买到更专业的付费 Agent。

## 原始内容

### Commit Message

```
feat(claw-interface): add paid agent pack listing (#2655)

## Summary

- Add paid agent-pack listing metadata, price rows, origin lookup, and
indexes.
- Add user-triggered paid listing submission that copies the source pack
submission asset into the ZooClaw org.
- Keep paid listing creation retryable by writing the paid pack as draft
first, then submission, then price, and finally moving the pack to
listing review.
- Extend review approval to bind the approved price to the paid pack.

## Validation

- `/Users/bill/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_paid_listing_service.py -q`
- `/opt/homebrew/bin/ruff check
services/claw-interface/app/services/pack_store/paid_listing_service.py
services/claw-interface/tests/unit/test_paid_listing_service.py`
- `/opt/homebrew/bin/ruff format --check
services/claw-interface/app/services/pack_store/paid_listing_service.py
services/claw-interface/tests/unit/test_paid_listing_service.py`
- `/Users/bill/.venvs/claw-interface/bin/lint-imports`
- `git diff --check`

## Notes

- `bash scripts/verify-changed.sh` returned 3 locally because the script
could not find the backend pyright/import-linter toolchain on PATH and
skipped the py gate.
- Direct import-linter passed via the existing venv. Direct pyright was
not usable in this local shell because it could not resolve broad
project dependencies such as fastapi, pytest, and favie_common.
```

### PR Description

## Summary

- Add paid agent-pack listing metadata, price rows, origin lookup, and indexes.
- Add user-triggered paid listing submission that copies the source pack submission asset into the ZooClaw org.
- Keep paid listing creation retryable by writing the paid pack as draft first, then submission, then price, and finally moving the pack to listing review.
- Extend review approval to bind the approved price to the paid pack.

## Validation

- `/Users/bill/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_paid_listing_service.py -q`
- `/opt/homebrew/bin/ruff check services/claw-interface/app/services/pack_store/paid_listing_service.py services/claw-interface/tests/unit/test_paid_listing_service.py`
- `/opt/homebrew/bin/ruff format --check services/claw-interface/app/services/pack_store/paid_listing_service.py services/claw-interface/tests/unit/test_paid_listing_service.py`
- `/Users/bill/.venvs/claw-interface/bin/lint-imports`
- `git diff --check`

## Notes

- `bash scripts/verify-changed.sh` returned 3 locally because the script could not find the backend pyright/import-linter toolchain on PATH and skipped the py gate.
- Direct import-linter passed via the existing venv. Direct pyright was not usable in this local shell because it could not resolve broad project dependencies such as fastapi, pytest, and favie_common.

