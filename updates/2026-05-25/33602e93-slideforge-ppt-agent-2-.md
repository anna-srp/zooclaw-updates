---
title: "SlideForge（PPT 生成 Agent）更新至 2.0.7"
type: "Agent 上架/更新"
priority: "中"
date: "2026-05-25"
status: "待审核"
channels: ""
---

# SlideForge（PPT 生成 Agent）更新至 2.0.7

## 核心宣传点

SlideForge PPT 生成 Agent 发布 2.0.7 版本，内部技能全面升级，生成效果更好

## 原始内容

**仓库**: SerendipityOneInc/ecap-agent-pack  
**Commit**: 33602e9396c64ec34c9bce30ae1fa252c9f7ec60  
**作者**: vincent-srp  
**日期**: 2026-05-25T09:45:49Z  

**Commit Message**:

```
feat(pptx-master): update SlideForge to 2.0.7 (#143)

Unpack build/slideforge-2.0.7-zooclawfixed-v5.zip over the pptx-master
pack (SlideForge), bumping 1.0.0 → 2.0.7. Same 16-skill set; changes are
within skills.

Highlights (full history in pptx-master/CHANGELOG.md, v2.0.0→v2.0.7):
- v2.0.0–2.0.2: prose SKILL.md → structured YAML lookup + thin wrappers +
  HTML template files; runnable validation.yaml; test suite (106 tests).
- v2.0.4: drop 68MB local font bundle (145 woff2) → ecap-skills/_fonts
  remote loading; package 72MB → 3.7MB.
- v2.0.5–2.0.6: cover visual-center rules + bbox guardrails + validator.
- v2.0.7: L1-PDF-RATIO blocking rule + validate_pdf_ratio.py.

Identity: agentPack_id and agent-pack.yaml name are "pptx-master" (the dir
name / deployed platform identity); description.json name + display_name
stay "SlideForge" (brand). badge=official, animal=Axolotl. Net vs main:
+51 / -146 / ~26 files (deletions = removed font bundle + heroicons-dict.md).

The only edit on top of the v5 zip: agent-pack.yaml `description` translated
zh→en (display metadata). All other files are verbatim from the zip; the
pack's intentional multilingual content (zh keyword matching, name_zh
bilingual fields, zh test samples, CJK examples) is preserved.

Verified: test_pack.py 70/0, test_extra.py 36/0, validate_pdf_ratio.py
--self-test pass, agent-pack.yaml/description.json/routing.yaml parse.

Co-authored-by: vincent-srp <180138700+vincent-srp@users.noreply.github.com>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR Description**:

Unpacks `build/slideforge-2.0.7-zooclawfixed-v5.zip` onto the `pptx-master` (SlideForge) pack, bumping `1.0.0 → 2.0.7`. The skill set is unchanged (still 16 skills); all changes are within the skills.

## Key changes (full history in `pptx-master/CHANGELOG.md`, v2.0.0 → v2.0.7)
- **v2.0.0–2.0.2**: prose `SKILL.md` → structured YAML lookup + thin wrappers + HTML template files; runnable `validation.yaml`; new test suite (106 tests).
- **v2.0.4**: removed the 68MB local font bundle (145 woff2) → `ecap-skills/_fonts` remote loading; package 72MB → 3.7MB.
- **v2.0.5–2.0.6**: cover visual-center rules + bbox guardrails + validator script.
- **v2.0.7**: new `L1-PDF-RATIO` blocking rule + `validate_pdf_ratio.py` (enforces PDF 16:9).

## Identity
- `agentPack_id` and `agent-pack.yaml` `name` are **`pptx-master`** (directory name / deployed platform identity); `description.json` `name` + `display_name` stay **SlideForge** (brand).
- `badge` = `official`, `animal` = `Axolotl`.
- Directory stays `pptx-master/`, consistent with the repo's dir-name == `agentPack_id` convention.

## Scope
- All changes confined to `pptx-master/`: **+51 / -146 / ~26** files. Deletions = 145 woff2 fonts + `heroicons-dict.md` (replaced by `heroicons.json`). No cruft (`__pycache__` / `.DS_Store` excluded).
- This PR contains **only** the SlideForge upgrade — none of the `feat/zoo-captain` branch changes are included (done in an isolated worktree off the latest `main`).

## Verification
- `tests/test_pack.py` → **70 / 0**
- `tests/test_extra.py` → **36 / 0**
- `validate_pdf_ratio.py --self-test` → pass
- `description.json` / `agent-pack.yaml` / `routing.yaml` all parse

🤖 Generated with [Claude Code](https://claude.com/claude-code)
