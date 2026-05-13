---
title: "修复会话标题生成导致的鉴权异常及安全隐患"
type: "Bug Fix"
priority: "中"
date: "2026-05-12"
status: "待审核"
channels: ""
---

# 修复会话标题生成导致的鉴权异常及安全隐患

## 核心宣传点

修复了后台对每条新消息都触发标题生成导致的鉴权错误，并加固了日志文件安全处理，防止敏感 token 意外进入 git 记录。

## 原始内容

**Commit:** `2026-05-12T03:47:35Z` by kaka-srp
**SHA:** 0308d8573e0fb00a73eabe077372856578ebcf63
**PR:** #1596

### Commit Message

```
fix(claw-interface): gate title generation to canvas (ECA-660) (#1596)

## Summary

- **What broke (ECA-660):** `generate_session_title` was firing on every
new chat session's first message for every agent, sending `gpt-5.2` to
LiteLLM with the user's `team_key`. Team keys are scoped to group
aliases (`pro-chat`, `pro-image_generation`, `pro-video_generation`),
not concrete model names — so every billing-initialized user hit
`litellm.AuthenticationError: team not allowed to access model`.
- **Why it was hidden:** the call is fire-and-forget with a truncation
fallback, so users just saw a "dumb" auto-truncated title.
`ecap-scanner` finally surfaced it on 2026-05-12 as ECA-660.
- **Why most of those calls were wasted work:** only `/canvas` actually
displays `task_title` in its UI. `/chat`, `/mini-chat`,
`/session-history` ignore it entirely; the `AgentChatClient` component
that would render it is orphaned (no page mounts it).

## Three-layer defense (so this can't quietly come back)

| Layer | Change |
| --- | --- |
| **Constant** | `TITLE_GENERATION_AGENTS = {"canvas"}` in
`services/claw-interface/app/routes/session/utils.py` — explicit set of
agents whose UI displays the generated title. |
| **Routing gate** | `chat.py` block 1 (canvas/fullstack_assistant
branch) gated by membership in that set. Block 2 (AGENT_PLATFORM branch)
was 100% dead code (no agent in that branch displays `task_title`) and
is **deleted**. |
| **Signature** | `generate_session_title()` loses its `api_key`
parameter — it now always uses `SETTINGS.LITELLM_PROXY_API_KEY` (system
key). Anyone trying to re-introduce a team_key path hits a `TypeError`,
not a silent 401. |

## Drive-by hygiene

Codex review flagged a Mattermost user token in
`.dev-logs/frontend.log:97` (untracked output from a previous
`scripts/dev.sh` run). Added `.dev-logs/` to `.gitignore` so the
directory can never be staged accidentally. **The leaked token should be
rotated separately** — this PR only prevents future leaks via git.

## Test plan

- [x] `pytest tests/unit/test_chat_validation.py
tests/unit/test_session_utils.py tests/unit/test_litellm_endpoints.py` →
92 passed
- [x] `ruff check` + `pyright` → clean on changed files (pre-commit
hooks all green)
- [x] New regression test `test_skips_title_for_non_canvas_agent`
confirms non-canvas agents do NOT spawn a title-gen task
- [x] Existing `test_auto_generates_title_when_missing` repurposed for
`agentName="canvas"` (positive path still covered)
- [ ] After deploy: confirm `[GENERATE_TITLE] Error generating title` in
GCP claw-interface logs drops to 0 → `ecap-scanner` auto-closes ECA-660
```

### PR Body

## Summary

- **What broke (ECA-660):** `generate_session_title` was firing on every new chat session's first message for every agent, sending `gpt-5.2` to LiteLLM with the user's `team_key`. Team keys are scoped to group aliases (`pro-chat`, `pro-image_generation`, `pro-video_generation`), not concrete model names — so every billing-initialized user hit `litellm.AuthenticationError: team not allowed to access model`.
- **Why it was hidden:** the call is fire-and-forget with a truncation fallback, so users just saw a "dumb" auto-truncated title. `ecap-scanner` finally surfaced it on 2026-05-12 as ECA-660.
- **Why most of those calls were wasted work:** only `/canvas` actually displays `task_title` in its UI. `/chat`, `/mini-chat`, `/session-history` ignore it entirely; the `AgentChatClient` component that would render it is orphaned (no page mounts it).

## Three-layer defense (so this can't quietly come back)

| Layer | Change |
| --- | --- |
| **Constant** | `TITLE_GENERATION_AGENTS = {"canvas"}` in `services/claw-interface/app/routes/session/utils.py` — explicit set of agents whose UI displays the generated title. |
| **Routing gate** | `chat.py` block 1 (canvas/fullstack_assistant branch) gated by membership in that set. Block 2 (AGENT_PLATFORM branch) was 100% dead code (no agent in that branch displays `task_title`) and is **deleted**. |
| **Signature** | `generate_session_title()` loses its `api_key` parameter — it now always uses `SETTINGS.LITELLM_PROXY_API_KEY` (system key). Anyone trying to re-introduce a team_key path hits a `TypeError`, not a silent 401. |

## Drive-by hygiene

Codex review flagged a Mattermost user token in `.dev-logs/frontend.log:97` (untracked output from a previous `scripts/dev.sh` run). Added `.dev-logs/` to `.gitignore` so the directory can never be staged accidentally. **The leaked token should be rotated separately** — this PR only prevents future leaks via git.

## Test plan

- [x] `pytest tests/unit/test_chat_validation.py tests/unit/test_session_utils.py tests/unit/test_litellm_endpoints.py` → 92 passed
- [x] `ruff check` + `pyright` → clean on changed files (pre-commit hooks all green)
- [x] New regression test `test_skips_title_for_non_canvas_agent` confirms non-canvas agents do NOT spawn a title-gen task
- [x] Existing `test_auto_generates_title_when_missing` repurposed for `agentName="canvas"` (positive path still covered)
- [ ] After deploy: confirm `[GENERATE_TITLE] Error generating title` in GCP claw-interface logs drops to 0 → `ecap-scanner` auto-closes ECA-660

🤖 Generated with [Claude Code](https://claude.com/claude-code)

