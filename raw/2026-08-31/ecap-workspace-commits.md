# SerendipityOneInc/ecap-workspace — commits 2026-08-31

## fix(team): align account avatar display (#3600)

- **SHA**: `5dc25a16e1fc200854d22651a7a3e3556dd8eec4`
- **作者**: tim-srp
- **日期**: 2026-08-31T12:16:45Z
- **PR**: #3600

### Commit Message

```
fix(team): align account avatar display (#3600)

## Summary

- return the persisted account avatar from `GET /account/me`
- preserve the avatar in the shared account client and Enterprise Admin
parser
- render the returned avatar in the Enterprise Admin account menu

## Validation

- `pytest services/claw-interface/tests/unit/test_routes_account.py -q`
- `pnpm --filter @zooclaw/auth-client test`
- `pnpm --filter @zooclaw/enterprise-admin test --
lib/__tests__/auth.test.ts`
- `pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit`
- `bash scripts/verify-changed.sh`

## Deployment

This change requires both the claw-interface backend and Enterprise
Admin frontend to be deployed.
```

### PR Body

## Summary

- return the persisted account avatar from `GET /account/me`
- preserve the avatar in the shared account client and Enterprise Admin parser
- render the returned avatar in the Enterprise Admin account menu

## Validation

- `pytest services/claw-interface/tests/unit/test_routes_account.py -q`
- `pnpm --filter @zooclaw/auth-client test`
- `pnpm --filter @zooclaw/enterprise-admin test -- lib/__tests__/auth.test.ts`
- `pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit`
- `bash scripts/verify-changed.sh`

## Deployment

This change requires both the claw-interface backend and Enterprise Admin frontend to be deployed.


---

## fix(agent-builder): keep recoverable steps in normal flow (#3599)

- **SHA**: `477029a819a932f09362fe87c7b79b929a000c93`
- **作者**: kaka-srp
- **日期**: 2026-08-31T11:46:48Z
- **PR**: #3599

### Commit Message

```
fix(agent-builder): keep recoverable steps in normal flow (#3599)

## Summary

- Make the server-generated Agent Builder bootstrap read project context
first and skip the absent manifest for new projects.
- Keep tool-step failures local to their detail rows instead of turning
the whole activity header into `Failed at step …`.
- Preserve the normal elapsed-time display while the turn continues and
the normal completed activity summary after it finishes, without
changing cancellation semantics.

## Root cause

The bootstrap probed `agent/agent-pack.yaml` before reading the project
mode, although blank projects do not have a manifest yet. Separately,
`ToolGroup` promoted any historical step with `phase: error` to the
aggregate activity status, so a recoverable tool failure permanently
replaced the running/completed timer with a failure label.

## Test plan

- [x] `pnpm exec vitest run src/__tests__/tool-group.test.tsx` — 55
passed
- [x] `pnpm tsc` and `pnpm lint` in `web/packages/chat-ui`
- [x] `pytest tests/unit/test_agent_builder_service.py -q` — 190 passed
- [x] `bash scripts/verify-py.sh`
- [x] Pre-push PR-size and changed-surface gates

## Known unrelated baseline

The full `@zooclaw/chat-ui` suite passed 453/454 tests. The single
failure is the unchanged ModelPicker test expecting `rounded-[8px]`
while the current design-system component renders `rounded-md`; it
reproduces when run alone and is unrelated to the touched activity
timeline files.

## Related

- Paired V2 Agent Studio source PR:
https://github.com/SerendipityOneInc/ecap-agent-pack/pull/251
```

### PR Body

## Summary

- Make the server-generated Agent Builder bootstrap read project context first and skip the absent manifest for new projects.
- Keep tool-step failures local to their detail rows instead of turning the whole activity header into `Failed at step …`.
- Preserve the normal elapsed-time display while the turn continues and the normal completed activity summary after it finishes, without changing cancellation semantics.

## Root cause

The bootstrap probed `agent/agent-pack.yaml` before reading the project mode, although blank projects do not have a manifest yet. Separately, `ToolGroup` promoted any historical step with `phase: error` to the aggregate activity status, so a recoverable tool failure permanently replaced the running/completed timer with a failure label.

## Test plan

- [x] `pnpm exec vitest run src/__tests__/tool-group.test.tsx` — 55 passed
- [x] `pnpm tsc` and `pnpm lint` in `web/packages/chat-ui`
- [x] `pytest tests/unit/test_agent_builder_service.py -q` — 190 passed
- [x] `bash scripts/verify-py.sh`
- [x] Pre-push PR-size and changed-surface gates

