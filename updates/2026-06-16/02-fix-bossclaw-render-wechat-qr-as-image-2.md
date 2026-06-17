---
title: "Bossclaw 开通页微信二维码改为图片，手机长按可识别"
type: "体验优化"
priority: "低"
date: "2026-06-16"
status: "待审核"
channels: ""
---
# Bossclaw 开通页微信二维码改为图片，手机长按可识别
## 核心宣传点
Bossclaw 开通页的微信绑定二维码现在以真实图片展示，手机长按即可识别扫码，绑定更顺畅。
## 原始内容
fix(bossclaw): render wechat qr as image (#2496)

## Summary
- Render Bossclaw WeChat setup QR codes as real PNG image elements so
mobile long-press recognition works.
- Keep inline backend QR image URLs as direct image sources.
- Add unit coverage for generated and inline QR image rendering paths.

## Test plan
- `bash scripts/verify-web.sh
web/app/src/app/[locale]/bossclaw/components/WechatBindStep.tsx
web/app/src/app/[locale]/bossclaw/bossclaw.module.css
web/app/tests/unit/bossclaw/wechat-bind-step.unit.spec.tsx`
- Manual local smoke: `http://localhost:3000/zh/bossclaw` responds 200
with current branch running.

Co-authored-by: Developer <dev@srp.one>

---

## PR Description

## Summary
- Render Bossclaw WeChat setup QR codes as real PNG image elements so mobile long-press recognition works.
- Keep inline backend QR image URLs as direct image sources.
- Add unit coverage for generated and inline QR image rendering paths.

## Test plan
- `bash scripts/verify-web.sh web/app/src/app/[locale]/bossclaw/components/WechatBindStep.tsx web/app/src/app/[locale]/bossclaw/bossclaw.module.css web/app/tests/unit/bossclaw/wechat-bind-step.unit.spec.tsx`
- Manual local smoke: `http://localhost:3000/zh/bossclaw` responds 200 with current branch running.

