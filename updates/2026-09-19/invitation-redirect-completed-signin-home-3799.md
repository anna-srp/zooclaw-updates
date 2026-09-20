---
title: "fix(invitation): redirect completed sign-in to home (#3799)"
type: "Bug Fix"
priority: "中"
date: "2026-09-19"
status: "待审核"
channels: ""
---

# 修复：邀请链接登录完成后进入首页，不再直接掉进聊天

## 核心宣传点

通过邀请链接注册或登录的用户，完成之后会被送到对应语言的首页（Home），而不是像以前那样直接跳进 Chat 并触发一次聊天初始化。如果链接里本来带了明确的 return_to 目标，老用户仍然按那个目标跳转，注册成功后的短暂延时提示也保持原样。对新用户来说，第一眼看到的是完整的产品首页入口，而不是一个空对话框。

## 分级

- 内部：P2
- 外部：B
- 发布状态：已上线（等效修复已随 ecap-v0.19.16-release 的生产 hotfix 发布；本条 main 分支提交本身为后续 backport，尚未进入新的 release tag）

## PR 说明

## Summary
- Route invitation registration completion and existing-user sign-in without a return target to the locale-aware Home page instead of Chat.
- Preserve existing-user explicit `return_to` navigation and the existing registration success delay.

## Root cause
The invitation flow defaulted to `/chat`, sending users directly into chat initialization instead of the intended `/home` entry point.

## Test plan
- `bash scripts/verify-web.sh 'src/app/[locale]/invitation/login/useBossclawLoginFlow.ts' tests/unit/bossclaw/bossclaw-login-flow.unit.spec.ts`
- All 20 login-flow tests pass, including new-user completion, existing-user sign-in, and explicit return targets.
- TypeScript, ESLint, and frontend governance checks pass.

## Review assessment
The automated review flags new-user completion ignoring `return_to`. The base implementation already unconditionally navigated new users to `/${locale}/chat`; this PR only changes that destination to `/${locale}/home`, as requested. New-user return-target semantics are pre-existing and remain outside this narrow redirect change. Existing-user explicit return targets remain unchanged and covered by tests.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `140a3590ddb94ef7be880d3d3d8124d936273f45`
- PR: #3799
- 作者：tim-srp
- 日期：2026-09-19

### Commit Message

```
fix(invitation): redirect completed sign-in to home (#3799)
```

## 备注

PR 描述标注本条为「Draft for a later main backport」，生产 hotfix 由 #3800 基于 `ecap-v0.19.15-release` 单独发出，并以 `ecap-v0.19.16-release`（源 commit `ef6d5fb9d`）发布。因此用户侧行为已经生效；本条 main 提交是回合并，release tag 判定脚本仍显示「已合并待发版」，属预期。

来源：SerendipityOneInc/ecap-workspace @ 140a3590，PR #3799，作者 tim-srp。
