# SerendipityOneInc/ecap-skills commits — 2026-08-14

## feat(publish): production lane 补 v2 registry sync（SKILLS_V2_SYNC_ENABLED 总闸） (#266)

- sha: `4f81afc118577311a080c8434f63016fa8575620`
- author: Chris@ZooClaw
- date: 2026-08-14T07:13:41Z
- PR: 266

### Commit message

```
feat(publish): production lane 补 v2 registry sync（SKILLS_V2_SYNC_ENABLED 总闸） (#266)

V2 上线计划 §1 B4 / §3.2-6 的落地（zooclaw-engine 计划
docs/plans/2026-08-12-v2-production-launch-plan.md，PR zooclaw-engine#677
已合入）。

## 内容

给 `publish-to-production` job 补上与 staging 对齐的 v2 registry dual-write：

1. **Validate PUBLISHED_SKILLS**（含 `sync-v2-registry.mjs --validate`
fail-fast 闸）与 **Publish skills to engine registry**（publish +
reconcile）两步，逐字对齐 staging job。
2. **总闸 `SKILLS_V2_SYNC_ENABLED`**（production environment var）：
- 未设置/非 true：跳过 registry 两步，S3 发布照常，但每次 run 打 `::warning`（"prod v2
agents get ZERO global skills"）——prod engine registry 还不存在，直接照抄 staging
的 fail-fast 会打断现有 v1 生产发布，故用显式开关分期。
- 设为 true：行为与 staging 完全一致，fail-fast（registry 配置缺失阻断整个发布，包括 S3——防止桶被
--delete 后 registry 步骤才失败）。
3. Lark 通知增加 V2 registry sync 状态行。

## 启用步骤（launch 时人工执行，计划 §3.2-6）

1. 完成 ecap-skills#265（泄漏 JWT 吊销）——硬前置；
2. production environment 配 `SKILLS_PUBLISH_BASE_URL` var（prod
claw-interface relay）+ `SKILLS_PUBLISH_TOKEN` secret；
3. 设 `SKILLS_V2_SYNC_ENABLED=true`；
4. 下一个 `-release` tag 即 dual-write，验收=prod registry 18 skill 就位 +
reconcile 成功。

## 验证

- `yaml.safe_load` 通过；production job 步骤序：Checkout → Note skipped（gate
off 分支）→ Validate（gate on）→ S3 → engine registry（gate on）→ Notify。
- 本 PR 合并后、开关未开期间，对现有生产发布行为零影响（仅多一条 warning）。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_012yunBhKSUgkUW152oFwdgs
```

### PR body

V2 上线计划 §1 B4 / §3.2-6 的落地（zooclaw-engine 计划 docs/plans/2026-08-12-v2-production-launch-plan.md，PR zooclaw-engine#677 已合入）。

## 内容

给 `publish-to-production` job 补上与 staging 对齐的 v2 registry dual-write：

1. **Validate PUBLISHED_SKILLS**（含 `sync-v2-registry.mjs --validate` fail-fast 闸）与 **Publish skills to engine registry**（publish + reconcile）两步，逐字对齐 staging job。
2. **总闸 `SKILLS_V2_SYNC_ENABLED`**（production environment var）：
   - 未设置/非 true：跳过 registry 两步，S3 发布照常，但每次 run 打 `::warning`（"prod v2 agents get ZERO global skills"）——prod engine registry 还不存在，直接照抄 staging 的 fail-fast 会打断现有 v1 生产发布，故用显式开关分期。
   - 设为 true：行为与 staging 完全一致，fail-fast（registry 配置缺失阻断整个发布，包括 S3——防止桶被 --delete 后 registry 步骤才失败）。
3. Lark 通知增加 V2 registry sync 状态行。

## 启用步骤（launch 时人工执行，计划 §3.2-6）

1. 完成 ecap-skills#265（泄漏 JWT 吊销）——硬前置；
2. production environment 配 `SKILLS_PUBLISH_BASE_URL` var（prod claw-interface relay）+ `SKILLS_PUBLISH_TOKEN` secret；
3. 设 `SKILLS_V2_SYNC_ENABLED=true`；
4. 下一个 `-release` tag 即 dual-write，验收=prod registry 18 skill 就位 + reconcile 成功。

## 验证

- `yaml.safe_load` 通过；production job 步骤序：Checkout → Note skipped（gate off 分支）→ Validate（gate on）→ S3 → engine registry（gate on）→ Notify。
- 本 PR 合并后、开关未开期间，对现有生产发布行为零影响（仅多一条 warning）。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_012yunBhKSUgkUW152oFwdgs

