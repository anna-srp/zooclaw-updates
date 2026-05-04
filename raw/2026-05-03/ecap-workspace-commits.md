# ecap-workspace - 2026-05-03

共 4 条 commits

---

## [70c4943c] chore(web): rename lib/sentry/ 10 个 camelCase 文件 → kebab-case (#1555)

- **SHA**: `70c4943c7bd6f2a4fcfd415b94aaf3ab6b7b252c`

- **作者**: Chris@ZooClaw

- **日期**: 2026-05-03T11:21:34Z

- **PR**: #1555


### 完整 Commit Message

```
chore(web): rename lib/sentry/ 10 个 camelCase 文件 → kebab-case (#1555)

## Summary
按 PR #1547 引入的 filename-naming 规则把 \`src/lib/sentry/\` 全部 10 个 camelCase
文件改成 kebab-case。这是 baseline 中**最大单批**（10 文件 / ~95 处 import）。

## 改名清单
| 旧名 | 新名 |
|---|---|
| adminMonitor.ts | admin-monitor.ts |
| agentMonitor.ts | agent-monitor.ts |
| chatMonitor.ts | chat-monitor.ts |
| feedbackService.ts | feedback-service.ts |
| healthMonitor.ts | health-monitor.ts |
| mattermostMonitor.ts | mattermost-monitor.ts |
| networkMonitor.ts | network-monitor.ts |
| openclawMonitor.ts | openclaw-monitor.ts |
| paymentMonitor.ts | payment-monitor.ts |
| userIdentity.ts | user-identity.ts |

## 改动
- 7 个 dedicated test 文件同步 rename（5 在 \`tests/unit/lib/sentry/\`，2 在
\`tests/unit/sentry/\`）
- sed 批量替换 95 处 import 路径，audit 残留仅 describe 标签字符串（不影响运行）
- \`eslint.config.mjs\`：SHRINK-ONLY 块删 10 行 + complexity 白名单同步
openclawMonitor → openclaw-monitor
- SHRINK-ONLY baseline: **48 → 38** entries（减 10）

## W1-lib-pure 检查
\`grep "^import" src/lib/sentry/*.ts | grep "@/(components|app)"\`
输出为空——sentry 子目录无任何反向依赖，搬迁安全。

## Test plan
- [x] \`pnpm lint\` exit 0
- [x] \`pnpm exec tsc --noEmit\` exit 0
- [x] \`pnpm lint:imports\` exit 0（dep-cruiser 0 errors）
- [x] \`bash web/scripts/check-filename-shrink-only.sh\` — main: 48,
HEAD: 38 ✅
- [x] sentry 全部 8 个 test files 61 tests 通过
- [ ] CI \`code-quality / lint-and-test\` 通过

## 与并行 PR 关系
- PR #1554 (lib/api/ rename) 已 mergeable 等手动 merge
- 两个 PR baseline 删的行不重叠（lib/api 4 行 vs lib/sentry 10 行），git auto-merge

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```


### PR Body (#1555): chore(web): rename lib/sentry/ 10 个 camelCase 文件 → kebab-case

## Summary
按 PR #1547 引入的 filename-naming 规则把 \`src/lib/sentry/\` 全部 10 个 camelCase 文件改成 kebab-case。这是 baseline 中**最大单批**（10 文件 / ~95 处 import）。

## 改名清单
| 旧名 | 新名 |
|---|---|
| adminMonitor.ts | admin-monitor.ts |
| agentMonitor.ts | agent-monitor.ts |
| chatMonitor.ts | chat-monitor.ts |
| feedbackService.ts | feedback-service.ts |
| healthMonitor.ts | health-monitor.ts |
| mattermostMonitor.ts | mattermost-monitor.ts |
| networkMonitor.ts | network-monitor.ts |
| openclawMonitor.ts | openclaw-monitor.ts |
| paymentMonitor.ts | payment-monitor.ts |
| userIdentity.ts | user-identity.ts |

