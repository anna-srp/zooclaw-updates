---
title: "Bossclaw 开通支持微信、企业微信、飞书多种绑定方式"
type: "新功能上线"
priority: "中"
date: "2026-06-20"
status: "待审核"
channels: "Discord+changelog"
---
# Bossclaw 开通支持微信、企业微信、飞书多种绑定方式
## 核心宣传点
Bossclaw 开通向导的绑定步骤现在支持在个人微信、企业微信（WeCom）和飞书之间切换，复用现有的 OpenClaw 频道设置与轮询接口，让不同渠道的用户都能顺利完成绑定开通。
## 原始内容
feat(bossclaw): support alternate bind channels (#2539)

## Linear

https://linear.app/srpone/issue/ECA-1035/bossclaw-onboarding-supports-wecom-and-feishu-bind-qr-options

## Summary
- Add Bossclaw bind-step channel switching for personal WeChat, WeCom,
and Feishu.
- Reuse existing OpenClaw channel setup, poll, and cancel APIs for the
alternate QR flows.
- Add focused Bossclaw unit coverage for default personal WeChat, WeCom
switching, and Feishu success polling.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web run test:unit
- [x] pnpm --dir web -r --workspace-concurrency=1 --if-present run tsc
- [x] pnpm --dir web --filter @zooclaw/web-app exec tsc --noEmit

## Notes
- `pnpm --dir web run tsc` currently fails because the package script
invokes `pnpm exec --if-present`, which this pnpm version rejects as
`Unknown option: 'if-present'`. Ran the equivalent workspace `run tsc`
command plus web-app `tsc --noEmit` directly.

## PR Description
## Linear
https://linear.app/srpone/issue/ECA-1035/bossclaw-onboarding-supports-wecom-and-feishu-bind-qr-options

## Summary
- Add Bossclaw bind-step channel switching for personal WeChat, WeCom, and Feishu.
- Reuse existing OpenClaw channel setup, poll, and cancel APIs for the alternate QR flows.
- Add focused Bossclaw unit coverage for default personal WeChat, WeCom switching, and Feishu success polling.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web run test:unit
- [x] pnpm --dir web -r --workspace-concurrency=1 --if-present run tsc
- [x] pnpm --dir web --filter @zooclaw/web-app exec tsc --noEmit

## Notes
- `pnpm --dir web run tsc` currently fails because the package script invokes `pnpm exec --if-present`, which this pnpm version rejects as `Unknown option: 'if-present'`. Ran the equivalent workspace `run tsc` command plus web-app `tsc --noEmit` directly.

