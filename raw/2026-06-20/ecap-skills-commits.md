# ecap-skills commits — 2026-06-20

共 1 个 commit

---

## `0fb653f92f`

- **作者**: Chris@ZooClaw
- **日期**: 2026-06-20T14:35:59Z
- **PR**: #215
- **链接**: https://github.com/SerendipityOneInc/ecap-skills/commit/0fb653f92f920b50aacbd2f9918cd29c90b6f9a7

### 完整 commit message

```
perf(ci): send Feishu notifications via lark-cli (#215)

* perf(ci): send Feishu notifications via lark-cli

Swap the Docker-based feishu-actions@main notifier for the fast
srp-actions/lark-notify@main composite action across all three
publish jobs. lark-notify sends a Feishu interactive card via
lark-cli (no Docker) when chat_id + app creds are present, else
falls back to the legacy custom-bot webhook. Card bodies preserved.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* ci: add dual-layer AI review (Claude + Codex) mirroring ecap-workspace

Adds the auto-review umbrella (srp-actions claude-review + codex-review +
auto-review-gate) so ecap-skills PRs get the same two-layer AI review as
ecap-workspace. Required secrets (APP_ID/APP_PRIVATE_KEY/AWS_ROLE_TO_ASSUME,
AZURE_OPENAI_API_KEY/CODEX_APP_ID/CODEX_APP_PRIVATE_KEY) and
AZURE_OPENAI_ENDPOINT var are already available org-level.

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What

Swap the slow Docker-based `SerendipityOneInc/feishu-actions@main` notifier for the fast `SerendipityOneInc/srp-actions/lark-notify@main` composite action across all three publish jobs (dev / staging / production) in `publish-skills.yml`.

## Why

`feishu-actions@main` runs as a Docker action, which is slow to pull and start on every notify step. `lark-notify` (already on `srp-actions` main) sends a Feishu interactive card via `lark-cli` (fast, no Docker) when `chat_id` + app creds are present, and otherwise falls back to the legacy custom-bot webhook — so behavior is preserved while startup latency drops.

## Changes

- All three `Notify Lark Bot` steps now `uses: SerendipityOneInc/srp-actions/lark-notify@main`.
- Inputs consolidated into a single `with:` (no `env:`): `chat_id` (with `vars.LARK_CHAT_GITHUB_ACTIONS` fallback), `app_id`/`app_secret` from `LARKSUITE_CLI_*` secrets, plus the existing `FEISHU_CUSTOMERBOT_WEBHOOK`/`_SECRET` for legacy fallback.
- `MSGTYPE` → `msgtype` (`interactive`), `CONTENT` → `content` — card bodies preserved byte-for-byte (dev / staging / production).

No merge / no auto-merge.

