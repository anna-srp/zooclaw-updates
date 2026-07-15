# ecap-skills commits — 2026-07-14

## chore(pptx): bump skill version to 1.2 (#239)
- sha: `1438b919e1b46b3d3e7b074724e3ce38e792fa62`
- 作者: sharplee-srp
- 日期: 2026-07-14T07:49:31Z
- PR: #239 by sharplee-srp — https://github.com/SerendipityOneInc/ecap-skills/pull/239

**Commit message:**

```
chore(pptx): bump skill version to 1.2 (#239)

## Summary

- bump the PPTX skill metadata version from `1.1` to `1.2`
- align the skill version with the recently merged PPTX runtime updates

## Validation

- `git diff --check`
- `python3 .github/scripts/lint_skills.py`
```

**PR body:**

## Summary

- bump the PPTX skill metadata version from `1.1` to `1.2`
- align the skill version with the recently merged PPTX runtime updates

## Validation

- `git diff --check`
- `python3 .github/scripts/lint_skills.py`

---

## fix(pptx): preserve generic contracts and decorations (#238)
- sha: `3f110e42f0ac378b35b825928b4ff20eb1a4b646`
- 作者: sharplee-srp
- 日期: 2026-07-14T06:55:25Z
- PR: #238 by sharplee-srp — https://github.com/SerendipityOneInc/ecap-skills/pull/238

**Commit message:**

```
fix(pptx): preserve generic contracts and decorations (#238)

## Summary

- preserve backward-compatible `generic` behavior when DeckSpec v1 omits
`profile`; strict provenance remains enabled for explicit
`consumer-retail`
- distinguish product identity from analysis text while preserving all
established DeckSpec analysis fields
- validate `image_fit: "contain"` against the source image's real aspect
ratio
- prevent missing declared product assets and stale template pictures
from satisfying visual coverage
- clear stale template-inspection artifacts and record partial
shape-operation failures in `qa-report.json`
- document every supported profile and fix the DeckSpec runtime path
- treat sub-0.5-inch accents as decoration while keeping compact content
callouts in the sibling-panel gate
- allow larger retained decorations only when the source shape name
starts with `[decorative]` and its id is also listed in
`decorative_shape_ids`; either signal alone cannot suppress a content
panel

## Why

The final reviews across #228, #229, #230, #234, and #236 identified
several runtime and documentation gaps. This follow-up closes the
remaining findings without weakening explicit consumer-retail
provenance, declared-asset matching, or sibling-panel coverage.

## Validation

- `pytest -q tests/runtime` from `pptx/` — 194 passed
- `python3 pptx/tests/check_links.py pptx` — 60 links passed
- `bash pptx/tests/smoke_test.sh` — 6 passed, 0 failed, 10
environment-dependent skips
- `git diff --check`
- independent Standards review — no findings
- independent Spec review — no remaining gaps before the latest GitHub
review follow-ups; each subsequent finding received a focused regression
test

## Decoration contract

For product-profile template slides:

- shapes with either side below 0.5 inch are treated as accents because
they cannot hold readable product analysis content;
- other empty `AUTO_SHAPE` rectangles remain protected content-panel
candidates;
- to retain a larger decoration, rename the source template shape with
the exact `[decorative]` prefix and list the same source shape id in
`decorative_shape_ids`;
- missing ids, invalid ids, or ids pointing to shapes without the prefix
fail validation.

## Review context

Follow-up to the stacked PPT runtime PRs and their final
`gpt:need-human-review` findings.
```

**PR body:**

## Summary

- preserve backward-compatible `generic` behavior when DeckSpec v1 omits `profile`; strict provenance remains enabled for explicit `consumer-retail`
- distinguish product identity from analysis text while preserving all established DeckSpec analysis fields
- validate `image_fit: "contain"` against the source image's real aspect ratio
- prevent missing declared product assets and stale template pictures from satisfying visual coverage
- clear stale template-inspection artifacts and record partial shape-operation failures in `qa-report.json`
- document every supported profile and fix the DeckSpec runtime path
- treat sub-0.5-inch accents as decoration while keeping compact content callouts in the sibling-panel gate
- allow larger retained decorations only when the source shape name starts with `[decorative]` and its id is also listed in `decorative_shape_ids`; either signal alone cannot suppress a content panel

## Why

The final reviews across #228, #229, #230, #234, and #236 identified several runtime and documentation gaps. This follow-up closes the remaining findings without weakening explicit consumer-retail provenance, declared-asset matching, or sibling-panel coverage.

## Validation

- `pytest -q tests/runtime` from `pptx/` — 194 passed
- `python3 pptx/tests/check_links.py pptx` — 60 links passed
- `bash pptx/tests/smoke_test.sh` — 6 passed, 0 failed, 10 environment-dependent skips
- `git diff --check`
- independent Standards review — no findings
- independent Spec review — no remaining gaps before the latest GitHub review follow-ups; each subsequent finding received a focused regression test

## Decoration contract

For product-profile template slides:

- shapes with either side below 0.5 inch are treated as accents because they cannot hold readable product analysis content;
- other empty `AUTO_SHAPE` rectangles remain protected content-panel candidates;
- to retain a larger decoration, rename the source template shape with the exact `[decorative]` prefix and list the same source shape id in `decorative_shape_ids`;
- missing ids, invalid ids, or ids pointing to shapes without the prefix fail validation.

## Review context

Follow-up to the stacked PPT runtime PRs and their final `gpt:need-human-review` findings.


---

