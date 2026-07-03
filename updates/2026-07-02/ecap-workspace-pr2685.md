---
title: "修复 Windows 桌面版构建兼容问题，桌面端恢复可用"
type: "Bug Fix"
priority: "中"
date: "2026-07-02"
status: "待审核"
channels: ""
---
# 修复 Windows 桌面版构建兼容问题，桌面端恢复可用
## 核心宣传点
ZooClaw Windows 桌面版恢复正常构建与运行：修复跨平台命令兼容、白屏问题排查日志和平台识别，Windows 用户可以正常安装使用桌面端。
## 原始内容
### [ecap-workspace PR #2685]

fix(desktop): restore Windows ZooClaw build compatibility (#2685)

## Summary
- restore cross-platform shell command handling for OpenClaw node
commands
- rebrand the desktop package to ZooClaw and update desktop
icons/protocol metadata
- retry desktop window loading and log packaged Next server output to
aid Windows white-screen diagnosis
- report the real desktop platform in OpenClaw connect instead of
hardcoding darwin

## Verification
- Cherry-picked the four Windows/ZooClaw desktop commits onto the latest
origin/main
- Ran git diff --check successfully
- The corresponding zooclaw-desktop CI run 28360651111 succeeded and
produced a valid ZooClaw Setup 0.1.0.exe artifact from the previous
branch head

## Notes
- Local typecheck was not run in the temporary worktree because
desktop/node_modules is not installed there
- Follow-up zooclaw-desktop PR should point its ecap-workspace submodule
at this PR branch head

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

---

## PR Description

## Summary
- restore cross-platform shell command handling for OpenClaw node commands
- rebrand the desktop package to ZooClaw and update desktop icons/protocol metadata
- retry desktop window loading and log packaged Next server output to aid Windows white-screen diagnosis
- report the real desktop platform in OpenClaw connect instead of hardcoding darwin

## Verification
- Cherry-picked the four Windows/ZooClaw desktop commits onto the latest origin/main
- Ran git diff --check successfully
- The corresponding zooclaw-desktop CI run 28360651111 succeeded and produced a valid ZooClaw Setup 0.1.0.exe artifact from the previous branch head

## Notes
- Local typecheck was not run in the temporary worktree because desktop/node_modules is not installed there
- Follow-up zooclaw-desktop PR should point its ecap-workspace submodule at this PR branch head
