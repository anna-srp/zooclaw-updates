---
title: "Agent Builder 支持自定义默认模型"
type: "产品基础功能更新"
priority: "高"
date: "2026-07-14"
status: "待审核"
channels: ""
---

# Agent Builder 支持自定义默认模型

## 核心宣传点
在 Agent Builder 提交时可以选择保留平台默认模型，或从模型目录里指定这个 Agent 默认用哪个大模型。

## 原始内容
### PR #2866 — feat(agent-builder): support custom default model (#2866)
作者: kaka-srp | https://github.com/SerendipityOneInc/ecap-workspace/pull/2866

## Linear

https://linear.app/srpone/issue/ECA-1216/agent-builder-%E9%BB%98%E8%AE%A4%E6%A8%A1%E5%9E%8B%E9%80%89%E6%8B%A9%E8%B0%83%E6%95%B4

## Summary

- Add a Submit confirmation dialog that lets Agent Builder users keep the platform default or choose from the same available chat-model catalog.
- Preserve omitted, explicit null, and concrete model semantics through Pack submission and auto-approval.
- Fail closed when a concrete model cannot be verified, while keeping platform-default submission and existing-submission recovery available.
- Keep retry and concurrent-submit behavior idempotent; Sonnet 5 rollout and billing discounts remain out of scope.

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] `pytest -q tests/unit/test_plan_models.py tests/unit/test_agent_builder_routes.py tests/unit/test_agent_builder_service.py` (176 passed)
- [x] `bash scripts/verify-web.sh --no-test <changed Agent Builder paths>`
- [x] Agent Builder frontend unit selection (85 passed)
- [x] Manual local submit persisted `openai/glm-5.2` through submission, Pack, and install state

### PR #2844 — feat(pack-store): add default_model to packs and submissions (#2844)
作者: bill-srp | https://github.com/SerendipityOneInc/ecap-workspace/pull/2844

## Linear
<!-- 无对应 Linear issue；按用户直接需求实现 -->

## Summary
- Add optional `default_model` (free-form string, trimmed, empty → null) to Pack Store `Pack` / `PackSubmission` and every metadata-bearing request/response schema, consolidated via a `DefaultModelMixin` (normalization lives in one place).
- Accept `default_model` on all pack write APIs: enterprise pack create + submission create, internal create / `POST /{pack_id}` update / submission create / from-private. Approval copies the submission's value onto the pack atomically (`approve_submission_and_sync_pack`); `submit_new_version` carries the pack's current value forward when the request omits it.
- Write it to agent config at install time: `agent_install_service.install_agent` → `apply_pack_agent_to_agents_list` seeds `agents.list[].model.primary` from the pack's `default_model` **only when the entry has no model yet**. A user-set per-agent model is never overwritten — and now survives reinstalls (previously the rebuild silently dropped it).
- Refactor: dedupe the literal `_binding_match_pair` / `_merge_agent_bindings` copies from `agent_deploy.py` / `agent_list_config.py` into `bot_config_payload.py` (keeps the jscpd source-duplication gate ≤3.00%).
- dashboard-console: "Default model" input in pack + submission dialogs; threaded through form state, normalization, API types; metadata-refresh preserves the existing value.
- web/app: read-only "Default model" row on `PackDetailView` (agent detail + shared pack pages); added to pack model types incl. `SharedPackResponse` (deliberate allowlist addition — model id is not sensitive).

Design spec: `docs/superpowers/specs/2026-07-13-pack-default-model-design.md`; implementation plan: `docs/superpowers/plans/2026-07-13-pack-default-model.md`.

## Test plan
- [x] Backend TDD per task: schema round-trip/normalization (7 tests), repo/service plumbing incl. approval copy + carry-forward fallback (5), route forwarding (2), install seeding: seeds when absent / preserves user model / omits when unset (3) — all green.
- [x] `bash scripts/verify-py.sh` (ruff, ruff-format, pyright, import-linter) green; jscpd src duplication 2.98% (≤3.00%).
- [x] `bash scripts/verify-changed.sh` green (web guards + tsc + eslint; py static checks).
- [x] dashboard-console `pnpm run typecheck && pnpm test` — 551 tests green (new pack lifecycle test covers create → update/clear → submission override → approval promotion).
- [x] web/app `bash scripts/verify-web.sh` — 7,606 tests green (PackDetailView shows/omits the row).
- [x] Full local backend suite ran (5,757 passed); 4 BDD failures + 89.71% coverage are local-env artifacts (no `redis` host outside the compose network) — CI with full sidecars is the authoritative 90% gate.

## Deploy note
Cross-surface: deploy backend (`claw-interface`) before or together with web/dashboard-console — the frontends read the new response field. Seeding affects new installs/reinstalls only; existing installed agents are untouched until redeployed.
