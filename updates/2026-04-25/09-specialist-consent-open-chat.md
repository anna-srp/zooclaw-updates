---
title: "专家 Agent 新增同意授权 + 开放对话卡片"
type: "产品基础功能更新"
priority: "中"
date: "2026-04-25"
status: "待审核"
channels: "Discord + changelog"
---

# 专家 Agent 新增同意授权 + 开放对话卡片

## 核心宣传点

调用专家 Agent 时新增授权确认流程，并在消息中展示直接打开对话的快捷卡片。

## 原始内容

Commit: 5cea8af5f80ddd695df621047f06a97cc06a013a

Message:
feat(web): specialist consent + open-chat cards in agent messages (#1245)

## Summary

Renders three new fenced code-block patterns emitted by agents into
interactive chat cards:

- `zooclaw-hire-specialist-consent@<id>` → neutral **Confirm / Cancel**
card
- `zooclaw-fire-specialist-consent@<id>` → destructive variant (red
chrome + ⚠️ banner)
- `zooclaw-open-specialist-chat@<id>` → avatar + greeting + send-style
CTA pill; click refreshes the local agent catalog then routes to
`/chat?agent_id=<id>`

Agent identity (display name, avatar) is resolved from the local catalog
using the info-string `@id`; the body markdown is presentational only.
Consent buttons send a localized, fully-composed message (`{label}
{action} {name}` — e.g. `确认雇佣 Market Analyst` / `confirm hiring Market
Analyst`). `{name}` prefers the catalog display name, falls back to
humanized agent id.

### Graceful degradation
- No quoted labels / no id → inline markdown render (not a raw code
block) so body text / URLs stay readable
- Everything unknown → falls through to the standard code-block renderer
(last resort)

### i18n
New keys across all 10 locales:
- `genClaw.specialistCardGreeting` — "Say hi 👋" / "打个招呼 👋" / …
- `genClaw.specialistCardAriaLabel` — "Start chat with {name}"
- `genClaw.consentHireMessageTemplate` — "{label} hiring {name}" /
"{label}雇佣 {name}" / …
- `genClaw.consentFireMessageTemplate` — "{label} firing {name}" /
"{label}解雇 {name}" / …

### Architecture note
Cards mounted via `createRoot` in `MarkdownContent`'s hydrate effect run
in a **detached React tree**, so they can't consume `LanguageContext` /
`RouterContext` directly. All context-dependent values (translated
strings, display name, avatar URL, router.push) are pre-resolved in the
main tree and passed as plain props — cards stay purely presentational.

## Test plan

- [x] `pnpm lint` clean
- [x] `pnpm tsc --noEmit` clean
- [x] Targeted vitest: 137 tests green
  - `renderMarkdownToHtml` — info-string parsing + fallback branches
- `SpecialistConsentCard` — hire / fire variants, button consumed state,
locale-agnostic label passthrough
- `SpecialistOpenCard` — avatar image / monogram fallback / img-error
fallback, keyboard activation
- `MarkdownContent` specialist hydration — confirm + cancel message
composition, suppression during streaming, no-labels / no-id degradation
- `OpenClawAssistantMessage` — unchanged behaviors still pass (new
router / team-refresh deps mocked)
- [ ] Manual: hire → confirm → tool runs → success → open-specialist
card appears → click → sidebar reflects new agent on destination page
- [ ] Manual: theme toggle (light + dark) — consent buttons, destructive
chrome, open-card pill all adapt via semantic tokens
- [ ] Manual: locale switch (at least en ↔ zh) — greeting pill + sent
consent message localize

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
Co-authored-by: peter-srp <peter@srp.one>

PR Description:
## Summary

Renders three new fenced code-block patterns emitted by agents into interactive chat cards:

- `zooclaw-hire-specialist-consent@<id>` → neutral **Confirm / Cancel** card
- `zooclaw-fire-specialist-consent@<id>` → destructive variant (red chrome + ⚠️ banner)
- `zooclaw-open-specialist-chat@<id>` → avatar + greeting + send-style CTA pill; click refreshes the local agent catalog then routes to `/chat?agent_id=<id>`

Agent identity (display name, avatar) is resolved from the local catalog using the info-string `@id`; the body markdown is presentational only. Consent buttons send a localized, fully-composed message (`{label} {action} {name}` — e.g. `确认雇佣 Market Analyst` / `confirm hiring Market Analyst`). `{name}` prefers the catalog display name, falls back to humanized agent id.

### Graceful degradation
- No quoted labels / no id → inline markdown render (not a raw code block) so body text / URLs stay readable
- Everything unknown → falls through to the standard code-block renderer (last resort)

### i18n
New keys across all 10 locales:
- `genClaw.specialistCardGreeting` — "Say hi 👋" / "打个招呼 👋" / …
- `genClaw.specialistCardAriaLabel` — "Start chat with {name}"
- `genClaw.consentHireMessageTemplate` — "{label} hiring {name}" / "{label}雇佣 {name}" / …
- `genClaw.consentFireMessageTemplate` — "{label} firing {name}" / "{label}解雇 {name}" / …

### Architecture note
Cards mounted via `createRoot` in `MarkdownContent`'s hydrate effect run in a **detached React tree**, so they can't consume `LanguageContext` / `RouterContext` directly. All context-dependent values (translated strings, display name, avatar URL, router.push) are pre-resolved in the main tree and passed as plain props — cards stay purely presentational.

## Test plan

- [x] `pnpm lint` clean
- [x] `pnpm tsc --noEmit` clean
- [x] Targeted vitest: 137 tests green
  - `renderMarkdownToHtml` — info-string parsing + fallback branches
  - `SpecialistConsentCard` — hire / fire variants, button consumed state, locale-agnostic label passthrough
  - `SpecialistOpenCard` — avatar image / monogram fallback / img-error fallback, keyboard activation
  - `MarkdownContent` specialist hydration — confirm + cancel message composition, suppression during streaming, no-labels / no-id degradation
  - `OpenClawAssistantMessage` — unchanged behaviors still pass (new router / team-refresh deps mocked)
- [ ] Manual: hire → confirm → tool runs → success → open-specialist card appears → click → sidebar reflects new agent on destination page
- [ ] Manual: theme toggle (light + dark) — consent buttons, destructive chrome, open-card pill all adapt via semantic tokens
- [ ] Manual: locale switch (at least en ↔ zh) — greeting pill + sent consent message localize

🤖 Generated with [Claude Code](https://claude.com/claude-code)
