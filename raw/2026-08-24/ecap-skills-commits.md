# SerendipityOneInc/ecap-skills — commits 2026-08-24

## fix(speech): hide backend implementation details (#271)

- **SHA**: `7f5553447d0adddb29a073ae4932c6682d60d230`
- **作者**: sharplee-srp
- **日期**: 2026-08-24T07:11:38Z
- **PR**: #271

### Commit Message

```
fix(speech): hide backend implementation details (#271)

## Summary

- remove explicit ASR/TTS backend model and inference-framework names
from published skill instructions, references, and script comments
- remove the internal speaker-provider name from meeting-notes guidance,
comments, docstrings, fixtures, and CLI help
- stop persisting or returning speaker-service `model` metadata to the
Agent
- add a skill-lint guard that prevents these replaceable implementation
details from being reintroduced

Operational model IDs required by non-published devcontainer routing
remain unchanged.

## Validation

- `python3 .github/scripts/lint_skills.py`
- `bash -n zooclaw-asr/scripts/transcribe.sh
zooclaw-tts/scripts/asr_transcribe.sh
zooclaw-tts/scripts/celebrity_clone.sh zooclaw-tts/scripts/synthesize.sh
zooclaw-tts/scripts/voice_mgmt.sh`
- `python3 -m unittest discover -s meeting-notes/tests -p 'test_*.py'
-v` (13 tests)
- `git diff --check origin/main...HEAD`
- A102 rootless-devcontainer E2E with the target staging image digest
and the real Gateway-backed Agent path: TTS, ASR, and one-speaker
identification completed; all four artifacts were produced; user-facing
text and structured results disclosed no backend model, serving engine,
or underlying provider
```

### PR Body

## Summary

- remove explicit ASR/TTS backend model and inference-framework names from published skill instructions, references, and script comments
- remove the internal speaker-provider name from meeting-notes guidance, comments, docstrings, fixtures, and CLI help
- stop persisting or returning speaker-service `model` metadata to the Agent
- add a skill-lint guard that prevents these replaceable implementation details from being reintroduced

Operational model IDs required by non-published devcontainer routing remain unchanged.

## Validation

- `python3 .github/scripts/lint_skills.py`
- `bash -n zooclaw-asr/scripts/transcribe.sh zooclaw-tts/scripts/asr_transcribe.sh zooclaw-tts/scripts/celebrity_clone.sh zooclaw-tts/scripts/synthesize.sh zooclaw-tts/scripts/voice_mgmt.sh`
- `python3 -m unittest discover -s meeting-notes/tests -p 'test_*.py' -v` (13 tests)
- `git diff --check origin/main...HEAD`
- A102 rootless-devcontainer E2E with the target staging image digest and the real Gateway-backed Agent path: TTS, ASR, and one-speaker identification completed; all four artifacts were produced; user-facing text and structured results disclosed no backend model, serving engine, or underlying provider


---

## revert: remove Creem generation moderation gate (#270)

- **SHA**: `1d022e8f25eaa863d6b3f5066d25864676f023c2`
- **作者**: tim-srp
- **日期**: 2026-08-24T02:39:05Z
- **PR**: #270

### Commit Message

```
revert: remove Creem generation moderation gate (#270)

## Summary

- revert `ecap-skills` PR #258
- remove Creem prompt moderation from image and video generation CLIs
- remove the dedicated moderation tests and retired design spec

## Scope

This is an exact revert of merge commit
`af3919905a7968533b6472023c69715f31315d3f`. No matching Creem moderation
code or publication PR exists in `ecap-agent-pack` current main.

## Validation

- `python -m py_compile designer/scripts/image_generation_cli.py
video-generator/scripts/video_generation_cli.py`
- `python .github/scripts/lint_skills.py` (passed with 12 pre-existing
warnings)
- `git diff HEAD^ --check`

## Follow-up

The now-unused `/creem/moderation` proxy implementation in
`ecap-proxy-service` can be retired separately after this caller
rollback lands.
```

### PR Body

## Summary

- revert `ecap-skills` PR #258
- remove Creem prompt moderation from image and video generation CLIs
- remove the dedicated moderation tests and retired design spec

## Scope

This is an exact revert of merge commit `af3919905a7968533b6472023c69715f31315d3f`. No matching Creem moderation code or publication PR exists in `ecap-agent-pack` current main.

## Validation

- `python -m py_compile designer/scripts/image_generation_cli.py video-generator/scripts/video_generation_cli.py`
- `python .github/scripts/lint_skills.py` (passed with 12 pre-existing warnings)
- `git diff HEAD^ --check`

## Follow-up

The now-unused `/creem/moderation` proxy implementation in `ecap-proxy-service` can be retired separately after this caller rollback lands.


---
