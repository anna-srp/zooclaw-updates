# SerendipityOneInc/ecap-skills — commits 2026-10-08

## chore(skills): remove retired zooclaw-connectors skill (#292)

- **SHA**: `2767df8b076c3716eab8c6ddd1c0d3ed5fc3e2bf`
- **作者**: tim-srp
- **日期**: 2026-10-08T09:47:37Z
- **PR**: #292

### Commit Message

```
chore(skills): remove retired zooclaw-connectors skill (#292)

## Summary
Remove the retired Nango-backed `zooclaw-connectors` skill and its CLI.
It was removed from publication in #213 and is absent from the current
V2 allowlist, but its source still advertised the legacy integrations
workflow.

Remove stale references in knowledge-base authentication documentation
and review guidance. The knowledge-base implementation and the 22-skill
publication allowlist are unchanged. This PR does not uninstall existing
copies or change proxy endpoints, environment variables, Composio, or
specialist-manager.

## Validation
- Skill linter passed (11 existing warnings in unrelated skills).
- Test-selection suite: 3 tests passed.
- V2 registry dry-run: 22 skills, no validation failures.
- No remaining zooclaw-connectors or legacy integrations endpoint
references found in the working tree.
- git diff --check passed.
```

### PR Body

## Summary
Remove the retired Nango-backed `zooclaw-connectors` skill and its CLI. It was removed from publication in #213 and is absent from the current V2 allowlist, but its source still advertised the legacy integrations workflow.

Remove stale references in knowledge-base authentication documentation and review guidance. The knowledge-base implementation and the 22-skill publication allowlist are unchanged. This PR does not uninstall existing copies or change proxy endpoints, environment variables, Composio, or specialist-manager.

## Validation
- Skill linter passed (11 existing warnings in unrelated skills).
- Test-selection suite: 3 tests passed.
- V2 registry dry-run: 22 skills, no validation failures.
- No remaining zooclaw-connectors or legacy integrations endpoint references found in the working tree.
- git diff --check passed.


---