## 改动
- 7 个 dedicated test 文件同步 rename（5 在 \`tests/unit/lib/sentry/\`，2 在 \`tests/unit/sentry/\`）
- sed 批量替换 95 处 import 路径，audit 残留仅 describe 标签字符串（不影响运行）
- \`eslint.config.mjs\`：SHRINK-ONLY 块删 10 行 + complexity 白名单同步 openclawMonitor → openclaw-monitor
- SHRINK-ONLY baseline: **48 → 38** entries（减 10）

## W1-lib-pure 检查
\`grep "^import" src/lib/sentry/*.ts | grep "@/(components|app)"\` 输出为空——sentry 子目录无任何反向依赖，搬迁安全。

## Test plan
- [x] \`pnpm lint\` exit 0
- [x] \`pnpm exec tsc --noEmit\` exit 0
- [x] \`pnpm lint:imports\` exit 0（dep-cruiser 0 errors）
- [x] \`bash web/scripts/check-filename-shrink-only.sh\` — main: 48, HEAD: 38 ✅
- [x] sentry 全部 8 个 test files 61 tests 通过
- [ ] CI \`code-quality / lint-and-test\` 通过

## 与并行 PR 关系
- PR #1554 (lib/api/ rename) 已 mergeable 等手动 merge
- 两个 PR baseline 删的行不重叠（lib/api 4 行 vs lib/sentry 10 行），git auto-merge

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## [eb3fa4b4] chore(web): move 5 components/.ts utils into src/lib/ (kebab-case) (#1551)

- **SHA**: `eb3fa4b443a7178e81590ef86dc60e2f36875501`

- **作者**: Chris@ZooClaw

- **日期**: 2026-05-03T08:48:02Z

- **PR**: #1551


### 完整 Commit Message

```
chore(web): move 5 components/.ts utils into src/lib/ (kebab-case) (#1551)

## Summary
按"src/lib/ 装工具函数 + src/components/ 只装 .tsx 组件"的分层惯例，把 src/components/ 下
5 个 .ts 工具文件移入 src/lib/，同时改成 kebab-case（PR #1547 的命名规则）。SHRINK-ONLY
baseline **53 → 48** entries（减 5）。

## 迁移列表
| 源（components/） | 目的地（lib/） |
|---|---|
| `markdown/extractQuotedLabels.ts` |
`markdown/extract-quoted-labels.ts` |
| `markdown/renderMarkdownToHtml.ts` |
`markdown/render-markdown-to-html.ts` |
| `navLabelUtils.ts` | `nav-label-utils.ts` |
| `onboarding/onboardingProgress.ts` |
`onboarding/onboarding-progress.ts` |
| `richTextUtils.ts` | `rich-text-utils.ts` |

5 个 test 文件同步迁移到 `tests/unit/lib/` 镜像目录。

## 改动
- 11 处 import 路径更新（含 `MarkdownContent.tsx` 1 处 dynamic import）
- 2 处 `import './onboardingProgress'` / `'./richTextUtils'` 相对路径改成
`@/lib/...` 绝对路径
- `eslint.config.mjs` SHRINK-ONLY 块删 5 行
- 4 个文件经 `eslint --fix` 自动 simple-import-sort 调整顺序

## Test plan
- [x] \`pnpm lint\` exit 0
- [x] \`pnpm exec tsc --noEmit\` exit 0
- [x] \`bash web/scripts/check-filename-shrink-only.sh\` — main: 53,
HEAD: 48 ✅
- [x] \`pnpm exec vitest run tests/unit/lib/markdown/
tests/unit/lib/nav-label-utils.unit.spec.ts
tests/unit/lib/onboarding/onboarding-progress.unit.spec.ts
tests/unit/lib/rich-text-utils.unit.spec.ts\` — 101/101 通过
- [ ] CI \`code-quality / lint-and-test\` 通过

## 设计决策记录
PR-1 时我自己定的规则是 components/**/*.ts → kebab-case。但用户在 review PR-4 时点明：放在
components/ 目录下的 .ts 工具文件本身就有歧义——按惯例工具应住 lib/。所以这个 PR 不只 rename
还做了**目录搬迁**，让命名和目录语义对齐。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```


### PR Body (#1551): chore(web): move 5 components/.ts utils into src/lib/ (kebab-case)

## Summary
按"src/lib/ 装工具函数 + src/components/ 只装 .tsx 组件"的分层惯例，把 src/components/ 下 5 个 .ts 工具文件移入 src/lib/，同时改成 kebab-case（PR #1547 的命名规则）。SHRINK-ONLY baseline **53 → 48** entries（减 5）。

## 迁移列表
| 源（components/） | 目的地（lib/） |
|---|---|
| `markdown/extractQuotedLabels.ts` | `markdown/extract-quoted-labels.ts` |
| `markdown/renderMarkdownToHtml.ts` | `markdown/render-markdown-to-html.ts` |
| `navLabelUtils.ts` | `nav-label-utils.ts` |
| `onboarding/onboardingProgress.ts` | `onboarding/onboarding-progress.ts` |
| `richTextUtils.ts` | `rich-text-utils.ts` |

5 个 test 文件同步迁移到 `tests/unit/lib/` 镜像目录。

## 改动
- 11 处 import 路径更新（含 `MarkdownContent.tsx` 1 处 dynamic import）
- 2 处 `import './onboardingProgress'` / `'./richTextUtils'` 相对路径改成 `@/lib/...` 绝对路径
- `eslint.config.mjs` SHRINK-ONLY 块删 5 行
- 4 个文件经 `eslint --fix` 自动 simple-import-sort 调整顺序

## Test plan
- [x] \`pnpm lint\` exit 0
- [x] \`pnpm exec tsc --noEmit\` exit 0
- [x] \`bash web/scripts/check-filename-shrink-only.sh\` — main: 53, HEAD: 48 ✅
- [x] \`pnpm exec vitest run tests/unit/lib/markdown/ tests/unit/lib/nav-label-utils.unit.spec.ts tests/unit/lib/onboarding/onboarding-progress.unit.spec.ts tests/unit/lib/rich-text-utils.unit.spec.ts\` — 101/101 通过
- [ ] CI \`code-quality / lint-and-test\` 通过

## 设计决策记录
PR-1 时我自己定的规则是 components/**/*.ts → kebab-case。但用户在 review PR-4 时点明：放在 components/ 目录下的 .ts 工具文件本身就有歧义——按惯例工具应住 lib/。所以这个 PR 不只 rename 还做了**目录搬迁**，让命名和目录语义对齐。

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## [22bde751] refactor(web): relocate ReplayContext from components/replay/ to contexts/ (#1552)

- **SHA**: `22bde751a733945c9255330c6e0289d6cb7c2df3`

- **作者**: Chris@ZooClaw

- **日期**: 2026-05-03T08:47:05Z

- **PR**: #1552


### 完整 Commit Message

```
refactor(web): relocate ReplayContext from components/replay/ to contexts/ (#1552)

## Summary
- 把 \`ReplayContext.tsx\` (38 行,Context+Provider+hooks 三件套同文件,无业务逻辑) 从
\`web/src/components/replay/\` 整体迁到 \`web/src/contexts/\`
- 4 处 import 改写,不留 re-export shim
- \`components/replay/\` 保留 \`ReplayLightbox.tsx\` +
\`useReplayPlayer.ts\`(replay feature 实现)

## Why
ReplayContext 形态完全匹配 \`contexts/\` 三件套先例(\`AppEnvironmentContext\` /
\`LanguageContext\` / \`UserBusinessDataContext\`):Context + Provider +
hooks 同文件、纯状态穿透、无业务逻辑。位置归类原则(由 PR #1550 spec 建立):

- **\`providers/\`**: 业务编排 Provider(注入 firebase auth、Mattermost
session、subscription 等)
- **\`contexts/\`**: 纯状态穿透(只透传 \`readOnly\` + \`shareId\`)

ReplayContext 属后者。

## Spec

[\`docs/superpowers/specs/2026-05-02-replay-context-relocation.md\`](../blob/feature/replay-context-move/docs/superpowers/specs/2026-05-02-replay-context-relocation.md)
— Follow-up to #1550.

## Test plan
- [x] \`npx tsc --noEmit\` 全仓 0 错误
- [x] \`pnpm lint:imports\` 0 errors(2 W5 warn 同 base,与本 PR 无关)
- [x] \`pnpm lint\` 0 errors(import sort auto-fix)
- [x] \`pnpm test:unit\` 4391 passed / 4393(1 failure 同 base 已存在的
\`MarkdownContent\` specialist-card hydration flake,与本 PR 无关)

## Out of scope
- 不动 \`components/replay/ReplayLightbox.tsx\` / \`useReplayPlayer.ts\`
- 不引入 dep-cruiser 新规则强制 contexts/ 命名

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```


### PR Body (#1552): refactor(web): relocate ReplayContext from components/replay/ to contexts/

## Summary
- 把 \`ReplayContext.tsx\` (38 行,Context+Provider+hooks 三件套同文件,无业务逻辑) 从 \`web/src/components/replay/\` 整体迁到 \`web/src/contexts/\`
- 4 处 import 改写,不留 re-export shim
- \`components/replay/\` 保留 \`ReplayLightbox.tsx\` + \`useReplayPlayer.ts\`(replay feature 实现)

## Why
ReplayContext 形态完全匹配 \`contexts/\` 三件套先例(\`AppEnvironmentContext\` / \`LanguageContext\` / \`UserBusinessDataContext\`):Context + Provider + hooks 同文件、纯状态穿透、无业务逻辑。位置归类原则(由 PR #1550 spec 建立):

- **\`providers/\`**: 业务编排 Provider(注入 firebase auth、Mattermost session、subscription 等)
- **\`contexts/\`**: 纯状态穿透(只透传 \`readOnly\` + \`shareId\`)

ReplayContext 属后者。

## Spec
[\`docs/superpowers/specs/2026-05-02-replay-context-relocation.md\`](../blob/feature/replay-context-move/docs/superpowers/specs/2026-05-02-replay-context-relocation.md) — Follow-up to #1550.

## Test plan
- [x] \`npx tsc --noEmit\` 全仓 0 错误
- [x] \`pnpm lint:imports\` 0 errors(2 W5 warn 同 base,与本 PR 无关)
- [x] \`pnpm lint\` 0 errors(import sort auto-fix)
- [x] \`pnpm test:unit\` 4391 passed / 4393(1 failure 同 base 已存在的 \`MarkdownContent\` specialist-card hydration flake,与本 PR 无关)

## Out of scope
- 不动 \`components/replay/ReplayLightbox.tsx\` / \`useReplayPlayer.ts\`
- 不引入 dep-cruiser 新规则强制 contexts/ 命名

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## [79be0173] refactor(web): consolidate *Provider components into components/providers/ (#1550)

- **SHA**: `79be0173223ea29cc4c6ce53fdf44c8d0987a14f`

- **作者**: Chris@ZooClaw

- **日期**: 2026-05-03T01:35:07Z

- **PR**: #1550


### 完整 Commit Message

```
refactor(web): consolidate *Provider components into components/providers/ (#1550)

## Summary
- 8 个 \`*Provider.tsx\` 从 \`components/\` 顶层(及 \`Feedback/\` /
\`onboarding/\` 子目录)迁到 \`components/providers/\` 子目录
- 25 处 import 改写(15 处 \`src/\` + 10 处 \`tests/\`),不留 re-export shim
- Provider 内部逻辑未动;\`contexts/\` 内 7 个 Context 定义未动

## Spec

[\`docs/superpowers/specs/2026-05-02-web-layered-structure-audit.md\`](../blob/feature/structure/docs/superpowers/specs/2026-05-02-web-layered-structure-audit.md)
— 含现状对照表、偏差分级、显式列出"不做的事"。

## Test plan
- [x] \`npx tsc --noEmit\` 全仓 0 错误
- [x] \`pnpm lint:imports\` 0 errors(2 W5 warn 在 base 已存在,与本 PR
无关:\`assets→chat\`)
- [x] \`pnpm test:unit\` 4387 passed / 4389(2 failures 与本 PR
无关:\`MarkdownContent\` specialist-card hydration 在 base
已失败;\`AdminClient\` flaky,单跑通过)
- [x] \`web/src/components/\` 顶层 \`*Provider.tsx\` 计数 0
- [x] \`ClientLayout.tsx\` Provider 嵌套顺序未动(reviewer 必检 L86-100 JSX 结构)

## Out of scope
- \`ReplayContext.tsx\` — Context+Provider+hooks 混合形态,P1 合并后另起 mini-spec
决定整体迁 \`contexts/\` 还是拆三处
- 新增 dep-cruiser W7 规则强制 Provider 位置 — 主观加严,按 spec 第 4 节不做

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```


### PR Body (#1550): refactor(web): consolidate *Provider components into components/providers/

## Summary
- 8 个 \`*Provider.tsx\` 从 \`components/\` 顶层(及 \`Feedback/\` / \`onboarding/\` 子目录)迁到 \`components/providers/\` 子目录
- 25 处 import 改写(15 处 \`src/\` + 10 处 \`tests/\`),不留 re-export shim
- Provider 内部逻辑未动;\`contexts/\` 内 7 个 Context 定义未动

## Spec
[\`docs/superpowers/specs/2026-05-02-web-layered-structure-audit.md\`](../blob/feature/structure/docs/superpowers/specs/2026-05-02-web-layered-structure-audit.md) — 含现状对照表、偏差分级、显式列出"不做的事"。

## Test plan
- [x] \`npx tsc --noEmit\` 全仓 0 错误
- [x] \`pnpm lint:imports\` 0 errors(2 W5 warn 在 base 已存在,与本 PR 无关:\`assets→chat\`)
- [x] \`pnpm test:unit\` 4387 passed / 4389(2 failures 与本 PR 无关:\`MarkdownContent\` specialist-card hydration 在 base 已失败;\`AdminClient\` flaky,单跑通过)
- [x] \`web/src/components/\` 顶层 \`*Provider.tsx\` 计数 0
- [x] \`ClientLayout.tsx\` Provider 嵌套顺序未动(reviewer 必检 L86-100 JSX 结构)

## Out of scope
- \`ReplayContext.tsx\` — Context+Provider+hooks 混合形态,P1 合并后另起 mini-spec 决定整体迁 \`contexts/\` 还是拆三处
- 新增 dep-cruiser W7 规则强制 Provider 位置 — 主观加严,按 spec 第 4 节不做

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
