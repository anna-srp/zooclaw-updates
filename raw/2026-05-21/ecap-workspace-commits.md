# ecap-workspace Commits — 2026-05-21

## b7f5aee9 — refactor(chat): split GenClawClient to clear legacy-complexity override (ECA-776) (#1841)

- **Author**: Chris@ZooClaw
- **Date**: 2026-05-21T19:10:18Z

### Full Commit Message

```
refactor(chat): split GenClawClient to clear legacy-complexity override (ECA-776) (#1841)

## Summary
Closes
[ECA-776](https://linear.app/srpone/issue/ECA-776/refactorchat-finish-genclawclient-split-to-remove-from-legacy).

- Removes `src/app/[locale]/chat/GenClawClient.tsx` from the
legacy-complexity override in `web/app/eslint.config.mjs`. The file now
satisfies the **unmodified** global limits (`max-lines:500`,
`max-lines-per-function:300`, `complexity:25`, `max-depth:5`,
`max-params:4`, `max-nested-callbacks:4`).
- Refactors GenClawClient.tsx by extracting JSX composition + state
derivations into focused components and hooks. File drops from **919 →
394** raw lines (well under 500). Main function complexity drops from
**66 → <25**.
- **No global lint policy changes.** Earlier revisions of this PR also
raised `max-lines:500→800` repo-wide; reverted in commit `86a1e200` per
Codex review — the extraction alone is enough, the global bump wasn't
load-bearing.

## Extractions
Seven new components and three new hooks under `src/app/[locale]/chat/`:

| New | Role |
|---|---|
| `components/ChatGateStates.tsx` (function `renderChatGateStates`) | 6
gate-state branches (expired / onboarding / mm-failed / init-error /
init-pending / ws-recovery). Returns `ReactElement \| null` so
`{contentOverride ?? <ChatBody />}` semantics carry through. |
| `components/ChatModals.tsx` | Redeploy confirm + image preview +
connection error + feature launch modal cluster. |
| `components/ChatHeader.tsx` | `ClawPageHeader` + degradation banner +
version widget + init banner. Avatar variant chain absorbed by a
`ChatHeaderAvatar` sub-component. |
| `components/ChatBody.tsx` | `ShareSelectionProvider` /
`AssistantRuntimeProvider` chain, share dialog, share selection bar,
subagent rail, composer. |
| `components/ChatSidePanels.tsx` | Agent settings popover + subagent
chat panel + artifacts sidebar + resources panel. |
| `components/ChatDragDropContainer.tsx` | Page wrapper + drag handlers
+ drop overlay. Owns its own drag state. |
| `components/ChatAuthLoadingScreen.tsx` | Auth-loading early-return UI.
|
| `components/ClawSpinner.tsx` | Shared 4-dot loading indicator. Used by
ChatGateStates + ChatAuthLoadingScreen. |
| `hooks/useChatLifecycle.ts` | `doRedeploy` / `handleRecreate`
choreography. |
| `hooks/useChatPageDerivations.ts` | `agentId` / `sessionKey` /
`activeAgent` derivations. Lifted ~12 cyclomatic points out of main fn.
|
| `hooks/useChatRestartCycle.ts` | Per-agent pending-restart
bookkeeping. |

## Notable behavior preservation
- `<ChatGateStates>` is called as `renderChatGateStates({...})`
(function, not JSX) because the original `renderContent()` returned
`ReactNode \| null` and the downstream `{!contentOverride && <chat>}` /
`{contentOverride ?? <ChatBody>}` semantics depended on `null` meaning
"fall through". A JSX element is always truthy.
- Redeploy confirm modal moved to a `RedeployConfirmModal` sub-component
within `ChatModals` — kept inline rather than reusing `ConfirmModal` to
preserve the AdvancedRecreate footer.
- Mattermost `<MaybeMMAuthProvider>` helper moved into `ChatBody` (only
consumer).
- Each `data-testid` (e.g. `genclaw-subscription-expired-renew`,
`genclaw-init-banner`, `genclaw-chat-container`, `genclaw-loading`)
preserved byte-for-byte.

## Test plumbing
`tests/unit/app/chat/GenClawClient.internals.unit.spec.tsx` —
`useChatReplayShare` mock now provides the full `actions` shape (was `{
state: {} }`). `<ChatHeader>` reads `shareFlow.actions.enter`
unconditionally as a prop value, so the previous JSX-`&&`-guarded access
pattern no longer protects the mock.

`src/components/ImagePreview.tsx` — exports `GalleryImage` so
`<ChatModals>` can type `imagePreview.images` accurately. No runtime
change.

## Test plan
- [x] `pnpm exec eslint src/app/[locale]/chat/GenClawClient.tsx` —
clean, no override
- [x] `pnpm exec vitest run tests/unit/app/chat/` — 530/530 pass
- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `web/scripts/check-{filename,ignores,svg-ignores}-shrink-only.sh`
— pass
- [ ] Manual staging smoke (per ECA-776 acceptance):
  - [ ] expired sub → dormant CTA
  - [ ] MM-disconnected w/ cache → cached chat renders, input disabled
  - [ ] init-pending w/ cache → cached chat renders, banner shows
  - [ ] init-error → retry/redeploy/AdvancedRecreate buttons work

## PR size
~2100 lines, over the 2000 default budget. Bulk is code **relocation**
(~700 lines moved from GenClawClient into the new files), not net new
logic. `size-override` label applied per session discussion — splitting
would leave issue acceptance only partially satisfied at the
intermediate PR.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary
Closes [ECA-776](https://linear.app/srpone/issue/ECA-776/refactorchat-finish-genclawclient-split-to-remove-from-legacy).

- Removes `src/app/[locale]/chat/GenClawClient.tsx` from the legacy-complexity override in `web/app/eslint.config.mjs`. The file now satisfies the **unmodified** global limits (`max-lines:500`, `max-lines-per-function:300`, `complexity:25`, `max-depth:5`, `max-params:4`, `max-nested-callbacks:4`).
- Refactors GenClawClient.tsx by extracting JSX composition + state derivations into focused components and hooks. File drops from **919 → 394** raw lines (well under 500). Main function complexity drops from **66 → <25**.
- **No global lint policy changes.** Earlier revisions of this PR also raised `max-lines:500→800` repo-wide; reverted in commit `86a1e200` per Codex review — the extraction alone is enough, the global bump wasn't load-bearing.

## Extractions
Seven new components and three new hooks under `src/app/[locale]/chat/`:

| New | Role |
|---|---|
| `components/ChatGateStates.tsx` (function `renderChatGateStates`) | 6 gate-state branches (expired / onboarding / mm-failed / init-error / init-pending / ws-recovery). Returns `ReactElement \| null` so `{contentOverride ?? <ChatBody />}` semantics carry through. |
| `components/ChatModals.tsx` | Redeploy confirm + image preview + connection error + feature launch modal cluster. |
| `components/ChatHeader.tsx` | `ClawPageHeader` + degradation banner + version widget + init banner. Avatar variant chain absorbed by a `ChatHeaderAvatar` sub-component. |
| `components/ChatBody.tsx` | `ShareSelectionProvider` / `AssistantRuntimeProvider` chain, share dialog, share selection bar, subagent rail, composer. |
| `components/ChatSidePanels.tsx` | Agent settings popover + subagent chat panel + artifacts sidebar + resources panel. |
| `components/ChatDragDropContainer.tsx` | Page wrapper + drag handlers + drop overlay. Owns its own drag state. |
| `components/ChatAuthLoadingScreen.tsx` | Auth-loading early-return UI. |
| `components/ClawSpinner.tsx` | Shared 4-dot loading indicator. Used by ChatGateStates + ChatAuthLoadingScreen. |
| `hooks/useChatLifecycle.ts` | `doRedeploy` / `handleRecreate` choreography. |
| `hooks/useChatPageDerivations.ts` | `agentId` / `sessionKey` / `activeAgent` derivations. Lifted ~12 cyclomatic points out of main fn. |
| `hooks/useChatRestartCycle.ts` | Per-agent pending-restart bookkeeping. |

## Notable behavior preservation
- `<ChatGateStates>` is called as `renderChatGateStates({...})` (function, not JSX) because the original `renderContent()` returned `ReactNode \| null` and the downstream `{!contentOverride && <chat>}` / `{contentOverride ?? <ChatBody>}` semantics depended on `null` meaning "fall through". A JSX element is always truthy.
- Redeploy confirm modal moved to a `RedeployConfirmModal` sub-component within `ChatModals` — kept inline rather than reusing `ConfirmModal` to preserve the AdvancedRecreate footer.
- Mattermost `<MaybeMMAuthProvider>` helper moved into `ChatBody` (only consumer).
- Each `data-testid` (e.g. `genclaw-subscription-expired-renew`, `genclaw-init-banner`, `genclaw-chat-container`, `genclaw-loading`) preserved byte-for-byte.

## Test plumbing
`tests/unit/app/chat/GenClawClient.internals.unit.spec.tsx` — `useChatReplayShare` mock now provides the full `actions` shape (was `{ state: {} }`). `<ChatHeader>` reads `shareFlow.actions.enter` unconditionally as a prop value, so the previous JSX-`&&`-guarded access pattern no longer protects the mock.

`src/components/ImagePreview.tsx` — exports `GalleryImage` so `<ChatModals>` can type `imagePreview.images` accurately. No runtime change.

## Test plan
- [x] `pnpm exec eslint src/app/[locale]/chat/GenClawClient.tsx` — clean, no override
- [x] `pnpm exec vitest run tests/unit/app/chat/` — 530/530 pass
- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `web/scripts/check-{filename,ignores,svg-ignores}-shrink-only.sh` — pass
- [ ] Manual staging smoke (per ECA-776 acceptance):
  - [ ] expired sub → dormant CTA
  - [ ] MM-disconnected w/ cache → cached chat renders, input disabled
  - [ ] init-pending w/ cache → cached chat renders, banner shows
  - [ ] init-error → retry/redeploy/AdvancedRecreate buttons work

## PR size
~2100 lines, over the 2000 default budget. Bulk is code **relocation** (~700 lines moved from GenClawClient into the new files), not net new logic. `size-override` label applied per session discussion — splitting would leave issue acceptance only partially satisfied at the intermediate PR.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## a5120232 — ci(codeql): switch to advanced setup, exclude Python PII heuristics (#1839)

- **Author**: Chris@ZooClaw
- **Date**: 2026-05-21T19:05:07Z

### Full Commit Message

```
ci(codeql): switch to advanced setup, exclude Python PII heuristics (#1839)

## Summary

切换 CodeQL 从 GitHub default code scanning setup 到 advanced setup，给 Python
扫描挂自定义 config 排除一条与本仓库 ID 日志策略冲突的启发式规则：

- `py/clear-text-logging-sensitive-data`

这条规则按变量名启发式（`*id*` flow into log call）把 `uid` / `team_id` / `bot_id` 当
PII，但本仓库政策（`services/claw-interface/AGENTS.md` "Log Sanitization (CodeQL
boundary)" 段）明确允许完整记录这类内部 ID。

**不动** `py/weak-sensitive-data-hashing`：历史仅 2 条 dismiss，规则也能抓 MD5 +
secret 的真问题（基于 Codex review 反馈调整）。

## Why now

- **历史 dismiss 工作量**：80 / 84（95%）已 dismiss 的 CodeQL alert 都是
`py/clear-text-logging-sensitive-data` 一条
- **当前 OPEN**：9 条 alert，全部在
`services/claw-interface/app/services/`，全部是同一条规则
- **兜底成本**：团队为绕过这条启发式维护了 78 文件 / 630+ 处 `_SafeId` 包装层
- Default setup **不支持** rule-filter，要做这事必须用 advanced workflow 接管 CodeQL
扫描
- Default vs advanced 在 GitHub 端是仓库级 binary 互斥（不是 per-language），所以
advanced workflow 必须接管 default 在扫的全部语言

Linear: https://linear.app/srpone/issue/ECA-693

## What changed

- `.github/workflows/codeql.yml`（新）— Advanced setup workflow，matrix
`[actions, python, ruby]`（沿用 default 之前扫的语言）；仅 python 行通过 matrix
`include:` 挂 config-file，actions / ruby 跑默认套件
- `.github/codeql/codeql-config-python.yml`（新）— Python 专用 query-filters
排除一条规则
- `services/claw-interface/AGENTS.md` — "Log Sanitization (CodeQL
boundary)" 段重写：`_SafeId` 改述为"防御性风格保留，不再是规则强制"

## ✅ Admin step (已完成)

为了让 advanced setup 能上传 SARIF，必须完全关闭 GitHub default code scanning
setup（PATCH `state=not-configured`）。**该步骤本作者已经预先执行**（v4 commit 之前），可以验证：

```bash
gh api /repos/SerendipityOneInc/ecap-workspace/code-scanning/default-setup | jq .state
# 期望："not-configured"
```

合入后 advanced workflow 接管所有 CodeQL 扫描；不需要进一步 admin 操作。

可选清理：批量 dismiss 现有 9 条 OPEN `py/clear-text-logging-sensitive-data`
alert（rule 已排除，新扫描不会再 fire，但旧 alert 会悬挂在 UI 直到 manual close）。

## 🔄 关于 Codex NEED_HUMAN_REVIEW

Codex 4 轮 review 一直 flag NEED_HUMAN_REVIEW，关切点：
- 仓库级排除 `py/clear-text-logging-sensitive-data` 也会让未来这条规则的真阳性被悄无声息地吞掉

这是 ECA-693 issue 的**预期 trade-off**（issue 显式说"safe_short_id 截断是过度保守"），而且
80/84 历史 dismiss 已经证明这条规则在本仓库的误报率 95%+。真 secret（API key / token /
密码）的检测覆盖由 `py/hardcoded-credentials`、GitHub secret-scanning + push
protection、Codex / Claude 自动 code review 兜底。

NEED_HUMAN_REVIEW 不 block merge（codex-review check pass）。

## Test plan

- [x] 所有 CI check pass（包括 advanced workflow 的 Analyze actions / python /
ruby）
- [ ] Merge 后 `gh api .../code-scanning/alerts?state=open | jq
'[.[]|select(.rule.id=="py/clear-text-logging-sensitive-data")] |
length'` 应为 0
- [ ] code-quality / lint-and-test 工作流不受影响

## Risk

- **真 secret 漏报场景失去这条规则保护**：依赖 `py/hardcoded-credentials`、GitHub
secret-scanning + push protection、Codex/Claude code review 兜底。整体覆盖可接受
- **default setup 已关，回退方式**：若需回退，PATCH default-setup `state=configured`
+ `languages=[actions, python, ruby]` 即可

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

切换 CodeQL 从 GitHub default code scanning setup 到 advanced setup，给 Python 扫描挂自定义 config 排除一条与本仓库 ID 日志策略冲突的启发式规则：

- `py/clear-text-logging-sensitive-data`

这条规则按变量名启发式（`*id*` flow into log call）把 `uid` / `team_id` / `bot_id` 当 PII，但本仓库政策（`services/claw-interface/AGENTS.md` "Log Sanitization (CodeQL boundary)" 段）明确允许完整记录这类内部 ID。

**不动** `py/weak-sensitive-data-hashing`：历史仅 2 条 dismiss，规则也能抓 MD5 + secret 的真问题（基于 Codex review 反馈调整）。

## Why now

- **历史 dismiss 工作量**：80 / 84（95%）已 dismiss 的 CodeQL alert 都是 `py/clear-text-logging-sensitive-data` 一条
- **当前 OPEN**：9 条 alert，全部在 `services/claw-interface/app/services/`，全部是同一条规则
- **兜底成本**：团队为绕过这条启发式维护了 78 文件 / 630+ 处 `_SafeId` 包装层
- Default setup **不支持** rule-filter，要做这事必须用 advanced workflow 接管 CodeQL 扫描
- Default vs advanced 在 GitHub 端是仓库级 binary 互斥（不是 per-language），所以 advanced workflow 必须接管 default 在扫的全部语言

Linear: https://linear.app/srpone/issue/ECA-693

## What changed

- `.github/workflows/codeql.yml`（新）— Advanced setup workflow，matrix `[actions, python, ruby]`（沿用 default 之前扫的语言）；仅 python 行通过 matrix `include:` 挂 config-file，actions / ruby 跑默认套件
- `.github/codeql/codeql-config-python.yml`（新）— Python 专用 query-filters 排除一条规则
- `services/claw-interface/AGENTS.md` — "Log Sanitization (CodeQL boundary)" 段重写：`_SafeId` 改述为"防御性风格保留，不再是规则强制"

## ✅ Admin step (已完成)

为了让 advanced setup 能上传 SARIF，必须完全关闭 GitHub default code scanning setup（PATCH `state=not-configured`）。**该步骤本作者已经预先执行**（v4 commit 之前），可以验证：

```bash
gh api /repos/SerendipityOneInc/ecap-workspace/code-scanning/default-setup | jq .state
# 期望："not-configured"
```

合入后 advanced workflow 接管所有 CodeQL 扫描；不需要进一步 admin 操作。

可选清理：批量 dismiss 现有 9 条 OPEN `py/clear-text-logging-sensitive-data` alert（rule 已排除，新扫描不会再 fire，但旧 alert 会悬挂在 UI 直到 manual close）。

## 🔄 关于 Codex NEED_HUMAN_REVIEW

Codex 4 轮 review 一直 flag NEED_HUMAN_REVIEW，关切点：
- 仓库级排除 `py/clear-text-logging-sensitive-data` 也会让未来这条规则的真阳性被悄无声息地吞掉

这是 ECA-693 issue 的**预期 trade-off**（issue 显式说"safe_short_id 截断是过度保守"），而且 80/84 历史 dismiss 已经证明这条规则在本仓库的误报率 95%+。真 secret（API key / token / 密码）的检测覆盖由 `py/hardcoded-credentials`、GitHub secret-scanning + push protection、Codex / Claude 自动 code review 兜底。

NEED_HUMAN_REVIEW 不 block merge（codex-review check pass）。

## Test plan

- [x] 所有 CI check pass（包括 advanced workflow 的 Analyze actions / python / ruby）
- [ ] Merge 后 `gh api .../code-scanning/alerts?state=open | jq '[.[]|select(.rule.id=="py/clear-text-logging-sensitive-data")] | length'` 应为 0
- [ ] code-quality / lint-and-test 工作流不受影响

## Risk

