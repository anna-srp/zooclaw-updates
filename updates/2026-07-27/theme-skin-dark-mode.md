---
title: 主题皮肤适配深色模式（新增 Warm Ember / Mono OLED 深色）
type: 体验优化
priority: 中
date: 2026-07-27
status: 待审核
channels: ""
---

## 核心宣传点

界面主题皮肤现在支持在浅色、深色和跟随系统三种外观模式下自由切换：两款可选皮肤新增了各具特色的 Warm Ember 与 Mono OLED 深色配色，且在深色下仍保留各皮肤原有的图标、按钮、悬停与聚焦色调；同时修复了 AI 专家页在深色模式下的背景显示，切换皮肤时页头状态标和设置导航也保持稳定不跳动。

## 原始内容

fix(theme): align custom skin dark modes (#3081)

## Summary

- allow theme skin selection in light, dark, and system appearance modes
- add distinct Warm Ember and Mono OLED dark treatments for the two selectable skins
- preserve each skin's light-mode icon, button, hover, and focus colors in dark mode
- fix dark backgrounds on AI Specialists pages
- keep the page header status pill and settings navigation fixed when switching skins

## Testing

- `PATH=/opt/homebrew/opt/node@24/bin:$PATH bash scripts/verify-web.sh src/components/settings/GeneralTab.tsx src/components/settings/SettingsLayout.tsx src/theme/brand-theme-tokens.css tests/unit/components/settings/GeneralTab.unit.spec.tsx tests/unit/theme/brand-themes.unit.spec.ts`
- browser-verified light and dark switching for ZooClaw Editorial and Productivity Flat
- browser-verified AI Specialists backgrounds and primary controls for both skins
- browser-measured identical header and settings-nav coordinates across all skins

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
