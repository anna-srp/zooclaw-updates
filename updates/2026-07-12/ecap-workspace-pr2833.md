---
title: "一键分享你的 Agent Pack，好友跨组织免费安装"
type: "新功能上线"
priority: "高"
date: "2026-07-12"
status: "待审核"
channels: ""
---

## 核心宣传点

现在你可以把自己创建的 Agent Pack 一键分享出去——分享是即时生效的（无需等待商店审核），并且可以随时取消。任何已登录用户拿到分享链接后，都能跨组织免费安装你分享的 Pack，直接开箱即用。想收回也很简单，点一下「取消分享」即可。

## 原始内容

**Commit**: `f83d033385` feat(pack-store): share packs via is_shared flag instead of store listing (#2833)
**作者**: bill-srp | **日期**: 2026-07-12T06:56:35Z | **PR**: #2833

### Commit Message

```
feat(pack-store): share packs via is_shared flag instead of store listing (#2833)
```

### PR Body

# Description

Decouples pack sharing from the official ZooClaw store. The Publish page Share button no longer copies the pack into the ZooClaw org via `/public-listing`; instead it flips a new `is_shared` flag on the user's own pack. The public share page resolves shared packs by `pack_id` across orgs, and any logged-in user can install a shared pack cross-org, free of charge. Sharing is instant (no listing review) and reversible via a new Unshare action.

Design spec: `docs/superpowers/specs/2026-07-11-pack-share-is-shared-design.md`
Implementation plan: `docs/superpowers/plans/2026-07-11-pack-share-is-shared.md`

No Linear issue exists for this work (direct request).

## Backend (`services/claw-interface`)

- `Pack.is_shared: bool = False` (+ `SharedPackResponse.is_shared`); `pack_repo.set_is_shared` setter. No migration — absent field reads false.
- New `POST /orgs/{org_id}/packs/{pack_id}/share` and `POST .../unshare` (owner-org guarded, idempotent; share requires `status == "active"`, error `pack.share_requires_active`).
- New public route `GET /shared-packs/{pack_id}` (separate prefix — structurally can never conflict with `/agent-packs/{pack_id}/...`) serves flag-shared packs cross-org while `is_shared` and active. `GET /agent-packs/shared/{display_id}` is unchanged (legacy ZooClaw listing lookup, still used by the in-app hide-market detail fallback). Frontend consumers try by-id first, fall back to display_id on 404. `is_official` fixed to "ZooClaw org and no origin"; `requires_payment` masked false for flag-shared packs.
- `start_agent_install` (`source="private"`): fallback resolution by `pack_id` — own-org packs, or cross-org packs when `is_shared` and active; the agent token is rebound to `pack.display_id` so the display_id-keyed install pipeline is untouched. Cross-org non-shared packs 404 (no existence leak). No archive copy needed — `build_pack_archive_source` already serves any `asset_id` via the shared R2 packs domain.

## Frontend (`web/app`)

- Publish page: Share → `shareOrgPack` (confirm-only modal, success shows `/packs/{pack_id}` link); new Unshare action; card state derives from `is_shared`. Paid "List" flow (`createPaidListing`) untouched.
- Shared pack page: hire CTA deep-links flag-shared packs by `pack_id`; the agents-manager detail view model hires flag-shared packs with `{ id: pack_id, source: 'private' }`; legacy listings keep display_id + official-source behavior.
- Locale keys added for share-link/unshare strings across all 10 locales.

## Deployment / rollout

- **Backend must deploy before web** — the UI switches to the new `/share` endpoints. Cross-surface release (both `claw-interface` and `web`).
- The old `/public-listing` endpoint stays (paid List flow + existing data); Share simply stops calling it.
- Existing ZooClaw listings created by the old Share flow are untouched and keep serving.

## Known v1 limitations

- Cross-org install keys the workspace by the source pack's `display_id`. A collision with an already-installed same-named agent is **rejected** with `agent.agent_id_conflict` (no overwrite); installing two same-named shared packs side by side is not supported in v1.
- Retiring/migrating legacy ZooClaw public listings is a deferred follow-up.

# Test Plan

- [x] Frontend: full `bash scripts/verify-web.sh` — tsc + eslint + vitest (568 files, 7586 tests) green locally.
- [x] Backend: unit tests written per TDD plan (schema/repo/service/routes/shared-listing/install — 20+ new cases).
- [ ] Backend pytest + ruff + pyright run in CI (`python-code-quality`) — no local Python env on this host (macOS, backend runs devcontainer-only); CI is the authoritative backend gate for this PR.
- [ ] Staging smoke after deploy: share a pack → open `/packs/{pack_id}` logged-out → install from another org's account → unshare → page 404s.
