# ecap-agent-pack commits — 2026-04-28

> 抓取范围：2026-04-27T00:00:00Z ～ 2026-04-28T23:59:59Z  
> 共计 2 条 commits

---

## 793a06c2 — feat(tvc-studio): bump to 0.3.5 with new pack layout (#108)
- **作者**: vincent-srp  
- **时间**: 2026-04-27T12:31:48Z  
- **完整 Commit Message**:  
  feat(tvc-studio): bump to 0.3.5 with new pack layout  
  
  * feat(tvc-studio): bump to 0.3.5 with new pack layout  
  - Bump version 0.3.1 → 0.3.5; tighten manifest description and tags  
  - Move root-level docs (AGENTS/SOUL/IDENTITY/BOOTSTRAP/HEARTBEAT/avatar) out of agent/ into pack root, and skills/ into .agents/skills/ to match standard pack layout  
  - Add description.json (publish-time derived listing artifact)  
  - Reverse Seedance first-frame strategy in AGENTS.md: now mandatory dual-image input (storyboard grid as --first-frame + product multi-view via prompt suffix)  
  - Rewrite BOOTSTRAP.md welcome flow: skip dual-language welcome, request product/USP/brand-vs-seeding/platform info upfront  
  - Update tvc-director SKILL.md (+41 lines), tvc-post SKILL.md (+10 lines), chameleon-bridge SKILL.md, tvc-post compose.py and fetch_bgm.py  
  - Add Avatar field to IDENTITY.md  
  - Preserve assets/fonts/ (still referenced by tvc-post SKILL.md, not in upstream tarball)  
  
  * chore(tvc-studio): switch manifest description to English

- **PR Body**:  
  Update tvc-studio pack from 0.3.1 to 0.3.5，内容含：版本号和 manifest 更新；pack 目录结构迁移（符合标准 pack layout）；Seedance first-frame 策略反转（现在强制双图输入：分镜宫格为 first-frame + 商品多视角 prompt suffix）；BOOTSTRAP 欢迎流程重写（跳过双语欢迎，直接上手收集产品/USP/品牌信息）；tvc-director/tvc-post SKILL.md 更新；新增 description.json。

---

## ecd12f0f — fix(oura-ring-connector): add CTA to onboarding welcome message (#105)
- **作者**: Nemo Feng  
- **时间**: 2026-04-27T02:50:49Z  
- **完整 Commit Message**:  
  fix(oura-ring-connector): add CTA to onboarding welcome message  
  
  The first user-visible message ended with "Let's get you set up — it only takes a couple minutes", which left new users unsure what to type next. Replace the closing line with an explicit call-to-action that tells the user exactly how to start the flow (reply "yes" / "let's go").

- **PR Body**:  
  Oura Ring Health Agent 的新用户引导第一条消息末尾缺乏明确行动指引，用户不知道该输入什么。将结尾替换为明确的 CTA，告诉用户回复 "yes" 或 "let's go" 开始流程。保留了"只需几分钟"的体验预期设定，未改动其他文件。
