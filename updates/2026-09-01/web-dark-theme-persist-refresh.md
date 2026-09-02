---
title: "修复：设成深色主题后一刷新就变回浅色"
type: "Bug Fix"
priority: "中"
date: "2026-09-01"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：设成深色主题后一刷新就变回浅色

## 核心宣传点

在设置里选了 Dark，强制刷新页面后主题会掉回系统模式——如果系统是浅色，看起来就是深色设置「丢了」。根因在认证流程的存储清理：`next-themes` 用 localStorage 的 `ecap-theme` 键保存主题模式，而 `clearUserStorage()` 的保留白名单里只有设备 ID 和品牌主题键，登录清理、身份恢复、无效身份处理调到它时会把 `ecap-theme` 一起删掉，刷新后找不到保存值就回退成 system。

现在把用户显式选择的 `light` / `dark` / `system` 三种主题模式加进了固定白名单——这属于非敏感偏好，sessionStorage、React Query、Zustand 及其他用户范围数据的清理逻辑一律不变，用户数据隔离照旧。营销页强制浅色但不覆盖已保存偏好的既有约定也保留。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `b3da84fb05cd61a13993a35c3a5864072cec2bb1`
- PR: #3596
- 作者: lynn Zhuang
- 日期: 2026-09-01T09:21:51Z

### Commit Message

```
fix(web): 修复深色主题刷新后丢失 (#3596)

## Summary
- 在认证存储清理时保留用户显式选择的 `light`、`dark`、`system` 主题模式
- 增加 `clearUserStorage()` 的主题持久化契约测试，同时保持用户数据隔离与现有清理范围
- 补强 Dark mode E2E，覆盖 Settings → General → Dark → Chat → 强制刷新，并在系统 Light
模式下同时断言存储值和 `html.dark`
- 保留 marketing 页面强制 Light、但不覆盖已保存主题偏好的现有契约

## Root cause
`next-themes` 使用 localStorage 键 `ecap-theme` 持久化主题模式，但认证流程的
`clearUserStorage()` 只保留设备 ID 和品牌主题键。登录清理、身份恢复或无效身份处理调用该函数时，会误删
`ecap-theme`。页面强制刷新后 `next-themes` 因找不到保存值而回退到 `system`，在系统配色为 Light
时表现为用户选择的 Dark 丢失。

本修复仅将非敏感的主题模式偏好加入固定 allowlist；sessionStorage、React Query、Zustand
以及其他用户范围数据的清理逻辑保持不变。

## Test plan
- [x] TDD 红灯验证：新增的 light/dark/system 三个契约测试在修复前全部失败
- [x] 聚焦 Vitest：108/108 通过
- [x] `bash scripts/verify-web.sh`：guards、完整 TypeScript、130 个匹配测试和
ESLint 通过
- [x] `bash scripts/verify-changed.sh` 通过
- [x] 本地 `ready-user` mock stack + Chromium E2E：认证 setup 与主题持久化场景共 2
个测试通过
- [x] E2E 将系统 `colorScheme` 固定为 Light，并断言 `localStorage['ecap-theme']
=== 'dark'` 与 `html.dark`
- [ ] 部署到 Staging 后执行最终冒烟验证
```

### PR Body

```
## Summary
- 在认证存储清理时保留用户显式选择的 `light`、`dark`、`system` 主题模式
- 增加 `clearUserStorage()` 的主题持久化契约测试，同时保持用户数据隔离与现有清理范围
- 补强 Dark mode E2E，覆盖 Settings → General → Dark → Chat → 强制刷新，并在系统 Light 模式下同时断言存储值和 `html.dark`
- 保留 marketing 页面强制 Light、但不覆盖已保存主题偏好的现有契约

## Root cause
`next-themes` 使用 localStorage 键 `ecap-theme` 持久化主题模式，但认证流程的 `clearUserStorage()` 只保留设备 ID 和品牌主题键。登录清理、身份恢复或无效身份处理调用该函数时，会误删 `ecap-theme`。页面强制刷新后 `next-themes` 因找不到保存值而回退到 `system`，在系统配色为 Light 时表现为用户选择的 Dark 丢失。

本修复仅将非敏感的主题模式偏好加入固定 allowlist；sessionStorage、React Query、Zustand 以及其他用户范围数据的清理逻辑保持不变。

## Test plan
- [x] TDD 红灯验证：新增的 light/dark/system 三个契约测试在修复前全部失败
- [x] 聚焦 Vitest：108/108 通过
- [x] `bash scripts/verify-web.sh`：guards、完整 TypeScript、130 个匹配测试和 ESLint 通过
- [x] `bash scripts/verify-changed.sh` 通过
- [x] 本地 `ready-user` mock stack + Chromium E2E：认证 setup 与主题持久化场景共 2 个测试通过
- [x] E2E 将系统 `colorScheme` 固定为 Light，并断言 `localStorage['ecap-theme'] === 'dark'` 与 `html.dark`
- [ ] 部署到 Staging 后执行最终冒烟验证

```
