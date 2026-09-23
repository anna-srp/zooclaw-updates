---
title: "新增「从精选模板创建 Agent」：一键得到带技能与配置的专属 Agent"
type: "新功能上线"
priority: "高"
date: "2026-09-22"
status: "待审核"
channels: ""
---

# 新增「从精选模板创建 Agent」：一键得到带技能与配置的专属 Agent

## 核心宣传点

创建 Agent 现在多了一条路：除了自己写提示词和用别人分享的 Agent，还能直接挑一个官方精选模板。选中模板会为你生成一个完全属于你自己的独立 Agent，自带它原生的配置、Skills 和固定资产，不是共享副本。如果不想再改，创建完直接进入任务页开始用；想调整就走原来的 Build 流程继续定制。生成出来的 Agent 后续照常可以构建、分享，和手搓的 Agent 没有区别。底层做了目录与发布元数据、按账号维度的创建预留位，以及带摘要校验的源文件和资产存储——中途失败重试会复用同一份预留源，即使模板期间被下架也能把没建完的那次补齐。

## 分级

- 内部：P0
- 外部：S
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary

Create Agent now offers a curated template alongside the existing prompt
composer and shared-Agent entry. Selecting a template creates an
independent, user-owned Agent with its native configuration, Skills and
immutable assets. Creation without instructions opens Task; optional
customization starts the existing Build flow. The resulting Agent
continues through the normal Build and Share lifecycle.

- Store catalog/publication metadata and owner-scoped creation
reservations in Mongo; store digest-verified source and assets in the
dedicated R2 Agent Packs bucket. Retries reuse the reserved source,
including after a template is unpublished.
- Add an offline validation/import/publication CLI. No runtime GitHub
dependency or upstream synchronization; the production catalog remains a
separate launch decision.
- Preserve asset references through source edits and revisions.
Materialize asset-bearing Skills using signed Engine uploads, requested
in batches of at most 256 files before creating one complete version.
- Add the localized picker, mock fixtures, and operator/acceptance
documentation. Remove the redundant bottom blank card and keep the
template/shared cards aligned. The Deco acceptance sample is retained
locally and is not part of this PR.

## Test plan

- [x] Relevant backend lifecycle/template/asset suites: 489 passed
during implementation; latest creation-options/template/upload suite
after the review fix and schema extraction: 36 passed, including
255/256/257/512/513-file boundaries and mismatched later-batch tickets.
- [x] Frontend creation/dialog/initial-Build/mock suites: 49 passed
during implementation; latest template/dialog/share-navigation tests: 15
passed.
- [x] CI fixture follow-up: 48 backend startup/baseline/template/upload
tests passed. Startup mocks include the new index, the legacy digest
assertion excludes empty assets, and page-hook tests provide the query
context.
- [x] Backend Ruff, formatting, Pyright and eight import contracts;
frontend TypeScript, ESLint and governance guards. The worktree-local
Next ESLint plugin resolution was repaired without changing tracked
dependencies.
- [x] Mock-browser flows reached Task without instructions and Build
with instructions.
- [x] With explicit approval, imported/published the Deco fixture to
existing test Mongo/R2 and verified readback/digest. Its offline script
produced HTML/Markdown/JSON with correct budget totals; Chromium
rendered its embedded assets.
- [x] New repository operations verified with the real staging
`favie_common` client: CSFLE enabled, auto-encryption configured, bypass
disabled; index creation, sorted/paged listing, draft insertion,
duplicate recovery, unpublication, reservation retries and owner/org
isolation. Unique unpublished probes were removed and cleanup
independently verified.
- [ ] Real-model Task/Build execution and cross-account Share remain
release acceptance checks. Current local Engine lacks
designer/websearch; live shopping/image generation was not validated.

## Rollout

Deploy ECAP backend support before the frontend. Curate and publish the
production catalog separately after template acceptance. Retain
immutable R2 content after unpublication because existing Agents and
shared copies continue referencing it. No Engine or ACS source change is
required.

<details>
<summary>Encrypted Mongo validation receipt — 2026-09-22 UTC</summary>

Executed the new repository methods from this feature worktree using the
running local backend's existing staging environment and the unchanged
`favie_common.database.mongo_client.mongo` client. The probe asserted
`ENVIRONMENT == "staging"`, CSFLE enabled, auto-encryption options
present and bypass disabled before performing any writes. It used unique
`tpl_pr3857_probe_*` / `adw_pr3857_probe_*` records, synthetic owner/org
IDs and the published Deco source; probe templates were never published.

```text
environment staging
encryption_enabled True
auto_encryption_configured True
PASS: encrypted-client index creation, sorted/paged catalog, template/source readback
PASS: draft insert, duplicate-key readback, immutable conflict and unpublish update
PASS: reservation insert, duplicate retry, owner/org isolation and conflicting retries
PASS: only unique probe fixtures removed; cleanup verified
```

