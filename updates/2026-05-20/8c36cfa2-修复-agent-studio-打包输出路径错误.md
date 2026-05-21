---
title: "修复 Agent Studio 打包输出路径错误"
type: "Bug Fix"
priority: "中"
date: "2026-05-20"
status: "待审核"
channels: ""
repo: "ecap-agent-pack"
sha: "8c36cfa2891ae4de2939468079fbb0f3e6273d82"
pr: 136
---
# 修复 Agent Studio 打包输出路径错误

## 核心宣传点

修复了 Agent Studio 中 package.py 打包时输出文件路径错误的问题，打包和分发 Agent 现在更可靠。

## 原始内容

### Commit Message

```
fix(agent-studio): anchor package.py --output to pack-dir (#136)

* fix(agent-studio): anchor package.py --output to pack-dir

`--output zip/` was a CWD-relative path. If the studio session's bash CWD
drifted into another workspace (e.g. an installed pack inspected during the
build), package.py silently created `zip/` there instead of in the studio
workspace — so the archive existed but the install UI, which only scans the
studio workspace, couldn't see it.

Anchor a relative `--output` to `pack-dir`. Absolute paths are unchanged for
backward compatibility.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): anchor install.py --output to pack-dir

Same CWD-vs-pack-dir bug as the previous commit, in install.py's
`list-sources` and `install` commands. install.py is usually called from
the studio workspace so the impact is smaller than package.py's, but
keeping the two scripts symmetric removes a latent footgun if the agent
ever drifts CWD between packaging and installing.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): anchor run_share.py --output to pack-dir

Final piece of the CWD-vs-pack-dir symmetry. run_share.py is invoked
both directly (/studio share) and as a subprocess from install.py;
either path could in principle stage the archive under the wrong
workspace if CWD drifted. Aligns with the same fix in package.py and
install.py.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(agent-studio): bump version 1.3.1 → 1.3.2

Patch bump for the package.py / install.py / run_share.py output-anchor fix.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Anchor `--output` to `--pack-dir` (rather than CWD) in three studio scripts so a session-CWD drift can't silently misdirect packaging / scanning / sharing into the wrong workspace.

- **`package.py`** — original reported bug. With `--output zip/` resolved against CWD, an in-session `cd` into another workspace (e.g. an installed pack inspected during the build) silently created `zip/` there. The install UI only scans the studio workspace, so the archive existed but couldn't be selected.
- **`install.py`** (`list-sources` + `install`) — same latent footgun on the install side: a CWD-drifted invocation would either scan the wrong `zip/` (`list-sources`) or stage the current pack's archive into the wrong workspace (`install --source current`, via `run_share.py`).
- **`run_share.py`** — same anchoring on the share path, both for direct `/studio share` and for the `install.py` subprocess call.

In all three: relative `--output` is now resolved against `pack_dir.resolve()`; absolute paths pass through unchanged.

## Repro / evidence

On the affected prod pod (`oc-f0dcf1f4-94f9cc886-c9jkg`):

```
workspace-agent_studio/zip/                                   ← correct
  xiaohongshu-publisher-{0.1.0, 0.2.0, 0.2.1, 0.2.2}.tar.gz   (09:57–09:58, after agent noticed and re-packaged)

workspace-custom-xiaohongshu-publisher-0-1-0/zip/             ← wrong
  xiaohongshu-publisher-{0.2.0, 0.2.1, 0.2.2}.tar.gz          (08:49–09:46)
```

Same Studio session packaged three versions into the installed pack's workspace before the agent caught it and re-packaged into the right place. Deterministic given the CWD drift — not intermittent.

## Test plan

- [x] Manual: `package.py --pack-dir /abs/path --output zip/` from `/tmp` — archive lands at `/abs/path/zip/`, not `/tmp/zip/`.
- [x] Manual: `install.py list-sources --pack-dir /abs/path --output zip/` from `/tmp` — no `/tmp/zip/` created; scan reads `/abs/path/zip/`.
- [x] Manual: `run_share.py --pack-dir /abs/path --output zip/` from `/tmp` — no `/tmp/zip/` created (errors expected before staging since the studio repo itself isn't a user pack).
- [x] AST parse-check on all three files.
- [ ] Reviewer: confirm normal `/studio publish` / `/studio install --source current` / `/studio share` paths still behave identically when invoked from the studio workspace (CWD == pack-dir, so the new anchoring is a no-op there).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