## Known unrelated baseline

The full `@zooclaw/chat-ui` suite passed 453/454 tests. The single failure is the unchanged ModelPicker test expecting `rounded-[8px]` while the current design-system component renders `rounded-md`; it reproduces when run alone and is unrelated to the touched activity timeline files.

## Related

- Paired V2 Agent Studio source PR: https://github.com/SerendipityOneInc/ecap-agent-pack/pull/251


---

## feat(settings): show the default theme skin first (#3598)

- **SHA**: `505fc095a687cbb1d8bcdb766d9361a1082bbb4c`
- **作者**: shana-srp
- **日期**: 2026-08-31T10:50:49Z
- **PR**: #3598

### Commit Message

```
feat(settings): show the default theme skin first (#3598)

## Summary

- expose Paper Focus as the selectable default Theme skin
- place the default skin first while preserving the order of the
remaining skins
- update the Paper Focus description in English and Chinese
- cover the default selection and tile order with a unit test

## Testing

- `pnpm exec vitest run
tests/unit/components/settings/GeneralTab.unit.spec.tsx
tests/unit/theme/brand-themes.unit.spec.ts` (48 passed)
- `bash scripts/verify-changed.sh` (pre-push: TypeScript and ESLint
passed)

## Preview

- `http://localhost:3000/claw-settings`

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary

- expose Paper Focus as the selectable default Theme skin
- place the default skin first while preserving the order of the remaining skins
- update the Paper Focus description in English and Chinese
- cover the default selection and tile order with a unit test

## Testing

- `pnpm exec vitest run tests/unit/components/settings/GeneralTab.unit.spec.tsx tests/unit/theme/brand-themes.unit.spec.ts` (48 passed)
- `bash scripts/verify-changed.sh` (pre-push: TypeScript and ESLint passed)

## Preview

- `http://localhost:3000/claw-settings`


---

## feat(mcp): configure managed identity personal MCP (#3479)

- **SHA**: `4e00d84711c89033f15a80cf866429d4e38db7da`
- **作者**: sam-srp
- **日期**: 2026-08-31T10:49:03Z
- **PR**: #3479

### Commit Message

```
feat(mcp): configure managed identity personal MCP (#3479)

## Summary
- support personal MCP entries using `auth: { type: "managed_identity"
}`
- use the canonical HTTPS MCP server URL itself as the RFC 8707
resource; managed identity cannot be combined with static headers or
bearer credentials
- exchange the current user token only for MCP probing and persist no
exchanged token in personal MCP records
- synchronize the managed identity declaration to all installed Engine
Agents while preserving Agent Pack MCP entries
- preserve MCP discovery, tool filters, enable/disable, refresh, edit,
and delete behavior
- return an actionable error for credentials encrypted with an
unavailable key while allowing full secret replacement to recover the
connection
- show Stop immediately for the first message in a newly created session

## Security
- MCP configuration stores only the managed identity declaration; the
server URL defines the token resource
- `user-interface` owns the trusted-resource allowlist and rejects
unregistered resources before issuing a token
- runtime authentication uses short-lived resource tokens; no resource
token is stored in Workspace
- static bearer/header authentication remains available for third-party
MCP servers

## Deployment
No new Workspace setting is required. Claw Interface uses its existing
`ACCOUNT_SERVICE_URL` (with the existing account URL fallback) for
probe-time token exchange.

## Test plan
- 30 targeted Claw Interface MCP tests, Ruff, and Pyright
- 26 targeted web MCP/new-session tests, TypeScript, and ESLint

Part of SerendipityOneInc/zooclaw-engine#892.
```

### PR Body

## Summary
- support personal MCP entries using `auth: { type: "managed_identity" }`
- use the canonical HTTPS MCP server URL itself as the RFC 8707 resource; managed identity cannot be combined with static headers or bearer credentials
- exchange the current user token only for MCP probing and persist no exchanged token in personal MCP records
- synchronize the managed identity declaration to all installed Engine Agents while preserving Agent Pack MCP entries
- preserve MCP discovery, tool filters, enable/disable, refresh, edit, and delete behavior
- return an actionable error for credentials encrypted with an unavailable key while allowing full secret replacement to recover the connection
- show Stop immediately for the first message in a newly created session

## Security
- MCP configuration stores only the managed identity declaration; the server URL defines the token resource
- `user-interface` owns the trusted-resource allowlist and rejects unregistered resources before issuing a token
- runtime authentication uses short-lived resource tokens; no resource token is stored in Workspace
- static bearer/header authentication remains available for third-party MCP servers

