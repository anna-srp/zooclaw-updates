# ecap-agent-pack — 2026-07-06 commits

共 1 个 commits

---

## fix(agent-studio): localize builder UI action prompts (#199)

- **SHA**: `fef77df55f05f35a7a8fdc86a8bb58e8ba3db34a`
- **作者**: kaka-srp
- **日期**: 2026-07-06T11:11:46Z
- **PR**: #199

### Commit Message

```
fix(agent-studio): localize builder UI action prompts (#199)
```

### PR Body

## Summary

- Update Agent Studio bootstrap and root skill prompts so Builder UI action names follow the creator language: Chinese UI names for Chinese conversations, English names otherwise.
- Align packaging and delivery guidance for localized Package & Test, Package & Test Again, Accept Test, Submit, Share, and Open references.
- Pair with Agent Builder runtime prompt update: https://github.com/SerendipityOneInc/ecap-workspace/pull/2749

## Tests

- `git diff --cached --check`


