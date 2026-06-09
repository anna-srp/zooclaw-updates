# SerendipityOneInc/ecap-agent-pack — 2026-06-08 commits

共 2 个 commit

## [99e58bf] fix(pptx-master): 堵住 Design DNA 门的"倒填"漏洞 (v2.2.1) (#167)

- **SHA**: 99e58bf6f0c8ec163bf212ed6a1b82ac0931ba7c
- **作者**: david-srp
- **日期**: 2026-06-08T11:23:42Z
- **PR**: #167
- **URL**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/99e58bf6f0c8ec163bf212ed6a1b82ac0931ba7c

### 完整 Commit Message

```
fix(pptx-master): 堵住 Design DNA 门的"倒填"漏洞 (v2.2.1) (#167)

实战发现 v2.2.0 的 DNA 硬门可被绕过：用 fidelity: reduced 跳过完整判断，
先拍脑袋定配色再补写 DNA 凑数（palette 写 data 但产物是蓝+金），validate_dna 仍放行。
根因：一致性检查可选、且只查字体不查配色；reduced 成了万能旁路。

- 配色一致性（核心）：交付校验要求声明 palette 的 primary hex 必须出现在产物里
- 强制化：新增 --delivery 模式，强制 --output <deck>，交付前必带产物校验
- reduced 不再是旁路：palette + font_pair 任何 fidelity 下都必填
- skin/brand 豁免：换肤/品牌锁定需 provenance.skin_source/brand 显式声明才跳过配色检查
- 顺序铁律：AGENTS.md + judgment-chain.md 明确"先判断后建，禁止反向倒填"
- test_dna 11→16（新增配色不符/reduced缺palette/skin豁免/交付缺output 等）；全套件 125 全绿

Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>
```

### PR Description

## 这个 PR 在做什么？（一句话）

修复上一个 PR（#166，v2.2.0 已合入）引入的 Design DNA 硬门的**"倒填"漏洞**：那道"判断必须留痕"的关卡**能被绕过**。

> 接续 #166（v2.2.0 架构重构 + Design DNA 硬门）。这是它的安全补丁 v2.2.1。

## 背景：漏洞是什么（实战发现）

v2.2.0 给设计判断加了硬门——必须产出 `data/design-dna.json` 并过 `validate_dna.py` 才能交付。但实测发现 agent 能绕过它：

> 用 `fidelity: reduced` 跳过完整判断，**先拍脑袋定配色（深海蓝+金）再补写 DNA 凑数**，DNA 写 `palette: data`(#0D9488 青绿) 但产物实际渲染蓝+金——`validate_dna.py` 仍然放行。

**三个洞**：
1. 一致性检查是**可选**的（`--output` 可省）→ agent 只验工件结构就放行。
2. 即使检查也**只查字体、不查配色** → 声明 data 却用蓝+金查不出来。
3. `fidelity: reduced` 是**万能旁路**（连 `palette` 都不要求）。

**本质**：v2.2.0 只校验了工件**自身**结构，没校验工件 ⟺ 产物**是否一致**。

## 修复（让"先拍脑袋后倒填"失去意义）

- **配色一致性（核心）**：交付校验要求"声明 palette 的 primary hex 必须出现在产物里"。声明 data 却渲染蓝+金 → 当场判不一致、HALT。
- **强制化**：新增 `--delivery` 模式，**强制 `--output <deck>`**，交付前必带产物校验、不可跳过。
- **`reduced` 不再是旁路**：`palette` + `font_pair` 在任何 fidelity 下都必填；reduced 只能省 `content_relationship`/`context_density`，不能省配色/字体判断。
- **skin/品牌豁免**：配色来自换肤或品牌锁定时，需 `provenance.skin_source`/`provenance.brand` 显式声明才跳过配色检查（避免误杀换肤 deck）。
- **顺序铁律**：`AGENTS.md` 交付门 + `judgment-chain.md` 明确"先查 judgment.yaml 得 DNA → 再据此建 deck，禁止反向倒填"。

## 怎么验证（可复跑）

```bash
cd pptx-master
python3 tests/test_dna.py   # 16 pass —— 含 "★ 配色不符(倒填案例)被拒"
python3 tests/test_pack.py  # 73 pass
python3 tests/test_extra.py # 36 pass
```
- 你这个实战原案现在是一条测试：`★ color mismatch (deck colors ≠ declared palette) rejected — the back-fill case`。
- 全套件 **125 测试全绿**（73 + 36 + 16）。

## 诚实的边界
这把"声明 palette 必须与产物一致"焊死了——倒填一个对不上的配色已不可能。残留缝隙：agent 仍可能"凭感觉选了一个真实存在的 palette"而非严格走 judgment.yaml 推导，只要产物与之一致就能过。要再收紧可加"判断输入（受众/场景/主题）交叉核对"，但更重、更易误杀，留待下轮评估。

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## [42caafc] fix(founder-ip-studio): bump ws to 8.20.1 (CVE-2026-45736) (#161)

- **SHA**: 42caafcac441930a08a8464ef27b0faf4d0f8567
- **作者**: felix-srp
- **日期**: 2026-06-08T08:38:40Z
- **PR**: #161
- **URL**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/42caafcac441930a08a8464ef27b0faf4d0f8567

### 完整 Commit Message

```
fix(founder-ip-studio): bump ws to 8.20.1 (CVE-2026-45736) (#161)

ws@8.17.1 (transitive via @remotion/renderer's exact 8.17.1 pin) is
affected by GHSA-58qx-3vcg-4xpx — WebSocket.close() discloses
uninitialized memory when a TypedArray is passed as the close reason
(fixed in 8.20.1). Force the patched version with an npm override and
regenerate the lockfile. Incidental "peer": true metadata churn is from
npm 11 regenerating the file; no resolved versions change besides ws.

Co-authored-by: Ning Hu <ning@gensmo.ai>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Resolves Dependabot alert #1 (moderate). `ws@8.17.1` — pulled in transitively by `@remotion/renderer@4.0.459` (which pins `ws` to exactly `8.17.1`) in `founder-ip-studio/.agents/skills/founder-post/remotion-project` — is affected by **CVE-2026-45736 / GHSA-58qx-3vcg-4xpx**: `WebSocket.close()` discloses uninitialized heap memory when a `TypedArray` is passed as the close reason. Fixed in **ws@8.20.1**.

Because the parent pins `ws` exactly, a plain Dependabot bump can't move it — so this forces the patched version via an npm `overrides` entry and regenerates the lockfile.

## Changes

- `remotion-project/package.json`: add `"overrides": { "ws": "8.20.1" }`
- `remotion-project/package-lock.json`: `ws` resolves to `8.20.1`. The incidental removal of `"peer": true` metadata flags on a handful of packages is from npm 11 regenerating the lockfile — **no resolved versions change besides `ws`**.

## Risk / context

Low. In this project `ws` is used by Remotion's renderer as a **localhost IPC client** to the headless compositor — not a network-facing server, and neither this project nor Remotion passes a `TypedArray` close-reason. The advisory's CVSS (4.4, `AC:H/PR:H`) requires control over the server-side `close()` call. The bump is a same-major patch, API-compatible with the renderer's `8.17.1` expectation.

## Test plan

- [x] `npm install --package-lock-only` regenerates cleanly; `--dry-run` reports "up to date" (lockfile ⇄ package.json consistent)
- [ ] Dependabot alert #1 auto-closes once merged to `main`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

