# SerendipityOneInc/ecap-skills — commits 2026-08-15

## docs: clarify V1/V2 skills publishing contract (#267)

- **SHA**: `9f5c63d7d45474c0ef7422d4bbfd9db90a9513af`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-15T16:48:40Z
- **PR**: #267

### Commit Message

```
docs: clarify V1/V2 skills publishing contract (#267)

## Summary

- distinguish the V1 S3/JuiceFS allowlist from the curated V2 registry
allowlist
- document the rendered-config, runtime materialization, eligibility,
and model-visibility boundaries
- align the environment matrix with the workflow: staging always syncs
V2, production is gated, and dev remains S3-only
- keep Skill lifecycle and propagation to existing immutable Agent
configs owned by zooclaw-engine#739

## Validation

- `PUBLISH_BASE_URL=http://example.invalid PUBLISH_TOKEN=validation-only
node .github/scripts/sync-v2-registry.mjs --validate`
- `python3 .github/scripts/lint_skills.py` (passes with 12 pre-existing
warnings)
- `git diff --check`

Closes SerendipityOneInc/zooclaw-engine#719
```

### PR Body

## Summary

- distinguish the V1 S3/JuiceFS allowlist from the curated V2 registry allowlist
- document the rendered-config, runtime materialization, eligibility, and model-visibility boundaries
- align the environment matrix with the workflow: staging always syncs V2, production is gated, and dev remains S3-only
- keep Skill lifecycle and propagation to existing immutable Agent configs owned by zooclaw-engine#739

## Validation

- `PUBLISH_BASE_URL=http://example.invalid PUBLISH_TOKEN=validation-only node .github/scripts/sync-v2-registry.mjs --validate`
- `python3 .github/scripts/lint_skills.py` (passes with 12 pre-existing warnings)
- `git diff --check`

Closes SerendipityOneInc/zooclaw-engine#719


---
