# SerendipityOneInc/ecap-skills — commits 2026-09-17

## ci: consolidate skill tests with change-based selection (#283)

- **SHA**: `96d070d480371a5b9c86ef2ee2c2f0ca34194eea`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-17T12:55:03Z
- **PR**: #283

### Commit Message

```
ci: consolidate skill tests with change-based selection (#283)

Replace the Council, DOCX conversion and DOCX revision workflows with
one
Skill Tests workflow. Select registered suites from the complete Git
diff:
skill directory changes run that skill, shared .github changes and
manual
runs run all suites, and unrelated changes skip skill jobs successfully.
Unavailable comparison history conservatively runs all suites.

Council retains its existing Python 3.12 pytest command. DOCX uses
Python
3.11 and one LibreOffice/Poppler setup for all 13 conversion/revision
tests
and the existing script typechecks. A stable Skill tests result
aggregates
selected jobs; a failed selector or failed/cancelled selected job fails
it.
PRs, pushes to main, merge queues and workflow_dispatch are supported.

The registry in .github/scripts/skill-tests.mjs is the single place to
add
skill-specific runtime/dependencies/commands. Existing tests that were
not
in CI are not enabled implicitly. No product code or branch protection
settings change.

Validation: 3 selector tests cover unrelated/individual/shared changes,
renames/deletions, >300 changed files, empty-matrix CLI output and
missing
history. Strict JavaScript typecheck and actionlint passed (using the
existing Blacksmith runner label). Council: 376 passed. DOCX: 13 passed,
including real LibreOffice. Python typechecks and git diff checks
passed.

This PR targets main and consolidates the existing Council and DOCX CI
workflows, removing all three old workflows together.
```

### PR Body

Replace the Council, DOCX conversion and DOCX revision workflows with one
Skill Tests workflow. Select registered suites from the complete Git diff:
skill directory changes run that skill, shared .github changes and manual
runs run all suites, and unrelated changes skip skill jobs successfully.
Unavailable comparison history conservatively runs all suites.

Council retains its existing Python 3.12 pytest command. DOCX uses Python
3.11 and one LibreOffice/Poppler setup for all 13 conversion/revision tests
and the existing script typechecks. A stable Skill tests result aggregates
selected jobs; a failed selector or failed/cancelled selected job fails it.
PRs, pushes to main, merge queues and workflow_dispatch are supported.

The registry in .github/scripts/skill-tests.mjs is the single place to add
skill-specific runtime/dependencies/commands. Existing tests that were not
in CI are not enabled implicitly. No product code or branch protection
settings change.

Validation: 3 selector tests cover unrelated/individual/shared changes,
renames/deletions, >300 changed files, empty-matrix CLI output and missing
history. Strict JavaScript typecheck and actionlint passed (using the
existing Blacksmith runner label). Council: 376 passed. DOCX: 13 passed,
including real LibreOffice. Python typechecks and git diff checks passed.

This PR targets main and consolidates the existing Council and DOCX CI
workflows, removing all three old workflows together.


---

## fix(docx): preserve revision outputs when LibreOffice fails (#282)

- **SHA**: `91d1ba5d056ff92d6fe44d680fb7e8b40a2bd2a3`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-17T12:40:23Z
- **PR**: #282

### Commit Message

```
fix(docx): preserve revision outputs when LibreOffice fails (#282)

`accept_changes.py` currently copies the input over the destination
before running LibreOffice, then reports a 30-second timeout as
successful revision acceptance. A stalled/failed invocation can
therefore replace an existing output with an unprocessed document while
callers receive a success message. Calls also share one LibreOffice
profile.

Process a private local copy with a per-call profile, and replace the
destination only after the Office process succeeds and the output copy
completes. Initialization and acceptance timeouts/nonzero exits now
return errors. The macro terminates its private Office instance after
storing and closing the document, so successful work exits normally. The
function signature, CLI arguments and message format are preserved.

This PR now targets main after #281 was merged. The global-test-workflow
PR #283 remains stacked on this PR so it can consolidate both DOCX
suites together. The revision implementation touches different files and
does not use the conversion helper in #281. Scope is failure handling
and invocation isolation, without a new revision/XML semantic validator,
format validator, checksum layer, or runtime dependency. Existing
LibreOffice timeouts remain 10 seconds for initialization and 30 seconds
for acceptance.

Validation:
- All 7 targeted tests passed locally, including real LibreOffice
accepting tracked insertions/deletions and preserving the source.
- The same 7 tests passed on the affected staging sandbox template with
LibreOffice 7.3.7.2 and input/output on NFS v3 (`local_lock=none`).
Disposable sandbox and dedicated workspace prefix were cleaned up; no
user agents/data were modified.
- Tests cover initialization/acceptance timeout and nonzero exit, failed
destination copy, concurrent profile isolation, identical input/output
rejection, and CLI failure status.
- Pyright, skill lint and diff checks passed (12 existing lint warnings
in unrelated skills).
- Added a path-filtered CI workflow for this script and its tests.

No deployment or skill publication is included. Infrastructure root
cause remains tracked in SerendipityOneInc/e2b-infra#40.
```

