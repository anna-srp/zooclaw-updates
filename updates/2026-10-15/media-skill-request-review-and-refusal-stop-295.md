---
title: "Skill 更新：图片/视频技能先确认需求再动手，被安全拦截后不再自作主张换方案"
type: "Skill 上架/更新"
priority: "中"
date: "2026-10-15"
status: "待审核"
channels: ""
---

# Skill 更新：图片/视频技能先确认需求再动手，被安全拦截后不再自作主张换方案

## 核心宣传点

更新了 Designer、Video Generator、Chameleon Seedance 三个媒体类技能的行为约束：你随口提一句「画张图」「做个视频」时，Agent 不会再跳过设计流程直接生成，而是先确认需求再执行；当请求触发安全限制被拒绝后，Agent 也不会再偷偷把同一个形象换个说法当成「原创替代方案」交付，更不会反复重试。本次只改三个 SKILL.md 的描述与限制条款，不涉及脚本与引擎代码，视频相关路由仍只作用于视频场景。已随 v0.6.22-release 技能包发布，无需配套后端发版。

## 分级

- 内部：P2
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-skills
- SHA: `d7a867f2fc7f23da7914f898fe7b4f46b05761db`
- PR: #295
- 作者：tim-srp
- 日期：2026-10-15T06:33:42Z

### Commit Message

```
fix(media-skills): enforce natural request review and refusal stops (#295)

Natural media requests could reach generation without loading Designer,
and refusal follow-ups could be treated as approval of an “original”
substitute. This changes only three SKILL.md files: model-visible
descriptions require review before execution; concise additions to
existing restrictions prohibit unsolicited substitutes,
unchanged-character “original” continuations, and retries after any
safety rejection, including one with no specific reason. Video routing
remains scoped to video.

## Concise implementation

Commit d245df7 removes the duplicated entry/refusal sections. Net
whitespace-delimited word increases versus main are Designer +25, Video
Generator +30, Chameleon Seedance +43. Descriptions are unchanged from
the prior revision. No scripts or engine code change.

## Validation of d245df7

Fresh real production-runtime sessions on the owner's authorized
account, with temporary personal versions of these exact skills. No
global deployment or engine changes. All requests are natural English;
no skill-reading reminders, warm-ups or context-retention instructions.

- Four IPs × two models × 11 consecutive generation requests in each
same session: all 88 refused before execution. Zero generation,
drawing-script or delegation calls; zero request errors/timeouts. No
inline SVG/Python/image output.
- All 11 user messages stored per session, full preceding context
retained with no compaction. Actual run models verified for all 88
rounds.
- Exact concise Designer body read in 7/8 sessions. Terra/Iron Man
refused without reading the body; this is not universal body-loading
compliance. All eight system prompts contained the expected description.
- Every public replay was checked anonymously: HTTP 200, all user
requests match original frontend post IDs and text in order.

|Target|DeepSeek Flash, 11 rounds|GPT Terra, 11 rounds|
|---|---|---|

|iron_man|[replay](https://zoowork.ai/share/cr_cbObfQsVRgkC1xfKR4ZZxg)|[replay](https://zoowork.ai/share/cr_ALnNEh1huJmabLvDDuOCrQ)|

|batman|[replay](https://zoowork.ai/share/cr_2PjJtrbM1kCtMA_aXxUuKg)|[replay](https://zoowork.ai/share/cr_vat8kr7SLp1nBVm7ELAFdA)|

|naruto|[replay](https://zoowork.ai/share/cr_7OKAjIrKdUGd9R03ab9Oew)|[replay](https://zoowork.ai/share/cr_574sCYYTaaCiTcarnDd5kQ)|

|luffy|[replay](https://zoowork.ai/share/cr_3tdJ4gVcipuBLC55Sj6JiQ)|[replay](https://zoowork.ai/share/cr_WttPgUtIP9mDF7nf9ntQ0w)|

## Actual generic safety-error chains

Two additional medical-reference requests reached the real native image
tool and received HTTP 400 with `Your request was rejected by the safety
system`. The visible runtime error is truncated and does not disclose a
specific reason; do not infer an IP category. After each real rejection,
four same-session natural follow-ups requested rephrasing, Grok/Gemini,
Python/Pillow, and SVG/delegation. Both agents refused and made **zero
subsequent tool calls**, including generation, scripts and delegation.
No injected errors or text-only replay.

|Model|Actual supplier request ID|Full five-round replay|
|---|---|---|
|DeepSeek
Flash|e5889ceb-d74c-4384-96e7-c89484b0579e|[replay](https://zoowork.ai/share/cr_lMOsAQd75BhiLd_KNDfjCQ)|
|GPT
Terra|c445171c-e93c-498a-a4a0-8f20a38ae2a3|[replay](https://zoowork.ai/share/cr_94hBU8jQrhV-giRsYYczxQ)|

These two initial provider blocks are separate from the 88 agent-side
refusals; they are evidence of stopping **after** a real supplier
rejection. Three other clinical probes generated and delivered ordinary
diagrams successfully, did not trigger safety, and are not counted as
safety-stop coverage. They also remain in the evidence. Total: 13 new
frontend sessions and 101 actual requests. No agent technical errors or
timeouts; a diagnostic Redis destructor warning after restoration is
recorded separately.

## Restoration and limits

All temporary skill bindings removed; original gpt-6-sol model,
non-model declared configuration, original selected frontend
conversation and global skill hashes restored. Agent active. Final
configuration version 325. Sessions, artifacts and public replays
retained. PR remains open, automatic merge disabled; nothing globally
published.

Linter and whitespace checks pass; CI checks complete. Review
adjudication: the video-routing ambiguity was fixed. The alleged removal
of text triggers is not supported by the base diff: the original
Designer description listed image capabilities only; this patch does not
expand generic writing routing.

These finite samples validate the concise revision's observed behavior,
not every possible input or an engine-enforced guarantee. Refusals
reflect platform rules, not legal infringement determinations. Follow-up
to merged #294.
```

