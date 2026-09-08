---
title: "修复：雇 BossClaw 一直卡在「Agent 环境仍在构建中」"
type: "Bug Fix"
priority: "高"
date: "2026-09-07"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：雇 BossClaw 一直卡在「Agent 环境仍在构建中」

## 核心宣传点

想雇 BossClaw（老板专属幕僚长）的用户会一直被挡在「Agent environment is still building / Agent 环境仍在构建中」这句提示上，等多久都不会好——环境其实每次都构建失败了。

根因在依赖安装这一层。Agent Pack 在 `dependencies.bins` 里声明的是**可执行命令名**，而不是系统软件包名，后端负责把命令名翻译成对应的 apt 包。这个映射表此前只处理了一个特例（`ffprobe` → `ffmpeg`），其余命令名都被原样当成包名丢给 apt。BossClaw 用到字体处理，声明了 `fc-scan` 和 `fc-cache` 两个命令——apt 上并不存在这两个包，安装直接报 `Unable to locate package`，整个环境构建随之失败。

现在把 `fc-scan` 和 `fc-cache` 都映射到真实存在的 `fontconfig` 包，走已有的包去重逻辑，两个命令合并成一次安装。受影响的用户重新雇一次即可正常完成环境构建。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `538d8443`
- PR: #3663
- 日期: 2026-09-07

### Commit Message

```
fix(agents): map fontconfig binaries to apt package (#3663)

## Summary

BossClaw hire fails with "Agent environment is still building" because
its Environment build tries to install nonexistent apt packages
`fc-scan` and `fc-cache`. Map both commands to `fontconfig`, which the
existing package deduplication emits once.

## Root cause

Pack `dependencies.bins` declares executable names. The backend maps
known executables to their apt packages, but previously only handled
`ffprobe` → `ffmpeg`; the fontconfig commands passed through as package
names and failed with `Unable to locate package`.

## Test plan

- [x] Extended the existing archive translation test for both legacy and
strict dependency modes; both cases failed before the mapping fix and
passed afterward.
- [x] Pack translation test file: 75 passed, including package
deduplication and preservation of other dependencies.
```

## 备注

发布状态：已合并待发版（尚未包含在最新的正式发布 tag 中）。
