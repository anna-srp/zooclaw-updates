---
title: "Bossclaw 微信绑定流程更清晰：可返回上一步、二维码长按识别、绑定成功有提示"
type: "体验优化"
priority: "中"
date: "2026-06-17"
status: "待审核"
channels: "Discord+changelog"
---
# Bossclaw 微信绑定流程更清晰：可返回上一步、二维码长按识别、绑定成功有提示
## 核心宣传点
Bossclaw 开通向导新增「返回上一步」按钮，微信绑定页提示改为长按二维码识别（不必再截图保存），并新增绑定成功确认引导（看到 WeixinClawBot 出现即代表绑定成功），整个开通流程更顺、更不易卡住。
## 原始内容
fix(bossclaw): clarify wechat binding flow (#2509)

## Summary
- add a back button for BossClaw app steps so users can return to the
previous step
- update the WeChat bind copy to tell users to long-press the QR code
instead of saving a screenshot
- add a confirmation guide showing that `WeixinClawBot` appearing in
WeChat means binding succeeded

## Local validation
- `git diff --check` passed
- `curl http://localhost:3000/zh/bossclaw` returned 200
- `bash scripts/verify-web.sh
web/app/src/app/[locale]/bossclaw/BossclawClient.tsx
web/app/src/app/[locale]/bossclaw/components/WechatBindStep.tsx
web/app/src/app/[locale]/bossclaw/bossclaw.module.css` partially passed:
guards, vitest, and eslint passed; global `tsc` is blocked by existing
`src/app/[locale]/(app)/(chat)/chat/components/GenClawInput.tsx` missing
`ldrs/react` type resolution in this local checkout

---------

Co-authored-by: Developer <dev@srp.one>

## PR Description
## Summary
- add a back button for BossClaw app steps so users can return to the previous step
- update the WeChat bind copy to tell users to long-press the QR code instead of saving a screenshot
- add a confirmation guide showing that `WeixinClawBot` appearing in WeChat means binding succeeded

## Local validation
- `git diff --check` passed
- `curl http://localhost:3000/zh/bossclaw` returned 200
- `bash scripts/verify-web.sh web/app/src/app/[locale]/bossclaw/BossclawClient.tsx web/app/src/app/[locale]/bossclaw/components/WechatBindStep.tsx web/app/src/app/[locale]/bossclaw/bossclaw.module.css` partially passed: guards, vitest, and eslint passed; global `tsc` is blocked by existing `src/app/[locale]/(app)/(chat)/chat/components/GenClawInput.tsx` missing `ldrs/react` type resolution in this local checkout

