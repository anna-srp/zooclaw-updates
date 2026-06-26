# SerendipityOneInc/ecap-skills — commits 2026-06-25


共 1 个 commit


---

## feat(chameleon-seedance): add Seedance 2.0 mini model (#217)

- **SHA**: 736d44404d8f9e7126e4c65f6f284cdc9eac3da6
- **作者**: david-srp (@david-srp)
- **日期**: 2026-06-25T11:36:50Z
- **PR**: #217
- **URL**: https://github.com/SerendipityOneInc/ecap-skills/commit/736d44404d8f9e7126e4c65f6f284cdc9eac3da6

### 完整 Commit Message

```
feat(chameleon-seedance): add Seedance 2.0 mini model (#217)

Wire dreamina-seedance-2-0-mini-260615 as a first-class model alongside
pro/fast. mini is the high cost-performance tier (~50% cheaper) aimed at
high-volume e-commerce / marketing / UGC / effects generation; like fast it
tops out at 720p (no 1080p / 4K).

- Extend the 1080p guard to reject fast AND mini (was fast-only), mirroring
  the existing 4K guard, so 1080p/4K stay Pro-only and invalid requests fail
  client-side before an upstream call or R2 upload.
- Correct the placeholder mini id in tests (...-260128 -> the real ...-260615).
- Surface the three model ids in --model help; clarify --resolution help.
- Document mini in chameleon-kb-summary (model list, ~50% pricing, resolution
  policy, priority) and the BytePlus API reference.
- Add regression tests: 1080p rejected on fast/mini, 1080p payload on pro.

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>
```

### 完整 PR Body

## What

Adds **Seedance 2.0 mini** (`dreamina-seedance-2-0-mini-260615`) as a first-class model in the chameleon-seedance skill, alongside pro and fast.

mini is the high cost-performance tier (~50% cheaper than 2.0) for high-volume scenarios — e-commerce content, batch marketing assets, UGC, and effects. Same request shape / multimodal inputs as pro/fast; like fast it tops out at **720p** (no 1080p, no 4K).

## Why

The skill was in a half-wired state: the script already had a `MINI_MODEL_MARKER` and a 4K-rejects-mini guard, and a test referenced a **placeholder** mini id — but mini wasn't a documented/selectable model and the 1080p guard didn't cover it (so mini would wrongly be allowed to request 1080p).

## Changes

- **Guard**: extend the 1080p rejection to cover `fast` **and** `mini` (was fast-only), mirroring the existing 4K guard — keeps 1080p/4K Pro-only and rejects invalid requests client-side before an upstream call or R2 upload.
- **Model id fix**: the test used a placeholder `dreamina-seedance-2-0-mini-260128` (date suffix copied from pro/fast); corrected to the real `dreamina-seedance-2-0-mini-260615`.
- **CLI help**: `--model` now lists the three model ids; `--resolution` help clarifies "1080p/4k are Pro-only, fast/mini max 720p".
- **Docs**: mini added to `chameleon-kb-summary.md` (model list, ~50% pricing, resolution policy, priority series) and the BytePlus API reference.
- **Tests**: new regression tests — 1080p rejected on fast/mini, 1080p payload allowed on pro.

## Test plan

```
uv run --with httpx --with pytest pytest chameleon-seedance/tests/ -q
# 11 passed
```

Smoke-tested: mini@720p builds a valid payload; mini@1080p and mini@4k are rejected with clear messages; `--help` renders cleanly.

## Reviewer notes

- **Resolution policy**: mini = 480p/720p only, matching BytePlus's "1080p/4K are Pro-only" rule (verified against the authoritative ModelArk doc).
- **priority / bitrate on mini**: treated as inherited (no new model-specific guard), since the request shape is identical and the API reference lists priority as a "Seedance 2.0 series" feature.
- **Out of scope / follow-up**: a separate audit is in progress to sync the reference docs to the latest BytePlus ModelArk doc (e.g. reference-video size 50 MB → 200 MB, total-pixel cap 2,086,876 → 8,295,044, new prompt-language support). Those will land in a separate PR.


