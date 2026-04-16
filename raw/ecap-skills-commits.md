# ecap-skills — 近7天原始 commits

> 抓取时间：2026-04-16 08:27 UTC
> 仓库：https://github.com/SerendipityOneInc/ecap-skills
> 共 22 条 commits

## 2026-04-16

### [5839242](https://github.com/SerendipityOneInc/ecap-skills/commit/583924205bb20f7464bed43c2fb5ae9a3aa1a41a) feat: add VS Code devcontainer with openclaw-docker image (#148)

**作者**: allenz-srp  
**SHA**: `583924205bb20f7464bed43c2fb5ae9a3aa1a41a`

```
* feat: add VS Code devcontainer with openclaw-docker image

Use openclaw-docker as the dev environment so skill development
matches the production runtime. Mounts host ~/.claude, ~/.claude.json
and ~/.config into the container for Claude Code and GCP auth.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* use 2026.3.13.38 image version

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

## 2026-04-15

### [fce7444](https://github.com/SerendipityOneInc/ecap-skills/commit/fce74446bf0f48e2a7cb148916c1ffb35b3457f5) fix(web-designer): move build/artifacts out of read-only skill directory (#152)

**作者**: felix-srp  
**SHA**: `fce74446bf0f48e2a7cb148916c1ffb35b3457f5`

```
* fix(web-designer): move build/artifacts out of read-only skill directory

On zooclaw the skill directory is mounted read-only. Redirect .build/
to /tmp/openclaw/web-designer/.build/ (transient, matches other skills)
and artifacts/ to $HOME/artifacts/ (workspace root, HTTP-accessible).

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(web-designer): use pwd instead of $HOME for artifacts path

$HOME may not equal the workspace directory. Use $(pwd) in bundle.sh
so the agent controls the output location by cd-ing to the workspace
before invoking the script. Update SKILL.md to use {workspace} notation.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(web-designer): remove invalid {workspace} from bash code block

{workspace} is an agent-level concept, not a shell variable. Rewrite
the build pipeline example as plain bash with a comment explaining
the cwd requirement.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(web-designer): fix Phase 4 bundle invocation instruction

Remove invalid cd+relative-path combo. The agent's default cwd is
already the workspace; just state the cwd requirement.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(web-designer): bundle.sh takes explicit output-dir argument

Avoids pwd/cwd ambiguity — the agent passes {workspace}/artifacts/<name>
directly. Trim SKILL.md for token efficiency.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(web-designer): fix stale bundle hint + remove dead SKILL_DIR

