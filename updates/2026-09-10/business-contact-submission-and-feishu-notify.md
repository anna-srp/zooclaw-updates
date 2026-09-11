---
title: "企业官网的联系表单终于真的能收到线索了：提交落库 + 飞书机器人实时通知"
type: "产品基础功能更新"
priority: "高"
date: "2026-09-10"
status: "待审核"
channels: "Discord+changelog"
---

# 企业官网的联系表单终于真的能收到线索了：提交落库 + 飞书机器人实时通知

## 核心宣传点

9 月 8 日上线的企业官网页 `/business` 有个相当致命的问题：**联系表单提交后显示成功，但线索根本没送出去**——纯前端假成功。今天两条 PR 一起把这条链路补齐。

第一步，提交真的走后端了。表单改为提交到免鉴权的 `POST /business/contact`，**只有后端确认收到才显示成功**，中间的 pending / error 状态也都在表单组件里如实呈现。邮箱做 Pydantic 显式校验，service 字段接受自由文本（直接用现有下拉框的文案，不引入 service 枚举和映射层）。被接受的提交以单行 JSON 记到 `business_contact_submitted` 日志。前端 auth 中间件只放通这一个匹配的 POST，仍复用现有的 claw 代理。

第二步，有人提交会立刻在飞书里响。记完日志后，可选地向飞书机器人发一条可读消息，带上来源 `zoowork-business`、邮箱和咨询服务。走 `aiohttp` 后台任务、5 秒超时，**通知失败不会导致提交失败，也不会把 webhook 打进日志**。

## 配置与部署要点

- 新增环境变量 `BUSINESS_CONTACT_FEISHU_WEBHOOK_URL`，默认空；**不配则跳过通知**，功能自动降级为「只落日志」。
- 生产需在 Vault KV `srp/ecap/claw-interface/env` 配置该 webhook 并滚动后端加载，webhook 本身不入代码库。
- 部署顺序：**先后端，再前端**。通知能力只需后端部署，无需前端发布。
- 目前联系人信息**只记录在应用日志里**，没有进 CRM 或数据库表。

## 原始内容

### feat(business): record public sales contact submissions (#3696)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `029923ff`
- PR: #3696
- 作者: tim-srp
- 日期: 2026-09-10T13:45:02Z

The Business contact form previously showed success without delivering the lead. It now submits to an unauthenticated `POST /business/contact` endpoint and shows success only after the backend acknowledges the request. Validate email and accept a free-form service string using explicit Pydantic request/response schemas; log accepted submissions as single-line JSON under `business_contact_submitted`. Allow only the matching POST through the frontend auth middleware and reuse the existing claw proxy. Contact details are recorded in application logs only. Deploy the backend before the frontend.

验证：后端端点测试 24 passed（匿名访问、自由文本 service、非法输入拒绝、单行 JSON 日志、OpenAPI schema）；前端 140 passed（提交生命周期、本地化、导航、中间件范围、代理）；后端 ruff / 格式化 / pyright / import-linter 通过；前端 TypeScript、改动文件 ESLint、治理检查通过。

### feat(business): notify Feishu after contact submissions (#3697)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `673ee3d8`
- PR: #3697
- 作者: tim-srp
- 日期: 2026-09-10T14:08:58Z

After logging a business contact submission, optionally send a readable Feishu bot message containing source `zoowork-business`, email, and service. The existing frontend and API payload stay unchanged. Add `BUSINESS_CONTACT_FEISHU_WEBHOOK_URL`, defaulting to empty; skip notification when unset. Send plain text with `aiohttp` in a background task with a 5-second timeout. Notification failures do not fail the submission or expose the webhook in logs.

验证：34 项针对性后端测试通过，含通知关闭、消息内容、非法输入、超时、传输失败、机器人拒绝；Ruff、格式化、pyright、import-linter、`git diff --check` 通过。

## 备注

发布状态：两条均为已合并待发版（`ecap-v0.19.3-release` 于 2026-09-10T13:59Z 发布，两条 PR 合并于其后）。

对外发布注意：这条本质是修一个「表单假成功」的问题，对外讲的时候不建议强调此前线索丢失，落点放在「企业咨询已可正常受理」更合适。内部则要提醒销售：**上线前必须确认 Vault 里已配好 webhook**，否则仍然只有日志。
