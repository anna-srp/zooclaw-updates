---
title: "用量页面改版为三列概览，订阅管理与取消入口在用量页和账单页都补齐"
type: "Improvement"
priority: "中"
date: "2026-09-29"
status: "待审核"
channels: ""
---

# 用量页面改版为三列概览，订阅管理与取消入口在用量页和账单页都补齐

## 核心宣传点

设置里的用量页面做了整理：剩余积分、充值积分和当前套餐收成三列概览，时间范围控件、统计图表和明细表格统一样式，字体、对比度和深色模式都做了改善；重复的标题和计算资源摘要被移除，原有的积分计算、查询、筛选和分页能力保持不变。订阅管理入口这次统一了：仍然有效的 Stripe 订阅通过客户门户管理和取消，已结束的 Stripe 订阅保留「激活」入口进入购买流程，符合条件的非 Stripe 订阅在用量页和账单页都保留「管理」和「取消」，取消仍走既有确认流程——这同时修掉了此前从套餐选择弹窗移除取消按钮后、账单页没有任何取消入口的问题。套餐展示也调整了：Pro 不再附加套餐后缀，已结束的订阅显示为 Free 并在有数据时展示结束日期，深色 Pro 卡片、购买按钮和间距做了优化。取消确认框改用设计系统的独立弹窗，带标题描述语义、自动聚焦、焦点约束和关闭后焦点恢复，处理中会禁用重复提交并默认聚焦「保留订阅」；「取消 → 续订 → 再次取消」的状态同步问题也一并修复。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## 改动说明

优化设置中的用量页面：将剩余积分、充值积分和当前套餐整理为三列概览，统一时间范围控件、统计图表和明细表格，改善字体、对比度与深色模式。移除重复标题及计算资源摘要，保留原有积分计算、查询、筛选和分页能力。

统一订阅管理入口：仍有效的 Stripe 订阅通过客户门户管理和取消；已结束的 Stripe 订阅保留“激活”入口，进入现有套餐购买流程。符合条件的非 Stripe 订阅在 Usage 与 Billing 均保留“管理”和“取消”，取消仍通过既有确认流程。Billing 页面也复用这套操作，保留非 Stripe 套餐管理按钮，修复从套餐选择弹窗移除取消按钮后，Billing 页面没有取消入口的问题。Apple、旧版 Creem、团队及权限限制沿用现有规则。

调整套餐展示与选择弹窗：Pro 不再附加套餐后缀，已结束订阅显示 Free，并在有数据时展示结束日期；优化深色 Pro 卡片、购买按钮和间距，隐藏侧栏手机入口，移除托管运行时/API 权益文案。

## 本次修复

