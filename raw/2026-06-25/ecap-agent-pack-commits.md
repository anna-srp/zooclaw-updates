# SerendipityOneInc/ecap-agent-pack — commits 2026-06-25


共 2 个 commit


---

## chore(agent-studio): bump version to 2.1.0 (#191)

- **SHA**: 882b5b6fc445f7263fae1650ae26d03fe2002207
- **作者**: kaka-srp (@kaka-srp)
- **日期**: 2026-06-25T15:34:00Z
- **PR**: #191
- **URL**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/882b5b6fc445f7263fae1650ae26d03fe2002207

### 完整 Commit Message

```
chore(agent-studio): bump version to 2.1.0 (#191)
```

### 完整 PR Body

## Summary

- Bump `agent-studio` pack version from `2.0.1` to `2.1.0`.
- This prepares the merged Agent Builder reset/workspace fixes from #190 for a new release tag.

## Verification

- `python3 .github/scripts/agent_release.py validate-changed --root . --paths-file <(printf 'agent-studio/agent-pack.yaml\n')`

## Release note

After this PR merges, create/push `v2.1.0-release` to trigger the production agent-studio package upload workflow.



---

## fix(agent-studio): recreate bootstrap on project reset (#190)

- **SHA**: 21d1e9dfe0d5137d9f71d61dc6252cc8ed6ad277
- **作者**: kaka-srp (@kaka-srp)
- **日期**: 2026-06-25T15:25:48Z
- **PR**: #190
- **URL**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/21d1e9dfe0d5137d9f71d61dc6252cc8ed6ad277

### 完整 Commit Message

```
fix(agent-studio): recreate bootstrap on project reset (#190)

* fix(agent-studio): recreate bootstrap on reset

* fix(agent-studio): add project workspace materializer

* fix(agent-studio): allow legacy project restore on missing snapshot

* fix(agent-studio): tag pack tests with builder project

* fix(agent-studio): pass prior pack test run for reuse

* fix(agent-studio): harden project reset and runtime reuse
```

### 完整 PR Body

## Summary

- Make `clean.py --confirm` delete stale root `BOOTSTRAP.md` / `BOOTSTRAP.md.done` and recreate `BOOTSTRAP.md` from the current Agent Studio template.
- Update `templates/BOOTSTRAP.md.tmpl` to match the Agent Builder UI flow: project history, Package & Test, Accept Test, Submit, Share, and Open are UI/backend controls.
- Add `scripts/project_workspace.py` so Agent Builder can capture, clear, and restore per-project workspace files inside the single physical `workspace-agent_studio`.
- Add regression tests for stale bootstrap reset, symlink-safe cleanup, and project workspace A/B switching.

## Why

New Project should behave like the old `/studio new` flow: after reset, the builder session must see a fresh root `BOOTSTRAP.md` and run first-time bootstrap again. The previous `clean.py` restored `BOOTSTRAP.md.done` back to `BOOTSTRAP.md`, which could reuse old consumed bootstrap content from a prior project/version.

Project History also needs protection now that multiple Builder projects share one installed Agent Studio workspace. Without a project-scoped materializer, opening project B after project A can leave A's local `agent/`, `skills/`, `zip/`, or other pack content in the live workspace. `project_workspace.py` makes that switch explicit:

- capture the previously active project into `.agent-builder-projects/<project_id>/workspace`;
- restore the selected project before continuing work or Package & Test;
- clear the live pack content for new/open project starts;
- refuse to adopt a live workspace if `BUILDER_PROJECT_CONTEXT.json` proves it belongs to a different project.

The backend will prefer this script when present and keep an inline fallback for older installed Agent Studio versions, so existing bots do not break before they receive this pack update.

## Script Audit

- `clean.py`: changed to create a fresh root `BOOTSTRAP.md` from `templates/BOOTSTRAP.md.tmpl`.
- `project_workspace.py`: new script for Builder UI project switching; it only manages pack content paths and does not mutate `.agents/`.
- `snapshot.py restore`: still renames an existing root `BOOTSTRAP.md` to `.done` after restoring history, so restoring an existing project does not rerun first-time bootstrap unless the backend writes a new root bootstrap.
- `import_archive.py`: still renames an existing root `BOOTSTRAP.md` to `.done` during import; the backend Open flow rewrites root `BOOTSTRAP.md` after import with project context.
- `package.py`: only treats `agent/BOOTSTRAP.md` as packable agent content; it does not drive Builder first-run reset.

## Tests

- `uv run --python 3.12 --with pytest --with pyyaml -m pytest agent-studio/.agents/skills/agent-studio/tests -q`
- `uv run --python 3.12 --with pytest --with pyyaml -m pytest agent-studio/.agents/skills/agent-studio/scripts/tests -q`
- `uv run --python 3.12 --with ruff -m ruff check agent-studio/.agents/skills/agent-studio/scripts/project_workspace.py agent-studio/.agents/skills/agent-studio/tests/test_project_workspace.py`
- `python -m py_compile agent-studio/.agents/skills/agent-studio/scripts/project_workspace.py`
- `git diff --check`


