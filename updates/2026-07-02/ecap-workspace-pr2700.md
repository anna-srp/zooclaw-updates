---
title: "修复 Firefox 下偶发「无法验证会话」黑屏问题"
type: "Bug Fix"
priority: "中"
date: "2026-07-02"
status: "待审核"
channels: ""
---
# 修复 Firefox 下偶发「无法验证会话」黑屏问题
## 核心宣传点
网络瞬断或浏览器（尤其 Firefox）请求偶发失败时，系统会自动重试登录校验，不再直接黑屏提示「Unable to verify your session」。
## 原始内容
### [ecap-workspace PR #2700]

fix(auth): retry /api/auth/me on transport-layer failures (ECA-1154) (#2700)

<!-- PR 标题：fix(scope): description —— 必须遵循 Conventional Commits -->

Linear: https://linear.app/srpone/issue/ECA-1154

## Summary
- 在 `useAccountMeQuery` 的 retry predicate 里增加对**传输层失败**（Firefox
`TypeError: NetworkError when attempting to fetch resource`、Chrome
`TypeError: Failed to fetch`、`AbortError`）的识别，最多 3 次退避重试（500ms / 1500ms
/ 3000ms）。
- 原有的 404 `account.not_found` / 401 legacy `"Account not found, please
register"` 引导注册重试路径完全保留，不改动 delay 序列。
- 把 retry 判定和 delay 抽成命名函数（`shouldRetryAccountMeQuery` /
`accountMeRetryDelayMs`）并导出，让预判逻辑可直接单测。
- 新增 12 个单元断言覆盖：Firefox / Chrome / AbortError 三种传输层形态、重试上限 3、原有
bootstrap-pending 行为、真正的 401/403/5xx **不重试**、null/undefined
**不重试**、delay 槽位与上限。

## Root cause
ECA-1154 报障：Nemo 用 Firefox 152 (Linux) 打开 Zooclaw，`/api/auth/me` 在传输层直接抛
`TypeError: NetworkError`（无 HTTP status），`useAccountMeQuery` 的旧 retry 谓词
`isAccountBootstrapPendingError` 只识别 `ApiError` 且 status ∈ {404,
401}，所以传输层错误 **一次都不重试**，直接落到 `AccountSessionGate` 非 auth-error 分支 →
用户看到「Unable to verify your session」黑屏，只能手动 Retry。Firefox 报此错的一秒稳定复现 =
Firefox 对短暂网络中断 / 边缘策略变化的容错比 Chrome 更严格；本次不定位 Firefox-only 的具体触发源（可能是
Cloudflare Worker / CORS / SameSite），先修补客户端容错。

## Test plan
- [x] `bash scripts/verify-web.sh src/hooks/queries/useAccountMeQuery.ts
tests/unit/hooks/queries/useAccountMeQuery.unit.spec.ts` — 8 guards +
tsc + vitest (12/12) + eslint 全绿
- [ ] CI `code-quality / lint-and-test` 全绿
- [ ] 手动验证（合并到 staging 后，Firefox 152）：DevTools Network → Offline 快速开关
1-2 秒，模拟传输层瞬时失败；会话验证应在 3 次退避内自愈，不再落到手动 Retry 页
- [ ] 回归：真实 401（token 过期）仍应触发 `router.replace('/')`，不进入重试循环

## Out of scope（避免和 ticket 二次误诊）
- Ticket 的「结论二」（bot pod `openclaw.sqlite` init WARN）**不在本 PR 内**。经诊断为
`openclaw-docker` PR #152 (`fix(litestream): per-version configs to stop
benign db-init-timeout noise`) 已明确定性为**良性日志噪声**，是 stale image 上残留的
litestream config 引用（Nemo 的 bot 目前在 `2026.5.7.63`，`Up to date:
false`；已单独 restart 验证过 bot 功能正常）。本 PR 只修真正影响用户可见的前端容错缺陷。
- 未额外调整 `AccountSessionGate.tsx`。原来的 manual Retry 按钮作为「3
次自动重试仍失败」的兜底继续存在，UX 语义合理，不做扩大化改动。

---

## PR Description

<!-- PR 标题：fix(scope): description —— 必须遵循 Conventional Commits -->

Linear: https://linear.app/srpone/issue/ECA-1154

## Summary
- 在 `useAccountMeQuery` 的 retry predicate 里增加对**传输层失败**（Firefox `TypeError: NetworkError when attempting to fetch resource`、Chrome `TypeError: Failed to fetch`、`AbortError`）的识别，最多 3 次退避重试（500ms / 1500ms / 3000ms）。
- 原有的 404 `account.not_found` / 401 legacy `"Account not found, please register"` 引导注册重试路径完全保留，不改动 delay 序列。
- 把 retry 判定和 delay 抽成命名函数（`shouldRetryAccountMeQuery` / `accountMeRetryDelayMs`）并导出，让预判逻辑可直接单测。
- 新增 12 个单元断言覆盖：Firefox / Chrome / AbortError 三种传输层形态、重试上限 3、原有 bootstrap-pending 行为、真正的 401/403/5xx **不重试**、null/undefined **不重试**、delay 槽位与上限。

## Root cause
ECA-1154 报障：Nemo 用 Firefox 152 (Linux) 打开 Zooclaw，`/api/auth/me` 在传输层直接抛 `TypeError: NetworkError`（无 HTTP status），`useAccountMeQuery` 的旧 retry 谓词 `isAccountBootstrapPendingError` 只识别 `ApiError` 且 status ∈ {404, 401}，所以传输层错误 **一次都不重试**，直接落到 `AccountSessionGate` 非 auth-error 分支 → 用户看到「Unable to verify your session」黑屏，只能手动 Retry。Firefox 报此错的一秒稳定复现 = Firefox 对短暂网络中断 / 边缘策略变化的容错比 Chrome 更严格；本次不定位 Firefox-only 的具体触发源（可能是 Cloudflare Worker / CORS / SameSite），先修补客户端容错。

## Test plan
- [x] `bash scripts/verify-web.sh src/hooks/queries/useAccountMeQuery.ts tests/unit/hooks/queries/useAccountMeQuery.unit.spec.ts` — 8 guards + tsc + vitest (12/12) + eslint 全绿
- [ ] CI `code-quality / lint-and-test` 全绿
- [ ] 手动验证（合并到 staging 后，Firefox 152）：DevTools Network → Offline 快速开关 1-2 秒，模拟传输层瞬时失败；会话验证应在 3 次退避内自愈，不再落到手动 Retry 页
- [ ] 回归：真实 401（token 过期）仍应触发 `router.replace('/')`，不进入重试循环

## Out of scope（避免和 ticket 二次误诊）
- Ticket 的「结论二」（bot pod `openclaw.sqlite` init WARN）**不在本 PR 内**。经诊断为 `openclaw-docker` PR #152 (`fix(litestream): per-version configs to stop benign db-init-timeout noise`) 已明确定性为**良性日志噪声**，是 stale image 上残留的 litestream config 引用（Nemo 的 bot 目前在 `2026.5.7.63`，`Up to date: false`；已单独 restart 验证过 bot 功能正常）。本 PR 只修真正影响用户可见的前端容错缺陷。
- 未额外调整 `AccountSessionGate.tsx`。原来的 manual Retry 按钮作为「3 次自动重试仍失败」的兜底继续存在，UX 语义合理，不做扩大化改动。

