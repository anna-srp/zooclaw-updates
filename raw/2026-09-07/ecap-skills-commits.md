# SerendipityOneInc/ecap-skills — commits 2026-09-07

## feat(feishu): enable Bitable record-write guidance (#277)

- **SHA**: `8a5aac4e1955a07435e200537d91c943f8891140`
- **作者**: sharplee-srp
- **日期**: 2026-09-07T02:51:27Z
- **PR**: #277

### Commit Message

```
feat(feishu): enable Bitable record-write guidance (#277)

## Summary

- update the `feishu-bitable` skill to version 1.1 for native record
writes
- document `create_record` and `update_record` as the current write
surface
- keep app and field creation explicitly marked as a later phase
- add field-shape, pagination, write verification, and unknown-outcome
safety guidance

## Context

This is the skill-layer companion to
`SerendipityOneInc/zooclaw-engine#1245`. The ACS executor dependency is
already merged in `SerendipityOneInc/agent-channel-service#107`.

## Validation

- `python3 .github/scripts/lint_skills.py` — passed with 12 unrelated
existing warnings
- `git diff --check origin/main...HEAD`

## Rollout

Publish to staging after the Engine change is deployed, refresh the test
Agent configuration, and run a one-record create/read/update/read E2E
before production promotion.
```

### PR Body

## Summary

- update the `feishu-bitable` skill to version 1.1 for native record writes
- document `create_record` and `update_record` as the current write surface
- keep app and field creation explicitly marked as a later phase
- add field-shape, pagination, write verification, and unknown-outcome safety guidance

## Context

This is the skill-layer companion to `SerendipityOneInc/zooclaw-engine#1245`. The ACS executor dependency is already merged in `SerendipityOneInc/agent-channel-service#107`.

## Validation

- `python3 .github/scripts/lint_skills.py` — passed with 12 unrelated existing warnings
- `git diff --check origin/main...HEAD`

## Rollout

Publish to staging after the Engine change is deployed, refresh the test Agent configuration, and run a one-record create/read/update/read E2E before production promotion.


---
