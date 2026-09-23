---
title: "Agents 欢迎页新增产品介绍视频，替换原「敬请期待」占位"
type: "新功能上线"
priority: "中"
date: "2026-09-22"
status: "待审核"
channels: ""
---

# Agents 欢迎页新增产品介绍视频，替换原「敬请期待」占位

## 核心宣传点

Agents 欢迎页上那块写着「Video coming soon」的占位区换成了正式的产品介绍视频。响应式布局保持不变，新增了原生播放控件、内联播放、封面图和本地化的无障碍标签。播放需要用户主动点击（preload="none"，不会偷跑流量）。完整的 65 秒视频含音轨和内嵌字幕，以 H.264/AAC 编码、960×540、约 1.5 MB。

## 分级

- 内部：P1
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

Replaces the Agents welcome screen's “Video coming soon” placeholder
with the supplied introduction video. Keeps the existing responsive
layout and adds native playback controls, inline playback, a poster, and
localized accessible labels. Playback is user-initiated with
`preload="none"`.

The complete 65-second video, including audio and embedded subtitles, is
encoded as H.264/AAC at 960×540 (~1.5 MB), below the repository's 2 MB
asset limit. Only frontend deployment is needed. The temporary local
preview route is not included.

Validation:
- Web governance guards, TypeScript, and ESLint passed.
- Local browser preview rendered the welcome screen and video controls.
- Full video decode completed without errors; sampled frame checked for
readability.

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `2566059311d65838521cc0c11ad40e6b294e372a`
- PR: #3862
- 作者：shana-srp
- 日期：2026-09-22T09:30:13Z

### Commit Message

```
feat(agents): add introduction video to welcome screen (#3862)

Replaces the Agents welcome screen's “Video coming soon” placeholder
with the supplied introduction video. Keeps the existing responsive
layout and adds native playback controls, inline playback, a poster, and
localized accessible labels. Playback is user-initiated with
`preload="none"`.

The complete 65-second video, including audio and embedded subtitles, is
encoded as H.264/AAC at 960×540 (~1.5 MB), below the repository's 2 MB
asset limit. Only frontend deployment is needed. The temporary local
preview route is not included.

Validation:
- Web governance guards, TypeScript, and ESLint passed.
- Local browser preview rendered the welcome screen and video controls.
- Full video decode completed without errors; sampled frame checked for
readability.

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

来源：SerendipityOneInc/ecap-workspace @ 25660593，PR #3862，作者 shana-srp。
