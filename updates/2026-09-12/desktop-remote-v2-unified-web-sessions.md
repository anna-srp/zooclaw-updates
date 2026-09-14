---
title: "Desktop 远程会话与 Web 打通：统一会话列表、历史记录和模型选择"
type: "新功能上线"
priority: "中"
date: "2026-09-12"
status: "待审核"
channels: "changelog"
---

# Desktop 远程会话与 Web 打通：统一会话列表、历史记录和模型选择

## 核心宣传点

Desktop 的 Remote V2 之前是一套"平行世界"——它会自己创建互不相干的 Engine session，导致桌面端看到的会话列表、历史记录和 Web 端对不上。这次把它接回了 Web/Mattermost 那条规范链路：会话列表和历史记录以 Web 为准，ACP 提示词通过 Mattermost/ACS 发送，而不再另起 Engine session。

**体验对齐 Web**。乐观发送反馈、表情回应 UI、模型选择和 Agent 筛选都复用 Web 的实现。模型目录 34 条和选择器菜单与 Web 完全一致。本地 ACP Agent 的行为保持原样，暂不支持的附件仍然是禁用状态。

**跨端可见**。Web 能显示 Desktop 发出的消息和回答；在 Web 里追问，回复也会实时出现在 Desktop 上。

**Desktop 来源标识**。新增了带版本号的 Desktop 来源元数据，配合 ACS 侧的 PR #121。这个元数据只用于上下文标注，明确不作为授权凭证或设备路由凭证——Claw Interface 会校验字段、版本、client 名称，以及一段非空、无 NUL、合法 UTF-8 且不超过 4096 字节的上下文，校验不过直接返回 invalid-params。没有来源上下文时不会发送来源属性，ACS 也不会注入任何兜底文案。来源上下文不会渲染进 Mattermost 消息正文。

**打包运行时**。通过 Git LFS 更新了打包的 DSH 运行时，暴露了 Desktop 工具命名，并修复了打包 web staging manifest。

## 已知未闭环问题（重要）

PR 原文明确列出了几个尚未修复的时序问题，作者要求在裁定/修复前不要合并：

- 同一个会话里 Desktop 和 Web 并发提问时，较早的那条可能被错误标记为"Completed without a visible response"。根因是共享的 Web 状态辅助函数把可见回复关联到最近的前一条用户消息，而不是显式的 run 身份。
- 迟到的 `assistant_phase=preview` 消息可能在同一 run 的最终片段和终止标记之后到达，产生重复的可见回答。
- 作者说明这两个问题都不代表 Engine 回答缺失或 MCP 桥接失败——真实 Engine 历史和 Mattermost 里都有最终结果，只是前端展示顺序出了问题。
- 本次 staging 验收未覆盖：本地 Codex/Claude 实时会话、表情回应持久化，以及超过 30 秒的长提示。

## 原始内容

### feat(desktop): unify remote v2 cloud sessions and desktop source (#3701)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `54809790`
- PR: #3701
- 作者: zayne-srp（Co-authored-by: kaka-srp）
- 日期: 2026-09-12
- 规模: 68 个文件，+2858 / -397

验证（PR 原文）：本地跑了针对性的前端和 Desktop 测试，后端 ACP 测试、Ruff 与导入边界检查通过。合成 ACS 验收确认了最终 Engine 输入、Web 追问不受影响、session 身份和重复抑制，但未调用真实模型。Staging 部署成功：Claw Interface `service-v0.18.3-beta.desktop-source.1`、Web `ecap-v0.19.4-beta`、ACS `v0.1.14-beta.desktop-source.1`；从 b7beaed8a 重新打包 arm64 App 并本地安装，未使用 dev server。真实打包 App → staging → Engine 验证了 Desktop 来源上下文，Desktop MCP 读取通过 `mcp__acp-desktop-tools__read` 取到本地哨兵值，Engine 历史包含正确的工具结果和最终回答。新增身份维度的 Remote V2 缓存回归测试，17 项会话测试通过，本地 ACP key 和前缀失效逻辑保留。另有 4 项真实 relay/WebSocket 测试、54 项针对性后端测试、Desktop typecheck、Ruff/Pyright/导入契约通过。

部署要求（PR 原文）：需要与 ACS #121 一起，用 staging beta tag 同时部署 Claw Interface 和 Web；未请求生产部署。Desktop App 需要用新的 relay header 重新打包，来源元数据才会生效。部署顺序为 ACS → Claw Interface → 更新后的 Desktop。运行时 manifest 记录的是 dirty DSH 源码哈希，属于 beta 产物，不是干净的上游 DSH 发布版本。

## 备注

发布状态：已合并待发版（当前为 main HEAD，尚未包含在任何发布 tag 中）。

⚠️ 对外发布注意：PR 正文明确要求"Keep PR unmerged pending adjudication/repair of these ordering issues"，但该 commit 实际已于 2026-09-12 04:27 合入 main。对外发文前建议先与作者确认上述两个时序问题是否已另行修复，否则不宜作为"已完成"能力宣传。另外本功能依赖 ACS #121 与重新打包的 Desktop App，未部署齐全时用户侧不可感知。
