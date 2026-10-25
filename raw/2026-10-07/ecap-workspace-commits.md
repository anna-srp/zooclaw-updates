# SerendipityOneInc/ecap-workspace — commits 2026-10-07

## test(e2e): Align coverage with the current Home, Agent, and Settings UI (#4027)

- **SHA**: `f1ce8873b99dc340a1c3b6395ea38bb7dd69d869`
- **作者**: rayhuang198212
- **日期**: 2026-10-07T13:18:24Z
- **PR**: #4027

### Commit Message

```
test(e2e): Align coverage with the current Home, Agent, and Settings UI (#4027)

## Summary

Several E2E specs still exercised legacy chat routes, standalone
scheduling, and Hire/Fire flows. Update them to use the current Home,
Agent workspace, and Settings UI.

- Cover schedules inside a dedicated Agent workspace, with Agent
creation and cleanup.
- Rename claw-settings to settings and update Playwright and CI project
names.
- Update profile and insufficient-credit coverage to use current
Settings and Agent Task flows.
- Switch language and theme through Settings General, then verify Home
and Agent Task behavior.
- Update landing and keyboard accessibility coverage and remove obsolete
flows.
- Remove unused legacy navigation helpers and Agent picker methods.
- Use the current overlay contract for popup dismissal, fix
multiple-overlay handling, and separate Agent Task response-wait tests.

Mini-chat and subagent specs remain unchanged from main.

## Validation

- Passed: frozen-lockfile install, TypeScript, ESLint, and CI lint.
- Staging: settings — 5 passed, 3 existing skips; insufficient-credits —
6 passed; chat-errors — 5 passed.
- Helper regression tests: popup-helper and response-wait-helper — 6
passed.

## Known issue

Dark-mode-smoke retains the assertion exposing the Home theme
regression: selecting Dark in Settings and navigating to Home does not
consistently preserve the dark theme. This product issue remains
unresolved; the test was not skipped or weakened.
```

### PR Body

## Summary

Several E2E specs still exercised legacy chat routes, standalone scheduling, and Hire/Fire flows. Update them to use the current Home, Agent workspace, and Settings UI.

- Cover schedules inside a dedicated Agent workspace, with Agent creation and cleanup.
- Rename claw-settings to settings and update Playwright and CI project names.
- Update profile and insufficient-credit coverage to use current Settings and Agent Task flows.
- Switch language and theme through Settings General, then verify Home and Agent Task behavior.
- Update landing and keyboard accessibility coverage and remove obsolete flows.
- Remove unused legacy navigation helpers and Agent picker methods.
- Use the current overlay contract for popup dismissal, fix multiple-overlay handling, and separate Agent Task response-wait tests.

Mini-chat and subagent specs remain unchanged from main.

## Validation

- Passed: frozen-lockfile install, TypeScript, ESLint, and CI lint.
- Staging: settings — 5 passed, 3 existing skips; insufficient-credits — 6 passed; chat-errors — 5 passed.
- Helper regression tests: popup-helper and response-wait-helper — 6 passed.

## Known issue

Dark-mode-smoke retains the assertion exposing the Home theme regression: selecting Dark in Settings and navigating to Home does not consistently preserve the dark theme. This product issue remains unresolved; the test was not skipped or weakened.

---
