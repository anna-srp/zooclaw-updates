# SerendipityOneInc/ecap-workspace — commits 2026-09-07

## fix(ci): migrate weekly architecture review to Foundry (#3664)

- **SHA**: `29d75a67516d42b11a7049a99d6e0e2aaee06a2a`
- **作者**: tim-srp
- **日期**: 2026-09-07T10:29:39Z
- **PR**: #3664

### Commit Message

```
fix(ci): migrate weekly architecture review to Foundry (#3664)

## Summary
Move weekly architecture review for Web, Backend, and iOS from AWS
Bedrock to Microsoft Foundry, using the existing CI Foundry endpoint and
AZURE_OPENAI_API_KEY. Keep Claude Sonnet 4.6 and all review/reporting
behavior unchanged. Remove AWS role setup and unused id-token
permission.

## Root cause
AWS role access was revoked. Run
https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34104690648
failed in all three modules with sts:AssumeRoleWithWebIdentity
authorization errors before review started.

## Test plan
- Ruby YAML parsing and git diff --check passed.
- verify-changed.sh and pre-push gate passed (no applicable local
business-code checks).
- Confirmed pinned Claude Action v1.0.165 supports use_foundry and
matched the existing shared Claude review configuration.
- All PR checks passed, including CodeQL and both automated review jobs.
- Live three-module dry run is running:
https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34110175461
(dry_run=true; no issue mutations).

## Reused configuration
Matches srp-actions/.github/workflows/claude-review.yaml and this
repository's release-notify-lark.yml Foundry configuration: existing
AZURE_OPENAI_API_KEY, srp-openai-cicd-resource Anthropic endpoint, and
pinned Claude Action v1.0.165. No generic reusable architecture-review
workflow exists; preserve the existing local review/report pipeline.

## Review adjudication
Claude review found no correctness issues. Codex claimed
ANTHROPIC_FOUNDRY_BASE_URL is unsupported; this is a false positive: the
official setup explicitly supports this variable as an alternative to
ANTHROPIC_FOUNDRY_RESOURCE
(https://code.claude.com/docs/en/microsoft-foundry), and the shared
Claude review uses it with the same Action version. Retain the existing
configuration pattern. Other AWS-dependent workflows are outside this
weekly-review PR.
```

### PR Body

## Summary
Move weekly architecture review for Web, Backend, and iOS from AWS Bedrock to Microsoft Foundry, using the existing CI Foundry endpoint and AZURE_OPENAI_API_KEY. Keep Claude Sonnet 4.6 and all review/reporting behavior unchanged. Remove AWS role setup and unused id-token permission.

## Root cause
AWS role access was revoked. Run https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34104690648 failed in all three modules with sts:AssumeRoleWithWebIdentity authorization errors before review started.

## Test plan
- Ruby YAML parsing and git diff --check passed.
- verify-changed.sh and pre-push gate passed (no applicable local business-code checks).
- Confirmed pinned Claude Action v1.0.165 supports use_foundry and matched the existing shared Claude review configuration.
- All PR checks passed, including CodeQL and both automated review jobs.
- Live three-module dry run is running: https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34110175461 (dry_run=true; no issue mutations).

## Reused configuration
Matches srp-actions/.github/workflows/claude-review.yaml and this repository's release-notify-lark.yml Foundry configuration: existing AZURE_OPENAI_API_KEY, srp-openai-cicd-resource Anthropic endpoint, and pinned Claude Action v1.0.165. No generic reusable architecture-review workflow exists; preserve the existing local review/report pipeline.

