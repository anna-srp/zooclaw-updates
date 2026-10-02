---
title: "Managed Agent API 入口全面开放：官网与 WebApp 的 Coming soon 全部解除"
type: "新功能"
priority: "高"
date: "2026-10-01"
status: "待审核"
channels: "站内弹窗+Use Case+Discord+changelog"
---

# Managed Agent API 入口全面开放：官网与 WebApp 的 Coming soon 全部解除

## 核心宣传点

Managed Agent API 其实已经在 platform.zoowork.ai 上线了，但官网上的入口还挂着 Coming soon、点不动，登录选择菜单里这个产品也还是禁用状态。这次把所有导流入口一次性启用：官网桌面页头和手机导航抽屉的 Products 菜单、首页首屏下方的四产品卡片、页头与首页 Hero / 底部 CTA 的 Get Started 下拉、公共页脚的产品区，以及 WebApp 的登录产品选择菜单，全部解除禁用并移除 Coming soon。站内导航保持当前标签页，外链类入口在新标签页打开。官网和 WebApp 之后共用同一个平台地址常量，以后改地址只需要改一处。

## 分级

- 内部：P1
- 外部：A
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## 改动说明

Managed Agent API 已在 https://platform.zoowork.ai 上线，但官网仍有入口显示 Coming soon、无法点击，登录选择菜单也仍禁用该产品。本次启用这些导流入口，并让官网与 WebApp 共用同一个平台地址常量。

基于最新 main（147177be3），包含 Lynn 的 #3968 以及随后首页产品文案调整 #3969；**已覆盖官网前部新增的四产品入口中的 Managed Agent API 卡片**。

## 涉及的全部入口

| 页面位置 | 本次改动 | 跳转方式 |
| --- | --- | --- |
| 官网桌面页头 → Products / 产品 → Managed Agent API | 解除禁用并移除 Coming soon，指向新平台 | 当前标签页 |
| 官网手机导航抽屉 → Products / 产品 → Managed Agent API | 与桌面共用产品配置，同步解除禁用并移除 Coming soon | 当前标签页 |
| 官网首页首屏下方四产品卡片 → Managed Agent API | 启用 Lynn 在 #3968 新增的卡片入口，移除 Coming soon 和不可点击状态 | 当前标签页 |
| 官网桌面页头 → 开始使用下拉菜单 → Managed Agent API | 将禁用菜单项改为平台外链 | 新标签页 |
| 官网手机导航抽屉 → 开始使用下拉菜单 → Managed Agent API | 通过共享菜单同步启用，点击后执行关闭导航回调 | 新标签页 |
| 官网首页首屏 Hero → Get Started / 开始使用下拉菜单 → Managed Agent API | 通过共享登录菜单启用平台外链 | 新标签页 |
| 官网首页底部 CTA → Get Started / 开始使用下拉菜单 → Managed Agent API | 通过共享登录菜单启用平台外链 | 新标签页 |
| 官网公共页脚 → Product / 产品 → Managed Agent API | 解除禁用并移除 Coming soon；覆盖首页及复用 MarketingChrome 的营销页面 | 新标签页 |
| 现有 /[locale]/platform/login 页面独立页脚 → Managed Agent API | StandaloneMarketingFooter 共用页脚配置，同步启用平台外链 | 新标签页 |
| WebApp 用户菜单 → Managed Agent API | 原先已可用且地址正确，本次改为引用统一地址常量，保持现有行为 | 新标签页 |

## 实现与边界

- 新增 `web/app/src/lib/platform-href.ts`，集中维护 `https://platform.zoowork.ai`，由产品配置、页脚配置、登录下拉菜单和 WebApp 用户菜单共用。
- 解除产品配置和页脚中的 `comingSoon` 状态；登录下拉菜单使用真实链接，保留键盘操作、菜单关闭和外链安全属性。
- 外链不拼接 `/zh`、`/en` 等语言前缀，也不携带 WebApp 的登录或 Agent handoff 参数；保留各入口原有的当前页/新标签页策略。
- 官网公共页头、页脚也覆盖 About 等营销页面；**About 页内底部的独立“开始使用”按钮未启用平台下拉菜单，不属于本次改动入口**。
- 现有 `/[locale]/platform/login` 路由及其登录逻辑保持不变，本次只影响其复用的页脚入口。
- 部署范围仅 `web/app`，无需修改或重新部署 `web/platform` 和后端。

## 验证

- [x] 5 个现有相关测试文件、176 项测试通过，覆盖桌面/手机导航、首页产品卡片、首页 CTA、中英文页脚及 WebApp 用户菜单回归。
- [x] 追加核验平台菜单点击关闭行为后，19 项页头测试再次通过。
- [x] TypeScript 类型检查和修改文件 ESLint 通过。
- [x] `verify-web.sh --guards-only` 仓库治理检查通过；`git diff --check` 通过。
- [x] `https://platform.zoowork.ai` 公网 HTTP 检查返回 200。
- [x] 合并预览构建、WebApp 全量测试、静态检查及 CodeQL 已通过；其余适用 CI 均通过。
- [x] Codex、Claude 自动评审均通过；人工评审已请求 @tim-srp。

