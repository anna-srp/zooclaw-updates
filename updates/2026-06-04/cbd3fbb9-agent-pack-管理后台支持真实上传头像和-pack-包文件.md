---
title: "Agent Pack 管理后台支持真实上传头像和 Pack 包文件"
type: "产品基础功能更新"
priority: "低"
date: "2026-06-04"
status: "待审核"
channels: ""
sha: "cbd3fbb9fdab69ba5dcce340df898ef53870e87f"
repo: "ecap-workspace"
pr: "2217"
---

# Agent Pack 管理后台支持真实上传头像和 Pack 包文件

## 核心宣传点

内部管理后台现支持真实上传 Agent 头像和 Pack 压缩包，替代此前的模拟上传，发布流程更完整。

## 原始内容

### Commit Message

```
feat(dashboard-console): real R2 upload for avatars and pack archives (#2217)

## Linear
https://linear.app/srpone/issue/ECA-886

## Summary

Replace the mock avatar/pack-archive uploader with a real R2 upload path
(ECA-886 infrastructure). Mirrors enterprise-admin's `/api/r2/upload`,
adapted for React Router + the dashboard-console worker's network
constraints.

**Worker / R2 (`wrangler.jsonc`)**
- Bind `R2_PUBLIC_BUCKET`→`gem-image` (avatars) and
`R2_AGENT_PACKS_BUCKET`→`zooclaw-agent-packs` (pack archives) +
`R2_PUBLIC_DOMAIN`, in both the top-level (prod) and `env.staging`
blocks. Verified the bindings land in the build-generated
`build/server/wrangler.json`.

**Upload lib (`app/lib/r2/`)**
- Ported `key` (purpose→key) + `index` (`uploadToR2`, purpose→bucket
routing), refactored to take the Worker `env` as a parameter instead of
opennext's `getCloudflareContext()`.

**Resource route (`app/routes/api/r2-upload.ts`, registered in
`routes.ts`)**
- Headless POST `/api/r2/upload`, outside the auth-gate shell. Validates
the bearer token against the **public account service** (this worker
can't reach the internal claw-interface — that's why agent-packs are
fetched browser-side) and gates to `@srp.one`, then enforces the same
size/type/metadata rules as enterprise-admin (logo ≤2 MB
png/jpg/webp/svg; archive ≤100 MB `.zip` + `org_id`/`pack_id`).

**Client + wiring**
- `uploadFileToR2` now POSTs to the route (drops the mock);
`getAccountUser(token)` added for server-side token→account resolution.
- `use-view-model`: **live** writes do the real upload (archives now
send `org_id`/`pack_id` metadata); **seed/demo** stays offline (local
`objectURL` / synthetic key) so the no-backend demo still works.

`LIVE_WRITES_ENABLED` stays **off** — this lands the infrastructure
dormant; flipping it is the separate go-live switch.

## Test plan
- [x] Unit (+21 tests, 91 total): `lib/r2/key`, `lib/r2/index` (bucket
routing + public_url), the resource route
(401/403/size/type/metadata/happy paths), and the client (`POST` shape +
error propagation)
- [x] `pnpm run lint` + `pnpm run typecheck` clean
- [x] `react-router build` succeeds; generated
`build/server/wrangler.json` carries the R2 bindings +
`R2_PUBLIC_DOMAIN`
- [ ] Live upload exercised end-to-end once `LIVE_WRITES_ENABLED` flips
and the buckets are confirmed in the deploy account

## Notes
- The deploy worker needs the `gem-image` / `zooclaw-agent-packs`
buckets in the Cloudflare account — enterprise-admin already binds the
same names.
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-886

## Summary

Replace the mock avatar/pack-archive uploader with a real R2 upload path (ECA-886 infrastructure). Mirrors enterprise-admin's `/api/r2/upload`, adapted for React Router + the dashboard-console worker's network constraints.

**Worker / R2 (`wrangler.jsonc`)**
- Bind `R2_PUBLIC_BUCKET`→`gem-image` (avatars) and `R2_AGENT_PACKS_BUCKET`→`zooclaw-agent-packs` (pack archives) + `R2_PUBLIC_DOMAIN`, in both the top-level (prod) and `env.staging` blocks. Verified the bindings land in the build-generated `build/server/wrangler.json`.

**Upload lib (`app/lib/r2/`)**
- Ported `key` (purpose→key) + `index` (`uploadToR2`, purpose→bucket routing), refactored to take the Worker `env` as a parameter instead of opennext's `getCloudflareContext()`.

**Resource route (`app/routes/api/r2-upload.ts`, registered in `routes.ts`)**
- Headless POST `/api/r2/upload`, outside the auth-gate shell. Validates the bearer token against the **public account service** (this worker can't reach the internal claw-interface — that's why agent-packs are fetched browser-side) and gates to `@srp.one`, then enforces the same size/type/metadata rules as enterprise-admin (logo ≤2 MB png/jpg/webp/svg; archive ≤100 MB `.zip` + `org_id`/`pack_id`).

**Client + wiring**
- `uploadFileToR2` now POSTs to the route (drops the mock); `getAccountUser(token)` added for server-side token→account resolution.
- `use-view-model`: **live** writes do the real upload (archives now send `org_id`/`pack_id` metadata); **seed/demo** stays offline (local `objectURL` / synthetic key) so the no-backend demo still works.

`LIVE_WRITES_ENABLED` stays **off** — this lands the infrastructure dormant; flipping it is the separate go-live switch.

## Test plan
- [x] Unit (+21 tests, 91 total): `lib/r2/key`, `lib/r2/index` (bucket routing + public_url), the resource route (401/403/size/type/metadata/happy paths), and the client (`POST` shape + error propagation)
- [x] `pnpm run lint` + `pnpm run typecheck` clean
- [x] `react-router build` succeeds; generated `build/server/wrangler.json` carries the R2 bindings + `R2_PUBLIC_DOMAIN`
- [ ] Live upload exercised end-to-end once `LIVE_WRITES_ENABLED` flips and the buckets are confirmed in the deploy account

## Notes
- The deploy worker needs the `gem-image` / `zooclaw-agent-packs` buckets in the Cloudflare account — enterprise-admin already binds the same names.

