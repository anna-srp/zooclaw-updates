# SerendipityOneInc/ecap-agent-pack — 2026-06-24

共 3 个 commit

---

## fix(agent-studio): clean directory symlinks safely (#189)

- **SHA**: `7a4d998b1c40c4c6d3933a8542f6fb9939097db1`
- **作者**: kaka-srp
- **日期**: 2026-06-24T10:01:08Z
- **PR**: #189
- **链接**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/7a4d998b1c40c4c6d3933a8542f6fb9939097db1

### 完整 commit message

```
fix(agent-studio): clean directory symlinks safely (#189)

* fix(agent-studio): clean directory symlinks safely

* docs(agent-studio): clarify accept test before submit
```

### PR 描述

## Summary
- Fix `clean.py` so symlink entries are unlinked before normal directory handling; real directories still use `shutil.rmtree()`.
- Cover both reset paths that can hit directory symlinks: top-level `skills/` cleanup and `agent/` skeleton reset cleanup.
- Clarify the Builder prompt flow as `Package & Test` -> `Accept Test` -> `Submit`, so the first-run guidance does not imply Submit can happen directly after Pack Test.
- Bump the Agent Studio pack version to `2.0.1` so the hotfix can be published as a distinct package update.

## Why
Production hit `OSError: Cannot call rmtree on a symbolic link` when `clean.py` saw a symlink-to-directory such as `skills/browser-skill`. `Path.is_dir()` follows directory symlinks, but `shutil.rmtree()` refuses to remove the symlink itself. The safe behavior is to unlink symlinks and only recursively delete real directories.

The core Builder docs already gate Submit behind Accept Test, but `BOOTSTRAP.md` summarized the first-run workflow as Pack Test -> Submit. This PR aligns that prompt with the actual UI gate: creators test the temporary bot, click Accept Test when satisfied, and only then click Submit.

## Tests
- `python -m pytest tests/test_clean.py -q` - 2 passed
- `python -m pytest tests -q` from `agent-studio/.agents/skills/agent-studio` - 108 passed
- `python -m pytest tests -q` from `agent-studio/.agents/skills/agent-studio/scripts` - 129 passed
- `python3 .github/scripts/agent_release.py validate-changed --root . --paths-file <changed-files>` - validated `agent-studio` version `2.0.1`
- `git diff --check`


---

## refactor(agent-studio): align workflow with agent builder (#186)

- **SHA**: `e3c58e9670654629e35e16941b26e562e779e5f4`
- **作者**: kaka-srp
- **日期**: 2026-06-24T08:51:43Z
- **PR**: #186
- **链接**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/e3c58e9670654629e35e16941b26e562e779e5f4

### 完整 commit message

```
refactor(agent-studio): align workflow with agent builder (#186)

* feat(agent-studio): add pack test publish flow

* fix(agent-studio): clarify pack test publish prompt

* refactor(agent-studio): align workflow with agent builder

* refactor(agent-studio): remove legacy builder triggers

* chore(agent-studio): bump pack version to 2.0.0
```

### PR 描述

## Summary
- Reposition the shipped pack as the Agent Builder experience in user-facing identity, prompts, and workflow guidance.
- Bump the Agent Studio pack version to `2.0.0` for this Builder workflow change.
- Remove the old local install/share command skills and local submit/test guidance that are no longer part of the Builder flow.
- Harden `validate` / `package` behavior so validation only blocks on packable manifest-referenced skills, while stale unreferenced skill folders cannot mask packaged cross-reference issues.
- Keep the internal pack id, paths, release assets, and upload key as `agent-studio` for compatibility; `Agent Builder` is the product/display name.

## Why This Shape
- The large negative diff is mostly deleting legacy `agent-studio-install` and `agent-studio-share` code that was no longer declared by the pack manifest or supported by the current UI-owned flow.
- Leaving those legacy skills in-tree made validation/release behavior misleading: the package step ships manifest-referenced content, while old folders could still be scanned or maintained as if they were active entry points.
- This PR intentionally does not do a full `agent-studio` to `agent-builder` technical rename. Internal ids and artifact names stay stable to avoid breaking existing installs, staging upload routing, release asset conventions, and compatibility assumptions.
- The user-facing name is now Agent Builder because the workflow is guided agent-pack creation, not a general-purpose studio/IDE surface.

## Tests
- `python -m pytest tests` from `agent-studio/.agents/skills/agent-studio` - 106 passed
- `python -m pytest tests` from `agent-studio/.agents/skills/agent-studio/scripts` - 104 passed
- `git diff --check`
- PR checks after the `2.0.0` version bump: 8/8 passed

## Beta Release Validation
- Latest PR head: `28e2934`
- Created beta tag `v1.0.0-beta.6` at that branch head
- `Release Agent Zips` completed successfully, including `Upload agent-studio release`
- Published prerelease: https://github.com/SerendipityOneInc/ecap-agent-pack/releases/tag/v1.0.0-beta.6
- Agent Studio pack version in the staging package: `2.0.0` (`agent-studio-2.0.0.zip` and `agent-studio.zip`)


---

## ci: release agent studio pack from tags (#188)

- **SHA**: `c10b6b6ae391644b483ea0904b1d91af129c24c5`
- **作者**: bill-srp
- **日期**: 2026-06-24T07:13:45Z
- **PR**: #188
- **链接**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/c10b6b6ae391644b483ea0904b1d91af129c24c5

### 完整 commit message

```
ci: release agent studio pack from tags (#188)

* ci: release agent zips from release tags

* ci: notify lark for agent studio releases
```

### PR 描述

## Summary
- trigger agent zip releases from release tags instead of merges to main
- add Lark release notifications for Agent Studio production releases
- limit release notes changelog content to agent-studio/ changes

## Verification
- ruby YAML parse for .github/workflows/*.yml
- bash -n for release-notify-lark.yml run blocks

