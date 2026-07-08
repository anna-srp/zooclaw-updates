---
title: "修复会话线程分享授权问题"
type: "Bug Fix"
priority: "中"
date: "2026-07-07"
status: "待审核"
channels: ""
---

# 修复会话线程分享授权问题

## 核心宣传点

会话线程的聊天回放分享现在可以正常创建，分享内容准确对应所在话题。

## 原始内容

```
fix(chat-replay): authorize session thread shares (#2751)

## Summary
- authorize chat replay creation from canonical OpenClaw session-channel
records
- keep current-org workspace ownership as the join point, even when the
cached workspace `session_channel_id` is empty
- scope session-thread replay posts to the recorded Mattermost thread
root

## Validation
- `/home/node/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_chat_replay_create.py -q`
- `/home/node/.venvs/claw-interface/bin/python -m ruff check
services/claw-interface/app/services/chat_replay/create.py
services/claw-interface/tests/unit/test_chat_replay_create.py`
- `/home/node/.venvs/claw-interface/bin/python -m ruff format --check
services/claw-interface/app/services/chat_replay/create.py
services/claw-interface/tests/unit/test_chat_replay_create.py`
- `bash scripts/verify-changed.sh`

---

## PR Description

## Summary
- authorize chat replay creation from canonical OpenClaw session-channel records
- keep current-org workspace ownership as the join point, even when the cached workspace `session_channel_id` is empty
- scope session-thread replay posts to the recorded Mattermost thread root

## Validation
- `/home/node/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_chat_replay_create.py -q`
- `/home/node/.venvs/claw-interface/bin/python -m ruff check services/claw-interface/app/services/chat_replay/create.py services/claw-interface/tests/unit/test_chat_replay_create.py`
- `/home/node/.venvs/claw-interface/bin/python -m ruff format --check services/claw-interface/app/services/chat_replay/create.py services/claw-interface/tests/unit/test_chat_replay_create.py`
- `bash scripts/verify-changed.sh`

```
