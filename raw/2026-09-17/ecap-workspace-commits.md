# SerendipityOneInc/ecap-workspace — commits 2026-09-17

## feat(kb): wire share-link installs into the kb grant domain (spec L0-L18) (#3779)

- **SHA**: `a52978e32e245a6d3cc64546d55930c75183c93a`
- **作者**: kyle-srp
- **日期**: 2026-09-17T13:21:16Z
- **PR**: #3779

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
- L0.5: committing a revision that adds/changes/removes `kb_ref` while
active share links exist returns `share_links_need_refresh` (installers
receive the shared version; the binding refreshes when the owner
publishes again).

**L6/L7b/L8 — share_service** (`test_kb_share_link_grants.py`)
- **publish() = the binding sync moment** (adapted from the spec's
create_link wording after #3773's shared-version model landed — links
now serve the shared revision, so publish is where content AND binding
refresh together): declared kb registers the binding fail-closed
(`agent_share.kb_not_authorized` / `kb_unavailable`); no declaration
probes the binding (L5c) and unbinds a leftover one as owner intent
(L5d, fail-closed on unbind failure, fail-open + alert on read failure).
- install: single-direction stale check (declared kb ≠ active binding →
`agent_share.link_stale`; undeclared always admits — the healing path
for historical links), then the grant event AFTER the install record,
best-effort, source = the SOURCE definition id.

**L9/L16/L17/L18 — lifecycle + cron**
(`test_kb_share_link_uninstall.py`, cron tests)
- New shared runtime-aware liveness predicate (`kb_grant_liveness`):
engine rows hold grants by workspace status alone (they have no V1
computers-collection projection — production: cmp_-era rows failed the
old check 0/276). Consumed by the reconcile cron's S7.2 check, V1
uninstall's last-holder check (fixing the "uninstalling a V1 copy
revokes a live engine install's grant" misfire), and the new engine
hook.
- Engine uninstall/delete: single post-terminal hook — pack rows revoke
on last holder; shared_copy rows revoke the SOURCE grant on last live
copy (cross-org, resolved through the install audit trail); source
deletions touch nothing (L9b, pinned negative).
- Engine pack install fires the same install event as V1 (L16).
- Cron gains the shared_copy reconciliation segment (L10a), keyed (uid,
source definition), revoked links included in provenance resolution.

**L11 — release audit (backfill endpoint withdrawn)**
- The one-shot backfill endpoint was removed after review (spec L10b/L11
second downgrade): its target population — links whose *published shared
revision* declares `kb_ref` but whose binding is missing — is near-empty
by release ordering (the declaration is undocumented until after
gate-open, and L6 is fail-closed so declared publishes never end up
half-registered). A privileged admin endpoint for a one-shot near-empty
sweep wasn't worth its surface (it immediately drew an auth P0).
Replacement: a read-only cross-DB audit at release (procedure in the
spec, expected 0 rows); any hit heals via the owner republishing (L6 is
idempotent).

**L12/L14/L15 — disclosure + web**
- `AgentInstallPreview.kb_access` resolved from the active binding
(L5c), degrading to snapshot on read failure, null when positively
unbound or the grant domain is unconfigured.
- Install page renders the disclosure section (zh/en); the three new
error codes map to neutral localized copy (`link_stale` wording
deliberately covers the owner's legitimate revocation). KB manage page
needs no change — grant rows already render by source id.

## Gating & rollout

- **No rollout flag (spec §7 v6)**: proxy and workspace ship on the same
train, so the deploy window the flag was built for does not exist —
`KB_SHARE_LINK_GRANTS_ENABLED` is removed and the share-link wiring
(L6/L7b/L8/L9/L10a/L12) is live with the deployment. The only gate is
the existing `KB_GRANT_ADMIN_KEY` master config: unconfigured ⇒
best-effort paths no-op, cron skips, and a DECLARED publish still
**fails closed** with `kb_unavailable` (F6 holds by construction —
`register_pack_binding` raises when unconfigured; no flag check needed).
Every environment deploying this code must therefore have the admin key
configured and the proxy reachable.
- Wire compat: pack-namespace requests stay byte-identical; only
agent_definition requests carry `source_kind` (old proxy 422s them →
fail-closed). L5c reads treat ANY 404 as read-failure (old proxy's
route-level 404 can never be misread as "no binding").
- **Deploy ordering is a hard constraint**: proxy #199 must be live
before (or same-train-earlier than) this PR. Rollback: roll BOTH
services together — proxy-alone rollback makes every declared publish
fail closed (safe but user-visible); workspace-alone rollback leaves
"status quo + frozen residual grants" (owner per-binding revocation on
the KB manage page remains the safety valve). Production issues are
handled by hotfix + data repair, not a behavior switch.
- **Release blockers (upgraded from post-launch items — there is no
"deploy, verify, then flip" without a flag)**: ① staging
encrypted-client (CSFLE) validation of the new query forms; ② the spec
§7 staging E2E pass (declare → link → cross-org install → search hit →
stale reject → unbind cascade → cron idempotency). Neither has run yet —
this PR must not release before both do.

## Verification

- `verify-py` fully green (ruff / ruff-format / pyright /
import-linter); cron queries are bounded single-collection reads + batch
association (CSFLE contract; no aggregation pipelines).
**Encrypted-client validation of the new query forms on staging is still
required before release** per `services/claw-interface/AGENTS.md` — not
claiming it passed.
- Unit suites green across the touched surface (new clause tests + all
pre-existing sharing/lifecycle/cron/uninstall suites; the only local
failures are the pre-existing `test_aiohttp_leak_debug` environment
issue, identical on untouched main).
- Web: tsc/eslint clean on touched files; vitest passes
(`kb-share-errors.unit.spec.ts`). Pre-existing tsc errors elsewhere come
from the local node_modules being stale vs main — untouched by this PR.
- Staging E2E per spec §7 (declare → link → cross-org install → search
hit → stale-link rejection → unbind cascade → cron idempotency) to run
before release.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## Post-review amendments (adversarial code review F1-F7, commit
92cfcf48a)

- The release audit keys on the **shared** revision (what installs
serve), never the active one — an unpublished declaration is not a
missing binding.
- shared_copy grant liveness = **active** only, matching the pack path's
predicate.
- Master gate off ⇒ declared publishes fail closed (F6, by
construction).
- Engine uninstall grant hook sits outside the finalize try; cron's
shared_copy segment honors batch_limit; owner-side publish errors
surface localized copy.

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

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




---

## fix(agents): persist exact environment pins in revisions (#3782)

- **SHA**: `2527b959c2b01aa86e1225a8d4133e696cabcd49`
- **作者**: kaka-srp
- **日期**: 2026-09-17T12:49:49Z
- **PR**: #3782

### Commit Message

```
fix(agents): persist exact environment pins in revisions (#3782)

## Summary

- Persist Engine's actual resolved environment ID/version in the initial
Agent Revision.
- Require exact pins when reusing a Revision or rendering
Build/Settings/Preview/Apply candidates; never implicitly reselect the
latest environment during an ordinary edit.
- Materialize an explicit environment when the last custom dependencies
are removed, and retain the existing explicit-rebuild protection.
- Keep legacy data repair offline and out of this PR. Only in-use Agents
are in scope for the separate repair; uninstalled Agents are excluded.

## Root cause

Default-environment creation let Engine resolve a concrete version, but
R0 persisted the original null input rather than the resolved pin.
Subsequent metadata-only edits inherited null and could resolve a newer
default. Once a sandbox locked the old environment, activation correctly
rejected that accidental upgrade with `environment_rebuild_required`.

## Review

Completed the `code-review` workflow against `origin/main`:
design/scope, completeness/reliability, and regressions/side effects.
Checked every candidate-rendering caller, initial creation/retries,
inherited pending Revision pins, and shared updates.

Follow-up automated review found a real missing guard: legacy source
Revisions with null pins could still enter shared install/link copy/fork
as a fresh default-environment creation. Fixed the common
`system_environment_version` boundary to reject incomplete pins,
including custom-environment sources. Fork validates before its durable
reservation as well, so invalid source cannot leave a failed empty copy.
Added install/copy/fork regression assertions (including no reservation
on rejection) and re-reviewed the correction.

The separate question about asynchronous default resolution was checked
against Engine source: `createAgentTx` awaits `resolveAgentEnvironment`
and `renderConfig`, then stores the rendered config and environment pin
in the creation transaction; Agent detail projects
`resolved_environment` from that persisted rendered config. No new
polling/fallback is needed.

## Test plan

- [x] Agent development, baseline, shared-update, authoring-operation,
shared-link-copy, and adopted-sharing unit suites: **459 passed**.
- [x] Final pre-reservation correction: **61 directly affected tests
passed**.
- [x] `bash scripts/verify-local.sh --py-static`: Ruff, format, Pyright,
and import contracts pass.
- [x] Pre-commit checks pass, including file length, complexity,
dependency consistency, repository contracts, and type checks.
- [x] Regression assertions for R0 resolved-pin persistence, exact
inheritance in commit/preview/apply retry, null/partial pin rejection,
and dependency removal.
- [ ] CI on the PR merge ref.
- [ ] Deployment and live smoke verification (not performed by this PR).

## Rollout boundary

Backend-only change; no Engine or frontend deployment dependency. Before
enabling the strict guard on existing in-use Agents, complete the
separately authorized offline pin backfill using exact immutable config
evidence. Coordinate rollout/backfill so the old writer does not leave
new incomplete records. Without backfill, an incomplete legacy Revision
will fail closed rather than silently upgrade.

No production data, sandbox, or active runtime configuration was
modified in preparing this PR. General Build rebuild-confirmation UX and
async image continuation's turn-to-Revision lookup are separate work,
not claimed fixed here.
```