Update init.sh "Next steps" to include required <output-dir> arg.
Remove unused SKILL_DIR variable from bundle.sh.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [68449c4](https://github.com/SerendipityOneInc/ecap-skills/commit/68449c40771f8a5585b43d2e919ef1c8dfba792a) Remove skill-crafting from published skills whitelist (#151)

**作者**: tim-srp  
**SHA**: `68449c40771f8a5585b43d2e919ef1c8dfba792a`

```
Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```

### [88c50d4](https://github.com/SerendipityOneInc/ecap-skills/commit/88c50d4ca601ae1599f7e68370875e119dc42fc3) Add web-designer and skill-crafting to published skills whitelist (#150)

**作者**: tim-srp  
**SHA**: `88c50d4ca601ae1599f7e68370875e119dc42fc3`

```
Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```

## 2026-04-14

### [ca2440d](https://github.com/SerendipityOneInc/ecap-skills/commit/ca2440d6fc65d141b807489bdb6cc34074a9c613) fix(pdf): Noto font discovery + chart/table bug fixes (#146)

**作者**: felix-srp  
**SHA**: `ca2440d6fc65d141b807489bdb6cc34074a9c613`

```
* fix(pdf): simplify Noto font discovery via setup-noto.sh

- setup-noto.sh: one-shot Noto installer (Sans/Serif/Mono/CJK SC),
  OTF->TTF conversion via otf2ttf, installs to
  $ECAP_FONTS_DIR/{truetype,opentype}/noto (default /usr/share/fonts)
- fonts.py: resolve font dir via $ECAP_FONTS_DIR prefix, drop legacy
  /extra-skills and relative-path fallbacks; truetype/opentype subdirs
- make.sh: add Noto font check in cmd_check; auto-install via
  setup-noto.sh in cmd_fix
- .env.example: document $ECAP_FONTS_DIR override for macOS dev
- SKILL.md: drop redundant Environment section (covered by make.sh check)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

* fix(pdf): chart data alias, repeatRows, KeepTogether for small tables

- chart datasets: accept "data" as alias for "values" (bar/line/pie) so
  LLMs using the intuitive key don't silently produce empty charts
- _add_table: repeatRows=1 so headers repeat across page breaks; wrap
  tables with <=10 rows in KeepTogether to keep table+caption together

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

* fix(pdf): address PR #146 review — surface silent failures

- make.sh: stop swallowing stderr on the Noto discovery probe so real
  errors (uv missing, import failure) stay visible to the user.
- setup-noto.sh: partial-install now fails hard — missing archive files
  and failed OTF→TTF conversions return non-zero instead of silently
  installing a subset; otf2ttf exit code is captured and surfaced
  instead of being discarded with `|| true`.
- render_body.py: chart dataset with neither `values` nor `data` key now
  logs a warning with chart/series name instead of silently rendering an
  empty series.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

---------

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```

### [0d1bafe](https://github.com/SerendipityOneInc/ecap-skills/commit/0d1bafeefaed9b18f2a9c17e86a7b8668bc92a7e) chore(web-designer): read fonts from $ECAP_FONTS_DIR/woff/ (#147)

**作者**: felix-srp  
**SHA**: `0d1bafeefaed9b18f2a9c17e86a7b8668bc92a7e`

```
* chore(web-designer): read web fonts from ECAP_FONTS_DIR/woff

Stop looking for .woff2 files under shared/fonts/web/. init.sh now
copies from ${ECAP_FONTS_DIR:-~/.local/share/fonts}/woff/{cjk,latin,fallback}/,
aligning with the standard fontconfig layout used by pdf/scripts/fonts.py
(truetype/, opentype/, woff/). Lets macOS local dev and Linux base images
share one env var for all font formats.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

* chore(web-designer): default ECAP_FONTS_DIR to /usr/local/share/fonts + add .env.example

- Flip init.sh default from ~/.local/share/fonts (macOS dev only) to
  /usr/local/share/fonts — the standard user-font prefix for Linux /
  Homebrew and what the zooclaw base image uses. Local Mac dev sets
  ECAP_FONTS_DIR explicitly when needed.
- Add web-designer/.env.example documenting the optional ECAP_FONTS_DIR.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

* chore(web-designer): use /usr/share/fonts as ECAP_FONTS_DIR default

Matches pdf/scripts/fonts.py's default and the standard fontconfig
prefix on zooclaw/Linux. Replaces the previous /usr/local/share/fonts
default so every skill resolves to the same system path.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

* docs(web-designer): clarify ECAP_FONTS_DIR is shell-exported, fix $HOME example

init.sh does not source .env; the variable must be exported in the
shell. Switch `~` to `$HOME` in the example for consistency and because
dotenv loaders don't tilde-expand.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

---------

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```

### [b115e1f](https://github.com/SerendipityOneInc/ecap-skills/commit/b115e1f3aea7fa819c92ff80489a461fb7ba5ed3) fix(chameleon): route local-file uploads through ecap-proxy /storage/r2/upload (#145)

**作者**: kaka-srp  
**SHA**: `b115e1f3aea7fa819c92ff80489a461fb7ba5ed3`

```
Before this commit the auto-upload path in chameleon_generate.py shelled out to
skills/cloudflare-assets/scripts/cf-assets.sh — a script and skill that do not
exist anywhere in the repo. david-srp/#143 then flipped --auto-upload-r2 default
to True, which detonated the dead code path for every run with a local reference
file.

Replace the shell-out with a direct HTTP upload to ecap-proxy-service's existing
/storage/r2/upload endpoint. Uses the same X-Litellm-Api-Base / X-Litellm-Api-Key
headers chameleon already sends for generation, via the proxy's new dual-auth
path (ecap-proxy-service PR #36). No new env vars.

- scripts/_upload.py (new): shared upload helper used by both scripts
- scripts/chameleon_generate.py: remove dead cf-assets.sh path, inline upload,
  add temp-file cleanup so normalize_*_for_byteplus outputs don't leak to /tmp
- scripts/asset_register.py: --local-file-path without --url now auto-uploads
  instead of erroring out, unifying the two scripts' local-file mental model
- SKILL.md / .env.example: drop the USER_INTERNAL_TOKEN placeholder (the route
  now accepts the LiteLLM headers we already have)

Depends on ecap-proxy-service#36 being deployed before this is rolled out.
```

### [34c762c](https://github.com/SerendipityOneInc/ecap-skills/commit/34c762c35fef2a38a36b6e86b28000f39e05e87c) feat(chameleon): add ideation guidance and rights reminder (#143)

**作者**: david-srp  
**SHA**: `34c762c35fef2a38a36b6e86b28000f39e05e87c`

```
* feat(chameleon): add ideation guidance and rights reminder

* feat(chameleon): enforce no-subtitles prompt default

* chore(chameleon): default local refs to R2 upload
```

## 2026-04-13

### [4ae6244](https://github.com/SerendipityOneInc/ecap-skills/commit/4ae62446aea8ff78bf54e6dd56cee2fcdbb596d4) feat(chameleon): seedance video skill via ecap-proxy with billing (ECA-465) (#140)

**作者**: kaka-srp  
**SHA**: `4ae62446aea8ff78bf54e6dd56cee2fcdbb596d4`

```
* feat(chameleon): seedance video skill via ecap-proxy with billing (ECA-465)

- Adds the chameleon skill (BytePlus/Volcengine Seedance video generation)
- Routes generation through ecap-proxy /video/seedance (server-side ARK_API_KEY,
  token-based billing)
- Routes asset management through ecap-proxy /byteplus/assets (server-side
  SigV4 credentials; CHAMELEON_ASSET_GROUP_ID auto-injected per environment)
- Skill only needs LITELLM_API_BASE / LITELLM_API_KEY / ECAP_PROXY_BASE_URL
- Default-on download to /tmp/openclaw/chameleon to align with video-generator;
  --no-download for opt-out, --archive for full request/result/CSV archive flow

* chore(chameleon): publish to S3 sync list
```

## 2026-04-10

### [070dce3](https://github.com/SerendipityOneInc/ecap-skills/commit/070dce3c68be34075421efcab04a2dac636077aa) fix(web-designer): respect prefers-reduced-motion in Presentation + InViewChart (#139)

**作者**: felix-srp  
**SHA**: `070dce3c68be34075421efcab04a2dac636077aa`

```
A subagent building a 13-slide deck via the skill surfaced three
pre-existing bugs in the Presentation and InViewChart recipes that only
manifest under rAF throttling — i.e. background tabs, headless Chrome,
MCP-driven visual verification, and OS reduced-motion users:

1. `AnimatePresence mode="wait"` + spring variants leave slides stuck
   mid-translate (opacity 0, transformX ~34%) because the spring never
   settles when rAF is throttled.
2. Per-element `motion.div initial={{ opacity: 0, y: N }} animate={{
   opacity: 1 }}` stays at `initial` state forever for the same reason.
3. ECharts `animationDuration: 1400-1800` series entrance animation
   freezes mid-draw, leaving only axes visible.

All three are framer-motion/ECharts rAF-dependent entrance animations
that the skill had no mitigation for. The CSS template already has
`@media (prefers-reduced-motion: reduce)` for CSS-level animations, but
neither framer nor ECharts is a CSS animation — both are inline-style
updates driven by JS rAF callbacks.

## Fix

Three layers of `prefers-reduced-motion` support so the 3 bugs are
covered end-to-end:

- **CSS** (`templates/index.css` — already in place from PR #138 era)
- **Framer-motion**: §7.11 Presentation recipe now imports `MotionConfig`
  and wraps its return in `<MotionConfig reducedMotion="user">`. This is
  framer v12's documented way to honor the OS / DevTools-emulated
  `prefers-reduced-motion: reduce` preference and propagates to both
  `AnimatePresence` transitions and per-element `motion.div`
  `initial→animate` variants (verified via context7 docs and framer
  source). Under reduced-motion framer snaps to the final state in one
  frame instead of driving the spring integration via rAF.
- **ECharts**: §2.7 InViewChart now reads
  `matchMedia('(prefers-reduced-motion: reduce)').matches` at init time
  and, if matched, spreads `animation: false` into the option before
  `setOption`. Charts render their final state in a single frame under
  reduced-motion while normal users still see the smooth entrance.

## Docs updates

- `references/components.md` §2.7 InViewChart recipe — add the matchMedia
  check with an explanation comment; no SSR guard (effect only runs
  client-side after `isInView`).
- `references/components.md` §7.11 Presentation recipe — import and wrap
  in `<MotionConfig reducedMotion="user">`, with a comment block above
  the return explaining why.
- `references/components.md` §7.11.1 Sizing — new bullet requiring
  visual verification to emulate `prefers-reduced-motion: reduce` via
  Chrome DevTools Rendering or CDP `Emulation.setEmulatedMedia`,
  explaining what breaks without it and where the mitigation lives.
- `SKILL.md` Motion quality gate — tighten from "`prefers-reduced-motion`
  respected" (vague) to enumerate all 3 layers with the specific
  mechanism at each.
- `SKILL.md` "Slides require a visual pass" paragraph — add sentence
  requiring reduced-motion emulation during verification.

## Review

Reviewed pre-commit by `pr-review-toolkit:code-reviewer`. Round 1 found:
(a) JSX indentation inconsistency on the `MotionConfig` wrapper, (b)
cargo-culted `typeof window !== 'undefined'` SSR guard in `InViewChart`
that's dead code in a Vite SPA, (c) slightly imprecise wording about "the
media query being set" in the §7.11.1 bullet. All 3 fixed before commit.

Context7 verification confirmed `reducedMotion="user" | "always" | "never"`
is the correct framer-motion v12 API, propagates to `AnimatePresence`
children, and that `"user"` honors the OS/emulated preference (vs
`"always"` which would force-disable for users who don't want it).

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [9848f43](https://github.com/SerendipityOneInc/ecap-skills/commit/9848f43ab9d8c637d1aec977a5e99a606c61bdc3) fix(web-designer): harden CJK line-breaking, slide sizing, optimize-image.py (#138)

**作者**: felix-srp  
**SHA**: `9848f43ab9d8c637d1aec977a5e99a606c61bdc3`

```
* fix(web-designer): harden CJK line-breaking, slide sizing, optimize-image.py

Real-usage learnings from building a 13-slide CJK deck + bugs caught by
the review loop on sibling PR #135 (pdf image acquisition).

## Template bug — CJK line breaking

`templates/index.css` used `word-break: break-all` on `[lang^="zh"]`,
which overrides the browser's UAX #14 line-breaker. Effects observed
in a real Chinese deck:

  - Latin words split mid-character: `Anthr│opic`
  - CJK closing punctuation orphaned: `供应链风│险"`

Fix: `word-break: normal` + `overflow-wrap: break-word`. Browser
default (`line-break: auto`) handles kinsoku shori correctly.

## Slide sizing guidance — references/components.md §7.11.1 (new)

The Presentation component had no guidance for fitting content inside
a 1440x900 viewport. Repeated overflow + unreadable body text bugs in
v1 of the Anthropic deck led to:

  - Body copy ≥14px floor (no `text-[10px]/[11px]` for slide body)
  - `html { font-size: 17px }` base bump recommendation
  - Canonical `flex flex-col h-full` + `flex-1 min-h-0` layout skeleton
  - Warning not to pair `variant="statement"` with a dense grid
  - New SKILL.md quality gates: CJK line breaks + slide fit/readability
  - "Slides require a visual pass" — screenshot every slide before
    declaring done; source-only review misses overflow + hierarchy bugs

## scripts/optimize-image.py — port fixes from pdf PR #135

The pdf skill's near-identical Pillow helper was reviewed in 6 rounds
on PR #135. Three of those findings applied here too:

  - rsvg temp file leaked fd + disk on every exit path
    (`tempfile.mkstemp(...)[1]` with zero cleanup). Fix: switch to
    `NamedTemporaryFile(delete=False)` + try/finally.
  - Small-viewBox SVG logos rasterized at their tiny intrinsic pixel
    size when no --resize was given. Fix: default rasterization width
    to 1600px for the no-resize case.
  - Script violated ecap-skills CLAUDE.md §3 (stdout must be JSON).
    Fix: emit `{output, width, height, format, bytes}` envelope on
    stdout; human log stays on stderr.
  - `Image.open()` crashes on corrupted input now return a clean
    error + exit 1 instead of a stack trace.

Not ported from pdf PR #135: --min-short-side print floor, WebP
output rejection, and the Playwright cover-image absolute-path fix —
all pdf-specific and inappropriate for web output.

## Lighter touches

  - `content.md`: 1-line 2-column balance rule for slide layouts
  - `SKILL.md`: 2 quality gates + visual-pass requirement

Reviewed in 2 rounds by pr-review-toolkit:code-reviewer. Ready to ship.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(web-designer): generalize pie+legend rule into §2.11 chart sizing

The previous fix for "pie chart arc bleeds into custom HTML legend" in
PR #126 (74ea2f9) added a "Layout with custom side legend" block under
§2.3 PieDonutChart. The fix was correct in practice but over-specified
in documentation: it framed the rule as (a) pie-chart-specific, (b)
legend-specific, (c) bound to a magic 360px width, and (d) "common in
report dashboards."

The actual principle is broader: ECharts measures container width at
init() time and draws to that. Any chart sharing a row with non-chart
content in a content-driven grid/flex cell has unpredictable visual
width, which affects bar/line/radar/gauge too, not just pies.

Changes:

- Delete the pie-specific "Layout with custom side legend" block from
  §2.3; replace with a one-line pointer to §2.11.
- Add §2.11 "Chart sizing in flex/grid layouts" with the general rule,
  symptoms it prevents (pie overlap, bar stretching, responsive drift),
  and the pie+legend code as ONE concrete example of the general rule
  rather than THE rule.
- Explicit note that any deterministic width works (280px, 400px, 45%,
  minmax) — the point is deterministic vs content-driven, not the
  specific number.

Same underlying guidance, broader applicability, one canonical home.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [f2ad487](https://github.com/SerendipityOneInc/ecap-skills/commit/f2ad4878b4354c893c48ccb8f3c56ec9bba0bd00) feat(pdf): image acquisition via designer + websearch skills (#135)

**作者**: felix-srp  
**SHA**: `f2ad4878b4354c893c48ccb8f3c56ec9bba0bd00`

```
* feat(pdf): add optimize-image.py helper for print-ready images

Adapted from web-designer/scripts/optimize-image.py with print-tuned
defaults: PNG/JPEG output only (no WebP, for PDF viewer compatibility),
JPEG quality 92, and --min-short-side 1200 to reject low-res sources
that would look pixelated at 300 DPI. Accepts SVG inputs via
rsvg-convert. Emits a JSON envelope on stdout, progress logs on stderr.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* docs(pdf): add image acquisition guidance via designer + websearch

Adds references/images.md covering when to reach for images, source
selection (designer vs websearch vs logo search), prompt ingredients,
print preset table, the websearch download pipeline, placement
conventions, and attribution.

Surfaces the decision rule in SKILL.md with a condensed doc-type matrix:
magazine/darkroom/poster recommend cover images; portfolio/editorial
encourage optional figures; report/proposal/general use figures only
when narrative demands; resume/academic/minimal/terminal stay image-
free (typography only). Also adds designer/websearch as soft skill
deps.

Extends design.md with the print quality floor (1200px short side for
figures, 2000px for covers) and a pointer to references/images.md.

No render-pipeline changes.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pdf): clean up rsvg temp file on all exit paths

tempfile.mkstemp was leaking the file descriptor (discarded via [1])
and the file itself was never deleted on any path — success or error.
Switch to NamedTemporaryFile(delete=False) so the fd is closed, and
wrap the post-rasterization body in try/finally so the temp file is
unlinked whether optimize succeeds or fails. Inline rsvg error paths
unlink before returning since they exit before entering the finally.

Found by feature-dev:code-reviewer.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pdf): honor EXIF orientation and rasterize SVG at 2400px default

Two P2 issues found by codex review:

1. JPEGs from phones and stock-photo sites often encode rotation in
   EXIF instead of pixel data. The helper measured/resized/saved
   without baking orientation, so those inputs were written sideways
   once EXIF was dropped on save. Fix: call ImageOps.exif_transpose
   right after Image.open.

2. SVG sources rasterized at rsvg-convert's default dimensions (which
   follow the viewBox) could be tiny (e.g. 200x200 for logos). The
   subsequent --min-short-side 1200 check then rejected them as
   low-res even though vectors are resolution-independent. Fix:
   default rsvg rasterization width to 2400px when no --resize is
   given, and skip the min-short-side check for SVG sources since
   they are not low-res in any meaningful sense.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pdf): enforce --min-short-side on post-resize image, not pre-resize

Round-2 codex review caught that my round-1 fix still had a gap: for
extreme-aspect SVGs or any source with a small explicit --resize, the
Pillow thumbnail downscale runs AFTER the short-side check, so cases
like a tall SVG rasterized to 800x3200 then thumbnailed to 200x800
would pass the gate at 800 (the rsvg output) and silently emit a
200-pixel short side.

Move the short-side check to run AFTER Image.thumbnail so it reflects
what actually lands in the PDF. This also catches a previously-missed
case for raster sources: a 2000x600 input resized down still fails
cleanly. The separate source_was_svg flag is no longer needed since
the check now has uniform semantics for all sources.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* docs(pdf): fix cover-image absolute-path requirement and poster preset

Two issues found by codex review round 3:

1. The cover-image example passed a relative path ("images/cover.jpg")
   but the cover is rendered by Playwright from a temp-dir HTML file,
   so relative paths resolve against the temp dir and silently fail
   to load — the cover renders without the image and no error is
   reported. Verified: relative produces a 23KB PDF with no cover
   image embedded, while "$PWD/images/..." produces the expected
   83KB PDF with the 61KB cover correctly embedded. Updated
   references/images.md and SKILL.md to require absolute paths (or
   file:// URLs) with an explanation.

2. The cover-poster preset advertised 1620x2880, but the document
   also says full-bleed covers need a short side of at least 2000px.
   Following the published preset would either fail the min-short-
   side gate or produce a cover contradicting the stated quality
   rule. Bumped the poster preset to 2160x3840 (same 9:16 aspect,
   satisfies the 2000px floor).

Figure/image block paths are unaffected — reportlab resolves them
from cwd, so both relative and absolute paths work for figures.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* docs(pdf): align optimize-image docstring with pdf skill uv-run convention

The script's docstring was copied verbatim from web-designer, which
uses `uv run --with pillow scripts/foo.py` (no python3). The pdf
skill consistently uses `uv run --with X python3 scripts/...` in all
13 existing script invocations (fill_inspect, pdf_tools, etc.).
Update the docstring and the Pillow-missing hint so there's a single
consistent form across the pdf skill.

No behavior change — uv run handles both forms. This is a docs-only
consistency fix.

Codex round 4 flagged "script lacks +x so direct CLI invocation
fails" — false positive: the pdf skill has zero .py scripts with +x
(all 13 are 0644), and no pdf doc invokes a script directly via
shebang. The convention is always `uv run --with deps python3 ...`.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* docs(pdf): bump cover-magazine preset to 3000x2000 to satisfy cover floor

Codex review round 5 caught that the cover-magazine preset
(2400x1600) fails the stated cover short-side floor of 2000px —
following the preset literally, `--resize 2400x1600 --min-short-side
2000` exits nonzero because the short side is 1600. Bump the preset
to 3000x2000 (same 3:2 aspect ratio) so all three cover presets
satisfy the floor when given aspect-matching sources:

  cover-magazine: 3000x2000 (3:2)   short side 2000 ✓
  cover-darkroom: 2000x2500 (4:5)   short side 2000 ✓
  cover-poster:   2160x3840 (9:16)  short side 2160 ✓

Update the designer invocation example to match. Verified against
the new presets with aspect-matching synthetic sources.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* docs(pdf): fix cover preset sizing + add image content verification

Two follow-up fixes from actually using the skill to render a Chinese
business report with images:

1. Cover preset sizing was massively over-specified. The spec said
   "full-bleed covers need 2000px short side" and set cover-magazine
   to 3000x2000 / cover-poster to 2160x3840. But cover.py actually
   renders cover_image as a small thumbnail on all three supporting
   patterns:

     magazine: max-width:340px max-height:220px
     darkroom: max-width:340px max-height:220px (grayscale 20%)
     poster:   width:260px height:340px (grayscale 100%)

   These are not full-bleed heroes — they are decorative thumbnails.
   A 1200x800 source (~3× the render size) is plenty for crisp print.
   Downgrade the cover floor from 2000 to 800 px short side, rewrite
   the preset table with realistic targets, and update the designer
   invocation example accordingly. Also fix design.md's inline note.

2. The spec told agents to pick images by intended use (websearch for
   real entities, designer for atmospherics) but said nothing about
   VERIFYING the downloaded content actually matches what the agent
   wanted. In practice, when a query includes a brand name like
   "Anthropic Claude AI", the top websearch results are dominated by
   the brand's own OG / logo / press-release card images, NOT
   editorial photos. Two separate runs of this exact flow both ended
   up embedding two logo-cards instead of real photos.

   Add a new §2 subsection "Verify content before using — don't
   trust dimensions alone" with a one-liner Pillow spot-check, a
   list of warning signs (flat corner pixels, 1:1/2:1 aspect with
   small central high-contrast region, suspicious filenames like
   "og", "logo", "brandmark"), and query refinement hints.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [beafbc6](https://github.com/SerendipityOneInc/ecap-skills/commit/beafbc62f0402a847b5dbf1666701500141b9ccf) feat(pptx): add image sourcing via designer + websearch (#134)

**作者**: felix-srp  
**SHA**: `beafbc62f0402a847b5dbf1666701500141b9ccf`

```
* feat(pptx): add image sourcing via designer + websearch skills

Adds the ability for pptx to fetch slide images from two sources:
- AI generation through the `designer` sibling skill (Gemini/GPT/Grok
  image models via `image_generation_cli.py`)
- Web image search through the `websearch` sibling skill (Serper images
  endpoint with license filters)

The integration mirrors web-designer's pattern (no new wrapper skill,
no extra navigation hop) so the chain stays at one level: `pptx ->
designer + websearch`. Each consumer keeps its own copy of the recipe
documentation; image-sourcing duplication is accepted as the price of
runtime token cheapness, with a sync marker for drift detection.

Changes:
- references/images.md (NEW, 405 lines): decision tree (gen vs search),
  preset → slide-type mapping (Cover/Section Divider/Mixed Media/Image
  Showcase), prompt-engineering recipes, full search→download→optimize
  pipeline, PptxGenJS placement contract, quality gates. Adapted from
  web-designer/references/content.md §8-9 with PPTX-specific bits:
  always download to disk first (PptxGenJS URL fetch has no defenses),
  text-over-image overlay shape pattern, slide-canvas sizing math.
- scripts/optimize-image.py (NEW): copied verbatim from web-designer
  (latest version with the SVG/rsvg-convert handling, palette-mode
  PNG transparency preservation, and RGBA→JPEG composite-on-white
  fixes from codex review).
- SKILL.md: bumps version 1.0 → 1.1, adds requires.skills
  ["designer","websearch"], requires.bins += "rsvg-convert", env vars
  LITELLM_API_BASE/KEY/ECAP_PROXY_BASE_URL (only required for image
  workflows), references images.md from the table, adds a Step 4b
  "Source Images" before slide JS generation, adds System Requirements
  install hints for librsvg.
- references/slide-types.md: each image-using slide type (Cover,
  Section Divider full-bleed, Mixed Media, Image Showcase) gets a
  default preset + placement coordinates pointing at images.md.
- references/pptxgenjs-images-icons.md: top-of-file pointer to
  images.md for sourcing (the file remains the addImage API reference).
- references/pitfalls-qa.md: placeholder URL grep added to QA process
  (catches stock placeholders like placehold.co, picsum.photos, etc).
- references/editing.md + SKILL.md + slide-types.md + pitfalls-qa.md:
  convert pre-existing python invocations in shell snippets to
  `uv run --with <deps> ...` (markitdown[pptx], Pillow, defusedxml,
  lxml). Python source files (docstrings, runtime usage messages)
  are deliberately untouched per the call-site-only convention.
- .env.example: documents the new env vars as image-sourcing-only.

Verified end-to-end:
- pptx/SKILL.md frontmatter parses cleanly (yaml.safe_load)
- optimize-image.py runs under uv: PNG → WebP and SVG → WebP
  (via rsvg-convert) both produce valid output
- All converted shell snippets (`uv run --with "markitdown[pptx]"
  markitdown ...`, `uv run --with Pillow,defusedxml ...
  thumbnail.py`, etc.) launch cleanly under uv

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pptx): address review round 1 findings

