# ecap-skills — 2026-05-28
共 1 条 commits

---
## [243e6fb] fix(connectors): rewrite description so social/login-site requests trigger the skill (#207)
- **作者**: vincent-srp
- **日期**: 2026-05-28T07:36:35Z
- **PR**: #207

### Commit Message
```
fix(connectors): rewrite description so social/login-site requests trigger the skill (#207)

* fix(connectors): rewrite description so social/login-site requests trigger the skill

zooclaw-connectors under-triggered for social / login-required services
(LinkedIn, Reddit, X). Root cause: the generic web-access skill intercepts
these — its description claims "社交媒体 / 需登录网站 / 操作网页", and the old
connector description neither named those platforms nor asserted any
precedence, so web-access won the triggering competition every time.
(Work tools like Notion/Slack/GitHub had no such competitor and already
triggered fine.)

Fix — rewrite the description to:
1. lead with capability and explicitly name social/consumer platforms
   (LinkedIn, X, Reddit, Discord) alongside the existing work tools;
2. add a precedence/boundary clause vs generic web/browser skills:
   "acts through the user's logged-in connection — NOT public-web browsing;
   prefer this over any generic web/browser skill when the target is a
   connected account";
3. keep a Skip list (Feishu/Lark, local git, Wi-Fi/VPN, building integrations)
   to preserve precision.

Validated with controlled triggering probes (claude -p, opus-4-7, full
real skill+MCP environment):
- LinkedIn(en/zh) + Reddit: 0/3 → 3/3 trigger the connector (was 100% web-access)
- Hard negatives (web search, Feishu msg, VPN, "write a connector", Wi-Fi):
  0/10 false triggers — precision held.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(connectors): add real connectors missing from the description (Confluence, Instagram, Facebook, Twitch)

Cross-checked the description against the live Connectors settings page
(ecap-proxy-service / Nango catalog, the skill's actual backend — NOT
claw-interface's google-only OAuth registry). Confirmed present but missing
from the description: Confluence (dev), Instagram/Facebook/Twitch (social).
LinkedIn and X/Twitter (added earlier) are confirmed real.

Additive only — Discord, Reddit, HubSpot, Salesforce are retained for now
pending confirmation (Discord/Reddit not seen in the SOCIAL MEDIA list, so
they may be overclaims to remove in a follow-up).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(connectors): repair SKILL.md frontmatter — colon+space in description broke YAML parse

The rewritten description contained "Typical asks: " and "Skip for: " — a
colon followed by space is illegal inside an unquoted YAML scalar, so
yaml.safe_load raised ScannerError and the skill linter reported the
frontmatter as missing (CI "Validate Skills" failure). Replaced both ": "
with " — " (the em-dash the description already uses); semantics and
triggering wording unchanged. Linter now passes locally (exit 0).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(connectors): drop the web-access precedence sentence from the description

Removed "Acts through the user's logged-in connection — NOT public-web
browsing or scraping; prefer this over any generic web/browser skill...".
It was added to win a triggering competition against a `web-access` skill
that exists only in the local dev environment — production deployments do
not ship web-access, so the premise doesn't hold. The real basis for this
skill's rewrite is that the old description never named social/consumer
platforms (LinkedIn/X/Instagram/...) and was framed narrowly as B2B "SaaS
accounts", so it under-triggered regardless of any competitor.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## 原先的问题
连接器 skill 对「操作我自己的社交 / 消费类账号」这类请求**不容易被触发**(典型:LinkedIn)。原描述把自己框定为 "external SaaS account",且只罗列了一串 **B2B 工作工具**(GitHub / Slack / Notion / Jira / Asana / HubSpot / Salesforce / Google 套件)。它**完全没点名 LinkedIn、X、Instagram 等社交 / 消费平台**,也没有对应这些平台的措辞——所以当用户说「帮我处理一下 LinkedIn」「发条 X」时,描述里没有任何信号表明该由这个 skill 处理,触发不稳定。

## 做了什么修改(只动 `SKILL.md` 的 description)
1. 能力导向开头("operate one of your own online accounts by name"),**显式点名真实存在的社交 / 消费平台**(LinkedIn、X/Twitter、Instagram、Facebook、Twitch),与工作类工具并列;
2. 对照线上 Connectors 设置页,**补齐此前漏写的真实连接器**(Confluence、Instagram、Facebook、Twitch);
3. 一句范围澄清:本 skill 是「操作你**已连接**的账号」,而非公网浏览 / 抓取;
4. 修复描述里 `: `(冒号+空格)破坏 YAML frontmatter、导致 Skill Lint 报 "missing frontmatter" 的问题。

## 依据与局限(诚实声明)
- 依据 = **原描述未涵盖这些平台、措辞过窄,导致不易触发**这一事实;改动让"用户点名的平台"与"skill 实际支持的连接器"对齐。
- 我此前用 `claude -p` 探针看到过触发改善,但那些探针跑在**我本地环境**(其中装了一个 `web-access` skill);**实际部署里没有 web-access**,因此本地观测到的"与 web-access 竞争"**不是生产成因,不作为本 PR 依据**——特此澄清,避免误导。
- 描述里的 Discord、Reddit、HubSpot、Salesforce 在设置页尚未确认存在,**暂保留未删**,待对照完整清单后清理。
- staging tag `v0.6.5-beta.1` 指向修复前 commit,尚未含本 PR 修正。

🤖 Generated with [Claude Code](https://claude.com/claude-code)
