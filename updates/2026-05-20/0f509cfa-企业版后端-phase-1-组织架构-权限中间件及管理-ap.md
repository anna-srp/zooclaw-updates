---
title: "企业版后端 Phase 1：组织架构、权限中间件及管理 API"
type: "新功能上线"
priority: "中"
date: "2026-05-20"
status: "待审核"
channels: ""
repo: "ecap-workspace"
sha: "0f509cfa34b005b5b5aaf71f4ab2460f4edc26ef"
pr: 1748
---
# 企业版后端 Phase 1：组织架构、权限中间件及管理 API

## 核心宣传点

企业版后端基础架构完成，支持创建组织、设置权限和管理企业账户，为企业版功能全面上线奠定基础。

## 原始内容

### Commit Message

```
feat(enterprise): Phase 1 backend — Org schema, middleware, /orgs admin CRUD (#1748)

## Summary

First slice of the Enterprise Phase 1 backend (per
`docs/superpowers/specs/2026-05-19-enterprise-phase1-backend.md`). Lays
the foundation for multi-tenant Org abstraction:

- **Schemas**: `Org`, `AccountOrg`, `OrgSettings`, `BillingTeam`,
`OrgResponse` (+ `billing_user_key` on `Account`)
- **Repos** (typed Pydantic in/out): `org_repo`, `account_org_repo`
- **Middleware** (`app/middleware/`): `get_current_user` (V2-style auth
via `HTTPBearer`, returns typed `Account`) + org-scoped deps
`require_org_member` / `require_org_admin` / `get_current_org`
- **Service**: `org_service.create_org` / `get_org` / `update_settings`
(raises `ServiceError` subclasses; route stays transport-only)
- **Routes**: `/orgs` package at `app/routes/enterprise/org.py` — POST
(create), GET (read), POST/{id} (update settings). Returns `OrgResponse`
(strips internal `billing_team`).
- **Billing-gateway client groundwork**:
`billing_client.add_user_to_team` + typed `AddUserToTeamResponse` for
the upcoming join-org flow

## Design decisions (reflected in refactor commits)

- `Org.billing_team` **required** (every Org has a billing identity from
creation)
- `Org.settings` defaults to `None` (no explicit settings → fall back to
system defaults; distinct from a deliberate `OrgSettings()`)
- `org_id` is bare 32-char UUIDv4 hex (no prefix, no truncation)
- New repos return typed Pydantic models, not dicts (avoids the
historical `.model_dump()` shim debt)
- Repo `create()` is fire-and-forget (returns `None`; business PK lives
on the typed model)
- `mongo.update` / `mongo.delete` wrappers (3-arg, auto `\$set`) —
matches existing repo idioms
- Auth deps move to `dependencies=[Depends(...)]` on route decorators
when they're pure gates
- Internal billing identifiers (`billing_team`, `team_id`, `team_key`)
NEVER reach the frontend (`OrgResponse` strips; tests assert leakage
absence)

## NOT in this PR (follow-ups)

- **Wiring**: `/orgs` router not yet included in `create_app.py`
(S1-16). Routes exist but aren't reachable end-to-end.
- **Invite/join/suspend flow**: `/orgs/{org_id}/users/*` (S1-12 + S1-13
+ S1-15) — needs `InviteCodeCreateRequest` extension +
`membership_service`
- **Billing-gateway team provisioning**: external API to be added later;
for now `POST /orgs` accepts `billing_team` from the request body as a
TODO stub (admin-gated)
- **V2 user/agent API, migration, BDD step-defs**: later slices

## Test plan

- [ ] CI `python-code-quality / build-and-test` — pytest with MongoDB
service container (devcontainer-only locally; deferred to CI for this
slice)
- [ ] CI `auto-review`
- [ ] Manual: once S1-16 wires the router, `curl POST /orgs` with admin
auth + stub billing_team
- [ ] Spec coverage: §1.1, §1.2, §1.3 (billing_user_key), §2.2
(org/account_org repos), §3.2 (org CRUD), §3.5 (auth middleware)

## Spec drift

The committed spec (`c0037588`) is the *original* design; the code has
tightened it during implementation (33 design changes captured in the
refactor commits — see `9cb05028` plan doc for the historical context).
A doc reconciliation pass after PR merge will sync the spec to match the
code.
```

### PR Description

## Summary

First slice of the Enterprise Phase 1 backend (per `docs/superpowers/specs/2026-05-19-enterprise-phase1-backend.md`). Lays the foundation for multi-tenant Org abstraction:

- **Schemas**: `Org`, `AccountOrg`, `OrgSettings`, `BillingTeam`, `OrgResponse` (+ `billing_user_key` on `Account`)
- **Repos** (typed Pydantic in/out): `org_repo`, `account_org_repo`
- **Middleware** (`app/middleware/`): `get_current_user` (V2-style auth via `HTTPBearer`, returns typed `Account`) + org-scoped deps `require_org_member` / `require_org_admin` / `get_current_org`
- **Service**: `org_service.create_org` / `get_org` / `update_settings` (raises `ServiceError` subclasses; route stays transport-only)
- **Routes**: `/orgs` package at `app/routes/enterprise/org.py` — POST (create), GET (read), POST/{id} (update settings). Returns `OrgResponse` (strips internal `billing_team`).
- **Billing-gateway client groundwork**: `billing_client.add_user_to_team` + typed `AddUserToTeamResponse` for the upcoming join-org flow

## Design decisions (reflected in refactor commits)

- `Org.billing_team` **required** (every Org has a billing identity from creation)
- `Org.settings` defaults to `None` (no explicit settings → fall back to system defaults; distinct from a deliberate `OrgSettings()`)
- `org_id` is bare 32-char UUIDv4 hex (no prefix, no truncation)
- New repos return typed Pydantic models, not dicts (avoids the historical `.model_dump()` shim debt)
- Repo `create()` is fire-and-forget (returns `None`; business PK lives on the typed model)
- `mongo.update` / `mongo.delete` wrappers (3-arg, auto `\$set`) — matches existing repo idioms
- Auth deps move to `dependencies=[Depends(...)]` on route decorators when they're pure gates
- Internal billing identifiers (`billing_team`, `team_id`, `team_key`) NEVER reach the frontend (`OrgResponse` strips; tests assert leakage absence)

## NOT in this PR (follow-ups)

- **Wiring**: `/orgs` router not yet included in `create_app.py` (S1-16). Routes exist but aren't reachable end-to-end.
- **Invite/join/suspend flow**: `/orgs/{org_id}/users/*` (S1-12 + S1-13 + S1-15) — needs `InviteCodeCreateRequest` extension + `membership_service`
- **Billing-gateway team provisioning**: external API to be added later; for now `POST /orgs` accepts `billing_team` from the request body as a TODO stub (admin-gated)
- **V2 user/agent API, migration, BDD step-defs**: later slices

## Test plan

- [ ] CI `python-code-quality / build-and-test` — pytest with MongoDB service container (devcontainer-only locally; deferred to CI for this slice)
- [ ] CI `auto-review`
- [ ] Manual: once S1-16 wires the router, `curl POST /orgs` with admin auth + stub billing_team
- [ ] Spec coverage: §1.1, §1.2, §1.3 (billing_user_key), §2.2 (org/account_org repos), §3.2 (org CRUD), §3.5 (auth middleware)

## Spec drift

The committed spec (`c0037588`) is the *original* design; the code has tightened it during implementation (33 design changes captured in the refactor commits — see `9cb05028` plan doc for the historical context). A doc reconciliation pass after PR merge will sync the spec to match the code.
