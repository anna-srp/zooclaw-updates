---
title: "飞书多维表格 Skill 升级 1.1：Agent 不只能读表，现在能写记录了"
type: "Skill 上架/更新"
priority: "中"
date: "2026-09-07"
status: "待审核"
channels: "Discord+changelog"
---

# 飞书多维表格 Skill 升级 1.1：Agent 不只能读表，现在能写记录了

## 核心宣传点

上周刚接进来的飞书多维表格（Bitable）技能只能读——把链接丢给 Agent，它能解析表格、看字段、按分页把记录读出来，但改不了任何东西。这次 `feishu-bitable` 技能升到 1.1，把「写」这一半补上了：`create_record`（新建一行）和 `update_record`（改某一行）正式成为当前可用的写入面。也就是说，你可以直接说「把这几条线索录进这张表」「把第 3 行的状态改成已完成」，Agent 会自己解析链接、找到表、按字段类型拼好值再写进去。

写入这件事比读更容易翻车，所以这一版技能里额外补了几类实操指引：

- **字段格式**：不同字段类型要求的值形状完全不同（文本是字符串、日期是毫秒时间戳、单选是选项名、人员要 `ou_` 开头的 ID、超链接是 `{text, link}` 对象），技能里把这套对照写清楚了，避免 Agent 拿错格式反复失败。
- **分页**：读取和去重时按游标翻页，不再靠猜。
- **写后校验**：写完回读一次确认，而不是「接口没报错就当成功了」。
- **结果不明时的安全处理**：如果一次写入的结果无法确定（超时、响应异常），技能要求 Agent 停下来说明情况，而不是盲目重试制造重复记录。

需要说明的是，**新建多维表格应用、新建字段这两件事仍然不在这一版里**，技能文档里明确标注为后续阶段——目前能操作的是「已有表的记录」。

这次是技能层的配套改动，依赖的 Engine 侧执行能力已先行合并；技能通过 ClawHub 独立分发，会在 Engine 变更部署到位后推上去。

## 原始内容

- 仓库: SerendipityOneInc/ecap-skills
- SHA: `8a5aac4e`
- PR: #277
- 日期: 2026-09-07

### Commit Message

```
feat(feishu): enable Bitable record-write guidance (#277)

## Summary

- update the `feishu-bitable` skill to version 1.1 for native record writes
- document `create_record` and `update_record` as the current write surface
- keep app and field creation explicitly marked as a later phase
- add field-shape, pagination, write verification, and unknown-outcome safety guidance

## Context

This is the skill-layer companion to SerendipityOneInc/zooclaw-engine#1245.
The ACS executor dependency is already merged in SerendipityOneInc/agent-channel-service#107.

## Validation

- `python3 .github/scripts/lint_skills.py` — passed with 12 unrelated existing warnings
- `git diff --check origin/main...HEAD`

## Rollout

Publish to staging after the Engine change is deployed, refresh the test Agent
configuration, and run a one-record create/read/update/read E2E before production promotion.
```

## 备注

发布状态：未知/需确认（回扫脚本判定）。Skill 走 ClawHub 独立分发，仓库 release tag 不适用，且本次依赖 Engine 侧改动先部署；PR 自述的 rollout 要求先上 staging 跑通「建一条 → 读 → 改 → 再读」的 E2E 才推生产。
