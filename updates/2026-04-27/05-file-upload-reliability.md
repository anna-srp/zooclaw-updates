---
title: "文件上传稳定性提升（减少间歇性失败）"
type: "Bug Fix"
priority: "高"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# 文件上传稳定性提升（减少间歇性失败）

## 核心宣传点
修复了部分用户遇到的文件上传间歇性失败问题，上传成功率更高，失败后会自动重试，不再需要手动重新上传。

## 原始内容
**Commit**: fix(web): harden MM file upload — auth detection, retry, concurrent guard (#1380)  
**PR Body**:  
修复用户间歇性文件上传失败（Sentry 15 events，2 users）。根因：快速连续上传时首个成功(201)但第二个报 TypeError: Failed to fetch —— im.ecap.gsmo.ai 的间歇性 CORS/网络拒绝，加上无错误恢复和无并发保护。  
变更：A. Auth expiry 检测（uploadFile 捕获 TypeError 时探测 token 有效性）；B. 失败自动重试；C. 并发上传保护（防止多个并发上传互相干扰）。
