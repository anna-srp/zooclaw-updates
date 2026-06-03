---
title: "[Skill] align openclaw.json.tmpl with prod for openclaw 2026.5.7"
type: "Skill 上架/更新"
priority: "中"
date: "2026-06-02"
status: "待审核"
channels: ""
---
# [Skill] align openclaw.json.tmpl with prod for openclaw 2026.5.7

## 核心宣传点
来自 ecap-skills 仓库的更新：fix(devcontainer): align openclaw.json.tmpl with prod for openclaw 2026.5.7

## 原始内容
**Commit**: 1901dbb29175024519d523d63d372f56b5342897
**Title**: fix(devcontainer): align openclaw.json.tmpl with prod for openclaw 2026.5.7 (#211)
**Author**: felix-srp
**Date**: 2026-06-02T12:06:18Z

**PR**: #211

### Commit Message
```
fix(devcontainer): align openclaw.json.tmpl with prod for openclaw 2026.5.7 (#211)

* fix(devcontainer): route image tool via openai-completions endpoint (match prod)

The devcontainer's image tool timed out (~50s) on every model. Comparing to a
working prod pod (via openclaw-diagnose) showed the cause: prod routes image
(and its main model) through the openai-completions endpoint, where every model
declares input:[text,image]; the devcontainer had NO imageModel, so image fell
back to model.primary = anthropic/claude-sonnet-4-6 (anthropic-messages), which
doesn't serve multimodal.

Match prod's routing (staging LITELLM host yesy.live kept — confirmed correct):
- agents.defaults.imageModel: primary openai/claude-sonnet-4-6 (+ openai/* fallbacks)
- agents.defaults.model.primary: anthropic/ -> openai/claude-sonnet-4-6
- openai provider: add claude-sonnet-4-6 + claude-haiku-4-5 (input:[text,image])
  so openai/claude-sonnet-4-6 resolves via openai-completions
- pdfModel left on anthropic/claude-sonnet-4-6 (matches prod)
- tools.deny: add x_search — prod denies it; without it the bot reached for the
  misconfigured xAI search instead of the websearch skill

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(devcontainer): allow :18789 ingress origin in gateway controlUi

The Control UI rejects the webchat WebSocket with "origin not allowed"
because --dev only auto-allows the gateway's own port (:18790), but the
UI is reached via the nginx/forwarded ingress on :18789. Declare both
ports explicitly in gateway.controlUi.allowedOrigins.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(devcontainer): drop invalid models.providers.*.enabled key (2026.5.7)

A clean devcontainer rebuild failed `openclaw config validate` with
"models.providers.{openai,anthropic}: Unrecognized key: enabled". The
enabled:true I added in #210 is not a valid provider key in 2026.5.7 (prod
has no such key; the live gateway tolerated it but config-validate rejects
it). Remove it from both providers. Verified: rendered config now passes
`openclaw config validate`.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(devcontainer): use host-header origin fallback instead of hardcoded ports

The enumerated allowedOrigins list (localhost/127.0.0.1 × :18789/:18790) is
brittle: the host-forwarded port is unpredictable (Dev Containers/Zed assigns a
free port if 18789 is taken), and the nginx ingress (:18789) vs gateway (:18790)
ports differ. Any of those changing reintroduces the "origin not allowed" WS
failure.

Replace the list with gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback
= true, which accepts the Control UI/WebChat WS regardless of origin port.
Access is still gated by the gateway token + local-only reachability; origin
(CSRF) checks are moot once dangerouslyDisableDeviceAuth is already on. This is a
dev-container-only config. Verified: gateway accepts a WS from an arbitrary port
and `openclaw config validate` passes.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(devcontainer): bump openai fallback gpt-5.4 -> gpt-5.5 (track newer prod pods)

Newer prod pods route the fallback to gpt-5.5; staging litellm (yesy.live)
serves it. Rename the model def and repoint model.fallbacks + imageModel.fallbacks.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(devcontainer): match prod model capability metadata (contextWindow/contextTokens)

Align the openai-provider model defs to the values prod actually declares
(verified across prod pods): claude-sonnet-4-6 contextWindow 200000 -> 1000000
+ contextTokens 400000 (the devcontainer was understating Sonnet's window,
making the bot compact far earlier than needed); add contextTokens to gpt-5.5
(400000), gemini-3-flash-preview (400000), kimi-k2.6 (262144). claude-haiku-4-5
already matched. Same Sonnet bump applied to the anthropic provider entry for
consistency.

These numbers previously came from the pre-existing devcontainer baseline, not
prod; this commit makes them identical to prod.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description
## What & why

When the devcontainer image bumped to **openclaw 2026.5.7**, the committed `.devcontainer/openclaw.json.tmpl` no longer matched what prod runs, and the gateway's image tool timed out. This PR brings the template in line with a working **prod pod** (verified live via kubectl across several pods) and with 2026.5.7's stricter `openclaw config validate`.

All changes are confined to `.devcontainer/openclaw.json.tmpl` (dev-container only).

## Changes

1. **Image-tool routing via `openai-completions` (match prod).** Route `model.primary` + add an `imageModel` block pointing at `openai/claude-sonnet-4-6`, and define `claude-sonnet-4-6` / `claude-haiku-4-5` under the `openai` provider with `input: [text, image]`. Previously image fell back to the anthropic-messages endpoint and timed out (~50s).

2. **Drop the invalid `models.providers.*.enabled` key.** 2026.5.7's strict schema rejects it (`Unrecognized key`); prod doesn't set it.

3. **Origin handling that survives port changes.** The Control UI/WebChat WS was rejected with "origin not allowed." Rather than enumerate ports (brittle — the host-forwarded port is unpredictable, and nginx ingress `:18789` vs gateway `:18790` differ), use `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback: true`. Access stays gated by the gateway token + local-only reachability; origin (CSRF) checks are moot once `dangerouslyDisableDeviceAuth` is on. Dev-container only.

4. **Bump openai fallback `gpt-5.4` → `gpt-5.5`** to track newer prod pods (staging litellm serves it).

5. **Match prod model capability metadata.** Align `contextWindow`/`contextTokens` to the values prod declares (verified consistent across pods): `claude-sonnet-4-6` `contextWindow` `200000 → 1000000` + `contextTokens 400000` (the template was understating Sonnet's window, forcing premature compaction); add `contextTokens` to `gpt-5.5`/`gemini-3-flash-preview`/`kimi-k2.6`.

## Verification

- Rebuilt the devcontainer locally; gateway + nginx healthy on 2026.5.7.
- Image tool routes via openai-completions (no timeout).
- WS accepted from an arbitrary forwarded port; `openclaw config validate` passes.
- openai-provider model defs verified byte-equal to prod's declared values.

## Known follow-up (not in this PR)
Prod additionally routes `heartbeat`/`compaction` via `openai/claude-haiku-4-5` and keeps a minimal `anthropic` provider stub; this devcontainer still routes those via `anthropic/claude-haiku-4-5`. Functionally fine — left as a separate optional alignment.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

