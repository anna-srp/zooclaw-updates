---
title: "Agent Studio 新增创作者知识库（RAG）：可基于专属内容问答"
type: "Skill 上架/更新"
priority: "高"
date: "2026-06-29"
status: "待审核"
channels: ""
---

# Agent Studio 新增创作者知识库（RAG）：可基于专属内容问答

## 核心宣传点

创作者现在可以为自己的 Agent 配置专属知识库：在 Studio 创作时一次性构建索引并随包发布，用户提问时 Agent 能基于创作者的原始内容（书籍/文档/图片）精准引用作答，支持大部头书籍、中文友好分块，让"懂你内容"的专属 Agent 成为可能。

## 原始内容

### Commit Message

```
feat(agent-studio): creator knowledge-base (RAG) — build at authoring, ship pre-built, large-book ready (#193)

Deterministic creator-owned KB (RAG): build the index once at authoring time in Studio, ship it pre-built in the pack, query at runtime with numpy-only deps. Flat-numpy cosine store, heading-aware CJK-safe chunking, image captioning, content-addressed incremental rebuilds. Large-book hardening (URL --source, concurrent+retried embed, resumable captioning). Source-output policy lets the agent quote the creator's own passages verbatim. 57 KB tests; bumps agent-studio 2.1.1 -> 2.2.1.
```

### PR Description

Adds a first-class **creator-owned knowledge-base (RAG)** capability to Agent Studio. Today KB agents are LLM-improvised (the Sky老思 production case improvised ChromaDB + OpenAI embeddings — it works but ships broken: the index isn't packaged and onboarding wrongly asks fans for the source PDF). This makes it deterministic: **build the index once at authoring time in Studio, ship it pre-built in the pack, query it at runtime with numpy-only deps.**

## What's here
- **`templates/knowledge-qa/query_kb.py`** (ships in generated packs, runtime): cosine top-k over a flat `vectors.npz`; query embedding via `openclaw infer embedding create --json`; threshold-gated; figure-image passthrough for display; degrades any load/embed failure to structured JSON (never a traceback). Invoked via `uv run --python 3.12 --with numpy …` so numpy is self-provided at query time (no onboarding install).
- **`templates/knowledge-qa/build_kb.py`** (Studio-only authoring tool, via `uv run --with`): heading-aware recursive chunking (~450 tok / 64 overlap, CJK-safe); PDF/MD/DOCX extraction; image extraction + vision captioning; OpenAI-SDK embedding (`text-embedding-3-small`, L2-normalized); **content-addressed incremental rebuilds** — position-independent chunk ids, caption cache by image hash, embedding-dimension validation.
- **`templates/knowledge-qa/SKILL.md.tmpl`** + **`references/knowledge-base.md`** + flow wiring (`references/skill-design.md`): minimal model-invoked retrieval skill, source-protection in the base prompt, `.agents/skills/<kb>/kb/` placement (hidden from the end-user file browser, ships once the skill is declared in the manifest).

## Large-book support
Hardened for real books (a staging finding motivated this), and **validated on a 28 MB book in the 2.2.1 staging build**:
- **`--source <url>`** — stream-download an http(s) book too large for the workspace upload limit (bounded memory; collision-safe per-source temp dirs; type resolved by URL → Content-Type → magic-byte sniff).
- **Concurrent + retried embedding** — token-aware batches + bounded thread pool + `max_retries` backoff, so a transient 429 doesn't abort a long build.
- **Concurrent + resumable captioning** — figures captioned in parallel and checkpointed to a `captions.jsonl` sidecar; a killed/timed-out build resumes the vision work instead of restarting. An un-captionable figure (empty vision reply) is dropped and retried next build — never embedded empty.

## Source protection (the creator's own content)
A staging Pack Test exposed the gap: a creator's digital-avatar agent **refused to share the creator's own book excerpts** when a fan asked "what does the book actually say," citing copyright and deflecting the fan to *buy the book* — which defeats the avatar's whole purpose. The base-prompt rule now:
- reframes the KB as the agent's **own work, shared with permission** (first person), so the model stops treating it as third-party copyrighted text;
- explicitly **forbids declining on copyright grounds** and **deflecting to "go buy it"**;
- keeps the guardrail — **never export/dump the whole KB** or reconstruct large continuous spans.

(This is template guidance for packs built *with* the new KB capability; an existing improvised pack like Sky老思 needs its own base prompt updated, or a rebuild on this template.)

## Design decisions (researched; design-doc vault)
Flat-numpy store (no ANN — exact cosine is fine to tens of thousands of chunks); embeddings via the platform proxy (only `text-embedding-3-small` exists); native OpenClaw memory rejected (conversational-only, can't ship pre-built); model-invoked retrieval (packs can't pre-turn-inject without a plugin); build-at-authoring + ship-in-pack fixes the distribution bug.

## Verification
- **57 KB tests** passing (`scripts/tests/test_kb_{build,query,packaging,integration}.py`).
- **Reviewed** — multiple two-reviewer (Claude + Codex) correctness rounds + `/simplify` + token-trim passes; all findings fixed (the embedding-envelope blocker, CJK no-whitespace split, incremental-id collisions, dimension-drift, runtime resilience, empty captions, same-basename URL collision). MD trims preserved every directive + test needle (two-reviewer-checked).
- **Smoke-tested in the `openclaw-docker:2026.6.6` devcontainer** — `uv run --with numpy query_kb.py` provisions numpy and runs the cosine/argpartition path end-to-end; the `openclaw infer embedding create --json` envelope is **confirmed from the CLI source** (embedding at `outputs[0].embedding`).
- **Staging** — large-book build validated on a 28 MB book in the 2.2.1 deploy.

## Notes (not blockers)
- **URL-source pod egress** — `--source <url>` uses raw `urllib` from the build subprocess. It **fails closed**: if pod egress is blocked it errors clearly and the creator just uploads the file (large books also fall back to split-into-<25 MB-parts + incremental build). Not a merge blocker.

## Deferred (intentionally not here)
`chunks.jsonl` at-rest obfuscation; a platform pre-turn-injection plugin (would remove the model-invoked round-trip for all KB agents); faiss-cpu (no ANN needed in-envelope).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