### PR Body

## Summary

- Persist Engine's actual resolved environment ID/version in the initial Agent Revision.
- Require exact pins when reusing a Revision or rendering Build/Settings/Preview/Apply candidates; never implicitly reselect the latest environment during an ordinary edit.
- Materialize an explicit environment when the last custom dependencies are removed, and retain the existing explicit-rebuild protection.
- Keep legacy data repair offline and out of this PR. Only in-use Agents are in scope for the separate repair; uninstalled Agents are excluded.

## Root cause

Default-environment creation let Engine resolve a concrete version, but R0 persisted the original null input rather than the resolved pin. Subsequent metadata-only edits inherited null and could resolve a newer default. Once a sandbox locked the old environment, activation correctly rejected that accidental upgrade with `environment_rebuild_required`.

## Review

Completed the `code-review` workflow against `origin/main`: design/scope, completeness/reliability, and regressions/side effects. Checked every candidate-rendering caller, initial creation/retries, inherited pending Revision pins, and shared updates.

Follow-up automated review found a real missing guard: legacy source Revisions with null pins could still enter shared install/link copy/fork as a fresh default-environment creation. Fixed the common `system_environment_version` boundary to reject incomplete pins, including custom-environment sources. Fork validates before its durable reservation as well, so invalid source cannot leave a failed empty copy. Added install/copy/fork regression assertions (including no reservation on rejection) and re-reviewed the correction.

The separate question about asynchronous default resolution was checked against Engine source: `createAgentTx` awaits `resolveAgentEnvironment` and `renderConfig`, then stores the rendered config and environment pin in the creation transaction; Agent detail projects `resolved_environment` from that persisted rendered config. No new polling/fallback is needed.

## Test plan

- [x] Agent development, baseline, shared-update, authoring-operation, shared-link-copy, and adopted-sharing unit suites: **459 passed**.
- [x] Final pre-reservation correction: **61 directly affected tests passed**.
- [x] `bash scripts/verify-local.sh --py-static`: Ruff, format, Pyright, and import contracts pass.
- [x] Pre-commit checks pass, including file length, complexity, dependency consistency, repository contracts, and type checks.
- [x] Regression assertions for R0 resolved-pin persistence, exact inheritance in commit/preview/apply retry, null/partial pin rejection, and dependency removal.
- [ ] CI on the PR merge ref.
- [ ] Deployment and live smoke verification (not performed by this PR).

## Rollout boundary

Backend-only change; no Engine or frontend deployment dependency. Before enabling the strict guard on existing in-use Agents, complete the separately authorized offline pin backfill using exact immutable config evidence. Coordinate rollout/backfill so the old writer does not leave new incomplete records. Without backfill, an incomplete legacy Revision will fail closed rather than silently upgrade.

No production data, sandbox, or active runtime configuration was modified in preparing this PR. General Build rebuild-confirmation UX and async image continuation's turn-to-Revision lookup are separate work, not claimed fixed here.


---

## fix(workspace): 修复 R2 工作台交互并统一资源页面样式 (#3781)

- **SHA**: `9f76a4995c0ff94c6e7b655497eaf04c0f02d57c`
- **作者**: lynn Zhuang
- **日期**: 2026-09-17T11:52:25Z
- **PR**: #3781

### Commit Message

```
fix(workspace): 修复 R2 工作台交互并统一资源页面样式 (#3781)

## 修改内容

修复 R2 验收中首页、Agent 工作区和资源页面的展示与导航问题。从首页首次进入可编辑 Agent 时打开 Edit Agent
并展示设置面板；再次进入时，按用户和 Agent 恢复浏览器本地记录的编辑页、New Task 或具体任务对话。

- Skills：输入框 Skill Store 与侧边栏 Official Skills 使用同一目录及图标；移除 Use Skills
子菜单中的重复列表，仅保留创建和打开商店入口；去掉商店弹窗上下分割线。
- 首页：最近活动过滤没有实际标题的空任务；Schedule 加载失败使用独立、准确的提示；Agent
卡片缩短、描述限制单行，头像放大并上移至卡片边缘；缩小 Agent Builder 图标。
- Agent 工作区：标题显示当前页面或任务名称；统一侧边栏悬停样式、返回按钮和切换器，优化 Recents 空状态；Artifacts
复用全局页面及空状态，并分别按 workspace ID / runtime agent ID 筛选生成文件和上传文件。
- Schedule 与
Knowledge：移除无关连接状态和重复标题；日历改为浅灰底，修正分割线、按钮及筛选器样式，列表筛选不再影响日历；修复 Agent
日程空状态被其他运行环境状态遮蔽的问题。Knowledge 标题与侧边栏一致，创建弹窗不再导致背景提前显示空的 Unfiled
卡片，移除空状态中的未归档上传入口。
- Tasks 与 Agents：任务整行可进入聊天，保留原生链接行为；去掉 Tasks 顶部 Refresh；新增默认 All
标签，各分类分页独立。Agent 入口记录不覆盖明确指定的任务链接，失效的已记忆任务可回退到 New Task。

- 页面头部：以 Connector 为基准，统一 Agents / Tasks / Artifacts / MCP / Skills /
Knowledge，以及 Agent 内的 Artifacts / Schedule / External
channels；标题、说明、宽度和留白复用同一组件。Credits 异常提示缩小并改为灰色。补齐本地 mock 的 Agent 详情接口，避免
External channels 请求 undefined。

## 问题原因

Skill Store 仍使用旧目录；首页直接把底层空会话当作活动；资源页复用了带运行环境连接状态的聊天标题组件。Agent
入口缺少本地停留位置记录，工作区与全局页面也存在重复组件及样式差异。

## 验证结果

- [x] 最新提交 `f9255fffb` 的 CI：26 项通过、15 项按条件跳过，无失败或等待项；Claude 与 Codex
对该提交复审均无新增问题。
- [x] 后端任务详情与历史列表定向测试：61 项通过。新增飞书 / Slack 原始标题为空、当前任务不在首批 50
条历史记录中的回归用例；修复前 4 个用例失败，修复后全部通过。
- [x] 后端 ruff、格式检查、Pyright 与 import-linter 全部通过；提交钩子检查通过。

- [x] Agent、Tasks 与首页相关单测：59 个文件、398 项通过（同步最新 main 后重新执行）。
- [x] chat-ui 的 SkillsSubMenu / SkillStoreDialog：20 项通过。
- [x] 本轮已验证 Skills、Knowledge、Artifacts、Schedule 相关定向测试。
- [x] 头部调整后定向测试：40 项通过；资源页、渠道和日程回归：154 项通过（既有 69 项跳过、1 项 todo）。
- [x] 浏览器核对：全局及 Agent 资源页标题均为 16px / 600，桌面顶部留白 24px；Credits 提示
12px；渠道页无 undefined 请求错误。
- [x] 同步最新 Agent 面板改动后，入口和工作区回归：54 个文件、392 项通过，保留面板优化及首次编辑/后续恢复行为。
- [x] TypeScript、ESLint、仓库治理检查、Knip 与 `git diff --check`。
- [x] CI 失败用例在无 Firebase API key 环境复测：7 个文件、250
项通过；补充工作区标题数据透传后，入口记忆与标题相关 34 项通过。
- [x] 浏览器模拟当前任务不在历史分页中：页头仍正确显示任务详情标题；新建任务后立即返回首页也能恢复该任务。

- [x] 本地 mock 浏览器验证：首次进入设置页、恢复 New Task、恢复具体历史对话、重新恢复 Edit Agent；Tasks
整行跳转与 Refresh 移除；All / My agents / Shared with me 分类切换。
- [x] 本地 mock 浏览器验证：Skill Store 目录一致、日程筛选/创建/删除、资源页标题与空状态。
- [x] 浏览器模拟已记忆任务返回 `agent_session.not_found`：自动恢复到 New Task，未停留在错误页面。

## 任务标题与入口一致性

- 前端优先读取当前任务详情标题；后端详情接口复用历史列表的标题补全逻辑。直接打开不在首批历史分页中的飞书 / Slack
任务时，会从首条用户消息补出标题，并沿用外部消息前缀清理规则。已有手动或生成标题保持不变，也不会增加事件查询。
- 回归测试覆盖原始标题为空、任务不在已加载历史页、历史标题过时及已有标题无需补全的情况。
- 新建或切换任务成功后立即保存停留位置（`60e82d971`），避免快速返回首页时仍恢复旧位置。
- 同步 Skill Store 新流程的页面测试，并隔离登录依赖；清理旧查询选项的无用导出，修复 CI 中的单测与静态扫描失败。

## 部署与边界

涉及前端、共享 chat-ui，以及 claw-interface 任务详情的标题补全；接口结构不变。完整修复需要同时部署前端和
claw-interface 后端。staging 上的真实 Schedule
服务请求失败仍取决于后端可用性，本次修正其局部提示和展示。未运行本地完整单测集或生产构建，由 CI 执行对应质量检查。
```

