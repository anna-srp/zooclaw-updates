---
title: "套餐内 Agent 现可显示快捷启动卡片"
type: "体验优化"
priority: "中"
date: "2026-06-25"
status: "待审核"
channels: ""
---

# 套餐内 Agent 现可显示快捷启动卡片

## 核心宣传点

购买的垂直套餐里包含的 Agent，现在也会在「新任务」里显示快捷启动卡片，不用再手动摸索就能一键发起任务。

## 原始内容

### Commit Message

```
fix(vertical-pack): expose package quick commands (#2605)

## Summary
- Return purchased vertical package agent pack metadata from `GET
/vertical-pack/package/current`.
- Merge current vertical package packs into New Task quick-command
lookup so hidden package agents can show Quick Start cards.
- Cover backend current-package pack details and frontend hidden
vertical-pack quick commands with focused tests.

## Root cause
Vertical package installation used package pack IDs, but New Task quick
commands only read the public `/agent-packs` catalog. Packs hidden from
the public market were installable through vertical packages but
unavailable to the New Task metadata lookup, so their `quick_commands`
were not rendered.

## Test plan
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_vertical_pack_plans_routes.py
services/claw-interface/tests/unit/test_schema_vertical_pack_package.py
-q`
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh
'web/app/src/app/[locale]/(app)/new-chat/useViewModel.ts'
web/app/src/hooks/useVerticalPackPackageInstaller.ts
web/app/src/services/vertical-pack-package.ts
web/app/tests/unit/app/new-chat/NewChatClient.unit.spec.tsx
web/app/tests/unit/app/new-chat/useViewModel.unit.spec.tsx
web/app/tests/unit/services/vertical-pack-package.unit.spec.ts`
```

### PR Description

## Summary
- Return purchased vertical package agent pack metadata from `GET /vertical-pack/package/current`.
- Merge current vertical package packs into New Task quick-command lookup so hidden package agents can show Quick Start cards.
- Cover backend current-package pack details and frontend hidden vertical-pack quick commands with focused tests.

## Root cause
Vertical package installation used package pack IDs, but New Task quick commands only read the public `/agent-packs` catalog. Packs hidden from the public market were installable through vertical packages but unavailable to the New Task metadata lookup, so their `quick_commands` were not rendered.

## Test plan
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_vertical_pack_plans_routes.py services/claw-interface/tests/unit/test_schema_vertical_pack_package.py -q`
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/new-chat/useViewModel.ts' web/app/src/hooks/useVerticalPackPackageInstaller.ts web/app/src/services/vertical-pack-package.ts web/app/tests/unit/app/new-chat/NewChatClient.unit.spec.tsx web/app/tests/unit/app/new-chat/useViewModel.unit.spec.tsx web/app/tests/unit/services/vertical-pack-package.unit.spec.ts`