## Deployment
No new Workspace setting is required. Claw Interface uses its existing `ACCOUNT_SERVICE_URL` (with the existing account URL fallback) for probe-time token exchange.

## Test plan
- 30 targeted Claw Interface MCP tests, Ruff, and Pyright
- 26 targeted web MCP/new-session tests, TypeScript, and ESLint

Part of SerendipityOneInc/zooclaw-engine#892.

---

## feat(agents): offer Auto on engine workspaces and route to a model ladder (#3568)

- **SHA**: `0a6b5e95bdf3e538f442c08b035cb24ff0c655a0`
- **作者**: siqiao-srp
- **日期**: 2026-08-31T10:26:31Z
- **PR**: #3568

### Commit Message

```
feat(agents): offer Auto on engine workspaces and route to a model ladder (#3568)

Depends on zooclaw-engine#846 + #988 being deployed. Without them this
writes a routing block no engine acts on: the turn keeps
`model.primary`, which is the intended degradation, not a break.

## What this does

Makes **Auto** selectable on engine workspaces and translates it into
the engine's `model.routing` contract.

- `engine_model_routing.py` — builds the block: `mode: auto`, the policy
ref, and a tier ladder (`low: gemini-3-flash-preview`, `mid:
claude-haiku-4-5`) **intersected with `resolve_verified_chat_models`**.
Plan enforcement is expressed by *which targets are declared*, not by a
ceiling the router has to honour, so a model the plan forbids is never
declared. The LiteLLM virtual key remains the hard backstop.
- `agent_model_service.py` — the engine read reports the `auto` sentinel
when routing is on (the stored primary is only the unrouted fallback, so
reporting it would show a model the user never chose). Picking a
concrete model writes `mode: off` and clears the targets, because
choosing a model is choosing not to route.
- `auto_model_scope` — new field on the response, `"session"` for engine
and `"subagents"` for V1.

## The frontend change is the copy, not the wiring

The composer already shows Auto as soon as the backend reports
`auto_model_available`. What was wrong is the description: *"Keep this
Agent's conversation on its configured model and route only tasks it
delegates"* is V1's subagent-only behaviour and is simply false for the
engine, which routes the conversation turn itself. One sentence cannot
be true for both runtimes, so the picker now chooses its wording from
`auto_model_scope`. A backend that reports no scope is a V1 backend, so
the default is the V1 wording.

## Contract doc reconciled

`services/claw-interface/AGENTS.md` required V2 to advertise a
fail-closed runtime capability before offering Auto. That was written
when routing was imagined as a plugin the runtime loads and a model
pinned at `sessions_spawn`. V2 routing is engine-native — no plugin to
install, version or negotiate with — so the clause is retired rather
than quietly violated. What replaces it is the part that still matters:
a stale control plane degrades to "Auto is on, every turn uses the
fallback", that degradation is **silent to the user**, and it is
detected from `session_events` `routing_decision` reason codes.

## Verified against a real engine

The write path was previously covered only by mocks, so the routing
block that had been validated was hand-written JSON rather than the
payload this code produces. Driven against a live controld:

- selecting Auto → rendered `mode: auto` with both targets, and a
per-alias route for each (no `MODEL_ROUTE_INVALID`);
- selecting a concrete model → rendered `mode: off`, `targets: {}`, and
the target's route dropped from the render.

Unit tests: 12 in `test_agent_model_service.py`, plus the frontend spec
asserting each runtime's wording.

---------

Co-authored-by: Claude Opus 5 (1M context) <noreply@anthropic.com>
```

### PR Body

Depends on zooclaw-engine#846 + #988 being deployed. Without them this writes a routing block no engine acts on: the turn keeps `model.primary`, which is the intended degradation, not a break.

## What this does

Makes **Auto** selectable on engine workspaces and translates it into the engine's `model.routing` contract.

- `engine_model_routing.py` — builds the block: `mode: auto`, the policy ref, and a tier ladder (`low: gemini-3-flash-preview`, `mid: claude-haiku-4-5`) **intersected with `resolve_verified_chat_models`**. Plan enforcement is expressed by *which targets are declared*, not by a ceiling the router has to honour, so a model the plan forbids is never declared. The LiteLLM virtual key remains the hard backstop.
- `agent_model_service.py` — the engine read reports the `auto` sentinel when routing is on (the stored primary is only the unrouted fallback, so reporting it would show a model the user never chose). Picking a concrete model writes `mode: off` and clears the targets, because choosing a model is choosing not to route.
- `auto_model_scope` — new field on the response, `"session"` for engine and `"subagents"` for V1.

