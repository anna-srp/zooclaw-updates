---
title: "安全加固：移除暴露敏感数据的调试接口"
type: "Bug Fix"
priority: "高"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# 安全加固：移除暴露敏感数据的调试接口

## 核心宣传点

修复了平台 API 中暴露环境变量、配置密钥等敏感信息的未鉴权调试接口，保护用户和平台安全。

## 原始内容

**Commit**: `351f0e3d44c4103bedd713a26d8ea8d810683bc6`
**仓库**: ecap-workspace
**作者**: tim-srp
**时间**: 2026-04-28T13:24:33Z

### 完整 Commit Message

```
fix(api): remove debug endpoints that expose sensitive system data (#1449)

## Summary
- Remove `/admin/settings`, `/admin/manifest`, `/admin/sysinfo`
endpoints that expose sensitive data (env vars, config secrets, system
metadata) without authentication
- Clean up unused `PrettyJSONResponse` class and commented-out GPU code
- Remove corresponding unit tests for deleted endpoints

## Test plan
- [ ] CI passes (ruff, pyright, pytest)
- [ ] Verify `/` heartbeat still responds with `{"status": "ok"}`
- [ ] Confirm `/admin/sysinfo`, `/admin/settings`, `/admin/manifest`
return 404

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR #1449 完整描述

## Summary
- Remove `/admin/settings`, `/admin/manifest`, `/admin/sysinfo` endpoints that expose sensitive data (env vars, config secrets, system metadata) without authentication
- Clean up unused `PrettyJSONResponse` class and commented-out GPU code
- Remove corresponding unit tests for deleted endpoints

## Test plan
- [ ] CI passes (ruff, pyright, pytest)
- [ ] Verify `/` heartbeat still responds with `{"status": "ok"}`
- [ ] Confirm `/admin/sysinfo`, `/admin/settings`, `/admin/manifest` return 404

🤖 Generated with [Claude Code](https://claude.com/claude-code)
