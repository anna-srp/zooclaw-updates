---
title: "官网页脚重组为 Product / Use Cases / Resources / Company 四栏，DCMA 错别字改成 DMCA"
type: "Improvement"
priority: "中"
date: "2026-09-30"
status: "待审核"
channels: ""
---

# 官网页脚重组为 Product / Use Cases / Resources / Company 四栏，DCMA 错别字改成 DMCA

## 核心宣传点

官网营销页脚按导航结构重新排了一遍。Product 栏放 Agent Builder、Managed Agent API（暂不可点，带「Coming soon」标记，域名就绪后改一个开关就变成链接）、Enterprise、iOS App（原有二维码弹窗不变）、ZooData（新标签页打开）。Industry 栏改名为 Use Cases，放 Solutions、Agent Gallery 和原有的 9 个行业页。Resources 栏放 Pricing、Blog、Docs。Company 栏内容不变，只把 10 个语种里的 DCMA 错别字改成 DMCA。页脚移除了 Web App、Learn、What's New 三个入口以及相关的无用逻辑，顶部导航不受影响。新增的 4 个文案键在 10 个语种都已补齐。

## 分级

- 内部：P2
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Linear
N/A

## Summary
Reorganizes the marketing footer (spec approved by David):
- **Product**: Agent Builder → /home · Managed Agent API (non-clickable,
"Coming soon" badge; data keeps https://platform.zoowork.ai +
`comingSoon` flag so it becomes a link by flipping one flag once DNS is
live) · Enterprise → /enterprise · iOS App (existing QR popup,
unchanged) · ZooData → https://zoodata.ai (new tab)
- **Use Cases** (new column title, replaces Industry): Solutions →
/solutions · Agent Gallery · the 9 existing industry pages (unchanged)
- **Resources**: Pricing → /pricing · Blog · Docs
- **Company**: unchanged, label typo DCMA → DMCA in all 10 locales
- Removed from footer: Web App, Learn, What's New. Removed the
now-unused `onWebApp` / footer `tips` plumbing (top nav still uses
`tips`). Locale keys `footerWebApp`, `resLearn`, `resWhatsNew`,
`footerIndustry` kept.
- New locale keys: `footerUseCases`, `footerAgentBuilder`,
`footerManagedAgentApi`, `footerComingSoon` (all 10 locales).

## Test plan
- [x] Updated landing-content, landing-footer, marketing-chrome and
legal-footer-links unit tests (new columns/order, /home link,
coming-soon renders as non-link text, DMCA, new labels)
- [x] Full unit suite, `tsc --noEmit`, `lint`, `lint:ci` pass locally
- [x] Rendered `/` and `/zh` locally at 1440px and checked the EN / ZH
footer (screenshots available on request)

## Follow-ups (not in this PR)
- Tips pages (/tips/) lose their main-site footer link. Add
`/tips/sitemap.xml` (and `/blog/sitemap-index.xml`) to the root sitemap
index so they stay discoverable.
- Decide whether to noindex `/home` (empty initial HTML, currently
index,follow).
- Top-nav alignment (e.g. a Product dropdown, ZooData placement) is
pending.
- Switch Managed Agent API to a real link once platform.zoowork.ai
resolves.
- Sync the blog (zooclaw-blog) and agent-gallery footer copies (also fix
DCMA in gallery-chrome.tsx).

---

## 概要
按 David 批准的方案调整官网页脚：
- **产品**：Agent Builder → /home · Managed Agent API（不可点击，带「即将推出」标记；数据里保留
https://platform.zoowork.ai 和 `comingSoon` 标志，域名解析上线后改一个标志即可变成链接）· 企业版 →
/enterprise · iOS 应用（沿用二维码弹窗）· ZooData → https://zoodata.ai（新标签页）
- **应用场景**（新列名，取代「行业」列）：解决方案 → /solutions · Agent Gallery · 原有 9
个行业页（不变）
- **资源**：定价 → /pricing · 博客 · 文档
- **公司**：不变，10 个语言的 DCMA 拼写错误改为 DMCA
- 页脚去掉 Web App、学习、更新日志，并删除不再使用的 `onWebApp` 和页脚 `tips` 相关代码（顶部导航仍使用
`tips`）。保留 `footerWebApp`、`resLearn`、`resWhatsNew`、`footerIndustry` 文案
key。
- 新增文案
key：`footerUseCases`、`footerAgentBuilder`、`footerManagedAgentApi`、`footerComingSoon`（10
种语言）。

## 测试
- 更新 landing-content、landing-footer、marketing-chrome、legal-footer-links
单测（新列和顺序、/home 链接、「即将推出」渲染为不可点击文字、DMCA、新文案）。
- 本地全量单测、`tsc --noEmit`、`lint`、`lint:ci` 均通过。
- 本地以 1440px 渲染 `/` 和 `/zh` 检查中英文页脚（截图可按需提供）。

