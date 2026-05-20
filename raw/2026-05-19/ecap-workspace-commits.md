# SerendipityOneInc/ecap-workspace - Commits on 2026-05-19

## [980fcced] refactor(ci): drop lark-cli-smoke + extract release-notify-lark to srp-actions reusable (#1754)
- **SHA:** 980fcced395b082d8f3a7129e6640e0ae5327590
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-19T17:30:04Z

### Full Commit Message
```
refactor(ci): drop lark-cli-smoke + extract release-notify-lark to srp-actions reusable (#1754)

## Summary

- 删除 `.github/workflows/lark-cli-smoke.yml`：早期 lark-cli + TAT 链路 smoke
test，目标已被 `release-notify-lark` 自动通知完整覆盖；workflow 自身仅
`workflow_dispatch` 触发、长期未跑。
- `release-notify-lark.yml` 由 405 行内联实现改为 ~150 行 caller，通用流程下沉到
[SerendipityOneInc/srp-actions#75](https://github.com/SerendipityOneInc/srp-actions/pull/75)
提供的 reusable workflow `release-notify-lark.yml@main`。本仓只保留 ECAP 特有的
tag→project / chat_id / path filter / deploy 文件名映射。
- 顺手修：reusable 抽取过程中 Codex review 发现一个原 inline 实现里就潜藏的 bug —— "首次发版" 场景下
`git tag -l ... | grep -v THIS_TAG` 在 `pipefail` 下 exit 1，让 fallback 2
(repo 首 commit) 不可达。已在 srp-actions PR #75 里修。本 PR merge 后，ecap main 上的同一
bug 也随之消除。

## 依赖（merge 顺序）

⚠️ **必须先 merge**
[srp-actions#75](https://github.com/SerendipityOneInc/srp-actions/pull/75)，否则本
PR merge 后下次 release deploy 触发 `workflow_run` 时会因解析不到 `@main` 上的
reusable workflow 失败。

srp-actions PR 状态：✅ CodeQL / actionlint / codex-review / auto-review
全绿，等待 human merge。

## 后续好处

新仓（fastclaw / openclaw-docker / ecap-skills / ecap-agent-pack 等）接入相同
release 通知链路时，只需：

```yaml
# .github/workflows/release-notify-lark.yml （新仓里）
on:
  workflow_run: { workflows: ["<本仓 deploy workflow name>"], types: [completed] }
  workflow_dispatch: { inputs: { tag: ..., dry_run: ..., is_test: ... } }
permissions: { contents: read, pull-requests: read, id-token: write, actions: read }
jobs:
  resolve: { ... tag → project / chat_id 映射，~50 行 ... }
  notify:
    needs: resolve
    uses: SerendipityOneInc/srp-actions/.github/workflows/release-notify-lark.yml@main
    with: { ... 12 inputs ... }
    secrets: inherit
```

不再复制 405 行实现，也跟着自动吃到 srp-actions 后续的 bug fix / 功能更新。

## Test plan

- [x] `actionlint` 本地跑过（caller + reusable 都过）
- [x] yaml.safe_load parse OK
- [x] srp-actions PR #75 静态 CI 全绿（Codex 第二轮 APPROVE）
- [ ] **srp-actions PR #75 merge 后** rebase 本 PR + 重跑 ecap CI
- [ ] `workflow_dispatch` dry-run 一次 `tag=ecap-v<历史 tag>-release` +
`dry_run=true` + `is_test=true`，确认 resolve job + reusable notify job
都成功，Lark 发送三步因 `dry_run=true` 被 skip
- [ ] `workflow_dispatch` dry-run 一次 `tag=service-v<历史 tag>-release`，确认
project=service 路径正常
- [ ] `dry_run=false + is_test=true` 跑一次，发送测试消息到测试群人工验收
- [ ] 等下一次正式 `*-release` 部署完，验证 `workflow_run` 自动通知链路无回归

## 回滚

如本 PR merge 后 reusable 行为异常，最快回滚是 revert 本 PR（恢复内联 405 行实现）；srp-actions
那侧不动也不影响 ECAP 现网。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1754 Body
## Summary

- 删除 `.github/workflows/lark-cli-smoke.yml`：早期 lark-cli + TAT 链路 smoke test，目标已被 `release-notify-lark` 自动通知完整覆盖；workflow 自身仅 `workflow_dispatch` 触发、长期未跑。
- `release-notify-lark.yml` 由 405 行内联实现改为 ~150 行 caller，通用流程下沉到 [SerendipityOneInc/srp-actions#75](https://github.com/SerendipityOneInc/srp-actions/pull/75) 提供的 reusable workflow `release-notify-lark.yml@main`。本仓只保留 ECAP 特有的 tag→project / chat_id / path filter / deploy 文件名映射。
- 顺手修：reusable 抽取过程中 Codex review 发现一个原 inline 实现里就潜藏的 bug —— "首次发版" 场景下 `git tag -l ... | grep -v THIS_TAG` 在 `pipefail` 下 exit 1，让 fallback 2 (repo 首 commit) 不可达。已在 srp-actions PR #75 里修。本 PR merge 后，ecap main 上的同一 bug 也随之消除。

## 依赖（merge 顺序）

⚠️ **必须先 merge** [srp-actions#75](https://github.com/SerendipityOneInc/srp-actions/pull/75)，否则本 PR merge 后下次 release deploy 触发 `workflow_run` 时会因解析不到 `@main` 上的 reusable workflow 失败。

srp-actions PR 状态：✅ CodeQL / actionlint / codex-review / auto-review 全绿，等待 human merge。

## 后续好处

新仓（fastclaw / openclaw-docker / ecap-skills / ecap-agent-pack 等）接入相同 release 通知链路时，只需：

```yaml
# .github/workflows/release-notify-lark.yml （新仓里）
on:
  workflow_run: { workflows: ["<本仓 deploy workflow name>"], types: [completed] }
  workflow_dispatch: { inputs: { tag: ..., dry_run: ..., is_test: ... } }
permissions: { contents: read, pull-requests: read, id-token: write, actions: read }
jobs:
  resolve: { ... tag → project / chat_id 映射，~50 行 ... }
  notify:
    needs: resolve
    uses: SerendipityOneInc/srp-actions/.github/workflows/release-notify-lark.yml@main
    with: { ... 12 inputs ... }
    secrets: inherit
