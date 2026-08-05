---
title: "Agent 市场「My Custom Specialists」入口恢复"
type: "Bug Fix"
priority: "中"
date: "2026-08-04"
status: "待审核"
channels: ""
commit: "922928f19ede5ab98131f6ce4178254c12aaa974"
repo: "SerendipityOneInc/ecap-workspace"
---

## 核心宣传点

Agent Marketplace 页面标题旁的「My Custom Specialists」入口回来了，点击可直达 /agents-manager/publish 管理自己发布的专家。

## 原始内容

```
fix(web): restore custom specialists marketplace entry (#3219)

## Linear

N/A — no Linear issue was provided.

## Summary

- restore the `My Custom Specialists` entry beside the Agent Marketplace
subtitle
- link the entry to `/agents-manager/publish` and hide it while
authentication is loading
- update unit coverage for the restored entry and loading state

## Test plan

- [x] `bash scripts/verify-web.sh
'src/app/[locale]/(app)/(chat)/agents-manager/AgentsManagerClient.tsx'
tests/unit/app/agents-manager-client.unit.spec.tsx
tests/unit/app/agents-manager/AgentsManagerClient.unit.spec.tsx`
- [x] verify the Marketplace in the local `ready-user` mock session and
confirm the entry appears once

---

### PR Body

## Linear

N/A — no Linear issue was provided.

## Summary

- restore the `My Custom Specialists` entry beside the Agent Marketplace subtitle
- link the entry to `/agents-manager/publish` and hide it while authentication is loading
- update unit coverage for the restored entry and loading state

## Test plan

- [x] `bash scripts/verify-web.sh 'src/app/[locale]/(app)/(chat)/agents-manager/AgentsManagerClient.tsx' tests/unit/app/agents-manager-client.unit.spec.tsx tests/unit/app/agents-manager/AgentsManagerClient.unit.spec.tsx`
- [x] verify the Marketplace in the local `ready-user` mock session and confirm the entry appears once

```
