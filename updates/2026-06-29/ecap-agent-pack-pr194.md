---
title: "Agent Studio 头像升级为写实人物肖像"
type: "体验优化"
priority: "低"
date: "2026-06-29"
status: "待审核"
channels: ""
---

# Agent Studio 头像升级为写实人物肖像

## 核心宣传点

Agent Studio 生成的头像从卡通动物形象升级为写实人物肖像，根据 Agent 角色生成专业影棚风格的人像，形象更真实、更有质感。

## 原始内容

### Commit Message

```
feat(agent-studio): avatar prompt → photorealistic human portrait (#194)

Replace the Pixar-animal-mascot avatar prompt with a photorealistic human studio-portrait prompt driven by {role}. Remove the now-unused `animal` field from description.json (schema doc + generator) and its packaging guidance — the claw-interface pack path never reads it (catalog animal is sourced from agent_id), so it's backward compatible. Bumps agent-studio 2.2.1 -> 2.2.2.
```

### PR Description

Replaces the avatar-generation prompt for new packs with a **photorealistic human portrait**, and removes the now-unused `animal` field from `description.json`.

## What changed
- **`templates/avatar-prompt.md`** — swapped the Pixar-style anthropomorphic-**animal** mascot prompt for a **photorealistic human studio portrait** driven by `{role}`. Adopts a clean studio-headshot aesthetic (simple theme-colored backdrop, premium lighting, anti-clutter/anti-text guardrails). Drops the animal/lanyard-prop and the team-distinctness lines (agent-studio generates a *single* pack avatar, not a roster).
- **`references/packaging.md`** — Stage 5b instruction now says `replace {role}` (was `{animal} / {role}`); dropped the `animal` TODO listing-field.
- **`references/description-schema.ts`** + **`scripts/generate_description.py`** — removed the `animal` field from the description.json schema doc and generator.

## Why removing `animal` is safe (backward compatible)
- **No producer requirement:** `validate.py` only checks description.json *exists*; `package.py` only checks `agentPack_id` matches the manifest and ships it as-is. Nothing requires `animal`.
- **No strict schema:** `description-schema.ts` is a reference doc for the Studio LLM, not a runtime validator — existing packs that still carry `animal` aren't rejected (it's an ignored extra field). Verified across the import→package→description.json round-trip.
- **No consumer:** the `claw-interface` pack-ingestion path never reads `animal` (`schema/pack.py` doesn't declare it → ignored on parse). The native Zoo-catalog `animal` (used by the frontend fallback avatar) is sourced from `agent_id`, **not** from the pack's `description.json`.

## Verification
- Full agent-studio test suite green (117 skill-root + 12 package tests); no test referenced `animal`.
- `py_compile` clean on the generator.

Note: this is independent of the KB capability PR (#193) — separate concern, separate branch off `main`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
