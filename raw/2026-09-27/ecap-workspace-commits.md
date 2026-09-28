# SerendipityOneInc/ecap-workspace — commits 2026-09-27

## fix(tasks): generate persistent titles from the first turn (#3906)

- **SHA**: `d35f4fd293d9a31a04e02915497fc0fb82224862`
- **作者**: Nemo Feng
- **日期**: 2026-09-27T04:16:41Z
- **PR**: #3906

### Commit Message

```
fix(tasks): generate persistent titles from the first turn (#3906)

Engine tasks created their chat transport without ever invoking title
generation, so the sidebar and Tasks page fell back to the first 80
characters of raw message Markdown. This adds a nonblocking, first-turn
title request for writable task conversations and persists the result in
their existing record. Reads use attachment-aware fallback text;
successful generated titles stay stable, and manual names always take
precedence. Nonempty first turns that clean down to nothing (including
URL-only messages) use `Shared content`, keeping those tasks visible
after switching conversations without exposing URL destinations; truly
empty messages remain untitled.

The title action resolves the canonical session and original stored
thread through the existing ownership boundary. Atomic fallback/attempt
checks prevent duplicate generation and protect concurrent
renames/archives. Failed generation keeps the readable fallback, with a
five-minute retry cooldown on later visits. Naming does not change
activity timestamps. The browser refreshes the sidebar, task detail and
`/tasks`, and patches the current conversation title without rebinding
its transport.

Validation:
- URL-only title/history regression: reproduced the disappearance before
the fix; all 79 focused task-title/history tests pass. Coverage includes
both history-list paths, saved URL fallback titles, generation
success/failure, unlabeled links/attachments, and empty messages. Ruff,
formatting, Pyright, and import contracts passed.
- Backend regression checks passed for first-turn extraction,
attachment/link normalization, canonical-to-original mapping, concurrent
generation, rename/archive races, failure/cooldown, ownership,
external/Build exclusion and route scope. Existing session-channel
service/repository/schema tests also passed (65 tests).
- Frontend title lifecycle, cache refresh, navigation isolation and
legacy workspace tests passed; TypeScript, ESLint, Ruff, Pyright and
import contracts passed.
- Playwright with the local mock: sent a first task message and verified
the same generated title in the sidebar, chat header and `/tasks`. Mock
inference is deterministic; real generation is exercised via service
tests with a stubbed existing title provider.

Requires backend and frontend deployment (backend first). Existing tasks
receive generated titles when opened; this does not bulk-backfill
historical tasks. Credit usage is unchanged. Staging's encrypted Mongo
client was unavailable here: the new classic single-collection CAS
passes the query guard, but actual encrypted-client validation remains a
release gate.

A fallback response gets at most two five-second follow-ups, so a
concurrent tab can observe the winning generation. Navigation cancels
those checks, and generated/manual titles stop them. Regression tests
cover successful completion, exhausted follow-ups and cancellation; no
unbounded polling or repeat inference is introduced.
```

### PR Body

Engine tasks created their chat transport without ever invoking title generation, so the sidebar and Tasks page fell back to the first 80 characters of raw message Markdown. This adds a nonblocking, first-turn title request for writable task conversations and persists the result in their existing record. Reads use attachment-aware fallback text; successful generated titles stay stable, and manual names always take precedence. Nonempty first turns that clean down to nothing (including URL-only messages) use `Shared content`, keeping those tasks visible after switching conversations without exposing URL destinations; truly empty messages remain untitled.

The title action resolves the canonical session and original stored thread through the existing ownership boundary. Atomic fallback/attempt checks prevent duplicate generation and protect concurrent renames/archives. Failed generation keeps the readable fallback, with a five-minute retry cooldown on later visits. Naming does not change activity timestamps. The browser refreshes the sidebar, task detail and `/tasks`, and patches the current conversation title without rebinding its transport.