### PR Body

## 修改内容

修复 R2 验收中首页、Agent 工作区和资源页面的展示与导航问题。从首页首次进入可编辑 Agent 时打开 Edit Agent 并展示设置面板；再次进入时，按用户和 Agent 恢复浏览器本地记录的编辑页、New Task 或具体任务对话。

- Skills：输入框 Skill Store 与侧边栏 Official Skills 使用同一目录及图标；移除 Use Skills 子菜单中的重复列表，仅保留创建和打开商店入口；去掉商店弹窗上下分割线。
- 首页：最近活动过滤没有实际标题的空任务；Schedule 加载失败使用独立、准确的提示；Agent 卡片缩短、描述限制单行，头像放大并上移至卡片边缘；缩小 Agent Builder 图标。
- Agent 工作区：标题显示当前页面或任务名称；统一侧边栏悬停样式、返回按钮和切换器，优化 Recents 空状态；Artifacts 复用全局页面及空状态，并分别按 workspace ID / runtime agent ID 筛选生成文件和上传文件。
- Schedule 与 Knowledge：移除无关连接状态和重复标题；日历改为浅灰底，修正分割线、按钮及筛选器样式，列表筛选不再影响日历；修复 Agent 日程空状态被其他运行环境状态遮蔽的问题。Knowledge 标题与侧边栏一致，创建弹窗不再导致背景提前显示空的 Unfiled 卡片，移除空状态中的未归档上传入口。
- Tasks 与 Agents：任务整行可进入聊天，保留原生链接行为；去掉 Tasks 顶部 Refresh；新增默认 All 标签，各分类分页独立。Agent 入口记录不覆盖明确指定的任务链接，失效的已记忆任务可回退到 New Task。

- 页面头部：以 Connector 为基准，统一 Agents / Tasks / Artifacts / MCP / Skills / Knowledge，以及 Agent 内的 Artifacts / Schedule / External channels；标题、说明、宽度和留白复用同一组件。Credits 异常提示缩小并改为灰色。补齐本地 mock 的 Agent 详情接口，避免 External channels 请求 undefined。

## 问题原因

Skill Store 仍使用旧目录；首页直接把底层空会话当作活动；资源页复用了带运行环境连接状态的聊天标题组件。Agent 入口缺少本地停留位置记录，工作区与全局页面也存在重复组件及样式差异。

## 验证结果

- [x] 最新提交 `f9255fffb` 的 CI：26 项通过、15 项按条件跳过，无失败或等待项；Claude 与 Codex 对该提交复审均无新增问题。
- [x] 后端任务详情与历史列表定向测试：61 项通过。新增飞书 / Slack 原始标题为空、当前任务不在首批 50 条历史记录中的回归用例；修复前 4 个用例失败，修复后全部通过。
- [x] 后端 ruff、格式检查、Pyright 与 import-linter 全部通过；提交钩子检查通过。

- [x] Agent、Tasks 与首页相关单测：59 个文件、398 项通过（同步最新 main 后重新执行）。
- [x] chat-ui 的 SkillsSubMenu / SkillStoreDialog：20 项通过。
- [x] 本轮已验证 Skills、Knowledge、Artifacts、Schedule 相关定向测试。
- [x] 头部调整后定向测试：40 项通过；资源页、渠道和日程回归：154 项通过（既有 69 项跳过、1 项 todo）。
- [x] 浏览器核对：全局及 Agent 资源页标题均为 16px / 600，桌面顶部留白 24px；Credits 提示 12px；渠道页无 undefined 请求错误。
- [x] 同步最新 Agent 面板改动后，入口和工作区回归：54 个文件、392 项通过，保留面板优化及首次编辑/后续恢复行为。
- [x] TypeScript、ESLint、仓库治理检查、Knip 与 `git diff --check`。
- [x] CI 失败用例在无 Firebase API key 环境复测：7 个文件、250 项通过；补充工作区标题数据透传后，入口记忆与标题相关 34 项通过。
- [x] 浏览器模拟当前任务不在历史分页中：页头仍正确显示任务详情标题；新建任务后立即返回首页也能恢复该任务。

- [x] 本地 mock 浏览器验证：首次进入设置页、恢复 New Task、恢复具体历史对话、重新恢复 Edit Agent；Tasks 整行跳转与 Refresh 移除；All / My agents / Shared with me 分类切换。
- [x] 本地 mock 浏览器验证：Skill Store 目录一致、日程筛选/创建/删除、资源页标题与空状态。
- [x] 浏览器模拟已记忆任务返回 `agent_session.not_found`：自动恢复到 New Task，未停留在错误页面。

## 任务标题与入口一致性

- 前端优先读取当前任务详情标题；后端详情接口复用历史列表的标题补全逻辑。直接打开不在首批历史分页中的飞书 / Slack 任务时，会从首条用户消息补出标题，并沿用外部消息前缀清理规则。已有手动或生成标题保持不变，也不会增加事件查询。
- 回归测试覆盖原始标题为空、任务不在已加载历史页、历史标题过时及已有标题无需补全的情况。
- 新建或切换任务成功后立即保存停留位置（`60e82d971`），避免快速返回首页时仍恢复旧位置。
- 同步 Skill Store 新流程的页面测试，并隔离登录依赖；清理旧查询选项的无用导出，修复 CI 中的单测与静态扫描失败。

## 部署与边界

涉及前端、共享 chat-ui，以及 claw-interface 任务详情的标题补全；接口结构不变。完整修复需要同时部署前端和 claw-interface 后端。staging 上的真实 Schedule 服务请求失败仍取决于后端可用性，本次修正其局部提示和展示。未运行本地完整单测集或生产构建，由 CI 执行对应质量检查。


---

## ci(review): restore Claude review through OpenRouter (#3780)

- **SHA**: `308f3f5c11938f7865628b00352d7148ddf9c350`
- **作者**: tim-srp
- **日期**: 2026-09-17T10:50:34Z
- **PR**: #3780

### Commit Message

```
ci(review): restore Claude review through OpenRouter (#3780)

## Summary

Claude review was disabled after provider availability issues. Route the
existing Claude reviewer through OpenRouter, following
https://github.com/SerendipityOneInc/gcp-foundation/pull/553.

- Set `provider: openrouter` and pass `OPENROUTER_API_KEY`.
- Preserve Sonnet 5 with medium effort, existing review filters, Codex
review, and aggregate gate wiring.
- Re-enable the repository's `AUTO_REVIEW_CLAUDE_ENABLED` variable to
validate the restored reviewer on this PR.

## Validation

- PyYAML parsing and focused assertions for OpenRouter wiring and
unchanged Codex/gate configuration: passed.
- `git diff --check`: passed.
- `scripts/verify-changed.sh` and push gates: passed (no application
surfaces changed).
- Local actionlint is unavailable; the live GitHub Actions reusable
workflow invocation succeeded.
- Live Claude review completed successfully through OpenRouter:
https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/35211593982.
This verifies provider/secret availability despite restricted
organization-secret metadata access.
- Codex review: APPROVE, no findings. Claude requested human
confirmation only because its environment could not read the private
reusable workflow; its provider/secret contract was independently
inspected and the live review succeeded. No code correction is required
for that observation.
```

