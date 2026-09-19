---
title: "fix(web): link directly to default-English Agent Gallery (#3791)"
type: "Bug Fix"
priority: "中"
date: "2026-09-18"
status: "待审核"
channels: ""
---

# 修复：官网 Agent Gallery 入口改为直连默认英文页面

## 核心宣传点

Agent Gallery 已经迁到默认英文地址，但官网导航、Solutions 推荐卡片和页脚还在用旧链接，各语言站点点进去会绕路。现在统一指向 https://zoowork.ai/agent-gallery，根站点地图也同步改成 /agent-gallery/sitemap.xml，浏览器正常跳转不受影响。

## 分级

- 内部：P2
- 外部：C
- 发布状态：已合并待发版

## PR 说明

## Summary

- Point the shared Agent Gallery URL to `https://zoowork.ai/agent-gallery`, so the navigation, featured Solutions cards and footer link directly to the default-English Worker pages in every website locale.
- Update the root sitemap to `/agent-gallery/sitemap.xml` and refresh the existing navigation/sitemap expectations. Keep ordinary browser navigation across Worker deployments.

## Root cause

Gallery migrated to the default-English URL in SerendipityOneInc/zoowork-agent-gallery#5 (deployed main `1468a36`), but the main website still advertises the old `/en/agent-gallery` URLs. Those links now take an unnecessary 301, and the root index still references the redirected child sitemap.

## Test plan

- [x] `bash scripts/verify-web.sh` scoped to the Gallery constant and three existing specs: TypeScript, governance guards, 15 targeted tests and ESLint passed. A line-wrap lint issue was fixed and the affected checks rerun.
- [x] Full pre-commit frontend lint passed; production Gallery hub and generated sitemap are direct 200 with 11 new URLs.
- [x] PR CI: 23 checks passed, 15 skipped; web build and full web test jobs passed. Claude and Codex automated reviews reported no findings.
- [x] Local Chrome: English navigation, Chinese featured card and Chinese footer clicks reach the new production Gallery hub/details; both locale pages and root XML contain only the new Gallery URLs. Local marketing preview used a nonfunctional Firebase placeholder; no login flow was tested.
- [ ] After merge: verify English and Chinese Solutions, navigation and footer on Staging; publish the verified commit through Production approval; verify root XML, then update GSC submissions.

This is a frontend-only follow-up. Gallery content/Worker routes, other marketing-page language URLs and GSC are unchanged by this PR.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `ee377fc6a5f95b2b3f00805f423a76c4cb326263`
- PR: #3791
- 作者：Mori-srp
- 日期：2026-09-18T08:23:28Z

### Commit Message

```
fix(web): link directly to default-English Agent Gallery (#3791)

## Summary

- Point the shared Agent Gallery URL to
`https://zoowork.ai/agent-gallery`, so the navigation, featured
Solutions cards and footer link directly to the default-English Worker
pages in every website locale.
- Update the root sitemap to `/agent-gallery/sitemap.xml` and refresh
the existing navigation/sitemap expectations. Keep ordinary browser
navigation across Worker deployments.

## Root cause

Gallery migrated to the default-English URL in
SerendipityOneInc/zoowork-agent-gallery#5 (deployed main `1468a36`), but
the main website still advertises the old `/en/agent-gallery` URLs.
Those links now take an unnecessary 301, and the root index still
references the redirected child sitemap.

## Test plan

- [x] `bash scripts/verify-web.sh` scoped to the Gallery constant and
three existing specs: TypeScript, governance guards, 15 targeted tests
and ESLint passed. A line-wrap lint issue was fixed and the affected
checks rerun.
- [x] Full pre-commit frontend lint passed; production Gallery hub and
generated sitemap are direct 200 with 11 new URLs.
- [x] PR CI: 23 checks passed, 15 skipped; web build and full web test
jobs passed. Claude and Codex automated reviews reported no findings.
- [x] Local Chrome: English navigation, Chinese featured card and
Chinese footer clicks reach the new production Gallery hub/details; both
locale pages and root XML contain only the new Gallery URLs. Local
marketing preview used a nonfunctional Firebase placeholder; no login
flow was tested.
- [ ] After merge: verify English and Chinese Solutions, navigation and
footer on Staging; publish the verified commit through Production
approval; verify root XML, then update GSC submissions.

This is a frontend-only follow-up. Gallery content/Worker routes, other
marketing-page language URLs and GSC are unchanged by this PR.
```

## 备注

发布状态：已合并待发版（尚未包含在任何 ecap-*-release tag 中，最新正式 release 为 ecap-v0.19.16-release）。

来源：SerendipityOneInc/ecap-workspace @ ee377fc6，PR #3791，作者 Mori-srp。
