---
title: "官网 ZooData 卡片文案重写，10 个语言版本同步对齐"
type: "体验优化"
priority: "低"
date: "2026-09-23"
status: "待审核"
channels: ""
---

# 官网 ZooData 卡片文案重写，10 个语言版本同步对齐

## 核心宣传点

官网首页 ZooData 卡片的产品说明整体更新，并把全部 10 个语言版本统一到最终英文文案。Token 节省从「约减少 75%」改为「最多减少 75% 的 LLM Token」；付费口径从「仅为使用的字段付费」改为「仅为使用的数据付费」；产品定位从 Amazon / TikTok 的预分析商业情报，改为电商、金融、外卖和社交平台的实时结构化数据，并移除了这段里关于竞品、市场、流量、消费者分析以及 API / CLI / MCP 附带能力的表述。中文、日语、韩语、德语、法语、西语、意语、葡语、阿语译文全部按最终英文重译。

## 分级

- 内部：P2
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## 改动概述

更新官网首页 ZooData 卡片的产品说明，并将全部 10 个语言版本统一到最终英文文案。调整集中在产品定位、Token 节省表述、付费口径和数据覆盖范围。

- **Token 节省表述**：将“约减少 75%”调整为“最多减少 75% 的 LLM Token”。
- **付费口径**：将“仅为使用的字段付费”调整为“仅为使用的数据付费”。
- **数据覆盖与定位**：将 Amazon / TikTok 的预分析商业情报描述，调整为电商、金融、外卖和社交平台的实时结构化数据描述；移除本段中的竞品、市场、流量、消费者分析及 API / CLI / MCP 附带能力表述。
- **多语言一致性**：以最终英文为基准，更新中文、日语、韩语、德语、法语、西班牙语、意大利语、葡萄牙语和阿拉伯语译文。英文使用正确的主谓形式“ZooData turns”；该语法修正不改变其他语言译文。
- **页面与翻译联动**：同步首页组件及 10 份语言字典的索引，确保各语言页面能读取对应译文。

## 最终英文文案

> ZooData turns any URL into agent-ready JSON with up to 75% fewer LLM tokens—and pay only for the data you use. Access real-time, structured data across e-commerce, finance, food delivery, and social platforms.

## 影响范围

共修改 11 个文件：1 个首页组件和 10 份语言字典，均限于 ZooData 的这一段说明。此次为产品文案更新，不包含数据接口或后端能力实现，也不涉及其他字段、页面样式和交互行为。

## 验证结果

- 本地已核对最终英文逐字一致、10 个语言版本的语法与字典读取正常，以及其他字典字段未被改动；`git diff --check` 通过。
- 最新代码提交 `526aa2aae` 的 CI 前端代码规范／类型检查、测试、构建及 CodeQL 检查均已通过。
- 独立工作目录未安装前端依赖，本地未运行完整前端检查或浏览器视觉验收；完整前端检查由 CI 完成。


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `bb644fa874d41ff9c739b8776f3009954c7ce433`
- PR: #3868
- 作者：ericma-srp
- 日期：2026-09-23T04:02:16Z

### Commit Message

```
fix(landing): update ZooData copy across all locales (#3868)

## 改动概述

更新官网首页 ZooData 卡片的产品说明，并将全部 10 个语言版本统一到最终英文文案。调整集中在产品定位、Token
节省表述、付费口径和数据覆盖范围。

- **Token 节省表述**：将“约减少 75%”调整为“最多减少 75% 的 LLM Token”。
- **付费口径**：将“仅为使用的字段付费”调整为“仅为使用的数据付费”。
- **数据覆盖与定位**：将 Amazon / TikTok
的预分析商业情报描述，调整为电商、金融、外卖和社交平台的实时结构化数据描述；移除本段中的竞品、市场、流量、消费者分析及 API / CLI /
MCP 附带能力表述。
-
**多语言一致性**：以最终英文为基准，更新中文、日语、韩语、德语、法语、西班牙语、意大利语、葡萄牙语和阿拉伯语译文。英文使用正确的主谓形式“ZooData
turns”；该语法修正不改变其他语言译文。
- **页面与翻译联动**：同步首页组件及 10 份语言字典的索引，确保各语言页面能读取对应译文。

## 最终英文文案

> ZooData turns any URL into agent-ready JSON with up to 75% fewer LLM
tokens—and pay only for the data you use. Access real-time, structured
data across e-commerce, finance, food delivery, and social platforms.

## 影响范围

共修改 11 个文件：1 个首页组件和 10 份语言字典，均限于 ZooData
的这一段说明。此次为产品文案更新，不包含数据接口或后端能力实现，也不涉及其他字段、页面样式和交互行为。

## 验证结果

- 本地已核对最终英文逐字一致、10 个语言版本的语法与字典读取正常，以及其他字典字段未被改动；`git diff --check` 通过。
- 最新代码提交 `526aa2aae` 的 CI 前端代码规范／类型检查、测试、构建及 CodeQL 检查均已通过。
- 独立工作目录未安装前端依赖，本地未运行完整前端检查或浏览器视觉验收；完整前端检查由 CI 完成。
```

来源：SerendipityOneInc/ecap-workspace @ bb644fa8，PR #3868，作者 ericma-srp。