### PR Body

## Summary

Claude review was disabled after provider availability issues. Route the existing Claude reviewer through OpenRouter, following https://github.com/SerendipityOneInc/gcp-foundation/pull/553.

- Set `provider: openrouter` and pass `OPENROUTER_API_KEY`.
- Preserve Sonnet 5 with medium effort, existing review filters, Codex review, and aggregate gate wiring.
- Re-enable the repository's `AUTO_REVIEW_CLAUDE_ENABLED` variable to validate the restored reviewer on this PR.

## Validation

- PyYAML parsing and focused assertions for OpenRouter wiring and unchanged Codex/gate configuration: passed.
- `git diff --check`: passed.
- `scripts/verify-changed.sh` and push gates: passed (no application surfaces changed).
- Local actionlint is unavailable; the live GitHub Actions reusable workflow invocation succeeded.
- Live Claude review completed successfully through OpenRouter: https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/35211593982. This verifies provider/secret availability despite restricted organization-secret metadata access.
- Codex review: APPROVE, no findings. Claude requested human confirmation only because its environment could not read the private reusable workflow; its provider/secret contract was independently inspected and the live review succeeded. No code correction is required for that observation.


---

## fix(agents): 优化设计面板、编辑入口和头像保存体验 (#3774)

- **SHA**: `7ea8a19d2576b5bd885a111015c65e849adeba39`
- **作者**: lynn Zhuang
- **日期**: 2026-09-17T10:34:31Z
- **PR**: #3774

### Commit Message

```
fix(agents): 优化设计面板、编辑入口和头像保存体验 (#3774)

## 修改内容

完善 Agent 设计面板的编辑流程：从首页进入 Agent 时直接打开 Edit Agent
和设置面板，指令可在面板内编辑，长内容保持在可视范围内；在 Profile 上传头像并保存后，继续停留在 Profile。

- **默认编辑入口**：首页 Agent 卡片、Agent 列表和侧栏入口进入 Edit
Agent，并展开右侧设置面板；保留任务、历史会话跳转及旧 Agent 的兼容行为。
- **面板内编辑指令**：按 Default model、Instructions、MD
文件选择器和文本区排列；补齐标题并调整组间间距，沿用共享草稿和顶部 Save。
- **限制长内容高度**：MD 文本框高度上限为视口的 33%，长文本内部滚动；Skill 预览弹窗随视口限高，正文滚动时标题、关闭按钮和
Done 保持可见。
- **模型选择细节**：选中默认模型时，选择框同步展示 Default 标签；模型和 MD 选择器统一使用同款向下箭头。
- **响应式布局与顶栏**：桌面聊天区和设置面板按 1:1 平分空间，窄屏保留覆盖式面板；左侧导航、主区域和设置面板顶栏统一为 51px。
- **页签与保存按钮**：选中页签使用 Medium（500）字重，2px 下划线贴齐分割线；移除 Save 中的 ⌘ S 提示，保留
Cmd/Ctrl+S 快捷键。
- **头像保存后保持页签**：上传头像、保存及后续版本或会话刷新均保留当前 Settings / Profile 选择；进入另一个 Agent
时仍默认选中 Settings。

## 实现要点

指令编辑器移入设置面板并复用已有草稿和保存流程。编辑框与 Skill 弹窗分别增加视口高度约束，避免长内容撑大页面。

保存后的版本加载会暂时卸载设置面板，原来的非受控页签会因此回到
Settings。将页签状态保存在页面层并传给设置面板后，可跨面板重新挂载保留选择；页面已有的 workspaceId key 负责在切换
Agent 时重新初始化。

## 验证

- [x] 本地 TypeScript、ESLint、前端治理检查及 `git diff --check` 通过。
- [x] Agent 入口相关 6 个测试文件、31 个测试通过，覆盖首页链接、侧栏高亮、任务导航、设置展开和旧 Agent 兼容行为。
- [x] 设置面板与头像保存相关 5 个测试文件、16 个测试通过；新增回归测试覆盖上传、保存、加载期间卸载及会话刷新后仍保持
Profile。
- [x] ModelPicker 的 22 个测试、Select 的 5 个测试及相应共享包检查通过。
- [x] 本地 mock 浏览器验收：60 行 MD 保持限高，Skills / Danger Zone 可见；150 段长 Skill 在
1440×900、390×844、844×390、320×568 下未溢出，正文可滚动，关闭按钮和 Done 可见。
- [x] 浏览器核对顶栏对齐、选中页签、默认模型标签、下拉箭头及 Save 按钮。
- [x] 提交 `01957c2ee` 的完整前端测试、构建、类型与 lint 检查、CodeQL 和自动审查通过；自动审查未发现问题。

本次仅修改前端，无需后端部署。
```

### PR Body

## 修改内容

完善 Agent 设计面板的编辑流程：从首页进入 Agent 时直接打开 Edit Agent 和设置面板，指令可在面板内编辑，长内容保持在可视范围内；在 Profile 上传头像并保存后，继续停留在 Profile。

- **默认编辑入口**：首页 Agent 卡片、Agent 列表和侧栏入口进入 Edit Agent，并展开右侧设置面板；保留任务、历史会话跳转及旧 Agent 的兼容行为。
- **面板内编辑指令**：按 Default model、Instructions、MD 文件选择器和文本区排列；补齐标题并调整组间间距，沿用共享草稿和顶部 Save。
- **限制长内容高度**：MD 文本框高度上限为视口的 33%，长文本内部滚动；Skill 预览弹窗随视口限高，正文滚动时标题、关闭按钮和 Done 保持可见。
- **模型选择细节**：选中默认模型时，选择框同步展示 Default 标签；模型和 MD 选择器统一使用同款向下箭头。
- **响应式布局与顶栏**：桌面聊天区和设置面板按 1:1 平分空间，窄屏保留覆盖式面板；左侧导航、主区域和设置面板顶栏统一为 51px。
- **页签与保存按钮**：选中页签使用 Medium（500）字重，2px 下划线贴齐分割线；移除 Save 中的 ⌘ S 提示，保留 Cmd/Ctrl+S 快捷键。
- **头像保存后保持页签**：上传头像、保存及后续版本或会话刷新均保留当前 Settings / Profile 选择；进入另一个 Agent 时仍默认选中 Settings。

## 实现要点

指令编辑器移入设置面板并复用已有草稿和保存流程。编辑框与 Skill 弹窗分别增加视口高度约束，避免长内容撑大页面。

保存后的版本加载会暂时卸载设置面板，原来的非受控页签会因此回到 Settings。将页签状态保存在页面层并传给设置面板后，可跨面板重新挂载保留选择；页面已有的 workspaceId key 负责在切换 Agent 时重新初始化。

## 验证

- [x] 本地 TypeScript、ESLint、前端治理检查及 `git diff --check` 通过。
- [x] Agent 入口相关 6 个测试文件、31 个测试通过，覆盖首页链接、侧栏高亮、任务导航、设置展开和旧 Agent 兼容行为。
- [x] 设置面板与头像保存相关 5 个测试文件、16 个测试通过；新增回归测试覆盖上传、保存、加载期间卸载及会话刷新后仍保持 Profile。
- [x] ModelPicker 的 22 个测试、Select 的 5 个测试及相应共享包检查通过。
- [x] 本地 mock 浏览器验收：60 行 MD 保持限高，Skills / Danger Zone 可见；150 段长 Skill 在 1440×900、390×844、844×390、320×568 下未溢出，正文可滚动，关闭按钮和 Done 可见。
- [x] 浏览器核对顶栏对齐、选中页签、默认模型标签、下拉箭头及 Save 按钮。
- [x] 提交 `01957c2ee` 的完整前端测试、构建、类型与 lint 检查、CodeQL 和自动审查通过；自动审查未发现问题。

本次仅修改前端，无需后端部署。


---

## feat(agents): publish shared agents with manual updates and independent copies (#3773)

- **SHA**: `09b9faecd042ebbc657d83a161220bced09047a6`
- **作者**: kaka-srp
- **日期**: 2026-09-17T09:27:22Z
- **PR**: #3773

### Commit Message

