---
title: "Motion Video 更新 0.2.3：视频制作能力随包内置，装完即可用"
type: "Agent 上架/更新"
priority: "高"
date: "2026-08-14"
status: "待审核"
channels: ""
---

## 核心宣传点

此前安装 Motion Video 后核心的视频制作流水线常常缺失、做不出片；0.2.3 把整套 vibe-product-intro 制作能力打包进 Agent，更新后开箱即用。

## 原始内容

Agent Pack 更新：motion-video（Motion Video）
版本：0.2.2 → 0.2.3
submission 变更，来源 ZooClaw Pack Store 接口管道

关键改动：
- agent-pack.yaml：skills 列表新增 `vibe-product-intro`（HyperFrames 视频制作流水线，含 scripts/transcribe.py、scripts/bgm-loop.sh）；
  同时从 dependencies.external_skills 中移除 `vibe-product-intro`。
  原注释说明：该 skill 此前只存在于 builder workspace、从未进入平台 skill 库，因此平台安装必然缺失。
- 新增文件（.agents/skills/vibe-product-intro/ 完整目录）：SKILL.md、references/（hyperframes-contract.md、dependencies.md 等）、
  scripts/（build.mjs、build-timeline.mjs、kit.mjs、theme.template.mjs、bgm-loop.sh、transcribe.py）、templates/（DESIGN.md、STORYBOARD.md）、artifacts/avatar.png
- AGENTS.md：改写关于 vibe-product-intro 缺失的话术——从「它是外部依赖 skill，平台会自动安装」改为
  「自 0.2.3 起随包内置，无需单独安装；早期版本安装时可能没带上，更新到最新版即可」。

能力影响：安装 Motion Video 后即可完整走完 时间轴+词级同步 → 设计系统 → HTML+GSAP 场景搭建 → QC → 60fps 渲染 → BGM 混音发布 全流程，
不再依赖平台侧未上架的外部 skill。

