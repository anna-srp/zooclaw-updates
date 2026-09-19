---
title: "style(chat): apply warm B2 billing notice design (#3807)"
type: "体验优化"
priority: "中"
date: "2026-09-18"
status: "待审核"
channels: ""
---

# 聊天里的额度提示换成更柔和的卡片样式

## 核心宣传点

输入框上方原来那条红色报错式的额度横幅换成了选定的 B2 设计：奶油底色卡片、暖色额度图标、标题和说明分行，充值按钮改成描边样式，深色主题有配套配色，窄容器下会自动换行。行为和 #3795 一致：点充值打开原有订阅面板，余额恢复后提示自动消失，历史对话里的报错仍然保留。

## 分级

- 内部：P2
- 外部：C
- 发布状态：已合并待发版

## PR 说明

## Summary
Replace the destructive billing banner above the chat composer with the selected B2 design: a soft cream card, warm credits icon, separate title and supporting text, and an outlined recharge button. Include matching dark-theme colors and a wrapping layout for narrow containers.

Keep billing behavior from #3795 unchanged: recharge opens the existing subscription panel, a confirmed balance recovery removes the notice, and historical assistant errors remain in the conversation. No API, ACS, or Engine changes.

## Test plan
- [x] TypeScript type check.
- [x] ChatBillingNotice unit tests: 6 passed, including balance recovery, recharge, and subscription copy.
- [x] ESLint on changed component, translations, and tests; formatting and diff checks.
- Initial verification included translation basenames as test filters and unintentionally selected unrelated suites; that run was stopped and replaced with the focused component suite. No full-suite success is claimed.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `5cce8f3b6aeb2dc2ce8583be7e2a2c218903b1d9`
- PR: #3807
- 作者：tim-srp
- 日期：2026-09-18T11:53:56Z

### Commit Message

```
style(chat): apply warm B2 billing notice design (#3807)

## Summary
Replace the destructive billing banner above the chat composer with the
selected B2 design: a soft cream card, warm credits icon, separate title
and supporting text, and an outlined recharge button. Include matching
dark-theme colors and a wrapping layout for narrow containers.

Keep billing behavior from #3795 unchanged: recharge opens the existing
subscription panel, a confirmed balance recovery removes the notice, and
historical assistant errors remain in the conversation. No API, ACS, or
Engine changes.

## Test plan
- [x] TypeScript type check.
- [x] ChatBillingNotice unit tests: 6 passed, including balance
recovery, recharge, and subscription copy.
- [x] ESLint on changed component, translations, and tests; formatting
and diff checks.
- Initial verification included translation basenames as test filters
and unintentionally selected unrelated suites; that run was stopped and
replaced with the focused component suite. No full-suite success is
claimed.
```

## 备注

发布状态：已合并待发版（尚未包含在任何 ecap-*-release tag 中，最新正式 release 为 ecap-v0.19.16-release）。

来源：SerendipityOneInc/ecap-workspace @ 5cce8f3b，PR #3807，作者 tim-srp。
