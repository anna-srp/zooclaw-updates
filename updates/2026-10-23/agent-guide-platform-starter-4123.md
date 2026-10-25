---
title: "官网 Agent 指南重写：改用 Platform Starter，照着做不再卡住"
type: "其他公告"
priority: "中"
date: "2026-10-23"
status: "待审核"
channels: ""
---

# 官网 Agent 指南重写：改用 Platform Starter，照着做不再卡住

## 核心宣传点

官网的发布 Agent 指南原本建立在已于 2026-10-01 下线的旧版 App Kit 和 Work 密钥之上，读者做到第四步就无路可走，第二步还在引导使用错误类型的密钥。本次把它重写成基于 Platform Agent Starter 的 Demo 指南，标题改为「用 ZooWork 快速做一个 Agent Demo」，版本升到 3.0，路由不变。内容拆成六个阶段：设计 Agent、领取项目密钥并充值、让编码 Agent 写配置并执行初始化、本地启动试用、迭代、公开前检查，部署环节交给 Starter 自述文件。密钥由读者自己填入环境变量文件，不交给编码 Agent，也不粘贴到聊天里。

## 分级

- 内部：P2
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `af1af5e34df3d6557b67af7f40226b59d12a8463`
- PR: #4123
- 作者：finn-srp
- 日期：2026-10-23T02:51:29Z

### Commit Message

```
docs(web): rebuild the Agent guide around the Platform starter (#4123)

<!-- PR 标题：type(scope): description -->

## Summary

`/guides/publish-agent` 原来建立在 ZooWork App Kit 和 Work API key 上。App Kit
已在 2026-10-01 从 quickstarts 删除（zoowork-platform-quickstarts #18），读者照第 4
到第 6 步做不下去，第 2 步还在让读者用 `zct_` key。这次把指南改成基于 Platform Agent Starter 的
Demo 指南。

- **定位**：标题改为 “Build a ZooWork Agent Demo” / “用 ZooWork 快速做一个 Agent
Demo”，版本 3.0。路由不变。
- **六个阶段**：设计 Agent → 拿 Project key 并充值 → coding agent 写
`agent/agent.md` 和 `app.config.ts`，运行 `npm run setup` → `npm run dev` 试用
→ 迭代 → 公开之前。指南不负责部署，第 6 步指向 starter README 的 “Before you go public”。
- **key**：读者自己把 `zwp_live_` key 填进 `.env`，不交给 coding
agent，也不粘贴到聊天里。`.env.example` 已带 production 地址，指南只让读者填 key。第 2 阶段加了直达
platform.zoowork.ai 的按钮。
- **狗狗案例**：给出给 coding agent 的
Prompt，以及两个结果文件的完整内容，中英文各一套。为了渲染这两个文件，`guide-sections.tsx` 加了 3 行。
- **截图**：Platform API keys 截图来自 `web/platform` 的 `dev:preview` 假数据，只显示
key 前缀。狗狗案例的 4 张截图来自 staging 上 starter 的真实运行（最新 starter
`f56d4be`，加上页面展示的同一版 `agent.md`）。跑完已 cleanup，没有残留资源。旧的 App Kit 截图已删除。
- **概念、清单、总结**：App Kit、`AGENT_PICKER`、`ZOOWORK_AGENT_ID`、share link
全部移除；区分 coding skill 和 Platform Skill。
- **测试**：单测锁定 `zwp_live_xxx`、`agent/agent.md`、`npm run setup` 和 Platform
链接；全页禁止出现 `zct_`、`App
Kit`、`AGENT_PICKER`、`ZOOWORK_AGENT_ID`、`ZOOWORK_BASE_URL` 和真实 key。SEO
测试同步更新标题。

相关 PR：
- zoowork-sdk-skills #38：skill 只在“空目录 + 想要可运行的聊天 demo”时提一次 starter。
- zoowork-agents-docs #69：quickstart 的下一步加上 Agent Starter 链接。

待定（本 PR 不改）：导航入口仍叫 “Publishing Guide / 发布指南”。内部原稿 v2.01 的作者需要知道这次改版。

## Test plan

- [x] rebase 到最新 main 后运行 `pnpm test:unit`：866 个文件、10909 个用例通过，1 个跳过
- [x] `pnpm lint:ci`、`verify-web.sh --no-test`（guards、tsc、eslint）通过
- [x] `prettier --check`、图片大小检查通过
- [x] 本地 `next dev` 打开中英文页面：所有图片加载成功，手机宽度 390 下没有横向滚动；可复制块、案例的两个结果文件和
Platform 按钮显示正常

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

