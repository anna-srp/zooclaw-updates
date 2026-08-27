---
title: "官网「Business」入口修正为直达企业管理后台登录页"
type: "体验优化"
priority: "低"
date: "2026-08-26"
status: "待审核"
channels: ""
---

# 官网「Business」入口修正为直达企业管理后台登录页

## 核心宣传点

官网顶部导航的 Business 链接和页脚对应入口此前指向不对，现在统一改为直达 ZooWork 企业管理后台的登录页，找企业版入口不用再绕路。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `af55006818ddbfccfa58b599d1ae1b4485fc7859`
- PR: #3519
- 作者: tim-srp
- 日期: 2026-08-26T03:39:46Z

### Commit Message

```
fix(landing): link business entry to enterprise login (#3519)

## Summary

- Point the landing-page Business navigation link to the ZooWork
Enterprise Admin login page.
- Align the ZooWork footer link with the same enterprise login
destination.

## Validation

- `git diff --check`
- `bash scripts/verify-web.sh web/app/src/lib/landing-content.ts`
(governance checks passed; TypeScript, Vitest, and ESLint unavailable
because this worktree has no frontend tool binaries)
```

### PR Description

```
## Summary

- Point the landing-page Business navigation link to the ZooWork Enterprise Admin login page.
- Align the ZooWork footer link with the same enterprise login destination.

## Validation

- `git diff --check`
- `bash scripts/verify-web.sh web/app/src/lib/landing-content.ts` (governance checks passed; TypeScript, Vitest, and ESLint unavailable because this worktree has no frontend tool binaries)

```
