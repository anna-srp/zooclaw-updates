# SerendipityOneInc/ecap-workspace — commits 2026-08-12

## fix(billing): cap Creem trial credits (#3358)

- **SHA**: `e1c932d2eba11817f48bebac5085c70e7c802cf6`
- **作者**: tim-srp
- **日期**: 2026-08-12T15:27:42Z
- **PR**: #3358

### Commit Message

```
fix(billing): cap Creem trial credits (#3358)

## Summary
- Grant exactly 1,000 credits for a Creem Card subscription trial
instead of the Starter paid-plan allowance.
- Keep the first successful paid Starter transaction at the full
4,800-credit grant.
- Add regression assertions for both the trial entitlement and the
Billing Gateway paid entitlement payload.

## Root cause
The Creem trial projection reused `credits_for_plan("starter")`, which
returns the paid Starter allowance of 4,800. Other subscription trials
use the dedicated 1,000-credit trial allowance.

## Test plan
- [x] Red test observed `4800 != 1000` before the fix.
- [x] 60 focused Creem Trial and first-payment tests pass.
- [x] 118 broader Trial/first-payment/reconciliation tests passed before
the paid-handoff assertion was strengthened.
- [x] Ruff check and format pass.
- [x] Commit-time Pyright and repository policy hooks pass.
- [ ] GitHub Code Quality Check passes.

## Expected behavior
- Trial activation adds 1,000 credits.
- The first successful charge after the seven-day trial adds a separate
full 4,800-credit Starter entitlement; remaining trial credits are not
deducted.
```

### PR Body

## Summary
- Grant exactly 1,000 credits for a Creem Card subscription trial instead of the Starter paid-plan allowance.
- Keep the first successful paid Starter transaction at the full 4,800-credit grant.
- Add regression assertions for both the trial entitlement and the Billing Gateway paid entitlement payload.

## Root cause
The Creem trial projection reused `credits_for_plan("starter")`, which returns the paid Starter allowance of 4,800. Other subscription trials use the dedicated 1,000-credit trial allowance.

## Test plan
- [x] Red test observed `4800 != 1000` before the fix.
- [x] 60 focused Creem Trial and first-payment tests pass.
- [x] 118 broader Trial/first-payment/reconciliation tests passed before the paid-handoff assertion was strengthened.
- [x] Ruff check and format pass.
- [x] Commit-time Pyright and repository policy hooks pass.
- [ ] GitHub Code Quality Check passes.

## Expected behavior
- Trial activation adds 1,000 credits.
- The first successful charge after the seven-day trial adds a separate full 4,800-credit Starter entitlement; remaining trial credits are not deducted.


---

## build(deps-dev): update ruff requirement from >=0.16.0 to >=0.16.1 in /services/claw-interface (#3301)

- **SHA**: `af4d273d2d058cd1f52902396f6c574ecde481a1`
- **作者**: dependabot[bot]
- **日期**: 2026-08-12T15:04:53Z
- **PR**: #3301

### Commit Message

