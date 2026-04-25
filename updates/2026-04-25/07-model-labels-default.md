---
title: "模型选择体验优化：统一标签 + 默认模型标注"
type: "产品基础功能更新"
priority: "中"
date: "2026-04-25"
status: "待审核"
channels: "Discord + changelog"
---

# 模型选择体验优化：统一标签 + 默认模型标注

## 核心宣传点

模型列表统一了展示标签，并标注了当前默认模型，选择时更清晰直观。

## 原始内容

Commit: f1a9ce03537ef01145103cf011c967410890c46f

Message:
feat(web): unify model labels + surface default (ECA-553) (#1317)

## Summary

Fixes two UX problems in the agent settings model dropdown (top-right of
every agent page):

1. **Model names were inconsistent** — `MODEL_LABELS` was duplicated in
two files and had drifted (e.g. `GPT-5.4`, `GLM-5` with hyphens while
`Claude Opus 4.6` used spaces). Worse, newly-added backend models
(`claude-opus-4-7`, `gemma-4-31B-it`) weren't in the dict at all, so the
raw kebab-case id leaked to the UI.
2. **The "Use default" option was opaque** — rendered `Use default
(global model)` without telling the user what the global default
actually resolved to.

## What changed

- **Algorithmic label normalization**
([`web/src/config/models.ts`](../tree/feat/eca-553-default-model-visible/web/src/config/models.ts)):
`backendModelLabel(id)` now computes the display name from the kebab id
(strip `openai/`, strip `-preview`, merge adjacent pure-digit tokens as
`X.Y`, per-token casing via acronym allowlist + title-case default) — so
new backend models format correctly with zero frontend changes. Kept an
empty `BACKEND_MODEL_LABEL_OVERRIDES` as a documented escape hatch for
brand names the algorithm can't guess (e.g. `GPT-4o`).
- **Collapsed duplicated `MODEL_LABELS`**:
`agent-settings/AgentModelSection.tsx` and
`claw-settings/ModelSection.tsx` both now import the shared helper.
- **Surfaced the concrete default** in the popover:
`AgentSettingsPopover` pulls `primary_model` via `useClawSettings` and
passes it down; the empty option now renders `Use default (Claude Sonnet
4.6)` (or whatever the global model is).
- **i18n**: added `agentSettings.useDefaultNamed` to the 7 locales that
already had `agentSettings` (`en/zh/ar/es/ja/ko/pt`); `de/fr/it` fall
back to English through `getNestedValue`.
- **Tests**: new `backendModelLabels.unit.spec.ts` with exact-output
table for 10 real backend ids + naming-rule regex guard (rejects
hyphens, asserts `-preview` ↔ ` Preview` consistency); new
`AgentModelSection.unit.spec.tsx` for both default-label paths; extended
`AgentSettingsPopover.unit.spec.tsx` to mock `useClawSettings` (popover
now calls it).

## Before → After (for visible dropdown rows)

| backend id | before | after |
|---|---|---|
| `openai/claude-opus-4-7` | `claude-opus-4-7` | `Claude Opus 4.7` |
| `gemma-4-31B-it` | `gemma-4-31B-it` | `Gemma 4 31B IT` |
| `openai/gpt-5.4` | `GPT-5.4` | `GPT 5.4` |
| `openai/glm-5` | `GLM-5` | `GLM 5` |
| `""` (default) | `Use default (global model)` | `Use default (Claude
Sonnet 4.6)` |

## Test plan

- [x] `cd web && pnpm lint` — clean
- [x] `cd web && pnpm exec tsc --noEmit` — clean
- [x] `cd web && pnpm test
tests/unit/config/backendModelLabels.unit.spec.ts
tests/unit/components/AgentModelSection.unit.spec.tsx
tests/unit/components/AgentSettingsPopover.unit.spec.tsx` — 34 tests
pass
- [ ] Manual: open an agent chat, click settings (top-right), verify the
default option reads `Use default (<concrete model name>)` and all other
options use consistent casing/spacing, no hyphens.
- [ ] Manual: open `/claw-settings`, confirm the Primary Model dropdown
uses the same labels.

Closes ECA-553.

PR Description:
## Summary

Fixes two UX problems in the agent settings model dropdown (top-right of every agent page):

1. **Model names were inconsistent** — `MODEL_LABELS` was duplicated in two files and had drifted (e.g. `GPT-5.4`, `GLM-5` with hyphens while `Claude Opus 4.6` used spaces). Worse, newly-added backend models (`claude-opus-4-7`, `gemma-4-31B-it`) weren't in the dict at all, so the raw kebab-case id leaked to the UI.
2. **The "Use default" option was opaque** — rendered `Use default (global model)` without telling the user what the global default actually resolved to.

## What changed

- **Algorithmic label normalization** ([`web/src/config/models.ts`](../tree/feat/eca-553-default-model-visible/web/src/config/models.ts)): `backendModelLabel(id)` now computes the display name from the kebab id (strip `openai/`, strip `-preview`, merge adjacent pure-digit tokens as `X.Y`, per-token casing via acronym allowlist + title-case default) — so new backend models format correctly with zero frontend changes. Kept an empty `BACKEND_MODEL_LABEL_OVERRIDES` as a documented escape hatch for brand names the algorithm can't guess (e.g. `GPT-4o`).
- **Collapsed duplicated `MODEL_LABELS`**: `agent-settings/AgentModelSection.tsx` and `claw-settings/ModelSection.tsx` both now import the shared helper.
- **Surfaced the concrete default** in the popover: `AgentSettingsPopover` pulls `primary_model` via `useClawSettings` and passes it down; the empty option now renders `Use default (Claude Sonnet 4.6)` (or whatever the global model is).
- **i18n**: added `agentSettings.useDefaultNamed` to the 7 locales that already had `agentSettings` (`en/zh/ar/es/ja/ko/pt`); `de/fr/it` fall back to English through `getNestedValue`.
- **Tests**: new `backendModelLabels.unit.spec.ts` with exact-output table for 10 real backend ids + naming-rule regex guard (rejects hyphens, asserts `-preview` ↔ ` Preview` consistency); new `AgentModelSection.unit.spec.tsx` for both default-label paths; extended `AgentSettingsPopover.unit.spec.tsx` to mock `useClawSettings` (popover now calls it).

## Before → After (for visible dropdown rows)

| backend id | before | after |
|---|---|---|
| `openai/claude-opus-4-7` | `claude-opus-4-7` | `Claude Opus 4.7` |
| `gemma-4-31B-it` | `gemma-4-31B-it` | `Gemma 4 31B IT` |
| `openai/gpt-5.4` | `GPT-5.4` | `GPT 5.4` |
| `openai/glm-5` | `GLM-5` | `GLM 5` |
| `""` (default) | `Use default (global model)` | `Use default (Claude Sonnet 4.6)` |

## Test plan

- [x] `cd web && pnpm lint` — clean
- [x] `cd web && pnpm exec tsc --noEmit` — clean
- [x] `cd web && pnpm test tests/unit/config/backendModelLabels.unit.spec.ts tests/unit/components/AgentModelSection.unit.spec.tsx tests/unit/components/AgentSettingsPopover.unit.spec.tsx` — 34 tests pass
- [ ] Manual: open an agent chat, click settings (top-right), verify the default option reads `Use default (<concrete model name>)` and all other options use consistent casing/spacing, no hyphens.
- [ ] Manual: open `/claw-settings`, confirm the Primary Model dropdown uses the same labels.

Closes ECA-553.
