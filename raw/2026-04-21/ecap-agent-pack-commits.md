# ecap-agent-pack Commits — 2026-04-21

共 1 条 commits

---

## [47f5fba8](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/47f5fba81927d466d60269731d750ece13ac9b8b)

**Author:** david-srp  
**Date:** 2026-04-20T07:45:22Z

**Message:**
```
feat(vibe-drama): upgrade to v1.0.9 workflow (#99)
```

**PR #99 Description:**

## Summary
This PR upgrades `zoodance-vibe-drama` to the latest `v1.0.9` workflow and brings in a substantial product-level step up for short-drama generation, especially around prompt control, asset flow clarity, cost transparency, and generation safety.

It also includes a compatibility preservation fix for this repo's current runtime layout: instead of hard-coding shared tools under `/extra-skills`, the docs/examples continue to support dynamic skill-path fallback (`$HOME/.openclaw/skills` first, `/extra-skills` second), so the upgraded pack remains usable in the current environment.

---

## Changes by category

### 1. Video generation workflow upgrade
- Added **mandatory art style + genre dual binding** for asset prompts and beat prompts, so visual style and narrative tone stay locked throughout the episode.
- Upgraded generation parameter guidance to support **480p / 720p / 1080p**, with explicit rules that:
  - `1080p` is **pro-only**
  - `1080p` costs **2.5x tokens vs 720p**
  - `fast` mode does **not** support `1080p`
- Added a **mandatory pre-flight review step** before concurrent beat generation.

User value:
- Much better consistency across beats, less visual drift.
- Higher-quality output options for premium use cases.
- Users see cost/quality tradeoffs before burning tokens.

### 2. Prompt preview and expensive-step confirmation
- Added a compact **beat-by-beat preview summary** before generation.
- Added a **reference-map table** so each beat's character / scene / prop input is visible before launch.
- Added an explicit confirmation fork: view full prompts / directly confirm generation / modify a specific beat first.

User value:
- Catches missing or wrong references before expensive generation starts.
- Makes the flow feel more controllable and less black-box.
- Reduces wasted runs caused by prompt misunderstandings.

### 3. Asset generation and copyright flow cleanup
- Added a **mandatory one-time copyright notice** before any reference image path is used.
- Split character-reference flow into two explicit paths: user uploads reference photos / AI generates character boards.
- If the user uploads reference photos, the flow can now go **directly into asset registration**, instead of forcing character-board generation first.

User value:
- Cleaner real-world onboarding when users already have reference photos.
- Better compliance posture around portraits and licensed materials.

### 4. Seedance safety and error-handling hardening
- Documented **reference input limits** for image / video / audio.
- Added explicit handling for `OutputAudioSensitiveContentDetected`: no silent fallback by default, user must choose whether to retry, generate silent + TTS later, or skip.

User value:
- Fewer invisible failures.
- Safer and more predictable runtime behavior.

### 5. Pack metadata refresh
- Bumped `agent-pack.yaml` version from `1.0.8` to `1.0.9`
- Updated author metadata

### 6. Repo compatibility preservation
- Kept dynamic shared-skill path resolution: prefer `$HOME/.openclaw/skills`, fallback to `/extra-skills`

---

## Why this is a big upgrade
Meaningfully upgrades the product from "can generate" to "can generate with stronger guardrails and better user control":
1. **consistency**: style + genre stay locked
2. **transparency**: preview and reference maps visible before launch
3. **cost control**: explicit user confirmation gates before expensive generation
4. **production safety**: copyright, asset registration, and audio-failure handling are much clearer
