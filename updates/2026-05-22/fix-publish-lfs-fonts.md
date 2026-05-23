---
title: "修复 Skill 发布流程：正确加载字体库，移除错误依赖"
type: "Bug Fix"
priority: "中"
date: "2026-05-22"
status: "待审核"
channels: ""
---

# 修复 Skill 发布流程：正确加载字体库，移除错误依赖

## 核心宣传点

修复了 Skill 发布时字体文件未正确打包的问题，Designer 等依赖字体的 Skill 现在能稳定加载字体资源。

## 原始内容

**Commit**: 7492cb9991e411a294c8cb1617da63c9daef1ae2
**Author**: allenz-srp
**Date**: 2026-05-22T11:06:58Z
**PR**: #203

### Commit Message
```
fix(publish): LFS on checkout, add _fonts, drop websearch from publish list (#203)

* fix(publish): pull Git LFS on checkout + add _fonts to publish whitelist

#202 introduced a Git LFS-tracked font library (_fonts/), but the publish
workflow's `actions/checkout@v4` defaults to lfs:false — so the checkout would
yield 130-byte LFS pointer files and `aws s3 sync` would publish pointers
instead of the real fonts to extra-skills/. Add `lfs: true` to all three
(dev/staging/production) checkout steps.

Also add `_fonts` to PUBLISHED_SKILLS so the shared font library is actually
synced to the extra-skills volume (it was excluded by the whitelist, and
--delete would have removed it otherwise).

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>

* chore(publish): drop websearch skill from publish list

Native web_search now ships via the @zooclaw/web-search plugin, so the legacy
websearch skill should no longer sync to the S3 gateway. Removing it from
PUBLISHED_SKILLS means the next publish (--delete) will remove
extra-skills/websearch/ from the gateway.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>
```

### PR Description
## Changes
1. **`lfs: true` on all 3 checkout steps** — #202 added a Git LFS font library (`_fonts/`, ~606MB). `actions/checkout@v4` defaults to `lfs: false`, so the checkout yields 130-byte LFS *pointer* files and `aws s3 sync` would publish pointers, not real fonts. (This is why v0.6.x wasn't published after merging #202.)
2. **Add `_fonts` to `PUBLISHED_SKILLS`** — otherwise the shared font library is never synced (and `--delete` would remove it). Synced to `extra-skills/_fonts/`.
3. **Drop `websearch` from `PUBLISHED_SKILLS`** — native web_search now ships via the `@zooclaw/web-search` plugin, so the legacy `websearch` skill should no longer sync. Next publish (`--delete`) will remove `extra-skills/websearch/` from the gateway.

## Heads-up
- First publish uploads ~606MB of fonts to `extra-skills/`; `aws s3 sync` is incremental afterwards.
- `--delete` will remove `extra-skills/websearch/` on the next publish — intended.
- Delivery model assumed = via extra-skills volume. If fonts should come from CDN (assets.yesy.site) instead, drop the `_fonts` whitelist line and keep only `lfs: true`.
- Still open (not in this PR): confirm redistribution rights for `方正粗金陵简体`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

