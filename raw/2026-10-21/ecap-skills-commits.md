# SerendipityOneInc/ecap-skills — commits 2026-10-21

## fix(pptx): streamline authoring and validate final deck constraints (#300)

- **SHA**: `61c4cd3650797690dab0732a30085a9e47c99cf4`
- **作者**: kaka-srp
- **日期**: 2026-10-21T11:42:29Z
- **PR**: #300

### Commit Message

```
fix(pptx): streamline authoring and validate final deck constraints (#300)

PPT authoring spent repeated model turns reading a large reference
bundle and generating programs just to serialize slide data. Final QA
could also accept an extra page or a table that expanded beyond the
footer after rendering.

This change:

- Splits the skill into a compact entrypoint and route-specific
references. Agents write JSON data directly; `validate-spec --out`
atomically produces a canonical contract while preserving an existing
output on invalid input.
- Returns a compact QA decision summary, clarifies attachment
publication, and fixes the shared cover-label foreground against its
existing light chips.
- Adds optional `requirements.exact_slide_count`, checked before build
and against the final PPTX. Sizes raw table rows according to their
content and blocks rendered table overflow or clipped raw-table text
without discarding cells, shrinking text or adding pages.

Table evidence comes from the PDF already produced by LibreOffice, using
Poppler's `pdftotext`. Extraction failure preserves PNG previews and
blocks only decks that need table evidence. Grouped native tables are
detected recursively and explicitly blocked until ungrouped;
group-coordinate solving is outside this change.

Validation:

- Final full local PPT suite: **443 passed** (170.87 s), including four
header regressions added during PR review. Repository skill lint passed
with nine existing warnings; `git diff --check` and Node syntax
validation passed.
- Real raw and template builds with LibreOffice/Poppler; the current
synthetic fixture has exactly 14 pages and passes the count/table gates.
Replaying the prior synthetic artifact now rejects table defects on
slides 8, 13 and 14.
- Uneven CJK rows fit with all cells, the same 9.5-point font and one
page. An impossible table remains rejected with its data/font/page count
preserved.
- Independent Astra review completed; both reported boundary issues were
fixed and re-reviewed, including six independently rerun closure cases.

PR review identified a real header omission: the initial check could
pass a clipped template header, and raw headers used duplicated
shrinking overlays. The fix uses native raw header cells at 9.5pt,
includes their text in the row-height budget, and checks rendered header
completeness in both modes. All raw cells enter the completeness count;
matching legacy header overlays remain compatible. Before the patch,
three of four new real-render cases failed; after it, all four and the
full 443-test suite passed. Astra independently reran the four cases,
confirmed that the original clipped template now reports 163 missing
header characters, and found no further mandatory issue.

The existing skill CI selector does not register the PPT suite, so the
443-test result is local evidence, not a claim that CI runs it. Earlier
real Sonnet 4.6/medium trials verified authoring/build/publication
plumbing but did **not** establish faster delivery at equal quality. The
latest deterministic fixes have not had another paid model trial. No
skill publication, production rollout or existing Agent config update is
included.

---------

Co-authored-by: sharplee-srp <sharplee@srp.one>
```

### PR Body

PPT authoring spent repeated model turns reading a large reference bundle and generating programs just to serialize slide data. Final QA could also accept an extra page or a table that expanded beyond the footer after rendering.

This change:

- Splits the skill into a compact entrypoint and route-specific references. Agents write JSON data directly; `validate-spec --out` atomically produces a canonical contract while preserving an existing output on invalid input.
- Returns a compact QA decision summary, clarifies attachment publication, and fixes the shared cover-label foreground against its existing light chips.
- Adds optional `requirements.exact_slide_count`, checked before build and against the final PPTX. Sizes raw table rows according to their content and blocks rendered table overflow or clipped raw-table text without discarding cells, shrinking text or adding pages.

Table evidence comes from the PDF already produced by LibreOffice, using Poppler's `pdftotext`. Extraction failure preserves PNG previews and blocks only decks that need table evidence. Grouped native tables are detected recursively and explicitly blocked until ungrouped; group-coordinate solving is outside this change.

Validation:

- Final full local PPT suite: **443 passed** (170.87 s), including four header regressions added during PR review. Repository skill lint passed with nine existing warnings; `git diff --check` and Node syntax validation passed.
- Real raw and template builds with LibreOffice/Poppler; the current synthetic fixture has exactly 14 pages and passes the count/table gates. Replaying the prior synthetic artifact now rejects table defects on slides 8, 13 and 14.
- Uneven CJK rows fit with all cells, the same 9.5-point font and one page. An impossible table remains rejected with its data/font/page count preserved.
- Independent Astra review completed; both reported boundary issues were fixed and re-reviewed, including six independently rerun closure cases.

