---
title: "连接器 Skill 现在能准确识别社交平台操作请求"
type: "Bug Fix"
priority: "中"
date: "2026-05-28"
status: "待审核"
channels: ""
---

# 连接器 Skill 现在能准确识别社交平台操作请求

## 核心宣传点

当你让 ZooClaw 帮你操作 LinkedIn、X/Twitter、Instagram 等社交账号时，系统现在能正确调用连接器功能，而不是被通用网页访问工具拦截。

## 原始内容

fix(connectors): rewrite description so social/login-site requests trigger the skill (#207)

* fix(connectors): rewrite description so social/login-site requests trigger the skill

zooclaw-connectors under-triggered for social / login-required services (LinkedIn, Reddit, X). Root cause: the generic web-access skill intercepts these — its description claims "社交媒体 / 需登录网站 / 操作网页", and the old connector description neither named those platforms nor asserted any precedence, so web-access won the tri

PR #207 Body:
原先的问题：连接器 skill 对「操作我自己的社交 / 消费类账号」这类请求不容易被触发。典型问题是 LinkedIn。原描述把自己框定为 "external SaaS account"，且只罗列了 B2B 工作工具（GitHub/Slack/Notion/Jira/Asana/HubSpot），完全没点名 LinkedIn、X、Instagram 等社交/消费平台。
修改：显式点名社交/消费平台（LinkedIn、X/Twitter、Instagram、Facebook、Twitch），与工作类工具并列。对照线上 Connectors 设置页，补齐此前漏写的真实连接器（Confluence、Instagram、Facebook、Twitch）。
