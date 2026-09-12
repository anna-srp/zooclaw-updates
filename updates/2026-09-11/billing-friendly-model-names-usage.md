---
title: "账单用量记录不再显示一串模型 ID，改成和模型选择器一样的友好名称"
type: "体验优化"
priority: "中"
date: "2026-09-11"
status: "待审核"
channels: "changelog"
---

# 账单用量记录不再显示一串模型 ID，改成和模型选择器一样的友好名称

## 核心宣传点

翻账单用量记录的时候，之前看到的是原始模型 ID——那种带 provider 前缀、一长串的技术标识符，对不上你在模型选择器里看到的名字。现在两边统一了：用量标签直接从已有的 LiteLLM 模型目录缓存里取显示名称，和模型选择器用的是同一套。

匹配逻辑覆盖了标准模型名和无歧义的 provider 模型别名，包括 Fireworks 和 OpenRouter 那类标识符。遇到未知或者有歧义的模型，回退到用路径最后一段——至少比整串 ID 可读。

需要说明的是底层数据没动：原始模型 ID、积分金额、分组方式和 Compute 标签都保持原样，改的只是展示层。

## 原始内容

### fix(billing): display friendly model names in usage records (#3700)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `1d6bd120`
- PR: #3700
- 作者: sam-srp
- 日期: 2026-09-11

改动要点（PR 原文）：从已有的 LiteLLM 模型目录缓存解析账单用量标签，使用与模型选择器相同的显示名称；匹配标准模型名和无歧义的 provider 模型别名（含 Fireworks 与 OpenRouter 标识符）；未知或有歧义的模型回退到路径最后一段；保留原始模型 ID、积分金额、分组与 Compute 标签；新增别名匹配、标准名优先、歧义处理、安全元数据解析与目录不可用回退的测试覆盖。

验证（PR 原文）：`git diff --check` 通过；提交钩子 Ruff、格式化、Pyright 与导入契约通过；devcontainer 测试未运行（本地 Docker daemon 不可用）；两个本地钩子（importlinter-repo-sync、database-pydantic-returns）因找不到 Python 3.12 在提交时跳过，CI 验证仍为必需；完整 pre-push Ruff 与 import-linter 检查通过。

## 备注

发布状态：已合并待发版（尚未包含在 `ecap-v0.19.5-release` 中）。

对外发布注意：小而实用的可读性改进，进 changelog 即可，不单独做素材。
