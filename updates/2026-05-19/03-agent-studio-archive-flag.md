---
title: "Agent Studio 分享功能新增 --archive 打包上传支持"
type: "产品基础功能更新"
priority: "中"
date: "2026-05-19"
status: "待审核"
channels: ""
---
# Agent Studio 分享功能新增 --archive 打包上传支持

## 核心宣传点
Agent Studio 的 /studio share 命令现在支持直接上传本地打包好的 .tar.gz 文件，创作者无需重新打包，分享流程更顺滑。

## 原始内容
```
commit: 3b9362f61f320ac044e873911c87ef40b97b4661
repo: SerendipityOneInc/ecap-agent-pack
author: felix-srp
date: 2026-05-19T17:47:48Z

fix(agent-studio): surface --archive flag in share + pack/command hints at session start (#133)

* fix(agent-studio): surface --archive flag in share + pack/command hints at session start

- agent-studio-share/SKILL.md: document the existing `--archive <path>` flag so
  creators can share a pre-packed `.tar.gz` without repackaging the current
  workspace. The Python already supported it; SKILL.md was hiding it from agents.
- AGENTS.md: add a one-line orientation on first DEV reply (active pack name +
  `/studio` prefix reminder) so creators stop typing `/new` instead of
  `/studio new` and always know which pack the workspace is editing.
- Bump version 1.3.0 → 1.3.1.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(agent-studio): trim tokens in share SKILL.md + AGENTS.md THIRD step

Tighten the prose added in the previous commit. No behavioral change.

- agent-studio-share/SKILL.md: collapse the `--archive` bullet (was ~70 words,
  now ~20) — drop where-to-find-archives illustration and the "package.py
  skipped" sentence (already covered in Internal behavior). Shorten
  `--artifacts-base-url` to `<url>` placeholder. Trim "that path … no
  packaging step" → "directly, no packaging".
- AGENTS.md: trim THIRD step ~30 tokens — drop "mode" / "of session"
  (parallel with FIRST/SECOND), drop "(the name: from agent/agent-pack.yaml)"
  (already read in SECOND), drop ", not /new" (positive example suffices),
  make skip-condition mechanically checkable ("starts with /studio").

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(agent-studio): tighten --archive fallback note + THIRD-step scope

Address review feedback on PR #133:
- SKILL.md: disclose the unversioned-filename fallback for --archive
  (version="unknown") so the documented identity contract matches
  run_share.py's actual parsing behavior.
- AGENTS.md THIRD step: state DEV-only / once-per-session scope and
  explicit TEST = no orientation, removing ambiguity around when the
  one-line orientation fires.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Ning Hu <ning@gensmo.ai>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

--- PR #133 Body ---
## Summary

Two small docs/SOP fixes for Agent Studio v1.3.1, motivated by friction seen with real creators.

- **`/studio share --archive <path>` is now reachable.** `run_share.py` already supported the flag (validates and stages a pre-packed `.tar.gz` without invoking `package.py`), but `agent-studio-share/SKILL.md` never told the agent it existed — so the share flow was locked to "repackage the current workspace" with no way to share a foreign archive. SKILL.md now documents the flag, the no-repackage path, and that an unversioned filename falls back to `version="unknown"` (mirrors `run_share.py`'s actual parsing).
- **Session-start orientation in DEV mode.** AGENTS.md now asks the agent to lead its first reply of a DEV session with a one-line orientation: which pack is active (`name:` from `agent/agent-pack.yaml`) and that creator commands use the `/studio` prefix (e.g. `/studio new`, not `/new`). Scope is explicit: DEV only, once per session, skipped when the user's first message already starts with `/studio`, and silent in TEST so the pack-agent persona is preserved.
- Version bump `1.3.0 → 1.3.1`.

No Python changes.

## Test plan

Verified in a sibling openclaw-docker container (`ghcr.io/serendipityoneinc/openclaw-docker:2026.5.7`) on the patched workspace.

Script-level (run via `uv run --python 3.12 .agents/skills/agent-studio-share/scripts/run_share.py`):

- [x] No `--archive`, no existing `zip/<pack>-<version>.tar.gz` → calls `package.py`; `archive_reused=false`, archive built and staged into `artifacts/shares/`.
- [x] No `--archive`, matching zip already in `zip/` → reuse path; `archive_reused=true`, `package.py` not invoked.
- [x] `--archive zip/imported-pack-2.0.5.tar.gz` → skips `package.py`; `pack_name=imported-pack`, `version=2.0.5` parsed from filename even though the workspace manifest says otherwise (workspace manifest correctly ignored).
- [x] `--archive zip/myarchive.tar.gz` (no version segment) → succeeds with `pack_name=myarchive`, `version="unknown"` (documented fallback).

LLM-level (manual webchat session against the deployed pack):

- [x] DEV first session, neutral message → first reply names the active pack and mentions the `/studio` prefix.
- [x] DEV first message is itself `/studio …` → orientation line skipped, command handled directly.
- [x] TEST mode first reply → pack-agent persona, no orientation line.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```
