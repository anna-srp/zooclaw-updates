---
title: "Agent Studio 升级至 v1.2.0：onboarding 脚本全面强化"
type: "Agent 上架/更新"
priority: "中"
date: "2026-05-13"
status: "待审核"
channels: "站内弹窗 + Use Case + Discord + changelog + EDM"
---

# Agent Studio 升级至 v1.2.0：onboarding 脚本全面强化

## 核心宣传点

Agent Studio 迎来 v1.2.0 重要更新：onboarding 流程现在能自动准确地配置你的 Agent 个性、记忆和定时任务，不再依赖 AI 临时生成——让每个新建 Agent 从第一天起就运行得更稳更准。

## 原始内容

**来源**: ecap-agent-pack PR #120 | SHA: d38d7430

**Commit Message**:
```
feat(agent-studio): v1.2.0 — close 20 PR #118 follow-ups (onboarding scripts,
package hardening, validate/scaffold alignment, clean.py rewrite) (#120)

Onboarding scripts — real implementations replace stubs / LLM string-edits:
- OB-1: provision.py now mechanically substitutes {{key}} / {{config.key}}
  placeholders in SOUL.md and IDENTITY.md; exits 1 on unresolved placeholders;
  skips in /test mode.
- OB-2: finalize.py reads config + data/*_baseline.json, writes MEMORY.md +
  data/plan.json; corrupt baselines surfaced in corrupt_baselines output field.
- OB-3: new add_cron.py mechanically resolves {{config.*}} in cron templates;
  exits 1 on missing/empty keys and missing required delivery fields — closes
  the silent-misdelivery hole.

Package.py hardening:
- PK-1: Replaced rglob with strict _AGENT_PACKABLE allow-list so runtime residue
  (MEMORY.md, USER.md, memory/, helper scripts) no longer leaks into the archive.
- PK-2: _clean_agent_file takes has_avatar: bool; removed the working-tree side effect.
```

**PR #120 Description**:
```
Agent Studio v1.1.0 → v1.2.0. Closes 20 follow-ups from the post-PR-#118 backlog:
all High items minus the cross-service ones needing OpenClaw backend, plus Medium and Low items.

Key improvements:
- provision.py mechanically substitutes placeholders in SOUL.md/IDENTITY.md;
  exits 1 on unresolved placeholders; skips in /test mode.
- finalize.py reads config + baseline JSONs, writes MEMORY.md + data/plan.json.
- new add_cron.py mechanically resolves {{config.*}} in cron templates;
  exits 1 on missing/empty keys — closes the silent-misdelivery hole.
- package.py: strict allow-list prevents runtime residue from leaking into archives.
- check_crossrefs accepts both skills/<n>/... and .agents/skills/<n>/... reference forms.
- agent/SOUL.md now required by structure check.
- scaffold.py emits cli_dependencies: [] and data_sources: [] sections.
```
