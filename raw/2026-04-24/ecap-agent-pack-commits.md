# ecap-agent-pack commits — 2026-04-24 (UTC 2026-04-23)

共 2 条 commits

---

## 1. 1cdaee1f — feat(video-ads-duplicate): new agent pack for ad video duplication (#101)

- **SHA**: 1cdaee1f8244a2f009213355fb3d8ac1a134c013
- **作者**: david-srp
- **日期**: 2026-04-23T17:38:36Z
- **PR**: #101

### 完整 commit message

feat(video-ads-duplicate): new agent pack for ad video duplication (#101)

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Body（#101）

## 🎬 全新 Agent Pack：Video Ads Duplicate —— 一句话复刻爆款广告

### 新增内容
新增 agent pack `video-ads-duplicate`，让广告主/电商卖家/内容团队 **不拍摄、不剪辑、不用任何技术背景**，只要一条参考广告 + 自家产品信息，就能在一次对话内生成全新的产品广告视频。

**核心公式**：`参考广告视频 + 产品信息（图片 / 标题 / 描述）= 你的新广告`

### 🚀 它能做什么

#### 1. 自动获取产品信息（Amazon & 任意电商页面）
- 用户扔一个产品链接就行，agent 会按**三级回退**自动拉取：
  1. **Amazon ASIN 直连**（Product API）—— 最快，官方数据
  2. **Crawl Agent 通用抓取** —— 覆盖 Shopify 独立站、TikTok Shop 等任意页面
  3. **WebFetch / Playwright 兜底** —— 反爬严格的站点也能拿到
- 自动提取：标题、品牌、描述、卖点（USP）、全部产品主图
- 也支持用户手动粘贴标题 / 描述 / 图片 URL

#### 2. 爆款广告素材库搜索
- 关键词 1-3 个词即可搜索 **Facebook 系、TikTok、独立站**跑量广告
- 按广告热度（新广告 / 爆款广告）、站点类型（Shopify 等）过滤
- 展示 5-10 个去重后的参考视频候选，直接内嵌播放

#### 3. 两条生成路径，用户自选

**Path A · 风格复刻（推荐）**
- 流程：AI 分析参考视频的分镜和节奏 → 为你的产品重写脚本 → 生成开场首帧 → Seedance 2.0 按首帧续生完整视频
- ✅ **产品外观 100% 还原**（首帧锁住包装 / Logo / 颜色 / 材质）
- ✅ 全新内容 → **规避版权风险**，可长时间投放
- ✅ 支持 **> 15 秒长视频**，通过 chunk 串联（上一段尾帧 → 下一段首帧）保证镜头连贯

**Path B · 智能商品替换**
- 流程：参考视频 + 产品图一次性交给 Seedance，端到端生成
- ✅ 运动 / 构图 / 节奏 **近乎 1:1** 保留，只换产品
- ⚠️ 单次调用受 Seedance 15 秒硬限制

#### 4. 专业级视频脚本改写
Stage 4 的脚本生成器按**高转化广告文案结构**改写旁白：
- **3 秒 Hook** —— 好奇 / 紧迫 / 大胆断言
- **真实使用体验** —— 第一人称感官细节，非套话
- **核心卖点** —— 自然植入品牌名、成分、差异化
- **CTA** —— 与参考视频口吻一致的收尾

#### 5. 首帧图片严格保真
- 默认 `gemini-3.1-flash-image-preview`，可切 `gemini-3-pro-image-preview`
- **Prompt 内置零容忍产品保真规则**：同形状、同颜色、同 Logo、同包装
- 默认 9:16 竖版（TikTok / Reels / Shorts）
- **人脸首帧不再是 blocker**：遇到 `InputImageSensitiveContentDetected` 时自动走 chameleon skill 的 `asset_register.py`

#### 6. Seedance 2.0 长视频 + Chunk 执行计划
Stage 5 结束后，agent 会向用户展示**完整 Chunk 确认表**再执行，杜绝"黑盒消耗 credit"

---

## 2. 110b61e8 — feat(amazon-analyst): new agent pack with proxy-based auth (#100)

- **SHA**: 110b61e8c445a88d5600f067babe232187738b37
- **作者**: christine-srp
- **日期**: 2026-04-23T07:57:57Z
- **PR**: #100

### 完整 commit message

feat(amazon-analyst): new agent pack with proxy-based auth (#100)

Introduces the Amazon Analyst agent pack (📦 亚马逊分析师) — a friendly,
data-driven advisor that routes natural-language questions to one of 10
bundled skills (listing audit, opportunity discovery, market entry,
competitor intelligence, pricing, reviews, daily radar, trend scanner,
general analysis, and the apiclaw base layer).

All upstream APIClaw traffic is routed through ecap-proxy-service:
- Scripts read ECAP_PROXY_BASE_URL and USER_INTERNAL_TOKEN from the pod env
- Proxy validates the JWT, swaps in the server-held APIClaw API key, and
  forwards to api.apiclaw.io/openapi/v2
- No credential is embedded in the pack — earlier iterations shipped a
  baked-in APICLAW_API_KEY which is eliminated here

Pack layout follows the existing convention (IDENTITY / SOUL / AGENTS /
BOOTSTRAP at root, skills under .agents/skills/). The apiclaw.py script
is canonical in .agents/skills/apiclaw/scripts/ and byte-identical copies
live in each amazon-*/scripts/ directory.

Depends on SerendipityOneInc/ecap-proxy-service#37 for the /apiclaw
route and the server-side APICLAW_API_KEY secret.

### PR Body（#100）

## Summary

Introduces the **Amazon Analyst** agent pack (📦 亚马逊分析师) — a data-driven advisor for Amazon sellers that routes natural-language questions to one of 10 bundled skills (listing audit, opportunity discovery, market entry, competitor intelligence, pricing, reviews, daily radar, trend scanner, general analysis, and the `apiclaw` base layer).

The pack was previously distributed as a standalone `.tar.gz` from zooclaw.ai with an upstream `APICLAW_API_KEY` baked into the distribution. That key is eliminated here. All APIClaw calls now go through `ecap-proxy-service` using the standard Zooclaw auth pattern.

## How auth works

```
user claw pod (USER_INTERNAL_TOKEN JWT + ECAP_PROXY_BASE_URL in env)
    │  Authorization: Bearer <jwt>
    ▼
ecap-proxy-service  /apiclaw/<endpoint>
    │  validate JWT, inject server-held APICLAW_API_KEY
    ▼
api.apiclaw.io/openapi/v2/<endpoint>
```

## Layout

```
amazon-analyst/
├── AGENTS.md          # routing rules, skill selection, runtime rules
├── BOOTSTRAP.md       # first-message greeting logic
├── IDENTITY.md        # name / emoji / vibe
├── SOUL.md            # tone and personality
├── agent-pack.yaml    # name / version / skills / requires.env
├── description.json   # ClawHub-facing metadata
└── .agents/skills/
    ├── apiclaw/                                       # base layer (11 endpoints)
    ├── amazon-listing-audit-pro/                      # P1 skills
    ├── amazon-opportunity-discoverer/
    ├── amazon-market-entry-analyzer/
    ├── amazon-competitor-intelligence-monitor/
    ├── amazon-daily-market-radar/                     # P2 skills
    ├── amazon-market-trend-scanner/
    ├── amazon-pricing-command-center/
    ├── amazon-review-intelligence-extractor/
    └── amazon-analysis/                               # P3 general fallback
```
