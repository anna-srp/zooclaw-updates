---
title: "Agents 欢迎视频换新，PRO 角标与 Kimi 图标素材更新"
type: "体验优化"
priority: "低"
date: "2026-09-23"
status: "待审核"
channels: ""
---

# Agents 欢迎视频换新，PRO 角标与 Kimi 图标素材更新

## 核心宣传点

Agents 欢迎区的介绍视频替换为新的托管 MP4，移除了上一版的封面图，改为预加载 metadata，播放控件和布局保持不变。侧边栏 PRO 角标去掉了里面的 logo，显示高度收到 16px。首页模型区的 Kimi 图标换成了新的黑色 K 加蓝点素材。

## 分级

- 内部：P2
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary
- Update the Agents welcome video to the supplied hosted MP4, remove the previous video's poster, and preload metadata while keeping playback controls and layout.
- Remove the logo from the sidebar PRO badge and reduce its displayed height to 16px.
- Replace the homepage model section's Kimi icon with the supplied black K and blue dot artwork.

## Root cause
The interface used the previous introduction video and branding assets. This updates those assets and the PRO badge dimensions to the approved design.

## Test plan
- [x] Synced branch with main at cc4281f797.
- [x] Frontend governance checks, TypeScript, and targeted ESLint passed via scripts/verify-web.sh.
- [x] Related UserCard tests passed: 33 tests.
- [x] Asset size check and git diff --check passed.
- [x] Browser verified the Agents video loaded (107 seconds, no media error), the compact text-only PRO badge, and the new Kimi logo.

Frontend-only change. Local mock data and Firebase preview configuration are not included.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `43f8dd80ded88bf1528124acf4233425b2a12188`
- PR: #3883
- 作者：shana-srp
- 日期：2026-09-23T09:01:43Z

### Commit Message

```
fix(web): refresh agent video and brand badges (#3883)

## Summary
- Update the Agents welcome video to the supplied hosted MP4, remove the
previous video's poster, and preload metadata while keeping playback
controls and layout.
- Remove the logo from the sidebar PRO badge and reduce its displayed
height to 16px.
- Replace the homepage model section's Kimi icon with the supplied black
K and blue dot artwork.

## Root cause
The interface used the previous introduction video and branding assets.
This updates those assets and the PRO badge dimensions to the approved
design.

## Test plan
- [x] Synced branch with main at cc4281f797.
- [x] Frontend governance checks, TypeScript, and targeted ESLint passed
via scripts/verify-web.sh.
- [x] Related UserCard tests passed: 33 tests.
- [x] Asset size check and git diff --check passed.
- [x] Browser verified the Agents video loaded (107 seconds, no media
error), the compact text-only PRO badge, and the new Kimi logo.

Frontend-only change. Local mock data and Firebase preview configuration
are not included.

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

来源：SerendipityOneInc/ecap-workspace @ 43f8dd80，PR #3883，作者 shana-srp。