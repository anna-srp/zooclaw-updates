---
title: "2026-06-07 无用户可感知更新（GitHub API 授权失效）"
type: "其他公告"
priority: "高"
date: "2026-06-07"
status: "待审核"
channels: ""
---
# 2026-06-07 同步异常说明

## 核心宣传点
今日同步因 GitHub SAML SSO 授权问题未能获取 commits 数据，无用户可感知的产品更新。

## 原始内容
GitHub PAT（anna-srp）对 SerendipityOneInc 组织的 SAML SSO 授权已连续多日失效（自 2026-06-05 起）。
- 错误码：HTTP 403
- 错误信息：Resource protected by organization SAML enforcement
- 修复方式：需 anna-srp 账号持有人访问 https://github.com/settings/tokens，找到对应 PAT，点击 "Grant access" 授权给 SerendipityOneInc 组织

本次同步时间：2026-06-08T01:05:25.694910+00:00
抓取目标日期：2026-06-07