```

不再复制 405 行实现，也跟着自动吃到 srp-actions 后续的 bug fix / 功能更新。

## Test plan

- [x] `actionlint` 本地跑过（caller + reusable 都过）
- [x] yaml.safe_load parse OK
- [x] srp-actions PR #75 静态 CI 全绿（Codex 第二轮 APPROVE）
- [ ] **srp-actions PR #75 merge 后** rebase 本 PR + 重跑 ecap CI
- [ ] `workflow_dispatch` dry-run 一次 `tag=ecap-v<历史 tag>-release` + `dry_run=true` + `is_test=true`，确认 resolve job + reusable notify job 都成功，Lark 发送三步因 `dry_run=true` 被 skip
- [ ] `workflow_dispatch` dry-run 一次 `tag=service-v<历史 tag>-release`，确认 project=service 路径正常
- [ ] `dry_run=false + is_test=true` 跑一次，发送测试消息到测试群人工验收
- [ ] 等下一次正式 `*-release` 部署完，验证 `workflow_run` 自动通知链路无回归

## 回滚

如本 PR merge 后 reusable 行为异常，最快回滚是 revert 本 PR（恢复内联 405 行实现）；srp-actions 那侧不动也不影响 ECAP 现网。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [041c5d6e] test(e2e): wait for streamed text to stabilise, not just the button cycle (#1747)
- **SHA:** 041c5d6e9cdbba3d63bbfd93e9c5f3705a9c783d
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-19T17:14:41Z

### Full Commit Message
```
test(e2e): wait for streamed text to stabilise, not just the button cycle (#1747)

## Summary

`waitForResponseComplete()` in `panda-claw-chat.page.ts` previously
returned as soon as the send/stop button cycle resolved. But the button
cycle signals "generation pipeline finished" — token-level assistant
text streaming can still be in flight after that. Callers reading
`getLastBotMessage()` immediately captured mid-stream snapshots like
`"Hel"` or `"The"`, and assertions failed with "Response too short"
against partial content.

Added a `waitForBotMessageStable()` second phase:

- Polls `getLastBotMessage()` length every 250 ms
- Returns once length has been unchanged for `stableMs` (default 1.5 s)
- Bounded by `timeout` (default 10 s); on cap, returns silently and lets
the caller's content assertion be the final arbiter

## Why this matters now

Pre-#1738, the bot-name strip regex left the header prefix in extracted
text. That padding pushed most streaming snapshots over the 5-char
threshold used by the smoke spec and made the issue effectively
invisible. Once #1738 stripped headers correctly, the underlying race
surfaced as 3 new failures in [run
26096207251](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/26096207251):

- `chat-smoke` — `"Hel"` (3/5)
- `session-features auto-titling` — `"The"` (3/30)
- `session-features multi-step` — `"The"` (3/30)

This PR addresses the underlying wait-logic gap that produced those
snapshots.

## Timeout design

| Param | Default | Why |
|-------|---------|-----|
| `stableMs` | 1500 ms | Tolerates natural pauses between tool calls and
assistant text; LLM streams at ~30-50 tokens/s, so 1.5 s of silence
reliably indicates burst end |
| `timeout` | 10000 ms | Covers virtually all single-response bursts; a
stream growing past this is pathologically slow and should fail the
caller's assertion |
| `pollIntervalMs` | 250 ms | Fine enough to catch streaming tokens,
coarse enough to keep CPU/network calls low |
| **No throw on timeout** | — | Avoids introducing a new error class;
the caller's `assertResponseHasContent` is the proper place to judge "is
this snapshot long enough" |

Also refactored the existing grace-period branch to fall through to the
stability poll instead of early-returning, so every path benefits.

## Out of scope

- `tool-misc healthcheck` (response \"✅ New session started.\" is 22
chars vs the 30-char default `assertResponseHasContent` threshold) is a
spec-assertion calibration question, not a wait-logic issue.
- `basic-usage video_reply` is a separate product issue tracked in
#1739.
- `.streaming-cursor` selector in `waitForResponseStart()` is dead code
(the class doesn't exist in product markup) — independent cleanup.

## Test plan
- [x] `pnpm --filter @zooclaw/web-app lint` passes (pre-commit hook)
- [ ] `gh workflow run \"ZooClaw E2E Tests\" --ref
feature/fix-e2e-wait-content-stable -f base_url=https://zooclaw.ai` —
expect the 3 streaming-snapshot failures gone, only video_reply (#1739)
+ possibly healthcheck (separate scope) remaining

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1747 Body
## Summary

`waitForResponseComplete()` in `panda-claw-chat.page.ts` previously returned as soon as the send/stop button cycle resolved. But the button cycle signals "generation pipeline finished" — token-level assistant text streaming can still be in flight after that. Callers reading `getLastBotMessage()` immediately captured mid-stream snapshots like `"Hel"` or `"The"`, and assertions failed with "Response too short" against partial content.

Added a `waitForBotMessageStable()` second phase:

- Polls `getLastBotMessage()` length every 250 ms
- Returns once length has been unchanged for `stableMs` (default 1.5 s)
- Bounded by `timeout` (default 10 s); on cap, returns silently and lets the caller's content assertion be the final arbiter

## Why this matters now

Pre-#1738, the bot-name strip regex left the header prefix in extracted text. That padding pushed most streaming snapshots over the 5-char threshold used by the smoke spec and made the issue effectively invisible. Once #1738 stripped headers correctly, the underlying race surfaced as 3 new failures in [run 26096207251](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/26096207251):

- `chat-smoke` — `"Hel"` (3/5)
- `session-features auto-titling` — `"The"` (3/30)
- `session-features multi-step` — `"The"` (3/30)

This PR addresses the underlying wait-logic gap that produced those snapshots.

## Timeout design

| Param | Default | Why |
|-------|---------|-----|
| `stableMs` | 1500 ms | Tolerates natural pauses between tool calls and assistant text; LLM streams at ~30-50 tokens/s, so 1.5 s of silence reliably indicates burst end |
| `timeout`  | 10000 ms | Covers virtually all single-response bursts; a stream growing past this is pathologically slow and should fail the caller's assertion |
| `pollIntervalMs` | 250 ms | Fine enough to catch streaming tokens, coarse enough to keep CPU/network calls low |
| **No throw on timeout** | — | Avoids introducing a new error class; the caller's `assertResponseHasContent` is the proper place to judge "is this snapshot long enough" |

Also refactored the existing grace-period branch to fall through to the stability poll instead of early-returning, so every path benefits.

## Out of scope

- `tool-misc healthcheck` (response \"✅ New session started.\" is 22 chars vs the 30-char default `assertResponseHasContent` threshold) is a spec-assertion calibration question, not a wait-logic issue.
- `basic-usage video_reply` is a separate product issue tracked in #1739.
- `.streaming-cursor` selector in `waitForResponseStart()` is dead code (the class doesn't exist in product markup) — independent cleanup.

## Test plan
- [x] `pnpm --filter @zooclaw/web-app lint` passes (pre-commit hook)
- [ ] `gh workflow run \"ZooClaw E2E Tests\" --ref feature/fix-e2e-wait-content-stable -f base_url=https://zooclaw.ai` — expect the 3 streaming-snapshot failures gone, only video_reply (#1739) + possibly healthcheck (separate scope) remaining

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [1e9b34d3] fix(ci): release-notify-lark — use Sonnet 4.6 (Haiku drops literal metadata) (#1753)
- **SHA:** 1e9b34d3ddba9a58b0f0b6bb962ab238c2498bcb
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-19T16:38:10Z

### Full Commit Message
```
fix(ci): release-notify-lark — use Sonnet 4.6 (Haiku drops literal metadata) (#1753)

Follow-up to #1751.

## Why

Dry-run dispatch of the Lark notify workflow on `ecap-v0.6.80-release`
([run
26110619073](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/26110619073))
and `service-v0.6.74-release` ([run
26110620750](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/26110620750))
revealed that **Haiku 4.5 silently drops the parenthetical part** of the
metadata label:

| Workflow computed | Haiku wrote |
|---|---|
| `测试消息（手动触发）` | `测试消息` |

Both runs showed identical trimming, on both prefixes, despite the
prompt's explicit instruction:

> 元信息（按下面格式原样写入消息顶部，**不要改字面**）

The metadata block is the operator's way to distinguish `正式发布` /
`测试消息（手动触发）` / `正式发布（手动重发）` at a glance — Haiku's trimming defeats that
contract.

## Fix

Switch to Sonnet 4.6 (`us.anthropic.claude-sonnet-4-6`), which
`claude-arch-review.yaml:147` already uses successfully — the alias is
registered as a Bedrock cross-region inference profile in this AWS
account, so the short form works.

Comment in the workflow now records *why* we switched (so a future
contributor doesn't optimize back to Haiku for cost without re-testing
literal-fidelity).

## Test plan

- [ ] After merge, re-dispatch the same two test runs
(`ecap-v0.6.80-release` + `service-v0.6.74-release`, `dry_run=false`,
`is_test=true`) and confirm the message kind line reads `测试消息（手动触发）`
verbatim.
- [ ] Wait for next real `*-release` tag push and confirm `正式发布` label
survives unchanged.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1753 Body
Follow-up to #1751.

## Why

Dry-run dispatch of the Lark notify workflow on `ecap-v0.6.80-release` ([run 26110619073](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/26110619073)) and `service-v0.6.74-release` ([run 26110620750](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/26110620750)) revealed that **Haiku 4.5 silently drops the parenthetical part** of the metadata label:

| Workflow computed | Haiku wrote |
|---|---|
| `测试消息（手动触发）` | `测试消息` |

Both runs showed identical trimming, on both prefixes, despite the prompt's explicit instruction:

> 元信息（按下面格式原样写入消息顶部，**不要改字面**）

The metadata block is the operator's way to distinguish `正式发布` / `测试消息（手动触发）` / `正式发布（手动重发）` at a glance — Haiku's trimming defeats that contract.

## Fix

Switch to Sonnet 4.6 (`us.anthropic.claude-sonnet-4-6`), which `claude-arch-review.yaml:147` already uses successfully — the alias is registered as a Bedrock cross-region inference profile in this AWS account, so the short form works.

Comment in the workflow now records *why* we switched (so a future contributor doesn't optimize back to Haiku for cost without re-testing literal-fidelity).

## Test plan

- [ ] After merge, re-dispatch the same two test runs (`ecap-v0.6.80-release` + `service-v0.6.74-release`, `dry_run=false`, `is_test=true`) and confirm the message kind line reads `测试消息（手动触发）` verbatim.
- [ ] Wait for next real `*-release` tag push and confirm `正式发布` label survives unchanged.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [7c4c4d58] fix(ci): release-notify-lark — wait for deploy success, add metadata, fix Haiku model ID (#1751)
- **SHA:** 7c4c4d589672f2955ec7e46e8740a9ac8a74dded
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-19T16:24:12Z

### Full Commit Message
```
fix(ci): release-notify-lark — wait for deploy success, add metadata, fix Haiku model ID (#1751)

Follow-up to #1745 — three accumulated improvements to the Lark release
notification workflow, discovered through dry-run testing:

## 1. Trigger on deploy success, not tag push (`26367f17`)

**Problem:** Previous `on: push: tags` fired the moment a release tag
was pushed — in parallel with `deploy.yml` / `service-deploy.yml`. The
notification could go out before deploy finished, or even when deploy
ended up failing.

**Fix:** Switch to `workflow_run: [Deploy ECAP, Service Build and
Deploy]
types: [completed]` with a job-level `if:` gating on
`conclusion == 'success'` plus a `*-release` head-branch match. Skips
main staging deploys, `*-beta` tags, and any failed release run.

Handles workflow_run quirks: `github.sha` / `github.ref_name` would
otherwise be main HEAD; everything switches to
`github.event.workflow_run.head_sha` / `head_branch`.

## 2. Metadata: prev tag + time + message kind (`101d3971`)

Per user request, the Lark message now leads with a metadata blockquote:

```
# frontend ecap-v0.6.80-release
> 📌 [消息类型] · 上次发版 ecap-v0.6.79-release (2026-05-18 21:18)
```

- **Prev tag + date** — jq filter already had to find the previous
  release deploy run; now extracts `headBranch` (= tag name) alongside
  `headSha`, then `git log -1 --format=%aI <tag>` gives the ISO date.
- **Message kind** — new `is_test` workflow_dispatch input (default
  true) lets the operator distinguish "正式发布 / 测试消息（手动触发） /
  正式发布（手动重发）"; workflow_run is always "正式发布".

## 3. Full Bedrock model ID for Haiku 4.5 (`b9fcba4e`)

The shorthand `us.anthropic.claude-haiku-4-5` (mirroring arch-review's
sonnet shorthand) is rejected by Bedrock with "400 invalid identifier".
The sonnet alias is a custom inference profile registered for that
specific model in this AWS account; Haiku 4.5 has no equivalent alias
yet, so we use the full cross-region inference profile ID
`us.anthropic.claude-haiku-4-5-20251001-v1:0`.

## Codex review 状态

5 轮 codex auto-review 中：

- **#1** (`THIS_SHA` 落回 `github.sha`)：`984af8c0` 已用 `git rev-parse
"$INPUT_TAG"` 修
- **#3a** (dispatch 空 tag 落到 branch name)：`dc9f9201` 已改 `required: true`
- **#4** (same-tag rerun 被误判 rollback)：`8010f0e7` baseline filter 已加
`.headSha != $s`，line 195 `BASE != THIS` 双守卫
- **#3b / #5** (`workflow_run.head_branch` 对 tag push 不可靠)：经实测验证为误报，见下方
PR 评论
- **#2** (rerun 已成功 deploy 会重复通知)：见下方"已知行为"

## 已知行为

手动 rerun 一个已经成功的 `*-release` deploy 会再发一条飞书通知
（`workflow_run` 不区分 `run_attempt == 1` vs 后续 attempts）。

- 正常发版流程不会触发：rerun 一个已成功的 deploy 没有业务理由
- rerun-after-failure（attempt 1 失败 → attempt 2 成功）是想要的通知场景，
  正是这个非区分行为让它能跑——`run_attempt == 1` 守卫会把这条合法通知一起拦掉
- 若将来真出现误发，follow-up 加 notify-self-dedupe（`gh run list` 自查同 tag 已成功）

## Test plan

### Dispatch dry-run (verified before opening this PR)
Run
[26104546089](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/26104546089)
— `tag=ecap-v0.6.80-release, dry_run=true, is_test=true` — generated:

```
# frontend ecap-v0.6.80-release
> 📌 测试消息 · 上次发版 ecap-v0.6.79-release (2026-05-18 21:18)

## ✨ 新功能
- 支付方式选择弹窗 UI 升级…

## 🔧 其他
- 修复测试框架，提高 E2E 测试稳定性。
```

### Post-merge end-to-end
- [ ] After this PR merges, manually dispatch with `is_test=false`,
      `dry_run=false`, `tag=ecap-v0.6.80-release` — verify a real Lark
message lands in the test group (`oc_213291d2715a9d02bf5b0bb18b847e3c`).
- [ ] Wait for next real `ecap-v*-release` tag push; verify
`workflow_run`
      fires this workflow only after `deploy.yml` ends with success.
- [ ] Replace the placeholder chat-id with the production groups when
      ready (still set to the lark-cli-smoke test group).

## Caveats

- **workflow_run requires the workflow file on default branch.** Until
  this PR merges, real release-tag-triggered runs use the old `on: push`
  trigger from #1745. After merge, deploys must finish before the
  notification fires.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1751 Body
Follow-up to #1745 — three accumulated improvements to the Lark release
notification workflow, discovered through dry-run testing:

## 1. Trigger on deploy success, not tag push (`26367f17`)

**Problem:** Previous `on: push: tags` fired the moment a release tag
was pushed — in parallel with `deploy.yml` / `service-deploy.yml`. The
notification could go out before deploy finished, or even when deploy
ended up failing.

**Fix:** Switch to `workflow_run: [Deploy ECAP, Service Build and Deploy]
types: [completed]` with a job-level `if:` gating on
`conclusion == 'success'` plus a `*-release` head-branch match. Skips
main staging deploys, `*-beta` tags, and any failed release run.

Handles workflow_run quirks: `github.sha` / `github.ref_name` would
otherwise be main HEAD; everything switches to
`github.event.workflow_run.head_sha` / `head_branch`.

## 2. Metadata: prev tag + time + message kind (`101d3971`)

Per user request, the Lark message now leads with a metadata blockquote:

```
# frontend ecap-v0.6.80-release
> 📌 [消息类型] · 上次发版 ecap-v0.6.79-release (2026-05-18 21:18)
```

- **Prev tag + date** — jq filter already had to find the previous
  release deploy run; now extracts `headBranch` (= tag name) alongside
  `headSha`, then `git log -1 --format=%aI <tag>` gives the ISO date.
- **Message kind** — new `is_test` workflow_dispatch input (default
  true) lets the operator distinguish "正式发布 / 测试消息（手动触发） /
  正式发布（手动重发）"; workflow_run is always "正式发布".

## 3. Full Bedrock model ID for Haiku 4.5 (`b9fcba4e`)

The shorthand `us.anthropic.claude-haiku-4-5` (mirroring arch-review's
sonnet shorthand) is rejected by Bedrock with "400 invalid identifier".
The sonnet alias is a custom inference profile registered for that
specific model in this AWS account; Haiku 4.5 has no equivalent alias
yet, so we use the full cross-region inference profile ID
`us.anthropic.claude-haiku-4-5-20251001-v1:0`.

## Codex review 状态

5 轮 codex auto-review 中：

- **#1** (`THIS_SHA` 落回 `github.sha`)：`984af8c0` 已用 `git rev-parse "$INPUT_TAG"` 修
- **#3a** (dispatch 空 tag 落到 branch name)：`dc9f9201` 已改 `required: true`
- **#4** (same-tag rerun 被误判 rollback)：`8010f0e7` baseline filter 已加 `.headSha != $s`，line 195 `BASE != THIS` 双守卫
- **#3b / #5** (`workflow_run.head_branch` 对 tag push 不可靠)：经实测验证为误报，见下方 PR 评论
- **#2** (rerun 已成功 deploy 会重复通知)：见下方"已知行为"

## 已知行为

手动 rerun 一个已经成功的 `*-release` deploy 会再发一条飞书通知
（`workflow_run` 不区分 `run_attempt == 1` vs 后续 attempts）。

- 正常发版流程不会触发：rerun 一个已成功的 deploy 没有业务理由
- rerun-after-failure（attempt 1 失败 → attempt 2 成功）是想要的通知场景，
  正是这个非区分行为让它能跑——`run_attempt == 1` 守卫会把这条合法通知一起拦掉
- 若将来真出现误发，follow-up 加 notify-self-dedupe（`gh run list` 自查同 tag 已成功）

## Test plan

### Dispatch dry-run (verified before opening this PR)
Run [26104546089](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/26104546089) — `tag=ecap-v0.6.80-release, dry_run=true, is_test=true` — generated:

```
# frontend ecap-v0.6.80-release
> 📌 测试消息 · 上次发版 ecap-v0.6.79-release (2026-05-18 21:18)

## ✨ 新功能
- 支付方式选择弹窗 UI 升级…

## 🔧 其他
- 修复测试框架，提高 E2E 测试稳定性。
```

### Post-merge end-to-end
- [ ] After this PR merges, manually dispatch with `is_test=false`,
      `dry_run=false`, `tag=ecap-v0.6.80-release` — verify a real Lark
      message lands in the test group (`oc_213291d2715a9d02bf5b0bb18b847e3c`).
- [ ] Wait for next real `ecap-v*-release` tag push; verify `workflow_run`
      fires this workflow only after `deploy.yml` ends with success.
- [ ] Replace the placeholder chat-id with the production groups when
      ready (still set to the lark-cli-smoke test group).

## Caveats

- **workflow_run requires the workflow file on default branch.** Until
  this PR merges, real release-tag-triggered runs use the old `on: push`
  trigger from #1745. After merge, deploys must finish before the
  notification fires.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## [7e9ca03c] feat(devcontainer): add @larksuite/cli + check in lark-im skill (#1745)
- **SHA:** 7e9ca03c55eb761501a832b4689250799281e931
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-19T14:25:07Z

### Full Commit Message
```
feat(devcontainer): add @larksuite/cli + check in lark-im skill (#1745)

## Summary
- Install `@larksuite/cli` globally in the devcontainer image, alongside
the existing `@openai/codex` install (`.devcontainer/Dockerfile` line
39).
- Check in the `lark-im` skill as static markdown under
`.agents/skills/lark-im/` (SKILL.md + 16 reference docs), with a
`.claude/skills/lark-im` symlink so Claude Code discovers it on the
standard path.
- Add `skills-lock.json` to pin the upstream source (`larksuite/cli`)
and content hash, parallel in role to `pnpm-lock.yaml`.

Foundation work for the `feature/auto-deploy-notification` branch —
gives every devcontainer user the Lark IM tooling needed to send deploy
notifications.

## Why split CLI vs skill
- CLI is a binary, must be in `$PATH` → bake into the image (one network
call at build time, not per-container-start).
- Skill is static markdown, no install step → check it in like any other
repo source so it's version-controlled and works offline.

## Note on PR size
The 2300+ added lines are vendored static markdown from upstream
`larksuite/cli` (SKILL.md + 16 reference docs under
`.agents/skills/lark-im/`), not hand-written code. Adding
`size-override` label since splitting a single skill drop isn't
meaningful.

## Test plan
- [ ] Rebuild the devcontainer; `which lark` resolves to the global npm
prefix.
- [ ] `lark --version` runs without error.
- [ ] `ls -la .claude/skills/` shows `lark-im ->
../../.agents/skills/lark-im` symlink intact.
- [ ] In Claude Code, the `lark-im` skill is discoverable (description
triggers on 飞书 / 发消息 / 搜聊天记录 keywords).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1745 Body
## Summary
- Install `@larksuite/cli` globally in the devcontainer image, alongside the existing `@openai/codex` install (`.devcontainer/Dockerfile` line 39).
- Check in the `lark-im` skill as static markdown under `.agents/skills/lark-im/` (SKILL.md + 16 reference docs), with a `.claude/skills/lark-im` symlink so Claude Code discovers it on the standard path.
- Add `skills-lock.json` to pin the upstream source (`larksuite/cli`) and content hash, parallel in role to `pnpm-lock.yaml`.

Foundation work for the `feature/auto-deploy-notification` branch — gives every devcontainer user the Lark IM tooling needed to send deploy notifications.

## Why split CLI vs skill
- CLI is a binary, must be in `$PATH` → bake into the image (one network call at build time, not per-container-start).
- Skill is static markdown, no install step → check it in like any other repo source so it's version-controlled and works offline.

## Note on PR size
The 2300+ added lines are vendored static markdown from upstream `larksuite/cli` (SKILL.md + 16 reference docs under `.agents/skills/lark-im/`), not hand-written code. Adding `size-override` label since splitting a single skill drop isn't meaningful.

## Test plan
- [ ] Rebuild the devcontainer; `which lark` resolves to the global npm prefix.
- [ ] `lark --version` runs without error.
- [ ] `ls -la .claude/skills/` shows `lark-im -> ../../.agents/skills/lark-im` symlink intact.
- [ ] In Claude Code, the `lark-im` skill is discoverable (description triggers on 飞书 / 发消息 / 搜聊天记录 keywords).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [a674ecf7] feat(service): add /version endpoint aligned with frontend schema (#1746)
- **SHA:** a674ecf70d6db777b77f5fadb87a5b2c37cf11a1
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-19T14:00:03Z

### Full Commit Message
```
feat(service): add /version endpoint aligned with frontend schema (#1746)

## Summary
- Adds `GET /version` on `claw-interface` returning the same JSON shape
as the frontend `/api/version`, so monitoring / oncall can compare
frontend vs backend deployed versions side-by-side.
- Reads `/code/manifest.metadata` (populated at image-build time by
`srp-actions/.github/workflows/build-and-push-image-cached.yml`) plus
the `ENVIRONMENT` env var; falls back gracefully when fields are missing
(local dev, branch builds, manifest absent).
- Schema mirrors the frontend `buildInfo` exactly: `{ success, data: {
version, commit, commitFull, buildTime, environment, ref, deployedBy }
}`.

## Field mapping
| Field | Source |
|---|---|
| `commit` / `commitFull` | `GIT_COMMIT_HASH` from manifest (7-char +
full) |
| `version` / `ref` | `GIT_TAGS` first entry; fallback to
`GIT_BRANCH_NAME`, then `pyproject.toml` `[project].version` |
| `buildTime` | `IMAGE_TIMESTAMP` normalized from `"YYYY-MM-DD HH:MM:SS
UTC"` to ISO 8601 `Z` |
| `environment` | `ENVIRONMENT` env var (currently \"unknown\" — see
follow-up) |
| `deployedBy` | `DEPLOYED_BY` from manifest if present, else `\"ci\"`
(see follow-up) |

## Follow-ups (not in this PR)
- Add `ENVIRONMENT` env var to
`services/claw-interface/kustomize/overlays/*` Deployment patches —
otherwise `environment` always reports `\"unknown\"`.
- Optionally extend the `srp-actions` reusable workflow to emit
`DEPLOYED_BY=\${{ github.actor }}` into `manifest.metadata` so
`deployedBy` returns a real handle instead of `\"ci\"`.
Forward-compatible: this PR already reads `DEPLOYED_BY` and will pick up
the real value automatically once upstream emits it.

## Test plan
- [x] `app/routes/status.py` + `tests/unit/test_status.py` pass
`ast.parse`
- [x] Smoke-tested `_normalize_build_time('2026-05-19 12:23:50 UTC')` ->
`'2026-05-19T12:23:50Z'` on local Python 3.11
- [x] Smoke-tested `_build_info()` no-manifest path -> returns sensible
`\"unknown\"` placeholders + `version='0.0.0'`
- [ ] CI `python-code-quality / build-and-test` (ruff + pyright +
pytest) covers the full suite incl. 3 new unit tests
- [ ] Post-deploy: `kubectl -n <ns> exec <claw-interface-pod> -- curl -s
localhost:8080/version | jq` returns a real SHA matching the deployment
image tag
- [ ] Side-by-side: `curl https://<frontend>/api/version | jq .data` vs
`curl https://<backend>/version | jq .data` — fields aligned, values
represent each service's own build

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1746 Body
## Summary
- Adds `GET /version` on `claw-interface` returning the same JSON shape as the frontend `/api/version`, so monitoring / oncall can compare frontend vs backend deployed versions side-by-side.
- Reads `/code/manifest.metadata` (populated at image-build time by `srp-actions/.github/workflows/build-and-push-image-cached.yml`) plus the `ENVIRONMENT` env var; falls back gracefully when fields are missing (local dev, branch builds, manifest absent).
- Schema mirrors the frontend `buildInfo` exactly: `{ success, data: { version, commit, commitFull, buildTime, environment, ref, deployedBy } }`.

## Field mapping
| Field | Source |
|---|---|
| `commit` / `commitFull` | `GIT_COMMIT_HASH` from manifest (7-char + full) |
| `version` / `ref` | `GIT_TAGS` first entry; fallback to `GIT_BRANCH_NAME`, then `pyproject.toml` `[project].version` |
| `buildTime` | `IMAGE_TIMESTAMP` normalized from `"YYYY-MM-DD HH:MM:SS UTC"` to ISO 8601 `Z` |
| `environment` | `ENVIRONMENT` env var (currently \"unknown\" — see follow-up) |
| `deployedBy` | `DEPLOYED_BY` from manifest if present, else `\"ci\"` (see follow-up) |

## Follow-ups (not in this PR)
- Add `ENVIRONMENT` env var to `services/claw-interface/kustomize/overlays/*` Deployment patches — otherwise `environment` always reports `\"unknown\"`.
- Optionally extend the `srp-actions` reusable workflow to emit `DEPLOYED_BY=\${{ github.actor }}` into `manifest.metadata` so `deployedBy` returns a real handle instead of `\"ci\"`. Forward-compatible: this PR already reads `DEPLOYED_BY` and will pick up the real value automatically once upstream emits it.

## Test plan
- [x] `app/routes/status.py` + `tests/unit/test_status.py` pass `ast.parse`
- [x] Smoke-tested `_normalize_build_time('2026-05-19 12:23:50 UTC')` -> `'2026-05-19T12:23:50Z'` on local Python 3.11
- [x] Smoke-tested `_build_info()` no-manifest path -> returns sensible `\"unknown\"` placeholders + `version='0.0.0'`
- [ ] CI `python-code-quality / build-and-test` (ruff + pyright + pytest) covers the full suite incl. 3 new unit tests
- [ ] Post-deploy: `kubectl -n <ns> exec <claw-interface-pod> -- curl -s localhost:8080/version | jq` returns a real SHA matching the deployment image tag
- [ ] Side-by-side: `curl https://<frontend>/api/version | jq .data` vs `curl https://<backend>/version | jq .data` — fields aligned, values represent each service's own build

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [f3bfdd8e] test(e2e): generalise bot-name strip regex in getLastBotMessage (#1738)
- **SHA:** f3bfdd8e2bed82c8b409dbb08d7efa625d170b6d
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-19T12:55:11Z

### Full Commit Message
```
test(e2e): generalise bot-name strip regex in getLastBotMessage (#1738)

## Summary
- Replaces the hardcoded `^Panda\s*Claw\s*...` strip in
`web/app/tests/e2e/page-objects/panda-claw-chat.page.ts:300` with
`^[^\d]{0,40}\d{1,2}:\d{2}...`.
- Now strips any non-digit bot-name prefix (Assistant, Panda Claw,
Fullstack Assistant, future custom display names) so long as it precedes
the timestamp.

## Why
`OpenClawAssistantMessage.tsx:319` renders the header as `{botName ||
'Assistant'}`. The default fallback "Assistant" stopped matching the old
regex, so `getLastBotMessage()` returned strings with the prefix left
intact:

```
Response too short (17 chars, need 30+): "Assistant10:05 AM"
```

Observed in [run
26090184027](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/26090184027)
— the `session-features` Auto-titling scenario failed 3/3 retries with
this trace. The other scenarios that use
`assertResponseHasContent(response, 5)` *passed* spuriously: a 5-char
threshold clears even with just the residual prefix, so the assertion
was effectively vacuous (`feedback_assertion_falsifiability` material).

This is a sibling fix to #1736 (FeatureLaunchModal suppression). Both
are E2E-side maintenance burdens that fell out of sync with product
changes; the daily schedule re-enable (#1733) depends on these to land
clean.

## Test plan
- [x] Local regex sanity check on 8 representative inputs
(Assistant/PandaClaw/Panda Claw/Fullstack Assistant prefixes; 12h/24h
timestamps; with/without Copy/Reply suffix; short-streaming edge case) —
all strip correctly
- [x] `pnpm --filter @zooclaw/web-app lint` passes (pre-commit hook)
- [ ] After merge: dispatch ZooClaw E2E Tests on this branch and confirm
`session-features` auto-titling no longer fails on the prefix-strip
artefact

## Notes
- The `Copy|Reply` suffix strip is unchanged.
- `getLastBotMessage()` still has a known TODO: replace textContent
slicing with a data-testid scoped locator once the product side ships
one. That instrumentation belongs in a separate PR (touches
`web/app/src/...`).
- Video-reply failure in the same run is a separate, real product-side
regression (`assertHasVideoCard` waits 5 min for `main
video[controls]`). Tracking via separate issue.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1738 Body
## Summary
- Replaces the hardcoded `^Panda\s*Claw\s*...` strip in `web/app/tests/e2e/page-objects/panda-claw-chat.page.ts:300` with `^[^\d]{0,40}\d{1,2}:\d{2}...`.
- Now strips any non-digit bot-name prefix (Assistant, Panda Claw, Fullstack Assistant, future custom display names) so long as it precedes the timestamp.

## Why
`OpenClawAssistantMessage.tsx:319` renders the header as `{botName || 'Assistant'}`. The default fallback "Assistant" stopped matching the old regex, so `getLastBotMessage()` returned strings with the prefix left intact:

```
Response too short (17 chars, need 30+): "Assistant10:05 AM"
```

Observed in [run 26090184027](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/26090184027) — the `session-features` Auto-titling scenario failed 3/3 retries with this trace. The other scenarios that use `assertResponseHasContent(response, 5)` *passed* spuriously: a 5-char threshold clears even with just the residual prefix, so the assertion was effectively vacuous (`feedback_assertion_falsifiability` material).

This is a sibling fix to #1736 (FeatureLaunchModal suppression). Both are E2E-side maintenance burdens that fell out of sync with product changes; the daily schedule re-enable (#1733) depends on these to land clean.

## Test plan
- [x] Local regex sanity check on 8 representative inputs (Assistant/PandaClaw/Panda Claw/Fullstack Assistant prefixes; 12h/24h timestamps; with/without Copy/Reply suffix; short-streaming edge case) — all strip correctly
- [x] `pnpm --filter @zooclaw/web-app lint` passes (pre-commit hook)
- [ ] After merge: dispatch ZooClaw E2E Tests on this branch and confirm `session-features` auto-titling no longer fails on the prefix-strip artefact

## Notes
- The `Copy|Reply` suffix strip is unchanged.
- `getLastBotMessage()` still has a known TODO: replace textContent slicing with a data-testid scoped locator once the product side ships one. That instrumentation belongs in a separate PR (touches `web/app/src/...`).
- Video-reply failure in the same run is a separate, real product-side regression (`assertHasVideoCard` waits 5 min for `main video[controls]`). Tracking via separate issue.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [41dba220] chore(ci): align lark-cli-smoke with Node 24 / setup-node@v6 (#1742)
- **SHA:** 41dba2204dd1eee6f56956635d2f479b39af2f95
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-19T12:23:45Z

### Full Commit Message
```
chore(ci): align lark-cli-smoke with Node 24 / setup-node@v6 (#1742)

## Summary
- Bumps `lark-cli-smoke.yml` from `setup-node@v4` + `node-version: '20'`
to `setup-node@v6` + `node-version: '24'` to match every other workflow
in the repo (`code-quality`, `deploy`, `e2e`,
`dependabot-lockfile-refresh`).
- Silences the Node 20 deprecation annotation that's been appearing on
each run; Node 20 will be removed from runners on 2026-09-16 per
GitHub's schedule.
- Pure CI alignment, no behavior change to lark-cli or the credential
flow.

## Test plan
- [ ] Merge, trigger `gh workflow run lark-cli-smoke.yml --ref main`
- [ ] Confirm the run still lands a message in the ZooClaw Launch
Tracking group
- [ ] Confirm the Node 20 deprecation annotation is gone

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1742 Body
## Summary
- Bumps `lark-cli-smoke.yml` from `setup-node@v4` + `node-version: '20'` to `setup-node@v6` + `node-version: '24'` to match every other workflow in the repo (`code-quality`, `deploy`, `e2e`, `dependabot-lockfile-refresh`).
- Silences the Node 20 deprecation annotation that's been appearing on each run; Node 20 will be removed from runners on 2026-09-16 per GitHub's schedule.
- Pure CI alignment, no behavior change to lark-cli or the credential flow.

## Test plan
- [ ] Merge, trigger `gh workflow run lark-cli-smoke.yml --ref main`
- [ ] Confirm the run still lands a message in the ZooClaw Launch Tracking group
- [ ] Confirm the Node 20 deprecation annotation is gone

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [a384add8] feat(billing): Select Payment Method 弹窗UI优化 (#1735)
- **SHA:** a384add8ad230d714f2d17e424ebaacf7137be7b
- **Author:** lynn Zhuang
- **Date:** 2026-05-19T12:18:57Z

### Full Commit Message
```
feat(billing): Select Payment Method 弹窗UI优化 (#1735)

## 概要
- 按 Figma 节点 `2718:1057` 重做 Select Payment Method 弹窗：22px 加粗标题、右上角 X
关闭按钮、两个选项卡片（左对齐
radio + label + 真实品牌 logo 横排）、底部居中显示禁用提示。替换原本的 emoji 图标 + 底部 Cancel
按钮布局。
- 在 `web/app/public/billing/` 新增两个品牌资源：`card-brands.png`（Visa /
MasterCard / Amex / Discover 合并图）和
`alipay-logo.svg`（修掉了 Figma 导出时塞入的 `preserveAspectRatio="none"`，原本会导致
SVG
  拉伸填满父容器、长宽比失真）。
- `PaymentMethodModal` 的 props 接口和行为合约**完全不变**：已有的 5 个 unit test
无需任何修改直接通过（测试的是
  `onSelect / onClose / disabled / isOpen` 行为合约，不锁定 DOM 结构）。

  ## 测试清单
  - [ ] 打开 `/en/subscription`，点任意非当前 plan 的 Upgrade —— 新弹窗按重做后的布局渲染。
- [ ] Stripe 流程：点 Card 卡片 → 出现 spinner + "Opening..."，下方显示
secure-checkout 提示。
- [ ] Antom 流程：点 Alipay 卡片 → 出现 spinner + "Redirecting..."，下方显示 Alipay
跳转提示。
- [ ] 已订阅 Stripe 的活跃用户：Alipay 卡片显示禁用态 + 下方居中显示 "Cancel your current
subscription first to
  switch payment method."
  - [ ] 已订阅 Antom 的活跃用户：Card 卡片显示同样的禁用态。
  - [ ] 关闭路径：右上角 X、背景点击、Esc 都能正常关闭；`processingChannel`
  非空时这三种关闭方式都被禁用（防止支付跳转中被中断）。

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1735 Body
## 概要
  - 按 Figma 节点 `2718:1057` 重做 Select Payment Method 弹窗：22px 加粗标题、右上角 X 关闭按钮、两个选项卡片（左对齐
  radio + label + 真实品牌 logo 横排）、底部居中显示禁用提示。替换原本的 emoji 图标 + 底部 Cancel 按钮布局。
  - 在 `web/app/public/billing/` 新增两个品牌资源：`card-brands.png`（Visa / MasterCard / Amex / Discover 合并图）和
  `alipay-logo.svg`（修掉了 Figma 导出时塞入的 `preserveAspectRatio="none"`，原本会导致 SVG
  拉伸填满父容器、长宽比失真）。
  - `PaymentMethodModal` 的 props 接口和行为合约**完全不变**：已有的 5 个 unit test 无需任何修改直接通过（测试的是
  `onSelect / onClose / disabled / isOpen` 行为合约，不锁定 DOM 结构）。

  ## 测试清单
  - [ ] 打开 `/en/subscription`，点任意非当前 plan 的 Upgrade —— 新弹窗按重做后的布局渲染。
  - [ ] Stripe 流程：点 Card 卡片 → 出现 spinner + "Opening..."，下方显示 secure-checkout 提示。
  - [ ] Antom 流程：点 Alipay 卡片 → 出现 spinner + "Redirecting..."，下方显示 Alipay 跳转提示。
  - [ ] 已订阅 Stripe 的活跃用户：Alipay 卡片显示禁用态 + 下方居中显示 "Cancel your current subscription first to
  switch payment method."
  - [ ] 已订阅 Antom 的活跃用户：Card 卡片显示同样的禁用态。
  - [ ] 关闭路径：右上角 X、背景点击、Esc 都能正常关闭；`processingChannel`
  非空时这三种关闭方式都被禁用（防止支付跳转中被中断）。

---

## [01ec8a87] fix(ci): mint TAT in workflow; env provider is token-only (#1741)
- **SHA:** 01ec8a87027c3fbd37ab279d9f28896da63cc838
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-19T12:18:43Z

### Full Commit Message
```
fix(ci): mint TAT in workflow; env provider is token-only (#1741)

## Summary
- Previous run (after merging #1740) failed with `no access token
available for bot` despite `LARKSUITE_CLI_APP_ID` /
`LARKSUITE_CLI_APP_SECRET` being correctly populated.
- Root cause is in lark-cli itself: the env-provider path is a
**static-token bridge**, not a TAT-minting client. When env vars are
present the provider locks itself in as the sole token source
(`internal/credential/credential_provider.go:203`) and the default
TAT-minting path becomes unreachable. The env provider's `ResolveToken`
(`extension/credential/env/env.go:97`) only forwards pre-existing
UAT/TAT — there is no HTTP call to
`/open-apis/auth/v3/tenant_access_token/internal`. The
`runtimePlaceholderAppSecret` marker at
`internal/credential/types.go:29` confirms the design intent: token-only
sources are first-class.
- Fix: mint a fresh TAT directly in the workflow (a single curl call)
and pass it through `LARKSUITE_CLI_TENANT_ACCESS_TOKEN`. The send step
no longer needs `APP_SECRET` at all — secret exposure is reduced to a
single step.

## Test plan
- [ ] Merge, trigger `gh workflow run lark-cli-smoke.yml --ref main`
- [ ] Confirm `Mint tenant_access_token` step exits 0 and the TAT does
not appear unmasked in logs
- [ ] Confirm `Send test message` step lands a message "GitHub Actions
测试消息 — run <id>" in the ZooClaw Launch Tracking group
- [ ] If `Mint` fails: diagnostic line `TAT mint failed:
{"code":N,"msg":"..."}` will reveal whether it's wrong app_id/app_secret
vs. an app-side configuration issue

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1741 Body
## Summary
- Previous run (after merging #1740) failed with `no access token available for bot` despite `LARKSUITE_CLI_APP_ID` / `LARKSUITE_CLI_APP_SECRET` being correctly populated.
- Root cause is in lark-cli itself: the env-provider path is a **static-token bridge**, not a TAT-minting client. When env vars are present the provider locks itself in as the sole token source (`internal/credential/credential_provider.go:203`) and the default TAT-minting path becomes unreachable. The env provider's `ResolveToken` (`extension/credential/env/env.go:97`) only forwards pre-existing UAT/TAT — there is no HTTP call to `/open-apis/auth/v3/tenant_access_token/internal`. The `runtimePlaceholderAppSecret` marker at `internal/credential/types.go:29` confirms the design intent: token-only sources are first-class.
- Fix: mint a fresh TAT directly in the workflow (a single curl call) and pass it through `LARKSUITE_CLI_TENANT_ACCESS_TOKEN`. The send step no longer needs `APP_SECRET` at all — secret exposure is reduced to a single step.

## Test plan
- [ ] Merge, trigger `gh workflow run lark-cli-smoke.yml --ref main`
- [ ] Confirm `Mint tenant_access_token` step exits 0 and the TAT does not appear unmasked in logs
- [ ] Confirm `Send test message` step lands a message "GitHub Actions 测试消息 — run <id>" in the ZooClaw Launch Tracking group
- [ ] If `Mint` fails: diagnostic line `TAT mint failed: {"code":N,"msg":"..."}` will reveal whether it's wrong app_id/app_secret vs. an app-side configuration issue

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [db66c9b4] feat(ci): switch lark-cli smoke to real bot message send (#1740)
- **SHA:** db66c9b4e834aeaddb3f9c8c463c27dfbe94f85a
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-19T12:10:26Z

### Full Commit Message
```
feat(ci): switch lark-cli smoke to real bot message send (#1740)

## Summary
- Replaces the `auth status --verify` step with a real `im
+messages-send` to the **ZooClaw Launch Tracking** topic group
(`oc_213291d2715a9d02bf5b0bb18b847e3c`).
- `auth status` was returning `external_provider` (designed for local
keychain mode, refuses env-provided creds — see `cmd/auth/auth.go:35`);
it never actually hit the Feishu API. The new step exercises the full
path: env provider → tenant_access_token → Feishu open API.
- Message body includes `${{ github.run_id }}` so each run is
distinguishable in the group.
- `chat_id` hard-coded on purpose (different future workflows →
different groups; a shared org variable would couple them).

## Operational prereqs (must be true before this can pass)
- [x] Org secrets `LARKSUITE_CLI_APP_ID` / `LARKSUITE_CLI_APP_SECRET`
filled with real values
- [ ] The GH Actions bot is a member of the ZooClaw Launch Tracking
group (`oc_213291d2715a9d02bf5b0bb18b847e3c`) — confirmed pulled in by
chris-srp
- [ ] The bot has `im:message` scope granted in the Feishu developer
console

## Test plan
- [ ] Merge, then trigger via `gh workflow run lark-cli-smoke.yml --ref
main`
- [ ] Confirm the workflow lands green and a "GitHub Actions 测试消息 — run
<id>" message appears in the ZooClaw Launch Tracking group
- [ ] If red: failure mode will be one of (a) bot not in chat, (b)
missing scope, (c) wrong app_id/app_secret — log line in the failed step
will identify which

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1740 Body
## Summary
- Replaces the `auth status --verify` step with a real `im +messages-send` to the **ZooClaw Launch Tracking** topic group (`oc_213291d2715a9d02bf5b0bb18b847e3c`).
- `auth status` was returning `external_provider` (designed for local keychain mode, refuses env-provided creds — see `cmd/auth/auth.go:35`); it never actually hit the Feishu API. The new step exercises the full path: env provider → tenant_access_token → Feishu open API.
- Message body includes `${{ github.run_id }}` so each run is distinguishable in the group.
- `chat_id` hard-coded on purpose (different future workflows → different groups; a shared org variable would couple them).

## Operational prereqs (must be true before this can pass)
- [x] Org secrets `LARKSUITE_CLI_APP_ID` / `LARKSUITE_CLI_APP_SECRET` filled with real values
- [ ] The GH Actions bot is a member of the ZooClaw Launch Tracking group (`oc_213291d2715a9d02bf5b0bb18b847e3c`) — confirmed pulled in by chris-srp
- [ ] The bot has `im:message` scope granted in the Feishu developer console

## Test plan
- [ ] Merge, then trigger via `gh workflow run lark-cli-smoke.yml --ref main`
- [ ] Confirm the workflow lands green and a "GitHub Actions 测试消息 — run <id>" message appears in the ZooClaw Launch Tracking group
- [ ] If red: failure mode will be one of (a) bot not in chat, (b) missing scope, (c) wrong app_id/app_secret — log line in the failed step will identify which

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [5eae6bc6] test(e2e): suppress FeatureLaunchModal overlay (#1736)
- **SHA:** 5eae6bc6b2f7e9dcf1c25229c6b616b0efb276c1
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-19T11:59:46Z

### Full Commit Message
```
test(e2e): suppress FeatureLaunchModal overlay (#1736)

## Summary
- Adds `'ecap:feature-launch-seen:{uid}': '1'` to
`E2E_OVERLAY_SUPPRESSION` in `web/app/tests/e2e/fixtures/test-data.ts`.
- Mirrors the existing per-user `ecap:seedance-launch-seen:{uid}` entry;
`auth.setup.ts` already does the `{uid}` → real-uid substitution.

## Why
`FeatureLaunchModal` (`web/app/src/components/FeatureLaunchModal.tsx`)
renders a fixed-inset backdrop with `z-50` that intercepts pointer
events on the chat page until dismissed. Because its dismiss key
(`STORAGE_KEYS.FEATURE_LAUNCH_SEEN = 'ecap:feature-launch-seen'`) was
not in the suppression map, the daily E2E run is blocked at
`chatSession` fixture setup:

> `<div data-testid=\"feature-launch-backdrop\"
data-sentry-component=\"FeatureLaunchModal\" ...> intercepts pointer
events`

Observed in run
[26087647063](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/26087647063):
7 scenarios failed (chat-smoke, voice-reply, web-search, browser,
document/python, weather, auto-titling) and 12 were skipped because the
shared session never reached "ready".

This is the same shape of fix as #1229 (`bc28a16f`) — the suppression
map needs an entry every time a new blocking overlay ships.

## Test plan
- [x] `pnpm --filter @zooclaw/web-app lint` passes (pre-commit hook)
- [ ] `gh workflow run \"ZooClaw E2E Tests\" --ref
feature/fix-e2e-feature-launch-modal -f base_url=https://zooclaw.ai`
reaches green
- [ ] Merge order: this PR → then re-trigger #1733 (daily schedule
re-enable) to confirm the cron path is clean before that one merges

## Notes
- Did **not** clean up the stale `ecap:seedance-launch-seen:{uid}` entry
(`SeedanceLaunchModal.tsx` no longer exists in the repo) or the outdated
`web/src/...` paths in the docstring above — both belong in a separate
cleanup PR to keep this fix minimal.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1736 Body
## Summary
- Adds `'ecap:feature-launch-seen:{uid}': '1'` to `E2E_OVERLAY_SUPPRESSION` in `web/app/tests/e2e/fixtures/test-data.ts`.
- Mirrors the existing per-user `ecap:seedance-launch-seen:{uid}` entry; `auth.setup.ts` already does the `{uid}` → real-uid substitution.

## Why
`FeatureLaunchModal` (`web/app/src/components/FeatureLaunchModal.tsx`) renders a fixed-inset backdrop with `z-50` that intercepts pointer events on the chat page until dismissed. Because its dismiss key (`STORAGE_KEYS.FEATURE_LAUNCH_SEEN = 'ecap:feature-launch-seen'`) was not in the suppression map, the daily E2E run is blocked at `chatSession` fixture setup:

> `<div data-testid=\"feature-launch-backdrop\" data-sentry-component=\"FeatureLaunchModal\" ...> intercepts pointer events`

Observed in run [26087647063](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/26087647063): 7 scenarios failed (chat-smoke, voice-reply, web-search, browser, document/python, weather, auto-titling) and 12 were skipped because the shared session never reached "ready".

This is the same shape of fix as #1229 (`bc28a16f`) — the suppression map needs an entry every time a new blocking overlay ships.

## Test plan
- [x] `pnpm --filter @zooclaw/web-app lint` passes (pre-commit hook)
- [ ] `gh workflow run \"ZooClaw E2E Tests\" --ref feature/fix-e2e-feature-launch-modal -f base_url=https://zooclaw.ai` reaches green
- [ ] Merge order: this PR → then re-trigger #1733 (daily schedule re-enable) to confirm the cron path is clean before that one merges

## Notes
- Did **not** clean up the stale `ecap:seedance-launch-seen:{uid}` entry (`SeedanceLaunchModal.tsx` no longer exists in the repo) or the outdated `web/src/...` paths in the docstring above — both belong in a separate cleanup PR to keep this fix minimal.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [a1212d5c] feat(ci): add lark-cli smoke workflow (#1737)
- **SHA:** a1212d5c95c0d71b9e568f1ac38292dba740cdbe
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-19T11:56:23Z

### Full Commit Message
```
feat(ci): add lark-cli smoke workflow (#1737)

## Summary
- Adds `.github/workflows/lark-cli-smoke.yml` — a manual-trigger
workflow that installs `@larksuite/cli` and runs `lark-cli auth status
--verify` to validate the org-level lark-cli credential path end-to-end.
- Wires the workflow to the newly-created org secrets
(`LARKSUITE_CLI_APP_ID`, `LARKSUITE_CLI_APP_SECRET`) and variables
(`LARKSUITE_CLI_BRAND`, `LARKSUITE_CLI_DEFAULT_AS`,
`LARKSUITE_CLI_STRICT_MODE`, `LARKSUITE_CLI_NO_UPDATE_NOTIFIER`,
`LARKSUITE_CLI_NO_SKILLS_NOTIFIER`).
- `permissions: {}` — workflow needs no GITHUB_TOKEN powers; trigger is
`workflow_dispatch` only so it stays out of PR status checks.

## Test plan
- [ ] Go to Actions → "lark-cli smoke" → Run workflow on
`feat/lark-cli-smoke`
- [ ] Confirm `auth status --verify` step prints JSON with `identity:
"bot"` / `verified: true` and the job is green
- [ ] Re-run on `main` after merge to confirm the baseline works there
too

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1737 Body
## Summary
- Adds `.github/workflows/lark-cli-smoke.yml` — a manual-trigger workflow that installs `@larksuite/cli` and runs `lark-cli auth status --verify` to validate the org-level lark-cli credential path end-to-end.
- Wires the workflow to the newly-created org secrets (`LARKSUITE_CLI_APP_ID`, `LARKSUITE_CLI_APP_SECRET`) and variables (`LARKSUITE_CLI_BRAND`, `LARKSUITE_CLI_DEFAULT_AS`, `LARKSUITE_CLI_STRICT_MODE`, `LARKSUITE_CLI_NO_UPDATE_NOTIFIER`, `LARKSUITE_CLI_NO_SKILLS_NOTIFIER`).
- `permissions: {}` — workflow needs no GITHUB_TOKEN powers; trigger is `workflow_dispatch` only so it stays out of PR status checks.

## Test plan
- [ ] Go to Actions → "lark-cli smoke" → Run workflow on `feat/lark-cli-smoke`
- [ ] Confirm `auth status --verify` step prints JSON with `identity: "bot"` / `verified: true` and the job is green
- [ ] Re-run on `main` after merge to confirm the baseline works there too

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [e2991e83] ci(e2e): re-enable daily schedule for ZooClaw E2E tests (#1733)
- **SHA:** e2991e836348c4f86f72fc020f9d473e56d56355
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-19T09:55:54Z

### Full Commit Message
```
ci(e2e): re-enable daily schedule for ZooClaw E2E tests (#1733)

## Summary
- Uncomments the `schedule: cron '0 0 * * *'` block in
`.github/workflows/e2e.yml` that was muted in PR #83 alongside an
unrelated race-condition fix.
- Restores the daily 00:00 UTC (08:00 UTC+8) production E2E run.
- No other workflow logic changes — the existing `setup` job already
routes the `schedule` event to `https://zooclaw.ai` / `e2e-production`.

## Why now
After PR #83 the suite was iteratively stabilized (#1028 base-URL
migration, #1140 stale-domain cleanup, #1229 overlay suppression +
response detection). Manual `workflow_dispatch` runs against production
now pass reliably, so the daily heartbeat is worth turning back on.

## Test plan
- [x] `python3 -c "import yaml;
yaml.safe_load(open('.github/workflows/e2e.yml'))"` — YAML parses
- [x] `git diff` limited to the 3 comment markers, no semantic changes
elsewhere
- [ ] Manual `gh workflow run "ZooClaw E2E Tests" --ref
feature/re-enable-daily-e2e-tests -f base_url=https://zooclaw.ai` passes
on this branch
- [ ] After merge: confirm `gh run list --workflow=e2e.yml
--event=schedule` shows a new run the morning after merge

## Notes
- GitHub Actions `schedule` only fires on the repository's default
branch, so the cron only becomes active once this PR merges to `main`.
- Rollback path if the daily run becomes noisy again: a single commit
re-adding the 3 `#` markers.
- The `notify` job already pages Feishu on failure/cancelled — no new
monitoring wiring needed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1733 Body
## Summary
- Uncomments the `schedule: cron '0 0 * * *'` block in `.github/workflows/e2e.yml` that was muted in PR #83 alongside an unrelated race-condition fix.
- Restores the daily 00:00 UTC (08:00 UTC+8) production E2E run.
- No other workflow logic changes — the existing `setup` job already routes the `schedule` event to `https://zooclaw.ai` / `e2e-production`.

## Why now
After PR #83 the suite was iteratively stabilized (#1028 base-URL migration, #1140 stale-domain cleanup, #1229 overlay suppression + response detection). Manual `workflow_dispatch` runs against production now pass reliably, so the daily heartbeat is worth turning back on.

## Test plan
- [x] `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/e2e.yml'))"` — YAML parses
- [x] `git diff` limited to the 3 comment markers, no semantic changes elsewhere
- [ ] Manual `gh workflow run "ZooClaw E2E Tests" --ref feature/re-enable-daily-e2e-tests -f base_url=https://zooclaw.ai` passes on this branch
- [ ] After merge: confirm `gh run list --workflow=e2e.yml --event=schedule` shows a new run the morning after merge

## Notes
- GitHub Actions `schedule` only fires on the repository's default branch, so the cron only becomes active once this PR merges to `main`.
- Rollback path if the daily run becomes noisy again: a single commit re-adding the 3 `#` markers.
- The `notify` job already pages Feishu on failure/cancelled — no new monitoring wiring needed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [fff5a50b] fix(subscription): complete ECA-681 reconciliation phase 2.5 (#1732)
- **SHA:** fff5a50b468d287b1ce1e8e4defc4dda35e0c06f
- **Author:** kaka-srp
- **Date:** 2026-05-19T09:26:43Z

### Full Commit Message
```
fix(subscription): complete ECA-681 reconciliation phase 2.5 (#1732)

## Summary

- Extend Stripe/Mongo reconciliation for Phase 2.5 drift classes:
plan/billing/product drift, legacy monthly product mapping,
unknown-product detection, mixed-provider Stripe residue, and
plan-correction resource sync.
- Add BG active-subscription detection for yearly cron renewals so
missing BG subscriptions are recreated without `ending_at` before wallet
refill, while healthy active BG subscriptions are left untouched.
- Add Apple production subscription-status fallback to Sandbox and
update cron/runbook docs with the current production scheduler gaps: BG
reconcile flow missing, stale `check-grace-expiry` hourly node, and
orphan monitor cadence mismatch.

## Verification

- `/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_billing_subscriptions.py
tests/unit/test_stripe_reconcile.py tests/unit/test_apple_service.py
tests/unit/test_subscription_manager.py
tests/unit/test_process_cron_renewal.py` — 124 passed
- `/home/node/.venvs/claw-interface/bin/ruff format --check app
tests/unit/test_billing_subscriptions.py
tests/unit/test_stripe_reconcile.py tests/unit/test_apple_service.py
tests/unit/test_subscription_manager.py
tests/unit/test_process_cron_renewal.py`
- `/home/node/.venvs/claw-interface/bin/ruff check app
tests/unit/test_billing_subscriptions.py
tests/unit/test_stripe_reconcile.py tests/unit/test_apple_service.py
tests/unit/test_subscription_manager.py
tests/unit/test_process_cron_renewal.py`
- `/home/node/.venvs/claw-interface/bin/pyright --pythonpath
/home/node/.venvs/claw-interface/bin/python app tests/`
- `git diff --check origin/main...HEAD`

Linear: ECA-681
```

### PR #1732 Body
## Summary

- Extend Stripe/Mongo reconciliation for Phase 2.5 drift classes: plan/billing/product drift, legacy monthly product mapping, unknown-product detection, mixed-provider Stripe residue, and plan-correction resource sync.
- Add BG active-subscription detection for yearly cron renewals so missing BG subscriptions are recreated without `ending_at` before wallet refill, while healthy active BG subscriptions are left untouched.
- Add Apple production subscription-status fallback to Sandbox and update cron/runbook docs with the current production scheduler gaps: BG reconcile flow missing, stale `check-grace-expiry` hourly node, and orphan monitor cadence mismatch.

## Verification

- `/home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_billing_subscriptions.py tests/unit/test_stripe_reconcile.py tests/unit/test_apple_service.py tests/unit/test_subscription_manager.py tests/unit/test_process_cron_renewal.py` — 124 passed
- `/home/node/.venvs/claw-interface/bin/ruff format --check app tests/unit/test_billing_subscriptions.py tests/unit/test_stripe_reconcile.py tests/unit/test_apple_service.py tests/unit/test_subscription_manager.py tests/unit/test_process_cron_renewal.py`
- `/home/node/.venvs/claw-interface/bin/ruff check app tests/unit/test_billing_subscriptions.py tests/unit/test_stripe_reconcile.py tests/unit/test_apple_service.py tests/unit/test_subscription_manager.py tests/unit/test_process_cron_renewal.py`
- `/home/node/.venvs/claw-interface/bin/pyright --pythonpath /home/node/.venvs/claw-interface/bin/python app tests/`
- `git diff --check origin/main...HEAD`

Linear: ECA-681


---

## [6156b852] docs(architecture): add user-interface (account/auth service) component (#1722)
- **SHA:** 6156b852bebe3c5ff3530003aff9f59007431309
- **Author:** Chris@ZooClaw
- **Date:** 2026-05-19T08:22:26Z

### Full Commit Message
```
docs(architecture): add user-interface (account/auth service) component (#1722)

## Summary
- Documents the `user-interface` service (called by `claw-interface`) as
a first-class component in `architecture.md` + `architecture.zh-CN.md` —
it owns end-user identity (JWT verify, account creation, agent-email
provisioning, warm-pool admin), which until now was implicit in the env
vars and scattered code refs.
- Calls out a previously-unstated boundary: this repo's Mongo `user`
collection holds billing/preference state keyed by `uid`, but the `uid`
itself, credentials, agent emails, and warm-pool records all live in
`user-interface`.
- Mirrors the change in both EN and zh-CN versions; new diagram node +
edge are appended at the end so existing `linkStyle` indices for the WS
(amber) and Lago (emerald) paths stay valid.

## Changes per section
- **A. Architecture** — new `ui` node, `claw → ui` edge labeled
`NEXT_PUBLIC_ACCOUNT_URL`, new `auth` style class (teal), plus a 5th
property bullet about identity authority.
- **B. External repository inventory** — new row for
`SerendipityOneInc/user-interface`.
- **C. Data flows** — new "User auth & identity" subsection with code
refs:
- `services/claw-interface/app/auth/token_verifier.py:52-55` (JWT
verify)
- `app/services/agent_identity.py:121` +
`app/services/openclaw/bot_config.py:301-304` (agent email)
- `app/services/account_service_warm_pool.py`,
`warm_pool_provisioner.py` (warm pool)
  - `web/app/tests/.../middleware.unit.spec.ts` (browser-side verify)
- **D. Where deployed versions live** — added as another exception to
`gcp-foundation` (deployed by its own repo's CI/CD).
- **E. Env var → service map** — added `NEXT_PUBLIC_ACCOUNT_URL`,
`AGENT_IDENTITY_ADMIN_KEY`, `WARM_POOL_ACCOUNT_SERVICE_ADMIN_TOKEN`.

## Test plan
- [ ] Open `architecture.md` on GitHub and confirm the Mermaid diagram
renders (new teal `ui` node visible, WS edges still amber, LiteLLM→Lago
edge still bold emerald).
- [ ] Open `architecture.zh-CN.md` on GitHub and confirm the same
diagram renders with Chinese labels.
- [ ] Spot-check the code-ref line numbers in Section C still match
`main`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1722 Body
## Summary
- Documents the `user-interface` service (called by `claw-interface`) as a first-class component in `architecture.md` + `architecture.zh-CN.md` — it owns end-user identity (JWT verify, account creation, agent-email provisioning, warm-pool admin), which until now was implicit in the env vars and scattered code refs.
- Calls out a previously-unstated boundary: this repo's Mongo `user` collection holds billing/preference state keyed by `uid`, but the `uid` itself, credentials, agent emails, and warm-pool records all live in `user-interface`.
- Mirrors the change in both EN and zh-CN versions; new diagram node + edge are appended at the end so existing `linkStyle` indices for the WS (amber) and Lago (emerald) paths stay valid.

## Changes per section
- **A. Architecture** — new `ui` node, `claw → ui` edge labeled `NEXT_PUBLIC_ACCOUNT_URL`, new `auth` style class (teal), plus a 5th property bullet about identity authority.
- **B. External repository inventory** — new row for `SerendipityOneInc/user-interface`.
- **C. Data flows** — new "User auth & identity" subsection with code refs:
  - `services/claw-interface/app/auth/token_verifier.py:52-55` (JWT verify)
  - `app/services/agent_identity.py:121` + `app/services/openclaw/bot_config.py:301-304` (agent email)
  - `app/services/account_service_warm_pool.py`, `warm_pool_provisioner.py` (warm pool)
  - `web/app/tests/.../middleware.unit.spec.ts` (browser-side verify)
- **D. Where deployed versions live** — added as another exception to `gcp-foundation` (deployed by its own repo's CI/CD).
- **E. Env var → service map** — added `NEXT_PUBLIC_ACCOUNT_URL`, `AGENT_IDENTITY_ADMIN_KEY`, `WARM_POOL_ACCOUNT_SERVICE_ADMIN_TOKEN`.

## Test plan
- [ ] Open `architecture.md` on GitHub and confirm the Mermaid diagram renders (new teal `ui` node visible, WS edges still amber, LiteLLM→Lago edge still bold emerald).
- [ ] Open `architecture.zh-CN.md` on GitHub and confirm the same diagram renders with Chinese labels.
- [ ] Spot-check the code-ref line numbers in Section C still match `main`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
