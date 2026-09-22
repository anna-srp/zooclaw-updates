---
title: "feat(platform): separate project and organization settings (#3830)"
type: "新功能"
priority: "中"
date: "2026-09-21"
status: "待审核"
channels: ""
---

# 开发者平台：项目设置与组织设置分开

## 核心宣传点

平台设置现在把项目范围的导航和组织设置拆开了。从账号菜单进去是一个独立的设置外壳，含 General 和 Organization 两页；Members 和 Billing 仍然显示但置灰，等对应产品模型实现后再开放。主侧边栏给组织积分余额留了位置，但不会先填一个假数字；用量统计保持在项目维度，老的 Billing 路由会重定向到组织 Billing。

## 分级

- 内部：P1
- 外部：B
- 发布状态：已上线

## PR 说明

## Summary

Platform settings now separate Project-scoped navigation from Organization settings. The account menu opens a dedicated settings shell with General and Organization pages, while Members and Billing remain visible but disabled until their product models are implemented.

The main sidebar reserves the Organization credit balance position without presenting a fake value. Usage stays Project-scoped, and the legacy Billing route redirects to the Organization Billing route.

## Validation

- `pnpm test` — 20 tests passed
- `pnpm typecheck`
- `pnpm lint`
- `pnpm build`
- visually checked the local Organization settings layout


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `162a9e988d68c8466b9955a3343104c7fedd743e`
- PR: #3830
- 作者：finn-srp
- 日期：2026-09-21T03:54:57Z

### Commit Message

```
feat(platform): separate project and organization settings (#3830)

## Summary

Platform settings now separate Project-scoped navigation from
Organization settings. The account menu opens a dedicated settings shell
with General and Organization pages, while Members and Billing remain
visible but disabled until their product models are implemented.

The main sidebar reserves the Organization credit balance position
without presenting a fake value. Usage stays Project-scoped, and the
legacy Billing route redirects to the Organization Billing route.

## Validation

- `pnpm test` — 20 tests passed
- `pnpm typecheck`
- `pnpm lint`
- `pnpm build`
- visually checked the local Organization settings layout
```

来源：SerendipityOneInc/ecap-workspace @ 162a9e98，PR #3830，作者 finn-srp。