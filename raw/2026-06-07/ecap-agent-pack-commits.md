# ecap-agent-pack commits — 2026-06-07

⚠️ GitHub SAML SSO 授权问题

GitHub PAT（anna-srp）对 SerendipityOneInc 组织的 SAML SSO 授权已失效。
Token 本身有效，但 SSO 授权已过期，导致 REST API 返回 403 错误。
需要 anna-srp 账户持有人重新在 GitHub 上对 PAT 进行 SSO 授权：
https://github.com/settings/tokens → 找到 PAT → Grant access to SerendipityOneInc

本次同步时间：2026-06-08T01:05:01.641547+00:00
抓取目标日期：2026-06-07
状态：无法获取数据（SAML 403）