- images.md: drop the `wide` 32:9 preset row — PPTX canvas is always
  16:9 (10"×5.625"), there is no widescreen slide layout in this skill,
  and a 32:9 image placed on a 16:9 slide either wastes resolution
  (cover crop) or letterboxes (contain). Replaced with prose telling
  the model not to source 21:9 / 32:9 images.
- pitfalls-qa.md: add `unsplash\.com/photos` to the placeholder URL
  grep — it was in images.md §6 but missing from the primary QA doc,
  so a deck with a raw Unsplash URL would slip past the QA gate and
  fail at PptxGenJS render time.
- images.md §6: document the file-existence check's known limitation —
  it only catches `path:`-sourced images, not `data:` base64 inlined
  ones (icons via react-icons → sharp → base64 are intentionally
  exempt; sourced photos always use path:).
- SKILL.md frontmatter: drop the `env` array. The chained `designer`
  and `websearch` skills declare their own env requirements, so
  declaring them on pptx duplicates the contract and wrongly implies
  pptx requires those vars even for text-only decks. This matches
  the web-designer pattern (which only declares `requires.skills`
  and lets the chained skills own their envs). .env.example still
  documents the vars for users who want image sourcing.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pptx): address review round 2 findings (regressions from round 1 fixes)

- images.md line 15: replace dead link reference "[SKILL.md](../SKILL.md)
  prerequisites" with the actual env var requirements inlined plus a
  link to .env.example. SKILL.md never had a Prerequisites section;
  this link was a leftover from an early draft and the round-1 env
  removal made the gap more obvious.
- images.md line 120: the CLI aspect-ratio list was contradicting line
  65's "do not source 21:9 / 32:9" prohibition by listing 21:9 and
  several other PPTX-incompatible ratios with no caveat. Now lists
  only the four PPTX-valid ratios as recommended (1:1, 4:3, 3:4, 16:9)
  with each tied to its slide-type use case, and explicitly marks the
  rest as "do not use in this skill".

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pptx): port optimize-image.py SVG intrinsic-size fix from web-designer

Sync optimize-image.py from web-designer/scripts/optimize-image.py at
HEAD of skill/web-designer-v2 (commit d543c94). Picks up the codex
review round 10 fix for PR #126:

When --resize is not passed, don't pass `-w 1920` to rsvg-convert.
Previously a 50x50 logo SVG would be silently upscaled to 1920x1920
producing an unnecessarily large WebP. The fix lets rsvg-convert use
the SVG's intrinsic size when no resize is requested. This matters
for pptx because logo sourcing in images.md §4 often deals with small
brand SVGs from Wikimedia that should stay at their native size.

Verified end-to-end: 50x50 SVG → 50x50 WebP without --resize, and
→ 100x100 WebP with --resize 100x100.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pptx): address codex review findings on requires gating + QA snippet clarity

Two fixes from `codex review` against origin/main:

1. Remove `rsvg-convert` from `requires.bins`. Verified by reading
   openclaw `src/shared/requirements.ts:155-178`: `requires.bins` is a
   hard eligibility gate (any missing bin makes the skill ineligible).
   Marking rsvg-convert as required would make the entire pptx skill
   unavailable on pods without librsvg installed, even though text-only
   decks and PNG/JPG-only image workflows never invoke it. Moved into a
   new "Optional" subsection of System Requirements with install hints
   and a note that optimize-image.py prints an actionable error if it
   hits an SVG without rsvg-convert available.

   Note: `requires.skills: ["designer", "websearch"]` is kept. Unlike
   bins, the runtime Requirements interface does not include `skills`
   (only bins/anyBins/env/config/os), so `requires.skills` is metadata
   for documentation/discovery only — not a hard gate. Same precedent
   in web-designer/SKILL.md.

2. Replace the embedded `node -e "..."` form of the file-existence
   check in images.md §6 with a `node <<'NODE'` single-quoted heredoc.
   The old form needed `\$` to escape the bash double-quote layer
   before node saw a valid `$` end-of-string anchor, which trips up
   readers (and reviewers — codex misread this as a broken regex even
   though it works correctly when actually executed). The heredoc form
   passes the JS to node verbatim with no shell escaping, so the
   regex reads as `^slide-\d+\.js$` without ambiguity.

Verified end-to-end: heredoc form correctly catches a missing-image
reference in a synthetic test case.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pptx): honor EXIF orientation in optimize-image.py

Phone photos and many stock-image sources tag rotation in EXIF
metadata rather than rotating the actual pixel buffer. Pillow does
not apply EXIF orientation on Image.open(), so a portrait JPEG
with orientation=6 would previously save sideways into the WebP —
showing up as a sideways slide image in any deck sourced via
images.md §4 (web search → download → optimize).

Fix: import ImageOps and call ImageOps.exif_transpose(im) right
after Image.open(), before any mode conversion or resize. This
applies the rotation to the pixel buffer and strips the orientation
tag from the output, matching the standard "store upright" behavior.

Verified end-to-end:
- Source: 400x200 landscape JPEG with EXIF orientation=6
- Output: 200x400 portrait WebP with no orientation tag (None)
- Regression: PNG and SVG inputs still work unchanged

NOTE: web-designer/scripts/optimize-image.py has the identical bug
(this script is a verbatim copy from there). The same fix should
land upstream so the next sync stays clean. Found by codex review
round 11 of PR #134.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pptx): drop skills from requires; document chain in prose

Codex review keeps flagging requires.skills: ["designer", "websearch"]
because the field name claims a hard requirement while the rest of
the patch explicitly says image sourcing is optional. The previous
defense (openclaw runtime ignores requires.skills since it's not in
the Requirements interface, only bins/anyBins/env/config/os) is true
but doesn't satisfy semantic readability — anyone reading the
frontmatter naturally interprets "requires" as "required".

Fix: remove skills from requires entirely. The chain is already
documented in prose at SKILL.md:60 (Reference Files table) and
SKILL.md:101 (Step 4 outline), and now explicitly in a new "Optional
sibling skills (image sourcing only)" subsection at the bottom of
System Requirements with the env var requirements spelled out.

This makes the frontmatter semantically honest (only truly-required
deps are in `requires`) and resolves a recurring review finding.

Note: web-designer/SKILL.md still declares
`requires.skills: ["designer", "websearch"]` for the same reason
(metadata-as-documentation). It will hit the same review finding
when next reviewed and should probably be cleaned up the same way.
For now, pptx is the more semantically clean version.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* chore(pptx): remove .env.example; env requirements live in chained skills

.env.example files are repo cruft — they're not consumed at runtime
(openclaw's setup wizard reads metadata.openclaw.requires.env +
primaryEnv from frontmatter, not .env.example), and any consumer
copy of a chained skill's env vars rots over time.

For pptx specifically, after dropping `env` and `skills` from
`requires` in earlier review rounds, .env.example was just shadowing
designer/SKILL.md and websearch/SKILL.md anyway. Remove it and point
the docs at the chained skills directly.

- Delete pptx/.env.example
- Update pptx/SKILL.md "Optional sibling skills" subsection: drop the
  link to .env.example, say env vars live in the chained skills' own
  SKILL.md files
- Update pptx/references/images.md §1: drop the link to .env.example,
  point to ../designer/SKILL.md and ../websearch/SKILL.md instead

CI is not affected: lint_skills.py:check_env_example only `warn`s
(non-fatal) on the new state, and the warning is itself imprecise
(triggers on os.environ.copy() in soffice.py for subprocess
pass-through, not real user-config consumption).

CLAUDE.md §5 still says ".env.example must be in each skill root" —
that text is now outdated and should be removed in a separate pass.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* Revert "chore(pptx): remove .env.example; env requirements live in chained skills"

This reverts commit 2cbe4c6de36e18ca9960bd51e63bd89c2edef8b9.

* chore(pptx): stop duplicating chained skills' env var names

The previous prose listed `LITELLM_API_BASE`, `LITELLM_API_KEY`, and
`ECAP_PROXY_BASE_URL` in pptx/.env.example, pptx/SKILL.md, and
pptx/references/images.md as part of the image-sourcing chain. Those
vars belong to the `designer` and `websearch` sibling skills, not to
pptx — pptx never reads them, never validates them, and shouldn't
shadow their contract. When a chained skill adds, removes, or renames
a var, the consumer's copy rots silently.

Fix: name the chained skills (`designer`, `websearch`) and what they
do, but don't enumerate their env vars. Point readers at
`../designer/SKILL.md` and `../websearch/SKILL.md` for the actual
contract.

- pptx/.env.example: drop the LITELLM_* and ECAP_PROXY_BASE_URL
  example lines that were shadowing designer/websearch. Keep only
  the truly-pptx-owned optional ECAP_PROXY_BASE_URL for R2 file
  delivery (pptx delivers the final .pptx to end users; that path
  is owned by pptx itself, not a chained skill).
- pptx/SKILL.md "Optional sibling skills" section: drop the
  parenthetical env var lists; say "each chained skill owns and
  documents its own env vars in its own SKILL.md".
