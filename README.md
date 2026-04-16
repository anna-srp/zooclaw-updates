# ZooClaw 发布信息库

存放从飞书多维表格同步的原始发布信息，供下游 agent 调用。

- **来源**：[飞书多维表格](https://starquest.feishu.cn/base/Iap1bcHgnaWlJqs8wRdcvcPcnye?table=tbl3NTAENOKmW0mv)
- **更新方式**：手动同步或 agent 自动写入
- **目录结构**：
  - `updates/` — 每条更新一个 Markdown 文件，按日期+标题命名
  - `index.md` — 所有条目的索引，方便 agent 快速检索

## 字段说明

| 字段 | 说明 |
|------|------|
| title | 更新标题 |
| type | 信息类型（Bug Fix / 新功能上线 / Skill 上架/更新 / Agent 上架/更新 / 产品基础功能更新 / 其他公告） |
| priority | 优先级（高 / 中 / 低） |
| date | 来源日期 |
| status | 处理状态 |
| raw | 原始群消息内容 |
| summary | 核心宣传点 |
| notes | 备注 |
