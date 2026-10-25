# SerendipityOneInc/ecap-workspace — commits 2026-10-05

## fix(platform): refine credit reminders and enable staging bonus (#4023)

- **SHA**: `bf8d0b79112d8b6c385c55004dc928ef7e653a52`
- **作者**: ericma-srp
- **日期**: 2026-10-05T02:39:06Z
- **PR**: #4023

### Commit Message

```
fix(platform): refine credit reminders and enable staging bonus (#4023)

The sidebar could prompt a second purchase while a confirmed payment was
still posting credits. Hide the ordinary zero-balance reminder during
principal delivery or a pending bonus, keep the normal Add funds link
available, and use the same default black/white Button for the
first-purchase card as Go to Billing. The two sidebar cards remain
mutually exclusive; no new customer-facing state or copy.

The existing billing response adds hasPendingTopup from an
Organization/environment-scoped existence read with a matching compound
index, covering all history pages. Read delivery state before balance.
The shell refreshes normal delivery every 3 seconds for at most 3
minutes, then backs off to every 5 minutes; failed reads also back off.
Unchanged responses and page remounts do not renew the window.
Completion stops principal polling, and an explicit new purchase gets a
fresh window. Payment, eligibility and credit mutations are unchanged.

The product owner explicitly requested staging activation after the
deployed eric account returned firstTopupBonus: null. Enable
PLATFORM_FIRST_TOPUP_BONUS_ENABLED only in the staging deployment
overlay; base defaults and production/dev overlays remain unchanged.
Platform sandbox Checkout already rejects live Stripe keys. This is a
follow-up to merged #4018.

Validation: 244 Platform tests, including normal completion,
unchanged/error backoff across remounts, delayed completion, and a fresh
purchase during an older pending delivery; Platform lint/build. Earlier
checks for the unchanged backend/UI: 74 targeted
backend/query/deployment tests, Python static/import checks and commit
hooks, and desktop browser verification of matching black/white buttons,
mutually exclusive cards, and hidden zero-balance reminder while credits
settle.

Deployment verification remains distinct from local checks. This host
has no authenticated Kubernetes context; actual CSFLE execution,
historical payment facts, and Stripe Sandbox → Lago credit delivery are
not claimed as tested. After normal review/merge and staging deployment,
verify the live billing response and eligible card. Production
activation is outside this PR.
```

### PR Body

The sidebar could prompt a second purchase while a confirmed payment was still posting credits. Hide the ordinary zero-balance reminder during principal delivery or a pending bonus, keep the normal Add funds link available, and use the same default black/white Button for the first-purchase card as Go to Billing. The two sidebar cards remain mutually exclusive; no new customer-facing state or copy.

The existing billing response adds hasPendingTopup from an Organization/environment-scoped existence read with a matching compound index, covering all history pages. Read delivery state before balance. The shell refreshes normal delivery every 3 seconds for at most 3 minutes, then backs off to every 5 minutes; failed reads also back off. Unchanged responses and page remounts do not renew the window. Completion stops principal polling, and an explicit new purchase gets a fresh window. Payment, eligibility and credit mutations are unchanged.

The product owner explicitly requested staging activation after the deployed eric account returned firstTopupBonus: null. Enable PLATFORM_FIRST_TOPUP_BONUS_ENABLED only in the staging deployment overlay; base defaults and production/dev overlays remain unchanged. Platform sandbox Checkout already rejects live Stripe keys. This is a follow-up to merged #4018.

Validation: 244 Platform tests, including normal completion, unchanged/error backoff across remounts, delayed completion, and a fresh purchase during an older pending delivery; Platform lint/build. Earlier checks for the unchanged backend/UI: 74 targeted backend/query/deployment tests, Python static/import checks and commit hooks, and desktop browser verification of matching black/white buttons, mutually exclusive cards, and hidden zero-balance reminder while credits settle.

Deployment verification remains distinct from local checks. This host has no authenticated Kubernetes context; actual CSFLE execution, historical payment facts, and Stripe Sandbox → Lago credit delivery are not claimed as tested. After normal review/merge and staging deployment, verify the live billing response and eligible card. Production activation is outside this PR.


---

## test(e2e): migrate tests to Agent task workflows (#4022)

- **SHA**: `3261135c93674f164324a5a32210c65b1f50a399`
- **作者**: rayhuang198212
- **日期**: 2026-10-05T02:28:12Z
- **PR**: #4022

### Commit Message

