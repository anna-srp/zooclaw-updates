---
title: "Agent 安装数量上限彻底放开：Free / Starter / Pro / Ultra 全部提到 100 万"
type: "产品基础功能更新"
priority: "中"
date: "2026-09-14"
status: "待审核"
channels: "changelog"
---

# Agent 安装数量上限彻底放开：Free / Starter / Pro / Ultra 全部提到 100 万

## 核心宣传点

Agent 安装数量的套餐上限在同一天被连续放开了两次：先从原值统一提到 10000（#3710），几十分钟后又统一提到 1000000（#3714）。四个套餐 Free / Starter / Pro / Ultra 现在拿到的是同一个数字 1000000，未知套餐仍然沿用 Starter 的默认值。换句话说，安装数量这个限制在实际使用中基本等于取消了。

生产代码的改动非常克制——两次都只是改映射表里的四个数值，安装锁、配额检查、重试逻辑和购买校验全部保留。数量检查用的是 Python 整数加法和比较，没有浮点转换，也不会按上限预分配资源，所以把上限提到百万级不会带来内存或资源开销。

仅需后端部署，无数据库迁移。

## 原始内容

### fix(agents): raise all plan install limits to 10000 (#3710)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `eb501ed1`
- PR: #3710
- 作者: tim-srp
- 日期: 2026-09-14T03:17:53Z

验证（PR 原文）：237 个相关单元测试通过；`bash scripts/verify-py.sh` 通过（Ruff、格式、Pyright、8 个导入契约）；`git diff --check` 通过。同步更新了四个测试文件中的套餐与边界断言，覆盖单装、Engine 安装、批量安装及到期套餐回退。

### fix(agents): raise all plan install limits to 1000000 (#3714)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `1452edfb`
- PR: #3714
- 作者: tim-srp
- 日期: 2026-09-14T04:05:25Z

验证（PR 原文）：237 个相关单元测试通过，覆盖 1000000 边界及超限拒绝；提交及推送钩子执行了静态、类型与导入检查；`git diff --check` 通过。

## 备注

发布状态：两条均为已合并待发版（尚未包含在任何 `ecap-*-release` tag 中）。

对外发布注意：#3710 已被同日的 #3714 取代，对外只讲最终值 1000000，不要提中间那次 10000。此前 9 月 10 日刚对外宣传过「Starter / Pro / Ultra 提到 20 / 40 / 100」，四天内连改三次，建议这次改成"安装数量不再设实际上限"这类不带具体数字的表述，避免再次打自己的脸。另外上限放开后是否有其他成本侧约束（运行环境、计算额度）需要产品确认，不宜让用户理解为可以无限免费安装。
