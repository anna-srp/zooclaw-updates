---
title: "TVC Studio Agent 更新至 v0.3.5"
type: "Agent 上架/更新"
priority: "中"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# TVC Studio Agent 更新至 v0.3.5

## 核心宣传点
TVC Studio（TVC 广告制作 Agent）更新至 0.3.5 版本：优化了视频首帧策略（强制双图输入提升画面一致性），简化了启动流程（直接进入产品信息收集），提升了整体使用体验。

## 原始内容
**Commit**: feat(tvc-studio): bump to 0.3.5 with new pack layout (#108)  
**PR Body**:  
Update tvc-studio pack from 0.3.1 to 0.3.5。变更摘要：  
- 版本：0.3.1 → 0.3.5；manifest 描述简化为一句话  
- Pack 目录结构迁移（符合标准 pack layout）  
- Seedance first-frame 策略反转：现在强制双图输入（分镜宫格为 --first-frame + 商品多视角 prompt suffix），原先"禁止多宫格首帧 + 默认不传 first-frame"策略反转  
- BOOTSTRAP 欢迎流程重写：跳过双语欢迎，直接收集产品/USP/品牌/平台信息  
- tvc-director SKILL.md (+41 lines)、tvc-post SKILL.md (+10 lines)、chameleon-bridge SKILL.md 更新  
- tvc-post compose.py 和 fetch_bgm.py 更新  
- 新增 Avatar 字段和 description.json（发布列表制品）