## 后续（不在本 PR）
- Tips 页面（/tips/）失去主站页脚入口，建议把 `/tips/sitemap.xml`（及
`/blog/sitemap-index.xml`）加入根 sitemap 索引，保证可被搜索引擎发现。
- `/home` 是否加 noindex（初始 HTML 为空，目前 index,follow）待定。
- 顶部导航对齐（如「产品」下拉菜单、ZooData 位置）待定。
- platform.zoowork.ai 解析上线后，把 Managed Agent API 改为真实链接。
- 同步博客站（zooclaw-blog）和 agent-gallery 的页脚副本（gallery-chrome.tsx 里也有 DCMA）。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `71940e63b846e8402a9a9a875fef24cc9ac61a77`
- PR: #3957
- 作者：Mori-srp
- 日期：2026-09-30T14:47:40Z

### Commit Message

```
feat(landing): align marketing footer with nav (Product / Use Cases / Resources), fix DMCA label (#3957)

## Linear
N/A

## Summary
Reorganizes the marketing footer (spec approved by David):
- **Product**: Agent Builder → /home · Managed Agent API (non-clickable,
"Coming soon" badge; data keeps https://platform.zoowork.ai +
`comingSoon` flag so it becomes a link by flipping one flag once DNS is
live) · Enterprise → /enterprise · iOS App (existing QR popup,
unchanged) · ZooData → https://zoodata.ai (new tab)
- **Use Cases** (new column title, replaces Industry): Solutions →
/solutions · Agent Gallery · the 9 existing industry pages (unchanged)
- **Resources**: Pricing → /pricing · Blog · Docs
- **Company**: unchanged, label typo DCMA → DMCA in all 10 locales
- Removed from footer: Web App, Learn, What's New. Removed the
now-unused `onWebApp` / footer `tips` plumbing (top nav still uses
`tips`). Locale keys `footerWebApp`, `resLearn`, `resWhatsNew`,
`footerIndustry` kept.
- New locale keys: `footerUseCases`, `footerAgentBuilder`,
`footerManagedAgentApi`, `footerComingSoon` (all 10 locales).

## Test plan
- [x] Updated landing-content, landing-footer, marketing-chrome and
legal-footer-links unit tests (new columns/order, /home link,
coming-soon renders as non-link text, DMCA, new labels)
- [x] Full unit suite, `tsc --noEmit`, `lint`, `lint:ci` pass locally
- [x] Rendered `/` and `/zh` locally at 1440px and checked the EN / ZH
footer (screenshots available on request)

## Follow-ups (not in this PR)
- Tips pages (/tips/) lose their main-site footer link. Add
`/tips/sitemap.xml` (and `/blog/sitemap-index.xml`) to the root sitemap
index so they stay discoverable.
- Decide whether to noindex `/home` (empty initial HTML, currently
index,follow).
- Top-nav alignment (e.g. a Product dropdown, ZooData placement) is
pending.
- Switch Managed Agent API to a real link once platform.zoowork.ai
resolves.
- Sync the blog (zooclaw-blog) and agent-gallery footer copies (also fix
DCMA in gallery-chrome.tsx).

---

## 概要
按 David 批准的方案调整官网页脚：
- **产品**：Agent Builder → /home · Managed Agent API（不可点击，带「即将推出」标记；数据里保留
https://platform.zoowork.ai 和 `comingSoon` 标志，域名解析上线后改一个标志即可变成链接）· 企业版 →
/enterprise · iOS 应用（沿用二维码弹窗）· ZooData → https://zoodata.ai（新标签页）
- **应用场景**（新列名，取代「行业」列）：解决方案 → /solutions · Agent Gallery · 原有 9
个行业页（不变）
- **资源**：定价 → /pricing · 博客 · 文档
- **公司**：不变，10 个语言的 DCMA 拼写错误改为 DMCA
- 页脚去掉 Web App、学习、更新日志，并删除不再使用的 `onWebApp` 和页脚 `tips` 相关代码（顶部导航仍使用
`tips`）。保留 `footerWebApp`、`resLearn`、`resWhatsNew`、`footerIndustry` 文案
key。
- 新增文案
key：`footerUseCases`、`footerAgentBuilder`、`footerManagedAgentApi`、`footerComingSoon`（10
种语言）。

## 测试
- 更新 landing-content、landing-footer、marketing-chrome、legal-footer-links
单测（新列和顺序、/home 链接、「即将推出」渲染为不可点击文字、DMCA、新文案）。
- 本地全量单测、`tsc --noEmit`、`lint`、`lint:ci` 均通过。
- 本地以 1440px 渲染 `/` 和 `/zh` 检查中英文页脚（截图可按需提供）。

## 后续（不在本 PR）
- Tips 页面（/tips/）失去主站页脚入口，建议把 `/tips/sitemap.xml`（及
`/blog/sitemap-index.xml`）加入根 sitemap 索引，保证可被搜索引擎发现。
- `/home` 是否加 noindex（初始 HTML 为空，目前 index,follow）待定。
- 顶部导航对齐（如「产品」下拉菜单、ZooData 位置）待定。
- platform.zoowork.ai 解析上线后，把 Managed Agent API 改为真实链接。
- 同步博客站（zooclaw-blog）和 agent-gallery 的页脚副本（gallery-chrome.tsx 里也有 DCMA）。
```

来源：SerendipityOneInc/ecap-workspace @ 71940e63，PR #3957，作者 Mori-srp。
