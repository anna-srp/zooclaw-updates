---
title: "Council 新增 Deep Research 深度研究模式"
type: "新功能上线"
priority: "高"
外部: "A"
date: "2026-07-31"
status: "待审核"
channels: ""
---

## 核心宣传点

Council 页面现在支持全新的「Deep Research 深度研究」模式：在 Council | Deep Research 标签间一键切换，深度研究全程在 Council 内以实时线程呈现，并可将结果一键升级为完整对话继续追问。让复杂课题的多方研判更连贯、更省心。

## 原始内容

**feat(council): add deep research mode to council run API (#3162)**

- SHA: `8ee10766d32478f971f5f8614dee7fa19e208658`
- PR: #3162
- 日期: 2026-07-31T02:45:28Z

```
feat(council): add deep research mode to council run API (#3162)

## Summary
- Backend half of **Deep Research mode** on the `/council` page (spec:
`docs/superpowers/specs/2026-07-30-deep-research-mode-design.md`, plan
Tasks 1-3 of `docs/superpowers/plans/2026-07-30-deep-research-mode.md`).
No new routes, no new collections, no state-machine changes - council
behavior is unchanged.
- **`mode` discriminator** (`CouncilMode = "council" | "deep_research"`)
on `CouncilRunCreateRequest`, `CouncilRun`, and `CouncilRunResponse`. It
defaults to `"council"` everywhere, so existing clients and
already-stored run documents keep working untouched.
- **User-chosen `depth`** on the create request, accepted only when
`mode == "deep_research"`.
- **Deep-research runs are inert records.** `create_run` skips the
admission check for them and stores the run already terminal
(`state="done"`, `terminal_at=created_at`). The record exists for
history listing plus the run-folder link.
- **Run-folder link** reuses the existing `pod_status_run_id`, assigned
deterministically at creation as `deep-research-<run_id>`. The response
exposes a server-built `pod_folder` (`research/deep-research-<run_id>`).
- **`refresh`/`cancel` reject deep-research runs** with
`council.mode_unsupported`.

**Deploy ordering:** this PR must merge and deploy **before** the
frontend PR (`extra="forbid"` on the request).

## Test plan
- [x] New unit tests for mode/depth defaults and rejections, legacy
read-back, to_response projection, admission bypass, cancel/refresh
rejection.
- [x] `bash scripts/verify-py.sh` clean.
- [x] Full backend unit suite: **7165 passed**.
```

---

**feat(council): add deep research mode to council page (#3163)**

- SHA: `c3d6bd2e7cf65e7861cffd9e5ddfd16d96b31ede`
- PR: #3163
- 日期: 2026-07-31T04:40:27Z

```
feat(council): add deep research mode to council page (#3163)

## Summary
- Frontend half of **Deep Research mode** on the `/council` page.
- **Depends on #3162 - merge and deploy that first.**
- **Composer tabs** - `Council | Deep Research` at the top of the input
card, driven by a `MODE_CONFIG` map. The Council tab is byte-for-byte
the current experience.
- **Depth selector** on the Deep Research tab (`Quick` / `Standard`
(default) / `Deep`) with investigator-count and duration hints.
- **Dispatch flow**: create the session conversation, record the run
(`mode: 'deep_research'`, `depth`), post `/deep-research <depth>:
<topic>` plus the run-folder pin into the thread, navigate to that chat
thread. Chat is the whole experience.
- **History rail** lists both modes; deep-research entries are badged
and link to their chat thread.

## Test plan
- [x] New/updated unit tests for dispatch composition, mode switching,
depth selection, navigation, history-rail links, run-page notice.
- [x] `bash scripts/verify-web.sh` - **7518 passed**, 556 files.
```

---

**feat(council): keep deep research inside council (#3172)**

- SHA: `639005ad93351a357ccae97d2ec2f96a91722f61`
- PR: #3172
- 日期: 2026-07-31T09:31:12Z

```
feat(council): keep deep research inside council (#3172)

## Summary
- Keep Deep Research runs inside Council and render their live
Mattermost thread transcript there instead of redirecting to Chat.
- Remove the Deep Research reply composer and the duplicate `New
council` action; Council remains read-only while research is running.
- Make `Open full chat` promote the existing Mattermost thread into an
owner-scoped Chat conversation and navigate to Chat.
- Reuse existing conversation mappings by `root_post_id`; idempotent
registration across repeated clicks and duplicate-key races.

## Test plan
- [x] `bash scripts/verify-web.sh` - 166 Council tests + ESLint passed.
- [x] Backend Council/session-channel unit tests - 69 passed.
- [x] Import-linter - all 8 architecture contracts kept.

## Deployment
- Deploy `claw-interface` first, then `web/app`.
```

---

**feat(council): show the terminal thread synthesis (#3161)**

- SHA: `abd8542150515f5ff9e9076f2469541dcc1ed6a9`
- PR: #3161
- 日期: 2026-07-31T02:38:02Z

```
feat(council): show the terminal thread synthesis (#3161)

## Summary
- fetch and cache the dedicated Council run thread history
- render the latest eligible bot reply from the final `go` turn as the
terminal synthesis summary
- keep the shared Mattermost subscription active for the full bounded
15-second terminal window
- route Mattermost-hosted file links through the authenticated shared
preview sidebar

## Verification
- TypeScript passed; 306 selected tests passed; ESLint passed.
```
