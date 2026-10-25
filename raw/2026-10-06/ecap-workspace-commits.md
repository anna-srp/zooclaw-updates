# SerendipityOneInc/ecap-workspace — commits 2026-10-06

## test(e2e): migrate regression specs to Agent task workflows (#4026)

- **SHA**: `38b2866638e6b6ba10cfbedcad989f45e0549dd9`
- **作者**: rayhuang198212
- **日期**: 2026-10-06T02:27:09Z
- **PR**: #4026

### Commit Message

```
test(e2e): migrate regression specs to Agent task workflows (#4026)

## Summary

Update E2E regression coverage to match the current Agent workspace and
Task workflows. Replace legacy launcher/shared-session usage and
strengthen assertions so tests verify user-visible behavior and
generated content.

- Migrate chat, tool, session, upload, recovery, and file-preview specs
to isolated Agent tasks.
- Redesign Agents management coverage around listing, grid/list views,
renaming, persistence, and source filters.
- Verify model changes in the Agent editor, persistence after reload,
and read-only model browsing in Task mode.
- Cover draft preservation and retry after reconnecting, concurrent
session isolation, and recovery from API and streaming failures.
- Submit the video and prompt together and allow six minutes for frame
extraction.
- Strengthen artifact preview, source switching, download, and reopening
checks.
- Distinguish invalid LLM judge responses from valid negative verdicts
and unavailable judge configuration.
- Remove unused legacy shared-session fixtures and launcher Page Object.

## Validation

- Staging file-preview run: 7 passed, including authentication setup.
- `pnpm install --frozen-lockfile`
- `pnpm exec tsc --noEmit --project app/tsconfig.json`
- `pnpm --filter @zooclaw/web-app run lint`
- `pnpm --filter @zooclaw/web-app run lint:ci`

All four local quality gates passed. The full E2E suite was not run
together.

## Scope

Test infrastructure and specs only; no product behavior changes.

File-generation tests depend on live staging services and LLM output.
PDF coverage checks the preview entry point and downloaded file format,
but does not verify page count or document text.
```

### PR Body

## Summary

Update E2E regression coverage to match the current Agent workspace and Task workflows. Replace legacy launcher/shared-session usage and strengthen assertions so tests verify user-visible behavior and generated content.

- Migrate chat, tool, session, upload, recovery, and file-preview specs to isolated Agent tasks.
- Redesign Agents management coverage around listing, grid/list views, renaming, persistence, and source filters.
- Verify model changes in the Agent editor, persistence after reload, and read-only model browsing in Task mode.
- Cover draft preservation and retry after reconnecting, concurrent session isolation, and recovery from API and streaming failures.
- Submit the video and prompt together and allow six minutes for frame extraction.
- Strengthen artifact preview, source switching, download, and reopening checks.
- Distinguish invalid LLM judge responses from valid negative verdicts and unavailable judge configuration.
- Remove unused legacy shared-session fixtures and launcher Page Object.

## Validation

- Staging file-preview run: 7 passed, including authentication setup.
- `pnpm install --frozen-lockfile`
- `pnpm exec tsc --noEmit --project app/tsconfig.json`
- `pnpm --filter @zooclaw/web-app run lint`
- `pnpm --filter @zooclaw/web-app run lint:ci`

All four local quality gates passed. The full E2E suite was not run together.

## Scope

Test infrastructure and specs only; no product behavior changes.

File-generation tests depend on live staging services and LLM output. PDF coverage checks the preview entry point and downloaded file format, but does not verify page count or document text.

---
