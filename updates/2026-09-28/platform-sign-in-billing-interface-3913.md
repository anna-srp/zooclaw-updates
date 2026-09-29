---
title: "开发者平台换新登录与账单界面：支持 Google 和邮箱验证码登录，余额入口改为 Credits 并可直接充值"
type: "Improvement"
priority: "中"
date: "2026-09-28"
status: "待审核"
channels: ""
---

# 开发者平台换新登录与账单界面：支持 Google 和邮箱验证码登录，余额入口改为 Credits 并可直接充值

## 核心宣传点

开发者平台把内嵌的第三方登录组件换成了自己的登录流程，支持 Google 和邮箱验证码两种方式，带回调处理，认证报错也更收敛、不再把底层细节抛给用户。界面整体套上 ZooWork 配色，侧边栏链接、项目图标和不可用设置项的状态都做了对齐。侧栏的余额入口改名为 Credits，点整行进账单页，点 Add funds 直接打开充值弹窗。充值金额给了 $20、$100、$500 三个快捷档加 Other，Other 支持 5 到 500 美元的整数金额；结账和支付处理仍走现有的平台接口与 Stripe 流程。注意生产环境的登录配置需要单独手动调整后才能上线这套登录方式。

## 分级

- 内部：P1
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary
- Replace the embedded Clerk sign-in widget with a Platform login flow for Google and email verification codes, including callback handling and safer auth errors.
- Apply the ZooWork palette to Platform and align sidebar links, project icons, and unavailable settings states.
- Rename the sidebar balance entry to Credits; make the row open Billing and Add funds open the existing top-up dialog directly.
- Show $20, $100, $500, and Other in the dialog. Other accepts whole-dollar amounts from $5 to $500; checkout and payment processing remain on the existing Platform API and Stripe flow.

## Rollout prerequisite
- The development Clerk instance has passwordless sign-up enabled. The production Clerk instance has not been updated. Before a production Platform deployment, make the production sign-up password optional, enable email codes for sign-in and sign-up, and verify new-user email and Google registration there. Production deployment is a separate manual workflow; this PR does not change production Clerk configuration.

## Test plan
- [x] Platform lint
- [x] Platform typecheck
- [x] Platform unit tests (70 passed)
- [x] Platform production build
- [x] PR size check (1,593 / 3,000 lines)
- [ ] Live production Clerk registration and Stripe checkout were not run.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `b255ec8fa6484bf0435e7c9382b4adef6d63ae2d`
- PR: #3913
- 作者：finn-srp
- 日期：2026-09-28T12:47:33Z

### Commit Message

```
feat(platform): refine sign-in and billing interface (#3913)

## Summary
- Replace the embedded Clerk sign-in widget with a Platform login flow
for Google and email verification codes, including callback handling and
safer auth errors.
- Apply the ZooWork palette to Platform and align sidebar links, project
icons, and unavailable settings states.
- Rename the sidebar balance entry to Credits; make the row open Billing
and Add funds open the existing top-up dialog directly.
- Show $20, $100, $500, and Other in the dialog. Other accepts
whole-dollar amounts from $5 to $500; checkout and payment processing
remain on the existing Platform API and Stripe flow.

## Rollout prerequisite
- The development Clerk instance has passwordless sign-up enabled. The
production Clerk instance has not been updated. Before a production
Platform deployment, make the production sign-up password optional,
enable email codes for sign-in and sign-up, and verify new-user email
and Google registration there. Production deployment is a separate
manual workflow; this PR does not change production Clerk configuration.

## Test plan
- [x] Platform lint
- [x] Platform typecheck
- [x] Platform unit tests (70 passed)
- [x] Platform production build
- [x] PR size check (1,593 / 3,000 lines)
- [ ] Live production Clerk registration and Stripe checkout were not
run.
```

来源：SerendipityOneInc/ecap-workspace @ b255ec8f，PR #3913，作者 finn-srp。
