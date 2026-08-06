---
title: "统一聊天中的用户头像显示"
type: "Bug Fix"
priority: "中"
date: "2026-08-05"
status: "待审核"
channels: ""
---

# 统一聊天中的用户头像显示

## 核心宣传点

聊天消息里的头像与右下角个人卡片保持一致，不会同一个人出现两种头像。

## 原始内容

- 仓库：`SerendipityOneInc/ecap-workspace`
- Commit：`19841fff6ee205bba69244e9ef9e0df3d045dde8`
- 作者：ericma-srp
- 日期：2026-08-05T07:58:15Z
- PR：#3247

### Commit Message

```
fix(web): align chat user avatar with profile card (#3247)

## Summary
- Align chat user-message avatars with the bottom-right profile card
avatar source.
- Reuse the same display-name fallback order and green gradient
presentation when no image is set.
- Keep replay-mode anonymity, reveal the matching fallback on image
errors, and recover when the reactive avatar URL changes.

## Root cause
The chat message avatar only read the Firebase `photoURL` and used a
separate email/phone fallback style. The profile card also reads the
reactive cached `userInfo.photoURL`, prefers the current display name,
and renders a branded gradient fallback, so the same user could appear
with different avatars on one page.

## Test plan
- [x] `vitest run tests/unit/app/chat/OpenClawUserMessage.unit.spec.tsx`
— 24 tests passed
- [x] `tsc --noEmit`
- [x] ESLint on the changed component and test
- [ ] `scripts/verify-web.sh` wrapper — local pnpm supply-chain
preflight is blocked by the existing `xlsx@0.20.3` lockfile entry
without integrity metadata; equivalent checks above passed using the
matching existing dependency tree

---------

Co-authored-by: eric <eric.ma@creatibi.com>
```

### PR Body

## Summary
- Align chat user-message avatars with the bottom-right profile card avatar source.
- Reuse the same display-name fallback order and green gradient presentation when no image is set.
- Keep replay-mode anonymity, reveal the matching fallback on image errors, and recover when the reactive avatar URL changes.

## Root cause
The chat message avatar only read the Firebase `photoURL` and used a separate email/phone fallback style. The profile card also reads the reactive cached `userInfo.photoURL`, prefers the current display name, and renders a branded gradient fallback, so the same user could appear with different avatars on one page.

## Test plan
- [x] `vitest run tests/unit/app/chat/OpenClawUserMessage.unit.spec.tsx` — 24 tests passed
- [x] `tsc --noEmit`
- [x] ESLint on the changed component and test
- [ ] `scripts/verify-web.sh` wrapper — local pnpm supply-chain preflight is blocked by the existing `xlsx@0.20.3` lockfile entry without integrity metadata; equivalent checks above passed using the matching existing dependency tree

