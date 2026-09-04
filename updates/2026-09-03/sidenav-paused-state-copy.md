---
title: "侧边栏「休眠 Asleep」改成更明确的「已暂停 Paused」"
type: "体验优化"
priority: "中"
date: "2026-09-03"
status: "待审核"
channels: "Discord+changelog"
---

# 侧边栏「休眠 Asleep」改成更明确的「已暂停 Paused」

## 核心宣传点

侧边栏、账号菜单、额度显示和聊天拦截提示里原来用的是「Asleep / 休眠」这套睡觉比喻，在企业场景下含义模糊——用户看不出这是账号出了状况还是产品的某种正常模式。现在统一换成含义直白的「Paused / 已暂停」，图标也从自定义的 Zzz 换成 Heroicons 的暂停圆圈，配色改用已有的「警告」语义色，而不是中性色或危险色。

鼠标悬停或键盘聚焦时会明确说明：Agent 处于暂停状态，但记忆和数据都被安全保留着——这句最容易让人慌的事先讲清楚。10 种语言的文案和无障碍朗读文本都已同步。另外，现在可以直接点暂停状态的个人资料卡打开订阅恢复面板，箭头按钮仍然保持原来打开账号菜单的行为，两个入口不再互相抢。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `1fa96b521cbe82812e7548c4e0b3f9202d8d6bca`
- PR: #3634
- 作者: shana-srp
- 日期: 2026-09-03T07:34:50Z

### Commit Message

```
fix(sidenav): replace asleep state with paused (#3634)

## Summary

- replace the customer-facing `Asleep` / sleeping metaphor with the
clearer B2B status `Paused` across the sidebar, account menu, credits,
and chat gate copy
- swap the custom Zzz icon for Heroicons' pause-circle and use the
existing warning semantic color instead of a neutral or destructive
state
- explain on hover or keyboard focus that agents are paused while
memories and data remain safely preserved, with matching accessible text
and localized copy in all 10 locales
- open the subscription recovery panel directly from the paused profile
card while keeping the arrow button as the account-menu control

## Testing

- `pnpm exec vitest run tests/unit/components/UserCard.unit.spec.tsx
tests/unit/components/UserMenu.unit.spec.tsx
tests/unit/components/credits/CreditsDisplay.unit.spec.tsx` (123 passed)
- `bash scripts/verify-web.sh` (TypeScript and ESLint passed; the full
unit run reported only a sandbox `listen EPERM` in the mock-backend
socket test)
- `pnpm exec vitest run
tests/unit/scripts/mock-backend-agent-builder.unit.spec.ts` outside the
socket-restricted sandbox (34 passed)
- `bash scripts/verify-changed.sh`
- local browser verification that clicking the paused card opens the
subscription panel and leaves the account menu closed

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

```
## Summary

- replace the customer-facing `Asleep` / sleeping metaphor with the clearer B2B status `Paused` across the sidebar, account menu, credits, and chat gate copy
- swap the custom Zzz icon for Heroicons' pause-circle and use the existing warning semantic color instead of a neutral or destructive state
- explain on hover or keyboard focus that agents are paused while memories and data remain safely preserved, with matching accessible text and localized copy in all 10 locales
- open the subscription recovery panel directly from the paused profile card while keeping the arrow button as the account-menu control

## Testing

- `pnpm exec vitest run tests/unit/components/UserCard.unit.spec.tsx tests/unit/components/UserMenu.unit.spec.tsx tests/unit/components/credits/CreditsDisplay.unit.spec.tsx` (123 passed)
- `bash scripts/verify-web.sh` (TypeScript and ESLint passed; the full unit run reported only a sandbox `listen EPERM` in the mock-backend socket test)
- `pnpm exec vitest run tests/unit/scripts/mock-backend-agent-builder.unit.spec.ts` outside the socket-restricted sandbox (34 passed)
- `bash scripts/verify-changed.sh`
- local browser verification that clicking the paused card opens the subscription panel and leaves the account menu closed
```
