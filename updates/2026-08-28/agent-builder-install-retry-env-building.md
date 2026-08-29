---
title: "修复：Agent 刚发布就装「仅自己可见」会失败，其实只是运行环境还没建好"
type: "Bug Fix"
priority: "中"
date: "2026-08-28"
status: "待审核"
channels: ""
---

# 修复：Agent 刚发布就装「仅自己可见」会失败，其实只是运行环境还没建好

## 核心宣传点

以「仅自己可见」发布 Agent 之后马上安装，经常直接报错——原因只是刚发布的 Pack 运行环境还在构建中，而安装请求不等它。现在遇到「环境未就绪」这一种错误会自动重试，采用指数退避、最长等 90 秒，通常几秒内就能装上。其他类型的失败仍然照常立即抛出，不会被重试逻辑吞掉，所以真正的问题不会被藏起来。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `aa335949c4b804f0d0234df8b9884a5c5d49d667`
- PR: #3570
- 作者: kaka-srp
- 日期: 2026-08-28T06:45:55Z

### Commit Message

```
fix(agent-builder): retry install while environment builds (#3570)

## Summary

- retry Agent Builder Only me installation while the published Pack
environment is still building
- scope retries to agent.environment_not_ready and preserve all other
failures
- bound retries to 90 seconds with exponential delays

## Verification

- agent-install unit tests: 24 passed
- agent-builder publish unit tests: 17 passed
- Prettier check passed for all four changed files
- Full local frontend gate skipped at the user's request; CI remains
authoritative

## Risk

Low. The retry is limited to one domain error and the backend reclaims
the same failed workspace with its existing idempotency key.
```

### PR Description

```
## Summary

- retry Agent Builder Only me installation while the published Pack environment is still building
- scope retries to agent.environment_not_ready and preserve all other failures
- bound retries to 90 seconds with exponential delays

## Verification

- agent-install unit tests: 24 passed
- agent-builder publish unit tests: 17 passed
- Prettier check passed for all four changed files
- Full local frontend gate skipped at the user's request; CI remains authoritative

## Risk

Low. The retry is limited to one domain error and the backend reclaims the same failed workspace with its existing idempotency key.

```
