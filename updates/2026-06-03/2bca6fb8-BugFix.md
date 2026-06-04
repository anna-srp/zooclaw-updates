---
title: "降低 claw-interface 探针重启频率"
type: "Bug Fix"
priority: "中"
date: "2026-06-03"
status: "待审核"
channels: "Discord, changelog"
---
# 降低 claw-interface 探针重启频率

## 核心宣传点

降低内部探针重启频率，系统更稳定。

## 原始内容

**Repo:** SerendipityOneInc/ecap-workspace  
**SHA:** `2bca6fb882e09e91c999e43dac71fdbd576e8038`  
**作者:** kaka-srp  
**日期:** 2026-06-03T07:28:42Z  
**URL:** https://github.com/SerendipityOneInc/ecap-workspace/commit/2bca6fb882e09e91c999e43dac71fdbd576e8038

### Commit Message

```
fix: reduce claw-interface probe restarts (#2159)

## Summary
- remove uvicorn --reload from the claw-interface container entrypoint
- increase liveness/readiness probe timeout from 1s to 5s while keeping
the existing / probe path

## Tests
- .venv/bin/pytest tests/unit/test_status.py
- .venv/bin/python -m ruff check app/routes/status.py
tests/unit/test_status.py
- kubectl kustomize kustomize/overlays/production
- git diff --check -- services/claw-interface/Dockerfile
services/claw-interface/kustomize/base/deployment.yaml

Note: full .venv/bin/pytest --cov=app --cov-report=term-missing -q was
started and then stopped at user request.
```

### PR Description

## Summary
- remove uvicorn --reload from the claw-interface container entrypoint
- increase liveness/readiness probe timeout from 1s to 5s while keeping the existing / probe path

## Tests
- .venv/bin/pytest tests/unit/test_status.py
- .venv/bin/python -m ruff check app/routes/status.py tests/unit/test_status.py
- kubectl kustomize kustomize/overlays/production
- git diff --check -- services/claw-interface/Dockerfile services/claw-interface/kustomize/base/deployment.yaml

Note: full .venv/bin/pytest --cov=app --cov-report=term-missing -q was started and then stopped at user request.
