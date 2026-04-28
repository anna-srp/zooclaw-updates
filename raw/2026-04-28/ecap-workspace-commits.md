# ecap-workspace commits — 2026-04-28

> 抓取范围：2026-04-27T00:00:00Z ～ 2026-04-28T23:59:59Z  
> 共计 42 条 commits

---

## a99e03a2 — fix(web): add QueryClientProvider to share replay page (#1413)
- **作者**: peter-srp  
- **时间**: 2026-04-27T13:21:24Z  
- **PR Body**:  
  修复 `/share/[shareId]` 页面（独立 html layout，绕过 ClientLayout）在用户预览分享回放的附件时，因 QueryClient 缺失而崩溃的问题。改为用 `createQueryClient` factory 包裹 `ReplayClient`。  
  Sentry: https://serendipity-one-inc.sentry.io/issues/7443872355/

---

## af70d4f7 — refactor(web): replace state-reset useEffect with parent key prop (#1414)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T13:02:55Z

---

## 25e7585f — chore(deps-dev): bump dotenv-cli from 7.4.4 to 11.0.0 in /web (#1409)
- **作者**: dependabot[bot]  
- **时间**: 2026-04-27T12:49:26Z

---

## 050051f3 — chore(deps): ignore eslint major bumps in /web (#1412)
- **作者**: dependabot[bot]  
- **时间**: 2026-04-27T12:42:37Z

---

## ac015a9a — chore(deps): bump stripe from 20.4.0 to 20.4.1 in /web (#1408)
- **作者**: dependabot[bot]  
- **时间**: 2026-04-27T12:41:57Z

---

## 0802a564 — chore(deps-dev): bump cross-env from 7.0.3 to 10.1.0 in /web (#1338)
- **作者**: dependabot[bot]  
- **时间**: 2026-04-27T12:39:20Z

---

## 00b1e0ed — refactor(web): drop ref-sync useEffect in three hooks (#1396)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T12:27:44Z

---

## fffa1a0b — chore(deps): bump marked from 16.4.2 to 18.0.0 in /web (#1335)
- **作者**: dependabot[bot]  
- **时间**: 2026-04-27T12:23:03Z

---

## 9f77c87a — fix(claw-interface): retry auth service call once on transient failure (#1393)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T12:12:37Z  
- **PR Body**:  
  Auth service 14天内约10次短暂不可达错误（集中在 pod 滚动升级期间）。新增单次重试（延迟1s）以吸收瞬时网络故障，改进错误日志输出。

---

## 27e79899 — chore(web): 收紧 jscpd 阈值 (#1410)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T11:56:12Z

---

## a8b74ceb — refactor(web): 抽 useSavingState hook (#1405)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T11:48:38Z

---

## 441893b1 — chore(deps): ignore jsdom + stripe major bumps in /web (#1407)
- **作者**: dependabot[bot]  
- **时间**: 2026-04-27T11:48:06Z

---

## a190e980 — chore(deps-dev): bump globals from 16.5.0 to 17.5.0 in /web (#1401)
- **作者**: dependabot[bot]  
- **时间**: 2026-04-27T11:43:11Z

---

## 66579cbf — refactor(web): UseBillingCreditsReturn extends SubscriptionContext (#1404)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T11:39:28Z

---

## 03072731 — fix(web): harden MM file upload — auth detection, retry, concurrent guard (#1380)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T11:37:35Z  
- **PR Body**:  
  修复用户间歇性文件上传失败（Sentry 15 events，2 users）。根因：快速连续上传时 auth token 失效 + CORS 网络拒绝 + 无并发保护。新增 auth expiry 检测、失败重试、并发上传保护。

---

## ea528523 — refactor(web): 抽 beginAsyncReinit helper (#1400)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T11:33:54Z

---

## 44293c00 — chore(deps): align @types/node (#1398)
- **作者**: dependabot[bot]  
- **时间**: 2026-04-27T11:22:12Z

---

## 8dbba699 — refactor(web): 抽 JSBridge 共享类型契约 (#1399)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T11:20:46Z

---

## 1434dda3 — chore(web): 清理 modal-overlay 假豁免 (#1397)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T11:13:51Z

---

## 58dc6188 — refactor(web): 抽取 useBodyLock hook (#1394)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T10:59:54Z

---

## 3ce622a5 — fix(claw-interface): include APP_FRONTEND_URL in portal return_url allowlist (#1395)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T10:14:44Z

---

## 00af3872 — feat(chat): 功能上新弹窗支持多 slide 轮播，新增 PPTX Master 上新 (#1315)
- **作者**: wangyin-srp  
- **时间**: 2026-04-27T09:59:47Z  
- **PR Body**:  
  把现有的 Seedance 上新弹窗从单一功能展示，改成支持任意数量功能上新的通用轮播弹窗。新增 PPTX Master 作为第二张 slide。核心重构：SeedanceLaunchModal → FeatureLaunchModal，内容改成 data-driven 的 SLIDES 数组，后续加第3/4个功能上新只要往数组里加一条。新增多媒体类型支持（视频+图片），轮播导航（Next/Previous/Got it），indicator dots。

---

