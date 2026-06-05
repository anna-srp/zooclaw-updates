---
title: "Agent Studio 上线 Connectors 功能：支持连接第三方服务"
type: "新功能上线"
priority: "高"
date: "2026-06-04"
status: "待审核"
channels: ""
sha: "cf9efae8143a21bb71a0f160df13be8bda4a85b7"
repo: "ecap-agent-pack"
pr: "142"
---

# Agent Studio 上线 Connectors 功能：支持连接第三方服务

## 核心宣传点

Agent Studio 新增 Connectors 功能，用户可以在 Studio 中配置和登录第三方服务（如 GitHub、Notion 等），让 Agent 直接调用外部服务完成任务。

## 原始内容

### Commit Message

```
feat(agent-studio): connectors — catalog client + onboarding login (v1.6.0) (#142)
```

### PR Description

## Summary

Adds a **connectors** capability to Agent Studio (`v1.4.2 → v1.6.0`). Creators can discover, inspect, and declare the third-party providers (Notion, Slack, GitHub, Gmail, Google Drive, …) a generated pack expects — and the generated pack's onboarding turns those declarations into clickable OAuth login links for the end user. Backed by the platform connector service (Composio via `ecap-proxy-service`); creators only ever see "connectors."

### 1. Connector catalog client (authoring time)
`scripts/connectors.py` — talks to `GET /composio/providers`:
- `list` — browse the live catalog; **available-only by default** (the catalog carries ~1000 providers but only the handful with an auth-config are connectable), `--all` reveals the rest marked `(unavailable)`.
- `show <name>` — print a provider's action allowlist (read inline from the catalog).
- `add <name> --pack-dir .` — record in the manifest's top-level `connectors:` field (atomic write, symlink-escape guarded). Refuses unknown/unavailable providers with distinct messages.
- `remove <name>` — idempotent removal.

`validate.py check_connectors` is a **release gate**: declared connectors are schema-checked (kebab-case) and validated against the live catalog, failing *closed* if the proxy is unreachable unless `--skip-online-validation` (offline creator runs). `package.py` delegates to this gate at publish time.

> The `connectors:` field is **authoring-time guidance** — nothing consumes it at runtime. The platform's connector plugin surfaces each user's connected+enabled tools dynamically; the field records intent and drives onboarding.

### 2. Onboarding connector login (delivery time)
`templates/onboarding/connect_composio.py` (shipped verbatim into generated packs, self-contained):
- `plan` — reads manifest connectors, checks `GET /composio/connections`, and for each not-yet-connected provider issues `POST /composio/connections/{provider}/connect` (body `{callback_url}`) → `{connected, needs_login:[{provider, display_name, auth_url}], errors}` so onboarding shows inline login links instead of sending the user hunting through Settings.
- `sync` — `PUT enable` for connected-but-disabled providers.

`write_onboarding.py` **self-derives** the connector set from `agent-pack.yaml#connectors` — declaring a connector in Stage 2 is enough; the generator adds the "Connect Your Accounts" onboarding step automatically.

Reference docs updated across the Studio flow (`data-sources.md` Layer 1, `skill-design.md` Stage 2b, `automation.md` Stage 3, `discovery.md`, `testing.md`, `SKILL.md`). Creator-facing prose says "connectors"; "Composio" remains only in the real API path + script/flag identifiers. End users are **prompted to connect during onboarding** (one-click login links); the **Settings → Connectors** menu is the management fallback (label rendered in the user's language).

## Testing

**202 unit tests** — 98 connector (`scripts/tests`, stdlib-only) + 104 spec/validate (`agent-studio/tests`). Covers YAML parse/splice round-trips, exit-code contract (0/1/2), error classification, atomic write + symlink-escape guard, onboarding plan/sync JSON contract, the available-only/`--all` filter.

**End-to-end against live staging** (Linux docker devcontainer, real Cloudflare-fronted path): list=11 providers, show=actions inline, add↔remove round-trip, exit 1 (unknown) / exit 2 (401, unreachable), `connect plan`→real OAuth URL, `sync`, validate gate pass/fail-closed/skip-online.

**Hand-tested in webchat** (staging account, sonnet-4-6): drove the Discovery → confirmation flow for a Gmail pack. Verified `google-mail` is the correct live provider id (Gmail, available, 20 actions) and tightened three creator/end-user touchpoints surfaced by the test — present the connector by display name (*Gmail*, not the `google-mail` slug); frame onboarding (not Settings) as the primary connect path; correct the menu label to **Settings → Connectors** (and the step name to "Connect Your Accounts").

**Probed live prod** (bot `0ae5098c`): the Composio contract matches the PR's assumptions (1042 providers, 11 available, field schema, 404 classification, `connect` requires `callback_url`). No code change was needed.

## Reviews

Reviewed by Claude + Codex across multiple rounds (catalog client, Composio migration, onboarding, cleanup, final pass); all findings fixed or dispositioned. Latest dual review: **READY** (Codex's 4 final findings reconciled — TOCTOU noted for a follow-up PR, the rest withdrawn).

## Notes

- **`--pack-dir` is unchanged** in this PR (stays `required=True`). The cleanup to default/remove it (and close the manifest-write TOCTOU) is deliberately deferred to a separate PR — preserved at tag `pack-dir-removal-wip` with a design doc.
- `origin/main` is **merged in** (resolved 2 conflicts; branch is current at v1.6.0).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

