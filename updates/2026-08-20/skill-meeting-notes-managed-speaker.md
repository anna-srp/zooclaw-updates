---
title: "会议纪要 Skill 重大升级：托管说话人识别 + 音视频一键成稿"
type: "Skill 上架/更新"
priority: "高"
date: "2026-08-20"
status: "待审核"
channels: ""
---

# 会议纪要 Skill 重大升级：托管说话人识别 + 音视频一键成稿

## 核心宣传点

会议纪要（meeting-notes）Skill 完成一次能力级重构：说话人注册、分离与身份匹配全部改由平台托管服务完成，不再依赖本地模型和额外的 Hugging Face token，声纹数据也不会外泄；同时补上了一条真正可跑通的端到端流水线，音频、视频、纯文本会议都能直接生成纪要。短视频直接走原生解析，长视频会自动转码后处理。纪要质量也更严格：说话人没确认就保持匿名，日期、时间戳、结论都必须有原文依据，模型输出不完整时直接拒绝而不是产出半成品。单个文件超过 90 分钟仍需自行切分（建议每段 ≤85 分钟）。

## 原始内容

- 仓库: SerendipityOneInc/ecap-skills
- SHA: `55f34c3a213a0f3c6f01560b557e431a1a4ad270`
- PR: #268
- 作者: sharplee-srp
- 日期: 2026-08-20T08:06:00Z

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


