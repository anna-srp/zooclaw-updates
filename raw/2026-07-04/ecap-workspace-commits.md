# ecap-workspace — 2026-07-04 commits

## refactor(pack-store): remove legacy official submission api (#2732)

- **SHA**: 7d45923b561ed134811883179b3fbd6ba162be4d
- **作者**: bill-srp
- **日期**: 2026-07-04T07:10:05Z
- **PR**: #2732

### Commit Message

```
refactor(pack-store): remove legacy official submission api (#2732)

## Summary

- remove the legacy `/internal/agent-packs/official-submissions*`
backend API
- delete the old official submission service and schema
- update route tests to assert the backend cleanup state

## Stacking

Stacked on PR #2727 (`fix/official-pack`). This cleanup should merge
only after the dashboard-console submit-from-private flow has shipped.

## Verification

- `/Users/bill/.venvs/claw-interface/bin/ruff check
app/routes/internal/agent_packs.py
tests/unit/test_internal_agent_packs_routes.py`
- `/Users/bill/.venvs/claw-interface/bin/pytest
tests/unit/test_internal_agent_packs_routes.py`
```

### PR Body

## Summary

- remove the legacy `/internal/agent-packs/official-submissions*` backend API
- delete the old official submission service and schema
- update route tests to assert the backend cleanup state

## Stacking

Stacked on PR #2727 (`fix/official-pack`). This cleanup should merge only after the dashboard-console submit-from-private flow has shipped.

## Verification

- `/Users/bill/.venvs/claw-interface/bin/ruff check app/routes/internal/agent_packs.py tests/unit/test_internal_agent_packs_routes.py`
- `/Users/bill/.venvs/claw-interface/bin/pytest tests/unit/test_internal_agent_packs_routes.py`


## refactor(dashboard-console): submit official packs from private packs (#2727)

- **SHA**: 6616485341264da2d4315a77b761d1aeacb58cb4
- **作者**: bill-srp
- **日期**: 2026-07-04T06:56:07Z
- **PR**: #2727

### Commit Message

```
refactor(dashboard-console): submit official packs from private packs (#2727)

## Summary

- replace the standalone official-submissions dashboard flow with a
submit-from-private-pack dialog on the agent-packs page
- copy private pack archives through the dashboard-console Worker R2
binding before submitting the official pack version
- remove the legacy backend official-submissions routes/schema/service
and move private-pack submission lookup into submission_service
- size override is intentional: the diff is inflated by deleting the
obsolete official-submissions page/service/tests and renaming the dialog
into a non-route component

## Testing

- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH python -m pytest
services/claw-interface/tests/unit/test_internal_agent_packs_routes.py
services/claw-interface/tests/unit/test_submission_service.py -q`
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`
- `git diff --check`
- `bash scripts/verify-changed.sh`
- Frontend checks attempted but blocked before test/compile execution by
local pnpm dependency validation: `ERR_PNPM_MISSING_TARBALL_INTEGRITY`
for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`.
```

### PR Body

## Summary

- replace the standalone official-submissions dashboard flow with a submit-from-private-pack dialog on the agent-packs page
- copy private pack archives through the dashboard-console Worker R2 binding before submitting the official pack version
- remove the legacy backend official-submissions routes/schema/service and move private-pack submission lookup into submission_service
- size override is intentional: the diff is inflated by deleting the obsolete official-submissions page/service/tests and renaming the dialog into a non-route component

## Testing

- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH python -m pytest services/claw-interface/tests/unit/test_internal_agent_packs_routes.py services/claw-interface/tests/unit/test_submission_service.py -q`
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`
- `git diff --check`
- `bash scripts/verify-changed.sh`
- Frontend checks attempted but blocked before test/compile execution by local pnpm dependency validation: `ERR_PNPM_MISSING_TARBALL_INTEGRITY` for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`.

