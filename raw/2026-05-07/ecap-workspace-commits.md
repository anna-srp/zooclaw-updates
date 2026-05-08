# ecap-workspace commits - 2026-05-07

## 67f57864 - feat(wecom): add WeCom channel via QR scan + manual fallback (#1571)

- **SHA**: 67f57864eddad17e8fcbf90466cc8f829bb41a5b
- **作者**: kaka-srp
- **日期**: 2026-05-07T09:55:17Z
- **PR**: #1571 https://github.com/SerendipityOneInc/ecap-workspace/pull/1571

### Commit Message

```
feat(wecom): add WeCom channel via QR scan + manual fallback (#1571)

## Summary

ECA-625: add WeCom (企业微信) as a first-class ZooClaw channel, modeled on
the existing WeChat / Feishu QR-scan flows.

- **Pure-QR setup**: backend hits
`https://work.weixin.qq.com/ai/qc/{generate,query_result}` (the upstream
`@wecom/wecom-openclaw-cli` API) to mint a fresh WeCom bot via QR scan.
On confirm, credentials (`botId` + `secret`) are pushed to FastClaw via
`add_channel` and the bot pod's plugin reload picks them up.
- **Manual fallback**: WeCom mobile only mints a *new* bot per scan, so
users with an existing bot can't reuse it via QR. An "advanced mode"
toggle exposes a Bot ID / Secret form alongside the QR CTA.
- **Multi-account**: the account-id input is shown for WeCom (defaults
to `default`), so users can connect multiple WeCom bots side-by-side.
Backend round-trips `request.account` through the session into the
FastClaw payload.
- **Auto-refresh on success**: `WecomSetupModal` fires `onSuccess`
immediately on phase=success so the channel list updates without waiting
for the user to dismiss the success card.

## Cross-repo dependency

