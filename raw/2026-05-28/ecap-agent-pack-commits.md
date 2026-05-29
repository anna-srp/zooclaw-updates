# ecap-agent-pack — 2026-05-28
共 3 条 commits

---
## [b377d37] feat(pptx-master): upgrade to 2.0.8 — 1080p canvas + sidebar-only wireframe (#152)
- **作者**: vincent-srp
- **日期**: 2026-05-28T07:34:37Z
- **PR**: #152

### Commit Message
```
feat(pptx-master): upgrade to 2.0.8 — 1080p canvas + sidebar-only wireframe (#152)

Apply build/pptx-master-2.0.8.zip on top of the deployed 2.0.7 (PPT Master).

- Canvas upgrade 1280x720 -> 1920x1080 across all pipelines: new bundled
  marp theme-1080p.css with mandatory --theme-set workflow; output-html
  coordinate system / template_mirror / thumbnail clone+scale / fidelity
  page dimensions all updated to 1080p.
- Wireframe simplified to sidebar-only (patch_wireframe.py v0.6.17 ->
  v0.6.18): removed the .pm-actions floating PDF/PPTX toolbar; audit_7b11a.py
  A16 now verifies .pm-sidebar instead of the action buttons.
- Bump version 2.0.7 -> 2.0.8; add v2.0.8 CHANGELOG entry; sync test_pack.py
  harness docstring to 2.0.8. Identity slug unchanged (pptx-master).

Verified: tests/test_pack.py 70/0, tests/test_extra.py 36/0,
validate_pdf_ratio.py --self-test pass.

Co-authored-by: vincent-srp <180138700+vincent-srp@users.noreply.github.com>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Upgrades the **PPT Master** pack (`pptx-master/`) from the deployed **2.0.7** to **2.0.8**, applying `build/pptx-master-2.0.8.zip` on top of `main`. Identity slug (`pptx-master` / `agentPack_id`) and PPT Master branding are unchanged — this PR is the pure 2.0.7→2.0.8 functional delta (14 files).

### What changed
- **Canvas upgrade 1280×720 → 1920×1080 (16:9)** across all pipelines:
  - Marp: new bundled `theme-1080p.css` (`/* @theme custom-1080p */`); `SKILL.md` documents the mandatory `--theme-set artifacts/theme-1080p.css` render workflow (Marp fixes the SVG viewBox from the theme at build time, so inline `<style>` overrides clip).
  - output-html: `pipeline.yaml` coordinate system @144dpi + `template_mirror` px; `patch_wireframe.py` thumbnail clone/scale (`148/1280`→`148/1920`); `fidelity-rules.yaml` page dims; `export-advanced.yaml`, `html-standards.md`, `output-html/SKILL.md`, `slides-shell.html`, `t10-team-update-5p.md`.
- **Wireframe → sidebar-only** (`patch_wireframe.py` v0.6.17 → v0.6.18): removed the `.pm-actions` floating PDF/PPTX toolbar; `audit_7b11a.py` A16 now verifies `.pm-sidebar` instead of the action buttons.
- Version bump `2.0.7 → 2.0.8`; new `v2.0.8` CHANGELOG entry; `test_pack.py` harness docstring synced to 2.0.8.

## Test plan
- [x] `python3 tests/test_pack.py` → 70 pass / 0 fail
- [x] `python3 tests/test_extra.py` → 36 pass / 0 fail
- [x] `python3 .agents/skills/output-pdf/scripts/validate_pdf_ratio.py --self-test` → pass
- [x] Identity verified: `name: pptx-master`, `agentPack_id: pptx-master` (hyphen), `display_name: PPT Master`, `avatar_url: avatar.png`
- [x] Version consistent across `agent-pack.yaml`, CHANGELOG, `test_pack.py`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [ac04d1b] fix(agent-studio): stage tmp share archives in public artifacts (#151)
- **作者**: sharplee-srp
- **日期**: 2026-05-28T06:22:21Z
- **PR**: #151

### Commit Message
```
fix(agent-studio): stage tmp share archives in public artifacts (#151)

* fix(agent-studio): stage tmp share archives publicly

* test(agent-studio): cover tmp share agent flow
```

### PR Body
## Summary
- detect Agent Studio source packs under workspace tmp directories and stage shared archives in the parent workspace public artifacts/shares directory
- build share URLs from the public workspace root while keeping delivery state on the source pack
- keep install preview/restage URL projection aligned with the share behavior
- document the tmp-pack staging behavior and add regression tests

## Tests
- uv run --python 3.12 --with pytest -m pytest agent-studio/.agents/skills/agent-studio-share/tests/test_run_share_tmp_artifacts.py
- python3 -m py_compile agent-studio/.agents/skills/agent-studio-share/scripts/run_share.py agent-studio/.agents/skills/agent-studio-install/scripts/install.py

---
## [27acb1f] fix(agent-studio): generate installable artifact share urls (#149)
- **作者**: sharplee-srp
- **日期**: 2026-05-28T04:03:22Z
- **PR**: #149

### Commit Message
```
fix(agent-studio): generate installable artifact share urls (#149)
```

### PR Body
## Summary
- Use zooclaw-artifact-url when staging Agent Studio shares so generated URLs include bot and agent path segments.
- Add runtime URL projection for check-only previews via PUBLIC_URL_PREFIX and BOT_ID.
- Keep local fallback behavior for non-runtime development.

## Tests
- python3 -m unittest discover -s ecap-agent-pack/agent-studio/.agents/tests -v
- verified in ecap-skills devcontainer: zooclaw-artifact-url and build_artifact_url returned https://artifacts.claw.yesy.live/<bot_id>/main/artifacts/shares/qiliang-0.1.0.tar.gz
