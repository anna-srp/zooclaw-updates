# SerendipityOneInc/ecap-skills commits 2026-08-13

## f79ed0b6

- sha: `f79ed0b65f5187d86ab817f23384c387d8ba0618`
- 作者: Chris@ZooClaw
- 日期: 2026-08-13T13:52:01Z
- PR: 264

### Commit message

```
chore(skills): remove unsupported V2 defaults (#264)

## Summary

- remove `browser-skill` from the V2 registry allowlist now that
`browser-ops` is the V2 browser source of truth
- remove `bot-mailbox` from the V2 registry allowlist until a mailbox
runtime contract exists
- keep both skills in the V1 S3 publication list and document why they
are held out of V2

## Tracking

- SerendipityOneInc/zooclaw-engine#540
- SerendipityOneInc/zooclaw-engine#719

## Validation

- `PUBLISH_BASE_URL=http://example.invalid PUBLISH_TOKEN=validation-only
node .github/scripts/sync-v2-registry.mjs --validate`
- `node .github/scripts/sync-v2-registry.mjs --dry-run`
- `python3 .github/scripts/lint_skills.py` (passes with 12 pre-existing
warnings)
- `git diff --check`

The V2 reconcile set now contains 17 skills. `bot-mailbox` and
`browser-skill` move to the held-out set; no skill source or V1
publication entry is deleted.
```

### PR body

## Summary

- remove `browser-skill` from the V2 registry allowlist now that `browser-ops` is the V2 browser source of truth
- remove `bot-mailbox` from the V2 registry allowlist until a mailbox runtime contract exists
- keep both skills in the V1 S3 publication list and document why they are held out of V2

## Tracking

- SerendipityOneInc/zooclaw-engine#540
- SerendipityOneInc/zooclaw-engine#719

## Validation

- `PUBLISH_BASE_URL=http://example.invalid PUBLISH_TOKEN=validation-only node .github/scripts/sync-v2-registry.mjs --validate`
- `node .github/scripts/sync-v2-registry.mjs --dry-run`
- `python3 .github/scripts/lint_skills.py` (passes with 12 pre-existing warnings)
- `git diff --check`

The V2 reconcile set now contains 17 skills. `bot-mailbox` and `browser-skill` move to the held-out set; no skill source or V1 publication entry is deleted.


## 40b5ad61

- sha: `40b5ad61302d055eaa5fb4e062ae4c83a3ebb2da`
- 作者: Chris@ZooClaw
- 日期: 2026-08-13T09:31:47Z
- PR: 263

### Commit message

```
feat(browser-ops): v2 browser tool skill (design/23 M3) (#263)

## 内容

v2 browser 工具的 built-in skill（design/23 M3）：`browser-ops/SKILL.md`。教模型使用
v2 原生 `browser` 工具（单工具 + action），纯散文、无脚本无 MCP（区别于 v1 `browser-skill` 的
Browserbase-MCP + node 脚本形态）。

覆盖：

1. **进度播报纪律**（从 browser-skill
移植）：每个有意义的步骤前给用户一句人话进度，用用户语言，不暴露工具名/JSON/ref/session 细节。
2. **操作循环**：navigate → snapshot → act → snapshot 验证，强调「act 后必 snapshot」。
3. **ref 纪律**：只用最近一次 snapshot 的 ref；`REF_STALE` → 重新 snapshot。
4. **CN 站点**：xhs/抖音/微信先 `session op=restart egressCountry="CN"`
再导航；`ANTI_BOT_SUSPECTED` 处置顺序 handoff > 换 egress > 放弃。
5. **登录**：两段式 SMS、`save_login` 时机、多账号 `loginLabel`。
6. **handoff**：captcha/扫码时返回 live 链接给用户接管，完成后 save_login。
7. **upload**：snapshot 找 file input ref → `action=upload ref r2Key`（如
image_generate 产物），50MB 上限。
8. 站点专属流程（小红书发布等）**不写死**在这里，留给站点专属 skill 叠加。

## 装配

- 加入 `PUBLISHED_SKILLS`。
- 条件装配：顶层 `requires.config: ["browser"]`（v2 controld `readRequires()`
读顶层；只有 declared config 有 `browser` 键的 agent 才 eligible）。
- `install: []`（无依赖）。skill-lint 本地通过。

## M3 剩余（本 PR 不含，后续跟进）

- **staging smoke**：zooclaw-engine `scripts/smoke/browser-ba.ts` 真实 BA
E2E（验 CDP 鉴权、upload 真通——单测的 fake driver 覆盖不到）。
- **production registry publish**：`publish-skills.yml` 目前 v2 registry
发布只在 staging job，上 prod 需补 production job 的 `/skills/registry-publish`
步骤（design/23 §7 M3）。
- 文档：`zooclaw-engine` 的
`docs/v1-parity-gap-inventory.md`、`docs/comparison/v2-vs-openclaw`、#338/#582
状态同步。

Refs SerendipityOneInc/zooclaw-engine#338、design/23-browser-tools.md §6。
```

### PR body

## 内容

v2 browser 工具的 built-in skill（design/23 M3）：`browser-ops/SKILL.md`。教模型使用 v2 原生 `browser` 工具（单工具 + action），纯散文、无脚本无 MCP（区别于 v1 `browser-skill` 的 Browserbase-MCP + node 脚本形态）。

覆盖：

1. **进度播报纪律**（从 browser-skill 移植）：每个有意义的步骤前给用户一句人话进度，用用户语言，不暴露工具名/JSON/ref/session 细节。
2. **操作循环**：navigate → snapshot → act → snapshot 验证，强调「act 后必 snapshot」。
3. **ref 纪律**：只用最近一次 snapshot 的 ref；`REF_STALE` → 重新 snapshot。
4. **CN 站点**：xhs/抖音/微信先 `session op=restart egressCountry="CN"` 再导航；`ANTI_BOT_SUSPECTED` 处置顺序 handoff > 换 egress > 放弃。
5. **登录**：两段式 SMS、`save_login` 时机、多账号 `loginLabel`。
6. **handoff**：captcha/扫码时返回 live 链接给用户接管，完成后 save_login。
7. **upload**：snapshot 找 file input ref → `action=upload ref r2Key`（如 image_generate 产物），50MB 上限。
8. 站点专属流程（小红书发布等）**不写死**在这里，留给站点专属 skill 叠加。

## 装配

- 加入 `PUBLISHED_SKILLS`。
- 条件装配：顶层 `requires.config: ["browser"]`（v2 controld `readRequires()` 读顶层；只有 declared config 有 `browser` 键的 agent 才 eligible）。
- `install: []`（无依赖）。skill-lint 本地通过。

## M3 剩余（本 PR 不含，后续跟进）

- **staging smoke**：zooclaw-engine `scripts/smoke/browser-ba.ts` 真实 BA E2E（验 CDP 鉴权、upload 真通——单测的 fake driver 覆盖不到）。
- **production registry publish**：`publish-skills.yml` 目前 v2 registry 发布只在 staging job，上 prod 需补 production job 的 `/skills/registry-publish` 步骤（design/23 §7 M3）。
- 文档：`zooclaw-engine` 的 `docs/v1-parity-gap-inventory.md`、`docs/comparison/v2-vs-openclaw`、#338/#582 状态同步。

Refs SerendipityOneInc/zooclaw-engine#338、design/23-browser-tools.md §6。

