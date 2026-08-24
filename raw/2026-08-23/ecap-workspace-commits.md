# ecap-workspace commits — 2026-08-23

## test(e2e): stabilize chat flows and align page objects with route ownership (#3490)

- **SHA**: `f0718dfe4ef9c6845ceb9e7142d77a0d4e9a3a84`
- **作者**: rayhuang198212
- **日期**: 2026-08-23T14:27:09Z
- **PR**: #3490

### Commit Message

```
test(e2e): stabilize chat flows and align page objects with route ownership (#3490)

## Summary

This PR improves the stability and maintainability of the E2E test
suite, with a focus on chat flows, session lifecycle, file preview,
agent management, and WebSocket reconnection.

  ## Changes

  - Split chat page-object responsibilities by route:
    - `ZooClawNewChatPage` owns the `/new-chat` launcher flow
    - `ZooClawChatPage` owns active chat and session flows
- `ComposerPickerControls` provides shared agent and model picker
interactions
- Added a shared chat-session coordinator to handle the transition from
the launcher to an active conversation
- Updated chat lifecycle, streaming, action, error, and tool scenarios
to match the current UI flow
- Reworked WebSocket reconnection coverage around observable network
recovery behavior
  - Stabilized file preview generation and artifact sidebar assertions
  - Improved agent manager locators and hire/fire test utilities
  - Added targeted `data-testid` hooks for:
    - Agent manager cards and card actions
    - Artifact preview sidebar
- Updated LLM judge and shared session utilities to reduce flaky waits
and locator ambiguity

  ## Test Coverage

  Updated coverage includes:

  - Chat lifecycle and streaming
  - Chat actions and error handling
  - WebSocket reconnection
  - File and artifact preview
  - Agent manager and agent hire/fire flows
  - Session features
  - Miscellaneous tool scenarios
  - New-chat to active-session transitions
```

### PR Body

## Summary

  This PR improves the stability and maintainability of the E2E test suite, with a focus on chat flows, session lifecycle, file preview, agent management, and WebSocket reconnection.

  ## Changes

  - Split chat page-object responsibilities by route:
    - `ZooClawNewChatPage` owns the `/new-chat` launcher flow
    - `ZooClawChatPage` owns active chat and session flows
    - `ComposerPickerControls` provides shared agent and model picker interactions
  - Added a shared chat-session coordinator to handle the transition from the launcher to an active conversation
  - Updated chat lifecycle, streaming, action, error, and tool scenarios to match the current UI flow
  - Reworked WebSocket reconnection coverage around observable network recovery behavior
  - Stabilized file preview generation and artifact sidebar assertions
  - Improved agent manager locators and hire/fire test utilities
  - Added targeted `data-testid` hooks for:
    - Agent manager cards and card actions
    - Artifact preview sidebar
  - Updated LLM judge and shared session utilities to reduce flaky waits and locator ambiguity

  ## Test Coverage

  Updated coverage includes:

  - Chat lifecycle and streaming
  - Chat actions and error handling
  - WebSocket reconnection
  - File and artifact preview
  - Agent manager and agent hire/fire flows
  - Session features
  - Miscellaneous tool scenarios
  - New-chat to active-session transitions

---

