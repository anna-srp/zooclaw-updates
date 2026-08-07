---
title: "修复 Council 讨论档位设置不生效"
type: "Bug Fix"
priority: "中"
date: "2026-08-06"
status: "待审核"
channels: ""
---

## 核心宣传点

Council 发起讨论时选择的档位（tier/深度）之前会在传递中丢失，导致设置不生效，现已修复。

## 原始内容

**fix(council): send dispatch hints on one line (#3280)**

- sha: `1e895a1b52cd2b56389a6cab2e73eb7454c28e09`
- PR: #3280

```
fix(council): send dispatch hints on one line (#3280)

## Summary

- send Council `tier:` and optional `depth:` hints on the same line as
the `/council` command
- keep quoted setting values while avoiding OpenClaw's structural-prefix
stripping of newline-prefixed `tier:` and `depth:` fields
- update the Council skill contract and message assertions for the
single-line format

## Root cause

OpenClaw's inbound preprocessing treats a new line beginning with
`name:` as a structural sender prefix. A dispatch such as `/council
topic\ntier: "standard"` therefore reached the Council skill as
`/council topic standard`. Keeping the hints on the command line
preserves their labels without changing the OpenClaw runtime.

## Testing

- `bash scripts/verify-web.sh
web/app/src/hooks/council/useCouncilActions.ts
web/app/tests/unit/hooks/council/useCouncilActions.unit.spec.tsx
web/app/tests/unit/app/council/CouncilClient.unit.spec.tsx
web/app/tests/unit/lib/council/thread-messages.unit.spec.ts`
- `bash scripts/verify-changed.sh`
- 118 targeted Council tests passed
```

**PR Body:**

## Summary

- send Council `tier:` and optional `depth:` hints on the same line as the `/council` command
- keep quoted setting values while avoiding OpenClaw's structural-prefix stripping of newline-prefixed `tier:` and `depth:` fields
- update the Council skill contract and message assertions for the single-line format

## Root cause

OpenClaw's inbound preprocessing treats a new line beginning with `name:` as a structural sender prefix. A dispatch such as `/council topic\ntier: "standard"` therefore reached the Council skill as `/council topic standard`. Keeping the hints on the command line preserves their labels without changing the OpenClaw runtime.

## Testing

- `bash scripts/verify-web.sh web/app/src/hooks/council/useCouncilActions.ts web/app/tests/unit/hooks/council/useCouncilActions.unit.spec.tsx web/app/tests/unit/app/council/CouncilClient.unit.spec.tsx web/app/tests/unit/lib/council/thread-messages.unit.spec.ts`
- `bash scripts/verify-changed.sh`
- 118 targeted Council tests passed