Validation:
- URL-only title/history regression: reproduced the disappearance before the fix; all 79 focused task-title/history tests pass. Coverage includes both history-list paths, saved URL fallback titles, generation success/failure, unlabeled links/attachments, and empty messages. Ruff, formatting, Pyright, and import contracts passed.
- Backend regression checks passed for first-turn extraction, attachment/link normalization, canonical-to-original mapping, concurrent generation, rename/archive races, failure/cooldown, ownership, external/Build exclusion and route scope. Existing session-channel service/repository/schema tests also passed (65 tests).
- Frontend title lifecycle, cache refresh, navigation isolation and legacy workspace tests passed; TypeScript, ESLint, Ruff, Pyright and import contracts passed.
- Playwright with the local mock: sent a first task message and verified the same generated title in the sidebar, chat header and `/tasks`. Mock inference is deterministic; real generation is exercised via service tests with a stubbed existing title provider.

Requires backend and frontend deployment (backend first). Existing tasks receive generated titles when opened; this does not bulk-backfill historical tasks. Credit usage is unchanged. Staging's encrypted Mongo client was unavailable here: the new classic single-collection CAS passes the query guard, but actual encrypted-client validation remains a release gate.

A fallback response gets at most two five-second follow-ups, so a concurrent tab can observe the winning generation. Navigation cancels those checks, and generated/manual titles stop them. Regression tests cover successful completion, exhausted follow-ups and cancellation; no unbounded polling or repeat inference is introduced.



---

## fix(agents): preserve chat while switching models (#3905)

- **SHA**: `52d3aa94b583e6a8ce42d188edb7427ae827efe0`
- **作者**: Nemo Feng
- **日期**: 2026-09-27T02:54:47Z
- **PR**: #3905

### Commit Message

```
fix(agents): preserve chat while switching models (#3905)

Changing an Agent model invalidated the entire definition subtree and
briefly removed the working revision, unmounting the chat and composer.
Settings saves now seed the returned revision and refresh only settings
metadata. Same-workspace revision transitions retain the previous
snapshot with settings controls disabled, including when polling sees
the new revision before the save response.

Validation:
- Targeted Vitest run: 112 tests passed, including delayed revision,
save success/failure, cache invalidation, and account/workspace
isolation.
- TypeScript, ESLint, governance guards and pre-push checks passed.
- Playwright against the local mock: delayed the save response by five
seconds, switched from Claude Sonnet 4.6 to GPT 5.4, and verified the
same composer DOM node and unsent draft survived, the URL did not
change, and no conversation-binding request ran.

Frontend-only deployment. Task titles and credits are separate work.

Review follow-up: added a real QueryClient test for a terminal
revision-read failure. The installed TanStack Query clears placeholder
data on error (`isPlaceholderData: false`) and recovers on refetch, so
the reported indefinite-placeholder failure did not reproduce. Added a
guard/test for late save responses after workspace navigation. Updated
avatar and legacy-workspace regression fixtures to follow the actual
authenticated, immutable-revision contract; the final focused run passed
19 tests.
```

### PR Body

Changing an Agent model invalidated the entire definition subtree and briefly removed the working revision, unmounting the chat and composer. Settings saves now seed the returned revision and refresh only settings metadata. Same-workspace revision transitions retain the previous snapshot with settings controls disabled, including when polling sees the new revision before the save response.

Validation:
- Targeted Vitest run: 112 tests passed, including delayed revision, save success/failure, cache invalidation, and account/workspace isolation.
- TypeScript, ESLint, governance guards and pre-push checks passed.
- Playwright against the local mock: delayed the save response by five seconds, switched from Claude Sonnet 4.6 to GPT 5.4, and verified the same composer DOM node and unsent draft survived, the URL did not change, and no conversation-binding request ran.

Frontend-only deployment. Task titles and credits are separate work.

Review follow-up: added a real QueryClient test for a terminal revision-read failure. The installed TanStack Query clears placeholder data on error (`isPlaceholderData: false`) and recovers on refetch, so the reported indefinite-placeholder failure did not reproduce. Added a guard/test for late save responses after workspace navigation. Updated avatar and legacy-workspace regression fixtures to follow the actual authenticated, immutable-revision contract; the final focused run passed 19 tests.


---
