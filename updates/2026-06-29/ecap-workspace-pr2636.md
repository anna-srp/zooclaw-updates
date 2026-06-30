---
title: "会话支持标题：自动生成 + 手动重命名"
type: "新功能上线"
priority: "中"
date: "2026-06-29"
status: "待审核"
channels: ""
---

# 会话支持标题：自动生成 + 手动重命名

## 核心宣传点

现在每个会话都有标题：新建会话时会根据内容自动生成简洁标题，你也可以随时手动重命名，会话列表一眼就能找到想要的对话。

## 原始内容

### Commit Message

```
feat(chat): support conversation titles (#2636)

## Summary

- Add conversation title metadata to OpenClaw session-channel records
and keep create/update/list responses on the same record shape.
- Generate a concise title during conversation creation from the
submitted title via LiteLLM proxy, with fallback behavior when
generation is unavailable.
- Add manual rename through `POST
/computers/{computer_id}/agents/{agent_id}/conversations/{session_id}`
with `title` in the request body.
- Wire the frontend conversation list/thread UI to display and rename
titles.

Linear:
https://linear.app/srpone/issue/ECA-1034/chat-session-%E6%94%AF%E6%8C%81%E6%A0%87%E9%A2%98-rename-%E5%92%8C%E8%87%AA%E5%8A%A8%E7%94%9F%E6%88%90%E6%A0%87%E9%A2%98

## Local Checks

- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh` passed.
- `cd services/claw-interface &&
/Users/bill/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_chat_session_title_service.py
tests/unit/test_openclaw_session_channel_schema.py
tests/unit/test_openclaw_session_channel_repo.py
tests/unit/test_conversations.py
tests/unit/test_openclaw_session_channel_service.py
tests/unit/test_agent_builder_service.py -q` passed: 127 passed.
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-changed.sh` ran backend verification successfully and
exited 3 because `web/node_modules` is missing, so the web surface was
skipped.
- `bash scripts/verify-web.sh ...` ran frontend governance guards, then
could not reach tsc/vitest/eslint because pnpm attempted install and
repeatedly failed to resolve `registry.npmjs.org` in this environment. I
interrupted the retrying install after the repeated DNS failures.
```

### PR Description

## Summary

- Add conversation title metadata to OpenClaw session-channel records and keep create/update/list responses on the same record shape.
- Generate a concise title during conversation creation from the submitted title via LiteLLM proxy, with fallback behavior when generation is unavailable.
- Add manual rename through `POST /computers/{computer_id}/agents/{agent_id}/conversations/{session_id}` with `title` in the request body.
- Wire the frontend conversation list/thread UI to display and rename titles.

Linear: https://linear.app/srpone/issue/ECA-1034/chat-session-%E6%94%AF%E6%8C%81%E6%A0%87%E9%A2%98-rename-%E5%92%8C%E8%87%AA%E5%8A%A8%E7%94%9F%E6%88%90%E6%A0%87%E9%A2%98

## Local Checks

- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh` passed.
- `cd services/claw-interface && /Users/bill/.venvs/claw-interface/bin/python -m pytest tests/unit/test_chat_session_title_service.py tests/unit/test_openclaw_session_channel_schema.py tests/unit/test_openclaw_session_channel_repo.py tests/unit/test_conversations.py tests/unit/test_openclaw_session_channel_service.py tests/unit/test_agent_builder_service.py -q` passed: 127 passed.
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-changed.sh` ran backend verification successfully and exited 3 because `web/node_modules` is missing, so the web surface was skipped.
- `bash scripts/verify-web.sh ...` ran frontend governance guards, then could not reach tsc/vitest/eslint because pnpm attempted install and repeatedly failed to resolve `registry.npmjs.org` in this environment. I interrupted the retrying install after the repeated DNS failures.

