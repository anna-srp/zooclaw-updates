---
title: "fix(agent-development): expose skill authoring guidance and receipts (#3747)"
type: "产品基础功能更新"
priority: "低"
date: "2026-09-16"
status: "待审核"
channels: ""
---

# fix(agent-development): expose skill authoring guidance and receipts (#3747)

## 核心宣传点

Agent Builder 现在会明确暴露 Skill 的源码目录结构和一个可直接用的纯指令模板，并在校验后回传实际产物变更与已注册的 skill 版本，避免把可复用能力只写进 AGENTS.md 而没有真正生成 Skill。

## PR 说明

## Summary

Build could save a reusable capability entirely in AGENTS.md without creating an Engine skill. Expose the skill source layout and a valid instruction-only template even when the source has no skills, then return effective artifact changes from validate and registered skill versions from commit.

## Root cause

The existing registration path works, but the authoring contract did not explain which artifact to create or provide registration feedback. This change keeps that existing path and adds guidance and content-free receipts. Persona-only changes remain valid with zero skills; no existing Agent source is migrated.

The companion Engine PR https://github.com/SerendipityOneInc/zooclaw-engine/pull/1468 updates the Build policy and tool descriptions. Deploy claw-interface first, then Engine. The detailed design and reproducible real-model check are in docs/superpowers/specs/2026-09-16-build-skill-artifacts-design.md.

## Test plan

- [x] Backend static checks: ruff, formatting, pyright, import-linter.
- [x] Agent Development regression suite: 331 passed, including 7 cases added after independent agent review for immutable post-commit reads, exact skill identity/version and cleanup failure handling.
- [x] Independent agent review: three harness findings fixed and re-reviewed; no remaining findings. Real-model scenarios rerun successfully with the stricter assertions.
- [x] Real gpt-5.6-terra source-contract check using the exported Engine policy: created skill v1, retained skills for a tone change, and upgraded the same capability to v2 with a script. Actual local Engine registry and eligible bindings were checked; test resources were cleaned up.
- [ ] Full ordinary-task worker/Temporal/sandbox skill-read path: not covered by this source-contract harness. Revision/ChangeSet persistence is in-memory in the harness; no production deployment or source repair was performed.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `411a656a81b0c1e3341442d22115f799f9a3be47`
- PR: #3747
- 作者：kaka-srp
- 日期：2026-09-16T06:22:51Z

### Commit Message

```
fix(agent-development): expose skill authoring guidance and receipts (#3747)

## Summary

Build could save a reusable capability entirely in AGENTS.md without
creating an Engine skill. Expose the skill source layout and a valid
instruction-only template even when the source has no skills, then
return effective artifact changes from validate and registered skill
versions from commit.

## Root cause

The existing registration path works, but the authoring contract did not
explain which artifact to
```
