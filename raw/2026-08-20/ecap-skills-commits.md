# SerendipityOneInc/ecap-skills — commits 2026-08-20

## Update meeting-notes for managed speaker identification (#268)

- **SHA**: `55f34c3a213a0f3c6f01560b557e431a1a4ad270`
- **作者**: sharplee-srp
- **日期**: 2026-08-20T08:06:00Z
- **PR**: #268

### Commit Message

```
Update meeting-notes for managed speaker identification (#268)

## Summary

- replace local pyannote and Hugging Face speaker embeddings with
managed enrollment, diarization, and profile matching through
ecap-proxy-service
- add an executable media and text meeting-notes pipeline through the
OpenAI-compatible LiteLLM endpoint
- align the skill with the managed sandbox: read-only skill files,
workspace state, attachment materialization, durable artifacts, and
process polling
- add deterministic guards for confirmed speaker names, dates,
timestamps, evidence, entity aliases, incomplete model responses,
media-bound reusable speaker results, and all-or-nothing outputs
- keep all speaker enrollment and identification traffic behind
ecap-proxy-service; the skill never reads SPEAKER_SERVICE_URL or calls
Speechio directly

## Why

The previous skill had no repeatable end-to-end CLI, depended on local
pyannote models and an HF token, and documented a model/provider path
unavailable in the managed runtime. Model output could also promote
unconfirmed identities, guessed dates, normalized entities, or
incomplete actions into final minutes.

## Impact

Audio and video meetings now use the deployed speaker gateway without
exposing raw embeddings. Short MP4/WebM inputs use native video_url
through LiteLLM; larger video inputs are normalized to MP3 locally
before the LiteLLM call. Unconfirmed matches remain anonymous, speaker
failure degrades safely, concurrent profile mutations are serialized,
and invalid or truncated model output is rejected before artifacts are
committed.

Media longer than 90 minutes still needs to be split into chunks of at
most 85 minutes before processing.

## Validation

- python3 -m unittest discover -s meeting-notes/tests -q — 13 tests
passed
- python3 -S -m unittest discover -s meeting-notes/tests -q — local-only
paths passed without site packages; 3 network-client tests skipped
- Ruff and Python compilation passed
- repository skill lint passed
- managed registry validation and meeting-notes dry-run passed
- A102 devcontainer real-media E2E passed with 6 managed speaker labels
and 98 diarization segments; all final model calls finished with stop
- PR diff is 2,987 changed lines
- no test media, speaker results, transcripts, minutes, or credentials
are included in this PR
```

### PR Body

## Summary

- replace local pyannote and Hugging Face speaker embeddings with managed enrollment, diarization, and profile matching through ecap-proxy-service
- add an executable media and text meeting-notes pipeline through the OpenAI-compatible LiteLLM endpoint
- align the skill with the managed sandbox: read-only skill files, workspace state, attachment materialization, durable artifacts, and process polling
- add deterministic guards for confirmed speaker names, dates, timestamps, evidence, entity aliases, incomplete model responses, media-bound reusable speaker results, and all-or-nothing outputs
- keep all speaker enrollment and identification traffic behind ecap-proxy-service; the skill never reads SPEAKER_SERVICE_URL or calls Speechio directly

## Why

The previous skill had no repeatable end-to-end CLI, depended on local pyannote models and an HF token, and documented a model/provider path unavailable in the managed runtime. Model output could also promote unconfirmed identities, guessed dates, normalized entities, or incomplete actions into final minutes.

## Impact

Audio and video meetings now use the deployed speaker gateway without exposing raw embeddings. Short MP4/WebM inputs use native video_url through LiteLLM; larger video inputs are normalized to MP3 locally before the LiteLLM call. Unconfirmed matches remain anonymous, speaker failure degrades safely, concurrent profile mutations are serialized, and invalid or truncated model output is rejected before artifacts are committed.

Media longer than 90 minutes still needs to be split into chunks of at most 85 minutes before processing.

## Validation

- python3 -m unittest discover -s meeting-notes/tests -q — 13 tests passed
- python3 -S -m unittest discover -s meeting-notes/tests -q — local-only paths passed without site packages; 3 network-client tests skipped
- Ruff and Python compilation passed
- repository skill lint passed
- managed registry validation and meeting-notes dry-run passed
- A102 devcontainer real-media E2E passed with 6 managed speaker labels and 98 diarization segments; all final model calls finished with stop
- PR diff is 2,987 changed lines
- no test media, speaker results, transcripts, minutes, or credentials are included in this PR


