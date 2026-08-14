---
title: "Agent Builder：可从现有 Agent 一键复制创建，测试对话支持传附件"
type: "新功能上线"
priority: "高"
date: "2026-08-13"
status: "待审核"
channels: ""
---

## 核心宣传点

创建 Agent 时可以直接「基于一个现有 Agent 开始」，省去从零配置；在 Test Agent 里还能上传附件来试对话效果，调试更贴近真实使用。

## 原始内容

仓库：SerendipityOneInc/ecap-workspace
commit：61cb471047acd03427c7feb38862e7ade72e1534
作者：kaka-srp
日期：2026-08-13T10:48:54Z

**Commit message**

```
feat(agent-builder): restore v2 fork and test attachments (#3370)

## Linear

N/A

## Summary

- restore the V2-only “Start from an existing agent” flow in the Create
Agent dialog, using every current-user-accessible Pack as an eligible
starting point
- filter and revalidate sources against immutable Engine runtime assets,
pin the complete asset identity on the Project, and preserve production
V2 Pack root files during import
- add attachment upload to the V2 Test Agent composer, including
attachment-only turns and feedback handling

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh <affected Agent Builder and Pack
service paths>`
- [x] targeted backend tests: 37 passed
- [x] targeted frontend tests: 157 passed
- [x] `bash scripts/verify-changed.sh`
- [x] pre-commit and pre-push hooks
```

**PR #3370 body**

## Linear

N/A

## Summary

- restore the V2-only “Start from an existing agent” flow in the Create Agent dialog, using every current-user-accessible Pack as an eligible starting point
- filter and revalidate sources against immutable Engine runtime assets, pin the complete asset identity on the Project, and preserve production V2 Pack root files during import
- add attachment upload to the V2 Test Agent composer, including attachment-only turns and feedback handling

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh <affected Agent Builder and Pack service paths>`
- [x] targeted backend tests: 37 passed
- [x] targeted frontend tests: 157 passed
- [x] `bash scripts/verify-changed.sh`
- [x] pre-commit and pre-push hooks


