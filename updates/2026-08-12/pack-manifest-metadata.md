---
title: "Agent 详情页展示技能说明、支持语言与版本更新日志"
type: "产品基础功能更新"
priority: "中"
date: "2026-08-12"
status: "待审核"
channels: ""
---

# Agent 详情页展示技能说明、支持语言与版本更新日志

## 核心宣传点

Agent（Pack）公开页现在会列出它包含哪些技能、各自能做什么、支持哪些语言，并展示每个版本的更新说明，挑选 Agent 时一眼看清能力边界。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `200f50fd88a5335185971c7d21b2a9f88461bba1`
- PR: #3347

### Commit Message

```
feat(agent-packs): store manifest metadata (#3347)

## Linear


https://linear.app/srpone/issue/ECA-1373/store-agent-pack-manifest-metadata

## Summary

- parse `skill_details`, `supported_languages`, and `release_notes` from
the exact submitted `agent-pack.yaml` archive
- persist the metadata on Pack Test runs, submissions, and published
Packs without adding collections or tables
- project the fields through official, private, shared-link,
marketplace, and version APIs
- render skill descriptions, supported languages, and version release
notes on the public Pack page
- update Enterprise Admin and Dashboard archive parsing while keeping
Agent Studio validation authoritative
- require release notes for update workspaces in Agent Studio
validation; backend submission only stores normalized metadata and does
not duplicate that blocking gate

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] backend targeted suite: 215 passed
- [x] Web targeted suite: 57 passed
- [x] Dashboard archive suite: 28 passed
- [x] submission service suite after validation-boundary adjustment: 34
passed
- [x] Dashboard typecheck and lint
- [x] Agent Pack archive package lint

## Related PR

- Agent Studio V1/V2 manifest authoring and validation:
https://github.com/SerendipityOneInc/ecap-agent-pack/pull/239
```

### PR Body

## Linear

https://linear.app/srpone/issue/ECA-1373/store-agent-pack-manifest-metadata

## Summary

- parse `skill_details`, `supported_languages`, and `release_notes` from the exact submitted `agent-pack.yaml` archive
- persist the metadata on Pack Test runs, submissions, and published Packs without adding collections or tables
- project the fields through official, private, shared-link, marketplace, and version APIs
- render skill descriptions, supported languages, and version release notes on the public Pack page
- update Enterprise Admin and Dashboard archive parsing while keeping Agent Studio validation authoritative
- require release notes for update workspaces in Agent Studio validation; backend submission only stores normalized metadata and does not duplicate that blocking gate

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] backend targeted suite: 215 passed
- [x] Web targeted suite: 57 passed
- [x] Dashboard archive suite: 28 passed
- [x] submission service suite after validation-boundary adjustment: 34 passed
- [x] Dashboard typecheck and lint
- [x] Agent Pack archive package lint

## Related PR

- Agent Studio V1/V2 manifest authoring and validation: https://github.com/SerendipityOneInc/ecap-agent-pack/pull/239


---
