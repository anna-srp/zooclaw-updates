---
title: "feat(mcp): require confirmation for Feishu approval writes (#3801)"
type: "新功能"
priority: "高"
date: "2026-09-21"
status: "待审核"
channels: ""
---

# 飞书审批类写操作现在每次都需要确认

## 核心宣传点

官方 staging / 生产的飞书审批 MCP 端点改成固定策略：查询类的抄送列表、待办列表、已办列表和审批详情继续自动执行；但写操作——审批评论和审批同意/拒绝——每次调用都必须经过确认。这个策略在能力发现之前就声明好，用户的权限覆盖设置、能力元数据或历史上的单工具选择都无法绕过它，只有「允许一次」和「拒绝」两种回答有效，普通的放行规则和此前会话里给过的授权都不管用。需要注意生效范围：部署顺序是 Engine worker → controld → ECAP，覆盖新建 Agent 以及存量 Agent 下一次成功保存设置或 MCP 新建/编辑/启停/测试同步之后的状态。已经处于同步正常状态的连接不会自动排队更新，也就是说——光部署并不会立刻保护所有存量 Agent。

## 分级

- 内部：P0
- 外部：A
- 发布状态：已合并待发版

## PR 说明

## Behavior

Official staging/production Feishu approval MCP endpoints use a fixed policy: `approval_list_cc`, `approval_list_pending`, `approval_list_done` and `approval_get` execute automatically; `approval_comment` and `approval_decide` require confirmation for every invocation. Other MCP endpoints retain existing behavior.

Both Agent Settings saves and personal MCP sync use `server_for()`. The six-tool policy is declared before catalog discovery; tool enable/disable remains supported. User permission overrides/reset settings are absent, and catalog metadata or historical per-tool choices cannot override the fixed policy.

