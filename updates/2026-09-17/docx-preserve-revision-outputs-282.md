---
title: "fix(docx): preserve revision outputs when LibreOffice fails (#282)"
type: "Bug 修复"
priority: "中"
date: "2026-09-17"
status: "待审核"
channels: ""
---

# fix(docx): preserve revision outputs when LibreOffice fails (#282)

## 核心宣传点

docx 技能接受修订时，LibreOffice 卡死或超时不再把已有成品文档覆盖成未处理的原稿，失败会明确报错而不是假装成功。

## PR 说明

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

## 原始内容

- 仓库：SerendipityOneInc/ecap-skills
- SHA: `91d1ba5d056ff92d6fe44d680fb7e8b40a2bd2a3`
- PR: #282
- 作者：Chris@ZooClaw
- 日期：2026-09-17T12:40:23Z

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
format va
```
