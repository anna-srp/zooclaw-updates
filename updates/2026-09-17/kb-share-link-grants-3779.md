---
title: "feat(kb): wire share-link installs into the kb grant domain (spec L0-L18) (#3779)"
type: "新功能"
priority: "中"
date: "2026-09-17"
status: "待审核"
channels: ""
---

# feat(kb): wire share-link installs into the kb grant domain (spec L0-L18) (#3779)

## 核心宣传点

分享链接安装 Agent 时会一并带上知识库授权，收到链接的人装完就能直接用作者挂的知识库，不用再手动补权限。

## PR 说明

## What

Implements the kb-share-link-grants spec (five review rounds, landed at `docs/superpowers/specs/2026-09-17-kb-share-link-grants.md` in this PR): v2 share-link installs now carry knowledge-base grants end to end, and the engine pack lifecycle's missing grant events + the reconcile cron's engine misjudgment are fixed. Companion PRs: SerendipityOneInc/ecap-proxy-service#199 (grant domain, **must deploy first**), SerendipityOneInc/ecap-agent-pack#255 (Studio guidance, releases only after this is live).

Background incident: a v2 agent shared via install link produced a copy that could not search the publisher's knowledge base — the share-link path had no grant wiring at all, and v2 definitions had no kb declaration surface to begin with.

## Clauses (test names = clause ids)

**L0 — declaration surface** (`test_kb_share_link_declaration.py`)
- `AgentSourceSnapshot.kb_ref` (optional `{kb_id}`, 32-hex), round-tripped through a top-level `agent.json` key; **agent.json unknown keys now fail loud** (a version-skewed platform must never silently drop a declaration — compat review P1-B5).
- L0.5: committing a revision that adds/changes/removes `kb_ref` while active share links exist returns `share_links_need_refresh` (installers receive the shared version; the binding refreshes when the owner publishes again).

**L6/L7b/L8 — share_service** (`test_kb_share_link_grants.py`)
- **publish() = the binding sync moment** (adapted from the spec's create_link wording after #3773's shared-version model landed — links now serve the shared revision, so publish is where content AND binding refresh together): declared kb registers the binding fail-closed (`agent_share.kb_not_authorized` / `kb_unavailable`); no declaration probes the binding (L5c) and unbinds a leftover one as owner intent (L5d, fail-closed on unbind failure, fail-open + alert on read failure).
- install: single-direction stale check (declared kb ≠ active binding → `agent_share.link_stale`; undeclared always admits — the healing path for historical links), then the grant event AFTER the install record, best-effort, source = the SOURCE definition id.

**L9/L16/L17/L18 — lifecycle + cron** (`test_kb_share_link_uninstall.py`, cron tests)
- New shared runtime-aware liveness predicate (`kb_grant_liveness`): engine rows hold grants by workspace status alone (they have no V1 computers-collection projection — production: cmp_-era rows failed the old check 0/276). Consumed by the reconcile cron's S7.2 check, V1 uninstall's last-holder check (fixing the "uninstalling a V1 copy revokes a live engine install's grant" misfire), and the new engine hook.
- Engine uninstall/delete: single post-terminal hook — pack rows revoke on last holder; shared_copy rows revoke the SOURCE grant on last live copy (cross-org, resolved through the install audit trail); source deletions touch nothing (L9b, pinned negative).
- Engine pack install fires the same install event as V1 (L16).
- Cron gains the shared_copy reconciliation segment (L10a), keyed (uid, source definition), revoked links included in provenance resolution.

**L11 — release audit (backfill endpoint withdrawn)**
- The one-shot backfill endpoint was removed after review (spec L10b/L11 second downgrade): its target population — links whose *published shared revision* declares `kb_ref` but whose binding is missing — is near-empty by release ordering (the declaration is undocumented until after gate-open, and L6 is fail-closed so declared publishes never end up half-registered). A privileged admin endpoint for a one-shot near-empty sweep wasn't worth its surface (it immediately drew an auth P0). Replacement: a read-only cross-DB audit at release (procedure in the spec, expected 0 rows); any hit heals via the owner republishing (L6 is idempotent).

