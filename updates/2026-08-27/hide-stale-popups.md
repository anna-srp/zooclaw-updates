---
title: "关掉了那些内容已经过期的引导弹窗和功能发布弹窗"
type: "体验优化"
priority: "低"
date: "2026-08-27"
status: "待审核"
channels: ""
---

# 关掉了那些内容已经过期的引导弹窗和功能发布弹窗

## 核心宣传点

新手引导（Guide Tour）和功能发布轮播在里面的内容早就过期之后，仍然会挂在页面上，符合条件的用户还会被弹出「One brain. Full crew.」「PPTX Master just leveled up」这类旧公告。现在这两个弹窗的自动展示被暂停，用户菜单里的 What's New 入口也一并隐藏；实现本身完整保留，等有新内容时重新打开开关即可。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `5120d60ce79cb7c96e226f689c7578a8cd7880b7`
- PR: #3549
- 作者: lynn Zhuang
- 日期: 2026-08-27T08:27:27Z

### Commit Message

```
fix(web): 隐藏过期的引导与功能发布弹窗 (#3549)

## 背景

Guide Tour 和 Feature Launch 轮播在公告内容过期后仍会全局挂载，符合条件的用户可能继续看到旧的「One brain.
Full crew.」和「PPTX Master just leveled up」弹窗。

## 改动内容

- 通过独立开关暂停自动展示 Guide Tour，并隐藏用户菜单中的 `What's New` 入口
- 暂停聊天页的 Feature Launch / PPTX 轮播弹窗，包括仅开发环境使用的 `?force-launch=1` 路径
- 保留两个弹窗的现有实现和内容，后续有新内容时只需重新开启对应开关
- 将 Feature Launch 开关与弹窗组件模块解耦，避免整模块 mock 缺少开关导出

## 验证

- [x] 相关 TypeScript 类型检查通过
- [x] 相关 Vitest：60 个测试通过
- [x] mock backend：34 个测试通过
- [x] ESLint 通过
- [x] pre-push changed-surface 验证通过
- [x] 本地浏览器验证：Guide Tour、`What's New` 入口和 Feature Launch
弹窗均不再出现，`?force-launch=1` 也无法绕过开关
- [x] GitHub CI：38/38 检查通过

## 风险与恢复方式

本次只控制组件挂载，不删除弹窗实现，风险较低。后续需要重新展示时，将对应开关设为开启并更新内容即可。
```

### PR Description

```
## 背景

Guide Tour 和 Feature Launch 轮播在公告内容过期后仍会全局挂载，符合条件的用户可能继续看到旧的「One brain. Full crew.」和「PPTX Master just leveled up」弹窗。

## 改动内容

- 通过独立开关暂停自动展示 Guide Tour，并隐藏用户菜单中的 `What's New` 入口
- 暂停聊天页的 Feature Launch / PPTX 轮播弹窗，包括仅开发环境使用的 `?force-launch=1` 路径
- 保留两个弹窗的现有实现和内容，后续有新内容时只需重新开启对应开关
- 将 Feature Launch 开关与弹窗组件模块解耦，避免整模块 mock 缺少开关导出

## 验证

- [x] 相关 TypeScript 类型检查通过
- [x] 相关 Vitest：60 个测试通过
- [x] mock backend：34 个测试通过
- [x] ESLint 通过
- [x] pre-push changed-surface 验证通过
- [x] 本地浏览器验证：Guide Tour、`What's New` 入口和 Feature Launch 弹窗均不再出现，`?force-launch=1` 也无法绕过开关
- [x] GitHub CI：38/38 检查通过

## 风险与恢复方式

本次只控制组件挂载，不删除弹窗实现，风险较低。后续需要重新展示时，将对应开关设为开启并更新内容即可。

```

---
