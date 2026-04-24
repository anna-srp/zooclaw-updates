---
title: "podcast-pal PDF 生成切换为平台内置 pdf skill"
type: "Skill 上架/更新"
priority: "低"
date: "2026-04-16"
status: "待审核"
channels: "站内弹窗+Use Case+Discord+changelog"
---
# podcast-pal PDF 生成切换为平台内置 pdf skill

## 核心宣传点
podcast-pal 的 PDF 输出不再依赖本地 LaTeX 环境，改用平台内置 pdf skill，在任何环境下都能稳定生成播客摘要文档。

## 原始内容
feat(podcast-pal): replace xelatex PDF pipeline with platform pdf skill (#80)

移除了 podcast-pal 里所有 LaTeX/xelatex 相关机制，改用平台内置的 pdf skill 生成 PDF 输出。同时更新了 README、示例对话和技能引用，确保文档和行为一致。