Depends on **fastclaw v0.0.108** (PR
https://github.com/SerendipityOneInc/fastclaw/pull/85), already deployed
to staging. That PR adds `BotID` / `Secret` to FastClaw's
`AddChannelRequest` struct so the credentials don't get silently dropped
by Go's JSON binder.

## Notable implementation details

- **Source param `source=wecom-cli`** — matches the upstream CLI; WeCom
server may gate on this string. A status_code is logged on every
QR-generate failure so a sustained shift would be detectable.
- **Poll error handling** — transient `httpx.TimeoutException` /
`NetworkError` / `429 rate-limited` keep the session alive (return
`pending`); only hard 4xx/5xx and other exceptions terminate setup.
- **5s polling cadence** — matches WeChat / Feishu modals (upstream CLI
uses 3s; we don't want WeCom to throttle us harder than the others).
- **No pod-side credential file** — unlike WeChat which writes
`~/.openclaw/openclaw-weixin/accounts/{id}.json`, WeCom's plugin reads
everything from `openclaw.json` directly, so credentials go in the
channel-config blob via `add_channel` only.

## Test plan

- [x] Backend: 20 unit tests in
`tests/unit/test_openclaw_settings_wecom.py` (setup/poll/cancel happy
paths + transient/429/503 error branches + multi-account round-trip +
pairing-policy `allowFrom` invariant)
- [x] Frontend: 64 unit tests across `WecomSetupModal.unit.spec.tsx` and
`ChannelsSection.unit.spec.tsx` (QR phase machine, multi-account
propagation, advanced/manual mode toggle, auto-refresh on success)
- [x] End-to-end on staging openclaw cluster — QR scan → bot pod's
`~/.openclaw/openclaw.json` shows
`channels.wecom.accounts.<account>.{botId, secret, dmPolicy,
groupPolicy, allowFrom}` correctly persisted
- [x] Channel removal — generic `client.remove_channel()` path cleans up
the entire `channels.wecom` node

## Note on pre-existing test failures

The full `pytest --cov=app` suite shows 8 failures + 5 errors in
unrelated files (`test_invite_codes.py`,
`test_mattermost_provisioner.py`, `test_openclaw_agents.py`,
`test_redis_client.py`, `test_storage.py`, etc.) — all triggered by
`PytestUnraisableExceptionWarning` cascades. Verified these reproduce on
`origin/main` without any of this PR's changes; tracked by PR #1567
(`promote stdlib ignore::ResourceWarning`). Not blocking ECA-625.
```

### PR Description

## Summary

ECA-625: add WeCom (企业微信) as a first-class ZooClaw channel, modeled on the existing WeChat / Feishu QR-scan flows.

- **Pure-QR setup**: backend hits `https://work.weixin.qq.com/ai/qc/{generate,query_result}` (the upstream `@wecom/wecom-openclaw-cli` API) to mint a fresh WeCom bot via QR scan. On confirm, credentials (`botId` + `secret`) are pushed to FastClaw via `add_channel` and the bot pod's plugin reload picks them up.
- **Manual fallback**: WeCom mobile only mints a *new* bot per scan, so users with an existing bot can't reuse it via QR. An "advanced mode" toggle exposes a Bot ID / Secret form alongside the QR CTA.
- **Multi-account**: the account-id input is shown for WeCom (defaults to `default`), so users can connect multiple WeCom bots side-by-side. Backend round-trips `request.account` through the session into the FastClaw payload.
- **Auto-refresh on success**: `WecomSetupModal` fires `onSuccess` immediately on phase=success so the channel list updates without waiting for the user to dismiss the success card.

## Cross-repo dependency

Depends on **fastclaw v0.0.108** (PR https://github.com/SerendipityOneInc/fastclaw/pull/85), already deployed to staging. That PR adds `BotID` / `Secret` to FastClaw's `AddChannelRequest` struct so the credentials don't get silently dropped by Go's JSON binder.

## Notable implementation details

- **Source param `source=wecom-cli`** — matches the upstream CLI; WeCom server may gate on this string. A status_code is logged on every QR-generate failure so a sustained shift would be detectable.
- **Poll error handling** — transient `httpx.TimeoutException` / `NetworkError` / `429 rate-limited` keep the session alive (return `pending`); only hard 4xx/5xx and other exceptions terminate setup.
- **5s polling cadence** — matches WeChat / Feishu modals (upstream CLI uses 3s; we don't want WeCom to throttle us harder than the others).
- **No pod-side credential file** — unlike WeChat which writes `~/.openclaw/openclaw-weixin/accounts/{id}.json`, WeCom's plugin reads everything from `openclaw.json` directly, so credentials go in the channel-config blob via `add_channel` only.

## Test plan

- [x] Backend: 20 unit tests in `tests/unit/test_openclaw_settings_wecom.py` (setup/poll/cancel happy paths + transient/429/503 error branches + multi-account round-trip + pairing-policy `allowFrom` invariant)
- [x] Frontend: 64 unit tests across `WecomSetupModal.unit.spec.tsx` and `ChannelsSection.unit.spec.tsx` (QR phase machine, multi-account propagation, advanced/manual mode toggle, auto-refresh on success)
- [x] End-to-end on staging openclaw cluster — QR scan → bot pod's `~/.openclaw/openclaw.json` shows `channels.wecom.accounts.<account>.{botId, secret, dmPolicy, groupPolicy, allowFrom}` correctly persisted
- [x] Channel removal — generic `client.remove_channel()` path cleans up the entire `channels.wecom` node

## Note on pre-existing test failures

The full `pytest --cov=app` suite shows 8 failures + 5 errors in unrelated files (`test_invite_codes.py`, `test_mattermost_provisioner.py`, `test_openclaw_agents.py`, `test_redis_client.py`, `test_storage.py`, etc.) — all triggered by `PytestUnraisableExceptionWarning` cascades. Verified these reproduce on `origin/main` without any of this PR's changes; tracked by PR #1567 (`promote stdlib ignore::ResourceWarning`). Not blocking ECA-625.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## d7d7f880 - feat(web): 订阅价格 + paywall 全量补 "Billed annually, $X/year" + dev FAB 可拖拽 (#1570)

- **SHA**: d7d7f880cdde33c6b1fdd5718cadf6978a4e9968
- **作者**: lynn Zhuang
- **日期**: 2026-05-07T06:19:11Z
- **PR**: #1570 https://github.com/SerendipityOneInc/ecap-workspace/pull/1570

### Commit Message

```
feat(web): 订阅价格 + paywall 全量补 "Billed annually, $X/year" + dev FAB 可拖拽 (#1570)

## Summary

  订阅展示全链路补齐 **Billed annually, $X/year**
  年总价行,让用户一眼看到年付实际扣多少钱,而不是只显示折算后的月单价。

  ### 三个价格展示入口都加了年付明细行(yearly cycle 下)

  | 入口 | 文件 | 套餐 | 显示 |
  |---|---|---|---|
| 订阅升级 modal | `src/components/billing/PlanCard.tsx` | Starter / Pro /
Ultra | $200
  / $1,000 / $2,000 |
| 官网 Pricing 页面 | `src/app/[locale]/pricing/PublicPricingClient.tsx` |
Starter / Pro
   / Ultra | 同上,**接 i18n 10 个 locale** |
| Starter 试用 paywall | `src/components/PaywallContent.tsx` | Starter |
$200(月单价 +
  年总价合并到同一行,中间用 · 分隔) |

  ### 实现要点

  - **价格单一 source of truth**:三处都从 `src/lib/stripe/stripe.ts` 的
`PLAN_PRICING`(cents)读出,UI 层 `/100` + `toLocaleString('en-US')` 拿千分位逗号 —
Pro
  `$1,000`、Ultra `$2,000` 都带逗号。将来改套餐价只需要改 `stripe.ts`,三处 UI 自动同步。
  - **i18n 覆盖**:新增 `publicPricing.billedAnnually` key 覆盖 10 个
  locale(en/zh/ja/ko/de/es/fr/it/pt/ar),用 `{total}`
  占位符接已格式化好的字符串,翻译只控制句式不重做数字格式化。
  - **PlanCard 同步去掉 ", billed yearly"
  后缀**:新行已经表达同样含义而且更明确,旧后缀变冗余。
- **PaywallContent 单行布局**:`then $17 /mo · Billed annually, $200/year`,外层
flex 加
  `flex-wrap`,窄视口(手机)下年总价段会自动换行不溢出。
- **没做 "first year then renews higher" 双价格格式**:ZooClaw 的 `PLAN_PRICING`
  是平价年付,没有首年促销+续费涨价的结构。如果将来引入,只需要在年总价行扩展条件即可。

  ### 测试

- `tests/unit/components/billing/PlanCard.unit.spec.tsx` — 14 个用例全过,补
Pro
  千分位逗号、yearly/monthly 切换等 4 条新断言
- `tests/unit/components/PaywallContent.unit.spec.tsx` — 14 个用例全过,旧的
`"billed
  yearly"` 文本断言改成 regex 匹配年总价

  ## Test plan

- [ ] **订阅 modal**:Annual cycle 下三张卡片都显示 `Billed annually,
$X/year`,Pro/Ultra
  带千分位逗号;切回 Monthly 该行消失
- [ ] **官网 `/pricing`**:英文站显示 `Billed annually, $X/year`;切到
`/zh/pricing` 显示
  `按年计费，$X/年`;日/韩/德/法/西/意/葡/阿语 locale 都要显示对应翻译
- [ ] **Paywall modal**(asleep 或 trial-exhausted 状态触发):Annual cycle 显示
`then $17
/mo · Billed annually, $200/year` 单行;切到 Monthly 显示 `then $24 /mo`(无年总价段)
  - [ ] **响应式**:手机视口下 paywall 单行如果放不下,年总价段优雅换行不溢出 modal 边界
<img width="1226" height="1126" alt="20260507-115255"
src="https://github.com/user-attachments/assets/47684243-c8d7-406c-b2c8-46f69fcdf4f5"
/>
<img width="2422" height="1692" alt="screenshot-20260507-105951"
src="https://github.com/user-attachments/assets/d79b3b06-da60-46eb-a15a-1536931ea26b"
/>

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@LynndeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
Co-authored-by: peter-srp <peter@srp.one>
```

### PR Description

## Summary

  订阅展示全链路补齐 **Billed annually, $X/year**
  年总价行,让用户一眼看到年付实际扣多少钱,而不是只显示折算后的月单价。

  ### 三个价格展示入口都加了年付明细行(yearly cycle 下)

  | 入口 | 文件 | 套餐 | 显示 |
  |---|---|---|---|
  | 订阅升级 modal | `src/components/billing/PlanCard.tsx` | Starter / Pro / Ultra | $200
  / $1,000 / $2,000 |
  | 官网 Pricing 页面 | `src/app/[locale]/pricing/PublicPricingClient.tsx` | Starter / Pro
   / Ultra | 同上,**接 i18n 10 个 locale** |
  | Starter 试用 paywall | `src/components/PaywallContent.tsx` | Starter | $200(月单价 +
  年总价合并到同一行,中间用 · 分隔) |

  ### 实现要点

  - **价格单一 source of truth**:三处都从 `src/lib/stripe/stripe.ts` 的
  `PLAN_PRICING`(cents)读出,UI 层 `/100` + `toLocaleString('en-US')` 拿千分位逗号 — Pro
  `$1,000`、Ultra `$2,000` 都带逗号。将来改套餐价只需要改 `stripe.ts`,三处 UI 自动同步。
  - **i18n 覆盖**:新增 `publicPricing.billedAnnually` key 覆盖 10 个
  locale(en/zh/ja/ko/de/es/fr/it/pt/ar),用 `{total}`
  占位符接已格式化好的字符串,翻译只控制句式不重做数字格式化。
  - **PlanCard 同步去掉 ", billed yearly"
  后缀**:新行已经表达同样含义而且更明确,旧后缀变冗余。
  - **PaywallContent 单行布局**:`then $17 /mo · Billed annually, $200/year`,外层 flex 加
  `flex-wrap`,窄视口(手机)下年总价段会自动换行不溢出。
  - **没做 "first year then renews higher" 双价格格式**:ZooClaw 的 `PLAN_PRICING`
  是平价年付,没有首年促销+续费涨价的结构。如果将来引入,只需要在年总价行扩展条件即可。

  ### 测试

  - `tests/unit/components/billing/PlanCard.unit.spec.tsx` — 14 个用例全过,补 Pro
  千分位逗号、yearly/monthly 切换等 4 条新断言
  - `tests/unit/components/PaywallContent.unit.spec.tsx` — 14 个用例全过,旧的 `"billed
  yearly"` 文本断言改成 regex 匹配年总价

  ## Test plan

  - [ ] **订阅 modal**:Annual cycle 下三张卡片都显示 `Billed annually, $X/year`,Pro/Ultra
  带千分位逗号;切回 Monthly 该行消失
  - [ ] **官网 `/pricing`**:英文站显示 `Billed annually, $X/year`;切到 `/zh/pricing` 显示
  `按年计费，$X/年`;日/韩/德/法/西/意/葡/阿语 locale 都要显示对应翻译
  - [ ] **Paywall modal**(asleep 或 trial-exhausted 状态触发):Annual cycle 显示 `then $17
  /mo · Billed annually, $200/year` 单行;切到 Monthly 显示 `then $24 /mo`(无年总价段)
  - [ ] **响应式**:手机视口下 paywall 单行如果放不下,年总价段优雅换行不溢出 modal 边界
<img width="1226" height="1126" alt="20260507-115255" src="https://github.com/user-attachments/assets/47684243-c8d7-406c-b2c8-46f69fcdf4f5" />
<img width="2422" height="1692" alt="screenshot-20260507-105951" src="https://github.com/user-attachments/assets/d79b3b06-da60-46eb-a15a-1536931ea26b" />


---

## 1671d5d2 - fix(web): defensive matchMedia wrapper to prevent UC Browser crash (#1569)

- **SHA**: 1671d5d2127961e1e95d21b93e1908c5fefaaee7
- **作者**: peter-srp
- **日期**: 2026-05-07T03:54:39Z
- **PR**: #1569 https://github.com/SerendipityOneInc/ecap-workspace/pull/1569

### Commit Message

```
fix(web): defensive matchMedia wrapper to prevent UC Browser crash (#1569)

## Summary
- UC Browser 17.x patches `window.matchMedia` with internal telemetry
that calls `JSON.stringify` on objects containing DOM element
references. On React-hydrated pages, this hits circular `__reactFiber`
refs and throws `TypeError: Converting circular structure to JSON`,
crashing the landing page via the route-error boundary.
- Adds an inline `<script>` in `<head>` that wraps `matchMedia` with
try-catch, returning a spec-compliant `MediaQueryList` stub on failure
(defaults to light mode — acceptable degradation)
- Filters `"circular structure" + "reactFiber"` errors in Sentry
`beforeSend` as secondary noise reduction

**Sentry issue:**
https://serendipity-one-inc.sentry.io/issues/7462625509/

## Test plan
- [x] Verify landing page renders correctly in standard browsers
(Chrome, Safari, Firefox)
- [ ] Verify the inline script doesn't break `next-themes` dark mode
detection
- [ ] Confirm Sentry `beforeSend` filter drops matching events but
passes unrelated `TypeError`s

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary
- UC Browser 17.x patches `window.matchMedia` with internal telemetry that calls `JSON.stringify` on objects containing DOM element references. On React-hydrated pages, this hits circular `__reactFiber` refs and throws `TypeError: Converting circular structure to JSON`, crashing the landing page via the route-error boundary.
- Adds an inline `<script>` in `<head>` that wraps `matchMedia` with try-catch, returning a spec-compliant `MediaQueryList` stub on failure (defaults to light mode — acceptable degradation)
- Filters `"circular structure" + "reactFiber"` errors in Sentry `beforeSend` as secondary noise reduction

**Sentry issue:** https://serendipity-one-inc.sentry.io/issues/7462625509/

## Test plan
- [x] Verify landing page renders correctly in standard browsers (Chrome, Safari, Firefox)
- [ ] Verify the inline script doesn't break `next-themes` dark mode detection
- [ ] Confirm Sentry `beforeSend` filter drops matching events but passes unrelated `TypeError`s

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 3a939fd9 - fix(web): enable image preview for images inside tables (#1501)

- **SHA**: 3a939fd9e9b0d0c2322cade2703be406597d08e0
- **作者**: peter-srp
- **日期**: 2026-05-07T03:52:31Z
- **PR**: #1501 https://github.com/SerendipityOneInc/ecap-workspace/pull/1501

### Commit Message

```
fix(web): enable image preview for images inside tables (#1501)

## Summary
- LLM 返回的 HTML 表格中的 `<img>` 标签（非 markdown 语法渲染）之前点击无法放大预览，因为 click
handler 仅识别 `markdown-image` class
- 扩展 click handler fallback：`.prose` 内任意 `<img>` 点击均可触发预览，优先用
`data-image-url`，fallback 到 `src`
- Gallery 选择器同步扩展，表格内图片也参与多图导航
- 表格内图片 CSS：`height: auto; max-height: 200px; cursor: pointer`（300px
对表格太高）

## Test plan
- [x] 新增单元测试：markdown 图片在 markdown 表格中可点击预览
- [x] 新增单元测试：raw HTML `<img>` 在表格中可点击预览
- [x] 原有 32 个测试全部通过
- [ ] 手动验证：聊天页面中 LLM 返回的表格图片可点击放大

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary
- LLM 返回的 HTML 表格中的 `<img>` 标签（非 markdown 语法渲染）之前点击无法放大预览，因为 click handler 仅识别 `markdown-image` class
- 扩展 click handler fallback：`.prose` 内任意 `<img>` 点击均可触发预览，优先用 `data-image-url`，fallback 到 `src`
- Gallery 选择器同步扩展，表格内图片也参与多图导航
- 表格内图片 CSS：`height: auto; max-height: 200px; cursor: pointer`（300px 对表格太高）

## Test plan
- [x] 新增单元测试：markdown 图片在 markdown 表格中可点击预览
- [x] 新增单元测试：raw HTML `<img>` 在表格中可点击预览
- [x] 原有 32 个测试全部通过
- [ ] 手动验证：聊天页面中 LLM 返回的表格图片可点击放大

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 16f43bfc - feat(web): landing page uses locale-free URL (#1568)

- **SHA**: 16f43bfceb7b6e82bee14df741237b96e68f23c9
- **作者**: peter-srp
- **日期**: 2026-05-07T03:19:30Z
- **PR**: #1568 https://github.com/SerendipityOneInc/ecap-workspace/pull/1568

### Commit Message

```
feat(web): landing page uses locale-free URL (#1568)

## Summary
- Add `/` to `APP_PATHS` so the homepage follows the same locale-free
routing as `/chat`, `/admin` etc.
- `/` → middleware rewrites to `/{locale}` internally (browser URL stays
`/`)
  - `/en`, `/zh` etc. → 301 redirect to `/`
- Fix hardcoded `/${locale}/chat` links in `LandingClient` (3 places)
and `/${locale}` in `OnboardingModal`
- Update root canonical URL from `/en` to `/`
- Normalize middleware rewrite to avoid trailing slash (`/en/` → `/en`)
for root path

## SEO Note
hreflang alternates in `_seo.ts` still generate `/{locale}` URLs — they
301 to `/` which Google consolidates. Non-English organic search landing
may degrade slightly since all locale versions resolve to the same URL.
If this becomes an issue, we can add bot-specific handling in middleware
later.

## Test plan
- [x] `isAppPath('/')` returns true, `isAppPath('/en')` returns true
- [x] `isAppPath('/en/pricing')` still returns false (SEO pages
unaffected)
- [x] `LocaleLink href="/"` renders as `/` (no locale prefix)
- [x] All 281 test files pass (4453 tests)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary
- Add `/` to `APP_PATHS` so the homepage follows the same locale-free routing as `/chat`, `/admin` etc.
  - `/` → middleware rewrites to `/{locale}` internally (browser URL stays `/`)
  - `/en`, `/zh` etc. → 301 redirect to `/`
- Fix hardcoded `/${locale}/chat` links in `LandingClient` (3 places) and `/${locale}` in `OnboardingModal`
- Update root canonical URL from `/en` to `/`
- Normalize middleware rewrite to avoid trailing slash (`/en/` → `/en`) for root path

## SEO Note
hreflang alternates in `_seo.ts` still generate `/{locale}` URLs — they 301 to `/` which Google consolidates. Non-English organic search landing may degrade slightly since all locale versions resolve to the same URL. If this becomes an issue, we can add bot-specific handling in middleware later.

## Test plan
- [x] `isAppPath('/')` returns true, `isAppPath('/en')` returns true
- [x] `isAppPath('/en/pricing')` still returns false (SEO pages unaffected)
- [x] `LocaleLink href="/"` renders as `/` (no locale prefix)
- [x] All 281 test files pass (4453 tests)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 617aa564 - feat(asr): add default prompt to bias upstream recognition (#1559)

- **SHA**: 617aa5640647985fe1ccf11df929c0f85d40358d
- **作者**: lark-srp
- **日期**: 2026-05-07T03:02:03Z
- **PR**: #1559 https://github.com/SerendipityOneInc/ecap-workspace/pull/1559

### Commit Message

```
feat(asr): add default prompt to bias upstream recognition (#1559)

## Summary
- Forward a configurable default prompt (\`ZooClaw, OpenClaw, Claude\`)
to upstream Qwen3-ASR on **both** transports:
- HTTP \`POST /v1/audio/transcriptions\` — multipart \`prompt\` form
field
  - Realtime WebSocket — \`session.update\` payload
- Biases recognition toward product-specific proper nouns prone to
homophone misrecognition.
- Override via env var \`ASR_DEFAULT_PROMPT\`.
- Drive-by: bump default \`ASR_BASE_URL\` domain from \`g.yesy.dev\` →
\`g.yesy.online\` (separate commit).

## Files
- \`app/settings.py\` — new \`ASR_DEFAULT_PROMPT\` setting
- \`app/services/asr/upstream_client.py\` — include prompt in
\`session.update\`
- \`app/services/asr/service.py\` — include prompt in HTTP multipart
- \`tests/unit/test_asr_upstream_client.py\` — assert prompt in WS
handshake
- \`tests/unit/test_asr_service.py\` — assert prompt in HTTP multipart

## Test plan
- [x] \`pytest tests/unit/test_asr_upstream_client.py
tests/unit/test_asr_service.py tests/unit/test_settings.py\` — 74 passed
locally
- [ ] CI \`python-code-quality / build-and-test\` green
- [ ] Manual smoke: realtime ASR session resolves \`ZooClaw\` /
\`OpenClaw\` / \`Claude\` correctly on near-homophone audio

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary
- Forward a configurable default prompt (\`ZooClaw, OpenClaw, Claude\`) to upstream Qwen3-ASR on **both** transports:
  - HTTP \`POST /v1/audio/transcriptions\` — multipart \`prompt\` form field
  - Realtime WebSocket — \`session.update\` payload
- Biases recognition toward product-specific proper nouns prone to homophone misrecognition.
- Override via env var \`ASR_DEFAULT_PROMPT\`.
- Drive-by: bump default \`ASR_BASE_URL\` domain from \`g.yesy.dev\` → \`g.yesy.online\` (separate commit).

## Files
- \`app/settings.py\` — new \`ASR_DEFAULT_PROMPT\` setting
- \`app/services/asr/upstream_client.py\` — include prompt in \`session.update\`
- \`app/services/asr/service.py\` — include prompt in HTTP multipart
- \`tests/unit/test_asr_upstream_client.py\` — assert prompt in WS handshake
- \`tests/unit/test_asr_service.py\` — assert prompt in HTTP multipart

## Test plan
- [x] \`pytest tests/unit/test_asr_upstream_client.py tests/unit/test_asr_service.py tests/unit/test_settings.py\` — 74 passed locally
- [ ] CI \`python-code-quality / build-and-test\` green
- [ ] Manual smoke: realtime ASR session resolves \`ZooClaw\` / \`OpenClaw\` / \`Claude\` correctly on near-homophone audio

---

## 2dc87a25 - feat(web): onboarding & launch loading dark-mode 适配 (#1566)

- **SHA**: 2dc87a259c9735c01eddedd600a9b1149138541e
- **作者**: lynn Zhuang
- **日期**: 2026-05-07T02:57:23Z
- **PR**: #1566 https://github.com/SerendipityOneInc/ecap-workspace/pull/1566

### Commit Message

```
feat(web): onboarding & launch loading dark-mode 适配 (#1566)

## Summary
- 新建 `web/src/components/onboarding/onboarding.css` ——
`.onboarding-root` + `.dark
.onboarding-root` 双向 token(bg / text / cta / border / error / toast /
card / arrow),把
   onboarding 整个 branded module 接到全局 `.dark` class 上但仍走独立色板,避免污染 `:root`
- LOGO 切换 `<img>` + `--onboarding-logo-filter: invert()` 跟随主题反色(R2
cross-origin
让 `mask-image` 不可用,filter 是更稳的替代)
- 7 个 step 组件 + Layout / Modal / SpriteDialogue / SpriteGuide /
WelcomeRewardToast
把所有 `rgba(26,26,24,*)` / `#fafafa` 等硬编码替换成
  `var(--onboarding-*)`,LoadingStep("Entering...")也一并适配
- `CompanionSelectStep`:cardBreathe keyframes 从 JS 注入挪进 CSS(box-shadow
能解析
token);3 个 slot 的 `AnimatePresence` 拆掉,改用 `LayoutGroup` + `layoutId` +
`layout`
  的纯 FLIP morph,消除点击侧卡时的 fade-flicker;hover 统一为 scale-only,消除侧卡 wash-out
闪烁
- `AGENTS.md` 加 "UI Components — shadcn-first" 章节,标注 onboarding 等
branded module
为例外
  
## Test plan
- [ ] light + dark 两种主题下走完整 onboarding flow(invite code → name →
companion
select → reminder → channel → loading)所有文字 / 边框 / 按钮可读
  - [ ] companion 切换:点击侧卡/箭头/拖拽,3 张卡之间过渡平滑,无 fade flicker
- [ ] hover 侧卡只有 scale,不再有背景色 wash-out
  - [ ] LOGO 在 light 下显示深色、dark 下显示浅色

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@LynndeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
Co-authored-by: peter-srp <peter@srp.one>
```

### PR Description

 ## Summary                                                                            
  - 新建 `web/src/components/onboarding/onboarding.css` —— `.onboarding-root` + `.dark
  .onboarding-root` 双向 token(bg / text / cta / border / error / toast / card / arrow),把
   onboarding 整个 branded module 接到全局 `.dark` class 上但仍走独立色板,避免污染 `:root`
  - LOGO 切换 `<img>` + `--onboarding-logo-filter: invert()` 跟随主题反色(R2 cross-origin 
  让 `mask-image` 不可用,filter 是更稳的替代)                                             
  - 7 个 step 组件 + Layout / Modal / SpriteDialogue / SpriteGuide / WelcomeRewardToast 
  把所有 `rgba(26,26,24,*)` / `#fafafa` 等硬编码替换成                                    
  `var(--onboarding-*)`,LoadingStep("Entering...")也一并适配
  - `CompanionSelectStep`:cardBreathe keyframes 从 JS 注入挪进 CSS(box-shadow 能解析      
  token);3 个 slot 的 `AnimatePresence` 拆掉,改用 `LayoutGroup` + `layoutId` + `layout`   
  的纯 FLIP morph,消除点击侧卡时的 fade-flicker;hover 统一为 scale-only,消除侧卡 wash-out
  闪烁                                                                                    
  - `AGENTS.md` 加 "UI Components — shadcn-first" 章节,标注 onboarding 等 branded module
  为例外                                                                                  
  
  ## Test plan                                                                            
  - [ ] light + dark 两种主题下走完整 onboarding flow(invite code → name → companion
  select → reminder → channel → loading)所有文字 / 边框 / 按钮可读                        
  - [ ] companion 切换:点击侧卡/箭头/拖拽,3 张卡之间过渡平滑,无 fade flicker
  - [ ] hover 侧卡只有 scale,不再有背景色 wash-out                                        
  - [ ] LOGO 在 light 下显示深色、dark 下显示浅色                

---

