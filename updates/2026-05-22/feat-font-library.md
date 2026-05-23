---
title: "新增内置字体库：Designer Skill 支持更多专业字体"
type: "产品基础功能更新"
priority: "中"
date: "2026-05-22"
status: "待审核"
channels: ""
---

# 新增内置字体库：Designer Skill 支持更多专业字体

## 核心宣传点

Designer Skill 现在内置了丰富的字体库，AI 设计时可以使用更多专业字体，让海报、图片设计效果更精美。

## 原始内容

**Commit**: de97bffb550547a316f00c59dada60693a7c2209
**Author**: shana-srp
**Date**: 2026-05-22T10:53:32Z
**PR**: #202

### Commit Message
```
feat: add font library collection with Git LFS (#202)

* feat: add font library collection with 101 usable fonts + 43 brand references

Curated font catalog (fonts.json) covering Google Fonts, cn-fontsource CDN,
Vercel Geist, Apple/Microsoft system fonts, and standalone sources.
Includes visual showcase HTML and SKILL.md shared resource documentation.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

* chore: remove _font-library-collection, font data lives in extra-skills/_fonts

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

* refactor: move font files from extra-skills/_fonts/ to _fonts/

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

* feat: download all 101 fonts to _fonts/ with Git LFS

Download all open-source fonts from the font library catalog:
- Source Han Serif (10 language variants/subsets, woff2)
- 88 Google Fonts (display/sans/serif/mono/CJK/handwriting)
- 4 cn_fontsource fonts (Smiley Sans, Yozai, LXGW WenKai, MiSans)
- Geist + Geist Mono (Vercel)
- D-DIN (SpaceX)
- 方正粗金陵简体 (local TTF)

Total: 3532 font files (~606MB), tracked via Git LFS.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

* chore: migrate 方正粗金陵简体.TTF to Git LFS

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```

### PR Description
## Summary
- Add curated font library at `_fonts/` with **101 usable fonts + 43 brand typography references**
- `fonts.json` — machine-readable font catalog (Google Fonts, cn_fontsource, standalone fonts, brand references)
- `font-showcase.html` — visual preview page ([live preview](https://assets.yesy.site/f/web/2026/05/h26moqy3.html))
- Download all open-source font files (~606MB, 3532 files) managed via **Git LFS**:
  - Source Han Serif (10 language variants/subsets, woff2)
  - 88 Google Fonts (display/sans-serif/serif/monospace/CJK/handwriting)
  - 4 cn_fontsource fonts (Smiley Sans, Yozai, LXGW WenKai, MiSans)
  - Geist + Geist Mono (Vercel), D-DIN (SpaceX), 方正粗金陵简体

## Test plan
- [ ] Verify `git lfs pull` works on fresh clone
- [ ] Confirm `fonts.json` is valid JSON and all font entries are consistent
- [ ] Open `font-showcase.html` and verify fonts render correctly
- [ ] Verify `.gitattributes` LFS tracking rules cover all font extensions

🤖 Generated with [Claude Code](https://claude.com/claude-code)

