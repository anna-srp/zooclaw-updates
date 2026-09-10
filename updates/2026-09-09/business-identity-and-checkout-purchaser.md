---
title: "修复：企业后台明明是团队管理员，买垂直行业 Pack 却被拦「仅企业账号可购买」"
type: "Bug Fix"
priority: "高"
date: "2026-09-09"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：企业后台明明是团队管理员，买垂直行业 Pack 却被拦「仅企业账号可购买」

## 核心宣传点

有客户报了个很难自证的问题：他两个 Business 账号在生产环境里都是团队管理员，后端也确实接受了他们的结账请求（2026-09-09 两次 `POST /vertical-pack/plan/…/purchase` 都返回 201），但页面就是弹「只有企业账号才能购买」。

那这个判断只能是**拿另一个身份**算出来的。根因有两条，这次一起收掉：

**一、身份来源有两个，还会互相打架。** Business（企业后台）与主站共用会话 Cookie，但它此前还会读一个遗留的 localStorage 账号 token（`zooclaw:auth:account_token`）；而 BFF 在转发时**优先用 `Authorization` 头**——于是浏览器里一个过期的旧 token 反而能盖掉正确的 Cookie 身份。现在身份和所有 `/api/claw/*`、`/api/auth/me`、`/api/r2/*` 调用**只认 `zc_session` Cookie**，遗留 key 会在下一次身份加载时被清掉。

**二、身份还会「过期不刷新」。** 身份查询用的是 `staleTime: Infinity`，意味着在别的标签页里换了账号、Cookie 变了，这个页面还拿着旧组织在用。现在**切回标签页 / 网络重连时会刷新身份**，进入垂直行业 Pack 结账页时也刷；身份请求与 `/api/auth/me` 响应一律禁用 HTTP 缓存。退出登录改成**等服务端确认删掉 Cookie 之后**才清理客户端查询并跳登录页，失败会给一条本地化的错误提示，不再是「发出删除请求就当成功」的竞态。

**三、页面终于告诉你「你是谁」。** 结账页现在直接显示购买人——头像、姓名、邮箱、组织，以及 Business / Personal 标签；付款状态和「仅企业账号可购买」的拦截状态**两种情况都显示**。付款状态下还加了「不是你？切换账号」。这条其实是运维体感最强的改动：以前客户截个图过来，谁也看不出那一刻用的是哪个账号。

共用 Cookie 名与域、遗留 token 的兼容性、后端购买授权逻辑均未改动。

## 原始内容

本条合并同一问题链上的两个 PR。

### fix(enterprise-admin): refresh shared session identity and await logout (#3674)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `daba44cf`
- PR: #3674
- 作者: sam-srp
- 日期: 2026-09-09T06:17:32Z

Summary：切回标签页/重连时以及进入垂直行业 Pack 结账页时刷新 Business 身份，不再在共用 Cookie 变化后仍保留「永久新鲜」的身份；身份请求与 `/api/auth/me` 响应禁用 HTTP 缓存；等服务端 Cookie 删除成功后再清客户端查询并跳登录，失败给本地化错误；保留既有共用 Cookie 名/域、遗留 token 兼容与后端购买授权。

Root cause：Business 与主站共用会话 Cookie，但身份查询用了 `staleTime: Infinity`，标签页外的 Cookie 变化会让购买页继续用旧组织。另外 logout 未等待 Cookie 删除结果就直接跳转，形成竞态并隐藏失败。PR 明确说明：这两条是已验证的**代码级风险**，但不宣称它们就是客户事故的确定解释——出问题页面的确切身份没有被抓到；不改动客户组织数据或支付服务。

Test plan：Enterprise Admin 套件 59 文件 / 438 tests passed；`tsc --noEmit`；改动文件全量 ESLint 与 `git diff --check`；回归覆盖 Personal↔Team 双向焦点刷新、pending/failed logout、跳转顺序、no-store 身份响应。未执行：部署后的主站/Business 多标签页实机验证。

### fix(enterprise-admin): Cookie-only identity and show purchaser on Vertical Pack checkout (#3676)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `ae1740fc`
- PR: #3676
- 作者: bill-srp
- 日期: 2026-09-09T11:28:40Z

Summary：Business 不再读遗留 localStorage 账号 token，身份与全部 `/api/claw/*`、`/api/auth/me`、`/api/r2/*` 调用仅依赖 `zc_session` Cookie，仍持有遗留 key 的浏览器在下次身份加载时被清除；垂直行业 Pack 结账页显示购买人（头像、姓名、邮箱、组织、Business/Personal 标签），付款状态与「仅企业账号可购买」拦截状态均显示，付款状态下另加「不是你？切换账号」。

Root cause：客户报告被企业专属拦截，但其两个 Business 账号在生产环境均为团队管理员且后端接受了结账（2026-09-09 两次 purchase 均 201）。该拦截必然是按另一个身份判定的：Business 与主站共用会话 Cookie，而 localStorage 里过期的遗留 bearer token 可能在 API 调用上覆盖 Cookie（BFF 优先 `Authorization` 头）。页面从未显示当前以哪个账号在操作，客户与支持都无法从截图判断。#3674 修的是身份刷新与 logout 竞态，本 PR 移除客户端第二个身份来源并把当前身份显式暴露出来。

主要改动文件：`services/api.ts`（去掉 `Authorization` 头，改同源 Cookie 认证）、`lib/auth.ts`（`fetchAccountUser` 仅 Cookie；移除 `fetchLegacyUserMe` 与 `getStoredAccountToken()` fallback；`loadCurrentUser` 先清遗留 key）、删除 `lib/legacy-auth-header.ts`、结账页 `useCheckoutViewModel.ts` / `CheckoutPageClient.tsx` 新增 `CheckoutIdentityBlock`。

## 备注

发布状态：两条均已上线（已包含在最新 `ecap-*-release` 正式发布中）。

toB 相关：直接影响企业客户的垂直行业 Pack 购买链路，属客户报障后的修复。对外传播建议低调处理或只在 changelog 呈现——#3674 自述并未确证这两条就是该客户事故的根因，对外不宜表述为「已彻底解决该购买失败问题」。「结账页显示购买人 + 切换账号」这一点可以作为正向体验改进单独讲。
