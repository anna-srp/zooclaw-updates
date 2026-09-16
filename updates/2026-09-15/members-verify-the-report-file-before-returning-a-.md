---
title: "feat(council): members verify the report file before returning a digest (#280)"
type: "新功能"
priority: "低"
date: "2026-09-15"
status: "待审核"
channels: ""
---

# feat(council): members verify the report file before returning a digest (#280)

## 核心宣传点

## 背景

staging cache-hit smoke [34997185557](https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/34997185557)（`/council … tier: economy`，编排者 terra）取证：gemini-3.1-flash-lite 成员 spawn 后 16 秒就以一段摘要 announce 完成，没有把报告写到 `$RUN/raw-reports/<encoded>.md`；编排者按协议 read 失败，用 `sessions_send` 催办后成员才写文件并二次 announce。编排者的处理是对的，但成员模板没有要求"先确认文件落盘再返回"。

## 改动

- `references/member-prompt.md`：最后一段拆成三步——先写完整报告到指定绝对路径；再读回核验（存在、非空、四个必需章节标题），失败就重写并再核验，文件不在磁盘上之前不结束、不只返回摘要；最后才返回摘要（长度限制与 never-paste-it-back 不变）。
- `SKILL.md` Stage 2：dispatch 时保留 write → verify → digest 顺序；收到 delivery 时若报告文件缺失或为空，用 `sessions_send` 让该成员按指定路径写文件并确认通过核验，文件通过核验前不记 done、不替成员把摘要写成文件。
- `tests/test_skill_md_contract.py`：两条契约测试钉住上述措辞。

不改 roster tier lineup（engine 侧 smoke 任务正改为 tier standard）、不改脚本、不改 frontmatter。

## 验证

- `uv run --with pytest --with jsonschema pytest council/tests -q`：376 passed（基线 374 + 新增 2）
- `python3 .github/scripts/lint_skills.py`：All skills passed（12 个既有 warning）

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## 原始内容

- 仓库：SerendipityOneInc/ecap-skills
- SHA: `c2ad030f12ef40bed6853bacaf0afc7bf6caadd9`
- PR: #280
- 作者：Chris@ZooClaw
- 日期：2026-09-15T17:51:15Z

### Commit Message

```
feat(council): members verify the report file before returning a digest (#280)

## 背景

staging cache-hit smoke
[34997185557](https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/34997185557)（`/council
… tier: economy`，编排者 terra）取证：gemini-3.1-flash-lite 成员 spawn 后 16
秒就以一段摘要 announce 完成，没有把报告写到 `$RUN/raw-reports/<encoded>.md`；编排者按协议 read
失败，用 `sessions_send` 催办后成员才写文件并二次
announce。编排者的处理是对的，但成员模板没有要求"先确认文件落盘再返回"。

## 改动

-
`references/member-prompt.md`：最后一段拆成三步——先写完整报告到指定绝对路径；再读回核验（存在、
```
