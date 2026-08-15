---
title: "API 密钥页面说明改写，一句话讲清用途和权限"
type: "体验优化"
priority: "中"
date: "2026-08-14"
status: "待审核"
channels: ""
---

## 核心宣传点

不再出现让人困惑的「组织服务令牌」，直接说明 API 密钥是给你的脚本和后端服务调用 ZooClaw API 用的，并明确它对本组织全部 Agent 有完整访问权限。

## 原始内容

fix(settings): clarify API key descriptions (#3394)

## 背景

设置页 API Keys tab 的副标题原文是 "Create org service tokens for scripts and
external services that need to call your organization."：页面标题叫 API
Keys，正文却引入第二个术语「org service token」，且 "call your organization / 调用你的组织"
语义不明。内部反馈看不懂这句话在说什么。

## 改动

仅改 `en.ts` / `zh.ts` 中 `apiKeys.description` 与
`apiKeys.emptyDescription` 四条字符串：

| 位置 | 旧 | 新 |
|---|---|---|
| 副标题 EN | Create org service tokens for scripts and external services
that need to call your organization. | API keys let your scripts and
backend services call the ZooClaw API, with full access to this
organization's agents. |
| 副标题 ZH | 为脚本和外部服务创建组织服务令牌，以便调用你的组织。 | API 密钥供你的脚本和后端服务调用 ZooClaw
API，对本组织的全部 Agent 有完整访问权限。 |
| 空状态 EN | API keys are org service tokens for automations and
integrations. Create one when a script needs access. | Create one when a
script or external service needs to call this organization's agents. |
| 空状态 ZH | API 密钥是供自动化流程和集成使用的组织服务令牌。脚本需要访问时即可创建。 | 当脚本或外部服务需要调用本组织的
Agent 时，创建一个即可。 |

写法对齐主流产品的 API key 页面文案（Stripe / Anthropic / Cloudflare / Manus 调研）：

- **只用一个术语**：全文只说 API key（ZH：API 密钥），不再出现「服务令牌」。
- **用途优先**：一句话说清「谁用它访问什么」（scripts/backend services → ZooClaw API）。
- **权限直接披露**：我们的组织级 key 无 scope、对组织内全部 Agent 完整读写，参照 Stripe 对
unrestricted secret key 的写法直说，而非回避。
- 空状态正文不再复读上方标题 "No API keys yet"。

## 影响面

- 其余 8 个 locale（ar/de/es/fr/it/ja/ko/pt）没有 `apiKeys`
块，服务端字典深合并会自动回落到新英文，无需改动。
- 与 #3371（API key 管理页 redesign）无冲突：本分支基于最新 main，两句旧文案在 redesign
后原样保留，此处仅替换字符串。

## 验证

- `tsc` 单文件编译通过。
- 本地 `dev:staging` 起服渲染过目。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: wangfulong <wfllike@gmail.com>
Co-authored-by: Claude Opus 5 <noreply@anthropic.com>

---
### PR Body

## 背景

设置页 API Keys tab 的副标题原文是 "Create org service tokens for scripts and external services that need to call your organization."：页面标题叫 API Keys，正文却引入第二个术语「org service token」，且 "call your organization / 调用你的组织" 语义不明。内部反馈看不懂这句话在说什么。

## 改动

仅改 `en.ts` / `zh.ts` 中 `apiKeys.description` 与 `apiKeys.emptyDescription` 四条字符串：

| 位置 | 旧 | 新 |
|---|---|---|
| 副标题 EN | Create org service tokens for scripts and external services that need to call your organization. | API keys let your scripts and backend services call the ZooClaw API, with full access to this organization's agents. |
| 副标题 ZH | 为脚本和外部服务创建组织服务令牌，以便调用你的组织。 | API 密钥供你的脚本和后端服务调用 ZooClaw API，对本组织的全部 Agent 有完整访问权限。 |
| 空状态 EN | API keys are org service tokens for automations and integrations. Create one when a script needs access. | Create one when a script or external service needs to call this organization's agents. |
| 空状态 ZH | API 密钥是供自动化流程和集成使用的组织服务令牌。脚本需要访问时即可创建。 | 当脚本或外部服务需要调用本组织的 Agent 时，创建一个即可。 |

写法对齐主流产品的 API key 页面文案（Stripe / Anthropic / Cloudflare / Manus 调研）：

- **只用一个术语**：全文只说 API key（ZH：API 密钥），不再出现「服务令牌」。
- **用途优先**：一句话说清「谁用它访问什么」（scripts/backend services → ZooClaw API）。
- **权限直接披露**：我们的组织级 key 无 scope、对组织内全部 Agent 完整读写，参照 Stripe 对 unrestricted secret key 的写法直说，而非回避。
- 空状态正文不再复读上方标题 "No API keys yet"。

## 影响面

- 其余 8 个 locale（ar/de/es/fr/it/ja/ko/pt）没有 `apiKeys` 块，服务端字典深合并会自动回落到新英文，无需改动。
- 与 #3371（API key 管理页 redesign）无冲突：本分支基于最新 main，两句旧文案在 redesign 后原样保留，此处仅替换字符串。

## 验证

- `tsc` 单文件编译通过。
- 本地 `dev:staging` 起服渲染过目。

🤖 Generated with [Claude Code](https://claude.com/claude-code)
