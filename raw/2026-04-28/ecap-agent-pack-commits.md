# ecap-agent-pack commits — 2026-04-28

**共 3 个 commit**

---

## chore: remove sup-fresh agent pack (#112)

- **SHA**: `1ae97ee7eec386ac5e7168f23ba9cd54c4f3907f`

- **作者**: david-srp

- **时间**: 2026-04-28T09:49:49Z


### 完整 Commit Message
```
chore: remove sup-fresh agent pack (#112)

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```


### PR #112 Body
## Summary
- Delete the entire \`sup-fresh/\` directory (12 files: agent pack scaffolding + 6 sop/init/loss/pricing/settle/task skills).

## Test plan
- [ ] Confirm no other pack imports or references \`sup-fresh\`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)



---

## fix(amazon-analyst): downgrade to keyword-only when categoryPath returns empty (#111)

- **SHA**: `a3b24a27e215f1b7481b25f5c468dd05151b00f6`

- **作者**: christine-srp

- **时间**: 2026-04-28T09:42:32Z


### 完整 Commit Message
```
fix(amazon-analyst): downgrade to keyword-only when categoryPath returns empty (#111)

Mirrors APIClaw-Skills #60: when --keyword and a deep-leaf --category are
both supplied (e.g. "Electronics > … > Over-Ear Headphones"), the
backend has no aggregation data for that exact leaf and markets/search
returns total=0. Without the fallback, the dead categoryPath propagates
to every downstream step in cmd_market_entry, so the entire 11-endpoint
report comes back empty.

After Step 1a, if markets/search came back failed/empty AND we have a
keyword to fall back to, drop categoryPath and rerun keyword-only. The
downgrade is recorded in results.meta.category_downgrade.

All 10 bundled apiclaw.py copies under amazon-analyst/.agents/skills/
get the same patch (sync-managed copies of the canonical script).

Reproduced via Kimi 2.5 driving amazon-analyst against "Over-Ear
Headphones" — the user-facing report ended up all-empty.

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```


### PR #111 Body
## Summary

Mirrors the canonical fix in SerendipityOneInc/APIClaw-Skills#61.

When `--keyword` and a deep-leaf `--category` are both supplied (e.g. `Electronics > … > Over-Ear Headphones`), the backend has no aggregation data for that exact leaf and `markets/search` returns `total=0`. Without the fallback, the dead `categoryPath` propagates to every downstream step in `cmd_market_entry`, so the entire 11-endpoint report comes back empty.

After Step 1a, if `markets/search` came back failed/empty AND we have a keyword to fall back to, drop `categoryPath` and rerun keyword-only. The downgrade is recorded in `results.meta.category_downgrade`.

All 10 bundled `apiclaw.py` copies under `amazon-analyst/.agents/skills/` get the same patch (sync-managed copies of the canonical script).

## Why

Reproduced via Kimi 2.5 driving `amazon-analyst` against "Over-Ear Headphones" — the user-facing report ended up all-empty. Symptoms:

- `markets/search` → `total: 0`
- `products/*` → `HTTP 500`
- `reviews/analysis` → `INSUFFICIENT_REVIEWS (0 reviews)`

## Diff shape

- 10 files, +200 lines, -0 (pure additive 20-line fallback block in each copy's `cmd_market_entry`)
- No other changes

## Related

- Canonical fix: SerendipityOneInc/APIClaw-Skills#61
- Backend bug tracker (separate, server-side fix needed for full resolution): SerendipityOneInc/hermes-workspace#223
  — `/products/*` HTTP 500 on `keyword` containing `-` / `'` / `&` / `/` (Lucene reserved chars). Skill cannot strip these without changing search semantics.

## History note

This PR replaces #110 (closed). #110 was opened against a stale local ref before noticing that the amazon-analyst pack had already merged into `main` via #100 on 2026-04-23 — that PR ended up trying to re-introduce the entire pack on top of an outdated base, producing 44-file conflicts. This PR is a clean fix-only diff against the latest `main`.

## Test plan

- [x] Cherry-picked from the original fix commit (213cd70) — diff identical to what was reviewed in #110
- [x] APIClaw-Skills test suite for the canonical fix: 45/45 ✅
- [ ] Smoke run amazon-analyst end-to-end on the deep-leaf prompt that triggered the bug

🤖 Generated with [Claude Code](https://claude.com/claude-code)



---

## fix(vibe-drama): prevent NO_REPLY swallowing CTAs after delivery + harden long-task monitoring (#109)

- **SHA**: `d94d2c0dc1febd1282d8614235c4c0f974db0324`

- **作者**: david-srp

- **时间**: 2026-04-28T07:49:15Z


### 完整 Commit Message
```
fix(vibe-drama): prevent NO_REPLY swallowing CTAs after delivery + harden long-task monitoring (#109)

Root cause: LLM selected NO_REPLY at phase boundaries while emitting "下一步: 用户确认"
text. Deliver layer drops NO_REPLY turn content, so users saw the video but never the
follow-up CTA, leaving the conversation stuck.

Changes:
- AGENTS.md: add Reply protocol (NO_REPLY allowed vs forbidden) + long-task monitoring
  rule (announce-yield-report).
- SKILL.md: rewrite Progress anchor section to clarify anchor lives only in visible
  replies; add top-level Reply protocol + Long-running task monitoring sections.
- SKILL.md Phase 5b/5c/6/7: bind every content delivery to a same-turn explicit CTA;
  forbid splitting media + question across turns; forbid NO_REPLY at delivery moments.
- references/repair-playbook.md: add failure class #13 "silent turn — CTA swallowed by
  NO_REPLY" with recovery script and prevention checklist.
- agent-pack.yaml: 1.0.9 → 1.0.10.

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```


### PR #109 Body
## 背景：用户视角的 \"agent 沉默\" 问题

实际症状（来自一次完整短剧生产 transcript 的诊断）：
1. agent 在 Phase 7 用 message tool 把第 1 集成片视频发给用户 — 用户看到视频
2. 紧接着 agent 在同一会话里输出 \`📍 阶段7 交付完成 | 已完成: ... | 下一步: 用户确认 → 第2集或修改\`，但选择了 \`NO_REPLY\` 模式
3. **deliver 层把 NO_REPLY turn 的所有文本（含\"请确认\"CTA）丢弃**
4. 用户只看到视频，没看到任何后续提问 → 不知道要回什么 → 对话死锁
5. 同一 transcript 中此模式重复 12 次，整段单次等待峰值 52 分钟

根因不是 OpenClaw runtime bug，是 **skill prompt 没有约束 LLM 何时不该用 NO_REPLY**。

## 修复（4 个文件，纯 prompt 工程，无代码）

### 1. \`AGENTS.md\` — 加 Reply protocol + long-task monitoring 段
- 明确 NO_REPLY 何时合法（仅纯空闲等 runtime 事件）vs 何时禁止（任何含问题/选项/CTA 的 turn）
- 5 条独立的 \"forbidden uses\" 列表，命中其一就必须 visible reply
- spawn → yield → 报告的强制三段式

### 2. \`SKILL.md\` — 顶部新增两节、改写 anchor 节
- **Reply protocol** 段：表格形式列两种停止模式 + 5 条 NO_REPLY 禁用条件 + \"如果用户什么也看不到，对话会卡住吗\"自检话术 + 一旦发生后的恢复脚本
- **Long-running task monitoring** 段：spawn 前 announce（含 wall-time 估计） / yield 期间禁止 NO_REPLY ping / yield 返回后必须 visible reply 报告每个 sub-agent 状态 + 失败分类 + 单一明确 CTA / 超 1.5× 估计需主动状态更新 / 失败不允许静默 retry
- **Progress anchor rule** 改写：anchor 只活在 visible reply 内；CTA 必须用自然语言提问，不靠 anchor 隐式表达

### 3. \`SKILL.md\` Phase 5b / 5c / 6 / 7 — 每个交付时刻显式绑定 CTA
- Phase 5b/c：图片送达和\"是否锁定/重生成\"提问必须同一可见 turn
- Phase 6 step 4-5：announce-spawn-yield-report 完整序列；4 段 beat 出齐与\"审阅 vs 拼接\"提问绑同 turn
- Phase 7 step 4：成片视频和\"是否满意 / 进下一集 / 重做\"提问绑同 turn，明确禁止只发视频留 NO_REPLY anchor

### 4. \`references/repair-playbook.md\` — 失败分类新增 #13
\"silent turn — CTA swallowed by NO_REPLY\" 失败类，含：症状识别、即时恢复脚本（用户终于发消息时怎么补救）、预防 checklist。

### 版本号
\`agent-pack.yaml\` 1.0.9 → 1.0.10

## 用户价值

| 场景 | 修复前 | 修复后 |
|------|--------|--------|
| Phase 7 出片后 | 用户看到视频，agent 沉默，对话死锁 | 视频 + \"满意吗？进下一集还是重做？\" 同一条消息 |
| Phase 5/6 spawn 4 个 sub-agent | yield 期间 + 完成后都可能静默 | 必须 announce 起跑、必须报告每个 beat 状态 + 失败原因 + CTA |
| 长任务超时 | 默默等不告知 | 1.5× 估计后主动状态更新 |
| 已经发生 NO_REPLY 吞 CTA | 用户被迫猜怎么唤醒 | repair-playbook 给出标准恢复话术 |

## Test plan

- [ ] 跑一遍完整短剧生产流程，观察 Phase 5/6/7 每次 \`sessions_yield\` 返回都收到可见 reply
- [ ] 故意触发 Beat 失败（如歌词内容触发 audio safety），确认 agent 报告失败而不是静默 retry
- [ ] 观察任何 NO_REPLY turn 的内容，应仅包含纯空闲（无 CTA、无 anchor 依赖用户输入）
- [ ] 老用户对话回归：上一轮以 NO_REPLY 收尾的会话，下一次唤醒能否正确补回 CTA

🤖 Generated with [Claude Code](https://claude.com/claude-code)