- **真 secret 漏报场景失去这条规则保护**：依赖 `py/hardcoded-credentials`、GitHub secret-scanning + push protection、Codex/Claude code review 兜底。整体覆盖可接受
- **default setup 已关，回退方式**：若需回退，PATCH default-setup `state=configured` + `languages=[actions, python, ruby]` 即可

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 9fb56c8c — fix(chat): support HEIC image upload previews (#1838)

- **Author**: Chris@ZooClaw
- **Date**: 2026-05-21T18:48:00Z

### Full Commit Message

```
fix(chat): support HEIC image upload previews (#1838)

## Summary
- Convert HEIC/HEIF uploads to JPEG before R2 and Mattermost upload
handling.
- Avoid rendering raw HEIC blobs as pending Mattermost previews, then
swap to the converted JPEG preview.
- Return the actual uploaded File from R2 uploads so chat asset metadata
records post-conversion name/type/size.
- Add regression coverage for the converter helper, R2 upload path,
Mattermost upload path, and chat asset metadata recording.

## Review-driven fixes
- Keep HEIC conversion inside the R2 upload error boundary so conversion
failures return a structured UploadResult error.
- Use the converted JPEG File, not the original HEIC Blob, when creating
Mattermost sourceUrl attachment previews.
- Persist normalized HEIC upload metadata in GenClaw asset records so
stored `.jpg` assets are not recorded as original `.HEIC` files.

## Test Plan
- pnpm --dir web --filter @zooclaw/web-app run lint
- pnpm --dir web --filter @zooclaw/web-app exec tsc --noEmit
- pnpm --dir web --filter @zooclaw/web-app exec vitest run --config
./vitest.config.mts tests/unit/lib/heic-image.unit.spec.ts
tests/unit/lib/upload-extras.unit.spec.ts
tests/unit/app/chat/useMattermostIntegration.unit.spec.ts
tests/unit/app/chat/GenClawInput-extras.unit.spec.tsx
- pnpm --dir web run test:unit

## Notes
- Related Linear issue: ECA-786
- `pnpm --dir web run tsc` currently fails before TypeScript runs
because the workspace script passes `--if-present` to `pnpm exec`;
package-level tsc passes.
- `pnpm --dir web run lint` currently fails after web-app lint passes
because packages/auth-client cannot resolve `typescript-eslint`;
package-level web-app lint passes.
```

### PR Description

## Summary
- Convert HEIC/HEIF uploads to JPEG before R2 and Mattermost upload handling.
- Avoid rendering raw HEIC blobs as pending Mattermost previews, then swap to the converted JPEG preview.
- Return the actual uploaded File from R2 uploads so chat asset metadata records post-conversion name/type/size.
- Add regression coverage for the converter helper, R2 upload path, Mattermost upload path, and chat asset metadata recording.

## Review-driven fixes
- Keep HEIC conversion inside the R2 upload error boundary so conversion failures return a structured UploadResult error.
- Use the converted JPEG File, not the original HEIC Blob, when creating Mattermost sourceUrl attachment previews.
- Persist normalized HEIC upload metadata in GenClaw asset records so stored `.jpg` assets are not recorded as original `.HEIC` files.

## Test Plan
- pnpm --dir web --filter @zooclaw/web-app run lint
- pnpm --dir web --filter @zooclaw/web-app exec tsc --noEmit
- pnpm --dir web --filter @zooclaw/web-app exec vitest run --config ./vitest.config.mts tests/unit/lib/heic-image.unit.spec.ts tests/unit/lib/upload-extras.unit.spec.ts tests/unit/app/chat/useMattermostIntegration.unit.spec.ts tests/unit/app/chat/GenClawInput-extras.unit.spec.tsx
- pnpm --dir web run test:unit

## Notes
- Related Linear issue: ECA-786
- `pnpm --dir web run tsc` currently fails before TypeScript runs because the workspace script passes `--if-present` to `pnpm exec`; package-level tsc passes.
- `pnpm --dir web run lint` currently fails after web-app lint passes because packages/auth-client cannot resolve `typescript-eslint`; package-level web-app lint passes.

---

## e6855791 — test(chat): add unit specs for 4 extracted chat hooks (ECA-773) (#1840)

- **Author**: Chris@ZooClaw
- **Date**: 2026-05-21T18:32:23Z

### Full Commit Message

```
test(chat): add unit specs for 4 extracted chat hooks (ECA-773) (#1840)

## Summary
Adds focused unit specs for the four hooks extracted from
`GenClawClient` in #1799 that were previously only covered via
integration / snapshot paths. Follow-up to #1813 (useChatMessaging spec)
and closes
[ECA-773](https://linear.app/srpone/issue/ECA-773/testchat-add-unit-specs-for-the-4-remaining-extracted-chat-hooks).

| Hook | Coverage |
| -- | -- |
| `useChatSubagentRail` | agent-prefix filter (incl. `agentId=null →
main` fallback), visible/collapsed phase split, `subagentParam`
deep-link auto-sync, agentId-change reset, `activeSubagentSession`
derivation across both slices, key persistence across
`effectiveIsGenerating` flips, `useSubagentSessions` wiring (verbatim
forward) |
| `useChatPanels` | `showToolSteps` localStorage round-trip (default +
`"0"`/`"1"`), `toggleSettings`/`toggleResources` mutual exclusion,
`closeArtifacts` prop call sites, `artifactsOpen` save effect +
`closeArtifactsAndRestoreResources` restore, one-shot ref clearing |
| `useChatPaymentReturn` | guard branches (null / missing `session_id` /
missing `order_id`), success path with `productType` default, URL
`session_id`/`order_id`/`type`/`plan` strip after success,
`paymentProcessedRef` single-fire guard, `logger.error` on gateway
rejection, no-strip on failure |
| `useImagePreviewBridge` | `window.openImagePreview` register +
cleanup, single-image vs gallery opener, `closePreview`,
`navigatePreview` for valid / out-of-range / no-gallery cases |

All four files follow the `useChatMessaging` + `useSubagentSessions`
template: `vi.hoisted()` mocks, `mkXxx()` factories with overrides,
`renderHook` + `act`, fake timers opt-in only (none of the new specs
need them).

## Test plan
- [x] `pnpm exec vitest run
tests/unit/app/chat/useChatSubagentRail.unit.spec.ts` — 15 pass
- [x] `pnpm exec vitest run
tests/unit/app/chat/useChatPanels.unit.spec.ts` — 12 pass
- [x] `pnpm exec vitest run
tests/unit/app/chat/useChatPaymentReturn.unit.spec.ts` — 9 pass
- [x] `pnpm exec vitest run
tests/unit/app/chat/useImagePreviewBridge.unit.spec.ts` — 8 pass
- [x] `pnpm exec vitest run tests/unit/app/chat` — 574 / 574 (37 files)
pass
- [x] `pnpm exec eslint
tests/unit/app/chat/use{ChatSubagentRail,ChatPanels,ChatPaymentReturn,ImagePreviewBridge}.unit.spec.ts`
clean
- [x] `pnpm exec tsc --noEmit` clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary
Adds focused unit specs for the four hooks extracted from `GenClawClient` in #1799 that were previously only covered via integration / snapshot paths. Follow-up to #1813 (useChatMessaging spec) and closes [ECA-773](https://linear.app/srpone/issue/ECA-773/testchat-add-unit-specs-for-the-4-remaining-extracted-chat-hooks).

| Hook | Coverage |
| -- | -- |
| `useChatSubagentRail` | agent-prefix filter (incl. `agentId=null → main` fallback), visible/collapsed phase split, `subagentParam` deep-link auto-sync, agentId-change reset, `activeSubagentSession` derivation across both slices, key persistence across `effectiveIsGenerating` flips, `useSubagentSessions` wiring (verbatim forward) |
| `useChatPanels` | `showToolSteps` localStorage round-trip (default + `"0"`/`"1"`), `toggleSettings`/`toggleResources` mutual exclusion, `closeArtifacts` prop call sites, `artifactsOpen` save effect + `closeArtifactsAndRestoreResources` restore, one-shot ref clearing |
| `useChatPaymentReturn` | guard branches (null / missing `session_id` / missing `order_id`), success path with `productType` default, URL `session_id`/`order_id`/`type`/`plan` strip after success, `paymentProcessedRef` single-fire guard, `logger.error` on gateway rejection, no-strip on failure |
| `useImagePreviewBridge` | `window.openImagePreview` register + cleanup, single-image vs gallery opener, `closePreview`, `navigatePreview` for valid / out-of-range / no-gallery cases |

All four files follow the `useChatMessaging` + `useSubagentSessions` template: `vi.hoisted()` mocks, `mkXxx()` factories with overrides, `renderHook` + `act`, fake timers opt-in only (none of the new specs need them).

## Test plan
- [x] `pnpm exec vitest run tests/unit/app/chat/useChatSubagentRail.unit.spec.ts` — 15 pass
- [x] `pnpm exec vitest run tests/unit/app/chat/useChatPanels.unit.spec.ts` — 12 pass
- [x] `pnpm exec vitest run tests/unit/app/chat/useChatPaymentReturn.unit.spec.ts` — 9 pass
- [x] `pnpm exec vitest run tests/unit/app/chat/useImagePreviewBridge.unit.spec.ts` — 8 pass
- [x] `pnpm exec vitest run tests/unit/app/chat` — 574 / 574 (37 files) pass
- [x] `pnpm exec eslint tests/unit/app/chat/use{ChatSubagentRail,ChatPanels,ChatPaymentReturn,ImagePreviewBridge}.unit.spec.ts` clean
- [x] `pnpm exec tsc --noEmit` clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 6f96b6ef — fix(claw-interface): stop injecting LITELLM_API_BASE into bot pod env (#1837)

- **Author**: siqiao-srp
- **Date**: 2026-05-21T16:10:20Z

### Full Commit Message

```
fix(claw-interface): stop injecting LITELLM_API_BASE into bot pod env (#1837)

## Summary

Remove all `LITELLM_API_BASE` injection into bot pod deployment env.
This is a companion to #1835 (xai provider revert).

- `LITELLM_PROXY_URL` points to an internal K8s service
(`litellm.openclaw.internal`) that resolves to a private IP
- Injecting it as `LITELLM_API_BASE` into bot pods causes OpenClaw's
`url-fetch` SSRF guard to block any tool that routes HTTP requests
through LiteLLM (e.g. `video_generate`)
- Removed from: `create_bot()`, `_litellm_deployment_env()`,
`patch_model_config_if_missing()` (3 code paths)
- Bots continue to use `OPENCLAW_PLATFORM_LLM_URL` for model provider
config and individual API keys (`XAI_API_KEY`, etc.) for direct provider
access

## Test plan

- [x] `pyright` clean on changed files
- [x] All 163 unit tests pass
- [x] No remaining `LITELLM_API_BASE` injection in bot deployment code
- [ ] CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```

### PR Description

## Summary

Remove all `LITELLM_API_BASE` injection into bot pod deployment env. This is a companion to #1835 (xai provider revert).

- `LITELLM_PROXY_URL` points to an internal K8s service (`litellm.openclaw.internal`) that resolves to a private IP
- Injecting it as `LITELLM_API_BASE` into bot pods causes OpenClaw's `url-fetch` SSRF guard to block any tool that routes HTTP requests through LiteLLM (e.g. `video_generate`)
- Removed from: `create_bot()`, `_litellm_deployment_env()`, `patch_model_config_if_missing()` (3 code paths)
- Bots continue to use `OPENCLAW_PLATFORM_LLM_URL` for model provider config and individual API keys (`XAI_API_KEY`, etc.) for direct provider access

## Test plan

- [x] `pyright` clean on changed files
- [x] All 163 unit tests pass
- [x] No remaining `LITELLM_API_BASE` injection in bot deployment code
- [ ] CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 37ed9a5e — fix(billing): dedupe Stripe renewal credit grants (#1829)

- **Author**: kaka-srp
- **Date**: 2026-05-21T13:36:11Z

### Full Commit Message

```
fix(billing): dedupe Stripe renewal credit grants (#1829)

## Summary
- make Stripe monthly cron recover only paid invoices, instead of
granting directly from active subscription status
- share Stripe webhook and cron renewal order resolution through
`stripe_invoice_id`
- link legacy `CRON-RENEWAL-*` orders to invoices to avoid post-cron
webhook double grants
- add Apple same-period guard and regression coverage

## Root cause
Stripe monthly subscription sync treated an active subscription with an
expired local `subscription_end_time` as a missed renewal webhook and
granted credits immediately. When the real `invoice.paid` webhook
arrived later, it created a separate `RENEWAL-{invoice_id}` order and
granted the same period again. The previous cron/webhook dedup depended
on mutable `subscription_end_time`, so it missed this race after cron
advanced the user row.

## Linear

https://linear.app/srpone/issue/ECA-783/prevent-duplicate-subscription-renewal-credits

## Test plan
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff check .`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/pyright --pythonpath
/home/node/.venvs/claw-interface/bin/python app tests`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_handle_invoice_paid.py
tests/unit/test_subscription_cron.py
tests/unit/test_stripe_renewal_cron.py
tests/unit/test_stripe_renewal_order.py
tests/unit/test_apple_subscription_manager.py
tests/unit/test_orders_repo.py`
```

### PR Description

## Summary
- make Stripe monthly cron recover only paid invoices, instead of granting directly from active subscription status
- share Stripe webhook and cron renewal order resolution through `stripe_invoice_id`
- link legacy `CRON-RENEWAL-*` orders to invoices to avoid post-cron webhook double grants
- add Apple same-period guard and regression coverage

## Root cause
Stripe monthly subscription sync treated an active subscription with an expired local `subscription_end_time` as a missed renewal webhook and granted credits immediately. When the real `invoice.paid` webhook arrived later, it created a separate `RENEWAL-{invoice_id}` order and granted the same period again. The previous cron/webhook dedup depended on mutable `subscription_end_time`, so it missed this race after cron advanced the user row.

## Linear
https://linear.app/srpone/issue/ECA-783/prevent-duplicate-subscription-renewal-credits

## Test plan
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff check .`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/pyright --pythonpath /home/node/.venvs/claw-interface/bin/python app tests`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_handle_invoice_paid.py tests/unit/test_subscription_cron.py tests/unit/test_stripe_renewal_cron.py tests/unit/test_stripe_renewal_order.py tests/unit/test_apple_subscription_manager.py tests/unit/test_orders_repo.py`


---

## 5874d310 — fix: allow naming WeChat channels (#1830)

- **Author**: tim-srp
- **Date**: 2026-05-21T13:08:56Z

### Full Commit Message

```
fix: allow naming WeChat channels (#1830)

## Summary\n- show the account/name input for WeChat QR setup\n- pass
optional WeChat account names through frontend and backend setup
sessions\n- preserve the old fallback to the detected WeChat ilink
account when the user leaves the default value untouched\n\nLinear:
https://linear.app/srpone/issue/ECA-780/allow-naming-wechat-channels\nCloses
#1826\n\n## Local checks\n- ✅ pnpm exec vitest run
tests/unit/app/claw-settings/ChannelsSection-extras.unit.spec.tsx
tests/unit/app/claw-settings/WeixinSetupModal.unit.spec.tsx
tests/unit/lib/api/openclaw-settings-extras.unit.spec.ts\n- ✅ pnpm exec
eslint 'src/app/[locale]/claw-settings/components/ChannelsSection.tsx'
'src/app/[locale]/claw-settings/components/WeixinSetupModal.tsx'
src/lib/api/openclaw-settings.ts
tests/unit/app/claw-settings/ChannelsSection-extras.unit.spec.tsx
tests/unit/app/claw-settings/WeixinSetupModal.unit.spec.tsx
tests/unit/lib/api/openclaw-settings-extras.unit.spec.ts\n- ✅ ruff check
app/schema/openclaw_settings.py app/routes/openclaw_settings/weixin.py
app/routes/openclaw_settings/weixin_session.py
tests/unit/test_openclaw_settings_routes.py\n- ✅ pytest -o
filterwarnings='ignore::PendingDeprecationWarning'
tests/unit/test_openclaw_settings_routes.py -k 'WeixinSetupScenarios or
WeixinPollEndpoint'\n\n## Full-check notes\n- ⚠️ pnpm --dir web run lint
currently fails on unrelated existing Prettier ordering in
web/app/src/app/[locale]/chat/components/GenClawInput.tsx\n- ⚠️ pnpm
--dir web run tsc fails because the workspace script invokes pnpm exec
with unsupported --if-present in this local pnpm; direct app tsc also
hits unrelated existing xlsx type-resolution errors\n- ⚠️ ruff check .
fails on unrelated existing unused noqa directives in
services/claw-interface/tests/unit/test_openclaw_agents.py\n- ⚠️
targeted pyright in this local environment cannot resolve installed
Python packages such as fastapi/httpx/pytest
```

### PR Description

## Summary\n- show the account/name input for WeChat QR setup\n- pass optional WeChat account names through frontend and backend setup sessions\n- preserve the old fallback to the detected WeChat ilink account when the user leaves the default value untouched\n\nLinear: https://linear.app/srpone/issue/ECA-780/allow-naming-wechat-channels\nCloses #1826\n\n## Local checks\n- ✅ pnpm exec vitest run tests/unit/app/claw-settings/ChannelsSection-extras.unit.spec.tsx tests/unit/app/claw-settings/WeixinSetupModal.unit.spec.tsx tests/unit/lib/api/openclaw-settings-extras.unit.spec.ts\n- ✅ pnpm exec eslint 'src/app/[locale]/claw-settings/components/ChannelsSection.tsx' 'src/app/[locale]/claw-settings/components/WeixinSetupModal.tsx' src/lib/api/openclaw-settings.ts tests/unit/app/claw-settings/ChannelsSection-extras.unit.spec.tsx tests/unit/app/claw-settings/WeixinSetupModal.unit.spec.tsx tests/unit/lib/api/openclaw-settings-extras.unit.spec.ts\n- ✅ ruff check app/schema/openclaw_settings.py app/routes/openclaw_settings/weixin.py app/routes/openclaw_settings/weixin_session.py tests/unit/test_openclaw_settings_routes.py\n- ✅ pytest -o filterwarnings='ignore::PendingDeprecationWarning' tests/unit/test_openclaw_settings_routes.py -k 'WeixinSetupScenarios or WeixinPollEndpoint'\n\n## Full-check notes\n- ⚠️ pnpm --dir web run lint currently fails on unrelated existing Prettier ordering in web/app/src/app/[locale]/chat/components/GenClawInput.tsx\n- ⚠️ pnpm --dir web run tsc fails because the workspace script invokes pnpm exec with unsupported --if-present in this local pnpm; direct app tsc also hits unrelated existing xlsx type-resolution errors\n- ⚠️ ruff check . fails on unrelated existing unused noqa directives in services/claw-interface/tests/unit/test_openclaw_agents.py\n- ⚠️ targeted pyright in this local environment cannot resolve installed Python packages such as fastapi/httpx/pytest

---

## f9b2ee87 — fix(claw-interface): preserve managed agent channel bindings (#1828)

- **Author**: sam-srp
- **Date**: 2026-05-21T12:34:32Z

### Full Commit Message

```
fix(claw-interface): preserve managed agent channel bindings (#1828)

## Summary
- Preserve existing channel bindings for selected managed agents when
rewriting OpenClaw agents.list.
- Only generate Mattermost bindings for newly hired managed agents.
- Add unit coverage for managed binding preservation, fired-agent
cleanup, and hire-time Mattermost binding generation.

## Root cause
The previous deploy path filtered out every binding whose agentId
belonged to managed agents, then added back only generated Mattermost
bindings. Hiring another managed agent therefore removed existing custom
channel bindings such as Weixin/Feishu from already-selected managed
agents.

## Test plan
- [x] `conda run -n base python -m pytest
services/claw-interface/tests/unit/test_openclaw_agents.py -k
'ApplyAgentsList or DeploySelectedAgents'`\n- [x] `ruff check
services/claw-interface/app/services/openclaw/agent_deploy.py
services/claw-interface/tests/unit/test_openclaw_agents.py`\n- [x] `ruff
format --check
services/claw-interface/app/services/openclaw/agent_deploy.py
services/claw-interface/tests/unit/test_openclaw_agents.py`
```

### PR Description

## Summary
- Preserve existing channel bindings for selected managed agents when rewriting OpenClaw agents.list.
- Only generate Mattermost bindings for newly hired managed agents.
- Add unit coverage for managed binding preservation, fired-agent cleanup, and hire-time Mattermost binding generation.

## Root cause
The previous deploy path filtered out every binding whose agentId belonged to managed agents, then added back only generated Mattermost bindings. Hiring another managed agent therefore removed existing custom channel bindings such as Weixin/Feishu from already-selected managed agents.

## Test plan
- [x] `conda run -n base python -m pytest services/claw-interface/tests/unit/test_openclaw_agents.py -k 'ApplyAgentsList or DeploySelectedAgents'`\n- [x] `ruff check services/claw-interface/app/services/openclaw/agent_deploy.py services/claw-interface/tests/unit/test_openclaw_agents.py`\n- [x] `ruff format --check services/claw-interface/app/services/openclaw/agent_deploy.py services/claw-interface/tests/unit/test_openclaw_agents.py`

---

## 71748641 — fix(claw-interface): add Agent Studio model to degradation fallback table (#1815)

- **Author**: siqiao-srp
- **Date**: 2026-05-21T12:30:07Z

### Full Commit Message

```
fix(claw-interface): add Agent Studio model to degradation fallback table (#1815)

## Summary

- **Root cause**: Agent Studio uses an internal model alias
`agent-studio-sonnet-4-6` (hardcoded at hire time in
`agent_catalog.py`). This model was missing from
`MODEL_DEGRADATION_MAPPINGS` in `plan_models.py`. When a user's credits
are exhausted, the billing-gateway LiteLLM pre-call hook has no fallback
mapping → the request fails entirely → "Something went wrong while
processing your request."
- **Fix**: Add `"agent-studio-sonnet-4-6": _CHAT_FALLBACK`
(`qwen35-122B`) to the degradation mappings table, so Agent Studio
degrades gracefully like all other chat agents.
- Updated existing tier_writer test to include the new model in the
spot-check.

Closes ECA-777

## Test plan

- [x] `test_tier_writer.py::test_mappings_have_expected_chat_entries` —
now includes `agent-studio-sonnet-4-6`
- [x] All 7 tier_writer tests pass
- [x] ruff + pyright clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```

### PR Description

## Summary

- **Root cause**: Agent Studio uses an internal model alias `agent-studio-sonnet-4-6` (hardcoded at hire time in `agent_catalog.py`). This model was missing from `MODEL_DEGRADATION_MAPPINGS` in `plan_models.py`. When a user's credits are exhausted, the billing-gateway LiteLLM pre-call hook has no fallback mapping → the request fails entirely → "Something went wrong while processing your request."
- **Fix**: Add `"agent-studio-sonnet-4-6": _CHAT_FALLBACK` (`qwen35-122B`) to the degradation mappings table, so Agent Studio degrades gracefully like all other chat agents.
- Updated existing tier_writer test to include the new model in the spot-check.

Closes ECA-777

## Test plan

- [x] `test_tier_writer.py::test_mappings_have_expected_chat_entries` — now includes `agent-studio-sonnet-4-6`
- [x] All 7 tier_writer tests pass
- [x] ruff + pyright clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 22580de6 — fix(claw-interface): guard agent install rollback against MongoDB failures (#1825)

- **Author**: siqiao-srp
- **Date**: 2026-05-21T12:29:47Z

### Full Commit Message

```
fix(claw-interface): guard agent install rollback against MongoDB failures (#1825)

## Summary

- Wraps `_rollback_agent_state()` in try/except so a MongoDB error
during rollback is logged instead of propagated
- Previously, if deploy failed **and** the rollback write also failed,
the rollback exception masked the original error and left
`selected_agent_ids` permanently inconsistent with the bot's live
`agents.list` — causing an infinite "Reaching your Claw..." spinner with
no self-healing path

## Root Cause (ECA-779)

Both exception handlers in `install.py:252-276` call
`_rollback_agent_state()` bare (no try/except). If rollback itself fails
(transient MongoDB error), `selected_agent_ids` is never reverted,
creating a permanent state split:
- MongoDB thinks the agent is installed → HTTP 409 blocks re-install
- Bot config has no agent → `mmConnected` stays `false` → infinite
spinner

## Fix

`shared.py:_rollback_agent_state()` now catches and logs any exception
from `_persist_agent_state()`, ensuring the caller's original error is
always re-raised. All 4 rollback call sites (install + uninstall × 2
exception handlers) benefit from this single-point fix.

## Test plan

- [x] New test: `test_rollback_agent_state_swallows_mongo_error` —
verifies rollback does not raise when MongoDB write fails
- [x] Existing tests still pass (`test_openclaw_agents_shared.py` — 4/4)
- [x] `pyright` clean on changed file

Closes ECA-779

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```

### PR Description

## Summary

- Wraps `_rollback_agent_state()` in try/except so a MongoDB error during rollback is logged instead of propagated
- Previously, if deploy failed **and** the rollback write also failed, the rollback exception masked the original error and left `selected_agent_ids` permanently inconsistent with the bot's live `agents.list` — causing an infinite "Reaching your Claw..." spinner with no self-healing path

## Root Cause (ECA-779)

Both exception handlers in `install.py:252-276` call `_rollback_agent_state()` bare (no try/except). If rollback itself fails (transient MongoDB error), `selected_agent_ids` is never reverted, creating a permanent state split:
- MongoDB thinks the agent is installed → HTTP 409 blocks re-install
- Bot config has no agent → `mmConnected` stays `false` → infinite spinner

## Fix

`shared.py:_rollback_agent_state()` now catches and logs any exception from `_persist_agent_state()`, ensuring the caller's original error is always re-raised. All 4 rollback call sites (install + uninstall × 2 exception handlers) benefit from this single-point fix.

## Test plan

- [x] New test: `test_rollback_agent_state_swallows_mongo_error` — verifies rollback does not raise when MongoDB write fails
- [x] Existing tests still pass (`test_openclaw_agents_shared.py` — 4/4)
- [x] `pyright` clean on changed file

Closes ECA-779

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## bf816360 — fix(claw-interface): return actual invite binding in open registration mode (#1827)

- **Author**: siqiao-srp
- **Date**: 2026-05-21T12:29:32Z

### Full Commit Message

```
fix(claw-interface): return actual invite binding in open registration mode (#1827)

## Summary

- `/users/invite-status` now always queries the actual invite binding,
even when invite codes are not required (open registration mode)
- Previously, the endpoint short-circuited with `has_bound_invite_code:
false` in open registration mode, which broke the frontend's "returning
user bypass" for onboarding

## Root Cause (ECA-782)

When all three conditions were met simultaneously, a returning user was
incorrectly sent through onboarding and then stuck on permanent loading:

1. **Open registration mode** → `_should_require_invite_code()` returns
`False` → endpoint returns `has_bound_invite_code: false` without
checking actual binding
2. **Bot temporarily unavailable** (pod restart, stopped, etc.) →
`botStatus ≠ 'ready'`
3. **New device / cleared localStorage** → no local onboarding progress

The frontend resolver (`resolve-status.ts:133`) uses
`hasBoundInviteCode` as the "returning user bypass" — when the backend
lies about it, returning users fall through to onboarding.

## Fix

```python
# Before: early return skipped actual binding check
if not await _should_require_invite_code():
    return InviteStatusResponse(invite_code_required=False, has_bound_invite_code=False)

# After: always check actual binding
invite_required = await _should_require_invite_code()
binding = await get_invite_binding_for_user(uid)
# ... return actual has_bound_invite_code based on binding
```

## Test plan

- [x] New test: `test_not_required_with_binding_returns_bound` — open
registration + existing binding → `has_bound_invite_code=True`
- [x] Updated test: `test_not_required_no_binding` — open registration +
no binding → `has_bound_invite_code=False`
- [x] Existing tests still pass (5/5 in `TestGetInviteStatus`)
- [x] `pyright` clean

## User impact

- Affected user (uid `7275149935702016000`): bot was `stopped` since May
18; manually restarted via FastClaw. User can refresh to resume chat.
- This fix prevents the same scenario from recurring for any returning
user on a new device during transient bot unavailability.

Closes ECA-782

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```

### PR Description

## Summary

- `/users/invite-status` now always queries the actual invite binding, even when invite codes are not required (open registration mode)
- Previously, the endpoint short-circuited with `has_bound_invite_code: false` in open registration mode, which broke the frontend's "returning user bypass" for onboarding

## Root Cause (ECA-782)

When all three conditions were met simultaneously, a returning user was incorrectly sent through onboarding and then stuck on permanent loading:

1. **Open registration mode** → `_should_require_invite_code()` returns `False` → endpoint returns `has_bound_invite_code: false` without checking actual binding
2. **Bot temporarily unavailable** (pod restart, stopped, etc.) → `botStatus ≠ 'ready'`
3. **New device / cleared localStorage** → no local onboarding progress

The frontend resolver (`resolve-status.ts:133`) uses `hasBoundInviteCode` as the "returning user bypass" — when the backend lies about it, returning users fall through to onboarding.

## Fix

```python
# Before: early return skipped actual binding check
if not await _should_require_invite_code():
    return InviteStatusResponse(invite_code_required=False, has_bound_invite_code=False)

# After: always check actual binding
invite_required = await _should_require_invite_code()
binding = await get_invite_binding_for_user(uid)
# ... return actual has_bound_invite_code based on binding
```

## Test plan

- [x] New test: `test_not_required_with_binding_returns_bound` — open registration + existing binding → `has_bound_invite_code=True`
- [x] Updated test: `test_not_required_no_binding` — open registration + no binding → `has_bound_invite_code=False`
- [x] Existing tests still pass (5/5 in `TestGetInviteStatus`)
- [x] `pyright` clean

## User impact

- Affected user (uid `7275149935702016000`): bot was `stopped` since May 18; manually restarted via FastClaw. User can refresh to resume chat.
- This fix prevents the same scenario from recurring for any returning user on a new device during transient bot unavailability.

Closes ECA-782

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## d481fd3a — feat(im-channel): 重做 Add IM Channel 弹窗 + Telegram wizard 嵌入到面板内 (#1818)

- **Author**: lynn Zhuang
- **Date**: 2026-05-21T11:46:17Z

### Full Commit Message

```
feat(im-channel): 重做 Add IM Channel 弹窗 + Telegram wizard 嵌入到面板内 (#1818)

## Linear


https://linear.app/srpone/issue/ECA-781/重做-add-im-channel-弹窗-telegram-wizard-嵌入面板

## 概要
  最初只是想改"账号标识"文案，但发现整个 IM 频道添加流程的 UI 跟 ZooClaw 设计系统差距太大，索性一次性把这个模态框 +
  Telegram 引导 wizard 都重做一遍。
  ### 表单 i18n
- 10 个 locale 把 `accountId` 标签从 "Account identifier" → "Channel
name"（zh: 通道名称、ja: チャネル名、ko: 채널
이름 ...），原本预填的 "default" 值改为 placeholder（`accountIdPlaceholder` key
加翻译，留空提交时后端仍兜底
  `default`）。
- 新增 `policyOptions` i18n namespace：DM Policy / Group Policy 的下拉选项（open
/ allowlist / disabled /
  pairing）现在跟随用户 locale 翻译；`value` 仍是英文 ID（跟后端 wire-compat）。

  ### 新增 shadcn 组件
- 装 `@radix-ui/react-select`，新建三个 ds 组件（`input.tsx` / `label.tsx` /
`select.tsx`），沿用仓库现有
`dropdown-menu` / `button` 的写法约定：`rounded-md`、无 shadow、语义 token、focus +
data-state=open 都有 ring
  视觉反馈。
- Select 的 trigger 把 SelectValue 显式包到 `<span className="flex-1 truncate
text-left">`，确保 chevron
  永远在右侧（防止之前 chevron 跑到左边的 bug）。

  ### ZooClaw 设计对齐
- **不再用 `bg-primary` / `border-primary` token**——仓库根本没定义
`--primary`，shadcn
默认变体直接失效（之前的按钮看起来像纯文字就是这个原因）。primary CTA 走 ZooClaw 的 `bg-foreground
text-background`
pattern；outlined CTA 走 `border-border bg-card hover:bg-muted`。Modal 和
Telegram wizard 全部统一。
- emoji 占位符（🤖 / 📱 / ✈）替换为 heroicons（SparklesIcon / QrCodeIcon）——
跨平台视觉一致性，避免 macOS / Windows
  渲染差异。
- 文字 chevron `›` 替换为 `<ChevronRightIcon h-4 w-4>`，跟 Select 触发器的下拉箭头大小一致。
  - "Manual setup" 链接左对齐（`w-full text-left`），不再居中。

  ### 嵌入式 wizard（单面板二级导航）
- `TelegramSetupWizard` 去掉自己的 `<div fixed inset-0>` 外壳，现在是纯 content
组件（返回 Fragment）。
- `AddChannelModal` 内部用 `setupMode` 状态机（`null |
'telegram-guided'`）渲染不同视图，点击 Guided Bot Setup 卡片
  → setupMode='telegram-guided' → 同一个面板内切换到 wizard 内容。
- 顶部左上角加 `ChevronLeftIcon` 返回按钮（仅在 setupMode !== null 时显示），点击
setSetupMode(null) → **表单 state
  完全保留**（platform / agent / dmPolicy / groupPolicy / account 都不丢）。
- Wizard 的 `onSuccess` 关整个 modal + refresh 列表；`onClose`
只是回到表单视图。`ChannelsSection` 移除了
  `telegramWizardAgentId` 状态和外部 wizard 渲染。

  ## 测试清单
- [ ] 打开 `/<locale>/claw-settings` → IM 通道 → 添加频道，4 个下拉的 trigger
视觉一致：trigger 鼠标 hover
  无变化，**点击展开后 trigger 显示 ring**（跟 Input focus 一致）。
  - [ ] DM Policy / Group Policy 下拉选项跟随 locale 翻译（zh: 开放/白名单/禁用/需要配对；en:
  Open/Allowlist/Disabled/Pairing required ...）。
  - [ ] Channel name 输入框 placeholder 跟随 locale，不再有 "default" 预填。
- [ ] 选 Telegram → 点击 **Guided Bot Setup** 卡片：modal **不闪屏 /
不弹新窗口**，content 在同一个面板内切换到
wizard welcome；顶部标题变 "Connect Telegram"，左上出现 ← 返回箭头；面板高度自适应 wizard
内容（比表单矮）。
  - [ ] 点 ← 返回箭头：回到表单视图，**之前选的 platform / agent / policy / account 还在**。
- [ ] Wizard 内点 Get Started → 进入 create-bot 步骤，wizard 内部的 Back 按钮回到
welcome（顶部 ←
  仍然存在，可以从任意 wizard 步骤跳回表单）。
  - [ ] Wizard 走完所有步骤到 complete → 点 Done：modal 整个关闭，列表刷新出新频道。
  - [ ] 切 locale 全部测一遍（en/zh/ja/ko 等），文案都翻译。

  ## 范围外（保留 sibling modal 模式）
- Slack / Discord wizards、Feishu / WeCom / WeChat QR 模态框还是旧
sibling-modal 模式。它们也有同样的 `bg-primary`
  token 坏的样式问题，未来一个单独 PR 可以同样的 pattern 改造。
<img width="1400" height="1360" alt="screenshot-20260521-151410"
src="https://github.com/user-attachments/assets/62673a3b-b01c-424b-bc47-dc8b57a1fb7e"
/>


<img width="1442" height="1348" alt="screenshot-20260521-154834"
src="https://github.com/user-attachments/assets/ece5c822-de33-4e6c-962d-20e30acb7bee"
/>

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
Co-authored-by: claude[bot] <41898282+claude[bot]@users.noreply.github.com>
Co-authored-by: lynn Zhuang <undefined@users.noreply.github.com>
```

### PR Description

## Linear

https://linear.app/srpone/issue/ECA-781/重做-add-im-channel-弹窗-telegram-wizard-嵌入面板

## 概要
  最初只是想改"账号标识"文案，但发现整个 IM 频道添加流程的 UI 跟 ZooClaw 设计系统差距太大，索性一次性把这个模态框 +
  Telegram 引导 wizard 都重做一遍。
  ### 表单 i18n
  - 10 个 locale 把 `accountId` 标签从 "Account identifier" → "Channel name"（zh: 通道名称、ja: チャネル名、ko: 채널
  이름 ...），原本预填的 "default" 值改为 placeholder（`accountIdPlaceholder` key 加翻译，留空提交时后端仍兜底
  `default`）。
  - 新增 `policyOptions` i18n namespace：DM Policy / Group Policy 的下拉选项（open / allowlist / disabled /
  pairing）现在跟随用户 locale 翻译；`value` 仍是英文 ID（跟后端 wire-compat）。

  ### 新增 shadcn 组件
  - 装 `@radix-ui/react-select`，新建三个 ds 组件（`input.tsx` / `label.tsx` / `select.tsx`），沿用仓库现有
  `dropdown-menu` / `button` 的写法约定：`rounded-md`、无 shadow、语义 token、focus + data-state=open 都有 ring
  视觉反馈。
  - Select 的 trigger 把 SelectValue 显式包到 `<span className="flex-1 truncate text-left">`，确保 chevron
  永远在右侧（防止之前 chevron 跑到左边的 bug）。

  ### ZooClaw 设计对齐
  - **不再用 `bg-primary` / `border-primary` token**——仓库根本没定义 `--primary`，shadcn
  默认变体直接失效（之前的按钮看起来像纯文字就是这个原因）。primary CTA 走 ZooClaw 的 `bg-foreground text-background`
  pattern；outlined CTA 走 `border-border bg-card hover:bg-muted`。Modal 和 Telegram wizard 全部统一。
  - emoji 占位符（🤖 / 📱 / ✈）替换为 heroicons（SparklesIcon / QrCodeIcon）—— 跨平台视觉一致性，避免 macOS / Windows
  渲染差异。
  - 文字 chevron `›` 替换为 `<ChevronRightIcon h-4 w-4>`，跟 Select 触发器的下拉箭头大小一致。
  - "Manual setup" 链接左对齐（`w-full text-left`），不再居中。

  ### 嵌入式 wizard（单面板二级导航）
  - `TelegramSetupWizard` 去掉自己的 `<div fixed inset-0>` 外壳，现在是纯 content 组件（返回 Fragment）。
  - `AddChannelModal` 内部用 `setupMode` 状态机（`null | 'telegram-guided'`）渲染不同视图，点击 Guided Bot Setup 卡片
  → setupMode='telegram-guided' → 同一个面板内切换到 wizard 内容。
  - 顶部左上角加 `ChevronLeftIcon` 返回按钮（仅在 setupMode !== null 时显示），点击 setSetupMode(null) → **表单 state
  完全保留**（platform / agent / dmPolicy / groupPolicy / account 都不丢）。
  - Wizard 的 `onSuccess` 关整个 modal + refresh 列表；`onClose` 只是回到表单视图。`ChannelsSection` 移除了
  `telegramWizardAgentId` 状态和外部 wizard 渲染。

  ## 测试清单
  - [ ] 打开 `/<locale>/claw-settings` → IM 通道 → 添加频道，4 个下拉的 trigger 视觉一致：trigger 鼠标 hover
  无变化，**点击展开后 trigger 显示 ring**（跟 Input focus 一致）。
  - [ ] DM Policy / Group Policy 下拉选项跟随 locale 翻译（zh: 开放/白名单/禁用/需要配对；en:
  Open/Allowlist/Disabled/Pairing required ...）。
  - [ ] Channel name 输入框 placeholder 跟随 locale，不再有 "default" 预填。
  - [ ] 选 Telegram → 点击 **Guided Bot Setup** 卡片：modal **不闪屏 / 不弹新窗口**，content 在同一个面板内切换到
  wizard welcome；顶部标题变 "Connect Telegram"，左上出现 ← 返回箭头；面板高度自适应 wizard 内容（比表单矮）。
  - [ ] 点 ← 返回箭头：回到表单视图，**之前选的 platform / agent / policy / account 还在**。
  - [ ] Wizard 内点 Get Started → 进入 create-bot 步骤，wizard 内部的 Back 按钮回到 welcome（顶部 ←
  仍然存在，可以从任意 wizard 步骤跳回表单）。
  - [ ] Wizard 走完所有步骤到 complete → 点 Done：modal 整个关闭，列表刷新出新频道。
  - [ ] 切 locale 全部测一遍（en/zh/ja/ko 等），文案都翻译。

  ## 范围外（保留 sibling modal 模式）
  - Slack / Discord wizards、Feishu / WeCom / WeChat QR 模态框还是旧 sibling-modal 模式。它们也有同样的 `bg-primary`
  token 坏的样式问题，未来一个单独 PR 可以同样的 pattern 改造。
<img width="1400" height="1360" alt="screenshot-20260521-151410" src="https://github.com/user-attachments/assets/62673a3b-b01c-424b-bc47-dc8b57a1fb7e" />


<img width="1442" height="1348" alt="screenshot-20260521-154834" src="https://github.com/user-attachments/assets/ece5c822-de33-4e6c-962d-20e30acb7bee" />



---

## 49abf86a — fix(claw-interface): remove team billing identity usage (#1824)

- **Author**: tim-srp
- **Date**: 2026-05-21T10:51:56Z

### Full Commit Message

```
fix(claw-interface): remove team billing identity usage (#1824)

## Summary
- Stop treating team_id/team_key as the claw-interface billing identity
in the user-key flow.
- Use billing_key naming in the sanitized session boundary and pass
billing_key to downstream agent calls.
- Allow billing_key bootstrap to proceed without requiring a
personal-team team_id response, and stop returning team_id from credits
endpoints.

## Testing
- python -m ruff check
services/claw-interface/app/routes/session/chat.py
services/claw-interface/app/services/billing.py
services/claw-interface/app/services/billing_key_bootstrap.py
services/claw-interface/app/services/sanitize.py
services/claw-interface/app/services/stripe/billing_gateway.py
services/claw-interface/app/services/stripe/entitlement.py
services/claw-interface/app/routes/credits.py
services/claw-interface/app/services/billing_revoke.py
services/claw-interface/tests/unit/test_litellm_helpers.py
services/claw-interface/tests/unit/test_user_billing.py
services/claw-interface/tests/unit/test_user_credits.py
services/claw-interface/tests/bdd/step_defs/test_user_credits.py
- python -m pytest -p no:warnings
services/claw-interface/tests/unit/test_litellm_helpers.py
services/claw-interface/tests/unit/test_user_billing.py
services/claw-interface/tests/unit/test_user_credits.py
services/claw-interface/tests/unit/test_billing_revoke.py
services/claw-interface/tests/unit/test_admin_events.py
services/claw-interface/tests/unit/test_bg_reconcile.py
services/claw-interface/tests/unit/test_litellm_model_access.py
services/claw-interface/tests/unit/test_chat_create_session.py
services/claw-interface/tests/unit/test_stripe_billing_gateway.py
services/claw-interface/tests/unit/test_stripe_entitlement_service.py -q
- git diff --check

## Notes
- Did not modify billing-gateway.
- Local BDD step collection is blocked in this environment by missing
pytest_bdd.
```

### PR Description

## Summary
- Stop treating team_id/team_key as the claw-interface billing identity in the user-key flow.
- Use billing_key naming in the sanitized session boundary and pass billing_key to downstream agent calls.
- Allow billing_key bootstrap to proceed without requiring a personal-team team_id response, and stop returning team_id from credits endpoints.

## Testing
- python -m ruff check services/claw-interface/app/routes/session/chat.py services/claw-interface/app/services/billing.py services/claw-interface/app/services/billing_key_bootstrap.py services/claw-interface/app/services/sanitize.py services/claw-interface/app/services/stripe/billing_gateway.py services/claw-interface/app/services/stripe/entitlement.py services/claw-interface/app/routes/credits.py services/claw-interface/app/services/billing_revoke.py services/claw-interface/tests/unit/test_litellm_helpers.py services/claw-interface/tests/unit/test_user_billing.py services/claw-interface/tests/unit/test_user_credits.py services/claw-interface/tests/bdd/step_defs/test_user_credits.py
- python -m pytest -p no:warnings services/claw-interface/tests/unit/test_litellm_helpers.py services/claw-interface/tests/unit/test_user_billing.py services/claw-interface/tests/unit/test_user_credits.py services/claw-interface/tests/unit/test_billing_revoke.py services/claw-interface/tests/unit/test_admin_events.py services/claw-interface/tests/unit/test_bg_reconcile.py services/claw-interface/tests/unit/test_litellm_model_access.py services/claw-interface/tests/unit/test_chat_create_session.py services/claw-interface/tests/unit/test_stripe_billing_gateway.py services/claw-interface/tests/unit/test_stripe_entitlement_service.py -q
- git diff --check

## Notes
- Did not modify billing-gateway.
- Local BDD step collection is blocked in this environment by missing pytest_bdd.

---

## 5b0cdbb2 — fix(billing): sync bot keys for legacy recovery (#1823)

- **Author**: kaka-srp
- **Date**: 2026-05-21T10:43:48Z

### Full Commit Message

```
fix(billing): sync bot keys for legacy recovery (#1823)

## Linear
https://linear.app/srpone/issue/ECA-768

## Summary
- Only for legacy users who were expired without billing_key and receive
a new billing_key during entitlement bootstrap, sync the current user
LiteLLM key into existing OpenClaw bot config and deployment env before
restart.
- Preserve normal recovery behavior for users that already have
billing_key; their OpenClaw config/env is not rewritten by this path.
- Skip starting a bot if credential sync fails, so an old team key is
not reintroduced on recovery.

## Testing
- /home/node/.venvs/claw-interface/bin/pytest
tests/unit/test_user_billing.py tests/unit/test_start_user_bots.py
tests/unit/test_openclaw_bot_config.py
tests/unit/test_stripe_entitlement_service.py -q
- /home/node/.venvs/claw-interface/bin/ruff check
app/services/billing.py app/services/openclaw/bot_config.py
app/services/openclaw/bot_stop.py app/services/subscription_manager.py
app/services/stripe/entitlement.py tests/unit/test_user_billing.py
tests/unit/test_start_user_bots.py
tests/unit/test_openclaw_bot_config.py
tests/unit/test_stripe_entitlement_service.py
- /home/node/.venvs/claw-interface/bin/ruff format --check
app/services/billing.py app/services/openclaw/bot_config.py
app/services/openclaw/bot_stop.py app/services/subscription_manager.py
app/services/stripe/entitlement.py tests/unit/test_user_billing.py
tests/unit/test_start_user_bots.py
tests/unit/test_openclaw_bot_config.py
tests/unit/test_stripe_entitlement_service.py
- git diff --check
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-768

## Summary
- Only for legacy users who were expired without billing_key and receive a new billing_key during entitlement bootstrap, sync the current user LiteLLM key into existing OpenClaw bot config and deployment env before restart.
- Preserve normal recovery behavior for users that already have billing_key; their OpenClaw config/env is not rewritten by this path.
- Skip starting a bot if credential sync fails, so an old team key is not reintroduced on recovery.

## Testing
- /home/node/.venvs/claw-interface/bin/pytest tests/unit/test_user_billing.py tests/unit/test_start_user_bots.py tests/unit/test_openclaw_bot_config.py tests/unit/test_stripe_entitlement_service.py -q
- /home/node/.venvs/claw-interface/bin/ruff check app/services/billing.py app/services/openclaw/bot_config.py app/services/openclaw/bot_stop.py app/services/subscription_manager.py app/services/stripe/entitlement.py tests/unit/test_user_billing.py tests/unit/test_start_user_bots.py tests/unit/test_openclaw_bot_config.py tests/unit/test_stripe_entitlement_service.py
- /home/node/.venvs/claw-interface/bin/ruff format --check app/services/billing.py app/services/openclaw/bot_config.py app/services/openclaw/bot_stop.py app/services/subscription_manager.py app/services/stripe/entitlement.py tests/unit/test_user_billing.py tests/unit/test_start_user_bots.py tests/unit/test_openclaw_bot_config.py tests/unit/test_stripe_entitlement_service.py
- git diff --check

---

## fd1077dc — test(e2e): convert silent skips to hard fails + harden LLM Judge (#1755)

- **Author**: Chris@ZooClaw
- **Date**: 2026-05-21T10:05:18Z

### Full Commit Message

```
test(e2e): convert silent skips to hard fails + harden LLM Judge (#1755)

## Summary

Independent of #1747. Converts 27 runtime `test.skip()` sites across 18
e2e spec files into hard `expect()` failures, and hardens the LLM Judge
utility so it can no longer silently no-op on missing credentials.

**Why this matters now:** the daily-scheduled e2e workflow ran ~13 specs
that quietly `test.skip()` when a precondition failed (keyword missing,
sidebar absent, upload threw, etc.). Skipped tests showed up in reports
as 'skipped' but masked real regressions. Worse, in the tool-*
scenarios, every skip short-circuited the follow-up
`assertResponseRelevance()` call — meaning the LLM Judge code path
**never actually ran in CI**.

Where conditions need to be loose (LLM output variance), the loose
judgement is the existing LLM Judge with a lenient 'reasonable attempt →
YES' prompt; what changes is that the judge is now hard-asserted and
required in CI, instead of being a soft warning that returns
`passed:true` without credentials.

## What changed

1. `utils/llm-judge.ts` — `judgeResponse` / `judgeImageContent` throw
`LLMJudgeUnavailableError` when LITELLM_PROXY_URL / KEY are missing
(was: silent `passed:true` fallback).
2. `utils/assertions.ts` — `assertResponseRelevance` and
`assertImageContentRelevance` now `expect(result.passed).toBe(true)`
(was: console.warn-only).
3. `.github/workflows/e2e.yml` — adds 'Validate LLM Judge secrets' step
+ conditionally passes `--grep-invert @staging` for production runs.
4. **27 `test.skip()` sites → `expect()`** across 18 spec files:
- 8 keyword-precheck skips in `tool-{browser,document,misc,web}` +
`basic-usage` audio/image: now let the lenient LLM Judge make the call.
- 6 file-generation sidebar skips: fail loudly when the bot doesn't
produce a file artefact.
   - 4 file-upload skips: no longer swallow upload exceptions.
- 4 test-account-state skips: assert preconditions with explanatory
messages pointing at account setup.
   - 5 viewport / WS / UI structure skips: assert positive conditions.
5. Staging-only describe blocks (`onboarding-flow.spec.ts`, the
'Subscription Mutations (Staging Only)' block) move from runtime
`test.skip(!isStaging)` to `@staging` describe-name tags +
`--grep-invert @staging` in production workflow.
6. `test.fixme(...)` cases (`dark-mode-tokens` landing drift,
`landing-page` ECA-675 fixture) kept as-is — those need ECA-675
follow-up work.

## Not changed

- **Production code.** The Explore-agent report that motivated this PR
initially claimed 41 testids were missing from production; manual grep
showed that was almost entirely false (5 testids are template literals
like `data-testid={\`plan-card-${plan}\`}` that raw string grep misses,
4 belong to deleted features with no remaining spec references, the rest
were grep noise). No production testid changes are needed.
- **CI run scope.** The workflow's `--project=...` list still runs only
8 of 35 spec files. The ~17 hygiene conversions in this PR for non-CI
specs take effect when those projects are added to the run list
(separate scope).

## Test plan
- [x] `pnpm tsc --noEmit` clean
- [x] `pnpm lint` clean
- [x] `pnpm exec playwright test --list` parses 151 tests in 35 files
- [x] `--grep @staging` collects 9 (1 setup + 5 onboarding + 3
sub-mutations)
- [x] `--grep-invert @staging` collects 143
- [ ] `gh workflow run \"ZooClaw E2E Tests\" --ref feature/fix-e2e-tests
-f base_url=https://zooclaw.ai` — expect: reported `skipped` count drops
from current ~13 to 4 (only the kept `test.fixme()` cases); some new
failures expected (these are real regressions previously masked by
skip).

## Full spec doc

[docs/superpowers/specs/2026-05-19-e2e-skip-to-fail.md](./docs/superpowers/specs/2026-05-19-e2e-skip-to-fail.md)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Independent of #1747. Converts 27 runtime `test.skip()` sites across 18 e2e spec files into hard `expect()` failures, and hardens the LLM Judge utility so it can no longer silently no-op on missing credentials.

**Why this matters now:** the daily-scheduled e2e workflow ran ~13 specs that quietly `test.skip()` when a precondition failed (keyword missing, sidebar absent, upload threw, etc.). Skipped tests showed up in reports as 'skipped' but masked real regressions. Worse, in the tool-* scenarios, every skip short-circuited the follow-up `assertResponseRelevance()` call — meaning the LLM Judge code path **never actually ran in CI**.

Where conditions need to be loose (LLM output variance), the loose judgement is the existing LLM Judge with a lenient 'reasonable attempt → YES' prompt; what changes is that the judge is now hard-asserted and required in CI, instead of being a soft warning that returns `passed:true` without credentials.

## What changed

1. `utils/llm-judge.ts` — `judgeResponse` / `judgeImageContent` throw `LLMJudgeUnavailableError` when LITELLM_PROXY_URL / KEY are missing (was: silent `passed:true` fallback).
2. `utils/assertions.ts` — `assertResponseRelevance` and `assertImageContentRelevance` now `expect(result.passed).toBe(true)` (was: console.warn-only).
3. `.github/workflows/e2e.yml` — adds 'Validate LLM Judge secrets' step + conditionally passes `--grep-invert @staging` for production runs.
4. **27 `test.skip()` sites → `expect()`** across 18 spec files:
   - 8 keyword-precheck skips in `tool-{browser,document,misc,web}` + `basic-usage` audio/image: now let the lenient LLM Judge make the call.
   - 6 file-generation sidebar skips: fail loudly when the bot doesn't produce a file artefact.
   - 4 file-upload skips: no longer swallow upload exceptions.
   - 4 test-account-state skips: assert preconditions with explanatory messages pointing at account setup.
   - 5 viewport / WS / UI structure skips: assert positive conditions.
5. Staging-only describe blocks (`onboarding-flow.spec.ts`, the 'Subscription Mutations (Staging Only)' block) move from runtime `test.skip(!isStaging)` to `@staging` describe-name tags + `--grep-invert @staging` in production workflow.
6. `test.fixme(...)` cases (`dark-mode-tokens` landing drift, `landing-page` ECA-675 fixture) kept as-is — those need ECA-675 follow-up work.

## Not changed

- **Production code.** The Explore-agent report that motivated this PR initially claimed 41 testids were missing from production; manual grep showed that was almost entirely false (5 testids are template literals like `data-testid={\`plan-card-${plan}\`}` that raw string grep misses, 4 belong to deleted features with no remaining spec references, the rest were grep noise). No production testid changes are needed.
- **CI run scope.** The workflow's `--project=...` list still runs only 8 of 35 spec files. The ~17 hygiene conversions in this PR for non-CI specs take effect when those projects are added to the run list (separate scope).

## Test plan
- [x] `pnpm tsc --noEmit` clean
- [x] `pnpm lint` clean
- [x] `pnpm exec playwright test --list` parses 151 tests in 35 files
- [x] `--grep @staging` collects 9 (1 setup + 5 onboarding + 3 sub-mutations)
- [x] `--grep-invert @staging` collects 143
- [ ] `gh workflow run \"ZooClaw E2E Tests\" --ref feature/fix-e2e-tests -f base_url=https://zooclaw.ai` — expect: reported `skipped` count drops from current ~13 to 4 (only the kept `test.fixme()` cases); some new failures expected (these are real regressions previously masked by skip).

## Full spec doc
[docs/superpowers/specs/2026-05-19-e2e-skip-to-fail.md](./docs/superpowers/specs/2026-05-19-e2e-skip-to-fail.md)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## e24fb24d — feat(enterprise): logo_url https-only validation + org lifecycle BDD step defs (#1821)

- **Author**: bill-srp
- **Date**: 2026-05-21T09:03:22Z

### Full Commit Message

```
feat(enterprise): logo_url https-only validation + org lifecycle BDD step defs (#1821)

**Linear:**
https://linear.app/srpone/issue/ECA-764/enterprise-phase-1-backend-backlog

## Summary

Two Phase 1 follow-ups bundled in one PR — both small, independent,
merge-safe.

### 1. `logo_url` https-only validation (MEDIUM-1 from #1816 code
review)

`OrgCreateRequest.logo_url` and `OrgUpdateRequest.logo_url` now enforce
`pattern="^https://"` and `max_length=2048`. Blocks the
realistic-but-dangerous URI schemes (`javascript:`, `data:` SVG
payloads, `file:`, `ftp:`, plain `http:`) and the "pasted an entire
base64 image" abuse pattern **before** the frontend renders the value as
`<img src=...>` or a CSS background.

**Design choice:** validation is **request-only**.
- `Org` (persistence) and `OrgResponse` (egress) stay permissive so a
(somehow) malformed legacy row reads cleanly rather than 500ing on every
`Org.model_validate(doc)`.
- Tightening at ingress prevents new bad data from accumulating — the
asymmetry is documented by `test_persistence_org_stays_permissive`.

**Null-clears-logo gesture still works** — Pydantic v2 skips
`pattern`/`max_length` when value is `None`. Pinned by
`test_update_request_null_logo_url_still_allowed`.

**18 new tests** in `TestLogoUrlValidation`:
- 9 unsafe-scheme rejections at create (parametrized: `http:`,
`javascript:`, `data:`, `file:`, `ftp:`, empty, leading whitespace,
protocol-relative `//`, relative path)
- 4 same at update
- Oversize > 2048 chars rejected at both
- Valid `https://` accepted
- Omitted accepted
- Null still allowed (clear-logo regression guard)
- Persistence `Org` stays permissive (asymmetry guard)

### 2. S1-17 — BDD step defs for `org_lifecycle.feature`

Closes the outside-in BDD loop opened by S1-1 back when the membership
work started. The two Gherkin scenarios (create → invite → join, suspend
→ resume) now run end-to-end against **real Mongo with real indexes**.

**Catches bugs unit tests can't:**
- `unique_uid_active` partial index on `ecap-account-orgs` actually
fires under real Mongo
- `find_one_and_update(... return_document=True)` is the wrapper's
effective default
- Full route → service → repo chain for `join_org_handler` correctly
threads email-binding + org-id-match before service delegation

**Layering choice for the "join" step:** calls `join_org_handler` (route
layer) directly so the route-only email-binding + org-id checks are
exercised. Other steps call services directly — the routes for
create/invite/suspend/resume are thin pass-throughs.

**Per-scenario index bootstrap:** the autouse `clean_database` fixture
drops every collection (and its indexes) before each scenario; the
clean-DB `Given` step recreates them via `ensure_indexes` on all three
repos so partial-unique constraints fire during these scenarios.

## Test plan

- [x] `pytest tests/unit/test_schema_org.py -v` — 32 passed (18 new)
- [x] `pytest tests/unit/test_middleware_auth_and_org.py
tests/unit/test_org_repo.py tests/unit/test_org_service.py
tests/unit/test_routes_org.py tests/unit/test_schema_org.py -q` — 74
passed (org-touching suite)
- [x] `TEST_MONGODB_HOST=mongo-bdd MONGODB_USER=mongo
MONGODB_PASSWORD=mongo pytest tests/bdd/step_defs/test_org_lifecycle.py
-v` — 2 BDD scenarios pass against real Mongo with index recreation logs
visible
- [x] Full unit suite: 3482 passed (2 deptry failures are environmental
— worktree gitdir not resolvable from devcontainer; CI runs in clean
checkout and won't hit them)
- [x] `ruff format --check` + `ruff check` + `pyright` all clean on
changed files
- [ ] CI `build-and-test` + `auto-review` green

## Risk

- **Request-validation change is observable to FE.** Pre-launch (no
production clients), but the FE upload flow will need to ensure it only
PUTs https URLs to the logo field. Coordinated with FE: they're not
wired up yet.
- **BDD changes are test-only** — zero production-code risk.
```

### PR Description

**Linear:** https://linear.app/srpone/issue/ECA-764/enterprise-phase-1-backend-backlog

## Summary

Two Phase 1 follow-ups bundled in one PR — both small, independent, merge-safe.

### 1. `logo_url` https-only validation (MEDIUM-1 from #1816 code review)

`OrgCreateRequest.logo_url` and `OrgUpdateRequest.logo_url` now enforce `pattern="^https://"` and `max_length=2048`. Blocks the realistic-but-dangerous URI schemes (`javascript:`, `data:` SVG payloads, `file:`, `ftp:`, plain `http:`) and the "pasted an entire base64 image" abuse pattern **before** the frontend renders the value as `<img src=...>` or a CSS background.

**Design choice:** validation is **request-only**.
- `Org` (persistence) and `OrgResponse` (egress) stay permissive so a (somehow) malformed legacy row reads cleanly rather than 500ing on every `Org.model_validate(doc)`.
- Tightening at ingress prevents new bad data from accumulating — the asymmetry is documented by `test_persistence_org_stays_permissive`.

**Null-clears-logo gesture still works** — Pydantic v2 skips `pattern`/`max_length` when value is `None`. Pinned by `test_update_request_null_logo_url_still_allowed`.

**18 new tests** in `TestLogoUrlValidation`:
- 9 unsafe-scheme rejections at create (parametrized: `http:`, `javascript:`, `data:`, `file:`, `ftp:`, empty, leading whitespace, protocol-relative `//`, relative path)
- 4 same at update
- Oversize > 2048 chars rejected at both
- Valid `https://` accepted
- Omitted accepted
- Null still allowed (clear-logo regression guard)
- Persistence `Org` stays permissive (asymmetry guard)

### 2. S1-17 — BDD step defs for `org_lifecycle.feature`

Closes the outside-in BDD loop opened by S1-1 back when the membership work started. The two Gherkin scenarios (create → invite → join, suspend → resume) now run end-to-end against **real Mongo with real indexes**.

**Catches bugs unit tests can't:**
- `unique_uid_active` partial index on `ecap-account-orgs` actually fires under real Mongo
- `find_one_and_update(... return_document=True)` is the wrapper's effective default
- Full route → service → repo chain for `join_org_handler` correctly threads email-binding + org-id-match before service delegation

**Layering choice for the "join" step:** calls `join_org_handler` (route layer) directly so the route-only email-binding + org-id checks are exercised. Other steps call services directly — the routes for create/invite/suspend/resume are thin pass-throughs.

**Per-scenario index bootstrap:** the autouse `clean_database` fixture drops every collection (and its indexes) before each scenario; the clean-DB `Given` step recreates them via `ensure_indexes` on all three repos so partial-unique constraints fire during these scenarios.

## Test plan

- [x] `pytest tests/unit/test_schema_org.py -v` — 32 passed (18 new)
- [x] `pytest tests/unit/test_middleware_auth_and_org.py tests/unit/test_org_repo.py tests/unit/test_org_service.py tests/unit/test_routes_org.py tests/unit/test_schema_org.py -q` — 74 passed (org-touching suite)
- [x] `TEST_MONGODB_HOST=mongo-bdd MONGODB_USER=mongo MONGODB_PASSWORD=mongo pytest tests/bdd/step_defs/test_org_lifecycle.py -v` — 2 BDD scenarios pass against real Mongo with index recreation logs visible
- [x] Full unit suite: 3482 passed (2 deptry failures are environmental — worktree gitdir not resolvable from devcontainer; CI runs in clean checkout and won't hit them)
- [x] `ruff format --check` + `ruff check` + `pyright` all clean on changed files
- [ ] CI `build-and-test` + `auto-review` green

## Risk

- **Request-validation change is observable to FE.** Pre-launch (no production clients), but the FE upload flow will need to ensure it only PUTs https URLs to the logo field. Coordinated with FE: they're not wired up yet.
- **BDD changes are test-only** — zero production-code risk.

---

## 95f2179b — ci(enterprise-admin): scope deploy job to GitHub Environment for secrets (#1822)

- **Author**: bill-srp
- **Date**: 2026-05-21T09:00:38Z

### Full Commit Message

```
ci(enterprise-admin): scope deploy job to GitHub Environment for secrets (#1822)

## Summary

Fixes the staging auto-deploy on every merge to main. The
`deploy-enterprise-admin.yml` workflow has been failing on **every run
since it was added** on 2026-05-20 — `wrangler-action` receives an empty
`apiToken` and exits with:

> In a non-interactive environment, it's necessary to set a
CLOUDFLARE_API_TOKEN environment variable for wrangler to work.

## Root cause

The `deploy` job referenced `\${{ secrets.CLOUDFLARE_API_TOKEN }}` and
`\${{ secrets.CLOUDFLARE_ACCOUNT_ID }}` directly but had no
`environment:` declaration. Those secrets are defined under **GitHub
Environment** scope (Settings → Environments → staging / production),
not repository scope — and environment secrets are only accessible to
jobs that declare the matching `environment:`. Without the declaration,
the secret references resolve to empty strings and the action fails.

The working `deploy.yml` (line 85) uses the same pattern this PR adds:
```yaml
environment: \${{ needs.setup.outputs.environment }}
```

## Fix

One-line addition to the `deploy` job:

```yaml
deploy:
  needs: setup
  environment: \${{ needs.setup.outputs.environment }}   # ← added
  runs-on: ubuntu-latest
  ...
```

The `setup` job already resolves the environment name (`staging` for
branch pushes / staging dispatches, `production` for `-release` tags /
production dispatches), so the deploy job just reads that output. Same
name → environment secrets resolve correctly.

As a bonus, this also enables environment-protection rules (e.g. manual
approval on production) for future use.

## Out of scope (separate)

The wrangler warning about `images` missing under `env.staging` in
`wrangler.jsonc` is logged but doesn't block the deploy. Left for a
separate config PR if/when Images binding is needed.

## Test plan

- [x] Diff is exactly 6 lines added, no other changes
- [ ] After merge: next push to main triggers a green staging deploy
- [ ] After staging confirms, tag a `-beta` to verify production
environment access works the same way
```

### PR Description

## Summary

Fixes the staging auto-deploy on every merge to main. The `deploy-enterprise-admin.yml` workflow has been failing on **every run since it was added** on 2026-05-20 — `wrangler-action` receives an empty `apiToken` and exits with:

> In a non-interactive environment, it's necessary to set a CLOUDFLARE_API_TOKEN environment variable for wrangler to work.

## Root cause

The `deploy` job referenced `\${{ secrets.CLOUDFLARE_API_TOKEN }}` and `\${{ secrets.CLOUDFLARE_ACCOUNT_ID }}` directly but had no `environment:` declaration. Those secrets are defined under **GitHub Environment** scope (Settings → Environments → staging / production), not repository scope — and environment secrets are only accessible to jobs that declare the matching `environment:`. Without the declaration, the secret references resolve to empty strings and the action fails.

The working `deploy.yml` (line 85) uses the same pattern this PR adds:
```yaml
environment: \${{ needs.setup.outputs.environment }}
```

## Fix

One-line addition to the `deploy` job:

```yaml
deploy:
  needs: setup
  environment: \${{ needs.setup.outputs.environment }}   # ← added
  runs-on: ubuntu-latest
  ...
```

The `setup` job already resolves the environment name (`staging` for branch pushes / staging dispatches, `production` for `-release` tags / production dispatches), so the deploy job just reads that output. Same name → environment secrets resolve correctly.

As a bonus, this also enables environment-protection rules (e.g. manual approval on production) for future use.

## Out of scope (separate)

The wrangler warning about `images` missing under `env.staging` in `wrangler.jsonc` is logged but doesn't block the deploy. Left for a separate config PR if/when Images binding is needed.

## Test plan

- [x] Diff is exactly 6 lines added, no other changes
- [ ] After merge: next push to main triggers a green staging deploy
- [ ] After staging confirms, tag a `-beta` to verify production environment access works the same way

---

## 5226e624 — feat(enterprise-admin): Phase H polish — a11y + UX hardening (#1820)

- **Author**: bill-srp
- **Date**: 2026-05-21T08:46:47Z

### Full Commit Message

```
feat(enterprise-admin): Phase H polish — a11y + UX hardening (#1820)

## Linear


https://linear.app/srpone/issue/ECA-771/admin-console-web-phase-1-org-settings

(Reusing the Phase-1 issue since Phase H is final-mile polish across all
surfaces — same scope, same admin-console deliverable.)

## Summary

Phase H of the Enterprise Admin Console — accessibility, double-submit
guards, loading skeletons, responsive nav, and a hardened global error
boundary. Spec §1.6 (Polish, Day 9–10).

### a11y — 10 banner sites

`role="alert" aria-live="polite"` on every error region; `role="status"
aria-live="polite"` on success/partial-success. Cover:

| Surface | Banner |
|---|---|
| `/login`, `/verify` | submit error |
| `InviteDialog` | invite error |
| Onboarding step 1/2/3 | per-step submit error |
| Onboarding (page level) | partial bulk-invite success |
| `/org` | load + save error + Saved status |
| `/packs`, `/packs/[packId]` | load + action error |
| `/users` | load + action error |
| `/invite/[code]` | accept error + terminal error |

### Double-submit guards — 6 mutation surfaces

`useRef` synchronous in-flight refs close the click-spam race that
`disabled={isPending}` can't (button disabled isn't flushed before a
fast second click). Applied to:

- Login submit
- Verify submit + Resend
- InviteDialog send
- Onboarding step 1 (create-org), step 2 (bulk invite), step 3 (finish)
— 3 separate refs so partial advancement doesn't block the next step
- Org Settings save
- Invite Landing accept

Skipped intentionally: Users-table row actions (Suspend/Resume/Remove)
and Pack approve/reject/deprecate. Per-row refs add complexity; pack
actions already go through AlertDialog confirmation which auto-closes.

New regression test: triple-click on `/login` Continue fires
`sendEmailOTP` exactly **once** (`app/login/__tests__/login.test.tsx`).

### Loading skeletons — 3 pages

- **`components/ui/skeleton.tsx`** — shadcn-style primitive,
`aria-hidden`, `animate-pulse rounded-md bg-muted`.
- Replaced `Loading…` text with shape-matched skeletons in `/org`,
`/invite/[code]`, `/packs/[packId]`. Each is wrapped in `role="status"
aria-label="Loading …"` so screen readers announce the loading state.
- `UserTable` / `PackTable` already had skeleton rows; left alone.

### Responsive — mobile navigation

The dashboard `Sidebar` is `hidden md:flex` — below 768px there was **no
nav at all** once inside the dashboard. Now:

- **`components/layout/MobileNav.tsx`** — horizontal scrollable nav
strip rendered below `TopBar`, visible only `md:hidden`.
- Sidebar exports `NAV_ITEMS` + `visibleNavItems(role)` as the single
source of role-filtered nav (both renderers share it).
- `TopBar` truncates org/email below md, hides them on narrow widths to
keep the row from overflowing.

### Global error boundary

`app/error.tsx` rewritten to classify the failure before rendering:

- 5xx → "Something went wrong on our end"
- 403 → "You don't have access"
- 404 → "Not found"
- Other `ApiError` → its message
- `TypeError: fetch …` → "Network problem"
- Anything else → generic copy

Raw `error.message` is only shown when `NODE_ENV !== "production"` —
production users no longer see stack traces or internal errors.
`error.digest` is surfaced as a support reference. `console.error` log
capture (telemetry slot). Added a `Return home` CTA next to `Try again`.
401 → `/login` redirect preserved.

## Test plan

- [x] `pnpm test` — 161/161 (added 1 new test: double-click guard on
/login)
- [x] `pnpm exec tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm build` — clean; 9 routes prerendered identically
- [ ] Manual at 320 / 768 / 1024 / 1440 — verify mobile nav strip +
table overflow + TopBar truncation
- [ ] Manual: trigger a 5xx in dev — verify error boundary classifies +
suppresses raw message in production build
- [ ] Manual: VoiceOver / NVDA — confirm error banners announce on
submit failure
```

### PR Description

## Linear

https://linear.app/srpone/issue/ECA-771/admin-console-web-phase-1-org-settings

(Reusing the Phase-1 issue since Phase H is final-mile polish across all surfaces — same scope, same admin-console deliverable.)

## Summary

Phase H of the Enterprise Admin Console — accessibility, double-submit guards, loading skeletons, responsive nav, and a hardened global error boundary. Spec §1.6 (Polish, Day 9–10).

### a11y — 10 banner sites

`role="alert" aria-live="polite"` on every error region; `role="status" aria-live="polite"` on success/partial-success. Cover:

| Surface | Banner |
|---|---|
| `/login`, `/verify` | submit error |
| `InviteDialog` | invite error |
| Onboarding step 1/2/3 | per-step submit error |
| Onboarding (page level) | partial bulk-invite success |
| `/org` | load + save error + Saved status |
| `/packs`, `/packs/[packId]` | load + action error |
| `/users` | load + action error |
| `/invite/[code]` | accept error + terminal error |

### Double-submit guards — 6 mutation surfaces

`useRef` synchronous in-flight refs close the click-spam race that `disabled={isPending}` can't (button disabled isn't flushed before a fast second click). Applied to:

- Login submit
- Verify submit + Resend
- InviteDialog send
- Onboarding step 1 (create-org), step 2 (bulk invite), step 3 (finish) — 3 separate refs so partial advancement doesn't block the next step
- Org Settings save
- Invite Landing accept

Skipped intentionally: Users-table row actions (Suspend/Resume/Remove) and Pack approve/reject/deprecate. Per-row refs add complexity; pack actions already go through AlertDialog confirmation which auto-closes.

New regression test: triple-click on `/login` Continue fires `sendEmailOTP` exactly **once** (`app/login/__tests__/login.test.tsx`).

### Loading skeletons — 3 pages

- **`components/ui/skeleton.tsx`** — shadcn-style primitive, `aria-hidden`, `animate-pulse rounded-md bg-muted`.
- Replaced `Loading…` text with shape-matched skeletons in `/org`, `/invite/[code]`, `/packs/[packId]`. Each is wrapped in `role="status" aria-label="Loading …"` so screen readers announce the loading state.
- `UserTable` / `PackTable` already had skeleton rows; left alone.

### Responsive — mobile navigation

The dashboard `Sidebar` is `hidden md:flex` — below 768px there was **no nav at all** once inside the dashboard. Now:

- **`components/layout/MobileNav.tsx`** — horizontal scrollable nav strip rendered below `TopBar`, visible only `md:hidden`.
- Sidebar exports `NAV_ITEMS` + `visibleNavItems(role)` as the single source of role-filtered nav (both renderers share it).
- `TopBar` truncates org/email below md, hides them on narrow widths to keep the row from overflowing.

### Global error boundary

`app/error.tsx` rewritten to classify the failure before rendering:

- 5xx → "Something went wrong on our end"
- 403 → "You don't have access"
- 404 → "Not found"
- Other `ApiError` → its message
- `TypeError: fetch …` → "Network problem"
- Anything else → generic copy

Raw `error.message` is only shown when `NODE_ENV !== "production"` — production users no longer see stack traces or internal errors. `error.digest` is surfaced as a support reference. `console.error` log capture (telemetry slot). Added a `Return home` CTA next to `Try again`. 401 → `/login` redirect preserved.

## Test plan

- [x] `pnpm test` — 161/161 (added 1 new test: double-click guard on /login)
- [x] `pnpm exec tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm build` — clean; 9 routes prerendered identically
- [ ] Manual at 320 / 768 / 1024 / 1440 — verify mobile nav strip + table overflow + TopBar truncation
- [ ] Manual: trigger a 5xx in dev — verify error boundary classifies + suppresses raw message in production build
- [ ] Manual: VoiceOver / NVDA — confirm error banners announce on submit failure

---

## 980615d3 — feat(billing): route business billing through user keys (#1817)

- **Author**: kaka-srp
- **Date**: 2026-05-21T08:49:24Z

### Full Commit Message

```
feat(billing): route business billing through user keys (#1817)

## Linear
https://linear.app/srpone/issue/ECA-768

## Summary
- Move business-layer billing identity to `uid` and per-account
`billing_key`.
- Remove request-path fallback to legacy `team_id` / `team_key` for
LiteLLM and Billing Gateway calls.
- Persist `billing_key` immediately during bootstrap and avoid repeated
request-time key creation for legacy initialized users without a key.
- Add design spec with legacy cleanup guidance for `billing_initialized`
/ `billing_key` data.

## Testing
- `pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/app/api/litellm.unit.spec.ts
tests/unit/lib/api/headers.unit.spec.ts
tests/unit/canvas-hooks/useFalImageProcess.unit.spec.ts
tests/unit/hooks/useSSEStream.unit.spec.ts`
- `pnpm --dir web/app exec tsc --noEmit`
- `pnpm --dir web/app run lint`
- `pnpm --dir web run test:unit`
- `/home/node/.venvs/claw-interface/bin/ruff check app tests`
- `/home/node/.venvs/claw-interface/bin/pytest
tests/unit/test_user_billing.py tests/unit/test_account_billing_key.py
tests/unit/test_litellm_helpers.py tests/unit/test_admin_boost.py -q`
- `git diff --check`

## Notes
- Workspace-level `pnpm --dir web run lint` is blocked locally by
`web/packages/auth-client` missing `typescript-eslint` in that package
install context.
- Workspace-level `pnpm --dir web run tsc` is blocked locally because
its script passes `--if-present` to `pnpm exec`.
- Full backend `pyright app tests` is blocked locally by unresolved
third-party imports in the venv context.
- Full backend pytest still has an unrelated local failure in
`tests/unit/test_openclaw_agents.py::TestUpdateUserAgents::test_updates_agents_and_applies_config`,
where the test hits external OpenClaw/Mattermost mock paths and observes
an extra `mattermost_user` update.
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-768

## Summary
- Move business-layer billing identity to `uid` and per-account `billing_key`.
- Remove request-path fallback to legacy `team_id` / `team_key` for LiteLLM and Billing Gateway calls.
- Persist `billing_key` immediately during bootstrap and avoid repeated request-time key creation for legacy initialized users without a key.
- Add design spec with legacy cleanup guidance for `billing_initialized` / `billing_key` data.

## Testing
- `pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/app/api/litellm.unit.spec.ts tests/unit/lib/api/headers.unit.spec.ts tests/unit/canvas-hooks/useFalImageProcess.unit.spec.ts tests/unit/hooks/useSSEStream.unit.spec.ts`
- `pnpm --dir web/app exec tsc --noEmit`
- `pnpm --dir web/app run lint`
- `pnpm --dir web run test:unit`
- `/home/node/.venvs/claw-interface/bin/ruff check app tests`
- `/home/node/.venvs/claw-interface/bin/pytest tests/unit/test_user_billing.py tests/unit/test_account_billing_key.py tests/unit/test_litellm_helpers.py tests/unit/test_admin_boost.py -q`
- `git diff --check`

## Notes
- Workspace-level `pnpm --dir web run lint` is blocked locally by `web/packages/auth-client` missing `typescript-eslint` in that package install context.
- Workspace-level `pnpm --dir web run tsc` is blocked locally because its script passes `--if-present` to `pnpm exec`.
- Full backend `pyright app tests` is blocked locally by unresolved third-party imports in the venv context.
- Full backend pytest still has an unrelated local failure in `tests/unit/test_openclaw_agents.py::TestUpdateUserAgents::test_updates_agents_and_applies_config`, where the test hits external OpenClaw/Mattermost mock paths and observes an extra `mattermost_user` update.

---

## 121044ef — fix(web): refresh Mattermost bots after agent updates (#1719)

- **Author**: Chris@ZooClaw
- **Date**: 2026-05-21T08:07:42Z

### Full Commit Message

```
fix(web): refresh Mattermost bots after agent updates (#1719)

## Summary
- derive MattermostProvider mmBots from userBusinessData as the single
source of truth
- refresh /users/get after agent update events even when Mattermost is
not connected
- cover connected sync, empty bot clearing, and disconnected refresh ->
auto-connect behavior

## Test Plan
- pnpm --dir web run lint
- pnpm --dir web run test:unit
- pnpm --dir web --filter @zooclaw/web-app exec tsc --noEmit
- pnpm --dir web --filter @zooclaw/enterprise-admin exec tsc --noEmit
- pnpm --dir web --filter @zooclaw/auth-client exec tsc --noEmit
- pnpm --dir web/app exec vitest run
tests/unit/contexts/MattermostContext.unit.spec.tsx --config
./vitest.config.mts
- pnpm --dir web/app exec eslint
src/components/providers/MattermostProvider.tsx
tests/unit/contexts/MattermostContext.unit.spec.tsx --quiet --cache
--cache-location .eslintcache --cache-strategy content
- git diff --check

Note: `pnpm --dir web run tsc` currently fails before typechecking
because the repo script expands to `pnpm -r --workspace-concurrency=1
--if-present exec tsc --noEmit`, and this pnpm version reports `Unknown
option: if-present` for `exec`. The equivalent filtered tsc commands
above passed.
```

### PR Description

## Summary
- derive MattermostProvider mmBots from userBusinessData as the single source of truth
- refresh /users/get after agent update events even when Mattermost is not connected
- cover connected sync, empty bot clearing, and disconnected refresh -> auto-connect behavior

## Test Plan
- pnpm --dir web run lint
- pnpm --dir web run test:unit
- pnpm --dir web --filter @zooclaw/web-app exec tsc --noEmit
- pnpm --dir web --filter @zooclaw/enterprise-admin exec tsc --noEmit
- pnpm --dir web --filter @zooclaw/auth-client exec tsc --noEmit
- pnpm --dir web/app exec vitest run tests/unit/contexts/MattermostContext.unit.spec.tsx --config ./vitest.config.mts
- pnpm --dir web/app exec eslint src/components/providers/MattermostProvider.tsx tests/unit/contexts/MattermostContext.unit.spec.tsx --quiet --cache --cache-location .eslintcache --cache-strategy content
- git diff --check

Note: `pnpm --dir web run tsc` currently fails before typechecking because the repo script expands to `pnpm -r --workspace-concurrency=1 --if-present exec tsc --noEmit`, and this pnpm version reports `Unknown option: if-present` for `exec`. The equivalent filtered tsc commands above passed.

---

## 1b86331e —  fix(billing): PaymentMethodModal 禁用提示文案改成意图前置 (#1744)

- **Author**: lynn Zhuang
- **Date**: 2026-05-21T08:00:27Z

### Full Commit Message

```
 fix(billing): PaymentMethodModal 禁用提示文案改成意图前置 (#1744)

## 概要
  把 Select Payment Method 弹窗里那条**禁用提示**重新表述，让 reader 一扫就知道这句话跟自己的诉求是否相关。

  ```diff
  - Cancel your current subscription first to switch payment method.
+ To change your payment method, cancel your current subscription first.
  ```

  ### 为什么
  原版**结果前置**：用户读到最后才知道这条提示是关于"换支付方式"的——如果不关心这件事的人会把整句读完才意识到不相关。
  新版**意图前置**：开头就点明"To change your payment method"，用户第一眼就能决定要不要继续往下看。

  ### 范围
  - 单行字符串替换在 `SubscriptionPanel.tsx:793`（`disableReason` prop）
  - 文案在用户**有 active subscription 且想换另一种支付方式**时触发（一张卡片显示禁用态 + 底部居中显示这条提示）
- 没动 modal 组件本身，没动 i18n（这条文案本来就是 hardcoded prop，跟其它 hardcoded copy 保持一致）

  ## 测试清单
- [ ] 用一个有 active subscription 的账号登录，访问 `/en/subscription` → 点任意 Upgrade
按钮 →
  弹窗里和当前不同的支付通道卡片显示灰禁用 → 底部居中显示新文案。
  - [ ] 用没有订阅的账号访问同样路径 → 两张卡片都可点 → 底部不显示这条提示（预期，文案只在禁用态触发）。

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## 概要
  把 Select Payment Method 弹窗里那条**禁用提示**重新表述，让 reader 一扫就知道这句话跟自己的诉求是否相关。

  ```diff
  - Cancel your current subscription first to switch payment method.
  + To change your payment method, cancel your current subscription first.
  ```

  ### 为什么
  原版**结果前置**：用户读到最后才知道这条提示是关于"换支付方式"的——如果不关心这件事的人会把整句读完才意识到不相关。
  新版**意图前置**：开头就点明"To change your payment method"，用户第一眼就能决定要不要继续往下看。

  ### 范围
  - 单行字符串替换在 `SubscriptionPanel.tsx:793`（`disableReason` prop）
  - 文案在用户**有 active subscription 且想换另一种支付方式**时触发（一张卡片显示禁用态 + 底部居中显示这条提示）
  - 没动 modal 组件本身，没动 i18n（这条文案本来就是 hardcoded prop，跟其它 hardcoded copy 保持一致）

  ## 测试清单
  - [ ] 用一个有 active subscription 的账号登录，访问 `/en/subscription` → 点任意 Upgrade 按钮 →
  弹窗里和当前不同的支付通道卡片显示灰禁用 → 底部居中显示新文案。
  - [ ] 用没有订阅的账号访问同样路径 → 两张卡片都可点 → 底部不显示这条提示（预期，文案只在禁用态触发）。


---

## 04a53972 — feat(web): 功能上新弹窗加 SlideForge + Agent Studio + 移除 PPTX Master (#1743)

- **Author**: lynn Zhuang
- **Date**: 2026-05-21T07:59:55Z

### Full Commit Message

```
feat(web): 功能上新弹窗加 SlideForge + Agent Studio + 移除 PPTX Master (#1743)

## 概要
合并 SlideForge + Agent Studio 两个 launch 公告到一个 PR，**移除被替代的旧 PPTX Master
slide**，并附带原 PR #1622 的
Seedance 黑闪修复 / storage 版本 bump / dev 旁路等基础设施改动。原 PR #1622 已关闭（所有内容已
port 进本 PR）。

  ### 新增内容
  - **SlideForge**（第 1 位，最新）—— PPTX Master 的全面升级：16 个专家技能、73+
品牌风格、深度研究、storytelling、export。图传到 R2
`https://assets.yesy.site/f/images/2026/05/7rjljax7.png`。**10
  个 locale 全部带翻译**（`en/zh/ja/ko/fr/de/es/it/pt/ar`）。
- **Agent Studio**（第 2 位，来自 #1622）—— "1/10 Sonnet 价格" promo slide。沿用原 PR
的英文 fallback 策略（无 i18n
  key）。

  ### 移除内容
- **旧 PPTX Master slide**（之前的第 3 位）—— SlideForge 在文案上就承接了 PPTX Master
的角色（标题"PPTX Master just
  leveled up"），两张并列只会让用户困惑"那 PPTX 还在吗"。一并清掉 `PPTX_IMAGE_URL` 常量。

  ### 来自 #1622 的基础设施改动
- **Seedance 黑闪修复**：video 底下铺同 URL `<img aria-hidden>` 兜底 + modal
打开预热图片缓存 + video 原生 `poster`
  属性。封面帧从原视频 2.5s 提取，122KB JPEG on R2。
- **`FEATURE_LAUNCH_SEEN` bump 到 `:v2`**：让看过老弹窗的用户重新看到新轮播。下次再加 slide 时再
bump
  `:v3`（约定写在 storage key 旁的注释里）。
- **`?force-launch=1` dev 旁路**：`process.env.NODE_ENV !== 'production'`
guard，生产 tree-shake 掉，方便 review/QA
  预览。

  ### 最终 Slide 顺序（最新放第一）
  1. SlideForge（今天）
  2. Agent Studio（5 天前）
  3. Seedance 2.0（最旧，加 poster 防黑闪）

  ### 实现细节
- **Port 而非 cherry-pick**：#1622 的源分支
`feat/agent-studio-90-subsidy-announcement` 创建于 `web/` workspace
嵌套重构（#1713）**之前**，路径还是 `web/src/...`。直接 cherry-pick 会在每个文件上冲突。所以手工把它的 3
处改动（`FeatureLaunchModal.tsx` / `lib/auth/types.ts` / 测试）port 到新路径，并与
SlideForge 的改动融合。
- **单元测试**：slide 计数 `1/2` → `1/3`；"advance through slides" 测试点 2 次
Next；"Got it" 测试点 2 次 Next + 1
  次 Got it。

  ## 测试清单
- [ ] 登录 `/<locale>/chat`，在 DevTools Console 跑下面这段清掉 v2 标记 + 标
guide-tour 已看：
    ```js
Object.keys(localStorage).filter(k =>
k.startsWith('ecap:feature-launch-seen')).forEach(k =>
  localStorage.removeItem(k));
    localStorage.setItem('zooclaw-guide-tour-seen', '1');
    location.reload();
    ```
    等 5 秒，弹窗自动出现，第一张是 SlideForge。
- [ ] 或者直接访问 `/<locale>/chat?force-launch=1`，立即弹出（不用清 localStorage，dev
专用）。
- [ ] 切语言 `/en` → `/zh` → `/ja` ...，确认 **SlideForge 跟随 locale**；Agent
Studio / Seedance
  仍英文（预存量，未在本 PR 范围内补）。
- [ ] 点 Next 3 次走完所有 slide，最后 "Got it" 关闭，确认
`localStorage['ecap:feature-launch-seen:v2:<uid>']` 设为
  `'1'`。
- [ ] 重新打开（force-launch），切到 Seedance（最后一张），观察 video 加载阶段没有黑闪（poster
`<img>` 兜底）。

  ## Commits
  - `47e09f41` feat(web): add SlideForge slide to FeatureLaunchModal
- `21eea6f7` feat(web): fold in PR #1622 — Agent Studio slide + Seedance
poster + storage v2
- `85fef8c1` chore(web): tighten SlideForge copy + drop superseded PPTX
slide
<img width="3006" height="1546" alt="image"
src="https://github.com/user-attachments/assets/0dcb3ab4-c253-428b-a863-927b22afb1b5"
/>

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## 概要
  合并 SlideForge + Agent Studio 两个 launch 公告到一个 PR，**移除被替代的旧 PPTX Master slide**，并附带原 PR #1622 的
   Seedance 黑闪修复 / storage 版本 bump / dev 旁路等基础设施改动。原 PR #1622 已关闭（所有内容已 port 进本 PR）。

  ### 新增内容
  - **SlideForge**（第 1 位，最新）—— PPTX Master 的全面升级：16 个专家技能、73+
  品牌风格、深度研究、storytelling、export。图传到 R2 `https://assets.yesy.site/f/images/2026/05/7rjljax7.png`。**10
  个 locale 全部带翻译**（`en/zh/ja/ko/fr/de/es/it/pt/ar`）。
  - **Agent Studio**（第 2 位，来自 #1622）—— "1/10 Sonnet 价格" promo slide。沿用原 PR 的英文 fallback 策略（无 i18n
  key）。

  ### 移除内容
  - **旧 PPTX Master slide**（之前的第 3 位）—— SlideForge 在文案上就承接了 PPTX Master 的角色（标题"PPTX Master just
  leveled up"），两张并列只会让用户困惑"那 PPTX 还在吗"。一并清掉 `PPTX_IMAGE_URL` 常量。

  ### 来自 #1622 的基础设施改动
  - **Seedance 黑闪修复**：video 底下铺同 URL `<img aria-hidden>` 兜底 + modal 打开预热图片缓存 + video 原生 `poster`
  属性。封面帧从原视频 2.5s 提取，122KB JPEG on R2。
  - **`FEATURE_LAUNCH_SEEN` bump 到 `:v2`**：让看过老弹窗的用户重新看到新轮播。下次再加 slide 时再 bump
  `:v3`（约定写在 storage key 旁的注释里）。
  - **`?force-launch=1` dev 旁路**：`process.env.NODE_ENV !== 'production'` guard，生产 tree-shake 掉，方便 review/QA
  预览。

  ### 最终 Slide 顺序（最新放第一）
  1. SlideForge（今天）
  2. Agent Studio（5 天前）
  3. Seedance 2.0（最旧，加 poster 防黑闪）

  ### 实现细节
  - **Port 而非 cherry-pick**：#1622 的源分支 `feat/agent-studio-90-subsidy-announcement` 创建于 `web/` workspace
  嵌套重构（#1713）**之前**，路径还是 `web/src/...`。直接 cherry-pick 会在每个文件上冲突。所以手工把它的 3
  处改动（`FeatureLaunchModal.tsx` / `lib/auth/types.ts` / 测试）port 到新路径，并与 SlideForge 的改动融合。
  - **单元测试**：slide 计数 `1/2` → `1/3`；"advance through slides" 测试点 2 次 Next；"Got it" 测试点 2 次 Next + 1
  次 Got it。

  ## 测试清单
  - [ ] 登录 `/<locale>/chat`，在 DevTools Console 跑下面这段清掉 v2 标记 + 标 guide-tour 已看：
    ```js
    Object.keys(localStorage).filter(k => k.startsWith('ecap:feature-launch-seen')).forEach(k =>
  localStorage.removeItem(k));
    localStorage.setItem('zooclaw-guide-tour-seen', '1');
    location.reload();
    ```
    等 5 秒，弹窗自动出现，第一张是 SlideForge。
  - [ ] 或者直接访问 `/<locale>/chat?force-launch=1`，立即弹出（不用清 localStorage，dev 专用）。
  - [ ] 切语言 `/en` → `/zh` → `/ja` ...，确认 **SlideForge 跟随 locale**；Agent Studio / Seedance
  仍英文（预存量，未在本 PR 范围内补）。
  - [ ] 点 Next 3 次走完所有 slide，最后 "Got it" 关闭，确认 `localStorage['ecap:feature-launch-seen:v2:<uid>']` 设为
  `'1'`。
  - [ ] 重新打开（force-launch），切到 Seedance（最后一张），观察 video 加载阶段没有黑闪（poster `<img>` 兜底）。

  ## Commits
  - `47e09f41` feat(web): add SlideForge slide to FeatureLaunchModal
  - `21eea6f7` feat(web): fold in PR #1622 — Agent Studio slide + Seedance poster + storage v2
  - `85fef8c1` chore(web): tighten SlideForge copy + drop superseded PPTX slide
<img width="3006" height="1546" alt="image" src="https://github.com/user-attachments/assets/0dcb3ab4-c253-428b-a863-927b22afb1b5" />


---

## e4a0197a — feat(enterprise): Org.logo_url + team-only gate on org-scoped middleware (#1816)

- **Author**: bill-srp
- **Date**: 2026-05-21T07:52:12Z

### Full Commit Message

```
feat(enterprise): Org.logo_url + team-only gate on org-scoped middleware (#1816)

**Linear:**
https://linear.app/srpone/issue/ECA-764/enterprise-phase-1-backend-backlog

## Summary

Two small enterprise-org polish items on top of #1792.

### 1. `Org.logo_url` + atomic `update_fields` refactor (commit
`f3596bfb`)

- `logo_url: str | None` added to `Org`, `OrgResponse`,
`OrgCreateRequest`, `OrgUpdateRequest` — persistence + API surface for
an org-branding image URL.
- `logo_url=null` on update clears the field (admin "remove logo"
gesture). The schema-level `_reject_explicit_null` validator still
blocks null on the non-nullable int settings fields, so the change is
scoped.
- `org_repo.update_fields` now uses `find_one_and_update` with explicit
`return_document=True`, returning the post-update `Org | None`.
`org_service.update_org` drops its pre-check `get_by_id` — single atomic
DB roundtrip per update; `None` from the repo translates to
`NotFoundError`. Mirrors the pattern established in
`account_org_repo.update_status`.

### 2. Team-only gate on org-scoped routes (commit `87c596fd`)

`require_org_member` and `require_org_admin` now reject personal orgs
with **400** — personal orgs are implicit single-user bookkeeping that
the org-scoped API surface doesn't support. Personal-org owners interact
with their own data via the V2 user routes (`get_current_org` stays
type-agnostic on purpose).

Affects every `/orgs/{org_id}/*` endpoint that uses these deps —
user-management (invite, join, list, suspend, resume) AND org-CRUD (GET
/ POST). Intentional per design discussion: personal orgs have no
org-scoped API surface in Phase 1.

Extracted `_gated_membership` helper since both deps now share the same
four-step gate (membership → active status → org exists → team type);
`require_org_admin` adds the role check on top.

## Trade-offs

- **Extra DB roundtrip per gated request.** The team-only check adds one
`org_repo.get_by_id` lookup. Cheap (PK lookup, ~1ms). FastAPI dedupes
deps within a request, so routes declaring both `get_current_user` and
`require_org_admin` don't pay twice.
- **Behaviour change visible to FE.** Personal-org callers now get 400
from `/orgs/{org_id}/*`. Pre-launch, no production clients hit these —
but worth FE confirmation they don't accidentally route personal
`org_id` through the team API.

## Known follow-up

`logo_url` has no length cap / scheme allowlist at the schema boundary.
Pre-launch, low blast radius — but before the frontend renders
user-supplied logos, add `Field(max_length=2048, pattern=r"^https://")`
or coerce via `HttpUrl`. Tracked separately.

## Test plan

- [x] `pytest tests/unit/test_middleware_auth_and_org.py
tests/unit/test_org_repo.py tests/unit/test_org_service.py
tests/unit/test_routes_org.py tests/unit/test_schema_org.py` — 55/55
pass
- [x] Full unit suite: 3463 passed (2 deptry failures are environmental:
worktree gitdir not resolvable from devcontainer — CI runs in clean
checkout and won't hit this)
- [x] `ruff format --check` clean on changed files
- [x] `pyright app/` clean
- [ ] CI `build-and-test` + `auto-review` green
```

### PR Description

**Linear:** https://linear.app/srpone/issue/ECA-764/enterprise-phase-1-backend-backlog

## Summary

Two small enterprise-org polish items on top of #1792.

### 1. `Org.logo_url` + atomic `update_fields` refactor (commit `f3596bfb`)

- `logo_url: str | None` added to `Org`, `OrgResponse`, `OrgCreateRequest`, `OrgUpdateRequest` — persistence + API surface for an org-branding image URL.
- `logo_url=null` on update clears the field (admin "remove logo" gesture). The schema-level `_reject_explicit_null` validator still blocks null on the non-nullable int settings fields, so the change is scoped.
- `org_repo.update_fields` now uses `find_one_and_update` with explicit `return_document=True`, returning the post-update `Org | None`. `org_service.update_org` drops its pre-check `get_by_id` — single atomic DB roundtrip per update; `None` from the repo translates to `NotFoundError`. Mirrors the pattern established in `account_org_repo.update_status`.

### 2. Team-only gate on org-scoped routes (commit `87c596fd`)

`require_org_member` and `require_org_admin` now reject personal orgs with **400** — personal orgs are implicit single-user bookkeeping that the org-scoped API surface doesn't support. Personal-org owners interact with their own data via the V2 user routes (`get_current_org` stays type-agnostic on purpose).

Affects every `/orgs/{org_id}/*` endpoint that uses these deps — user-management (invite, join, list, suspend, resume) AND org-CRUD (GET / POST). Intentional per design discussion: personal orgs have no org-scoped API surface in Phase 1.

Extracted `_gated_membership` helper since both deps now share the same four-step gate (membership → active status → org exists → team type); `require_org_admin` adds the role check on top.

## Trade-offs

- **Extra DB roundtrip per gated request.** The team-only check adds one `org_repo.get_by_id` lookup. Cheap (PK lookup, ~1ms). FastAPI dedupes deps within a request, so routes declaring both `get_current_user` and `require_org_admin` don't pay twice.
- **Behaviour change visible to FE.** Personal-org callers now get 400 from `/orgs/{org_id}/*`. Pre-launch, no production clients hit these — but worth FE confirmation they don't accidentally route personal `org_id` through the team API.

## Known follow-up

`logo_url` has no length cap / scheme allowlist at the schema boundary. Pre-launch, low blast radius — but before the frontend renders user-supplied logos, add `Field(max_length=2048, pattern=r"^https://")` or coerce via `HttpUrl`. Tracked separately.

## Test plan

- [x] `pytest tests/unit/test_middleware_auth_and_org.py tests/unit/test_org_repo.py tests/unit/test_org_service.py tests/unit/test_routes_org.py tests/unit/test_schema_org.py` — 55/55 pass
- [x] Full unit suite: 3463 passed (2 deptry failures are environmental: worktree gitdir not resolvable from devcontainer — CI runs in clean checkout and won't hit this)
- [x] `ruff format --check` clean on changed files
- [x] `pyright app/` clean
- [ ] CI `build-and-test` + `auto-review` green


---

## c1f9b618 — feat(enterprise-admin): Phase G onboarding wizard (3-step) (#1812)

- **Author**: bill-srp
- **Date**: 2026-05-21T07:49:42Z

### Full Commit Message

```
feat(enterprise-admin): Phase G onboarding wizard (3-step) (#1812)

## Linear


https://linear.app/srpone/issue/ECA-771/admin-console-web-phase-1-org-settings

(Reusing the Org Settings issue since the wizard primarily creates +
configures an org. The wizard is the first-touch flow for a new admin;
Org Settings is the steady-state version of the same surface.)

## Summary

Phase 1.5 of the Enterprise Admin Console — 3-step onboarding wizard at
`/onboarding` per spec §8.5 + design-doc §3.5.

| Step | Inputs | API |
|------|--------|-----|
| 1. Org Setup | org name | `POST /orgs` |
| 2. Invite Team (Skip allowed) | bulk textarea `email, role, quota` per
line | `POST /orgs/{id}/invite` × N |
| 3. Warm Pool | pre-deployed count, auto-adjust checkbox | `POST
/orgs/{id}` |

Finish → `/users`.

## What ships

- **`lib/parse-bulk-invite.ts`** — robust line parser. Validates email
(basic `@.` shape), role (admin/user case-insensitive), quota
(non-negative integer). Collects errors per line without
short-circuiting so users see every problem at once.
- **`hooks/useOrg.ts`** — adds `useCreateOrgMutation`. Invalidates
`auth.currentUser` on success so the dashboard layout sees the new
membership and unblocks.
- **`components/onboarding/{StepIndicator, OrgSetupForm, BulkInviteForm,
WarmPoolForm}.tsx`** — pure controlled components. The parent VM owns
all form state, so step navigation preserves entry (no per-step
`useState` to lose).
- **`app/onboarding/{page.tsx, useOnboardingViewModel.ts}`** —
orchestrates the three steps + create-org + sequential bulk invites +
warm-pool update. MVVM convention.
- **`vitest.setup.ts`** — global ResizeObserver polyfill so Radix
`Checkbox` / `Dialog` / `AlertDialog` mount cleanly in jsdom without
per-test boilerplate.
- Gated behind `NEXT_PUBLIC_ONBOARDING_ENABLED` (default off → "coming
soon" panel, same pattern as D/E/F).

## Backend dependency + intentional security boundary

### `billing_team` is intentionally omitted (security)

`POST /orgs` backend `OrgCreateRequest` currently requires
`billing_team: { team_id, team_key }` from the client. `team_key` is a
billing-gateway credential that maps the org to a billing account —
**the frontend must never see, fabricate, or transit it through the
UI**. The wizard's `POST /orgs` body omits `billing_team` deliberately
and that posture stays.

The fix path is **backend-side**: the route handler should call
billing-gateway to provision a `billing_team` for the caller before
persisting the Org, then drop `billing_team` from the public request
shape. Until that lands the wizard is gated behind
`NEXT_PUBLIC_ONBOARDING_ENABLED` (default off), so `POST /orgs` doesn't
fire in production.

Codex's `REQUEST_CHANGES` on this PR ("create-org omits required
billing_team and will fail at runtime") correctly identifies the
symptom; the root fix is on the backend. Human reviewer override
expected.

### Invite endpoint

`POST /orgs/{org_id}/invite` (per PR #1792) accepts a batch shape
(`emails: string[]`). Phase 1 loops it per parsed line (one single-email
batch per line) since each line carries its own role + quota. A future
polish could group lines by `(role, quota)` for a smaller request count.

## Test plan

- [x] `pnpm test` — 157/157 (27 new across parser + hook + 4 components
+ page tests)
- [x] `pnpm exec tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm build` — clean; `/onboarding` prerendered as static
- [ ] Manual after backend ships: walk through all three steps with
valid data → land on `/users`
- [ ] Manual: skip step 2 → no invite calls fire → reach step 3
- [ ] Manual: paste mixed-validity bulk-invite text → see per-line error
rows + Send button disabled
```

### PR Description

## Linear

https://linear.app/srpone/issue/ECA-771/admin-console-web-phase-1-org-settings

(Reusing the Org Settings issue since the wizard primarily creates + configures an org. The wizard is the first-touch flow for a new admin; Org Settings is the steady-state version of the same surface.)

## Summary

Phase 1.5 of the Enterprise Admin Console — 3-step onboarding wizard at `/onboarding` per spec §8.5 + design-doc §3.5.

| Step | Inputs | API |
|------|--------|-----|
| 1. Org Setup | org name | `POST /orgs` |
| 2. Invite Team (Skip allowed) | bulk textarea `email, role, quota` per line | `POST /orgs/{id}/invite` × N |
| 3. Warm Pool | pre-deployed count, auto-adjust checkbox | `POST /orgs/{id}` |

Finish → `/users`.

## What ships

- **`lib/parse-bulk-invite.ts`** — robust line parser. Validates email (basic `@.` shape), role (admin/user case-insensitive), quota (non-negative integer). Collects errors per line without short-circuiting so users see every problem at once.
- **`hooks/useOrg.ts`** — adds `useCreateOrgMutation`. Invalidates `auth.currentUser` on success so the dashboard layout sees the new membership and unblocks.
- **`components/onboarding/{StepIndicator, OrgSetupForm, BulkInviteForm, WarmPoolForm}.tsx`** — pure controlled components. The parent VM owns all form state, so step navigation preserves entry (no per-step `useState` to lose).
- **`app/onboarding/{page.tsx, useOnboardingViewModel.ts}`** — orchestrates the three steps + create-org + sequential bulk invites + warm-pool update. MVVM convention.
- **`vitest.setup.ts`** — global ResizeObserver polyfill so Radix `Checkbox` / `Dialog` / `AlertDialog` mount cleanly in jsdom without per-test boilerplate.
- Gated behind `NEXT_PUBLIC_ONBOARDING_ENABLED` (default off → "coming soon" panel, same pattern as D/E/F).

## Backend dependency + intentional security boundary

### `billing_team` is intentionally omitted (security)

`POST /orgs` backend `OrgCreateRequest` currently requires `billing_team: { team_id, team_key }` from the client. `team_key` is a billing-gateway credential that maps the org to a billing account — **the frontend must never see, fabricate, or transit it through the UI**. The wizard's `POST /orgs` body omits `billing_team` deliberately and that posture stays.

The fix path is **backend-side**: the route handler should call billing-gateway to provision a `billing_team` for the caller before persisting the Org, then drop `billing_team` from the public request shape. Until that lands the wizard is gated behind `NEXT_PUBLIC_ONBOARDING_ENABLED` (default off), so `POST /orgs` doesn't fire in production.

Codex's `REQUEST_CHANGES` on this PR ("create-org omits required billing_team and will fail at runtime") correctly identifies the symptom; the root fix is on the backend. Human reviewer override expected.

### Invite endpoint

`POST /orgs/{org_id}/invite` (per PR #1792) accepts a batch shape (`emails: string[]`). Phase 1 loops it per parsed line (one single-email batch per line) since each line carries its own role + quota. A future polish could group lines by `(role, quota)` for a smaller request count.

## Test plan

- [x] `pnpm test` — 157/157 (27 new across parser + hook + 4 components + page tests)
- [x] `pnpm exec tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm build` — clean; `/onboarding` prerendered as static
- [ ] Manual after backend ships: walk through all three steps with valid data → land on `/users`
- [ ] Manual: skip step 2 → no invite calls fire → reach step 3
- [ ] Manual: paste mixed-validity bulk-invite text → see per-line error rows + Send button disabled


---

## d662dfc7 — ci(notify): wire release_actor + USER_MAPPING_JSON to release notify caller (#1803)

- **Author**: Chris@ZooClaw
- **Date**: 2026-05-21T07:45:51Z

### Full Commit Message

```
ci(notify): wire release_actor + USER_MAPPING_JSON to release notify caller (#1803)

## Summary

caller workflow 跟随
[srp-actions#82](https://github.com/SerendipityOneInc/srp-actions/pull/82)
reusable 升级，给 release 飞书通知接入按 PR merger / 发版人的 `<at>` @mention 数据源。

- `resolve` job ctx step 按 `event_name` 解析 `release_actor`：workflow_run
路径取 `workflow_run.actor.login`（按按钮触发上游 deploy 的人）；dispatch 路径取
`sender.login` 退一步 `github.actor`。
- `notify` job 透传两个新 input：`release_actor: ${{
needs.resolve.outputs.release_actor }}` + `user_mapping_json: ${{
vars.USER_MAPPING_JSON }}`（参照 `lark-notify-user.yml` 的 input 契约风格）。
- 同时落地 `docs/superpowers/specs/2026-05-21-release-通知mention改造.md` 描述完整 5
阶段改造、降级矩阵、合并顺序硬约束。

**`uses:` ref 当前临时指向**
`SerendipityOneInc/srp-actions/.github/workflows/release-notify-lark.yml@feat/release-notify-mention`
—— srp-actions#82 合并后会再 push 一次把 ref 改回 `@main`，参照 spec 阶段 5。

## Test plan

- [x] yaml 语法 check 通过 (yaml.safe_load)
- [x] 复用同仓 `lark-notify-user.yml` 的 `user_mapping_json` input 契约
- [ ] (待执行) workflow_dispatch + dry_run=true 跑历史 tag
(`ecap-v1.0.0-release` 之类)，CI log 验证：
    - `.pr-changelog.txt` 每个 PR 块顶部有 `Merged-by:` 行
    - `.pr-mentions.json` 结构正确（PR号 → merger / is_bot）
- `release-notes.md` 每条 bullet 末尾有 ` [#N]` marker、不同 merger 没被合并到一条
bullet
- `Inject Feishu @mentions` step 输出最终文本：顶部 `> 本次发版人 <at>...</at>`；bullet
末尾 marker 已替换为 `<at>` / `@<login>` / 静默吞掉
- [ ] (srp-actions#82 合并后) `uses:` ref 改回 `@main`，关 dry_run、保留
is_test=true，dispatch 真发一条到 review
群（`oc_213291d2715a9d02bf5b0bb18b847e3c`）肉眼验证飞书 client 渲染 `<at>` 为 "@姓名"
蓝色高亮 + 触发推送通知

## Merge order


[srp-actions#82](https://github.com/SerendipityOneInc/srp-actions/pull/82)
必须先合并；否则 caller 传 `release_actor` 给老 reusable 会触发 workflow validation
失败（unknown input）。本 PR hold 在 "指向 feature branch" 状态，等 srp-actions PR
合并后 push 一次 ref 改回 `@main` 再合并本 PR。

## Design spec

`docs/superpowers/specs/2026-05-21-release-通知mention改造.md`（本 PR 新增）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

caller workflow 跟随 [srp-actions#82](https://github.com/SerendipityOneInc/srp-actions/pull/82) reusable 升级，给 release 飞书通知接入按 PR merger / 发版人的 `<at>` @mention 数据源。

- `resolve` job ctx step 按 `event_name` 解析 `release_actor`：workflow_run 路径取 `workflow_run.actor.login`（按按钮触发上游 deploy 的人）；dispatch 路径取 `sender.login` 退一步 `github.actor`。
- `notify` job 透传两个新 input：`release_actor: ${{ needs.resolve.outputs.release_actor }}` + `user_mapping_json: ${{ vars.USER_MAPPING_JSON }}`（参照 `lark-notify-user.yml` 的 input 契约风格）。
- 同时落地 `docs/superpowers/specs/2026-05-21-release-通知mention改造.md` 描述完整 5 阶段改造、降级矩阵、合并顺序硬约束。

**`uses:` ref 当前临时指向** `SerendipityOneInc/srp-actions/.github/workflows/release-notify-lark.yml@feat/release-notify-mention` —— srp-actions#82 合并后会再 push 一次把 ref 改回 `@main`，参照 spec 阶段 5。

## Test plan

- [x] yaml 语法 check 通过 (yaml.safe_load)
- [x] 复用同仓 `lark-notify-user.yml` 的 `user_mapping_json` input 契约
- [ ] (待执行) workflow_dispatch + dry_run=true 跑历史 tag (`ecap-v1.0.0-release` 之类)，CI log 验证：
    - `.pr-changelog.txt` 每个 PR 块顶部有 `Merged-by:` 行
    - `.pr-mentions.json` 结构正确（PR号 → merger / is_bot）
    - `release-notes.md` 每条 bullet 末尾有 ` [#N]` marker、不同 merger 没被合并到一条 bullet
    - `Inject Feishu @mentions` step 输出最终文本：顶部 `> 本次发版人 <at>...</at>`；bullet 末尾 marker 已替换为 `<at>` / `@<login>` / 静默吞掉
- [ ] (srp-actions#82 合并后) `uses:` ref 改回 `@main`，关 dry_run、保留 is_test=true，dispatch 真发一条到 review 群（`oc_213291d2715a9d02bf5b0bb18b847e3c`）肉眼验证飞书 client 渲染 `<at>` 为 "@姓名" 蓝色高亮 + 触发推送通知

## Merge order

[srp-actions#82](https://github.com/SerendipityOneInc/srp-actions/pull/82) 必须先合并；否则 caller 传 `release_actor` 给老 reusable 会触发 workflow validation 失败（unknown input）。本 PR hold 在 "指向 feature branch" 状态，等 srp-actions PR 合并后 push 一次 ref 改回 `@main` 再合并本 PR。

## Design spec

`docs/superpowers/specs/2026-05-21-release-通知mention改造.md`（本 PR 新增）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 822ce371 — docs(spec): backfill 个人化通知改造 跨仓 rollout 状态 (#1814)

- **Author**: Chris@ZooClaw
- **Date**: 2026-05-21T07:30:28Z

### Full Commit Message

```
docs(spec): backfill 个人化通知改造 跨仓 rollout 状态 (#1814)

## Summary

仅文档变更，无代码改动。本 PR 把 `docs/superpowers/specs/2026-05-20-个人化通知改造.md` 跟现实对齐：

- 修正两条已 merged 但还写"in flight"的旧 PR 状态：4.b 升级为 `merged #1798`，6.b 升级为
`merged #1810`
- 决策表里把 ecap-workspace 之外的 4 个仓显式列入：billing-gateway / ecap-proxy-service
/ fastclaw / zooclaw-extras（zooclaw-extras 评估为不动）
- PR 拆分表加 7.a / 7.b / 7.c（Phase 1 已 merged）+ 7.d / 7.e（Phase 2 in
flight）

## 改前/改后

决策表新增 12 行（涵盖 4 个外仓的所有 workflow + 通知去向）；PR 拆分表把 4.b / 6.b 改成 merged 并新增
5 行 7.a-7.e。

## 不需要 Test plan

文档改动，不影响 CI / 部署 / 通知行为。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

仅文档变更，无代码改动。本 PR 把 `docs/superpowers/specs/2026-05-20-个人化通知改造.md` 跟现实对齐：

- 修正两条已 merged 但还写"in flight"的旧 PR 状态：4.b 升级为 `merged #1798`，6.b 升级为 `merged #1810`
- 决策表里把 ecap-workspace 之外的 4 个仓显式列入：billing-gateway / ecap-proxy-service / fastclaw / zooclaw-extras（zooclaw-extras 评估为不动）
- PR 拆分表加 7.a / 7.b / 7.c（Phase 1 已 merged）+ 7.d / 7.e（Phase 2 in flight）

## 改前/改后

决策表新增 12 行（涵盖 4 个外仓的所有 workflow + 通知去向）；PR 拆分表把 4.b / 6.b 改成 merged 并新增 5 行 7.a-7.e。

## 不需要 Test plan

文档改动，不影响 CI / 部署 / 通知行为。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 7036417b — test(chat): add useChatMessaging spec, clean stale lint overrides (#1813)

- **Author**: Chris@ZooClaw
- **Date**: 2026-05-21T07:17:59Z

### Full Commit Message

```
test(chat): add useChatMessaging spec, clean stale lint overrides (#1813)

## Summary

Follow-up to #1799 (GenClawClient refactor):

- **New unit spec** `tests/unit/app/chat/useChatMessaging.unit.spec.ts`
(14 tests) covering the invariants this hook now owns:
- `handleAbort` 300ms re-entrancy guard + `/stop` failure → warning
toast
- `handleSendMessage` error classification: `MattermostError` w/
`MM_ERROR_CODE_MESSAGE_TOO_LONG` → `logger.warn` only (no Sentry); other
errors → `captureChatError` + toast
- `displayMessages` sticky cache: keeps last MM snapshot when MM drops,
clears on agent switch (prevents cross-agent message bleed)
- `mm.error` toast effect: fires only while `mmConnected` (no spam
during reconnect storms)
  - `effectiveIsGenerating` mirrors `mm.isWaitingForBotReply`
- **Clean dead entry** in `web/app/eslint.config.mjs` legacy-complexity
override list: `useOpenClawChat.ts` no longer exists (renamed/split
during the refactor).
- **Correct stale note** in `web/app/AGENTS.md`: `GenClawClient` is now
a function component; the actual remaining class holdouts are
`ErrorBoundary`, `ChatErrorBoundary`, and `AssistantUiTapErrorBoundary`
(React 19 still requires class components for error boundaries).

Mocks `useMattermostIntegration` / `useOpenClawRuntime` /
`useStableConnectionStatus` / `abortMattermostGeneration` at the
dependency boundary so the spec stays focused on this hook's own logic
(the underlying hooks already have their own dedicated specs).

## Test plan

- [x] \`pnpm exec vitest run
tests/unit/app/chat/useChatMessaging.unit.spec.ts\` — 14/14 pass
- [x] \`pnpm exec eslint\` — clean on touched files
- [x] \`pnpm exec tsc --noEmit\` — clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Follow-up to #1799 (GenClawClient refactor):

- **New unit spec** `tests/unit/app/chat/useChatMessaging.unit.spec.ts` (14 tests) covering the invariants this hook now owns:
  - `handleAbort` 300ms re-entrancy guard + `/stop` failure → warning toast
  - `handleSendMessage` error classification: `MattermostError` w/ `MM_ERROR_CODE_MESSAGE_TOO_LONG` → `logger.warn` only (no Sentry); other errors → `captureChatError` + toast
  - `displayMessages` sticky cache: keeps last MM snapshot when MM drops, clears on agent switch (prevents cross-agent message bleed)
  - `mm.error` toast effect: fires only while `mmConnected` (no spam during reconnect storms)
  - `effectiveIsGenerating` mirrors `mm.isWaitingForBotReply`
- **Clean dead entry** in `web/app/eslint.config.mjs` legacy-complexity override list: `useOpenClawChat.ts` no longer exists (renamed/split during the refactor).
- **Correct stale note** in `web/app/AGENTS.md`: `GenClawClient` is now a function component; the actual remaining class holdouts are `ErrorBoundary`, `ChatErrorBoundary`, and `AssistantUiTapErrorBoundary` (React 19 still requires class components for error boundaries).

Mocks `useMattermostIntegration` / `useOpenClawRuntime` / `useStableConnectionStatus` / `abortMattermostGeneration` at the dependency boundary so the spec stays focused on this hook's own logic (the underlying hooks already have their own dedicated specs).

## Test plan

- [x] \`pnpm exec vitest run tests/unit/app/chat/useChatMessaging.unit.spec.ts\` — 14/14 pass
- [x] \`pnpm exec eslint\` — clean on touched files
- [x] \`pnpm exec tsc --noEmit\` — clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## d87cbd17 — feat(enterprise): /orgs/{org_id}/users routes + invite email (#1792)

- **Author**: bill-srp
- **Date**: 2026-05-21T06:54:52Z

### Full Commit Message

```
feat(enterprise): /orgs/{org_id}/users routes + invite email (#1792)

**Linear:**
https://linear.app/srpone/issue/ECA-764/phase-1-backend-changes-enterprise-data-model-warm-pool-cross-service

## Summary

Phase 1 enterprise user-management HTTP surface — five endpoints on top
of the membership service from PR-3, plus EngageLab invite-email
delivery and a meaningful simplification of the membership lifecycle.

**Routes (`app/routes/enterprise/users.py`):**

| Method | Path | Auth |
|---|---|---|
| POST | `/orgs/{org_id}/invite` | admin — batch (1–100 emails) |
| POST | `/orgs/{org_id}/join` | authenticated user |
| GET  | `/orgs/{org_id}/users` | member |
| POST | `/orgs/{org_id}/users/{uid}/suspend` | admin |
| POST | `/orgs/{org_id}/users/{uid}/resume` | admin |

`POST .../remove` is deliberately not in Phase 1 — `/suspend` +
`/resume` cover the admin lifecycle. A hard-remove path can land when
cross-org transitions are needed.

**Invite path:**
- Batch shape: `{emails: [...], role, computer_quota}` → `{invites,
duplicates, errors}`. Role + quota apply to all entries. Emails
normalized + deduped at the Pydantic boundary (case-insensitive,
whitespace-stripped) so the partial-unique `(invited_email, org_id)`
index sees one canonical form.
- Pre-filter rejects only when **all** submitted emails already have
active invites (pending or redeemed) → 409. Partial overlap proceeds;
filtered ones surface in `duplicates`.
- Code entropy: 128 bits (`secrets.token_hex(16).upper()` → 32 hex
chars). DB lookup is the only validation; no HMAC layer.
- Delivery via EngageLab `/mail/sendtemplate` in a `BackgroundTask` —
exception-swallowing, PII-masked logs (`mask_email()`), silent skip when
`ENGAGELAB_*` settings are unset so dev/CI never need credentials.

**Join path:**
- Route enforces (a) invite resolves, (b) `invite.org_id == path org_id`
(defense-in-depth), (c) `account.email == invite.invited_email`. Service
takes the typed `OrgInvite` to avoid duplicate `get_by_code`.
- Strict single-membership: any prior `account_org` row (active /
suspended / pending, this org or another) → 409 `org.already_a_member`.
No more idempotent re-join, no personal→team auto-suspend. Suspended
users are recovered via admin `/resume`.

**Suspend / resume:**
- Single atomic `find_one_and_update` per call. Returns the post-update
row or `None` (→ 404). Pre-check read eliminated.

**Service contract:**
- `membership_service.invite_users` returns a plain
`tuple[list[OrgInvite], list[str], list[str]]` so internal callers
aren't forced to materialize an HTTP response shape.

**Security review (independent pass):** clean except H1 (full invite
code in compensation logs) — fixed in `8e273cf8` by wrapping with
`safe_short_id`.

## Test plan

- [x] 76+ unit tests across affected files (schema, repo, service,
route, email) — all green
- [x] Full unit suite — 3422 pass (2 pre-existing deptry env-only
failures, unchanged from main)
- [x] `ruff check` on all touched files — clean
- [x] `pyright` on all touched files — 0 errors
- [x] `lint-imports` — 8/8 contracts kept (`app.services.email`
correctly above the data layer, fastapi-free)
- [x] `deptry app tests` — no dependency issues (httpx already in
requirements)
- [x] Coverage: 88% project-wide (no CI gate); new modules
`invite_email.py`, `users.py` exercise every branch
- [x] Independent code review pass — H1 patched, M1-M3 / L1-L3 deferred
(perf + cosmetic)
- [ ] Frontend (`enterprise-admin/`, `web/`) impact: list-users response
shape changed (`{users, total, quota_used, quota_total}` → bare
`[...]`), `/users/{uid}/remove` removed, join path moved to
`/orgs/{org_id}/join`. Out of scope for this PR; flag for downstream
PRs.
- [ ] BDD: `org_lifecycle.feature` step defs (S1-17) still pending —
`.feature` itself now matches the implemented behavior

## Out of scope (deferred)

- BDD step defs for `org_lifecycle.feature` (S1-17)
- V2 user routes (§3.6) — the `/v2/users/me` line was removed from the
BDD feature for this reason
- Hard-remove endpoint
- Quota summarization (`quota_used` / `quota_total`) — requires org-tier
model
- HMAC-signed invite codes (entropy alone is sufficient at 128 bits per
the security review)
```

### PR Description

**Linear:** https://linear.app/srpone/issue/ECA-764/phase-1-backend-changes-enterprise-data-model-warm-pool-cross-service

## Summary

Phase 1 enterprise user-management HTTP surface — five endpoints on top of the membership service from PR-3, plus EngageLab invite-email delivery and a meaningful simplification of the membership lifecycle.

**Routes (`app/routes/enterprise/users.py`):**

| Method | Path | Auth |
|---|---|---|
| POST | `/orgs/{org_id}/invite` | admin — batch (1–100 emails) |
| POST | `/orgs/{org_id}/join` | authenticated user |
| GET  | `/orgs/{org_id}/users` | member |
| POST | `/orgs/{org_id}/users/{uid}/suspend` | admin |
| POST | `/orgs/{org_id}/users/{uid}/resume` | admin |

`POST .../remove` is deliberately not in Phase 1 — `/suspend` + `/resume` cover the admin lifecycle. A hard-remove path can land when cross-org transitions are needed.

**Invite path:**
- Batch shape: `{emails: [...], role, computer_quota}` → `{invites, duplicates, errors}`. Role + quota apply to all entries. Emails normalized + deduped at the Pydantic boundary (case-insensitive, whitespace-stripped) so the partial-unique `(invited_email, org_id)` index sees one canonical form.
- Pre-filter rejects only when **all** submitted emails already have active invites (pending or redeemed) → 409. Partial overlap proceeds; filtered ones surface in `duplicates`.
- Code entropy: 128 bits (`secrets.token_hex(16).upper()` → 32 hex chars). DB lookup is the only validation; no HMAC layer.
- Delivery via EngageLab `/mail/sendtemplate` in a `BackgroundTask` — exception-swallowing, PII-masked logs (`mask_email()`), silent skip when `ENGAGELAB_*` settings are unset so dev/CI never need credentials.

**Join path:**
- Route enforces (a) invite resolves, (b) `invite.org_id == path org_id` (defense-in-depth), (c) `account.email == invite.invited_email`. Service takes the typed `OrgInvite` to avoid duplicate `get_by_code`.
- Strict single-membership: any prior `account_org` row (active / suspended / pending, this org or another) → 409 `org.already_a_member`. No more idempotent re-join, no personal→team auto-suspend. Suspended users are recovered via admin `/resume`.

**Suspend / resume:**
- Single atomic `find_one_and_update` per call. Returns the post-update row or `None` (→ 404). Pre-check read eliminated.

**Service contract:**
- `membership_service.invite_users` returns a plain `tuple[list[OrgInvite], list[str], list[str]]` so internal callers aren't forced to materialize an HTTP response shape.

**Security review (independent pass):** clean except H1 (full invite code in compensation logs) — fixed in `8e273cf8` by wrapping with `safe_short_id`.

## Test plan

- [x] 76+ unit tests across affected files (schema, repo, service, route, email) — all green
- [x] Full unit suite — 3422 pass (2 pre-existing deptry env-only failures, unchanged from main)
- [x] `ruff check` on all touched files — clean
- [x] `pyright` on all touched files — 0 errors
- [x] `lint-imports` — 8/8 contracts kept (`app.services.email` correctly above the data layer, fastapi-free)
- [x] `deptry app tests` — no dependency issues (httpx already in requirements)
- [x] Coverage: 88% project-wide (no CI gate); new modules `invite_email.py`, `users.py` exercise every branch
- [x] Independent code review pass — H1 patched, M1-M3 / L1-L3 deferred (perf + cosmetic)
- [ ] Frontend (`enterprise-admin/`, `web/`) impact: list-users response shape changed (`{users, total, quota_used, quota_total}` → bare `[...]`), `/users/{uid}/remove` removed, join path moved to `/orgs/{org_id}/join`. Out of scope for this PR; flag for downstream PRs.
- [ ] BDD: `org_lifecycle.feature` step defs (S1-17) still pending — `.feature` itself now matches the implemented behavior

## Out of scope (deferred)

- BDD step defs for `org_lifecycle.feature` (S1-17)
- V2 user routes (§3.6) — the `/v2/users/me` line was removed from the BDD feature for this reason
- Hard-remove endpoint
- Quota summarization (`quota_used` / `quota_total`) — requires org-tier model
- HMAC-signed invite codes (entropy alone is sufficient at 128 bits per the security review)


---

## e2b9eff8 — feat(enterprise-admin): Phase F Org Settings page (#1811)

- **Author**: bill-srp
- **Date**: 2026-05-21T06:44:00Z

### Full Commit Message

```
feat(enterprise-admin): Phase F Org Settings page (#1811)

## Linear


https://linear.app/srpone/issue/ECA-771/admin-console-web-phase-1-org-settings

## Summary

Phase 1.4 of the Enterprise Admin Console — the **Org Settings** page
(spec §8.4 + design-doc §3.4).

### What ships

- **`hooks/useOrg.ts`** — `useOrgQuery(orgId)` +
`useUpdateOrgMutation(orgId)`. URL-encoded `orgId` paths. The mutation
invalidates BOTH `["org", orgId]` AND `["auth", "currentUser"]` so an
org name rename propagates to the dashboard TopBar (which sources name
from `useAuth().org.name`) without a page reload.
- **`types/org.ts`** — adds optional `name?` to `OrgUpdateRequest`
(frontend now sends `name` as part of the PATCH; backend
`OrgUpdateRequest` schema may need the same field).
- **`app/(dashboard)/org/page.tsx`** + **`useOrgSettingsViewModel.ts`**
— replaces the placeholder. Form with editable name + 3 quotas,
read-only org_type + created_at. Save/Discard buttons enabled only when
dirty. MVVM convention.

### Form-state pattern (no useEffect)

The VM tracks **only user overrides** on top of the live query baseline
rather than copying server data into form state via useEffect. This
avoids Next 16's `react-hooks/set-state-in-effect` rule (same constraint
we navigated in Phase B's auth refactor) and means dirty-tracking
naturally clears after a successful refetch — no manual sync. When the
mutation succeeds, `onSuccess` clears overrides and the form snaps to
the fresh baseline.

### Feature gating

Gated behind `NEXT_PUBLIC_ORG_MODULE_ENABLED`. Default off → "coming
soon" panel, same pattern as Phase D/E/D.5.

### Backend status — closer to ready than Users/Packs

`GET /orgs/{orgId}` and `POST /orgs/{orgId}` already exist in
`services/claw-interface/app/routes/enterprise/org.py` (shipped in
#1748). The only verification needed before flipping the flag: confirm
the backend `OrgUpdateRequest` Pydantic schema accepts `name`. If it
doesn't, that's a small backend change.

## Test plan

- [x] `pnpm test` — 130/130 (12 new across hook + page tests)
- [x] `pnpm exec tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm build` — clean; `/org` route prerendered as static
- [ ] Manual after backend verified: flip flag → load `/org` as admin →
edit name → see Save enable → click Save → see Saved confirmation → see
TopBar refresh with new org name
- [ ] Manual: edit then Discard → form reverts to baseline
- [ ] Manual as `role=user`: `/org` redirects to `/users` (existing
dashboard layout guard)
```

### PR Description

## Linear

https://linear.app/srpone/issue/ECA-771/admin-console-web-phase-1-org-settings

## Summary

Phase 1.4 of the Enterprise Admin Console — the **Org Settings** page (spec §8.4 + design-doc §3.4).

### What ships

- **`hooks/useOrg.ts`** — `useOrgQuery(orgId)` + `useUpdateOrgMutation(orgId)`. URL-encoded `orgId` paths. The mutation invalidates BOTH `["org", orgId]` AND `["auth", "currentUser"]` so an org name rename propagates to the dashboard TopBar (which sources name from `useAuth().org.name`) without a page reload.
- **`types/org.ts`** — adds optional `name?` to `OrgUpdateRequest` (frontend now sends `name` as part of the PATCH; backend `OrgUpdateRequest` schema may need the same field).
- **`app/(dashboard)/org/page.tsx`** + **`useOrgSettingsViewModel.ts`** — replaces the placeholder. Form with editable name + 3 quotas, read-only org_type + created_at. Save/Discard buttons enabled only when dirty. MVVM convention.

### Form-state pattern (no useEffect)

The VM tracks **only user overrides** on top of the live query baseline rather than copying server data into form state via useEffect. This avoids Next 16's `react-hooks/set-state-in-effect` rule (same constraint we navigated in Phase B's auth refactor) and means dirty-tracking naturally clears after a successful refetch — no manual sync. When the mutation succeeds, `onSuccess` clears overrides and the form snaps to the fresh baseline.

### Feature gating

Gated behind `NEXT_PUBLIC_ORG_MODULE_ENABLED`. Default off → "coming soon" panel, same pattern as Phase D/E/D.5.

### Backend status — closer to ready than Users/Packs

`GET /orgs/{orgId}` and `POST /orgs/{orgId}` already exist in `services/claw-interface/app/routes/enterprise/org.py` (shipped in #1748). The only verification needed before flipping the flag: confirm the backend `OrgUpdateRequest` Pydantic schema accepts `name`. If it doesn't, that's a small backend change.

## Test plan

- [x] `pnpm test` — 130/130 (12 new across hook + page tests)
- [x] `pnpm exec tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm build` — clean; `/org` route prerendered as static
- [ ] Manual after backend verified: flip flag → load `/org` as admin → edit name → see Save enable → click Save → see Saved confirmation → see TopBar refresh with new org name
- [ ] Manual: edit then Discard → form reverts to baseline
- [ ] Manual as `role=user`: `/org` redirects to `/users` (existing dashboard layout guard)

---

## 63c77808 — ci(notify): web/enterprise-admin/claw-interface 失败切个人私信 (#1810)

- **Author**: Chris@ZooClaw
- **Date**: 2026-05-21T06:44:39Z

### Full Commit Message

```
ci(notify): web/enterprise-admin/claw-interface 失败切个人私信 (#1810)

## Summary

- 把 `web-quality` / `enterprise-admin-quality` /
`claw-interface-quality` 三个 caller 的失败通知从 `FEISHU_CUSTOMERBOT_WEBHOOK`
群组改为个人私信（通过新版 reusable 的 `notify_target: author`）
- 映射缺失 / `vars.NOTIFY_INDIVIDUAL_ENABLED=false` 时降级到
`oc_213291d2715a9d02bf5b0bb18b847e3c` 群（与 iOS
`notify-ios-author-on-failure` 共用同一回退群）
- 更新 `docs/superpowers/specs/2026-05-20-个人化通知改造.md` 记录 PR 6.a / 6.b 拆分

## 依赖

✅ **SerendipityOneInc/srp-actions#83** 已 merge。

## Test plan

- [x] srp-actions#83 合到 main 后 rerun 本 PR 的 CI，确认 caller 解析通过 — run
26209006818 rerun success
- [x] 故意搞坏 web lint（`__notify_test__.ts` 加 TS 类型错）→ 推 commit → PR
作者收到飞书私信，带 `Lint & Type Check: ❌ FAIL / Tests: ✅ PASS` 明细 — run
26209677235 + 26209845588 各发一条 DM
- [x] 故意搞坏 claw-interface 的 ruff 规则（`__notify_test__.py` 加 F401 unused
import）→ 私信到达，文案为 Python 模板 — run 26209845588 一条 Python DM
- [ ] 临时设 `vars.NOTIFY_INDIVIDUAL_ENABLED=false` → 失败时退回到 fallback
群组，消息前缀含 `[通知开关关闭]` — **跳过**：会影响其他正在跑的 caller PR，列为未来 rollback 演练
- [x] 群组里应**不再**收到 `web-code-quality-v1` / `python-code-quality-v3`
模板的失败播报 — 验证期间手工核实

## 回滚

- 软回滚：设 `vars.NOTIFY_INDIVIDUAL_ENABLED=false`（所有 caller 退回群通知）
- 硬回滚：revert 本 PR，reusable 默认 `notify_target=group` 自然落回群通知

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

- 把 `web-quality` / `enterprise-admin-quality` / `claw-interface-quality` 三个 caller 的失败通知从 `FEISHU_CUSTOMERBOT_WEBHOOK` 群组改为个人私信（通过新版 reusable 的 `notify_target: author`）
- 映射缺失 / `vars.NOTIFY_INDIVIDUAL_ENABLED=false` 时降级到 `oc_213291d2715a9d02bf5b0bb18b847e3c` 群（与 iOS `notify-ios-author-on-failure` 共用同一回退群）
- 更新 `docs/superpowers/specs/2026-05-20-个人化通知改造.md` 记录 PR 6.a / 6.b 拆分

## 依赖

✅ **SerendipityOneInc/srp-actions#83** 已 merge。

## Test plan

- [x] srp-actions#83 合到 main 后 rerun 本 PR 的 CI，确认 caller 解析通过 — run 26209006818 rerun success
- [x] 故意搞坏 web lint（`__notify_test__.ts` 加 TS 类型错）→ 推 commit → PR 作者收到飞书私信，带 `Lint & Type Check: ❌ FAIL / Tests: ✅ PASS` 明细 — run 26209677235 + 26209845588 各发一条 DM
- [x] 故意搞坏 claw-interface 的 ruff 规则（`__notify_test__.py` 加 F401 unused import）→ 私信到达，文案为 Python 模板 — run 26209845588 一条 Python DM
- [ ] 临时设 `vars.NOTIFY_INDIVIDUAL_ENABLED=false` → 失败时退回到 fallback 群组，消息前缀含 `[通知开关关闭]` — **跳过**：会影响其他正在跑的 caller PR，列为未来 rollback 演练
- [x] 群组里应**不再**收到 `web-code-quality-v1` / `python-code-quality-v3` 模板的失败播报 — 验证期间手工核实

## 回滚

- 软回滚：设 `vars.NOTIFY_INDIVIDUAL_ENABLED=false`（所有 caller 退回群通知）
- 硬回滚：revert 本 PR，reusable 默认 `notify_target=group` 自然落回群通知

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 285df91b — refactor(chat): split GenClawClient controllers (#1799)

- **Author**: Chris@ZooClaw
- **Date**: 2026-05-21T06:27:47Z

### Full Commit Message

```
refactor(chat): split GenClawClient controllers (#1799)

## Summary
- split GenClawClient control logic into focused chat hooks
- extract reusable chat modal/error/subagent rail components
- remove dead profile greeting and unreachable channel read-only code
- add refactor design spec

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web run tsc (blocked by current script passing
--if-present to pnpm exec; validated each workspace with tsc --noEmit
instead)
- [x] pnpm --dir web run test:unit
- [x] focused chat vitest suite
```

### PR Description

## Summary
- split GenClawClient control logic into focused chat hooks
- extract reusable chat modal/error/subagent rail components
- remove dead profile greeting and unreachable channel read-only code
- add refactor design spec

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web run tsc (blocked by current script passing --if-present to pnpm exec; validated each workspace with tsc --noEmit instead)
- [x] pnpm --dir web run test:unit
- [x] focused chat vitest suite

---

## b6327a6d — fix(web): bust browser cache for artifact iframe when content changes (#1805)

- **Author**: siqiao-srp
- **Date**: 2026-05-21T06:17:13Z

### Full Commit Message

```
fix(web): bust browser cache for artifact iframe when content changes (#1805)

## Summary

- **Root cause**: When a bot modifies an artifact HTML file (e.g.
`alt-pokemon-terminal.html`), the URL stays the same
(`https://artifacts.zooclaw.ai/{bot_id}/artifacts/file.html`). Even
though the frontend correctly detects the new message and remounts the
iframe, the **browser's HTTP cache** serves stale content for the same
URL. The user sees old content in the artifact panel while opening the
URL directly in a new tab shows the updated version.
- **Fix**: `HtmlRenderer` now appends `?_cb=<timestamp>` to artifact
proxy URLs on mount. This is safe because the proxy URL is not presigned
— the proxy generates a fresh presigned S3 redirect on each request, so
the `_cb` param never reaches S3. Non-artifact URLs (presigned S3,
external) are left untouched, guarded by the existing `isArtifactUrl()`
check.
- Updated the comment in `ArtifactPreview.tsx` to document the new
cache-busting strategy.
- Added 3 unit tests for `HtmlRenderer`.

Closes ECA-769

## Test plan

- [x] `HtmlRenderer.unit.spec.tsx` — 3 tests:
  - Appends `_cb` param to prod artifact proxy URLs
  - Appends `_cb` param to staging artifact proxy URLs
  - Does NOT append to non-artifact URLs (presigned S3)
- [x] All 99 existing artifact tests pass (7 files)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```

### PR Description

## Summary

- **Root cause**: When a bot modifies an artifact HTML file (e.g. `alt-pokemon-terminal.html`), the URL stays the same (`https://artifacts.zooclaw.ai/{bot_id}/artifacts/file.html`). Even though the frontend correctly detects the new message and remounts the iframe, the **browser's HTTP cache** serves stale content for the same URL. The user sees old content in the artifact panel while opening the URL directly in a new tab shows the updated version.
- **Fix**: `HtmlRenderer` now appends `?_cb=<timestamp>` to artifact proxy URLs on mount. This is safe because the proxy URL is not presigned — the proxy generates a fresh presigned S3 redirect on each request, so the `_cb` param never reaches S3. Non-artifact URLs (presigned S3, external) are left untouched, guarded by the existing `isArtifactUrl()` check.
- Updated the comment in `ArtifactPreview.tsx` to document the new cache-busting strategy.
- Added 3 unit tests for `HtmlRenderer`.

Closes ECA-769

## Test plan

- [x] `HtmlRenderer.unit.spec.tsx` — 3 tests:
  - Appends `_cb` param to prod artifact proxy URLs
  - Appends `_cb` param to staging artifact proxy URLs
  - Does NOT append to non-artifact URLs (presigned S3)
- [x] All 99 existing artifact tests pass (7 files)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 9f7db513 — fix(web): remove stale agent pending sync (#1779)

- **Author**: Chris@ZooClaw
- **Date**: 2026-05-21T06:16:13Z

### Full Commit Message

```
fix(web): remove stale agent pending sync (#1779)

## Summary
- Remove the AGENTS_PENDING_SYNC localStorage replay mechanism so agent
refreshes can no longer write stale local lists back to the backend.
- Make onboarding companion hire call the backend directly and refresh
the real agents cache instead of writing a fake AGENTS_CACHE entry.
- Update unit coverage around refresh, retry failure, and onboarding
companion hire behavior.

## Root cause
Frontend localStorage was still treated as a writable recovery source:
refreshUserAgentsCache consumed AGENTS_PENDING_SYNC and replayed saved
agent IDs to the backend, while onboarding wrote a synthetic
AGENTS_CACHE and queued that list for later sync. That could let stale
browser state overwrite the MongoDB-backed selected_agent_ids state.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web run test:unit
- [x] cd web/app && pnpm exec tsc --noEmit
- [x] targeted eslint for touched files

Fixes #437
```

### PR Description

## Summary
- Remove the AGENTS_PENDING_SYNC localStorage replay mechanism so agent refreshes can no longer write stale local lists back to the backend.
- Make onboarding companion hire call the backend directly and refresh the real agents cache instead of writing a fake AGENTS_CACHE entry.
- Update unit coverage around refresh, retry failure, and onboarding companion hire behavior.

## Root cause
Frontend localStorage was still treated as a writable recovery source: refreshUserAgentsCache consumed AGENTS_PENDING_SYNC and replayed saved agent IDs to the backend, while onboarding wrote a synthetic AGENTS_CACHE and queued that list for later sync. That could let stale browser state overwrite the MongoDB-backed selected_agent_ids state.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web run test:unit
- [x] cd web/app && pnpm exec tsc --noEmit
- [x] targeted eslint for touched files

Fixes #437

---

## b3f2c8a3 — feat(enterprise-admin): invite landing page + acceptance flow (#1808)

- **Author**: bill-srp
- **Date**: 2026-05-21T06:00:08Z

### Full Commit Message

```
feat(enterprise-admin): invite landing page + acceptance flow (#1808)

## Linear


https://linear.app/srpone/issue/ECA-749/admin-console-web-phase-1-users-module

Completes the user-onboarding loop missing from Phase D (the admin-side
invite send shipped, but invitees had no way to actually join).

## Summary

When a user clicks the invite link from their email (e.g.
`https://admin.zooclaw.ai/invite/abc123`), they now land on a real page
that previews the invite, gates on auth, and lets them accept in one
click.

### What ships (frontend only)

- **`hooks/useInvite.ts`** — `useInviteInfoQuery(code)` previews the
invite; `useAcceptInviteMutation(code)` redeems it. Both URL-encode the
code. On success the mutation invalidates `["auth", "currentUser"]` so
the dashboard layout sees the new membership and unblocks.
- **`app/invite/[code]/page.tsx`** + **`useInviteLandingViewModel.ts`**
— top-level route (NOT under `(dashboard)/` so the no-org redirect
doesn't intercept). Five view states with specific copy per HTTP error
code (404 / 410 / 409 / 403). MVVM convention.
- **`app/useEntryViewModel.ts`** updated — pops a `sessionStorage`
`pending_invite_code` after OTP verify and routes back to
`/invite/{code}`, so the before-login → sign-in → return loop works.
- **`types/invite.ts`** — `InvitePreview` shape.

### Spec update


`docs/superpowers/specs/2026-05-19-enterprise-admin-console-frontend.md`:
- §6.4 — Invite hooks subsection
- §6.5 — Invite-acceptance API table
- §8.8 — new wireframe + flow description

## Backend dependency (not in this PR)

The two endpoints called by the new hooks aren't yet wired in
`services/claw-interface`. The service layer already exists from #1771
(`membership_service.join_org`); only thin route handlers need adding:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v2/invites/{code}` | Returns `{ org_id, org_name, role,
computer_quota, invited_email, expires_at }` |
| `POST` | `/v2/invites/{code}/accept` | Wraps
`membership_service.join_org(code, uid=caller)` |

A separate backend PR will add these. Until that lands, the Accept
button will 404 — but the UI gracefully shows the right error copy.

## Test plan

- [x] `pnpm test` — 117/117 (8 new across hook + page + entry-VM tests)
- [x] `pnpm exec tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm build` — clean; `/invite/[code]` registered as dynamic route
- [ ] Manual after backend ships: paste an invite URL while logged out →
click Sign in → OTP login → land back on `/invite/{code}` → Accept → see
`/users`
- [ ] Manual: paste an invite URL while logged in (same email) → preview
shows → Accept → routes to `/users`
- [ ] Manual: paste an invite URL while logged in (different email) →
403 "different account" copy
- [ ] Manual: paste an expired/used invite URL → 410/409 copy
```

### PR Description

## Linear

https://linear.app/srpone/issue/ECA-749/admin-console-web-phase-1-users-module

Completes the user-onboarding loop missing from Phase D (the admin-side invite send shipped, but invitees had no way to actually join).

## Summary

When a user clicks the invite link from their email (e.g. `https://admin.zooclaw.ai/invite/abc123`), they now land on a real page that previews the invite, gates on auth, and lets them accept in one click.

### What ships (frontend only)

- **`hooks/useInvite.ts`** — `useInviteInfoQuery(code)` previews the invite; `useAcceptInviteMutation(code)` redeems it. Both URL-encode the code. On success the mutation invalidates `["auth", "currentUser"]` so the dashboard layout sees the new membership and unblocks.
- **`app/invite/[code]/page.tsx`** + **`useInviteLandingViewModel.ts`** — top-level route (NOT under `(dashboard)/` so the no-org redirect doesn't intercept). Five view states with specific copy per HTTP error code (404 / 410 / 409 / 403). MVVM convention.
- **`app/useEntryViewModel.ts`** updated — pops a `sessionStorage` `pending_invite_code` after OTP verify and routes back to `/invite/{code}`, so the before-login → sign-in → return loop works.
- **`types/invite.ts`** — `InvitePreview` shape.

### Spec update

`docs/superpowers/specs/2026-05-19-enterprise-admin-console-frontend.md`:
- §6.4 — Invite hooks subsection
- §6.5 — Invite-acceptance API table
- §8.8 — new wireframe + flow description

## Backend dependency (not in this PR)

The two endpoints called by the new hooks aren't yet wired in `services/claw-interface`. The service layer already exists from #1771 (`membership_service.join_org`); only thin route handlers need adding:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/v2/invites/{code}` | Returns `{ org_id, org_name, role, computer_quota, invited_email, expires_at }` |
| `POST` | `/v2/invites/{code}/accept` | Wraps `membership_service.join_org(code, uid=caller)` |

A separate backend PR will add these. Until that lands, the Accept button will 404 — but the UI gracefully shows the right error copy.

## Test plan

- [x] `pnpm test` — 117/117 (8 new across hook + page + entry-VM tests)
- [x] `pnpm exec tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm build` — clean; `/invite/[code]` registered as dynamic route
- [ ] Manual after backend ships: paste an invite URL while logged out → click Sign in → OTP login → land back on `/invite/{code}` → Accept → see `/users`
- [ ] Manual: paste an invite URL while logged in (same email) → preview shows → Accept → routes to `/users`
- [ ] Manual: paste an invite URL while logged in (different email) → 403 "different account" copy
- [ ] Manual: paste an expired/used invite URL → 410/409 copy

---

## 1ed19066 — refactor(web): UploadsFeed agents cache → setState-during-render (#1667) (#1806)

- **Author**: Chris@ZooClaw
- **Date**: 2026-05-21T05:53:47Z

### Full Commit Message

```
refactor(web): UploadsFeed agents cache → setState-during-render (#1667) (#1806)

## Summary

- 新增 `useAllBucketAgentsCache` hook 替代 `useEffect(setAgentsCache,
[agentFilter, feedQuery.data])` post-paint 同步;snapshot 在 render 时随
`'all'` bucket data 引用变化原子更新,跟 #1667 audit 里 `useArtifactsSidebar`
(#1676) 走的 setState-during-render 模式一致。
- Hook 内同时接管 `agentsCache` 的 cross-session reset(observe
`authToken`),UploadsFeed 的 token-reset block 不再持有该 state——一处 reset 来源,跟跨
session 的 filter/preview reset 责任并列。
- 新增 unit test `'all-filter: new agent in next page → dropdown reflects
it atomically with file content'` 锁定原子快照行为:新 page 引入新 agent 时,该 agent
必须在新文件 DOM commit 的同一 render 出现于 dropdown 而不是多一个 commit cycle。
- 复杂度回落:抽 hook 后 `UploadsFeed` cyclomatic 从 26(>25 cap)降回 23。

Refs #1667 — bucket 1 audit 单文件清理;`OnboardingProvider` 已由 #1689 (#1526
B) 修,`CronClient` 在 flight #1796,这是剩下未跟踪的最后一个 bucket-1 文件。

## Test plan

- [x] \`npx tsc --noEmit --pretty false\` (web/app) — pass
- [x] \`pnpm lint\` (web/app) — pass
- [x] \`npx vitest run tests/unit/app/assets/UploadsFeed.unit.spec.tsx\`
— 17/17 pass (16 既有 + 1 新)
- [ ] CI green

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## 2855b53b — test(web): ReplayPlayer unit coverage (#1652-B) (#1809)

- **Author**: Chris@ZooClaw
- **Date**: 2026-05-21T05:51:38Z

### Full Commit Message

```
test(web): ReplayPlayer unit coverage (#1652-B) (#1809)

Refs #1652 (closes the ReplayPlayer portion). E2E `share-replay.spec.ts`
单独后续——Playwright fixture seeding 是另一类工作。

## Summary
23 个 unit test 把 `src/app/share/[shareId]/ReplayPlayer.tsx` (234 line,
was 0% line cov) 推到接近完全覆盖：

- **Header**：title prop > `snapshot.bot.name` > translation key 三段
fallback，message-count placeholder 替换
- **PlayerControls 三状态**（playing / paused / complete）：按钮可见性 + click
handlers（Pause/Resume/Skip/Restart）
- **Provider tree**：ReplayProvider readOnly+shareId、MMAuthProvider 空
token replay 标记、ReplayLightbox mount-once
- **ArtifactsSidebar**：mirror useArtifactsSidebar 钩子状态（closed /
open-with-file）
- **Message slicing → runtime**：`useOpenClawRuntime` 只收 `revealedCount`
条，OpenClawThread 拿到匹配的 messageCount，showToolSteps=true
- **useReplayPlayer 接线**：reducedMotion 从 matchMedia 透传，snapshot.messages
原样转发

复用 PR #1802 引入的 `assistantUiPassthrough` helper。

## 沿用前 PR 的项目特定坑
- `vi.stubGlobal('matchMedia', ...)` + `vi.unstubAllGlobals()` —— jsdom
不带 matchMedia（[[feedback_vitest_async_timers_and_dynamic_import]]）
- Default mock impl 在 `beforeEach` —— `mockReset: true` wipe impls
- `cleanup()` in `afterEach` —— 项目 spec 通用模式
- `queryBy*().not.toBeInTheDocument()` 替代 `.toBeNull()` —— 项目 lint 硬规则

## 不在 scope
- chat-subagent E2E fixture 加强（PR #1802 已 close 了 SubagentChatPanel 的
unit 部分）
- /share/[shareId] E2E spec（需 Playwright + share fixture seeding）

## Test plan
- [x] `vitest run tests/unit/app/share/ReplayPlayer.unit.spec.tsx` — 23
passed
- [x] `vitest run tests/unit/app/share tests/unit/app/chat` — 573 passed
无回归
- [x] `npx tsc --noEmit` clean
- [x] `prettier --check` clean
- [x] pre-commit ESLint pass
- [ ] CI 绿后等手动 merge（不开 auto-merge）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

Refs #1652 (closes the ReplayPlayer portion). E2E `share-replay.spec.ts` 单独后续——Playwright fixture seeding 是另一类工作。

## Summary
23 个 unit test 把 `src/app/share/[shareId]/ReplayPlayer.tsx` (234 line, was 0% line cov) 推到接近完全覆盖：

- **Header**：title prop > `snapshot.bot.name` > translation key 三段 fallback，message-count placeholder 替换
- **PlayerControls 三状态**（playing / paused / complete）：按钮可见性 + click handlers（Pause/Resume/Skip/Restart）
- **Provider tree**：ReplayProvider readOnly+shareId、MMAuthProvider 空 token replay 标记、ReplayLightbox mount-once
- **ArtifactsSidebar**：mirror useArtifactsSidebar 钩子状态（closed / open-with-file）
- **Message slicing → runtime**：`useOpenClawRuntime` 只收 `revealedCount` 条，OpenClawThread 拿到匹配的 messageCount，showToolSteps=true
- **useReplayPlayer 接线**：reducedMotion 从 matchMedia 透传，snapshot.messages 原样转发

复用 PR #1802 引入的 `assistantUiPassthrough` helper。

## 沿用前 PR 的项目特定坑
- `vi.stubGlobal('matchMedia', ...)` + `vi.unstubAllGlobals()` —— jsdom 不带 matchMedia（[[feedback_vitest_async_timers_and_dynamic_import]]）
- Default mock impl 在 `beforeEach` —— `mockReset: true` wipe impls
- `cleanup()` in `afterEach` —— 项目 spec 通用模式
- `queryBy*().not.toBeInTheDocument()` 替代 `.toBeNull()` —— 项目 lint 硬规则

## 不在 scope
- chat-subagent E2E fixture 加强（PR #1802 已 close 了 SubagentChatPanel 的 unit 部分）
- /share/[shareId] E2E spec（需 Playwright + share fixture seeding）

## Test plan
- [x] `vitest run tests/unit/app/share/ReplayPlayer.unit.spec.tsx` — 23 passed
- [x] `vitest run tests/unit/app/share tests/unit/app/chat` — 573 passed 无回归
- [x] `npx tsc --noEmit` clean
- [x] `prettier --check` clean
- [x] pre-commit ESLint pass
- [ ] CI 绿后等手动 merge（不开 auto-merge）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## b0994221 — refactor(web): migrate effect data reads to react query (#1796)

- **Author**: Chris@ZooClaw
- **Date**: 2026-05-21T05:46:23Z

### Full Commit Message

```
refactor(web): migrate effect data reads to react query (#1796)

## Summary
- Move remaining effect-driven remote data reads for user business data,
integrations, agent settings, archived sessions, chat identity, channel
sessions, and conversation assets onto React Query.
- Keep browser/DOM/WebSocket lifecycle effects intact and document the
migration scope.
- Replace schedule job filtering effect with render-time derivation.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit --pretty false
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit --pretty false
- [x] pnpm --dir web/packages/auth-client exec tsc --noEmit --pretty
false
- [x] pnpm --dir web run test:unit

Note: pnpm --dir web run tsc currently fails because the existing script
passes --if-present to pnpm exec, which pnpm 10 rejects; direct package
tsc checks above passed.
```

### PR Description

## Summary
- Move remaining effect-driven remote data reads for user business data, integrations, agent settings, archived sessions, chat identity, channel sessions, and conversation assets onto React Query.
- Keep browser/DOM/WebSocket lifecycle effects intact and document the migration scope.
- Replace schedule job filtering effect with render-time derivation.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit --pretty false
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit --pretty false
- [x] pnpm --dir web/packages/auth-client exec tsc --noEmit --pretty false
- [x] pnpm --dir web run test:unit

Note: pnpm --dir web run tsc currently fails because the existing script passes --if-present to pnpm exec, which pnpm 10 rejects; direct package tsc checks above passed.

---

## 99e64d20 — fix(web): SubagentChatPanel — drop uploading: placeholders on upload throw (#1804) (#1807)

- **Author**: Chris@ZooClaw
- **Date**: 2026-05-21T05:44:21Z

### Full Commit Message

```
fix(web): SubagentChatPanel — drop uploading: placeholders on upload throw (#1804) (#1807)

Closes #1804

## Summary
- `processFiles` 的 catch 分支当时只调 `captureChatError` + `alert`，**没调
`removePlaceholder`**。`uploadToR2` 抛错时 `![](uploading:xxx)` 占位符永久残留 →
`hasUploadingPlaceholder=true` → `isSendDisabled=true` →
发送按钮永久禁用，直到用户手动编辑输入。
- 修：catch 分支补一个 `for (const { placeholderId } of fileInfos)
removePlaceholder(placeholderId)` 循环。`removePlaceholder` 的 regex 对已被
publicUrl 替换的 id 是 no-op，因此 partial-success-then-throw 也安全。
- 翻 PR #1802 加的 `it.fails` 红锁 → `it()`：`upload throw clears the
uploading: placeholder so send button is not permanently
disabled`。pattern 跟 [[feedback_red_test_via_it_fails]] 一致。

## Root cause
`{ success: false }`（非 throw）路径在 for-loop 内调 `removePlaceholder` 是对的，但当
`uploadToR2` **throws**（network error / fetch reject），JS 立即跳出 for-loop 进
catch，loop 内的 cleanup 被绕过。catch 只有日志和 alert，placeholder 漏清。

## Test plan
- [x] `vitest run tests/unit/app/chat/SubagentChatPanel.unit.spec.tsx` —
27 passed（含 #1804 regression flipped from `it.fails` to `it()`）
- [x] `npx tsc --noEmit` clean
- [x] `prettier --check` clean
- [x] pre-commit ESLint pass
- [ ] CI 绿后等手动 merge（不开 auto-merge）

## Refs
- Issue: #1804（surface 于 PR #1802 Claude reviewer）
- 上游 PR: #1802（#1652-A SubagentChatPanel coverage）加了红锁

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## 6c419b46 — test(web): SubagentChatPanel unit coverage + shared assistant-ui helper (#1652-A) (#1802)

- **Author**: Chris@ZooClaw
- **Date**: 2026-05-21T05:37:34Z

### Full Commit Message

```
test(web): SubagentChatPanel unit coverage + shared assistant-ui helper (#1652-A) (#1802)

Refs #1652 (closes the SubagentChatPanel portion). ReplayPlayer + E2E
parts continue separately.

## Summary
- `tests/unit/helpers/assistantUiMocks.tsx` — 共享的 `@assistant-ui/react`
passthrough mock factory（只 mock `AssistantRuntimeProvider`），给
SubagentChatPanel / ReplayPlayer 这种"只用 provider 包一层"的组件用。文档注明 *不* 替代
OpenClawThread.unit.spec.tsx 那套更厚的 ThreadPrimitive / MessagePrimitive
mock。
- `tests/unit/app/chat/SubagentChatPanel.unit.spec.tsx` — 26 个新 unit
test，把 SubagentChatPanel (283 line, was 0% line cov) 推到接近完全覆盖：
  - render variants（默认 / fullPage / readOnly / drag overlay）
  - label fallback chain
  - close button
- send button disabled 五状态（empty / disconnected / uploading placeholder
/ generating）
  - send 路径（click + Enter）+ isGenerating → Stop → abort
- file upload 全流程（paperclip click / success replace / failure remove /
oversized filter / all-oversized no-op / upload throw → captureChatError
/ drop 路径）
  - wiring contracts（onSubmit 只在 enabled 时连 / onFileDrop 始终连）

## 设计 notes
- Default mock impl 放 `beforeEach` 不放 `vi.hoisted`，因为
`vitest.config.mts` 开了 `mockReset: true`，hoisted impl 在第一个 test 后就被
wipe（trapped on it 一次，加了内联 comment 说明）
- `cleanup()` in `afterEach` — 跟 GenClawInput / useBillingCredits 现有
spec 一致
- RichTextInput stub 通过把 `onFileDrop` stash 到 DOM 节点 `__dropHandler` 让
drop test 不用模拟真 DnD 事件序列

## 不在 scope
- ReplayPlayer 单测（紧跟其后下一个 PR）
- chat-subagent E2E fixture 加强（需 Playwright seeding 工作，另起 session）
- /share/[shareId] E2E spec（同上）

## Test plan
- [x] `vitest run tests/unit/app/chat/SubagentChatPanel.unit.spec.tsx` —
26 passed
- [x] `vitest run tests/unit/app/chat tests/unit/helpers` — 548 passed
无回归
- [x] `npx tsc --noEmit` clean
- [x] `prettier --check` clean
- [x] pre-commit ESLint pass
- [ ] CI 绿后等 manual merge（不开 auto-merge）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

Refs #1652 (closes the SubagentChatPanel portion). ReplayPlayer + E2E parts continue separately.

## Summary
- `tests/unit/helpers/assistantUiMocks.tsx` — 共享的 `@assistant-ui/react` passthrough mock factory（只 mock `AssistantRuntimeProvider`），给 SubagentChatPanel / ReplayPlayer 这种"只用 provider 包一层"的组件用。文档注明 *不* 替代 OpenClawThread.unit.spec.tsx 那套更厚的 ThreadPrimitive / MessagePrimitive mock。
- `tests/unit/app/chat/SubagentChatPanel.unit.spec.tsx` — 26 个新 unit test，把 SubagentChatPanel (283 line, was 0% line cov) 推到接近完全覆盖：
  - render variants（默认 / fullPage / readOnly / drag overlay）
  - label fallback chain
  - close button
  - send button disabled 五状态（empty / disconnected / uploading placeholder / generating）
  - send 路径（click + Enter）+ isGenerating → Stop → abort
  - file upload 全流程（paperclip click / success replace / failure remove / oversized filter / all-oversized no-op / upload throw → captureChatError / drop 路径）
  - wiring contracts（onSubmit 只在 enabled 时连 / onFileDrop 始终连）

## 设计 notes
- Default mock impl 放 `beforeEach` 不放 `vi.hoisted`，因为 `vitest.config.mts` 开了 `mockReset: true`，hoisted impl 在第一个 test 后就被 wipe（trapped on it 一次，加了内联 comment 说明）
- `cleanup()` in `afterEach` — 跟 GenClawInput / useBillingCredits 现有 spec 一致
- RichTextInput stub 通过把 `onFileDrop` stash 到 DOM 节点 `__dropHandler` 让 drop test 不用模拟真 DnD 事件序列

## 不在 scope
- ReplayPlayer 单测（紧跟其后下一个 PR）
- chat-subagent E2E fixture 加强（需 Playwright seeding 工作，另起 session）
- /share/[shareId] E2E spec（同上）

## Test plan
- [x] `vitest run tests/unit/app/chat/SubagentChatPanel.unit.spec.tsx` — 26 passed
- [x] `vitest run tests/unit/app/chat tests/unit/helpers` — 548 passed 无回归
- [x] `npx tsc --noEmit` clean
- [x] `prettier --check` clean
- [x] pre-commit ESLint pass
- [ ] CI 绿后等 manual merge（不开 auto-merge）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 899daa4f — docs(web): clarify GiftPaywallFab — trialing intentionally sees FAB (#1680) (#1800)

- **Author**: Chris@ZooClaw
- **Date**: 2026-05-21T04:54:47Z

### Full Commit Message

```
docs(web): clarify GiftPaywallFab — trialing intentionally sees FAB (#1680) (#1800)

Closes #1680

## Summary
- 选 option (a) 从 #1680：code 是对的，**inline comment 误导**。trialing 用户继续看到 🎁
FAB 是 intentional —— 让试用期用户能提前看高 tier 选项。
- 改 `GiftPaywallFab.tsx` line 41 行内注释：原"Hide only when user has an
active/trialing subscription with a plan"删 "/trialing"，并补一行解释 trialing
故意不在 hide set 里。
- 改 `GiftPaywallFab.unit.spec.tsx` trialing 测试的注释：去掉 "see #1680" + "如果
issue 决议成 (b) 翻断言" 这种 TODO，改写为稳定 contract 的描述。

## 不动的部分
- `SUBSCRIBED_STATUSES` 常量本身（已经 `['active', 'canceling', 'past_due']`）
- Line 13-15 的 JSDoc（跟 code 一致，列了正确的 statuses）
- 生产行为完全不变

## Test plan
- [x] `vitest run tests/unit/components/GiftPaywallFab.unit.spec.tsx` —
13 passed
- [x] `npx tsc --noEmit` clean
- [x] `prettier --check` clean
- [x] pre-commit ESLint pass
- [ ] CI 绿后等手动 merge

## Refs
- Issue: #1680（surface 于 PR #1679 codex review during Phase 4 web
coverage push）
- 相关测试在 PR #1679 引入，已含 "see #1680" 指针；本 PR 一并清

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## c236a1d3 — fix(web): forward AbortSignal through checkUserCredits and getAPI (#1618) (#1797)

- **Author**: Chris@ZooClaw
- **Date**: 2026-05-21T04:40:58Z

### Full Commit Message

```
fix(web): forward AbortSignal through checkUserCredits and getAPI (#1618) (#1797)

Closes #1618

## Summary
- `useBillingCredits.queryFn` 不接 React Query 注入的
`AbortSignal`，`queryClient.cancelQueries()` 只 observer-side discard
结果，**真正的 HTTP 请求继续飞**。Codex round 7 review + Claude reviewer 都在 PR-b3
(#1537) 点出过。
- 修一条 signal 完整链路：`useBillingCredits.queryFn({ signal })` →
`checkUserCredits(uid, 10, signal)` → `getAPI(url, undefined, signal)` →
`callAPI({..., signal})` → `AbortSignal.any([timeoutController.signal,
signal])` → `fetch(signal: composite)`。
- `postAPI` / `putAPI` / `deleteAPI` / `patchAPI` 不动 —— issue 明确"留给 RQ
migration spec PR-f 一并处理"。
- `checkCreditsEnough` 内 imperative `checkUserCredits` 调用也不动（plan option
B）—— 路径短，cancel 收益小；reviewer 觉得有必要可单独再补。

## Root cause
Pre-RQ migration 的 `useBillingCredits` 直接拿 fetch 出来,signal 只用于
timeout。PR-b3 切到 `useQuery`,加了 `cancelQueries`/`setQueryData` 防 stale,但
queryFn `async () => checkUserCredits(uid!, 10)` 漏接 signal —— RQ 的 abort
primitive 接到了一个 *new AbortController + 没人监听 signal* 的 promise,所以 cancel
只在 observer 层有效。

测试侧的 contract drift：原 `credits-refresh-data cancels in-flight refetch`
测试用 `queryClient.fetchQuery({ queryFn: async ({ signal }) => ... })`
push 了一个测试自己写的 signal-aware queryFn,只证明了 RQ 的 cancel primitive 工作,*不*证明
production 路径连到了这个 primitive。

## Test plan
- [x] new: `callAPI` + `getAPI` signal 转发契约（断 fetch 收到的 signal 跟 caller
controller 同步 abort）
- [x] new: `checkUserCredits` 第三参数转发给 `getAPI`
- [x] new: `useBillingCredits` production 路径——RQ 注入 signal →
`checkUserCredits` 第三参数 → `credits-refresh-data` listener 触发
cancelQueries → signal aborts
- [x] 原 line-864 测试（RQ-level cancel primitive）保留作 companion——它仍然证明
primitive 工作，新测试证明 production 已接上
- [x] 既有 `checkUserCredits` 两个 `toHaveBeenCalledWith` 切到
`mock.calls[0]?.[0]`——`toHaveBeenCalledWith` 单 matcher 隐含断言参数个数，新增
optional params 让它 fail
- [x] `vitest run tests/unit/lib/api tests/unit/hooks` 1081 passed
- [x] `npx tsc --noEmit` 全仓 + `prettier --check` 已改文件
- [ ] CI 绿后等 manual merge（不开 auto-merge）

## Refs
- Issue: #1618（Codex round 7 + Claude reviewer 都点出过）
- 上游 PR: #1537（PR-b3：useBillingCredits 切 useQuery）
- 待跟进 spec:
`docs/superpowers/specs/2026-04-25-react-query-migration-v2.md` PR-f 处理
`postAPI`/`putAPI`/etc 的 signal 转发

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---
