---
title: "Founder IP Studio 2.0 上线"
type: "Agent 上架/更新"
priority: "高"
date: "2026-05-30"
status: "待审核"
channels: "站内弹窗, 社媒素材, Use Case, Discord, changelog, KOL, EDM"
---

# Founder IP Studio 2.0 上线

## 核心宣传点

全新 Founder IP Studio 2.0 Agent 上线！一站式创始人 IP 视频生产流水线：从业务访谈、脚本策划、数字分身口播视频生成，到字幕烧录、BGM 混音，6 个专业 Skill 全流程协作，帮你高效打造个人 IP 视频内容。

## 原始内容

feat(founder-ip-studio): add founder-ip-studio 2.0.0 agent pack (#155)

End-to-end founder-IP video pipeline: founder-director (topic
selection, viral copy, legal review, character lock), chameleon-bridge
(Seedance avatar speaking video), auto-caption (ASR + forced align),
founder-post (Remotion animated caption burn, BGM mix). Ships an
18-track BGM library and a Remotion project for caption styles.

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Description

## 概述
  - 新增端到端创始人 IP 视频生产流水线 agent 包 (`founder-ip-studio/`, v2.0.0)
  - 内置 6 个 skill:
    - `founder-director` — 创始人 IP 创意总监:业务/故事访谈、IP 方向推荐(含真实参考账号库)、人脸+人声+场景素材采集、选题(agent 推荐/热点/用户想法)、文案生成、内置法务审核与人设守护
    - `chameleon-bridge` — Seedance 2.0 数字分身视频桥接:从 ip-profile.json 读人脸/人声,处理人脸资产注册回退、对口型、相似度校验、分段拼接、多平台裁切
    - `auto-caption` — ASR + 强制对齐,产出词级字幕
    - `founder-post` — 基于 Remotion 的动态字幕烧录、调色、B-roll、BGM 混音后期
    - `pack-onboarding` — 首次使用引导
    - `zooclaw-forcedalign` — 强制对齐底层 skill
  - 配套资源:
    - 18 首专为创始人 IP 视频准备的 BGM 曲库(覆盖极简电子、轻柔钢琴、企业弦乐、温暖吉他、轻快节拍、高级品牌感 6 种风格)
    - Remotion 项目附带 7 套字幕风格 (tiktok-karaoke / editorial-serif / cn-serif / cn-bold / comic-red / podcast-bold)
    - 中英文字体包 (Noto Serif SC, MaShanZheng, Cormorant Garamond, Anton, Montserrat)
  - 集成:Seedance 2.0 (BytePlus/Volcengine)、Nano Banana 2 (Gemini)、zooclaw-asr + qwen3-forced-align、Remotion、ffmpeg
