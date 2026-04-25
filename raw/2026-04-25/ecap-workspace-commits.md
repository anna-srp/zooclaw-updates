# ecap-workspace - 2026-04-25

共 50 条 commits

---

## refactor(web): svg-inline — admin + chat (6 files, 14 svgs) (#1341)

- **SHA**: `8f234916d29d90b73345b252c492a49c0fa0026c`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T18:16:26Z
- **PR**: #1341

### Commit Message

```
refactor(web): svg-inline — admin + chat (6 files, 14 svgs) (#1341)

## Summary

继续 SVG 治理系列 (PR #14 of the series) — 清理 \`src/app/[locale]/admin/\` 4
个文件 + \`src/components/chat/\` 2 个文件,共 14 处 inline svg。svg-inline
baseline **48 → 42**。

### 迁移文件 (6)
- \`admin/AdminClient.tsx\` (2) — WarningTriangleIcon, RefreshIcon
- \`admin/components/OrderHistoryModal.tsx\` (1) — ReceiptIcon
- \`admin/components/Spinner.tsx\` (1) — \`SvgSpinner\` 改成 thin wrapper
调 SpinnerIcon + animate-spin
- \`admin/components/UsersTab.tsx\` (7) — WarningCircleTallIcon,
ReceiptIcon, PlusIcon, TrendingUpIcon, ChevronLeftIcon,
ChevronRightPathIcon, UsersGroupIcon
- \`chat/CopyButton.tsx\` (2) — CheckIcon, DuplicateIcon
- \`chat/RetryButton.tsx\` (1) — RefreshIcon

### 新增 wrapper (3)
- \`ReceiptIcon\` — single-path receipt / journal (stroke=2),UsersTab +
OrderHistoryModal 共用
- \`TrendingUpIcon\` — 向上箭头 + 折线(\`M13 7h8m0 0v8m0-8l-8 8-4-4-6 6\`,
stroke=2),UsersTab "提升"按钮
- \`UsersGroupIcon\` — Heroicons v1 三人 group(stroke=2),UsersTab 空状态

### 复用 wrapper (8)
- AdminClient: \`WarningTriangleIcon\`, \`RefreshIcon\`
- UsersTab: \`WarningCircleTallIcon\`, \`PlusIcon\`,
\`ChevronLeftIcon\`, \`ChevronRightPathIcon\`
- admin/Spinner: \`SpinnerIcon\`(SvgSpinner 保持同样的 API + animate-spin
className)
- chat/CopyButton: \`CheckIcon\`, \`DuplicateIcon\`
- chat/RetryButton: \`RefreshIcon\`

### DuplicateIcon 去 \`@public\`

\`DuplicateIcon\` 之前只被 ExampleShowcase(knip ignore)消费,加了 \`@public\` tag
抑制 knip 的 "unused export" 报错。现在 chat/CopyButton 成为非 ignore 消费者,tag
失去必要性,在 barrel + source 两处都去掉,同时更新 source 文件注释反映新的调用方。

## Test plan

- [x] \`pnpm lint\` — clean
- [x] \`npx tsc --noEmit\` — clean
- [x] \`pnpm lint:ci\` — knip hard gates pass
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` — 48 → 42 ✅
- [x] \`bash scripts/check-ignores-shrink-only.sh\` — 45 → 45 ✅
- [x] \`bash scripts/check-no-raw-fetch-shrink-only.sh\` — 5 → 5 ✅
- [ ] 视觉回归:
- admin page (/admin) 三处:权限失败警告三角形、刷新按钮 spin 状态、users tab 的 7 处(warning
circle 错误、receipt 充值历史、plus 发放、trending-up 提升、chevron 分页左右、users-group
空状态)
  - 充值历史弹窗(OrderHistoryModal)空状态 receipt icon + 加载 spinner
- 任意聊天消息的 hover: Copy button(未复制 duplicate icon / 已复制 check)+ Retry
button(refresh icon)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

继续 SVG 治理系列 (PR #14 of the series) — 清理 \`src/app/[locale]/admin/\` 4 个文件 + \`src/components/chat/\` 2 个文件,共 14 处 inline svg。svg-inline baseline **48 → 42**。

### 迁移文件 (6)
- \`admin/AdminClient.tsx\` (2) — WarningTriangleIcon, RefreshIcon
- \`admin/components/OrderHistoryModal.tsx\` (1) — ReceiptIcon
- \`admin/components/Spinner.tsx\` (1) — \`SvgSpinner\` 改成 thin wrapper 调 SpinnerIcon + animate-spin
- \`admin/components/UsersTab.tsx\` (7) — WarningCircleTallIcon, ReceiptIcon, PlusIcon, TrendingUpIcon, ChevronLeftIcon, ChevronRightPathIcon, UsersGroupIcon
- \`chat/CopyButton.tsx\` (2) — CheckIcon, DuplicateIcon
- \`chat/RetryButton.tsx\` (1) — RefreshIcon

### 新增 wrapper (3)
- \`ReceiptIcon\` — single-path receipt / journal (stroke=2),UsersTab + OrderHistoryModal 共用
- \`TrendingUpIcon\` — 向上箭头 + 折线(\`M13 7h8m0 0v8m0-8l-8 8-4-4-6 6\`, stroke=2),UsersTab "提升"按钮
- \`UsersGroupIcon\` — Heroicons v1 三人 group(stroke=2),UsersTab 空状态

### 复用 wrapper (8)
- AdminClient: \`WarningTriangleIcon\`, \`RefreshIcon\`
- UsersTab: \`WarningCircleTallIcon\`, \`PlusIcon\`, \`ChevronLeftIcon\`, \`ChevronRightPathIcon\`
- admin/Spinner: \`SpinnerIcon\`(SvgSpinner 保持同样的 API + animate-spin className)
- chat/CopyButton: \`CheckIcon\`, \`DuplicateIcon\`
- chat/RetryButton: \`RefreshIcon\`

### DuplicateIcon 去 \`@public\`

\`DuplicateIcon\` 之前只被 ExampleShowcase(knip ignore)消费,加了 \`@public\` tag 抑制 knip 的 "unused export" 报错。现在 chat/CopyButton 成为非 ignore 消费者,tag 失去必要性,在 barrel + source 两处都去掉,同时更新 source 文件注释反映新的调用方。

## Test plan

- [x] \`pnpm lint\` — clean
- [x] \`npx tsc --noEmit\` — clean
- [x] \`pnpm lint:ci\` — knip hard gates pass
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` — 48 → 42 ✅
- [x] \`bash scripts/check-ignores-shrink-only.sh\` — 45 → 45 ✅
- [x] \`bash scripts/check-no-raw-fetch-shrink-only.sh\` — 5 → 5 ✅
- [ ] 视觉回归:
  - admin page (/admin) 三处:权限失败警告三角形、刷新按钮 spin 状态、users tab 的 7 处(warning circle 错误、receipt 充值历史、plus 发放、trending-up 提升、chevron 分页左右、users-group 空状态)
  - 充值历史弹窗(OrderHistoryModal)空状态 receipt icon + 加载 spinner
  - 任意聊天消息的 hover: Copy button(未复制 duplicate icon / 已复制 check)+ Retry button(refresh icon)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): svg-inline — artifacts (2 files, 10 svgs) (#1339)

- **SHA**: `d1f84ad5aa6cd6133833d26b58f2a91b4be4284e`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T17:49:01Z
- **PR**: #1339

### Commit Message

```
refactor(web): svg-inline — artifacts (2 files, 10 svgs) (#1339)

## Summary

继续 SVG 治理系列 (PR #13 of the series) — 清理 \`src/components/artifacts/\` 下
2 个文件的 10 处 inline svg。svg-inline baseline **50 → 48**。

### 迁移文件 (2)
- \`ArtifactPreview.tsx\` (9 svgs) — 之前是 9 个文件底部的 local \`function
EyeIcon() {}\` / \`CodeIcon\` / \`LinkIcon\` / \`CheckIcon\` /
\`DownloadIcon\` / \`ReloadIcon\` / \`CloseIcon\` / \`FrameIcon\` /
\`ChevronDownIcon\` 本地封装,全部删除,调用点改为 import + \`className\` prop
- \`renderers/FallbackRenderer.tsx\` (1 svg) — DocumentBlankThinIcon

### 新增 wrapper (8)
全部 byte-exact 保留源 svg 属性,命名刻意与已有 wrapper 区分:

- \`EyeThinIcon\` — Heroicons v2 eye outline (stroke=1.5),区分
\`EyeIcon\`(Heroicons v1, stroke=2,almond 曲率不同)
- \`CodeSlashIcon\` — Heroicons v2 code-bracket 带斜杠 (stroke=1.5),区分
\`CodeBracketsIcon\`(Feather 2-polyline,无斜杠)
- \`LinkChainIcon\` — 2 path 对称 chain link (stroke=1.5),区分
\`LinkIcon\`(Feather single-path)
- \`CheckLargeIcon\` — \`M4.5 12.75l6 6 9-13.5\` stroke=2,sweep 比
\`CheckIcon\` (\`M5 13l4 4L19 7\`) 更大
- \`ReloadIcon\` — Heroicons v2 arrow-path (stroke=1.5),和
\`RefreshIcon\`(v1 arrow-loop)字形不同
- \`FrameIcon\` — 4 个 L 形角 bracket(stroke=1.5),用于 fit-to-frame 切换
- \`ChevronDownLargeThickIcon\` — 与 \`ChevronDownLargeIcon\` 同 path 但
stroke=2(补齐 path×stroke 的 2×2 矩阵)
- \`DocumentBlankThinIcon\` — 与 \`DocumentBlankIcon\` (\`@public\`,
stroke=2) + \`FileGenericIcon\` (stroke=1.75) 同 path,stroke=1.5 的第三个变体

### 复用 wrapper (2)
- \`DownloadIcon\` — path + stroke=1.5 完全匹配
- \`CloseIcon\` — path + stroke=2 完全匹配

### 跳过 PptxRenderer

\`renderers/PptxRenderer.tsx\` 还有 2 处 inline svg,但留在 baseline —— 该文件 4 处
inline style 用了 \`rgba(\${r},\${g},\${b})\` / \`'#1a1a2e'\` 这类 template
literal + hex fallback(数据驱动,从 pptx 主题派生),如果把它从 svg-inline list 移除,color
rules 会触发。色值来源是数据不是 branded palette,未来拿专门 PR 处理时顺手迁移。

## Test plan

- [x] \`pnpm lint\` — clean
- [x] \`npx tsc --noEmit\` — clean
- [x] \`pnpm lint:ci\` — knip hard gates pass
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` — 50 → 48 ✅
- [x] \`bash scripts/check-ignores-shrink-only.sh\` — 45 → 45 ✅
- [x] \`bash scripts/check-no-raw-fetch-shrink-only.sh\` — 5 → 5 ✅
- [ ] 视觉回归:chat 里预览 artifact(点 artifact tile 打开 ArtifactPreview);切
source/preview(eye/code),复制链接(link→check
状态切换),下载(download),重新加载(reload),关闭(close),aspect ratio 菜单(frame +
chevron);失败状态的 fallback renderer 文档图标。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

继续 SVG 治理系列 (PR #13 of the series) — 清理 \`src/components/artifacts/\` 下 2 个文件的 10 处 inline svg。svg-inline baseline **50 → 48**。

### 迁移文件 (2)
- \`ArtifactPreview.tsx\` (9 svgs) — 之前是 9 个文件底部的 local \`function EyeIcon() {}\` / \`CodeIcon\` / \`LinkIcon\` / \`CheckIcon\` / \`DownloadIcon\` / \`ReloadIcon\` / \`CloseIcon\` / \`FrameIcon\` / \`ChevronDownIcon\` 本地封装,全部删除,调用点改为 import + \`className\` prop
- \`renderers/FallbackRenderer.tsx\` (1 svg) — DocumentBlankThinIcon

### 新增 wrapper (8)
全部 byte-exact 保留源 svg 属性,命名刻意与已有 wrapper 区分:

- \`EyeThinIcon\` — Heroicons v2 eye outline (stroke=1.5),区分 \`EyeIcon\`(Heroicons v1, stroke=2,almond 曲率不同)
- \`CodeSlashIcon\` — Heroicons v2 code-bracket 带斜杠 (stroke=1.5),区分 \`CodeBracketsIcon\`(Feather 2-polyline,无斜杠)
- \`LinkChainIcon\` — 2 path 对称 chain link (stroke=1.5),区分 \`LinkIcon\`(Feather single-path)
- \`CheckLargeIcon\` — \`M4.5 12.75l6 6 9-13.5\` stroke=2,sweep 比 \`CheckIcon\` (\`M5 13l4 4L19 7\`) 更大
- \`ReloadIcon\` — Heroicons v2 arrow-path (stroke=1.5),和 \`RefreshIcon\`(v1 arrow-loop)字形不同
- \`FrameIcon\` — 4 个 L 形角 bracket(stroke=1.5),用于 fit-to-frame 切换
- \`ChevronDownLargeThickIcon\` — 与 \`ChevronDownLargeIcon\` 同 path 但 stroke=2(补齐 path×stroke 的 2×2 矩阵)
- \`DocumentBlankThinIcon\` — 与 \`DocumentBlankIcon\` (\`@public\`, stroke=2) + \`FileGenericIcon\` (stroke=1.75) 同 path,stroke=1.5 的第三个变体

### 复用 wrapper (2)
- \`DownloadIcon\` — path + stroke=1.5 完全匹配
- \`CloseIcon\` — path + stroke=2 完全匹配

### 跳过 PptxRenderer

\`renderers/PptxRenderer.tsx\` 还有 2 处 inline svg,但留在 baseline —— 该文件 4 处 inline style 用了 \`rgba(\${r},\${g},\${b})\` / \`'#1a1a2e'\` 这类 template literal + hex fallback(数据驱动,从 pptx 主题派生),如果把它从 svg-inline list 移除,color rules 会触发。色值来源是数据不是 branded palette,未来拿专门 PR 处理时顺手迁移。

## Test plan

- [x] \`pnpm lint\` — clean
- [x] \`npx tsc --noEmit\` — clean
- [x] \`pnpm lint:ci\` — knip hard gates pass
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` — 50 → 48 ✅
- [x] \`bash scripts/check-ignores-shrink-only.sh\` — 45 → 45 ✅
- [x] \`bash scripts/check-no-raw-fetch-shrink-only.sh\` — 5 → 5 ✅
- [ ] 视觉回归:chat 里预览 artifact(点 artifact tile 打开 ArtifactPreview);切 source/preview(eye/code),复制链接(link→check 状态切换),下载(download),重新加载(reload),关闭(close),aspect ratio 菜单(frame + chevron);失败状态的 fallback renderer 文档图标。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): svg-inline — ermp + agent-settings (6 files, 9 svgs) (#1333)

- **SHA**: `299f9c1290c0d451924ab3053d593b20f72c87f8`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T17:31:50Z
- **PR**: #1333

### Commit Message

```
refactor(web): svg-inline — ermp + agent-settings (6 files, 9 svgs) (#1333)

## Summary

继续 SVG 治理系列 (PR #12 of the series) — 清理 `src/components/ermp/` (3 文件) +
`src/components/agent-settings/` (3 文件) 共 6 个文件的 9 处 inline
svg。svg-inline baseline **56 → 50**。

### 迁移文件 (6)
- `ermp/AudioCard.tsx` (1) — MusicNoteIcon
- `ermp/FileCard.tsx` (2) — FileFeatherIcon, DownloadFeatherIcon
- `ermp/VideoCard.tsx` (1) — VideoFeatherIcon
- `agent-settings/AgentBindingsSection.tsx` (2) — CloseIcon,
PlusThinIcon
- `agent-settings/AgentIdentitySection.tsx` (2) — CameraIcon,
SpinnerArcIcon
- `agent-settings/AgentModelSection.tsx` (1) — ChevronDownIcon

### 新增 wrapper (7)
全部 byte-exact 保留源 svg 属性。Feather-style (多 primitive) 与已有的
Heroicons-style 单 path 变体**刻意不合并**:

- \`MusicNoteIcon\` — Feather music-note (path + 2 circle)
- \`FileFeatherIcon\` — Feather file (path + polyline),区分
\`FileGenericIcon\`(Heroicons v2 单 path)
- \`DownloadFeatherIcon\` — Feather download (path + polyline + line),区分
\`DownloadIcon\`/\`DownloadThickIcon\`(Heroicons v2 单 path)
- \`VideoFeatherIcon\` — Feather video (polygon + rect),区分
\`RectangleVideoIcon\`(Heroicons v2 单 path)
- \`PlusThinIcon\` — Heroicons v2 plus \`M12
4.5v15m7.5-7.5h-15\`(full-span),区分 \`PlusIcon\`(compact \`M12 6v6...\`)和
\`PlusLargeIcon\`(longer reach \`M12 4v16m8-8H4\`)
- \`CameraIcon\` — Heroicons v2 camera(2 path,body + lens)
- \`SpinnerArcIcon\` — 单弧 spinner(stroke=2.5,配合 animate-spin),区分
\`SpinnerIcon\`(双色 ring+arc 两 primitive 方案)

### 复用 wrapper (2)
- \`CloseIcon\` — AgentBindingsSection 移除 channel 的 X 按钮
- \`ChevronDownIcon\` — AgentModelSection select 下拉箭头

### 注:onboarding 集群被跳过

原本计划把 \`src/components/onboarding/**\` (9 svg × 6 文件) 也一起做,但发现 eslint
配置把 svg-inline 和 color rules 放在**同一个** \`ignores\` 数组里(per flat-config 的
\`no-restricted-syntax\` rule-replacement constraint),而 onboarding 是
branded module(按 \`web/CLAUDE.md\` 明确列出,跟 login/paywall/pricing
一起),刻意硬编码 \`rgba(184,134,11,*)\` 金色 + \`rgba(26,26,24,*)\` 墨色,属于 #796
theme refactor 范围。把 onboarding 从 svg-inline list 移出会触发 40+
处颜色规则错误,修那些等于推 #796。留给 #796 完成后再一起做。已保存 memory
\`feedback_svg_branded_modules_blocked.md\` 防止未来重蹈覆辙。

## Test plan

- [x] \`pnpm lint\` — clean
- [x] \`npx tsc --noEmit\` — clean
- [x] \`pnpm lint:ci\` — knip hard gates pass
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` — 56 → 50 ✅
- [x] \`bash scripts/check-ignores-shrink-only.sh\` — 45 → 45 ✅
- [x] \`bash scripts/check-no-raw-fetch-shrink-only.sh\` — 5 → 5 ✅
- [ ] 视觉回归:ermp card 三种(audio / file / video,chat 里 tool 返回时会
render),agent-settings 的三段(identity 头像 hover camera icon / bindings 列表的
remove X + Add Channel + / model 选择器 chevron)。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

继续 SVG 治理系列 (PR #12 of the series) — 清理 `src/components/ermp/` (3 文件) + `src/components/agent-settings/` (3 文件) 共 6 个文件的 9 处 inline svg。svg-inline baseline **56 → 50**。

### 迁移文件 (6)
- `ermp/AudioCard.tsx` (1) — MusicNoteIcon
- `ermp/FileCard.tsx` (2) — FileFeatherIcon, DownloadFeatherIcon
- `ermp/VideoCard.tsx` (1) — VideoFeatherIcon
- `agent-settings/AgentBindingsSection.tsx` (2) — CloseIcon, PlusThinIcon
- `agent-settings/AgentIdentitySection.tsx` (2) — CameraIcon, SpinnerArcIcon
- `agent-settings/AgentModelSection.tsx` (1) — ChevronDownIcon

### 新增 wrapper (7)
全部 byte-exact 保留源 svg 属性。Feather-style (多 primitive) 与已有的 Heroicons-style 单 path 变体**刻意不合并**:

- \`MusicNoteIcon\` — Feather music-note (path + 2 circle)
- \`FileFeatherIcon\` — Feather file (path + polyline),区分 \`FileGenericIcon\`(Heroicons v2 单 path)
- \`DownloadFeatherIcon\` — Feather download (path + polyline + line),区分 \`DownloadIcon\`/\`DownloadThickIcon\`(Heroicons v2 单 path)
- \`VideoFeatherIcon\` — Feather video (polygon + rect),区分 \`RectangleVideoIcon\`(Heroicons v2 单 path)
- \`PlusThinIcon\` — Heroicons v2 plus \`M12 4.5v15m7.5-7.5h-15\`(full-span),区分 \`PlusIcon\`(compact \`M12 6v6...\`)和 \`PlusLargeIcon\`(longer reach \`M12 4v16m8-8H4\`)
- \`CameraIcon\` — Heroicons v2 camera(2 path,body + lens)
- \`SpinnerArcIcon\` — 单弧 spinner(stroke=2.5,配合 animate-spin),区分 \`SpinnerIcon\`(双色 ring+arc 两 primitive 方案)

### 复用 wrapper (2)
- \`CloseIcon\` — AgentBindingsSection 移除 channel 的 X 按钮
- \`ChevronDownIcon\` — AgentModelSection select 下拉箭头

### 注:onboarding 集群被跳过

原本计划把 \`src/components/onboarding/**\` (9 svg × 6 文件) 也一起做,但发现 eslint 配置把 svg-inline 和 color rules 放在**同一个** \`ignores\` 数组里(per flat-config 的 \`no-restricted-syntax\` rule-replacement constraint),而 onboarding 是 branded module(按 \`web/CLAUDE.md\` 明确列出,跟 login/paywall/pricing 一起),刻意硬编码 \`rgba(184,134,11,*)\` 金色 + \`rgba(26,26,24,*)\` 墨色,属于 #796 theme refactor 范围。把 onboarding 从 svg-inline list 移出会触发 40+ 处颜色规则错误,修那些等于推 #796。留给 #796 完成后再一起做。已保存 memory \`feedback_svg_branded_modules_blocked.md\` 防止未来重蹈覆辙。

## Test plan

- [x] \`pnpm lint\` — clean
- [x] \`npx tsc --noEmit\` — clean
- [x] \`pnpm lint:ci\` — knip hard gates pass
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` — 56 → 50 ✅
- [x] \`bash scripts/check-ignores-shrink-only.sh\` — 45 → 45 ✅
- [x] \`bash scripts/check-no-raw-fetch-shrink-only.sh\` — 5 → 5 ✅
- [ ] 视觉回归:ermp card 三种(audio / file / video,chat 里 tool 返回时会 render),agent-settings 的三段(identity 头像 hover camera icon / bindings 列表的 remove X + Add Channel + / model 选择器 chevron)。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): svg-inline — billing (5 files, 8 svgs) (#1330)

- **SHA**: `08994d6363bf9be8a74c589f571670c83b13eea5`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T16:17:40Z
- **PR**: #1330

### Commit Message

```
refactor(web): svg-inline — billing (5 files, 8 svgs) (#1330)

## Summary

继续 SVG 治理系列 (PR #11 of the series) — 清理 `src/components/billing/` 目录下有
inline `<svg>` 的全部 5 个文件的 8 处 inline svg。svg-inline baseline 从 **61 →
56**。

### 迁移文件 (5)
- `InvoiceHistory.tsx` (1) — CreditCardIcon
- `PlanCard.tsx` (1) — SevenDayTrialRibbonIcon
- `SharedPlanCard.tsx` (1) — InfoCircleLineIcon
- `SubscriptionPanel.tsx` (2) — CloseLineIcon, QuestionMarkCircleIcon
- `UpgradePromptModal.tsx` (3) — ClockCircleIcon, CoinIcon,
HeartSolidIcon

### 新增 wrapper (7)
所有 wrapper 均逐字节保留源 svg 的 `path` / `viewBox` / `fill` / `stroke` /
`strokeWidth` / `strokeLinecap` / `strokeLinejoin`：

- \`CreditCardIcon\` — Heroicons v2 credit-card outline（stroke=1.5）
- \`SevenDayTrialRibbonIcon\` — 装饰性 "7 Days Trial" 角带，硬编码品牌色 #F04D59 +
白色
- \`InfoCircleLineIcon\` — Feather 风格 info-circle（circle + 2 line
元素，stroke=2）— 与 \`InfoCircleIcon\`（Heroicons 单 path）和
\`InfoSolidIcon\`（填充 20x20 mini）区分
- \`QuestionMarkCircleIcon\` — Heroicons v2 question-mark-circle
outline（stroke=1.5）
- \`ClockCircleIcon\` — Heroicons v2 clock outline（stroke=1.5）— 与
\`ClockIcon\`（Feather circle + polyline, stroke=2）区分
- \`CoinIcon\` — Heroicons v1 currency-dollar mini solid（20x20
fill=currentColor）
- \`HeartSolidIcon\` — 单 path heart solid（24x24 fill）

### 复用 wrapper (1)
- \`CloseLineIcon\` — SubscriptionPanel 关闭按钮 svg 与 CloseLineIcon 功能等价（仅差
inert attrs: width/height 被 className 覆盖、两条独立 line 没有 join 所以
strokeLinejoin 无效）

### knip 无需 \`@public\`
和 PR #1329 (ExampleShowcase) 不同，billing/ 是可达模块（通过 settings page），所以 knip
自动追踪到 7 个新 wrapper 的使用，无需 \`@public\` tag。

## Test plan

- [x] \`pnpm lint\` — clean
- [x] \`npx tsc --noEmit\` — clean
- [x] \`pnpm lint:ci\` — knip hard gates pass
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` — 61 → 56 ✅
- [x] \`bash scripts/check-ignores-shrink-only.sh\` — 45 → 45 ✅
- [x] \`bash scripts/check-no-raw-fetch-shrink-only.sh\` — 7 → 7 ✅
- [ ] 视觉回归（staging）：settings → billing / credits / subscription panel /
upgrade prompt modal 三个入口；特别验证 SevenDayTrialRibbon（trial 状态 Starter card
的右上角红色角带）和 InfoCircleLineIcon（credits 旁边的 14x14 tooltip 触发器）。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

继续 SVG 治理系列 (PR #11 of the series) — 清理 `src/components/billing/` 目录下有 inline `<svg>` 的全部 5 个文件的 8 处 inline svg。svg-inline baseline 从 **61 → 56**。

### 迁移文件 (5)
- `InvoiceHistory.tsx` (1) — CreditCardIcon
- `PlanCard.tsx` (1) — SevenDayTrialRibbonIcon
- `SharedPlanCard.tsx` (1) — InfoCircleLineIcon
- `SubscriptionPanel.tsx` (2) — CloseLineIcon, QuestionMarkCircleIcon
- `UpgradePromptModal.tsx` (3) — ClockCircleIcon, CoinIcon, HeartSolidIcon

### 新增 wrapper (7)
所有 wrapper 均逐字节保留源 svg 的 `path` / `viewBox` / `fill` / `stroke` / `strokeWidth` / `strokeLinecap` / `strokeLinejoin`：

- \`CreditCardIcon\` — Heroicons v2 credit-card outline（stroke=1.5）
- \`SevenDayTrialRibbonIcon\` — 装饰性 "7 Days Trial" 角带，硬编码品牌色 #F04D59 + 白色
- \`InfoCircleLineIcon\` — Feather 风格 info-circle（circle + 2 line 元素，stroke=2）— 与 \`InfoCircleIcon\`（Heroicons 单 path）和 \`InfoSolidIcon\`（填充 20x20 mini）区分
- \`QuestionMarkCircleIcon\` — Heroicons v2 question-mark-circle outline（stroke=1.5）
- \`ClockCircleIcon\` — Heroicons v2 clock outline（stroke=1.5）— 与 \`ClockIcon\`（Feather circle + polyline, stroke=2）区分
- \`CoinIcon\` — Heroicons v1 currency-dollar mini solid（20x20 fill=currentColor）
- \`HeartSolidIcon\` — 单 path heart solid（24x24 fill）

### 复用 wrapper (1)
- \`CloseLineIcon\` — SubscriptionPanel 关闭按钮 svg 与 CloseLineIcon 功能等价（仅差 inert attrs: width/height 被 className 覆盖、两条独立 line 没有 join 所以 strokeLinejoin 无效）

### knip 无需 \`@public\`
和 PR #1329 (ExampleShowcase) 不同，billing/ 是可达模块（通过 settings page），所以 knip 自动追踪到 7 个新 wrapper 的使用，无需 \`@public\` tag。

## Test plan

- [x] \`pnpm lint\` — clean
- [x] \`npx tsc --noEmit\` — clean
- [x] \`pnpm lint:ci\` — knip hard gates pass
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` — 61 → 56 ✅
- [x] \`bash scripts/check-ignores-shrink-only.sh\` — 45 → 45 ✅
- [x] \`bash scripts/check-no-raw-fetch-shrink-only.sh\` — 7 → 7 ✅
- [ ] 视觉回归（staging）：settings → billing / credits / subscription panel / upgrade prompt modal 三个入口；特别验证 SevenDayTrialRibbon（trial 状态 Starter card 的右上角红色角带）和 InfoCircleLineIcon（credits 旁边的 14x14 tooltip 触发器）。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): useSendMessage terminate → terminateSessionChat (RQ PR 8) (#1331)

- **SHA**: `1be3931b09c71e0a97ca2145e21326b98ad06fec`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T15:52:16Z
- **PR**: #1331

### Commit Message

```
refactor(web): useSendMessage terminate → terminateSessionChat (RQ PR 8) (#1331)

## Summary

Eighth domain migration. The 709-line \`useSendMessage\` hook contained
exactly **one** raw fetch — the best-effort POST to terminate an
in-flight chat job. Spec estimated 400-600 lines because it assumed
fetch was woven through the send/state-machine flow, but that flow is
WS/SSE-based; HTTP is only used for this administrative end-of-stream
call.

- **\`lib/api/session.ts\`** — added \`terminateSessionChat(jobId)\`
using \`postAPI\`, alongside the existing \`recordSessionChat\`.
Auto-injects bearer + consistent error envelope handling.
- **\`useSendMessage.ts\`** — replaced inline fetch + manual
Authorization header construction with the helper call. Same best-effort
semantics (caller still ignores result and runs cleanup
unconditionally). \`getLoginToken\` import dropped (no longer used in
this file).
- **ESLint SHRINK-ONLY** — \`useSendMessage.ts\` removed (6 → 5
transitional).

Spec:
[\`docs/superpowers/specs/2026-04-24-react-query-migration.md\`](docs/superpowers/specs/2026-04-24-react-query-migration.md).

**Why no new tests**: caller-visible behavior is unchanged,
\`postAPI\`'s auth + error handling has its own coverage, and the
existing 49 \`useSendMessage\` spec cases pass without modification.

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm lint:ci\` clean (knip dep-health hard gate + dep-cruiser
boundaries)
- [x] \`pnpm test:unit\` — useSendMessage's existing 49 tests pass
- [ ] Local \`pnpm dev\` — start a chat, hit Stop mid-stream; confirm
terminate fires + UI returns to idle

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Eighth domain migration. The 709-line \`useSendMessage\` hook contained exactly **one** raw fetch — the best-effort POST to terminate an in-flight chat job. Spec estimated 400-600 lines because it assumed fetch was woven through the send/state-machine flow, but that flow is WS/SSE-based; HTTP is only used for this administrative end-of-stream call.

- **\`lib/api/session.ts\`** — added \`terminateSessionChat(jobId)\` using \`postAPI\`, alongside the existing \`recordSessionChat\`. Auto-injects bearer + consistent error envelope handling.
- **\`useSendMessage.ts\`** — replaced inline fetch + manual Authorization header construction with the helper call. Same best-effort semantics (caller still ignores result and runs cleanup unconditionally). \`getLoginToken\` import dropped (no longer used in this file).
- **ESLint SHRINK-ONLY** — \`useSendMessage.ts\` removed (6 → 5 transitional).

Spec: [\`docs/superpowers/specs/2026-04-24-react-query-migration.md\`](docs/superpowers/specs/2026-04-24-react-query-migration.md).

**Why no new tests**: caller-visible behavior is unchanged, \`postAPI\`'s auth + error handling has its own coverage, and the existing 49 \`useSendMessage\` spec cases pass without modification.

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm lint:ci\` clean (knip dep-health hard gate + dep-cruiser boundaries)
- [x] \`pnpm test:unit\` — useSendMessage's existing 49 tests pass
- [ ] Local \`pnpm dev\` — start a chat, hit Stop mid-stream; confirm terminate fires + UI returns to idle

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): useLiteLLMApi → 3 useMutation (RQ PR 7) (#1326)

- **SHA**: `d93284fd4ffa1f4bf4b995b1644b6b2437481e3e`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T15:44:19Z
- **PR**: #1326

### Commit Message

```
refactor(web): useLiteLLMApi → 3 useMutation (RQ PR 7) (#1326)

## Summary

Seventh domain migration — the **high-risk chat main path**. Three paid
LLM endpoints (chat / image generation / video generation) move from
hand-rolled imperative fetch to \`useMutation\`. Caller API preserved so
\`useCanvasChat\`'s \`await sendXRequest(...)\` orchestration is
untouched.

- **\`src/lib/api/chat.ts\`** (NEW, permanent allowlist) — pure utils
(\`sanitizeMessageContent\` / \`limitMessages\` /
\`prepareMessagesForApi\`) + three mutationFn wrappers
(\`sendTextChatCompletion\` / \`sendImageGeneration\` /
\`sendVideoGeneration\`) + \`consumeImageSseStream\` +
\`InsufficientCreditsError\` (promoted from \`useSSEStream.ts\` to avoid
the W1 lib→hooks boundary violation). Named \`/chat.ts\` because
\`lib/api/litellm.ts\` already exists as the server-side LiteLLM proxy
wrapper.
- **\`src/hooks/useLiteLLMApi.ts\`** — 3 \`useMutation\` +
\`mutateAsync\` delegates. \`recordToSession\` + \`handleApiError\` stay
(they touch React state / closures). \`buildRequestHeaders\` export
dropped (trivial passthrough with no consumer outside the test file).
- **\`mutations.retry: 0\`** inherited from global \`createQueryClient\`
defaults — critical for paid endpoints. No double-charge on flaky
network.
- **ESLint SHRINK-ONLY** — \`useLiteLLMApi.ts\` removed (7 → 6
transitional).
- **Tests** — all 33 existing cases preserved, wrapped with
\`createQueryWrapper\`. 3 \`buildRequestHeaders\` cases moved to a new
\`tests/unit/lib/api/headers.unit.spec.ts\` that tests
\`buildAuthHeaders\` directly.

Spec:
[\`docs/superpowers/specs/2026-04-24-react-query-migration.md\`](docs/superpowers/specs/2026-04-24-react-query-migration.md).

**Why the caller API is preserved**: \`useCanvasChat\` orchestrates
\`await sendX(...)\` then \`await recordToSession(...)\` imperatively;
exposing mutation state through the hook would force a call-site rewrite
for minimal ergonomic gain. The machinery (retry policy, global error
handling hooks) works identically from the call site's POV.

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm lint:ci\` clean (dep-cruiser W1 lib→hooks resolved by
moving \`InsufficientCreditsError\`)
- [x] \`pnpm test:unit\` — 263 files / 4175 tests pass (only
pre-existing admin auth flakies)
- [ ] Local \`pnpm dev\` — canvas chat: text completion (\`gpt-4\`),
image generation (\`dall-e-3\` with SSE), video generation. Confirm each
returns results and insufficient-credits modal fires correctly on 403.
- [ ] Staging visual regression (chat is the primary surface)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Seventh domain migration — the **high-risk chat main path**. Three paid LLM endpoints (chat / image generation / video generation) move from hand-rolled imperative fetch to \`useMutation\`. Caller API preserved so \`useCanvasChat\`'s \`await sendXRequest(...)\` orchestration is untouched.

- **\`src/lib/api/chat.ts\`** (NEW, permanent allowlist) — pure utils (\`sanitizeMessageContent\` / \`limitMessages\` / \`prepareMessagesForApi\`) + three mutationFn wrappers (\`sendTextChatCompletion\` / \`sendImageGeneration\` / \`sendVideoGeneration\`) + \`consumeImageSseStream\` + \`InsufficientCreditsError\` (promoted from \`useSSEStream.ts\` to avoid the W1 lib→hooks boundary violation). Named \`/chat.ts\` because \`lib/api/litellm.ts\` already exists as the server-side LiteLLM proxy wrapper.
- **\`src/hooks/useLiteLLMApi.ts\`** — 3 \`useMutation\` + \`mutateAsync\` delegates. \`recordToSession\` + \`handleApiError\` stay (they touch React state / closures). \`buildRequestHeaders\` export dropped (trivial passthrough with no consumer outside the test file).
- **\`mutations.retry: 0\`** inherited from global \`createQueryClient\` defaults — critical for paid endpoints. No double-charge on flaky network.
- **ESLint SHRINK-ONLY** — \`useLiteLLMApi.ts\` removed (7 → 6 transitional).
- **Tests** — all 33 existing cases preserved, wrapped with \`createQueryWrapper\`. 3 \`buildRequestHeaders\` cases moved to a new \`tests/unit/lib/api/headers.unit.spec.ts\` that tests \`buildAuthHeaders\` directly.

Spec: [\`docs/superpowers/specs/2026-04-24-react-query-migration.md\`](docs/superpowers/specs/2026-04-24-react-query-migration.md).

**Why the caller API is preserved**: \`useCanvasChat\` orchestrates \`await sendX(...)\` then \`await recordToSession(...)\` imperatively; exposing mutation state through the hook would force a call-site rewrite for minimal ergonomic gain. The machinery (retry policy, global error handling hooks) works identically from the call site's POV.

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm lint:ci\` clean (dep-cruiser W1 lib→hooks resolved by moving \`InsufficientCreditsError\`)
- [x] \`pnpm test:unit\` — 263 files / 4175 tests pass (only pre-existing admin auth flakies)
- [ ] Local \`pnpm dev\` — canvas chat: text completion (\`gpt-4\`), image generation (\`dall-e-3\` with SSE), video generation. Confirm each returns results and insufficient-credits modal fires correctly on 403.
- [ ] Staging visual regression (chat is the primary surface)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): svg-inline — ExampleShowcase (7 files, 39 svgs) (#1329)

- **SHA**: `b6719888f68365b701080a2ead6310b4c7a29ac0`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T15:21:22Z
- **PR**: #1329

### Commit Message

```
refactor(web): svg-inline — ExampleShowcase (7 files, 39 svgs) (#1329)

## Summary

继续 SVG 治理系列 (PR #10 of the series) — 清理
`src/components/ExampleShowcase/` 目录下所有 7 个文件的 39 处 inline
`<svg>`。svg-inline baseline 从 **68 → 61**。

### 迁移文件 (7)
- `ExampleFeed.tsx` (1) — PhotoIcon
- `ExampleFeedCard.tsx` (3) — PhotoIcon, PlayIcon, EyeIcon
- `QueryContent.tsx` (2) — PlayIcon, CloseIcon
- `ExamplePreviewModal.tsx` (3) — PhotoIcon, VideoCameraIcon, CloseIcon
- `CreatifyPreview.tsx` (7) — CheckIcon, PlayIcon ×2, InboxIcon,
ChatBubbleDotsIcon, DuplicateIcon, CloseIcon
- `CreativeMaterialPreview.tsx` (10) — PhotoIcon ×4, CheckIcon,
SearchPlusIcon, PhotoThickIcon, ChatBubbleDotsIcon, DuplicateIcon,
CloseIcon
- `GenMediaPdpPreview.tsx` (13) — PhotoIcon ×4, CheckIcon,
SearchPlusIcon, PhotoThickIcon ×2, DocumentLinedIcon, DocumentBlankIcon,
ChatBubbleDotsIcon, DuplicateIcon, CloseIcon

### 新增 wrapper (6)
所有 wrapper 均逐字节保留源 svg 的 `path` / `viewBox` / `fill` / `stroke` /
`strokeWidth` / `strokeLinecap` / `strokeLinejoin`：

- `VideoCameraIcon` — Heroicons v1 video-camera outline（与
`RectangleVideoIcon` 的 v2 path 不同，三角形几何与圆角半径都不同）
- `InboxIcon` — Heroicons v1 inbox outline（box + 隔线 + 顶部把手槽）
- `ChatBubbleDotsIcon` — Heroicons v1 chat-alt-2 outline（气泡带三个点）— 与
`ChatBubbleIcon`（简单圆角带尾巴气泡）区分
- `DuplicateIcon` — Heroicons v1 duplicate outline（两个叠合矩形）
- `DocumentLinedIcon` — Heroicons v1 document-text outline（折角文档 + 两条横线）
- `DocumentBlankIcon` — Heroicons v1 document outline（空白折角文档）

### knip \`@public\` tag
ExampleShowcase/** 在 \`knip.config.ts\` 的 \`ignore\` 列表里（"legacy modules
preserved for reactivation"）。6 个新 wrapper 唯一消费方都在这个 frozen 目录，没有 tag 的话
knip 会标记为 "unused exports"。按仓库约定（见 \`knip.config.ts\` 中 \`tags:
['-public']\` 说明）给 wrapper source 文件 + \`index.ts\` barrel re-export 都加
\`@public\` JSDoc。

### 复用 wrapper (7)
已 diff \`strokeWidth\` / \`strokeLinecap\` / \`strokeLinejoin\` /
element type 确认**完全一致**再复用：`CheckIcon`, `CloseIcon`, `EyeIcon`,
`PhotoIcon`, `PhotoThickIcon`, `PlayIcon`, `SearchPlusIcon`.

## Test plan

- [x] \`pnpm lint\` — clean
- [x] \`npx tsc --noEmit\` — clean
- [x] \`pnpm lint:ci\` — knip hard gates (files/exports/dep-health) pass
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` — 68 → 61 ✅
- [x] \`bash scripts/check-ignores-shrink-only.sh\` — 45 → 45 ✅
- [x] \`bash scripts/check-no-raw-fetch-shrink-only.sh\` — 7 → 7 ✅
- [ ] 视觉回归（staging）：ExampleShowcase 不在当前 UI 主路径（legacy module），但若通过
AgentChatClient 某条路径能 surface preview modal，需要对比 Creative Material / Gen
Media PDP / Creatify 三种 preview 的 result/source-assets/prompt 三段 icon。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

继续 SVG 治理系列 (PR #10 of the series) — 清理 `src/components/ExampleShowcase/` 目录下所有 7 个文件的 39 处 inline `<svg>`。svg-inline baseline 从 **68 → 61**。

### 迁移文件 (7)
- `ExampleFeed.tsx` (1) — PhotoIcon
- `ExampleFeedCard.tsx` (3) — PhotoIcon, PlayIcon, EyeIcon
- `QueryContent.tsx` (2) — PlayIcon, CloseIcon
- `ExamplePreviewModal.tsx` (3) — PhotoIcon, VideoCameraIcon, CloseIcon
- `CreatifyPreview.tsx` (7) — CheckIcon, PlayIcon ×2, InboxIcon, ChatBubbleDotsIcon, DuplicateIcon, CloseIcon
- `CreativeMaterialPreview.tsx` (10) — PhotoIcon ×4, CheckIcon, SearchPlusIcon, PhotoThickIcon, ChatBubbleDotsIcon, DuplicateIcon, CloseIcon
- `GenMediaPdpPreview.tsx` (13) — PhotoIcon ×4, CheckIcon, SearchPlusIcon, PhotoThickIcon ×2, DocumentLinedIcon, DocumentBlankIcon, ChatBubbleDotsIcon, DuplicateIcon, CloseIcon

### 新增 wrapper (6)
所有 wrapper 均逐字节保留源 svg 的 `path` / `viewBox` / `fill` / `stroke` / `strokeWidth` / `strokeLinecap` / `strokeLinejoin`：

- `VideoCameraIcon` — Heroicons v1 video-camera outline（与 `RectangleVideoIcon` 的 v2 path 不同，三角形几何与圆角半径都不同）
- `InboxIcon` — Heroicons v1 inbox outline（box + 隔线 + 顶部把手槽）
- `ChatBubbleDotsIcon` — Heroicons v1 chat-alt-2 outline（气泡带三个点）— 与 `ChatBubbleIcon`（简单圆角带尾巴气泡）区分
- `DuplicateIcon` — Heroicons v1 duplicate outline（两个叠合矩形）
- `DocumentLinedIcon` — Heroicons v1 document-text outline（折角文档 + 两条横线）
- `DocumentBlankIcon` — Heroicons v1 document outline（空白折角文档）

### knip \`@public\` tag
ExampleShowcase/** 在 \`knip.config.ts\` 的 \`ignore\` 列表里（"legacy modules preserved for reactivation"）。6 个新 wrapper 唯一消费方都在这个 frozen 目录，没有 tag 的话 knip 会标记为 "unused exports"。按仓库约定（见 \`knip.config.ts\` 中 \`tags: ['-public']\` 说明）给 wrapper source 文件 + \`index.ts\` barrel re-export 都加 \`@public\` JSDoc。

### 复用 wrapper (7)
已 diff \`strokeWidth\` / \`strokeLinecap\` / \`strokeLinejoin\` / element type 确认**完全一致**再复用：`CheckIcon`, `CloseIcon`, `EyeIcon`, `PhotoIcon`, `PhotoThickIcon`, `PlayIcon`, `SearchPlusIcon`.

## Test plan

- [x] \`pnpm lint\` — clean
- [x] \`npx tsc --noEmit\` — clean
- [x] \`pnpm lint:ci\` — knip hard gates (files/exports/dep-health) pass
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` — 68 → 61 ✅
- [x] \`bash scripts/check-ignores-shrink-only.sh\` — 45 → 45 ✅
- [x] \`bash scripts/check-no-raw-fetch-shrink-only.sh\` — 7 → 7 ✅
- [ ] 视觉回归（staging）：ExampleShowcase 不在当前 UI 主路径（legacy module），但若通过 AgentChatClient 某条路径能 surface preview modal，需要对比 Creative Material / Gen Media PDP / Creatify 三种 preview 的 result/source-assets/prompt 三段 icon。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): svg-inline — AgentChatClient/components (10 files, 28 svgs) (#1327)

- **SHA**: `f9315c4d9e798509fc9c0bff62734cb08b1f1df2`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T14:16:23Z
- **PR**: #1327

### Commit Message

```
refactor(web): svg-inline — AgentChatClient/components (10 files, 28 svgs) (#1327)

## Summary

继续 SVG 治理系列 (PR #9 of the series) — 清理
`src/components/AgentChatClient/components/` 目录下 10 个文件的 28 处 inline
`<svg>`。svg-inline baseline 从 **78 → 68**。

### 迁移文件 (10)
- `ExamplePromptGrid.tsx` (6) — PhotoIcon ×2, PlayIcon, EyeIcon,
InfoSolidIcon, ChevronRightPathIcon
- `TaskStatusIndicator.tsx` (5) — RefreshIcon ×3, InfoCircleIcon,
WarningCircleTallIcon
- `InputArea.tsx` (4) — SpinnerIcon, PaperclipIcon, StopSquareIcon,
PaperPlaneIcon
- `PageHeader.tsx` (3) — PencilSquareIcon, PlusLargeIcon, PhotoThickIcon
- `FunctionCallDisplay.tsx` (3) — InfoSolidIcon, ChevronDownSolidIcon,
BoltSolidIcon
- `LoadingStates.tsx` (2) — LockIcon, SpinnerIcon
- `UploadButton.tsx` (2) — SpinnerIcon, PaperclipThinIcon
- `ReadOnlyBanner.tsx` (1) — WarningTriangleIcon
- `PlaybackBanner.tsx` (1) — PlayCircleIcon
- `SendButton.tsx` (1) — PaperPlaneIcon

### 新增 wrapper (7)
所有 wrapper 均逐字节保留源 svg 的 `path` / `viewBox` / `fill` / `stroke` /
`strokeWidth` / `strokeLinecap` / `strokeLinejoin`：

- `EyeIcon` — Heroicons outline eye (stroke=2)
- `InfoSolidIcon` — Heroicons mini info-circle solid (20×20, i-shape
dot-on-top) — 与 `AlertSolidIcon`（exclamation !）区分
- `InfoCircleIcon` — outline info 圆圈（i-shape，stroke=2）— 与
`WarningCircleIcon` (exclamation) 区分
- `LockIcon` — Heroicons lock-closed outline (stroke=1.5)
- `PaperclipThinIcon` — path 同 `PaperclipIcon`，但 stroke=1.5 (对比 1.75)，匹配
`UploadButton` 的 h-[18px]
- `PencilSquareIcon` — Heroicons pencil-square (stroke=2) — 与
`PencilIcon`（Feather style, stroke=1.5）区分
- `PlayCircleIcon` — play triangle 加 circle outline — 与 `PlayIcon`（bare
triangle, fill）区分

### 复用 wrapper (14)
已 diff `strokeWidth` / `strokeLinecap` / `strokeLinejoin` / element
type（path vs polyline）确认**完全一致**再复用（按 memory
`feedback_wrapper_reuse_byte_exact.md` 规则）：`ChevronRightPathIcon`,
`PhotoIcon`, `PlayIcon`, `RefreshIcon`, `WarningCircleTallIcon`,
`PaperPlaneIcon`, `PaperclipIcon`, `SpinnerIcon`, `StopSquareIcon`,
`PhotoThickIcon`, `PlusLargeIcon`, `BoltSolidIcon`,
`ChevronDownSolidIcon`, `WarningTriangleIcon`.

## Test plan

- [x] `pnpm lint` — clean
- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint:ci` — knip hard gates (files/exports/dep-health) pass
- [x] `bash scripts/check-svg-ignores-shrink-only.sh` — 78 → 68 ✅
- [x] `bash scripts/check-ignores-shrink-only.sh` — 45 → 45 ✅
- [x] `bash scripts/check-no-raw-fetch-shrink-only.sh` — 7 → 7 ✅
- [ ] Visual 0 diff in staging (ecommerce-studio-web-staging) —
AgentChatClient chat surfaces: welcome / prompt grid, input area (upload
/ send / stop), page header (edit-title / new-task / assets toggle),
playback + readonly banners, task-in-progress +
network/conversation-failed banners, loading + needs-login states.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

继续 SVG 治理系列 (PR #9 of the series) — 清理 `src/components/AgentChatClient/components/` 目录下 10 个文件的 28 处 inline `<svg>`。svg-inline baseline 从 **78 → 68**。

### 迁移文件 (10)
- `ExamplePromptGrid.tsx` (6) — PhotoIcon ×2, PlayIcon, EyeIcon, InfoSolidIcon, ChevronRightPathIcon
- `TaskStatusIndicator.tsx` (5) — RefreshIcon ×3, InfoCircleIcon, WarningCircleTallIcon
- `InputArea.tsx` (4) — SpinnerIcon, PaperclipIcon, StopSquareIcon, PaperPlaneIcon
- `PageHeader.tsx` (3) — PencilSquareIcon, PlusLargeIcon, PhotoThickIcon
- `FunctionCallDisplay.tsx` (3) — InfoSolidIcon, ChevronDownSolidIcon, BoltSolidIcon
- `LoadingStates.tsx` (2) — LockIcon, SpinnerIcon
- `UploadButton.tsx` (2) — SpinnerIcon, PaperclipThinIcon
- `ReadOnlyBanner.tsx` (1) — WarningTriangleIcon
- `PlaybackBanner.tsx` (1) — PlayCircleIcon
- `SendButton.tsx` (1) — PaperPlaneIcon

### 新增 wrapper (7)
所有 wrapper 均逐字节保留源 svg 的 `path` / `viewBox` / `fill` / `stroke` / `strokeWidth` / `strokeLinecap` / `strokeLinejoin`：

- `EyeIcon` — Heroicons outline eye (stroke=2)
- `InfoSolidIcon` — Heroicons mini info-circle solid (20×20, i-shape dot-on-top) — 与 `AlertSolidIcon`（exclamation !）区分
- `InfoCircleIcon` — outline info 圆圈（i-shape，stroke=2）— 与 `WarningCircleIcon` (exclamation) 区分
- `LockIcon` — Heroicons lock-closed outline (stroke=1.5)
- `PaperclipThinIcon` — path 同 `PaperclipIcon`，但 stroke=1.5 (对比 1.75)，匹配 `UploadButton` 的 h-[18px]
- `PencilSquareIcon` — Heroicons pencil-square (stroke=2) — 与 `PencilIcon`（Feather style, stroke=1.5）区分
- `PlayCircleIcon` — play triangle 加 circle outline — 与 `PlayIcon`（bare triangle, fill）区分

### 复用 wrapper (14)
已 diff `strokeWidth` / `strokeLinecap` / `strokeLinejoin` / element type（path vs polyline）确认**完全一致**再复用（按 memory `feedback_wrapper_reuse_byte_exact.md` 规则）：`ChevronRightPathIcon`, `PhotoIcon`, `PlayIcon`, `RefreshIcon`, `WarningCircleTallIcon`, `PaperPlaneIcon`, `PaperclipIcon`, `SpinnerIcon`, `StopSquareIcon`, `PhotoThickIcon`, `PlusLargeIcon`, `BoltSolidIcon`, `ChevronDownSolidIcon`, `WarningTriangleIcon`.

## Test plan

- [x] `pnpm lint` — clean
- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint:ci` — knip hard gates (files/exports/dep-health) pass
- [x] `bash scripts/check-svg-ignores-shrink-only.sh` — 78 → 68 ✅
- [x] `bash scripts/check-ignores-shrink-only.sh` — 45 → 45 ✅
- [x] `bash scripts/check-no-raw-fetch-shrink-only.sh` — 7 → 7 ✅
- [ ] Visual 0 diff in staging (ecommerce-studio-web-staging) — AgentChatClient chat surfaces: welcome / prompt grid, input area (upload / send / stop), page header (edit-title / new-task / assets toggle), playback + readonly banners, task-in-progress + network/conversation-failed banners, loading + needs-login states.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(web): components-4 — finish top-level components (AssetsPanel + SupportTicketModal) (#1325)

- **SHA**: `923da54dbb2b545f0eff3bc9fa38699e9cf5898e`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T13:53:24Z
- **PR**: #1325

### Commit Message

```
feat(web): components-4 — finish top-level components (AssetsPanel + SupportTicketModal) (#1325)

## Summary

Continues #1321 / #1323. Migrates the last 2 non-special top-level
\`components/\` files (13 svg occurrences) to \`ui/icons/\` wrappers and
shrinks the \`svg-inline\` baseline from **80 → 78**. Top-level
\`components/*.tsx\` baseline now empty except \`ProviderLogo\` (30
brand logos — separate PR) and \`UserAvatar\` (pre-existing dead code).

## Files migrated

| File | svgs | wrappers |
|---|---|---|
| \`AssetsPanel.tsx\` | 9 | ChevronRightPathIcon (reused),
PhotoThickIcon, WarningCircleTallIcon, SearchPlusIcon, DownloadThickIcon
×2, SpinnerIcon (reused), CheckSolidIcon (reused), PlusLargeIcon |
| \`SupportTicketModal.tsx\` | 4 | SupportOwlIcon, SupportRaccoonIcon,
SupportFoxIcon (3 mascot illustrations) + CloseIcon (reused) |

## Stroke/element diff against existing wrappers (per #1323 lesson)

Per the PR #1323 learning, every reused wrapper here was diffed against
the original svg for \`strokeWidth\` / \`strokeLinecap\` /
\`strokeLinejoin\` / element-type before reuse. Where mismatches
existed, a new byte-exact variant wrapper was created instead of
reusing:

- AssetsPanel original \`PhotoIcon\` is **stroke=2** (not the existing
\`PhotoIcon\` stroke=1.5) → new \`PhotoThickIcon\`
- AssetsPanel original \`DownloadIcon\` is **stroke=2** (not the
existing \`DownloadIcon\` stroke=1.5) → new \`DownloadThickIcon\`
- AssetsPanel original exclamation-circle has taller \`!\` (y=8..12)
than \`WarningCircleIcon\` (y=9..11) → new \`WarningCircleTallIcon\`
- AssetsPanel original \`+\` has wider span (\`M12 4v16m8-8H4\`) than
\`PlusIcon\` (\`M12 6v6m0 0v6m0-6h6m-6 0H6\`) → new \`PlusLargeIcon\`

Verified byte-exact reuses: \`ChevronRightPathIcon\`, \`SpinnerIcon\`,
\`CheckSolidIcon\`, \`CloseIcon\`.

## SupportTicketModal mascots

\`SupportTicketModal.tsx\` had a local \`SupportIllustration\` switch
function returning 3 hand-drawn 88x80 SVG mascots (each ~30 lines of
paths/circles/ellipses with hardcoded brand-color hexes). Each extracted
as a self-contained wrapper:

- \`SupportOwlIcon\` — owl + magnifying glass, brown tones (bug-report)
- \`SupportRaccoonIcon\` — raccoon + receipt, gray tones (billing)
- \`SupportFoxIcon\` — fox + lightbulb, orange tones (suggestion /
default)

The local \`SupportIllustration\` switch function was kept (rewritten to
dispatch to the 3 wrappers) so the call-site API doesn't change.

## Visual fidelity: 0 risk

All wrappers preserve \`path\` / \`viewBox\` / \`fill\` / \`stroke\` /
\`strokeWidth\` / \`strokeLinecap\` / \`strokeLinejoin\` byte-for-byte.

## Test plan

- [x] \`pnpm lint\` clean
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint:ci\` clean (\`✓ All web/ ci-lint checks passed\`)
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` shows 80 → 78 (✓
shrink, exactly 2 files)
- [x] Sibling shrink scripts (react/forbid-dom-props 45→45, no-raw-fetch
8→8) unchanged
- [x] Both migrated files: \`grep -c '<svg'\` returns 0
- [x] Related unit tests pass (AssetsPanel + SupportTicketModal — 13
tests)
- [ ] Visual regression on staging: assets panel (empty / error /
per-asset toolbar download/zoom/spinner/check), support ticket modal (3
mascots × bug/billing/suggestion, close X) — each pixel-identical to
main

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Continues #1321 / #1323. Migrates the last 2 non-special top-level \`components/\` files (13 svg occurrences) to \`ui/icons/\` wrappers and shrinks the \`svg-inline\` baseline from **80 → 78**. Top-level \`components/*.tsx\` baseline now empty except \`ProviderLogo\` (30 brand logos — separate PR) and \`UserAvatar\` (pre-existing dead code).

## Files migrated

| File | svgs | wrappers |
|---|---|---|
| \`AssetsPanel.tsx\` | 9 | ChevronRightPathIcon (reused), PhotoThickIcon, WarningCircleTallIcon, SearchPlusIcon, DownloadThickIcon ×2, SpinnerIcon (reused), CheckSolidIcon (reused), PlusLargeIcon |
| \`SupportTicketModal.tsx\` | 4 | SupportOwlIcon, SupportRaccoonIcon, SupportFoxIcon (3 mascot illustrations) + CloseIcon (reused) |

## Stroke/element diff against existing wrappers (per #1323 lesson)

Per the PR #1323 learning, every reused wrapper here was diffed against the original svg for \`strokeWidth\` / \`strokeLinecap\` / \`strokeLinejoin\` / element-type before reuse. Where mismatches existed, a new byte-exact variant wrapper was created instead of reusing:

- AssetsPanel original \`PhotoIcon\` is **stroke=2** (not the existing \`PhotoIcon\` stroke=1.5) → new \`PhotoThickIcon\`
- AssetsPanel original \`DownloadIcon\` is **stroke=2** (not the existing \`DownloadIcon\` stroke=1.5) → new \`DownloadThickIcon\`
- AssetsPanel original exclamation-circle has taller \`!\` (y=8..12) than \`WarningCircleIcon\` (y=9..11) → new \`WarningCircleTallIcon\`
- AssetsPanel original \`+\` has wider span (\`M12 4v16m8-8H4\`) than \`PlusIcon\` (\`M12 6v6m0 0v6m0-6h6m-6 0H6\`) → new \`PlusLargeIcon\`

Verified byte-exact reuses: \`ChevronRightPathIcon\`, \`SpinnerIcon\`, \`CheckSolidIcon\`, \`CloseIcon\`.

## SupportTicketModal mascots

\`SupportTicketModal.tsx\` had a local \`SupportIllustration\` switch function returning 3 hand-drawn 88x80 SVG mascots (each ~30 lines of paths/circles/ellipses with hardcoded brand-color hexes). Each extracted as a self-contained wrapper:

- \`SupportOwlIcon\` — owl + magnifying glass, brown tones (bug-report)
- \`SupportRaccoonIcon\` — raccoon + receipt, gray tones (billing)
- \`SupportFoxIcon\` — fox + lightbulb, orange tones (suggestion / default)

The local \`SupportIllustration\` switch function was kept (rewritten to dispatch to the 3 wrappers) so the call-site API doesn't change.

## Visual fidelity: 0 risk

All wrappers preserve \`path\` / \`viewBox\` / \`fill\` / \`stroke\` / \`strokeWidth\` / \`strokeLinecap\` / \`strokeLinejoin\` byte-for-byte.

## Test plan

- [x] \`pnpm lint\` clean
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint:ci\` clean (\`✓ All web/ ci-lint checks passed\`)
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` shows 80 → 78 (✓ shrink, exactly 2 files)
- [x] Sibling shrink scripts (react/forbid-dom-props 45→45, no-raw-fetch 8→8) unchanged
- [x] Both migrated files: \`grep -c '<svg'\` returns 0
- [x] Related unit tests pass (AssetsPanel + SupportTicketModal — 13 tests)
- [ ] Visual regression on staging: assets panel (empty / error / per-asset toolbar download/zoom/spinner/check), support ticket modal (3 mascots × bug/billing/suggestion, close X) — each pixel-identical to main

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): lib/auth/api → apiClient (RQ PR 6) (#1324)

- **SHA**: `49370b98dc72a9b059161d5a84c9439a037d2e11`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T13:45:06Z
- **PR**: #1324

### Commit Message

```
refactor(web): lib/auth/api → apiClient (RQ PR 6) (#1324)

## Summary

Sixth domain migration. The 5 account-service helpers in
\`lib/auth/api.ts\` move from raw \`fetch\` to \`apiClient.post/get\`.
UI callers and \`manager.ts\` stay imperative — login is critical path
and useMutation wrapping wins little here (\`manager.ts\` is a non-React
class; React callers manage simple state).

- **\`lib/auth/api.ts\`** — \`withBusiness(url)\` helper for the shared
\`?business=ecap\` query param. \`sendEmailOTP\` / \`verifyEmailOTP\` /
\`getAnonymousToken\` use \`apiClient.post\`. \`exchangeAuth\` passes a
custom \`fb-token\` header. \`getUserMe\` passes a caller-supplied
\`Authorization\` header (account flows can have a different token from
the persisted one during refresh / multi-account). Zod parsing
preserved.
- **\`lib/api/client.ts\`** — exports \`apiClient\` (was private). Error
extraction now falls back from \`errorData.message\` to
\`errorData.detail\` to match the account-service shape (and the
precedence already used by \`lib/api/backend.ts::callAPI\`).
- **ESLint SHRINK-ONLY** — \`lib/auth/api.ts\` removed (8 → 7
transitional).
- **Tests** — existing 13-case spec rewritten to use proper \`Response\`
objects (apiClient calls \`response.headers.get\`; old plain mocks
crashed) and match \`ApiError\` messages. All edge cases preserved.

**Why no useMutation wrapping**: \`manager.ts\` can't use hooks (it's a
class). \`LoginForm\` + verify page have simple loading state that
doesn't materially benefit from RQ — wrapping would add ceremony without
removing any useEffect (these are event-handler triggered).

Spec:
[\`docs/superpowers/specs/2026-04-24-react-query-migration.md\`](docs/superpowers/specs/2026-04-24-react-query-migration.md).

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm lint:ci\` clean (knip dep-health hard gate)
- [x] Rewritten \`auth/api.unit.spec.ts\` 13/13 pass
- [x] \`pnpm test:unit\` full run — 262 files / 4169 tests pass
- [ ] Local \`pnpm dev\`: email-OTP login round-trip; anonymous flow;
user/me hydration after login
- [ ] Staging visual regression (login is critical path)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Sixth domain migration. The 5 account-service helpers in \`lib/auth/api.ts\` move from raw \`fetch\` to \`apiClient.post/get\`. UI callers and \`manager.ts\` stay imperative — login is critical path and useMutation wrapping wins little here (\`manager.ts\` is a non-React class; React callers manage simple state).

- **\`lib/auth/api.ts\`** — \`withBusiness(url)\` helper for the shared \`?business=ecap\` query param. \`sendEmailOTP\` / \`verifyEmailOTP\` / \`getAnonymousToken\` use \`apiClient.post\`. \`exchangeAuth\` passes a custom \`fb-token\` header. \`getUserMe\` passes a caller-supplied \`Authorization\` header (account flows can have a different token from the persisted one during refresh / multi-account). Zod parsing preserved.
- **\`lib/api/client.ts\`** — exports \`apiClient\` (was private). Error extraction now falls back from \`errorData.message\` to \`errorData.detail\` to match the account-service shape (and the precedence already used by \`lib/api/backend.ts::callAPI\`).
- **ESLint SHRINK-ONLY** — \`lib/auth/api.ts\` removed (8 → 7 transitional).
- **Tests** — existing 13-case spec rewritten to use proper \`Response\` objects (apiClient calls \`response.headers.get\`; old plain mocks crashed) and match \`ApiError\` messages. All edge cases preserved.

**Why no useMutation wrapping**: \`manager.ts\` can't use hooks (it's a class). \`LoginForm\` + verify page have simple loading state that doesn't materially benefit from RQ — wrapping would add ceremony without removing any useEffect (these are event-handler triggered).

Spec: [\`docs/superpowers/specs/2026-04-24-react-query-migration.md\`](docs/superpowers/specs/2026-04-24-react-query-migration.md).

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm lint:ci\` clean (knip dep-health hard gate)
- [x] Rewritten \`auth/api.unit.spec.ts\` 13/13 pass
- [x] \`pnpm test:unit\` full run — 262 files / 4169 tests pass
- [ ] Local \`pnpm dev\`: email-OTP login round-trip; anonymous flow; user/me hydration after login
- [ ] Staging visual regression (login is critical path)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(web): restore byte-exact stroke widths on 3 migrated svgs (#1323)

- **SHA**: `ecbf13c93730068c2214dc1b25370a2f0ae70807`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T13:32:55Z
- **PR**: #1323

### Commit Message

```
fix(web): restore byte-exact stroke widths on 3 migrated svgs (#1323)

## Summary

Review audit on #1321 surfaced two wrapper reuses that broke the "0
visual risk" promise because the reused wrapper's \`strokeWidth\`
differed from the original inline svg. One additional mismatch from
#1313 had gone un-flagged (different SVG element type entirely). All
three fixed here.

## Visual regressions fixed

| File | PR | original | merged wrapper | fix |
|---|---|---|---|---|
| \`ImagePreview.tsx\` close button | #1321 | \`strokeWidth={1.5}\` |
\`CloseIcon\` (stroke=2) | new \`CloseThinIcon\` (stroke=1.5) |
| \`ClawPageHeader.tsx\` folder button | #1321 | \`strokeWidth={2}\` |
\`FolderIcon\` (stroke=1.75) | new \`FolderThickIcon\` (stroke=2) |
| \`workspace-shared.tsx\` FileRow chevron | #1313 | path \`M9 5l7 7-7
7\` stroke=2 linecap=round | \`ChevronRightIcon\` (polyline, flat
endpoints) | use \`ChevronRightPathIcon\` (introduced in #1316 for this
exact shape — I missed updating workspace-shared at that time) |

### Why these matter

1. **ImagePreview X** at h-5 w-5: stroke 2 vs 1.5 is ~33% thicker —
reads as a heavier X in production since PR #1321.
2. **ClawPageHeader folder** at h-4 w-4: stroke 1.75 vs 2 is a slight
thinning — barely visible but technically a regression.
3. **workspace-shared chevron**: the polyline (\`9 18 15 12 9 6\`) has
different geometry from the path (\`M9 5l7 7-7 7\`) — different aspect
ratio AND the polyline uses default flat endpoints while the path used
\`strokeLinecap="round"\`. At h-3.5 w-3.5 in the file tree this is
visible on close inspection.

## New wrappers (2)

- \`CloseThinIcon\`: same path as \`CloseIcon\`, strokeWidth=1.5 (vs 2).
Joins the CloseIcon family alongside \`CloseLineIcon\`,
\`CloseLineThickIcon\`, \`CloseTinyIcon\`, \`CloseMicroIcon\` — each
preserves a distinct source byte-exact.
- \`FolderThickIcon\`: same path as \`FolderIcon\`, strokeWidth=2 (vs
1.75).

## What changed (3 files)

- \`src/components/ImagePreview.tsx\`: \`CloseIcon\` → \`CloseThinIcon\`
- \`src/components/ClawPageHeader.tsx\`: \`FolderIcon\` →
\`FolderThickIcon\`
- \`src/app/[locale]/chat/components/workspace-shared.tsx\`:
\`ChevronRightIcon\` → \`ChevronRightPathIcon\`

No new baseline entries; \`svg-inline\` baseline unchanged (80 → 80).

## Process learning

This is a tax on our byte-exact promise: when reusing an existing
wrapper, I need to diff the wrapper against the original svg (not just
path — also \`strokeWidth\`, \`strokeLinecap\`, \`strokeLinejoin\`, and
any element-type differences like polyline vs path). Caller-side
\`className\` can override stroke via Tailwind utilities (\`stroke-2\`),
but not reliably across all browsers/SVG prop inheritance — new wrappers
are the safer path. Will do this diff-check more carefully on remaining
migrations.

## Test plan

- [x] \`pnpm lint\` clean
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint:ci\` clean (\`✓ All web/ ci-lint checks passed\`)
- [x] Shrink scripts unchanged (svg-inline 80→80, react/forbid-dom-props
45→45, no-raw-fetch 8→8)
- [ ] Visual spot-check on staging: image preview X size, claw page
header folder, resources panel file tree chevrons — should match
pre-#1321/#1313 pixel-identically

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Review audit on #1321 surfaced two wrapper reuses that broke the "0 visual risk" promise because the reused wrapper's \`strokeWidth\` differed from the original inline svg. One additional mismatch from #1313 had gone un-flagged (different SVG element type entirely). All three fixed here.

## Visual regressions fixed

| File | PR | original | merged wrapper | fix |
|---|---|---|---|---|
| \`ImagePreview.tsx\` close button | #1321 | \`strokeWidth={1.5}\` | \`CloseIcon\` (stroke=2) | new \`CloseThinIcon\` (stroke=1.5) |
| \`ClawPageHeader.tsx\` folder button | #1321 | \`strokeWidth={2}\` | \`FolderIcon\` (stroke=1.75) | new \`FolderThickIcon\` (stroke=2) |
| \`workspace-shared.tsx\` FileRow chevron | #1313 | path \`M9 5l7 7-7 7\` stroke=2 linecap=round | \`ChevronRightIcon\` (polyline, flat endpoints) | use \`ChevronRightPathIcon\` (introduced in #1316 for this exact shape — I missed updating workspace-shared at that time) |

### Why these matter

1. **ImagePreview X** at h-5 w-5: stroke 2 vs 1.5 is ~33% thicker — reads as a heavier X in production since PR #1321.
2. **ClawPageHeader folder** at h-4 w-4: stroke 1.75 vs 2 is a slight thinning — barely visible but technically a regression.
3. **workspace-shared chevron**: the polyline (\`9 18 15 12 9 6\`) has different geometry from the path (\`M9 5l7 7-7 7\`) — different aspect ratio AND the polyline uses default flat endpoints while the path used \`strokeLinecap="round"\`. At h-3.5 w-3.5 in the file tree this is visible on close inspection.

## New wrappers (2)

- \`CloseThinIcon\`: same path as \`CloseIcon\`, strokeWidth=1.5 (vs 2). Joins the CloseIcon family alongside \`CloseLineIcon\`, \`CloseLineThickIcon\`, \`CloseTinyIcon\`, \`CloseMicroIcon\` — each preserves a distinct source byte-exact.
- \`FolderThickIcon\`: same path as \`FolderIcon\`, strokeWidth=2 (vs 1.75).

## What changed (3 files)

- \`src/components/ImagePreview.tsx\`: \`CloseIcon\` → \`CloseThinIcon\`
- \`src/components/ClawPageHeader.tsx\`: \`FolderIcon\` → \`FolderThickIcon\`
- \`src/app/[locale]/chat/components/workspace-shared.tsx\`: \`ChevronRightIcon\` → \`ChevronRightPathIcon\`

No new baseline entries; \`svg-inline\` baseline unchanged (80 → 80).

## Process learning

This is a tax on our byte-exact promise: when reusing an existing wrapper, I need to diff the wrapper against the original svg (not just path — also \`strokeWidth\`, \`strokeLinecap\`, \`strokeLinejoin\`, and any element-type differences like polyline vs path). Caller-side \`className\` can override stroke via Tailwind utilities (\`stroke-2\`), but not reliably across all browsers/SVG prop inheritance — new wrappers are the safer path. Will do this diff-check more carefully on remaining migrations.

## Test plan

- [x] \`pnpm lint\` clean
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint:ci\` clean (\`✓ All web/ ci-lint checks passed\`)
- [x] Shrink scripts unchanged (svg-inline 80→80, react/forbid-dom-props 45→45, no-raw-fetch 8→8)
- [ ] Visual spot-check on staging: image preview X size, claw page header folder, resources panel file tree chevrons — should match pre-#1321/#1313 pixel-identically

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(subscription-code): grant credits + fix start_date on active subs (#1318)

- **SHA**: `a02d3c36ecce04f8f1df4b8c06844c7aed17a1a6`
- **作者**: tim-srp
- **日期**: 2026-04-24T13:21:01Z
- **PR**: #1318

### Commit Message

```
fix(subscription-code): grant credits + fix start_date on active subs (#1318)

## Summary

Fixes two post-merge regressions from #1270 (subscription code redeem)
that are currently live in production:

### 1. Credits never arrive on redeem (the one you just reproduced)
`redeem_subscription_code` was calling `subscribe()` +
`update_team_models()` + `user_repo.update_fields()`, but **never topped
up the subscription wallet** (`wallet_subscription_id`). The plan badge
flipped to the new tier, but the user's credit balance was untouched.

Fix mirrors `stripe/billing_gateway.py:181-213`: after `subscribe()`,
call `billing_client.topup_wallet(wallet_id=wallet_subscription_id,
granted_credits=PLAN_CREDITS[plan_tier])` — `4800` for starter, `20000`
for pro, `40000` for ultra. On `404/422` (terminated/missing wallet) →
`recover_wallets_and_reread` + one retry; if recovery still can't
produce a wallet_id, raise `ServiceError` so the caller's rollback
branch unwinds the activation (avoids a silent credits-less
subscription).

The top-up logic is extracted into `_topup_subscription_wallet` so the
caller drops below the McCabe-20 complexity gate.

### 2. `start_date` sent to BG for already-subscribed users
`has_active_sub` was derived from `credits_info.get("plan")`, but BG's
`check_credits` response does **not** include a `plan` field (only
`{enough, available_credits, wallets, current_period_end, ...}`). So
`has_active_sub` was always `False`, `start_date` was always sent, and
BG rejected any active-subscriber retest with:

> `400 start_date is only supported when creating a new subscription`

Fix: derive `has_active_sub` from BG's own 400 signal (the only reliable
ground-truth we have), and read the current tier from the local user
doc's `plan` field — same single source of truth
`stripe/entitlement.py:372` uses via `BG_NO_SUBSCRIPTION_STATUSES`.

## Files
- `services/claw-interface/app/services/subscription_code.py` — credits
top-up + data-source fix + helper extraction
- `services/claw-interface/tests/unit/test_subscription_code.py` — mocks
realigned to new data source; happy-path asserts `topup_wallet` called
with `PLAN_CREDITS["pro"] = 20000` on `wallet-sub-123`

## Local verification
- `pytest tests/unit/test_subscription_code.py` — 12/12 pass
- `ruff check` / `ruff format --check` — clean
- `pyright app/ tests/` — `0 errors, 0 warnings, 0 informations`
- `scripts/ci-lint/03-complexity.sh` — `redeem_subscription_code` no
longer appears as a violation (was 22 > 20)

## Test plan
- [ ] CI all green (lint-and-typecheck was the original blocker on #1289
— this PR's squashed diff passes locally)
- [ ] Staging redeem against new-user case (BG returns 400 on
check_credits) → verify continues as rank=0, credits =
`PLAN_CREDITS[tier]`, no BG 400 on subscribe
- [ ] Staging redeem against active-subscriber case (BG already has
subscription) → verify no `start_date` 400, credits stack on existing
balance
- [ ] Staging redeem UI: subscription wallet balance increases by
`PLAN_CREDITS[tier]` after redeem

## Relation to #1289
This is a fresh PR with the same net content as #1289 squashed into a
single commit. #1289 can be closed once this lands; no need to carry
both.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Fixes two post-merge regressions from #1270 (subscription code redeem) that are currently live in production:

### 1. Credits never arrive on redeem (the one you just reproduced)
`redeem_subscription_code` was calling `subscribe()` + `update_team_models()` + `user_repo.update_fields()`, but **never topped up the subscription wallet** (`wallet_subscription_id`). The plan badge flipped to the new tier, but the user's credit balance was untouched.

Fix mirrors `stripe/billing_gateway.py:181-213`: after `subscribe()`, call `billing_client.topup_wallet(wallet_id=wallet_subscription_id, granted_credits=PLAN_CREDITS[plan_tier])` — `4800` for starter, `20000` for pro, `40000` for ultra. On `404/422` (terminated/missing wallet) → `recover_wallets_and_reread` + one retry; if recovery still can't produce a wallet_id, raise `ServiceError` so the caller's rollback branch unwinds the activation (avoids a silent credits-less subscription).

The top-up logic is extracted into `_topup_subscription_wallet` so the caller drops below the McCabe-20 complexity gate.

### 2. `start_date` sent to BG for already-subscribed users
`has_active_sub` was derived from `credits_info.get("plan")`, but BG's `check_credits` response does **not** include a `plan` field (only `{enough, available_credits, wallets, current_period_end, ...}`). So `has_active_sub` was always `False`, `start_date` was always sent, and BG rejected any active-subscriber retest with:

> `400 start_date is only supported when creating a new subscription`

Fix: derive `has_active_sub` from BG's own 400 signal (the only reliable ground-truth we have), and read the current tier from the local user doc's `plan` field — same single source of truth `stripe/entitlement.py:372` uses via `BG_NO_SUBSCRIPTION_STATUSES`.

## Files
- `services/claw-interface/app/services/subscription_code.py` — credits top-up + data-source fix + helper extraction
- `services/claw-interface/tests/unit/test_subscription_code.py` — mocks realigned to new data source; happy-path asserts `topup_wallet` called with `PLAN_CREDITS["pro"] = 20000` on `wallet-sub-123`

## Local verification
- `pytest tests/unit/test_subscription_code.py` — 12/12 pass
- `ruff check` / `ruff format --check` — clean
- `pyright app/ tests/` — `0 errors, 0 warnings, 0 informations`
- `scripts/ci-lint/03-complexity.sh` — `redeem_subscription_code` no longer appears as a violation (was 22 > 20)

## Test plan
- [ ] CI all green (lint-and-typecheck was the original blocker on #1289 — this PR's squashed diff passes locally)
- [ ] Staging redeem against new-user case (BG returns 400 on check_credits) → verify continues as rank=0, credits = `PLAN_CREDITS[tier]`, no BG 400 on subscribe
- [ ] Staging redeem against active-subscriber case (BG already has subscription) → verify no `start_date` 400, credits stack on existing balance
- [ ] Staging redeem UI: subscription wallet balance increases by `PLAN_CREDITS[tier]` after redeem

## Relation to #1289
This is a fresh PR with the same net content as #1289 squashed into a single commit. #1289 can be closed once this lands; no need to carry both.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): useMattermostIntegration → fetchMmBlob (RQ PR 5) (#1322)

- **SHA**: `b78ed2d56f8e75ca5537ea785accb6d04808df7a`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T13:19:29Z
- **PR**: #1322

### Commit Message

```
refactor(web): useMattermostIntegration → fetchMmBlob (RQ PR 5) (#1322)

## Summary

Fifth domain migration of the React Query rollout. Much smaller than the
300-500 line spec estimate — this 306-line hook only contains **one**
raw \`fetch\` (in \`attachExistingMmFile\`), and PR 2 already extracted
exactly that operation into \`lib/mattermost/blob.ts::fetchMmBlob\`.

- **\`attachExistingMmFile\` simplified** — inline
\`globalThis.fetch(url, { Authorization: Bearer })\` + \`res.blob()\` +
manual \`!res.ok\` check replaced with one \`await fetchMmBlob(url,
token)\`. Same throw-on-non-2xx semantics, same Bearer-only headers.
- **Everything else** — local state (\`mmAttachments\`,
AbortControllers, refs) and MM api service wrapper calls already route
through allowlisted code; no further changes needed.
- **ESLint SHRINK-ONLY** — \`useMattermostIntegration.ts\` removed (9 →
8 transitional).

Spec:
[\`docs/superpowers/specs/2026-04-24-react-query-migration.md\`](docs/superpowers/specs/2026-04-24-react-query-migration.md).

**Why no new tests**: \`fetchMmBlob\` has full coverage in PR 2's spec
(\`tests/unit/hooks/queries/mm/useAuthBlob.unit.spec.tsx\` indirectly +
the helper itself). The caller behavior visible from the test surface
(mmAttachments transitions, error path) is unchanged.
\`attachExistingMmFile\` was uncovered before this PR — adding tests now
is scope creep for a behavior-preserving substitution.

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm lint:ci\` clean (knip dep-health hard gate)
- [x] \`pnpm test:unit\` — useMattermostIntegration's existing 26 tests
pass; only 2 pre-existing admin auth flakies (unrelated)
- [ ] Local \`pnpm dev\` — open chat, attach an existing MM file via the
upload popover; confirm preview + final attachment work the same as
before

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Fifth domain migration of the React Query rollout. Much smaller than the 300-500 line spec estimate — this 306-line hook only contains **one** raw \`fetch\` (in \`attachExistingMmFile\`), and PR 2 already extracted exactly that operation into \`lib/mattermost/blob.ts::fetchMmBlob\`.

- **\`attachExistingMmFile\` simplified** — inline \`globalThis.fetch(url, { Authorization: Bearer })\` + \`res.blob()\` + manual \`!res.ok\` check replaced with one \`await fetchMmBlob(url, token)\`. Same throw-on-non-2xx semantics, same Bearer-only headers.
- **Everything else** — local state (\`mmAttachments\`, AbortControllers, refs) and MM api service wrapper calls already route through allowlisted code; no further changes needed.
- **ESLint SHRINK-ONLY** — \`useMattermostIntegration.ts\` removed (9 → 8 transitional).

Spec: [\`docs/superpowers/specs/2026-04-24-react-query-migration.md\`](docs/superpowers/specs/2026-04-24-react-query-migration.md).

**Why no new tests**: \`fetchMmBlob\` has full coverage in PR 2's spec (\`tests/unit/hooks/queries/mm/useAuthBlob.unit.spec.tsx\` indirectly + the helper itself). The caller behavior visible from the test surface (mmAttachments transitions, error path) is unchanged. \`attachExistingMmFile\` was uncovered before this PR — adding tests now is scope creep for a behavior-preserving substitution.

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm lint:ci\` clean (knip dep-health hard gate)
- [x] \`pnpm test:unit\` — useMattermostIntegration's existing 26 tests pass; only 2 pre-existing admin auth flakies (unrelated)
- [ ] Local \`pnpm dev\` — open chat, attach an existing MM file via the upload popover; confirm preview + final attachment work the same as before

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(web): components-3 — extract 25 inline <svg> across 4 components (#1321)

- **SHA**: `461b6bb14da649c4013d536382a722ea0489dbad`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T13:17:57Z
- **PR**: #1321

### Commit Message

```
feat(web): components-3 — extract 25 inline <svg> across 4 components (#1321)

## Summary

Continues #1316. Migrates 4 top-level components (25 svg occurrences) to
\`ui/icons/\` wrappers and shrinks the \`svg-inline\` baseline from **84
→ 80**.

## Files migrated (all live importers verified)

| File | svgs | wrappers |
|---|---|---|
| \`LoginForm.tsx\` | 8 | GoogleColorIcon, PhoneCallIcon,
EmailEnvelopeIcon, AlertSolidIcon ×2, ChevronLeftIcon ×2,
ChevronDownIcon |
| \`ModelSelector.tsx\` | 7 | SparklesIcon (full+small), ImageFrameIcon,
RectangleVideoIcon, ChatBubbleQuestionIcon, ChevronDownLargeIcon,
CheckSolidIcon |
| \`ImagePreview.tsx\` | 5 | DownloadIcon, CloseIcon, ChevronLeftIcon,
ChevronRightPathIcon, PhotoIcon |
| \`ClawPageHeader.tsx\` | 5 | ChevronRightPathIcon, ChevronDownIcon,
LinkIcon, FolderIcon, SettingsGearIcon |

## New icon wrappers (13)

**Brand / colored**:
- GoogleColorIcon (4-color "G" logo for sign-in)
- AlertSolidIcon (Heroicons mini fill viewBox 20)

**Generic primitives** (will be reused widely):
- PhoneCallIcon, EmailEnvelopeIcon, DownloadIcon, LinkIcon
- SparklesIcon (4-pointed star + smaller companion star)
- SparklesSmallIcon (single-star variant — distinct from SparklesIcon
which has 2 stars; ModelSelector uses both)
- ImageFrameIcon (Heroicons "photo" with frame border + sun + 2
mountains — distinct from PhotoIcon which is Feather-style with no
enclosing border)
- RectangleVideoIcon (Heroicons video-camera outline)
- ChatBubbleQuestionIcon (Heroicons chat-bubble with internal lines +
dots — distinct from ChatBubbleIcon and ChatHelpIcon)
- ChevronDownLargeIcon (\`M19.5 8.25l-7.5 7.5-7.5-7.5\` stroke=1.5 —
different sweep from ChevronDownIcon and ChevronDownThinIcon)
- SettingsGearIcon (Feather-style gear stroke=2 — distinct from
SettingsCogIcon Heroicons-style stroke=1.5)

## Reused (no new wrapper)

ChevronLeftIcon, ChevronDownIcon, ChevronRightPathIcon, CheckSolidIcon,
FolderIcon, CloseIcon, PhotoIcon

## Visual fidelity: 0 risk

All wrappers preserve \`path\` / \`viewBox\` / \`fill\` / \`stroke\` /
\`strokeWidth\` / \`strokeLinecap\` / \`strokeLinejoin\` byte-for-byte.

## Test plan

- [x] \`pnpm lint\` clean
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint:ci\` clean (\`✓ All web/ ci-lint checks passed\`)
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` shows 84 → 80 (✓
shrink, exactly 4 files)
- [x] Sibling shrink scripts (react/forbid-dom-props 45→45, no-raw-fetch
10→10) unchanged
- [x] All 4 migrated files: \`grep -c '<svg'\` returns 0
- [ ] Visual regression on staging: login form (Google/phone/email +
error tooltips + back chevron + dropdown), model selector (sparkles
category icons + dropdown chevron + selected check), image preview
(download/close/prev/next/error fallback), claw page header (chevron
tabs + link/folder/settings buttons) — each pixel-identical to main

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Continues #1316. Migrates 4 top-level components (25 svg occurrences) to \`ui/icons/\` wrappers and shrinks the \`svg-inline\` baseline from **84 → 80**.

## Files migrated (all live importers verified)

| File | svgs | wrappers |
|---|---|---|
| \`LoginForm.tsx\` | 8 | GoogleColorIcon, PhoneCallIcon, EmailEnvelopeIcon, AlertSolidIcon ×2, ChevronLeftIcon ×2, ChevronDownIcon |
| \`ModelSelector.tsx\` | 7 | SparklesIcon (full+small), ImageFrameIcon, RectangleVideoIcon, ChatBubbleQuestionIcon, ChevronDownLargeIcon, CheckSolidIcon |
| \`ImagePreview.tsx\` | 5 | DownloadIcon, CloseIcon, ChevronLeftIcon, ChevronRightPathIcon, PhotoIcon |
| \`ClawPageHeader.tsx\` | 5 | ChevronRightPathIcon, ChevronDownIcon, LinkIcon, FolderIcon, SettingsGearIcon |

## New icon wrappers (13)

**Brand / colored**:
- GoogleColorIcon (4-color "G" logo for sign-in)
- AlertSolidIcon (Heroicons mini fill viewBox 20)

**Generic primitives** (will be reused widely):
- PhoneCallIcon, EmailEnvelopeIcon, DownloadIcon, LinkIcon
- SparklesIcon (4-pointed star + smaller companion star)
- SparklesSmallIcon (single-star variant — distinct from SparklesIcon which has 2 stars; ModelSelector uses both)
- ImageFrameIcon (Heroicons "photo" with frame border + sun + 2 mountains — distinct from PhotoIcon which is Feather-style with no enclosing border)
- RectangleVideoIcon (Heroicons video-camera outline)
- ChatBubbleQuestionIcon (Heroicons chat-bubble with internal lines + dots — distinct from ChatBubbleIcon and ChatHelpIcon)
- ChevronDownLargeIcon (\`M19.5 8.25l-7.5 7.5-7.5-7.5\` stroke=1.5 — different sweep from ChevronDownIcon and ChevronDownThinIcon)
- SettingsGearIcon (Feather-style gear stroke=2 — distinct from SettingsCogIcon Heroicons-style stroke=1.5)

## Reused (no new wrapper)

ChevronLeftIcon, ChevronDownIcon, ChevronRightPathIcon, CheckSolidIcon, FolderIcon, CloseIcon, PhotoIcon

## Visual fidelity: 0 risk

All wrappers preserve \`path\` / \`viewBox\` / \`fill\` / \`stroke\` / \`strokeWidth\` / \`strokeLinecap\` / \`strokeLinejoin\` byte-for-byte.

## Test plan

- [x] \`pnpm lint\` clean
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint:ci\` clean (\`✓ All web/ ci-lint checks passed\`)
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` shows 84 → 80 (✓ shrink, exactly 4 files)
- [x] Sibling shrink scripts (react/forbid-dom-props 45→45, no-raw-fetch 10→10) unchanged
- [x] All 4 migrated files: \`grep -c '<svg'\` returns 0
- [ ] Visual regression on staging: login form (Google/phone/email + error tooltips + back chevron + dropdown), model selector (sparkles category icons + dropdown chevron + selected check), image preview (download/close/prev/next/error fallback), claw page header (chevron tabs + link/folder/settings buttons) — each pixel-identical to main

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): useFalImageProcess → useMutation (RQ PR 4) (#1320)

- **SHA**: `e8c2edc8b69f61f7ac7d57906af4a85aea8b7721`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T13:11:11Z
- **PR**: #1320

### Commit Message

```
refactor(web): useFalImageProcess → useMutation (RQ PR 4) (#1320)

## Summary

Fourth domain migration of the React Query rollout. Smaller surface than
PR 1-3 — only one caller (\`useCanvasChat\`) and it consumes results via
\`await processImage(...)\`, so preserving that exact return shape lets
\`useMutation\` slot in without touching the caller.

- **\`processFalImage\`** — \`src/lib/api/fal.ts\` (permanent
allowlist). Extracted from the hook; uses the shared
\`buildAuthHeaders\` helper so the duplicated bearer + virtual-key
bookkeeping in the hook is gone.
- **Hook** — \`useMutation\` around \`processFalImage\`; returns \`{
processImage }\` delegating to \`mutateAsync\`. Inherits
\`mutations.retry: 0\` from the global \`createQueryClient\` defaults —
fal.ai is paid per call, so a flaky network must not double-charge.
- **Existing tests preserved** —
\`tests/unit/canvas-hooks/useFalImageProcess.unit.spec.ts\` (9 cases:
auth header variants, error paths, empty-images guard) wrapped with
\`createQueryWrapper\` for the new \`QueryClientProvider\` dependency.
- **ESLint SHRINK-ONLY** — \`useFalImageProcess.ts\` removed (10 → 9
transitional).

Spec:
[\`docs/superpowers/specs/2026-04-24-react-query-migration.md\`](docs/superpowers/specs/2026-04-24-react-query-migration.md).

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm lint:ci\` clean (knip dep-health hard gate)
- [x] \`pnpm test:unit\` full run — 262 files / 4169 tests pass;
existing useFalImageProcess spec all 9 cases pass with the wrapper
- [ ] Local \`pnpm dev\` — open canvas, run upscale / background-remove
/ layer-split on an image; confirm transformation completes and no
double-spend on intentional network blip

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Fourth domain migration of the React Query rollout. Smaller surface than PR 1-3 — only one caller (\`useCanvasChat\`) and it consumes results via \`await processImage(...)\`, so preserving that exact return shape lets \`useMutation\` slot in without touching the caller.

- **\`processFalImage\`** — \`src/lib/api/fal.ts\` (permanent allowlist). Extracted from the hook; uses the shared \`buildAuthHeaders\` helper so the duplicated bearer + virtual-key bookkeeping in the hook is gone.
- **Hook** — \`useMutation\` around \`processFalImage\`; returns \`{ processImage }\` delegating to \`mutateAsync\`. Inherits \`mutations.retry: 0\` from the global \`createQueryClient\` defaults — fal.ai is paid per call, so a flaky network must not double-charge.
- **Existing tests preserved** — \`tests/unit/canvas-hooks/useFalImageProcess.unit.spec.ts\` (9 cases: auth header variants, error paths, empty-images guard) wrapped with \`createQueryWrapper\` for the new \`QueryClientProvider\` dependency.
- **ESLint SHRINK-ONLY** — \`useFalImageProcess.ts\` removed (10 → 9 transitional).

Spec: [\`docs/superpowers/specs/2026-04-24-react-query-migration.md\`](docs/superpowers/specs/2026-04-24-react-query-migration.md).

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm lint:ci\` clean (knip dep-health hard gate)
- [x] \`pnpm test:unit\` full run — 262 files / 4169 tests pass; existing useFalImageProcess spec all 9 cases pass with the wrapper
- [ ] Local \`pnpm dev\` — open canvas, run upscale / background-remove / layer-split on an image; confirm transformation completes and no double-spend on intentional network blip

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): ArtifactPreview polling → useQuery refetchInterval (RQ PR 3) (#1312)

- **SHA**: `d7556e8a441228ddaf9d4f69a6ede420546cb687`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T13:00:41Z
- **PR**: #1312

### Commit Message

```
refactor(web): ArtifactPreview polling → useQuery refetchInterval (RQ PR 3) (#1312)

## Summary

Third domain migration of the React Query rollout. Replaces the manual
\`useEffect+setTimeout\` HEAD polling chain in \`FileAvailabilityGate\`
with a \`useQuery\`-based hook; also routes the download-blob fetch
through the lib/api wrapper so the component is fetch-free.

- **\`useArtifactAvailability\` hook** —
\`src/hooks/queries/artifact/useArtifactAvailability.ts\`. Internally
\`useQuery\` + RQ's retry machinery (5 retries on \`'not-found-yet'\`
error, 1s spacing) preserves the original 6-attempt / ~5s timing.
Exposes \`status: 'checking' | 'ready' | 'failed'\` + \`stop()\` that
calls \`queryClient.cancelQueries\` and flips a userStopped flag
(matches the original Stop button).
- **API helpers added** — \`headArtifact(url, signal)\` and
\`fetchArtifactBlob(url, init?)\` in \`src/lib/api/artifact.ts\`
(permanent allowlist).
- **\`FileAvailabilityGate\` refactored** — drops ~40 lines of
imperative polling (cancelRef, retries counter, manual setTimeout
chain).
- **\`handleDownload\` refactored** — same UX, calls
\`fetchArtifactBlob\` instead of raw \`fetch\`.
- **ESLint SHRINK-ONLY** — \`ArtifactPreview.tsx\` removed (12 → 11
transitional).

Spec:
[\`docs/superpowers/specs/2026-04-24-react-query-migration.md\`](docs/superpowers/specs/2026-04-24-react-query-migration.md).

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm lint:ci\` clean (knip dep-health hard gate)
- [x] New hook spec — 7 cases (200 / opaqueredirect / non-404 error /
network error / poll-then-ready / exhaust budget → failed / stop)
- [x] Existing \`ArtifactPreview\` spec — wrapped in
\`createQueryWrapper\` (FileAvailabilityGate now needs
QueryClientProvider); all 16 cases pass
- [x] \`pnpm test:unit\` full run — 258 files / 4123 tests pass
- [ ] Local \`pnpm dev\` — open an artifact preview just after
generation; confirm polling spinner → renders. Confirm "Stop" button
transitions to failed state with Retry/Open in new tab.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Third domain migration of the React Query rollout. Replaces the manual \`useEffect+setTimeout\` HEAD polling chain in \`FileAvailabilityGate\` with a \`useQuery\`-based hook; also routes the download-blob fetch through the lib/api wrapper so the component is fetch-free.

- **\`useArtifactAvailability\` hook** — \`src/hooks/queries/artifact/useArtifactAvailability.ts\`. Internally \`useQuery\` + RQ's retry machinery (5 retries on \`'not-found-yet'\` error, 1s spacing) preserves the original 6-attempt / ~5s timing. Exposes \`status: 'checking' | 'ready' | 'failed'\` + \`stop()\` that calls \`queryClient.cancelQueries\` and flips a userStopped flag (matches the original Stop button).
- **API helpers added** — \`headArtifact(url, signal)\` and \`fetchArtifactBlob(url, init?)\` in \`src/lib/api/artifact.ts\` (permanent allowlist).
- **\`FileAvailabilityGate\` refactored** — drops ~40 lines of imperative polling (cancelRef, retries counter, manual setTimeout chain).
- **\`handleDownload\` refactored** — same UX, calls \`fetchArtifactBlob\` instead of raw \`fetch\`.
- **ESLint SHRINK-ONLY** — \`ArtifactPreview.tsx\` removed (12 → 11 transitional).

Spec: [\`docs/superpowers/specs/2026-04-24-react-query-migration.md\`](docs/superpowers/specs/2026-04-24-react-query-migration.md).

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm lint:ci\` clean (knip dep-health hard gate)
- [x] New hook spec — 7 cases (200 / opaqueredirect / non-404 error / network error / poll-then-ready / exhaust budget → failed / stop)
- [x] Existing \`ArtifactPreview\` spec — wrapped in \`createQueryWrapper\` (FileAvailabilityGate now needs QueryClientProvider); all 16 cases pass
- [x] \`pnpm test:unit\` full run — 258 files / 4123 tests pass
- [ ] Local \`pnpm dev\` — open an artifact preview just after generation; confirm polling spinner → renders. Confirm "Stop" button transitions to failed state with Retry/Open in new tab.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(web): components-2 — extract 28 inline <svg> across 6 files (UserMenu cluster) (#1316)

- **SHA**: `3b9d239353a04ec37863fc28bf12668bccf0bd11`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T12:58:25Z
- **PR**: #1316

### Commit Message

```
feat(web): components-2 — extract 28 inline <svg> across 6 files (UserMenu cluster) (#1316)

## Summary

Continues #1314. Migrates 6 user-profile / menu / paywall components (28
svg occurrences) to \`ui/icons/\` wrappers and shrinks the
\`svg-inline\` baseline from **91 → 84** (also drops a no-op
false-positive entry).

## Files migrated (all live importers verified)

| File | svgs | notes |
|---|---|---|
| \`UserMenu.tsx\` | 14 | Biggest single file in remaining baseline.
Includes 2 self-contained animated SVGs |
| \`UserCard.tsx\` | 6 | Status badges + tooltip arrow + chevron |
| \`AgentSettingsPopover.tsx\` | 3 | Warning + close + spinner |
| \`GuideTourModal.tsx\` | 3 | Chevron prev/next + 2 close |
| \`PaywallContent.tsx\` | 1 | Feature check |
| \`GiftPaywallFab.tsx\` | 1 | Animated FAB gift (+ removed local 1-line
wrapper) |

## Baseline cleanup (no code change)

- **\`MarkdownContent.tsx\`** removed from svg-inline ignores: its only
\`<svg>\` is inside a JS template string for HTML injection (not JSX),
so the ESLint rule's \`JSXOpeningElement\` selector cannot match it. The
baseline entry was a no-op false-positive — same pattern as
\`renderMarkdownToHtml.ts\` already excluded in #1307.

## New icon wrappers (22)

**Generic primitives** (will be reused widely):
HelpInfoIcon, ChevronRightPathIcon (path-based variant of polyline
ChevronRightIcon — distinct visual, kept byte-exact), ChevronLeftIcon,
ChevronUpIcon, SettingsCogIcon, ClipboardIcon, ArchiveBoxIcon,
RectangleStackIcon, GlobeIcon, ChatHelpIcon, PhoneIcon (1024 viewBox),
ArrowRightOnRectangleIcon (sign-out), DiscordLogoIcon, CrownIcon,
ClockIcon, ZzzIcon, TooltipArrowUpIcon (inverse of
TooltipArrowDownIcon), SmallSpinnerIcon (single-arc, distinct from
SpinnerIcon two-tone), CheckThinIcon (14x14, stroke=1.5)

**Self-contained animated SVGs** (linearGradient defs + scoped CSS
keyframes via inline \`<style>\`):
- \`GiftMenuAnimatedIcon\` (24x24 lid pop, 3s loop)
- \`AnimatedGiftDropIcon\` (84x94 drop → lid open → star burst +
confetti, 5s loop) — eslint-disable on two \`<g style={{ transformOrigin
}}>\` nodes (UserMenu was in react/forbid-dom-props ignores; the wrapper
isn't, and the inline transform-origin is preserved byte-exact)
- \`AnimatedGiftFabIcon\` (100x100 FAB; relies on global gift-paywall
stylesheet for the \`.gift-*\` animation classes — wrapper hardcodes
\`gift-icon overflow-visible\` className since animation depends on it)

\`CrownIcon\`/\`ClockIcon\`/\`ZzzIcon\` use \`{...rest}\` prop spread to
forward \`data-testid\` (used by UserCard).

## Reused (no new wrapper needed)

- BookOpenIcon (PR #1307 — exact path match)
- CloseIcon
- WarningTriangleIcon

## Side-effect cleanup

\`GiftPaywallFab.tsx\` removed local \`AnimatedGiftIcon\` (1-line
passthrough over \`AnimatedGiftFabIcon\` — redundant after the
migration).

## Visual fidelity: 0 risk

All wrappers preserve \`path\` / \`viewBox\` / \`fill\` / \`stroke\` /
\`strokeWidth\` / \`strokeLinecap\` / \`strokeLinejoin\` byte-for-byte.
Animated wrappers preserve all keyframes, gradients, and
transform-origins.

## Test plan

- [x] \`pnpm lint\` clean
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint:ci\` clean (\`✓ All web/ ci-lint checks passed\` — no
knip unused-export issues)
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` shows 91 → 84 (✓
shrink — 6 migrated + 1 false-positive)
- [x] Sibling shrink scripts (react/forbid-dom-props 45→45, no-raw-fetch
11→11) unchanged
- [x] All 6 migrated files: \`grep -c '<svg'\` returns 0
- [x] Related unit tests pass (UserMenu / UserCard /
AgentSettingsPopover / GuideTourModal / PaywallContent — 154 tests)
- [ ] Visual regression on staging: user menu (full open with all 14
icons, redeem-modal animated drop), user card (avatar bar status badges
+ tooltip + chevron), agent settings popover, guide tour modal nav,
paywall content checkmarks, gift paywall FAB animation — each
pixel-identical to main

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Continues #1314. Migrates 6 user-profile / menu / paywall components (28 svg occurrences) to \`ui/icons/\` wrappers and shrinks the \`svg-inline\` baseline from **91 → 84** (also drops a no-op false-positive entry).

## Files migrated (all live importers verified)

| File | svgs | notes |
|---|---|---|
| \`UserMenu.tsx\` | 14 | Biggest single file in remaining baseline. Includes 2 self-contained animated SVGs |
| \`UserCard.tsx\` | 6 | Status badges + tooltip arrow + chevron |
| \`AgentSettingsPopover.tsx\` | 3 | Warning + close + spinner |
| \`GuideTourModal.tsx\` | 3 | Chevron prev/next + 2 close |
| \`PaywallContent.tsx\` | 1 | Feature check |
| \`GiftPaywallFab.tsx\` | 1 | Animated FAB gift (+ removed local 1-line wrapper) |

## Baseline cleanup (no code change)

- **\`MarkdownContent.tsx\`** removed from svg-inline ignores: its only \`<svg>\` is inside a JS template string for HTML injection (not JSX), so the ESLint rule's \`JSXOpeningElement\` selector cannot match it. The baseline entry was a no-op false-positive — same pattern as \`renderMarkdownToHtml.ts\` already excluded in #1307.

## New icon wrappers (22)

**Generic primitives** (will be reused widely):
HelpInfoIcon, ChevronRightPathIcon (path-based variant of polyline ChevronRightIcon — distinct visual, kept byte-exact), ChevronLeftIcon, ChevronUpIcon, SettingsCogIcon, ClipboardIcon, ArchiveBoxIcon, RectangleStackIcon, GlobeIcon, ChatHelpIcon, PhoneIcon (1024 viewBox), ArrowRightOnRectangleIcon (sign-out), DiscordLogoIcon, CrownIcon, ClockIcon, ZzzIcon, TooltipArrowUpIcon (inverse of TooltipArrowDownIcon), SmallSpinnerIcon (single-arc, distinct from SpinnerIcon two-tone), CheckThinIcon (14x14, stroke=1.5)

**Self-contained animated SVGs** (linearGradient defs + scoped CSS keyframes via inline \`<style>\`):
- \`GiftMenuAnimatedIcon\` (24x24 lid pop, 3s loop)
- \`AnimatedGiftDropIcon\` (84x94 drop → lid open → star burst + confetti, 5s loop) — eslint-disable on two \`<g style={{ transformOrigin }}>\` nodes (UserMenu was in react/forbid-dom-props ignores; the wrapper isn't, and the inline transform-origin is preserved byte-exact)
- \`AnimatedGiftFabIcon\` (100x100 FAB; relies on global gift-paywall stylesheet for the \`.gift-*\` animation classes — wrapper hardcodes \`gift-icon overflow-visible\` className since animation depends on it)

\`CrownIcon\`/\`ClockIcon\`/\`ZzzIcon\` use \`{...rest}\` prop spread to forward \`data-testid\` (used by UserCard).

## Reused (no new wrapper needed)

- BookOpenIcon (PR #1307 — exact path match)
- CloseIcon
- WarningTriangleIcon

## Side-effect cleanup

\`GiftPaywallFab.tsx\` removed local \`AnimatedGiftIcon\` (1-line passthrough over \`AnimatedGiftFabIcon\` — redundant after the migration).

## Visual fidelity: 0 risk

All wrappers preserve \`path\` / \`viewBox\` / \`fill\` / \`stroke\` / \`strokeWidth\` / \`strokeLinecap\` / \`strokeLinejoin\` byte-for-byte. Animated wrappers preserve all keyframes, gradients, and transform-origins.

## Test plan

- [x] \`pnpm lint\` clean
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint:ci\` clean (\`✓ All web/ ci-lint checks passed\` — no knip unused-export issues)
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` shows 91 → 84 (✓ shrink — 6 migrated + 1 false-positive)
- [x] Sibling shrink scripts (react/forbid-dom-props 45→45, no-raw-fetch 11→11) unchanged
- [x] All 6 migrated files: \`grep -c '<svg'\` returns 0
- [x] Related unit tests pass (UserMenu / UserCard / AgentSettingsPopover / GuideTourModal / PaywallContent — 154 tests)
- [ ] Visual regression on staging: user menu (full open with all 14 icons, redeem-modal animated drop), user card (avatar bar status badges + tooltip + chevron), agent settings popover, guide tour modal nav, paywall content checkmarks, gift paywall FAB animation — each pixel-identical to main

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(chat-replay): use APP_FRONTEND_URL for share links (#1319)

- **SHA**: `e7dbc1491aa6d9ea815742074250207df3e4fee7`
- **作者**: kaka-srp
- **日期**: 2026-04-24T12:58:13Z
- **PR**: #1319

### Commit Message

```
fix(chat-replay): use APP_FRONTEND_URL for share links (#1319)

## Summary

- Share URLs are user-facing frontend links (`/share/*` route lives in
the Next.js app), so `_build_share_url()` now resolves against
`APP_FRONTEND_URL` instead of `APP_PUBLIC_URL`.
- Falls back to relative path `/share/{id}` when `APP_FRONTEND_URL` is
unset; the frontend's `absoluteUrl()` helper resolves that against
`window.location.origin`.

## Why

In staging the two settings point at different hosts:

| Key | Staging value | Purpose |
|---|---|---|
| `APP_PUBLIC_URL` | `https://claw-interface.ecap.yesy.live` |
**Backend** host — OAuth/webhook callbacks (Google, Stripe return, bot
env) |
| `APP_FRONTEND_URL` | `https://ecap.gensmo.nosay.live` | **Frontend**
host — what users open in the browser |

The previous code used `APP_PUBLIC_URL`, so shared replay links pointed
at the backend domain where `/share/*` doesn't exist → 404. This PR
fixes only the share-link call site; other callers of `APP_PUBLIC_URL`
(OAuth callbacks, Stripe portal, bot env injection) are correct as-is
and unchanged.

DB stores only `share_id`, not full URLs — no data migration needed.
After deploy, all newly created links will use the frontend host.

## Test plan

- [x] Three new unit tests cover `APP_FRONTEND_URL` precedence,
trailing-slash stripping, and relative-path fallback
- [x] `pytest tests/unit/test_chat_replay_create.py` — 17/17 passing
locally
- [x] ruff, pyright, import-linter, deptry, file-length, complexity,
collection-constants, repo-sync — all clean
- [ ] After merge: smoke-test on staging by creating a new share and
opening the URL in incognito
```

### PR Description

## Summary

- Share URLs are user-facing frontend links (`/share/*` route lives in the Next.js app), so `_build_share_url()` now resolves against `APP_FRONTEND_URL` instead of `APP_PUBLIC_URL`.
- Falls back to relative path `/share/{id}` when `APP_FRONTEND_URL` is unset; the frontend's `absoluteUrl()` helper resolves that against `window.location.origin`.

## Why

In staging the two settings point at different hosts:

| Key | Staging value | Purpose |
|---|---|---|
| `APP_PUBLIC_URL` | `https://claw-interface.ecap.yesy.live` | **Backend** host — OAuth/webhook callbacks (Google, Stripe return, bot env) |
| `APP_FRONTEND_URL` | `https://ecap.gensmo.nosay.live` | **Frontend** host — what users open in the browser |

The previous code used `APP_PUBLIC_URL`, so shared replay links pointed at the backend domain where `/share/*` doesn't exist → 404. This PR fixes only the share-link call site; other callers of `APP_PUBLIC_URL` (OAuth callbacks, Stripe portal, bot env injection) are correct as-is and unchanged.

DB stores only `share_id`, not full URLs — no data migration needed. After deploy, all newly created links will use the frontend host.

## Test plan

- [x] Three new unit tests cover `APP_FRONTEND_URL` precedence, trailing-slash stripping, and relative-path fallback
- [x] `pytest tests/unit/test_chat_replay_create.py` — 17/17 passing locally
- [x] ruff, pyright, import-linter, deptry, file-length, complexity, collection-constants, repo-sync — all clean
- [ ] After merge: smoke-test on staging by creating a new share and opening the URL in incognito

---

## feat(web): unify model labels + surface default (ECA-553) (#1317)

- **SHA**: `f1a9ce03537ef01145103cf011c967410890c46f`
- **作者**: kaka-srp
- **日期**: 2026-04-24T12:56:26Z
- **PR**: #1317

### Commit Message

```
feat(web): unify model labels + surface default (ECA-553) (#1317)

## Summary

Fixes two UX problems in the agent settings model dropdown (top-right of
every agent page):

1. **Model names were inconsistent** — `MODEL_LABELS` was duplicated in
two files and had drifted (e.g. `GPT-5.4`, `GLM-5` with hyphens while
`Claude Opus 4.6` used spaces). Worse, newly-added backend models
(`claude-opus-4-7`, `gemma-4-31B-it`) weren't in the dict at all, so the
raw kebab-case id leaked to the UI.
2. **The "Use default" option was opaque** — rendered `Use default
(global model)` without telling the user what the global default
actually resolved to.

## What changed

- **Algorithmic label normalization**
([`web/src/config/models.ts`](../tree/feat/eca-553-default-model-visible/web/src/config/models.ts)):
`backendModelLabel(id)` now computes the display name from the kebab id
(strip `openai/`, strip `-preview`, merge adjacent pure-digit tokens as
`X.Y`, per-token casing via acronym allowlist + title-case default) — so
new backend models format correctly with zero frontend changes. Kept an
empty `BACKEND_MODEL_LABEL_OVERRIDES` as a documented escape hatch for
brand names the algorithm can't guess (e.g. `GPT-4o`).
- **Collapsed duplicated `MODEL_LABELS`**:
`agent-settings/AgentModelSection.tsx` and
`claw-settings/ModelSection.tsx` both now import the shared helper.
- **Surfaced the concrete default** in the popover:
`AgentSettingsPopover` pulls `primary_model` via `useClawSettings` and
passes it down; the empty option now renders `Use default (Claude Sonnet
4.6)` (or whatever the global model is).
- **i18n**: added `agentSettings.useDefaultNamed` to the 7 locales that
already had `agentSettings` (`en/zh/ar/es/ja/ko/pt`); `de/fr/it` fall
back to English through `getNestedValue`.
- **Tests**: new `backendModelLabels.unit.spec.ts` with exact-output
table for 10 real backend ids + naming-rule regex guard (rejects
hyphens, asserts `-preview` ↔ ` Preview` consistency); new
`AgentModelSection.unit.spec.tsx` for both default-label paths; extended
`AgentSettingsPopover.unit.spec.tsx` to mock `useClawSettings` (popover
now calls it).

## Before → After (for visible dropdown rows)

| backend id | before | after |
|---|---|---|
| `openai/claude-opus-4-7` | `claude-opus-4-7` | `Claude Opus 4.7` |
| `gemma-4-31B-it` | `gemma-4-31B-it` | `Gemma 4 31B IT` |
| `openai/gpt-5.4` | `GPT-5.4` | `GPT 5.4` |
| `openai/glm-5` | `GLM-5` | `GLM 5` |
| `""` (default) | `Use default (global model)` | `Use default (Claude
Sonnet 4.6)` |

## Test plan

- [x] `cd web && pnpm lint` — clean
- [x] `cd web && pnpm exec tsc --noEmit` — clean
- [x] `cd web && pnpm test
tests/unit/config/backendModelLabels.unit.spec.ts
tests/unit/components/AgentModelSection.unit.spec.tsx
tests/unit/components/AgentSettingsPopover.unit.spec.tsx` — 34 tests
pass
- [ ] Manual: open an agent chat, click settings (top-right), verify the
default option reads `Use default (<concrete model name>)` and all other
options use consistent casing/spacing, no hyphens.
- [ ] Manual: open `/claw-settings`, confirm the Primary Model dropdown
uses the same labels.

Closes ECA-553.
```

### PR Description

## Summary

Fixes two UX problems in the agent settings model dropdown (top-right of every agent page):

1. **Model names were inconsistent** — `MODEL_LABELS` was duplicated in two files and had drifted (e.g. `GPT-5.4`, `GLM-5` with hyphens while `Claude Opus 4.6` used spaces). Worse, newly-added backend models (`claude-opus-4-7`, `gemma-4-31B-it`) weren't in the dict at all, so the raw kebab-case id leaked to the UI.
2. **The "Use default" option was opaque** — rendered `Use default (global model)` without telling the user what the global default actually resolved to.

## What changed

- **Algorithmic label normalization** ([`web/src/config/models.ts`](../tree/feat/eca-553-default-model-visible/web/src/config/models.ts)): `backendModelLabel(id)` now computes the display name from the kebab id (strip `openai/`, strip `-preview`, merge adjacent pure-digit tokens as `X.Y`, per-token casing via acronym allowlist + title-case default) — so new backend models format correctly with zero frontend changes. Kept an empty `BACKEND_MODEL_LABEL_OVERRIDES` as a documented escape hatch for brand names the algorithm can't guess (e.g. `GPT-4o`).
- **Collapsed duplicated `MODEL_LABELS`**: `agent-settings/AgentModelSection.tsx` and `claw-settings/ModelSection.tsx` both now import the shared helper.
- **Surfaced the concrete default** in the popover: `AgentSettingsPopover` pulls `primary_model` via `useClawSettings` and passes it down; the empty option now renders `Use default (Claude Sonnet 4.6)` (or whatever the global model is).
- **i18n**: added `agentSettings.useDefaultNamed` to the 7 locales that already had `agentSettings` (`en/zh/ar/es/ja/ko/pt`); `de/fr/it` fall back to English through `getNestedValue`.
- **Tests**: new `backendModelLabels.unit.spec.ts` with exact-output table for 10 real backend ids + naming-rule regex guard (rejects hyphens, asserts `-preview` ↔ ` Preview` consistency); new `AgentModelSection.unit.spec.tsx` for both default-label paths; extended `AgentSettingsPopover.unit.spec.tsx` to mock `useClawSettings` (popover now calls it).

## Before → After (for visible dropdown rows)

| backend id | before | after |
|---|---|---|
| `openai/claude-opus-4-7` | `claude-opus-4-7` | `Claude Opus 4.7` |
| `gemma-4-31B-it` | `gemma-4-31B-it` | `Gemma 4 31B IT` |
| `openai/gpt-5.4` | `GPT-5.4` | `GPT 5.4` |
| `openai/glm-5` | `GLM-5` | `GLM 5` |
| `""` (default) | `Use default (global model)` | `Use default (Claude Sonnet 4.6)` |

## Test plan

- [x] `cd web && pnpm lint` — clean
- [x] `cd web && pnpm exec tsc --noEmit` — clean
- [x] `cd web && pnpm test tests/unit/config/backendModelLabels.unit.spec.ts tests/unit/components/AgentModelSection.unit.spec.tsx tests/unit/components/AgentSettingsPopover.unit.spec.tsx` — 34 tests pass
- [ ] Manual: open an agent chat, click settings (top-right), verify the default option reads `Use default (<concrete model name>)` and all other options use consistent casing/spacing, no hyphens.
- [ ] Manual: open `/claw-settings`, confirm the Primary Model dropdown uses the same labels.

Closes ECA-553.

---

## refactor(billing): remove legacy monthly product and STARTER_PLAN_CREDITS (#1310)

- **SHA**: `d5a98d29a3580d4f343c1224f06def6b99d70a06`
- **作者**: bryce-srp
- **日期**: 2026-04-24T12:12:30Z
- **PR**: #1310

### Commit Message

```
refactor(billing): remove legacy monthly product and STARTER_PLAN_CREDITS (#1310)

## Summary

- Remove the legacy `STRIPE_PRODUCT_ID_MONTHLY` branch from
`_grant_subscription` — all 5 users on this product have had their
subscriptions set to `cancel_at_period_end`
- Replace the unknown-product fallback with `UnknownStripeProductError`
(previously fell back to 24,000 credits silently)
- Delete `STARTER_PLAN_CREDITS = 24000` constant — all paths now use
`PLAN_CREDITS[plan]` (4,800 / 20,000 / 40,000)
- Remove legacy product IDs (`MONTHLY`, `DAYLY`, `ONCE`) from
`VALID_PRODUCT_IDS` and subscription whitelist
- Plan resolution now uses `plan_from_stripe_product_id()` as fallback
when `order.plan` is missing

## Context

PR #1256 fixed the immediate bug (legacy branch giving 24,000 instead of
4,800). This PR completes the cleanup by removing the legacy code
entirely, now that no active subscriptions use the old product.

## Test plan
- [ ] CI passes (ruff, pyright, pytest)
- [ ] Verify no pending `product_type: "credits"` or legacy monthly
orders in production before deploy
- [ ] Monitor `UnknownStripeProductError` in Sentry after deploy —
should be zero

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

- Remove the legacy `STRIPE_PRODUCT_ID_MONTHLY` branch from `_grant_subscription` — all 5 users on this product have had their subscriptions set to `cancel_at_period_end`
- Replace the unknown-product fallback with `UnknownStripeProductError` (previously fell back to 24,000 credits silently)
- Delete `STARTER_PLAN_CREDITS = 24000` constant — all paths now use `PLAN_CREDITS[plan]` (4,800 / 20,000 / 40,000)
- Remove legacy product IDs (`MONTHLY`, `DAYLY`, `ONCE`) from `VALID_PRODUCT_IDS` and subscription whitelist
- Plan resolution now uses `plan_from_stripe_product_id()` as fallback when `order.plan` is missing

## Context

PR #1256 fixed the immediate bug (legacy branch giving 24,000 instead of 4,800). This PR completes the cleanup by removing the legacy code entirely, now that no active subscriptions use the old product.

## Test plan
- [ ] CI passes (ruff, pyright, pytest)
- [ ] Verify no pending `product_type: "credits"` or legacy monthly orders in production before deploy
- [ ] Monitor `UnknownStripeProductError` in Sentry after deploy — should be zero

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(web): components-1 — extract 16 inline <svg> across 12 small components (#1314)

- **SHA**: `95d01c620d4ee0c5738ea392ab13c94689002337`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T12:01:59Z
- **PR**: #1314

### Commit Message

```
feat(web): components-1 — extract 16 inline <svg> across 12 small components (#1314)

## Summary

Continues #1313. Migrates 12 small/medium top-level \`components/\`
files (16 svg occurrences) to \`ui/icons/\` wrappers and shrinks the
\`svg-inline\` baseline from **103 → 91**.

## Files migrated (all live importers verified)

| File | svgs | wrappers used |
|---|---|---|
| \`ThemeToggle.tsx\` | 2 | SunIcon, MoonIcon (replaces local function
decls) |
| \`MobileAppModal.tsx\` | 2 | CloseIcon, AppleLogoIcon |
| \`AppLayout.tsx\` | 1 conditional | CloseIcon / MenuBarsIcon |
| \`LoginModal.tsx\` | 1 | CloseLineThickIcon |
| \`VersionUpgradeWidget.tsx\` | 1 | CloseTinyIcon |
| \`UpgradeNotificationBanner.tsx\` | 1 | CloseLineIcon |
| \`GiftPaywallModal.tsx\` | 1 | CloseIcon |
| \`CompensationPopup.tsx\` | 1 | GiftBoxIcon |
| \`ProgressiveImage.tsx\` | 1 | PhotoIcon |
| \`SelectField.tsx\` | 2 | ChevronDownThinIcon, CheckSolidIcon |
| \`SizeSelector.tsx\` | 1 | ChevronDownThinIcon |
| \`SeedanceLaunchModal.tsx\` | 2 | PlayIcon, CloseMicroIcon |

## NOT migrated (pre-existing dead code)

- \`components/UserAvatar.tsx\` — no importer in repo
(OpenClawUserMessage has a local UserAvatar function of the same name;
the standalone file is orphan). Stays in baseline with a comment.
**Follow-up:** cleanup PR should delete the file (joins the ChatWelcome
/ ToolProgressFloat dead-code follow-up list).

## New icon wrappers (13)

**Theme**: SunIcon, MoonIcon

**Brand**: AppleLogoIcon (App Store apple, 814x1000 viewBox)

**Generic primitives** (will be reused widely): MenuBarsIcon
(hamburger), GiftBoxIcon, PhotoIcon, PlayIcon

**Close-variant family** (each preserves its source byte-for-byte
instead of forcing a one-size-fits-all \`CloseIcon\` with props):
- \`CloseLineThickIcon\` — LoginModal (2x \`<line>\`, stroke=2.5)
- \`CloseLineIcon\` — UpgradeNotificationBanner (2x \`<line>\`,
stroke=2)
- \`CloseTinyIcon\` — VersionUpgradeWidget (16x16 path, stroke=1.5)
- \`CloseMicroIcon\` — SeedanceLaunchModal (12x12 path, stroke=2)

**Chevron / check variants** (same family but distinct stroke / fill /
viewBox):
- \`ChevronDownThinIcon\` — SelectField + SizeSelector (same path as
ChevronDownIcon but stroke=1.5 vs 2)
- \`CheckSolidIcon\` — SelectField selected indicator (Heroicons mini
20x20 fill, distinct from outline CheckIcon)

## Reused (no new wrapper needed)

CloseIcon

## Side-effect cleanup

\`ThemeToggle.tsx\` had local \`SunIcon\`/\`MoonIcon\` function
declarations at the bottom of the file — they're removed in favor of the
\`ui/icons\` imports.

## Visual fidelity: 0 risk

All wrappers preserve \`path\` / \`viewBox\` / \`fill\` / \`stroke\` /
\`strokeWidth\` / \`strokeLinecap\` / \`strokeLinejoin\` byte-for-byte
from the original code.

## Test plan

- [x] \`pnpm lint\` clean
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint:ci\` clean (\`✓ All web/ ci-lint checks passed\` — no
knip unused-export issues; live-importer pre-check caught UserAvatar
dead code, learning from #1308)
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` shows 103 → 91
(✓ shrink, exactly 12 files removed)
- [x] Sibling shrink scripts (react/forbid-dom-props 45→45, no-raw-fetch
11→11) unchanged
- [x] All 12 migrated files: \`grep -c '<svg'\` returns 0
- [ ] Visual regression on staging: theme toggle, mobile app modal, app
layout mobile menu, login modal close, version upgrade widget close,
upgrade notification close, gift paywall modal close, compensation
popup, image placeholder, select fields + size selector dropdowns,
seedance launch modal — each pixel-identical to main

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Continues #1313. Migrates 12 small/medium top-level \`components/\` files (16 svg occurrences) to \`ui/icons/\` wrappers and shrinks the \`svg-inline\` baseline from **103 → 91**.

## Files migrated (all live importers verified)

| File | svgs | wrappers used |
|---|---|---|
| \`ThemeToggle.tsx\` | 2 | SunIcon, MoonIcon (replaces local function decls) |
| \`MobileAppModal.tsx\` | 2 | CloseIcon, AppleLogoIcon |
| \`AppLayout.tsx\` | 1 conditional | CloseIcon / MenuBarsIcon |
| \`LoginModal.tsx\` | 1 | CloseLineThickIcon |
| \`VersionUpgradeWidget.tsx\` | 1 | CloseTinyIcon |
| \`UpgradeNotificationBanner.tsx\` | 1 | CloseLineIcon |
| \`GiftPaywallModal.tsx\` | 1 | CloseIcon |
| \`CompensationPopup.tsx\` | 1 | GiftBoxIcon |
| \`ProgressiveImage.tsx\` | 1 | PhotoIcon |
| \`SelectField.tsx\` | 2 | ChevronDownThinIcon, CheckSolidIcon |
| \`SizeSelector.tsx\` | 1 | ChevronDownThinIcon |
| \`SeedanceLaunchModal.tsx\` | 2 | PlayIcon, CloseMicroIcon |

## NOT migrated (pre-existing dead code)

- \`components/UserAvatar.tsx\` — no importer in repo (OpenClawUserMessage has a local UserAvatar function of the same name; the standalone file is orphan). Stays in baseline with a comment. **Follow-up:** cleanup PR should delete the file (joins the ChatWelcome / ToolProgressFloat dead-code follow-up list).

## New icon wrappers (13)

**Theme**: SunIcon, MoonIcon

**Brand**: AppleLogoIcon (App Store apple, 814x1000 viewBox)

**Generic primitives** (will be reused widely): MenuBarsIcon (hamburger), GiftBoxIcon, PhotoIcon, PlayIcon

**Close-variant family** (each preserves its source byte-for-byte instead of forcing a one-size-fits-all \`CloseIcon\` with props):
- \`CloseLineThickIcon\` — LoginModal (2x \`<line>\`, stroke=2.5)
- \`CloseLineIcon\` — UpgradeNotificationBanner (2x \`<line>\`, stroke=2)
- \`CloseTinyIcon\` — VersionUpgradeWidget (16x16 path, stroke=1.5)
- \`CloseMicroIcon\` — SeedanceLaunchModal (12x12 path, stroke=2)

**Chevron / check variants** (same family but distinct stroke / fill / viewBox):
- \`ChevronDownThinIcon\` — SelectField + SizeSelector (same path as ChevronDownIcon but stroke=1.5 vs 2)
- \`CheckSolidIcon\` — SelectField selected indicator (Heroicons mini 20x20 fill, distinct from outline CheckIcon)

## Reused (no new wrapper needed)

CloseIcon

## Side-effect cleanup

\`ThemeToggle.tsx\` had local \`SunIcon\`/\`MoonIcon\` function declarations at the bottom of the file — they're removed in favor of the \`ui/icons\` imports.

## Visual fidelity: 0 risk

All wrappers preserve \`path\` / \`viewBox\` / \`fill\` / \`stroke\` / \`strokeWidth\` / \`strokeLinecap\` / \`strokeLinejoin\` byte-for-byte from the original code.

## Test plan

- [x] \`pnpm lint\` clean
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint:ci\` clean (\`✓ All web/ ci-lint checks passed\` — no knip unused-export issues; live-importer pre-check caught UserAvatar dead code, learning from #1308)
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` shows 103 → 91 (✓ shrink, exactly 12 files removed)
- [x] Sibling shrink scripts (react/forbid-dom-props 45→45, no-raw-fetch 11→11) unchanged
- [x] All 12 migrated files: \`grep -c '<svg'\` returns 0
- [ ] Visual regression on staging: theme toggle, mobile app modal, app layout mobile menu, login modal close, version upgrade widget close, upgrade notification close, gift paywall modal close, compensation popup, image placeholder, select fields + size selector dropdowns, seedance launch modal — each pixel-identical to main

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(web): chat-2 — extract 30 inline <svg> across 9 chat files (#1313)

- **SHA**: `f0cf41ff22969d3cac4755b016377a432bc4d505`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T11:44:45Z
- **PR**: #1313

### Commit Message

```
feat(web): chat-2 — extract 30 inline <svg> across 9 chat files (#1313)

## Summary

Continues #1308. Migrates 9 active `chat/` files (30 svg occurrences) to
`ui/icons/` wrappers and shrinks the `svg-inline` baseline from **112 →
103**.

## Files migrated

| File | svgs |
|---|---|
| `chat/GenClawClient.tsx` | 8 (the largest chat file) |
| `chat/components/ModelDegradationBanner.tsx` | 1 |
| `chat/components/MyUploadsTab.tsx` | 2 |
| `chat/components/OpenClawAssistantMessage.tsx` | 4 |
| `chat/components/OpenClawThread.tsx` | 1 |
| `chat/components/OpenClawUserMessage.tsx` | 4 |
| `chat/components/SubagentChatPanel.tsx` | 4 |
| `chat/components/UploadPopover.tsx` | 2 |
| `chat/components/workspace-shared.tsx` | 4 |

## New icon wrappers (15)

**Generic primitives** (will be widely reused in upcoming PRs):
- \`CheckIcon\` — re-added (was deleted in #1308 because its only caller
there was dead code; now lives again because OpenClawAssistantMessage /
OpenClawUserMessage use it)
- \`CheckSmallIcon\` — 16x16 + stroke=2.5 variant for GenClawClient
subagent status pills
- \`ArrowDownIcon\`
- \`ArrowUpCircleIcon\` (stroke=1.75) + \`ArrowUpCircleThinIcon\`
(stroke=1.5) — same path, two stroke widths used in different contexts.
Keep both wrappers byte-for-byte
- \`HashtagIcon\`, \`FileGenericIcon\`, \`FolderIcon\`

**Warning variants** (3 separate icons because each has distinct
stroke/fill/viewBox):
- \`WarningTriangleIcon\` (outline), \`WarningCircleIcon\` (outline)
- \`WarningTriangleSolidIcon\` (fill, 20x20 — for
ModelDegradationBanner)

**Chat-specific**:
- \`ChevronDownSolidIcon\` (20x20 mini chevron used by
OpenClawAssistantMessage expand/collapse)
- \`ClipboardCopyIcon\` (rect+L path used by both message components)
- \`SpinnerIcon\` (animate-spin friendly two-tone circle)
- \`PaperPlaneIcon\`

## Reused from #1307+#1308 (no new wrapper needed)

CloseIcon, ChevronRightIcon, RefreshIcon, PaperclipIcon, StopSquareIcon,
ReplyArrowIcon

## Side-effect cleanup in workspace-shared.tsx

Local \`FolderIcon\`/\`FileIcon\`/\`ChevronIcon\` wrapper functions
removed — they were thin re-wrappers over inline svg with the same
className shape; the new \`ui/icons\` imports replace them inline at
call sites in \`FileRow\`.

## Visual fidelity: 0 risk

All wrappers preserve \`path\` / \`viewBox\` / \`fill\` / \`stroke\` /
\`strokeWidth\` / \`strokeLinecap\` / \`strokeLinejoin\` byte-for-byte
from the original code.

## Test plan

- [x] \`pnpm lint\` clean
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint:ci\` clean (\`✓ All web/ ci-lint checks passed\` — no
knip unused-export issues; learned from #1308)
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` shows 112 → 103
(✓ shrink)
- [x] Sibling shrink scripts (react/forbid-dom-props 45→45, no-raw-fetch
11→11) unchanged
- [x] All 9 modified files: \`grep -c '<svg'\` returns 0
- [ ] Visual regression on staging: chat thread (assistant + user +
subagent panels), uploads/workspace tabs, upload popover, model
degradation banner — each pixel-identical to main

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Continues #1308. Migrates 9 active `chat/` files (30 svg occurrences) to `ui/icons/` wrappers and shrinks the `svg-inline` baseline from **112 → 103**.

## Files migrated

| File | svgs |
|---|---|
| `chat/GenClawClient.tsx` | 8 (the largest chat file) |
| `chat/components/ModelDegradationBanner.tsx` | 1 |
| `chat/components/MyUploadsTab.tsx` | 2 |
| `chat/components/OpenClawAssistantMessage.tsx` | 4 |
| `chat/components/OpenClawThread.tsx` | 1 |
| `chat/components/OpenClawUserMessage.tsx` | 4 |
| `chat/components/SubagentChatPanel.tsx` | 4 |
| `chat/components/UploadPopover.tsx` | 2 |
| `chat/components/workspace-shared.tsx` | 4 |

## New icon wrappers (15)

**Generic primitives** (will be widely reused in upcoming PRs):
- \`CheckIcon\` — re-added (was deleted in #1308 because its only caller there was dead code; now lives again because OpenClawAssistantMessage / OpenClawUserMessage use it)
- \`CheckSmallIcon\` — 16x16 + stroke=2.5 variant for GenClawClient subagent status pills
- \`ArrowDownIcon\`
- \`ArrowUpCircleIcon\` (stroke=1.75) + \`ArrowUpCircleThinIcon\` (stroke=1.5) — same path, two stroke widths used in different contexts. Keep both wrappers byte-for-byte
- \`HashtagIcon\`, \`FileGenericIcon\`, \`FolderIcon\`

**Warning variants** (3 separate icons because each has distinct stroke/fill/viewBox):
- \`WarningTriangleIcon\` (outline), \`WarningCircleIcon\` (outline)
- \`WarningTriangleSolidIcon\` (fill, 20x20 — for ModelDegradationBanner)

**Chat-specific**:
- \`ChevronDownSolidIcon\` (20x20 mini chevron used by OpenClawAssistantMessage expand/collapse)
- \`ClipboardCopyIcon\` (rect+L path used by both message components)
- \`SpinnerIcon\` (animate-spin friendly two-tone circle)
- \`PaperPlaneIcon\`

## Reused from #1307+#1308 (no new wrapper needed)

CloseIcon, ChevronRightIcon, RefreshIcon, PaperclipIcon, StopSquareIcon, ReplyArrowIcon

## Side-effect cleanup in workspace-shared.tsx

Local \`FolderIcon\`/\`FileIcon\`/\`ChevronIcon\` wrapper functions removed — they were thin re-wrappers over inline svg with the same className shape; the new \`ui/icons\` imports replace them inline at call sites in \`FileRow\`.

## Visual fidelity: 0 risk

All wrappers preserve \`path\` / \`viewBox\` / \`fill\` / \`stroke\` / \`strokeWidth\` / \`strokeLinecap\` / \`strokeLinejoin\` byte-for-byte from the original code.

## Test plan

- [x] \`pnpm lint\` clean
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint:ci\` clean (\`✓ All web/ ci-lint checks passed\` — no knip unused-export issues; learned from #1308)
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` shows 112 → 103 (✓ shrink)
- [x] Sibling shrink scripts (react/forbid-dom-props 45→45, no-raw-fetch 11→11) unchanged
- [x] All 9 modified files: \`grep -c '<svg'\` returns 0
- [ ] Visual regression on staging: chat thread (assistant + user + subagent panels), uploads/workspace tabs, upload popover, model degradation banner — each pixel-identical to main

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): MM auth-blob hook → useQuery (RQ PR 2) (#1305)

- **SHA**: `ac022e75a7e6cb561ae31d2ea6309468d2602b1e`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T11:23:14Z
- **PR**: #1305

### Commit Message

```
refactor(web): MM auth-blob hook → useQuery (RQ PR 2) (#1305)

## Summary

Second domain migration of the React Query rollout. Consolidates 3
nearly-identical local \`useAuthBlobURL\` implementations + an
imperative variant into a single shared \`useAuthBlob\` hook.

- **\`useAuthBlob\` hook** — \`src/hooks/queries/mm/useAuthBlob.ts\`.
\`useQuery\` returns the **Blob** (not ObjectURL); each consumer
\`createObjectURL\`+revokes locally via \`useEffect\`. Why: sharing a
cached Blob across mounts is safe; sharing ObjectURLs is not — one
consumer's revoke leaks a dead URL to siblings.
- **Shared MM helpers** — \`src/lib/mattermost/blob.ts\` (permanent
allowlist): \`isMmHosted(url)\`, \`fetchMmBlob(url, token, signal)\`.
Replaces 3 inline copies of \`MM_SERVER_URL\` + \`isMmHosted\`.
- **4 callers refactored** — \`MyUploadsTab\`, \`UploadsFeed\`,
\`UploadPopover\` (chat), \`MMAttachments\` (Image/Audio/Video
sub-components). Each loses its local \`useAuthBlobURL\` impl +
duplicate trust-check helper.
- **Imperative blob fetches** in click/download handlers
(\`handleClick\`, \`resolveUrl\`, \`handleDownload\`) call
\`fetchMmBlob\` — same imperative shape, but no raw fetch in the
component file.
- **Hook return rename** — \`useConversationAssets\` now returns
\`reload\` (was \`fetch\`); the old name shadowed the global \`fetch\`
and tripped the new lint rule's name-based selector.
- **ESLint SHRINK-ONLY** — 4 files removed (16 → 12 transitional).

Spec:
[\`docs/superpowers/specs/2026-04-24-react-query-migration.md\`](docs/superpowers/specs/2026-04-24-react-query-migration.md).

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm lint:ci\` clean (knip dep-health hard gate)
- [x] New spec — 7 cases (success / 401 / null url disabled / null token
disabled / unmount revokes / url-switch revokes old / bearer header)
- [x] \`pnpm test:unit\` full run — 256 files / 4110 tests pass;
existing MMAttachments tests updated to wrap with \`createQueryWrapper\`
- [ ] Local \`pnpm dev\` — open chat with MM image/audio/video
attachments; preview; download; switch agents to confirm no stale blob
bleed

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Second domain migration of the React Query rollout. Consolidates 3 nearly-identical local \`useAuthBlobURL\` implementations + an imperative variant into a single shared \`useAuthBlob\` hook.

- **\`useAuthBlob\` hook** — \`src/hooks/queries/mm/useAuthBlob.ts\`. \`useQuery\` returns the **Blob** (not ObjectURL); each consumer \`createObjectURL\`+revokes locally via \`useEffect\`. Why: sharing a cached Blob across mounts is safe; sharing ObjectURLs is not — one consumer's revoke leaks a dead URL to siblings.
- **Shared MM helpers** — \`src/lib/mattermost/blob.ts\` (permanent allowlist): \`isMmHosted(url)\`, \`fetchMmBlob(url, token, signal)\`. Replaces 3 inline copies of \`MM_SERVER_URL\` + \`isMmHosted\`.
- **4 callers refactored** — \`MyUploadsTab\`, \`UploadsFeed\`, \`UploadPopover\` (chat), \`MMAttachments\` (Image/Audio/Video sub-components). Each loses its local \`useAuthBlobURL\` impl + duplicate trust-check helper.
- **Imperative blob fetches** in click/download handlers (\`handleClick\`, \`resolveUrl\`, \`handleDownload\`) call \`fetchMmBlob\` — same imperative shape, but no raw fetch in the component file.
- **Hook return rename** — \`useConversationAssets\` now returns \`reload\` (was \`fetch\`); the old name shadowed the global \`fetch\` and tripped the new lint rule's name-based selector.
- **ESLint SHRINK-ONLY** — 4 files removed (16 → 12 transitional).

Spec: [\`docs/superpowers/specs/2026-04-24-react-query-migration.md\`](docs/superpowers/specs/2026-04-24-react-query-migration.md).

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm lint:ci\` clean (knip dep-health hard gate)
- [x] New spec — 7 cases (success / 401 / null url disabled / null token disabled / unmount revokes / url-switch revokes old / bearer header)
- [x] \`pnpm test:unit\` full run — 256 files / 4110 tests pass; existing MMAttachments tests updated to wrap with \`createQueryWrapper\`
- [ ] Local \`pnpm dev\` — open chat with MM image/audio/video attachments; preview; download; switch agents to confirm no stale blob bleed

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(chat-replay): chat-page selection UI + share flow (ECA-548 3/3) (#1302)

- **SHA**: `a3be1850c771d9362da42f2653690b2652401219`
- **作者**: kaka-srp
- **日期**: 2026-04-24T11:27:40Z
- **PR**: #1302

### Commit Message

```
feat(chat-replay): chat-page selection UI + share flow (ECA-548 3/3) (#1302)

## Summary

Third of three stacked PRs
([ECA-548](https://linear.app/srpone/issue/ECA-548/share-selected-chat-messages-as-replay-page)).
Adds the creator-side flow on `/chat`: a selection mode that lets users
pick messages and generate a public replay link via the BFF from #1301 →
backend from #1300.

- **`useChatReplayShare`** hook owns the selection-mode flag, selected
MM post-id set, and create/revoke plumbing. Derives the shareable set
from current `displayMessages` per render (respects the "Select visible"
spec — loaded messages only, never full channel history).
- **`getShareableMessages`** filter drops synthetic tool-group
aggregation rows and `isSystem` messages — keeps parity with the backend
visibility filter from PR 1.
- **`ChatShare*`** components under `components/share/`:
- `ChatShareCheckbox`: reads `ShareSelectionContext` so message
components don't need prop-drilling
- `ChatShareSelectionContext`: tiny provider, default `{enabled: false}`
— zero impact on chat when unmounted
- `ChatShareSelectionBar`: Cancel / Select visible / Clear / count /
Create replay
  - `ChatShareCreatedDialog`: copyable URL + Open + Revoke (idempotent)
- **Integration**: `GenClawClient` mounts the selection provider around
`OpenClawThread`, adds a Share button to the header (hidden when nothing
is shareable yet). `OpenClawUserMessage` / `OpenClawAssistantMessage`
each gain one `<ChatShareCheckbox postId={messageId} />` call.

## Stack

- PR 1 (#1300): backend ← `main`
- PR 2 (#1301): viewer + BFF ← base: `feat/eca-548-a-backend`
- **PR 3 (this one)**: `/chat` selection UI ← base:
`feat/eca-548-b-viewer`

⚠ Merge order: #1300 → #1301 → this.

## Test plan

- [x] `pnpm tsc --noEmit` clean, `pnpm exec eslint` clean
- [x] `getShareableMessages` unit tests (sync filter rules, tool-group
exclusion, order preserved)
- [x] Manual E2E: enter selection mode → select N messages → Create
replay → copy URL → open in incognito → confirm full replay
- [ ] Manual E2E: revoke from created dialog → incognito 404
- [ ] CI green
```

### PR Description

## Summary

Third of three stacked PRs ([ECA-548](https://linear.app/srpone/issue/ECA-548/share-selected-chat-messages-as-replay-page)). Adds the creator-side flow on `/chat`: a selection mode that lets users pick messages and generate a public replay link via the BFF from #1301 → backend from #1300.

- **`useChatReplayShare`** hook owns the selection-mode flag, selected MM post-id set, and create/revoke plumbing. Derives the shareable set from current `displayMessages` per render (respects the "Select visible" spec — loaded messages only, never full channel history).
- **`getShareableMessages`** filter drops synthetic tool-group aggregation rows and `isSystem` messages — keeps parity with the backend visibility filter from PR 1.
- **`ChatShare*`** components under `components/share/`:
  - `ChatShareCheckbox`: reads `ShareSelectionContext` so message components don't need prop-drilling
  - `ChatShareSelectionContext`: tiny provider, default `{enabled: false}` — zero impact on chat when unmounted
  - `ChatShareSelectionBar`: Cancel / Select visible / Clear / count / Create replay
  - `ChatShareCreatedDialog`: copyable URL + Open + Revoke (idempotent)
- **Integration**: `GenClawClient` mounts the selection provider around `OpenClawThread`, adds a Share button to the header (hidden when nothing is shareable yet). `OpenClawUserMessage` / `OpenClawAssistantMessage` each gain one `<ChatShareCheckbox postId={messageId} />` call.

## Stack

- PR 1 (#1300): backend ← `main`
- PR 2 (#1301): viewer + BFF ← base: `feat/eca-548-a-backend`
- **PR 3 (this one)**: `/chat` selection UI ← base: `feat/eca-548-b-viewer`

⚠ Merge order: #1300 → #1301 → this.

## Test plan

- [x] `pnpm tsc --noEmit` clean, `pnpm exec eslint` clean
- [x] `getShareableMessages` unit tests (sync filter rules, tool-group exclusion, order preserved)
- [x] Manual E2E: enter selection mode → select N messages → Create replay → copy URL → open in incognito → confirm full replay
- [ ] Manual E2E: revoke from created dialog → incognito 404
- [ ] CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(web): chat-1 — extract 14 inline <svg> across 4 chat files (#1308)

- **SHA**: `82b29779189b6f2367c1eb6d46fd3688b4015339`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T11:24:04Z
- **PR**: #1308

### Commit Message

```
feat(web): chat-1 — extract 14 inline <svg> across 4 chat files (#1308)

## Summary

Continues #1307. Migrates 4 active `chat/` files (15 actual `<svg>`
occurrences, 14 unique shapes after dedup) to `ui/icons/` wrappers and
shrinks the `svg-inline` baseline from **116 → 112**.

## Files migrated

| File | svgs | new wrappers used |
|---|---|---|
| `QuickActionCards.tsx` | 10 | 10 category icons + ChevronRightIcon |
| `ToolGroup.tsx` | 3 | BoltSolidIcon (reused from #1307),
ChevronDownIcon, PlusIcon |
| `ResourcesPanel.tsx` | 1 | CloseIcon (reused from #1307) |
| `WorkspaceFilesTab.tsx` | 1 | RefreshIcon |

## NOT migrated (pre-existing dead code)

- `ChatWelcome.tsx` — no importer in repo
- `ToolProgressFloat.tsx` — `<ToolProgressFloat />` used in
`GenClawClient.tsx` but the corresponding `import` line above it is
commented out

Both stay in the `svg-inline` baseline. Extracting their svg to wrappers
would create wrappers with no live caller, which trips knip's \"unused
exports\" gate. Per the touch-it-fix-it scope rule (and
`feedback_test_as_bug_hunt` — migration PRs shouldn't carry
business-code fixes), this PR doesn't delete them. **Follow-up:** a
separate cleanup PR should remove these two files and any dangling
references.

## New icon wrappers (13)

**Feather-style category icons** (QuickActionCards): CalendarLinedIcon,
ActivityIcon, PencilIcon, CodeBracketsIcon, DollarSignIcon,
ShoppingCartIcon, CubeIcon, SearchIcon, ChatBubbleIcon, ChevronRightIcon

**Generic ui primitives** used in ToolGroup (will be reused widely in
upcoming chat PRs): ChevronDownIcon, PlusIcon

**WorkspaceFilesTab**: RefreshIcon

## Visual fidelity: 0 risk

All wrappers preserve \`path\` / \`viewBox\` / \`fill\` / \`stroke\` /
\`strokeWidth\` / \`strokeLinecap\` / \`strokeLinejoin\` byte-for-byte
from the original code. Naming distinguishes Feather-style
(\`CalendarLinedIcon\`) from existing Heroicons-style (\`CalendarIcon\`)
so future call sites pick the right visual variant.

## Test plan

- [x] \`pnpm lint\` clean
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint:ci\` clean (✓ All web/ ci-lint checks passed — no knip
unused-export issues)
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` shows 116 → 112
(✓ shrink)
- [x] Sibling shrink scripts (react/forbid-dom-props, no-raw-fetch)
unchanged
- [ ] Visual regression on staging: chat quick-action cards, tool group
expand/collapse, resources panel close, workspace files refresh — each
pixel-identical to main

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Continues #1307. Migrates 4 active `chat/` files (15 actual `<svg>` occurrences, 14 unique shapes after dedup) to `ui/icons/` wrappers and shrinks the `svg-inline` baseline from **116 → 112**.

## Files migrated

| File | svgs | new wrappers used |
|---|---|---|
| `QuickActionCards.tsx` | 10 | 10 category icons + ChevronRightIcon |
| `ToolGroup.tsx` | 3 | BoltSolidIcon (reused from #1307), ChevronDownIcon, PlusIcon |
| `ResourcesPanel.tsx` | 1 | CloseIcon (reused from #1307) |
| `WorkspaceFilesTab.tsx` | 1 | RefreshIcon |

## NOT migrated (pre-existing dead code)

- `ChatWelcome.tsx` — no importer in repo
- `ToolProgressFloat.tsx` — `<ToolProgressFloat />` used in `GenClawClient.tsx` but the corresponding `import` line above it is commented out

Both stay in the `svg-inline` baseline. Extracting their svg to wrappers would create wrappers with no live caller, which trips knip's \"unused exports\" gate. Per the touch-it-fix-it scope rule (and `feedback_test_as_bug_hunt` — migration PRs shouldn't carry business-code fixes), this PR doesn't delete them. **Follow-up:** a separate cleanup PR should remove these two files and any dangling references.

## New icon wrappers (13)

**Feather-style category icons** (QuickActionCards): CalendarLinedIcon, ActivityIcon, PencilIcon, CodeBracketsIcon, DollarSignIcon, ShoppingCartIcon, CubeIcon, SearchIcon, ChatBubbleIcon, ChevronRightIcon

**Generic ui primitives** used in ToolGroup (will be reused widely in upcoming chat PRs): ChevronDownIcon, PlusIcon

**WorkspaceFilesTab**: RefreshIcon

## Visual fidelity: 0 risk

All wrappers preserve \`path\` / \`viewBox\` / \`fill\` / \`stroke\` / \`strokeWidth\` / \`strokeLinecap\` / \`strokeLinejoin\` byte-for-byte from the original code. Naming distinguishes Feather-style (\`CalendarLinedIcon\`) from existing Heroicons-style (\`CalendarIcon\`) so future call sites pick the right visual variant.

## Test plan

- [x] \`pnpm lint\` clean
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint:ci\` clean (✓ All web/ ci-lint checks passed — no knip unused-export issues)
- [x] \`bash scripts/check-svg-ignores-shrink-only.sh\` shows 116 → 112 (✓ shrink)
- [x] Sibling shrink scripts (react/forbid-dom-props, no-raw-fetch) unchanged
- [ ] Visual regression on staging: chat quick-action cards, tool group expand/collapse, resources panel close, workspace files refresh — each pixel-identical to main

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(web): extract inline <svg> to ui/icons/ + lint guard (#1307)

- **SHA**: `d7c4c6c4849851e144536feaeecdaf465c401596`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T10:50:01Z
- **PR**: #1307

### Commit Message

```
feat(web): extract inline <svg> to ui/icons/ + lint guard (#1307)

## Summary

- Inline `<svg>` JSX is sprawling — **120 files / 407 occurrences**
before this PR; close X duplicated 23 times, chevron-right 13 times.
Stops the spread by extracting wrappers to `src/components/ui/icons/`,
adding a `no-restricted-syntax` error for inline `<svg>`, and
grandfathering the 116 remaining files in a SHRINK-ONLY (svg-inline)
section enforced by CI.
- **Visual fidelity: 0 risk.** Each wrapper preserves `path` / `viewBox`
/ `fill` / `stroke` / `strokeWidth` / `strokeLinecap` / `strokeLinejoin`
byte-for-byte from the original code. No external icon library
introduced (`lucide-react` remains untouched in `ZoomControls.tsx`).
- Demo migration on 3 hot files: SideNav (20 svgs), GenClawInput (7
svgs), `admin/components/CloseIcon.tsx` (1 svg, orphan removed).
Subsequent PRs shrink the list per directory (chat / components / admin
/ artifacts / etc.).

## Architecture notes

- **Why merge into the colors+raw-fetch block?** Flat-config `rules` are
REPLACED (not merged) when multiple blocks match a file. A separate svg
block would silently drop color/raw-fetch checks for everything matching
both. So the svg selector goes into the same `no-restricted-syntax`
array as the existing color rules and the raw-fetch ban (#1296), and the
svg ignores list goes into the same block's `ignores`. Trade-off: 116
svg-legacy files temporarily lose color/raw-fetch coverage too — but the
regression window is bounded (it returns when the file is migrated and
removed from the list, which the touch-it-fix-it convention encourages).
- **Why a sibling shrink-only script?** Each script anchors on its own
scoped sentinel (`SHRINK-ONLY (svg-inline)` / `SHRINK-ONLY
(no-raw-fetch)` / unscoped `SHRINK-ONLY: do NOT add new entries here`
for react/forbid-dom-props), so the three lists don't false-match each
other through the awk range.
- **Bootstrap path:** when origin/main has no `END SHRINK-ONLY
(svg-inline)` sentinel yet, growth from 0 → N is allowed once.
Subsequent PRs go through the normal shrink-only check.

## Files changed

- New: `src/components/ui/icons/` (19 wrapper files + `index.ts` barrel)
- New: `web/scripts/check-svg-ignores-shrink-only.sh`
- Modified: `web/eslint.config.mjs` (svg ignores + selector merged into
existing colors+raw-fetch block)
- Modified: `.github/workflows/code-quality.yml` (CI step)
- Modified: `web/CLAUDE.md` (Icons section, Code Style summary)
- Modified: `web/src/components/SideNav.tsx`,
`web/src/app/[locale]/chat/components/GenClawInput.tsx` (demo migration)
- Modified:
`web/src/app/[locale]/admin/components/{BotsTab,OrderHistoryModal}.tsx`
(use new shared `CloseIcon`)
- Deleted: `web/src/app/[locale]/admin/components/CloseIcon.tsx`
(orphan, migrated)

## Test plan

- [x] `pnpm lint` clean
- [x] `npx tsc --noEmit` clean
- [x] All 3 shrink-only scripts pass (`react/forbid-dom-props`: 45→45,
`no-raw-fetch`: 15→15, `svg-inline`: bootstrap 0→116)
- [x] Positive test: a fresh inline `<svg>` outside `ui/icons/` is
caught by the rule with the proper Chinese message
- [x] All 4097 unit tests pass
- [ ] Visual regression check on staging
(`ecommerce-studio-web-staging.chris-a5e.workers.dev`): SideNav main nav
+ GenClawInput chat input + admin tab close buttons render identical to
main

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

- Inline `<svg>` JSX is sprawling — **120 files / 407 occurrences** before this PR; close X duplicated 23 times, chevron-right 13 times. Stops the spread by extracting wrappers to `src/components/ui/icons/`, adding a `no-restricted-syntax` error for inline `<svg>`, and grandfathering the 116 remaining files in a SHRINK-ONLY (svg-inline) section enforced by CI.
- **Visual fidelity: 0 risk.** Each wrapper preserves `path` / `viewBox` / `fill` / `stroke` / `strokeWidth` / `strokeLinecap` / `strokeLinejoin` byte-for-byte from the original code. No external icon library introduced (`lucide-react` remains untouched in `ZoomControls.tsx`).
- Demo migration on 3 hot files: SideNav (20 svgs), GenClawInput (7 svgs), `admin/components/CloseIcon.tsx` (1 svg, orphan removed). Subsequent PRs shrink the list per directory (chat / components / admin / artifacts / etc.).

## Architecture notes

- **Why merge into the colors+raw-fetch block?** Flat-config `rules` are REPLACED (not merged) when multiple blocks match a file. A separate svg block would silently drop color/raw-fetch checks for everything matching both. So the svg selector goes into the same `no-restricted-syntax` array as the existing color rules and the raw-fetch ban (#1296), and the svg ignores list goes into the same block's `ignores`. Trade-off: 116 svg-legacy files temporarily lose color/raw-fetch coverage too — but the regression window is bounded (it returns when the file is migrated and removed from the list, which the touch-it-fix-it convention encourages).
- **Why a sibling shrink-only script?** Each script anchors on its own scoped sentinel (`SHRINK-ONLY (svg-inline)` / `SHRINK-ONLY (no-raw-fetch)` / unscoped `SHRINK-ONLY: do NOT add new entries here` for react/forbid-dom-props), so the three lists don't false-match each other through the awk range.
- **Bootstrap path:** when origin/main has no `END SHRINK-ONLY (svg-inline)` sentinel yet, growth from 0 → N is allowed once. Subsequent PRs go through the normal shrink-only check.

## Files changed

- New: `src/components/ui/icons/` (19 wrapper files + `index.ts` barrel)
- New: `web/scripts/check-svg-ignores-shrink-only.sh`
- Modified: `web/eslint.config.mjs` (svg ignores + selector merged into existing colors+raw-fetch block)
- Modified: `.github/workflows/code-quality.yml` (CI step)
- Modified: `web/CLAUDE.md` (Icons section, Code Style summary)
- Modified: `web/src/components/SideNav.tsx`, `web/src/app/[locale]/chat/components/GenClawInput.tsx` (demo migration)
- Modified: `web/src/app/[locale]/admin/components/{BotsTab,OrderHistoryModal}.tsx` (use new shared `CloseIcon`)
- Deleted: `web/src/app/[locale]/admin/components/CloseIcon.tsx` (orphan, migrated)

## Test plan

- [x] `pnpm lint` clean
- [x] `npx tsc --noEmit` clean
- [x] All 3 shrink-only scripts pass (`react/forbid-dom-props`: 45→45, `no-raw-fetch`: 15→15, `svg-inline`: bootstrap 0→116)
- [x] Positive test: a fresh inline `<svg>` outside `ui/icons/` is caught by the rule with the proper Chinese message
- [x] All 4097 unit tests pass
- [ ] Visual regression check on staging (`ecommerce-studio-web-staging.chris-a5e.workers.dev`): SideNav main nav + GenClawInput chat input + admin tab close buttons render identical to main

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(chat-replay): public /share viewer + BFF proxy (ECA-548 2/3) (#1301)

- **SHA**: `9bc91aa8c86cd9f8ee9515edb94742b471b4d51c`
- **作者**: kaka-srp
- **日期**: 2026-04-24T10:14:23Z
- **PR**: #1301

### Commit Message

```
feat(chat-replay): public /share viewer + BFF proxy (ECA-548 2/3) (#1301)

## Summary

Second of three stacked PRs
([ECA-548](https://linear.app/srpone/issue/ECA-548/share-selected-chat-messages-as-replay-page)).
Adds the public-viewer half of the chat-replay share feature — the
`/share/[shareId]` route that renders the conversation verbatim using
the existing chat components, plus the Next.js BFF proxy layer bridging
viewers to the backend from #1300.

- **Visual parity with chat**: `ReplayPlayer` stands up a minimal
`@assistant-ui/react` runtime around a sliced view of the snapshot and
reuses **the real `OpenClawThread` + `OpenClawUserMessage` +
`OpenClawAssistantMessage`**. Zero fork of message rendering. Auto-play
grows `revealedCount` over time with spec's adaptive delay (`clamp(700 +
content.length * 8, 900, 3500)`).
- **`ReplayContext`**: `{ readOnly, shareId }`, defaults to `{readOnly:
false}` so chat page behavior is byte-identical. Consumed by
`MMAttachments` (swaps to public proxy URL, no MM-Bearer blob fetch) and
`ActionsCard` / `FormCard` (disables interactive handlers). File
attachments reuse **the existing `window.openFilePreview` +
`ArtifactsSidebar`** — clicking a PDF opens the artifact sidebar just
like in live chat.
- **BFF**: `/api/chat-replays{,/[shareId]{,/revoke,/files/[fileId]}}`
proxies. Public GET streams body (no `.text()` buffering on Workers). CF
Access headers extracted into shared `getCFAccessHeaders()`.
- **Middleware**: `PUBLIC_API_GET_PREFIXES` allows unauthenticated GET
on `/api/chat-replays/*` (length guard keeps the list route auth-gated);
`/share` added to locale-skip.
- **Reduced-motion**: `usePrefersReducedMotion` flips after mount —
added an effect so users with `prefers-reduced-motion` jump to final
state instead of landing on a blank frozen frame.

## Stack

- PR 1 (#1300): backend ← `main`
- **PR 2 (this one)**: viewer + BFF ← base: `feat/eca-548-a-backend`
- PR 3: `/chat` selection UI ← base: this branch

⚠ Merge order: #1300 first, then this. When PR 1 merges, rebase this
onto main (or GitHub will auto-update the base).

## Test plan

- [x] `pnpm tsc --noEmit` clean, `pnpm exec eslint` clean
- [x] `useReplayPlayer` unit tests (auto-play / pause / resume / skip /
restart / reduced-motion)
- [x] Manual E2E: open `/share/<id>` in incognito → auto-play works,
ERMP action cards show disabled, file attachments open in artifacts
sidebar, `prefers-reduced-motion` renders everything immediately
- [ ] CI green
```

### PR Description

## Summary

Second of three stacked PRs ([ECA-548](https://linear.app/srpone/issue/ECA-548/share-selected-chat-messages-as-replay-page)). Adds the public-viewer half of the chat-replay share feature — the `/share/[shareId]` route that renders the conversation verbatim using the existing chat components, plus the Next.js BFF proxy layer bridging viewers to the backend from #1300.

- **Visual parity with chat**: `ReplayPlayer` stands up a minimal `@assistant-ui/react` runtime around a sliced view of the snapshot and reuses **the real `OpenClawThread` + `OpenClawUserMessage` + `OpenClawAssistantMessage`**. Zero fork of message rendering. Auto-play grows `revealedCount` over time with spec's adaptive delay (`clamp(700 + content.length * 8, 900, 3500)`).
- **`ReplayContext`**: `{ readOnly, shareId }`, defaults to `{readOnly: false}` so chat page behavior is byte-identical. Consumed by `MMAttachments` (swaps to public proxy URL, no MM-Bearer blob fetch) and `ActionsCard` / `FormCard` (disables interactive handlers). File attachments reuse **the existing `window.openFilePreview` + `ArtifactsSidebar`** — clicking a PDF opens the artifact sidebar just like in live chat.
- **BFF**: `/api/chat-replays{,/[shareId]{,/revoke,/files/[fileId]}}` proxies. Public GET streams body (no `.text()` buffering on Workers). CF Access headers extracted into shared `getCFAccessHeaders()`.
- **Middleware**: `PUBLIC_API_GET_PREFIXES` allows unauthenticated GET on `/api/chat-replays/*` (length guard keeps the list route auth-gated); `/share` added to locale-skip.
- **Reduced-motion**: `usePrefersReducedMotion` flips after mount — added an effect so users with `prefers-reduced-motion` jump to final state instead of landing on a blank frozen frame.

## Stack

- PR 1 (#1300): backend ← `main`
- **PR 2 (this one)**: viewer + BFF ← base: `feat/eca-548-a-backend`
- PR 3: `/chat` selection UI ← base: this branch

⚠ Merge order: #1300 first, then this. When PR 1 merges, rebase this onto main (or GitHub will auto-update the base).

## Test plan

- [x] `pnpm tsc --noEmit` clean, `pnpm exec eslint` clean
- [x] `useReplayPlayer` unit tests (auto-play / pause / resume / skip / restart / reduced-motion)
- [x] Manual E2E: open `/share/<id>` in incognito → auto-play works, ERMP action cards show disabled, file attachments open in artifacts sidebar, `prefers-reduced-motion` renders everything immediately
- [ ] CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## docs: archive completed specs + new WS-fallback spec (#1304)

- **SHA**: `8d85a74a3e8dc1d7aff8b34efd0365f933c2e4f5`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T09:52:35Z
- **PR**: #1304

### Commit Message

```
docs: archive completed specs + new WS-fallback spec (#1304)

## Summary

Docs-only housekeeping — no source code changes. Two logical commits:

**1. Add new design spec**
(`docs/superpowers/specs/2026-04-24-zooclaw-main-chat-drop-ws-fallback.md`)
— single-PR plan to remove the unreachable direct-to-OpenClaw-Gateway WS
fallback from `web/src/app/[locale]/chat/`. Mattermost is now the sole
transport; `page.tsx` pins `<GenClawClient forceMM />`, so the WS `else`
branches in `GenClawClient` and the 759-line `useOpenClawChat` hook are
dead code. Spec lists 4 implementation steps + verification + rollback.
Implementation not in this PR.

**2. Sweep the specs directory** so it reflects open work, not
historical debris.

### Archived (work already landed in production)

| File | Evidence |
|---|---|
| `plans/2026-03-19-mattermost-plan.md` | MM integration shipped (#152,
main chat now MM-only) |
| `plans/2026-03-24-integration-platform-requirements.md` | Nango
selected + deployed |
| `plans/2026-03-24-third-party-integration-design.md` | Design
evaluation closed |
| `plans/2026-03-28-nango-integrations-batch1.md` | First batch live
(#1294 Google connectors) |
| `superpowers/specs/2026-04-14-stripe-cleanup.md` | Self-marked ✅
Completed (PR 1-11 merged) |
| `superpowers/specs/2026-04-16-deptry-rollout.md` | Self-marked
Completed; `04-deptry.sh` gate live |

### Status updated (Draft → Completed; spec stayed in place)

| File | Shipping evidence |
|---|---|
| `superpowers/specs/2026-04-20-web-dead-code.md` | knip hard gate #1291
(B2 → B4 → B5 → B6) |
| `superpowers/specs/2026-04-20-web-import-boundaries.md` |
dependency-cruiser hard gate #1115 (A1-PR2) |

### Renamed (file name didn't match content)

- `plans/2026-04-01-image-service-decomposition.md` →
`plans/2026-04-01-litellm-decomposition.md`
- Content titled "litellm.py Incremental Decomposition Plan (Provider
Pattern)"
- Added Status header: PR 1/7 merged (#478), `litellm.py` still ~2665
lines, 6 PRs remaining

### Link fixes (so archived moves don't leave broken refs)

- `web-dead-code.md` + `web-import-boundaries.md` → archive path for
deptry-rollout link
- `service-layer-exceptions.md` → archive path for stripe-cleanup (2
places)

Verified with `grep -rn "<old-filename>" docs/ web/ services/` — no
broken links remain outside `docs/archive/` itself.

## Test plan

- [x] No code changes — lint/type/test not applicable
- [x] grep for all old spec filenames; updated all refs outside
`docs/archive/`
- [x] `git mv` preserves history for the 6 archived + 1 renamed file
- [x] Pre-commit hooks pass (ran locally)
- [ ] CI: `code-quality / lint-and-test` and `python-code-quality /
build-and-test` both target `web/**` / `services/**` — neither should
trigger on docs-only diff

## Out of scope

- Actually implementing the WS-fallback removal (the new spec describes
that, a future PR)
- Auditing the remaining Draft/Proposed specs (e.g.
`service-layer-exceptions` Proposed, several older specs missing
`Status:` headers) — see the "needs audit" and "consistency" sections of
the doc survey that prompted this PR

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Docs-only housekeeping — no source code changes. Two logical commits:

**1. Add new design spec** (`docs/superpowers/specs/2026-04-24-zooclaw-main-chat-drop-ws-fallback.md`) — single-PR plan to remove the unreachable direct-to-OpenClaw-Gateway WS fallback from `web/src/app/[locale]/chat/`. Mattermost is now the sole transport; `page.tsx` pins `<GenClawClient forceMM />`, so the WS `else` branches in `GenClawClient` and the 759-line `useOpenClawChat` hook are dead code. Spec lists 4 implementation steps + verification + rollback. Implementation not in this PR.

**2. Sweep the specs directory** so it reflects open work, not historical debris.

### Archived (work already landed in production)

| File | Evidence |
|---|---|
| `plans/2026-03-19-mattermost-plan.md` | MM integration shipped (#152, main chat now MM-only) |
| `plans/2026-03-24-integration-platform-requirements.md` | Nango selected + deployed |
| `plans/2026-03-24-third-party-integration-design.md` | Design evaluation closed |
| `plans/2026-03-28-nango-integrations-batch1.md` | First batch live (#1294 Google connectors) |
| `superpowers/specs/2026-04-14-stripe-cleanup.md` | Self-marked ✅ Completed (PR 1-11 merged) |
| `superpowers/specs/2026-04-16-deptry-rollout.md` | Self-marked Completed; `04-deptry.sh` gate live |

### Status updated (Draft → Completed; spec stayed in place)

| File | Shipping evidence |
|---|---|
| `superpowers/specs/2026-04-20-web-dead-code.md` | knip hard gate #1291 (B2 → B4 → B5 → B6) |
| `superpowers/specs/2026-04-20-web-import-boundaries.md` | dependency-cruiser hard gate #1115 (A1-PR2) |

### Renamed (file name didn't match content)

- `plans/2026-04-01-image-service-decomposition.md` → `plans/2026-04-01-litellm-decomposition.md`
  - Content titled "litellm.py Incremental Decomposition Plan (Provider Pattern)"
  - Added Status header: PR 1/7 merged (#478), `litellm.py` still ~2665 lines, 6 PRs remaining

### Link fixes (so archived moves don't leave broken refs)

- `web-dead-code.md` + `web-import-boundaries.md` → archive path for deptry-rollout link
- `service-layer-exceptions.md` → archive path for stripe-cleanup (2 places)

Verified with `grep -rn "<old-filename>" docs/ web/ services/` — no broken links remain outside `docs/archive/` itself.

## Test plan

- [x] No code changes — lint/type/test not applicable
- [x] grep for all old spec filenames; updated all refs outside `docs/archive/`
- [x] `git mv` preserves history for the 6 archived + 1 renamed file
- [x] Pre-commit hooks pass (ran locally)
- [ ] CI: `code-quality / lint-and-test` and `python-code-quality / build-and-test` both target `web/**` / `services/**` — neither should trigger on docs-only diff

## Out of scope

- Actually implementing the WS-fallback removal (the new spec describes that, a future PR)
- Auditing the remaining Draft/Proposed specs (e.g. `service-layer-exceptions` Proposed, several older specs missing `Status:` headers) — see the "needs audit" and "consistency" sections of the doc survey that prompted this PR

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): useFetchContent → useQuery (RQ PR 1) (#1303)

- **SHA**: `c711eee3665cf70b58d5f1fa858e699fe179ec36`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T09:40:07Z
- **PR**: #1303

### Commit Message

```
refactor(web): useFetchContent → useQuery (RQ PR 1) (#1303)

## Summary

First domain migration of the React Query rollout (after PR #1296
infra).

- **\`useFetchContent\` → \`useQuery\`** —
\`src/components/artifacts/renderers/useFetchContent.ts\` internals
replaced. Raw fetch lifted to
\`src/lib/api/artifact.ts::fetchArtifactContent()\` (permanent
allowlist), so the component layer is fetch-free.
- **Foundations landed** — \`src/lib/query/keys.ts\` (\`QUERY_VERSION\`,
deferred from PR 0) + \`src/hooks/queries/artifact/keys.ts\`
(\`artifactKeys.content(url)\`).
- **Defaults overridden for this hook** — \`staleTime: Infinity\` +
\`refetchOnWindowFocus: false\` (artifact URLs are immutable presigned
resources; refetching them gains nothing and costs bandwidth).
- **Return shape preserved** — \`{content, loading, error}\` unchanged,
so the 5 caller renderers (Code/Csv/Markdown/Mermaid/Source) need no
edits.
- **SHRINK-ONLY shrunk** — \`useFetchContent.ts\` removed from
no-raw-fetch ignores; CI guard now enforces it.

Spec:
[\`docs/superpowers/specs/2026-04-24-react-query-migration.md\`](docs/superpowers/specs/2026-04-24-react-query-migration.md).

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm lint:ci\` clean (knip dep-health hard gate)
- [x] New spec — 6 cases (success / HTTP 4xx / network error / empty url
/ dedupe / url switch)
- [x] \`pnpm test:unit\` full run — 253 files pass; useFetchContent's
caller renderers had no existing tests but their import shape is
preserved
- [ ] Local \`pnpm dev\` — open a code/csv/markdown/mermaid artifact,
confirm content renders

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

First domain migration of the React Query rollout (after PR #1296 infra).

- **\`useFetchContent\` → \`useQuery\`** — \`src/components/artifacts/renderers/useFetchContent.ts\` internals replaced. Raw fetch lifted to \`src/lib/api/artifact.ts::fetchArtifactContent()\` (permanent allowlist), so the component layer is fetch-free.
- **Foundations landed** — \`src/lib/query/keys.ts\` (\`QUERY_VERSION\`, deferred from PR 0) + \`src/hooks/queries/artifact/keys.ts\` (\`artifactKeys.content(url)\`).
- **Defaults overridden for this hook** — \`staleTime: Infinity\` + \`refetchOnWindowFocus: false\` (artifact URLs are immutable presigned resources; refetching them gains nothing and costs bandwidth).
- **Return shape preserved** — \`{content, loading, error}\` unchanged, so the 5 caller renderers (Code/Csv/Markdown/Mermaid/Source) need no edits.
- **SHRINK-ONLY shrunk** — \`useFetchContent.ts\` removed from no-raw-fetch ignores; CI guard now enforces it.

Spec: [\`docs/superpowers/specs/2026-04-24-react-query-migration.md\`](docs/superpowers/specs/2026-04-24-react-query-migration.md).

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm lint:ci\` clean (knip dep-health hard gate)
- [x] New spec — 6 cases (success / HTTP 4xx / network error / empty url / dedupe / url switch)
- [x] \`pnpm test:unit\` full run — 253 files pass; useFetchContent's caller renderers had no existing tests but their import shape is preserved
- [ ] Local \`pnpm dev\` — open a code/csv/markdown/mermaid artifact, confirm content renders

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(chat-replay): backend snapshot infrastructure (ECA-548 1/3) (#1300)

- **SHA**: `90bf7c1271d28c25eb45e66adfbd2c2d6f3d1666`
- **作者**: kaka-srp
- **日期**: 2026-04-24T09:42:25Z
- **PR**: #1300

### Commit Message

```
feat(chat-replay): backend snapshot infrastructure (ECA-548 1/3) (#1300)

## Summary

First of three stacked PRs
([ECA-548](https://linear.app/srpone/issue/ECA-548/share-selected-chat-messages-as-replay-page)).
Adds the backend half of a new feature that lets users share a selected
chunk of their chat as a public replay link.

- **Immutable snapshot + public API**: client sends MM post IDs, backend
**refetches** via admin token, re-applies visibility filter, and stores
a versioned snapshot in two Mongo collections (metadata + blob). Public
link is opaque, revocable, and idempotent on already-revoked.
- **Security boundary**: admin MM token can read any channel, so the
backend gates by checking the `channelId` is in the creator's
`openclaw_bots[].mattermost_bots[].dm_channel_id` list (narrowest MVP
scope per spec) — covered by the cross-user-channel unit test.
- **MM file proxy**: `GET /chat-replays/{id}/files/{fileId}` streams
bytes with `Cache-Control: private, no-store` so revocation is immediate
(no CDN/browser cache outliving the check).

Full design:
[docs/superpowers/specs/2026-04-24-chat-replay-share-design.md](../blob/main/docs/superpowers/specs/2026-04-24-chat-replay-share-design.md)

## Stack

- **PR 1 (this one)**: backend infrastructure ← base: `main`
- PR 2: `/share/[shareId]` viewer + BFF proxy ← base: this branch
- PR 3: `/chat` selection UI ← base: PR 2's branch

## Test plan

- [x] 43 unit tests green (14 `test_chat_replay_create.py` + 29
`test_chat_replay_visibility.py`)
- [x] `ruff check` / `pyright` / `lint-imports` all clean
- [x] All CI-lint guards (file length, complexity,
no-collection-strings, deptry, repo-sync)
- [ ] CI green on this PR
- [ ] Manual: `curl -X POST /chat-replays` with a valid token + valid
channel → 200 with `shareId`
```

### PR Description

## Summary

First of three stacked PRs ([ECA-548](https://linear.app/srpone/issue/ECA-548/share-selected-chat-messages-as-replay-page)). Adds the backend half of a new feature that lets users share a selected chunk of their chat as a public replay link.

- **Immutable snapshot + public API**: client sends MM post IDs, backend **refetches** via admin token, re-applies visibility filter, and stores a versioned snapshot in two Mongo collections (metadata + blob). Public link is opaque, revocable, and idempotent on already-revoked.
- **Security boundary**: admin MM token can read any channel, so the backend gates by checking the `channelId` is in the creator's `openclaw_bots[].mattermost_bots[].dm_channel_id` list (narrowest MVP scope per spec) — covered by the cross-user-channel unit test.
- **MM file proxy**: `GET /chat-replays/{id}/files/{fileId}` streams bytes with `Cache-Control: private, no-store` so revocation is immediate (no CDN/browser cache outliving the check).

Full design: [docs/superpowers/specs/2026-04-24-chat-replay-share-design.md](../blob/main/docs/superpowers/specs/2026-04-24-chat-replay-share-design.md)

## Stack

- **PR 1 (this one)**: backend infrastructure ← base: `main`
- PR 2: `/share/[shareId]` viewer + BFF proxy ← base: this branch
- PR 3: `/chat` selection UI ← base: PR 2's branch

## Test plan

- [x] 43 unit tests green (14 `test_chat_replay_create.py` + 29 `test_chat_replay_visibility.py`)
- [x] `ruff check` / `pyright` / `lint-imports` all clean
- [x] All CI-lint guards (file length, complexity, no-collection-strings, deptry, repo-sync)
- [ ] CI green on this PR
- [ ] Manual: `curl -X POST /chat-replays` with a valid token + valid channel → 200 with `shareId`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(web): replace xlsx with read-excel-file to close 4 high CVEs (#1299)

- **SHA**: `539e72006d75061520e5a1af2d21e03a50048ac7`
- **作者**: sam-srp
- **日期**: 2026-04-24T09:26:47Z
- **PR**: #1299

### Commit Message

```
fix(web): replace xlsx with read-excel-file to close 4 high CVEs (#1299)

## Summary
- Removes `xlsx@^0.18.5` and replaces with `read-excel-file@^8.0.3` in
the single consumer,
`web/src/components/artifacts/renderers/ExcelRenderer.tsx`.
- Closes 4 open Dependabot alerts on `xlsx` (#23 prototype pollution,
#24 ReDoS, #25, #26) — SheetJS removed the patched `0.19.3`/`0.20.2`
releases from npm, so no bump or `pnpm.overrides` can close these.
- Usage in this repo is **Import/Parse user uploads** (URL → Blob → rows
for preview), which is the "must migrate" path from #1254 — accept-risk
is not defensible.

## Why `read-excel-file` over SheetJS CDN tarball
- Option A (CDN tarball `https://cdn.sheetjs.com/...`) bypasses npm
provenance and the repo's `minimumReleaseAge` supply-chain gate, and
keeps the same SheetJS code that produced the CVE class.
- Option B with `read-excel-file`: npm-native, browser-focused, still
under ecosystem review. API (`readXlsxFile(blob, { sheet })` +
`readSheetNames(blob)`) maps 1:1 onto the existing `(rows, sheets,
activeSheet)` state — minimal-diff migration.
- Bundle shrinks from ~400KB (xlsx) to ~100KB (read-excel-file) inside
the dynamically-imported chunk.

## Behavior diff for users
| Case | Before | After |
|---|---|---|
| Text / number / formula-result cells | ✅ | ✅ |
| Date cells | ❌ Rendered as Excel serial number (e.g. `45291`) because
`cellDates: true` was not set | ✅ Native `Date` → `toLocaleDateString()`
|
| Multi-sheet tabs | ✅ | ✅ |
| Merged cells, styling, virtualization | ❌ (unchanged) | ❌ (unchanged —
out of scope) |
| Exotic/malformed xlsx files | Sometimes parsed by SheetJS's lenient
parser | May fall through to existing `.catch()` → "Failed to load" +
download link (no crash) |

## Test plan
- [ ] Open an xlsx attachment preview in chat artifacts — rows render
- [ ] Open an xlsx in Assets preview area — rows render
- [ ] Multi-sheet xlsx: sheet tabs switch content
- [ ] Spreadsheet with date column: dates render as dates, not
`45291`-style serial numbers
- [ ] Broken/corrupt xlsx URL: shows error message + Download link, no
white screen
- [ ] CI: `code-quality / lint-and-test` green

Closes #1254

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary
- Removes `xlsx@^0.18.5` and replaces with `read-excel-file@^8.0.3` in the single consumer, `web/src/components/artifacts/renderers/ExcelRenderer.tsx`.
- Closes 4 open Dependabot alerts on `xlsx` (#23 prototype pollution, #24 ReDoS, #25, #26) — SheetJS removed the patched `0.19.3`/`0.20.2` releases from npm, so no bump or `pnpm.overrides` can close these.
- Usage in this repo is **Import/Parse user uploads** (URL → Blob → rows for preview), which is the "must migrate" path from #1254 — accept-risk is not defensible.

## Why `read-excel-file` over SheetJS CDN tarball
- Option A (CDN tarball `https://cdn.sheetjs.com/...`) bypasses npm provenance and the repo's `minimumReleaseAge` supply-chain gate, and keeps the same SheetJS code that produced the CVE class.
- Option B with `read-excel-file`: npm-native, browser-focused, still under ecosystem review. API (`readXlsxFile(blob, { sheet })` + `readSheetNames(blob)`) maps 1:1 onto the existing `(rows, sheets, activeSheet)` state — minimal-diff migration.
- Bundle shrinks from ~400KB (xlsx) to ~100KB (read-excel-file) inside the dynamically-imported chunk.

## Behavior diff for users
| Case | Before | After |
|---|---|---|
| Text / number / formula-result cells | ✅ | ✅ |
| Date cells | ❌ Rendered as Excel serial number (e.g. `45291`) because `cellDates: true` was not set | ✅ Native `Date` → `toLocaleDateString()` |
| Multi-sheet tabs | ✅ | ✅ |
| Merged cells, styling, virtualization | ❌ (unchanged) | ❌ (unchanged — out of scope) |
| Exotic/malformed xlsx files | Sometimes parsed by SheetJS's lenient parser | May fall through to existing `.catch()` → "Failed to load" + download link (no crash) |

## Test plan
- [ ] Open an xlsx attachment preview in chat artifacts — rows render
- [ ] Open an xlsx in Assets preview area — rows render
- [ ] Multi-sheet xlsx: sheet tabs switch content
- [ ] Spreadsheet with date column: dates render as dates, not `45291`-style serial numbers
- [ ] Broken/corrupt xlsx URL: shows error message + Download link, no white screen
- [ ] CI: `code-quality / lint-and-test` green

Closes #1254

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## chore(web): React Query infra + raw-fetch lint guard (RQ PR 0) (#1296)

- **SHA**: `0d858bcec99db281c2243a4a9349116a7bb2ac8b`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T09:26:40Z
- **PR**: #1296

### Commit Message

```
chore(web): React Query infra + raw-fetch lint guard (RQ PR 0) (#1296)

## Summary

Bootstrap PR for migrating all client-side raw \`fetch()\` in \`web/\`
to \`@tanstack/react-query\` (RQ). Foundations + lint ratchet so PR 1-9
can land safely (and partly in parallel).

- **Infrastructure** — \`src/lib/query/\` (queryClient factory +
\`QUERY_VERSION\` + \`normalizeError\`);
\`tests/unit/helpers/queryWrapper.tsx\` lifted from admin;
\`ReactQueryDevtools\` mounted in dev only.
- **Lint guard** — \`no-restricted-syntax\` ban on
\`CallExpression[callee.name='fetch']\` in \`src/**\`, with permanent
allowlist for wrappers (\`lib/api/**\`, \`middleware.ts\`,
\`useSSEStream.ts\`, …) and a SHRINK-ONLY transitional list seeded with
the 16 files PR 1-8 will migrate.
- **CI gate** — \`web/scripts/check-no-raw-fetch-shrink-only.sh\`
hard-fails if the list grows. Bootstrap-aware (skips when origin/main
lacks the sentinel — that's this PR).
- **Defaults rationale** — \`staleTime: 30s\` (C-end baseline) +
\`refetchOnWindowFocus: true\` compose to "切回标签页 stale 才补刀";
\`mutations.retry: 0\` avoids double-spend on paid endpoints (LiteLLM).

Full 10-PR plan + decision rationale:
[\`docs/superpowers/specs/2026-04-24-react-query-migration.md\`](docs/superpowers/specs/2026-04-24-react-query-migration.md).

## Test plan

- [x] \`pnpm tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm test:unit\` — 251 files / 4035 tests pass (admin wrapper
rename verified)
- [x] Spot check: writing \`fetch('x')\` in a non-ignored file triggers
the lint error
- [x] \`bash web/scripts/check-no-raw-fetch-shrink-only.sh\` runs
(bootstrap skip path)
- [ ] Local \`pnpm dev\` — admin dashboard loads; ReactQueryDevtools
floats bottom-right

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Bootstrap PR for migrating all client-side raw \`fetch()\` in \`web/\` to \`@tanstack/react-query\` (RQ). Foundations + lint ratchet so PR 1-9 can land safely (and partly in parallel).

- **Infrastructure** — \`src/lib/query/\` (queryClient factory + \`QUERY_VERSION\` + \`normalizeError\`); \`tests/unit/helpers/queryWrapper.tsx\` lifted from admin; \`ReactQueryDevtools\` mounted in dev only.
- **Lint guard** — \`no-restricted-syntax\` ban on \`CallExpression[callee.name='fetch']\` in \`src/**\`, with permanent allowlist for wrappers (\`lib/api/**\`, \`middleware.ts\`, \`useSSEStream.ts\`, …) and a SHRINK-ONLY transitional list seeded with the 16 files PR 1-8 will migrate.
- **CI gate** — \`web/scripts/check-no-raw-fetch-shrink-only.sh\` hard-fails if the list grows. Bootstrap-aware (skips when origin/main lacks the sentinel — that's this PR).
- **Defaults rationale** — \`staleTime: 30s\` (C-end baseline) + \`refetchOnWindowFocus: true\` compose to "切回标签页 stale 才补刀"; \`mutations.retry: 0\` avoids double-spend on paid endpoints (LiteLLM).

Full 10-PR plan + decision rationale: [\`docs/superpowers/specs/2026-04-24-react-query-migration.md\`](docs/superpowers/specs/2026-04-24-react-query-migration.md).

## Test plan

- [x] \`pnpm tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm test:unit\` — 251 files / 4035 tests pass (admin wrapper rename verified)
- [x] Spot check: writing \`fetch('x')\` in a non-ignored file triggers the lint error
- [x] \`bash web/scripts/check-no-raw-fetch-shrink-only.sh\` runs (bootstrap skip path)
- [ ] Local \`pnpm dev\` — admin dashboard loads; ReactQueryDevtools floats bottom-right

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(claw-interface): replace per-token httpx client cache with single client + dynamic auth (#840)

- **SHA**: `b2ceb520677035a752a638d81114343e21dee36e`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T08:52:30Z
- **PR**: #840

### Commit Message

```
refactor(claw-interface): replace per-token httpx client cache with single client + dynamic auth (#840)

Closes #815. Supersedes the original PR #840 which became conflicting
after #1055 refactored `openclaw_client.py` into a mixin package.

## Summary
- Drop `_app_clients` (FIFO-pretending-to-be-LRU), `_MAX_APP_CLIENTS`,
`_pending_closes`, `_closing`, `_admin_client`, `_get_admin_client`,
`_get_app_client`, `_delayed_close` — and the fire-and-forget GC race +
shutdown cancellation complexity they spawned.
- Single shared `httpx.AsyncClient` (lazy via `_get_client`); new
`_request(method, url, *, app_token=None, **kwargs)` injects
`Authorization` per request. `httpcore` already pools TCP/TLS by `(host,
port)`, so one client covers every token.
- `aclose()` drops from ~15 LOC to a 3-line close of the shared client.
- 44 call sites across 7 mixin files migrated to `_request`; routes
layer unchanged.
- Tests: delete 8 eviction/lifecycle/delayed_close tests (testing
implementation, not behavior); add 4 contract tests for `_request`
(admin-default auth, app_token override, extra-header preservation,
`aclose` idempotency); migrate 122 behavior tests from patching
`_get_app_client` to patching `_request`.

Net diff: **+280 / −585** across 10 files.

## Test plan
- [x] `pyright app/ tests/` — 0 errors
- [x] `ruff check + format` — clean
- [x] `pytest tests/unit/test_openclaw_client.py` — 146/146 passed
- [x] `pytest tests/unit/` — 2630/2630 passed
- [ ] Staging: observe p99 latency and active connection count
post-deploy

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR Description

Closes #815. Supersedes the original PR #840 which became conflicting after #1055 refactored `openclaw_client.py` into a mixin package.

## Summary
- Drop `_app_clients` (FIFO-pretending-to-be-LRU), `_MAX_APP_CLIENTS`, `_pending_closes`, `_closing`, `_admin_client`, `_get_admin_client`, `_get_app_client`, `_delayed_close` — and the fire-and-forget GC race + shutdown cancellation complexity they spawned.
- Single shared `httpx.AsyncClient` (lazy via `_get_client`); new `_request(method, url, *, app_token=None, **kwargs)` injects `Authorization` per request. `httpcore` already pools TCP/TLS by `(host, port)`, so one client covers every token.
- `aclose()` drops from ~15 LOC to a 3-line close of the shared client.
- 44 call sites across 7 mixin files migrated to `_request`; routes layer unchanged.
- Tests: delete 8 eviction/lifecycle/delayed_close tests (testing implementation, not behavior); add 4 contract tests for `_request` (admin-default auth, app_token override, extra-header preservation, `aclose` idempotency); migrate 122 behavior tests from patching `_get_app_client` to patching `_request`.

Net diff: **+280 / −585** across 10 files.

## Test plan
- [x] `pyright app/ tests/` — 0 errors
- [x] `ruff check + format` — clean
- [x] `pytest tests/unit/test_openclaw_client.py` — 146/146 passed
- [x] `pytest tests/unit/` — 2630/2630 passed
- [ ] Staging: observe p99 latency and active connection count post-deploy

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(openclaw): accept namespaced skill workspaces in agent archives (#1298)

- **SHA**: `0c726998918b8124979e2fffd45776d6a82f6759`
- **作者**: nolan-srp
- **日期**: 2026-04-24T08:46:24Z
- **PR**: #1298

### Commit Message

```
fix(openclaw): accept namespaced skill workspaces in agent archives (#1298)

## Summary
- accept when detecting archive-backed agent workspaces during OpenClaw
installs
- keep archive workspace detection working for legacy and markdown-based
layouts
- add focused backend unit coverage for the namespaced workspace
detection paths

## Behavior
- custom agent archives that package skills under no longer fail install
with solely because they omit legacy or top-level markdown files
- existing archive layouts that rely on or markdown files continue to
resolve as before
```

### PR Description

## Summary
- accept  when detecting archive-backed agent workspaces during OpenClaw installs
- keep archive workspace detection working for legacy  and markdown-based layouts
- add focused backend unit coverage for the namespaced workspace detection paths

## Behavior
- custom agent archives that package skills under  no longer fail install with  solely because they omit legacy  or top-level markdown files
- existing archive layouts that rely on  or markdown files continue to resolve as before

---

## feat(web): specialist consent + open-chat cards in agent messages (#1245)

- **SHA**: `5cea8af5f80ddd695df621047f06a97cc06a013a`
- **作者**: vincent-srp
- **日期**: 2026-04-24T08:18:47Z
- **PR**: #1245

### Commit Message

```
feat(web): specialist consent + open-chat cards in agent messages (#1245)

## Summary

Renders three new fenced code-block patterns emitted by agents into
interactive chat cards:

- `zooclaw-hire-specialist-consent@<id>` → neutral **Confirm / Cancel**
card
- `zooclaw-fire-specialist-consent@<id>` → destructive variant (red
chrome + ⚠️ banner)
- `zooclaw-open-specialist-chat@<id>` → avatar + greeting + send-style
CTA pill; click refreshes the local agent catalog then routes to
`/chat?agent_id=<id>`

Agent identity (display name, avatar) is resolved from the local catalog
using the info-string `@id`; the body markdown is presentational only.
Consent buttons send a localized, fully-composed message (`{label}
{action} {name}` — e.g. `确认雇佣 Market Analyst` / `confirm hiring Market
Analyst`). `{name}` prefers the catalog display name, falls back to
humanized agent id.

### Graceful degradation
- No quoted labels / no id → inline markdown render (not a raw code
block) so body text / URLs stay readable
- Everything unknown → falls through to the standard code-block renderer
(last resort)

### i18n
New keys across all 10 locales:
- `genClaw.specialistCardGreeting` — "Say hi 👋" / "打个招呼 👋" / …
- `genClaw.specialistCardAriaLabel` — "Start chat with {name}"
- `genClaw.consentHireMessageTemplate` — "{label} hiring {name}" /
"{label}雇佣 {name}" / …
- `genClaw.consentFireMessageTemplate` — "{label} firing {name}" /
"{label}解雇 {name}" / …

### Architecture note
Cards mounted via `createRoot` in `MarkdownContent`'s hydrate effect run
in a **detached React tree**, so they can't consume `LanguageContext` /
`RouterContext` directly. All context-dependent values (translated
strings, display name, avatar URL, router.push) are pre-resolved in the
main tree and passed as plain props — cards stay purely presentational.

## Test plan

- [x] `pnpm lint` clean
- [x] `pnpm tsc --noEmit` clean
- [x] Targeted vitest: 137 tests green
  - `renderMarkdownToHtml` — info-string parsing + fallback branches
- `SpecialistConsentCard` — hire / fire variants, button consumed state,
locale-agnostic label passthrough
- `SpecialistOpenCard` — avatar image / monogram fallback / img-error
fallback, keyboard activation
- `MarkdownContent` specialist hydration — confirm + cancel message
composition, suppression during streaming, no-labels / no-id degradation
- `OpenClawAssistantMessage` — unchanged behaviors still pass (new
router / team-refresh deps mocked)
- [ ] Manual: hire → confirm → tool runs → success → open-specialist
card appears → click → sidebar reflects new agent on destination page
- [ ] Manual: theme toggle (light + dark) — consent buttons, destructive
chrome, open-card pill all adapt via semantic tokens
- [ ] Manual: locale switch (at least en ↔ zh) — greeting pill + sent
consent message localize

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
Co-authored-by: peter-srp <peter@srp.one>
```

### PR Description

## Summary

Renders three new fenced code-block patterns emitted by agents into interactive chat cards:

- `zooclaw-hire-specialist-consent@<id>` → neutral **Confirm / Cancel** card
- `zooclaw-fire-specialist-consent@<id>` → destructive variant (red chrome + ⚠️ banner)
- `zooclaw-open-specialist-chat@<id>` → avatar + greeting + send-style CTA pill; click refreshes the local agent catalog then routes to `/chat?agent_id=<id>`

Agent identity (display name, avatar) is resolved from the local catalog using the info-string `@id`; the body markdown is presentational only. Consent buttons send a localized, fully-composed message (`{label} {action} {name}` — e.g. `确认雇佣 Market Analyst` / `confirm hiring Market Analyst`). `{name}` prefers the catalog display name, falls back to humanized agent id.

### Graceful degradation
- No quoted labels / no id → inline markdown render (not a raw code block) so body text / URLs stay readable
- Everything unknown → falls through to the standard code-block renderer (last resort)

### i18n
New keys across all 10 locales:
- `genClaw.specialistCardGreeting` — "Say hi 👋" / "打个招呼 👋" / …
- `genClaw.specialistCardAriaLabel` — "Start chat with {name}"
- `genClaw.consentHireMessageTemplate` — "{label} hiring {name}" / "{label}雇佣 {name}" / …
- `genClaw.consentFireMessageTemplate` — "{label} firing {name}" / "{label}解雇 {name}" / …

### Architecture note
Cards mounted via `createRoot` in `MarkdownContent`'s hydrate effect run in a **detached React tree**, so they can't consume `LanguageContext` / `RouterContext` directly. All context-dependent values (translated strings, display name, avatar URL, router.push) are pre-resolved in the main tree and passed as plain props — cards stay purely presentational.

## Test plan

- [x] `pnpm lint` clean
- [x] `pnpm tsc --noEmit` clean
- [x] Targeted vitest: 137 tests green
  - `renderMarkdownToHtml` — info-string parsing + fallback branches
  - `SpecialistConsentCard` — hire / fire variants, button consumed state, locale-agnostic label passthrough
  - `SpecialistOpenCard` — avatar image / monogram fallback / img-error fallback, keyboard activation
  - `MarkdownContent` specialist hydration — confirm + cancel message composition, suppression during streaming, no-labels / no-id degradation
  - `OpenClawAssistantMessage` — unchanged behaviors still pass (new router / team-refresh deps mocked)
- [ ] Manual: hire → confirm → tool runs → success → open-specialist card appears → click → sidebar reflects new agent on destination page
- [ ] Manual: theme toggle (light + dark) — consent buttons, destructive chrome, open-card pill all adapt via semantic tokens
- [ ] Manual: locale switch (at least en ↔ zh) — greeting pill + sent consent message localize

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(web): centralize trackPurchase in handlePaymentSuccess with dedup (#1242)

- **SHA**: `8931c4de209b49c5bd60030b972879598564777e`
- **作者**: Fangmiao-srp
- **日期**: 2026-04-24T08:16:27Z
- **PR**: #1242

### Commit Message

```
feat(web): centralize trackPurchase in handlePaymentSuccess with dedup (#1242)

## Summary
- Centralize `trackPurchase` in `handlePaymentSuccess` to cover all 3
payment paths (subscription success page, onboarding success page,
GenClaw inline checkout)
- Add sessionStorage dedup to prevent duplicate tracking on page refresh
- Include `is_trial` in event params — trial orders tracked with
`value=0`
- Add Google Ads conversion for purchase with
`value`/`currency`/`transaction_id`
- Align `OrderConfirmResponse` type with backend nested `{ order,
payment_status }` structure
- Fix field paths in `SuccessClient.tsx` (`order_status` →
`order.status`)

## Test plan
- [x] 8 unit tests for `handlePaymentSuccess`
(paid/trial/pending/failed/dedup scenarios)
- [x] 15 unit tests for `tracking.ts` (cents→dollars, trial value=0,
Google Ads conversion, Reddit Pixel)
- [ ] Manual: subscription purchase → verify GA4 purchase event in
DebugView
- [ ] Manual: trial subscription → verify `value=0` and `is_trial=true`
- [ ] Manual: refresh success page → verify no duplicate tracking

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Muyao Wang <muyao@MuyaodeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```

### PR Description

## Summary
- Centralize `trackPurchase` in `handlePaymentSuccess` to cover all 3 payment paths (subscription success page, onboarding success page, GenClaw inline checkout)
- Add sessionStorage dedup to prevent duplicate tracking on page refresh
- Include `is_trial` in event params — trial orders tracked with `value=0`
- Add Google Ads conversion for purchase with `value`/`currency`/`transaction_id`
- Align `OrderConfirmResponse` type with backend nested `{ order, payment_status }` structure
- Fix field paths in `SuccessClient.tsx` (`order_status` → `order.status`)

## Test plan
- [x] 8 unit tests for `handlePaymentSuccess` (paid/trial/pending/failed/dedup scenarios)
- [x] 15 unit tests for `tracking.ts` (cents→dollars, trial value=0, Google Ads conversion, Reddit Pixel)
- [ ] Manual: subscription purchase → verify GA4 purchase event in DebugView
- [ ] Manual: trial subscription → verify `value=0` and `is_trial=true`
- [ ] Manual: refresh success page → verify no duplicate tracking

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(web): add tracking for add_agent and send_message events (#1246)

- **SHA**: `38b104f02d8b7c5db6d29504ea76b83ef8dcf6fe`
- **作者**: Fangmiao-srp
- **日期**: 2026-04-24T08:07:56Z
- **PR**: #1246

### Commit Message

```
feat(web): add tracking for add_agent and send_message events (#1246)

## Summary
- Wire `trackAddAgent` after successful hire in `useAgentActions`
- Wire `trackSendMessage` after successful `chat.send` in
`useOpenClawChat` and `useSubagentChat`
- Add 6 unit tests covering success/failure paths for all three hooks

Part of PR #1032 split — covers `add_agent` and `send_message` P1
tracking events.

## Test plan
- [x] `useAgentActions`: trackAddAgent called with correct agent_id on
success, not called on failure
- [x] `useOpenClawChat`: trackSendMessage called with (messageId,
agentId, sessionKey) on success, not called on failure
- [x] `useSubagentChat`: trackSendMessage called with (messageId,
undefined, sessionKey) on success, not called on failure
- [ ] Manual: verify GA4 events fire in dev console after hiring an
agent and sending a message

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Muyao Wang <muyao@MuyaodeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```

### PR Description

## Summary
- Wire `trackAddAgent` after successful hire in `useAgentActions`
- Wire `trackSendMessage` after successful `chat.send` in `useOpenClawChat` and `useSubagentChat`
- Add 6 unit tests covering success/failure paths for all three hooks

Part of PR #1032 split — covers `add_agent` and `send_message` P1 tracking events.

## Test plan
- [x] `useAgentActions`: trackAddAgent called with correct agent_id on success, not called on failure
- [x] `useOpenClawChat`: trackSendMessage called with (messageId, agentId, sessionKey) on success, not called on failure
- [x] `useSubagentChat`: trackSendMessage called with (messageId, undefined, sessionKey) on success, not called on failure
- [ ] Manual: verify GA4 events fire in dev console after hiring an agent and sending a message

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## perf(api): cache user doc on _CheckoutCtx to eliminate duplicate Mongo reads (#746) (#773)

- **SHA**: `67ade1e90293cbaa2a37bd2fd4b30a04d0a9c2d1`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T08:01:41Z
- **PR**: #746

### Commit Message

```
perf(api): cache user doc on _CheckoutCtx to eliminate duplicate Mongo reads (#746) (#773)

## Summary

Caches the user doc on `_CheckoutCtx` to eliminate duplicate user reads
on the `checkout.session.completed` path.

**Before:** up to 3 calls to `user_repo.get_user(ctx.uid)` per event —
one in `_apply_base_order_update` (for the `old_stripe_sub_id` snapshot
fallback), plus one each in `_try_invite_trial_path` and
`_try_stripe_trial_path`.

**After:** 1 call, issued once by `_load_checkout_context` and reused by
every path helper via `ctx.user`. Saves ~5-20ms per webhook on the hot
billing path.

## Why a pre-update snapshot is sufficient

`user_repo.update_subscription_info` only mirrors Stripe IDs
(`subscription_id` / `customer_id` / `product_id`). The fields the
downstream helpers inspect (`subscription_status`, `team_id`,
`wallet_subscription_id`, `billing_customer_id`) are untouched, so a
single pre-update snapshot is valid for every downstream check. The
`_CheckoutCtx.user` docstring records this invariant so future edits
don't silently regress it.

For the `old_stripe_sub_id` snapshot, retry safety is preserved:
`_apply_base_order_update` still prefers
`ctx.order.get("old_stripe_sub_id")` (persisted on the order by a prior
attempt) over the cached user doc, so a retry after
`user`-update-success / `order`-update-fail still enters the upgrade
path.

## Rebase note

This PR was originally drafted against a pre-#771 tree where handlers
read user docs via raw `mongo.read_one(ACCOUNT_COLLECTION, ...)`. After
rebase onto main, the "migrate to `user_repo`" portion is already in
place (#771 PR B2), so this PR is now a single-concern change: add the
`ctx.user` cache and route the three path helpers through it.

## Test plan
- [x] `ruff format .` / `ruff check .` — clean
- [x] `ruff format --check .` — clean
- [x] `pyright app/ tests/` — 0 errors
- [x] `lint-imports` — all 8 contracts KEPT (C1 `mongo` import boundary
preserved)
- [x] `pytest tests/unit/test_checkout_*
tests/unit/test_subscription_manager.py
tests/bdd/step_defs/test_stripe_webhooks.py
tests/bdd/step_defs/test_stripe_webhook_dispatch.py
tests/bdd/step_defs/test_stripe_order_confirm.py` — 47 passed
- [x] BDD with `TEST_MONGODB_HOST=127.0.0.1 MONGODB_USER=
MONGODB_PASSWORD=` — 16 passed on checkout/order scope (memory:
`reference_local_bdd_mongo`)
- [ ] CI green

Resolves #746. Related: #771, #776.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

---

## feat: enable Google connectors in production + hide legacy Google Workspace (#1294)

- **SHA**: `7a9871ec44d368b0b03fc11892b1f7ba247bacde`
- **作者**: Leo-srp
- **日期**: 2026-04-24T07:48:30Z
- **PR**: #1294

### Commit Message

```
feat: enable Google connectors in production + hide legacy Google Workspace (#1294)

## Summary
- Add 5 Google Nango connectors to production whitelist
- Hide legacy Google Workspace (gog CLI) card in production

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Description

## Summary
- Add 5 Google Nango connectors to production whitelist
- Hide legacy Google Workspace (gog CLI) card in production

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(web): exclude 409 from Sentry httpClientIntegration + widen rate limit window (#1295)

- **SHA**: `ab6c650b4c12dbcfd652fd2ebc02cbea714fd964`
- **作者**: peter-srp
- **日期**: 2026-04-24T07:31:25Z
- **PR**: #1295

### Commit Message

```
fix(web): exclude 409 from Sentry httpClientIntegration + widen rate limit window (#1295)

## Summary
- **Exclude 409 from `httpClientIntegration`**: 409 (Conflict) is an
expected app state ("bot not ready") that frontend code handles via
try/catch, but Sentry's automatic fetch instrumentation captured it as
unhandled — generating 1229 events from a single user on the
claw-settings page
- **Widen rate limiter window**: from 1 minute → 5 minutes (still 5
events max) to catch slow-drip patterns (1 event/minute) that the old
1-minute window reset couldn't cap

## Context
[Sentry issue
#7417488438](https://serendipity-one-inc.sentry.io/issues/7417488438/) —
`HTTP Client Error with status code: 409` from
`api/openclaw/settings/resources`. 1270 total events, 12 users, but one
user contributed 96.8% (1229 events) due to repeated fetch attempts
every ~1 minute on the settings page.

Root cause: `httpClientIntegration({ failedRequestStatusCodes: [400,
[402, 599]] })` captures 409 at the browser fetch level before our
app-level try/catch runs. Same approach as the existing 401 exclusion
(auth failures are expected).

## Test plan
- [ ] Verify 409 responses from `api/openclaw/settings/resources` no
longer appear in Sentry
- [ ] Verify other HTTP errors (400, 402-408, 410-599) still captured
- [ ] Verify rate limiter caps repeated errors to 5 per 5-minute window

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary
- **Exclude 409 from `httpClientIntegration`**: 409 (Conflict) is an expected app state ("bot not ready") that frontend code handles via try/catch, but Sentry's automatic fetch instrumentation captured it as unhandled — generating 1229 events from a single user on the claw-settings page
- **Widen rate limiter window**: from 1 minute → 5 minutes (still 5 events max) to catch slow-drip patterns (1 event/minute) that the old 1-minute window reset couldn't cap

## Context
[Sentry issue #7417488438](https://serendipity-one-inc.sentry.io/issues/7417488438/) — `HTTP Client Error with status code: 409` from `api/openclaw/settings/resources`. 1270 total events, 12 users, but one user contributed 96.8% (1229 events) due to repeated fetch attempts every ~1 minute on the settings page.

Root cause: `httpClientIntegration({ failedRequestStatusCodes: [400, [402, 599]] })` captures 409 at the browser fetch level before our app-level try/catch runs. Same approach as the existing 401 exclusion (auth failures are expected).

## Test plan
- [ ] Verify 409 responses from `api/openclaw/settings/resources` no longer appear in Sentry
- [ ] Verify other HTTP errors (400, 402-408, 410-599) still captured
- [ ] Verify rate limiter caps repeated errors to 5 per 5-minute window

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(web): artifacts preview fixes + React lifecycle cleanup (#1292)

- **SHA**: `931eaf0cb2ba75b22eb8b47c715e1ff96d771595`
- **作者**: peter-srp
- **日期**: 2026-04-24T07:16:42Z
- **PR**: #1292

### Commit Message

```
fix(web): artifacts preview fixes + React lifecycle cleanup (#1292)

Artifact preview:
- FileAvailabilityGate: use HEAD with redirect:'manual' to avoid hitting
S3 presigned URLs (method mismatch → 403); only retry on 404
- Remove _t cache-buster from renderUrl — breaks presigned S3 signatures
when carried through 307 redirects; key-based remount handles reload
- Add aspect-ratio viewport control (16:9, 4:3, 9:16, 1:1) for visual
file types (html, pdf, svg, pptx, mermaid)
- Sidebar max width: 2/3 viewport; chat area min-width: 320px
- Workspace files: module-level cache (30s TTL) so panel reopen doesn't
refetch

Session lifecycle:
- useArtifactsSidebar: add sessionKey param, reset state on session
change; split auto-open / URL-sync into separate effects
- Fix onSubagentClose missing from effect deps

React lifecycle cleanup:
- GenClawClient: add cancellation to getClawSettings + getSubagentTasks
fetches; add uid to channel sessions effect deps
- useSubagentSessions: derive hasTerminalVisible boolean so dismiss
interval isn't torn down on every poll

Misc:
- .gitignore: .venv/ → .venv (match symlinks)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR Description

Artifact preview:
- FileAvailabilityGate: use HEAD with redirect:'manual' to avoid hitting S3 presigned URLs (method mismatch → 403); only retry on 404
- Remove _t cache-buster from renderUrl — breaks presigned S3 signatures when carried through 307 redirects; key-based remount handles reload
- Add aspect-ratio viewport control (16:9, 4:3, 9:16, 1:1) for visual file types (html, pdf, svg, pptx, mermaid)
- Sidebar max width: 2/3 viewport; chat area min-width: 320px
- Workspace files: module-level cache (30s TTL) so panel reopen doesn't refetch

Session lifecycle:
- useArtifactsSidebar: add sessionKey param, reset state on session change; split auto-open / URL-sync into separate effects
- Fix onSubagentClose missing from effect deps

React lifecycle cleanup:
- GenClawClient: add cancellation to getClawSettings + getSubagentTasks fetches; add uid to channel sessions effect deps
- useSubagentSessions: derive hasTerminalVisible boolean so dismiss interval isn't torn down on every poll

Misc:
- .gitignore: .venv/ → .venv (match symlinks)

---

## refactor(web): hoist GeneralTab + DiaryCards to components/settings — fix W5 (A1-PR13) (#1293)

- **SHA**: `de47b41f197797c4ae0e85b1671ae7d9bc36bbd5`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T06:52:41Z
- **PR**: #1293

### Commit Message

```
refactor(web): hoist GeneralTab + DiaryCards to components/settings — fix W5 (A1-PR13) (#1293)

## Summary
Fixes 1 of the 2 remaining `W5-feature-isolation` warnings (the one that
user previously called legitimate-family-coupling — turns out it's a
clean hoist).

`GeneralTab` is consumed by both `profile/ProfilePageClient` and
`claw-settings/ClawSettingsClient`. The W5 rule comment says: _"share
via src/components or src/lib"_ — so GeneralTab's rightful home is
`src/components/settings/`, next to the already-hoisted
`SettingsLayout`.

## Why DiaryCards also moves

GeneralTab imports `DiaryCards`. If only `GeneralTab` hoists and
`DiaryCards` stays in `src/app/[locale]/profile/components/`, then
`src/components/settings/GeneralTab.tsx` would be importing `src/app/**`
— a **W4 violation** (components must not import pages). Hoisting both
keeps the dependency chain legal.

## Net moves

| From | To |
|---|---|
| `src/app/[locale]/profile/components/GeneralTab.tsx` |
`src/components/settings/GeneralTab.tsx` |
| `src/app/[locale]/profile/components/DiaryCards.tsx` |
`src/components/settings/DiaryCards.tsx` |
| `tests/unit/app/profile/GeneralTab.unit.spec.tsx` |
`tests/unit/components/settings/GeneralTab.unit.spec.tsx` |
| `tests/unit/app/profile/DiaryCards.unit.spec.tsx` |
`tests/unit/components/settings/DiaryCards.unit.spec.tsx` |

Plus import/mock retargets in 3 caller files. Net diff: 8 files, +10 /
−19.

## Baseline

`.dependency-cruiser-known-violations.json`:
```diff
- // W5: claw-settings/ClawSettingsClient → profile/GeneralTab (1 entry removed)
  // W5: mini-chat/MiniChatClient → chat/components/index (stays — cascade-hoist too expensive, deferred)
```

## Remaining W5 (1)

`mini-chat/MiniChatClient → chat/SubagentChatPanel` — requires cascading
hoist of SubagentChatPanel + OpenClawThread + 3 message components + 2
hooks + constants (~2000 lines). Deferred per prior plan discussion; can
be broken into 3 sub-PRs when chat feature gets scheduled rework.

## Test plan
- [x] `npx tsc --noEmit` clean
- [x] `bash scripts/ci-lint/00-run-all.sh` green (dep-cruiser baseline 1
warn remaining, down from 2)
- [x] `tests/unit/components/settings/**` +
`tests/unit/app/claw-settings/ClawSettingsClient.unit.spec.tsx` — 64
tests pass

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary
Fixes 1 of the 2 remaining `W5-feature-isolation` warnings (the one that user previously called legitimate-family-coupling — turns out it's a clean hoist).

`GeneralTab` is consumed by both `profile/ProfilePageClient` and `claw-settings/ClawSettingsClient`. The W5 rule comment says: _"share via src/components or src/lib"_ — so GeneralTab's rightful home is `src/components/settings/`, next to the already-hoisted `SettingsLayout`.

## Why DiaryCards also moves

GeneralTab imports `DiaryCards`. If only `GeneralTab` hoists and `DiaryCards` stays in `src/app/[locale]/profile/components/`, then `src/components/settings/GeneralTab.tsx` would be importing `src/app/**` — a **W4 violation** (components must not import pages). Hoisting both keeps the dependency chain legal.

## Net moves

| From | To |
|---|---|
| `src/app/[locale]/profile/components/GeneralTab.tsx` | `src/components/settings/GeneralTab.tsx` |
| `src/app/[locale]/profile/components/DiaryCards.tsx` | `src/components/settings/DiaryCards.tsx` |
| `tests/unit/app/profile/GeneralTab.unit.spec.tsx` | `tests/unit/components/settings/GeneralTab.unit.spec.tsx` |
| `tests/unit/app/profile/DiaryCards.unit.spec.tsx` | `tests/unit/components/settings/DiaryCards.unit.spec.tsx` |

Plus import/mock retargets in 3 caller files. Net diff: 8 files, +10 / −19.

## Baseline

`.dependency-cruiser-known-violations.json`:
```diff
- // W5: claw-settings/ClawSettingsClient → profile/GeneralTab (1 entry removed)
  // W5: mini-chat/MiniChatClient → chat/components/index (stays — cascade-hoist too expensive, deferred)
```

## Remaining W5 (1)

`mini-chat/MiniChatClient → chat/SubagentChatPanel` — requires cascading hoist of SubagentChatPanel + OpenClawThread + 3 message components + 2 hooks + constants (~2000 lines). Deferred per prior plan discussion; can be broken into 3 sub-PRs when chat feature gets scheduled rework.

## Test plan
- [x] `npx tsc --noEmit` clean
- [x] `bash scripts/ci-lint/00-run-all.sh` green (dep-cruiser baseline 1 warn remaining, down from 2)
- [x] `tests/unit/components/settings/**` + `tests/unit/app/claw-settings/ClawSettingsClient.unit.spec.tsx` — 64 tests pass

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## chore(web): promote knip exports to CI hard gate (B6 final) (#1291)

- **SHA**: `f177f52c55bd6edc6459aae47bcbd134b6d9ee09`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T06:27:02Z
- **PR**: #1291

### Commit Message

```
chore(web): promote knip exports to CI hard gate (B6 final) (#1291)

## Summary
Flips the knip CI gate to **fail on any unused export** across `src/` /
`tests/` / `functions/`. Closes out the B6 series.

## Status after B6b/c/d/e

- **B6b** (PR #1277): cleaned `src/lib/` (29 → 0) + introduced `@public`
whitelist
- **B6c** (PR #1282): cleaned hooks/components/contexts/utils (10 → 0)
- **B6d/e** (PR #1285): cleaned `src/app/` + `tests/e2e/` (19 → 0)
- **This PR**: last 7 exports + hard-gate flip

## Last 7 unexports

Cascading fallout from B6c's re-export barrel shrink — these library
exports lost their downstream consumer but still have internal
self-refs:

| File | Unexported |
|---|---|
| `src/lib/customAgentPublishes.ts` | `sanitizeCustomAgentZipName`,
`decodeBase64PathValue` |
| `src/app/[locale]/chat/components/workspace-shared.tsx` |
`formatSize`, `FolderIcon`, `FileIcon`, `ChevronIcon`, `RefreshButton`
(5 local helpers consumed by sibling `FileRow` / `Breadcrumbs` / etc. in
same file) |

## Hard-gate change

`scripts/ci-lint/02-dead-code.sh`:
```diff
 pnpm exec knip --reporter symbols \
-  --include dependencies,devDependencies,unlisted,binaries,optionalPeerDependencies,unresolved,duplicates,files
+  --include dependencies,devDependencies,unlisted,binaries,optionalPeerDependencies,unresolved,duplicates,files,exports
```

Also updated the comment block to reflect B6 completion + the `@public`
escape hatch for scaffolded APIs.

## Verification

Two-way check on the gate:

1. **Unused export → fails CI**: added `export const
INTENTIONAL_UNUSED_FIXTURE = 'test'` to `src/lib/agentCatalogCache.ts`,
ran `02-dead-code.sh` → `exit=1`, reported correctly. Reverted.
2. **`@public` escape hatch still works**: added `/** @public demo
scaffold */ export const DEMO_SCAFFOLD_FIXTURE = 'test'` → `exit=0` ✓.
Reverted.

Baseline at main + this PR: **0 unused exports**.

## Test plan
- [x] `npx tsc --noEmit` clean
- [x] `bash scripts/ci-lint/00-run-all.sh` green
- [x] Hard-gate fixture test (unused export) → red
- [x] `@public`-tagged fixture → green

## Scaffolded-API tracking
The `@public` whitelist preserves 14 intentionally-kept future-use
exports:

- **`@public` in src/lib** (per #1278): `getOpenClawAgentUsecases`, 4 ×
`getRuntime*`, `cancelSubscription`, `isInTrial`, `getTrialDaysLeft`,
`trackAddAgent`, `trackSendMessage`, `trackPurchase`,
`getNoIndexRobots`, `createStaticPublicMetadata`
- **`@public` in tests/e2e/utils/assertions.ts** (per #1286):
`assertToolWasUsed`, `assertHasAudioCard`, `assertHasVideoCard`,
`assertKeywordsPresent`

Each is either (a) a frontend wrapper whose backend endpoint + proxy
route are live, awaiting a UI consumer, or (b) an assertion helper kept
on ice for the dual-check (content + format card) scenario restoration.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary
Flips the knip CI gate to **fail on any unused export** across `src/` / `tests/` / `functions/`. Closes out the B6 series.

## Status after B6b/c/d/e

- **B6b** (PR #1277): cleaned `src/lib/` (29 → 0) + introduced `@public` whitelist
- **B6c** (PR #1282): cleaned hooks/components/contexts/utils (10 → 0)
- **B6d/e** (PR #1285): cleaned `src/app/` + `tests/e2e/` (19 → 0)
- **This PR**: last 7 exports + hard-gate flip

## Last 7 unexports

Cascading fallout from B6c's re-export barrel shrink — these library exports lost their downstream consumer but still have internal self-refs:

| File | Unexported |
|---|---|
| `src/lib/customAgentPublishes.ts` | `sanitizeCustomAgentZipName`, `decodeBase64PathValue` |
| `src/app/[locale]/chat/components/workspace-shared.tsx` | `formatSize`, `FolderIcon`, `FileIcon`, `ChevronIcon`, `RefreshButton` (5 local helpers consumed by sibling `FileRow` / `Breadcrumbs` / etc. in same file) |

## Hard-gate change

`scripts/ci-lint/02-dead-code.sh`:
```diff
 pnpm exec knip --reporter symbols \
-  --include dependencies,devDependencies,unlisted,binaries,optionalPeerDependencies,unresolved,duplicates,files
+  --include dependencies,devDependencies,unlisted,binaries,optionalPeerDependencies,unresolved,duplicates,files,exports
```

Also updated the comment block to reflect B6 completion + the `@public` escape hatch for scaffolded APIs.

## Verification

Two-way check on the gate:

1. **Unused export → fails CI**: added `export const INTENTIONAL_UNUSED_FIXTURE = 'test'` to `src/lib/agentCatalogCache.ts`, ran `02-dead-code.sh` → `exit=1`, reported correctly. Reverted.
2. **`@public` escape hatch still works**: added `/** @public demo scaffold */ export const DEMO_SCAFFOLD_FIXTURE = 'test'` → `exit=0` ✓. Reverted.

Baseline at main + this PR: **0 unused exports**.

## Test plan
- [x] `npx tsc --noEmit` clean
- [x] `bash scripts/ci-lint/00-run-all.sh` green
- [x] Hard-gate fixture test (unused export) → red
- [x] `@public`-tagged fixture → green

## Scaffolded-API tracking
The `@public` whitelist preserves 14 intentionally-kept future-use exports:

- **`@public` in src/lib** (per #1278): `getOpenClawAgentUsecases`, 4 × `getRuntime*`, `cancelSubscription`, `isInTrial`, `getTrialDaysLeft`, `trackAddAgent`, `trackSendMessage`, `trackPurchase`, `getNoIndexRobots`, `createStaticPublicMetadata`
- **`@public` in tests/e2e/utils/assertions.ts** (per #1286): `assertToolWasUsed`, `assertHasAudioCard`, `assertHasVideoCard`, `assertKeywordsPresent`

Each is either (a) a frontend wrapper whose backend endpoint + proxy route are live, awaiting a UI consumer, or (b) an assertion helper kept on ice for the dual-check (content + format card) scenario restoration.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## chore(web): remove unused exports from src/app + tests/e2e (B6d + B6e) (#1285)

- **SHA**: `6d9f3df2a1ca6da9ff019763755cf412bfa3d03d`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T04:03:01Z
- **PR**: #1285

### Commit Message

```
chore(web): remove unused exports from src/app + tests/e2e (B6d + B6e) (#1285)

## Summary
Combined final sweep of knip's unused-export gap — covers `src/app/**`
(13) + `tests/e2e/**` (6). Categorized into the same buckets as PR
#1277.

## Pure deletes (zero refs)
| File | Removed |
|---|---|
| `app/[locale]/chat/hooks/useDeepLinkHireFlow.ts` |
`PENDING_PROMPT_TTL_MS` (constant + its "future work" comment — never
had a reader) |
| `app/[locale]/chat/hooks/index.ts` | Barrel re-exports for
`useOpenClawRuntime` + `useSubagentChat` (the real hooks stay;
direct-path imports from `GenClawClient.tsx` / `SubagentChatPanel.tsx`
are the live consumers) |
| `tests/e2e/fixtures/test-data.ts` | `MODELS`, `TEST_IMAGE_PATH` |

## `@public`-tagged scaffolds (tracked in #1278 / #1286)
| File | Kept |
|---|---|
| `app/_seo.ts` | `getNoIndexRobots` (sister to live `getGlobalRobots`),
`createStaticPublicMetadata` (sister to live
`createLocalizedPublicMetadata`) — both are ready-to-use SEO scaffolds
for no-index routes / static legal pages — tracked in #1278 |
| `tests/e2e/utils/assertions.ts` | `assertToolWasUsed`,
`assertHasAudioCard`, `assertHasVideoCard`, `assertKeywordsPresent` —
were call sites in PR #61 scenario specs; dropped in PR #283 when tests
pivoted to LLM-judge-only. Preserved pending **dual-check (content +
format card) restoration** tracked in #1286 |

## Drop `export` keyword (internal-only)
| File | Unexported |
|---|---|
| `app/_seo.ts` | `siteUrl`, `isStaging`, `getGlobalRobots`,
`localizePathname`, `getOrganizationSchema`, `getWebsiteSchema`,
`getSoftwareApplicationSchema` — 7 helpers with all call sites inside
`_seo.ts` itself |
| `app/[locale]/chat/lib/messageFilters.ts` | `SESSION_DIVIDER_CONTENT`
(only used inside `filterMessages` in same file) |

## Verification
For each reported export, ran `grep -rn '\b${name}\b' src/ tests/` and
counted occurrences outside the defining file. For the e2e assertion
helpers, traced full git history: they were legitimately used in the
original PR #61 scenario specs, dropped in PR #283's pivot to LLM-judge
assertions —
[#1286](https://github.com/SerendipityOneInc/ecap-workspace/issues/1286)
captures the product intent (each scenario should check **both** content
relevance AND format card rendering, not just one).

## Test plan
- [x] `npx tsc --noEmit` clean
- [x] `bash scripts/ci-lint/00-run-all.sh` green
- [x] Knip `src/app` + `tests/e2e` unused-exports: 19 → 0
- [x] `tests/unit/app/chat/**` — 349 tests pass

## Remaining (not in this PR)
- Hooks/components/contexts/utils cleanup → PR #1282 (B6c, awaiting
review)
- Once #1282 merges, baseline is fully zero → **final PR** can promote
`exports` category to knip hard gate via `--include files,exports,...`
in `scripts/ci-lint/02-dead-code.sh`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary
Combined final sweep of knip's unused-export gap — covers `src/app/**` (13) + `tests/e2e/**` (6). Categorized into the same buckets as PR #1277.

## Pure deletes (zero refs)
| File | Removed |
|---|---|
| `app/[locale]/chat/hooks/useDeepLinkHireFlow.ts` | `PENDING_PROMPT_TTL_MS` (constant + its "future work" comment — never had a reader) |
| `app/[locale]/chat/hooks/index.ts` | Barrel re-exports for `useOpenClawRuntime` + `useSubagentChat` (the real hooks stay; direct-path imports from `GenClawClient.tsx` / `SubagentChatPanel.tsx` are the live consumers) |
| `tests/e2e/fixtures/test-data.ts` | `MODELS`, `TEST_IMAGE_PATH` |

## `@public`-tagged scaffolds (tracked in #1278 / #1286)
| File | Kept |
|---|---|
| `app/_seo.ts` | `getNoIndexRobots` (sister to live `getGlobalRobots`), `createStaticPublicMetadata` (sister to live `createLocalizedPublicMetadata`) — both are ready-to-use SEO scaffolds for no-index routes / static legal pages — tracked in #1278 |
| `tests/e2e/utils/assertions.ts` | `assertToolWasUsed`, `assertHasAudioCard`, `assertHasVideoCard`, `assertKeywordsPresent` — were call sites in PR #61 scenario specs; dropped in PR #283 when tests pivoted to LLM-judge-only. Preserved pending **dual-check (content + format card) restoration** tracked in #1286 |

## Drop `export` keyword (internal-only)
| File | Unexported |
|---|---|
| `app/_seo.ts` | `siteUrl`, `isStaging`, `getGlobalRobots`, `localizePathname`, `getOrganizationSchema`, `getWebsiteSchema`, `getSoftwareApplicationSchema` — 7 helpers with all call sites inside `_seo.ts` itself |
| `app/[locale]/chat/lib/messageFilters.ts` | `SESSION_DIVIDER_CONTENT` (only used inside `filterMessages` in same file) |

## Verification
For each reported export, ran `grep -rn '\b${name}\b' src/ tests/` and counted occurrences outside the defining file. For the e2e assertion helpers, traced full git history: they were legitimately used in the original PR #61 scenario specs, dropped in PR #283's pivot to LLM-judge assertions — [#1286](https://github.com/SerendipityOneInc/ecap-workspace/issues/1286) captures the product intent (each scenario should check **both** content relevance AND format card rendering, not just one).

## Test plan
- [x] `npx tsc --noEmit` clean
- [x] `bash scripts/ci-lint/00-run-all.sh` green
- [x] Knip `src/app` + `tests/e2e` unused-exports: 19 → 0
- [x] `tests/unit/app/chat/**` — 349 tests pass

## Remaining (not in this PR)
- Hooks/components/contexts/utils cleanup → PR #1282 (B6c, awaiting review)
- Once #1282 merges, baseline is fully zero → **final PR** can promote `exports` category to knip hard gate via `--include files,exports,...` in `scripts/ci-lint/02-dead-code.sh`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix: rename google-sheets to google-sheet (#1290)

- **SHA**: `201f6eabb3faa3976fdc69e1e3f433b181735225`
- **作者**: Leo-srp
- **日期**: 2026-04-24T04:02:25Z
- **PR**: #1290

### Commit Message

```
fix: rename google-sheets to google-sheet (#1290)

Match Nango provider key. Updates integrations.ts, ProviderLogo.tsx, and
test.
```

### PR Description

Match Nango provider key. Updates integrations.ts, ProviderLogo.tsx, and test.

---

## chore(web): remove unused exports from hooks/components/contexts/utils (B6c) (#1282)

- **SHA**: `fff79803a1297fd5cc768af4e0fce9afee159e35`
- **作者**: Chris@ZooClaw
- **日期**: 2026-04-24T03:51:38Z
- **PR**: #1282

### Commit Message

```
chore(web): remove unused exports from hooks/components/contexts/utils (B6c) (#1282)

## Summary
Second B6b pass — covers the 10 unused exports knip reports outside
`src/lib/` (excluding `src/app/**` and `tests/**`, which land in later
PRs).

None of the 10 exports looked like scaffolded APIs (no corresponding
backend endpoint + proxy route pattern like PR #1277's `getRuntime*` /
`getOpenClawAgentUsecases`), so no \`@public\` preservation needed.

## Deletes (zero refs)
| File | Removed |
|---|---|
| `components/LocaleLink.tsx` | `useLocalizedPath` hook |
| `utils/admin-helpers.ts` | `getAgentPath` |
| `contexts/AppEnvironmentContext.tsx` | `useAppEnvironment` hook +
`useContext` import — the `AppEnvironmentProvider` stays (it writes
`window.isNativeApp` / `window.brandInfo` for non-React consumers) but
the React hook had zero callers |

## Drop `export` keyword (internal-only)
- `components/billing/SubscriptionPanel.tsx`: `SubscriptionPanelContext`
(only read by `useSubscriptionPanel()` + JSX provider in same file)

## Barrel shrink
- `hooks/useCustomAgentPublishes.ts`: the file was re-exporting 10 items
from `@/lib/customAgentPublishes` but only 4 are consumed via the hook
path (`PublishAgentsClient.tsx`). The other 6 are imported directly from
`@/lib/customAgentPublishes` by the unit test — kept the 4 hot-path
re-exports, dropped the 6 dead ones + their top-level imports.

## Test plan
- [x] `npx tsc --noEmit` clean
- [x] `bash scripts/ci-lint/00-run-all.sh` green
- [x] Knip hooks/components/contexts/utils unused-exports: 10 → 0
- [x] `tests/unit/hooks/useCustomAgentPublishes.unit.spec.ts` +
`tests/unit/app/agents-manager-publish.unit.spec.tsx` — 16 tests pass

## Follow-ups
- `src/app/**` unused exports (13) — next PR
- `tests/e2e/**` unused exports (6) — small PR
- Promote \`exports\` category to knip hard gate once baseline hits zero

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary
Second B6b pass — covers the 10 unused exports knip reports outside `src/lib/` (excluding `src/app/**` and `tests/**`, which land in later PRs).

None of the 10 exports looked like scaffolded APIs (no corresponding backend endpoint + proxy route pattern like PR #1277's `getRuntime*` / `getOpenClawAgentUsecases`), so no \`@public\` preservation needed.

## Deletes (zero refs)
| File | Removed |
|---|---|
| `components/LocaleLink.tsx` | `useLocalizedPath` hook |
| `utils/admin-helpers.ts` | `getAgentPath` |
| `contexts/AppEnvironmentContext.tsx` | `useAppEnvironment` hook + `useContext` import — the `AppEnvironmentProvider` stays (it writes `window.isNativeApp` / `window.brandInfo` for non-React consumers) but the React hook had zero callers |

## Drop `export` keyword (internal-only)
- `components/billing/SubscriptionPanel.tsx`: `SubscriptionPanelContext` (only read by `useSubscriptionPanel()` + JSX provider in same file)

## Barrel shrink
- `hooks/useCustomAgentPublishes.ts`: the file was re-exporting 10 items from `@/lib/customAgentPublishes` but only 4 are consumed via the hook path (`PublishAgentsClient.tsx`). The other 6 are imported directly from `@/lib/customAgentPublishes` by the unit test — kept the 4 hot-path re-exports, dropped the 6 dead ones + their top-level imports.

## Test plan
- [x] `npx tsc --noEmit` clean
- [x] `bash scripts/ci-lint/00-run-all.sh` green
- [x] Knip hooks/components/contexts/utils unused-exports: 10 → 0
- [x] `tests/unit/hooks/useCustomAgentPublishes.unit.spec.ts` + `tests/unit/app/agents-manager-publish.unit.spec.tsx` — 16 tests pass

## Follow-ups
- `src/app/**` unused exports (13) — next PR
- `tests/e2e/**` unused exports (6) — small PR
- Promote \`exports\` category to knip hard gate once baseline hits zero

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(ios): Add gift code redemption flow (#1283)

- **SHA**: `36849b60610b53b3a515bd81ea8c30512a9b1d20`
- **作者**: bill-srp
- **日期**: 2026-04-24T03:37:19Z
- **PR**: #1283

### Commit Message

```
feat(ios): Add gift code redemption flow (#1283)

## Summary

Add a complete gift code redemption feature to the iOS app, allowing
users to enter and redeem gift codes for bonus credits or subscription
activations.

- **GiftCodeService** — new actor-based service calling `POST
/api/gift-code/redeem` with proper error mapping for all backend error
codes (`invalid_code`, `already_participated`, `code_exhausted`,
`no_subscription`, `plan_downgrade_not_allowed`)
- **RedeemResult** — enum supporting both `.credits(Int)` and
`.subscription(planTier:durationDays:)` responses, forward-compatible
with the unified redeem endpoint from #1270
- **RedeemGiftCodeView** — modal UI with centered text input,
slide-from-bottom animation, loading state, error display, and success
auto-dismiss
- **RedeemSuccessToast** — toast notification with category-aware
messaging (credits vs subscription)
- **Sidebar integration** — redeem button added to sidebar drawer with
gift icon asset
- **NetworkError enhancement** — `httpError` case now carries response
body `Data` so callers can parse structured error responses
- **28 unit tests** — GiftCodeServiceTests (11), RedeemStateTests (3),
RedeemDisabledTests (7), AppShellRedeemWiringTests (3),
RedeemOverlayContractTests (6)

### Version bump: 1.4.0 → 1.5.0 (build 1)

Build number reset from 7 to 1 is intentional. App Store Connect tracks
`CURRENT_PROJECT_VERSION` per `MARKETING_VERSION` — build 1 of 1.5.0
does not conflict with build 7 of 1.4.0. Ref: [Apple
TN3104](https://developer.apple.com/documentation/technotes/tn3104-xcode-build-numbers)

## Test plan

- [ ] Open sidebar, tap "Redeem Gift Code" button
- [ ] Verify modal slides up from bottom with spring animation
- [ ] Enter a valid credit gift code → verify success toast and credits
refresh
- [ ] Enter a valid subscription code → verify subscription activation
toast
- [ ] Enter an invalid code → verify "invalid code" error message
- [ ] Enter an already-used code → verify "already participated" error
- [ ] Enter an exhausted/expired code → verify "redemption limit" error
- [ ] Redeem with a plan higher than the code → verify "plan downgrade"
error
- [ ] Tap backdrop to dismiss modal
- [ ] Verify text input is centered in the code field

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Description

## Summary

Add a complete gift code redemption feature to the iOS app, allowing users to enter and redeem gift codes for bonus credits or subscription activations.

- **GiftCodeService** — new actor-based service calling `POST /api/gift-code/redeem` with proper error mapping for all backend error codes (`invalid_code`, `already_participated`, `code_exhausted`, `no_subscription`, `plan_downgrade_not_allowed`)
- **RedeemResult** — enum supporting both `.credits(Int)` and `.subscription(planTier:durationDays:)` responses, forward-compatible with the unified redeem endpoint from #1270
- **RedeemGiftCodeView** — modal UI with centered text input, slide-from-bottom animation, loading state, error display, and success auto-dismiss
- **RedeemSuccessToast** — toast notification with category-aware messaging (credits vs subscription)
- **Sidebar integration** — redeem button added to sidebar drawer with gift icon asset
- **NetworkError enhancement** — `httpError` case now carries response body `Data` so callers can parse structured error responses
- **28 unit tests** — GiftCodeServiceTests (11), RedeemStateTests (3), RedeemDisabledTests (7), AppShellRedeemWiringTests (3), RedeemOverlayContractTests (6)

### Version bump: 1.4.0 → 1.5.0 (build 1)

Build number reset from 7 to 1 is intentional. App Store Connect tracks `CURRENT_PROJECT_VERSION` per `MARKETING_VERSION` — build 1 of 1.5.0 does not conflict with build 7 of 1.4.0. Ref: [Apple TN3104](https://developer.apple.com/documentation/technotes/tn3104-xcode-build-numbers)

## Test plan

- [ ] Open sidebar, tap "Redeem Gift Code" button
- [ ] Verify modal slides up from bottom with spring animation
- [ ] Enter a valid credit gift code → verify success toast and credits refresh
- [ ] Enter a valid subscription code → verify subscription activation toast
- [ ] Enter an invalid code → verify "invalid code" error message
- [ ] Enter an already-used code → verify "already participated" error
- [ ] Enter an exhausted/expired code → verify "redemption limit" error
- [ ] Redeem with a plan higher than the code → verify "plan downgrade" error
- [ ] Tap backdrop to dismiss modal
- [ ] Verify text input is centered in the code field

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix: add Google service logos (Gmail, Calendar, Drive, Sheets) (#1272)

- **SHA**: `d71ed17f6bf35297fb0c966b3f5b13cc5b18f628`
- **作者**: Leo-srp
- **日期**: 2026-04-24T03:27:11Z
- **PR**: #1272

### Commit Message

```
fix: add Google service logos (Gmail, Calendar, Drive, Sheets) (#1272)

## Summary
Add inline SVG logos for google-mail, google-calendar, google-drive,
google-sheets to ProviderLogo component. Previously showed generic "G"
fallback.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Description

## Summary
Add inline SVG logos for google-mail, google-calendar, google-drive, google-sheets to ProviderLogo component. Previously showed generic "G" fallback.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(web): replace landing hero screenshot with autoplay demo video (#1276)

- **SHA**: `29fcffd7a883d3038d56e752804b552726a81767`
- **作者**: shana-srp
- **日期**: 2026-04-24T02:53:50Z
- **PR**: #1276

### Commit Message

```
feat(web): replace landing hero screenshot with autoplay demo video (#1276)

## Summary
- Replace the static hero product screenshot (`<img>`) with a
muted-autoplay `<video>` (720p, 13.7 MB, hosted on Cloudflare R2),
paired with a circular click-to-unmute button overlay in the
bottom-right corner of the video
- Inline SVG icons (speaker-mute / speaker-on) toggled via `useState`,
consistent with the existing inline-SVG convention in `LandingSecurity`
/ `LandingSpecialists`
- Header now collapses to its pill form on any scroll (threshold 10 px)
instead of only after the user has scrolled past the entire hero section
— matches the scroll-sticky behavior common on Apple / Stripe / Linear
landing pages

## Why
The previous hero image was a static screenshot; a demo video conveys
the product's "proactive AI team" pitch far more effectively. The header
collapse delay was unintuitive — users scrolling even a small amount
expected the sticky pill immediately.

## Test plan
- [x] Verified in Playwright: `autoPlay + muted` triggers autoplay;
click toggles `muted` state and swaps SVG icon
- [x] Verified header transitions: `scrollY <= 10` → full-width bar;
`scrollY > 10` → 920 px pill with `border-radius: 999px`; returns on
scroll back to 0
- [x] Mobile responsive tweaks: mute button shrinks to 40 px at `<768px`
viewport
- [x] A11y: `aria-label` on video + button, `aria-pressed` reflects mute
state, keyboard-focusable via `:focus-visible` outline
- [ ] Sanity-check on real iOS Safari (inline playback + click gesture
unlock)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
2. 官网视频替换，
- 强压缩；3:18 全长，720p，CRF 28 + 保留音轨；~20-30MB；
默认静音自动播放，用户点一下才开声音（行业惯例，Apple/Stripe 都这么做）
- 并修复顶bar显示bug，只要鼠标滚动就缩起
<img width="1280" height="383" alt="image"
src="https://github.com/user-attachments/assets/7c4a4777-d8b7-4c1b-b4a1-a714213cf7de"
/>

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary
- Replace the static hero product screenshot (`<img>`) with a muted-autoplay `<video>` (720p, 13.7 MB, hosted on Cloudflare R2), paired with a circular click-to-unmute button overlay in the bottom-right corner of the video
- Inline SVG icons (speaker-mute / speaker-on) toggled via `useState`, consistent with the existing inline-SVG convention in `LandingSecurity` / `LandingSpecialists`
- Header now collapses to its pill form on any scroll (threshold 10 px) instead of only after the user has scrolled past the entire hero section — matches the scroll-sticky behavior common on Apple / Stripe / Linear landing pages

## Why
The previous hero image was a static screenshot; a demo video conveys the product's "proactive AI team" pitch far more effectively. The header collapse delay was unintuitive — users scrolling even a small amount expected the sticky pill immediately.

## Test plan
- [x] Verified in Playwright: `autoPlay + muted` triggers autoplay; click toggles `muted` state and swaps SVG icon
- [x] Verified header transitions: `scrollY <= 10` → full-width bar; `scrollY > 10` → 920 px pill with `border-radius: 999px`; returns on scroll back to 0
- [x] Mobile responsive tweaks: mute button shrinks to 40 px at `<768px` viewport
- [x] A11y: `aria-label` on video + button, `aria-pressed` reflects mute state, keyboard-focusable via `:focus-visible` outline
- [ ] Sanity-check on real iOS Safari (inline playback + click gesture unlock)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
2. 官网视频替换，
- 强压缩；3:18 全长，720p，CRF 28 + 保留音轨；~20-30MB； 默认静音自动播放，用户点一下才开声音（行业惯例，Apple/Stripe 都这么做）
- 并修复顶bar显示bug，只要鼠标滚动就缩起
<img width="1280" height="383" alt="image" src="https://github.com/user-attachments/assets/7c4a4777-d8b7-4c1b-b4a1-a714213cf7de" />


---

## fix(web): 版本更新弹窗 What's new 跳转独立 changelog 页 (#1262)

- **SHA**: `584221fb6915c9aa51d2f534e0f26705c090b5ae`
- **作者**: lynn Zhuang
- **日期**: 2026-04-24T02:53:05Z
- **PR**: #1262

### Commit Message

```
fix(web): 版本更新弹窗 What's new 跳转独立 changelog 页 (#1262)

## 改动说明
  `VersionUpgradeWidget` 里的 "What's new" 按钮原本跳本地
  `/${locale}/changelog`，改为统一跳到
  `https://zooclaw.ai/tips/changelog`。changelog 已迁至独立的
  [zooclaw-tips](https://github.com/SerendipityOneInc/zooclaw-tips)
  站点维护，内容更新无需再部署主仓。

  ## 净改动
  1 个文件，**+1 / -4**

  | 文件 | 变更 |
  |---|---|
| `web/src/components/VersionUpgradeWidget.tsx` | "What's new" 按钮
onClick
  从拼本地 locale 路径改成直接 `window.open` 外链，加上 `noopener,noreferrer`
  防跨源 tabnabbing |

  ## 测试计划
  - [ ] 版本更新弹窗出现时（chat 页 `versionCheck.needsUpgrade ===
  true`），点击 "What's new" 在新标签页打开
  `https://zooclaw.ai/tips/changelog`
  - [ ] `code-quality / lint-and-test` CI 通过

Co-authored-by: Lynn Zhuang <lynnzhuang@LynndeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

 ## 改动说明
  `VersionUpgradeWidget` 里的 "What's new" 按钮原本跳本地
  `/${locale}/changelog`，改为统一跳到
  `https://zooclaw.ai/tips/changelog`。changelog 已迁至独立的
  [zooclaw-tips](https://github.com/SerendipityOneInc/zooclaw-tips)
  站点维护，内容更新无需再部署主仓。

  ## 净改动
  1 个文件，**+1 / -4**

  | 文件 | 变更 |
  |---|---|
  | `web/src/components/VersionUpgradeWidget.tsx` | "What's new" 按钮 onClick
  从拼本地 locale 路径改成直接 `window.open` 外链，加上 `noopener,noreferrer`
  防跨源 tabnabbing |

  ## 测试计划
  - [ ] 版本更新弹窗出现时（chat 页 `versionCheck.needsUpgrade ===
  true`），点击 "What's new" 在新标签页打开
  `https://zooclaw.ai/tips/changelog`
  - [ ] `code-quality / lint-and-test` CI 通过