### PR Body

`accept_changes.py` currently copies the input over the destination before running LibreOffice, then reports a 30-second timeout as successful revision acceptance. A stalled/failed invocation can therefore replace an existing output with an unprocessed document while callers receive a success message. Calls also share one LibreOffice profile.

Process a private local copy with a per-call profile, and replace the destination only after the Office process succeeds and the output copy completes. Initialization and acceptance timeouts/nonzero exits now return errors. The macro terminates its private Office instance after storing and closing the document, so successful work exits normally. The function signature, CLI arguments and message format are preserved.

This PR now targets main after #281 was merged. The global-test-workflow PR #283 remains stacked on this PR so it can consolidate both DOCX suites together. The revision implementation touches different files and does not use the conversion helper in #281. Scope is failure handling and invocation isolation, without a new revision/XML semantic validator, format validator, checksum layer, or runtime dependency. Existing LibreOffice timeouts remain 10 seconds for initialization and 30 seconds for acceptance.

Validation:
- All 7 targeted tests passed locally, including real LibreOffice accepting tracked insertions/deletions and preserving the source.
- The same 7 tests passed on the affected staging sandbox template with LibreOffice 7.3.7.2 and input/output on NFS v3 (`local_lock=none`). Disposable sandbox and dedicated workspace prefix were cleaned up; no user agents/data were modified.
- Tests cover initialization/acceptance timeout and nonzero exit, failed destination copy, concurrent profile isolation, identical input/output rejection, and CLI failure status.
- Pyright, skill lint and diff checks passed (12 existing lint warnings in unrelated skills).
- Added a path-filtered CI workflow for this script and its tests.

No deployment or skill publication is included. Infrastructure root cause remains tracked in SerendipityOneInc/e2b-infra#40.



---

## ci: restore Claude review through OpenRouter (#284)

- **SHA**: `e3e484d070f6f628846fae522d42df150f7e8ed5`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-17T12:39:15Z
- **PR**: #284

### Commit Message

```
ci: restore Claude review through OpenRouter (#284)

## Summary

Restore Claude Code review through OpenRouter following
SerendipityOneInc/gcp-foundation#553. Use the shared workflow's default
Claude Sonnet 5 model and pass the organization-provided
`OPENROUTER_API_KEY` instead of the Foundry credential. Skip Claude
review on fork PRs, whose secrets are unavailable.

Preserve the existing Codex reviewer, repository prompts, and effort
settings. Align the gate's Claude-enabled input with the fork guard so
an intentionally skipped Claude job is not treated as a missing review.
Repository administration also restores
`AUTO_REVIEW_CLAUDE_ENABLED=true`; merge this workflow change to apply
the provider switch to future branches.

## Validation

- PyYAML parsing and focused assertions for provider, secrets, fork
guard, and Claude gate wiring
- Asserted existing Codex configuration and additional review prompts
remain unchanged; checked Claude gate eligibility for
enabled/disabled/unset variables, fork/same-repo PRs, and merge-group
events
- actionlint
- git diff --check
- Confirmed the repository can access the organization-level App and
OpenRouter secrets (metadata only)

Application code and dependencies are unchanged; full application suites
were not run locally.
```

### PR Body

## Summary

Restore Claude Code review through OpenRouter following SerendipityOneInc/gcp-foundation#553. Use the shared workflow's default Claude Sonnet 5 model and pass the organization-provided `OPENROUTER_API_KEY` instead of the Foundry credential. Skip Claude review on fork PRs, whose secrets are unavailable.

