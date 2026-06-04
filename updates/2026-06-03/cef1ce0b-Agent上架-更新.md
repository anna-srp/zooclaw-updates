---
title: "ZooCaptain 新增中央客服支持包"
type: "Agent 上架/更新"
priority: "高"
date: "2026-06-03"
status: "待审核"
channels: "站内弹窗, 社媒素材, Use Case, Discord, changelog, KOL"
---
# ZooCaptain 新增中央客服支持包

## 核心宣传点

ZooCaptain 内置客服支持包，遇到问题可以直接联系支持，响应更及时。

## 原始内容

**Repo:** SerendipityOneInc/ecap-agent-pack  
**SHA:** `cef1ce0b26aeb6b054d86caeeae712a5e94f061c`  
**作者:** vincent-srp  
**日期:** 2026-06-03T03:36:18Z  
**URL:** https://github.com/SerendipityOneInc/ecap-agent-pack/commit/cef1ce0b26aeb6b054d86caeeae712a5e94f061c

### Commit Message

```
feat(zoo-captain): add central customer-support pack (#156)

* feat(zoo-captain): add central customer-support pack

zoo-captain (Captain) is a central, multi-customer support agent for
OpenClaw/ZooClaw: answers grounded in verified sources (无据不答), isolates
DMs via runtime session.dmScope=per-channel-peer, and escalates to
support@zooclaw.ai only after customer confirmation.

Includes 8 skills under .agents/skills, root + skill scripts, a single
knowledge source registry (data/sources.yaml) feeding data/knowledge
(6 sources + INDEX/CHANGELOG), and a deterministic deploy bootstrap
(set_runtime_config + optional seed_config; verify_deploy hard-fails on an
unverifiable dmScope when --openclaw-config is explicit). pytest: 56 passing.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* feat(zoo-captain): add optional daily knowledge-refresh ops cron to BOOTSTRAP

Schedule a non-delivering (--no-deliver) isolated OpenClaw cron that runs
sync-knowledge daily. It uses the agent's own agent_id (from the identity seed)
and needs no peer_id, so it is feasible for central support — unlike a delivering
cron. Kept optional/non-blocking, with a quality note that an unattended fetch can
silently pollute the baseline.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* docs(zoo-captain): use full script paths in skill-private docstrings

fetch_source / run_diagnosis / collect_signals / update_tips / finalize_review
showed `scripts/<name>.py` in their own docstring Usage examples, but they live
under .agents/skills/<skill>/scripts/ and run with cwd=workspace-root. The
examples now use the full path, matching the SKILL.md commands. Docstring-only —
no behavior change.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: vincent-srp <180138700+vincent-srp@users.noreply.github.com>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What
Add **zoo-captain** (Captain) — a central, multi-customer support agent for OpenClaw/ZooClaw — as a top-level pack (packaged/runtime layout: root identity + `.agents/skills/`, consistent with repo convention).

## Highlights
- **Grounded answers (无据不答)**: every platform answer needs a source URL or an explicit uncertainty statement; never fabricates.
- **Multi-customer isolation**: runtime `session.dmScope = per-channel-peer` (set at deploy, top-level `session` key — not `agents.defaults.session`); per-customer notes in `customers/<key>.md` outside the memory tree, never cross-leaking.
- **Confirm-before-send escalation** to support@zooclaw.ai.
- **Single knowledge registry**: `data/sources.yaml` → `data/knowledge/` (6 sources + INDEX + CHANGELOG), refreshed by `sync-knowledge`; `search-knowledge` works a 5-layer evidence chain.
- **Deterministic deploy bootstrap**: `set_runtime_config.py` (idempotent, path-resolved, merge-safe) + optional ops `seed_config.py` identity; `verify_deploy.py` **hard-fails on an unverifiable dmScope when `--openclaw-config` is explicit** (no false-green skip).
- 8 skills under `.agents/skills/`, root + skill scripts, **pytest: 56 passing**.

## Notes
- Runtime files (`data/config.json`, caches) are gitignored.
- Identity seed is an optional ops step (does not block deploy completion); customer Q&A works without it.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