The two writes now include `requireConfirmation: true`. Depends on [Engine #1565](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1565): its existing approval chain enforces the per-call requirement despite ordinary allow rules, permission sugar and prior session grants; only allow-once/deny are valid. Companion channel confirmation behavior is [ACS #139](https://github.com/SerendipityOneInc/agent-channel-service/pull/139).

## Rollout

Deploy Engine worker first, controld second, then ECAP. This release covers new Agents and existing Agents at their next successful Settings save or MCP create/edit/enable/disable/test synchronization, plus the existing pending/error reconciliation paths. Connections already at `sync_status=ok` are not automatically queued: **deployment alone does not immediately protect all existing Agents**. No fleet backfill or live-data mutation is included. New snapshots do not rewrite already-pinned turns.

## Validation

- 21 targeted ECAP tests and the backend static gate passed; CI passed. Engine companion tests cover rendered configuration, parser/evaluator precedence, prior grants and repeated confirmation.
- Earlier real Feishu validation was superseded by run `approval-short-final-20260920134833`, documented in [ACS #139](https://github.com/SerendipityOneInc/agent-channel-service/pull/139): ACS `c3c6016`, Engine `8bceb74f`, ECAP materialization `0598e030a`, MCP `9d75157`. Five automatic real-model/Feishu API scenarios passed. Manual confirmation then cancellation wrote exactly one comment, left the cancelled comment absent, completed both turns, and delivered/acknowledged each approval prompt and resolution receipt once.
- The earlier cancellation-follow-up failure is superseded for that isolated local lane: no automatic retry or new approval occurred; the user accepted wording that requires an explicit new request to retry. Internal tool-name display was shortened. This real-channel result covers Engine `8bceb74f`; the latest Engine head is covered by the supplemental tests below.
- That Feishu lane exported ECAP materialization rather than exercising the complete UI save/sync path. It is not a deployed-staging/production verdict.

## Stored URL canonicalization follow-up

At `d8f8c2bd5`, `fixed_tool_permissions()` now normalizes URLs with the existing `HttpUrl` adapter before policy matching. This directly addresses the Codex dot-segment finding even for raw persisted records that did not pass through today's write boundary. Literal/encoded dot segments normalize, then the actual MCP router's single percent-decoding rule applies. Persisted URLs are not rewritten; only the two official Feishu approval hosts receive fixed rules. Invalid HTTP URLs return no fixed policy.

- **10 new raw-record cases failed before the fix**; **90 related tests pass after the fix and rebase**, including both official hosts, runtime/public agreement and negative cases for encoded separators, double encoding and traversal to another endpoint.
- Claude's cross-repository evidence request is addressed in the checked-in spec's **Router contract evidence** section: actual MCP package `9d751573`, isolated Go handler, exact HTTP results, no external API writes. It is not a deployed-ingress verdict.
- This supersedes the earlier decision to leave the classification boundary unchanged. Both review labels are left to the new automated review; they will not be removed manually. CI passed at this head: 11,880 backend tests passed (5 skipped), coverage 89.69%; lint/typecheck passed. Both Codex and Claude now report APPROVE / no new findings. Claude reassessed the completed CI evidence in [its updated review](https://github.com/SerendipityOneInc/ecap-workspace/pull/3801#issuecomment-5755280388); both need-human-review labels were removed by the review workflow. No labels were manually removed in this follow-up.
- No full local model/channel E2E rerun: the change is confined to endpoint classification. Existing rollout limits and earlier E2E commit pins below still apply.

## Percent-encoded approval path fix — 2026-09-21 UTC

Follow-up boundary audit found that the actual approval MCP router accepts percent-encoded equivalents of `/mcp`, while ECAP previously compared the raw path. At `0b337257a`, the fixed-policy classifier decodes the path exactly once before comparison. The policy still applies only to the official Feishu approval endpoints; other MCP endpoints and ordinary approval/session-grant behavior are unchanged.

- Regression reproduced before the fix: **12 failed, 27 passed**. After the fix and rebase: **77 tests passed** across fixed permissions, resource runtime, MCP sync and MCP service.
- Both official hosts are covered through `McpConnectionWrite`/`HttpUrl`, runtime policy, public metadata and sync. Encoded equivalents (`/%6dcp`, `/%6Dcp`, `/m%63p`, `/mc%70`, `/%6d%63%70`) retain the mandatory confirmation policy; double encoding, encoded separators, extra segments, NUL and malformed escapes do not broaden the match.
- A local `httptest` probe against the actual approval MCP package at `9d751573` confirmed HTTP 200 and both write-tool definitions for all five equivalent paths, and HTTP 404 for the tested non-equivalent paths. This used a dummy API key and `tools/list` only, with no Feishu API calls or writes; it is handler-level evidence, not a deployed ingress verdict.
- Repository-venv Ruff, formatting, Pyright and import contracts passed. CI passed on `0b337257a`, including backend tests/lint/typecheck, duplication and CodeQL. Review adjudication is recorded below; green review jobs are not being represented as finding-free reviews.
- Review adjudication at this head: Codex raised dot-segment canonicalization. The cited `/mcp/.` and `/mcp/%2e` inputs normalize to `/mcp/` in the actual `McpConnectionWrite` boundary; `/x/../mcp` and `/x/%2e%2e/mcp` normalize to `/mcp`. All four retain both fixed `always_ask` rules in a direct boundary/classifier probe. `mcp_service.py` persists `str(resource.server_url)` on create/update, so the claimed user-input bypass was not reproduced. Additionally, the actual MCP handler returns 404 for `/mcp/`; this review did not establish an executable bypass. This earlier decision is superseded by the stored-URL canonicalization follow-up above.
- Claude reported no blocking code findings and requested evidence of router decoding and rollout scope. The actual-package handler probe above supplies the former; the documented no-backfill rollout remains unchanged. An empty fixed-policy result is **not** fail-closed: ordinary permissions would apply, which is why the encoded-path mismatch was fixed.
- No new full model/channel local E2E was run. The focused classifier/sync regressions and real-handler probe cover this change; prior E2E remains valid only for its recorded heads and scope. Full browser/auth/Mongo and deployed channel acceptance remain separate follow-ups.

## Terminal-dot hostname review fix — 2026-09-21 UTC

Addresses [kaka's hostname canonicalization finding](https://github.com/SerendipityOneInc/ecap-workspace/pull/3801#issuecomment-5754928556). `fixed_tool_permissions()` removes one terminal DNS root dot before matching the official hostname. HTTPS, exact official-host allowlist, default/443 port and `/mcp` path checks remain in place; persisted URLs and other MCP permissions are unchanged. This protects both existing stored dotted URLs and newly validated input without a data rewrite.

- Regression confirmed before the fix: five failing cases (both official hosts, upper/lowercase variants through `McpConnectionWrite`/`HttpUrl`, and personal MCP sync).
- After the fix: **59 tests passed** across fixed permissions, resource runtime, MCP sync and MCP service. Tests also reject lookalike domains with a terminal dot, HTTP, nonstandard ports and other paths; runtime policy and public permission metadata agree.
- Repository-venv Ruff check/format, Pyright and import contracts passed, as did pre-commit checks. Initial global-Ruff and test-typing setup failures were corrected; no unrelated files changed.
- CI on `124c33ac9` passed, including backend tests/lint/typecheck, duplication and CodeQL. Both Codex and Claude reviews reported no findings.
- The earlier local E2E below remains evidence for its explicitly pinned heads, not a rerun at this follow-up commit. This classifier-only fix is covered by reproducing boundary/sync regressions; no new full local model/channel E2E was run. Deployment/UI acceptance limits below remain unchanged.

## Latest supplemental validation — 2026-09-21 UTC

Frozen heads: ECAP `0598e030a`, ACS `c3c6016`, Engine `b829ca478`. Fresh isolated A102 rootless run `approval-compat-20260921023553`; no product source changes or production/staging data mutations.

- **Six runtime scenarios passed** using real controld HTTP, PostgreSQL, Redis, Temporal, worker and an authorized real model, with a local synthetic non-Feishu MCP write-count fixture:
  - Ordinary automatic tool: no approval prompt, exactly one execution.
  - Ordinary `allow-always`: first call approved; the next turn in the same session executes once without another prompt.
  - Duplicate `allow-once` confirmations: exactly one execution and one resolution event.
  - Duplicate denials: zero executions and one resolution event.
  - Required confirmation: an `allow-always` batch containing another valid event returns HTTP 400 with no partial event delivery; a later valid `allow-once` still completes.
- **ECAP → real Engine service integration passed**: actual `runtime_bindings()` plus `EngineClient` config-version creation/activation and readback; personal MCP sync restores the fixed policy on a disposable Agent; unrelated MCP configuration and direct exposure remain intact. Ownership/catalog repositories are isolated fixtures and Mongo access is explicitly prohibited. This is not full browser/auth/Mongo Settings transaction E2E.
- **Engine: 276 tests passed in four targeted files** (`approvals`, `sessions-api`, `agents-service`, `tool-hooks`), including Temporal grant carryover, denial/timeout and resolver validation.
- **ACS: 194 tests passed in four targeted files** (`channel-approval-event`, `chat-command-service`, `inbound-runtime-service`, `receiver-input-worker`). Test-tool caveat: used Vitest **4.1.10**, mounted read-only from the isolated Engine tools volume, rather than ACS-declared 4.1.11, after npm 10.9.8 failed installing test tools with `edgesOut` before any tests ran. ACS product dependency manifests/lock and pinned runtime dependencies were unchanged.

Verdicts: environment valid for this isolated scope with the test-tool caveat above; workflow completion PASS; deterministic QA PASS; API/tool execution acceptance PASS. No regression observed in the tested non-Feishu automatic execution or ordinary session grants. This round did not send real channel messages or establish a deployed-staging/production verdict.

All task-owned containers are stopped; evidence and volumes retained privately. No workers, tmux sessions or sidebar workspaces were created.

**Further testing:** another identical local E2E round is not needed while these heads and configuration remain unchanged. Full browser/auth/Mongo save-transaction coverage remains unverified; use a dedicated safe profile or staging canary, then validate the newly deployed channel chain. Re-run affected scenarios if relevant code/configuration changes. These remaining checks are not implied by the local PASS above.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `697b685ee43e88817728fdc391678b5b6907f176`
- PR: #3801
- 作者：sharplee-srp
- 日期：2026-09-21T07:36:54Z

### Commit Message

```
feat(mcp): require confirmation for Feishu approval writes (#3801)

## Behavior

Official staging/production Feishu approval MCP endpoints use a fixed
policy: `approval_list_cc`, `approval_list_pending`,
`approval_list_done` and `approval_get` execute automatically;
`approval_comment` and `approval_decide` require confirmation for every
invocation. Other MCP endpoints retain existing behavior.

Both Agent Settings saves and personal MCP sync use `server_for()`. The
six-tool policy is declared before catalog discovery; tool
enable/disable remains supported. User permission overrides/reset
settings are absent, and catalog metadata or historical per-tool choices
cannot override the fixed policy.

The two writes now include `requireConfirmation: true`. Depends on
[Engine
#1565](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1565):
its existing approval chain enforces the per-call requirement despite
ordinary allow rules, permission sugar and prior session grants; only
allow-once/deny are valid. Companion channel confirmation behavior is
[ACS
#139](https://github.com/SerendipityOneInc/agent-channel-service/pull/139).

## Rollout

Deploy Engine worker first, controld second, then ECAP. This release
covers new Agents and existing Agents at their next successful Settings
save or MCP create/edit/enable/disable/test synchronization, plus the
existing pending/error reconciliation paths. Connections already at
`sync_status=ok` are not automatically queued: **deployment alone does
not immediately protect all existing Agents**. No fleet backfill or
live-data mutation is included. New snapshots do not rewrite
already-pinned turns.

## Validation

- 21 targeted ECAP tests and the backend static gate passed; CI passed.
Engine companion tests cover rendered configuration, parser/evaluator
precedence, prior grants and repeated confirmation.
- Earlier real Feishu validation was superseded by run
`approval-short-final-20260920134833`, documented in [ACS
#139](https://github.com/SerendipityOneInc/agent-channel-service/pull/139):
ACS `c3c6016`, Engine `8bceb74f`, ECAP materialization `0598e030a`, MCP
`9d75157`. Five automatic real-model/Feishu API scenarios passed. Manual
confirmation then cancellation wrote exactly one comment, left the
cancelled comment absent, completed both turns, and
delivered/acknowledged each approval prompt and resolution receipt once.
- The earlier cancellation-follow-up failure is superseded for that
isolated local lane: no automatic retry or new approval occurred; the
user accepted wording that requires an explicit new request to retry.
Internal tool-name display was shortened. This real-channel result
covers Engine `8bceb74f`; the latest Engine head is covered by the
supplemental tests below.
- That Feishu lane exported ECAP materialization rather than exercising
the complete UI save/sync path. It is not a deployed-staging/production
verdict.

## Stored URL canonicalization follow-up

At `d8f8c2bd5`, `fixed_tool_permissions()` now normalizes URLs with the
existing `HttpUrl` adapter before policy matching. This directly
addresses the Codex dot-segment finding even for raw persisted records
that did not pass through today's write boundary. Literal/encoded dot
segments normalize, then the actual MCP router's single percent-decoding
rule applies. Persisted URLs are not rewritten; only the two official
Feishu approval hosts receive fixed rules. Invalid HTTP URLs return no
fixed policy.

- **10 new raw-record cases failed before the fix**; **90 related tests
pass after the fix and rebase**, including both official hosts,
runtime/public agreement and negative cases for encoded separators,
double encoding and traversal to another endpoint.
- Claude's cross-repository evidence request is addressed in the
checked-in spec's **Router contract evidence** section: actual MCP
package `9d751573`, isolated Go handler, exact HTTP results, no external
API writes. It is not a deployed-ingress verdict.
- This supersedes the earlier decision to leave the classification
boundary unchanged. Both review labels are left to the new automated
review; they will not be removed manually. CI passed at this head:
11,880 backend tests passed (5 skipped), coverage 89.69%; lint/typecheck
passed. Both Codex and Claude now report APPROVE / no new findings.
Claude reassessed the completed CI evidence in [its updated
review](https://github.com/SerendipityOneInc/ecap-workspace/pull/3801#issuecomment-5755280388);
both need-human-review labels were removed by the review workflow. No
labels were manually removed in this follow-up.
- No full local model/channel E2E rerun: the change is confined to
endpoint classification. Existing rollout limits and earlier E2E commit
pins below still apply.

## Percent-encoded approval path fix — 2026-09-21 UTC

Follow-up boundary audit found that the actual approval MCP router
accepts percent-encoded equivalents of `/mcp`, while ECAP previously
compared the raw path. At `0b337257a`, the fixed-policy classifier
decodes the path exactly once before comparison. The policy still
applies only to the official Feishu approval endpoints; other MCP
endpoints and ordinary approval/session-grant behavior are unchanged.

- Regression reproduced before the fix: **12 failed, 27 passed**. After
the fix and rebase: **77 tests passed** across fixed permissions,
resource runtime, MCP sync and MCP service.
- Both official hosts are covered through
`McpConnectionWrite`/`HttpUrl`, runtime policy, public metadata and
sync. Encoded equivalents (`/%6dcp`, `/%6Dcp`, `/m%63p`, `/mc%70`,
`/%6d%63%70`) retain the mandatory confirmation policy; double encoding,
encoded separators, extra segments, NUL and malformed escapes do not
broaden the match.
- A local `httptest` probe against the actual approval MCP package at
`9d751573` confirmed HTTP 200 and both write-tool definitions for all
five equivalent paths, and HTTP 404 for the tested non-equivalent paths.
This used a dummy API key and `tools/list` only, with no Feishu API
calls or writes; it is handler-level evidence, not a deployed ingress
verdict.
- Repository-venv Ruff, formatting, Pyright and import contracts passed.
CI passed on `0b337257a`, including backend tests/lint/typecheck,
duplication and CodeQL. Review adjudication is recorded below; green
review jobs are not being represented as finding-free reviews.
- Review adjudication at this head: Codex raised dot-segment
canonicalization. The cited `/mcp/.` and `/mcp/%2e` inputs normalize to
`/mcp/` in the actual `McpConnectionWrite` boundary; `/x/../mcp` and
`/x/%2e%2e/mcp` normalize to `/mcp`. All four retain both fixed
`always_ask` rules in a direct boundary/classifier probe.
`mcp_service.py` persists `str(resource.server_url)` on create/update,
so the claimed user-input bypass was not reproduced. Additionally, the
actual MCP handler returns 404 for `/mcp/`; this review did not
establish an executable bypass. This earlier decision is superseded by
the stored-URL canonicalization follow-up above.
- Claude reported no blocking code findings and requested evidence of
router decoding and rollout scope. The actual-package handler probe
above supplies the former; the documented no-backfill rollout remains
unchanged. An empty fixed-policy result is **not** fail-closed: ordinary
permissions would apply, which is why the encoded-path mismatch was
fixed.
- No new full model/channel local E2E was run. The focused
classifier/sync regressions and real-handler probe cover this change;
prior E2E remains valid only for its recorded heads and scope. Full
browser/auth/Mongo and deployed channel acceptance remain separate
follow-ups.

## Terminal-dot hostname review fix — 2026-09-21 UTC

Addresses [kaka's hostname canonicalization
finding](https://github.com/SerendipityOneInc/ecap-workspace/pull/3801#issuecomment-5754928556).
`fixed_tool_permissions()` removes one terminal DNS root dot before
matching the official hostname. HTTPS, exact official-host allowlist,
default/443 port and `/mcp` path checks remain in place; persisted URLs
and other MCP permissions are unchanged. This protects both existing
stored dotted URLs and newly validated input without a data rewrite.

- Regression confirmed before the fix: five failing cases (both official
hosts, upper/lowercase variants through `McpConnectionWrite`/`HttpUrl`,
and personal MCP sync).
- After the fix: **59 tests passed** across fixed permissions, resource
runtime, MCP sync and MCP service. Tests also reject lookalike domains
with a terminal dot, HTTP, nonstandard ports and other paths; runtime
policy and public permission metadata agree.
- Repository-venv Ruff check/format, Pyright and import contracts
passed, as did pre-commit checks. Initial global-Ruff and test-typing
setup failures were corrected; no unrelated files changed.
- CI on `124c33ac9` passed, including backend tests/lint/typecheck,
duplication and CodeQL. Both Codex and Claude reviews reported no
findings.
- The earlier local E2E below remains evidence for its explicitly pinned
heads, not a rerun at this follow-up commit. This classifier-only fix is
covered by reproducing boundary/sync regressions; no new full local
model/channel E2E was run. Deployment/UI acceptance limits below remain
unchanged.

## Latest supplemental validation — 2026-09-21 UTC

Frozen heads: ECAP `0598e030a`, ACS `c3c6016`, Engine `b829ca478`. Fresh
isolated A102 rootless run `approval-compat-20260921023553`; no product
source changes or production/staging data mutations.

- **Six runtime scenarios passed** using real controld HTTP, PostgreSQL,
Redis, Temporal, worker and an authorized real model, with a local
synthetic non-Feishu MCP write-count fixture:
  - Ordinary automatic tool: no approval prompt, exactly one execution.
- Ordinary `allow-always`: first call approved; the next turn in the
same session executes once without another prompt.
- Duplicate `allow-once` confirmations: exactly one execution and one
resolution event.
  - Duplicate denials: zero executions and one resolution event.
- Required confirmation: an `allow-always` batch containing another
valid event returns HTTP 400 with no partial event delivery; a later
valid `allow-once` still completes.
- **ECAP → real Engine service integration passed**: actual
`runtime_bindings()` plus `EngineClient` config-version
creation/activation and readback; personal MCP sync restores the fixed
policy on a disposable Agent; unrelated MCP configuration and direct
exposure remain intact. Ownership/catalog repositories are isolated
fixtures and Mongo access is explicitly prohibited. This is not full
browser/auth/Mongo Settings transaction E2E.
- **Engine: 276 tests passed in four targeted files** (`approvals`,
`sessions-api`, `agents-service`, `tool-hooks`), including Temporal
grant carryover, denial/timeout and resolver validation.
- **ACS: 194 tests passed in four targeted files**
(`channel-approval-event`, `chat-command-service`,
`inbound-runtime-service`, `receiver-input-worker`). Test-tool caveat:
used Vitest **4.1.10**, mounted read-only from the isolated Engine tools
volume, rather than ACS-declared 4.1.11, after npm 10.9.8 failed
installing test tools with `edgesOut` before any tests ran. ACS product
dependency manifests/lock and pinned runtime dependencies were
unchanged.

Verdicts: environment valid for this isolated scope with the test-tool
caveat above; workflow completion PASS; deterministic QA PASS; API/tool
execution acceptance PASS. No regression observed in the tested
non-Feishu automatic execution or ordinary session grants. This round
did not send real channel messages or establish a
deployed-staging/production verdict.

All task-owned containers are stopped; evidence and volumes retained
privately. No workers, tmux sessions or sidebar workspaces were created.

**Further testing:** another identical local E2E round is not needed
while these heads and configuration remain unchanged. Full
browser/auth/Mongo save-transaction coverage remains unverified; use a
dedicated safe profile or staging canary, then validate the newly
deployed channel chain. Re-run affected scenarios if relevant
code/configuration changes. These remaining checks are not implied by
the local PASS above.
```

来源：SerendipityOneInc/ecap-workspace @ 697b685e，PR #3801，作者 sharplee-srp。