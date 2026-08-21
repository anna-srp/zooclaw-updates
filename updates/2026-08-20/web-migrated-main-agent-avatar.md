---
title: "修复：迁移后的主 Agent 头像恢复为官方形象"
type: "Bug Fix"
priority: "中"
date: "2026-08-20"
status: "待审核"
channels: ""
---

# 修复：迁移后的主 Agent 头像恢复为官方形象

## 核心宣传点

账号迁移后主 Agent 换用了新的公开 ID，聊天记录和输入框识别不出它是主 Agent，于是退回成一个硬编码的机器人 emoji。现在实时聊天和历史会话都能正确识别主 Agent，统一显示官方 Assistant 头像。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `015a6adda26719cc8576b54820ed8686a2c628e3`
- PR: #3464
- 作者: kaka-srp
- 日期: 2026-08-20T09:01:31Z

### Commit Message

```
fix(web): preserve main avatar for migrated agents (#3464)

## Summary
- Preserve canonical main-agent identity when migrated agents use a
public `agt_*` ID in both live chat and historical sessions.
- Use the branded Assistant avatar as the main-agent fallback in
transcript messages and the unified composer.
- Add regression coverage for migrated main agents and the empty
agent-picker fallback.

## Root cause
The session transcript inferred main-agent identity from the legacy
`main` ID, while migrated main agents expose a public `agt_*` ID. The
unified composer also used a hard-coded robot emoji when no explicit
avatar was present. Both paths therefore bypassed the branded main-agent
fallback even though the workspace correctly reported `is_main: true`.

## Test plan
- [x] `bash scripts/verify-web.sh <changed frontend paths>`
- [x] TypeScript compilation passed.
- [x] 158 targeted unit tests passed across the original changed chat
surfaces.
- [x] 56 targeted unit tests passed for the live-chat follow-up.
- [x] ESLint passed for the changed files and the repository commit
hook.
```

### PR Body

## Summary
- Preserve canonical main-agent identity when migrated agents use a public `agt_*` ID in both live chat and historical sessions.
- Use the branded Assistant avatar as the main-agent fallback in transcript messages and the unified composer.
- Add regression coverage for migrated main agents and the empty agent-picker fallback.

## Root cause
The session transcript inferred main-agent identity from the legacy `main` ID, while migrated main agents expose a public `agt_*` ID. The unified composer also used a hard-coded robot emoji when no explicit avatar was present. Both paths therefore bypassed the branded main-agent fallback even though the workspace correctly reported `is_main: true`.

## Test plan
- [x] `bash scripts/verify-web.sh <changed frontend paths>`
- [x] TypeScript compilation passed.
- [x] 158 targeted unit tests passed across the original changed chat surfaces.
- [x] 56 targeted unit tests passed for the live-chat follow-up.
- [x] ESLint passed for the changed files and the repository commit hook.


