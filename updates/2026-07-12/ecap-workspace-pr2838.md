---
title: "Agent 发布页操作更清爽，安装/更新一步到位"
type: "体验优化"
priority: "中"
date: "2026-07-12"
status: "待审核"
channels: ""
---

## 核心宣传点

自定义专家 Agent 的发布页面焕新了：安装/更新按钮成为最醒目的主操作，「打开 Builder」保持一键可达，而列表上架、分享/取消分享、卸载、删除等操作被收进整洁的「更多」菜单里。界面状态提示和确认弹窗也统一采用了新设计系统，操作更清爽、主次更分明。

## 原始内容

**Commit**: `797e5af2ac` feat(web): streamline publish card actions (#2838)
**作者**: bill-srp | **日期**: 2026-07-12T14:24:30Z | **PR**: #2838

### Commit Message

```
feat(web): streamline publish card actions (#2838)

## Summary

- refresh the custom specialist publish page, cards, status feedback,
and confirmation modals with the shared design-system controls
- make Install/Update the primary card action, keep Open Builder
visible, and move List, Share/Unshare, Uninstall, and destructive Delete
into an overflow menu
- add localized labels plus coverage for install state, menu ordering,
destructive placement, and keyboard interaction

## Testing

- `bash scripts/verify-web.sh
web/app/tests/unit/app/agents-manager-publish.unit.spec.tsx`
- ESLint across all changed `web/app` files
- `bash scripts/verify-changed.sh`
- local `ready-user` Mock browser validation on
`/agents-manager/publish`, including the expanded overflow menu
```

### PR Body

## Summary

- refresh the custom specialist publish page, cards, status feedback, and confirmation modals with the shared design-system controls
- make Install/Update the primary card action, keep Open Builder visible, and move List, Share/Unshare, Uninstall, and destructive Delete into an overflow menu
- add localized labels plus coverage for install state, menu ordering, destructive placement, and keyboard interaction

## Testing

- `bash scripts/verify-web.sh web/app/tests/unit/app/agents-manager-publish.unit.spec.tsx`
- ESLint across all changed `web/app` files
- `bash scripts/verify-changed.sh`
- local `ready-user` Mock browser validation on `/agents-manager/publish`, including the expanded overflow menu
