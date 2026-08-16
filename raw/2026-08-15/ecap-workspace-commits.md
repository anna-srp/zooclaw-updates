# SerendipityOneInc/ecap-workspace — commits 2026-08-15

## feat(agents): publish delegation metadata (#3403)

- **SHA**: `a153ebb00be62823f3874cf07c05622eda85d825`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-15T13:51:46Z
- **PR**: #3403

### Commit Message

```
feat(agents): publish delegation metadata (#3403)

## Summary

- publish Agent directory `description` and `delegation.enabled` on
Engine Agent create/update
- prefer pack `short_bio`, falling back to `bio`, while keeping hidden,
pack-test, and Agent Builder runtimes non-delegatable
- add a dry-run-by-default, paginated, resumable metadata backfill for
retained Engine Agent workspaces
- parse directory metadata from Engine Agent reads for idempotent repair

## Rollout

Deploy the Engine contract first with owner-scoped delegation disabled,
then deploy this change, run the backfill in dry-run and write modes,
and finally enable owner-scoped delegation in Engine.

Engine counterpart:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/774

## Testing

- `bash scripts/verify-py.sh`
- 239 targeted unit tests covering the Engine client,
install/update/main/test runtimes, repository pagination, and backfill
behavior
```

### PR Body

## Summary

- publish Agent directory `description` and `delegation.enabled` on Engine Agent create/update
- prefer pack `short_bio`, falling back to `bio`, while keeping hidden, pack-test, and Agent Builder runtimes non-delegatable
- add a dry-run-by-default, paginated, resumable metadata backfill for retained Engine Agent workspaces
- parse directory metadata from Engine Agent reads for idempotent repair

## Rollout

Deploy the Engine contract first with owner-scoped delegation disabled, then deploy this change, run the backfill in dry-run and write modes, and finally enable owner-scoped delegation in Engine.

Engine counterpart: https://github.com/SerendipityOneInc/zooclaw-engine/pull/774

## Testing

- `bash scripts/verify-py.sh`
- 239 targeted unit tests covering the Engine client, install/update/main/test runtimes, repository pagination, and backfill behavior


---
