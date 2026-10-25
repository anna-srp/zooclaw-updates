---
title: "国内访问时模型名称、简介和图标改用中文元数据"
type: "体验优化"
priority: "中"
date: "2026-10-22"
status: "待审核"
channels: ""
---

# 国内访问时模型名称、简介和图标改用中文元数据

## 核心宣传点

模型展示此前从表格同步进数据库的地区覆盖项里读中文信息，而网关侧现在已经直接提供了中文元数据。本次按「当前组织 → 网络归属 → CN」的既有优先级判定有效地区，中国地区请求统一使用网关提供的中文展示名、中文简介和中文图标；对应中文字段缺失、为空或互相冲突时各自独立回退到原有元数据，其他地区维持原字段不变。设置页的用量列表也采用同样的展示名选择逻辑，包含可明确对应的供应商别名。可选中文字段类型非法时会记录告警并保留部署原有的元数据、价格、别名与展示分层，模型 ID 不变。

## 分级

- 内部：P2
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `b32bdf9af1052e1594d7925cef744b1e2f0e21ed`
- PR: #4119
- 作者：sam-srp
- 日期：2026-10-22T08:55:00Z

### Commit Message

```
feat(models): use LiteLLM CN metadata for regional display (#4119)

## Summary

Model presentation currently reads regional overrides from Google
Sheet-synced Mongo data even though LiteLLM now provides the Chinese
metadata. Resolve the effective region using the existing current-org →
Cloudflare → CN priority, then use LiteLLM `model_info.display_name_cn`,
`description_cn`, and `logo_url_cn` for CN requests. Missing, blank, or
conflicting CN fields independently fall back to the original metadata;
other regions keep the original fields.

- Apply the same display-name selection to Settings Usage, including
unambiguous provider aliases.
- Ignore invalid types in optional CN fields with a diagnostic warning,
retaining the deployment's original metadata, prices, aliases, and
display tier.
- Preserve model IDs, entitlements, visibility, default selection,
prices, and display tiers.
- Remove the obsolete Mongo override reader, schema, related tests, and
import-contract entries. Existing database records are left intact.
- Backend-only change; no new environment variables or data migration.
Deployment should ensure the CN fields are populated in LiteLLM;
metadata retains the existing five-minute cache.

## Test plan

- [x] 176 targeted unit tests passed, covering model catalog, CN field
fallback/conflicts/invalid types, regional resolution, shared-cache
isolation, Usage aliases/routes, display tiers, and model retirement.
Invalid-type cases exercise the LiteLLM fetch path for each CN field.
- [x] `bash scripts/verify-py.sh`: Ruff lint/format, Pyright, and all
eight import contracts passed.
- [x] Complexity, repository-list synchronization, and dead-code checks
passed.
- [ ] Staging verification against real LiteLLM metadata after
deployment.
```