```
feat(agents): publish shared agents with manual updates and independent copies (#3773)

## Summary

Sharing an Agent previously created an editable copy with no update
path. This change introduces explicitly published, read-only shared
instances: authors choose when to publish; recipients choose when to
apply an update. Make a copy creates an independently editable Agent
with no future update relationship.

- Reuse immutable Revisions for the published pointer. Preview/install
pin the shown version; revoking a link blocks new installs while
existing recipients keep update access.
- Add manual Update on Shared with me, with explicit confirmation only
when an Environment rebuild is needed. Copy source-owned resources into
the recipient scope and preserve runtime bindings and user data. Use
existing CAS, lifecycle and a small workspace update record; no new
release/task collection, scheduler, lease or historical migration.
- Enforce shared-instance write restrictions in the backend and both
Home/detail model controls. Make a copy uses the effective local
revision; Create Agent's existing “Start from a shared Agent” entry
creates an independent copy directly from the published link and opens
Build. Ordinary link Preview/Install stays a shared install.
- Keep Publish availability consistent between Build and list dialogs,
and show explicit success feedback. Allow shareable Agents using a
pinned public base Environment; keep custom-environment source
validation.
- Address independent review findings: prepare inactive candidates
before claiming an update, validate candidate identity and recheck the
base/publication/confirmation before activation, preserve locking for
uncertain activation results, complete the mock copy endpoint, and
restore unrelated chat-share wording.

## Dependencies and release

Depends on [Engine
#1496](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1496)
for complete source/Environment replacement. Deployment order: Engine
migration `0046` and image → claw-interface → Web. Backend/Web must be
coordinated because new installs require the previewed revision. ACS has
no code change. Design and implementation/acceptance details are in the
two `2026-09-16-agent-share-update-fork` documents.

## Test plan

- [x] Independent backend, Web and Engine reviews; fixes independently
re-reviewed.
- [x] Latest targeted tests: Web 379 passed; backend 85 passed. ECAP Web
and Python static checks passed, including commit/push gates.
- [x] Earlier feature validation: 343 Agent backend tests and browser
mock smoke for Update, copy, shared Build restrictions, publishing and
links.
- [x] Latest local existing Engine/ACS lane migrated and healthy; ECAP
frontend/backend use this feature checkout.
- [x] Real staging CSFLE repository validation on September 17:
publish/fork transactions, competing update claims, uninstall/copy
exclusion, atomic completion, retry identity, source scope and
revoked-link behavior passed. Run
`share_csfle_28d4f746e6dc4c3d814cdd2f45d359aa` created 11 isolated
records; exact cleanup and absence checks passed with zero failures. No
app lifecycle or Engine calls. Details are recorded in the
implementation plan.
- [ ] Complete real sandbox rebuild/recovery and verify preserved files,
memory, application data, sessions, connections, tasks and channel
delivery before production release.

Full Web testing previously reported three failures in existing
Builder/Markdown suites; those files passed all 131 tests when rerun
separately. Do not interpret that initial full run as green.

## Review scope

The size override keeps the coupled feature reviewable as one ECAP PR:
the repository size check counts 4,041 changed lines after exclusions,
including 1,772 test lines and the mock contract. Backend, Web and
Engine were reviewed separately; the override does not bypass quality
checks.
```

### PR Body

## Summary

Sharing an Agent previously created an editable copy with no update path. This change introduces explicitly published, read-only shared instances: authors choose when to publish; recipients choose when to apply an update. Make a copy creates an independently editable Agent with no future update relationship.

- Reuse immutable Revisions for the published pointer. Preview/install pin the shown version; revoking a link blocks new installs while existing recipients keep update access.
- Add manual Update on Shared with me, with explicit confirmation only when an Environment rebuild is needed. Copy source-owned resources into the recipient scope and preserve runtime bindings and user data. Use existing CAS, lifecycle and a small workspace update record; no new release/task collection, scheduler, lease or historical migration.
- Enforce shared-instance write restrictions in the backend and both Home/detail model controls. Make a copy uses the effective local revision; Create Agent's existing “Start from a shared Agent” entry creates an independent copy directly from the published link and opens Build. Ordinary link Preview/Install stays a shared install.
- Keep Publish availability consistent between Build and list dialogs, and show explicit success feedback. Allow shareable Agents using a pinned public base Environment; keep custom-environment source validation.
- Address independent review findings: prepare inactive candidates before claiming an update, validate candidate identity and recheck the base/publication/confirmation before activation, preserve locking for uncertain activation results, complete the mock copy endpoint, and restore unrelated chat-share wording.

## Dependencies and release