## The frontend change is the copy, not the wiring

The composer already shows Auto as soon as the backend reports `auto_model_available`. What was wrong is the description: *"Keep this Agent's conversation on its configured model and route only tasks it delegates"* is V1's subagent-only behaviour and is simply false for the engine, which routes the conversation turn itself. One sentence cannot be true for both runtimes, so the picker now chooses its wording from `auto_model_scope`. A backend that reports no scope is a V1 backend, so the default is the V1 wording.

## Contract doc reconciled

`services/claw-interface/AGENTS.md` required V2 to advertise a fail-closed runtime capability before offering Auto. That was written when routing was imagined as a plugin the runtime loads and a model pinned at `sessions_spawn`. V2 routing is engine-native — no plugin to install, version or negotiate with — so the clause is retired rather than quietly violated. What replaces it is the part that still matters: a stale control plane degrades to "Auto is on, every turn uses the fallback", that degradation is **silent to the user**, and it is detected from `session_events` `routing_decision` reason codes.

## Verified against a real engine

The write path was previously covered only by mocks, so the routing block that had been validated was hand-written JSON rather than the payload this code produces. Driven against a live controld:

- selecting Auto → rendered `mode: auto` with both targets, and a per-alias route for each (no `MODEL_ROUTE_INVALID`);
- selecting a concrete model → rendered `mode: off`, `targets: {}`, and the target's route dropped from the render.

Unit tests: 12 in `test_agent_model_service.py`, plus the frontend spec asserting each runtime's wording.


---

## fix(agent-builder): 修复 Agent 详情弹窗分享链接溢出 (#3595)

- **SHA**: `cd6abe078cebfb8ff4e82b60c8527b15ac65a5d4`
- **作者**: lynn Zhuang
- **日期**: 2026-08-31T07:04:07Z
- **PR**: #3595

### Commit Message

```
fix(agent-builder): 修复 Agent 详情弹窗分享链接溢出 (#3595)

## 摘要
- 修复共享 Agent 详情弹窗中长分享链接撑出弹窗边界的问题。
- 保留现有的 URL 省略显示与复制按钮行为。

## 根因
分享链接行是 CSS Grid 的直接子项。其默认的 `min-width: auto` 会保留长 URL
的最小内容宽度，导致该行超过固定宽度的弹窗；即使内部 Flex 子项已允许收缩，也无法跨层覆盖 Grid item 的最小宽度约束。

## 测试计划
- [x] `bash scripts/verify-web.sh
'src/app/[locale]/(app)/(chat)/agent-builder/my-agents/owned/components/PublishDetailModal.tsx'
'tests/unit/app/agent-builder/my-agents/OwnedAgentsClient.unit.spec.tsx'`
- [x] `bash scripts/verify-changed.sh`
- [x] 在 1440px 视口下使用 Playwright 测量：弹窗的 `scrollWidth` 与 `clientWidth` 均为
512px，分享链接行右边界保持在弹窗内部。
```

### PR Body

## 摘要
- 修复共享 Agent 详情弹窗中长分享链接撑出弹窗边界的问题。
- 保留现有的 URL 省略显示与复制按钮行为。

## 根因
分享链接行是 CSS Grid 的直接子项。其默认的 `min-width: auto` 会保留长 URL 的最小内容宽度，导致该行超过固定宽度的弹窗；即使内部 Flex 子项已允许收缩，也无法跨层覆盖 Grid item 的最小宽度约束。

## 测试计划
- [x] `bash scripts/verify-web.sh 'src/app/[locale]/(app)/(chat)/agent-builder/my-agents/owned/components/PublishDetailModal.tsx' 'tests/unit/app/agent-builder/my-agents/OwnedAgentsClient.unit.spec.tsx'`
- [x] `bash scripts/verify-changed.sh`
- [x] 在 1440px 视口下使用 Playwright 测量：弹窗的 `scrollWidth` 与 `clientWidth` 均为 512px，分享链接行右边界保持在弹窗内部。

---

## test(e2e): stabilize and align the Playwright suite (#3594)

- **SHA**: `e7700aaf38a32c41997baf36697f984e2ef0c25e`
- **作者**: rayhuang198212
- **日期**: 2026-08-31T06:37:44Z
- **PR**: #3594

### Commit Message

