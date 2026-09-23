---
title: "ZooWork 登录页改版：双栏布局、新 Logo 与循环播放的品牌视频"
type: "体验优化"
priority: "中"
date: "2026-09-22"
status: "待审核"
channels: ""
---

# ZooWork 登录页改版：双栏布局、新 Logo 与循环播放的品牌视频

## 核心宣传点

独立登录页重做成响应式双栏布局，用上了 ZooWork 横版 Logo 和本地托管的 GFS Didot 衬线标题字体，表单的间距、边框和阴影都重新收拾过。右侧加了一段竖版品牌视频，静音循环播放、不显示播放器控件，页面切到后台或滚出视口时自动暂停，并且尊重系统的「减少动态效果」偏好（新旧 Safari 的媒体查询监听都做了兼容）。样式只作用在这个独立登录卡片上，原有文案、认证流程和站内共享的登录弹窗外观都没变。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary

- Redesign the standalone login page with a responsive two-column
layout, the ZooWork horizontal logo, locally hosted GFS Didot headings,
and refined form spacing, borders, and shadows.
- Add the supplied portrait video and matching poster. The video plays
muted in a loop without player controls, pauses when hidden or
offscreen, and respects reduced-motion preferences with modern and
legacy Safari media-query listeners.
- Scope the form styling to the standalone login card while preserving
the existing copy, authentication flows, and shared login dialog
appearance.

## Test plan

- [x] Frontend governance checks, TypeScript, 86 targeted unit tests
across 4 files, and ESLint via `scripts/verify-web.sh`.
- [x] Reproduce the legacy Safari listener crash before the fix; verify
playback, reduced-motion changes, visibility changes, and listener
cleanup for both media-query APIs after the fix.
- [x] Check desktop and mobile layouts in the local mock preview.
- [x] Verify video autoplay, looping, mute, playback rate, and absence
of player controls in the browser.
- [x] Check asset sizes and font license; the optimized MP4 is below the
2 MB asset limit.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `9379d083ab36e7340b1dfef62f0a0a88a6c4bd9f`
- PR: #3843
- 作者：shana-srp
- 日期：2026-09-22T06:01:46Z

### Commit Message

```
style(auth): redesign ZooWork login page (#3843)

## Summary

- Redesign the standalone login page with a responsive two-column
layout, the ZooWork horizontal logo, locally hosted GFS Didot headings,
and refined form spacing, borders, and shadows.
- Add the supplied portrait video and matching poster. The video plays
muted in a loop without player controls, pauses when hidden or
offscreen, and respects reduced-motion preferences with modern and
legacy Safari media-query listeners.
- Scope the form styling to the standalone login card while preserving
the existing copy, authentication flows, and shared login dialog
appearance.

## Test plan

- [x] Frontend governance checks, TypeScript, 86 targeted unit tests
across 4 files, and ESLint via `scripts/verify-web.sh`.
- [x] Reproduce the legacy Safari listener crash before the fix; verify
playback, reduced-motion changes, visibility changes, and listener
cleanup for both media-query APIs after the fix.
- [x] Check desktop and mobile layouts in the local mock preview.
- [x] Verify video autoplay, looping, mute, playback rate, and absence
of player controls in the browser.
- [x] Check asset sizes and font license; the optimized MP4 is below the
2 MB asset limit.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

来源：SerendipityOneInc/ecap-workspace @ 9379d083，PR #3843，作者 shana-srp。
