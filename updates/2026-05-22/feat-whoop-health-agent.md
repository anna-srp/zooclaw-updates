---
title: "新 Agent 上架：WHOOP 健康教练 Agent，实时分析你的运动恢复与压力状态"
type: "Agent 上架/更新"
priority: "高"
date: "2026-05-22"
status: "待审核"
channels: ""
---

# 新 Agent 上架：WHOOP 健康教练 Agent，实时分析你的运动恢复与压力状态

## 核心宣传点

全新 WHOOP 健康教练 Agent 上线！连接你的 WHOOP 运动手环，自动分析恢复评分、运动负荷和睡眠质量，给出个性化健康建议，帮你科学安排训练和休息。

## 原始内容

**Commit**: 548ae7689882d068d65377748278db5fe50627b3
**Author**: Nemo Feng
**Date**: 2026-05-22T03:11:36Z
**PR**: #140

### Commit Message
```
feat(whoop-health-agent): add WHOOP recovery & strain coaching pack (#140)

Introduces Rally, a WHOOP-connected performance and recovery agent with
OAuth2 onboarding, a v2 API data layer, an HTML dashboard, and morning /
midday / evening briefing automations plus proactive change detection.

Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>
```

### PR Description
## Summary
- New agent pack **Rally** (`whoop-health-agent/`) — a WHOOP-connected personal performance and recovery coach.
- Skills: `whoop-connect` (OAuth2 authorize-URL → paste-back redirect → token exchange with rotating refresh tokens), `whoop-data` (unified v2 API client, cache, dashboard builder, change detector, briefings), and `pack-onboarding` (first-session provisioning).
- Automations: morning recovery briefing (07:00), midday strain check (13:00), evening recap (21:00), silent pre-morning data refresh (06:45), and a proactive-poll every 30 min during waking hours.

## Test plan
- [ ] Load the pack into a bot pod and run first-time onboarding end-to-end against a real WHOOP developer app
- [ ] Verify OAuth code exchange and refresh-token rotation persist correctly to `~/.config/whoop/auth.json`
- [ ] Fetch cycle / recovery / sleep / workout data and confirm the HTML dashboard renders
- [ ] Trigger each of the five cron automations manually and confirm delivery (silent job stays silent)
- [ ] Confirm proactive-poll only sends when `detect_changes.py` reports `should_notify: true`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

