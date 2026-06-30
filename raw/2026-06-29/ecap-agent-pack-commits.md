# ecap-agent-pack commits — 2026-06-29


共 2 个 commit


---

## feat(agent-studio): avatar prompt → photorealistic human portrait (#194)

- **SHA**: `97bb4fa59a1be5e8ebf5fea33bfe3bae3bb277e8`
- **作者**: felix-srp
- **日期**: 2026-06-29T14:34:07Z
- **PR**: #194

### 完整 Commit Message

```
feat(agent-studio): avatar prompt → photorealistic human portrait (#194)

Replace the Pixar-animal-mascot avatar prompt with a photorealistic human studio-portrait prompt driven by {role}. Remove the now-unused `animal` field from description.json (schema doc + generator) and its packaging guidance — the claw-interface pack path never reads it (catalog animal is sourced from agent_id), so it's backward compatible. Bumps agent-studio 2.2.1 -> 2.2.2.
```

### PR Body

Replaces the avatar-generation prompt for new packs with a **photorealistic human portrait**, and removes the now-unused `animal` field from `description.json`.

## What changed
- **`templates/avatar-prompt.md`** — swapped the Pixar-style anthropomorphic-**animal** mascot prompt for a **photorealistic human studio portrait** driven by `{role}`. Adopts a clean studio-headshot aesthetic (simple theme-colored backdrop, premium lighting, anti-clutter/anti-text guardrails). Drops the animal/lanyard-prop and the team-distinctness lines (agent-studio generates a *single* pack avatar, not a roster).
- **`references/packaging.md`** — Stage 5b instruction now says `replace {role}` (was `{animal} / {role}`); dropped the `animal` TODO listing-field.
- **`references/description-schema.ts`** + **`scripts/generate_description.py`** — removed the `animal` field from the description.json schema doc and generator.

## Why removing `animal` is safe (backward compatible)
- **No producer requirement:** `validate.py` only checks description.json *exists*; `package.py` only checks `agentPack_id` matches the manifest and ships it as-is. Nothing requires `animal`.
- **No strict schema:** `description-schema.ts` is a reference doc for the Studio LLM, not a runtime validator — existing packs that still carry `animal` aren't rejected (it's an ignored extra field). Verified across the import→package→description.json round-trip.
- **No consumer:** the `claw-interface` pack-ingestion path never reads `animal` (`schema/pack.py` doesn't declare it → ignored on parse). The native Zoo-catalog `animal` (used by the frontend fallback avatar) is sourced from `agent_id`, **not** from the pack's `description.json`.

## Verification
- Full agent-studio test suite green (117 skill-root + 12 package tests); no test referenced `animal`.
- `py_compile` clean on the generator.

Note: this is independent of the KB capability PR (#193) — separate concern, separate branch off `main`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(agent-studio): creator knowledge-base (RAG) — build at authoring, ship pre-built, large-book ready (#193)

- **SHA**: `40403c27b0af26728196a1d197142c01f2b9bb72`
- **作者**: felix-srp
- **日期**: 2026-06-29T14:17:46Z
- **PR**: #193

### 完整 Commit Message

```
feat(agent-studio): creator knowledge-base (RAG) — build at authoring, ship pre-built, large-book ready (#193)

Deterministic creator-owned KB (RAG): build the index once at authoring time in Studio, ship it pre-built in the pack, query at runtime with numpy-only deps. Flat-numpy cosine store, heading-aware CJK-safe chunking, image captioning, content-addressed incremental rebuilds. Large-book hardening (URL --source, concurrent+retried embed, resumable captioning). Source-output policy lets the agent quote the creator's own passages verbatim. 57 KB tests; bumps agent-studio 2.1.1 -> 2.2.1.
```

### PR Body

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

