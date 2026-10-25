---
title: "开发者平台全面接入 ZooWork 设计系统，导航、页面结构和移动端深色模式统一重做"
type: "体验优化"
priority: "高"
date: "2026-10-19"
status: "待审核"
channels: ""
---

# 开发者平台全面接入 ZooWork 设计系统，导航、页面结构和移动端深色模式统一重做

## 核心宣传点

Platform 统一改用 ZooWork Design System 组件，并按「导航 → 页面结构 → 操作反馈」重排信息层级，覆盖桌面、平板、移动端和深色模式。品牌 Logo/favicon 按 Figma 更新，高亮色统一为 #288DFF，主侧栏复用共享导航、Project 切换、Profile 菜单和 Credits，移动端改用抽屉。API keys、Projects、Organization、Account、Usage/Billing、Webhooks 等页统一列表与分区布局，密钥仍只展示一次，真实余额、赠送额度和权限逻辑不变，并修复短屏菜单裁切与深色 Logo 可读性问题。

## 分级

- 内部：P1
- 外部：A
- toB 相关：是
- 发布状态：已合并待发版

## 备注

尚未接通的 Members / Limits 页面如实展示为不可用状态；依赖共享组件（Project 切换、账号菜单/Credits、Footer、页头、外观选择）与主站同步复用，需确认设计系统包版本配套。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `429f3585ca7b375210e8c579cdcbc1cc80980a15`
- PR: #4084
- 作者：lynn Zhuang
- 日期：2026-10-19T04:14:58Z

### Commit Message

```
feat(platform): 统一 ZooWork 设计系统并优化全站布局与交互 (#4084)

## 改动摘要

将 Platform 从各页独立的样式与布局，统一为直接使用 ZooWork Design System 的组件，并按「导航 → 页面结构 →
操作反馈」整理信息层级。侧边栏与各业务页已经过多轮本地预览验收，最终包含桌面、平板、移动端和深色模式适配。

### 导航与品牌

- 使用指定 Figma Logo / favicon，品牌高亮色统一为 `#288DFF`。
- 主侧栏复用共享导航、Project 切换、Profile 菜单、Credits 和底部分隔线；选中项目显示对勾，创建项目使用描边按钮。
- 桌面侧栏保持展开；移动端使用抽屉，并补全当前路由的焦点行为。
- Settings 二级侧栏移除底部重复的 Profile 入口及其分隔线，保留顶部 Account
导航、页面内退出登录，以及独立的额度提示。

### 页面与交互

- API keys：统一页头、项目范围提示与表格，明确创建校验、撤销对象和处理中状态，保留密钥仅展示一次的行为。
- Projects / Project settings / Organization / Account：统一列表和分区布局、状态标识、详情
Tabs 与外观选择；未接通的 Members / Limits 如实展示不可用状态。
- Usage / Billing：梳理范围筛选、概览、明细和付款记录；保留真实余额、赠送额度与权限逻辑，补全支付处理中对弹窗的保护。
- Webhooks：按配置、密钥、投递记录和删除操作分区，保留创建、编辑、测试、轮换、删除和重试流程。
- 登录、条款、404：统一反馈与基础组件，保留现有法律正文和登录流程。
- 修复短屏菜单裁切、页面滚动、错误恢复焦点与深色 Logo 可读性。
- 自动审查后补正：Settings 侧栏关闭充值提醒时，焦点返回 Billing 导航；主侧栏仍返回 Profile，避免移除二级
Profile 后出现键盘焦点丢失。

### 共享组件与主站兼容

补齐共享的 Project 切换、账号菜单 / Credits、Footer、页头、外观选择及表格可访问性能力。主站同步复用 Footer 与
Credits；合并最新 main 时保留其新增的 Cookie 设置入口。

通用能力已同步提取到独立组件库的 [Design System PR
#8](https://github.com/SerendipityOneInc/Zoowork-design-system/pull/8)。本
PR 使用 monorepo 内的 workspace 包，不依赖该 PR 合并或 npm 发版。

## 提交与验收资料

- 按侧栏、API
keys、账号与项目、Usage、Billing、Webhooks、辅助页、回归修复、验收文档分批提交，保留逐批追溯与回滚边界。
- 设计规范：`web/platform/DESIGN.md`。
- 计划：`docs/superpowers/plans/2026-10-16-platform-full-redesign.md`。
- 截图、交互验证与 HTML 对比报告的复现入口：`web/platform/scripts/README.md`。
- 已将改动清单、组件反向补充记录和 HTML 前后对比报告写入用户的 Obsidian Platform 笔记目录；本地验收截图未提交到
Git。

## 验证

- [x] Platform：297 项单元测试、TypeScript、ESLint 通过。
- [x] Workspace Design System：477 项测试、TypeScript、ESLint 通过。
- [x] 同步最新 main 后，主站账号菜单、侧栏 Footer 与 Cookie 设置相关 94 项测试通过。
- [x] Platform 生产构建通过。
- [x] 16 条浏览器交互流程通过；13 个页面 × 4 种展示模式的改后截图共 52
张，未检测到横向溢出或页面异常，并保留同场景改前截图供对比。
- [x] 针对最新二级侧栏反馈，复验桌面、390px 移动端、深色模式、Account / Billing 导航及返回 Console
后的账号菜单。
- [x] 充值提醒焦点问题先以回归测试复现，再验证修复；相关 98 项路由测试、类型检查和定向 ESLint
通过。[二级侧栏回归测试](https://github.com/SerendipityOneInc/ecap-workspace/blob/296eaf529daf036610ae87089bb9819f4f89f8ac/web/platform/src/app/router.test.tsx#L603)
分别覆盖 Account 与 Billing 路由，直接断言关闭提醒后 Billing 导航链接获得焦点；另保留主侧栏返回 Profile
的断言。

验证基于本地样例数据；没有执行真实支付、生产 API 写入或线上部署。Billing
本次调整为展示与交互反馈，不修改支付后端、金额计算或权限边界。完整仓库检查以本 PR 的 CI 为准。
```

