---
title: "修复：垂直行业套餐里的 Agent 有新版本也不提示更新"
type: "Bug Fix"
priority: "中"
date: "2026-09-02"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：垂直行业套餐里的 Agent 有新版本也不提示更新

## 核心宣传点

已安装 Agent 的「有更新」判断以前只比对 Marketplace、组织私有包和分享包三个目录，而且排除了非 engine 运行时。垂直行业套餐里的 Agent Pack 来自另一个接口，所以这类 Agent 永远找不到对应的最新版本，界面上根本不显示更新状态。侧边栏那边也只画了一个头像角标，没有真正能点的更新入口。

现在判断更新时纳入当前登录用户的垂直行业套餐 Agent Pack，并在侧边栏里为有新版本的 Agent 在「New Task」旁边加了一个紧凑的品牌紫色更新按钮，主 Agent 和附加 Agent 都覆盖。更新开始后即使鼠标移出该行也会持续显示「Updating」，请求很快返回时也至少展示 500ms 的加载反馈，不会一闪而过让人以为没点上。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `7506b2f777833f17ab17ed17a57b9ac62f6d3fda`
- PR: #3627
- 作者: lynn Zhuang
- 日期: 2026-09-02T13:45:11Z

### Commit Message

```
fix(agents): 展示垂直行业包 Agent 更新提示 (#3627)

## 变更摘要
- 在判断已安装 Agent 是否有更新时，纳入当前登录用户的垂直行业套餐 Agent Pack
- 在侧边栏过期 Agent 的 New Task 旁展示紧凑的品牌紫色更新按钮，覆盖主 Agent 和附加 Agent
- 更新开始后，即使鼠标移出 Agent 行也持续显示 Updating；快速请求至少展示 500ms 的加载反馈
- 增加垂直行业包、computer runtime、侧边栏按钮顺序与常驻状态、快速更新反馈的回归测试

## 根因
原有更新判断仅对比 Marketplace、组织私有包或分享包目录，并且排除了非 engine runtime。垂直行业套餐中的 Agent
Pack 来自当前垂直套餐接口，因此已安装 Agent 找不到对应的最新版本，界面无法显示更新状态。侧边栏此前也只渲染头像
badge，没有提供实际更新入口。

## 测试计划
- [x] 针对更新 hook、版本判断、侧边栏组件及相关测试运行 `bash scripts/verify-web.sh`
- [x] 通过 46 项 Vitest 定向测试，覆盖侧边栏及共享更新反馈
- [x] 通过 `bash scripts/verify-changed.sh`
- [x] 使用本地 mock 手动验证 Update、鼠标移出后的 Updating 常驻，以及成功后的按钮消失
```

### PR Body

```
## 变更摘要
- 在判断已安装 Agent 是否有更新时，纳入当前登录用户的垂直行业套餐 Agent Pack
- 在侧边栏过期 Agent 的 New Task 旁展示紧凑的品牌紫色更新按钮，覆盖主 Agent 和附加 Agent
- 更新开始后，即使鼠标移出 Agent 行也持续显示 Updating；快速请求至少展示 500ms 的加载反馈
- 增加垂直行业包、computer runtime、侧边栏按钮顺序与常驻状态、快速更新反馈的回归测试

## 根因
原有更新判断仅对比 Marketplace、组织私有包或分享包目录，并且排除了非 engine runtime。垂直行业套餐中的 Agent Pack 来自当前垂直套餐接口，因此已安装 Agent 找不到对应的最新版本，界面无法显示更新状态。侧边栏此前也只渲染头像 badge，没有提供实际更新入口。

## 测试计划
- [x] 针对更新 hook、版本判断、侧边栏组件及相关测试运行 `bash scripts/verify-web.sh`
- [x] 通过 46 项 Vitest 定向测试，覆盖侧边栏及共享更新反馈
- [x] 通过 `bash scripts/verify-changed.sh`
- [x] 使用本地 mock 手动验证 Update、鼠标移出后的 Updating 常驻，以及成功后的按钮消失

```

