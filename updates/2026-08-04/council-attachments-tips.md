---
title: "Council 圆桌支持上传文件附件，深度/档位新增直观说明"
type: "新功能上线"
priority: "中"
date: "2026-08-04"
status: "待审核"
channels: ""
commit: "f0fe91a810c4aaf78c0c138a3bb2a717f6258a6a"
repo: "SerendipityOneInc/ecap-workspace"
---

## 核心宣传点

Council/Deep-Research 讨论现在可以直接附上文件一起提问；同时 Depth 和 Tier 选项下新增说明提示（如 quick/standard/deep 对应 3/4/5 位成员、各档位代表模型），选择不再靠猜。

## 原始内容

```
feat(council): composer depth/tier tips and file attachments (#3222)

## Linear
<!-- no Linear issue for this change -->

## Summary
- Add explanatory tips under the Council composer's Depth and Tier rows.
Depth tips give the council size per depth (quick/standard/deep = 3/4/5
members, Auto = the skill classifies the topic); tier tips name each
tier's representative models with a "Latest" suffix to signal the skill
resolves each series to the newest version on the pod (e.g. "Mid-class
models · Claude Sonnet Latest, GPT Terra Latest, Gemini Flash Latest… ·
the balanced default."). Copy is grounded in `ecap-skills/council`
(`SKILL.md` + `roster.py` tier lineups / `SEATS_BY_DEPTH`).
- Add file attachments to the Council/Deep-Research composer: paperclip
button + pending-attachment chips (name · size · remove) with the
Mattermost per-post file cap enforced. On dispatch, files upload to the
run thread's channel via the existing `uploadMattermostAttachment`
helper (HEIC normalization + image-downscale retries), and the topic
post carries their `file_ids` — `postThreadReply` gains an optional
`fileIds` pass-through to `sendPost`. Protocol messages (`go` / `cancel`
/ tier tokens) never attach files. Upload failure aborts the dispatch
post and keeps the files for retry; success clears them.
- Map the `--chat-ui-*` CSS variables to app semantic tokens on the
chips container so `AttachmentChip` follows the app theme (its built-in
fallbacks are light-mode colors, which rendered unreadable chips in dark
mode).
- Design note: a per-model selection picker was explored and specced
during review but deliberately dropped in favor of the simpler tips
(`docs/superpowers/specs/2026-08-04-council-composer-attachments.md`
documents the attachment design; the picker never landed on this
branch).

## Test plan
- [x] Unit: tip rendering + selection swaps, attach button/chips
add-remove/cap, dispatch carries `file_ids` on council and deep-research
paths, upload-failure aborts the post, `postThreadReply` file-id
forwarding (council suite green)
- [x] `bash scripts/verify-web.sh` — guards, tsc, vitest (8050 tests),
eslint all green; coverage thresholds pass
- [x] Manual (mock stack + Chrome): tips swap across all depth/tier
pills; attach → chips render with correct dark-theme contrast → remove
works
- [ ] Staging (post-merge): dispatch a council run with attachments and
confirm the skill sees the files in the run thread (skill contract does
not formalize attachments yet — noted in the spec)

---

### PR Body

## Linear
<!-- no Linear issue for this change -->

## Summary
- Add explanatory tips under the Council composer's Depth and Tier rows. Depth tips give the council size per depth (quick/standard/deep = 3/4/5 members, Auto = the skill classifies the topic); tier tips name each tier's representative models with a "Latest" suffix to signal the skill resolves each series to the newest version on the pod (e.g. "Mid-class models · Claude Sonnet Latest, GPT Terra Latest, Gemini Flash Latest… · the balanced default."). Copy is grounded in `ecap-skills/council` (`SKILL.md` + `roster.py` tier lineups / `SEATS_BY_DEPTH`).
- Add file attachments to the Council/Deep-Research composer: paperclip button + pending-attachment chips (name · size · remove) with the Mattermost per-post file cap enforced. On dispatch, files upload to the run thread's channel via the existing `uploadMattermostAttachment` helper (HEIC normalization + image-downscale retries), and the topic post carries their `file_ids` — `postThreadReply` gains an optional `fileIds` pass-through to `sendPost`. Protocol messages (`go` / `cancel` / tier tokens) never attach files. Upload failure aborts the dispatch post and keeps the files for retry; success clears them.
- Map the `--chat-ui-*` CSS variables to app semantic tokens on the chips container so `AttachmentChip` follows the app theme (its built-in fallbacks are light-mode colors, which rendered unreadable chips in dark mode).
- Design note: a per-model selection picker was explored and specced during review but deliberately dropped in favor of the simpler tips (`docs/superpowers/specs/2026-08-04-council-composer-attachments.md` documents the attachment design; the picker never landed on this branch).

## Test plan
- [x] Unit: tip rendering + selection swaps, attach button/chips add-remove/cap, dispatch carries `file_ids` on council and deep-research paths, upload-failure aborts the post, `postThreadReply` file-id forwarding (council suite green)
- [x] `bash scripts/verify-web.sh` — guards, tsc, vitest (8050 tests), eslint all green; coverage thresholds pass
- [x] Manual (mock stack + Chrome): tips swap across all depth/tier pills; attach → chips render with correct dark-theme contrast → remove works
- [ ] Staging (post-merge): dispatch a council run with attachments and confirm the skill sees the files in the run thread (skill contract does not formalize attachments yet — noted in the spec)

```