```
test(e2e): migrate tests to Agent task workflows (#4022)

## Summary

Update the E2E suite to follow the current product workflow:

1. Create an Agent
2. Wait for the Agent build to complete
3. Start conversations through `New Task`
4. Validate Agent behavior
5. Delete the Agent after testing

This replaces legacy assumptions around pre-existing Assistants, `/chat`
sessions, and Agent hire/fire behavior.

## What changed

### Agent lifecycle coverage

- Replaced `agent-hire-fire.spec.ts` with `agent-create-delete.spec.ts`.
- Added coverage for the current Agent creation entry points:
  - `/agents?create=1`
  - `/home`
  - The `Create Agent` action on `/agents`
  - Template and shared-Agent entry points
- Added coverage for:
  - Creating an Agent from a description
  - Waiting for the build to complete
  - Verifying the generated Agent appears in the Agents list
  - Deleting the Agent with `DELETE` confirmation
- Renamed the Playwright project and CI workflow entry from
`agent-hire-fire` to `agent-create-delete`.

### Reusable Agent test infrastructure

Added reusable Page Objects and fixtures for the current product flow:

- `AgentsPage`
- `HomePage`
- `AgentWorkspacePage`
- `AgentTaskPage`
- `agent-task-session` fixture
- Agent lifecycle cleanup utilities

The shared fixture ensures the test account starts without existing
Agents, creates a dedicated Agent for the scenarios, and cleans up
Agents after the tests finish.

### Agent behavior scenarios

Migrated the following specs from the legacy shared `/chat` session to
Agent Task sessions:

- Chat smoke
- Basic usage
- Web search and URL fetch
- Browser tool

Each behavior scenario starts a fresh conversation through `New Task`,
preventing conversation history from leaking between scenarios.

The basic usage attachment scenarios now submit the prompt and
attachment together in the same conversation turn.

## Validation

The following staging suites passed:

- `basic-usage`: 7 passed
- `chat-smoke`: 2 passed
- `tool-web`: 3 passed
- `tool-browser`: 2 passed

Quality gates also passed:

- `pnpm install --frozen-lockfile`
- `pnpm exec tsc --noEmit --project app/tsconfig.json`
- `pnpm --filter @zooclaw/web-app run lint`
- `pnpm --filter @zooclaw/web-app run lint:ci`
```

### PR Body

## Summary

Update the E2E suite to follow the current product workflow:

1. Create an Agent
2. Wait for the Agent build to complete
3. Start conversations through `New Task`
4. Validate Agent behavior
5. Delete the Agent after testing

This replaces legacy assumptions around pre-existing Assistants, `/chat` sessions, and Agent hire/fire behavior.

## What changed

### Agent lifecycle coverage

- Replaced `agent-hire-fire.spec.ts` with `agent-create-delete.spec.ts`.
- Added coverage for the current Agent creation entry points:
  - `/agents?create=1`
  - `/home`
  - The `Create Agent` action on `/agents`
  - Template and shared-Agent entry points
- Added coverage for:
  - Creating an Agent from a description
  - Waiting for the build to complete
  - Verifying the generated Agent appears in the Agents list
  - Deleting the Agent with `DELETE` confirmation
- Renamed the Playwright project and CI workflow entry from `agent-hire-fire` to `agent-create-delete`.

### Reusable Agent test infrastructure

Added reusable Page Objects and fixtures for the current product flow:

- `AgentsPage`
- `HomePage`
- `AgentWorkspacePage`
- `AgentTaskPage`
- `agent-task-session` fixture
- Agent lifecycle cleanup utilities

The shared fixture ensures the test account starts without existing Agents, creates a dedicated Agent for the scenarios, and cleans up Agents after the tests finish.

### Agent behavior scenarios

Migrated the following specs from the legacy shared `/chat` session to Agent Task sessions:

- Chat smoke
- Basic usage
- Web search and URL fetch
- Browser tool

Each behavior scenario starts a fresh conversation through `New Task`, preventing conversation history from leaking between scenarios.

The basic usage attachment scenarios now submit the prompt and attachment together in the same conversation turn.

## Validation

The following staging suites passed:

- `basic-usage`: 7 passed
- `chat-smoke`: 2 passed
- `tool-web`: 3 passed
- `tool-browser`: 2 passed

Quality gates also passed:

- `pnpm install --frozen-lockfile`
- `pnpm exec tsc --noEmit --project app/tsconfig.json`
- `pnpm --filter @zooclaw/web-app run lint`
- `pnpm --filter @zooclaw/web-app run lint:ci`

---
