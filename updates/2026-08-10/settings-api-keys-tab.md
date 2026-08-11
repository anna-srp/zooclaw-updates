---
title: "设置页新增 API Keys：自助创建与轮换服务令牌"
type: "新功能上线"
priority: "高"
date: "2026-08-10"
status: "待审核"
channels: ""
---

# 设置页新增 API Keys：自助创建与轮换服务令牌

## 核心宣传点

符合条件的用户可以在设置页自助创建、轮换和吊销组织服务令牌，用于程序化调用平台 API；密钥仅在创建时展示一次，安全可控。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `7b71f4fcb647505f1ba9e66c46ee72b5d6d3df73`
- PR: #3310

### Commit Message

```
feat(settings): add API Keys tab for org service tokens (#3310)

## Linear
<!-- no Linear issue for this change -->

## Summary
- Add an **API Keys** tab to the webapp settings page (`claw-settings`)
that manages org service tokens through the already-merged
claw-interface management API (`/orgs/{org_id}/service-tokens` create /
list / revoke / rebind, PRs #3272/#3274/#3276/#3284).
- Tab visibility requires BOTH gates: (1) the backend
`require_org_token_admin` mirror — personal-org members (owner) or
team-org admins, from `GET /account/me` (`org.org_type` / `org.role`);
and (2) server-authoritative **agents-v2 eligibility** — `GET
/agents/install-capability` must return `runtime: "engine"` (i.e.
`AGENTS_V2_ENABLED` on AND staging open-rollout or
`AGENTS_V2_EMAIL_ALLOWLIST` match). Capability loading/error states fail
closed; the capability query fires only when the org gate already
passes. New `useAgentInstallCapabilityQuery` hook (5-min staleTime)
added to the `hooks/queries/agents/` factory.
- Flows: create dialog (name, 1–100 chars) → one-time secret reveal
dialog with copy-to-clipboard and a "shown only once" warning; rotate
(`/rebind`) with confirmation → new one-time secret; revoke with
confirmation; loading / error / empty states. Revoked rows expose no
actions.
- Layering follows the repo conventions: `src/models/service-token.ts` →
`src/services/service-tokens.ts` (via the generic `callClawInterfaceAPI`
catch-all — no new BFF route) → `src/hooks/queries/service-tokens/`
(QUERY_VERSION-prefixed, org-scoped keys) → `ApiKeysTab.tsx` +
`useApiKeysController.ts`.
- Security constraint carried over from the backend design review: the
plaintext `zct_` token never passes through `useMutation` / the React
Query cache — create and rotate are direct service calls with the secret
held only in controller-local state and cleared when the reveal dialog
closes. Only revoke (no secret in the response path it consumes) uses
`useMutation`.
- UI uses `@zooclaw/design-system` components (Dialog, AlertDialog,
Alert, Badge, Button, Input, Label) + heroicons; en + zh strings added
(other locales fall back to English).

## Test plan
- [x] `bash scripts/verify-web.sh` — guards, tsc, vitest (8534 passed),
eslint all green
- [x] Unit specs added: service contract
(`service-tokens.unit.spec.ts`), query hook
(`useServiceTokensQuery.unit.spec.ts`), tab flows
(`ApiKeysTab.unit.spec.tsx`: metadata rendering, create validation,
one-time reveal + clear-on-close, copy, rotate confirm, revoke confirm +
list invalidation), and settings tab gating
(`ClawSettingsClient.unit.spec.tsx`)
- [ ] Staging smoke after backend release: create → call `/service/v1`
with the token → rotate (old plaintext 401s) → revoke
```

### PR Body

## Linear
<!-- no Linear issue for this change -->

## Summary
- Add an **API Keys** tab to the webapp settings page (`claw-settings`) that manages org service tokens through the already-merged claw-interface management API (`/orgs/{org_id}/service-tokens` create / list / revoke / rebind, PRs #3272/#3274/#3276/#3284).
- Tab visibility requires BOTH gates: (1) the backend `require_org_token_admin` mirror — personal-org members (owner) or team-org admins, from `GET /account/me` (`org.org_type` / `org.role`); and (2) server-authoritative **agents-v2 eligibility** — `GET /agents/install-capability` must return `runtime: "engine"` (i.e. `AGENTS_V2_ENABLED` on AND staging open-rollout or `AGENTS_V2_EMAIL_ALLOWLIST` match). Capability loading/error states fail closed; the capability query fires only when the org gate already passes. New `useAgentInstallCapabilityQuery` hook (5-min staleTime) added to the `hooks/queries/agents/` factory.
- Flows: create dialog (name, 1–100 chars) → one-time secret reveal dialog with copy-to-clipboard and a "shown only once" warning; rotate (`/rebind`) with confirmation → new one-time secret; revoke with confirmation; loading / error / empty states. Revoked rows expose no actions.
- Layering follows the repo conventions: `src/models/service-token.ts` → `src/services/service-tokens.ts` (via the generic `callClawInterfaceAPI` catch-all — no new BFF route) → `src/hooks/queries/service-tokens/` (QUERY_VERSION-prefixed, org-scoped keys) → `ApiKeysTab.tsx` + `useApiKeysController.ts`.
- Security constraint carried over from the backend design review: the plaintext `zct_` token never passes through `useMutation` / the React Query cache — create and rotate are direct service calls with the secret held only in controller-local state and cleared when the reveal dialog closes. Only revoke (no secret in the response path it consumes) uses `useMutation`.
- UI uses `@zooclaw/design-system` components (Dialog, AlertDialog, Alert, Badge, Button, Input, Label) + heroicons; en + zh strings added (other locales fall back to English).

## Test plan
- [x] `bash scripts/verify-web.sh` — guards, tsc, vitest (8534 passed), eslint all green
- [x] Unit specs added: service contract (`service-tokens.unit.spec.ts`), query hook (`useServiceTokensQuery.unit.spec.ts`), tab flows (`ApiKeysTab.unit.spec.tsx`: metadata rendering, create validation, one-time reveal + clear-on-close, copy, rotate confirm, revoke confirm + list invalidation), and settings tab gating (`ClawSettingsClient.unit.spec.tsx`)
- [ ] Staging smoke after backend release: create → call `/service/v1` with the token → rotate (old plaintext 401s) → revoke