The reservation checks exercised `reserve_creation` twice with identical
input, readback with the original owner/org, rejection of changed
digest/owner on the same key, and absence for a different owner or org.
Cleanup used exact generated IDs plus owner/operator predicates,
followed by independent repository reads returning no record. The
published Deco template was unchanged. This is repository/CSFLE
evidence, not real-model or cross-account Share acceptance.

</details>

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `fbdf28616c3c34b43be1844b39b7e880240a5d44`
- PR: #3857
- 作者：kaka-srp
- 日期：2026-09-22T09:14:58Z

### Commit Message

```
feat(agents): create agents from curated offline templates (#3857)

## Summary

Create Agent now offers a curated template alongside the existing prompt
composer and shared-Agent entry. Selecting a template creates an
independent, user-owned Agent with its native configuration, Skills and
immutable assets. Creation without instructions opens Task; optional
customization starts the existing Build flow. The resulting Agent
continues through the normal Build and Share lifecycle.

- Store catalog/publication metadata and owner-scoped creation
reservations in Mongo; store digest-verified source and assets in the
dedicated R2 Agent Packs bucket. Retries reuse the reserved source,
including after a template is unpublished.
- Add an offline validation/import/publication CLI. No runtime GitHub
dependency or upstream synchronization; the production catalog remains a
separate launch decision.
- Preserve asset references through source edits and revisions.
Materialize asset-bearing Skills using signed Engine uploads, requested
in batches of at most 256 files before creating one complete version.
- Add the localized picker, mock fixtures, and operator/acceptance
documentation. Remove the redundant bottom blank card and keep the
template/shared cards aligned. The Deco acceptance sample is retained
locally and is not part of this PR.

## Test plan

- [x] Relevant backend lifecycle/template/asset suites: 489 passed
during implementation; latest creation-options/template/upload suite
after the review fix and schema extraction: 36 passed, including
255/256/257/512/513-file boundaries and mismatched later-batch tickets.
- [x] Frontend creation/dialog/initial-Build/mock suites: 49 passed
during implementation; latest template/dialog/share-navigation tests: 15
passed.
- [x] CI fixture follow-up: 48 backend startup/baseline/template/upload
tests passed. Startup mocks include the new index, the legacy digest
assertion excludes empty assets, and page-hook tests provide the query
context.
- [x] Backend Ruff, formatting, Pyright and eight import contracts;
frontend TypeScript, ESLint and governance guards. The worktree-local
Next ESLint plugin resolution was repaired without changing tracked
dependencies.
- [x] Mock-browser flows reached Task without instructions and Build
with instructions.
- [x] With explicit approval, imported/published the Deco fixture to
existing test Mongo/R2 and verified readback/digest. Its offline script
produced HTML/Markdown/JSON with correct budget totals; Chromium
rendered its embedded assets.
- [x] New repository operations verified with the real staging
`favie_common` client: CSFLE enabled, auto-encryption configured, bypass
disabled; index creation, sorted/paged listing, draft insertion,
duplicate recovery, unpublication, reservation retries and owner/org
isolation. Unique unpublished probes were removed and cleanup
independently verified.
- [ ] Real-model Task/Build execution and cross-account Share remain
release acceptance checks. Current local Engine lacks
designer/websearch; live shopping/image generation was not validated.

## Rollout

Deploy ECAP backend support before the frontend. Curate and publish the
production catalog separately after template acceptance. Retain
immutable R2 content after unpublication because existing Agents and
shared copies continue referencing it. No Engine or ACS source change is
required.

<details>
<summary>Encrypted Mongo validation receipt — 2026-09-22 UTC</summary>

Executed the new repository methods from this feature worktree using the
running local backend's existing staging environment and the unchanged
`favie_common.database.mongo_client.mongo` client. The probe asserted
`ENVIRONMENT == "staging"`, CSFLE enabled, auto-encryption options
present and bypass disabled before performing any writes. It used unique
`tpl_pr3857_probe_*` / `adw_pr3857_probe_*` records, synthetic owner/org
IDs and the published Deco source; probe templates were never published.

```text
environment staging
encryption_enabled True
auto_encryption_configured True
PASS: encrypted-client index creation, sorted/paged catalog, template/source readback
PASS: draft insert, duplicate-key readback, immutable conflict and unpublish update
PASS: reservation insert, duplicate retry, owner/org isolation and conflicting retries
PASS: only unique probe fixtures removed; cleanup verified
```

The reservation checks exercised `reserve_creation` twice with identical
input, readback with the original owner/org, rejection of changed
digest/owner on the same key, and absence for a different owner or org.
Cleanup used exact generated IDs plus owner/operator predicates,
followed by independent repository reads returning no record. The
published Deco template was unchanged. This is repository/CSFLE
evidence, not real-model or cross-account Share acceptance.

</details>
```

来源：SerendipityOneInc/ecap-workspace @ fbdf2861，PR #3857，作者 kaka-srp。
