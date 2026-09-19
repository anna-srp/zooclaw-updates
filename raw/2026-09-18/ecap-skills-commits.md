# SerendipityOneInc/ecap-skills — commits 2026-09-18

## fix(designer): add concise image IP restrictions (#286)

- **SHA**: `d0eb9299a82c5065f9642f4124f59348014b5d51`
- **作者**: tim-srp
- **日期**: 2026-09-18T10:11:09Z
- **PR**: #286

### Commit Message

```
fix(designer): add concise image IP restrictions (#286)

## Summary
Add two short sentences to Designer's existing Rules section: refuse
recognizable third-party character, mascot, logo, and branded-setting
reproductions, including reference-image edits and lookalikes; do not
bypass via renamed subjects or alternate tools/models; offer an original
alternative.

Only designer/SKILL.md changes. This is model guidance, not a
server-side moderation gate. No global system prompt or script changes,
and no deployment.

Companion engine tool guidance:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1517

## Validation
Skill linter passed (12 existing warnings in other skills). Reviewed the
rule against existing generation/editing instructions.
```

### PR Body

## Summary
Add two short sentences to Designer's existing Rules section: refuse recognizable third-party character, mascot, logo, and branded-setting reproductions, including reference-image edits and lookalikes; do not bypass via renamed subjects or alternate tools/models; offer an original alternative.

Only designer/SKILL.md changes. This is model guidance, not a server-side moderation gate. No global system prompt or script changes, and no deployment.

Companion engine tool guidance: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1517

## Validation
Skill linter passed (12 existing warnings in other skills). Reviewed the rule against existing generation/editing instructions.


---
