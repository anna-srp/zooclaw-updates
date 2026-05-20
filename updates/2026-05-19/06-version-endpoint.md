---
title: "新增服务版本查询接口"
type: "产品基础功能更新"
priority: "低"
date: "2026-05-19"
status: "待审核"
channels: ""
---
# 新增服务版本查询接口

## 核心宣传点
后端新增版本信息查询接口，便于技术团队快速定位线上部署版本，提升运维响应速度。

## 原始内容
```
commit: a674ecf70d6db777b77f5fadb87a5b2c37cf11a1
repo: SerendipityOneInc/ecap-workspace
author: Chris@ZooClaw
date: 2026-05-19T14:00:03Z

feat(service): add /version endpoint aligned with frontend schema (#1746)

## Summary
- Adds `GET /version` on `claw-interface` returning the same JSON shape
as the frontend `/api/version`, so monitoring / oncall can compare
frontend vs backend deployed versions side-by-side.
- Reads `/code/manifest.metadata` (populated at image-build time by
`srp-actions/.github/workflows/build-and-push-image-cached.yml`) plus
the `ENVIRONMENT` env var; falls back gracefully when fields are missing
(local dev, branch builds, manifest absent).
- Schema mirrors the frontend `buildInfo` exactly: `{ success, data: {
version, commit, commitFull, buildTime, environment, ref, deployedBy }
}`.

## Field mapping
| Field | Source |
|---|---|
| `commit` / `commitFull` | `GIT_COMMIT_HASH` from manifest (7-char +
full) |
| `version` / `ref` | `GIT_TAGS` first entry; fallback to
`GIT_BRANCH_NAME`, then `pyproject.toml` `[project].version` |
| `buildTime` | `IMAGE_TIMESTAMP` normalized from `"YYYY-MM-DD HH:MM:SS
UTC"` to ISO 8601 `Z` |
| `environment` | `ENVIRONMENT` env var (currently \"unknown\" — see
follow-up) |
| `deployedBy` | `DEPLOYED_BY` from manifest if present, else `\"ci\"`
(see follow-up) |

## Follow-ups (not in this PR)
- Add `ENVIRONMENT` env var to
`services/claw-interface/kustomize/overlays/*` Deployment patches —
otherwise `environment` always reports `\"unknown\"`.
- Optionally extend the `srp-actions` reusable workflow to emit
`DEPLOYED_BY=\${{ github.actor }}` into `manifest.metadata` so
`deployedBy` returns a real handle instead of `\"ci\"`.
Forward-compatible: this PR already reads `DEPLOYED_BY` and will pick up
the real value automatically once upstream emits it.

## Test plan
- [x] `app/routes/status.py` + `tests/unit/test_status.py` pass
`ast.parse`
- [x] Smoke-tested `_normalize_build_time('2026-05-19 12:23:50 UTC')` ->
`'2026-05-19T12:23:50Z'` on local Python 3.11
- [x] Smoke-tested `_build_info()` no-manifest path -> returns sensible
`\"unknown\"` placeholders + `version='0.0.0'`
- [ ] CI `python-code-quality / build-and-test` (ruff + pyright +
pytest) covers the full suite incl. 3 new unit tests
- [ ] Post-deploy: `kubectl -n <ns> exec <claw-interface-pod> -- curl -s
localhost:8080/version | jq` returns a real SHA matching the deployment
image tag
- [ ] Side-by-side: `curl https://<frontend>/api/version | jq .data` vs
`curl https://<backend>/version | jq .data` — fields aligned, values
represent each service's own build

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

--- PR #1746 Body ---
## Summary
- Adds `GET /version` on `claw-interface` returning the same JSON shape as the frontend `/api/version`, so monitoring / oncall can compare frontend vs backend deployed versions side-by-side.
- Reads `/code/manifest.metadata` (populated at image-build time by `srp-actions/.github/workflows/build-and-push-image-cached.yml`) plus the `ENVIRONMENT` env var; falls back gracefully when fields are missing (local dev, branch builds, manifest absent).
- Schema mirrors the frontend `buildInfo` exactly: `{ success, data: { version, commit, commitFull, buildTime, environment, ref, deployedBy } }`.

## Field mapping
| Field | Source |
|---|---|
| `commit` / `commitFull` | `GIT_COMMIT_HASH` from manifest (7-char + full) |
| `version` / `ref` | `GIT_TAGS` first entry; fallback to `GIT_BRANCH_NAME`, then `pyproject.toml` `[project].version` |
| `buildTime` | `IMAGE_TIMESTAMP` normalized from `"YYYY-MM-DD HH:MM:SS UTC"` to ISO 8601 `Z` |
| `environment` | `ENVIRONMENT` env var (currently \"unknown\" — see follow-up) |
| `deployedBy` | `DEPLOYED_BY` from manifest if present, else `\"ci\"` (see follow-up) |

## Follow-ups (not in this PR)
- Add `ENVIRONMENT` env var to `services/claw-interface/kustomize/overlays/*` Deployment patches — otherwise `environment` always reports `\"unknown\"`.
- Optionally extend the `srp-actions` reusable workflow to emit `DEPLOYED_BY=\${{ github.actor }}` into `manifest.metadata` so `deployedBy` returns a real handle instead of `\"ci\"`. Forward-compatible: this PR already reads `DEPLOYED_BY` and will pick up the real value automatically once upstream emits it.

## Test plan
- [x] `app/routes/status.py` + `tests/unit/test_status.py` pass `ast.parse`
- [x] Smoke-tested `_normalize_build_time('2026-05-19 12:23:50 UTC')` -> `'2026-05-19T12:23:50Z'` on local Python 3.11
- [x] Smoke-tested `_build_info()` no-manifest path -> returns sensible `\"unknown\"` placeholders + `version='0.0.0'`
- [ ] CI `python-code-quality / build-and-test` (ruff + pyright + pytest) covers the full suite incl. 3 new unit tests
- [ ] Post-deploy: `kubectl -n <ns> exec <claw-interface-pod> -- curl -s localhost:8080/version | jq` returns a real SHA matching the deployment image tag
- [ ] Side-by-side: `curl https://<frontend>/api/version | jq .data` vs `curl https://<backend>/version | jq .data` — fields aligned, values represent each service's own build

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```
