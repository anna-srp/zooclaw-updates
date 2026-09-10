---
title: "新建 Bot 的默认模型统一切到 GPT-5.6 Terra"
type: "体验优化"
priority: "中"
date: "2026-09-09"
status: "待审核"
channels: "Discord+changelog"
---

# 新建 Bot 的默认模型统一切到 GPT-5.6 Terra

## 核心宣传点

新建 Bot 的默认模型换成 **GPT-5.6 Terra**。之前的改动只覆盖了 V1 套餐的默认值，而「模型目录里哪个标为默认」和「V2 创建入口用哪个」各有一套独立配置，于是同一个产品里冒出三个不一样的默认答案。这次把它们对齐成一个。

对齐后的行为：

- 四个套餐加上未知套餐的 fallback 都用 `gpt-5.6-terra`；V1 创建与配置缺失回填派生为 `openai/gpt-5.6-terra`。
- 模型目录即使把 Claude 列在前面，**标为默认的是 Terra**；保留「默认模型不可用时自动选第一个有权限的模型」这个既有行为。
- V2 主 Agent、以及那些解析不出默认模型的 Pack 安装，会显式传入 Terra（`litellm/gpt-5.6-terra`）。
- `.env.example` 同步了两个设置，防止示例里的 Claude 或空字符串把新的代码默认值盖掉。

**不影响你现有的东西**：已经建好的 V1/V2 Agent、会话里已固定的模型、Pack 里显式指定且可用的模型，全部保持原值。这不是强制迁移，也没有全局隐藏 Claude——只是「你什么都不选时给你哪个」变了。

## 原始内容

### feat(claw-interface): default V1/V2 chat and catalog to terra (#3675)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `72d3a002`
- PR: #3675
- 作者: Chris@ZooClaw
- 日期: 2026-09-09T07:15:35Z
- 配套 PR: zooclaw-engine#1303（已合并，覆盖 Engine primary/PDF 默认值及 wire API 兼容路径）

### 改动

- 四个套餐及未知套餐 fallback 使用 `gpt-5.6-terra`，V1 创建/缺失配置回填派生为 `openai/gpt-5.6-terra`。
- `CHAT_MODEL_DEFAULT_MODEL=gpt-5.6-terra`，目录即使先列 Claude，也将 Terra 标记为默认；保留默认模型不可用时选择首个有权限模型的现有行为。
- `ZOOCLAW_ENGINE_DEFAULT_MODEL=litellm/gpt-5.6-terra`，V2 主 Agent、没有可解析默认模型的 Pack 安装显式传入 Terra；保留有效 Pack 显式选择及部署配置覆盖。
- `.env.example` 同步两个设置。
- 新增发布核查说明：`docs/staging-validation/2026-09-09-default-terra-rollout.md`。

### 验收边界（PR 原文）

已有 V1/V2 Agent、会话固定模型和可用的 Pack 显式模型保持原值。此 PR **不代表存量 Claude 故障已全部解除**，也不全局隐藏 Claude。评论中要求的存量修复、Claude 可用性调整、Auto/子任务/PDF/后台任务核查，已列入发布说明；线上历史数据修复需独立清单、备份、并发保护和回滚，并由人确认执行。V2 Auto 的 Claude Haiku 候选仍是其中一个待核查入口。

### 验证

`pytest -q --no-cov` 748 passed（12 个测试文件，覆盖 plan models、model catalog、V1 client/config、V2 main/install/lifecycle、Agent Builder model/service/routes/runtime、Pack test runtime）；`verify-py.sh` 的 ruff check/format、pyright（0 errors / 0 warnings）、8 项 import-linter 合约全部通过。部署与存量迁移不在单测证据内。

## 备注

发布状态：已上线（已包含在最新 `ecap-*-release` 正式发布中）。

对外发布注意：这是默认值变更，用户侧最直观的感受是「新建的 Bot 现在默认是 Terra」。PR 明确写了本次不代表存量 Claude 问题全部解除、也没有全局隐藏 Claude，对外文案不要引申成「已切换/已弃用 Claude」。
