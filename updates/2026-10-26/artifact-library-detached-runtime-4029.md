---
title: "修复：有 Agent 运行时脱离后，全局产物库整页打不开"
type: "Bug Fix"
priority: "中"
date: "2026-10-26"
status: "待审核"
channels: ""
---

# 修复：有 Agent 运行时脱离后，全局产物库整页打不开

## 核心宣传点

只要账号下有一个已保存的 Agent 其引擎运行时处于脱离状态，全局 Artifact 库整页就会返回 409，连其他健康 Agent 的产物也一并看不到。现在全局汇总时只跳过 `agent.runtime_detached` 这一类来源，其余 Agent 的产物照常展示；如果你明确选中那个出问题的 Agent，仍会如实报出冲突，其他冲突和依赖失败也依旧会抛出，不会被静默吞掉。本次不改动任何工作区记录，也不涉及工作区文件和产物解析器的跨域配置。

验证时在 staging 上复现了 409，改动后的本地后端返回 200 并正常渲染出三个已有产物。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `eaefa002951b6b8e0d3d285686f1e7e5521d2c6b`
- PR: #4029
- 作者：kaka-srp
- 日期：2026-10-26T03:02:02Z

### Commit Message

```
fix(artifacts): isolate detached runtimes in global library (#4029)

The global Artifact Library returned 409 for the whole page when one
persisted Agent had a detached Engine runtime. Skip only
`agent.runtime_detached` sources during the global aggregation so
artifacts from healthy Agents remain available. Explicit Agent selection
preserves the conflict; other conflicts and dependency failures still
propagate. No workspace records are changed.

This fixes an existing issue independently of V1 retirement PR #4028. It
does not change Workspace Files or artifact-resolver CORS configuration.

Validation: 22 related tests passed; scoped Ruff/format/Pyright and
pre-commit review passed. Local FastAPI used the tasks.json staging
dependencies and encrypted Mongo client without mocked HTTP: deployed
staging returned 409, modified local backend returned 200 with three
existing artifacts, and local `/assets` rendered all three after the
cold-compile request was retried. Browser credentials were cleared and
the original account locale was restored independently.

Evidence: [validation
report](docs/validation/2026-10-08-artifact-library-detached.md). All
required CI checks passed. Claude and Codex reviews returned APPROVE
with no actionable correctness findings. Remains a draft for owner
review; do not merge or release automatically.

Review adjudication: retain the existing missing-Engine-agent log
because the targeted detached-runtime condition is the client mapping of
an Engine 404, not a transport disconnection. The suggested
boolean-expression comment is stylistic; the scope/code matrix is
directly covered by tests. No extra refactor is included.
```
