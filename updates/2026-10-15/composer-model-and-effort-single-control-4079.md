---
title: "体验优化：输入框里模型和思考强度合成一个选择器，少点一次菜单"
type: "体验优化"
priority: "中"
date: "2026-10-15"
status: "待审核"
channels: ""
---

# 体验优化：输入框里模型和思考强度合成一个选择器，少点一次菜单

## 核心宣传点

聊天输入框原本把模型和思考强度做成两个独立控件，现在合并为一个紧凑控件：一个下拉箭头、一行浅色的强度标签。菜单里仍保留模型搜索和「常用/更多模型」分组，模型专属的思考强度选项排在列表下方，「模型默认」与「跟随 Agent」两个动作仍然分开。控件会显示当前运行时默认值（包含继承来的原生覆盖），而显式创建的 Task 草稿则使用自己的模型默认值。即使模型列表加载失败或为空，合并后的选择器也会给出恢复入口，老的选择器调用方仍保持搜索粘性。

## 分级

- 内部：P2
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `a8f86c12f57b8f1b0bb2270471bb6aed5de15dc3`
- PR: #4079
- 作者：kaka-srp
- 日期：2026-10-15T04:00:21Z

### Commit Message

```
fix(chat): combine model and thinking effort controls (#4079)

## Summary
- Combine model and thinking effort into one compact composer control,
with a muted effort label and one dropdown arrow.
- Keep model search and common/more models in the same menu; put
model-specific effort choices below the list and retain distinct Model
default and Follow Agent actions.
- Display the current runtime default, including inherited native
overrides, while explicit Task drafts use their own model default.

## Root cause
The composer rendered model and effort as two independent controls. The
combined picker now exposes recovery actions even when the model catalog
fails or is empty, and preserves sticky search for existing picker
consumers.

## Test plan
- App and shared chat-ui TypeScript/ESLint; frontend governance guards.
- 106 targeted app tests (composer, Task model, launcher and runtime
model query), plus 38 shared model picker tests; the affected suite was
rerun after correcting its fixed-Task fixture.
- Real staging-backed browser checks: effort save and reload, Model
default, Follow Agent, Chinese/dark theme and 390px viewport.
- Real Agent Settings menu: scrolling 100px preserves the search input
position.
- Astra local review: fixed two P2 findings (recovery actions and actual
default labels) and one P3 finding (sticky search); targeted re-review
confirmed all three addressed.

Related issue: #4073. This PR covers the agreed Agent/Web scope; iOS and
Schedule configuration/UI were excluded from this iteration.
```

