---
title: "修复：企业咨询表单邮箱输入框字号与服务选择器不一致"
type: "Bug Fix"
priority: "低"
date: "2026-09-22"
status: "待审核"
channels: ""
---

# 修复：企业咨询表单邮箱输入框字号与服务选择器不一致

## 核心宣传点

企业咨询表单里的邮箱输入框沿用了共享 Input 组件的 14px 桌面端字号，而旁边的服务类型选择器是 16px，两个控件看起来一高一低不整齐。现在邮箱字段在桌面端固定 16px，两个控件字号对齐；桌面和移动端都已确认。

## 分级

- 内部：P2
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

The Enterprise contact form's email input inherited a 14px desktop font
from the shared Input, while the service selector used 16px. Keep the
email field at 16px on desktop so both controls match.

Validation:
- Web governance checks, TypeScript, and scoped ESLint passed.
- All 5 existing business contact form tests passed.
- Browser verification confirmed both controls render at 16px on desktop
and mobile.

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `c09cf9568a6cd5e76fd7aa8d2354ff30dcc19051`
- PR: #3841
- 作者：shana-srp
- 日期：2026-09-22T05:56:56Z

### Commit Message

```
fix(enterprise): align contact form field font sizes (#3841)

The Enterprise contact form's email input inherited a 14px desktop font
from the shared Input, while the service selector used 16px. Keep the
email field at 16px on desktop so both controls match.

Validation:
- Web governance checks, TypeScript, and scoped ESLint passed.
- All 5 existing business contact form tests passed.
- Browser verification confirmed both controls render at 16px on desktop
and mobile.

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

来源：SerendipityOneInc/ecap-workspace @ c09cf956，PR #3841，作者 shana-srp。