PR review identified a real header omission: the initial check could pass a clipped template header, and raw headers used duplicated shrinking overlays. The fix uses native raw header cells at 9.5pt, includes their text in the row-height budget, and checks rendered header completeness in both modes. All raw cells enter the completeness count; matching legacy header overlays remain compatible. Before the patch, three of four new real-render cases failed; after it, all four and the full 443-test suite passed. Astra independently reran the four cases, confirmed that the original clipped template now reports 163 missing header characters, and found no further mandatory issue.

The existing skill CI selector does not register the PPT suite, so the 443-test result is local evidence, not a claim that CI runs it. Earlier real Sonnet 4.6/medium trials verified authoring/build/publication plumbing but did **not** establish faster delivery at equal quality. The latest deterministic fixes have not had another paid model trial. No skill publication, production rollout or existing Agent config update is included.


---

## docs(skills): clarify runtime Bearer identity contract (#298)

- **SHA**: `8fc966226723885a0ca840c6dd5b3a2f486a7b04`
- **作者**: kaka-srp
- **日期**: 2026-10-21T03:49:43Z
- **PR**: #298

### Commit Message

```
docs(skills): clarify runtime Bearer identity contract (#298)

## Summary

Describe USER_INTERNAL_TOKEN as the platform-injected identity Bearer
credential in knowledge-base, ASR, TTS and meeting-notes. New Agents
receive opaque zrt_ credentials in that compatibility variable; existing
Agents may still receive a login JWT. Keep scripts, variable names,
frontmatter and authentication behavior unchanged.

Clarify Work-only knowledge-base authorization, Platform audio resource
isolation, and that opaque credentials must not be combined with a
shared proxy key. The meeting-notes text/skip-speaker paths retain their
LiteLLM-only prerequisites.

## Validation

- Targeted Skill schema lint and `git diff --check`.
- Documentation only; no script behavior or publication allowlist
changes. Audio scope behavior ships through [Proxy
#218](https://github.com/SerendipityOneInc/ecap-proxy-service/pull/218),
with default alignment in [CI
#4103](https://github.com/SerendipityOneInc/ecap-workspace/pull/4103),
and has passed real staging provider acceptance.


Feature source `384863c48cfdd24032b0bfafc24f4a874a045977` was published
directly to staging by [run
39411684523](https://github.com/SerendipityOneInc/ecap-skills/actions/runs/39411684523),
without merging. Workflow definition source is main, while actual
checkout/SOURCE_REF is this feature commit. Knowledge-base v2,
meeting-notes v4, zooclaw-asr v4 and zooclaw-tts v4 are published; the
scripts remain unchanged.

Actual Sandbox execution of the published TTS, ASR and speaker
enrollment scripts passed with new opaque identity credentials on CI
`d48073feb` / Proxy `92b97490`; private audio isolation and Work
KB/Platform denial also passed. Test resources were cleaned up.
Third-party/custom consumers and existing-Agent migration are not
covered by this documentation-only PR. No production publication in this
step.
```

### PR Body

## Summary

Describe USER_INTERNAL_TOKEN as the platform-injected identity Bearer credential in knowledge-base, ASR, TTS and meeting-notes. New Agents receive opaque zrt_ credentials in that compatibility variable; existing Agents may still receive a login JWT. Keep scripts, variable names, frontmatter and authentication behavior unchanged.

Clarify Work-only knowledge-base authorization, Platform audio resource isolation, and that opaque credentials must not be combined with a shared proxy key. The meeting-notes text/skip-speaker paths retain their LiteLLM-only prerequisites.

## Validation

- Targeted Skill schema lint and `git diff --check`.
- Documentation only; no script behavior or publication allowlist changes. Audio scope behavior ships through [Proxy #218](https://github.com/SerendipityOneInc/ecap-proxy-service/pull/218), with default alignment in [CI #4103](https://github.com/SerendipityOneInc/ecap-workspace/pull/4103), and has passed real staging provider acceptance.


Feature source `384863c48cfdd24032b0bfafc24f4a874a045977` was published directly to staging by [run 39411684523](https://github.com/SerendipityOneInc/ecap-skills/actions/runs/39411684523), without merging. Workflow definition source is main, while actual checkout/SOURCE_REF is this feature commit. Knowledge-base v2, meeting-notes v4, zooclaw-asr v4 and zooclaw-tts v4 are published; the scripts remain unchanged.

Actual Sandbox execution of the published TTS, ASR and speaker enrollment scripts passed with new opaque identity credentials on CI `d48073feb` / Proxy `92b97490`; private audio isolation and Work KB/Platform denial also passed. Test resources were cleaned up. Third-party/custom consumers and existing-Agent migration are not covered by this documentation-only PR. No production publication in this step.


---
