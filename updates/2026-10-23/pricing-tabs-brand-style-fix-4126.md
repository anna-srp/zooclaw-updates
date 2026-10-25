---
title: "修复：官网定价页分类栏被组件库样式覆盖，紫色选中态失效"
type: "Bug Fix"
priority: "低"
date: "2026-10-23"
status: "待审核"
channels: ""
---

# 修复：官网定价页分类栏被组件库样式覆盖，紫色选中态失效

## 核心宣传点

官网定价页的工具与媒体分类栏被新版设计系统的中性选择样式覆盖：共享组件引入了未纳入 CSS 分层的规则，优先级高过官网原有的工具类，宽度自适应和灰色底覆盖了原本与价格卡片同宽的全宽白色分类栏，白色滑块又接管了选中背景，导致紫色选中态消失。本次让官网这两组标签页直接使用底层无样式组件、在页面内设置品牌样式，恢复同宽分类栏、紫色选中背景与白色文字，手机端保持三列两行布局，顶部产品切换栏的全宽布局和品牌下划线也一并恢复，键盘导航、焦点与无障碍关联不变。

## 分级

- 内部：P3
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## 备注

仅改官网页面，设计系统仓库与 npm 包无需发布。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `53e5d93ce5b7c184f8fa4b5c831c6d44972904bd`
- PR: #4126
- 作者：lynn Zhuang
- 日期：2026-10-23T06:36:23Z

### Commit Message

```
fix(marketing): 恢复官网 pricing 分类栏的品牌样式 (#4126)

## Summary

- 修复官网 pricing 工具与媒体分类栏被设计系统 2.1.0
样式覆盖的问题，恢复与价格卡片同宽的分类栏、紫色选中背景和白色文字；手机端保留三列两行布局。
- 同时恢复页面顶部产品切换栏的全宽布局和品牌下划线。
- pricing 的品牌外观由官网页面管理，使用 Radix Tabs 保留键盘导航、焦点及 ARIA 关联。修改位于 ECAP
官网，独立设计系统仓库与 npm 包无需发布。

## Root cause

共享 Tabs 引入了未放入 CSS layer 的 `.zc-selection-group` / `.zc-selection-item`
规则，优先于官网原有的 Tailwind 工具类。`width: fit-content` 和灰色背景覆盖了官网的全宽白色分类栏；白色
moving indicator 又接管了选中背景，导致紫色选中态失效。

本次让官网两组 Tabs 直接使用现有 Radix 底层组件，在页面内设置品牌样式，不再依赖设计系统的中性 selection
样式。价格、文案和业务导航逻辑保持不变，未回退产品内 Tabs / Segmented。

## Test plan

- [x] 先运行浏览器回归检查复现失败：1440px 下分类栏比内容卡片窄约 494px。
- [x] 修复后 Playwright 6/6 通过：中英文 × 375 / 768 /
1440px；检查实际计算颜色、全宽对齐、各分类内容关联、键盘循环与 End 导航、产品切换及横向溢出。
- [x] pricing 相关单元测试 70/70 通过，包含价格目录、导航、方案展示、翻译完整性与 typography 检查。
- [x] `verify-web.sh --no-test`：治理检查、TypeScript 和改动文件 ESLint
通过；新增独立测试配置后再次运行 TypeScript / ESLint 通过。
- [x] `pnpm install --frozen-lockfile --offline --ignore-scripts`
通过；仅声明工作区已有的 `radix-ui@1.5.0` 为官网直接依赖，没有升级依赖。
- [x] 新视觉测试配置已登记到 Knip 的 Playwright 入口，`knip` 硬门禁与完整 `pnpm lint:ci`
通过。初轮 CI 暴露的两个测试文件未登记问题已修复，未增加任何忽略项。
- [x] 最新提交 `672f3ee2c` 的远程 CI 已通过，包括官网生产构建、全量单测、质量门禁与
CodeQL；两项自动审查均通过，无阻塞发现。仍需仓库要求的人工 review 后合并。

本地重跑视觉检查（先启动官网并读取实际端口）：

```sh
PRICING_BASE_URL=http://localhost:<实际端口> pnpm exec playwright test --config tests/visual/pricing-tabs.config.ts
```

另：排查期间误跑到已有的页脚视觉测试 `landing-footer-consent-row.spec.ts`，其 fixture 读取现有
Button re-export 时报 `Unexpected fixture dependency:
@zooclaw/design-system`。该 fixture 与 Button 文件均未在本 PR 改动；本次为 pricing
提供独立配置，不扩大到页脚测试修复。

## 审查备注的处理

- 视觉回归检查目前需本地启动服务后运行，未接入 CI；CI 已通过的是既有构建、单元测试和质量门禁。自动启动服务的视觉 CI 可独立完善。
- RGB 固定值用于保护用户指定的品牌外观；有意更改 pricing 的设计 token 时应同步更新预期。
- 面板的 `outline-none` 沿用原共享 Tabs 的表现，本 PR 没有新增或扩大该行为。焦点规则的整体改进留作独立调整。
```

