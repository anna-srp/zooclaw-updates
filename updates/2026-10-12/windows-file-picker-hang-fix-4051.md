---
title: "修复：Windows 上点聊天附件的文件类型下拉会卡死 Edge，现在改为直接「所有文件」"
type: "Bug Fix"
priority: "高"
date: "2026-10-12"
status: "待审核"
channels: ""
---

# 修复：Windows 上点聊天附件的文件类型下拉会卡死 Edge，现在改为直接「所有文件」

## 核心宣传点

有用户反馈在 Windows 上打开聊天附件选择器后，悬停或点击系统自带的「文件类型」下拉会直接把 Edge 卡死，连文件都选不了。原因是聊天的 accept 列表包含图片/音视频通配符加一堆文档与压缩包扩展名，Chromium 会展开成超长筛选项，在跨不同 DPI 缩放的多显示器场景触发已知卡死问题。现在 Windows 上打开前会同步移除 accept，直接以「所有文件」打开，其他平台筛选行为不变，上传仍校验大小和数量。

## 分级

- 内部：P1
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## 备注

属于匹配到的上游已知失效模式，并非对该用户机器的确诊：对方的显示器配置与 Windows/Edge 版本尚未提供。本改动不新增文件类型校验。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `115f5c10e987fd243f06ddebfa35b939599dbfa5`
- PR: #4051
- 作者：siqiao-srp
- 日期：2026-10-12T08:05:24Z

### Commit Message

```
fix(chat-ui): avoid Windows file-type dropdown hang (#4051)

## Summary
- On Windows, open the chat attachment picker with All files instead of
the long Custom Files filter. A user reported that hovering/clicking the
native file-type dropdown freezes Edge before selecting or uploading a
file.
- Remove the accept attribute synchronously before opening the picker;
retain existing filters on other platforms and preserve attachment
callbacks and disabled/uploading guards.
- This applies to all Windows chat-composer pickers. The existing upload
handlers continue to check size/count; this change does not add
file-type validation. The original native picker already offered All
files.

## Root cause
The chat accept list contains image/audio/video wildcards plus
document/archive extensions. Chromium expands these into a long native
filter. Mozilla bug 1881950 documents the same dropdown/tooltip hang in
Edge and Chromium when the resulting window crosses monitors with
different DPI scaling:
https://bugzilla.mozilla.org/show_bug.cgi?id=1881950#c9

This is a matching upstream failure mode, not a confirmed diagnosis of
the customer's machine: monitor configuration and Windows/Edge versions
have not yet been supplied. The patch avoids that filter path and needs
native Windows validation before production release.

## Test plan
- [x] Composer regression suite: 54 tests passed.
- [x] Chat UI TypeScript and targeted ESLint checks passed.
- [x] Real Chrome on macOS: 30 repeated ZIP+PNG selections across
Windows, macOS, and Android user-agent scenarios; default/custom
actions, changed accept prop, input reset, and disabled/uploading guards
passed. Platform identities were simulated and filechooser events
intercepted; these tests do not exercise native Windows dialogs or
backend upload delivery.
- [x] Deployed commit 0f2e22c to staging; /api/version confirms the
revision and the page returns HTTP 200.
- [ ] On the affected Windows Edge machine, repeatedly hover/click the
All files dropdown, including near monitor boundaries, then upload the
original ZIPs and an image and send the message.

Staging: https://ecap.gensmo.nosay.live/
Deployment:
https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/38031648866
```

