---
title: "产品正式更名 ZooWork：全站用户可见文案、图标与分享信息统一切换"
type: "产品基础功能更新"
priority: "高"
date: "2026-09-01"
status: "待审核"
channels: "站内弹窗+Use Case+Discord+changelog"
---

# 产品正式更名 ZooWork：全站用户可见文案、图标与分享信息统一切换

## 核心宣传点

主应用、企业管理后台和控制台里所有用户能看到的「ZooClaw / Claw」产品字样全部换成了 ZooWork，10 种语言的文案词典、页面标题、SEO 与分享卡片信息、PWA manifest 文案、静态指南正文、图片 alt 文本和展示用的字标素材一并更新。首页头图内容在桌面端改为整体居中，轮播的 Agent 角色词按实际渲染宽度居中，最长的西班牙语、意大利语变体在手机上也能正常换行。

身份设置页的正式地址改为 `/identity`，旧的 `/claw-settings` 做 301 永久跳转并保留查询参数，老书签不会失效。内部包名、API、标识符、兼容路由、OpenClaw 相关术语、域名和支持邮箱都保持不变，只动用户可见的表述。

配套还有两处品牌收尾：登录页的 ZooWork 品牌在所有主题、所有落地页语言下都补上了回归测试覆盖（不改登录行为和 Logo 素材）；iOS App 的侧边栏、启动页、引导页 Logo 换成新版 ZooWork 素材，欢迎页的背景、文案、字体、间距和按钮圆角按定稿设计刷新，引导流程里的通知示例也从 ZooClaw 改成 ZooWork。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `064f4800f2698db905cd1f1f4473e7f18a8f8e12`
- PR: #3609
- 作者: shana-srp
- 日期: 2026-09-01T08:41:56Z

### Commit Message

```
fix(brand): complete ZooWork user-facing rebrand (#3609)

## Summary
- Center the homepage hero content as a cohesive desktop group and keep
rotating agent roles centered by rendered width
- Keep every localized rotating role mobile-wrappable, including the
longest Spanish and Italian variants
- Replace all remaining user-visible ZooClaw / Claw product wording with
ZooWork across the main app, enterprise admin, and dashboard console
- Update all 10 locale dictionaries, page metadata, SEO/share metadata,
manifest copy, static guide text, image alt text, and displayed wordmark
assets
- Make `/identity` the canonical Identity page URL and permanently
redirect the legacy `/claw-settings` path while preserving query
parameters
- Preserve internal package names, APIs, identifiers, compatibility
routes, OpenClaw terminology, domains, and support email addresses

## Test plan
- [x] `bash scripts/verify-web.sh` — TypeScript, full Vitest suite
(9,411 passed), and ESLint
- [x] `bash scripts/verify-web.sh --no-test` after final formatting pass
- [x] `pnpm --dir web/enterprise-admin test` — 421 passed
- [x] `pnpm --dir web/enterprise-admin lint`
- [x] `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- [x] `pnpm --dir web/dashboard-console test` — 651 passed
- [x] `pnpm --dir web/dashboard-console lint`
- [x] `pnpm --dir web/dashboard-console exec react-router typegen`
- [x] `pnpm --dir web/dashboard-console exec tsc -b --pretty false`
- [x] AST residual scan across production source roots; only the
intentionally preserved `ZooClaw.ai` legal-domain references remain
- [x] Added regression coverage that rejects capitalized legacy product
wording in every supported locale dictionary

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

```
## Summary
- Center the homepage hero content as a cohesive desktop group and keep rotating agent roles centered by rendered width
- Keep every localized rotating role mobile-wrappable, including the longest Spanish and Italian variants
- Replace all remaining user-visible ZooClaw / Claw product wording with ZooWork across the main app, enterprise admin, and dashboard console
- Update all 10 locale dictionaries, page metadata, SEO/share metadata, manifest copy, static guide text, image alt text, and displayed wordmark assets
- Make `/identity` the canonical Identity page URL and permanently redirect the legacy `/claw-settings` path while preserving query parameters
- Preserve internal package names, APIs, identifiers, compatibility routes, OpenClaw terminology, domains, and support email addresses

## Test plan
- [x] `bash scripts/verify-web.sh` — TypeScript, full Vitest suite (9,411 passed), and ESLint
- [x] `bash scripts/verify-web.sh --no-test` after final formatting pass
- [x] `pnpm --dir web/enterprise-admin test` — 421 passed
- [x] `pnpm --dir web/enterprise-admin lint`
- [x] `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- [x] `pnpm --dir web/dashboard-console test` — 651 passed
- [x] `pnpm --dir web/dashboard-console lint`
- [x] `pnpm --dir web/dashboard-console exec react-router typegen`
- [x] `pnpm --dir web/dashboard-console exec tsc -b --pretty false`
- [x] AST residual scan across production source roots; only the intentionally preserved `ZooClaw.ai` legal-domain references remain
- [x] Added regression coverage that rejects capitalized legacy product wording in every supported locale dictionary

```
