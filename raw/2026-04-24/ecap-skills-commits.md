# ecap-skills commits — 2026-04-24 (UTC 2026-04-23)

共 4 条 commits

---

## 1. 49f33cec — chore(chameleon): clarify InputVideoSensitiveContentDetected fallback + copyright guidance (#180)

- **SHA**: 49f33cecb6f750c13be4bd22040a5d926a716b1d
- **作者**: david-srp
- **日期**: 2026-04-23T16:07:56Z
- **PR**: #180

### 完整 commit message

chore(chameleon): clarify InputVideoSensitiveContentDetected fallback + copyright guidance (#180)

Rewrite the two compliance bullets to spell out the actual flow: on
real-face rejection ZooClaw onboards the portrait and retries with
asset://, and a post-retry block means policy-sensitive copyrighted
material — steer users to switch portraits or pre-vetted safe sources.

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Body

（无 PR body 或未抓取）

---

## 2. d7dce6d3 — chore(devcontainer): bump openclaw image to 2026.4.2.12 + inject ecap/litellm env vars (#178)

- **SHA**: d7dce6d38a9a403fbcfa170b6114405aa4b57993
- **作者**: allenz-srp
- **日期**: 2026-04-23T01:11:19Z
- **PR**: #178

### 完整 commit message

chore(devcontainer): bump openclaw image to 2026.4.2.12 + inject ecap/litellm env vars (#178)

- openclaw-docker: 2026.3.13.38 → 2026.4.2.12 (matches gcp-foundation
  fastclaw rollout on dev/staging, 2026-04-22)
- Inject canonical env vars into the container so skills using
  ecap-proxy / LiteLLM work out-of-the-box: ECAP_PROXY_BASE_URL,
  USER_INTERNAL_TOKEN, LITELLM_API_BASE, LITELLM_API_KEY
- All vars use ${VAR:-} so host-unset stays empty (no compose warnings,
  no hard failures at startup)

Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>

### PR Body

（无 PR body 或未抓取）

---

## 3. 77f5798c — chore(web-designer): trim skill docs ~460 lines for runtime context efficiency (#169)

- **SHA**: 77f5798cb84d51c8f2104f924e19c3ecfb07cbb9
- **作者**: felix-srp
- **日期**: 2026-04-23T00:18:05Z
- **PR**: #169

### 完整 commit message

chore(web-designer): trim skill docs ~460 lines for runtime context efficiency (#169)

* chore(web-designer): simplify skill docs and scripts

Tighten runtime skill files for better context engineering in ZooClaw.
Removes prose redundancy in SKILL.md, references/*.md, and scripts/ while
preserving all CSS themes, component recipes, CLI commands, and "why"
comments. Net: -460 lines.

Key changes:
- SKILL.md: condense overview/tech-stack/workflow, keep quality gates
- design-system.md: remove §13 (duplicated SKILL.md anti-slop), inline
  per-theme "Best for" + font bullets, trim aesthetic-direction prose
- components.md: compress §2 ECharts gotcha and §7.11.1 reduced-motion
  walls of prose into structured bullets
- content.md: collapse headline examples, shorten §9 image-search
  pipeline, trim per-framework narration
- scripts: light comment-tightening only; no logic changes

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(web-designer): restore three workflow anchors in SKILL.md

Reviewer flagged that the simplification dropped three procedural details
that change skill behavior.

---

## 4. b17a718d — pdf: trim runtime docs (~50%) + schema/cache fixes from audit (#166)

- **SHA**: b17a718d77f744a565faf335394288e258b98943
- **作者**: felix-srp
- **日期**: 2026-04-23T00:16:40Z
- **PR**: #166

### 完整 commit message

pdf: trim runtime docs (~50%) + schema/cache fixes from audit (#166)

* chore(pdf): trim runtime .md files for context efficiency

Token-efficiency pass on skill docs. Total: 1919 → 947 lines (~50% reduction).

* chore(pdf): safe script cleanups — dead code + hot-path hoists

* fix(pdf): schema accuracy + footguns surfaced during trim audit

* fix(pdf): review findings — fill_annotate schema, fonts cache purity

* fix(pdf): round 2 review — empty fields no-op + partial-hint warn + forms.md Format B

* fix(pdf): round 3 — partial coord-hint warn covers Format B too

* fix(pdf): left-align FreeText annotations by default

* feat(pdf): add --dpi flag to ocr subcommand

Default was pdf2image's 200 DPI, which struggles on handwritten or
small-font Chinese text. New default 300 DPI; at 400 DPI with tessdata_best
the same image OCRs correctly (e.g. "胡 宁" vs "#8" at 200 DPI).

- ocr: new --dpi (default 300). Bump to 400-600 for handwritten/small-font CJK.
- SKILL.md: mention the flag + tessdata_best substantially beats tessdata_fast on CJK accuracy.

* docs(pdf): mention --dpi + tessdata_best hint in ocr usage
