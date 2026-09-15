---
title: "修复：a.zoowork.ai 上的产物链接不出预览"
type: "Bug Fix"
priority: "高"
date: "2026-09-14"
status: "待审核"
channels: "changelog"
---

# 修复：a.zoowork.ai 上的产物链接不出预览

## 核心宣传点

Agent 在聊天里发回来的产物链接点了没反应、侧边栏不出预览、文件卡片也不渲染——这个问题出在品牌迁移的收尾没做干净。

产物预览、文件卡片提取和已发布产物引用解析这三件事，背后共用同一份域名白名单 `STABLE_ARTIFACT_HOSTS`。ZooWork 品牌切换之后，生产环境 V2 的产物域名已经搬到了 `a.zoowork.ai`,但白名单里还只写着 `a.zooclaw.ai`,于是新域名上的 URL 被直接判为非法，什么都渲染不出来。这次把 `a.zoowork.ai` 加进白名单，原有四个域名全部保留。

改动只涉及 Web 前端，没有触碰 `services/`、`desktop/` 或 `ios/`。

**遗留问题（PR 原文已标注）**：V1 的旧域名选择逻辑（`WorkspaceShared.tsx` 和 claw-interface 侧的 `artifact_url.py`）仍然在按"域名里是否包含 zooclaw"来分支判断，所以在 `zoowork.ai` 上会落到 staging 域名去。这部分不在本次范围内，需要另外跟进。

## 原始内容

### fix(chat): allow a.zoowork.ai artifact host for previews (#3721)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `16b98364`
- PR: #3721
- 作者: bill-srp
- 日期: 2026-09-14

验证（PR 原文）：按 TDD 先加 `a.zoowork.ai` 断言确认失败，再加域名确认转绿。在 `web/app` 下跑 vitest 针对 artifacts 与 published-artifact 用例:10 个文件、126 项测试通过。Staging/生产冒烟测试尚未完成——需要打开一条带 `https://a.zoowork.ai/...` 产物链接的聊天消息，确认预览侧栏和文件卡片能正常渲染。

## 备注

发布状态：已合并待发版（尚未包含在任何 `ecap-*-release` tag 中）。

⚠️ 对外发布注意：PR 自述的 staging/生产冒烟验证还是未勾选状态，且 V1 旧域名分支逻辑仍未修。对外说"产物预览已修复"之前，建议先确认 V2 链路冒烟通过，并说明 V1 路径可能仍有问题。
