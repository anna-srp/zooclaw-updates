---
title: "Skill 加载器隐藏文件过滤范围修正"
type: "Bug Fix"
priority: "低"
date: "2026-04-16"
status: "待审核"
channels: "Discord+changelog"
---
# Skill 加载器隐藏文件过滤范围修正

## 核心宣传点
修复了 Skill 加载器误过滤 skill 目录以外隐藏文件的问题，skill 注册更准确，避免遗漏合法 skill 文件。

## 原始内容
fix(claw-interface): scope skill loader hidden-file filter to skill dir (#839)

SkillRegistry.get_skill_files() 的 __pycache__/隐藏文件过滤范围之前不限于 skill 目录，现已修正为只过滤 skill 目录内的隐藏文件。
