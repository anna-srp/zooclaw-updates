# ecap-agent-pack — commits 2026-07-01

共 2 个 commit


## fix(agent-studio): lock project workspace cleanup (#198)

- **SHA**: `117c4884a9cb0672ccf8995cc46f290d4931c31e`
- **作者**: kaka-srp <kaka@srp.one>
- **日期**: 2026-07-01T10:14:14Z
- **URL**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/117c4884a9cb0672ccf8995cc46f290d4931c31e
- **PR**: #198

### 完整 Commit Message

```
fix(agent-studio): lock project workspace cleanup (#198)
```

### PR Body

## Summary
- Add a shared Agent Studio workspace lock helper using `.agent-builder-projects/.workspace.lock`.
- Use the shared lock in `project_workspace.py` and `clean.py` so project activation and cleanup do not mutate the same live workspace concurrently.
- Retry transient `ENOTEMPTY` / `EBUSY` directory removals in `clean.py` while still surfacing persistent failures.
- Add tests for retry behavior and lock creation.

## Tests
- `python -m py_compile agent-studio/.agents/skills/agent-studio/scripts/_workspace_lock.py agent-studio/.agents/skills/agent-studio/scripts/clean.py agent-studio/.agents/skills/agent-studio/scripts/project_workspace.py`
- `python -m pytest agent-studio/.agents/skills/agent-studio/tests/test_clean.py agent-studio/.agents/skills/agent-studio/tests/test_project_workspace.py`

## Notes
- This PR only changes Agent Studio source files; no generated pack archive was rebuilt.



## fix(agent-studio): publish display name as pack name (#197)

- **SHA**: `11595538207eec20eb2a24f5af8c80ff3617a2af`
- **作者**: kaka-srp <kaka@srp.one>
- **日期**: 2026-07-01T09:50:25Z
- **URL**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/11595538207eec20eb2a24f5af8c80ff3617a2af
- **PR**: #197

### 完整 Commit Message

```
fix(agent-studio): publish display name as pack name (#197)
```

### PR Body

## Summary
- send agent-pack.yaml display_name as Pack Test pack_name from Agent Studio publish
- keep manifest name as stable display_id / archive manifest_name
- reject stale description.json agentPack_id and sync description name from display_name
- keep existing-source version-bump enforcement even when only display_name changes

## Tests
- uv run --python 3.12 -m pytest agent-studio/.agents/skills/agent-studio/scripts/tests/test_publish.py -q
- uv run --python 3.12 -m pytest agent-studio/.agents/skills/agent-studio/scripts/tests/test_connect_composio.py agent-studio/.agents/skills/agent-studio/scripts/tests/test_connectors.py agent-studio/.agents/skills/agent-studio/scripts/tests/test_connectors_helpers.py agent-studio/.agents/skills/agent-studio/scripts/tests/test_package_agent_md.py agent-studio/.agents/skills/agent-studio/scripts/tests/test_package_connectors.py agent-studio/.agents/skills/agent-studio/scripts/tests/test_publish.py agent-studio/.agents/skills/agent-studio/scripts/tests/test_validate_connectors.py -q

## Notes
- Full scripts test collection currently needs numpy for KB tests in this local environment.

