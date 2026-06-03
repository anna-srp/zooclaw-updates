---
title: "[平台] add time-grouped usage records"
type: "Bug Fix"
priority: "中"
date: "2026-06-02"
status: "待审核"
channels: ""
---
# [平台] add time-grouped usage records

## 核心宣传点
来自 ecap-workspace 仓库的更新：feat(billing): add time-grouped usage records

## 原始内容
**Commit**: bc0f659dcd41681ab26bd590b54df9c0b16cab9d
**Title**: feat(billing): add time-grouped usage records (#2151)
**Author**: kaka-srp
**Date**: 2026-06-02T09:43:24Z

**PR**: #2151

### Commit Message
```
feat(billing): add time-grouped usage records (#2151)

## Linear
https://linear.app/srpone/issue/ECA-873/usage-records

## Summary
- Add authenticated LLM credits usage record aggregation from Billing
Gateway events.
- Add Next BFF proxy and account usage UI with range switcher, summary
cards, credits chart, top models, and detail table.
- Keep token details and credits conversion metadata out of the
user-facing API and UI.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web/app run test:unit
tests/unit/app/api/user-usage-records.unit.spec.ts
tests/unit/components/billing/UsageRecord.unit.spec.tsx
tests/unit/hooks/queries/keys.unit.spec.ts
tests/unit/lib/api/user.unit.spec.ts
- [x] pnpm --dir web/app run test:unit
tests/unit/lint/react-hooks-config.unit.spec.ts --testTimeout=30000
- [x] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff check .
- [x] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pyright app tests
- [x] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_billing_usage_records.py tests/unit/test_user_credits.py
-q
- [ ] pnpm --dir web run tsc (local workspace script fails before
typechecking with `ERROR Unknown option: if-present`; app-level `tsc
--noEmit` passed)
- [ ] pnpm --dir web run test:unit (local full run: 6740/6741 tests
passed; existing `tests/unit/lint/react-hooks-config.unit.spec.ts` hit
default 10s timeout; isolated run passes with higher timeout)
- [ ] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest --cov=app
--cov-report=term-missing --cov-fail-under=90 -q (local full run failed
in unrelated openclaw_agents/org_invite tests and repo total coverage
was 88.51%; usage focused tests pass)
```

### PR Description
## Linear
https://linear.app/srpone/issue/ECA-873/usage-records

## Summary
- Add authenticated LLM credits usage record aggregation from Billing Gateway events.
- Add Next BFF proxy and account usage UI with range switcher, summary cards, credits chart, top models, and detail table.
- Keep token details and credits conversion metadata out of the user-facing API and UI.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web/app run test:unit tests/unit/app/api/user-usage-records.unit.spec.ts tests/unit/components/billing/UsageRecord.unit.spec.tsx tests/unit/hooks/queries/keys.unit.spec.ts tests/unit/lib/api/user.unit.spec.ts
- [x] pnpm --dir web/app run test:unit tests/unit/lint/react-hooks-config.unit.spec.ts --testTimeout=30000
- [x] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff check .
- [x] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pyright app tests
- [x] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_billing_usage_records.py tests/unit/test_user_credits.py -q
- [ ] pnpm --dir web run tsc (local workspace script fails before typechecking with `ERROR Unknown option: if-present`; app-level `tsc --noEmit` passed)
- [ ] pnpm --dir web run test:unit (local full run: 6740/6741 tests passed; existing `tests/unit/lint/react-hooks-config.unit.spec.ts` hit default 10s timeout; isolated run passes with higher timeout)
- [ ] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q (local full run failed in unrelated openclaw_agents/org_invite tests and repo total coverage was 88.51%; usage focused tests pass)


