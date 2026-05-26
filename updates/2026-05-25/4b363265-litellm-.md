---
title: "修复 LiteLLM 安装来源，提升服务稳定性"
type: "Bug Fix"
priority: "中"
date: "2026-05-25"
status: "待审核"
channels: ""
---

# 修复 LiteLLM 安装来源，提升服务稳定性

## 核心宣传点

将 LiteLLM 恢复从 PyPI 安装，避免直接从 GitHub 安装可能导致的不稳定问题

## 原始内容

**仓库**: SerendipityOneInc/ecap-workspace  
**Commit**: 4b363265fcd1d7fbf5cf329b3ad932d145b7089a  
**作者**: tim-srp  
**日期**: 2026-05-25T06:22:01Z  

**Commit Message**:

```
fix(claw-interface): restore litellm install from PyPI (#1902)

## Summary
- Switch `services/claw-interface/requirements.txt` from
`git+https://github.com/BerriAI/litellm.git@v1.82.3` to
`litellm==1.82.3`.
- Same exact version (1.82.3), only the install source changes (git →
PyPI).
- Speeds up every fresh devcontainer / CI `uv pip install` by skipping
the git clone + setuptools wheel build of litellm (several minutes →
~15s for a cached PyPI wheel).

## Root cause
The original switch to git install — `91fb7a48` (2026-03-24, "fix:
install litellm from GitHub (PyPI quarantined)") — was a workaround for
PyPI quarantining all litellm versions. That quarantine has since been
lifted:

- `GET https://pypi.org/pypi/litellm/1.82.3/json` → `200`, both files
`yanked=False`
- `GET https://pypi.org/simple/litellm/` → `200`
- `pypi.org/pypi/litellm/json` lists 1.86.0 as latest stable (so the
project is actively publishing again)

`pyproject.toml`'s `[tool.deptry.package_module_name_map]` entry
`litellm = "litellm"` was already added as a defensive identity mapping
intended to survive a PyPI ↔ git source flip (per its own comment), so
no other config changes are needed.

## Test plan
- [x] Confirm PyPI hosts 1.82.3 unyanked: `curl
pypi.org/pypi/litellm/1.82.3/json | jq '.urls[].yanked'`
- [x] `uv pip install --reinstall-package litellm 'litellm==1.82.3'`
succeeds and replaces the git-installed copy
- [x] `importlib.metadata.version("litellm")` → `'1.82.3'`
- [x] `litellm.acompletion`, `litellm.exceptions.BadRequestError`,
`litellm.api_base`, `litellm.api_key` all available (these are the only
attrs used by `app/routes/litellm.py`)
- [x] `from app.routes import litellm` + `app.create_app.create_app()`
import cleanly (211 routes)
- [ ] CI `python-code-quality` (ruff + pyright + pytest + deptry +
import-linter) green
- [ ] `code-quality` (frontend lint+tsc+unit) — not relevant to this
change, expected unaffected

## Notes
- `app/routes/litellm.py` is documented as deprecated in
`services/claw-interface/CLAUDE.md` (legacy — serves only
`fullstack_assistant` and `canvas`; OpenClaw doesn't call it). The
conservative choice to stay at `1.82.3` rather than jump to latest
1.86.0 avoids spending regression effort on a module being phased out.
- `services/claw-interface/uv.lock` is an 8-line placeholder (only the
virtual `claw-interface` package), so no lockfile update is needed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>
```

**PR Description**:

## Summary
- Switch `services/claw-interface/requirements.txt` from `git+https://github.com/BerriAI/litellm.git@v1.82.3` to `litellm==1.82.3`.
- Same exact version (1.82.3), only the install source changes (git → PyPI).
- Speeds up every fresh devcontainer / CI `uv pip install` by skipping the git clone + setuptools wheel build of litellm (several minutes → ~15s for a cached PyPI wheel).

## Root cause
The original switch to git install — `91fb7a48` (2026-03-24, "fix: install litellm from GitHub (PyPI quarantined)") — was a workaround for PyPI quarantining all litellm versions. That quarantine has since been lifted:

- `GET https://pypi.org/pypi/litellm/1.82.3/json` → `200`, both files `yanked=False`
- `GET https://pypi.org/simple/litellm/` → `200`
- `pypi.org/pypi/litellm/json` lists 1.86.0 as latest stable (so the project is actively publishing again)

`pyproject.toml`'s `[tool.deptry.package_module_name_map]` entry `litellm = "litellm"` was already added as a defensive identity mapping intended to survive a PyPI ↔ git source flip (per its own comment), so no other config changes are needed.

## Test plan
- [x] Confirm PyPI hosts 1.82.3 unyanked: `curl pypi.org/pypi/litellm/1.82.3/json | jq '.urls[].yanked'`
- [x] `uv pip install --reinstall-package litellm 'litellm==1.82.3'` succeeds and replaces the git-installed copy
- [x] `importlib.metadata.version("litellm")` → `'1.82.3'`
- [x] `litellm.acompletion`, `litellm.exceptions.BadRequestError`, `litellm.api_base`, `litellm.api_key` all available (these are the only attrs used by `app/routes/litellm.py`)
- [x] `from app.routes import litellm` + `app.create_app.create_app()` import cleanly (211 routes)
- [ ] CI `python-code-quality` (ruff + pyright + pytest + deptry + import-linter) green
- [ ] `code-quality` (frontend lint+tsc+unit) — not relevant to this change, expected unaffected

## Notes
- `app/routes/litellm.py` is documented as deprecated in `services/claw-interface/CLAUDE.md` (legacy — serves only `fullstack_assistant` and `canvas`; OpenClaw doesn't call it). The conservative choice to stay at `1.82.3` rather than jump to latest 1.86.0 avoids spending regression effort on a module being phased out.
- `services/claw-interface/uv.lock` is an 8-line placeholder (only the virtual `claw-interface` package), so no lockfile update is needed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
