# ecap-skills Commits — 2026-05-13

仓库: SerendipityOneInc/ecap-skills  
日期: 2026-05-13 (UTC)  
Commits 数量: 1

---

## Commit 1

**SHA**: 27552e67  
**作者**: 未知  
**日期**: 2026-05-13  
**PR**: #194

### 完整 Commit Message

```
feat(zooclaw-connectors): add skill for third-party connector access via ecap-proxy-service (#194)

* feat(integrations): add skill for third-party connector access via ecap-proxy-service

Thin CLI wrapper around the ecap-proxy-service /integrations/* API so an agent
can discover what the user has connected (GitHub, Linear, Slack, Notion, Google
services, etc.) and invoke tools without per-service skills.

- Single integrations.py with subcommands: list-connectors, list-connections,
  list-tools <provider>, execute <provider> <action>.
- Auth mode picked from env: USER_INTERNAL_TOKEN (User-JWT) takes priority over
  ECAP_PROXY_API_KEY + ECAP_END_USER_ID (Service-key). end_user_id is sent only
  via X-End-User-Id header (proxy refuses it in body/query).
- One HTTP call per invocation. Two-phase write confirmation is owned by the
  agent: first call returns summary, agent shows it, second call re-invokes with
  --confirmed. Script stays stateless.
- User-Agent: ecap-skill/1.0 on every call per CLAUDE.md §2.
- Upstream JSON error envelopes surfaced as-is on stderr so error_code and
  recovery_hint reach the agent.

Compliance:
- C1: only canonical env names; no alias fallback.
- C3: requires.env == os.getenv calls without defaults (ECAP_PROXY_BASE_URL).
- C4: .env.example omitted — all env vars are platform-injected.
- C5: USER_INTERNAL_TOKEN / ECAP_PROXY_API_KEY / ECAP_END_USER_ID read with ""
  defaults; documented in Prerequisites as optional overrides.
- C6: {baseDir}/scripts/... paths, Path Resolution Rule at top, no .claude/skills/
  substring. Verified locally via .github/scripts/lint_skills.py.

* refactor(zooclaw-connectors): rename skill from integrations

- Directory: integrations/ → zooclaw-connectors/
- Script: integrations.py → zooclaw-connectors.py
- SKILL.md frontmatter name + title + path-resolution rule + Quick Start
  examples updated to the new name.

References to the proxy's /integrations/* URL path are intentionally kept —
that's the upstream API path.
```

### PR #194 Body

```
## Summary

New `zooclaw-connectors/` skill that lets an agent reach the user's connected third-party services
(GitHub, Linear, Slack, Notion, Google Drive/Calendar/Gmail, Jira, etc.) via the
ecap-proxy-service `/integrations/*` API. Follows the upstream spec at
ecap-proxy-service/docs/integrations-skill.md, with project-specific adjustments noted below.

### What's in the box

- **`zooclaw-connectors/SKILL.md`** — frontmatter, path rule, decision flow, auth modes,
  two-phase write-confirmation, full error-code taxonomy, caching guidance, end-to-end examples.
- **`zooclaw-connectors/scripts/zooclaw-connectors.py`** — single CLI with four subcommands:
  - `list-connectors`            → `GET /integrations/connectors`
  - `list-connections`           → `GET /integrations/connections`
  - `list-tools <provider>`      → `GET /integrations/<provider>/tools`
  - `execute <provider> <action> --params-json '<json>' [--confirmed]` → `POST /integrations/execute`

### Design decisions

- **Env name**: uses the repo-canonical `ECAP_PROXY_BASE_URL`
- **Auth-mode priority**: `USER_INTERNAL_TOKEN` set → User-JWT mode wins.
  Otherwise `ECAP_PROXY_API_KEY` + `ECAP_END_USER_ID` → Service-key mode.
  Neither → `auth_missing` at startup, exit 2.
```
