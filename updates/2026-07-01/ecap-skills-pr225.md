---
title: "新增共享 BGM 背景音乐库，视频创作可直接调用"
type: "Skill 上架/更新"
priority: "中"
date: "2026-07-01"
status: "待审核"
channels: ""
---
# 新增共享 BGM 背景音乐库，视频创作可直接调用
## 核心宣传点
平台新增了一套共享背景音乐库（Founder IP Studio BGM 合集），Agent 在生成视频等内容时可以直接挑选并配上合适的背景音乐，让成片更有氛围感。
## 原始内容
Add shared BGM library (#225)

## Summary
- add a shared _BGM library with the Founder IP Studio BGM collection
- add bgm.json metadata and resolve_bgm.py for agent consumption
- publish _BGM alongside _fonts and track mp3 assets with Git LFS

## Verification
- jq empty _BGM/bgm.json
- python3 _BGM/scripts/resolve_bgm.py --id calm-ambition
- python3 _BGM/scripts/resolve_bgm.py --use-case 'founder vision'
--energy medium --format json
- confirmed mp3 files are staged and pushed as Git LFS pointers

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>

---

### PR Description

## Summary
- add a shared _BGM library with the Founder IP Studio BGM collection
- add bgm.json metadata and resolve_bgm.py for agent consumption
- publish _BGM alongside _fonts and track mp3 assets with Git LFS

## Verification
- jq empty _BGM/bgm.json
- python3 _BGM/scripts/resolve_bgm.py --id calm-ambition
- python3 _BGM/scripts/resolve_bgm.py --use-case 'founder vision' --energy medium --format json
- confirmed mp3 files are staged and pushed as Git LFS pointers
