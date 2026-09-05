# SerendipityOneInc/ecap-skills — commits 2026-09-04

## feat(feishu): add managed Bitable skill (#276)

- **SHA**: `002377fc11503d4a64211758cefcf6fd88c87013`
- **作者**: sharplee-srp
- **日期**: 2026-09-04T07:30:52Z
- **PR**: #276

### Commit Message

```
feat(feishu): add managed Bitable skill (#276)

## Summary

- Add `feishu-bitable/SKILL.md` for the native `feishu_bitable_*` tools
(Engine v2, channel-backed Feishu/Lark app identity).
- Register it in `PUBLISHED_SKILLS_V2`.

The Skill mirrors `feishu-doc`'s frontmatter (`requires.config:
feishu.enabled` plus the OpenClaw metadata block) and covers: the eight
tools are single-operation with **no `action` field**; URL input goes
through `get_meta` first (`/base/` and `/wiki/`, Feishu and Lark);
`list_fields` before reading/writing records; `list_records` pagination
via `has_more` / `page_token` (page_size 1–500); field value shapes per
type; account selection and `feishu_account_required`; error handling
incl. `feishu_payload_too_large` and `feishu_tool_outcome_unknown` (read
back, never replay); explicit "no delete tools / no Sheet cell API / no
user OAuth"; and a note that the write tools land after the read tools
(use whatever subset is on the surface).

Scopes named in the Skill (`bitable:app:readonly` / `bitable:app`) are
the plan's candidates and still need staging confirmation in ACS.

## Related work

- Plan and Engine contract 0.2.0: SerendipityOneInc/zooclaw-engine#1112
- ACS executor: SerendipityOneInc/agent-channel-service#107 (draft)

## Validation

- `lint_skills.py`: all skills passed; the 12 warnings are pre-existing
in other skills, zero new.
- `sync-v2-registry.mjs --validate`: `PUBLISHED_SKILLS_V2 validated (22
skills)`; `--dry-run`: `feishu-bitable` present, `wouldFail: []`.

## Release order

Merging publishes the Skill to the v2 registry. No Engine config
references it until Engine PR-2 adds it to `FEISHU_BASE_SKILLS`, so
existing Agents are unaffected (plan §8 step 3).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_018haS3ohvB5XUtBJLD8fk2T

---------

Co-authored-by: Claude Fable 5.1 <noreply@anthropic.com>
```

### PR Body

## Summary

- Add `feishu-bitable/SKILL.md` for the native `feishu_bitable_*` tools (Engine v2, channel-backed Feishu/Lark app identity).
- Register it in `PUBLISHED_SKILLS_V2`.

The Skill mirrors `feishu-doc`'s frontmatter (`requires.config: feishu.enabled` plus the OpenClaw metadata block) and covers: the eight tools are single-operation with **no `action` field**; URL input goes through `get_meta` first (`/base/` and `/wiki/`, Feishu and Lark); `list_fields` before reading/writing records; `list_records` pagination via `has_more` / `page_token` (page_size 1–500); field value shapes per type; account selection and `feishu_account_required`; error handling incl. `feishu_payload_too_large` and `feishu_tool_outcome_unknown` (read back, never replay); explicit "no delete tools / no Sheet cell API / no user OAuth"; and a note that the write tools land after the read tools (use whatever subset is on the surface).

Scopes named in the Skill (`bitable:app:readonly` / `bitable:app`) are the plan's candidates and still need staging confirmation in ACS.

## Related work

- Plan and Engine contract 0.2.0: SerendipityOneInc/zooclaw-engine#1112
- ACS executor: SerendipityOneInc/agent-channel-service#107 (draft)

## Validation

- `lint_skills.py`: all skills passed; the 12 warnings are pre-existing in other skills, zero new.
- `sync-v2-registry.mjs --validate`: `PUBLISHED_SKILLS_V2 validated (22 skills)`; `--dry-run`: `feishu-bitable` present, `wouldFail: []`.

## Release order

Merging publishes the Skill to the v2 registry. No Engine config references it until Engine PR-2 adds it to `FEISHU_BASE_SKILLS`, so existing Agents are unaffected (plan §8 step 3).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_018haS3ohvB5XUtBJLD8fk2T


---
