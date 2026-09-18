---
title: "fix(docx): write LibreOffice conversion output locally before copying to NFS (#281)"
type: "Bug 修复"
priority: "中"
date: "2026-09-17"
status: "待审核"
channels: ""
---

# fix(docx): write LibreOffice conversion output locally before copying to NFS (#281)

## 核心宣传点

Word 转换不再因为直接往 NFS 工作区写文件而卡住：转换先落本地 /tmp 再拷回工作区，doc 转 docx 稳定多了。

## PR 说明

LibreOffice hangs when it writes a converted file directly to the NFS workspace. The existing `soffice.py --headless --convert-to ...` CLI and `doc_to_docx.sh` now write conversion output and a per-call profile to local `/tmp`, then copy the result to the requested workspace directory.

The wrapper checks the exit code and that output exists and is non-empty. It stages the copy beside the destination before replacing it, so failed conversion/copy does not truncate an existing result. Temporary directories are cleaned on normal completion and Python exceptions. Inputs remain at their original paths; the existing socket shim is retained.

Scope: conversion paths only. `accept_changes.py` is unchanged. No revision semantic checks, PDF/DOCX validators, checksum verification, new runtime dependencies, or custom process/signal management. Additional LibreOffice flags are forwarded and script/module entrypoints are covered; non-conversion CLI invocations and the low-level Python `run_soffice` API retain their existing behavior.

Validation:
- 6 targeted tests passed locally, including real binary DOC → DOCX → PDF through the existing CLI wrappers.
- The same 6 tests passed in a disposable staging sandbox on the affected template, with input/final output on NFS v3 (`local_lock=none`) and LibreOffice 7.3.7.2. Sandbox and dedicated workspace prefix were cleaned up.
- Pyright (converter), skill lint, shell syntax, and diff checks passed. Skill lint has 12 pre-existing warnings outside DOCX.
- Path-filtered CI runs those tests with LibreOffice and uses pdfinfo only as a test dependency to verify the generated PDF.

Related infrastructure issue: https://github.com/SerendipityOneInc/e2b-infra/issues/40. This application workaround does not fix NFS locking. No deployment or skill publication is included.

## 原始内容

- 仓库：SerendipityOneInc/ecap-skills
- SHA: `7d3dbdca44cdf86213ffa83cbe5794e7f0ad8e38`
- PR: #281
- 作者：Chris@ZooClaw
- 日期：2026-09-17T12:10:08Z

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
- 6 targeted tests passed locally, including real binary DOC → DO
```
