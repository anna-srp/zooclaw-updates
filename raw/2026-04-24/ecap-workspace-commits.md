# ecap-workspace commits — 2026-04-24 (UTC 2026-04-23)

共 37 条 commits

---

## 1. 73c231f3 — feat(web): add back button to session history page (#1261)

- **SHA**: 73c231f30d62baa3420dcc1a5e1655bfab1f366f
- **作者**: tim-srp
- **日期**: 2026-04-23T15:08:40Z
- **PR**: #1261

### 完整 commit message

feat(web): add back button to session history page (#1261)

## Summary
- Add a BackButton component to the session history page header
- Navigates back to `/claw-settings` when clicked
- Applied consistently across all page states (loading, empty, normal)

## Test plan
- [ ] Open session history page, verify back arrow appears in header
- [ ] Click back button, confirm navigation to claw-settings
- [ ] Verify button appears in loading/empty/populated states

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### PR Body（#1261）

## Summary
- Add a BackButton component to the session history page header
- Navigates back to `/claw-settings` when clicked
- Applied consistently across all page states (loading, empty, normal)

## Test plan
- [ ] Open session history page, verify back arrow appears in header
- [ ] Click back button, confirm navigation to claw-settings
- [ ] Verify button appears in loading/empty/populated states

---

## 2. 2c1a22b8 — feat: subscription code — redeem codes that grant real subscriptions (#1270)

- **SHA**: 2c1a22b86c530db02870b7bfec10652c62a1c524
- **作者**: tim-srp
- **日期**: 2026-04-23T14:53:11Z
- **PR**: #1270

### 完整 commit message

feat: subscription code — redeem codes that grant real subscriptions (#1270)

## Summary
- Add subscription codes — gift codes that grant real subscriptions
(Starter/Pro/Ultra) instead of credits
- Admin manages via independent "Subscription Code" tab with plan tier,
duration days, max activations
- Users redeem via the same input — backend auto-detects code category
and dispatches accordingly
- Rejects redeem if current plan is higher than code (no downgrade);
same-tier appends duration

## Changes

### Backend
- New `subscription_code` service with plan validation, time window
calculation, rollback on failure
- Unified `POST /api/gift-code/redeem` dispatches by `category` field
(credits vs subscription)
- New admin `POST/GET /admin/subscription-codes` endpoints
- New `ecap-subscription-code-activations` collection (independent
frequency tracking)
- Extends `ecap-gift-codes` with `category`, `plan_tier`,
`duration_days` fields
- 13 unit tests covering expiry, exhaustion, plan downgrade, CAS
conflict, rollback

### Frontend
- New `SubscriptionCodesTab` admin component with plan tier badges
- `useSubscriptionCodes` hook (React Query CRUD)
- Modified `UserMenu` redeem handler — shows subscription-specific toast
- i18n keys added to 7 locales (en, zh, ja, ko, es, pt, ar)

## Design Spec
See `docs/superpowers/specs/2026-04-23-subscription-code-design.md`
(#1263)

## Test plan
- [ ] Backend: `pytest tests/unit/test_subscription_code.py
tests/unit/test_subscription_code_repo.py -v` — 13 tests pass
- [ ] Frontend: `tsc --noEmit` — zero errors
- [ ] Lint: `ruff check` + `lint-imports` + `eslint` — all clean
- [ ] Manual: create subscription code in admin, redeem as user, verify
subscription activates
- [ ] Manual: try redeeming with higher plan — verify rejection

### PR Body（#1270）

## Summary
- Add subscription codes — gift codes that grant real subscriptions (Starter/Pro/Ultra) instead of credits
- Admin manages via independent "Subscription Code" tab with plan tier, duration days, max activations
- Users redeem via the same input — backend auto-detects code category and dispatches accordingly
- Rejects redeem if current plan is higher than code (no downgrade); same-tier appends duration

## Changes

### Backend
- New `subscription_code` service with plan validation, time window calculation, rollback on failure
- Unified `POST /api/gift-code/redeem` dispatches by `category` field (credits vs subscription)
- New admin `POST/GET /admin/subscription-codes` endpoints
- New `ecap-subscription-code-activations` collection (independent frequency tracking)
- Extends `ecap-gift-codes` with `category`, `plan_tier`, `duration_days` fields
- 13 unit tests covering expiry, exhaustion, plan downgrade, CAS conflict, rollback

### Frontend
- New `SubscriptionCodesTab` admin component with plan tier badges
- `useSubscriptionCodes` hook (React Query CRUD)
- Modified `UserMenu` redeem handler — shows subscription-specific toast
- i18n keys added to 7 locales (en, zh, ja, ko, es, pt, ar)

---

## 3. 8624433f — fix(web): use soft navigation on landing to fix login tracking (#1284)

- **SHA**: 8624433fb7ed308a2713d05b605e8353d79a361c
- **作者**: Fangmiao-srp
- **日期**: 2026-04-23T14:30:36Z
- **PR**: #1284

### 完整 commit message

fix(web): use soft navigation on landing to fix login tracking (#1284)

## Summary
- Landing page used `window.location.href` (hard navigation) to redirect
to `/chat` after login, which killed the `_completeLogin` async chain
before `trackLogin`/`trackSignUp` could fire
- Replace with `router.push` (soft navigation) so the page doesn't
unload and tracking events are sent
- All other login entry points (Pricing, UserGuide, AgentChat, Canvas)
already use soft navigation — Landing was the only outlier

## Test plan
- [ ] Login via Google on landing page → verify `login` event appears in
GA4 DebugView
- [ ] Sign up as new user on landing page → verify `sign_up` event
appears in GA4 DebugView
- [ ] Verify landing → chat redirect still works correctly after login
- [ ] Verify login from Pricing and UserGuide pages still works

### PR Body（#1284）

## Summary
- Landing page used `window.location.href` (hard navigation) to redirect to `/chat` after login, which killed the `_completeLogin` async chain before `trackLogin`/`trackSignUp` could fire
- Replace with `router.push` (soft navigation) so the page doesn't unload and tracking events are sent
- All other login entry points (Pricing, UserGuide, AgentChat, Canvas) already use soft navigation — Landing was the only outlier

---

## 4. e5ca7f34 — feat(ios): Codex-generated App Store release notes + auto-submit for review (#1279)

- **SHA**: e5ca7f342ac39394c9743fa890918ffc5a24a6fa
- **作者**: bill-srp
- **日期**: 2026-04-23T13:38:54Z
- **PR**: #1279

### 完整 commit message

feat(ios): Codex-generated App Store release notes + auto-submit for review (#1279)

## Summary

- Replace `changelog_from_git_commits` in the Fastfile `appstore` lane
with Codex-generated release notes
- New workflow steps collect PR titles and descriptions (ios/ path only)
since the previous release tag, then feed them to
`openai/codex-action@v1` to produce user-facing numbered release notes
- Enable `submit_for_review: true` so builds enter Apple review
automatically on release tag
- Set `skip_metadata: false` so the generated changelog is actually
uploaded to App Store Connect

---

## 5. fa1f7834 — docs: subscription code feature design spec (#1263)

- **SHA**: fa1f7834bff9adc47192c0b5e2ca2035f9d70dbd
- **作者**: tim-srp
- **日期**: 2026-04-23T13:48:46Z

### 完整 commit message

docs: subscription code feature design spec (#1263)

Design specification for the subscription code feature.

---

## 6. 69889acb — feat: resource management — workspace file browser + upload assets tracking (#1117)

- **SHA**: 69889acba938bc444e37eac10f8a239cfd3ef492
- **作者**: tim-srp
- **日期**: 2026-04-23T12:53:15Z
- **PR**: #1134

### 完整 commit message

feat: resource management — workspace file browser + upload assets tracking (#1134)

## Summary

- Add **Resources Panel** sidebar to chat page for browsing workspace
files and user uploads
- Redesign **attachment button** with popover for referencing existing
files or uploading new ones
- Store user upload metadata in MongoDB for retrieval and reuse across
conversations
- Proxy FastClaw's new `GET /files/list` endpoint for real-time
workspace directory browsing

## Architecture

```
Frontend (ResourcesPanel)
  → claw-interface (GET /conversation/workspace/files)
    → FastClaw (GET /bots/{id}/files/list)

Frontend (MyUploadsTab / UploadPopover)
  → claw-interface (GET/POST /conversation/assets)
    → MongoDB (ecap-conversation-assets)
```

---

## 7. 60143569 — fix(web): match community skills against bundled and extra runtime skills (#1281)

- **SHA**: 6014356998875624f4d40a8e5b0fb05896ff8615
- **作者**: tim-srp
- **日期**: 2026-04-23T12:49:37Z
- **PR**: #1281

### 完整 commit message

fix(web): match community skills against bundled and extra runtime skills (#1281)

Fix skill-store matching so community skills correctly detect both kinds
of runtime-provided builtin skills: `openclaw-bundled` and `openclaw-extra`.

---

## 8. 18a43e02 — ci(deploy): auto-deploy staging on every main merge (#1280)

- **SHA**: 18a43e028cd2545feb43e807c62fff28b5d3360e
- **作者**: tim-srp
- **日期**: 2026-04-23T12:52:13Z
- **PR**: #1280

### 完整 commit message

ci(deploy): auto-deploy staging on every main merge (#1280)

## Summary
- Staging now auto-deploys on every merge to `main` (frontend + backend in parallel).
- Retires the `staging` branch flow.
- Added `concurrency` group with dynamic `cancel-in-progress`.

---

## 9. 09e8a573 — chore(web): remove unused exports from src/lib + whitelist scaffold APIs (#1249)

- **SHA**: 09e8a573f21c868e1ae2c48e07f616cd19589098
- **作者**: tim-srp
- **日期**: 2026-04-23T12:46:24Z

### 完整 commit message

chore(web): remove unused exports from src/lib + whitelist scaffold APIs (#1249)

Dead code removal and API whitelisting.

---

## 10. e74b1c17 — fix(web): refresh preview iframe when artifact file identity changes (#1252)

- **SHA**: e74b1c17a7d4d582ad2d730601d73ce29489522e
- **作者**: tim-srp
- **日期**: 2026-04-23T11:47:12Z
- **PR**: #1252

### 完整 commit message

fix(web): refresh preview iframe when artifact file identity changes (#1252)

When the model regenerates a same-name artifact, ArtifactPreview's iframe
stayed frozen on the cached old HTML. Fix: refresh cacheBuster when file
identity changes.

---

## 11. ff21cdb6 — feat(openclaw): install custom agents from catalog records (#1231)

- **SHA**: ff21cdb61d748adf6713a3184f24478a75899a26
- **作者**: tim-srp
- **日期**: 2026-04-23T08:33:13Z
- **PR**: #1231

### 完整 commit message

feat(openclaw): install custom agents from catalog records (#1231)

## Summary
- unify archive runtime deployment for pack and custom agent installs
- resolve private custom agent installs from catalog metadata and version hashes
- simplify publish page installs to use saved records and updated confirmations

---

## 12. 8786085c — feat: auto-enable connector on connect + remove Claw Tools toggle (#1232)

- **SHA**: 8786085cbaaf524d433700788437bf82928b194a
- **作者**: tim-srp
- **日期**: 2026-04-23T08:57:05Z
- **PR**: #1232

### 完整 commit message

feat: auto-enable connector on connect + remove Claw Tools toggle (#1232)

## Summary
- Auto-enable and inject skill when OAuth completes (polling + webhook)
- Remove Claw Tools toggle — connected cards now match Google Workspace style

---

## 13. 1fd86794 — feat(openclaw): simplify publish page custom agent install flow (#1260)

- **SHA**: 1fd867941824a01e8546f741bd44c132689cc92a
- **作者**: tim-srp
- **日期**: 2026-04-23T09:36:42Z
- **PR**: #1260

### 完整 commit message

feat(openclaw): simplify publish page custom agent install flow (#1260)

## Summary
- simplify the custom agent install and uninstall flow on the publish page
- generate stable, readable custom agent ids from the visible agent name or package basename
- support reinstalling saved custom agents when the persisted record already contains the archive metadata

---

## 14. 1959b946 — refactor(web): extract OpenClawProvider — fix 3 W3 violations (#1236)

- **SHA**: 1959b9462d6153e746dd68edab1a10ecf2274799
- **作者**: tim-srp
- **日期**: 2026-04-23T09:33:44Z

### 完整 commit message

refactor(web): extract OpenClawProvider — fix 3 W3 violations (A1-PR11) (#1236)

Refactoring to fix W3 architecture violations.

---

## 15. 1bef0468 — fix(web): preserve textarea input on FeedbackDialog submit failure (#1268)

- **SHA**: 1bef0468993a1181f43260789f8bcde2c763f1f0
- **作者**: tim-srp
- **日期**: 2026-04-23T09:28:40Z
- **PR**: #1268

### 完整 commit message

fix(web): preserve textarea input on FeedbackDialog submit failure (#1177) (#1268)

Preserve user input if feedback submission fails.

---

## 16. 3a4a95d5 — fix(web): async hygiene — interval cleanup + unhandled rejection + race guard (#1255)

- **SHA**: 3a4a95d51d45713a0bafea3c0c99a59b08566ba6
- **作者**: tim-srp
- **日期**: 2026-04-23T09:19:32Z

### 完整 commit message

fix(web): async hygiene — interval cleanup + unhandled rejection + race guard (#1255)

Async cleanup fixes.

---

## 17. bfae614b — feat(ios): iOS 1.4.0 — header redesign, copy tooltip, voice input fixes (#1277)

- **SHA**: bfae614b80681baf6666ea2c69902d0f179b7495
- **作者**: bill-srp
- **日期**: 2026-04-23T08:22:01Z

### 完整 commit message

feat(ios): iOS 1.4.0 — header redesign, copy tooltip, voice input fixes, CI improvements (#1277)

iOS 1.4.0 release with UI improvements and voice input fixes.

---

## 18. 4aad097e — refactor(billing): clarify credit copy and surface add-on freeze note (#824)

- **SHA**: 4aad097ea635ad5fb58886e9a58d0cc89fa49e62
- **作者**: tim-srp
- **日期**: 2026-04-23T08:25:35Z

### 完整 commit message

refactor(billing): clarify credit copy and surface add-on freeze note (#824)

Billing copy improvements.

---

## 19. 5e4eba79 — docs(claude-md): codify log-sanitization + pnpm-override rules (#1240)

- **SHA**: 5e4eba7954e22bb69a03836bd3e4b45f69d1fb10
- **作者**: tim-srp
- **日期**: 2026-04-23T07:48:55Z

### 完整 commit message

docs(claude-md): codify log-sanitization + pnpm-override rules from security series (#1240)

Documentation for security practices.

---

## 20. afadbbb8 — fix(web): IntegrationsSection onConnect rejection clears connecting state (#1251)

- **SHA**: afadbbb8e63a9f9e1fe62563c569fccc6b8fd342
- **作者**: tim-srp
- **日期**: 2026-04-23T07:40:27Z

### 完整 commit message

fix(web): IntegrationsSection onConnect rejection clears connecting state (#1069) (#1251)

UI state fix for integration connections.

---

## 21. dbad204f — fix(security): close 4 remaining Dependabot alerts (#1235)

- **SHA**: dbad204fd751eecbe6833623d9286ad9a211be5a
- **作者**: tim-srp
- **日期**: 2026-04-23T07:28:48Z

### 完整 commit message

fix(security): close 4 remaining Dependabot alerts (uuid / fast-xml-parser / lodash / dompurify) (#1235)

Security patch: update dependencies to resolve Dependabot alerts.

---

## 22. 046de178 — fix(security): scrub uid in mattermost provisioning logs (#1241)

- **SHA**: 046de178ccc81512daaf6f011e3d557af5eec86b
- **作者**: tim-srp
- **日期**: 2026-04-23T07:09:21Z

### 完整 commit message

fix(security): scrub uid in mattermost provisioning logs (4 CodeQL alerts, final) (#1241)

Security: remove sensitive UID from logs.

---

## 23. fa74b74f — fix(web): payment UX — SuccessClient failed UI + SubscriptionPanel loading leak (#1262)

- **SHA**: fa74b74f8bc00f8e382801b28a90a6e83c80fb87
- **作者**: tim-srp
- **日期**: 2026-04-23T07:09:45Z

### 完整 commit message

fix(web): payment UX — SuccessClient failed UI + SubscriptionPanel loading leak (#1262)

Payment flow UX fixes.

---

## 24. 635d7c13 — fix(security): scrub bot_id in openclaw-family logs (#1242)

- **SHA**: 635d7c13e911003ac552ef111e241b47d0326d08
- **作者**: tim-srp
- **日期**: 2026-04-23T06:52:52Z

### 完整 commit message

fix(security): scrub bot_id in openclaw-family logs (clears 7 CodeQL alerts) (#1242)

Security: remove bot_id from logs to resolve CodeQL alerts.

---

## 25-37. 其他 commits

详见原始 JSON 文件。包含：
- f9f81df4 — fix(security): bump electron 35 → 39 in desktop (#1248)
- da5d87f8 — fix(security): pnpm.overrides for 10 transitive vuln packages (#1247)
- eec7823a — fix(security): bump next to ^15.5.15 (#1239)
- fa78fa47 — fix(web): batch tiny bugs — #935 #1113 #1164 #1199 (#1237)
- 70ad5125 — test(web): harden against AdminClient cross-file flake (#1274)
- b2fa98a5 — refactor(web): relocate single-consumer tabs (#1271)
- 7b7b9d2a — fix: 消除 claw-interface ERROR 日志噪音 (#1267)
- 4d05fdd7 — refactor(web): extract MattermostProvider (#1265)
- 640d5aac — fix(web): defer LoginForm Google saveLoginInfo (#1264)
- 192e21d9 — fix(ci): align pr-size-check reusable permissions (#1249)
- b73e5e67 — fix(ios): Update Gemfile.lock (#1259)
- 5a72a595 — fix(stripe): 修复 order_confirm / portal 问题 (#795)
- 7c573b21 — fix(stripe): 升级取消幂等化 (#841)
