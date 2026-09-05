---
title: "新增飞书多维表格 Skill：Agent 能直接读你贴过来的 Bitable 链接"
type: "Skill 上架/更新"
priority: "中"
date: "2026-09-04"
status: "待审核"
channels: "Discord+changelog"
---

# 新增飞书多维表格 Skill：Agent 能直接读你贴过来的 Bitable 链接

## 核心宣传点

继上周飞书云文档、云盘、知识库之后，飞书多维表格（Bitable）也接进来了。新增 `feishu-bitable` 技能，对应一组原生的 `feishu_bitable_*` 工具，跑在 Engine v2 上，用的是渠道自带的飞书/Lark 应用身份——不用你另外配 App ID、贴 Token。

用法上就是把多维表格的链接丢给 Agent：`/base/` 和 `/wiki/` 两种地址、飞书和国际版 Lark 都支持，Agent 会先解析链接拿到表格元信息和数据表清单，再看字段定义，然后按分页游标把记录读出来（每页 1–500 条）。这一组工具都是单一职责的，没有那种一个工具塞十几种操作的 `action` 参数，Agent 判断该调哪个更不容易出错。多账号场景下会明确要求你指定用哪个飞书账号，数据量过大等错误也有专门的提示而不是含糊失败。

技能的元数据与 `feishu-doc` 对齐（同样要求飞书渠道已启用），并已注册进 v2 已发布技能清单。

## 原始内容

- 仓库: SerendipityOneInc/ecap-skills
- SHA: `002377fc11503d4a64211758cefcf6fd88c87013`
- PR: #276
- 作者: sharplee-srp
- 日期: 2026-09-04T07:30:52Z

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

```
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

```
