---
title: "引导流程与启动加载页支持深色模式"
type: "体验优化"
priority: "低"
date: "2026-05-07"
status: "待审核"
channels: ""
---
# 引导流程与启动加载页支持深色模式

## 核心宣传点
首次使用引导流程和启动加载页面现已完整适配深色模式，深色主题下视觉体验更统一。

## 原始内容

### Commit Message
```
feat(web): onboarding & launch loading dark-mode 适配 (#1566)
```

### PR Description
## Summary
- 新建 `web/src/components/onboarding/onboarding.css` —— `.onboarding-root` + `.dark .onboarding-root` 双向 token，把 onboarding 整个 branded module 接到全局 `.dark` class 上但仍走独立色板，避免污染 `:root`
- LOGO 切换 `<img>` + `--onboarding-logo-filter: invert()` 跟随主题反色（R2 cross-origin 让 `mask-image` 不可用，filter 是更稳的替代）
- 7 个 step 组件 + Layout / Modal / SpriteDialogue / SpriteGuide / WelcomeRewardToast 把所有 `rgba(26,26,24,*)` / `#fafafa` 等硬编码替换成 `var(--onboarding-*)`，LoadingStep（"Entering..."）也一并适配
- `CompanionSelectStep`：cardBreathe keyframes 从 JS 注入挪进 CSS；3 个 slot 的 `AnimatePresence` 拆掉，改用 `LayoutGroup` + `layoutId` + `layout` 的纯 FLIP morph，消除点击侧卡时的 fade-flicker；hover 统一为 scale-only，消除侧卡 wash-out 闪烁
