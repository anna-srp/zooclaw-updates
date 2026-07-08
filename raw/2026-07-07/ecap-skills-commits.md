# ecap-skills — 2026-07-07 commits

## fix(docx): separate content from code in Pipeline A + scoped CJK quote rules (#233)

- **SHA**: 9a6e873e9cb71d6262962b88f2beb0bbc946566b
- **作者**: felix-srp
- **日期**: 2026-07-07T12:29:22Z
- **PR**: #233

### Commit Message

```
fix(docx): separate content from code in Pipeline A + scoped CJK quote rules (#233)

## Summary

Hardens the docx skill's Pipeline A (create via docx-js) guidance
against a failure observed in prod (bot `8ad69d30`, 2026-07-07): the
agent inlined the entire Chinese document body into JS string literals,
using ASCII `"` as Chinese quotation marks. The quotes terminated the
literals and the generator crashed twice with `SyntaxError: missing )
after argument list`, e.g.:

```js
body("……他们能用于"经营管理"的时间，每天不超过 15 分钟……")
//              ↑ ASCII quote ends the string literal
```

The agent eventually recovered by switching to pandoc, but the skill
guidance never told it not to do this in the first place.

## Changes

- **`docx/SKILL.md`** — new CRITICAL rule in Pipeline A: write body
content to a standalone MD (preferred — no escaping) or JSON file
(quoted heredoc) and `fs.readFileSync` it from the generator script;
never inline body text in JS string literals. Chinese prose quotes are
full-width; code/JSON literals keep ASCII quotes.
- **`docx/references/critical_rules.md`** — docx-js rule **17**:
content/code separation with the exact failure signature; MD needs no
escaping, JSON quotes escape as `\"`, hand-written `\uXXXX` escapes are
banned (transcription errors silently corrupt characters). Rule **18**:
Chinese *prose* quotation marks are full-width “”/「」; literals (code,
JSON, CLI, product names, quoted English) keep their ASCII quotes
verbatim.
- **`docx/references/cjk_typography.md`** — quotes table row annotated
(curly vs ASCII); scoped warning: full-width quotes apply to prose only,
literal content is preserved verbatim, and inlined ASCII quotes crash
generator scripts.

Content/code separation kills the entire quote-escaping failure class
regardless of language; the quote-style rule is scoped to prose so
agents never rewrite valid literal content (codex review round 2).

## Review rounds

1. Quotes-table ambiguity → table annotated (`1d428ed`).
2. `REQUEST_CHANGES`: blanket ASCII-quote ban could corrupt literals
like `{"mode":"fast"}` → rule scoped to prose with explicit literal
exemption (`b234dc4`).
3. E2E finding: agent hand-wrote `\uXXXX` escapes in its content JSON
and silently corrupted three characters (值→値, 摊→戡, 钮→鈕) → MD preferred,
`\uXXXX` banned (`4d481c3`).
4. Final rounds: APPROVE, no findings.

## Validation

- `.github/scripts/lint_skills.py` passes (exit 0, no docx findings).
- Devcontainer end-to-end (`openclaw agent --local`, staging bot, this
branch's skills mounted, quote-baited Chinese prompt forced through
Pipeline A): agent read the new guidance and planned content/code
separation unprompted; the prod `SyntaxError` failure mode did not
occur; prose quotes rendered full-width, `{"mode":"fast"}` and `"AI
Mode"` preserved verbatim; `validate.py` all passed.
- Docs-only change; no script behavior touched.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01V9aBDojAYRAHSUDFrudXE6

---------

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
Co-authored-by: claude[bot] <41898282+claude[bot]@users.noreply.github.com>
Co-authored-by: undefined <undefined@users.noreply.github.com>
```

### PR Body

## Summary

Hardens the docx skill's Pipeline A (create via docx-js) guidance against a failure observed in prod (bot `8ad69d30`, 2026-07-07): the agent inlined the entire Chinese document body into JS string literals, using ASCII `"` as Chinese quotation marks. The quotes terminated the literals and the generator crashed twice with `SyntaxError: missing ) after argument list`, e.g.:

```js
body("……他们能用于"经营管理"的时间，每天不超过 15 分钟……")
//              ↑ ASCII quote ends the string literal
```

The agent eventually recovered by switching to pandoc, but the skill guidance never told it not to do this in the first place.

## Changes

- **`docx/SKILL.md`** — new CRITICAL rule in Pipeline A: write body content to a standalone MD (preferred — no escaping) or JSON file (quoted heredoc) and `fs.readFileSync` it from the generator script; never inline body text in JS string literals. Chinese prose quotes are full-width; code/JSON literals keep ASCII quotes.
- **`docx/references/critical_rules.md`** — docx-js rule **17**: content/code separation with the exact failure signature; MD needs no escaping, JSON quotes escape as `\"`, hand-written `\uXXXX` escapes are banned (transcription errors silently corrupt characters). Rule **18**: Chinese *prose* quotation marks are full-width “”/「」; literals (code, JSON, CLI, product names, quoted English) keep their ASCII quotes verbatim.
- **`docx/references/cjk_typography.md`** — quotes table row annotated (curly vs ASCII); scoped warning: full-width quotes apply to prose only, literal content is preserved verbatim, and inlined ASCII quotes crash generator scripts.

Content/code separation kills the entire quote-escaping failure class regardless of language; the quote-style rule is scoped to prose so agents never rewrite valid literal content (codex review round 2).

## Review rounds

1. Quotes-table ambiguity → table annotated (`1d428ed`).
2. `REQUEST_CHANGES`: blanket ASCII-quote ban could corrupt literals like `{"mode":"fast"}` → rule scoped to prose with explicit literal exemption (`b234dc4`).
3. E2E finding: agent hand-wrote `\uXXXX` escapes in its content JSON and silently corrupted three characters (值→値, 摊→戡, 钮→鈕) → MD preferred, `\uXXXX` banned (`4d481c3`).
4. Final rounds: APPROVE, no findings.

## Validation

- `.github/scripts/lint_skills.py` passes (exit 0, no docx findings).
- Devcontainer end-to-end (`openclaw agent --local`, staging bot, this branch's skills mounted, quote-baited Chinese prompt forced through Pipeline A): agent read the new guidance and planned content/code separation unprompted; the prod `SyntaxError` failure mode did not occur; prose quotes rendered full-width, `{"mode":"fast"}` and `"AI Mode"` preserved verbatim; `validate.py` all passed.
- Docs-only change; no script behavior touched.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01V9aBDojAYRAHSUDFrudXE6
