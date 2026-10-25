---
title: "修复：登录后重复跳转会清空充值弹窗里已填的金额"
type: "Bug Fix"
priority: "高"
date: "2026-10-22"
status: "待审核"
channels: ""
---

# 修复：登录后重复跳转会清空充值弹窗里已填的金额

## 核心宣传点

用户带着充值参数进入登录页，登录成功后开始填金额时，稍后完成的登录回调会再跳转一次，生成新的页面定位标识，导致按定位标识管理的充值弹窗会话被重新创建、已输入的金额被重置。修复方式是把跳转统一交给首页路由按已发布的登录状态执行，邮箱和 Google 登录表单只负责完成认证、不再自己跳转，同时保留首页的深链接解析、普通登录与会话恢复逻辑。没有加任何等待、重试，也没有放宽原有测试。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## 备注

这是 Platform 0.0.11 生产发布失败的修复；失败发生在测试阶段，未覆盖生产版本，修复合并并通过预发验收后需用新版本标签重新发布。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `f4aee4678372c76f72f0d0b4a9fbbd03a3f1b29f`
- PR: #4120
- 作者：lynn Zhuang
- 日期：2026-10-22T10:26:02Z

### Commit Message

```
fix(platform): 修复登录后重复跳转导致充值弹窗重置 (#4120)

## Summary

修复登录成功后重复导航导致充值弹窗被重新创建的问题。用户从 `?addFunds=1`
进入登录页，登录后开始填写金额时，稍后完成的登录回调可能再次跳转，清空金额草稿。现在由 `HomeRoute`
根据已发布的登录状态统一跳转，邮箱和 Google 登录表单只完成认证。

这是 [Platform 0.0.11
生产发布失败](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/39748356053)
的修复。失败发生在测试阶段，构建及 Cloudflare 上传均未执行，未覆盖生产版本。已推送的
`platform-v0.0.11-release` 不会移动；修复合并、staging 验收后应使用新版本标签发布。

## Root cause

`PasswordlessSignIn` 等待认证 Promise 后主动调用 `navigate`；与此同时，认证状态发布后
`HomeRoute` 已渲染 `Navigate`。两次导航会生成不同的 location key，`AddFundsProvider` 按
location key 管理的弹窗会话随之被重新创建。

CI 表现为 `findByRole` 找到的弹窗在断言前已脱离 DOM。控制认证状态先发布、Promise 后完成的时序后，邮箱和
Google 两个场景都能稳定复现：已输入的 `37` 被重置为
`20`。此次修复移除表单中的重复导航，保留首页的深链接解析、普通登录及恢复会话逻辑；没有增加 sleep、重试或放宽原测试。

## Test plan

- [x] 修改实现前，新增的邮箱 / Google 两项回归测试均因弹窗重建和草稿丢失失败；修改后通过。
- [x] 登录与路由相关 4 个测试文件、140 项测试通过，包含真实 auth provider 的跨标签页退出 / 重新登录用例。
- [x] Platform 全量 26 个测试文件、339 项测试通过。
- [x] Platform lint、TypeScript 检查及生产构建通过（`pnpm build` 包含 `tsc -b`）。
- [x] 仅修改登录表单与回归测试两个文件，无新增后端接口、依赖或支付操作。
- [x] 所有适用 CI 检查通过；[Code
Quality](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/39757342024)
与
[自动审查](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/39757341928)
成功。Claude / Codex 均给出 APPROVE，无需修改的发现，CodeQL 未处理告警为 0。
- [ ] 合并后部署 staging，再发布新的 Platform 补丁版本。

真实 Google / 邮箱登录及真实付款未在本轮执行。没有创建订单、扣款或修改余额。
```

