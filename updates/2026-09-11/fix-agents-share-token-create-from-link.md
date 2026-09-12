---
title: "修复：通过分享链接创建 Agent 时提示「链接无效」"
type: "Bug Fix"
priority: "高"
date: "2026-09-11"
status: "待审核"
channels: "changelog"
---

# 修复：通过分享链接创建 Agent 时提示「链接无效」

## 核心宣传点

别人分享 Agent 给你，你点「Create from link」粘贴链接——结果安装页直接报链接无效。这个问题现在修好了。

**根因挺绕的，是三个机制叠在一起**：创建弹窗本身把分享 token 提取得没问题，但 `useLocalizedRouter` 会给目标地址加上 `/en` 或 `/zh` 前缀；staging 中间件又会把带语言前缀的应用 URL 重定向到无前缀的规范路径；而 Next.js 客户端导航在这次重定向过程中会丢掉 URL 里的 token fragment。于是安装页拿不到 token，还没调安装接口就先报了链接无效。

修复方式是让「Create from link」直接打开本地规范地址 `/agent-install#token=...`，绕开语言前缀那一环。其他本地化导航、链接校验、fragment-only token 传输和安装行为都不变。

验证做得比较实在：用匿名浏览器和一个合成的非敏感 token 在真实 staging 前端上验证了直接导航和规范客户端导航两条路径，token 都能保住。

## 原始内容

### fix(agents): preserve share token when creating from link (#3703)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `f4eeeeb9`
- PR: #3703
- 作者: kaka-srp
- 日期: 2026-09-11

改动要点（PR 原文）：修复「Create from link」，使其直接打开本地规范 `/agent-install#token=...` URL；保持其他本地化导航、链接校验、fragment-only token 传输与安装行为不变；通过真实 Agents view model、创建流程与本地化 router wrapper 增加回归覆盖。

根因（PR 原文）：创建弹窗正确提取了分享 token，但 `useLocalizedRouter` 给目标地址加了 `/en` 或 `/zh` 前缀。Staging 中间件将带语言前缀的应用 URL 重定向到无前缀的规范路径，Next.js 客户端导航在该重定向中丢失 token fragment，因此安装页在调用安装 API 之前就报告链接无效。使用匿名浏览器与合成的非敏感 token 在真实 staging 前端验证了直接导航与规范客户端导航，两者均保留 token。

## 备注

发布状态：已合并待发版（尚未包含在 `ecap-v0.19.5-release` 中）。

对外发布注意：影响 Agent 分享安装这条核心增长链路，优先级高。进 changelog。