- pptx/references/images.md §1: same — point to ../designer/SKILL.md
  and ../websearch/SKILL.md instead of listing the var names inline.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* chore(pptx): drop redundant chained-skill explanations; match web-designer pattern

In zooclaw deployment, sibling skills (designer, websearch) and their
bin deps (librsvg2-bin) are pre-installed. The previous prose:

- Optional sibling skills (image sourcing only) subsection in SKILL.md
- Optional system binaries (image sourcing only) subsection in SKILL.md
- Multi-paragraph chain explanation at top of references/images.md §1
- Verbose .env.example preamble

...were all dead weight. The model already knows what designer and
websearch do from their own SKILL.md, so re-explaining them is token
waste. The "might not be installed" rationale doesn't apply when the
deployment target always has them.

web-designer is the reference pattern: declare the bin deps in
requires.bins, write ONE sentence in Overview ("Delegates image
generation to the designer skill ... during Phase X"), and let the
recipes carry the actual CLI invocations. Match it.

- pptx/SKILL.md: add `rsvg-convert` back to requires.bins; collapse
  the two "Optional ..." subsections back into a single one-line
  System line listing all required system bins.
- pptx/references/images.md: drop the chain-explanation paragraph
  at the top of §1; the recipes in §3 and §4 already show the
  designer/websearch CLI invocations directly.
- pptx/.env.example: trim the multi-line preamble; keep only the
  optional R2 delivery line that pptx actually owns.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* chore(pptx): remove unused R2 delivery vars from .env.example

pptx never delivers files via ecap-proxy R2 directly — file delivery
is owned by zooclaw, not pptx itself. The optional ECAP_PROXY_BASE_URL
and ECAP_PROXY_API_KEY lines were carried over from an older version
and have never been read by any pptx script.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* chore(pptx): remove .env.example — pptx has no env vars to document

After trimming the unused R2 delivery lines, pptx/.env.example was
just a single comment saying "no env vars required". A one-line
template that documents nothing is dead weight. CLAUDE.md §5
mandates .env.example for skills that have env vars; pptx has none,
so the file shouldn't exist.

If pptx ever gains a real env var of its own (not one belonging to
a chained sibling skill), .env.example should be re-added at that
point with the actual var documented.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* docs(pptx): three skill-doc lessons from anthropic-report dogfood test

Built a real Chinese-language deck from a 227-line markdown source as
an end-to-end test of the new image-sourcing capability. Hit four bugs
during QA; three are generic teachable lessons that should live in the
skill itself, not in a one-off fix. Adding them now so the next user
doesn't relearn them.

1. pptxgenjs-cjk.md — "Hazard: stat callouts with a CJK unit suffix"

   The "use CJK font for mixed content" rule already existed, but a model
   writing big numeric callouts like `$300 亿` naturally reaches for
   `fontFace: "Arial"` because the value is "mostly a number". When Arial
   meets a CJK char, the substitute font has different metrics, and any
   hand-positioned adjacent textbox (e.g. a separate `亿` element) will
   collide or leave gaps. Documented with the WRONG/CORRECT before/after
   from the actual slide-06 bug.

2. pptxgenjs-cjk.md — "Hazard: writing CJK strings in JS source files"

   Writing literal `"` inside a `"..."` JS string for Chinese quoted
   phrases (e.g. `"国防部"供应链风险"案"`) breaks the parser silently.
   Documents four safe options (Chinese 「」, U+201C/D escapes, \" escape,
   single-quoted outer string) and recommends 「」 as the typographically
   correct choice.

3. pitfalls-pptxgenjs.md — "Stat-card grids: size for the LARGEST value"

   Generic layout rule: when generating N equal-width cards from a list
   of values, the cell width must fit the longest entry, not the first.
   Includes a quick-estimate rule for Latin+CJK width budgets.

The fourth bug (TOC section title too long for the 2-column cell) was
situational, not generic — skipped.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* chore(pptx): tighten dogfood lessons from b5a4f70

Reviewing the previous commit honestly: ~58 lines added across two
files for what amounts to ~2 reusable rules. Trimming to just the
parts that earn their keep.

- pptxgenjs-cjk.md: collapse the verbose "Hazard: stat callouts"
  subsection into a single sentence appended to the existing "Mixed
  CJK + Latin Text" section. The base rule ("use CJK font for mixed
  content") is already there; this just calls out that it applies
  to numeric stats with a CJK unit suffix, which is the failure mode
  I missed during the dogfood test.

- pptxgenjs-cjk.md: collapse the verbose "Hazard: writing CJK strings
  in JS source files" subsection into one short paragraph in the same
  section. The strongest argument is typographic ("use 「」 in Chinese
  content") with parser safety as a side benefit; the WRONG/CORRECT
  matrix and the four escape options were noise.

- pitfalls-pptxgenjs.md: drop the entire "Stat-card grids" section.
  "Size cells for the largest content" is layout common sense, the
  failure mode was narrow, and 18 lines of width-budget arithmetic
  doesn't earn its keep in a pitfalls doc.

Net: -56 / +2 lines. Same skill knowledge, no bloat.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pptx): port temp-file leak fix in optimize-image.py from PR #135

Picked up from PR #135 (skill/pdf-images, codex review round 1
finding by claude reviewer): the SVG-rasterization branch in
optimize-image.py created a temp PNG via tempfile.mkstemp() but
never closed the returned file descriptor and never deleted the
file. Both leaks survived every exit path (success, rsvg
FileNotFoundError, rsvg CalledProcessError), accumulating one
orphan fd + one orphan PNG in $TMPDIR per SVG processed.

Fix matches the PDF skill's resolution:
- Replace tempfile.mkstemp() with tempfile.NamedTemporaryFile(
  suffix=".png", delete=False) inside a `with` block — closes the
  fd cleanly on context exit while keeping the file on disk for
  rsvg-convert to write to.
- Wrap the Pillow processing in try/finally so the temp file is
  unlinked on success.
- Add explicit svg_temp.unlink(missing_ok=True) to both rsvg
  exception handlers (FileNotFoundError, CalledProcessError) so
  the early-return paths don't leak either.

Verified end-to-end: tmp .png file count stays at 0 in $TMPDIR
across success and failure runs (both rsvg-not-installed and
rsvg-input-invalid paths exercised).

NOTE: web-designer/scripts/optimize-image.py at HEAD of
skill/web-designer-v2 has the IDENTICAL bug (this script is a
verbatim copy from there). Same fix should land upstream so the
next sync stays clean. Worth filing as a separate one-liner PR
against web-designer.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pptx): make optimize-image.py SVG cleanup truly exhaustive

Round 4 review (feature-dev:code-reviewer P1, conf 88) flagged that
the previous fix in 930222f had a misleading comment AND a real edge
case: the rsvg `subprocess.run` call lived OUTSIDE the outer try/finally
block, so any exception not caught by the explicit FileNotFoundError /
CalledProcessError handlers (e.g. PermissionError, OSError, KeyboardInterrupt
mid-fork) would propagate out and leak svg_temp.

Fix: hoist `svg_temp = None` above the outer try and pull the entire
SVG handling block INSIDE the try. The `finally` now genuinely covers
every exit path:

- Success with PNG/JPEG input: svg_temp is None, finally is a no-op.
- Success with SVG input: finally unlinks the rasterized temp.
- rsvg-convert not installed: except → return 1 → finally unlinks.
- rsvg-convert input error: except → return 1 → finally unlinks.
- Unexpected subprocess exception: propagates → finally still unlinks.
- Pillow open/save exception: propagates → finally still unlinks.

Removed the explicit `svg_temp.unlink()` calls from the two `except`
handlers — they're now redundant since the finally handles them, and
keeping them around invited future readers to incorrectly remove either
one. Comment rewritten to honestly describe what the finally covers.

Verified end-to-end: success path, rsvg failure path, and pure-PNG
path all leave 0 leftover temp files in $TMPDIR.

