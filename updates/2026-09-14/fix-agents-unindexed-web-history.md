---
title: "修复：Agent 历史会话列表只剩三条，大量 Web 老对话读不出来"
type: "Bug Fix"
priority: "高"
date: "2026-09-14"
status: "待审核"
channels: "changelog"
---

# 修复：Agent 历史会话列表只剩三条，大量 Web 老对话读不出来

## 核心宣传点

这是个"数据看起来没了"的问题，体感很差。反馈的那个 staging Agent 实际上有 12 条非空 Web 会话加 1 条飞书会话，但历史列表里只显示 3 条 Web 会话和飞书那条——剩下 9 条既看不见也打不开，用户会以为自己的对话记录丢了。

根因是上一轮兼容性修复只给「Engine 返回的会话」做了信息补全，而那 9 条原始 Web thread 从来没进入候选集合，自然补不到。更麻烦的是去重：有一个规范 Engine ID 还额外挂着一条空的别名 thread，光靠 ID 没法正确去重。

这次的修法是在做产品分页之前就把用户自己拥有的原始 thread 索引合并进来，保留已保存的标题，并对原始根 thread 和规范 Engine ID 双向去重。没有 Engine session 索引的那些 thread 现在能打开了，展示的是它们原本完整的富文本历史，以只读方式呈现。

**安全边界写得比较明确**：读取或选中这些历史不会创建 session/thread、不会绑定 ACS、不会重放入站消息、也不会启动 Agent。直接读取遗留数据会强制校验归属、归档状态和用途边界。配套的 Engine 改动带来了删除元数据，已删除的会话不会再通过 Mongo 兜底路径复活；ECAP 要求 Engine 显式确认支持该能力，如果 Engine 是旧版本就维持原有列表、不启用不安全兜底。访问凭证刷新失败时会立即停止暴露缓存的原始 thread 引用。

老客户端仍然保留文本历史接口，HTTP 校验接受它那套有界的原始 thread 续传游标，同时保留原有的 Engine 事件游标格式和条数限制。

## 原始内容

### fix(agents): restore unindexed web conversation history (#3722)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `281719bd`
- PR: #3722
- 作者: kaka-srp
- 日期: 2026-09-14

验证（PR 原文）：后端静态/类型/导入检查，以及 92 项针对 task、history 和 HTTP 路由的测试通过。遗留历史回归测试跟着服务端真实下发的游标走了三次 HTTP 请求，校验原文、附件，以及对跨 session、格式错误、超长游标的拒绝。前端 16 项针对性测试和静态/类型/lint 守卫通过；全量前端跑了 5820 项，仅有一处与本次无关的 Markdown hydration 时序失败，该文件单独重跑 51 项全通过。候选代码在真实 staging 加密 Mongo 和原始 Mattermost thread 上验证：12 条 Web 加 1 条飞书，9 条缺失的标题/正文全部可读，两条一页的分页下共 13 个唯一条目。

依赖：需要先部署 Engine 侧 PR zooclaw-engine#1435。

## 备注

发布状态：已合并待发版（尚未包含在任何 `ecap-*-release` tag 中）。

⚠️ 对外发布注意：本修复依赖 Engine #1435 先行部署，Engine 未升级时 ECAP 会维持旧列表行为，用户侧看不到变化。建议等前后端都上线并完成验收后再对外宣传。
