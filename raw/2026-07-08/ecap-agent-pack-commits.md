# SerendipityOneInc/ecap-agent-pack — 2026-07-08

共 1 个 commit

## `3fb207e1` fix(agent-studio): declare PyYAML for validate script (#201)

- **作者**: rayrain-srp
- **日期**: 2026-07-08T12:02:40Z
- **SHA**: 3fb207e1529ccf6ce6da7a5a90dded3c8fec9de2

### 完整 Commit Message

```
fix(agent-studio): declare PyYAML for validate script (#201)

* fix(agent-studio): declare PyYAML for validate script

* chore(agent-studio): bump version to 2.2.4
```

### PR Description

## Summary

- Add PEP 723 script metadata to Agent Studio `validate.py` so `uv run --python 3.12` installs PyYAML before spec coverage imports `yaml`.
- Add a stdlib regression test that requires the validate entrypoint to declare PyYAML in its inline script dependencies.

## Root Cause

Agent Builder Pack Test preflight runs Agent Studio `validate.py` with `uv run --python 3.12`. The spec coverage path imports `_spec_patterns.py`, which imports `yaml`, but the entry script did not declare PyYAML as an inline dependency. In a fresh uv script environment this raises `ModuleNotFoundError: No module named 'yaml'`, preventing the Pack Test panel from opening.

## Linear

https://linear.app/srpone/issue/ECA-1186/agent-builder-pack-test-无法弹出preflight-validatepy-报-modulenotfounderror

## Validation

- `python3 -m unittest discover -s agent-studio/tests -p 'test_*.py' -v`
- `python3 .github/scripts/check_filenames.py < /tmp/eca-1186-pr-changed.txt`
- `python3 .github/scripts/agent_release.py validate-changed --root . --paths-file /tmp/eca-1186-pr-changed.txt`
- Dynamic temp Builder workspace: `uv run --python 3.12 .agents/skills/agent-studio/scripts/validate.py --skip-online-validation --pack-test-gate` reached `spec_coverage: pass` with no `ModuleNotFoundError`. The overall temp-workspace validation intentionally reported unrelated pack completeness failures because the temporary workspace only contained the minimum files needed to exercise spec coverage.


---
