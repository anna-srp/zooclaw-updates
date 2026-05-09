# ecap-skills Commits — 2026-05-08

## Commit a99372e0

- **SHA:** a99372e0e3a5f3e2d3c1b4a5d6e7f8091234abcd
- **Author:** allenz-srp
- **Date:** 2026-05-08T12:31:12Z
- **PR:** #192

### Full Commit Message

```
chore(devcontainer): wire @zooclaw/web-fetch into openclaw config (#192)

Adds the zooclaw-web-fetch plugin entry under plugins.entries and sets
tools.web.fetch.provider="zooclaw" so the devcontainer dispatches
web_fetch through the new plugin once openclaw-docker bakes it into
the image (ECA-624 W2 work).

The plugin is configured with no inline config — proxyUrl (from
ECAP_PROXY_BASE_URL) and the bearer token (from USER_INTERNAL_TOKEN)
are both injected by initializeCommand.sh's fastclaw deployment.env
fetch.

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #192 Body

## Summary

- Wires `@zooclaw/web-fetch` (zooclaw-extras#28) into the devcontainer's `openclaw.json.tmpl` so `web_fetch` tool calls dispatch through the new ZooClaw fetch proxy once openclaw-docker bakes the plugin into the image (ECA-624 W2).
- Adds two pieces:
  - `tools.web.fetch.provider="zooclaw"` — selects the new provider when present
  - `plugins.entries.zooclaw-web-fetch: { enabled: true }` — enables the plugin (no inline config; `proxyUrl` and the bearer token come from `ECAP_PROXY_BASE_URL` and `USER_INTERNAL_TOKEN` respectively, injected by `initializeCommand.sh`)

---

**筛选结果：❌ 仅保留 raw（chore，devcontainer 配置，内部开发工具）**
