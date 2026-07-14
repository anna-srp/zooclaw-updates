# ecap-skills commits — 2026-07-13

共 5 个 commit

## fix(pptx): integrate native image search and strengthen E2E gates (#236)

- **SHA**: `ae32fbf5cd32b552d151dbdd7ab73bcb1b5a08d1`
- **作者**: sharplee-srp <sharplee@srp.one>
- **日期**: 2026-07-13T10:09:31Z
- **PR**: #236

### 完整 commit message

```
fix(pptx): integrate native image search and strengthen E2E gates (#236)

## Summary

- update the PPT skill to use the platform `web_image_search` tool for
visual discovery and keep source-policy decisions in the task workflow
- strengthen deck-spec, frame-map, render-QA, and QA-gate validation for
missing assets, template coverage, and dense table layouts

## Stack and runtime dependency

- stacked on #234 (`feat/pptx-runtime-image-fixes`)
- requires SerendipityOneInc/zooclaw-extras#178 for the
`web_image_search` tool
- the runtime image must package `@zooclaw/web-search@20260606.0.3`
before this skill is deployed

## Validation

- `uv run --with pytest --with python-pptx --with pillow pytest -q
pptx/tests/runtime` (143 passed)
- Ruff on all changed Python runtime and test files
- `git diff --check`
- fresh stagingbot + devcontainer run through Gateway on
`openclaw-docker:2026.6.11.5@sha256:1c16b6c6c27e0e6a4ed66fbed7dde8c0756fa2a5c4622546acad4ad1c7c8e1dd`

## E2E result

The fresh run completed a full PPT without host-side artifact repair.
The agent selected `web_image_search` naturally 32 times and made zero
browser calls; the previous summary-slide overlap was not reproduced.
Independent inspection still found source-provenance and requested
price-band gaps that the generic profile did not reject, so this PR does
not claim that the current washing-machine deck fully passes semantic
acceptance.
```

### 完整 PR body

## Summary

- update the PPT skill to use the platform `web_image_search` tool for visual discovery and keep source-policy decisions in the task workflow
- strengthen deck-spec, frame-map, render-QA, and QA-gate validation for missing assets, template coverage, and dense table layouts

## Stack and runtime dependency

- stacked on #234 (`feat/pptx-runtime-image-fixes`)
- requires SerendipityOneInc/zooclaw-extras#178 for the `web_image_search` tool
- the runtime image must package `@zooclaw/web-search@20260606.0.3` before this skill is deployed

## Validation

- `uv run --with pytest --with python-pptx --with pillow pytest -q pptx/tests/runtime` (143 passed)
- Ruff on all changed Python runtime and test files
- `git diff --check`
- fresh stagingbot + devcontainer run through Gateway on `openclaw-docker:2026.6.11.5@sha256:1c16b6c6c27e0e6a4ed66fbed7dde8c0756fa2a5c4622546acad4ad1c7c8e1dd`

## E2E result

The fresh run completed a full PPT without host-side artifact repair. The agent selected `web_image_search` naturally 32 times and made zero browser calls; the previous summary-slide overlap was not reproduced. Independent inspection still found source-provenance and requested price-band gaps that the generic profile did not reject, so this PR does not claim that the current washing-machine deck fully passes semantic acceptance.


---

## fix(pptx): harden official image handling (#234)

- **SHA**: `28ac76217a3b0fcd32829f7420d9cdce21421239`
- **作者**: sharplee-srp <sharplee@srp.one>
- **日期**: 2026-07-13T09:37:31Z
- **PR**: #234

### 完整 commit message

```
fix(pptx): harden official image handling (#234)

Stacked on #230.\n\nSummary:\n- tighten DeckSpec/frame-map/render QA
gates for consumer product decks and official product images\n- add
download-image helper support for compressed official image responses\n-
preserve aspect ratio for template image inserts via
image_fit=contain\n\nValidation:\n- uv run --with-requirements
pptx/requirements.txt python -m pytest pptx/tests/test_download_image.py
pptx/tests/shape_cli/test_shape_insert.py pptx/tests/test_shape_batch.py
pptx/tests/runtime/test_deck_spec.py
pptx/tests/runtime/test_frame_map.py pptx/tests/runtime/test_qa_gate.py
pptx/tests/runtime/test_render_qa.py
pptx/tests/runtime/test_template_starter.py\n- uv run
--with-requirements pptx/requirements.txt python
pptx/tests/check_links.py pptx\n- git diff --check
```

### 完整 PR body

Stacked on #230.\n\nSummary:\n- tighten DeckSpec/frame-map/render QA gates for consumer product decks and official product images\n- add download-image helper support for compressed official image responses\n- preserve aspect ratio for template image inserts via image_fit=contain\n\nValidation:\n- uv run --with-requirements pptx/requirements.txt python -m pytest pptx/tests/test_download_image.py pptx/tests/shape_cli/test_shape_insert.py pptx/tests/test_shape_batch.py pptx/tests/runtime/test_deck_spec.py pptx/tests/runtime/test_frame_map.py pptx/tests/runtime/test_qa_gate.py pptx/tests/runtime/test_render_qa.py pptx/tests/runtime/test_template_starter.py\n- uv run --with-requirements pptx/requirements.txt python pptx/tests/check_links.py pptx\n- git diff --check

---

## docs(pptx): wire zooclaw runtime workflow (#230)

