# ecap-skills — commits 2026-06-09

## chore: stop publishing zooclaw-connectors skill (#213)

- **SHA**: `0a9fefe276d10a68f531a0d1fc43bb656d107f7c`
- **作者**: tim-srp
- **日期**: 2026-06-09T09:03:53Z
- **PR**: #213
- **URL**: https://github.com/SerendipityOneInc/ecap-skills/commit/0a9fefe276d10a68f531a0d1fc43bb656d107f7c

### 完整 commit message

```
chore: stop publishing zooclaw-connectors skill (#213)
```

### 完整 PR body

## Summary
- remove `zooclaw-connectors` from `PUBLISHED_SKILLS`
- leave the skill source directory in the repo, but exclude it from S3 extra-skills publishing

## Notes
- publish workflow stages only entries listed in `PUBLISHED_SKILLS` and syncs with `--delete`, so the next publish will remove this skill from the published extra-skills bundle.

## Verification
- `rg -n '^zooclaw-connectors$' PUBLISHED_SKILLS` returns no matches
- `git diff --check`
- `/tmp/ecap-skills-lint-venv/bin/python .github/scripts/lint_skills.py` (passes with existing warnings)

---

