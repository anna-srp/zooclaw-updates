# 2026-07-16 同步阻塞说明

## 状态：GitHub 数据源凭据失效（部分阻塞）

### 【甲】GitHub commits（ecap-skills + ecap-workspace）— 阻塞
- 从 zooclaw-updates git remote 解析出的 PAT（ghp_，40 位）在 **GitHub REST API 上一律返回 `401 Bad credentials`**（含 `/user`、`/rate_limit`、`/repos/{repo}`）。
- 同一 token 对源仓库的 **git-over-HTTPS 也失败**：`remote: Invalid username or token`。
- 仅对 `anna-srp/zooclaw-updates` 自身仓库的 `git fetch/ls-remote` 仍可用（推测为该仓专用/缓存）。
- 结论：该 PAT 已轮换或对三个私有源仓的读权限被撤销，**无法按文档路径抓取 commits / PR body**。

### 替代通道验证：Composio GitHub 可用但不适合批量枚举
- Composio（github provider）**能访问** SerendipityOneInc 私有仓（`github_get_repo`/`github_list_pulls`/`github_get_pull` 均成功）。
- 但其返回体每个对象都携带完整 repo 样板元数据（单 PR ~16–20KB），在上下文内无法可靠枚举“昨日合并”的全部 PR（响应被截断在所需的 merged_at/title 字段之前）。
- `github_search_issues` 在 Composio 侧报错（`q` 字段校验 bug），无法用日期筛选。
- 已确认的昨日合并 PR 样本：ecap-workspace **#2925**（feat(web): BFF agent-install route，agents-v2 后端安装路由，属 ToB/用户无感基建，按硬规则#1 本就不进 updates/）。

### 【乙】Agent Pack 接口管道 — 正常
- `pack_diff.js`（用 USER_INTERNAL_TOKEN，未受影响）运行成功：first_run=false，追踪 12 个 pack，**本期 0 个 pack 更新**。

### 【7.6】历史「已合并待发版」回扫 — 阻塞
- `backfill_release_status.py` 依赖同一 GitHub API token，因 401 而 `TypeError`（release 列表返回错误 dict）。本次无法回扫。

## 需运维处理
请轮换/重新授权可读以下三仓的 GitHub PAT，并更新 zooclaw-updates 的 git remote 内嵌 token：
- SerendipityOneInc/ecap-skills
- SerendipityOneInc/ecap-workspace
- （agent-pack 已改走接口，无需 GitHub）
