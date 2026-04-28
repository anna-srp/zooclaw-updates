---
title: "Bot 唤醒期间聊天界面不再空白等待"
type: "体验优化"
priority: "高"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# Bot 唤醒期间聊天界面不再空白等待

## 核心宣传点
Bot 从休眠唤醒时，聊天界面会立刻显示（不再是空白屏），输入框禁用显示等待状态，Bot 就绪后自动解锁，再也不会出现"等了3分钟然后报错"的情况。

## 原始内容
**Commit**: fix(web): decouple chat UI from bot init readiness (ECA-542) (#1388)  
**PR Body**:  
关闭 ECA-542。两个配套修复：把"3分钟空白等待→错误"变成"立刻显示聊天UI+输入禁用→bot唤醒→输入可用"。  
1. 提高 INIT_POLL_TIMEOUT_MS 3分→5分（实测生产环境 bot 唤醒需~210s，之前3分钟预算在 bot 距就绪还剩30s时就触发超时报错）  
2. 将 UI ready 判断与 bot init 轮询解耦——bot 未就绪时显示 chatUI 但锁定输入，提升感知体验。
