---
title: "新增「知识库检索」Skill：Agent 可直接搜索组织内部知识库"
type: "Skill 上架/更新"
priority: "高"
date: "2026-07-02"
status: "待审核"
channels: ""
---
# 新增「知识库检索」Skill：Agent 可直接搜索组织内部知识库
## 核心宣传点
Agent 现在可以直接检索你所在组织上传的内部知识库文档（含图文段落），问内部资料不用再翻文件，答案直接来自你自己的知识库。
## 原始内容
### [ecap-skills PR #220]

feat(knowledge-base): add org knowledge-base search skill (#220)

---

## PR Description

## Summary
- New `knowledge-base` skill that lets an agent query an organization's internal knowledge base via ecap-proxy-service's new `POST /knowledge-base/search` endpoint (org-scoped RAG over uploaded docs, Vertex AI Search backed).
- Modeled on the existing proxy-backed skills (`websearch`, `video-generator`): stdlib-only Python CLI, standard `User-Agent: ecap-skill/1.0`, stdout JSON / stderr errors, YAML frontmatter.
- Scope: **search only** — the sibling `/knowledge-base/upload` is intentionally out of scope.

## Changes
- `knowledge-base/scripts/kb_search.py` — POSTs `{query, page_size, include_images}` and prints the proxy JSON (passages: `title` / `content` / `score` / `page_start` / `page_end` / `image_descriptions` / `images`) to stdout; errors to stderr with exit code 2.
  - **Flexible auth** (the endpoint requires an end-user identity): sends a user JWT (`Authorization: Bearer` from `USER_INTERNAL_TOKEN`) when present; otherwise the service key (`X-Proxy-Key` from `ECAP_PROXY_API_KEY`) plus `X-End-User-Id` (`ECAP_END_USER_ID`).
- `knowledge-base/SKILL.md` — single-line description (183 chars, bilingual triggers), `requires.bins: [python3]`, `requires.env: [ECAP_PROXY_BASE_URL]`, `install: []` (no third-party deps), When/When-NOT-to-use, prerequisites check, CLI/env tables, output schema.
- `knowledge-base/.env.example` — required `ECAP_PROXY_BASE_URL` + the two auth options.
- `PUBLISHED_SKILLS` — add `knowledge-base` so it ships to S3 on release.

## Related
- Backend endpoint: `ecap-proxy-service` branch `131-knowledge-base-search` (`app/routes/knowledge_base.py`, `app/service/knowledge_base.py`).

## Test plan
- [x] `python3 .github/scripts/lint_skills.py` passes clean (no errors/warnings for `knowledge-base`).
- [x] `python3 -m py_compile` + `--help` OK.
- [x] Missing `ECAP_PROXY_BASE_URL` -> `config_missing` JSON on stderr, exit 2.
- [x] Success path against a mock proxy: service-key mode sends `X-Proxy-Key` + `X-End-User-Id`; JWT mode sends `Authorization: Bearer` (raw token auto-prefixed); `--page-size` / `--no-images` correctly shape the request body.
- [ ] Live smoke test against a deployed proxy once `131-knowledge-base-search` is merged.

Fixes #219

🤖 Generated with [Claude Code](https://claude.com/claude-code)