请求 @tim-srp review。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `9ec8efab48eeb573366040b288cf99649a826e9e`
- PR: #3981
- 作者：david-srp
- 日期：2026-10-01T11:11:42Z

### Commit Message

```
fix(marketing): 启用官网与 WebApp 的 Managed Agent API 平台入口 (#3981)

## 改动说明

Managed Agent API 已在 https://platform.zoowork.ai 上线，但官网仍有入口显示 Coming
soon、无法点击，登录选择菜单也仍禁用该产品。本次启用这些导流入口，并让官网与 WebApp 共用同一个平台地址常量。

基于最新 main（147177be3），包含 Lynn 的 #3968 以及随后首页产品文案调整
#3969；**已覆盖官网前部新增的四产品入口中的 Managed Agent API 卡片**。

## 涉及的全部入口

| 页面位置 | 本次改动 | 跳转方式 |
| --- | --- | --- |
| 官网桌面页头 → Products / 产品 → Managed Agent API | 解除禁用并移除 Coming soon，指向新平台
| 当前标签页 |
| 官网手机导航抽屉 → Products / 产品 → Managed Agent API | 与桌面共用产品配置，同步解除禁用并移除
Coming soon | 当前标签页 |
| 官网首页首屏下方四产品卡片 → Managed Agent API | 启用 Lynn 在 #3968 新增的卡片入口，移除 Coming
soon 和不可点击状态 | 当前标签页 |
| 官网桌面页头 → 开始使用下拉菜单 → Managed Agent API | 将禁用菜单项改为平台外链 | 新标签页 |
| 官网手机导航抽屉 → 开始使用下拉菜单 → Managed Agent API | 通过共享菜单同步启用，点击后执行关闭导航回调 |
新标签页 |
| 官网首页首屏 Hero → Get Started / 开始使用下拉菜单 → Managed Agent API |
通过共享登录菜单启用平台外链 | 新标签页 |
| 官网首页底部 CTA → Get Started / 开始使用下拉菜单 → Managed Agent API |
通过共享登录菜单启用平台外链 | 新标签页 |
| 官网公共页脚 → Product / 产品 → Managed Agent API | 解除禁用并移除 Coming
soon；覆盖首页及复用 MarketingChrome 的营销页面 | 新标签页 |
| 现有 /[locale]/platform/login 页面独立页脚 → Managed Agent API |
StandaloneMarketingFooter 共用页脚配置，同步启用平台外链 | 新标签页 |
| WebApp 用户菜单 → Managed Agent API | 原先已可用且地址正确，本次改为引用统一地址常量，保持现有行为 |
新标签页 |

## 实现与边界

- 新增 `web/app/src/lib/platform-href.ts`，集中维护
`https://platform.zoowork.ai`，由产品配置、页脚配置、登录下拉菜单和 WebApp 用户菜单共用。
- 解除产品配置和页脚中的 `comingSoon` 状态；登录下拉菜单使用真实链接，保留键盘操作、菜单关闭和外链安全属性。
- 外链不拼接 `/zh`、`/en` 等语言前缀，也不携带 WebApp 的登录或 Agent handoff
参数；保留各入口原有的当前页/新标签页策略。
- 官网公共页头、页脚也覆盖 About 等营销页面；**About 页内底部的独立“开始使用”按钮未启用平台下拉菜单，不属于本次改动入口**。
- 现有 `/[locale]/platform/login` 路由及其登录逻辑保持不变，本次只影响其复用的页脚入口。
- 部署范围仅 `web/app`，无需修改或重新部署 `web/platform` 和后端。

## 验证

- [x] 5 个现有相关测试文件、176 项测试通过，覆盖桌面/手机导航、首页产品卡片、首页 CTA、中英文页脚及 WebApp
用户菜单回归。
- [x] 追加核验平台菜单点击关闭行为后，19 项页头测试再次通过。
- [x] TypeScript 类型检查和修改文件 ESLint 通过。
- [x] `verify-web.sh --guards-only` 仓库治理检查通过；`git diff --check` 通过。
- [x] `https://platform.zoowork.ai` 公网 HTTP 检查返回 200。
- [x] 合并预览构建、WebApp 全量测试、静态检查及 CodeQL 已通过；其余适用 CI 均通过。
- [x] Codex、Claude 自动评审均通过；人工评审已请求 @tim-srp。

请求 @tim-srp review。
```

来源：SerendipityOneInc/ecap-workspace @ 9ec8efab，PR #3981，作者 david-srp。
