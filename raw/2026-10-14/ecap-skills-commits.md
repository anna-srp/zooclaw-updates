# SerendipityOneInc/ecap-skills — commits 2026-10-14

## fix(media-skills): harden unnamed character restrictions (#294)

- **SHA**: `f2eb7a4e06d4628eb8a4e7a9c8f6de0202c08f4e`
- **作者**: tim-srp
- **日期**: 2026-10-14T17:01:24Z
- **PR**: #294

### Commit Message

```
fix(media-skills): harden unnamed character restrictions (#294)
```

### PR Body

Strengthen Designer, Video Generator, and Chameleon rules against unnamed character requests assembled from recognizable visual features. Add combined-appearance checks, synonym normalization, Chinese reinforcement, and review of follow-up costume changes and prior suggested alternatives. Preserve terminal handling of provider safety/moderation refusals. Only skill documents change; no engine changes.

Validation:
- Skill lint passed (11 existing warnings); selector tests passed 3/3; diff whitespace check passed.
- Real production agent with seed-2.0-mini and personal skill revision 9: all seven single-turn negative cases refused without generation, execution, or attachments; English three-turn case refused; ordinary field-mouse control generated an attachment.
- **Remaining failure:** Chinese three-turn case still emitted both refusal text and a Gemini image_generate call in the same assistant message. The call completed and created an image attachment. Renaming the animal while preserving the restricted feature combination still bypasses the instructions. This PR must not be treated as a complete fix or proof of reliable enforcement.
- Test model restored to gpt-6-sol and temporary skill bindings removed. No global rollout, merge, or engine modification performed.

The current tests cover the pre-generation recognizability gate. The failing latest case did not receive a provider safety error, so it is not evidence of retrying after a provider refusal. Earlier real provider safety-stop tests are a separate boundary.

## Follow-up fixes after independent review

The description above records the original documentation-only revision and its production observations. This follow-up also changes repository CLI error handling; it does not fix or verify the reported native image_generate Chinese multi-turn refusal-plus-tool-call failure.

- Designer CLI classifies sanitized terminal safety refusals across Grok generation/edit, GPT generation/edit, and Gemini responses/exceptions. Nested safety and success-response filtering stop the request; ambiguous empty or unknown rejection codes fail closed. Only confirmed technical errors retain the intended Grok quality-to-base fallback. Failure now exits 1 and emits a sanitized error envelope on stderr; successful stdout paths are unchanged.
- PPTX/web-designer direct routes must read Designer's authoritative preflight before any CLI call, including execution-ready prompts and visual references; PDF's full-contract route is unchanged.
- Chameleon restores the common copyright/portrait/trademark rights notice for all image/video/audio references, including first/last frames and edit/extend. Moderation errors no longer suggest asset onboarding; legitimate onboarding is a separate explicitly authorized provider-supported workflow.
- Descriptions retain useful routing capabilities without unsupported video-generator editing; policies distinguish strict character restrictions from legal findings, generic/public-domain/original inputs, styles/logos, endorsement and consent. No legal certification or immunity is claimed.

Validation on the follow-up commit (local Claude Code Opus 5.5 implementation plus independent rerun; no live provider calls or installs):
- Existing Anaconda PyYAML skill lint: passed, 11 pre-existing warnings.
- Selector tests: 3/3; existing Chameleon tests: 24/24.
- New offline Designer mocked-transport tests: 64/64; structural/path tests: 19/19; Chameleon safety tests: 21/21. These are non-overlapping suites (128 Python tests total), not behavioral agent evaluations.
- Nested content_policy_violation makes exactly one provider attempt; confirmed technical failures preserve fallback; ordinary success remains supported. git diff --check passed.
- Follow-up AutoReview identified an incidental prompt-echo false positive in Chameleon: repaired with structured error-field classification and explicit rejection wording, plus mocked HTTP/task regressions. Native-tool Chinese bypass and the separate video-generator raw error_message contract remain documented limitations, not claims of repair.
- Static scenario checklist is explicitly NOT behavioral proof. Native image_generate, real production/model recognizability, other provider CLIs, and legal outcomes remain outside this validation. New offline suites are not wired into the shared CI selector in this scoped patch.


---
