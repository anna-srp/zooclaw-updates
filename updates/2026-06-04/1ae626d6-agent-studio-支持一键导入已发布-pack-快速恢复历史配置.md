---
title: "Agent Studio 支持一键导入已发布 Pack，快速恢复历史配置"
type: "新功能上线"
priority: "高"
date: "2026-06-04"
status: "待审核"
channels: ""
sha: "1ae626d6a54a56090dd6904b18c8d3cb56b8ee68"
repo: "ecap-agent-pack"
pr: "162"
---

# Agent Studio 支持一键导入已发布 Pack，快速恢复历史配置

## 核心宣传点

在 Agent Studio 中打开 /studio，现支持直接导入已发布的 Agent Pack 归档文件，并恢复 snapshot 前的配置状态，让 Agent 的版本管理和回滚更便捷。

## 原始内容

### Commit Message

```
feat(agent-studio): /studio open imports published archives, restore pre-snapshot packs to built state (#162)

Adds /studio open <archive|share-url> via new import_archive.py (reverse of package.py), restoring a pre-snapshot pack's source + scaffold-state + zip artifact + delivery proof + snapshot. Fixes the empty/placeholder-pack failure from LLM-improvised builds in deployed workspaces. SKILL.md guardrail + 14-test suite (104 pass). Bumps agent-studio 1.4.2 → 1.5.0.
```

### PR Description

## Why

When a creator wants to update an old pack that predates the snapshot mechanism (or whose snapshot was lost), `list_packs.py` returns it as unavailable and `/studio open <name>` can't restore it. With no legitimate update path, Studio's LLM improvised by `cd`-ing into the **deployed** agent's runtime workspace (`~/.openclaw/agents/<id>/`, `/workspace/<other>/`) and running `package.py` there.

That improvisation ships a broken pack:

- The deployed layout has `.agents/skills/` (runtime), not the `skills/` (pack-source) that `package.py` reads — so the archive contains **zero skills**.
- The deployed workspace has no `agent/*.md` pack-source, so Studio satisfies `package.py`'s required-files check by writing `(To be filled in by Agent Studio during Stage 3.)` placeholders into `agent/AGENTS.md` / `SOUL.md` / `IDENTITY.md` — and ships those placeholders to the catalog.

**Real-world repro:** a prod agent installed via this path ("Chanel Stylist") looked identical to the default chat — no skills, no persona — because the catalog archive was a ~2.5 KB shell. The fully-built `.agents/skills/` + root `.md` content was orphaned in the deployed workspace.

## What

### `/studio open <target>` — one command, dispatch by target shape

| Target shape | Treated as | Backed by |
|---|---|---|
| `https://` artifacts URL (or its base64) | share URL | `import_archive.py --share` |
| local `.tar.gz` / `.tgz` path | local archive | `import_archive.py --archive` |
| anything else | snapshot name | `snapshot.py restore` |

A snapshot name not in `list_packs.py` errors with the available names — it does **not** fall through to "treat as archive" (never what a typo meant). The `--share` URL is validated against the Studio artifacts CDN shape (`https://artifacts.<host>/[<bot>/<agent>/]artifacts/shares/<name>-<version>.tar.gz`); arbitrary URLs are refused.

### `import_archive.py` — reverse of `package.py`

Maps the archive back into Studio's workspace:

| archive | → workspace |
|---|---|
| root `*.md` / `agent-pack.yaml` / `description.json` | `agent/*` |
| `.agents/skills/<n>/…` | `skills/<n>/…` |
| `scripts/…`, `data/…` | same path |
| `artifacts/avatar.png` (or legacy root) | `agent/avatar.png` |

### Restores the pack to its built *state*, not just its files

After extraction the import reconstructs the signals Studio uses to recompute "current stage" — which otherwise never travel inside a pack archive, so a re-imported published pack used to drop back to **Stage 4 (Testing)**:

- `data/.scaffold-state.json` — `agent_dir_filled` true, or **false + warning** when the archive still ships Stage-3 placeholders (the direct guard against the chanel-stylist failure mode above).
- `zip/<name>-<version>.tar.gz` — the archive is restored as the publish artifact → recognized as **already packaged**.
- `data/.delivery-state.json` — for `--share`, the artifacts URL is durable proof of prior delivery, so the delivery record is rebuilt (via the shared `write_delivery_state`) → resumes at **done**. A local `--archive` proves packaging only → resumes at **Stage 6**. A placeholder pack is never marked delivered.
- an initial **snapshot** so the next `/studio open <name>` takes the fast snapshot path and the pack shows in `/studio list`.

The two stage-marker restores are soft-fail: the pack source is already committed, so a copy/write error only costs the stage promotion and surfaces an actionable warning.

### Safety

Layout is enforced by the existing `assert_archive_layout` contract (rejects symlinks, hardlinks, absolute paths, parent traversal, forbidden top-level `agent/`/`skills/`/`package/`). Extraction stages into a temp dir then does an atomic per-top-level-dir move-aside + `os.replace` with rollback. Decompression-bomb cap (256 MiB uncompressed); remote downloads reuse `install.py`'s 64 MiB cap + 30 s timeout, HTTPS-only.

### Guardrail (SKILL.md)

Adds **"Build and pack only in Studio's own workspace"** — every script `--pack-dir` must resolve to Studio's workspace, never a deployed agent's. `/studio open <archive>` is named as the legitimate "old pack, no snapshot" path. The Truth-sources section records `import_archive.py` as a writer of both `.scaffold-state.json` and (for `--share`) `.delivery-state.json`. BOOTSTRAP.md option (c) describes the unified `<target>` form.

## How tested

`import_archive.py` test suite — 14 tests; full agent-studio suite **104 pass**:

- **Round-trip:** `package.py` → `import_archive.py` preserves pack source byte-for-byte; a sync test asserts the import layout map can't drift from `package.py`'s `_AGENT_PACKABLE`.
- **Stage restore:** `--archive` import lands `zip/<v>.tar.gz` and writes no delivery-state; `--share` import additionally writes delivery-state with the real `share_url`; a placeholder pack via `--share` is left unmarked.
- **`--share` validation:** accepts the real artifacts URL (short + full `bot/agent` form) and its base64; rejects wrong host / wrong path / bad filename / `http` / missing version.
- **Refusals:** path-traversal name, non-conforming filename, dirty workspace, `.mode == test`, pre-existing symlink.
- **Placeholder:** archive shipping `(To be filled…)` → `agent_dir_filled=false` + warning.

Also verified end-to-end in a devcontainer against the real prod artifact (`plh-merchandiser-0.1.0` via its share URL): restores `zip/` + delivery-state, and `/studio list` shows it **✅ Delivered**.

## Not in scope

- A `package.py`-side check that rejects placeholder `(To be filled…)` agent files at pack time — belt-and-braces on top of the import path's detection. Follow-up.
- Legacy-avatar restaging for share URLs (`install.py`'s `_restage_remote_if_legacy`). Import accepts the URL; it just doesn't normalize legacy avatar layouts. Follow-up.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

