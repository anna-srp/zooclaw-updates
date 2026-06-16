# SerendipityOneInc/ecap-agent-pack — commits 2026-06-15

共 1 条 commits

---

## feat(agent-studio): add pack test publish flow (#177)
- **sha**: `d5215131011c4511b0019ca744b6cbd37333216d`
- **作者**: kaka-srp (kaka-srp)
- **日期**: 2026-06-15T07:42:05Z
- **URL**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/d5215131011c4511b0019ca744b6cbd37333216d
- **PR**: #177

### 完整 commit message

```
feat(agent-studio): add pack test publish flow (#177)

* feat(agent-studio): add pack test publish flow

* fix(agent-studio): clarify pack test publish prompt
```

### PR body

## Summary
- add Agent Studio `publish.py` flow for Pack Test start/status/submit
- upload candidate archives directly to the R2 access worker before creating Pack Test runs
- update Agent Studio prompts/docs for Accept-gated Pack Store submission and repeated test uploads
- add publish workflow unit tests

## Tests
- `python -m unittest discover -s .agents/skills/agent-studio/scripts/tests`
- `python -m py_compile .agents/skills/agent-studio/scripts/publish.py .agents/skills/agent-studio/scripts/tests/test_publish.py`

