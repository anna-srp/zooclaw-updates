# SerendipityOneInc/ecap-agent-pack - 2026-05-25

共 2 条 commits

## 090da3a1 - fix(agent-studio): forbid memory-only onboarding config check in templates (#144)

**作者**: felix-srp  
**日期**: 2026-05-25T14:13:53Z  
**SHA**: 090da3a156af5608e009642f4d3bd128ee7781b9

**完整 Commit Message**:

```
fix(agent-studio): forbid memory-only onboarding config check in templates (#144)

* fix(agent-studio): forbid memory-only onboarding config check in templates

Scaffolded packs were instructed to "check" `data/config.json` with
hints like `ls data/config.json` and `ls data/config.json 2>/dev/null`,
but the wording never forbade the model from claiming the result from
memory. In production this led to an agent telling the user "我看了
一下，data/config.json 已经存在" without ever invoking a tool, then
having to apologize and restart onboarding mid-conversation — either
re-onboarding returning users or silently skipping new ones.

- BOOTSTRAP.md.tmpl Step 2: require an actual Bash `test -f ...` or
  Read call; explicitly name the hallucination and the two failure
  modes it causes.
- AGENTS.md.tmpl Step 5: same guardrail.
- agent-pack.yaml: bump 1.3.3 → 1.3.4.

Existing packs (e.g. video-duplicate) need re-scaffolding or a
hand-patch to inherit the guardrail; this commit only fixes the
template so newly generated packs are protected.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): propagate config-check guardrail to automation spec; trim templates

Code-review caught two follow-ups to the previous template fix:

1. references/automation.md §"Required sections" is the Stage 3a spec
   the Studio LLM reads when writing a new pack's AGENTS.md. It still
   said `ls data/config.json missing → trigger pack-onboarding`, so
   Studio would write the unguarded form into generated packs even
   with the template updated — the template fix would not actually
   reach end-user packs.

2. The template wording was ~30-40 tokens longer than necessary in
   both files. The bolded prohibition + the concrete command carry
   the guardrail; the quoted hallucination example and the
   failure-mode explainer were motivational, not load-bearing. Also
   replaced "Read errors with ENOENT" (Claude Code's Read tool
   surfaces a human-readable error, not a literal errno).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR Description**:

## Summary

- BOOTSTRAP.md.tmpl Step 2 and AGENTS.md.tmpl Step 5 previously hinted at \`ls data/config.json\` but never forbade the model from claiming the check result from memory. In production an agent did exactly that — said \"我看了一下，data/config.json 已经存在\" without invoking a tool, then apologized and restarted onboarding mid-conversation.
- Both templates now require an actual Bash \`test -f …\` or Read call and explicitly name the hallucination and the two failure modes (re-onboarding returning users / silently skipping new ones).
- agent-pack.yaml: 1.3.3 → 1.3.4.

Existing packs (e.g. video-duplicate) need re-scaffolding or a hand-patch to inherit the guardrail; this PR only fixes the template so newly generated packs are protected.

## Test plan

- [ ] Render a new pack via agent-studio and confirm the generated BOOTSTRAP.md / AGENTS.md contain the new guardrail wording.
- [ ] Spot-check that the new wording doesn't break existing pack-onboarding behavior on a returning user (config.json present).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 33602e93 - feat(pptx-master): update SlideForge to 2.0.7 (#143)

**作者**: vincent-srp  
**日期**: 2026-05-25T09:45:49Z  
**SHA**: 33602e9396c64ec34c9bce30ae1fa252c9f7ec60

**完整 Commit Message**:

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

---

