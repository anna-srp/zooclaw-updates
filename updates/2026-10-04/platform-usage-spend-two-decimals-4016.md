---
title: "修复：开发者平台 Usage 页的消费金额统一保留两位小数，明细不再显示一长串小数位"
type: "Bug Fix"
priority: "中"
date: "2026-10-04"
status: "待审核"
channels: ""
---

# 修复：开发者平台 Usage 页的消费金额统一保留两位小数，明细不再显示一长串小数位

## 核心宣传点

开发者平台 Usage → Activity 里的 Spend 明细以前最多会显示到六位小数，总额却固定两位，看起来像两套口径，一列 $0.01123、$0.127756 这样的数字也很难快速比对。现在明细和总额共用同一个格式化规则，全部四舍五入到两位小数：$0.01123 显示成 $0.01、$0.127756 显示成 $0.13，极小的金额按同一规则显示为 $0.00。

这次只改展示：原始 credits 记录、服务端汇总、实际扣费和分页逻辑都没有变化，也不涉及后端或按时间 / Session 的聚合方式。Load more 和 Refresh 行为不变，手机窄屏下金额列也不会把页面撑出横向滚动。

## 分级

- 内部：P2
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `22d17ae272264d05cc711af4a18e400339464b35`
- PR: #4016
- 作者：david-srp
- 日期：2026-10-04T05:12:04Z

### Commit Message

```
fix(platform): Usage 金额统一保留两位小数 (#4016)

## Summary

- Platform → Usage → Activity 的 Spend 明细统一四舍五入到两位小数，例如 `$0.01123 →
$0.01`、`$0.127756 → $0.13`；极小金额按同一规则显示为 `$0.00`。
- Total spend 和明细共用 `formatUsageSpend`，总额保持现有的两位小数展示。原始
credits、服务端汇总、扣费和分页逻辑不变，不涉及后端或时间/Session 聚合。

## Root cause

总额与明细此前使用不同的格式化入口：总额固定两位小数，明细最多保留六位。此次统一展示规则，并移除不再需要的独立总额格式化函数。

## Test plan

- [x] `pnpm exec vitest run src/routes/usage.test.tsx`：11/11
通过；同步现有测试的明细金额预期。
- [x] `pnpm typecheck`、`pnpm lint`、`git diff --check` 通过。
- [x] 本地示例数据预览：桌面与 390px 手机视口的金额均为两位小数；Load more、Refresh 正常，手机页面无整体横向溢出。
- [x] 浏览器核对截图中的八个金额示例，以及零值和极小金额的显示。
```

来源：SerendipityOneInc/ecap-workspace @ 22d17ae2，PR #4016，作者 david-srp。
