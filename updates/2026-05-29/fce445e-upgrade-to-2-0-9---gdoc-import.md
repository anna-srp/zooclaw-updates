---
title: "upgrade to 2.0.9 — gdoc-import (Google Docs/Sheets/Slides, n"
type: "新功能上线"
priority: "高"
date: "2026-05-29"
status: "待审核"
channels: "Discord,changelog"
---

# upgrade to 2.0.9 — gdoc-import (Google Docs/Sheets/Slides, n

## 核心宣传点
新增 upgrade to 2.0.9 — gdoc-import (Google Docs/Sheets/Slides, n，让您可以完成更多任务

## 原始内容
feat(pptx-master): upgrade to 2.0.9 — gdoc-import (Google Docs/Sheets/Slides, no login) (#154)

Apply build/pptx-master-2.0.9.zip. Adds the gdoc-import skill (import public
Google Docs/Sheets/Slides via Google's export endpoints, no OAuth), version
bump 2.0.8 → 2.0.9, plus routing.yaml + description.json entries.

The build artifact's CHANGELOG had regressed to a v2.0.7 top (dropping v2.0.8,
no v2.0.9) and test_pack.py's docstring read 2.0.7; both corrected here so the
repo carries full release history and a proper v2.0.9 entry. Tests: 70/0 + 36/0.

Co-authored-by: vincent-srp <180138700+vincent-srp@users.noreply.github.com>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

---

**PR #154 Description**:
## Summary

Upgrades the `pptx-master` pack to **2.0.9** from `build/pptx-master-2.0.9.zip`.

### New feature — Google Import (`gdoc-import` skill)
- New skill `.agents/skills/gdoc-import/SKILL.md`: import public Google Docs / Sheets / Slides via Google's built-in export endpoints — no OAuth, no login. Auto-detects type from the URL, exports to the deck-optimal format, detects login-wall / permission failures (never fabricates), routes into narrative / data-viz / Path B template pipeline.
- `routing.yaml`: new `external_doc_import` section (detect regex, type→endpoint map, format options, multi-sheet handling, failure detection, red lines) + skill registry entry.
- `description.json`: "Google Import" feature + skill line.
- `agent-pack.yaml`: version `2.0.8 → 2.0.9`.
- Identity preserved: `name: pptx-master`, `display_name: PPT Master`, `agentPack_id: pptx-master`.

### Build-artifact fixes (surfaced by the diff check)
The zip's `CHANGELOG.md` had regressed to a v2.0.7 top — missing the v2.0.8 entry and lacking a v2.0.9 entry. Restored the exact **v2.0.8** entry and wrote a new **v2.0.9** entry. Also fixed `tests/test_pack.py` docstring `2.0.7 → 2.0.9`.

> ⚠️ The source zip still carries the stale CHANGELOG/docstring, so repo and zip are no longer byte-identical. Regenerate the artifact upstream so they reconverge.

## Test
- `python3 tests/test_pack.py` → **70 pass / 0 fail**
- `python3 tests/test_extra.py` → **36 pass / 0 fail**

🤖 Generated with [Claude Code](https://claude.com/claude-code)