Depends on [Engine #1496](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1496) for complete source/Environment replacement. Deployment order: Engine migration `0046` and image → claw-interface → Web. Backend/Web must be coordinated because new installs require the previewed revision. ACS has no code change. Design and implementation/acceptance details are in the two `2026-09-16-agent-share-update-fork` documents.

## Test plan

- [x] Independent backend, Web and Engine reviews; fixes independently re-reviewed.
- [x] Latest targeted tests: Web 379 passed; backend 85 passed. ECAP Web and Python static checks passed, including commit/push gates.
- [x] Earlier feature validation: 343 Agent backend tests and browser mock smoke for Update, copy, shared Build restrictions, publishing and links.
- [x] Latest local existing Engine/ACS lane migrated and healthy; ECAP frontend/backend use this feature checkout.
- [x] Real staging CSFLE repository validation on September 17: publish/fork transactions, competing update claims, uninstall/copy exclusion, atomic completion, retry identity, source scope and revoked-link behavior passed. Run `share_csfle_28d4f746e6dc4c3d814cdd2f45d359aa` created 11 isolated records; exact cleanup and absence checks passed with zero failures. No app lifecycle or Engine calls. Details are recorded in the implementation plan.
- [ ] Complete real sandbox rebuild/recovery and verify preserved files, memory, application data, sessions, connections, tasks and channel delivery before production release.

Full Web testing previously reported three failures in existing Builder/Markdown suites; those files passed all 131 tests when rerun separately. Do not interpret that initial full run as green.

## Review scope

The size override keeps the coupled feature reviewable as one ECAP PR: the repository size check counts 4,041 changed lines after exclusions, including 1,772 test lines and the mock contract. Backend, Web and Engine were reviewed separately; the override does not bypass quality checks.


---

## fix(chat): render model provider icons locally (#3770)

- **SHA**: `82b8f6355fab065be659c5c9203d5d97d9fefa91`
- **作者**: finn-srp
- **日期**: 2026-09-17T07:11:53Z
- **PR**: #3770

### Commit Message

```
fix(chat): render model provider icons locally (#3770)

## Summary

- render model provider logos as local React SVG components instead of
backend/CDN image URLs
- map the staging catalog metadata to Claude, DeepSeek, Doubao/Seed,
Gemini, GLM, Grok, Kimi, OpenAI, Qwen, and ZooWork icons
- use a fixed CPU icon for unknown/private providers
- cover staging catalog labels and known/unknown rendering behavior with
unit tests

## Verification

- `pnpm --filter @zooclaw/chat-ui test`
- `pnpm --filter @zooclaw/chat-ui tsc`
- `pnpm --filter @zooclaw/chat-ui lint`
- targeted `web/app` Vitest suite: 71 tests passed
- `bash scripts/verify-web.sh <changed app paths>`
- `bash scripts/verify-changed.sh`
```

### PR Body

## Summary

- render model provider logos as local React SVG components instead of backend/CDN image URLs
- map the staging catalog metadata to Claude, DeepSeek, Doubao/Seed, Gemini, GLM, Grok, Kimi, OpenAI, Qwen, and ZooWork icons
- use a fixed CPU icon for unknown/private providers
- cover staging catalog labels and known/unknown rendering behavior with unit tests

## Verification

- `pnpm --filter @zooclaw/chat-ui test`
- `pnpm --filter @zooclaw/chat-ui tsc`
- `pnpm --filter @zooclaw/chat-ui lint`
- targeted `web/app` Vitest suite: 71 tests passed
- `bash scripts/verify-web.sh <changed app paths>`
- `bash scripts/verify-changed.sh`



---

## fix(agents): 修复头像保存同步、首页路径与全局输入框高度 (#3768)

- **SHA**: `721a2d037ad4253b0b31243fcfc14e130c0533bc`
- **作者**: lynn Zhuang
- **日期**: 2026-09-17T06:52:58Z
- **PR**: #3768

### Commit Message

```
fix(agents): 修复头像保存同步、首页路径与全局输入框高度 (#3768)

## 修复内容

新建 Agent 曾直接把用户的整段需求截断后当作名称；手动上传头像后，Save
又因头像地址不符合源配置校验规则而失败。本次同时修复这两个问题，并完成首页、聊天输入框和 Agents 列表的界面调整。

- 新建 Agent 未指定名称时使用 `Untitled Agent`，保留用户显式设置的名称。
- 首页统一为 `/home`，旧 `/new-chat` 链接通过 308 跳转并保留查询参数；导航、登录落地与对应测试同步更新。
- 在共享 `@zooclaw/chat-ui` 中限制输入框最大高度为各自默认高度的两倍，覆盖首页、Agent
编辑、聊天会话及其他复用入口。超出后内部滚动，工具栏保持可见，清空后恢复原高度。
- 新增受归属校验保护的头像上传接口，将图片规范化并存入 Agent 头像专用存储，使返回地址可通过保存校验；Profile 头像恢复圆形裁切。
- 保存后刷新 Agent 定义、侧边栏、首页和普通聊天页使用的列表缓存，确保各入口展示用户上传的头像。
- Agents 标题上移，增加 `My agents` / `Shared with me` 标签并与右侧操作对齐，列表列名改为
`Name`。

## 问题原因

- #3753 修复的是旧 Agent Builder 命名路径，新版 Agent 定义创建服务仍从 intent 截取默认名称。
- Profile 原先复用了旧头像上传地址，而新版 Agent Source 只接受规范化的
`agent-avatars/<sha256>.png` 地址，因此上传预览成功后仍无法保存。
- 设置保存未刷新普通聊天页使用的 Agent 列表缓存，可能继续显示旧头像。
- 输入框各变体的高度规则不一致，launcher 缺少统一上限。

## 验证

- [x] 共享 chat-ui：480 项测试通过。
- [x] 输入框相关页面：242 项测试通过；会话高度校准后相关 141 项测试再次通过。
- [x] 头像保存、缓存刷新、设置、展示及侧边栏：40 项测试通过；聊天渲染另有 41 项测试通过。
- [x] 后端头像及路由边界：52 项测试通过；创建选项相关测试已通过。
- [x] 前后端静态检查已通过；推送前运行仓库 changed-surface gate。
- [x] 本地浏览器在桌面和手机宽度验证：首页 `160 → 320px`，Agent 编辑、Agent 会话及普通聊天页 `118 →
236px`，超长内容内部滚动且工具栏可见。
- [x]
本地模拟环境验证头像上传预览、Save、侧边栏、聊天页和刷新后的持久展示；头像图片加载成功且为圆形裁切。真实图片规范化、归属及大小校验由后端测试覆盖。
- [x] Agents 标签与按钮对齐，移动端无页面横向溢出。

## 发布说明

头像修复涉及 `web/app` 和 `services/claw-interface`，合并后需要前后端 staging
部署均成功才完整生效。以上浏览器验证基于本地模拟环境，尚未宣称 staging 已修复。

## 自动评审处理

- **已修复：本地 mock 缺少头像上传接口。** 新增 multipart 上传、图片规范化和图片读取接口，保存前不改 Agent
定义。新增接口测试与既有 mock 测试共 14 项通过；独立 mock HTTP 服务已验证上传、PNG 读取、settings
commit、列表和 active revision 回读完整链路。此前浏览器验证对上传接口做了测试拦截，这一补充验证覆盖了实际 mock
服务。
- **本次未扩展：未提交头像对象的清理。** 经核查，main 原有 Profile 上传已在 Save 前调用公开 R2 上传；生成头像也在
ChangeSet
提交前写入同一不可变头像存储。本次复用现有规范化存储并限制上传大小，没有引入新的“先上传、后保存”生命周期。跨草稿、已发布版本、分享副本的引用回收应统一设计，不能简单在取消编辑时删除可能已被其他版本引用的同
hash 对象；此项作为既有存储生命周期问题保留给人工评审。
- **已修复：CI 依赖声明检查。** mock 图片规范化与测试直接使用 `sharp`，已在 `web/app`
声明开发依赖并复用锁文件已有的 0.35.1；冻结锁文件安装和 CI 同款 knip 依赖检查通过，未升级其他依赖。
```

### PR Body

## 修复内容

新建 Agent 曾直接把用户的整段需求截断后当作名称；手动上传头像后，Save 又因头像地址不符合源配置校验规则而失败。本次同时修复这两个问题，并完成首页、聊天输入框和 Agents 列表的界面调整。

- 新建 Agent 未指定名称时使用 `Untitled Agent`，保留用户显式设置的名称。
- 首页统一为 `/home`，旧 `/new-chat` 链接通过 308 跳转并保留查询参数；导航、登录落地与对应测试同步更新。
- 在共享 `@zooclaw/chat-ui` 中限制输入框最大高度为各自默认高度的两倍，覆盖首页、Agent 编辑、聊天会话及其他复用入口。超出后内部滚动，工具栏保持可见，清空后恢复原高度。
- 新增受归属校验保护的头像上传接口，将图片规范化并存入 Agent 头像专用存储，使返回地址可通过保存校验；Profile 头像恢复圆形裁切。
- 保存后刷新 Agent 定义、侧边栏、首页和普通聊天页使用的列表缓存，确保各入口展示用户上传的头像。
- Agents 标题上移，增加 `My agents` / `Shared with me` 标签并与右侧操作对齐，列表列名改为 `Name`。

## 问题原因

- #3753 修复的是旧 Agent Builder 命名路径，新版 Agent 定义创建服务仍从 intent 截取默认名称。
- Profile 原先复用了旧头像上传地址，而新版 Agent Source 只接受规范化的 `agent-avatars/<sha256>.png` 地址，因此上传预览成功后仍无法保存。
- 设置保存未刷新普通聊天页使用的 Agent 列表缓存，可能继续显示旧头像。
- 输入框各变体的高度规则不一致，launcher 缺少统一上限。

## 验证

- [x] 共享 chat-ui：480 项测试通过。
- [x] 输入框相关页面：242 项测试通过；会话高度校准后相关 141 项测试再次通过。
- [x] 头像保存、缓存刷新、设置、展示及侧边栏：40 项测试通过；聊天渲染另有 41 项测试通过。
- [x] 后端头像及路由边界：52 项测试通过；创建选项相关测试已通过。
- [x] 前后端静态检查已通过；推送前运行仓库 changed-surface gate。
- [x] 本地浏览器在桌面和手机宽度验证：首页 `160 → 320px`，Agent 编辑、Agent 会话及普通聊天页 `118 → 236px`，超长内容内部滚动且工具栏可见。
- [x] 本地模拟环境验证头像上传预览、Save、侧边栏、聊天页和刷新后的持久展示；头像图片加载成功且为圆形裁切。真实图片规范化、归属及大小校验由后端测试覆盖。
- [x] Agents 标签与按钮对齐，移动端无页面横向溢出。

## 发布说明

头像修复涉及 `web/app` 和 `services/claw-interface`，合并后需要前后端 staging 部署均成功才完整生效。以上浏览器验证基于本地模拟环境，尚未宣称 staging 已修复。

## 自动评审处理

- **已修复：本地 mock 缺少头像上传接口。** 新增 multipart 上传、图片规范化和图片读取接口，保存前不改 Agent 定义。新增接口测试与既有 mock 测试共 14 项通过；独立 mock HTTP 服务已验证上传、PNG 读取、settings commit、列表和 active revision 回读完整链路。此前浏览器验证对上传接口做了测试拦截，这一补充验证覆盖了实际 mock 服务。
- **本次未扩展：未提交头像对象的清理。** 经核查，main 原有 Profile 上传已在 Save 前调用公开 R2 上传；生成头像也在 ChangeSet 提交前写入同一不可变头像存储。本次复用现有规范化存储并限制上传大小，没有引入新的“先上传、后保存”生命周期。跨草稿、已发布版本、分享副本的引用回收应统一设计，不能简单在取消编辑时删除可能已被其他版本引用的同 hash 对象；此项作为既有存储生命周期问题保留给人工评审。
- **已修复：CI 依赖声明检查。** mock 图片规范化与测试直接使用 `sharp`，已在 `web/app` 声明开发依赖并复用锁文件已有的 0.35.1；冻结锁文件安装和 CI 同款 knip 依赖检查通过，未升级其他依赖。


---

## feat(marketing): add Agent Gallery to Solutions and navigation (#3738)

- **SHA**: `1d3913df3fc08db883a025119907bd35bc934f9b`
- **作者**: Mori-srp
- **日期**: 2026-09-17T06:39:17Z
- **PR**: #3738

### Commit Message

```
feat(marketing): add Agent Gallery to Solutions and navigation (#3738)

Solutions currently lists only industries. This change adds Agent
Gallery above Industries, groups the Solutions navigation into Agent
Gallery and Industry, and adds a Gallery footer link. English and
Chinese chrome point to the initial English Gallery at
`https://zoowork.ai/en/agent-gallery`; no links point to chatgpt.site.
The grouped navigation uses named sections and native link lists with
focus and Escape handling.

Gallery pages and reports live in
[zoowork-agent-gallery](https://github.com/SerendipityOneInc/zoowork-agent-gallery).
Its independent Worker owns `/en/agent-gallery`, its descendants, and
`/agent-gallery-assets/*`. This PR adds `/en/agent-gallery/sitemap.xml`
to the main site's root sitemap. It includes the industry-card
presentation from #3734 so reviewers can assess the complete Solutions
page.

**Release gate:** keep this PR in draft until [Gallery PR
#1](https://github.com/SerendipityOneInc/zoowork-agent-gallery/pull/1)
is approved and merged, Guangbin completes Workers Builds setup, and the
official directory, all 10 details, assets, reports and sitemap pass
production checks. Publish the main-site entry and sitemap only
afterward. Analytics is not yet connected in the independent Worker.

Validation: main-app TypeScript and ESLint passed; all seven header
regressions and eight affected link/sitemap tests pass. All final-commit
CI checks passed, including web-quality, web-build-check and CodeQL.
Automated review confirmed the prior navigation accessibility finding is
resolved. English/Chinese Solutions and the two-column menu were
inspected locally. The independent Gallery passed its production build
and local Worker checks for 11 pages, 64 referenced assets/reports, five
negative routes, preview noindex and 11 sitemap URLs; all ten detail
pages were checked at 390px without horizontal overflow. The formal
route remained 404 at the last live check, so the complete production
click path is still pending.
```

### PR Body

Solutions currently lists only industries. This change adds Agent Gallery above Industries, groups the Solutions navigation into Agent Gallery and Industry, and adds a Gallery footer link. English and Chinese chrome point to the initial English Gallery at `https://zoowork.ai/en/agent-gallery`; no links point to chatgpt.site. The grouped navigation uses named sections and native link lists with focus and Escape handling.

Gallery pages and reports live in [zoowork-agent-gallery](https://github.com/SerendipityOneInc/zoowork-agent-gallery). Its independent Worker owns `/en/agent-gallery`, its descendants, and `/agent-gallery-assets/*`. This PR adds `/en/agent-gallery/sitemap.xml` to the main site's root sitemap. It includes the industry-card presentation from #3734 so reviewers can assess the complete Solutions page.

**Release gate:** keep this PR in draft until [Gallery PR #1](https://github.com/SerendipityOneInc/zoowork-agent-gallery/pull/1) is approved and merged, Guangbin completes Workers Builds setup, and the official directory, all 10 details, assets, reports and sitemap pass production checks. Publish the main-site entry and sitemap only afterward. Analytics is not yet connected in the independent Worker.

Validation: main-app TypeScript and ESLint passed; all seven header regressions and eight affected link/sitemap tests pass. All final-commit CI checks passed, including web-quality, web-build-check and CodeQL. Automated review confirmed the prior navigation accessibility finding is resolved. English/Chinese Solutions and the two-column menu were inspected locally. The independent Gallery passed its production build and local Worker checks for 11 pages, 64 referenced assets/reports, five negative routes, preview noindex and 11 sitemap URLs; all ten detail pages were checked at 390px without horizontal overflow. The formal route remained 404 at the last live check, so the complete production click path is still pending.


---

## feat(plugins): 接入 Skills 能力并统一侧边栏资源页面体验 (#3757)

- **SHA**: `46913a706cba3c4a7c13d8b370a0d148519c6d96`
- **作者**: lynn Zhuang
- **日期**: 2026-09-17T06:33:00Z
- **PR**: #3757

### Commit Message

```
feat(plugins): 接入 Skills 能力并统一侧边栏资源页面体验 (#3757)

## 改动说明
首页侧边栏的 Skills 页面此前没有接入现有 Skill Registry，Connector、MCP 和 Knowledge
的标题、搜索、空状态及添加入口也不一致。本次接入现有能力，并统一四个资源页面的交互与视觉样式。

- **Skills**：读取完整分页目录，区分 Official / Personal，支持搜索及个人 Skill ZIP
上传、版本更新和删除；展示卡片使用统一闪电图标，不再提供卡片详情弹窗、版本和 Official 标签。
- **统一页面组件**：复用标题、搜索、下划线 Tab 与空状态组件；调整工具栏右侧搜索和操作按钮，移除 Connector
手动刷新按钮；修复主题焦点样式与设计系统输入框叠加产生的多重边框。
- **MCP**：保留运行时能力判断；移除标题数量，空列表将 Add MCP 放在空状态下方，有数据时放在右上角。
- **Knowledge**：增加空状态插画和添加弹窗，搜索紧邻添加按钮；精简上传说明并折叠格式细节；列表每页 20
条，取消固定高度和嵌套滚动；侧边栏名称缩短为 Knowledge。
- **上传与配套**：Skill ZIP 接口避开 Next middleware 的 10 MB
请求体克隆限制，继续由代理/后端校验认证；补充中英文文案、Mock 场景和回归测试。

## 验证
- [x] TypeScript 类型检查
- [x] Web 治理规则检查
- [x] 首轮 7 个相关单元测试文件，共 189 项通过；审查修复后 Skills 相关 15 项测试通过（新增 4 项）
- [x] 全量 ESLint 与 Knip 未使用代码检查
- [x] Connector 27 项测试通过，验证移除手动刷新按钮后 OAuth 返回自动刷新
- [x] 本地 Mock 页面交互验证（此前迭代）
- [ ] 真实账号的线上 Skill Registry 上传与权限验证

当前本地展示数据来自 Mock；未修改后端业务服务。最终一轮浏览器工具连接不可用，因此分页调整以单元测试验证，未宣称完成最终全页面视觉回归。

## 审查修复
- 切换账号或组织时重新初始化 Skill 视图，清空已选择的上传文件，避免跨身份误提交。
- 校验分页总数、分页大小与最终唯一记录数量，拒绝重复或不完整的目录。
- 清理取消详情弹窗和刷新入口后留下的未使用导出。
```

### PR Body

## 改动说明
首页侧边栏的 Skills 页面此前没有接入现有 Skill Registry，Connector、MCP 和 Knowledge 的标题、搜索、空状态及添加入口也不一致。本次接入现有能力，并统一四个资源页面的交互与视觉样式。

- **Skills**：读取完整分页目录，区分 Official / Personal，支持搜索及个人 Skill ZIP 上传、版本更新和删除；展示卡片使用统一闪电图标，不再提供卡片详情弹窗、版本和 Official 标签。
- **统一页面组件**：复用标题、搜索、下划线 Tab 与空状态组件；调整工具栏右侧搜索和操作按钮，移除 Connector 手动刷新按钮；修复主题焦点样式与设计系统输入框叠加产生的多重边框。
- **MCP**：保留运行时能力判断；移除标题数量，空列表将 Add MCP 放在空状态下方，有数据时放在右上角。
- **Knowledge**：增加空状态插画和添加弹窗，搜索紧邻添加按钮；精简上传说明并折叠格式细节；列表每页 20 条，取消固定高度和嵌套滚动；侧边栏名称缩短为 Knowledge。
- **上传与配套**：Skill ZIP 接口避开 Next middleware 的 10 MB 请求体克隆限制，继续由代理/后端校验认证；补充中英文文案、Mock 场景和回归测试。

## 验证
- [x] TypeScript 类型检查
- [x] Web 治理规则检查
- [x] 首轮 7 个相关单元测试文件，共 189 项通过；审查修复后 Skills 相关 15 项测试通过（新增 4 项）
- [x] 全量 ESLint 与 Knip 未使用代码检查
- [x] Connector 27 项测试通过，验证移除手动刷新按钮后 OAuth 返回自动刷新
- [x] 本地 Mock 页面交互验证（此前迭代）
- [ ] 真实账号的线上 Skill Registry 上传与权限验证

当前本地展示数据来自 Mock；未修改后端业务服务。最终一轮浏览器工具连接不可用，因此分页调整以单元测试验证，未宣称完成最终全页面视觉回归。

## 审查修复
- 切换账号或组织时重新初始化 Skill 视图，清空已选择的上传文件，避免跨身份误提交。
- 校验分页总数、分页大小与最终唯一记录数量，拒绝重复或不完整的目录。
- 清理取消详情弹窗和刷新入口后留下的未使用导出。


---

## fix(agents): pin effective global skills as inherited refs on first skill declaration (#3764)

- **SHA**: `a9d4fd0b1168123977aa9c835f167a657b25bc16`
- **作者**: kyle-srp
- **日期**: 2026-09-17T06:24:04Z
- **PR**: #3764

### Commit Message

```
fix(agents): pin effective global skills as inherited refs on first skill declaration (#3764)

## 问题

self-evolving agent 在 Build 里首次声明任何自建技能后,**全部 22 个平台全局技能(含
`knowledge-base`)静默从可见技能面消失**。引擎契约:`declared.skills` 一旦存在(即使
`[]`)就停用全局技能自动启用(spec
`docs/superpowers/specs/2026-09-10-unified-agents-navigation.md`)。

线上实例 `agt_01m2mwrp8p1s27v7eyjd8b11ms`(挂知识库 `eab504…`):Build AI 为它生成
prompt-only 技能 `marketing-kb-service` 后,终端(active)会话 4 个、`kb_search` 调用
**0** 次——模型不知道自己有检索工具;而 authoring 会话(会翻文件系统)自行找到脚本检索成功(7 调 5
中),证明能力/权限/数据全部健康,唯独可见性被声明动作剥离。详见 #3763。

## 根因

既定设计(同 spec:"**Preserve effective global skill bindings when projecting
source skills**")要求投影 source skills
时把生效全局物化为只读继承引用(`inherited-skills.json`)。该机制在 **legacy
采编路径已实现**(`agent_baseline_adoption` 从 `resolved_skill_pins`
填充),但**新建定义路径从未实现**——首次声明自建技能时 `materialize_skills`
只产出自建绑定,基线全局被丢弃。实现缺口,非设计变更。

## 修复

收口在 `materialize_skills`(所有声明路径的共同漏斗):当 source 首次引入 source-owned 技能、而
agent 活跃配置仍在自动启用基线上时,把 `active_agent.resolved_skill_pins` 合成为
`source.inherited_skills`(只读、`source_owned=False`),声明列表 = 继承全局 + 自建。

- `active_agent` 由两个调用点(change_set / authoring_gateway)传入**它们本就已获取的**
`EngineAgentDetail`,零额外 engine 调用;
- create 路径(engine agent 尚不存在)不传 → 跳过;
- 四重护栏:source 已有继承引用 / `skills_explicit`(显式自管)/ 上一 revision 已声明 /
活跃配置已离开基线(含历史 `[]`)——**已有声明永不被复活**,显式清空语义不变;
- 快照被就地写入继承引用 → 存入 revision → 后续 commit 从 source 直接派生
`inherited-skills.json`(只读校验已有)。

## 测试

`tests/unit/test_skill_materialization_inherited.py` 6 条:首次声明合成基线(含
`inherited-skills.json` 派生)/ 无 active(create 路径)跳过 / 已离开基线不复活 /
`skills_explicit` 跳过 / 已有声明历史跳过 / 无自建技能不声明。
本地:pyright 0 错、ruff/format/import-linter 全过、相关单测 18/18 绿。

## 存量

已中招的 3 个 agent(#3763 列出)不自愈,按 issue 中迁移方案单独处理;#3763 同时追踪 C1(KB 依赖
fail-closed 校验)与 lockfile 时鲜性设计议题。

Fixes #3763

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## 问题

self-evolving agent 在 Build 里首次声明任何自建技能后,**全部 22 个平台全局技能(含 `knowledge-base`)静默从可见技能面消失**。引擎契约:`declared.skills` 一旦存在(即使 `[]`)就停用全局技能自动启用(spec `docs/superpowers/specs/2026-09-10-unified-agents-navigation.md`)。

线上实例 `agt_01m2mwrp8p1s27v7eyjd8b11ms`(挂知识库 `eab504…`):Build AI 为它生成 prompt-only 技能 `marketing-kb-service` 后,终端(active)会话 4 个、`kb_search` 调用 **0** 次——模型不知道自己有检索工具;而 authoring 会话(会翻文件系统)自行找到脚本检索成功(7 调 5 中),证明能力/权限/数据全部健康,唯独可见性被声明动作剥离。详见 #3763。

## 根因

既定设计(同 spec:"**Preserve effective global skill bindings when projecting source skills**")要求投影 source skills 时把生效全局物化为只读继承引用(`inherited-skills.json`)。该机制在 **legacy 采编路径已实现**(`agent_baseline_adoption` 从 `resolved_skill_pins` 填充),但**新建定义路径从未实现**——首次声明自建技能时 `materialize_skills` 只产出自建绑定,基线全局被丢弃。实现缺口,非设计变更。

## 修复

收口在 `materialize_skills`(所有声明路径的共同漏斗):当 source 首次引入 source-owned 技能、而 agent 活跃配置仍在自动启用基线上时,把 `active_agent.resolved_skill_pins` 合成为 `source.inherited_skills`(只读、`source_owned=False`),声明列表 = 继承全局 + 自建。

- `active_agent` 由两个调用点(change_set / authoring_gateway)传入**它们本就已获取的** `EngineAgentDetail`,零额外 engine 调用;
- create 路径(engine agent 尚不存在)不传 → 跳过;
- 四重护栏:source 已有继承引用 / `skills_explicit`(显式自管)/ 上一 revision 已声明 / 活跃配置已离开基线(含历史 `[]`)——**已有声明永不被复活**,显式清空语义不变;
- 快照被就地写入继承引用 → 存入 revision → 后续 commit 从 source 直接派生 `inherited-skills.json`(只读校验已有)。

## 测试

`tests/unit/test_skill_materialization_inherited.py` 6 条:首次声明合成基线(含 `inherited-skills.json` 派生)/ 无 active(create 路径)跳过 / 已离开基线不复活 / `skills_explicit` 跳过 / 已有声明历史跳过 / 无自建技能不声明。
本地:pyright 0 错、ruff/format/import-linter 全过、相关单测 18/18 绿。

## 存量

已中招的 3 个 agent(#3763 列出)不自愈,按 issue 中迁移方案单独处理;#3763 同时追踪 C1(KB 依赖 fail-closed 校验)与 lockfile 时鲜性设计议题。

Fixes #3763

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## fix(web): 优化首页 Agent 卡片布局、选择面板与日程文案 (#3758)

- **SHA**: `51e99348d18076fec63e249467cfbbc56a1745c7`
- **作者**: lynn Zhuang
- **日期**: 2026-09-17T03:29:58Z
- **PR**: #3758

### Commit Message

```
fix(web): 优化首页 Agent 卡片布局、选择面板与日程文案 (#3758)

## 修改说明
- 首页 Agent 卡片改为头像在上、名称和描述在下且左对齐，去掉使用时间与对话数量。
- 横向列表新增左右箭头，随滚动位置更新可用状态，并支持减少动态效果设置。
- 首页输入框的 Agent 选择面板移除系统 Assistant；Engine Agent 使用自身名称与头像，避免旧身份接口将普通
Agent 显示成 Assistant。
- 首页定时任务区域复用详情页的 Schedule（日程）文案，同步调整空状态提示。

## 问题原因
卡片展示了多余的活动信息，横向列表缺少明确的滚动控件；Agent 选择面板复用了旧运行环境的身份数据，可能用默认 Assistant 名称覆盖
Engine Agent 的实际名称。

## 验证
- [x] 113 项相关单元测试通过，包含系统 Assistant 过滤和 Engine 名称回归测试。
- [x] TypeScript 类型检查和相关 ESLint 检查通过。
- [x] 本地模拟预览验证左右滚动、卡片对齐和下拉实际名称。

## 关联说明
本 PR 按最新确认的卡片方案实现（展示名称和描述），与尚未合并的 #3755 存在卡片布局重叠；合并时应以本 PR 的最新布局为准。
本次不包含此前讨论的 Recent Activity 会话标题及定时任务部分加载失败修复。
```

### PR Body

## 修改说明
- 首页 Agent 卡片改为头像在上、名称和描述在下且左对齐，去掉使用时间与对话数量。
- 横向列表新增左右箭头，随滚动位置更新可用状态，并支持减少动态效果设置。
- 首页输入框的 Agent 选择面板移除系统 Assistant；Engine Agent 使用自身名称与头像，避免旧身份接口将普通 Agent 显示成 Assistant。
- 首页定时任务区域复用详情页的 Schedule（日程）文案，同步调整空状态提示。

## 问题原因
卡片展示了多余的活动信息，横向列表缺少明确的滚动控件；Agent 选择面板复用了旧运行环境的身份数据，可能用默认 Assistant 名称覆盖 Engine Agent 的实际名称。

## 验证
- [x] 113 项相关单元测试通过，包含系统 Assistant 过滤和 Engine 名称回归测试。
- [x] TypeScript 类型检查和相关 ESLint 检查通过。
- [x] 本地模拟预览验证左右滚动、卡片对齐和下拉实际名称。

## 关联说明
本 PR 按最新确认的卡片方案实现（展示名称和描述），与尚未合并的 #3755 存在卡片布局重叠；合并时应以本 PR 的最新布局为准。
本次不包含此前讨论的 Recent Activity 会话标题及定时任务部分加载失败修复。


---
