---
title: "API 快速入门链接直接指向 ZooWork 域名，不再先闪一下旧地址"
type: "体验优化"
priority: "低"
date: "2026-09-10"
status: "待审核"
channels: "changelog"
---

# API 快速入门链接直接指向 ZooWork 域名，不再先闪一下旧地址

## 核心宣传点

小而具体的打磨：API Keys 页、以及创建密钥后那段引导里的 **API Quickstart 链接，现在直接指向 `https://zoowork.ai/docs/en/get-started/quickstart`**。

之前共享的 Quickstart 地址还留着旧域名，旧地址会返回 301 跳到 ZooWork——于是点开文档时，地址栏会先出现 `zooclaw.ai` 再切成 `zoowork.ai`，多一次请求，还有一下视觉闪现。顺手删掉了「文档迁移前保留旧域名」那条已经过期的注释。文档路径和英文语言设置没变。

## 原始内容

### fix(settings): API 快速入门直接使用 ZooWork 域名 (#3691)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `de1d2bde`
- PR: #3691
- 作者: lynn Zhuang
- 日期: 2026-09-10T09:31:25Z

验证（PR 原文）：确认旧地址返回 301、新地址直接返回 200；更新现有链接断言，修复前 2 个用例失败、修复后 API Keys 的 57 项测试全部通过；`verify-web.sh` 的 TypeScript、目标测试、ESLint 及适用治理检查通过。仅修改前端文档链接，无需调整后端 API 域名或部署配置。

## 备注

发布状态：已合并待发版（尚未包含在 `ecap-v0.19.3-release` 中）。

对外发布注意：优先级低，只进 changelog 即可，不单独做素材。