NOTE: pdf/scripts/optimize-image.py at HEAD of skill/pdf-images has
the same edge case (its `_process()` refactor moves Pillow into a
helper, but the rsvg subprocess.run is still outside the cleanup
try/finally). Worth flagging for an upstream fix when convenient.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [4663b4d](https://github.com/SerendipityOneInc/ecap-skills/commit/4663b4d48929d6f485b8c71b8364a8eee2a8de7b) fix(pptx): smoke test section 1 unreachable under set -e (#137)

**作者**: felix-srp  
**SHA**: `4663b4d48929d6f485b8c71b8364a8eee2a8de7b`

```
`set -euo pipefail` is active at the top of pptx/tests/smoke_test.sh
(line 11). Section 1 currently runs `check_links.py` as a bare statement
followed by `if [ $? -eq 0 ]`:

    python3 "$SKILL_ROOT/tests/check_links.py" "$SKILL_ROOT"
    if [ $? -eq 0 ]; then
      pass "All internal markdown links are valid"
    else
      fail "Broken internal markdown links found"
    fi

When check_links.py exits non-zero (broken links found), bash aborts the
whole script immediately due to `set -e` — it never reaches the `if` line,
never records a `FAIL`, and never runs sections 2-11. Instead of a clean
test summary the user gets a confusing crash exit, with no indication
that section 1 was the cause and no record of the FAIL.

Fix: use the inline-`if` idiom that section 2 (line 42) and the rest of
the file already use. `if cmd; then ...` is exempt from `set -e` per
POSIX, so the bash abort path is bypassed and the test runner records
a graceful FAIL and continues.

This was a long-standing bug found during a wider sweep while reviewing
PR #134. Filing as a separate one-liner so it's reviewable on its own.

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [c531713](https://github.com/SerendipityOneInc/ecap-skills/commit/c5317132ac59f4fbd6368a9f45afc7b65fa1e0ed) feat(web-designer): v2 — stunning HTML page generation with React+ECharts+Framer Motion (#126)

**作者**: felix-srp  
**SHA**: `c5317132ac59f4fbd6368a9f45afc7b65fa1e0ed`

```
* chore(web-designer): clean slate — remove old v1 files for v2 rewrite

* feat(web-designer): add tailwind.config.js and components.json templates

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

* feat(shared): add pre-downloaded .woff2 fonts for web-designer skill

Latin: Outfit, Bricolage, Playfair, Sora, DM Sans, Lora, Crimson Pro, etc.
CJK: Noto Sans SC/JP/KR, LXGW WenKai
Fallback: Noto Sans Arabic, Thai, Devanagari

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

* feat(web-designer): add index.css template with font-face, themes, CJK, print

* feat(web-designer): add bundle.sh — Parcel build + html-inline to artifacts/

* feat(web-designer): add init.sh — scaffolds React+Vite+Tailwind+shadcn+ECharts project

* feat(web-designer): add SKILL.md v2 — 4-phase workflow with quality gates

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

* feat(web-designer): add design-system.md — themes, typography, motion, effects

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* feat(web-designer): add components.md — ECharts, motion, navigation, content blocks

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* feat(web-designer): add content.md — copywriting, asset prompts, data realism

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(web-designer): fix init.sh path bug and switch bundle.sh from Parcel to Vite build

- init.sh: cd into .build/ before running pnpm create vite (fixes relative path issue)
- init.sh: strip JSONC comments from tsconfig.app.json before JSON.parse
- init.sh: use .cjs extension for postcss/tailwind configs (ESM project compat)
- bundle.sh: replace Parcel with Vite build + custom Node.js inliner
- Tested end-to-end: init → write App.tsx → bundle → 1.5MB inlined HTML

* feat(web-designer): add report.html example — Manus-quality CJK data report

Chinese AI agent market research report with Ocean Depths theme, ECharts
visualizations (bar, line, radar, area), animated KPI counters, scroll-spy
TOC, and Framer Motion reveals. Demonstrates full build pipeline output.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* feat(web-designer): add slides.html example — Gamma-quality slide deck

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* feat(web-designer): add landing.html example — product marketing page

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* feat(web-designer): add blog.html example — rich article with CJK

Long-form article about AI agents with mixed English + Chinese content.
Botanical Garden theme (sage green, warm cream). Includes reading progress
bar, ECharts line chart, Python code block, pull quote, author bio card,
scroll-reveal animations, and back-to-top button.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(web-designer): preserve type=module in inlined scripts

Vite emits <script type="module" src=...> in <head>. Removing the src but
also stripping type=module caused scripts to execute before DOM was ready,
resulting in blank pages. Now preserving type=module defers execution
until DOMContentLoaded, matching original Vite behavior.

Also remove modulepreload link tags which are useless after inlining.

* fix(web-designer): rebuild examples with fixed bundler (type=module preserved)

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* feat(web-designer): add InViewChart wrapper, animation presets, and Presentation component

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

* feat(web-designer): presentation-mode slides + scroll-triggered chart animations

- slides: replace scroll-snap with Presentation component (keyboard nav, AnimatePresence)
- report: wrap all charts with InViewChart + dramatic/smooth animation presets
- blog: scroll-triggered line chart with smooth preset + gradient fill

* fix(web-designer): use direct ECharts API to prevent animation interruption

The echarts-for-react wrapper calls setOption() on every React re-render
when it detects a new option prop reference. This interrupted running
animations (freezing charts mid-draw on hover) and broke tooltip state
(only first point triggered after animation).

Fix: InViewChart now uses direct echarts.init() + setOption() inside a
useEffect with [isInView] dependency. Chart initializes exactly once when
scrolled into view, React re-renders no longer affect it.

* fix(web-designer): ECharts tooltip conflicts on line/area charts

- Use trigger: 'axis' for line/area charts (not 'item')
- Remove per-point animationDelay that broke tooltip hit detection
- Document tooltip trigger rules in components.md
- Fixes issue where hovering during animation froze chart and tooltip only worked on first point

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

* Revert "fix(web-designer): ECharts tooltip conflicts on line/area charts"

This reverts commit c4e2544101509de600b1dc32546ea2b1fc8a085a.

* fix(web-designer): address code review issues

Critical:
- useCountUp hook: accept elementRef from caller (was never attached to DOM)
- ECharts chart sections: use direct API pattern via InViewChart (was using echarts-for-react wrapper that caused animation/tooltip bugs)

Important:
- components.json: reference tailwind.config.cjs (matches init.sh rename)
- design-system.md: remove Source Han Serif SC and Clash Display (not in fonts dir), replace with LXGW WenKai and Cabinet Grotesk
- init.sh: use node instead of BSD-only 'sed -i \'\'' for cross-platform (Linux/macOS)
- init.sh: warn when Noto Sans CJK subset files are missing
- init.sh (vite.config): inlineDynamicImports to prevent bundle splitting
- bundle.sh: robust regex for <link> and <script> tags (any attribute order)
- Presentation: guard space/arrow keys in form inputs

Minor:
- useScrollSpy: stable dependency via sectionIds.join()
- Shimmer keyframes: clarify direction in doc

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

* fix(web-designer): replace Noto Sans CJK subset files with full-coverage single files

The 698-subset-per-font approach caused @font-face rules to collide:
each subset had identical font-family + font-weight without unicode-range,
so per CSS spec only the last rule wins. ~697/698 subsets were silently
ignored, causing missing CJK glyphs (tofu) for most characters.

Fix:
- Replace subset files with 6 full-coverage .woff2 files (~11-12MB each)
  for Noto Sans SC/JP/KR × regular/bold
- Simplify init.sh to generate one @font-face per family+weight
- Add artifacts/ to .gitignore (was missing)

* fix(web-designer): rebuild examples with correct CJK font references

Previous examples had 698 broken @font-face subset references per file
(total 2,792 broken requests across all 4 files). Rebuilt with the
simplified single-file-per-family init.sh logic.

Each file now references exactly 6 CJK woff2 files (sc/jp/kr ×
regular/bold) with no numeric suffixes. Content rebuilt as simplified
but high-quality versions:
- report.html: Ocean Depths theme, Chinese AI agent market report with
  bar + line ECharts (InViewChart), 4 KPI cards, competitive table
- slides.html: Sunset Boulevard theme, 8-slide product pitch deck using
  Presentation state-machine pattern with donut chart on MetricsSlide
- landing.html: Modern Minimalist/Geist, SaaS landing page (FlowDesk)
  with sticky nav, hero, features, how-it-works, metrics, testimonials,
  pricing, CTA, footer
- blog.html: Botanical Garden theme, mixed EN+Chinese article with
  ReadingProgressBar, BackToTop, PullQuote, CodeBlock, line chart, and
  a Chinese-language section with lang="zh-Hans"

Also update stale comment in templates/index.css to describe the
current single-file-per-family approach.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

* fix(web-designer): rebuild report/slides/landing with verified InViewChart pattern

Previous rebuild had chart components that didn't match the verified
pattern. Using the exact same InViewChart implementation that was
manually tested and confirmed to work correctly with animation +
tooltip (no hover-freeze, no first-point-only tooltip).

* fix(web-designer): make references clickable with proper link semantics

- Rebuild example-report with clickable <a> tags in references section
- External links include target='_blank' and rel='noopener noreferrer'
- Inline citations [1], [2] etc. scroll to references section via anchor
- Update references/content.md citation system docs to require clickable links

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

* fix(web-designer): use chart-appropriate tooltip triggers

- Bar charts: trigger 'axis' with axisPointer shadow (highlights column)
- Line/area: trigger 'axis' with axisPointer line dashed (vertical line)
- Pie/radar: trigger 'item' (hover individual elements)
- Update components.md Tooltip Configuration Rules section with per-chart-type guide
- Rebuild example-report with correct bar chart tooltip behavior

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* feat(web-designer): enhance example-report with more chart types

- Add gauge chart for overall market health score in executive summary
- Add donut chart for use case distribution (new section 💡 用例分布)
- Add horizontal bar chart for revenue by segment in financial section
- Add comparison matrix table below radar chart for per-dimension scores
- Now showcases 7 chart types: bar, line/area, radar, area, donut, horizontal bar, gauge

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

* fix(web-designer): disable gauge interaction with silent:true

ECharts adds cursor:pointer on hover by default for all interactive
elements, including gauges. For display-only gauges (KPIs, health
scores), this creates a misleading UX — users think they can click.
Adding silent: true disables all hover/click interaction and removes
the pointer cursor.

Also document this gotcha in references/components.md for future
generations.

* feat(web-designer): rebuild example-slides using skill workflow with AI-generated images

Rebuilds examples/slides.html as a 9-slide Lumen Signal product pitch using
the Sunset Boulevard dark-creative theme. Uses the Presentation component
pattern (state-based with keyboard nav + AnimatePresence), two ECharts
visualizations (market donut, MTTR paired bar), and five images generated
via the designer skill (openai/gemini-2.5-flash-image).

* feat(web-designer): rebuild example-landing using skill workflow with AI-generated images

* feat(web-designer): rebuild example-blog using skill workflow with AI-generated images

* feat(web-designer): rebuild example-report using skill workflow with AI-generated images

* fix(web-designer): address documentation gaps from 4-agent e2e test

Critical fixes:
- Presentation component: fix stale closure bug with functional setCurrent

Important fixes:
- templates/index.css: use Geist as default Modern Minimalist fonts
- Add theme-switching instructions to docs
- Vite @font-face warnings: use /assets/fonts root-absolute paths
- bundle.sh: inline images as base64 data URIs for self-contained HTML
- Add scripts/optimize-image.py Pillow-based helper
- design-system.md: add CJK font pairing guidance per theme
- components.md: add Phosphor icon lookup, typography recipes, classic gauge
- tailwind.config.js: add bg-gradient-radial and bg-gradient-conic utilities
- Landing page: document standard section archetype list

Discovered via 4 parallel agents building example pages end-to-end
using only skill documentation.

* feat(web-designer): rebuild example-slides round 2

* feat(web-designer): rebuild example-blog round 2

* feat(web-designer): rebuild example-landing round 2

* feat(web-designer): rebuild example-report round 2

* fix(web-designer): round 2 — critical regex + documentation polish

Critical:
- bundle.sh: replace quote-dependent image inlining regex with
  path-based matcher that handles Vite's backtick-minified JSX output
  (verified failing in 4/4 round 2 e2e tests)

Important:
- SKILL.md + content.md: document optimize-image.py helper as preferred
  post-processing tool; promote it over sharp/ffmpeg in content.md
- templates/index.css: align default palette with design-system.md §3.4
  Modern Minimalist (avoid pure #FFFFFF which violates anti-slop)
- Theme switching docs: clarify that --success-foreground etc. extras
  should be preserved when replacing :root block

Minor:
- init.sh vite.config: remove deprecated inlineDynamicImports,
  add chunkSizeWarningLimit: 2000
- SKILL.md quality gates: clarify fonts remain external (too large)
- SKILL.md overview + build pipeline: align wording with actual behavior

* fix(web-designer): fix ECharts emphasis/hover bugs

Discovered via e2e testing — 3 chart hover bugs in example-report:
- Bar: second hover didn't clear first bar's shadow highlight
- Pie: flickered due to graphic center labels capturing mouse events
- Area: lines disappeared on hover due to wrong emphasis.focus/blur config

Fixed by updating components.md chart patterns with:
- Explicit emphasis config for bar with shadow axisPointer clearing
- silent: true on pie chart graphic center label elements
- Removing focus:'series' with blurScope:'global' on area charts
- New 'Emphasis & Hover Rules' section documenting pitfalls

Also rebuilt example-report with corrected configs.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

* feat(web-designer): rewrite SKILL.md description for better skill discovery

- Add comprehensive trigger keywords (English + Chinese)
- Explicit comparison with pdf/pptx/docx/xlsx skills
- List 50+ chart type keywords for ECharts coverage
- Declare dependency on designer + websearch skills in metadata
- Add CJK / multi-language positioning prominent in description
- Reorganized Overview section with 'when to invoke' and 'what makes it different'
  to help LLM-based skill selection in ZooClaw

* fix(web-designer): definitive fix for chart hover-disappearance bug

Root cause identified via isolated browser reproduction:
ECharts Canvas renderer does NOT support CSS Color Level 4
space-separated hsl() syntax ('hsl(174 72% 46%)'). Charts render
initially but disappear on hover because emphasis color derivation
silently fails in the custom ECharts parser.

Fix:
- Add themeColor() helper to convert Tailwind-style CSS vars
  ('174 72% 46%') to legacy comma hsl syntax ('hsl(174, 72%, 46%)')
- Add prominent warning to top of ECharts section in components.md
- Update all chart examples (2.1-2.7) to use themeColor() instead of
  raw 'hsl(var(--accent))' strings
- Scaffold src/lib/chart-utils.ts in init.sh with the helper
- Rebuild all 4 example pages with the corrected pattern

Previous investigation rounds misdiagnosed as emphasis/focus/blur
config issues. None of those were the actual cause. This is the
definitive fix verified via isolated test.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(web-designer): make SKILL.md description concise

* refactor(web-designer): compress SKILL.md Overview to 2 sentences

* refactor(web-designer): remove all special hover configs, use ECharts defaults

Three rounds of investigation wrongly blamed chart hover bugs on
emphasis/silent/focus/blurScope configs. The true root cause was
CSS Color Level 4 hsl() syntax (fixed in bbf2962 with themeColor()).

Cleanup:
- Remove 'Emphasis & Hover Rules' section 2.10 (wrong diagnoses)
- Remove emphasis.focus:'self' from bar examples
- Remove silent:true from pie graphic center labels
- Remove emphasis.scale:false from pie series
- Remove silent:true from gauge (let it show pointer cursor like others)
- Remove all 'gauge gotcha' and similar anti-pattern warnings
- Rebuild all 4 examples with pure ECharts defaults

Principle: all charts use ECharts default hover behavior for UX
consistency. Defaults are designed by dataviz experts and agent-side
'optimization' was causing bugs and inconsistency.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

* feat(web-designer): rebuild all 4 examples with full quality

- Apply proper theme CSS variable overrides (Ocean Depths, Sunset
  Boulevard, Modern Minimalist, Botanical Garden)
- Use themeColor() helper for all chart colors to avoid modern
  hsl() Canvas parsing bug
- Ensure area charts have visible gradient fills (0.4 to 0.02 alpha)
- Generate 3-6 AI images per example via designer skill
- Use default ECharts hover behavior (no emphasis/silent configs)
- Verified theme application in bundled output

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(web-designer): address round 5 review issues

Critical:
- Section 2.8 tooltip examples used forbidden 'hsl(var(--card))' syntax
  (the exact bug pattern that section 2 CRITICAL warning forbids)
  → rewrite all 3 tooltip recipes to use themeColor() helper

Important:
- design-system.md §5.2 described slides as scroll-snap, contradicting
  components.md §7.11 Presentation component → align both to
  state-based Presentation as canonical pattern
- Latin display fonts table had duplicate Cabinet Grotesk row
  → replace with General Sans

* fix(web-designer): correct slides example description — state-based Presentation, not scroll-snap

* fix(web-designer): install gsap in init.sh

GSAP is documented as first-class animation library (SKILL.md Tech Stack,
design-system.md motion intensity 6-10, components.md section 7.8
HorizontalScrollHijack) but wasn't in the install list. Any agent using
scroll-linked animations would hit 'Cannot find module gsap' at build time.

* fix(web-designer): use 'uv run' consistently for script invocations

- Change python3 ../websearch/... to uv run ../websearch/... (per ecap-skills convention)
- Standardize --with pillow (lowercase) across all optimize-image.py calls

* test(web-designer): rebuild landing example with real logos via websearch skill

Tests the end-to-end websearch image pipeline documented in content.md §9:
search → parse JSON → download with browser UA → optimize via Pillow helper.
Trust bar now shows 6 real company logos (Stripe, Notion, Vercel, Linear,
Figma, Shopify) instead of fictional ones, validating the websearch integration
path. All logos fetched from Wikimedia Commons (5) and seeklogo (1), converted
to WebP via optimize-image.py, and base64-inlined in the final HTML bundle.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

* feat(web-designer): handle SVG input in optimize-image.py + docs

E2E test of websearch image pipeline found that imageUrl can be SVG
(common on Wikimedia Commons for logos). Pillow can't open SVG directly.

Fix:
- optimize-image.py: auto-rasterize SVG input via cairosvg (preferred,
  when libcairo available) or rsvg-convert binary (fallback, works on
  macOS/Linux with librsvg installed). Tested end-to-end — SVG → WebP.
- content.md §9: add SVG gotcha note + pipeline snippet that filters
  search results to PNG/JPG first to avoid the issue entirely.
- Add rsvg-convert path as documented fallback when no SVG converter
  is available in the environment.

* fix(web-designer): simplify SVG handling to rsvg-convert only + declare deps

Testing showed no pure-Python SVG → raster option works:
- svglib (latest) requires libcairo (via rlpycairo)
- svglib 1.5.1 pinned also fails on modern reportlab
- cairosvg also requires libcairo
- Real SVGs with gradients/patterns need a real rendering engine

rsvg-convert (librsvg2-bin, 5MB, used by Wikipedia) is the best choice:
- Smallest package (~5MB)
- Best quality (GNOME project)
- Fast (C code)
- Zero Python deps

Changes:
- optimize-image.py: drop cairosvg import attempt, go straight to rsvg-convert
  with clear error message listing install commands
- SKILL.md metadata: declare rsvg-convert + uv as required binaries
- SKILL.md: add 'System Requirements' section telling ZooClaw pod builder
  to 'apt install librsvg2-bin' for SVG support

* refactor(web-designer): remove System Requirements section from SKILL.md

Dependencies already declared in metadata.requires.bins — no need to
spend tokens documenting them again in prose.

* chore(web-designer): move design docs out of skill tree

Design spec and implementation plan belong in ~/Workspace/design-doc/
alongside other skill design docs (pdf, xlsx, etc.), not inside the
skill source tree. Moved files:

- docs/superpowers/specs/2026-04-09-web-designer-v2-design.md
  → ~/Workspace/design-doc/2026-04-09-web-designer-design.md
- docs/superpowers/plans/2026-04-09-web-designer-v2.md
  → ~/Workspace/design-doc/2026-04-09-web-designer-plan.md

artifacts/ is already in .gitignore (commit fbe5a70), no tracked
artifact files to remove.

* chore(shared): stop tracking font binaries, add manifest README

Font .woff2 files (24 files, ~76 MB total) should not live in git.
The pod image builder populates shared/fonts/web/ as part of the
base image based on the manifest.

Changes:
- Remove 24 tracked .woff2 files from git (still present on disk,
  working copy unaffected)
- Add shared/fonts/web/README.md with the full font manifest:
  names, sources, and OTF → WOFF2 conversion tip
- Add shared/fonts/web/.gitignore to prevent re-committing binaries

* chore(web-designer): strip to runtime-only files

Skill directory now contains only files required at runtime:

  SKILL.md
  dependencies.md      — manifest for pod image builder (system bins, fonts)
  references/          — 3 reference docs the LLM loads
  scripts/             — init.sh, bundle.sh, optimize-image.py
  templates/           — tailwind.config.js, index.css, components.json

Removed from git:
- examples/*.html      — 4 example bundles (not used at runtime)
- .gitignore           — build artifact patterns live in top-level .gitignore
- .serena/             — local tool config, not skill runtime
- shared/fonts/web/README.md → moved into web-designer/dependencies.md

Also removed the Examples section from SKILL.md since the files are gone.

* chore(web-designer): rename dependencies.md to DEPENDENCIES.md

Match the ALL CAPS convention used for repo-root metadata files
(SKILL.md, README.md, LICENSE, CHANGELOG.md, etc.).

* chore(web-designer): fix stale font size + remove dead html-inline install

- SKILL.md: 24MB → ~70MB (CJK font total, accurate after full-coverage replacement)
- bundle.sh: remove dead 'pnpm add -D html-inline' install attempt
  (we use the inline Node script, not the html-inline package)

* chore(shared): remove shared/fonts/web/.gitignore

Font binary patterns can be covered by the top-level .gitignore if needed.
Individual skill/subdirectory .gitignore files are not runtime-required.

* fix(web-designer): 3 bugs found by codex review

[P1] templates/index.css + init.sh: use relative './assets/fonts/...'
instead of root-absolute '/assets/fonts/...' in @font-face URLs.
Absolute paths resolve against the domain root, so artifacts served
at any subpath (including file:// and ZooClaw's per-project URLs)
silently fail to load custom fonts. 18 Latin + 3 fallback + 6 CJK
generated rules all fixed.

[P2] init.sh vite.config: add inlineDynamicImports: true to
rollupOptions.output. manualChunks:undefined alone does not prevent
Rollup from splitting React.lazy()/import() into extra chunks, which
bundle.sh doesn't inline → runtime failure. Re-adding this option
ensures a true single-entry bundle.

[P2] optimize-image.py: preserve alpha for palette-mode PNGs with a
transparency index (PIL mode='P' + 'transparency' in info). Previous
check 'A in im.mode' missed this common logo/icon format, dropping
transparency to an opaque background in the WebP output.

All 3 fixes verified end-to-end with init.sh + a synthetic palette PNG.

* fix(web-designer): composite RGBA onto white when saving JPEG

Pillow cannot encode alpha channels in JPEG — attempting to save
an RGBA or LA image as JPEG raises 'cannot write mode RGBA as JPEG'.
Any logo or transparent PNG passed with --output *.jpg currently
crashes. Fix by compositing the image onto a white background
before saving, which is the standard behavior for JPEG exports.

Also fix small bug: uppercase the format string from --format arg
too (not just from suffix), so --format webp works same as --format WEBP.

Verified: RGBA PNG → JPEG output now produces valid 3-channel JPEG
without crashing. (Found by codex review of PR #126.)

* fix(web-designer): move @font-face to public/fonts.css, eliminate Vite warnings

Codex review round 3 kept flagging the './assets/fonts/...' URL paths
in templates/index.css as a Vite build issue. Previous rounds fixed
the runtime behavior (relative paths are correct), but Vite's CSS
preprocessor still tries to resolve these URLs at build time relative
to src/index.css and emits 24+ warnings per project.

Clean fix: extract all @font-face declarations into templates/fonts.css,
which init.sh copies to public/fonts.css (Vite copies public/ files
as-is without processing). index.html gets a <link rel='stylesheet'
href='/fonts.css' /> injection via the existing Node cleanup step.
bundle.sh inlines this stylesheet along with the Vite-generated one.

Changes:
- New file: templates/fonts.css (140 lines, all Latin + LXGW WenKai +
  fallback @font-face rules, moved verbatim from templates/index.css)
- templates/index.css: stripped of all @font-face rules (now 189 lines,
  only Tailwind + theme vars + base styles)
- scripts/init.sh:
  * Copy templates/fonts.css to public/fonts.css
  * Append Noto CJK @font-face rules to public/fonts.css (not src/index.css)
  * Inject <link rel='stylesheet' href='/fonts.css' /> into index.html
  * Replace deprecated rollupOptions.output.inlineDynamicImports with
    build.codeSplitting: false (Vite 8 rename)

Verified end-to-end:
- Vite build: zero warnings (was emitting 24+ font resolve warnings)
- bundle.sh: correctly inlines fonts.css into final HTML (29 @font-face
  rules present after bundling)
- Font paths in final HTML: all relative './assets/fonts/...'
- Runtime: Chrome incognito loads all fonts from artifacts/<project>/assets/fonts/

* fix(web-designer): 2 bugs from codex review round 4

[P1] Revert to rollupOptions.output.inlineDynamicImports: true
Vite 8's deprecation warning suggests 'build.codeSplitting: false' as
the replacement, but verified empirically that setting does NOT work
(React.lazy() still produces separate LazyHeader-<hash>.js chunk).
inlineDynamicImports still functions correctly despite the warning.
Without this, any generated page using React.lazy() or import() would
break at runtime because bundle.sh only inlines the entry chunk.

[P2] bundle.sh: copy dist/assets/* (excluding already-inlined .js/.css)
to artifacts/<project>/assets/. Previously only public/assets/ was
copied, so any page that imports an asset from src/ (e.g., 'import
logo from ./logo.svg') would get a hashed reference in the inlined JS
but the actual file would be missing from the shipped artifact.

Both bugs found by codex review of PR #126.

* fix(web-designer): rewrite absolute /assets/ URLs to relative ./assets/

Vite emits src/ imports (e.g. 'import logo from ./logo.svg') as
root-absolute /assets/<hash>.<ext> paths in the bundled JS. These
only resolve correctly when the HTML is served from the domain root,
breaking file:// viewing and any subpath deployment (including
ZooClaw's per-project artifact URLs).

Fix: after all inlining, do a single pass to rewrite any quoted
'/assets/' prefix (single quote, double quote, or backtick) to
'./assets/'. Combined with the dist/assets copy step, this makes
src-imported assets work from any path.

Verified end-to-end with a 22KB test SVG:
- Vite emits to dist/assets/logo-DYP9eBf2.svg (hashed)
- bundle.sh copies to artifacts/<project>/assets/
- Rewritten reference in bundle.html: `./assets/logo-DYP9eBf2.svg`
- Zero remaining unquoted /assets/ references
- Opens correctly in Chrome via file://

Found by codex review round 5 of PR #126.

* fix(web-designer): also rewrite bare url(/assets/) in CSS

Previous rewrite only matched quoted ('"`) absolute /assets/ prefixes,
missing CSS url(/assets/...) form emitted by Vite for assets imported
from src/index.css (e.g. background-image: url('./hero.svg')).
Extended regex to also match 'url(' as a valid prefix.

Verified with a CSS background-image referencing a 125KB SVG:
before → 'url(/assets/hero-HASH.svg)'
after  → 'url(./assets/hero-HASH.svg)'

Found by codex review round 6 of PR #126.

* fix(web-designer): use 'pnpm --yes create vite' for unattended init.sh

On fresh machines where create-vite isn't cached in pnpm's store, pnpm
prompts 'Ok to proceed? (y/n)' before fetching, which blocks init.sh
automation until a human answers. Adding --yes auto-confirms so Phase 3
scaffolding runs unattended as intended.

Found by codex review round 8 of PR #126.

Note: codex also suggested failing fast when ../shared/fonts/web is
missing, but the current warn-and-continue behavior is intentional —
it lets devs verify layouts locally without the 76MB font pack, with
graceful fallback to system fonts. The pod image builder populates
fonts in production.

* fix(web-designer): support dynamic chart updates + TextScramble timer cleanup

[P2] InViewChart: add second useEffect to call setOption(option) when the
option prop changes after initial mount. Previously the chart locked in
its initial option and ignored all updates, breaking loading→loaded
states, theme toggles, and interactive filters. The init effect still
only depends on [isInView] so the entrance animation runs once; the
update effect runs on [option] changes but only after chartRef.current
is set (so it skips pre-mount renders). Document that parents should
useMemo their option if they create it inline per render.

[P3] TextScramble: clear the setInterval on unmount and when text/speed
changes mid-scramble. Previously the interval would keep firing and
calling setDisplay on a stale component instance, leaking timers and
triggering React state-update-after-unmount warnings in slide transitions
or conditional sections.

Found by codex review round 9 of PR #126.

* fix(web-designer): escape </script> in bundles + preserve SVG intrinsic size

[P2] bundle.sh: escape literal '</script' inside inlined JS bundles as
'<\/script'. If the page content embeds raw HTML closing tags (e.g. a
blog post about HTML parsing, or a code sample), the browser would
terminate the inline <script> tag early, corrupting the final artifact.
This is the standard escape for JSON/script embedding.

[P2] optimize-image.py: when --resize is not given, don't pass -w 1920
to rsvg-convert. Let the tool use the SVG's intrinsic size instead.
Previously a 50x50 logo SVG would be upscaled to 1920x1920 and produce
an unnecessarily large WebP. Verified: 50x50 SVG → 50x50 WebP without
--resize, → 100x100 WebP with --resize 100x100.

Found by codex review round 10 of PR #126.

* fix(web-designer): inline all src/ image assets + fix fallback unreachability

[P2] bundle.sh: unified asset inliner reads from dist/assets/ (not just
public/assets/images/). The new regex matches /assets/<path>.<ext> for
any image file extension and looks up the file in dist/assets/, which
contains both public/ copies AND Vite-hashed src/ imports. Fonts are
explicitly skipped (too large). This fulfills the 'single self-contained
HTML' contract: importing logo from './logo.svg' in src/ now inlines
as a data URI, not a sidecar file.

[P3] bundle.sh: wrap the node inliner in 'set +e' / 'set -e' so the
fallback to dist/index.html actually runs if the inliner throws.
Previously 'set -e' at the top of the script would abort bundle.sh
on any node -e failure, never reaching the bundle.html existence check.

Also: fix init.sh 'pnpm --yes' → 'echo y | pnpm'. pnpm doesn't have
a --yes flag; the correct way to auto-confirm the 'Ok to proceed?'
prompt on first-run is to pipe 'y' to stdin.

Removed the dist/assets/ sidecar copy loop since the inliner now
handles everything except fonts (which come from public/assets/fonts/).

Verified end-to-end with a 21KB SVG import: inlined as data URI,
zero sidecar files, artifacts/<project>/assets/ contains only fonts.

Found by codex review rounds 8+10 of PR #126.

* fix(web-designer): robust bundle fallback path

[P1] Remove stale bundle.html at start of each run. If a previous run
succeeded and the current run's inliner fails, the [-s bundle.html]
check would pass with stale content and ship the previous build as if
it were the current one. Now rm -rf dist bundle.html at the top so
there's no chance of stale output.

[P1] When falling back to dist/ verbatim (inliner failed), copy the
entire dist/assets/ too. Previously only dist/index.html was copied,
leaving the fallback HTML referencing /assets/*.js, /assets/*.css etc.
that weren't shipped, so the fallback page failed to boot. Now the
fallback copies the full dist/ tree including all hashed assets.

Also: clean the artifacts directory at the start of each copy phase
so leftover files from a previous (different) bundle shape never
mix with the current run.

Found by codex review round 12 of PR #126.

* fix(web-designer): fallback path copies full dist/ and rewrites URLs

Previous fallback only copied dist/index.html + dist/assets/*, missing
dist/fonts.css (Vite copies public/fonts.css to dist root). It also
left the absolute /assets/ and /fonts.css URLs untouched, so the
delivered fallback wouldn't work under file:// or from a subpath.

Fix: cp -a dist/. $ARTIFACTS_DIR/ mirrors the whole dist tree, then
a tiny node script rewrites absolute paths to relative in index.html.

Found by codex review round 13 of PR #126.

* feat(web-designer): final rebuild example-landing — full showcase with websearch logos

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* feat(web-designer): final rebuild example-report — Chinese data report showcase

Flagship example for the web-designer skill: a 2026 Chinese market research
report on the humanoid robotics industry, rendered in the Ocean Depths theme
with CJK typography, scroll-spy TOC, 4 animated KPI cards, 7 ECharts chart
types (horizontal bar, dual-axis area, radar, donut, classic gauge with
rotating pointer, stacked bar, heatmap), a comparison matrix, clickable
citations, 4 AI-generated images, and recommendation callouts.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* feat(web-designer): final rebuild example-slides — Presentation showcase

* feat(web-designer): final rebuild example-blog — mixed EN+CJK article showcase

* fix(web-designer): document exact designer skill CLI in content.md §8

3/4 rebuild agents hit 'ModuleNotFoundError: No module named litellm'
on first run because the docs said 'Use the designer skill to generate'
without showing the actual uv run command. Adding the full CLI with
all 4 required --with deps (litellm, aiohttp, Pillow, + implied openai)
plus both available model names.

Found by final rebuild agents of PR #126.

* fix(web-designer): 2 bugs reported by pptx skill sync

[1] optimize-image.py: apply EXIF orientation before processing.
Phone/camera JPEGs embed an Orientation tag instead of rotating the
raw pixel data. Browsers apply this automatically in <img> rendering
but Pillow does not — without ImageOps.exif_transpose(), a portrait
iPhone photo would come out sideways in the final WebP.

Verified: input 400x200 with Orientation=6 → output 200x400 (rotated),
left blue band correctly ends up at the top.

The pptx skill already has this fix (they learned image handling from
web-designer and hit the bug first). This PR backports it upstream.

[2] SKILL.md: remove non-standard 'requires.skills' metadata field.
No other skill in ecap-skills uses requires.skills — the 'requires'
block is for system-level deps (bins/env), not skill composition.
codex flagged this as semantically inconsistent when pptx was being
reviewed. Dependencies on designer/websearch are still documented in
the description text and Overview section, which is what matters for
LLM skill discovery.

Found by pptx skill's codex review during image-handling sync.

* fix(web-designer): document pie+legend layout + clickable contact info

User found 2 bugs in the final showcase examples:

1. Report pie chart's right arc visually overlapped the custom HTML
   legend text. Root cause: components.md §2.3 only documented the
   centered-pie-with-legend-below pattern; when an agent wrote a 2-col
   grid (chart | legend), the chart container stretched to fill half
   the row, the pie SVG centered in that wider column, and the right
   arc bled into the legend column.

2. Slides CTA slide displayed 'hello@kinograph.co' as plain text but
   clicking did nothing. Root cause: content.md §4 had no rule about
   clickable contact info, so agents default to <span>email</span>
   instead of <a href='mailto:...'>.

Fix:
- components.md §2.3: add a 'Layout with custom side legend' section
  showing grid-cols-[360px_1fr] with fixed chart column width and
  legend:{show:false} to hide default legend.
- content.md §4 CTA Patterns: add 'Interactive Contact Info' subsection
  with a table of correct markup for email, phone, address, social.

Agent reproduction of these fixes in the next rebuild round will
validate them as skill tests.

* feat(web-designer): rebuild example-slides — fix CTA email mailto link

* feat(web-designer): rebuild example-report — fix pie legend overlap

Rebuild the Chinese humanoid robotics 2026 research report showcase
with Ocean Depths theme. Fixes the previously-reported bug where the
donut chart's right arc visually overlapped the custom HTML side
legend next to it: the chart column now has a fixed 360px width
(grid-cols-[360px_1fr]) and the option override passes
legend:{show:false}, matching the new §2.3 pattern in components.md.

Verified via headless Chrome: 7 charts render (bar, line/area, donut,
radar, classic gauge, stacked bar, heatmap); pie canvas width = 360px,
gap to legend column = 40px (no overlap).

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### [0700822](https://github.com/SerendipityOneInc/ecap-skills/commit/070082221b16f55a6bcda846895b3d3bcda910c5) docs(skills): rewrite SKILL.md descriptions for better zooclaw discovery (#133)

**作者**: felix-srp  
**SHA**: `070082221b16f55a6bcda846895b3d3bcda910c5`

```
Rewrite descriptions for 7 skills (pdf, docx, xlsx, pptx, meeting-notes,
deep-research, humanizer) so that zooclaw and openclaw route to them more
reliably. The previous descriptions used literal phrase triggers ("create a
PDF", "write a report") which often missed user intents phrased differently
— especially in Chinese.

New descriptions follow a consistent formula:
- verb list up front (create/edit/read/fill/...)
- concrete artifact types (reports, proposals, resumes, whitepapers, ...)
- "use whenever deliverable is X or task implies Y" proactive clause
- dense trigger phrases in both English and Chinese

Kept all descriptions in the same ~55-70 word range to limit the per-call
token cost. No functional changes — frontmatter metadata, scripts, and
references are untouched.

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [97d5479](https://github.com/SerendipityOneInc/ecap-skills/commit/97d5479f20bd4845636cb15bb529b59392ca7d07) Revert "Update pptx skill and add frontend-zooclaw skill (#127)" (#132)

**作者**: felix-srp  
**SHA**: `97d5479f20bd4845636cb15bb529b59392ca7d07`

```
This reverts commit 6992d953460292dc0c924c94f8364c50cc4d319c.

Co-authored-by: felix-srp <felix@serendipityone.com>
```

### [d72b154](https://github.com/SerendipityOneInc/ecap-skills/commit/d72b1548ca1a82930d2eede794a5f7b02c175dc2) fix(pdf): clickable links + CJK layout + font fallback (#129)

**作者**: felix-srp  
**SHA**: `d72b1548ca1a82930d2eede794a5f7b02c175dc2`

```
* fix(pdf): make URLs and markdown links clickable in body text

The CREATE route rendered URLs as plain text because render_body.py
passed content through to ReportLab's Paragraph without any link
handling. Add a _linkify pre-pass that wraps [label](url) markdown
links and bare http(s) URLs in <link href=...> tags so ReportLab
emits clickable link annotations. Runs before i18n font-wrapping so
Chinese/CJK labels inside markdown links nest correctly.

Skip code/math text (their "text" is not prose). Also fix an
adjacent bug in _preprocess_i18n that crashed bibliography blocks by
calling str() on dict items instead of recursing into their "text".

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pdf): XML-escape URLs and preserve balanced parens in links

Review found three bugs in the linkify pass:

1. URLs with `&` in query strings (common) produced invalid XML inside
   href="..." and crashed ReportLab's Paragraph parser. Added
   _xml_escape helper applied to both the href attribute and the
   displayed URL text.

2. Markdown links with parenthesized paths were truncated. For
   example [Python](https://en.wikipedia.org/wiki/Python_(programming_language))
   stopped at the first `)` because _MD_LINK_RE used [^\s)]+.
   Relaxed the pattern to allow one level of balanced parens.

3. Bare URLs containing matched parens had their closing paren
   stripped as trailing punctuation. Replaced the simple trailing-set
   strip with _strip_url_trailing which only strips `)` when it
   would leave the URL's parens balanced — so
   https://en.wikipedia.org/wiki/Python_(programming_language)
   is kept intact while `(see https://example.com)` still drops
   the wrapping `)`.

Verified with 15-link test PDF covering &, parenthesized paths,
wrapping parens, sentence-ending periods, bilingual Chinese, table
cells, bullet items, bibliography dict items, and code blocks.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pdf): enable CJK wrap on prose styles to fix Chinese layout

Two symptoms in Chinese PDFs:

1. Closing brackets orphaned to the next line, e.g. 宽大偏差（Leniency）
   with the `）` dropped alone on the following line.

2. Enormous gaps inside justified paragraphs when a line contained a
   long unbreakable Latin token (URL slug like
   `performance-reviews-2025-11`). ReportLab pushed the token to the
   next line and justified the sparse remainder by stretching a few
   word-spaces across the full column width.

Root cause: the prose ParagraphStyles used alignment=TA_JUSTIFY but
did not set wordWrap="CJK". Without CJK wrap, ReportLab treats CJK
runs as one giant unbreakable "word" and has nowhere to absorb
justification slack except the few Latin spaces.

Fix: add wordWrap="CJK" to body, bullet, numbered, callout, caption,
table_header, table_cell, and bib styles. This lets ReportLab:
- break between any two CJK characters
- distribute justification stretch evenly across the line instead of
  concentrating it in a handful of inter-word gaps
- keep bracket/punctuation pairs like （Leniency）, （Central Tendency）,
  （Strictness）, （Self-Underrating Phenomenon） intact because the
  denser break-opportunity graph gives the greedy line-breaker much
  better alternatives

Verified against a reproducer drawn from the original PDF content:
all five paragraphs render cleanly, no orphan brackets, no huge gaps.
Re-ran the 15-link matrix — all links remain clickable (16 annots
now because CJK wrap splits one long URL across two lines, producing
one /Link rectangle per line per the standard PDF convention).

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pdf): extend ReportLab kinsoku set for Chinese punctuation

Follow-up to the wordWrap="CJK" fix. Code review found that even
though ReportLab's cjkFragSplit does implement partial kinsoku-shori
via the ALL_CANNOT_START set, the shipped set only contains Japanese
punctuation and is missing several Chinese fullwidth marks:

  ，  U+FF0C  fullwidth comma
  ；  U+FF1B  fullwidth semicolon
  ：  U+FF1A  fullwidth colon
  ！  U+FF01  fullwidth exclamation
  ？  U+FF1F  fullwidth question mark
  》  U+300B  right double angle bracket
  〉  U+3009  right single angle bracket

This was visible in the user's original PDF as an orphaned `，` on
page 2 (`，放大了系统性偏差。` starting its own line). After
enabling wordWrap="CJK" the closing bracket `）` cases are caught
by the existing ALL_CANNOT_START contents, but `，` and the other
missing marks still slip through and become line-leading.

Fix: at render_body.py import time, extend the ALL_CANNOT_START
binding inside reportlab.platypus.paragraph with the missing chars.
The string is immutable so rebinding reportlab.lib.textsplit's
export would not propagate — paragraph.py captured its own name at
import time via `from ... import ALL_CANNOT_START`. Patch the
paragraph module's binding directly so cjkFragSplit's runtime global
lookup picks up the extended set.

Verified:
- Bilingual reproducer showing no orphaned punctuation across 4
  paragraphs with ，；：！？）（Leniency）(Central Tendency) cases.
- Scanned the user's original PDF and confirmed zero remaining
  pure-punctuation orphan lines after the combined fixes.
- Link regression: all 16 link annotations still emitted correctly.

Known limitation: ReportLab only "hangs in margin" one overflow
char at a time, so a pathological case like
`...long-url/）。` (two forbidden chars after an overflow) can
still orphan the second char. This does not appear in the user's
real content; patching cjkFragSplit for multi-char hangs would
require copying the full 80-line function and is deferred.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* refactor(pdf): tighten kinsoku extension + add curly quotes

Code review feedback:
- Restructured the ALL_CANNOT_START extension to use a single
  comprehension instead of a for-loop so there is no loop variable
  to clean up (latent NameError if _EXTRA_CANNOT_START were ever
  edited to an empty string).
- Added ” (U+201D) and ’ (U+2019) — standard Chinese curly-quote
  closers — to the forbidden line-start set. These were absent from
  ReportLab's shipped ALL_CANNOT_START and would orphan the same
  way `，` did in the user's original PDF.

Verified: patch applies for all 9 added characters; link regression
and orphan regression tests both pass.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pdf): stop wrap_non_latin from referencing unregistered fonts

Surfaced while converting a real Chinese report that contained `——`
(em-dash U+2014). wrap_non_latin was blanket-wrapping every non-Latin-1
codepoint with either NotoSans or NotoSansCJKsc, but:

1. Em-dash, en-dash, ellipsis, and curly quotes (U+2000–U+206F General
   Punctuation) are already present in the standard Helvetica/Times
   encoding — wrapping them in a Noto font tag is unnecessary and
   visually inconsistent with surrounding Latin prose.

2. If only NotoSansCJK is discovered on disk (no NotoSans), wrapping an
   em-dash with `<font name="NotoSans">——</font>` produces XML that
   ReportLab's paraparser cannot resolve: ps2tt('NotoSans') raises
   "Can't map determine family/bold/italic for notosans" and kills the
   whole render.

Fix _needs_noto to (a) skip the General Punctuation block and (b) only
return a font name that is actually present in _discovered. If the
needed font is missing, return None so the character falls through to
the primary font and renders at worst as a notdef glyph — far better
than crashing the pipeline.

Verified by converting a 9-page bilingual Chinese/English report with
em-dashes, 68 inline links, tables, bullets, callouts, and numbered
lists.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* refactor(pdf): narrow _needs_noto skip set to verified WinAnsi chars

Code review correctly pointed out that the 112-codepoint U+2000–U+206F
range in _needs_noto was too broad. Most chars in the General
Punctuation block are NOT present in the WinAnsi/cp1252 encoding that
ReportLab's Type1 Helvetica/Times ships with — only ~15 are:

  U+2013 U+2014 (en/em dash)
  U+2018–U+201E (curly quotes, low quotes)
  U+2020–U+2022 U+2026 (dagger, double dagger, bullet, ellipsis)
  U+2030 (per mille)
  U+2039 U+203A (single guillemets)

With the broad skip, non-WinAnsi chars like U+2010 (hyphen), U+2025
(two-dot leader), U+2060 (word joiner) would silently render as notdef
glyphs via the primary font even when NotoSans was available to render
them correctly. Narrowed to a frozenset of the verifiably-WinAnsi
characters; everything else in the General Punctuation block now falls
through to the existing _discovered gate (which is the actual
crash-prevention mechanism — chars recommend a Noto font only if it is
registered).

Verified: the 9-page bilingual report with em-dashes still renders
identically (9 pages, 68 links, 399 KB). The crash fix is preserved;
the fallback behavior is more accurate.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pdf): prevent nested <link> when markdown label is itself a URL

External code review (codex) caught a functional regression in the
two-pass _linkify implementation. When the markdown label is
URL-shaped, the first (markdown) pass correctly produces:

  <link href=\"https://target.com\" ...><u>https://label.com</u></link>

The second (bare URL) pass then split on _LINK_TAG_RE which only
matches single XML tags, so the inner label text
\"https://label.com\" sat in an even-indexed (non-tag) segment and
was re-wrapped, producing nested <link> tags that ReportLab turns
into overlapping link annotations — and the inner (label) URL could
intercept clicks intended for the outer (target) URL.

Reproducer: _linkify(\"[https://label.com](https://target.com)\",
accent) returned

  <link href=\"https://target.com\"...><u><link href=\"https://label.com\"
  ...><u>https://label.com</u></link></u></link>

Fix: introduce a second tokenizer _LINK_REGION_OR_TAG_RE that treats a
full <link ...>...</link> region as a single atomic token (the longer
alternation branch fires first under Python's leftmost-first alternation
semantics). Pass the appropriate splitter into _apply: single-tag
splitter for the markdown pass (so bare <b>/<font> spans are skipped
normally), full-region splitter for the bare-URL pass (so the label
text inside a link we just produced is protected).

Verified: 7-case test including URL-shaped labels, Wikipedia parens,
mixed bare+markdown, bilingual, and empty — all produce link-depth <= 1.
Full regression matrix still passes (16 links in the test fixture, 68
links in the real Anthropic bilingual report).

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pdf): protect existing <link> regions in BOTH linkify passes

Follow-up to b0f37aa. External review (codex) pointed out that the
same nesting bug exists in the markdown pass: if upstream content
already contains ReportLab markup like

  <link href=\"https://x.com\" ...><u>[label](https://y.com)</u></link>

the markdown regex _MD_LINK_RE sees the inner `[label](https://y.com)`
as plain text (the previous pass used _LINK_TAG_RE which only tokenizes
on single XML tags, so the segment between <u> and </u> was processed)
and wraps it, producing nested <link> tags.

Fix: use _LINK_REGION_OR_TAG_RE for BOTH passes and delete the now-unused
_LINK_TAG_RE. A full <link>...</link> region is treated as one atomic
token in both the markdown and the bare-URL pass, so neither pass can
ever recurse into the body of an existing link — whether that link was
hand-written by the caller or produced by our own earlier pass.

Verified 7 cases including:
- pre-existing <link> with [label](url) inside (codex bug case)
- markdown label that is itself a URL
- Wikipedia-style parens
- mixed bare + markdown
- pre-existing link adjacent to new markdown
- bare URL inside an existing link body
- Chinese markdown label

All produce link-depth <= 1. 16-link fixture and 68-link real-world
bilingual report regressions both pass.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pdf): XML-escape markdown link labels to prevent crash on bare <

External review (codex) pointed at a real hazard in _sub_md: label
text from markdown links was inserted raw into the <u>...</u> body.
Verified empirically that `[R&D](url)` is fine (ReportLab's
HTMLParser-based paraparser is lenient about bare `&`), but
`[a<b](url)` produces `<u>a<b</u>` and CRASHES the paragraph parser
with a ValueError — ReportLab treats the bare `<` as the start of an
unclosed tag.

Fix: run m.group(1) through _xml_escape before interpolating into the
<u> body, same as already done for the href attribute. Labels can no
longer contain raw `<b>`/`<i>` markup but this feature was already
broken for a different reason: _LINK_REGION_OR_TAG_RE tokenizes
single tags, so a label like `<b>bold</b>` was splitting across
segments and failing the markdown match entirely. Users who want
styled link text should write the ReportLab <link> XML directly.

Tested: R&D, a<b, a>b, plain, Chinese labels — all render OK.
Regression matrix still 16 + 68 links.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pdf): make _xml_escape idempotent on existing entity references

External review (codex) flagged that _xml_escape was double-escaping
any input that already contained XML entities. For example, a caller
writing `[A &amp; B](https://example.com/?a=1&amp;b=2)` to defensively
pre-escape for ReportLab's paraparser ended up with `&amp;amp;` in
both the href attribute and the <u> label, so the link target became
`?a=1&amp;b=2` instead of `?a=1&b=2` and the visible text showed
`A &amp; B` instead of `A & B`.

Fix: introduce _XML_BARE_AMP_RE which only matches an ampersand that
is NOT already the start of a valid entity reference (named, numeric,
or hex). Replace that regex instead of the bare `.replace('&', ...)`.
The `<`, `>`, `"` replacements are unchanged — those characters don't
realistically appear pre-escaped in URLs or labels, and if they do,
the existing entity form (e.g. `&lt;`) no longer contains a literal
`<` after the amp pass so the replace is a no-op.

Now idempotent:
- `R&D`              -> `R&amp;D`         (bare & escaped)
- `A &amp; B`        -> `A &amp; B`       (pre-escaped preserved)
- `x&#10;y`          -> `x&#10;y`         (numeric entity preserved)
- `_xml_escape(_xml_escape('R&D'))` -> `R&amp;D` (double call stable)

Verified end-to-end: zero double-escaped URIs in the 16-link fixture
and the 68-link real-world bilingual report; literal `&` preserved in
all /URI action strings stored in the PDF.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

* fix(pdf): accept optional title in markdown link syntax

External review (codex) pointed out that _MD_LINK_RE rejected
`[label](url "title")` — the standard Markdown link syntax with an
optional title attribute. Because the markdown pass failed to match,
the bare-URL pass then ran on the inner URL and produced malformed
output like

  [label](<link ...>url</link> "title")

with the surrounding brackets and title text left as literal body
content.

Fix: rewrite _MD_LINK_RE in re.VERBOSE form and extend the URL
portion with an optional `\s+(?:"[^"]*"|'[^']*')` group that
consumes either a double-quoted or single-quoted title. The title
is matched but not captured — ReportLab links have no tooltip
equivalent so there is nothing to preserve it as, and simply
dropping it is the least-surprising behavior.

Verified:
- `[label](url "title")` — title consumed, clean link
- `[label](url 'title')` — single-quote variant
- Wikipedia URL + title combined works
- Plain markdown links still match
- Multiple links on one line all linkify correctly
- Unterminated title (malformed input) produces partial output —
  acceptable since no well-formed interpretation exists.

Regression matrix still 16 + 68 links.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [15c65d9](https://github.com/SerendipityOneInc/ecap-skills/commit/15c65d91ed3081d00681135d1481fe33f3644fac) fix(deep-research): prevent process leakage in report output (#131)

**作者**: felix-srp  
**SHA**: `15c65d91ed3081d00681135d1481fe33f3644fac`

```
Three targeted edits in SKILL.md to stop the agent from leaking
internal workflow into the delivered report:

- Before You Deliver: clarify self-challenge scores are a
  pre-delivery internal check, not a report section.
- Anti-Patterns → Process leakage: add self-challenge scores and
  meta-commentary defending the execution-failure vs information-gap
  classification as explicit examples of what to keep out.
- Fault tolerance: trim to a pointer to the Completeness gate
  recovery ladder to remove duplication.

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [6992d95](https://github.com/SerendipityOneInc/ecap-skills/commit/6992d953460292dc0c924c94f8364c50cc4d319c) Update pptx skill and add frontend-zooclaw skill (#127)

**作者**: Leah-srp  
**SHA**: `6992d953460292dc0c924c94f8364c50cc4d319c`

```
* Update pptx skill and add frontend-zooclaw skill

Replace pptx skill with delivery_0410 version (adds research/image
generation scripts and references). Add new frontend-zooclaw skill
for building frontend pages with AI-generated imagery.

* Fix frontend-zooclaw skill name to match directory

---------

Co-authored-by: liiiixy <lixiaoye@XiaoyeMacBook-Pro.local>
```

### [988a947](https://github.com/SerendipityOneInc/ecap-skills/commit/988a947ac94a6af5a0fe7617fa364e4f356be3b7) fix(deep-research): require recovery before dropping gaps into Limitations (#130)

**作者**: felix-srp  
**SHA**: `988a947ac94a6af5a0fe7617fa364e4f356be3b7`

```
Close a loophole where the Completeness gate and Fault tolerance rule
let execution failures (subagent timeout, error, empty return) be
silently reported under "报告局限性" instead of being recovered.
Limitations is now reserved for genuine information gaps; execution
failures must go through retry → reassign → main-agent inline.

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [a5794f0](https://github.com/SerendipityOneInc/ecap-skills/commit/a5794f05a545f2440331416157443a3cec08f730) chore: replace license with author metadata in skills (#125)

**作者**: felix-srp  
**SHA**: `a5794f05a545f2440331416157443a3cec08f730`

```
Remove MIT license field from pptx and xlsx, add "author: Ning Hu"
to all 9 Ning Hu-authored skills' SKILL.md frontmatter.

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

