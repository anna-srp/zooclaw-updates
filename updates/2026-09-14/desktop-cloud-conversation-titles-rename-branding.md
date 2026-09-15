---
title: "Desktop 云端会话终于有名字了，还能重命名；桌面端 ZooWork 品牌切换完成"
type: "新功能上线"
priority: "中"
date: "2026-09-14"
status: "待审核"
channels: "changelog"
---

# Desktop 云端会话终于有名字了，还能重命名；桌面端 ZooWork 品牌切换完成

## 核心宣传点

Desktop 的 Remote V2 云端会话之前一律是"无标题"状态，而且没法改名。这次补齐了：新会话的标题会从第一条消息生成（走的是已有的 Web 创建接口），标题就绪后自动刷新对应工作区；重命名也接到了已有的云端接口上，缓存更新按 workspace / target 精确作用域。本地 Codex / Claude 的行为保持原样。

**品牌切换收尾**。窗口标题、托盘、helper 进程、Agent 描述、错误文案和安装包产品名统一改成 ZooWork，并直接复用 Web 的品牌素材，而不是在过时的 Desktop 图片上再叠一层。兼容性做了保护：app ID、用户数据目录、URL scheme 和环境变量名全部保持不变，所以升级不会丢配置和登录态。

**范围与注意事项（PR 原文）**：不涉及 Claw Interface、ACS、Engine 或 DSH 运行时的 API 变更。已知的"自动标题 vs 手动重命名"竞态问题明确不在本次范围内。已存在的无标题会话不会批量回填标题。macOS 升级后使用 ZooWork.app，旧的 ZooClaw.app bundle 需要另外手动删除，注意不要连应用数据一起删掉。

## 原始内容

### fix(desktop): sync cloud conversation titles and rename (#3717)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `8bf6ad5a`
- PR: #3717
- 作者: zayne-srp
- 日期: 2026-09-14

验证（PR 原文）：Desktop 52 项测试通过，1 项可选 Codex 集成测试跳过，TypeScript 通过。最新一次品牌 + 标题合并构建：23 项针对性前端测试通过，生产构建成功。推送时的 TypeScript、ESLint 和改动面检查通过。本地构建并临时签名了 ZooWork.app，在 staging 上安装启动，UI、保留的登录/会话列表、Desktop 桥接和签名校验均通过。

⚠️ 分发状态（PR 原文）：此前用 Developer ID 签名并公证过的 DMG 只包含标题修复，【不】包含后续的品牌更新，且尚未重新构建；本地这个 ZooWork.app 不是新公证的分发版 DMG。

## 备注

发布状态：已合并待发版（尚未包含在任何 `ecap-*-release` tag 中）。

⚠️ 对外发布注意：桌面端需要重新打包、签名并公证 DMG 才能让用户拿到这次改动，在此之前不要对外宣称 Desktop 已完成 ZooWork 品牌切换。另外"自动标题与手动重命名竞态"仍未解决，宣传重命名功能时不宜承诺该场景。
