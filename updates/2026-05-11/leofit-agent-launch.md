---
title: "新 Agent 上架：Leo 健身教练 🦁（leofit v4.2.1）"
type: "Agent 上架/更新"
priority: "高"
date: "2026-05-11"
status: "待审核"
channels: ""
---

# 新 Agent 上架：Leo 健身教练 🦁（leofit v4.2.1）

## 核心宣传点

全新 AI 健身教练 Leo 正式上线，提供个性化训练计划、营养建议、运动记录、进度追踪等 11 项专属功能，拥有 123 个运动动作库。

## 原始内容

Commit message:
feat(leofit): add leofit 4.2.1 agent pack (#119)

* feat(leofit): add leofit 4.2.1 agent pack

AI fitness coach with 11 skills covering profile setup, weekly planner,
workout logger, 123-exercise library with muscle maps, nutrition tracking,
progress analytics, smart reminders, and AI coaching.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(leofit): remove ReDoS-prone alternation in muscle-map regex

`[^>]` already matches `\n`, so the `(?:[^>]|\n)*?` alternation was
redundant and caused catastrophic backtracking on inputs starting with
`<path` followed by many newlines. Replace with `[^>]*` — same matches,
linear time.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: vincent-srp <180138700+vincent-srp@users.noreply.github.com>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

PR Description:
## Summary
- New `leofit/` agent pack — AI fitness coach (Leo 🦁), v4.2.1, unpacked from `build/leofit-v4-20260507-0706.tar.gz`.
- 11 skills: fitpack-init, CARD-STYLE, LANGUAGE, fit-profile, fit-planner, fit-logger, fit-exercises, fit-nutrition, fit-progress, fit-remind, fit-coach.
- Bundled data: 123-exercise library, muscle-activation maps (PNG + SVG), foods database.

## Test plan
- [ ] `agent-pack.yaml` parses; all 11 declared skills resolve to existing `skills/<name>/SKILL.md`.
- [ ] No sensitive files staged (no `.env`, keys, or credentials).
- [ ] Install dry-run: `openclaw install leofit` from this branch.
- [ ] Smoke check `fitpack-init` onboarding flow end-to-end.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
