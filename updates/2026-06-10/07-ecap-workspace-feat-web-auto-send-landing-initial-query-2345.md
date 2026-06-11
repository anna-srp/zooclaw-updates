---
title: "落地页首条提问自动发送"
type: "体验优化"
priority: "中"
date: "2026-06-10"
status: "待审核"
channels: ""
---
# 落地页首条提问自动发送

## 核心宣传点
从落地页带着问题进入对话后，系统会在切换到对应专家并就绪后自动发送首条提问，免去手动点击发送，首次互动更顺滑。

## 原始内容
```
feat(web): auto-send landing initial query (#2345)

## Linear

https://linear.app/srpone/issue/ECA-927/web-specialist-%E8%90%BD%E5%9C%B0%E9%A1%B5%E5%88%9D%E5%A7%8B-query-%E8%87%AA%E5%8A%A8%E5%8F%91%E9%80%81%E5%85%8D%E5%8E%BB%E7%94%A8%E6%88%B7%E6%89%8B%E5%8A%A8%E7%82%B9%E5%87%BB-send%E7%BC%A9%E7%9F%AD%E9%A6%96%E6%AC%A1%E4%BA%92%E5%8A%A8%E6%BC%8F%E6%96%97

## Summary
- Auto-send non-empty landing-context initial queries after the chat
switches to the target Specialist and the Mattermost channel is ready.
- Keep the existing composer prefill path as the retry fallback when
direct auto-send fails.
- Return send success/failure from the shared chat send path and cover
the landing/send behavior with unit tests.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web/app test:unit
tests/unit/hooks/useLandingContextFlow.unit.spec.ts
tests/unit/app/chat/useChatMessaging.unit.spec.ts
- [x] pnpm --dir web run test:unit --
tests/unit/hooks/useLandingContextFlow.unit.spec.ts
tests/unit/app/chat/useChatMessaging.unit.spec.ts

Note: pnpm --dir web run tsc currently fails locally before TypeScript
runs because the root script invokes pnpm exec with an unsupported
--if-present flag under pnpm 10.30.1; the touched app typecheck above
passes.

---

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-927/web-specialist-%E8%90%BD%E5%9C%B0%E9%A1%B5%E5%88%9D%E5%A7%8B-query-%E8%87%AA%E5%8A%A8%E5%8F%91%E9%80%81%E5%85%8D%E5%8E%BB%E7%94%A8%E6%88%B7%E6%89%8B%E5%8A%A8%E7%82%B9%E5%87%BB-send%E7%BC%A9%E7%9F%AD%E9%A6%96%E6%AC%A1%E4%BA%92%E5%8A%A8%E6%BC%8F%E6%96%97

## Summary
- Auto-send non-empty landing-context initial queries after the chat switches to the target Specialist and the Mattermost channel is ready.
- Keep the existing composer prefill path as the retry fallback when direct auto-send fails.
- Return send success/failure from the shared chat send path and cover the landing/send behavior with unit tests.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web/app test:unit tests/unit/hooks/useLandingContextFlow.unit.spec.ts tests/unit/app/chat/useChatMessaging.unit.spec.ts
- [x] pnpm --dir web run test:unit -- tests/unit/hooks/useLandingContextFlow.unit.spec.ts tests/unit/app/chat/useChatMessaging.unit.spec.ts

Note: pnpm --dir web run tsc currently fails locally before TypeScript runs because the root script invokes pnpm exec with an unsupported --if-present flag under pnpm 10.30.1; the touched app typecheck above passes.
```