**L12/L14/L15 — disclosure + web**
- `AgentInstallPreview.kb_access` resolved from the active binding (L5c), degrading to snapshot on read failure, null when positively unbound or the grant domain is unconfigured.
- Install page renders the disclosure section (zh/en); the three new error codes map to neutral localized copy (`link_stale` wording deliberately covers the owner's legitimate revocation). KB manage page needs no change — grant rows already render by source id.

## Gating & rollout

- **No rollout flag (spec §7 v6)**: proxy and workspace ship on the same train, so the deploy window the flag was built for does not exist — `KB_SHARE_LINK_GRANTS_ENABLED` is removed and the share-link wiring (L6/L7b/L8/L9/L10a/L12) is live with the deployment. The only gate is the existing `KB_GRANT_ADMIN_KEY` master config: unconfigured ⇒ best-effort paths no-op, cron skips, and a DECLARED publish still **fails closed** with `kb_unavailable` (F6 holds by construction — `register_pack_binding` raises when unconfigured; no flag check needed). Every environment deploying this code must therefore have the admin key configured and the proxy reachable.
- Wire compat: pack-namespace requests stay byte-identical; only agent_definition requests carry `source_kind` (old proxy 422s them → fail-closed). L5c reads treat ANY 404 as read-failure (old proxy's route-level 404 can never be misread as "no binding").
- **Deploy ordering is a hard constraint**: proxy #199 must be live before (or same-train-earlier than) this PR. Rollback: roll BOTH services together — proxy-alone rollback makes every declared publish fail closed (safe but user-visible); workspace-alone rollback leaves "status quo + frozen residual grants" (owner per-binding revocation on the KB manage page remains the safety valve). Production issues are handled by hotfix + data repair, not a behavior switch.
- **Release blockers (upgraded from post-launch items — there is no "deploy, verify, then flip" without a flag)**: ① staging encrypted-client (CSFLE) validation of the new query forms; ② the spec §7 staging E2E pass (declare → link → cross-org install → search hit → stale reject → unbind cascade → cron idempotency). Neither has run yet — this PR must not release before both do.

## Verification

- `verify-py` fully green (ruff / ruff-format / pyright / import-linter); cron queries are bounded single-collection reads + batch association (CSFLE contract; no aggregation pipelines). **Encrypted-client validation of the new query forms on staging is still required before release** per `services/claw-interface/AGENTS.md` — not claiming it passed.
- Unit suites green across the touched surface (new clause tests + all pre-existing sharing/lifecycle/cron/uninstall suites; the only local failures are the pre-existing `test_aiohttp_leak_debug` environment issue, identical on untouched main).
- Web: tsc/eslint clean on touched files; vitest passes (`kb-share-errors.unit.spec.ts`). Pre-existing tsc errors elsewhere come from the local node_modules being stale vs main — untouched by this PR.
- Staging E2E per spec §7 (declare → link → cross-org install → search hit → stale-link rejection → unbind cascade → cron idempotency) to run before release.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## Post-review amendments (adversarial code review F1-F7, commit 92cfcf48a)

- The release audit keys on the **shared** revision (what installs serve), never the active one — an unpublished declaration is not a missing binding.
- shared_copy grant liveness = **active** only, matching the pack path's predicate.
- Master gate off ⇒ declared publishes fail closed (F6, by construction).
- Engine uninstall grant hook sits outside the finalize try; cron's shared_copy segment honors batch_limit; owner-side publish errors surface localized copy.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `a52978e32e245a6d3cc64546d55930c75183c93a`
- PR: #3779
- 作者：kyle-srp
- 日期：2026-09-17T13:21:16Z

### Commit Message

```
feat(kb): wire share-link installs into the kb grant domain (spec L0-L18) (#3779)

## What

Implements the kb-share-link-grants spec (five review rounds, landed at
`docs/superpowers/specs/2026-09-17-kb-share-link-grants.md` in this PR):
v2 share-link installs now carry knowledge-base grants end to end, and
the engine pack lifecycle's missing grant events + the reconcile cron's
engine misjudgment are fixed. Companion PRs:
SerendipityOneInc/ecap-proxy-service#199 (grant domain, **must deploy
first**), SerendipityOneInc/ecap-agent-pack#255 (Studio guidance,
releases only after this is live).

Background incident: a v2 agent shared via install link produced a copy
that could not search the publisher's knowledge base — the share-link
path had no grant wiring at all, and v2 definitions had no kb
declaration surface to begin with.

## Clauses (test names = clause ids)

**L0 — declaration surface** (`test_kb_share_link_declaration.py`)
- `AgentSourceSnapshot.kb_ref` (optional `{kb_id}`, 32-hex),
round-tripped through a top-level `agent.json` key; **agent.json unknown
keys now fail loud** (a version-skewed platform must never silently drop
a declaration — compat review P1-B5).
- L0.5: commi
```
