---
title: "修复 Agent Builder 提交的 Pack 头像不显示的问题"
type: "Bug Fix"
priority: "中"
date: "2026-07-10"
status: "待审核"
channels: ""
---

## 核心宣传点

修复了通过 Agent Builder 提交的 Agent Pack 头像未能正确发布的问题，现在打包在压缩包内的头像会正常上架显示。

## 原始内容

**fix(agent-builder): publish submitted pack avatars (#2814)**

SHA: `0616fdf4f68a952edee3545f98a3a0306077341e` | 作者: kaka-srp | PR #2814

```
fix(agent-builder): publish submitted pack avatars (#2814)

## Summary
- Publish Agent Builder-submitted pack avatars when listing metadata
references `artifacts/avatar.png` inside the pack archive.
- Add deterministic public R2 avatar uploads and server-side R2 object
reads for backend-owned archives.
- Validate avatar size/type and reject missing or duplicate archive
avatar entries.

## Root cause
Agent Studio writes `avatar_url: "artifacts/avatar.png"` into listing
metadata and packages the image inside the archive. The Agent Builder
submit path only accepted `http(s)` avatar URLs, so the relative path
was filtered to `None` and Pack Store submissions were created without a
valid avatar.

## Test plan
- [x] `bash scripts/verify-py.sh`
- [x] `pytest
services/claw-interface/tests/unit/test_agent_builder_service.py
services/claw-interface/tests/unit/test_r2_storage.py`

Linear:
https://linear.app/srpone/issue/ECA-1205/investigate-missing-agent-pack-avatar
```

### PR body

## Summary
- Publish Agent Builder-submitted pack avatars when listing metadata references `artifacts/avatar.png` inside the pack archive.
- Add deterministic public R2 avatar uploads and server-side R2 object reads for backend-owned archives.
- Validate avatar size/type and reject missing or duplicate archive avatar entries.

## Root cause
Agent Studio writes `avatar_url: "artifacts/avatar.png"` into listing metadata and packages the image inside the archive. The Agent Builder submit path only accepted `http(s)` avatar URLs, so the relative path was filtered to `None` and Pack Store submissions were created without a valid avatar.

## Test plan
- [x] `bash scripts/verify-py.sh`
- [x] `pytest services/claw-interface/tests/unit/test_agent_builder_service.py services/claw-interface/tests/unit/test_r2_storage.py`

Linear: https://linear.app/srpone/issue/ECA-1205/investigate-missing-agent-pack-avatar