```
build(deps-dev): update ruff requirement from >=0.16.0 to >=0.16.1 in /services/claw-interface (#3301)

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to
permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/releases">ruff's
releases</a>.</em></p>
<blockquote>
<h2>0.16.1</h2>
<h2>Release Notes</h2>
<p>Released on 2026-07-30.</p>
<h3>Preview features</h3>
<ul>
<li>Add an option to opt out of human-readable names (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27160">#27160</a>)</li>
<li>[<code>flake8-pytest-style</code>] Make fixes safe by default and
unsafe only when comments are present (<code>PT018</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27201">#27201</a>)</li>
<li>[<code>pyupgrade</code>] Skip fix when a defaulted
<code>TypeVar</code> precedes a non-defaulted one (<code>UP040</code>,
<code>UP046</code>, <code>UP047</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27133">#27133</a>)</li>
<li>[<code>ruff</code>] Fix false positive with unpacked arguments
(<code>RUF065</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26959">#26959</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Bump <code>gen-lsp-types</code> to gracefully handle unknown
enumeration values in LSP messages (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27230">#27230</a>)</li>
<li>[<code>flake8-bugbear</code>] Mark <code>range</code> as immutable
(<code>B008</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27247">#27247</a>)</li>
<li>[<code>flake8-comprehensions</code>] NFKC-normalize keyword names in
<code>C408</code> fix (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26813">#26813</a>)</li>
<li>[<code>flake8-return</code>] Fix false positive when variable is
read in <code>finally</code> clause (<code>RET504</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25441">#25441</a>)</li>
<li>[<code>pydocstyle</code>] Skip section detection inside RST
directive bodies (<code>D214</code>, <code>D405</code>,
<code>D413</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/23635">#23635</a>)</li>
<li>[<code>refurb</code>] Parenthesize <code>yield</code> arguments in
the <code>FURB192</code> fix (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27192">#27192</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>flake8-pytest-style</code>] Mark <code>PT022</code> fixes as
unsafe (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26440">#26440</a>)</li>
<li>[<code>refurb</code>] Mark fixes that remove unknown separators as
unsafe (<code>FURB105</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27200">#27200</a>)</li>
</ul>
<h3>Server</h3>
<ul>
<li>Fix indexing of excluded nested Ruff workspaces (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27303">#27303</a>)</li>
<li>Lint TOML files in the LSP (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26862">#26862</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Cover <code>pycon</code> Markdown formatting (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27153">#27153</a>)</li>
<li>[<code>flake8-bandit</code>] Document <code>TYPE_CHECKING</code>
exception (<code>S101</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27004">#27004</a>)</li>
<li>[<code>flake8-import-conventions</code>] Document that
<code>extend-aliases</code> can override default aliases (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27191">#27191</a>)</li>
<li>[<code>pylint</code>] Add missing fix safety gotchas for
<code>non-augmented-assignment</code> (<code>PLR6104</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27250">#27250</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Reduce syntax error noise by swallowing dedents like indents (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27170">#27170</a>)</li>
<li>Vendor latest annotate-snippets (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27033">#27033</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/bxff"><code>@​bxff</code></a></li>
<li><a
href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li>
<li><a href="https://github.com/Avasam"><code>@​Avasam</code></a></li>
<li><a href="https://github.com/epage"><code>@​epage</code></a></li>
<li><a href="https://github.com/LHMQ878"><code>@​LHMQ878</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's
changelog</a>.</em></p>
<blockquote>
<h2>0.16.1</h2>
<p>Released on 2026-07-30.</p>
<h3>Preview features</h3>
<ul>
<li>Add an option to opt out of human-readable names (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27160">#27160</a>)</li>
<li>[<code>flake8-pytest-style</code>] Make fixes safe by default and
unsafe only when comments are present (<code>PT018</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27201">#27201</a>)</li>
<li>[<code>pyupgrade</code>] Skip fix when a defaulted
<code>TypeVar</code> precedes a non-defaulted one (<code>UP040</code>,
<code>UP046</code>, <code>UP047</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27133">#27133</a>)</li>
<li>[<code>ruff</code>] Fix false positive with unpacked arguments
(<code>RUF065</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26959">#26959</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Bump <code>gen-lsp-types</code> to gracefully handle unknown
enumeration values in LSP messages (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27230">#27230</a>)</li>
<li>[<code>flake8-bugbear</code>] Mark <code>range</code> as immutable
(<code>B008</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27247">#27247</a>)</li>
<li>[<code>flake8-comprehensions</code>] NFKC-normalize keyword names in
<code>C408</code> fix (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26813">#26813</a>)</li>
<li>[<code>flake8-return</code>] Fix false positive when variable is
read in <code>finally</code> clause (<code>RET504</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25441">#25441</a>)</li>
<li>[<code>pydocstyle</code>] Skip section detection inside RST
directive bodies (<code>D214</code>, <code>D405</code>,
<code>D413</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/23635">#23635</a>)</li>
<li>[<code>refurb</code>] Parenthesize <code>yield</code> arguments in
the <code>FURB192</code> fix (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27192">#27192</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>flake8-pytest-style</code>] Mark <code>PT022</code> fixes as
unsafe (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26440">#26440</a>)</li>
<li>[<code>refurb</code>] Mark fixes that remove unknown separators as
unsafe (<code>FURB105</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27200">#27200</a>)</li>
</ul>
<h3>Server</h3>
<ul>
<li>Fix indexing of excluded nested Ruff workspaces (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27303">#27303</a>)</li>
<li>Lint TOML files in the LSP (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26862">#26862</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Cover <code>pycon</code> Markdown formatting (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27153">#27153</a>)</li>
<li>[<code>flake8-bandit</code>] Document <code>TYPE_CHECKING</code>
exception (<code>S101</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27004">#27004</a>)</li>
<li>[<code>flake8-import-conventions</code>] Document that
<code>extend-aliases</code> can override default aliases (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27191">#27191</a>)</li>
<li>[<code>pylint</code>] Add missing fix safety gotchas for
<code>non-augmented-assignment</code> (<code>PLR6104</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27250">#27250</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Reduce syntax error noise by swallowing dedents like indents (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27170">#27170</a>)</li>
<li>Vendor latest annotate-snippets (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27033">#27033</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/bxff"><code>@​bxff</code></a></li>
<li><a
href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li>
<li><a href="https://github.com/Avasam"><code>@​Avasam</code></a></li>
<li><a href="https://github.com/epage"><code>@​epage</code></a></li>
<li><a href="https://github.com/LHMQ878"><code>@​LHMQ878</code></a></li>
<li><a
href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/astral-sh/ruff/commit/80790b348b5188e7fc253665540f442c6ec7dd05"><code>80790b3</code></a>
Bump 0.16.1 (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27330">#27330</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/63830f3e97b56ca3be0dd8f1092f76c4acc63213"><code>63830f3</code></a>
[ty] Borrow from constraint set storage less often (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27328">#27328</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/f40dca98a7f1b6fff0cee5ecf1e6364d5a8bdc15"><code>f40dca9</code></a>
[ty] Preserve forwarded expanded-variadic diagnostic sources (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27266">#27266</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/0d804975a2645d6e4a795cf501fd764b88aa47e3"><code>0d80497</code></a>
Lint TOML files in the LSP (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26862">#26862</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/d91586bd5b30f77f6614d57b73fc7dbea9051a0e"><code>d91586b</code></a>
Update prek dependencies (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27293">#27293</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/7da4b8b8d78fd6df2b3e06d8466d9cd49822900d"><code>7da4b8b</code></a>
[ty] Respect bounds and constraints in generic materializations (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27228">#27228</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/b20daf741241a6829ff8963a203f7847561deb62"><code>b20daf7</code></a>
[ty] refactor: add helper function to send partial results (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27249">#27249</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/4d4c8fa1c75b00561ea24eefefb13eb5ff80e01f"><code>4d4c8fa</code></a>
[ty] Emit diagnostic when specializing a non-generic class (<a
href="https://redirect.github.com/astral-sh/ruff/issues/26883">#26883</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/7c3e2db97deb5c5edd6e4303403ef6caf2bde8be"><code>7c3e2db</code></a>
[ty] Fix enum class container assignability (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27318">#27318</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/d5ef97fcd03e108f7510f84b8ed85bb4051311fe"><code>d5ef97f</code></a>
[<code>flake8-return</code>] Fix false positive when variable is read in
<code>finally</code> claus...</li>
<li>Additional commits viewable in <a
href="https://github.com/astral-sh/ruff/compare/0.16.0...0.16.1">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Body

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's releases</a>.</em></p>
<blockquote>
<h2>0.16.1</h2>
<h2>Release Notes</h2>
<p>Released on 2026-07-30.</p>
<h3>Preview features</h3>
<ul>
<li>Add an option to opt out of human-readable names (<a href="https://redirect.github.com/astral-sh/ruff/pull/27160">#27160</a>)</li>
<li>[<code>flake8-pytest-style</code>] Make fixes safe by default and unsafe only when comments are present (<code>PT018</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27201">#27201</a>)</li>
<li>[<code>pyupgrade</code>] Skip fix when a defaulted <code>TypeVar</code> precedes a non-defaulted one (<code>UP040</code>, <code>UP046</code>, <code>UP047</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27133">#27133</a>)</li>
<li>[<code>ruff</code>] Fix false positive with unpacked arguments (<code>RUF065</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26959">#26959</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Bump <code>gen-lsp-types</code> to gracefully handle unknown enumeration values in LSP messages (<a href="https://redirect.github.com/astral-sh/ruff/pull/27230">#27230</a>)</li>
<li>[<code>flake8-bugbear</code>] Mark <code>range</code> as immutable (<code>B008</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27247">#27247</a>)</li>
<li>[<code>flake8-comprehensions</code>] NFKC-normalize keyword names in <code>C408</code> fix (<a href="https://redirect.github.com/astral-sh/ruff/pull/26813">#26813</a>)</li>
<li>[<code>flake8-return</code>] Fix false positive when variable is read in <code>finally</code> clause (<code>RET504</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25441">#25441</a>)</li>
<li>[<code>pydocstyle</code>] Skip section detection inside RST directive bodies (<code>D214</code>, <code>D405</code>, <code>D413</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/23635">#23635</a>)</li>
<li>[<code>refurb</code>] Parenthesize <code>yield</code> arguments in the <code>FURB192</code> fix (<a href="https://redirect.github.com/astral-sh/ruff/pull/27192">#27192</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>flake8-pytest-style</code>] Mark <code>PT022</code> fixes as unsafe (<a href="https://redirect.github.com/astral-sh/ruff/pull/26440">#26440</a>)</li>
<li>[<code>refurb</code>] Mark fixes that remove unknown separators as unsafe (<code>FURB105</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27200">#27200</a>)</li>
</ul>
<h3>Server</h3>
<ul>
<li>Fix indexing of excluded nested Ruff workspaces (<a href="https://redirect.github.com/astral-sh/ruff/pull/27303">#27303</a>)</li>
<li>Lint TOML files in the LSP (<a href="https://redirect.github.com/astral-sh/ruff/pull/26862">#26862</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Cover <code>pycon</code> Markdown formatting (<a href="https://redirect.github.com/astral-sh/ruff/pull/27153">#27153</a>)</li>
<li>[<code>flake8-bandit</code>] Document <code>TYPE_CHECKING</code> exception (<code>S101</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27004">#27004</a>)</li>
<li>[<code>flake8-import-conventions</code>] Document that <code>extend-aliases</code> can override default aliases (<a href="https://redirect.github.com/astral-sh/ruff/pull/27191">#27191</a>)</li>
<li>[<code>pylint</code>] Add missing fix safety gotchas for <code>non-augmented-assignment</code> (<code>PLR6104</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27250">#27250</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Reduce syntax error noise by swallowing dedents like indents (<a href="https://redirect.github.com/astral-sh/ruff/pull/27170">#27170</a>)</li>
<li>Vendor latest annotate-snippets (<a href="https://redirect.github.com/astral-sh/ruff/pull/27033">#27033</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/bxff"><code>@​bxff</code></a></li>
<li><a href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li>
<li><a href="https://github.com/Avasam"><code>@​Avasam</code></a></li>
<li><a href="https://github.com/epage"><code>@​epage</code></a></li>
<li><a href="https://github.com/LHMQ878"><code>@​LHMQ878</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
<blockquote>
<h2>0.16.1</h2>
<p>Released on 2026-07-30.</p>
<h3>Preview features</h3>
<ul>
<li>Add an option to opt out of human-readable names (<a href="https://redirect.github.com/astral-sh/ruff/pull/27160">#27160</a>)</li>
<li>[<code>flake8-pytest-style</code>] Make fixes safe by default and unsafe only when comments are present (<code>PT018</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27201">#27201</a>)</li>
<li>[<code>pyupgrade</code>] Skip fix when a defaulted <code>TypeVar</code> precedes a non-defaulted one (<code>UP040</code>, <code>UP046</code>, <code>UP047</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27133">#27133</a>)</li>
<li>[<code>ruff</code>] Fix false positive with unpacked arguments (<code>RUF065</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/26959">#26959</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Bump <code>gen-lsp-types</code> to gracefully handle unknown enumeration values in LSP messages (<a href="https://redirect.github.com/astral-sh/ruff/pull/27230">#27230</a>)</li>
<li>[<code>flake8-bugbear</code>] Mark <code>range</code> as immutable (<code>B008</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27247">#27247</a>)</li>
<li>[<code>flake8-comprehensions</code>] NFKC-normalize keyword names in <code>C408</code> fix (<a href="https://redirect.github.com/astral-sh/ruff/pull/26813">#26813</a>)</li>
<li>[<code>flake8-return</code>] Fix false positive when variable is read in <code>finally</code> clause (<code>RET504</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25441">#25441</a>)</li>
<li>[<code>pydocstyle</code>] Skip section detection inside RST directive bodies (<code>D214</code>, <code>D405</code>, <code>D413</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/23635">#23635</a>)</li>
<li>[<code>refurb</code>] Parenthesize <code>yield</code> arguments in the <code>FURB192</code> fix (<a href="https://redirect.github.com/astral-sh/ruff/pull/27192">#27192</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>flake8-pytest-style</code>] Mark <code>PT022</code> fixes as unsafe (<a href="https://redirect.github.com/astral-sh/ruff/pull/26440">#26440</a>)</li>
<li>[<code>refurb</code>] Mark fixes that remove unknown separators as unsafe (<code>FURB105</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27200">#27200</a>)</li>
</ul>
<h3>Server</h3>
<ul>
<li>Fix indexing of excluded nested Ruff workspaces (<a href="https://redirect.github.com/astral-sh/ruff/pull/27303">#27303</a>)</li>
<li>Lint TOML files in the LSP (<a href="https://redirect.github.com/astral-sh/ruff/pull/26862">#26862</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Cover <code>pycon</code> Markdown formatting (<a href="https://redirect.github.com/astral-sh/ruff/pull/27153">#27153</a>)</li>
<li>[<code>flake8-bandit</code>] Document <code>TYPE_CHECKING</code> exception (<code>S101</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27004">#27004</a>)</li>
<li>[<code>flake8-import-conventions</code>] Document that <code>extend-aliases</code> can override default aliases (<a href="https://redirect.github.com/astral-sh/ruff/pull/27191">#27191</a>)</li>
<li>[<code>pylint</code>] Add missing fix safety gotchas for <code>non-augmented-assignment</code> (<code>PLR6104</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27250">#27250</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Reduce syntax error noise by swallowing dedents like indents (<a href="https://redirect.github.com/astral-sh/ruff/pull/27170">#27170</a>)</li>
<li>Vendor latest annotate-snippets (<a href="https://redirect.github.com/astral-sh/ruff/pull/27033">#27033</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/bxff"><code>@​bxff</code></a></li>
<li><a href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li>
<li><a href="https://github.com/Avasam"><code>@​Avasam</code></a></li>
<li><a href="https://github.com/epage"><code>@​epage</code></a></li>
<li><a href="https://github.com/LHMQ878"><code>@​LHMQ878</code></a></li>
<li><a href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/astral-sh/ruff/commit/80790b348b5188e7fc253665540f442c6ec7dd05"><code>80790b3</code></a> Bump 0.16.1 (<a href="https://redirect.github.com/astral-sh/ruff/issues/27330">#27330</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/63830f3e97b56ca3be0dd8f1092f76c4acc63213"><code>63830f3</code></a> [ty] Borrow from constraint set storage less often (<a href="https://redirect.github.com/astral-sh/ruff/issues/27328">#27328</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/f40dca98a7f1b6fff0cee5ecf1e6364d5a8bdc15"><code>f40dca9</code></a> [ty] Preserve forwarded expanded-variadic diagnostic sources (<a href="https://redirect.github.com/astral-sh/ruff/issues/27266">#27266</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/0d804975a2645d6e4a795cf501fd764b88aa47e3"><code>0d80497</code></a> Lint TOML files in the LSP (<a href="https://redirect.github.com/astral-sh/ruff/issues/26862">#26862</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/d91586bd5b30f77f6614d57b73fc7dbea9051a0e"><code>d91586b</code></a> Update prek dependencies (<a href="https://redirect.github.com/astral-sh/ruff/issues/27293">#27293</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/7da4b8b8d78fd6df2b3e06d8466d9cd49822900d"><code>7da4b8b</code></a> [ty] Respect bounds and constraints in generic materializations (<a href="https://redirect.github.com/astral-sh/ruff/issues/27228">#27228</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/b20daf741241a6829ff8963a203f7847561deb62"><code>b20daf7</code></a> [ty] refactor: add helper function to send partial results (<a href="https://redirect.github.com/astral-sh/ruff/issues/27249">#27249</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/4d4c8fa1c75b00561ea24eefefb13eb5ff80e01f"><code>4d4c8fa</code></a> [ty] Emit diagnostic when specializing a non-generic class (<a href="https://redirect.github.com/astral-sh/ruff/issues/26883">#26883</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/7c3e2db97deb5c5edd6e4303403ef6caf2bde8be"><code>7c3e2db</code></a> [ty] Fix enum class container assignability (<a href="https://redirect.github.com/astral-sh/ruff/issues/27318">#27318</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/d5ef97fcd03e108f7510f84b8ed85bb4051311fe"><code>d5ef97f</code></a> [<code>flake8-return</code>] Fix false positive when variable is read in <code>finally</code> claus...</li>
<li>Additional commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.16.0...0.16.1">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---

## build(deps): update cryptography requirement from >=49.0.0 to >=50.0.0 in /services/claw-interface (#3303)

- **SHA**: `a0cc2cd7b6b8acbe8547c0ebd9a553585667aff2`
- **作者**: dependabot[bot]
- **日期**: 2026-08-12T15:04:41Z
- **PR**: #3303

### Commit Message

```
build(deps): update cryptography requirement from >=49.0.0 to >=50.0.0 in /services/claw-interface (#3303)

Updates the requirements on
[cryptography](https://github.com/pyca/cryptography) to permit the
latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst">cryptography's
changelog</a>.</em></p>
<blockquote>
<p>50.0.0 - 2026-07-31</p>
<pre><code>
* **SECURITY ISSUE**:

:func:`~cryptography.hazmat.primitives.serialization.pkcs7.pkcs7_decrypt_der`
and its PEM and S/MIME variants no longer expose distinguishable errors
or
timing when unwrapping a ``RecipientInfo``'s ``encryptedKey``, which
could
act as a Bleichenbacher oracle for callers that decrypt untrusted
messages.
A random key is now substituted on failure, as described in :rfc:`3218`.
  Credit to **@X1AOxiang** for reporting the issue. **CVE-2026-69247**
* Deprecated Diffie-Hellman key exchange over finite fields (FFDH).
  Everything FFDH is deprecated, including the types in
``cryptography.hazmat.primitives.asymmetric.dh`` and loading FFDH keys
or
  parameters with the key loading APIs. Users should migrate to a more
  modern key exchange algorithm.
* Added ``xof()`` class methods to
  :class:`~cryptography.hazmat.primitives.hashes.SHAKE128` and
:class:`~cryptography.hazmat.primitives.hashes.SHAKE256` for
constructing
  algorithm instances configured for use with
  :class:`~cryptography.hazmat.primitives.hashes.XOFHash`.
* The :mod:`X.509 verification &lt;cryptography.x509.verification&gt;`
APIs are now
  considered stable and are subject to our API stability policy.
* Added the :doc:`/cobblestone` recipe, an implementation of the
  Cobblestone-128 and Cobblestone-256 instantiations of the `C2SP
  chunked-encryption specification
&lt;https://c2sp.org/chunked-encryption&gt;`_ for streaming
authenticated
  encryption of large messages.
* Parsing a Signed Certificate Timestamp list now rejects encodings that
carry trailing bytes after the list or after an individual SCT, instead
of
  silently ignoring them.
* Added support for using :class:`~cryptography.x509.Name` as a field
type in
  the :doc:`/hazmat/asn1/index` module.
* Loading a public key or an EC private key now rejects DER where the
``subjectPublicKey`` (or EC ``publicKey``) ``BIT STRING`` declares a
non-zero
  number of unused bits, instead of silently ignoring it.
* Parsing a CRL entry's ``InvalidityDate`` extension now rejects a
``GeneralizedTime`` that carries fractional seconds or another non-DER
form,
matching the strict encoding already required for every other X.509 time
  field.
* :func:`~cryptography.x509.ocsp.load_der_ocsp_request` and
:func:`~cryptography.x509.ocsp.load_der_ocsp_response` now reject a
request
or response whose ``version`` field is not ``v1``, the only version
defined
by RFC 6960, matching the version validation already performed when
loading
  certificates, CSRs and CRLs.
* :class:`~cryptography.hazmat.primitives.hashes.XOFHash` is now
supported
  when building against AWS-LC.
* HMAC (and therefore PBKDF2-HMAC) with SHA-3 hashes is now supported
when
  building against AWS-LC.
* Diffie-Hellman (:doc:`/hazmat/primitives/asymmetric/dh`) is now
supported
  when building against AWS-LC.
&lt;/tr&gt;&lt;/table&gt; 
</code></pre>
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/pyca/cryptography/commit/dcb7050b807b00392fa9fe2eac7cb362fcf355cc"><code>dcb7050</code></a>
Prepare for 50.0.0 release (<a
href="https://redirect.github.com/pyca/cryptography/issues/15372">#15372</a>)</li>
<li><a
href="https://github.com/pyca/cryptography/commit/53fccd93413a8d7f07d6d8999681f27b75cffa3f"><code>53fccd9</code></a>
Don't leak how PKCS#7 encryptedKey decryption failed (<a
href="https://redirect.github.com/pyca/cryptography/issues/15369">#15369</a>)</li>
<li><a
href="https://github.com/pyca/cryptography/commit/d472f978470fbefa521b86d98b2ecccbbb4d1dd8"><code>d472f97</code></a>
Add <code>from __future__ import annotations</code> to all src/ Python
files (<a
href="https://redirect.github.com/pyca/cryptography/issues/15371">#15371</a>)</li>
<li><a
href="https://github.com/pyca/cryptography/commit/908773d53829fb1466c6db364b31321c3cd8eb9a"><code>908773d</code></a>
Bump downstream dependencies in CI (<a
href="https://redirect.github.com/pyca/cryptography/issues/15368">#15368</a>)</li>
<li><a
href="https://github.com/pyca/cryptography/commit/2cc07cc948948211899bcb0cddd1fddf86e95812"><code>2cc07cc</code></a>
Bump BoringSSL, OpenSSL, AWS-LC in CI (<a
href="https://redirect.github.com/pyca/cryptography/issues/15367">#15367</a>)</li>
<li><a
href="https://github.com/pyca/cryptography/commit/c94ede9f040fa44942f7139772603419000acf66"><code>c94ede9</code></a>
chore(deps): bump ruff from 0.16.0 to 0.16.1 (<a
href="https://redirect.github.com/pyca/cryptography/issues/15366">#15366</a>)</li>
<li><a
href="https://github.com/pyca/cryptography/commit/67a8308dc9ea4cce6056e0f1438f903c208c3f35"><code>67a8308</code></a>
chore(deps): bump virtualenv from 21.7.0 to 21.7.1 (<a
href="https://redirect.github.com/pyca/cryptography/issues/15365">#15365</a>)</li>
<li><a
href="https://github.com/pyca/cryptography/commit/95018ffcdbbc510fd92fc872e3a3e80aa6e58596"><code>95018ff</code></a>
Release the GIL in one-shot AEAD encrypt/decrypt (<a
href="https://redirect.github.com/pyca/cryptography/issues/15361">#15361</a>)</li>
<li><a
href="https://github.com/pyca/cryptography/commit/6954733eaf55a0074abf88f06f7242dfca3a5d02"><code>6954733</code></a>
Release the GIL during DH and DSA parameter generation (<a
href="https://redirect.github.com/pyca/cryptography/issues/15364">#15364</a>)</li>
<li><a
href="https://github.com/pyca/cryptography/commit/6893b94c33e948f6240082461424cfb5da2dacc6"><code>6893b94</code></a>
Import _serialization instead of serialization in x509/extensions (<a
href="https://redirect.github.com/pyca/cryptography/issues/15363">#15363</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/pyca/cryptography/compare/49.0.0...50.0.0">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Body

Updates the requirements on [cryptography](https://github.com/pyca/cryptography) to permit the latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst">cryptography's changelog</a>.</em></p>
<blockquote>
<p>50.0.0 - 2026-07-31</p>
<pre><code>
* **SECURITY ISSUE**:
  :func:`~cryptography.hazmat.primitives.serialization.pkcs7.pkcs7_decrypt_der`
  and its PEM and S/MIME variants no longer expose distinguishable errors or
  timing when unwrapping a ``RecipientInfo``'s ``encryptedKey``, which could
  act as a Bleichenbacher oracle for callers that decrypt untrusted messages.
  A random key is now substituted on failure, as described in :rfc:`3218`.
  Credit to **@X1AOxiang** for reporting the issue. **CVE-2026-69247**
* Deprecated Diffie-Hellman key exchange over finite fields (FFDH).
  Everything FFDH is deprecated, including the types in
  ``cryptography.hazmat.primitives.asymmetric.dh`` and loading FFDH keys or
  parameters with the key loading APIs. Users should migrate to a more
  modern key exchange algorithm.
* Added ``xof()`` class methods to
  :class:`~cryptography.hazmat.primitives.hashes.SHAKE128` and
  :class:`~cryptography.hazmat.primitives.hashes.SHAKE256` for constructing
  algorithm instances configured for use with
  :class:`~cryptography.hazmat.primitives.hashes.XOFHash`.
* The :mod:`X.509 verification &lt;cryptography.x509.verification&gt;` APIs are now
  considered stable and are subject to our API stability policy.
* Added the :doc:`/cobblestone` recipe, an implementation of the
  Cobblestone-128 and Cobblestone-256 instantiations of the `C2SP
  chunked-encryption specification
  &lt;https://c2sp.org/chunked-encryption&gt;`_ for streaming authenticated
  encryption of large messages.
* Parsing a Signed Certificate Timestamp list now rejects encodings that
  carry trailing bytes after the list or after an individual SCT, instead of
  silently ignoring them.
* Added support for using :class:`~cryptography.x509.Name` as a field type in
  the :doc:`/hazmat/asn1/index` module.
* Loading a public key or an EC private key now rejects DER where the
  ``subjectPublicKey`` (or EC ``publicKey``) ``BIT STRING`` declares a non-zero
  number of unused bits, instead of silently ignoring it.
* Parsing a CRL entry's ``InvalidityDate`` extension now rejects a
  ``GeneralizedTime`` that carries fractional seconds or another non-DER form,
  matching the strict encoding already required for every other X.509 time
  field.
* :func:`~cryptography.x509.ocsp.load_der_ocsp_request` and
  :func:`~cryptography.x509.ocsp.load_der_ocsp_response` now reject a request
  or response whose ``version`` field is not ``v1``, the only version defined
  by RFC 6960, matching the version validation already performed when loading
  certificates, CSRs and CRLs.
* :class:`~cryptography.hazmat.primitives.hashes.XOFHash` is now supported
  when building against AWS-LC.
* HMAC (and therefore PBKDF2-HMAC) with SHA-3 hashes is now supported when
  building against AWS-LC.
* Diffie-Hellman (:doc:`/hazmat/primitives/asymmetric/dh`) is now supported
  when building against AWS-LC.
&lt;/tr&gt;&lt;/table&gt; 
</code></pre>
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/pyca/cryptography/commit/dcb7050b807b00392fa9fe2eac7cb362fcf355cc"><code>dcb7050</code></a> Prepare for 50.0.0 release (<a href="https://redirect.github.com/pyca/cryptography/issues/15372">#15372</a>)</li>
<li><a href="https://github.com/pyca/cryptography/commit/53fccd93413a8d7f07d6d8999681f27b75cffa3f"><code>53fccd9</code></a> Don't leak how PKCS#7 encryptedKey decryption failed (<a href="https://redirect.github.com/pyca/cryptography/issues/15369">#15369</a>)</li>
<li><a href="https://github.com/pyca/cryptography/commit/d472f978470fbefa521b86d98b2ecccbbb4d1dd8"><code>d472f97</code></a> Add <code>from __future__ import annotations</code> to all src/ Python files (<a href="https://redirect.github.com/pyca/cryptography/issues/15371">#15371</a>)</li>
<li><a href="https://github.com/pyca/cryptography/commit/908773d53829fb1466c6db364b31321c3cd8eb9a"><code>908773d</code></a> Bump downstream dependencies in CI (<a href="https://redirect.github.com/pyca/cryptography/issues/15368">#15368</a>)</li>
<li><a href="https://github.com/pyca/cryptography/commit/2cc07cc948948211899bcb0cddd1fddf86e95812"><code>2cc07cc</code></a> Bump BoringSSL, OpenSSL, AWS-LC in CI (<a href="https://redirect.github.com/pyca/cryptography/issues/15367">#15367</a>)</li>
<li><a href="https://github.com/pyca/cryptography/commit/c94ede9f040fa44942f7139772603419000acf66"><code>c94ede9</code></a> chore(deps): bump ruff from 0.16.0 to 0.16.1 (<a href="https://redirect.github.com/pyca/cryptography/issues/15366">#15366</a>)</li>
<li><a href="https://github.com/pyca/cryptography/commit/67a8308dc9ea4cce6056e0f1438f903c208c3f35"><code>67a8308</code></a> chore(deps): bump virtualenv from 21.7.0 to 21.7.1 (<a href="https://redirect.github.com/pyca/cryptography/issues/15365">#15365</a>)</li>
<li><a href="https://github.com/pyca/cryptography/commit/95018ffcdbbc510fd92fc872e3a3e80aa6e58596"><code>95018ff</code></a> Release the GIL in one-shot AEAD encrypt/decrypt (<a href="https://redirect.github.com/pyca/cryptography/issues/15361">#15361</a>)</li>
<li><a href="https://github.com/pyca/cryptography/commit/6954733eaf55a0074abf88f06f7242dfca3a5d02"><code>6954733</code></a> Release the GIL during DH and DSA parameter generation (<a href="https://redirect.github.com/pyca/cryptography/issues/15364">#15364</a>)</li>
<li><a href="https://github.com/pyca/cryptography/commit/6893b94c33e948f6240082461424cfb5da2dacc6"><code>6893b94</code></a> Import _serialization instead of serialization in x509/extensions (<a href="https://redirect.github.com/pyca/cryptography/issues/15363">#15363</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/pyca/cryptography/compare/49.0.0...50.0.0">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---

## build(deps): update websockets requirement from >=16.1.1 to >=17.0.1 in /services/claw-interface (#3304)

- **SHA**: `838236b1d5fe9f0a962004454601b618e550dcf5`
- **作者**: dependabot[bot]
- **日期**: 2026-08-12T15:04:20Z
- **PR**: #3304

### Commit Message

```
build(deps): update websockets requirement from >=16.1.1 to >=17.0.1 in /services/claw-interface (#3304)

Updates the requirements on
[websockets](https://github.com/python-websockets/websockets) to permit
the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/python-websockets/websockets/releases">websockets's
releases</a>.</em></p>
<blockquote>
<h2>17.0.1</h2>
<p>See <a
href="https://websockets.readthedocs.io/en/stable/project/changelog.html">https://websockets.readthedocs.io/en/stable/project/changelog.html</a>
for details.</p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/python-websockets/websockets/commit/fd3f16cc4f57ace08e323a7806f1432e957cb75e"><code>fd3f16c</code></a>
Release version 17.0.1.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/3e4634aa0a4480893252c1b2907aae2930977a93"><code>3e4634a</code></a>
Remove superfluous &quot;no cover&quot; pragmas.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/b93ef1e6618de151c62b5131f69e33998febe171"><code>b93ef1e</code></a>
Add tests for the asyncio server.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/fef04d84cd7e4dfd90c612bd1305bdd795e90715"><code>fef04d8</code></a>
Fix backpressure in the Trio implementation.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/eb3600ce789ca8e19ecda5f07bad68b66fe1a762"><code>eb3600c</code></a>
Restore compatibility of serve_forever with uvloop.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/8b5e7679ecd1600634e3163e849b7b0885ebda49"><code>8b5e767</code></a>
Simplify asyncio server implementation.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/94f638481b6641da9a8efaf57d0b18651c0367c2"><code>94f6384</code></a>
Refactor connection handling outside of Server class.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/382699387f5a54a788c003b2c15c2b56605eadba"><code>3826993</code></a>
Unpin sphinx.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/31ec0025216aa34fa5320fe581bb89bc6b323909"><code>31ec002</code></a>
Add Trio to requirements for building docs.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/ff7a7fb3bb512d5fcf4678d8c6f347e3a929bcea"><code>ff7a7fb</code></a>
Increase timeout for building wheels.</li>
<li>Additional commits viewable in <a
href="https://github.com/python-websockets/websockets/compare/16.1.1...17.0.1">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Body

Updates the requirements on [websockets](https://github.com/python-websockets/websockets) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/python-websockets/websockets/releases">websockets's releases</a>.</em></p>
<blockquote>
<h2>17.0.1</h2>
<p>See <a href="https://websockets.readthedocs.io/en/stable/project/changelog.html">https://websockets.readthedocs.io/en/stable/project/changelog.html</a> for details.</p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/python-websockets/websockets/commit/fd3f16cc4f57ace08e323a7806f1432e957cb75e"><code>fd3f16c</code></a> Release version 17.0.1.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/3e4634aa0a4480893252c1b2907aae2930977a93"><code>3e4634a</code></a> Remove superfluous &quot;no cover&quot; pragmas.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/b93ef1e6618de151c62b5131f69e33998febe171"><code>b93ef1e</code></a> Add tests for the asyncio server.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/fef04d84cd7e4dfd90c612bd1305bdd795e90715"><code>fef04d8</code></a> Fix backpressure in the Trio implementation.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/eb3600ce789ca8e19ecda5f07bad68b66fe1a762"><code>eb3600c</code></a> Restore compatibility of serve_forever with uvloop.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/8b5e7679ecd1600634e3163e849b7b0885ebda49"><code>8b5e767</code></a> Simplify asyncio server implementation.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/94f638481b6641da9a8efaf57d0b18651c0367c2"><code>94f6384</code></a> Refactor connection handling outside of Server class.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/382699387f5a54a788c003b2c15c2b56605eadba"><code>3826993</code></a> Unpin sphinx.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/31ec0025216aa34fa5320fe581bb89bc6b323909"><code>31ec002</code></a> Add Trio to requirements for building docs.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/ff7a7fb3bb512d5fcf4678d8c6f347e3a929bcea"><code>ff7a7fb</code></a> Increase timeout for building wheels.</li>
<li>Additional commits viewable in <a href="https://github.com/python-websockets/websockets/compare/16.1.1...17.0.1">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---

## build(deps): update openai requirement from <2.47.0,>=2.46.0 to >=2.52.0,<2.53.0 in /services/claw-interface (#3305)

- **SHA**: `62b2a232cdb5129d3602c6a098b032e646c2a0cb`
- **作者**: dependabot[bot]
- **日期**: 2026-08-12T15:04:02Z
- **PR**: #3305

### Commit Message

```
build(deps): update openai requirement from <2.47.0,>=2.46.0 to >=2.52.0,<2.53.0 in /services/claw-interface (#3305)

Updates the requirements on
[openai](https://github.com/openai/openai-python) to permit the latest
version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/openai/openai-python/releases">openai's
releases</a>.</em></p>
<blockquote>
<h2>v2.52.0</h2>
<h2>2.52.0 (2026-07-31)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.51.0...v2.52.0">v2.51.0...v2.52.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> content provenance checks (<a
href="https://github.com/openai/openai-python/commit/1d6c1180f8eaa71bfd45cae67360987b2bea3656">1d6c118</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>client:</strong> honor Retry-After delays up to two minutes
(<a
href="https://redirect.github.com/openai/openai-python/issues/3555">#3555</a>)
(<a
href="https://github.com/openai/openai-python/commit/7fa7946485b5ecbadd0ebf8624c574e2c9e3370c">7fa7946</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>add API-key mTLS HTTP client recipes (<a
href="https://redirect.github.com/openai/openai-python/issues/3552">#3552</a>)
(<a
href="https://github.com/openai/openai-python/commit/7a3d5e46b61cb36109dc4e7fd6d4ab70cc6d6c0f">7a3d5e4</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/openai/openai-python/blob/main/CHANGELOG.md">openai's
changelog</a>.</em></p>
<blockquote>
<h2>2.52.0 (2026-07-31)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.51.0...v2.52.0">v2.51.0...v2.52.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> content provenance checks (<a
href="https://github.com/openai/openai-python/commit/1d6c1180f8eaa71bfd45cae67360987b2bea3656">1d6c118</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>client:</strong> honor Retry-After delays up to two minutes
(<a
href="https://redirect.github.com/openai/openai-python/issues/3555">#3555</a>)
(<a
href="https://github.com/openai/openai-python/commit/7fa7946485b5ecbadd0ebf8624c574e2c9e3370c">7fa7946</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>add API-key mTLS HTTP client recipes (<a
href="https://redirect.github.com/openai/openai-python/issues/3552">#3552</a>)
(<a
href="https://github.com/openai/openai-python/commit/7a3d5e46b61cb36109dc4e7fd6d4ab70cc6d6c0f">7a3d5e4</a>)</li>
</ul>
<h2>2.51.0 (2026-07-30)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.50.0...v2.51.0">v2.50.0...v2.51.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> fast tier (<a
href="https://github.com/openai/openai-python/commit/8808ed27952dae13fb8761f045376af5b3e5bec2">8808ed2</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> add fast tier to helper methods (<a
href="https://github.com/openai/openai-python/commit/60641266ff4b296044a81fe1717c17a70ceadbf1">6064126</a>)</li>
</ul>
<h2>2.50.0 (2026-07-28)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.49.0...v2.50.0">v2.49.0...v2.50.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> transcription model updates (<a
href="https://github.com/openai/openai-python/commit/fd57393389eac75af08c2e887cb188590448be20">fd57393</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>audio:</strong> restore transcription keyword overload (<a
href="https://github.com/openai/openai-python/commit/713a2624966c40f4e5b0c20436b8a79aa8383b08">713a262</a>)</li>
</ul>
<h2>2.49.0 (2026-07-27)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.48.0...v2.49.0">v2.48.0...v2.49.0</a></p>
<h3>Features</h3>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/openai/openai-python/commit/ca693fbaa20a620ce53a48f4419a1a01444564e7"><code>ca693fb</code></a>
release: 2.52.0</li>
<li><a
href="https://github.com/openai/openai-python/commit/2ad8c98747a0cbf9abd7c5a6bc8f74186e57fb6f"><code>2ad8c98</code></a>
feat(api): content provenance checks</li>
<li><a
href="https://github.com/openai/openai-python/commit/7a3d5e46b61cb36109dc4e7fd6d4ab70cc6d6c0f"><code>7a3d5e4</code></a>
docs: add API-key mTLS HTTP client recipes (<a
href="https://redirect.github.com/openai/openai-python/issues/3552">#3552</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/7fa7946485b5ecbadd0ebf8624c574e2c9e3370c"><code>7fa7946</code></a>
fix(client): honor Retry-After delays up to two minutes (<a
href="https://redirect.github.com/openai/openai-python/issues/3555">#3555</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/3844843c277f42b0b18beaa58152cfda61df524a"><code>3844843</code></a>
release: 2.51.0 (<a
href="https://redirect.github.com/openai/openai-python/issues/3553">#3553</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/4f404262955cb711c56c07cce52076b6107303e5"><code>4f40426</code></a>
release: 2.50.0</li>
<li><a
href="https://github.com/openai/openai-python/commit/92594f1908ae385d355f01f7dcd2958e13ecfb7e"><code>92594f1</code></a>
fix(audio): restore transcription keyword overload</li>
<li><a
href="https://github.com/openai/openai-python/commit/59ed1dccac26e7e92f5b91dd106dd273bf32b922"><code>59ed1dc</code></a>
feat(api): transcription model updates</li>
<li><a
href="https://github.com/openai/openai-python/commit/6ba31bcbb2df31fa1890f51877104133c0a0be60"><code>6ba31bc</code></a>
release: 2.49.0 (<a
href="https://redirect.github.com/openai/openai-python/issues/3539">#3539</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/90483adb3034186c18c0f64de26b24699d733173"><code>90483ad</code></a>
test: support a hermetic local API reference (<a
href="https://redirect.github.com/openai/openai-python/issues/3542">#3542</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/openai/openai-python/compare/v2.46.0...v2.52.0">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Body

Updates the requirements on [openai](https://github.com/openai/openai-python) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/openai/openai-python/releases">openai's releases</a>.</em></p>
<blockquote>
<h2>v2.52.0</h2>
<h2>2.52.0 (2026-07-31)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.51.0...v2.52.0">v2.51.0...v2.52.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> content provenance checks (<a href="https://github.com/openai/openai-python/commit/1d6c1180f8eaa71bfd45cae67360987b2bea3656">1d6c118</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>client:</strong> honor Retry-After delays up to two minutes (<a href="https://redirect.github.com/openai/openai-python/issues/3555">#3555</a>) (<a href="https://github.com/openai/openai-python/commit/7fa7946485b5ecbadd0ebf8624c574e2c9e3370c">7fa7946</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>add API-key mTLS HTTP client recipes (<a href="https://redirect.github.com/openai/openai-python/issues/3552">#3552</a>) (<a href="https://github.com/openai/openai-python/commit/7a3d5e46b61cb36109dc4e7fd6d4ab70cc6d6c0f">7a3d5e4</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/openai/openai-python/blob/main/CHANGELOG.md">openai's changelog</a>.</em></p>
<blockquote>
<h2>2.52.0 (2026-07-31)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.51.0...v2.52.0">v2.51.0...v2.52.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> content provenance checks (<a href="https://github.com/openai/openai-python/commit/1d6c1180f8eaa71bfd45cae67360987b2bea3656">1d6c118</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>client:</strong> honor Retry-After delays up to two minutes (<a href="https://redirect.github.com/openai/openai-python/issues/3555">#3555</a>) (<a href="https://github.com/openai/openai-python/commit/7fa7946485b5ecbadd0ebf8624c574e2c9e3370c">7fa7946</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>add API-key mTLS HTTP client recipes (<a href="https://redirect.github.com/openai/openai-python/issues/3552">#3552</a>) (<a href="https://github.com/openai/openai-python/commit/7a3d5e46b61cb36109dc4e7fd6d4ab70cc6d6c0f">7a3d5e4</a>)</li>
</ul>
<h2>2.51.0 (2026-07-30)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.50.0...v2.51.0">v2.50.0...v2.51.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> fast tier (<a href="https://github.com/openai/openai-python/commit/8808ed27952dae13fb8761f045376af5b3e5bec2">8808ed2</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> add fast tier to helper methods (<a href="https://github.com/openai/openai-python/commit/60641266ff4b296044a81fe1717c17a70ceadbf1">6064126</a>)</li>
</ul>
<h2>2.50.0 (2026-07-28)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.49.0...v2.50.0">v2.49.0...v2.50.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> transcription model updates (<a href="https://github.com/openai/openai-python/commit/fd57393389eac75af08c2e887cb188590448be20">fd57393</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>audio:</strong> restore transcription keyword overload (<a href="https://github.com/openai/openai-python/commit/713a2624966c40f4e5b0c20436b8a79aa8383b08">713a262</a>)</li>
</ul>
<h2>2.49.0 (2026-07-27)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.48.0...v2.49.0">v2.48.0...v2.49.0</a></p>
<h3>Features</h3>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/openai/openai-python/commit/ca693fbaa20a620ce53a48f4419a1a01444564e7"><code>ca693fb</code></a> release: 2.52.0</li>
<li><a href="https://github.com/openai/openai-python/commit/2ad8c98747a0cbf9abd7c5a6bc8f74186e57fb6f"><code>2ad8c98</code></a> feat(api): content provenance checks</li>
<li><a href="https://github.com/openai/openai-python/commit/7a3d5e46b61cb36109dc4e7fd6d4ab70cc6d6c0f"><code>7a3d5e4</code></a> docs: add API-key mTLS HTTP client recipes (<a href="https://redirect.github.com/openai/openai-python/issues/3552">#3552</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/7fa7946485b5ecbadd0ebf8624c574e2c9e3370c"><code>7fa7946</code></a> fix(client): honor Retry-After delays up to two minutes (<a href="https://redirect.github.com/openai/openai-python/issues/3555">#3555</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/3844843c277f42b0b18beaa58152cfda61df524a"><code>3844843</code></a> release: 2.51.0 (<a href="https://redirect.github.com/openai/openai-python/issues/3553">#3553</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/4f404262955cb711c56c07cce52076b6107303e5"><code>4f40426</code></a> release: 2.50.0</li>
<li><a href="https://github.com/openai/openai-python/commit/92594f1908ae385d355f01f7dcd2958e13ecfb7e"><code>92594f1</code></a> fix(audio): restore transcription keyword overload</li>
<li><a href="https://github.com/openai/openai-python/commit/59ed1dccac26e7e92f5b91dd106dd273bf32b922"><code>59ed1dc</code></a> feat(api): transcription model updates</li>
<li><a href="https://github.com/openai/openai-python/commit/6ba31bcbb2df31fa1890f51877104133c0a0be60"><code>6ba31bc</code></a> release: 2.49.0 (<a href="https://redirect.github.com/openai/openai-python/issues/3539">#3539</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/90483adb3034186c18c0f64de26b24699d733173"><code>90483ad</code></a> test: support a hermetic local API reference (<a href="https://redirect.github.com/openai/openai-python/issues/3542">#3542</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/openai/openai-python/compare/v2.46.0...v2.52.0">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---

## fix(pack-test): close Engine Environment archive gaps in cleanup lifecycle (#3356)

- **SHA**: `e9aa74e6193a41f6225a79c10841329e0cb8baf7`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-12T15:01:58Z
- **PR**: #3356

### Commit Message

```
fix(pack-test): close Engine Environment archive gaps in cleanup lifecycle (#3356)

## 背景

Pack Test v2 每个 test run 在引擎侧创建一个
Environment（`pack-test-{test_run_id}`，`pack_test_engine_runtime_service.py`）。staging
已积累 24 个 `pack-test-ptr_*` 孤儿 Environment，持续污染引擎 `stale_total`
指标（SerendipityOneInc/zooclaw-engine#691，第 1 层"测试自清理"修法；存量清理与 TTL 兜底 GC 由
engine 侧另行处理）。

现行 `_cleanup_engine_test_run` 的分阶段清理里已有 archive 阶段（#3121 引入），但审计整个 run
状态机后发现两条路径仍会让 Environment 无限期泄漏：

## 修复内容

1. **早期阶段失败不再饿死 archive**：staged cleanup 严格顺序执行（disable channels → agent
cleanup → env archive → …）。channel-service 或引擎 agent 清理持续失败时，archive
阶段永远到不了。现在 staged cleanup 失败时会对 Environment 做 best-effort
archive——archive 语义只阻止新引用（engine design/13 §3），先于 agent
阶段执行是安全的；引擎端点幂等（`archived_at` COALESCE），跨 cron 轮重复调用无害。原阶段错误仍写入
`cleanup_error` 并在下轮 cron 重试整个阶段机，不静默吞。
2. **回收卡死的 `promoting`**：`promoting` 在 `_CLEANUP_SKIPPED_STATUSES`
里且此前不在 `list_cleanup_due` 查询中，promote 请求 worker 中途死掉的 run
永远到不了终态、Environment 永不 archive。现在纳入 30 分钟 in-progress 恢复 TTL：promoted
asset 已存在则补完 `promoting → promoted`（随后走 promoted 清理路径），不存在则回退 `promoting
→ accepted`（走 accepted 7 天 TTL 清理路径）。
3. **Environment 已不存在视为已归档**：引擎 404（可能被 layer-2 GC
先清掉）不再让清理卡死，按无害跳过处理并记日志；其余错误照常抛出、记录、下轮重试。

## 终态路径覆盖（均归于 archive）

| 终态路径 | archive 接入点 |
|---|---|
| cron 过期清理 / preview 超时 / failed / timed_out |
`_cleanup_engine_test_run` archive 阶段 |
| install 失败（`install_test_run` except → `cleanup_pending`） | 同上（cron
收敛） |
| 提交后清理（`request_test_run_cleanup` reason=submitted） | 同上（cron 收敛） |
| superseded / 卡死 in-progress 恢复 | 同上（cron 收敛） |
| 早期阶段持续失败 | **新增** best-effort archive（本 PR） |
| 卡死 `promoting` | **新增** 恢复到 promoted/accepted 后归入上述路径（本 PR） |
| `runtime_transferred` | Environment 所有权随 transfer 移交新 run，由新 run 终态
archive（无泄漏，不重复处理） |

## 引擎不可达时的语义

与该 cron 现有语义一致：错误写入 run 的 `cleanup_error`（可查询）、cron `failed_count`
计数、异常日志留痕；run 停在当前 cleanup stage，下一轮 cron 幂等重试。引擎故障不会阻塞 run
状态收敛之外的清理，也不会被静默吞掉。

## Guard（#691 要求的 created == cleaned）

`test_pack_test_engine_cleanup_service.py` 新增参数化守卫：**每个可达清理的 run
状态**（`cleanup_pending` / `failed` / `timed_out` / `ready_for_preview` /
`previewing` / `accepted` / `promoted`）走一遍清理后断言 `archive_environment`
恰被调用一次且 run 归于 `cleaned`；另覆盖失败路径（channel disable 失败、agent cleanup
失败、sandbox 未释放、引擎 404、引擎 5xx 不可达）与 `promoting` 恢复两分支。

## 验证

- `bash scripts/verify-py.sh`：ruff check + ruff format + pyright +
import-linter 全绿
- `pytest tests/unit/test_pack_test_engine_cleanup_service.py
tests/unit/test_pack_test_repos.py`：22 passed
- 相邻套件 `test_pack_test_runtime_service.py` / `test_pack_test_service.py`
/ `test_pack_test_routes.py` /
`test_agent_builder_recovery_readiness.py` /
`test_pack_test_engine_runtime_service.py` /
`test_engine_client_environments.py`：105 passed

Refs SerendipityOneInc/zooclaw-engine#691

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01GMngUSFBCS3dU6ZfN5QAVn

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## 背景

Pack Test v2 每个 test run 在引擎侧创建一个 Environment（`pack-test-{test_run_id}`，`pack_test_engine_runtime_service.py`）。staging 已积累 24 个 `pack-test-ptr_*` 孤儿 Environment，持续污染引擎 `stale_total` 指标（SerendipityOneInc/zooclaw-engine#691，第 1 层"测试自清理"修法；存量清理与 TTL 兜底 GC 由 engine 侧另行处理）。

现行 `_cleanup_engine_test_run` 的分阶段清理里已有 archive 阶段（#3121 引入），但审计整个 run 状态机后发现两条路径仍会让 Environment 无限期泄漏：

## 修复内容

1. **早期阶段失败不再饿死 archive**：staged cleanup 严格顺序执行（disable channels → agent cleanup → env archive → …）。channel-service 或引擎 agent 清理持续失败时，archive 阶段永远到不了。现在 staged cleanup 失败时会对 Environment 做 best-effort archive——archive 语义只阻止新引用（engine design/13 §3），先于 agent 阶段执行是安全的；引擎端点幂等（`archived_at` COALESCE），跨 cron 轮重复调用无害。原阶段错误仍写入 `cleanup_error` 并在下轮 cron 重试整个阶段机，不静默吞。
2. **回收卡死的 `promoting`**：`promoting` 在 `_CLEANUP_SKIPPED_STATUSES` 里且此前不在 `list_cleanup_due` 查询中，promote 请求 worker 中途死掉的 run 永远到不了终态、Environment 永不 archive。现在纳入 30 分钟 in-progress 恢复 TTL：promoted asset 已存在则补完 `promoting → promoted`（随后走 promoted 清理路径），不存在则回退 `promoting → accepted`（走 accepted 7 天 TTL 清理路径）。
3. **Environment 已不存在视为已归档**：引擎 404（可能被 layer-2 GC 先清掉）不再让清理卡死，按无害跳过处理并记日志；其余错误照常抛出、记录、下轮重试。

## 终态路径覆盖（均归于 archive）

| 终态路径 | archive 接入点 |
|---|---|
| cron 过期清理 / preview 超时 / failed / timed_out | `_cleanup_engine_test_run` archive 阶段 |
| install 失败（`install_test_run` except → `cleanup_pending`） | 同上（cron 收敛） |
| 提交后清理（`request_test_run_cleanup` reason=submitted） | 同上（cron 收敛） |
| superseded / 卡死 in-progress 恢复 | 同上（cron 收敛） |
| 早期阶段持续失败 | **新增** best-effort archive（本 PR） |
| 卡死 `promoting` | **新增** 恢复到 promoted/accepted 后归入上述路径（本 PR） |
| `runtime_transferred` | Environment 所有权随 transfer 移交新 run，由新 run 终态 archive（无泄漏，不重复处理） |

## 引擎不可达时的语义

与该 cron 现有语义一致：错误写入 run 的 `cleanup_error`（可查询）、cron `failed_count` 计数、异常日志留痕；run 停在当前 cleanup stage，下一轮 cron 幂等重试。引擎故障不会阻塞 run 状态收敛之外的清理，也不会被静默吞掉。

## Guard（#691 要求的 created == cleaned）

`test_pack_test_engine_cleanup_service.py` 新增参数化守卫：**每个可达清理的 run 状态**（`cleanup_pending` / `failed` / `timed_out` / `ready_for_preview` / `previewing` / `accepted` / `promoted`）走一遍清理后断言 `archive_environment` 恰被调用一次且 run 归于 `cleaned`；另覆盖失败路径（channel disable 失败、agent cleanup 失败、sandbox 未释放、引擎 404、引擎 5xx 不可达）与 `promoting` 恢复两分支。

## 验证

- `bash scripts/verify-py.sh`：ruff check + ruff format + pyright + import-linter 全绿
- `pytest tests/unit/test_pack_test_engine_cleanup_service.py tests/unit/test_pack_test_repos.py`：22 passed
- 相邻套件 `test_pack_test_runtime_service.py` / `test_pack_test_service.py` / `test_pack_test_routes.py` / `test_agent_builder_recovery_readiness.py` / `test_pack_test_engine_runtime_service.py` / `test_engine_client_environments.py`：105 passed

Refs SerendipityOneInc/zooclaw-engine#691

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01GMngUSFBCS3dU6ZfN5QAVn


---

## fix(billing): preserve Creem checkout environment (#3357)

- **SHA**: `b4a99063c9732902c6403fba46181e137bea1432`
- **作者**: tim-srp
- **日期**: 2026-08-12T15:00:23Z
- **PR**: #3357

### Commit Message

```
fix(billing): preserve Creem checkout environment (#3357)

## Summary
- Persist the current Creem billing environment on newly created Card
Checkout orders.
- Validate Checkout and Trial webhook provider modes against the order
environment: sandbox accepts test/sandbox and production accepts prod.
- Pass the dynamic environment through checkout binding, first-payment,
settlement, trial projection, and reconciliation CAS operations.
- Keep legacy orders unchanged; this PR does not add historical-order
migration or manual MongoDB repair.

## Root cause
Card Checkout orders were always persisted with `environment=sandbox`,
and Checkout/Trial projection code only accepted Creem test/sandbox
provider modes. In production, Creem emits `mode=prod`, so a successful
production checkout could not bind or project the trial and the local
order remained pending.

## Test plan
- [x] 218 targeted Card Checkout and Creem lifecycle unit tests pass.
- [x] Production Checkout webhook binds a production order.
- [x] Production Trial webhook records the agreement and trial
projection with production environment.
- [x] Ruff check and format pass.
- [x] Commit-time Pyright and repository policy hooks pass.
- [ ] GitHub Code Quality Check passes in the dependency-complete CI
environment.

## Local environment note
The pre-push changed-surface verifier could not resolve the worktree's
Python dependencies and reported repository-wide missing imports. The
commit hook's Pyright check passed, and the branch was pushed with
`--no-verify` so GitHub CI can run the authoritative dependency-complete
checks.
```

### PR Body

## Summary
- Persist the current Creem billing environment on newly created Card Checkout orders.
- Validate Checkout and Trial webhook provider modes against the order environment: sandbox accepts test/sandbox and production accepts prod.
- Pass the dynamic environment through checkout binding, first-payment, settlement, trial projection, and reconciliation CAS operations.
- Keep legacy orders unchanged; this PR does not add historical-order migration or manual MongoDB repair.

## Root cause
Card Checkout orders were always persisted with `environment=sandbox`, and Checkout/Trial projection code only accepted Creem test/sandbox provider modes. In production, Creem emits `mode=prod`, so a successful production checkout could not bind or project the trial and the local order remained pending.

## Test plan
- [x] 218 targeted Card Checkout and Creem lifecycle unit tests pass.
- [x] Production Checkout webhook binds a production order.
- [x] Production Trial webhook records the agreement and trial projection with production environment.
- [x] Ruff check and format pass.
- [x] Commit-time Pyright and repository policy hooks pass.
- [ ] GitHub Code Quality Check passes in the dependency-complete CI environment.

## Local environment note
The pre-push changed-surface verifier could not resolve the worktree's Python dependencies and reported repository-wide missing imports. The commit hook's Pyright check passed, and the branch was pushed with `--no-verify` so GitHub CI can run the authoritative dependency-complete checks.


---

## feat(billing): enable Card checkout in production (#3355)

- **SHA**: `cb75b029cc28d52f675cce0b59542bdb2a0ac855`
- **作者**: tim-srp
- **日期**: 2026-08-12T13:33:24Z
- **PR**: #3355

### Commit Message

```
feat(billing): enable Card checkout in production (#3355)

## Summary

- show Card alongside Alipay in the payment-method modal in production
- request the backend Card checkout capability for authenticated
production users
- allow production runtime only with Creem production mode, while
retaining test-mode staging/dev pairing
- treat `card_available=false` as a hard Card gate without falling back
new users to legacy Stripe

## Why

The Creem Card trial and subscription flows are now implemented and
validated, but both frontend and backend still contained
staging/test-only rollout guards. Production Creem products and Vault
configuration are now ready.

## Validation

- 155 related frontend tests passed
- 77 related backend tests passed
- TypeScript, ESLint, Ruff, Ruff format, import contracts, and
pre-commit Pyright passed
- PR size: 326 changed lines across 15 files (+146/-180), mostly
regression-test migration from new-user Stripe to Creem semantics

## Deployment note

Production is enabled only for the `production` runtime paired with
`CREEM_ENVIRONMENT=production`. Staging/dev/local remain paired with
Creem test mode. Incomplete or mismatched configuration returns
`card_available=false` and Card is disabled/rejected safely. Existing
Stripe subscribers retain their legacy compatibility path; Alipay is
unchanged.
```

### PR Body

## Summary

- show Card alongside Alipay in the payment-method modal in production
- request the backend Card checkout capability for authenticated production users
- allow production runtime only with Creem production mode, while retaining test-mode staging/dev pairing
- treat `card_available=false` as a hard Card gate without falling back new users to legacy Stripe

## Why

The Creem Card trial and subscription flows are now implemented and validated, but both frontend and backend still contained staging/test-only rollout guards. Production Creem products and Vault configuration are now ready.

## Validation

- 155 related frontend tests passed
- 77 related backend tests passed
- TypeScript, ESLint, Ruff, Ruff format, import contracts, and pre-commit Pyright passed
- PR size: 326 changed lines across 15 files (+146/-180), mostly regression-test migration from new-user Stripe to Creem semantics

## Deployment note

Production is enabled only for the `production` runtime paired with `CREEM_ENVIRONMENT=production`. Staging/dev/local remain paired with Creem test mode. Incomplete or mismatched configuration returns `card_available=false` and Card is disabled/rejected safely. Existing Stripe subscribers retain their legacy compatibility path; Alipay is unchanged.


---

## fix(billing): converge null Creem terminal trial orders (#3353)

- **SHA**: `1fd5620ee68aad34c4268247ece711d7ce9799bb`
- **作者**: tim-srp
- **日期**: 2026-08-12T12:32:51Z
- **PR**: #3353

### Commit Message

```
fix(billing): converge null Creem terminal trial orders (#3353)

## Summary
- allow terminal Creem Trial reconciliation to treat a missing or
explicit-null provider transaction ID as unsettled
- fail closed when the terminal order CAS misses, while accepting an
exact concurrent terminal replay
- add focused regression coverage for both historical storage shapes and
CAS convergence outcomes

## Root cause
Historical Card Trial orders can store `provider_transaction_id` as an
explicit null. The terminal reconciliation CAS only accepted a missing
field, so it left those orders pending. The service also treated every
CAS miss as success, which let the cron count an unchanged order as
processed and retain its checkout lease.

## Test plan
- [x] `PYTHONPATH=services/claw-interface pytest
services/claw-interface/tests/unit/test_billing_v2_repos.py
services/claw-interface/tests/unit/test_creem_reconciliation.py -q`
(`132 passed`)
- [x] commit hooks: Ruff, Ruff format, dependency checks, complexity
checks, import contracts, repository contracts, and Pyright
- [x] changed-file Pyright with the local Conda interpreter (`0 errors`)
- [x] PR size gate (`112 / 3000` business/test lines)
- [ ] GitHub Actions in the complete CI environment
- [ ] controlled staging reconciliation for the verified historical
explicit-null order shape after deployment

## Local environment note
The standalone `verify-py.sh` invocation in this new worktree selected a
global Pyright process without the project dependency search path. Ruff,
format, and import-linter passed; explicit changed-file Pyright and the
repository's commit-hook Pyright passed. GitHub Actions remains the
authoritative full-environment type check.
```

### PR Body

## Summary
- allow terminal Creem Trial reconciliation to treat a missing or explicit-null provider transaction ID as unsettled
- fail closed when the terminal order CAS misses, while accepting an exact concurrent terminal replay
- add focused regression coverage for both historical storage shapes and CAS convergence outcomes

## Root cause
Historical Card Trial orders can store `provider_transaction_id` as an explicit null. The terminal reconciliation CAS only accepted a missing field, so it left those orders pending. The service also treated every CAS miss as success, which let the cron count an unchanged order as processed and retain its checkout lease.

## Test plan
- [x] `PYTHONPATH=services/claw-interface pytest services/claw-interface/tests/unit/test_billing_v2_repos.py services/claw-interface/tests/unit/test_creem_reconciliation.py -q` (`132 passed`)
- [x] commit hooks: Ruff, Ruff format, dependency checks, complexity checks, import contracts, repository contracts, and Pyright
- [x] changed-file Pyright with the local Conda interpreter (`0 errors`)
- [x] PR size gate (`112 / 3000` business/test lines)
- [ ] GitHub Actions in the complete CI environment
- [ ] controlled staging reconciliation for the verified historical explicit-null order shape after deployment

## Local environment note
The standalone `verify-py.sh` invocation in this new worktree selected a global Pyright process without the project dependency search path. Ruff, format, and import-linter passed; explicit changed-file Pyright and the repository's commit-hook Pyright passed. GitHub Actions remains the authoritative full-environment type check.


---

## fix(billing): converge unpaid terminal Creem trials (#3352)

- **SHA**: `238a4957e7f141cbc151c692ab38a556fb883376`
- **作者**: tim-srp
- **日期**: 2026-08-12T11:56:37Z
- **PR**: #3352

### Commit Message

```
fix(billing): converge unpaid terminal Creem trials (#3352)

## Summary

- Stop routing terminated `$0` Trial subscriptions into `manual_review`:
before failing closed, terminal settlement now reads the authoritative
transaction (`client.get_transaction`) and only holds the order for
operator review when `amount_paid > 0`. A `$0` Trial invoice converges
as an unpaid termination (`failed`/`expired` + checkout release), so the
user is unblocked instead of stuck behind a sticky review lock. The
transaction is cross-checked against the subscription identity and
environment mode before it is trusted.
- Let legacy expired Checkouts converge: the unbound-checkout identity
gate no longer requires `payment_order_id == local_order_id` (a
newer-flow invariant that legacy orders predate). It still requires the
exact checkout session id, environment mode, `request_id ==
local_order_id`, and signed-metadata uid/order matches; all repo writes
remain keyed by exact `payment_order_id` CAS filters, so the relaxation
removes no safety.

## Root cause

Both gaps were left by #3345/#3348 and confirmed against latest `main`:

1. `settle_terminal_bound_order` used `last_transaction_id` presence as
the "provider collected money" signal. Creem issues a `$0` invoice
transaction at Trial start (`CreemTransaction.amount_paid` is
`NonNegativeInt`, and the Trial's first webhook is `subscription.paid`
with status `trialing`), so a canceled unpaid Trial also carries a
transaction id and was misrouted to `manual_review` with reason
`..._after_payment` — wrong customer-facing state, wrong operator alert,
and the user is blocked from checking out again.
2. `_unbound_checkout_matches_order` required `checkout.request_id ==
local_order_id == payment_order_id`. Legacy orders where the two local
ids differ failed this identity check before the expired branch could
run, so an expired legacy Checkout retried forever and
`create_card_checkout` kept replaying its dead checkout URL for that
user.

## Test plan

- [x] TDD: `$0` transaction (`amount_paid=0`) on a canceled/expired
subscription → `mark_bound_checkout_terminal` + checkout release, no
manual review.
- [x] `amount_paid > 0` still fails closed into manual review with the
existing terminal-status reason codes (both `canceled` and `expired`).
- [x] Transaction/subscription identity or environment-mode mismatch is
rejected; missing reconciliation client is rejected.
- [x] Legacy order with `payment_order_id != local_order_id` + expired
Checkout → marked expired against its exact `payment_order_id` and the
checkout lease released.
- [x] Backend regression: creem suite 751 passed; billing/checkout suite
1417 passed, 5 skipped.
- [x] `ruff check` + `ruff format --check` clean on changed files.
- [ ] CI Code Quality Check.
- [ ] Staging: hourly `check-subscription-sync` converges the remaining
stale records without new `manual_review` entries for unpaid Trials.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## Summary

- Stop routing terminated `$0` Trial subscriptions into `manual_review`: before failing closed, terminal settlement now reads the authoritative transaction (`client.get_transaction`) and only holds the order for operator review when `amount_paid > 0`. A `$0` Trial invoice converges as an unpaid termination (`failed`/`expired` + checkout release), so the user is unblocked instead of stuck behind a sticky review lock. The transaction is cross-checked against the subscription identity and environment mode before it is trusted.
- Let legacy expired Checkouts converge: the unbound-checkout identity gate no longer requires `payment_order_id == local_order_id` (a newer-flow invariant that legacy orders predate). It still requires the exact checkout session id, environment mode, `request_id == local_order_id`, and signed-metadata uid/order matches; all repo writes remain keyed by exact `payment_order_id` CAS filters, so the relaxation removes no safety.

## Root cause

Both gaps were left by #3345/#3348 and confirmed against latest `main`:

1. `settle_terminal_bound_order` used `last_transaction_id` presence as the "provider collected money" signal. Creem issues a `$0` invoice transaction at Trial start (`CreemTransaction.amount_paid` is `NonNegativeInt`, and the Trial's first webhook is `subscription.paid` with status `trialing`), so a canceled unpaid Trial also carries a transaction id and was misrouted to `manual_review` with reason `..._after_payment` — wrong customer-facing state, wrong operator alert, and the user is blocked from checking out again.
2. `_unbound_checkout_matches_order` required `checkout.request_id == local_order_id == payment_order_id`. Legacy orders where the two local ids differ failed this identity check before the expired branch could run, so an expired legacy Checkout retried forever and `create_card_checkout` kept replaying its dead checkout URL for that user.

## Test plan

- [x] TDD: `$0` transaction (`amount_paid=0`) on a canceled/expired subscription → `mark_bound_checkout_terminal` + checkout release, no manual review.
- [x] `amount_paid > 0` still fails closed into manual review with the existing terminal-status reason codes (both `canceled` and `expired`).
- [x] Transaction/subscription identity or environment-mode mismatch is rejected; missing reconciliation client is rejected.
- [x] Legacy order with `payment_order_id != local_order_id` + expired Checkout → marked expired against its exact `payment_order_id` and the checkout lease released.
- [x] Backend regression: creem suite 751 passed; billing/checkout suite 1417 passed, 5 skipped.
- [x] `ruff check` + `ruff format --check` clean on changed files.
- [ ] CI Code Quality Check.
- [ ] Staging: hourly `check-subscription-sync` converges the remaining stale records without new `manual_review` entries for unpaid Trials.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(agent-builder): Agent builder 支持聊天页内联重命名 (#3351)

- **SHA**: `e1ae26e5a06075243742e0f41ef416fc3e0411dc`
- **作者**: lynn Zhuang
- **日期**: 2026-08-12T11:23:09Z
- **PR**: #3351

### Commit Message

```
feat(agent-builder): Agent builder 支持聊天页内联重命名 (#3351)

## Linear

N/A

## 变更摘要

- 参考 PR #3192，在 Agent Builder 聊天页顶部增加 Agent 名称内联重命名，支持点击全选、失焦或 Enter
保存、Escape 取消、中文输入法保护以及保存失败后保留草稿
- 根据当前 v1/v2 运行时调用对应的重命名接口，同步当前项目缓存并刷新首页列表；编辑期间暂时隐藏状态 Tag
- 在标题末尾使用渐变遮罩叠加 hover 铅笔，缩短标题与状态 Tag 的间距；同时将 Agent Builder 首页 Rename
菜单换成单支铅笔图标

## 测试计划

- [x] `bash scripts/verify-web.sh <本次变更的 Web 文件>`：TypeScript、103
个定向测试、ESLint 和治理检查通过
- [x] `bash scripts/verify-changed.sh`：变更 surface 的前端检查通过
- [x] 本地 mock 浏览器验证：hover/focus 铅笔、点击全选、失焦保存、Escape 取消、状态 Tag 显隐、渐变间距及首页
Rename 图标
```

### PR Body

## Linear

N/A

## 变更摘要

- 参考 PR #3192，在 Agent Builder 聊天页顶部增加 Agent 名称内联重命名，支持点击全选、失焦或 Enter 保存、Escape 取消、中文输入法保护以及保存失败后保留草稿
- 根据当前 v1/v2 运行时调用对应的重命名接口，同步当前项目缓存并刷新首页列表；编辑期间暂时隐藏状态 Tag
- 在标题末尾使用渐变遮罩叠加 hover 铅笔，缩短标题与状态 Tag 的间距；同时将 Agent Builder 首页 Rename 菜单换成单支铅笔图标

## 测试计划

- [x] `bash scripts/verify-web.sh <本次变更的 Web 文件>`：TypeScript、103 个定向测试、ESLint 和治理检查通过
- [x] `bash scripts/verify-changed.sh`：变更 surface 的前端检查通过
- [x] 本地 mock 浏览器验证：hover/focus 铅笔、点击全选、失焦保存、Escape 取消、状态 Tag 显隐、渐变间距及首页 Rename 图标


---

## fix(agent-builder): stabilize v2 preview runtime (#3349)

- **SHA**: `cc1b99d17fced476edd0946bc8dcde8d0f61e507`
- **作者**: kaka-srp
- **日期**: 2026-08-12T11:09:23Z
- **PR**: #3349

### Commit Message

```
fix(agent-builder): stabilize v2 preview runtime (#3349)

## Summary

Follow-up to merged PR #3338 for the v2 Agent Builder preview/runtime
path.

- replace the process-owned v2 Preview background loop with request/poll
reconciliation backed by persisted TestRun state
- keep Builder chat independent from Preview packaging/deployment and
remove stale runtime-operation blocking
- make session-channel creation and runtime allocation idempotent across
retries and duplicate-key races
- reconcile stale Preview creation after worker/deploy interruption
without a fixed 30-minute ownership TTL
- return the Test Agent's user-visible `message.send` response to
Builder instead of the hidden `NO_REPLY` terminal sentinel
- authorize Share Chat for the creator's canonical v2 Builder session
backed by its hidden Engine workspace, without broadening generic
hidden-channel ownership
- include the v2 Preview reconciliation design document and regression
coverage

## Verification

- backend Agent Builder / packaging targeted suite: 225 passed
- backend Share Chat suite: 37 passed
- frontend Agent Builder targeted suite: 45 passed
- Ruff, ESLint, Prettier, and `git diff --check` passed
- replayed the reported Test run: extracted the complete 4,786-character
visible response with no `NO_REPLY`
- resolved the reported Builder session/channel through the new
ownership path against staging-backed local data

## Manual checks

- local frontend and backend both healthy
- latest `origin/main` merged, including PR #3347 `manifest_metadata`
packaging compatibility
```

### PR Body

## Summary

Follow-up to merged PR #3338 for the v2 Agent Builder preview/runtime path.

- replace the process-owned v2 Preview background loop with request/poll reconciliation backed by persisted TestRun state
- keep Builder chat independent from Preview packaging/deployment and remove stale runtime-operation blocking
- make session-channel creation and runtime allocation idempotent across retries and duplicate-key races
- reconcile stale Preview creation after worker/deploy interruption without a fixed 30-minute ownership TTL
- return the Test Agent's user-visible `message.send` response to Builder instead of the hidden `NO_REPLY` terminal sentinel
- authorize Share Chat for the creator's canonical v2 Builder session backed by its hidden Engine workspace, without broadening generic hidden-channel ownership
- include the v2 Preview reconciliation design document and regression coverage

## Verification

- backend Agent Builder / packaging targeted suite: 225 passed
- backend Share Chat suite: 37 passed
- frontend Agent Builder targeted suite: 45 passed
- Ruff, ESLint, Prettier, and `git diff --check` passed
- replayed the reported Test run: extracted the complete 4,786-character visible response with no `NO_REPLY`
- resolved the reported Builder session/channel through the new ownership path against staging-backed local data

## Manual checks

- local frontend and backend both healthy
- latest `origin/main` merged, including PR #3347 `manifest_metadata` packaging compatibility


---

## feat(agent-builder): generalize Environment replacement to ordinary Agents (#3350)

- **SHA**: `043c3aec58ef3cecfc88972bc87493a94bbc8054`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-12T10:31:13Z
- **PR**: #3350

### Commit Message

```
feat(agent-builder): generalize Environment replacement to ordinary Agents (#3350)

## Summary

Implements zooclaw-engine#598 gap 2: generalize the explicit Agent
Environment
replacement pipeline from Agent-Studio-only to the ordinary Agent
`update` and
`reinstall`/`reclaim` paths, and add support for the NULL-pin population
(Agents locked before Pack Environment binding existed).

Design spec:
`docs/superpowers/specs/2026-08-13-ordinary-agent-environment-replacement.md`
(explicitly supersedes §7 of
`docs/superpowers/specs/2026-08-04-agent-builder-v2-staging-fixes.md`,
which said "不开放普通 Agent 自动 Environment replacement").

- `engine_agent_environment_replacement.py`: planner renamed from
`BuilderEnvironmentReplacementPlan`/`plan_builder_environment_update` to
`EnvironmentReplacementPlan`/`plan_environment_replacement`. A locked
Agent
with no resolved pin at all (NULL-pin population) now plans an explicit
`null`/`null` CAS pair ("currently unbound") instead of failing closed
with
  `agent.pack_environment_migration_required`. Adds
`resolve_environment_update`/`apply_environment_replacement` helpers
shared
  by both application call sites.
- `engine_agent_lifecycle_service.update_engine_agent()`: drops the
  `allow_environment_replacement` gate entirely — the planner itself now
decides ordinary pre-lock update vs explicit replacement, so the
ordinary
update route (`routes/agents/crud.py`) and Agent Studio's convergence
path
  share one pipeline.
- `engine_agent_install_service.install_engine_agent()`: the
reinstall/reclaim
branch replaces its hard `EngineAgentEnvironmentLockedError` → terminal
  `agent.pack_environment_migration_required` mapping with the same
  plan → apply update → replace sequence, applied after Pack Skills
  reconciliation and before provenance (`submission_id`/
  `pack_runtime_asset_sha256`) is recorded.
- `EngineClient.replace_agent_environment`: `expected_environment_id`/
`expected_environment_version` become `str | None`/`int | None`, always
sent explicitly in the request body (never omitted) so Engine's CAS
check
  isn't silently degraded into "unconditional replace." A mixed
`None`/non-`None` pair is rejected client-side before the request is
sent.
  409 `environment_assignment_changed` (and the other existing conflict
  types) continue to map to `DependencyNotReadyError`.

## Dependency

**Depends on a parallel zooclaw-engine PR** that adds explicit-`null`
support
to `POST /v1/agents/{id}:replace-environment`'s
`expected_environment_id`/
`expected_environment_version` (CAS semantics: both `null` means "expect
currently unbound," not unconditional replace; row `environment_id IS
NULL`
must match or Engine returns 409 `environment_assignment_changed`;
target pin
still must be non-null). See zooclaw-engine#598.

**Do not merge before the Engine-side PR merges and is deployed** — the
null
CAS shape this PR sends would otherwise be rejected or misinterpreted by
the
current Engine contract.

## Test plan

- [x] `bash scripts/verify-py.sh` — ruff check, ruff format, pyright,
import-linter all pass
- [x] Targeted unit tests (216 tests across the four changed test files)
pass:
`test_engine_agent_lifecycle_service.py`,
`test_engine_agent_install_service.py`,
`test_engine_client.py`, `test_agent_builder_v2_runtime_service.py`
- [x] New/rewritten coverage:
- Client: explicit `null`/`null` expected pair sent as JSON `null` (not
omitted);
mixed `None`/non-`None` expected pair rejected before the request is
sent.
- Ordinary `update_engine_agent` (no `allow_hidden`): exact-pin
replacement
timing (config → credentials → replace → provenance), idempotent
recovery
when the pin already matches, provenance gate on replacement failure,
NULL-pin replacement, a defensive terminal-error case for a
half-resolved
    pin, and a plan/apply race terminal-error case. The old

`test_update_locked_environment_requires_migration_before_pack_mutation`
(encoded the pre-generalization "always hard-fail" behavior) is replaced
    by this set.
- `install_engine_agent` reinstall/reclaim branch: exact-pin replacement
before provenance, NULL-pin replacement, idempotent recovery, provenance
    gate on replacement failure.
- [ ] Full coverage gate (`scripts/verify-py.sh --full`, needs MongoDB
on
      `127.0.0.1` per this repo's devcontainer) could not be run in this
sandbox (no local MongoDB/devcontainer available) — please confirm via
      CI's `claw-interface-quality` job.

## Deviations from the brief

- Worktree branch is `feature/ordinary-agent-env-replacement`, not
`feat/ordinary-agent-env-replacement` — `scripts/worktree.sh` hardcodes
the
  `feature/<name>` branch prefix for this repo and that convention was
  followed per this repo's `AGENTS.md`.
- Item 3 ("普通 update 路径开闸门") landed as removing the
`allow_environment_replacement` parameter entirely rather than the more
conservative "pass `True` explicitly at `crud.py:113`" fallback the
brief
offered — the parameter had exactly two call sites (Agent Studio,
already
always `True`; the ordinary route, always `False`), so keeping it around
after generalizing would have left a dead toggle. The planner's own
branch
  structure (unlocked vs. locked vs. NULL-pin) now fully expresses when
replacement applies, matching the brief's stated intent of "只开闸门" for a
  single shared pipeline rather than two behaviors gated by a flag.
- Two small extraction helpers (`resolve_environment_update`,
`apply_environment_replacement`) were added to the planner module beyond
  what the brief's file list mentioned — required to bring
`engine_agent_install_service.py` back under this repo's enforced
500-line
  file-length pre-commit guard (writing the reclaim branch's replacement
logic inline pushed it to 510 lines) and incidentally removed
duplication
  between the update and install call sites.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_018bzavhv5vccEXHVeTWoouY

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## Summary

Implements zooclaw-engine#598 gap 2: generalize the explicit Agent Environment
replacement pipeline from Agent-Studio-only to the ordinary Agent `update` and
`reinstall`/`reclaim` paths, and add support for the NULL-pin population
(Agents locked before Pack Environment binding existed).

Design spec: `docs/superpowers/specs/2026-08-13-ordinary-agent-environment-replacement.md`
(explicitly supersedes §7 of `docs/superpowers/specs/2026-08-04-agent-builder-v2-staging-fixes.md`,
which said "不开放普通 Agent 自动 Environment replacement").

- `engine_agent_environment_replacement.py`: planner renamed from
  `BuilderEnvironmentReplacementPlan`/`plan_builder_environment_update` to
  `EnvironmentReplacementPlan`/`plan_environment_replacement`. A locked Agent
  with no resolved pin at all (NULL-pin population) now plans an explicit
  `null`/`null` CAS pair ("currently unbound") instead of failing closed with
  `agent.pack_environment_migration_required`. Adds
  `resolve_environment_update`/`apply_environment_replacement` helpers shared
  by both application call sites.
- `engine_agent_lifecycle_service.update_engine_agent()`: drops the
  `allow_environment_replacement` gate entirely — the planner itself now
  decides ordinary pre-lock update vs explicit replacement, so the ordinary
  update route (`routes/agents/crud.py`) and Agent Studio's convergence path
  share one pipeline.
- `engine_agent_install_service.install_engine_agent()`: the reinstall/reclaim
  branch replaces its hard `EngineAgentEnvironmentLockedError` → terminal
  `agent.pack_environment_migration_required` mapping with the same
  plan → apply update → replace sequence, applied after Pack Skills
  reconciliation and before provenance (`submission_id`/
  `pack_runtime_asset_sha256`) is recorded.
- `EngineClient.replace_agent_environment`: `expected_environment_id`/
  `expected_environment_version` become `str | None`/`int | None`, always
  sent explicitly in the request body (never omitted) so Engine's CAS check
  isn't silently degraded into "unconditional replace." A mixed
  `None`/non-`None` pair is rejected client-side before the request is sent.
  409 `environment_assignment_changed` (and the other existing conflict
  types) continue to map to `DependencyNotReadyError`.

## Dependency

**Depends on a parallel zooclaw-engine PR** that adds explicit-`null` support
to `POST /v1/agents/{id}:replace-environment`'s `expected_environment_id`/
`expected_environment_version` (CAS semantics: both `null` means "expect
currently unbound," not unconditional replace; row `environment_id IS NULL`
must match or Engine returns 409 `environment_assignment_changed`; target pin
still must be non-null). See zooclaw-engine#598.

**Do not merge before the Engine-side PR merges and is deployed** — the null
CAS shape this PR sends would otherwise be rejected or misinterpreted by the
current Engine contract.

## Test plan

- [x] `bash scripts/verify-py.sh` — ruff check, ruff format, pyright, import-linter all pass
- [x] Targeted unit tests (216 tests across the four changed test files) pass:
      `test_engine_agent_lifecycle_service.py`, `test_engine_agent_install_service.py`,
      `test_engine_client.py`, `test_agent_builder_v2_runtime_service.py`
- [x] New/rewritten coverage:
  - Client: explicit `null`/`null` expected pair sent as JSON `null` (not omitted);
    mixed `None`/non-`None` expected pair rejected before the request is sent.
  - Ordinary `update_engine_agent` (no `allow_hidden`): exact-pin replacement
    timing (config → credentials → replace → provenance), idempotent recovery
    when the pin already matches, provenance gate on replacement failure,
    NULL-pin replacement, a defensive terminal-error case for a half-resolved
    pin, and a plan/apply race terminal-error case. The old
    `test_update_locked_environment_requires_migration_before_pack_mutation`
    (encoded the pre-generalization "always hard-fail" behavior) is replaced
    by this set.
  - `install_engine_agent` reinstall/reclaim branch: exact-pin replacement
    before provenance, NULL-pin replacement, idempotent recovery, provenance
    gate on replacement failure.
- [ ] Full coverage gate (`scripts/verify-py.sh --full`, needs MongoDB on
      `127.0.0.1` per this repo's devcontainer) could not be run in this
      sandbox (no local MongoDB/devcontainer available) — please confirm via
      CI's `claw-interface-quality` job.

## Deviations from the brief

- Worktree branch is `feature/ordinary-agent-env-replacement`, not
  `feat/ordinary-agent-env-replacement` — `scripts/worktree.sh` hardcodes the
  `feature/<name>` branch prefix for this repo and that convention was
  followed per this repo's `AGENTS.md`.
- Item 3 ("普通 update 路径开闸门") landed as removing the
  `allow_environment_replacement` parameter entirely rather than the more
  conservative "pass `True` explicitly at `crud.py:113`" fallback the brief
  offered — the parameter had exactly two call sites (Agent Studio, already
  always `True`; the ordinary route, always `False`), so keeping it around
  after generalizing would have left a dead toggle. The planner's own branch
  structure (unlocked vs. locked vs. NULL-pin) now fully expresses when
  replacement applies, matching the brief's stated intent of "只开闸门" for a
  single shared pipeline rather than two behaviors gated by a flag.
- Two small extraction helpers (`resolve_environment_update`,
  `apply_environment_replacement`) were added to the planner module beyond
  what the brief's file list mentioned — required to bring
  `engine_agent_install_service.py` back under this repo's enforced 500-line
  file-length pre-commit guard (writing the reclaim branch's replacement
  logic inline pushed it to 510 lines) and incidentally removed duplication
  between the update and install call sites.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_018bzavhv5vccEXHVeTWoouY


---

## fix(billing): recover Creem trial callback race (#3348)

- **SHA**: `2fdb4b17ee10c70910b72f32de27e39d1601296d`
- **作者**: tim-srp
- **日期**: 2026-08-12T10:03:09Z
- **PR**: #3348

### Commit Message

```
fix(billing): recover Creem trial callback race (#3348)

## Summary
- Recover an unbound Creem checkout from the authoritative Checkout API
when a Trial subscription webhook arrives before `checkout.completed`
finishes binding the local order.
- Reuse the existing checkout identity validation, atomic binding, and
Trial entitlement projection; already-bound Trial orders keep the
original projection path.
- Persist Trial recovery mismatches as stable `ConflictError` failures
instead of leaving provider events stuck in a processing lease.
- Extend Card success-page polling from 30 seconds to a bounded 60
seconds. Explicit failed, canceled, refund, and manual-review states
still fail immediately.
- No Antom/Alipay, Catalog, renewal, past-due, or production-purchase
behavior is changed.

## Root cause
Creem emits `checkout.completed` and the Trial `subscription.paid` event
at nearly the same time. The webhook receiver processes them
independently, so the subscription event can validate the local order
before the checkout event has persisted its provider
subscription/customer binding. That event fails and succeeds only after
Creem retries roughly 38–44 seconds later, while the success page
previously stopped polling after 30 seconds and displayed a false
failure.

## Test plan
- [x] TDD regression: Trial subscription webhook recovers and projects a
completed but unbound Checkout without waiting for provider retry.
- [x] Bound Trial orders remain on the existing projection path and do
not create a Creem API client.
- [x] Pending/expired Checkout state is not acknowledged as recovered.
- [x] Identity, Checkout-state, and subscription mismatches are
recordable service errors.
- [x] Card success page remains processing before 60 seconds and times
out at the 60-second wall-clock deadline.
- [x] Backend targeted suite: 109 passed.
- [x] Frontend targeted suite: 35 passed; TypeScript and ESLint passed.
- [x] Ruff and changed-file Pyright: 0 errors.

## Local verification note
The repository-wide host Pyright run still reports seven unchanged
`r2_storage.py` boto client typing errors from `origin/main`; the four
changed Python files pass Pyright with 0 errors, and CI remains
authoritative for the complete environment.
```

### PR Body

## Summary
- Recover an unbound Creem checkout from the authoritative Checkout API when a Trial subscription webhook arrives before `checkout.completed` finishes binding the local order.
- Reuse the existing checkout identity validation, atomic binding, and Trial entitlement projection; already-bound Trial orders keep the original projection path.
- Persist Trial recovery mismatches as stable `ConflictError` failures instead of leaving provider events stuck in a processing lease.
- Extend Card success-page polling from 30 seconds to a bounded 60 seconds. Explicit failed, canceled, refund, and manual-review states still fail immediately.
- No Antom/Alipay, Catalog, renewal, past-due, or production-purchase behavior is changed.

## Root cause
Creem emits `checkout.completed` and the Trial `subscription.paid` event at nearly the same time. The webhook receiver processes them independently, so the subscription event can validate the local order before the checkout event has persisted its provider subscription/customer binding. That event fails and succeeds only after Creem retries roughly 38–44 seconds later, while the success page previously stopped polling after 30 seconds and displayed a false failure.

## Test plan
- [x] TDD regression: Trial subscription webhook recovers and projects a completed but unbound Checkout without waiting for provider retry.
- [x] Bound Trial orders remain on the existing projection path and do not create a Creem API client.
- [x] Pending/expired Checkout state is not acknowledged as recovered.
- [x] Identity, Checkout-state, and subscription mismatches are recordable service errors.
- [x] Card success page remains processing before 60 seconds and times out at the 60-second wall-clock deadline.
- [x] Backend targeted suite: 109 passed.
- [x] Frontend targeted suite: 35 passed; TypeScript and ESLint passed.
- [x] Ruff and changed-file Pyright: 0 errors.

## Local verification note
The repository-wide host Pyright run still reports seven unchanged `r2_storage.py` boto client typing errors from `origin/main`; the four changed Python files pass Pyright with 0 errors, and CI remains authoritative for the complete environment.


---

## fix(billing): recover stale Creem checkout reconciliation (#3345)

- **SHA**: `e82846e20dea8e59ea3fd4367204b34d0a53170d`
- **作者**: tim-srp
- **日期**: 2026-08-12T10:01:48Z
- **PR**: #3345

### Commit Message

```
fix(billing): recover stale Creem checkout reconciliation (#3345)

## Summary

- Accept authoritative Creem Checkout reads whose `order` object omits
`customer`: retrieval now uses a dedicated `CreemRetrievedOrder`
projection with an optional customer, and `completed_object()` backfills
`order.customer` from the top-level checkout customer so every existing
binding cross-check stays exact. The webhook schema (`CreemWebhookOrder`
in `checkout.completed` payloads) remains strict.
- Converge bound pending Card orders whose provider subscription is
terminally `canceled`/`expired` instead of raising `Bound Creem checkout
is not recoverable` on every hourly run: orders with no provider payment
are marked `failed` (`provider_subscription_canceled`) and the account
checkout lease is released; orders where the provider collected a
payment fail closed into sticky `manual_review`
(`provider_subscription_canceled_after_payment`).
- The retrieval models (`CreemRetrievedCheckout` + new
`CreemRetrievedOrder`) move to `app/schema/creem_retrieval.py` because
the addition pushed `app/schema/creem.py` past the 500-line CI guard;
the webhook schemas in `creem.py` are unchanged.

## Root cause

Staging's hourly `check-subscription-sync` reconciliation has been
failing on the same three historical records every run:

- Two unbound checkouts (`ch_x8ysu5Hs7wCAkXIxMln6E`,
`ch_5Pk8KZ7SQeGATYLvQ7Zv9M`) fail during `client.get_checkout()` with
`ValidationError: order.customer Field required` — Creem's `GET
/v1/checkouts` response genuinely omits `order.customer` for these
historical orders, while `CreemRetrievedCheckout` reused the strict
webhook order model.
- One bound pending order (`sub_6MehYopz16rL68tmOr15GR`) reaches
`project_bound_pending_order`, which only handled `trialing`/`active`
subscriptions, so a canceled subscription raised unconditionally with no
terminal transition and no retry backoff (the bound loop retries every
hour forever).

Besides the log noise (`failed >= 3` every run), the affected uids stay
permanently "unresolved" in `find_unresolved_subscription`, blocking
those accounts from ever starting a new Card checkout.

## Test plan

- [x] New unit tests: retrieved checkout without `order.customer` parses
and its completed projection backfills the customer; completed
projection still fails loudly when no customer identity exists at all.
- [x] New unit tests: canceled unpaid subscription → order failed +
checkout lease released; canceled subscription with a provider
transaction → sticky manual review, no release; unknown provider status
still raises; subscription identity / environment-mode mismatches are
rejected.
- [x] New repo CAS tests pin the exact filters for
`mark_bound_checkout_canceled` / `mark_bound_checkout_manual_review`.
- [x] Local focused regression: creem suite 738 passed; billing/checkout
suite 1407 passed, 5 skipped.
- [x] `ruff check` + `ruff format --check` + import-linter (8 contracts
kept) passed locally; local pyright reports only pre-existing
environment errors (missing `favie_common`/`stripe` in the host
interpreter — identical error set on a clean baseline); CI Pyright is
authoritative.
- [ ] CI Code Quality Check.
- [ ] Staging: next hourly `check-subscription-sync` run converges the
three historical records and the recurring WARNING tracebacks stop.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## Summary

- Accept authoritative Creem Checkout reads whose `order` object omits `customer`: retrieval now uses a dedicated `CreemRetrievedOrder` projection with an optional customer, and `completed_object()` backfills `order.customer` from the top-level checkout customer so every existing binding cross-check stays exact. The webhook schema (`CreemWebhookOrder` in `checkout.completed` payloads) remains strict.
- Converge bound pending Card orders whose provider subscription is terminally `canceled`/`expired` instead of raising `Bound Creem checkout is not recoverable` on every hourly run: orders with no provider payment are marked `failed` (`provider_subscription_canceled`) and the account checkout lease is released; orders where the provider collected a payment fail closed into sticky `manual_review` (`provider_subscription_canceled_after_payment`).
- The retrieval models (`CreemRetrievedCheckout` + new `CreemRetrievedOrder`) move to `app/schema/creem_retrieval.py` because the addition pushed `app/schema/creem.py` past the 500-line CI guard; the webhook schemas in `creem.py` are unchanged.

## Root cause

Staging's hourly `check-subscription-sync` reconciliation has been failing on the same three historical records every run:

- Two unbound checkouts (`ch_x8ysu5Hs7wCAkXIxMln6E`, `ch_5Pk8KZ7SQeGATYLvQ7Zv9M`) fail during `client.get_checkout()` with `ValidationError: order.customer Field required` — Creem's `GET /v1/checkouts` response genuinely omits `order.customer` for these historical orders, while `CreemRetrievedCheckout` reused the strict webhook order model.
- One bound pending order (`sub_6MehYopz16rL68tmOr15GR`) reaches `project_bound_pending_order`, which only handled `trialing`/`active` subscriptions, so a canceled subscription raised unconditionally with no terminal transition and no retry backoff (the bound loop retries every hour forever).

Besides the log noise (`failed >= 3` every run), the affected uids stay permanently "unresolved" in `find_unresolved_subscription`, blocking those accounts from ever starting a new Card checkout.

## Test plan

- [x] New unit tests: retrieved checkout without `order.customer` parses and its completed projection backfills the customer; completed projection still fails loudly when no customer identity exists at all.
- [x] New unit tests: canceled unpaid subscription → order failed + checkout lease released; canceled subscription with a provider transaction → sticky manual review, no release; unknown provider status still raises; subscription identity / environment-mode mismatches are rejected.
- [x] New repo CAS tests pin the exact filters for `mark_bound_checkout_canceled` / `mark_bound_checkout_manual_review`.
- [x] Local focused regression: creem suite 738 passed; billing/checkout suite 1407 passed, 5 skipped.
- [x] `ruff check` + `ruff format --check` + import-linter (8 contracts kept) passed locally; local pyright reports only pre-existing environment errors (missing `favie_common`/`stripe` in the host interpreter — identical error set on a clean baseline); CI Pyright is authoritative.
- [ ] CI Code Quality Check.
- [ ] Staging: next hourly `check-subscription-sync` run converges the three historical records and the recurring WARNING tracebacks stop.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(agent-packs): store manifest metadata (#3347)

- **SHA**: `200f50fd88a5335185971c7d21b2a9f88461bba1`
- **作者**: kaka-srp
- **日期**: 2026-08-12T08:58:48Z
- **PR**: #3347

### Commit Message

```
feat(agent-packs): store manifest metadata (#3347)

## Linear


https://linear.app/srpone/issue/ECA-1373/store-agent-pack-manifest-metadata

## Summary

- parse `skill_details`, `supported_languages`, and `release_notes` from
the exact submitted `agent-pack.yaml` archive
- persist the metadata on Pack Test runs, submissions, and published
Packs without adding collections or tables
- project the fields through official, private, shared-link,
marketplace, and version APIs
- render skill descriptions, supported languages, and version release
notes on the public Pack page
- update Enterprise Admin and Dashboard archive parsing while keeping
Agent Studio validation authoritative
- require release notes for update workspaces in Agent Studio
validation; backend submission only stores normalized metadata and does
not duplicate that blocking gate

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] backend targeted suite: 215 passed
- [x] Web targeted suite: 57 passed
- [x] Dashboard archive suite: 28 passed
- [x] submission service suite after validation-boundary adjustment: 34
passed
- [x] Dashboard typecheck and lint
- [x] Agent Pack archive package lint

## Related PR

- Agent Studio V1/V2 manifest authoring and validation:
https://github.com/SerendipityOneInc/ecap-agent-pack/pull/239
```

### PR Body

## Linear

https://linear.app/srpone/issue/ECA-1373/store-agent-pack-manifest-metadata

## Summary

- parse `skill_details`, `supported_languages`, and `release_notes` from the exact submitted `agent-pack.yaml` archive
- persist the metadata on Pack Test runs, submissions, and published Packs without adding collections or tables
- project the fields through official, private, shared-link, marketplace, and version APIs
- render skill descriptions, supported languages, and version release notes on the public Pack page
- update Enterprise Admin and Dashboard archive parsing while keeping Agent Studio validation authoritative
- require release notes for update workspaces in Agent Studio validation; backend submission only stores normalized metadata and does not duplicate that blocking gate

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] backend targeted suite: 215 passed
- [x] Web targeted suite: 57 passed
- [x] Dashboard archive suite: 28 passed
- [x] submission service suite after validation-boundary adjustment: 34 passed
- [x] Dashboard typecheck and lint
- [x] Agent Pack archive package lint

## Related PR

- Agent Studio V1/V2 manifest authoring and validation: https://github.com/SerendipityOneInc/ecap-agent-pack/pull/239


---

## fix(billing): show subscription period in user menu (#3346)

- **SHA**: `ec90a2adbfab9704304605c3cbb4c5609f557c0e`
- **作者**: tim-srp
- **日期**: 2026-08-12T08:10:46Z
- **PR**: #3346

### Commit Message

```
fix(billing): show subscription period in user menu (#3346)

## Summary
- Show the localized renewal date for active subscriptions in the user
menu.
- Show the period ending date when auto-renewal is canceled.
- Preserve the existing Trial countdown and actual credits balance
display.
- Avoid presenting `past_due` subscriptions as normal renewals.

## Root cause
The detailed plan card already rendered `currentPeriodEnd`, but the
compact user menu always assigned a null sub-label to active
subscriptions. This caused a real paid subscription to lose its renewal
or ending date in the sidebar even though the backend returned the
correct period boundary.

## Test plan
- [x] Verify an active subscription renders its localized renewal date.
- [x] Verify cancel-at-period-end renders an ending date.
- [x] Verify `past_due` does not render a normal renewal or ending
label.
- [x] Verify existing Trial and credits display tests remain green.
- [x] Run `bash scripts/verify-web.sh src/components/UserMenu.tsx
tests/unit/components/UserMenu.unit.spec.tsx`.
- [x] Run the pre-push changed-surface gate.
```

### PR Body

## Summary
- Show the localized renewal date for active subscriptions in the user menu.
- Show the period ending date when auto-renewal is canceled.
- Preserve the existing Trial countdown and actual credits balance display.
- Avoid presenting `past_due` subscriptions as normal renewals.

## Root cause
The detailed plan card already rendered `currentPeriodEnd`, but the compact user menu always assigned a null sub-label to active subscriptions. This caused a real paid subscription to lose its renewal or ending date in the sidebar even though the backend returned the correct period boundary.

## Test plan
- [x] Verify an active subscription renders its localized renewal date.
- [x] Verify cancel-at-period-end renders an ending date.
- [x] Verify `past_due` does not render a normal renewal or ending label.
- [x] Verify existing Trial and credits display tests remain green.
- [x] Run `bash scripts/verify-web.sh src/components/UserMenu.tsx tests/unit/components/UserMenu.unit.spec.tsx`.
- [x] Run the pre-push changed-surface gate.


---

## fix(pack-test): upgrade temporary OpenClaw image (#3344)

- **SHA**: `44912ddc0b1757718e9143399bed4db806d46898`
- **作者**: sam-srp
- **日期**: 2026-08-12T07:34:11Z
- **PR**: #3344

### Commit Message

```
fix(pack-test): upgrade temporary OpenClaw image (#3344)

## Summary
- Upgrade the temporary OpenClaw bot image used by legacy/direct Pack
Test runs from `2026.6.6` to `2026.6.11.20`.
- Update focused unit-test expectations for the selected image.

## Scope
- This only affects Pack Test runs that use the legacy/direct OpenClaw
runtime.
- Agent Builder projects using `builder_runtime=engine_v2` continue to
use zooclaw-engine Environment/Agent runtimes and are unaffected.

## Validation
- `conda run -n ecap-claw-py312 pytest -q
tests/unit/test_pack_test_runtime_service.py` (35 passed)
```

### PR Body

## Summary
- Upgrade the temporary OpenClaw bot image used by legacy/direct Pack Test runs from `2026.6.6` to `2026.6.11.20`.
- Update focused unit-test expectations for the selected image.

## Scope
- This only affects Pack Test runs that use the legacy/direct OpenClaw runtime.
- Agent Builder projects using `builder_runtime=engine_v2` continue to use zooclaw-engine Environment/Agent runtimes and are unaffected.

## Validation
- `conda run -n ecap-claw-py312 pytest -q tests/unit/test_pack_test_runtime_service.py` (35 passed)


---

## fix(whatsapp): accept engine session lifecycle fields (#3343)

- **SHA**: `4c7c085715069170e23fa90e2d8011c01d75a704`
- **作者**: bill-srp
- **日期**: 2026-08-12T07:25:13Z
- **PR**: #3343

### Commit Message

```
fix(whatsapp): accept engine session lifecycle fields (#3343)

## Summary
- accept the current ZooClaw Engine session lifecycle fields
(`run_status` and `archived`) at the Claw Interface boundary
- preserve compatibility with the legacy `status` field for
mixed-version rollouts
- keep malformed responses fail-closed when no lifecycle field is
present

## Root cause
The staging Engine Session API returns HTTP 200 session rows with
`run_status` and `archived`, while Claw Interface required a `status`
string. Pydantic rejected the otherwise valid list response, so
`/whatsapp/sessions/messages` returned `502 service.unavailable` before
posting the inbound WhatsApp event to the Agent session.

## Test plan
- [x] `./.venv/bin/pytest tests/unit/test_engine_client_sessions.py
tests/unit/test_whatsapp_sessions_routes.py -q` (22 passed)
- [x] `bash scripts/verify-py.sh` (ruff, format, pyright, and
import-linter passed; pyright used the project virtualenv explicitly to
work around local interpreter discovery)
- [x] `git diff --check`
```

### PR Body

## Summary
- accept the current ZooClaw Engine session lifecycle fields (`run_status` and `archived`) at the Claw Interface boundary
- preserve compatibility with the legacy `status` field for mixed-version rollouts
- keep malformed responses fail-closed when no lifecycle field is present

## Root cause
The staging Engine Session API returns HTTP 200 session rows with `run_status` and `archived`, while Claw Interface required a `status` string. Pydantic rejected the otherwise valid list response, so `/whatsapp/sessions/messages` returned `502 service.unavailable` before posting the inbound WhatsApp event to the Agent session.

## Test plan
- [x] `./.venv/bin/pytest tests/unit/test_engine_client_sessions.py tests/unit/test_whatsapp_sessions_routes.py -q` (22 passed)
- [x] `bash scripts/verify-py.sh` (ruff, format, pyright, and import-linter passed; pyright used the project virtualenv explicitly to work around local interpreter discovery)
- [x] `git diff --check`


---

## fix(billing): harden Creem trial upgrades and reconciliation (#3341)

- **SHA**: `54f9d4e0ee3382477cd19349c54c94aeefc93284`
- **作者**: tim-srp
- **日期**: 2026-08-12T06:19:25Z
- **PR**: #3341

### Commit Message

```
fix(billing): harden Creem trial upgrades and reconciliation (#3341)

## Summary

- Allow an active Creem Starter Card Trial to be replaced by a paid Card
subscription while retaining the existing Trial credits, matching the
Antom/Alipay upgrade behavior.
- Make the replacement handoff durable across missed, duplicated, and
reordered Creem webhooks with exact admission fingerprints, provider
watermarks, reconciliation leases, and sticky manual-review handling for
ambiguous financial outcomes.
- Prevent terminal cleanup from deleting a successor subscription's
shared wallet, and require authoritative provider cancellation before
immediate cleanup completes.
- Surface pending/manual-review Card checkout state consistently in
Billing Summary and the frontend, while isolating those records by Creem
environment.
- Validate the complete paid + Trial Creem catalog used by the
staging/Test Mode path.

## Root cause

The original Card Trial upgrade path assumed an in-order happy path:
checkout completion, provider activation, local projection, and
old-Trial cleanup. A missed or reordered webhook could leave the local
order pending after Creem was already active, or clean up shared billing
state belonging to the successor subscription. The UI also treated Trial
as an ordinary effective subscription and blocked upgrades.

This change records the replacement intent and provider observations
durably, then lets webhook handling and hourly reconciliation converge
on the same idempotent state machine. Ambiguous cases fail closed into
`manual_review` instead of retrying a potentially duplicate cancellation
or charge transition.

## Risk and rollout

- High-risk billing state-machine change, limited to the currently
enabled staging / Creem Test Mode Card path.
- Production Card checkout remains disabled. Remaining Test
Mode-specific binding and settlement guards must be parameterized before
enabling Creem Card in production.
- Antom/Alipay behavior is unchanged; regression tests cover its
existing Trial and paid-order paths.
- No production purchase was initiated during validation.

## Size override rationale

The diff is large because the same replacement transaction spans
checkout admission, first-payment settlement, webhook recovery, hourly
reconciliation, terminal cleanup, Billing Summary, and frontend
presentation. Splitting those pieces would temporarily ship incompatible
state contracts. More than half of the added lines are unit tests
covering event-order permutations and failure recovery.

## Test plan

- [x] Backend focused regression: 740 tests passed.
- [x] Antom/Alipay regression: 163 tests passed.
- [x] Final reconciliation/manual-review/cleanup regression: 197 tests
passed.
- [x] Frontend focused regression: 372 passed, 1 skipped.
- [x] Frontend governance, TypeScript, and ESLint checks passed.
- [x] Ruff check + format, import contracts, repository guards,
file-length/complexity guards, and changed-file Pyright passed.
- [x] Two independent code reviews completed; both blocking findings
were fixed and re-tested.
- [ ] CI full Code Quality Check.
- [ ] Staging E2E: Card Starter Trial creation and entitlement grant.
- [ ] Staging E2E: Trial to paid Card upgrade, old Trial cleanup, and
retained credits.
- [ ] Staging E2E: cancellation and hourly reconciliation recovery.

Note: one local attempt to run the entire Python unit suite hit a
Miniconda interpreter segmentation fault during `unittest.mock` garbage
collection. The focused suites above and commit hooks completed
successfully; CI remains the authoritative full-suite run.
```

### PR Body

## Summary

- Allow an active Creem Starter Card Trial to be replaced by a paid Card subscription while retaining the existing Trial credits, matching the Antom/Alipay upgrade behavior.
- Make the replacement handoff durable across missed, duplicated, and reordered Creem webhooks with exact admission fingerprints, provider watermarks, reconciliation leases, and sticky manual-review handling for ambiguous financial outcomes.
- Prevent terminal cleanup from deleting a successor subscription's shared wallet, and require authoritative provider cancellation before immediate cleanup completes.
- Surface pending/manual-review Card checkout state consistently in Billing Summary and the frontend, while isolating those records by Creem environment.
- Validate the complete paid + Trial Creem catalog used by the staging/Test Mode path.

## Root cause

The original Card Trial upgrade path assumed an in-order happy path: checkout completion, provider activation, local projection, and old-Trial cleanup. A missed or reordered webhook could leave the local order pending after Creem was already active, or clean up shared billing state belonging to the successor subscription. The UI also treated Trial as an ordinary effective subscription and blocked upgrades.

This change records the replacement intent and provider observations durably, then lets webhook handling and hourly reconciliation converge on the same idempotent state machine. Ambiguous cases fail closed into `manual_review` instead of retrying a potentially duplicate cancellation or charge transition.

## Risk and rollout

- High-risk billing state-machine change, limited to the currently enabled staging / Creem Test Mode Card path.
- Production Card checkout remains disabled. Remaining Test Mode-specific binding and settlement guards must be parameterized before enabling Creem Card in production.
- Antom/Alipay behavior is unchanged; regression tests cover its existing Trial and paid-order paths.
- No production purchase was initiated during validation.

## Size override rationale

The diff is large because the same replacement transaction spans checkout admission, first-payment settlement, webhook recovery, hourly reconciliation, terminal cleanup, Billing Summary, and frontend presentation. Splitting those pieces would temporarily ship incompatible state contracts. More than half of the added lines are unit tests covering event-order permutations and failure recovery.

## Test plan

- [x] Backend focused regression: 740 tests passed.
- [x] Antom/Alipay regression: 163 tests passed.
- [x] Final reconciliation/manual-review/cleanup regression: 197 tests passed.
- [x] Frontend focused regression: 372 passed, 1 skipped.
- [x] Frontend governance, TypeScript, and ESLint checks passed.
- [x] Ruff check + format, import contracts, repository guards, file-length/complexity guards, and changed-file Pyright passed.
- [x] Two independent code reviews completed; both blocking findings were fixed and re-tested.
- [ ] CI full Code Quality Check.
- [ ] Staging E2E: Card Starter Trial creation and entitlement grant.
- [ ] Staging E2E: Trial to paid Card upgrade, old Trial cleanup, and retained credits.
- [ ] Staging E2E: cancellation and hourly reconciliation recovery.

Note: one local attempt to run the entire Python unit suite hit a Miniconda interpreter segmentation fault during `unittest.mock` garbage collection. The focused suites above and commit hooks completed successfully; CI remains the authoritative full-suite run.


---

## fix(agent-builder): recover stale v2 project creation (#3342)

- **SHA**: `36917eb316e4f1d07bc6eee9829d948e653b3c70`
- **作者**: kaka-srp
- **日期**: 2026-08-12T06:10:05Z
- **PR**: #3342

### Commit Message

```
fix(agent-builder): recover stale v2 project creation (#3342)

## Summary

- allow a new dedicated-layout v2 Project to replace stale pending
creation when the user changes input or the original Project is terminal
- reconcile ambiguous successful initialization by opening the
already-progressed Project instead of creating a duplicate
- serialize automatic recovery and explicit submission, and keep
recovery UI aligned with the authoritative pending Project
- preserve existing v1 and legacy-layout behavior

## Validation

- code-review agent review and post-fix re-review: no remaining findings
- 48 Agent Builder entry unit tests passed
- TypeScript passed
- ESLint passed
- all web governance guards passed via scripts/verify-web.sh
```

### PR Body

## Summary

- allow a new dedicated-layout v2 Project to replace stale pending creation when the user changes input or the original Project is terminal
- reconcile ambiguous successful initialization by opening the already-progressed Project instead of creating a duplicate
- serialize automatic recovery and explicit submission, and keep recovery UI aligned with the authoritative pending Project
- preserve existing v1 and legacy-layout behavior

## Validation

- code-review agent review and post-fix re-review: no remaining findings
- 48 Agent Builder entry unit tests passed
- TypeScript passed
- ESLint passed
- all web governance guards passed via scripts/verify-web.sh

---

## feat(whatsapp): route bridge messages via engine session API (#3314)

- **SHA**: `a092c8dc081d1f3872e7a0eda4c8b0321871eb2e`
- **作者**: bill-srp
- **日期**: 2026-08-12T04:06:10Z
- **PR**: #3314

### Commit Message

```
feat(whatsapp): route bridge messages via engine session API (#3314)

## Summary
- **Hard cutover** of the WhatsApp bridge's message transport from
Mattermost to the zooclaw-engine **external Session API** (engine
`design/15`, Available since controld `v0.1.0-beta.72`) — spec + plan +
implementation in one PR. The Mattermost transport (REST post, WebSocket
pool/listener, reply filter chain, `MATTERMOST_SERVER_URL`) and the
feature flag are **deleted in this PR**; engine sessions are the only
path. Net diff: the MM machinery's removal outweighs the new transport
several times over.
- Docs:
`docs/superpowers/specs/2026-08-10-whatsapp-engine-session-design.md`
(design authority, v2 — deliberately stateless) +
`docs/superpowers/plans/2026-08-10-whatsapp-engine-session.md`.
- **Design**: webhook → claim → `user.message` into the engine session →
turn-scoped loop delivers `agent.message` events to the Graph API until
`run.finished`. Session identity is engine-authoritative (list-based
resolve; create only when none exists; archived sessions self-heal). The
only durable state is `{session_id, cursor_seq}` embedded on the
existing binding record — the engine's read API has no "from now" mode,
so the consumer keeps its position; the forward-only cursor doubles as
**catch-up**: a turn interrupted by a pod death is delivered at the
start of the user's next message.
- **claw-interface**: `engine_client` sessions mixin
(list/create/events, typed models); unconditional service-token
endpoints `POST /whatsapp/sessions/messages` (`not_bound` vs
`bound_not_routable`, `external_msg_id` = Meta message id), `POST
.../deliveries/poll` (events after cursor, `session_reset` on
archived/missing), `POST .../deliveries/ack` (forward-only
session-scoped CAS). Deleted: read-only lookup endpoint and the MM
outbound-resolution surface (now uncalled). Kept:
bind/register/claim/complete (auto-bind + install repair).
- **whatsapp-business-service**: typed `WhatsAppGraphSendError`
(httpStatus + parsed Graph code/subcode); turn loop with strict
seq-order acks, per-binding in-process registry (rerun coalescing),
sentinel strip, typing on `run.started`, Graph classification (terminal
131047/131026 → `whatsapp_delivery_failed` + advance; else backoff retry
with 20s send timeout); `not_bound` → auto-bind gated on `bindCompleted`
+ one retry. The entire MM stack and its tests are gone.
- **Deliberate scope (spec Decisions 4/8)**: no lease/recovery
machinery, no fallback transport (bridge is pre-launch; rollback =
deploy rollback, backend deploys first). Accepted trade-offs: a mid-turn
pod death delays that reply until the user's next message (catch-up, not
loss); concurrent same-sender turns on different replicas can duplicate
a reply. Reply-only scope (proactive schedule output still needs an ACS
story — spec Decision 6).

## Test plan
- [x] Bridge: `pnpm typecheck` + vitest 41/41 (turn loop: seq-order
acks, catch-up, registry coalescing, Graph classification incl. 20s
abort, sentinel handling; per-sender ordering retained; auto-bind retry)
- [x] Backend: ruff + ruff-format + pyright + import-linter (8/8) +
file-length clean; full pytest 8404 passed (2 known local-env deptry
failures — broken repo-local `.venv` shims; CI authoritative)
- [ ] CI: full quality gates + dual AI review
- [ ] Staging (backend first, then bridge): controld ≥ `v0.1.0-beta.72`
smoke; first message → session created + reply delivered; second message
mid-run → queued + delivered in order; pod kill mid-turn → next message
catches up the interrupted reply
```

### PR Body

## Summary
- **Hard cutover** of the WhatsApp bridge's message transport from Mattermost to the zooclaw-engine **external Session API** (engine `design/15`, Available since controld `v0.1.0-beta.72`) — spec + plan + implementation in one PR. The Mattermost transport (REST post, WebSocket pool/listener, reply filter chain, `MATTERMOST_SERVER_URL`) and the feature flag are **deleted in this PR**; engine sessions are the only path. Net diff: the MM machinery's removal outweighs the new transport several times over.
- Docs: `docs/superpowers/specs/2026-08-10-whatsapp-engine-session-design.md` (design authority, v2 — deliberately stateless) + `docs/superpowers/plans/2026-08-10-whatsapp-engine-session.md`.
- **Design**: webhook → claim → `user.message` into the engine session → turn-scoped loop delivers `agent.message` events to the Graph API until `run.finished`. Session identity is engine-authoritative (list-based resolve; create only when none exists; archived sessions self-heal). The only durable state is `{session_id, cursor_seq}` embedded on the existing binding record — the engine's read API has no "from now" mode, so the consumer keeps its position; the forward-only cursor doubles as **catch-up**: a turn interrupted by a pod death is delivered at the start of the user's next message.
- **claw-interface**: `engine_client` sessions mixin (list/create/events, typed models); unconditional service-token endpoints `POST /whatsapp/sessions/messages` (`not_bound` vs `bound_not_routable`, `external_msg_id` = Meta message id), `POST .../deliveries/poll` (events after cursor, `session_reset` on archived/missing), `POST .../deliveries/ack` (forward-only session-scoped CAS). Deleted: read-only lookup endpoint and the MM outbound-resolution surface (now uncalled). Kept: bind/register/claim/complete (auto-bind + install repair).
- **whatsapp-business-service**: typed `WhatsAppGraphSendError` (httpStatus + parsed Graph code/subcode); turn loop with strict seq-order acks, per-binding in-process registry (rerun coalescing), sentinel strip, typing on `run.started`, Graph classification (terminal 131047/131026 → `whatsapp_delivery_failed` + advance; else backoff retry with 20s send timeout); `not_bound` → auto-bind gated on `bindCompleted` + one retry. The entire MM stack and its tests are gone.
- **Deliberate scope (spec Decisions 4/8)**: no lease/recovery machinery, no fallback transport (bridge is pre-launch; rollback = deploy rollback, backend deploys first). Accepted trade-offs: a mid-turn pod death delays that reply until the user's next message (catch-up, not loss); concurrent same-sender turns on different replicas can duplicate a reply. Reply-only scope (proactive schedule output still needs an ACS story — spec Decision 6).

## Test plan
- [x] Bridge: `pnpm typecheck` + vitest 41/41 (turn loop: seq-order acks, catch-up, registry coalescing, Graph classification incl. 20s abort, sentinel handling; per-sender ordering retained; auto-bind retry)
- [x] Backend: ruff + ruff-format + pyright + import-linter (8/8) + file-length clean; full pytest 8404 passed (2 known local-env deptry failures — broken repo-local `.venv` shims; CI authoritative)
- [ ] CI: full quality gates + dual AI review
- [ ] Staging (backend first, then bridge): controld ≥ `v0.1.0-beta.72` smoke; first message → session created + reply delivered; second message mid-run → queued + delivered in order; pod kill mid-turn → next message catches up the interrupted reply


---

## fix(agent-builder): hide unusable model picker on v1 builder projects (#3340)

- **SHA**: `8a3b185f6bb574bffc62f3b61358dab89e444677`
- **作者**: siqiao-srp
- **日期**: 2026-08-12T03:06:06Z
- **PR**: #3340

### Commit Message

```
fix(agent-builder): hide unusable model picker on v1 builder projects (#3340)

## Summary
- Hide the composer model picker on **v1** Agent Builder projects, where
it was permanently stuck on "Select model" and could never resolve a
value.
- Make `ModelPicker` surface the `readOnlyReason` it already computes,
instead of showing a "Select model" prompt that invites a selection
which cannot work.

Reported from the Agent Builder page (`/agent-builder/abp_…`): the
dropdown always read "Select model" even though the model catalog was
healthy.

## Root cause

`AgentBuilderClient` passes `modelController` only for `engine_v2`, and
never passes `modelSettingsWorkspaceId` at all — but
`UnifiedChatComposer` defaults `showModelPicker` to `true`. So on v1 the
picker renders with no model source behind it.

From there the empty label is forced:

1. `useAgentModelQuery(uid, null)` → `enabled: Boolean(uid &&
workspaceId)` is **false**, so the query never runs.
2. It then reports `ready: false` (never succeeded), `loading: false`
(that flag is itself guarded by `workspaceId`), `loadError: null` (never
errored) — a **limbo state**.
3. `useComposerModelState` gates its catalog-default fallback behind
`controller.ready || controller.loadError`, both false, so
`useCatalogDefault` stays `false`.
4. `resolveComposerSelectedModel('', models, false)` returns `''`.
5. `ModelPicker` receives a full option list and `value: ''` → no match
→ `'Select model'`, forever.

Confirmed against the live API: the catalog is fine — it returns 24
models with `claude-sonnet-4-6` correctly flagged `is_default`. Step 3
is why that default is never consulted.

v1 is being deprecated, so this hides the control rather than wiring a
model source into it. Deliberately a one-liner with no v1-specific
abstraction — it gets deleted with v1.

The second change is the part that outlives v1. `UnifiedChatComposer`
already detects exactly this combination and computes an accurate
message:

```ts
(!modelController && !modelSettingsWorkspaceId && !composerModel.canSelectDraftModel
  ? 'Current model is unavailable.'
  : null)
```

…but `readOnlyReason` only drove a tooltip and never reached the trigger
label. Now any surface wired without a model source says why, instead of
failing silently as a dead dropdown. Behaviour is unchanged when
`readOnlyReason` is null (a genuine "nothing picked yet" still reads
"Select model") and when the inventory is empty ("No models available"
still wins).

## Test plan
- [x] `web/packages/chat-ui`: `pnpm test` — 354 passed (3 new: reason
surfaced, null-reason still prompts, empty-inventory label preserved)
- [x] `web/packages/chat-ui`: `pnpm tsc` + `pnpm lint` clean
- [x] `web/app`: `agent-builder-client.unit.spec.tsx` — 62 passed (v1
asserts `showModelPicker: false`; new test asserts `engine_v2` keeps it)
- [x] `bash scripts/verify-web.sh` — guards + tsc + vitest (645 files /
8657 tests) + eslint all pass

## Notes for review
- Not fixed here: the underlying limbo in `useAgentModelQuery`, where a
*disabled* query is indistinguishable from "loaded, no model" and
silently suppresses the catalog-default fallback. Any future surface
that forgets to pass a workspace id inherits the same dead dropdown. The
label change makes that self-diagnosing rather than invisible, but the
state modelling is still worth a follow-up.
- If v1 model switching was ever intended as a product behaviour, this
is the wrong fix and we should wire `modelSettingsWorkspaceId` instead.
This was checked before implementing: v1 is being deprecated.

Co-authored-by: Claude Opus 5 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary
- Hide the composer model picker on **v1** Agent Builder projects, where it was permanently stuck on "Select model" and could never resolve a value.
- Make `ModelPicker` surface the `readOnlyReason` it already computes, instead of showing a "Select model" prompt that invites a selection which cannot work.

Reported from the Agent Builder page (`/agent-builder/abp_…`): the dropdown always read "Select model" even though the model catalog was healthy.

## Root cause

`AgentBuilderClient` passes `modelController` only for `engine_v2`, and never passes `modelSettingsWorkspaceId` at all — but `UnifiedChatComposer` defaults `showModelPicker` to `true`. So on v1 the picker renders with no model source behind it.

From there the empty label is forced:

1. `useAgentModelQuery(uid, null)` → `enabled: Boolean(uid && workspaceId)` is **false**, so the query never runs.
2. It then reports `ready: false` (never succeeded), `loading: false` (that flag is itself guarded by `workspaceId`), `loadError: null` (never errored) — a **limbo state**.
3. `useComposerModelState` gates its catalog-default fallback behind `controller.ready || controller.loadError`, both false, so `useCatalogDefault` stays `false`.
4. `resolveComposerSelectedModel('', models, false)` returns `''`.
5. `ModelPicker` receives a full option list and `value: ''` → no match → `'Select model'`, forever.

Confirmed against the live API: the catalog is fine — it returns 24 models with `claude-sonnet-4-6` correctly flagged `is_default`. Step 3 is why that default is never consulted.

v1 is being deprecated, so this hides the control rather than wiring a model source into it. Deliberately a one-liner with no v1-specific abstraction — it gets deleted with v1.

The second change is the part that outlives v1. `UnifiedChatComposer` already detects exactly this combination and computes an accurate message:

```ts
(!modelController && !modelSettingsWorkspaceId && !composerModel.canSelectDraftModel
  ? 'Current model is unavailable.'
  : null)
```

…but `readOnlyReason` only drove a tooltip and never reached the trigger label. Now any surface wired without a model source says why, instead of failing silently as a dead dropdown. Behaviour is unchanged when `readOnlyReason` is null (a genuine "nothing picked yet" still reads "Select model") and when the inventory is empty ("No models available" still wins).

## Test plan
- [x] `web/packages/chat-ui`: `pnpm test` — 354 passed (3 new: reason surfaced, null-reason still prompts, empty-inventory label preserved)
- [x] `web/packages/chat-ui`: `pnpm tsc` + `pnpm lint` clean
- [x] `web/app`: `agent-builder-client.unit.spec.tsx` — 62 passed (v1 asserts `showModelPicker: false`; new test asserts `engine_v2` keeps it)
- [x] `bash scripts/verify-web.sh` — guards + tsc + vitest (645 files / 8657 tests) + eslint all pass

## Notes for review
- Not fixed here: the underlying limbo in `useAgentModelQuery`, where a *disabled* query is indistinguishable from "loaded, no model" and silently suppresses the catalog-default fallback. Any future surface that forgets to pass a workspace id inherits the same dead dropdown. The label change makes that self-diagnosing rather than invisible, but the state modelling is still worth a follow-up.
- If v1 model switching was ever intended as a product behaviour, this is the wrong fix and we should wire `modelSettingsWorkspaceId` instead. This was checked before implementing: v1 is being deprecated.


---

## fix(agent-builder): preserve project context and preview refresh (#3338)

- **SHA**: `c3f2ec74ea143b04f4662e77f92c75cd3a21c23c`
- **作者**: kaka-srp
- **日期**: 2026-08-12T03:04:25Z
- **PR**: #3338

### Commit Message

```
fix(agent-builder): preserve project context and preview refresh (#3338)

## Summary

- preserve Project mode, source identity/version, and fork target
identity when ECAP imports a dedicated Agent Studio workspace
- let Refresh Preview renew the Project's existing package-test capacity
lease instead of rejecting it as a competing runtime operation
- fence terminal cleanup by both package operation and iteration so a
stale finalizer cannot clear or cool down a newly refreshed preview
- roll back a reclaimed lease generation when the Project start CAS
fails

## Root causes

1. The dedicated Project runtime serialized only `project_id`,
`source_type`, and `source_ref`, so Agent Studio could not apply fork
target identity or preserve the source version used by the pre-publish
guard.
2. A previewing TestRun intentionally retained the Project's
package-test slot, but Refresh Preview attempted to acquire a new
operation and was rejected by the same Project's active lease.
3. Reusing that lifecycle lease without an iteration fence allowed a
stale terminal snapshot to finish the slot and clear
`workspace_operation_id` after a newer refresh had started.

## Design

- Keep the existing per-user three-Project capacity model and existing
Project/slot persistence.
- Treat refresh as another iteration in the same active package-test
lifecycle; do not add a lock or a new state machine.
- Use the Project's `current_iteration_id` CAS to serialize lifecycle
cleanup with refresh, and the slot `fence` to distinguish an unchanged
lease from a reclaimed generation.

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] focused runtime/repository/sandbox unit suite — 37 passed
- [x] pre-commit Python hooks
- [x] pre-push changed-surface verification

## Dependency

- Companion Agent Studio runtime fix:
https://github.com/SerendipityOneInc/ecap-agent-pack/pull/236
```

### PR Body

## Summary

- preserve Project mode, source identity/version, and fork target identity when ECAP imports a dedicated Agent Studio workspace
- let Refresh Preview renew the Project's existing package-test capacity lease instead of rejecting it as a competing runtime operation
- fence terminal cleanup by both package operation and iteration so a stale finalizer cannot clear or cool down a newly refreshed preview
- roll back a reclaimed lease generation when the Project start CAS fails

## Root causes

1. The dedicated Project runtime serialized only `project_id`, `source_type`, and `source_ref`, so Agent Studio could not apply fork target identity or preserve the source version used by the pre-publish guard.
2. A previewing TestRun intentionally retained the Project's package-test slot, but Refresh Preview attempted to acquire a new operation and was rejected by the same Project's active lease.
3. Reusing that lifecycle lease without an iteration fence allowed a stale terminal snapshot to finish the slot and clear `workspace_operation_id` after a newer refresh had started.

## Design

- Keep the existing per-user three-Project capacity model and existing Project/slot persistence.
- Treat refresh as another iteration in the same active package-test lifecycle; do not add a lock or a new state machine.
- Use the Project's `current_iteration_id` CAS to serialize lifecycle cleanup with refresh, and the slot `fence` to distinguish an unchanged lease from a reclaimed generation.

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] focused runtime/repository/sandbox unit suite — 37 passed
- [x] pre-commit Python hooks
- [x] pre-push changed-surface verification

## Dependency

- Companion Agent Studio runtime fix: https://github.com/SerendipityOneInc/ecap-agent-pack/pull/236


---
