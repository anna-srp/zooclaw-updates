---
title: "修复 ZooCaptain URL 值导致 JSON 损坏的问题"
type: "Agent 上架/更新"
priority: "高"
date: "2026-06-03"
status: "待审核"
channels: "Discord, changelog"
---
# 修复 ZooCaptain URL 值导致 JSON 损坏的问题

## 核心宣传点

修复 ZooCaptain 在处理特定 URL 时崩溃的问题。

## 原始内容

**Repo:** SerendipityOneInc/ecap-agent-pack  
**SHA:** `c2382ff7e393d1a35b5be938c710366a3316aa3d`  
**作者:** vincent-srp  
**日期:** 2026-06-03T08:00:06Z  
**URL:** https://github.com/SerendipityOneInc/ecap-agent-pack/commit/c2382ff7e393d1a35b5be938c710366a3316aa3d

### Commit Message

```
fix(zoo-captain): don't corrupt JSON with URL values when verifying dmScope (#158)

* fix(zoo-captain): don't corrupt JSON with URL values when verifying dmScope

verify_deploy.py and set_runtime_config.py stripped `//` comments
unconditionally, which ate the `//` inside URL string values (e.g.
"https://docs.openclaw.ai/"), corrupting otherwise-valid JSON and making
dm_scope_per_peer falsely FAIL on a correctly-configured openclaw.json
(BOOTSTRAP Step 4 false fail).

Fix: parse strict JSON first (URL values survive untouched); only a JSON5-ish
config (comments / trailing commas) falls back to a string-aware strip that
keeps `//` inside string literals. Adds regression tests for URL values in both
standard JSON and JSON5-with-comments. pytest: 59 passing.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* feat(zoo-captain): add C-side quick_commands to manifest

Six one-tap shortcuts (how-to / fix-issue / review-usage / explain-concept /
find-agent / build-my-agent), each firing its prompt verbatim as the customer's
message. Kept in sync with the staging catalog (2026-06-03). They map onto the
pack's skills: diagnose-env / insight-review / teach-concept / tour-specialist /
handoff-to-studio.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: vincent-srp <180138700+vincent-srp@users.noreply.github.com>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## Bug
`verify_deploy.py` / `set_runtime_config.py` stripped `//` comments **unconditionally**, so the `//` inside a URL string value (e.g. `"https://docs.openclaw.ai/"`) got eaten → an otherwise-valid `openclaw.json` was corrupted → `dm_scope_per_peer` **falsely FAILs** even when `session.dmScope` is correctly set (BOOTSTRAP Step 4 false fail).

## Fix
Parse **strict JSON first** — a standard config (with URL values) is safe and never touched by the comment rule. Only a JSON5-ish config (comments / trailing commas) falls back to a **string-aware** strip that keeps `//` inside string literals.

## Verify
- Repro: standard JSON with a URL → old strip → `"https:` (unterminated string) → parse fail.
- After: strict-first parse → succeeds. New regression tests cover a URL value in standard JSON **and** in JSON5-with-comments.
- `pytest`: **59 passing**.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