## 344f7eb3 — refactor(web): 抽取 useEscapeKey hook (#1392)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T09:44:45Z

---

## 613ae539 — chore(web): 6 处机械替换 inline style → Tailwind class (#1391)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T09:28:06Z

---

## 149a266a — fix: preserve /chat draft when switching agents (#1389)
- **作者**: wangyin-srp  
- **时间**: 2026-04-27T09:20:17Z  
- **PR Body**:  
  切换 Agent 时保留 /chat 输入框的草稿内容（存入 sessionStorage）。修复此前切换 Agent 会清空草稿的问题，仅在发送后或用户手动清空时才清除。

---

## ea2e7cc5 — chore(web): 清理 UserAvatar 死码 (#1390)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T09:18:48Z

---

## e62c41ea — fix(web): decouple chat UI from bot init readiness (ECA-542) (#1388)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T09:03:17Z  
- **PR Body**:  
  关闭 ECA-542。两个配套修复：把"3分钟空白等待→错误"变成"立刻显示聊天UI+输入禁用→bot唤醒→输入可用"。1. 提高 INIT_POLL_TIMEOUT_MS 3分→5分（实测 bot 唤醒需~210s）；2. 将 UI ready 判断与 bot init 轮询解耦——bot 未就绪时显示 chatUI 但锁定输入，提升感知体验。

---

## fd6f4c03 — feat(web): User Guide 跳转到独立 tips 站点（新标签页）(#1311)
- **作者**: peter-srp  
- **时间**: 2026-04-27T08:17:02Z  
- **PR Body**:  
  User Guide 点击改为新标签页打开独立 tips 站点（zooclaw.ai/tips/），支持多语言（zh/ja/en）。官网 header 和侧栏 sidebar 均已更新。Cloudflare zone 路由 /tips/* → tips worker，前端不再耦合具体域名。

---

## 0e1c3fda — fix(web): lock input during bootstrap greeting after /new session (#1383)
- **作者**: wangyin-srp  
- **时间**: 2026-04-27T08:15:42Z  
- **PR Body**:  
  修复 /new 会话后输入框有1.5s窗口期短暂可用的问题（用户可偷跑消息导致时序混乱）。改进流程：/new 发送→立即锁定输入→greeting流式输出完毕→1.5s后解锁。异常兜底：10s后自动解锁。

---

## f59f5b6c — fix(web): enforce file upload limit during in-progress uploads (#1385)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T08:02:03Z  
- **PR Body**:  
  修复上传进行中拖入更多文件可绕过10文件限制的竞态条件。根因：count检查读取的是异步React state，尚未更新。新增同步ref计数器（pendingFileCountRef）+ R2 placeholder计数关闭竞态。

---

## 48a13631 — docs(web): two-week refactor + lint controls status report (#1386)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T07:54:04Z

---

## 574fe9fd — fix(chat): refresh credits when user menu opens (#1382)
- **作者**: wangyin-srp  
- **时间**: 2026-04-27T07:44:54Z  
- **PR Body**:  
  用户打开聊天菜单时刷新积分/额度显示，保证显示最新数据。

---

## 8de97690 — refactor(web): remove brand info from user-agent.ts (#1384)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T07:37:01Z

---

## 77ccd520 — Investigate/sentry 7417488438 user spam (#1377)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T06:57:28Z

---

## 37e9c99f — feat(ios): Add gradient background to chat input overlay (#1381)
- **作者**: peter-srp  
- **时间**: 2026-04-27T06:50:12Z  
- **PR Body**:  
  iOS 聊天输入框 overlay 新增渐变背景，改善视觉层次感和可读性。

---

## 6c40c6c0 — fix(web): downgrade MM message-too-long send failure from error to warn (#1379)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T06:38:17Z

---

## a53a96af — revert(devcontainer): terminal default location back to bottom panel (#1378)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T06:32:00Z

---

## c1764fc4 — fix(claw-interface): retry billing-gateway GETs on connect transients (#1373)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T06:18:08Z  
- **PR Body**:  
  关闭 ECA-558。claw-interface 对 billing-gateway 的 ConnectTimeout 错误集中在 BG pod 重启期间（iptables规则未更新窗口期）。新增 GET 请求的 connect transient 重试，防止用户操作受 BG 部署影响。

---

## 299ff4b2 — fix(ci): re-indent claude-develop.yaml block scalar (#1375)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T04:52:37Z

---

## 6046fc15 — refactor(web): heroicons PR 7 (#1372)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T03:40:32Z

---

## 35e0a1d7 — chore(web): lock heroicons migration policy via ESLint allowlist (#1371)
- **作者**: Chris@ZooClaw  
- **时间**: 2026-04-27T03:23:04Z

---

## 4c21a210 — fix(ios): Fix chat tap gestures and streaming app hang (#1370)
- **作者**: peter-srp  
- **时间**: 2026-04-27T02:34:00Z  
- **PR Body**:  
  三个 iOS 聊天视图修复：1. 解除点击手势拦截（ScrollView 上的 onTapGesture 抢占导致链接/图片/视频/文件卡片无法点击）；2. 修复 bubble overlay 吸收所有点击的问题；3. 修复 streaming 期间 app 卡死（可能由主线程操作引起）。
