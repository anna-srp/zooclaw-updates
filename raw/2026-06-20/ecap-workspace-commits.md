# ecap-workspace commits — 2026-06-20

共 2 个 commit

---

## `48377383eb`

- **作者**: tim-srp
- **日期**: 2026-06-20T14:38:26Z
- **PR**: #2539
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/48377383eb3a8dce3cd929a8a59f6cf47d616a6c

### 完整 commit message

```
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
```

### PR Description

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


---

## `8d3ada8f93`

- **作者**: bill-srp
- **日期**: 2026-06-20T02:57:06Z
- **PR**: #2525
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/8d3ada8f935f7c7b3f5f646c73c7fc0c77eccccd

### 完整 commit message

```
feat(account): gate web app with account session (#2525)

## Summary

- Add `AccountSessionGate` to verify `/account/me` before rendering
authenticated web app pages.
- Update landing auth redirect to validate server session state through
`/account/me`.
- Preserve the existing `UserBusinessDataProvider` and `/users/get` path
for the next PR in the stack.

## Stack

1. `codex/account-me-contract`: account/me contract + client service.
2. This PR: web app session gate on account/me.
3. `codex/web-remove-users-get`: remove web users/get dependency.

## Verification

- `bash scripts/verify-web.sh
web/app/src/components/AccountSessionGate.tsx
'web/app/src/app/[locale]/(app)/layout.tsx'
web/app/src/app/landing/hooks/useLandingAuthRedirect.ts
web/app/src/app/landing/hooks/useLandingRedirect.ts
web/app/sentry.client.config.ts
web/app/tests/unit/components/AccountSessionGate.unit.spec.tsx
web/app/tests/unit/app/app-group-layout.unit.spec.tsx
web/app/tests/unit/app/landing/hooks/useLandingAuthRedirect.unit.spec.ts
web/app/tests/unit/app/landing/hooks/useLandingRedirect.unit.spec.ts
web/app/tests/unit/config/sentry-client-config.unit.spec.ts`
```

### PR Description

## Summary

- Add `AccountSessionGate` to verify `/account/me` before rendering authenticated web app pages.
- Update landing auth redirect to validate server session state through `/account/me`.
- Preserve the existing `UserBusinessDataProvider` and `/users/get` path for the next PR in the stack.

## Stack

1. `codex/account-me-contract`: account/me contract + client service.
2. This PR: web app session gate on account/me.
3. `codex/web-remove-users-get`: remove web users/get dependency.

## Verification

- `bash scripts/verify-web.sh web/app/src/components/AccountSessionGate.tsx 'web/app/src/app/[locale]/(app)/layout.tsx' web/app/src/app/landing/hooks/useLandingAuthRedirect.ts web/app/src/app/landing/hooks/useLandingRedirect.ts web/app/sentry.client.config.ts web/app/tests/unit/components/AccountSessionGate.unit.spec.tsx web/app/tests/unit/app/app-group-layout.unit.spec.tsx web/app/tests/unit/app/landing/hooks/useLandingAuthRedirect.unit.spec.ts web/app/tests/unit/app/landing/hooks/useLandingRedirect.unit.spec.ts web/app/tests/unit/config/sentry-client-config.unit.spec.ts`

