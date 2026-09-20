# SerendipityOneInc/ecap-workspace — commits 2026-09-19

## fix(invitation): redirect completed sign-in to home (#3799)

- **SHA**: `140a3590ddb94ef7be880d3d3d8124d936273f45`
- **作者**: tim-srp
- **日期**: 2026-09-19T09:31:20Z
- **PR**: #3799

### Commit Message

```
fix(invitation): redirect completed sign-in to home (#3799)
```

### PR Body

> Draft for a later main backport. Do not merge yet. Production hotfix is tracked in #3800, based on `ecap-v0.19.15-release`, and published as `ecap-v0.19.16-release` from `ef6d5fb9d`.

## Summary
- Route invitation registration completion and existing-user sign-in without a return target to the locale-aware Home page instead of Chat.
- Preserve existing-user explicit `return_to` navigation and the existing registration success delay.

## Root cause
The invitation flow defaulted to `/chat`, sending users directly into chat initialization instead of the intended `/home` entry point.

## Test plan
- [x] `bash scripts/verify-web.sh 'src/app/[locale]/invitation/login/useBossclawLoginFlow.ts' tests/unit/bossclaw/bossclaw-login-flow.unit.spec.ts`
- [x] All 20 login-flow tests pass, including new-user completion, existing-user sign-in, and explicit return targets.
- [x] TypeScript, ESLint, and frontend governance checks pass.

## Review assessment
The automated review flags new-user completion ignoring `return_to`. The base implementation already unconditionally navigated new users to `/${locale}/chat`; this PR only changes that destination to `/${locale}/home`, as requested. New-user return-target semantics are pre-existing and remain outside this narrow redirect change. Existing-user explicit return targets remain unchanged and covered by tests.


---
