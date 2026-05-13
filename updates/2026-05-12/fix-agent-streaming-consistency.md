---
title: "统一主 Bot 与自定义 Agent 的消息输出节奏"
type: "产品基础功能更新"
priority: "低"
date: "2026-05-12"
status: "待审核"
channels: ""
---

# 统一主 Bot 与自定义 Agent 的消息输出节奏

## 核心宣传点

修复了主 Bot 和自定义 Agent 的消息流速不一致问题，现在所有 Agent 的回复节奏更加统一流畅。

## 原始内容

**Commit:** `2026-05-12T07:46:33Z` by sam-srp
**SHA:** 164e6660e9be2d60722d27d89aa1038cf4f64d19
**PR:** #1598

### Commit Message

```
refactor(claw-interface): drop divergent blockStreaming MM channel config (#1598)

## Summary
- `build_mm_channel_config` (default bot init, account_id=\"default\")
and `inject_fastclaw_channel` (per-agent install, Phase 7 of
`deploy_selected_agents`) were writing **different** blockStreaming /
Coalesce / Chunk parameters:
- Default channel: `blockStreaming=true` + `Coalesce={minChars:800,
idleMs:500}`
- Per-agent channel: `blockStreaming=true` + `Coalesce={minChars:800,
maxChars:1200, idleMs:1000}` + `Chunk={minChars:150, maxChars:1000}`
- The drift meant main bot streamed visibly faster than hired agents
(500ms vs 1000ms idle window, different chunk sizing), and the
\`default\` channel didn't even have the `maxChars`/`Chunk` knobs the
per-agent path had.
- Cleanest fix: drop the whole block-streaming knob from both paths and
let OpenClaw stream tokens to Mattermost with its default behavior.
Restores a single, consistent cadence across main and per-agent
channels.

## Test plan
- [x] `pyright` + `ruff` clean (pre-commit)
- [x] `pytest tests/unit -k \"provisioner or mattermost or channel\"` —
124 passed
- [ ] Manual: create a new agent, send a message, verify streaming
cadence in MM DM
- [ ] Manual: confirm main bot streams identically to hired agents

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary
- `build_mm_channel_config` (default bot init, account_id=\"default\") and `inject_fastclaw_channel` (per-agent install, Phase 7 of `deploy_selected_agents`) were writing **different** blockStreaming / Coalesce / Chunk parameters:
  - Default channel: `blockStreaming=true` + `Coalesce={minChars:800, idleMs:500}`
  - Per-agent channel: `blockStreaming=true` + `Coalesce={minChars:800, maxChars:1200, idleMs:1000}` + `Chunk={minChars:150, maxChars:1000}`
- The drift meant main bot streamed visibly faster than hired agents (500ms vs 1000ms idle window, different chunk sizing), and the \`default\` channel didn't even have the `maxChars`/`Chunk` knobs the per-agent path had.
- Cleanest fix: drop the whole block-streaming knob from both paths and let OpenClaw stream tokens to Mattermost with its default behavior. Restores a single, consistent cadence across main and per-agent channels.

## Test plan
- [x] `pyright` + `ruff` clean (pre-commit)
- [x] `pytest tests/unit -k \"provisioner or mattermost or channel\"` — 124 passed
- [ ] Manual: create a new agent, send a message, verify streaming cadence in MM DM
- [ ] Manual: confirm main bot streams identically to hired agents

🤖 Generated with [Claude Code](https://claude.com/claude-code)

