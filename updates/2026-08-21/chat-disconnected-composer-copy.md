---
title: "修正断线/启动中时输入框的误导性提示文案"
type: "体验优化"
priority: "中"
date: "2026-08-21"
status: "待审核"
channels: ""
---

# 修正断线/启动中时输入框的误导性提示文案

## 核心宣传点

Agent 正在自动启动或重连时，输入框会提示你「去连接 Claw」——既用了早已废弃的旧叫法，又让人误以为需要自己动手操作一遍。现在 10 种语言的这段提示都换成了不点名具体运行时、也不暗示需要手动操作的中性文案，等待期间不会再被带偏。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `8de1900f5ae29c20160f5d43fcccb9ef8ee833a9`
- PR: #3472
- 作者: rayrain-srp
- 日期: 2026-08-21T12:07:11Z

### Commit Message

```
fix(chat): replace stale disconnected composer copy (#3472)

## Summary
- Replace `genClaw.inputDisabled` in all 10 supported locales with
connection-neutral copy that does not mention the stale Claw runtime
term or imply a manual connection step.
- Add regression coverage for both connecting/disconnected composer
states and for the exact copy in every supported locale.
- Linear:
https://linear.app/srpone/issue/ECA-1390/chat-copy-replace-stale-claw-wording-in-disconnected-composer

## Root cause
The shared v1/v2 `GenClawInput` composer still used legacy locale
strings that told users to connect to “Claw.” During automatic startup
or reconnect, that wording was both inconsistent with the current Agent
terminology and incorrectly suggested that users needed to take action.

## Test plan
- [x] `pnpm exec vitest run
tests/unit/app/chat/GenClawInput.unit.spec.tsx
tests/unit/locales/index.unit.spec.ts` (118 tests)
- [x] `bash scripts/verify-web.sh --no-test <changed files>` (governance
guards, TypeScript, ESLint)
- [x] Pre-commit frontend lint
- [x] Pre-push PR size and changed-surface verification
```

### PR Body

## Summary
- Replace `genClaw.inputDisabled` in all 10 supported locales with connection-neutral copy that does not mention the stale Claw runtime term or imply a manual connection step.
- Add regression coverage for both connecting/disconnected composer states and for the exact copy in every supported locale.
- Linear: https://linear.app/srpone/issue/ECA-1390/chat-copy-replace-stale-claw-wording-in-disconnected-composer

## Root cause
The shared v1/v2 `GenClawInput` composer still used legacy locale strings that told users to connect to “Claw.” During automatic startup or reconnect, that wording was both inconsistent with the current Agent terminology and incorrectly suggested that users needed to take action.

## Test plan
- [x] `pnpm exec vitest run tests/unit/app/chat/GenClawInput.unit.spec.tsx tests/unit/locales/index.unit.spec.ts` (118 tests)
- [x] `bash scripts/verify-web.sh --no-test <changed files>` (governance guards, TypeScript, ESLint)
- [x] Pre-commit frontend lint
- [x] Pre-push PR size and changed-surface verification