- 按 [Tim 的确认框评审](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#issuecomment-5886168682)，将取消确认框改为设计系统独立 AlertDialog，提供标题/描述语义、自动聚焦、焦点约束与关闭后焦点恢复；取消成功导致原入口移除时，焦点回到可用的管理操作。
- 取消请求处理中保持确认框打开，禁用重复提交、关闭按钮及 Escape 关闭；默认聚焦“保留订阅”。新增键盘与可访问性测试，覆盖 Tab/Shift+Tab 循环、背景焦点隔离、退出与成功后的焦点恢复。

- 按 [Tim 第二轮评审](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#issuecomment-5885536252) 修复“取消 → 续订 → 再次取消”的状态同步：服务端确认取消后清除本地临时标记，后续续订刷新重新恢复取消入口并移除旧提示；服务端确认前继续保留临时取消保护。
- 新增使用真实订阅 action/lifecycle hooks 的回归测试，覆盖 Usage/Billing 全程不卸载的连续操作，确认第二次取消实际调用接口，并覆盖服务端延迟确认。

- 按 [Tim 的评审](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#issuecomment-5885192183) 恢复已结束 Stripe 订阅的重新购买入口，并在 Usage 页面保留非 Stripe 套餐管理按钮。
- 新增跨组件回归测试，从 Usage/Billing 的激活入口进入真实套餐弹窗，再点击 Resubscribe，确认触发订阅购买；管理与取消分别验证各自回调。

- 合入最新 main，解决用量明细组件冲突，保留游标分页、快照、归属筛选与服务端时间窗口，同时保留界面本地化。
- 补回 Billing 页面的取消确认入口；Stripe 管理及已预约取消后的管理统一进入客户门户。
- 新增默认账单卡片回归测试，覆盖 Card/Antom 的取消入口、保留套餐管理，以及 Stripe 的门户跳转。

## 验证

- 前端治理检查、TypeScript 类型检查及全部改动 TS/TSX 文件的 ESLint 检查通过。
- 7 个相关单元测试文件、87 条用例通过；按 Tim 反馈修复后，相关 59 条用例通过；第二轮状态同步修复后，3 个相关测试文件、62 条用例通过；本轮确认框改动后上述 62 条仍通过，并新增 4 条可访问性用例通过。
- 覆盖用量游标/快照分页、归属筛选、订阅操作、日期回退、套餐弹窗及设置页面回调。
- 未执行真实付款、取消订阅或权益变更；本轮未运行浏览器视觉验证。构建和完整测试由 CI 验证。

## 自动检查与评审说明

最新提交 `593a952f0` 已获得 [Codex review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#pullrequestreview-5349630629) 和 [Claude review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#issuecomment-5886365152)，未发现问题。GitHub CI 已全部通过（不适用检查正常跳过），包括完整前端测试与构建。

此前保留 Usage 非 Stripe 场景“仅取消”的处理已按 Tim 的反馈修正：两处页面均同时保留管理与取消入口。`Free` 继续按原设计文档作为套餐名称展示，结束日期等说明文案仍本地化。

## 范围

仅涉及前端，复用现有账单 API。Free 只是已结束订阅的展示标签，不新增免费权益。取消操作从套餐选择弹窗迁移到 Usage 和 Billing 页面。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `a57dc72e6cc29522525e8584febf598ff53d5037`
- PR: #3895
- 作者：shana-srp
- 日期：2026-09-29T08:24:09Z

### Commit Message

```
feat(billing): 优化用量页面并完善订阅管理入口 (#3895)

## 改动说明


优化设置中的用量页面：将剩余积分、充值积分和当前套餐整理为三列概览，统一时间范围控件、统计图表和明细表格，改善字体、对比度与深色模式。移除重复标题及计算资源摘要，保留原有积分计算、查询、筛选和分页能力。

统一订阅管理入口：仍有效的 Stripe 订阅通过客户门户管理和取消；已结束的 Stripe
订阅保留“激活”入口，进入现有套餐购买流程。符合条件的非 Stripe 订阅在 Usage 与 Billing
均保留“管理”和“取消”，取消仍通过既有确认流程。Billing 页面也复用这套操作，保留非 Stripe
套餐管理按钮，修复从套餐选择弹窗移除取消按钮后，Billing 页面没有取消入口的问题。Apple、旧版
Creem、团队及权限限制沿用现有规则。

调整套餐展示与选择弹窗：Pro 不再附加套餐后缀，已结束订阅显示 Free，并在有数据时展示结束日期；优化深色 Pro
卡片、购买按钮和间距，隐藏侧栏手机入口，移除托管运行时/API 权益文案。

## 本次修复

- 按 [Tim
的确认框评审](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#issuecomment-5886168682)，将取消确认框改为设计系统独立
AlertDialog，提供标题/描述语义、自动聚焦、焦点约束与关闭后焦点恢复；取消成功导致原入口移除时，焦点回到可用的管理操作。
- 取消请求处理中保持确认框打开，禁用重复提交、关闭按钮及 Escape 关闭；默认聚焦“保留订阅”。新增键盘与可访问性测试，覆盖
Tab/Shift+Tab 循环、背景焦点隔离、退出与成功后的焦点恢复。

- 按 [Tim
第二轮评审](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#issuecomment-5885536252)
修复“取消 → 续订 →
再次取消”的状态同步：服务端确认取消后清除本地临时标记，后续续订刷新重新恢复取消入口并移除旧提示；服务端确认前继续保留临时取消保护。
- 新增使用真实订阅 action/lifecycle hooks 的回归测试，覆盖 Usage/Billing
全程不卸载的连续操作，确认第二次取消实际调用接口，并覆盖服务端延迟确认。

- 按 [Tim
的评审](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#issuecomment-5885192183)
恢复已结束 Stripe 订阅的重新购买入口，并在 Usage 页面保留非 Stripe 套餐管理按钮。
- 新增跨组件回归测试，从 Usage/Billing 的激活入口进入真实套餐弹窗，再点击
Resubscribe，确认触发订阅购买；管理与取消分别验证各自回调。

- 合入最新 main，解决用量明细组件冲突，保留游标分页、快照、归属筛选与服务端时间窗口，同时保留界面本地化。
- 补回 Billing 页面的取消确认入口；Stripe 管理及已预约取消后的管理统一进入客户门户。
- 新增默认账单卡片回归测试，覆盖 Card/Antom 的取消入口、保留套餐管理，以及 Stripe 的门户跳转。

## 验证

- 前端治理检查、TypeScript 类型检查及全部改动 TS/TSX 文件的 ESLint 检查通过。
- 7 个相关单元测试文件、87 条用例通过；按 Tim 反馈修复后，相关 59 条用例通过；第二轮状态同步修复后，3 个相关测试文件、62
条用例通过；本轮确认框改动后上述 62 条仍通过，并新增 4 条可访问性用例通过。
- 覆盖用量游标/快照分页、归属筛选、订阅操作、日期回退、套餐弹窗及设置页面回调。
- 未执行真实付款、取消订阅或权益变更；本轮未运行浏览器视觉验证。构建和完整测试由 CI 验证。

## 自动检查与评审说明

最新提交 `593a952f0` 已获得 [Codex
review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#pullrequestreview-5349630629)
和 [Claude
review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#issuecomment-5886365152)，未发现问题。GitHub
CI 已全部通过（不适用检查正常跳过），包括完整前端测试与构建。

此前保留 Usage 非 Stripe 场景“仅取消”的处理已按 Tim 的反馈修正：两处页面均同时保留管理与取消入口。`Free`
继续按原设计文档作为套餐名称展示，结束日期等说明文案仍本地化。

## 范围

仅涉及前端，复用现有账单 API。Free 只是已结束订阅的展示标签，不新增免费权益。取消操作从套餐选择弹窗迁移到 Usage 和
Billing 页面。

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
Co-authored-by: lynn-srp <lynn@srp.one>
```

来源：SerendipityOneInc/ecap-workspace @ a57dc72e，PR #3895，作者 shana-srp。