- **SHA**: `fb84b038c3a394ade3cdc7689be00c4cbdf37ea1`
- **作者**: sharplee-srp <sharplee@srp.one>
- **日期**: 2026-07-13T09:33:59Z
- **PR**: #230

### 完整 commit message

```
docs(pptx): wire zooclaw runtime workflow (#230)

## Summary
- Wire the PPTX skill instructions to the Zooclaw runtime workflow.
- Add agent contracts, execution router, profile gates, and runtime
reference docs.
- Update link validation coverage for the newly linked reference
documents.

## Stack
1. Runtime core primitives.
2. Build/raw/render QA CLI: base branch for this PR.
3. This PR: skill-facing docs and routing instructions.

## Testing
- python3 pptx/tests/check_links.py pptx
- python3 -m pytest pptx/tests/runtime pptx/tests/test_shape_batch.py -q
- bash pptx/tests/smoke_test.sh

---------

Co-authored-by: sharp <sharpalgotrading@gmail.com>
```

### 完整 PR body

## Summary
- Wire the PPTX skill instructions to the Zooclaw runtime workflow.
- Add agent contracts, execution router, profile gates, and runtime reference docs.
- Update link validation coverage for the newly linked reference documents.

## Stack
1. Runtime core primitives.
2. Build/raw/render QA CLI: base branch for this PR.
3. This PR: skill-facing docs and routing instructions.

## Testing
- python3 pptx/tests/check_links.py pptx
- python3 -m pytest pptx/tests/runtime pptx/tests/test_shape_batch.py -q
- bash pptx/tests/smoke_test.sh


---

## feat(pptx): add runtime build and QA CLI (#229)

- **SHA**: `34add9f46851d82cf6444b40b5611552aa2fd429`
- **作者**: sharplee-srp <sharplee@srp.one>
- **日期**: 2026-07-13T09:24:24Z
- **PR**: #229

### 完整 commit message

```
feat(pptx): add runtime build and QA CLI (#229)

## Summary
- Add raw DeckSpec PPTX builder, RenderQA artifacts, QA gate evaluation,
and template inspection.
- Add the unified zooclaw_ppt_runtime.py CLI and runtime smoke coverage.
- Keep this stacked on the runtime core PR so reviewers only see
build/QA integration here.

## Stack
1. Runtime core primitives: base branch for this PR.
2. This PR: build/raw/render QA CLI.
3. Follow-up: SKILL.md and reference docs wiring.

## Testing
- python3 -m pytest pptx/tests/runtime pptx/tests/test_shape_batch.py -q
- python3 pptx/tests/check_links.py pptx
- bash pptx/tests/smoke_test.sh

---------

Co-authored-by: sharp <sharpalgotrading@gmail.com>
```

### 完整 PR body

## Summary
- Add raw DeckSpec PPTX builder, RenderQA artifacts, QA gate evaluation, and template inspection.
- Add the unified zooclaw_ppt_runtime.py CLI and runtime smoke coverage.
- Keep this stacked on the runtime core PR so reviewers only see build/QA integration here.

## Stack
1. Runtime core primitives: base branch for this PR.
2. This PR: build/raw/render QA CLI.
3. Follow-up: SKILL.md and reference docs wiring.

## Testing
- python3 -m pytest pptx/tests/runtime pptx/tests/test_shape_batch.py -q
- python3 pptx/tests/check_links.py pptx
- bash pptx/tests/smoke_test.sh


---

## feat(pptx): add runtime core primitives (#228)

- **SHA**: `751bf49e5f5c222f8928c417569e14a2d9114d88`
- **作者**: sharplee-srp <sharplee@srp.one>
- **日期**: 2026-07-13T09:11:27Z
- **PR**: #228

### 完整 commit message

```
feat(pptx): add runtime core primitives (#228)

## Summary
- Add DeckSpec validation/resolution and source manifest helpers.
- Add frame-map validation, shape-op emission, layout export, template
starter, and workspace path helpers.
- Extend shape_batch insert-image support used by template workflows.

## Stack
1. This PR: runtime core primitives.
2. Follow-up: build/raw/render QA CLI.
3. Follow-up: SKILL.md and reference docs wiring.

## Testing
- python3 -m pytest pptx/tests/runtime/test_deck_spec.py
pptx/tests/runtime/test_frame_map.py
pptx/tests/runtime/test_layout_export.py
pptx/tests/runtime/test_template_starter.py
pptx/tests/runtime/test_workspace.py pptx/tests/test_shape_batch.py -q

---------

Co-authored-by: sharp <sharpalgotrading@gmail.com>
```

### 完整 PR body

## Summary
- Add DeckSpec validation/resolution and source manifest helpers.
- Add frame-map validation, shape-op emission, layout export, template starter, and workspace path helpers.
- Extend shape_batch insert-image support used by template workflows.

## Stack
1. This PR: runtime core primitives.
2. Follow-up: build/raw/render QA CLI.
3. Follow-up: SKILL.md and reference docs wiring.

## Testing
- python3 -m pytest pptx/tests/runtime/test_deck_spec.py pptx/tests/runtime/test_frame_map.py pptx/tests/runtime/test_layout_export.py pptx/tests/runtime/test_template_starter.py pptx/tests/runtime/test_workspace.py pptx/tests/test_shape_batch.py -q


---
