---
title: "修复：预发环境官网入口会跳到生产版开发者平台"
type: "Bug Fix"
priority: "中"
date: "2026-10-22"
status: "待审核"
channels: ""
---

# 修复：预发环境官网入口会跳到生产版开发者平台

## 核心宣传点

官网里指向开发者平台的地址此前被写死为生产域名，而平台是独立部署的应用只能用绝对地址，导致预发环境上的 Managed Agent API 入口会把人带到生产平台。本次改为读取构建期环境变量，未设置时回退到生产域名，Get Started 下拉、产品列表、页脚、WebApp 用户菜单和定价页这 5 处入口一次性全部跟随环境；部署流水线会注入该变量并将其列为必填，预发漏配时部署直接失败而不是静默跳回生产。生产环境行为不变。

## 分级

- 内部：P2
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `4ade38ed6e432f9139c3d0d21617604b3a34e853`
- PR: #4111
- 作者：finn-srp
- 日期：2026-10-22T01:54:40Z

### Commit Message

```
fix(web): 按环境配置 Managed Agent API 的 platform 地址 (#4111)

## Summary
- `PLATFORM_HREF` 改为读取构建期变量 `NEXT_PUBLIC_PLATFORM_URL`，未设置时回退到
`https://platform.zoowork.ai`。官网 Get Started 下拉、产品列表、页脚、WebApp
用户菜单、pricing 页这 5 处入口都通过它跳转，不需要逐个改。
- `deploy.yml` 在 `Set environment variables` 和 `Create env file`
中注入该变量，并在 `Validate required variables` 中设为必填。staging 漏配时 deploy
直接失败，不会静默跳回生产。
- `.env.example` 增加该变量（staging 值）。
- GitHub Environment variables 已设置：staging 为
`https://platform.ecap.nosay.live`，production 为
`https://platform.zoowork.ai`。

## Root cause
`web/app/src/lib/platform-href.ts` 把 platform 地址写死为生产域名。Agent Builder
入口用的是相对路径 `/login`，会跟随当前 host，所以 staging 上正常；platform 是独立部署的应用，只能用绝对
URL，而这个 URL 没有按环境区分，导致 staging 的 Managed Agent API 入口跳到了生产。

## Test plan
- [x] 新增
`tests/unit/lib/platform-href.unit.spec.ts`：配置变量时使用配置值，未配置时回退生产地址
- [x] `bash scripts/verify-web.sh`（guards、tsc、vitest、eslint）
- [x] Node 24 下全量 `pnpm test:unit`：866 files，10909 passed，1 skipped
- [x] Node 24 下 `pnpm lint:ci`
- [ ] 合并后 staging deploy 完成，确认 staging 官网 Get Started > Managed Agent
API 跳到 `https://platform.ecap.nosay.live`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

