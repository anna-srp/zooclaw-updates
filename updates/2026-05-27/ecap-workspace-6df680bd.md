---
title: "注册流程新增数据合规确认弹窗"
type: "产品基础功能更新"
priority: "中"
date: "2026-05-27"
status: "待审核"
channels: ""
---

# 注册流程新增数据合规确认弹窗

## 核心宣传点

用户注册时会看到数据合规权限确认提示，让您对自己的数据使用更加透明和放心。

## 原始内容

**仓库**: SerendipityOneInc/ecap-workspace  
**SHA**: [6df680bd](https://github.com/SerendipityOneInc/ecap-workspace/commit/6df680bda6e385518e82566a6e633ae02a149d8b)
**PR**: [#1980](https://github.com/SerendipityOneInc/ecap-workspace/pull/1980)  
**作者**: bill-srp  
**日期**: 2026-05-27T09:59:55Z

**Commit Message:**

```
feat(settings): add data compliance permissions (#1980)

## Linear

https://linear.app/srpone/issue/ECA-839/zooclaw%E6%B3%A8%E5%86%8C%E9%A1%B5%E9%9D%A2%E5%A2%9E%E5%8A%A0%E6%95%B0%E6%8D%AE%E5%90%88%E8%A7%84%E7%A1%AE%E8%AE%A4%E5%BC%B9%E7%AA%97

## Summary
- Add settings data compliance permission rows with persisted checkbox
preferences
- Add the user-facing preferences update API route
- Preserve sequential consent updates by saving the full data compliance
consent snapshot each time
- Align web/app backend configuration on CLAW_INTERFACE_URL while
allowing deploy to source it from existing BACKEND_URL vars until
external config is renamed

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web run test:unit
- [x] pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/components/settings/GeneralTab.unit.spec.tsx
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit
- [x] pnpm --dir web/packages/auth-client exec tsc --noEmit
- [ ] pnpm --dir web run tsc (blocked locally: script passes unsupported
--if-present to pnpm exec)
```


**PR Description:**

## Linear
https://linear.app/srpone/issue/ECA-839/zooclaw%E6%B3%A8%E5%86%8C%E9%A1%B5%E9%9D%A2%E5%A2%9E%E5%8A%A0%E6%95%B0%E6%8D%AE%E5%90%88%E8%A7%84%E7%A1%AE%E8%AE%A4%E5%BC%B9%E7%AA%97

## Summary
- Add settings data compliance permission rows with persisted checkbox preferences
- Add the user-facing preferences update API route
- Preserve sequential consent updates by saving the full data compliance consent snapshot each time
- Align web/app backend configuration on CLAW_INTERFACE_URL while allowing deploy to source it from existing BACKEND_URL vars until external config is renamed

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web run test:unit
- [x] pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/components/settings/GeneralTab.unit.spec.tsx
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit
- [x] pnpm --dir web/packages/auth-client exec tsc --noEmit
- [ ] pnpm --dir web run tsc (blocked locally: script passes unsupported --if-present to pnpm exec)