## Review adjudication
Claude review found no correctness issues. Codex claimed ANTHROPIC_FOUNDRY_BASE_URL is unsupported; this is a false positive: the official setup explicitly supports this variable as an alternative to ANTHROPIC_FOUNDRY_RESOURCE (https://code.claude.com/docs/en/microsoft-foundry), and the shared Claude review uses it with the same Action version. Retain the existing configuration pattern. Other AWS-dependent workflows are outside this weekly-review PR.


---

## fix(agents): map fontconfig binaries to apt package (#3663)

- **SHA**: `538d8443d246208ac64ee23249b81ae65476d510`
- **作者**: kaka-srp
- **日期**: 2026-09-07T07:40:43Z
- **PR**: #3663

### Commit Message

```
fix(agents): map fontconfig binaries to apt package (#3663)

## Summary

BossClaw hire fails with “Agent environment is still building” because
its Environment build tries to install nonexistent apt packages
`fc-scan` and `fc-cache`. Map both commands to `fontconfig`, which the
existing package deduplication emits once.

## Root cause

Pack `dependencies.bins` declares executable names. The backend maps
known executables to their apt packages, but previously only handled
`ffprobe` → `ffmpeg`; the fontconfig commands passed through as package
names and failed with `Unable to locate package`.

## Test plan

- [x] Extended the existing archive translation test for both legacy and
strict dependency modes; both cases failed before the mapping fix and
passed afterward.
- [x] Pack translation test file: 75 passed, including package
deduplication and preservation of other dependencies.
- [x] Backend static checks: ruff, formatting, pyright, and
import-linter passed.
- [x] Python pre-commit hooks passed.

## Rollout

Deploy the backend change, then regenerate BossClaw's Environment with
the corrected package configuration and bind the approved submission to
the new ready version. Retrying the existing immutable failed version
retains the invalid package names. This PR does not change production
state.
```

### PR Body

## Summary

BossClaw hire fails with “Agent environment is still building” because its Environment build tries to install nonexistent apt packages `fc-scan` and `fc-cache`. Map both commands to `fontconfig`, which the existing package deduplication emits once.

## Root cause

Pack `dependencies.bins` declares executable names. The backend maps known executables to their apt packages, but previously only handled `ffprobe` → `ffmpeg`; the fontconfig commands passed through as package names and failed with `Unable to locate package`.

## Test plan

- [x] Extended the existing archive translation test for both legacy and strict dependency modes; both cases failed before the mapping fix and passed afterward.
- [x] Pack translation test file: 75 passed, including package deduplication and preservation of other dependencies.
- [x] Backend static checks: ruff, formatting, pyright, and import-linter passed.
- [x] Python pre-commit hooks passed.

## Rollout

Deploy the backend change, then regenerate BossClaw's Environment with the corrected package configuration and bind the approved submission to the new ready version. Retrying the existing immutable failed version retains the invalid package names. This PR does not change production state.


---

## fix(chat): hide historical routing decision progress (#3661)

- **SHA**: `2ba2c8168501e468af68e0c348237fd970375b6a`
- **作者**: sam-srp
- **日期**: 2026-09-07T06:24:09Z
- **PR**: #3661

### Commit Message

```
fix(chat): hide historical routing decision progress (#3661)

## Summary
Hide `routing_decision` tool-status posts through the shared parser,
covering history loading and incoming messages. Previously saved routing
decisions no longer render as indefinitely running activity steps.
Ordinary tool progress and assistant replies remain visible.

## Root cause
The channel conversion published one-shot engine routing decisions with
`phase=update` and no terminal status. The frontend correctly
interpreted that generic progress shape as running, but no completion
event exists for these decisions. Add the internal event name to the
existing hidden-tool list; engine routing data is not changed.

The companion agent-channel-service fix prevents new routing-decision
tool posts.

## Test plan
- [x] Tool-status parser and chat activity suites: 88 tests passed.
- [x] Changed-file ESLint and git diff checks passed.
- Full web gate was not run; Git hooks skipped it because the worktree
has no workspace-root node_modules. Targeted checks above were run using
the existing app dependencies.
```

### PR Body

## Summary
Hide `routing_decision` tool-status posts through the shared parser, covering history loading and incoming messages. Previously saved routing decisions no longer render as indefinitely running activity steps. Ordinary tool progress and assistant replies remain visible.

## Root cause
The channel conversion published one-shot engine routing decisions with `phase=update` and no terminal status. The frontend correctly interpreted that generic progress shape as running, but no completion event exists for these decisions. Add the internal event name to the existing hidden-tool list; engine routing data is not changed.

The companion agent-channel-service fix prevents new routing-decision tool posts.

## Test plan
- [x] Tool-status parser and chat activity suites: 88 tests passed.
- [x] Changed-file ESLint and git diff checks passed.
- Full web gate was not run; Git hooks skipped it because the worktree has no workspace-root node_modules. Targeted checks above were run using the existing app dependencies.


---

## test(e2e): stabilize chat, file preview, and schedule coverage (#3660)

- **SHA**: `855cd95ff9cf2d5951682552ef0ddb21431c63bb`
- **作者**: rayhuang198212
- **日期**: 2026-09-07T02:35:53Z
- **PR**: #3660

### Commit Message

```
test(e2e): stabilize chat, file preview, and schedule coverage (#3660)

## Summary

- Stabilize chat response tracking across launcher-to-session
transitions and prevent assertions from matching stale text or images.
- Align chat, onboarding, and landing-page locators and assertions with
the current UI.
- Strengthen voice-reply coverage by validating both the audio
attachment and its text transcript.
  - Extract reusable page objects for file previews and scheduled jobs.
- Improve file-preview reliability with scoped renderer assertions,
retrying waits, decorated filename support, and longer generation
timeouts.
- Make session title and schedule run-history assertions deterministic.
```

### PR Body

## Summary

  - Stabilize chat response tracking across launcher-to-session transitions and prevent assertions from matching stale text or images.
  - Align chat, onboarding, and landing-page locators and assertions with the current UI.
  - Strengthen voice-reply coverage by validating both the audio attachment and its text transcript.
  - Extract reusable page objects for file previews and scheduled jobs.
  - Improve file-preview reliability with scoped renderer assertions, retrying waits, decorated filename support, and longer generation timeouts.
  - Make session title and schedule run-history assertions deterministic.

---