Preserve the existing Codex reviewer, repository prompts, and effort settings. Align the gate's Claude-enabled input with the fork guard so an intentionally skipped Claude job is not treated as a missing review. Repository administration also restores `AUTO_REVIEW_CLAUDE_ENABLED=true`; merge this workflow change to apply the provider switch to future branches.

## Validation

- PyYAML parsing and focused assertions for provider, secrets, fork guard, and Claude gate wiring
- Asserted existing Codex configuration and additional review prompts remain unchanged; checked Claude gate eligibility for enabled/disabled/unset variables, fork/same-repo PRs, and merge-group events
- actionlint
- git diff --check
- Confirmed the repository can access the organization-level App and OpenRouter secrets (metadata only)

Application code and dependencies are unchanged; full application suites were not run locally.


---

## fix(docx): write LibreOffice conversion output locally before copying to NFS (#281)

- **SHA**: `7d3dbdca44cdf86213ffa83cbe5794e7f0ad8e38`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-17T12:10:08Z
- **PR**: #281

### Commit Message

```
fix(docx): write LibreOffice conversion output locally before copying to NFS (#281)

LibreOffice hangs when it writes a converted file directly to the NFS
workspace. The existing `soffice.py --headless --convert-to ...` CLI and
`doc_to_docx.sh` now write conversion output and a per-call profile to
local `/tmp`, then copy the result to the requested workspace directory.

The wrapper checks the exit code and that output exists and is
non-empty. It stages the copy beside the destination before replacing
it, so failed conversion/copy does not truncate an existing result.
Temporary directories are cleaned on normal completion and Python
exceptions. Inputs remain at their original paths; the existing socket
shim is retained.

Scope: conversion paths only. `accept_changes.py` is unchanged. No
revision semantic checks, PDF/DOCX validators, checksum verification,
new runtime dependencies, or custom process/signal management.
Additional LibreOffice flags are forwarded and script/module entrypoints
are covered; non-conversion CLI invocations and the low-level Python
`run_soffice` API retain their existing behavior.

Validation:
- 6 targeted tests passed locally, including real binary DOC → DOCX →
PDF through the existing CLI wrappers.
- The same 6 tests passed in a disposable staging sandbox on the
affected template, with input/final output on NFS v3 (`local_lock=none`)
and LibreOffice 7.3.7.2. Sandbox and dedicated workspace prefix were
cleaned up.
- Pyright (converter), skill lint, shell syntax, and diff checks passed.
Skill lint has 12 pre-existing warnings outside DOCX.
- Path-filtered CI runs those tests with LibreOffice and uses pdfinfo
only as a test dependency to verify the generated PDF.

Related infrastructure issue:
https://github.com/SerendipityOneInc/e2b-infra/issues/40. This
application workaround does not fix NFS locking. No deployment or skill
publication is included.
```

### PR Body

LibreOffice hangs when it writes a converted file directly to the NFS workspace. The existing `soffice.py --headless --convert-to ...` CLI and `doc_to_docx.sh` now write conversion output and a per-call profile to local `/tmp`, then copy the result to the requested workspace directory.

The wrapper checks the exit code and that output exists and is non-empty. It stages the copy beside the destination before replacing it, so failed conversion/copy does not truncate an existing result. Temporary directories are cleaned on normal completion and Python exceptions. Inputs remain at their original paths; the existing socket shim is retained.

Scope: conversion paths only. `accept_changes.py` is unchanged. No revision semantic checks, PDF/DOCX validators, checksum verification, new runtime dependencies, or custom process/signal management. Additional LibreOffice flags are forwarded and script/module entrypoints are covered; non-conversion CLI invocations and the low-level Python `run_soffice` API retain their existing behavior.

Validation:
- 6 targeted tests passed locally, including real binary DOC → DOCX → PDF through the existing CLI wrappers.
- The same 6 tests passed in a disposable staging sandbox on the affected template, with input/final output on NFS v3 (`local_lock=none`) and LibreOffice 7.3.7.2. Sandbox and dedicated workspace prefix were cleaned up.
- Pyright (converter), skill lint, shell syntax, and diff checks passed. Skill lint has 12 pre-existing warnings outside DOCX.
- Path-filtered CI runs those tests with LibreOffice and uses pdfinfo only as a test dependency to verify the generated PDF.

Related infrastructure issue: https://github.com/SerendipityOneInc/e2b-infra/issues/40. This application workaround does not fix NFS locking. No deployment or skill publication is included.


---
