---
title: "首页焕新：示例提示词与专家 Agent 展示优化"
type: "体验优化"
priority: "中"
date: "2026-07-20"
status: "待审核"
channels: ""
---

## 核心宣传点

首页做了视觉与内容焕新：更新了英文示例提示词标题、优化了 Hero/页脚排版，并扩充了专家 Agent 选择器（加入官方 Agent、ID 和头像），选择器在各屏幕尺寸下都能更好地展示和滚动。

### 原始内容

**Commit message:**

```
feat(landing): refresh homepage prompts and specialists (#2964)

## Summary

- refresh the homepage hero/footer typography and English sample prompt
titles
- include PPT template requirements in the login handoff for PPT Master
- expand the specialist picker with official agents, IDs, and avatars
- keep the picker inside the viewport with a measured responsive height
and an independently scrolling option list

## Testing

- `vitest run --config ./vitest.config.mts
tests/unit/app/landing-hero-prompt-editing.unit.spec.tsx` — 11 passed
- targeted ESLint for all changed frontend files — passed
- `git diff --check` — passed
- `bash scripts/verify-web.sh ...` — governance checks and ESLint
passed; full run is blocked locally because the shared dependency tree
is missing `recharts`, and the script's default Node 20 runtime is
incompatible with Vitest 4 (`node:util.styleText`). The same targeted
test passes under the bundled Node 24 runtime.

## Preview

- Local mock preview verified with HTTP 200 at
`http://localhost:3001/en`

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

**PR body:**

## Summary

- refresh the homepage hero/footer typography and English sample prompt titles
- include PPT template requirements in the login handoff for PPT Master
- expand the specialist picker with official agents, IDs, and avatars
- keep the picker inside the viewport with a measured responsive height and an independently scrolling option list

## Testing

- `vitest run --config ./vitest.config.mts tests/unit/app/landing-hero-prompt-editing.unit.spec.tsx` — 11 passed
- targeted ESLint for all changed frontend files — passed
- `git diff --check` — passed
- `bash scripts/verify-web.sh ...` — governance checks and ESLint passed; full run is blocked locally because the shared dependency tree is missing `recharts`, and the script's default Node 20 runtime is incompatible with Vitest 4 (`node:util.styleText`). The same targeted test passes under the bundled Node 24 runtime.

## Preview

- Local mock preview verified with HTTP 200 at `http://localhost:3001/en`

