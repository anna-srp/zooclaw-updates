---
title: "修复 SlideForge（PPT 生成 Agent）文件交付不稳定问题"
type: "Bug Fix"
priority: "高"
date: "2026-05-22"
status: "待审核"
channels: ""
---

# 修复 SlideForge（PPT 生成 Agent）文件交付不稳定问题

## 核心宣传点

修复了 SlideForge PPT 生成 Agent 有时生成成功但无法下载文件的问题，现在文件交付机制更加可靠，生成的 PPT 能稳定送到你手里。

## 原始内容

**Commit**: 3e6fb72e3a9e72da8c32e296901c493e0b7f7bb7
**Author**: sharplee-srp
**Date**: 2026-05-22T09:27:04Z
**PR**: #141

### Commit Message
```
fix(pptx-master): harden artifact delivery contract (ECA-784) (#141)

* fix(pptx-master): harden artifact delivery contract (ECA-784)

zooclaw-artifact-url rejects path segments outside [A-Za-z0-9.-], so
the existing `artifacts/{topic}.html` guidance silently breaks for any
topic with spaces, underscores, or CJK characters — leaving the file
undelivered. Also the previous {{LINK}} template line carried an
implementation note inline, which an LLM agent could copy into the
user-facing reply.

- AGENTS.md § Step 6: add a "Filename rule" block (ASCII slugify before
  save, rename + rerun on validation failure, concrete examples).
- AGENTS.md delivery template: move the note out of the fenced block so
  the rendered message contains only `{{LINK}}` on its own line.
- output-{html,pptx,pdf,image} SKILL.md: add slugify pointer near each
  save step and replace `{topic}` with `{slug}` in filename examples.

Linear: https://linear.app/srpone/issue/ECA-784

* fix(pptx-master): finish slugify rollout in output-html (ECA-784)

Codex re-review caught three stale `{topic}` examples in output-html
that the previous commit missed — these are the default HTML delivery
path, so leaving the raw `artifacts/{topic}.html` examples in Step 5/6
and §10 could still steer the agent into a filename `zooclaw-artifact-
url` rejects.

Replace `{topic}` with `{slug}` in the save-path heading, the Step 6
CLI example, and the §10 output filename list. References to `{topic}`
inside the slugify-rule sentences themselves are kept (they describe
the input variable, not example filenames).
```

### PR Description
## Summary

`zooclaw-artifact-url` rejects path segments outside `[A-Za-z0-9.-]`, so the existing `artifacts/{topic}.html` guidance silently breaks for any topic with spaces, underscores, or CJK characters — the CLI exits non-zero and the file ends up undelivered (root cause of ECA-784's recurring "file not sent" symptom alongside the agent pasting the local `artifacts/...` path).

This PR also fixes a smaller foot-gun introduced alongside the new delivery contract: the `{{LINK}}` line in the standard delivery template carried an implementation note inline (`← MUST be the stdout of ...`), which an LLM agent could copy verbatim into the user-facing reply, violating the "plain HTTPS URL on its own line" rule.

## Changes

- `pptx-master/AGENTS.md` § Step 6 "Delivery contract":
  - Added a **Filename rule** block — ASCII slugify `[a-z0-9-]` before saving under `artifacts/`, with concrete examples (`「AI 周报」.html` → `ai-weekly-report.html`) and a rename-and-rerun fallback on `illegal characters in segment` errors.
  - Standard delivery template: moved the implementation note **outside** the fenced block so `{{LINK}}` sits alone on its own line in the message agents copy.
- `pptx-master/.agents/skills/output-{html,pptx,pdf,image}/SKILL.md`:
  - Added a short slugify pointer near each "Save to `artifacts/`" step that cross-refs the canonical rule in `AGENTS.md`.
  - Replaced `{topic}` placeholders with `{slug}` in the descriptive filename lists for `output-pdf` and `output-image`.

Docs-only; no `agent-pack.yaml` version bump (consistent with PR #139's pattern for content refreshes on `1.0.0`).

## Verification

- Reviewed twice via Codex (initial pass surfaced the two issues; second pass confirmed both findings resolved on the working-tree diff).
- `git diff --check` clean.
- Cross-checked the validator at `openclaw-docker/zooclaw-artifact-url:52` — the allowed character class in the new rule matches its actual regex (`A-Za-z0-9.-`).

## Linear

https://linear.app/srpone/issue/ECA-784