---

## fix(publish): production 强制同步 v2 global skills (#269)

- **SHA**: `1c96ba3fc88052e71444938d16e550844dd7eca3`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-20T07:33:34Z
- **PR**: #269

### Commit Message

```
fix(publish): production 强制同步 v2 global skills (#269)

## 背景

production 已上线 v2 Engine，但当前 skills registry 中 global skill 为 0；同一套
staging 环境已有 17 个 active global skills、5 个 deprecated global skills。

根因是 production publish workflow 仍保留上线前的 `SKILLS_V2_SYNC_ENABLED`
总闸。production GitHub Environment 未配置该变量时，release 只发布 V1 S3 内容并以 warning
跳过 v2 registry，导致 workflow 成功但新 Agent 没有系统 global skills。

## 改动

1. 移除 production 的可选总闸和 skip 分支。
2. production 与 staging 一样，强制执行 allowlist 校验、registry publish 和
reconcile。
3. registry URL/token 缺失时，在 S3 `--delete` 之前 fail fast，避免部分发布。
4. 更新 README 和 `PUBLISHED_SKILLS_V2`，明确 staging/production 的双环境契约。

## 验证

- `PUBLISH_BASE_URL=https://example.invalid PUBLISH_TOKEN=test node
.github/scripts/sync-v2-registry.mjs --validate`
- `actionlint -ignore 'label ".*" is unknown'
.github/workflows/publish-skills.yml`
- `git diff --check`
- `python3 .github/scripts/lint_skills.py`（通过；12 条既有 warning）

## Rollout checklist

合并后、触发 production publish 前，需要人工配置 GitHub Environment `production`：

- Variable `SKILLS_PUBLISH_BASE_URL=https://clawapi.ecap.gsmo.ai`
- Secret `SKILLS_PUBLISH_TOKEN`，值与 production claw-interface 的
`AGENT_STUDIO_PACK_UPDATE_TOKEN` 相同

随后手动 dispatch `Publish Skills`，选择 `production`、`ref=main`，完成现有 17 个
global skills 的首次 backfill/reconcile。未完成上述配置前，production publish 会按本 PR
的预期 fail fast。
```

### PR Body

## 背景

production 已上线 v2 Engine，但当前 skills registry 中 global skill 为 0；同一套 staging 环境已有 17 个 active global skills、5 个 deprecated global skills。

根因是 production publish workflow 仍保留上线前的 `SKILLS_V2_SYNC_ENABLED` 总闸。production GitHub Environment 未配置该变量时，release 只发布 V1 S3 内容并以 warning 跳过 v2 registry，导致 workflow 成功但新 Agent 没有系统 global skills。

## 改动

1. 移除 production 的可选总闸和 skip 分支。
2. production 与 staging 一样，强制执行 allowlist 校验、registry publish 和 reconcile。
3. registry URL/token 缺失时，在 S3 `--delete` 之前 fail fast，避免部分发布。
4. 更新 README 和 `PUBLISHED_SKILLS_V2`，明确 staging/production 的双环境契约。

## 验证

- `PUBLISH_BASE_URL=https://example.invalid PUBLISH_TOKEN=test node .github/scripts/sync-v2-registry.mjs --validate`
- `actionlint -ignore 'label ".*" is unknown' .github/workflows/publish-skills.yml`
- `git diff --check`
- `python3 .github/scripts/lint_skills.py`（通过；12 条既有 warning）

## Rollout checklist

合并后、触发 production publish 前，需要人工配置 GitHub Environment `production`：

- Variable `SKILLS_PUBLISH_BASE_URL=https://clawapi.ecap.gsmo.ai`
- Secret `SKILLS_PUBLISH_TOKEN`，值与 production claw-interface 的 `AGENT_STUDIO_PACK_UPDATE_TOKEN` 相同

随后手动 dispatch `Publish Skills`，选择 `production`、`ref=main`，完成现有 17 个 global skills 的首次 backfill/reconcile。未完成上述配置前，production publish 会按本 PR 的预期 fail fast。


---