```
test(e2e): stabilize and align the Playwright suite (#3594)

## Summary

This PR stabilizes the Playwright E2E suite and aligns existing
scenarios with the current ZooWork UI and runtime behavior.

  ## Changes

  - Update production E2E targets from `zooclaw.ai` to `zoowork.ai`
- Validate that the selected target URL matches the staging or
production environment
- Add a global Playwright timeout so reporting and artifact uploads can
finish before the CI job timeout
  - Align locators, assertions, and test flows with the current UI for:
    - agent hire/fire and marketplace management
    - chat streaming, errors, and recovery
    - concurrent sessions and subagent panels
    - file previews and upload boundaries
    - model switching
    - landing page and mobile i18n
    - insufficient credits
    - GIF search
- Require generated images and extracted video frames to be attached
directly to the assistant response instead of being returned as links,
file paths, or `MEDIA:` references
  - Simplify brittle assertions and improve session isolation

  ## Validation

  - `pnpm install --frozen-lockfile`
  - `pnpm exec tsc --noEmit --project app/tsconfig.json`
  - `pnpm --filter @zooclaw/web-app run lint`

  ## Scope

This PR only changes E2E tests, Playwright/CI configuration, test
fixtures, page objects, and related documentation. It does not change
application behavior.
```

### PR Body

 ## Summary

  This PR stabilizes the Playwright E2E suite and aligns existing scenarios with the current ZooWork UI and runtime behavior.

  ## Changes

  - Update production E2E targets from `zooclaw.ai` to `zoowork.ai`
  - Validate that the selected target URL matches the staging or production environment
  - Add a global Playwright timeout so reporting and artifact uploads can finish before the CI job timeout
  - Align locators, assertions, and test flows with the current UI for:
    - agent hire/fire and marketplace management
    - chat streaming, errors, and recovery
    - concurrent sessions and subagent panels
    - file previews and upload boundaries
    - model switching
    - landing page and mobile i18n
    - insufficient credits
    - GIF search
  - Require generated images and extracted video frames to be attached directly to the assistant response instead of being returned as links, file paths, or `MEDIA:` references
  - Simplify brittle assertions and improve session isolation

  ## Validation

  - `pnpm install --frozen-lockfile`
  - `pnpm exec tsc --noEmit --project app/tsconfig.json`
  - `pnpm --filter @zooclaw/web-app run lint`

  ## Scope

  This PR only changes E2E tests, Playwright/CI configuration, test fixtures, page objects, and related documentation. It does not change application behavior.

---

## feat(landing): refresh homepage hero content (#3578)

- **SHA**: `40a5897c1a0e8f55692292fdc2f259e67afd4ea4`
- **作者**: shana-srp
- **日期**: 2026-08-31T06:14:34Z
- **PR**: #3578

### Commit Message

```
feat(landing): refresh homepage hero content (#3578)

## Linear

N/A

## Summary

- Refresh the homepage hero title, subtitle, CTA alignment, typography,
and footer tagline across all supported locales.
- Replace the hero background and product interface with the supplied
high-resolution assets; preserve the interface at a 16 px radius.
- Add regression coverage for hero copy, media sources, layout classes,
and localized dictionaries.

## Test plan

- [x] `pnpm exec vitest run
tests/unit/app/zoowork-home-body.unit.spec.tsx
tests/unit/locales/zoowork-home-dictionary.unit.spec.ts
tests/unit/app/marketing-chrome.unit.spec.tsx
tests/unit/app/landing-footer.unit.spec.tsx` (58 tests)
- [x] `bash scripts/verify-changed.sh`
- [x] `node web/scripts/check-asset-size.mjs --mode=ci
--base=origin/main --head=HEAD`

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Linear

N/A

## Summary

- Refresh the homepage hero title, subtitle, CTA alignment, typography, and footer tagline across all supported locales.
- Replace the hero background and product interface with the supplied high-resolution assets; preserve the interface at a 16 px radius.
- Add regression coverage for hero copy, media sources, layout classes, and localized dictionaries.

## Test plan

- [x] `pnpm exec vitest run tests/unit/app/zoowork-home-body.unit.spec.tsx tests/unit/locales/zoowork-home-dictionary.unit.spec.ts tests/unit/app/marketing-chrome.unit.spec.tsx tests/unit/app/landing-footer.unit.spec.tsx` (58 tests)
- [x] `bash scripts/verify-changed.sh`
- [x] `node web/scripts/check-asset-size.mjs --mode=ci --base=origin/main --head=HEAD`


---
