---
title: "PPT Master Agent 正式发布 v2.0.7（原 SlideForge 更名）"
type: "Agent 上架/更新"
priority: "高"
date: "2026-05-27"
status: "待审核"
channels: ""
---

# PPT Master Agent 正式发布 v2.0.7（原 SlideForge 更名）

## 核心宣传点

PPT 制作 Agent 完成品牌升级，正式命名为 PPT Master，发布 v2.0.7 稳定版，支持输出 HTML/PDF/PPTX 多种格式和美化功能。

## 原始内容

**仓库**: SerendipityOneInc/ecap-agent-pack  
**SHA**: [34e7189b](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/34e7189ba5ee7f042d4f1286f1e2e584dc673a84)
**PR**: [#150](https://github.com/SerendipityOneInc/ecap-agent-pack/pull/150)  
**作者**: vincent-srp  
**日期**: 2026-05-27T08:40:03Z

**Commit Message:**

```
feat(pptx-master): apply 2.0.7-final build, rebrand SlideForge to PPT Master (#150)

Replace pptx-master pack contents with the finalized pptx_master-2.0.7-final build (21 files: output-html/pdf/pptx + ppt-beautify + onboarding skills, plus AGENTS/SOUL/IDENTITY/HEARTBEAT/BOOTSTRAP/routing/CHANGELOG/description). Version stays 2.0.7 (finalized re-build, not a bump).

Adopt the PPT Master display brand throughout (was SlideForge; 0 SlideForge refs remain). Preserve the deployment identity slug agentPack_id/name = pptx-master (hyphen) — the build shipped pptx_master (underscore), which would orphan the live OpenClaw deployment. Set agent-pack.yaml description to the English PPT Master bio (build shipped Chinese). Unify the two cosmetic pptx_master refs in tests/ to pptx-master.

Validation: test_pack.py 70/0, test_extra.py 36/0, validate_pdf_ratio.py --self-test passed.

Co-authored-by: vincent-srp <180138700+vincent-srp@users.noreply.github.com>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```


**PR Description:**

## Summary

Replaces the `pptx-master` pack with the finalized `pptx_master-2.0.7-final` build, adopting the new **PPT Master** display brand while preserving the deployment identity. Version stays **2.0.7** — this is the finalized re-build, not a version bump (current `main` was already 2.0.7).

## Changes

- **Content/code refresh** (~15 files): `output-html`, `output-pdf`, `output-pptx`, `ppt-beautify`, `onboarding` skills + docs (`AGENTS`/`SOUL`/`IDENTITY`/`HEARTBEAT`/`BOOTSTRAP`/`routing`/`CHANGELOG`).
- **Rebrand SlideForge → PPT Master** (display fields only): `display_name`, `name`, `bio`, `short_bio`, `author`, and all in-pack copy. 0 SlideForge references remain.
- **Identity slug preserved**: `agent-pack.yaml name` + `description.json agentPack_id` kept as `pptx-master` (hyphen). The build shipped `pptx_master` (underscore), which would orphan the live OpenClaw deployment, so it was patched back. Dir name unchanged.
- **Description**: `agent-pack.yaml description` set to the English PPT Master bio sentence (build shipped Chinese).
- **tests/**: unified the two cosmetic `pptx_master` refs (docstring + README) to `pptx-master`.

## Validation

- `tests/test_pack.py`: **70 pass / 0 fail**
- `tests/test_extra.py`: **36 pass / 0 fail**
- `output-pdf/scripts/validate_pdf_ratio.py --self-test`: **passed**
- `package.py` invariant `agentPack_id == manifest name` holds (both `pptx-master`).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
