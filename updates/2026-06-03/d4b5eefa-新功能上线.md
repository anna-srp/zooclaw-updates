---
title: "新增 Mattermost 频道连接支持"
type: "新功能上线"
priority: "高"
date: "2026-06-03"
status: "待审核"
channels: "站内弹窗, Use Case, Discord, changelog"
---
# 新增 Mattermost 频道连接支持

## 核心宣传点

现在可以直接在 Mattermost 频道里使用 ZooClaw，无需切换工具。

## 原始内容

**Repo:** SerendipityOneInc/ecap-workspace  
**SHA:** `d4b5eefaf8285248ac19db668bfc74ba02bb4dbb`  
**作者:** bill-srp  
**日期:** 2026-06-03T02:59:13Z  
**URL:** https://github.com/SerendipityOneInc/ecap-workspace/commit/d4b5eefaf8285248ac19db668bfc74ba02bb4dbb

### Commit Message

```
feat(openclaw): create Mattermost session channels (#2155)

## Linear

https://linear.app/srpone/issue/ECA-881/create-mattermost-channel-per-openclaw-chat-session

## Summary
- Add `ecap-openclaw-session-channels` Mongo mapping for OpenClaw
session id, uid, computer id, agent id, Mattermost channel id, title,
and status.
- Add backend service to create a fresh Mattermost private channel per
OpenClaw chat session, add the human Mattermost user and selected agent
bot, remove the service/admin creator member, and persist the mapping.
- Add best-effort cleanup for Mattermost channels created before
downstream membership/creator/DB persistence failures, preserving the
original error while logging cleanup failures.
- Add Mattermost client support for private channel creation,
current-user lookup, member removal, and channel deletion.
- Expose backend APIs: `POST /openclaw/conversation/sessions` and `GET
/openclaw/conversation/sessions`.
- Add `MATTERMOST_TEAM_ID` setting plus startup index creation for the
session-channel collection.

Scope explicitly excludes Next.js BFF and chat UI wiring.

## Test plan
- [x] `.venv/bin/ruff check .`
- [x] `.venv/bin/python -m pytest
tests/unit/test_openclaw_session_channel_repo.py
tests/unit/test_mattermost_client.py
tests/unit/test_openclaw_session_channel_service.py
tests/unit/test_openclaw_conversation.py tests/unit/test_lifetime.py -v`
— 79 passed
- [x] `.venv/bin/python -m pytest --cov=app --cov-report=term-missing
--cov-fail-under=90 -q` — 4456 passed, 377 skipped, but repo-wide
coverage gate failed at 88.53% vs 90%
- [ ] CI `python-code-quality / build-and-test` green
- [ ] Manual: `POST /openclaw/conversation/sessions` for a
provisioned-agent user creates a Mattermost private channel with human +
bot user only, no service/admin member
- [ ] Manual: `GET /openclaw/conversation/sessions?agent_id=main` lists
prior sessions in descending recency

---------

Co-authored-by: claude[bot] <41898282+claude[bot]@users.noreply.github.com>
Co-authored-by: bill-srp <undefined@users.noreply.github.com>
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-881/create-mattermost-channel-per-openclaw-chat-session

## Summary
- Add `ecap-openclaw-session-channels` Mongo mapping for OpenClaw session id, uid, computer id, agent id, Mattermost channel id, title, and status.
- Add backend service to create a fresh Mattermost private channel per OpenClaw chat session, add the human Mattermost user and selected agent bot, remove the service/admin creator member, and persist the mapping.
- Add best-effort cleanup for Mattermost channels created before downstream membership/creator/DB persistence failures, preserving the original error while logging cleanup failures.
- Add Mattermost client support for private channel creation, current-user lookup, member removal, and channel deletion.
- Expose backend APIs: `POST /openclaw/conversation/sessions` and `GET /openclaw/conversation/sessions`.
- Add `MATTERMOST_TEAM_ID` setting plus startup index creation for the session-channel collection.

Scope explicitly excludes Next.js BFF and chat UI wiring.

## Test plan
- [x] `.venv/bin/ruff check .`
- [x] `.venv/bin/python -m pytest tests/unit/test_openclaw_session_channel_repo.py tests/unit/test_mattermost_client.py tests/unit/test_openclaw_session_channel_service.py tests/unit/test_openclaw_conversation.py tests/unit/test_lifetime.py -v` — 79 passed
- [x] `.venv/bin/python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q` — 4456 passed, 377 skipped, but repo-wide coverage gate failed at 88.53% vs 90%
- [ ] CI `python-code-quality / build-and-test` green
- [ ] Manual: `POST /openclaw/conversation/sessions` for a provisioned-agent user creates a Mattermost private channel with human + bot user only, no service/admin member
- [ ] Manual: `GET /openclaw/conversation/sessions?agent_id=main` lists prior sessions in descending recency
