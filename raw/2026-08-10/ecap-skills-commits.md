# SerendipityOneInc/ecap-skills — commits 2026-08-10

## feat(chameleon-seedance): add Seedance 2.5 model support (#262)

- **SHA**: `8842efdcba7326b39213d9609d18002e6ac89e5a`
- **作者**: david-srp
- **日期**: 2026-08-10T11:08:58Z
- **PR**: #262

### Commit Message

```
feat(chameleon-seedance): add Seedance 2.5 model support (#262)

## What

Adds `dreamina-seedance-2-5-260628` (Seedance 2.5) support to the
chameleon-seedance skill, alongside the existing 2.0 / fast / mini
models.

### Script (`chameleon_generate.py`)
- Family-aware client-side validation (2.0 series vs 2.5):
- 2.5: `--duration` up to **30s**, reference assets up to **30 images +
10 videos + 10 audios**, **pure audio reference** allowed (new payload
branch — previously audio-only input was silently dropped)
- 2.5 rejections with clear errors: `1080p/4k` (2.5 outputs 480p/720p
only), `--bitrate-mode`, `--priority`
- 2.0 series keeps existing limits (15s, 9/3/3); passing 30s on 2.0
errors with a hint to switch to 2.5
- New `--output-format mp4|mov` flag (2.5 only; mov = H.264 + yuv444p +
PCM for post-production)
- `generation_log.csv` gains an `output_format` column (append-only
header migration covered by tests)

### References
- New `references/byteplus-dreamina-seedance-2.5-api.md`: task-type
constraints (`ratio=adaptive` / `duration=-1` for
edit/extend/first-frame, `InvalidParameter.TaskTypeConstraint`), asset
limits, rate limits
- `chameleon-kb-summary.md`: 4-model matrix, per-family limits, official
BytePlus USD pricing tables (2026-08)
- `SKILL.md`: 2.5 routing + description refresh

## Testing

- `pytest`: 24 passed (13 new 2.5 cases); repo linter passes
- **Live E2E through ecap-proxy** (real generations):
  - 2.5 text-to-video mp4 → `cgt-20260810181347-b9645` succeeded
- 2.5 `--output-format mov` → `cgt-20260810181347-b9kcg` succeeded,
downloaded file verified **h264 + yuv444p + pcm_s16le** (new field
passes through the proxy untouched)
  - mini text-to-video → `cgt-20260810181350-mhmnr` succeeded
- 4-model same-prompt comparison (mini/fast/pro/2.5 @480p) all succeeded

## Note (non-blocking)

ecap-proxy-service bills all Seedance calls at flat 2.0-pro rates
(`app/routes/video.py:43-44`); until its per-model rate map lands, 2.5
calls under-bill ~33-35% and mini over-bills ~2x. Billing fix is tracked
separately on the proxy side — this PR is functionality-complete and
safe to ship independently.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## What

Adds `dreamina-seedance-2-5-260628` (Seedance 2.5) support to the chameleon-seedance skill, alongside the existing 2.0 / fast / mini models.

### Script (`chameleon_generate.py`)
- Family-aware client-side validation (2.0 series vs 2.5):
  - 2.5: `--duration` up to **30s**, reference assets up to **30 images + 10 videos + 10 audios**, **pure audio reference** allowed (new payload branch — previously audio-only input was silently dropped)
  - 2.5 rejections with clear errors: `1080p/4k` (2.5 outputs 480p/720p only), `--bitrate-mode`, `--priority`
  - 2.0 series keeps existing limits (15s, 9/3/3); passing 30s on 2.0 errors with a hint to switch to 2.5
- New `--output-format mp4|mov` flag (2.5 only; mov = H.264 + yuv444p + PCM for post-production)
- `generation_log.csv` gains an `output_format` column (append-only header migration covered by tests)

### References
- New `references/byteplus-dreamina-seedance-2.5-api.md`: task-type constraints (`ratio=adaptive` / `duration=-1` for edit/extend/first-frame, `InvalidParameter.TaskTypeConstraint`), asset limits, rate limits
- `chameleon-kb-summary.md`: 4-model matrix, per-family limits, official BytePlus USD pricing tables (2026-08)
- `SKILL.md`: 2.5 routing + description refresh

## Testing

- `pytest`: 24 passed (13 new 2.5 cases); repo linter passes
- **Live E2E through ecap-proxy** (real generations):
  - 2.5 text-to-video mp4 → `cgt-20260810181347-b9645` succeeded
  - 2.5 `--output-format mov` → `cgt-20260810181347-b9kcg` succeeded, downloaded file verified **h264 + yuv444p + pcm_s16le** (new field passes through the proxy untouched)
  - mini text-to-video → `cgt-20260810181350-mhmnr` succeeded
  - 4-model same-prompt comparison (mini/fast/pro/2.5 @480p) all succeeded

## Note (non-blocking)

ecap-proxy-service bills all Seedance calls at flat 2.0-pro rates (`app/routes/video.py:43-44`); until its per-model rate map lands, 2.5 calls under-bill ~33-35% and mini over-bills ~2x. Billing fix is tracked separately on the proxy side — this PR is functionality-complete and safe to ship independently.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
